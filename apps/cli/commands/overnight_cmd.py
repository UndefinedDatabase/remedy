"""CLI handlers for ``remedy overnight`` — read-only Bounded Overnight Prep v0.

All handlers are read-only: no repo mutation, no test/apply/repair/provider
execution, no background work. JSON/markdown carry safe summaries only.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_overnight_readiness(args: Any) -> None:
    from packages.orchestration.overnight_readiness import (
        build_overnight_readiness,
        export_readiness_json,
    )
    report = build_overnight_readiness(args.job_id)
    data = export_readiness_json(report)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Overnight readiness: {str(args.job_id)[:8]}")
    print(f"  level: {data['readiness_level']}  ready: {data['ready']}  "
          f"unattended: {data['can_run_unattended']}")
    if data["blockers"]:
        print("  blockers: " + ", ".join(data["blockers"]))
    top_risks = [r for r in data["risks"] if r["severity"] in ("blocker", "high")]
    if top_risks:
        print("  top risks: " + "; ".join(r["summary"] for r in top_risks[:3]))
    na = data.get("next_action")
    if na:
        print(f"  next: {na['label']} -> {na['command']}")


def _cmd_overnight_plan(args: Any) -> None:
    from packages.orchestration.overnight_readiness import (
        build_overnight_plan,
        export_plan_json,
    )
    plan = build_overnight_plan(args.job_id)
    data = export_plan_json(plan)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Overnight plan (dry-run): {str(args.job_id)[:8]}")
    print(f"  would_run: {data['would_run']} (default policy is report-only)")
    if data["hypothetical_cycle"]:
        print("  hypothetical cycle:")
        for ph in data["hypothetical_cycle"]:
            print(f"    - {ph['phase']}: {ph['detail']}")
    if data["stop_points"]:
        print("  stop points: " + ", ".join(data["stop_points"]))
    if data["missing_evidence"]:
        print("  missing evidence: " + ", ".join(data["missing_evidence"]))


def _cmd_overnight_report(args: Any) -> None:
    from packages.orchestration.overnight_readiness import (
        build_overnight_report,
        render_overnight_report_markdown,
    )
    data = build_overnight_report(args.job_id)
    if getattr(args, "markdown", False):
        print(render_overnight_report_markdown(data))
        return
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(render_overnight_report_markdown(data))


def _cmd_overnight_run(args: Any) -> None:
    """Foreground Bounded Overnight Executor v0 — at most one bounded step.

    Report-only unless ``--allow-one-cycle`` plus an explicit action flag is given.
    No daemon/scheduler/watch/background/loop. Calls central services directly.
    """
    from packages.orchestration.overnight_executor import (
        OvernightRunRequest,
        build_executor_policy,
        export_run_result_json,
        run_overnight_executor,
        summarize_run_result,
    )
    policy = build_executor_policy(
        allow_one_cycle=bool(getattr(args, "allow_one_cycle", False)),
        allow_apply=bool(getattr(args, "allow_apply", False)),
        allow_repair_propose=bool(getattr(args, "allow_repair_propose", False)),
        allow_repair_apply=bool(getattr(args, "allow_repair_apply", False)),
    )
    result = run_overnight_executor(
        OvernightRunRequest(job_id=args.job_id, policy=policy, created_by="cli_v0"))
    if getattr(args, "json", False):
        print(json.dumps(export_run_result_json(result), indent=2))
        return
    print(summarize_run_result(result))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "overnight.readiness": _cmd_overnight_readiness,
    "overnight.plan": _cmd_overnight_plan,
    "overnight.report": _cmd_overnight_report,
    "overnight.run": _cmd_overnight_run,
}
