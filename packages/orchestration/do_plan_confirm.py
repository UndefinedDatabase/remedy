"""Operator amendment amend1014-do-golden-path-now D3 — the plan boundary of a full `remedy do` plan.

A plan the bounded lane makes runs at once, in Remedy's isolated workspace, and stops before apply.
A generated plan of the full lane keeps an explicit approval boundary. On an interactive terminal
this module shows the plan concisely and asks one descriptive question; with no terminal, nothing
asks, and the walk stops with the command that approves it or the flag, `--run-unattended`, that
runs a generated plan without asking.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

#: Answers that approve; anything else, including end of input, declines.
_YES_ANSWERS = frozenset({"y", "yes"})


def plan_summary_lines(job: Any) -> list[str]:
    """The plan as the person reads it before answering: each task, its deliverable and the open questions."""
    from packages.orchestration.task_deliverables import task_deliverable

    lines = [f"[remedy] Plan for job {job.job_id}: {len(job.tasks)} task(s)"]
    for number, task in enumerate(job.tasks, start=1):
        lines.append(f"[remedy]   {number}. {task.title} — deliverable: {task_deliverable(task) or '(none)'}")
    plan = job.task_plan if isinstance(job.task_plan, dict) else {}
    for question in plan.get("clarifications_resolved") or []:
        if isinstance(question, dict) and not str(question.get("answer", "") or "").strip():
            lines.append(f"[remedy]   open question: {question.get('question', '')} "
                         f"(default: {question.get('default_answer', '')})")
    return lines


def make_plan_confirmer(
    *,
    ask: Callable[[str], str],
    write: Callable[[str], None] | None = None,
) -> Callable[[Any], bool]:
    """The confirmer an interactive terminal's walk carries: show the plan, ask, True only on `y`.

    *ask* reads one line (the CLI passes `input`; this package reads no terminal itself).
    """
    def say(text: str) -> None:
        sys.stderr.write(text + "\n")
        sys.stderr.flush()

    def confirm(job: Any) -> bool:
        out = write or say
        for line in plan_summary_lines(job):
            out(line)
        question = (f"[remedy] Run these {len(job.tasks)} task(s) now in Remedy's isolated workspace? "
                    f"Open questions take their documented defaults, and nothing is applied to "
                    f"your repository unless you pass --apply. [y/N] ")
        try:
            return ask(question).strip().lower() in _YES_ANSWERS
        except EOFError:
            return False

    return confirm


def approve_confirmed_plan(job: Any) -> None:
    """Record the person's approval of the plan they just confirmed, with every open question on its default."""
    from packages.orchestration.job_plan import resolve_task_plan_approval

    plan = job.task_plan if isinstance(job.task_plan, dict) else {}
    questions = list(plan.get("clarifications_resolved") or [])
    resolve_task_plan_approval(job, reason="approve", answers={}, questions=questions)
