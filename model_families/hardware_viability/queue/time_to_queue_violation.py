"""HW-QUEUE-002 — time to queue violation."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/queue/time_to_queue_violation')

import math

def compute_time_to_queue_violation(queue_backlog_items: int, queue_crit_items: int, dQ_dt_items_per_s: float) -> float:
    dQ_dt = float(dQ_dt_items_per_s)
    if dQ_dt <= 0.0:
        return math.inf
    return (int(queue_crit_items) - int(queue_backlog_items)) / dQ_dt


__all__ = ['compute_time_to_queue_violation']

_policy.bind(globals())
