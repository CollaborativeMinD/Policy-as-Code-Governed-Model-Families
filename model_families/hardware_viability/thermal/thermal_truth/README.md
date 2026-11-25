# Thermal truth

## Subdirectories

- [thermal_cross_domain_models](thermal_cross_domain_models/README.md)
- [thermal_distortion](thermal_distortion/README.md)
- [thermal_qualification](thermal_qualification/README.md)
- [thermal_two_layer](thermal_two_layer/README.md)

## Model files

- [cycle_energy_reserve_margin.py](cycle_energy_reserve_margin.py) — Duty-cycle energy reserve margin law
- [thermal_timing_derate_margin.py](thermal_timing_derate_margin.py) — Thermal timing derate margin law
- [two_layer_thermal_distortion.py](two_layer_thermal_distortion.py) — Two-layer thermal distortion law

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/cycle_energy_reserve_margin](../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/cycle_energy_reserve_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_timing_derate_margin](../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_timing_derate_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/two_layer_thermal_distortion](../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/two_layer_thermal_distortion_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
cycle_energy_reserve_margin.py
  compute_duty_cycle_energy_reserve_margin = -0.40000000000000013
thermal_timing_derate_margin.py
  compute_thermal_timing_derate_margin = -0.09999999999999998
two_layer_thermal_distortion.py
  compute_two_layer_thermal_dynamics = {"core_temp_dot": 0.9999999999999999, "surface_temp_dot": -0.010101010101010104, "thermal_distortion_index": 0.09999999999999998}
PASS hardware_viability/thermal/thermal_truth
```

<!-- end-observed-output -->

## cycle_energy_reserve_margin.py

### Model context from the archive

P1.1 — Duty-cycle energy reserve margin law

Purpose
-------
Estimates how much energy remains after projected mission loads, comm duty,
thermal survival loads, and contingency reserve are paid for. This law matters
because real vehicles do not care how elegant the planner was once the battery
becomes a historical artifact.

### Entry points

- `compute_duty_cycle_energy_reserve_margin(energy_stored: float, power_segments: Sequence[float], duration_segments: Sequence[float], thermal_hold_energy: float=0.0, contingency_energy: float=0.0)`

### Original formula record

- **Formula id**  P1.1
- **Name**  Duty-cycle energy reserve margin law
- **Symbolic form**  `m_power = E_store - Σ(P_i Δt_i) - E_thermal_hold - E_contingency`
- **Typed inputs**  `energy_stored` (float), `power_segments` (Sequence[float]), `duration_segments` (Sequence[float]), `thermal_hold_energy` (float), `contingency_energy` (float)
- **Units**  `energy_stored` (J), `power_segments` (W), `duration_segments` (s), `thermal_hold_energy` (J), `contingency_energy` (J), `output` (J)
- **Assumptions**  Power and duration vectors are aligned. Includes propulsion, sensing, compute, relay, hotel loads, or any other mission duty bucket.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  power survivability, thermal survivability, contested edge-network realism, mission-demand conflict

## thermal_timing_derate_margin.py

### Model context from the archive

P1.3 — Thermal timing derate margin law

Purpose
-------
Transforms temperature into execution-time risk. Hot compute is not just a
materials problem; it is a schedule problem, a stale-data problem, and eventually
an authority problem when deadlines slip past the lease window.

### Entry points

- `compute_thermal_timing_derate_margin(deadline: float, base_exec_time: float, core_temp: float, temp_threshold: float, derate_gain: float, io_jitter: float=0.0, guard_band: float=0.0)`

### Original formula record

- **Formula id**  P1.3
- **Name**  Thermal timing derate margin law
- **Symbolic form**  `m_t = T_deadline - (t_base * (1 + k max(0, T_core-T_th)) + t_io + t_guard)`
- **Typed inputs**  `deadline` (float), `base_exec_time` (float), `core_temp` (float), `temp_threshold` (float), `derate_gain` (float), `io_jitter` (float), `guard_band` (float)
- **Units**  `deadline` (s), `base_exec_time` (s), `core_temp` (K), `temp_threshold` (K), `derate_gain` (1/K), `io_jitter` (s), `guard_band` (s), `output` (s)
- **Assumptions**  Execution derating is monotonic with thermal excess; suitable for bounded runtime screening even when the exact throttling curve is platform specific.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  power and thermal survivability, hardware-closed timing, temporal coherence, authority seams

## two_layer_thermal_distortion.py

### Model context from the archive

P1.2 — Two-layer thermal distortion law

Purpose
-------
Models core-surface thermal separation with an output distortion index. This is
broad enough for batteries, processors, avionics boxes, relay payloads, and edge
compute modules where the outer shell still looks fine while the interior is busy
becoming a problem.

### Entry points

- `compute_two_layer_thermal_dynamics(core_temp: float, surface_temp: float, ambient_temp: float, heat_generation: float, core_heat_capacity: float, surface_heat_capacity: float, core_surface_resistance: float, surface_ambient_resistance: float, alpha: float=1.0, beta: float=1.0, nominal_temp: float=298.15)`

### Original formula record

- **Formula id**  P1.2
- **Name**  Two-layer thermal distortion law
- **Symbolic form**  `C_c T_c_dot = Q_gen + (T_s - T_c)/R_c ; C_s T_s_dot = (T_f - T_s)/R_u - (T_s - T_c)/R_c ; I_td = α max(0, T_c-T_nom) + β |T_c-T_s|`
- **Typed inputs**  `core_temp` (float), `surface_temp` (float), `ambient_temp` (float), `heat_generation` (float), `core_heat_capacity` (float), `surface_heat_capacity` (float), `core_surface_resistance` (float), `surface_ambient_resistance` (float), `alpha` (float), `beta` (float), `nominal_temp` (float)
- **Units**  `core_temp` (K), `surface_temp` (K), `ambient_temp` (K), `heat_generation` (W), `core_heat_capacity` (J/K), `surface_heat_capacity` (J/K), `core_surface_resistance` (K/W), `surface_ambient_resistance` (K/W), `nominal_temp` (K), `output` (K/s derivatives and unitless distortion index)
- **Assumptions**  Two-node lumped approximation; dominant for small embedded assets or reduced-order runtime estimation.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  power and thermal survivability, thermal distortion, silent degradation laws, timing margin erosion
