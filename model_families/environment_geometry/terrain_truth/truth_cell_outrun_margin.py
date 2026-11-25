"""ET-001 - truth_cell_outrun_margin"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('environment_geometry/terrain_truth/truth_cell_outrun_margin')


from math import isfinite


def compute_truth_cell_outrun_margin(
    truth_cell_scale_m: float,
    relative_speed_m_s: float,
    total_age_s: float,
) -> float:
    L = float(truth_cell_scale_m)
    v = float(relative_speed_m_s)
    tau = float(total_age_s)

    if not all(isfinite(x) for x in (L, v, tau)):
        raise ValueError("inputs must be finite")
    if L < 0 or v < 0 or tau < 0:
        raise ValueError("all inputs must be non-negative")

    return L - v * tau


__all__ = ['compute_truth_cell_outrun_margin']

_policy.bind(globals())
