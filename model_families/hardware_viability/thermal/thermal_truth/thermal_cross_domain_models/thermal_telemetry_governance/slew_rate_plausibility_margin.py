"""THERM-TELEM-002 — Slew rate plausibility margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/slew_rate_plausibility_margin')


def symbolic_expression() -> str:
    return 'smax - abs(Tcurr - Tprev) / dt'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Tprev, Tcurr, dt, smax):
        return smax - abs(Tcurr - Tprev) / dt

    return evaluate


def compute_slew_rate_plausibility_margin(temp_prev_c: float, temp_curr_c: float, dt_s: float, max_allowed_slew_c_per_s: float) -> float:
    if dt_s <= 0 or max_allowed_slew_c_per_s <= 0:
        raise ValueError("dt_s and max_allowed_slew_c_per_s must be > 0")
    measured_slew = abs(temp_curr_c - temp_prev_c) / dt_s
    return float(max_allowed_slew_c_per_s - measured_slew)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_slew_rate_plausibility_margin",
]

_policy.bind(globals())
