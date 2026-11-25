"""GEN-TRUTH-001 — generative_divergence_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_truth_governance/generative_divergence_margin')


from collections.abc import Sequence
import math
def weighted_quadratic_norm(a, b, weights) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    if len(weights) != len(a) or any(len(row) != len(a) for row in weights):
        raise ValueError("weights must be a square matrix matching vector length")
    diff = [float(x) - float(y) for x, y in zip(a, b)]
    accum = 0.0
    for i, di in enumerate(diff):
        for j, dj in enumerate(diff):
            accum += di * float(weights[i][j]) * dj
    return math.sqrt(max(accum, 0.0))


def compute_generative_divergence_margin(
    suggestion_vector: Sequence[float],
    baseline_vector: Sequence[float],
    allowed_bound: float,
    weights: Sequence[Sequence[float]] | None = _policy.default,
) -> float:
    if allowed_bound <= 0:
        raise ValueError("allowed_bound must be positive")
    n = len(suggestion_vector)
    if n == 0:
        raise ValueError("vectors must not be empty")
    if weights is None:
        weights = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    divergence = weighted_quadratic_norm(suggestion_vector, baseline_vector, weights)
    return float(allowed_bound - divergence)


generative_divergence_margin = compute_generative_divergence_margin

__all__ = ['compute_generative_divergence_margin', 'generative_divergence_margin']

_policy.bind(globals())
