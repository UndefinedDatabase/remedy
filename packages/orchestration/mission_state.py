"""F056 — the MISSION: a persistent goal and the ordered chain of jobs serving it.

A job is an execution unit; it starts, it ends, and its goal dies with it.  A
goal that outlives one job needs a home of its own, and that home is a mission:
a THIN persistent record above jobs.  It holds the goal text, a status, and an
ordered list of links to the jobs that served it.  It holds no plans, no
evidence and no results — those stay on the jobs, where they already live.

What a mission deliberately is NOT:

* It is not created for you.  Nothing in this module ever creates a mission as
  a side effect of running work.  A mission exists because a human ran
  ``remedy mission start`` or answered the plan-approval opt-in with yes — the
  opt-in defaults to NO (P2).  A plain do-flow leaves no mission behind.
* It is not a second job store.  A link is a job id and a role, nothing more.
  ``mission show`` reads each job's terminal state from the job store at read
  time, so a mission can never disagree with the jobs it points at.
* It does not transition itself.  ``achieved``/``abandoned``/``paused`` are set
  by explicit commands only; this feature contains no automatic transition.

Storage, like every other entity in this codebase (``storage.save_job``,
``project_registry``, ``proposed_tasks``): one atomic JSON file per record,
under a project-scoped area of the data root::

    <data root>/missions/<project id>/<mission id>.json

Reuse (A6): the atomic write is ``storage._atomic_write_job`` — temp file,
fsync, ``os.replace`` — the same helper behind ``save_job`` and behind
``checkpoints.write_checkpoint``.  This module introduces NO second atomic
writer and NO second reader of the data root.

Honesty rules this module holds to:

* A goal is IMMUTABLE.  Changing what a mission is for produces a NEW mission,
  never a rewritten one — a rewritten goal would silently falsify the history
  of every job already linked below it.
* One job belongs to at most ONE mission.  Cross-mission reuse of a job would
  make lineage ambiguous, so it is refused at link time.
* Listings never crash.  A record that will not parse is skipped and COUNTED
  (``list_missions_safe``), exactly as ``storage.list_jobs_safe`` does for
  jobs; a link whose job is gone renders ``(missing job)`` rather than raising.

Verify-first (T003) lives at the bottom of this module: a follow-up job's plan
is REQUIRED to begin with a verify task, and that requirement is enforced by
building the plan that way and validating it, never by asking a model nicely.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.data_paths import missions_dir
from packages.orchestration.storage import _atomic_write_job as _atomic_write

#: Bumped whenever the record body changes shape.  A reader meeting a version
#: it does not know refuses that record rather than guessing at its meaning.
MISSION_SCHEMA_VERSION = 1

MISSION_STATUS_ACTIVE = "active"
MISSION_STATUS_PAUSED = "paused"
MISSION_STATUS_ACHIEVED = "achieved"
MISSION_STATUS_ABANDONED = "abandoned"
#: Every status a mission may hold.  Nothing in this feature moves a mission
#: between them on its own — see the module docstring.
MISSION_STATUSES = (
    MISSION_STATUS_ACTIVE,
    MISSION_STATUS_PAUSED,
    MISSION_STATUS_ACHIEVED,
    MISSION_STATUS_ABANDONED,
)

#: The two roles a linked job can play in a mission's chain.
MISSION_ROLE_INITIAL = "initial"
MISSION_ROLE_FOLLOW_UP = "follow_up"
MISSION_ROLES = (MISSION_ROLE_INITIAL, MISSION_ROLE_FOLLOW_UP)

#: A goal is operator input: it is small, or it is not a goal.
MAX_MISSION_GOAL_CHARS = 8_000

#: Rendered for a link whose job is no longer in the job store, and for one
#: whose job file will not parse.  Two different facts, two different labels —
#: a listing that blurs them is a listing that lies.
MISSING_JOB_LABEL = "(missing job)"
UNREADABLE_JOB_LABEL = "(unreadable job)"

#: Anything that becomes a path component: the shape ``job_queue`` established.
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class MissionError(RuntimeError):
    """A mission operation failed in a way the caller must handle."""


class MissionNotFoundError(MissionError):
    """No mission with this id exists in this project."""


class MissionGoalImmutableError(MissionError):
    """An attempt to change a persisted mission's goal.

    A changed goal is a NEW mission (feature-file rule).  Rewriting one in
    place would retroactively relabel every job already linked below it.
    """


class MissionJobAlreadyLinkedError(MissionError):
    """This job already belongs to a mission — one job, at most one mission."""

    def __init__(self, job_id: str, mission_id: str) -> None:
        super().__init__(
            f"job {job_id} is already linked to mission {mission_id}")
        self.job_id = job_id
        self.mission_id = mission_id


class MissionLinkRoleError(MissionError):
    """The role does not fit the chain: exactly one initial job, and it is first."""


class MissionVerifyFirstError(MissionError):
    """A follow-up plan does not begin with the injected verify task.

    Raised by :func:`assert_verify_first`.  This is the structural half of the
    verify-first rule: the plan is BUILT verify-first and then CHECKED to be,
    so a caller cannot ship a follow-up whose verification is optional.
    """


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MissionJobLink:
    """One job's place in a mission's chain."""

    job_id: str
    role: str
    created_at: str

    def to_json(self) -> dict[str, Any]:
        return {"job_id": self.job_id, "role": self.role,
                "created_at": self.created_at}

    @classmethod
    def from_json(cls, body: Any) -> MissionJobLink:
        if not isinstance(body, dict):
            raise ValueError("mission job link must be an object")
        role = str(body.get("role", ""))
        if role not in MISSION_ROLES:
            raise ValueError(f"unknown mission job role: {role!r}")
        job_id = str(body.get("job_id", ""))
        if not job_id:
            raise ValueError("mission job link carries no job id")
        return cls(job_id=job_id, role=role,
                   created_at=str(body.get("created_at", "")))


@dataclass(frozen=True)
class Mission:
    """A persistent goal plus the ordered chain of jobs that served it.

    ``dossier_ref`` is RESERVED for the later dossier feature and is never
    filled by this one.  It exists now so that the record shape does not have
    to change when the dossier lands — an empty string means "no dossier",
    which is the truth today for every mission.

    ``mission_plan`` (F069) is the compiled MissionPlan, ADDITIVE and OPTIONAL:
    the key is written only once a plan exists, so every record written before
    F069 stays byte-identical and every reader that predates F069 keeps working
    — which is why :data:`MISSION_SCHEMA_VERSION` does NOT move for it.  The
    body is the plan's ``model_dump()`` plus the ``_versions``/``_version``
    keys the flight-plan replan precedent established; ``None`` and an absent
    key both mean "not compiled yet".
    """

    id: str
    project_id: str
    goal: str
    status: str = MISSION_STATUS_ACTIVE
    job_links: tuple[MissionJobLink, ...] = ()
    dossier_ref: str = ""
    created_at: str = ""
    schema_version: int = MISSION_SCHEMA_VERSION
    mission_plan: dict[str, Any] | None = None

    def to_json(self) -> dict[str, Any]:
        body = {
            "schema_version": self.schema_version,
            "id": self.id,
            "project_id": self.project_id,
            "goal": self.goal,
            "status": self.status,
            "job_links": [link.to_json() for link in self.job_links],
            "dossier_ref": self.dossier_ref,
            "created_at": self.created_at,
        }
        # Written only when there IS one: an absent key is how a pre-F069
        # record says "no plan", and a record that never gained a plan must not
        # start differing from the bytes already on disk.
        if self.mission_plan is not None:
            body["mission_plan"] = self.mission_plan
        return body

    @classmethod
    def from_json(cls, body: Any) -> Mission:
        if not isinstance(body, dict):
            raise ValueError("mission record must be an object")
        version = int(body.get("schema_version", 0))
        if version != MISSION_SCHEMA_VERSION:
            raise ValueError(f"unknown mission schema version: {version}")
        status = str(body.get("status", ""))
        if status not in MISSION_STATUSES:
            raise ValueError(f"unknown mission status: {status!r}")
        mission_id = str(body.get("id", ""))
        project_id = str(body.get("project_id", ""))
        if not mission_id or not project_id:
            raise ValueError("mission record carries no id or project id")
        links = body.get("job_links") or []
        if not isinstance(links, list):
            raise ValueError("mission job_links must be a list")
        plan = body.get("mission_plan")
        if plan is not None and not isinstance(plan, dict):
            raise ValueError("mission_plan must be an object")
        return cls(
            id=mission_id,
            project_id=project_id,
            goal=str(body.get("goal", "")),
            status=status,
            job_links=tuple(MissionJobLink.from_json(link) for link in links),
            dossier_ref=str(body.get("dossier_ref", "")),
            created_at=str(body.get("created_at", "")),
            schema_version=version,
            mission_plan=plan,
        )

    def job_ids(self) -> tuple[str, ...]:
        return tuple(link.job_id for link in self.job_links)

    def latest_link(self) -> MissionJobLink | None:
        """The last job linked into the chain, or None for an empty mission."""
        return self.job_links[-1] if self.job_links else None


# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------


def _validate_path_id(raw: str, what: str) -> str:
    """Refuse anything that must not become a path component."""
    text = str(raw)
    if not _ID_RE.match(text):
        raise MissionError(f"invalid {what}: {raw!r}")
    return text


def mission_root(root: Path | None = None) -> Path:
    """The mission area of the data root — one directory per project below it."""
    return missions_dir(root)


def mission_dir_for_project(project_id: str, root: Path | None = None) -> Path:
    """Where one project's mission records live."""
    return mission_root(root) / _validate_path_id(project_id, "project id")


def mission_record_path(project_id: str, mission_id: str,
                        root: Path | None = None) -> Path:
    """The single file one mission record lives in."""
    return (mission_dir_for_project(project_id, root)
            / f"{_validate_path_id(mission_id, 'mission id')}.json")


def mission_evidence_dir(project_id: str, mission_id: str,
                         root: Path | None = None) -> Path:
    """Where one mission's own artifacts live — its rendered plan, its DoDs.

    Mirrors the job precedent (``pingpong_job.job_evidence_dir`` =
    ``<jobs>/<job id>/evidence``): a directory named after the record, with an
    ``evidence`` area inside it.  It is a SIBLING of the ``<mission id>.json``
    record, and ``list_missions_safe`` globs ``*.json``, so adding it cannot
    disturb any listing.
    """
    return (mission_dir_for_project(project_id, root)
            / _validate_path_id(mission_id, "mission id") / "evidence")


def project_ids_with_missions(root: Path | None = None) -> list[str]:
    """Every project directory that actually exists under the mission area.

    Read from disk, not from the registry: a mission whose project was
    unregistered still exists, and hiding it would make the answer dishonest.
    """
    base = mission_root(root)
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


# ---------------------------------------------------------------------------
# Reading and writing
# ---------------------------------------------------------------------------


def _utc_now_iso(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).isoformat()


def save_mission(mission: Mission, root: Path | None = None) -> Path:
    """Persist one mission atomically, refusing to rewrite its goal.

    The goal check reads the record already on disk: a save that would change
    it is a :class:`MissionGoalImmutableError`, because a changed goal is a new
    mission, never an edited one.
    """
    path = mission_record_path(mission.project_id, mission.id, root)
    if path.exists():
        try:
            existing = Mission.from_json(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            existing = None      # unreadable: overwriting it cannot lose a goal
        if existing is not None and existing.goal != mission.goal:
            raise MissionGoalImmutableError(
                f"mission {mission.id} already exists with a different goal — "
                f"a changed goal is a new mission (remedy mission start)")
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(path, json.dumps(mission.to_json(), indent=2, sort_keys=True))
    return path


def load_mission(project_id: str, mission_id: str,
                 root: Path | None = None) -> Mission:
    """Load one mission by id.  Raises when it is missing or will not parse."""
    path = mission_record_path(project_id, mission_id, root)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MissionNotFoundError(
            f"no mission {mission_id} in project {project_id}") from exc
    except OSError as exc:
        raise MissionError(f"cannot read mission {mission_id}: {exc}") from exc
    except ValueError as exc:
        raise MissionError(f"corrupt mission record {mission_id}: {exc}") from exc
    try:
        return Mission.from_json(raw)
    except ValueError as exc:
        raise MissionError(f"corrupt mission record {mission_id}: {exc}") from exc


def list_missions_safe(project_id: str, root: Path | None = None,
                       ) -> tuple[list[Mission], bool, list[str]]:
    """List one project's missions with corruption VISIBLE.

    Returns ``(missions, degraded, skipped_files)``.  Newest first by
    ``created_at``, ties broken by id so the order is total and reproducible —
    the same rule ``storage.list_jobs_safe`` follows for jobs.
    """
    directory = mission_dir_for_project(project_id, root)
    if not directory.is_dir():
        return ([], False, [])
    missions: list[Mission] = []
    skipped: list[str] = []
    for path in sorted(directory.glob("*.json")):
        try:
            missions.append(
                Mission.from_json(json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, ValueError):
            skipped.append(path.name)
    missions.sort(key=lambda m: (m.created_at, m.id), reverse=True)
    return (missions, len(skipped) > 0, skipped)


def list_missions(project_id: str, root: Path | None = None) -> list[Mission]:
    """One project's missions, newest first.  Unreadable records are skipped."""
    missions, _degraded, _skipped = list_missions_safe(project_id, root)
    return missions


def create_mission(project_id: str, goal: str, *,
                   now: datetime | None = None,
                   root: Path | None = None) -> Mission:
    """Create and persist a mission.  This is the ONLY way one comes into being.

    Called by ``remedy mission start`` and by the plan-approval opt-in — never
    as a side effect of running work.
    """
    text = str(goal).strip()
    if not text:
        raise MissionError("a mission needs a goal")
    if len(text) > MAX_MISSION_GOAL_CHARS:
        raise MissionError(
            f"mission goal exceeds {MAX_MISSION_GOAL_CHARS} characters "
            f"(got {len(text)})")
    mission = Mission(
        id=uuid4().hex,
        project_id=_validate_path_id(project_id, "project id"),
        goal=text,
        status=MISSION_STATUS_ACTIVE,
        created_at=_utc_now_iso(now),
    )
    save_mission(mission, root)
    return mission


# ---------------------------------------------------------------------------
# Linking jobs
# ---------------------------------------------------------------------------


def mission_for_job(job_id: str, root: Path | None = None) -> Mission | None:
    """The mission this job belongs to, or None.

    Scans every project's mission area, because job ids are globally unique and
    "already linked" must not depend on which project the caller asked about.
    """
    wanted = str(job_id)
    for project_id in project_ids_with_missions(root):
        for mission in list_missions(project_id, root):
            if wanted in mission.job_ids():
                return mission
    return None


def link_job_to_mission(project_id: str, mission_id: str, job_id: str,
                        role: str = MISSION_ROLE_FOLLOW_UP, *,
                        now: datetime | None = None,
                        root: Path | None = None) -> Mission:
    """Append a job to a mission's chain, enforcing both link validators.

    * One job belongs to at most one mission — an already-linked job is
      refused, whichever mission holds it.
    * A chain begins with exactly one ``initial`` job; every later link is a
      ``follow_up``.
    """
    if role not in MISSION_ROLES:
        raise MissionLinkRoleError(
            f"unknown mission job role {role!r} (expected one of "
            f"{', '.join(MISSION_ROLES)})")

    mission = load_mission(project_id, mission_id, root)
    holder = mission_for_job(job_id, root)
    if holder is not None:
        raise MissionJobAlreadyLinkedError(str(job_id), holder.id)

    if mission.job_links and role == MISSION_ROLE_INITIAL:
        raise MissionLinkRoleError(
            f"mission {mission.id} already has an initial job "
            f"({mission.job_links[0].job_id}) — later jobs are follow_up")
    if not mission.job_links and role != MISSION_ROLE_INITIAL:
        raise MissionLinkRoleError(
            f"mission {mission.id} has no jobs yet — the first link is "
            f"{MISSION_ROLE_INITIAL}, not {role}")

    link = MissionJobLink(job_id=str(job_id), role=role,
                          created_at=_utc_now_iso(now))
    updated = replace(mission, job_links=(*mission.job_links, link))
    save_mission(updated, root)
    return updated


def set_mission_status(project_id: str, mission_id: str, status: str,
                       root: Path | None = None) -> Mission:
    """Set a mission's status.

    Two kinds of caller write here.  The explicit human verbs — ``remedy
    mission achieve|abandon|pause``, through
    ``apps.cli.commands.mission_cmd._cmd_mission_set_status`` — and the loop's
    own terminal moves: ``mission_achieved`` writes ``achieved`` for
    ``declare_mission_achieved``, and ``execute_move`` writes ``abandoned``
    for ``abort_with_reason``, both in
    ``packages.orchestration.orchestrator_loop``.  A status on disk is
    therefore NOT evidence that a human put it there.

    Deliberately absent: any rule that moves a mission to ``achieved`` because
    its jobs finished.  A finished job is not an achieved goal, and this
    feature does not pretend otherwise — see the module docstring.
    """
    if status not in MISSION_STATUSES:
        raise MissionError(
            f"unknown mission status {status!r} (expected one of "
            f"{', '.join(MISSION_STATUSES)})")
    mission = load_mission(project_id, mission_id, root)
    updated = replace(mission, status=status)
    save_mission(updated, root)
    return updated


def set_mission_plan(project_id: str, mission_id: str,
                     plan_body: dict[str, Any] | None,
                     root: Path | None = None) -> Mission:
    """Persist a compiled MissionPlan body on the mission record.

    The record is the plan's home because the plan describes the MISSION, not
    any one job.  Writing it changes nothing else: the goal, the status and the
    job chain are untouched, and nothing is started — persisting a plan is not
    running one.
    """
    if plan_body is not None and not isinstance(plan_body, dict):
        raise MissionError("a mission plan body must be an object")
    mission = load_mission(project_id, mission_id, root)
    updated = replace(mission, mission_plan=plan_body)
    save_mission(updated, root)
    return updated


def resolve_mission_id(project_id: str, raw: str,
                       root: Path | None = None) -> str:
    """Full id, or a unique prefix — the same affordance job and queue ids have.

    Returns the input unchanged when nothing matches, so the caller's own
    not-found path produces the error message.
    """
    candidate = str(raw).strip()
    matches = [m.id for m in list_missions(project_id, root)
               if m.id.startswith(candidate)]
    if candidate in matches:
        return candidate
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise MissionError(
            f"ambiguous mission id prefix {raw!r} matches {len(matches)} "
            f"missions: {', '.join(sorted(m[:12] for m in matches))}")
    return candidate


# ---------------------------------------------------------------------------
# Rendering the chain
# ---------------------------------------------------------------------------


def mission_job_state_label(job_id: str) -> str:
    """A linked job's terminal state, read from the job store at render time.

    Never raises: a job that was deleted renders ``(missing job)`` and one
    whose file will not parse renders ``(unreadable job)``.  Those are
    different facts and get different labels.
    """
    from packages.orchestration.storage import load_job_safe

    try:
        uuid = UUID(str(job_id))
    except (AttributeError, TypeError, ValueError):
        return MISSING_JOB_LABEL
    try:
        job, degraded = load_job_safe(uuid)
    except Exception:  # noqa: BLE001 — a listing never dies of a bad record
        return UNREADABLE_JOB_LABEL
    if job is not None:
        return str(getattr(job.state, "value", job.state))
    return UNREADABLE_JOB_LABEL if degraded else MISSING_JOB_LABEL


def render_mission_chain(mission: Mission) -> list[str]:
    """The lines ``remedy mission show`` prints for one mission.

    Chain order is link order — the order the jobs were added, which is the
    order they ran.  Each line carries the job's state as the job store reports
    it RIGHT NOW, so the rendering cannot drift from the jobs it describes.
    """
    lines = [
        f"Mission {mission.id}",
        f"  Status: {mission.status}",
        f"  Goal:   {mission.goal}",
    ]
    if mission.dossier_ref:
        lines.append(f"  Dossier: {mission.dossier_ref}")
    if not mission.job_links:
        lines.append("  Chain:  (no jobs linked yet)")
        return lines
    lines.append("  Chain:")
    for index, link in enumerate(mission.job_links, start=1):
        lines.append(
            f"    {index}. {link.job_id}  {link.role:<9}  "
            f"{mission_job_state_label(link.job_id)}")
    return lines


def render_mission_row(mission: Mission) -> str:
    """One line of ``remedy mission list``."""
    goal = mission.goal.replace("\n", " ").strip()[:60]
    return (f"{mission.id[:12]}  {mission.status:<9}  "
            f"{len(mission.job_links):>2} job(s)  {goal}")


# ---------------------------------------------------------------------------
# Verify-first follow-ups (T003)
# ---------------------------------------------------------------------------

#: The planned id the injected verify task always carries, and which every
#: follow-up task in the same plan declares as its dependency.  Because
#: ``dag_schedule.ready_set`` withholds a task until every dependency is
#: COMPLETED, a failed verification makes the follow-up work unreachable — the
#: rule is enforced by the scheduler that already exists, not by a prompt.
MISSION_VERIFY_PLANNED_ID = "M000"
MISSION_VERIFY_TASK_TYPE = "mission_verify"

#: What a follow-up job records when the previous job left no runnable
#: verification behind.  A9 default: it is reported as unverified — loudly and
#: by name — and never as a passed verification.
VERIFY_RESULT_PASSED = "passed"
VERIFY_RESULT_FAILED = "failed"
VERIFY_RESULT_UNVERIFIABLE = "unverifiable"

#: Where a follow-up's verify record lands: the job's own evidence area, one
#: directory over from the cycle and checkpoint records.
MISSION_VERIFY_FILENAME = "mission_verify.json"


def resolve_verify_command(job: Any) -> str:
    """The command that re-checks a finished job's Definition of Done.

    Looked up in the order a job records it: an explicit
    ``metadata["verify_command"]`` first, then the flight plan's own
    ``verify_command``.  Returns "" when the job recorded none — which is
    reported as :data:`VERIFY_RESULT_UNVERIFIABLE`, never as a pass.
    """
    metadata = getattr(job, "metadata", None)
    if isinstance(metadata, dict):
        command = str(metadata.get("verify_command", "") or "").strip()
        if command:
            return command
    plan = getattr(job, "flight_plan", None)
    if isinstance(plan, dict):
        command = str(plan.get("verify_command", "") or "").strip()
        if command:
            return command
    return ""


def build_verify_first_task(previous_job: Any) -> Any:
    """The verify task injected at the head of every follow-up plan.

    It re-runs the PREVIOUS job's Definition of Done against the CURRENT state
    of the world.  It is a task, not an instruction: it occupies position 0 of
    the plan and every other task depends on it.
    """
    from packages.core.models import AcceptanceCheck, RunState, Task

    previous_id = str(getattr(previous_job, "id", "") or "")
    command = resolve_verify_command(previous_job)
    described = command or "no verification command recorded"
    return Task(
        description=(
            f"Verify the previous job's Definition of Done still holds "
            f"(job {previous_id}): {described}"),
        acceptance_checks=[AcceptanceCheck(
            description=(
                "The previous job's recorded verification passes against the "
                "current state before any follow-up work starts."))],
        inputs={
            "task_type": MISSION_VERIFY_TASK_TYPE,
            "verify_command": command,
            "previous_job_id": previous_id,
            "flight": {
                "planned_id": MISSION_VERIFY_PLANNED_ID,
                "title": "Verify previous state",
                "depends_on": [],
                "est_tokens_band": "S",
                "files_hint": [],
            },
        },
        status=RunState.PENDING,
    )


def is_verify_task(task: Any) -> bool:
    """True for the injected verify task, identified by its task type."""
    inputs = getattr(task, "inputs", None)
    if not isinstance(inputs, dict):
        return False
    return inputs.get("task_type") == MISSION_VERIFY_TASK_TYPE


def inject_verify_first(previous_job: Any, follow_up_tasks: list[Any]) -> list[Any]:
    """Return the follow-up plan with verification structurally in front.

    Every follow-up task is rewritten to declare the verify task as a
    dependency, so the existing scheduler — not this module, and not a prompt —
    is what keeps the work from starting before the check passes.
    """
    verify = build_verify_first_task(previous_job)
    planned: list[Any] = [verify]
    for index, task in enumerate(follow_up_tasks, start=1):
        flight = dict(task.inputs.get("flight") or {})
        declared = [str(dep) for dep in (flight.get("depends_on") or [])]
        if MISSION_VERIFY_PLANNED_ID not in declared:
            declared.insert(0, MISSION_VERIFY_PLANNED_ID)
        flight["depends_on"] = declared
        flight.setdefault("planned_id", f"M{index:03d}")
        flight.setdefault("title", task.description[:60])
        flight.setdefault("est_tokens_band", "M")
        flight.setdefault("files_hint", [])
        inputs = dict(task.inputs)
        inputs["flight"] = flight
        planned.append(task.model_copy(update={"inputs": inputs}))
    return planned


def assert_verify_first(tasks: list[Any]) -> None:
    """Refuse a follow-up plan that does not begin with the verify task.

    The second half of the structural rule: plans are built verify-first by
    :func:`inject_verify_first` and then CHECKED here, so no caller can ship a
    follow-up whose verification is merely suggested.
    """
    if not tasks:
        raise MissionVerifyFirstError(
            "a follow-up plan must begin with the injected verify task, but it "
            "has no tasks at all")
    if not is_verify_task(tasks[0]):
        raise MissionVerifyFirstError(
            "a follow-up plan must begin with the injected verify task "
            f"(task_type {MISSION_VERIFY_TASK_TYPE!r}); the plan starts with: "
            f"{getattr(tasks[0], 'description', '?')!r}")
    for task in tasks[1:]:
        flight = task.inputs.get("flight") if isinstance(task.inputs, dict) else None
        declared = list((flight or {}).get("depends_on") or [])
        if MISSION_VERIFY_PLANNED_ID not in [str(d) for d in declared]:
            raise MissionVerifyFirstError(
                f"follow-up task {getattr(task, 'description', '?')!r} does not "
                f"depend on the verify task {MISSION_VERIFY_PLANNED_ID} — it "
                f"could start before the previous state was verified")


@dataclass(frozen=True)
class MissionVerifyOutcome:
    """What running one follow-up's verify task actually established."""

    result: str
    command: str
    exit_code: int | None
    output_tail: str
    previous_job_id: str
    checked_at: str
    #: True only when the follow-up work is allowed to start.  An unverifiable
    #: previous job does not block (there is nothing to fail), but it is
    #: recorded as unverified, never as passed.
    follow_up_may_start: bool = False
    detail: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "command": self.command,
            "exit_code": self.exit_code,
            "output_tail": self.output_tail,
            "previous_job_id": self.previous_job_id,
            "checked_at": self.checked_at,
            "follow_up_may_start": self.follow_up_may_start,
            "detail": self.detail,
        }


@dataclass
class MissionFollowupRun:
    """The evidence record of one follow-up execution, in order.

    ``steps`` is the ordered list of what ran.  The verify task is always
    ``steps[0]``; a reader asserting verify-first ordering reads it from here
    rather than from a claim in prose.
    """

    mission_id: str
    job_id: str
    verify: MissionVerifyOutcome
    steps: list[str] = field(default_factory=list)
    follow_up_started: bool = False
    message: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": MISSION_SCHEMA_VERSION,
            "mission_id": self.mission_id,
            "job_id": self.job_id,
            "verify": self.verify.to_json(),
            "steps": list(self.steps),
            "follow_up_started": self.follow_up_started,
            "message": self.message,
        }


def _tail(text: str, limit: int = 800) -> str:
    stripped = (text or "").strip()
    return stripped if len(stripped) <= limit else "…" + stripped[-limit:]


def run_verify_task(task: Any, *, cwd: Path | None = None,
                    now: datetime | None = None,
                    runner: Any = None) -> MissionVerifyOutcome:
    """Run the injected verify task and report what it established.

    ``runner`` exists for tests and for callers that already own a sandboxed
    executor; it takes ``(argv, cwd)`` and returns ``(exit_code, output)``.
    The default runs the recorded command as an argv list — never through a
    shell, so a recorded command cannot become a recorded shell injection.
    """
    inputs = task.inputs if isinstance(getattr(task, "inputs", None), dict) else {}
    command = str(inputs.get("verify_command", "") or "").strip()
    previous_job_id = str(inputs.get("previous_job_id", "") or "")
    stamp = _utc_now_iso(now)

    if not command:
        return MissionVerifyOutcome(
            result=VERIFY_RESULT_UNVERIFIABLE,
            command="", exit_code=None, output_tail="",
            previous_job_id=previous_job_id, checked_at=stamp,
            follow_up_may_start=True,
            detail=(f"job {previous_job_id} recorded no verification command — "
                    f"nothing was verified"),
        )

    import shlex

    argv = shlex.split(command)
    if runner is None:
        def runner(argv: list[str], cwd: Path | None):  # noqa: E306
            import subprocess

            completed = subprocess.run(
                argv, cwd=str(cwd) if cwd else None, capture_output=True,
                text=True, timeout=900,
            )
            return (completed.returncode,
                    (completed.stdout or "") + (completed.stderr or ""))

    try:
        exit_code, output = runner(argv, cwd)
    except Exception as exc:  # noqa: BLE001 — a broken command is a failed verify
        return MissionVerifyOutcome(
            result=VERIFY_RESULT_FAILED, command=command, exit_code=None,
            output_tail=_tail(f"{type(exc).__name__}: {exc}"),
            previous_job_id=previous_job_id, checked_at=stamp,
            follow_up_may_start=False,
            detail=f"verification command could not run: {type(exc).__name__}: {exc}",
        )

    passed = int(exit_code) == 0
    return MissionVerifyOutcome(
        result=VERIFY_RESULT_PASSED if passed else VERIFY_RESULT_FAILED,
        command=command, exit_code=int(exit_code), output_tail=_tail(output),
        previous_job_id=previous_job_id, checked_at=stamp,
        follow_up_may_start=passed,
        detail=("" if passed else
                f"the previous job's verification now fails: `{command}` exited "
                f"{int(exit_code)}"),
    )


def mission_verify_record_path(job_id: str) -> Path:
    """Where a follow-up job's verify record lands, inside its evidence area."""
    from packages.orchestration.pingpong_job import job_evidence_dir

    return Path(job_evidence_dir(str(job_id))) / MISSION_VERIFY_FILENAME


def write_mission_verify_record(run: MissionFollowupRun) -> Path:
    """Persist the follow-up run record atomically, next to the job's evidence."""
    path = mission_verify_record_path(run.job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write(path, json.dumps(run.to_json(), indent=2, sort_keys=True))
    return path


def read_mission_verify_record(job_id: str) -> dict[str, Any] | None:
    """The follow-up run record for a job, or None when it never ran."""
    try:
        return json.loads(mission_verify_record_path(job_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


#: The task type a follow-up's own work carries, so the verify task and the
#: work it gates are distinguishable in a plan without reading descriptions.
MISSION_FOLLOW_UP_TASK_TYPE = "mission_follow_up"


def build_follow_up_task(next_step: str) -> Any:
    """The single work task a ``mission continue`` step asks for.

    Deliberately ONE task: planning a follow-up into a DAG is the planner's
    job, not this module's.  What this module owns is that whatever the plan
    turns out to be, verification comes first.
    """
    from packages.core.models import RunState, Task

    return Task(
        description=str(next_step).strip(),
        inputs={"task_type": MISSION_FOLLOW_UP_TASK_TYPE},
        status=RunState.PENDING,
    )


def continue_mission(project_id: str, mission_id: str, next_step: str, *,
                     now: datetime | None = None,
                     root: Path | None = None) -> Any:
    """Create the next job in a mission's chain and link it.

    With a previous job in the chain, the new job's plan is built verify-first
    and then validated as such: the injected verify task is task 0 and the work
    declares it as a dependency, so ``dag_schedule.ready_set`` withholds the
    work until the verification has COMPLETED.

    On an empty mission there is nothing to verify yet, so this creates the
    ``initial`` job with the work alone — an honest plan, not a verify task
    pointed at a job that does not exist.
    """
    from packages.core.models import Job, RunState
    from packages.orchestration.storage import (
        JobNotFoundError,
        JobStoreError,
        load_job,
        save_job,
    )

    text = str(next_step).strip()
    if not text:
        raise MissionError("a follow-up needs a step to take")

    mission = load_mission(project_id, mission_id, root)
    previous = mission.latest_link()

    work = build_follow_up_task(text)
    if previous is None:
        tasks = [work]
        role = MISSION_ROLE_INITIAL
    else:
        try:
            previous_job = load_job(UUID(previous.job_id))
        except (ValueError, JobNotFoundError) as exc:
            raise MissionError(
                f"the previous job {previous.job_id} is gone, so its Definition "
                f"of Done cannot be verified — a follow-up would be starting "
                f"blind") from exc
        except JobStoreError as exc:
            raise MissionError(
                f"the previous job {previous.job_id} cannot be read, so its "
                f"Definition of Done cannot be verified: {exc}") from exc
        tasks = inject_verify_first(previous_job, [work])
        role = MISSION_ROLE_FOLLOW_UP

    # Built verify-first above; CHECKED here, so the rule cannot be skipped by
    # a future caller that assembles the plan some other way.
    if role == MISSION_ROLE_FOLLOW_UP:
        assert_verify_first(tasks)

    job = Job(
        name=text[:80],
        mission=mission.goal,
        user_prompt=text,
        project_id=str(mission.project_id),
        tasks=tasks,
        state=RunState.PLANNED,
        metadata={"mission_id": mission.id, "mission_role": role},
    )
    save_job(job)
    link_job_to_mission(project_id, mission.id, str(job.id), role, now=now,
                        root=root)
    return job


def execute_mission_followup(job: Any, *, cwd: Path | None = None,
                             runner: Any = None, work_runner: Any = None,
                             now: datetime | None = None) -> MissionFollowupRun:
    """Run a follow-up job verify-FIRST, and let the work start only if it passed.

    The ordering is not a convention here: the verify task is task 0, the work
    declares it as a dependency, and readiness is computed by
    ``dag_schedule.ready_set`` — the scheduler the multi-cycle executor already
    uses.  A failed verification therefore leaves the work unreachable rather
    than merely discouraged.

    ``work_runner`` is how a caller executes one work task; it takes the task
    and returns True when the task completed.  It is REQUIRED to do the work —
    this module never marks a task completed on its own, because it has not
    observed anything that would justify the claim.
    """
    from packages.core.models import RunState
    from packages.orchestration.dag_schedule import blocked_downstream, ready_set
    from packages.orchestration.storage import save_job

    assert_verify_first(list(job.tasks))
    verify_task = job.tasks[0]

    outcome = run_verify_task(verify_task, cwd=cwd, now=now, runner=runner)
    run = MissionFollowupRun(
        mission_id=str((getattr(job, "metadata", None) or {}).get("mission_id", "")),
        job_id=str(job.id),
        verify=outcome,
        steps=[f"verify:{outcome.result}"],
    )

    if not outcome.follow_up_may_start:
        verify_task.status = RunState.FAILED
        blocked = blocked_downstream(list(job.tasks), [verify_task.id])
        job.state = RunState.FAILED
        run.message = (
            f"{outcome.detail} — the follow-up never started "
            f"({len(blocked)} task(s) blocked behind it)")
        save_job(job)
        write_mission_verify_record(run)
        return run

    verify_task.status = RunState.COMPLETED
    for task in job.tasks[1:]:
        if task.id not in ready_set(list(job.tasks)):
            continue
        if work_runner is None:
            break
        if work_runner(task):
            task.status = RunState.COMPLETED
            run.steps.append(f"work:{task.description}")
    run.follow_up_started = len(run.steps) > 1
    run.message = (
        "verification passed; the follow-up work ran"
        if run.follow_up_started else
        "verification passed; the follow-up work is ready to run")
    if outcome.result == VERIFY_RESULT_UNVERIFIABLE:
        run.message = f"{outcome.detail}; " + run.message.split("; ", 1)[-1]
    job.state = (RunState.COMPLETED
                 if all(t.status == RunState.COMPLETED for t in job.tasks)
                 else RunState.PLANNED)
    save_job(job)
    write_mission_verify_record(run)
    return run
