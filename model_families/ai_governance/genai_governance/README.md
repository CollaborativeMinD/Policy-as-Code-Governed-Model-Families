# Genai governance

Agent-governance primitives for evidence coverage, contradiction exposure, deterministic parse yield, and stale evidence decay.

### Use cases

- Design reviews, summaries, triage notes, and recommendations that must prove evidence contact.
- Prompt and schema hardening loops.
- Replay packets and cached evidence that lose authority with age.

### Non-use cases

- Do not treat schema validity or citation count as truth.
- Do not use without canonical required references, contradiction flags, and freshness windows.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [contradiction_exposure_score.py](contradiction_exposure_score.py) — contradiction_exposure_score
- [deterministic_parse_yield.py](deterministic_parse_yield.py) — deterministic_parse_yield
- [evidence_coverage_ratio.py](evidence_coverage_ratio.py) — evidence_coverage_ratio
- [stale_evidence_decay.py](stale_evidence_decay.py) — stale_evidence_decay

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [ai_governance/genai_governance/contradiction_exposure_score](../../../model_policy_engine/policies/ai_governance/genai_governance/contradiction_exposure_score_policy.toml)
- [ai_governance/genai_governance/deterministic_parse_yield](../../../model_policy_engine/policies/ai_governance/genai_governance/deterministic_parse_yield_policy.toml)
- [ai_governance/genai_governance/evidence_coverage_ratio](../../../model_policy_engine/policies/ai_governance/genai_governance/evidence_coverage_ratio_policy.toml)
- [ai_governance/genai_governance/stale_evidence_decay](../../../model_policy_engine/policies/ai_governance/genai_governance/stale_evidence_decay_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
contradiction_exposure_score.py
  compute_contradiction_exposure_score = 0.75
deterministic_parse_yield.py
  compute_deterministic_parse_yield = 0.8
evidence_coverage_ratio.py
  compute_evidence_coverage_ratio = 0.5
stale_evidence_decay.py
  compute_stale_evidence_decay = 0.6400000000000001
PASS ai_governance/genai_governance
```

<!-- end-observed-output -->

## contradiction_exposure_score.py

### Model context from the archive

GEN-GOV-005 — contradiction_exposure_score

Purpose
-------
Generic contradiction meter across control, EE, thermal, terrain, policy, and mission-summary lanes.

Assumptions
-----------
Weights emphasize high-consequence contradictions such as live death states, hold posture, terrain-provenance failures, or EPS fabrication.

### Entry points

- `clamp01(value: float)`
- `compute_contradiction_exposure_score(contradiction_flags: Sequence[bool], weights: Sequence[float] | None=None)`

### Original formula record

- **Formula id**  GEN-GOV-005
- **Family**  genai_governance
- **Name**  contradiction_exposure_score
- **Symbolic form**  `CES = (Σ_i w_i * I(contradiction_i)) / Σ_i w_i`
- **Typed inputs**  `contradiction_flags` (Sequence[bool]), `weights` (Sequence[float] | None)
- **Units**  `contradiction_flags` (unitless), `weights` (unitless), `output` (unitless)
- **Assumptions**  Weights emphasize high-consequence contradictions such as live death states, hold posture, terrain-provenance failures, or EPS fabrication.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Generic contradiction meter across control, EE, thermal, terrain, policy, and mission-summary lanes.
- **Status**  proposed_for_future_builds

## deterministic_parse_yield.py

### Model context from the archive

GEN-GOV-007 — deterministic_parse_yield

Purpose
-------
Works for prompt hardening, contract replay, test loops, and multi-sample evaluation.

Assumptions
-----------
A lane that cannot stay inside schema under repetition has no business touching important summaries.

### Entry points

- `compute_deterministic_parse_yield(schema_valid_outputs: int, total_outputs: int)`

### Original formula record

- **Formula id**  GEN-GOV-007
- **Family**  genai_governance
- **Name**  deterministic_parse_yield
- **Symbolic form**  `DPY = N_schema_valid_outputs / N_total_outputs`
- **Typed inputs**  `schema_valid_outputs` (int), `total_outputs` (int)
- **Units**  `schema_valid_outputs` (count), `total_outputs` (count), `output` (unitless)
- **Assumptions**  A lane that cannot stay inside schema under repetition has no business touching important summaries.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Works for prompt hardening, contract replay, test loops, and multi-sample evaluation.
- **Status**  proposed_for_future_builds

## evidence_coverage_ratio.py

### Model context from the archive

GEN-GOV-004 — evidence_coverage_ratio

Purpose
-------
Reusable anywhere a model must prove it actually touched the required evidence instead of bluffing.

Assumptions
-----------
Required references are canonical artifact refs or public source IDs material to the claim surface.

### Entry points

- `compute_evidence_coverage_ratio(required_refs: Sequence[str], cited_refs: Sequence[str])`

### Original formula record

- **Formula id**  GEN-GOV-004
- **Family**  genai_governance
- **Name**  evidence_coverage_ratio
- **Symbolic form**  `ECR = |R_required ∩ R_cited| / |R_required|`
- **Typed inputs**  `required_refs` (Sequence[str]), `cited_refs` (Sequence[str])
- **Units**  `required_refs` (count), `cited_refs` (count), `output` (unitless)
- **Assumptions**  Required references are canonical artifact refs or public source IDs material to the claim surface.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable anywhere a model must prove it actually touched the required evidence instead of bluffing.
- **Status**  proposed_for_future_builds

## stale_evidence_decay.py

### Model context from the archive

GEN-GOV-009 — stale_evidence_decay

Purpose
-------
Reusable for telemetry, replay packets, test evidence, issue triage, and advisory summaries that age out.

Assumptions
-----------
Freshness collapses to zero once evidence ages beyond the allowed coherence window unless a wider contract explicitly says otherwise.

### Entry points

- `compute_stale_evidence_decay(age_s: float, freshness_margin_s: float, decay_power: float=1.0)`

### Original formula record

- **Formula id**  GEN-GOV-009
- **Family**  genai_governance
- **Name**  stale_evidence_decay
- **Symbolic form**  `F = max(0, 1 - age / tau_fresh)^p`
- **Typed inputs**  `age_s` (float), `freshness_margin_s` (float), `decay_power` (float)
- **Units**  `age_s` (s), `freshness_margin_s` (s), `decay_power` (unitless), `output` (unitless)
- **Assumptions**  Freshness collapses to zero once evidence ages beyond the allowed coherence window unless a wider contract explicitly says otherwise.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable for telemetry, replay packets, test evidence, issue triage, and advisory summaries that age out.
- **Status**  proposed_for_future_builds
