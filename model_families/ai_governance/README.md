# Ai governance

Bounded governance for generated or successor logic so heuristics stay caged by deterministic acceptance rules.

### Optimal use

Use when prompts, generated plans, tool calls, patches, summaries, or successor updates must remain subordinate to evidence, timing, authority, provenance, and thresholds.

### Do not use when

Do not treat these as direct command authority or as replacements for deterministic safety law.

## Subdirectories

- [genai_governance](genai_governance/README.md)
- [genai_safety_governance](genai_safety_governance/README.md)
- [genai_trust_governance](genai_trust_governance/README.md)
- [genai_truth_governance](genai_truth_governance/README.md)

## Model files

- [ai_candidate_admission.py](ai_candidate_admission.py) — Governed candidate objective
- [multi_agent_consensus.py](multi_agent_consensus.py) — Multi‑agent consensus gate
- [penalized_prompt.py](penalized_prompt.py) — Penalized prompt objective
- [volley_successor.py](volley_successor.py) — Volley successor synthesis update

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [ai_governance/ai_candidate_admission](../../model_policy_engine/policies/ai_governance/ai_candidate_admission_policy.toml)
- [ai_governance/multi_agent_consensus](../../model_policy_engine/policies/ai_governance/multi_agent_consensus_policy.toml)
- [ai_governance/penalized_prompt](../../model_policy_engine/policies/ai_governance/penalized_prompt_policy.toml)
- [ai_governance/volley_successor](../../model_policy_engine/policies/ai_governance/volley_successor_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
ai_candidate_admission.py
  compute_governed_candidate_objective = {"accepted": true, "hard_gate_failures": [], "penalties": {"authority_penalty": 0.0, "hallucination_penalty": 1.0, "physics_penalty": 0.0, "provenance_penalty": 0.0, "schema_penalty": 0.0, "timing_penalty": 0.0}, "reason_code": "ACCEPT_RANKED_SURVIVOR", "score": 4.5, "utility": 5.0}
multi_agent_consensus.py
  consensus_gate = true
penalized_prompt.py
  compute_penalized_objective = 8.0
volley_successor.py
  update_volley_successor = 0.30000000000000004
PASS ai_governance
```

<!-- end-observed-output -->

## ai_candidate_admission.py

### Model context from the archive

AI-GOV-001 — Governed candidate objective.

A generalized Lambda Law for AI-generated or AI-assisted candidate artifacts.
Hard deterministic gates outrank optimization: schema, physics, timing,
authority, and provenance failures reject the candidate immediately.

Only candidates that survive those gates are ranked by a penalized
objective:

    J(c) = U(c)
           - λ_h E_halluc(c)
           - λ_p E_phys(c)
           - λ_s E_schema(c)
           - λ_t E_time(c)
           - λ_a E_authority(c)
           - λ_r E_provenance(c)

This law is intentionally broader than the prompt-specific M9.4 law. Use it
at AI-to-deterministic seams for plans, tool calls, patches, summaries,
scenario proposals, and successor seeds.

### Entry points

- `CandidateObjectiveResult` (type)
- `compute_governed_candidate_objective(utility: float, hallucination_penalty: float, physics_penalty: float, schema_penalty: float, timing_penalty: float, authority_penalty: float, provenance_penalty: float, penalty_weights: Tuple[float, float, float, float, float, float], *, schema_valid: bool, physics_valid: bool, timing_valid: bool, authority_valid: bool, provenance_valid: bool)`

### Original formula record

- **Formula id**  AI-GOV-001
- **Name**  Governed candidate objective
- **Symbolic form**  `J(c) = U(c) - λ_h E_halluc(c) - λ_p E_phys(c) - λ_s E_schema(c) - λ_t E_time(c) - λ_a E_authority(c) - λ_r E_provenance(c); hard gates: schema_valid ∧ physics_valid ∧ timing_valid ∧ authority_valid ∧ provenance_valid`
- **Typed inputs**  `utility` (float), `hallucination_penalty` (float), `physics_penalty` (float), `schema_penalty` (float), `timing_penalty` (float), `authority_penalty` (float), `provenance_penalty` (float), `penalty_weights` (Tuple[float, float, float, float, float, float]), `schema_valid` (bool), `physics_valid` (bool), `timing_valid` (bool), `authority_valid` (bool), `provenance_valid` (bool)
- **Units**  `utility` (utility), `hallucination_penalty` (penalty), `physics_penalty` (penalty), `schema_penalty` (penalty), `timing_penalty` (penalty), `authority_penalty` (penalty), `provenance_penalty` (penalty), `penalty_weights` (unitless), `schema_valid` (bool), `physics_valid` (bool), `timing_valid` (bool), `authority_valid` (bool), `provenance_valid` (bool), `output` (CandidateObjectiveResult)
- **Assumptions**  Penalty terms are non-negative, hard gates are authoritative, and utility is only allowed to rank candidates that already survived deterministic seam validation.

## multi_agent_consensus.py

### Model context from the archive

M9.3 — Multi‑agent consensus gate

This module computes a consensus gate over multiple agent scores.  The
gate returns 1 (True) if the aggregated score meets or exceeds a
threshold ``α`` and 0 (False) otherwise:

    C(y₁, …, y_n) = 1[score(y₁, …, y_n) ≥ α].

The default score is the mean of the input scores, but a custom
aggregation function can be provided.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `consensus_gate(scores: Sequence[float], alpha: float, score_fn: Callable[[Sequence[float]], float] | None=None)`

### Original formula record

- **Formula id**  M9.3
- **Name**  Multi‑agent consensus gate
- **Symbolic form**  `C(y₁, …, y_n) = 1[score(y₁, …, y_n) ≥ α]`
- **Typed inputs**  `scores` (Sequence[float]), `alpha` (float), `score_fn` (Callable)
- **Units**  `scores` (unitless), `alpha` (unitless), `output` (bool)
- **Assumptions**  scores is a sequence of numeric values.  score_fn defaults to the mean.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_multi_agent_consensus.py::test_multi_agent_consensus`, `rtm_link=lambda_laws.multi_agent_consensus`, `ssot_gate=notebooks/gate_multi_agent_consensus.ipynb`

## penalized_prompt.py

### Model context from the archive

M9.4 — Penalized prompt objective

This module implements the penalized prompt objective used in AI
alignment and prompt design:

    J(p) = U(p) − λ₁ E_halluc(p) − λ₂ E_phys(p) − λ₃ E_schema(p),

where ``U(p)`` is the utility of prompt ``p`` and the ``E_*`` terms
measure hallucination, physical infeasibility, and schema violations.  The
λ coefficients determine the penalty weights.

### Entry points

- `compute_penalized_objective(U_p: float, E_halluc: float, E_phys: float, E_schema: float, lambdas: Tuple[float, float, float])`

### Original formula record

- **Formula id**  M9.4
- **Name**  Penalized prompt objective
- **Symbolic form**  `J(p) = U(p) − λ₁ E_halluc(p) − λ₂ E_phys(p) − λ₃ E_schema(p)`
- **Typed inputs**  `U_p` (float), `E_halluc` (float), `E_phys` (float), `E_schema` (float), `lambdas` (Tuple[float, float, float])
- **Units**  `U_p` (utility), `E_halluc` (penalty), `E_phys` (penalty), `E_schema` (penalty), `lambdas` (), `output` (utility)
- **Assumptions**  All penalty functions return non‑negative values.  Higher utility is better.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_penalized_prompt.py::test_penalized_prompt`, `rtm_link=lambda_laws.penalized_prompt`, `ssot_gate=notebooks/gate_penalized_prompt.ipynb`

## volley_successor.py

### Model context from the archive

C.7 — Volley successor synthesis update

This module provides a simple implementation of the successor update law:

    AFB_{k+1} = F(AFB_k, Δ_k, V_term,k),

where AFB stands for Active Fidelity Baseline, Δ_k is the weighted
divergence between reality and the twin at time ``k``, and V_term,k is
the terminal state vector magnitude.  In this simplified version, the
update function ``F`` is defined as:

    F(afb, delta, v_term) = afb + delta - v_term.

This is a placeholder for a more sophisticated update rule.

### Entry points

- `update_volley_successor(afb_k: float, delta_k: float, v_term_k: float)`

### Original formula record

- **Formula id**  C.7
- **Name**  Volley successor synthesis update
- **Symbolic form**  `AFB_{k+1} = F(AFB_k, Δ_k, V_term,k)`
- **Typed inputs**  `afb_k` (float), `delta_k` (float), `v_term_k` (float)
- **Units**  `afb_k` (unit), `delta_k` (unit), `v_term_k` (unit), `output` (unit)
- **Assumptions**  The update law is a placeholder.  In practice, a domain‑specific function should be used to update the active fidelity baseline.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_volley_successor.py::test_volley_successor`, `rtm_link=lambda_laws.volley_successor`, `ssot_gate=notebooks/gate_volley_successor.ipynb`
