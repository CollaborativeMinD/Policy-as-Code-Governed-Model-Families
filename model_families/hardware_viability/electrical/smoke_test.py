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


def check_bus_anchor_consistency_margin(m):
    actual = m.compute_bus_anchor_consistency_margin(0.4, 0.5)
    expected = 0.4
    check('compute_bus_anchor_consistency_margin', actual, expected)


def check_electrical_survivability_margins(m):
    actual = m.compute_effective_brownout_margin(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -2.2
    check('compute_effective_brownout_margin', actual, expected)
    actual = m.compute_thermal_derated_power_margin(50, 60, 50, 90, 0.95, 12, 2)
    expected = 21.625
    check('compute_thermal_derated_power_margin', actual, expected)
    actual = m.compute_recovery_energy_margin(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -2.2
    check('compute_recovery_energy_margin', actual, expected)
    actual = m.compute_bus_clear_time_margin(0.4, 2, 0.6, 0.7, 0.8, 0.9)
    expected = -5.333333333333333
    check('compute_bus_clear_time_margin', actual, expected)
    actual = m.compute_segment_isolation_margin(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -2.2
    check('compute_segment_isolation_margin', actual, expected)
    actual = m.compute_post_recovery_reacquisition_margin(0.4, 0.5, 0.6, 0.7, 0.8)
    expected = -2.2
    check('compute_post_recovery_reacquisition_margin', actual, expected)
    actual = m.compute_telemetry_use_freshness_margin(2, 3, 2, 0.1, 0.2)
    expected = 0.7
    check('compute_telemetry_use_freshness_margin', actual, expected)
    actual = m.compute_mixed_stream_coherence_margin(0.4, [0.4, 0.8])
    expected = 0.0
    check('compute_mixed_stream_coherence_margin', actual, expected)
    actual = m.compute_boot_epoch_sequence_gate('boot', 'boot', 1, 2, 3, 4, 0)
    expected = True
    check('compute_boot_epoch_sequence_gate', actual, expected)
    actual = m.compute_substrate_evidence_completeness_ratio({'a': True, 'b': False})
    expected = 0.5
    check('compute_substrate_evidence_completeness_ratio', actual, expected)
    actual = m.compute_trust_root_attestation_freshness_margin(5, 3, 2)
    expected = 4.0
    check('compute_trust_root_attestation_freshness_margin', actual, expected)
    actual = m.compute_authority_to_act_gate(0.4, 0.5, 0.6, True, True, True, True)
    expected = False
    check('compute_authority_to_act_gate', actual, expected)
    actual = m.compute_hardware_timing_closure_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = -3.1
    check('compute_hardware_timing_closure_margin', actual, expected)
    actual = m.compute_thermal_timing_derate_margin(0.4, 0.5, 0.8, 0.7, 0.8, 0.9)
    expected = -2.625
    check('compute_thermal_timing_derate_margin', actual, expected)
    actual = m.compute_hardware_closed_command_seam_gate(0.4, 0.5, 0.6, 0.7, True)
    expected = True
    check('compute_hardware_closed_command_seam_gate', actual, expected)


def check_illumination_cycle_energy_margin(m):
    actual = m.compute_illumination_duty_cycle_energy_margin(100.0, 20.0, 5.0, 10.0, 2.0, 3.0)
    expected = 100.0
    check('compute_illumination_duty_cycle_energy_margin', actual, expected)


def check_occlusion_energy_reserve_margin(m):
    actual = m.compute_occlusion_energy_reserve_margin(100.0, 10.0, 2.0, 5.0, 15.0)
    expected = 60.0
    check('compute_occlusion_energy_reserve_margin', actual, expected)


def check_regulation_chain_disparity_margin(m):
    actual = m.compute_regulation_chain_disparity_margin(0.4, 0.5, 0.6)
    expected = 0.5
    check('compute_regulation_chain_disparity_margin', actual, expected)


FIXTURES = {
    "bus_anchor_consistency_margin.py": check_bus_anchor_consistency_margin,
    "electrical_survivability_margins.py": check_electrical_survivability_margins,
    "illumination_cycle_energy_margin.py": check_illumination_cycle_energy_margin,
    "occlusion_energy_reserve_margin.py": check_occlusion_energy_reserve_margin,
    "regulation_chain_disparity_margin.py": check_regulation_chain_disparity_margin,
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
    print("PASS hardware_viability/electrical")

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
