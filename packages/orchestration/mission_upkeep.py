"""F301 T002, DECISION F301 D1 — a project's upkeep ledger: what its missions' jobs left behind.

One append-only JSON-lines file per project, ``<data root>/projects/<project_id>/upkeep_ledger.jsonl``,
beside ``bench_history.jsonl``. Every line carries ``version``, ``kind``, ``recorded_at`` and
``mission_id``. A ``job_closed`` line is written ONCE per job of a mission, when the job has ended
completed, failed or cancelled, by :func:`record_closed_jobs`, which runs before the mission's
next job is made; ``run_job`` writes nothing here, because it may not grow (the structure rule).

Which findings a job leaves open is one fixed rule: every finding of its ``final_job_review.json``
and the last-round reviewer findings of each blocked task, keyed by job, task and id, because no
finding id is stable across jobs. A finding stays open until an upkeep job that carried it ends
completed; that job's own ``job_closed`` line names it in ``resolved``. Nothing else resolves one.
The mission, job and task records gain nothing: an upkeep job is known by the key
:data:`UPKEEP_METADATA_KEY` of its job's free metadata.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import job_dir, projects_dir

#: The ledger's file name under a project's own data folder (DECISION F301 D1 (2)).
UPKEEP_LEDGER_FILENAME = "upkeep_ledger.jsonl"
#: Stamped on every line, so a later shape is readable beside this one.
UPKEEP_LEDGER_VERSION = 1
#: The job-metadata key that marks an upkeep job and holds what it was planned to carry.
UPKEEP_METADATA_KEY = "mission_upkeep"

#: The line kinds the ledger holds (DECISION F301 D1 (2)).
LINE_JOB_CLOSED = "job_closed"
LINE_UPKEEP_PLANNED = "upkeep_planned"
LINE_UPKEEP_SKIPPED = "upkeep_skipped"
LINE_UPKEEP_NOT_NEEDED = "upkeep_not_needed"
UPKEEP_LINE_KINDS = (LINE_JOB_CLOSED, LINE_UPKEEP_PLANNED, LINE_UPKEEP_SKIPPED,
                     LINE_UPKEEP_NOT_NEEDED)

#: A job in one of these states has ended and gets its ``job_closed`` line.
CLOSED_JOB_STATES = ("completed", "failed", "cancelled")
#: The round hygiene rule's id for an added file that sits beside the one it replaces.
REPLACED_FINDING_PREFIX = "HYG-replaced-"


def upkeep_ledger_path(project_id: str, root: Path | None = None) -> Path:
    """``<data root>/projects/<project_id>/upkeep_ledger.jsonl``."""
    return projects_dir(root) / str(project_id) / UPKEEP_LEDGER_FILENAME


def append_upkeep_line(project_id: str, mission_id: str, kind: str, body: dict[str, Any],
                       root: Path | None = None, *, now: datetime | None = None) -> dict[str, Any]:
    """Append one line and answer it. Never rewrites, never truncates, never reorders."""
    if kind not in UPKEEP_LINE_KINDS:
        raise ValueError(f"not an upkeep ledger line kind: {kind!r}")
    line = {**body, "version": UPKEEP_LEDGER_VERSION, "kind": kind, "mission_id": mission_id,
            "recorded_at": (now or datetime.now(timezone.utc)).isoformat()}
    path = upkeep_ledger_path(project_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, sort_keys=True) + "\n")
    return line


def read_upkeep_ledger(project_id: str, root: Path | None = None) -> list[dict[str, Any]]:
    """Every line, in file order. A torn or unreadable line is SKIPPED, as the loop's ledger does."""
    path = upkeep_ledger_path(project_id, root)
    if not path.is_file():
        return []
    lines: list[dict[str, Any]] = []
    for text in path.read_text(encoding="utf-8").splitlines():
        try:
            line = json.loads(text)
        except ValueError:
            continue
        if isinstance(line, dict) and line.get("kind") in UPKEEP_LINE_KINDS:
            lines.append(line)
    return lines


def finding_key(job_id: str, task_id: str, finding_id: str) -> str:
    """``<job_id>:<task_id>:<finding id>``, the task being ``job`` for a job-level finding."""
    return f"{job_id}:{task_id or 'job'}:{finding_id}"


def _final_review_findings(job_id: str, root: Path | None) -> list[dict[str, Any]]:
    path = job_dir(job_id, root) / "final_job_review.json"
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    found = review.get("findings") if isinstance(review, dict) else None
    if not isinstance(found, list):
        return []
    return [{"key": finding_key(job_id, str(f.get("task_id") or ""), str(f.get("id", ""))),
             "source": "final_review", "finding_id": str(f.get("id", "")),
             "severity": str(f.get("severity", "")), "file": "",
             "summary": str(f.get("message", "")), "task_id": str(f.get("task_id") or "")}
            for f in found if isinstance(f, dict)]


def job_open_findings(job: Any, root: Path | None = None) -> list[dict[str, Any]]:
    """The findings a job left open, by DECISION F301 D1 (3): its final review's, then its
    blocked tasks' last-round reviewer findings, in task order."""
    from packages.orchestration.pingpong_job import collect_blocked_task_findings

    job_id = str(job.job_id)
    findings = _final_review_findings(job_id, root)
    for entry in collect_blocked_task_findings(job, full=True):
        task_id = str(entry.get("task_id", ""))
        for f in entry.get("findings", []):
            findings.append({"key": finding_key(job_id, task_id, str(f.get("id", ""))),
                             "source": "review", "finding_id": str(f.get("id", "")),
                             "severity": str(f.get("severity", "")), "file": str(f.get("file", "")),
                             "summary": str(f.get("summary", "")), "task_id": task_id})
    return findings


def replaced_pairs_from_findings(findings: list[dict[str, Any]]) -> list[dict[str, str]]:
    """The ``{path, original}`` pairs of the round hygiene rule's replaced-file findings."""
    from packages.orchestration.contract_hygiene import replaced_originals

    pairs: list[dict[str, str]] = []
    for f in findings:
        if not f["finding_id"].startswith(REPLACED_FINDING_PREFIX) or not f["file"]:
            continue
        original = next((o for o in replaced_originals(f["file"])
                         if f"added beside {o}," in f["summary"]), "")
        if original:
            pairs.append({"path": f["file"], "original": original})
    return pairs


def _carried_keys(job: Any) -> list[str]:
    planned = (getattr(job, "metadata", None) or {}).get(UPKEEP_METADATA_KEY)
    keys = planned.get("findings") if isinstance(planned, dict) else None
    return [str(k) for k in keys] if isinstance(keys, list) else []


def record_closed_jobs(project_id: str, mission_id: str, root: Path | None = None, *,
                       now: datetime | None = None) -> list[dict[str, Any]]:
    """Write the ``job_closed`` line of every ended job of the mission that has none yet.

    In link order. A job whose record cannot be read is passed over and tried again next time.
    Answers the lines written.
    """
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import load_job_plan_safe

    mission = load_mission(project_id, mission_id, root)
    seen = {line.get("job_id") for line in read_upkeep_ledger(project_id, root)
            if line.get("kind") == LINE_JOB_CLOSED}
    written: list[dict[str, Any]] = []
    for job_id in mission.job_ids():
        if job_id in seen:
            continue
        try:
            job, _unreadable = load_job_plan_safe(normalize_job_id(job_id), root)
        except ValueError:
            continue
        if job is None:
            continue
        state = str(getattr(job.state, "value", job.state))
        if state not in CLOSED_JOB_STATES:
            continue
        findings = job_open_findings(job, root)
        resolved = _carried_keys(job) if state == "completed" else []
        written.append(append_upkeep_line(project_id, mission.id, LINE_JOB_CLOSED, {
            "job_id": job_id, "job_state": state, "open_findings": findings,
            "replaced": replaced_pairs_from_findings(findings), "resolved": resolved,
        }, root, now=now))
        seen.add(job_id)
    return written


def open_findings(lines: list[dict[str, Any]], mission_id: str | None = None) -> list[dict[str, Any]]:
    """The findings still open, oldest first, each once; only one mission's when it is named."""
    resolved = {key for line in lines if line.get("kind") == LINE_JOB_CLOSED
                for key in line.get("resolved", [])}
    found: list[dict[str, Any]] = []
    keys: set[str] = set()
    for line in lines:
        if line.get("kind") != LINE_JOB_CLOSED:
            continue
        if mission_id is not None and line.get("mission_id") != mission_id:
            continue
        for finding in line.get("open_findings", []):
            key = finding.get("key")
            if key in resolved or key in keys:
                continue
            keys.add(key)
            found.append({**finding, "job_id": line.get("job_id", "")})
    return found
