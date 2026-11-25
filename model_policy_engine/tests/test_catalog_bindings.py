"""Compare trusted TOML contracts with the distributed source, without importing models."""
import ast
from pathlib import Path
import tomllib
import unittest

from model_policy_engine.schema import TEMPLATES, admit, catalog

MODELS = Path(__file__).resolve().parents[2] / "model_families"
ARCHIVED = "hardware_viability/time_control_enforcement/degraded_inverse_kinematics"


class CatalogBindingTests(unittest.TestCase):
    def test_bidirectional_inventory(self):
        model_ids = {p.relative_to(MODELS).with_suffix("").as_posix() for p in MODELS.rglob("*.py")
                     if not p.name.startswith(("test_", "run_", "__init__", "smoke_test"))}
        self.assertEqual(model_ids - {ARCHIVED}, set(catalog()))
        self.assertNotIn(ARCHIVED, catalog())

    def test_bound_source_and_policy_match(self):
        for model_id, path in catalog().items():
            with self.subTest(model_id=model_id):
                data = tomllib.loads((TEMPLATES / path).read_text(encoding="utf8"))
                admit(model_id, data)
                tree = ast.parse((MODELS / (model_id + ".py")).read_bytes())
                bindings = [i for i, n in enumerate(tree.body) if ast.unparse(n) == "_policy.bind(globals())"]
                self.assertEqual(len(bindings), 1)
                for n in tree.body[bindings[0] + 1:]:
                    self.assertIsInstance(n, ast.If)
                    self.assertEqual(ast.unparse(n.test), "__name__ == '__main__'")
                policy_ids = [n.args[0].value for n in ast.walk(tree) if isinstance(n, ast.Call)
                              and ast.unparse(n.func) == "_ModelPolicy"]
                self.assertEqual(policy_ids, [model_id])
                settings = {n.args[0].value for n in ast.walk(tree) if isinstance(n, ast.Call)
                            and ast.unparse(n.func) == "_policy.value"}
                self.assertEqual(settings, set(data["settings"]))
                funcs, records = {}, set()
                for node in tree.body:
                    if not isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        cached_settings = [n for n in ast.walk(node) if isinstance(n, ast.Call)
                                           and ast.unparse(n.func) == "_policy.value"]
                        self.assertFalse(cached_settings, "load settings inside the governed call")
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                        funcs[node.name] = node
                    if isinstance(node, ast.ClassDef):
                        if any(isinstance(dec, ast.Call) and ast.unparse(dec.func) == "_policy.record"
                               for dec in node.decorator_list):
                            records.add(node.name)
                            for field in node.body:
                                self.assertNotIsInstance(field, (ast.Assign, ast.AnnAssign),
                                                         "declare record fields and defaults in TOML")
                        for method in node.body:
                            if isinstance(method, ast.FunctionDef) and (
                                not method.name.startswith("_") or method.name == "__init__"
                            ):
                                funcs[f"{node.name}.{method.name}"] = method
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        for dec in node.decorator_list:
                            if isinstance(dec, ast.Call) and ast.unparse(dec.func) == "_policy.evaluator":
                                funcs[dec.args[0].value] = node
                self.assertEqual(records, set(data["records"]))
                self.assertEqual(set(funcs) | records, set(data["calls"]))
                for op, fn in funcs.items():
                    fields = data["calls"][op]
                    args = [a for a in (*fn.args.posonlyargs, *fn.args.args, *fn.args.kwonlyargs)
                            if a.arg not in ("self", "cls")]
                    self.assertEqual({a.arg for a in args}, set(fields), op)
                    for a in args:
                        if a.annotation:
                            self.assertEqual(ast.unparse(a.annotation), fields[a.arg]["annotation"], op)
                    for value in (*fn.args.defaults, *fn.args.kw_defaults):
                        if value is not None:
                            self.assertEqual(ast.unparse(value), "_policy.default", op)
