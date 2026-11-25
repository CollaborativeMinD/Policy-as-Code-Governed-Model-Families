"""HW-QUEUE-001 — queue margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/queue/queue_margin')


def compute_queue_margin(queue_backlog_items: int, queue_crit_items: int) -> int:
    return int(queue_crit_items) - int(queue_backlog_items)


__all__ = ['compute_queue_margin']

_policy.bind(globals())
