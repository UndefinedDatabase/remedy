"""The `client` object's version-1 frame in `remedy status --json` (DECISION F295 D4, D5, D7).

Version 1 carries every registered project with its missions and its cost of
the day, every job on the data root that still needs something and the jobs
that ended last, with how many ended jobs it left out (DECISION F304 D16),
each with its measured cost and its evidence
references (DECISION F295 D7), the provider calls and tokens by kind that the
project ledgers hold for each job and each project's day (DECISION F304 D13),
which of those jobs wait for an operator's apply, whether the supervisor
answers, and every job's open decisions (DECISION F295 D5). Each completed
job carries its approval card, what an operator approves its result on, read
from the job's record and its mission's contract only, with one
recommendation word and one risk word derived from them by fixed rules
(DECISIONs F304 D10 to D12).
"""
from __future__ import annotations

import sqlite3
from collections.abc import Collection
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.budget_guard import BudgetCounterError, decode_persisted_budget_actuals
from packages.orchestration.data_paths import job_dir, job_evidence_dir, resolve_data_root
from packages.orchestration.decision_queue import HumanDecision, list_decisions
from packages.orchestration.escalation import DECISION_TYPE_TASK_DECISION
from packages.orchestration.job_apply import job_apply_landed, job_result_decline
from packages.orchestration.job_digest import cost_exactness_basis
from packages.orchestration.mission_contract import (
    CRITERION_STATUS_UNCHECKED,
    ContractError,
    read_mission_contract,
)
from packages.orchestration.mission_state import MISSION_STATUS_ABANDONED, Mission, list_missions_safe
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JobPlan,
    TaskEntry,
    _reviewed_task_files,
    job_is_terminal,
    list_job_plans_safe,
    load_job_plan_safe,
)
from packages.orchestration.project_cockpit import project_cost_of_day
from packages.orchestration.project_registry import _list_projects_readonly
from packages.orchestration.serve_daemon import socket_answers
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.timeline import load_run_events
from packages.orchestration.token_ledger import CostRow, ledger_usage_by_job, query_cost

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

#: The words an approval card's `recommendation` and `risk` take, from the most to the least
#: favourable; `_card_recommendation` and `_card_risk` state the rules (DECISION F304 D12).
APPROVAL_RECOMMENDATIONS = ("apply", "review", "hold")
APPROVAL_RISKS = ("low", "medium", "high")

#: The most changed files an approval card's risk may still read `low` (DECISION F304 D12).
APPROVAL_LOW_RISK_FILE_LIMIT = 5

#: How many ended jobs the digest lists by default, those that ended last (DECISION F304 D16).
CLIENT_DIGEST_ENDED_JOB_LIMIT = 20


def _job_ended(plan: JobPlan, waits_for_apply: bool, open_decision_count: int) -> bool:
    """True when nothing is left to do about the job: its state is terminal, it does not wait for
    its apply and no decision of it is open. Every other job still needs something (DECISION F304
    D16)."""
    return job_is_terminal(plan.state) and not waits_for_apply and open_decision_count == 0


def _ended_at(plan: JobPlan) -> str:
    """When the job ended, for ordering ended jobs: its `finished_at`, else its `created_at`."""
    return plan.finished_at or plan.created_at


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


def _tokens_by_kind(row: CostRow | None) -> dict[str, int | None]:
    """A ledger total's tokens by kind (DECISION F304 D13); a kind no call reported is null."""
    return {
        "input": row.tokens_in if row is not None else None,
        "output": row.tokens_out if row is not None else None,
        "cache_read": row.cache_read if row is not None else None,
        "cache_creation": row.cache_write if row is not None else None,
    }


def _known_sum(first: int | None, second: int | None) -> int | None:
    """Two ledger figures added; null only when neither ledger reported one."""
    if first is None or second is None:
        return second if first is None else first
    return first + second


def _merged_usage(first: CostRow, second: CostRow) -> CostRow:
    """One job's totals from two project ledgers, added, a figure neither reported staying null."""
    return CostRow(calls=first.calls + second.calls,
                   tokens_in=_known_sum(first.tokens_in, second.tokens_in),
                   tokens_out=_known_sum(first.tokens_out, second.tokens_out),
                   cache_read=_known_sum(first.cache_read, second.cache_read),
                   cache_write=_known_sum(first.cache_write, second.cache_write))


def _day_tokens(project_id: Any, moment: datetime) -> dict[str, int | None]:
    """The project's ledger tokens by kind on *moment*'s UTC day, the day `cost_today` reads."""
    day = moment.date()
    report = query_cost(project_id=project_id, since=day.isoformat(),
                        until=(day + timedelta(days=1)).isoformat())
    return _tokens_by_kind(report.total)


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


def _mission_blocking_criteria(mission: Mission | None) -> list[dict[str, Any]]:
    """The blocking criteria of *mission*'s contract with their id, text and status, in contract
    order (DECISION F304 D11); none without a mission or a contract. Raises ``ContractError`` on a
    contract that cannot be read.
    """
    contract = read_mission_contract(mission) if mission is not None else None
    return [{"id": criterion.id, "text": criterion.text, "status": criterion.status}
            for criterion in (contract.criteria if contract is not None else ()) if criterion.blocking]


# WHY: the two words are derived from recorded facts by fixed rules, which the machine client page
# states, so a client can check every word against the card it stands on (DECISION F304 D12).
def _card_recommendation(tasks: list[dict[str, Any]],
                         blocking_criteria: list[dict[str, Any]] | None, checks_ran: bool) -> str:
    """`hold` when a record says no: a test that ran and failed, a reviewer's verdict other than
    `pass`, or an `unmet` blocking criterion. Else `review` when something is unverified: no check
    ran, a task without a reviewer's verdict, a blocking criterion still `open` or `unchecked`
    (DECISION F299 D2 (5)), or a contract that cannot be read. Else `apply`.
    """
    if (any(task["test_passed"] is False for task in tasks)
            or any(task["reviewer_verdict"] not in (None, "pass") for task in tasks)
            or any(criterion["status"] == "unmet" for criterion in blocking_criteria or ())):
        return "hold"
    if (not checks_ran or blocking_criteria is None
            or any(task["reviewer_verdict"] is None for task in tasks)
            or any(criterion["status"] in ("open", CRITERION_STATUS_UNCHECKED)
                   for criterion in blocking_criteria)):
        return "review"
    return "apply"


def _card_risk(tasks: list[dict[str, Any]], changed_file_count: int, checks_ran: bool) -> str:
    """`high` when no check ran or more files changed than the card names
    (`APPROVAL_CARD_FILE_LIMIT`). Else `medium` when a task took a repair round or more than
    `APPROVAL_LOW_RISK_FILE_LIMIT` files changed. Else `low`.
    """
    if not checks_ran or changed_file_count > APPROVAL_CARD_FILE_LIMIT:
        return "high"
    if (any(task["repair_rounds_used"] > 0 for task in tasks)
            or changed_file_count > APPROVAL_LOW_RISK_FILE_LIMIT):
        return "medium"
    return "low"


# WHY: a client approves a result on what the records hold, never on a model's summary
# (F304 T005, DECISIONs F304 D10 to D12).
def _approval_card(plan: JobPlan, blocking_criteria: list[dict[str, Any]] | None) -> dict[str, Any]:
    """A completed job's approval card, read from its record and its mission's contract only.

    The changed files are the paths its tasks' applied manifests name, sorted, the first
    `APPROVAL_CARD_FILE_LIMIT` of them by name and all of them by count. `blocking_criteria` is
    null when the mission's contract cannot be read. A check ran when a task's test command ran or
    a gate evaluated a blocking criterion, `met` or `unmet`; `checks_ran` false says none did. The
    `recommendation` and the `risk` follow from those facts alone.
    """
    changed_files = _reviewed_task_files(plan)
    test_command = plan.execution_config.test_command if plan.execution_config else ""
    tasks = [_card_task(task) for task in plan.tasks]
    checks_ran = (any(task["test_ran"] for task in tasks)
                  or any(criterion["status"] in ("met", "unmet")
                         for criterion in blocking_criteria or ()))
    return {
        "changed_file_count": len(changed_files),
        "changed_files": changed_files[:APPROVAL_CARD_FILE_LIMIT],
        "test_command": test_command or None,
        "tasks": tasks,
        "blocking_criteria": blocking_criteria,
        "checks_ran": checks_ran,
        "recommendation": _card_recommendation(tasks, blocking_criteria, checks_ran),
        "risk": _card_risk(tasks, len(changed_files), checks_ran),
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
    """One mission's DECISION F295 D4 (2) shape; an order given as text leaves two keys empty.

    DECISION F301 D5 adds the mission's upkeep counts: the setting, the completed jobs left before
    the next upkeep job, and the open findings it would carry, each ``None`` when unreadable.
    """
    from packages.orchestration.mission_upkeep import upkeep_digest_counts

    order = mission.order
    upkeep = upkeep_digest_counts(mission.project_id, mission.id)
    return {
        "mission_id": mission.id,
        "status": mission.status,
        "goal": mission.goal,
        "job_ids": list(mission.job_ids()),
        "order_source_path": order.source_path if order is not None else "",
        "order_source_sha256": order.source_sha256 if order is not None else "",
        "upkeep_every": upkeep["every"],
        "upkeep_jobs_left": upkeep["jobs_left"],
        "upkeep_open_findings": upkeep["open_findings"],
    }


def _job_entry(plan: Any, mission: Mission | None, waits_for_apply: bool,
               cost: dict[str, Any] | None, calls: int | None, usage: CostRow | None,
               approval_card: dict[str, Any] | None) -> dict[str, Any]:
    """One job's entry under the digest's `jobs`, from what `build_client_digest` read for it.

    Moved out of `build_client_digest` unchanged, as step (1) of that function's boundary on
    `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D6).
    """
    return {
        "job_id": str(plan.job_id),
        "project_id": plan.project_id,
        "mission_id": mission.id if mission is not None else None,
        "title": plan.job_title,
        "state": plan.state.value,
        "waits_for_apply": waits_for_apply,
        "cost": cost,
        "calls": calls,
        "tokens": _tokens_by_kind(usage),
        "evidence": _job_evidence(plan),
        "approval_card": approval_card,
    }


# DECISION F295 D4 (2): the one builder of the `client` key `_cmd_status` adds to its answer.
def build_client_digest(now: datetime | None = None, *,
                        every_ended_job: bool = False,
                        job_ids: Collection[str] | None = None) -> dict[str, Any]:
    """The `client` object's version-1 frame (DECISION F295 D4 (2), (3); D5; D7); reads only, never writes.

    Projects sorted by slug, each with its missions newest first
    (``list_missions_safe``'s own order); jobs sorted by job id
    (``list_job_plans_safe``'s own order gives the plans, this function
    sorts them); ``awaiting_apply`` sorted. ``jobs`` holds every job that
    still needs something and the ``CLIENT_DIGEST_ENDED_JOB_LIMIT`` ended
    jobs that ended last, or every ended job when *every_ended_job* is
    true; ``job_window`` names that limit, null when every ended job is
    listed, and how many ended jobs it left out (DECISION F304 D16).
    ``decisions`` holds every open
    decision of every job, sorted by job id then decision id (DECISION
    F295 D5). Each project carries ``cost_today`` for the UTC day of
    ``read_at`` and each job its ``cost`` and ``evidence`` (DECISION F295
    D7), the calls and tokens by kind its project ledgers hold (DECISION
    F304 D13), and its ``approval_card``, null unless the job is completed
    (DECISIONs F304 D10 to D12). ``degraded`` and ``skipped_files`` gather
    what the listing functions and the per-job and per-project reads could
    not read, named exactly as they return them, plus ``decisions of job
    <job_id>``, ``cost of job <job_id>``, ``contract of job <job_id>``,
    ``cost of the day of project <project_id>`` and ``calls and tokens of the
    jobs of project <project_id>`` for a read that failed; the value that
    read would have filled is null. ``job_ids``, given, reads only those jobs
    with ``load_job_plan_safe``, an id with no record left out and an
    unreadable one named in ``skipped_files``; ``jobs`` lists every one of
    them, ``decisions`` and ``awaiting_apply`` only theirs, and ``job_window``
    reads ``ended_limit`` null and ``left_out`` 0 (DECISION F253 D4 (1)).
    """
    when = now if now is not None else datetime.now(timezone.utc)
    day_moment = (when if when.tzinfo is not None
                  else when.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)

    degraded = False
    skipped_files: list[str] = []

    # R-1144: the read-only projection, never `list_projects`, which migrates a legacy record on read.
    projects = sorted(_list_projects_readonly(), key=lambda p: p.slug or "")
    project_entries: list[dict[str, Any]] = []
    mission_by_job_id: dict[str, Mission] = {}
    abandoned_job_ids: set[str] = set()
    # DECISION F304 D13: every job's ledger totals, one grouped read per project ledger.
    usage_by_job_id: dict[str, CostRow] = {}
    every_ledger_read = True
    for project in projects:
        project_id = str(project.id)
        missions, mission_degraded, mission_skipped = list_missions_safe(project_id)
        degraded = degraded or mission_degraded
        skipped_files.extend(mission_skipped)
        try:
            cost_today: dict[str, Any] | None = {
                **project_cost_of_day(project.id, day_moment),
                "tokens": _day_tokens(project.id, day_moment),
            }
        except _LEDGER_READ_ERRORS:
            cost_today = None
            degraded = True
            skipped_files.append(f"cost of the day of project {project_id}")
        try:
            for job_id, row in ledger_usage_by_job(project_id=project.id).items():
                kept = usage_by_job_id.get(job_id)
                usage_by_job_id[job_id] = row if kept is None else _merged_usage(kept, row)
        except _LEDGER_READ_ERRORS:
            every_ledger_read = False
            degraded = True
            skipped_files.append(f"calls and tokens of the jobs of project {project_id}")
        project_entries.append({
            "project_id": project_id,
            "slug": project.slug or "",
            "missions": [_mission_entry(m) for m in missions],
            "cost_today": cost_today,
        })
        # Built once here, never one scan per job below.
        for mission in missions:
            for job_id in mission.job_ids():
                mission_by_job_id[job_id] = mission
                if mission.status == MISSION_STATUS_ABANDONED:
                    abandoned_job_ids.add(job_id)

    if job_ids is None:
        plans, jobs_degraded, jobs_skipped = list_job_plans_safe()
        degraded = degraded or jobs_degraded
        skipped_files.extend(jobs_skipped)
    else:
        plans = []
        for job_id in sorted(set(job_ids)):
            plan, plan_degraded = load_job_plan_safe(job_id)
            if plan is None:
                if plan_degraded:
                    degraded = True
                    skipped_files.append(job_id)
                continue
            plans.append(plan)

    job_entries: list[dict[str, Any]] = []
    ended_jobs: list[tuple[str, str, dict[str, Any]]] = []
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
        mission = mission_by_job_id.get(job_id)
        approval_card: dict[str, Any] | None = None
        if plan.state == JOB_COMPLETED:
            try:
                blocking_criteria: list[dict[str, Any]] | None = _mission_blocking_criteria(mission)
            except ContractError:
                blocking_criteria = None
                degraded = True
                skipped_files.append(f"contract of job {job_id}")
            approval_card = _approval_card(plan, blocking_criteria)
        # A job no ledger names made no recorded call, unless a ledger could not be read.
        usage = usage_by_job_id.get(job_id)
        calls = usage.calls if usage is not None else (0 if every_ledger_read else None)
        entry = _job_entry(plan, mission, waits_for_apply, cost, calls, usage, approval_card)
        decisions_before = len(decision_entries)
        decisions_read = True
        try:
            events = load_run_events(resolve_data_root(), plan.job_id)
            for decision in list_decisions(plan, events):
                if decision.status == "open":
                    decision_entries.append(
                        _decision_entry(job_id, plan.project_id, decision, when))
        except _DECISION_READ_ERRORS:
            decisions_read = False
            degraded = True
            skipped_files.append(f"decisions of job {job_id}")
        # A job whose decisions could not be read is never taken for ended (DECISION F304 D16).
        # DECISION F253 D4 (1): a `job_ids`-restricted call lists every requested job as itself,
        # never trimmed into the ended-job window — there is no "ended last" ordering to apply to
        # a caller-chosen set.
        if job_ids is None and decisions_read and _job_ended(
                plan, waits_for_apply, len(decision_entries) - decisions_before):
            ended_jobs.append((_ended_at(plan), job_id, entry))
        else:
            job_entries.append(entry)

    if job_ids is None:
        # DECISION F304 D16: every job that still needs something, and the ended jobs that ended last.
        ended_jobs.sort(key=lambda ended: (ended[0], ended[1]), reverse=True)
        ended_limit = None if every_ended_job else CLIENT_DIGEST_ENDED_JOB_LIMIT
        listed_ended = ended_jobs if ended_limit is None else ended_jobs[:ended_limit]
        job_entries.extend(entry for _ended, _job_id, entry in listed_ended)
        job_window = {"ended_limit": ended_limit, "left_out": len(ended_jobs) - len(listed_ended)}
    else:
        job_window = {"ended_limit": None, "left_out": 0}
    job_entries.sort(key=lambda entry: entry["job_id"])

    return {
        "version": CLIENT_DIGEST_VERSION,
        "read_at": when.isoformat(),
        "supervisor": {"answers": socket_answers(serve_paths().socket)},
        "projects": project_entries,
        "jobs": job_entries,
        "job_window": job_window,
        "awaiting_apply": sorted(awaiting_apply),
        "decisions": sorted(decision_entries, key=lambda e: (e["job_id"], e["decision_id"])),
        "degraded": degraded,
        "skipped_files": skipped_files,
    }
