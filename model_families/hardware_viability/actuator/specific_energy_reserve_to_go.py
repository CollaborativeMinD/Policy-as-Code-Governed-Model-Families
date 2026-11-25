"""M3.2d — Specific energy reserve-to-go law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/specific_energy_reserve_to_go')


def compute_specific_energy_reserve_margin(
    energy_available: float,
    energy_to_go: float,
    abort_reserve: float,
    uncertainty_buffer: float = _policy.default,
) -> float:
    return float(energy_available - (energy_to_go + abort_reserve + uncertainty_buffer))

__all__ = ['compute_specific_energy_reserve_margin']

_policy.bind(globals())
