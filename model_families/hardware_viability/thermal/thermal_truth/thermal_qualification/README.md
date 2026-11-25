# Thermal qualification

Mission-window margin for darkness or cold-soak exposure against an asset-class policy envelope.

### Use cases

- Relay, rover, habitat, fixed sensor, or dormant drone darkness planning.
- Shadow transit and cold-soak exposure checks.
- Policy-window screening before detailed thermal modeling.

### Non-use cases

- Do not use without a governed asset-class policy window.
- Do not treat darkness margin as a full thermal survivability proof.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [darkness_hold_margin_hours.py](darkness_hold_margin_hours.py) — darkness_hold_margin_hours

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../../../model_policy_engine/README.md)

- [hardware_viability/thermal/thermal_truth/thermal_qualification/darkness_hold_margin_hours](../../../../../model_policy_engine/policies/hardware_viability/thermal/thermal_truth/thermal_qualification/darkness_hold_margin_hours_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
darkness_hold_margin_hours.py
  compute_darkness_hold_margin_hours = 7.0
PASS hardware_viability/thermal/thermal_truth/thermal_qualification
```

<!-- end-observed-output -->

## darkness_hold_margin_hours.py

### Model context from the archive

THERM-QUAL-001 — darkness_hold_margin_hours

Purpose
-------
Provides a typed margin for relay, rover, habitat, or fixed-asset darkness planning.

Assumptions
-----------
Positive margin means the requested darkness window remains inside the governed asset-class envelope.

### Entry points

- `compute_darkness_hold_margin_hours(t_policy_h: float, t_dark_h: float)`

### Original formula record

- **Formula id**  THERM-QUAL-001
- **Family**  thermal_qualification
- **Name**  darkness_hold_margin_hours
- **Symbolic form**  `m_dark = t_policy_h - t_dark_h`
- **Typed inputs**  `t_policy_h` (float), `t_dark_h` (float)
- **Units**  `t_policy_h` (h), `t_dark_h` (h), `output` (h)
- **Assumptions**  Positive margin means the requested darkness window remains inside the governed asset-class envelope.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Provides a typed margin for relay, rover, habitat, or fixed-asset darkness planning.
- **Status**  proposed_for_future_builds
