"""Isolated process runner for smoke scripts.

Each phase runs in its own process group with stdout/stderr to temp files.
No pipe inheritance. No shell=True. killpg cleanup on timeout and after exit.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
import time

MAX_OUTPUT_BYTES = 512 * 1024  # 512KB cap per stream


def _pg_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _kill_pg(pgid: int, sig: int) -> None:
    try:
        os.killpg(pgid, sig)
    except (ProcessLookupError, PermissionError):
        pass


def _ensure_pg_dead(pgid: int) -> None:
    if not _pg_exists(pgid):
        return
    _kill_pg(pgid, signal.SIGTERM)
    for _ in range(20):
        time.sleep(0.05)
        if not _pg_exists(pgid):
            return
    _kill_pg(pgid, signal.SIGKILL)
    for _ in range(20):
        time.sleep(0.05)
        if not _pg_exists(pgid):
            return


def run_phase(
    label: str,
    cmd: list[str],
    *,
    timeout: int = 120,
    env: dict[str, str] | None = None,
) -> int:
    """Run a smoke phase in full process isolation. Returns exit code."""
    print(f"--- {label} ---", flush=True)

    run_env = {**os.environ, **(env or {})}

    stdout_f = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".smoke-stdout", delete=False
    )
    stderr_f = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".smoke-stderr", delete=False
    )

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=stdout_f,
            stderr=stderr_f,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
            env=run_env,
        )
        pgid = os.getpgid(proc.pid)

        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill_pg(pgid, signal.SIGTERM)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                _kill_pg(pgid, signal.SIGKILL)
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass

        _ensure_pg_dead(pgid)

        stdout_f.seek(0)
        stderr_f.seek(0)
        stdout_text = stdout_f.read(MAX_OUTPUT_BYTES)
        stderr_text = stderr_f.read(MAX_OUTPUT_BYTES)
    finally:
        stdout_f.close()
        stderr_f.close()
        try:
            os.unlink(stdout_f.name)
        except OSError:
            pass
        try:
            os.unlink(stderr_f.name)
        except OSError:
            pass

    if stdout_text:
        sys.stdout.write(stdout_text)
        if not stdout_text.endswith("\n"):
            sys.stdout.write("\n")
        sys.stdout.flush()
    if stderr_text:
        sys.stderr.write(stderr_text)
        if not stderr_text.endswith("\n"):
            sys.stderr.write("\n")
        sys.stderr.flush()

    if timed_out:
        print(f"FAIL: {label} timed out after {timeout}s", file=sys.stderr, flush=True)
        return 124

    if proc.returncode != 0:
        print(f"FAIL: {label} exited with code {proc.returncode}", file=sys.stderr, flush=True)

    return proc.returncode
