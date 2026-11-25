"""TIME-COH-001 — ephemeris_horizon_coherence_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/timing_validity/ephemeris_horizon_coherence_margin')


def compute_ephemeris_horizon_coherence_margin(tau_align_s: float, t_ephem_s: float, t_horizon_s: float) -> float:
    return float(tau_align_s - abs(t_ephem_s - t_horizon_s))


ephemeris_horizon_coherence_margin = compute_ephemeris_horizon_coherence_margin

__all__ = ['compute_ephemeris_horizon_coherence_margin', 'ephemeris_horizon_coherence_margin']

_policy.bind(globals())
