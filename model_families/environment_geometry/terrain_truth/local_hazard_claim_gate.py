"""TERRAIN-TRUTH-011 — local_hazard_claim_gate"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/local_hazard_claim_gate')


def compute_local_hazard_claim_gate(lane: str, provenance_complete: bool, status: str, c_lane: float, tau_claim: float = _policy.default) -> bool:
    return bool(lane == _policy.value("local_lane") and provenance_complete and status == _policy.value("required_status") and c_lane >= tau_claim)


local_hazard_claim_gate = compute_local_hazard_claim_gate

__all__ = ['compute_local_hazard_claim_gate', 'local_hazard_claim_gate']

_policy.bind(globals())
