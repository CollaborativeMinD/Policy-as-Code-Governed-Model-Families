"""T1.3 — Sequence/replay integrity law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/timing_validity/sequence_replay_integrity')


def compute_sequence_replay_integrity_score(
    seq_prev: int,
    seq_curr: int,
    time_prev: float,
    time_curr: float,
    hash_prev: str,
    hash_curr: str,
    allow_duplicate_hash: bool = _policy.default,
) -> int:
    score = 0
    if seq_curr <= seq_prev:
        score += 1
    if time_curr <= time_prev:
        score += 1
    if (hash_curr == hash_prev) and (seq_curr != seq_prev) and not allow_duplicate_hash:
        score += 1
    return int(score)

__all__ = ['compute_sequence_replay_integrity_score']

_policy.bind(globals())
