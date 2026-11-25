"""GEN-GOV-007 — deterministic_parse_yield"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_governance/deterministic_parse_yield')


def compute_deterministic_parse_yield(schema_valid_outputs: int, total_outputs: int) -> float:
    if total_outputs <= 0:
        raise ValueError("total_outputs must be positive")
    if schema_valid_outputs < 0 or schema_valid_outputs > total_outputs:
        raise ValueError("schema_valid_outputs must be between 0 and total_outputs")
    return float(schema_valid_outputs / total_outputs)


deterministic_parse_yield = compute_deterministic_parse_yield

__all__ = ['compute_deterministic_parse_yield', 'deterministic_parse_yield']

_policy.bind(globals())
