"""
Permission-gated local test runner v1 — Step 34.

Runs a discovered test command inside a target repository and returns a
safe, structured TestRunRecord.  Raw process output is saved to a workspace
file but is NEVER included in the returned record, run-log metadata,
Brain/Viewer JSON, Trust Report, or Timeline.

Command selection (via command_discovery.py):
  1. Run all detectors against the target repo.
  2. Select the best test candidate: high confidence > medium, explicit
     source (constitution, pyproject, cargo, go) > heuristic (makefile etc.).
  3. If no qualifying candidate exists, block with "no_test_command_discovered".

Execution safety guard:
  _EXECUTION_SAFE_EXECUTABLES is the closed list of executables we are
  willing to invoke.  It is NOT the project-logic allowlist (that lives in
  command_discovery.py).  It exists purely to prevent a future refactor or
  misconfiguration from accidentally running an arbitrary executable.
  This list must NOT grow ad-hoc; add only after explicit security review.

Safety constraints:
  - No shell=True.
  - subprocess.run receives an argv list only (from CommandCandidate.argv_list()).
  - cwd is the resolved target_repo path.
  - Environment: inherits os.environ (no extra vars, no .env reading).
  - Timeout: default 60 seconds (configurable via timeout_sec argument).
  - Raw stdout/stderr are written to the workspace test_runs/ subdirectory
    and are not returned in any structured field.

Public API::

    run_tests_local(job, workspace_root, *, timeout_sec=60) -> TestRunRecord
"""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TIMEOUT_DEFAULT_SEC: int = 60

# Execution safety guard — NOT project logic.
# This is the closed set of executables we are willing to invoke.
# Project command discovery lives in command_discovery.py and may return
# candidates with any argv; this guard is the final hard check before exec.
# Do not expand this list without a security review.
_EXECUTION_SAFE_EXECUTABLES: frozenset[str] = frozenset({
    # Python
    "python3", "python", "pytest",
    # Build scripts
    "make",
    # Rust
    "cargo",
    # Go
    "go",
    # JavaScript
    "npm", "npx", "pnpm", "yarn", "bun",
    # Task runners
    "just", "task",
    # JVM
    "gradle", "gradlew", "mvn", "mvnw",
    # .NET
    "dotnet",
    # Ruby
    "rake",
    # PHP
    "composer",
    # Python build tools
    "poetry", "uv", "hatch",
})


# ---------------------------------------------------------------------------
# Record model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TestRunRecord:
    """Safe, structured result of one local test run.

    Raw stdout/stderr are NOT included.  Only safe scalar metrics and
    provenance metadata are stored.
    """

    __test__ = False  # prevent pytest from collecting this dataclass as a test class

    test_run_id: str
    command: str                   # e.g. "python3 -m pytest"
    status: str                    # "passed" | "failed" | "blocked" | "timeout"
    exit_code: int | None          # None when blocked or timeout
    duration_ms: int
    output_path: str               # basename of the output file, or "" when blocked
    output_line_count: int
    output_bytes: int
    created_at: str                # ISO-8601 UTC timestamp
    blocked_reason: str            # non-empty only when status == "blocked"
    # Command provenance (Step 34) — empty strings when blocked before discovery.
    command_source_type: str       # e.g. "pyproject", "makefile", "cargo"
    command_source_path: str       # relative path to source file
    command_purpose: str           # "test" | "build" | "lint" | ...
    command_confidence: str        # "high" | "medium" | "low"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_tests_local(
    job: "Job",
    workspace_root: Path,
    *,
    timeout_sec: int = TIMEOUT_DEFAULT_SEC,
) -> TestRunRecord:
    """Run the best discovered test command for job's target repo.

    Does NOT check the repo_test_run permission — the caller (CLI) is
    responsible for that gate.

    Args:
        job:            The job whose target_repo will be used.
        workspace_root: Root of the job's workspace
                        (.data/workspaces/<job_id>/).  Test output is
                        written to workspace_root/test_runs/<run_id>.txt.
        timeout_sec:    Subprocess timeout in seconds (default 60).

    Returns:
        A TestRunRecord with safe scalar fields and provenance only.
        No raw output.
    """
    from datetime import datetime, timezone
    from uuid import uuid4

    test_run_id = uuid4().hex[:16]
    created_at = datetime.now(timezone.utc).isoformat()

    # ── Resolve target repo ──────────────────────────────────────────────────
    target_repo_str: str | None = job.metadata.get("target_repo")
    if not target_repo_str:
        return _blocked(test_run_id, created_at, "no_target_repo")
    repo_root = Path(target_repo_str).resolve()
    if not repo_root.is_dir():
        return _blocked(test_run_id, created_at, "target_repo_not_a_directory")

    # ── Discover and select test command ─────────────────────────────────────
    from packages.orchestration.command_discovery import (
        CommandCandidate,
        discover_commands,
        select_best_test_candidate,
    )

    candidates = discover_commands(job, repo_root)
    candidate: CommandCandidate | None = select_best_test_candidate(candidates)

    if candidate is None:
        return _blocked(test_run_id, created_at, "no_test_command_discovered")

    # ── Execution safety guard ───────────────────────────────────────────────
    # Validates the candidate's argv before any subprocess call.
    # This guard is independent of project discovery logic.
    if candidate.argv[0] not in _EXECUTION_SAFE_EXECUTABLES:
        raise RuntimeError(
            f"BUG: executable not in safe list: {candidate.argv[0]!r}"
        )
    if candidate.risk == "high":
        raise RuntimeError(
            f"BUG: high-risk candidate must not be executed: {candidate.display!r}"
        )

    # ── Prepare output file ──────────────────────────────────────────────────
    test_runs_dir = workspace_root / "test_runs"
    test_runs_dir.mkdir(parents=True, exist_ok=True)
    output_file = test_runs_dir / f"{test_run_id}.txt"

    # ── Run subprocess ───────────────────────────────────────────────────────
    argv = candidate.argv_list()
    command = candidate.display
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
        return _blocked(
            test_run_id, created_at, "command_not_found",
            source_type=candidate.source_type,
            source_path=candidate.source_path,
            purpose=candidate.purpose,
            confidence=candidate.confidence,
        )

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
        command_source_type=candidate.source_type,
        command_source_path=candidate.source_path,
        command_purpose=candidate.purpose,
        command_confidence=candidate.confidence,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _blocked(
    test_run_id: str,
    created_at: str,
    reason: str,
    *,
    source_type: str = "",
    source_path: str = "",
    purpose: str = "",
    confidence: str = "",
) -> TestRunRecord:
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
        command_source_type=source_type,
        command_source_path=source_path,
        command_purpose=purpose,
        command_confidence=confidence,
    )
