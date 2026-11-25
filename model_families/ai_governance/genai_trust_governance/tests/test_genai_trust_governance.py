from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestGenaiTrustGovernance(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "context_saturation_index": ("compute_context_saturation_index", "GEN-TRUST-002"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_context_saturation_index(self):
        from context_saturation_index import compute_context_saturation_index
        self.assertAlmostEqual(compute_context_saturation_index(0.5, 3, 2, 3, 4), 0.65)
        self.assertEqual(compute_context_saturation_index(9.0, 99, 99, 3, 4), 1.0)


if __name__ == "__main__":
    unittest.main()
