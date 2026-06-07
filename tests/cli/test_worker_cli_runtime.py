"""Runtime subprocess tests for worker CLI — thin wrapper around standalone smoke script.

Pytest runs a single subprocess (the smoke script) per test, avoiding
pytest-process teardown contamination from many in-process CLI calls.

IMPORTANT: This file must NOT import packages.orchestration.proposed_tasks
or any module that uses fcntl.flock.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

SMOKE_SCRIPT = "scripts/remedy_runtime_cli_smoke.py"
TIMEOUT = 30


def _run_smoke(mode: str) -> subprocess.CompletedProcess:
    """Run standalone smoke script in isolated subprocess."""
    return subprocess.run(
        [sys.executable, SMOKE_SCRIPT, "--mode", mode],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        stdin=subprocess.DEVNULL,
        close_fds=True,
    )


class TestWorkerRuntimeSmoke:
    def test_worker_flow(self):
        """Full worker lifecycle: propose, enqueue, execute, verify events."""
        r = _run_smoke("worker")
        assert r.returncode == 0, f"Smoke failed:\n{r.stdout}\n{r.stderr}"
        assert "worker: PASS" in r.stdout
