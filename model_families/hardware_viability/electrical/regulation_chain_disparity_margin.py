"""POWER-SURV-005 — regulation_chain_disparity_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/electrical/regulation_chain_disparity_margin')


def compute_regulation_chain_disparity_margin(v_upstream_pu: float, v_downstream_pu: float, delta_limit_pu: float) -> float:
    return float(delta_limit_pu - abs(v_upstream_pu - v_downstream_pu))


regulation_chain_disparity_margin = compute_regulation_chain_disparity_margin

__all__ = ['compute_regulation_chain_disparity_margin', 'regulation_chain_disparity_margin']

_policy.bind(globals())
