"""PCC-11 — DODA Law, kinetic latency bound."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/network_execution_bounds/doda_latency_bound')


from collections.abc import Sequence


def symbolic_expression() -> str:
    return 'T_budget - T_total'


def lambdified_margin():
    @_policy.evaluator("lambdified_margin.evaluate")
    def evaluate(T_budget, T_total):
        return T_budget - T_total

    return evaluate


def compute_latency_budget_margin(hop_latencies_s: Sequence[float], time_budget_s: float) -> float:
    if time_budget_s < 0.0:
        raise ValueError("time_budget_s must be non-negative")
    if any(float(v) < 0.0 for v in hop_latencies_s):
        raise ValueError("hop latencies must be non-negative")
    return float(float(time_budget_s) - sum(float(v) for v in hop_latencies_s))


def within_latency_budget(hop_latencies_s: Sequence[float], time_budget_s: float) -> bool:
    return bool(compute_latency_budget_margin(hop_latencies_s, time_budget_s) >= 0.0)


__all__ = [
    "symbolic_expression",
    "lambdified_margin",
    "compute_latency_budget_margin",
    "within_latency_budget",
]

_policy.bind(globals())
