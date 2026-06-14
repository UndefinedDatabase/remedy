"""CLI handlers for ``remedy provider`` — Provider Trust Gate v0.

``intake-repair`` quarantines + trust-validates UNTRUSTED external model output and
creates a pending Repair Patch Intent only when accepted. ``trust-show`` is read-only.
No provider execution, no network, no apply, no approval. No raw output in any surface.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _cmd_provider_intake_repair(args: Any) -> None:
    from packages.orchestration.provider_trust import (
        ProviderOutputIntakeRequest, intake_provider_repair, export_intake_result_json,
        SourceKind,
    )
    use_stdin = bool(getattr(args, "stdin", False))
    input_path = getattr(args, "input", None)
    if not use_stdin and not input_path:
        print("Error: provide --input <path> or --stdin", file=sys.stderr)
        sys.exit(1)
    stdin_text = sys.stdin.read() if use_stdin else None
    request = ProviderOutputIntakeRequest(
        job_id=args.job_id,
        failure_artifact_id=getattr(args, "failure_artifact_id", None) or "",
        provider_name=getattr(args, "provider", None) or "unknown",
        model_name=getattr(args, "model", None) or "",
        source_kind=SourceKind.STDIN if use_stdin else SourceKind.FILE,
    )
    result = intake_provider_repair(request, input_path=input_path, stdin_text=stdin_text)
    data = export_intake_result_json(result)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Provider intake: {str(args.job_id)[:8]}")
    print(f"  trust: {data['trust_status']}  kind: {data['candidate_kind']}  "
          f"confidence: {data['confidence']}")
    if data["findings"]:
        print("  findings: " + ", ".join(f"{f['severity']}:{f['code']}" for f in data["findings"][:6]))
    if data["repair_intent_id"]:
        print(f"  pending intent: {data['repair_intent_id']}")
    print(f"  next: {data['next_safe_action']}")


def _cmd_provider_trust_show(args: Any) -> None:
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.provider_trust import get_trust_report
    try:
        job = load_job(args.job_id)
    except (JobNotFoundError, ValueError) as exc:
        print(f"Error: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)
    report = get_trust_report(job, args.trust_report_id)
    if report is None:
        print("Error: trust report not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(report, indent=2))
        return
    print(f"Provider trust report {args.trust_report_id}")
    print(f"  status: {report['trust_status']}  kind: {report['candidate_kind']}  "
          f"confidence: {report['confidence']}")
    print(f"  provider: {report['provider_name']}  model: {report.get('model_name', '')}")
    for f in report.get("findings", []):
        print(f"  - {f['severity']}: {f['code']} {f.get('target', '')}".rstrip())
    if report.get("repair_intent_id"):
        print(f"  pending intent: {report['repair_intent_id']}")
    print(f"  next: {report.get('next_safe_action', '')}")


def _cmd_provider_material_show(args: Any) -> None:
    from packages.orchestration.storage import load_job, JobNotFoundError
    from packages.orchestration.provider_patch_material import (
        get_material, verify_provider_patch_material,
    )
    try:
        job = load_job(args.job_id)
    except (JobNotFoundError, ValueError) as exc:
        print(f"Error: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)
    material = get_material(job, args.material_id)
    if material is None:
        print("Error: material not found", file=sys.stderr)
        sys.exit(1)
    verification = verify_provider_patch_material(str(args.job_id), args.material_id)
    out = {**material, "verification": verification.to_dict()}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Provider patch material {args.material_id}")
    print(f"  state: {material['material_state']}  verified: {verification.ok}  "
          f"format: {material['patch_format']}")
    print(f"  targets: {material['target_path_count']}  ops: {material['operation_count']}  "
          f"lines: {material['total_line_count']}")
    if material.get("linked_intent_id"):
        print(f"  pending intent: {material['linked_intent_id']}")
    print(f"  trust report: {material.get('trust_report_id', '')}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "provider.intake-repair": _cmd_provider_intake_repair,
    "provider.trust-show": _cmd_provider_trust_show,
    "provider.material-show": _cmd_provider_material_show,
}
