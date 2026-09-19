"""
Reviewer Recommendation Loop v1 — post-task reviewer that suggests follow-up tasks.

After a task verifies pass, a reviewer can propose follow-up tasks. The reviewer provider
is replaceable (same pattern as planner/builder); the default is inert and returns none.

The store that kept recommendations on the job, and the accept and reject steps that turned
one into a proposed task, had no caller once the `review` group was deleted, and went with
the two cockpit readers of that store (R-0908). `dev status` still probes `run_reviewer`.

Public API::

    run_reviewer(job, *, after_task_id, reviewer_fn) -> list[ReviewerRecommendation]
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class ReviewerRecommendation:
    """A single task recommendation from the reviewer."""
    id: str
    title: str
    description: str
    task_type: str
    reason: str
    risk: str
    priority: str
    source: str = "reviewer"
    origin_task_id: str = ""
    status: str = "pending"  # pending, accepted, rejected
    created_at: str = ""


def _default_reviewer(context: dict[str, Any]) -> list[dict[str, Any]]:
    """Inert fixture reviewer — returns no recommendations."""
    return []


def run_reviewer(
    job: Any,
    *,
    after_task_id: str | None = None,
    reviewer_fn: Callable[[dict[str, Any]], list[dict[str, Any]]] | None = None,
    max_recommendations: int = 5,
) -> list[ReviewerRecommendation]:
    """Run reviewer and return recommendations (not yet appended to job)."""
    fn = reviewer_fn or _default_reviewer

    # Build safe context for reviewer
    context: dict[str, Any] = {
        "job_name": str(job.job_title)[:80] if hasattr(job, "job_title") else "",
        "task_count": len(job.tasks),
        "completed_tasks": [],
        "current_test_status": "unknown",
    }

    for t in job.tasks:
        tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
        if tstat == "completed":
            context["completed_tasks"].append({
                "id": str(t.task_id),
                "task_type": (getattr(t, "inputs", None) or {}).get("task_type", "unknown"),
                "status": tstat,
            })

    raw = fn(context)
    recs = []
    for item in raw[:max_recommendations]:
        rec = ReviewerRecommendation(
            id=uuid4().hex[:12],
            title=str(item.get("title", ""))[:80],
            description=str(item.get("description", ""))[:200],
            task_type=str(item.get("task_type", "unknown")),
            reason=str(item.get("reason", ""))[:200],
            risk=str(item.get("risk", "low")),
            priority=str(item.get("priority", "low")),
            source="reviewer",
            origin_task_id=after_task_id or "",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        recs.append(rec)

    return recs
