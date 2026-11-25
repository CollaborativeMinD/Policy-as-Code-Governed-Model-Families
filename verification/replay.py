"""Replay shipped directory fixtures with disposable admissions and record per-model coverage."""
import hashlib
import json
import logging
import os
from pathlib import Path
import platform
import re
import runpy
import secrets
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "model_families"
sys.path.insert(0, str(ROOT))
import model_policy_engine
from model_policy_engine import store
from model_policy_engine.schema import catalog
from model_policy_engine.policy_loader import PolicySecurityError

# Mixed directories retain their individual civilian fixtures.
EXCLUDED = {
    "space-and-comms/communications_and_radar",
}

def replay_group(smoke, names):
    logging.getLogger("model_policy_engine.policy_loader").setLevel(logging.CRITICAL)
    scope = runpy.run_path(smoke)
    for name in names:
        fixture = scope["FIXTURES"][name]
        with patch.dict(os.environ, MODEL_POLICY_HOME=os.environ["EMPTY_POLICY_HOME"]):
            try:
                scope["isolated_model"](name, fixture)
            except PolicySecurityError:
                pass
            else:
                raise AssertionError(f"{name} ran without admission")
        model_id = (Path(smoke).parent / name).relative_to(MODELS).with_suffix("").as_posix()

        def check_hot(module):
            observed = []
            original_loader = model_policy_engine.load_model
            def observe(requested):
                admitted = original_loader(requested)
                observed.append((admitted.model_id, admitted.version))
                return admitted

            def check_version(version):
                observed.clear()
                with patch.object(model_policy_engine, "load_model", observe):
                    fixture(module)
                if set(observed) != {(model_id, version)}:
                    raise AssertionError((model_id, version, observed))

            draft = Path(os.environ["MODEL_POLICY_HOME"]) / "drafts" / catalog()[model_id]
            old = store.load_model(model_id).version
            check_version(old)
            major, minor, revision = old.split(".")
            new = f"{major}.{minor}.{int(revision) + 1}"
            source = draft.read_text(encoding="utf8")
            source, count = re.subn(r'^version = "[^"]+"$', f'version = "{new}"', source, flags=re.M)
            if count != 1:
                raise AssertionError(f"Expected one version in {model_id}")
            draft.write_text(source, encoding="utf8")
            store.publish(Path(os.environ["MODEL_POLICY_HOME"]), draft)
            check_version(new)
            print("REVISION", model_id, old, new, hashlib.sha256(draft.read_bytes()).hexdigest())

        scope["isolated_model"](name, check_hot)
        print("CHECKED", name)


def replay_suite(path):
    sys.path.insert(0, str(path.parent))
    suite = unittest.defaultTestLoader.discover(str(path.parent), pattern=path.name)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return not (result.testsRun and result.wasSuccessful())


def main():
    results = []
    lineage = {}
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        key = home / "keyring.json"
        key.write_text(json.dumps({"keys": {"test": secrets.token_hex(32)}, "active_key_id": "test"}))
        os.environ.update(MODEL_POLICY_HOME=str(home), MODEL_POLICY_KEYRING_FILE=str(key))
        env = dict(os.environ, PYTHONPATH=str(ROOT), MODEL_POLICY_SMOKE_ACTIVE="1", EMPTY_POLICY_HOME=str(home / "empty"))
        groups = {}
        for model_id, relative in catalog().items():
            if model_id in EXCLUDED:
                continue
            draft = home / "drafts" / relative
            draft.parent.mkdir(parents=True, exist_ok=True)
            draft.write_bytes((store.TEMPLATES / relative).read_bytes())
            store.publish(home, draft)
            model = MODELS / (model_id + ".py")
            lineage[model_id] = {"model_sha256": hashlib.sha256(model.read_bytes()).hexdigest(),
                                 "policy_sha256": hashlib.sha256(draft.read_bytes()).hexdigest()}
            groups.setdefault(model.parent, []).append(model.name)
        def run(label, args):
            proc = subprocess.run([sys.executable, "-S", "-P", "-B", "-X", "utf8", *args],
                                  env=env, cwd=ROOT, capture_output=True, text=True, encoding="utf8")
            results.append({"scope": label, "exit": proc.returncode, "stdout": proc.stdout,
                            "stderr": proc.stderr})
            if proc.returncode:
                print(label, proc.stderr[-950:], flush=True)
        for directory, names in sorted(groups.items()):
            smoke = directory / "smoke_test.py"
            run(directory.relative_to(MODELS).as_posix(), [__file__, "--group", str(smoke), *sorted(names)])
        for suite in sorted(MODELS.rglob("test_*.py")):
            group = suite.parent.parent if suite.parent.name.lower() == "tests" else suite.parent
            if group not in groups:
                continue
            run(suite.relative_to(MODELS).as_posix(), [__file__, "--suite", str(suite)])
    report = {"python": platform.python_version(), "excluded_from_full_fixture_replay": sorted(EXCLUDED),
              "catalog_entries": len(catalog()), "models_replayed": sum(
                  line.startswith("CHECKED ") for result in results for line in result["stdout"].splitlines()),
              "model_and_policy_inputs": lineage, "failed_groups": sum(bool(r["exit"]) for r in results), "results": results}
    (ROOT / "verification" / "fixture-results.json").write_text(json.dumps(report, indent=2)+"\n")
    print({k:v for k,v in report.items() if k not in ("results", "model_and_policy_inputs")})
    return bool(report["failed_groups"])

if __name__ == "__main__":
    if sys.argv[1:2] == ["--group"]:
        replay_group(sys.argv[2], sys.argv[3:])
    elif sys.argv[1:2] == ["--suite"]:
        sys.exit(replay_suite(Path(sys.argv[2])))
    else:
        sys.exit(main())
