from __future__ import annotations
import unittest
from clock_derate_fraction import compute_clock_derate_fraction
from deadline_margin_under_derate import compute_deadline_margin_under_derate
from thermal_authority_scale import compute_thermal_authority_scale
from recovery_hysteresis_margin import compute_recovery_hysteresis_margin
class ThermalTimingAuthorityTests(unittest.TestCase):
    def test_clock_derate(self): self.assertAlmostEqual(compute_clock_derate_fraction(75,50,100,0.5,0.25),0.75)
    def test_deadline_margin(self): self.assertAlmostEqual(compute_deadline_margin_under_derate(100,50,0.5),0)
    def test_authority_scale(self): self.assertAlmostEqual(compute_thermal_authority_scale(75,50,100,20,100,0.1),0.2)
    def test_hysteresis(self): self.assertAlmostEqual(compute_recovery_hysteresis_margin(45,50),5)
if __name__ == "__main__": unittest.main(verbosity=2)
