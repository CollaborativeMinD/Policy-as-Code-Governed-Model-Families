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


def check_control_allocation_residual(m):
    actual = m.compute_control_allocation_residual(
        [[1, 0, 1], [0, 1, 1]],
        [4, -1],
        [-1, -1, 0],
        [1, 1, 1],
    )
    expected = 2.2360679774997902
    check('compute_control_allocation_residual', actual, expected)
    actual = m.compute_control_allocation_residual([[1, 1], [2, 2]], [3, 6], [-1, -1], [1, 1])
    expected = 2.23606797749979
    check('compute_control_allocation_residual', actual, expected)


def check_coupled_rigid_body_6_dof_propagation(m):
    actual = m.compute_rigid_body_6dof_step(
        [1, 2, 3],
        [0, 1, 0],
        [1, 0, 0, 0],
        [0.1, 0.2, 0.3],
        2,
        [[2, 0, 0], [0, 3, 0], [0, 0, 4]],
        [2, 0, 0],
        [0, 1, 0],
        0.1,
    )
    expected = {'position': [1.0, 2.1, 3.0],
     'velocity': [0.1, 1.0, 0.0],
     'quaternion': [0.9998250459241057,
                    0.004999125229620529,
                    0.009998250459241059,
                    0.014997375688861584],
     'omega': [0.097, 0.23533333333333334, 0.2995],
     'linear_acceleration': [1.0, 0.0, 0.0],
     'angular_acceleration': [-0.029999999999999985,
                              0.35333333333333333,
                              -0.005000000000000001]}
    check('compute_rigid_body_6dof_step', actual, expected)


def check_curvature_feasibility_margin(m):
    actual = m.compute_curvature_feasibility_margin(0.4, 0.5, 0.6)
    expected = 3.249999999999999
    check('compute_curvature_feasibility_margin', actual, expected)


def check_newton_euler_translational(m):
    actual = m.compute_translational_acceleration(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1)
    expected = 1.209
    check('compute_translational_acceleration', actual, expected)


def check_truth_conditioned_safe_velocity_margin(m):
    actual = m.compute_truth_conditioned_safe_velocity_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    expected = -0.5
    check('compute_truth_conditioned_safe_velocity_margin', actual, expected)


FIXTURES = {
    "Control-allocation-residual.py": check_control_allocation_residual,
    "Coupled rigid-body 6-DOF propagation.py": check_coupled_rigid_body_6_dof_propagation,
    "curvature_feasibility_margin.py": check_curvature_feasibility_margin,
    "newton_euler_translational.py": check_newton_euler_translational,
    "Truth-conditioned-safe-velocity-margin.py": check_truth_conditioned_safe_velocity_margin,
}


def main():
    model_names = {p.name for p in HERE.glob("*.py") if not p.name.startswith(("test_", "run_"))}
    model_names -= {"smoke_test.py", "__init__.py"}
    if model_names != FIXTURES.keys():
        raise AssertionError(f"Unmatched model or fixture: {model_names ^ FIXTURES.keys()}")
    for filename, fixture in FIXTURES.items():
        isolated_model(filename, fixture)
    if "--tree" in sys.argv:
        for entry in sorted(HERE.glob("*/smoke_test.py")):
            subprocess.run([sys.executable, "-S", "-P", "-B", "-X", "utf8", str(entry), "--tree"], check=True)
    print("PASS plant_fidelity")

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
