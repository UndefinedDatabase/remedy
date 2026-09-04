"""`remedy queue` — the per-project work queue (F048 T003).

Commands over the file-based queue in ``packages.orchestration.job_queue``: ``add`` puts
work in, ``list`` shows what is there and who holds what, ``rm`` takes an unclaimed entry
back out. Reclaiming a stale claim is its own command (T003b) — explicit, never silent.

Scoping follows F148: the project comes from ``--project``, ``REMEDY_PROJECT`` or the
working directory, exactly as ``remedy job list`` resolves it. There is no cross-project
queue; ``--all-projects`` only widens the LISTING, entry by entry, over the project
queues that exist on disk.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

EXIT_ERROR = 1
EXIT_USAGE = 2
#: The contract's exit code for "no project" — the same one `job create` uses.
EXIT_NO_PROJECT = 3


def _resolve_project_id(project_flag: str | None) -> str:
    """The one project this command acts on, or exit 3 with the same wording as job create."""
    from packages.orchestration.project_registry import (
        ProjectNotFoundError,
        select_project,
    )

    try:
        project, _source = select_project(project_flag, ".")
    except ProjectNotFoundError:
        print(
            "Error: no project found. Run: remedy init\n"
            "  or pass --project <slug-or-id>",
            file=sys.stderr,
        )
        sys.exit(EXIT_NO_PROJECT)
    return str(project.id)


def _looks_like_a_path(text: str) -> bool:
    """A goal that names an existing file is a goal FILE. Anything else is goal text.

    Existence, not spelling: a sentence containing a slash is still a sentence, and a
    typo'd path is better enqueued as text the operator can read back than silently
    treated as a file reference that will never resolve.
    """
    stripped = text.strip()
    if not stripped or "\n" in stripped:
        return False
    try:
        return Path(stripped).expanduser().is_file()
    except OSError:
        return False


def _age(created_at: str, *, now: datetime | None = None) -> str:
    """Compact age for the listing. Unparsable timestamps print as `?` rather than a guess."""
    try:
        stamp = datetime.fromisoformat(created_at)
    except (TypeError, ValueError):
        return "?"
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    seconds = int(((now or datetime.now(timezone.utc)) - stamp).total_seconds())
    if seconds < 0:
        return "?"
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h"
    return f"{seconds // 86400}d"


def _goal_label(entry: Any) -> str:
    text = entry.goal or f"@{entry.goal_path}"
    single_line = text.replace("\n", " ").strip()
    return single_line[:60]


def _cmd_queue_add(goal: str, *, project: str | None = None,
                   prio: str | None = None, path: bool = False) -> None:
    from packages.orchestration.job_queue import QueueError, enqueue

    project_id = _resolve_project_id(project)

    try:
        priority = int(prio) if prio is not None else 0
    except (TypeError, ValueError):
        print(f"Error: --prio must be an integer, got {prio!r}", file=sys.stderr)
        sys.exit(EXIT_USAGE)

    as_path = path or _looks_like_a_path(goal)
    try:
        if as_path:
            entry = enqueue(project_id, goal_path=goal, prio=priority)
        else:
            entry = enqueue(project_id, goal, priority)
    except QueueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    print(entry.id)


def _project_ids_with_a_queue() -> list[str]:
    """Every project directory that actually exists under the queue area.

    Read from disk, not from the registry: a queue whose project was unregistered still
    holds work, and hiding it would make the listing dishonest.
    """
    from packages.orchestration.job_queue import queue_root

    root = queue_root()
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def _cmd_queue_list(*, project: str | None = None, all_projects: bool = False,
                    json_output: bool = False) -> None:
    from packages.orchestration.job_queue import list_entries_safe

    if all_projects:
        project_ids = _project_ids_with_a_queue()
    else:
        project_ids = [_resolve_project_id(project)]

    rows: list[tuple[str, Any]] = []
    skipped_total = 0
    for project_id in project_ids:
        entries, _degraded, skipped = list_entries_safe(project_id)
        skipped_total += len(skipped)
        rows.extend((project_id, entry) for entry in entries)

    if json_output:
        import json as _json
        print(_json.dumps({
            "version": 1,
            "entry_count": len(rows),
            "entries": [{"id": entry.id, "status": entry.status, "priority": entry.priority,
                        "created_at": entry.created_at, "claimed_by": entry.claimed_by or "",
                        "goal": _goal_label(entry), "project_id": project_id}
                       for project_id, entry in rows],
        }, sort_keys=True))
        return

    if not rows:
        print("No queue entries found.")
    for project_id, entry in rows:
        owner = entry.claimed_by or "-"
        label = f"  (project: {project_id[:8]})" if all_projects else ""
        print(f"{entry.id[:12]}  {entry.status:<8}  prio {entry.priority:<4}  "
              f"{_age(entry.created_at):>4}  {owner:<24}  {_goal_label(entry)}{label}")
    if skipped_total:
        print(f"  ({skipped_total} unreadable queue file(s) skipped)", file=sys.stderr)


def _resolve_entry_id(project_id: str, raw: str) -> str:
    """Full id, or a unique prefix — the same affordance job ids have."""
    from packages.orchestration.job_queue import list_entries

    candidate = raw.strip()
    matches = [e.id for e in list_entries(project_id) if e.id.startswith(candidate)]
    if candidate in matches:
        return candidate
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Error: ambiguous queue entry prefix {raw!r} matches {len(matches)} entries:",
              file=sys.stderr)
        for match in sorted(matches):
            print(f"  {match[:12]}", file=sys.stderr)
        sys.exit(EXIT_USAGE)
    return candidate


def _cmd_queue_rm(entry_id: str, *, project: str | None = None) -> None:
    from packages.orchestration.job_queue import (
        QueueEntryClaimedError,
        QueueEntryNotFoundError,
        QueueError,
        remove_entry,
    )

    project_id = _resolve_project_id(project)
    resolved = _resolve_entry_id(project_id, entry_id)
    try:
        entry = remove_entry(project_id, resolved)
    except QueueEntryClaimedError as exc:
        print(f"Error: {exc}. Claimed at {exc.entry.claimed_at or 'an unknown time'}.",
              file=sys.stderr)
        print("  A claimed entry is held by a consumer. Use: remedy queue reclaim "
              f"{exc.entry.id[:12]}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except QueueEntryNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except QueueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    print(f"Removed {entry.id}")


def _cmd_queue_reclaim(entry_id: str, *, project: str | None = None) -> None:
    from packages.orchestration.job_queue import (
        QueueError,
        ReclaimRefusedError,
        reclaim,
        resolve_reclaim_ttl_minutes,
    )

    project_id = _resolve_project_id(project)
    resolved = _resolve_entry_id(project_id, entry_id)
    try:
        entry = reclaim(project_id, resolved)
    except ReclaimRefusedError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("  A reclaim needs BOTH: a claim older than "
              f"{resolve_reclaim_ttl_minutes()} minutes AND an owner that is verifiably "
              "gone. Remedy never takes a claim away on a timer alone.", file=sys.stderr)
        sys.exit(EXIT_ERROR)
    except QueueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    print(f"Reclaimed {entry.id} — back in the queue.")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "queue.add": lambda args: _cmd_queue_add(
        args.goal,
        project=getattr(args, "project", None),
        prio=getattr(args, "prio", None),
        path=getattr(args, "path", False),
    ),
    "queue.list": lambda args: _cmd_queue_list(
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=args.json,
    ),
    "queue.rm": lambda args: _cmd_queue_rm(
        args.entry_id, project=getattr(args, "project", None)),
    "queue.reclaim": lambda args: _cmd_queue_reclaim(
        args.entry_id, project=getattr(args, "project", None)),
}
