"""A run report's readers of one task record's own fields: origin, attempt, model override.

Moved out of `packages/orchestration/run_report.py` unchanged but for their public names, as a
structure step that keeps that file under its line pin (amend1015); `collect_report_sources`
is their one caller.

Public API::

    report_task_origin(t) -> str
    report_task_attempt(t) -> int
    report_task_model_override(t) -> str
"""

from __future__ import annotations

from typing import Any


def report_task_origin(t: Any) -> str:
    """DECISION F028 D8: a task's provenance, read off its own plan inputs —
    `inputs["plan"]["origin"]` when `inputs["plan"]` is a dict and that value
    is a non-empty string, else "" (P6: not recorded, never guessed).  Mirrors
    `serve_http_handler._task_origin` (DECISION F028 D6 (1)); the report reads the
    job's own tasks directly rather than importing the UI server, so the
    report and the server agree by reading the same shape independently
    rather than by sharing an import.
    """
    inputs = getattr(t, "inputs", None)
    plan = inputs.get("plan") if isinstance(inputs, dict) else None
    if not isinstance(plan, dict):
        return ""
    origin = plan.get("origin")
    return origin if isinstance(origin, str) and origin else ""


def report_task_attempt(t: Any) -> int:
    """DECISION F029 D6: a task's attempt number, off its own record's
    `attempt` (DECISION F029 D2, `subtree_rerun.py`'s `TaskEntry.attempt`) —
    an int, or 1 (the record's own default for a task that has never been
    rerun) for anything else.  Read defensively, as `report_task_origin` reads
    `origin`: a malformed or absent value never raises into a render.
    """
    value = getattr(t, "attempt", 1)
    return value if isinstance(value, int) and not isinstance(value, bool) else 1


def report_task_model_override(t: Any) -> str:
    """DECISION F029 D6: the model a rerun task ran under, off its own
    record's `model_override` (DECISION F029 D2, `TaskEntry.model_override`)
    — a non-empty string, or "" (P6: not recorded) for anything else.  Read
    defensively, as `report_task_origin` reads `origin`.
    """
    value = getattr(t, "model_override", "")
    return value if isinstance(value, str) and value else ""
