from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestThermalTwoLayer(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "two_layer_temperature_step": ("compute_two_layer_temperature_step", "THERM-2L-002"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_thermal_two_layer(self):
        from two_layer_temperature_step import compute_surface_radiative_forcing_density
        from two_layer_temperature_step import compute_two_layer_temperature_step
        self.assertAlmostEqual(compute_surface_radiative_forcing_density(1.0, 2.0, 100.0, 0.9, 20.0, 20.0), 200.0)
        skin, sub = compute_two_layer_temperature_step(20.0, 10.0, 20.0, 0.0, 0.0, 0.9, 1.0, 10.0, 20.0, 1.0, 0.0, 0.0, 1.0)
        self.assertAlmostEqual(skin, 19.0)
        self.assertAlmostEqual(sub, 10.5)


if __name__ == "__main__":
    unittest.main()
