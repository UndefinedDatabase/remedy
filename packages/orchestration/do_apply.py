"""F268, F270 — the apply step of a `remedy do` walk: each job applied with the walk's commit
flag, and the mission's one push;
moved out of `packages/orchestration/do_sequence.py` unchanged, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D3);
`do_sequence.py` imports every name back by name, so each import path keeps working.
"""

from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any

from packages.orchestration.do_context import (
    DO_STEP_DONE,
    DO_STEP_FAILED,
    DO_STEP_STOPPED,
    DoContext,
    _job_run_role_flags,
    do_stopped_walk_note,
)


def do_waiting_job_next_lines(ctx: DoContext) -> list[str]:
    """One line per waiting job, with real ids: commit its predecessor's applied output, then run it.

    DECISION F268 D12: a job's workspace is cut from the target's HEAD commit,
    so a waiting job runs only once the job before it is applied AND committed.
    """
    repo = shlex.quote(ctx.repo_root)
    lines = []
    for position, job_id in enumerate(ctx.job_ids):
        if job_id not in ctx.waiting_job_ids:
            continue
        before = ctx.job_ids[position - 1]
        lines.append(f"commit job {before}'s applied output in {repo}, then: "
                     f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
    return lines


def _step_apply(ctx: DoContext) -> tuple[str, str]:
    """Stop before apply, printing the apply command per job that ran; `--apply` applies them.

    With `--apply` each job that ran goes through `job_apply.apply_job(...,
    approve=True)` in run order, and the walk fails at the first job that is not
    applied, naming it and why (DECISION F268 D9 (2)). The apply gate is
    `job_apply`'s own. A waiting job is never applied here; the Next lines say
    how it runs (DECISION F268 D12). Under a commit flag the jobs the run step
    already applied are not applied again, and a push is asked once after the
    last job (DECISION F270 D4 (4)); in a walk of one job a red contract
    refuses it before anything is applied (D4 (6)).
    """
    if not ctx.apply:
        commands = [f"remedy job apply {job_id} --repo {shlex.quote(ctx.repo_root)} --approve"
                    for job_id in ctx.run_job_ids]
        ctx.next_lines.extend(commands)
        ctx.next_lines.extend(do_waiting_job_next_lines(ctx))
        return DO_STEP_STOPPED, (
            f"stopped before apply; {ctx.repo_root} is untouched. "
            f"Apply the reviewed result with: {'; then '.join(commands)}")

    if ctx.push and len(ctx.run_job_ids) == 1:
        # D4 (6): one job's contract is final once it ran, so red refuses before anything.
        refusals, still_open, unchecked = do_mission_push_refusals(ctx)
        if refusals:
            ctx.push_outcome = _do_push_record(
                ctx, "", still_open, unchecked, error=" ".join(refusals))
            return DO_STEP_FAILED, (
                f"{ctx.push_source} was refused, so nothing was applied, committed or "
                f"pushed: {' '.join(refusals)}")

    for job_id in ctx.run_job_ids:
        if job_id in ctx.applied:
            continue
        failure = do_apply_one_job(ctx, job_id)
        if failure:
            return DO_STEP_FAILED, failure + (do_stopped_walk_note(ctx) if ctx.commit_mode else "")
    ctx.next_lines.extend(do_waiting_job_next_lines(ctx))
    detail = f"{'; '.join(ctx.applied.values())} to {ctx.repo_root}"
    if not ctx.push:
        return DO_STEP_DONE, detail
    status, sentence = do_push_mission(ctx)
    return status, f"{detail}; {sentence}"


def do_apply_one_job(ctx: DoContext, job_id: str) -> str:
    """Apply one job with the walk's commit flag and never its push; "" or why it was not applied.

    Without a commit flag the call is `apply_job(job_id, repo, approve=True)`,
    exactly as before F270. In a walk of several jobs `--commit`'s line gains
    ` (job <k> of <n>)` and `--commit-auto` asks each job's title first
    (DECISION F270 D4 (3)). What landed is added to ``ctx.landed``.
    """
    from packages.orchestration.job_apply import apply_job

    flags: dict[str, Any] = {}
    if ctx.commit_mode:
        total = len(ctx.job_ids)
        message = ctx.commit_message
        if message is not None and total > 1:
            message = f"{message.strip()} (job {ctx.job_ids.index(job_id) + 1} of {total})"
        # D4 (4): the push is the mission's, asked once after the last job, never here.
        flags = {"commit_message": message, "commit_auto": ctx.commit_auto,
                 "commit_with_history": ctx.commit_with_history,
                 "commit_auto_title_first": total > 1}
    result = apply_job(job_id, ctx.repo_root, approve=True, **flags)
    if result.status != "applied":
        why = result.blocked_reason or "; ".join(result.blocked_reasons) or "no reason given"
        ctx.next_lines.append(f"remedy job apply {job_id} --repo "
                              f"{shlex.quote(ctx.repo_root)} --dry-run")
        before = (f"; applied before it: {'; '.join(ctx.applied.values())}"
                  if ctx.applied else "")
        return (f"job {job_id} was not applied to {ctx.repo_root} "
                f"(status {result.status}): {why}{before}")
    said = f"job {job_id} applied {len(result.files_applied)} file(s)"
    if result.commit_sha:
        ctx.landed.append({"job_id": job_id, "sha": result.commit_sha,
                           "branch": result.target_branch})
        said += f" and landed {result.commit_sha[:12]} on {result.target_branch}"
    ctx.applied[job_id] = said
    return ""


def do_mission_push_refusals(ctx: DoContext) -> tuple[list[str], list[str], list[str]]:
    """``(refusals, open, unchecked)`` for the walk's one push: the upstream's, then the
    mission's; reads only.

    `job_apply`'s own refusals (DECISIONs F270 D3 (5), D4 (6) and F299 D2 (6)),
    asked of the walk's mission rather than of one job's.
    """
    from packages.orchestration.job_apply import mission_push_refusals, upstream_push_refusals
    from packages.orchestration.mission_state import load_mission

    def read_mission() -> Any:
        if not ctx.mission_id or ctx.project is None:
            return None
        return load_mission(str(ctx.project.id), ctx.mission_id)

    refusals, still_open, unchecked = mission_push_refusals(read_mission)
    return upstream_push_refusals(Path(ctx.repo_root)) + refusals, still_open, unchecked


def _do_push_record(ctx: DoContext, sha: str, still_open: list[str], unchecked: list[str], *,
                    error: str = "") -> dict[str, Any]:
    """The `push` object of `do --json` (DECISION F270 D4 (7)), before the push is tried."""
    return {"pushed": False, "sha": sha, "remote": "", "ref": "", "error": error,
            "source": ctx.push_source, "open_blocking_criteria": list(still_open),
            "unchecked_blocking_criteria": list(unchecked)}


def do_push_mission(ctx: DoContext) -> tuple[str, str]:
    """Push the walk's last landed commit ONCE, never forced; ``(status, sentence)``.

    DECISION F270 D4 (4): push is a mission-level act, so it runs once, after
    the last job, through the push `job apply` uses. The refusals are asked
    again first; a refused or failed push leaves every commit where it landed
    and fails the step, so `do` exits 1. The blocking criteria still open and
    those unchecked are named whatever happens (D4 (6), DECISION F299 D2 (6)).
    """
    from packages.orchestration.job_apply import (
        push_open_criteria_sentence,
        push_to_upstream,
        push_unchecked_criteria_sentence,
    )

    if not ctx.landed:
        return DO_STEP_DONE, "nothing landed, so nothing was pushed"
    last = ctx.landed[-1]
    refusals, still_open, unchecked = do_mission_push_refusals(ctx)
    ctx.push_outcome = _do_push_record(ctx, last["sha"], still_open, unchecked)
    sentences = [push_open_criteria_sentence(still_open).rstrip("."),
                push_unchecked_criteria_sentence(unchecked).rstrip(".")]
    named = "; ".join(s for s in sentences if s)
    named = f"; {named}" if named else ""
    if refusals:
        ctx.push_outcome["error"] = " ".join(refusals)
        return DO_STEP_FAILED, (
            f"{ctx.push_source} was refused after the commits landed, so nothing was pushed "
            f"and they stay on {last['branch']}: {' '.join(refusals)}")
    outcome = push_to_upstream(Path(ctx.repo_root), last["sha"], last["branch"])
    ctx.push_outcome.update(pushed=outcome.pushed, remote=outcome.remote,
                            ref=outcome.ref, error=outcome.error)
    if not outcome.pushed:
        return DO_STEP_FAILED, (
            f"the push of {last['sha'][:12]} failed ({outcome.error}); the commit stays on "
            f"{last['branch']}, so push it by hand once the cause is fixed{named}")
    return DO_STEP_DONE, (f"pushed {last['sha'][:12]} to {outcome.remote} {outcome.ref} once, "
                          f"never forced ({ctx.push_source}){named}")
