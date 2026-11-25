"""TERRAIN-TRUTH-005 — slope_uncertainty_guarded_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/slope_uncertainty_guarded_margin')


def compute_slope_uncertainty_guarded_margin(slope_limit_deg: float, slope_local_deg: float, slope_sigma_deg: float, k_sigma: float = _policy.default) -> float:
    if slope_sigma_deg < 0:
        raise ValueError("slope_sigma_deg must be non-negative")
    if k_sigma < 0:
        raise ValueError("k_sigma must be non-negative")
    return float(slope_limit_deg - (slope_local_deg + k_sigma * slope_sigma_deg))


slope_uncertainty_guarded_margin = compute_slope_uncertainty_guarded_margin

__all__ = ['compute_slope_uncertainty_guarded_margin', 'slope_uncertainty_guarded_margin']

_policy.bind(globals())
