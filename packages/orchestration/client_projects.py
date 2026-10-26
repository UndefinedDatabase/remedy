"""The projects a client may see (operator amendment amend1026-go-live-and-ask, Part C1).

`GET /api/v1/projects` and `remedy client projects --json` answer it: each registered project the
calling token lists (the server's own token sees every one), with its `slug`, `name`, `repo_path`,
`description`, how many of its jobs are still open, when its newest job was created, and the result
of its newest test run, read from the jobs' verification (`order_verification.job_verification`).
It reads the project registry and the job records and writes nothing.

Remedy deliberately keeps no per-project counter of its own: every figure is read from the job
records at the moment of the call, so the list can never disagree with the jobs it counts.
"""
from __future__ import annotations

from typing import Any

#: The top-level keys of the answer beside the envelope's own.
CLIENT_PROJECTS_ANSWER_KEYS: tuple[str, ...] = ("projects",)

#: The keys under them, as the machine client interface declares them.
CLIENT_PROJECTS_KEY_TREE: dict[str, Any] = {
    "projects": {"slug": {}, "name": {}, "repo_path": {}, "description": {}, "open_jobs": {},
                 "last_job_at": {}, "last_test": {"status": {}, "job_id": {}, "at": {}}},
}

#: The verification statuses that mean a test really ran (`order_verification.VERIFICATION_STATUSES`).
_TEST_RAN = ("passed", "failed")


def _last_test(plans: list[Any]) -> dict[str, Any] | None:
    """The newest job of PLANS (newest first) whose tests ran: its status, its id and when it ended."""
    from packages.orchestration.order_verification import job_verification

    for plan in plans:
        status = job_verification(plan).get("status")
        if status in _TEST_RAN:
            return {"status": status, "job_id": str(plan.job_id),
                    "at": str(plan.finished_at or plan.created_at or "") or None}
    return None


def client_projects(client: Any = None) -> dict[str, Any]:
    """Every registered project CLIENT lists, sorted by slug; every project for the server's token."""
    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.pingpong_job import job_is_terminal, list_job_plans_safe
    from packages.orchestration.project_registry import list_projects_readonly

    plans, _degraded, _skipped = list_job_plans_safe()
    entries: list[dict[str, Any]] = []
    for project in list_projects_readonly():
        if client is not None and not client_lists_project(client, (project.slug or "", str(project.id))):
            continue
        own = [plan for plan in plans if str(plan.project_id or "") == str(project.id)]
        entries.append({
            "slug": project.slug or "", "name": project.name,
            "repo_path": project.canonical_repo_path or (project.repo_paths[0] if project.repo_paths else None),
            "description": project.description or "",
            "open_jobs": sum(1 for plan in own if not job_is_terminal(plan.state)),
            "last_job_at": max((str(plan.created_at) for plan in own if plan.created_at), default=None),
            "last_test": _last_test(own),
        })
    return {"projects": sorted(entries, key=lambda entry: entry["slug"])}


def client_projects_answer(*, client: Any = None) -> dict[str, Any]:
    """The answer `GET /api/v1/projects` and `remedy client projects --json` share."""
    from apps.cli.json_envelope import build_ok

    return build_ok(**client_projects(client))
