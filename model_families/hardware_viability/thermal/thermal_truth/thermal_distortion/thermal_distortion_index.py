"""THERM-SILENT-001 — thermal_distortion_index"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_distortion/thermal_distortion_index')


def compute_thermal_distortion_index(
    temp_c: float,
    warning_high_c: float,
    critical_high_c: float,
    latency_baseline_ms: float,
    latency_current_ms: float,
    throughput_baseline_hz: float,
    throughput_current_hz: float,
    clock_fraction: float,
) -> float:
    thermal_utilization = max(0.0, (temp_c - warning_high_c) / max(critical_high_c - warning_high_c, _policy.value("denominator_floor")))
    latency_inflation = max(0.0, (latency_current_ms / max(latency_baseline_ms, _policy.value("denominator_floor"))) - 1.0)
    throughput_loss = max(0.0, 1.0 - (throughput_current_hz / max(throughput_baseline_hz, _policy.value("denominator_floor"))))
    clock_loss = max(0.0, 1.0 - clock_fraction)
    return float(max(thermal_utilization, latency_inflation, throughput_loss, clock_loss))


thermal_distortion_index = compute_thermal_distortion_index

__all__ = ['compute_thermal_distortion_index', 'thermal_distortion_index']

_policy.bind(globals())
