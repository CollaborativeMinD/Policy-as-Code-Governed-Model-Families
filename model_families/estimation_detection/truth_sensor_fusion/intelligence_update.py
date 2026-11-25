"""PCC-07 — Intelligence Update, Bayes theorem."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/truth_sensor_fusion/intelligence_update')


def symbolic_expression() -> str:
    return 'p_b_given_a * p_a / p_b'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(p_b_given_a, p_a, p_b):
        return p_b_given_a * p_a / p_b

    return evaluate


def compute_bayes_posterior(p_b_given_a: float, p_a: float, p_b: float) -> float:
    for name, value in {"p_b_given_a": p_b_given_a, "p_a": p_a, "p_b": p_b}.items():
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"{name} must be in [0,1]")
    if p_b <= 0.0:
        raise ValueError("p_b must be greater than zero")
    posterior = (float(p_b_given_a) * float(p_a)) / float(p_b)
    return float(max(0.0, min(1.0, posterior)))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_bayes_posterior",
]

_policy.bind(globals())
