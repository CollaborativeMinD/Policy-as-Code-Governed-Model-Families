"""THERM-TELEM-004 — Multisensor consistency margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/multisensor_consistency_margin')

from collections.abc import Sequence
from statistics import median


def symbolic_expression() -> str:
    return 'tol - spread'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(tol, spread):
        return tol - spread

    return evaluate


def compute_multisensor_consistency_margin(sensor_temps_c: Sequence[float], allowed_spread_c: float) -> float:
    if not sensor_temps_c:
        raise ValueError("sensor_temps_c cannot be empty")
    if allowed_spread_c <= 0:
        raise ValueError("allowed_spread_c must be > 0")
    center = median(sensor_temps_c)
    spread = max(abs(float(value) - center) for value in sensor_temps_c)
    return float(allowed_spread_c - spread)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_multisensor_consistency_margin",
]

_policy.bind(globals())
