"""F103 T001 — the token ledger: a per-project SQLite mirror of provider calls.

Actuals capture already exists file-based, one record per provider call. What
it cannot do is answer a question: "what did the reviewer role cost last week",
"how many tokens did job X burn". This module adds the QUERYABLE store for
exactly those questions, and nothing else.

The file evidence remains the source of truth and the database is a mirror.
Every row here restates something a file already says, which is what makes the
two rules below safe: a ledger write may fail without failing the run, and a
missing row is a reconcilable defect rather than lost data. Nothing in Remedy
may read a cost figure from this database and treat it as authoritative when
the evidence files disagree — the files win, and ``remedy stats
verify-ledger`` (T002) is how the disagreement is found.

SQLITE NOTE: this is the FIRST and so far ONLY place in Remedy that uses
SQLite. Everything else persists as atomic JSON files under the data root
(``storage.py``, ``project_registry.py``, ``mission_state.py``). A reader
looking for "where does Remedy use a database" lands here and finds all of it.
The precedent this module sets — Python's bundled ``sqlite3`` only, WAL mode,
schema versioning through a ``meta`` row, transactions of one statement — is
meant to be copied by any later writer, not re-invented.

Deliberate absences, documented here because text search cannot find code that
does not exist:

* Remedy deliberately does NOT add an ORM or any third-party database
  dependency for this. The bundled ``sqlite3`` module covers every query this
  feature needs, and the feature's Orchestrator brief rejects the alternative.
* Remedy deliberately does NOT add a second capture path. This module records
  what the existing actuals path already produced; it never parses a provider
  response itself: the usage counters come from ``token_truth``'s existing
  extractor rather than from a second parse of provider output. Its ONE call
  site is the seam where actuals are finalized
  (``pingpong_evidence.write_evidence_bundle``), where it is opt-in and stays
  inert until a caller names a ledger target.
* Remedy deliberately does NOT store one row per HTTP request. A ROW IS ONE
  FINALIZED TASK RUN, keyed ``"<job_id>:<task_id>"`` (DECISION D16, recorded on
  the feature file): ``task_runs/<task_id>/provider_evidence.json`` is the
  finest record the actuals feature puts on disk, and a per-request row would
  have to invent ids, timestamps and a usage split no file records. F115 D4 adds
  ``call_segments`` BESIDE it rather than widening it — one row per segment of
  one composed prompt, keyed by the row's ``call_id`` plus the trace line's
  position — so the per-call breakdown lives in its own table and ``calls``
  keeps its one-row-per-task-run identity untouched.
* Remedy deliberately does NOT invent prices. ``cost_usd`` stays NULL unless a
  caller supplies a real figure together with the basis it came from, and a
  call with no reported usage produces NULL counts with basis ``unknown``
  rather than a fabricated zero. There is no price table in this round.
* Budget counting deliberately does NOT read this database. ``budget_guard.py``
  and ``budget_resolution.py`` read the actuals files directly; switching them
  is a later, explicit change.

Public API::

    SCHEMA_VERSION: int
    SCHEMA_VERSION_KEY / LEDGER_FILENAME / BUSY_TIMEOUT_MS
    COST_BASIS_PROVIDER_REPORTED / COST_BASIS_PRICE_TABLE / COST_BASIS_UNKNOWN
    COST_BASES: frozenset[str]
    CallRecord / CallSegmentRow / BackfillResult / ReconcileResult
    CostRow / CostReport / COST_GROUP_KEYS
    token_ledger_path_for(project_id, root=None) -> Path
    open_ledger(path) -> sqlite3.Connection
    record_call(record, *, project_id=None, path=None) -> bool
    record_call_segments(rows, *, project_id=None, path=None) -> bool
    ledger_miss_count() -> int
    reset_ledger_miss_count() -> None
    call_id_for_task_run(job_id, task_id) -> str
    job_id_for_evidence_dir(evidence_dir) -> str
    call_record_from_evidence(evidence_dir, job_id, task_id) -> CallRecord | None
    segment_rows_from_trace_file(trace_path, *, call_id, task_id)
        -> list[CallSegmentRow]
    backfill_ledger(evidence_dir, *, project_id=None, path=None) -> BackfillResult
    verify_ledger(evidence_dir, *, project_id=None, path=None) -> ReconcileResult
    query_cost(*, project_id=None, path=None, since=None, job_id=None, by=None)
        -> CostReport
    merge_cost_reports(reports) -> CostReport
"""

from __future__ import annotations

import logging
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.common.strict_json import StrictJsonError, strict_loads
from packages.orchestration.data_paths import projects_dir

# The usage counters come from the parser the actuals feature ALREADY uses. A
# second parse of provider output here would be the SECOND CAPTURE PATH the
# feature file's Orchestrator brief rejects, and it would be free to disagree
# with the numbers the evidence files publish. ``_strict_cost`` is imported for
# the same reason: one spelling of "what is a valid cost figure", not two.
from packages.orchestration.token_truth import (
    TokenEvidenceError,
    _extract_actual,
    _strict_cost,
)

logger = logging.getLogger(__name__)


# The on-disk schema generation; bump it only together with a new migration step.
SCHEMA_VERSION = 2

# The meta key carrying SCHEMA_VERSION, so a future reader can tell old DBs apart.
SCHEMA_VERSION_KEY = "schema_version"

# One ledger file per project; the name is fixed so tooling can find it by path.
LEDGER_FILENAME = "ledger.sqlite"

# How long a writer waits for another writer's lock before giving up (ms).
BUSY_TIMEOUT_MS = 5000

# The evidence-tree layout this module mirrors; the actuals feature owns these names.
_TASK_RUNS_DIRNAME = "task_runs"
_PROVIDER_EVIDENCE_FILENAME = "provider_evidence.json"
_TOKEN_ACCOUNTING_FILENAME = "token_accounting.json"
_JOB_MANIFEST_FILENAME = "manifest.json"

# The prompt trace the evidence exporter COPIES into the task-run directory
# beside provider_evidence.json (``pingpong_evidence.py:533``); it is the only
# place a finalized task run publishes its per-call segment manifests.
_PROMPT_TRACE_FILENAME = "prompt_trace.jsonl"

# Timestamp fields the evidence may carry, most specific first; else the file mtime.
_TIMESTAMP_FIELDS = ("ts_utc", "finished_at", "started_at")

# Model fields that name the model that ACTUALLY ran — configured models are not it.
_VERIFIED_MODEL_FIELDS = ("builder_actual_model", "reviewer_actual_model")
_NAMED_MODEL_FIELDS = ("model", "builder_model")

# The three honest answers to "where does this cost figure come from" (P6).
COST_BASIS_PROVIDER_REPORTED = "provider_reported"
COST_BASIS_PRICE_TABLE = "price_table"
COST_BASIS_UNKNOWN = "unknown"

# The closed set of bases; the schema CHECK is built from it so the two cannot drift.
COST_BASES = frozenset(
    {COST_BASIS_PROVIDER_REPORTED, COST_BASIS_PRICE_TABLE, COST_BASIS_UNKNOWN}
)

# Column order of the calls table, mirroring CallRecord's field order exactly.
_CALL_COLUMNS = (
    "call_id",
    "job_id",
    "task_id",
    "role",
    "model",
    "ts_utc",
    "tokens_in",
    "tokens_out",
    "cache_read",
    "cache_write",
    "cost_usd",
    "cost_basis",
    "evidence_ref",
)

_COST_BASIS_CHECK = ", ".join(f"'{b}'" for b in sorted(COST_BASES))

# The three group keys ``query_cost`` understands; None means "grand total only".
COST_GROUP_KEYS: tuple[str, ...] = ("role", "model", "day")

# How each group key becomes a SQL bucket expression. Values are literals of this
# module, never caller input, so they are safe to inline into the statement.
_COST_GROUP_EXPRESSIONS: dict[str, str] = {
    "role": "role",
    "model": "model",
    # The first 10 characters of an ISO-8601 UTC timestamp ARE its calendar day.
    "day": "substr(ts_utc, 1, 10)",
}

# Migrations as NUMBERED STEPS, not an if-ladder: version 2 appends an entry and
# version 1's path is never rewritten, which is what keeps old DBs upgradable.
_MIGRATIONS: dict[int, tuple[str, ...]] = {
    1: (
        """
        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """,
        f"""
        CREATE TABLE IF NOT EXISTS calls (
            call_id      TEXT PRIMARY KEY NOT NULL,
            job_id       TEXT,
            task_id      TEXT,
            role         TEXT,
            model        TEXT,
            ts_utc       TEXT NOT NULL,
            tokens_in    INTEGER,
            tokens_out   INTEGER,
            cache_read   INTEGER,
            cache_write  INTEGER,
            cost_usd     REAL,
            cost_basis   TEXT NOT NULL CHECK (cost_basis IN ({_COST_BASIS_CHECK})),
            evidence_ref TEXT
        )
        """,
        # Covering indexes for the three query patterns the feature names.
        "CREATE INDEX IF NOT EXISTS idx_calls_job_id ON calls (job_id)",
        "CREATE INDEX IF NOT EXISTS idx_calls_ts_utc ON calls (ts_utc)",
        "CREATE INDEX IF NOT EXISTS idx_calls_role_model ON calls (role, model)",
    ),
    # F115 D4: the segment manifest is per PROVIDER CALL while a `calls` row is
    # one finalized TASK RUN, so it gets its own table instead of a column. The
    # value columns mirror ComposedPrompt.manifest_as_dicts() one for one, so a
    # writer never has to invent or rename a field.
    2: (
        """
        CREATE TABLE IF NOT EXISTS call_segments (
            call_id          TEXT NOT NULL,
            trace_seq        INTEGER NOT NULL,
            segment_name     TEXT NOT NULL,
            segment_rank     INTEGER NOT NULL,
            segment_sha256   TEXT NOT NULL,
            chars            INTEGER NOT NULL,
            tokens_estimated INTEGER NOT NULL,
            PRIMARY KEY (call_id, trace_seq, segment_name)
        )
        """,
        "CREATE INDEX IF NOT EXISTS idx_call_segments_call_id ON call_segments (call_id)",
    ),
}


# One provider call as the ledger stores it; only call_id and ts_utc are required.
@dataclass(kw_only=True)
class CallRecord:
    """A single provider call.

    Every count and the cost default to ``None`` on purpose: a call whose
    provider reported no usage must land as NULLs with basis ``unknown``, never
    as a fabricated zero. Field order matches ``_CALL_COLUMNS``.

    Keyword-only so that ``call_id`` and ``ts_utc`` can both stay genuinely
    required while every field between them carries a default — and so that a
    thirteen-field record can never be built by positional accident.
    """

    call_id: str
    job_id: str | None = None
    task_id: str | None = None
    role: str | None = None
    model: str | None = None
    ts_utc: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    cache_read: int | None = None
    cache_write: int | None = None
    cost_usd: float | None = None
    cost_basis: str = COST_BASIS_UNKNOWN
    evidence_ref: str | None = None


# Column order restated once, exactly as migration step 2 declares it, so the
# INSERT and every later SELECT are built from ONE source and cannot drift.
_CALL_SEGMENT_COLUMNS = (
    "call_id",
    "trace_seq",
    "segment_name",
    "segment_rank",
    "segment_sha256",
    "chars",
    "tokens_estimated",
)

# The manifest keys a trace entry publishes, in the order the columns above take
# them. Named once so a missing key is detected rather than defaulted to zero.
_MANIFEST_KEYS = ("name", "rank", "sha256", "chars", "tokens_estimated")


@dataclass(frozen=True)
class CallSegmentRow:
    """One segment of one composed prompt, as the ledger stores it.

    Mirrors ``ComposedPrompt.manifest_as_dicts()`` one field per key
    (``prompt_segments.py:107-121``) plus two identity columns: the ledger row's
    ``call_id``, and ``trace_seq`` — the zero-based position of the trace line
    among THAT TASK RUN's entries, which is what makes a re-read of the same
    static file produce the same keys and a repeat backfill a no-op.

    A trace entry whose ``segment_manifest`` is empty produces NO row at all.
    That absence is what the report renders as unattributed; it is never a zero,
    and no row is ever invented to stand in for it.
    """

    call_id: str
    trace_seq: int
    segment_name: str
    segment_rank: int
    segment_sha256: str
    chars: int
    tokens_estimated: int


# What one backfill pass did, in counts a caller can report without re-scanning.
@dataclass
class BackfillResult:
    """The outcome of one ``backfill_ledger`` pass.

    ``scanned`` task-run directories, of which ``recorded`` produced a durable
    row (already-durable rows included — that is why a second pass over the same
    evidence reports the SAME total without creating a duplicate), ``skipped``
    carried no ``provider_evidence.json`` to mirror at all, and ``failed`` could
    not be recorded: malformed evidence, or a write the ledger rejected.

    ``scanned == recorded + skipped + failed`` holds by construction, so a
    caller can always tell that no task run was silently dropped.
    """

    scanned: int = 0
    recorded: int = 0
    skipped: int = 0
    failed: int = 0


# What a read-only reconcile found: where the mirror disagrees with the files.
@dataclass
class ReconcileResult:
    """Drift between the evidence files and the ledger rows.

    THE FILES ARE THE SOURCE OF TRUTH AND THE DATABASE IS THE MIRROR. Every
    entry below therefore reads as "the DB is wrong", never as "the files are
    wrong" — there is no direction in which evidence gets corrected to match a
    row.

    ``checked`` task runs carried provider evidence and were compared.
    ``missing_rows`` are call_ids on disk with no row (a lost write — a counted
    miss, a crash, a ledger that did not exist yet). ``orphan_rows`` are
    call_ids in the DB whose evidence is gone. ``drifted_rows`` are call_ids
    whose stored row no longer matches what its evidence says it should be.
    ``unreadable`` are task runs whose evidence could not be turned into a row
    at all, so nothing about them can be asserted in either direction.
    """

    checked: int = 0
    missing_rows: list[str] = field(default_factory=list)
    orphan_rows: list[str] = field(default_factory=list)
    drifted_rows: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)

    # One question a caller almost always asks; spelled once so it cannot drift.
    @property
    def has_drift(self) -> bool:
        """True when the mirror disagrees with the files in any way."""
        return bool(self.missing_rows or self.orphan_rows or self.drifted_rows)


# One aggregated bucket of the ledger, carrying its OWN basis breakdown (P6).
@dataclass
class CostRow:
    """One row of a cost report: a bucket, its figures, and how measured they are.

    ``bucket`` is the group key's value — a role, a model, a ``YYYY-MM-DD`` day —
    or None for the grand total AND for a bucket whose group column is NULL in
    the database (a call whose role the evidence never named). ``calls`` counts
    the rows in the bucket.

    EVERY FIGURE IS NULLABLE ON PURPOSE. ``SUM()`` over rows that all reported
    NULL yields NULL in SQLite, and that NULL is preserved here instead of being
    coerced to 0: an UNMEASURED figure must never look like a MEASURED ZERO.
    That is the P6 rule and the reason the ledger stores nulls at all — a
    ``COALESCE`` in the query would silently turn "we do not know" into "it cost
    nothing".

    ``measured_calls`` and ``unmeasured_calls`` are the basis breakdown: how many
    of ``calls`` carry basis ``provider_reported`` and how many carry ``unknown``.
    They are COUNTS, not measurements, so 0 is the honest empty value for them —
    the exact opposite of the rule above, which is why they are counted with
    ``COUNT`` rather than summed. Their sum can be less than ``calls`` if a row
    ever carries the ``price_table`` basis; no code in Remedy writes one.
    """

    bucket: str | None = None
    calls: int = 0
    tokens_in: int | None = None
    tokens_out: int | None = None
    cache_read: int | None = None
    cache_write: int | None = None
    cost_usd: float | None = None
    measured_calls: int = 0
    unmeasured_calls: int = 0

    # A bucket is only fully measured when every call in it reported its basis.
    @property
    def fully_measured(self) -> bool:
        """True when every call in this bucket reported a provider figure."""
        return self.calls > 0 and self.measured_calls == self.calls


# One answered cost question: the buckets, the grand total, and the provenance.
@dataclass
class CostReport:
    """The result of one ``query_cost`` call.

    ``rows`` are the buckets (empty when no grouping was asked for) and ``total``
    is the grand total over the SAME filters — it is not the sum of ``rows`` by
    definition but by construction, computed from the same WHERE clause.

    The remaining fields echo the question back so a renderer can state its own
    provenance: which ledger was read, whether that file even existed, and which
    filters produced these numbers. A report over a ledger that does not exist is
    EMPTY, not an error — and ``ledger_exists`` is how a caller tells "no ledger
    yet" apart from "a ledger with nothing in it".
    """

    rows: list[CostRow] = field(default_factory=list)
    total: CostRow = field(default_factory=CostRow)
    by: str | None = None
    since: str | None = None
    job_id: str | None = None
    project_id: str | None = None
    ledger_path: str | None = None
    ledger_exists: bool = False


# Misses are process-level and lock-guarded: several worker threads may write.
_miss_lock = threading.Lock()
_miss_count = 0


# The ledger file for one project, keyed by the REGISTRY UUID (not a repo hash).
def token_ledger_path_for(project_id: UUID | str, root: Path | None = None) -> Path:
    """Return ``<data_root>/projects/<project_id>/ledger.sqlite``.

    ``project_id`` is ``project_registry.RemyProject.id`` — the registry UUID,
    the canonical project identity. It is NOT the sha256 repo-path hash that
    ``worktrees.py`` uses for lock directories; those two must never be swapped.

    The data root is resolved through ``data_paths.projects_dir``, which is the
    single authoritative reader of the data-root configuration. This module
    never reads that environment variable itself.
    """
    return projects_dir(root) / str(project_id) / LEDGER_FILENAME


# Opens (creating if needed) a ledger and brings its schema up to SCHEMA_VERSION.
def open_ledger(path: Path | str) -> sqlite3.Connection:
    """Open the ledger at ``path``, in WAL mode, migrated to ``SCHEMA_VERSION``.

    Creates parent directories. Idempotent: opening an existing current-version
    database runs no migration step and changes no row. The caller owns the
    returned connection and must close it — ``record_call`` closes its own in a
    ``finally``.

    WAL plus short transactions is what lets a reader read while a write is in
    flight; do not hold a connection open across calls.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), timeout=BUSY_TIMEOUT_MS / 1000)
    try:
        conn.execute("PRAGMA journal_mode=WAL").fetchone()
        conn.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
        _migrate_to_current(conn)
    except BaseException:
        conn.close()
        raise
    return conn


# Records one call; returns True if the row is durable, False on ANY failure.
def record_call(
    record: CallRecord,
    *,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
) -> bool:
    """Persist ``record``. NEVER raises, and a failure NEVER fails the run.

    Returns True when the row is durable — including when the ``call_id`` was
    already present, because ``INSERT OR IGNORE`` makes re-recording a no-op and
    that already-durable row is what makes T002's backfill idempotent.

    Returns False on any failure whatsoever, after logging loudly at ERROR and
    incrementing the miss counter. A later ``remedy stats verify-ledger`` run
    reconciles the miss against the evidence files, which are the source of
    truth; nothing is lost by a miss except queryability.

    Give either ``path`` (explicit file) or ``project_id`` (resolved through
    ``token_ledger_path_for``). Giving neither is a failure like any other.
    """
    conn: sqlite3.Connection | None = None
    try:
        target = _resolve_ledger_path(project_id=project_id, path=path)
        conn = open_ledger(target)
        placeholders = ", ".join("?" for _ in _CALL_COLUMNS)
        columns = ", ".join(_CALL_COLUMNS)
        # One statement, one commit: the transaction stays as short as it can be.
        cursor = conn.execute(
            f"INSERT OR IGNORE INTO calls ({columns}) VALUES ({placeholders})",
            tuple(getattr(record, name) for name in _CALL_COLUMNS),
        )
        conn.commit()
        if cursor.rowcount == 0:
            # OR IGNORE swallows CHECK and NOT NULL rejections as quietly as it
            # swallows a duplicate key, so "no row inserted" is ambiguous and must
            # never be guessed at. Ask the table which case this is: an existing
            # row means idempotent re-record (durable, True); no row means a
            # constraint — an unknown cost_basis, a missing ts_utc — rejected the
            # write, and reporting True there would invent durability.
            landed = conn.execute(
                "SELECT 1 FROM calls WHERE call_id = ?", (record.call_id,)
            ).fetchone()
            if landed is None:
                raise sqlite3.IntegrityError(
                    f"ledger rejected call_id={record.call_id!r}: no row inserted and "
                    f"none present (cost_basis={record.cost_basis!r} must be one of "
                    f"{sorted(COST_BASES)}, ts_utc must be non-null)"
                )
        return True
    except Exception:
        _count_ledger_miss()
        logger.error(
            "token ledger write FAILED for call_id=%r (miss counted, run continues; "
            "the evidence files remain the source of truth and reconcile can heal this)",
            getattr(record, "call_id", None),
            exc_info=True,
        )
        return False
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:  # pragma: no cover - close() failing is not actionable
                logger.error("token ledger connection close failed", exc_info=True)


# The deterministic ledger identity of one finalized task run (DECISION D16).
def call_id_for_task_run(job_id: str, task_id: str) -> str:
    """Return ``"<job_id>:<task_id>"`` — the ledger identity of one task run.

    IMMUTABLE BY CONSTRUCTION: the id is a pure function of two identifiers the
    evidence tree already carries, with no clock, no counter and no random part
    in it. That is exactly what makes backfill idempotent — the same task run
    always maps to the same row, so a second pass ``INSERT OR IGNORE``s into a
    no-op instead of creating a duplicate.

    Per DECISION D16 a ROW IS ONE FINALIZED TASK RUN, not one HTTP request:
    ``task_runs/<task_id>/provider_evidence.json`` is the finest record the
    actuals feature puts on disk.

    Raises ``ValueError`` when either part is empty: an id with an empty half
    would collide across task runs and silently merge two calls into one row.
    """
    job = str(job_id or "").strip()
    task = str(task_id or "").strip()
    if not job or not task:
        raise ValueError(
            "call_id needs a non-empty job_id and task_id, got "
            f"job_id={job_id!r} task_id={task_id!r}"
        )
    return f"{job}:{task}"


# The job an evidence tree belongs to — the left half of every call_id inside it.
def job_id_for_evidence_dir(evidence_dir: Path | str) -> str:
    """Return the job id that ``evidence_dir`` belongs to.

    Prefers the tree's own ``manifest.json`` ``job_id``, which is what the job
    evidence bundle writes; falls back to the directory's own name, which is how
    the evidence tree is laid out on disk. Never invents an id — it is always
    one of those two, so the same tree always yields the same call_ids.
    """
    base = Path(evidence_dir)
    try:
        manifest = _read_evidence_object(base / _JOB_MANIFEST_FILENAME)
    except (StrictJsonError, OSError, ValueError):
        manifest = None
    if manifest:
        named = _first_string(manifest, ("job_id",))
        if named:
            return named
    return base.resolve().name


# Builds one ledger row from one on-disk task run; None when it is unrecordable.
def call_record_from_evidence(
    evidence_dir: Path | str,
    job_id: str,
    task_id: str,
) -> CallRecord | None:
    """Build the ``CallRecord`` for ``task_runs/<task_id>/`` under ``evidence_dir``.

    Reads ``provider_evidence.json`` and, where present, ``token_accounting.json``.
    The usage counters come from ``token_truth``'s own extractor — Remedy
    deliberately does NOT parse provider output a second time here, because a
    second parse is the SECOND CAPTURE PATH the feature file's Orchestrator brief
    rejects and would be free to disagree with the published evidence.

    Returns None when the task run is UNRECORDABLE: no provider evidence file,
    unreadable or non-object JSON, or a malformed counter. The extractor RAISES
    on a malformed counter rather than coercing a plausible number, and that
    refusal is honoured here — the caller counts the task run instead of storing
    a guess.

    Field provenance, all of it honest or absent:

    * ``tokens_in`` / ``tokens_out`` / ``cache_read`` / ``cache_write`` — the
      prompt, completion, cache-read and cache-creation counters. A counter the
      provider did not report stays None. NO reported usage at all yields NULL
      counts with ``cost_basis`` ``unknown`` — never a fabricated zero.
    * ``cost_usd`` — only a figure genuinely present in the evidence
      (``total_cost_usd``), and then ``cost_basis`` is ``provider_reported``.
      There is no price table here and no price is ever computed.
    * ``role`` / ``model`` — taken only where the evidence names them, left None
      otherwise. A configured model is not the model that ran, so it is not used.
    * ``ts_utc`` — the evidence's own timestamp where it carries one; OTHERWISE
      THE ``provider_evidence.json`` FILE'S MTIME rendered as a UTC ISO-8601
      string. A timestamp's provenance matters, so the fallback is stated rather
      than hidden: an mtime says when the evidence was written, not when the
      provider was called.
    * ``evidence_ref`` — ``task_runs/<task_id>``, the path relative to
      ``evidence_dir``, so a row can always be traced back to the file that is
      the source of truth.
    """
    base = Path(evidence_dir)
    task = str(task_id)
    task_dir = base / _TASK_RUNS_DIRNAME / task
    evidence_path = task_dir / _PROVIDER_EVIDENCE_FILENAME
    ctx = f"{_TASK_RUNS_DIRNAME}/{task}/{_PROVIDER_EVIDENCE_FILENAME}"
    try:
        provider_evidence = _read_evidence_object(evidence_path)
        if provider_evidence is None:
            return None
        accounting = _read_evidence_object(task_dir / _TOKEN_ACCOUNTING_FILENAME) or {}
        timestamp = (
            _first_string(provider_evidence, _TIMESTAMP_FIELDS)
            or _first_string(accounting, _TIMESTAMP_FIELDS)
            or _mtime_as_utc_iso(evidence_path)
        )
        return _call_record_from_parts(
            provider_evidence=provider_evidence,
            accounting=accounting,
            call_id=call_id_for_task_run(job_id, task),
            job_id=str(job_id),
            task_id=task,
            ts_utc=timestamp,
            evidence_ref=f"{_TASK_RUNS_DIRNAME}/{task}",
            ctx=ctx,
        )
    except (TokenEvidenceError, StrictJsonError, OSError, ValueError):
        logger.warning(
            "token ledger cannot record task run %r from %s: the evidence is "
            "unrecordable, so no row is invented for it",
            task, evidence_path, exc_info=True,
        )
        return None


# One task run's segment rows, read out of the prompt trace copied beside it.
def segment_rows_from_trace_file(
    trace_path: Path | str,
    *,
    call_id: str,
    task_id: str,
) -> list[CallSegmentRow]:
    """Read ``prompt_trace.jsonl`` into the ``call_segments`` rows of one task run.

    PURE AND READ-ONLY: it opens nothing but ``trace_path``, writes nothing and
    never brings a database into existence. NEVER RAISES for any input either —
    an absent or unreadable file yields ``[]``, and a line that is not valid
    JSON is skipped while the scan continues, because one corrupt line must not
    cost every other segment its row.

    ``task_id`` is LOAD-BEARING, not defensive: the trace copied beside the
    evidence is the WHOLE JOB's file — ``prompt_trace.append_trace_jsonl`` keeps
    one per job, not one per task run — so the other task runs' entries sit in
    it and would otherwise be attributed to this ``call_id``.

    ``trace_seq`` is the zero-based index AMONG THE KEPT entries, assigned in
    file order. An entry whose ``segment_manifest`` is empty produces no row but
    STILL CONSUMES its index: the number means "position among this task run's
    provider calls", so it stays stable once a later round makes more of those
    calls carry a manifest. A blank line is not an entry and consumes nothing.

    A manifest dict missing any of ``_MANIFEST_KEYS`` is SKIPPED rather than
    defaulted — a figure nobody published must not land as a measured zero (P6).
    """
    source = Path(trace_path)
    rows: list[CallSegmentRow] = []
    try:
        raw = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        # No trace beside the evidence is the NORMAL pre-F115 case, not a fault.
        return rows
    wanted = str(task_id)
    trace_seq = 0
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            entry = strict_loads(line, where=str(source), require_object=True)
        except StrictJsonError:
            logger.warning(
                "token ledger skips an unreadable prompt-trace line in %s; the "
                "scan continues so one corrupt line costs no other row",
                source, exc_info=True,
            )
            continue
        if entry.get("task_id") != wanted:
            continue
        manifest = entry.get("segment_manifest")
        if isinstance(manifest, list):
            for item in manifest:
                row = _call_segment_row(item, call_id=call_id, trace_seq=trace_seq)
                if row is not None:
                    rows.append(row)
        trace_seq += 1
    return rows


# Records one task run's segment rows; a failure is a counted miss, never a raise.
def record_call_segments(
    rows: list[CallSegmentRow],
    *,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
) -> bool:
    """Persist ``rows`` into ``call_segments``. NEVER raises; failure is a miss.

    ``record_call``'s discipline, applied to the segment table: one statement,
    one commit, the connection closed in a ``finally``, and a failure that logs
    at ERROR, counts a ledger miss and returns False without ever failing the
    run. The evidence files remain the source of truth, so a lost segment row is
    a reconcilable defect rather than lost data.

    IDEMPOTENT BY THE TABLE'S OWN PRIMARY KEY (``call_id``, ``trace_seq``,
    ``segment_name``): ``INSERT OR IGNORE`` turns a repeat pass into a no-op
    that still reports the rows as durable, which is what makes a second
    ``backfill_ledger`` over unchanged evidence add nothing here either.

    An EMPTY ``rows`` returns True WITHOUT opening the ledger: a task run whose
    trace carries no manifest must not be the thing that creates a database.

    Give either ``path`` (explicit file) or ``project_id``, exactly as
    ``record_call`` does; giving neither is a failure like any other.
    """
    if not rows:
        return True
    conn: sqlite3.Connection | None = None
    try:
        target = _resolve_ledger_path(project_id=project_id, path=path)
        conn = open_ledger(target)
        placeholders = ", ".join("?" for _ in _CALL_SEGMENT_COLUMNS)
        columns = ", ".join(_CALL_SEGMENT_COLUMNS)
        conn.executemany(
            f"INSERT OR IGNORE INTO call_segments ({columns}) VALUES ({placeholders})",
            [
                tuple(getattr(row, name) for name in _CALL_SEGMENT_COLUMNS)
                for row in rows
            ],
        )
        conn.commit()
        return True
    except Exception:
        _count_ledger_miss()
        logger.error(
            "token ledger segment write FAILED for call_id=%r (%d row(s); miss "
            "counted, run continues; the evidence files remain the source of "
            "truth and a later backfill can heal this)",
            getattr(rows[0], "call_id", None), len(rows),
            exc_info=True,
        )
        return False
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:  # pragma: no cover - close() failing is not actionable
                logger.error("token ledger connection close failed", exc_info=True)


# Mirrors a whole evidence tree into rows; idempotent, and never raises.
def backfill_ledger(
    evidence_dir: Path | str,
    *,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
) -> BackfillResult:
    """Record every task run under ``evidence_dir`` into the ledger.

    IDEMPOTENT BY CONSTRUCTION: ``call_id_for_task_run`` recovers the same
    ``call_id`` for the same task run on every pass, and ``record_call``'s
    ``INSERT OR IGNORE`` turns a repeat into a no-op that still reports the row
    as durable. A second run over unchanged evidence therefore reports the same
    ``recorded`` total and leaves the ROW COUNT unchanged — the feature file's
    "rerunning backfill adds nothing".

    NEVER RAISES on a malformed task run: it is counted in ``failed`` and the
    scan continues, because one unreadable file must not cost every other row.
    The evidence files remain the source of truth; this only builds the mirror.

    Give either ``path`` (explicit file) or ``project_id``, exactly as
    ``record_call`` does; giving neither makes every write a counted miss.
    """
    base = Path(evidence_dir)
    result = BackfillResult()
    job_id = job_id_for_evidence_dir(base)
    for task_dir in _task_run_dirs(base):
        result.scanned += 1
        try:
            if not (task_dir / _PROVIDER_EVIDENCE_FILENAME).is_file():
                # Nothing on disk to mirror: not an error, just not a call.
                result.skipped += 1
                continue
            record = call_record_from_evidence(base, job_id, task_dir.name)
            if record is None:
                result.failed += 1
                continue
            if record_call(record, project_id=project_id, path=path):
                result.recorded += 1
                # BACKFILL IS THE ONLY WIRED PATH, deliberately: the live hook
                # at the actuals seam fires BEFORE the exporter copies
                # prompt_trace.jsonl into the task-run directory
                # (``pingpong_evidence.py:517-525`` vs ``:527-536``), so this is
                # the only place the file demonstrably exists. NO BackfillResult
                # COUNTER MOVES either way — the return value is deliberately
                # not branched on, because a segment read or write that fails is
                # a counted ledger miss and nothing else, and `calls` mirroring
                # must stay exactly as measurable as it was before F115.
                record_call_segments(
                    segment_rows_from_trace_file(
                        task_dir / _PROMPT_TRACE_FILENAME,
                        call_id=record.call_id,
                        task_id=task_dir.name,
                    ),
                    project_id=project_id,
                    path=path,
                )
            else:
                result.failed += 1
        except Exception:  # pragma: no cover - defence in depth; nothing below raises
            result.failed += 1
            logger.error(
                "token ledger backfill failed for task run %r (counted in failed, "
                "the scan continues)",
                task_dir.name, exc_info=True,
            )
    return result


# Read-only drift report: what the files say versus what the rows say.
def verify_ledger(
    evidence_dir: Path | str,
    *,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
) -> ReconcileResult:
    """Compare the evidence files against the ledger rows and report DRIFT.

    THE FILES ARE THE SOURCE OF TRUTH AND THE DATABASE IS THE MIRROR, so every
    disagreement found here means THE DB IS WRONG — never that the files are.
    Nothing is corrected: this reports, and ``backfill_ledger`` re-records.

    READ-ONLY BY CONSTRUCTION: when the ledger file does not exist it is not
    opened, so verifying never CREATES a database; when it does exist only
    ``SELECT``s run against it. The row count is identical before and after.

    R-0219 is resolved here by CONTENT COMPARISON rather than presence: each row
    is compared field by field against the record re-derived from its own
    evidence, so a row that drifted AFTER it was written is visible instead of
    passing as "a row is there". It has to be reported rather than silently
    re-recorded, because ``INSERT OR IGNORE`` cannot overwrite an existing row.

    Orphan detection is scoped to THIS job's rows, because one project ledger
    legitimately holds many jobs and another job's rows are not orphans of this
    evidence tree.

    Raises ``ValueError`` when neither ``project_id`` nor ``path`` is given —
    there is no ledger to compare against and reporting universal drift would be
    a lie about the mirror rather than a fact about it.
    """
    base = Path(evidence_dir)
    result = ReconcileResult()
    job_id = job_id_for_evidence_dir(base)
    target = _resolve_ledger_path(project_id=project_id, path=path)

    on_disk: dict[str, CallRecord] = {}
    for task_dir in _task_run_dirs(base):
        if not (task_dir / _PROVIDER_EVIDENCE_FILENAME).is_file():
            continue
        result.checked += 1
        record = call_record_from_evidence(base, job_id, task_dir.name)
        if record is None:
            result.unreadable.append(call_id_for_task_run(job_id, task_dir.name))
            continue
        on_disk[record.call_id] = record

    stored: dict[str, CallRecord] = {}
    if target.exists():
        conn = open_ledger(target)
        try:
            columns = ", ".join(_CALL_COLUMNS)
            for row in conn.execute(
                f"SELECT {columns} FROM calls WHERE job_id = ?", (job_id,)
            ):
                stored[row[0]] = CallRecord(**dict(zip(_CALL_COLUMNS, row)))
        finally:
            conn.close()

    for call_id, expected in sorted(on_disk.items()):
        found = stored.get(call_id)
        if found is None:
            result.missing_rows.append(call_id)
        elif found != expected:
            result.drifted_rows.append(call_id)

    unreadable = set(result.unreadable)
    result.orphan_rows.extend(
        sorted(cid for cid in stored if cid not in on_disk and cid not in unreadable)
    )
    return result


# The aggregation the ledger exists for: what did this cost, grouped and honest.
def query_cost(
    *,
    project_id: UUID | str | None = None,
    path: Path | str | None = None,
    since: str | None = None,
    job_id: str | None = None,
    by: str | None = None,
) -> CostReport:
    """Aggregate the ledger into a ``CostReport``. READ-ONLY, and never raises on absence.

    ``by`` is one of None (grand total only), ``"role"``, ``"model"`` or
    ``"day"``; anything else is a ``ValueError``, because silently answering a
    different question than the one asked is worse than refusing.

    ``since`` filters ``ts_utc`` with a LEXICOGRAPHIC ``>=``. That is correct
    rather than sloppy: ISO-8601 UTC timestamps sort identically as text and as
    time — the fields run most-significant first and are zero-padded — and it is
    exactly why ``ts_utc`` is stored as TEXT instead of an epoch number. The
    comparison is only sound between timestamps written in the same ISO-8601 UTC
    shape, which is the only shape this module ever writes.

    ``job_id`` filters to one job. ``"day"`` buckets by the first 10 characters
    of ``ts_utc``, i.e. its calendar day in UTC.

    NULLS ARE PRESERVED. A bucket in which NO row reported tokens has
    ``tokens_in=None``, never 0, and the same holds for ``cost_usd``: ``SUM()``
    over all-NULL is NULL in SQLite and nothing here coerces it away. An
    unmeasured figure must not be renderable as a measured zero (P6). NO PRICE IS
    EVER COMPUTED — a cost figure appears only where a provider reported one.

    A ledger file that does not exist yields an EMPTY report: not an error, and
    NOT a created database. Asking what a project cost must never be the thing
    that brings its ledger into being.
    """
    if by is not None and by not in COST_GROUP_KEYS:
        raise ValueError(
            f"query_cost(by={by!r}) is not a group key; use one of "
            f"{list(COST_GROUP_KEYS)} or None for the grand total"
        )
    target = _resolve_ledger_path(project_id=project_id, path=path)
    report = CostReport(
        by=by,
        since=since,
        job_id=job_id,
        project_id=None if project_id is None else str(project_id),
        ledger_path=str(target),
        ledger_exists=target.is_file(),
    )
    if not report.ledger_exists:
        return report

    where, where_params = _cost_filters(since=since, job_id=job_id)
    conn = _connect_readonly(target)
    try:
        report.total = _cost_bucket_rows(conn, where, where_params, group_expr=None)[0]
        if by is not None:
            report.rows = _cost_bucket_rows(
                conn, where, where_params, group_expr=_COST_GROUP_EXPRESSIONS[by]
            )
    finally:
        conn.close()
    return report


# Folds several project reports into one, which is what ``--all-projects`` is.
def merge_cost_reports(reports: list[CostReport]) -> CostReport:
    """Combine per-project reports into one, keeping every NULL a NULL.

    Buckets with the same key are added together; a figure that was unmeasured in
    EVERY report stays None, while a figure measured anywhere becomes the sum of
    the reports that measured it — the honest reading, since the unmeasured
    reports contribute nothing known rather than a known zero.

    The merged report echoes back only what all its inputs agree on: the filters
    and the grouping. ``project_id`` and ``ledger_path`` are cleared, because a
    cross-project total belongs to no single project or file, and
    ``ledger_exists`` is True when at least one ledger was actually read.
    """
    merged = CostReport(
        by=reports[0].by if reports else None,
        since=reports[0].since if reports else None,
        job_id=reports[0].job_id if reports else None,
        ledger_exists=any(r.ledger_exists for r in reports),
    )
    merged.total = _combine_cost_rows([r.total for r in reports], bucket=None)
    buckets: dict[str | None, list[CostRow]] = {}
    for report in reports:
        for row in report.rows:
            buckets.setdefault(row.bucket, []).append(row)
    ordered = sorted(buckets.items(), key=lambda item: (item[0] is not None, item[0] or ""))
    merged.rows = [_combine_cost_rows(rows, bucket=bucket) for bucket, rows in ordered]
    return merged


# How many ledger writes have failed in this process — surfaced by verify-ledger.
def ledger_miss_count() -> int:
    """Return the number of failed ledger writes since the last reset."""
    with _miss_lock:
        return _miss_count


# Zeroes the miss counter; used by tests and by a future verify-ledger run.
def reset_ledger_miss_count() -> None:
    """Reset the process-level miss counter to zero."""
    global _miss_count
    with _miss_lock:
        _miss_count = 0


def _resolve_ledger_path(
    *,
    project_id: UUID | str | None,
    path: Path | str | None,
) -> Path:
    """The ledger file to use: an explicit ``path`` wins, else the project's own.

    One spelling of the rule, shared by every entry point, so a caller can never
    get a different answer from the writer than from the reconciler.
    """
    if path is not None:
        return Path(path)
    if project_id is not None:
        return token_ledger_path_for(project_id)
    raise ValueError("a ledger target needs either project_id or path")


def _connect_readonly(path: Path) -> sqlite3.Connection:
    """Open ``path`` for querying only: it cannot be created and cannot be written.

    Deliberately NOT ``open_ledger``: a query must never create a database and
    must never MIGRATE one. ``remedy stats cost --all-projects`` reads other
    projects' ledgers, and a read that quietly upgraded another project's schema
    would be a write wearing a query's name. Two mechanisms, neither of them a
    promise: ``mode=rw`` refuses to bring a missing file into existence, and
    ``PRAGMA query_only=1`` makes SQLite itself reject every INSERT, UPDATE and
    DDL statement on the handle.

    Remedy deliberately does NOT use ``mode=ro`` here even though it sounds
    stricter. A ``mode=ro`` handle cannot checkpoint the write-ahead log when it
    closes, so merely READING a WAL database would leave ``-wal`` and ``-shm``
    files sitting next to it forever. A read that litters the data root is not
    the read-only this feature promised.
    """
    uri = f"{path.resolve().as_uri()}?mode=rw"
    conn = sqlite3.connect(uri, uri=True, timeout=BUSY_TIMEOUT_MS / 1000)
    try:
        conn.execute("PRAGMA query_only=1")
        conn.execute(f"PRAGMA busy_timeout={BUSY_TIMEOUT_MS}")
    except BaseException:
        conn.close()
        raise
    return conn


def _cost_filters(*, since: str | None, job_id: str | None) -> tuple[str, list[Any]]:
    """The shared WHERE clause, so the buckets and the grand total cannot diverge."""
    clauses: list[str] = []
    params: list[Any] = []
    if since:
        clauses.append("ts_utc >= ?")
        params.append(since)
    if job_id:
        clauses.append("job_id = ?")
        params.append(job_id)
    return (" WHERE " + " AND ".join(clauses)) if clauses else "", params


def _cost_bucket_rows(
    conn: sqlite3.Connection,
    where: str,
    where_params: list[Any],
    *,
    group_expr: str | None,
) -> list[CostRow]:
    """Run one aggregation and map it onto ``CostRow``s, NULLS INTACT.

    The measurement columns are ``SUM``med, so an all-NULL bucket stays NULL. The
    two basis columns are ``COUNT``ed instead, because ``COUNT`` never returns
    NULL and "zero calls reported a basis" is a fact rather than a gap — a count
    of nothing IS 0, while a sum of nothing is not.

    ``group_expr`` is a literal from ``_COST_GROUP_EXPRESSIONS``, never caller
    input; ``since`` and ``job_id`` reach the statement as bound parameters.
    """
    bucket_expr = group_expr or "NULL"
    sql = (
        f"SELECT {bucket_expr} AS bucket, COUNT(*), "
        "SUM(tokens_in), SUM(tokens_out), SUM(cache_read), SUM(cache_write), "
        "SUM(cost_usd), "
        "COUNT(CASE WHEN cost_basis = ? THEN 1 END), "
        "COUNT(CASE WHEN cost_basis = ? THEN 1 END) "
        f"FROM calls{where}"
    )
    params = [COST_BASIS_PROVIDER_REPORTED, COST_BASIS_UNKNOWN, *where_params]
    if group_expr is not None:
        sql += " GROUP BY bucket ORDER BY bucket"
    rows = conn.execute(sql, params).fetchall()
    return [
        CostRow(
            bucket=None if row[0] is None else str(row[0]),
            calls=int(row[1]),
            tokens_in=row[2],
            tokens_out=row[3],
            cache_read=row[4],
            cache_write=row[5],
            cost_usd=row[6],
            measured_calls=int(row[7]),
            unmeasured_calls=int(row[8]),
        )
        for row in rows
    ]


def _add_optional(left: int | float | None, right: int | float | None) -> int | float | None:
    """Add two possibly-unmeasured figures; None only when BOTH are unmeasured.

    ``None`` here means "nobody reported this", not "zero". Adding it as 0 would
    manufacture a measurement; dropping the whole sum because one side is unknown
    would discard a real one. Keeping the known part and staying None only when
    nothing is known is the sole answer that invents nothing.
    """
    if left is None:
        return right
    if right is None:
        return left
    return left + right


def _combine_cost_rows(rows: list[CostRow], *, bucket: str | None) -> CostRow:
    """Fold several buckets with the same key into one, preserving unmeasuredness."""
    combined = CostRow(bucket=bucket)
    for row in rows:
        combined.calls += row.calls
        combined.measured_calls += row.measured_calls
        combined.unmeasured_calls += row.unmeasured_calls
        combined.tokens_in = _add_optional(combined.tokens_in, row.tokens_in)
        combined.tokens_out = _add_optional(combined.tokens_out, row.tokens_out)
        combined.cache_read = _add_optional(combined.cache_read, row.cache_read)
        combined.cache_write = _add_optional(combined.cache_write, row.cache_write)
        combined.cost_usd = _add_optional(combined.cost_usd, row.cost_usd)
    return combined


def _read_evidence_object(path: Path) -> dict[str, Any] | None:
    """Return the JSON object at ``path``; None when absent; raise when malformed.

    Uses the repository's strict decoder, so a duplicate key or a non-object root
    is a refusal rather than a silently-kept last value.
    """
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return None
    return strict_loads(raw, where=str(path), require_object=True)


def _first_string(container: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    """The first key in ``keys`` holding a non-blank string, or None."""
    for key in keys:
        value = container.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _mtime_as_utc_iso(path: Path) -> str:
    """``path``'s modification time as a UTC ISO-8601 string.

    The LAST-RESORT timestamp for a row: it says when the evidence was written,
    not when the provider was called, which is why every caller documents it.
    """
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def _call_record_from_parts(
    *,
    provider_evidence: dict[str, Any],
    accounting: dict[str, Any],
    call_id: str,
    job_id: str,
    task_id: str,
    ts_utc: str,
    evidence_ref: str,
    ctx: str,
) -> CallRecord:
    """Map already-loaded evidence onto one ``CallRecord``.

    The ONE mapping from evidence to row, shared by the backfill path and by the
    call site at the seam where actuals are finalized. Sharing it is what lets
    ``verify_ledger`` compare content at all: two producers of the same row must
    not be free to disagree about what that row is.

    Raises ``TokenEvidenceError`` when a counter or the cost figure is
    malformed — the caller decides what to do with an unrecordable task run.
    """
    actual = _extract_actual(provider_evidence, ctx) or {}
    cost_usd = _strict_cost(provider_evidence, "total_cost_usd", ctx)
    model = None
    if provider_evidence.get("actual_model_verified") is True:
        model = _first_string(provider_evidence, _VERIFIED_MODEL_FIELDS)
    if model is None:
        model = _first_string(provider_evidence, _NAMED_MODEL_FIELDS)
    return CallRecord(
        call_id=call_id,
        job_id=job_id,
        task_id=task_id,
        role=_first_string(accounting, ("role",)),
        model=model,
        ts_utc=ts_utc,
        tokens_in=actual.get("actual_prompt_tokens"),
        tokens_out=actual.get("actual_completion_tokens"),
        cache_read=actual.get("actual_cache_read_tokens"),
        cache_write=actual.get("actual_cache_creation_tokens"),
        cost_usd=cost_usd,
        # The basis describes the COST, so it is provider_reported only when a
        # real provider figure is present; otherwise unknown, never a price.
        cost_basis=(
            COST_BASIS_PROVIDER_REPORTED if cost_usd is not None else COST_BASIS_UNKNOWN
        ),
        evidence_ref=evidence_ref,
    )


def _call_segment_row(
    manifest_entry: Any,
    *,
    call_id: str,
    trace_seq: int,
) -> CallSegmentRow | None:
    """One manifest dict as a row, or None when it does not carry all five keys.

    A dict missing a key is SKIPPED rather than completed with 0 or "": the
    values are taken verbatim from ``_MANIFEST_KEYS`` and nothing here invents,
    coerces or defaults one. An unpublished figure must never become a measured
    zero (P6), and a partial manifest row would be exactly that.
    """
    if not isinstance(manifest_entry, dict):
        return None
    if any(key not in manifest_entry for key in _MANIFEST_KEYS):
        return None
    name, rank, sha256, chars, tokens_estimated = (
        manifest_entry[key] for key in _MANIFEST_KEYS
    )
    return CallSegmentRow(
        call_id=call_id,
        trace_seq=trace_seq,
        segment_name=name,
        segment_rank=rank,
        segment_sha256=sha256,
        chars=chars,
        tokens_estimated=tokens_estimated,
    )


def _task_run_dirs(evidence_dir: Path) -> list[Path]:
    """Every ``task_runs/<task_id>/`` directory under ``evidence_dir``, name-sorted.

    Sorted so two passes visit the same task runs in the same order and produce
    the same counts; an evidence tree with no ``task_runs`` yields nothing.
    """
    runs = evidence_dir / _TASK_RUNS_DIRNAME
    if not runs.is_dir():
        return []
    return sorted((child for child in runs.iterdir() if child.is_dir()),
                  key=lambda child: child.name)


def _count_ledger_miss() -> None:
    """Increment the miss counter under its lock."""
    global _miss_count
    with _miss_lock:
        _miss_count += 1


def _read_schema_version(conn: sqlite3.Connection) -> int:
    """Return the stored schema version, or 0 when the ledger is brand new."""
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='meta'"
    ).fetchone()
    if row is None:
        return 0
    row = conn.execute(
        "SELECT value FROM meta WHERE key = ?", (SCHEMA_VERSION_KEY,)
    ).fetchone()
    if row is None:
        return 0
    try:
        return int(row[0])
    except (TypeError, ValueError):
        return 0


def _migrate_to_current(conn: sqlite3.Connection) -> None:
    """Apply every migration step above the stored version, in numeric order.

    Each version's steps plus its meta bump commit together, so a ledger is
    never left claiming a version it does not have. An already-current database
    executes nothing at all.
    """
    current = _read_schema_version(conn)
    for version in sorted(_MIGRATIONS):
        if version <= current:
            continue
        for statement in _MIGRATIONS[version]:
            conn.execute(statement)
        conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)",
            (SCHEMA_VERSION_KEY, str(version)),
        )
        conn.commit()
