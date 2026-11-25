#!/usr/bin/env python3
"""Executable sampling-based reachability model."""
from __future__ import annotations

from model_policy_engine import ModelPolicy as _ModelPolicy

_policy = _ModelPolicy('sampling_based_reachability_search/sampling_based_reachability')


from dataclasses import asdict
import json
import math
import random
from typing import Iterable


Vector = tuple[float, ...]


@_policy.record(frozen=True)
class Bounds:
    """Closed sampling bound for one state dimension."""


    def validate(self) -> None:
        if not math.isfinite(self.lower) or not math.isfinite(self.upper):
            raise ValueError("Bounds must be finite.")
        if self.lower >= self.upper:
            raise ValueError("Bounds.lower must be less than Bounds.upper.")


@_policy.record(frozen=True)
class Obstacle:
    """Circular/spherical obstacle in N-dimensional state space."""


    def validate(self, dim: int) -> None:
        if len(self.center) != dim:
            raise ValueError("Obstacle center dimension must match the model state dimension.")
        if self.radius < 0.0 or not math.isfinite(self.radius):
            raise ValueError("Obstacle radius must be finite and non-negative.")
        if any(not math.isfinite(v) for v in self.center):
            raise ValueError("Obstacle center values must be finite.")
        if not self.label.strip():
            raise ValueError("Obstacle label must not be blank.")


@_policy.record(frozen=True)
class SearchConfig:
    """Configuration for the executable reachability search."""


    def validate(self) -> None:
        dim = len(self.start)
        if dim == 0:
            raise ValueError("Start vector must not be empty.")
        if len(self.goal) != dim:
            raise ValueError("Start and goal dimensions must match.")
        if len(self.bounds) != dim:
            raise ValueError("Bounds dimension must match state dimension.")
        if any(not math.isfinite(v) for v in self.start + self.goal):
            raise ValueError("Start and goal values must be finite.")
        for bound in self.bounds:
            bound.validate()
        for obstacle in self.obstacles:
            obstacle.validate(dim)


@_policy.record(frozen=True)
class Node:
    """A node in the admitted or rejected reachability tree."""


@_policy.record(frozen=True)
class SearchResult:
    """Search result with explicit accepted/rejected branches and extracted path."""


    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "success": self.success,
            "goal_node_id": self.goal_node_id,
            "accepted_nodes": [asdict(n) for n in self.accepted_nodes],
            "rejected_nodes": [asdict(n) for n in self.rejected_nodes],
            "path": [asdict(n) for n in self.path],
            "telemetry": self.telemetry,
        }

    def to_json(self, *, indent: int = _policy.default) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def distance(a: Vector, b: Vector) -> float:
    """Euclidean distance."""

    if len(a) != len(b):
        raise ValueError("Vector dimensions must match.")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def clamp_to_bounds(state: Vector, bounds: tuple[Bounds, ...]) -> Vector:
    """Clamp a state to configured bounds."""

    return tuple(max(b.lower, min(b.upper, x)) for x, b in zip(state, bounds))


def interpolate_step(origin: Vector, target: Vector, step_size: float) -> Vector:
    """Move from origin toward target by at most step_size."""

    d = distance(origin, target)
    if d <= _policy.value("distance_epsilon"):
        return origin
    scale = min(step_size, d) / d
    return tuple(o + scale * (t - o) for o, t in zip(origin, target))


def min_obstacle_margin(state: Vector, obstacles: Iterable[Obstacle], clearance: float) -> float:
    """Minimum signed distance to obstacle boundary minus required clearance.

    Positive means outside all obstacles with required clearance.
    Negative means collision or clearance violation.
    """

    margins = [distance(state, obs.center) - obs.radius - clearance for obs in obstacles]
    return min(margins) if margins else float("inf")


def compute_time_margin(config: SearchConfig, state: Vector, elapsed_s: float) -> float:
    """Remaining time after paying estimated travel-to-goal and preparation time."""

    remaining_distance = distance(state, config.goal)
    estimated_remaining_s = remaining_distance / config.speed + config.preparation_time_s
    return config.deadline_s - elapsed_s - estimated_remaining_s


def compute_branch_risk(config: SearchConfig, obstacle_margin_m: float, time_margin_s: float, parent_risk: float) -> float:
    """Monotone branch risk from clearance and deadline pressure."""

    if math.isinf(obstacle_margin_m):
        clearance_risk = 0.0
    else:
        clearance_risk = max(0.0, min(1.0, 1.0 - obstacle_margin_m))

    time_risk = 0.0 if time_margin_s >= 0.0 else min(1.0, abs(time_margin_s) / config.deadline_s)
    clearance_weight, time_weight = _policy.value("branch_risk_weights")
    local_risk = min(1.0, clearance_weight * clearance_risk + time_weight * time_risk)
    return max(parent_risk, local_risk)


def rejection_reason(config: SearchConfig, obstacle_margin_m: float, time_margin_s: float, branch_risk: float) -> str | None:
    """Return the first hard gate failure reason, or None when admitted."""

    if obstacle_margin_m < 0.0:
        return "obstacle_clearance_gate"
    if time_margin_s < config.min_time_margin_s:
        return "time_margin_gate"
    if branch_risk > config.max_branch_risk:
        return "branch_risk_gate"
    return None


class SamplingReachabilitySearch:
    """Executable sampling-based reachability search.

    Construct with SearchConfig, then call run().
    """

    def __init__(self, config: SearchConfig):
        config.validate()
        self.config = config
        self.rng = random.Random(config.seed)

    def sample_state(self) -> Vector:
        if self.rng.random() < self.config.goal_sample_rate:
            return self.config.goal
        return tuple(self.rng.uniform(b.lower, b.upper) for b in self.config.bounds)

    def nearest(self, nodes: list[Node], sample: Vector) -> Node:
        return min(nodes, key=lambda node: distance(node.state, sample))

    def propagate(self, near: Node, sample: Vector) -> tuple[Vector, float]:
        commanded = interpolate_step(near.state, sample, self.config.step_size)

        if self.config.disturbance_scale > 0.0:
            disturbed = tuple(
                x + self.rng.gauss(0.0, self.config.disturbance_scale)
                for x in commanded
            )
            new_state = clamp_to_bounds(disturbed, self.config.bounds)
        else:
            new_state = commanded

        step_distance = distance(near.state, new_state)
        elapsed_s = near.time_s + step_distance / self.config.speed
        return new_state, elapsed_s

    def _make_node(self, node_id: int, parent: Node | None, state: Vector, elapsed_s: float, admitted: bool, reason: str | None) -> Node:
        path_length = 0.0 if parent is None else parent.path_length + distance(parent.state, state)
        obs_margin = min_obstacle_margin(state, self.config.obstacles, self.config.obstacle_clearance_m)
        time_margin = compute_time_margin(self.config, state, elapsed_s)
        parent_risk = 0.0 if parent is None else parent.branch_risk
        branch_risk = compute_branch_risk(self.config, obs_margin, time_margin, parent_risk)
        return Node(
            node_id=node_id,
            parent_id=None if parent is None else parent.node_id,
            state=tuple(float(v) for v in state),
            time_s=float(elapsed_s),
            path_length=float(path_length),
            time_margin_s=float(time_margin),
            obstacle_margin_m=float(obs_margin),
            branch_risk=float(branch_risk),
            admitted=admitted,
            rejection_reason=reason,
        )

    def _extract_path(self, nodes: list[Node], goal_node_id: int) -> tuple[Node, ...]:
        by_id = {n.node_id: n for n in nodes}
        path: list[Node] = []
        cursor: int | None = goal_node_id
        while cursor is not None:
            node = by_id[cursor]
            path.append(node)
            cursor = node.parent_id
        return tuple(reversed(path))

    def run(self) -> SearchResult:
        root = self._make_node(0, None, self.config.start, 0.0, True, None)
        accepted: list[Node] = [root]
        rejected: list[Node] = []
        goal_node_id: int | None = None

        for _ in range(self.config.max_iterations):
            sample = self.sample_state()
            near = self.nearest(accepted, sample)
            new_state, elapsed_s = self.propagate(near, sample)

            obs_margin = min_obstacle_margin(new_state, self.config.obstacles, self.config.obstacle_clearance_m)
            time_margin = compute_time_margin(self.config, new_state, elapsed_s)
            branch_risk = compute_branch_risk(self.config, obs_margin, time_margin, near.branch_risk)
            reason = rejection_reason(self.config, obs_margin, time_margin, branch_risk)

            if reason is not None:
                node = self._make_node(
                    len(accepted) + len(rejected),
                    near,
                    new_state,
                    elapsed_s,
                    False,
                    reason,
                )
                rejected.append(node)
                continue

            node = self._make_node(
                len(accepted) + len(rejected),
                near,
                new_state,
                elapsed_s,
                True,
                None,
            )
            accepted.append(node)

            if distance(node.state, self.config.goal) <= self.config.goal_radius:
                goal_node_id = node.node_id
                break

        success = goal_node_id is not None
        total_branches = len(accepted) + len(rejected) - 1
        collapse_pressure = len(rejected) / max(1, total_branches)

        if success:
            status = "REACHABILITY_WITNESS_FOUND"
            path = self._extract_path(accepted, goal_node_id)
        elif collapse_pressure >= self.config.collapse_pressure_threshold:
            status = "COLLAPSE_PRESSURE_DOMINANT"
            path = ()
        else:
            status = "NO_REACHABILITY_WITNESS_FOUND"
            path = ()

        final_node = path[-1] if path else accepted[-1]
        telemetry = {
            "seed": self.config.seed,
            "accepted_nodes": len(accepted),
            "rejected_nodes": len(rejected),
            "total_branches": total_branches,
            "collapse_pressure": float(collapse_pressure),
            "final_time_margin_s": float(final_node.time_margin_s),
            "final_obstacle_margin_m": float(final_node.obstacle_margin_m),
            "final_branch_risk": float(final_node.branch_risk),
            "path_length": float(path[-1].path_length) if path else None,
        }

        return SearchResult(
            status=status,
            success=success,
            goal_node_id=goal_node_id,
            accepted_nodes=tuple(accepted),
            rejected_nodes=tuple(rejected),
            path=path,
            telemetry=telemetry,
        )


def run_campaign(configs: Iterable[SearchConfig]) -> dict[str, object]:
    """Run multiple configured searches and summarize reachability statistics."""

    results = [SamplingReachabilitySearch(cfg).run() for cfg in configs]
    success_count = sum(1 for result in results if result.success)
    collapse_count = sum(1 for result in results if result.status == "COLLAPSE_PRESSURE_DOMINANT")
    return {
        "campaign_count": len(results),
        "success_count": success_count,
        "success_probability": success_count / max(1, len(results)),
        "collapse_dominant_count": collapse_count,
        "collapse_dominant_probability": collapse_count / max(1, len(results)),
        "results": [result.to_dict() for result in results],
    }


def demo_clear_path_config(seed: int = _policy.default) -> SearchConfig:
    """A small reachable 2-D scenario."""

    return SearchConfig(
        start=_policy.value("demo_clear_path_config_start"),
        goal=_policy.value("demo_clear_path_config_goal"),
        bounds=_policy.value("demo_clear_path_config_bounds"),
        obstacles=_policy.value("demo_clear_path_config_obstacles"),
        seed=seed,
        max_iterations=_policy.value("demo_clear_path_config_max_iterations"),
        step_size=_policy.value("demo_clear_path_config_step_size"),
        goal_radius=_policy.value("demo_clear_path_config_goal_radius"),
        speed=_policy.value("demo_clear_path_config_speed"),
        deadline_s=_policy.value("demo_clear_path_config_deadline_s"),
        obstacle_clearance_m=_policy.value("demo_clear_path_config_obstacle_clearance_m"),
        max_branch_risk=_policy.value("demo_clear_path_config_max_branch_risk"),
    )


def demo_blocked_path_config(seed: int = _policy.default) -> SearchConfig:
    """A deliberately blocked scenario that should emit collapse pressure."""

    return SearchConfig(
        start=_policy.value("demo_blocked_path_config_start"),
        goal=_policy.value("demo_blocked_path_config_goal"),
        bounds=_policy.value("demo_blocked_path_config_bounds"),
        obstacles=_policy.value("demo_blocked_path_config_obstacles"),
        seed=seed,
        max_iterations=_policy.value("demo_blocked_path_config_max_iterations"),
        step_size=_policy.value("demo_blocked_path_config_step_size"),
        goal_radius=_policy.value("demo_blocked_path_config_goal_radius"),
        speed=_policy.value("demo_blocked_path_config_speed"),
        deadline_s=_policy.value("demo_blocked_path_config_deadline_s"),
        obstacle_clearance_m=_policy.value("demo_blocked_path_config_obstacle_clearance_m"),
        max_branch_risk=_policy.value("demo_blocked_path_config_max_branch_risk"),
        collapse_pressure_threshold=_policy.value("demo_blocked_path_config_collapse_pressure_threshold"),
    )


_policy.bind(globals())

if __name__ == "__main__":
    result = SamplingReachabilitySearch(demo_clear_path_config()).run()
    print(result.to_json())
