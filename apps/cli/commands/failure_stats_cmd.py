"""`remedy stats failures` — the failure histogram, read from the evidence on disk (F010).

Read-only: it opens post-mortems and counts them. It starts nothing, writes nothing and
calls no provider. When there is nothing to report it says so, and it always prints the
coverage line — because "no failures recorded" and "we never recorded anything" are very
different sentences and only one of them is good news.
"""
from __future__ import annotations

import json as _json
import sys
from datetime import datetime

EXIT_USAGE = 2
EXIT_ERROR = 1


def _validate_since(raw: str) -> str:
    """Same ``--since`` language the event ledger already speaks: an ISO-8601 timestamp."""
    text = (raw or "").strip()
    if not text:
        return ""
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        print(
            f"Error: --since {raw!r} is not an ISO-8601 timestamp "
            f"(e.g. 2026-07-13 or 2026-07-13T12:00:00+00:00)",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_USAGE) from None
    return text


def _cmd_stats_failures(*, job: str = "", since: str = "",
                        project: str | None = None,
                        all_projects: bool = False,
                        json_output: bool = False) -> None:
    from packages.orchestration.failure_stats import (
        FailureStatsError,
        collect_failures,
        render_human,
    )

    since = _validate_since(since)

    scoped_ids = None
    if not job:
        from packages.orchestration.project_scope import resolve_scope, scoped_jobs
        scope = resolve_scope(project_flag=project, all_projects=all_projects)
        if not scope.all_projects:
            jobs, _degraded, _skipped = scoped_jobs(scope)
            scoped_ids = {str(j.id) for j in jobs}

    try:
        result = collect_failures(job=job or "", since=since, job_ids=scoped_ids)
    except FailureStatsError as exc:
        # An unreadable evidence root is not "no failures". Saying so would be the exact
        # lie this feature exists to prevent.
        if json_output:
            print(_json.dumps({"ok": False, "error": str(exc)}, indent=2))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR)

    if json_output:
        print(_json.dumps(result, indent=2))
    else:
        print(render_human(result))


COMMAND_HANDLERS = {
    "stats.failures": lambda args: _cmd_stats_failures(
        job=getattr(args, "job", "") or "",
        since=getattr(args, "since", "") or "",
        project=getattr(args, "project", None),
        all_projects=getattr(args, "all_projects", False),
        json_output=getattr(args, "json", False),
    ),
}
