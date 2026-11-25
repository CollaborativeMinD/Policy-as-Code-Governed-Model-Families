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


def check_chi_hardware_coefficient(m):
    actual = m.compute_hardware_coefficient(0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    expected = 0.44559760983162217
    check('compute_hardware_coefficient', actual, expected)
    actual = m.lambdified()(2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
    expected = 0.4569895542260725
    check('lambdified', actual, expected)


def check_chi_squared_reality_gap_monitor(m):
    actual = m.compute_chi_squared_gap([0.4, 0.8], [0.4, 0.8])
    expected = 0.0
    check('compute_chi_squared_gap', actual, expected)
    actual = m.lambdified()(2.0, 3.0)
    expected = 0.3333333333333333
    check('lambdified', actual, expected)


def check_delay_adjusted_innovation_consistency(m):
    actual = m.compute_delay_adjusted_innovation_consistency([2, -1], [[3, 0.2], [0.2, 1]], 0.5, 1, 1)
    expected = 5.27027027027027
    check('compute_delay_adjusted_innovation_consistency', actual, expected)


def check_imm_mode_probability_update(m):
    actual = m.compute_imm_mode_probability_update([0.6, 0.4], [[0.8, 0.2], [0.1, 0.9]], [0.7, 0.2])
    expected = [0.7913043478260869, 0.20869565217391306]
    check('compute_imm_mode_probability_update', actual, expected)
    actual = m.compute_imm_mode_probability_update([0, 0], [[1, 0], [0, 1]], [1, 1])
    expected = [0.5, 0.5]
    check('compute_imm_mode_probability_update', actual, expected)
    try:
        m.compute_imm_mode_probability_update([1], [[0.9]], [1])
    except ValueError:
        print('  compute_imm_mode_probability_update rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_kalman_filter(m):
    actual = m.kalman_predict_update(
        [[1, 1], [0, 1]],
        [[0], [1]],
        [[1, 0]],
        [1, 2],
        [[2, 0], [0, 1]],
        [0.5],
        [4],
        [[0.1, 0], [0, 0.1]],
        [[0.5]],
    )
    expected = [[3.861111111111111, 2.7777777777777777],
     [[0.4305555555555554, 0.13888888888888884],
      [0.13888888888888884, 0.8222222222222223]]]
    check('kalman_predict_update', actual, expected)
    try:
        m.kalman_predict_update([[1]], [[0]], [[1]], [0], [[0]], [0], [1], [[0]], [[0]])
    except ValueError:
        print('  kalman_predict_update rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_mahalanobis(m):
    actual = m.compute_mahalanobis_distance([2, 3], [1, 1], [[2, 0.1], [0.1, 1]])
    expected = 2.078847767442581
    check('compute_mahalanobis_distance', actual, expected)
    try:
        m.compute_mahalanobis_distance([1,2], [0,0], [[1,1],[1,1]])
    except ValueError:
        print('  compute_mahalanobis_distance rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_streaming_deviation(m):
    actual = m.update_streaming_deviation(0.4, 0.5, 0.6, 4)
    expected = [0.475, 0.6074999999999999, -0.16666666666666657]
    check('update_streaming_deviation', actual, expected)


def check_unknown_correlation_safe_fusion(m):
    actual = m.compute_covariance_intersection(
        [1, 2],
        [[2, 0.1], [0.1, 3]],
        [3, 1],
        [[3, 0], [0, 1]],
        0.4,
    )
    expected = [[1.985672049124403, 1.19103934500796],
     [[2.498294291562429, 0.022742779167614285],
      [0.02274277916761428, 1.3634296110984763]]]
    check('compute_covariance_intersection', actual, expected)
    try:
        m.compute_covariance_intersection([1], [[1]], [1], [[1]], 2)
    except ValueError:
        print('  compute_covariance_intersection rejected invalid input')
    else:
        raise AssertionError("expected ValueError")


def check_weighted_divergence(m):
    actual = m.compute_weighted_divergence([2, 3], [1, 1], [[2, 0.1], [0.1, 1]])
    expected = 2.5298221281347035
    check('compute_weighted_divergence', actual, expected)


def check_z_score_universal_stress_metric(m):
    actual = m.compute_z_score(0.4, 0.5, 2.0)
    expected = -0.04999999999999999
    check('compute_z_score', actual, expected)
    actual = m.lambdified()(2.0, 3.0, 4.0)
    expected = -0.25
    check('lambdified', actual, expected)


FIXTURES = {
    "chi_hardware_coefficient.py": check_chi_hardware_coefficient,
    "chi_squared_reality_gap_monitor.py": check_chi_squared_reality_gap_monitor,
    "delay-adjusted-innovation-consistency.py": check_delay_adjusted_innovation_consistency,
    "IMM-mode-probability-update.py": check_imm_mode_probability_update,
    "kalman_filter.py": check_kalman_filter,
    "mahalanobis.py": check_mahalanobis,
    "streaming_deviation.py": check_streaming_deviation,
    "unknown-correlation-safe-fusion.py": check_unknown_correlation_safe_fusion,
    "weighted_divergence.py": check_weighted_divergence,
    "z_score_universal_stress_metric.py": check_z_score_universal_stress_metric,
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
    print("PASS estimation_detection")

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
