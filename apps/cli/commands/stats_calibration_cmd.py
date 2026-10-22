"""`remedy stats calibration` — the estimate calibration's trust view (F074 T003, DECISION F074 D2).

It shows what the shared estimator reads for one project: per task class and role, how many tasks
were measured and their P20, P50 and P80 of tokens and of cost, which classes are calibrated, the
window, the sample floor and how old the measurement is. It reads the project's cost ledger and job
records and never writes either; the one file it may write is the calibration snapshot beside the
ledger, which it measures again when the snapshot is older than its limit
(`docs/system/estimate-calibration-v1.md`).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from apps.cli.json_envelope import emit_ok, fail

#: The version of this command's own JSON payload.
CALIBRATION_OUTPUT_VERSION = 1
_HEADERS = ("class", "role", "tasks", "tokens P20", "P50", "P80", "cost P20", "P50", "P80", "estimates")
UNPRICED = "unpriced"


def _estimates_cell(table: Any, entry: Any) -> str:
    # Only the whole task is what an estimate reads, so only its row says which basis applies.
    from packages.orchestration.estimate_calibration import TASK_TOTAL_ROLE, calibration_basis_label

    if entry.role != TASK_TOTAL_ROLE:
        return ""
    if entry.tokens.n >= table.sample_floor:
        return calibration_basis_label(entry.tokens.n)
    return f"class default ({entry.tokens.n} of {table.sample_floor})"


def calibration_rows(table: Any) -> list[list[str]]:
    """One row per task class and role, the whole task first within its class."""
    from packages.orchestration.estimate_calibration import TASK_TOTAL_ROLE

    rows = []
    for entry in sorted(table.entries, key=lambda e: (e.task_class, e.role != TASK_TOTAL_ROLE, e.role)):
        tokens, cost = entry.tokens, entry.cost_usd
        costs = [f"${v:.4f}" for v in (cost.p20, cost.p50, cost.p80)] if cost is not None else [UNPRICED] * 3
        rows.append([entry.task_class, entry.role, str(tokens.n),
                     *(f"{round(v):,}" for v in (tokens.p20, tokens.p50, tokens.p80)), *costs,
                     _estimates_cell(table, entry)])
    return rows


def render_calibration_text(table: Any, *, max_age_seconds: int, now: datetime) -> str:
    """The table with its window, its floor and its staleness, or why every estimate stays on its default."""
    lines = [f"Estimate calibration of project {table.project_id}, measured from its cost ledger"]
    if not table.ledger_present:
        lines.append("This project has no cost ledger yet, so every estimate stays on its class default.")
        return "\n".join(lines)
    measured = datetime.fromisoformat(table.updated_at)
    lines.append(f"Window: the last {table.window_days} days, tasks whose latest call is at or after "
                 f"{table.window_start}. Floor: {table.sample_floor} tasks per class.")
    lines.append(f"Measured at {table.updated_at}, {max(0, int((now - measured).total_seconds()))} seconds ago; "
                 f"the first read after {(measured + timedelta(seconds=max_age_seconds)).isoformat()} "
                 "measures again.")
    if table.entries:
        rows = calibration_rows(table)
        widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(_HEADERS)]
        lines.append("  ".join(h.ljust(widths[i]) for i, h in enumerate(_HEADERS)).rstrip())
        lines += ["  ".join(c.ljust(widths[i]) for i, c in enumerate(r)).rstrip() for r in rows]
    else:
        lines.append("No measured task falls inside the window, so every estimate stays on its class default.")
    lines.append(f"Not counted: {table.unclassified_tasks} tasks with no class on record, "
                 f"{table.unmeasured_tasks} tasks whose calls did not all report their tokens.")
    return "\n".join(lines)


def _project_repo(project_id: str) -> str | None:
    """The registered repository of ``project_id``, read without writing the registry."""
    from packages.orchestration.project_registry import list_projects_readonly

    project = next((p for p in list_projects_readonly() if str(p.id) == project_id), None)
    return getattr(project, "canonical_repo_path", None) or None


def _cmd_stats_calibration(*, project: str | None = None, json_output: bool = False) -> None:
    from packages.orchestration.budget_resolution import BudgetConfigError, resolve_calibration_settings
    from packages.orchestration.estimate_calibration import load_calibration_table
    from packages.orchestration.project_scope import resolve_scope

    scope = resolve_scope(project_flag=project, all_projects=False)
    if scope.project_id is None:
        fail("no_project", "no project resolved for stats calibration. Run inside a registered "
             "project or pass --project <slug-or-uuid>.", json_output=json_output)
    try:
        settings = resolve_calibration_settings(project_root=_project_repo(scope.project_id))
    except BudgetConfigError as exc:
        fail("invalid_budget", f"{exc} Nothing was measured.", json_output=json_output, exit_code=2)
    now = datetime.now(timezone.utc)
    table = load_calibration_table(scope.project_id, now=now, **settings)
    if json_output:
        calibrated = sorted({e.task_class for e in table.entries if table.calibrated_tokens(e.task_class)})
        emit_ok(version=CALIBRATION_OUTPUT_VERSION, max_age_seconds=settings["max_age_seconds"],
                calibrated_classes=calibrated, **table.to_json())
    else:
        print(render_calibration_text(table, max_age_seconds=settings["max_age_seconds"], now=now))


COMMAND_HANDLERS = {
    "stats.calibration": lambda args: _cmd_stats_calibration(
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
}
