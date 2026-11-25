---
name: model-plant-abortability-tests
description: Maintain plant abortability tests in the consolidated model collection and verify its local working baseline.
---

# Plant abortability tests

Maintain `test_plant_abortability.py`. Load the models from the immediate parent directory in this family. Keep the original assertion inputs and expected outcomes across filename changes. Record absent implementations explicitly. Run `python smoke_test.py` and record the observed suite results in [README.md](README.md).

Use the model IDs and baseline policies listed in the [directory README](README.md#admitted-model-policies). Change tuning, defaults and admissible ranges in the owning TOML. Keep reference fixtures independent of the values being tested. Apply a changed policy in a disposable deployment and check both its effect and an unaffected model before accepting a new baseline.
