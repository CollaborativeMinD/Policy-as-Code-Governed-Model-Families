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


def check_base_excitation_transmissibility(m):
    actual = m.compute_base_excitation_transmissibility(0.4, 0.5, 0.6, 0.7)
    expected = {'frequency_ratio': 0.8,
     'transmissibility': 1.3520377540143105,
     'transmitted_acceleration': 0.9464264278100173}
    check('compute_base_excitation_transmissibility', actual, expected)


def check_fastener_preload_retention_margin(m):
    actual = m.compute_fastener_preload_retention_margin(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2)
    expected = {'thermal_loss': -0.036,
     'mechanical_loss': 1.1,
     'retained_preload': -0.6640000000000001,
     'retention_margin': -1.5533333333333335,
     'joint_secure': False}
    check('compute_fastener_preload_retention_margin', actual, expected)


def check_resonance_separation_margin(m):
    actual = m.compute_resonance_separation_margin([10, 20], [12, 30], 0.2)
    expected = {'minimum_separation_ratio': 0.16666666666666666,
     'required_exclusion_ratio': 0.2,
     'signed_margin': -0.033333333333333354,
     'critical_natural_frequency_hz': 10.0,
     'critical_forcing_frequency_hz': 12.0,
     'resonance_clear': False}
    check('compute_resonance_separation_margin', actual, expected)
    actual = m.compute_resonance_separation_margin([8, 12], [10], 0.2)
    expected = {'minimum_separation_ratio': 0.2,
     'required_exclusion_ratio': 0.2,
     'signed_margin': 0.0,
     'critical_natural_frequency_hz': 8.0,
     'critical_forcing_frequency_hz': 10.0,
     'resonance_clear': True}
    check('compute_resonance_separation_margin', actual, expected)


FIXTURES = {
    "Base-excitation-transmissibility.py": check_base_excitation_transmissibility,
    "Fastener-preload-retention-margin.py": check_fastener_preload_retention_margin,
    "Resonance-separation-margin.py": check_resonance_separation_margin,
}


def main():
    model_names = {p.name for p in HERE.glob("*.py") if not p.name.startswith(("test_", "run_"))}
    model_names -= {"smoke_test.py", "__init__.py"}
    if model_names != FIXTURES.keys():
        raise AssertionError(f"Unmatched model or fixture: {model_names ^ FIXTURES.keys()}")
    for filename, fixture in FIXTURES.items():
        isolated_model(filename, fixture)
    print("PASS hardware_viability/resonance")

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
