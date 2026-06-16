"""
Stop Reasons + Recovery Queue v1 — structured stop/blocker tracking.

When Remedy stops, blocks, or fails, it records exactly why and what
safe action is next. No raw output.

Public API::

    StopReason — frozen dataclass
    create_stop_reason(job_id, ...) -> StopReason
    list_stop_reasons(job_id) -> list[StopReason]
    get_stop_reason(job_id, stop_id) -> StopReason | None
    resolve_stop_reason(job_id, stop_id, reason) -> StopReason | None
    derive_stop_reasons(job, events) -> list[StopReason]
    export_stop_reason_json(sr) -> dict
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.data_paths import resolve_data_root

# Valid reason codes
REASON_CODES = frozenset({
    "not_approved",
    "missing_permission",
    "test_failed",
    "no_target_repo",
    "unsafe_path",
    "unsupported_file_type",
    "dirty_repo_blocks_level",
    "token_budget_exceeded",
    "no_safe_worker",
    "missing_snapshot",
    "pending_human_decision",
    "external_provider_requires_approval",
})


@dataclass
class StopReason:
    """A structured stop/blocker record."""

    id: str
    job_id: str
    source: str
    reason_code: str
    severity: str  # info, warning, blocker
    status: str  # active, resolved
    created_at: str
    resolved_at: str | None
    related_node_id: str
    related_intent_id: str
    related_file: str
    safe_summary: str
    next_actions: tuple[str, ...]


def _stops_path(job_id: str) -> Path:
    """Path to stops JSONL file for a job."""
    root = resolve_data_root()
    return root / "stops" / f"{job_id}.jsonl"


def _load_stops(job_id: str) -> list[StopReason]:
    """Load all stop reasons for a job."""
    path = _stops_path(job_id)
    if not path.exists():
        return []
    stops: list[StopReason] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
            stops.append(StopReason(
                id=d["id"],
                job_id=d["job_id"],
                source=d.get("source", ""),
                reason_code=d.get("reason_code", ""),
                severity=d.get("severity", "blocker"),
                status=d.get("status", "active"),
                created_at=d.get("created_at", ""),
                resolved_at=d.get("resolved_at"),
                related_node_id=d.get("related_node_id", ""),
                related_intent_id=d.get("related_intent_id", ""),
                related_file=d.get("related_file", ""),
                safe_summary=d.get("safe_summary", ""),
                next_actions=tuple(d.get("next_actions", ())),
            ))
        except (json.JSONDecodeError, KeyError):
            pass
    return stops


def _save_stops(job_id: str, stops: list[StopReason]) -> None:
    """Write all stop reasons for a job."""
    path = _stops_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for s in stops:
        d = {
            "id": s.id, "job_id": s.job_id, "source": s.source,
            "reason_code": s.reason_code, "severity": s.severity,
            "status": s.status, "created_at": s.created_at,
            "resolved_at": s.resolved_at,
            "related_node_id": s.related_node_id,
            "related_intent_id": s.related_intent_id,
            "related_file": s.related_file,
            "safe_summary": s.safe_summary,
            "next_actions": list(s.next_actions),
        }
        lines.append(json.dumps(d, separators=(",", ":")))
    path.write_text("\n".join(lines) + "\n" if lines else "")


def create_stop_reason(
    job_id: str,
    *,
    source: str,
    reason_code: str,
    severity: str = "blocker",
    safe_summary: str,
    next_actions: tuple[str, ...] = (),
    related_node_id: str = "",
    related_intent_id: str = "",
    related_file: str = "",
) -> StopReason:
    """Create and persist a stop reason."""
    sr = StopReason(
        id=uuid4().hex[:16],
        job_id=job_id,
        source=source,
        reason_code=reason_code,
        severity=severity,
        status="active",
        created_at=datetime.now(timezone.utc).isoformat(),
        resolved_at=None,
        related_node_id=related_node_id,
        related_intent_id=related_intent_id,
        related_file=related_file,
        safe_summary=safe_summary,
        next_actions=next_actions,
    )
    stops = _load_stops(job_id)
    stops.append(sr)
    _save_stops(job_id, stops)
    return sr


def list_stop_reasons(job_id: str) -> list[StopReason]:
    """List all stop reasons for a job."""
    return _load_stops(job_id)


def get_stop_reason(job_id: str, stop_id: str) -> StopReason | None:
    """Find a specific stop reason by ID."""
    for s in _load_stops(job_id):
        if s.id == stop_id:
            return s
    return None


def resolve_stop_reason(job_id: str, stop_id: str, reason: str) -> StopReason | None:
    """Resolve a stop reason."""
    stops = _load_stops(job_id)
    target = None
    for s in stops:
        if s.id == stop_id:
            s.status = "resolved"
            s.resolved_at = datetime.now(timezone.utc).isoformat()
            target = s
            break
    if target is None:
        return None
    _save_stops(job_id, stops)
    return target


def derive_stop_reasons(
    job: Any,
    events: list[dict[str, Any]],
) -> list[StopReason]:
    """Derive stop reasons from job state and events. Does not persist."""

    reasons: list[StopReason] = []
    job_id = str(job.id)
    now = datetime.now(timezone.utc).isoformat()

    # No target repo
    target_repo = (job.metadata or {}).get("target_repo", "")
    if not target_repo:
        reasons.append(StopReason(
            id="derived_no_repo", job_id=job_id, source="readiness",
            reason_code="no_target_repo", severity="blocker", status="active",
            created_at=now, resolved_at=None,
            related_node_id="", related_intent_id="", related_file="",
            safe_summary="No target repository attached to job.",
            next_actions=("remedy job attach-repo <job_id> <path>",),
        ))

    # Test failures
    test_fails = [e for e in events
                  if e.get("event") == "test_run_completed"
                  and e.get("metadata", {}).get("status") == "failed"]
    if test_fails:
        reasons.append(StopReason(
            id="derived_test_fail", job_id=job_id, source="test_run",
            reason_code="test_failed", severity="blocker", status="active",
            created_at=now, resolved_at=None,
            related_node_id="", related_intent_id="", related_file="",
            safe_summary=f"{len(test_fails)} test run(s) failed.",
            next_actions=("Review test output.", "remedy test run <job_id>"),
        ))

    # Unapproved intents
    unapproved = [e for e in events
                  if e.get("event") == "patch_intent_created"
                  and not any(
                      a.get("event") == "approval_decision"
                      and a.get("metadata", {}).get("intent_id") == e.get("metadata", {}).get("intent_id")
                      for a in events
                  )]
    if unapproved:
        reasons.append(StopReason(
            id="derived_not_approved", job_id=job_id, source="approval",
            reason_code="not_approved", severity="blocker", status="active",
            created_at=now, resolved_at=None,
            related_node_id="", related_intent_id="", related_file="",
            safe_summary=f"{len(unapproved)} patch intent(s) awaiting approval.",
            next_actions=("remedy patch approve <job_id> <intent_id>",),
        ))

    # Dirty repo blocks higher levels
    git_reads = [e for e in events if e.get("event") == "git_status_read"]
    if git_reads:
        last = git_reads[-1].get("metadata", {})
        if last.get("dirty"):
            reasons.append(StopReason(
                id="derived_dirty_repo", job_id=job_id, source="git_status",
                reason_code="dirty_repo_blocks_level", severity="warning",
                status="active", created_at=now, resolved_at=None,
                related_node_id="", related_intent_id="", related_file="",
                safe_summary="Target repository has uncommitted changes.",
                next_actions=("Commit or stash changes in target repo.",),
            ))

    return reasons


def export_stop_reason_json(sr: StopReason) -> dict[str, Any]:
    """Export as safe JSON dict."""
    return {
        "id": sr.id,
        "job_id": sr.job_id,
        "source": sr.source,
        "reason_code": sr.reason_code,
        "severity": sr.severity,
        "status": sr.status,
        "created_at": sr.created_at,
        "resolved_at": sr.resolved_at,
        "related_node_id": sr.related_node_id,
        "related_intent_id": sr.related_intent_id,
        "related_file": sr.related_file,
        "safe_summary": sr.safe_summary,
        "next_actions": list(sr.next_actions),
    }
