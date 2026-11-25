"""M6.1c — Authority lease validity margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/lease_validity_margin')


def compute_authority_lease_validity_margin(
    lease_expiry_time: float,
    predicted_execution_time: float,
    clock_uncertainty: float,
    guard_band: float,
) -> float:
    """Compute remaining authority lease margin."""
    if clock_uncertainty < 0.0 or guard_band < 0.0:
        raise ValueError("clock_uncertainty and guard_band must be non-negative")
    return float(lease_expiry_time - predicted_execution_time - clock_uncertainty - guard_band)


__all__ = ['compute_authority_lease_validity_margin']

_policy.bind(globals())
