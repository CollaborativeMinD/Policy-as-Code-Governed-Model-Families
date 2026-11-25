---
name: model-thermal-cross-domain-models
description: Maintain thermal cross domain models in the consolidated model collection and verify its local working baseline.
---

# Thermal cross domain models

This directory collects power_thermal_coupling, thermal_environment_validity, thermal_rc_envelope, thermal_telemetry_governance, thermal_timing_authority. Follow the README and skill in the child that owns the model. Keep the children independently executable. Run `python smoke_test.py` here to check the aggregate and record observed results in [README.md](README.md).

Use the model IDs and baseline policies listed in the [directory README](README.md#admitted-model-policies). Change tuning, defaults and admissible ranges in the owning TOML. Keep reference fixtures independent of the values being tested. Apply a changed policy in a disposable deployment and check both its effect and an unaffected model before accepting a new baseline.
