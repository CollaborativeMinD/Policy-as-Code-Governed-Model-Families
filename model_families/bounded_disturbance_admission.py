"""M3.1e — Bounded disturbance injection"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('bounded_disturbance_admission')


import math
from typing import Sequence


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def compute_bounded_disturbance(
    A: Sequence[Sequence[float]],
    B: Sequence[Sequence[float]],
    G: Sequence[Sequence[float]],
    x: Sequence[float],
    u: Sequence[float],
    w: Sequence[float],
    w_max: float,
) -> list[float]:
    """Compute the state derivative under bounded disturbance.

    Parameters
    ----------
    A, B, G : Sequence[Sequence[float]]
        System matrices of appropriate dimensions.
    x : Sequence[float]
        Current state vector.
    u : Sequence[float]
        Control input vector.
    w : Sequence[float]
        Disturbance vector.
    w_max : float
        Maximum allowable norm of the disturbance vector.

    Returns
    -------
    list[float]
        The state derivative ``ẋ``.

    Raises
    ------
    ValueError
        If ``||w|| > w_max`` or dimensions are inconsistent.
    """
    norm_w = math.hypot(*w)
    if norm_w > w_max:
        raise ValueError(f"Disturbance norm {norm_w} exceeds w_max {w_max}")
    return [a + b + g for a, b, g in zip(_matvec(A, x), _matvec(B, u), _matvec(G, w), strict=True)]


__all__ = ['compute_bounded_disturbance']

_policy.bind(globals())
