from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestThermalDistortion(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "thermal_distortion_index": ("compute_thermal_distortion_index", "THERM-SILENT-001"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_thermal_distortion_index(self):
        from thermal_distortion_index import compute_thermal_distortion_index
        self.assertEqual(compute_thermal_distortion_index(80.0, 60.0, 100.0, 10.0, 20.0, 100.0, 50.0, 0.9), 1.0)


if __name__ == "__main__":
    unittest.main()
