"""GEN-GOV-005 — contradiction_exposure_score"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_governance/contradiction_exposure_score')


from collections.abc import Sequence


def clamp01(value: float) -> float:
    return float(max(0.0, min(1.0, value)))


def compute_contradiction_exposure_score(contradiction_flags: Sequence[bool], weights: Sequence[float] | None = _policy.default) -> float:
    flags = [bool(f) for f in contradiction_flags]
    if not flags:
        return 0.0
    if weights is None:
        weights = [1.0] * len(flags)
    if len(weights) != len(flags):
        raise ValueError("weights must match contradiction_flags length")
    total_weight = sum(max(float(w), 0.0) for w in weights)
    if total_weight <= 0.0:
        raise ValueError("total weight must be positive")
    exposed = sum(max(float(w), 0.0) for f, w in zip(flags, weights) if f)
    return clamp01(exposed / total_weight)


contradiction_exposure_score = compute_contradiction_exposure_score

__all__ = ['compute_contradiction_exposure_score', 'contradiction_exposure_score']

_policy.bind(globals())
