# Actuator

Whether actuation remains safe and supportable given current power, thermal, and bus conditions.

### Optimal use

Use when commands can themselves collapse the substrate or when derate shrinks the actuator envelope.

### Do not use when

Do not use without the matching electrical and thermal truths that define the envelope.

## Model files

- [abort_closure_margin.py](abort_closure_margin.py) — Abort closure margin
- [actuator_saturation.py](actuator_saturation.py) — Actuator saturation law
- [actuator_slew_rate.py](actuator_slew_rate.py) — Actuator slew‑rate bound
- [attainable_wrench_residual.py](attainable_wrench_residual.py) — Attainable wrench residual law
- [control_allocation_residual.py](control_allocation_residual.py) — Control allocation residual under bounded actuators
- [controllability_margin.py](controllability_margin.py) — Authority-weighted controllability margin
- [lawful_actuation_clf_cbf_qp.py](lawful_actuation_clf_cbf_qp.py) — Lawful actuation governance CLF–CBF QP
- [lease_validity_margin.py](lease_validity_margin.py) — Authority lease validity margin
- [mechatronics_power_roundup.py](mechatronics_power_roundup.py)
- [safe_velocity_margin.py](safe_velocity_margin.py) — Truth-conditioned safe velocity margin
- [specific_energy_reserve_to_go.py](specific_energy_reserve_to_go.py) — Specific energy reserve-to-go law

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/actuator/abort_closure_margin](../../../model_policy_engine/policies/hardware_viability/actuator/abort_closure_margin_policy.toml)
- [hardware_viability/actuator/actuator_saturation](../../../model_policy_engine/policies/hardware_viability/actuator/actuator_saturation_policy.toml)
- [hardware_viability/actuator/actuator_slew_rate](../../../model_policy_engine/policies/hardware_viability/actuator/actuator_slew_rate_policy.toml)
- [hardware_viability/actuator/attainable_wrench_residual](../../../model_policy_engine/policies/hardware_viability/actuator/attainable_wrench_residual_policy.toml)
- [hardware_viability/actuator/control_allocation_residual](../../../model_policy_engine/policies/hardware_viability/actuator/control_allocation_residual_policy.toml)
- [hardware_viability/actuator/controllability_margin](../../../model_policy_engine/policies/hardware_viability/actuator/controllability_margin_policy.toml)
- [hardware_viability/actuator/lawful_actuation_clf_cbf_qp](../../../model_policy_engine/policies/hardware_viability/actuator/lawful_actuation_clf_cbf_qp_policy.toml)
- [hardware_viability/actuator/lease_validity_margin](../../../model_policy_engine/policies/hardware_viability/actuator/lease_validity_margin_policy.toml)
- [hardware_viability/actuator/mechatronics_power_roundup](../../../model_policy_engine/policies/hardware_viability/actuator/mechatronics_power_roundup_policy.toml)
- [hardware_viability/actuator/safe_velocity_margin](../../../model_policy_engine/policies/hardware_viability/actuator/safe_velocity_margin_policy.toml)
- [hardware_viability/actuator/specific_energy_reserve_to_go](../../../model_policy_engine/policies/hardware_viability/actuator/specific_energy_reserve_to_go_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
abort_closure_margin.py
  compute_abort_closure_margin = -0.9583333333333334
actuator_saturation.py
  compute_actuator_saturation = 0.4
  compute_actuator_saturation = 2
actuator_slew_rate.py
  compute_slew_limited_command = 0.5
attainable_wrench_residual.py
  compute_attainable_wrench_residual = 2.0
control_allocation_residual.py
  compute_control_allocation_residual = 2.23606797749979
  compute_control_allocation_residual = 2.23606797749979
  compute_control_allocation_residual rejected invalid input
controllability_margin.py
  compute_authority_weighted_controllability_margin = 0.6000000000000001
  compute_authority_weighted_controllability_margin = -0.1
  compute_authority_weighted_controllability_margin rejected invalid input
lawful_actuation_clf_cbf_qp.py
  cbf_margin = 1.25
  clf_value = 0.5
  clf_vdot = -0.4
  clf_margin = -0.09999999999999998
  null_set_trigger = true
  active CLF [control, slack, null_set] = [-0.4000000000000001, 0.09999999999999992, true]
  clear [success, safe_without_slack, null_set] = [true, true, false]
lease_validity_margin.py
  compute_authority_lease_validity_margin = -1.4
mechatronics_power_roundup.py
  pbr001_min_hold_up_time_closure = {"passed": true, "value": 0.065}
  pbr002_brownout_entry_guard = false
  pbr003_stable_restart_gate = false
  pbr004_rail_coherence_index = {"passed": true, "value": 0.03333333333333333}
  ptt001_tau_valid = 0.282258064516129
  ptt001_power_telemetry_freshness_at_use_gate = {"passed": true, "value": -0.5256756756756756}
  paa001_actuation_enable_authority_gate = false
  paa002_actuator_induced_bus_sag_closure = {"passed": false, "value": -0.72}
  paa003_thermal_voltage_derated_actuator_envelope = 0.75
  paa004_safe_reenable_delay = 0.8
  tpd001_two_node_thermal_rc_step = [0.8999999999999999, 0.494949494949495]
  tpd002_thermal_timing_derate = {"passed": true, "value": 0.4}
  tpd003_thermal_distortion_confidence_ceiling = 0.4
  ecl001_energy_continuity_margin = -0.8
  ecl002_regulation_chain_delivery_margin = {"passed": false, "value": -1.6742857142857144}
  ecl003_priority_load_shed_optimization = [[], 0]
safe_velocity_margin.py
  compute_truth_conditioned_safe_velocity_margin = -0.5
specific_energy_reserve_to_go.py
  compute_specific_energy_reserve_margin = -0.7000000000000001
test_lawful_actuation_clf_cbf_qp.py: 3 passed, 0 skipped
PASS hardware_viability/actuator
```

<!-- end-observed-output -->

## abort_closure_margin.py

### Model context from the archive

M3.2c — Abort closure margin

This law computes whether a platform still has enough corridor left to decide,
react, and decelerate into a survivable abort or waveoff:

    m_abort = d_corridor − v τ_decide − v²/(2 a_eff) − d_reserve

When the margin goes negative, the system has already consumed its physical
escape path.

### Entry points

- `compute_abort_closure_margin(corridor_distance: float, current_speed: float, effective_deceleration: float, decision_latency: float, reserve_distance: float)`

### Original formula record

- **Formula id**  M3.2c
- **Name**  Abort closure margin
- **Symbolic form**  `m_abort = d_corridor − v τ_decide − v²/(2 a_eff) − d_reserve`
- **Typed inputs**  `corridor_distance` (float), `current_speed` (float), `effective_deceleration` (float), `decision_latency` (float), `reserve_distance` (float)
- **Units**  `corridor_distance` (m), `current_speed` (m/s), `effective_deceleration` (m/s²), `decision_latency` (s), `reserve_distance` (m), `output` (m)
- **Assumptions**  Current speed is non-negative along the abort axis. Effective deceleration must be positive.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_m3_2c_abort_closure_margin.py::test_positive_margin_when_enough_corridor_exists`, `rtm_link=lambda_laws.m3_2c_abort_closure_margin`, `ssot_gate=notebooks/gate_m3_2c_abort_closure_margin.ipynb`

## actuator_saturation.py

### Model context from the archive

M3.1c — Actuator saturation law

This module implements actuator saturation, which clips the commanded
control input to the allowable range ``[u_min, u_max]``:

    u_sat(t) = clip(u_cmd(t), u_min, u_max).

If the command lies within the range, it is returned unchanged; otherwise
it is clipped to the nearest bound.

### Entry points

- `compute_actuator_saturation(u_cmd: float, u_min: float, u_max: float)`

### Original formula record

- **Formula id**  M3.1c
- **Name**  Actuator saturation law
- **Symbolic form**  `u_sat(t) = clip(u_cmd(t), u_min, u_max)`
- **Typed inputs**  `u_cmd` (float), `u_min` (float), `u_max` (float)
- **Units**  `u_cmd` (unit), `u_min` (unit), `u_max` (unit), `output` (unit)
- **Assumptions**  u_min <= u_max.  Control inputs outside this range are clipped to the nearest bound.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_actuator_saturation.py::test_actuator_saturation`, `rtm_link=lambda_laws.actuator_saturation`, `ssot_gate=notebooks/gate_actuator_saturation.ipynb`

Additional reference comparisons during migration: 1.

## actuator_slew_rate.py

### Model context from the archive

M3.1d — Actuator slew‑rate bound

This module implements the slew‑rate limiting of actuator commands.  The
commanded control input is adjusted to respect a maximum rate of change
``u_dot_max``:

    |u(t) − u_prev| / dt ≤ u_dot_max.

Given the previous command ``u_prev``, desired command ``u_cmd``, time
step ``dt``, and maximum slew rate ``u_dot_max``, the function returns
a new command that respects the rate bound.

### Entry points

- `compute_slew_limited_command(u_prev: float, u_cmd: float, dt: float, u_dot_max: float)`

### Original formula record

- **Formula id**  M3.1d
- **Name**  Actuator slew‑rate bound
- **Symbolic form**  `|u̇(t)| ≤ u_dot_max`
- **Typed inputs**  `u_prev` (float), `u_cmd` (float), `dt` (float), `u_dot_max` (float)
- **Units**  `u_prev` (unit), `u_cmd` (unit), `dt` (s), `u_dot_max` (unit/s), `output` (unit)
- **Assumptions**  dt > 0 and u_dot_max ≥ 0.  The slew rate bound applies to the absolute change in command over the time step.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_actuator_slew_rate.py::test_actuator_slew_rate`, `rtm_link=lambda_laws.actuator_slew_rate`, `ssot_gate=notebooks/gate_actuator_slew_rate.ipynb`

## attainable_wrench_residual.py

### Model context from the archive

M3.2b — Attainable wrench residual law

Purpose
-------
Measures how far a commanded force-moment wrench sits outside real actuator
authority after saturation. This turns "controller asked for it" into "hardware
could actually do it," which is the sort of distinction reality enjoys enforcing.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_attainable_wrench_residual(allocation_matrix: list[list[float]], commanded_actuator: list[float], u_min: list[float], u_max: list[float], commanded_wrench: list[float], weight_matrix: list[list[float]] | None=None)`

### Original formula record

- **Formula id**  M3.2b
- **Name**  Attainable wrench residual law
- **Symbolic form**  `r_w = || w_cmd - B sat(u_cmd, u_min, u_max) ||_W`
- **Typed inputs**  `allocation_matrix` (ndarray[shape=(m,n), dtype=float]), `commanded_actuator` (ndarray[shape=(n,), dtype=float]), `u_min` (ndarray[shape=(n,), dtype=float]), `u_max` (ndarray[shape=(n,), dtype=float]), `commanded_wrench` (ndarray[shape=(m,), dtype=float]), `weight_matrix` (ndarray[shape=(m,m), dtype=float] | None)
- **Units**  `output` (weighted wrench residual)
- **Assumptions**  Allocation matrix is locally valid; actuator clipping approximates dominant authority limits; positive residual indicates command infeasibility or control allocation loss.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  full plant fidelity, hardware-closed timing and authority seams, actuator fault degradation, late-abort feasibility

Additional reference comparisons during migration: 51.

## control_allocation_residual.py

### Model context from the archive

M3.2b — Control allocation residual under bounded actuators

Given a control effectiveness matrix B and a desired generalized wrench w_d,
this law solves a least-squares allocation, clips the result to actuator
bounds, and returns the residual mismatch:

    r_alloc = ||w_d − B sat(B⁺ w_d)||_2

A growing residual means the controller is asking hardware for authority it
no longer has.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_control_allocation_residual(effectiveness_matrix: Sequence[Sequence[float]], desired_wrench: Sequence[float], actuator_min: Sequence[float], actuator_max: Sequence[float])`

### Original formula record

- **Formula id**  M3.2b
- **Name**  Control allocation residual under bounded actuators
- **Symbolic form**  `r_alloc = ||w_d − B sat(B⁺ w_d)||_2`
- **Typed inputs**  `effectiveness_matrix` (Sequence[Sequence[float]]), `desired_wrench` (Sequence[float]), `actuator_min` (Sequence[float]), `actuator_max` (Sequence[float])
- **Units**  `effectiveness_matrix` (mapping), `desired_wrench` (generalized_force), `actuator_min` (actuator_command), `actuator_max` (actuator_command), `output` (generalized_force)
- **Assumptions**  The effectiveness matrix must map actuator commands into the desired wrench space. Bounds must be elementwise valid.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_m3_2b_control_allocation_residual.py::test_identity_allocation_zero_residual`, `rtm_link=lambda_laws.m3_2b_control_allocation_residual`, `ssot_gate=notebooks/gate_m3_2b_control_allocation_residual.ipynb`

Additional reference comparisons during migration: 186.

## controllability_margin.py

### Model context from the archive

M3.2e — Authority-weighted controllability margin

This law estimates remaining control authority after actuator degradation,
partial outages, or command vetoes by scaling the control effectiveness matrix
with authority weights a_i ∈ [0,1] and comparing the smallest singular value
to a required floor:

    m_ctrl = σ_min(B diag(a)) − σ_req

Positive margin means the platform still retains the minimum directional
authority needed to command the controlled axes.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_authority_weighted_controllability_margin(effectiveness_matrix: Sequence[Sequence[float]], authority_weights: Sequence[float], required_min_singular_value: float)`

### Original formula record

- **Formula id**  M3.2e
- **Name**  Authority-weighted controllability margin
- **Symbolic form**  `m_ctrl = σ_min(B diag(a)) − σ_req`
- **Typed inputs**  `effectiveness_matrix` (Sequence[Sequence[float]]), `authority_weights` (Sequence[float]), `required_min_singular_value` (float)
- **Units**  `effectiveness_matrix` (mapping), `authority_weights` (unitless), `required_min_singular_value` (authority), `output` (authority)
- **Assumptions**  Authority weights must lie in [0,1]. The effectiveness matrix must have at least one singular value.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_m3_2e_authority_weighted_controllability_margin.py::test_degraded_authority_reduces_margin`, `rtm_link=lambda_laws.m3_2e_authority_weighted_controllability_margin`, `ssot_gate=notebooks/gate_m3_2e_authority_weighted_controllability_margin.ipynb`

Additional reference comparisons during migration: 186.

## lease_validity_margin.py

### Model context from the archive

M6.1c — Authority lease validity margin

This law checks whether delegated authority remains valid at the predicted
execution instant rather than merely at dispatch time:

    m_lease = t_expire − t_exec − ε_clock − τ_guard

A negative result means the command will execute outside its lawful time
window even if the packet itself arrived without complaint.

### Entry points

- `compute_authority_lease_validity_margin(lease_expiry_time: float, predicted_execution_time: float, clock_uncertainty: float, guard_band: float)`

### Original formula record

- **Formula id**  M6.1c
- **Name**  Authority lease validity margin
- **Symbolic form**  `m_lease = t_expire − t_exec − ε_clock − τ_guard`
- **Typed inputs**  `lease_expiry_time` (float), `predicted_execution_time` (float), `clock_uncertainty` (float), `guard_band` (float)
- **Units**  `lease_expiry_time` (s), `predicted_execution_time` (s), `clock_uncertainty` (s), `guard_band` (s), `output` (s)
- **Assumptions**  Lease expiry and execution time use the same reference clock domain or have already been converted into one.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_m6_1c_authority_lease_validity_margin.py::test_margin_turns_negative_after_expiry`, `rtm_link=lambda_laws.m6_1c_authority_lease_validity_margin`, `ssot_gate=notebooks/gate_m6_1c_authority_lease_validity_margin.ipynb`

## mechatronics_power_roundup.py

### Model context from the archive

Deterministic mechatronics-power formula primitives for network keep/cut/merge review.

These are refinement-grade executable laws. They are NOT promoted to certification truth.
No external dependencies required because life is short and broken imports are embarrassing.

### Entry points

- `GateResult` (type)
- `clamp(value: float, low: float, high: float)`
- `pbr001_min_hold_up_time_closure(c_eff_f: float, v_start_v: float, v_bor_v: float, p_crit_w: float, t_inhibit_s: float, t_log_s: float, t_reset_s: float)`
- `pbr002_brownout_entry_guard(v_bus_v: float, v_fall_v: float, dt_below_s: float, tau_confirm_s: float, dv_bus_dt_v_per_s: float, gamma_drop_v_per_s: float)`
- `pbr003_stable_restart_gate(v_bus_v: float, v_rise_v: float, sigma_v: float, sigma_max: float, dv_bus_dt_v_per_s: float, gamma_settle_v_per_s: float, dt_above_s: float, tau_stable_s: float)`
- `pbr004_rail_coherence_index(voltages_v: Sequence[float], v_nom_v: float, rho_max: float)`
- `ptt001_tau_valid(dv_bus_dt_abs_v_per_s: float, tau_base_s: float, k_dv_s2_per_v: float, state_factor: float)`
- `ptt001_power_telemetry_freshness_at_use_gate(t_use_s: float, t_stamp_s: float, dv_bus_dt_abs_v_per_s: float, tau_base_s: float, k_dv_s2_per_v: float, state_factor: float)`
- `paa001_actuation_enable_authority_gate(power_valid: bool, actuator_bus_valid: bool, thermal_valid: bool, state_valid: bool, fault_latched: bool, valid_for_use: bool)`
- `paa002_actuator_induced_bus_sag_closure(i_step_a: float, r_eq_ohm: float, l_eq_h: float, di_dt_a_per_s: float, v_pre_v: float, v_hold_v: float)`
- `paa003_thermal_voltage_derated_actuator_envelope(u_nom: float, t_core_c: float, t_warn_c: float, t_crit_c: float, v_bus_v: float, v_min_v: float, v_nom_v: float)`
- `paa004_safe_reenable_delay(t_sensor_settle_s: float, t_estimator_lock_s: float, t_bus_stable_s: float, t_clock_sync_s: float, t_fault_clear_s: float)`
- `tpd001_two_node_thermal_rc_step(t_core_c: float, t_sink_c: float, t_amb_c: float, p_loss_w: float, c_core_j_per_c: float, c_sink_j_per_c: float, r_cs_c_per_w: float, r_sa_c_per_w: float, dt_s: float)`
- `tpd002_thermal_timing_derate(wcet_nom_s: float, t_core_c: float, t_ref_c: float, k_t_per_c: float, t_budget_s: float)`
- `tpd003_thermal_distortion_confidence_ceiling(conf_nom: float, k_conf_per_c: float, t_core_c: float, t_cal_c: float)`
- `ecl001_energy_continuity_margin(e_avail: float, eta_gen: float, p_gen_profile_w: Sequence[float], p_load_profile_w: Sequence[float], dt_s: float, e_reserve: float, e_req: float)`
- `ecl002_regulation_chain_delivery_margin(p_src_w: float, eta_stages: Sequence[float], p_parasitic_w: float, p_demand_w: float)`
- `ecl003_priority_load_shed_optimization(utilities: Sequence[float], powers_w: Sequence[float], p_avail_w: float, p_reserve_w: float, critical_indices: Sequence[int]=(), prohibited_indices: Sequence[int]=())`

## safe_velocity_margin.py

### Model context from the archive

M3.2d — Truth-conditioned safe velocity margin

This law turns terrain or obstacle uncertainty into a control-relevant speed
guard by shrinking usable distance before computing the maximum survivable
closing speed:

    d_eff = d_hazard − v τ_lat − σ_terrain − 0.5 r_map − σ_loc
    v_safe = sqrt(max(2 a_eff d_eff, 0))
    m_v = v_safe − v

It helps prevent a controller from treating coarse or stale environment truth
as if it were precise geometry.

### Entry points

- `compute_truth_conditioned_safe_velocity_margin(distance_to_hazard: float, current_speed: float, effective_deceleration: float, actuation_latency: float, terrain_truth_sigma: float, map_resolution: float, localization_sigma: float)`

### Original formula record

- **Formula id**  M3.2d
- **Name**  Truth-conditioned safe velocity margin
- **Symbolic form**  `d_eff = d_hazard − vτ_lat − σ_terrain − 0.5r_map − σ_loc; v_safe = sqrt(max(2a_eff d_eff,0)); m_v = v_safe − v`
- **Typed inputs**  `distance_to_hazard` (float), `current_speed` (float), `effective_deceleration` (float), `actuation_latency` (float), `terrain_truth_sigma` (float), `map_resolution` (float), `localization_sigma` (float)
- **Units**  `distance_to_hazard` (m), `current_speed` (m/s), `effective_deceleration` (m/s²), `actuation_latency` (s), `terrain_truth_sigma` (m), `map_resolution` (m), `localization_sigma` (m), `output` (m/s)
- **Assumptions**  Distance and uncertainty terms are along the relevant closure axis. Effective deceleration must be positive.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_m3_2d_truth_conditioned_safe_velocity_margin.py::test_uncertainty_reduces_margin`, `rtm_link=lambda_laws.m3_2d_truth_conditioned_safe_velocity_margin`, `ssot_gate=notebooks/gate_m3_2d_truth_conditioned_safe_velocity_margin.ipynb`

## specific_energy_reserve_to_go.py

### Model context from the archive

M3.2d — Specific energy reserve-to-go law

Purpose
-------
Compresses mission closure into a single question: after accounting for what the
vehicle must still do and what it must still survive, is there enough energy left
to make the demanded future physically credible?

### Entry points

- `compute_specific_energy_reserve_margin(energy_available: float, energy_to_go: float, abort_reserve: float, uncertainty_buffer: float=0.0)`

### Original formula record

- **Formula id**  M3.2d
- **Name**  Specific energy reserve-to-go law
- **Symbolic form**  `m_E = E_available - (E_to_go + E_abort_reserve + E_uncertainty_buffer)`
- **Typed inputs**  `energy_available` (float), `energy_to_go` (float), `abort_reserve` (float), `uncertainty_buffer` (float)
- **Units**  `energy_available` (J), `energy_to_go` (J), `abort_reserve` (J), `uncertainty_buffer` (J), `output` (J)
- **Assumptions**  Energy buckets already include propulsion, hotel loads, comm duty, thermal survival, and control margin as needed.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  full plant fidelity, power survivability, thermal survivability, late-abort feasibility

## lawful_actuation_clf_cbf_qp.py

**V.1–V.3 · Lawful actuation governance CLF–CBF QP.** The supplied model uses a local single-integrator step in seconds. The objective is half the squared distance from nominal control plus separate quadratic penalties for barrier and stability slack. Each hazard is a point with exclusion radius `r_safe`. The quadratic barrier constraints make the feasible control region potentially nonconvex.

| Quantity | Definition |
|---|---|
| Barrier margin for hazard `i` | `h_i = ||x + dt*u - hazard_i||² - r_safe²` |
| Lyapunov value and derivative | `V = ||x - x_ref||² / 2` and `Vdot = (x - x_ref) · u` |
| Stability margin | `-alpha*V - Vdot` |
| Decision objective | `0.5*||u - u_nom||² + Gamma_cbf*delta_cbf² + Gamma_clf*delta_clf²` |

The four numerical helpers are `cbf_margin`, `clf_value`, `clf_vdot` and `clf_margin`. `lawful_control_qp(x, u_nom, hazards, r_safe, dt, u_bounds, Gamma=1e6, *, x_ref=None, alpha=1.0, Gamma_cbf=None, Gamma_clf=None, clf_required=True)` returns the bounded control, both nonnegative slacks, aggregate slack, margins, solver status and gate decisions. The reference is required by default. Explicitly passing `clf_required=False` permits a barrier-only solve when the reference is absent. The model returns `u_star` as a list. The original record classified this prototype as requiring optimization and identified `ledger.V.1_V.3` and `legacy_pcc_architecture_ledger.md#3` as historical trace references. The supplied test pointer was `tests/test_pcc_models.py::test_lawful_qp`.

### Portable solver and decision rules

The portable solver starts at the clipped nominal control. At each iteration it linearizes the barrier constraints, keeps the affine stability constraint and control bounds, and solves the resulting convex subproblem with a primal active-set projection. It uses one shared barrier slack for all hazards and a separate stability slack. At the exact center of a violated hazard it tries bounded axial perturbations to find a descent direction. Results depend on the local solution. The solver reports failure when its active-set or outer iteration limit is reached or its active constraints become numerically dependent.

On success the model recomputes margins at the returned control. A slack of at most `1e-7` and a corresponding margin of at least `-1e-7` satisfy that gate. `null_set_trigger(safe_without_slack)` and the result’s `null_set` field negate the combined gate. A solver failure returns the clipped nominal control, infinite slacks and `null_set=True`. A successful optimization can also produce `null_set=True` when it needs slack.

### Comparison with the supplied SciPy implementation

The replay includes 10 named cases and 120 seeded cases in one through three dimensions. The fixture file stores every input, the original SciPy output, and the observed portable output for each known difference. The regression suite uses an absolute tolerance of `1e-4` for source numeric comparisons and exact gate/status comparisons. It checks the separate portable baselines for the 14 known differences at `1e-8`. It also recomputes the constraints and verifies failure fallbacks. [Reference observations](clf_cbf_solver_reference.json) · [Regression suite](test_lawful_actuation_clf_cbf_qp.py)

| Observed result | Cases |
|---|---:|
| Both solvers converged | 118 |
| Jointly converged, all numeric fields within `1e-4` | 116 |
| Only the portable solver converged | 11 |
| Only SciPy SLSQP converged | 1 |
| Same final `null_set` decision | 130 of 130 |

Three of the 11 SciPy failure cases differed on the component `cbf_safe_without_slack` flag. The combined gate still failed in each. In `seed204-50` both solvers reported success at different local controls. The second control component was about `0.740186` for SLSQP and `-0.8` for the port. In `seed204-69` the controls agreed at the upper bound, with a CLF slack difference of about `0.01285`. The `slow_convergence` case exercises the portable iteration-limit fallback. These comparisons characterize the recorded cases.

The source oracle executed the supplied objective, constraints, SLSQP call, and decision logic. Its unavailable relative-base import and metadata constructor were bypassed for evaluation, with a local finite-positive input check. The packaged solver and its shared policy engine use the Python standard library. The oracle used SciPy 1.18.0 and NumPy 2.4.4.

Supplied source SHA-256: `425cf076d49dc41305b76ac5efccaa722aa3e42b29ea66c5cb1ccf8e9f6b6b38`.
