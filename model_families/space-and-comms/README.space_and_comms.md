# space_and_comm

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.space_and_comm.md`

## Why this family exists
Link closure, radar range, orbital timing, perturbation drift, and custody-transfer viability.

## Cross-domain use cases
space relay availability; over-the-horizon relay sanity; sensor coverage; track handoff timing.

## Optimal use
Use for first-pass sensing and comms geometry, relay planning, and space-layer timing support.

## Do not use when
Do not use as complete RF, SPICE, clutter, weather, or contested-spectrum truth.

## Canonical formulas in this family

- **C.1** `c_1__space_and_comm__communications_link_budget.py`: Communications link budget
  - Symbolic form: `P_r = P_t + G_t + G_r - L_p - L_a - L_s`
  - Why kept: Base compendium law split from shared module for direct lookup.
- **C.2** `c_2__space_and_comm__radar_range_equation.py`: Radar range equation
  - Symbolic form: `R_max = ((P_t G^2 λ^2 σ) / ((4π)^3 S_min L))^(1/4)`
  - Why kept: Base compendium law split from shared module for direct lookup.
- **C.3** `c_3__space_and_comm__orbital_mean_motion.py`: Orbital mean motion
  - Symbolic form: `n = sqrt(μ / a^3)`
  - Why kept: Base compendium law split from shared module for direct lookup.
- **C.4** `c_4__space_and_comm__j2_nodal_precession.py`: J2 nodal precession
  - Symbolic form: `Ω_dot = -(3/2) J2 n (R_E / p)^2 cos(i)`
  - Why kept: Base compendium law split from shared module for direct lookup.
- **C.6** `c_6__space_and_comm__handoff_survival_condition.py`: Handoff survival condition
  - Symbolic form: `t_handoff < t_coast_limit`
  - Why kept: Base compendium law canonicalized for searchability.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
