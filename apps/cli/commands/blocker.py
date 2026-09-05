"""Blocker group command handlers (stop reasons)."""

from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_blocker_list(
    job_id_str: str,
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.stop_reasons import (
        export_stop_reason_json,
        list_stop_reasons,
    )

    stops = list_stop_reasons(job_id_str)
    try:
        stops = apply_list_options(
            stops,
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "created_at": lambda s: s.created_at,
                "status": lambda s: s.status,
                "severity": lambda s: s.severity,
            },
            default_sort_field="created_at",
            date_getter=lambda s: s.created_at or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": job_id_str,
            "stop_reasons": [export_stop_reason_json(s) for s in stops],
        }, sort_keys=True))
    else:
        if not stops:
            print(f"No blockers for job {job_id_str[:8]}.")
            return
        for s in stops:
            status_mark = "[resolved]" if s.status == "resolved" else "[active]"
            resolved_str = f", resolved={s.resolved_at}" if s.resolved_at else ""
            print(f"  {s.reason_code} {status_mark}  {s.safe_summary}  (id={s.id[:8]}, created={s.created_at}{resolved_str})")


def _cmd_blocker_show(
    job_id_str: str,
    stop_id: str,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.stop_reasons import (
        export_stop_reason_json,
        get_stop_reason,
    )

    sr = get_stop_reason(job_id_str, stop_id)
    if sr is None:
        print(f"Error: blocker not found: {stop_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": job_id_str,
            "stop_reason": export_stop_reason_json(sr),
        }, sort_keys=True))
    else:
        print(f"Blocker: {sr.id}")
        print(f"  Code: {sr.reason_code}")
        print(f"  Severity: {sr.severity}")
        print(f"  Status: {sr.status}")
        print(f"  Summary: {sr.safe_summary}")
        if sr.next_actions:
            print("  Next actions:")
            for a in sr.next_actions:
                print(f"    - {a}")


def _cmd_blocker_resolve(
    job_id_str: str,
    stop_id: str,
    *,
    reason: str | None = None,
) -> None:
    from packages.orchestration.stop_reasons import resolve_stop_reason

    sr = resolve_stop_reason(job_id_str, stop_id, reason or "manually resolved")
    if sr is None:
        print(f"Error: blocker not found: {stop_id}", file=sys.stderr)
        sys.exit(1)
    print(f"Resolved: {sr.id[:8]} ({sr.reason_code})")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "blocker.list": lambda args: _cmd_blocker_list(
        args.job_id,
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "blocker.show": lambda args: _cmd_blocker_show(
        args.job_id,
        args.stop_id,
        json_output=getattr(args, "json", False),
    ),
    "blocker.resolve": lambda args: _cmd_blocker_resolve(
        args.job_id,
        args.stop_id,
        reason=getattr(args, "reason", None),
    ),
}
