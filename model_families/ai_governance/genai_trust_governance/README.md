# Genai trust governance

Context saturation scoring for advisory lanes under token pressure, conflict density, and source sprawl.

### Use cases

- Large incident review packets.
- Cross-domain mission briefs.
- Agent orchestration where too much context or conflict increases hallucination risk.

### Non-use cases

- Do not use as factual accuracy measurement.
- Do not compare scores across workloads with different budgets without recalibration.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [context_saturation_index.py](context_saturation_index.py) — context_saturation_index

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [ai_governance/genai_trust_governance/context_saturation_index](../../../model_policy_engine/policies/ai_governance/genai_trust_governance/context_saturation_index_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
context_saturation_index.py
  compute_context_saturation_index = 0.65
PASS ai_governance/genai_trust_governance
```

<!-- end-observed-output -->

## context_saturation_index.py

### Model context from the archive

GEN-TRUST-002 — context_saturation_index

Purpose
-------
Reusable whenever an advisory model is forced to reason across many competing engineering surfaces under time pressure.

Assumptions
-----------
Trust must decay monotonically as relevant context pressure, conflict density, and source sprawl increase.

### Entry points

- `clamp01(value: float)`
- `compute_context_saturation_index(token_pressure_ratio: float, conflict_count: int, source_count: int, safe_conflict_budget: int=3, safe_source_budget: int=4)`

### Original formula record

- **Formula id**  GEN-TRUST-002
- **Family**  genai_trust_governance
- **Name**  context_saturation_index
- **Symbolic form**  `CSI = clip(w_t*r_token + w_c*r_conflict + w_s*r_source, 0, 1)`
- **Typed inputs**  `token_pressure_ratio` (float), `conflict_count` (int), `source_count` (int), `safe_conflict_budget` (int), `safe_source_budget` (int)
- **Units**  `token_pressure_ratio` (unitless), `conflict_count` (count), `source_count` (count), `safe_conflict_budget` (count), `safe_source_budget` (count), `output` (unitless)
- **Assumptions**  Trust must decay monotonically as relevant context pressure, conflict density, and source sprawl increase.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable whenever an advisory model is forced to reason across many competing engineering surfaces under time pressure.
- **Status**  proposed_for_future_builds
