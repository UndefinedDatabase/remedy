"""Subtree reset mechanics for a job branch task (F029 T001, DECISION F029 D1).

A task's commit on the job branch is its own address: the state before it is the
first parent of that commit, kept alive for as long as the branch lives. Resetting
a task's subtree writes ONE new commit that puts the subtree's changed paths back
to that state; nothing on the branch is ever rewritten.

This module computes a task's subtree (S2), walks the job branch since that
task's commit (S3), plans and refuses an unsafe reset (S4), builds the reset's
commit message (S5) and applies the reset with its hash proof (S6). ``plan_subtree_reset``
and ``apply_subtree_reset`` never write ``job.json``, never change a task's status and take
no lock.

F029 T002, DECISION F029 D2 (round 2): ``prepare_subtree_rerun`` is the ADMISSION and
FOLD this module now also owns. It takes the job's plan-edit lock and its worktree lock,
resets the subtree with ``apply_subtree_reset`` above, returns the subtree's tasks to
pending with the finished attempt archived on each task, and writes the record once. It
runs no provider and starts no task itself — ``remedy job run`` (round 3's command) is
what re-executes the pending subtree afterwards.
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration import checkpoints, dag_schedule, plan_editing, task_veto
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_PAUSED,
    TASK_PENDING,
    TASK_SKIPPED,
    JobPlan,
    TaskEntry,
    _task_stream_dir,
    job_worktree_id,
    load_job_plan,
    save_job_plan,
)

__all__ = [
    "RERUN_TRAILER",
    "RERUN_FILES_NAMED",
    "HUMAN_OVERRIDE_REASON",
    "RERUN_ADMITTED_STATES",
    "SubtreeRerunRefused",
    "SubtreeRerunError",
    "rerun_subtree_ids",
    "branch_commits_since",
    "plan_subtree_reset",
    "build_rerun_commit_message",
    "apply_subtree_reset",
    "fold_subtree_rerun",
    "prepare_subtree_rerun",
]

#: S1 — the trailer a rerun's reset commit carries beside ``Remedy-Job``, naming
#: the root task the reset put back.
RERUN_TRAILER = "Remedy-Rerun"

#: S1 — how many changed paths a rerun's commit message names before "...".
RERUN_FILES_NAMED = 5

#: DECISION F029 D2 — the `reruns` record's `model.reason` when an override was given.
HUMAN_OVERRIDE_REASON = "human_override"

#: DECISION F029 D2 — the job states `prepare_subtree_rerun` admits a rerun from.
RERUN_ADMITTED_STATES: frozenset[str] = frozenset({"completed", "blocked", "paused", "stopped"})

#: DECISION F029 D2 — a rerun's model override, when given: a plain model-name token.
_MODEL_OVERRIDE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}$")


class SubtreeRerunRefused(Exception):
    """A rerun cannot proceed safely; ``code`` and ``detail`` say why.

    ``facts`` carries structured evidence beyond the prose — currently only the
    ``interleaved`` refusal's list of conflicting commits.
    """

    def __init__(self, code: str, detail: str, facts: dict[str, Any] | None = None) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail
        self.facts: dict[str, Any] = facts if facts is not None else {}


class SubtreeRerunError(RuntimeError):
    """A reset's own hash proof failed after its commit was already made."""


def _join_listing(items: Sequence[str]) -> str:
    """The first ten of ``items`` joined with ``", "``, ``" and N more"`` beyond that."""
    head = list(items[:10])
    listing = ", ".join(head)
    if len(items) > 10:
        listing += f" and {len(items) - 10} more"
    return listing


def _status_paths(worktree_path: str | Path) -> list[str]:
    """Paths ``git status --porcelain=v1 -z --untracked-files=all`` names, sorted.

    A rename or copy entry's SECOND path (the original) is skipped: only the
    path the worktree now holds is a live uncommitted change.
    """
    out = W._git(worktree_path, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    parts = out.split("\0")
    paths: list[str] = []
    i = 0
    while i < len(parts):
        entry = parts[i]
        if not entry:
            i += 1
            continue
        code = entry[:2]
        paths.append(entry[3:])
        i += 2 if ("R" in code or "C" in code) else 1
    return sorted(paths)


def _read_trailers_at(worktree_path: str | Path, sha: str) -> dict[str, str]:
    """The ``Remedy-Task`` and ``Remedy-Rerun`` trailers of ``sha``, as read_head_remedy_trailers reads HEAD's."""
    out = W._git(worktree_path, "log", "-1", "--format=%(trailers:only,unfold)", sha)
    found: dict[str, str] = {}
    for line in out.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() in (W.REMEDY_TASK_TRAILER, RERUN_TRAILER):
            found[key.strip()] = value.strip()
    return found


def _tree_entry(worktree_path: str | Path, tree: str, path: str) -> tuple[str, str] | None:
    """``(mode, blob_sha)`` of ``path`` in ``tree``, or None when ``tree`` holds no entry there."""
    if not tree:
        return None
    proc = subprocess.run(
        ["git", "ls-tree", "-z", tree, "--", path], cwd=str(worktree_path),
        capture_output=True, text=True, timeout=W.GIT_QUERY_TIMEOUT_SEC,
    )
    if proc.returncode != 0:
        return None
    entry = proc.stdout.split("\0")[0]
    if not entry.strip():
        return None
    meta, _, _ = entry.partition("\t")
    mode, _, rest = meta.partition(" ")
    _, _, sha = rest.partition(" ")
    return (mode, sha)


def rerun_subtree_ids(tasks: Sequence[TaskEntry], root_task_id: str) -> list[str]:
    """The root and every task depending on it directly or transitively, in plan order.

    Every task is included WHATEVER its status: a completed dependent is still
    part of the subtree that must go back to pending. Raises
    ``SubtreeRerunRefused("unknown_task", ...)`` when ``root_task_id`` names no
    task here.
    """
    ids = [t.task_id for t in tasks]
    if root_task_id not in ids:
        raise SubtreeRerunRefused(
            "unknown_task",
            f"there is no task {root_task_id!r} in this job; its tasks are: {_join_listing(ids)}",
        )

    nodes = dag_schedule.build_graph(tasks)
    included = {root_task_id}
    changed = True
    while changed:
        changed = False
        for node in nodes:
            if node.task_id in included:
                continue
            if any(dep in included for dep in node.depends_on):
                included.add(node.task_id)
                changed = True

    return [t.task_id for t in tasks if t.task_id in included]


def branch_commits_since(worktree_path: str | Path, base: str) -> list[dict[str, Any]]:
    """Every commit of ``git rev-list --reverse --first-parent {base}..HEAD``, oldest first.

    Each dict: ``sha``, ``task_id`` (its ``Remedy-Task`` trailer, "" when absent),
    ``rerun_of`` (its ``Remedy-Rerun`` trailer, "" when absent) and ``paths`` (the
    sorted paths ``git diff --name-only --no-renames`` reports against its
    first parent).
    """
    out = W._git(worktree_path, "rev-list", "--reverse", "--first-parent", f"{base}..HEAD")
    shas = [line.strip() for line in out.splitlines() if line.strip()]
    commits: list[dict[str, Any]] = []
    for sha in shas:
        trailers = _read_trailers_at(worktree_path, sha)
        diff_out = W._git(
            worktree_path, "diff", "--name-only", "--no-renames", "-z", f"{sha}^", sha,
        )
        paths = sorted(p for p in diff_out.split("\0") if p)
        commits.append({
            "sha": sha,
            "task_id": trailers.get(W.REMEDY_TASK_TRAILER, ""),
            "rerun_of": trailers.get(RERUN_TRAILER, ""),
            "paths": paths,
        })
    return commits


def _build_target_tree(worktree_path: str | Path, base: str, paths: Sequence[str]) -> str:
    """The tree object equal to ``HEAD`` except ``paths`` reset to their entry in ``base``.

    Built in a private temporary index, exactly as ``worktrees.write_tree_at``
    manages ``GIT_INDEX_FILE`` — the worktree's real index is never touched.
    """
    fd, tmp = tempfile.mkstemp(prefix="remedy-subtree-index-")
    os.close(fd)
    os.unlink(tmp)
    env = {**os.environ, "GIT_INDEX_FILE": tmp}
    try:
        proc = subprocess.run(
            ["git", "read-tree", "HEAD"], cwd=str(worktree_path), env=env,
            capture_output=True, text=True, timeout=W.GIT_QUERY_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            raise W.WorktreeError(f"git read-tree for subtree target failed: {proc.stderr[:200]}")

        for path in paths:
            entry = _tree_entry(worktree_path, base, path)
            if entry is None:
                rm = subprocess.run(
                    ["git", "update-index", "--force-remove", "--", path],
                    cwd=str(worktree_path), env=env, capture_output=True, text=True,
                    timeout=W.GIT_QUERY_TIMEOUT_SEC,
                )
                if rm.returncode != 0:
                    raise W.WorktreeError(
                        f"git update-index --force-remove failed for {path!r}: {rm.stderr[:200]}")
                continue
            mode, sha = entry
            add = subprocess.run(
                ["git", "update-index", "--add", "--replace", "--cacheinfo", f"{mode},{sha},{path}"],
                cwd=str(worktree_path), env=env, capture_output=True, text=True,
                timeout=W.GIT_QUERY_TIMEOUT_SEC,
            )
            if add.returncode != 0:
                raise W.WorktreeError(
                    f"git update-index --cacheinfo failed for {path!r}: {add.stderr[:200]}")

        wt = subprocess.run(
            ["git", "write-tree"], cwd=str(worktree_path), env=env,
            capture_output=True, text=True, timeout=W.GIT_QUERY_TIMEOUT_SEC,
        )
        if wt.returncode != 0:
            raise W.WorktreeError(f"git write-tree for subtree target failed: {wt.stderr[:200]}")
        return wt.stdout.strip()
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def plan_subtree_reset(job: JobPlan, root_task_id: str, worktree_path: str | Path) -> dict[str, Any]:
    """Read-only: the subtree, the walk and the target tree of a rerun from ``root_task_id``.

    Raises ``SubtreeRerunRefused`` from the first unsafe condition, in order:
    an unknown task, a copy-mode job, an uncommitted root task, a drifted or
    dirty worktree, a root commit not on the branch, a subtree task whose
    commit precedes the root's, and interleaving with work outside the
    subtree. Raises ``SubtreeRerunError`` when an EXACT reset's target tree
    disagrees with the tree before the root task — an invariant, never a user
    refusal.
    """
    subtree_ids = rerun_subtree_ids(job.tasks, root_task_id)          # a
    tasks_by_id = {t.task_id: t for t in job.tasks}
    root_task = tasks_by_id[root_task_id]

    if job.isolation_mode != "worktree":                              # b
        raise SubtreeRerunRefused(
            "not_worktree_mode",
            "the job ran in a copy of the repository, not on a job branch, "
            "so no task has a commit to go back to",
        )

    if not root_task.worktree_commit:                                 # c
        raise SubtreeRerunRefused(
            "task_not_committed",
            f"task {root_task_id} has no commit on the job branch yet, "
            f"so there is nothing to rerun",
        )

    live_head = W.head_at(worktree_path)
    if not live_head or live_head != job.worktree_head:               # d (R-1080)
        raise SubtreeRerunRefused(
            "worktree_drift",
            checkpoints.worktree_drift_message(job.worktree_head, live_head or "unknown"),
        )

    if not W.worktree_matches_head(worktree_path):                    # e
        listing = _join_listing(_status_paths(worktree_path))
        raise SubtreeRerunRefused(
            "worktree_dirty",
            f"the job worktree holds uncommitted changes to {listing}; "
            f"commit or discard them before a rerun",
        )

    root_commit = root_task.worktree_commit
    if not W.is_ancestor(worktree_path, root_commit, "HEAD"):         # f
        raise SubtreeRerunRefused(
            "commit_not_on_branch",
            f"task {root_task_id}'s commit {root_commit[:12]} is not on this job's branch",
        )

    base = W._git(worktree_path, "rev-parse", f"{root_commit}^").strip()
    commits = branch_commits_since(worktree_path, base)
    commit_shas = {c["sha"] for c in commits}

    for tid in subtree_ids:                                           # g
        task = tasks_by_id[tid]
        if task.worktree_commit and task.worktree_commit not in commit_shas:
            raise SubtreeRerunRefused(
                "subtree_order",
                f"task {tid} depends on {root_task_id} but its commit "
                f"{task.worktree_commit[:12]} is not after {root_task_id}'s on the job "
                f"branch; rerun from an earlier task",
            )

    subtree_id_set = set(subtree_ids)
    in_paths: set[str] = set()
    for commit in commits:
        if commit["task_id"] in subtree_id_set:
            in_paths.update(commit["paths"])

    interleaving: list[dict[str, Any]] = []
    for commit in commits:                                            # h
        if commit["task_id"] not in subtree_id_set:
            shared = sorted(set(commit["paths"]) & in_paths)
            if shared:
                name = commit["task_id"] or f"commit {commit['sha'][:12]}"
                interleaving.append({"by": name, "paths": shared})
    if interleaving:
        parts = "; ".join(f"{d['by']} changed {', '.join(d['paths'])}" for d in interleaving)
        raise SubtreeRerunRefused(
            "interleaved",
            f"rerunning {root_task_id} would also undo work outside its subtree: {parts}; "
            f"start the rerun at an earlier task whose subtree includes that work",
            facts={"interleaving": interleaving},
        )

    sorted_paths = sorted(in_paths)
    target_tree = _build_target_tree(worktree_path, base, sorted_paths)
    base_tree = W._git(worktree_path, "rev-parse", f"{base}^{{tree}}").strip()
    exact = all(commit["task_id"] in subtree_id_set for commit in commits)

    if exact and target_tree != base_tree:
        raise SubtreeRerunError(
            f"exact reset's target tree {target_tree} does not equal the tree before "
            f"{root_task_id}, {base_tree}",
        )

    return {
        "job_id": job.job_id,
        "root_task_id": root_task_id,
        "subtree": subtree_ids,
        "base_commit": base,
        "head_commit": live_head,
        "commits": [dict(commit, in_subtree=(commit["task_id"] in subtree_id_set))
                    for commit in commits],
        "paths": sorted_paths,
        "target_tree": target_tree,
        "base_tree": base_tree,
        "exact": exact,
        "root_start_tree": root_task.task_start_tree or "",
    }


def build_rerun_commit_message(job: JobPlan, plan: dict[str, Any]) -> str:
    """The reset commit's message: subject, body naming what changed, then its trailers."""
    root = plan["root_task_id"]
    n = len(plan["subtree"]) - 1
    subject = f"rerun: reset task {root} and {n} dependent task{'' if n == 1 else 's'}\n\n"

    paths = plan["paths"]
    if not paths:
        changed = "changing no file"
    else:
        named = ", ".join(paths[:RERUN_FILES_NAMED])
        if len(paths) > RERUN_FILES_NAMED:
            named += ", ..."
        changed = f"changing {named}"

    body = (
        f"Remedy reset task {root} of job {job.job_id} and the tasks depending on it to "
        f"their state before commit {plan['base_commit'][:12]}, {changed}.\n\n"
    )
    return (subject + body
            + f"{W.REMEDY_JOB_TRAILER}: {job.job_id}\n"
            + f"{RERUN_TRAILER}: {root}\n")


def apply_subtree_reset(job: JobPlan, root_task_id: str, worktree_path: str | Path) -> dict[str, Any]:
    """Plan, then commit the reset — and prove it before handing the result back.

    Does not touch ``job``: T002's caller records the new head and returns the
    subtree's tasks to pending. Raises ``SubtreeRerunError`` naming the failed
    check and path when the proof fails; the commit stays, nothing is rewritten.
    """
    plan = plan_subtree_reset(job, root_task_id, worktree_path)

    branch = W._git(worktree_path, "rev-parse", "--abbrev-ref", "HEAD").strip()
    handle = W.WorktreeHandle(
        job_id=job.job_id, repo_path=job.repo_path, path=str(worktree_path), branch=branch,
    )
    restored = W.restore_tree(handle, plan["target_tree"])
    reset_commit = W.commit_job_worktree(str(worktree_path), build_rerun_commit_message(job, plan))
    reset_tree = W._git(worktree_path, "rev-parse", f"{reset_commit}^{{tree}}").strip()

    if reset_tree != plan["target_tree"]:
        raise SubtreeRerunError(
            f"tree_equals_target check failed: reset commit {reset_commit} has tree "
            f"{reset_tree}, expected {plan['target_tree']}",
        )

    for path in plan["paths"]:
        new_entry = _tree_entry(worktree_path, reset_commit, path)
        base_entry = _tree_entry(worktree_path, plan["base_commit"], path)
        if new_entry != base_entry:
            raise SubtreeRerunError(
                f"paths_equal check failed at {path!r}: reset commit entry {new_entry} "
                f"does not equal the entry before {root_task_id}, {base_entry}",
            )

    if plan["exact"] and reset_tree != plan["base_tree"]:
        raise SubtreeRerunError(
            f"tree_equals_base check failed: reset commit {reset_commit} has tree "
            f"{reset_tree}, expected {plan['base_tree']}",
        )

    result = dict(plan)
    result["reset_commit"] = reset_commit
    result["reset_tree"] = reset_tree
    result["restored"] = restored
    result["proof"] = {
        "paths_checked": len(plan["paths"]),
        "paths_equal": True,
        "tree_equals_base": plan["exact"],
    }
    result["pre_task_tree_equal"] = (
        None if not (plan["exact"] and plan["root_start_tree"])
        else reset_tree == plan["root_start_tree"]
    )
    return result


def _task_ran(task: TaskEntry) -> bool:
    """DECISION F029 D2 — a task RAN when it has a run id or a commit, or its status
    ever moved off pending. A never-started subtree task keeps its attempt at 1 and
    gets no attempt record."""
    return bool(task.run_id) or bool(task.worktree_commit) or task.status != TASK_PENDING


def fold_subtree_rerun(
    job: JobPlan,
    reset: dict[str, Any],
    *,
    rerun_id: str,
    model_override: str,
    actor: str,
    now: datetime,
    moved_streams: dict[str, str],
) -> dict[str, Any]:
    """Pure: fold a subtree reset into *job* in memory and return its new ``reruns`` entry.

    ``reset`` is what ``apply_subtree_reset`` answered; ``moved_streams`` maps a task id
    to the evidence-relative path its earlier stream directory was moved to. Writes
    nothing to disk — the caller persists ``job`` once, after this returns.
    """
    tasks_by_id = {t.task_id: t for t in job.tasks}
    subtree_id_set = set(reset["subtree"])
    state_before = str(job.state)

    for task_id in reset["subtree"]:
        task = tasks_by_id[task_id]
        if _task_ran(task):
            task.attempts.append({
                "attempt": task.attempt,
                "status": task.status,
                "final_status": task.final_status,
                "reviewer_verdict": task.reviewer_verdict,
                "test_passed": task.test_passed,
                "run_id": task.run_id,
                "worktree_commit": task.worktree_commit,
                "model_override": task.model_override,
                "output_artifact_ids": list(task.output_artifact_ids),
                "stream_evidence": moved_streams.get(task_id, ""),
                "rerun_id": rerun_id,
                "ended_at": now.isoformat(),
            })
            task.attempt += 1
        task.status = TASK_PENDING
        task.model_override = model_override
        task.run_id = ""
        task.final_status = ""
        task.final_status_detail = ""
        task.reviewer_verdict = ""
        task.error = ""
        task.task_start_tree = ""
        task.task_start_tree_ref = ""
        task.task_start_recorded_at = ""
        task.task_attempt_state = ""
        task.worktree_commit = ""
        task.tripped_limit = ""
        task.safe_diff_files = []
        task.output_artifact_ids = []
        task.test_passed = None
        task.apply_manifest = None
        task.proof_summary = None
        task.repair_rounds_used = 0

    restored_pending: list[str] = []
    for task in job.tasks:
        if task.task_id not in subtree_id_set and task.status == TASK_SKIPPED:
            task.status = TASK_PENDING
            restored_pending.append(task.task_id)

    job.worktree_head = reset["reset_commit"]
    if job.state == JOB_COMPLETED:
        job.state = JOB_PAUSED
        job.finished_at = ""
    job.worktree_cleanup_status = "retained"
    job.worktree_cleanup_error = ""

    configured_model = job.execution_config.builder_model if job.execution_config else ""
    record: dict[str, Any] = {
        "rerun_id": rerun_id,
        "root_task_id": reset["root_task_id"],
        "subtree": list(reset["subtree"]),
        "restored_pending": restored_pending,
        "base_commit": reset["base_commit"],
        "reset_commit": reset["reset_commit"],
        "paths": list(reset["paths"]),
        "exact": reset["exact"],
        "proof": reset["proof"],
        "pre_task_tree_equal": reset["pre_task_tree_equal"],
        "model": {
            "override": model_override,
            "configured": configured_model,
            "reason": HUMAN_OVERRIDE_REASON if model_override else "",
        },
        "actor": actor,
        "at": now.isoformat(),
        "state_before": state_before,
        "state_after": str(job.state),
    }
    job.reruns.append(record)
    return record


def prepare_subtree_rerun(
    job_id: str,
    root_task_id: str,
    *,
    model_override: str = "",
    actor: str = "operator",
    now: datetime | None = None,
) -> dict[str, Any]:
    """DECISION F029 D2 — prepare a subtree rerun on a job that is NOT running.

    Re-acquires the job's worktree under its lock (re-adding it from the kept branch
    when the job had completed), resets the subtree with ``apply_subtree_reset``, and
    returns the subtree's tasks to pending with the finished attempt archived on each
    (S4's fold, ``fold_subtree_rerun``). Runs no provider and starts no task itself:
    ``remedy job run`` (round 3's command) is what re-executes the pending subtree.

    Raises ``SubtreeRerunRefused`` from the first unsafe condition, admission checks
    before anything worktree-related is touched, then ``apply_subtree_reset``'s own
    ladder once the worktree is claimed. A refusal removes a worktree this call
    created, or releases the lock on one that already existed, and leaves ``job.json``
    unchanged.
    """
    bounded_actor = task_veto._bounded_actor(actor)
    at = now or datetime.now(timezone.utc)

    with plan_editing.plan_edit_lock(job_id):
        job = load_job_plan(job_id)
        if job is None:
            raise SubtreeRerunRefused("job_not_found", f"there is no job {job_id!r}")

        if model_override and not _MODEL_OVERRIDE_RE.match(model_override):
            raise SubtreeRerunRefused(
                "model_invalid",
                f"{model_override!r} is not a valid model override; it must match "
                f"{_MODEL_OVERRIDE_RE.pattern}",
            )

        state = str(job.state)
        if state == "running":
            raise SubtreeRerunRefused(
                "job_running", "the job is running; pause or stop it, then rerun")
        if state not in RERUN_ADMITTED_STATES:
            raise SubtreeRerunRefused(
                "job_not_rerunnable",
                f"the job is {state!r}; a rerun needs a job that has completed, "
                f"blocked, paused or stopped",
            )

        subtree_ids = rerun_subtree_ids(job.tasks, root_task_id)   # unknown_task
        tasks_by_id = {t.task_id: t for t in job.tasks}
        root_task = tasks_by_id[root_task_id]

        if job.isolation_mode != "worktree":
            raise SubtreeRerunRefused(
                "not_worktree_mode",
                "the job ran in a copy of the repository, not on a job branch, "
                "so no task has a commit to go back to",
            )
        if not root_task.worktree_commit:
            raise SubtreeRerunRefused(
                "task_not_committed",
                f"task {root_task_id} has no commit on the job branch yet, "
                f"so there is nothing to rerun",
            )
        if not W._branch_exists(job.repo_path, job.worktree_branch):
            raise SubtreeRerunRefused(
                "job_branch_missing",
                f"job branch {job.worktree_branch!r} no longer exists",
            )
        if not job.job_initial_tree or not W.object_exists(job.repo_path, job.job_initial_tree):
            raise SubtreeRerunRefused(
                "checkpoint_object_missing",
                f"the job's initial tree {job.job_initial_tree!r} is gone",
            )

        try:
            handle = W.create(job_worktree_id(job_id), job.repo_path)
        except W.WorktreeLockError:
            raise SubtreeRerunRefused(
                "job_running", "the job is running; pause or stop it, then rerun") from None
        except W.WorktreeConflictError as exc:
            raise SubtreeRerunRefused("worktree_conflict", str(exc)) from exc

        try:
            reset = apply_subtree_reset(job, root_task_id, handle.path)
        except SubtreeRerunRefused:
            if handle.created:
                W.remove(handle, keep_branch=True)
            else:
                W.release_lock(handle)
            raise
        except (SubtreeRerunError, W.WorktreeError) as exc:
            # Every OTHER exception `apply_subtree_reset` can raise: a failed hash
            # proof or a git operation on the worktree itself. Kept for recovery,
            # never removed — an unproven or half-made reset must stay inspectable.
            W.retain_for_recovery(handle, f"{type(exc).__name__}: {exc}")
            raise

        moved_streams: dict[str, str] = {}
        evidence_root = job_evidence_dir(job_id)
        for task_id in subtree_ids:
            task = tasks_by_id[task_id]
            if not _task_ran(task):
                continue
            stream_dir = _task_stream_dir(job_id, task_id)
            if not stream_dir.exists():
                continue
            dest_rel = f"rerun_attempts/{task_id}/attempt-{task.attempt}"
            dest = evidence_root / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stream_dir, dest)
            moved_streams[task_id] = dest_rel

        rerun_id = f"rerun-{len(job.reruns) + 1}"
        record = fold_subtree_rerun(
            job, reset, rerun_id=rerun_id, model_override=model_override,
            actor=bounded_actor, now=at, moved_streams=moved_streams,
        )

        ref = job.job_initial_tree_ref
        if W.resolve_checkpoint_ref(job.repo_path, ref) != job.job_initial_tree:
            W.set_checkpoint_ref(job.repo_path, ref, job.job_initial_tree)

        save_job_plan(job)
        W.release_lock(handle)

        return {**record, "job_id": job_id, "worktree_rematerialized": handle.created}
