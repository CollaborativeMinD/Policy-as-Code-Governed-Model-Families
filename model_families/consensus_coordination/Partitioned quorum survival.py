"""N1.2 — Partitioned quorum survival"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('consensus_coordination/Partitioned quorum survival')


from typing import Sequence


def compute_partitioned_quorum_survival(
    partition_authority_weights: Sequence[float],
    quorum_threshold_weight: float,
) -> float:
    """Return normalized quorum survival score."""
    if quorum_threshold_weight <= 0.0:
        raise ValueError("quorum_threshold_weight must be positive")
    if len(partition_authority_weights) == 0:
        raise ValueError("at least one partition weight is required")
    best_partition = max(float(w) for w in partition_authority_weights)
    return best_partition / float(quorum_threshold_weight) - 1.0


__all__ = ['compute_partitioned_quorum_survival']

_policy.bind(globals())
