"""C.7 — Volley successor synthesis update"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/volley_successor')


def update_volley_successor(afb_k: float, delta_k: float, v_term_k: float) -> float:
    """Compute the next active fidelity baseline value.

    Parameters
    ----------
    afb_k : float
        Current active fidelity baseline.
    delta_k : float
        Weighted divergence at time ``k``.
    v_term_k : float
        Terminal state magnitude at time ``k``.

    Returns
    -------
    float
        Updated active fidelity baseline.
    """
    return afb_k + delta_k - v_term_k


__all__ = ['update_volley_successor']

_policy.bind(globals())
