"""Behavioral tests for scripts/remedy_pytest.sh.

These tests actually execute the wrapper and verify exit codes are truthful.
Uses isolated lock files and short timeouts. Fast, foreground, no flaky concurrency.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
WRAPPER = str(REPO_ROOT / "scripts" / "remedy_pytest.sh")


def _run_wrapper(
    args: list[str],
    *,
    timeout_sec: int = 10,
    lock_file: str | None = None,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess:
    env = {**os.environ}
    env["REMEDY_PYTEST_TIMEOUT_SEC"] = str(timeout_sec)
    if lock_file:
        env["REMEDY_PYTEST_LOCK"] = lock_file
    else:
        env["REMEDY_PYTEST_LOCK"] = tempfile.mktemp(suffix=".lock")
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [WRAPPER] + args,
        capture_output=True,
        text=True,
        timeout=timeout_sec + 10,
        env=env,
        cwd=str(REPO_ROOT),
    )


class TestWrapperExitCodes:
    """Wrapper must propagate pytest exit codes truthfully."""

    def test_passing_test_exits_zero(self, tmp_path):
        test_file = tmp_path / "test_ok.py"
        test_file.write_text("def test_pass(): assert True\n")
        result = _run_wrapper([str(test_file), "-q"])
        assert result.returncode == 0

    def test_failing_test_exits_nonzero(self, tmp_path):
        test_file = tmp_path / "test_fail.py"
        test_file.write_text("def test_fail(): assert False\n")
        result = _run_wrapper([str(test_file), "-q"])
        assert result.returncode != 0

    def test_nonexistent_path_exits_nonzero(self):
        result = _run_wrapper(["tests/does_not_exist_xyz.py", "-q"])
        assert result.returncode != 0

    def test_timeout_exits_124(self, tmp_path):
        test_file = tmp_path / "test_slow.py"
        test_file.write_text(
            "import time\n"
            "def test_slow(): time.sleep(30)\n"
        )
        result = _run_wrapper([str(test_file), "-q"], timeout_sec=2)
        assert result.returncode == 124
        assert "timed out" in result.stderr.lower()


class TestWrapperLock:
    """Wrapper must refuse parallel runs via flock."""

    def test_lock_busy_exits_nonzero(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY)
        try:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = _run_wrapper(
                ["--co", "-q"],
                lock_file=lock_file,
            )
            assert result.returncode != 0
            assert "already active" in result.stderr.lower()
        finally:
            os.close(fd)

    def test_lock_message_is_clear(self, tmp_path):
        lock_file = str(tmp_path / "test.lock")
        fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY)
        try:
            import fcntl

            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = _run_wrapper(
                ["--co", "-q"],
                lock_file=lock_file,
            )
            assert "Refusing to start a parallel run" in result.stderr
        finally:
            os.close(fd)
