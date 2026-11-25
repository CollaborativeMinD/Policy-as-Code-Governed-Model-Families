# Thermal rc envelope

### Use cases

- First-order thermal screening.
- Runtime headroom estimates.
- Cooldown hysteresis and rearm timing.

### Non-use cases

- Not finite-element analysis.
- Not certification-grade thermal prediction.
- Not valid without calibrated resistance/time constants.

## Model files

- [cooldown_time_to_rearm.py](cooldown_time_to_rearm.py) — cooldown_time_to_rearm
- [equilibrium_temperature_under_load.py](equilibrium_temperature_under_load.py) — equilibrium_temperature_under_load
- [time_to_temperature_threshold.py](time_to_temperature_threshold.py) — time_to_temperature_threshold

## Regression suites

- [test_thermal_rc_envelope.py](test_thermal_rc_envelope.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/cooldown_time_to_rearm](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/cooldown_time_to_rearm_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/equilibrium_temperature_under_load](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/equilibrium_temperature_under_load_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/time_to_temperature_threshold](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope/time_to_temperature_threshold_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
cooldown_time_to_rearm.py
  compute_cooldown_time_to_rearm = 78.84573603642701
  lambdified = 78.84573603642701
equilibrium_temperature_under_load.py
  compute_equilibrium_temperature_under_load = 45.0
  lambdified = 14.0
time_to_temperature_threshold.py
  compute_time_to_temperature_threshold = 87.54687373538998
  lambdified = 87.54687373538998
  compute_time_to_temperature_threshold = Infinity
test_thermal_rc_envelope.py: 3 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_rc_envelope
```

<!-- end-observed-output -->

## cooldown_time_to_rearm.py

### Model context from the archive

THERM-RC-003 — Cooldown time to rearm.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_cooldown_time_to_rearm(start_temp_c: float, rearm_temp_c: float, cool_equilibrium_temp_c: float, cooldown_time_constant_s: float)`

### Original formula record

- **Formula id**  THERM-RC-003
- **Latex**  `t_{rearm}=-\tau_{cool}\ln\frac{T_{rearm}-T_{eq,cool}}{T_{start}-T_{eq,cool}}`
- **Family**  thermal_rc_envelope
- **Name**  cooldown_time_to_rearm

Additional reference comparisons during migration: 5.

## equilibrium_temperature_under_load.py

### Model context from the archive

THERM-RC-001 — Equilibrium temperature under load.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_equilibrium_temperature_under_load(ambient_temp_c: float, effective_power_w: float, thermal_resistance_c_per_w: float)`

### Original formula record

- **Formula id**  THERM-RC-001
- **Latex**  `T_{eq}=T_{amb}+P_{eff}R_{th}`
- **Family**  thermal_rc_envelope
- **Name**  equilibrium_temperature_under_load

Additional reference comparisons during migration: 5.

## time_to_temperature_threshold.py

### Model context from the archive

THERM-RC-002 — Time to temperature threshold.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_time_to_temperature_threshold(initial_temp_c: float, threshold_temp_c: float, equilibrium_temp_c: float, thermal_time_constant_s: float)`

### Original formula record

- **Formula id**  THERM-RC-002
- **Latex**  `t_{thr}=-\tau_{th}\ln\frac{T_{thr}-T_{eq}}{T_0-T_{eq}}`
- **Family**  thermal_rc_envelope
- **Name**  time_to_temperature_threshold

Additional reference comparisons during migration: 6.
