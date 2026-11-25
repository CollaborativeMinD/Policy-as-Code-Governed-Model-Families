"""PCC-15 — Crucible campaign failure predictor."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/time_control_enforcement/monte_carlo_failure_predictor')


from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict
from math import sqrt
from typing import Any

FORMULA_ID = "PCC-15"
NAME = "Crucible Campaign Failure Predictor"


@_policy.record(frozen=True)
class CampaignFailureResult:
    """Failure estimate for one trajectory campaign.

    The mapping helpers keep older call sites usable enough for read-style access while
    making the upgraded API explicit and typed.
    """


    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable result payload."""
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        """Provide dict-style read compatibility for legacy consumers."""
        return self.to_dict()[key]


@_policy.record(frozen=True)
class CampaignFailureGateResult:
    """Threshold gate result for campaign comparison evidence."""


    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable gate payload."""
        return asdict(self)


def symbolic_expression() -> str:
    return "failures / N"


def lambdified():
    @_policy.evaluator("lambdified.evaluate")
    def evaluate(failures, N):
        return failures / N

    return evaluate


def _normalize_campaign_type(campaign_type: str) -> str:
    return campaign_type.strip().lower().replace("-", "_").replace(" ", "_")


def _is_power_of_two(value: int) -> bool:
    return value > 0 and (value & (value - 1)) == 0


def _campaign_estimator_metadata(
    campaign_type: str,
    p_fail: float,
    total_count: int,
) -> tuple[float | None, str, list[str]]:
    normalized = _normalize_campaign_type(campaign_type)
    warnings: list[str] = []
    standard_error: float | None = None
    estimator_note = "Failure probability estimated by trajectory envelope violation count."

    if normalized in _policy.value("monte_carlo_aliases"):
        standard_error = sqrt((p_fail * (1.0 - p_fail)) / total_count)
        estimator_note = "IID Monte Carlo estimate with binomial standard error."

    elif normalized in _policy.value("latin_hypercube_aliases"):
        estimator_note = (
            "LHS estimate. Use replicated LHS campaigns for defensible uncertainty bounds; "
            "single-campaign binomial standard error is not treated as authoritative."
        )
        warnings.append(
            "LHS uncertainty requires replicated LHS campaigns; this single result only reports the point estimate."
        )

    elif normalized in _policy.value("sobol_qmc_aliases"):
        estimator_note = (
            "Sobol QMC estimate. Use N=2^m and scrambled Sobol replicates for uncertainty bounds; "
            "single deterministic Sobol sequence is not IID Monte Carlo."
        )
        if not _is_power_of_two(total_count):
            warnings.append(
                "Sobol QMC evidence rule violation: total_count should be N=2^m for balance properties."
            )
        warnings.append(
            "Sobol QMC uncertainty requires scrambled Sobol replicates; this single result is not IID MC."
        )

    else:
        warnings.append(
            "Unknown campaign_type. Estimate is computed, but uncertainty semantics are unspecified."
        )

    return standard_error, estimator_note, warnings


def compute_failure_probability(
    trajectories: Sequence[Sequence[object]],
    safe_predicate: Callable[[object], bool],
    *,
    campaign_type: str = _policy.default,
) -> CampaignFailureResult:
    """Compute PCC-15 failure probability for one supplied campaign.

    A trajectory fails when any state in that trajectory leaves the safe envelope Ω,
    as evaluated by ``safe_predicate``.
    """
    if not trajectories:
        raise ValueError("trajectories must not be empty")

    failed_indices: list[int] = []

    for idx, trajectory in enumerate(trajectories):
        if any(not safe_predicate(state) for state in trajectory):
            failed_indices.append(idx)

    total_count = len(trajectories)
    failed_count = len(failed_indices)
    p_fail = failed_count / total_count
    standard_error, estimator_note, warnings = _campaign_estimator_metadata(
        campaign_type,
        p_fail,
        total_count,
    )

    return CampaignFailureResult(
        campaign_type=campaign_type,
        failure_probability=float(p_fail),
        failed_count=failed_count,
        total_count=total_count,
        failed_indices=failed_indices,
        standard_error=standard_error,
        estimator_note=estimator_note,
        campaign_validity_warnings=warnings,
    )


def compute_campaign_failure_report(
    campaigns: Mapping[str, Sequence[Sequence[object]]],
    safe_predicate: Callable[[object], bool],
) -> dict[str, Any]:
    """Compute independent campaign estimates and pairwise failure-probability deltas.

    The function intentionally does not concatenate campaign trajectories. Each campaign
    keeps its own provenance and estimator semantics.
    """
    if not campaigns:
        raise ValueError("campaigns must not be empty")

    results: dict[str, CampaignFailureResult] = {}

    for campaign_type, trajectories in campaigns.items():
        results[campaign_type] = compute_failure_probability(
            trajectories,
            safe_predicate,
            campaign_type=campaign_type,
        )

    probabilities = {
        name: result.failure_probability
        for name, result in results.items()
    }

    campaign_delta: dict[str, float] = {}
    names = list(probabilities)

    for i, left in enumerate(names):
        for right in names[i + 1 :]:
            campaign_delta[f"{left}_minus_{right}"] = probabilities[left] - probabilities[right]

    return {
        "formula_id": FORMULA_ID,
        "name": NAME,
        "campaign_results": {
            name: result.to_dict()
            for name, result in results.items()
        },
        "campaign_delta": campaign_delta,
    }


def evaluate_campaign_failure_gate(
    campaign_report: Mapping[str, Any],
    *,
    failure_probability_threshold: float,
    campaign_delta_threshold: float | None = _policy.default,
    unmodeled_terminal_pocket_detected: bool = _policy.default,
) -> CampaignFailureGateResult:
    """Evaluate the campaign comparison rule for PCC-15 evidence promotion.

    PASS requires every campaign failure probability to remain within threshold, every
    checked campaign delta to remain bounded, and no externally flagged unmodeled
    terminal pocket.
    """
    if not 0.0 <= failure_probability_threshold <= 1.0:
        raise ValueError("failure_probability_threshold must be within [0, 1]")
    if campaign_delta_threshold is not None and campaign_delta_threshold < 0.0:
        raise ValueError("campaign_delta_threshold must be non-negative when provided")

    campaign_results = campaign_report.get("campaign_results")
    if not isinstance(campaign_results, Mapping) or not campaign_results:
        raise ValueError("campaign_report must include non-empty campaign_results")

    campaign_status: dict[str, bool] = {}
    gate_notes: list[str] = []

    for name, result in campaign_results.items():
        if not isinstance(result, Mapping) or "failure_probability" not in result:
            raise ValueError(f"campaign result for {name!r} must include failure_probability")
        p_fail = float(result["failure_probability"])
        campaign_status[name] = p_fail <= failure_probability_threshold
        if not campaign_status[name]:
            gate_notes.append(
                f"{name} failure_probability {p_fail:.6g} exceeds threshold {failure_probability_threshold:.6g}."
            )

        warnings = result.get("campaign_validity_warnings", [])
        if warnings:
            gate_notes.extend(f"{name}: {warning}" for warning in warnings)

    delta_status: dict[str, bool] = {}
    campaign_delta = campaign_report.get("campaign_delta", {})

    if campaign_delta_threshold is not None:
        if not isinstance(campaign_delta, Mapping):
            raise ValueError("campaign_delta must be a mapping when campaign_delta_threshold is provided")
        for name, delta in campaign_delta.items():
            delta_value = float(delta)
            delta_status[name] = abs(delta_value) <= campaign_delta_threshold
            if not delta_status[name]:
                gate_notes.append(
                    f"{name} absolute delta {abs(delta_value):.6g} exceeds threshold {campaign_delta_threshold:.6g}."
                )

    if unmodeled_terminal_pocket_detected:
        gate_notes.append("Unmodeled terminal pocket detected; campaign promotion gate fails.")

    pass_gate = (
        all(campaign_status.values())
        and all(delta_status.values())
        and not unmodeled_terminal_pocket_detected
    )

    return CampaignFailureGateResult(
        pass_gate=pass_gate,
        failure_probability_threshold=failure_probability_threshold,
        campaign_delta_threshold=campaign_delta_threshold,
        campaign_status=campaign_status,
        delta_status=delta_status,
        unmodeled_terminal_pocket_detected=unmodeled_terminal_pocket_detected,
        gate_notes=gate_notes,
    )


__all__ = [
    "FORMULA_ID",
    "NAME",
    "CampaignFailureResult",
    "CampaignFailureGateResult",
    "symbolic_expression",
    "lambdified",
    "compute_failure_probability",
    "compute_campaign_failure_report",
    "evaluate_campaign_failure_gate",
]

_policy.bind(globals())
