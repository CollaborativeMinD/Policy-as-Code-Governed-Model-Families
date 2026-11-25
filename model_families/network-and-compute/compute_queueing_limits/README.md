# Compute queueing limits

### Use cases

Use this set when modeling hard compute ceilings, serial bottlenecks, ingestion queues, backlog growth, and throttling conditions.

### Non-use cases

Do not use this set as:

- a full cluster simulator,
- a scheduler,
- a Kubernetes autoscaler,
- a replacement for measured latency and throughput telemetry.

## Model files

- [amdahl_cluster_limit.py](amdahl_cluster_limit.py) — Illusion of the Cluster
- [littles_law_queue.py](littles_law_queue.py) — DOM Preventer

## Regression suites

- [test_compute_queueing_limits.py](test_compute_queueing_limits.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [network-and-compute/compute_queueing_limits/amdahl_cluster_limit](../../../model_policy_engine/policies/network-and-compute/compute_queueing_limits/amdahl_cluster_limit_policy.toml)
- [network-and-compute/compute_queueing_limits/littles_law_queue](../../../model_policy_engine/policies/network-and-compute/compute_queueing_limits/littles_law_queue_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

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
```

<!-- end-observed-output -->

## amdahl_cluster_limit.py

### Model context from the archive

PCC-16 — Illusion of the Cluster, Amdahl's Law.

Paper law:
    S(s) = 1 / ((1 - p) + p/s)

Runtime role:
    Proves adding nodes does not create infinite speed when serial work remains.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_amdahl_speedup(parallel_fraction: float, workers: float)`

### Original formula record

- **Formula id**  PCC-16
- **Name**  Illusion of the Cluster
- **Family**  compute_queueing_limits
- **Symbolic form**  `S(s)=\frac{1}{(1-p)+\frac{p}{s}}`
- **Typed inputs**  `parallel_fraction` (float), `workers` (float)
- **Output**  float
- **Units**  speedup
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## littles_law_queue.py

### Model context from the archive

PCC-17 — DOM Preventer, Little's Law.

Paper law:
    L = lambda * W

Runtime role:
    Relates queue length, arrival rate, and processing time to trigger throttling before RAM exhaustion.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_little_law_queue_length(arrival_rate_per_s: float, processing_time_s: float)`
- `compute_queue_margin(arrival_rate_per_s: float, processing_time_s: float, queue_limit: float)`
- `should_throttle(arrival_rate_per_s: float, processing_time_s: float, queue_limit: float)`

### Original formula record

- **Formula id**  PCC-17
- **Name**  DOM Preventer
- **Family**  compute_queueing_limits
- **Symbolic form**  `L=\lambda W`
- **Typed inputs**  `arrival_rate_per_s` (float), `processing_time_s` (float), `queue_limit` (float)
- **Output**  float/bool
- **Units**  items
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.
