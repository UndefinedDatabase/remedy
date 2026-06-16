"""
Event persistence result (Steps 1162) — close R-0051 / R-0057.

Important lifecycle events must never be lost silently. Emitters return an
EventPersistenceResult so callers can surface evidence status instead of
swallowing failures and discarding them.

Status values:
  - "complete": the event was durably appended
  - "partial":  best-effort write reported a recoverable issue
  - "failed":   the event could not be persisted
  - "skipped":  the event type was not eligible for emission

No raw exception text is exposed — only safe reason codes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EventPersistenceResult:
    """Outcome of attempting to persist a single important event."""

    event_type: str
    status: str            # complete | partial | failed | skipped
    reason: str = ""       # safe reason code, never raw exception text

    @property
    def persisted(self) -> bool:
        return self.status == "complete"

    @property
    def degraded(self) -> bool:
        return self.status in ("partial", "failed")


def emit_important_event(
    data_dir,
    job_id: str,
    event_type: str,
    metadata: dict,
    *,
    eligible: frozenset[str] | set[str] | None = None,
) -> EventPersistenceResult:
    """Append an important event, returning a structured persistence result.

    Never raises and never leaks raw exception text. When *eligible* is given
    and *event_type* is not a member, the event is reported as "skipped".
    """
    if eligible is not None and event_type not in eligible:
        return EventPersistenceResult(event_type, "skipped", "not_eligible")
    try:
        from uuid import UUID

        from packages.orchestration.timeline import append_run_event
        try:
            UUID(str(job_id))
        except (ValueError, TypeError):
            return EventPersistenceResult(event_type, "failed", "invalid_job_id")
        append_run_event(str(data_dir), job_id, event=event_type, metadata=metadata)
        return EventPersistenceResult(event_type, "complete")
    except (OSError, ValueError, TypeError):
        return EventPersistenceResult(event_type, "failed", "append_failed")
    except Exception:
        # Defensive: any unexpected error is surfaced as a failed status, not raised.
        return EventPersistenceResult(event_type, "failed", "unexpected")
