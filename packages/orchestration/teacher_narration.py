"""
Teacher narration — Stage 1 of the teacher role (F255 T002).

Turns run-log events into plain sentences an operator can read while a mission
runs. DETERMINISTIC and ZERO-TOKEN by construction: narrating an event is a
lookup in ``NARRATED_EVENTS`` followed by string formatting, so two passes over
the same run log produce byte-identical output and the token ledger records no
call for either.

Remedy deliberately does NOT invent a description for an event outside
``NARRATED_EVENTS``. Run-log event names are free strings and no stable event
vocabulary exists (DECISION F255 D2), so an unrecognised name is narrated AS
unrecognised rather than guessed at — the honesty rule of
docs/agents/teacher_conventions.md applied to this module's own blind spot.

Remedy deliberately opens no file here and provides no writer. The caller
supplies events already read by the production reader
``packages.orchestration.timeline.load_run_events``, which is read-only and
already drops a malformed line rather than repairing it (DECISION F255 D5).
Keeping the read out of this module is what makes the read-only invariant a
property of the whole teacher path rather than a claim about part of it.

Public API::

    NARRATED_EVENTS      — the enumerated Stage 1 set: event name -> template
    UNKNOWN_FIELD        — what an absent template field renders as
    narrate_run_event(event) -> str
    narrate_run_events(events) -> list[str]
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

#: What an absent template field renders as. A narration that RAISED on a
#: missing field could stop a run the teacher is forbidden to touch, and one
#: that invented a value would break the honesty rule; both are worse than a
#: sentence that says plainly which part it does not know.
UNKNOWN_FIELD = "unknown"

#: The enumerated Stage 1 event set, in the order a job lives through them.
#: Each value is a template over the TOP-LEVEL fields of a run-log event
#: (packages/orchestration/run_log.py ``RunEvent``). Adding an entry here is
#: the only way to narrate a new event: that is the point of the enumeration.
NARRATED_EVENTS: dict[str, str] = {
    "job_created": "The job was created.",
    "planning_started": "Planning started.",
    "planning_completed": "Planning finished and produced a task list.",
    "planning_failed": "Planning failed: {message}",
    "workspace_materialized": "The workspace was prepared for this run.",
    "task_run_started": "A task started: {task_id}",
    "task_run_completed": "A task finished: {task_id} (outcome: {outcome})",
    "task_run_failed": "A task failed: {task_id} (outcome: {outcome})",
    "task_run_noop": "A task ran and changed nothing: {task_id}",
    "verification_passed": "Verification passed.",
    "verification_failed": "Verification failed: {message}",
}

#: How an event outside NARRATED_EVENTS is narrated. It names the event rather
#: than describing it, because describing it would be inventing.
UNRECOGNISED_TEMPLATE = "An event this teacher has no narration for: {event}"


class _FieldsWithUnknown(dict):
    """Formatting map that yields :data:`UNKNOWN_FIELD` for absent fields."""

    def __missing__(self, key: str) -> str:
        return UNKNOWN_FIELD


def narrate_run_event(event: Mapping[str, Any]) -> str:
    """Narrate ONE run-log event as a single plain sentence.

    Never raises and never calls a model. An event whose name is missing, is
    not a string, or is absent from :data:`NARRATED_EVENTS` is narrated as
    unrecognised.
    """
    fields = _FieldsWithUnknown(event)
    name = event.get("event")
    if not isinstance(name, str) or name not in NARRATED_EVENTS:
        return UNRECOGNISED_TEMPLATE.format_map(fields)
    return NARRATED_EVENTS[name].format_map(fields)


def narrate_run_events(events: list[Mapping[str, Any]]) -> list[str]:
    """Narrate a run log, one sentence per event, in the order given.

    The caller's order is preserved rather than re-sorted: ``load_run_events``
    already sorts by timestamp, and re-sorting here would silently disagree
    with the reader when a timestamp is missing.
    """
    return [narrate_run_event(event) for event in events]
