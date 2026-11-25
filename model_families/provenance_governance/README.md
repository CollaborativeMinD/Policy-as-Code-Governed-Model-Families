# Provenance governance

Source ceiling and completeness checks for replayable, auditable, and bounded claims.

### Use cases

- Replay payload validation.
- Schema migration and handoff validation.
- Preventing planning-grade or proxy products from being promoted into certification truth.

### Non-use cases

- Do not use completeness as authenticity proof.
- Do not use an unordered or undefined claim ladder.

## Subdirectories

- [tests](tests/README.md)

## Model files

- [lineage_completeness_margin.py](lineage_completeness_margin.py) — lineage_completeness_margin
- [provenance_completeness_margin.py](provenance_completeness_margin.py) — provenance_completeness_margin
- [provenance_truth_ceiling.py](provenance_truth_ceiling.py) — Provenance truth ceiling law

## Missing source

The source-claim ceiling gate named in the original suite is absent. Its original expectations admitted REGION_PROXY under PAD_TILE_INGESTED and rejected SITE_CERTIFIED under REGION_PROXY. The suite records the missing case as skipped. The supplied numeric provenance truth ceiling has its own fixture.

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [provenance_governance/lineage_completeness_margin](../../model_policy_engine/policies/provenance_governance/lineage_completeness_margin_policy.toml)
- [provenance_governance/provenance_completeness_margin](../../model_policy_engine/policies/provenance_governance/provenance_completeness_margin_policy.toml)
- [provenance_governance/provenance_truth_ceiling](../../model_policy_engine/policies/provenance_governance/provenance_truth_ceiling_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
lineage_completeness_margin.py
  compute_lineage_completeness_margin = 0
provenance_completeness_margin.py
  compute_provenance_completeness_margin = -1
provenance_truth_ceiling.py
  compute_provenance_truth_ceiling = 0.4
PASS provenance_governance
```

<!-- end-observed-output -->

## lineage_completeness_margin.py

### Model context from the archive

TRACE-GOV-004 — lineage_completeness_margin

Purpose
-------
Turns missing lineage into a countable regression instead of a vague warning.

Assumptions
-----------
Every required field must be present and materially non-empty.

### Entry points

- `compute_lineage_completeness_margin(required_fields: list[str], payload: dict[str, object])`

### Original formula record

- **Formula id**  TRACE-GOV-004
- **Family**  provenance_governance
- **Name**  lineage_completeness_margin
- **Symbolic form**  `m_lineage = n_present_required - n_required`
- **Typed inputs**  `required_fields` (list[str]), `payload` (dict[str, object])
- **Units**  `required_fields` (unitless), `payload` (unitless), `output` (count)
- **Assumptions**  Every required field must be present and materially non-empty.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Turns missing lineage into a countable regression instead of a vague warning.
- **Status**  proposed_for_future_builds

## provenance_completeness_margin.py

### Model context from the archive

TRACE-GOV-003 — provenance_completeness_margin

Purpose
-------
Replay audits, interface certification prep, red-team payload degradation, and contract migration tracking.

Assumptions
-----------
A boolean provenance gate hides how incomplete a payload really is. This margin makes absence countable so regression tests and replay audits can show whether the problem is one missing field or a whole rotten payload.

### Entry points

- `compute_provenance_completeness_margin(required_fields: list[str], payload: dict[str, object])`

### Original formula record

- **Formula id**  TRACE-GOV-003
- **Family**  provenance_governance
- **Name**  provenance_completeness_margin
- **Symbolic form**  `m_prov = n_present_required_fields - n_required_fields`
- **Typed inputs**  `required_fields` (list[str]), `payload` (dict[str, object])
- **Units**  `required_fields` (unitless), `payload` (unitless), `output` (count)
- **Assumptions**  A boolean provenance gate hides how incomplete a payload really is. This margin makes absence countable so regression tests and replay audits can show whether the problem is one missing field or a whole rotten payload.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Multi use role**  Replay audits, interface certification prep, red-team payload degradation, and contract migration tracking.
- **Status**  proposed_for_future_builds

## provenance_truth_ceiling.py

### Model context from the archive

G1.1 — Provenance truth ceiling law

Purpose
-------
Computes the maximum confidence ceiling a system is allowed to claim from source
tier, lineage completeness, contract validity, temporal validity, and semantic
alignment. This is the anti-laundering law. It stops regional truth from
cosplaying as local truth and prototype evidence from sneaking into deployment.

### Entry points

- `compute_provenance_truth_ceiling(source_ceiling: float, lineage_completeness: float, contract_validity: float, temporal_validity: float, semantic_alignment: float)`

### Original formula record

- **Formula id**  G1.1
- **Name**  Provenance truth ceiling law
- **Symbolic form**  `C_truth = min(C_source, C_lineage, C_contract, C_temporal, C_semantic)`
- **Typed inputs**  `source_ceiling` (float), `lineage_completeness` (float), `contract_validity` (float), `temporal_validity` (float), `semantic_alignment` (float)
- **Units**  `source_ceiling` (unitless), `lineage_completeness` (unitless), `contract_validity` (unitless), `temporal_validity` (unitless), `semantic_alignment` (unitless), `output` (unitless)
- **Assumptions**  All confidence terms are normalized to [0,1]. Final trust may never exceed the weakest governing term.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Primary gaps closed**  provenance governance and truth ceilings, source claim ceiling, lineage completeness, lane-aware confidence ceilings
