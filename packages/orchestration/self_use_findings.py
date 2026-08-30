"""F258 T003 — surfacing a self-use run's own defects, verbatim, for the ledger.

:mod:`packages.orchestration.self_use_runner` runs a planned self-use item to
the normal approval gate and answers whatever ``JobPlan`` `run_job` produces
— ``JOB_COMPLETED`` or ``JOB_BLOCKED``, with every task's own outcome
recorded on it. This module is the one step further T003 asks for: reading
that ``JobPlan`` back and naming, in the job's OWN words, what (if anything)
went wrong — so the closing session can register each one as a normal
finding in ``.agent/live_review.md`` under the standard rules, per
``docs/roadmap/features/T5_F258.md`` T003.

Public API::

    describe_self_use_run_defects(result) -> tuple[str, ...]

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT REGISTER A FINDING HERE. This module only
    READS a ``JobPlan`` and answers plain strings; writing an ``- R-XXXX``
    line into ``.agent/live_review.md`` stays the closing session's own act,
    exactly as `docs/agents/planner_reviewer_prompt.md` §3 item 30 already
    requires searching the open set before minting one — a step only a
    reviewer performs, never automated.
  * Remedy deliberately does not SUMMARIZE, TRUNCATE OR REWORD a defect. Each
    returned string quotes the ``JobPlan``'s or a ``TaskEntry``'s own
    ``error`` field verbatim, the same "never invent" discipline
    :mod:`packages.orchestration.self_use_generator` already holds a ledger
    finding's paragraph to.
  * Remedy deliberately does not judge SEVERITY here. A registering session
    picks the severity the normal finding-ledger rules already use; this
    module answers only WHETHER something went wrong and WHAT the job itself
    said about it.
"""

from __future__ import annotations

from packages.orchestration.pingpong_job import JobPlan


def describe_self_use_run_defects(result: JobPlan) -> tuple[str, ...]:
    """Plain-text defects ``result`` surfaced, quoting its own fields verbatim.

    Answers one string for the job itself when ``result.error`` is non-blank
    (``"job {job_id} ({status}): {error}"``), then one string per task whose
    own ``error`` is non-blank (``"{task_id} ({status}): {error}"``), in task
    order. An empty tuple means the run surfaced nothing to register — not
    that nothing was checked; a job that completed with every task's `error`
    blank answers ``()``.
    """
    defects: list[str] = []
    if result.error:
        defects.append(f"job {result.job_id} ({result.status}): {result.error}")
    for task in result.tasks:
        if task.error:
            defects.append(f"{task.task_id} ({task.status}): {task.error}")
    return tuple(defects)
