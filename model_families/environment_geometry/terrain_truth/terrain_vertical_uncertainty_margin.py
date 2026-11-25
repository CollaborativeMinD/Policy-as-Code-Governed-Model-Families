"""TERRAIN-TRUTH-004 — terrain_vertical_uncertainty_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/terrain_vertical_uncertainty_margin')


def compute_terrain_vertical_uncertainty_margin(z_uncert_limit_m: float, terrain_vertical_uncertainty_m: float) -> float:
    return float(z_uncert_limit_m - terrain_vertical_uncertainty_m)


terrain_vertical_uncertainty_margin = compute_terrain_vertical_uncertainty_margin

__all__ = ['compute_terrain_vertical_uncertainty_margin', 'terrain_vertical_uncertainty_margin']

_policy.bind(globals())
