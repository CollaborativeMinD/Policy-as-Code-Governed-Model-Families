"""TERRAIN-GOV-005 — terrain_commit_closure_gate"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/terrain_commit_closure')


def geospatial_status_ceiling_gate(claimed_status: str, status_ceiling: str) -> bool:
    if claimed_status not in _policy.value("status_order") or status_ceiling not in _policy.value("status_order"):
        raise ValueError("claimed_status and status_ceiling must be canonical values")
    return bool(_policy.value("status_order")[claimed_status] <= _policy.value("status_order")[status_ceiling])


def compute_terrain_commit_closure_gate(
    local_hazard_closed: bool,
    geospatial_status: str,
    provenance_complete: bool,
    region_proxy_alias_used: bool,
) -> bool:
    return bool(
        local_hazard_closed
        and geospatial_status_ceiling_gate(_policy.value("required_status"), geospatial_status)
        and provenance_complete
        and not region_proxy_alias_used
    )


terrain_commit_closure_gate = compute_terrain_commit_closure_gate

__all__ = ['compute_terrain_commit_closure_gate', 'terrain_commit_closure_gate']

_policy.bind(globals())
