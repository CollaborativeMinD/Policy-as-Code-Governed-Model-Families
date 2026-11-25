"""TERRAIN-TRUTH-009 — multiscale_disagreement_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/multiscale_disagreement_margin')


from collections.abc import Sequence
import math


def compute_multiscale_disagreement_margin(f_local: Sequence[float], f_regional: Sequence[float], tau_ms: float = _policy.default) -> float:
    if len(f_local) != len(f_regional):
        raise ValueError("feature vectors must be the same length")
    if len(f_local) == 0:
        raise ValueError("feature vectors must not be empty")
    default_weights = _policy.value("feature_weights")
    weights = default_weights[: len(f_local)]
    if len(weights) < len(f_local):
        weights.extend([_policy.value("additional_feature_weight")] * (len(f_local) - len(weights)))
    divergence_sq = sum(float(w) * (float(a) - float(b)) ** 2 for a, b, w in zip(f_local, f_regional, weights))
    divergence = math.sqrt(max(divergence_sq, 0.0))
    return float(float(tau_ms) - divergence)


multiscale_disagreement_margin = compute_multiscale_disagreement_margin

__all__ = ['compute_multiscale_disagreement_margin', 'multiscale_disagreement_margin']

_policy.bind(globals())
