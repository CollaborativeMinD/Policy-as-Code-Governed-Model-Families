"""M3.1d — Actuator slew‑rate bound"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/actuator/actuator_slew_rate')


def compute_slew_limited_command(u_prev: float, u_cmd: float, dt: float, u_dot_max: float) -> float:
    """Limit the command based on the maximum slew rate.

    Parameters
    ----------
    u_prev : float
        Previous command value at the beginning of the time step.
    u_cmd : float
        Desired command value at the end of the time step.
    dt : float
        Duration of the time step (seconds).
    u_dot_max : float
        Maximum allowable rate of change (units per second).

    Returns
    -------
    float
        The adjusted command value that respects the slew rate bound.

    Raises
    ------
    ValueError
        If ``dt`` ≤ 0 or ``u_dot_max`` < 0.
    """
    if dt <= 0:
        raise ValueError(f"dt must be positive; got {dt}")
    if u_dot_max < 0:
        raise ValueError(f"u_dot_max must be non‑negative; got {u_dot_max}")
    max_delta = u_dot_max * dt
    delta = u_cmd - u_prev
    if abs(delta) <= max_delta:
        return u_cmd
    # Limit the change to ±max_delta
    return u_prev + max_delta if delta > 0 else u_prev - max_delta


__all__ = ['compute_slew_limited_command']

_policy.bind(globals())
