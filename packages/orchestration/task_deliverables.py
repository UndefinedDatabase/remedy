"""F268 T002 — tasks are bounded by DELIVERABLES, and one validator enforces it (DECISION F268 D6).

Three things live here, all pure (no I/O, no provider):

(a) `extract_order_deliverables` — the deterministic deliverable extractor: the
    file-path-like tokens of an order in order of first appearance, deduplicated;
    the order itself is the single deliverable when it names no path.
(b) `deterministic_job_plans` — the deterministic plan `remedy do` uses in place
    of `job_runner.plan_job`'s fixed three-task skeleton: one task per
    deliverable, its deliverable recorded in `inputs["deliverable"]`, ONE
    acceptance item each, so every `planning.granularity.*` ceiling holds. More
    deliverables than `_MAX_TASK_PLAN_TASKS` become several jobs' task lists,
    never a truncated one.
(c) `validate_deliverable_plan` — the one validator, run on every job `do`
    plans, deterministic or LLM: it rejects a task with no deliverable and a
    task whose title begins with an inspection verb. Reading is context (F107),
    never a task of its own (DECISION amend0911-feedback D3, R-0808).

A path-like token is a word holding a dot-extension that starts with a letter
(`CONTRIBUTING.md`, `src/app.py`, `.github/workflows/ci.yml`). Deliberately not
recognised: extension-less names such as `Makefile`, and one-letter stems such
as `e.g`; a bare domain such as `example.com` does read as a path. The extractor
is a deterministic floor, the LLM planner is the ceiling.
"""

from __future__ import annotations

import re

from packages.orchestration.pingpong_job import TaskEntry
from packages.orchestration.schemas.models import _MAX_TASK_PLAN_TASKS

#: A task whose title begins with one of these words is inspection, not a
#: deliverable, and the validator rejects it. Compared lower-cased, first word only.
INSPECTION_VERBS: tuple[str, ...] = (
    "analyze", "analyse", "inspect", "review", "read", "explore",
    "investigate", "examine", "study", "understand", "survey", "research",
)

#: The `inputs` key a task's deliverable is recorded under.
DELIVERABLE_INPUT_KEY = "deliverable"

_PATH_TOKEN_RE = re.compile(
    r"(?<![\w/.-])"
    r"((?:\.?[\w-]+/)*\.?[\w-]+(?:\.[\w-]+)*\.[A-Za-z][A-Za-z0-9]{0,7})"
    r"(?![\w/-])"
)


class DeliverablePlanError(ValueError):
    """A job plan holds a task without a deliverable, or an inspection task."""


def extract_order_deliverables(order: str) -> list[str]:
    """The order's path-like tokens in first-appearance order, deduplicated; else the order."""
    found: list[str] = []
    for match in _PATH_TOKEN_RE.finditer(order):
        token = match.group(1)
        # A one-letter stem outside a directory is an abbreviation (`e.g`, `i.e`).
        one_letter = "/" not in token and len(token.lstrip(".").split(".", 1)[0]) < 2
        if one_letter or token in found:
            continue
        found.append(token)
    return found or [order.strip()]


def deliverable_task(deliverable: str, order: str) -> TaskEntry:
    """One deterministic task producing one deliverable, with one acceptance item."""
    return TaskEntry(
        title=f"Deliver {deliverable}",
        body=f"{order}\n\nThis task's deliverable: {deliverable}",
        acceptance=f"{deliverable} is produced and meets the order: {order}",
        inputs={"task_type": "deliverable", DELIVERABLE_INPUT_KEY: deliverable},
    )


def deliverable_check_task(deliverable: str, order: str) -> TaskEntry:
    """One deterministic task whose deliverable is the named check that *deliverable* meets the order."""
    check = f"check: {deliverable} meets the order"
    return TaskEntry(
        title=f"Check that {deliverable} meets the order",
        body=f"{order}\n\nThis task's deliverable: {check}",
        acceptance=f"A check exists and passes showing {deliverable} meets the order: {order}",
        inputs={"task_type": "deliverable_check", DELIVERABLE_INPUT_KEY: check},
    )


def deterministic_job_plans(order: str) -> list[list[TaskEntry]]:
    """One task per deliverable, in order, split into job-sized lists; none dropped."""
    tasks = [deliverable_task(d, order) for d in extract_order_deliverables(order)]
    return [tasks[i:i + _MAX_TASK_PLAN_TASKS]
            for i in range(0, len(tasks), _MAX_TASK_PLAN_TASKS)]


def task_deliverable(task: TaskEntry) -> str:
    """The deliverable recorded on *task*, or "" when it has none."""
    return str(task.inputs.get(DELIVERABLE_INPUT_KEY) or "").strip()


def record_llm_task_deliverables(tasks: list[TaskEntry]) -> None:
    """Record an LLM task's deliverable: its first `files_hint`, else its first acceptance line.

    `job_plan.map_task_plan_to_tasks` keeps the planner's `files_hint` under
    `inputs["plan"]`; a task built from a job file keeps it on the task itself.
    A task with neither keeps no deliverable, and the validator rejects it.
    """
    for task in tasks:
        if task_deliverable(task):
            continue
        hints = list(task.files_hint) or list(
            (task.inputs.get("plan") or {}).get("files_hint") or [])
        lines = [line.strip() for line in task.acceptance.splitlines() if line.strip()]
        chosen = next((str(h).strip() for h in hints if str(h).strip()), "") or (
            lines[0] if lines else "")
        if chosen:
            task.inputs[DELIVERABLE_INPUT_KEY] = chosen


def _first_word(title: str) -> str:
    words = re.findall(r"[A-Za-z]+", title)
    return words[0].lower() if words else ""


def validate_deliverable_plan(tasks: list[TaskEntry]) -> None:
    """Raise `DeliverablePlanError` naming every task without a deliverable or that only inspects."""
    problems: list[str] = []
    if not tasks:
        problems.append("the plan holds no task")
    for task in tasks:
        if not task_deliverable(task):
            problems.append(f"task {task.task_id} ({task.title!r}) names no deliverable")
        verb = _first_word(task.title)
        if verb in INSPECTION_VERBS:
            problems.append(
                f"task {task.task_id} ({task.title!r}) is inspection ({verb!r}), "
                f"not a deliverable")
    if problems:
        raise DeliverablePlanError("; ".join(problems))
