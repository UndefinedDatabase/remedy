"""
Proposed Task domain model and lifecycle.

A proposed task is a task suggestion that must be evaluated before it can
enter the build queue. Sources: reviewer findings, orchestrator rework
requests, user suggestions, model recommendations.

Lifecycle::

    proposed -> evaluated -> approved_for_build | rejected | deferred

Only tasks with status ``approved_for_build`` may enter the build queue.
Finalized gate is blocked while any task has status ``proposed`` or ``evaluated``.

Storage: JSON files under <data_dir>/proposed_tasks/<job_id>.json
Each file is a JSON array of ProposedTask dicts for that job.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from packages.orchestration.data_paths import proposed_tasks_dir


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class ProposedTaskSource(str, Enum):
    """Who or what created the proposed task."""

    USER = "user"
    REVIEWER = "reviewer"
    ORCHESTRATOR = "orchestrator"
    MODEL = "model"


class ProposedTaskStatus(str, Enum):
    """Lifecycle state of a proposed task."""

    PROPOSED = "proposed"
    EVALUATED = "evaluated"
    APPROVED_FOR_BUILD = "approved_for_build"
    REJECTED = "rejected"
    DEFERRED = "deferred"


# Statuses that block finalized gate
UNRESOLVED_STATUSES = frozenset({
    ProposedTaskStatus.PROPOSED,
    ProposedTaskStatus.EVALUATED,
})

# Statuses that are terminal (no further transitions)
TERMINAL_STATUSES = frozenset({
    ProposedTaskStatus.APPROVED_FOR_BUILD,
    ProposedTaskStatus.REJECTED,
    ProposedTaskStatus.DEFERRED,
})


class ProposedTask(BaseModel):
    """A task suggestion awaiting evaluation before build."""

    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    title: str
    reason: str = ""
    description: str = ""
    source: ProposedTaskSource = ProposedTaskSource.REVIEWER
    risk: str = "low"
    priority: str = "medium"
    status: ProposedTaskStatus = ProposedTaskStatus.PROPOSED
    approval_required: bool = True

    # Traceability
    job_id: str = ""
    origin_task_id: str = ""
    origin_recommendation_id: str = ""
    task_type: str = "unknown"

    # Evaluation result (filled by evaluator)
    evaluation_notes: str = ""
    evaluated_by: str = ""  # "deterministic" or "llm" or "user"
    evaluated_at: datetime | None = None

    # Timestamps
    created_at: datetime = Field(default_factory=_utcnow)
    resolved_at: datetime | None = None

    def is_unresolved(self) -> bool:
        """True if this task blocks finalized gate."""
        return self.status in UNRESOLVED_STATUSES

    def is_terminal(self) -> bool:
        """True if no further transitions are possible."""
        return self.status in TERMINAL_STATUSES


# ---------------------------------------------------------------------------
# State transitions
# ---------------------------------------------------------------------------

_VALID_TRANSITIONS: dict[ProposedTaskStatus, frozenset[ProposedTaskStatus]] = {
    ProposedTaskStatus.PROPOSED: frozenset({
        ProposedTaskStatus.EVALUATED,
        ProposedTaskStatus.APPROVED_FOR_BUILD,
        ProposedTaskStatus.REJECTED,
        ProposedTaskStatus.DEFERRED,
    }),
    ProposedTaskStatus.EVALUATED: frozenset({
        ProposedTaskStatus.APPROVED_FOR_BUILD,
        ProposedTaskStatus.REJECTED,
        ProposedTaskStatus.DEFERRED,
    }),
    # Terminal states have no outgoing transitions
    ProposedTaskStatus.APPROVED_FOR_BUILD: frozenset(),
    ProposedTaskStatus.REJECTED: frozenset(),
    ProposedTaskStatus.DEFERRED: frozenset(),
}


class InvalidTransitionError(Exception):
    """Raised when a proposed task state transition is not allowed."""

    def __init__(self, task_id: str, current: ProposedTaskStatus, target: ProposedTaskStatus) -> None:
        super().__init__(f"Cannot transition proposed task {task_id} from {current.value} to {target.value}")
        self.task_id = task_id
        self.current = current
        self.target = target


def transition_status(task: ProposedTask, target: ProposedTaskStatus, *, by: str = "") -> None:
    """Transition a proposed task to a new status.

    Raises InvalidTransitionError if the transition is not allowed.
    Mutates the task in place.
    """
    allowed = _VALID_TRANSITIONS.get(task.status, frozenset())
    if target not in allowed:
        raise InvalidTransitionError(task.id, task.status, target)

    task.status = target
    now = _utcnow()

    if target == ProposedTaskStatus.EVALUATED:
        task.evaluated_at = now
        if by:
            task.evaluated_by = by

    if target in TERMINAL_STATUSES:
        task.resolved_at = now


# ---------------------------------------------------------------------------
# Persistence — JSON files per job
# ---------------------------------------------------------------------------

_STORE_DIR: Path = proposed_tasks_dir()


def _job_path(job_id: str) -> Path:
    """Return the JSON file path for a job's proposed tasks."""
    return _STORE_DIR / f"{job_id}.json"


def save_proposed_tasks(job_id: str, tasks: list[ProposedTask]) -> None:
    """Persist all proposed tasks for a job."""
    _STORE_DIR.mkdir(parents=True, exist_ok=True)
    path = _job_path(job_id)
    data = [t.model_dump(mode="json") for t in tasks]
    path.write_text(json.dumps(data, indent=2, default=str))


def load_proposed_tasks(job_id: str) -> list[ProposedTask]:
    """Load all proposed tasks for a job. Returns [] if none exist."""
    path = _job_path(job_id)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        return [ProposedTask.model_validate(d) for d in data]
    except (ValueError, OSError):
        return []


def add_proposed_task(job_id: str, task: ProposedTask) -> None:
    """Append a single proposed task for a job."""
    tasks = load_proposed_tasks(job_id)
    tasks.append(task)
    save_proposed_tasks(job_id, tasks)


def get_proposed_task(job_id: str, task_id: str) -> ProposedTask | None:
    """Find a single proposed task by ID."""
    for t in load_proposed_tasks(job_id):
        if t.id == task_id:
            return t
    return None


def update_proposed_task(job_id: str, task: ProposedTask) -> bool:
    """Update a proposed task in place. Returns True if found and updated."""
    tasks = load_proposed_tasks(job_id)
    for i, t in enumerate(tasks):
        if t.id == task.id:
            tasks[i] = task
            save_proposed_tasks(job_id, tasks)
            return True
    return False


def count_unresolved(job_id: str) -> int:
    """Count proposed tasks that block finalized gate."""
    return sum(1 for t in load_proposed_tasks(job_id) if t.is_unresolved())


def list_by_status(job_id: str, status: ProposedTaskStatus) -> list[ProposedTask]:
    """List proposed tasks filtered by status."""
    return [t for t in load_proposed_tasks(job_id) if t.status == status]


# ---------------------------------------------------------------------------
# Review finding → proposed task bridge
# ---------------------------------------------------------------------------

def propose_task_from_review_finding(
    job_id: str,
    *,
    title: str,
    reason: str = "",
    description: str = "",
    risk: str = "low",
    priority: str = "medium",
    task_type: str = "unknown",
    origin_task_id: str = "",
    origin_recommendation_id: str = "",
    source: ProposedTaskSource = ProposedTaskSource.REVIEWER,
) -> ProposedTask:
    """Create and persist a proposed task from a review finding.

    Returns the created ProposedTask (status=proposed, approval_required=True).
    """
    task = ProposedTask(
        title=title[:80],
        reason=reason[:200],
        description=description[:500],
        source=source,
        risk=risk,
        priority=priority,
        task_type=task_type,
        job_id=job_id,
        origin_task_id=origin_task_id,
        origin_recommendation_id=origin_recommendation_id,
    )
    add_proposed_task(job_id, task)
    return task


def propose_from_recommendation(
    job_id: str,
    rec: Any,
) -> ProposedTask:
    """Create a proposed task from a ReviewerRecommendation.

    Accepts either a ReviewerRecommendation dataclass or a dict with the
    same keys. This replaces the old accept_recommendation() flow where
    reviewer findings directly became executable tasks.
    """
    if hasattr(rec, "title"):
        # Dataclass
        return propose_task_from_review_finding(
            job_id,
            title=rec.title,
            reason=rec.reason,
            description=getattr(rec, "description", ""),
            risk=rec.risk,
            priority=rec.priority,
            task_type=rec.task_type,
            origin_task_id=getattr(rec, "origin_task_id", ""),
            origin_recommendation_id=rec.id,
            source=ProposedTaskSource.REVIEWER,
        )
    # Dict form
    return propose_task_from_review_finding(
        job_id,
        title=str(rec.get("title", "")),
        reason=str(rec.get("reason", "")),
        description=str(rec.get("description", "")),
        risk=str(rec.get("risk", "low")),
        priority=str(rec.get("priority", "medium")),
        task_type=str(rec.get("task_type", "unknown")),
        origin_task_id=str(rec.get("origin_task_id", "")),
        origin_recommendation_id=str(rec.get("id", "")),
        source=ProposedTaskSource.REVIEWER,
    )


# ---------------------------------------------------------------------------
# Deterministic evaluator (Step 569)
# ---------------------------------------------------------------------------

class EvaluationResult:
    """Result of evaluating a proposed task."""

    __slots__ = ("decision", "notes")

    def __init__(self, decision: ProposedTaskStatus, notes: str = "") -> None:
        self.decision = decision
        self.notes = notes


def _evaluate_risk_rule(task: ProposedTask) -> EvaluationResult | None:
    """High-risk tasks always require human approval."""
    if task.risk == "high":
        return EvaluationResult(ProposedTaskStatus.EVALUATED, "high risk — needs human approval")
    return None


def _evaluate_duplicate_rule(task: ProposedTask, existing: list[ProposedTask]) -> EvaluationResult | None:
    """Reject if an identical title already exists (approved or proposed)."""
    title_lower = task.title.lower().strip()
    for other in existing:
        if other.id == task.id:
            continue
        if other.title.lower().strip() == title_lower and other.status not in (
            ProposedTaskStatus.REJECTED,
            ProposedTaskStatus.DEFERRED,
        ):
            return EvaluationResult(ProposedTaskStatus.REJECTED, f"duplicate of {other.id}")
    return None


def _evaluate_auto_approve_rule(task: ProposedTask) -> EvaluationResult | None:
    """Low-risk tasks from trusted sources can auto-approve."""
    if task.risk == "low" and not task.approval_required:
        return EvaluationResult(ProposedTaskStatus.APPROVED_FOR_BUILD, "auto-approved: low risk, no approval required")
    return None


def evaluate_proposed_task(
    job_id: str,
    task_id: str,
) -> ProposedTask | None:
    """Run deterministic evaluation rules on a proposed task.

    Returns the updated task, or None if not found.
    Mutates and persists the task.
    """
    tasks = load_proposed_tasks(job_id)
    task = None
    for t in tasks:
        if t.id == task_id:
            task = t
            break
    if task is None:
        return None

    if task.status != ProposedTaskStatus.PROPOSED:
        return task  # already evaluated or resolved

    # Run rules in priority order
    result = _evaluate_duplicate_rule(task, tasks)
    if result is None:
        result = _evaluate_risk_rule(task)
    if result is None:
        result = _evaluate_auto_approve_rule(task)
    if result is None:
        # Default: mark as evaluated, needs human decision
        result = EvaluationResult(ProposedTaskStatus.EVALUATED, "awaiting human decision")

    transition_status(task, result.decision, by="deterministic")
    task.evaluation_notes = result.notes
    save_proposed_tasks(job_id, tasks)
    return task


def evaluate_all_proposed(job_id: str) -> list[ProposedTask]:
    """Evaluate all proposed (unevaluated) tasks for a job. Returns updated list."""
    tasks = load_proposed_tasks(job_id)
    changed = False
    for task in tasks:
        if task.status != ProposedTaskStatus.PROPOSED:
            continue
        result = _evaluate_duplicate_rule(task, tasks)
        if result is None:
            result = _evaluate_risk_rule(task)
        if result is None:
            result = _evaluate_auto_approve_rule(task)
        if result is None:
            result = EvaluationResult(ProposedTaskStatus.EVALUATED, "awaiting human decision")
        transition_status(task, result.decision, by="deterministic")
        task.evaluation_notes = result.notes
        changed = True
    if changed:
        save_proposed_tasks(job_id, tasks)
    return tasks


# ---------------------------------------------------------------------------
# LLM evaluator interface (Step 570 — disabled by default)
# ---------------------------------------------------------------------------

def evaluate_with_llm(
    job_id: str,
    task_id: str,
    *,
    llm_fn: Any | None = None,
) -> ProposedTask | None:
    """Optional LLM-based evaluation. Disabled when llm_fn is None.

    The llm_fn signature: (task: ProposedTask) -> EvaluationResult
    When enabled, overrides deterministic evaluation for a single task.
    """
    if llm_fn is None:
        return evaluate_proposed_task(job_id, task_id)

    task = get_proposed_task(job_id, task_id)
    if task is None or task.status != ProposedTaskStatus.PROPOSED:
        return task

    result: EvaluationResult = llm_fn(task)
    transition_status(task, result.decision, by="llm")
    task.evaluation_notes = result.notes
    update_proposed_task(job_id, task)
    return task


# ---------------------------------------------------------------------------
# Approve / reject / defer (Step 571)
# ---------------------------------------------------------------------------

def approve_proposed_task(job_id: str, task_id: str) -> ProposedTask | None:
    """Approve a proposed task for build. Returns updated task or None."""
    task = get_proposed_task(job_id, task_id)
    if task is None:
        return None
    transition_status(task, ProposedTaskStatus.APPROVED_FOR_BUILD, by="user")
    update_proposed_task(job_id, task)
    return task


def reject_proposed_task(job_id: str, task_id: str, *, reason: str = "") -> ProposedTask | None:
    """Reject a proposed task. Returns updated task or None."""
    task = get_proposed_task(job_id, task_id)
    if task is None:
        return None
    if reason:
        task.evaluation_notes = reason
    transition_status(task, ProposedTaskStatus.REJECTED, by="user")
    update_proposed_task(job_id, task)
    return task


def defer_proposed_task(job_id: str, task_id: str, *, reason: str = "") -> ProposedTask | None:
    """Defer a proposed task. Returns updated task or None."""
    task = get_proposed_task(job_id, task_id)
    if task is None:
        return None
    if reason:
        task.evaluation_notes = reason
    transition_status(task, ProposedTaskStatus.DEFERRED, by="user")
    update_proposed_task(job_id, task)
    return task


# ---------------------------------------------------------------------------
# Review loop rework proposals (Step 573)
# ---------------------------------------------------------------------------

def propose_rework(
    job_id: str,
    *,
    failed_task_id: str,
    title: str,
    reason: str = "",
    risk: str = "medium",
) -> ProposedTask:
    """Create a rework proposal when a build/test cycle fails.

    Called by the orchestrator when a task fails verification and needs
    rework. The rework proposal goes through the same evaluation flow.
    """
    return propose_task_from_review_finding(
        job_id,
        title=title[:80],
        reason=reason[:200] if reason else f"rework needed for failed task {failed_task_id}",
        risk=risk,
        priority="high",
        task_type="rework",
        origin_task_id=failed_task_id,
        source=ProposedTaskSource.ORCHESTRATOR,
    )


# ---------------------------------------------------------------------------
# Event audit trail (Step 576)
# ---------------------------------------------------------------------------

def emit_proposed_task_event(
    writer: Any,
    event_name: str,
    task: ProposedTask,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
    """Emit an audit event for a proposed task lifecycle change.

    Uses RunLogWriter.log() pattern. Safe if writer is None (no-op).

    Event names: proposed_task_created, proposed_task_evaluated,
    proposed_task_approved, proposed_task_rejected, proposed_task_deferred
    """
    if writer is None:
        return
    metadata: dict[str, Any] = {
        "proposed_task_id": task.id,
        "title": task.title[:80],
        "source": task.source.value,
        "status": task.status.value,
        "risk": task.risk,
        "task_type": task.task_type,
    }
    if task.evaluation_notes:
        metadata["evaluation_notes"] = task.evaluation_notes[:200]
    if task.evaluated_by:
        metadata["evaluated_by"] = task.evaluated_by
    if task.origin_task_id:
        metadata["origin_task_id"] = task.origin_task_id
    if extra:
        metadata.update(extra)
    writer.log(event_name, task_id=task.origin_task_id or None, outcome=task.status.value, **metadata)
