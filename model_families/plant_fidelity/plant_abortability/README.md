# Plant abortability

Abort and waveoff recoverability timing margins for late-stage commit logic.

### Use cases

- Powered descent waveoff, docking retreat, runway go-around, station-keeping escape, and collision avoidance.
- Red-team inflation of engine start, settle, escape, clearance, and guard timing.
- Late-stage commit guards where software optimism can outlive physics.

### Non-use cases

- Do not treat reduced-order timing as a 6-DOF escape simulation.
- Do not use negative timing terms to make the margin look better.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [waveoff_closure_margin.py](waveoff_closure_margin.py) — waveoff_closure_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [plant_fidelity/plant_abortability/waveoff_closure_margin](../../../model_policy_engine/policies/plant_fidelity/plant_abortability/waveoff_closure_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
waveoff_closure_margin.py
  compute_waveoff_closure_margin = 2.5
PASS plant_fidelity/plant_abortability
```

<!-- end-observed-output -->

## waveoff_closure_margin.py

### Model context from the archive

PLANT-ABORT-001 — waveoff_closure_margin

Purpose
-------
Turns late-abort handwaving into a typed recoverability margin for landing, docking, and collision-avoidance escape logic.

Assumptions
-----------
Negative margin means waveoff is already physically unavailable, regardless of software optimism.

### Entry points

- `compute_waveoff_closure_margin(t_available_for_waveoff_s: float, t_engine_start_s: float, t_attitude_settle_s: float, t_vertical_escape_s: float, t_lateral_clearance_s: float, t_guard_s: float=0.0)`

### Original formula record

- **Formula id**  PLANT-ABORT-001
- **Family**  plant_abortability
- **Name**  waveoff_closure_margin
- **Symbolic form**  `m_abort = t_available_for_waveoff_s - (t_engine_start_s + t_attitude_settle_s + t_vertical_escape_s + t_lateral_clearance_s + t_guard_s)`
- **Typed inputs**  `t_available_for_waveoff_s` (float), `t_engine_start_s` (float), `t_attitude_settle_s` (float), `t_vertical_escape_s` (float), `t_lateral_clearance_s` (float), `t_guard_s` (float)
- **Units**  `t_available_for_waveoff_s` (s), `t_engine_start_s` (s), `t_attitude_settle_s` (s), `t_vertical_escape_s` (s), `t_lateral_clearance_s` (s), `t_guard_s` (s), `output` (s)
- **Assumptions**  Negative margin means waveoff is already physically unavailable, regardless of software optimism.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Turns late-abort handwaving into a typed recoverability margin for landing, docking, and collision-avoidance escape logic.
- **Status**  proposed_for_future_builds
