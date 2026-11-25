"""Verify the offline distribution with a copied model, outside the source tree."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import secrets
import shutil
import subprocess
import sys
import tempfile
import venv
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "ai_governance/genai_governance/stale_evidence_decay"


def exercise(model):
    import model_policy_engine
    from model_policy_engine.schema import catalog, TEMPLATES
    if not Path(model_policy_engine.__file__).resolve().is_relative_to(Path(sys.prefix)):
        raise RuntimeError("Expected the installed wheel")
    home = Path(os.environ["MODEL_POLICY_HOME"])
    relative = catalog()[MODEL_ID]
    draft = home / "drafts" / relative
    draft.parent.mkdir(parents=True)
    (home / "keyring.json").write_text(json.dumps({"active_key_id": "test", "keys": {"test": secrets.token_hex(32)}}))
    draft.write_bytes((TEMPLATES / relative).read_bytes())
    apply = [sys.executable, "-I", "-m", "model_policy_engine", "apply", str(draft)]
    subprocess.run(apply, check=True, capture_output=True)
    evaluate = runpy.run_path(model)["stale_evidence_decay"]
    before = evaluate(5, 10)
    draft.write_text(draft.read_text().replace('"default" = 1.0', '"default" = 3.0, fixed = true'))
    subprocess.run(apply, check=True, capture_output=True)
    after = evaluate(5, 10)
    if (before, after) != (0.5, 0.125):
        raise AssertionError((before, after))
    try:
        evaluate(5, 10, 2)
    except ValueError as exc:
        if "fixed" not in str(exc):
            raise
    else:
        raise AssertionError("Expected a fixed-value rejection")
    print(json.dumps({"catalog_entries": len(catalog()), "before": before, "after": after,
                      "explicit_conflict": "rejected", "model_id": MODEL_ID}))


def main():
    wheel, = ROOT.glob("model_policy_engine-1.1.0-*.whl")
    package = ROOT / "model_policy_engine"
    with ZipFile(wheel) as archive:
        sources = [*package.glob("*.py"), package / "protocol.toml", *(package / "policies").rglob("*.toml")]
        for path in sources:
            if archive.read(path.relative_to(ROOT).as_posix()) != path.read_bytes():
                raise ValueError(f"Wheel differs from source at {path.name}")
    with tempfile.TemporaryDirectory() as temp:
        work = Path(temp)
        env_dir = work / "env"
        venv.EnvBuilder().create(env_dir)
        python = env_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run([sys.executable, "-m", "pip", "--python", str(python), "install",
                        "--no-index", "--no-deps", str(wheel)], cwd=work, check=True, capture_output=True)
        model = shutil.copy(ROOT / "model_families" / (MODEL_ID + ".py"), work)
        env = dict(os.environ, MODEL_POLICY_HOME=str(work / "state"))
        env.pop("MODEL_POLICY_KEYRING_FILE", None)
        result = subprocess.run([str(python), "-I", __file__, "--exercise", model], cwd=work, env=env,
                                check=True, text=True, stdout=subprocess.PIPE)
    evidence = dict(json.loads(result.stdout), wheel=wheel.name, verified_files=len(sources),
                    sha256=hashlib.sha256(wheel.read_bytes()).hexdigest())
    (ROOT / "verification" / "wheel-result.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence))

if __name__ == "__main__":
    if sys.argv[1:2] == ["--exercise"]:
        exercise(sys.argv[2])
    else:
        main()
