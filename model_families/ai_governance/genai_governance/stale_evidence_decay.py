"""GEN-GOV-009 — stale_evidence_decay"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_governance/stale_evidence_decay')


def compute_stale_evidence_decay(age_s: float, freshness_margin_s: float, decay_power: float = _policy.default) -> float:
    if freshness_margin_s <= 0:
        raise ValueError("freshness_margin_s must be positive")
    if decay_power <= 0:
        raise ValueError("decay_power must be positive")
    freshness = max(0.0, 1.0 - max(float(age_s), 0.0) / freshness_margin_s)
    return float(freshness ** decay_power)


stale_evidence_decay = compute_stale_evidence_decay

__all__ = ['compute_stale_evidence_decay', 'stale_evidence_decay']

_policy.bind(globals())
