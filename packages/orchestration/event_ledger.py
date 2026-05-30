"""
Audit/Event Ledger v1 — safe normalized event query surface.

Reads run logs and exports safe, redacted, deterministic event records.
No raw stdout/stderr, no command output, no file content, no diff preview,
no approval reason, no traceback.

Public API::

    list_events(job_id, events, *, event_type, since, limit) -> list[LedgerEvent]
    get_event(job_id, events, event_id) -> LedgerEvent | None
    build_event_timeline(job_id, events) -> EventTimeline
    build_event_summary(events) -> EventSummary
    export_ledger_event_json(event) -> dict
    export_event_timeline_json(timeline) -> dict
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

# Fields that must never appear in ledger metadata
_REDACT_KEYS = frozenset({
    "stdout", "stderr", "raw_output", "command_output",
    "diff_preview", "approval_reason", "traceback", "content",
    "raw_content", "file_content", "workspace_content",
})


@dataclass(frozen=True)
class LedgerEvent:
    """Normalized, safe event record."""

    event_id: str
    event_type: str
    job_id: str
    run_id: str
    timestamp: str
    scope: str
    outcome: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class EventTimeline:
    """Timeline of safe events for a job."""

    version: int
    job_id: str
    event_count: int
    events: tuple[LedgerEvent, ...]


@dataclass(frozen=True)
class EventSummary:
    """Aggregate summary of events — no individual event data."""

    event_count: int
    type_counts: dict[str, int]
    failed_count: int
    proof_count: int
    test_count: int
    last_event_at: str


def _make_event_id(run_id: str, index: int) -> str:
    """Deterministic event ID from run_id + line index."""
    raw = f"{run_id}:{index}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _redact_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    """Strip unsafe keys from metadata."""
    return {k: v for k, v in meta.items() if k not in _REDACT_KEYS}


def _normalize_event(raw: dict[str, Any], index: int) -> LedgerEvent:
    """Convert raw run-log dict to safe LedgerEvent."""
    run_id = str(raw.get("run_id", ""))
    event_id = _make_event_id(run_id, index)
    event_type = str(raw.get("event", "unknown"))
    job_id = str(raw.get("job_id", ""))
    timestamp = str(raw.get("timestamp", ""))
    outcome = str(raw.get("outcome", ""))

    # Derive scope from event type
    if event_type.startswith("patch_"):
        scope = "patch"
    elif event_type.startswith("test_"):
        scope = "test"
    elif event_type.startswith("agent_"):
        scope = "agent"
    elif event_type.startswith("memory_"):
        scope = "memory"
    elif event_type.startswith("token_"):
        scope = "policy"
    elif event_type.startswith("git_"):
        scope = "repo"
    else:
        scope = "system"

    safe_meta = _redact_metadata(raw.get("metadata", {}))

    return LedgerEvent(
        event_id=event_id,
        event_type=event_type,
        job_id=job_id,
        run_id=run_id,
        timestamp=timestamp,
        scope=scope,
        outcome=outcome,
        metadata=safe_meta,
    )


def list_events(
    job_id: str,
    events: list[dict[str, Any]],
    *,
    event_type: str | None = None,
    since: str | None = None,
    limit: int = 50,
) -> list[LedgerEvent]:
    """List normalized events with optional filtering."""
    result: list[LedgerEvent] = []
    for i, raw in enumerate(events):
        le = _normalize_event(raw, i)
        if event_type and le.event_type != event_type:
            continue
        if since and le.timestamp < since:
            continue
        result.append(le)
        if len(result) >= limit:
            break
    return result


def get_event(
    job_id: str,
    events: list[dict[str, Any]],
    event_id: str,
) -> LedgerEvent | None:
    """Find a specific event by ID."""
    for i, raw in enumerate(events):
        le = _normalize_event(raw, i)
        if le.event_id == event_id:
            return le
    return None


def build_event_timeline(
    job_id: str,
    events: list[dict[str, Any]],
) -> EventTimeline:
    """Build full timeline of safe events."""
    ledger_events = [_normalize_event(raw, i) for i, raw in enumerate(events)]
    return EventTimeline(
        version=1,
        job_id=job_id,
        event_count=len(ledger_events),
        events=tuple(ledger_events),
    )


def build_event_summary(events: list[dict[str, Any]]) -> EventSummary:
    """Build aggregate summary — no individual event data."""
    type_counts: dict[str, int] = {}
    failed = 0
    proof = 0
    test = 0
    last_ts = ""

    for raw in events:
        et = str(raw.get("event", "unknown"))
        type_counts[et] = type_counts.get(et, 0) + 1
        outcome = str(raw.get("outcome", ""))
        if outcome in ("failed", "error"):
            failed += 1
        if "proof" in et:
            proof += 1
        if "test" in et:
            test += 1
        ts = str(raw.get("timestamp", ""))
        if ts > last_ts:
            last_ts = ts

    return EventSummary(
        event_count=len(events),
        type_counts=type_counts,
        failed_count=failed,
        proof_count=proof,
        test_count=test,
        last_event_at=last_ts,
    )


def export_ledger_event_json(event: LedgerEvent) -> dict[str, Any]:
    """Export single event as safe JSON dict."""
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "job_id": event.job_id,
        "run_id": event.run_id,
        "timestamp": event.timestamp,
        "scope": event.scope,
        "outcome": event.outcome,
        "metadata": event.metadata,
    }


def export_event_timeline_json(timeline: EventTimeline) -> dict[str, Any]:
    """Export timeline as safe JSON dict."""
    return {
        "version": timeline.version,
        "job_id": timeline.job_id,
        "event_count": timeline.event_count,
        "events": [export_ledger_event_json(e) for e in timeline.events],
    }
