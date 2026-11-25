"""M3.2b — Control allocation residual under bounded actuators"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/Control-allocation-residual')


from typing import Sequence

import math


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _transpose(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def _identity(size):
    return [[float(i == j) for j in range(size)] for i in range(size)]


def _singular_columns(matrix):
    '''One-sided Jacobi SVD. Columns become sigma*u, paired with right singular vectors.'''
    columns = _transpose(matrix)
    count = len(columns)
    axes = _identity(count)
    for _ in range(max(_policy.value("min_sweeps"), _policy.value("sweeps_per_column") * count)):
        rotated = False
        for p in range(count):
            for q in range(p+1, count):
                x, y = columns[p], columns[q]
                norm_x, norm_y = math.hypot(*x), math.hypot(*y)
                if not norm_x or not norm_y:
                    continue
                correlation = math.fsum((a/norm_x) * (b/norm_y) for a, b in zip(x, y))
                if abs(correlation) <= _policy.value("singular_tolerance"):
                    continue
                # Scale the two-column Gram matrix before forming the rotation.
                scale = max(norm_x, norm_y)
                rx, ry = norm_x/scale, norm_y/scale
                cross = 2 * rx * ry * correlation
                if cross == 0:
                    continue
                tau = (ry*ry - rx*rx) / cross
                tangent = math.copysign(1.0, tau) / (abs(tau) + math.hypot(1, tau))
                cosine = 1.0 / math.hypot(1.0, tangent)
                sine = cosine * tangent
                for basis in (columns, axes):
                    left, right = basis[p], basis[q]
                    basis[p] = [cosine*a - sine*b for a,b in zip(left, right)]
                    basis[q] = [sine*a + cosine*b for a,b in zip(left, right)]
                rotated = True
        if not rotated:
            break
    return [(math.hypot(*column), column, axis) for column, axis in zip(columns, axes)]


def compute_control_allocation_residual(
    effectiveness_matrix: Sequence[Sequence[float]],
    desired_wrench: Sequence[float],
    actuator_min: Sequence[float],
    actuator_max: Sequence[float],
) -> float:
    """Compute the allocation residual after actuator saturation."""
    matrix = [list(map(float, row)) for row in effectiveness_matrix]
    bounds = list(zip(actuator_min, actuator_max, strict=True))
    if any(low > high for low, high in bounds):
        raise ValueError("actuator_min cannot exceed actuator_max")
    if len(matrix) != len(desired_wrench) or any(len(row) != len(bounds) for row in matrix):
        raise ValueError("effectiveness matrix must match wrench and actuator dimensions")

    # Transpose wide matrices so the Jacobi iteration operates on independent axes.
    wide = len(bounds) > len(matrix)
    terms = _singular_columns(_transpose(matrix) if wide else matrix)
    cutoff = _policy.value("singular_tolerance") * max((sigma for sigma, _, _ in terms), default=0.0)
    command = [0.0] * len(bounds)
    for sigma, scaled_left, right in terms:
        if sigma <= cutoff:
            continue
        left = [v / sigma for v in scaled_left]
        input_axis, output_axis = (right, left) if wide else (left, right)
        component = _dot(input_axis, desired_wrench) / sigma
        command = [v + component*d for v, d in zip(command, output_axis, strict=True)]
    clipped = [max(low, min(high, v)) for v, (low, high) in zip(command, bounds)]
    return math.dist(desired_wrench, _matvec(matrix, clipped))


__all__ = ['compute_control_allocation_residual']

_policy.bind(globals())
