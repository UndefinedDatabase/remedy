"""Runaway fixtures for `packages/orchestration/exec_guard.py` — F085 stage 1, T001.

Each fixture is a real child process, so every test here carries the
`subprocess` marker registered in `pyproject.toml`. Limits are kept deliberately
small: the point is that the guard trips, not how long it takes to trip.

These tests exercise the guard DIRECTLY, so a green run here says the mechanism
works and says nothing about which of Remedy's own subprocesses are spawned
through it. That migration state lives in one place on purpose — the PARTIAL
COVERAGE note in `exec_guard`'s own module docstring — and the caller grep is the
honest answer. No count is repeated here, because a count in a second file is a
second thing to forget.
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
import time

import pytest

# `test_command_exec_policy` is called through this module handle on purpose: bound
# as a bare name here it would match pytest's `test_*` collection pattern and error
# on fixtures it never had.
from packages.orchestration import exec_guard
from packages.orchestration.exec_guard import (
    TEST_COMMAND_ENV_ALLOWLIST,
    ExecGuardPolicy,
    _StreamPump,
    plan_child_spawn,
    run_guarded,
    run_guarded_test_command,
    scrub_child_env,
)

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
    """RLIMIT_CPU with a grace band gives SIGXCPU, which is attributable.

    The deadline below is a BACKSTOP and NOT the property under test (R-0513): it
    sits thirty times above the CPU limit so it never fires on the healthy path,
    and it exists so that a regression which stops the rlimit reaching the child
    ends as a named `wall_timeout` failure instead of an unbounded hang that leaves
    the busy loop orphaned. `tripped_limit == "cpu_seconds"` below is therefore also
    the proof that the backstop never steals the attribution.
    """
    result = run_guarded(
        _child("x = 0\nwhile True:\n    x += 1\n"),
        ExecGuardPolicy(cpu_seconds=1, wall_timeout_seconds=30.0, output_cap_bytes=64 * 1024),
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


def test_stream_pump_snapshot_reports_nothing_before_the_pump_has_read():
    """A pump that never ran holds no bytes, has seen none and dropped none.

    The zero state matters because `run_guarded` now reads EVERY stream field
    through `snapshot()`, including on the path where a pump is still blocked and
    has produced nothing at all.
    """
    pump = _StreamPump(io.BytesIO(b"never read, because run() is never called"), None)

    assert pump.snapshot() == (b"", 0, False)


@pytest.mark.subprocess
def test_a_pump_blocked_by_an_escapee_still_returns_the_bytes_it_already_read():
    """The drain deadline costs the REST of a stream, never the part already read.

    Same escapee shape as
    `test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group` — the
    grandchild holds the inherited pipe write end past the deadline — but the child
    writes and flushes a known line FIRST. That line must come back even though the
    pump never reaches EOF, and `streams_complete` must still report the stream as
    incomplete.
    """
    escapee = (
        "import subprocess, sys, time\n"
        "sys.stdout.write('line-written-before-the-escapee\\n')\n"
        "sys.stdout.flush()\n"
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)', sys.argv[1]],\n"
        "                 start_new_session=True)\n"
        "time.sleep(120)\n"
    )
    result = run_guarded(
        _child(escapee),
        ExecGuardPolicy(wall_timeout_seconds=1.0, stream_drain_grace_seconds=2.0, output_cap_bytes=64 * 1024),
    )

    assert result.tripped_limit == "wall_timeout"
    assert result.streams_complete is False
    assert b"line-written-before-the-escapee" in result.stdout

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


# ---------------------------------------------------------------------------
# plan_child_spawn — the CHILD half a streaming supervisor can take on its own
# ---------------------------------------------------------------------------

def test_plan_child_spawn_names_rlimits_only_and_no_parent_side_limit():
    """`limits_enforced` is the rlimit half; the deadline and the cap are the parent's.

    The policy below asks for a wall timeout and an output cap on purpose: a plan
    that named them would be claiming enforcement it cannot perform, since nothing
    in a `preexec_fn` bounds either.
    """
    plan = plan_child_spawn(
        ExecGuardPolicy(core_file_bytes=0, wall_timeout_seconds=10.0, output_cap_bytes=64 * 1024)
    )

    assert "core_file_bytes" in plan.limits_enforced
    assert "wall_timeout" not in plan.limits_enforced
    assert "output_bytes" not in plan.limits_enforced
    assert plan.limits_unsupported == ()


def test_plan_child_spawn_scrubs_exactly_like_scrub_child_env():
    """With an allowlist the plan's env IS `scrub_child_env` of the same inputs."""
    env = {"PATH": "/usr/bin", "REMEDY_KEPT": "yes", "ANTHROPIC_API_KEY": "sk-nope"}
    allowlist = ("PATH", "REMEDY_KEPT", "ANTHROPIC_API_KEY")

    plan = plan_child_spawn(ExecGuardPolicy(env=env, env_allowlist=allowlist))

    assert plan.env == scrub_child_env(env, allowlist)


def test_plan_child_spawn_hands_the_environment_over_unchanged_without_an_allowlist():
    """No allowlist means no scrub — and `None` stays `None`, which means "inherit"."""
    env = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "sk-unscrubbed-by-design"}

    assert plan_child_spawn(ExecGuardPolicy(env=env)).env == env
    assert plan_child_spawn(ExecGuardPolicy(env=None)).env is None


@pytest.mark.subprocess
def test_plan_child_spawn_preexec_really_lowers_the_core_limit_in_the_child():
    """Proved in a REAL child, never by calling `preexec_fn` in the test process.

    Calling it here would lower this interpreter's own RLIMIT_CORE for the rest of
    the session and would prove only that the function runs, not that a spawn under
    the plan obeys it. The guarded run reads the limit back out of the child.
    """
    plan = plan_child_spawn(ExecGuardPolicy(core_file_bytes=0))
    assert callable(plan.preexec_fn)

    result = run_guarded(
        _child("import resource\nprint(resource.getrlimit(resource.RLIMIT_CORE))\n"),
        ExecGuardPolicy(core_file_bytes=0, wall_timeout_seconds=10.0, output_cap_bytes=64 * 1024),
    )

    assert result.returncode == 0
    assert result.stdout.strip() == b"(0, 0)"


# ---------------------------------------------------------------------------
# The shared `test`-class seam (T002b) — the policy, the allowlist and the runner
# ---------------------------------------------------------------------------


def test_the_ui_no_auto_build_variable_is_a_member_of_the_test_allowlist():
    """R-0202, pinned as a membership: dropping this key re-creates the bug."""
    assert "REMEDY_UI_NO_AUTO_BUILD" in TEST_COMMAND_ENV_ALLOWLIST


def test_the_test_policy_sets_only_the_limits_it_can_defend():
    """The three unmeasured rlimits stay None; the cap stays above the caller's own.

    `MAX_TEST_OUTPUT_BYTES` is imported HERE rather than in `exec_guard`, so the two
    values move together while the dependency keeps running one way only.
    """
    from packages.orchestration.test_runner import MAX_TEST_OUTPUT_BYTES

    policy = exec_guard.test_command_exec_policy(60, "/tmp")

    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None
    assert policy.core_file_bytes == 0
    assert policy.output_cap_bytes > MAX_TEST_OUTPUT_BYTES


@pytest.mark.subprocess
def test_the_seam_hands_a_child_the_allowlist_and_neither_secret(monkeypatch):
    """A real child, spawned through the runner itself, dumps what it inherited.

    Spawned through `run_guarded_test_command` and not through `scrub_child_env`
    alone, because the property under test is what the SEAM gives a child.
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-never-appear")
    monkeypatch.setenv("MY_PROJECT_SECRET", "should-never-appear-either")
    monkeypatch.setenv("REMEDY_UI_NO_AUTO_BUILD", "1")

    result = run_guarded_test_command(_child(_ENV_DUMP), timeout_sec=30, cwd=None)
    dumped = _dumped(result)

    assert result.returncode == 0
    assert dumped["REMEDY_UI_NO_AUTO_BUILD"] == "1"
    assert "PATH" in dumped
    assert "ANTHROPIC_API_KEY" not in dumped
    assert "MY_PROJECT_SECRET" not in dumped
    assert b"sk-should-never-appear" not in result.stdout
    assert b"should-never-appear-either" not in result.stdout


@pytest.mark.subprocess
def test_extra_env_keys_widens_the_allowlist_for_that_call_only(monkeypatch):
    """The per-project override knob: named it arrives, unnamed it does not."""
    monkeypatch.setenv("MY_PROJECT_TOOLCHAIN", "yes")

    named = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env_keys=("MY_PROJECT_TOOLCHAIN",),
    )
    unnamed = run_guarded_test_command(_child(_ENV_DUMP), timeout_sec=30, cwd=None)

    assert _dumped(named)["MY_PROJECT_TOOLCHAIN"] == "yes"
    assert "MY_PROJECT_TOOLCHAIN" not in _dumped(unnamed)


@pytest.mark.subprocess
def test_a_wall_trip_raises_timeout_expired_carrying_the_partial_output():
    """The partial-stream promise, proven: the line printed before the trip survives."""
    argv = _child(
        "import sys, time\n"
        "sys.stdout.write('printed-before-the-timeout\\n')\n"
        "sys.stdout.flush()\n"
        "time.sleep(120)\n"
    )

    with pytest.raises(subprocess.TimeoutExpired) as excinfo:
        run_guarded_test_command(argv, timeout_sec=2, cwd=None)

    assert b"printed-before-the-timeout" in excinfo.value.output


@pytest.mark.subprocess
def test_a_nonzero_exit_comes_back_as_a_completed_process():
    """The `subprocess.run` shape a migrated call site keeps reading."""
    result = run_guarded_test_command(
        _child("import sys\nsys.stdout.write('ran\\n')\nsys.exit(3)\n"),
        timeout_sec=30,
        cwd=None,
    )

    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 3
    assert b"ran" in result.stdout


@pytest.mark.subprocess
def test_extra_env_sets_a_value_the_parent_does_not_have(monkeypatch):
    """The SET knob, which `extra_env_keys` cannot provide.

    `extra_env_keys` names keys to pass THROUGH, so a key the parent lacks arrives
    absent. The remaining `test`-class sites SET a value instead, which is why the
    two knobs are separate rather than one.
    """
    monkeypatch.delenv("REMEDY_PROBE_BUDGET", raising=False)

    passed_through = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env_keys=("REMEDY_PROBE_BUDGET",),
    )
    set_by_overlay = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env={"REMEDY_PROBE_BUDGET": "4242"},
    )

    assert "REMEDY_PROBE_BUDGET" not in _dumped(passed_through)
    assert _dumped(set_by_overlay)["REMEDY_PROBE_BUDGET"] == "4242"


@pytest.mark.subprocess
def test_extra_env_cannot_smuggle_a_forbidden_key_past_the_floor():
    """`FORBIDDEN_ENV_KEYS` is the guard's floor and not a caller's to lower."""
    result = run_guarded_test_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None,
        extra_env={"ANTHROPIC_API_KEY": "sk-should-never-appear"},
    )

    assert "ANTHROPIC_API_KEY" not in _dumped(result)
    assert b"sk-should-never-appear" not in result.stdout


def test_extra_env_adds_to_the_allowlisted_environment_rather_than_replacing_it(monkeypatch):
    """The overlay ADDS; what the allowlist already carries still reaches the child."""
    monkeypatch.setenv("REMEDY_UI_NO_AUTO_BUILD", "1")

    policy = exec_guard.test_command_exec_policy(
        60, None, extra_env={"REMEDY_PROBE_BUDGET": "7"}
    )
    child_env = exec_guard.plan_child_spawn(policy).env

    assert child_env["REMEDY_PROBE_BUDGET"] == "7"
    assert child_env["REMEDY_UI_NO_AUTO_BUILD"] == "1"
    assert "PATH" in child_env


def test_the_dod_process_policy_keeps_the_wall_timeout_its_class_is_defined_by():
    """The one column separating `dod-process` from `dod-app` in T2_F085's table.

    Everything is reached through the `exec_guard` module handle, for the reason
    the import block states: a bare name here would meet pytest's collection
    pattern or drift from the module's own spelling. The allowlist is asserted by
    IDENTITY rather than by re-listing its members, so widening the shared set
    cannot silently make this test the second place to edit.
    """
    policy = exec_guard.dod_process_exec_policy(45, "/tmp/dod-cwd")
    assert policy.wall_timeout_seconds == 45.0
    assert policy.cwd == "/tmp/dod-cwd"
    assert policy.core_file_bytes == 0
    assert policy.output_cap_bytes == exec_guard.DOD_PROCESS_OUTPUT_CAP_BYTES
    assert policy.env is None
    assert policy.env_allowlist == exec_guard.DOD_PROCESS_ENV_ALLOWLIST
    assert not exec_guard.FORBIDDEN_ENV_KEYS & set(policy.env_allowlist)
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None


def test_the_dod_app_policy_takes_neither_a_wall_timeout_nor_an_output_cap():
    """The two columns separating `dod-app` from every bounded class in T2_F085.

    Both are PARENT-side, and this policy's caller takes the CHILD half alone, so
    None here is the row the table rules rather than an omission. The declared
    keys are asserted to JOIN the allowlist rather than replace it, and
    `FORBIDDEN_ENV_KEYS` is asserted to survive a caller that names one.
    """
    policy = exec_guard.dod_app_exec_policy(
        cwd="/tmp/dod-app-cwd",
        env={"PATH": "/usr/bin", "PORT": "5173", "AWS_SECRET_ACCESS_KEY": "leak"},
        declared_env_keys=("PORT", "AWS_SECRET_ACCESS_KEY"),
    )

    assert policy.wall_timeout_seconds is None
    assert policy.output_cap_bytes is None
    assert policy.cwd == "/tmp/dod-app-cwd"
    assert policy.core_file_bytes == 0
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None
    assert set(exec_guard.DOD_APP_ENV_ALLOWLIST) <= set(policy.env_allowlist)
    assert "PORT" in policy.env_allowlist

    child_env = exec_guard.plan_child_spawn(policy).env
    assert child_env["PORT"] == "5173"
    assert child_env["PATH"] == "/usr/bin"
    assert "AWS_SECRET_ACCESS_KEY" not in child_env


def test_the_runtime_build_policy_keeps_the_wall_timeout_its_class_is_defined_by():
    policy = exec_guard.runtime_build_exec_policy(90.0, "/tmp")
    assert policy.wall_timeout_seconds == 90.0
    assert policy.output_cap_bytes == exec_guard.RUNTIME_BUILD_OUTPUT_CAP_BYTES
    assert policy.cwd == "/tmp"
    assert policy.core_file_bytes == 0
    assert policy.env is None
    assert policy.env_allowlist == exec_guard.RUNTIME_BUILD_ENV_ALLOWLIST
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None


@pytest.mark.subprocess
def test_the_runtime_build_seam_hands_a_child_the_allowlist_and_not_the_secret(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-never-appear")
    monkeypatch.setenv("MY_PROJECT_SECRET", "should-never-appear-either")
    completed = exec_guard.run_guarded_runtime_build_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None)
    dumped = _dumped(completed)
    assert completed.returncode == 0
    assert "PATH" in dumped
    assert "ANTHROPIC_API_KEY" not in dumped
    assert "MY_PROJECT_SECRET" not in dumped


@pytest.mark.subprocess
def test_the_runtime_build_seam_raises_called_process_error_only_when_check_is_asked():
    cmd = _child("raise SystemExit(3)")
    completed = exec_guard.run_guarded_runtime_build_command(cmd, timeout_sec=30, cwd=None)
    assert completed.returncode == 3
    with pytest.raises(subprocess.CalledProcessError) as caught:
        exec_guard.run_guarded_runtime_build_command(
            cmd, timeout_sec=30, cwd=None, check=True)
    assert caught.value.returncode == 3
    assert caught.value.cmd == cmd


@pytest.mark.subprocess
def test_the_runtime_build_seam_raises_timeout_expired_on_a_wall_trip():
    with pytest.raises(subprocess.TimeoutExpired) as caught:
        exec_guard.run_guarded_runtime_build_command(
            _child("import time; print('before', flush=True); time.sleep(30)"),
            timeout_sec=1.0, cwd=None, check=True)
    assert b"before" in (caught.value.output or b"")

#: The npm and node CONFIGURATION keys the `runtime-build` row adds to the `test` base.
#: Listed here so the two tests below read the same set and a widening edits one place.
_RUNTIME_BUILD_ADDED_ENV_KEYS = frozenset({
    "NODE_ENV", "NODE_EXTRA_CA_CERTS", "NODE_OPTIONS", "NODE_PATH",
    "NPM_CONFIG_CACHE", "NPM_CONFIG_PREFIX", "NPM_CONFIG_REGISTRY",
    "NPM_CONFIG_USERCONFIG",
})


def test_the_runtime_build_row_adds_the_npm_configuration_to_the_test_base():
    """The widened row, asserted as base-plus-additions rather than as a re-listing.

    The `test` set is asserted to SURVIVE as a subset, so a later widening of the
    shared base cannot silently drop out of this class, and `FORBIDDEN_ENV_KEYS` is
    asserted disjoint so the floor holds however the row grows.
    """
    allowlist = set(exec_guard.RUNTIME_BUILD_ENV_ALLOWLIST)
    assert set(TEST_COMMAND_ENV_ALLOWLIST) <= allowlist
    assert _RUNTIME_BUILD_ADDED_ENV_KEYS <= allowlist
    assert not exec_guard.FORBIDDEN_ENV_KEYS & allowlist


@pytest.mark.subprocess
def test_the_runtime_build_row_passes_npm_config_by_name_and_never_by_prefix(monkeypatch):
    """A named `NPM_CONFIG_*` key reaches the child; a credential in that namespace does not.

    This is the property that makes the widening safe to ship: `scrub_child_env` matches
    a whole key, so `NPM_CONFIG__AUTHTOKEN` is unlisted rather than merely unmentioned.
    `HTTPS_PROXY` is asserted absent for the other reason — it is a `FORBIDDEN_ENV_KEYS`
    member, so the floor drops it even though a build behind a proxy would want it.
    """
    monkeypatch.setenv("NPM_CONFIG_REGISTRY", "https://registry.example.invalid")
    monkeypatch.setenv("NPM_CONFIG__AUTHTOKEN", "npm-token-should-never-appear")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example.invalid:8080")

    completed = exec_guard.run_guarded_runtime_build_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None)

    dumped = _dumped(completed)
    assert completed.returncode == 0
    assert dumped["NPM_CONFIG_REGISTRY"] == "https://registry.example.invalid"
    assert "NPM_CONFIG__AUTHTOKEN" not in dumped
    assert "HTTPS_PROXY" not in dumped
