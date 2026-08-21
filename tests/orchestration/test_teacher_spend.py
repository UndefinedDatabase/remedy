"""Teacher spend lands as ONE ledger row per question, attributed to the role.

These pin DECISION F255 D7 — a teacher question is not a finalized task run, so
its row carries a NULL ``task_id`` and that NULL is the mark of the class — and
the acceptance criterion that ``query_cost(by="role")`` reports teacher spend
separately from mission spend. No network and no model: the writer records
figures it is GIVEN, so every property here is observable offline.
"""

from __future__ import annotations

import sqlite3

from packages.orchestration.teacher_spend import (
    TEACHER_ROLE,
    TeacherUsage,
    record_teacher_question,
)
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    query_cost,
    record_call,
)


def _rows(ledger):
    """Every stored row, as dicts, read straight from SQLite."""
    conn = sqlite3.connect(ledger)
    try:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute("SELECT * FROM calls ORDER BY call_id")]
    finally:
        conn.close()


def test_one_question_writes_one_row_with_a_null_task_id(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    call_id, durable = record_teacher_question(
        model="teacher-model", job_id="job-1", path=ledger
    )

    assert durable is True
    rows = _rows(ledger)
    assert len(rows) == 1
    assert rows[0]["call_id"] == call_id
    assert rows[0]["role"] == TEACHER_ROLE
    assert rows[0]["job_id"] == "job-1"
    assert rows[0]["task_id"] is None


def test_unreported_usage_lands_as_null_never_zero(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    record_teacher_question(model="teacher-model", path=ledger)

    row = _rows(ledger)[0]
    assert row["tokens_in"] is None
    assert row["tokens_out"] is None
    assert row["cost_usd"] is None
    assert row["cost_basis"] == COST_BASIS_UNKNOWN


def test_reported_cost_carries_the_provider_reported_basis(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    record_teacher_question(
        model="teacher-model",
        usage=TeacherUsage(tokens_in=12, tokens_out=3, cost_usd=0.004),
        path=ledger,
    )

    row = _rows(ledger)[0]
    assert row["tokens_in"] == 12
    assert row["tokens_out"] == 3
    assert row["cost_usd"] == 0.004
    assert row["cost_basis"] == COST_BASIS_PROVIDER_REPORTED


def test_two_questions_are_two_rows(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    first, _ = record_teacher_question(model="teacher-model", path=ledger)
    second, _ = record_teacher_question(model="teacher-model", path=ledger)

    assert first != second
    assert len(_rows(ledger)) == 2


def test_query_cost_by_role_reports_teacher_separately(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"
    record_call(
        CallRecord(
            call_id="job-1:task-1",
            job_id="job-1",
            task_id="task-1",
            role="builder",
            model="mission-model",
            ts_utc="2026-08-21T00:00:00+00:00",
            tokens_in=100,
            cost_basis=COST_BASIS_UNKNOWN,
        ),
        path=ledger,
    )
    record_teacher_question(
        model="teacher-model", usage=TeacherUsage(tokens_in=12), path=ledger
    )

    buckets = {row.bucket: row for row in query_cost(path=ledger, by="role").rows}

    assert set(buckets) == {"builder", TEACHER_ROLE}
    assert buckets[TEACHER_ROLE].calls == 1
    assert buckets[TEACHER_ROLE].tokens_in == 12
    assert buckets["builder"].tokens_in == 100
