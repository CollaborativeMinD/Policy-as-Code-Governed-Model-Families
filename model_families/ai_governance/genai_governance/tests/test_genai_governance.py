from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestGenaiGovernance(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "evidence_coverage_ratio": ("compute_evidence_coverage_ratio", "GEN-GOV-004"),
            "contradiction_exposure_score": ("compute_contradiction_exposure_score", "GEN-GOV-005"),
            "deterministic_parse_yield": ("compute_deterministic_parse_yield", "GEN-GOV-007"),
            "stale_evidence_decay": ("compute_stale_evidence_decay", "GEN-GOV-009"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_genai_governance_primitives(self):
        from evidence_coverage_ratio import compute_evidence_coverage_ratio
        from contradiction_exposure_score import compute_contradiction_exposure_score
        from deterministic_parse_yield import compute_deterministic_parse_yield
        from stale_evidence_decay import compute_stale_evidence_decay
        self.assertEqual(compute_evidence_coverage_ratio(["a", "b"], ["b", "c"]), 0.5)
        self.assertEqual(compute_contradiction_exposure_score([False, True], [1.0, 3.0]), 0.75)
        self.assertEqual(compute_deterministic_parse_yield(8, 10), 0.8)
        self.assertAlmostEqual(compute_stale_evidence_decay(2.0, 10.0, 2.0), 0.64)


if __name__ == "__main__":
    unittest.main()
