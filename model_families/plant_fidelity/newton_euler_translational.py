"""M3.1a — Newton–Euler translational plant law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('plant_fidelity/newton_euler_translational')


def compute_translational_acceleration(
    mass: float,
    thrust: float,
    disturbance: float,
    velocity: float,
    rho: float,
    C_d: float,
    area: float,
    g: float,
) -> float:
    """Compute the translational acceleration ``v̇`` of a point mass.

    Parameters
    ----------
    mass : float
        Instantaneous mass ``m(t)`` of the system (kg).
    thrust : float
        Applied thrust force ``F_thrust(u)`` (N).
    disturbance : float
        External disturbance force ``F_dist(w)`` (N).
    velocity : float
        Current velocity ``v`` (m/s).  The sign indicates direction.
    rho : float
        Ambient fluid density ρ (kg/m³).
    C_d : float
        Drag coefficient (dimensionless).
    area : float
        Reference area A (m²).
    g : float
        Gravitational acceleration (m/s²).  Positive values denote
        acceleration due to gravity in the opposite direction of thrust.

    Returns
    -------
    float
        The resulting acceleration ``v̇`` (m/s²).

    Raises
    ------
    ValueError
        If ``mass`` is non‑positive.
    """
    if mass <= 0:
        raise ValueError(f"mass must be positive; got {mass}")
    # Quadratic drag magnitude
    # Drag magnitude is always non‑negative and proportional to |v|^2
    drag_magnitude = 0.5 * rho * C_d * area * abs(velocity) * abs(velocity)
    # Drag acts opposite the sign of velocity.  When velocity is positive,
    # drag is negative; when velocity is negative, drag is positive.
    F_drag = -drag_magnitude if velocity > 0 else drag_magnitude
    # Sum of forces
    total_force = thrust + disturbance + F_drag
    # Newton–Euler translational equation
    return total_force / mass - g


__all__ = ['compute_translational_acceleration']

_policy.bind(globals())
