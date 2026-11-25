"""TRACE-GOV-003 — provenance_completeness_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('provenance_governance/provenance_completeness_margin')


def compute_provenance_completeness_margin(required_fields: list[str], payload: dict[str, object]) -> int:
    if not required_fields:
        raise ValueError("required_fields must not be empty")
    present = 0
    for field in required_fields:
        if field in payload and payload[field] not in (None, "", [], {}):
            present += 1
    return int(present - len(required_fields))


provenance_completeness_margin = compute_provenance_completeness_margin

__all__ = ['compute_provenance_completeness_margin', 'provenance_completeness_margin']

_policy.bind(globals())
