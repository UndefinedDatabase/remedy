"""F103 T001 — the SQLite token ledger: schema, writer, and the never-fail rule.

What the feature file requires proof of:

  * the schema bootstraps to ``SCHEMA_VERSION``, in WAL mode, with the three
    covering indexes the query patterns need (job_id; ts_utc; role+model);
  * opening an already-current ledger changes nothing — the bootstrap is a
    migration, not a rewrite;
  * a call round-trips through disk with every field intact, nullables included;
  * a call with NO reported usage lands as NULL counts with basis ``unknown`` —
    never a fabricated zero and never an invented price;
  * recording the same ``call_id`` twice leaves ONE row and reports success both
    times, which is what makes T002's backfill idempotent;
  * a ledger write that FAILS never fails the run: no exception escapes, the
    return is False, the miss is counted and an ERROR is logged (the
    Orchestrator brief demands a test for exactly this);
  * a reader still reads while a write is in flight — the WAL guarantee.

Every test writes inside ``tmp_path`` and passes ``root=``/``path=``
explicitly. ``REMEDY_DATA_DIR`` is never mutated and the repository's real data
root is never touched.
"""

from __future__ import annotations

import logging
import os
import sqlite3
from uuid import UUID, uuid4

import pytest

from packages.orchestration.token_ledger import (
    COST_BASES,
    COST_BASIS_PRICE_TABLE,
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    LEDGER_FILENAME,
    SCHEMA_VERSION,
    SCHEMA_VERSION_KEY,
    CallRecord,
    ledger_miss_count,
    open_ledger,
    record_call,
    reset_ledger_miss_count,
    token_ledger_path_for,
)

LEDGER_LOGGER = "packages.orchestration.token_ledger"

# The three indexes the feature file names as the query patterns to cover.
EXPECTED_INDEXES = {
    "idx_calls_job_id",
    "idx_calls_ts_utc",
    "idx_calls_role_model",
}


@pytest.fixture(autouse=True)
def _reset_miss_counter():
    """Keep the process-level miss counter from leaking between tests."""
    reset_ledger_miss_count()
    yield
    reset_ledger_miss_count()


@pytest.fixture
def ledger_path(tmp_path):
    """A ledger path two directories deep, so parent creation is exercised."""
    return tmp_path / "projects" / str(uuid4()) / LEDGER_FILENAME


def _schema_objects(conn, kind):
    return {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type = ?", (kind,)
    )}


def _meta_version(conn):
    row = conn.execute(
        "SELECT value FROM meta WHERE key = ?", (SCHEMA_VERSION_KEY,)
    ).fetchone()
    return None if row is None else int(row[0])


class TestOpenLedger:
    def test_creates_file_meta_wal_and_indexes(self, ledger_path):
        conn = open_ledger(ledger_path)
        try:
            assert ledger_path.exists()
            assert _meta_version(conn) == SCHEMA_VERSION
            journal = conn.execute("PRAGMA journal_mode").fetchone()[0]
            assert journal.lower() == "wal"
            assert {"meta", "calls"} <= _schema_objects(conn, "table")
            assert EXPECTED_INDEXES <= _schema_objects(conn, "index")
        finally:
            conn.close()

    def test_open_is_idempotent(self, ledger_path):
        first = open_ledger(ledger_path)
        try:
            before_tables = _schema_objects(first, "table")
            before_indexes = _schema_objects(first, "index")
            before_meta = sorted(first.execute("SELECT key, value FROM meta"))
        finally:
            first.close()

        second = open_ledger(ledger_path)
        try:
            assert _schema_objects(second, "table") == before_tables
            assert _schema_objects(second, "index") == before_indexes
            assert sorted(second.execute("SELECT key, value FROM meta")) == before_meta
            assert _meta_version(second) == SCHEMA_VERSION
        finally:
            second.close()

    def test_schema_version_matches_the_last_migration_step(self):
        """A bumped SCHEMA_VERSION without a migration step would never apply."""
        from packages.orchestration.token_ledger import _MIGRATIONS
        assert max(_MIGRATIONS) == SCHEMA_VERSION
        assert sorted(_MIGRATIONS) == list(range(1, SCHEMA_VERSION + 1))

    def test_meta_holds_exactly_one_version_row(self, ledger_path):
        open_ledger(ledger_path).close()
        conn = open_ledger(ledger_path)
        try:
            rows = conn.execute("SELECT key, value FROM meta").fetchall()
            assert rows == [(SCHEMA_VERSION_KEY, str(SCHEMA_VERSION))]
        finally:
            conn.close()


class TestRecordCall:
    def test_round_trips_every_field(self, ledger_path):
        record = CallRecord(
            call_id="call-0001",
            job_id="job-42",
            task_id="task-7",
            role="reviewer",
            model="claude-opus-5",
            ts_utc="2026-08-08T12:00:00Z",
            tokens_in=1234,
            tokens_out=567,
            cache_read=89,
            cache_write=10,
            cost_usd=0.4213,
            cost_basis=COST_BASIS_PROVIDER_REPORTED,
            evidence_ref="jobs/job-42/calls/call-0001.json",
        )
        assert record_call(record, path=ledger_path) is True

        conn = open_ledger(ledger_path)
        try:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM calls WHERE call_id = ?",
                               (record.call_id,)).fetchone()
        finally:
            conn.close()

        assert row["job_id"] == "job-42"
        assert row["task_id"] == "task-7"
        assert row["role"] == "reviewer"
        assert row["model"] == "claude-opus-5"
        assert row["ts_utc"] == "2026-08-08T12:00:00Z"
        assert row["tokens_in"] == 1234
        assert row["tokens_out"] == 567
        assert row["cache_read"] == 89
        assert row["cache_write"] == 10
        assert row["cost_usd"] == pytest.approx(0.4213)
        assert row["cost_basis"] == COST_BASIS_PROVIDER_REPORTED
        assert row["evidence_ref"] == "jobs/job-42/calls/call-0001.json"
        assert ledger_miss_count() == 0

    def test_nullable_fields_round_trip_as_null(self, ledger_path):
        record = CallRecord(call_id="call-nulls", ts_utc="2026-08-08T12:00:00Z")
        assert record_call(record, path=ledger_path) is True

        conn = open_ledger(ledger_path)
        try:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM calls WHERE call_id = ?",
                               (record.call_id,)).fetchone()
        finally:
            conn.close()

        for column in ("job_id", "task_id", "role", "model", "evidence_ref"):
            assert row[column] is None, column

    def test_unmeasured_call_is_null_and_unknown(self, ledger_path):
        """No reported usage → NULL counts and basis unknown, never a fake zero."""
        record = CallRecord(call_id="call-unmeasured", ts_utc="2026-08-08T12:00:00Z")
        assert record.cost_basis == COST_BASIS_UNKNOWN
        assert record_call(record, path=ledger_path) is True

        conn = open_ledger(ledger_path)
        try:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM calls WHERE call_id = ?",
                               (record.call_id,)).fetchone()
        finally:
            conn.close()

        for column in ("tokens_in", "tokens_out", "cache_read", "cache_write"):
            assert row[column] is None, f"{column} must be NULL, not a fabricated zero"
        assert row["cost_usd"] is None, "cost must stay NULL rather than invent a price"
        assert row["cost_basis"] == COST_BASIS_UNKNOWN

    def test_same_call_id_twice_leaves_one_row(self, ledger_path):
        first = CallRecord(
            call_id="call-dup",
            ts_utc="2026-08-08T12:00:00Z",
            tokens_in=10,
            cost_basis=COST_BASIS_PRICE_TABLE,
            cost_usd=0.5,
        )
        assert record_call(first, path=ledger_path) is True
        # Re-recording an already durable call is a no-op, not a failure — this
        # is what makes T002's backfill idempotent.
        assert record_call(first, path=ledger_path) is True

        conn = open_ledger(ledger_path)
        try:
            assert conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0] == 1
            assert conn.execute(
                "SELECT tokens_in FROM calls WHERE call_id = ?", ("call-dup",)
            ).fetchone()[0] == 10
        finally:
            conn.close()
        assert ledger_miss_count() == 0

    def test_resolves_path_from_project_id(self, tmp_path, monkeypatch):
        # Redirect the data root at the module's own seam rather than by setting
        # REMEDY_DATA_DIR: data_paths.py stays the single authoritative reader.
        monkeypatch.setattr(
            "packages.orchestration.token_ledger.projects_dir",
            lambda root=None: tmp_path / "projects",
        )
        project_id = uuid4()
        record = CallRecord(call_id="call-by-project", ts_utc="2026-08-08T12:00:00Z")
        assert record_call(record, project_id=project_id) is True
        assert (tmp_path / "projects" / str(project_id) / LEDGER_FILENAME).exists()


class TestNeverFailTheRun:
    """The Orchestrator brief requires a test for the never-fail-the-run rule."""

    @pytest.fixture
    def readonly_ledger(self, tmp_path):
        """A real, initialised ledger made unwritable — restored on teardown."""
        path = tmp_path / "readonly" / LEDGER_FILENAME
        open_ledger(path).close()
        original = {path: path.stat().st_mode, path.parent: path.parent.stat().st_mode}
        path.chmod(0o444)
        path.parent.chmod(0o555)
        try:
            yield path
        finally:
            for target, mode in original.items():
                try:
                    target.chmod(mode)
                except OSError:  # pragma: no cover - nothing left to restore
                    pass

    @pytest.mark.skipif(
        getattr(os, "geteuid", lambda: 1)() == 0,
        reason="root ignores file permissions, so a read-only DB cannot be simulated",
    )
    def test_readonly_database_is_a_counted_miss(self, readonly_ledger, caplog):
        record = CallRecord(call_id="call-readonly", ts_utc="2026-08-08T12:00:00Z")
        before = ledger_miss_count()

        with caplog.at_level(logging.ERROR, logger=LEDGER_LOGGER):
            result = record_call(record, path=readonly_ledger)

        assert result is False
        assert ledger_miss_count() == before + 1
        errors = [r for r in caplog.records
                  if r.levelno >= logging.ERROR and r.name == LEDGER_LOGGER]
        assert errors, "a ledger write failure must be logged loudly at ERROR"
        assert "call-readonly" in errors[0].getMessage()

    def test_uncreatable_path_is_a_counted_miss(self, tmp_path, caplog):
        """A path whose parent is a regular file can never be created."""
        blocker = tmp_path / "not-a-directory"
        blocker.write_text("this is a file, not a directory\n", encoding="utf-8")
        record = CallRecord(call_id="call-nopath", ts_utc="2026-08-08T12:00:00Z")
        before = ledger_miss_count()

        with caplog.at_level(logging.ERROR, logger=LEDGER_LOGGER):
            result = record_call(record, path=blocker / "sub" / LEDGER_FILENAME)

        assert result is False
        assert ledger_miss_count() == before + 1
        assert any(r.name == LEDGER_LOGGER and r.levelno >= logging.ERROR
                   for r in caplog.records)

    def test_missing_target_is_a_counted_miss(self, caplog):
        """Neither project_id nor path: a failure like any other, never a raise."""
        record = CallRecord(call_id="call-notarget", ts_utc="2026-08-08T12:00:00Z")
        before = ledger_miss_count()

        with caplog.at_level(logging.ERROR, logger=LEDGER_LOGGER):
            result = record_call(record)

        assert result is False
        assert ledger_miss_count() == before + 1

    def test_rejected_basis_is_a_counted_miss_not_a_silent_drop(
        self, ledger_path, caplog
    ):
        """An unknown cost_basis must not be reported as durable."""
        record = CallRecord(
            call_id="call-badbasis",
            ts_utc="2026-08-08T12:00:00Z",
            cost_basis="made-up-basis",
        )
        assert record.cost_basis not in COST_BASES
        before = ledger_miss_count()

        with caplog.at_level(logging.ERROR, logger=LEDGER_LOGGER):
            result = record_call(record, path=ledger_path)

        assert result is False
        assert ledger_miss_count() == before + 1

        conn = open_ledger(ledger_path)
        try:
            assert conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0] == 0
        finally:
            conn.close()

    def test_miss_counter_resets(self):
        record_call(CallRecord(call_id="call-reset-probe", ts_utc="2026-08-08T12:00:00Z"))
        assert ledger_miss_count() >= 1
        reset_ledger_miss_count()
        assert ledger_miss_count() == 0


class TestConcurrentReadDuringWrite:
    def test_reader_reads_while_a_write_is_open(self, ledger_path):
        """WAL: an in-flight write must not block a concurrent reader."""
        assert record_call(
            CallRecord(call_id="call-before", ts_utc="2026-08-08T12:00:00Z"),
            path=ledger_path,
        ) is True

        reader = open_ledger(ledger_path)
        writer = open_ledger(ledger_path)
        try:
            writer.execute("BEGIN IMMEDIATE")
            writer.execute(
                "INSERT INTO calls (call_id, ts_utc, cost_basis) VALUES (?, ?, ?)",
                ("call-during", "2026-08-08T12:00:01Z", COST_BASIS_UNKNOWN),
            )
            # The write is open and uncommitted; the reader must still answer,
            # and must see the pre-write snapshot rather than a dirty row.
            visible = reader.execute("SELECT call_id FROM calls").fetchall()
            assert visible == [("call-before",)]

            # A brand-new reader opened mid-write must also succeed.
            late_reader = open_ledger(ledger_path)
            try:
                assert late_reader.execute(
                    "SELECT COUNT(*) FROM calls"
                ).fetchone()[0] == 1
            finally:
                late_reader.close()

            writer.commit()
            assert reader.execute("SELECT COUNT(*) FROM calls").fetchone()[0] == 2
        finally:
            writer.close()
            reader.close()


class TestTokenLedgerPathFor:
    def test_uses_projects_dir_under_the_given_root(self, tmp_path):
        project_id = uuid4()
        assert token_ledger_path_for(project_id, root=tmp_path) == (
            tmp_path / "projects" / str(project_id) / "ledger.sqlite"
        )

    def test_accepts_uuid_and_str_alike(self, tmp_path):
        project_id = uuid4()
        from_uuid = token_ledger_path_for(project_id, root=tmp_path)
        from_str = token_ledger_path_for(str(project_id), root=tmp_path)
        assert from_uuid == from_str
        assert isinstance(project_id, UUID)

    def test_does_not_create_anything(self, tmp_path):
        path = token_ledger_path_for(uuid4(), root=tmp_path)
        assert not path.exists()
        assert not path.parent.exists()
