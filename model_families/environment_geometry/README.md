# Environment geometry

A path that looks clear on stale geometry is not clear. These laws quantify clearance erosion caused by motion, latency, and environment uncertainty.

### Optimal use

Use when moving geometry and delayed environment knowledge can consume a safety margin before the platform gets to use it.

### Do not use when

Do not use for terrain credibility, plant controllability, or authority validity. This shelf is about geometric clearance only.

## Subdirectories

- [horizon_geometry](horizon_geometry/README.md)
- [terrain_truth](terrain_truth/README.md)

## Model files

- [dynamic_clearance_margin.py](dynamic_clearance_margin.py) — dynamic_clearance_margin
- [spatial_hazard.py](spatial_hazard.py) — Spatial hazard set

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [environment_geometry/dynamic_clearance_margin](../../model_policy_engine/policies/environment_geometry/dynamic_clearance_margin_policy.toml)
- [environment_geometry/spatial_hazard](../../model_policy_engine/policies/environment_geometry/spatial_hazard_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
dynamic_clearance_margin.py
  compute_dynamic_clearance_margin = -1.3199999999999998
spatial_hazard.py
  compute_hazard_function = -0.36
  is_point_in_hazard = true
PASS environment_geometry
```

<!-- end-observed-output -->

## dynamic_clearance_margin.py

### Model context from the archive

ET-002 - dynamic_clearance_margin

Inflates the required clearance by closure during packet age plus declared environment uncertainty.
This is a better answer than pretending a once-measured gap stays true while the vehicle keeps moving.

### Entry points

- `compute_dynamic_clearance_margin(measured_clearance_m: float, required_clearance_m: float, closure_speed_m_s: float, environment_age_s: float, environment_uncertainty_m: float)`

### Original formula record

- **Formula id**  ET-002
- **Family**  environment_truth
- **Name**  dynamic_clearance_margin
- **Symbolic form**  `m_clear = c_measured - (c_required + v_closure*t_age + sigma_env)`
- **Typed inputs**  `measured_clearance_m` (float), `required_clearance_m` (float), `closure_speed_m_s` (float), `environment_age_s` (float), `environment_uncertainty_m` (float)
- **Units**  `measured_clearance_m` (m), `required_clearance_m` (m), `closure_speed_m_s` (m/s), `environment_age_s` (s), `environment_uncertainty_m` (m), `output` (m)
- **Assumptions**  Uncertainty term already includes map, sensor, and registration error contributions relevant to the current path corridor.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Weak areas hit**  environment truth, terrain truth, hardware-closed timing and authority seams
- **Multi use role**  Works for landing corridors, obstacle clearance, berth approach, mast or rotor clearance, and low-altitude route checks.

## spatial_hazard.py

### Model context from the archive

M3.4a — Spatial hazard set

This module defines spatial hazard sets as spheres in Euclidean space:

    O_i = { p ∈ ℝⁿ : ||p − c_i|| ≤ r_i },

with hazard function

    h_i(p) = ||p − c_i||² − r_i².

Points with ``h_i(p) ≤ 0`` lie inside or on the hazard boundary.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_hazard_function(p: Sequence[float], c: Sequence[float], r: float)`
- `is_point_in_hazard(p: Sequence[float], c: Sequence[float], r: float)`

### Original formula record

- **Formula id**  M3.4a
- **Name**  Spatial hazard set
- **Symbolic form**  `O_i = { p ∈ R^n : ||p - c_i|| ≤ r_i } ; h_i(p) = ||p - c_i||² - r_i²`
- **Typed inputs**  `p` (Sequence[float]), `c` (Sequence[float]), `r` (float)
- **Units**  `p` (m), `c` (m), `r` (m), `output` (m²)
- **Assumptions**  p and c must be vectors of the same dimension.  r must be non‑negative.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_spatial_hazard.py::test_spatial_hazard`, `rtm_link=lambda_laws.spatial_hazard`, `ssot_gate=notebooks/gate_spatial_hazard.ipynb`
