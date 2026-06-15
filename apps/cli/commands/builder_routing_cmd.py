"""CLI handlers for ``remedy builder-routing`` — Expensive Builder Routing v0.

``decide`` selects ONE local-first routing tier (deterministic / local advisor / local
candidate generation / external candidate generation / human review / no safe route) and
persists a SAFE trace. ``report`` is read-only. Routing/policy/planning ONLY — NO builder/
model/provider execution, NO candidate generation, NO apply/approval, NO intent creation.
No raw prompt/response/source/diff/log/secrets/paths in any surface.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _build_request(args: Any):
    from packages.orchestration.builder_routing import BuilderRoutingRequest
    return BuilderRoutingRequest(
        job_id=getattr(args, "job_id", None) or "",
        failure_artifact_id=getattr(args, "failure_artifact_id", None) or "",
        self_attempt_id=getattr(args, "self_attempt_id", None) or "",
        request_package_id=getattr(args, "request_package_id", None) or "",
        orchestrator_decision_id=getattr(args, "orchestrator_decision_id", None) or "",
        user_requested=bool(getattr(args, "user_requested", False)),
        new=bool(getattr(args, "new", False)),
    )


def _cmd_builder_routing_decide(args: Any) -> None:
    from packages.orchestration.builder_routing import (
        select_builder_routing_decision, export_builder_routing_json,
    )
    decision = select_builder_routing_decision(_build_request(args))
    data = export_builder_routing_json(decision)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Builder routing: {str(data['job_id'])[:8] or 'repository'}")
    print(f"  tier: {data['selected_tier']}  stop: {data['stop_reason']}  "
          f"loop: {data['loop_guard_status']}  risk: {data['risk_summary']['level']}")
    if data["justification_codes"]:
        print("  justification: " + ", ".join(data["justification_codes"][:8]))
    b = data["budget_summary"]
    print(f"  budget: local_advisor={b['local_advisor_runs_remaining']} "
          f"local_gen={b['local_candidate_runs_remaining']} "
          f"external={b['external_candidate_runs_remaining']} "
          f"ext_cost={b['estimated_external_cost']}")
    for rt in data["rejected_tiers"][:6]:
        print(f"  rejected: {rt['tier']} ({rt.get('why_not', '') or 'not selected'})")
    print(f"  why: {data['selected_reason']}")
    print(f"  next: {data['next_safe_action']}")


def _cmd_builder_routing_report(args: Any) -> None:
    from packages.orchestration.builder_routing import (
        select_builder_routing_decision, export_builder_routing_json,
    )
    decision = select_builder_routing_decision(_build_request(args), persist=False)
    data = export_builder_routing_json(decision)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    b = data["budget_summary"]
    lines = [
        f"# Builder Routing Report — {str(data['job_id'])[:8] or 'repository'}",
        "",
        "## Situation",
        f"- evidence_fingerprint: {data['evidence_fingerprint']}",
        f"- risk: {data['risk_summary']['level']} ({data['risk_summary']['summary']})",
        "",
        "## Whether builder help is needed",
        f"- selected tier: **{data['selected_tier']}**",
        f"- stop reason: {data['stop_reason']}",
        "",
        "## Local-first route",
        f"- {data['selected_reason']}",
        "",
        "## Expensive builder justification",
        ("- " + ", ".join(data['justification_codes'])) if data['justification_codes']
        else "- (none — expensive route not justified)",
        "",
        "## Budget",
        f"- local_advisor_runs_remaining: {b['local_advisor_runs_remaining']}",
        f"- local_candidate_runs_remaining: {b['local_candidate_runs_remaining']}",
        f"- external_candidate_runs_remaining: {b['external_candidate_runs_remaining']}",
        f"- estimated_external_cost: {b['estimated_external_cost']}",
        f"- daily_external_attempts: {b['daily_external_attempts']}",
        "",
        "## Loop guard",
        f"- status: {data['loop_guard_status']}",
        "",
        "## Human decisions",
        "- routing recommends only; nothing is executed, approved, or applied here.",
        "",
        "## Next safe action",
        f"- `{data['next_safe_action']}`",
    ]
    if getattr(args, "markdown", False):
        print("\n".join(lines))
        return
    print("\n".join(lines))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "builder-routing.decide": _cmd_builder_routing_decide,
    "builder-routing.report": _cmd_builder_routing_report,
}
