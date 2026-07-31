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
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

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
    """

    id: str
    project_id: str
    goal: str
    status: str = MISSION_STATUS_ACTIVE
    job_links: tuple[MissionJobLink, ...] = ()
    dossier_ref: str = ""
    created_at: str = ""
    schema_version: int = MISSION_SCHEMA_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "id": self.id,
            "project_id": self.project_id,
            "goal": self.goal,
            "status": self.status,
            "job_links": [link.to_json() for link in self.job_links],
            "dossier_ref": self.dossier_ref,
            "created_at": self.created_at,
        }

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
        return cls(
            id=mission_id,
            project_id=project_id,
            goal=str(body.get("goal", "")),
            status=status,
            job_links=tuple(MissionJobLink.from_json(link) for link in links),
            dossier_ref=str(body.get("dossier_ref", "")),
            created_at=str(body.get("created_at", "")),
            schema_version=version,
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

