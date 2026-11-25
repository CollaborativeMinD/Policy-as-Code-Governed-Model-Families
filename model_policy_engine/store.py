"""Explicit local signing and publication; model processes only verify policies."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile
import time
from functools import lru_cache

from .locking import state_transaction
from .policy_loader import PolicyLoader, PolicyManifest, PolicySecurityError
from .schema import TEMPLATES, admit, catalog


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as f:
        temp = Path(f.name)
        try:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        except BaseException:
            f.close()
            temp.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _keys(home):
    path = Path(os.environ.get("MODEL_POLICY_KEYRING_FILE", home / "keyring.json"))
    try:
        payload = json.loads(path.read_bytes())
        return {k: bytes.fromhex(v) for k, v in payload["keys"].items()}, payload["active_key_id"]
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise PolicySecurityError(f"Cannot read the configured policy keyring at {path}") from exc


def _loader(home, model_id):
    keys, active = _keys(home)
    return _cached_loader(home, model_id, tuple(sorted(keys.items())), active)


@lru_cache(maxsize=512)
def _cached_loader(home, model_id, keys, active):
    return PolicyLoader(dict(keys), active, home / "state", home / "quarantine",
                        policy_validator=lambda parsed: admit(model_id, parsed))


def home_path():
    home = os.environ.get("MODEL_POLICY_HOME")
    if not home:
        raise PolicySecurityError("Set MODEL_POLICY_HOME to an initialized policy deployment")
    return Path(home).resolve()


def load_model(model_id):
    home = home_path()
    return _loader(home, model_id).load(home / "active" / catalog()[model_id])


def publish(home, draft, *, epoch=None, override=None):
    """Publish one operator-selected draft. Authenticate and admit the exact bytes."""
    home, draft = Path(home).resolve(), Path(draft).resolve()
    relative = draft.relative_to(home / "drafts")
    expected = {path: model_id for model_id, path in catalog().items()}.get(relative)
    if expected is None:
        raise ValueError("Draft is outside the installed model catalog")
    with state_transaction(home / "state"):
        loader = _loader(home, expected)
        with draft.open("rb") as stream:
            raw = stream.read(loader._max_bytes + 1)
        # Do not replace an active pair with a malformed or wrongly routed draft.
        candidate = loader._parse_and_validate_policy(raw)
        path = home / "active" / relative
        digest = hashlib.sha256(raw).hexdigest()
        loader._load_persisted_lkg(path)
        previous = loader._memory_cache.get(path)
        stamp = epoch
        if stamp is None:
            stamp = max(int(time.time()), previous[1] + 1 if previous else 1)
        key = loader._active_key_id
        canonical = f"manifest:v3:{key}:{path.name}:{candidate.version}:{stamp}:{digest}"
        manifest = PolicyManifest(key_id=key, target_file=path.name, policy_version=candidate.version,
                                  issued_at_epoch=stamp, sha256=digest,
                                  hmac_sha256=loader._compute_hmac(key, canonical))
        manifest_path = path.with_suffix(".toml.manifest.json")
        old_files = {p: p.read_bytes() if p.exists() else None for p in (path, manifest_path)}
        try:
            _write(path, raw)
            _write(manifest_path, manifest.model_dump_json(indent=2).encode())
            return loader.load(path, allow_fallback=False, override_token_path=override)
        except (OSError, PolicySecurityError):
            for previous_path, previous_bytes in old_files.items():
                if previous_bytes is None:
                    previous_path.unlink(missing_ok=True)
                else:
                    _write(previous_path, previous_bytes)
            raise


def initialize(home):
    home = Path(home).resolve()
    home.mkdir(parents=True, exist_ok=True)
    with state_transaction(home / "state"):
        if not os.environ.get("MODEL_POLICY_KEYRING_FILE") and not (home / "keyring.json").exists():
            _write(home / "keyring.json", json.dumps({
                "active_key_id": "local", "keys": {"local": secrets.token_hex(32)}
            }).encode())
        _keys(home)
        for model_id, relative in catalog().items():
            draft = home / "drafts" / relative
            target = home / "active" / relative
            if target.exists() and target.with_suffix(".toml.manifest.json").exists():
                continue
            loader = _loader(home, model_id)
            if loader._lkg_file_path(target.resolve()).exists():
                continue
            baseline = (TEMPLATES / relative).read_bytes()
            if draft.is_file() and draft.read_bytes() != baseline:
                continue
            _write(draft, baseline)
            publish(home, draft)
    return home

