"""TERRAIN-TRUTH-012 — roughness_alias_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/roughness_alias_margin')


def compute_roughness_alias_margin(relief_local_p95: float, relief_regional_p95: float, r_alias_limit: float = _policy.default) -> float:
    return float(r_alias_limit - abs(relief_local_p95 - relief_regional_p95))


roughness_alias_margin = compute_roughness_alias_margin

__all__ = ['compute_roughness_alias_margin', 'roughness_alias_margin']

_policy.bind(globals())
