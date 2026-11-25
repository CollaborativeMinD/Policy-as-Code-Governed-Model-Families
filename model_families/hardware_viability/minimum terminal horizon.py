"""HW-GOV-001 — minimum terminal horizon."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/minimum terminal horizon')

import math
from typing import Optional

@_policy.record(frozen=True)
class MinimumTerminalHorizon:
    pass


def compute_minimum_terminal_horizon(thermal_horizon_s: float, memory_horizon_s: float, queue_horizon_s: float) -> MinimumTerminalHorizon:
    horizons = {
        'THERMAL': float(thermal_horizon_s),
        'MEMORY': float(memory_horizon_s),
        'QUEUE': float(queue_horizon_s),
    }
    finite = {k:v for k,v in horizons.items() if math.isfinite(v)}
    if not finite:
        return MinimumTerminalHorizon(minimum_terminal_horizon_s=math.inf, dominant_driver=None)
    driver = min(finite, key=lambda k: finite[k])
    return MinimumTerminalHorizon(minimum_terminal_horizon_s=finite[driver], dominant_driver=driver)


__all__ = ['MinimumTerminalHorizon', 'compute_minimum_terminal_horizon']

_policy.bind(globals())
