# Thermal

## Subdirectories

- [thermal_truth](thermal_truth/README.md)

## Model files

- [thermal_margin.py](thermal_margin.py) — Thermal margin
- [time_to_thermal_violation.py](time_to_thermal_violation.py) — Time to thermal violation

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_margin](../../../model_policy_engine/policies/hardware_viability/thermal/thermal_margin_policy.toml)
- [hardware_viability/thermal/time_to_thermal_violation](../../../model_policy_engine/policies/hardware_viability/thermal/time_to_thermal_violation_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
thermal_margin.py
  compute_thermal_margin = 30.0
time_to_thermal_violation.py
  compute_time_to_thermal_violation = 50.0
PASS hardware_viability/thermal
```

<!-- end-observed-output -->

## thermal_margin.py

### Model context from the archive

HW-THERM-001 — thermal margin.

### Entry points

- `compute_thermal_margin(current_temp_c: float, t_crit_c: float)`

### Original formula record

- **Formula id**  HW-THERM-001
- **Name**  Thermal margin
- **Symbolic form**  `m_T = T_crit - T`
- **Typed inputs**  `current_temp_c` (float), `t_crit_c` (float)
- **Units**  `current_temp_c` (C), `t_crit_c` (C), `output` (C)
- **Assumptions**  Use when current temperature and the governing critical temperature are expressed in the same scale. Positive margin means thermal headroom remains; non-positive margin means thermal corpse-threshold breach.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_therm_001__hardware_viability_governance__thermal_margin`, `ssot_gate=notebooks/hw_therm_001__hardware_viability_governance__thermal_margin.ipynb`

## time_to_thermal_violation.py

### Model context from the archive

HW-THERM-002 — time to thermal violation.

### Entry points

- `compute_time_to_thermal_violation(current_temp_c: float, t_crit_c: float, dT_dt_c_per_s: float)`

### Original formula record

- **Formula id**  HW-THERM-002
- **Name**  Time to thermal violation
- **Symbolic form**  `H_T = (T_crit - T) / dT_dt, dT_dt > 0 ; +inf otherwise`
- **Typed inputs**  `current_temp_c` (float), `t_crit_c` (float), `dT_dt_c_per_s` (float)
- **Units**  `current_temp_c` (C), `t_crit_c` (C), `dT_dt_c_per_s` (C/s), `output` (s)
- **Assumptions**  Short-horizon predictive law. Use when dT/dt is locally meaningful and positive. Treat the result as an earliest credible warning horizon, not long-range thermal prophecy.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_hardware_viability_governance.py`, `rtm_link=lambda_laws.hw_therm_002__hardware_viability_governance__time_to_thermal_violation`, `ssot_gate=notebooks/hw_therm_002__hardware_viability_governance__time_to_thermal_violation.ipynb`
