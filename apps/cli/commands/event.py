"""Event group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

if TYPE_CHECKING:
    import argparse


def _load_job_events(job_id_str: str):
    """Load job and events, exit on error. Returns (job, events, job_id_str)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import JobNotFoundError, load_job
    from packages.orchestration.timeline import load_run_events

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

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    return job, events, job_id_str


def _cmd_event_list(
    job_id_str: str,
    *,
    event_type: str | None = None,
    since: str | None = None,
    limit: int = 50,
    json_output: bool = False,
) -> None:
    from packages.orchestration.event_ledger import (
        export_ledger_event_json,
        list_events,
    )

    _job, events, jid = _load_job_events(job_id_str)
    result = list_events(jid, events, event_type=event_type, since=since, limit=limit)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "events": [export_ledger_event_json(e) for e in result],
        }, sort_keys=True))
    else:
        if not result:
            print(f"No events for job {jid[:8]}.")
            return
        for e in result:
            outcome_str = f" [{e.outcome}]" if e.outcome else ""
            print(f"  {e.timestamp[:19]}  {e.event_type}{outcome_str}  (id={e.event_id[:8]})")


def _cmd_event_show(
    job_id_str: str,
    event_id: str,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.event_ledger import (
        export_ledger_event_json,
        get_event,
    )

    _job, events, jid = _load_job_events(job_id_str)
    event = get_event(jid, events, event_id)

    if event is None:
        print(f"Error: event not found: {event_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": jid,
            "event": export_ledger_event_json(event),
        }, sort_keys=True))
    else:
        print(f"Event: {event.event_id}")
        print(f"  Type: {event.event_type}")
        print(f"  Time: {event.timestamp}")
        print(f"  Scope: {event.scope}")
        print(f"  Outcome: {event.outcome}")
        if event.metadata:
            for k, v in sorted(event.metadata.items()):
                print(f"  {k}: {v}")


def _cmd_event_timeline(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.event_ledger import (
        build_event_timeline,
        export_event_timeline_json,
    )

    _job, events, jid = _load_job_events(job_id_str)
    timeline = build_event_timeline(jid, events)

    if json_output:
        print(_json.dumps(export_event_timeline_json(timeline), sort_keys=True))
    else:
        print(f"Event Timeline for {jid[:8]} ({timeline.event_count} events)")
        for e in timeline.events:
            outcome_str = f" [{e.outcome}]" if e.outcome else ""
            print(f"  {e.timestamp[:19]}  {e.event_type}{outcome_str}")


def _cmd_event_replay(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.event_replay import (
        export_replay_json,
        replay_job,
    )

    data_dir = resolve_data_root()
    replay = replay_job(job_id_str, data_dir)

    if json_output:
        print(_json.dumps(export_replay_json(replay), indent=2))
    else:
        print(f"Replay: {replay.job_id[:8]}")
        print(f"  Events: {replay.event_count}")
        print(f"  Stage: {replay.current_stage}")
        if replay.provider:
            print(f"  Provider: {replay.provider}")
        if replay.stop_reason:
            print(f"  Stop reason: {replay.stop_reason}")
        if replay.degraded:
            print(f"  Degraded: {replay.degraded_reason}")
        reached = [s.id for s in replay.stages if s.reached]
        if reached:
            print(f"  Reached: {', '.join(reached)}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "event.list": lambda args: _cmd_event_list(
        args.job_id,
        event_type=getattr(args, "type", None),
        since=getattr(args, "since", None),
        limit=int(getattr(args, "limit", "50")),
        json_output=getattr(args, "json", False),
    ),
    "event.show": lambda args: _cmd_event_show(
        args.job_id,
        args.event_id,
        json_output=getattr(args, "json", False),
    ),
    "event.timeline": lambda args: _cmd_event_timeline(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "event.replay": lambda args: _cmd_event_replay(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
}
