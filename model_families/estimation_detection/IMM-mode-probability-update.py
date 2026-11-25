"""Proposed formula M5.4 — IMM Mode Probability Update."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/IMM-mode-probability-update')


from typing import Iterable
import math


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def compute_imm_mode_probability_update(
    mode_probabilities: Iterable[float],
    transition_matrix: Iterable[Iterable[float]],
    likelihoods: Iterable[float],
) -> list[float]:
    prior, likelihood = list(mode_probabilities), list(likelihoods)
    matrix = [list(row) for row in transition_matrix]
    size = len(prior)
    if len(likelihood) != size or len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("transition matrix and likelihoods must match the number of modes")
    if any(x < 0 for x in prior + likelihood):
        raise ValueError("probabilities and likelihoods must be nonnegative")
    if not all(abs(sum(row) - 1.0) <= _policy.value("row_sum_tolerance") for row in matrix):
        raise ValueError("each transition row must sum to one")
    scale = max(sum(prior), _policy.value("denominator_floor"))
    normalized = [p / scale for p in prior]
    posterior = [l * _dot(normalized, column) for l, column in zip(likelihood, zip(*matrix))]
    total = sum(posterior)
    if total <= 0:
        return [1.0 / size for _ in prior]
    return [p / total for p in posterior]

_policy.bind(globals())
