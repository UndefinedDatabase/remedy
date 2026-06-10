"""CLI handlers for the ``contract`` command group."""

from __future__ import annotations

import json
import sys
from typing import Any


def _cmd_contract_inspect(args: Any) -> None:
    """Show the run contract for a job."""
    from packages.orchestration.run_contract import (
        RunContract,
        build_default_run_contract,
        export_run_contract_json,
        summarize_run_contract,
    )
    from packages.orchestration.storage import load_job

    job_id = getattr(args, "job_id", "")
    if not job_id:
        print(json.dumps({"error": "job_id required"}, indent=2) if getattr(args, "json", False) else "Error: job_id required")
        sys.exit(1)

    try:
        job = load_job(job_id)
    except Exception:
        msg = f"Job {job_id[:8]} not found"
        if getattr(args, "json", False):
            print(json.dumps({"error": msg}, indent=2))
        else:
            print(f"Error: {msg}")
        sys.exit(1)

    contract = build_default_run_contract(job)

    if getattr(args, "json", False):
        print(json.dumps(export_run_contract_json(contract), indent=2))
    else:
        print(summarize_run_contract(contract))


def _cmd_contract_check(args: Any) -> None:
    """Check whether an action is allowed by the contract."""
    from packages.orchestration.run_contract import (
        build_default_run_contract,
        evaluate_run_action,
        export_run_action_decision_json,
    )
    from packages.orchestration.storage import load_job

    job_id = getattr(args, "job_id", "")
    action = getattr(args, "action", "")

    if not job_id or not action:
        msg = "job_id and action required"
        if getattr(args, "json", False):
            print(json.dumps({"error": msg}, indent=2))
        else:
            print(f"Error: {msg}")
        sys.exit(1)

    try:
        job = load_job(job_id)
    except Exception:
        msg = f"Job {job_id[:8]} not found"
        if getattr(args, "json", False):
            print(json.dumps({"error": msg}, indent=2))
        else:
            print(f"Error: {msg}")
        sys.exit(1)

    contract = build_default_run_contract(job)

    path = getattr(args, "path", None)
    risk = getattr(args, "risk", None)

    decision = evaluate_run_action(contract, action, path=path, risk=risk)

    if getattr(args, "json", False):
        print(json.dumps(export_run_action_decision_json(decision), indent=2))
    else:
        status_icon = "[+]" if decision.allowed else "[x]"
        print(f"{status_icon} {action}: {decision.status}")
        print(f"  Reason: {decision.reason}")
        if decision.next_safe_action:
            print(f"  Next: {decision.next_safe_action}")


COMMAND_HANDLERS = {
    "contract.inspect": lambda args: _cmd_contract_inspect(args),
    "contract.check": lambda args: _cmd_contract_check(args),
}
