"""M5.1 — Weighted divergence between reality and twin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/weighted_divergence')


import math
from typing import Sequence


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def compute_weighted_divergence(x_real: Sequence[float], x_twin: Sequence[float], W: Sequence[Sequence[float]]) -> float:
    """Compute the weighted divergence between two state vectors.

    Parameters
    ----------
    x_real : Sequence[float]
        Real system state vector.
    x_twin : Sequence[float]
        Digital twin state vector.
    W : Sequence[Sequence[float]]
        Weighting matrix.

    Returns
    -------
    float
        Weighted divergence ``Δ(t)``.
    """
    diff = [float(a) - float(b) for a, b in zip(x_real, x_twin, strict=True)]
    quadratic = _dot(diff, _matvec(W, diff))
    return math.sqrt(quadratic) if quadratic >= 0 else math.nan


__all__ = ['compute_weighted_divergence']

_policy.bind(globals())
