# Electrical

Rail headroom, thermal derate, and recovery energy laws that tell higher layers whether the substrate is still real.

### Optimal use

Use when timing, sensing, or actuation depends on a substrate that may be electrically sick before it is visibly dead.

### Do not use when

Do not use as full circuit simulation or bus qualification testing.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [bus_anchor_consistency_margin.py](bus_anchor_consistency_margin.py) — bus_anchor_consistency_margin
- [electrical_survivability_margins.py](electrical_survivability_margins.py)
- [illumination_cycle_energy_margin.py](illumination_cycle_energy_margin.py) — illumination_duty_cycle_energy_margin
- [occlusion_energy_reserve_margin.py](occlusion_energy_reserve_margin.py) — occlusion_energy_reserve_margin
- [regulation_chain_disparity_margin.py](regulation_chain_disparity_margin.py) — regulation_chain_disparity_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/electrical/bus_anchor_consistency_margin](../../../model_policy_engine/policies/hardware_viability/electrical/bus_anchor_consistency_margin_policy.toml)
- [hardware_viability/electrical/electrical_survivability_margins](../../../model_policy_engine/policies/hardware_viability/electrical/electrical_survivability_margins_policy.toml)
- [hardware_viability/electrical/illumination_cycle_energy_margin](../../../model_policy_engine/policies/hardware_viability/electrical/illumination_cycle_energy_margin_policy.toml)
- [hardware_viability/electrical/occlusion_energy_reserve_margin](../../../model_policy_engine/policies/hardware_viability/electrical/occlusion_energy_reserve_margin_policy.toml)
- [hardware_viability/electrical/regulation_chain_disparity_margin](../../../model_policy_engine/policies/hardware_viability/electrical/regulation_chain_disparity_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
bus_anchor_consistency_margin.py
  compute_bus_anchor_consistency_margin = 0.4
electrical_survivability_margins.py
  compute_effective_brownout_margin = -2.2
  compute_thermal_derated_power_margin = 21.625
  compute_recovery_energy_margin = -2.2
  compute_bus_clear_time_margin = -5.333333333333333
  compute_segment_isolation_margin = -2.2
  compute_post_recovery_reacquisition_margin = -2.2
  compute_telemetry_use_freshness_margin = 0.7
  compute_mixed_stream_coherence_margin = 0.0
  compute_boot_epoch_sequence_gate = true
  compute_substrate_evidence_completeness_ratio = 0.5
  compute_trust_root_attestation_freshness_margin = 4.0
  compute_authority_to_act_gate = false
  compute_hardware_timing_closure_margin = -3.1
  compute_thermal_timing_derate_margin = -2.625
  compute_hardware_closed_command_seam_gate = true
illumination_cycle_energy_margin.py
  compute_illumination_duty_cycle_energy_margin = 100.0
occlusion_energy_reserve_margin.py
  compute_occlusion_energy_reserve_margin = 60.0
regulation_chain_disparity_margin.py
  compute_regulation_chain_disparity_margin = 0.5
PASS hardware_viability/electrical
```

<!-- end-observed-output -->

## bus_anchor_consistency_margin.py

### Model context from the archive

POWER-SURV-006 — bus_anchor_consistency_margin

Purpose
-------
Provides one pessimistic typed margin for downstream decision logic and dashboards.

Assumptions
-----------
Use only when the single-rail survival margin and regulation disparity margin are already computed on compatible normalized scales.

### Entry points

- `compute_bus_anchor_consistency_margin(m_bus: float, m_reg: float)`

### Original formula record

- **Formula id**  POWER-SURV-006
- **Family**  electrical_survivability
- **Name**  bus_anchor_consistency_margin
- **Symbolic form**  `m_anchor = min(m_bus, m_reg)`
- **Typed inputs**  `m_bus` (float), `m_reg` (float)
- **Units**  `m_bus` (unitless), `m_reg` (unitless), `output` (unitless)
- **Assumptions**  Use only when the single-rail survival margin and regulation disparity margin are already computed on compatible normalized scales.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Provides one pessimistic typed margin for downstream decision logic and dashboards.
- **Status**  proposed_for_future_builds

## electrical_survivability_margins.py

### Model context from the archive

Cross-domain EE models for digital_twin_ssot.

These proposals are deliberately scoped to the EE lane:
electrical survivability, bus recovery, telemetry integrity,
trust-root governance, and hardware-closed timing/authority seams.

The file is self-contained on purpose so evaluators can keep or cut
individual candidates without dragging a large support package behind
them like a bag of wet concrete.

### Current interface

- The proposal registry and its records moved to this README. The computational functions retain their names.

### Entry points

- `compute_effective_brownout_margin(v_min_measured_v: float, v_uvlo_v: float, v_ripple_pk_v: float, v_predicted_droop_v: float, v_reference_uncertainty_v: float)`
- `compute_thermal_derated_power_margin(p_nominal_w: float, t_junction_c: float, t_warn_c: float, t_shutdown_c: float, aging_factor: float, p_load_w: float, p_transient_reserve_w: float)`
- `compute_recovery_energy_margin(e_available_j: float, e_restart_j: float, e_reacquire_j: float, e_isolate_j: float, e_safe_reserve_j: float)`
- `compute_bus_clear_time_margin(tau_clear_s: float, n_clock_pulses: int, f_clear_hz: float, t_buffer_s: float, t_slave_release_s: float, t_reprobe_s: float)`
- `compute_segment_isolation_margin(t_fault_spread_s: float, t_detect_s: float, t_gate_s: float, t_switch_s: float, t_quarantine_confirm_s: float)`
- `compute_post_recovery_reacquisition_margin(tau_data_valid_s: float, t_sample_age_s: float, t_recovery_s: float, t_reacquire_s: float, t_skew_s: float)`
- `compute_telemetry_use_freshness_margin(tau_use_s: float, t_now_s: float, t_sample_s: float, t_transport_s: float, t_clock_uncertainty_s: float)`
- `compute_mixed_stream_coherence_margin(tau_align_s: float, timestamps_s: Sequence[float], path_delays_s: Sequence[float] | None=None)`
- `compute_boot_epoch_sequence_gate(boot_epoch_id: str, attested_boot_epoch_id: str, seq_prev: int, seq_curr: int, t_prev_s: float, t_curr_s: float, rollback_tolerance_s: float)`
- `compute_substrate_evidence_completeness_ratio(field_validity: Mapping[str, bool], field_weights: Mapping[str, float] | None=None)`
- `compute_trust_root_attestation_freshness_margin(tau_attest_s: float, t_now_s: float, t_last_attest_s: float)`
- `compute_authority_to_act_gate(attestation_margin_s: float, evidence_completeness_ratio: float, evidence_threshold: float, electrical_valid: bool, timing_valid: bool, role_allowed: bool, recovery_blocked: bool)`
- `compute_hardware_timing_closure_margin(tau_deadline_s: float, wcet_s: float, isr_jitter_s: float, bus_block_s: float, clock_skew_s: float, recovery_guard_s: float)`
- `compute_thermal_timing_derate_margin(tau_deadline_s: float, wcet_nominal_s: float, clock_fraction: float, thermal_jitter_s: float, bus_service_s: float, clock_error_s: float)`
- `compute_hardware_closed_command_seam_gate(brownout_margin_v: float, freshness_margin_s: float, coherence_margin_s: float, timing_closure_margin_s: float, authority_gate: bool)`

### EE-ELEC-001 — effective_brownout_margin

- **Formula id**  EE-ELEC-001
- **Family**  electrical_survivability
- **Name**  effective_brownout_margin
- **Symbolic form**  `m_bro = V_min - (V_uvlo + ΔV_ripple + ΔV_droop + ΔV_ref)`
- **Typed inputs**  `v_min_measured_v` (float), `v_uvlo_v` (float), `v_ripple_pk_v` (float), `v_predicted_droop_v` (float), `v_reference_uncertainty_v` (float)
- **Units**  `v_min_measured_v` (V), `v_uvlo_v` (V), `v_ripple_pk_v` (V), `v_predicted_droop_v` (V), `v_reference_uncertainty_v` (V), `output` (V)
- **Assumptions**  All terms refer to the same rail or reference dependency window. Positive margin means the rail stays above the effective undervoltage boundary even after ripple, predicted droop, and reference uncertainty are admitted.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Single pessimistic rail-health scalar for compute rails, sensor references, propulsion buses, payload regulators, and relay-node power domains.
- **Blindspots strengthened**  power and thermal survivability, telemetry trust, hardware-closed timing and authority seams

### EE-ELEC-002 — thermal_derated_power_margin

- **Formula id**  EE-ELEC-002
- **Family**  electrical_survivability
- **Name**  thermal_derated_power_margin
- **Symbolic form**  `m_pth = P_nom * d_T * a - (P_load + P_transient),  d_T = clip((T_shutdown - T_j)/(T_shutdown - T_warn), 0, 1)`
- **Typed inputs**  `p_nominal_w` (float), `t_junction_c` (float), `t_warn_c` (float), `t_shutdown_c` (float), `aging_factor` (float), `p_load_w` (float), `p_transient_reserve_w` (float)
- **Units**  `p_nominal_w` (W), `t_junction_c` (C), `t_warn_c` (C), `t_shutdown_c` (C), `aging_factor` (unitless), `p_load_w` (W), `p_transient_reserve_w` (W), `output` (W)
- **Assumptions**  Aging factor lies in (0, 1]. The formula intentionally derates usable electrical power as junction temperature approaches shutdown, because hot hardware lies about remaining headroom right before it fails.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Bridges thermal stress into electrical capacity budgeting for edge compute, battery buses, motor drivers, radios, and payload processing nodes.
- **Blindspots strengthened**  power and thermal survivability, hardware-closed timing and authority seams, full plant fidelity

### EE-ELEC-003 — recovery_energy_margin

- **Formula id**  EE-ELEC-003
- **Family**  electrical_survivability
- **Name**  recovery_energy_margin
- **Symbolic form**  `m_rec = E_avail - (E_restart + E_reacquire + E_isolate + E_safe)`
- **Typed inputs**  `e_available_j` (float), `e_restart_j` (float), `e_reacquire_j` (float), `e_isolate_j` (float), `e_safe_reserve_j` (float)
- **Units**  `e_available_j` (J), `e_restart_j` (J), `e_reacquire_j` (J), `e_isolate_j` (J), `e_safe_reserve_j` (J), `output` (J)
- **Assumptions**  Recovery is only allowed when enough energy remains to restart, reacquire trustworthy state, isolate any bad segment, and still retain a governed safe reserve.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Turns restart optimism into an explicit keep-trying-versus-isolate decision for robots, spacecraft, maritime nodes, ground vehicles, and remote edge platforms.
- **Blindspots strengthened**  power and thermal survivability, hardware-closed timing and authority seams, telemetry trust

### EE-BUS-001 — bus_clear_time_margin

- **Formula id**  EE-BUS-001
- **Family**  bus_recovery_integrity
- **Name**  bus_clear_time_margin
- **Symbolic form**  `m_bclr = τ_clear - (N_clk/f_clear + t_buf + t_release + t_probe)`
- **Typed inputs**  `tau_clear_s` (float), `n_clock_pulses` (int), `f_clear_hz` (float), `t_buffer_s` (float), `t_slave_release_s` (float), `t_reprobe_s` (float)
- **Units**  `tau_clear_s` (s), `n_clock_pulses` (count), `f_clear_hz` (Hz), `t_buffer_s` (s), `t_slave_release_s` (s), `t_reprobe_s` (s), `output` (s)
- **Assumptions**  Applies to recoverable shared buses where deterministic clearing is permitted by protocol and hardware. Positive margin means recovery fits inside the bus-clear budget.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Generalizes to I2C, SMBus, shared SPI recovery windows, and serial command links that must be cleared before stale control windows collapse.
- **Blindspots strengthened**  contested edge-network realism, temporal coherence and provenance governance, hardware-closed timing and authority seams

### EE-BUS-002 — segment_isolation_margin

- **Formula id**  EE-BUS-002
- **Family**  bus_recovery_integrity
- **Name**  segment_isolation_margin
- **Symbolic form**  `m_iso = t_spread - (t_detect + t_gate + t_switch + t_confirm)`
- **Typed inputs**  `t_fault_spread_s` (float), `t_detect_s` (float), `t_gate_s` (float), `t_switch_s` (float), `t_quarantine_confirm_s` (float)
- **Units**  `t_fault_spread_s` (s), `t_detect_s` (s), `t_gate_s` (s), `t_switch_s` (s), `t_quarantine_confirm_s` (s), `output` (s)
- **Assumptions**  Fault spread time is the maximum tolerable delay before the bad segment contaminates shared state, data trust, or control authority. Positive margin means isolation beats propagation.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Useful for shared electrical segments, relay trunks, sensor backplanes, and mixed compute-peripheral buses where one liar or dead device can poison everyone else.
- **Blindspots strengthened**  contested edge-network realism, hardware-closed timing and authority seams, telemetry trust

### EE-BUS-003 — post_recovery_reacquisition_margin

- **Formula id**  EE-BUS-003
- **Family**  bus_recovery_integrity
- **Name**  post_recovery_reacquisition_margin
- **Symbolic form**  `m_prr = τ_data - (t_age + t_recovery + t_reacquire + t_skew)`
- **Typed inputs**  `tau_data_valid_s` (float), `t_sample_age_s` (float), `t_recovery_s` (float), `t_reacquire_s` (float), `t_skew_s` (float)
- **Units**  `tau_data_valid_s` (s), `t_sample_age_s` (s), `t_recovery_s` (s), `t_reacquire_s` (s), `t_skew_s` (s), `output` (s)
- **Assumptions**  Recovery is not enough. Trust only returns if the bus can recover and reacquire a new trustworthy sample before the data-validity budget expires.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Works for post-fault IMU, encoder, battery monitor, radio state, or navigation sensor reacquisition across land, air, sea, space, and fixed edge nodes.
- **Blindspots strengthened**  telemetry trust, temporal coherence and provenance governance, hardware-closed timing and authority seams

### EE-TEL-001 — telemetry_use_freshness_margin

- **Formula id**  EE-TEL-001
- **Family**  telemetry_temporal_integrity
- **Name**  telemetry_use_freshness_margin
- **Symbolic form**  `m_fresh = τ_use - ((t_now - t_sample) + t_transport + t_clock)`
- **Typed inputs**  `tau_use_s` (float), `t_now_s` (float), `t_sample_s` (float), `t_transport_s` (float), `t_clock_uncertainty_s` (float)
- **Units**  `tau_use_s` (s), `t_now_s` (s), `t_sample_s` (s), `t_transport_s` (s), `t_clock_uncertainty_s` (s), `output` (s)
- **Assumptions**  Data is only valid at use time, not merely at ingest. Positive margin means the sample is still usable after transport delay and clock uncertainty are admitted.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Simple enough for runtime admission control, broad enough for sensor packets, replicated state, digital twin deltas, and cross-domain telemetry gateways.
- **Blindspots strengthened**  temporal coherence and provenance governance, telemetry trust, contested edge-network realism

### EE-TEL-002 — mixed_stream_coherence_margin

- **Formula id**  EE-TEL-002
- **Family**  telemetry_temporal_integrity
- **Name**  mixed_stream_coherence_margin
- **Symbolic form**  `m_coh = τ_align - max_{{i,j}} |(t_i - d_i) - (t_j - d_j)|`
- **Typed inputs**  `tau_align_s` (float), `timestamps_s` (Sequence[float]), `path_delays_s` (Sequence[float] | None)
- **Units**  `tau_align_s` (s), `timestamps_s` (s), `path_delays_s` (s), `output` (s)
- **Assumptions**  Each timestamp refers to the same physical state estimate or fusion epoch. Positive margin means the streams still describe one coherent moment after delay correction.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Catches mixed fresh-and-stale packets in sensor fusion, multi-radio swarms, digital twin merges, and relay chains that individually look valid but jointly lie.
- **Blindspots strengthened**  temporal coherence and provenance governance, telemetry trust, contested edge-network realism

### EE-TEL-003 — boot_epoch_sequence_gate

- **Formula id**  EE-TEL-003
- **Family**  telemetry_temporal_integrity
- **Name**  boot_epoch_sequence_gate
- **Symbolic form**  `g_bes = I(epoch = epoch_attested) * I(seq_curr > seq_prev) * I(t_curr + ε_roll >= t_prev)`
- **Typed inputs**  `boot_epoch_id` (str), `attested_boot_epoch_id` (str), `seq_prev` (int), `seq_curr` (int), `t_prev_s` (float), `t_curr_s` (float), `rollback_tolerance_s` (float)
- **Units**  `boot_epoch_id` (text), `attested_boot_epoch_id` (text), `seq_prev` (count), `seq_curr` (count), `t_prev_s` (s), `t_curr_s` (s), `rollback_tolerance_s` (s), `output` (bool)
- **Assumptions**  A reboot, replay, or rollback can make well-formed packets operationally false. This gate only passes when epoch identity matches attestation, sequence increases, and timestamps do not roll back beyond tolerance.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Useful for anti-replay telemetry gates, reset-loop detection, post-brownout quarantine, and any path where old packets may masquerade as current truth.
- **Blindspots strengthened**  temporal coherence and provenance governance, telemetry trust, hardware-closed timing and authority seams

### EE-ROOT-001 — substrate_evidence_completeness_ratio

- **Formula id**  EE-ROOT-001
- **Family**  trust_root_governance
- **Name**  substrate_evidence_completeness_ratio
- **Symbolic form**  `R_sec = Σ w_i I(field_i valid) / Σ w_i`
- **Typed inputs**  `field_validity` (Mapping[str, bool]), `field_weights` (Mapping[str, float] | None)
- **Units**  `field_validity` (bool-map), `field_weights` (unitless-map), `output` (unitless)
- **Assumptions**  This is for electrical and telemetry evidence completeness, not narrative completeness. Missing monotonic sequence, fault code, bus correlation, recovery state, or electrical validity should hurt the score materially.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable as a low-level provenance quality floor before telemetry, events, recovery logs, or command acknowledgements are allowed upstream.
- **Blindspots strengthened**  temporal coherence and provenance governance, telemetry trust, hardware-closed timing and authority seams

### EE-ROOT-002 — trust_root_attestation_freshness_margin

- **Formula id**  EE-ROOT-002
- **Family**  trust_root_governance
- **Name**  trust_root_attestation_freshness_margin
- **Symbolic form**  `m_att = τ_attest - (t_now - t_attest)`
- **Typed inputs**  `tau_attest_s` (float), `t_now_s` (float), `t_last_attest_s` (float)
- **Units**  `tau_attest_s` (s), `t_now_s` (s), `t_last_attest_s` (s), `output` (s)
- **Assumptions**  Attestation is not immortal. Positive margin means the current trust-root proof is still inside its allowed freshness window.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Keeps firmware trust and command authority tied to recent verification instead of startup mythology.
- **Blindspots strengthened**  temporal coherence and provenance governance, hardware-closed timing and authority seams, telemetry trust

### EE-ROOT-003 — authority_to_act_gate

- **Formula id**  EE-ROOT-003
- **Family**  trust_root_governance
- **Name**  authority_to_act_gate
- **Symbolic form**  `g_auth = I(m_att >= 0) * I(R_sec >= τ_sec) * I(elec_valid) * I(time_valid) * I(role_allowed) * I(recovery_block = 0)`
- **Typed inputs**  `attestation_margin_s` (float), `evidence_completeness_ratio` (float), `evidence_threshold` (float), `electrical_valid` (bool), `timing_valid` (bool), `role_allowed` (bool), `recovery_blocked` (bool)
- **Units**  `attestation_margin_s` (s), `evidence_completeness_ratio` (unitless), `evidence_threshold` (unitless), `electrical_valid` (bool), `timing_valid` (bool), `role_allowed` (bool), `recovery_blocked` (bool), `output` (bool)
- **Assumptions**  Command authority is a multi-precondition gate. Passing credentials alone are insufficient when the electrical substrate, time base, or recovery state are compromised.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Portable mission-action gate for actuators, radios, mode changes, flight-software commands, and fleet coordination updates.
- **Blindspots strengthened**  hardware-closed timing and authority seams, temporal coherence and provenance governance, telemetry trust

### EE-TIME-001 — hardware_timing_closure_margin

- **Formula id**  EE-TIME-001
- **Family**  hardware_timing_survivability
- **Name**  hardware_timing_closure_margin
- **Symbolic form**  `m_htc = τ_deadline - (WCET + J_isr + B_bus + E_clk + G_rec)`
- **Typed inputs**  `tau_deadline_s` (float), `wcet_s` (float), `isr_jitter_s` (float), `bus_block_s` (float), `clock_skew_s` (float), `recovery_guard_s` (float)
- **Units**  `tau_deadline_s` (s), `wcet_s` (s), `isr_jitter_s` (s), `bus_block_s` (s), `clock_skew_s` (s), `recovery_guard_s` (s), `output` (s)
- **Assumptions**  Positive margin means the loop still closes after execution time, interrupt jitter, bus blocking, clock error, and recovery guard are all charged against the deadline.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Works for embedded control loops, telemetry ingest deadlines, edge inference windows, and coordinated fleet behavior where timing closure is a hard boundary.
- **Blindspots strengthened**  hardware-closed timing and authority seams, contested edge-network realism, full plant fidelity

### EE-TIME-002 — thermal_timing_derate_margin

- **Formula id**  EE-TIME-002
- **Family**  hardware_timing_survivability
- **Name**  thermal_timing_derate_margin
- **Symbolic form**  `m_ttd = τ_deadline - (WCET_nom/max(ϕ_clk, ε) + J_thermal + B_bus + E_clk)`
- **Typed inputs**  `tau_deadline_s` (float), `wcet_nominal_s` (float), `clock_fraction` (float), `thermal_jitter_s` (float), `bus_service_s` (float), `clock_error_s` (float)
- **Units**  `tau_deadline_s` (s), `wcet_nominal_s` (s), `clock_fraction` (unitless), `thermal_jitter_s` (s), `bus_service_s` (s), `clock_error_s` (s), `output` (s)
- **Assumptions**  Clock fraction is the available execution-rate fraction under thermal throttling. Positive margin means the loop still closes after heat-induced slowdown is admitted.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Binds thermal throttling to deadline miss risk for compute nodes, payload processors, autonomy pods, and communications relays.
- **Blindspots strengthened**  power and thermal survivability, hardware-closed timing and authority seams, telemetry trust

### EE-TIME-003 — hardware_closed_command_seam_gate

- **Formula id**  EE-TIME-003
- **Family**  hardware_timing_survivability
- **Name**  hardware_closed_command_seam_gate
- **Symbolic form**  `g_hcc = I(m_bro >= 0) * I(m_fresh >= 0) * I(m_coh >= 0) * I(m_htc >= 0) * I(g_auth = 1)`
- **Typed inputs**  `brownout_margin_v` (float), `freshness_margin_s` (float), `coherence_margin_s` (float), `timing_closure_margin_s` (float), `authority_gate` (bool)
- **Units**  `brownout_margin_v` (V), `freshness_margin_s` (s), `coherence_margin_s` (s), `timing_closure_margin_s` (s), `authority_gate` (bool), `output` (bool)
- **Assumptions**  This top seam gate is intentionally fail-closed. Electrical health, freshness, cross-stream coherence, timing closure, and authority must all be true at once before a command crosses into actuation.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Cross-domain last barrier that prevents individually plausible but jointly unsafe data from reaching motors, thrusters, radios, valves, or mode switches.
- **Blindspots strengthened**  hardware-closed timing and authority seams, temporal coherence and provenance governance, telemetry trust, power and thermal survivability

## illumination_cycle_energy_margin.py

### Model context from the archive

POWER-SURV-003 — illumination_duty_cycle_energy_margin

Purpose
-------
Improves power survivability estimates when illumination is intermittent.

Assumptions
-----------
Separates lit and dark operating modes and charge recovery instead of flattening the whole window into one average load.

### Entry points

- `compute_illumination_duty_cycle_energy_margin(E_available_wh: float, gen_lit_wh_per_h: float, load_lit_wh_per_h: float, load_dark_wh_per_h: float, t_lit_h: float, t_dark_h: float)`

### Original formula record

- **Formula id**  POWER-SURV-003
- **Family**  power_survivability
- **Name**  illumination_duty_cycle_energy_margin
- **Symbolic form**  `m_idc = E_available_wh + gen_lit_wh_per_h * t_lit_h - (load_lit_wh_per_h * t_lit_h + load_dark_wh_per_h * t_dark_h)`
- **Typed inputs**  `E_available_wh` (float), `gen_lit_wh_per_h` (float), `load_lit_wh_per_h` (float), `load_dark_wh_per_h` (float), `t_lit_h` (float), `t_dark_h` (float)
- **Units**  `E_available_wh` (Wh), `gen_lit_wh_per_h` (Wh/h), `load_lit_wh_per_h` (Wh/h), `load_dark_wh_per_h` (Wh/h), `t_lit_h` (h), `t_dark_h` (h), `output` (Wh)
- **Assumptions**  Separates lit and dark operating modes and charge recovery instead of flattening the whole window into one average load.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Improves power survivability estimates when illumination is intermittent.
- **Status**  proposed_for_future_builds

## occlusion_energy_reserve_margin.py

### Model context from the archive

POWER-SURV-004 — occlusion_energy_reserve_margin

Purpose
-------
Abort reserve screening, shadow crossing, eclipse handling, relay outage survival, and time-bounded safe-state entry calculations.

Assumptions
-----------
Improves on average-load darkness margins when the critical branch is a short predicted occlusion that must still pay for waveoff or safe-state entry energy. A vehicle can fail even when long-horizon darkness averages look acceptable.

### Entry points

- `compute_occlusion_energy_reserve_margin(E_available_wh: float, P_dark_whph: float, t_occ_h: float, E_waveoff_wh: float, E_keepalive_wh: float)`

### Original formula record

- **Formula id**  POWER-SURV-004
- **Family**  power_survivability
- **Name**  occlusion_energy_reserve_margin
- **Symbolic form**  `m_occ = E_available_wh - P_dark_whph * t_occ_h - E_waveoff_wh - E_keepalive_wh`
- **Typed inputs**  `E_available_wh` (float), `P_dark_whph` (float), `t_occ_h` (float), `E_waveoff_wh` (float), `E_keepalive_wh` (float)
- **Units**  `E_available_wh` (Wh), `P_dark_whph` (Wh/h), `t_occ_h` (h), `E_waveoff_wh` (Wh), `E_keepalive_wh` (Wh), `output` (Wh)
- **Assumptions**  Improves on average-load darkness margins when the critical branch is a short predicted occlusion that must still pay for waveoff or safe-state entry energy. A vehicle can fail even when long-horizon darkness averages look acceptable.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Abort reserve screening, shadow crossing, eclipse handling, relay outage survival, and time-bounded safe-state entry calculations.
- **Status**  proposed_for_future_builds

## regulation_chain_disparity_margin.py

### Model context from the archive

POWER-SURV-005 — regulation_chain_disparity_margin

Purpose
-------
Detects converter-chain disagreement even when each rail is still individually inside bounds.

Assumptions
-----------
Both rails are already normalized to their own nominal voltages and delta_limit_pu is a governed threshold.

### Entry points

- `compute_regulation_chain_disparity_margin(v_upstream_pu: float, v_downstream_pu: float, delta_limit_pu: float)`

### Original formula record

- **Formula id**  POWER-SURV-005
- **Family**  electrical_survivability
- **Name**  regulation_chain_disparity_margin
- **Symbolic form**  `m_reg = delta_limit_pu - abs(v_upstream_pu - v_downstream_pu)`
- **Typed inputs**  `v_upstream_pu` (float), `v_downstream_pu` (float), `delta_limit_pu` (float)
- **Units**  `v_upstream_pu` (unitless), `v_downstream_pu` (unitless), `delta_limit_pu` (unitless), `output` (unitless)
- **Assumptions**  Both rails are already normalized to their own nominal voltages and delta_limit_pu is a governed threshold.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Detects converter-chain disagreement even when each rail is still individually inside bounds.
- **Status**  proposed_for_future_builds
