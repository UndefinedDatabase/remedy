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
from packages.orchestration.planner_models import PlannerOutput


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
      - NOT mutating the job through the provider

    Caller must persist result.job after this call returns.

    Returns PlanJobResult(job, changed=False) if planning was skipped.
    """
    if job.tasks or job.artifacts:
        return PlanJobResult(job=job, changed=False)

    job.state = RunState.RUNNING

    prompt = job.user_prompt or job.name
    output: PlannerOutput = call_planner(prompt)

    job.tasks = [
        Task(
            description=t.description,
            inputs={"task_type": t.task_type},
        )
        for t in output.proposed_tasks
    ]

    content_lines = [
        "LLM Planning Output",
        f"Job:    {job.id}",
        f"Prompt: {prompt}",
        "",
        f"Summary: {output.summary}",
        "",
        "Tasks:",
    ]
    for t in output.proposed_tasks:
        content_lines.append(f"  - {t.task_type}: {t.description}")
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

    # task_id=None: orchestration-owned artifact (see Artifact docstring)
    job.artifacts = [
        Artifact(
            name="planning_output",
            content="\n".join(content_lines),
            mime_type="text/plain",
            task_id=None,
            metadata={
                "planner": "llm",
                "summary": output.summary,
            },
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

    Mutates the artifact in place. No-op if result.changed is False or there
    are no artifacts (e.g. the job was already planned).

    Designed to be called after plan_job_with_llm returns, before persisting.
    """
    if not result.changed or not result.job.artifacts:
        return
    result.job.artifacts[0].metadata.update(
        {
            "provider": provider,
            "role": role,
            "model": model,
            "task_count": len(result.job.tasks),
            "elapsed_ms": round(elapsed_ms),
        }
    )
