"""THERM-TIME-001 — Clock derate fraction."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/clock_derate_fraction')


def symbolic_expression_unclipped() -> str:
    return '1 - k * ((T - Tw) / (Tc - Tw))'


def lambdified_unclipped():
    @_policy.evaluator("lambdified_unclipped.evaluate")
    def evaluate(T, Tw, Tc, k):
        return 1 - k * ((T - Tw) / (Tc - Tw))

    return evaluate


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def compute_clock_derate_fraction(temp_c: float, warning_temp_c: float, critical_temp_c: float, derate_gain: float, clock_floor_fraction: float) -> float:
    if critical_temp_c <= warning_temp_c:
        raise ValueError("critical_temp_c must exceed warning_temp_c")
    if not 0.0 < clock_floor_fraction <= 1.0:
        raise ValueError("clock_floor_fraction must be in (0, 1]")
    if derate_gain <= 0:
        raise ValueError("derate_gain must be > 0")
    thermal_utilization = _clip((temp_c - warning_temp_c) / (critical_temp_c - warning_temp_c), 0.0, 1.0)
    return float(_clip(1.0 - derate_gain * thermal_utilization, clock_floor_fraction, 1.0))


__all__ = [
    "symbolic_expression_unclipped",
    "lambdified_unclipped",
    "compute_clock_derate_fraction",
]

_policy.bind(globals())
