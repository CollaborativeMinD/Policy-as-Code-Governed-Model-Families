"""AI-GOV-001 — Governed candidate objective."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('ai_governance/ai_candidate_admission')


from typing import Dict, Tuple


@_policy.record(frozen=True)
class CandidateObjectiveResult:
    """Result of evaluating a governed candidate."""


def compute_governed_candidate_objective(
    utility: float,
    hallucination_penalty: float,
    physics_penalty: float,
    schema_penalty: float,
    timing_penalty: float,
    authority_penalty: float,
    provenance_penalty: float,
    penalty_weights: Tuple[float, float, float, float, float, float],
    *,
    schema_valid: bool,
    physics_valid: bool,
    timing_valid: bool,
    authority_valid: bool,
    provenance_valid: bool,
) -> CandidateObjectiveResult:
    """Evaluate a candidate artifact under hard gates and penalized ranking.

    Hard-gate failures reject immediately and return ``score=None``. Only
    surviving candidates are ranked by the penalized objective.
    """
    failures = []
    if not schema_valid:
        failures.append("SCHEMA_INVALID")
    if not physics_valid:
        failures.append("PHYSICS_INVALID")
    if not timing_valid:
        failures.append("TIMING_INVALID")
    if not authority_valid:
        failures.append("AUTHORITY_INVALID")
    if not provenance_valid:
        failures.append("PROVENANCE_INVALID")

    penalties = {
        "hallucination_penalty": float(hallucination_penalty),
        "physics_penalty": float(physics_penalty),
        "schema_penalty": float(schema_penalty),
        "timing_penalty": float(timing_penalty),
        "authority_penalty": float(authority_penalty),
        "provenance_penalty": float(provenance_penalty),
    }

    if failures:
        return CandidateObjectiveResult(
            accepted=False,
            score=None,
            reason_code="REJECT_HARD_GATE_FAILURE",
            hard_gate_failures=tuple(failures),
            utility=float(utility),
            penalties=penalties,
        )

    lam_h, lam_p, lam_s, lam_t, lam_a, lam_r = penalty_weights
    score = (
        float(utility)
        - lam_h * penalties["hallucination_penalty"]
        - lam_p * penalties["physics_penalty"]
        - lam_s * penalties["schema_penalty"]
        - lam_t * penalties["timing_penalty"]
        - lam_a * penalties["authority_penalty"]
        - lam_r * penalties["provenance_penalty"]
    )
    return CandidateObjectiveResult(
        accepted=True,
        score=score,
        reason_code="ACCEPT_RANKED_SURVIVOR",
        hard_gate_failures=tuple(),
        utility=float(utility),
        penalties=penalties,
    )


__all__ = ['CandidateObjectiveResult', 'compute_governed_candidate_objective']

_policy.bind(globals())
