"""PCC-18 — Pavlovian Reflex Gate, discrete state transition."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/pavlovian_reflex_state_machine')


from collections.abc import Mapping


def symbolic_gate_expression() -> str:
    return 'g - theta'


def lambdified_gate_margin():
    @_policy.evaluator("lambdified_gate_margin.evaluate")
    def evaluate(g, theta):
        return g - theta

    return evaluate


def compute_reflex_gate(guard_value: float, threshold: float) -> bool:
    return bool(float(guard_value) >= float(threshold))


def compute_next_state(
    current_state: str,
    guard_value: float,
    threshold: float,
    event: str,
    transitions: Mapping[tuple[str, str], str],
) -> str:
    if not compute_reflex_gate(guard_value, threshold):
        return str(current_state)
    key = (str(current_state), str(event))
    if key not in transitions:
        raise KeyError(f"missing transition for {key}")
    return str(transitions[key])


__all__ = [
    "symbolic_gate_expression",
    "lambdified_gate_margin",
    "compute_reflex_gate",
    "compute_next_state",
]

_policy.bind(globals())
