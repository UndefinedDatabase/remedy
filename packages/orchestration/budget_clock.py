"""The working wall clock of a job (F310, DECISION F310 D4); it began as step (1) of the boundary of ``decode_persisted_budget_actuals`` on the structure page, the start instant's checks moved out of that decoder unchanged."""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

from packages.orchestration.budget_guard import BudgetCounterError


# The persisted start instant's checks, moved unchanged out of decode_persisted_budget_actuals.
def decode_persisted_started_at(sa_raw: Any, first_running_at: str | None) -> datetime:
    """Parse a persisted start instant and check it against the job's first-run instant."""
    if not isinstance(sa_raw, str) or not sa_raw:
        raise BudgetCounterError(
            f"persisted started_at must be a nonempty string, got {sa_raw!r}")
    try:
        sa_parsed = datetime.fromisoformat(sa_raw)
    except (ValueError, TypeError) as exc:
        raise BudgetCounterError(
            f"persisted started_at cannot be parsed: {sa_raw!r}: {exc}")
    if sa_parsed.tzinfo is None:
        raise BudgetCounterError(
            f"persisted started_at is timezone-naive: {sa_raw!r}")

    if first_running_at is not None:
        try:
            fra_parsed = datetime.fromisoformat(first_running_at)
        except (ValueError, TypeError) as exc:
            raise BudgetCounterError(
                f"first_running_at cannot be parsed: {first_running_at!r}: {exc}")
        if fra_parsed.tzinfo is None:
            raise BudgetCounterError(
                f"first_running_at is timezone-naive: {first_running_at!r}")
        if sa_parsed != fra_parsed:
            raise BudgetCounterError(
                f"persisted started_at ({sa_raw}) != "
                f"first_running_at ({first_running_at}): wall-clock split")
    return sa_parsed


# A job's first-run instant cannot be read, so its clock cannot be resumed.
class BudgetClockError(ValueError):
    """The job's first-run instant is unparsable or timezone-naive."""


def _parse_aware(text: Any, start: datetime | None = None) -> datetime | None:
    """The timezone-aware instant *text* spells, or None when it is not one (or precedes *start*)."""
    if not isinstance(text, str) or not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except (ValueError, TypeError):
        return None
    if parsed.tzinfo is None or (start is not None and parsed < start):
        return None
    return parsed


# The persisted record's whole clock: the start instant, the seconds waited and the last active moment.
def decode_persisted_clock(
    raw: dict[str, Any], first_running_at: str | None,
) -> tuple[datetime, float, datetime | None]:
    """Decode a record's clock fields; a record without ``waited_s`` waited nothing and was never active."""
    start = decode_persisted_started_at(raw["started_at"], first_running_at)
    if "waited_s" not in raw:
        return start, 0.0, None
    waited = raw["waited_s"]
    if isinstance(waited, bool) or not isinstance(waited, (int, float)):
        raise BudgetCounterError(f"persisted waited_s has type {type(waited).__name__}")
    if not math.isfinite(waited) or waited < 0:
        raise BudgetCounterError(f"persisted waited_s is not a finite non-negative number: {waited!r}")
    until_raw = raw.get("active_until")
    if not isinstance(until_raw, str) or not until_raw:
        raise BudgetCounterError(f"persisted active_until must be a nonempty string, got {until_raw!r}")
    try:
        until = datetime.fromisoformat(until_raw)
    except (ValueError, TypeError) as exc:
        raise BudgetCounterError(f"persisted active_until cannot be parsed: {until_raw!r}: {exc}")
    if until.tzinfo is None:
        raise BudgetCounterError(f"persisted active_until is timezone-naive: {until_raw!r}")
    if until < start:
        raise BudgetCounterError(
            f"persisted active_until ({until_raw}) is before started_at ({start.isoformat()})")
    return start, float(waited), until


# Every gap between two runs is waiting: a resume adds the time since the job was last active.
def resume_job_clock(
    job: Any, prior: dict[str, Any], *, now: datetime | None = None,
) -> tuple[datetime, float]:
    """``(first run instant, seconds waited)`` for a run starting at *now*; upgrades the job's record to version 3."""
    if now is None:
        now = datetime.now(timezone.utc)
    raw = getattr(job, "first_running_at", "")
    if not raw:
        return now, 0.0
    try:
        first = datetime.fromisoformat(raw)
    except (ValueError, TypeError) as exc:
        raise BudgetClockError(f"cannot parse {raw!r}: {exc}")
    if first.tzinfo is None:
        raise BudgetClockError(f"timezone-naive value {raw!r}")
    last = prior.get("active_until") or _parse_aware(getattr(job, "stopped_at", ""), first)
    waited = prior.get("waited_s", 0.0)
    if last is not None:
        waited += max(0.0, (now - last).total_seconds())
    record = getattr(job, "budget_actuals", None)
    if prior and isinstance(record, dict):
        upgraded = dict(record)
        upgraded["schema_version"] = "3.0.0"
        upgraded.setdefault("measured_cost_usd", None)
        upgraded.setdefault("priced_call_count", 0)
        upgraded.setdefault("unpriced_call_count", 0)
        upgraded["waited_s"] = waited
        upgraded["active_until"] = now.isoformat()
        job.budget_actuals = upgraded
    return first, waited


# The instant a job's wall clock effectively began: its first run plus every second it spent waiting.
def job_work_start(job: Any) -> datetime | None:
    """The first-run instant moved forward by the recorded waiting, or None before the first run."""
    raw = getattr(job, "first_running_at", "")
    if not raw:
        return None
    first = datetime.fromisoformat(raw)
    if first.tzinfo is None:
        raise ValueError(f"timezone-naive value {raw!r}")
    record = getattr(job, "budget_actuals", None)
    waited = record.get("waited_s") if isinstance(record, dict) else None
    if isinstance(waited, bool) or not isinstance(waited, (int, float)) or not math.isfinite(waited) or waited < 0:
        return first
    return first + timedelta(seconds=waited)
