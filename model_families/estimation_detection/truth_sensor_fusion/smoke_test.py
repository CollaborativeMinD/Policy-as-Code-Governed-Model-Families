"""Execute this directory's working baseline. Pass --tree to include descendants."""
from pathlib import Path
import subprocess
import sys


import ast
from contextlib import chdir
from dataclasses import asdict, is_dataclass
import json
import math
import runpy
import shutil
from tempfile import TemporaryDirectory
from types import SimpleNamespace


HERE = Path(__file__).resolve().parent


def plain(value):
    if is_dataclass(value):
        return plain(asdict(value))
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    return value


def matches(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and all(
            matches(actual[k], expected[k]) for k in expected
        )
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            matches(a, b) for a, b in zip(actual, expected)
        )
    if isinstance(expected, float):
        return type(actual) in (float, int) and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10)
    return type(actual) is type(expected) and actual == expected


def check(label, actual, expected):
    actual = plain(actual)
    if not matches(actual, expected):
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")
    print(f"  {label} = {json.dumps(actual, sort_keys=True, ensure_ascii=True)}")


def isolated_model(filename, fixture):
    with TemporaryDirectory() as folder:
        path = Path(shutil.copyfile(HERE / filename, Path(folder) / filename))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [(node.module or "").split(".")[0]] if not node.level else [".relative"]
            else:
                continue
            external = set(names) - sys.stdlib_module_names - {"model_policy_engine"}
            if external:
                raise AssertionError(f"{filename} imports {sorted(external)}")
        print(filename)
        with chdir(folder):
            fixture(SimpleNamespace(**runpy.run_path(str(path))))

import importlib.util
import unittest


def run_suite(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        result = unittest.TestResult()
        suite.run(result)
    finally:
        sys.path.remove(str(path.parent))
    if not result.testsRun or not result.wasSuccessful():
        raise AssertionError(f"{path.name}: {result.errors + result.failures}")
    print(f"{path.name}: {result.testsRun - len(result.skipped)} passed, {len(result.skipped)} skipped")
    for test, reason in result.skipped:
        print(f"  SKIP {test._testMethodName}: {reason}")


def check_ground_truth_arbitrator(m):
    actual = m.compute_scalar_kalman_update(
        x_previous=10.0,
        p_previous=2.0,
        control=0.0,
        sensor=12.0,
        F=1.0,
        B=0.0,
        H=1.0,
        Q=0.0,
        R=2.0,
    )
    expected = {'x_predict': 10.0,
     'p_predict': 2.0,
     'kalman_gain': 0.5,
     'innovation': 2.0,
     'x_new': 11.0,
     'p_new': 1.0}
    check('compute_scalar_kalman_update', actual, expected)
    actual = m.lambdified_update()(2.0, 3.0, 4.0, 5.0)
    expected = -16.0
    check('lambdified_update', actual, expected)


def check_intelligence_update(m):
    actual = m.compute_bayes_posterior(0.9, 0.1, 0.3)
    expected = 0.30000000000000004
    check('compute_bayes_posterior', actual, expected)
    actual = m.lambdified()(2.0, 3.0, 4.0)
    expected = 1.5
    check('lambdified', actual, expected)


FIXTURES = {
    "ground_truth_arbitrator.py": check_ground_truth_arbitrator,
    "intelligence_update.py": check_intelligence_update,
}


def main():
    model_names = {p.name for p in HERE.glob("*.py") if not p.name.startswith(("test_", "run_"))}
    model_names -= {"smoke_test.py", "__init__.py"}
    if model_names != FIXTURES.keys():
        raise AssertionError(f"Unmatched model or fixture: {model_names ^ FIXTURES.keys()}")
    for filename, fixture in FIXTURES.items():
        isolated_model(filename, fixture)
    for path in sorted(HERE.glob("test_*.py")):
        run_suite(path)
    print("PASS estimation_detection/truth_sensor_fusion")

if __name__ == "__main__":
    if not (sys.flags.no_site and sys.flags.safe_path and sys.flags.dont_write_bytecode and sys.flags.utf8_mode):
        import importlib.util
        import os
        env = os.environ.copy()
        engine = importlib.util.find_spec("model_policy_engine")
        if engine and engine.origin:
            env["PYTHONPATH"] = str(Path(engine.origin).resolve().parent.parent)
        raise SystemExit(subprocess.call([sys.executable, "-S", "-P", "-B", "-X", "utf8",
                                          __file__, *sys.argv[1:]], env=env))
    try:
        from model_policy_engine.testing import baseline_deployment
    except ModuleNotFoundError as exc:
        if exc.name != "model_policy_engine":
            raise
        # Resolve only the bundled engine; leave the model families off the import path.
        import importlib.util
        package = next((p.parent / "model_policy_engine" / "__init__.py" for p in (HERE, *HERE.parents)
                        if p.name == "model_families" and (p.parent / "model_policy_engine" / "__init__.py").is_file()), None)
        if package is None:
            raise
        spec = importlib.util.spec_from_file_location("model_policy_engine", package)
        engine = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = engine
        spec.loader.exec_module(engine)
        from model_policy_engine.testing import baseline_deployment
    with baseline_deployment():
        main()
