"""The study step of a `remedy do` walk: study the repository once, again when the repository moved on.

Moved out of `packages/orchestration/do_sequence.py` unchanged in meaning, as a step of that file's
boundary on `docs/system/structure-ledger-v1.md` (the file fell under its 1,000-line row when the
scale audit of 2026-10-17 added the staleness and hold checks to this step).
"""

from __future__ import annotations

import shlex
import subprocess

from packages.orchestration.do_context import (
    DO_STEP_DONE,
    DO_STEP_SKIPPED,
    DO_STEP_STOPPED,
    DoContext,
)
from packages.orchestration.do_lane import settle_do_lane


def repo_has_committed_file(repo_root: str) -> bool:
    """At least one commit exists and HEAD holds at least one tracked file."""
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
        cwd=repo_root, capture_output=True, text=True, timeout=30,
    )
    return proc.returncode == 0 and bool(proc.stdout.strip())


def do_step_study(ctx: DoContext) -> tuple[str, str]:
    """Study the repository exactly once, and only when it is non-empty (D3)."""
    from packages.orchestration.study import (
        record_study_pass,
        run_study,
        study_call_fn,
        study_stale_reason,
    )

    lane = settle_do_lane(ctx)
    if lane.hold:
        # Audit P0-1: an order that cannot be placed is a question, never a guess that edits files.
        return DO_STEP_STOPPED, f"nothing was planned or run: {lane.reason}"
    metadata = ctx.project.metadata
    stale = ""
    if metadata.get("studied_at"):
        stale = study_stale_reason(ctx.repo_root, str(metadata.get("studied_head") or ""))
        if not stale:
            return DO_STEP_SKIPPED, (
                f"already studied at {metadata['studied_at']} "
                f"(head {metadata.get('studied_head') or 'none'}); study again by hand: "
                f"remedy study run --path {shlex.quote(ctx.repo_root)}")
    if not repo_has_committed_file(ctx.repo_root):
        return DO_STEP_SKIPPED, (
            f"{ctx.repo_root} has no commit holding a tracked file — nothing to study")

    # Amend1014 D1 and audit P1-7: a bounded order is studied from facts, with no narration call, in a
    # repository of any size: a README edit in a 10,000-file repository needs no whole-repository model pass.
    # exec-1018 (R-1352): nor does any order on a tiny repository, whose facts the planner sees whole
    # (measured: four narration calls, 23.8 of 27.5 s, on six files).
    call_fn = None if ctx.no_llm or lane.bounded or ctx.tiny_repo else study_call_fn()
    result = run_study(ctx.repo_root, project_id=str(ctx.project.id), call_fn=call_fn)
    updated = record_study_pass(str(ctx.project.id), ctx.repo_root)
    if updated is not None:
        ctx.project = updated
    detail = f"{len(result.cards_written)} memory card(s) written for project {ctx.project.slug}"
    if stale:
        detail += f" (studied again: {stale})"
    if result.partial:
        detail += f" (PARTIAL — {result.stopped_reason})"
    return DO_STEP_DONE, detail
