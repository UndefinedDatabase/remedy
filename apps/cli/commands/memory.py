"""Memory group command handlers."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_memory_store(
    key: str,
    value: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    tags: str | None = None,
    approved: bool = False,
) -> None:
    from packages.memory.local_gateway import store_memory

    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    entry = store_memory(
        key=key,
        value=value,
        project_id=project_id,
        job_id=job_id,
        tags=tag_list,
        approved=approved,
    )
    print(f"Stored: {entry.id} key={entry.key}")


def _cmd_memory_recall(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    keyword: str | None = None,
    limit: int = 5,
    json_output: bool = False,
) -> None:
    from packages.memory.local_gateway import recall_memory

    entries = recall_memory(
        project_id=project_id,
        job_id=job_id,
        keyword=keyword,
        max_results=limit,
    )

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
            }
            for e in entries
        ]
        print(_json.dumps({"version": 1, "entries": output, "count": len(output)}, sort_keys=True))
    else:
        if not entries:
            scope = f"project={project_id}" if project_id else (f"job={job_id}" if job_id else "global")
            print(f"No memory entries found ({scope}).")
            return
        for e in entries:
            approved_mark = " [approved]" if e.approved else ""
            print(f"  {e.key}: {e.value}{approved_mark}  (id={str(e.id)[:8]})")


def _cmd_memory_list(
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    json_output: bool = False,
) -> None:
    from packages.memory.local_gateway import list_memory

    entries = list_memory(project_id=project_id, job_id=job_id)

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
                "updated_at": e.updated_at,
            }
            for e in entries
        ]
        print(_json.dumps({"version": 1, "entries": output, "count": len(output)}, sort_keys=True))
    else:
        if not entries:
            scope = f"project={project_id}" if project_id else (f"job={job_id}" if job_id else "global")
            print(f"No memory entries ({scope}).")
            return
        for e in entries:
            approved_mark = " [approved]" if e.approved else ""
            tags_str = f" tags={','.join(e.tags)}" if e.tags else ""
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]}, created={e.created_at}, updated={e.updated_at})")


def _cmd_memory_learn(
    job_id_str: str,
    *,
    approved: bool = False,
    json_output: bool = False,
) -> None:
    from uuid import UUID

    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.memory_learn import export_learn_json, learn_from_job
    from packages.orchestration.run_log import RunLogWriter
    from packages.orchestration.timeline import load_run_events

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job.id)
    result = learn_from_job(job, events, approved=approved)

    if json_output:
        print(_json.dumps(export_learn_json(result), sort_keys=True))
    else:
        print(f"Memory learn: {result.learned_count} created, {result.skipped_count} skipped")
        for e in result.entries:
            print(f"  {e['key']} = {e['value']} ({e['status']})")

    log = RunLogWriter(job_id=job.id)
    log.log(
        "memory_learned",
        learned_count=result.learned_count,
        skipped_count=result.skipped_count,
        approved=approved,
        source_count=len(result.entries),
    )


def _cmd_memory_card_show(
    memory_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
    json_output: bool = False,
) -> None:
    from packages.memory.local_gateway import get_memory_card

    card = get_memory_card(memory_id, project_id=project_id, job_id=job_id)
    if card is None:
        print(f"Error: memory card not found: {memory_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "id": str(card.id), "key": card.key, "value": card.value,
            "summary": card.summary, "tags": card.tags,
            "source_type": card.source_type, "source_id": card.source_id,
            "scope": card.scope, "validity": card.validity,
            "review_status": card.review_status, "approved": card.approved,
            "evidence_refs": card.evidence_refs,
            "supersedes": card.supersedes, "contradicts": card.contradicts,
            "created_at": card.created_at, "updated_at": card.updated_at,
        }, sort_keys=True))
    else:
        print(f"Memory Card: {card.id}")
        print(f"  key: {card.key}")
        print(f"  value: {card.value}")
        print(f"  summary: {card.summary}")
        print(f"  validity: {card.validity}  review: {card.review_status}  approved: {card.approved}")
        print(f"  source: {card.source_type}  scope: {card.scope}")
        if card.evidence_refs:
            print(f"  evidence: {', '.join(card.evidence_refs)}")


def _cmd_memory_card_approve(
    memory_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    from packages.memory.local_gateway import approve_memory_card

    card = approve_memory_card(memory_id, project_id=project_id, job_id=job_id)
    if card is None:
        print(f"Error: memory card not found: {memory_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Approved: {card.id} key={card.key}")


def _cmd_memory_card_reject(
    memory_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    from packages.memory.local_gateway import reject_memory_card

    card = reject_memory_card(memory_id, project_id=project_id, job_id=job_id)
    if card is None:
        print(f"Error: memory card not found: {memory_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Rejected: {card.id} key={card.key}")


def _cmd_memory_card_stale(
    memory_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    from packages.memory.local_gateway import mark_stale

    card = mark_stale(memory_id, project_id=project_id, job_id=job_id)
    if card is None:
        print(f"Error: memory card not found: {memory_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Marked stale: {card.id} key={card.key}")


def _cmd_memory_card_supersede(
    old_id: str,
    new_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    from packages.memory.local_gateway import supersede_memory_card

    old, new = supersede_memory_card(old_id, new_id, project_id=project_id, job_id=job_id)
    if old is None:
        print(f"Error: old memory card not found: {old_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Superseded: {old_id[:8]} by {new_id[:8]}")


def _cmd_memory_card_contradict(
    memory_id: str,
    by_id: str,
    *,
    project_id: str | None = None,
    job_id: str | None = None,
) -> None:
    from packages.memory.local_gateway import contradict_memory_card

    contradicted, by = contradict_memory_card(
        memory_id, by_id, project_id=project_id, job_id=job_id,
    )
    if contradicted is None:
        print(f"Error: memory card not found: {memory_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Contradicted: {memory_id[:8]} by {by_id[:8]}")


def _cmd_memory_candidates(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    """List memory candidates for a job."""
    from uuid import UUID

    from packages.orchestration.memory_candidates import list_candidates
    from packages.orchestration.storage import load_job

    job = load_job(UUID(job_id_str))
    candidates = list_candidates(job)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": str(job.id),
            "candidates": candidates,
        }, indent=2))
    else:
        if not candidates:
            print("No memory candidates.")
            return
        for c in candidates:
            status = c.get("status", "?")
            kind = c.get("kind", "?")
            summary = c.get("safe_summary", "?")[:60]
            cid = c.get("id", "?")
            print(f"  [{status}] {cid}  {kind}: {summary}")


def _cmd_memory_approve_candidate(
    job_id_str: str,
    candidate_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Approve a memory candidate."""
    from uuid import UUID

    from packages.orchestration.memory_candidates import approve_candidate
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(job_id_str))
    ok = approve_candidate(job, candidate_id)
    if ok:
        save_job(job)
        if json_output:
            print(_json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "candidate_id": candidate_id,
                "approved": True,
                "memory_created": True,
            }, indent=2))
        else:
            print(f"Approved: {candidate_id}")
    else:
        if json_output:
            print(_json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "candidate_id": candidate_id,
                "approved": False,
                "memory_created": False,
                "error": "not found or already resolved",
            }, indent=2))
        else:
            print(f"Not found or already resolved: {candidate_id}", file=sys.stderr)
        sys.exit(1)


def _cmd_memory_reject_candidate(
    job_id_str: str,
    candidate_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Reject a memory candidate."""
    from uuid import UUID

    from packages.orchestration.memory_candidates import reject_candidate
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(job_id_str))
    ok = reject_candidate(job, candidate_id)
    if ok:
        save_job(job)
        if json_output:
            print(_json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "candidate_id": candidate_id,
                "rejected": True,
                "memory_created": False,
            }, indent=2))
        else:
            print(f"Rejected: {candidate_id}")
    else:
        if json_output:
            print(_json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "candidate_id": candidate_id,
                "rejected": False,
                "memory_created": False,
                "error": "not found or already resolved",
            }, indent=2))
        else:
            print(f"Not found or already resolved: {candidate_id}", file=sys.stderr)
        sys.exit(1)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "memory.store": lambda args: _cmd_memory_store(
        args.key, args.value,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        tags=getattr(args, "tags", None),
        approved=bool(getattr(args, "approved", False)),
    ),
    "memory.recall": lambda args: _cmd_memory_recall(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        keyword=getattr(args, "keyword", None),
        limit=int(getattr(args, "limit", "5")),
        json_output=getattr(args, "json", False),
    ),
    "memory.list": lambda args: _cmd_memory_list(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        json_output=getattr(args, "json", False),
    ),
    "memory.learn": lambda args: _cmd_memory_learn(
        args.job_id,
        approved=bool(getattr(args, "approved", False)),
        json_output=getattr(args, "json", False),
    ),
    "memory.card-show": lambda args: _cmd_memory_card_show(
        args.memory_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        json_output=getattr(args, "json", False),
    ),
    "memory.card-approve": lambda args: _cmd_memory_card_approve(
        args.memory_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
    ),
    "memory.card-reject": lambda args: _cmd_memory_card_reject(
        args.memory_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
    ),
    "memory.card-stale": lambda args: _cmd_memory_card_stale(
        args.memory_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
    ),
    "memory.card-supersede": lambda args: _cmd_memory_card_supersede(
        args.old_id, args.new_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
    ),
    "memory.card-contradict": lambda args: _cmd_memory_card_contradict(
        args.memory_id, args.by_id,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
    ),
    "memory.candidates": lambda args: _cmd_memory_candidates(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "memory.approve-candidate": lambda args: _cmd_memory_approve_candidate(
        args.job_id, args.candidate_id,
        json_output=getattr(args, "json", False),
    ),
    "memory.reject-candidate": lambda args: _cmd_memory_reject_candidate(
        args.job_id, args.candidate_id,
        json_output=getattr(args, "json", False),
    ),
}
