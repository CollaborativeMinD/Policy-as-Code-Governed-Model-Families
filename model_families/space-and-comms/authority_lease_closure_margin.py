"""C.6a - Authority lease closure margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/authority_lease_closure_margin')


def compute_authority_lease_closure_margin(
    t_lease: float,
    t_sensor: float,
    t_transport: float,
    t_queue: float,
    t_compute: float,
    t_actuate: float,
    j_total: float,
    t_reconfig: float,
) -> float:
    """Return positive margin when authority can close before lease expiry."""
    values = {
        "t_lease": t_lease,
        "t_sensor": t_sensor,
        "t_transport": t_transport,
        "t_queue": t_queue,
        "t_compute": t_compute,
        "t_actuate": t_actuate,
        "j_total": j_total,
        "t_reconfig": t_reconfig,
    }
    if any(v < 0 for v in values.values()):
        raise ValueError("all timing inputs must be non-negative")
    return t_lease - (t_sensor + t_transport + t_queue + t_compute + t_actuate + j_total + t_reconfig)


__all__ = ['compute_authority_lease_closure_margin']

_policy.bind(globals())
