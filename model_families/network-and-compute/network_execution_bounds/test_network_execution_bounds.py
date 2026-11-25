from __future__ import annotations
import unittest

from shannon_hartley_capacity import compute_channel_capacity_bps, lambdified
from k_connectivity_survival import has_two_independent_paths, lambdified_margin
from quarantine_blast_radius import compute_blast_radius
from doda_latency_bound import compute_latency_budget_margin, within_latency_budget, lambdified_margin as latency_lambdified


class NetworkExecutionTests(unittest.TestCase):
    def test_capacity(self):
        self.assertAlmostEqual(compute_channel_capacity_bps(100.0, 3.0, 1.0), 200.0)
        self.assertAlmostEqual(compute_channel_capacity_bps(100.0, 3.0, 1.0), lambdified()(100.0, 3.0, 1.0))

    def test_k_connectivity(self):
        nodes = ["a", "b", "c"]
        ring = [("a", "b"), ("b", "c"), ("c", "a")]
        line = [("a", "b"), ("b", "c")]
        self.assertTrue(has_two_independent_paths(nodes, ring))
        self.assertFalse(has_two_independent_paths(nodes, line))
        self.assertGreaterEqual(lambdified_margin()(2.0), 0.0)

    def test_blast_radius(self):
        edges = [("a", "b"), ("b", "c"), ("c", "d")]
        self.assertEqual(compute_blast_radius("a", ["b", "d"], edges), 3)

    def test_latency_bound(self):
        self.assertAlmostEqual(compute_latency_budget_margin([0.1, 0.2, 0.3], 1.0), 0.4)
        self.assertTrue(within_latency_budget([0.1, 0.2], 0.5))
        self.assertAlmostEqual(latency_lambdified()(1.0, 0.6), 0.4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
