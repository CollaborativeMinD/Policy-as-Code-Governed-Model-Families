"""THERM-AUTH-002 — Recovery hysteresis margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/recovery_hysteresis_margin')


def symbolic_expression() -> str:
    return 'Trearm - Tcurrent'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Tcurrent, Trearm):
        return Trearm - Tcurrent

    return evaluate


def compute_recovery_hysteresis_margin(current_temp_c: float, rearm_temp_c: float) -> float:
    return float(rearm_temp_c - current_temp_c)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_recovery_hysteresis_margin",
]

_policy.bind(globals())
