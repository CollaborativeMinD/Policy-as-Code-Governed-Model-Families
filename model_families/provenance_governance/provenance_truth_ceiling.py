"""G1.1 — Provenance truth ceiling law"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('provenance_governance/provenance_truth_ceiling')


def compute_provenance_truth_ceiling(
    source_ceiling: float,
    lineage_completeness: float,
    contract_validity: float,
    temporal_validity: float,
    semantic_alignment: float,
) -> float:
    vals = [source_ceiling, lineage_completeness, contract_validity, temporal_validity, semantic_alignment]
    vals = [max(0.0, min(1.0, float(v))) for v in vals]
    return float(min(vals))

__all__ = ['compute_provenance_truth_ceiling']

_policy.bind(globals())
