# mechanical_survivability

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.mechanical_survivability.md`

## Why this family exists
Resonance separation, transmissibility, preload retention, and structural survivability gates.

## Cross-domain use cases
payload mounting on drones; maritime equipment shock; spacecraft sensor mounts; UGV payload carriers.

## Optimal use
Use when payload or platform survivability depends on vibration separation, base motion leakage, or fastener integrity.

## Do not use when
Do not use as full structural FEA or material qualification testing.

## Canonical formulas in this family

- **MECH-SURV-001** `mech_surv_001__mechanical_survivability__resonance_separation_margin.py`: Resonance separation margin
  - Symbolic form: `m_sep = min_{i,j} (|f_n,i - f_exc,j| / f_exc,j) with negative margin when forcing lies inside an exclusion band`
  - Why kept: Classic structural margin with broad value across mounts and payloads.
- **MECH-SURV-002** `mech_surv_002__mechanical_survivability__base_excitation_transmissibility.py`: Base-excitation transmissibility
  - Symbolic form: `T(r,zeta) = sqrt((1 + (2 zeta r)^2) / ((1 - r^2)^2 + (2 zeta r)^2))`
  - Why kept: Quantifies how base motion leaks into sensitive payloads.
- **MECH-SURV-003** `mech_surv_003__mechanical_survivability__fastener_preload_retention_margin.py`: Fastener preload retention margin
  - Symbolic form: `F_remain = F0 - k_eq*(alpha_j - alpha_c)*L*DeltaT - gamma*F_ext ; m = (F_remain - F_min)/F_min`
  - Why kept: Portable mounting survivability gate.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
