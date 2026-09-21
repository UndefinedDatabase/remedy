"""Event group command handlers."""

from __future__ import annotations

import json as _json
from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import fail

if TYPE_CHECKING:
    import argparse


def _load_job_events(job_id_str: str, *, json_output: bool = False):
    """Load job and events, exit on error. Returns (job, events, job_id_str)."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan
    from packages.orchestration.timeline import load_run_events

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    try:
        job = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)

    data_dir = resolve_data_root()
    events = load_run_events(data_dir, job_id)
    return job, events, job_id_str


def _cmd_event_list(
    job_id_str: str,
    *,
    event_type: str | None = None,
    since: str | None = None,
    limit: str | None = "50",
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    until: str | None = None,
) -> None:
    from packages.orchestration.event_ledger import (
        export_ledger_event_json,
        list_events,
    )
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    _job, events, jid = _load_job_events(job_id_str, json_output=json_output)
    # Every row of the requested type first; the shared helper then filters by
    # time, orders newest-first and caps — so --limit keeps the NEWEST events.
    result = list_events(jid, events, event_type=event_type, limit=len(events) + 1)
    try:
        result = apply_list_options(
            result,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "timestamp": lambda e: e.timestamp,
                "event_type": lambda e: e.event_type,
                "outcome": lambda e: e.outcome or "",
            },
            default_sort_field="timestamp",
            date_getter=lambda e: e.timestamp or None,
        )
    except ListOptionError as exc:
        fail("invalid_list_option", str(exc), json_output=json_output)

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

    _job, events, jid = _load_job_events(job_id_str, json_output=json_output)
    event = get_event(jid, events, event_id)

    if event is None:
        fail("event_not_found", f"event not found: {event_id}", json_output=json_output)

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

    _job, events, jid = _load_job_events(job_id_str, json_output=json_output)
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


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "event.list": lambda args: _cmd_event_list(
        args.job_id,
        event_type=getattr(args, "type", None),
        since=getattr(args, "since", None),
        limit=getattr(args, "limit", "50"),
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        until=getattr(args, "until", None),
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
