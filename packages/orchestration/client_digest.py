"""The `client` object's version-1 frame in `remedy status --json` (DECISION F295 D4, D5).

Version 1 carries every registered project with its missions, every job on the
data root, which of those jobs wait for an operator's apply, whether the
supervisor answers, and every job's open decisions (DECISION F295 D5). The
next round adds, under the same version, each job's measured cost and its
evidence references.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.decision_queue import HumanDecision, list_decisions
from packages.orchestration.escalation import DECISION_TYPE_TASK_DECISION
from packages.orchestration.job_apply import job_apply_landed
from packages.orchestration.mission_state import Mission, list_missions_safe
from packages.orchestration.pingpong_job import JOB_COMPLETED, list_job_plans_safe
from packages.orchestration.project_registry import list_projects
from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.timeline import load_run_events

#: The frame's own version; DECISION F295 D4 (5) adds to it without moving it.
CLIENT_DIGEST_VERSION = 1


def _decision_entry(
    job_id: str, project_id: str, decision: HumanDecision, now: datetime,
) -> dict[str, Any]:
    """One open `HumanDecision` as DECISION F295 D5's object; `age_seconds` against *now*."""
    payload = decision.payload if isinstance(decision.payload, dict) else {}
    is_task_decision = decision.type == DECISION_TYPE_TASK_DECISION
    question = str(payload.get("question", "")) if is_task_decision else decision.safe_summary
    safe_default = str(payload.get("safe_default", "") or "") if is_task_decision else ""
    options = [str(o) for o in (payload.get("options") or [])]

    clarifications: list[dict[str, Any]] = []
    if decision.type == "task_plan_approval":
        for question_record in payload.get("clarifications") or []:
            default_answer = str(question_record.get("default_answer", "") or "")
            clarifications.append({
                "id": str(question_record.get("id", "")),
                "question": str(question_record.get("question", "")),
                "default": default_answer or None,
            })

    created_at = decision.created_at
    age_seconds: int | None = None
    if created_at:
        try:
            created = datetime.fromisoformat(created_at)
        except ValueError:
            created = None
        if created is not None:
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            age_seconds = int((now - created).total_seconds())

    return {
        "job_id": job_id,
        "project_id": project_id,
        "decision_id": decision.id,
        "type": decision.type,
        "severity": decision.severity,
        "question": question,
        "default": safe_default or None,
        "options": options,
        "clarifications": clarifications,
        "created_at": created_at,
        "age_seconds": age_seconds,
    }


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
    """The `client` object's version-1 frame (DECISION F295 D4 (2), (3); D5); reads only, never writes.

    Projects sorted by slug, each with its missions newest first
    (``list_missions_safe``'s own order); jobs sorted by job id
    (``list_job_plans_safe``'s own order gives the plans, this function
    sorts them); ``awaiting_apply`` sorted. ``decisions`` holds every open
    decision of every job, sorted by job id then decision id (DECISION
    F295 D5). ``degraded`` and ``skipped_files`` gather what the listing
    functions and the per-job decision read could not read, named exactly
    as they return them, plus ``decisions of job <job_id>`` for a job whose
    decisions could not be read.
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
    decision_entries: list[dict[str, Any]] = []
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
        try:
            events = load_run_events(resolve_data_root(), plan.job_id)
            for decision in list_decisions(plan, events):
                if decision.status == "open":
                    decision_entries.append(
                        _decision_entry(job_id, plan.project_id, decision, when))
        except Exception:  # noqa: BLE001 — one job's unreadable decisions must not break the digest
            degraded = True
            skipped_files.append(f"decisions of job {job_id}")

    return {
        "version": CLIENT_DIGEST_VERSION,
        "read_at": when.isoformat(),
        "supervisor": {"answers": socket_answers(serve_paths().socket)},
        "projects": project_entries,
        "jobs": job_entries,
        "awaiting_apply": sorted(awaiting_apply),
        "decisions": sorted(decision_entries, key=lambda e: (e["job_id"], e["decision_id"])),
        "degraded": degraded,
        "skipped_files": skipped_files,
    }
