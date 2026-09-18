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

A criterion's ``check`` is compiled by F061's compiler, called here and never
re-implemented (DECISION F269 D4 (1)): :func:`compile_contract_criteria`
hands the criteria to ``dod_compiler.compile_dod`` as one task each, and
``mission_compiler.plan_mission`` writes one planner criterion per milestone
through :func:`write_planner_criteria` (D4 (2)).  This module never RUNS a
check: the job's own gate in ``dod_gate.py`` does.  At dispatch the
orchestrator merges a job's slice checks into that job's DoD
(:func:`merge_contract_slice_into_dod`, D4 (3); a whole-mission criterion's
check enters it as a reported, non-blocking check, D6 (1)), and after the job ran it
reads the gate's verdict back onto the slice criteria
(:func:`record_contract_results`, D4 (4)).  Beside that merge, both sites bind
the job to its repository and grant it what the repository commands check
(:func:`grant_contract_job_repository`, D7).

An operator message after the order is an AMENDMENT (DECISION F269 D8):
:func:`amend_mission_contract` adds its criterion and appends its entry
``{"id", "text", "received_at", "applies_from", "criteria", "understood",
"acknowledged_in"}``, whose rules are checked on read and on write like
every other D2 rule.  The orchestrator loop acknowledges each amendment in
its ledger in the round it applies from (:func:`due_contract_amendments`,
:func:`record_amendments_acknowledged`).

When a run stops at its budget with blocking criteria open, the REMAINDER is
proposed to the operator (DECISION F269 D9):
:func:`raise_contract_remainder_decision` puts one decision in the inbox
carrying the prefilled follow-up order, and a one-word ``yes`` at either
answer door starts that follow-up mission through
:func:`start_remainder_follow_up_mission`.

The names ``save_contract`` and ``load_contract`` belong to
``run_contract.py`` (a job's run contract, a different record) and are not
used here.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timezone
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

#: A compiled criterion's check id is this prefix plus the criterion id (D4 (1)).
CONTRACT_CHECK_ID_PREFIX = "ctr-"

_CRITERION_ID_RE = re.compile(r"^C\d{3}$")
_AMENDMENT_ID_RE = re.compile(r"^A\d{3}$")
_CONTRACT_FIELDS = ("schema", "template", "criteria", "amendments")
_CRITERION_FIELDS = ("id", "text", "blocking", "origin", "milestones", "check",
                     "status", "evidence_ref")
#: An amendment entry's fields, every one required (DECISION F269 D8 (1)).
_AMENDMENT_FIELDS = ("id", "text", "received_at", "applies_from", "criteria",
                     "understood", "acknowledged_in")


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


def _is_round(value: Any) -> bool:
    """A loop round number: an int of at least 1, and never a bool."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _check_amendment(body: dict[str, Any],
                     criteria: Mapping[str, ContractCriterion]) -> None:
    """Refuse an amendment entry that breaks a DECISION F269 D8 (1) rule."""
    _refuse_unknown_fields(body, _AMENDMENT_FIELDS, "an amendment")
    _require_fields(body, _AMENDMENT_FIELDS, "an amendment")
    ident = body["id"]
    if not isinstance(ident, str) or not _AMENDMENT_ID_RE.match(ident):
        raise ContractError("amendment id is A plus three digits", f"got {ident!r}")
    if not isinstance(body["text"], str) or not body["text"].strip():
        raise ContractError("amendment text is non-empty", f"amendment {ident}")
    received = body["received_at"]
    try:
        datetime.fromisoformat(received)
    except (TypeError, ValueError):
        raise ContractError("received_at is an ISO timestamp",
                            f"amendment {ident} has {received!r}") from None
    if not _is_round(body["applies_from"]):
        raise ContractError("applies_from is a round of at least 1",
                            f"amendment {ident} has {body['applies_from']!r}")
    added = body["criteria"]
    if (not isinstance(added, list)
            or not all(isinstance(c, str) for c in added)
            or len(set(added)) != len(added)
            or not all(c in criteria and criteria[c].origin == "amendment"
                       for c in added)):
        raise ContractError("amendment criteria are amendment criteria of the contract",
                            f"amendment {ident} has {added!r}")
    if not isinstance(body["understood"], str) or not body["understood"].strip():
        raise ContractError("understood is non-empty", f"amendment {ident}")
    acknowledged = body["acknowledged_in"]
    if acknowledged is not None and (
            not _is_round(acknowledged) or acknowledged < body["applies_from"]):
        raise ContractError("acknowledged_in is null or a round not before applies_from",
                            f"amendment {ident} has {acknowledged!r}")


@dataclass(frozen=True)
class MissionContract:
    """A mission's contract: its criteria in order, its template, its amendments.

    An amendment is a dict with the fields DECISION F269 D8 (1) rules, checked
    here, so a read and a write refuse the same broken entry.
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
        by_id = {c.id: c for c in self.criteria}
        amendment_ids: set[str] = set()
        for amendment in self.amendments:
            _check_amendment(amendment, by_id)
            if amendment["id"] in amendment_ids:
                raise ContractError("amendment id is unique in the contract",
                                    f"{amendment['id']} appears twice")
            amendment_ids.add(amendment["id"])

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
# Compiling the criteria — F061's compiler, called (DECISION F269 D4 (1), (2))
# ---------------------------------------------------------------------------


def compile_contract_criteria(
        criteria: Sequence[ContractCriterion],
        call_fn: Callable[[str, int], str] | None = None,
) -> tuple[ContractCriterion, ...]:
    """Give every criterion its check, compiled by ``dod_compiler.compile_dod``.

    The criteria become a ``TaskPlan`` of one task each — task id = criterion
    id, the one acceptance line = the criterion text — and each criterion
    takes the FIRST compiled check whose ``acceptance_refs`` holds
    ``<criterion id>:0``, re-labelled as its own: id ``ctr-<criterion id>``,
    that one ref, and the criterion's own ``blocking``.  F061's traceability
    rule guarantees such a check exists.  ``call_fn=None`` is the compiler's
    own deterministic path.
    """
    from packages.orchestration.dod_compiler import acceptance_line_key, compile_dod
    from packages.orchestration.schemas.models import TASK_PLAN_SCHEMA_V, TaskPlan

    if not criteria:
        return ()
    plan = TaskPlan(schema_v=TASK_PLAN_SCHEMA_V, tasks=[
        {"id": c.id, "title": c.id, "goal": c.text, "acceptance": [c.text],
         "est_tokens_band": "M"}
        for c in criteria])
    dod = compile_dod({}, plan, call_fn).dod
    compiled: list[ContractCriterion] = []
    for criterion in criteria:
        ref = acceptance_line_key(criterion.id, 0)
        check = next(c for c in dod.checks if ref in c.acceptance_refs)
        body = check.model_dump(mode="json")
        body.update(id=f"{CONTRACT_CHECK_ID_PREFIX}{criterion.id}",
                    acceptance_refs=[ref], blocking=criterion.blocking)
        compiled.append(replace(criterion, check=body))
    return tuple(compiled)


def write_planner_criteria(project_id: str, mission_id: str, plan: Any,
                           root: Path | None = None) -> MissionContract:
    """Write the mission's contract after its plan is compiled (D4 (2)).

    Every criterion whose origin is not ``planner`` is kept with its id; the
    planner criteria are replaced by one per milestone of ``plan`` — text =
    the milestone's goal, scoped to that milestone, blocking — with fresh ids
    after the highest kept one.  The new criteria, and any kept criterion that
    has no check yet, are compiled with no provider; a kept check is kept.
    """
    from packages.orchestration.mission_state import load_mission

    existing = read_mission_contract(load_mission(project_id, mission_id, root))
    kept = [c for c in (existing.criteria if existing else ())
            if c.origin != "planner"]
    first = max((int(c.id[1:]) for c in kept), default=0) + 1
    planner = [ContractCriterion(id=f"C{number:03d}", text=milestone.goal,
                                 origin="planner", milestones=(milestone.id,))
               for number, milestone in enumerate(plan.milestones, start=first)]
    compiled = compile_contract_criteria(
        [c for c in kept if c.check is None] + planner)
    by_id = {c.id: c for c in compiled}
    criteria = tuple(by_id.get(c.id, c) for c in kept) + tuple(
        by_id[c.id] for c in planner)
    contract = MissionContract(
        criteria=criteria,
        template=existing.template if existing else None,
        amendments=existing.amendments if existing else ())
    return write_mission_contract(project_id, mission_id, contract, root)


# ---------------------------------------------------------------------------
# Amendments (DECISION F269 D8)
# ---------------------------------------------------------------------------


def amend_mission_contract(project_id: str, mission_id: str, text: str, *,
                           milestones: Sequence[str] = (),
                           blocking: bool = True,
                           root: Path | None = None,
                           now: datetime | None = None) -> MissionContract:
    """Amend a mission's contract from an operator message (D8 (2)).

    Creates the contract when the mission has none; adds ONE criterion — the
    message as its text, origin ``amendment``, whole-mission unless
    ``milestones`` are given, compiled by F061's compiler with the next free
    id — and appends the amendment entry, whose ``applies_from`` is the
    mission's next loop round (``orchestrator_loop.next_iteration_index``).
    Every job dispatched from that round on takes the new check in its DoD at
    dispatch (D8 (3)); the loop acknowledges the entry in that round (D8 (4)).
    No existing criterion or entry is edited.  No command calls this: F264
    owns the route an amendment arrives by.
    """
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.orchestrator_loop import next_iteration_index

    existing = read_mission_contract(load_mission(project_id, mission_id, root))
    criteria = existing.criteria if existing else ()
    amendments = existing.amendments if existing else ()
    criterion_id = f"C{max((int(c.id[1:]) for c in criteria), default=0) + 1:03d}"
    [criterion] = compile_contract_criteria([ContractCriterion(
        id=criterion_id, text=text, origin="amendment", blocking=blocking,
        milestones=tuple(milestones))])
    amendment_id = f"A{max((int(a['id'][1:]) for a in amendments), default=0) + 1:03d}"
    kind = "blocking" if blocking else "advisory"
    amendment = {
        "id": amendment_id,
        "text": text,
        "received_at": (now or datetime.now(timezone.utc)).isoformat(),
        "applies_from": next_iteration_index(project_id, mission_id, root),
        "criteria": [criterion_id],
        "understood": f"adds {kind} criterion {criterion_id}: {text}",
        "acknowledged_in": None,
    }
    contract = MissionContract(
        criteria=(*criteria, criterion),
        template=existing.template if existing else None,
        amendments=(*amendments, amendment))
    return write_mission_contract(project_id, mission_id, contract, root)


def due_contract_amendments(contract: MissionContract | None,
                            round_number: int) -> tuple[dict[str, Any], ...]:
    """The amendments a loop round must acknowledge, in contract order (D8 (4)).

    Every amendment whose ``applies_from`` is at most ``round_number`` and whose
    ``acknowledged_in`` is still null; a mission with no contract has none.
    """
    if contract is None:
        return ()
    return tuple(a for a in contract.amendments
                 if a["applies_from"] <= round_number and a["acknowledged_in"] is None)


def record_amendments_acknowledged(project_id: str, mission_id: str,
                                   amendment_ids: Sequence[str], round_number: int,
                                   root: Path | None = None) -> MissionContract:
    """Set ``acknowledged_in`` to ``round_number`` on the named amendments (D8 (4)).

    The one field an acknowledgement writes; every other field of every entry,
    and every criterion, is written back as it was read.
    """
    from packages.orchestration.mission_state import load_mission

    contract = read_mission_contract(load_mission(project_id, mission_id, root))
    if contract is None:
        raise ContractError("an acknowledged amendment is in the contract",
                            f"mission {mission_id} has no contract")
    wanted = set(amendment_ids)
    amendments = tuple({**a, "acknowledged_in": round_number} if a["id"] in wanted else a
                       for a in contract.amendments)
    return write_mission_contract(
        project_id, mission_id, replace(contract, amendments=amendments), root)


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
# The job's DoD carries its slice, and the job's gate decides it (D4 (3), (4))
# ---------------------------------------------------------------------------


def _same_check(a_kind: Any, a_spec: Any, b_kind: Any, b_spec: Any) -> bool:
    """Two checks are the same check when their ``kind`` and ``spec`` are equal."""
    return a_kind == b_kind and a_spec == b_spec


def merge_contract_slice_into_dod(mission: Any, milestone_id: str | None,
                                  job_id: str) -> int:
    """Add a job's slice checks to its stored DoD; return how many were added.

    A slice criterion's check is added only when no check already in the DoD
    has the same ``kind`` and ``spec``; a job with no DoD gets one made of its
    slice checks.  A DoD file that will not parse is left alone — the gate
    already holds such a job, and overwriting it would hide that.  A mission
    with no contract, or a slice with no compiled check, changes nothing.

    DECISION F269 D6 (1): a whole-mission criterion's check enters the DoD
    with ``blocking`` false — a reported check the gate evaluates and never
    holds on, because it describes the mission's end state and one job of a
    many-milestone mission cannot meet it.  A milestone-scoped criterion's
    check keeps the criterion's ``blocking``.  The criterion's status still
    follows the evidence (:func:`record_contract_results`), so the mission
    gate still holds the achieve move on it.
    """
    from packages.orchestration.dod_gate import dod_path, load_dod, store_dod
    from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck

    contract = read_mission_contract(mission)
    if contract is None:
        return 0
    slice_checks = [DoDCheck.model_validate(
                        {**c.check, "blocking": c.blocking and bool(c.milestones)})
                    for c in job_contract_slice(contract, milestone_id)
                    if c.check is not None]
    if not slice_checks:
        return 0
    dod = load_dod(job_id)
    if dod is None and dod_path(job_id).is_file():
        return 0
    present = list(dod.checks) if dod is not None else []
    taken = {c.id for c in present}
    added: list[DoDCheck] = []
    for check in slice_checks:
        if any(_same_check(c.kind, c.spec, check.kind, check.spec)
               for c in present + added):
            continue
        ident, n = check.id, 2
        while ident in taken:
            ident, n = f"{check.id}-{n}", n + 1
        taken.add(ident)
        added.append(check.model_copy(update={"id": ident}))
    if not added:
        return 0
    store_dod(job_id, DoD(
        schema_v=DOD_SCHEMA_V, checks=present + added,
        compiled=dod.compiled if dod is not None else False,
        origin=dod.origin if dod is not None else "deterministic"))
    return len(added)


# ---------------------------------------------------------------------------
# The job's repository and grants come from the contract (DECISION F269 D7)
# ---------------------------------------------------------------------------

#: The grants a contract gives each of its jobs: exactly what `test run`,
#: `test discover`, `patch apply`, `patch revert` and `self execute` check.
CONTRACT_JOB_GRANTS = ("repo_test_run", "repo_generated_write", "repo_revert")

#: The job metadata key the repository binding is written under.
JOB_TARGET_REPO_KEY = "target_repo"


def _project_canonical_repo(project_id: str) -> str:
    """The project's canonical repository path, or "" when it has none."""
    from uuid import UUID

    from packages.orchestration.project_registry import ProjectNotFoundError, load_project

    try:
        project = load_project(UUID(str(project_id)))
    except (ValueError, ProjectNotFoundError, OSError):
        return ""
    return project.canonical_repo_path or ""


def grant_contract_job_repository(mission: Any, job_id: str,
                                  root: Path | None = None) -> dict[str, Any]:
    """Bind a contract's job to its repository and grant it the three capabilities.

    DECISION F269 D7: a contract is the operator's accepted order for its
    repository, so each of its jobs gets ``metadata["target_repo"]`` — the
    job's own ``repo_path``, else the project's canonical repository, else
    nothing — and the grants :data:`CONTRACT_JOB_GRANTS` allowed.  A
    ``target_repo`` already set is never overwritten and no grant is ever
    denied.  A mission with no contract, or no readable job record, writes
    nothing.  Returns the metadata entries written, for a caller holding the
    job in memory to carry the same values.
    """
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.pingpong_job import load_job_plan_safe, save_job_plan

    if read_mission_contract(mission) is None:
        return {}
    job, _degraded = load_job_plan_safe(job_id, root)
    if job is None:
        return {}
    if job.metadata is None:
        job.metadata = {}
    if not job.metadata.get(JOB_TARGET_REPO_KEY):
        repo = job.repo_path or _project_canonical_repo(
            getattr(mission, "project_id", ""))
        if repo:
            job.metadata[JOB_TARGET_REPO_KEY] = str(repo)
    for grant in CONTRACT_JOB_GRANTS:
        set_permission(job, Capability(grant), allow=True)
    save_job_plan(job, root)
    return {key: job.metadata[key] for key in (JOB_TARGET_REPO_KEY, "permissions")
            if key in job.metadata}


def record_contract_results(project_id: str, mission_id: str, job_id: str,
                            milestone_id: str | None,
                            root: Path | None = None) -> MissionContract | None:
    """Read a job's gate result back onto its slice criteria (D4 (4)).

    Each slice criterion whose check has the ``kind`` and ``spec`` of a check
    in the job's stored DoD becomes ``met`` when that check's evidence passed
    and ``unmet`` otherwise, with ``evidence_ref`` = ``<job id>:<check id>``.
    A job with no gate result, or no readable DoD, changes nothing and returns
    None; otherwise the contract as written is returned.
    """
    from packages.orchestration.dod_gate import load_dod, load_gate_result
    from packages.orchestration.dod_runners import STATUS_PASSED
    from packages.orchestration.mission_state import load_mission

    contract = read_mission_contract(load_mission(project_id, mission_id, root))
    if contract is None:
        return None
    result = load_gate_result(job_id)
    dod = load_dod(job_id)
    if result is None or dod is None:
        return None
    passed = {str(e.get("check_id")) for e in result.get("checks") or []
              if isinstance(e, dict) and e.get("status") == STATUS_PASSED}
    in_slice = {c.id for c in job_contract_slice(contract, milestone_id)}
    criteria: list[ContractCriterion] = []
    for criterion in contract.criteria:
        check = criterion.check
        match = None if criterion.id not in in_slice or check is None else next(
            (c for c in dod.checks
             if _same_check(c.kind, c.spec, check.get("kind"), check.get("spec"))),
            None)
        if match is not None:
            criterion = replace(
                criterion, status="met" if match.id in passed else "unmet",
                evidence_ref=f"{job_id}:{match.id}")
        criteria.append(criterion)
    return write_mission_contract(
        project_id, mission_id, replace(contract, criteria=tuple(criteria)), root)


# ---------------------------------------------------------------------------
# The mission gate (D4 (5))
# ---------------------------------------------------------------------------


def contract_blockers(contract: MissionContract | None) -> tuple[str, ...]:
    """The ids of the blocking criteria whose status is not ``met``, in order.

    These hold the orchestrator's ``declare_mission_achieved``; a mission with
    no contract has none.
    """
    if contract is None:
        return ()
    return tuple(c.id for c in contract.criteria
                 if c.blocking and c.status != "met")


# ---------------------------------------------------------------------------
# The remainder proposal (DECISION F269 D9)
# ---------------------------------------------------------------------------

#: The start of a remainder decision's question, and the WHOLE of its dedupe
#: key: the watchdog's precedent (DECISION F077 D2), because
#: ``enqueue_task_decision`` writes a fixed key set and the question is the one
#: field a caller controls.  A remainder decision is an ordinary
#: ``task_decision`` in the inbox; no decision type is added (D9).
CONTRACT_REMAINDER_MARKER = "[contract remainder]"

#: The one answer that starts the follow-up mission; any other only records.
CONTRACT_REMAINDER_YES = "yes"

#: The options a remainder decision offers.  It has no safe default: a human answers.
CONTRACT_REMAINDER_OPTIONS = (CONTRACT_REMAINDER_YES, "no")


def contract_blocking_criteria(
        contract: MissionContract | None) -> tuple[ContractCriterion, ...]:
    """The criteria :func:`contract_blockers` names, in contract order."""
    blockers = set(contract_blockers(contract))
    return () if contract is None else tuple(
        c for c in contract.criteria if c.id in blockers)


def contract_remainder_order(mission_id: str,
                             blockers: Sequence[ContractCriterion]) -> str:
    """The prefilled follow-up order a remainder decision carries (D9 (1))."""
    return (f"Meet the acceptance criteria mission {mission_id} left unmet: "
            f"{'; '.join(c.text for c in blockers)}.")


def raise_contract_remainder_decision(project_id: str, mission_id: str, *,
                                      root: Path | None = None,
                                      now: datetime | None = None) -> str | None:
    """Put the remainder of a mission's contract in front of the operator (D9 (1)).

    When the contract has blockers and no OPEN remainder decision exists on
    any of the mission's jobs, ONE decision is enqueued on the latest linked
    job's first task — the attachment ``escalate_repeated_refusal`` and the
    watchdog use.  Its question starts with :data:`CONTRACT_REMAINDER_MARKER`
    and names the mission and every blocker by id and text; its options are
    ``yes`` and ``no``; it has no safe default; its ``impact`` is the
    prefilled follow-up order.  Returns the decision id, or None when there
    are no blockers, an open remainder decision already exists, or the
    mission has no job with a task to attach one to.
    """
    from packages.orchestration.data_paths import normalize_job_id
    from packages.orchestration.escalation import enqueue_task_decision
    from packages.orchestration.mission_state import load_mission
    from packages.orchestration.orchestrator_loop import open_mission_decisions
    from packages.orchestration.pingpong_job import require_job_plan, save_job_plan

    mission = load_mission(project_id, mission_id, root)
    blockers = contract_blocking_criteria(read_mission_contract(mission))
    if not blockers:
        return None
    if any(str(record.get("question", "") or "").startswith(CONTRACT_REMAINDER_MARKER)
           for record in open_mission_decisions(mission)):
        return None
    link = mission.latest_link()
    if link is None:
        return None
    try:
        job = require_job_plan(normalize_job_id(link.job_id))
    except Exception:  # noqa: BLE001 — an unreadable job has no task to attach to
        return None
    tasks = list(getattr(job, "tasks", ()) or ())
    if not tasks:
        return None
    named = "; ".join(f"{c.id}: {c.text}" for c in blockers)
    record = enqueue_task_decision(
        job,
        task_id=tasks[0].task_id,
        question=(f"{CONTRACT_REMAINDER_MARKER} Mission {mission_id} stopped at its "
                  f"budget with {len(blockers)} blocking acceptance criteria not "
                  f"met — {named}. Start a follow-up mission to meet them?"),
        options=CONTRACT_REMAINDER_OPTIONS,
        safe_default="",
        impact=contract_remainder_order(mission_id, blockers),
        now=now or datetime.now(timezone.utc))
    save_job_plan(job)
    return str(record.get("decision_id", "")) or None


def start_remainder_follow_up_mission(job_id: str, record: Mapping[str, Any], *,
                                      root: Path | None = None,
                                      now: datetime | None = None) -> str | None:
    """Act on an answered remainder decision; return the follow-up mission's id (D9 (3)).

    Both answer doors call this after a ``td:`` decision was answered.  It acts
    only on a remainder decision (its question starts with
    :data:`CONTRACT_REMAINDER_MARKER`) answered exactly ``yes``: it creates the
    follow-up mission in the same project, whose goal and order are the
    prefilled order the decision carries, and whose contract is the blockers
    of the mission the job belongs to, copied in order and renumbered from
    ``C001`` — text, blocking, origin and check kept, whole-mission, ``open``,
    no evidence.  A compiled check is relabelled to its new criterion id (D4
    (1)'s ``ctr-<id>`` and ``<id>:0``).  Any other answer or decision, a job
    that belongs to no mission, or a mission with no blockers left, creates
    nothing and returns None.
    """
    from packages.orchestration.dod_compiler import acceptance_line_key
    from packages.orchestration.escalation import ESCALATION_STATUS_ANSWERED
    from packages.orchestration.mission_state import (
        MissionOrder,
        create_mission,
        mission_for_job,
        set_mission_order,
    )

    if not str(record.get("question", "") or "").startswith(CONTRACT_REMAINDER_MARKER):
        return None
    if (record.get("status") != ESCALATION_STATUS_ANSWERED
            or record.get("answer") != CONTRACT_REMAINDER_YES):
        return None
    mission = mission_for_job(str(job_id), root)
    if mission is None:
        return None
    blockers = contract_blocking_criteria(read_mission_contract(mission))
    if not blockers:
        return None
    order = (str(record.get("impact", "") or "")
             or contract_remainder_order(mission.id, blockers))
    criteria: list[ContractCriterion] = []
    for number, criterion in enumerate(blockers, start=1):
        ident = f"C{number:03d}"
        check = None if criterion.check is None else {
            **criterion.check, "id": f"{CONTRACT_CHECK_ID_PREFIX}{ident}",
            "acceptance_refs": [acceptance_line_key(ident, 0)]}
        criteria.append(ContractCriterion(
            id=ident, text=criterion.text, origin=criterion.origin,
            blocking=criterion.blocking, check=check))
    follow_up = create_mission(mission.project_id, order, now=now, root=root)
    set_mission_order(mission.project_id, follow_up.id, MissionOrder(text=order), root)
    write_mission_contract(mission.project_id, follow_up.id,
                           MissionContract(criteria=tuple(criteria)), root)
    return follow_up.id


# ---------------------------------------------------------------------------
# Rendering — one renderer for `mission contract` and `job contract`
# ---------------------------------------------------------------------------


def render_contract_lines(title: str, template: str | None,
                          criteria: Sequence[ContractCriterion],
                          amendments: Sequence[Mapping[str, Any]] = ()) -> list[str]:
    """The text lines both contract commands print, criteria in contract order.

    The amendments follow the criteria (DECISION F269 D8 (5)), each with its
    round of effect, its acknowledgement and the criteria it added; a contract
    with none prints no amendment section.
    """
    lines = [title, f"  Template: {template or '(none)'}"]
    if not criteria:
        lines.append("  Criteria: (none)")
    else:
        lines.append(f"  Criteria: {len(criteria)}")
    for c in criteria:
        scope = ", ".join(c.milestones) if c.milestones else "whole mission"
        kind = "blocking" if c.blocking else "advisory"
        lines.append(f"    {c.id}  {c.status:<5}  {kind:<8}  {c.origin:<9}  {scope}")
        lines.append(f"          {c.text}")
        if c.evidence_ref:
            lines.append(f"          evidence: {c.evidence_ref}")
    if amendments:
        lines.append(f"  Amendments: {len(amendments)}")
    for a in amendments:
        acknowledged = (f"acknowledged in round {a['acknowledged_in']}"
                        if a.get("acknowledged_in") is not None
                        else "not yet acknowledged")
        lines.append(f"    {a['id']}  applies from round {a['applies_from']}  "
                     f"{acknowledged}  adds {', '.join(a['criteria']) or 'nothing'}")
        lines.append(f"          {a['text']}")
    return lines
