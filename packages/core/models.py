"""
Core domain models for Remedy.

These are plain data containers — no business logic, no provider-specific fields.
All models are Pydantic BaseModel for validation and serialization.
"""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Budget(BaseModel):
    """Resource budget for a job or task."""

    max_tokens: int | None = None
    max_cost_usd: float | None = None
    max_steps: int | None = None


class AcceptanceCheck(BaseModel):
    """Criteria that must pass before an artifact or task is accepted."""

    description: str
    required: bool = True


class Artifact(BaseModel):
    """A discrete unit of output produced during a workflow."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    content: str
    mime_type: str = "text/plain"
    metadata: dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """A single unit of work within a job."""

    id: UUID = Field(default_factory=uuid4)
    description: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    acceptance_checks: list[AcceptanceCheck] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)


class RunState(str, Enum):
    """Lifecycle state of a running job."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Job(BaseModel):
    """Top-level orchestration unit composed of tasks."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    tasks: list[Task] = Field(default_factory=list)
    state: RunState = RunState.PENDING
    artifacts: list[Artifact] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    metadata: dict[str, Any] = Field(default_factory=dict)
