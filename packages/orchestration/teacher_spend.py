"""
Teacher spend — the ledger row one answered teacher question produces (F255 T004).

Stage 2 calls a model, so Stage 2 costs money, and DECISION F255 D3 rules that
teacher spend is REPORTED through the ``role`` column the F103 ledger already
carries rather than capped by a new budget axis. This module is the one place
that builds such a row, so no caller assembles a ``CallRecord`` of its own.

WHY THIS IS NOT THE ACTUALS PATH: DECISION F255 D7, which states the argument in
full. In short, ``token_ledger`` documents a row as one FINALIZED TASK RUN keyed
``"<job_id>:<task_id>"``; a teacher question is neither, so D7 widens that
identity by one class — a NULL ``task_id`` MARKS the teacher row — rather than
invent the task id and the evidence file the actuals path exists to refuse.

Remedy deliberately records NULL counts rather than zeros when a reply reports no
usage, matching ``token_ledger``'s own rule: a fabricated zero is worse than an
honest unknown, because a zero sums and an unknown does not.

Public API:: ``TEACHER_ROLE``, ``TeacherUsage``, ``record_teacher_question``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    record_call,
)

#: The role name teacher spend is attributed to. Spelled once here so the ledger
#: row, the query that reports it and the tests cannot drift apart.
TEACHER_ROLE = "teacher"


@dataclass(frozen=True)
class TeacherUsage:
    """What one teacher reply reported about its own cost.

    Every field is optional because a provider that reports nothing must land as
    NULL. There is no default of zero anywhere in this class.
    """

    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None


def record_teacher_question(
    *,
    model: str,
    usage: TeacherUsage | None = None,
    job_id: str | None = None,
    path: Path | str | None = None,
    project_id: str | None = None,
    call_id: str | None = None,
    ts_utc: str | None = None,
) -> tuple[str, bool]:
    """Record ONE ledger row for ONE answered teacher question.

    Returns the row's ``call_id`` and whether it is durable. Never raises:
    ``record_call`` already absorbs every failure, and a teacher that could break
    a run by failing to bill itself would not be the passive role F255 specifies.

    ``task_id`` is deliberately NOT a parameter: it is always NULL, and making it
    settable would let a caller disguise a question as a task run (F255 D7).
    """
    reported = usage or TeacherUsage()
    record = CallRecord(
        call_id=call_id or f"teacher:{uuid.uuid4()}",
        job_id=job_id,
        task_id=None,
        role=TEACHER_ROLE,
        model=model,
        ts_utc=ts_utc or datetime.now(timezone.utc).isoformat(),
        tokens_in=reported.tokens_in,
        tokens_out=reported.tokens_out,
        cost_usd=reported.cost_usd,
        cost_basis=(
            COST_BASIS_PROVIDER_REPORTED
            if reported.cost_usd is not None
            else COST_BASIS_UNKNOWN
        ),
    )
    return record.call_id, record_call(record, project_id=project_id, path=path)
