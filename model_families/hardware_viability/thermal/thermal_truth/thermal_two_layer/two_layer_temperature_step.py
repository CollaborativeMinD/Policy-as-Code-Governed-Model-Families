"""THERM-2L-002 — two_layer_temperature_step"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_two_layer/two_layer_temperature_step')


def compute_surface_radiative_forcing_density(alpha: float, area_m2: float, insolation_w_m2: float, epsilon: float, T_skin_c: float, T_env_c: float) -> float:
    sigma = 5.670374419e-8
    t_skin_k = T_skin_c + 273.15
    t_env_k = T_env_c + 273.15
    return float(alpha * area_m2 * max(insolation_w_m2, 0.0) - epsilon * sigma * area_m2 * (t_skin_k**4 - t_env_k**4))


def compute_two_layer_temperature_step(
    skin_temp_c: float,
    substrate_temp_c: float,
    env_temp_c: float,
    insolation_w_m2: float,
    alpha: float,
    epsilon: float,
    area_m2: float,
    skin_heat_capacity_j_per_c: float,
    substrate_heat_capacity_j_per_c: float,
    conduction_w_per_c: float,
    internal_power_w: float,
    heater_power_w: float,
    dt_s: float,
) -> tuple[float, float]:
    if float(dt_s) < 0.0:
        raise ValueError("dt_s must be non-negative")
    if float(skin_heat_capacity_j_per_c) <= 0.0 or float(substrate_heat_capacity_j_per_c) <= 0.0:
        raise ValueError("heat capacities must be positive")
    if float(area_m2) < 0.0 or float(conduction_w_per_c) < 0.0:
        raise ValueError("area_m2 and conduction_w_per_c must be non-negative")
    q_surf = compute_surface_radiative_forcing_density(
        alpha,
        area_m2,
        insolation_w_m2,
        epsilon,
        skin_temp_c,
        env_temp_c,
    )
    q_cond = float(conduction_w_per_c) * (float(skin_temp_c) - float(substrate_temp_c))
    d_skin = (q_surf - q_cond) * float(dt_s) / float(skin_heat_capacity_j_per_c)
    d_sub = (q_cond + float(internal_power_w) + float(heater_power_w)) * float(dt_s) / float(substrate_heat_capacity_j_per_c)
    return float(float(skin_temp_c) + d_skin), float(float(substrate_temp_c) + d_sub)


two_layer_temperature_step = compute_two_layer_temperature_step

__all__ = ['compute_two_layer_temperature_step', 'two_layer_temperature_step']

_policy.bind(globals())
