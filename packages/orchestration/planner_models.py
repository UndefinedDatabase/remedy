"""
Planner output models.

These represent structured planning results returned by any planner provider.
They live in orchestration/ (not in providers/) because orchestration code
imports and transforms them — providers depend on these, not the other way around.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProposedTask(BaseModel):
    """A task proposed by the planner."""

    task_type: str
    description: str


class PlannerOutput(BaseModel):
    """Structured planning result returned by a planner provider.

    summary:           short overview of the overall plan.
    proposed_tasks:    ordered list of tasks to execute.
    acceptance_checks: optional job-level criteria for a successful outcome.
    notes:             optional assumptions or caveats from the planner.
    """

    summary: str
    proposed_tasks: list[ProposedTask] = Field(min_length=1)
    acceptance_checks: list[str] = []
    notes: list[str] = []
