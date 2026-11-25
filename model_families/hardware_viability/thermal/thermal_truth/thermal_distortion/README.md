# Thermal distortion

Runtime distortion scoring from heat-driven latency, throughput, clock, and thermal-utilization degradation.

### Use cases

- Processor throttling, inference latency inflation, sensor cadence drift, and edge-compute degradation.
- Runtime health gates before thermal shutdown occurs.
- Hardware timing realism in digital twins.

### Non-use cases

- Do not use without a valid workload-specific baseline.
- Do not treat the index as a material certification or detailed thermal model.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [thermal_distortion_index.py](thermal_distortion_index.py) — thermal_distortion_index

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_distortion/thermal_distortion_index](../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_distortion/thermal_distortion_index_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
thermal_distortion_index.py
  compute_thermal_distortion_index = 1.0
PASS hardware_viability/thermal/thermal_truth/thermal_distortion
```

<!-- end-observed-output -->

## thermal_distortion_index.py

### Model context from the archive

THERM-SILENT-001 — thermal_distortion_index

Purpose
-------
Detects silent thermal throttling before shutdown when clocks and latency already drift under heat.

Assumptions
-----------
Use only when a valid performance baseline exists for the same workload class.

### Entry points

- `compute_thermal_distortion_index(temp_c: float, warning_high_c: float, critical_high_c: float, latency_baseline_ms: float, latency_current_ms: float, throughput_baseline_hz: float, throughput_current_hz: float, clock_fraction: float)`

### Original formula record

- **Formula id**  THERM-SILENT-001
- **Family**  thermal_distortion
- **Name**  thermal_distortion_index
- **Symbolic form**  `I_td = max(u_T, latency_ratio-1, 1-throughput_ratio, 1-clock_fraction)`
- **Typed inputs**  `temp_c` (float), `warning_high_c` (float), `critical_high_c` (float), `latency_baseline_ms` (float), `latency_current_ms` (float), `throughput_baseline_hz` (float), `throughput_current_hz` (float), `clock_fraction` (float)
- **Units**  `temp_c` (C), `warning_high_c` (C), `critical_high_c` (C), `latency_baseline_ms` (ms), `latency_current_ms` (ms), `throughput_baseline_hz` (Hz), `throughput_current_hz` (Hz), `clock_fraction` (unitless), `output` (unitless)
- **Assumptions**  Use only when a valid performance baseline exists for the same workload class.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Detects silent thermal throttling before shutdown when clocks and latency already drift under heat.
- **Status**  proposed_for_future_builds
