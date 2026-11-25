"""P1.1 — Duty-cycle energy reserve margin law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/cycle_energy_reserve_margin')


from typing import Sequence


def compute_duty_cycle_energy_reserve_margin(
    energy_stored: float,
    power_segments: Sequence[float],
    duration_segments: Sequence[float],
    thermal_hold_energy: float = _policy.default,
    contingency_energy: float = _policy.default,
) -> float:
    if len(power_segments) != len(duration_segments):
        raise ValueError("power_segments and duration_segments must have equal length")
    mission_energy = sum(float(p) * float(dt) for p, dt in zip(power_segments, duration_segments))
    return float(energy_stored - mission_energy - thermal_hold_energy - contingency_energy)

__all__ = ['compute_duty_cycle_energy_reserve_margin']

_policy.bind(globals())
