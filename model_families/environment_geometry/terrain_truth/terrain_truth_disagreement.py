"""E1.1 — Terrain truth disagreement index"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/terrain_truth_disagreement')


def compute_terrain_truth_disagreement_index(
    elevation_delta_rms: float,
    slope_delta_rms: float,
    hazard_probability_delta: float,
    lineage_completeness: float,
    elevation_ref: float,
    slope_ref: float,
    weights: tuple[float, float, float, float] = _policy.default,
) -> float:
    wh, ws, wp, wl = weights
    return float(
        wh * abs(elevation_delta_rms) / max(elevation_ref, _policy.value("denominator_floor"))
        + ws * abs(slope_delta_rms) / max(slope_ref, _policy.value("denominator_floor"))
        + wp * abs(hazard_probability_delta)
        + wl * (1.0 - max(0.0, min(1.0, lineage_completeness)))
    )

__all__ = ['compute_terrain_truth_disagreement_index']

_policy.bind(globals())
