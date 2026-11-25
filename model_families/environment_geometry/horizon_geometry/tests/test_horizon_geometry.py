from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestHorizonGeometry(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "horizon_sampling_margin": ("compute_horizon_sampling_margin", "HORIZON-GEO-003"),
            "solar_disk_clearance_margin": ("compute_solar_disk_guarded_clearance_margin", "HORIZON-GEO-004"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_horizon_geometry_margins(self):
        from horizon_sampling_margin import compute_horizon_sampling_margin
        from solar_disk_clearance_margin import compute_solar_disk_guarded_clearance_margin
        self.assertAlmostEqual(compute_horizon_sampling_margin(10.0, 1.0, 1.0), -35.0)
        self.assertAlmostEqual(compute_solar_disk_guarded_clearance_margin(5.0, 1.0, 0.266, 0.1, 0.2), 3.434)


if __name__ == "__main__":
    unittest.main()
