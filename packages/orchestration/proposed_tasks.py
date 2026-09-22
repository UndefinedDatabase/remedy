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

import fcntl
import json
import os
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from packages.common.secure_fs import durable_write
from packages.orchestration.data_paths import normalize_job_id, proposed_tasks_dir


def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


class ProposedTaskSource(str, Enum):
    USER = "user"
    REVIEWER = "reviewer"
    ORCHESTRATOR = "orchestrator"
    MODEL = "model"


class ProposedTaskStatus(str, Enum):
    PROPOSED = "proposed"
    EVALUATED = "evaluated"
    APPROVED_FOR_BUILD = "approved_for_build"
    REJECTED = "rejected"
    DEFERRED = "deferred"


UNRESOLVED_STATUSES = frozenset({
    ProposedTaskStatus.PROPOSED,
    ProposedTaskStatus.EVALUATED,
})

TERMINAL_STATUSES = frozenset({
    ProposedTaskStatus.APPROVED_FOR_BUILD,
    ProposedTaskStatus.REJECTED,
    ProposedTaskStatus.DEFERRED,
})


class ProposedTask(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex[:12])
    title: str
    reason: str = ""
    description: str = ""
    source: ProposedTaskSource = ProposedTaskSource.REVIEWER
    risk: str = "low"
    priority: str = "medium"
    status: ProposedTaskStatus = ProposedTaskStatus.PROPOSED
    approval_required: bool = True

    job_id: str = ""
    origin_task_id: str = ""
    origin_recommendation_id: str = ""
    task_type: str = "unknown"

    evaluation_notes: str = ""
    evaluated_by: str = ""
    evaluated_at: datetime | None = None

    created_at: datetime = Field(default_factory=_utcnow)
    resolved_at: datetime | None = None

    materialized_task_id: str = ""
    materialized_at: datetime | None = None

    def is_unresolved(self) -> bool:
        return self.status in UNRESOLVED_STATUSES

    def is_terminal(self) -> bool:
        return self.status in TERMINAL_STATUSES

    @property
    def is_materialized(self) -> bool:
        return bool(self.materialized_task_id)


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
    ProposedTaskStatus.APPROVED_FOR_BUILD: frozenset(),
    ProposedTaskStatus.REJECTED: frozenset(),
    ProposedTaskStatus.DEFERRED: frozenset(),
}


class InvalidTransitionError(Exception):
    def __init__(self, task_id: str, current: ProposedTaskStatus, target: ProposedTaskStatus) -> None:
        super().__init__(f"Cannot transition proposed task {task_id} from {current.value} to {target.value}")
        self.task_id = task_id
        self.current = current
        self.target = target


class ProposedTaskStoreError(Exception):
    """Raised when proposed task storage is corrupt or unreadable."""


def transition_status(task: ProposedTask, target: ProposedTaskStatus, *, by: str = "") -> None:
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
# Persistence — JSON files per job, atomic writes, file locking
# ---------------------------------------------------------------------------

# Legacy compat: monkeypatchable in old tests (deprecated, use root= param)
_STORE_DIR: Path | None = None


def _resolve_store_dir(root: Path | None = None) -> Path:
    if root is not None:
        return root / "proposed_tasks"
    if _STORE_DIR is not None:
        return _STORE_DIR
    return proposed_tasks_dir()


def _job_path(job_id: str, root: Path | None = None) -> Path:
    return _resolve_store_dir(root) / f"{job_id}.json"


def _lock_path(job_id: str, root: Path | None = None) -> Path:
    return _resolve_store_dir(root) / f".{job_id}.lock"


_LOCK_TIMEOUT_SEC = 5


@contextmanager
def _file_lock(job_id: str, root: Path | None = None) -> Iterator[None]:
    """Acquire an advisory file lock for a job's proposed task store.

    Uses fcntl.flock with bounded timeout via alarm-free retry.
    """
    store = _resolve_store_dir(root)
    store.mkdir(parents=True, exist_ok=True)
    lock_file = _lock_path(job_id, root)
    fd = os.open(str(lock_file), os.O_CREAT | os.O_RDWR)
    try:
        import time
        deadline = time.monotonic() + _LOCK_TIMEOUT_SEC
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (OSError, BlockingIOError):
                if time.monotonic() >= deadline:
                    raise ProposedTaskStoreError(
                        f"Could not acquire lock for job {job_id} within {_LOCK_TIMEOUT_SEC}s"
                    )
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)
        try:
            os.unlink(str(lock_file))
        except OSError:
            pass


def save_proposed_tasks(job_id: str, tasks: list[ProposedTask], root: Path | None = None) -> None:
    store = _resolve_store_dir(root)
    store.mkdir(parents=True, exist_ok=True)
    path = _job_path(job_id, root)
    data = [t.model_dump(mode="json") for t in tasks]
    durable_write(path, json.dumps(data, indent=2, default=str))


def load_proposed_tasks(job_id: str, root: Path | None = None) -> list[ProposedTask]:
    """Load all proposed tasks for a job.

    Returns [] if file does not exist.
    Raises ProposedTaskStoreError if file exists but is corrupt.
    """
    path = _job_path(job_id, root)
    if not path.exists():
        return []
    try:
        raw = path.read_text()
        data = json.loads(raw)
        return [ProposedTask.model_validate(d) for d in data]
    except (json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        raise ProposedTaskStoreError(f"Corrupt proposed task store for job {job_id}: {exc}") from exc
    except OSError as exc:
        raise ProposedTaskStoreError(f"Cannot read proposed task store for job {job_id}: {exc}") from exc


def load_proposed_tasks_safe(job_id: str, root: Path | None = None) -> tuple[list[ProposedTask], bool]:
    """Load proposed tasks, returning (tasks, degraded).

    If store is corrupt, returns ([], True) instead of raising.
    """
    try:
        return (load_proposed_tasks(job_id, root), False)
    except ProposedTaskStoreError:
        return ([], True)


def add_proposed_task(job_id: str, task: ProposedTask, root: Path | None = None) -> None:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        tasks.append(task)
        save_proposed_tasks(job_id, tasks, root)


def add_and_evaluate_proposed_task(job_id: str, task: ProposedTask, root: Path | None = None) -> ProposedTask:
    """Add a proposed task to the store and immediately evaluate it.

    Evaluates the task inside the same file lock that add_proposed_task takes,
    running the deterministic rules (duplicate, risk, auto-approve) before appending.

    Returns the evaluated task.
    """
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)

        # Run the three deterministic rules
        result = _evaluate_duplicate_rule(task, tasks)
        if result is None:
            result = _evaluate_risk_rule(task)
        if result is None:
            result = _evaluate_auto_approve_rule(task)
        if result is None:
            result = EvaluationResult(ProposedTaskStatus.EVALUATED, "awaiting human decision")

        # Transition and set evaluation notes
        transition_status(task, result.decision, by="deterministic")
        task.evaluation_notes = result.notes

        # Append and save
        tasks.append(task)
        save_proposed_tasks(job_id, tasks, root)

    return task


def get_proposed_task(job_id: str, task_id: str, root: Path | None = None) -> ProposedTask | None:
    for t in load_proposed_tasks(job_id, root):
        if t.id == task_id:
            return t
    return None


def count_unresolved(job_id: str, root: Path | None = None) -> int:
    return sum(1 for t in load_proposed_tasks(job_id, root) if t.is_unresolved())


def count_unresolved_safe(job_id: str, root: Path | None = None) -> tuple[int, bool]:
    try:
        return (count_unresolved(job_id, root), False)
    except ProposedTaskStoreError:
        return (-1, True)


def list_by_status(job_id: str, status: ProposedTaskStatus, root: Path | None = None) -> list[ProposedTask]:
    return [t for t in load_proposed_tasks(job_id, root) if t.status == status]


# ---------------------------------------------------------------------------
# Deterministic evaluator
# ---------------------------------------------------------------------------

class EvaluationResult:
    __slots__ = ("decision", "notes")

    def __init__(self, decision: ProposedTaskStatus, notes: str = "") -> None:
        self.decision = decision
        self.notes = notes


def _evaluate_risk_rule(task: ProposedTask) -> EvaluationResult | None:
    if task.risk == "high":
        return EvaluationResult(ProposedTaskStatus.EVALUATED, "high risk — needs human approval")
    return None


def _evaluate_duplicate_rule(task: ProposedTask, existing: list[ProposedTask]) -> EvaluationResult | None:
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
    if task.risk == "low" and not task.approval_required:
        return EvaluationResult(ProposedTaskStatus.APPROVED_FOR_BUILD, "auto-approved: low risk, no approval required")
    return None


# ---------------------------------------------------------------------------
# Approve / reject / defer
# ---------------------------------------------------------------------------

_MAX_REASON_LEN = 200


def approve_proposed_task(job_id: str, task_id: str, root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        task = None
        for i, t in enumerate(tasks):
            if t.id == task_id:
                task = t
                transition_status(task, ProposedTaskStatus.APPROVED_FOR_BUILD, by="user")
                tasks[i] = task
                break
        if task is None:
            return None
        save_proposed_tasks(job_id, tasks, root)
    return task


def reject_proposed_task(job_id: str, task_id: str, *, reason: str = "", root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        task = None
        for i, t in enumerate(tasks):
            if t.id == task_id:
                task = t
                if reason:
                    task.evaluation_notes = reason[:_MAX_REASON_LEN]
                transition_status(task, ProposedTaskStatus.REJECTED, by="user")
                tasks[i] = task
                break
        if task is None:
            return None
        save_proposed_tasks(job_id, tasks, root)
    return task


def defer_proposed_task(job_id: str, task_id: str, *, reason: str = "", root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        task = None
        for i, t in enumerate(tasks):
            if t.id == task_id:
                task = t
                if reason:
                    task.evaluation_notes = reason[:_MAX_REASON_LEN]
                transition_status(task, ProposedTaskStatus.DEFERRED, by="user")
                tasks[i] = task
                break
        if task is None:
            return None
        save_proposed_tasks(job_id, tasks, root)
    return task


# ---------------------------------------------------------------------------
# Materialization — approved proposed tasks → build tasks
# ---------------------------------------------------------------------------

def materialize_approved_task(proposed: ProposedTask) -> dict[str, Any]:
    """Convert an approved ProposedTask into a Task-compatible dict.

    Returns a dict that can be used with Task.model_validate() to create
    a real build task. Does NOT persist — caller is responsible for
    appending to job.tasks and saving the job.

    Raises ValueError if the proposed task is not approved_for_build.
    """
    if proposed.status != ProposedTaskStatus.APPROVED_FOR_BUILD:
        raise ValueError(f"Cannot materialize: status is {proposed.status.value}, not approved_for_build")
    if proposed.is_materialized:
        raise ValueError(f"Already materialized: {proposed.id} → {proposed.materialized_task_id}")

    from uuid import uuid4 as _uuid4
    task_id = str(_uuid4())

    inputs: dict[str, Any] = {
        "proposed_task_id": proposed.id,
        "task_type": proposed.task_type,
        "reason": proposed.reason[:200],
        "source": proposed.source.value,
        "risk": proposed.risk,
        "priority": proposed.priority,
    }
    if proposed.origin_task_id:
        inputs["origin_task_id"] = proposed.origin_task_id
    if proposed.origin_recommendation_id:
        inputs["origin_recommendation_id"] = proposed.origin_recommendation_id

    return {
        "id": task_id,
        "description": proposed.title[:80],
        "inputs": inputs,
        "status": "pending",
    }


def do_materialize(job_id: str, task_id: str, root: Path | None = None) -> ProposedTask | None:
    """Materialize an approved proposed task into a real Job Task.

    1. Loads the Job (requires real persisted Job).
    2. Creates a Task from the approved ProposedTask.
    3. Appends Task to Job.tasks and saves the Job.
    4. Marks ProposedTask.materialized_task_id and saves proposal store.

    Order: Job saved first, then proposal. If proposal save fails after
    Job save, the Task exists in Job while the proposal stays unmarked.

    Raises:
        JobNotFoundError: if job_id does not correspond to a persisted Job.
        ValueError: if task is not approved or already materialized.
    """
    from packages.orchestration.pingpong_job import TaskEntry, load_job_plan, save_job_plan

    job_uuid = normalize_job_id(job_id)

    with _file_lock(job_id, root):
        job = load_job_plan(job_uuid, root)
        tasks = load_proposed_tasks(job_id, root)
        ptask = None
        for t in tasks:
            if t.id == task_id:
                ptask = t
                break
        if ptask is None:
            return None
        if ptask.status != ProposedTaskStatus.APPROVED_FOR_BUILD:
            raise ValueError(f"Cannot materialize: status is {ptask.status.value}, not approved_for_build")
        if ptask.is_materialized:
            raise ValueError(f"Already materialized: {ptask.id} → {ptask.materialized_task_id}")

        task_dict = materialize_approved_task(ptask)
        real_task = TaskEntry(task_id=task_dict["id"], title=task_dict["description"], inputs=task_dict["inputs"],
                              status=task_dict["status"])

        job.tasks.append(real_task)
        save_job_plan(job, root)

        ptask.materialized_task_id = str(real_task.task_id)
        ptask.materialized_at = _utcnow()
        save_proposed_tasks(job_id, tasks, root)
    return ptask


def list_approved_not_materialized(
    job_id: str,
    root: Path | None = None,
) -> list[ProposedTask]:
    approved = list_by_status(job_id, ProposedTaskStatus.APPROVED_FOR_BUILD, root)
    return [t for t in approved if not t.is_materialized]


# ---------------------------------------------------------------------------
# Finalized gate helper
# ---------------------------------------------------------------------------

def can_finalize(
    job_id: str,
    *,
    pending_task_count: int = 0,
    blocked_task_count: int = 0,
    pending_approvals: int = 0,
    root: Path | None = None,
) -> tuple[bool, str]:
    """Check whether a job can be finalized.

    Returns (can_finalize, reason).
    Blocks if: corrupt store, unresolved proposals, approved-not-materialized,
    pending/blocked tasks, pending approvals.
    """
    tasks_result, degraded = load_proposed_tasks_safe(job_id, root)
    if degraded:
        return (False, "proposed_task_store_degraded")
    unresolved = sum(1 for t in tasks_result if t.is_unresolved())
    if pending_task_count > 0:
        return (False, f"{pending_task_count} pending tasks")
    if blocked_task_count > 0:
        return (False, f"{blocked_task_count} blocked tasks")
    if pending_approvals > 0:
        return (False, f"{pending_approvals} pending approvals")
    if unresolved > 0:
        return (False, f"{unresolved} unresolved proposals")
    not_materialized = sum(
        1 for t in tasks_result
        if t.status == ProposedTaskStatus.APPROVED_FOR_BUILD and not t.is_materialized
    )
    if not_materialized > 0:
        return (False, f"{not_materialized} approved but not materialized")
    return (True, "ready")


# ---------------------------------------------------------------------------
# Event audit trail
# ---------------------------------------------------------------------------

def emit_proposed_task_event(
    writer: Any,
    event_name: str,
    task: ProposedTask,
    *,
    extra: dict[str, Any] | None = None,
) -> None:
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
    if task.materialized_task_id:
        metadata["materialized_task_id"] = task.materialized_task_id
    if extra:
        metadata.update(extra)
    writer.log(event_name, task_id=task.origin_task_id or None, outcome=task.status.value, **metadata)
