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

import os
import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.ci_stages import CiStage, pytest_argv_for_stage

#: Exit code `scripts/remedy_pytest_runner.py` returns when it kills a timeout.
PYTEST_TIMEOUT_EXIT_CODE = 124

#: The env var `scripts/remedy_pytest_runner.py` reads its budget from.
PYTEST_TIMEOUT_ENV_VAR = "REMEDY_PYTEST_TIMEOUT_SEC"

#: The runner every stage goes through, relative to the repository root.
PYTEST_RUNNER_SCRIPT = "scripts/remedy_pytest_runner.py"


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


def _run_via_subprocess(command: list[str], cwd: Path, timeout_sec: int) -> int:
    """Run `command` ANCHORED at `cwd` and BUDGETED at `timeout_sec` seconds.

    A stage selects by MARKER and carries no path, and this repository sets no
    `testpaths`, so pytest collects from the working directory — without this
    anchor the caller's cwd decides what a stage means (finding R-0456).

    The budget travels as an environment variable because that is the runner's
    only input for it, and it is set on THIS call rather than left to the ambient
    environment: the runner's own default is 600 s, and `standard` was killed at
    it three times out of three (`.agent/f083_inventory.md` `## Q10`) while
    needing 935.14 s at its slowest uncapped sample (`## Q11`). Budgeting per
    stage leaves every OTHER caller of the runner on the 600-second default,
    which raising that default would not.
    """
    env = {**os.environ, PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)}
    return subprocess.run(command, check=False, cwd=cwd, env=env).returncode


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
