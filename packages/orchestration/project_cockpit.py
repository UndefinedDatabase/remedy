"""The multi-project cockpit's project list and per-project summary (F042 T001, DECISION F042 D1).

PURE COMPOSITION over readers that already exist: this module owns no storage,
writes no file, starts no subprocess and opens no socket. ``projects_view``
lists every registered project with its folder checked at read time;
``project_summary`` answers one project's card by summing over that project's
own scoped jobs, through ``project_scope.scoped_jobs`` (F148's legacy rule
unchanged), each job's own ``decision_inbox`` and the token ledger's
``query_cost``. Nothing here mutates the registry, a job record or a ledger.

Public API::

    PROJECT_COCKPIT_VERSION — int, payload version of both envelopes
    MISSING_REPO_FIX_IT — str template, a recorded folder that is gone
    NO_REPO_FIX_IT — str template, a project with no folder attached
    projects_view(cwd=".") -> dict
    find_project(selector) -> RemyProject | None
    project_summary(project, now=None) -> dict
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.job_digest import (
    COST_BASIS_ABSENT,
    COST_BASIS_ACTUAL,
    COST_BASIS_LOWER_BOUND,
    OPEN_CARD_STATUS,
)

#: Payload version of both envelopes this module answers.
PROJECT_COCKPIT_VERSION = 1

#: A project whose recorded folder is no longer a directory (DECISION F042 D1
#: clause 3). ``{path}`` and ``{slug}`` are filled by the caller.
MISSING_REPO_FIX_IT = (
    "The folder {path} is not there any more. If the project moved, "
    "run: remedy project attach --project {slug} --repo <the new folder>"
)

#: A project with no folder attached at all — the registry allows this, so
#: the cockpit names the fix rather than hiding the entry.
NO_REPO_FIX_IT = (
    "No folder is attached to this project. "
    "Run: remedy project attach --project {slug} --repo <its folder>"
)


def _project_entry(project: Any) -> dict[str, Any]:
    """One project's row in the list: its folder checked NOW, never cached."""
    repo = project.canonical_repo_path
    if not repo:
        return {
            "id": str(project.id),
            "slug": project.slug,
            "name": project.name,
            "repo_path": None,
            "repo_reachable": False,
            "fix_it": NO_REPO_FIX_IT.format(slug=project.slug),
        }
    reachable = Path(repo).is_dir()
    fix_it = None if reachable else MISSING_REPO_FIX_IT.format(path=repo, slug=project.slug)
    return {
        "id": str(project.id),
        "slug": project.slug,
        "name": project.name,
        "repo_path": repo,
        "repo_reachable": reachable,
        "fix_it": fix_it,
    }


def projects_view(cwd: str = ".") -> dict[str, Any]:
    """Every registered project, the resolution precedence's default, and the
    jobs no card can show — counted, never hidden (DECISION F042 D1 clause 1).
    """
    from packages.orchestration.pingpong_job import list_job_plans_safe
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        _list_projects_readonly,
        select_project,
    )

    projects = sorted(_list_projects_readonly(), key=lambda p: (p.slug or "", str(p.id)))
    entries = [_project_entry(p) for p in projects]

    try:
        project, source = select_project(None, cwd)
        default_project: dict[str, Any] | None = {
            "id": str(project.id), "slug": project.slug, "source": source,
        }
    except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
        default_project = None

    known_ids = {str(p.id) for p in projects}
    jobs, _degraded, _skipped = list_job_plans_safe()
    unscoped_jobs = sum(1 for j in jobs if not j.project_id)
    orphaned_jobs = sum(1 for j in jobs if j.project_id and j.project_id not in known_ids)

    return {
        "version": PROJECT_COCKPIT_VERSION,
        "projects": entries,
        "default_project": default_project,
        "single_project": len(entries) == 1,
        "unscoped_jobs": unscoped_jobs,
        "orphaned_jobs": orphaned_jobs,
    }


def find_project(selector: str) -> Any | None:
    """The project *selector* (a slug or a UUID) names, or None when it names
    none or more than one (DECISION F042 D1)."""
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        ProjectNotFoundError,
        _lookup_by_slug_or_uuid_readonly,
    )

    try:
        return _lookup_by_slug_or_uuid_readonly(selector)
    except (AmbiguousProjectError, ProjectNotFoundError):
        return None


def job_project_view(job: Any) -> dict[str, Any]:
    """The project one job belongs to, labelled the way ``remedy job list`` labels a job
    (F042 T002, DECISION F042 D2): ``unscoped`` for a job with no recorded project,
    ``orphaned`` for a project id ``find_project`` cannot resolve, and ``project``
    otherwise, carrying the SAME list entry ``projects_view`` builds for that project.
    """
    job_id = str(job.job_id)
    if not job.project_id:
        return {"version": PROJECT_COCKPIT_VERSION, "job_id": job_id, "scope": "unscoped", "project": None}
    project = find_project(job.project_id)
    if project is None:
        return {"version": PROJECT_COCKPIT_VERSION, "job_id": job_id, "scope": "orphaned", "project": None}
    return {
        "version": PROJECT_COCKPIT_VERSION,
        "job_id": job_id,
        "scope": "project",
        "project": _project_entry(project),
    }


def project_summary(project: Any, now: datetime | None = None) -> dict[str, Any]:
    """One project's card: its scoped jobs, newest result, open decisions summed
    across those jobs, and today's cost, all through readers that already exist
    (DECISION F042 D1 clause 2). ``now`` defaults to the real clock; a naive
    value is taken as UTC.
    """
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    moment = moment.astimezone(timezone.utc)

    from packages.orchestration.pingpong_job import job_is_terminal
    from packages.orchestration.project_scope import ProjectScope, scoped_jobs

    scope = ProjectScope(project_id=str(project.id), all_projects=False, source="cockpit")
    jobs, degraded, _skipped = scoped_jobs(scope)

    active = sum(1 for j in jobs if not job_is_terminal(j.state))
    total = len(jobs)

    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.decision_inbox import build_decision_inbox, decision_urgency
    from packages.orchestration.timeline import load_run_events

    open_count = 0
    peak_urgency = 0
    for job in jobs:
        try:
            events = load_run_events(resolve_data_root(), str(job.job_id))
            inbox = build_decision_inbox(job, events, now=moment)
        except Exception:  # noqa: BLE001 — an unreadable job's inbox is skipped, never the card
            continue
        for card in inbox.get("decisions", ()):
            if card.get("status") == OPEN_CARD_STATUS:
                open_count += 1
                peak_urgency = max(peak_urgency, decision_urgency(card))

    if jobs:
        from packages.orchestration.job_digest import build_job_digest

        newest = jobs[0]
        digest = build_job_digest(newest)
        last_result: dict[str, Any] | None = {
            "job_id": str(newest.job_id),
            "title": newest.job_title,
            "state": digest["state"],
            "headline": digest["headline"],
        }
    else:
        last_result = None

    from packages.orchestration.token_ledger import query_cost

    since = moment.date().isoformat()
    until = (moment.date() + timedelta(days=1)).isoformat()
    report = query_cost(project_id=project.id, since=since, until=until)
    total_row = report.total
    if not report.ledger_exists or not total_row.calls or total_row.cost_usd is None:
        basis = COST_BASIS_ABSENT
    elif total_row.unmeasured_calls > 0:
        basis = COST_BASIS_LOWER_BOUND
    else:
        basis = COST_BASIS_ACTUAL
    cost_today = {
        "day": since,
        "value_usd": total_row.cost_usd,
        "basis": basis,
        "calls": total_row.calls,
    }

    return {
        "version": PROJECT_COCKPIT_VERSION,
        "project_id": str(project.id),
        "slug": project.slug,
        "jobs": {"active": active, "total": total},
        "last_result": last_result,
        "cost_today": cost_today,
        "decisions": {"open_count": open_count, "peak_urgency": peak_urgency},
        "degraded": degraded,
    }
