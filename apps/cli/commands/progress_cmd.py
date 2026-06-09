"""CLI handlers for the ``progress`` command group."""

from __future__ import annotations

import json
import sys
from typing import Any


def _cmd_progress_checklist(args: Any) -> None:
    """Show structured progress checklist."""
    from apps.cli.commands import read_agent_file
    from packages.orchestration.progress_ledger import (
        build_progress_ledger,
        export_progress_ledger_json,
        summarize_progress_ledger,
    )

    use_agent = getattr(args, "agent", False)
    job_id = getattr(args, "job_id", "") or ""

    plan_text = read_agent_file("plan.md")
    live_review_text = read_agent_file("live_review.md")
    context_text = read_agent_file("context.md")

    job = None
    events = None

    if not use_agent and job_id:
        from packages.orchestration.storage import JobNotFoundError, load_job, load_run_events
        try:
            job = load_job(job_id)
            events = load_run_events(job_id)
        except (JobNotFoundError, Exception) as exc:
            print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
            sys.exit(1)
    elif not use_agent and not job_id:
        print("Error: provide job_id or --agent", file=sys.stderr)
        sys.exit(1)

    ledger = build_progress_ledger(
        plan_text=plan_text,
        live_review_text=live_review_text,
        context_text=context_text,
        job=job,
        events=events,
    )

    if getattr(args, "json", False):
        print(json.dumps(export_progress_ledger_json(ledger), indent=2))
    else:
        print(summarize_progress_ledger(ledger))


COMMAND_HANDLERS = {
    "progress.checklist": lambda args: _cmd_progress_checklist(args),
}
