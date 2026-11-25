"""N1.1 — Delay-loss consensus stability"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('consensus_coordination/Delay-loss consensus stability')


import math


def compute_delay_loss_consensus_stability(
    algebraic_connectivity: float,
    network_delay_s: float,
    consensus_time_constant_s: float,
    loss_probability: float,
    network_jitter_s: float,
    jitter_budget_s: float,
) -> float:
    """Return degraded consensus stability score."""
    if consensus_time_constant_s <= 0.0 or jitter_budget_s <= 0.0:
        raise ValueError("consensus_time_constant_s and jitter_budget_s must be positive")
    lam2 = max(0.0, float(algebraic_connectivity))
    p_loss = max(0.0, min(1.0, float(loss_probability)))
    jitter_factor = 1.0 - min(max(float(network_jitter_s), 0.0) / float(jitter_budget_s), 1.0)
    return lam2 * math.exp(-max(float(network_delay_s), 0.0) / float(consensus_time_constant_s)) * (1.0 - p_loss) * jitter_factor


__all__ = ['compute_delay_loss_consensus_stability']

_policy.bind(globals())
