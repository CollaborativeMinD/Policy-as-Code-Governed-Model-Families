"""M1.1 — Safe operational space"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('safety_pace/safe_operational_space')


from typing import Sequence


def compute_safe_operational_space(phi_values: Sequence[float], c_max: Sequence[float]) -> bool:
    """Evaluate whether the state lies in the safe operational space.

    Parameters
    ----------
    phi_values : Sequence[float]
        Normalized constraint metrics φ_i(x) for i=1..m.
    c_max : Sequence[float]
        Maximum allowable values C_i,max for the corresponding metrics.

    Returns
    -------
    bool
        ``True`` if ``phi_values[i] ≤ c_max[i]`` for all ``i``; ``False`` otherwise.

    Raises
    ------
    ValueError
        If the input sequences have different lengths.
    """
    if len(phi_values) != len(c_max):
        raise ValueError(
            "phi_values and c_max must have the same length; "
            f"got {len(phi_values)} and {len(c_max)}"
        )
    for phi_i, c_i in zip(phi_values, c_max):
        if phi_i > c_i:
            return False
    return True


__all__ = ['compute_safe_operational_space']

_policy.bind(globals())
