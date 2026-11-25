"""M4.1c — Fastener preload retention margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/resonance/Fastener-preload-retention-margin')


from typing import Dict, Any


def compute_fastener_preload_retention_margin(
    initial_preload: float,
    joint_stiffness: float,
    alpha_joint: float,
    alpha_clamped: float,
    grip_length: float,
    delta_temperature: float,
    external_separating_load: float,
    load_loss_factor: float,
    minimum_retained_preload: float,
) -> Dict[str, Any]:
    if joint_stiffness <= 0.0:
        raise ValueError("joint_stiffness must be positive")
    if grip_length < 0.0:
        raise ValueError("grip_length must be non-negative")
    if load_loss_factor < 0.0:
        raise ValueError("load_loss_factor must be non-negative")
    if minimum_retained_preload <= 0.0:
        raise ValueError("minimum_retained_preload must be positive")

    thermal_loss = joint_stiffness * (alpha_joint - alpha_clamped) * grip_length * delta_temperature
    mechanical_loss = load_loss_factor * external_separating_load
    retained_preload = initial_preload - thermal_loss - mechanical_loss
    margin = (retained_preload - minimum_retained_preload) / minimum_retained_preload

    return {
        "thermal_loss": thermal_loss,
        "mechanical_loss": mechanical_loss,
        "retained_preload": retained_preload,
        "retention_margin": margin,
        "joint_secure": bool(retained_preload >= minimum_retained_preload),
    }


__all__ = ['compute_fastener_preload_retention_margin']

_policy.bind(globals())
