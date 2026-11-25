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


def check_c6_1_los_terrain_mask_closure(m):
    actual = m.compute_los_terrain_mask_margin(0.4, 0.5)
    expected = -0.09999999999999998
    check('compute_los_terrain_mask_margin', actual, expected)


def check_lane_aware_confidence_ceiling(m):
    actual = m.compute_lane_aware_confidence_ceiling(0.9, 'local_nac', 'PAD_TILE_INGESTED', 1.0, 6.0)
    expected = [0.9, 1.0]
    check('compute_lane_aware_confidence_ceiling', actual, expected)


def check_local_hazard_claim_gate(m):
    actual = m.compute_local_hazard_claim_gate('local_nac', True, 'PAD_TILE_INGESTED', 0.8, 0.5)
    expected = True
    check('compute_local_hazard_claim_gate', actual, expected)


def check_multiscale_disagreement_margin(m):
    actual = m.compute_multiscale_disagreement_margin([1.0, 2.0], [1.0, 2.0], 6.0)
    expected = 6.0
    check('compute_multiscale_disagreement_margin', actual, expected)


def check_roughness_alias_margin(m):
    actual = m.compute_roughness_alias_margin(0.5, 0.3, 0.35)
    expected = 0.14999999999999997
    check('compute_roughness_alias_margin', actual, expected)


def check_slope_uncertainty_guarded_margin(m):
    actual = m.compute_slope_uncertainty_guarded_margin(15.0, 10.0, 1.0, 2.0)
    expected = 3.0
    check('compute_slope_uncertainty_guarded_margin', actual, expected)


def check_terrain_commit_closure(m):
    actual = m.geospatial_status_ceiling_gate('REGION_PROXY', 'PAD_TILE_INGESTED')
    expected = True
    check('geospatial_status_ceiling_gate', actual, expected)
    actual = m.compute_terrain_commit_closure_gate(True, 'PAD_TILE_INGESTED', True, False)
    expected = True
    check('compute_terrain_commit_closure_gate', actual, expected)


def check_terrain_truth_disagreement(m):
    actual = m.compute_terrain_truth_disagreement_index(0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
    expected = 0.508888888888889
    check('compute_terrain_truth_disagreement_index', actual, expected)


def check_terrain_vertical_uncertainty_margin(m):
    actual = m.compute_terrain_vertical_uncertainty_margin(0.5, 0.2)
    expected = 0.3
    check('compute_terrain_vertical_uncertainty_margin', actual, expected)


def check_truth_cell_outrun_margin(m):
    actual = m.compute_truth_cell_outrun_margin(0.4, 0.5, 0.6)
    expected = 0.10000000000000003
    check('compute_truth_cell_outrun_margin', actual, expected)


FIXTURES = {
    "c6_1_los_terrain_mask_closure.py": check_c6_1_los_terrain_mask_closure,
    "lane_aware_confidence_ceiling.py": check_lane_aware_confidence_ceiling,
    "local_hazard_claim_gate.py": check_local_hazard_claim_gate,
    "multiscale_disagreement_margin.py": check_multiscale_disagreement_margin,
    "roughness_alias_margin.py": check_roughness_alias_margin,
    "slope_uncertainty_guarded_margin.py": check_slope_uncertainty_guarded_margin,
    "terrain_commit_closure.py": check_terrain_commit_closure,
    "terrain_truth_disagreement.py": check_terrain_truth_disagreement,
    "terrain_vertical_uncertainty_margin.py": check_terrain_vertical_uncertainty_margin,
    "truth_cell_outrun_margin.py": check_truth_cell_outrun_margin,
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
    print("PASS environment_geometry/terrain_truth")

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
