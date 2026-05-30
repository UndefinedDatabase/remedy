"""
CLI handlers for ``remedy review`` commands — reviewer recommendation loop.
"""

from __future__ import annotations

import json
import sys
from typing import Any
from uuid import UUID


def _cmd_review_run(args: Any) -> None:
    """Run reviewer for a job."""
    from packages.orchestration.reviewer import (
        run_reviewer,
        store_recommendations,
    )
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(args.job_id))
    after_task = getattr(args, "after_task", None)
    recs = run_reviewer(job, after_task_id=after_task)
    store_recommendations(job, recs)
    save_job(job)

    if getattr(args, "json", False):
        print(json.dumps({"recommendations": len(recs), "job_id": str(job.id)}))
    else:
        if recs:
            for r in recs:
                print(f"  {r.id}  {r.title}  [{r.risk}]  {r.reason[:60]}")
        else:
            print("No recommendations from reviewer.")


def _cmd_review_list(args: Any) -> None:
    """List reviewer recommendations."""
    from packages.orchestration.reviewer import list_recommendations
    from packages.orchestration.storage import load_job

    job = load_job(UUID(args.job_id))
    recs = list_recommendations(job)

    if getattr(args, "json", False):
        print(json.dumps({"version": 1, "job_id": str(job.id), "recommendations": recs}))
    else:
        if not recs:
            print("No reviewer recommendations.")
            return
        for r in recs:
            status = r.get("status", "?")
            title = r.get("title", "?")
            rid = r.get("id", "?")
            print(f"  [{status}] {rid}  {title}")


def _cmd_review_accept(args: Any) -> None:
    """Accept a reviewer recommendation."""
    from packages.orchestration.reviewer import accept_recommendation
    from packages.orchestration.storage import load_job, save_job

    job = load_job(UUID(args.job_id))
    ok = accept_recommendation(job, args.recommendation_id)
    if ok:
        save_job(job)
        print(f"Accepted: {args.recommendation_id}")
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
        print(f"Rejected: {args.recommendation_id}")
    else:
        print(f"Not found or already resolved: {args.recommendation_id}", file=sys.stderr)
        sys.exit(1)


COMMAND_HANDLERS = {
    "review.run": lambda args: _cmd_review_run(args),
    "review.list": lambda args: _cmd_review_list(args),
    "review.accept": lambda args: _cmd_review_accept(args),
    "review.reject": lambda args: _cmd_review_reject(args),
}
