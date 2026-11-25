# Terrain truth

Multiscale terrain confidence, local hazard closure, and whether motion or uncertainty outran the truth cell.

### Optimal use

Use when map or terrain inputs are tiered and you must distinguish coarse regional truth from local commit-worthy truth.

### Do not use when

Do not use as direct contact or touchdown certification proof without validated local terrain products.

Commit gates that prevent regional or proxy terrain from impersonating local hazard closure.

### Use cases

- Landing, traverse, manipulator placement, drill placement, and contact operations.
- Multi-resolution terrain stacks where regional maps arrive before local hazard layers.
- Digital twins where coarse map safety can mask missing local closure.

### Non-use cases

- Do not use regional proxy terrain for local contact closure.
- Do not treat a commit gate pass as proof that the terrain itself is correct.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [c6_1_los_terrain_mask_closure.py](c6_1_los_terrain_mask_closure.py) — Line-of-sight / terrain-mask closure law
- [lane_aware_confidence_ceiling.py](lane_aware_confidence_ceiling.py) — lane_aware_confidence_ceiling
- [local_hazard_claim_gate.py](local_hazard_claim_gate.py) — local_hazard_claim_gate
- [multiscale_disagreement_margin.py](multiscale_disagreement_margin.py) — multiscale_disagreement_margin
- [roughness_alias_margin.py](roughness_alias_margin.py) — roughness_alias_margin
- [slope_uncertainty_guarded_margin.py](slope_uncertainty_guarded_margin.py) — slope_uncertainty_guarded_margin
- [terrain_commit_closure.py](terrain_commit_closure.py) — terrain_commit_closure_gate
- [terrain_truth_disagreement.py](terrain_truth_disagreement.py) — Terrain truth disagreement index
- [terrain_vertical_uncertainty_margin.py](terrain_vertical_uncertainty_margin.py) — terrain_vertical_uncertainty_margin
- [truth_cell_outrun_margin.py](truth_cell_outrun_margin.py) — truth_cell_outrun_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [environment_geometry/terrain_truth/c6_1_los_terrain_mask_closure](../../../model_policy_engine/policies/environment_geometry/terrain_truth/c6_1_los_terrain_mask_closure_policy.toml)
- [environment_geometry/terrain_truth/lane_aware_confidence_ceiling](../../../model_policy_engine/policies/environment_geometry/terrain_truth/lane_aware_confidence_ceiling_policy.toml)
- [environment_geometry/terrain_truth/local_hazard_claim_gate](../../../model_policy_engine/policies/environment_geometry/terrain_truth/local_hazard_claim_gate_policy.toml)
- [environment_geometry/terrain_truth/multiscale_disagreement_margin](../../../model_policy_engine/policies/environment_geometry/terrain_truth/multiscale_disagreement_margin_policy.toml)
- [environment_geometry/terrain_truth/roughness_alias_margin](../../../model_policy_engine/policies/environment_geometry/terrain_truth/roughness_alias_margin_policy.toml)
- [environment_geometry/terrain_truth/slope_uncertainty_guarded_margin](../../../model_policy_engine/policies/environment_geometry/terrain_truth/slope_uncertainty_guarded_margin_policy.toml)
- [environment_geometry/terrain_truth/terrain_commit_closure](../../../model_policy_engine/policies/environment_geometry/terrain_truth/terrain_commit_closure_policy.toml)
- [environment_geometry/terrain_truth/terrain_truth_disagreement](../../../model_policy_engine/policies/environment_geometry/terrain_truth/terrain_truth_disagreement_policy.toml)
- [environment_geometry/terrain_truth/terrain_vertical_uncertainty_margin](../../../model_policy_engine/policies/environment_geometry/terrain_truth/terrain_vertical_uncertainty_margin_policy.toml)
- [environment_geometry/terrain_truth/truth_cell_outrun_margin](../../../model_policy_engine/policies/environment_geometry/terrain_truth/truth_cell_outrun_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
c6_1_los_terrain_mask_closure.py
  compute_los_terrain_mask_margin = -0.09999999999999998
lane_aware_confidence_ceiling.py
  compute_lane_aware_confidence_ceiling = [0.9, 1.0]
local_hazard_claim_gate.py
  compute_local_hazard_claim_gate = true
multiscale_disagreement_margin.py
  compute_multiscale_disagreement_margin = 6.0
roughness_alias_margin.py
  compute_roughness_alias_margin = 0.14999999999999997
slope_uncertainty_guarded_margin.py
  compute_slope_uncertainty_guarded_margin = 3.0
terrain_commit_closure.py
  geospatial_status_ceiling_gate = true
  compute_terrain_commit_closure_gate = true
terrain_truth_disagreement.py
  compute_terrain_truth_disagreement_index = 0.508888888888889
terrain_vertical_uncertainty_margin.py
  compute_terrain_vertical_uncertainty_margin = 0.3
truth_cell_outrun_margin.py
  compute_truth_cell_outrun_margin = 0.10000000000000003
PASS environment_geometry/terrain_truth
```

<!-- end-observed-output -->

## c6_1_los_terrain_mask_closure.py

### Model context from the archive

C6.1 — Line-of-sight / terrain-mask closure law

Purpose
-------
Computes whether a sensing, comms, or illumination ray clears the true horizon
mask with enough margin to matter. Same law, different pain: RF relay, optical
tracking, solar line, and navigation visibility all care whether terrain blocks
the ray.

### Entry points

- `compute_los_terrain_mask_margin(ray_elevation_angle: float, horizon_mask_angle: float, buffer_angle: float=0.0)`

### Original formula record

- **Formula id**  C6.1
- **Name**  Line-of-sight / terrain-mask closure law
- **Symbolic form**  `m_los = θ_ray - θ_horizon_mask - θ_buffer`
- **Typed inputs**  `ray_elevation_angle` (float), `horizon_mask_angle` (float), `buffer_angle` (float)
- **Units**  `ray_elevation_angle` (rad), `horizon_mask_angle` (rad), `buffer_angle` (rad), `output` (rad)
- **Assumptions**  Angles are expressed in a common local frame. Positive margin means the ray clears terrain with buffer.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  terrain truth, environment truth, contested edge-network realism, first-pass space/comm geometry

## lane_aware_confidence_ceiling.py

### Model context from the archive

TERRAIN-TRUTH-010 — lane_aware_confidence_ceiling

Purpose
-------
Prevents model confidence trained on local truth from being replayed unchanged on regional proxy tiles.

Assumptions
-----------
Confidence must be capped by source lane and disagreement margin before any downstream consumer sees it.

### Entry points

- `compute_lane_aware_confidence_ceiling(c_model: float, lane: str, status: str, m_ms: float, tau: float=6.0)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-010
- **Family**  terrain_truth
- **Name**  lane_aware_confidence_ceiling
- **Symbolic form**  `c_lane = min(c_model, c_cap(lane,status) * exp(min(m_ms,0)/tau))`
- **Typed inputs**  `c_model` (float), `lane` (str), `status` (str), `m_ms` (float), `tau` (float)
- **Units**  `c_model` (unitless), `lane` (unitless), `status` (unitless), `m_ms` (feature_distance), `tau` (feature_distance), `output` (unitless)
- **Assumptions**  Confidence must be capped by source lane and disagreement margin before any downstream consumer sees it.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Prevents model confidence trained on local truth from being replayed unchanged on regional proxy tiles.
- **Status**  proposed_for_future_builds

## local_hazard_claim_gate.py

### Model context from the archive

TERRAIN-TRUTH-011 — local_hazard_claim_gate

Purpose
-------
Reusable claim gate for landing, traverse, manipulation, and drill placement hazard assertions.

Assumptions
-----------
A safe-looking score is not enough when source lane or provenance is wrong.

### Entry points

- `compute_local_hazard_claim_gate(lane: str, provenance_complete: bool, status: str, c_lane: float, tau_claim: float=0.5)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-011
- **Family**  terrain_truth
- **Name**  local_hazard_claim_gate
- **Symbolic form**  `g_local = I(lane = local_nac) * I(provenance_complete) * I(status = PAD_TILE_INGESTED) * I(c_lane >= tau_claim)`
- **Typed inputs**  `lane` (str), `provenance_complete` (bool), `status` (str), `c_lane` (float), `tau_claim` (float)
- **Units**  `lane` (unitless), `provenance_complete` (unitless), `status` (unitless), `c_lane` (unitless), `tau_claim` (unitless), `output` (bool)
- **Assumptions**  A safe-looking score is not enough when source lane or provenance is wrong.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable claim gate for landing, traverse, manipulation, and drill placement hazard assertions.
- **Status**  proposed_for_future_builds

## multiscale_disagreement_margin.py

### Model context from the archive

TERRAIN-TRUTH-009 — multiscale_disagreement_margin

Purpose
-------
Flags when a regional planning lane diverges too far from local pad truth to support a safe confidence claim.

Assumptions
-----------
Local and regional feature vectors are aligned and weighted by mission-relevant sensitivity.

### Entry points

- `compute_multiscale_disagreement_margin(f_local: Sequence[float], f_regional: Sequence[float], tau_ms: float=6.0)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-009
- **Family**  terrain_truth
- **Name**  multiscale_disagreement_margin
- **Symbolic form**  `m_ms = tau_ms - ||f_local - f_regional||_W`
- **Typed inputs**  `f_local` (list[float]), `f_regional` (list[float]), `tau_ms` (float)
- **Units**  `f_local` (mixed_feature_units), `f_regional` (mixed_feature_units), `tau_ms` (feature_distance), `output` (feature_distance)
- **Assumptions**  Local and regional feature vectors are aligned and weighted by mission-relevant sensitivity.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Flags when a regional planning lane diverges too far from local pad truth to support a safe confidence claim.
- **Status**  proposed_for_future_builds

## roughness_alias_margin.py

### Model context from the archive

TERRAIN-TRUTH-012 — roughness_alias_margin

Purpose
-------
Surfaces aliasing blind spots for terrain, ice cracks, trench lips, berms, and cable-shadow lookalikes.

Assumptions
-----------
High-frequency relief hidden by coarse regional truth is treated as risk, not noise.

### Entry points

- `compute_roughness_alias_margin(relief_local_p95: float, relief_regional_p95: float, r_alias_limit: float=0.35)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-012
- **Family**  terrain_truth
- **Name**  roughness_alias_margin
- **Symbolic form**  `m_alias = r_alias_limit - |relief_local_p95 - relief_regional_p95|`
- **Typed inputs**  `relief_local_p95` (float), `relief_regional_p95` (float), `r_alias_limit` (float)
- **Units**  `relief_local_p95` (m), `relief_regional_p95` (m), `r_alias_limit` (m), `output` (m)
- **Assumptions**  High-frequency relief hidden by coarse regional truth is treated as risk, not noise.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Surfaces aliasing blind spots for terrain, ice cracks, trench lips, berms, and cable-shadow lookalikes.
- **Status**  proposed_for_future_builds

## slope_uncertainty_guarded_margin.py

### Model context from the archive

TERRAIN-TRUTH-005 — slope_uncertainty_guarded_margin

Purpose
-------
Landing, rover traverse, mast deployment, drill placement, and any contact operation where surface slope uncertainty matters.

Assumptions
-----------
Use when slope is inferred from coarse or mixed-resolution terrain products. A positive nominal slope margin is not enough if slope uncertainty can still push the vehicle over limit.

### Entry points

- `compute_slope_uncertainty_guarded_margin(slope_limit_deg: float, slope_local_deg: float, slope_sigma_deg: float, k_sigma: float=2.0)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-005
- **Family**  terrain_truth
- **Name**  slope_uncertainty_guarded_margin
- **Symbolic form**  `m_su = slope_limit_deg - (slope_local_deg + k_sigma * slope_sigma_deg)`
- **Typed inputs**  `slope_limit_deg` (float), `slope_local_deg` (float), `slope_sigma_deg` (float), `k_sigma` (float)
- **Units**  `slope_limit_deg` (deg), `slope_local_deg` (deg), `slope_sigma_deg` (deg), `k_sigma` (unitless), `output` (deg)
- **Assumptions**  Use when slope is inferred from coarse or mixed-resolution terrain products. A positive nominal slope margin is not enough if slope uncertainty can still push the vehicle over limit.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Landing, rover traverse, mast deployment, drill placement, and any contact operation where surface slope uncertainty matters.
- **Status**  proposed_for_future_builds

## terrain_commit_closure.py

### Model context from the archive

TERRAIN-GOV-005 — terrain_commit_closure_gate

Purpose
-------
Blocks commit when runtime is tempted to reuse regional proxy terrain as local hazard truth.

Assumptions
-----------
Region-scale terrain may guide planning but cannot stand in for local touchdown closure.

### Entry points

- `geospatial_status_ceiling_gate(claimed_status: str, status_ceiling: str)`
- `compute_terrain_commit_closure_gate(local_hazard_closed: bool, geospatial_status: str, provenance_complete: bool, region_proxy_alias_used: bool)`

### Original formula record

- **Formula id**  TERRAIN-GOV-005
- **Family**  terrain_governance
- **Name**  terrain_commit_closure_gate
- **Symbolic form**  `g_terr = I(local_hazard_closed) * I(geospatialStatus >= PAD_TILE_INGESTED) * I(provenance_complete) * I(region_proxy_alias_used = 0)`
- **Typed inputs**  `local_hazard_closed` (bool), `geospatial_status` (str), `provenance_complete` (bool), `region_proxy_alias_used` (bool)
- **Units**  `local_hazard_closed` (bool), `geospatial_status` (text), `provenance_complete` (bool), `region_proxy_alias_used` (bool), `output` (bool)
- **Assumptions**  Region-scale terrain may guide planning but cannot stand in for local touchdown closure.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Blocks commit when runtime is tempted to reuse regional proxy terrain as local hazard truth.
- **Status**  proposed_for_future_builds

## terrain_truth_disagreement.py

### Model context from the archive

E1.1 — Terrain truth disagreement index

Purpose
-------
Quantifies how badly coarse map truth, fine local truth, and observed hazard
content disagree. This is aimed straight at the classic failure where the map
looked clean right up until the vehicle met the ground in person.

### Entry points

- `compute_terrain_truth_disagreement_index(elevation_delta_rms: float, slope_delta_rms: float, hazard_probability_delta: float, lineage_completeness: float, elevation_ref: float, slope_ref: float, weights: tuple[float, float, float, float]=(0.35, 0.25, 0.25, 0.15))`

### Original formula record

- **Formula id**  E1.1
- **Name**  Terrain truth disagreement index
- **Symbolic form**  `I_tt = w_h*|Δh|/H_ref + w_s*|Δs|/S_ref + w_p*|Δp_hazard| + w_l*(1-L)`
- **Typed inputs**  `elevation_delta_rms` (float), `slope_delta_rms` (float), `hazard_probability_delta` (float), `lineage_completeness` (float), `elevation_ref` (float), `slope_ref` (float), `weights` (tuple[float,float,float,float])
- **Units**  `elevation_delta_rms` (m), `slope_delta_rms` (deg), `hazard_probability_delta` (unitless), `lineage_completeness` (unitless), `elevation_ref` (m), `slope_ref` (deg), `output` (unitless)
- **Assumptions**  Lineage completeness is normalized to [0,1]. Larger values indicate more trust loss; use hard gates when the index exceeds mission-specific truth ceiling bands.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Primary gaps closed**  environment truth, terrain truth, provenance governance, source lineage gates

## terrain_vertical_uncertainty_margin.py

### Model context from the archive

TERRAIN-TRUTH-004 — terrain_vertical_uncertainty_margin

Purpose
-------
Prevents weak vertical truth from being treated like contact-safe geometry.

Assumptions
-----------
A positive margin means the product remains inside the allowed vertical-uncertainty bound for the intended task.

### Entry points

- `compute_terrain_vertical_uncertainty_margin(z_uncert_limit_m: float, terrain_vertical_uncertainty_m: float)`

### Original formula record

- **Formula id**  TERRAIN-TRUTH-004
- **Family**  terrain_truth
- **Name**  terrain_vertical_uncertainty_margin
- **Symbolic form**  `m_z = z_uncert_limit_m - terrain_vertical_uncertainty_m`
- **Typed inputs**  `z_uncert_limit_m` (float), `terrain_vertical_uncertainty_m` (float)
- **Units**  `z_uncert_limit_m` (m), `terrain_vertical_uncertainty_m` (m), `output` (m)
- **Assumptions**  A positive margin means the product remains inside the allowed vertical-uncertainty bound for the intended task.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Prevents weak vertical truth from being treated like contact-safe geometry.
- **Status**  proposed_for_future_builds

## truth_cell_outrun_margin.py

### Model context from the archive

ET-001 - truth_cell_outrun_margin

Checks whether a spatial truth product remains locally relevant by the time it is used.
Coarse truth kills with confidence; this law helps stop that.

### Entry points

- `compute_truth_cell_outrun_margin(truth_cell_scale_m: float, relative_speed_m_s: float, total_age_s: float)`

### Original formula record

- **Formula id**  ET-001
- **Family**  environment_truth
- **Name**  truth_cell_outrun_margin
- **Symbolic form**  `m_truth = L_truth - v_rel * tau_total`
- **Typed inputs**  `truth_cell_scale_m` (float), `relative_speed_m_s` (float), `total_age_s` (float)
- **Units**  `truth_cell_scale_m` (m), `relative_speed_m_s` (m/s), `total_age_s` (s), `output` (m)
- **Assumptions**  Truth cell scale should match the smallest spatial feature that materially changes a go or no-go decision.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Weak areas hit**  environment truth, terrain truth, temporal coherence and provenance governance
- **Multi use role**  Reusable for terrain grids, sea-state cells, current maps, weather tiles, and threat occupancy products.
