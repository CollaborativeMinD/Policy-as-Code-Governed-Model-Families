from __future__ import annotations
import math, unittest
from equilibrium_temperature_under_load import compute_equilibrium_temperature_under_load
from time_to_temperature_threshold import compute_time_to_temperature_threshold
from cooldown_time_to_rearm import compute_cooldown_time_to_rearm
class ThermalRCEnvelopeTests(unittest.TestCase):
    def test_equilibrium(self): self.assertAlmostEqual(compute_equilibrium_temperature_under_load(25,10,2),45)
    def test_time_to_threshold(self): self.assertTrue(math.isfinite(compute_time_to_temperature_threshold(25,60,85,100)))
    def test_cooldown(self): self.assertTrue(math.isfinite(compute_cooldown_time_to_rearm(80,50,25,100)))
if __name__ == "__main__": unittest.main(verbosity=2)
