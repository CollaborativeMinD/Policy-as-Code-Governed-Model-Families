"""P1.2 — Two-layer thermal distortion law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/two_layer_thermal_distortion')


def compute_two_layer_thermal_dynamics(
    core_temp: float,
    surface_temp: float,
    ambient_temp: float,
    heat_generation: float,
    core_heat_capacity: float,
    surface_heat_capacity: float,
    core_surface_resistance: float,
    surface_ambient_resistance: float,
    alpha: float = _policy.default,
    beta: float = _policy.default,
    nominal_temp: float = _policy.default,
) -> dict[str, float]:
    if min(core_heat_capacity, surface_heat_capacity, core_surface_resistance, surface_ambient_resistance) <= 0:
        raise ValueError("thermal capacities and resistances must be positive")
    core_dot = (heat_generation + (surface_temp - core_temp) / core_surface_resistance) / core_heat_capacity
    surface_dot = (
        (ambient_temp - surface_temp) / surface_ambient_resistance
        - (surface_temp - core_temp) / core_surface_resistance
    ) / surface_heat_capacity
    distortion_index = alpha * max(0.0, core_temp - nominal_temp) + beta * abs(core_temp - surface_temp)
    return {
        "core_temp_dot": float(core_dot),
        "surface_temp_dot": float(surface_dot),
        "thermal_distortion_index": float(distortion_index),
    }

__all__ = ['compute_two_layer_thermal_dynamics']

_policy.bind(globals())
