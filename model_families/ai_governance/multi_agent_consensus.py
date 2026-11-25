"""M9.3 — Multi‑agent consensus gate"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/multi_agent_consensus')


from typing import Callable, Sequence


def consensus_gate(scores: Sequence[float], alpha: float, score_fn: Callable[[Sequence[float]], float] | None = _policy.default) -> bool:
    """Compute the consensus gate over agent scores.

    Parameters
    ----------
    scores : Sequence[float]
        Scores from individual agents.
    alpha : float
        Threshold for acceptance.
    score_fn : Callable, optional
        Aggregation function to combine scores.  Defaults to the mean.

    Returns
    -------
    bool
        ``True`` if the aggregated score ≥ alpha; ``False`` otherwise.
    """
    if not scores:
        raise ValueError("scores must be non‑empty")
    fn = score_fn if score_fn is not None else (lambda xs: sum(xs) / len(xs))
    aggregated = fn(scores)
    return aggregated >= alpha


__all__ = ['consensus_gate']

_policy.bind(globals())
