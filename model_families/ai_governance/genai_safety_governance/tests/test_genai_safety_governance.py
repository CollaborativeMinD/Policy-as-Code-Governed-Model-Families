from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestGenaiSafetyGovernance(unittest.TestCase):
    def test_documented_exports(self):
        from importlib import import_module

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        exports = {
            "heuristic_rejection_gate": ("compute_heuristic_rejection_gate", "GEN-SAFE-003"),
        }
        for name, (function, formula_id) in exports.items():
            with self.subTest(module=name):
                record = readme.split("\n## " + name + ".py\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn(formula_id, record)
                self.assertIn("**Symbolic form**", record)
                module = import_module(name)
                self.assertIn(function, module.__all__)
                self.assertTrue(callable(getattr(module, function)))

    def test_heuristic_rejection_gate(self):
        from heuristic_rejection_gate import compute_heuristic_rejection_gate
        passed, reasons = compute_heuristic_rejection_gate(
            {"thermal": 0.1, "power": 1.0}, [], 1.0, 1.0, 0.9, 0.0, 0.0, 0.0
        )
        self.assertTrue(passed)
        self.assertEqual(reasons, [])
        passed, reasons = compute_heuristic_rejection_gate(
            {"thermal": -0.1}, ["DEATH_STATE"], 0.5, 1.0, 0.9, 0.0, 0.0, 0.0
        )
        self.assertFalse(passed)
        self.assertIn("active_death_state_present", reasons)


if __name__ == "__main__":
    unittest.main()
