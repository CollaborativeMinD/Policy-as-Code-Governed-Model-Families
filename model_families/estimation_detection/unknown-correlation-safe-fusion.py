"""Proposed formula M5.3 — Unknown-Correlation Safe Fusion (Covariance Intersection)."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/unknown-correlation-safe-fusion')


from typing import Iterable
import math


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


def compute_covariance_intersection(
    x_a: Iterable[float],
    p_a: Iterable[Iterable[float]],
    x_b: Iterable[float],
    p_b: Iterable[Iterable[float]],
    omega: float = _policy.default,
) -> tuple[list[float], list[list[float]]]:
    if not 0 <= omega <= 1:
        raise ValueError("omega must be in [0,1]")
    p_a, p_b = [list(row) for row in p_a], [list(row) for row in p_b]
    x_a = [float(x_a)] if isinstance(x_a, (int, float)) else list(x_a)
    x_b = [float(x_b)] if isinstance(x_b, (int, float)) else list(x_b)
    alpha, beta = omega, 1-omega

    first, second = _inverse(p_a), _inverse(p_b)
    covariance = _inverse(_combine(first, second, alpha, beta))
    rhs = [alpha*a + beta*b for a, b in zip(_matvec(first, x_a), _matvec(second, x_b), strict=True)]
    state = _matvec(covariance, rhs)
    return state, covariance

_policy.bind(globals())
