"""GEN-GOV-004 — evidence_coverage_ratio"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_governance/evidence_coverage_ratio')


from collections.abc import Sequence


def compute_evidence_coverage_ratio(required_refs: Sequence[str], cited_refs: Sequence[str]) -> float:
    required = {str(r) for r in required_refs if str(r)}
    cited = {str(r) for r in cited_refs if str(r)}
    if not required:
        return 1.0
    return float(len(required & cited) / len(required))


evidence_coverage_ratio = compute_evidence_coverage_ratio

__all__ = ['compute_evidence_coverage_ratio', 'evidence_coverage_ratio']

_policy.bind(globals())
