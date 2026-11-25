"""Execute this directory's working baseline. Pass --tree to include descendants."""
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent


def main():
    for entry in sorted(HERE.glob("*/smoke_test.py")):
        subprocess.run([sys.executable, "-S", "-P", "-B", "-X", "utf8", str(entry), "--tree"], check=True)
    print("PASS hardware_viability/thermal/thermal_truth/thermal_cross_domain_models")

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
