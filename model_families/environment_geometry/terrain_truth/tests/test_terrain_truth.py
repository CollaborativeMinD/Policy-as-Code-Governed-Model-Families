from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestTerrainTruth(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "terrain_vertical_uncertainty_margin": ("compute_terrain_vertical_uncertainty_margin", "TERRAIN-TRUTH-004"),
            "slope_uncertainty_guarded_margin": ("compute_slope_uncertainty_guarded_margin", "TERRAIN-TRUTH-005"),
            "multiscale_disagreement_margin": ("compute_multiscale_disagreement_margin", "TERRAIN-TRUTH-009"),
            "lane_aware_confidence_ceiling": ("compute_lane_aware_confidence_ceiling", "TERRAIN-TRUTH-010"),
            "local_hazard_claim_gate": ("compute_local_hazard_claim_gate", "TERRAIN-TRUTH-011"),
            "roughness_alias_margin": ("compute_roughness_alias_margin", "TERRAIN-TRUTH-012"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_terrain_truth_margins_and_gates(self):
        from terrain_vertical_uncertainty_margin import compute_terrain_vertical_uncertainty_margin
        from slope_uncertainty_guarded_margin import compute_slope_uncertainty_guarded_margin
        from multiscale_disagreement_margin import compute_multiscale_disagreement_margin
        from lane_aware_confidence_ceiling import compute_lane_aware_confidence_ceiling
        from local_hazard_claim_gate import compute_local_hazard_claim_gate
        from roughness_alias_margin import compute_roughness_alias_margin
        self.assertAlmostEqual(compute_terrain_vertical_uncertainty_margin(0.5, 0.2), 0.3)
        self.assertEqual(compute_slope_uncertainty_guarded_margin(15.0, 10.0, 1.0, 2.0), 3.0)
        self.assertEqual(compute_multiscale_disagreement_margin([1.0, 2.0], [1.0, 2.0], 6.0), 6.0)
        c_lane, ceiling = compute_lane_aware_confidence_ceiling(0.9, "local_nac", "PAD_TILE_INGESTED", 1.0, 6.0)
        self.assertEqual((c_lane, ceiling), (0.9, 1.0))
        self.assertTrue(compute_local_hazard_claim_gate("local_nac", True, "PAD_TILE_INGESTED", 0.8, 0.5))
        self.assertAlmostEqual(compute_roughness_alias_margin(0.5, 0.3, 0.35), 0.15)


if __name__ == "__main__":
    unittest.main()
