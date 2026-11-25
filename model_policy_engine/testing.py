"""Run original smoke fixtures against disposable, explicitly admitted policies."""
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from .store import initialize


@contextmanager
def baseline_deployment():
    if os.environ.get("MODEL_POLICY_SMOKE_ACTIVE") and os.environ.get("MODEL_POLICY_HOME"):
        yield
        return
    saved = {key: os.environ.get(key) for key in (
        "MODEL_POLICY_HOME", "MODEL_POLICY_KEYRING_FILE", "MODEL_POLICY_SMOKE_ACTIVE", "PYTHONPATH"
    )}
    with TemporaryDirectory() as directory:
        root = Path(directory)
        try:
            # Child programs see only the engine on PYTHONPATH, including copied-model tests.
            lib = root / "lib"
            shutil.copytree(Path(__file__).parent, lib / "model_policy_engine",
                            ignore=shutil.ignore_patterns("__pycache__", "tests"))
            os.environ["PYTHONPATH"] = str(lib)
            os.environ.pop("MODEL_POLICY_KEYRING_FILE", None)
            os.environ["MODEL_POLICY_HOME"] = str(initialize(root / "deployment"))
            os.environ["MODEL_POLICY_SMOKE_ACTIVE"] = "1"
            yield
        finally:
            for key, value in saved.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

