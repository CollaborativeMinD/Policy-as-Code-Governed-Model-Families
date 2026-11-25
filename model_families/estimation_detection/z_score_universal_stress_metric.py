"""PCC-01 — Universal Stress Metric, Z-score."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/z_score_universal_stress_metric')


import math


def symbolic_expression() -> str:
    return '(x_live - mu_baseline) / sigma_baseline'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(x_live, mu_baseline, sigma_baseline):
        return (x_live - mu_baseline) / sigma_baseline

    return evaluate


def compute_z_score(x_live: float, mu_baseline: float, sigma_baseline: float) -> float:
    if not math.isfinite(sigma_baseline) or sigma_baseline <= 0.0:
        raise ValueError("sigma_baseline must be positive and finite")
    return float((float(x_live) - float(mu_baseline)) / float(sigma_baseline))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_z_score",
]

_policy.bind(globals())
