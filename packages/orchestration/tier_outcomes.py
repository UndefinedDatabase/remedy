"""F296 T002b — what each model tier did for a task: its outcome, its rounds, its retries, its cost.

A run whose builder and reviewer both run on configured tier models carries `tier_ladder` in its
record (`packages/orchestration/tier_escalation.py`): the tiers it started on and every escalation
it took. A job's evidence export turns that, with the run's rounds and its per-call evidence, into
one row per tier the task's builder ran on — the task's class, the tier and the reviewer's tier, the
rounds that tier served, the retries among their calls, their cost, and the outcome: `escalated`
with the trigger that moved it up, or the run's final status for the tier that ended it — and writes
the rows as `tier_outcomes.json` beside the task's other evidence (DECISION F296 D4).

The cost ledger mirrors that file into its own table, `tier_outcomes`, in the project's
`ledger.sqlite`, the same way the ledger mirrors a task's calls: the file is written first and the
rows are read back from it, so the database restates the file and never decides anything. F133
reads `query_tier_outcomes`, one summary per task class and tier.

Remedy deliberately does not invent a cost: a tier whose calls did not all report one has no cost
and the basis `unknown`. It does not write a row for a run whose tiers are not known, and its
ledger table is created by this module, with its own schema key in the ledger's `meta` table,
because `packages/orchestration/token_ledger.py` is held at its row of the structure ledger.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: The evidence file one task run's rows are written to, beside its other task-run evidence.
TIER_OUTCOMES_FILENAME = "tier_outcomes.json"

#: The outcome of a tier the task moved up from; the tier that ended the run takes the run's status.
OUTCOME_ESCALATED = "escalated"

#: The ledger table and the `meta` key carrying its schema generation.
TIER_OUTCOMES_TABLE = "tier_outcomes"
TIER_OUTCOMES_SCHEMA_KEY = "tier_outcomes_schema_version"
TIER_OUTCOMES_SCHEMA_VERSION = 1

_CREATE_TABLE = f"""
CREATE TABLE IF NOT EXISTS {TIER_OUTCOMES_TABLE} (
    job_id         TEXT NOT NULL,
    task_id        TEXT NOT NULL,
    run_id         TEXT NOT NULL,
    first_round    INTEGER NOT NULL,
    task_class     TEXT NOT NULL,
    tier           TEXT NOT NULL,
    reviewer_tier  TEXT NOT NULL,
    last_round     INTEGER NOT NULL,
    rounds         INTEGER NOT NULL,
    retries        INTEGER NOT NULL,
    outcome        TEXT NOT NULL,
    reason         TEXT NOT NULL,
    cost_usd       REAL,
    cost_basis     TEXT NOT NULL,
    PRIMARY KEY (job_id, task_id, run_id, first_round)
)
"""


@dataclass(frozen=True)
class TierOutcomeRow:
    """What one tier did for one task run."""

    job_id: str
    task_id: str
    run_id: str
    first_round: int
    task_class: str
    tier: str
    reviewer_tier: str
    last_round: int
    rounds: int
    retries: int
    outcome: str
    reason: str
    cost_usd: float | None
    cost_basis: str


def _segments(ladder: dict[str, Any], total_rounds: int) -> list[tuple[int, int, str, str, str, str]]:
    """(first round, last round, tier, reviewer tier, outcome, reason) for each tier the builder ran on."""
    starts = [(1, str(ladder["builder_tier"]), str(ladder["reviewer_tier"]))]
    escalations = sorted(ladder.get("escalations") or [], key=lambda e: int(e["round"]))
    starts += [(int(e["round"]), str(e["builder_to"]), str(e["reviewer_to"])) for e in escalations]
    reasons = [str(e["reason"]) for e in escalations]
    segments = []
    for i, (first, tier, reviewer_tier) in enumerate(starts):
        moved = i + 1 < len(starts)
        last = starts[i + 1][0] - 1 if moved else max(total_rounds, first)
        outcome, reason = (OUTCOME_ESCALATED, reasons[i]) if moved else ("", "")
        segments.append((first, last, tier, reviewer_tier, outcome, reason))
    return segments


def tier_outcome_rows(run_data: dict[str, Any], *, job_id: str, task_id: str, task_class: str) -> list[TierOutcomeRow]:
    """The rows of one persisted run, or none when its record carries no `tier_ladder`."""
    ladder = run_data.get("tier_ladder")
    if not isinstance(ladder, dict) or not ladder.get("builder_tier") or not ladder.get("reviewer_tier"):
        return []
    total = int(run_data.get("total_rounds") or len(run_data.get("rounds") or []))
    attempts = (run_data.get("provider_evidence") or {}).get("provider_attempts") or []
    rows = []
    for first, last, tier, reviewer_tier, outcome, reason in _segments(ladder, total):
        served = [a for a in attempts if first <= int(a.get("round") or 0) <= last]
        costs = [a.get("total_cost_usd") for a in served]
        priced = bool(served) and all(isinstance(c, (int, float)) and not isinstance(c, bool) for c in costs)
        rows.append(TierOutcomeRow(
            job_id=job_id, task_id=task_id, run_id=str(run_data.get("run_id") or ""), first_round=first,
            task_class=task_class, tier=tier, reviewer_tier=reviewer_tier, last_round=last,
            rounds=max(0, min(last, total) - first + 1),
            retries=sum(1 for a in served if a.get("is_retry") or a.get("is_parse_retry")),
            outcome=outcome or str(run_data.get("final_status") or ""), reason=reason,
            cost_usd=round(sum(costs), 6) if priced else None,
            cost_basis="provider_reported" if priced else "unknown",
        ))
    return rows


def write_task_tier_outcomes(run_data: dict[str, Any], task: Any, task_out: Path, task_rel: str,
                             ledger_project_id: str | None, job_id: str | None) -> dict[str, str]:
    """Write one task run's `tier_outcomes.json` and mirror it; answer the written files by relative name.

    Writes nothing for a run without tiers. The mirror, armed only by a ledger target, never fails
    the export: the file is the record.
    """
    rows = tier_outcome_rows(run_data, job_id=str(job_id or ""), task_id=str(task.task_id),
                             task_class=str(getattr(task, "task_class", "") or ""))
    if not rows:
        return {}
    target = Path(task_out) / TIER_OUTCOMES_FILENAME
    target.write_text(json.dumps({"rows": [asdict(row) for row in rows]}, indent=2) + "\n", encoding="utf-8")
    if ledger_project_id is not None and job_id:
        try:
            record_tier_outcomes(rows_from_evidence_file(target), project_id=ledger_project_id)
        # The ledger's own errors, a file that will not read back, and a row the table refuses.
        except (sqlite3.Error, OSError, ValueError, TypeError):
            logger.error("tier outcome mirror FAILED for task %r; the evidence file is unaffected",
                         task.task_id, exc_info=True)
    return {f"{task_rel}/{TIER_OUTCOMES_FILENAME}": str(target)}


def rows_from_evidence_file(path: Path) -> list[TierOutcomeRow]:
    """The rows a `tier_outcomes.json` holds, read back as the mirror records them."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [TierOutcomeRow(**row) for row in data.get("rows") or []]


def _open(project_id: str | None, path: Path | str | None) -> Any:
    from packages.orchestration.token_ledger import open_ledger, token_ledger_path_for

    conn = open_ledger(path if path is not None else token_ledger_path_for(str(project_id)))
    with conn:
        conn.execute(_CREATE_TABLE)
        conn.execute("INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)",
                     (TIER_OUTCOMES_SCHEMA_KEY, str(TIER_OUTCOMES_SCHEMA_VERSION)))
    return conn


def record_tier_outcomes(rows: list[TierOutcomeRow], *, project_id: str | None = None,
                         path: Path | str | None = None) -> int:
    """Mirror `rows` into the ledger's `tier_outcomes` table; a re-export replaces its own rows."""
    conn = _open(project_id, path)
    try:
        with conn:
            conn.executemany(
                f"INSERT OR REPLACE INTO {TIER_OUTCOMES_TABLE} VALUES "
                "(:job_id, :task_id, :run_id, :first_round, :task_class, :tier, :reviewer_tier, :last_round, "
                ":rounds, :retries, :outcome, :reason, :cost_usd, :cost_basis)",
                [asdict(row) for row in rows])
    finally:
        conn.close()
    return len(rows)


@dataclass(frozen=True)
class TierOutcomeSummary:
    """One task class on one tier, over every task run the ledger holds."""

    task_class: str
    tier: str
    task_runs: int
    outcomes: dict[str, int]
    rounds: int
    retries: int
    cost_usd: float | None
    priced_runs: int


def query_tier_outcomes(*, project_id: str | None = None, path: Path | str | None = None) -> list[TierOutcomeSummary]:
    """One summary per task class and tier, sorted by both; the cost sums only the runs that report one."""
    conn = _open(project_id, path)
    try:
        found = conn.execute(
            f"SELECT task_class, tier, outcome, rounds, retries, cost_usd FROM {TIER_OUTCOMES_TABLE} "
            "ORDER BY task_class, tier").fetchall()
    finally:
        conn.close()
    groups: dict[tuple[str, str], list[Any]] = {}
    for row in found:
        groups.setdefault((row[0], row[1]), []).append(row)
    summaries = []
    for (task_class, tier), rows in sorted(groups.items()):
        outcomes: dict[str, int] = {}
        for row in rows:
            outcomes[row[2]] = outcomes.get(row[2], 0) + 1
        priced = [row[5] for row in rows if row[5] is not None]
        summaries.append(TierOutcomeSummary(
            task_class=task_class, tier=tier, task_runs=len(rows), outcomes=dict(sorted(outcomes.items())),
            rounds=sum(row[3] for row in rows), retries=sum(row[4] for row in rows),
            cost_usd=round(sum(priced), 6) if priced else None, priced_runs=len(priced)))
    return summaries
