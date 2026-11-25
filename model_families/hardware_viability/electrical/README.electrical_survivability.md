# electrical_survivability

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.electrical_survivability.md`

## Why this family exists
Rail headroom, thermal derate, and recovery energy laws that tell higher layers whether the substrate is still real.

## Cross-domain use cases
flight computer rails; torpedo bus survivability; edge compute power margins; maritime electronics resilience.

## Optimal use
Use when timing, sensing, or actuation depends on a substrate that may be electrically sick before it is visibly dead.

## Do not use when
Do not use as full circuit simulation or bus qualification testing.

## Canonical formulas in this family

- **EE-ELEC-001** `ee_elec_001__electrical_survivability__effective_brownout_margin.py`: effective_brownout_margin
  - Symbolic form: `m_bro = V_min - (V_uvlo + ΔV_ripple + ΔV_droop + ΔV_ref)`
  - Why kept: Strong pessimistic rail-health primitive that broadens electrical survivability beyond normalized consistency only.
- **EE-ELEC-002** `ee_elec_002__electrical_survivability__thermal_derated_power_margin.py`: thermal_derated_power_margin
  - Symbolic form: `m_pth = P_nom * d_T * a - (P_load + P_transient),  d_T = clip((T_shutdown - T_j)/(T_shutdown - T_warn), 0, 1)`
  - Why kept: Useful cross-domain bridge from thermal stress into usable electrical capacity.
- **EE-ELEC-003** `ee_elec_003__electrical_survivability__recovery_energy_margin.py`: recovery_energy_margin
  - Symbolic form: `m_rec = E_avail - (E_restart + E_reacquire + E_isolate + E_safe)`
  - Why kept: Needed for restart-versus-isolate decisions across battery, bus, and remote-edge platforms.
- **POWER-SURV-005** `power_surv_005__electrical_survivability__regulation_chain_disparity_margin.py`: regulation chain disparity margin
  - Symbolic form: `m_reg = delta_limit_pu - abs(v_upstream_pu - v_downstream_pu)`
  - Why kept: Detects converter-chain disagreement even when each rail is still individually inside bounds.
- **POWER-SURV-006** `power_surv_006__electrical_survivability__bus_anchor_consistency_margin.py`: bus anchor consistency margin
  - Symbolic form: `m_anchor = min(m_bus, m_reg)`
  - Why kept: Provides one pessimistic typed margin for downstream decision logic and dashboards.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
