---
name: model-network-and-compute
description: Maintain network and compute in the consolidated model collection and verify its local working baseline.
---

# Network and compute

This directory collects compute_queueing_limits, network_execution_bounds. Follow the README and skill in the child that owns the model. Keep the children independently executable. Run `python smoke_test.py` here to check the aggregate and record observed results in [README.md](README.md).

Use the model IDs and baseline policies listed in the [directory README](README.md#admitted-model-policies). Change tuning, defaults and admissible ranges in the owning TOML. Keep reference fixtures independent of the values being tested. Apply a changed policy in a disposable deployment and check both its effect and an unaffected model before accepting a new baseline.
