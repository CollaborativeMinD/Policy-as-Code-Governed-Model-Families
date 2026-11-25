# Horizon geometry

Reduced-order line-of-sight and horizon-clearance margins carrying sampling, finite-source, pointing, and uncertainty terms.

### Use cases

- Solar panel LOS, Earth visibility, camera blinding, and relay visibility screening.
- Terrain horizon products used by surface, maritime, aerial, or orbital twins.
- First-pass geometry sanity checks before ray tracing or higher-fidelity optics.

### Non-use cases

- Do not treat these formulas as full ray tracing or optical simulation.
- Do not use with non-positive observer height or terrain resolution.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [horizon_sampling_margin.py](horizon_sampling_margin.py) — horizon_sampling_margin
- [solar_disk_clearance_margin.py](solar_disk_clearance_margin.py) — solar_disk_guarded_clearance_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [environment_geometry/horizon_geometry/horizon_sampling_margin](../../../model_policy_engine/policies/environment_geometry/horizon_geometry/horizon_sampling_margin_policy.toml)
- [environment_geometry/horizon_geometry/solar_disk_clearance_margin](../../../model_policy_engine/policies/environment_geometry/horizon_geometry/solar_disk_clearance_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
horizon_sampling_margin.py
  compute_horizon_sampling_margin = -35.0
solar_disk_clearance_margin.py
  compute_solar_disk_guarded_clearance_margin = 3.4339999999999997
PASS environment_geometry/horizon_geometry
```

<!-- end-observed-output -->

## horizon_sampling_margin.py

### Model context from the archive

HORIZON-GEO-003 — horizon_sampling_margin

Purpose
-------
Flags when the horizon tile is too coarse for LOS and shadow decisions.

Assumptions
-----------
First-order angular sampling check. Observer height and terrain resolution must be positive.

### Entry points

- `compute_horizon_sampling_margin(alpha_tol_deg: float, terrain_resolution_m: float, observer_height_m: float)`

### Original formula record

- **Formula id**  HORIZON-GEO-003
- **Family**  horizon_geometry
- **Name**  horizon_sampling_margin
- **Symbolic form**  `m_hs = alpha_tol_deg - atan(terrain_resolution_m / observer_height_m) * 180/pi`
- **Typed inputs**  `alpha_tol_deg` (float), `terrain_resolution_m` (float), `observer_height_m` (float)
- **Units**  `alpha_tol_deg` (deg), `terrain_resolution_m` (m/pixel), `observer_height_m` (m), `output` (deg)
- **Assumptions**  First-order angular sampling check. Observer height and terrain resolution must be positive.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Flags when the horizon tile is too coarse for LOS and shadow decisions.
- **Status**  proposed_for_future_builds

## solar_disk_clearance_margin.py

### Model context from the archive

HORIZON-GEO-004 — solar_disk_guarded_clearance_margin

Purpose
-------
Solar panel survivability, camera blinding, horizon camera custody, relay visibility, and Earth visibility screening with finite source size and uncertainty.

Assumptions
-----------
Improves on centerline-only horizon clearance by carrying solar disk, pointing, and terrain-horizon uncertainty. Positive line-of-sight center margin can still be operationally unsafe when the disk clips terrain or structure.

### Entry points

- `compute_solar_disk_guarded_clearance_margin(alpha_sun_center_deg: float, alpha_horizon_deg: float, alpha_sun_half_deg: float=0.266, alpha_pointing_err_deg: float=0.0, alpha_horizon_unc_deg: float=0.0)`

### Original formula record

- **Formula id**  HORIZON-GEO-004
- **Family**  horizon_geometry
- **Name**  solar_disk_guarded_clearance_margin
- **Symbolic form**  `m_sdg = alpha_sun_center_deg - alpha_horizon_deg - alpha_sun_half_deg - alpha_pointing_err_deg - alpha_horizon_unc_deg`
- **Typed inputs**  `alpha_sun_center_deg` (float), `alpha_horizon_deg` (float), `alpha_sun_half_deg` (float), `alpha_pointing_err_deg` (float), `alpha_horizon_unc_deg` (float)
- **Units**  `alpha_sun_center_deg` (deg), `alpha_horizon_deg` (deg), `alpha_sun_half_deg` (deg), `alpha_pointing_err_deg` (deg), `alpha_horizon_unc_deg` (deg), `output` (deg)
- **Assumptions**  Improves on centerline-only horizon clearance by carrying solar disk, pointing, and terrain-horizon uncertainty. Positive line-of-sight center margin can still be operationally unsafe when the disk clips terrain or structure.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Solar panel survivability, camera blinding, horizon camera custody, relay visibility, and Earth visibility screening with finite source size and uncertainty.
- **Status**  proposed_for_future_builds
