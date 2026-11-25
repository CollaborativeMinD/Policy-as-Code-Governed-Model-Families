# Graph survivability

## Model files

- [blast_radius.py](blast_radius.py) — Blast radius over graph topology
- [consensus_dynamics.py](consensus_dynamics.py) — Consensus dynamics over graph topology
- [graph_survivability.py](graph_survivability.py) — Critical connectivity after node loss
- [isolation_condition.py](isolation_condition.py) — Isolation timing condition

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [graph-survivability/blast_radius](../../model_policy_engine/policies/graph-survivability/blast_radius_policy.toml)
- [graph-survivability/consensus_dynamics](../../model_policy_engine/policies/graph-survivability/consensus_dynamics_policy.toml)
- [graph-survivability/graph_survivability](../../model_policy_engine/policies/graph-survivability/graph_survivability_policy.toml)
- [graph-survivability/isolation_condition](../../model_policy_engine/policies/graph-survivability/isolation_condition_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
blast_radius.py
  compute_blast_radius = 2
consensus_dynamics.py
  compute_consensus_update = [1.5, 2.5]
graph_survivability.py
  compute_vertex_connectivity = 2
  is_graph_survivable = true
  compute_vertex_connectivity = 0
isolation_condition.py
  check_isolation_condition = true
PASS graph-survivability
```

<!-- end-observed-output -->

## blast_radius.py

### Model context from the archive

M2.2 — Blast radius over graph topology

The blast radius ``R_b(v)`` of a node ``v`` is the maximum graph
distance to any other node reachable from ``v``.  Formally,

    R_b(v) = max_{u ∈ V} d_G(v, u),

where ``d_G`` denotes the shortest‑path distance in graph ``G`` and
``V`` is the set of vertices reachable from ``v``.  In practice, this
is computed via a breadth‑first search (BFS) on an unweighted,
undirected graph.

### Entry points

- `compute_blast_radius(graph: Dict[str, Sequence[str]], v: str)`

### Original formula record

- **Formula id**  M2.2
- **Name**  Blast radius over graph topology
- **Symbolic form**  `R_b(v) = max_{u ∈ A(v)} d_G(v,u)`
- **Typed inputs**  `graph` (Dict[Hashable, Sequence[Hashable]]), `v` (Hashable)
- **Units**  `graph` (), `v` (), `output` (edges)
- **Assumptions**  Graph is unweighted and undirected.  All vertices reachable from v are included when computing the maximum shortest‑path distance.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_blast_radius.py::test_blast_radius`, `rtm_link=lambda_laws.blast_radius`, `ssot_gate=notebooks/gate_blast_radius.ipynb`

## consensus_dynamics.py

### Model context from the archive

M2.5 — Consensus dynamics over graph topology

This module implements a single discrete consensus update step
according to

    x_{k+1} = x_k − α L x_k,

where ``x`` is the vector of agent states, ``α`` is a positive step
size, and ``L`` is the graph Laplacian matrix.  The continuous
analogue is \dot{x} = −L x.

### Current interface

- The numerical implementation uses Python scalars and sequences. Vector and matrix outputs use lists and nested lists.

### Entry points

- `compute_consensus_update(x: Sequence[float], L: Sequence[Sequence[float]], alpha: float)`

### Original formula record

- **Formula id**  M2.5
- **Name**  Consensus dynamics over graph topology
- **Symbolic form**  `ẋ = −L x ; discrete: x_(k+1) = x_k − α L x_k`
- **Typed inputs**  `x` (Sequence[float]), `L` (Sequence[Sequence[float]]), `alpha` (float)
- **Units**  `x` (unitless), `L` (unitless), `alpha` (unitless), `output` (unitless)
- **Assumptions**  L must be a square matrix with dimensions matching the length of x. Alpha must be positive and sufficiently small to ensure stability.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_consensus_dynamics.py::test_consensus_update`, `rtm_link=lambda_laws.consensus_dynamics`, `ssot_gate=notebooks/gate_consensus_dynamics.ipynb`

Additional reference comparisons during migration: 50.

## graph_survivability.py

### Model context from the archive

M2.3 — Critical connectivity after node loss

This module implements a simple connectivity check for an undirected
graph.  The compendium states that the graph must remain at least
2‑connected after the loss of any single node:

    κ(G_c) ≥ 2,

where κ(G_c) is the vertex connectivity.  We compute the minimum
vertex cut of the graph using NetworkX and return either the
connectivity value or a boolean indicating whether the condition is
satisfied.

### Current interface

- Supply a mapping from each node to its neighbors. Connectivity is defined for simple undirected graphs. The empty graph raises ValueError.

### Entry points

- `compute_vertex_connectivity(graph: Mapping[Hashable, Iterable[Hashable]])`
- `is_graph_survivable(graph: Mapping[Hashable, Iterable[Hashable]], threshold: int=2)`

### Original formula record

- **Formula id**  M2.3
- **Name**  Critical connectivity after node loss
- **Symbolic form**  `κ(G_c) ≥ 2`
- **Typed inputs**  `graph` (networkx.Graph), `threshold` (int)
- **Units**  `graph` (), `threshold` (), `output` (int)
- **Assumptions**  Graph is undirected and unweighted.  The vertex connectivity κ(G) is the size of the smallest set of vertices whose removal disconnects the graph.  A connectivity ≥ 2 indicates that the graph can survive any single node failure.
- **Runtime class**  offline_only
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_graph_survivability.py::test_graph_connectivity`, `rtm_link=lambda_laws.graph_survivability`, `ssot_gate=notebooks/gate_graph_survivability.ipynb`

Additional reference comparisons during migration: 1100.

## isolation_condition.py

### Model context from the archive

M2.4 — Isolation timing condition

This module implements the isolation timing condition for a node in a
communication or control graph.  The condition states that when a
failure event ``F(v)`` occurs, the time to isolate the faulty node
must not exceed the isolation threshold ``τ_isolate``:

    F(v) ⇒ cut(v, C) ≤ τ_isolate.

We model ``cut(v, C)`` as a measured time to isolate ``v`` from the
rest of the cluster ``C`` and return a boolean indicating whether the
condition is satisfied.

### Entry points

- `check_isolation_condition(time_to_isolate: float, tau_isolate: float)`

### Original formula record

- **Formula id**  M2.4
- **Name**  Isolation timing condition
- **Symbolic form**  `F(v) ⇒ cut(v, C) ≤ τ_isolate`
- **Typed inputs**  `time_to_isolate` (float), `tau_isolate` (float)
- **Units**  `time_to_isolate` (s), `tau_isolate` (s), `output` (bool)
- **Assumptions**  time_to_isolate is a non‑negative scalar representing the measured time to isolate the failing node.  tau_isolate is the maximum allowable isolation time.
- **Runtime class**  runtime_safe
- **Deployment class**  prototype
- **Historical trace references from the archive**  `tests=tests/test_isolation_condition.py::test_isolation_condition`, `rtm_link=lambda_laws.isolation_condition`, `ssot_gate=notebooks/gate_isolation_condition.ipynb`
