"""TERRAIN-TRUTH-010 — lane_aware_confidence_ceiling"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/lane_aware_confidence_ceiling')


import math


def compute_lane_aware_confidence_ceiling(c_model: float, lane: str, status: str, m_ms: float, tau: float = _policy.default) -> tuple[float, float]:
    if not 0.0 <= c_model <= 1.0:
        raise ValueError("c_model must be in [0,1]")
    lane_cap = _policy.value("local_cap") if lane == _policy.value("local_lane") else _policy.value("other_cap")
    status_factor = _policy.value("ingested_factor") if status == _policy.value("ingested_status") else _policy.value("other_factor")
    ceiling = max(0.0, min(1.0, lane_cap * status_factor * math.exp(min(m_ms, 0.0) / tau)))
    return min(c_model, ceiling), float(ceiling)


lane_aware_confidence_ceiling = compute_lane_aware_confidence_ceiling

__all__ = ['compute_lane_aware_confidence_ceiling', 'lane_aware_confidence_ceiling']

_policy.bind(globals())
