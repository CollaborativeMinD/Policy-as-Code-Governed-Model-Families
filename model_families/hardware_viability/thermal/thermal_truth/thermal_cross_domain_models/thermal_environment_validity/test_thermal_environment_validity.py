from __future__ import annotations
import unittest
from cooling_assumption_mismatch_margin import compute_cooling_assumption_mismatch_margin
class ThermalEnvironmentValidityTests(unittest.TestCase):
    def test_margin(self): self.assertAlmostEqual(compute_cooling_assumption_mismatch_margin(65,25,20,2.0,0.5),0.5)
if __name__ == "__main__": unittest.main(verbosity=2)
