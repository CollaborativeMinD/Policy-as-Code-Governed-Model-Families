"""Replay source comparisons and verify decisions against the returned margins."""
import json
import math
from pathlib import Path
import runpy
import unittest

HERE = Path(__file__).resolve().parent
api = runpy.run_path(str(HERE / "lawful_actuation_clf_cbf_qp.py"))


class LawfulActuationTests(unittest.TestCase):
    def test_source_and_portable_solver_results(self):
        data = json.loads((HERE / "clf_cbf_solver_reference.json").read_text(encoding="utf-8"))
        for case in data["cases"]:
            with self.subTest(case=case["case"]):
                args, kw = case["args"], case["kwargs"]
                actual = api["lawful_control_qp"](*args, **kw)
                expected = case.get("portable", case["source"])
                tolerance = 1e-8 if "portable" in case else data["absolute_tolerance"]
                self.assertEqual(actual.keys(), expected.keys())
                for key, value in expected.items():
                    with self.subTest(field=key):
                        if value == "Infinity":
                            self.assertEqual(actual[key], math.inf)
                        elif isinstance(value, list):
                            self.assertEqual(len(actual[key]), len(value))
                            for x, y in zip(actual[key], value):
                                self.assertAlmostEqual(x, y, delta=tolerance)
                        elif isinstance(value, float):
                            self.assertAlmostEqual(actual[key], value, delta=tolerance)
                        else:
                            self.assertEqual(actual[key], value)

                x, nominal, hazards, radius, dt, bounds = args
                u = actual["u_star"]
                for value, (low, high) in zip(u, bounds):
                    self.assertLessEqual(low, value)
                    self.assertLessEqual(value, high)
                margins = [math.fsum((v + dt*w - h)**2 for v, w, h in zip(x, u, hazard)) - radius**2
                           for hazard in hazards]
                for saved, recomputed in zip(actual["cbf_margins"], margins, strict=True):
                    self.assertAlmostEqual(saved, recomputed, delta=1e-10)
                if actual["success"]:
                    self.assertGreaterEqual(actual["cbf_slack"], 0)
                    self.assertGreaterEqual(actual["clf_slack"], 0)
                    self.assertTrue(all(m + actual["cbf_slack"] >= -1e-10 for m in margins))
                    if kw.get("x_ref") is not None:
                        error = [a-b for a, b in zip(x, kw["x_ref"])]
                        derivative = math.fsum(e*v for e, v in zip(error, u))
                        margin = -kw.get("alpha", 1.0) * math.fsum(e*e for e in error)/2 - derivative
                        self.assertAlmostEqual(actual["clf_margin"], margin, delta=1e-10)
                        self.assertGreaterEqual(margin + actual["clf_slack"], -1e-10)
                else:
                    self.assertEqual(u, [min(hi, max(lo, v)) for v, (lo, hi) in zip(nominal, bounds)])
                    self.assertEqual(actual["slack"], math.inf)
                self.assertEqual(actual["null_set"], not actual["safe_without_slack"])

    def test_validation(self):
        inputs = dict(x=[0], u_nom=[0], hazards=[], r_safe=1, dt=1, u_bounds=[(-1, 1)], x_ref=[0])
        for change in ({"x_ref": None}, {"x": [math.nan]}, {"dt": 0}, {"alpha": -1},
                       {"Gamma": 0}, {"Gamma_cbf": 0}, {"Gamma_clf": 0}, {"hazards": [[1, 2]]},
                       {"u_bounds": [(1, -1)]}, {"u_bounds": []}, {"x_ref": [0, 0]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                api["lawful_control_qp"](**(inputs | change))

    def test_vector_hazard_and_explicit_optional_reference(self):
        base = dict(x=[0], u_nom=[0], r_safe=1, dt=1, u_bounds=[(-1, 1)], clf_required=False)
        result = api["lawful_control_qp"](hazards=[3], **base)
        self.assertEqual(result, api["lawful_control_qp"](hazards=[[3]], **base))
        self.assertIsNone(result["clf_margin"])
        self.assertTrue(result["safe_without_slack"])


if __name__ == "__main__":
    unittest.main()
