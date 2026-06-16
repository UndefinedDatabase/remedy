"""CLI handlers for ``remedy local-advisor`` — Local Model Advisor Adapter v0.

status is read-only; run is metadata-only (advisory critique; persists a private run record
and a safe decision trace). Optional, loopback-only, disabled by default. No action execution,
no model output ever becomes a command/entity/approval/apply.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_local_advisor_status(args: Any) -> None:
    from packages.orchestration.local_model_advisor import (
        check_local_advisor_availability,
        list_local_advisor_runs,
        load_local_advisor_config,
    )
    config = load_local_advisor_config()
    av = check_local_advisor_availability(config)
    runs = list_local_advisor_runs()
    last = runs[-1] if runs else {}
    data = {
        "enabled": av.enabled,
        "available": av.available,
        "endpoint_label": av.endpoint_label,
        "model_name": av.model_name,
        "stop_reason": av.stop_reason,
        "detail": av.detail,
        "run_count": len(runs),
        "last_run_id": last.get("advisor_run_id", ""),
        "last_status": last.get("status", ""),
    }
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Local advisor: enabled={data['enabled']} available={data['available']}")
    print(f"  endpoint: {data['endpoint_label']}  model: {data['model_name']}")
    print(f"  stop_reason: {data['stop_reason']}  runs: {data['run_count']}  "
          f"last: {data['last_status']}")


def _cmd_local_advisor_run(args: Any) -> None:
    from packages.orchestration.local_model_advisor import load_local_advisor_config
    from packages.orchestration.orchestrator_brain import (
        build_orchestrator_situation,
        consult_local_advisor_for_decision,
        export_decision_json,
        persist_decision,
        select_orchestrator_decision,
    )

    config = load_local_advisor_config(enabled_override=True)
    if not config.enabled:
        data = {
            "enabled": False, "status": "disabled",
            "detail": "Local advisor requires a loopback endpoint and a model.",
            "next_safe_action": (
                "set REMEDY_LOCAL_ADVISOR_ENABLED=1, REMEDY_LOCAL_ADVISOR_ENDPOINT="
                "http://127.0.0.1:11434, REMEDY_LOCAL_ADVISOR_MODEL=<model>"),
        }
        if getattr(args, "json", False):
            print(json.dumps(data, indent=2))
        else:
            print("Local advisor disabled — " + data["detail"])
            print("  next: " + data["next_safe_action"])
        return

    job_id = getattr(args, "job_id", None)
    s = build_orchestrator_situation(job_id)
    d = select_orchestrator_decision(s, persist=False)
    d = consult_local_advisor_for_decision(
        d, s, enabled_override=True, new=bool(getattr(args, "new", False)))
    persist_decision(d)
    decision = export_decision_json(d)
    advisor = decision.get("advisor") or {}
    data = {
        "decision_id": decision.get("decision_id", ""),
        "scope": decision.get("scope", ""),
        "stop_reason": decision.get("stop_reason", ""),
        "confidence": decision.get("confidence", ""),
        "next_safe_action": decision.get("next_safe_action", ""),
        "advisor": advisor,
    }
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Local advisor run: {advisor.get('status')}  impact: {advisor.get('decision_impact')}")
    print(f"  decision: {data['stop_reason']}  confidence: {data['confidence']}")
    print(f"  next: {data['next_safe_action']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "local-advisor.status": _cmd_local_advisor_status,
    "local-advisor.run": _cmd_local_advisor_run,
}
