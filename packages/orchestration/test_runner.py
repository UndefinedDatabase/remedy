"""
Permission-gated local test runner v0 — Step 33.

Runs an allowlisted pytest command inside a target repository and returns a
safe, structured TestRunRecord.  Raw process output is saved to a workspace
file but is NEVER included in the returned record, run-log metadata,
Brain/Viewer JSON, Trust Report, or Timeline.

Allowed command forms (exact match required):
  - python3 -m pytest
  - python -m pytest
  - pytest

Command selection:
  1. If the job's Project Constitution defines a test command that exactly
     matches one of the allowed forms, use it.
  2. Else if pyproject.toml exists AND a tests/ directory exists inside the
     target repo, fall back to "python3 -m pytest".
  3. Otherwise block with status="blocked", reason="no_supported_test_command".

Safety constraints:
  - No shell=True.
  - subprocess.run receives an argv list only.
  - cwd is the resolved target_repo path.
  - Environment: inherits os.environ (no extra vars, no .env reading).
  - Timeout: default 60 seconds (configurable via timeout_sec argument).
  - Raw stdout/stderr are written to the workspace test_runs/ subdirectory
    and are not returned in any structured field.

Public API::

    run_tests_local(job, workspace_root, *, data_dir=None, timeout_sec=60)
        -> TestRunRecord
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALLOWED_COMMANDS: tuple[str, ...] = (
    "python3 -m pytest",
    "python -m pytest",
    "pytest",
)

TIMEOUT_DEFAULT_SEC: int = 60


# ---------------------------------------------------------------------------
# Record model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TestRunRecord:
    """Safe, structured result of one local test run.

    Raw stdout/stderr are NOT included.  Only safe scalar metrics are stored.
    """

    __test__ = False  # prevent pytest from collecting this dataclass as a test class

    test_run_id: str
    command: str           # e.g. "python3 -m pytest"
    status: str            # "passed" | "failed" | "blocked" | "timeout"
    exit_code: int | None  # None when blocked or timeout
    duration_ms: int
    output_path: str       # basename of the output file, or "" when blocked
    output_line_count: int
    output_bytes: int
    created_at: str        # ISO-8601 UTC timestamp
    blocked_reason: str    # non-empty only when status == "blocked"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_tests_local(
    job: "Job",
    workspace_root: Path,
    *,
    timeout_sec: int = TIMEOUT_DEFAULT_SEC,
) -> TestRunRecord:
    """Run the allowlisted test command for job's target repo.

    Does NOT check the repo_test_run permission — the caller (CLI) is
    responsible for that gate.

    Args:
        job:            The job whose target_repo will be used.
        workspace_root: Root of the job's workspace
                        (.data/workspaces/<job_id>/).  Test output is
                        written to workspace_root/test_runs/<run_id>.txt.
        timeout_sec:    Subprocess timeout in seconds (default 60).

    Returns:
        A TestRunRecord with safe scalar fields only.  No raw output.
    """
    test_run_id = uuid4().hex[:16]
    created_at = datetime.now(timezone.utc).isoformat()

    # ── Resolve target repo ──────────────────────────────────────────────────
    target_repo_str: str | None = job.metadata.get("target_repo")
    if not target_repo_str:
        return _blocked(test_run_id, created_at, "no_target_repo")
    repo_root = Path(target_repo_str).resolve()
    if not repo_root.is_dir():
        return _blocked(test_run_id, created_at, "target_repo_not_a_directory")

    # ── Determine command ────────────────────────────────────────────────────
    command = _select_command(job, repo_root)
    if command is None:
        return _blocked(test_run_id, created_at, "no_supported_test_command")

    # ── Prepare output file ──────────────────────────────────────────────────
    test_runs_dir = workspace_root / "test_runs"
    test_runs_dir.mkdir(parents=True, exist_ok=True)
    output_file = test_runs_dir / f"{test_run_id}.txt"

    # ── Run subprocess ───────────────────────────────────────────────────────
    assert command in ALLOWED_COMMANDS, f"BUG: command not in allowlist: {command!r}"
    argv = command.split()  # safe: command is from the allowlist only
    start = time.monotonic()
    status: str
    exit_code: int | None = None

    try:
        proc = subprocess.run(
            argv,
            cwd=str(repo_root),
            capture_output=True,
            timeout=timeout_sec,
        )
        duration_ms = int((time.monotonic() - start) * 1000)
        exit_code = proc.returncode
        raw_output = proc.stdout + proc.stderr
        status = "passed" if exit_code == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        duration_ms = int((time.monotonic() - start) * 1000)
        raw_output = (exc.stdout or b"") + (exc.stderr or b"")
        raw_output += b"\n[timeout expired]\n"
        status = "timeout"
        exit_code = None
    except FileNotFoundError:
        # e.g. "pytest" not installed — return blocked with empty output_path
        return _blocked(test_run_id, created_at, "command_not_found")

    # ── Write output file ────────────────────────────────────────────────────
    output_file.write_bytes(raw_output)
    output_bytes = len(raw_output)
    output_line_count = raw_output.count(b"\n")

    return TestRunRecord(
        test_run_id=test_run_id,
        command=command,
        status=status,
        exit_code=exit_code,
        duration_ms=duration_ms,
        output_path=output_file.name,
        output_line_count=output_line_count,
        output_bytes=output_bytes,
        created_at=created_at,
        blocked_reason="",
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _select_command(job: "Job", repo_root: Path) -> str | None:
    """Return the allowed test command string, or None to block."""
    # 1. Constitution test_commands (first allowlisted match wins)
    constitution_cmd = _constitution_test_command(job, repo_root)
    if constitution_cmd is not None:
        return constitution_cmd

    # 2. Auto-detect: pyproject.toml + tests/ both present → python3 -m pytest
    if (repo_root / "pyproject.toml").is_file() and (repo_root / "tests").is_dir():
        return "python3 -m pytest"

    return None


def _constitution_test_command(job: "Job", repo_root: Path) -> str | None:
    """Extract the first allowlisted test command from the Project Constitution.

    Returns None if the constitution is unavailable or has no allowlisted command.
    Never raises.
    """
    try:
        from packages.orchestration.project_constitution import load_project_constitution
        constitution = load_project_constitution(repo_root)
        for cmd in constitution.test_commands:
            stripped = cmd.strip()
            if stripped in ALLOWED_COMMANDS:
                return stripped
    except Exception:
        pass
    return None


def _blocked(test_run_id: str, created_at: str, reason: str) -> TestRunRecord:
    return TestRunRecord(
        test_run_id=test_run_id,
        command="",
        status="blocked",
        exit_code=None,
        duration_ms=0,
        output_path="",
        output_line_count=0,
        output_bytes=0,
        created_at=created_at,
        blocked_reason=reason,
    )
