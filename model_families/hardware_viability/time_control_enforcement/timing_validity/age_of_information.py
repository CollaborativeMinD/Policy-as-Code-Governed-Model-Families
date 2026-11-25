"""T1.1 — Age-of-information at use law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/timing_validity/age_of_information')


def compute_age_of_information_margin(
    time_generated: float,
    time_used: float,
    freshness_limit: float,
) -> float:
    aoi_use = time_used - time_generated
    return float(freshness_limit - aoi_use)

__all__ = ['compute_age_of_information_margin']

_policy.bind(globals())
