# Thermal two layer

Reduced-order two-node thermal forcing and transient stepping for fast skin and slower substrate separation.

### Use cases

- Sunlit skin over insulated electronics.
- Engine-bay skin vs electronics tray.
- Low-compute thermal twins and what-if controller analysis under illumination changes.

### Non-use cases

- Do not treat two-node dynamics as FEA or certification evidence.
- Do not use non-positive heat capacities or negative physical geometry terms.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [surface_radiative_forcing_density.py](surface_radiative_forcing_density.py) — surface_radiative_forcing_density
- [two_layer_temperature_step.py](two_layer_temperature_step.py) — two_layer_temperature_step

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_two_layer/surface_radiative_forcing_density](../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_two_layer/surface_radiative_forcing_density_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_two_layer/two_layer_temperature_step](../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_two_layer/two_layer_temperature_step_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
surface_radiative_forcing_density.py
  compute_surface_radiative_forcing_density = 200.0
two_layer_temperature_step.py
  compute_two_layer_temperature_step = [19.0, 10.5]
PASS hardware_viability/thermal/thermal_truth/thermal_two_layer
```

<!-- end-observed-output -->

## surface_radiative_forcing_density.py

### Model context from the archive

THERM-2L-001 — surface_radiative_forcing_density

Purpose
-------
Separates illumination forcing on exposed skin from deeper electronics state.

Assumptions
-----------
Reduced-order radiative forcing term for patch-level thermal forcing. Not a full finite-element model.

### Entry points

- `compute_surface_radiative_forcing_density(alpha: float, area_m2: float, insolation_w_m2: float, epsilon: float, T_skin_c: float, T_env_c: float)`

### Original formula record

- **Formula id**  THERM-2L-001
- **Family**  thermal_two_layer
- **Name**  surface_radiative_forcing_density
- **Symbolic form**  `q_surf = alpha*A*G - epsilon*sigma*A*(T_skin^4 - T_env^4)`
- **Typed inputs**  `alpha` (float), `A` (float), `G` (float), `epsilon` (float), `T_skin_c` (float), `T_env_c` (float)
- **Units**  `alpha` (unitless), `A` (m^2), `G` (W/m^2), `epsilon` (unitless), `T_skin_c` (C), `T_env_c` (C), `output` (W)
- **Assumptions**  Reduced-order radiative forcing term for patch-level thermal forcing. Not a full finite-element model.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Separates illumination forcing on exposed skin from deeper electronics state.
- **Status**  proposed_for_future_builds

## two_layer_temperature_step.py

### Model context from the archive

THERM-2L-002 — two_layer_temperature_step

Purpose
-------
Lets the twin preserve fast skin dynamics and slower substrate dynamics without pretending they are the same node.

Assumptions
-----------
First-order two-node transient. Useful for governed refinement and failure discovery, not certification.

### Entry points

- `compute_surface_radiative_forcing_density(alpha: float, area_m2: float, insolation_w_m2: float, epsilon: float, T_skin_c: float, T_env_c: float)`
- `compute_two_layer_temperature_step(skin_temp_c: float, substrate_temp_c: float, env_temp_c: float, insolation_w_m2: float, alpha: float, epsilon: float, area_m2: float, skin_heat_capacity_j_per_c: float, substrate_heat_capacity_j_per_c: float, conduction_w_per_c: float, internal_power_w: float, heater_power_w: float, dt_s: float)`

### Original formula record

- **Formula id**  THERM-2L-002
- **Family**  thermal_two_layer
- **Name**  two_layer_temperature_step
- **Symbolic form**  `dT_skin/dt=(q_absorb-q_rad-q_cond)/C_skin ; dT_sub/dt=(q_cond+q_internal+q_heater)/C_sub`
- **Typed inputs**  `skin_temp_c` (float), `substrate_temp_c` (float), `env_temp_c` (float), `insolation_w_m2` (float), `alpha` (float), `epsilon` (float), `area_m2` (float), `skin_heat_capacity_j_per_c` (float), `substrate_heat_capacity_j_per_c` (float), `conduction_w_per_c` (float), `internal_power_w` (float), `heater_power_w` (float), `dt_s` (float)
- **Units**  `skin_temp_c` (C), `substrate_temp_c` (C), `env_temp_c` (C), `insolation_w_m2` (W/m^2), `area_m2` (m^2), `skin_heat_capacity_j_per_c` (J/C), `substrate_heat_capacity_j_per_c` (J/C), `conduction_w_per_c` (W/C), `internal_power_w` (W), `heater_power_w` (W), `dt_s` (s), `output` ((C,C))
- **Assumptions**  First-order two-node transient. Useful for governed refinement and failure discovery, not certification.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Lets the twin preserve fast skin dynamics and slower substrate dynamics without pretending they are the same node.
- **Status**  proposed_for_future_builds
