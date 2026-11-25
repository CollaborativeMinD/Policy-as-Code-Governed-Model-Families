"""C.3 and C.4 — Orbital dynamics laws"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/orbital_dynamics')


import math


def compute_mean_motion(mu: float, a: float) -> float:
    """Compute the orbital mean motion.

    Parameters
    ----------
    mu : float
        Standard gravitational parameter (m³/s²).
    a : float
        Semi‑major axis (m).

    Returns
    -------
    float
        Mean motion ``n`` (rad/s).
    """
    if a <= 0:
        raise ValueError("Semi‑major axis a must be positive")
    return math.sqrt(mu / (a ** 3))


def compute_j2_nodal_precession(J2: float, n: float, R_E: float, p: float, i: float) -> float:
    """Compute the J2 nodal precession rate.

    Parameters
    ----------
    J2 : float
        Second zonal harmonic coefficient (dimensionless).
    n : float
        Mean motion (rad/s).
    R_E : float
        Earth's radius (m).
    p : float
        Semi‑latus rectum (m).
    i : float
        Inclination angle (radians).

    Returns
    -------
    float
        Nodal precession rate ``Ω̇`` (rad/s).
    """
    if R_E <= 0 or p <= 0:
        raise ValueError("R_E and p must be positive")
    return -1.5 * J2 * n * (R_E / p) ** 2 * math.cos(i)


__all__ = ['compute_mean_motion', 'compute_j2_nodal_precession']

_policy.bind(globals())
