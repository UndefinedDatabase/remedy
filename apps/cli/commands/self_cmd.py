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
    data = build_self_dogfood_report(getattr(args, "job_id", None))
    if getattr(args, "markdown", False):
        print(render_report_markdown(data))
        return
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(render_report_markdown(data))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "self.inspect": _cmd_self_inspect,
    "self.plan": _cmd_self_plan,
    "self.propose": _cmd_self_propose,
    "self.report": _cmd_self_report,
}
