"""CLI handlers for ``remedy local-candidate`` — Automated Local Candidate Generator v0.

``status`` is read-only. ``generate`` asks an explicitly-configured LOOPBACK local model for a
candidate (only when routing/policy/contract allow) and IMMEDIATELY routes the UNTRUSTED output
through quarantine → Trust Gate → Verification → Materialization. Disabled by default. No
approval/apply/test/PR/git. No raw prompt/output in any surface.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_local_candidate_status(args: Any) -> None:
    from packages.orchestration.local_candidate_generator import (
        check_local_candidate_availability,
        list_local_candidate_runs,
        load_local_candidate_config,
        load_local_candidate_usage,
    )
    cfg = load_local_candidate_config()
    avail = check_local_candidate_availability(cfg)
    job_id = getattr(args, "job_id", None) or ""
    scope = f"job:{job_id}" if job_id else "repository"
    usage = load_local_candidate_usage(scope)
    runs = [r for r in list_local_candidate_runs() if (not job_id or r.get("job_id") == job_id)]
    latest = runs[-1] if runs else None
    data = {
        **cfg.to_public_dict(),
        "available": avail["available"],
        "availability_stop_reason": avail["stop_reason"],
        "usage": usage,
        "latest_status": (latest or {}).get("status", "none"),
        "latest_stop_reason": (latest or {}).get("stop_reason", ""),
    }
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print("Local candidate generator")
    print(f"  enabled: {data['enabled']}  available: {data['available']}  "
          f"endpoint: {data['endpoint_label']}  model: {data['model_name']}")
    print(f"  runs: {usage['run_count']}  latest: {data['latest_status']}")


def _cmd_local_candidate_generate(args: Any) -> None:
    from packages.orchestration.local_candidate_generator import (
        LocalCandidateGenerationRequest,
        export_local_candidate_result_json,
        run_local_candidate_generation,
    )
    request_package_id = getattr(args, "request_package_id", None) or ""
    if not request_package_id:
        print("Error: --request-package-id is required", file=sys.stderr)
        sys.exit(1)
    req = LocalCandidateGenerationRequest(
        request_package_id=request_package_id,
        job_id=getattr(args, "job_id", None) or "",
        failure_artifact_id=getattr(args, "failure_artifact_id", None) or "",
        self_attempt_id=getattr(args, "self_attempt_id", None) or "",
        routing_id=getattr(args, "routing_id", None) or "",
        new=bool(getattr(args, "new", False)),
    )
    res = run_local_candidate_generation(req)
    data = export_local_candidate_result_json(res)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Local candidate generate: {str(data['job_id'])[:8] or 'repository'}")
    print(f"  status: {data['status']}  stop: {data['stop_reason']}")
    lk = data["linkage"]
    if lk.get("intent_id"):
        print(f"  pending intent: {lk['intent_id']}")
    if lk.get("verification_id"):
        print(f"  verification: {lk['verification_id']}")
    print(f"  next: {data['next_safe_action']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "local-candidate.status": _cmd_local_candidate_status,
    "local-candidate.generate": _cmd_local_candidate_generate,
}
