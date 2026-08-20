"""Running Remedy's own CI stages — one stage in, one honest verdict out.

The stage TABLE lives in :mod:`packages.orchestration.ci_stages`; this module
runs it. The split is deliberate: importing the table must never be able to
start a test run.

EVERY STAGE GOES THROUGH `scripts/remedy_pytest_runner.py`, AS A SUBPROCESS —
that script owns the process-group isolation, the 512 KiB output caps, the
`REMEDY_PYTEST_TIMEOUT_SEC` budget and exit code 124 for a timeout, and shelling
out to bare `pytest` would lose all four. It is invoked rather than imported
because `scripts/` carries no `__init__.py`, which is how
`tests/cli/test_pytest_runner.py` reaches it too.

Remedy deliberately does NOT retry a failing stage — a flaky test is quarantined
only by an explicit marker change in a reviewed diff (T2_F083: "retries hide
rot"). The command runner is INJECTED so a test can prove the wiring without
spawning pytest; the default really does spawn it. Rendering the summary belongs
with the command that prints it and is not here.
"""
from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.ci_stages import CiStage, pytest_argv_for_stage
from packages.orchestration.exec_guard import run_guarded_test_command

#: Exit code `scripts/remedy_pytest_runner.py` returns when it kills a timeout.
PYTEST_TIMEOUT_EXIT_CODE = 124

#: The env var `scripts/remedy_pytest_runner.py` reads its budget from.
PYTEST_TIMEOUT_ENV_VAR = "REMEDY_PYTEST_TIMEOUT_SEC"

#: The runner every stage goes through, relative to the repository root.
PYTEST_RUNNER_SCRIPT = "scripts/remedy_pytest_runner.py"

#: Seconds the guard's wall sits ABOVE a stage's own budget (DECISION F085 D4, which
#: rules WHY the wall is a backstop and is not restated here).
#:
#: The number is chosen against the runner's own teardown, which its code BOUNDS rather
#: than estimates: after the budget expires `scripts/remedy_pytest_runner.py` sends
#: SIGTERM and waits 5 s, sends SIGKILL and waits 5 s, then `_ensure_pg_dead` repeats
#: that pair with 1 s waits — at most about 12 s before it returns 124. A pytest child
#: that dies on the first SIGTERM took 0.05 s in three of three samples measured at
#: f3e9687a under a 3-second budget. 60 s clears the derived bound five times over.
PYTEST_WALL_GRACE_SEC = 60


@dataclass(frozen=True)
class StageResult:
    """What one stage did: whether it ran, how it ended, how long it took."""

    stage: str
    ran: bool
    exit_code: int | None
    duration_s: float
    note: str


def stage_command(stage: CiStage, repo_root: Path) -> list[str]:
    """The exact argv that runs `stage`. Builds it; runs nothing."""
    return [
        sys.executable,
        str(repo_root / PYTEST_RUNNER_SCRIPT),
        "--",
        *pytest_argv_for_stage(stage),
    ]


def _reemit(stdout: bytes | None, stderr: bytes | None) -> None:
    """Write a finished stage's captured streams back to this process's own."""
    if stdout:
        sys.stdout.buffer.write(stdout)
        sys.stdout.buffer.flush()
    if stderr:
        sys.stderr.buffer.write(stderr)
        sys.stderr.buffer.flush()


def _run_via_subprocess(
    command: list[str],
    cwd: Path,
    timeout_sec: int,
    *,
    wall_grace_sec: float = PYTEST_WALL_GRACE_SEC,
) -> int:
    """Run `command` ANCHORED at `cwd` and BUDGETED at `timeout_sec` seconds.

    Goes through the stage-1 guard; DECISION F085 D4 rules the three deltas that
    creates and the alternatives rejected for each. The budget still travels as an
    environment variable, the runner's only input for it, and is set on THIS call
    rather than left ambient — the runner defaults to 600 s and `standard` was killed
    at it three times of three (`.agent/f083_inventory.md` `## Q10`) while needing
    935.14 s uncapped (`## Q11`). It travels through `extra_env` because the guard
    SCRUBS the child environment to an allowlist, so a copy of `os.environ` no longer
    reaches the child. The guard also CAPTURES both streams, which is what makes its
    output cap enforceable, so they are re-emitted before returning; what is LOST is
    live streaming, and a long stage now looks silent while it runs. A wall trip
    returns `PYTEST_TIMEOUT_EXIT_CODE`, the same 124 the runner returns when it kills
    its own child, so `run_ci_stage` writes the same `timed out` note either way.

    The cwd anchor is unchanged and still load-bearing: a stage selects by MARKER and
    carries no path, and this repository sets no `testpaths`, so without it the
    caller's cwd decides what a stage means (finding R-0456).
    """
    try:
        completed = run_guarded_test_command(
            command,
            timeout_sec=timeout_sec + wall_grace_sec,
            cwd=str(cwd),
            extra_env={PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)},
        )
    except subprocess.TimeoutExpired as expired:
        _reemit(expired.stdout, expired.stderr)
        return PYTEST_TIMEOUT_EXIT_CODE
    _reemit(completed.stdout, completed.stderr)
    return completed.returncode


def run_ci_stage(
    stage: CiStage,
    repo_root: Path,
    *,
    run_command: Callable[[list[str], Path, int], int] = _run_via_subprocess,
    monotonic: Callable[[], float] = time.monotonic,
) -> StageResult:
    """Run one stage, or record why it was not run. Never raises on a red stage."""
    if not stage.runs_in_ci:
        return StageResult(
            stage=stage.name,
            ran=False,
            exit_code=None,
            duration_s=0.0,
            note=f"not run by CI — run it manually with: {stage.manual_command}",
        )
    started = monotonic()
    exit_code = run_command(stage_command(stage, repo_root), repo_root, stage.timeout_sec)
    elapsed = monotonic() - started
    note = "timed out" if exit_code == PYTEST_TIMEOUT_EXIT_CODE else ""
    return StageResult(
        stage=stage.name,
        ran=True,
        exit_code=exit_code,
        duration_s=elapsed,
        note=note,
    )


def ci_exit_code(results: tuple[StageResult, ...]) -> int:
    """0 only when a stage actually RAN and every stage that ran ended green.

    A run in which NOTHING ran is red: `all()` over the empty selection is True,
    so the plain reading reports an invocation that executed no test — every
    stage skipped, or no stage at all — as a passing CI (finding R-0457).
    """
    ran = [result for result in results if result.ran]
    return 0 if ran and all(result.exit_code == 0 for result in ran) else 1
