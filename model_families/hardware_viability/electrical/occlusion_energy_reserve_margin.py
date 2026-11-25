"""POWER-SURV-004 — occlusion_energy_reserve_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/electrical/occlusion_energy_reserve_margin')


def compute_occlusion_energy_reserve_margin(
    E_available_wh: float,
    P_dark_whph: float,
    t_occ_h: float,
    E_waveoff_wh: float,
    E_keepalive_wh: float,
) -> float:
    if min(E_available_wh, P_dark_whph, t_occ_h, E_waveoff_wh, E_keepalive_wh) < 0:
        raise ValueError("energy and duration terms must be non-negative")
    return float(E_available_wh - P_dark_whph * t_occ_h - E_waveoff_wh - E_keepalive_wh)


occlusion_energy_reserve_margin = compute_occlusion_energy_reserve_margin

__all__ = ['compute_occlusion_energy_reserve_margin', 'occlusion_energy_reserve_margin']

_policy.bind(globals())
