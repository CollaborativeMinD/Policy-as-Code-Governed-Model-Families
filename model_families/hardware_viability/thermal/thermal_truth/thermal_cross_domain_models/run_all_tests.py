#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
BASE = ROOT
loader = unittest.TestLoader()
suite = unittest.TestSuite()

for family in sorted(BASE.iterdir()):
    if not family.is_dir() or not list(family.glob("test_*.py")):
        continue
    sys.path.insert(0, str(family))
    try:
        for test_file in sorted(family.glob("test_*.py")):
            print(f"LOAD {test_file.relative_to(ROOT)}")
            module_name = test_file.stem
            if module_name in sys.modules:
                del sys.modules[module_name]
            module = __import__(module_name)
            suite.addTests(loader.loadTestsFromModule(module))
    finally:
        try:
            sys.path.remove(str(family))
        except ValueError:
            pass

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
if not result.wasSuccessful():
    print("THERMAL_CANDIDATE_TESTS_FAILED")
    raise SystemExit(1)
print("THERMAL_CANDIDATE_TESTS_PASS")
