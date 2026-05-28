"""Memory group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable

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
    json_output: bool = False,
) -> None:
    from packages.memory.local_gateway import recall_memory

    entries = recall_memory(
        project_id=project_id,
        job_id=job_id,
        keyword=keyword,
    )

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "tags": e.tags, "approved": e.approved,
                "source_type": e.source_type,
                "created_at": e.created_at,
            }
            for e in entries
        ]
        print(_json.dumps({"entries": output, "count": len(output)}, sort_keys=True))
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
                "tags": e.tags, "approved": e.approved,
                "source_type": e.source_type,
                "created_at": e.created_at,
            }
            for e in entries
        ]
        print(_json.dumps({"entries": output, "count": len(output)}, sort_keys=True))
    else:
        if not entries:
            scope = f"project={project_id}" if project_id else (f"job={job_id}" if job_id else "global")
            print(f"No memory entries ({scope}).")
            return
        for e in entries:
            approved_mark = " [approved]" if e.approved else ""
            tags_str = f" tags={','.join(e.tags)}" if e.tags else ""
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]})")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "memory.store": lambda args: _cmd_memory_store(
        args.key, args.value,
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        tags=getattr(args, "tags", None),
        approved=getattr(args, "approved", "false") == "true",
    ),
    "memory.recall": lambda args: _cmd_memory_recall(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        keyword=getattr(args, "keyword", None),
        json_output=getattr(args, "json", False),
    ),
    "memory.list": lambda args: _cmd_memory_list(
        project_id=getattr(args, "project", None),
        job_id=getattr(args, "job", None),
        json_output=getattr(args, "json", False),
    ),
}
