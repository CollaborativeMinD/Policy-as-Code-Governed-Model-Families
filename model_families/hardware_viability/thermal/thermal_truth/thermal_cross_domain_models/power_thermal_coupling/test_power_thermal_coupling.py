from __future__ import annotations
import unittest
from effective_duty_cycle_power import compute_effective_duty_cycle_power
from duty_cycle_temperature_margin import compute_duty_cycle_temperature_margin
from conversion_loss_temperature_margin import compute_conversion_loss_temperature_margin
class PowerThermalCouplingTests(unittest.TestCase):
    def test_effective_power(self): self.assertAlmostEqual(compute_effective_duty_cycle_power(5,[0.5,0.25],[10,20]),15)
    def test_duty_temp_margin(self): self.assertAlmostEqual(compute_duty_cycle_temperature_margin(80,25,10,2),35)
    def test_conversion_margin(self): self.assertAlmostEqual(compute_conversion_loss_temperature_margin(80,25,90,0.9,1),45)
if __name__ == "__main__": unittest.main(verbosity=2)
