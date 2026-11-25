"""M3.1c — Actuator saturation law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/actuator_saturation')


def compute_actuator_saturation(u_cmd: float, u_min: float, u_max: float) -> float:
    """Clip the commanded control input to the allowable range.

    Parameters
    ----------
    u_cmd : float
        Commanded control input.
    u_min : float
        Minimum allowable input.
    u_max : float
        Maximum allowable input.

    Returns
    -------
    float
        Saturated control input.
    """
    if u_min > u_max:
        raise ValueError(f"u_min ({u_min}) must be <= u_max ({u_max})")
    return max(u_min, min(u_cmd, u_max))


__all__ = ['compute_actuator_saturation']

_policy.bind(globals())
