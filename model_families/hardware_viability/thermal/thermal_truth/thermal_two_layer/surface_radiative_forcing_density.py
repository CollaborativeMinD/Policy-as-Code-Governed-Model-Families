"""THERM-2L-001 — surface_radiative_forcing_density"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/thermal/thermal_truth/thermal_two_layer/surface_radiative_forcing_density')


def compute_surface_radiative_forcing_density(alpha: float, area_m2: float, insolation_w_m2: float, epsilon: float, T_skin_c: float, T_env_c: float) -> float:
    sigma = 5.670374419e-8
    t_skin_k = T_skin_c + 273.15
    t_env_k = T_env_c + 273.15
    return float(alpha * area_m2 * max(insolation_w_m2, 0.0) - epsilon * sigma * area_m2 * (t_skin_k**4 - t_env_k**4))


surface_radiative_forcing_density = compute_surface_radiative_forcing_density

__all__ = ['compute_surface_radiative_forcing_density', 'surface_radiative_forcing_density']

_policy.bind(globals())
