"""R-1411: a real pytest run beside a supervisor that answers on the guarded data root.

The installed service writes the operator's data root while a run lasts, its call ledger above all,
and the R-0803 guard read that as the run's own pollution. Each test here starts a child pytest run
whose guarded root is a scratch folder, with a unix socket listening where a supervisor's would, and
a child test that writes one folder of that root.
"""
from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CHILD_TEST = (
    "import os\n"
    "from pathlib import Path\n\n\n"
    "def test_it_writes_one_folder_of_the_guarded_root():\n"
    "    Path(os.environ['R1411_TARGET']).mkdir(parents=True)\n"
)


@pytest.fixture
def guarded_root():
    """A short scratch data root, so the socket path stays below the unix limit."""
    root = Path(tempfile.mkdtemp(prefix="r1411-"))
    (root / "serve").mkdir()
    yield root
    shutil.rmtree(root, ignore_errors=True)


def _child_run(root: Path, target: str, tmp_path: Path, *, supervisor: bool) -> subprocess.CompletedProcess:
    test_file = tmp_path / "child" / "test_child.py"
    test_file.parent.mkdir()
    test_file.write_text(CHILD_TEST, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if not k.startswith("REMEDY_TEST_")}
    env.update({"REMEDY_DATA_DIR": str(root), "R1411_TARGET": str(root / target), "REMEDY_TEST_LOAD_LOG": ""})
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) if supervisor else None
    try:
        if listener is not None:
            listener.bind(str(root / "serve" / "serve.sock"))
            listener.listen(8)
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest", "-n", "0",
             "--basetemp", str(tmp_path / "base"), str(test_file)],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300)
    finally:
        if listener is not None:
            listener.close()


def test_a_write_in_the_supervisors_own_folder_passes_while_one_answers(guarded_root, tmp_path):
    done = _child_run(guarded_root, os.path.join("api", "calls"), tmp_path, supervisor=True)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "R-1411: 2 entries of the configured data root" in done.stdout
    assert "R-0803" not in done.stdout


def test_a_record_written_beside_an_answering_supervisor_still_fails_the_run(guarded_root, tmp_path):
    done = _child_run(guarded_root, os.path.join("jobs", "job-1"), tmp_path, supervisor=True)
    assert done.returncode == 1, done.stdout + done.stderr
    assert "R-0803: the test run changed the configured data root" in done.stdout


def test_the_same_write_fails_the_run_when_no_supervisor_answers(guarded_root, tmp_path):
    done = _child_run(guarded_root, os.path.join("api", "calls"), tmp_path, supervisor=False)
    assert done.returncode == 1, done.stdout + done.stderr
    assert "R-0803: the test run changed the configured data root" in done.stdout
    assert "R-1411" not in done.stdout
