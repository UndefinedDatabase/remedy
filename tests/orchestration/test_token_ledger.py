"""F103 T001/T002 — the SQLite token ledger: schema, writer, backfill, reconcile.

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

What T002 adds proof of, against a real on-disk evidence tree:

  * backfill is IDEMPOTENT — a second pass over the same evidence leaves the row
    count unchanged and reports the same ``recorded`` total (the feature file's
    "rerunning backfill adds nothing");
  * a task run with no reported usage becomes a row with NULL counts and basis
    ``unknown``, and a malformed one is counted in ``failed`` without raising
    and without costing the other task runs their rows;
  * reconcile reports ZERO DRIFT on a clean tree and FINDS AN INJECTED MISSING
    ROW — that pair is the feature file's Acceptance, verbatim;
  * reconcile is read-only: it inserts nothing and does not even create a ledger;
  * reconcile compares CONTENT, so a row that drifted after it was written is
    visible (finding R-0219's resolution);
  * the call site at the seam where actuals are finalized writes a row when a
    ledger target is given, and does nothing at all when none is.

What T003 adds proof of, over a ledger written row by row:

  * ``query_cost`` groups by role, by model and by day, filters on ``since``, on
    the EXCLUSIVE ``until`` and on ``job_id``, and reports a grand total over the
    same filters;
  * a bucket in which NOTHING was measured reports ``tokens_in is None`` and
    ``cost_usd is None`` — never 0 — with ``unmeasured_calls`` equal to its own
    row count, which is the P6 rule this feature exists to keep;
  * querying a ledger that does not exist yields an EMPTY report and creates no
    file, no directory and no database;
  * the query connection itself refuses to write, and leaves no ``-wal``/``-shm``
    behind, so reading another project's ledger cannot change it.

What R6 adds proof of, against the PRODUCTION caller (finding R-0220):

  * a fake-provider job exported through ``export_job_evidence`` — with NO
    ``ledger_*`` argument passed by hand — yields its task runs as rows, with
    the ``"<job_id>:<task_id>"`` call_id, role, token counters and basis the
    evidence files themselves carry. The hand-passed path was already green;
    it is what hid the fact that nobody ever armed the hook;
  * the INERTNESS guarantee the opt-in exists for still holds: an export for
    which no project resolves — an unregistered repo, a non-git directory, or a
    job whose ``repo_path`` is empty — creates no ledger file ANYWHERE, and in
    particular never falls back to the process working directory;
  * evidence output is BYTE-IDENTICAL whether the mirror fires or not.

Tests outside the R6 class write inside ``tmp_path`` and pass
``root=``/``path=`` explicitly, never touching ``REMEDY_DATA_DIR``. The R6
class must drive the real resolution path, so it points ``REMEDY_DATA_DIR`` at
a ``tmp_path`` directory via ``monkeypatch``; the repository's real data root is
never touched by any test in this file.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
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
    BackfillResult,
    CallRecord,
    CallSegmentRow,
    PriorReportPeriod,
    SegmentShareRow,
    backfill_ledger,
    call_id_for_task_run,
    call_record_from_evidence,
    job_id_for_evidence_dir,
    ledger_miss_count,
    merge_cost_reports,
    open_ledger,
    prior_report_period,
    query_cost,
    query_segment_shares,
    record_call,
    record_call_segments,
    reset_ledger_miss_count,
    segment_rows_from_trace_file,
    token_ledger_path_for,
    verify_ledger,
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


# ---------------------------------------------------------------------------
# T002 — backfill and reconcile over a real on-disk evidence tree
# ---------------------------------------------------------------------------

FIXTURE_JOB_ID = "job-ledger-fixture"
TASK_FULL = "T001"          # full provider actuals, a cost figure and a model
TASK_UNMEASURED = "T002"    # provider reported no usage at all
TASK_MALFORMED = "T003"     # a negative counter: unrecordable by design
TASK_NO_EVIDENCE = "T004"   # a task-run dir with nothing to mirror


def _write_json_file(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _row_count(ledger_path):
    conn = open_ledger(ledger_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0]
    finally:
        conn.close()


def _call_ids(ledger_path):
    conn = open_ledger(ledger_path)
    try:
        return sorted(r[0] for r in conn.execute("SELECT call_id FROM calls"))
    finally:
        conn.close()


def _row(ledger_path, call_id):
    conn = open_ledger(ledger_path)
    try:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT * FROM calls WHERE call_id = ?", (call_id,)
        ).fetchone()
    finally:
        conn.close()


@pytest.fixture
def evidence_tree(tmp_path):
    """A small evidence tree exactly like the actuals feature writes on disk.

    Four task runs: full actuals, no usage at all, malformed counters, and a
    directory with no provider evidence in it. Nothing here is a mock — the
    backfill reads these files the same way it reads a real job's.
    """
    base = tmp_path / "evidence" / FIXTURE_JOB_ID
    _write_json_file(base / "manifest.json",
                     {"bundle_type": "job_evidence", "job_id": FIXTURE_JOB_ID})
    runs = base / "task_runs"

    _write_json_file(runs / TASK_FULL / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": TASK_FULL,
        "execution_mode": "provider_backed",
        "provider_call_count": 2,
        "actual_call_count": 2,
        "cost_call_count": 2,
        "actual_prompt_tokens": 1000,
        "actual_completion_tokens": 200,
        "actual_total_tokens": 1200,
        "actual_cache_read_tokens": 64,
        "actual_cache_creation_tokens": 32,
        "total_cost_usd": 0.25,
        "actual_model_verified": True,
        "builder_actual_model": "claude-opus-5",
        "ts_utc": "2026-08-08T09:00:00+00:00",
    })
    _write_json_file(runs / TASK_FULL / "token_accounting.json", {"role": "builder"})

    # No usage counters and no cost at all — the claude-cli case.
    _write_json_file(runs / TASK_UNMEASURED / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": TASK_UNMEASURED,
        "execution_mode": "provider_backed",
        "provider_call_count": 1,
        "actual_call_count": 0,
        "cost_call_count": 0,
        "actual_missing_reasons": ["provider reports no ledger usage"],
    })
    _write_json_file(runs / TASK_UNMEASURED / "token_accounting.json",
                     {"role": "reviewer"})

    # A negative token count: the extractor RAISES rather than coercing it into
    # a plausible number, and this fixture pins that refusal end to end.
    _write_json_file(runs / TASK_MALFORMED / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": TASK_MALFORMED,
        "actual_prompt_tokens": -5,
    })

    (runs / TASK_NO_EVIDENCE).mkdir(parents=True, exist_ok=True)
    return base


class TestCallIdForTaskRun:
    def test_is_the_deterministic_job_and_task_pair(self):
        assert call_id_for_task_run("job-7", "T012") == "job-7:T012"
        assert call_id_for_task_run("job-7", "T012") == call_id_for_task_run(
            "job-7", "T012")

    @pytest.mark.parametrize("job_id,task_id", [
        ("", "T001"), ("job-7", ""), ("   ", "T001"), (None, "T001"), ("job-7", None),
    ])
    def test_rejects_empty_parts(self, job_id, task_id):
        """An id with an empty half would merge two task runs into one row."""
        with pytest.raises(ValueError):
            call_id_for_task_run(job_id, task_id)


class TestJobIdForEvidenceDir:
    def test_prefers_the_manifest_job_id(self, evidence_tree):
        assert job_id_for_evidence_dir(evidence_tree) == FIXTURE_JOB_ID

    def test_falls_back_to_the_directory_name(self, tmp_path):
        base = tmp_path / "job-from-dirname"
        base.mkdir()
        assert job_id_for_evidence_dir(base) == "job-from-dirname"


class TestCallRecordFromEvidence:
    def test_maps_full_actuals_onto_the_row(self, evidence_tree):
        record = call_record_from_evidence(evidence_tree, FIXTURE_JOB_ID, TASK_FULL)
        assert record is not None
        assert record.call_id == f"{FIXTURE_JOB_ID}:{TASK_FULL}"
        assert record.job_id == FIXTURE_JOB_ID
        assert record.task_id == TASK_FULL
        assert record.role == "builder"
        assert record.model == "claude-opus-5"
        assert record.ts_utc == "2026-08-08T09:00:00+00:00"
        assert record.tokens_in == 1000
        assert record.tokens_out == 200
        assert record.cache_read == 64
        assert record.cache_write == 32
        assert record.cost_usd == pytest.approx(0.25)
        assert record.cost_basis == COST_BASIS_PROVIDER_REPORTED
        assert record.evidence_ref == f"task_runs/{TASK_FULL}"

    def test_unmeasured_run_has_null_counts_and_no_invented_price(self, evidence_tree):
        record = call_record_from_evidence(
            evidence_tree, FIXTURE_JOB_ID, TASK_UNMEASURED)
        assert record is not None
        assert (record.tokens_in, record.tokens_out) == (None, None)
        assert (record.cache_read, record.cache_write) == (None, None)
        assert record.cost_usd is None
        assert record.cost_basis == COST_BASIS_UNKNOWN
        assert record.model is None

    def test_timestamp_falls_back_to_the_evidence_file_mtime(self, evidence_tree):
        """No timestamp in the evidence → the file's mtime, stated as UTC."""
        record = call_record_from_evidence(
            evidence_tree, FIXTURE_JOB_ID, TASK_UNMEASURED)
        source = (evidence_tree / "task_runs" / TASK_UNMEASURED
                  / "provider_evidence.json")
        from datetime import datetime, timezone
        expected = datetime.fromtimestamp(
            source.stat().st_mtime, tz=timezone.utc).isoformat()
        assert record.ts_utc == expected

    def test_malformed_counters_yield_no_record_at_all(self, evidence_tree):
        assert call_record_from_evidence(
            evidence_tree, FIXTURE_JOB_ID, TASK_MALFORMED) is None

    def test_absent_evidence_yields_no_record(self, evidence_tree):
        assert call_record_from_evidence(
            evidence_tree, FIXTURE_JOB_ID, TASK_NO_EVIDENCE) is None


class TestBackfillLedger:
    def test_records_every_recordable_task_run(self, evidence_tree, ledger_path):
        result = backfill_ledger(evidence_tree, path=ledger_path)
        assert isinstance(result, BackfillResult)
        assert result.scanned == 4
        assert result.recorded == 2      # full + unmeasured
        assert result.skipped == 1       # the dir with no provider evidence
        assert result.failed == 1        # the malformed one
        assert result.scanned == result.recorded + result.skipped + result.failed
        assert _row_count(ledger_path) == 2

    def test_is_idempotent(self, evidence_tree, ledger_path):
        """Rerunning backfill adds nothing — the feature file's own words."""
        first = backfill_ledger(evidence_tree, path=ledger_path)
        rows_after_first = _row_count(ledger_path)
        ids_after_first = _call_ids(ledger_path)

        second = backfill_ledger(evidence_tree, path=ledger_path)
        assert _row_count(ledger_path) == rows_after_first
        assert second.recorded == first.recorded
        assert second.scanned == first.scanned
        assert second.failed == first.failed
        assert _call_ids(ledger_path) == ids_after_first
        conn = open_ledger(ledger_path)
        try:
            duplicates = conn.execute(
                "SELECT call_id, COUNT(*) c FROM calls GROUP BY call_id HAVING c > 1"
            ).fetchall()
        finally:
            conn.close()
        assert duplicates == []

    def test_unmeasured_task_run_lands_as_nulls_with_basis_unknown(
        self, evidence_tree, ledger_path
    ):
        backfill_ledger(evidence_tree, path=ledger_path)
        row = _row(ledger_path, f"{FIXTURE_JOB_ID}:{TASK_UNMEASURED}")
        for column in ("tokens_in", "tokens_out", "cache_read", "cache_write"):
            assert row[column] is None, f"{column} must be NULL, not a fabricated zero"
        assert row["cost_usd"] is None
        assert row["cost_basis"] == COST_BASIS_UNKNOWN

    def test_malformed_task_run_never_raises_and_costs_no_other_row(
        self, evidence_tree, ledger_path
    ):
        result = backfill_ledger(evidence_tree, path=ledger_path)
        assert result.failed == 1
        assert _row(ledger_path, f"{FIXTURE_JOB_ID}:{TASK_MALFORMED}") is None
        # The task runs on either side of the malformed one are still recorded.
        assert _row(ledger_path, f"{FIXTURE_JOB_ID}:{TASK_FULL}") is not None
        assert _row(ledger_path, f"{FIXTURE_JOB_ID}:{TASK_UNMEASURED}") is not None

    def test_empty_tree_records_nothing(self, tmp_path, ledger_path):
        result = backfill_ledger(tmp_path / "job-empty", path=ledger_path)
        assert (result.scanned, result.recorded, result.failed) == (0, 0, 0)
        assert not ledger_path.exists()


class TestVerifyLedger:
    def test_reports_zero_drift_on_a_clean_tree(self, evidence_tree, ledger_path):
        backfill_ledger(evidence_tree, path=ledger_path)
        report = verify_ledger(evidence_tree, path=ledger_path)
        assert report.missing_rows == []
        assert report.orphan_rows == []
        assert report.drifted_rows == []
        assert report.has_drift is False
        assert report.checked == 3           # the three dirs carrying evidence
        assert report.unreadable == [f"{FIXTURE_JOB_ID}:{TASK_MALFORMED}"]

    def test_finds_an_injected_missing_row(self, evidence_tree, ledger_path):
        """The feature file's Acceptance: reconcile finds an injected missing row."""
        backfill_ledger(evidence_tree, path=ledger_path)
        gone = f"{FIXTURE_JOB_ID}:{TASK_FULL}"
        conn = open_ledger(ledger_path)
        try:
            conn.execute("DELETE FROM calls WHERE call_id = ?", (gone,))
            conn.commit()
        finally:
            conn.close()

        report = verify_ledger(evidence_tree, path=ledger_path)
        assert report.missing_rows == [gone]
        assert report.orphan_rows == []
        assert report.has_drift is True

    def test_finds_a_content_drifted_row(self, evidence_tree, ledger_path):
        """R-0219: a row whose content no longer matches its evidence is visible."""
        backfill_ledger(evidence_tree, path=ledger_path)
        drifted = f"{FIXTURE_JOB_ID}:{TASK_FULL}"
        conn = open_ledger(ledger_path)
        try:
            conn.execute(
                "UPDATE calls SET tokens_in = 999999 WHERE call_id = ?", (drifted,))
            conn.commit()
        finally:
            conn.close()

        report = verify_ledger(evidence_tree, path=ledger_path)
        assert report.drifted_rows == [drifted]
        assert report.missing_rows == []
        assert report.has_drift is True

    def test_finds_an_orphan_row_of_this_job(self, evidence_tree, ledger_path):
        backfill_ledger(evidence_tree, path=ledger_path)
        orphan = f"{FIXTURE_JOB_ID}:T999"
        assert record_call(
            CallRecord(call_id=orphan, job_id=FIXTURE_JOB_ID, task_id="T999",
                       ts_utc="2026-08-08T10:00:00+00:00"),
            path=ledger_path,
        ) is True

        report = verify_ledger(evidence_tree, path=ledger_path)
        assert report.orphan_rows == [orphan]
        assert report.missing_rows == []

    def test_ignores_another_job_s_rows(self, evidence_tree, ledger_path):
        """One project ledger holds many jobs; the others are not orphans."""
        backfill_ledger(evidence_tree, path=ledger_path)
        assert record_call(
            CallRecord(call_id="some-other-job:T001", job_id="some-other-job",
                       task_id="T001", ts_utc="2026-08-08T10:00:00+00:00"),
            path=ledger_path,
        ) is True

        report = verify_ledger(evidence_tree, path=ledger_path)
        assert report.orphan_rows == []
        assert report.has_drift is False

    def test_inserts_nothing(self, evidence_tree, ledger_path):
        backfill_ledger(evidence_tree, path=ledger_path)
        before = _row_count(ledger_path)
        verify_ledger(evidence_tree, path=ledger_path)
        verify_ledger(evidence_tree, path=ledger_path)
        assert _row_count(ledger_path) == before

    def test_does_not_create_a_ledger_that_does_not_exist(
        self, evidence_tree, ledger_path
    ):
        """Verifying is read-only enough that it never brings a database into being."""
        report = verify_ledger(evidence_tree, path=ledger_path)
        assert not ledger_path.exists()
        assert report.missing_rows == [
            f"{FIXTURE_JOB_ID}:{TASK_FULL}",
            f"{FIXTURE_JOB_ID}:{TASK_UNMEASURED}",
        ]

    def test_needs_a_target(self, evidence_tree):
        with pytest.raises(ValueError):
            verify_ledger(evidence_tree)


class TestCallSiteAtTheActualsSeam:
    """The hook in ``write_evidence_bundle`` — opt-in, inert, never fatal."""

    @staticmethod
    def _bundle():
        return {
            "manifest": {"run_id": "run-1"},
            "summary_md": "# run\n",
            "tests": "ok\n",
            "token_accounting": {"role": "builder"},
            "provider_evidence": {
                "schema_version": "1.0.0",
                "task_id": TASK_FULL,
                "execution_mode": "provider_backed",
                "provider_call_count": 1,
                "actual_call_count": 1,
                "cost_call_count": 1,
                "actual_prompt_tokens": 11,
                "actual_completion_tokens": 5,
                "actual_total_tokens": 16,
                "total_cost_usd": 0.02,
                "ts_utc": "2026-08-08T11:00:00+00:00",
            },
        }

    def test_writes_a_row_when_a_target_is_given(self, tmp_path, ledger_path):
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        out_dir = tmp_path / "evidence" / FIXTURE_JOB_ID / "task_runs" / TASK_FULL
        written = write_evidence_bundle(
            self._bundle(), str(out_dir),
            ledger_path=str(ledger_path),
            ledger_job_id=FIXTURE_JOB_ID,
            ledger_task_id=TASK_FULL,
        )

        assert "provider_evidence.json" in written
        row = _row(ledger_path, f"{FIXTURE_JOB_ID}:{TASK_FULL}")
        assert row is not None
        assert row["job_id"] == FIXTURE_JOB_ID
        assert row["task_id"] == TASK_FULL
        assert row["role"] == "builder"
        assert row["tokens_in"] == 11
        assert row["tokens_out"] == 5
        assert row["cost_basis"] == COST_BASIS_PROVIDER_REPORTED
        assert row["evidence_ref"] == f"task_runs/{TASK_FULL}"

    def test_the_live_row_is_the_row_backfill_would_have_written(
        self, tmp_path, ledger_path
    ):
        """One row, two producers: reconcile can only compare content if they agree."""
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        evidence_dir = tmp_path / "evidence" / FIXTURE_JOB_ID
        out_dir = evidence_dir / "task_runs" / TASK_FULL
        write_evidence_bundle(
            self._bundle(), str(out_dir),
            ledger_path=str(ledger_path),
            ledger_job_id=FIXTURE_JOB_ID,
            ledger_task_id=TASK_FULL,
        )
        report = verify_ledger(evidence_dir, path=ledger_path)
        assert report.has_drift is False
        assert report.drifted_rows == []

    def test_default_writes_nothing_and_raises_nothing(self, tmp_path, ledger_path):
        """Every existing caller passes no ledger argument: nothing may happen."""
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        out_dir = tmp_path / "evidence" / FIXTURE_JOB_ID / "task_runs" / TASK_FULL
        before = ledger_miss_count()

        written = write_evidence_bundle(self._bundle(), str(out_dir))

        assert "provider_evidence.json" in written
        assert not ledger_path.exists(), "no ledger target means no ledger file"
        assert list(tmp_path.rglob("*.sqlite")) == []
        assert ledger_miss_count() == before, "an inert hook is not a counted miss"

    def test_a_target_without_identifiers_stays_inert(self, tmp_path, ledger_path):
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        out_dir = tmp_path / "evidence" / FIXTURE_JOB_ID / "task_runs" / TASK_FULL
        write_evidence_bundle(
            self._bundle(), str(out_dir), ledger_path=str(ledger_path))
        assert not ledger_path.exists()

    def test_a_non_task_run_layout_invents_no_row(self, tmp_path, ledger_path):
        """Outside the task_runs/<task_id>/ layout there is no honest evidence_ref."""
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        out_dir = tmp_path / "somewhere-else"
        write_evidence_bundle(
            self._bundle(), str(out_dir),
            ledger_path=str(ledger_path),
            ledger_job_id=FIXTURE_JOB_ID,
            ledger_task_id=TASK_FULL,
        )
        assert not ledger_path.exists()

    def test_a_broken_ledger_target_never_fails_the_evidence_write(
        self, tmp_path, caplog
    ):
        """The mirror may fail; the evidence write may not."""
        from packages.orchestration.pingpong_evidence import write_evidence_bundle

        blocker = tmp_path / "not-a-directory"
        blocker.write_text("this is a file, not a directory\n", encoding="utf-8")
        out_dir = tmp_path / "evidence" / FIXTURE_JOB_ID / "task_runs" / TASK_FULL

        with caplog.at_level(logging.ERROR):
            written = write_evidence_bundle(
                self._bundle(), str(out_dir),
                ledger_path=str(blocker / "sub" / LEDGER_FILENAME),
                ledger_job_id=FIXTURE_JOB_ID,
                ledger_task_id=TASK_FULL,
            )

        assert "provider_evidence.json" in written
        assert (out_dir / "provider_evidence.json").is_file()
        assert ledger_miss_count() >= 1


# ── T003: the cost aggregation queries ───────────────────────────────────────
# Four rows in one ledger: two MEASURED builder calls on one day and one job,
# two UNMEASURED reviewer calls on the next day and another job. That shape is
# what lets one fixture pin every grouping, both filters, the grand total and —
# the point of the feature — a bucket in which nothing was measured at all.

COST_JOB_MEASURED = "job-a"
COST_JOB_UNMEASURED = "job-b"


@pytest.fixture
def cost_ledger(tmp_path):
    """A ledger with two measured and two unmeasured calls, written row by row."""
    path = tmp_path / "projects" / str(uuid4()) / LEDGER_FILENAME
    for record in (
        CallRecord(
            call_id=f"{COST_JOB_MEASURED}:T001", job_id=COST_JOB_MEASURED,
            task_id="T001", role="builder", model="claude-opus-5",
            ts_utc="2026-08-01T10:00:00+00:00",
            tokens_in=1000, tokens_out=200, cache_read=64, cache_write=32,
            cost_usd=0.25, cost_basis=COST_BASIS_PROVIDER_REPORTED,
        ),
        CallRecord(
            call_id=f"{COST_JOB_MEASURED}:T002", job_id=COST_JOB_MEASURED,
            task_id="T002", role="builder", model="claude-opus-5",
            ts_utc="2026-08-01T12:00:00+00:00",
            tokens_in=500, tokens_out=50,
            cost_usd=0.10, cost_basis=COST_BASIS_PROVIDER_REPORTED,
        ),
        # The claude-cli case: the provider reported no usage and no cost.
        CallRecord(
            call_id=f"{COST_JOB_UNMEASURED}:T001", job_id=COST_JOB_UNMEASURED,
            task_id="T001", role="reviewer", model="claude-sonnet-4",
            ts_utc="2026-08-02T09:00:00+00:00",
        ),
        CallRecord(
            call_id=f"{COST_JOB_UNMEASURED}:T002", job_id=COST_JOB_UNMEASURED,
            task_id="T002", role="reviewer", model="claude-sonnet-4",
            ts_utc="2026-08-02T11:00:00+00:00",
        ),
    ):
        assert record_call(record, path=path) is True
    return path


def _bucket(report, name):
    return next(row for row in report.rows if row.bucket == name)


class TestQueryCostGrandTotal:
    def test_the_grand_total_sums_every_row(self, cost_ledger):
        total = query_cost(path=cost_ledger).total

        assert total.bucket is None
        assert total.calls == 4
        assert total.tokens_in == 1500
        assert total.tokens_out == 250
        assert total.cache_read == 64
        assert total.cache_write == 32
        assert total.cost_usd == pytest.approx(0.35)
        assert total.measured_calls == 2
        assert total.unmeasured_calls == 2

    def test_no_grouping_means_no_buckets(self, cost_ledger):
        assert query_cost(path=cost_ledger).rows == []

    def test_the_report_echoes_the_question_back(self, cost_ledger):
        report = query_cost(path=cost_ledger, by="role", since="2026-08-01",
                            job_id=COST_JOB_MEASURED)
        assert (report.by, report.since, report.job_id) == (
            "role", "2026-08-01", COST_JOB_MEASURED)
        assert report.ledger_path == str(cost_ledger)
        assert report.ledger_exists is True

    def test_an_unknown_group_key_is_refused(self, cost_ledger):
        with pytest.raises(ValueError):
            query_cost(path=cost_ledger, by="provider")

    def test_needs_a_target(self):
        with pytest.raises(ValueError):
            query_cost()


class TestQueryCostGrouping:
    def test_by_role(self, cost_ledger):
        report = query_cost(path=cost_ledger, by="role")
        assert [row.bucket for row in report.rows] == ["builder", "reviewer"]
        assert _bucket(report, "builder").calls == 2
        assert _bucket(report, "builder").tokens_in == 1500
        assert _bucket(report, "reviewer").calls == 2

    def test_by_model(self, cost_ledger):
        report = query_cost(path=cost_ledger, by="model")
        assert [row.bucket for row in report.rows] == [
            "claude-opus-5", "claude-sonnet-4"]
        assert _bucket(report, "claude-opus-5").cost_usd == pytest.approx(0.35)

    def test_by_day_buckets_on_the_date_prefix(self, cost_ledger):
        report = query_cost(path=cost_ledger, by="day")
        assert [row.bucket for row in report.rows] == ["2026-08-01", "2026-08-02"]
        assert _bucket(report, "2026-08-01").calls == 2
        assert _bucket(report, "2026-08-02").calls == 2

    def test_the_buckets_add_up_to_the_total(self, cost_ledger):
        report = query_cost(path=cost_ledger, by="role")
        assert sum(row.calls for row in report.rows) == report.total.calls


class TestQueryCostFilters:
    def test_since_compares_iso_timestamps_lexicographically(self, cost_ledger):
        total = query_cost(path=cost_ledger, since="2026-08-02").total
        assert total.calls == 2
        assert total.measured_calls == 0

    def test_since_can_exclude_everything(self, cost_ledger):
        assert query_cost(path=cost_ledger, since="2027-01-01").total.calls == 0

    def test_the_job_filter(self, cost_ledger):
        total = query_cost(path=cost_ledger, job_id=COST_JOB_MEASURED).total
        assert total.calls == 2
        assert total.tokens_in == 1500

    def test_the_filters_apply_to_the_buckets_too(self, cost_ledger):
        report = query_cost(path=cost_ledger, job_id=COST_JOB_UNMEASURED, by="role")
        assert [row.bucket for row in report.rows] == ["reviewer"]

    def test_a_call_at_exactly_until_is_out_while_one_at_exactly_since_is_in(
        self, cost_ledger
    ):
        """DECISION F115 D5: the period is the half-open ``[since, until)``.

        ONE instant read as both boundaries. The 09:00 call on 08-02 is INSIDE
        the window that starts there and OUTSIDE the window that ends there, so
        the two adjacent windows partition the four rows exactly once between
        them — no row counted twice, none dropped.
        """
        boundary = "2026-08-02T09:00:00+00:00"

        opened = query_cost(path=cost_ledger, since=boundary)
        closed = query_cost(path=cost_ledger, until=boundary, by="day")

        assert opened.total.calls == 2
        assert closed.total.calls == 2
        assert [row.bucket for row in closed.rows] == ["2026-08-01"]
        assert closed.until == boundary
        assert (opened.total.calls + closed.total.calls
                == query_cost(path=cost_ledger).total.calls)


class TestUnmeasuredIsNeverAZero:
    """The P6 rule: SUM over all-NULL stays NULL, so nothing renders as 0."""

    def test_an_all_unmeasured_bucket_reports_none_not_zero(self, cost_ledger):
        bucket = _bucket(query_cost(path=cost_ledger, by="role"), "reviewer")

        assert bucket.calls == 2
        assert bucket.tokens_in is None and bucket.tokens_in != 0
        assert bucket.tokens_out is None
        assert bucket.cache_read is None
        assert bucket.cache_write is None
        assert bucket.cost_usd is None
        assert bucket.unmeasured_calls == bucket.calls
        assert bucket.measured_calls == 0
        assert bucket.fully_measured is False

    def test_an_all_unmeasured_total_reports_none_not_zero(self, cost_ledger):
        total = query_cost(path=cost_ledger, job_id=COST_JOB_UNMEASURED).total
        assert total.calls == 2
        assert total.tokens_in is None
        assert total.cost_usd is None
        assert total.unmeasured_calls == 2

    def test_a_measured_bucket_says_so(self, cost_ledger):
        bucket = _bucket(query_cost(path=cost_ledger, by="role"), "builder")
        assert bucket.measured_calls == 2 and bucket.unmeasured_calls == 0
        assert bucket.fully_measured is True

    def test_a_cache_counter_nobody_reported_stays_none(self, cost_ledger):
        """T002 reported tokens but no cache figures; the day still sums honestly."""
        assert _bucket(query_cost(path=cost_ledger, by="day"),
                       "2026-08-01").cache_read == 64
        assert _bucket(query_cost(path=cost_ledger, by="day"),
                       "2026-08-02").cache_read is None


class TestQueryCostIsReadOnly:
    def test_a_missing_ledger_yields_an_empty_report_and_creates_nothing(self, tmp_path):
        absent = tmp_path / "projects" / str(uuid4()) / LEDGER_FILENAME

        report = query_cost(path=absent, by="role")

        assert report.ledger_exists is False
        assert report.rows == []
        assert report.total.calls == 0
        assert report.total.tokens_in is None
        assert not absent.exists()
        assert not absent.parent.exists(), "a query created a project directory"

    def test_the_row_count_is_unchanged_and_no_sidecar_is_left_behind(self, cost_ledger):
        before = _row_count(cost_ledger)
        before_files = sorted(p.name for p in cost_ledger.parent.iterdir())

        query_cost(path=cost_ledger, by="day")

        assert _row_count(cost_ledger) == before
        assert sorted(p.name for p in cost_ledger.parent.iterdir()) == before_files

    def test_the_connection_itself_refuses_to_write(self, cost_ledger):
        from packages.orchestration.token_ledger import _connect_readonly

        conn = _connect_readonly(cost_ledger)
        try:
            with pytest.raises(sqlite3.OperationalError):
                conn.execute("DELETE FROM calls")
        finally:
            conn.close()


class TestMergeCostReports:
    def test_two_ledgers_add_up_without_inventing_a_zero(self, cost_ledger, tmp_path):
        other = tmp_path / "projects" / str(uuid4()) / LEDGER_FILENAME
        assert record_call(
            CallRecord(call_id="job-c:T001", job_id="job-c", role="builder",
                       model="claude-opus-5", ts_utc="2026-08-03T10:00:00+00:00",
                       tokens_in=7, cost_usd=0.01,
                       cost_basis=COST_BASIS_PROVIDER_REPORTED),
            path=other) is True

        merged = merge_cost_reports([
            query_cost(path=cost_ledger, by="role"),
            query_cost(path=other, by="role"),
        ])

        assert merged.total.calls == 5
        assert merged.total.tokens_in == 1507
        assert merged.total.measured_calls == 3
        assert _bucket(merged, "builder").calls == 3
        # The reviewer bucket exists in only one ledger and is unmeasured there,
        # so the merged figure is still unknown — not 0.
        assert _bucket(merged, "reviewer").tokens_in is None

    def test_merging_reports_over_missing_ledgers_stays_empty(self, tmp_path):
        merged = merge_cost_reports([
            query_cost(path=tmp_path / "a" / LEDGER_FILENAME, by="role"),
            query_cost(path=tmp_path / "b" / LEDGER_FILENAME, by="role"),
        ])
        assert merged.ledger_exists is False
        assert merged.rows == []
        assert merged.total.calls == 0
        assert merged.total.cost_usd is None

    def test_the_merge_carries_the_period_end_of_its_inputs(self, cost_ledger,
                                                            tmp_path):
        """A merged report that forgot ``until`` would not match its own shares.

        ``cost_report._same_question`` compares the period on both halves, so a
        cross-project total that dropped its end would be refused beside a
        legitimate ``query_segment_shares`` over the very same arguments.
        """
        boundary = "2026-08-02T09:00:00+00:00"

        merged = merge_cost_reports([
            query_cost(path=cost_ledger, until=boundary, by="role"),
            query_cost(path=tmp_path / "b" / LEDGER_FILENAME, until=boundary,
                       by="role"),
        ])

        assert merged.until == boundary
        assert merged.total.calls == 2
        # No input, no period: the empty fold invents no end either.
        assert merge_cost_reports([]).until is None


class TestPriorReportPeriod:
    """DECISION F115 D6: the window before ``[since, until)``, or why there is none."""

    def test_the_prior_window_of_a_bare_date_pair(self):
        prior = prior_report_period("2026-08-08", "2026-08-15")

        assert prior.available is True
        assert prior.since == "2026-08-01T00:00:00"
        assert prior.until == "2026-08-08"
        assert prior.unavailable_reason is None

    def test_the_prior_window_of_an_offset_aware_pair(self):
        """The opening bound reproduces the awareness of the input it came from."""
        prior = prior_report_period(
            "2026-08-08T00:00:00+00:00", "2026-08-09T06:00:00+00:00"
        )

        assert prior.available is True
        assert prior.since == "2026-08-06T18:00:00+00:00"
        assert prior.until == "2026-08-08T00:00:00+00:00"

    def test_the_prior_until_is_the_original_since_string_byte_for_byte(self):
        """A re-serialisation would break the abutment by formatting luck alone.

        ``_cost_filters`` compares ``ts_utc`` lexicographically, so the boundary
        the two windows share has to be the SAME STRING on both sides. Both
        spellings below round-trip to something ELSE, which is exactly why the
        caller's own bytes are passed through instead.
        """
        for spelling, end in (
            ("2026-08-08T00:00:00Z", "2026-08-09T00:00:00Z"),
            ("2026-08-08", "2026-08-09"),
        ):
            prior = prior_report_period(spelling, end)

            assert prior.until == spelling
            round_tripped = datetime.fromisoformat(
                spelling.replace("Z", "+00:00")
            ).isoformat()
            assert round_tripped != spelling, "the spelling must not survive a round-trip"

    def test_an_open_ended_period_has_no_prior_window(self):
        for since, until in ((None, "2026-08-15"), ("2026-08-08", None), (None, None)):
            prior = prior_report_period(since, until)

            assert prior.available is False
            assert prior.since is None and prior.until is None
            assert "open-ended" in prior.unavailable_reason

    def test_an_unparseable_end_is_never_guessed_at(self):
        for since, until in (("last tuesday", "2026-08-15"), ("2026-08-08", "soon")):
            prior = prior_report_period(since, until)

            assert prior.available is False
            assert "ISO-8601" in prior.unavailable_reason

    def test_a_naive_end_beside_an_aware_one_invents_no_offset(self):
        prior = prior_report_period("2026-08-08T00:00:00+00:00", "2026-08-15T00:00:00")

        assert prior.available is False
        assert "offset" in prior.unavailable_reason

    def test_an_empty_or_inverted_period_has_no_prior_window_either(self):
        for since, until in (
            ("2026-08-08", "2026-08-08"),
            ("2026-08-15", "2026-08-08"),
        ):
            prior = prior_report_period(since, until)

            assert prior.available is False
            assert "ends at or before it starts" in prior.unavailable_reason

    def test_each_unavailable_case_states_its_own_reason(self):
        """Four different failures, four different sentences — never one catch-all."""
        reasons = {
            prior_report_period(None, "2026-08-15").unavailable_reason,
            prior_report_period("nope", "2026-08-15").unavailable_reason,
            prior_report_period(
                "2026-08-08T00:00:00+00:00", "2026-08-15T00:00:00"
            ).unavailable_reason,
            prior_report_period("2026-08-15", "2026-08-08").unavailable_reason,
        }
        assert len(reasons) == 4

    def test_a_window_or_a_reason_but_never_both_and_never_neither(self):
        with pytest.raises(ValueError):
            PriorReportPeriod()
        with pytest.raises(ValueError):
            PriorReportPeriod(since="2026-08-01", until="2026-08-08",
                              unavailable_reason="both halves")
        with pytest.raises(ValueError):
            PriorReportPeriod(since="2026-08-01")
        with pytest.raises(ValueError):
            PriorReportPeriod(since="2026-08-01", unavailable_reason="half a window")

    def test_the_prior_and_the_current_window_partition_the_ledger(self, cost_ledger):
        """The partition property of DECISION F115 D5, over a real ledger.

        The prior window plus the current one cover ``[prior.since, until)``
        exactly once: no boundary call is counted twice and none is dropped.
        """
        since, until = "2026-08-02T00:00:00+00:00", "2026-08-03T00:00:00+00:00"
        prior = prior_report_period(since, until)
        assert prior.available is True

        before = query_cost(path=cost_ledger, since=prior.since,
                            until=prior.until).total
        current = query_cost(path=cost_ledger, since=since, until=until).total
        whole = query_cost(path=cost_ledger, since=prior.since, until=until).total

        assert (before.calls, current.calls, whole.calls) == (2, 2, 4)
        assert before.calls + current.calls == whole.calls
        assert before.measured_calls + current.measured_calls == whole.measured_calls
        # The two measured calls sit in the PRIOR window; the current one holds
        # only unmeasured rows, so its share of the total stays None, not 0.
        assert before.tokens_in == 1500
        assert current.tokens_in is None
        assert whole.tokens_in == 1500


# ---------------------------------------------------------------------------
# R6 (finding R-0220) — the LIVE mirror on the PRODUCTION path
# ---------------------------------------------------------------------------

#: A one-task job file. One task is enough: the seam is per TASK RUN (D16), so
#: one finalized run is the whole unit of behaviour under test.
_LIVE_JOB_FILE = """\
# Job: Live ledger mirror

## Task 1
Add a greeting.

Acceptance:
- file exists
"""


@pytest.fixture
def live_data_root(tmp_path, monkeypatch):
    """A throwaway data root for the tests that drive real project resolution.

    ``REMEDY_PROJECT`` is cleared as well: the seam must resolve the project from
    the JOB's own repo path, and a leaked environment selector would mask that.
    """
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    return data_dir


def _git_repo(path):
    """A real git repo with one commit — what a project can be registered against."""
    path.mkdir(parents=True, exist_ok=True)
    (path / "main.py").write_text("VALUE = 1\n")

    def _git(*args):
        subprocess.run(["git", *args], cwd=str(path), check=True,
                       capture_output=True, text=True)

    _git("init", "-q")
    _git("config", "user.email", "t@example.com")
    _git("config", "user.name", "Test")
    _git("add", "-A")
    _git("commit", "-q", "-m", "init")
    return path


@pytest.fixture
def live_job_repo(tmp_path):
    return _git_repo(tmp_path / "job_repo")


def _run_fake_provider_job(repo):
    """Run a real job end to end with the fake provider — no network, no real model."""
    from packages.orchestration.pingpong_job import parse_job_file, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    plan = parse_job_file(_LIVE_JOB_FILE, str(repo))
    return run_job(
        plan.job_id,
        builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
        repair_rounds=0,
    )


def _database_files_under(root):
    """Every SQLite artefact under *root*, sidecars included — the inertness probe."""
    base = Path(root)
    if not base.exists():
        return []
    return sorted(
        str(p.relative_to(base)) for p in base.rglob("*")
        if p.is_file() and (
            p.suffix == ".sqlite" or p.name.endswith(("-wal", "-shm"))
        )
    )


def _file_digests(base):
    return {
        str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(base.rglob("*")) if p.is_file()
    }


class TestLiveMirrorOnTheProductionPath:
    """Finding R-0220: a REAL job must yield rows with nobody passing ``ledger_*``.

    Every test in this class calls ``export_job_evidence`` — the production
    caller behind `remedy do job-evidence` and `do job-flow` — and passes NO
    ``ledger_*`` argument. A test that supplies the target itself proves only
    the hand-passed path, which was already green and is exactly what let the
    feature ship switched off.
    """

    def test_a_fake_provider_job_yields_its_task_run_as_a_row(
        self, live_data_root, live_job_repo, tmp_path
    ):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("ledger-live", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)

        result = export_job_evidence(job.job_id, str(tmp_path / "evidence"))
        assert "error" not in result

        ledger = token_ledger_path_for(project.id)
        assert ledger.is_file(), (
            "the production path armed no ledger: export_job_evidence must "
            "supply the ledger_* target itself (finding R-0220)"
        )

        call_id = f"{job.job_id}:T001"
        assert _call_ids(ledger) == [call_id]

        row = _row(ledger, call_id)
        assert row["job_id"] == job.job_id
        assert row["task_id"] == "T001"
        assert row["evidence_ref"] == "task_runs/T001"
        assert row["ts_utc"]
        assert row["cost_basis"] in COST_BASES

    def test_the_live_row_says_exactly_what_the_evidence_files_say(
        self, live_data_root, live_job_repo, tmp_path
    ):
        """Role, model, counters and basis are the FILES' values, not invented ones."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("ledger-live", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)
        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))

        expected = call_record_from_evidence(out, job.job_id, "T001")
        assert expected is not None, "the exported tree carries no provider evidence"

        row = _row(token_ledger_path_for(project.id), f"{job.job_id}:T001")
        for field in (
            "call_id", "job_id", "task_id", "role", "model",
            "tokens_in", "tokens_out", "cache_read", "cache_write",
            "cost_usd", "cost_basis", "ts_utc", "evidence_ref",
        ):
            assert row[field] == getattr(expected, field), field

        # A fake-provider call reports no price, and an unreported counter must
        # not have become a zero on the way in (the P6 rule).
        assert row["cost_usd"] is None
        assert row["cost_basis"] == COST_BASIS_UNKNOWN

    def test_the_live_row_is_the_row_backfill_would_have_written(
        self, live_data_root, live_job_repo, tmp_path
    ):
        """Reconcile is the independent judge: one producer, so zero drift."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("ledger-live", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)
        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))

        report = verify_ledger(out, path=token_ledger_path_for(project.id))
        assert report.has_drift is False
        assert report.missing_rows == []
        assert report.drifted_rows == []

    def test_re_exporting_the_same_job_adds_no_second_row(
        self, live_data_root, live_job_repo, tmp_path
    ):
        """The call_id is a pure function of (job, task), so a re-export is a no-op."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("ledger-live", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)

        export_job_evidence(job.job_id, str(tmp_path / "first"))
        ledger = token_ledger_path_for(project.id)
        after_first = _row_count(ledger)

        export_job_evidence(job.job_id, str(tmp_path / "second"))
        assert _row_count(ledger) == after_first == 1

    def test_the_export_never_fails_when_the_ledger_cannot_be_written(
        self, live_data_root, live_job_repo, tmp_path, monkeypatch, caplog
    ):
        """A broken mirror is a counted, logged miss — never a failed export."""
        import packages.orchestration.token_ledger as ledger_mod
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        register_project_repo("ledger-live", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)

        def _boom(*_args, **_kwargs):
            raise RuntimeError("ledger is on fire")

        monkeypatch.setattr(ledger_mod, "open_ledger", _boom)
        with caplog.at_level(logging.ERROR, logger=LEDGER_LOGGER):
            result = export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        assert "error" not in result
        assert "task_runs/T001/provider_evidence.json" in result["files"]
        assert ledger_miss_count() == 1

    def test_evidence_bytes_are_identical_whether_the_mirror_fires_or_not(
        self, live_data_root, live_job_repo, tmp_path
    ):
        """The files are the source of truth; the mirror may not alter one byte."""
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.project_registry import register_project_repo

        job = _run_fake_provider_job(live_job_repo)

        inert = tmp_path / "inert"
        export_job_evidence(job.job_id, str(inert))          # no project yet
        assert _database_files_under(live_data_root) == []

        register_project_repo("ledger-live", str(live_job_repo))
        armed = tmp_path / "armed"
        export_job_evidence(job.job_id, str(armed))
        assert _database_files_under(live_data_root) != []

        inert_files = _file_digests(inert)
        armed_files = _file_digests(armed)
        assert set(inert_files) == set(armed_files)
        differing = [
            name for name, digest in inert_files.items()
            if name.startswith("task_runs/T001/") and armed_files[name] != digest
        ]
        assert differing == []


class TestTheMirrorStaysInertWithoutAProject:
    """The opt-in's reason for existing: no resolved project, no ledger anywhere.

    ``_record_finalized_call_in_ledger`` refuses to resolve a project itself so
    that a test which merely writes an evidence bundle never starts touching the
    user's data root. Arming the hook at the job seam must not weaken that, so
    the resolver has to answer None — not "the project of whatever directory the
    process happens to be in".
    """

    def test_an_unregistered_git_repo_writes_no_ledger(
        self, live_data_root, live_job_repo, tmp_path
    ):
        from packages.orchestration.job_evidence import export_job_evidence

        job = _run_fake_provider_job(live_job_repo)
        result = export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        assert "error" not in result
        assert _database_files_under(live_data_root) == []
        assert _database_files_under(tmp_path) == []
        assert ledger_miss_count() == 0

    def test_a_plain_directory_writes_no_ledger(self, live_data_root, tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence

        plain = tmp_path / "not_a_repo"
        plain.mkdir()
        (plain / "main.py").write_text("VALUE = 1\n")

        job = _run_fake_provider_job(plain)
        result = export_job_evidence(job.job_id, str(tmp_path / "evidence"))

        assert "error" not in result
        assert _database_files_under(live_data_root) == []
        assert _database_files_under(tmp_path) == []

    def test_an_empty_repo_path_never_falls_back_to_the_process_cwd(self):
        """The dangerous case: ``Path("")`` resolves to the process CWD, which may
        well be a REGISTERED project — this repository is one. The resolver must
        refuse an absent repo path outright rather than file a test's rows under
        whatever checkout the suite happens to be running in.
        """
        from packages.orchestration.job_evidence import _resolve_job_ledger_project_id

        class _JobWithoutRepoPath:
            repo_path = ""

        class _JobWithoutTheAttribute:
            pass

        assert _resolve_job_ledger_project_id(_JobWithoutRepoPath()) is None
        assert _resolve_job_ledger_project_id(_JobWithoutTheAttribute()) is None

    def test_a_vanished_repo_path_is_inert_and_never_raises(self, tmp_path):
        from packages.orchestration.job_evidence import _resolve_job_ledger_project_id

        class _Job:
            repo_path = str(tmp_path / "gone")

        assert _resolve_job_ledger_project_id(_Job()) is None


class TestCallSegmentsSchema:
    """F115 D4 — the per-call segment manifest lands in its own table.

    A ``calls`` row is one finalized task run while a manifest belongs to one
    provider call, so the manifest gets ``call_segments`` beside the ledger row
    rather than a column on it. This round adds the SCHEMA ONLY: nothing writes
    to the table yet, so what is provable here is its shape, its arrival on a
    fresh ledger, its arrival on an already-migrated one, and the structural
    backfill tolerance the empty table gives every pre-F115 row.
    """

    def test_a_fresh_ledger_carries_the_call_segments_table(self, ledger_path):
        conn = open_ledger(ledger_path)
        try:
            table = conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='call_segments'"
            ).fetchone()
            assert table is not None
            stored = conn.execute(
                "SELECT value FROM meta WHERE key = ?", (SCHEMA_VERSION_KEY,)
            ).fetchone()
            assert stored[0] == "2"
        finally:
            conn.close()

    def test_a_version_one_ledger_gains_the_table_on_reopen(self, ledger_path):
        """Migration step 2 must reach a ledger that already stopped at step 1.

        This is the first time the numbered-step mechanism runs past step 1, so
        the upgrade path is proven here rather than assumed from its comment.
        """
        conn = open_ledger(ledger_path)
        try:
            conn.execute("DROP TABLE call_segments")
            conn.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
                (SCHEMA_VERSION_KEY, "1"),
            )
            conn.commit()
        finally:
            conn.close()

        downgraded = sqlite3.connect(str(ledger_path))
        try:
            assert downgraded.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='call_segments'"
            ).fetchone() is None
        finally:
            downgraded.close()

        upgraded = open_ledger(ledger_path)
        try:
            assert upgraded.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='call_segments'"
            ).fetchone() is not None
            stored = upgraded.execute(
                "SELECT value FROM meta WHERE key = ?", (SCHEMA_VERSION_KEY,)
            ).fetchone()
            assert stored[0] == "2"
        finally:
            upgraded.close()

    def test_call_segments_columns_mirror_the_manifest(self, ledger_path):
        """The value columns are ``manifest_as_dicts()``'s keys, in its order."""
        conn = open_ledger(ledger_path)
        try:
            columns = [
                row[1]
                for row in conn.execute("PRAGMA table_info(call_segments)")
            ]
        finally:
            conn.close()

        assert columns == [
            "call_id",
            "trace_seq",
            "segment_name",
            "segment_rank",
            "segment_sha256",
            "chars",
            "tokens_estimated",
        ]

    def test_a_pre_f115_call_owns_no_segment_rows(self, ledger_path):
        """No rows is what the report renders as unattributed, never a guess."""
        record = CallRecord(call_id="call-unattributed", ts_utc="2026-08-08T12:00:00Z")
        assert record_call(record, path=ledger_path) is True

        conn = open_ledger(ledger_path)
        try:
            segments = conn.execute(
                "SELECT COUNT(*) FROM call_segments WHERE call_id = ?",
                (record.call_id,),
            ).fetchone()[0]
            calls = conn.execute(
                "SELECT COUNT(*) FROM calls WHERE call_id = ?", (record.call_id,)
            ).fetchone()[0]
        finally:
            conn.close()

        assert segments == 0
        assert calls == 1


# The task run whose trace carries a manifest in the fixtures below; it is the
# evidence tree's own full-actuals run, so the end-to-end test writes its trace
# beside the very provider_evidence.json the ledger row is built from.
SEGMENT_TASK = TASK_FULL


def _manifest_entry(name, rank, sha256, chars, tokens_estimated):
    """One ``ComposedPrompt.manifest_as_dicts()`` row, key for key."""
    return {
        "name": name,
        "rank": rank,
        "sha256": sha256,
        "chars": chars,
        "tokens_estimated": tokens_estimated,
    }


def _trace_entry(task_id, manifest, *, role="builder"):
    """One prompt-trace entry in the shape ``prompt_trace.py`` writes on disk.

    A real JSONL object, not a private helper's output: the ledger reads this
    file as bytes, so the fixture has to be bytes the tracer could have written.
    """
    return {
        "run_id": "run-ledger-fixture",
        "job_id": FIXTURE_JOB_ID,
        "task_id": task_id,
        "round": 1,
        "role": role,
        "provider": "fake",
        "prompt_kind": "initial",
        "prompt_sha256": "0" * 64,
        "prompt_chars": 1234,
        "prompt_tokens_estimated": 308,
        "segment_manifest": list(manifest),
        "segment_manifest_chars": sum(m.get("chars", 0) for m in manifest),
        "created_at": "2026-08-08T09:00:00+00:00",
    }


def _write_trace_file(path, entries):
    """Write real JSONL — one JSON object per line — as ``prompt_trace.py`` does."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(entry) + "\n" for entry in entries), encoding="utf-8"
    )


def _segment_rows(ledger_path):
    conn = open_ledger(ledger_path)
    try:
        conn.row_factory = sqlite3.Row
        return [
            dict(row)
            for row in conn.execute(
                "SELECT * FROM call_segments ORDER BY trace_seq, segment_rank"
            )
        ]
    finally:
        conn.close()


def _segment_count(ledger_path):
    conn = open_ledger(ledger_path)
    try:
        return conn.execute("SELECT COUNT(*) FROM call_segments").fetchone()[0]
    finally:
        conn.close()


class TestCallSegmentsWriter:
    """F115 T001-Writer — the manifests reach ``call_segments`` on the backfill path.

    The trace file is the WHOLE JOB's, copied beside the evidence by the
    exporter, so the reader has to filter by ``task_id`` and number the entries
    it keeps. Everything below drives the real functions over real files: no
    private tracer helper is imported and no manifest is mocked.

    ``BackfillResult`` is FROZEN BEHAVIOUR here. The end-to-end test asserts the
    four counters against the SAME tree backfilled without a trace file, so a
    segment write that ever started moving one would be visible immediately.
    """

    def test_two_entries_yield_their_rows_in_file_order(self, tmp_path):
        brief = _manifest_entry("task_brief", 10, "a" * 64, 120, 30)
        diff = _manifest_entry("diff", 20, "b" * 64, 400, 100)
        tail = _manifest_entry("schema_tail", 30, "c" * 64, 60, 15)
        trace = tmp_path / "prompt_trace.jsonl"
        _write_trace_file(trace, [
            _trace_entry(SEGMENT_TASK, [brief, diff]),
            _trace_entry(SEGMENT_TASK, [tail]),
        ])

        rows = segment_rows_from_trace_file(
            trace, call_id="job-7:T001", task_id=SEGMENT_TASK
        )

        assert rows == [
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=0, segment_name="task_brief",
                segment_rank=10, segment_sha256="a" * 64, chars=120,
                tokens_estimated=30,
            ),
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=0, segment_name="diff",
                segment_rank=20, segment_sha256="b" * 64, chars=400,
                tokens_estimated=100,
            ),
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=1, segment_name="schema_tail",
                segment_rank=30, segment_sha256="c" * 64, chars=60,
                tokens_estimated=15,
            ),
        ]

    def test_an_empty_manifest_yields_no_row_but_still_consumes_its_index(self, tmp_path):
        """The index counts PROVIDER CALLS, so it cannot shift when one is empty."""
        carried = _manifest_entry("task_brief", 10, "d" * 64, 88, 22)
        trace = tmp_path / "prompt_trace.jsonl"
        _write_trace_file(trace, [
            _trace_entry(SEGMENT_TASK, []),
            _trace_entry(SEGMENT_TASK, [carried]),
        ])

        rows = segment_rows_from_trace_file(
            trace, call_id="job-7:T001", task_id=SEGMENT_TASK
        )

        assert [row.trace_seq for row in rows] == [1]
        assert rows[0].segment_name == "task_brief"

    def test_another_task_runs_entries_are_ignored(self, tmp_path):
        """The copied file is the whole job's trace, not this task run's."""
        mine = _manifest_entry("task_brief", 10, "e" * 64, 11, 2)
        theirs = _manifest_entry("other_task_brief", 10, "f" * 64, 99, 24)
        trace = tmp_path / "prompt_trace.jsonl"
        _write_trace_file(trace, [
            _trace_entry("T099", [theirs]),
            _trace_entry(SEGMENT_TASK, [mine]),
            _trace_entry("T099", [theirs]),
        ])

        rows = segment_rows_from_trace_file(
            trace, call_id="job-7:T001", task_id=SEGMENT_TASK
        )

        assert [(row.trace_seq, row.segment_name) for row in rows] == [
            (0, "task_brief")
        ]

    def test_absent_malformed_and_partial_inputs_never_raise(self, tmp_path):
        """A missing file, a corrupt line and a partial manifest dict, all survivable."""
        assert segment_rows_from_trace_file(
            tmp_path / "nowhere" / "prompt_trace.jsonl",
            call_id="job-7:T001", task_id=SEGMENT_TASK,
        ) == []

        brief = _manifest_entry("task_brief", 10, "e" * 64, 11, 2)
        partial = _manifest_entry("diff", 20, "f" * 64, 22, 5)
        del partial["tokens_estimated"]
        sibling = _manifest_entry("schema_tail", 30, "9" * 64, 33, 8)
        trace = tmp_path / "prompt_trace.jsonl"
        trace.write_text(
            json.dumps(_trace_entry(SEGMENT_TASK, [brief])) + "\n"
            + "{not json at all\n"
            + json.dumps(_trace_entry(SEGMENT_TASK, [partial, sibling])) + "\n",
            encoding="utf-8",
        )

        rows = segment_rows_from_trace_file(
            trace, call_id="job-7:T001", task_id=SEGMENT_TASK
        )

        # The corrupt line consumed no index, and the partial dict was SKIPPED
        # rather than completed with a zero its sibling would then be summed with.
        assert [(row.trace_seq, row.segment_name) for row in rows] == [
            (0, "task_brief"), (1, "schema_tail")
        ]

    def test_recording_the_same_segments_twice_leaves_one_row_each(
        self, ledger_path, tmp_path
    ):
        rows = [
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=0, segment_name="task_brief",
                segment_rank=10, segment_sha256="a" * 64, chars=120,
                tokens_estimated=30,
            ),
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=0, segment_name="diff",
                segment_rank=20, segment_sha256="b" * 64, chars=400,
                tokens_estimated=100,
            ),
        ]
        assert record_call_segments(rows, path=ledger_path) is True
        assert record_call_segments(rows, path=ledger_path) is True
        assert _segment_count(ledger_path) == len(rows)

        # Nothing to store must not be the thing that creates a database.
        untouched = tmp_path / "no-ledger-here" / LEDGER_FILENAME
        assert record_call_segments([], path=untouched) is True
        assert not untouched.exists()
        assert not untouched.parent.exists()

    def test_backfill_writes_the_segment_rows_and_moves_no_counter(
        self, evidence_tree, ledger_path, tmp_path
    ):
        """End to end, against the frozen ``BackfillResult`` of the same tree."""
        without_trace = backfill_ledger(
            evidence_tree, path=tmp_path / "baseline" / LEDGER_FILENAME
        )

        brief = _manifest_entry("task_brief", 10, "a" * 64, 120, 30)
        _write_trace_file(
            evidence_tree / "task_runs" / SEGMENT_TASK / "prompt_trace.jsonl",
            [_trace_entry(SEGMENT_TASK, [brief])],
        )
        with_trace = backfill_ledger(evidence_tree, path=ledger_path)

        assert _segment_rows(ledger_path) == [{
            "call_id": f"{FIXTURE_JOB_ID}:{SEGMENT_TASK}",
            "trace_seq": 0,
            "segment_name": "task_brief",
            "segment_rank": 10,
            "segment_sha256": "a" * 64,
            "chars": 120,
            "tokens_estimated": 30,
        }]
        assert _row(ledger_path, f"{FIXTURE_JOB_ID}:{SEGMENT_TASK}") is not None

        counters = (with_trace.scanned, with_trace.recorded,
                    with_trace.skipped, with_trace.failed)
        assert counters == (without_trace.scanned, without_trace.recorded,
                            without_trace.skipped, without_trace.failed)
        assert counters == (4, 2, 1, 1)

    def test_a_wrongly_typed_manifest_value_is_skipped_like_a_missing_key(self, tmp_path):
        """R-0329: a string ``chars`` would be stored as TEXT and SUM to 0."""
        text_chars = _manifest_entry("diff", 20, "a" * 64, "not-a-number", 5)
        flag_tokens = _manifest_entry("schema_tail", 30, "b" * 64, 33, True)
        sibling = _manifest_entry("task_brief", 10, "c" * 64, 120, 30)
        # The fixture derives ``segment_manifest_chars`` by summing the entries,
        # which a non-numeric ``chars`` cannot survive; the manifest is swapped
        # in afterwards so the file on disk carries exactly the bad values.
        entry = _trace_entry(SEGMENT_TASK, [sibling])
        entry["segment_manifest"] = [text_chars, sibling, flag_tokens]
        trace = tmp_path / "prompt_trace.jsonl"
        _write_trace_file(trace, [entry])

        rows = segment_rows_from_trace_file(
            trace, call_id="job-7:T001", task_id=SEGMENT_TASK
        )

        # Both bad dicts are gone and the well-formed sibling is untouched, so
        # nothing that reaches the ledger can become a measured zero later.
        assert rows == [
            CallSegmentRow(
                call_id="job-7:T001", trace_seq=0, segment_name="task_brief",
                segment_rank=10, segment_sha256="c" * 64, chars=120,
                tokens_estimated=30,
            ),
        ]


# ── F115 T002: the per-segment share aggregation ─────────────────────────────
# Two evidence trees backfilled into ONE ledger by the REAL backfill: a job whose
# two task runs carry a copied prompt trace, and a job whose single task run does
# not. That shape is what lets one fixture pin the grouping, the pinned row
# order, both filters, the totals and — the point of the feature — a call the
# tracer never covered, which is an absence rather than a zero share.

SHARE_JOB_TRACED = "job-traced"
SHARE_JOB_BARE = "job-bare"


def _share_evidence_tree(base, job_id, task_runs):
    """An evidence tree for ``job_id``; ``task_runs`` is ``(task_id, ts_utc, manifest)``.

    A ``manifest`` of None leaves that task run WITHOUT a ``prompt_trace.jsonl``,
    which is the pre-F115 shape on disk. Nothing here is mocked: these are the
    files the exporter writes, read back by the real backfill.
    """
    _write_json_file(base / "manifest.json",
                     {"bundle_type": "job_evidence", "job_id": job_id})
    for task_id, ts_utc, manifest in task_runs:
        run = base / "task_runs" / task_id
        _write_json_file(run / "provider_evidence.json", {
            "schema_version": "1.0.0",
            "task_id": task_id,
            "execution_mode": "provider_backed",
            "provider_call_count": 1,
            "actual_call_count": 1,
            "cost_call_count": 1,
            "actual_prompt_tokens": 1000,
            "actual_completion_tokens": 200,
            "ts_utc": ts_utc,
        })
        _write_json_file(run / "token_accounting.json", {"role": "builder"})
        if manifest is not None:
            entry = _trace_entry(task_id, manifest)
            entry["job_id"] = job_id
            _write_trace_file(run / "prompt_trace.jsonl", [entry])
    return base


@pytest.fixture
def share_ledger(ledger_path, tmp_path):
    """Three calls: two traced ones in one job, one untraced one in another.

    ``diff`` and ``schema_tail`` publish the SAME ``tokens_estimated`` on purpose,
    so the fixture pins the tie-break of the row order and not only its direction.
    """
    brief = _manifest_entry("task_brief", 10, "a" * 64, 120, 30)
    diff = _manifest_entry("diff", 20, "b" * 64, 400, 100)
    tail = _manifest_entry("schema_tail", 30, "c" * 64, 60, 100)

    traced = _share_evidence_tree(
        tmp_path / "evidence" / SHARE_JOB_TRACED, SHARE_JOB_TRACED,
        [("T001", "2026-08-01T10:00:00+00:00", [brief, diff]),
         ("T002", "2026-08-05T10:00:00+00:00", [tail])],
    )
    bare = _share_evidence_tree(
        tmp_path / "evidence" / SHARE_JOB_BARE, SHARE_JOB_BARE,
        [("T001", "2026-08-09T10:00:00+00:00", None)],
    )
    assert backfill_ledger(traced, path=ledger_path).recorded == 2
    assert backfill_ledger(bare, path=ledger_path).recorded == 1
    return ledger_path


class TestQuerySegmentShares:
    """F115 T002-Query — where the tokens went, and how much of that we know.

    The whole class reads a ledger the real ``backfill_ledger`` wrote from real
    files; no row here was hand-inserted with SQL, so a writer that stopped
    producing these rows would fail these tests rather than pass them.
    """

    def test_shares_group_by_segment_name_in_the_pinned_row_order(self, share_ledger):
        """``tokens_estimated`` DESC, then ``segment_name`` ASC — R11 pins bytes on it."""
        report = query_segment_shares(path=share_ledger)

        assert report.rows == [
            SegmentShareRow(segment_name="diff", calls=1, segments=1,
                            chars=400, tokens_estimated=100),
            SegmentShareRow(segment_name="schema_tail", calls=1, segments=1,
                            chars=60, tokens_estimated=100),
            SegmentShareRow(segment_name="task_brief", calls=1, segments=1,
                            chars=120, tokens_estimated=30),
        ]
        assert report.ledger_exists is True

    def test_a_call_without_segment_rows_is_unattributed_and_in_no_share_row(
        self, share_ledger
    ):
        """The pre-F115 shape is reported as a missing row, never as a 0 share."""
        everything = query_segment_shares(path=share_ledger)
        traced_only = query_segment_shares(path=share_ledger, job_id=SHARE_JOB_TRACED)
        bare_only = query_segment_shares(path=share_ledger, job_id=SHARE_JOB_BARE)

        assert (everything.attributed_calls, everything.unattributed_calls) == (2, 1)
        assert (traced_only.attributed_calls, traced_only.unattributed_calls) == (2, 0)
        assert (bare_only.attributed_calls, bare_only.unattributed_calls) == (0, 1)

        # The untraced call moves nothing: the shares are identical with and
        # without it in the period, so it was counted and not distributed.
        assert bare_only.rows == []
        assert everything.rows == traced_only.rows

    def test_the_shares_sum_to_the_totals_and_the_calls_match_query_cost(
        self, share_ledger
    ):
        """The Acceptance line: nothing in the report may disagree with itself."""
        report = query_segment_shares(path=share_ledger)

        assert sum(row.segments for row in report.rows) == report.total_segments
        assert sum(row.chars for row in report.rows) == report.total_chars
        assert sum(
            row.tokens_estimated for row in report.rows
        ) == report.total_tokens_estimated
        assert (report.total_segments, report.total_chars,
                report.total_tokens_estimated) == (3, 580, 230)

        assert report.attributed_calls + report.unattributed_calls == query_cost(
            path=share_ledger).total.calls
        narrowed = query_segment_shares(path=share_ledger, since="2026-08-05")
        assert narrowed.attributed_calls + narrowed.unattributed_calls == query_cost(
            path=share_ledger, since="2026-08-05").total.calls

    def test_since_and_job_id_narrow_the_rows_and_both_attribution_counts(
        self, share_ledger
    ):
        """A call outside the period is in neither the shares nor either count."""
        since = query_segment_shares(path=share_ledger, since="2026-08-05")
        assert since.rows == [
            SegmentShareRow(segment_name="schema_tail", calls=1, segments=1,
                            chars=60, tokens_estimated=100),
        ]
        assert (since.attributed_calls, since.unattributed_calls) == (1, 1)

        job = query_segment_shares(path=share_ledger, job_id=SHARE_JOB_TRACED)
        assert [row.segment_name for row in job.rows] == [
            "diff", "schema_tail", "task_brief"]
        assert (job.attributed_calls, job.unattributed_calls) == (2, 0)

        both = query_segment_shares(
            path=share_ledger, since="2026-08-05", job_id=SHARE_JOB_TRACED)
        assert both.rows == since.rows
        assert (both.attributed_calls, both.unattributed_calls) == (1, 0)
        assert (both.since, both.job_id) == ("2026-08-05", SHARE_JOB_TRACED)

    def test_until_narrows_the_shares_exactly_as_it_narrows_the_cost(
        self, share_ledger
    ):
        """ONE ``_cost_filters`` clause, so the pair cannot disagree on the period.

        The boundary is the traced 08-05 call's own timestamp, so the EXCLUSIVE
        end drops it together with the untraced 08-09 one and leaves only the
        08-01 call — whose two segment kinds are the whole breakdown.
        """
        boundary = "2026-08-05T10:00:00+00:00"

        shares = query_segment_shares(path=share_ledger, until=boundary)
        cost = query_cost(path=share_ledger, until=boundary)

        assert [row.segment_name for row in shares.rows] == ["diff", "task_brief"]
        assert (shares.attributed_calls, shares.unattributed_calls) == (1, 0)
        assert shares.attributed_calls + shares.unattributed_calls == cost.total.calls
        assert shares.until == boundary == cost.until

    def test_a_missing_ledger_yields_an_empty_report_and_creates_nothing(self, tmp_path):
        """Asking where the tokens went must not be what brings a ledger into being."""
        absent = tmp_path / "projects" / str(uuid4()) / LEDGER_FILENAME

        report = query_segment_shares(path=absent, since="2026-08-01")

        assert report.ledger_exists is False
        assert report.rows == []
        assert (report.attributed_calls, report.unattributed_calls) == (0, 0)
        assert (report.total_segments, report.total_chars,
                report.total_tokens_estimated) == (0, 0, 0)
        assert not absent.exists()
        assert not absent.parent.exists(), "a query created a project directory"

    def test_the_report_changes_no_byte_and_leaves_no_wal_beside_the_ledger(
        self, share_ledger
    ):
        """Report generation touches nothing — measured on the bytes themselves."""
        before = share_ledger.read_bytes()

        query_segment_shares(path=share_ledger)
        query_segment_shares(path=share_ledger, since="2026-08-01",
                             job_id=SHARE_JOB_TRACED)

        assert share_ledger.read_bytes() == before
        assert sorted(p.name for p in share_ledger.parent.iterdir()) == [
            LEDGER_FILENAME]


# ---------------------------------------------------------------------------
# Operator order amend0828-daily-driver, point 2 — cost truth on the JOB RUNNER
#
# The 2026-08-25 dogfooding finding in T2_F103: two real claude-cli calls with
# measured usage ran under `remedy do job-run`, and `remedy stats cost` then
# reported "0 ledger(s) read". The scope was right and the report was honest —
# the ledger simply did not exist, because the live mirror is armed only from
# `export_job_evidence` and the job runner never reached it.
#
# The operator ruled for the shape with the least wiring depth: reuse the seam
# that is already armed, rather than reopen DECISION D16's row granularity or
# add a second backfill source that would leave `stats cost` empty until someone
# asked. `mirror_job_run_into_ledger` is that one call.
# ---------------------------------------------------------------------------


from packages.orchestration.pingpong_provider import FakeProvider  # noqa: E402


class _MeasuredStubProvider(FakeProvider):
    """A FakeProvider that reports MEASURED usage, like a real CLI provider does.

    `_aggregate_usage_actuals` skips every attempt whose provider is named
    ``fake``, so a stub that wants its usage counted must not be called that.
    Cost coverage must be COMPLETE for `total_cost_usd` to survive aggregation,
    which is why both roles report — a half-measured run is deliberately NULL.
    """

    #: One call's reported usage. Small, exact, and asserted on downstream.
    USAGE = {
        "input_tokens": 1000,
        "output_tokens": 500,
        "cache_read": 0,
        "cache_creation": 0,
        "total_cost_usd": 0.125,
        "num_turns": 1,
        "duration_ms": 10,
        "session_id": "stub-session",
        "cli_version": "stub-1.0",
        "parse_source": "claude_cli_json",
    }

    #: Any name but "fake" — see `_run_measured_job`.
    PROVIDER_NAME = "measured-stub"

    @property
    def name(self) -> str:
        return self.PROVIDER_NAME

    def build(self, prompt, **kwargs):
        out = super().build(prompt, **kwargs)
        out.usage_actuals = dict(self.USAGE)
        return out

    def review(self, prompt, **kwargs):
        out = super().review(prompt, **kwargs)
        out.usage_actuals = dict(self.USAGE)
        return out


def _run_measured_job(repo):
    """A real `run_job` whose provider calls carry measured usage."""
    from packages.orchestration.pingpong_job import parse_job_file, run_job

    plan = parse_job_file(_LIVE_JOB_FILE, str(repo))
    # The NAME matters as much as the object: `_aggregate_usage_actuals` skips
    # every attempt whose recorded provider is "fake", and the recorded name comes
    # from `builder_name`/`reviewer_name`, not from the injected object's own
    # `.name`. A stub that only overrides the property is silently uncounted.
    return run_job(
        plan.job_id,
        builder_name=_MeasuredStubProvider.PROVIDER_NAME,
        reviewer_name=_MeasuredStubProvider.PROVIDER_NAME,
        builder_provider=_MeasuredStubProvider(pass_on_round=1, fail_on_round=99),
        reviewer_provider=_MeasuredStubProvider(pass_on_round=1, fail_on_round=99),
        repair_rounds=0,
    )


class TestCostTruthOnTheJobRunPath:
    """`stats cost` must find a row after a run, without anyone exporting by hand."""

    def test_a_measured_run_leaves_a_row_stats_cost_finds(
        self, live_data_root, live_job_repo,
    ):
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("cost-truth", str(live_job_repo))
        job = _run_measured_job(live_job_repo)

        # This is the ONE call `remedy do job-run` now makes. Nothing else here
        # arms the ledger, and no ledger_* argument is passed by hand.
        mirror = mirror_job_run_into_ledger(job.job_id)
        assert mirror["ledger_mirrored"] is True, mirror["error"]

        report = query_cost(project_id=project.id)

        assert report.ledger_exists is True, (
            "remedy stats cost would still report 'No ledger on disk for this "
            "scope' after a real run — the dogfooding finding is not fixed"
        )
        assert report.total.calls >= 1
        assert report.project_id == str(project.id)

        # The money is VISIBLE, not merely counted.
        assert report.total.cost_usd is not None
        assert report.total.cost_usd > 0
        assert report.total.measured_calls >= 1

    def test_the_row_lands_in_the_right_project_scope(
        self, live_data_root, live_job_repo, tmp_path,
    ):
        """A job's cost belongs to the repo the job ran against, not an ambient one."""
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        from packages.orchestration.project_registry import register_project_repo

        other_repo = _git_repo(tmp_path / "other_repo")
        project = register_project_repo("cost-truth", str(live_job_repo))
        other = register_project_repo("cost-truth-other", str(other_repo))

        job = _run_measured_job(live_job_repo)
        mirror_job_run_into_ledger(job.job_id)

        assert query_cost(project_id=project.id).total.calls >= 1
        assert query_cost(project_id=other.id).total.calls == 0
        assert token_ledger_path_for(other.id).is_file() is False

    def test_unmeasured_cost_stays_honestly_unmeasured(
        self, live_data_root, live_job_repo,
    ):
        """P6: an unmeasured figure must never render as a measured zero."""
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("cost-truth", str(live_job_repo))
        job = _run_fake_provider_job(live_job_repo)   # reports no usage at all

        mirror = mirror_job_run_into_ledger(job.job_id)
        assert mirror["ledger_mirrored"] is True, mirror["error"]

        report = query_cost(project_id=project.id)
        assert report.ledger_exists is True
        assert report.total.calls >= 1

        # NOT 0.0 — the call is counted, the money is unknown, and it says so.
        assert report.total.cost_usd is None
        assert report.total.measured_calls == 0
        assert report.total.unmeasured_calls >= 1

        row = _row(token_ledger_path_for(project.id), f"{job.job_id}:T001")
        assert row["cost_usd"] is None
        assert row["cost_basis"] == COST_BASIS_UNKNOWN

    def test_the_measured_row_carries_the_provider_reported_basis(
        self, live_data_root, live_job_repo,
    ):
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("cost-truth", str(live_job_repo))
        job = _run_measured_job(live_job_repo)
        mirror_job_run_into_ledger(job.job_id)

        row = _row(token_ledger_path_for(project.id), f"{job.job_id}:T001")
        assert row["cost_basis"] == COST_BASIS_PROVIDER_REPORTED
        assert row["cost_usd"] is not None
        assert row["tokens_in"] is not None and row["tokens_in"] > 0

    def test_mirroring_twice_adds_no_second_row(
        self, live_data_root, live_job_repo,
    ):
        """`do job-run` then `do job-evidence` must not double-count the money."""
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger
        from packages.orchestration.project_registry import register_project_repo

        project = register_project_repo("cost-truth", str(live_job_repo))
        job = _run_measured_job(live_job_repo)

        mirror_job_run_into_ledger(job.job_id)
        first = query_cost(project_id=project.id).total
        mirror_job_run_into_ledger(job.job_id)
        second = query_cost(project_id=project.id).total

        assert second.calls == first.calls
        assert second.cost_usd == first.cost_usd

    def test_a_mirror_failure_never_fails_the_run(self, live_data_root):
        """A job that ran is a job that ran; an unmirrorable one reports and moves on."""
        from packages.orchestration.job_evidence import mirror_job_run_into_ledger

        mirror = mirror_job_run_into_ledger("no-such-job-id")

        assert mirror["ledger_mirrored"] is False
        assert mirror["error"]


class TestJobRunActuallyCallsTheMirror:
    """A working seam nobody calls is the original defect in another dress.

    The finding was never that the mirror could not record — `do job-evidence`
    already proved it could. It was that `remedy do job-run` did not reach it.
    So the wiring is asserted on the COMMAND, not only on the function.
    """

    def test_the_job_run_command_mirrors_the_job_it_just_ran(self, monkeypatch):
        from apps.cli.commands import do_cmd
        from packages.orchestration import job_evidence, pingpong_job

        class _StubJob:
            job_id = "jid-under-test"

        monkeypatch.setattr(pingpong_job, "run_job", lambda *a, **k: _StubJob())
        monkeypatch.setattr(
            pingpong_job, "format_job_report_text", lambda job: "report",
        )

        seen: list[str] = []

        def _record(job_id):
            seen.append(job_id)
            return {"ledger_mirrored": True, "out_dir": "/tmp/x", "error": ""}

        monkeypatch.setattr(job_evidence, "mirror_job_run_into_ledger", _record)

        do_cmd._cmd_do_job_run("jid-under-test")

        assert seen == ["jid-under-test"], (
            "remedy do job-run did not mirror its own run into the ledger: "
            "stats cost would still be empty after a real run"
        )

    def test_a_mirror_failure_does_not_crash_the_command(self, monkeypatch, capsys):
        from apps.cli.commands import do_cmd
        from packages.orchestration import job_evidence, pingpong_job

        class _StubJob:
            job_id = "jid-under-test"

        monkeypatch.setattr(pingpong_job, "run_job", lambda *a, **k: _StubJob())
        monkeypatch.setattr(
            pingpong_job, "format_job_report_text", lambda job: "report",
        )
        monkeypatch.setattr(
            job_evidence, "mirror_job_run_into_ledger",
            lambda job_id: {"ledger_mirrored": False, "out_dir": "",
                            "error": "boom"},
        )

        do_cmd._cmd_do_job_run("jid-under-test")

        err = capsys.readouterr().err
        assert "Cost NOT recorded to the ledger" in err
        assert "backfill-ledger" in err
