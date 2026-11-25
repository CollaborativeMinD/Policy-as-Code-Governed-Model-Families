"""HW-GOV-003 — predictive hardware viability state."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/predictive_hardware_viability_state')

from typing import Optional

@_policy.record(frozen=True)
class HardwareViabilityState:
    pass


def compute_predictive_hardware_viability_state(
    thermal_margin_c: float,
    memory_margin_pct: float,
    queue_margin_items: float,
    minimum_terminal_horizon_s: float,
    converging_terminal_pressure: float,
    dominant_driver: Optional[str],
    critical_horizon_s: float = _policy.default,
    degraded_thermal_margin_c: float = _policy.default,
    degraded_memory_margin_pct: float = _policy.default,
    degraded_queue_margin_items: float = _policy.default,
    degraded_pressure_floor: float = _policy.default,
) -> HardwareViabilityState:
    m_t = float(thermal_margin_c); m_m = float(memory_margin_pct); m_q = float(queue_margin_items)
    h_min = float(minimum_terminal_horizon_s); p_term = float(converging_terminal_pressure)
    if m_t <= 0.0 or m_m <= 0.0 or m_q <= 0.0:
        status='FATAL_BREACH'
    elif h_min <= float(critical_horizon_s):
        status='SAFETY_CRITICAL'
    elif (
        m_t <= float(degraded_thermal_margin_c)
        or m_m <= float(degraded_memory_margin_pct)
        or m_q <= float(degraded_queue_margin_items)
        or p_term >= float(degraded_pressure_floor)
    ):
        status='DEGRADED'
    else:
        status='NOMINAL'
    return HardwareViabilityState(
        status=status,
        dominant_driver=dominant_driver,
        minimum_terminal_horizon_s=h_min,
        thermal_margin_c=m_t,
        memory_margin_pct=m_m,
        queue_margin_items=m_q,
        converging_terminal_pressure=p_term,
    )


__all__ = ['HardwareViabilityState', 'compute_predictive_hardware_viability_state']

_policy.bind(globals())
