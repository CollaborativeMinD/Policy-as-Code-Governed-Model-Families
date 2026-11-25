"""THERM-RC-002 — Time to temperature threshold."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/time_to_temperature_threshold')


import math
from fractions import Fraction
from math import inf
from sys import float_info


def symbolic_expression() -> str:
    return '-tau * math.log((Tthr - Teq) / (T0 - Teq))'


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
    def evaluate(T0, Tthr, Teq, tau):
        return _crossing(T0, Tthr, Teq, tau)

    return evaluate


def compute_time_to_temperature_threshold(initial_temp_c: float, threshold_temp_c: float, equilibrium_temp_c: float, thermal_time_constant_s: float) -> float:
    if thermal_time_constant_s <= 0:
        raise ValueError("thermal_time_constant_s must be > 0")
    if initial_temp_c >= threshold_temp_c:
        return 0.0
    if equilibrium_temp_c <= threshold_temp_c:
        return inf
    return _crossing(initial_temp_c, threshold_temp_c, equilibrium_temp_c, thermal_time_constant_s)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_time_to_temperature_threshold",
]

_policy.bind(globals())
