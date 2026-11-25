"""M3.4a — Spatial hazard set"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/spatial_hazard')


from typing import Sequence


def compute_hazard_function(p: Sequence[float], c: Sequence[float], r: float) -> float:
    """Compute the hazard function h_i(p).

    Parameters
    ----------
    p : Sequence[float]
        Point coordinates.
    c : Sequence[float]
        Center of the hazard sphere.
    r : float
        Radius of the hazard sphere.

    Returns
    -------
    float
        The hazard function value ``h_i(p) = ||p - c||² - r²``.  Values ≤ 0
        indicate that the point lies inside or on the hazard boundary.
    """
    if r < 0:
        raise ValueError("r must be non-negative")
    return sum((float(a) - float(b))**2 for a, b in zip(p, c, strict=True)) - r*r


def is_point_in_hazard(p: Sequence[float], c: Sequence[float], r: float) -> bool:
    """Check whether a point lies inside or on the hazard boundary.

    Returns ``True`` if ``h_i(p) ≤ 0``.
    """
    return compute_hazard_function(p, c, r) <= 0.0


__all__ = ['compute_hazard_function', 'is_point_in_hazard']

_policy.bind(globals())
