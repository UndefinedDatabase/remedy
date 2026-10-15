"""amend1015 Part 1: ONE answer to "is this task done?" for every surface that counts tasks.

Before this module the cockpit counted a task as done only when its status was exactly
``"completed"`` — a word the JobPlan never persists — so a finished ``remedy do`` run, whose
task ends as ``applied_to_job_workspace``, read DONE 0 and PROGRESS 0 while its row showed a
check mark. Every reader that turns a task status into done/planned/open now asks here.

Public API::

    TASK_LIFECYCLE_WORDS — the five words a status maps to
    task_lifecycle(status) -> str
"""

from __future__ import annotations

from packages.orchestration.run_manifest import VALID_TASK_STATUSES

TASK_LIFECYCLE_WORDS = frozenset({"done", "open", "planned", "blocked", "skipped"})

#: The JobPlan's own statuses (``VALID_TASK_STATUSES``), each to exactly one word.
#: DECISION amend1015 D2: ``split`` is ``skipped`` — a split task's work lives in its
#: children, so counting the parent as done or open would count that work twice.
_JOB_PLAN_LIFECYCLE = {
    "pending": "planned",
    "running": "open",
    "passed": "done",
    "applied_to_job_workspace": "done",
    "blocked": "blocked",
    "failed": "blocked",
    "vetoed": "blocked",
    "skipped": "skipped",
    "split": "skipped",
}

#: The older job model's words, still read by the cockpit for jobs written before JobPlan.
_LEGACY_LIFECYCLE = {
    "completed": "done",
    "planned": "planned",
    "active": "open",
}

assert set(_JOB_PLAN_LIFECYCLE) == set(VALID_TASK_STATUSES), "a JobPlan status has no lifecycle word"


# The one mapping from a persisted task status to the word the cockpit and the report count by.
def task_lifecycle(status: str) -> str:
    """``done``, ``open``, ``planned``, ``blocked`` or ``skipped`` for *status*; ValueError otherwise."""
    key = str(status or "").strip().lower()
    word = _JOB_PLAN_LIFECYCLE.get(key) or _LEGACY_LIFECYCLE.get(key)
    if word is None:
        raise ValueError(f"task status {status!r} has no lifecycle word")
    return word


# The dashboard's reading: a record with an unknown status is counted in no bucket, never raised.
def task_lifecycle_or_empty(status: str) -> str:
    """``task_lifecycle(status)``, or ``""`` when the status has no lifecycle word."""
    try:
        return task_lifecycle(status)
    except ValueError:
        return ""
