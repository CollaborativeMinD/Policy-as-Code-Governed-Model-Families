# Thermal telemetry governance

### Use cases

- Thermal packet admission.
- Sensor plausibility and replay defense.
- Observability checks for fast heating events.
- Redundant sensor consistency.

### Non-use cases

- Does not estimate thermal state alone.
- Does not replace sensor calibration.

## Model files

- [freshness_at_use_margin.py](freshness_at_use_margin.py) — freshness_at_use_margin
- [multisensor_consistency_margin.py](multisensor_consistency_margin.py) — multisensor_consistency_margin
- [sampling_observability_margin.py](sampling_observability_margin.py) — sampling_observability_margin
- [slew_rate_plausibility_margin.py](slew_rate_plausibility_margin.py) — slew_rate_plausibility_margin

## Regression suites

- [test_thermal_telemetry_governance.py](test_thermal_telemetry_governance.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/freshness_at_use_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/freshness_at_use_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/multisensor_consistency_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/multisensor_consistency_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/sampling_observability_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/sampling_observability_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/slew_rate_plausibility_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance/slew_rate_plausibility_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
freshness_at_use_margin.py
  compute_freshness_at_use_margin = 3.0
  lambdified = 5.0
multisensor_consistency_margin.py
  compute_multisensor_consistency_margin = 2.0
  lambdified = -1.0
sampling_observability_margin.py
  compute_sampling_observability_margin = 5.0
  lambdified = -2.5
slew_rate_plausibility_margin.py
  compute_slew_rate_plausibility_margin = 1.0
  lambdified = 4.75
test_thermal_telemetry_governance.py: 4 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_telemetry_governance
```

<!-- end-observed-output -->

## freshness_at_use_margin.py

### Model context from the archive

THERM-TELEM-001 — Freshness at use margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_freshness_at_use_margin(use_time_s: float, sample_time_s: float, freshness_budget_s: float)`

### Original formula record

- **Formula id**  THERM-TELEM-001
- **Latex**  `m_{fresh}=\tau_{fresh}-(t_{use}-t_{sample})`
- **Family**  thermal_telemetry_governance
- **Name**  freshness_at_use_margin

Additional reference comparisons during migration: 5.

## multisensor_consistency_margin.py

### Model context from the archive

THERM-TELEM-004 — Multisensor consistency margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_multisensor_consistency_margin(sensor_temps_c: Sequence[float], allowed_spread_c: float)`

### Original formula record

- **Formula id**  THERM-TELEM-004
- **Latex**  `m_{cons}=\Delta T_{tol}-\max_i|T_i-median(T)|`
- **Family**  thermal_telemetry_governance
- **Name**  multisensor_consistency_margin

Additional reference comparisons during migration: 5.

## sampling_observability_margin.py

### Model context from the archive

THERM-TELEM-003 — Sampling observability margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_sampling_observability_margin(thermal_time_constant_s: float, sample_period_s: float, min_samples_per_time_constant: float)`

### Original formula record

- **Formula id**  THERM-TELEM-003
- **Latex**  `m_{obs}=\tau_{th}/N_{min}-\Delta t_{sample}`
- **Family**  thermal_telemetry_governance
- **Name**  sampling_observability_margin

Additional reference comparisons during migration: 5.

## slew_rate_plausibility_margin.py

### Model context from the archive

THERM-TELEM-002 — Slew rate plausibility margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_slew_rate_plausibility_margin(temp_prev_c: float, temp_curr_c: float, dt_s: float, max_allowed_slew_c_per_s: float)`

### Original formula record

- **Formula id**  THERM-TELEM-002
- **Latex**  `m_{slew}=s_{max}-|dT/dt|`
- **Family**  thermal_telemetry_governance
- **Name**  slew_rate_plausibility_margin

Additional reference comparisons during migration: 5.
