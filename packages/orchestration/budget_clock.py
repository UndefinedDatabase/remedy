"""The working wall clock of a job (F310, DECISION F310 D4); it began as step (1) of the boundary of ``decode_persisted_budget_actuals`` on the structure page, the start instant's checks moved out of that decoder unchanged."""
from __future__ import annotations

from datetime import datetime
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
