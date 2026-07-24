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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator


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


class JobBudgets(BaseModel):
    """Closed type for per-job budget limits (F018 T001).

    All fields are optional. Absent means no limit.
    StrictInt rejects bool, float, and string coercion.
    extra="forbid" rejects unknown fields.
    """

    model_config = ConfigDict(extra="forbid")

    max_total_tokens: StrictInt | None = None
    max_provider_calls: StrictInt | None = None
    max_wall_clock_minutes: StrictInt | None = None
    deadline: datetime | None = None

    @model_validator(mode="after")
    def _validate_budget_fields(self) -> JobBudgets:
        for name in ("max_total_tokens", "max_provider_calls", "max_wall_clock_minutes"):
            val = getattr(self, name)
            if val is not None:
                if val <= 0:
                    raise ValueError(f"JobBudgets.{name} must be strictly positive, got {val}")
                if not (-2**53 < val < 2**53):
                    raise ValueError(f"JobBudgets.{name} is not finite")
        if self.deadline is not None:
            if not isinstance(self.deadline, datetime):
                raise ValueError(
                    f"JobBudgets.deadline must be a datetime, "
                    f"got {type(self.deadline).__name__}"
                )
            if self.deadline.tzinfo is None:
                raise ValueError(
                    "JobBudgets.deadline must be timezone-aware (UTC)"
                )
            object.__setattr__(
                self, "deadline",
                self.deadline.astimezone(timezone.utc),
            )
        return self


class JobFences(BaseModel):
    """Closed type for per-job scope fences (F017 T003).

    Both fields are optional lists of glob strings. An empty list means
    no restriction (allow) or no additional denies (deny).
    Malformed input fails closed via Pydantic validation — no str() coercion.
    extra="forbid" rejects unknown fields.
    """

    model_config = ConfigDict(extra="forbid")

    allow: list[str] = Field(default_factory=list)
    deny: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_glob_entries(self) -> JobFences:
        for field_name in ("allow", "deny"):
            raw = getattr(self, field_name)
            cleaned: list[str] = []
            for i, item in enumerate(raw):
                if not isinstance(item, str):
                    raise ValueError(
                        f"JobFences.{field_name}[{i}] must be a string, "
                        f"got {type(item).__name__}"
                    )
                trimmed = item.strip()
                if not trimmed:
                    raise ValueError(
                        f"JobFences.{field_name}[{i}] is empty or "
                        f"whitespace-only after trimming"
                    )
                cleaned.append(trimmed)
            object.__setattr__(self, field_name, cleaned)
        return self


class Job(BaseModel):
    """Top-level orchestration unit composed of tasks."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    mission: str | None = None
    user_prompt: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    tasks: list[Task] = Field(default_factory=list)
    state: RunState = RunState.PENDING
    artifacts: list[Artifact] = Field(default_factory=list)
    budget: Budget = Field(default_factory=Budget)
    metadata: dict[str, Any] = Field(default_factory=dict)
    project_id: str | None = None
    fences: JobFences | None = None
    budgets: JobBudgets | None = None
