"""Console effects run under the model engine's existing publication lock."""
from collections import Counter
from datetime import datetime, timezone
import json
import runpy
import threading
import tomllib
from uuid import uuid4

from model_policy_engine import store
from model_policy_engine.locking import state_transaction
from model_policy_engine.policy_loader import PolicyLoader, PolicySecurityError
from model_policy_engine.schema import TEMPLATES, admit, catalog
from .config import ROOT, digest


class Service:
    def __init__(self, config):
        self.config = config
        self.home = store.home_path()
        self.running = Counter()
        self.latest = {}
        self.lock = threading.Lock()

    def inspect(self, model):
        keys, active = store._keys(self.home)
        loader = PolicyLoader(keys, active, self.home / "state", self.home / "quarantine",
                              policy_validator=lambda doc: admit(model, doc))
        return loader.inspect_active(self.home / "active" / catalog()[model])

    def inventory(self, role):
        tasks = self.config["tasks"]
        scoped = {task["model"] for task in tasks.values()}
        rows = []
        for model in catalog():
            if role == "agent" and model not in scoped:
                continue
            row = {"model": model, "state": "inactive", "version": "", "revision": "", "tasks": {}}
            try:
                current = self.inspect(model)
                if current:
                    _, manifest = current
                    row.update(state="active", version=manifest.policy_version,
                               revision=f"{manifest.issued_at_epoch}/{manifest.sha256}")
                    if role == "agent" and "task.execute" in self.config["roles"][role]:
                        row["tasks"] = {name: task for name, task in tasks.items() if task["model"] == model}
            except (OSError, ValueError, PolicySecurityError):
                row["state"] = "unverified"
            with self.lock:
                row["running"] = self.running[model]
                row["latest"] = self.latest.get(model)
            rows.append(row)
        return {"role": role, "tools": self.config["roles"][role], "poll_seconds": self.config["poll_seconds"],
                "rows": rows}

    def open_policy(self, model):
        relative = catalog()[model]
        active = self.inspect(model)
        draft = self.home / "drafts" / relative
        raw = draft.read_bytes() if draft.is_file() else (TEMPLATES / relative).read_bytes()
        revision = f"{active[1].issued_at_epoch}/{active[1].sha256}" if active else ""
        return {"model": model, "toml": raw.decode(), "draft_sha256": digest(raw), "revision": revision}

    def apply(self, model, source, draft_sha256, revision):
        with state_transaction(self.home / "state"):
            old = self.open_policy(model)
            if (old["draft_sha256"], old["revision"]) != (draft_sha256, revision):
                raise ValueError("Policy changed since opening. Reload before applying.")
            raw = source.encode()
            admit(model, tomllib.loads(source))
            path = self.home / "drafts" / catalog()[model]
            existed = path.exists()
            store._write(path, raw)
            try:
                store.publish(self.home, path)
            except Exception:
                if existed:
                    store._write(path, old["toml"].encode())
                else:
                    path.unlink(missing_ok=True)
                raise
            return {"disposition": "published", **self.open_policy(model)}

    def execute(self, name, inputs, revision):
        task = self.config["tasks"].get(name)
        if not task or not isinstance(inputs, dict) or inputs.keys() != task["inputs"].keys():
            raise ValueError("Task or input outside policy scope")
        model = task["model"]
        with state_transaction(self.home / "state"):
            current = self.inspect(model)
            if not current or revision != f"{current[1].issued_at_epoch}/{current[1].sha256}":
                raise ValueError("Task requires the selected active policy revision")
            with self.lock:
                self.running[model] += 1
            try:
                path = ROOT / "model_families" / (model + ".py")
                fn = runpy.run_path(str(path))[task["operation"]]
                result = fn(**inputs)
                receipt = {"id": uuid4().hex, "at": datetime.now(timezone.utc).isoformat(),
                           "task": name, "model": model, "operation": task["operation"], "revision": revision,
                           "model_sha256": digest(path.read_bytes()), "inputs": inputs, "result": result,
                           "disposition": "executed"}
                store._write(self.home / "receipts" / (receipt["id"] + ".json"),
                             json.dumps(receipt, allow_nan=False).encode())
                with self.lock:
                    self.latest[model] = {k: receipt[k] for k in ("id", "at", "task", "disposition", "revision")}
                return receipt
            finally:
                with self.lock:
                    self.running[model] -= 1
