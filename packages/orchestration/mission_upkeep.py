"""F301 T002, DECISION F301 D1 — a project's upkeep ledger: what its missions' jobs left behind.

One append-only JSON-lines file per project, ``<data root>/projects/<project_id>/upkeep_ledger.jsonl``,
beside ``bench_history.jsonl``. Every line carries ``version``, ``kind``, ``recorded_at`` and
``mission_id``. A ``job_closed`` line is written ONCE per job of a mission, when the job has ended
completed, failed or cancelled, or has halted blocked or stopped and a later job of the mission is
linked, by :func:`record_closed_jobs`, which runs before the mission's next job is made;
``run_job`` writes nothing here, because it may not grow (the structure rule).

Which findings a job leaves open is one fixed rule: every finding of its ``final_job_review.json``
and the last-round reviewer findings of each blocked task, keyed by job, task and id, because no
finding id is stable across jobs. A finding stays open until an upkeep job that carried it ends
completed; that job's own ``job_closed`` line names it in ``resolved``. Nothing else resolves one.
The mission, job and task records gain nothing: an upkeep job is known by the key
:data:`UPKEEP_METADATA_KEY` of its job's free metadata.

F301 T003 adds the cadence: after ``mission.upkeep_every`` completed jobs of a mission (default
5), :func:`make_upkeep_job_if_due` makes the mission's next job an upkeep job whose one step
:func:`compile_upkeep_step` writes from the ledger by fixed rules, or records that nothing was
left to clean up; :func:`record_upkeep_skip` is the one way to skip it, with a reason.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
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
#: A job halted in one of these states counts as ended once a later job of its mission is linked,
#: because the mission has moved on past it (R-1234, DECISION F301 D4).
HALTED_JOB_STATES = ("blocked", "stopped")
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

    In link order. A job ends completed, failed or cancelled; a job halted blocked or stopped counts
    as ended once a later job is linked, because the mission has moved on past it (R-1234). A job
    whose record cannot be read is passed over and tried again next time.
    Answers the lines written.
    """
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.pingpong_job import load_job_plan_safe

    mission = load_mission(project_id, mission_id, root)
    seen = {line.get("job_id") for line in read_upkeep_ledger(project_id, root)
            if line.get("kind") == LINE_JOB_CLOSED}
    written: list[dict[str, Any]] = []
    job_ids = mission.job_ids()
    for index, job_id in enumerate(job_ids):
        if job_id in seen:
            continue
        try:
            job, _unreadable = load_job_plan_safe(normalize_job_id(job_id), root)
        except ValueError:
            continue
        if job is None:
            continue
        state = str(getattr(job.state, "value", job.state))
        moved_on = index < len(job_ids) - 1
        if state not in CLOSED_JOB_STATES and not (moved_on and state in HALTED_JOB_STATES):
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


# ---------------------------------------------------------------------------
# F301 T003, DECISIONs F301 D1 and D3: the cadence, the plan, the upkeep job and the skip
# ---------------------------------------------------------------------------

#: The setting that says after how many completed jobs upkeep is due (DECISION F301 D1 (6)).
UPKEEP_EVERY_KEY = "mission.upkeep_every"
UPKEEP_EVERY_DEFAULT = 5
#: At most this many open findings ride in one upkeep job; the rest wait for the next one.
UPKEEP_MAX_FINDINGS = 5


class UpkeepError(ValueError):
    """An upkeep request the rules refuse: a bad setting, a skip without a reason or with
    nothing due."""


def upkeep_every_setting(config: Any = None) -> int:
    """``mission.upkeep_every``: unset reads 5; a value that is not a whole number of at
    least 1 is refused."""
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    value = config.get(UPKEEP_EVERY_KEY)
    if value is None:
        return UPKEEP_EVERY_DEFAULT
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise UpkeepError(f"{UPKEEP_EVERY_KEY} must be a whole number of at least 1, not {value!r}")
    return value


@dataclass(frozen=True)
class UpkeepCadence:
    """Where a mission stands against its cadence (DECISION F301 D3 (1))."""

    every: int
    completed: int
    after_job_id: str

    @property
    def due(self) -> bool:
        return self.completed >= self.every

    @property
    def jobs_left(self) -> int:
        return max(self.every - self.completed, 0)


def _job_state(job_id: str, root: Path | None) -> str:
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.pingpong_job import load_job_plan_safe

    try:
        job, _unreadable = load_job_plan_safe(normalize_job_id(job_id), root)
    except ValueError:
        return ""
    return "" if job is None else str(getattr(job.state, "value", job.state))


def upkeep_cadence(project_id: str, mission_id: str, root: Path | None = None, *,
                   config: Any = None, lines: list[dict[str, Any]] | None = None) -> UpkeepCadence:
    """Count the mission's completed jobs since its last upkeep slot.

    A slot ends at an upkeep job, and at the job a skip or a not-needed line names as
    ``after_job_id``. The count is the linked jobs after the last such job, in link order, whose
    state is completed; an upkeep job is never among them, because it ends its own slot.
    """
    from packages.orchestration.mission_state import load_mission

    mission = load_mission(project_id, mission_id, root)
    lines = read_upkeep_ledger(project_id, root) if lines is None else lines
    mine = [line for line in lines if line.get("mission_id") == mission.id]
    upkeep_ids = {line.get("job_id") for line in mine if line.get("kind") == LINE_UPKEEP_PLANNED}
    ends = upkeep_ids | {line.get("after_job_id") for line in mine
                         if line.get("kind") in (LINE_UPKEEP_SKIPPED, LINE_UPKEEP_NOT_NEEDED)}
    job_ids = list(mission.job_ids())
    start = max((index + 1 for index, job_id in enumerate(job_ids) if job_id in ends), default=0)
    completed = sum(1 for job_id in job_ids[start:] if _job_state(job_id, root) == "completed")
    return UpkeepCadence(upkeep_every_setting(config), completed, job_ids[-1] if job_ids else "")


def project_repository(project_id: str) -> str:
    """The project's repository folder: ``canonical_repo_path``, else its first ``repo_paths``."""
    from uuid import UUID

    from packages.orchestration.project_registry import ProjectNotFoundError, load_project

    try:
        project = load_project(UUID(str(project_id)))
    except (ValueError, ProjectNotFoundError, OSError):
        return ""
    return project.canonical_repo_path or (project.repo_paths[0] if project.repo_paths else "")


def _structure_item(repository: str) -> dict[str, Any]:
    """The largest Python function and the largest code file above the limits (DECISION F301 D3 (2))."""
    from packages.orchestration.contract_hygiene import CODE_FILE_SUFFIXES
    from packages.orchestration.structure_measure import NotAGitRepository, measure_repository

    if not repository:
        return {"unmeasured": "the project names no repository"}
    try:
        measure = measure_repository(Path(repository))
    except (NotAGitRepository, OSError) as exc:
        return {"unmeasured": f"the repository could not be measured: {exc}"}
    function = measure.large_functions[0] if measure.large_functions else None
    code_files = [f for f in measure.large_files if f.path.endswith(CODE_FILE_SUFFIXES)]
    return {
        "limits": {"function_lines": measure.function_limit, "file_lines": measure.file_limit},
        "largest_function": None if function is None else {
            "path": function.path, "name": function.name, "line": function.line, "lines": function.lines},
        "largest_file": {"path": code_files[0].path, "lines": code_files[0].lines} if code_files else None,
    }


def _replaced_pairs(repository: str, lines: list[dict[str, Any]], mission_id: str) -> list[dict[str, str]]:
    """Every replaced file beside its original, found now or left by a job, while both exist."""
    from packages.orchestration.contract_hygiene import find_replaced_files, replaced_originals
    from packages.orchestration.structure_measure import NotAGitRepository, tracked_files

    if not repository:
        return []
    top = Path(repository)
    pairs: list[dict[str, str]] = []
    try:
        for finding in find_replaced_files(top, tracked_files(top)):
            original = next((o for o in replaced_originals(finding.path) if (top / o).is_file()), "")
            if original:
                pairs.append({"path": finding.path, "original": original})
    except (NotAGitRepository, OSError):
        return []
    for line in lines:
        if line.get("kind") == LINE_JOB_CLOSED and line.get("mission_id") == mission_id:
            pairs.extend(pair for pair in line.get("replaced", [])
                         if (top / pair["path"]).is_file() and (top / pair["original"]).is_file())
    unique: dict[str, dict[str, str]] = {}
    for pair in pairs:
        unique.setdefault(pair["path"], pair)
    return list(unique.values())


def plan_upkeep(project_id: str, mission_id: str, cadence: UpkeepCadence,
                lines: list[dict[str, Any]]) -> dict[str, Any]:
    """What an upkeep job due now would carry, by DECISION F301 D1 (3) to (5) and D3 (2)."""
    repository = project_repository(project_id)
    carried = open_findings(lines, mission_id=mission_id)[:UPKEEP_MAX_FINDINGS]
    return {"after_jobs": cadence.completed, "after_job_id": cadence.after_job_id, "every": cadence.every,
            "repository": repository, "findings": [f["key"] for f in carried], "carried": carried,
            "structure": _structure_item(repository), "replaced": _replaced_pairs(repository, lines, mission_id)}


def upkeep_has_work(plan: dict[str, Any]) -> bool:
    structure = plan["structure"]
    return bool(plan["findings"] or plan["replaced"]
                or structure.get("largest_function") or structure.get("largest_file"))


def compile_upkeep_step(plan: dict[str, Any]) -> str:
    """The upkeep job's one step, in the fixed order of DECISION F301 D1 (8)."""
    count = plan["after_jobs"]
    text = [f"Upkeep after {count} completed job{'' if count == 1 else 's'} of this mission, planned by "
            f"Remedy's fixed rules (DECISION F301 D1)."]
    if plan["carried"]:
        text.append("Repair these findings that earlier jobs left open, oldest first:")
        text.extend(f"- {f['severity']} finding {f['finding_id']} left by job {f['job_id']}"
                    f"{' in ' + f['file'] if f['file'] else ''}: {f['summary']}" for f in plan["carried"])
    structure = plan["structure"]
    if structure.get("largest_function"):
        function, limit = structure["largest_function"], structure["limits"]["function_lines"]
        text.append(f"Shorten the function {function['name']} in {function['path']} (line {function['line']}), "
                    f"{function['lines']} lines against a limit of {limit}, without changing what it does.")
    if structure.get("largest_file"):
        largest, limit = structure["largest_file"], structure["limits"]["file_lines"]
        text.append(f"Shorten the file {largest['path']}, {largest['lines']} lines against a limit of {limit}, "
                    f"without changing what it does.")
    if plan["replaced"]:
        text.append("Delete each file that a newer one replaced:")
        text.extend(f"- {pair['original']}, replaced by {pair['path']}" for pair in plan["replaced"])
    return "\n".join(text)


@dataclass(frozen=True)
class UpkeepOutcome:
    """What one look at the cadence did: the cadence, the plan when due, the job when made, and the
    ledger line written."""

    cadence: UpkeepCadence
    plan: dict[str, Any] | None
    job: Any
    line: dict[str, Any] | None


def make_upkeep_job_if_due(project_id: str, mission_id: str, root: Path | None = None, *,
                           config: Any = None, now: datetime | None = None) -> UpkeepOutcome:
    """Record the ended jobs, then, when upkeep is due, make the upkeep job or record that none
    was needed. The job is an ordinary follow-up job made by ``continue_mission``."""
    from packages.orchestration.mission_state import continue_mission
    from packages.orchestration.pingpong_job import save_job_plan

    record_closed_jobs(project_id, mission_id, root, now=now)
    lines = read_upkeep_ledger(project_id, root)
    cadence = upkeep_cadence(project_id, mission_id, root, config=config, lines=lines)
    if not cadence.due:
        return UpkeepOutcome(cadence, None, None, None)
    plan = plan_upkeep(project_id, mission_id, cadence, lines)
    if not upkeep_has_work(plan):
        line = append_upkeep_line(project_id, mission_id, LINE_UPKEEP_NOT_NEEDED, {
            "after_jobs": cadence.completed, "after_job_id": cadence.after_job_id}, root, now=now)
        return UpkeepOutcome(cadence, plan, None, line)
    job = continue_mission(project_id, mission_id, compile_upkeep_step(plan), root=root, now=now)
    planned = {"job_id": str(job.job_id), "after_jobs": cadence.completed, "after_job_id": cadence.after_job_id,
               "findings": plan["findings"], "structure": plan["structure"], "replaced": plan["replaced"]}
    job.metadata[UPKEEP_METADATA_KEY] = planned
    save_job_plan(job)
    line = append_upkeep_line(project_id, mission_id, LINE_UPKEEP_PLANNED, planned, root, now=now)
    return UpkeepOutcome(cadence, plan, job, line)


def record_upkeep_skip(project_id: str, mission_id: str, reason: str, root: Path | None = None, *,
                       config: Any = None, now: datetime | None = None) -> dict[str, Any]:
    """Record the operator's decision to skip the upkeep job that is due, with its reason."""
    text = str(reason or "").strip()
    if not text:
        raise UpkeepError("a skipped upkeep job needs its reason")
    record_closed_jobs(project_id, mission_id, root, now=now)
    cadence = upkeep_cadence(project_id, mission_id, root, config=config)
    if not cadence.due:
        left = cadence.jobs_left
        raise UpkeepError(f"no upkeep job is due: {left} more completed job{'' if left == 1 else 's'} of "
                          f"this mission come first")
    return append_upkeep_line(project_id, mission_id, LINE_UPKEEP_SKIPPED, {
        "reason": text, "after_jobs": cadence.completed, "after_job_id": cadence.after_job_id}, root, now=now)
