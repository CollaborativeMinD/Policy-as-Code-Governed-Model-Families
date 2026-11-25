# Provenance governance tests

Regression tests for the models one directory above. The runner uses the supplied family and runs the behavioral assertions against its current filenames.

## Regression suites

- [test_provenance_governance.py](test_provenance_governance.py)

## Admitted model policies

This directory runs fixtures for the models in the linked family directories. Each model owns its policy. The smoke run provisions the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

## Working baseline

Run `python smoke_test.py` in this directory. The runner executes the local regression suite.

<!-- observed-output -->

```text
test_provenance_governance.py: 2 passed, 1 skipped
  SKIP test_source_claim_ceiling_gate: Source-claim ceiling gate implementation absent from the supplied archive
PASS provenance_governance/tests
```

<!-- end-observed-output -->
