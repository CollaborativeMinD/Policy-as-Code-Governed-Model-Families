---
name: model-electrical
description: Maintain electrical in the consolidated model collection and verify its local working baseline.
---

# Electrical

This directory owns `bus_anchor_consistency_margin.py`, `electrical_survivability_margins.py`, `illumination_cycle_energy_margin.py`, `occlusion_energy_reserve_margin.py`, `regulation_chain_disparity_margin.py`.

Read the model’s record and fixture in [README.md](README.md) and [smoke_test.py](smoke_test.py) before editing. Preserve its formula, units, public call signature, return ordering, threshold inclusivity, and invalid-input rules. Keep model math local. A copied file must resolve its own admitted policy through the standard-library model policy engine. Keep model-specific helpers with their caller. Store provenance, catalog records, and measured outputs in this README.

When changing a model, run `python smoke_test.py` here. Add a fixed fixture for a new model. Investigate a mismatch against the original inputs and the owning formula before updating the recorded baseline.

Use the model IDs and baseline policies listed in the [directory README](README.md#admitted-model-policies). Change tuning, defaults and admissible ranges in the owning TOML. Keep reference fixtures independent of the values being tested. Apply a changed policy in a disposable deployment and check both its effect and an unaffected model before accepting a new baseline.
