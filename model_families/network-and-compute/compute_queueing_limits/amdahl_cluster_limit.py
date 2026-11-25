"""PCC-16 — Illusion of the Cluster, Amdahl's Law."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/compute_queueing_limits/amdahl_cluster_limit')


def symbolic_expression() -> str:
    return '1 / (1 - p + p / s)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(p, s):
        return 1 / (1 - p + p / s)

    return evaluate


def compute_amdahl_speedup(parallel_fraction: float, workers: float) -> float:
    if not 0.0 <= parallel_fraction <= 1.0:
        raise ValueError("parallel_fraction must be in [0,1]")
    if workers <= 0.0:
        raise ValueError("workers must be positive")
    return float(1.0 / ((1.0 - parallel_fraction) + parallel_fraction / workers))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_amdahl_speedup",
]

_policy.bind(globals())
