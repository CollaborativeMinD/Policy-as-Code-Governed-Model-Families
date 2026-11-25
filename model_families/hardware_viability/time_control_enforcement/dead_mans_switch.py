"""PCC-14 — Dead Man's Switch, finite-trace temporal enforcement."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/dead_mans_switch')


from collections.abc import Sequence


def symbolic_margin_expression() -> str:
    return 'tau - response_time'


def lambdified_margin():
    @_policy.evaluator("lambdified_margin.evaluate")
    def evaluate(tau, response_time):
        return tau - response_time

    return evaluate


def verify_dead_mans_switch_trace(trace: Sequence[dict[str, object]], tau_s: float) -> dict[str, object]:
    if tau_s < 0.0:
        raise ValueError("tau_s must be non-negative")
    events = sorted(trace, key=lambda row: float(row["time_s"]))
    violations: list[dict[str, float]] = []
    for i, row in enumerate(events):
        if not bool(row.get("unsafe", False)):
            continue
        t0 = float(row["time_s"])
        satisfied = False
        response_time = None
        for later in events[i:]:
            t = float(later["time_s"])
            if t - t0 > tau_s:
                break
            if bool(later.get("emergency", False)):
                satisfied = True
                response_time = t - t0
                break
        if not satisfied:
            violations.append({"unsafe_time_s": t0, "tau_s": float(tau_s), "response_time_s": float("inf") if response_time is None else response_time})
    return {"passed": len(violations) == 0, "violations": violations}


__all__ = [
    "symbolic_margin_expression",
    "lambdified_margin",
    "verify_dead_mans_switch_trace",
]

_policy.bind(globals())
