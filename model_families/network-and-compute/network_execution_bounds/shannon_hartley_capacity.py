"""PCC-08 — Limit of the Invisible Thread, Shannon-Hartley capacity."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('network-and-compute/network_execution_bounds/shannon_hartley_capacity')


import math


def symbolic_expression() -> str:
    return 'B * math.log(1 + S / N, 2)'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(B, S, N):
        return B * math.log(1 + S / N, 2)

    return evaluate


def compute_channel_capacity_bps(bandwidth_hz: float, signal_power_w: float, noise_power_w: float) -> float:
    if bandwidth_hz <= 0.0 or signal_power_w < 0.0 or noise_power_w <= 0.0:
        raise ValueError("bandwidth and noise must be positive; signal must be non-negative")
    return float(bandwidth_hz * math.log2(1.0 + signal_power_w / noise_power_w))


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_channel_capacity_bps",
]

_policy.bind(globals())
