"""Decision inbox view — one calm read of everything a job is waiting on (F031 T001).

Derives the inbox from ``decision_queue.list_decisions`` and adds nothing to
storage: DECISION F031 D1 rules the decision queue a derived read view, so this
module performs NO I/O, opens no path and keeps no state of its own.  It exists
to add the three things a card needs and the queue does not carry: how long the
question has been waiting, how much work waits behind it, and whether the write
door can answer it at all.

Scoping is BY JOB and the route enforces it: ``/api/jobs/<job_id>/decisions``
loads exactly one job through ``ui_server._load_job``.  Remedy deliberately does
NOT take a project argument here and never reads a second job — a cross-job
inbox would need a scoping rule the route does not have, so it is not offered.

Public API::

    DECISION_INBOX_VERSION — int, payload version of the inbox document
    build_decision_inbox(job, events, now=None) -> dict
    decision_urgency(card) -> int
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from packages.orchestration.dag_schedule import blocked_downstream
from packages.orchestration.decision_queue import export_decision_json, list_decisions
from packages.orchestration.escalation import (
    ESCALATION_STATUS_OPEN,
    find_task_decision,
)

#: Payload version of the inbox document.  The three top-level key spellings
#: below are the ones ``remedy decision list --json`` already prints, so the
#: browser and the CLI describe one thing one way.
DECISION_INBOX_VERSION = 1


def _decision_age_seconds(created_at: Any, now: datetime) -> int | None:
    """Seconds a decision has been waiting, or None when its stamp is unreadable.

    ``created_at`` is written by ``datetime.isoformat()`` (see
    ``enqueue_task_decision`` in escalation.py).  A naive stamp is read as UTC,
    and the answer is clamped at 0 so a skewed or future clock reports 0 rather
    than a negative age.
    """
    try:
        created = datetime.fromisoformat(str(created_at))
    except (ValueError, TypeError):
        return None
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    return max(0, int((now - created).total_seconds()))


def _blocked_subtree_size(job: Any, payload: Any) -> int:
    """How much downstream work this decision holds up — 0 when it names no task.

    MEASURED, not assumed (source inventory Q3): only the ``task_decision``
    branch of ``list_decisions`` sets ``payload["task_id"]``, so
    ``task_decision`` is the only type whose count can be non-zero today.  A
    reader who does not know that would read the zeros as a bug.  An empty seed
    set makes ``blocked_downstream`` return the empty set by its own first
    branch, so every other type reports 0 with no special case here.
    """
    seeds: set[UUID] = set()
    if isinstance(payload, dict):
        try:
            seeds = {UUID(str(payload.get("task_id")))}
        except (ValueError, TypeError):
            seeds = set()
    # ``list_decisions`` accepts a JobPlan too, and a JobPlan has no ``.tasks``.
    tasks = getattr(job, "tasks", None) or ()
    return len(blocked_downstream(tasks, seeds))


def _answerable_by_decision_resolve(job: Any, decision_id: Any) -> bool:
    """Whether the write door's ``decision.resolve`` can answer this card.

    MEASURED against the door itself, not against the card's type.  The door
    ``ui_server._dispatch_decision_resolve`` now has TWO branches, and this
    predicate mirrors every refusal of theirs that is a property of the JOB.
    The door ALSO refuses a malformed ``args.answers`` (DECISION F031 D26), and
    this predicate deliberately does NOT mirror that one: it is a property of
    the REQUEST BODY, invisible to a card, and a card is answerable whenever a
    well-formed request would be accepted.

    An ``fp:``-prefixed id is DECISION F031 D24's branch: the door hands it to
    ``flight_plan.resolve_flight_plan_approval`` and refuses unless
    ``job.flight_plan`` is a dict whose ``_approval`` is ``"pending"``.  Those
    are the same two readings of the same object the door makes, taken from the
    job rather than from the card, so the two cannot drift apart silently.

    Every OTHER id reaches ``escalation.answer_task_decision``, which refuses
    on two conditions of its own.  EXISTENCE is enforced by
    ``find_task_decision``, which iterates the job's ESCALATION RECORDS alone,
    so of the eight producing branches of ``list_decisions`` only
    ``task_decision`` mints a non-``fp:`` id that list holds; every other such
    id is refused.  BEING OPEN is enforced one line later in
    ``answer_task_decision`` itself, which returns None unless
    ``record.get("status")`` equals ``ESCALATION_STATUS_OPEN``, and the caller
    answers that None with 409 ``rejected_state``.  Both conditions are read
    here from the same record the door reads.  Finding R-0693 carries the first
    measurement and R-0695 the second; DECISION F031 D19 rules that this key is
    computed from the door's own predicate and DECISION F031 D21 that it
    mirrors what the door REFUSES.

    Remedy deliberately does NOT branch on the card's ``type`` here, and a
    reader searching this file for such a branch should stop here: a type check
    and the door's predicate NO LONGER COINCIDE, because an ANSWERED task
    decision still yields a card of type ``task_decision`` — branch 8 of
    ``list_decisions`` appends every escalation record and lets ``is_open``
    decide only the status — while the door refuses that record.  The ``fp:``
    test above reads the ID PREFIX rather than the type for that very reason
    and not in defiance of it: the door dispatches on the prefix, while the
    type ``flight_plan_approval`` is also what the RESOLVED card carries and
    the door refuses that one.  Section (g) of
    ``tests/orchestration/test_decision_inbox.py`` builds exactly those
    fixtures, so this file no longer rests on an absence: the difference
    between the two predicates is caught by a test.
    """
    if str(decision_id).startswith("fp:"):
        flight_plan = getattr(job, "flight_plan", None)
        return (isinstance(flight_plan, dict)
                and flight_plan.get("_approval") == "pending")
    record = find_task_decision(job, str(decision_id))
    return record is not None and record.get("status") == ESCALATION_STATUS_OPEN


def decision_urgency(card: dict[str, Any]) -> int:
    """How urgent one card is, as the single number a reader sorts the inbox by.

    THE SINGLE HOME of the rule, per DECISION F040 D2.  The browser carries a
    second copy today — ``decisionUrgency`` in
    ``apps/ui/src/api/decisionOrder.ts`` — and the two are PINNED equal by
    ``tests/ui_contracts/test_decision_urgency_parity.py`` rather than trusted,
    so a reader who changes one is sent to the other.  F040 T002 retires the
    TypeScript copy and leaves this function as the only one.

    Reads exactly the two keys ``build_decision_inbox`` already sets on every
    card, ``blocked_count`` and ``age_seconds``, and TOTAL by construction: no
    input makes this raise.  An age or a blocked size this module cannot trust
    — a missing key, a None, a bool, a string, a NaN or an infinity — scores as
    nothing rather than sorting ahead of a real one.
    """

    def _real_number(value: Any) -> float | None:
        """The value as a real number, or None when it is not a measurement.

        A bool is an ``int`` in Python and would otherwise score as 0 or 1 by
        accident; a NaN compares unequal to itself and would make the order
        depend on which pair happened to be compared; an infinity would
        dominate every card at every age.  None of the three is a measurement.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        if value != value or value in (float("inf"), float("-inf")):
            return None
        return float(value)

    # A None age is the endpoint's own answer for an unreadable ``created_at``
    # (see ``_decision_age_seconds`` above), which is not evidence of urgency;
    # a negative age means the clocks disagree.  Both score 0.
    raw_age = _real_number(card.get("age_seconds"))
    age = raw_age if raw_age is not None and raw_age > 0 else 0.0
    # A card that blocks NOTHING must SCORE as blocking nothing, so a negative
    # count is clamped here rather than eating into the age beside it.
    raw_blocked = _real_number(card.get("blocked_count"))
    blocked = max(0.0, raw_blocked) if raw_blocked is not None else 0.0
    # WHY THE ``+ 1``, which a reader standing at this expression will not have:
    # DECISION F031 D6 records that a literal ``blocked * age`` collapses every
    # card that blocks NOTHING to exactly 0 whatever its age, so a question
    # asked a week ago and one asked a second ago tie and their order becomes
    # whatever the endpoint happened to send.  Adding one keeps blocked size
    # dominant — one blocked task doubles a card's score — and leaves age as the
    # total order among the cards that block nothing.
    return int((blocked + 1) * age)


def build_decision_inbox(
    job: Any,
    events: list[dict[str, Any]],
    now: datetime | None = None,
) -> dict[str, Any]:
    """The inbox document for one job: every decision as a renderable card.

    Additive over ``export_decision_json``: each card carries exactly three
    extra keys, ``age_seconds``, ``blocked_count`` and
    ``answerable_by_decision_resolve``.  No input makes this function
    raise — an unreadable ``created_at`` gives a None age, a task id that is not
    a UUID gives 0 blocked, and the card still renders.  Being honest about an
    unreadable entry is the point; hiding it would lose the question.
    """
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)

    cards: list[dict[str, Any]] = []
    for decision in list_decisions(job, events):
        card = export_decision_json(decision)
        card["age_seconds"] = _decision_age_seconds(decision.created_at, moment)
        card["blocked_count"] = _blocked_subtree_size(job, decision.payload)
        card["answerable_by_decision_resolve"] = _answerable_by_decision_resolve(
            job, decision.id
        )
        cards.append(card)

    return {
        "version": DECISION_INBOX_VERSION,
        "job_id": str(getattr(job, "job_id", None) or getattr(job, "id", "")),
        "decisions": cards,
    }
