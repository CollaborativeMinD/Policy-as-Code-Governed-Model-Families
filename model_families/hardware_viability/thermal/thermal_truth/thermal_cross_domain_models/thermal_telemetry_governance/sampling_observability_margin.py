"""THERM-TELEM-003 — Sampling observability margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/sampling_observability_margin')


def symbolic_expression() -> str:
    return 'tau / N - dt'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(tau, dt, N):
        return tau / N - dt

    return evaluate


def compute_sampling_observability_margin(thermal_time_constant_s: float, sample_period_s: float, min_samples_per_time_constant: float) -> float:
    if thermal_time_constant_s <= 0 or sample_period_s <= 0 or min_samples_per_time_constant <= 0:
        raise ValueError("all inputs must be > 0")
    return float(thermal_time_constant_s / min_samples_per_time_constant - sample_period_s)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_sampling_observability_margin",
]

_policy.bind(globals())
