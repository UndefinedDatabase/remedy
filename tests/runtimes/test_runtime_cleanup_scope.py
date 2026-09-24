"""The cleanup scans find this worker's processes and never a sibling worker's (R-1028).

Under `pytest -n auto` worker gw1's basetemp `.../popen-gw1` is a string prefix of gw10's,
so the file-level scan of `tests/runtimes/runtime_cleanup.py` once reported gw10's live
runtimes as gw1's survivors, and gw1's whole file errored at teardown. Each test starts one
idle process that names a path in its argv, or runs inside one, and asks the scans about it.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.runtimes.runtime_cleanup import RuntimeRegistry, basetemp_survivors, names_path

pytestmark = pytest.mark.subprocess

IDLE = "import time\nwhile True: time.sleep(0.2)\n"


@pytest.fixture
def idle(tmp_path):
    """Start an idle process with the given argv tail and cwd; stop every one at teardown."""
    procs: list[subprocess.Popen] = []

    def start(*argv: str, cwd: Path | None = None) -> subprocess.Popen:
        proc = subprocess.Popen([sys.executable, "-c", IDLE, *argv], cwd=str(cwd or tmp_path))
        procs.append(proc)
        return proc

    yield start
    for proc in procs:
        proc.kill()
        proc.wait(timeout=10)


def _pids(entries: list[str]) -> set[int]:
    return {int(entry.split()[0]) for entry in entries}


@pytest.mark.parametrize(("text", "expected"), [
    ("--repo /t/popen-gw1/proj", True),
    ("--repo /t/popen-gw1", True),
    ("--repo /t/popen-gw1 --json", True),
    ("--repo /t/popen-gw10/proj", False),
    ("--repo /t/popen-gw1x", False),
])
def test_a_root_is_named_only_as_itself_or_a_parent(text, expected):
    assert names_path(text, "/t/popen-gw1") is expected


def test_the_file_scan_skips_a_sibling_basetemp_named_in_argv(tmp_path, idle):
    mine = tmp_path / "popen-gw1"
    sibling = tmp_path / "popen-gw10"
    ours = idle("--repo", str(mine / "proj"))
    theirs = idle("--repo", str(sibling / "proj"))

    found = _pids(basetemp_survivors(mine))

    assert ours.pid in found
    assert theirs.pid not in found


def test_the_file_scan_skips_a_server_running_in_a_sibling_basetemp(tmp_path, idle):
    mine = tmp_path / "popen-gw1"
    sibling = tmp_path / "popen-gw10"
    for directory in (mine, sibling):
        directory.mkdir()
    ours = idle("server.py", cwd=mine)
    theirs = idle("server.py", cwd=sibling)

    found = _pids(basetemp_survivors(mine))

    assert ours.pid in found
    assert theirs.pid not in found


def test_the_per_test_scan_skips_a_sibling_tmp_path(tmp_path, idle):
    mine = tmp_path / "test_x1"
    sibling = tmp_path / "test_x10"
    ours = idle("--repo", str(mine / "proj"))
    theirs = idle("--repo", str(sibling / "proj"))

    found = _pids(RuntimeRegistry(mine).survivors_in_tmp())

    assert ours.pid in found
    assert theirs.pid not in found
