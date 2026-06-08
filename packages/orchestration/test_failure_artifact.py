"""
Test Failure Artifact v1 — structured failure evidence + fix task creation.

When a test fails after an apply/test phase, Remedy creates a safe structured
failure artifact and a fix task. No raw stdout/stderr in artifacts or events.

Public API::

    build_test_failure_artifact(job, test_result, ...) -> TestFailureArtifact
    persist_failure_artifact(job, failure) -> Artifact
    create_fix_task_from_failure(job, failure) -> Task
    emit_failure_events(data_dir, job_id, failure, fix_task_id) -> None
    export_failure_artifact_json(failure) -> dict
    summarize_failure_artifact(failure) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


# ---------------------------------------------------------------------------
# Failure kinds (Step 941)
# ---------------------------------------------------------------------------

FAILURE_TEST_FAILED = "test_failed"
FAILURE_COMMAND_FAILED = "command_failed"
FAILURE_TIMEOUT = "timeout"
FAILURE_COLLECTION_FAILED = "collection_failed"
FAILURE_ENVIRONMENT_FAILED = "environment_failed"
FAILURE_UNKNOWN = "unknown"

FAILURE_KINDS = (
    FAILURE_TEST_FAILED,
    FAILURE_COMMAND_FAILED,
    FAILURE_TIMEOUT,
    FAILURE_COLLECTION_FAILED,
    FAILURE_ENVIRONMENT_FAILED,
    FAILURE_UNKNOWN,
)


# ---------------------------------------------------------------------------
# Data model (Step 941)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RelatedChangeRef:
    """Reference to a related change (intent, apply, task)."""

    ref_type: str  # "intent", "apply", "task", "artifact"
    ref_id: str
    label: str = ""


@dataclass(frozen=True)
class SuggestedRepairAction:
    """What the user/system should do next to fix the failure."""

    label: str
    command: str
    reason: str


@dataclass
class TestFailureArtifact:
    """Structured evidence of a test failure. No raw output."""

    __test__ = False  # Not a pytest test class

    artifact_id: str = ""
    job_id: str = ""
    task_id: str = ""
    related_intent_id: str = ""
    related_apply_id: str = ""
    related_test_run_id: str = ""
    failing_phase: str = ""  # "test", "build", "apply"
    command_safe: str = ""  # normalized command, no raw shell
    exit_code: int | None = None
    safe_summary: str = ""  # bounded human-readable summary
    output_ref: str = ""  # safe ref to persisted output, or ""
    related_files: list[str] = field(default_factory=list)  # relative paths only
    failure_kind: str = FAILURE_UNKNOWN
    suggested_next_action: SuggestedRepairAction | None = None
    related_changes: list[RelatedChangeRef] = field(default_factory=list)
    created_at: str = ""


@dataclass(frozen=True)
class TestFailureSummary:
    """Minimal summary for embedding in other results."""

    __test__ = False  # Not a pytest test class

    failure_kind: str
    safe_summary: str
    fix_task_id: str = ""
    repair_available: bool = False


# ---------------------------------------------------------------------------
# Build failure artifact from test result (Step 942)
# ---------------------------------------------------------------------------


def build_test_failure_artifact(
    job: Any,
    test_result: Any,
    *,
    related_intent_id: str = "",
    related_apply_id: str = "",
    failing_phase: str = "test",
) -> TestFailureArtifact:
    """Build a TestFailureArtifact from a TestRunRecord or event metadata.

    Args:
        job: Job instance.
        test_result: TestRunRecord dataclass, or dict with event metadata.
        related_intent_id: Patch intent this failure relates to.
        related_apply_id: Apply record this failure relates to.
        failing_phase: Which phase failed (test, build, apply).

    Returns:
        TestFailureArtifact with safe fields only.
    """
    artifact_id = uuid4().hex[:12]
    job_id = str(job.id) if hasattr(job, "id") else ""
    task_id = str(job.tasks[0].id) if hasattr(job, "tasks") and job.tasks else ""

    # Extract from TestRunRecord dataclass
    if hasattr(test_result, "test_run_id"):
        return _build_from_record(
            artifact_id, job_id, task_id,
            test_result,
            related_intent_id=related_intent_id,
            related_apply_id=related_apply_id,
            failing_phase=failing_phase,
        )

    # Extract from event dict
    if isinstance(test_result, dict):
        return _build_from_event(
            artifact_id, job_id, task_id,
            test_result,
            related_intent_id=related_intent_id,
            related_apply_id=related_apply_id,
            failing_phase=failing_phase,
        )

    # Fallback
    return TestFailureArtifact(
        artifact_id=artifact_id,
        job_id=job_id,
        task_id=task_id,
        failing_phase=failing_phase,
        failure_kind=FAILURE_UNKNOWN,
        safe_summary="Test failure detected (no structured result available)",
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _build_from_record(
    artifact_id: str, job_id: str, task_id: str,
    record: Any,
    *,
    related_intent_id: str,
    related_apply_id: str,
    failing_phase: str,
) -> TestFailureArtifact:
    """Build from a TestRunRecord."""
    # Classify failure kind
    status = getattr(record, "status", "unknown")
    kind = _classify_failure_kind(status, getattr(record, "exit_code", None))

    # Build safe summary (bounded)
    cmd = getattr(record, "command", "")
    safe_cmd = _normalize_command(cmd)
    exit_code = getattr(record, "exit_code", None)
    duration = getattr(record, "duration_ms", 0)

    summary_parts = [f"Test {status}"]
    if exit_code is not None:
        summary_parts.append(f"exit {exit_code}")
    if duration:
        summary_parts.append(f"{duration}ms")
    safe_summary = ", ".join(summary_parts)[:200]

    # Output ref (basename only, no absolute path)
    output_path = getattr(record, "output_path", "")
    output_ref = Path(output_path).name if output_path else ""

    # Related changes
    changes: list[RelatedChangeRef] = []
    if related_intent_id:
        changes.append(RelatedChangeRef("intent", related_intent_id, "Related patch intent"))
    if related_apply_id:
        changes.append(RelatedChangeRef("apply", related_apply_id, "Related apply record"))

    return TestFailureArtifact(
        artifact_id=artifact_id,
        job_id=job_id,
        task_id=task_id,
        related_intent_id=related_intent_id,
        related_apply_id=related_apply_id,
        related_test_run_id=getattr(record, "test_run_id", ""),
        failing_phase=failing_phase,
        command_safe=safe_cmd,
        exit_code=exit_code,
        safe_summary=safe_summary,
        output_ref=output_ref,
        related_files=[],
        failure_kind=kind,
        related_changes=changes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _build_from_event(
    artifact_id: str, job_id: str, task_id: str,
    event: dict[str, Any],
    *,
    related_intent_id: str,
    related_apply_id: str,
    failing_phase: str,
) -> TestFailureArtifact:
    """Build from an event metadata dict."""
    status = event.get("status", "unknown")
    exit_code = event.get("exit_code")
    if isinstance(exit_code, str):
        try:
            exit_code = int(exit_code)
        except ValueError:
            exit_code = None

    kind = _classify_failure_kind(status, exit_code)
    cmd = event.get("command", "")
    safe_cmd = _normalize_command(cmd)

    summary = f"Test {status}"
    if exit_code is not None:
        summary += f", exit {exit_code}"
    safe_summary = summary[:200]

    output_ref = event.get("output_ref", "")
    if "/" in output_ref:
        output_ref = Path(output_ref).name

    changes: list[RelatedChangeRef] = []
    if related_intent_id:
        changes.append(RelatedChangeRef("intent", related_intent_id))
    if related_apply_id:
        changes.append(RelatedChangeRef("apply", related_apply_id))

    return TestFailureArtifact(
        artifact_id=artifact_id,
        job_id=job_id,
        task_id=task_id,
        related_intent_id=related_intent_id,
        related_apply_id=related_apply_id,
        related_test_run_id=event.get("test_run_id", ""),
        failing_phase=failing_phase,
        command_safe=safe_cmd,
        exit_code=exit_code,
        safe_summary=safe_summary,
        output_ref=output_ref,
        failure_kind=kind,
        related_changes=changes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _classify_failure_kind(status: str, exit_code: int | None) -> str:
    if status == "timeout":
        return FAILURE_TIMEOUT
    if status == "blocked":
        return FAILURE_ENVIRONMENT_FAILED
    if status == "failed":
        if exit_code == 2:
            return FAILURE_COLLECTION_FAILED
        if exit_code == 5:
            return FAILURE_COLLECTION_FAILED  # pytest: no tests collected
        return FAILURE_TEST_FAILED
    if status == "passed":
        return FAILURE_UNKNOWN  # shouldn't build failure for passing test
    return FAILURE_UNKNOWN


def _normalize_command(cmd: str) -> str:
    """Normalize command string — no raw shell, bounded."""
    if not cmd:
        return ""
    # Strip leading paths, keep command name + args
    safe = cmd.strip()[:200]
    # Remove any env vars that look like secrets
    parts = safe.split()
    filtered = [p for p in parts if "=" not in p or not any(
        s in p.upper() for s in ("KEY", "SECRET", "TOKEN", "PASS")
    )]
    return " ".join(filtered)[:200]


# ---------------------------------------------------------------------------
# Persist failure artifact in Job (Step 943)
# ---------------------------------------------------------------------------


def persist_failure_artifact(job: Any, failure: TestFailureArtifact) -> Any:
    """Create a Job Artifact from a TestFailureArtifact and attach to job.

    Returns the created Artifact.
    """
    from packages.core.models import Artifact, ArtifactKind

    safe_content = failure.safe_summary[:500]

    artifact = Artifact(
        name=f"test-failure-{failure.artifact_id}",
        content=safe_content,
        kind=ArtifactKind.VERIFICATION,
        task_id=UUID(failure.task_id) if failure.task_id else None,
        metadata={
            "test_failure": True,
            "failure_kind": failure.failure_kind,
            "artifact_id": failure.artifact_id,
            "related_test_run_id": failure.related_test_run_id,
            "related_intent_id": failure.related_intent_id,
            "related_apply_id": failure.related_apply_id,
            "related_task_id": failure.task_id,
            "failing_phase": failure.failing_phase,
            "command_safe": failure.command_safe,
            "exit_code": failure.exit_code,
            "output_ref": failure.output_ref,
            "related_files": failure.related_files[:20],
            "safe_summary": failure.safe_summary[:500],
        },
    )
    job.artifacts.append(artifact)
    failure.artifact_id = str(artifact.id)

    from packages.orchestration.storage import save_job
    save_job(job)
    return artifact


# ---------------------------------------------------------------------------
# Failure events (Step 944)
# ---------------------------------------------------------------------------


def emit_failure_events(
    data_dir: Path, job_id: UUID | str,
    failure: TestFailureArtifact,
    fix_task_id: str = "",
) -> None:
    """Emit safe failure + repair events. No raw output."""
    from packages.orchestration.timeline import append_run_event

    jid = UUID(str(job_id)) if not isinstance(job_id, UUID) else job_id

    append_run_event(data_dir, jid, event="test_failure_artifact_created", metadata={
        "artifact_id": failure.artifact_id,
        "job_id": failure.job_id,
        "task_id": failure.task_id,
        "failure_kind": failure.failure_kind,
        "related_intent_id": failure.related_intent_id,
        "safe_summary": failure.safe_summary[:200],
    })

    if fix_task_id:
        append_run_event(data_dir, jid, event="repair_task_created", metadata={
            "fix_task_id": fix_task_id,
            "failure_artifact_id": failure.artifact_id,
            "job_id": failure.job_id,
        })


# ---------------------------------------------------------------------------
# Fix task creation (Step 945)
# ---------------------------------------------------------------------------


def create_fix_task_from_failure(
    job: Any, failure: TestFailureArtifact,
) -> Any:
    """Create a fix Task from a failure artifact and attach to job.

    Returns the created Task.
    """
    from packages.core.models import Task

    description = f"Fix failing tests after {failure.failing_phase}"
    if failure.failure_kind != FAILURE_UNKNOWN:
        description += f" ({failure.failure_kind})"

    task = Task(
        description=description[:200],
        inputs={
            "failure_artifact_id": failure.artifact_id,
            "original_task_id": failure.task_id,
            "failure_kind": failure.failure_kind,
            "safe_summary": failure.safe_summary[:200],
        },
    )
    job.tasks.append(task)

    from packages.orchestration.storage import save_job
    save_job(job)
    return task


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_failure_artifact_json(failure: TestFailureArtifact) -> dict[str, Any]:
    """Export a TestFailureArtifact as safe JSON dict."""
    out: dict[str, Any] = {
        "artifact_id": failure.artifact_id,
        "job_id": failure.job_id,
        "task_id": failure.task_id,
        "related_intent_id": failure.related_intent_id,
        "related_apply_id": failure.related_apply_id,
        "related_test_run_id": failure.related_test_run_id,
        "failing_phase": failure.failing_phase,
        "command_safe": failure.command_safe,
        "exit_code": failure.exit_code,
        "safe_summary": failure.safe_summary,
        "output_ref": failure.output_ref,
        "related_files": failure.related_files,
        "failure_kind": failure.failure_kind,
        "created_at": failure.created_at,
        "related_changes": [
            {"ref_type": r.ref_type, "ref_id": r.ref_id, "label": r.label}
            for r in failure.related_changes
        ],
    }
    if failure.suggested_next_action:
        out["suggested_next_action"] = {
            "label": failure.suggested_next_action.label,
            "command": failure.suggested_next_action.command,
            "reason": failure.suggested_next_action.reason,
        }
    return out


def summarize_failure_artifact(failure: TestFailureArtifact) -> str:
    """Human-readable failure summary."""
    lines = [
        f"Test Failure: {failure.failure_kind}",
        f"  Phase: {failure.failing_phase}",
        f"  Summary: {failure.safe_summary}",
    ]
    if failure.command_safe:
        lines.append(f"  Command: {failure.command_safe}")
    if failure.exit_code is not None:
        lines.append(f"  Exit code: {failure.exit_code}")
    if failure.output_ref:
        lines.append(f"  Output: {failure.output_ref}")
    if failure.related_intent_id:
        lines.append(f"  Intent: {failure.related_intent_id}")
    return "\n".join(lines)
