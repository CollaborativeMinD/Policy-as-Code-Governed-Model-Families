# Thermal timing authority

### Use cases

- Thermal throttling and deadline checks.
- Noncritical workload authority scaling.
- Recovery/rearm gating.

### Non-use cases

- Not silicon-vendor microarchitecture truth.
- Not a replacement for measured latency.

## Model files

- [clock_derate_fraction.py](clock_derate_fraction.py) — clock_derate_fraction
- [deadline_margin_under_derate.py](deadline_margin_under_derate.py) — deadline_margin_under_derate
- [recovery_hysteresis_margin.py](recovery_hysteresis_margin.py) — recovery_hysteresis_margin
- [thermal_authority_scale.py](thermal_authority_scale.py) — thermal_authority_scale

## Regression suites

- [test_thermal_timing_authority.py](test_thermal_timing_authority.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/clock_derate_fraction](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/clock_derate_fraction_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/deadline_margin_under_derate](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/deadline_margin_under_derate_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/recovery_hysteresis_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/recovery_hysteresis_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/thermal_authority_scale](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority/thermal_authority_scale_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
clock_derate_fraction.py
  compute_clock_derate_fraction = 0.75
  lambdified_unclipped = 6.0
deadline_margin_under_derate.py
  compute_deadline_margin_under_derate = 0.0
  lambdified = 1.25
recovery_hysteresis_margin.py
  compute_recovery_hysteresis_margin = 5.0
  lambdified = 1.0
thermal_authority_scale.py
  compute_thermal_authority_scale = 0.2
test_thermal_timing_authority.py: 4 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/thermal_timing_authority
```

<!-- end-observed-output -->

## clock_derate_fraction.py

### Model context from the archive

THERM-TIME-001 — Clock derate fraction.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression_unclipped()`
- `lambdified_unclipped()`
- `compute_clock_derate_fraction(temp_c: float, warning_temp_c: float, critical_temp_c: float, derate_gain: float, clock_floor_fraction: float)`

### Original formula record

- **Formula id**  THERM-TIME-001
- **Latex**  `u_T=clip((T-T_{warn})/(T_{crit}-T_{warn}),0,1);\phi_{clk}=clip(1-k_{clk}u_T,\phi_{floor},1)`
- **Family**  thermal_timing_authority
- **Name**  clock_derate_fraction

Additional reference comparisons during migration: 5.

## deadline_margin_under_derate.py

### Model context from the archive

THERM-TIME-002 — Deadline margin under derate.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_deadline_margin_under_derate(deadline_budget_ms: float, nominal_latency_ms: float, clock_derate_fraction: float)`

### Original formula record

- **Formula id**  THERM-TIME-002
- **Latex**  `m_{dead}=\tau_{deadline}-\tau_{nom}/\phi_{clk}`
- **Family**  thermal_timing_authority
- **Name**  deadline_margin_under_derate

Additional reference comparisons during migration: 5.

## recovery_hysteresis_margin.py

### Model context from the archive

THERM-AUTH-002 — Recovery hysteresis margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_recovery_hysteresis_margin(current_temp_c: float, rearm_temp_c: float)`

### Original formula record

- **Formula id**  THERM-AUTH-002
- **Latex**  `m_{hys}=T_{rearm}-T_{current}`
- **Family**  thermal_timing_authority
- **Name**  recovery_hysteresis_margin

Additional reference comparisons during migration: 5.

## thermal_authority_scale.py

### Model context from the archive

THERM-AUTH-001 — Thermal authority scale.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression_min_unclipped()`
- `compute_thermal_authority_scale(temp_c: float, warning_temp_c: float, critical_temp_c: float, deadline_margin_ms: float, deadline_budget_ms: float, authority_floor: float)`

### Original formula record

- **Formula id**  THERM-AUTH-001
- **Latex**  `\alpha_{auth}=clip(min((T_{crit}-T)/(T_{crit}-T_{warn}),m_{dead}/\tau_{deadline}),\alpha_{floor},1)`
- **Family**  thermal_timing_authority
- **Name**  thermal_authority_scale
