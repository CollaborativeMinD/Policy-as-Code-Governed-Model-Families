# Contact dynamics

Touchdown, docking, berthing, and collision boundary events fail when impact energy exceeds what the structure or interface can dissipate.

### Optimal use

Use when the dominant risk is whether contact remains survivable after translational, drop, and rotational energy are counted honestly.

### Do not use when

Do not use when the real problem is guidance, terrain truth, or authority gating upstream of contact.

## Model files

- [contact_energy_margin.py](contact_energy_margin.py) — contact_energy_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [plant_fidelity/contact_dynamics/contact_energy_margin](../../../model_policy_engine/policies/plant_fidelity/contact_dynamics/contact_energy_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
contact_energy_margin.py
  compute_contact_energy_margin = 7.053669999999999
PASS plant_fidelity/contact_dynamics
```

<!-- end-observed-output -->

## contact_energy_margin.py

### Model context from the archive

PF-004 - contact_energy_margin

Checks whether touchdown, berth capture, or docking contact energy stays inside the system's dissipatable envelope.
This catches fake-safe arrivals that look calm in position space but hit hard in energy space.

### Entry points

- `compute_contact_energy_margin(mass_kg: float, relative_speed_m_s: float, drop_height_m: float, inertia_diag_kg_m2: Sequence[float], omega_body_rad_s: Sequence[float], max_dissipatable_energy_j: float, gravity_m_s2: float=9.80665)`

### Original formula record

- **Formula id**  PF-004
- **Family**  plant_fidelity
- **Name**  contact_energy_margin
- **Symbolic form**  `m_contact = E_diss_max - (0.5*m*v_rel^2 + m*g*h_drop + 0.5*omega^T*I*omega)`
- **Typed inputs**  `mass_kg` (float), `relative_speed_m_s` (float), `drop_height_m` (float), `inertia_diag_kg_m2` (Sequence[float]), `omega_body_rad_s` (Sequence[float]), `max_dissipatable_energy_j` (float), `gravity_m_s2` (float)
- **Units**  `mass_kg` (kg), `relative_speed_m_s` (m/s), `drop_height_m` (m), `inertia_diag_kg_m2` (kg*m^2), `omega_body_rad_s` (rad/s), `max_dissipatable_energy_j` (J), `gravity_m_s2` (m/s^2), `output` (J)
- **Assumptions**  Principal-axis inertia approximation; drop_height_m is the unrecovered closing height component that still becomes contact energy.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Weak areas hit**  full plant fidelity, terrain truth, power and thermal survivability
- **Multi use role**  Unifies linear, rotational, and vertical contact hazard into one honest energy margin.
