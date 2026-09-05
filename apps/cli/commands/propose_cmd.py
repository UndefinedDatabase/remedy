"""
CLI handlers for ``remedy propose`` commands — proposed task evaluation lifecycle.

List, show, evaluate, approve, reject, defer, materialize proposed tasks.
All output is safe (no raw source/model/prompt content).
"""

from __future__ import annotations

import json
import sys
from typing import Any
from uuid import UUID

_MAX_REASON_LEN = 200
_MAX_NOTES_DISPLAY = 200


def _safe_text(text: str, limit: int = 80) -> str:
    if not text:
        return ""
    return text[:limit]


def _make_writer(job_id: str) -> Any:
    """Create a RunLogWriter for audit events. Returns None if job_id is not a valid UUID."""
    try:
        from packages.orchestration.run_log import RunLogWriter
        uid = UUID(job_id)
        return RunLogWriter(uid)
    except (ValueError, TypeError, ImportError, OSError):
        return None


def _require_job(job_id: str, args: Any) -> bool:
    """Validate that a real Job exists for mutating commands.

    Returns True if job exists, False + printed error if not.
    """
    try:
        from packages.orchestration.storage import JobNotFoundError, JobStoreError, load_job
        uid = UUID(job_id)
        load_job(uid)
        return True
    except (ValueError, TypeError):
        msg = f"Invalid job ID: {job_id}"
    except JobNotFoundError:
        msg = f"Job not found: {job_id}"
    except JobStoreError:
        msg = f"Job store is unreadable for: {job_id}"
    except ImportError:
        msg = "Job storage module unavailable"

    if getattr(args, "json", False):
        print(json.dumps({"version": 1, "error": msg}))
    else:
        print(msg, file=sys.stderr)
    return False


def _task_to_safe_dict(t: Any) -> dict[str, Any]:
    return {
        "id": t.id,
        "title": _safe_text(t.title, 80),
        "status": t.status.value if hasattr(t.status, "value") else str(t.status),
        "source": t.source.value if hasattr(t.source, "value") else str(t.source),
        "risk": t.risk,
        "priority": t.priority,
        "task_type": t.task_type,
        "approval_required": t.approval_required,
        "evaluation_notes": _safe_text(t.evaluation_notes, _MAX_NOTES_DISPLAY),
        "evaluated_by": t.evaluated_by,
        "evaluated_at": str(t.evaluated_at) if t.evaluated_at else None,
        "created_at": str(t.created_at) if t.created_at else None,
        "resolved_at": str(t.resolved_at) if t.resolved_at else None,
        "origin_task_id": t.origin_task_id,
        "origin_recommendation_id": t.origin_recommendation_id,
        "materialized_task_id": getattr(t, "materialized_task_id", "") or "",
        "materialized_at": str(t.materialized_at) if getattr(t, "materialized_at", None) else None,
    }


def _cmd_propose_list(args: Any) -> None:
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStatus,
        ProposedTaskStoreError,
        list_by_status,
        load_proposed_tasks,
    )

    job_id = args.job_id
    status_filter = getattr(args, "status", None)

    try:
        if status_filter:
            try:
                st = ProposedTaskStatus(status_filter)
            except ValueError:
                msg = f"Unknown status: {status_filter}"
                if getattr(args, "json", False):
                    print(json.dumps({"version": 1, "error": msg}))
                else:
                    print(msg, file=sys.stderr)
                sys.exit(1)
            tasks = list_by_status(job_id, st)
        else:
            tasks = load_proposed_tasks(job_id)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.list_options import ListOptionError, apply_list_options
    try:
        tasks = apply_list_options(
            tasks,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda t: t.created_at,
                "status": lambda t: t.status.value if hasattr(t.status, "value") else str(t.status),
                "priority": lambda t: t.priority,
            },
            default_sort_field="created_at",
            date_getter=lambda t: t.created_at.isoformat(),
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "count": len(tasks),
            "tasks": [_task_to_safe_dict(t) for t in tasks],
        }, indent=2))
    else:
        if not tasks:
            print("No proposed tasks.")
            return
        for t in tasks:
            status = t.status.value if hasattr(t.status, "value") else str(t.status)
            print(f"  [{status}] {t.id}  {_safe_text(t.title, 60)}  [{t.risk}]")


def _cmd_propose_show(args: Any) -> None:
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStoreError,
        get_proposed_task,
    )

    job_id = args.job_id
    task_id = args.task_id

    try:
        task = get_proposed_task(job_id, task_id)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if task is None:
        msg = f"Proposed task not found: {task_id}"
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "task": _task_to_safe_dict(task),
        }, indent=2))
    else:
        d = _task_to_safe_dict(task)
        for k, v in d.items():
            if v is not None and v != "":
                print(f"  {k}: {v}")


def _cmd_propose_evaluate(args: Any) -> None:
    if not _require_job(args.job_id, args):
        sys.exit(1)
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStoreError,
        emit_proposed_task_event,
        evaluate_all_proposed,
        evaluate_proposed_task,
    )

    job_id = args.job_id
    task_id = getattr(args, "task_id", None)
    writer = _make_writer(job_id)

    try:
        if task_id:
            result = evaluate_proposed_task(job_id, task_id)
            if result is None:
                msg = f"Proposed task not found: {task_id}"
                if getattr(args, "json", False):
                    print(json.dumps({"version": 1, "error": msg}))
                else:
                    print(msg, file=sys.stderr)
                sys.exit(1)
            emit_proposed_task_event(writer, "proposed_task_evaluated", result)
            tasks = [result]
        else:
            tasks = evaluate_all_proposed(job_id)
            for t in tasks:
                emit_proposed_task_event(writer, "proposed_task_evaluated", t)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "evaluated_count": len(tasks),
            "tasks": [_task_to_safe_dict(t) for t in tasks],
        }, indent=2))
    else:
        if not tasks:
            print("No tasks to evaluate.")
            return
        for t in tasks:
            status = t.status.value if hasattr(t.status, "value") else str(t.status)
            print(f"  [{status}] {t.id}  {_safe_text(t.title, 60)}  — {_safe_text(t.evaluation_notes, 80)}")


def _cmd_propose_approve(args: Any) -> None:
    if not _require_job(args.job_id, args):
        sys.exit(1)
    from packages.orchestration.proposed_tasks import (
        InvalidTransitionError,
        ProposedTaskStoreError,
        approve_proposed_task,
        emit_proposed_task_event,
    )

    job_id = args.job_id
    task_id = args.task_id
    writer = _make_writer(job_id)

    try:
        result = approve_proposed_task(job_id, task_id)
    except InvalidTransitionError as exc:
        msg = str(exc)
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        msg = f"Proposed task not found: {task_id}"
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    emit_proposed_task_event(writer, "proposed_task_approved", result)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "task_id": task_id,
            "approved": True,
            "task": _task_to_safe_dict(result),
        }, indent=2))
    else:
        print(f"Approved: {task_id}")


def _cmd_propose_reject(args: Any) -> None:
    if not _require_job(args.job_id, args):
        sys.exit(1)
    from packages.orchestration.proposed_tasks import (
        InvalidTransitionError,
        ProposedTaskStoreError,
        emit_proposed_task_event,
        reject_proposed_task,
    )

    job_id = args.job_id
    task_id = args.task_id
    reason = _safe_text(getattr(args, "reason", "") or "", _MAX_REASON_LEN)
    writer = _make_writer(job_id)

    try:
        result = reject_proposed_task(job_id, task_id, reason=reason)
    except InvalidTransitionError as exc:
        msg = str(exc)
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        msg = f"Proposed task not found: {task_id}"
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    emit_proposed_task_event(writer, "proposed_task_rejected", result)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "task_id": task_id,
            "rejected": True,
            "task": _task_to_safe_dict(result),
        }, indent=2))
    else:
        print(f"Rejected: {task_id}")


def _cmd_propose_defer(args: Any) -> None:
    if not _require_job(args.job_id, args):
        sys.exit(1)
    from packages.orchestration.proposed_tasks import (
        InvalidTransitionError,
        ProposedTaskStoreError,
        defer_proposed_task,
        emit_proposed_task_event,
    )

    job_id = args.job_id
    task_id = args.task_id
    reason = _safe_text(getattr(args, "reason", "") or "", _MAX_REASON_LEN)
    writer = _make_writer(job_id)

    try:
        result = defer_proposed_task(job_id, task_id, reason=reason)
    except InvalidTransitionError as exc:
        msg = str(exc)
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if result is None:
        msg = f"Proposed task not found: {task_id}"
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    emit_proposed_task_event(writer, "proposed_task_deferred", result)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "task_id": task_id,
            "deferred": True,
            "task": _task_to_safe_dict(result),
        }, indent=2))
    else:
        print(f"Deferred: {task_id}")


def _cmd_propose_materialize(args: Any) -> None:
    if not _require_job(args.job_id, args):
        sys.exit(1)
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStoreError,
        do_materialize,
        emit_proposed_task_event,
        list_approved_not_materialized,
    )

    job_id = args.job_id
    task_id = getattr(args, "task_id", None)
    do_all = getattr(args, "all", False)
    writer = _make_writer(job_id)

    try:
        if task_id:
            result = do_materialize(job_id, task_id)
            if result is None:
                msg = f"Proposed task not found: {task_id}"
                if getattr(args, "json", False):
                    print(json.dumps({"version": 1, "error": msg}))
                else:
                    print(msg, file=sys.stderr)
                sys.exit(1)
            emit_proposed_task_event(writer, "proposed_task_materialized", result)
            results = [result]
        elif do_all:
            pending = list_approved_not_materialized(job_id)
            results = []
            for pt in pending:
                r = do_materialize(job_id, pt.id)
                if r:
                    emit_proposed_task_event(writer, "proposed_task_materialized", r)
                    results.append(r)
        else:
            msg = "Specify --task-id or --all"
            if getattr(args, "json", False):
                print(json.dumps({"version": 1, "error": msg}))
            else:
                print(msg, file=sys.stderr)
            sys.exit(1)
    except ValueError as exc:
        msg = str(exc)
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": msg}))
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)
    except ProposedTaskStoreError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"version": 1, "error": "Proposed task store is unreadable.", "degraded": True}))
        else:
            print(f"Proposed task store is unreadable: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": job_id,
            "materialized_count": len(results),
            "tasks": [_task_to_safe_dict(t) for t in results],
        }, indent=2))
    else:
        if not results:
            print("No tasks to materialize.")
            return
        for t in results:
            print(f"  Materialized: {t.id} → task {t.materialized_task_id}")


COMMAND_HANDLERS = {
    "propose.list": lambda args: _cmd_propose_list(args),
    "propose.show": lambda args: _cmd_propose_show(args),
    "propose.evaluate": lambda args: _cmd_propose_evaluate(args),
    "propose.approve": lambda args: _cmd_propose_approve(args),
    "propose.reject": lambda args: _cmd_propose_reject(args),
    "propose.defer": lambda args: _cmd_propose_defer(args),
    "propose.materialize": lambda args: _cmd_propose_materialize(args),
}
