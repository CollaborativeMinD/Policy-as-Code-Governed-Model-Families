"""Execute this directory's working baseline. Pass --tree to include descendants."""
from pathlib import Path
import subprocess
import sys


import ast
import importlib.util
import unittest
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


def check_abort_closure_margin(m):
    actual = m.compute_abort_closure_margin(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -0.9583333333333334
    check('compute_abort_closure_margin', actual, expected)


def check_actuator_saturation(m):
    actual = m.compute_actuator_saturation(0.4, 0.0, 2.0)
    expected = 0.4
    check('compute_actuator_saturation', actual, expected)
    actual = m.compute_actuator_saturation(4, -1, 2)
    expected = 2
    check('compute_actuator_saturation', actual, expected)


def check_actuator_slew_rate(m):
    actual = m.compute_slew_limited_command(0.4, 0.5, 0.6, 0.7)
    expected = 0.5
    check('compute_slew_limited_command', actual, expected)


def check_attainable_wrench_residual(m):
    actual = m.compute_attainable_wrench_residual([[1, 0], [0, 1]], [2, -1], [0, 0], [1, 1], [1, 2])
    expected = 2.0
    check('compute_attainable_wrench_residual', actual, expected)


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
    try:
        m.compute_control_allocation_residual([[1]], [1], [2], [1])
    except ValueError:
        print('  compute_control_allocation_residual rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_controllability_margin(m):
    actual = m.compute_authority_weighted_controllability_margin([[1, 0], [0, 2]], [0.8, 0.5], 0.2)
    expected = 0.6000000000000001
    check('compute_authority_weighted_controllability_margin', actual, expected)
    actual = m.compute_authority_weighted_controllability_margin([[1, 0], [0, 1]], [1, 0], 0.1)
    expected = -0.1
    check('compute_authority_weighted_controllability_margin', actual, expected)
    try:
        m.compute_authority_weighted_controllability_margin([[1]], [2], 1)
    except ValueError:
        print('  compute_authority_weighted_controllability_margin rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_lease_validity_margin(m):
    actual = m.compute_authority_lease_validity_margin(0.4, 0.5, 0.6, 0.7)
    expected = -1.4
    check('compute_authority_lease_validity_margin', actual, expected)


def check_mechatronics_power_roundup(m):
    actual = m.pbr001_min_hold_up_time_closure(0.01, 12, 9, 3, 0.01, 0.01, 0.02)
    expected = {'value': 0.065, 'passed': True}
    check('pbr001_min_hold_up_time_closure', actual, expected)
    actual = m.pbr002_brownout_entry_guard(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = False
    check('pbr002_brownout_entry_guard', actual, expected)
    actual = m.pbr003_stable_restart_gate(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1)
    expected = False
    check('pbr003_stable_restart_gate', actual, expected)
    actual = m.pbr004_rail_coherence_index([0.4, 0.8], 12.0, 0.6)
    expected = {'value': 0.03333333333333333, 'passed': True}
    check('pbr004_rail_coherence_index', actual, expected)
    actual = m.ptt001_tau_valid(0.4, 0.5, 0.6, 0.7)
    expected = 0.282258064516129
    check('ptt001_tau_valid', actual, expected)
    actual = m.ptt001_power_telemetry_freshness_at_use_gate(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = {'value': -0.5256756756756756, 'passed': True}
    check('ptt001_power_telemetry_freshness_at_use_gate', actual, expected)
    actual = m.paa001_actuation_enable_authority_gate(True, True, True, True, True, True)
    expected = False
    check('paa001_actuation_enable_authority_gate', actual, expected)
    actual = m.paa002_actuator_induced_bus_sag_closure(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = {'value': -0.72, 'passed': False}
    check('paa002_actuator_induced_bus_sag_closure', actual, expected)
    actual = m.paa003_thermal_voltage_derated_actuator_envelope(1, 60, 50, 90, 12, 9, 13)
    expected = 0.75
    check('paa003_thermal_voltage_derated_actuator_envelope', actual, expected)
    actual = m.paa004_safe_reenable_delay(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = 0.8
    check('paa004_safe_reenable_delay', actual, expected)
    actual = m.tpd001_two_node_thermal_rc_step(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 0.5)
    expected = [0.8999999999999999, 0.494949494949495]
    check('tpd001_two_node_thermal_rc_step', actual, expected)
    actual = m.tpd002_thermal_timing_derate(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = {'value': 0.4, 'passed': True}
    check('tpd002_thermal_timing_derate', actual, expected)
    actual = m.tpd003_thermal_distortion_confidence_ceiling(0.4, 0.5, 0.6, 0.7)
    expected = 0.4
    check('tpd003_thermal_distortion_confidence_ceiling', actual, expected)
    actual = m.ecl001_energy_continuity_margin(0.4, 0.5, [0.4, 0.8], [0.4, 0.8], 0.5, 0.9, 1.0)
    expected = -0.8
    check('ecl001_energy_continuity_margin', actual, expected)
    actual = m.ecl002_regulation_chain_delivery_margin(0.4, [0.4, 0.8], 0.6, 0.7)
    expected = {'value': -1.6742857142857144, 'passed': False}
    check('ecl002_regulation_chain_delivery_margin', actual, expected)
    actual = m.ecl003_priority_load_shed_optimization([0.4, 0.8], [0.4, 0.8], 0.6, 0.7)
    expected = [[], 0]
    check('ecl003_priority_load_shed_optimization', actual, expected)


def check_safe_velocity_margin(m):
    actual = m.compute_truth_conditioned_safe_velocity_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    expected = -0.5
    check('compute_truth_conditioned_safe_velocity_margin', actual, expected)


def check_specific_energy_reserve_to_go(m):
    actual = m.compute_specific_energy_reserve_margin(0.4, 0.5, 0.6)
    expected = -0.7000000000000001
    check('compute_specific_energy_reserve_margin', actual, expected)


def check_lawful_actuation(m):
    check("cbf_margin", m.cbf_margin([0], [0.5], [2], 1, 1), 1.25)
    check("clf_value", m.clf_value([1], [0]), 0.5)
    check("clf_vdot", m.clf_vdot([1], [-0.4], [0]), -0.4)
    check("clf_margin", m.clf_margin([1], [-0.4], [0], 1), -0.1)
    check("null_set_trigger", m.null_set_trigger(False), True)
    active = m.lawful_control_qp([1], [0], [], 1, 1, [(-1, 1)], Gamma=2, x_ref=[0])
    check("active CLF [control, slack, null_set]", [active["u_star"][0], active["clf_slack"], active["null_set"]],
          [-0.4, 0.1, True])
    clear = m.lawful_control_qp([0], [0], [[2]], 1, 1, [(-1, 1)], x_ref=[0])
    check("clear [success, safe_without_slack, null_set]",
          [clear["success"], clear["safe_without_slack"], clear["null_set"]], [True, True, False])


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


FIXTURES = {
    "abort_closure_margin.py": check_abort_closure_margin,
    "actuator_saturation.py": check_actuator_saturation,
    "actuator_slew_rate.py": check_actuator_slew_rate,
    "attainable_wrench_residual.py": check_attainable_wrench_residual,
    "control_allocation_residual.py": check_control_allocation_residual,
    "controllability_margin.py": check_controllability_margin,
    "lawful_actuation_clf_cbf_qp.py": check_lawful_actuation,
    "lease_validity_margin.py": check_lease_validity_margin,
    "mechatronics_power_roundup.py": check_mechatronics_power_roundup,
    "safe_velocity_margin.py": check_safe_velocity_margin,
    "specific_energy_reserve_to_go.py": check_specific_energy_reserve_to_go,
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
    print("PASS hardware_viability/actuator")

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
