"""PF-002 - curvature_feasibility_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/curvature_feasibility_margin')


from math import isfinite


def compute_curvature_feasibility_margin(
    speed_m_s: float,
    required_curvature_inv_m: float,
    available_lateral_accel_m_s2: float,
) -> float:
    speed = float(speed_m_s)
    kappa_req = float(required_curvature_inv_m)
    a_lat = float(available_lateral_accel_m_s2)

    if not all(isfinite(v) for v in (speed, kappa_req, a_lat)):
        raise ValueError("inputs must be finite")
    if speed <= 0:
        raise ValueError("speed_m_s must be positive")
    if a_lat <= 0:
        raise ValueError("available_lateral_accel_m_s2 must be positive")
    if kappa_req < 0:
        raise ValueError("required_curvature_inv_m must be non-negative")

    kappa_max = a_lat / (speed * speed)
    return kappa_max - kappa_req


__all__ = ['compute_curvature_feasibility_margin']

_policy.bind(globals())
