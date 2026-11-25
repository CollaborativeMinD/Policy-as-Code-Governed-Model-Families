"""HW-MEM-002 — time to memory violation."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/memory/time_to_memory_violation')

import math

def compute_time_to_memory_violation(current_mem_pct: float, mem_crit_pct: float, dM_dt_pct_per_s: float) -> float:
    dM_dt = float(dM_dt_pct_per_s)
    if dM_dt <= 0.0:
        return math.inf
    return (float(mem_crit_pct) - float(current_mem_pct)) / dM_dt


__all__ = ['compute_time_to_memory_violation']

_policy.bind(globals())
