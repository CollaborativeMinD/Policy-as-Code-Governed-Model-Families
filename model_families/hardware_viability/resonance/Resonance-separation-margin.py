"""M4.1a — Resonance separation margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/resonance/Resonance-separation-margin')


from typing import Sequence, Dict, Any


def _flatten(values):
    try:
        items = iter(values) if not isinstance(values, (bytes, str)) else None
    except TypeError:
        items = None
    if items is None:
        yield float(values)
    else:
        for item in items:
            yield from _flatten(item)


def compute_resonance_separation_margin(
    natural_frequencies_hz: Sequence[float],
    forcing_frequencies_hz: Sequence[float],
    exclusion_ratio: float = _policy.default,
) -> Dict[str, Any]:
    natural = list(_flatten(natural_frequencies_hz))
    forcing = list(_flatten(forcing_frequencies_hz))
    if not natural or not forcing or any(v <= 0 for v in natural + forcing):
        raise ValueError("frequency lists must be nonempty and positive")
    if exclusion_ratio < 0:
        raise ValueError("exclusion_ratio must be non-negative")
    pairs = ((abs(n-f)/f, n, f) for n in natural for f in forcing)
    separation, critical_natural, critical_forcing = min(pairs, key=lambda item: item[0])
    margin = separation - exclusion_ratio
    return {
        "minimum_separation_ratio": separation,
        "required_exclusion_ratio": exclusion_ratio,
        "signed_margin": margin,
        "critical_natural_frequency_hz": critical_natural,
        "critical_forcing_frequency_hz": critical_forcing,
        "resonance_clear": margin >= 0,
    }


__all__ = ['compute_resonance_separation_margin']

_policy.bind(globals())
