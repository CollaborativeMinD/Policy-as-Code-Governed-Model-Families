# Space and comms

Link closure, radar range, orbital timing, perturbation drift, and custody-transfer viability.

### Optimal use

Use for first-pass sensing and comms geometry, relay planning, and space-layer timing support.

### Do not use when

Do not use as complete RF, SPICE, clutter, weather, or contested-spectrum truth.

## Model files

- [authority_lease_closure_margin.py](authority_lease_closure_margin.py) — Authority lease closure margin
- [communications_and_radar.py](communications_and_radar.py) — Communications link budget and radar range
- [covariance_weighted_fusion.py](covariance_weighted_fusion.py) — Covariance‑weighted sensor fusion
- [handoff_survival.py](handoff_survival.py) — Handoff survival condition
- [orbital_dynamics.py](orbital_dynamics.py) — Orbital mean motion and J2 nodal precession
- [sensor_actuator_delay_budget.py](sensor_actuator_delay_budget.py) — Sensor-to-actuator delay budget margin
- [volley_successor.py](volley_successor.py) — Volley successor synthesis update

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [space-and-comms/authority_lease_closure_margin](../../model_policy_engine/policies/space-and-comms/authority_lease_closure_margin_policy.toml)
- [space-and-comms/communications_and_radar](../../model_policy_engine/policies/space-and-comms/communications_and_radar_policy.toml)
- [space-and-comms/covariance_weighted_fusion](../../model_policy_engine/policies/space-and-comms/covariance_weighted_fusion_policy.toml)
- [space-and-comms/handoff_survival](../../model_policy_engine/policies/space-and-comms/handoff_survival_policy.toml)
- [space-and-comms/orbital_dynamics](../../model_policy_engine/policies/space-and-comms/orbital_dynamics_policy.toml)
- [space-and-comms/sensor_actuator_delay_budget](../../model_policy_engine/policies/space-and-comms/sensor_actuator_delay_budget_policy.toml)
- [space-and-comms/volley_successor](../../model_policy_engine/policies/space-and-comms/volley_successor_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
authority_lease_closure_margin.py
  compute_authority_lease_closure_margin = -5.199999999999999
communications_and_radar.py
  compute_received_power_db = -0.9
  compute_radar_range = 0.06480516386008059
covariance_weighted_fusion.py
  fuse_estimates = [[[1.1990995497748875, 0.015007503751875937], [0.015007503751875938, 0.7498749374687343]], [1.7843921960980489, 1.2601300650325162]]
handoff_survival.py
  check_handoff_survival = true
orbital_dynamics.py
  compute_mean_motion = 1.7888543819998317
  compute_j2_nodal_precession = -0.15355984614182427
sensor_actuator_delay_budget.py
  compute_sensor_to_actuator_delay_budget_margin = -5.199999999999999
volley_successor.py
  update_volley_successor = 0.30000000000000004
PASS space-and-comms
```

<!-- end-observed-output -->

## authority_lease_closure_margin.py

### Model context from the archive

C.6a - Authority lease closure margin.

This module computes whether an end-to-end authority path can close before the
lease or watchdog window expires.

### Entry points

- `compute_authority_lease_closure_margin(t_lease: float, t_sensor: float, t_transport: float, t_queue: float, t_compute: float, t_actuate: float, j_total: float, t_reconfig: float)`

### Original formula record

- **Formula id**  C.6a
- **Name**  Authority lease closure margin
- **Symbolic form**  `m_auth = T_lease - (T_sensor + T_transport + T_queue + T_compute + T_actuate + J_total + T_reconfig)`
- **Typed inputs**  `t_lease` (float), `t_sensor` (float), `t_transport` (float), `t_queue` (float), `t_compute` (float), `t_actuate` (float), `j_total` (float), `t_reconfig` (float)
- **Units**  `t_lease` (s), `t_sensor` (s), `t_transport` (s), `t_queue` (s), `t_compute` (s), `t_actuate` (s), `j_total` (s), `t_reconfig` (s), `output` (s)
- **Assumptions**  All timing terms are worst-case bounded terms measured or modeled on a common end-to-end authority path.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_authority_lease_closure_margin.py`, `rtm_link=lambda_laws.authority_lease_closure_margin`, `ssot_gate=notebooks/gate_authority_lease_closure_margin.ipynb`

## communications_and_radar.py

### Model context from the archive

C.1 and C.2 — Communications link budget and radar range

This module implements two capstone formulas:

* **Communications link budget**:

      P_r = P_t + G_t + G_r − L_p − L_a − L_s

  where quantities are expressed in decibels.

* **Radar range equation**:

      R_max = \Bigl(rac{P_t G² λ² σ}{(4π)³ S_min L}\Bigr)^{1/4},

  where ``P_t`` is transmit power, ``G`` is antenna gain, ``λ``
  wavelength, ``σ`` radar cross section, ``S_min`` minimum detectable
  signal, and ``L`` system losses (linear units).

### Entry points

- `compute_received_power_db(P_t_db: float, G_t_db: float, G_r_db: float, L_p_db: float, L_a_db: float, L_s_db: float)`
- `compute_radar_range(P_t: float, G: float, lambda_: float, sigma: float, S_min: float, L: float)`

### Original formula record

- **Formula id**  C.1/C.2
- **Name**  Communications link budget and radar range
- **Symbolic form**  `P_r = P_t + G_t + G_r − L_p − L_a − L_s; R_max = ((P_t G² λ² σ) / ((4π)³ S_min L))^(1/4)`
- **Typed inputs**  `P_t_db` (float), `G_t_db` (float), `G_r_db` (float), `L_p_db` (float), `L_a_db` (float), `L_s_db` (float), `P_t` (float), `G` (float), `lambda_` (float), `sigma` (float), `S_min` (float), `L` (float)
- **Units**  `P_t_db` (dB), `G_t_db` (dB), `G_r_db` (dB), `L_p_db` (dB), `L_a_db` (dB), `L_s_db` (dB), `P_r_db` (dB), `P_t` (W), `G` (unitless), `lambda_` (m), `sigma` (m²), `S_min` (W), `L` (unitless), `R_max` (m)
- **Assumptions**  dB quantities use a 10*log10 reference.  Radar range equation uses linear units.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_communications_and_radar.py::test_communications_and_radar`, `rtm_link=lambda_laws.communications_and_radar`, `ssot_gate=notebooks/gate_communications_and_radar.ipynb`

## covariance_weighted_fusion.py

### Model context from the archive

C.5 — Covariance‑weighted sensor fusion

This module fuses two independent sensor estimates based on their
covariance matrices:

    P⁻¹ = P₁⁻¹ + P₂⁻¹
    x̂ = P (P₁⁻¹ x̂₁ + P₂⁻¹ x̂₂).

This corresponds to the optimal linear combination under Gaussian
assumptions.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `fuse_estimates(P1: Sequence[Sequence[float]], P2: Sequence[Sequence[float]], x_hat1: Sequence[float], x_hat2: Sequence[float])`

### Original formula record

- **Formula id**  C.5
- **Name**  Covariance‑weighted sensor fusion
- **Symbolic form**  `P⁻¹ = P₁⁻¹ + P₂⁻¹ ; x̂ = P(P₁⁻¹ x̂₁ + P₂⁻¹ x̂₂)`
- **Typed inputs**  `P1` (Sequence[Sequence[float]]), `P2` (Sequence[Sequence[float]]), `x_hat1` (Sequence[float]), `x_hat2` (Sequence[float])
- **Units**  `P1` (state²), `P2` (state²), `x_hat1` (state), `x_hat2` (state), `output` (tuple)
- **Assumptions**  P1 and P2 must be symmetric positive definite and of matching dimension.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_covariance_weighted_fusion.py::test_covariance_fusion`, `rtm_link=lambda_laws.covariance_weighted_fusion`, `ssot_gate=notebooks/gate_covariance_weighted_fusion.ipynb`

Additional reference comparisons during migration: 50.

## handoff_survival.py

### Model context from the archive

C.6 — Handoff survival condition

This module checks whether the handoff from one system to another is
performed before a coasting time limit expires:

    t_handoff < t_coast_limit.

If the condition is not met, the handoff fails.

### Entry points

- `check_handoff_survival(t_handoff: float, t_coast_limit: float)`

### Original formula record

- **Formula id**  C.6
- **Name**  Handoff survival condition
- **Symbolic form**  `t_handoff < t_coast_limit`
- **Typed inputs**  `t_handoff` (float), `t_coast_limit` (float)
- **Units**  `t_handoff` (s), `t_coast_limit` (s), `output` (bool)
- **Assumptions**  t_handoff and t_coast_limit are non‑negative times.  If the handoff occurs at or after the coast limit, the operation fails.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_handoff_survival.py::test_handoff_survival`, `rtm_link=lambda_laws.handoff_survival`, `ssot_gate=notebooks/gate_handoff_survival.ipynb`

## orbital_dynamics.py

### Model context from the archive

C.3 and C.4 — Orbital dynamics laws

This module implements orbital mechanics formulas including the mean
motion and J2 nodal precession:

* **Mean motion**:

      n = sqrt(μ / a³),

  where μ is the gravitational parameter and a is the semi‑major axis.

* **J2 nodal precession**:

      Ω̇ = −(3/2) J₂ n (R_E / p)² cos(i),

  where J₂ is the second zonal harmonic, n is the mean motion, R_E
  is the Earth's radius, p is the semi‑latus rectum, and i is the
  inclination angle (radians).

### Entry points

- `compute_mean_motion(mu: float, a: float)`
- `compute_j2_nodal_precession(J2: float, n: float, R_E: float, p: float, i: float)`

### Original formula record

- **Formula id**  C.3/C.4
- **Name**  Orbital mean motion and J2 nodal precession
- **Symbolic form**  `n = sqrt(μ / a³); Ω̇ = −(3/2) J₂ n (R_E / p)² cos(i)`
- **Typed inputs**  `mu` (float), `a` (float), `J2` (float), `R_E` (float), `p` (float), `i` (float)
- **Units**  `mu` (m³/s²), `a` (m), `J2` (unitless), `R_E` (m), `p` (m), `i` (rad), `output` (tuple)
- **Assumptions**  a, R_E, p > 0; 0 ≤ i ≤ π.  The formulas assume a two‑body problem with J₂ perturbation.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_orbital_dynamics.py::test_orbital_dynamics`, `rtm_link=lambda_laws.orbital_dynamics`, `ssot_gate=notebooks/gate_orbital_dynamics.ipynb`

## sensor_actuator_delay_budget.py

### Model context from the archive

C.6b - Sensor-to-actuator delay budget margin.

This module computes whether a sensing, arbitration, and actuation chain stays
inside the maximum permissible closed-loop delay budget.

### Entry points

- `compute_sensor_to_actuator_delay_budget_margin(t_budget: float, t_sample_hold: float, t_transport: float, t_queue: float, t_compute: float, t_driver: float, t_actuate: float, j_total: float)`

### Original formula record

- **Formula id**  C.6b
- **Name**  Sensor-to-actuator delay budget margin
- **Symbolic form**  `m_loop = T_budget - (T_sample_hold + T_transport + T_queue + T_compute + T_driver + T_actuate + J_total)`
- **Typed inputs**  `t_budget` (float), `t_sample_hold` (float), `t_transport` (float), `t_queue` (float), `t_compute` (float), `t_driver` (float), `t_actuate` (float), `j_total` (float)
- **Units**  `t_budget` (s), `t_sample_hold` (s), `t_transport` (s), `t_queue` (s), `t_compute` (s), `t_driver` (s), `t_actuate` (s), `j_total` (s), `output` (s)
- **Assumptions**  The controlled hazard or guidance problem can be bounded by a maximum allowable sensing-to-actuation delay.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_sensor_to_actuator_delay_budget.py`, `rtm_link=lambda_laws.sensor_to_actuator_delay_budget`, `ssot_gate=notebooks/gate_sensor_to_actuator_delay_budget.ipynb`

## volley_successor.py

### Model context from the archive

C.7 — Volley successor synthesis update

This module provides a simple implementation of the successor update law:

    AFB_{k+1} = F(AFB_k, Δ_k, V_term,k),

where AFB stands for Active Fidelity Baseline, Δ_k is the weighted
divergence between reality and the twin at time ``k``, and V_term,k is
the terminal state vector magnitude.  In this simplified version, the
update function ``F`` is defined as:

    F(afb, delta, v_term) = afb + delta - v_term.

This is a placeholder for a more sophisticated update rule.

### Entry points

- `update_volley_successor(afb_k: float, delta_k: float, v_term_k: float)`

### Original formula record

- **Formula id**  C.7
- **Name**  Volley successor synthesis update
- **Symbolic form**  `AFB_{k+1} = F(AFB_k, Δ_k, V_term,k)`
- **Typed inputs**  `afb_k` (float), `delta_k` (float), `v_term_k` (float)
- **Units**  `afb_k` (unit), `delta_k` (unit), `v_term_k` (unit), `output` (unit)
- **Assumptions**  The update law is a placeholder.  In practice, a domain‑specific function should be used to update the active fidelity baseline.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_volley_successor.py::test_volley_successor`, `rtm_link=lambda_laws.volley_successor`, `ssot_gate=notebooks/gate_volley_successor.ipynb`
