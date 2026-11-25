"""Exercise three real terminal sessions against a local MCP server and disposable state."""
import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

from textual.widgets import Button, DataTable, Input, Static, TextArea

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from console_app.client import Remote
from console_app.config import digest, read_config
from console_app.server import provision
from console_app.tui import Console
from model_policy_engine import store
from model_policy_engine.schema import catalog

MODEL = "ai_governance/genai_governance/stale_evidence_decay"

def snapshot(home):
    return {p.relative_to(home): (p.stat().st_mtime_ns, digest(p.read_bytes()))
            for p in home.rglob("*") if p.is_file()}

async def denied(remote, tool, **args):
    try:
        await remote.call(tool, **args)
    except TypeError:
        raise
    except Exception:
        return
    raise AssertionError(f"Unexpected grant for {tool}")

async def witness(tmp):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    config = tmp / "console.toml"
    config.write_text((ROOT / "console.toml").read_text().replace("port = 8766", f"port = {port}")
                      .replace("poll_seconds = 3", "poll_seconds = 0.5"))
    pin = digest(config.read_bytes())
    invalid = tmp / "invalid-budget.toml"
    invalid.write_bytes(config.read_bytes().replace(b"max_inflight = 24", b"max_inflight = 0"))
    try:
        read_config(invalid, digest(invalid.read_bytes()))
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid runtime budget was admitted")
    settings = read_config(config, pin)
    assert settings["port"] == port
    keys = tmp / "credentials"
    provision(keys)
    home = tmp / "state"
    with patch.dict(os.environ, MODEL_POLICY_HOME=str(home)):
        os.environ.pop("MODEL_POLICY_KEYRING_FILE", None)
        store.initialize(home)
        proc = subprocess.Popen([sys.executable, "-B", "-m", "console_app.server", "serve", "--policy", str(config),
                                 "--sha256", pin, "--credentials", str(keys)], cwd=ROOT)
    clients = {r: Remote(port, keys / (r + ".token")) for r in settings["roles"]}
    try:
        for _ in range(100):
            if proc.poll() is not None:
                raise RuntimeError("Server exited")
            try:
                reader, writer = await asyncio.open_connection("127.0.0.1", port)
                writer.close()
                await writer.wait_closed()
                break
            except OSError:
                await asyncio.sleep(0.1)
        before = snapshot(home)
        viewer = clients["viewer"]
        panel = Console(viewer)
        async with panel.run_test(size=(110, 38)) as pilot:
            await pilot.pause()
            assert panel.sub_title == "Viewer" and panel.query_one(DataTable).row_count == len(catalog())
            assert not panel.query_one("#open").display and not panel.query_one("#run").display
            panel.query_one(Input).value = "stale_evidence_decay"
            await pilot.pause()
            assert panel.selected == MODEL
            assert snapshot(home) == before
            await denied(viewer, "policy.open", model=MODEL)
            await denied(viewer, "task.execute", name="evidence_decay", inputs={}, revision="")
            assert snapshot(home) == before
            admin = clients["admin"]
            initial = await admin.call("policy.open", model=MODEL)
            external = await admin.call("policy.apply", model=MODEL, source=initial["toml"] + "\n# viewer witness\n",
                                        draft_sha256=initial["draft_sha256"], revision=initial["revision"])
            for _ in range(60):
                await asyncio.sleep(0.1)
                if panel.rows[MODEL]["revision"] == external["revision"]:
                    break
            assert panel.rows[MODEL]["revision"] == external["revision"]
        editor = Console(admin)
        async with editor.run_test(size=(110, 38)) as admin_pilot:
            editor.query_one(Input).value = "stale_evidence_decay"
            await admin_pilot.pause()
            await admin_pilot.click("#open")
            await admin_pilot.pause()
            old = dict(editor.edit)
            text = old["toml"].replace('"default" = 1.0', '"default" = 3.0, fixed = true')
            editor.query_one(TextArea).load_text(text)
            editor.query_one("#apply", Button).press()
            for _ in range(60):
                await asyncio.sleep(0.1)
                if editor.edit["revision"] != old["revision"]:
                    break
            assert editor.edit["revision"] != old["revision"]
            new_revision = editor.edit["revision"]
            await denied(admin, "policy.apply", model=MODEL, source=text, revision=old["revision"],
                         draft_sha256=old["draft_sha256"])
            await denied(admin, "policy.apply", model=MODEL, source="broken =", revision=new_revision,
                         draft_sha256=editor.edit["draft_sha256"])
            assert (await admin.call("policy.open", model=MODEL))["revision"] == new_revision
            await denied(admin, "task.execute", name="evidence_decay", inputs={}, revision=new_revision)
        agent = clients["agent"]
        actor = Console(agent)
        async with actor.run_test(size=(110, 38)) as agent_pilot:
            actor.query_one(Input).value = "stale_evidence_decay"
            await agent_pilot.pause()
            assert len(actor.rows) == 2 and not actor.query_one("#open").display
            await agent_pilot.click("#run")
            for _ in range(60):
                await asyncio.sleep(0.1)
                if list((home / "receipts").glob("*.json")):
                    break
            assert list((home / "receipts").glob("*.json")), (actor.selected, actor.query_one("#run").region, actor.query_one("#tasks").value, actor.query_one(TextArea).text, actor.query_one("#feedback", Static).content)
            receipt_path, = (home / "receipts").glob("*.json")
            receipt = json.loads(receipt_path.read_bytes())
            observer = await viewer.call("inventory.read")
            assert next(r for r in observer["rows"] if r["model"] == MODEL)["latest"]["id"] == receipt["id"]
            assert receipt["result"] == 0.125 and receipt["revision"] == new_revision
            await agent_pilot.pause()
            assert receipt["id"] in str(actor.query_one("#feedback", Static).content)
            await denied(agent, "policy.open", model=MODEL)
            for name, inputs, revision in [("unlisted", {}, new_revision),
                                          ("evidence_decay", {"decay_power": 2}, new_revision),
                                          ("evidence_decay", receipt["inputs"], old["revision"])]:
                await denied(agent, "task.execute", name=name, inputs=inputs, revision=revision)
            assert list((home / "receipts").glob("*.json")) == [receipt_path]
            active = home / "active" / catalog()[MODEL]
            active.write_text("invalid")
            await actor.action_refresh_now()
            assert actor.rows[MODEL]["state"] == "unverified" and actor.query_one("#run").disabled
            await denied(agent, "task.execute", name="evidence_decay", inputs=receipt["inputs"], revision=new_revision)
        (keys / "bad.token").write_text("invalid")
        await denied(Remote(port, keys / "bad.token"), "inventory.read")
        return {"status": "PASS", "inventory": len(catalog()), "transport": "stateless loopback HTTP",
                "verified": ["read-only poll leaves file bytes and mtimes intact", "filter follows selected model",
                             "live polling observes publication", "invalid and stale edits rejected",
                             "role separation on wire and in TUI", "tampered policy withheld",
                             "stale and unlisted tasks rejected", "terminal effect matches persisted receipt"],
                "effect": receipt}
    finally:
        proc.terminate()
        proc.wait(timeout=15)

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        report = asyncio.run(witness(Path(folder)))
    (ROOT / "verification/console-witness.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: three Textual roles, real MCP and persisted effect")
