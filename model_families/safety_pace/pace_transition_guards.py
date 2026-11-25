"""M1.3 — PACE transition guards"""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('safety_pace/pace_transition_guards')


from typing import Sequence


def compute_pace_transition(margins: Sequence[float], current_state: str) -> str:
    """Determine the next PACE state based on safety margins.

    Parameters
    ----------
    margins : Sequence[float]
        A sequence of margin values m_i ∈ ℝ.  Lower values indicate
        proximity to failure.
    current_state : str
        The current PACE mode ('P', 'A', 'C', or 'E').

    Returns
    -------
    str
        The next PACE mode according to the transition rules.  If
        already in 'E' (Execute) or if no transition condition is
        satisfied, returns ``current_state``.

    Raises
    ------
    ValueError
        If ``current_state`` is not a valid mode.
    """
    # If already in Execute mode, stay there.
    if current_state == "E":
        return current_state
    # Determine the minimum margin
    min_margin = min(margins) if margins else 1.0
    # Evaluate transition conditions in order of severity
    if current_state == "C" and min_margin <= _policy.value("contingency_margin"):
        return "E"
    if current_state == "A" and min_margin <= _policy.value("alternate_margin"):
        return "C"
    if current_state == "P" and min_margin <= _policy.value("primary_margin"):
        return "A"
    return current_state


__all__ = ['compute_pace_transition']

_policy.bind(globals())
