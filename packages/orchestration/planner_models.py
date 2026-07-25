"""
Planner output models.

These represent structured planning results returned by any planner provider.
They live in orchestration/ (not in providers/) because orchestration code
imports and transforms them — providers depend on these, not the other way around.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# Deprecated by F014: superseded by PlannedTask. Retained for --no-llm/fallback.
class ProposedTask(BaseModel):
    """A task proposed by the planner."""

    task_type: str
    description: str


# Deprecated by F014: superseded by FlightPlan. Retained for --no-llm/fallback.
class PlannerOutput(BaseModel):
    """Structured planning result returned by a planner provider."""

    summary: str
    proposed_tasks: list[ProposedTask] = Field(min_length=1)
    acceptance_checks: list[str] = []
    notes: list[str] = []
