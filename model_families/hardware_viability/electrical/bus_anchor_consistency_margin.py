"""POWER-SURV-006 — bus_anchor_consistency_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/electrical/bus_anchor_consistency_margin')


def compute_bus_anchor_consistency_margin(m_bus: float, m_reg: float) -> float:
    return float(min(m_bus, m_reg))


bus_anchor_consistency_margin = compute_bus_anchor_consistency_margin

__all__ = ['compute_bus_anchor_consistency_margin', 'bus_anchor_consistency_margin']

_policy.bind(globals())
