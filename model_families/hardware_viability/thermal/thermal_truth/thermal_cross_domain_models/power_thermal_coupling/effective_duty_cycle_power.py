"""THERM-PWR-001 — Effective duty-cycle power."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/effective_duty_cycle_power')

from collections.abc import Sequence


def symbolic_expression_2term() -> str:
    return 'Pbase + D1 * DP1 + D2 * DP2'


def lambdified_2term():
    @_policy.evaluator("lambdified_2term.evaluate")
    def evaluate(Pbase, D1, DP1, D2, DP2):
        return Pbase + D1 * DP1 + D2 * DP2

    return evaluate


def compute_effective_duty_cycle_power(base_power_w: float, duty_cycles: Sequence[float], incremental_powers_w: Sequence[float]) -> float:
    if len(duty_cycles) != len(incremental_powers_w):
        raise ValueError("duty_cycles and incremental_powers_w must have equal length")
    p_eff = float(base_power_w)
    for d_i, dp_i in zip(duty_cycles, incremental_powers_w):
        if not 0.0 <= float(d_i) <= 1.0:
            raise ValueError("each duty cycle must be in [0, 1]")
        p_eff += float(d_i) * float(dp_i)
    return float(p_eff)


__all__ = [
    "symbolic_expression_2term",
    "lambdified_2term",
    "compute_effective_duty_cycle_power",
]

_policy.bind(globals())
