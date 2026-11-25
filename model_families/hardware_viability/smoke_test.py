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


def check_converging_terminal_pressure(m):
    actual = m.compute_converging_terminal_pressure(0.2, 0.4, 0.1, 0.5)
    expected = 0.31
    check('compute_converging_terminal_pressure', actual, expected)


def check_minimum_terminal_horizon(m):
    actual = m.compute_minimum_terminal_horizon(0.4, 0.5, 0.6)
    expected = {'minimum_terminal_horizon_s': 0.4, 'dominant_driver': 'THERMAL'}
    check('compute_minimum_terminal_horizon', actual, expected)


def check_predictive_hardware_viability_state(m):
    actual = m.compute_predictive_hardware_viability_state(15, 20, 300, 10, 0.3, 'thermal')
    expected = {'status': 'NOMINAL',
     'dominant_driver': 'thermal',
     'minimum_terminal_horizon_s': 10.0,
     'thermal_margin_c': 15.0,
     'memory_margin_pct': 20.0,
     'queue_margin_items': 300.0,
     'converging_terminal_pressure': 0.3}
    check('compute_predictive_hardware_viability_state', actual, expected)


def check_recovery_time_inflation(m):
    actual = m.evaluate_recovery_state(recovery_time_s=4, baseline_recovery_time_s=2, ttv_s=8)
    expected = {'recovery_time_s': 4.0,
     'baseline_recovery_time_s': 2.0,
     'ttv_s': 8.0,
     'rti': 2.0,
     'recovery_margin_s': 4.0,
     'recovery_ratio': 0.5,
     'rti_growth_per_s': 1.0,
     'divergence_pressure': 0.35,
     'phase_code': 1,
     'phase_label': 'GRACEFUL_DEGRADATION',
     'terminal_required': False}
    check('evaluate_recovery_state', actual, expected)
    actual = m.deterministic_exponential_recovery_trace([0.0, 1.0, 2.0], amplitude=1.0, tau_s=1.0)
    expected = [1.0, 0.36787944117144233, 0.1353352832366127]
    check('deterministic_exponential_recovery_trace', actual, expected)
    actual = m.theoretical_exponential_recovery_time_s(amplitude=1, threshold_abs=0.1, tau_s=2)
    expected = 4.605170185988092
    check('theoretical_exponential_recovery_time_s', actual, expected)
    actual = m.estimate_recovery_time_s(
        [0, 1, 2, 3],
        [1, 0.5, 0.1, 0.05],
        threshold_abs=0.1,
        dwell_samples=2,
    )
    expected = 2.0
    check('estimate_recovery_time_s', actual, expected)
    actual = m.evaluate_recovery_state(recovery_time_s=1, baseline_recovery_time_s=1, ttv_s=5).phase_label
    expected = 'NOMINAL_RECOVERY'
    check('evaluate_recovery_state', actual, expected)
    actual = m.evaluate_recovery_state(recovery_time_s=8, baseline_recovery_time_s=8, ttv_s=10).phase_label
    expected = 'LAWFUL_RECOVERY_PRESSURE'
    check('evaluate_recovery_state', actual, expected)
    actual = m.evaluate_recovery_state(recovery_time_s=10, baseline_recovery_time_s=8, ttv_s=10).phase_label
    expected = 'ESCROW_OR_TERMINAL_REQUIRED'
    check('evaluate_recovery_state', actual, expected)
    try:
        m.RecoveryTraceConfig(amplitude=1, threshold_abs=1)
    except ValueError:
        print('  RecoveryTraceConfig rejected invalid input')
    else:
        raise AssertionError("expected ValueError")
    try:
        m.RecoveryTimeInflationConfig(epsilon_s=0)
    except ValueError:
        print('  RecoveryTimeInflationConfig rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


FIXTURES = {
    "converging_terminal_pressure.py": check_converging_terminal_pressure,
    "minimum terminal horizon.py": check_minimum_terminal_horizon,
    "predictive_hardware_viability_state.py": check_predictive_hardware_viability_state,
    "recovery_time_inflation.py": check_recovery_time_inflation,
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
    print("PASS hardware_viability")

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
