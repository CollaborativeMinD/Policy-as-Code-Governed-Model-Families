"""C.6b - Sensor-to-actuator delay budget margin."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('space-and-comms/sensor_actuator_delay_budget')


def compute_sensor_to_actuator_delay_budget_margin(
    t_budget: float,
    t_sample_hold: float,
    t_transport: float,
    t_queue: float,
    t_compute: float,
    t_driver: float,
    t_actuate: float,
    j_total: float,
) -> float:
    """Return positive margin when the loop closes within the allowed budget."""
    values = {
        "t_budget": t_budget,
        "t_sample_hold": t_sample_hold,
        "t_transport": t_transport,
        "t_queue": t_queue,
        "t_compute": t_compute,
        "t_driver": t_driver,
        "t_actuate": t_actuate,
        "j_total": j_total,
    }
    if any(v < 0 for v in values.values()):
        raise ValueError("all timing inputs must be non-negative")
    return t_budget - (t_sample_hold + t_transport + t_queue + t_compute + t_driver + t_actuate + j_total)


__all__ = ['compute_sensor_to_actuator_delay_budget_margin']

_policy.bind(globals())
