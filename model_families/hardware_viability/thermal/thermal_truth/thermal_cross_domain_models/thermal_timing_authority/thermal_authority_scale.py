"""THERM-AUTH-001 — Thermal authority scale."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/thermal_authority_scale')


def symbolic_expression_min_unclipped() -> str:
    return 'min((Tc - T) / (Tc - Tw), m / tau)'


def _clip(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def compute_thermal_authority_scale(temp_c: float, warning_temp_c: float, critical_temp_c: float, deadline_margin_ms: float, deadline_budget_ms: float, authority_floor: float) -> float:
    if critical_temp_c <= warning_temp_c:
        raise ValueError("critical_temp_c must exceed warning_temp_c")
    if deadline_budget_ms <= 0:
        raise ValueError("deadline_budget_ms must be > 0")
    if not 0.0 <= authority_floor <= 1.0:
        raise ValueError("authority_floor must be in [0, 1]")
    thermal_fraction = _clip((critical_temp_c - temp_c) / (critical_temp_c - warning_temp_c), 0.0, 1.0)
    timing_fraction = _clip(deadline_margin_ms / deadline_budget_ms, 0.0, 1.0)
    return float(_clip(min(thermal_fraction, timing_fraction), authority_floor, 1.0))


__all__ = ['symbolic_expression_min_unclipped', 'compute_thermal_authority_scale']

_policy.bind(globals())
