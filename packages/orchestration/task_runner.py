"""
Single-task execution orchestration.

Provides run_next_task() which executes exactly one pending task per call
using an injected builder callable.

State semantics:
  Job transitions:
    PLANNED  -> RUNNING    when a pending task is found and execution begins
    RUNNING  -> COMPLETED  when the last task completes (all tasks COMPLETED)

  Task transitions:
    PENDING  -> RUNNING    during execution
    RUNNING  -> COMPLETED  on successful execution

  A partially-executed job (some tasks COMPLETED, some PENDING) remains RUNNING.
  No state change to PLANNED or FAILED is made here — errors propagate to caller.

  Caller is responsible for persisting the returned job.

Pre-execution note (Step 5):
  This step does NOT perform filesystem edits, command execution, or patch
  application. The builder callable returns structured output describing
  proposed changes; actual code modification is deferred to a later step.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from uuid import UUID

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.builder_models import BuilderOutput


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


def run_next_task(
    job: Job,
    call_builder: Callable[[str], BuilderOutput],
) -> RunTaskResult:
    """Execute the next pending task using the injected builder callable.

    Selects the first PENDING task (by order in job.tasks), calls call_builder
    with the task description, creates one task-owned Artifact, marks the task
    COMPLETED, and appends its id to task.output_artifact_ids.

    Returns RunTaskResult(job, task_id=None, changed=False) if no PENDING task
    exists (job is already complete, or has no tasks).

    All errors from call_builder propagate to the caller — no retries.
    """
    task = _find_next_pending(job)
    if task is None:
        return RunTaskResult(job=job, task_id=None, changed=False)

    job.state = RunState.RUNNING
    task.status = RunState.RUNNING

    output: BuilderOutput = call_builder(task.description)

    task_type = task.inputs.get("task_type", "unknown")

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

    # task_id=task.id: this artifact is task-owned (see Artifact docstring)
    artifact = Artifact(
        name=f"task_output_{task_type}",
        content="\n".join(content_lines),
        mime_type="text/plain",
        task_id=task.id,
        metadata={
            "builder": "llm",
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
    assuming a fixed index position. No-op if result.changed is False or the
    artifact cannot be found (e.g. no-op run with no task executed).

    Designed to be called after run_next_task returns, before persisting.
    """
    if not result.changed or result.task_id is None:
        return
    artifact = next(
        (a for a in result.job.artifacts if a.task_id == result.task_id),
        None,
    )
    if artifact is None:
        return
    artifact.metadata.update(
        {
            "provider": provider,
            "role": role,
            "model": model,
            "elapsed_ms": round(elapsed_ms),
        }
    )
