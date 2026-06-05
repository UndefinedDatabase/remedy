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
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterator
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.orchestration.data_paths import proposed_tasks_dir, resolve_data_root


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
                    os.close(fd)
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


def _atomic_write(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    closed = False
    try:
        os.write(fd, data.encode("utf-8"))
        os.fsync(fd)
        os.close(fd)
        closed = True
        os.replace(tmp, str(path))
    except BaseException:
        if not closed:
            try:
                os.close(fd)
            except OSError:
                pass
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def save_proposed_tasks(job_id: str, tasks: list[ProposedTask], root: Path | None = None) -> None:
    store = _resolve_store_dir(root)
    store.mkdir(parents=True, exist_ok=True)
    path = _job_path(job_id, root)
    data = [t.model_dump(mode="json") for t in tasks]
    _atomic_write(path, json.dumps(data, indent=2, default=str))


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


def get_proposed_task(job_id: str, task_id: str, root: Path | None = None) -> ProposedTask | None:
    for t in load_proposed_tasks(job_id, root):
        if t.id == task_id:
            return t
    return None


def update_proposed_task(job_id: str, task: ProposedTask, root: Path | None = None) -> bool:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                save_proposed_tasks(job_id, tasks, root)
                return True
    return False


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
    root: Path | None = None,
) -> ProposedTask:
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
    add_proposed_task(job_id, task, root)
    return task


def propose_from_recommendation(
    job_id: str,
    rec: Any,
    root: Path | None = None,
) -> ProposedTask:
    if hasattr(rec, "title"):
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
            root=root,
        )
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
        root=root,
    )


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


def evaluate_proposed_task(
    job_id: str,
    task_id: str,
    root: Path | None = None,
) -> ProposedTask | None:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
        task = None
        for t in tasks:
            if t.id == task_id:
                task = t
                break
        if task is None:
            return None

        if task.status != ProposedTaskStatus.PROPOSED:
            return task

        result = _evaluate_duplicate_rule(task, tasks)
        if result is None:
            result = _evaluate_risk_rule(task)
        if result is None:
            result = _evaluate_auto_approve_rule(task)
        if result is None:
            result = EvaluationResult(ProposedTaskStatus.EVALUATED, "awaiting human decision")

        transition_status(task, result.decision, by="deterministic")
        task.evaluation_notes = result.notes
        save_proposed_tasks(job_id, tasks, root)
    return task


def evaluate_all_proposed(job_id: str, root: Path | None = None) -> list[ProposedTask]:
    with _file_lock(job_id, root):
        tasks = load_proposed_tasks(job_id, root)
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
            save_proposed_tasks(job_id, tasks, root)
    return tasks


# ---------------------------------------------------------------------------
# LLM evaluator interface (disabled by default)
# ---------------------------------------------------------------------------

def evaluate_with_llm(
    job_id: str,
    task_id: str,
    *,
    llm_fn: Any | None = None,
    root: Path | None = None,
) -> ProposedTask | None:
    if llm_fn is None:
        return evaluate_proposed_task(job_id, task_id, root)

    task = get_proposed_task(job_id, task_id, root)
    if task is None or task.status != ProposedTaskStatus.PROPOSED:
        return task

    result: EvaluationResult = llm_fn(task)
    transition_status(task, result.decision, by="llm")
    task.evaluation_notes = result.notes
    update_proposed_task(job_id, task, root)
    return task


# ---------------------------------------------------------------------------
# Approve / reject / defer
# ---------------------------------------------------------------------------

_MAX_REASON_LEN = 200


def approve_proposed_task(job_id: str, task_id: str, root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        task = get_proposed_task(job_id, task_id, root)
        if task is None:
            return None
        transition_status(task, ProposedTaskStatus.APPROVED_FOR_BUILD, by="user")
        tasks = load_proposed_tasks(job_id, root)
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                break
        save_proposed_tasks(job_id, tasks, root)
    return task


def reject_proposed_task(job_id: str, task_id: str, *, reason: str = "", root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        task = get_proposed_task(job_id, task_id, root)
        if task is None:
            return None
        if reason:
            task.evaluation_notes = reason[:_MAX_REASON_LEN]
        transition_status(task, ProposedTaskStatus.REJECTED, by="user")
        tasks = load_proposed_tasks(job_id, root)
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                break
        save_proposed_tasks(job_id, tasks, root)
    return task


def defer_proposed_task(job_id: str, task_id: str, *, reason: str = "", root: Path | None = None) -> ProposedTask | None:
    with _file_lock(job_id, root):
        task = get_proposed_task(job_id, task_id, root)
        if task is None:
            return None
        if reason:
            task.evaluation_notes = reason[:_MAX_REASON_LEN]
        transition_status(task, ProposedTaskStatus.DEFERRED, by="user")
        tasks = load_proposed_tasks(job_id, root)
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                break
        save_proposed_tasks(job_id, tasks, root)
    return task


# ---------------------------------------------------------------------------
# Rework proposals
# ---------------------------------------------------------------------------

def propose_rework(
    job_id: str,
    *,
    failed_task_id: str,
    title: str,
    reason: str = "",
    risk: str = "medium",
    root: Path | None = None,
) -> ProposedTask:
    return propose_task_from_review_finding(
        job_id,
        title=title[:80],
        reason=reason[:200] if reason else f"rework needed for failed task {failed_task_id}",
        risk=risk,
        priority="high",
        task_type="rework",
        origin_task_id=failed_task_id,
        source=ProposedTaskSource.ORCHESTRATOR,
        root=root,
    )


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
    Job save, the Task exists in Job — reconcile_materialized can detect
    and repair the mismatch.

    Raises:
        JobNotFoundError: if job_id does not correspond to a persisted Job.
        ValueError: if task is not approved or already materialized.
    """
    from packages.orchestration.storage import load_job, save_job, JobNotFoundError
    from packages.core.models import Task

    job_uuid = UUID(job_id)

    with _file_lock(job_id, root):
        job = load_job(job_uuid, root)
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
        real_task = Task.model_validate(task_dict)

        job.tasks.append(real_task)
        save_job(job, root)

        ptask.materialized_task_id = str(real_task.id)
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

def reconcile_materialized(job_id: str, root: Path | None = None) -> dict[str, Any]:
    """Check consistency between ProposedTask materialization and Job.tasks.

    Returns a report dict (inspect-only by default).
    """
    from packages.orchestration.storage import load_job_safe

    job_uuid = UUID(job_id)
    job, job_degraded = load_job_safe(job_uuid, root)

    try:
        proposals = load_proposed_tasks(job_id, root)
        proposals_degraded = False
    except ProposedTaskStoreError:
        proposals_degraded = True
        proposals = []

    if job_degraded or proposals_degraded:
        return {
            "consistent": False,
            "job_degraded": job_degraded,
            "proposals_degraded": proposals_degraded,
            "missing_job_task": [],
            "missing_proposal_marker": [],
        }

    job_task_ids = set()
    proposed_task_id_map: dict[str, str] = {}
    if job:
        for t in job.tasks:
            tid = str(t.id)
            job_task_ids.add(tid)
            pt_id = (t.inputs or {}).get("proposed_task_id", "")
            if pt_id:
                proposed_task_id_map[pt_id] = tid

    missing_job_task = []
    missing_proposal_marker = []

    for p in proposals:
        if p.materialized_task_id and p.materialized_task_id not in job_task_ids:
            missing_job_task.append(p.id)
        if not p.materialized_task_id and p.id in proposed_task_id_map:
            missing_proposal_marker.append(p.id)

    return {
        "consistent": not missing_job_task and not missing_proposal_marker,
        "job_degraded": False,
        "proposals_degraded": False,
        "missing_job_task": missing_job_task,
        "missing_proposal_marker": missing_proposal_marker,
    }


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


# ---------------------------------------------------------------------------
# Backend readiness
# ---------------------------------------------------------------------------

def _task_status_val(t: Any) -> str:
    return t.status.value if hasattr(t.status, "value") else str(t.status)


def backend_readiness(job_id: str, root: Path | None = None) -> dict[str, Any]:
    """Structured readiness report: storage, build, finalize, overnight sections."""
    from packages.orchestration.storage import load_job_safe

    job, job_degraded = load_job_safe(UUID(job_id), root)
    proposals, proposals_degraded = load_proposed_tasks_safe(job_id, root)
    recon = reconcile_materialized(job_id, root)

    # Storage health
    job_missing = job is None and not job_degraded
    storage_healthy = not job_degraded and not job_missing and not proposals_degraded and recon["consistent"]
    storage_blockers: list[str] = []
    if job_degraded:
        storage_blockers.append("job_store_degraded")
    if job_missing:
        storage_blockers.append("job_not_found")
    if proposals_degraded:
        storage_blockers.append("proposal_store_degraded")
    if not recon["consistent"]:
        storage_blockers.append("materialization_mismatch")

    # Proposal health
    unresolved = sum(1 for t in proposals if t.is_unresolved()) if not proposals_degraded else -1
    not_mat = sum(
        1 for t in proposals
        if t.status == ProposedTaskStatus.APPROVED_FOR_BUILD and not t.is_materialized
    ) if not proposals_degraded else -1

    # Job task counts
    pending_tasks = 0
    blocked_tasks = 0
    completed_tasks = 0
    if job:
        for t in job.tasks:
            s = _task_status_val(t)
            if s in ("pending", "planned"):
                pending_tasks += 1
            elif s in ("blocked", "failed"):
                blocked_tasks += 1
            elif s == "completed":
                completed_tasks += 1

    # Build readiness
    build_blockers: list[str] = list(storage_blockers)
    if unresolved > 0:
        build_blockers.append(f"{unresolved}_unresolved_proposals")
    if not_mat > 0:
        build_blockers.append(f"{not_mat}_approved_not_materialized")
    if pending_tasks == 0 and not storage_blockers:
        build_blockers.append("no_pending_work")
    build_ready = len(build_blockers) == 0

    # Finalize readiness
    finalize_ok, finalize_reason = can_finalize(
        job_id,
        pending_task_count=pending_tasks,
        blocked_task_count=blocked_tasks,
        root=root,
    )

    return {
        "storage_health": {
            "healthy": storage_healthy,
            "blockers": storage_blockers,
            "job_exists": job is not None and not job_degraded,
            "proposal_store_healthy": not proposals_degraded,
            "materialization_consistent": recon["consistent"],
        },
        "proposal_health": {
            "unresolved": unresolved,
            "approved_not_materialized": not_mat,
            "degraded": proposals_degraded,
        },
        "build_readiness": {
            "ready": build_ready,
            "blockers": build_blockers,
            "pending_tasks": pending_tasks,
        },
        "finalize_readiness": {
            "ready": finalize_ok,
            "reason": finalize_reason,
            "pending_tasks": pending_tasks,
            "blocked_tasks": blocked_tasks,
            "completed_tasks": completed_tasks,
        },
        "overnight_readiness": {
            "ready": False,
            "blockers": ["no_overnight_mode_implemented"],
        },
    }


def overnight_readiness(job_id: str, root: Path | None = None) -> dict[str, Any]:
    """Overnight autonomy readiness gate. Does NOT execute anything."""
    base = backend_readiness(job_id, root)
    blockers: list[str] = []

    for section in ("storage_health", "build_readiness"):
        blockers.extend(base[section]["blockers"])

    if base["finalize_readiness"]["pending_tasks"] > 0:
        blockers.append(f"{base['finalize_readiness']['pending_tasks']}_pending_tasks")
    if base["finalize_readiness"]["blocked_tasks"] > 0:
        blockers.append(f"{base['finalize_readiness']['blocked_tasks']}_blocked_tasks")

    blockers.append("no_overnight_mode_implemented")
    blockers.append("no_rollback_snapshot_proof")
    blockers.append("no_token_time_budget_set")

    return {
        "ready": False,
        "blockers": blockers,
        "max_safe_autonomy_level": 0,
        "required_human_actions": ["review and approve proposed tasks", "set token budget", "configure rollback"],
        "risk_summary": "Overnight autonomy not yet safe — missing rollback, budget, and execution proof.",
    }
