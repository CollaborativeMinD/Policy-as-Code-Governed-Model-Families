# Thermal environment validity

### Use cases

- Enclosure/cooling model validation.
- Twin-to-hardware mismatch detection.
- Cooling assumption audits.

### Non-use cases

- Not valid without steady-state measured data.
- Does not identify root cause.

## Model files

- [cooling_assumption_mismatch_margin.py](cooling_assumption_mismatch_margin.py) — cooling_assumption_mismatch_margin

## Regression suites

- [test_thermal_environment_validity.py](test_thermal_environment_validity.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_environment_validity/cooling_assumption_mismatch_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_environment_validity/cooling_assumption_mismatch_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
cooling_assumption_mismatch_margin.py
  compute_cooling_assumption_mismatch_margin = 0.5
  lambdified = 1.0
test_thermal_environment_validity.py: 1 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_environment_validity
```

<!-- end-observed-output -->

## cooling_assumption_mismatch_margin.py

### Model context from the archive

THERM-ENV-001 — Cooling assumption mismatch margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_cooling_assumption_mismatch_margin(measured_steady_temp_c: float, measured_ambient_c: float, measured_power_w: float, claimed_thermal_resistance_c_per_w: float, allowed_resistance_error_c_per_w: float)`

### Original formula record

- **Formula id**  THERM-ENV-001
- **Latex**  `m_{cool}=\Delta R_{allow}-|R_{th,measured}-R_{th,claimed}|`
- **Family**  thermal_environment_validity
- **Name**  cooling_assumption_mismatch_margin

Additional reference comparisons during migration: 5.
