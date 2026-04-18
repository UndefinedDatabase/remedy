"""
Job orchestration runner.

Provides the first minimal job-processing step: plan_job.

This module is free of LLM calls, external dependencies, and async logic.
Planning is deterministic and local — it shapes the job for future execution.
Caller is responsible for persisting the returned job.
"""

from __future__ import annotations

from dataclasses import dataclass

from packages.core.models import Artifact, Job, RunState, Task

# Fixed planning task templates — order is intentional.
_PLANNING_TASK_SPECS: list[tuple[str, str]] = [
    (
        "analyze_requirements",
        "Analyze the job requirements and user prompt.",
    ),
    (
        "define_acceptance_checks",
        "Define acceptance criteria for the job outcome.",
    ),
    (
        "prepare_implementation_plan",
        "Outline a step-by-step implementation plan.",
    ),
]


@dataclass
class PlanJobResult:
    """Result of a plan_job call.

    job:     the (possibly mutated) job after planning.
    changed: True if planning work was performed; False if already planned.
    """

    job: Job
    changed: bool


def plan_job(job: Job) -> PlanJobResult:
    """Generate an initial planning skeleton for the given job.

    Adds 3 standard planning Tasks and 1 orchestration-owned planning Artifact.
    Returns PlanJobResult(job, changed=False) unchanged if the job already has
    tasks or artifacts (idempotent).

    State transitions:
      PENDING -> RUNNING (during planning) -> PLANNED (tasks ready)

    No I/O is performed. Caller must persist result.job.
    """
    if job.tasks or job.artifacts:
        return PlanJobResult(job=job, changed=False)

    job.state = RunState.RUNNING

    job.tasks = [
        Task(description=description, inputs={"task_type": name})
        for name, description in _PLANNING_TASK_SPECS
    ]

    prompt_summary = job.user_prompt or job.name
    task_lines = "\n".join(
        f"  - {name}: {description}"
        for name, description in _PLANNING_TASK_SPECS
    )
    # task_id=None: this artifact is produced by orchestration logic, not a Task.
    job.artifacts = [
        Artifact(
            name="planning_output",
            content=(
                f"Initial planning output\n"
                f"Job:    {job.id}\n"
                f"Prompt: {prompt_summary}\n\n"
                f"Tasks generated:\n{task_lines}\n\n"
                f"Note: deterministic planning skeleton — no LLM involved."
            ),
            mime_type="text/plain",
            task_id=None,
            metadata={"planner": "local_deterministic", "step": "3"},
        )
    ]

    # Planning complete; tasks are ready and the job is waiting for execution.
    job.state = RunState.PLANNED

    return PlanJobResult(job=job, changed=True)
