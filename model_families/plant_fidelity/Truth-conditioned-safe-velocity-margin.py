"""M3.2d — Truth-conditioned safe velocity margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/Truth-conditioned-safe-velocity-margin')


import math


def compute_truth_conditioned_safe_velocity_margin(
    distance_to_hazard: float,
    current_speed: float,
    effective_deceleration: float,
    actuation_latency: float,
    terrain_truth_sigma: float,
    map_resolution: float,
    localization_sigma: float,
) -> float:
    """Compute the speed margin after discounting uncertain usable distance."""
    values = [
        distance_to_hazard,
        current_speed,
        actuation_latency,
        terrain_truth_sigma,
        map_resolution,
        localization_sigma,
    ]
    if any(v < 0.0 for v in values):
        raise ValueError("distance, speed, latency, and uncertainty terms must be non-negative")
    if effective_deceleration <= 0.0:
        raise ValueError("effective_deceleration must be positive")

    effective_distance = (
        distance_to_hazard
        - current_speed * actuation_latency
        - terrain_truth_sigma
        - 0.5 * map_resolution
        - localization_sigma
    )
    safe_speed = math.sqrt(max(2.0 * effective_deceleration * effective_distance, 0.0))
    return float(safe_speed - current_speed)


__all__ = ['compute_truth_conditioned_safe_velocity_margin']

_policy.bind(globals())
