from __future__ import annotations
import unittest

from ground_truth_arbitrator import compute_scalar_kalman_update, lambdified_update
from intelligence_update import compute_bayes_posterior, lambdified


class TruthFusionTests(unittest.TestCase):
    def test_scalar_kalman_update(self):
        result = compute_scalar_kalman_update(
            x_previous=10.0,
            p_previous=2.0,
            control=0.0,
            sensor=12.0,
            F=1.0,
            B=0.0,
            H=1.0,
            Q=0.0,
            R=2.0,
        )
        self.assertAlmostEqual(result["kalman_gain"], 0.5)
        self.assertAlmostEqual(result["x_new"], 11.0)
        self.assertAlmostEqual(result["x_new"], lambdified_update()(10.0, 0.5, 12.0, 1.0))

    def test_bayes(self):
        self.assertAlmostEqual(compute_bayes_posterior(0.9, 0.1, 0.3), 0.3)
        self.assertAlmostEqual(compute_bayes_posterior(0.9, 0.1, 0.3), lambdified()(0.9, 0.1, 0.3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
