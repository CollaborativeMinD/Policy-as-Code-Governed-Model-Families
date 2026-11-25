---
name: model-policy-admission
description: Maintain the shared TOML admission engine, signed deployment state and model contracts in this bundle.
---

# Model policy admission

Read the [deployment guide](README.md) and the owning model’s README and fixtures. Keep the catalog identity bound to the signed content and deployment path. Runtime model calls consume verified snapshots. Signing and initialization belong to explicit operator commands.

For a tuning change, exercise the draft through `apply` and call the model through its ordinary interface. Verify rejection, last-known-good recovery and isolation from a second model when changing admission logic. Preserve the loader’s canonical payloads and the exact numeric and label fixtures in the model families. Run the engine tests and the family smoke suite listed in the deployment guide.


When a requested field or operation is unbound, capture the failing call first. Develop the missing runtime behavior, check an independent numerical reference, then repeat publication and the ordinary call. Keep configurable values in the model’s TOML. Run the catalog tests and reviewed fixture replay before release. [Commands and evidence](../verification/Review.md)
