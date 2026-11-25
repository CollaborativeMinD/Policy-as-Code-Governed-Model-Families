"""HORIZON-GEO-003 — horizon_sampling_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/horizon_geometry/horizon_sampling_margin')


import math


def compute_horizon_sampling_margin(alpha_tol_deg: float, terrain_resolution_m: float, observer_height_m: float) -> float:
    if terrain_resolution_m <= 0 or observer_height_m <= 0:
        raise ValueError('terrain_resolution_m and observer_height_m must be positive')
    return float(alpha_tol_deg - math.degrees(math.atan(terrain_resolution_m / observer_height_m)))


horizon_sampling_margin = compute_horizon_sampling_margin

__all__ = ['compute_horizon_sampling_margin', 'horizon_sampling_margin']

_policy.bind(globals())
