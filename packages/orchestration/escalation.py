"""Escalate instead of block — the ``needs_decision`` task outcome (F051 T001).

A task that needs a human answer must not end the run.  It raises
``needs_decision``, ONE decision is enqueued for it, and the task is marked
awaiting-decision: its own branch pauses, every disjoint branch keeps running,
and the run stays resumable.  Awaiting is NOT failure — nothing was attempted
and lost, so the task keeps its PENDING status exactly as a rolled-back attempt
does, and the executor withholds its transitive downstream the same way it
withholds the downstream of a blocked task (``dag_schedule.blocked_downstream``).

Where the records live
----------------------
On ``job.metadata["escalations"]`` — a list of plain JSON-safe dicts.  This is
NOT a second decision queue: ``decision_queue`` stays the one read-only
aggregation over existing records and simply derives one ``task_decision``
entry per record, the same way it derives the flight-plan approval from
``job.flight_plan``.  Answering goes through the existing
``remedy decision resolve`` command.

Two tasks raising the same question produce TWO records (deduplication is a
human call, feature-file A9); they cross-reference each other by decision id so
whoever answers sees the pair.

Attended vs unattended
----------------------
A safe default is still ASKED in attended mode: the record is created open and
waits.  Only an unattended run (``--yes``) auto-applies the default, and then
the record says so (``answer_source="default"``) and lands in the escalation
assumption log.

Remedy deliberately does NOT write these into the flight plan's
``assumptions.md``: that log states in its own first paragraph that every
question in it was asked at plan time and nothing mid-run.  Mid-run escalations
therefore get their own ``escalation_assumptions.md`` in the same evidence area,
in the same table shape, rather than making the plan-time log lie.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.core.models import Job

#: The additive task outcome.  A task step reports it instead of a failure when
#: it cannot proceed without a human answer.
TASK_OUTCOME_NEEDS_DECISION = "needs_decision"

#: ``decision_queue`` type for a derived task decision.  Additive: every
#: existing producer keeps its own type.
DECISION_TYPE_TASK_DECISION = "task_decision"

#: Where the records live on the job.  One key, additive, JSON-safe.
JOB_METADATA_ESCALATIONS_KEY = "escalations"

ESCALATION_STATUS_OPEN = "open"
ESCALATION_STATUS_ANSWERED = "answered"

#: Who supplied the answer.  Same vocabulary as the flight-plan clarifications.
ANSWER_SOURCE_HUMAN = "human"
ANSWER_SOURCE_DEFAULT = "default"

#: Decision-id prefix for a task decision — the namespace ``decision resolve``
#: dispatches on, next to ``sr:`` (stop reason) and ``fp:`` (flight plan).
DECISION_ID_PREFIX = "td:"

#: Task inputs key carrying the answers a task's decisions received, so the
#: next attempt of that task can actually use them.
TASK_INPUTS_ANSWERS_KEY = "decision_answers"

#: Filename of the mid-run assumption log inside the job's evidence area.
ESCALATION_ASSUMPTIONS_FILENAME = "escalation_assumptions.md"

__all__ = [
    "ANSWER_SOURCE_DEFAULT",
    "ANSWER_SOURCE_HUMAN",
    "DECISION_ID_PREFIX",
    "DECISION_TYPE_TASK_DECISION",
    "ESCALATION_ASSUMPTIONS_FILENAME",
    "ESCALATION_STATUS_ANSWERED",
    "ESCALATION_STATUS_OPEN",
    "JOB_METADATA_ESCALATIONS_KEY",
    "TASK_INPUTS_ANSWERS_KEY",
    "TASK_OUTCOME_NEEDS_DECISION",
    "answer_task_decision",
    "answered_task_decisions",
    "auto_apply_safe_default",
    "awaiting_decision_task_ids",
    "enqueue_task_decision",
    "escalation_records",
    "find_task_decision",
    "open_task_decisions",
    "render_escalation_assumptions_md",
    "task_decision_answer_command",
    "write_escalation_assumptions_md",
]


def _metadata(job: Job | Any) -> dict[str, Any]:
    """The job's metadata dict, created on first use.

    Both Core ``Job`` and the pingpong ``JobPlan`` are accepted; a job shape
    without metadata at all gets an empty dict rather than an AttributeError,
    because a missing metadata store means "no escalations", not a crash.
    """
    meta = getattr(job, "metadata", None)
    if not isinstance(meta, dict):
        meta = {}
        try:
            job.metadata = meta
        except (AttributeError, ValueError):  # frozen or validated shapes
            pass
    return meta


def escalation_records(job: Job | Any) -> list[dict[str, Any]]:
    """Every escalation record on *job*, in creation order.

    The live list is returned, so callers that append go through the helpers
    below rather than mutating it themselves.
    """
    records = _metadata(job).get(JOB_METADATA_ESCALATIONS_KEY)
    if not isinstance(records, list):
        return []
    return [r for r in records if isinstance(r, dict)]


def _stored_records(job: Job | Any) -> list[dict[str, Any]]:
    """The stored list itself, created if absent — the write path."""
    meta = _metadata(job)
    records = meta.get(JOB_METADATA_ESCALATIONS_KEY)
    if not isinstance(records, list):
        records = []
        meta[JOB_METADATA_ESCALATIONS_KEY] = records
    return records


def open_task_decisions(job: Job | Any) -> list[dict[str, Any]]:
    """Records still waiting for an answer, in creation order."""
    return [r for r in escalation_records(job)
            if r.get("status") == ESCALATION_STATUS_OPEN]


def answered_task_decisions(job: Job | Any) -> list[dict[str, Any]]:
    """Records that have an answer — human or auto-applied default."""
    return [r for r in escalation_records(job)
            if r.get("status") == ESCALATION_STATUS_ANSWERED]


def awaiting_decision_task_ids(job: Job | Any) -> set[UUID]:
    """Task ids whose branch is paused on an OPEN decision.

    This is what the executor withholds from the ready set: the tasks
    themselves and — through ``blocked_downstream`` — everything depending on
    them.  Answering a decision empties this set for that task with no further
    bookkeeping, which is why the awaiting state is derived and never stored
    twice.
    """
    awaiting: set[UUID] = set()
    for record in open_task_decisions(job):
        try:
            awaiting.add(UUID(str(record.get("task_id"))))
        except (TypeError, ValueError):
            continue                        # a malformed id blocks nothing
    return awaiting


def find_task_decision(job: Job | Any, decision_id: str) -> dict[str, Any] | None:
    """The record with this decision id, or None."""
    for record in escalation_records(job):
        if record.get("decision_id") == decision_id:
            return record
    return None


def task_decision_answer_command(job_id: str, decision_id: str,
                                 answer: str = "<your answer>") -> str:
    """The EXACT command that answers this decision.

    Rendered into the decision's next actions and into the status/report views,
    so what a human reads is what a human can paste.
    """
    return (f'remedy decision resolve {str(job_id)[:8]} {decision_id} '
            f'--reason "{answer}"')


def _next_decision_id(records: Iterable[Mapping[str, Any]], task_id: Any) -> str:
    """``td:<task8>`` for a task's first decision, ``td:<task8>-<n>`` after.

    Task-scoped and deterministic: no clock and no randomness, so the same
    sequence of escalations always produces the same ids across a resume.
    """
    task_str = str(task_id)
    try:
        task_hex = UUID(task_str).hex[:8]
    except (TypeError, ValueError):
        task_hex = task_str[:8]
    seen = sum(1 for r in records if str(r.get("task_id")) == task_str)
    return (f"{DECISION_ID_PREFIX}{task_hex}" if seen == 0
            else f"{DECISION_ID_PREFIX}{task_hex}-{seen + 1}")


def _normalized_question(text: Any) -> str:
    """Whitespace- and case-insensitive question key for cross-referencing."""
    return " ".join(str(text or "").split()).casefold()


def enqueue_task_decision(
    job: Job | Any,
    *,
    task_id: Any,
    question: str,
    options: Iterable[str] = (),
    safe_default: str = "",
    impact: str = "",
    now: datetime,
) -> dict[str, Any]:
    """Enqueue ONE decision for *task_id* and return its record.

    One call, one record — a task raising the same question twice really did
    ask twice.  Records whose question matches an existing OPEN one are
    cross-referenced in both directions (``cross_references``) so a human sees
    the pair without the code guessing they are the same call.
    """
    records = _stored_records(job)
    decision_id = _next_decision_id(records, task_id)
    question_key = _normalized_question(question)

    siblings = [r for r in records
                if r.get("status") == ESCALATION_STATUS_OPEN
                and _normalized_question(r.get("question")) == question_key]

    record: dict[str, Any] = {
        "decision_id": decision_id,
        "task_id": str(task_id),
        "question": str(question),
        "options": [str(o) for o in options],
        "safe_default": str(safe_default or ""),
        "impact": str(impact or ""),
        "status": ESCALATION_STATUS_OPEN,
        "answer": "",
        "answer_source": "",
        "created_at": now.isoformat(),
        "answered_at": "",
        "cross_references": [str(r.get("decision_id")) for r in siblings],
    }
    for sibling in siblings:
        refs = sibling.setdefault("cross_references", [])
        if isinstance(refs, list) and decision_id not in refs:
            refs.append(decision_id)
    records.append(record)
    return record


def _record_answer_on_task(job: Job | Any, record: Mapping[str, Any]) -> None:
    """Put the answer where the next attempt of that task will read it.

    Without this the branch would resume as ignorant as it paused.  Additive:
    tasks that never escalated keep their inputs untouched.
    """
    task_id = str(record.get("task_id"))
    for task in getattr(job, "tasks", ()) or ():
        # F112 T003b2b1: pingpong JobPlan's TaskEntry carries `task_id`
        # (a plain string), never Core Job's Task.id (a UUID) — accept
        # either shape rather than assuming the Core one, matching
        # _metadata()'s own "both Core Job and pingpong JobPlan" contract.
        task_identifier = getattr(task, "id", None)
        if task_identifier is None:
            task_identifier = getattr(task, "task_id", None)
        if str(task_identifier) != task_id:
            continue
        inputs = task.inputs if isinstance(task.inputs, dict) else {}
        answers = inputs.get(TASK_INPUTS_ANSWERS_KEY)
        if not isinstance(answers, dict):
            answers = {}
            inputs[TASK_INPUTS_ANSWERS_KEY] = answers
        answers[str(record.get("decision_id"))] = str(record.get("answer", ""))
        return


def answer_task_decision(
    job: Job | Any,
    decision_id: str,
    *,
    answer: str,
    source: str = ANSWER_SOURCE_HUMAN,
    now: datetime,
) -> dict[str, Any] | None:
    """Answer an OPEN decision and return the updated record.

    Returns None when no such decision exists.  Answering one that is already
    answered is refused the same way — answers are written once, so a late
    second answer cannot silently overwrite the one the run acted on.
    """
    record = find_task_decision(job, decision_id)
    if record is None or record.get("status") != ESCALATION_STATUS_OPEN:
        return None
    record["status"] = ESCALATION_STATUS_ANSWERED
    record["answer"] = str(answer)
    record["answer_source"] = str(source)
    record["answered_at"] = now.isoformat()
    _record_answer_on_task(job, record)
    return record


def auto_apply_safe_default(
    job: Job | Any,
    record: Mapping[str, Any],
    *,
    now: datetime,
) -> dict[str, Any] | None:
    """Apply *record*'s safe default — unattended runs only.

    The caller decides whether the run is unattended; this function only
    refuses records that have no default to apply.  A default applied here is
    marked ``answer_source="default"`` and therefore shows up in the escalation
    assumption log, which is the whole point of recording it.
    """
    if not str(record.get("safe_default") or ""):
        return None
    return answer_task_decision(
        job, str(record.get("decision_id")),
        answer=str(record["safe_default"]),
        source=ANSWER_SOURCE_DEFAULT,
        now=now,
    )


def _cell(text: Any) -> str:
    """Make a value safe for a markdown table cell."""
    return " ".join(str(text or "").split()).replace("|", "\\|") or "-"


def render_escalation_assumptions_md(job: Job | Any) -> str:
    """The mid-run assumption log: what was asked, answered, and by whom.

    Deliberately separate from the flight plan's ``assumptions.md`` — see the
    module docstring.  Same table shape, so a reviewer reads both the same way.
    """
    records = escalation_records(job)

    lines = ["# Escalation assumptions", ""]
    lines.append(
        "Questions raised BY A TASK DURING THE RUN. Each one paused only its "
        "own branch; the run continued on every disjoint branch.")
    lines.append("")

    if not records:
        lines.append("No escalations — no task needed a decision.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| Decision | Task | Question | Answer | Source | Impact |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for record in records:
        source = str(record.get("answer_source") or "")
        lines.append(
            f"| {_cell(record.get('decision_id'))} "
            f"| {_cell(str(record.get('task_id'))[:8])} "
            f"| {_cell(record.get('question'))} "
            f"| {_cell(record.get('answer'))} "
            f"| {_cell(source or 'unanswered')} "
            f"| {_cell(record.get('impact'))} |")
    lines.append("")

    human = sum(1 for r in records if r.get("answer_source") == ANSWER_SOURCE_HUMAN)
    default = sum(1 for r in records if r.get("answer_source") == ANSWER_SOURCE_DEFAULT)
    still_open = sum(1 for r in records if r.get("status") == ESCALATION_STATUS_OPEN)
    lines.append(
        f"Sources: {human} human, {default} default, {still_open} unresolved.")
    lines.append("")
    return "\n".join(lines)


def write_escalation_assumptions_md(job: Job | Any, evidence_dir: Path) -> Path:
    """Write the mid-run assumption log into the job's evidence area."""
    evidence_dir = Path(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / ESCALATION_ASSUMPTIONS_FILENAME
    path.write_text(render_escalation_assumptions_md(job), encoding="utf-8")
    return path
