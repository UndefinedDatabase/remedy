"""F269 T001 — the CONTRACT a mission carries, and the slice of it a job serves.

A mission's contract is its acceptance criteria: what must hold before the
mission counts as done (DECISION amend0905-vocab D9).  This module owns the
SHAPE of that record — DECISION F269 D2 — and is the only production writer of
``Mission.contract``; ``mission_state.set_mission_contract`` stays the storage
call underneath and defines no shape of its own.

The body is one JSON object::

    {"schema": "contract_v1", "template": <name or null>,
     "criteria": [<criterion>, ...], "amendments": [<object>, ...]}

and a criterion is ``{"id", "text", "blocking", "origin", "milestones",
"check", "status", "evidence_ref"}``.  Every rule D2 states is checked on read
AND on write.  A body that breaks one is refused with a :class:`ContractError`
naming the rule — it is never repaired and never half-loaded, because a
contract that silently lost a criterion would let a mission count as done
while an acceptance criterion was never even looked at.

A job's contract is not stored anywhere: it is DERIVED (DECISION F269 D3).  The
orchestrator records on each job it dispatches the milestone the job serves
(``metadata["milestone_id"]``), and the job's slice is every whole-mission
criterion plus every criterion scoped to that milestone, in contract order —
a subset of the mission's criteria by construction.

Deliberately absent: the compiled ``check`` of a criterion.  It stays null
until T002 compiles it through F061's compiler, and this module never
compiles, runs or gates anything.  The names ``save_contract`` and
``load_contract`` belong to ``run_contract.py`` (a job's run contract, a
different record) and are not used here.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: The one schema tag a contract body carries today.
CONTRACT_SCHEMA = "contract_v1"

#: Where a criterion came from (DECISION amend0911-feedback D5).
CONTRACT_ORIGINS = ("template", "planner", "amendment")

#: A criterion's state.  ``open`` until the mission gate (T002) says otherwise.
CRITERION_STATUS_OPEN = "open"
CRITERION_STATUSES = (CRITERION_STATUS_OPEN, "met", "unmet")

#: The job metadata key the orchestrator's dispatch writes (DECISION F269 D3).
JOB_MILESTONE_KEY = "milestone_id"

_CRITERION_ID_RE = re.compile(r"^C\d{3}$")
_CONTRACT_FIELDS = ("schema", "template", "criteria", "amendments")
_CRITERION_FIELDS = ("id", "text", "blocking", "origin", "milestones", "check",
                     "status", "evidence_ref")


class ContractError(ValueError):
    """A contract body breaks one of DECISION F269 D2's rules.

    ``rule`` is the rule's short statement, and the message leads with it, so
    the operator reads WHICH rule was broken before the detail of how.
    """

    def __init__(self, rule: str, detail: str) -> None:
        super().__init__(f"contract rule broken: {rule} ({detail})")
        self.rule = rule
        self.detail = detail


def _refuse_unknown_fields(body: Mapping[str, Any], known: Sequence[str],
                           where: str) -> None:
    unknown = sorted(set(body) - set(known))
    if unknown:
        raise ContractError("fields are known", f"{where} carries {', '.join(unknown)}")


def _require_fields(body: Mapping[str, Any], required: Sequence[str],
                    where: str) -> None:
    missing = [name for name in required if name not in body]
    if missing:
        raise ContractError("required fields are present",
                            f"{where} lacks {', '.join(missing)}")


@dataclass(frozen=True)
class ContractCriterion:
    """One acceptance criterion of a mission's contract.

    ``milestones`` empty means the criterion covers the whole mission.  Every
    value is checked at construction, so no instance breaks a D2 rule.
    """

    id: str
    text: str
    origin: str
    blocking: bool = True
    milestones: tuple[str, ...] = ()
    check: dict[str, Any] | None = None
    status: str = CRITERION_STATUS_OPEN
    evidence_ref: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not _CRITERION_ID_RE.match(self.id):
            raise ContractError("id is C plus three digits", f"got {self.id!r}")
        if not isinstance(self.text, str) or not self.text.strip():
            raise ContractError("text is non-empty", f"criterion {self.id}")
        if not isinstance(self.blocking, bool):
            raise ContractError("blocking is a bool",
                                f"criterion {self.id} has {self.blocking!r}")
        if self.origin not in CONTRACT_ORIGINS:
            raise ContractError("origin is template, planner or amendment",
                                f"criterion {self.id} has {self.origin!r}")
        if (not isinstance(self.milestones, tuple)
                or not all(isinstance(m, str) and m for m in self.milestones)
                or len(set(self.milestones)) != len(self.milestones)):
            raise ContractError("milestones is a list of distinct milestone ids",
                                f"criterion {self.id} has {self.milestones!r}")
        if self.check is not None and not isinstance(self.check, dict):
            raise ContractError("check is null or an object",
                                f"criterion {self.id} has {self.check!r}")
        if self.status not in CRITERION_STATUSES:
            raise ContractError("status is open, met or unmet",
                                f"criterion {self.id} has {self.status!r}")
        if self.evidence_ref is not None and (
                not isinstance(self.evidence_ref, str) or not self.evidence_ref):
            raise ContractError("evidence_ref is null or a non-empty string",
                                f"criterion {self.id} has {self.evidence_ref!r}")

    def to_json(self) -> dict[str, Any]:
        return {"id": self.id, "text": self.text, "blocking": self.blocking,
                "origin": self.origin, "milestones": list(self.milestones),
                "check": self.check, "status": self.status,
                "evidence_ref": self.evidence_ref}

    @classmethod
    def from_json(cls, body: Any) -> ContractCriterion:
        if not isinstance(body, dict):
            raise ContractError("criterion is an object", f"got {type(body).__name__}")
        _refuse_unknown_fields(body, _CRITERION_FIELDS, "a criterion")
        _require_fields(body, ("id", "text", "origin"), "a criterion")
        milestones = body.get("milestones", [])
        if not isinstance(milestones, list):
            raise ContractError("milestones is a list of distinct milestone ids",
                                f"criterion {body.get('id')!r} has {milestones!r}")
        return cls(id=body["id"], text=body["text"], origin=body["origin"],
                   blocking=body.get("blocking", True),
                   milestones=tuple(milestones),
                   check=body.get("check"),
                   status=body.get("status", CRITERION_STATUS_OPEN),
                   evidence_ref=body.get("evidence_ref"))


@dataclass(frozen=True)
class MissionContract:
    """A mission's contract: its criteria in order, its template, its amendments.

    ``amendments`` are stored verbatim; T004 rules an entry's fields.
    """

    criteria: tuple[ContractCriterion, ...]
    template: str | None = None
    amendments: tuple[dict[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if self.template is not None and (
                not isinstance(self.template, str) or not self.template):
            raise ContractError("template is a name or null", f"got {self.template!r}")
        if not isinstance(self.criteria, tuple) or not all(
                isinstance(c, ContractCriterion) for c in self.criteria):
            raise ContractError("criteria is a list", f"got {self.criteria!r}")
        seen: set[str] = set()
        for criterion in self.criteria:
            if criterion.id in seen:
                raise ContractError("id is unique in the contract",
                                    f"{criterion.id} appears twice")
            seen.add(criterion.id)
        if not isinstance(self.amendments, tuple) or not all(
                isinstance(a, dict) for a in self.amendments):
            raise ContractError("amendments is a list of objects",
                                f"got {self.amendments!r}")

    def to_json(self) -> dict[str, Any]:
        return {"schema": CONTRACT_SCHEMA, "template": self.template,
                "criteria": [c.to_json() for c in self.criteria],
                "amendments": [dict(a) for a in self.amendments]}

    @classmethod
    def from_json(cls, body: Any) -> MissionContract:
        if not isinstance(body, dict):
            raise ContractError("body is an object", f"got {type(body).__name__}")
        _refuse_unknown_fields(body, _CONTRACT_FIELDS, "the contract")
        _require_fields(body, ("schema", "criteria"), "the contract")
        if body["schema"] != CONTRACT_SCHEMA:
            raise ContractError(f"schema is {CONTRACT_SCHEMA}", f"got {body['schema']!r}")
        criteria = body["criteria"]
        if not isinstance(criteria, list):
            raise ContractError("criteria is a list", f"got {type(criteria).__name__}")
        amendments = body.get("amendments", [])
        if not isinstance(amendments, list):
            raise ContractError("amendments is a list of objects",
                                f"got {type(amendments).__name__}")
        return cls(criteria=tuple(ContractCriterion.from_json(c) for c in criteria),
                   template=body.get("template"),
                   amendments=tuple(amendments))


# ---------------------------------------------------------------------------
# Reading and writing the mission's record
# ---------------------------------------------------------------------------


def write_mission_contract(project_id: str, mission_id: str,
                           contract: MissionContract | dict[str, Any],
                           root: Path | None = None) -> MissionContract:
    """Validate a contract and store it on the mission record.

    A raw body is checked by the same rules a read applies, so nothing this
    writes can later fail to read.  Returns the contract as stored.
    """
    from packages.orchestration.mission_state import set_mission_contract

    body = (contract.to_json() if isinstance(contract, MissionContract)
            else contract)
    validated = MissionContract.from_json(body)
    set_mission_contract(project_id, mission_id, validated.to_json(), root)
    return validated


def read_mission_contract(mission: Any) -> MissionContract | None:
    """The mission's contract, None when it has none, or RAISE on a bad body."""
    body = getattr(mission, "contract", None)
    if body is None:
        return None
    return MissionContract.from_json(body)


# ---------------------------------------------------------------------------
# The job's slice
# ---------------------------------------------------------------------------


def job_contract_slice(contract: MissionContract,
                       milestone_id: str | None) -> tuple[ContractCriterion, ...]:
    """The criteria a job serving ``milestone_id`` answers for, in contract order.

    Whole-mission criteria (empty ``milestones``) always; a milestone's own
    criteria only when the job serves that milestone.  A job with no milestone
    gets the whole-mission criteria alone.
    """
    return tuple(c for c in contract.criteria
                 if not c.milestones
                 or (milestone_id is not None and milestone_id in c.milestones))


def read_job_milestone(job_id: str, root: Path | None = None) -> str | None:
    """The milestone a job was dispatched for, or None when it records none."""
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id, root)
    if job is None:
        return None
    value = (job.metadata or {}).get(JOB_MILESTONE_KEY)
    return value if isinstance(value, str) and value else None


def record_job_milestone(job_id: str, milestone_id: str,
                         root: Path | None = None) -> bool:
    """Record on a job's record the milestone it was dispatched for.

    Returns False and writes nothing when no readable job record exists.
    """
    from packages.orchestration.pingpong_job import load_job_plan_safe, save_job_plan

    job, _degraded = load_job_plan_safe(job_id, root)
    if job is None:
        return False
    job.metadata = {**(job.metadata or {}), JOB_MILESTONE_KEY: str(milestone_id)}
    save_job_plan(job, root)
    return True


# ---------------------------------------------------------------------------
# Rendering — one renderer for `mission contract` and `job contract`
# ---------------------------------------------------------------------------


def render_contract_lines(title: str, template: str | None,
                          criteria: Sequence[ContractCriterion]) -> list[str]:
    """The text lines both contract commands print, criteria in contract order."""
    lines = [title, f"  Template: {template or '(none)'}"]
    if not criteria:
        lines.append("  Criteria: (none)")
        return lines
    lines.append(f"  Criteria: {len(criteria)}")
    for c in criteria:
        scope = ", ".join(c.milestones) if c.milestones else "whole mission"
        kind = "blocking" if c.blocking else "advisory"
        lines.append(f"    {c.id}  {c.status:<5}  {kind:<8}  {c.origin:<9}  {scope}")
        lines.append(f"          {c.text}")
        if c.evidence_ref:
            lines.append(f"          evidence: {c.evidence_ref}")
    return lines
