"""Unit tests for reconciled PolicyLoader."""

import hashlib
import hmac
from pathlib import Path
import tempfile
import time
import unittest

from model_policy_engine.policy_loader import (
    PolicyLoader,
    PolicyManifest,
    PolicySecurityError,
    RollbackOverrideToken,
)


def _sign(secret: bytes, payload: str) -> str:
    return hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()


class TestPolicyLoader(unittest.TestCase):
    """Validates keyring verification, rotation, anti-rollback, and break-glass override."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.key_v1 = b"A" * 32
        self.key_v2 = b"B" * 32
        self.keyring = {"k1": self.key_v1, "k2": self.key_v2}
        self.policy_path = self.root / "policy.toml"
        self.manifest_path = self.root / "policy.toml.manifest.json"
        self.override_path = self.root / "override.json"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write_policy(
        self, version: str, epoch: int, key_id: str, secret: bytes
    ) -> str:
        content = (
            f'version = "{version}"\n'
            "strict_mode = true\n"
            'allowed_actions = ["read", "audit"]\n'
            "max_retries = 3\n"
        ).encode("utf-8")
        self.policy_path.write_bytes(content)
        sha = hashlib.sha256(content).hexdigest()
        canonical = (
            f"manifest:v3:{key_id}:{self.policy_path.name}:{version}:{epoch}:{sha}"
        )
        manifest = PolicyManifest(
            key_id=key_id,
            target_file=self.policy_path.name,
            policy_version=version,
            issued_at_epoch=epoch,
            sha256=sha,
            hmac_sha256=_sign(secret, canonical),
        )
        self.manifest_path.write_text(
            manifest.model_dump_json(indent=2), encoding="utf-8"
        )
        return sha

    def test_load_and_key_rotation_cold_boot(self) -> None:
        """Loads v1.2.0 under k1, then cold-boots under k2 and re-seals LKG."""
        self._write_policy("1.2.0", 1000, "k1", self.key_v1)
        loader1 = PolicyLoader(
            keyring={"k1": self.key_v1},
            active_key_id="k1",
            lkg_state_dir=self.root / "lkg",
            quarantine_dir=self.root / "quarantine",
        )
        pol1 = loader1.load(self.policy_path)
        self.assertEqual(pol1.version, "1.2.0")

        loader2 = PolicyLoader(
            keyring=self.keyring,
            active_key_id="k2",
            lkg_state_dir=self.root / "lkg",
            quarantine_dir=self.root / "quarantine",
        )
        pol2 = loader2.load(self.policy_path)
        self.assertEqual(pol2.version, "1.2.0")

    def test_rollback_blocked_and_break_glass_single_use(self) -> None:
        """Blocks unapproved downgrade, allows signed override once, blocks replay."""
        self._write_policy("2.0.0", 2000, "k2", self.key_v2)
        loader = PolicyLoader(
            keyring=self.keyring,
            active_key_id="k2",
            lkg_state_dir=self.root / "lkg",
            quarantine_dir=self.root / "quarantine",
        )
        self.assertEqual(loader.load(self.policy_path).version, "2.0.0")

        # Attempt downgrade without override -> quarantined + LKG fallback
        self._write_policy("1.5.0", 1500, "k2", self.key_v2)
        pol_fallback = loader.load(self.policy_path, allow_fallback=True)
        self.assertEqual(pol_fallback.version, "2.0.0")

        # Rewrite old policy + valid break-glass token
        sha_old = self._write_policy("1.5.0", 1500, "k2", self.key_v2)
        expires = int(time.time()) + 300
        token_id = "breakglass-0001"
        operator = "ops-lead"
        reason = "Emergency regression mitigation"
        canonical_tok = (
            f"override:v1:k2:{token_id}:{operator}:{self.policy_path.name}:"
            f"1.5.0:{sha_old}:{expires}:{reason}"
        )
        token = RollbackOverrideToken(
            token_id=token_id,
            key_id="k2",
            operator_id=operator,
            reason=reason,
            target_file=self.policy_path.name,
            approved_version="1.5.0",
            approved_sha256=sha_old,
            expires_at_epoch=expires,
            hmac_sha256=_sign(self.key_v2, canonical_tok),
        )
        self.override_path.write_text(
            token.model_dump_json(indent=2), encoding="utf-8"
        )

        pol_downgraded = loader.load(
            self.policy_path, override_token_path=self.override_path
        )
        self.assertEqual(pol_downgraded.version, "1.5.0")
        self.assertFalse(self.override_path.exists())

        # Upgrade back to 2.0.0 then try replaying the same token_id
        self._write_policy("2.0.0", 2100, "k2", self.key_v2)
        self.assertEqual(loader.load(self.policy_path).version, "2.0.0")
        self._write_policy("1.5.0", 1500, "k2", self.key_v2)
        self.override_path.write_text(
            token.model_dump_json(indent=2), encoding="utf-8"
        )
        with self.assertRaises(PolicySecurityError):
            loader.load(
                self.policy_path,
                override_token_path=self.override_path,
                allow_fallback=False,
            )


if __name__ == "__main__":
    unittest.main()
