"""
CLI handlers for ``remedy review`` commands — reviewer recommendation loop.

Recommendations require human approval. Reviewer does NOT auto-append tasks.
"""

from __future__ import annotations

import json
import sys
from typing import Any
from uuid import UUID


def _cmd_review_run(args: Any) -> None:
    """Run reviewer for a job."""
    from packages.orchestration.reviewer import (
        _fixture_reviewer,
        run_reviewer,
        store_recommendations,
    )
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(args.job_id))
    after_task = getattr(args, "after_task", None)

    # Use fixture reviewer if requested
    reviewer_fn = None
    if getattr(args, "fixture_reviewer", False):
        reviewer_fn = _fixture_reviewer

    recs = run_reviewer(job, after_task_id=after_task, reviewer_fn=reviewer_fn)
    store_recommendations(job, recs)
    save_job(job)

    if getattr(args, "json", False):
        out = {
            "version": 1,
            "job_id": str(job.id),
            "recommendation_count": len(recs),
            "recommendations": [
                {
                    "id": r.id,
                    "title": r.title,
                    "description": r.description,
                    "task_type": r.task_type,
                    "reason": r.reason,
                    "risk": r.risk,
                    "priority": r.priority,
                    "status": r.status,
                }
                for r in recs
            ],
        }
        print(json.dumps(out, indent=2))
    else:
        if recs:
            for r in recs:
                print(f"  {r.id}  {r.title}  [{r.risk}]  {r.reason[:60]}")
        else:
            print("No recommendations from reviewer.")


def _cmd_review_list(args: Any) -> None:
    """List reviewer recommendations."""
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.reviewer import list_recommendations
    from packages.orchestration.storage import load_job

    job = load_job(UUID(args.job_id))
    recs = list_recommendations(job)
    try:
        recs = apply_list_options(
            recs,
            sort=getattr(args, "sort", None), desc=getattr(args, "desc", False),
            since=getattr(args, "since", None), until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={
                "created_at": lambda r: r.get("created_at", ""),
                "status": lambda r: r.get("status", ""),
            },
            default_sort_field="created_at",
            date_getter=lambda r: r.get("created_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps({
            "version": 1,
            "job_id": str(job.id),
            "recommendations": recs,
        }, indent=2))
    else:
        if not recs:
            print("No reviewer recommendations.")
            return
        for r in recs:
            status = r.get("status", "?")
            title = r.get("title", "?")
            rid = r.get("id", "?")
            created = r.get("created_at", "?")
            print(f"  [{status}] {rid}  {title}  (created={created})")


def _cmd_review_accept(args: Any) -> None:
    """Accept a reviewer recommendation — creates a proposed task for evaluation."""
    from packages.orchestration.reviewer import accept_recommendation
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(args.job_id))
    ok = accept_recommendation(job, args.recommendation_id)
    if ok:
        save_job(job)
        if getattr(args, "json", False):
            print(json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "recommendation_id": args.recommendation_id,
                "accepted": True,
                "proposed_task_created": True,
            }, indent=2))
        else:
            print(f"Accepted: {args.recommendation_id} (proposed task created — evaluate before build)")
    else:
        if getattr(args, "json", False):
            print(json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "recommendation_id": args.recommendation_id,
                "accepted": False,
                "proposed_task_created": False,
                "error": "not found or already resolved",
            }, indent=2))
        else:
            print(f"Not found or already resolved: {args.recommendation_id}", file=sys.stderr)
        sys.exit(1)


def _cmd_review_reject(args: Any) -> None:
    """Reject a reviewer recommendation."""
    from packages.orchestration.reviewer import reject_recommendation
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(args.job_id))
    ok = reject_recommendation(job, args.recommendation_id)
    if ok:
        save_job(job)
        if getattr(args, "json", False):
            print(json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "recommendation_id": args.recommendation_id,
                "rejected": True,
                "task_appended": False,
            }, indent=2))
        else:
            print(f"Rejected: {args.recommendation_id}")
    else:
        if getattr(args, "json", False):
            print(json.dumps({
                "version": 1,
                "job_id": str(job.id),
                "recommendation_id": args.recommendation_id,
                "rejected": False,
                "task_appended": False,
                "error": "not found or already resolved",
            }, indent=2))
        else:
            print(f"Not found or already resolved: {args.recommendation_id}", file=sys.stderr)
        sys.exit(1)


def _cmd_review_bundle(args: Any) -> None:
    """Generate a safe review bundle zip for a job."""
    from packages.orchestration.review_bundle import (
        build_review_bundle,
        export_review_bundle_json,
        summarize_review_bundle,
    )
    from packages.orchestration.storage import JobNotFoundError, JobStoreError

    output = getattr(args, "output", None)

    try:
        result = build_review_bundle(args.job_id, output_path=output)
    except (JobNotFoundError, JobStoreError) as exc:
        print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if result.error:
        print(f"Error: {result.error}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(export_review_bundle_json(result), indent=2))
    else:
        print(summarize_review_bundle(result))


COMMAND_HANDLERS = {
    "review.bundle": lambda args: _cmd_review_bundle(args),
    "review.run": lambda args: _cmd_review_run(args),
    "review.list": lambda args: _cmd_review_list(args),
    "review.accept": lambda args: _cmd_review_accept(args),
    "review.reject": lambda args: _cmd_review_reject(args),
}
