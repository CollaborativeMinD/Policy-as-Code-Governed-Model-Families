"""PCC-02 — Reality Gap Monitor, chi-squared residual law."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('estimation_detection/chi_squared_reality_gap_monitor')


import math
from collections.abc import Sequence


def symbolic_expression() -> str:
    return '(O - E) ** 2 / E'


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(O, E):
        return (O - E) ** 2 / E

    return evaluate


def compute_chi_squared_gap(observed: Sequence[float], expected: Sequence[float]) -> float:
    if len(observed) != len(expected):
        raise ValueError("observed and expected must have equal length")
    if not observed:
        raise ValueError("observed and expected must not be empty")
    total = 0.0
    for o, e in zip(observed, expected):
        if not math.isfinite(float(e)) or float(e) <= 0.0:
            raise ValueError("expected values must be positive and finite")
        total += (float(o) - float(e)) ** 2 / float(e)
    return float(total)


__all__ = [
    "symbolic_expression",
    "lambdified",
    "compute_chi_squared_gap",
]

_policy.bind(globals())
