"""F070 T001 — the OrchestratorMove schema: what the loop is allowed to decide.

One orchestrator provider call per iteration returns exactly one move. The move
is the ONLY thing the model gets to say, and this file is the whole vocabulary:

    dispatch_job · wait_on_decisions · declare_milestone_done ·
    declare_mission_achieved · abort_with_reason

**The authority boundary is this schema, not the prompt.** Remedy deliberately
does NOT define a move kind that creates a mission, edits a goal, or changes the
mission plan — so the loop cannot grant itself new goals no matter what the
model writes, and no prompt wording can widen the set. A response naming an
unlisted kind (``create_mission``, say) fails ``Literal`` validation and is a
parse-class failure like any other malformed answer. New goals travel the human
idea/approval path; that absence is the feature, not an oversight.

Conventions follow F005 structured outputs and the F061/F069 precedent: a small
model, ``extra="forbid"``, a REQUIRED ``schema_v`` (a bare ``Literal`` with no
default) and the version in a ``SCHEMA_V`` class constant. Like ``dod_v1`` and
``mission_plan_v1``, ``om1`` is registered in ``schemas.models.SCHEMA_REGISTRY``
— by that module, importing this one — because a move is PERSISTED in the
decision ledger and therefore has to be resolvable from its tag alone. The
shared bases come from :mod:`packages.orchestration.structured_base` so the
dependency stays one-directional.

Validation here is compile-time and refuses detectable nonsense rather than
deferring it to the executor: a kind whose required payload key is missing or
blank is rejected at parse time, so an executed move always carries what its
execution needs.
"""
from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import Field, model_validator

from packages.orchestration.structured_base import _Structured

#: The compact schema tag. Travels in every orchestrator prompt — keep it short.
ORCHESTRATOR_MOVE_SCHEMA_V = "om1"

#: Ask for the next job on a milestone. Payload: ``milestone_id``, ``step``.
MOVE_DISPATCH_JOB = "dispatch_job"
#: Nothing can proceed until a human answers an open decision. No payload.
MOVE_WAIT_ON_DECISIONS = "wait_on_decisions"
#: Claim a milestone's outcome is reached. Payload: ``milestone_id``.
MOVE_DECLARE_MILESTONE_DONE = "declare_milestone_done"
#: Claim the whole mission goal is met. No payload.
MOVE_DECLARE_MISSION_ACHIEVED = "declare_mission_achieved"
#: Give up, honestly and on the record. Payload: ``reason``.
MOVE_ABORT_WITH_REASON = "abort_with_reason"

#: Every kind the loop can execute, in the order the protocol document lists
#: them. THE authority boundary — see the module docstring for what is
#: deliberately absent and why.
ORCHESTRATOR_MOVE_KINDS: tuple[str, ...] = (
    MOVE_DISPATCH_JOB,
    MOVE_WAIT_ON_DECISIONS,
    MOVE_DECLARE_MILESTONE_DONE,
    MOVE_DECLARE_MISSION_ACHIEVED,
    MOVE_ABORT_WITH_REASON,
)

OrchestratorMoveKind = Literal[
    "dispatch_job",
    "wait_on_decisions",
    "declare_milestone_done",
    "declare_mission_achieved",
    "abort_with_reason",
]

#: Payload keys each kind REQUIRES, non-blank. A kind absent from this map
#: takes no payload of its own. Kept beside the kinds so the two cannot drift.
REQUIRED_PAYLOAD_KEYS: dict[str, tuple[str, ...]] = {
    MOVE_DISPATCH_JOB: ("milestone_id", "step"),
    MOVE_DECLARE_MILESTONE_DONE: ("milestone_id",),
    MOVE_ABORT_WITH_REASON: ("reason",),
}

#: How long a payload value may be. A move is an instruction, not a document;
#: an unbounded string here would travel into every ledger entry that follows.
MAX_PAYLOAD_VALUE_CHARS = 2000


class OrchestratorMove(_Structured):
    """One decision by the orchestrator role (schema ``om1``).

    ``payload`` is a flat string map on purpose: the ledger renders it for a
    human to read, and a nested structure would be a second place for the
    orchestrator to smuggle state the loop never validated.
    """

    SCHEMA_V: ClassVar[str] = ORCHESTRATOR_MOVE_SCHEMA_V
    schema_v: Literal["om1"]  # required: no default
    kind: OrchestratorMoveKind
    payload: dict[str, str] = Field(default_factory=dict)
    #: One line on WHY this move, for the ledger. Never load-bearing.
    rationale: str = ""

    @model_validator(mode="after")
    def _validate_payload(self) -> OrchestratorMove:
        for key in REQUIRED_PAYLOAD_KEYS.get(self.kind, ()):
            if not str(self.payload.get(key, "") or "").strip():
                raise ValueError(
                    f"move {self.kind!r} requires a non-empty "
                    f"payload key {key!r}")
        for key, value in self.payload.items():
            if len(str(value)) > MAX_PAYLOAD_VALUE_CHARS:
                raise ValueError(
                    f"payload value {key!r} is {len(str(value))} chars, over "
                    f"the {MAX_PAYLOAD_VALUE_CHARS}-char limit")
        return self
