"""
Reviewer Recommendation Loop v1 — post-task reviewer that suggests follow-up tasks.

After a task verifies pass, a reviewer can propose follow-up tasks.
Humans decide whether to accept or reject recommendations.

The reviewer provider is replaceable (same pattern as planner/builder).
Default: inert fixture reviewer for testing.

Public API::

    run_reviewer(job, *, after_task_id, reviewer_fn) -> list[ReviewerRecommendation]
    accept_recommendation(job, recommendation_id) -> bool
    reject_recommendation(job, recommendation_id) -> bool
    list_recommendations(job) -> list[dict]
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


def _fixture_reviewer(context: dict[str, Any]) -> list[dict[str, Any]]:
    """Deterministic fixture reviewer — returns 2 recommendations for testing."""
    return [
        {
            "title": "Add edge case tests",
            "description": "Add tests for zero and negative inputs to calc functions",
            "task_type": "test_improvement",
            "reason": "Current tests only cover positive integers",
            "risk": "low",
            "priority": "medium",
        },
        {
            "title": "Add type hints to calc.py",
            "description": "Ensure all function signatures have complete type annotations",
            "task_type": "code_quality",
            "reason": "Type hints improve maintainability",
            "risk": "low",
            "priority": "low",
        },
    ]


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
        "job_name": job.name[:80] if hasattr(job, "name") else "",
        "task_count": len(job.tasks),
        "completed_tasks": [],
        "current_test_status": "unknown",
    }

    for t in job.tasks:
        tstat = t.status.value if hasattr(t.status, "value") else str(t.status)
        if tstat == "completed":
            context["completed_tasks"].append({
                "id": str(t.id),
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


def accept_recommendation(job: Any, recommendation_id: str) -> bool:
    """Accept a recommendation — create a proposed task for evaluation.

    Does NOT directly append a Task to job.tasks. The proposed task must
    go through evaluation (evaluate → approve) before it becomes buildable.
    """
    from packages.orchestration.proposed_tasks import propose_from_recommendation

    recs = _get_recommendations(job)
    for rec in recs:
        if rec.get("id") == recommendation_id and rec.get("status") == "pending":
            rec["status"] = "accepted"
            propose_from_recommendation(str(job.id), rec)
            _save_recommendations(job, recs)
            return True
    return False


def reject_recommendation(job: Any, recommendation_id: str) -> bool:
    """Reject a recommendation — mark as rejected, do not append task."""
    recs = _get_recommendations(job)
    for rec in recs:
        if rec.get("id") == recommendation_id and rec.get("status") == "pending":
            rec["status"] = "rejected"
            _save_recommendations(job, recs)
            return True
    return False


def list_recommendations(job: Any) -> list[dict[str, Any]]:
    """List all reviewer recommendations for a job."""
    return _get_recommendations(job)


def store_recommendations(job: Any, recs: list[ReviewerRecommendation]) -> None:
    """Store reviewer recommendations in job metadata."""
    existing = _get_recommendations(job)
    for rec in recs:
        existing.append({
            "id": rec.id,
            "title": rec.title,
            "description": rec.description,
            "task_type": rec.task_type,
            "reason": rec.reason,
            "risk": rec.risk,
            "priority": rec.priority,
            "source": rec.source,
            "origin_task_id": rec.origin_task_id,
            "status": rec.status,
            "created_at": rec.created_at,
        })
    _save_recommendations(job, existing)


def _get_recommendations(job: Any) -> list[dict[str, Any]]:
    """Get recommendations from job metadata."""
    if not hasattr(job, "metadata") or not job.metadata:
        return []
    return job.metadata.get("reviewer_recommendations", [])


def _save_recommendations(job: Any, recs: list[dict[str, Any]]) -> None:
    """Save recommendations to job metadata."""
    if not hasattr(job, "metadata") or job.metadata is None:
        job.metadata = {}
    job.metadata["reviewer_recommendations"] = recs
