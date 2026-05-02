"""
Core domain models for Remedy.

These are plain data containers — no business logic, no provider-specific fields.
All models are Pydantic BaseModel for validation and serialization.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class Budget(BaseModel):
    """Resource budget for a job or task."""

    max_tokens: int | None = None
    max_cost_usd: float | None = None
    max_steps: int | None = None


class AcceptanceCheck(BaseModel):
    """Criteria that must pass before an artifact or task is accepted."""

    description: str
    required: bool = True


class RunState(str, Enum):
    """Lifecycle state of a job or task."""

    PENDING = "pending"
    PLANNED = "planned"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ArtifactKind(str, Enum):
    """Semantic category of an Artifact.

    Provides a stable, machine-readable signal about what role an artifact
    plays in the workflow — complementing the free-form name and metadata
    fields.

    v1 active (set at creation sites in job_runner, llm_planner, task_runner):
      PLANNING, BUILDER_PROPOSAL

    v1 reserved (defined for future steps; not yet emitted as standalone artifacts):
      WORKSPACE_MATERIALIZATION, VERIFICATION, PATCH_INTENT, REPO_APPLICATION

    UNKNOWN:
        Default / not-yet-classified.  Old artifacts loaded from JSON without
        a 'kind' field will deserialize to UNKNOWN (Pydantic default).
    PLANNING:
        Artifact produced by a planning step (deterministic or LLM planner).
        task_id is typically None (orchestration-owned).
    BUILDER_PROPOSAL:
        Artifact produced by a builder/task execution step.
        task_id points to the owning Task.
    WORKSPACE_MATERIALIZATION:
        Artifact representing a file written to the local workspace.
    VERIFICATION:
        Artifact produced by a verification step.
    PATCH_INTENT:
        Artifact produced by patch-intent derivation (patch_intent.py).
    REPO_APPLICATION:
        Artifact produced by repo-application (repo_applicator.py).
    """

    UNKNOWN = "unknown"
    PLANNING = "planning"
    BUILDER_PROPOSAL = "builder_proposal"
    WORKSPACE_MATERIALIZATION = "workspace_materialization"
    VERIFICATION = "verification"
    PATCH_INTENT = "patch_intent"
    REPO_APPLICATION = "repo_application"


class Artifact(BaseModel):
    """A discrete unit of output produced during a workflow.

    Note: content is text-only (str). Binary artifact support is a known
    limitation deferred to a later step.

    task_id convention:
      task_id = UUID  — artifact produced by that specific Task.
      task_id = None  — artifact produced by orchestration/system logic
                        (e.g. planning output, metadata). Not tied to a Task.

    kind:
      Semantic category — set at creation sites for all new artifacts.
      Defaults to ArtifactKind.UNKNOWN for backward-compatibility with
      persisted JSON that predates Step 14.
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    content: str
    mime_type: str = "text/plain"
    task_id: UUID | None = None
    kind: ArtifactKind = ArtifactKind.UNKNOWN
    metadata: dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """A single unit of work within a job."""

    id: UUID = Field(default_factory=uuid4)
    description: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    acceptance_checks: list[AcceptanceCheck] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    status: RunState = RunState.PENDING
    output_artifact_ids: list[UUID] = Field(default_factory=list)


class Job(BaseModel):
    """Top-level orchestration unit composed of tasks."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    user_prompt: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    tasks: list[Task] = Field(default_factory=list)
    state: RunState = RunState.PENDING
    artifacts: list[Artifact] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    metadata: dict[str, Any] = Field(default_factory=dict)
