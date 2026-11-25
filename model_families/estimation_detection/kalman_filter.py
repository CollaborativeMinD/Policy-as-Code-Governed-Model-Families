"""M5.2 — Kalman filter prediction and update"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/kalman_filter')


import math
from typing import Sequence


def _dot(left, right):
    return math.fsum(float(a) * float(b) for a, b in zip(left, right, strict=True))


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _transpose(matrix):
    return [list(column) for column in zip(*matrix, strict=True)]


def _matmul(left, right):
    columns = _transpose(right)
    return [[_dot(row, column) for column in columns] for row in left]


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


def kalman_predict_update(
    A: Sequence[Sequence[float]],
    B: Sequence[Sequence[float]],
    H: Sequence[Sequence[float]],
    x_prev: Sequence[float],
    P_prev: Sequence[Sequence[float]],
    u_prev: Sequence[float],
    z_k: Sequence[float],
    Q: Sequence[Sequence[float]],
    R: Sequence[Sequence[float]],
) -> tuple[list[float], list[list[float]]]:
    """Perform one Kalman filter prediction and update step.

    Parameters
    ----------
    A, B, H : Sequence of matrices
        State transition, control, and observation matrices.
    x_prev : Sequence[float]
        Prior state estimate x̂_{k−1|k−1}.
    P_prev : Sequence[Sequence[float]]
        Prior state covariance P_{k−1|k−1}.
    u_prev : Sequence[float]
        Control input u_{k−1}.
    z_k : Sequence[float]
        Measurement vector at time k.
    Q : Sequence[Sequence[float]]
        Process noise covariance.
    R : Sequence[Sequence[float]]
        Measurement noise covariance.

    Returns
    -------
    tuple[list[float], list[list[float]]]
        Updated state estimate x̂_{k|k} and covariance P_{k|k}.

    Raises
    ------
    ValueError
        If matrix dimensions do not align or matrix inversion fails.
    """
    predicted = [a + b for a, b in zip(_matvec(A, x_prev), _matvec(B, u_prev), strict=True)]
    covariance = _combine(_matmul(_matmul(A, P_prev), _transpose(A)), Q)
    innovation = [z - h for z, h in zip(z_k, _matvec(H, predicted), strict=True)]
    cross_covariance = _matmul(covariance, _transpose(H))
    innovation_covariance = _combine(_matmul(H, cross_covariance), R)
    gain = _matmul(cross_covariance, _inverse(innovation_covariance))
    state = [x + dx for x, dx in zip(predicted, _matvec(gain, innovation), strict=True)]
    correction = _combine(_identity(len(state)), _matmul(gain, H), b=-1)
    # Joseph form retains measurement noise even when the gain rounds to one.
    prior_term = _matmul(_matmul(correction, covariance), _transpose(correction))
    noise_term = _matmul(_matmul(gain, R), _transpose(gain))
    return state, _combine(prior_term, noise_term)


__all__ = ['kalman_predict_update']

_policy.bind(globals())
