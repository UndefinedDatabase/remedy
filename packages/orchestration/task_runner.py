"""
Single-task execution orchestration.

Provides run_next_task() which executes exactly one pending task per call
using an injected builder callable, and materialize_task_output() which
writes the builder's proposed changes into a workspace file.

State semantics:
  Job transitions:
    PLANNED  -> RUNNING    when a pending task is found and execution begins
    RUNNING  -> COMPLETED  when the last task completes (all tasks COMPLETED)

  Task transitions:
    PENDING  -> RUNNING    at the start of execution
    RUNNING  -> COMPLETED  on successful execution
    RUNNING  -> PENDING    on builder failure (rolled back to avoid stranded state)

  Failure behavior:
    If the builder callable raises, the task is rolled back to PENDING and
    job.state is restored to its value before this call. The exception
    propagates to the caller with no retry. This keeps the job in a
    consistent, re-executable state.

  A partially-executed job (some tasks COMPLETED, some PENDING) remains RUNNING.
  Caller is responsible for persisting the returned job.

Materialization (Step 6):
  materialize_task_output() writes the builder's proposed_changes and summary
  to a structured text file inside the workspace.  The workspace is managed
  by an injected runtime; this module never creates or accesses directories
  directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from uuid import UUID

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
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
    creates one task-owned Artifact, marks the task COMPLETED, and appends
    its id to task.output_artifact_ids.

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

    task.status = RunState.COMPLETED
    task.output_artifact_ids.append(artifact.id)
    job.artifacts.append(artifact)

    # Advance job state: COMPLETED only when every task is done.
    if all(t.status == RunState.COMPLETED for t in job.tasks):
        job.state = RunState.COMPLETED

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


def materialize_task_output(
    result: RunTaskResult,
    runtime: LocalWorkspaceRuntime,
) -> MaterializedFile | None:
    """Write the builder's proposed changes for the executed task to the workspace.

    Writes a structured text file at:
        <workspace_root>/<job_id>/task_output/<task_type>.txt

    The file contains the task summary and all proposed_changes lines.

    No-op (returns None) if result.changed is False.

    The file content mirrors the artifact stored in the job so that downstream
    tools can read it from the filesystem without loading the full job JSON.

    Returns the MaterializedFile describing what was written, or None if
    result.changed is False.
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

    lines: list[str] = [
        f"Task Type: {task_type}",
        f"Summary:   {summary}",
        "",
        "Proposed Changes:",
    ]
    # Re-derive proposed_changes from the artifact content (lines starting with "  - ")
    for line in artifact.content.splitlines():
        if line.startswith("  - "):
            lines.append(line)

    file_content = "\n".join(lines) + "\n"
    relative_path = f"task_output/{task_type}.txt"
    mf = runtime.write(relative_path, file_content)

    # Record the workspace file path in the artifact metadata.
    artifact.metadata["workspace_file"] = str(mf.path)

    return mf
