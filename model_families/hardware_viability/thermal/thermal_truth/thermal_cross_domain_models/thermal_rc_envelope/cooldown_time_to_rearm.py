"""THERM-RC-003 — Cooldown time to rearm."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/cooldown_time_to_rearm')


import math
from fractions import Fraction
from math import inf
from sys import float_info


def symbolic_expression() -> str:
    return '-tau * math.log((Trearm - Teq) / (Tstart - Teq))'


def _crossing(start, target, equilibrium, tau):
    if start < target < equilibrium or start > target > equilibrium:
        step = abs(target - start)
        gap = abs(equilibrium - target)
        ratio = step / gap
        if float_info.min <= ratio < inf and math.isfinite(gap):
            return tau * math.log1p(ratio)
        # Retain scale if a finite input difference or ratio overflows or underflows.
        exact = abs((Fraction(target) - Fraction(start)) / (Fraction(equilibrium) - Fraction(target)))
        if exact < float_info.min:
            return float(Fraction(tau) * exact)
        if exact <= float_info.max:
            return tau * math.log1p(float(exact))
        total = 1 + exact
        return tau * (math.log(total.numerator) - math.log(total.denominator))
    return -tau * math.log((target - equilibrium) / (start - equilibrium))


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(Tstart, Trearm, Teq, tau):
        return _crossing(Tstart, Trearm, Teq, tau)

    return evaluate


def compute_cooldown_time_to_rearm(start_temp_c: float, rearm_temp_c: float, cool_equilibrium_temp_c: float, cooldown_time_constant_s: float) -> float:
    if cooldown_time_constant_s <= 0:
        raise ValueError("cooldown_time_constant_s must be > 0")
    if start_temp_c <= rearm_temp_c:
        return 0.0
    if cool_equilibrium_temp_c >= rearm_temp_c:
        return inf
    return _crossing(start_temp_c, rearm_temp_c, cool_equilibrium_temp_c, cooldown_time_constant_s)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_cooldown_time_to_rearm",
]

_policy.bind(globals())
