"""CLI handlers for ``remedy external-builder`` — External Builder Sandbox v0.

``package-create`` exports a SAFE request package for an external worker; ``submit`` ingests an
UNTRUSTED candidate file into quarantine + the existing Trust/Verification pipeline; ``evaluate``
scores a submission via Candidate Quality; ``package-show/list`` + ``submission-show/list`` +
``integrity`` are read-only. NO execution / apply / approve / test. No raw candidate/context in any
surface.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_external_builder_package_create(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import (
        create_external_builder_request_package,
        export_external_package_json,
    )
    pkg = create_external_builder_request_package(
        str(args.job_id), task_id=getattr(args, "task_id", None) or "",
        route_id=getattr(args, "route_id", None) or "",
        objective=getattr(args, "objective", None) or "",
        new=bool(getattr(args, "new", False)))
    if not pkg.package_id:
        print("Error: job not found", file=sys.stderr)
        sys.exit(1)
    data = export_external_package_json(pkg)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"External builder package: {data['package_id']}")
    print(f"  job: {str(data['job_id'])[:8]}  failure: {str(data['failure_artifact_id'])[:8]}  "
          f"context_refs: {len(data['safe_context_refs'])}")
    print(f"  max_candidate_bytes: {data['max_candidate_bytes']}")


def _cmd_external_builder_package_show(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import get_external_package
    rec = get_external_package(args.package_id)
    if rec is None:
        print("Error: package not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"External builder package {args.package_id}")
    print(f"  objective: {rec.get('objective', '')}")
    print(f"  context_refs: {len(rec.get('safe_context_refs', []))}")


def _cmd_external_builder_package_list(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import load_external_packages
    pkgs = load_external_packages(job_id=str(args.job_id))
    out = {"job_id": str(args.job_id), "package_count": len(pkgs),
           "packages": [{"package_id": p.get("package_id"), "route_id": p.get("route_id"),
                         "created_at": p.get("created_at"),
                         "context_refs": len(p.get("safe_context_refs", []))} for p in pkgs]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"External builder packages for {str(args.job_id)[:8]}: {len(pkgs)}")


def _cmd_external_builder_submit(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import (
        export_external_submission_json,
        submit_external_candidate,
    )
    candidate_file = getattr(args, "candidate_file", None)
    if not candidate_file:
        print("Error: --candidate-file is required", file=sys.stderr)
        sys.exit(1)
    sub = submit_external_candidate(
        args.package_id, candidate_file, getattr(args, "source_label", None) or "external",
        new=bool(getattr(args, "new", False)))
    data = export_external_submission_json(sub)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"External builder submission: {data['submission_id']}")
    print(f"  state: {data['state']}  stop: {data['stop_reason']}  source: {data['source_label']}")
    if data.get("intent_id"):
        print(f"  pending intent: {data['intent_id']}")
    print(f"  next: {data['next_safe_action']}")


def _cmd_external_builder_submission_show(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import get_external_submission
    rec = get_external_submission(args.submission_id)
    if rec is None:
        print("Error: submission not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"External builder submission {args.submission_id}")
    print(f"  state: {rec.get('state')}  trust: {rec.get('trust_status')}  "
          f"verification: {rec.get('verification_decision')}")
    print(f"  next: {rec.get('next_safe_action', '')}")


def _cmd_external_builder_submission_list(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import load_external_submissions
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    subs = load_external_submissions(job_id=str(args.job_id))
    try:
        subs = apply_list_options(
            subs,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda s: s.get("received_at", ""),
                "state": lambda s: s.get("state", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda s: s.get("received_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    out = {"job_id": str(args.job_id), "submission_count": len(subs),
           "submissions": [{"submission_id": s.get("submission_id"), "state": s.get("state"),
                            "source_label": s.get("source_label"),
                            "intent_id": s.get("intent_id", ""),
                            "received_at": s.get("received_at", "")} for s in subs]}
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"External builder submissions for {str(args.job_id)[:8]}: {len(subs)}")
    for s in subs:
        print(f"  {s.get('submission_id')}: {s.get('state')}  source={s.get('source_label')}"
              f"  (received={s.get('received_at', '')})")


def _cmd_external_builder_evaluate(args: Any) -> None:
    from packages.orchestration.candidate_quality import (
        evaluate_candidate_quality,
        export_candidate_quality_json,
    )
    from packages.orchestration.external_builder_sandbox import get_external_submission
    rec = get_external_submission(args.submission_id)
    if rec is None:
        print("Error: submission not found", file=sys.stderr)
        sys.exit(1)
    e = evaluate_candidate_quality(
        trust_report_id=rec.get("trust_report_id") or None,
        verification_id=rec.get("verification_id") or None,
        intent_id=rec.get("intent_id") or None, job_id=rec.get("job_id") or None,
        model_label=f"external_builder:{rec.get('source_label', 'external')}",
        route_tier="external_candidate_generator", new=bool(getattr(args, "new", False)))
    data = export_candidate_quality_json(e)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"External candidate quality: {data['evaluation_id']}")
    print(f"  outcome: {data['outcome']}  score: {data['score']['band']} ({data['score']['value']})")
    print(f"  next: {data['next_safe_action']}")


def _cmd_external_builder_integrity(args: Any) -> None:
    from packages.orchestration.external_builder_sandbox import external_builder_integrity
    data = external_builder_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"External builder integrity: passed={data['passed']} "
          f"violations={data['violation_count']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "external-builder.package-create": _cmd_external_builder_package_create,
    "external-builder.package-show": _cmd_external_builder_package_show,
    "external-builder.package-list": _cmd_external_builder_package_list,
    "external-builder.submit": _cmd_external_builder_submit,
    "external-builder.submission-show": _cmd_external_builder_submission_show,
    "external-builder.submission-list": _cmd_external_builder_submission_list,
    "external-builder.evaluate": _cmd_external_builder_evaluate,
    "external-builder.integrity": _cmd_external_builder_integrity,
}
