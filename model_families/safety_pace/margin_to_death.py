"""M1.2 — Margin‑to‑death function"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('safety_pace/margin_to_death')


def compute_margin_to_death(phi_value: float, c_max: float) -> float:
    """Compute the margin‑to‑death for a single constraint.

    Parameters
    ----------
    phi_value : float
        The constraint metric φ_i(x).
    c_max : float
        The maximum allowable value C_i,max.

    Returns
    -------
    float
        The margin m_i(x) ∈ ℝ.  A value ≤ 0 indicates violation.

    Raises
    ------
    ValueError
        If ``c_max`` is zero or negative.
    """
    if c_max <= 0:
        raise ValueError(f"c_max must be positive; got {c_max}")
    return 1.0 - (phi_value / c_max)


__all__ = ['compute_margin_to_death']

_policy.bind(globals())
