"""M5.1a — Robust multivariate deviation score"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/mahalanobis')


import math
from typing import Sequence


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _identity(size):
    return [[float(i == j) for j in range(size)] for i in range(size)]


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


def compute_mahalanobis_distance(x: Sequence[float], mu: Sequence[float], Sigma: Sequence[Sequence[float]]) -> float:
    """Compute the Mahalanobis distance.

    Parameters
    ----------
    x : Sequence[float]
        Observation vector.
    mu : Sequence[float]
        Mean vector.
    Sigma : Sequence[Sequence[float]]
        Covariance matrix (must be symmetric positive definite).

    Returns
    -------
    float
        The Mahalanobis distance between ``x`` and the distribution
        defined by ``mu`` and ``Sigma``.

    Raises
    ------
    ValueError
        If dimensions do not align or if ``Sigma`` is singular.
    """
    diff = [float(a) - float(b) for a, b in zip(x, mu, strict=True)]
    quadratic = _dot(diff, _matvec(_inverse(Sigma), diff))
    return math.sqrt(quadratic) if quadratic >= 0 else math.nan


__all__ = ['compute_mahalanobis_distance']

_policy.bind(globals())
