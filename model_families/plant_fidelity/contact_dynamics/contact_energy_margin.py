"""PF-004 - contact_energy_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/contact_dynamics/contact_energy_margin')


from math import isfinite
from typing import Sequence


def _vec3(name: str, value: Sequence[float]) -> tuple[float, float, float]:
    if len(value) != 3:
        raise ValueError(f"{name} must have length 3")
    out = tuple(float(v) for v in value)
    if not all(isfinite(v) for v in out):
        raise ValueError(f"{name} must be finite")
    return out  # type: ignore[return-value]


def compute_contact_energy_margin(
    mass_kg: float,
    relative_speed_m_s: float,
    drop_height_m: float,
    inertia_diag_kg_m2: Sequence[float],
    omega_body_rad_s: Sequence[float],
    max_dissipatable_energy_j: float,
    gravity_m_s2: float = _policy.default,
) -> float:
    mass = float(mass_kg)
    v_rel = float(relative_speed_m_s)
    h = float(drop_height_m)
    e_max = float(max_dissipatable_energy_j)
    g = float(gravity_m_s2)

    if not all(isfinite(x) for x in (mass, v_rel, h, e_max, g)):
        raise ValueError("scalar inputs must be finite")
    if mass <= 0:
        raise ValueError("mass_kg must be positive")
    if v_rel < 0 or h < 0:
        raise ValueError("relative_speed_m_s and drop_height_m must be non-negative")
    if e_max < 0 or g <= 0:
        raise ValueError("max_dissipatable_energy_j must be non-negative and gravity_m_s2 positive")

    Ixx, Iyy, Izz = _vec3("inertia_diag_kg_m2", inertia_diag_kg_m2)
    wx, wy, wz = _vec3("omega_body_rad_s", omega_body_rad_s)
    if Ixx <= 0 or Iyy <= 0 or Izz <= 0:
        raise ValueError("inertia diagonal terms must be positive")

    translational = 0.5 * mass * v_rel * v_rel
    potential = mass * g * h
    rotational = 0.5 * (Ixx * wx * wx + Iyy * wy * wy + Izz * wz * wz)
    return e_max - (translational + potential + rotational)


__all__ = ['compute_contact_energy_margin']

_policy.bind(globals())
