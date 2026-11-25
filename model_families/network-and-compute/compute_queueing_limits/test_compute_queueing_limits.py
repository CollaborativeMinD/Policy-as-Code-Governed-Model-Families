from __future__ import annotations
import unittest

from amdahl_cluster_limit import compute_amdahl_speedup, lambdified as amdahl_lambdified
from littles_law_queue import compute_little_law_queue_length, compute_queue_margin, should_throttle, lambdified as little_lambdified


class ComputeQueueingTests(unittest.TestCase):
    def test_amdahl(self):
        self.assertAlmostEqual(compute_amdahl_speedup(0.75, 3.0), 2.0)
        self.assertAlmostEqual(compute_amdahl_speedup(0.75, 3.0), amdahl_lambdified()(0.75, 3.0))

    def test_little(self):
        self.assertAlmostEqual(compute_little_law_queue_length(10.0, 0.5), 5.0)
        self.assertAlmostEqual(little_lambdified()(10.0, 0.5), 5.0)
        self.assertAlmostEqual(compute_queue_margin(10.0, 0.5, 8.0), 3.0)
        self.assertTrue(should_throttle(10.0, 1.0, 8.0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
