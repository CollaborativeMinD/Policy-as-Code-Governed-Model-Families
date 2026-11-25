"""M3.2b — Attainable wrench residual law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/attainable_wrench_residual')


import math


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def compute_attainable_wrench_residual(
    allocation_matrix: list[list[float]],
    commanded_actuator: list[float],
    u_min: list[float],
    u_max: list[float],
    commanded_wrench: list[float],
    weight_matrix: list[list[float]] | None = _policy.default,
) -> float:
    command = [min(max(v, low), high) for v, low, high in zip(commanded_actuator, u_min, u_max, strict=True)]
    achieved = _matvec(allocation_matrix, command)
    residual = [a-b for a,b in zip(commanded_wrench, achieved, strict=True)]
    if weight_matrix is None:
        return math.hypot(*residual)
    quadratic = _dot(residual, _matvec(weight_matrix, residual))
    return math.sqrt(quadratic) if quadratic >= 0 else math.nan

__all__ = ['compute_attainable_wrench_residual']

_policy.bind(globals())
