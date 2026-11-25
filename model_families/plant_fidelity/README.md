# Plant fidelity

Higher-fidelity systems-level plant laws for coupled rigid-body motion, control allocation residuals, curvature feasibility, and truth-conditioned speed closure.

### Optimal use

Use when translational-only dynamics are too weak and you need coupled rigid-body or degraded authority realism.

### Do not use when

Do not mistake these for CFD, hydro, plume, soil, aeroelastic, or certification-grade truth.

## Subdirectories

- [contact_dynamics](contact_dynamics/README.md)
- [plant_abortability](plant_abortability/README.md)

## Model files

- [Control-allocation-residual.py](Control-allocation-residual.py) — Control allocation residual under bounded actuators
- [Coupled rigid-body 6-DOF propagation.py](Coupled%20rigid-body%206-DOF%20propagation.py) — Coupled rigid-body 6-DOF propagation
- [curvature_feasibility_margin.py](curvature_feasibility_margin.py) — curvature_feasibility_margin
- [newton_euler_translational.py](newton_euler_translational.py) — Newton–Euler translational plant law
- [Truth-conditioned-safe-velocity-margin.py](Truth-conditioned-safe-velocity-margin.py) — Truth-conditioned safe velocity margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [plant_fidelity/Control-allocation-residual](../../model_policy_engine/policies/plant_fidelity/Control-allocation-residual_policy.toml)
- [plant_fidelity/Coupled rigid-body 6-DOF propagation](../../model_policy_engine/policies/plant_fidelity/Coupled%20rigid-body%206-DOF%20propagation_policy.toml)
- [plant_fidelity/curvature_feasibility_margin](../../model_policy_engine/policies/plant_fidelity/curvature_feasibility_margin_policy.toml)
- [plant_fidelity/newton_euler_translational](../../model_policy_engine/policies/plant_fidelity/newton_euler_translational_policy.toml)
- [plant_fidelity/Truth-conditioned-safe-velocity-margin](../../model_policy_engine/policies/plant_fidelity/Truth-conditioned-safe-velocity-margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
Control-allocation-residual.py
  compute_control_allocation_residual = 2.23606797749979
  compute_control_allocation_residual = 2.23606797749979
Coupled rigid-body 6-DOF propagation.py
  compute_rigid_body_6dof_step = {"angular_acceleration": [-0.029999999999999985, 0.35333333333333333, -0.005000000000000001], "linear_acceleration": [1.0, 0.0, 0.0], "omega": [0.097, 0.23533333333333334, 0.2995], "position": [1.0, 2.1, 3.0], "quaternion": [0.9998250459241057, 0.004999125229620529, 0.009998250459241059, 0.014997375688861584], "velocity": [0.1, 1.0, 0.0]}
curvature_feasibility_margin.py
  compute_curvature_feasibility_margin = 3.249999999999999
newton_euler_translational.py
  compute_translational_acceleration = 1.209
Truth-conditioned-safe-velocity-margin.py
  compute_truth_conditioned_safe_velocity_margin = -0.5
PASS plant_fidelity
```

<!-- end-observed-output -->

## Control-allocation-residual.py

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

Additional reference comparisons during migration: 185.

## Coupled rigid-body 6-DOF propagation.py

### Model context from the archive

M3.2a — Coupled rigid-body 6-DOF propagation

Broad plant law for autonomous vehicles with coupled translational and rotational motion.
Quaternion convention is scalar-first: [q0, q1, q2, q3].

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_rigid_body_6dof_step(position: Sequence[float], velocity: Sequence[float], quaternion: Sequence[float], omega: Sequence[float], mass: float, inertia: Sequence[Sequence[float]], body_force: Sequence[float], body_torque: Sequence[float], dt: float, env_force: Optional[Sequence[float]]=None, env_torque: Optional[Sequence[float]]=None, gravity: Optional[Sequence[float]]=None)`

### Original formula record

- **Formula id**  M3.2a
- **Name**  Coupled rigid-body 6-DOF propagation
- **Family**  Plant fidelity
- **Symbolic form**  `r_dot = v; m v_dot = R(q) f_B + f_env + m g; J omega_dot = tau_B + tau_env - omega x (J omega); q_dot = 0.5 Omega(omega) q`
- **Typed inputs**  `position` (Sequence[float]), `velocity` (Sequence[float]), `quaternion` (Sequence[float]), `omega` (Sequence[float]), `mass` (float), `inertia` (Sequence[Sequence[float]]), `body_force` (Sequence[float]), `body_torque` (Sequence[float]), `dt` (float)
- **Units**  `position` (m), `velocity` (m/s), `quaternion` (unitless), `omega` (rad/s), `mass` (kg), `inertia` (kg*m^2), `body_force` (N), `body_torque` (N*m), `dt` (s), `output` (state_dict)
- **Assumptions**  Rigid body, scalar-first unit quaternion, constant inputs over dt, and Euler forward integration for the proposal stage.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype

Additional reference comparisons during migration: 50.

## curvature_feasibility_margin.py

### Model context from the archive

PF-002 - curvature_feasibility_margin

Checks whether the platform can physically follow a demanded path curvature at the current speed.
This is reusable across aircraft, ground robots, marine craft, and surface-relative orbital proximity paths.

### Entry points

- `compute_curvature_feasibility_margin(speed_m_s: float, required_curvature_inv_m: float, available_lateral_accel_m_s2: float)`

### Original formula record

- **Formula id**  PF-002
- **Family**  plant_fidelity
- **Name**  curvature_feasibility_margin
- **Symbolic form**  `m_kappa = a_lat_avail / v^2 - kappa_req`
- **Typed inputs**  `speed_m_s` (float), `required_curvature_inv_m` (float), `available_lateral_accel_m_s2` (float)
- **Units**  `speed_m_s` (m/s), `required_curvature_inv_m` (1/m), `available_lateral_accel_m_s2` (m/s^2), `output` (1/m)
- **Assumptions**  Forward-speed path-following regime; speed and available lateral acceleration are strictly positive.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Weak areas hit**  full plant fidelity, terrain truth, hardware-closed timing and authority seams
- **Multi use role**  Turns route geometry into a hard physical feasibility check instead of a vibes-based waypoint promise.

## newton_euler_translational.py

### Model context from the archive

M3.1a — Newton–Euler translational plant law

This module implements the translational dynamics law for a point
mass subject to thrust, disturbance, aerodynamic drag and gravity:

    m(t) \dot{v} = F_thrust(u) + F_dist(w) − F_drag(v, ρ, C_d, A) − m(t) g.

Assuming scalar (one‑dimensional) motion, the acceleration ``v̇`` is
computed as

    v̇ = (F_thrust + F_dist − F_drag) / m − g.

The drag force is modeled as

    F_drag = 0.5 · ρ · C_d · A · v · |v|,

which acts opposite the direction of velocity.

### Entry points

- `compute_translational_acceleration(mass: float, thrust: float, disturbance: float, velocity: float, rho: float, C_d: float, area: float, g: float)`

### Original formula record

- **Formula id**  M3.1a
- **Name**  Newton–Euler translational plant law
- **Symbolic form**  `m(t) v̇ = F_thrust(u) + F_dist(w) − F_drag(v, ρ, C_d, A) − m(t) g`
- **Typed inputs**  `mass` (float), `thrust` (float), `disturbance` (float), `velocity` (float), `rho` (float), `C_d` (float), `area` (float), `g` (float)
- **Units**  `mass` (kg), `thrust` (N), `disturbance` (N), `velocity` (m/s), `rho` (kg/m³), `C_d` (unitless), `area` (m²), `g` (m/s²), `output` (m/s²)
- **Assumptions**  Motion is along a single axis.  Thrust and disturbance forces are applied along this axis.  Drag follows a quadratic model and acts opposite the velocity direction.  Mass must be positive.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_newton_euler_translational.py::test_acceleration`, `rtm_link=lambda_laws.newton_euler_translational`, `ssot_gate=notebooks/gate_newton_euler_translational.ipynb`

## Truth-conditioned-safe-velocity-margin.py

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
