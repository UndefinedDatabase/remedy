"""CLI handlers for ``remedy self`` — Self-Dogfood Planner v0.

inspect/plan/report are read-only; propose is metadata-only (creates ProposedTasks
through the existing approval flow). No apply, no approval, no execution, no git.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_self_inspect(args: Any) -> None:
    from packages.orchestration.self_dogfood import (
        build_self_dogfood_inspection, export_inspection_json,
    )
    insp = build_self_dogfood_inspection(getattr(args, "job_id", None))
    data = export_inspection_json(insp)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self-dogfood inspect: {data['repository_identity']}")
    print(f"  items: {data['item_count']}  blockers: {len(data['blockers'])}  "
          f"risks: {len(data['risks'])}")
    for it in data["items"][:5]:
        print(f"  - ({it['priority']}) [{it['item_type']}] {it['title']}")
    na = data.get("next_safe_action")
    if na:
        print(f"  next: {na['label']} -> {na['command']}")


def _cmd_self_plan(args: Any) -> None:
    from packages.orchestration.self_dogfood import (
        build_self_improvement_plan, export_plan_json,
    )
    plan = build_self_improvement_plan(getattr(args, "job_id", None))
    data = export_plan_json(plan)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self-improvement plan: {data['item_count']} item(s) in {len(data['groups'])} group(s)")
    for it in data["recommended"]:
        print(f"  - ({it['priority']}) [{it['item_type']}] {it['title']}")


def _cmd_self_propose(args: Any) -> None:
    from packages.orchestration.self_dogfood import (
        propose_self_improvement, export_result_json,
    )
    item_ids = [args.item_id] if getattr(args, "item_id", None) else None
    top = None
    raw_top = getattr(args, "top", None)
    if raw_top is not None:
        try:
            top = int(raw_top)
        except (TypeError, ValueError):
            print("Error: --top must be an integer", file=sys.stderr)
            sys.exit(1)
    result = propose_self_improvement(args.job_id, item_ids=item_ids, top=top)
    data = export_result_json(result)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self-propose: {data['stop_reason']}")
    print(f"  proposed: {len(data['proposed_task_ids'])}  skipped: {len(data['skipped_existing'])}")
    na = data.get("next_safe_action")
    if na:
        print(f"  next: {na['label']} -> {na['command']}")


def _cmd_self_report(args: Any) -> None:
    from packages.orchestration.self_dogfood import (
        build_self_dogfood_report, render_report_markdown,
    )
    from packages.orchestration.self_dogfood_execution import list_attempts
    data = build_self_dogfood_report(getattr(args, "job_id", None))
    attempts = list_attempts()
    data["self_execution_attempts"] = [
        {"attempt_id": a["attempt_id"], "state": a["state"],
         "proposed_task_id": a["proposed_task_id"],
         "next_safe_action": a.get("next_safe_action", "")}
        for a in attempts
    ]
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    md = render_report_markdown(data)
    if attempts:
        md += "\n\n## Active self-improvement attempts\n"
        for a in attempts:
            md += f"- {a['attempt_id'][:8]} [{a['state']}]\n"
    print(md)


def _cmd_self_execute(args: Any) -> None:
    from packages.orchestration.self_dogfood_execution import (
        start_self_execution, export_result_json,
    )
    result = start_self_execution(args.proposed_task_id, getattr(args, "job_id", None))
    data = export_result_json(result)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self execute: {data['state']}  stop: {data['stop_reason']}")
    if data["request_package_id"]:
        print(f"  request: {data['request_package_id']}")
    if data["next_safe_action"]:
        print(f"  next: {data['next_safe_action']}")


def _cmd_self_status(args: Any) -> None:
    from packages.orchestration.self_dogfood_execution import list_attempts, get_attempt
    attempt_id = getattr(args, "attempt_id", None)
    attempts = [get_attempt(attempt_id)] if attempt_id else list_attempts()
    attempts = [a for a in attempts if a]
    if getattr(args, "json", False):
        print(json.dumps({"attempts": attempts}, indent=2))
        return
    print(f"Self attempts: {len(attempts)}")
    for a in attempts:
        print(f"  - {a['attempt_id'][:8]} [{a['state']}] task={a['proposed_task_id'][:8]} "
              f"intent={a.get('patch_intent_id', '') or 'n/a'}")


def _cmd_self_reconcile(args: Any) -> None:
    from packages.orchestration.self_dogfood_execution import (
        reconcile_self_attempt, export_result_json,
    )
    data = export_result_json(reconcile_self_attempt(args.attempt_id))
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self reconcile: {data['state']}  stop: {data['stop_reason']}  proof: {data['proof_status']}")
    if data["next_safe_action"]:
        print(f"  next: {data['next_safe_action']}")


def _cmd_self_integrity(args: Any) -> None:
    from packages.orchestration.self_dogfood_execution import self_integrity_check
    data = self_integrity_check()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Self integrity: passed={data['passed']}  attempts={data['attempt_count']}  "
          f"issues={data['issue_count']}")
    for i in data["issues"]:
        print(f"  - {i}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "self.inspect": _cmd_self_inspect,
    "self.plan": _cmd_self_plan,
    "self.propose": _cmd_self_propose,
    "self.report": _cmd_self_report,
    "self.execute": _cmd_self_execute,
    "self.status": _cmd_self_status,
    "self.reconcile": _cmd_self_reconcile,
    "self.integrity": _cmd_self_integrity,
}
