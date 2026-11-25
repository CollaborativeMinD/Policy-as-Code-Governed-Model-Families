"""
Production Policy Loader with Keyring Rotation, Break-Glass Override, and LKG.

To support key rotation (key_id keyring lookup) and break-glass emergency
downgrades (signed rollback authorization tokens), this module provides:

1. Keyring-Based HMAC Verification (keyring: dict[str, bytes], active_key_id: str):
   - Manifests and persisted LKG envelopes include a key_id field bound inside
     the HMAC-SHA256 canonical payload.
   - During key rotation, old keys remain in keyring for verification of
     existing manifests and persisted LKG envelopes, while new LKG persists
     are automatically re-sealed using active_key_id.

2. Break-Glass Rollback Authorization Token (RollbackOverrideToken):
   - When an operator needs to execute a legitimate emergency downgrade, they
     supply an HMAC-signed token bound to the exact target filename, target
     SHA-256 digest, target version, and expiration timestamp (expires_at_epoch).
   - Single-use replay protection tracks consumed token_id values on disk
     (HMAC-sealed) so a captured break-glass token cannot be reused.
"""

import base64
from datetime import datetime, timezone
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import shutil
import tempfile
import time
import tomllib
from .locking import state_transaction

from .protocol import (ConsumedTokensLedger, GoverningPolicy, PersistedLKGEnvelope,
                       PolicyManifest, RollbackOverrideToken)

logger = logging.getLogger(__name__)


class PolicySecurityError(RuntimeError):
    """Raised on HMAC failure, unknown key_id, SHA mismatch, rollback, or invalid override."""


class PolicyPayloadError(ValueError):
    """Raised when TOML syntax, size, or schema validation fails."""


def _parse_semver(version_str: str) -> tuple[int, int, int]:
    """Parses a strict X.Y.Z semantic version string into an integer tuple."""
    major, minor, patch = version_str.split(".")
    return (int(major), int(minor), int(patch))


class PolicyLoader:
    """Fail-closed policy loader with keyring rotation, anti-rollback, and LKG.

    Features:
    - Keyring-based HMAC-SHA256 verification and seamless key rotation
    - Anti-rollback watermark enforcement (SemVer + monotonic issued_at_epoch)
    - Single-use, time-bounded, target-pinned break-glass rollback override tokens
    - Forensic quarantine on tamper or unauthorized rollback
    - Authenticated, atomic on-disk LKG persistence for cold-boot resilience
    """

    def __init__(
        self,
        keyring: dict[str, bytes],
        active_key_id: str,
        lkg_state_dir: str | Path = "./state/lkg",
        quarantine_dir: str | Path = "./state/quarantine",
        max_bytes: int = 1_048_576,
        policy_validator=None,
    ) -> None:
        if not keyring:
            raise ValueError("Keyring must contain at least one key.")
        if active_key_id not in keyring:
            raise ValueError(f"active_key_id '{active_key_id}' not found in keyring.")

        for kid, secret in keyring.items():
            if len(secret) < 32:
                raise ValueError(
                    f"Secret key for '{kid}' must be at least 32 bytes (256 bits)."
                )

        self._keyring = dict(keyring)
        self._active_key_id = active_key_id
        self._lkg_dir = Path(lkg_state_dir).resolve()
        self._quarantine_dir = Path(quarantine_dir).resolve()
        self._max_bytes = max_bytes
        self._policy_validator = policy_validator or GoverningPolicy.model_validate

        # In-memory state: {resolved_policy_path: (verified_sha256, issued_at_epoch, policy)}
        self._memory_cache: dict[Path, tuple[str, int, GoverningPolicy]] = {}
        self._consumed_tokens: set[str] | None = None

    def _compute_hmac(self, key_id: str, canonical_payload: str) -> str:
        secret = self._keyring.get(key_id)
        if secret is None:
            raise PolicySecurityError(f"Unknown or retired key_id: '{key_id}'.")
        return hmac.new(
            secret,
            canonical_payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _atomic_write_json(self, target_path: Path, json_text: str) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=target_path.parent, prefix=".tmp_state_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(json_text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, target_path)
        except BaseException:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise

    def load(
        self,
        policy_path: str | Path,
        manifest_path: str | Path | None = None,
        override_token_path: str | Path | None = None,
        allow_fallback: bool = True,
    ) -> GoverningPolicy:
        """Loads, verifies, and returns the active GoverningPolicy or LKG fallback."""
        p_path = Path(policy_path).resolve()
        m_path = (
            Path(manifest_path).resolve()
            if manifest_path
            else p_path.with_suffix(f"{p_path.suffix}.manifest.json")
        )
        o_path = Path(override_token_path).resolve() if override_token_path else None

        with state_transaction(self._lkg_dir):
            # Hydrate persisted LKG watermark on cold boot before inspecting active files
            self._load_persisted_lkg(p_path)
            self._consumed_tokens = None

            try:
                return self._verify_and_load(p_path, m_path, o_path)
            except (PolicySecurityError, PolicyPayloadError, OSError) as exc:
                logger.critical("Active policy load failed for %s: %s", p_path, exc)
                self._quarantine_artifacts(p_path, m_path, o_path, reason=str(exc))

                if allow_fallback and p_path in self._memory_cache:
                    lkg_sha, lkg_epoch, lkg_policy = self._memory_cache[p_path]
                    logger.warning(
                        "Falling back to LKG policy (version=%s, epoch=%d, sha256=%s...)",
                        lkg_policy.version,
                        lkg_epoch,
                        lkg_sha[:12],
                    )
                    return lkg_policy

                raise PolicySecurityError(
                    f"Fail-closed: no permitted fallback for {p_path}."
                ) from exc

    def _verify_and_load(
        self, p_path: Path, m_path: Path, o_path: Path | None
    ) -> GoverningPolicy:
        if not p_path.is_file() or not m_path.is_file():
            raise FileNotFoundError(
                f"Missing policy ({p_path}) or manifest ({m_path})."
            )

        # 1. Single-read ingestion (prevents TOCTOU swaps)
        manifest_bytes = m_path.read_bytes()
        with p_path.open("rb") as stream:
            policy_bytes = stream.read(self._max_bytes + 1)
        if len(policy_bytes) > self._max_bytes:
            raise PolicyPayloadError("Policy size limit exceeded")

        # 2. Parse & verify HMAC-SHA256 manifest using its declared key_id
        manifest = self._verify_manifest(manifest_bytes, expected_filename=p_path.name)

        # 3. Verify policy SHA-256 against authenticated manifest digest
        actual_sha256 = hashlib.sha256(policy_bytes).hexdigest()
        expected_sha256 = manifest.sha256.lower()

        if not hmac.compare_digest(actual_sha256, expected_sha256):
            raise PolicySecurityError(
                f"SHA-256 mismatch: manifest expects {expected_sha256}, "
                f"actual is {actual_sha256}"
            )

        # Parse and validate the signed TOML before using the cached object.
        cached = self._memory_cache.get(p_path)
        policy = cached[2] if cached and cached[0] == actual_sha256 else self._parse_and_validate_policy(policy_bytes)

        # Ensure manifest's signed version matches the inner TOML policy version
        if policy.version != manifest.policy_version:
            raise PolicySecurityError(
                f"Version binding mismatch: manifest declares "
                f"{manifest.policy_version}, TOML payload declares {policy.version}."
            )

        # Anti-rollback check (or verified break-glass override)
        self._enforce_anti_rollback(
            p_path=p_path,
            manifest=manifest,
            actual_sha256=actual_sha256,
            override_path=o_path,
        )

        if cached and cached[:2] == (actual_sha256, manifest.issued_at_epoch):
            return cached[2]
        self._persist_lkg(p_path, actual_sha256, manifest.issued_at_epoch, policy_bytes, policy)
        self._memory_cache[p_path] = (actual_sha256, manifest.issued_at_epoch, policy)
        return policy

    def _enforce_anti_rollback(
        self,
        p_path: Path,
        manifest: PolicyManifest,
        actual_sha256: str,
        override_path: Path | None,
    ) -> bool:
        """Enforces monotonic watermark progression unless authorized by override token.

        Returns True if a break-glass override was consumed.
        """
        if p_path not in self._memory_cache:
            return False

        lkg_sha, lkg_epoch, lkg_policy = self._memory_cache[p_path]

        # Idempotent reload of the active policy
        if hmac.compare_digest(lkg_sha, actual_sha256):
            if manifest.issued_at_epoch < lkg_epoch:
                raise PolicySecurityError(
                    f"Rollback detected: manifest epoch {manifest.issued_at_epoch} "
                    f"< LKG {lkg_epoch}."
                )
            return False

        candidate_ver = _parse_semver(manifest.policy_version)
        lkg_ver = _parse_semver(lkg_policy.version)
        is_downgrade = (
            candidate_ver < lkg_ver
            or manifest.issued_at_epoch < lkg_epoch
            or (
                candidate_ver == lkg_ver
                and manifest.issued_at_epoch == lkg_epoch
            )
        )

        if not is_downgrade:
            return False

        # Downgrade detected: require valid break-glass override token
        if override_path is None or not override_path.is_file():
            raise PolicySecurityError(
                f"Rollback blocked "
                f"(candidate={manifest.policy_version}@{manifest.issued_at_epoch}, "
                f"LKG={lkg_policy.version}@{lkg_epoch}) and no override token provided."
            )

        token = self._verify_and_consume_override_token(
            override_path=override_path,
            expected_file=p_path.name,
            expected_version=manifest.policy_version,
            expected_sha256=actual_sha256,
        )

        logger.warning(
            "BREAK-GLASS OVERRIDE ACCEPTED: Downgrading %s from %s to %s "
            "(token_id=%s, operator=%s, reason=%r)",
            p_path.name,
            lkg_policy.version,
            manifest.policy_version,
            token.token_id,
            token.operator_id,
            token.reason,
        )

        return True

    def _verify_and_consume_override_token(
        self,
        override_path: Path,
        expected_file: str,
        expected_version: str,
        expected_sha256: str,
    ) -> RollbackOverrideToken:
        try:
            token = RollbackOverrideToken.model_validate_json(
                override_path.read_bytes()
            )
        except ValueError as exc:
            raise PolicySecurityError(
                f"Malformed break-glass override token: {exc}"
            ) from exc

        # 1. Verify HMAC signature using token's key_id
        canonical = (
            f"override:v1:{token.key_id}:"
            f"{token.token_id}:{token.operator_id}:"
            f"{token.target_file}:"
            f"{token.approved_version}:"
            f"{token.approved_sha256.lower()}:"
            f"{token.expires_at_epoch}:"
            f"{token.reason}"
        )
        expected_hmac = self._compute_hmac(token.key_id, canonical)

        if not hmac.compare_digest(expected_hmac, token.hmac_sha256.lower()):
            raise PolicySecurityError(
                "Break-glass override token HMAC verification failed."
            )

        # 2. Check expiration window
        now_epoch = int(time.time())
        if now_epoch > token.expires_at_epoch:
            raise PolicySecurityError(
                f"Break-glass override token '{token.token_id}' expired at "
                f"{token.expires_at_epoch}."
            )

        # 3. Verify strict binding to target file, version, and exact SHA-256
        if token.target_file != expected_file:
            raise PolicySecurityError(
                f"Override token target_file mismatch: "
                f"'{token.target_file}' != '{expected_file}'."
            )

        if token.approved_version != expected_version:
            raise PolicySecurityError(
                f"Override token version mismatch: "
                f"'{token.approved_version}' != '{expected_version}'."
            )

        if not hmac.compare_digest(
            token.approved_sha256.lower(), expected_sha256.lower()
        ):
            raise PolicySecurityError(
                "Override token approved_sha256 does not match candidate policy."
            )

        # 4. Enforce single-use replay protection
        consumed = self._get_consumed_tokens()
        if token.token_id in consumed:
            raise PolicySecurityError(
                f"Break-glass override token '{token.token_id}' has already been consumed."
            )

        consumed.add(token.token_id)
        self._persist_consumed_tokens(consumed)

        # Remove the used token file so it isn't accidentally re-submitted
        try:
            override_path.unlink(missing_ok=True)
        except OSError as exc:
            logger.warning(
                "Could not delete consumed override token file %s: %s",
                override_path,
                exc,
            )

        return token

    def _get_consumed_tokens(self) -> set[str]:
        if self._consumed_tokens is not None:
            return self._consumed_tokens

        ledger_path = self._lkg_dir / "consumed_override_tokens.json"

        if not ledger_path.is_file():
            self._consumed_tokens = set()
            return self._consumed_tokens

        try:
            ledger = ConsumedTokensLedger.model_validate_json(
                ledger_path.read_bytes()
            )
            canonical = (
                f"ledger:v1:{ledger.key_id}:"
                f"{','.join(sorted(ledger.consumed_token_ids))}"
            )
            expected_hmac = self._compute_hmac(ledger.key_id, canonical)
            if not hmac.compare_digest(
                expected_hmac, ledger.ledger_hmac_sha256.lower()
            ):
                raise PolicySecurityError(
                    "Consumed override token ledger HMAC verification failed."
                )
            self._consumed_tokens = set(ledger.consumed_token_ids)
            return self._consumed_tokens
        except Exception as exc:
            raise PolicySecurityError(
                f"Fail-closed: Cannot verify consumed override token ledger: {exc}"
            ) from exc

    def _persist_consumed_tokens(self, token_ids: set[str]) -> None:
        sorted_ids = tuple(sorted(token_ids))
        canonical = f"ledger:v1:{self._active_key_id}:{','.join(sorted_ids)}"
        tag = self._compute_hmac(self._active_key_id, canonical)
        ledger = ConsumedTokensLedger(
            key_id=self._active_key_id,
            consumed_token_ids=sorted_ids,
            ledger_hmac_sha256=tag,
        )
        self._atomic_write_json(
            self._lkg_dir / "consumed_override_tokens.json",
            ledger.model_dump_json(indent=2),
        )

    def _verify_manifest(
        self, manifest_bytes: bytes, expected_filename: str
    ) -> PolicyManifest:
        try:
            manifest = PolicyManifest.model_validate_json(manifest_bytes)
        except ValueError as exc:
            raise PolicySecurityError(f"Malformed manifest JSON: {exc}") from exc

        if manifest.target_file != expected_filename:
            raise PolicySecurityError(
                f"Manifest target mismatch: expected '{expected_filename}', "
                f"got '{manifest.target_file}'."
            )

        canonical = (
            f"manifest:v3:{manifest.key_id}:{manifest.target_file}:"
            f"{manifest.policy_version}:{manifest.issued_at_epoch}:"
            f"{manifest.sha256.lower()}"
        )
        expected_hmac = self._compute_hmac(manifest.key_id, canonical)
        if not hmac.compare_digest(expected_hmac, manifest.hmac_sha256.lower()):
            raise PolicySecurityError("Manifest HMAC-SHA256 verification failed.")
        return manifest

    def _parse_and_validate_policy(self, raw_bytes: bytes) -> GoverningPolicy:
        if not raw_bytes:
            raise PolicyPayloadError("Policy payload is empty.")
        if len(raw_bytes) > self._max_bytes:
            raise PolicyPayloadError(
                f"Policy payload exceeds {self._max_bytes} bytes."
            )
        try:
            decoded = raw_bytes.decode("utf-8")
            parsed = tomllib.loads(decoded)
        except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise PolicyPayloadError(
                f"Invalid UTF-8 or TOML syntax: {exc}"
            ) from exc

        if not isinstance(parsed, dict) or not parsed:
            raise PolicyPayloadError("TOML root must be a non-empty table.")
        try:
            return self._policy_validator(parsed)
        except (ValueError, TypeError, KeyError, OverflowError) as exc:
            raise PolicyPayloadError(f"Schema validation error:\n{exc}") from exc

    def _lkg_file_path(self, p_path: Path) -> Path:
        path_id = hashlib.sha256(str(p_path).encode("utf-8")).hexdigest()[:16]
        return self._lkg_dir / f"lkg_{p_path.stem}_{path_id}.json"

    def _persist_lkg(
        self,
        p_path: Path,
        sha256_hex: str,
        issued_at_epoch: int,
        policy_bytes: bytes,
        policy,
    ) -> None:
        """Atomically writes an HMAC-sealed LKG envelope using the active_key_id."""
        try:
            policy_b64 = base64.b64encode(policy_bytes).decode("ascii")
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            canonical = (
                f"lkg:v3:{self._active_key_id}:{p_path}:{policy.version}:"
                f"{issued_at_epoch}:{sha256_hex}:{policy_b64}:{ts}"
            )
            envelope_hmac = self._compute_hmac(self._active_key_id, canonical)
            envelope = PersistedLKGEnvelope(
                key_id=self._active_key_id,
                target_path=str(p_path),
                policy_version=policy.version,
                issued_at_epoch=issued_at_epoch,
                sha256=sha256_hex,
                policy_b64=policy_b64,
                persisted_at_utc=ts,
                envelope_hmac_sha256=envelope_hmac,
            )
            self._atomic_write_json(
                self._lkg_file_path(p_path), envelope.model_dump_json(indent=2)
            )
        except OSError as exc:
            raise PolicySecurityError(f"Cannot persist admitted policy for {p_path}") from exc

    def _load_persisted_lkg(self, p_path: Path, *, reseal: bool = True) -> GoverningPolicy | None:
        """Hydrates persisted LKG on cold boot using its recorded key_id.

        If persisted under an older retired-but-valid key_id, automatically
        re-seals the LKG envelope under active_key_id upon verification.
        """
        lkg_file = self._lkg_file_path(p_path)
        if not lkg_file.is_file():
            return None
        try:
            envelope = PersistedLKGEnvelope.model_validate_json(
                lkg_file.read_bytes()
            )
            if envelope.target_path != str(p_path):
                raise PolicySecurityError("Persisted LKG target_path mismatch.")
            canonical = (
                f"lkg:v3:{envelope.key_id}:{envelope.target_path}:"
                f"{envelope.policy_version}:{envelope.issued_at_epoch}:"
                f"{envelope.sha256.lower()}:{envelope.policy_b64}:"
                f"{envelope.persisted_at_utc}"
            )
            expected_hmac = self._compute_hmac(envelope.key_id, canonical)
            if not hmac.compare_digest(
                expected_hmac, envelope.envelope_hmac_sha256.lower()
            ):
                raise PolicySecurityError(
                    "Persisted LKG envelope HMAC verification failed."
                )
            policy_bytes = base64.b64decode(envelope.policy_b64, validate=True)
            actual_sha256 = hashlib.sha256(policy_bytes).hexdigest()
            if not hmac.compare_digest(actual_sha256, envelope.sha256.lower()):
                raise PolicySecurityError(
                    "Persisted LKG inner payload SHA-256 mismatch."
                )
            cached = self._memory_cache.get(p_path)
            policy = cached[2] if cached and cached[0] == actual_sha256 else self._parse_and_validate_policy(policy_bytes)
            if policy.version != envelope.policy_version:
                raise PolicySecurityError(
                    "Persisted LKG inner/outer version mismatch."
                )
            self._memory_cache[p_path] = (
                actual_sha256,
                envelope.issued_at_epoch,
                policy,
            )

            # Seamless key rotation: re-seal LKG envelope under active_key_id
            if reseal and envelope.key_id != self._active_key_id:
                logger.info(
                    "Rotating LKG envelope seal from key_id='%s' to active_key_id='%s'",
                    envelope.key_id,
                    self._active_key_id,
                )
                self._persist_lkg(
                    p_path, actual_sha256, envelope.issued_at_epoch, policy_bytes, policy
                )
            return policy
        except Exception as exc:
            logger.critical(
                "Persisted LKG envelope at %s is corrupt or tampered: %s",
                lkg_file,
                exc,
            )
            raise PolicySecurityError("Persisted admission state could not be verified") from exc

    def inspect_active(self, path: Path):
        """Read the signed active bytes only when they match the durable admission."""
        path = path.resolve()
        manifest_path = path.with_suffix(".toml.manifest.json")
        if not any(p.exists() for p in (path, manifest_path, self._lkg_file_path(path))):
            return None
        manifest = self._verify_manifest(manifest_path.read_bytes(), path.name)
        with path.open("rb") as stream:
            raw = stream.read(self._max_bytes + 1)
        digest = hashlib.sha256(raw).hexdigest()
        if len(raw) > self._max_bytes or digest != manifest.sha256.lower():
            raise PolicySecurityError("Active bytes differ from signed policy")
        policy = self._load_persisted_lkg(path, reseal=False)
        if (policy is None or policy.version != manifest.policy_version
                or self._memory_cache[path][:2] != (digest, manifest.issued_at_epoch)):
            raise PolicySecurityError("Active policy differs from durable admission")
        return raw, manifest

    def _quarantine_artifacts(
        self, p_path: Path, m_path: Path, o_path: Path | None, reason: str
    ) -> None:
        try:
            if not any(p and p.exists() for p in (p_path, m_path, o_path)):
                return
            self._quarantine_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            incident_dir = Path(tempfile.mkdtemp(dir=self._quarantine_dir, prefix=f"{ts}_{p_path.stem}_"))
            artifacts = [p_path, m_path] + ([o_path] if o_path else [])
            for artifact in artifacts:
                if artifact and artifact.exists():
                    shutil.move(str(artifact), str(incident_dir / artifact.name))
            (incident_dir / "incident.json").write_text(
                json.dumps(
                    {
                        "timestamp_utc": ts,
                        "policy_path": str(p_path),
                        "manifest_path": str(m_path),
                        "override_token_path": str(o_path) if o_path else None,
                        "reason": reason,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            logger.warning(
                "Quarantined suspect policy artifacts to %s", incident_dir
            )
        except OSError as q_err:
            logger.error("Failed to quarantine suspect artifacts: %s", q_err)
