# Safety pace

Survivability envelopes, normalized margin erosion, and explicit PACE degradation.

### Optimal use

Use for fail-closed envelope logic and supervisory demotion under shrinking margin.

### Do not use when

Do not use as a substitute for deriving real physical limits.

## Model files

- [margin_to_death.py](margin_to_death.py) — Margin‑to‑death function
- [pace_transition_guards.py](pace_transition_guards.py) — PACE transition guards
- [safe_operational_space.py](safe_operational_space.py) — Safe operational space

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [safety_pace/margin_to_death](../../model_policy_engine/policies/safety_pace/margin_to_death_policy.toml)
- [safety_pace/pace_transition_guards](../../model_policy_engine/policies/safety_pace/pace_transition_guards_policy.toml)
- [safety_pace/safe_operational_space](../../model_policy_engine/policies/safety_pace/safe_operational_space_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
margin_to_death.py
  compute_margin_to_death = 0.19999999999999996
pace_transition_guards.py
  compute_pace_transition = "A"
  compute_pace_transition = "A"
safe_operational_space.py
  compute_safe_operational_space = true
PASS safety_pace
```

<!-- end-observed-output -->

## margin_to_death.py

### Model context from the archive

M1.2 — Margin‑to‑death function

The margin‑to‑death function is defined as

    m_i(x) = 1 − φ_i(x) / C_i,max,

where φ_i(x) is a constraint metric and C_i,max is its maximum allowable
value.  A larger ``m_i`` indicates greater safety margin; a value of
zero or negative indicates imminent failure.

### Entry points

- `compute_margin_to_death(phi_value: float, c_max: float)`

### Original formula record

- **Formula id**  M1.2
- **Name**  Margin‑to‑death function
- **Symbolic form**  `m_i(x) = 1 − φ_i(x)/C_i,max`
- **Typed inputs**  `phi_value` (float), `c_max` (float)
- **Units**  `phi_value` (unitless), `c_max` (unitless), `output` (unitless)
- **Assumptions**  C_i,max must be non‑zero and positive.  φ_i(x) should be non‑negative.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_margin_to_death.py::test_margin_to_death`, `rtm_link=lambda_laws.margin_to_death`, `ssot_gate=notebooks/gate_margin_to_death.ipynb`

## pace_transition_guards.py

### Model context from the archive

M1.3 — PACE transition guards

The PACE transition guards govern how a supervisory logic moves
between P (Prepare), A (Assess), C (Commit), and E (Execute) modes
based on the minimum safety margin:

* **P → A** when any margin m_i ≤ 0.20.
* **A → C** when any margin m_i ≤ 0.10.
* **C → E** when any margin m_i ≤ 0.

If none of these conditions are met, the mode remains unchanged.

### Entry points

- `compute_pace_transition(margins: Sequence[float], current_state: str)`

### Original formula record

- **Formula id**  M1.3
- **Name**  PACE transition guards
- **Symbolic form**  `P → A when ∃i: m_i ≤ 0.20; A → C when ∃i: m_i ≤ 0.10; C → E when ∃i: m_i ≤ 0`
- **Typed inputs**  `margins` (Sequence[float]), `current_state` (str)
- **Units**  `margins` (unitless), `current_state` (state), `output` (state)
- **Assumptions**  The current_state must be one of 'P', 'A', 'C', or 'E'. Margins must be normalized to the range [0, 1] where lower values indicate reduced safety.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_pace_transition_guards.py::test_pace_transition`, `rtm_link=lambda_laws.pace_transition_guards`, `ssot_gate=notebooks/gate_pace_transition_guards.ipynb`

Additional reference comparisons during migration: 1.

## safe_operational_space.py

### Model context from the archive

M1.1 — Safe operational space

This module implements the safe operational space predicate

    Ω = {x ∈ ℝⁿ : φ_i(x) ≤ C_i,max, i=1..m},

which appears in Module 1 of the compendium.  The predicate returns
``True`` if the state lies within all configured constraints and
``False`` otherwise.

### Entry points

- `compute_safe_operational_space(phi_values: Sequence[float], c_max: Sequence[float])`

### Original formula record

- **Formula id**  M1.1
- **Name**  Safe operational space
- **Symbolic form**  `Ω = {x ∈ R^n : φ_i(x) ≤ C_i,max, i = 1..m}`
- **Typed inputs**  `phi_values` (Sequence[float]), `c_max` (Sequence[float])
- **Units**  `phi_values` (unitless), `c_max` (unitless), `output` (bool)
- **Assumptions**  phi_values and c_max must have the same length.  Each entry φ_i(x) represents a normalized constraint metric and must not exceed its corresponding C_i,max for the state to be considered safe.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_safe_operational_space.py::test_safe_operational_space`, `rtm_link=lambda_laws.safe_operational_space`, `ssot_gate=notebooks/gate_safe_operational_space.ipynb`
