# Thermal distortion tests

Regression tests for the models one directory above. The runner uses the supplied family and runs the behavioral assertions against its current filenames.

## Regression suites

- [test_thermal_distortion.py](test_thermal_distortion.py)

## Admitted model policies

This directory runs fixtures for the models in the linked family directories. Each model owns its policy. The smoke run provisions the shipped settings. [Policy setup and publication](../../../../../../model_policy_engine/README.md)

## Working baseline

Run `python smoke_test.py` in this directory. The runner executes the local regression suite.

<!-- observed-output -->

```text
test_thermal_distortion.py: 2 passed, 0 skipped
PASS hardware_viability/thermal/thermal_truth/thermal_distortion/tests
```

<!-- end-observed-output -->
