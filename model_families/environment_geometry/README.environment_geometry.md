# environment_geometry

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.environment_geometry.md`

## Why this family exists
A path that looks clear on stale geometry is not clear. These laws quantify clearance erosion caused by motion, latency, and environment uncertainty.

## Cross-domain use cases
missile keep-out closure; spacecraft proximity operations; UGV obstacle clearance; maritime passage clearance; swarm separation maintenance.

## Optimal use
Use when moving geometry and delayed environment knowledge can consume a safety margin before the platform gets to use it.

## Do not use when
Do not use for terrain credibility, plant controllability, or authority validity. This shelf is about geometric clearance only.

## Canonical formulas in this family

- **ENV-GEO-001** `env_geo_001__environment_geometry__et_002_dynamic_clearance_margin.py`: ET-002 - dynamic_clearance_margin
  - Symbolic form: `m_clear = c_measured - (c_required + v_closure*t_age + sigma_env)`
  - Why kept: Clearance inflation under motion/latency is broadly reusable.
  - Merged from: M4-2C-OCCLUSION-CLEARANCE-MARGIN, PROP-M4.2_surface_relative_clearance_margin

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
