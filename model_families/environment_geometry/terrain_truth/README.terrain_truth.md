# terrain_truth

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.terrain_truth.md`

## Why this family exists
Multiscale terrain confidence, local hazard closure, and whether motion or uncertainty outran the truth cell.

## Cross-domain use cases
planetary landing; UGV terrain routing; near-shore autonomy; low-altitude hazard closure.

## Optimal use
Use when map or terrain inputs are tiered and you must distinguish coarse regional truth from local commit-worthy truth.

## Do not use when
Do not use as direct contact or touchdown certification proof without validated local terrain products.

## Canonical formulas in this family

- **TERRAIN-TRUTH-004** `terrain_truth_004__terrain_truth__terrain_vertical_uncertainty_margin.py`: terrain vertical uncertainty margin
  - Symbolic form: `m_z = z_uncert_limit_m - terrain_vertical_uncertainty_m`
  - Why kept: Prevents weak vertical truth from being treated like contact-safe geometry.
- **TERRAIN-TRUTH-005** `terrain_truth_005__terrain_truth__slope_uncertainty_guarded_margin.py`: slope uncertainty guarded margin
  - Symbolic form: `m_su = slope_limit_deg - (slope_local_deg + k_sigma * slope_sigma_deg)`
  - Why kept: Landing, rover traverse, mast deployment, drill placement, and any contact operation where surface slope uncertainty matters.
- **TERRAIN-TRUTH-009** `terrain_truth_009__terrain_truth__multiscale_disagreement_margin.py`: multiscale disagreement margin
  - Symbolic form: `m_ms = tau_ms - ||f_local - f_regional||_W`
  - Why kept: Flags when a regional planning lane diverges too far from local pad truth to support a safe confidence claim.
- **TERRAIN-TRUTH-010** `terrain_truth_010__terrain_truth__lane_aware_confidence_ceiling.py`: lane aware confidence ceiling
  - Symbolic form: `c_lane = min(c_model, c_cap(lane,status) * exp(min(m_ms,0)/tau))`
  - Why kept: Prevents model confidence trained on local truth from being replayed unchanged on regional proxy tiles.
- **TERRAIN-TRUTH-011** `terrain_truth_011__terrain_truth__local_hazard_claim_gate.py`: local hazard claim gate
  - Symbolic form: `g_local = I(lane = local_nac) * I(provenance_complete) * I(status = PAD_TILE_INGESTED) * I(c_lane >= tau_claim)`
  - Why kept: Reusable claim gate for landing, traverse, manipulation, and drill placement hazard assertions.
- **TERRAIN-TRUTH-012** `terrain_truth_012__terrain_truth__roughness_alias_margin.py`: roughness alias margin
  - Symbolic form: `m_alias = r_alias_limit - |relief_local_p95 - relief_regional_p95|`
  - Why kept: Surfaces aliasing blind spots for terrain, ice cracks, trench lips, berms, and cable-shadow lookalikes.
- **TERRAIN-TRUTH-013** `terrain_truth_013__terrain_truth__local_hazard_commit_margin.py`: local_hazard_commit_margin
  - Symbolic form: `m_lhc = s_local_safe - tau_safe - (u_vertical + u_slope + u_alias + u_lineage)`
  - Why kept: Turns local hazard closure into a pessimistic commit margin.
  - Merged from: M4-2B-LOCAL-HAZARD-CLOSURE-MARGIN
- **TERRAIN-TRUTH-014** `terrain_truth_014__terrain_truth__et_001_truth_cell_outrun_margin.py`: ET-001 - truth_cell_outrun_margin
  - Symbolic form: `m_truth = L_truth - v_rel * tau_total`
  - Why kept: Broad law for outrunning spatial truth cells with motion and staleness.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
