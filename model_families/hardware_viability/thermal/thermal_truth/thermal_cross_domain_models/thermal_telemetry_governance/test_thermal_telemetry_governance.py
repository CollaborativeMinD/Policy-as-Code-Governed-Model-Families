from __future__ import annotations
import unittest
from freshness_at_use_margin import compute_freshness_at_use_margin
from slew_rate_plausibility_margin import compute_slew_rate_plausibility_margin
from sampling_observability_margin import compute_sampling_observability_margin
from multisensor_consistency_margin import compute_multisensor_consistency_margin
class ThermalTelemetryGovernanceTests(unittest.TestCase):
    def test_freshness(self): self.assertAlmostEqual(compute_freshness_at_use_margin(12,10,5),3)
    def test_slew(self): self.assertAlmostEqual(compute_slew_rate_plausibility_margin(20,24,2,3),1)
    def test_observability(self): self.assertAlmostEqual(compute_sampling_observability_margin(100,5,10),5)
    def test_consistency(self): self.assertAlmostEqual(compute_multisensor_consistency_margin([30,31,33],4),2)
if __name__ == "__main__": unittest.main(verbosity=2)
