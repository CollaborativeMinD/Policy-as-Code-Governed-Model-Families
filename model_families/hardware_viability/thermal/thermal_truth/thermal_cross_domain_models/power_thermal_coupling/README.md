# Power thermal coupling

### Use cases

- Bursty compute/radio/sensor/heater load modeling.
- Thermal margin from mixed duty cycles.
- Converter loss thermal screening.

### Non-use cases

- Not a full power-network model.
- Not valid without characterized efficiency and thermal resistance.

## Model files

- [conversion_loss_temperature_margin.py](conversion_loss_temperature_margin.py) — conversion_loss_temperature_margin
- [duty_cycle_temperature_margin.py](duty_cycle_temperature_margin.py) — duty_cycle_temperature_margin
- [effective_duty_cycle_power.py](effective_duty_cycle_power.py) — effective_duty_cycle_power

## Regression suites

- [test_power_thermal_coupling.py](test_power_thermal_coupling.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/conversion_loss_temperature_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/conversion_loss_temperature_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/duty_cycle_temperature_margin](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/duty_cycle_temperature_margin_policy.toml)
- [hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/effective_duty_cycle_power](../../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling/effective_duty_cycle_power_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
conversion_loss_temperature_margin.py
  compute_conversion_loss_temperature_margin = 45.0
  lambdified = 18.200000000000003
duty_cycle_temperature_margin.py
  compute_duty_cycle_temperature_margin = 35.0
  lambdified = -21.0
effective_duty_cycle_power.py
  compute_effective_duty_cycle_power = 15.0
  lambdified_2term = 44.0
test_power_thermal_coupling.py: 3 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models/power_thermal_coupling
```

<!-- end-observed-output -->

## conversion_loss_temperature_margin.py

### Model context from the archive

THERM-PWR-003 — Conversion loss temperature margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_conversion_loss_temperature_margin(warning_temp_c: float, ambient_temp_c: float, output_power_w: float, efficiency: float, thermal_resistance_c_per_w: float)`

### Original formula record

- **Formula id**  THERM-PWR-003
- **Latex**  `m_{conv}=T_{warn}-[T_{amb}+R_{th}P_{out}(1/\eta-1)]`
- **Family**  power_thermal_coupling
- **Name**  conversion_loss_temperature_margin

Additional reference comparisons during migration: 5.

## duty_cycle_temperature_margin.py

### Model context from the archive

THERM-PWR-002 — Duty-cycle temperature margin.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_duty_cycle_temperature_margin(warning_temp_c: float, ambient_temp_c: float, effective_power_w: float, thermal_resistance_c_per_w: float)`

### Original formula record

- **Formula id**  THERM-PWR-002
- **Latex**  `m_{duty}=T_{warn}-(T_{amb}+P_{eff}R_{th})`
- **Family**  power_thermal_coupling
- **Name**  duty_cycle_temperature_margin

Additional reference comparisons during migration: 5.

## effective_duty_cycle_power.py

### Model context from the archive

THERM-PWR-001 — Effective duty-cycle power.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression_2term()`
- `lambdified_2term()`
- `compute_effective_duty_cycle_power(base_power_w: float, duty_cycles: Sequence[float], incremental_powers_w: Sequence[float])`

### Original formula record

- **Formula id**  THERM-PWR-001
- **Latex**  `P_{eff}=P_{base}+\sum_i D_i\Delta P_i`
- **Family**  power_thermal_coupling
- **Name**  effective_duty_cycle_power

Additional reference comparisons during migration: 5.
