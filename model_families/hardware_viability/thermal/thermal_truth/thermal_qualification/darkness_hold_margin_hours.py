"""THERM-QUAL-001 — darkness_hold_margin_hours"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_qualification/darkness_hold_margin_hours')


def compute_darkness_hold_margin_hours(t_policy_h: float, t_dark_h: float) -> float:
    return float(t_policy_h - t_dark_h)


darkness_hold_margin_hours = compute_darkness_hold_margin_hours

__all__ = ['compute_darkness_hold_margin_hours', 'darkness_hold_margin_hours']

_policy.bind(globals())
