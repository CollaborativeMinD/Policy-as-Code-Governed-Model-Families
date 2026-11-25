# Sampling based reachability search tests

Regression tests for the models one directory above. The runner uses the supplied family and runs the behavioral assertions against its current filenames.

## Regression suites

- [test_sampling_reachability_model.py](test_sampling_reachability_model.py)

The smoke runner also executes the supplied seeded demo in `run_sampling_reachability_demo.py`.

## Admitted model policies

This directory runs fixtures for the models in the linked family directories. Each model owns its policy. The smoke run provisions the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

## Working baseline

Run `python smoke_test.py` in this directory. The runner executes the local regression suite.

<!-- observed-output -->

```text
CLEAR_PATH_STATUS: REACHABILITY_WITNESS_FOUND
CLEAR_PATH_SUCCESS: True
CLEAR_PATH_ACCEPTED_NODES: 45
CLEAR_PATH_REJECTED_NODES: 1
CLEAR_PATH_LENGTH: 15.2
BLOCKED_PATH_STATUS: COLLAPSE_PRESSURE_DOMINANT
BLOCKED_PATH_SUCCESS: False
BLOCKED_PATH_ACCEPTED_NODES: 1
BLOCKED_PATH_REJECTED_NODES: 120
BLOCKED_COLLAPSE_PRESSURE: 1.0
CAMPAIGN_SUMMARY:
{
  "campaign_count": 12,
  "collapse_dominant_count": 0,
  "collapse_dominant_probability": 0.0,
  "success_count": 12,
  "success_probability": 1.0
}
test_sampling_reachability_model.py: 7 passed, 0 skipped
PASS sampling_based_reachability_search/Tests
```

<!-- end-observed-output -->
