"""Cross-domain EE models for digital_twin_ssot."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('hardware_viability/electrical/electrical_survivability_margins')


from typing import Mapping, Sequence


def _clip(value: float, lower: float, upper: float) -> float:
    if lower > upper:
        raise ValueError("lower must be <= upper")
    return max(lower, min(value, upper))


def _require_nonnegative(name: str, value: float) -> None:
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative, got {value!r}")


def _require_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0, got {value!r}")


def compute_effective_brownout_margin(
    v_min_measured_v: float,
    v_uvlo_v: float,
    v_ripple_pk_v: float,
    v_predicted_droop_v: float,
    v_reference_uncertainty_v: float,
) -> float:
    for name, value in {
        "v_ripple_pk_v": v_ripple_pk_v,
        "v_predicted_droop_v": v_predicted_droop_v,
        "v_reference_uncertainty_v": v_reference_uncertainty_v,
    }.items():
        _require_nonnegative(name, value)
    return float(v_min_measured_v - (v_uvlo_v + v_ripple_pk_v + v_predicted_droop_v + v_reference_uncertainty_v))


def compute_thermal_derated_power_margin(
    p_nominal_w: float,
    t_junction_c: float,
    t_warn_c: float,
    t_shutdown_c: float,
    aging_factor: float,
    p_load_w: float,
    p_transient_reserve_w: float,
) -> float:
    if t_shutdown_c <= t_warn_c:
        raise ValueError("t_shutdown_c must be > t_warn_c")
    if not (0.0 < aging_factor <= 1.0):
        raise ValueError("aging_factor must lie in (0, 1]")
    _require_nonnegative("p_nominal_w", p_nominal_w)
    _require_nonnegative("p_load_w", p_load_w)
    _require_nonnegative("p_transient_reserve_w", p_transient_reserve_w)
    d_t = _clip((t_shutdown_c - t_junction_c) / (t_shutdown_c - t_warn_c), 0.0, 1.0)
    p_allow = p_nominal_w * d_t * aging_factor
    return float(p_allow - (p_load_w + p_transient_reserve_w))


def compute_recovery_energy_margin(
    e_available_j: float,
    e_restart_j: float,
    e_reacquire_j: float,
    e_isolate_j: float,
    e_safe_reserve_j: float,
) -> float:
    for name, value in {
        "e_available_j": e_available_j,
        "e_restart_j": e_restart_j,
        "e_reacquire_j": e_reacquire_j,
        "e_isolate_j": e_isolate_j,
        "e_safe_reserve_j": e_safe_reserve_j,
    }.items():
        _require_nonnegative(name, value)
    return float(e_available_j - (e_restart_j + e_reacquire_j + e_isolate_j + e_safe_reserve_j))


def compute_bus_clear_time_margin(
    tau_clear_s: float,
    n_clock_pulses: int,
    f_clear_hz: float,
    t_buffer_s: float,
    t_slave_release_s: float,
    t_reprobe_s: float,
) -> float:
    _require_positive("tau_clear_s", tau_clear_s)
    if n_clock_pulses < 0:
        raise ValueError("n_clock_pulses must be nonnegative")
    _require_positive("f_clear_hz", f_clear_hz)
    for name, value in {
        "t_buffer_s": t_buffer_s,
        "t_slave_release_s": t_slave_release_s,
        "t_reprobe_s": t_reprobe_s,
    }.items():
        _require_nonnegative(name, value)
    t_clear = (n_clock_pulses / f_clear_hz) + t_buffer_s + t_slave_release_s + t_reprobe_s
    return float(tau_clear_s - t_clear)


def compute_segment_isolation_margin(
    t_fault_spread_s: float,
    t_detect_s: float,
    t_gate_s: float,
    t_switch_s: float,
    t_quarantine_confirm_s: float,
) -> float:
    _require_nonnegative("t_fault_spread_s", t_fault_spread_s)
    for name, value in {
        "t_detect_s": t_detect_s,
        "t_gate_s": t_gate_s,
        "t_switch_s": t_switch_s,
        "t_quarantine_confirm_s": t_quarantine_confirm_s,
    }.items():
        _require_nonnegative(name, value)
    return float(t_fault_spread_s - (t_detect_s + t_gate_s + t_switch_s + t_quarantine_confirm_s))


def compute_post_recovery_reacquisition_margin(
    tau_data_valid_s: float,
    t_sample_age_s: float,
    t_recovery_s: float,
    t_reacquire_s: float,
    t_skew_s: float,
) -> float:
    _require_positive("tau_data_valid_s", tau_data_valid_s)
    for name, value in {
        "t_sample_age_s": t_sample_age_s,
        "t_recovery_s": t_recovery_s,
        "t_reacquire_s": t_reacquire_s,
        "t_skew_s": t_skew_s,
    }.items():
        _require_nonnegative(name, value)
    return float(tau_data_valid_s - (t_sample_age_s + t_recovery_s + t_reacquire_s + t_skew_s))


def compute_telemetry_use_freshness_margin(
    tau_use_s: float,
    t_now_s: float,
    t_sample_s: float,
    t_transport_s: float,
    t_clock_uncertainty_s: float,
) -> float:
    _require_positive("tau_use_s", tau_use_s)
    _require_nonnegative("t_transport_s", t_transport_s)
    _require_nonnegative("t_clock_uncertainty_s", t_clock_uncertainty_s)
    if t_now_s < t_sample_s:
        raise ValueError("t_now_s must be >= t_sample_s")
    return float(tau_use_s - ((t_now_s - t_sample_s) + t_transport_s + t_clock_uncertainty_s))


def compute_mixed_stream_coherence_margin(
    tau_align_s: float,
    timestamps_s: Sequence[float],
    path_delays_s: Sequence[float] | None = _policy.default,
) -> float:
    _require_positive("tau_align_s", tau_align_s)
    if len(timestamps_s) == 0:
        raise ValueError("timestamps_s must be non-empty")
    if path_delays_s is None:
        path_delays_s = [0.0] * len(timestamps_s)
    if len(path_delays_s) != len(timestamps_s):
        raise ValueError("path_delays_s length must match timestamps_s length")
    corrected = []
    for idx, (ts, delay) in enumerate(zip(timestamps_s, path_delays_s)):
        _require_nonnegative(f"path_delays_s[{idx}]", float(delay))
        corrected.append(float(ts) - float(delay))
    max_sep = 0.0
    for i in range(len(corrected)):
        for j in range(i + 1, len(corrected)):
            max_sep = max(max_sep, abs(corrected[i] - corrected[j]))
    return float(tau_align_s - max_sep)


def compute_boot_epoch_sequence_gate(
    boot_epoch_id: str,
    attested_boot_epoch_id: str,
    seq_prev: int,
    seq_curr: int,
    t_prev_s: float,
    t_curr_s: float,
    rollback_tolerance_s: float,
) -> bool:
    if seq_prev < 0 or seq_curr < 0:
        raise ValueError("sequence values must be nonnegative")
    _require_nonnegative("rollback_tolerance_s", rollback_tolerance_s)
    return bool(
        boot_epoch_id == attested_boot_epoch_id
        and seq_curr > seq_prev
        and (t_curr_s + rollback_tolerance_s) >= t_prev_s
    )


def compute_substrate_evidence_completeness_ratio(
    field_validity: Mapping[str, bool],
    field_weights: Mapping[str, float] | None = _policy.default,
) -> float:
    if not field_validity:
        raise ValueError("field_validity must be non-empty")
    if field_weights is None:
        field_weights = {key: 1.0 for key in field_validity}
    missing = [key for key in field_validity if key not in field_weights]
    if missing:
        raise ValueError(f"missing weights for fields: {missing}")
    weighted_good = 0.0
    weighted_total = 0.0
    for key, valid in field_validity.items():
        weight = float(field_weights[key])
        _require_positive(f"field_weights[{key!r}]", weight)
        weighted_total += weight
        if bool(valid):
            weighted_good += weight
    return float(weighted_good / weighted_total)


def compute_trust_root_attestation_freshness_margin(
    tau_attest_s: float,
    t_now_s: float,
    t_last_attest_s: float,
) -> float:
    _require_positive("tau_attest_s", tau_attest_s)
    if t_now_s < t_last_attest_s:
        raise ValueError("t_now_s must be >= t_last_attest_s")
    return float(tau_attest_s - (t_now_s - t_last_attest_s))


def compute_authority_to_act_gate(
    attestation_margin_s: float,
    evidence_completeness_ratio: float,
    evidence_threshold: float,
    electrical_valid: bool,
    timing_valid: bool,
    role_allowed: bool,
    recovery_blocked: bool,
) -> bool:
    if not (0.0 <= evidence_completeness_ratio <= 1.0):
        raise ValueError("evidence_completeness_ratio must lie in [0, 1]")
    if not (0.0 <= evidence_threshold <= 1.0):
        raise ValueError("evidence_threshold must lie in [0, 1]")
    return bool(
        attestation_margin_s >= 0.0
        and evidence_completeness_ratio >= evidence_threshold
        and electrical_valid
        and timing_valid
        and role_allowed
        and not recovery_blocked
    )


def compute_hardware_timing_closure_margin(
    tau_deadline_s: float,
    wcet_s: float,
    isr_jitter_s: float,
    bus_block_s: float,
    clock_skew_s: float,
    recovery_guard_s: float,
) -> float:
    _require_positive("tau_deadline_s", tau_deadline_s)
    for name, value in {
        "wcet_s": wcet_s,
        "isr_jitter_s": isr_jitter_s,
        "bus_block_s": bus_block_s,
        "clock_skew_s": clock_skew_s,
        "recovery_guard_s": recovery_guard_s,
    }.items():
        _require_nonnegative(name, value)
    return float(tau_deadline_s - (wcet_s + isr_jitter_s + bus_block_s + clock_skew_s + recovery_guard_s))


def compute_thermal_timing_derate_margin(
    tau_deadline_s: float,
    wcet_nominal_s: float,
    clock_fraction: float,
    thermal_jitter_s: float,
    bus_service_s: float,
    clock_error_s: float,
) -> float:
    _require_positive("tau_deadline_s", tau_deadline_s)
    _require_positive("wcet_nominal_s", wcet_nominal_s)
    _require_positive("clock_fraction", clock_fraction)
    for name, value in {
        "thermal_jitter_s": thermal_jitter_s,
        "bus_service_s": bus_service_s,
        "clock_error_s": clock_error_s,
    }.items():
        _require_nonnegative(name, value)
    effective_wcet = wcet_nominal_s / max(clock_fraction, _policy.value("denominator_floor"))
    return float(tau_deadline_s - (effective_wcet + thermal_jitter_s + bus_service_s + clock_error_s))


def compute_hardware_closed_command_seam_gate(
    brownout_margin_v: float,
    freshness_margin_s: float,
    coherence_margin_s: float,
    timing_closure_margin_s: float,
    authority_gate: bool,
) -> bool:
    return bool(
        brownout_margin_v >= 0.0
        and freshness_margin_s >= 0.0
        and coherence_margin_s >= 0.0
        and timing_closure_margin_s >= 0.0
        and authority_gate
    )


__all__ = [
    "compute_effective_brownout_margin",
    "compute_thermal_derated_power_margin",
    "compute_recovery_energy_margin",
    "compute_bus_clear_time_margin",
    "compute_segment_isolation_margin",
    "compute_post_recovery_reacquisition_margin",
    "compute_telemetry_use_freshness_margin",
    "compute_mixed_stream_coherence_margin",
    "compute_boot_epoch_sequence_gate",
    "compute_substrate_evidence_completeness_ratio",
    "compute_trust_root_attestation_freshness_margin",
    "compute_authority_to_act_gate",
    "compute_hardware_timing_closure_margin",
    "compute_thermal_timing_derate_margin",
    "compute_hardware_closed_command_seam_gate",
]

_policy.bind(globals())
