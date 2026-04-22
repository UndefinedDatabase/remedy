"""
Builder models: execution context and output.

These models live in orchestration/ (not in providers/) because orchestration
imports and transforms them — providers depend on these, not the other way around.
"""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class TaskExecutionContext(BaseModel):
    """Context provided to a builder provider for a single task execution.

    Contains all information the builder needs to produce meaningful output.
    Built by run_next_task() from the current job and task state — the provider
    receives this object and must not mutate the Job directly.

    job_id:               UUID of the job containing the task.
    job_prompt:           User prompt from the job (may be None).
    task_id:              UUID of the task to execute.
    task_type:            snake_case type identifier for the task.
    task_description:     Human-readable description of what the task should accomplish.
    planning_summary:     Summary from the planning artifact, if available.
    prior_task_summaries: Summaries from already-completed task artifacts, in order.
    """

    job_id: UUID
    job_prompt: str | None
    task_id: UUID
    task_type: str
    task_description: str
    planning_summary: str | None = None
    prior_task_summaries: list[str] = []


class BuilderOutput(BaseModel):
    """Structured execution result returned by a builder provider.

    summary:          short overview of what was done or planned for this task.
    proposed_changes: list of concrete changes or actions taken/proposed.
    notes:            optional assumptions, observations, or clarifications.
    risks:            optional list of potential issues or concerns.
    """

    summary: str
    proposed_changes: list[str] = Field(min_length=1)
    notes: list[str] = []
    risks: list[str] = []
