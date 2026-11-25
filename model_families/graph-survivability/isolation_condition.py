"""M2.4 — Isolation timing condition"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('graph-survivability/isolation_condition')


def check_isolation_condition(time_to_isolate: float, tau_isolate: float) -> bool:
    """Evaluate the isolation timing condition.

    Parameters
    ----------
    time_to_isolate : float
        Time taken to isolate the failing node ``v`` (seconds).
    tau_isolate : float
        Maximum permissible isolation time (seconds).

    Returns
    -------
    bool
        ``True`` if ``time_to_isolate ≤ tau_isolate``; ``False`` otherwise.
    """
    return time_to_isolate <= tau_isolate


__all__ = ['check_isolation_condition']

_policy.bind(globals())
