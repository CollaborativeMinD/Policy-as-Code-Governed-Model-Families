"""HW-MEM-001 — memory margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/memory/memory_margin')


def compute_memory_margin(current_mem_pct: float, mem_crit_pct: float) -> float:
    return float(mem_crit_pct) - float(current_mem_pct)


__all__ = ['compute_memory_margin']

_policy.bind(globals())
