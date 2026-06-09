"""CLI handlers for the ``feature`` command group."""

from __future__ import annotations

import json
import sys
from typing import Any


def _build_ledger_and_plan(*, job_id: str = "", use_agent: bool = False) -> tuple:
    """Build ledger + feature plan."""
    from apps.cli.commands import read_agent_file
    from packages.orchestration.feature_planner import build_feature_plan
    from packages.orchestration.progress_ledger import build_progress_ledger

    plan_text = read_agent_file("plan.md")
    live_review_text = read_agent_file("live_review.md")
    context_text = read_agent_file("context.md")

    job = None
    events = None

    if not use_agent and job_id:
        from packages.orchestration.storage import load_job, load_run_events
        job = load_job(job_id)
        events = load_run_events(job_id)

    ledger = build_progress_ledger(
        plan_text=plan_text,
        live_review_text=live_review_text,
        context_text=context_text,
        job=job,
        events=events,
    )
    feature_plan = build_feature_plan(ledger, job=job)
    return ledger, feature_plan


def _cmd_feature_plan(args: Any) -> None:
    """Show deterministic feature suggestions."""
    from packages.orchestration.feature_planner import (
        export_feature_plan_json,
        summarize_feature_plan,
    )

    use_agent = getattr(args, "agent", False)
    job_id = getattr(args, "job_id", "") or ""

    if not use_agent and not job_id:
        print("Error: provide job_id or --agent", file=sys.stderr)
        sys.exit(1)

    try:
        _, feature_plan = _build_ledger_and_plan(job_id=job_id, use_agent=use_agent)
    except Exception as exc:
        print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(export_feature_plan_json(feature_plan), indent=2))
    else:
        print(summarize_feature_plan(feature_plan))


def _cmd_feature_accept(args: Any) -> None:
    """Accept a feature suggestion — creates ProposedTask metadata."""
    from packages.orchestration.feature_planner import accept_feature_suggestion

    job_id = getattr(args, "job_id", "")
    suggestion_id = getattr(args, "suggestion_id", "")

    if not job_id or not suggestion_id:
        print("Error: job_id and suggestion_id are required", file=sys.stderr)
        sys.exit(1)

    try:
        _, feature_plan = _build_ledger_and_plan(job_id=job_id)
    except Exception as exc:
        print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)

    result = accept_feature_suggestion(feature_plan, suggestion_id, job_id)

    if not result.get("accepted"):
        print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2))
    else:
        print(f"Accepted: {result['title']}")
        print(f"Suggestion: {result['suggestion_id']}")
        print(f"Priority: {result['priority']}")
        print(f"Creates ProposedTask: {result['creates_proposed_task']}")
        print(f"Executed: {result['executed']}")


COMMAND_HANDLERS = {
    "feature.plan": lambda args: _cmd_feature_plan(args),
    "feature.accept": lambda args: _cmd_feature_accept(args),
}
