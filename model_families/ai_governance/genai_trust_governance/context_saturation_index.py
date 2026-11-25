"""GEN-TRUST-002 — context_saturation_index"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/genai_trust_governance/context_saturation_index')


def clamp01(value: float) -> float:
    return float(max(0.0, min(1.0, value)))


def compute_context_saturation_index(
    token_pressure_ratio: float,
    conflict_count: int,
    source_count: int,
    safe_conflict_budget: int = _policy.default,
    safe_source_budget: int = _policy.default,
) -> float:
    if safe_conflict_budget <= 0 or safe_source_budget <= 0:
        raise ValueError("safe budgets must be positive")
    token_component = clamp01(max(float(token_pressure_ratio), 0.0))
    conflict_component = clamp01(max(int(conflict_count), 0) / safe_conflict_budget)
    source_component = clamp01(max(int(source_count), 0) / safe_source_budget)
    token_weight, conflict_weight, source_weight = _policy.value("component_weights")
    return clamp01(token_weight * token_component + conflict_weight * conflict_component + source_weight * source_component)


context_saturation_index = compute_context_saturation_index

__all__ = ['compute_context_saturation_index', 'context_saturation_index']

_policy.bind(globals())
