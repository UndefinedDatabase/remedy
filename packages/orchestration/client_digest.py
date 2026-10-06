"""The `client` object's version-1 frame in `remedy status --json` (DECISION F295 D4).

Version 1 carries every registered project with its missions, every job on the
data root, which of those jobs wait for an operator's apply, and whether the
supervisor answers. The next round adds, under the same version, each job's
open decisions, its measured cost and its evidence references.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from packages.orchestration.job_apply import job_apply_landed
from packages.orchestration.mission_state import Mission, list_missions_safe
from packages.orchestration.pingpong_job import JOB_COMPLETED, list_job_plans_safe
from packages.orchestration.project_registry import list_projects
from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths

#: The frame's own version; DECISION F295 D4 (5) adds to it without moving it.
CLIENT_DIGEST_VERSION = 1


def _mission_entry(mission: Mission) -> dict[str, Any]:
    """One mission's DECISION F295 D4 (2) shape; an order given as text leaves two keys empty."""
    order = mission.order
    return {
        "mission_id": mission.id,
        "status": mission.status,
        "goal": mission.goal,
        "job_ids": list(mission.job_ids()),
        "order_source_path": order.source_path if order is not None else "",
        "order_source_sha256": order.source_sha256 if order is not None else "",
    }


# DECISION F295 D4 (2): the one builder of the `client` key `_cmd_status` adds to its answer.
def build_client_digest(now: datetime | None = None) -> dict[str, Any]:
    """The `client` object's version-1 frame (DECISION F295 D4 (2), (3)); reads only, never writes.

    Projects sorted by slug, each with its missions newest first
    (``list_missions_safe``'s own order); jobs sorted by job id
    (``list_job_plans_safe``'s own order gives the plans, this function
    sorts them); ``awaiting_apply`` sorted. ``degraded`` and
    ``skipped_files`` gather what the two listing functions could not read,
    named exactly as they return them.
    """
    when = now if now is not None else datetime.now(timezone.utc)

    degraded = False
    skipped_files: list[str] = []

    projects = sorted(list_projects(), key=lambda p: p.slug or "")
    project_entries: list[dict[str, Any]] = []
    mission_id_by_job_id: dict[str, str] = {}
    for project in projects:
        project_id = str(project.id)
        missions, mission_degraded, mission_skipped = list_missions_safe(project_id)
        degraded = degraded or mission_degraded
        skipped_files.extend(mission_skipped)
        project_entries.append({
            "project_id": project_id,
            "slug": project.slug or "",
            "missions": [_mission_entry(m) for m in missions],
        })
        # Built once here, never one scan per job below.
        for mission in missions:
            for job_id in mission.job_ids():
                mission_id_by_job_id[job_id] = mission.id

    plans, jobs_degraded, jobs_skipped = list_job_plans_safe()
    degraded = degraded or jobs_degraded
    skipped_files.extend(jobs_skipped)

    job_entries: list[dict[str, Any]] = []
    awaiting_apply: list[str] = []
    for plan in sorted(plans, key=lambda p: str(p.job_id)):
        job_id = str(plan.job_id)
        state = plan.state.value
        waits_for_apply = plan.state == JOB_COMPLETED and not job_apply_landed(job_id)
        if waits_for_apply:
            awaiting_apply.append(job_id)
        job_entries.append({
            "job_id": job_id,
            "project_id": plan.project_id,
            "mission_id": mission_id_by_job_id.get(job_id),
            "title": plan.job_title,
            "state": state,
            "waits_for_apply": waits_for_apply,
        })

    return {
        "version": CLIENT_DIGEST_VERSION,
        "read_at": when.isoformat(),
        "supervisor": {"answers": socket_answers(serve_paths().socket)},
        "projects": project_entries,
        "jobs": job_entries,
        "awaiting_apply": sorted(awaiting_apply),
        "degraded": degraded,
        "skipped_files": skipped_files,
    }
