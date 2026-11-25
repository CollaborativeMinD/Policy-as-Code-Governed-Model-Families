"""THERM-RC-001 — Equilibrium temperature under load."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/equilibrium_temperature_under_load')


def symbolic_expression() -> str:
    return 'Tamb + Peff * Rth'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Tamb, Peff, Rth):
        return Tamb + Peff * Rth

    return evaluate


def compute_equilibrium_temperature_under_load(ambient_temp_c: float, effective_power_w: float, thermal_resistance_c_per_w: float) -> float:
    if thermal_resistance_c_per_w <= 0:
        raise ValueError("thermal_resistance_c_per_w must be > 0")
    return float(ambient_temp_c + effective_power_w * thermal_resistance_c_per_w)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_equilibrium_temperature_under_load",
]

_policy.bind(globals())
