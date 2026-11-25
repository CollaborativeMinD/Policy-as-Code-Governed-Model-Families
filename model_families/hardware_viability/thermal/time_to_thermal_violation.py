"""HW-THERM-002 — time to thermal violation."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/time_to_thermal_violation')

import math

def compute_time_to_thermal_violation(current_temp_c: float, t_crit_c: float, dT_dt_c_per_s: float) -> float:
    dT_dt = float(dT_dt_c_per_s)
    if dT_dt <= 0.0:
        return math.inf
    return (float(t_crit_c) - float(current_temp_c)) / dT_dt


__all__ = ['compute_time_to_thermal_violation']

_policy.bind(globals())
