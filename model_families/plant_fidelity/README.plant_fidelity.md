# plant_fidelity

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.plant_fidelity.md`

## Why this family exists
Higher-fidelity systems-level plant laws for coupled rigid-body motion, control allocation residuals, curvature feasibility, and truth-conditioned speed closure.

## Cross-domain use cases
hypersonic body motion; torpedo turn feasibility; spacecraft terminal approach; multirotor residual control authority.

## Optimal use
Use when translational-only dynamics are too weak and you need coupled rigid-body or degraded authority realism.

## Do not use when
Do not mistake these for CFD, hydro, plume, soil, aeroelastic, or certification-grade truth.

## Canonical formulas in this family

- **PLANT-FID-001** `plant_fid_001__plant_fidelity__coupled_rigid_body_6_dof_propagation.py`: Coupled rigid-body 6-DOF propagation
  - Symbolic form: `r_dot = v; m v_dot = R(q) f_B + f_env + m g; J omega_dot = tau_B + tau_env - omega x (J omega); q_dot = 0.5 Omega(omega) q`
  - Why kept: Cross-domain 6-DOF rigid-body step law.
  - Merged from: M3-2A-COUPLED-6DOF-RIGID-BODY, PF-001-RIGID-BODY-WRENCH-RESPONSE, PROP-M3.2_six_dof_rigid_body_state_propagation
- **PLANT-FID-002** `plant_fid_002__plant_fidelity__control_allocation_residual_under_bounded_actuators.py`: Control allocation residual under bounded actuators
  - Symbolic form: `r_alloc = ||w_d − B sat(B⁺ w_d)||_2`
  - Why kept: Bounded-actuator residual authority is a reusable primitive across vehicles.
  - Merged from: AR-002-CONTROL-ALLOCATION-RESIDUAL, D1-2-CONTROL-ALLOCATION-RESIDUAL-AUTHORITY, M3-2B-CONTROL-ALLOCATION-AUTHORITY-MARGIN, PROP-M3.3_degraded_control_allocation_effectiveness_law
- **PLANT-FID-003** `plant_fid_003__plant_fidelity__truth_conditioned_safe_velocity_margin.py`: Truth-conditioned safe velocity margin
  - Symbolic form: `d_eff = d_hazard − vτ_lat − σ_terrain − 0.5r_map − σ_loc; v_safe = sqrt(max(2a_eff d_eff,0)); m_v = v_safe − v`
  - Why kept: Binds speed to map/terrain truth quality instead of assuming perfect knowledge.
- **PLANT-FID-004** `plant_fid_004__plant_fidelity__pf_002_curvature_feasibility_margin.py`: PF-002 - curvature_feasibility_margin
  - Symbolic form: `m_kappa = a_lat_avail / v^2 - kappa_req`
  - Why kept: Broad path-feasibility primitive for land, air, maritime, and docking trajectories.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
