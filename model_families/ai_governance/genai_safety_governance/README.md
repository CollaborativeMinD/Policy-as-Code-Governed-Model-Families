# Genai safety governance

Hard-veto advisory governance for probabilistic or heuristic outputs that must stay subordinate to safety law.

### Use cases

- Mission-summary rejection gates.
- Patch or optimization proposal gates.
- Human-plus-agent workflows where any death state, evidence deficit, stale context, or contradiction must hard-fail advisory output.

### Non-use cases

- Do not use as a scoring dashboard; this is a veto gate.
- Do not soften death states, stale evidence, or negative margins into advisory warnings.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [heuristic_rejection_gate.py](heuristic_rejection_gate.py) — heuristic_rejection_gate

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [ai_governance/genai_safety_governance/heuristic_rejection_gate](../../../model_policy_engine/policies/ai_governance/genai_safety_governance/heuristic_rejection_gate_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
heuristic_rejection_gate.py
  compute_heuristic_rejection_gate = [true, []]
PASS ai_governance/genai_safety_governance
```

<!-- end-observed-output -->

## heuristic_rejection_gate.py

### Model context from the archive

GEN-SAFE-003 — heuristic_rejection_gate

Purpose
-------
Works for mission summaries, design suggestions, triage notes, and optimization proposals that must stay subordinate to safety law.

Assumptions
-----------
Any live death state, negative safety margin, evidence deficit, stale context, contradiction, alias laundering, or fabricated truth hard-fails the advisory.

### Entry points

- `compute_heuristic_rejection_gate(active_margins: Mapping[str, float], active_death_states: Sequence[str], evidence_coverage_ratio_value: float, parse_yield: float, freshness_score: float, contradiction_score: float, semantic_alias_drift_score: float, unbound_truth_penalty: float, *, min_ecr: float=1.0, min_parse_yield: float=1.0, min_freshness: float=0.5, max_contradiction: float=0.0, max_semantic_alias: float=0.0, max_unbound_truth: float=0.0)`

### Original formula record

- **Formula id**  GEN-SAFE-003
- **Family**  genai_safety_governance
- **Name**  heuristic_rejection_gate
- **Symbolic form**  `g_hrg = I(min(m_i) > 0) * I(N_death = 0) * I(ECR >= tau_ecr) * I(DPY >= tau_dpy) * I(F >= tau_f) * I(CES <= tau_ces) * I(SAD <= tau_sad) * I(UTIP <= tau_utip)`
- **Typed inputs**  `active_margins` (dict[str, float]), `active_death_states` (Sequence[str]), `evidence_coverage_ratio` (float), `parse_yield` (float), `freshness_score` (float), `contradiction_score` (float), `semantic_alias_drift_score` (float), `unbound_truth_penalty` (float)
- **Units**  `active_margins` (mixed_domain_units), `active_death_states` (unitless), `evidence_coverage_ratio` (unitless), `parse_yield` (unitless), `freshness_score` (unitless), `contradiction_score` (unitless), `semantic_alias_drift_score` (unitless), `unbound_truth_penalty` (unitless), `output` (bool)
- **Assumptions**  Any live death state, negative safety margin, evidence deficit, stale context, contradiction, alias laundering, or fabricated truth hard-fails the advisory.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Works for mission summaries, design suggestions, triage notes, and optimization proposals that must stay subordinate to safety law.
- **Status**  proposed_for_future_builds
