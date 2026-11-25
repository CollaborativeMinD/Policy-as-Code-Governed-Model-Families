# ai_governance

Historical family notes from the supplied archive. The current filenames, interfaces, and observed working baseline are in [README.md](README.md).

**Family tail:** `README.ai_governance.md`

## Why this family exists
Bounded governance for generated or successor logic so heuristics stay caged by deterministic acceptance rules.

## Cross-domain use cases
AI-assisted scenario generation; governed prompt and artifact evaluation; tool-call admission; patch promotion; successor volley updates after failure.

## Optimal use
Use when prompts, generated plans, tool calls, patches, summaries, or successor updates must remain subordinate to evidence, timing, authority, provenance, and thresholds.

## Do not use when
Do not treat these as direct command authority or as replacements for deterministic safety law.

## Canonical formulas in this family

- **AI-GOV-001** `ai_gov_001__ai_governance__governed_candidate_objective.py`: Governed candidate objective
  - Symbolic form: `J(c) = U(c) - λ_h E_halluc(c) - λ_p E_phys(c) - λ_s E_schema(c) - λ_t E_time(c) - λ_a E_authority(c) - λ_r E_provenance(c)` with hard gates for schema, physics, timing, authority, and provenance.
  - Why kept: New Lambda Law that generalizes the prompt-specific penalized objective into a governed candidate-admission primitive at AI-to-deterministic seams.
- **C.7** `c_7__ai_governance__volley_successor_synthesis_update.py`: Volley successor synthesis update
  - Symbolic form: `AFB_{k+1} = F(AFB_k, Δ_k, V_term,k)`
  - Why kept: Base compendium law canonicalized for searchability.
- **M9.4** `m9_4__ai_governance__penalized_prompt_objective.py`: Penalized prompt objective
  - Symbolic form: `J(p) = U(p) − λ₁ E_halluc(p) − λ₂ E_phys(p) − λ₃ E_schema(p)`
  - Why kept: Base compendium law canonicalized for searchability. Treated as the prompt-specialized companion to AI-GOV-001.

## Underlying formula concepts

These laws are reusable starting primitives for humans, agents, and HIL operators. Pair them with timing, provenance, and authority shelves whenever the thread is mission-critical. AI-GOV-001 is the broader seam law; M9.4 remains the prompt-focused specialization.
