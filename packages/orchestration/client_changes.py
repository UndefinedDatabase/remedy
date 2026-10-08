"""What changed since a cursor a machine client holds (F253, DECISION F253 D4 (2)).

A client reads the digest once (`packages.orchestration.client_digest.build_client_digest`) and
then asks this module what changed since that read, rather than reading the whole digest again —
measured at 7.7 seconds over 11,654 jobs on the operator's own data root. A record CHANGED when
its file's modification time is at or after the cursor less `CLIENT_CHANGES_OVERLAP_SECONDS`: a
job when its `job.json`, a file of its run log or one of its apply records changed; a mission
when its own record changed. The overlap covers a write that lands between two reads at the same
second. This module reads only and never writes.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.client_digest import _mission_entry, build_client_digest
from packages.orchestration.data_paths import job_record_path, jobs_dir, resolve_data_root, run_log_dir
from packages.orchestration.decision_queue import budget_stop_answer, list_decisions
from packages.orchestration.job_apply import _job_apply_records_dir
from packages.orchestration.mission_state import list_missions_safe, mission_dir_for_project
from packages.orchestration.pingpong_job import load_job_plan_safe
from packages.orchestration.project_registry import _list_projects_readonly
from packages.orchestration.timeline import load_run_events

#: D4 (2): a write that lands within this many seconds of a cursor is still reported, so a record
#: saved in the same second as a read that just finished is never silently missed on the next one.
CLIENT_CHANGES_OVERLAP_SECONDS = 5

#: What one job's decision read raises on a bad record — the same tuple
#: `client_digest._DECISION_READ_ERRORS` names, for the same reason: a run log that cannot be
#: read, a line that is not UTF-8 or not JSON or a decision that fails its evidence gate
#: (`ValueError`), a line that is JSON but not an object, and timestamps of mixed types.
_DECISION_READ_ERRORS = (OSError, ValueError, AttributeError, TypeError)

#: What an apply record's read raises on a bad file: a file that cannot be opened, and JSON that
#: will not parse.
_APPLY_READ_ERRORS = (OSError, json.JSONDecodeError)


def parse_client_cursor(text: str) -> datetime:
    """One client cursor: an ISO 8601 time with an offset, or a trailing ``Z`` read as ``+00:00``.

    This repository's local Python is 3.10, whose ``datetime.fromisoformat`` does not accept a
    trailing ``Z`` itself (DECISION F253 D4 (2)). A naive time, an empty string or anything else
    that is not an ISO 8601 time raises ``ValueError``.
    """
    if not text:
        raise ValueError("the cursor is empty")
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"the cursor carries no UTC offset: {text!r}")
    return parsed


def _as_utc(when: datetime) -> datetime:
    """*when*, timezone-aware: an offsetless time is read as UTC."""
    return when if when.tzinfo is not None else when.replace(tzinfo=timezone.utc)


def _mtime_at_or_after(path: Path, cutoff: datetime) -> bool:
    """True when *path* is a file whose modification time is at or after *cutoff*."""
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return False
    return datetime.fromtimestamp(mtime, tz=timezone.utc) >= cutoff


def _parsed_time(value: str | None) -> datetime | None:
    """*value* as a timezone-aware datetime, or None when it is empty or does not parse."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return _as_utc(parsed)


def _changed_job_ids_and_applies(
    cutoff: datetime,
) -> tuple[set[str], list[dict[str, Any]], bool, list[str]]:
    """Job ids changed by their own record or their run log, the apply records that changed (and
    the job ids they add), `degraded`, and `skipped_files` — one pass each over `jobs/` and
    `job_apply_records/`.
    """
    degraded = False
    skipped_files: list[str] = []
    changed_job_ids: set[str] = set()

    jdir = jobs_dir()
    if jdir.is_dir():
        for job_path in sorted(jdir.iterdir()):
            if not job_path.is_dir():
                continue
            job_id = job_path.name
            if _mtime_at_or_after(job_record_path(job_id), cutoff):
                changed_job_ids.add(job_id)
                continue
            log_dir = run_log_dir(job_id)
            if log_dir.is_dir() and any(
                    _mtime_at_or_after(p, cutoff) for p in log_dir.iterdir() if p.is_file()):
                changed_job_ids.add(job_id)

    applies: list[dict[str, Any]] = []
    apply_base = _job_apply_records_dir()
    if apply_base.is_dir():
        for job_path in sorted(apply_base.iterdir()):
            if not job_path.is_dir():
                continue
            job_id = job_path.name
            for record_path in sorted(job_path.glob("*.json")):
                if not _mtime_at_or_after(record_path, cutoff):
                    continue
                changed_job_ids.add(job_id)
                try:
                    data = json.loads(record_path.read_text(encoding="utf-8"))
                except _APPLY_READ_ERRORS:
                    data = None
                if not isinstance(data, dict):
                    degraded = True
                    skipped_files.append(f"apply record {record_path.name} of job {job_id}")
                    continue
                applies.append({
                    "job_id": job_id,
                    "job_apply_id": str(data.get("job_apply_id", record_path.stem)),
                    "status": data.get("status"),
                    "finished_at": data.get("finished_at"),
                })

    return changed_job_ids, applies, degraded, skipped_files


def _closed_decisions_for_job(job_id: str, cutoff: datetime) -> tuple[list[dict[str, Any]], bool, list[str]]:
    """Every decision of *job_id* resolved at or after *cutoff*, `degraded`, and `skipped_files`.

    A decision carries a `resolved_at` only once answered; most derivations omit it while open and
    never add it once answered (budget decisions leave the open-decision list instead of gaining a
    resolved entry there), so the budget stop's own answer record, read by `budget_stop_answer`,
    is checked beside `list_decisions`'s own resolved entries.
    """
    degraded = False
    skipped_files: list[str] = []
    closed: list[dict[str, Any]] = []

    plan, plan_degraded = load_job_plan_safe(job_id)
    if plan is None:
        if plan_degraded:
            degraded = True
            skipped_files.append(f"closed decisions of job {job_id}")
        return closed, degraded, skipped_files

    try:
        events = load_run_events(resolve_data_root(), job_id)
    except _DECISION_READ_ERRORS:
        degraded = True
        skipped_files.append(f"closed decisions of job {job_id}")
        events = []
    else:
        try:
            for decision in list_decisions(plan, events):
                resolved = _parsed_time(decision.resolved_at)
                if resolved is not None and resolved >= cutoff:
                    closed.append({"job_id": job_id, "decision_id": decision.id,
                                   "resolved_at": decision.resolved_at})
        except _DECISION_READ_ERRORS:
            degraded = True
            skipped_files.append(f"closed decisions of job {job_id}")

    answer = budget_stop_answer(plan)
    if answer is not None:
        resolved = _parsed_time(str(answer.get("answered_at", "")))
        if resolved is not None and resolved >= cutoff:
            closed.append({"job_id": job_id, "decision_id": str(answer.get("decision_id", "")),
                           "resolved_at": str(answer.get("answered_at", ""))})
    return closed, degraded, skipped_files


def _changed_missions(cutoff: datetime) -> tuple[list[dict[str, Any]], bool, list[str]]:
    """Every mission whose record changed at or after *cutoff*, as the digest's own mission
    object with its `project_id`; `degraded` and `skipped_files`."""
    degraded = False
    skipped_files: list[str] = []
    missions: list[dict[str, Any]] = []

    for project in _list_projects_readonly():
        project_id = str(project.id)
        project_missions, mission_degraded, mission_skipped = list_missions_safe(project_id)
        degraded = degraded or mission_degraded
        skipped_files.extend(mission_skipped)
        mission_dir = mission_dir_for_project(project_id)
        if not mission_dir.is_dir():
            continue
        for mission in project_missions:
            path = mission_dir / f"{mission.id}.json"
            if _mtime_at_or_after(path, cutoff):
                missions.append({"project_id": project_id, **_mission_entry(mission)})

    missions.sort(key=lambda m: (m["project_id"], m["mission_id"]))
    return missions, degraded, skipped_files


# DECISION F253 D4 (2): the one builder `remedy client changes` and its HTTP twin both call.
def build_client_changes(since: datetime | None, now: datetime | None = None) -> dict[str, Any]:
    """What changed since *since*, less the overlap; reads only, never writes.

    Without *since* every list is empty and `cursor` is the time of this read. With it, `jobs`
    and `decisions` are `build_client_digest`'s own, for the jobs whose `job.json`, a run-log file
    or an apply record changed at or after `since` minus `CLIENT_CHANGES_OVERLAP_SECONDS`;
    `closed_decisions` names each decision of a changed job resolved at or after that time;
    `missions` lists each mission whose record changed; `applies` lists each apply record that
    changed. An item may be listed on two reads in a row, kept by a client by its id.
    """
    when = _as_utc(now) if now is not None else datetime.now(timezone.utc)
    read_at = when.isoformat()

    if since is None:
        return {
            "read_at": read_at,
            "cursor": read_at,
            "since": None,
            "overlap_seconds": CLIENT_CHANGES_OVERLAP_SECONDS,
            "jobs": [],
            "decisions": [],
            "closed_decisions": [],
            "missions": [],
            "applies": [],
            "degraded": False,
            "skipped_files": [],
        }

    cutoff = _as_utc(since) - timedelta(seconds=CLIENT_CHANGES_OVERLAP_SECONDS)
    degraded = False
    skipped_files: list[str] = []

    changed_job_ids, applies, applies_degraded, applies_skipped = _changed_job_ids_and_applies(cutoff)
    degraded = degraded or applies_degraded
    skipped_files.extend(applies_skipped)

    digest = build_client_digest(now=when, job_ids=sorted(changed_job_ids))
    degraded = degraded or digest["degraded"]
    skipped_files.extend(digest["skipped_files"])

    closed_decisions: list[dict[str, Any]] = []
    for job_id in sorted(changed_job_ids):
        closed, job_degraded, job_skipped = _closed_decisions_for_job(job_id, cutoff)
        closed_decisions.extend(closed)
        degraded = degraded or job_degraded
        skipped_files.extend(job_skipped)
    closed_decisions.sort(key=lambda d: (d["job_id"], d["decision_id"]))

    missions, missions_degraded, missions_skipped = _changed_missions(cutoff)
    degraded = degraded or missions_degraded
    skipped_files.extend(missions_skipped)

    return {
        "read_at": read_at,
        "cursor": read_at,
        "since": since.isoformat(),
        "overlap_seconds": CLIENT_CHANGES_OVERLAP_SECONDS,
        "jobs": digest["jobs"],
        "decisions": digest["decisions"],
        "closed_decisions": closed_decisions,
        "missions": missions,
        "applies": applies,
        "degraded": degraded,
        "skipped_files": skipped_files,
    }
