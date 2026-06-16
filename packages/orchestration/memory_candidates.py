"""
Memory Candidate v1 — learning candidates that require human approval.

Candidates are derived from repair success, repeated blockers, reviewer
recommendations, command discovery, or token policy results. They are NOT
approved by default — human must approve/reject.

Public API::

    create_candidate(job, kind, summary, evidence_node_ids, confidence) -> dict
    list_candidates(job) -> list[dict]
    approve_candidate(job, candidate_id) -> bool
    reject_candidate(job, candidate_id) -> bool
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

VALID_KINDS = frozenset({
    "repair_pattern", "test_command", "repo_preference",
    "token_policy", "review_note",
})


def create_candidate(
    job: Any,
    kind: str,
    summary: str,
    *,
    evidence_node_ids: list[str] | None = None,
    confidence: str = "medium",
) -> dict[str, Any]:
    """Create a memory candidate and store in job metadata.

    Returns the candidate dict. Does NOT auto-approve.
    Deduplicates by (kind, summary) — returns existing if match found.
    """
    if kind not in VALID_KINDS:
        kind = "review_note"

    candidates = _get_candidates(job)

    # Deduplicate
    for c in candidates:
        if c["kind"] == kind and c["safe_summary"] == summary[:200]:
            return c

    candidate: dict[str, Any] = {
        "id": uuid4().hex[:12],
        "job_id": str(job.id),
        "kind": kind,
        "status": "pending",
        "safe_summary": summary[:200],
        "evidence_node_ids": (evidence_node_ids or [])[:10],
        "confidence": confidence if confidence in ("low", "medium", "high") else "medium",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    candidates.append(candidate)
    _save_candidates(job, candidates)
    return candidate


def list_candidates(job: Any) -> list[dict[str, Any]]:
    """List all memory candidates for a job."""
    return _get_candidates(job)


def approve_candidate(job: Any, candidate_id: str) -> bool:
    """Approve a candidate — creates an approved memory entry."""
    candidates = _get_candidates(job)
    for c in candidates:
        if c["id"] == candidate_id and c["status"] == "pending":
            c["status"] = "approved"
            _save_candidates(job, candidates)
            # Create approved memory via existing memory module
            try:
                from packages.orchestration.memory import store_memory
                store_memory(
                    key=f"learned:{c['kind']}:{c['id']}",
                    value=c["safe_summary"],
                    project_id=None,
                    job_id=str(job.id),
                    tags=[c["kind"], "learned"],
                    approved=True,
                )
            except (ImportError, Exception):
                pass  # Memory module may not exist yet
            return True
    return False


def reject_candidate(job: Any, candidate_id: str) -> bool:
    """Reject a candidate — does NOT create memory."""
    candidates = _get_candidates(job)
    for c in candidates:
        if c["id"] == candidate_id and c["status"] == "pending":
            c["status"] = "rejected"
            _save_candidates(job, candidates)
            return True
    return False


def _get_candidates(job: Any) -> list[dict[str, Any]]:
    if not hasattr(job, "metadata") or not job.metadata:
        return []
    return job.metadata.get("memory_candidates", [])


def _save_candidates(job: Any, candidates: list[dict[str, Any]]) -> None:
    if not hasattr(job, "metadata") or job.metadata is None:
        job.metadata = {}
    job.metadata["memory_candidates"] = candidates
