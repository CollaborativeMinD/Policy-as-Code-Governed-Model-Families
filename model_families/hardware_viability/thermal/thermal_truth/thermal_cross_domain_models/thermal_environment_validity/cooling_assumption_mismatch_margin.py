"""THERM-ENV-001 — Cooling assumption mismatch margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_environment_validity/cooling_assumption_mismatch_margin')


def symbolic_expression() -> str:
    return 'allow - abs(measured - claimed)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(allow, measured, claimed):
        return allow - abs(measured - claimed)

    return evaluate


def compute_cooling_assumption_mismatch_margin(measured_steady_temp_c: float, measured_ambient_c: float, measured_power_w: float, claimed_thermal_resistance_c_per_w: float, allowed_resistance_error_c_per_w: float) -> float:
    if measured_power_w <= 0:
        raise ValueError("measured_power_w must be > 0")
    if claimed_thermal_resistance_c_per_w <= 0:
        raise ValueError("claimed_thermal_resistance_c_per_w must be > 0")
    if allowed_resistance_error_c_per_w <= 0:
        raise ValueError("allowed_resistance_error_c_per_w must be > 0")
    measured_r_th = (measured_steady_temp_c - measured_ambient_c) / measured_power_w
    return float(allowed_resistance_error_c_per_w - abs(measured_r_th - claimed_thermal_resistance_c_per_w))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_cooling_assumption_mismatch_margin",
]

_policy.bind(globals())
