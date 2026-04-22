"""
LLM-backed job planning orchestration.

Provides plan_job_with_llm() which runs the planning step when a real
LLM planner provider is available.

The provider is injected as a callable — this module never imports provider
code. Orchestration owns all state transitions, transformation, and idempotency.
"""

from __future__ import annotations

from typing import Callable

from packages.core.models import Artifact, Job, RunState, Task
from packages.orchestration.job_runner import PlanJobResult
from packages.orchestration.planner_models import PlannerOutput, ProposedTask


def _deduplicate_task_types(proposed_tasks: list[ProposedTask]) -> list[Task]:
    """Convert ProposedTask list to Task list with unique task_type values.

    If two proposed tasks share the same task_type, the second and subsequent
    occurrences are suffixed with _2, _3, etc. This prevents downstream
    consumers from confusing semantically different tasks that a planner
    accidentally gave the same type label.

    Example: [write_tests, write_tests] -> [write_tests, write_tests_2]
    """
    seen: dict[str, int] = {}
    tasks: list[Task] = []
    for t in proposed_tasks:
        tt = t.task_type
        if tt in seen:
            seen[tt] += 1
            tt = f"{t.task_type}_{seen[tt]}"
        else:
            seen[tt] = 1
        tasks.append(Task(description=t.description, inputs={"task_type": tt}))
    return tasks


def plan_job_with_llm(
    job: Job,
    call_planner: Callable[[str], PlannerOutput],
) -> PlanJobResult:
    """Plan a job using an injected LLM planner callable.

    call_planner receives the job prompt string and must return a validated
    PlannerOutput. All errors from the provider propagate to the caller.

    Orchestration is responsible for:
      - idempotency (no-op if job already has tasks or artifacts)
      - state transitions: PENDING -> RUNNING -> PLANNED
      - transforming PlannerOutput into Job.tasks and a planning Artifact
      - deduplicating task_type values to avoid ambiguous downstream execution
      - NOT mutating the job through the provider

    Caller must persist result.job after this call returns.

    Returns PlanJobResult(job, changed=False) if planning was skipped.
    """
    if job.tasks or job.artifacts:
        return PlanJobResult(job=job, changed=False)

    job.state = RunState.RUNNING

    prompt = job.user_prompt or job.name
    output: PlannerOutput = call_planner(prompt)

    job.tasks = _deduplicate_task_types(output.proposed_tasks)

    content_lines = [
        "LLM Planning Output",
        f"Job:    {job.id}",
        f"Prompt: {prompt}",
        "",
        f"Summary: {output.summary}",
        "",
        "Tasks:",
    ]
    for task in job.tasks:
        content_lines.append(f"  - {task.inputs['task_type']}: {task.description}")
    if output.acceptance_checks:
        content_lines.append("")
        content_lines.append("Acceptance Checks:")
        for c in output.acceptance_checks:
            content_lines.append(f"  - {c}")
    if output.notes:
        content_lines.append("")
        content_lines.append("Notes:")
        for n in output.notes:
            content_lines.append(f"  - {n}")

    # task_id=None: orchestration-owned artifact (see Artifact docstring).
    # Metadata uses consistent keys; provider/role/model/elapsed_ms/task_count
    # are added later by annotate_planning_result() after timing is known.
    job.artifacts = [
        Artifact(
            name="planning_output",
            content="\n".join(content_lines),
            mime_type="text/plain",
            task_id=None,
            metadata={"summary": output.summary},
        )
    ]

    job.state = RunState.PLANNED
    return PlanJobResult(job=job, changed=True)


def annotate_planning_result(
    result: PlanJobResult,
    *,
    provider: str,
    role: str,
    model: str,
    elapsed_ms: float,
) -> None:
    """Enrich the planning artifact metadata with provider/role/model/timing info.

    Locates the artifact by name ("planning_output") and task_id (None) rather
    than blindly using index 0 — safe if artifacts are reordered or accumulated.

    No-op if result.changed is False (job was already planned; nothing to annotate).

    Raises RuntimeError if result.changed is True but no planning artifact is found —
    this indicates a bug in plan_job_with_llm and must not be silently ignored.
    Mirrors the strict behavior of annotate_task_result.

    Designed to be called after plan_job_with_llm returns, before persisting.
    """
    if not result.changed:
        return
    artifact = next(
        (
            a
            for a in result.job.artifacts
            if a.name == "planning_output" and a.task_id is None
        ),
        None,
    )
    if artifact is None:
        raise RuntimeError(
            "annotate_planning_result: result.changed=True but no planning_output "
            "artifact found. This indicates a bug in plan_job_with_llm."
        )
    artifact.metadata.update(
        {
            "provider": provider,
            "role": role,
            "model": model,
            "task_count": len(result.job.tasks),
            "elapsed_ms": round(elapsed_ms),
        }
    )
