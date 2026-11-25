"""P1.3 — Thermal timing derate margin law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_timing_derate_margin')


def compute_thermal_timing_derate_margin(
    deadline: float,
    base_exec_time: float,
    core_temp: float,
    temp_threshold: float,
    derate_gain: float,
    io_jitter: float = _policy.default,
    guard_band: float = _policy.default,
) -> float:
    derate_factor = 1.0 + derate_gain * max(0.0, core_temp - temp_threshold)
    effective_exec = base_exec_time * derate_factor + io_jitter + guard_band
    return float(deadline - effective_exec)

__all__ = ['compute_thermal_timing_derate_margin']

_policy.bind(globals())
