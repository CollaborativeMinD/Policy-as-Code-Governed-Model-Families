from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestProvenanceGovernance(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "provenance_completeness_margin": ("compute_provenance_completeness_margin", "TRACE-GOV-003"),
            "lineage_completeness_margin": ("compute_lineage_completeness_margin", "TRACE-GOV-004"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    @unittest.skip("Source-claim ceiling gate implementation absent from the supplied archive")
    def test_source_claim_ceiling_gate(self):
        pass

    def test_provenance_governance(self):
        from provenance_completeness_margin import compute_provenance_completeness_margin
        from lineage_completeness_margin import compute_lineage_completeness_margin
        self.assertEqual(compute_provenance_completeness_margin(["a", "b"], {"a": 1, "b": ""}), -1)
        self.assertEqual(compute_lineage_completeness_margin(["a", "b"], {"a": 1, "b": 2}), 0)


if __name__ == "__main__":
    unittest.main()
