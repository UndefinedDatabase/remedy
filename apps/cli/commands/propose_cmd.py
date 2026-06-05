"""
CLI handlers for ``remedy propose`` commands — proposed task evaluation lifecycle.

List, show, evaluate, approve, reject, defer proposed tasks.
All output is safe (no raw source/model/prompt content).
"""

from __future__ import annotations

import json
import sys
from typing import Any


_MAX_REASON_LEN = 200
_MAX_NOTES_DISPLAY = 200


def _safe_text(text: str, limit: int = 80) -> str:
    if not text:
        return ""
    return text[:limit]


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
    }


def _cmd_propose_list(args: Any) -> None:
    from packages.orchestration.proposed_tasks import (
        load_proposed_tasks,
        list_by_status,
        ProposedTaskStatus,
        ProposedTaskStoreError,
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
        get_proposed_task,
        ProposedTaskStoreError,
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
    from packages.orchestration.proposed_tasks import (
        evaluate_proposed_task,
        evaluate_all_proposed,
        emit_proposed_task_event,
        ProposedTaskStoreError,
    )

    job_id = args.job_id
    task_id = getattr(args, "task_id", None)

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
            emit_proposed_task_event(None, "proposed_task_evaluated", result)
            tasks = [result]
        else:
            tasks = evaluate_all_proposed(job_id)
            for t in tasks:
                emit_proposed_task_event(None, "proposed_task_evaluated", t)
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
    from packages.orchestration.proposed_tasks import (
        approve_proposed_task,
        emit_proposed_task_event,
        InvalidTransitionError,
        ProposedTaskStoreError,
    )

    job_id = args.job_id
    task_id = args.task_id

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

    emit_proposed_task_event(None, "proposed_task_approved", result)

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
    from packages.orchestration.proposed_tasks import (
        reject_proposed_task,
        emit_proposed_task_event,
        InvalidTransitionError,
        ProposedTaskStoreError,
    )

    job_id = args.job_id
    task_id = args.task_id
    reason = _safe_text(getattr(args, "reason", "") or "", _MAX_REASON_LEN)

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

    emit_proposed_task_event(None, "proposed_task_rejected", result)

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
    from packages.orchestration.proposed_tasks import (
        defer_proposed_task,
        emit_proposed_task_event,
        InvalidTransitionError,
        ProposedTaskStoreError,
    )

    job_id = args.job_id
    task_id = args.task_id
    reason = _safe_text(getattr(args, "reason", "") or "", _MAX_REASON_LEN)

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

    emit_proposed_task_event(None, "proposed_task_deferred", result)

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


COMMAND_HANDLERS = {
    "propose.list": lambda args: _cmd_propose_list(args),
    "propose.show": lambda args: _cmd_propose_show(args),
    "propose.evaluate": lambda args: _cmd_propose_evaluate(args),
    "propose.approve": lambda args: _cmd_propose_approve(args),
    "propose.reject": lambda args: _cmd_propose_reject(args),
    "propose.defer": lambda args: _cmd_propose_defer(args),
}
