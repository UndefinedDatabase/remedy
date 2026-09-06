"""Local job queue and worker lifecycle.

Safe, single-machine, file-based job queue with lease-based locking.
No external services, no Docker, no database.

Public API::

    enqueue_job(job_id, data_dir) -> QueueEntry
    list_queued(data_dir) -> list[QueueEntry]
    claim_job(job_id, worker_id, data_dir) -> WorkerLease
    release_lease(job_id, data_dir)
    get_worker_status(data_dir) -> WorkerStatus
    run_worker_once(data_dir, ...) -> WorkerResult
    run_worker_loop(data_dir, ...) -> WorkerResult
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

LIFECYCLE_STATES = frozenset({
    "queued", "claimed", "running", "waiting_for_approval",
    "blocked", "paused", "cancelling", "cancelled",
    "completed", "failed", "stale",
})

VALID_TRANSITIONS: dict[str, frozenset[str]] = {
    "queued": frozenset({"claimed", "paused", "cancelled"}),
    "claimed": frozenset({"running", "cancelled", "failed"}),
    "running": frozenset({"waiting_for_approval", "blocked", "completed", "failed", "cancelling", "paused", "queued"}),
    "waiting_for_approval": frozenset({"running", "paused", "cancelled"}),
    "blocked": frozenset({"queued", "cancelled", "failed"}),
    "paused": frozenset({"queued", "cancelled"}),
    "cancelling": frozenset({"cancelled"}),
    "cancelled": frozenset(),
    "completed": frozenset(),
    "failed": frozenset({"queued"}),
    "stale": frozenset({"queued", "cancelled"}),
}

LEASE_TIMEOUT_SEC = 300
HEARTBEAT_INTERVAL_SEC = 30


@dataclass
class QueueEntry:
    """A job in the local queue."""

    job_id: str
    lifecycle_state: str = "queued"
    queued_at: str = ""
    claimed_at: str = ""
    started_at: str = ""
    updated_at: str = ""
    completed_at: str = ""
    worker_id: str = ""
    lease_id: str = ""
    lease_expires_at: str = ""
    heartbeat_at: str = ""
    pause_requested: bool = False
    cancel_requested: bool = False
    blocked_reason: str = ""
    last_safe_event_id: str = ""


@dataclass
class WorkerLease:
    """Active claim on a job."""

    job_id: str
    worker_id: str
    lease_id: str
    lease_expires_at: str
    claimed_at: str


@dataclass
class WorkerStatus:
    """Safe worker status report."""

    worker_id: str = ""
    current_job_id: str = ""
    lifecycle_state: str = "idle"
    heartbeat_at: str = ""
    last_action: str = ""
    why_it_stopped: str = ""
    processed_job_count: int = 0
    started_at: str = ""
    stale: bool = False
    redaction: str = "safe_metadata_only"


@dataclass
class WorkerResult:
    """Result from worker run-once or run-loop."""

    worker_id: str = ""
    jobs_processed: int = 0
    last_job_id: str = ""
    last_task_id: str = ""
    last_lifecycle_state: str = ""
    action_taken: str = "idle"
    why_it_stopped: str = ""
    next_command: str = ""
    duration_ms: int = 0
    provider: str = ""
    work_performed: bool = False
    task_status: str = ""
    artifact_ids: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    budget_status: str = ""
    redaction: str = "safe_metadata_only"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _queue_dir(data_dir: str | Path) -> Path:
    d = Path(data_dir) / "queue"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _queue_file(data_dir: str | Path, job_id: str) -> Path:
    return _queue_dir(data_dir) / f"{job_id}.json"


def _load_entry(data_dir: str | Path, job_id: str) -> QueueEntry | None:
    f = _queue_file(data_dir, job_id)
    if not f.exists():
        return None
    data = json.loads(f.read_text())
    return QueueEntry(**{k: v for k, v in data.items() if k in QueueEntry.__dataclass_fields__})


def _save_entry(data_dir: str | Path, entry: QueueEntry) -> None:
    from dataclasses import asdict
    f = _queue_file(data_dir, entry.job_id)
    f.write_text(json.dumps(asdict(entry), indent=2))


def is_valid_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, frozenset())


def enqueue_job(job_id: str, data_dir: str | Path) -> QueueEntry:
    existing = _load_entry(data_dir, job_id)
    if existing and existing.lifecycle_state in ("queued", "claimed", "running"):
        return existing

    now = _now_iso()
    entry = QueueEntry(
        job_id=job_id,
        lifecycle_state="queued",
        queued_at=now,
        updated_at=now,
    )
    _save_entry(data_dir, entry)
    return entry


def list_queued(data_dir: str | Path) -> list[QueueEntry]:
    entries = []
    qdir = _queue_dir(data_dir)
    for f in sorted(qdir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            entries.append(QueueEntry(**{k: v for k, v in data.items() if k in QueueEntry.__dataclass_fields__}))
        except (json.JSONDecodeError, TypeError):
            continue
    return entries


def _has_unresolved_proposals(job_id: str, data_dir: str | Path | None = None) -> bool:
    """Check if a job has unresolved or un-materialized proposed tasks blocking build.

    Returns True if: unresolved proposals, approved_not_materialized, or store corrupt.
    """
    try:
        from packages.orchestration.proposed_tasks import (
            ProposedTaskStatus,
            load_proposed_tasks_safe,
        )
        root = Path(data_dir) if data_dir is not None else None
        tasks, degraded = load_proposed_tasks_safe(job_id, root)
        if degraded:
            return True
        for t in tasks:
            if t.is_unresolved():
                return True
            if t.status == ProposedTaskStatus.APPROVED_FOR_BUILD and not t.is_materialized:
                return True
        return False
    except ImportError:
        return False


def get_next_job(data_dir: str | Path) -> QueueEntry | None:
    entries = list_queued(data_dir)
    for e in entries:
        if e.lifecycle_state == "queued" and not e.pause_requested and not e.cancel_requested:
            if _has_unresolved_proposals(e.job_id, data_dir):
                continue
            return e
    return None


def claim_job(
    job_id: str,
    worker_id: str,
    data_dir: str | Path,
) -> WorkerLease | None:
    entry = _load_entry(data_dir, job_id)
    if entry is None:
        return None

    if entry.lifecycle_state == "stale":
        pass
    elif entry.lifecycle_state != "queued":
        if entry.worker_id and entry.worker_id != worker_id:
            if entry.lease_expires_at and entry.lease_expires_at > _now_iso():
                return None
        elif entry.lifecycle_state not in ("queued", "stale"):
            return None

    now = _now_iso()
    lease_id = uuid4().hex[:12]
    expires = datetime.now(timezone.utc).timestamp() + LEASE_TIMEOUT_SEC
    expires_iso = datetime.fromtimestamp(expires, tz=timezone.utc).isoformat()

    entry.lifecycle_state = "claimed"
    entry.worker_id = worker_id
    entry.lease_id = lease_id
    entry.lease_expires_at = expires_iso
    entry.claimed_at = now
    entry.heartbeat_at = now
    entry.updated_at = now
    _save_entry(data_dir, entry)

    return WorkerLease(
        job_id=job_id,
        worker_id=worker_id,
        lease_id=lease_id,
        lease_expires_at=expires_iso,
        claimed_at=now,
    )


def update_heartbeat(job_id: str, data_dir: str | Path) -> None:
    entry = _load_entry(data_dir, job_id)
    if entry:
        entry.heartbeat_at = _now_iso()
        entry.updated_at = _now_iso()
        _save_entry(data_dir, entry)


def transition_state(
    job_id: str,
    target_state: str,
    data_dir: str | Path,
    *,
    blocked_reason: str = "",
    why_stopped: str = "",
) -> QueueEntry | None:
    entry = _load_entry(data_dir, job_id)
    if entry is None:
        return None
    if not is_valid_transition(entry.lifecycle_state, target_state):
        return None

    now = _now_iso()
    entry.lifecycle_state = target_state
    entry.updated_at = now
    if blocked_reason:
        entry.blocked_reason = blocked_reason
    if target_state == "completed":
        entry.completed_at = now
    if target_state in ("completed", "failed", "cancelled"):
        entry.worker_id = ""
        entry.lease_id = ""
        entry.lease_expires_at = ""
    _save_entry(data_dir, entry)
    return entry


def release_lease(job_id: str, data_dir: str | Path) -> None:
    entry = _load_entry(data_dir, job_id)
    if entry:
        entry.worker_id = ""
        entry.lease_id = ""
        entry.lease_expires_at = ""
        entry.updated_at = _now_iso()
        _save_entry(data_dir, entry)


def pause_job(job_id: str, data_dir: str | Path) -> QueueEntry | None:
    entry = _load_entry(data_dir, job_id)
    if entry is None:
        return None
    if entry.lifecycle_state in ("completed", "cancelled", "failed"):
        return None
    entry.pause_requested = True
    if entry.lifecycle_state == "queued":
        entry.lifecycle_state = "paused"
    entry.updated_at = _now_iso()
    _save_entry(data_dir, entry)
    return entry


def cancel_job(job_id: str, data_dir: str | Path) -> QueueEntry | None:
    entry = _load_entry(data_dir, job_id)
    if entry is None:
        return None
    if entry.lifecycle_state in ("completed", "cancelled"):
        return None
    if entry.lifecycle_state in ("running", "claimed"):
        entry.cancel_requested = True
        entry.lifecycle_state = "cancelling"
    else:
        entry.lifecycle_state = "cancelled"
    entry.updated_at = _now_iso()
    _save_entry(data_dir, entry)
    return entry


def resume_queued(job_id: str, data_dir: str | Path) -> QueueEntry | None:
    entry = _load_entry(data_dir, job_id)
    if entry is None:
        return None
    if entry.lifecycle_state != "paused":
        return None
    entry.lifecycle_state = "queued"
    entry.pause_requested = False
    entry.updated_at = _now_iso()
    _save_entry(data_dir, entry)
    return entry


def detect_stale(data_dir: str | Path, timeout_sec: int = LEASE_TIMEOUT_SEC) -> list[QueueEntry]:
    stale = []
    now_ts = datetime.now(timezone.utc).timestamp()
    for entry in list_queued(data_dir):
        if entry.lifecycle_state in ("claimed", "running") and entry.lease_expires_at:
            try:
                expires_ts = datetime.fromisoformat(entry.lease_expires_at).timestamp()
                if now_ts > expires_ts:
                    entry.lifecycle_state = "stale"
                    entry.updated_at = _now_iso()
                    _save_entry(data_dir, entry)
                    stale.append(entry)
            except (ValueError, TypeError):
                continue
    return stale


def get_worker_status(data_dir: str | Path) -> WorkerStatus:
    status_file = Path(data_dir) / "worker_status.json"
    if not status_file.exists():
        return WorkerStatus()
    try:
        data = json.loads(status_file.read_text())
        return WorkerStatus(**{k: v for k, v in data.items() if k in WorkerStatus.__dataclass_fields__})
    except (json.JSONDecodeError, TypeError):
        return WorkerStatus()


def _save_worker_status(data_dir: str | Path, status: WorkerStatus) -> None:
    from dataclasses import asdict
    status_file = Path(data_dir) / "worker_status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)
    status_file.write_text(json.dumps(asdict(status), indent=2))


ALLOWED_PROVIDERS = frozenset({"none", "fixture", "ollama"})

_TASK_EXEC_PROVIDERS = frozenset({"fixture"})


def validate_provider(provider: str) -> str | None:
    """Return error message if provider invalid, None if valid."""
    if provider not in ALLOWED_PROVIDERS:
        return f"Unknown provider '{provider}'. Allowed: {', '.join(sorted(ALLOWED_PROVIDERS))}"
    return None


def _map_result_to_lifecycle(
    provider: str,
    autorun_stage: str = "",
    autorun_stop_reason: str = "",
) -> tuple[str, str, str]:
    """Map worker result to (lifecycle_state, action_taken, why_it_stopped)."""
    if provider == "none":
        return ("blocked", "no_work_performed", "no_worker_selected")

    if autorun_stop_reason == "approval_required":
        return ("waiting_for_approval", "stopped_for_approval", "approval_required")
    if autorun_stop_reason == "provider_unavailable":
        return ("blocked", "blocked", "provider_unavailable")
    if autorun_stop_reason in ("structured_patch_parse_failed", "provider_output_prose_only",
                                "provider_output_malformed", "no_structured_patch_text"):
        return ("blocked", "blocked", autorun_stop_reason)
    if autorun_stage == "proof_collected" or autorun_stop_reason == "":
        if autorun_stage in ("proof_collected", "tested"):
            return ("completed", "completed", "work_done")
    if autorun_stage == "fixture_complete":
        return ("completed", "example_completed", "fixture_complete")

    return ("blocked", "blocked", autorun_stop_reason or "unknown")


def _run_via_task_execution(
    entry: QueueEntry,
    provider: str,
    data_dir: str | Path,
    worker_id: str,
    start: float,
    result: WorkerResult,
    *,
    max_steps: int = 1,
    max_tokens: int = 0,
    max_runtime_seconds: int = 60,
) -> WorkerResult:
    """Execute one pending Job.tasks item through the modular task_execution port."""
    from packages.core.models import RunState
    from packages.orchestration.storage import JobNotFoundError, JobStoreError, load_job, save_job
    from packages.orchestration.task_execution import BudgetGate, TaskExecutionRequest, execute_task

    root = Path(data_dir)
    result.provider = provider

    budget = BudgetGate(max_steps=max_steps, max_tokens=max_tokens, max_runtime_seconds=max_runtime_seconds)
    budget_ok, budget_reason = budget.can_execute()
    if not budget_ok:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason=budget_reason)
        release_lease(entry.job_id, data_dir)
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = budget_reason
        result.budget_status = budget_reason
        return result
    result.budget_status = "ok"

    try:
        job = load_job(entry.job_id, root)
    except JobNotFoundError:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason="job_not_found")
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = "job_not_found"
        result.blocked_reason = "job_not_found"
        return result
    except JobStoreError:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason="job_store_degraded")
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = "job_store_degraded"
        result.blocked_reason = "job_store_degraded"
        return result

    pending_task = None
    for t in job.tasks:
        s = t.status.value if hasattr(t.status, "value") else str(t.status)
        if s == "pending":
            pending_task = t
            break

    if pending_task is None:
        transition_state(entry.job_id, "completed", data_dir)
        result.last_lifecycle_state = "completed"
        result.action_taken = "no_pending_tasks"
        result.why_it_stopped = "all_tasks_done"
        return result

    task_id_str = str(pending_task.id)
    result.last_task_id = task_id_str
    result.last_job_id = str(job.id)

    writer = None
    try:
        from packages.orchestration.run_log import RunLogWriter
        writer = RunLogWriter(job.id, data_root=root)
    except (ImportError, OSError):
        pass

    proposed_task_id = (pending_task.inputs or {}).get("proposed_task_id", "")
    event_meta = {
        "proposed_task_id": proposed_task_id,
        "provider": provider,
    }

    if writer:
        writer.log("task_execution_started", task_id=task_id_str, outcome="started", **event_meta)

    req = TaskExecutionRequest(
        job_id=str(job.id),
        task_id=task_id_str,
        task_description=pending_task.description[:80],
        task_inputs=dict(pending_task.inputs) if pending_task.inputs else {},
        provider=provider,
    )
    exec_result = execute_task(req)

    budget.record_step(tokens=exec_result.token_count, elapsed=exec_result.duration_ms / 1000.0)

    result.work_performed = exec_result.work_performed
    result.artifact_ids = list(exec_result.artifact_ids)

    if exec_result.status == "completed":
        pending_task.status = RunState.COMPLETED
        result.task_status = "completed"
        if exec_result.safe_summary:
            pending_task.inputs["execution_summary"] = exec_result.safe_summary[:200]
        if exec_result.artifact_ids:
            pending_task.inputs["execution_artifact_ids"] = exec_result.artifact_ids
        pending_task.inputs["execution_provider"] = exec_result.provider
    elif exec_result.status == "blocked":
        pending_task.status = RunState.FAILED
        result.task_status = "blocked"
        result.blocked_reason = exec_result.blocked_reason[:200]
        pending_task.inputs["blocked_reason"] = exec_result.blocked_reason[:200]
    else:
        pending_task.status = RunState.FAILED
        result.task_status = "failed"
        result.blocked_reason = (exec_result.outcome or "unknown")[:200]
        pending_task.inputs["blocked_reason"] = (exec_result.outcome or "unknown")[:200]

    save_job(job, root)

    if writer:
        end_event = f"task_execution_{exec_result.status}"
        end_meta = {
            **event_meta,
            "work_performed": exec_result.work_performed,
            "exec_status": exec_result.status,
            "artifact_count": len(exec_result.artifact_ids),
            "token_count": exec_result.token_count,
            "duration_ms": exec_result.duration_ms,
        }
        writer.log(end_event, task_id=task_id_str, outcome=exec_result.status, **end_meta)

    if exec_result.status == "completed":
        remaining = sum(
            1 for t in job.tasks
            if (t.status.value if hasattr(t.status, "value") else str(t.status)) == "pending"
        )
        if remaining == 0:
            transition_state(entry.job_id, "completed", data_dir)
            result.last_lifecycle_state = "completed"
            result.jobs_processed = 1
        else:
            transition_state(entry.job_id, "queued", data_dir)
            release_lease(entry.job_id, data_dir)
            result.last_lifecycle_state = "queued"
        result.action_taken = "task_completed"
        result.why_it_stopped = "task_done"
    else:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason=result.blocked_reason or "execution_failed")
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = result.blocked_reason or "execution_failed"

    result.duration_ms = int((time.monotonic() - start) * 1000)
    return result


def _run_via_legacy_autorun(
    entry: QueueEntry,
    provider: str,
    data_dir: str | Path,
    result: WorkerResult,
    start: float,
) -> WorkerResult:
    """Legacy autorun path for providers not yet on task_execution port."""
    try:
        from packages.orchestration.autorun import run_autorun
        from packages.orchestration.storage import JobNotFoundError, load_job
        job = load_job(entry.job_id)
        ar = run_autorun(job, builder_provider=provider, data_dir=str(data_dir))
        stage = ar.stage if hasattr(ar, "stage") else ""
        stop = ar.stop_reason if hasattr(ar, "stop_reason") else ""
        intent_id = getattr(ar, "intent_id", "") or ""

        if stop == "approval_required" and intent_id:
            transition_state(entry.job_id, "waiting_for_approval", data_dir, blocked_reason="approval_required")
            result.last_lifecycle_state = "waiting_for_approval"
            result.action_taken = "stopped_for_approval"
            result.why_it_stopped = "approval_required"
            result.next_command = f"remedy patch approve {entry.job_id[:8]} {intent_id}"
        elif stop == "approval_required":
            transition_state(entry.job_id, "blocked", data_dir, blocked_reason="approval_required_no_intent")
            result.last_lifecycle_state = "blocked"
            result.action_taken = "blocked"
            result.why_it_stopped = "approval_required_no_intent"
        else:
            lc, action, why = _map_result_to_lifecycle(provider, stage, stop)
            transition_state(entry.job_id, lc, data_dir, blocked_reason=why if lc == "blocked" else "")
            result.last_lifecycle_state = lc
            result.action_taken = action
            result.why_it_stopped = why
            if lc == "completed":
                result.jobs_processed = 1
    except JobNotFoundError:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason="job_not_found")
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = "job_not_found"
    except ImportError:
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason="missing_dependency")
        result.last_lifecycle_state = "blocked"
        result.action_taken = "blocked"
        result.why_it_stopped = "missing_dependency"
    result.duration_ms = int((time.monotonic() - start) * 1000)
    return result


def run_worker_once(
    data_dir: str | Path,
    *,
    worker_id: str = "",
    job_id: str = "",
    provider: str = "none",
    max_steps: int = 1,
    max_tokens: int = 0,
    max_runtime_seconds: int = 60,
) -> WorkerResult:
    """Run one safe unit of work. Returns immediately."""
    if not worker_id:
        worker_id = f"worker-{uuid4().hex[:8]}"

    start = time.monotonic()
    result = WorkerResult(worker_id=worker_id)

    err = validate_provider(provider)
    if err:
        result.action_taken = "error"
        result.why_it_stopped = err
        result.duration_ms = int((time.monotonic() - start) * 1000)
        return result

    detect_stale(data_dir)

    if job_id:
        entry = _load_entry(data_dir, job_id)
        if entry is None:
            entry = enqueue_job(job_id, data_dir)
    else:
        entry = get_next_job(data_dir)

    if entry is None:
        result.action_taken = "idle"
        result.why_it_stopped = "no_queued_jobs"
        result.next_command = "remedy job enqueue <job_id>"
        result.duration_ms = int((time.monotonic() - start) * 1000)
        return result

    lease = claim_job(entry.job_id, worker_id, data_dir)
    if lease is None:
        result.action_taken = "idle"
        result.why_it_stopped = "claim_failed"
        result.next_command = "remedy worker status"
        result.duration_ms = int((time.monotonic() - start) * 1000)
        return result

    result.last_job_id = entry.job_id
    transition_state(entry.job_id, "running", data_dir)

    entry = _load_entry(data_dir, entry.job_id)
    if entry and entry.cancel_requested:
        transition_state(entry.job_id, "cancelled", data_dir)
        result.last_lifecycle_state = "cancelled"
        result.action_taken = "cancelled"
        result.why_it_stopped = "cancel_requested"
        result.duration_ms = int((time.monotonic() - start) * 1000)
        return result

    if provider == "none":
        transition_state(entry.job_id, "blocked", data_dir, blocked_reason="no_worker_selected")
        release_lease(entry.job_id, data_dir)
        result.last_lifecycle_state = "blocked"
        result.action_taken = "no_work_performed"
        result.why_it_stopped = "no_worker_selected"
        result.next_command = f"remedy worker run --once --provider fixture --job {entry.job_id[:8]}"
    elif provider in _TASK_EXEC_PROVIDERS:
        result = _run_via_task_execution(
            entry, provider, data_dir, worker_id, start, result,
            max_steps=max_steps, max_tokens=max_tokens, max_runtime_seconds=max_runtime_seconds,
        )
    elif provider == "ollama":
        result = _run_via_legacy_autorun(entry, provider, data_dir, result, start)

    result.duration_ms = int((time.monotonic() - start) * 1000)

    status = WorkerStatus(
        worker_id=worker_id,
        current_job_id="" if result.last_lifecycle_state in ("completed", "failed", "cancelled", "blocked") else entry.job_id,
        lifecycle_state=result.last_lifecycle_state or "idle",
        heartbeat_at=_now_iso(),
        last_action=result.action_taken,
        why_it_stopped=result.why_it_stopped,
        processed_job_count=result.jobs_processed,
        started_at=_now_iso(),
    )
    _save_worker_status(data_dir, status)

    return result


def run_worker_loop(
    data_dir: str | Path,
    *,
    worker_id: str = "",
    provider: str = "none",
    max_jobs: int = 1,
    max_seconds: int = 60,
    idle_timeout: int = 10,
) -> WorkerResult:
    """Run bounded worker loop. Stops on limit, idle, or cancel."""
    if not worker_id:
        worker_id = f"worker-{uuid4().hex[:8]}"

    start = time.monotonic()
    total_processed = 0
    last_result = WorkerResult(worker_id=worker_id)

    for _ in range(max_jobs):
        elapsed = time.monotonic() - start
        if elapsed >= max_seconds:
            last_result.why_it_stopped = "max_seconds_reached"
            break

        result = run_worker_once(data_dir, worker_id=worker_id, provider=provider)
        if result.action_taken == "idle":
            time.sleep(min(idle_timeout, max(0, max_seconds - elapsed)))
            last_result.why_it_stopped = "idle_timeout"
            break

        total_processed += result.jobs_processed
        last_result = result

    last_result.jobs_processed = total_processed
    last_result.duration_ms = int((time.monotonic() - start) * 1000)
    if not last_result.why_it_stopped:
        last_result.why_it_stopped = "max_jobs_reached"
    return last_result


def export_worker_result_json(result: WorkerResult) -> dict[str, Any]:
    return {
        "worker_id": result.worker_id,
        "jobs_processed": result.jobs_processed,
        "last_job_id": result.last_job_id,
        "last_task_id": result.last_task_id,
        "last_lifecycle_state": result.last_lifecycle_state,
        "action_taken": result.action_taken,
        "why_it_stopped": result.why_it_stopped,
        "next_command": result.next_command,
        "duration_ms": result.duration_ms,
        "provider": result.provider,
        "work_performed": result.work_performed,
        "task_status": result.task_status,
        "artifact_ids": result.artifact_ids,
        "blocked_reason": result.blocked_reason,
        "budget_status": result.budget_status,
        "redaction": result.redaction,
    }


def export_worker_status_json(status: WorkerStatus) -> dict[str, Any]:
    return {
        "worker_id": status.worker_id,
        "current_job_id": status.current_job_id,
        "lifecycle_state": status.lifecycle_state,
        "heartbeat_at": status.heartbeat_at,
        "last_action": status.last_action,
        "why_it_stopped": status.why_it_stopped,
        "processed_job_count": status.processed_job_count,
        "started_at": status.started_at,
        "stale": status.stale,
        "redaction": status.redaction,
    }


def export_queue_entry_json(entry: QueueEntry) -> dict[str, Any]:
    return {
        "job_id": entry.job_id,
        "lifecycle_state": entry.lifecycle_state,
        "queued_at": entry.queued_at,
        "worker_id": entry.worker_id,
        "blocked_reason": entry.blocked_reason,
        "pause_requested": entry.pause_requested,
        "cancel_requested": entry.cancel_requested,
    }
