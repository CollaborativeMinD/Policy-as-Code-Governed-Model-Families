from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestGenaiTruthGovernance(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "generative_divergence_margin": ("compute_generative_divergence_margin", "GEN-TRUTH-001"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_generative_divergence_margin(self):
        from generative_divergence_margin import compute_generative_divergence_margin
        self.assertAlmostEqual(compute_generative_divergence_margin([1.0, 2.0], [1.0, 4.0], 3.0), 1.0)


if __name__ == "__main__":
    unittest.main()
