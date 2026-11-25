from __future__ import annotations
import unittest

from monte_carlo_failure_predictor import compute_failure_probability, lambdified as mc_lambdified
from pid_control import compute_pid_control, lambdified as pid_lambdified
from dead_mans_switch import verify_dead_mans_switch_trace, lambdified_margin
from pavlovian_reflex_state_machine import compute_next_state, lambdified_gate_margin


class TimeControlTests(unittest.TestCase):
    def test_pid(self):
        self.assertAlmostEqual(compute_pid_control(2.0, 3.0, -1.0, 4.0, 0.5, 2.0), 7.5)
        self.assertAlmostEqual(compute_pid_control(2.0, 3.0, -1.0, 4.0, 0.5, 2.0), pid_lambdified()(2.0, 3.0, -1.0, 4.0, 0.5, 2.0))

    @unittest.skip("PCC-13 turret aiming model excluded from validation")
    def test_degraded_inverse_kinematics_identity(self):
        pass

    def test_dead_mans_switch(self):
        ok = verify_dead_mans_switch_trace([{"time_s": 0.0, "unsafe": True}, {"time_s": 2.0, "emergency": True}], 3.0)
        bad = verify_dead_mans_switch_trace([{"time_s": 0.0, "unsafe": True}, {"time_s": 5.0, "emergency": True}], 3.0)
        self.assertTrue(ok["passed"])
        self.assertFalse(bad["passed"])
        self.assertAlmostEqual(lambdified_margin()(3.0, 2.0), 1.0)

    def test_monte_carlo_failure(self):
        result = compute_failure_probability([[0, 1, 2], [0, 3, 9], [1, 2]], lambda x: x < 5)
        self.assertAlmostEqual(result["failure_probability"], 1 / 3)
        self.assertAlmostEqual(mc_lambdified()(1.0, 3.0), 1 / 3)

    def test_pavlovian_state_machine(self):
        transitions = {("PRIMARY", "collapse_warning"): "ALTERNATE"}
        self.assertEqual(compute_next_state("PRIMARY", 0.8, 0.7, "collapse_warning", transitions), "ALTERNATE")
        self.assertEqual(compute_next_state("PRIMARY", 0.6, 0.7, "collapse_warning", transitions), "PRIMARY")
        self.assertAlmostEqual(lambdified_gate_margin()(0.8, 0.7), 0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
