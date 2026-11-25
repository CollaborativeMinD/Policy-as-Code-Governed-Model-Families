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


def check_authority_lease_closure_margin(m):
    actual = m.compute_authority_lease_closure_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1)
    expected = -5.199999999999999
    check('compute_authority_lease_closure_margin', actual, expected)


def check_communications_and_radar(m):
    actual = m.compute_received_power_db(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = -0.9
    check('compute_received_power_db', actual, expected)
    actual = m.compute_radar_range(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = 0.06480516386008059
    check('compute_radar_range', actual, expected)


def check_covariance_weighted_fusion(m):
    actual = m.fuse_estimates([[2, 0.1], [0.1, 3]], [[3, 0], [0, 1]], [1, 2], [3, 1])
    expected = [[[1.1990995497748875, 0.015007503751875938],
      [0.015007503751875937, 0.7498749374687343]],
     [1.784392196098049, 1.2601300650325162]]
    check('fuse_estimates', actual, expected)


def check_handoff_survival(m):
    actual = m.check_handoff_survival(0.4, 0.5)
    expected = True
    check('check_handoff_survival', actual, expected)


def check_orbital_dynamics(m):
    actual = m.compute_mean_motion(0.4, 0.5)
    expected = 1.7888543819998317
    check('compute_mean_motion', actual, expected)
    actual = m.compute_j2_nodal_precession(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -0.15355984614182427
    check('compute_j2_nodal_precession', actual, expected)


def check_sensor_actuator_delay_budget(m):
    actual = m.compute_sensor_to_actuator_delay_budget_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1)
    expected = -5.199999999999999
    check('compute_sensor_to_actuator_delay_budget_margin', actual, expected)


def check_volley_successor(m):
    actual = m.update_volley_successor(0.4, 0.5, 0.6)
    expected = 0.30000000000000004
    check('update_volley_successor', actual, expected)


FIXTURES = {
    "authority_lease_closure_margin.py": check_authority_lease_closure_margin,
    "communications_and_radar.py": check_communications_and_radar,
    "covariance_weighted_fusion.py": check_covariance_weighted_fusion,
    "handoff_survival.py": check_handoff_survival,
    "orbital_dynamics.py": check_orbital_dynamics,
    "sensor_actuator_delay_budget.py": check_sensor_actuator_delay_budget,
    "volley_successor.py": check_volley_successor,
}


def main():
    model_names = {p.name for p in HERE.glob("*.py") if not p.name.startswith(("test_", "run_"))}
    model_names -= {"smoke_test.py", "__init__.py"}
    if model_names != FIXTURES.keys():
        raise AssertionError(f"Unmatched model or fixture: {model_names ^ FIXTURES.keys()}")
    for filename, fixture in FIXTURES.items():
        isolated_model(filename, fixture)
    print("PASS space-and-comms")

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
