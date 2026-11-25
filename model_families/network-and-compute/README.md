# Network and compute

## Subdirectories

- [compute_queueing_limits](compute_queueing_limits/README.md)
- [network_execution_bounds](network_execution_bounds/README.md)

## Admitted model policies

This directory runs fixtures for the models in the linked family directories. Each model owns its policy. The smoke run provisions the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

## Working baseline

Run `python smoke_test.py` in this directory. This directory aggregates the child runners.

<!-- observed-output -->

```text
amdahl_cluster_limit.py
  compute_amdahl_speedup = 2.0
  lambdified = -2.9999999999999996
littles_law_queue.py
  compute_little_law_queue_length = 5.0
  compute_queue_margin = 3.0
  should_throttle = true
  lambdified = 6.0
test_compute_queueing_limits.py: 2 passed, 0 skipped
PASS network-and-compute/compute_queueing_limits
doda_latency_bound.py
  compute_latency_budget_margin = 0.4
  within_latency_budget = true
  lambdified_margin = -1.0
k_connectivity_survival.py
  has_two_independent_paths = true
  lambdified_margin = 0.0
quarantine_blast_radius.py
  shortest_hop_distances = {"a": 0, "b": 1, "c": 2}
  compute_blast_radius = 2
  lambdified_distance_identity = 2.0
shannon_hartley_capacity.py
  compute_channel_capacity_bps = 200.0
  lambdified = 1.6147098441152081
test_network_execution_bounds.py: 4 passed, 0 skipped
PASS network-and-compute/network_execution_bounds
PASS network-and-compute
```

<!-- end-observed-output -->
