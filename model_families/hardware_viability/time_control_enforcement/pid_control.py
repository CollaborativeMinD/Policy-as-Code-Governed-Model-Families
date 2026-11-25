"""PCC-12 — Sniper's Breath, PID control law."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/pid_control')


def symbolic_expression() -> str:
    return 'kp * e + ki * integral_e + kd * derivative_e'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(e, integral_e, derivative_e, kp, ki, kd):
        return kp * e + ki * integral_e + kd * derivative_e

    return evaluate


def compute_pid_control(error: float, integral_error: float, derivative_error: float, kp: float, ki: float, kd: float) -> float:
    return float(kp * error + ki * integral_error + kd * derivative_error)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_pid_control",
]

_policy.bind(globals())
