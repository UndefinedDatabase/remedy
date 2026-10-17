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
(`CONTRIBUTING.md`, `src/app.py`, `.github/workflows/ci.yml`), or one of the
extension-less file names `EXTENSIONLESS_DELIVERABLE_NAMES` lists (`Makefile`,
`docker/Dockerfile`). No token inside a URL — `https://…` or `www.…` — is a
deliverable (R-0966). Deliberately not recognised: one-letter stems such as
`e.g`; a bare domain such as `example.com` outside a URL does read as a path.
The extractor is a deterministic floor, the LLM planner is the ceiling.
"""

from __future__ import annotations

import re

from pydantic import ValidationError

from packages.orchestration.pingpong_job import TaskEntry
from packages.orchestration.schemas.models import _MAX_TASK_PLAN_TASKS, PlannedTask, TaskPlan

#: A task whose title begins with one of these words is inspection, not a
#: deliverable, and the validator rejects it. Compared lower-cased, first word only.
INSPECTION_VERBS: tuple[str, ...] = (
    "analyze", "analyse", "inspect", "review", "read", "explore",
    "investigate", "examine", "study", "understand", "survey", "research",
    "verify", "confirm", "locate", "find", "identify", "assess", "audit",
    # German planners (lab order of 2026-10-17: "Prüfe Änderungsumfang und Abhängigkeiten").
    "prüfe", "überprüfe", "verifiziere", "kontrolliere", "bestätige", "analysiere",
    "untersuche", "inspiziere", "lies", "finde", "identifiziere", "ermittle",
)

#: The `inputs` key a task's deliverable is recorded under.
DELIVERABLE_INPUT_KEY = "deliverable"

_PATH_TOKEN_RE = re.compile(
    r"(?<![\w/.-])"
    r"((?:\.?[\w-]+/)*\.?[\w-]+(?:\.[\w-]+)*\.[A-Za-z][A-Za-z0-9]{0,7})"
    r"(?![\w/-])"
)

#: Common file names without a dot-extension that an order names as a deliverable
#: (R-0966). Matched case-sensitively, optionally under a directory.
EXTENSIONLESS_DELIVERABLE_NAMES: tuple[str, ...] = (
    "Makefile", "GNUmakefile", "Dockerfile", "Containerfile", "Jenkinsfile",
    "Procfile", "Gemfile", "Rakefile", "Vagrantfile", "Brewfile", "Justfile",
    "LICENSE", "CODEOWNERS",
)

_EXTENSIONLESS_TOKEN_RE = re.compile(
    r"(?<![\w/.-])"
    r"((?:\.?[\w-]+/)*(?:" + "|".join(map(re.escape, EXTENSIONLESS_DELIVERABLE_NAMES)) + r"))"
    r"(?![\w/-]|\.\w)"
)

#: A URL, with a scheme or starting `www.`, up to the next whitespace; a token inside one is no path.
_URL_RE = re.compile(r"(?<![\w.-])(?:[A-Za-z][A-Za-z0-9+.-]*://|www\.)\S+")


class DeliverablePlanError(ValueError):
    """A job plan holds a task without a deliverable, or an inspection task."""


def extract_order_deliverables(order: str) -> list[str]:
    """The order's path-like tokens in first-appearance order, deduplicated; else the order."""
    urls = [m.span() for m in _URL_RE.finditer(order)]
    matches = sorted(
        (m.start(1), m.group(1))
        for regex in (_PATH_TOKEN_RE, _EXTENSIONLESS_TOKEN_RE)
        for m in regex.finditer(order)
    )
    found: list[str] = []
    for start, token in matches:
        if any(url_start <= start < url_end for url_start, url_end in urls):
            continue
        # A one-letter stem outside a directory is an abbreviation (`e.g`, `i.e`).
        one_letter = "/" not in token and len(token.lstrip(".").split(".", 1)[0]) < 2
        if one_letter or token in found:
            continue
        found.append(token)
    return found or [order.strip()]


def deliverable_task(deliverable: str, order: str, *, with_tests: bool = False) -> TaskEntry:
    """One deterministic task producing one deliverable, with one acceptance item.

    *with_tests*: the order itself asks for a test beside the deliverable (2026-10-17 audit P0-2).
    That test is a requested output of this same task, so its files are allowed and its existence
    is part of the one acceptance item; it is never a task of its own.
    """
    accept = f"{deliverable} is produced and meets the order: {order}"
    body = f"{order}\n\nThis task's deliverable: {deliverable}"
    inputs = {"task_type": "deliverable", DELIVERABLE_INPUT_KEY: deliverable}
    if with_tests:
        body += ("\nThe order asks for a test: write it in the project's existing test location and "
                 "style, and it may be a new test file.")
        accept += "; the test the order asks for exists and passes"
        inputs["with_tests"] = True
    return TaskEntry(title=f"Deliver {deliverable}", body=body, acceptance=accept, inputs=inputs)


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
    # Letters of any script: `[A-Za-z]` read "Prüfe" as "pr" (lab order of 2026-10-17).
    words = re.findall(r"[^\W\d_]+", title)
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


def _is_inspection(task: PlannedTask) -> bool:
    return _first_word(task.title) in INSPECTION_VERBS


def _fold_into(target: PlannedTask, inspection: PlannedTask, *, last: bool = False) -> PlannedTask:
    """*target* with *inspection*'s work as its first (or, *last*, its final) step and its dependencies as its own."""
    depends = [d for d in [*target.depends_on, *inspection.depends_on]
               if d not in (inspection.id, target.id)]
    hints = [*target.files_hint, *(h for h in inspection.files_hint if h not in target.files_hint)]
    when = "Last" if last else "First"
    return target.model_copy(update={
        "goal": f"{target.goal}\n{when}, as part of this task: {inspection.title}: {inspection.goal}",
        "depends_on": list(dict.fromkeys(depends)),
        "files_hint": hints,
    })


def explicit_order_paths(text: str) -> list[str]:
    """The path-like tokens *text* names, and [] when it names none (no fallback to the text itself)."""
    found = extract_order_deliverables(text)
    return [] if found == [text.strip()] else found


def _plan_deliverable(task: PlannedTask) -> str:
    """The concrete file a planned task serves: its first `files_hint`, else the one file its text names.

    "" when it names none or several, so such a task is never merged.
    """
    hint = next((str(h).strip() for h in task.files_hint if str(h).strip()), "")
    if hint:
        return hint
    named = explicit_order_paths(" ".join([task.title, task.goal, *task.acceptance]))
    return named[0] if len(named) == 1 else ""


def _merge_same_deliverable(group: list[PlannedTask], deliverable: str) -> PlannedTask:
    """One task for *group*, which all serve *deliverable*: the last task's title, every step in order."""
    last = group[-1]
    members = {t.id for t in group}
    depends = [d for t in group for d in t.depends_on if d not in members]
    steps = "\n".join(f"Step {n}, {t.title}: {t.goal}" for n, t in enumerate(group, start=1))
    return last.model_copy(update={
        "goal": f"{last.goal}\nThis one task does all of these, in order:\n{steps}",
        "acceptance": list(dict.fromkeys(a for t in group for a in t.acceptance)),
        "depends_on": list(dict.fromkeys(depends)),
        "files_hint": list(dict.fromkeys([deliverable, *(h for t in group for h in t.files_hint)])),
    })


def coalesce_deliverable_tasks(plan: TaskPlan) -> TaskPlan | None:
    """The plan with every set of tasks serving ONE concrete file merged into a single task (amend1014 D2).

    Tasks are keyed by their first `files_hint` and nothing else; a task naming no file is never
    merged, and short titles alone merge nothing. The merged task takes the title of the LAST
    task of its set, the final mutating action, with the others' work as its numbered steps; the
    tasks that waited for any of them wait for it. A set whose merge would put a task outside the
    set between two of its members (a dependency cycle) is left as planned. Returns None when
    nothing merged or when the merged plan is no valid `TaskPlan`.
    """
    tasks = list(plan.tasks)
    by_file: dict[str, list[PlannedTask]] = {}
    for task in tasks:
        if (key := _plan_deliverable(task)):
            by_file.setdefault(key, []).append(task)
    merged_any = False
    for key, group in ((k, g) for k, g in by_file.items() if len(g) > 1):
        ids = {t.id for t in group}
        merged = _merge_same_deliverable(group, key)
        rewired = [
            merged if t.id == merged.id else
            t.model_copy(update={"depends_on": list(dict.fromkeys(
                merged.id if d in ids else d for d in t.depends_on))})
            for t in tasks if t.id == merged.id or t.id not in ids]
        try:
            candidate = TaskPlan.model_validate(
                {**plan.model_dump(), "tasks": [t.model_dump() for t in rewired]})
        except ValidationError:
            continue
        tasks, plan, merged_any = rewired, candidate, True
    return plan if merged_any else None


def fold_inspection_tasks(plan: TaskPlan) -> TaskPlan | None:
    """The plan with each inspection task folded into the next task that depends on it (amend1011 D1).

    The inspection task is dropped; its title and goal become the first step of
    the task that waits for it (or, when none does, of the next task in plan
    order; when it is the last task, the final step of the work task before it),
    and whatever waited for it waits for that task. Acceptance of an
    inspection task is dropped with it: reading is context, never a deliverable.
    Returns None when the plan holds no inspection task, when one has no work task
    to fold into, or when the folded plan is no valid `TaskPlan`.
    """
    tasks = list(plan.tasks)
    if not any(_is_inspection(t) for t in tasks):
        return None
    while True:
        index = next((i for i, t in enumerate(tasks) if _is_inspection(t)), None)
        if index is None:
            break
        inspection, later = tasks[index], tasks[index + 1:]
        target = next((t for t in later if inspection.id in t.depends_on),
                      later[0] if later else None)
        if target is None:
            # A check AFTER the work ("Verify only README.md changed", lab orders of 2026-10-17) is
            # the last step of the work task before it, never a task of its own.
            target = next((t for t in reversed(tasks[:index]) if not _is_inspection(t)), None)
            if target is None:
                return None
            folded = _fold_into(target, inspection, last=True)
        else:
            folded = _fold_into(target, inspection)
        tasks = [
            folded if t.id == target.id else
            t.model_copy(update={"depends_on": list(dict.fromkeys(
                target.id if d == inspection.id else d for d in t.depends_on))})
            for t in tasks if t.id != inspection.id]
    try:
        return TaskPlan.model_validate({**plan.model_dump(), "tasks": [t.model_dump() for t in tasks]})
    except ValidationError:
        return None
