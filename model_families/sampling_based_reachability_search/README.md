# Sampling based reachability search

### What this is

A standard-library sampling-based reachability search with TOML-governed configuration.

The model grows a tree from `start` toward `goal`:

1. sample a bounded state,
2. find nearest accepted node,
3. steer toward the sample,
4. evaluate obstacle clearance,
5. evaluate remaining time margin,
6. compute branch risk,
7. admit or reject the node,
8. emit a reachability witness, no-witness result, or collapse-pressure result.

### Status values

| Status | Meaning |
|---|---|
| `REACHABILITY_WITNESS_FOUND` | A path reached the goal set. |
| `NO_REACHABILITY_WITNESS_FOUND` | The search ended without a goal witness, but collapse pressure did not dominate. |
| `COLLAPSE_PRESSURE_DOMINANT` | Rejection pressure dominated the sampled search. |

### Use cases

Use this for:

- quick reachability witness generation,
- stress-searching a bounded state space,
- testing whether obstacle, time, and risk gates collapse sampled futures,
- deterministic replay by seed,
- proving that a planning candidate actually runs before it is wired into a larger twin.

### Non-use cases

Do not use this as:

- a certified motion planner,
- a complete RRT* implementation,
- a formal Hamilton-Jacobi reachability solver,
- an actuator-authority controller,
- a vehicle dynamics simulator,
- a substitute for calibrated mission physics.

## Subdirectories

- [Tests](Tests/README.md)

## Model files

- [sampling_based_reachability.py](sampling_based_reachability.py)

## Admitted model policies

Each link opens the baseline TOML for the named model ID. Edit its deployment copy under `drafts` and apply it to change ordinary calls. The working baseline below uses the shipped settings. [Policy setup and publication](../../model_policy_engine/README.md)

- [sampling_based_reachability_search/sampling_based_reachability](../../model_policy_engine/policies/sampling_based_reachability_search/sampling_based_reachability_policy.toml)

## Working baseline

Run `python smoke_test.py` in this directory. The fixtures in [smoke_test.py](smoke_test.py) give the inputs and expected results. Each model is copied alone to a temporary directory before execution.

<!-- observed-output -->

```text
sampling_based_reachability.py
  SamplingReachabilitySearch = "REACHABILITY_WITNESS_FOUND"
  SamplingReachabilitySearch = "COLLAPSE_PRESSURE_DOMINANT"
PASS sampling_based_reachability_search
```

<!-- end-observed-output -->

## sampling_based_reachability.py

### Model context from the archive

Executable sampling-based reachability model.

This file is the model.

It implements a deterministic, standard-library-only, sampling-based reachability
search with PCC-style admission gates:

1. sample a bounded state,
2. find nearest accepted node,
3. steer toward the sample,
4. evaluate obstacle clearance, branch risk, and remaining-time margin,
5. admit or reject the node,
6. stop when the goal set is reached or collapse pressure dominates.

The model obtains its configuration from the shared policy engine.

### Entry points

- `Bounds` (type)
- `Obstacle` (type)
- `SearchConfig` (type)
- `Node` (type)
- `SearchResult` (type)
- `distance(a: Vector, b: Vector)`
- `clamp_to_bounds(state: Vector, bounds: tuple[Bounds, ...])`
- `interpolate_step(origin: Vector, target: Vector, step_size: float)`
- `min_obstacle_margin(state: Vector, obstacles: Iterable[Obstacle], clearance: float)`
- `compute_time_margin(config: SearchConfig, state: Vector, elapsed_s: float)`
- `compute_branch_risk(config: SearchConfig, obstacle_margin_m: float, time_margin_s: float, parent_risk: float)`
- `rejection_reason(config: SearchConfig, obstacle_margin_m: float, time_margin_s: float, branch_risk: float)`
- `SamplingReachabilitySearch` (type)
- `run_campaign(configs: Iterable[SearchConfig])`
- `demo_clear_path_config(seed: int=7)`
- `demo_blocked_path_config(seed: int=7)`
