"""M3.2c — Abort closure margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/abort_closure_margin')


def compute_abort_closure_margin(
    corridor_distance: float,
    current_speed: float,
    effective_deceleration: float,
    decision_latency: float,
    reserve_distance: float,
) -> float:
    """Compute remaining abort corridor margin."""
    if corridor_distance < 0.0:
        raise ValueError("corridor_distance must be non-negative")
    if current_speed < 0.0:
        raise ValueError("current_speed must be non-negative")
    if effective_deceleration <= 0.0:
        raise ValueError("effective_deceleration must be positive")
    if decision_latency < 0.0 or reserve_distance < 0.0:
        raise ValueError("decision_latency and reserve_distance must be non-negative")

    required_distance = current_speed * decision_latency + (current_speed ** 2) / (2.0 * effective_deceleration) + reserve_distance
    return float(corridor_distance - required_distance)


__all__ = ['compute_abort_closure_margin']

_policy.bind(globals())
