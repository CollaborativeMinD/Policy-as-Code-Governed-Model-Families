# safety_pace

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.safety_pace.md`

## Why this family exists
Survivability envelopes, normalized margin erosion, and explicit PACE degradation.

## Cross-domain use cases
missile envelope management; torpedo survivability bands; spacecraft terminal posture demotion; drone fallback; maritime fail-closed navigation.

## Optimal use
Use for fail-closed envelope logic and supervisory demotion under shrinking margin.

## Do not use when
Do not use as a substitute for deriving real physical limits.

## Canonical formulas in this family

- **M1.1** `m1_1__safety_pace__safe_operational_space.py`: Safe operational space
  - Symbolic form: `Ω = {x ∈ R^n : φ_i(x) ≤ C_i,max, i = 1..m}`
  - Why kept: Base compendium law canonicalized for searchability.
- **M1.2** `m1_2__safety_pace__margin_to_death_function.py`: Margin-to-death function
  - Symbolic form: `m_i(x) = 1 − φ_i(x)/C_i,max`
  - Why kept: Base compendium law canonicalized for searchability.
- **M1.3** `m1_3__safety_pace__pace_transition_guards.py`: PACE transition guards
  - Symbolic form: `P → A when ∃i: m_i ≤ 0.20; A → C when ∃i: m_i ≤ 0.10; C → E when ∃i: m_i ≤ 0`
  - Why kept: Base compendium law canonicalized for searchability.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical.
