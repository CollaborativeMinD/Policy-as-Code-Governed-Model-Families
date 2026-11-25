"""N1.3 — Byzantine trust-weighted agreement"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('consensus_coordination/Byzantine trust-weighted agreement')


from typing import Sequence, Tuple


def compute_byzantine_trust_weighted_agreement(
    values: Sequence[float],
    trust_weights: Sequence[float],
    tolerance: float,
    eps: float = _policy.default,
) -> Tuple[float, float]:
    """Return (agreement_score, fused_value)."""
    pairs = sorted(zip(map(float, values), map(float, trust_weights), strict=True))
    if not pairs or tolerance <= 0 or any(weight < 0 for _, weight in pairs):
        raise ValueError("expected observations, nonnegative weights and positive tolerance")
    total_weight = sum(weight for _, weight in pairs)
    if total_weight <= 0:
        raise ValueError("at least one trust weight must be positive")
    cumulative = 0.0
    for fused, weight in pairs:
        cumulative += weight
        if cumulative >= total_weight / 2:
            break
    deviation = sum(weight * abs(value - fused) for value, weight in pairs)
    agreement = 1 - deviation / max(total_weight * tolerance, eps)
    return max(0.0, min(1.0, agreement)), fused


__all__ = ['compute_byzantine_trust_weighted_agreement']

_policy.bind(globals())
