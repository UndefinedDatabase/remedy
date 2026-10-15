"""The cockpit's mission card: a project's missions, each mission's orders on demand, and each
order's chain band (F305, DECISIONS F305 D1 and D2; finding R-1248).

READS ONLY: this module owns no storage, writes no file, starts no subprocess and opens no socket.
It reads the mission records through ``mission_state``, the jobs through the job store, and the
calls and tokens through the project's token ledger.

A repository has one lasting mission and every order is a batch in it (DECISION amend1011b D1,
D3); an order over several repositories adds a batch to each repository's own mission, all
batches sharing one correlation id (DECISION amend1011b D4). An order's CHAIN is therefore the
jobs of its own batch plus the jobs of every batch, in any project's missions, that carries the
same correlation id. A record written before order batches, which spans several projects through
``project_ids``, keeps its chain in its links, each naming its project.

A CHIP names one job of a chain by references and titles only — its id, its project, the folder
name of its repository, its title and its state — and never another project's evidence, cost or
path: Remedy deliberately does not show a job of another project beyond what its own cockpit,
opened from the chip, shows through that project's own routes. A per-order roll-up counts the
calls and tokens the token ledger of this mission's project holds for the order's own jobs; a cost
in US dollars is not shown (DECISION amend1007b D7).

Public API::

    MISSION_COCKPIT_VERSION — int, payload version of both envelopes
    project_missions_view(project) -> dict
    mission_orders_view(project, mission_id) -> (status, body)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.orchestration.client_digest import (
    _LEDGER_READ_ERRORS,
    _merged_usage,
    _tokens_by_kind,
)
from packages.orchestration.mission_record import Mission, MissionError
from packages.orchestration.mission_state import (
    MISSING_JOB_LABEL,
    UNREADABLE_JOB_LABEL,
    list_missions,
    list_missions_safe,
    load_mission,
    project_ids_with_missions,
)
from packages.orchestration.repo_mission import RENDER_RECENT, order_batch_view, project_by_id
from packages.orchestration.token_ledger import CostRow, ledger_usage_by_job

#: Payload version of both envelopes this module answers.
MISSION_COCKPIT_VERSION = 1

#: The longest order title a row carries: the order text's first line, cut here.
ORDER_TITLE_CHARS = 80


def _mission_card(mission: Mission) -> dict[str, Any]:
    """One mission's card: what it is for and how much it holds, with no job's content."""
    return {
        "mission_id": mission.id,
        "goal": mission.goal,
        "status": mission.status,
        "created_at": mission.created_at,
        "order_count": len(mission.orders),
        "job_count": len(mission.job_links),
    }


def project_missions_view(project: Any) -> dict[str, Any]:
    """Every mission of *project*, newest first, as cards; their orders are a second request."""
    missions, degraded, skipped = list_missions_safe(str(project.id))
    return {
        "version": MISSION_COCKPIT_VERSION,
        "project_id": str(project.id),
        "slug": project.slug,
        "missions": [_mission_card(mission) for mission in missions],
        "degraded": degraded,
        "skipped_count": len(skipped),
    }


def _job_chip(job_id: str, project_id: str, slugs: dict[str, str]) -> dict[str, Any]:
    """One job of a chain by references and titles only; the job's state as the store says it now."""
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.pingpong_job import load_job_plan_safe

    if project_id not in slugs:
        slugs[project_id] = str(project_by_id(project_id).slug or project_id)
    try:
        plan, degraded = load_job_plan_safe(normalize_job_id(job_id))
    except (OSError, ValueError):
        plan, degraded = None, False
    if plan is None:
        state, title, repo_name = (UNREADABLE_JOB_LABEL if degraded else MISSING_JOB_LABEL), "", ""
    else:
        state = str(getattr(plan.state, "value", plan.state))
        title = plan.job_title
        repo_name = Path(plan.repo_path).name if plan.repo_path else ""
    return {"job_id": job_id, "project_id": project_id, "slug": slugs[project_id],
            "repo_name": repo_name, "title": title, "state": state}


def _correlated_links(correlation_id: str, own: Mission) -> list[tuple[str, str, str]]:
    """``(created_at, job_id, project_id)`` of every job another mission's batch of the same
    correlation id holds, read across every project's missions."""
    found: list[tuple[str, str, str]] = []
    for project_id in project_ids_with_missions():
        for mission in list_missions(project_id):
            if mission.id == own.id:
                continue
            order_ids = {batch.order_id for batch in mission.orders
                         if batch.correlation_id == correlation_id}
            found += [(link.created_at, link.job_id, mission.project_id)
                      for link in mission.job_links if link.order_id in order_ids]
    return found


def _order_model_turns(job_ids: list[str]) -> int | None:
    """The Pi model turns of an order's jobs, from Pi's own call records; null when Pi made none."""
    from packages.orchestration.pi_turn_counts import pi_turns_for_job
    from packages.orchestration.pingpong_job import load_job_plan

    run_ids: list[str] = []
    for job_id in job_ids:
        plan = load_job_plan(job_id)
        run_ids += [str(r) for r in plan.run_refs] if plan is not None else []
    per_role = pi_turns_for_job(run_ids)
    return sum(figures["model_turns"] for figures in per_role.values()) if per_role else None


def _order_usage(job_ids: list[str], usage_by_job: dict[str, CostRow] | None) -> dict[str, Any]:
    """The calls and tokens one project's ledger holds for *job_ids*, summed; null when the ledger
    could not be read, and a job the ledger does not name made no recorded call there."""
    if usage_by_job is None:
        return {"harness_invocations": None, "model_turns": None, "tokens": _tokens_by_kind(None)}
    total = CostRow()
    for job_id in job_ids:
        row = usage_by_job.get(job_id)
        if row is not None:
            total = _merged_usage(total, row)
    return {"harness_invocations": total.calls, "model_turns": _order_model_turns(job_ids),
            "tokens": _tokens_by_kind(total)}


def _order_title(text: str) -> str:
    """An order's title: the first line of its text, cut to ``ORDER_TITLE_CHARS``."""
    return (text.strip().splitlines() or [""])[0][:ORDER_TITLE_CHARS]


def mission_orders_view(project: Any, mission_id: str) -> tuple[int, dict[str, Any]]:
    """One mission's newest orders, each with its chain band and its calls and tokens; 404 for a
    mission *project* does not hold or an id that is no mission id."""
    project_id = str(project.id)
    try:
        mission = load_mission(project_id, mission_id)
    except MissionError:
        return (404, {"error": "mission not found"})
    try:
        usage_by_job: dict[str, CostRow] | None = ledger_usage_by_job(project_id=project_id)
    except _LEDGER_READ_ERRORS:
        usage_by_job = None
    created = {link.job_id: link.created_at for link in mission.job_links}
    link_project = {link.job_id: link.project_id or mission.project_id for link in mission.job_links}
    slugs = {project_id: str(project.slug or project_id)}
    rows = order_batch_view(mission)
    orders = []
    for row in reversed(rows[-RENDER_RECENT:]):
        job_ids = list(row["job_ids"])
        chain = [(created.get(job_id, ""), job_id, link_project[job_id]) for job_id in job_ids]
        correlation_id = str(row.get("correlation_id", ""))
        if correlation_id:
            chain += _correlated_links(correlation_id, mission)
        orders.append({
            "order_id": row["order_id"],
            "title": _order_title(str(row.get("text", ""))),
            "created_at": str(row.get("created_at", "")),
            "kind": str(row.get("kind", "")),
            "sealed": bool(row.get("sealed")),
            "correlation_id": correlation_id,
            "job_count": len(job_ids),
            "usage": _order_usage(job_ids, usage_by_job),
            "chain": [_job_chip(job_id, chain_project, slugs)
                      for _created, job_id, chain_project in sorted(chain)],
        })
    return (200, {
        "version": MISSION_COCKPIT_VERSION,
        "project_id": project_id,
        "slug": project.slug,
        "mission_id": mission.id,
        "goal": mission.goal,
        "orders": orders,
        "earlier_orders": max(0, len(rows) - RENDER_RECENT),
        "degraded": usage_by_job is None,
    })
