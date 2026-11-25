"""THERM-TIME-002 — Deadline margin under derate."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/deadline_margin_under_derate')


def symbolic_expression() -> str:
    return 'deadline - nominal / phi'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(deadline, nominal, phi):
        return deadline - nominal / phi

    return evaluate


def compute_deadline_margin_under_derate(deadline_budget_ms: float, nominal_latency_ms: float, clock_derate_fraction: float) -> float:
    if deadline_budget_ms <= 0 or nominal_latency_ms <= 0:
        raise ValueError("deadline_budget_ms and nominal_latency_ms must be > 0")
    if not 0.0 < clock_derate_fraction <= 1.0:
        raise ValueError("clock_derate_fraction must be in (0, 1]")
    return float(deadline_budget_ms - nominal_latency_ms / clock_derate_fraction)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_deadline_margin_under_derate",
]

_policy.bind(globals())
