# Genai truth governance

Divergence control for heuristic suggestions against deterministic baselines.

### Use cases

- Code suggestions, triage recommendations, plan suggestions, and summary deltas that must remain near a deterministic baseline.
- Simulation assistants proposing bounded maneuver changes.
- Review copilots with a governed divergence leash.

### Non-use cases

- Do not use without a deterministic baseline vector and meaningful weights.
- Do not let a positive margin certify the proposed action; it only bounds divergence.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [generative_divergence_margin.py](generative_divergence_margin.py) — generative_divergence_margin

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [ai_governance/genai_truth_governance/generative_divergence_margin](../../../model_policy_engine/policies/ai_governance/genai_truth_governance/generative_divergence_margin_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
generative_divergence_margin.py
  compute_generative_divergence_margin = 1.0
PASS ai_governance/genai_truth_governance
```

<!-- end-observed-output -->

## generative_divergence_margin.py

### Model context from the archive

GEN-TRUTH-001 — generative_divergence_margin

Purpose
-------
Reusable for advisory, planning, triage, summarization, or code-suggestion lanes that must stay near a bounded baseline.

Assumptions
-----------
Positive margin means the heuristic remains inside the allowed divergence leash relative to deterministic truth.

### Entry points

- `weighted_quadratic_norm(a, b, weights)`
- `compute_generative_divergence_margin(suggestion_vector: Sequence[float], baseline_vector: Sequence[float], allowed_bound: float, weights: Sequence[Sequence[float]] | None=None)`

### Original formula record

- **Formula id**  GEN-TRUTH-001
- **Family**  genai_truth_governance
- **Name**  generative_divergence_margin
- **Symbolic form**  `m_gen = tau_gen - ||x_gen - x_base||_W`
- **Typed inputs**  `suggestion_vector` (Sequence[float]), `baseline_vector` (Sequence[float]), `allowed_bound` (float), `weights` (Sequence[Sequence[float]] | None)
- **Units**  `suggestion_vector` (state), `baseline_vector` (state), `allowed_bound` (state), `weights` (unitless), `output` (state)
- **Assumptions**  Positive margin means the heuristic remains inside the allowed divergence leash relative to deterministic truth.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Reusable for advisory, planning, triage, summarization, or code-suggestion lanes that must stay near a bounded baseline.
- **Status**  proposed_for_future_builds
