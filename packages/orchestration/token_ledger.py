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
  response itself. As of T001 it has NO call site at all — wiring
  ``record_call`` into the seam where actuals are finalized is T002's first
  item, and until then this module is intentionally inert.
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
    CallRecord
    token_ledger_path_for(project_id, root=None) -> Path
    open_ledger(path) -> sqlite3.Connection
    record_call(record, *, project_id=None, path=None) -> bool
    ledger_miss_count() -> int
    reset_ledger_miss_count() -> None
"""

from __future__ import annotations

import logging
import sqlite3
import threading
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from packages.orchestration.data_paths import projects_dir

logger = logging.getLogger(__name__)


# The on-disk schema generation; bump it only together with a new migration step.
SCHEMA_VERSION = 1

# The meta key carrying SCHEMA_VERSION, so a future reader can tell old DBs apart.
SCHEMA_VERSION_KEY = "schema_version"

# One ledger file per project; the name is fixed so tooling can find it by path.
LEDGER_FILENAME = "ledger.sqlite"

# How long a writer waits for another writer's lock before giving up (ms).
BUSY_TIMEOUT_MS = 5000

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
        if path is not None:
            target = Path(path)
        elif project_id is not None:
            target = token_ledger_path_for(project_id)
        else:
            raise ValueError("record_call needs either project_id or path")

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
