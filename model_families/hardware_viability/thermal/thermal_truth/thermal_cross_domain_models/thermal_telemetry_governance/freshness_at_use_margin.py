"""THERM-TELEM-001 — Freshness at use margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/freshness_at_use_margin')


def symbolic_expression() -> str:
    return 'tau - (use - sample)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(use, sample, tau):
        return tau - (use - sample)

    return evaluate


def compute_freshness_at_use_margin(use_time_s: float, sample_time_s: float, freshness_budget_s: float) -> float:
    if freshness_budget_s <= 0:
        raise ValueError("freshness_budget_s must be > 0")
    if use_time_s < sample_time_s:
        raise ValueError("use_time_s cannot be earlier than sample_time_s")
    return float(freshness_budget_s - (use_time_s - sample_time_s))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_freshness_at_use_margin",
]

_policy.bind(globals())
