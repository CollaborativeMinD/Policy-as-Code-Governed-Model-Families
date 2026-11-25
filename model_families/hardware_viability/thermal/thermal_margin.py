"""HW-THERM-001 — thermal margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_margin')


def compute_thermal_margin(current_temp_c: float, t_crit_c: float) -> float:
    return float(t_crit_c) - float(current_temp_c)


__all__ = ['compute_thermal_margin']

_policy.bind(globals())
