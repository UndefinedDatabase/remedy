"""`remedy stats trust` — the model trust view (F133 T003, DECISION F133 D2 (6)).

It shows, for one project, every model and role seen inside the window: how often its tasks
passed, how many repair rounds they needed, how often its answers could not be read, and what a
passed task cost, each with the number of tasks or calls it rests on, and the pass quota's change
against the prior window of the same length. It reads the project's cost ledger, job records and
provider evidence and never writes any of them; the one file it may write is the trust snapshot
beside the ledger (`docs/system/model-trust-score-v1.md`).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from apps.cli.json_envelope import emit_ok, fail

#: The version of this command's own JSON payload.
TRUST_OUTPUT_VERSION = 1
_HEADERS = ("role", "model", "tasks", "pass quota", "repair/task", "format err", "cost/pass",
            "Δ pass quota")
DASH = "—"


def _format_change(row: Any, prior: Any) -> str:
    prior_row = prior.lookup(row.model, row.role)
    if prior_row is None:
        return "new"
    if row.pass_quota.value is None or prior_row.pass_quota.value is None:
        return DASH
    delta = (row.pass_quota.value - prior_row.pass_quota.value) * 100
    return f"{delta:+.0f}pp"


def _format_cost(row: Any) -> str:
    """The cost cell, naming its basis and — R-1431 — the passes the figure rests on."""
    from packages.orchestration.model_trust_score import (
        COST_BASIS_PROVIDER_REPORTED,
        TRUST_COST_BASIS_MIXED,
        TRUST_COST_BASIS_PRICE_TABLE,
        TRUST_COST_BASIS_TOKENS,
    )

    n = row.cost_per_pass.n
    basis = row.cost_basis
    detail = basis if n == 0 else f"{basis}, {n} {'pass' if n == 1 else 'passes'}"
    if row.cost_per_pass.value is None:
        return f"{DASH} ({detail})"
    if basis in (COST_BASIS_PROVIDER_REPORTED, TRUST_COST_BASIS_PRICE_TABLE, TRUST_COST_BASIS_MIXED):
        return f"${row.cost_per_pass.value:.4f} ({detail})"
    if basis == TRUST_COST_BASIS_TOKENS:
        return f"{row.cost_per_pass.value:.0f} tokens ({detail})"
    return f"{DASH} ({detail})"


def trust_rows(table: Any, prior: Any, *, role: str | None = None) -> list[list[str]]:
    """One row per model and role, sorted as the table already is; ``role`` keeps one role's rows."""
    rows = []
    for row in table.rows:
        if role is not None and row.role != role:
            continue
        floor_note = f"{row.settled_tasks}/{table.sample_floor} thin" if row.thin else str(row.settled_tasks)
        pass_quota = DASH if row.pass_quota.value is None else f"{row.pass_quota.value * 100:.0f}%"
        repair = DASH if row.repair_need.value is None else f"{row.repair_need.value:.2f}"
        fmt_err = (DASH if row.format_error_rate.n == 0
                   else f"{row.format_error_rate.value * 100:.0f}% ({row.format_error_rate.n} calls)")
        rows.append([row.role, row.model, floor_note, pass_quota, repair, fmt_err,
                     _format_cost(row), _format_change(row, prior)])
    return rows


def render_trust_text(table: Any, prior: Any, *, max_age_seconds: int, now: datetime,
                       role: str | None = None) -> str:
    """The matrix with its window, its floor and its staleness, or why there is nothing to show."""
    lines = [f"Model trust of project {table.project_id}, measured from its cost ledger, job "
             "records and provider evidence"]
    if not table.ledger_present:
        lines.append("This project has no cost ledger yet, so no model has a trust row.")
        return "\n".join(lines)
    measured = datetime.fromisoformat(table.updated_at)
    lines.append(f"Window: the last {table.window_days} days, tasks whose latest call is at or after "
                 f"{table.window_start}. Floor: {table.sample_floor} settled tasks per model and role.")
    lines.append(f"Measured at {table.updated_at}, {max(0, int((now - measured).total_seconds()))} "
                 f"seconds ago; the first read after "
                 f"{(measured + timedelta(seconds=max_age_seconds)).isoformat()} measures again.")
    rows = trust_rows(table, prior, role=role)
    if rows:
        widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(_HEADERS)]
        lines.append("  ".join(h.ljust(widths[i]) for i, h in enumerate(_HEADERS)).rstrip())
        lines += ["  ".join(c.ljust(widths[i]) for i, c in enumerate(r)).rstrip() for r in rows]
    else:
        lines.append("No model or role falls inside the window.")
    lines.append(f"Unattributed calls: {table.unattributed_calls}. Unsettled tasks: "
                 f"{table.unsettled_tasks}.")
    return "\n".join(lines)


def _project_repo(project_id: str) -> str | None:
    """The registered repository of ``project_id``, read without writing the registry."""
    from packages.orchestration.project_registry import list_projects_readonly

    project = next((p for p in list_projects_readonly() if str(p.id) == project_id), None)
    return getattr(project, "canonical_repo_path", None) or None


def _table_payload(table: Any, *, role: str | None) -> dict[str, Any]:
    """``table.to_json()``, with its rows kept to one role when ``role`` is given."""
    payload = table.to_json()
    if role is not None:
        payload["rows"] = [row for row in payload["rows"] if row["role"] == role]
    return payload


def _changes_payload(table: Any, prior: Any, *, role: str | None) -> list[dict[str, Any]]:
    changes = []
    for row in table.rows:
        if role is not None and row.role != role:
            continue
        prior_row = prior.lookup(row.model, row.role)
        if prior_row is None:
            change = {"role": row.role, "model": row.model, "new": True, "pass_quota_change": None}
        else:
            both_known = row.pass_quota.value is not None and prior_row.pass_quota.value is not None
            change = {
                "role": row.role, "model": row.model, "new": False,
                "pass_quota_change": (
                    (row.pass_quota.value - prior_row.pass_quota.value) if both_known else None),
            }
        changes.append(change)
    return changes


def _cmd_stats_trust(*, project: str | None = None, role: str | None = None,
                      json_output: bool = False) -> None:
    from packages.orchestration.model_trust_score import (
        TrustConfigError,
        build_model_trust_table,
        load_model_trust_table,
        resolve_trust_settings,
    )
    from packages.orchestration.project_scope import resolve_scope

    scope = resolve_scope(project_flag=project, all_projects=False)
    if scope.project_id is None:
        fail("no_project", "no project resolved for stats trust. Run inside a registered "
             "project or pass --project <slug-or-uuid>.", json_output=json_output)
    try:
        settings = resolve_trust_settings(project_root=_project_repo(scope.project_id))
    except TrustConfigError as exc:
        fail("invalid_trust_setting", f"{exc} Nothing was measured.", json_output=json_output, exit_code=2)
    now = datetime.now(timezone.utc)
    table = load_model_trust_table(
        scope.project_id, now=now, window_days=settings["window_days"],
        sample_floor=settings["sample_floor"], max_age_seconds=settings["max_age_seconds"])
    prior_now = now - timedelta(days=settings["window_days"])
    prior = build_model_trust_table(
        scope.project_id, now=prior_now, window_days=settings["window_days"],
        sample_floor=settings["sample_floor"], window_end=prior_now)
    if json_output:
        emit_ok(version=TRUST_OUTPUT_VERSION, max_age_seconds=settings["max_age_seconds"], role=role,
                table=_table_payload(table, role=role), prior=_table_payload(prior, role=role),
                changes=_changes_payload(table, prior, role=role))
    else:
        print(render_trust_text(table, prior, max_age_seconds=settings["max_age_seconds"], now=now, role=role))


COMMAND_HANDLERS = {
    "stats.trust": lambda args: _cmd_stats_trust(
        project=getattr(args, "project", None),
        role=getattr(args, "role", None),
        json_output=getattr(args, "json", False),
    ),
}
