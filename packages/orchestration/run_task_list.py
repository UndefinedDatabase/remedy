"""F308 — what a run manifest says about the task list a job ran: the ids the episode's embedded
definition declares, their agreement across a job's episodes, what a task that owns no run is
expected to have done, the split of a task whose context exceeds its class cap, and the record
that split leaves (DECISION F308 D2). It imports neither `run_manifest` nor `pingpong_job` at its
top, so that `run_manifest.py` can import it at its own top without a cycle; each function below
imports what it needs from those two modules inside its own body. `manifest_schema` is imported
at the top, exactly as `run_manifest.py` imports it.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from packages.orchestration import manifest_schema as _S

if TYPE_CHECKING:
    from packages.orchestration.context_compiler import ClassBudgetFit
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    from packages.orchestration.run_manifest import RunManifestV1

# F308, DECISION F308 D2 (1): THE RECORD — the key a split is filed under in `job.metadata`.
TASK_SPLITS_METADATA_KEY = "task_splits"
# F308, DECISION F308 D2 (1): THE RECORD — one split is a map of exactly these four keys.
TASK_SPLIT_FIELDS = ("parent_task_id", "part_task_ids", "episode_id", "reason")


# F308, step (2) of `_collect_calls`'s boundary: the task without a run gets its own function.
def expect_task_without_run(
    task_id: str, status: str, must_have_calls: bool, problems: list[str], expectations: list,
) -> None:
    """Record what a task that owns no run is expected to have done, by F6's three cases."""
    from packages.orchestration.pingpong_job import (
        TASK_BLOCKED,
        TASK_FAILED,
        TASK_SKIPPED,
        TASK_SPLIT,
        TASK_VETOED,
    )
    from packages.orchestration.run_manifest import (
        DISPATCH_NEVER,
        DISPATCH_THIS_EPISODE,
        EXPECT_EXECUTED,
        EXPECT_FAILED_PRE_DISPATCH,
        EXPECT_NOT_DISPATCHED,
        EXPECT_SKIPPED,
        TaskCallExpectationV1,
    )
    # F6: a task whose status says it ran, but which carries no run to point at, is
    # MISSING evidence — not a zero-call task. Publishing it as "complete" would be the
    # manifest certifying its own blind spot.
    if must_have_calls:
        problems.append(
            f"task {task_id} is {status!r} but has no run id, so its calls cannot be "
            f"accounted for")
        expectations.append(TaskCallExpectationV1(
            task_id=task_id, expectation=EXPECT_EXECUTED, run_id="",
            expected_call_count=1, task_status_at_finalization=status,
            dispatch_state=DISPATCH_THIS_EPISODE))
    elif status in (TASK_FAILED, TASK_BLOCKED):
        # F4 (round 12): failed/blocked with NO run is its own truth — the task never
        # reached dispatch. Calling it "not dispatched" would lose the failure; calling
        # it "dispatched_no_calls" would invent a run that never existed.
        expectations.append(TaskCallExpectationV1(
            task_id=task_id, expectation=EXPECT_FAILED_PRE_DISPATCH, run_id="",
            task_status_at_finalization=status, dispatch_state=DISPATCH_NEVER))
    else:
        # F027 D2 (6): a vetoed task with no run is EXPECT_SKIPPED exactly as a
        # skipped one is — the veto struck before dispatch, same as a skip. F308: so is a
        # split parent — it owns no run of its own and the resume loop never dispatches it.
        expectations.append(TaskCallExpectationV1(
            task_id=task_id,
            expectation=(EXPECT_SKIPPED if status in (TASK_SKIPPED, TASK_VETOED, TASK_SPLIT)
                         else EXPECT_NOT_DISPATCHED),
            run_id="", task_status_at_finalization=status,
            dispatch_state=DISPATCH_NEVER))


# F308, DECISION F308 D2 (1): the split a run makes gets its own record in the job's history.
def record_task_split(
    job: JobPlan, parent_task_id: str, part_task_ids: list[str], reason: str,
) -> dict:
    """Append one split's record to `job.metadata[TASK_SPLITS_METADATA_KEY]` and answer it."""
    entry = {
        "parent_task_id": str(parent_task_id),
        "part_task_ids": [str(p) for p in part_task_ids],
        "episode_id": str(getattr(job, "active_episode_id", "") or ""),
        "reason": str(reason or "")[:_S.MAX_SHORT_TEXT],
    }
    job.metadata.setdefault(TASK_SPLITS_METADATA_KEY, []).append(entry)
    return entry


# F308, outside `run_job`'s named steps: the split of a task over its class cap gets its own
# function.
def split_task_over_class_cap(
    job: JobPlan, task: TaskEntry, idx: int, fit_result: ClassBudgetFit,
) -> bool:
    """Answer True when it replaced the task with its parts."""
    from packages.orchestration.escalation import (
        auto_apply_safe_default,
        enqueue_task_decision,
    )
    from packages.orchestration.pingpong_job import (
        TASK_SPLIT,
        planned_task_to_task_entry,
        save_job_plan,
        task_entry_to_planned_task,
    )
    from packages.orchestration.task_granularity import (
        split_one_task,
    )
    decision = enqueue_task_decision(
        job,
        task_id=task.task_id,
        question="task context exceeds its class cap",
        options=["split task"],
        safe_default="split task",
        impact=(
            f"tier1_tokens={fit_result.tier1_tokens} "
            f"cap_tokens={fit_result.cap_tokens} "
            f"task_class={fit_result.task_class}"
        ),
        now=datetime.now(timezone.utc),
    )
    answered = auto_apply_safe_default(
        job, decision, now=datetime.now(timezone.utc))
    split_entries: list[TaskEntry] = []
    if answered is not None and answered["answer"] == "split task":
        planned = task_entry_to_planned_task(task)
        if planned is not None:
            used_ids = {t.task_id for t in job.tasks}
            children = split_one_task(planned, used_ids=used_ids)
            if children:
                split_entries = [
                    planned_task_to_task_entry(
                        child,
                        task_class=task.task_class,
                        source_heading_number=task.source_heading_number,
                    )
                    for child in children
                ]
    if split_entries:
        job.tasks[idx + 1:idx + 1] = split_entries
        task.status = TASK_SPLIT
        record_task_split(
            job, task.task_id, [e.task_id for e in split_entries],
            f"{decision['question']}: {decision['impact']}")
        save_job_plan(job)
        return True
    return False


# F308: the ids a run manifest's embedded job-input definition declares, read in one place.
def job_input_task_ids(manifest: RunManifestV1) -> list[str]:
    """The task ids the EMBEDDED, immutable JobInputDefinition declares."""
    out: list[str] = []
    ji = getattr(getattr(manifest.episode_snapshot, "input", None), "job_input", None)
    if isinstance(ji, dict) and isinstance(ji.get("tasks"), list):
        for t in ji["tasks"]:
            if isinstance(t, dict):
                out.append(str(t.get("task_id", "")))
    return out


# F308, DECISION F308 D2 (3): THE LIST — the definition's ids with this manifest's own recorded
# splits applied, so every validator bound to it accepts the parts a split inserted.
def declared_job_input_task_ids(manifest: RunManifestV1) -> list[str]:
    """`job_input_task_ids(manifest)` with `manifest.task_splits` applied."""
    return task_ids_after_splits(
        job_input_task_ids(manifest), getattr(manifest, "task_splits", ()))[0]


# F308, DECISION F308 D2 (3): the split arithmetic, read in one place by the F7 check and by
# `task_split_problems`.
def task_ids_after_splits(ids: list[str], splits: Any) -> tuple[list[str], list[str]]:
    """`ids` with each split's parts inserted directly after its parent, in the splits' order.

    Answers (the list after the splits, the problems). A split with a problem is not applied —
    a parent not in `ids` exactly once, a parent already split, parts that are empty, repeated,
    or already present in the list, or a record that is not a map of exactly `TASK_SPLIT_FIELDS`.
    """
    out = list(ids)
    problems: list[str] = []
    split_parents: set[str] = set()
    present: set[str] = set(ids)
    for s in splits:
        if not (isinstance(s, dict) and set(s) == set(TASK_SPLIT_FIELDS)):
            problems.append(f"a recorded split is not a map of exactly {TASK_SPLIT_FIELDS}: {s!r}")
            continue
        parent = str(s.get("parent_task_id", ""))
        parts_raw = s.get("part_task_ids")
        if ids.count(parent) != 1:
            problems.append(
                f"split of {parent!r}: its parent appears {ids.count(parent)} time(s) in the "
                f"task list (must be exactly once)")
            continue
        if parent in split_parents:
            problems.append(f"split of {parent!r}: this parent was already split by an earlier "
                            f"recorded split")
            continue
        if not isinstance(parts_raw, list) or not parts_raw:
            problems.append(f"split of {parent!r}: its parts are empty")
            continue
        parts = [str(p) for p in parts_raw]
        if len(set(parts)) != len(parts):
            problems.append(f"split of {parent!r}: its parts repeat: {parts}")
            continue
        already = [p for p in parts if p in present]
        if already:
            problems.append(
                f"split of {parent!r}: its parts {already} are already in the task list")
            continue
        idx = out.index(parent)
        out[idx + 1:idx + 1] = parts
        split_parents.add(parent)
        present.update(parts)
    return out, problems


# F308, DECISION F308 D2 (3): the splits THIS episode recorded, read off the job's own history.
def episode_task_splits(job: JobPlan, episode_id: str) -> tuple[dict, ...]:
    """The record's entries whose `episode_id` equals *episode_id*, in the record's order.

    An entry that is not a map with exactly `TASK_SPLIT_FIELDS` is answered as it is, so the
    checks in `checked_episode_task_list` refuse it rather than this reader dropping it.
    """
    metadata = getattr(job, "metadata", None)
    items = metadata.get(TASK_SPLITS_METADATA_KEY, []) if isinstance(metadata, dict) else []
    if not isinstance(items, list):
        return ()
    out: list[dict] = []
    for entry in items:
        if isinstance(entry, dict) and set(entry) == set(TASK_SPLIT_FIELDS):
            if entry.get("episode_id") == episode_id:
                out.append(dict(entry))
        else:
            out.append(entry)
    return tuple(out)


# F308, DECISION F308 D2 (4): THE F7 CHECK — the declared list with this episode's own splits
# applied, refusing a split record that does not hold or a live list that moved any other way.
def checked_episode_task_list(
    job: JobPlan, job_input: dict, episode_id: str,
) -> tuple[tuple[str, ...], tuple[dict, ...]]:
    """Answer (the list after the splits, the splits) or raise `ManifestError`."""
    from packages.orchestration.pingpong_job import TASK_SPLIT
    from packages.orchestration.run_manifest import ManifestError

    declared_task_ids = [
        str(tk.get("task_id", "")) for tk in (job_input.get("tasks") or [])
        if isinstance(tk, dict)]
    splits = episode_task_splits(job, episode_id)
    after, problems = task_ids_after_splits(declared_task_ids, splits)
    by_id = {str(getattr(t, "task_id", "") or ""): t for t in getattr(job, "tasks", [])}
    for s in splits:
        if not (isinstance(s, dict) and set(s) == set(TASK_SPLIT_FIELDS)):
            continue
        parent_id = str(s.get("parent_task_id", ""))
        parent = by_id.get(parent_id)
        if parent is None or str(getattr(parent, "status", "") or "") != TASK_SPLIT:
            problems.append(
                f"split of {parent_id!r} is recorded for episode {episode_id!r}, but the job "
                f"does not record {parent_id!r} as {TASK_SPLIT!r}")
    if problems:
        raise ManifestError("; ".join(problems))
    live_task_ids = tuple(str(getattr(tk, "task_id", "") or "")
                          for tk in getattr(job, "tasks", []))
    if declared_task_ids and live_task_ids and live_task_ids != tuple(after):
        raise ManifestError(
            f"the job's task list {list(live_task_ids)} no longer matches the episode-start "
            f"snapshot's job-input definition {list(after)} (F7: tasks were added, "
            f"removed or reordered after capture; this episode cannot be finalized against a "
            f"definition it did not run)")
    return tuple(after), tuple(splits)


# F308, DECISION F308 D2 (6): THE VALIDATOR — each recorded split answers for itself.
def task_split_problems(manifest: RunManifestV1) -> list[str]:
    """Problems in `manifest.task_splits`: episode agreement, a non-empty reason, the list
    arithmetic of `task_ids_after_splits`, and each parent's `skipped`/`split` expectation."""
    from packages.orchestration.run_manifest import EXPECT_SKIPPED

    problems: list[str] = []
    splits = getattr(manifest, "task_splits", ())
    if not splits:
        return problems
    for s in splits:
        if not (isinstance(s, dict) and set(s) == set(TASK_SPLIT_FIELDS)):
            problems.append(f"a recorded split is not a map of exactly {TASK_SPLIT_FIELDS}: {s!r}")
            continue
        if s.get("episode_id") != manifest.episode_id:
            problems.append(
                f"split of {s.get('parent_task_id')!r} is recorded for episode "
                f"{s.get('episode_id')!r}, not this manifest's episode {manifest.episode_id!r}")
        if not str(s.get("reason", "")).strip():
            problems.append(f"split of {s.get('parent_task_id')!r} records an empty reason")
    _, arithmetic_problems = task_ids_after_splits(job_input_task_ids(manifest), splits)
    problems.extend(arithmetic_problems)
    by_task = {t.task_id: t for t in manifest.call_expectation.tasks}
    for s in splits:
        if not (isinstance(s, dict) and set(s) == set(TASK_SPLIT_FIELDS)):
            continue
        parent_id = s.get("parent_task_id")
        te = by_task.get(parent_id)
        if te is None:
            problems.append(f"split of {parent_id!r} names a parent with no call expectation")
        elif te.expectation != EXPECT_SKIPPED or te.task_status_at_finalization != "split":
            problems.append(
                f"split of {parent_id!r}: its call expectation is "
                f"{te.expectation!r}/{te.task_status_at_finalization!r}, not skipped/split")
    return problems


# F308, DECISION F308 D2 (2): strict decode of a manifest's optional `task_splits` list.
def decode_task_splits_v1(raw: Any) -> tuple[dict, ...]:
    """At most `MAX_TASKS` maps, each held to exactly `TASK_SPLIT_FIELDS` and the schema's
    existing bounds; a wrong shape raises `SchemaError`."""
    if not isinstance(raw, list):
        raise _S.SchemaError(f"task_splits: expected a JSON array, got {type(raw).__name__}")
    if len(raw) > _S.MAX_TASKS:
        raise _S.SchemaError(f"task_splits: has {len(raw)} entries, exceeding {_S.MAX_TASKS}")
    out: list[dict] = []
    for i, item in enumerate(raw):
        where = f"task_splits[{i}]"
        m = _S.req_map(item, where)
        _S.no_unknown_keys(m, set(TASK_SPLIT_FIELDS), where)
        parent = _S.req_str(m, "parent_task_id", where, max_len=_S.MAX_ID_LEN)
        parts = _S.req_str_list(m, "part_task_ids", where, max_len=_S.MAX_TASKS,
                                max_item_len=_S.MAX_ID_LEN)
        episode = _S.req_str(m, "episode_id", where, max_len=_S.MAX_ID_LEN)
        reason = _S.req_str(m, "reason", where, max_len=_S.MAX_SHORT_TEXT, allow_empty=True)
        out.append({
            "parent_task_id": parent,
            "part_task_ids": list(parts),
            "episode_id": episode,
            "reason": reason,
        })
    return tuple(out)


# F308, DECISION F308 D2 (7): the declared task list's agreement check across a job's episodes
# gets its own function.
def task_list_chain_problems(ordered: list[RunManifestV1]) -> list[str]:
    """Problems where a later episode's declared task list does not pick up exactly where the
    episode directly before it left off — that episode's definition with its own splits applied."""
    problems: list[str] = []
    for earlier, later in zip(ordered, ordered[1:]):
        expected = declared_job_input_task_ids(earlier)
        ids = job_input_task_ids(later)
        if ids != expected:
            problems.append(
                f"episode {later.episode_id}: its embedded job input declares tasks {ids}, but "
                f"episode {earlier.episode_id} left {expected}: the task list is "
                f"immutable across a job's episodes — no addition, removal or reordering")
    return problems
