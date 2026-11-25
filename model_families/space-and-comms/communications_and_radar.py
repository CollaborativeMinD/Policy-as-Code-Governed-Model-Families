"""C.1 and C.2 — Communications link budget and radar range"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/communications_and_radar')


import math


def compute_received_power_db(P_t_db: float, G_t_db: float, G_r_db: float, L_p_db: float, L_a_db: float, L_s_db: float) -> float:
    """Compute the received power in dB.

    Parameters
    ----------
    P_t_db : float
        Transmit power (dBW).
    G_t_db : float
        Transmit antenna gain (dB).
    G_r_db : float
        Receive antenna gain (dB).
    L_p_db : float
        Path loss (dB).
    L_a_db : float
        Atmospheric loss (dB).
    L_s_db : float
        System loss (dB).

    Returns
    -------
    float
        Received power (dBW).
    """
    return P_t_db + G_t_db + G_r_db - L_p_db - L_a_db - L_s_db


def compute_radar_range(
    P_t: float,
    G: float,
    lambda_: float,
    sigma: float,
    S_min: float,
    L: float,
) -> float:
    """Compute the maximum radar detection range.

    Parameters
    ----------
    P_t : float
        Transmit power (W).
    G : float
        Antenna gain (linear).
    lambda_ : float
        Wavelength (m).
    sigma : float
        Radar cross section (m²).
    S_min : float
        Minimum detectable signal (W).
    L : float
        System losses (linear).

    Returns
    -------
    float
        Maximum detection range (m).

    Raises
    ------
    ValueError
        If any input is non‑positive.
    """
    if any(x <= 0 for x in (P_t, G, lambda_, sigma, S_min, L)):
        raise ValueError("All inputs must be positive")
    numerator = P_t * (G ** 2) * (lambda_ ** 2) * sigma
    denominator = ((4 * math.pi) ** 3) * S_min * L
    return (numerator / denominator) ** 0.25


__all__ = ['compute_received_power_db', 'compute_radar_range']

_policy.bind(globals())
