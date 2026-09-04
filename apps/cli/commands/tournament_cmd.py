"""CLI handlers for `remedy tournament` — Model/Route Tournament Harness v0 (Step 1806).

`tournament report` generates a safe evidence-based route comparison (metadata report; never runs
workers/models/providers); `tournament show/list/integrity` are read-only. No raw evidence/prompts/
candidates/secrets/absolute paths in any output.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_tournament_report(args: Any) -> None:
    from packages.orchestration.model_route_tournament import (
        export_tournament_report_json,
        generate_tournament_report,
    )
    rep = generate_tournament_report(
        str(args.job_id), task_id=getattr(args, "task_id", None) or "",
        task_type=getattr(args, "task_type", None) or "repair")
    data = export_tournament_report_json(rep)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Tournament {data['tournament_id']} for {str(args.job_id)[:8]} ({data['status']})")
    print(f"  competitors: {len(data['competitors'])}  winner: {data['winner_competitor_id'] or '(none)'}"
          f"  confidence: {data['confidence']}")
    print(f"  reason: {data['safe_reason']}")


def _cmd_tournament_show(args: Any) -> None:
    from packages.orchestration.model_route_tournament import load_tournament_report
    rec = load_tournament_report(str(args.tournament_id))
    if rec is None:
        print("Error: tournament not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"Tournament {rec.get('tournament_id')} ({rec.get('status')})")
    print(f"  winner: {rec.get('winner_competitor_id') or '(none)'}  confidence: {rec.get('confidence')}")


def _cmd_tournament_list(args: Any) -> None:
    from packages.orchestration.model_route_tournament import list_tournament_reports
    reps = list_tournament_reports(job_id=str(args.job_id))
    out = {"job_id": str(args.job_id), "report_count": len(reps),
           "reports": [{"tournament_id": r.get("tournament_id"), "status": r.get("status"),
                        "winner_competitor_id": r.get("winner_competitor_id", ""),
                        "confidence": r.get("confidence"),
                        "created_at": r.get("created_at", "")} for r in reps]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Tournament reports for {str(args.job_id)[:8]}: {len(reps)}")
    for r in reps:
        winner = r.get("winner_competitor_id") or "(none)"
        print(f"  {r.get('tournament_id')}: {r.get('status')}  winner={winner}"
              f"  confidence={r.get('confidence')}  (created={r.get('created_at', '')})")


def _cmd_tournament_integrity(args: Any) -> None:
    from packages.orchestration.model_route_tournament import tournament_integrity
    data = tournament_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Tournament integrity: passed={data['passed']} "
          f"violations={data['violation_count']} reports={data['report_count']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "tournament.report": _cmd_tournament_report,
    "tournament.show": _cmd_tournament_show,
    "tournament.list": _cmd_tournament_list,
    "tournament.integrity": _cmd_tournament_integrity,
}
