"""HORIZON-GEO-004 — solar_disk_guarded_clearance_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/horizon_geometry/solar_disk_clearance_margin')


def compute_solar_disk_guarded_clearance_margin(
    alpha_sun_center_deg: float,
    alpha_horizon_deg: float,
    alpha_sun_half_deg: float = _policy.default,
    alpha_pointing_err_deg: float = _policy.default,
    alpha_horizon_unc_deg: float = _policy.default,
) -> float:
    if alpha_sun_half_deg < 0 or alpha_pointing_err_deg < 0 or alpha_horizon_unc_deg < 0:
        raise ValueError("solar and uncertainty terms must be non-negative")
    return float(
        alpha_sun_center_deg
        - alpha_horizon_deg
        - alpha_sun_half_deg
        - alpha_pointing_err_deg
        - alpha_horizon_unc_deg
    )


solar_disk_guarded_clearance_margin = compute_solar_disk_guarded_clearance_margin

__all__ = ['compute_solar_disk_guarded_clearance_margin', 'solar_disk_guarded_clearance_margin']

_policy.bind(globals())
