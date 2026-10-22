"""F113 T003a — the side-role calls a task run made, as evidence and in the cost ledger, with their basis.

A summary written by a side role mapped to a local endpoint records its route beside its text
(`packages/orchestration/side_role_routing.py`). A task run's summaries are cached in its run
directory under `calls/<role>/round-<nn>/`; a job's evidence export reads every one that carries a
route, writes one row per summary as `side_role_calls.json` beside the task's other evidence, and the
cost ledger mirrors that file into its own table, `side_role_calls`, in the project's `ledger.sqlite`.
The file is written first and read back, so the database restates the file (DECISION F113 D2).

The basis of a local call is `local_zero`: no API tokens were bought. Remedy deliberately does not
record a token count for it: the endpoint's client hands back only the text, so the count is
unmeasured and the row says so with NULL, never with a zero that would sum. The ledger table is
created by this module, with its own schema key in the ledger's `meta` table, because
`packages/orchestration/token_ledger.py` is held at its row of the structure ledger and its `calls`
table admits no `local_zero`.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from packages.orchestration.side_role_routing import COST_BASIS_LOCAL_ZERO
from packages.orchestration.token_ledger import COST_BASIS_UNKNOWN

logger = logging.getLogger(__name__)

#: The evidence file one task run's rows are written to, beside its other task-run evidence.
SIDE_ROLE_CALLS_FILENAME = "side_role_calls.json"

#: The ledger table and the `meta` key carrying its schema generation.
SIDE_ROLE_CALLS_TABLE = "side_role_calls"
SIDE_ROLE_CALLS_SCHEMA_KEY = "side_role_calls_schema_version"
SIDE_ROLE_CALLS_SCHEMA_VERSION = 1

#: Where a run's summaries are cached, relative to its run directory.
_SUMMARY_GLOB = "calls/*/round-*/*.summary.json"

_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {SIDE_ROLE_CALLS_TABLE} (
    job_id        TEXT NOT NULL,
    task_id       TEXT NOT NULL,
    run_id        TEXT NOT NULL,
    call_ref      TEXT NOT NULL,
    role          TEXT NOT NULL,
    route         TEXT NOT NULL,
    endpoint      TEXT NOT NULL,
    routed_model  TEXT NOT NULL,
    reason        TEXT NOT NULL,
    tokens_out    INTEGER,
    cost_basis    TEXT NOT NULL CHECK (cost_basis IN ('{COST_BASIS_LOCAL_ZERO}', '{COST_BASIS_UNKNOWN}')),
    PRIMARY KEY (job_id, task_id, run_id, call_ref)
)
"""


@dataclass(frozen=True)
class SideRoleCallRow:
    """One side-role call of one task run: where it went, why, and its cost basis.

    `tokens_out` is None when the call's client reported no count: unmeasured, never zero.
    """

    job_id: str
    task_id: str
    run_id: str
    call_ref: str
    role: str
    route: str
    endpoint: str
    routed_model: str
    reason: str
    tokens_out: int | None
    cost_basis: str


def side_role_call_rows(run_path: Path, *, job_id: str, task_id: str, run_id: str) -> list[SideRoleCallRow]:
    """The rows of the routed summaries cached under `run_path`, by their path; a summary without a route has none."""
    from packages.orchestration.artifact_summary import ArtifactSummary

    rows = []
    for path in sorted(Path(run_path).glob(_SUMMARY_GLOB)):
        try:
            route = ArtifactSummary.model_validate_json(path.read_text(encoding="utf-8")).route
        except (OSError, UnicodeDecodeError, ValidationError):
            logger.warning("side-role call record skipped: %s does not read as a summary", path)
            continue
        if not route:
            continue
        rows.append(SideRoleCallRow(
            job_id=job_id, task_id=task_id, run_id=run_id, call_ref=path.relative_to(run_path).as_posix(),
            role=route.get("role", ""), route=route.get("route", ""), endpoint=route.get("endpoint", ""),
            routed_model=route.get("routed_model", ""), reason=route.get("reason", ""), tokens_out=None,
            cost_basis=route.get("cost_basis", COST_BASIS_UNKNOWN)))
    return rows


def write_task_side_role_calls(run_data: dict[str, Any], task: Any, task_out: Path, task_rel: str,
                               ledger_project_id: str | None, job_id: str | None) -> dict[str, str]:
    """Write one task run's `side_role_calls.json` and mirror it; answer the written files by relative name.

    Writes nothing for a run whose summaries carry no route. The mirror, armed only by a ledger
    target, never fails the export: the file is the record.
    """
    from packages.orchestration.data_paths import run_dir

    run_id = str(run_data.get("run_id") or "")
    if not run_id:
        return {}
    rows = side_role_call_rows(run_dir(run_id), job_id=str(job_id or ""), task_id=str(task.task_id), run_id=run_id)
    if not rows:
        return {}
    target = Path(task_out) / SIDE_ROLE_CALLS_FILENAME
    target.write_text(json.dumps({"rows": [asdict(row) for row in rows]}, indent=2) + "\n", encoding="utf-8")
    if ledger_project_id is not None and job_id:
        try:
            record_side_role_calls(rows_from_evidence_file(target), project_id=ledger_project_id)
        # The ledger's own errors, a file that will not read back, and a row the table refuses.
        except (sqlite3.Error, OSError, ValueError, TypeError):
            logger.error("side-role call mirror FAILED for task %r; the evidence file is unaffected",
                         task.task_id, exc_info=True)
    return {f"{task_rel}/{SIDE_ROLE_CALLS_FILENAME}": str(target)}


def rows_from_evidence_file(path: Path) -> list[SideRoleCallRow]:
    """The rows a `side_role_calls.json` holds, read back as the mirror records them."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [SideRoleCallRow(**row) for row in data.get("rows") or []]


def _open(project_id: str | None, path: Path | str | None) -> Any:
    from packages.orchestration.token_ledger import open_ledger, token_ledger_path_for

    conn = open_ledger(path if path is not None else token_ledger_path_for(str(project_id)))
    with conn:
        conn.execute(_CREATE_TABLE)
        conn.execute("INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)",
                     (SIDE_ROLE_CALLS_SCHEMA_KEY, str(SIDE_ROLE_CALLS_SCHEMA_VERSION)))
    return conn


def record_side_role_calls(rows: list[SideRoleCallRow], *, project_id: str | None = None,
                           path: Path | str | None = None) -> int:
    """Mirror `rows` into the ledger's `side_role_calls` table; a re-export replaces its own rows."""
    conn = _open(project_id, path)
    try:
        with conn:
            conn.executemany(
                f"INSERT OR REPLACE INTO {SIDE_ROLE_CALLS_TABLE} VALUES "
                "(:job_id, :task_id, :run_id, :call_ref, :role, :route, :endpoint, :routed_model, :reason, "
                ":tokens_out, :cost_basis)",
                [asdict(row) for row in rows])
    finally:
        conn.close()
    return len(rows)


@dataclass(frozen=True)
class SideRoleCallSummary:
    """One side role on one route with one basis, over every call the ledger holds."""

    role: str
    route: str
    cost_basis: str
    calls: int


def query_side_role_calls(*, project_id: str | None = None, path: Path | str | None = None) -> list[SideRoleCallSummary]:
    """One summary per role, route and basis, sorted by all three."""
    conn = _open(project_id, path)
    try:
        found = conn.execute(
            f"SELECT role, route, cost_basis, COUNT(*) FROM {SIDE_ROLE_CALLS_TABLE} "
            "GROUP BY role, route, cost_basis ORDER BY role, route, cost_basis").fetchall()
    finally:
        conn.close()
    return [SideRoleCallSummary(role=row[0], route=row[1], cost_basis=row[2], calls=row[3]) for row in found]
