"""PLANT-ABORT-001 — waveoff_closure_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/plant_abortability/waveoff_closure_margin')


def compute_waveoff_closure_margin(
    t_available_for_waveoff_s: float,
    t_engine_start_s: float,
    t_attitude_settle_s: float,
    t_vertical_escape_s: float,
    t_lateral_clearance_s: float,
    t_guard_s: float = _policy.default,
) -> float:
    terms = [
        t_available_for_waveoff_s,
        t_engine_start_s,
        t_attitude_settle_s,
        t_vertical_escape_s,
        t_lateral_clearance_s,
        t_guard_s,
    ]
    if any(t < 0.0 for t in terms):
        raise ValueError("waveoff time terms must be non-negative")
    required = t_engine_start_s + t_attitude_settle_s + t_vertical_escape_s + t_lateral_clearance_s + t_guard_s
    return float(t_available_for_waveoff_s - required)


waveoff_closure_margin = compute_waveoff_closure_margin

__all__ = ['compute_waveoff_closure_margin', 'waveoff_closure_margin']

_policy.bind(globals())
