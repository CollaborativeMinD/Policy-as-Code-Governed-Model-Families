"""M9.4 — Penalized prompt objective"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/penalized_prompt')


from typing import Tuple


def compute_penalized_objective(
    U_p: float,
    E_halluc: float,
    E_phys: float,
    E_schema: float,
    lambdas: Tuple[float, float, float],
) -> float:
    """Compute the penalized prompt objective.

    Parameters
    ----------
    U_p : float
        Utility of the prompt.
    E_halluc : float
        Hallucination penalty.
    E_phys : float
        Physical infeasibility penalty.
    E_schema : float
        Schema violation penalty.
    lambdas : Tuple[float, float, float]
        Penalty weights ``(λ₁, λ₂, λ₃)``.

    Returns
    -------
    float
        The penalized objective value ``J(p)``.
    """
    lam1, lam2, lam3 = lambdas
    return U_p - lam1 * E_halluc - lam2 * E_phys - lam3 * E_schema


__all__ = ['compute_penalized_objective']

_policy.bind(globals())
