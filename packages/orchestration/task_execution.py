"""
Task Execution Port — modular interface for executing Job Tasks.

Defines TaskExecutionRequest/Result and a provider-neutral execution contract.
Provider-specific logic lives in adapter modules, not here.

Public API::

    TaskExecutionRequest
    TaskExecutionResult
    FixtureTaskExecutor
    execute_task(request, executor) -> TaskExecutionResult
    can_retry_task(job_id, task_id, root) -> dict
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol
from uuid import uuid4


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TaskExecutionRequest:
    job_id: str
    task_id: str
    task_description: str
    task_inputs: dict[str, Any] = field(default_factory=dict)
    provider: str = "fixture"
    mode: str = "one_shot"
    repo_path: str = ""
    max_steps: int = 1
    max_runtime_seconds: int = 60
    max_tokens: int = 0


@dataclass
class TaskExecutionResult:
    task_id: str
    provider: str = ""
    work_performed: bool = False
    status: str = "no_work"
    outcome: str = ""
    artifact_ids: list[str] = field(default_factory=list)
    patch_intent_id: str = ""
    approval_required: bool = False
    tests_run: int = 0
    tests_passed: int = 0
    blocked_reason: str = ""
    safe_summary: str = ""
    token_count: int = 0
    duration_ms: int = 0
    started_at: str = ""
    completed_at: str = ""


class TaskExecutor(Protocol):
    def execute(self, request: TaskExecutionRequest) -> TaskExecutionResult: ...


class FixtureTaskExecutor:
    """Deterministic executor for testing. Does not call any LLM or external service."""

    def execute(self, request: TaskExecutionRequest) -> TaskExecutionResult:
        start = _utcnow_iso()
        task_type = request.task_inputs.get("task_type", "unknown")
        source = request.task_inputs.get("source", "unknown")

        if task_type == "blocked_fixture":
            return TaskExecutionResult(
                task_id=request.task_id,
                provider="fixture",
                work_performed=False,
                status="blocked",
                outcome="blocked_by_fixture",
                blocked_reason="fixture_blocked_task_type",
                safe_summary=f"Fixture: blocked task type '{task_type}'",
                started_at=start,
                completed_at=_utcnow_iso(),
            )

        artifact_id = uuid4().hex[:12]
        return TaskExecutionResult(
            task_id=request.task_id,
            provider="fixture",
            work_performed=True,
            status="completed",
            outcome="fixture_completed",
            artifact_ids=[artifact_id],
            safe_summary=f"Fixture completed: {request.task_description[:60]}",
            token_count=0,
            duration_ms=1,
            started_at=start,
            completed_at=_utcnow_iso(),
        )


class NoneExecutor:
    """No-op executor — returns no_work/blocked."""

    def execute(self, request: TaskExecutionRequest) -> TaskExecutionResult:
        return TaskExecutionResult(
            task_id=request.task_id,
            provider="none",
            work_performed=False,
            status="blocked",
            outcome="no_worker_selected",
            blocked_reason="no_worker_selected",
            safe_summary="No worker provider selected.",
        )


# ---------------------------------------------------------------------------
# Provider adapter selection
# ---------------------------------------------------------------------------

_EXECUTORS: dict[str, type] = {
    "fixture": FixtureTaskExecutor,
    "none": NoneExecutor,
}

ALLOWED_PROVIDERS = frozenset(_EXECUTORS.keys() | {"ollama"})


def get_executor(provider: str) -> TaskExecutor | None:
    cls = _EXECUTORS.get(provider)
    if cls:
        return cls()
    if provider == "ollama":
        return None
    return None


def execute_task(request: TaskExecutionRequest) -> TaskExecutionResult:
    """Execute a task using the provider specified in the request."""
    executor = get_executor(request.provider)
    if executor is None:
        return TaskExecutionResult(
            task_id=request.task_id,
            provider=request.provider,
            work_performed=False,
            status="blocked",
            outcome="provider_unavailable",
            blocked_reason=f"Provider '{request.provider}' unavailable",
            safe_summary=f"Provider '{request.provider}' is not available.",
        )
    return executor.execute(request)


# ---------------------------------------------------------------------------
# Budget gate
# ---------------------------------------------------------------------------

@dataclass
class BudgetGate:
    max_steps: int = 0
    max_tokens: int = 0
    max_runtime_seconds: int = 0
    steps_used: int = 0
    tokens_used: int = 0

    @property
    def has_budget(self) -> bool:
        return self.max_steps > 0

    def can_execute(self) -> tuple[bool, str]:
        if self.max_steps <= 0:
            return (False, "no_budget_set")
        if self.steps_used >= self.max_steps:
            return (False, "max_steps_exhausted")
        return (True, "ok")

    def record_step(self, tokens: int = 0) -> None:
        self.steps_used += 1
        self.tokens_used += tokens


# ---------------------------------------------------------------------------
# Retry boundary
# ---------------------------------------------------------------------------

def can_retry_task(job_id: str, task_id: str, root: Path | None = None) -> dict[str, Any]:
    """Read-only retry readiness check. Does NOT execute anything."""
    from packages.orchestration.storage import load_job_safe
    from packages.orchestration.proposed_tasks import reconcile_materialized
    from uuid import UUID

    blockers: list[str] = []

    job, job_degraded = load_job_safe(UUID(job_id), root)
    if job_degraded:
        return {"ready": False, "blockers": ["job_store_degraded"], "reason": "corrupt job store"}
    if job is None:
        return {"ready": False, "blockers": ["job_not_found"], "reason": "job not found"}

    task = None
    for t in job.tasks:
        if str(t.id) == task_id:
            task = t
            break
    if task is None:
        return {"ready": False, "blockers": ["task_not_found"], "reason": "task not in job"}

    status = t.status.value if hasattr(t.status, "value") else str(t.status)
    if status == "completed":
        return {"ready": False, "blockers": ["already_completed"], "reason": "task already completed"}
    if status == "pending":
        return {"ready": False, "blockers": ["still_pending"], "reason": "task is pending, not failed"}
    if status not in ("failed",):
        blockers.append(f"status_{status}")

    recon = reconcile_materialized(job_id, root)
    if not recon["consistent"]:
        blockers.append("materialization_mismatch")

    return {
        "ready": len(blockers) == 0,
        "blockers": blockers,
        "reason": blockers[0] if blockers else "retryable",
        "required_human_action": "review failure reason before retry" if not blockers else "",
    }
