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

#: Exit code `scripts/remedy_pytest_runner.py` returns when it kills a timeout.
PYTEST_TIMEOUT_EXIT_CODE = 124

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


def _run_via_subprocess(command: list[str]) -> int:
    return subprocess.run(command, check=False).returncode


def run_ci_stage(
    stage: CiStage,
    repo_root: Path,
    *,
    run_command: Callable[[list[str]], int] = _run_via_subprocess,
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
    exit_code = run_command(stage_command(stage, repo_root))
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
    """0 only when every stage that RAN ended green. A skipped stage is not a pass."""
    return 0 if all(r.exit_code == 0 for r in results if r.ran) else 1
