"""Proposed formula M5.5 — Delay-Adjusted Innovation Consistency Statistic."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/delay-adjusted-innovation-consistency')


from typing import Iterable
import math


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


def compute_delay_adjusted_innovation_consistency(
    residual: Iterable[float],
    innovation_covariance: Iterable[Iterable[float]],
    measurement_age_s: float,
    cadence_s: float,
    sequence_gap: int = _policy.default,
    dynamic_staleness: float = _policy.default,
    lambda_age: float = _policy.default,
    lambda_seq: float = _policy.default,
    lambda_dyn: float = _policy.default,
) -> float:
    if cadence_s <= 0 or measurement_age_s < 0 or dynamic_staleness < 0:
        raise ValueError("cadence must be positive and age and staleness nonnegative")
    nu = [float(residual)] if isinstance(residual, (int, float)) else list(residual)
    covariance = [list(row) for row in innovation_covariance]
    nis = _dot(nu, _matvec(_inverse(covariance), nu))
    return nis * (1 + lambda_age * measurement_age_s / cadence_s
                  + lambda_seq * max(sequence_gap, 0) + lambda_dyn * dynamic_staleness)

_policy.bind(globals())
