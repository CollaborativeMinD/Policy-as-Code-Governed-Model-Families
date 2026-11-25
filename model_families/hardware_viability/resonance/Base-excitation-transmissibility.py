"""M4.1b — Base-excitation transmissibility"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/resonance/Base-excitation-transmissibility')


from typing import Dict, Any
import math


def compute_base_excitation_transmissibility(
    forcing_frequency_hz: float,
    natural_frequency_hz: float,
    damping_ratio: float,
    base_acceleration: float,
) -> Dict[str, Any]:
    if forcing_frequency_hz <= 0.0 or natural_frequency_hz <= 0.0:
        raise ValueError("frequencies must be positive")
    if damping_ratio < 0.0:
        raise ValueError("damping_ratio must be non-negative")

    r = forcing_frequency_hz / natural_frequency_hz
    num = 1.0 + (2.0 * damping_ratio * r) ** 2
    den = (1.0 - r ** 2) ** 2 + (2.0 * damping_ratio * r) ** 2
    transmissibility = math.sqrt(num / den)
    transmitted_acceleration = transmissibility * base_acceleration

    return {
        "frequency_ratio": r,
        "transmissibility": transmissibility,
        "transmitted_acceleration": transmitted_acceleration,
    }


__all__ = ['compute_base_excitation_transmissibility']

_policy.bind(globals())
