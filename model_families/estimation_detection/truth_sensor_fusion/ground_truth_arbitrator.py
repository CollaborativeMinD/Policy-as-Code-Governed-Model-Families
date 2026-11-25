"""PCC-06 — Ground Truth Arbitrator, scalar Kalman filter."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/truth_sensor_fusion/ground_truth_arbitrator')


import math


def symbolic_expression_update() -> str:
    return 'x_pred + K * (z - H * x_pred)'


def lambdified_update():
    @_policy.evaluator("lambdified_update.evaluate")
    def evaluate(x_pred, K, z, H):
        return x_pred + K * (z - H * x_pred)

    return evaluate


def compute_scalar_kalman_update(
    x_previous: float,
    p_previous: float,
    control: float,
    sensor: float,
    F: float = _policy.default,
    B: float = _policy.default,
    H: float = _policy.default,
    Q: float = _policy.default,
    R: float = _policy.default,
) -> dict[str, float]:
    if p_previous < 0.0 or Q < 0.0 or R <= 0.0:
        raise ValueError("p_previous and Q must be non-negative; R must be positive")
    x_pred = F * x_previous + B * control
    p_pred = F * p_previous * F + Q
    innovation = sensor - H * x_pred
    innovation_covariance = H * p_pred * H + R
    if innovation_covariance <= 0.0 or not math.isfinite(innovation_covariance):
        raise ValueError("innovation covariance must be positive and finite")
    K = p_pred * H / innovation_covariance
    x_new = x_pred + K * innovation
    p_new = (1.0 - K * H) * p_pred
    return {
        "x_predict": float(x_pred),
        "p_predict": float(p_pred),
        "kalman_gain": float(K),
        "innovation": float(innovation),
        "x_new": float(x_new),
        "p_new": float(p_new),
    }


__all__ = [
    "symbolic_expression_update",
    "lambdified_update",
    "compute_scalar_kalman_update",
]

_policy.bind(globals())
