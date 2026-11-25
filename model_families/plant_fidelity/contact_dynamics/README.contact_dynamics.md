# contact_dynamics

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.contact_dynamics.md`

## Why this family exists
Touchdown, docking, berthing, and collision boundary events fail when impact energy exceeds what the structure or interface can dissipate.

## Cross-domain use cases
lander touchdown; drone perch; spacecraft docking; maritime berthing; UGV obstacle contact.

## Optimal use
Use when the dominant risk is whether contact remains survivable after translational, drop, and rotational energy are counted honestly.

## Do not use when
Do not use when the real problem is guidance, terrain truth, or authority gating upstream of contact.

## Canonical formulas in this family

- **CONTACT-DYN-001** `contact_dyn_001__contact_dynamics__pf_004_contact_energy_margin.py`: PF-004 - contact_energy_margin
  - Symbolic form: `m_contact = E_diss_max - (0.5*m*v_rel^2 + m*g*h_drop + 0.5*omega^T*I*omega)`
  - Why kept: Reusable touchdown, berth, or docking contact survivability law.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
