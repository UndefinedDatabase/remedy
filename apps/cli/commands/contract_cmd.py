"""CLI handlers for the ``contract`` command group."""

from __future__ import annotations

import json
import sys
from typing import Any


def _cmd_contract_inspect(args: Any) -> None:
    """Show the run contract for a job."""
    from packages.orchestration.run_contract import (
        ensure_contract,
        export_run_contract_json,
        summarize_run_contract,
    )
    from packages.orchestration.storage import load_job, save_job

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

    contract = ensure_contract(job)
    save_job(job)  # persist if newly created

    if getattr(args, "json", False):
        print(json.dumps(export_run_contract_json(contract), indent=2))
    else:
        print(summarize_run_contract(contract))


def _cmd_contract_check(args: Any) -> None:
    """Check whether an action is allowed by the contract."""
    from packages.orchestration.run_contract import (
        ensure_contract,
        evaluate_run_action,
        export_run_action_decision_json,
    )
    from packages.orchestration.storage import load_job, save_job

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

    contract = ensure_contract(job)
    save_job(job)

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


def _cmd_contract_set(args: Any) -> None:
    """Set a contract field on a job (limited to safe fields)."""
    from packages.orchestration.run_contract import (
        ensure_contract,
        export_run_contract_json,
        save_contract,
        validate_run_contract,
    )
    from packages.orchestration.run_contract import RunContract
    from packages.orchestration.storage import load_job, save_job
    from dataclasses import fields as dc_fields

    job_id = getattr(args, "job_id", "")
    field_name = getattr(args, "field", "")
    value = getattr(args, "value", "")

    if not job_id or not field_name or value == "":
        msg = "job_id, field, and value required"
        if getattr(args, "json", False):
            print(json.dumps({"error": msg}, indent=2))
        else:
            print(f"Error: {msg}")
        sys.exit(1)

    # Only allow safe fields to be set
    SETTABLE_FIELDS = frozenset({
        "max_loops", "max_test_runs", "max_runtime_seconds",
        "stop_before_apply", "stop_on_unknown_risk", "stop_on_medium_risk",
        "no_cloud", "notes",
    })

    if field_name not in SETTABLE_FIELDS:
        msg = f"Field '{field_name}' not settable. Allowed: {sorted(SETTABLE_FIELDS)}"
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

    contract = ensure_contract(job)

    # Parse value to correct type
    field_type = {f.name: f.type for f in dc_fields(contract)}
    if field_name in ("max_loops", "max_test_runs", "max_runtime_seconds"):
        try:
            parsed_value = int(value)
        except ValueError:
            msg = f"Field '{field_name}' requires integer value"
            if getattr(args, "json", False):
                print(json.dumps({"error": msg}, indent=2))
            else:
                print(f"Error: {msg}")
            sys.exit(1)
    elif field_name in ("stop_before_apply", "stop_on_unknown_risk", "stop_on_medium_risk", "no_cloud"):
        parsed_value = value.lower() in ("true", "1", "yes")
    else:
        parsed_value = value

    # Create updated contract
    base = {f.name: getattr(contract, f.name) for f in dc_fields(contract)}
    base[field_name] = parsed_value
    base["source"] = "user_override"
    updated = RunContract(**base)

    errors = validate_run_contract(updated)
    real_errors = [e for e in errors if "unknown actions" not in e]
    if real_errors:
        msg = f"Invalid contract: {'; '.join(real_errors)}"
        if getattr(args, "json", False):
            print(json.dumps({"error": msg, "details": real_errors}, indent=2))
        else:
            print(f"Error: {msg}")
        sys.exit(1)

    save_contract(job, updated)
    save_job(job)

    if getattr(args, "json", False):
        print(json.dumps({"status": "updated", "field": field_name, "value": parsed_value}, indent=2))
    else:
        print(f"Contract updated: {field_name} = {parsed_value}")


COMMAND_HANDLERS = {
    "contract.inspect": lambda args: _cmd_contract_inspect(args),
    "contract.check": lambda args: _cmd_contract_check(args),
    "contract.set": lambda args: _cmd_contract_set(args),
}
