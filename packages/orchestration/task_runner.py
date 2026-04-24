"""
Single-task execution orchestration.

Provides run_next_task() which executes exactly one pending task per call
using an injected builder callable, and materialize_task_output() which
writes the builder's proposed changes into a workspace file.

State semantics (Step 7 — verifier gate):
  Job transitions:
    PLANNED  -> RUNNING    when a pending task is found and execution begins
    RUNNING  -> COMPLETED  when the last task is finalized (all tasks COMPLETED)

  Task transitions:
    PENDING  -> RUNNING    at the start of execution
    RUNNING  -> RUNNING    after builder succeeds (task stays RUNNING until verified)
    RUNNING  -> COMPLETED  after finalize_task() is called with a passing VerificationResult
    RUNNING  -> PENDING    on builder failure OR on verification failure

  Verifier gate:
    run_next_task() does NOT mark the task COMPLETED. After builder output is
    produced and materialized, the caller must:
      1. call verify_task_output() from verifier.py (pure check)
      2. call finalize_task() to apply the result (state mutation)
    Only finalize_task() with a passing VerificationResult marks the task COMPLETED.

  Failure behavior:
    Builder failure: task rolls back to PENDING, job.state restored. Exception propagates.
    Verification failure: finalize_task() rolls task back to PENDING, records failure
      details in artifact metadata. No exception — the job remains RUNNING and retryable.

  A partially-executed job (some tasks COMPLETED, some PENDING) remains RUNNING.
  Caller is responsible for persisting the returned job.

Materialization (Step 6 + 6.5):
  materialize_task_output() writes the builder's proposed_changes and summary
  to a structured text file inside the workspace.  The workspace is managed
  by an injected runtime; this module never creates or accesses directories
  directly.

  Hardening (Step 6.5):
  - Section-aware extraction: only "Proposed Changes:" lines are written;
    Notes and Risks are excluded even though they share the "  - " prefix.
  - Collision-safe filenames: <index>_<safe_type>_<short_id>.txt ensures
    every task produces a unique, deterministic filename.
  - Path sanitization: task_type is sanitized before use in file paths to
    prevent traversal and reject unsafe characters.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable
from uuid import UUID

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.verifier import VerificationResult
from packages.orchestration.workspace import LocalWorkspaceRuntime, MaterializedFile


@dataclass
class RunTaskResult:
    """Result of a run_next_task call.

    job:      the (possibly mutated) job after attempting execution.
    task_id:  UUID of the task that was executed, or None if no task was run.
    changed:  True if a task was executed; False if no pending task was found.
    """

    job: Job
    task_id: UUID | None
    changed: bool


def _find_next_pending(job: Job) -> Task | None:
    """Return the first task with status PENDING, or None."""
    for task in job.tasks:
        if task.status == RunState.PENDING:
            return task
    return None


def _build_execution_context(job: Job, task: Task) -> TaskExecutionContext:
    """Build a TaskExecutionContext from the current job and task state.

    Extracts planning_summary from the orchestration-owned planning artifact
    (task_id=None, name="planning_output") and collects summaries from all
    previously completed task artifacts, in task order.
    """
    task_type = task.inputs.get("task_type", "unknown")

    # Find planning summary from the orchestration-owned planning artifact.
    planning_summary: str | None = None
    for artifact in job.artifacts:
        if artifact.task_id is None and artifact.name == "planning_output":
            planning_summary = artifact.metadata.get("summary")
            break

    # Collect summaries from already-completed tasks, preserving task order.
    prior_summaries: list[str] = []
    for t in job.tasks:
        if t.status == RunState.COMPLETED:
            for artifact in job.artifacts:
                if artifact.task_id == t.id:
                    s = artifact.metadata.get("summary")
                    if s:
                        prior_summaries.append(s)
                    break

    return TaskExecutionContext(
        job_id=job.id,
        job_prompt=job.user_prompt,
        task_id=task.id,
        task_type=task_type,
        task_description=task.description,
        planning_summary=planning_summary,
        prior_task_summaries=prior_summaries,
    )


def run_next_task(
    job: Job,
    call_builder: Callable[[TaskExecutionContext], BuilderOutput],
) -> RunTaskResult:
    """Execute the next pending task using the injected builder callable.

    Selects the first PENDING task (by order in job.tasks), builds a
    TaskExecutionContext from the current job state, calls call_builder,
    creates one task-owned Artifact, and appends its id to
    task.output_artifact_ids.

    The task remains RUNNING after this call — it is NOT marked COMPLETED here.
    The caller must run verify_task_output() then finalize_task() to complete
    the task after materialization and verification.

    On provider failure: task is rolled back to PENDING and job.state is
    restored to its pre-call value. The exception propagates to the caller.

    Returns RunTaskResult(job, task_id=None, changed=False) if no PENDING task
    exists (job is already complete, or has no tasks).

    All errors from call_builder propagate to the caller — no retries.
    """
    task = _find_next_pending(job)
    if task is None:
        return RunTaskResult(job=job, task_id=None, changed=False)

    original_job_state = job.state
    job.state = RunState.RUNNING
    task.status = RunState.RUNNING

    context = _build_execution_context(job, task)

    try:
        output: BuilderOutput = call_builder(context)
    except Exception:
        # Roll back to avoid stranding the task/job in RUNNING on failure.
        task.status = RunState.PENDING
        job.state = original_job_state
        raise

    task_type = context.task_type

    content_lines = [
        "Builder Execution Output",
        f"Task:  {task.id}",
        f"Type:  {task_type}",
        f"Desc:  {task.description}",
        "",
        f"Summary: {output.summary}",
        "",
        "Proposed Changes:",
    ]
    for change in output.proposed_changes:
        content_lines.append(f"  - {change}")
    if output.notes:
        content_lines.append("")
        content_lines.append("Notes:")
        for note in output.notes:
            content_lines.append(f"  - {note}")
    if output.risks:
        content_lines.append("")
        content_lines.append("Risks:")
        for risk in output.risks:
            content_lines.append(f"  - {risk}")

    # task_id=task.id: this artifact is task-owned (see Artifact docstring).
    # Metadata uses consistent keys; provider/role/model/elapsed_ms are added
    # later by annotate_task_result() after timing is known.
    artifact = Artifact(
        name=f"task_output_{task_type}",
        content="\n".join(content_lines),
        mime_type="text/plain",
        task_id=task.id,
        metadata={
            "task_type": task_type,
            "summary": output.summary,
        },
    )

    # Task intentionally stays RUNNING here — finalize_task() will mark it
    # COMPLETED only after verify_task_output() passes (Step 7 verifier gate).
    task.output_artifact_ids.append(artifact.id)
    job.artifacts.append(artifact)

    return RunTaskResult(job=job, task_id=task.id, changed=True)


def annotate_task_result(
    result: RunTaskResult,
    *,
    provider: str,
    role: str,
    model: str,
    elapsed_ms: float,
) -> None:
    """Enrich the task execution artifact metadata with provider/role/model/timing info.

    Locates the artifact by matching task_id == result.task_id rather than
    assuming a fixed index position — safe even when planning artifacts precede
    task artifacts in job.artifacts.

    No-op if result.changed is False (no task was executed).

    Raises RuntimeError if result.changed is True but no matching artifact is
    found — this indicates a bug in run_next_task and must not be silently ignored.

    Designed to be called after run_next_task returns, before persisting.
    """
    if not result.changed or result.task_id is None:
        return
    artifact = next(
        (a for a in result.job.artifacts if a.task_id == result.task_id),
        None,
    )
    if artifact is None:
        raise RuntimeError(
            f"annotate_task_result: result.changed=True but no artifact found for "
            f"task_id={result.task_id}. This indicates a bug in run_next_task."
        )
    artifact.metadata.update(
        {
            "provider": provider,
            "role": role,
            "model": model,
            "elapsed_ms": round(elapsed_ms),
        }
    )


def finalize_task(result: RunTaskResult, vr: VerificationResult) -> None:
    """Apply a verification result to finalize task and job state.

    If vr.passed:
      task -> COMPLETED
      job  -> COMPLETED if every task is now COMPLETED

    If not vr.passed:
      task -> PENDING (rolled back from RUNNING, safe to retry)
      failure details recorded in artifact.metadata under 'verification_passed'
      and 'verification_failures'

    No-op if result.changed is False.

    Raises RuntimeError if result.task_id is not found in job.tasks — this
    indicates a bug in run_next_task and must not be silently ignored.

    Designed to be called after verify_task_output() returns, before persisting.
    """
    if not result.changed or result.task_id is None:
        return

    task = next(
        (t for t in result.job.tasks if t.id == result.task_id),
        None,
    )
    if task is None:
        raise RuntimeError(
            f"finalize_task: task_id={result.task_id} not found in job.tasks. "
            "This indicates a bug in run_next_task."
        )

    if vr.passed:
        task.status = RunState.COMPLETED
        if all(t.status == RunState.COMPLETED for t in result.job.tasks):
            result.job.state = RunState.COMPLETED
    else:
        task.status = RunState.PENDING
        # Record failure details in artifact metadata for diagnostics.
        artifact = next(
            (a for a in result.job.artifacts if a.task_id == result.task_id),
            None,
        )
        if artifact is not None:
            artifact.metadata["verification_passed"] = False
            artifact.metadata["verification_failures"] = [
                f"{c.check}: {c.message}" for c in vr.failures
            ]


# Known section headers in the builder artifact content format.
# Used by _extract_proposed_changes to detect section boundaries.
_ARTIFACT_SECTION_HEADERS = frozenset({"Proposed Changes:", "Notes:", "Risks:"})

# Characters allowed in a workspace path component.
_SAFE_PATH_RE = re.compile(r"[^a-zA-Z0-9_-]")
_MAX_PATH_COMPONENT_LENGTH = 48


def _extract_proposed_changes(content: str) -> list[str]:
    """Extract only the Proposed Changes lines from a builder artifact content string.

    Parses the content section-by-section using the known section headers
    ("Proposed Changes:", "Notes:", "Risks:"). Only lines under the
    "Proposed Changes:" header are returned — Notes and Risks lines are
    excluded even though they share the same "  - " prefix format.

    Returns lines with their original "  - " prefix intact.
    """
    changes: list[str] = []
    in_section = False
    for line in content.splitlines():
        if line == "Proposed Changes:":
            in_section = True
        elif line in _ARTIFACT_SECTION_HEADERS:
            in_section = False
        elif in_section and line.startswith("  - "):
            changes.append(line)
    return changes


def _sanitize_path_component(value: str) -> str:
    """Sanitize a string for safe use as a single workspace path component.

    Replaces any character that is not alphanumeric, underscore, or hyphen
    with an underscore. Truncates to _MAX_PATH_COMPONENT_LENGTH characters.
    Strips leading/trailing underscores. Returns "unknown" if the result is
    empty after sanitization.

    This neutralizes path traversal sequences ("../", "/") because "." and "/"
    are both replaced. It does not implement a general path policy — callers
    must still pass the result as a single component, not a path.
    """
    sanitized = _SAFE_PATH_RE.sub("_", value)
    sanitized = sanitized[:_MAX_PATH_COMPONENT_LENGTH].strip("_")
    return sanitized or "unknown"


def materialize_task_output(
    result: RunTaskResult,
    runtime: LocalWorkspaceRuntime,
) -> MaterializedFile | None:
    """Write the builder's proposed changes for the executed task to the workspace.

    Writes a structured text file at:
        <workspace_root>/<job_id>/task_output/<index>_<safe_type>_<short_id>.txt

    where:
        <index>      0-based position of the task in job.tasks, zero-padded to 3 digits
        <safe_type>  task_type with unsafe characters replaced by underscores (max 48 chars)
        <short_id>   first 8 hex characters of the task UUID

    This naming is:
        - collision-safe: index + task UUID fragment make every file unique
        - deterministic: same task always produces the same filename
        - path-safe: sanitized type prevents traversal; no raw user data in paths

    Only lines from the "Proposed Changes:" section of the artifact content are
    written — Notes and Risks lines are not included.

    Materialization ordering:
        annotate_task_result (in-memory) → materialize_task_output (disk write)
        → save_job (persist job JSON). This order ensures the workspace file
        exists before the job JSON records its path. If materialization fails,
        save_job must not be called — the caller is responsible for this.

    No-op (returns None) if result.changed is False.
    """
    if not result.changed or result.task_id is None:
        return None

    artifact = next(
        (a for a in result.job.artifacts if a.task_id == result.task_id),
        None,
    )
    if artifact is None:
        raise RuntimeError(
            f"materialize_task_output: result.changed=True but no artifact found for "
            f"task_id={result.task_id}. This indicates a bug in run_next_task."
        )

    task_type = artifact.metadata.get("task_type", "unknown")
    summary = artifact.metadata.get("summary", "")
    safe_type = _sanitize_path_component(task_type)
    short_id = result.task_id.hex[:8]

    # 0-based index in job.tasks — used for deterministic, collision-safe naming.
    # Raises rather than falling back silently: a missing task_id here is an
    # invariant violation (result.changed=True means a task was executed and
    # must be present in job.tasks).
    task_index = next(
        (i for i, t in enumerate(result.job.tasks) if t.id == result.task_id),
        None,
    )
    if task_index is None:
        raise RuntimeError(
            f"materialize_task_output: task_id={result.task_id} not found in "
            f"job.tasks. This indicates a bug — result.task_id must always "
            "correspond to a task in result.job."
        )

    changes = _extract_proposed_changes(artifact.content)

    lines: list[str] = [
        f"Task Type: {task_type}",
        f"Summary:   {summary}",
        "",
        "Proposed Changes:",
        *changes,
    ]

    file_content = "\n".join(lines) + "\n"
    relative_path = f"task_output/{task_index:03d}_{safe_type}_{short_id}.txt"
    mf = runtime.write(relative_path, file_content)

    # Record the workspace file path in the artifact metadata.
    artifact.metadata["workspace_file"] = str(mf.path)

    return mf
