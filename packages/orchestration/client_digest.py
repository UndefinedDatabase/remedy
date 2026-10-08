"""The `client` object's version-1 frame in `remedy status --json` (DECISION F295 D4, D5, D7).

Version 1 carries every registered project with its missions and its cost of
the day, every job on the data root with its measured cost and its evidence
references (DECISION F295 D7), which of those jobs wait for an operator's
apply, whether the supervisor answers, and every job's open decisions
(DECISION F295 D5). Each completed job carries its approval card, what an
operator approves its result on, read from the job's record only (DECISION
F304 D10).
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.budget_guard import BudgetCounterError, decode_persisted_budget_actuals
from packages.orchestration.data_paths import job_dir, job_evidence_dir, resolve_data_root
from packages.orchestration.decision_queue import HumanDecision, list_decisions
from packages.orchestration.escalation import DECISION_TYPE_TASK_DECISION
from packages.orchestration.job_apply import job_apply_landed, job_result_decline
from packages.orchestration.job_digest import cost_exactness_basis
from packages.orchestration.mission_state import MISSION_STATUS_ABANDONED, Mission, list_missions_safe
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JobPlan,
    TaskEntry,
    _reviewed_task_files,
    list_job_plans_safe,
)
from packages.orchestration.project_cockpit import project_cost_of_day
from packages.orchestration.project_registry import _list_projects_readonly
from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.timeline import load_run_events

#: The frame's own version; DECISION F295 D4 (5) adds to it without moving it.
CLIENT_DIGEST_VERSION = 1

#: What one job's decision read raises on a bad record (DECISION F295 D6): a run log that cannot
#: be read, a line that is not UTF-8 or not JSON or a decision that fails its evidence gate
#: (`ValueError`), a line that is JSON but not an object, and timestamps of mixed types.
_DECISION_READ_ERRORS = (OSError, ValueError, AttributeError, TypeError)

#: What one project's ledger read raises (DECISION F295 D7): a file that cannot be opened, and a
#: database SQLite cannot read.
_LEDGER_READ_ERRORS = (OSError, sqlite3.Error)

#: How many changed files an approval card names; its count names them all (DECISION F304 D10).
APPROVAL_CARD_FILE_LIMIT = 20


def _job_cost(plan: JobPlan) -> dict[str, Any]:
    """One job's measured cost in USD and its exactness basis (DECISION F295 D7).

    Read from the job's persisted budget actuals; raises ``BudgetCounterError``
    on a damaged record. A job with no actuals reads ``value_usd`` null and
    ``basis`` ``absent``.
    """
    if plan.budget_actuals is None:
        return {"value_usd": None, "basis": cost_exactness_basis(None, 0)}
    decoded = decode_persisted_budget_actuals(
        plan.budget_actuals, first_running_at=plan.first_running_at or None)
    value_usd = decoded["measured_cost_usd"]
    return {"value_usd": value_usd,
            "basis": cost_exactness_basis(value_usd, decoded["unpriced_call_count"])}


def _existing_file(path: Path) -> str | None:
    """*path* as a string when it is a file on disk, else None."""
    return str(path) if path.is_file() else None


def _job_evidence(plan: JobPlan) -> dict[str, Any]:
    """References to one job's evidence (DECISION F295 D7): absolute paths that exist, or null."""
    job_id = str(plan.job_id)
    evidence_dir = job_evidence_dir(job_id)
    return {
        "evidence_dir": str(evidence_dir) if evidence_dir.is_dir() else None,
        "run_ids": list(plan.run_refs),
        "postmortem_path": (_existing_file(evidence_dir / plan.postmortem_path)
                            if plan.postmortem_path else None),
        "run_manifest_path": (_existing_file(evidence_dir / plan.run_manifest_path)
                              if plan.run_manifest_path else None),
        "result_diff_path": (_existing_file(job_dir(job_id) / plan.result_diff_path)
                             if plan.result_diff_path else None),
        "result_diff_sha256": plan.result_diff_sha256 or None,
    }


def _card_task(task: TaskEntry) -> dict[str, Any]:
    """One task of an approval card; a task whose test command never ran reads `test_ran` false."""
    return {
        "task_id": task.task_id,
        "title": task.title,
        "reviewer_verdict": task.reviewer_verdict or None,
        "repair_rounds_used": task.repair_rounds_used,
        "test_ran": task.test_passed is not None,
        "test_passed": task.test_passed,
    }


# WHY: a client approves a result on what the records hold, never on a model's summary
# (F304 T005, DECISION F304 D10).
def _approval_card(plan: JobPlan) -> dict[str, Any] | None:
    """A completed job's approval card, read from its record only; None for any other job.

    The changed files are the paths its tasks' applied manifests name, sorted, the first
    `APPROVAL_CARD_FILE_LIMIT` of them by name and all of them by count.
    """
    if plan.state != JOB_COMPLETED:
        return None
    changed_files = _reviewed_task_files(plan)
    test_command = plan.execution_config.test_command if plan.execution_config else ""
    return {
        "changed_file_count": len(changed_files),
        "changed_files": changed_files[:APPROVAL_CARD_FILE_LIMIT],
        "test_command": test_command or None,
        "tasks": [_card_task(task) for task in plan.tasks],
    }


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
    """The `client` object's version-1 frame (DECISION F295 D4 (2), (3); D5; D7); reads only, never writes.

    Projects sorted by slug, each with its missions newest first
    (``list_missions_safe``'s own order); jobs sorted by job id
    (``list_job_plans_safe``'s own order gives the plans, this function
    sorts them); ``awaiting_apply`` sorted. ``decisions`` holds every open
    decision of every job, sorted by job id then decision id (DECISION
    F295 D5). Each project carries ``cost_today`` for the UTC day of
    ``read_at`` and each job its ``cost`` and ``evidence`` (DECISION F295
    D7), and its ``approval_card``, null unless the job is completed
    (DECISION F304 D10). ``degraded`` and ``skipped_files`` gather what the listing
    functions and the per-job and per-project reads could not read, named
    exactly as they return them, plus ``decisions of job <job_id>``,
    ``cost of job <job_id>`` and ``cost of the day of project
    <project_id>`` for a read that failed; the value that read would have
    filled is null.
    """
    when = now if now is not None else datetime.now(timezone.utc)
    day_moment = (when if when.tzinfo is not None
                  else when.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)

    degraded = False
    skipped_files: list[str] = []

    # R-1144: the read-only projection, never `list_projects`, which migrates a legacy record on read.
    projects = sorted(_list_projects_readonly(), key=lambda p: p.slug or "")
    project_entries: list[dict[str, Any]] = []
    mission_id_by_job_id: dict[str, str] = {}
    abandoned_job_ids: set[str] = set()
    for project in projects:
        project_id = str(project.id)
        missions, mission_degraded, mission_skipped = list_missions_safe(project_id)
        degraded = degraded or mission_degraded
        skipped_files.extend(mission_skipped)
        try:
            cost_today: dict[str, Any] | None = project_cost_of_day(project.id, day_moment)
        except _LEDGER_READ_ERRORS:
            cost_today = None
            degraded = True
            skipped_files.append(f"cost of the day of project {project_id}")
        project_entries.append({
            "project_id": project_id,
            "slug": project.slug or "",
            "missions": [_mission_entry(m) for m in missions],
            "cost_today": cost_today,
        })
        # Built once here, never one scan per job below.
        for mission in missions:
            for job_id in mission.job_ids():
                mission_id_by_job_id[job_id] = mission.id
                if mission.status == MISSION_STATUS_ABANDONED:
                    abandoned_job_ids.add(job_id)

    plans, jobs_degraded, jobs_skipped = list_job_plans_safe()
    degraded = degraded or jobs_degraded
    skipped_files.extend(jobs_skipped)

    job_entries: list[dict[str, Any]] = []
    awaiting_apply: list[str] = []
    decision_entries: list[dict[str, Any]] = []
    for plan in sorted(plans, key=lambda p: str(p.job_id)):
        job_id = str(plan.job_id)
        state = plan.state.value
        # DECISION F304 D5: a declined result, and a job of an abandoned mission, waits for nothing.
        waits_for_apply = (plan.state == JOB_COMPLETED and not job_apply_landed(job_id)
                           and job_result_decline(plan) is None
                           and job_id not in abandoned_job_ids)
        if waits_for_apply:
            awaiting_apply.append(job_id)
        try:
            cost: dict[str, Any] | None = _job_cost(plan)
        except BudgetCounterError:
            cost = None
            degraded = True
            skipped_files.append(f"cost of job {job_id}")
        job_entries.append({
            "job_id": job_id,
            "project_id": plan.project_id,
            "mission_id": mission_id_by_job_id.get(job_id),
            "title": plan.job_title,
            "state": state,
            "waits_for_apply": waits_for_apply,
            "cost": cost,
            "evidence": _job_evidence(plan),
            "approval_card": _approval_card(plan),
        })
        try:
            events = load_run_events(resolve_data_root(), plan.job_id)
            for decision in list_decisions(plan, events):
                if decision.status == "open":
                    decision_entries.append(
                        _decision_entry(job_id, plan.project_id, decision, when))
        except _DECISION_READ_ERRORS:
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
