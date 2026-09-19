"""Guard for finding R-0803: the suite never resolves the operator's data root.

``tests/conftest.py::_isolated_data_root`` points ``REMEDY_DATA_DIR`` at a fresh
temporary directory for every test, and ``pytest_sessionfinish`` there fails the
run when the configured data root changed. These tests pin the per-test half:
without the fixture, ``resolve_data_root()`` falls through to the configured
root and every assertion below goes red.
"""

import os
import subprocess
import sys
from pathlib import Path

from packages.orchestration import data_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_DEFAULT_ROOT = Path(data_paths.__file__).resolve().parents[2] / ".data"


def test_the_resolved_root_is_under_the_pytest_temp_base(tmp_path_factory):
    root = data_paths.resolve_data_root().resolve()
    assert root != REPO_DEFAULT_ROOT
    assert root.is_relative_to(tmp_path_factory.getbasetemp().resolve())


def test_each_test_gets_a_fresh_empty_root():
    root = data_paths.resolve_data_root()
    assert root.is_dir()
    assert list(root.iterdir()) == []


def test_a_cli_subprocess_inherits_the_isolated_root():
    code = "from packages.orchestration.data_paths import resolve_data_root; print(resolve_data_root())"
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=REPO_ROOT, env=os.environ.copy(),
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout.strip()
    assert Path(out) == data_paths.resolve_data_root()
    assert Path(out).resolve() != REPO_DEFAULT_ROOT
