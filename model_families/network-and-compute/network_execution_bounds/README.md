# Network execution bounds

### Use cases

Use this set to evaluate whether telemetry can move, whether graph routing survives single-node failure, whether a compromised node is bounded, and whether processing/network hops fit inside mission reaction time.

### Non-use cases

Do not use this set as:

- a full RF propagation model,
- a network simulator,
- a Byzantine consensus proof,
- a cyber containment certification.

## Model files

- [doda_latency_bound.py](doda_latency_bound.py) — DODA Law
- [k_connectivity_survival.py](k_connectivity_survival.py) — Single Point of Failure Law
- [quarantine_blast_radius.py](quarantine_blast_radius.py) — Quarantine Boundary
- [shannon_hartley_capacity.py](shannon_hartley_capacity.py) — Limit of the Invisible Thread

## Regression suites

- [test_network_execution_bounds.py](test_network_execution_bounds.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../../model_policy_engine/README.md)

- [network-and-compute/network_execution_bounds/doda_latency_bound](../../../model_policy_engine/policies/network-and-compute/network_execution_bounds/doda_latency_bound_policy.toml)
- [network-and-compute/network_execution_bounds/k_connectivity_survival](../../../model_policy_engine/policies/network-and-compute/network_execution_bounds/k_connectivity_survival_policy.toml)
- [network-and-compute/network_execution_bounds/quarantine_blast_radius](../../../model_policy_engine/policies/network-and-compute/network_execution_bounds/quarantine_blast_radius_policy.toml)
- [network-and-compute/network_execution_bounds/shannon_hartley_capacity](../../../model_policy_engine/policies/network-and-compute/network_execution_bounds/shannon_hartley_capacity_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
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
```

<!-- end-observed-output -->

## doda_latency_bound.py

### Model context from the archive

PCC-11 — DODA Law, kinetic latency bound.

Paper law:
    sum_i^k T_node_i <= T_budget

Runtime role:
    The sum of all processing and network hops must fit inside mission reaction time.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified_margin()`
- `compute_latency_budget_margin(hop_latencies_s: Sequence[float], time_budget_s: float)`
- `within_latency_budget(hop_latencies_s: Sequence[float], time_budget_s: float)`

### Original formula record

- **Formula id**  PCC-11
- **Name**  DODA Law
- **Family**  network_execution_bounds
- **Symbolic form**  `\sum_{i=1}^{k}T_{node-i}\le T_{budget}`
- **Typed inputs**  `hop_latencies_s` (Sequence[float]), `time_budget_s` (float)
- **Output**  float
- **Units**  seconds margin
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## k_connectivity_survival.py

### Model context from the archive

PCC-09 — Single Point of Failure Law, k-connectivity.

Paper law:
    k(G) >= 2

Runtime role:
    Requires at least two independent routing paths so one node failure does not kill the mesh.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified_margin()`
- `has_two_independent_paths(nodes: Iterable[str], edges: Iterable[tuple[str, str]])`

### Original formula record

- **Formula id**  PCC-09
- **Name**  Single Point of Failure Law
- **Family**  network_execution_bounds
- **Symbolic form**  `\kappa(G)\ge 2`
- **Typed inputs**  `nodes` (Iterable[str]), `edges` (Iterable[tuple[str,str]])
- **Output**  bool
- **Units**  graph connectivity
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## quarantine_blast_radius.py

### Model context from the archive

PCC-10 — Quarantine Boundary, blast radius.

Paper law:
    R_b(v) = max_{u in A(v)} d_G(v,u)

Runtime role:
    Computes how far corrupted data can travel from a compromised node before containment.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified_distance_identity()`
- `shortest_hop_distances(source: str, edges: Iterable[tuple[str, str]])`
- `compute_blast_radius(source: str, affected_nodes: Iterable[str], edges: Iterable[tuple[str, str]])`

### Original formula record

- **Formula id**  PCC-10
- **Name**  Quarantine Boundary
- **Family**  network_execution_bounds
- **Symbolic form**  `R_b(v)=\max_{u\in A(v)}d_G(v,u)`
- **Typed inputs**  `source` (str), `affected_nodes` (Iterable[str]), `edges` (Iterable[tuple[str,str]])
- **Output**  int
- **Units**  graph hops
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.

## shannon_hartley_capacity.py

### Model context from the archive

PCC-08 — Limit of the Invisible Thread, Shannon-Hartley capacity.

Paper law:
    C = B log2(1 + S/N)

Runtime role:
    Defines the absolute physical ceiling of a noisy telemetry channel.

### Current interface

- The symbolic accessor returns expression text. Each supplied callable factory retains its positional argument order and evaluates with Python scalars.

### Entry points

- `symbolic_expression()`
- `lambdified()`
- `compute_channel_capacity_bps(bandwidth_hz: float, signal_power_w: float, noise_power_w: float)`

### Original formula record

- **Formula id**  PCC-08
- **Name**  Limit of the Invisible Thread
- **Family**  network_execution_bounds
- **Symbolic form**  `C=B\log_2(1+\frac{S}{N})`
- **Typed inputs**  `bandwidth_hz` (float), `signal_power_w` (float), `noise_power_w` (float)
- **Output**  float
- **Units**  bits/s
- **Runtime class**  runtime_safe

Additional reference comparisons during migration: 5.
