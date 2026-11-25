"""M3.2e — Authority-weighted controllability margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/controllability_margin')


from typing import Sequence

import math


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


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


def compute_authority_weighted_controllability_margin(
    effectiveness_matrix: Sequence[Sequence[float]],
    authority_weights: Sequence[float],
    required_min_singular_value: float,
) -> float:
    """Compute controllability margin after authority scaling."""
    weights = list(authority_weights)
    if any(a < 0 or a > 1 for a in weights) or required_min_singular_value < 0:
        raise ValueError("weights must lie in [0,1] and the singular-value requirement must be nonnegative")
    matrix = [[float(v)*a for v, a in zip(row, weights, strict=True)] for row in effectiveness_matrix]
    if len(weights) > len(matrix):
        matrix = _transpose(matrix)
    singular = _singular_columns(matrix)
    return min((sigma for sigma, _, _ in singular), default=0.0) - required_min_singular_value


__all__ = ['compute_authority_weighted_controllability_margin']

_policy.bind(globals())
