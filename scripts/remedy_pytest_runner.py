#!/usr/bin/env python3
"""Pipe-safe pytest runner with process group isolation.

Runs pytest in its own process group with stdout/stderr redirected to temp
files instead of inherited pipes. This prevents child/grandchild processes
from holding pipes open and hanging the caller (e.g. bash scripts waiting
for EOF on stdout).

Usage:
    python3 scripts/remedy_pytest_runner.py -- tests/ -q --cache-clear

Environment:
    REMEDY_PYTEST_TIMEOUT_SEC  — max seconds (default: 600)
    REMEDY_PYTHON              — python binary (default: python3)
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
import time

MAX_OUTPUT_BYTES = 512 * 1024  # 512KB cap per stream


def _process_group_exists(pgid: int) -> bool:
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
    if not _process_group_exists(pgid):
        return
    _kill_pg(pgid, signal.SIGTERM)
    for _ in range(20):
        time.sleep(0.05)
        if not _process_group_exists(pgid):
            return
    _kill_pg(pgid, signal.SIGKILL)
    for _ in range(20):
        time.sleep(0.05)
        if not _process_group_exists(pgid):
            return


def run(pytest_args: list[str]) -> int:
    timeout_sec = int(os.environ.get("REMEDY_PYTEST_TIMEOUT_SEC", "600"))
    python = os.environ.get("REMEDY_PYTHON", sys.executable)
    cmd = [python, "-m", "pytest"] + pytest_args

    stdout_f = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".pytest-stdout", delete=False
    )
    stderr_f = tempfile.NamedTemporaryFile(
        mode="w+", suffix=".pytest-stderr", delete=False
    )

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=stdout_f,
            stderr=stderr_f,
            stdin=subprocess.DEVNULL,
            close_fds=True,
            start_new_session=True,
        )
        pgid = os.getpgid(proc.pid)

        timed_out = False
        try:
            try:
                proc.wait(timeout=timeout_sec)
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
        finally:
            # Guarantee process group cleanup on any exit path
            _ensure_pg_dead(pgid)

        # Read bounded output from temp files
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

    # Print captured output (now safe — all processes dead)
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
        sys.stderr.write(
            f"\nERROR: pytest timed out after {timeout_sec} seconds.\n"
        )
        sys.stderr.flush()
        return 124

    return proc.returncode


def main() -> None:
    args = sys.argv[1:]
    # Strip leading '--' if present
    if args and args[0] == "--":
        args = args[1:]
    sys.exit(run(args))


if __name__ == "__main__":
    main()
