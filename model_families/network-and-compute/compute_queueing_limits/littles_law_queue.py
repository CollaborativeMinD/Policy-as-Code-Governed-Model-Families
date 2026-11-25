"""PCC-17 — DOM Preventer, Little's Law."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/compute_queueing_limits/littles_law_queue')


def symbolic_expression() -> str:
    return 'lam * W'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(lam, W):
        return lam * W

    return evaluate


def compute_little_law_queue_length(arrival_rate_per_s: float, processing_time_s: float) -> float:
    if arrival_rate_per_s < 0.0 or processing_time_s < 0.0:
        raise ValueError("arrival_rate_per_s and processing_time_s must be non-negative")
    return float(arrival_rate_per_s * processing_time_s)


def compute_queue_margin(arrival_rate_per_s: float, processing_time_s: float, queue_limit: float) -> float:
    if queue_limit < 0.0:
        raise ValueError("queue_limit must be non-negative")
    return float(queue_limit - compute_little_law_queue_length(arrival_rate_per_s, processing_time_s))


def should_throttle(arrival_rate_per_s: float, processing_time_s: float, queue_limit: float) -> bool:
    return bool(compute_queue_margin(arrival_rate_per_s, processing_time_s, queue_limit) < 0.0)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_little_law_queue_length",
    "compute_queue_margin",
    "should_throttle",
]

_policy.bind(globals())
