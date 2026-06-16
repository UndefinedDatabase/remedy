"""CLI handlers for the Overnight Mission Contract + Review/Repair Spine v0 (Step 1850).

`overnight contract-create` builds a Mission Contract from a job (metadata only); `evaluate` judges
satisfaction from durable evidence and persists a safe evaluation; `next-action`, `contract-show`,
`cycles`, `contract-readiness`, `integrity` are read-only. NONE execute a worker, run a test, call a
provider/model, or apply/approve/git. No raw prompts/logs/diffs/secrets/absolute paths in output.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _split_acceptance(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _cmd_contract_create(args: Any) -> None:
    from packages.orchestration.overnight_mission import (
        create_mission_contract_from_job,
        export_mission_contract_json,
    )
    try:
        autonomy = int(getattr(args, "autonomy_level", 1) or 1)
    except (TypeError, ValueError):
        print("Error: --autonomy-level must be an integer", file=sys.stderr)
        sys.exit(1)
    contract = create_mission_contract_from_job(
        str(args.job_id), user_goal=getattr(args, "user_goal", None) or "",
        acceptance_criteria=_split_acceptance(getattr(args, "acceptance", None)),
        autonomy_level=autonomy)
    data = export_mission_contract_json(contract)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Mission contract {data['contract_id']} for {str(args.job_id)[:8]}")
    print(f"  goal: {data['user_goal']}")
    print(f"  acceptance_criteria: {len(data['acceptance_criteria'])}  gates: {data['required_gates']}")


def _cmd_contract_show(args: Any) -> None:
    from packages.orchestration.overnight_mission import load_mission_contract
    rec = load_mission_contract(str(args.contract_id))
    if rec is None:
        print("Error: contract not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"Mission contract {rec.get('contract_id')}")
    print(f"  goal: {rec.get('user_goal')}")
    print(f"  acceptance_criteria: {len(rec.get('acceptance_criteria', []))}  "
          f"gates: {rec.get('required_gates')}")


def _cmd_evaluate(args: Any) -> None:
    from packages.orchestration.overnight_mission import (
        _contract_from_dict,
        evaluate_mission_contract,
        export_mission_evaluation_json,
        load_mission_contract,
    )
    rec = load_mission_contract(str(args.contract_id))
    if rec is None:
        print("Error: contract not found", file=sys.stderr)
        sys.exit(1)
    ev = evaluate_mission_contract(_contract_from_dict(rec), persist=True)
    data = export_mission_evaluation_json(ev)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Mission evaluation {data['contract_id']}")
    print(f"  status: {data['status']}  satisfied: {data['satisfied']}  phase: {data['phase']}")
    print(f"  open_findings: {data['open_review_findings']}  open_tasks: {data['open_tasks']}  "
          f"failed_tests: {data['failed_tests']}")
    print(f"  summary: {data['user_summary']}")


def _cmd_next_action(args: Any) -> None:
    from packages.orchestration.overnight_mission import (
        _contract_from_dict,
        evaluate_mission_contract,
        load_mission_contract,
    )
    rec = load_mission_contract(str(args.contract_id))
    if rec is None:
        print("Error: contract not found", file=sys.stderr)
        sys.exit(1)
    ev = evaluate_mission_contract(_contract_from_dict(rec), persist=False)
    out = {"contract_id": ev.contract_id, "status": ev.status,
           "required_next_actions": ev.required_next_actions,
           "optional_next_ideas": ev.optional_next_ideas,
           "next_safe_actions": ev.next_safe_actions,
           "user_decision_required": ev.user_decision_required}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Mission next actions ({ev.status})")
    for a in ev.required_next_actions:
        flag = " [user decision]" if a.get("user_decision_required") else ""
        print(f"  required: {a['title']} -> {a['command']}{flag}")
    for a in ev.optional_next_ideas:
        print(f"  optional: {a.get('title')} (impact={a.get('impact')}, effort={a.get('effort')})")


def _cmd_cycles(args: Any) -> None:
    from packages.orchestration.overnight_mission import list_mission_cycles
    cycles = list_mission_cycles(str(args.contract_id))
    out = {"contract_id": str(args.contract_id), "cycle_count": len(cycles),
           "cycles": [{"cycle_id": c.get("cycle_id"), "cycle_index": c.get("cycle_index"),
                       "phase": c.get("phase")} for c in cycles]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Mission cycles for {str(args.contract_id)}: {len(cycles)}")


def _cmd_contract_readiness(args: Any) -> None:
    from packages.orchestration.overnight_mission import mission_readiness
    data = mission_readiness(str(args.job_id))
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Overnight mission readiness for {str(args.job_id)[:8]}")
    print(f"  has_contract: {data['has_mission_contract']}  review_verdict: {data['review_verdict']}")
    print(f"  full_overnight_autonomy: {data['full_overnight_autonomy']} (not built)")
    print(f"  next: {data['next_safe_action']}")


def _cmd_integrity(args: Any) -> None:
    from packages.orchestration.overnight_mission import mission_integrity
    data = mission_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Mission integrity: passed={data['passed']} violations={data['violation_count']} "
          f"contracts={data['contract_count']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "overnight.contract-create": _cmd_contract_create,
    "overnight.contract-show": _cmd_contract_show,
    "overnight.evaluate": _cmd_evaluate,
    "overnight.next-action": _cmd_next_action,
    "overnight.cycles": _cmd_cycles,
    "overnight.contract-readiness": _cmd_contract_readiness,
    "overnight.integrity": _cmd_integrity,
}
