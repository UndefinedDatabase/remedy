"""A job task whose work an earlier task of its job already did ends done, not blocked (F332).

Operator order beweis, job 6c4564622e87457e: task 2 changed `NetHeader.tsx` and its call site
`KnowledgeNet.tsx`, so task 3 („Update KnowledgeNet ...") had nothing left to do. Its builder staged
no change, the empty diff turned the review into needs_repair (R-0999, amend1014b D3), and
`no_file_changed` (R-1117) blocked the whole job; task 4 („Run the test command ...") was skipped.

A job task that stages no change now ends done when two things hold:

* an earlier task of the same job already changed the files the task names (`earlier_work`): its
  deliverable file when it names one, else every file its hints, title, goal or acceptance name;
  a task that only runs the tests (`is_test_run_task`) names no file and checks the files every
  earlier task changed;
* the reviewer, asked by `no_change_diff_summary` whether the task's acceptance already holds in the
  job's workspace, passes it with no finding above `low`.

The decision is made here in code from that verdict (`empty_diff_gate`, `settle_already_done`), and
the task keeps the plain record `inputs["already_done"]`: the earlier task's number and id, the files,
and one evidence line; the story names it with the phrase `already_done`. Every other no-change
task fails exactly as before.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: The task's `inputs` key of the record, and the story's phrase word for such a task.
ALREADY_DONE_KEY = "already_done"

#: The first words of a task that only runs the tests („Run the test command and confirm it exits
#: green"): such a task changes no file by design, and its title also says `test`.
TEST_RUN_VERBS: tuple[str, ...] = ("run", "rerun", "execute", "führe", "starte")

#: The reviewer's diff line for a builder that changed no file; the line before F332, kept word for word.
NO_CHANGE_LINE = "(no changes — the builder changed no file)"


@dataclass(frozen=True)
class EarlierWork:
    """Which earlier task of the job did this task's work, and on which files.

    WHY: one value carries the answer from the job's record to the reviewer's prompt, the empty-diff
    gate and the task's record, so all three read the same earlier task and the same files.
    """
    task_number: int                       # 1-based place in the job of the latest such task
    task_id: str
    files: tuple[tuple[str, int], ...]     # (file, the 1-based number of the task that changed it)
    test_run: bool                         # the task only runs the tests over the earlier work

    def file_names(self) -> list[str]:
        return [path for path, _ in self.files]

    def evidence(self) -> str:
        """The plain evidence line: the earlier task and the files."""
        named = ", ".join(f"{path} (task {number})" for path, number in self.files)
        verb = "checked the work of" if self.test_run else "already done by"
        return f"{verb} task {self.task_number} ({self.task_id}): {named}"


def task_named_files(task: Any) -> list[str]:
    """The files TASK names: its hints, its planner's hints, its deliverable and the paths its words name."""
    from packages.orchestration.task_deliverables import DELIVERABLE_INPUT_KEY, explicit_order_paths

    inputs = getattr(task, "inputs", None) or {}
    plan = inputs.get("plan") or {}
    hints = [*(getattr(task, "files_hint", None) or ()), *(plan.get("files_hint") or ())]
    words = [str(inputs.get(DELIVERABLE_INPUT_KEY) or ""), str(getattr(task, "title", "") or ""),
             str(getattr(task, "body", "") or ""), str(getattr(task, "acceptance", "") or "")]
    text = "\n".join(str(h) for h in [*hints, *words] if str(h).strip())
    return explicit_order_paths(text) if text.strip() else []


def is_test_run_task(task: Any) -> bool:
    """True for a task that only runs the tests: its title begins with a run verb and says `test`."""
    title = str(getattr(task, "title", "") or "").strip().lower()
    words = title.split()
    return bool(words) and words[0] in TEST_RUN_VERBS and "test" in title


def _changed_by_earlier_tasks(job: Any, index: int) -> dict[str, int]:
    """Every file the job's tasks before INDEX applied, mapped to the 1-based number of the last one."""
    from packages.orchestration.pingpong_job import TASK_APPLIED

    changed: dict[str, int] = {}
    for number, earlier in enumerate(job.tasks[:index], start=1):
        if earlier.status != TASK_APPLIED:
            continue
        manifest = earlier.apply_manifest
        for path in (list(manifest.applied_files) if manifest else []) or list(earlier.safe_diff_files):
            changed[str(path)] = number
    return changed


def earlier_work(job: Any, task: Any) -> EarlierWork | None:
    """The earlier task of JOB that already did TASK's work, or None when none did (F332)."""
    index = next((i for i, t in enumerate(job.tasks) if str(t.task_id) == str(task.task_id)), None)
    if not index:
        return None
    changed = _changed_by_earlier_tasks(job, index)
    named = task_named_files(task)
    if named:
        from packages.orchestration.task_deliverables import DELIVERABLE_INPUT_KEY, explicit_order_paths

        deliverable = explicit_order_paths(str(task.inputs.get(DELIVERABLE_INPUT_KEY) or ""))
        needed = deliverable[:1] or named
        if any(path not in changed for path in needed):
            return None
        files = [(path, changed[path]) for path in named if path in changed]
        test_run = False
    elif is_test_run_task(task) and changed:
        files, test_run = sorted(changed.items()), True
    else:
        return None
    latest = max(number for _, number in files)
    return EarlierWork(task_number=latest, task_id=str(job.tasks[latest - 1].task_id),
                       files=tuple(files), test_run=test_run)


def earlier_work_of(job_id: str, task_id: str) -> EarlierWork | None:
    """`earlier_work` read from the job's saved record; None outside a job or when it cannot be read."""
    if not job_id or not task_id:
        return None
    from packages.orchestration.pingpong_job import load_job_plan

    try:
        job = load_job_plan(job_id)
    except Exception:  # noqa: BLE001 — an unreadable record leaves the no-change task to the old defenses
        return None
    task = next((t for t in job.tasks if str(t.task_id) == str(task_id)), None) if job else None
    return earlier_work(job, task) if task is not None else None


def no_change_diff_summary(job_id: str, task_id: str) -> str:
    """The reviewer's diff line for a builder that changed no file, with the F332 question when it applies."""
    work = earlier_work_of(job_id, task_id)
    if work is None:
        return NO_CHANGE_LINE
    named = ", ".join(f"{path} (task {number})" for path, number in work.files)
    about = ("This task only runs the tests over them." if work.test_run
             else "These are the files this task names.")
    return (f"{NO_CHANGE_LINE}\nThe job's earlier tasks changed these files: {named}. {about} "
            "Judge whether this task's acceptance already holds in the workspace: answer pass with no "
            "finding when it holds, and needs_repair naming what is missing when it does not.")


def settle_already_done(job: Any, task: Any, result: Any, gate: tuple[bool, list[str]]) -> tuple[bool, list[str]]:
    """GATE (`validate_job_task_result`'s answer) with `no_file_changed` lifted for a task already done.

    Only when `no_file_changed` is the gate's one reason, so the review passed with no finding above
    `low`, no test failed and nothing else is wrong; then TASK keeps the record under
    `ALREADY_DONE_KEY` and the gate passes. Every other answer is returned unchanged.
    """
    ok, reasons = gate
    if ok or reasons != ["no_file_changed"] or getattr(result, "staged_files", None):
        return gate
    work = earlier_work(job, task)
    if work is None:
        return gate
    task.inputs[ALREADY_DONE_KEY] = {"task": work.task_number, "task_id": work.task_id,
                                     "files": work.file_names(), "evidence": work.evidence()}
    return True, []


def already_done_record(task: Any) -> dict[str, Any] | None:
    """The task's F332 record, or None when it carries none."""
    record = (getattr(task, "inputs", None) or {}).get(ALREADY_DONE_KEY)
    return record if isinstance(record, dict) else None
