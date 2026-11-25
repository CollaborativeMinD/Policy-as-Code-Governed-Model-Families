#!/usr/bin/env python3
"""Unit tests for the flat executable reachability model.

Run:
    python test_reachability_model.py
"""
from __future__ import annotations

import unittest

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sampling_based_reachability import (
    Bounds,
    Obstacle,
    SamplingReachabilitySearch,
    SearchConfig,
    compute_time_margin,
    demo_blocked_path_config,
    demo_clear_path_config,
    distance,
    interpolate_step,
    min_obstacle_margin,
    run_campaign,
)


class ReachabilityModelTests(unittest.TestCase):
    def test_distance_and_step(self) -> None:
        self.assertAlmostEqual(distance((0.0, 0.0), (3.0, 4.0)), 5.0)
        stepped = interpolate_step((0.0, 0.0), (3.0, 4.0), 2.5)
        self.assertAlmostEqual(distance((0.0, 0.0), stepped), 2.5)

    def test_obstacle_margin(self) -> None:
        obs = (Obstacle((0.0, 0.0), 1.0),)
        self.assertAlmostEqual(min_obstacle_margin((3.0, 0.0), obs, 0.25), 1.75)
        self.assertLess(min_obstacle_margin((0.5, 0.0), obs, 0.0), 0.0)

    def test_time_margin(self) -> None:
        cfg = SearchConfig(
            start=(0.0,),
            goal=(10.0,),
            bounds=(Bounds(0.0, 10.0),),
            speed=1.0,
            deadline_s=20.0,
            preparation_time_s=2.0,
        )
        self.assertAlmostEqual(compute_time_margin(cfg, (5.0,), elapsed_s=3.0), 10.0)

    def test_clear_path_reaches_goal(self) -> None:
        result = SamplingReachabilitySearch(demo_clear_path_config(seed=7)).run()
        self.assertEqual(result.status, "REACHABILITY_WITNESS_FOUND")
        self.assertTrue(result.success)
        self.assertGreater(len(result.path), 1)
        self.assertEqual(result.path[0].state, demo_clear_path_config(seed=7).start)
        self.assertLessEqual(distance(result.path[-1].state, demo_clear_path_config(seed=7).goal), demo_clear_path_config(seed=7).goal_radius)

    def test_blocked_path_collapse(self) -> None:
        result = SamplingReachabilitySearch(demo_blocked_path_config(seed=7)).run()
        self.assertEqual(result.status, "COLLAPSE_PRESSURE_DOMINANT")
        self.assertFalse(result.success)
        self.assertGreater(result.telemetry["rejected_nodes"], 0)
        self.assertGreaterEqual(result.telemetry["collapse_pressure"], 0.95)

    def test_campaign(self) -> None:
        summary = run_campaign(demo_clear_path_config(seed=i) for i in range(8))
        self.assertEqual(summary["campaign_count"], 8)
        self.assertGreaterEqual(summary["success_count"], 1)
        self.assertGreaterEqual(summary["success_probability"], 0.0)
        self.assertLessEqual(summary["success_probability"], 1.0)

    def test_validation_rejects_bad_bounds(self) -> None:
        with self.assertRaises(ValueError):
            SearchConfig(
                start=(0.0,),
                goal=(1.0,),
                bounds=(Bounds(2.0, 1.0),),
            ).validate()


if __name__ == "__main__":
    unittest.main(verbosity=2)
