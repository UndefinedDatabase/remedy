"""Runaway fixtures for `packages/orchestration/exec_guard.py` — F085 stage 1, T001.

Each fixture is a real child process, so every test here carries the
`subprocess` marker registered in `pyproject.toml`. Limits are kept deliberately
small: the point is that the guard trips, not how long it takes to trip.

The guard has NO callers in this repository, so nothing here says anything about
whether any existing Remedy subprocess is limited. It is not.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time

import pytest

from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded

#: Unique argv token so `pgrep -af` can find leftovers of THIS run and no other.
MARKER = f"REMEDY_EXEC_GUARD_FIXTURE_{os.getpid()}"

_MEBIBYTE = 1024 * 1024


def _child(source: str) -> list[str]:
    """argv for a python child carrying MARKER, so an orphan is findable by name."""
    return [sys.executable, "-c", source, MARKER]


def _survivors() -> list[str]:
    """Command lines still matching MARKER, with pgrep's own line filtered out."""
    found = subprocess.run(["pgrep", "-af", MARKER], capture_output=True, text=True)
    return [line for line in found.stdout.splitlines() if "pgrep" not in line]


@pytest.mark.subprocess
def test_well_behaved_command_is_unchanged_by_the_guard():
    """A command inside its limits produces exactly what it produces unguarded."""
    argv = _child(
        "import sys\n"
        "sys.stdout.write('stdout payload\\n')\n"
        "sys.stderr.write('stderr payload\\n')\n"
    )
    bare = subprocess.run(argv, capture_output=True)

    result = run_guarded(
        argv,
        ExecGuardPolicy(
            cpu_seconds=5,
            address_space_bytes=512 * _MEBIBYTE,
            open_files=256,
            wall_timeout_seconds=10.0,
            output_cap_bytes=64 * 1024,
        ),
    )

    assert result.returncode == bare.returncode == 0
    assert result.stdout == bare.stdout
    assert result.stderr == bare.stderr
    assert result.term_signal is None
    assert result.classification == "ok"
    assert result.tripped_limit is None
    assert result.stdout_truncated is False
    assert result.stderr_truncated is False
    assert result.stdout_bytes_seen == len(bare.stdout)
    assert result.stderr_bytes_seen == len(bare.stderr)
    assert result.limits_unsupported == ()


@pytest.mark.subprocess
def test_cpu_limit_kills_a_busy_loop_and_names_the_limit():
    """RLIMIT_CPU with a grace band gives SIGXCPU, which is attributable."""
    result = run_guarded(
        _child("x = 0\nwhile True:\n    x += 1\n"),
        ExecGuardPolicy(cpu_seconds=1, output_cap_bytes=64 * 1024),
    )

    assert result.returncode is None
    assert result.term_signal == "SIGXCPU"
    assert result.classification == "resource_limit"
    assert result.tripped_limit == "cpu_seconds"
    assert result.tripped_limit in result.limits_enforced
    assert result.cpu_seconds_used >= 1.0


@pytest.mark.subprocess
def test_wall_timeout_kills_a_sleeper_the_cpu_limit_never_reaches():
    """The guard's own deadline, with no cpu limit that could fire first."""
    result = run_guarded(
        _child("import time\ntime.sleep(120)\n"),
        ExecGuardPolicy(wall_timeout_seconds=1.0, output_cap_bytes=64 * 1024),
    )

    assert result.classification == "resource_limit"
    assert result.tripped_limit == "wall_timeout"
    assert result.tripped_limit in result.limits_enforced
    assert result.returncode is None
    # Upper bound only: the child would have slept 120s, so any value well under
    # that proves the deadline fired. An exact duration would be a flaky assert.
    assert result.wall_seconds < 30.0


@pytest.mark.subprocess
def test_output_cap_truncates_storage_while_the_count_stays_true():
    """Past the cap the guard stops storing and keeps counting."""
    cap = 4096
    result = run_guarded(
        _child("import sys\nfor _ in range(200):\n    sys.stdout.write('x' * 1000)\n"),
        ExecGuardPolicy(output_cap_bytes=cap, wall_timeout_seconds=30.0),
    )

    assert result.classification == "resource_limit"
    assert result.tripped_limit == "output_bytes"
    assert result.tripped_limit in result.limits_enforced
    assert result.stdout_truncated is True
    assert len(result.stdout) <= cap
    assert result.stdout_bytes_seen > cap
    assert result.stdout_bytes_seen == 200_000


@pytest.mark.subprocess
def test_address_space_limit_is_enforced_but_not_attributed():
    """The SAME argv fails tight and succeeds generous — enforcement, not attribution.

    Nothing is asserted about `tripped_limit`: a RLIMIT_AS death is an ordinary
    exit 1 with no signal, so the guard's docstring declines to claim it and this
    test declines to invent it.
    """
    argv = _child("b = bytearray(200 * 1024 * 1024)\nprint(len(b))\n")

    tight = run_guarded(
        argv,
        ExecGuardPolicy(address_space_bytes=64 * _MEBIBYTE, wall_timeout_seconds=30.0, output_cap_bytes=64 * 1024),
    )
    generous = run_guarded(
        argv,
        ExecGuardPolicy(address_space_bytes=2048 * _MEBIBYTE, wall_timeout_seconds=30.0, output_cap_bytes=64 * 1024),
    )

    assert tight.returncode != 0
    assert b"MemoryError" in tight.stderr
    assert "address_space_bytes" in tight.limits_enforced
    assert generous.returncode == 0
    assert generous.stdout.strip() == b"209715200"


@pytest.mark.subprocess
def test_no_child_survives_a_killed_run():
    """The group kill reaches a grandchild too, and nothing outlives run_guarded."""
    grandchild = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)', sys.argv[1]])\n"
        "time.sleep(120)\n"
    )
    result = run_guarded(
        _child(grandchild),
        ExecGuardPolicy(wall_timeout_seconds=1.0, output_cap_bytes=64 * 1024),
    )
    assert result.tripped_limit == "wall_timeout"

    # Brief retry: the kernel reaps the group asynchronously.
    for _ in range(10):
        survivors = _survivors()
        if not survivors:
            break
        time.sleep(0.2)
    assert survivors == [], f"orphans survived run_guarded: {survivors}"
