"""Runtime subprocess tests for propose CLI — thin wrapper around standalone smoke script.

Pytest runs a single subprocess (the smoke script) per test, avoiding
pytest-process teardown contamination from many in-process CLI calls.

Process isolation: Popen + start_new_session + temp files (no pipes).

IMPORTANT: This file must NOT import packages.orchestration.proposed_tasks
or any module that uses fcntl.flock.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile

SMOKE_SCRIPT = "scripts/remedy_runtime_cli_smoke.py"
TIMEOUT = 30


def _run_smoke_isolated(mode: str) -> tuple[int, str, str]:
    """Run smoke script with full process isolation. No pipes."""
    cmd = [sys.executable, SMOKE_SCRIPT, "--mode", mode]
    out_f = tempfile.NamedTemporaryFile(mode="w+", suffix=".out", delete=False)
    err_f = tempfile.NamedTemporaryFile(mode="w+", suffix=".err", delete=False)
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=out_f,
            stderr=err_f,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
        )
        pgid = os.getpgid(proc.pid)
        timed_out = False
        try:
            proc.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(pgid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(pgid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
                proc.wait(timeout=3)

        # Best-effort cleanup
        try:
            os.killpg(pgid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass

        out_f.seek(0)
        err_f.seek(0)
        stdout = out_f.read(64 * 1024)
        stderr = err_f.read(64 * 1024)
    finally:
        out_f.close()
        err_f.close()
        try:
            os.unlink(out_f.name)
        except OSError:
            pass
        try:
            os.unlink(err_f.name)
        except OSError:
            pass

    rc = 124 if timed_out else proc.returncode
    return rc, stdout, stderr


class TestProposeRuntimeSmoke:
    def test_propose_flow(self):
        """Full propose lifecycle: list, evaluate, approve, materialize, events."""
        rc, stdout, stderr = _run_smoke_isolated("propose")
        assert rc == 0, f"Smoke failed (rc={rc}):\n{stdout}\n{stderr}"
        assert "propose: PASS" in stdout
