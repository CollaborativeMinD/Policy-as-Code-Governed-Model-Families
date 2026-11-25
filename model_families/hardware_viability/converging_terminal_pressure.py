"""HW-GOV-002 — converging terminal pressure."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/converging_terminal_pressure')

from typing import Tuple

def compute_converging_terminal_pressure(thermal_pressure_ratio: float, memory_pressure_ratio: float, queue_pressure_ratio: float, horizon_pressure_ratio: float, weights: Tuple[float,float,float,float]=_policy.default) -> float:
    if len(weights) != 4:
        raise ValueError('weights must contain four values')
    if any(w < 0 for w in weights):
        raise ValueError('weights must be non-negative')
    vals=[float(thermal_pressure_ratio), float(memory_pressure_ratio), float(queue_pressure_ratio), float(horizon_pressure_ratio)]
    if any(v < 0 or v > 1 for v in vals):
        raise ValueError('all pressure ratios must be in [0,1]')
    score = sum(w*v for w,v in zip(weights, vals))
    return max(0.0, min(1.0, score))


__all__ = ['compute_converging_terminal_pressure']

_policy.bind(globals())
