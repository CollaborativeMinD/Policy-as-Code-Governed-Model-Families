"""POWER-SURV-003 — illumination_duty_cycle_energy_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/electrical/illumination_cycle_energy_margin')


def compute_illumination_duty_cycle_energy_margin(E_available_wh: float, gen_lit_wh_per_h: float, load_lit_wh_per_h: float, load_dark_wh_per_h: float, t_lit_h: float, t_dark_h: float) -> float:
    return float(E_available_wh + gen_lit_wh_per_h * t_lit_h - (load_lit_wh_per_h * t_lit_h + load_dark_wh_per_h * t_dark_h))


illumination_duty_cycle_energy_margin = compute_illumination_duty_cycle_energy_margin

__all__ = ['compute_illumination_duty_cycle_energy_margin', 'illumination_duty_cycle_energy_margin']

_policy.bind(globals())
