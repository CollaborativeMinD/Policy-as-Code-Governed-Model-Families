"""THERM-PWR-002 — Duty-cycle temperature margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/duty_cycle_temperature_margin')


def symbolic_expression() -> str:
    return 'Twarn - (Tamb + Peff * Rth)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Twarn, Tamb, Peff, Rth):
        return Twarn - (Tamb + Peff * Rth)

    return evaluate


def compute_duty_cycle_temperature_margin(warning_temp_c: float, ambient_temp_c: float, effective_power_w: float, thermal_resistance_c_per_w: float) -> float:
    if thermal_resistance_c_per_w <= 0:
        raise ValueError("thermal_resistance_c_per_w must be > 0")
    return float(warning_temp_c - (ambient_temp_c + effective_power_w * thermal_resistance_c_per_w))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_duty_cycle_temperature_margin",
]

_policy.bind(globals())
