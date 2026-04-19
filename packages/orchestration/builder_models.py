"""
Builder output models.

These represent structured execution results returned by any builder provider.
They live in orchestration/ (not in providers/) because orchestration code
imports and transforms them — providers depend on these, not the other way around.
"""

from __future__ import annotations

from pydantic import BaseModel


class BuilderOutput(BaseModel):
    """Structured execution result returned by a builder provider.

    summary:          short overview of what was done or planned for this task.
    proposed_changes: list of concrete changes or actions taken/proposed.
    notes:            optional assumptions, observations, or clarifications.
    risks:            optional list of potential issues or concerns.
    """

    summary: str
    proposed_changes: list[str]
    notes: list[str] = []
    risks: list[str] = []
