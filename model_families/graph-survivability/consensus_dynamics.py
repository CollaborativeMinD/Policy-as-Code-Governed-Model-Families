"""M2.5 — Consensus dynamics over graph topology"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('graph-survivability/consensus_dynamics')


import math
from typing import Sequence


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def compute_consensus_update(x: Sequence[float], L: Sequence[Sequence[float]], alpha: float) -> list[float]:
    """Perform one discrete consensus update step.

    Parameters
    ----------
    x : Sequence[float]
        Current state vector of length ``n``.
    L : Sequence[Sequence[float]]
        ``n×n`` Laplacian matrix of the underlying graph.
    alpha : float
        Step size (learning rate).  Must be positive.

    Returns
    -------
    list[float]
        The updated state vector ``x_{k+1}``.

    Raises
    ------
    ValueError
        If the dimensions of ``x`` and ``L`` do not align or if ``alpha`` is non‑positive.
    """
    if alpha <= 0:
        raise ValueError("alpha must be positive")
    return [v - alpha*d for v, d in zip(x, _matvec(L, x), strict=True)]


__all__ = ['compute_consensus_update']

_policy.bind(globals())
