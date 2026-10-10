"""The mission record: its constants, its errors and the three types a mission is stored as.

F205 moved these out of `packages/orchestration/mission_state.py` unchanged, as step (1) of that
file's boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D1).
`mission_state.py` imports every name back by name, so each import path keeps working; the
storage, the links and the verify-first path stay there.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


class MissionProjectError(MissionError):
    """The projects of a mission over several repositories do not fit (DECISION F205 D2).

    Raised when the projects given at creation are not the lead project first and each once, and
    when a job is linked to such a mission whose project the mission does not span or whose
    record cannot be read to tell.
    """


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MissionJobLink:
    """One job's place in a mission's chain.

    ``project_id`` (F205, DECISION F205 D2) is the project the linked job works in, ADDITIVE and
    OPTIONAL on ``Mission.mission_plan``'s terms: it is set and written only on a mission that
    spans several projects, so every other link keeps the bytes it has on disk.
    """

    job_id: str
    role: str
    created_at: str
    project_id: str = ""

    def to_json(self) -> dict[str, Any]:
        body = {"job_id": self.job_id, "role": self.role,
                "created_at": self.created_at}
        if self.project_id:
            body["project_id"] = self.project_id
        return body

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
                   created_at=str(body.get("created_at", "")),
                   project_id=str(body.get("project_id", "")))


# Three fields rather than a union, because they answer different questions.
@dataclass(frozen=True)
class MissionOrder:
    """What a mission was ASKED for, and where the asking came from.

    DECISION F260 D1 words the order as "text, or file path + sha256".  All
    three are carried instead of a union because they are not alternatives: the
    text is what Remedy actually acted on, while the path and the digest are
    what a later reader checks the file against to see whether the order has
    moved underneath the mission since.  ``source_sha256`` is spelled to match
    ``JobPlan.job_file_sha256``, which the vocabulary page's Order row names as
    the same concept under another name — one spelling per concept.

    Every field defaults to the empty string: an order given as pasted text has
    no file, and one given as a file has no separate text.
    """

    text: str = ""
    source_path: str = ""
    source_sha256: str = ""

    def to_json(self) -> dict[str, Any]:
        return {"text": self.text, "source_path": self.source_path,
                "source_sha256": self.source_sha256}

    @classmethod
    def from_json(cls, body: Any) -> MissionOrder:
        if not isinstance(body, dict):
            raise ValueError("mission order must be an object")
        return cls(text=str(body.get("text", "")),
                   source_path=str(body.get("source_path", "")),
                   source_sha256=str(body.get("source_sha256", "")))


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
    keys the task plan's versioning established; ``None`` and an absent
    key both mean "not compiled yet".

    ``order`` and ``contract`` (F272) are the last two fields DECISION F260 D1
    names, and both are ADDITIVE and OPTIONAL on exactly ``mission_plan``'s
    terms: each key is written only once its value exists, so every record
    written before F272 stays byte-identical and every reader that predates it
    keeps working — which is why :data:`MISSION_SCHEMA_VERSION` does NOT move
    for them either.  ``order`` is the :class:`MissionOrder` this mission came
    from.  ``contract`` is the mission's acceptance criteria (DECISION
    amend0905-vocab D9).  Its SHAPE is owned by
    ``packages/orchestration/mission_contract.py`` (DECISION F269 D2), which
    validates it on read and on write and is its only production writer; this
    module stores the body and defines no shape for it.  ``None`` and an absent
    key both mean "no contract compiled yet".

    ``project_ids`` (F205, DECISION F205 D2) are the projects a mission over several repositories
    spans, ``project_id`` first, each once; ADDITIVE and OPTIONAL on ``mission_plan``'s terms, the
    key is written only on such a mission, and an empty tuple means the mission's own project
    alone (:meth:`spanned_project_ids`).
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
    order: MissionOrder | None = None
    contract: dict[str, Any] | None = None
    project_ids: tuple[str, ...] = ()

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
        # Each written only when there IS one, on the same terms and for the
        # same reason as the plan above: an absent key is how a pre-F272 record
        # says "no order" and "no contract", and a record that never gained
        # either must not start differing from the bytes already on disk.
        if self.order is not None:
            body["order"] = self.order.to_json()
        if self.contract is not None:
            body["contract"] = self.contract
        # Written only on a mission over several projects, for the same reason (DECISION F205 D2).
        if self.project_ids:
            body["project_ids"] = list(self.project_ids)
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
        order = body.get("order")
        contract = body.get("contract")
        if contract is not None and not isinstance(contract, dict):
            raise ValueError("mission contract must be an object")
        spanned = body.get("project_ids")
        if spanned is not None:
            if not isinstance(spanned, list):
                raise ValueError("mission project_ids must be a list")
            spanned = tuple(str(project) for project in spanned)
            check_spanned_project_ids(project_id, spanned)
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
            order=MissionOrder.from_json(order) if order is not None else None,
            contract=contract,
            project_ids=spanned or (),
        )

    def job_ids(self) -> tuple[str, ...]:
        return tuple(link.job_id for link in self.job_links)

    def latest_link(self) -> MissionJobLink | None:
        """The last job linked into the chain, or None for an empty mission."""
        return self.job_links[-1] if self.job_links else None

    def spanned_project_ids(self) -> tuple[str, ...]:
        """Every project this mission's jobs may work in, its own project first."""
        return self.project_ids or (self.project_id,)


def check_spanned_project_ids(lead: str, project_ids: tuple[str, ...]) -> None:
    """Raise ValueError unless *project_ids* is at least two projects, *lead* first, each once.

    The one rule for the projects a mission spans (DECISION F205 D2), read by
    :meth:`Mission.from_json` and by ``create_mission``.
    """
    if len(project_ids) < 2:
        raise ValueError("a mission over several projects spans at least two")
    if project_ids[0] != lead:
        raise ValueError(f"the projects a mission spans begin with its own project {lead!r}")
    if len(set(project_ids)) != len(project_ids):
        raise ValueError("the projects a mission spans name each project once")


def follow_up_target(mission: Mission, previous_job: Any) -> dict[str, str]:
    """Where the next job of *mission* works: the previous job's project and repository.

    A mission over several projects continues in the project and repository of the job its
    chain ends with, so the next job's verify-first task re-checks that job where it worked
    (DECISION F205 D5); the next job's record carries both. ``{}`` for a mission of one project,
    or one with no job yet, whose next job is planned as before. Raises
    :class:`MissionProjectError` when the previous job names no repository, or a project the
    mission does not span.
    """
    if not mission.project_ids or previous_job is None:
        return {}
    project = str(getattr(previous_job, "project_id", "") or "")
    repo = str(getattr(previous_job, "repo_path", "") or "")
    if not repo or project not in mission.project_ids:
        raise MissionProjectError(
            f"the previous job {getattr(previous_job, 'job_id', '')} works in project "
            f"{project or '(none)'} and repository {repo or '(none)'}, so mission {mission.id}, "
            f"which spans several projects, cannot tell where its next job works")
    return {"project_id": project, "repo_path": repo}
