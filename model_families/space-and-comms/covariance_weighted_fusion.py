"""C.5 — Covariance‑weighted sensor fusion"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/covariance_weighted_fusion')


import math
from typing import Sequence, Tuple


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _identity(size):
    return [[float(i == j) for j in range(size)] for i in range(size)]


def _combine(left, right, a=1.0, b=1.0):
    return [[a*x + b*y for x, y in zip(lrow, rrow, strict=True)]
            for lrow, rrow in zip(left, right, strict=True)]


def _inverse(matrix):
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    rows = [list(map(float, row)) + unit for row, unit in zip(matrix, _identity(size))]
    for col in range(size):
        pivot = max(range(col, size), key=lambda i: abs(rows[i][col]))
        if rows[pivot][col] == 0:
            raise ValueError("matrix is singular")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for i in range(size):
            if i != col:
                factor = rows[i][col]
                rows[i] = [x - factor*y for x, y in zip(rows[i], rows[col])]
    return [row[size:] for row in rows]


def fuse_estimates(
    P1: Sequence[Sequence[float]],
    P2: Sequence[Sequence[float]],
    x_hat1: Sequence[float],
    x_hat2: Sequence[float],
) -> tuple[list[list[float]], list[float]]:
    """Fuse two estimates based on their covariances.

    Parameters
    ----------
    P1, P2 : Sequence of matrices
        Covariance matrices of the individual estimates.
    x_hat1, x_hat2 : Sequence of floats
        The state estimates.

    Returns
    -------
    tuple[list[list[float]], list[float]]
        Tuple of (fused covariance P, fused state x_hat).
    """
    first, second = _inverse(P1), _inverse(P2)
    covariance = _inverse(_combine(first, second))
    rhs = [a + b for a, b in zip(_matvec(first, x_hat1), _matvec(second, x_hat2), strict=True)]
    state = _matvec(covariance, rhs)
    return covariance, state


__all__ = ['fuse_estimates']

_policy.bind(globals())
