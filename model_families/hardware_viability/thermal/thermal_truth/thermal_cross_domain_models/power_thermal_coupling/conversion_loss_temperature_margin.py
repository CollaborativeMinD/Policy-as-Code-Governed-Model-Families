"""THERM-PWR-003 — Conversion loss temperature margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/conversion_loss_temperature_margin')


def symbolic_expression() -> str:
    return 'Twarn - (Tamb + Rth * Pout * (1 / eta - 1))'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Twarn, Tamb, Pout, eta, Rth):
        return Twarn - (Tamb + Rth * Pout * (1 / eta - 1))

    return evaluate


def compute_conversion_loss_temperature_margin(warning_temp_c: float, ambient_temp_c: float, output_power_w: float, efficiency: float, thermal_resistance_c_per_w: float) -> float:
    if not 0.0 < efficiency <= 1.0:
        raise ValueError("efficiency must be in (0, 1]")
    if thermal_resistance_c_per_w <= 0:
        raise ValueError("thermal_resistance_c_per_w must be > 0")
    conversion_loss_w = output_power_w * (1.0 / efficiency - 1.0)
    return float(warning_temp_c - (ambient_temp_c + thermal_resistance_c_per_w * conversion_loss_w))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_conversion_loss_temperature_margin",
]

_policy.bind(globals())
