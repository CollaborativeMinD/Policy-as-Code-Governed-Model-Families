"""ET-002 - dynamic_clearance_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/dynamic_clearance_margin')


from math import isfinite


def compute_dynamic_clearance_margin(
    measured_clearance_m: float,
    required_clearance_m: float,
    closure_speed_m_s: float,
    environment_age_s: float,
    environment_uncertainty_m: float,
) -> float:
    c_meas = float(measured_clearance_m)
    c_req = float(required_clearance_m)
    v = float(closure_speed_m_s)
    age = float(environment_age_s)
    sigma = float(environment_uncertainty_m)

    if not all(isfinite(x) for x in (c_meas, c_req, v, age, sigma)):
        raise ValueError("inputs must be finite")
    if min(c_meas, c_req, v, age, sigma) < 0:
        raise ValueError("all inputs must be non-negative")

    return c_meas - (c_req + v * age + sigma)


__all__ = ['compute_dynamic_clearance_margin']

_policy.bind(globals())
