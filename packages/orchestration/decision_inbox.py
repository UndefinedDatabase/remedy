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
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from packages.orchestration.dag_schedule import blocked_downstream
from packages.orchestration.decision_queue import export_decision_json, list_decisions
from packages.orchestration.escalation import find_task_decision

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

    MEASURED against the door itself, not against the card's type:
    ``ui_server._dispatch_decision_resolve`` calls
    ``escalation.answer_task_decision`` and nothing else, that function reaches
    a record only through ``find_task_decision``, and ``find_task_decision``
    iterates the job's ESCALATION RECORDS alone.  So of the eight producing
    branches of ``list_decisions`` only ``task_decision`` mints an id that list
    holds; every other id is refused.  Finding R-0693 carries the measurement
    and DECISION F031 D19 rules that this key is computed from the door's own
    predicate.

    Remedy deliberately does NOT branch on the card's ``type`` here, and a
    reader searching this file for such a branch should stop here: no fixture
    in this repository can tell that predicate apart from a type check, because
    the ``task_decision`` branch derives its id FROM the escalation record, so
    type and door-answerability coincide on every buildable fixture.  The
    door's own predicate is used because it is the door's rule, not because a
    test can currently catch the difference.
    """
    return find_task_decision(job, str(decision_id)) is not None


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
