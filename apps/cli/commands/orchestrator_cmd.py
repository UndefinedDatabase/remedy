"""CLI handlers for ``remedy orchestrator`` — Main Orchestrator Brain v0.

inspect/report are read-only; decide is metadata-only (persists a safe decision trace);
idea is metadata-only. No action execution, no model/provider calls, no apply/approve.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_orchestrator_inspect(args: Any) -> None:
    from packages.orchestration.orchestrator_brain import (
        build_orchestrator_situation, export_situation_json,
    )
    s = build_orchestrator_situation(getattr(args, "job_id", None))
    data = export_situation_json(s)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Orchestrator inspect: {data['repository_identity']}  phase: {data['current_phase']}")
    print(f"  options: {data['available_option_count']} available  blockers: {len(data['blockers'])}  "
          f"loop: {data['loop_guard']['status']}  routing: {data['model_routing_plan']['tier']}")


def _cmd_orchestrator_decide(args: Any) -> None:
    from packages.orchestration.orchestrator_brain import (
        build_orchestrator_situation, select_orchestrator_decision, export_decision_json,
    )
    s = build_orchestrator_situation(getattr(args, "job_id", None))
    d = select_orchestrator_decision(s, persist=True)
    data = export_decision_json(d)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    sel = data.get("selected_option")
    print(f"Orchestrator decide: {data['stop_reason']}  confidence: {data['confidence']}")
    if sel:
        print(f"  selected: {sel['label']}")
    print(f"  next: {data['next_safe_action']}")
    print(f"  routing: {data['model_routing_plan']['tier']}  loop: {data['loop_guard_status']}")


def _cmd_orchestrator_report(args: Any) -> None:
    from packages.orchestration.orchestrator_brain import (
        build_orchestrator_report, render_report_markdown,
    )
    data = build_orchestrator_report(getattr(args, "job_id", None))
    if getattr(args, "markdown", False):
        print(render_report_markdown(data))
        return
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(render_report_markdown(data))


def _cmd_orchestrator_idea(args: Any) -> None:
    from packages.orchestration.orchestrator_brain import record_idea
    rec = record_idea(args.text)
    data = rec.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Idea captured: {data['classification']}  id: {data['idea_id']}")
    print(f"  {data['summary']}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "orchestrator.inspect": _cmd_orchestrator_inspect,
    "orchestrator.decide": _cmd_orchestrator_decide,
    "orchestrator.report": _cmd_orchestrator_report,
    "orchestrator.idea": _cmd_orchestrator_idea,
}
