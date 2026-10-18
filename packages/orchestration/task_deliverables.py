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
from typing import Any

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


#: The inputs a deterministic task records the order's other named files under (exec-1018, R-1348).
TASK_OPTIONAL_FILES_KEY = "optional_files"
TASK_CONTEXT_FILES_KEY = "context_files"
TASK_PROTECTED_FILES_KEY = "protected_files"
#: exec-1018b (R-1358): files the order names whose role its words did not make sure; never held to change.
TASK_MENTIONED_FILES_KEY = "mentioned_files"
#: exec-1018c (R-1363): when the order fences its files ("change no other files"), every file it names in
#: any role; a change to any other file is refused, in every round of the task, a repair round's too.
TASK_FENCE_FILES_KEY = "fence_files"


def deliverable_task(deliverable: str, order: str, *, with_tests: bool = False,
                     also: tuple[str, ...] = (), tests: tuple[str, ...] | None = None,
                     optional: tuple[str, ...] = (), context: tuple[str, ...] = (),
                     protected: tuple[str, ...] = (), parts: int = 0,
                     mentioned: tuple[str, ...] = ()) -> TaskEntry:
    """One deterministic task producing one deliverable, with one acceptance item.

    *with_tests*: the order itself asks for a test beside the deliverable (2026-10-17 audit P0-2).
    That test is a requested output of this same task, so its files are allowed and its existence
    is part of the one acceptance item; it is never a task of its own. *tests* names the test files
    of this task when the caller split them among several tasks (default: every test path the order
    names). *also* names the further files of the same one change (a small change over a few named
    files): they are declared as the task's `files_hint`, so every guard of a declared target reads
    them, and the task says it changes all of them in one step.

    exec-1018: *optional*, *context* and *protected* are the order's other named files (it allows
    them, only refers to them, or forbids changing them, `order_intent.order_file_roles`); the task
    says so and records them, and `deliverable_files_refusal` holds a protected one unchanged.
    *parts* > 1 says this task is one of that many independent parts of the order, each its own task.
    exec-1018b: *mentioned* are named files whose role the order's words did not make sure
    (`order_intent.FILE_ROLE_MENTIONED`): the task names them for the builder, never holds them to change.
    """
    files = [deliverable, *(path for path in also if path != deliverable)]
    named_files = " and ".join(files) if len(files) <= 2 else ", ".join(files[:-1]) + f" and {files[-1]}"
    verb = "is produced and meets" if len(files) == 1 else "are produced and meet"
    accept = f"{named_files} {verb} the order: {order}"
    body = f"{order}\n\nThis task's deliverable: {deliverable}"
    title = f"Deliver {named_files}"
    inputs = {"task_type": "deliverable", DELIVERABLE_INPUT_KEY: deliverable}
    if len(files) > 1:
        body += (f"\nThis one change spans {len(files)} files, all in this step: {named_files}. "
                 "Change each of them as the order asks before you finish.")
    if parts > 1:
        body += (f"\nThe order has {parts} independent parts, each its own task: this task does only "
                 f"the part about {named_files}; leave the other parts to their own tasks.")
    for key, named, words in ((TASK_OPTIONAL_FILES_KEY, optional, "you may change, if the change needs it"),
                              (TASK_CONTEXT_FILES_KEY, context, "are named for reference: read them if useful, "
                               "do not change them"),
                              (TASK_PROTECTED_FILES_KEY, protected, "must stay unchanged, as the order says"),
                              (TASK_MENTIONED_FILES_KEY, mentioned, "are named in the order too: change them only as "
                               "far as the order asks, and leave them as they are where it does not")):
        if named:
            inputs[key] = list(named)
            body += f"\nThese files {words}: {', '.join(named)}."
    from packages.orchestration.do_scope import order_has_scope_fence

    if order_has_scope_fence(order):
        # Every file the order names counts, whatever role its words were read in: a misread role
        # (R-1358) must never turn a requested change into a refused one. Protected files stay refused.
        inputs[TASK_FENCE_FILES_KEY] = sorted({*files, *explicit_order_paths(order), *(tests or ()),
                                               *optional, *context, *mentioned})
    if with_tests:
        # Lab calc order of 2026-10-17: "deliverable: src/calc.js" with a side sentence about a test
        # made the builder fix only calc.js; the reviewer failed it and the repair round ran the job
        # out of budget. The test file is named as a deliverable of this same task.
        from packages.orchestration.order_scope import is_test_path

        named = list(tests) if tests is not None else [p for p in explicit_order_paths(order) if is_test_path(p)]
        test = " and ".join(named) if named else "a test file in the project's existing test folder"
        title = f"Deliver {named_files} and its test" + (f" {test}" if named else "")
        body += (f"\nThis task delivers TWO things in this one step: the change to {named_files} AND "
                 f"the test the order asks for, {test} (it may be a new file; follow the existing "
                 "tests' location and style). Do not finish until both are written.")
        accept += "; the test the order asks for exists and passes" + (f" ({test})" if named else "")
        inputs["with_tests"] = True
    return TaskEntry(title=title, body=body, acceptance=accept, inputs=inputs,
                     files_hint=files if len(files) > 1 else [])


def deterministic_job_plans(order: str) -> list[list[TaskEntry]]:
    """One task per deliverable, in order, split into job-sized lists; none dropped."""
    tasks = [deliverable_task(d, order) for d in extract_order_deliverables(order)]
    return [tasks[i:i + _MAX_TASK_PLAN_TASKS]
            for i in range(0, len(tasks), _MAX_TASK_PLAN_TASKS)]


def task_deliverable(task: TaskEntry) -> str:
    """The deliverable recorded on *task*, or "" when it has none."""
    return str(task.inputs.get(DELIVERABLE_INPUT_KEY) or "").strip()


def deliverable_files_refusal(job: Any, result: Any, changed: list[str]) -> str:
    """Why the task *result* ran may not pass by the files it changed, or "" when it may.

    Only a deterministic deliverable task is read (`deliverable_task`); a planner's task never is,
    because its `files_hint` are hints, some only to be read. Two refusals, the first that applies:

    * `named_files_unchanged`: the task's one change spans several named files (its `files_hint`)
      and the run left one of them unchanged; a reviewer's pass over it is no completion (R-1342);
    * `protected_file_changed`: the run changed a file the order says must stay unchanged (R-1348);
    * `unrequested_file_changed`: the order fences its files and the run changed one it does not name
      (R-1363); a test file counts as named when the task delivers a test the order did not name, and a
      tool cache a test run leaves is no change.

    A file the order names only as context or merely allows is held to nothing else.
    """
    task = next((t for t in job.tasks if str(t.task_id) == str(getattr(result, "task_id", ""))), None)
    if task is None or task.inputs.get("task_type") != "deliverable":
        return ""
    missing = [path for path in task.files_hint if path not in set(changed)]
    if missing:
        return (f"named_files_unchanged: the change left {', '.join(missing)} unchanged, which the order "
                f"names as part of it")
    touched = [path for path in task.inputs.get(TASK_PROTECTED_FILES_KEY) or [] if path in set(changed)]
    if touched:
        return (f"protected_file_changed: the change touched {', '.join(touched)}, which the order says must "
                f"stay unchanged")
    fence = task.inputs.get(TASK_FENCE_FILES_KEY)
    outside = [path for path in changed if fence is not None and not _fence_allows(task, fence, path)]
    return (f"unrequested_file_changed: the change touched {', '.join(outside)}, which the order does not "
            f"name and says no other file may change" if outside else "")


def _fence_allows(task: TaskEntry, fence: list[str], path: str) -> bool:
    """Whether a fenced *task* may change *path*: a named file (a bare name matches it in any folder), a
    test file when the task delivers a test the order did not name, or a test run's tool cache."""
    from packages.orchestration.order_scope import is_test_path
    from packages.orchestration.pingpong_loop import _is_target_noise

    name = path.rsplit("/", 1)[-1]
    if path in fence or any("/" not in named and named == name for named in fence):
        return True
    if task.inputs.get("with_tests") and is_test_path(path) and not any(is_test_path(f) for f in fence):
        return True
    return any(_is_target_noise(part) for part in path.split("/"))


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


def validate_deliverable_plan(tasks: list[TaskEntry], *, allow_empty: bool = False) -> None:
    """Raise `DeliverablePlanError` naming every task without a deliverable or that only inspects.

    An empty plan is refused unless *allow_empty*: a job the shape step plans with no build task by
    design, a verification-only order's, whose DoD runs the project's tests (exec-1018, R-1349).
    """
    problems: list[str] = []
    if not tasks and not allow_empty:
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
