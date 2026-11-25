"""C6.1 — Line-of-sight / terrain-mask closure law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/c6_1_los_terrain_mask_closure')


def compute_los_terrain_mask_margin(
    ray_elevation_angle: float,
    horizon_mask_angle: float,
    buffer_angle: float = _policy.default,
) -> float:
    return float(ray_elevation_angle - horizon_mask_angle - buffer_angle)

__all__ = ['compute_los_terrain_mask_margin']

_policy.bind(globals())
