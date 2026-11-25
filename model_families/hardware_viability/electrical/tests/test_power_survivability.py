from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestPowerSurvivability(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "illumination_cycle_energy_margin": ("compute_illumination_duty_cycle_energy_margin", "POWER-SURV-003"),
            "occlusion_energy_reserve_margin": ("compute_occlusion_energy_reserve_margin", "POWER-SURV-004"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_power_survivability_margins(self):
        from illumination_cycle_energy_margin import compute_illumination_duty_cycle_energy_margin
        from occlusion_energy_reserve_margin import compute_occlusion_energy_reserve_margin
        self.assertEqual(compute_illumination_duty_cycle_energy_margin(100.0, 20.0, 5.0, 10.0, 2.0, 3.0), 100.0)
        self.assertEqual(compute_occlusion_energy_reserve_margin(100.0, 10.0, 2.0, 5.0, 15.0), 60.0)


if __name__ == "__main__":
    unittest.main()
