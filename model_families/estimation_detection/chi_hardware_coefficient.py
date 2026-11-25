"""PCC-05 — Hardware Coefficient, composite mission vector."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/chi_hardware_coefficient')


import math


def compute_sigmoid(value: float) -> float:
    decay = math.exp(-abs(value))
    return 1.0 / (1.0 + decay) if value >= 0 else decay / (1.0 + decay)


def symbolic_expression() -> str:
    return 'T / Tmax * (L / Lmax) * (M / Mmax) * compute_sigmoid(Z)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(T, Tmax, L, Lmax, M, Mmax, Z):
        return T / Tmax * (L / Lmax) * (M / Mmax) * compute_sigmoid(Z)

    return evaluate


def _ratio(value: float, limit: float, name: str) -> float:
    if not math.isfinite(limit) or limit <= 0.0:
        raise ValueError(f"{name} limit must be positive and finite")
    return max(0.0, float(value) / float(limit))


def compute_hardware_coefficient(
    cpu_temp: float,
    cpu_temp_max: float,
    cpu_load: float,
    cpu_load_max: float,
    memory_used: float,
    memory_max: float,
    anomaly_z: float,
) -> float:
    pressure = (
        _ratio(cpu_temp, cpu_temp_max, "cpu_temp")
        * _ratio(cpu_load, cpu_load_max, "cpu_load")
        * _ratio(memory_used, memory_max, "memory")
        * compute_sigmoid(anomaly_z)
    )
    return float(pressure)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_hardware_coefficient",
]

_policy.bind(globals())
