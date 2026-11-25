"""T1.2 — Mixed-stream temporal coherence score"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/timing_validity/mixed_stream_temporal_coherence')


from typing import Sequence


def compute_mixed_stream_temporal_coherence_score(
    timestamps: Sequence[float],
    max_skew: float,
    sequence_gap_penalty: float = _policy.default,
) -> float:
    if not timestamps:
        raise ValueError("timestamps cannot be empty")
    if max_skew <= 0:
        raise ValueError("max_skew must be positive")
    skew = max(timestamps) - min(timestamps)
    score = 1.0 - (skew / max_skew) - sequence_gap_penalty
    return float(max(0.0, min(1.0, score)))

__all__ = ['compute_mixed_stream_temporal_coherence_score']

_policy.bind(globals())
