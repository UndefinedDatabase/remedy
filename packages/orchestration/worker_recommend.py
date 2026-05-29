"""
Worker Recommend v0 — local-first worker recommendation.

Uses worker adapter registry, token policy, job state, and context pack
estimate to produce a recommendation. No provider execution, no network.

Public API::

    recommend_worker(job, events) -> WorkerRecommendation
    export_worker_recommendation_json(rec) -> dict
    summarize_worker_recommendation(rec) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job, RunState


@dataclass(frozen=True)
class WorkerCandidate:
    """One candidate in the recommendation."""

    provider_id: str
    display_name: str
    execution_mode: str
    status: str
    score: int
    reason: str


@dataclass(frozen=True)
class WorkerRecommendation:
    """Immutable worker recommendation result."""

    version: int
    job_id: str
    recommended_worker: str
    reason: str
    token_mode: str
    estimated_context_tokens: int
    requires_approval: bool
    candidates: tuple[WorkerCandidate, ...]


def recommend_worker(
    job: Job,
    events: list[dict[str, Any]],
) -> WorkerRecommendation:
    """Produce a local-first worker recommendation.

    No provider execution. Uses adapter metadata and job state.
    """
    from packages.orchestration.context_pack import build_context_pack
    from packages.orchestration.token_policy import build_default_token_policy
    from packages.orchestration.worker_adapters import list_worker_specs

    policy = build_default_token_policy(job)
    pack = build_context_pack(job, events, budget=2000, mode="compact")
    specs = list_worker_specs()

    # Determine token mode from job complexity
    task_count = len(job.tasks) if job.tasks else 0
    if task_count == 0 or job.state == RunState.COMPLETED:
        token_mode = "caveman"
    elif task_count <= 2:
        token_mode = "compact"
    else:
        token_mode = "standard"

    # Score candidates: local > external, available > future
    candidates: list[WorkerCandidate] = []
    for spec in specs:
        score = 0
        reason_parts: list[str] = []

        if spec.execution_mode == "local_process":
            score += 50
            reason_parts.append("local")
        elif spec.execution_mode == "external_harness":
            score += 20
            reason_parts.append("external")
        else:
            score += 10
            reason_parts.append("api")

        if spec.status == "available":
            score += 30
            reason_parts.append("available")
        else:
            score += 0
            reason_parts.append("future")

        # Check if roles match job needs
        needs_builder = any(
            t.status == RunState.PENDING for t in (job.tasks or [])
        )
        if needs_builder and "builder" in spec.supported_roles:
            score += 10
            reason_parts.append("builder-capable")

        candidates.append(WorkerCandidate(
            provider_id=spec.provider_id,
            display_name=spec.display_name,
            execution_mode=spec.execution_mode,
            status=spec.status,
            score=score,
            reason=", ".join(reason_parts),
        ))

    candidates.sort(key=lambda c: -c.score)
    best = candidates[0] if candidates else None

    requires_approval = best is not None and best.execution_mode != "local_process"

    return WorkerRecommendation(
        version=1,
        job_id=str(job.id),
        recommended_worker=best.provider_id if best else "none",
        reason=best.reason if best else "no providers available",
        token_mode=token_mode,
        estimated_context_tokens=pack.estimated_tokens,
        requires_approval=requires_approval,
        candidates=tuple(candidates),
    )


def export_worker_recommendation_json(
    rec: WorkerRecommendation,
) -> dict[str, Any]:
    """Export as safe JSON dict."""
    return {
        "version": rec.version,
        "job_id": rec.job_id,
        "recommended_worker": rec.recommended_worker,
        "reason": rec.reason,
        "token_mode": rec.token_mode,
        "estimated_context_tokens": rec.estimated_context_tokens,
        "requires_approval": rec.requires_approval,
        "candidates": [
            {
                "provider_id": c.provider_id,
                "display_name": c.display_name,
                "execution_mode": c.execution_mode,
                "status": c.status,
                "score": c.score,
                "reason": c.reason,
            }
            for c in rec.candidates
        ],
    }


def summarize_worker_recommendation(rec: WorkerRecommendation) -> str:
    """Human-readable summary."""
    lines = [
        f"Worker Recommendation for {rec.job_id[:8]}",
        f"  Recommended: {rec.recommended_worker}",
        f"  Reason: {rec.reason}",
        f"  Token mode: {rec.token_mode}",
        f"  Est. context tokens: {rec.estimated_context_tokens}",
        f"  Requires approval: {rec.requires_approval}",
        "",
        "  Candidates:",
    ]
    for c in rec.candidates:
        lines.append(f"    {c.provider_id} (score={c.score}, {c.reason})")
    return "\n".join(lines)
