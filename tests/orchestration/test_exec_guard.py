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

from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded, scrub_child_env

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


#: A child that prints its whole environment, one KEY=VALUE per line.
_ENV_DUMP = (
    "import os, sys\n"
    "sys.stdout.write(''.join(f'{k}={v}\\n' for k, v in sorted(os.environ.items())))\n"
)

#: CPython adds this to any child spawned with a restricted environment (PEP 538
#: locale coercion). It is the interpreter's, not the guard's, so assertions below
#: subtract it rather than crediting the guard with producing it.
_INTERPRETER_ADDED_ENV_KEYS = frozenset({"LC_CTYPE"})


def _dumped(result) -> dict[str, str]:
    """The child's environment from its stdout, minus what the interpreter added.

    Subtract-if-present, never assert-present: a build that does not coerce the
    locale has nothing to subtract and the assertions still hold.
    """
    lines = result.stdout.decode().splitlines()
    parsed = dict(line.split("=", 1) for line in lines if "=" in line)
    return {k: v for k, v in parsed.items() if k not in _INTERPRETER_ADDED_ENV_KEYS}


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
    # Tolerance strictly BELOW the limit, never ON it (R-0496): `ru_utime +
    # ru_stime` is the kernel's own CPU accounting, which is granular and rounds
    # against RLIMIT_CPU rather than exactly to it, so a value a few hundred
    # microseconds under an integer limit is the normal outcome. The property
    # this test is named for is the SIGXCPU trip asserted above; the number only
    # has to show the child really burned the CPU it was limited on.
    assert result.cpu_seconds_used >= 0.5


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


@pytest.mark.subprocess
def test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group():
    """A grandchild in its OWN session survives the kill and keeps holding the pipe.

    The deadline must still bound `run_guarded`'s own return (R-0495): the drain
    grace is a bounded cost on top of the deadline, not the escapee's lifetime.
    """
    escapee = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)', sys.argv[1]],\n"
        "                 start_new_session=True)\n"
        "time.sleep(120)\n"
    )
    started = time.monotonic()
    result = run_guarded(
        _child(escapee),
        ExecGuardPolicy(wall_timeout_seconds=1.0, stream_drain_grace_seconds=2.0, output_cap_bytes=64 * 1024),
    )
    elapsed = time.monotonic() - started

    assert result.tripped_limit == "wall_timeout"
    assert result.streams_complete is False
    # Upper bound only: the escapee sleeps 20s, so any return well under that is
    # the property. Deadline + grace is ~3s here; 10s leaves room for a slow box.
    assert elapsed < 10.0

    # The escapee outlives the guard BY DESIGN, so this test ends it rather than
    # leaving a MARKER process that a later test's pgrep sweep would find.
    subprocess.run(["pkill", "-f", MARKER], check=False)
    for _ in range(10):
        if not _survivors():
            break
        time.sleep(0.2)
    assert _survivors() == []


@pytest.mark.subprocess
def test_no_allowlist_hands_the_environment_to_the_child_unchanged():
    """The T001 contract, pinned: without an allowlist NOTHING is scrubbed.

    A forbidden key sits in `env` on purpose and arrives, so a migration that
    forgets its allowlist is visibly unprotected, not quietly half-protected.
    """
    passed = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-unscrubbed-by-design"}

    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(wall_timeout_seconds=10.0, env=passed),
    )

    assert result.returncode == 0
    assert _dumped(result) == passed


@pytest.mark.subprocess
def test_the_allowlist_keeps_only_the_variables_it_names():
    """An allowlisted key survives; an unlisted key never reaches the child."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "REMEDY_KEPT": "yes", "REMEDY_DROPPED": "no"},
            env_allowlist=("PATH", "REMEDY_KEPT"),
        ),
    )

    assert result.returncode == 0
    assert _dumped(result) == {"PATH": "/usr/bin", "REMEDY_KEPT": "yes"}


@pytest.mark.subprocess
def test_a_secret_like_variable_never_reaches_the_child_even_when_allowlisted():
    """`FORBIDDEN_ENV_KEYS` is the guard's floor: a wrong allowlist cannot lower it."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-should-never-appear"},
            env_allowlist=("PATH", "ANTHROPIC_API_KEY"),
        ),
    )

    assert result.returncode == 0
    assert "ANTHROPIC_API_KEY" not in _dumped(result)
    assert b"sk-should-never-appear" not in result.stdout
    assert _dumped(result) == {"PATH": "/usr/bin"}


@pytest.mark.subprocess
def test_the_ui_no_auto_build_variable_survives_an_allowlist_that_names_it():
    """R-0202: the variable a spawn path once dropped is allowlistable and arrives."""
    result = run_guarded(
        _child(_ENV_DUMP),
        ExecGuardPolicy(
            wall_timeout_seconds=10.0,
            env={"PATH": "/usr/bin", "REMEDY_UI_NO_AUTO_BUILD": "1"},
            env_allowlist=("PATH", "REMEDY_UI_NO_AUTO_BUILD"),
        ),
    )

    assert result.returncode == 0
    assert _dumped(result)["REMEDY_UI_NO_AUTO_BUILD"] == "1"


def test_scrub_child_env_drops_a_key_the_source_never_defined():
    """An allowlisted but undefined key is ABSENT, never present and empty."""
    scrubbed = scrub_child_env({"PATH": "/usr/bin"}, ("PATH", "NEVER_SET_ANYWHERE"))

    assert scrubbed == {"PATH": "/usr/bin"}
    assert "NEVER_SET_ANYWHERE" not in scrubbed
