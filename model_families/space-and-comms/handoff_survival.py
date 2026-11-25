"""C.6 — Handoff survival condition"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/handoff_survival')


def check_handoff_survival(t_handoff: float, t_coast_limit: float) -> bool:
    """Check if the handoff occurs before the coast limit.

    Returns ``True`` if ``t_handoff < t_coast_limit``.
    """
    return t_handoff < t_coast_limit


__all__ = ['check_handoff_survival']

_policy.bind(globals())
