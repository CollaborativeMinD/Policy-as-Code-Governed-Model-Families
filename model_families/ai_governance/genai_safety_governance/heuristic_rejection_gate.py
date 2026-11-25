"""GEN-SAFE-003 — heuristic_rejection_gate"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_safety_governance/heuristic_rejection_gate')


from collections.abc import Sequence, Mapping


def compute_heuristic_rejection_gate(
    active_margins: Mapping[str, float],
    active_death_states: Sequence[str],
    evidence_coverage_ratio_value: float,
    parse_yield: float,
    freshness_score: float,
    contradiction_score: float,
    semantic_alias_drift_score: float,
    unbound_truth_penalty: float,
    *,
    min_ecr: float = _policy.default,
    min_parse_yield: float = _policy.default,
    min_freshness: float = _policy.default,
    max_contradiction: float = _policy.default,
    max_semantic_alias: float = _policy.default,
    max_unbound_truth: float = _policy.default,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if any(float(v) <= 0.0 for v in active_margins.values()):
        bad = [k for k, v in active_margins.items() if float(v) <= 0.0]
        reasons.append(f"negative_or_zero_active_margin:{','.join(sorted(bad))}")
    if any(str(s).strip() for s in active_death_states):
        reasons.append("active_death_state_present")
    if evidence_coverage_ratio_value < min_ecr:
        reasons.append("evidence_coverage_below_threshold")
    if parse_yield < min_parse_yield:
        reasons.append("parse_yield_below_threshold")
    if freshness_score < min_freshness:
        reasons.append("freshness_below_threshold")
    if contradiction_score > max_contradiction:
        reasons.append("contradiction_detected")
    if semantic_alias_drift_score > max_semantic_alias:
        reasons.append("semantic_alias_drift_detected")
    if unbound_truth_penalty > max_unbound_truth:
        reasons.append("unbound_truth_intrusion_detected")
    return (len(reasons) == 0, reasons)


heuristic_rejection_gate = compute_heuristic_rejection_gate

__all__ = ['compute_heuristic_rejection_gate', 'heuristic_rejection_gate']

_policy.bind(globals())
