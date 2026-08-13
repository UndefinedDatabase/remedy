"""Diff-only repair apply and fallback (F111 T002, apply half).

A repair round that answered with a unified diff either LANDS that diff or
falls back to today's full-file round. This module is the one place that
decision is made: it validates the answer, asks the fences BEFORE any file is
opened, converts the answer into the shape the existing applicator takes, and
reports the outcome as a mode — ``diff`` or ``full_fallback`` — with a NAMED
``fallback_reason`` on every path that did not land.

This module implements NO rollback and NO diff parsing of its own. The
all-or-nothing guarantee is ``source_apply``'s durable snapshot: created and
verified before any mutation, and restoring every touched file when a hunk
conflicts AND the restore itself succeeds. So a partially applied patch never
reaches the caller — what reaches it is ``full_fallback`` plus the applicator's
own error strings. Remedy deliberately does not add a second applier, a second
rollback, or a second reading of unified-diff syntax here.

When the restore does NOT succeed, the applicator says so: it catches OSError
per entry and appends ``rollback_incomplete (N file(s)): …`` to its errors,
leaving those files half-restored. This module refuses to summarise that as a
clean tree (finding R-0316): ``rollback_incomplete`` is then True and
``files_modified`` carries the applicator's real count instead of a reassuring
zero. A zero here means the tree is untouched by fact, not by convention.

A fence-denied path is rejected BEFORE the applicator runs, not by it. The
applicator's own ``enforce_change_set`` raises, and a raise mid-apply is not a
fallback; ``precheck_diff_repair_fences`` answers the same question as data, so
the acceptance criterion "a diff targeting a fence-denied path never reaches
the applicator" holds by construction. Both readings use the SAME fence spec:
when the caller passes no ``job_fences``, this module derives them from the job
exactly as ``apply_structured_patch`` does, so precheck and applicator cannot
disagree.

Creation diffs are NOT applied as diffs in v1 (DECISION F111 D6,
docs/roadmap/features/T2_F111.md): the applicator requires the target file to
exist, so a ``@@ -0,0 +1,N @@`` answer fails the apply and falls back to the
full-file path, which creates files through ``_apply_file_op``'s ``create``
action under the same durable snapshot.

This module is a SEAM: nothing calls ``apply_diff_repair`` yet. T003 wires it
into ``run_builder_bridge_loop``, where the job, the approved intent and the
snapshot already live.

Public API::

    DIFF_REPAIR_MODE_DIFF — the mode of a repair round whose diff landed
    DIFF_REPAIR_MODE_FULL_FALLBACK — the mode of every round that did not
    DiffRepairApplyResult — the outcome as data, never as an exception
    apply_diff_repair(response, repo_path, *, job, intent_id,
                      data_dir=None, job_fences=None) -> DiffRepairApplyResult
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.diff_repair_response import (
    DiffRepairResponse,
    diff_repair_response_to_patch,
    precheck_diff_repair_fences,
    validate_diff_repair_response,
)
from packages.orchestration.source_apply import apply_structured_patch

# The mode a repair round reports when its unified diff actually landed — the
# only value that means the full-file round was skipped.
DIFF_REPAIR_MODE_DIFF = "diff"

# The mode every non-apply path reports: validation rejection, fence denial and
# apply failure all fall back to the full-file round, never to a partial write.
DIFF_REPAIR_MODE_FULL_FALLBACK = "full_fallback"


# One repair round's apply outcome as DATA: the mode the evidence records, plus
# the applicator's ids so a landed diff stays revertible.
@dataclass(frozen=True)
class DiffRepairApplyResult:
    """What a diff-only repair attempt did, and why it did not do more."""

    mode: str
    applied: bool
    fallback_reason: str
    apply_id: str
    snapshot_id: str
    files_modified: int
    errors: tuple[str, ...]
    # True only when the applicator reported that its own rollback failed, so
    # the tree is neither the pre-attempt state nor the patched one (R-0316).
    rollback_incomplete: bool = False


# The single entry point from a validated repair answer to the repository: it
# decides diff-versus-fallback and never leaves the tree half-written.
def apply_diff_repair(
    response: DiffRepairResponse,
    repo_path: Path,
    *,
    job: Any,
    intent_id: str,
    data_dir: str | Path | None = None,
    job_fences: dict | None = None,
) -> DiffRepairApplyResult:
    """Apply a diff-only repair answer, or report why the round falls back.

    Order is fixed: validate, fence-precheck, convert, apply. The first two
    steps touch no file, so a rejected answer costs no snapshot and no write.
    Every failure returns ``DIFF_REPAIR_MODE_FULL_FALLBACK`` with a
    ``fallback_reason`` prefixed ``validation:``, ``fence_denied:`` or
    ``apply_failed:`` — the caller reports the reason and reruns the round in
    full-file mode. Raises nothing of its own.
    """
    issues = validate_diff_repair_response(response)
    if issues:
        return DiffRepairApplyResult(
            mode=DIFF_REPAIR_MODE_FULL_FALLBACK,
            applied=False,
            fallback_reason="validation:" + "; ".join(issues[:3]),
            apply_id="",
            snapshot_id="",
            files_modified=0,
            errors=tuple(issues),
        )

    # Same derivation as source_apply.apply_structured_patch, so the precheck
    # below and the applicator's own enforce_change_set read one spec.
    effective_job_fences = job_fences
    if effective_job_fences is None:
        if hasattr(job, "fences") and job.fences is not None:
            effective_job_fences = {
                "allow": job.fences.allow,
                "deny": job.fences.deny,
            }

    precheck = precheck_diff_repair_fences(
        Path(repo_path), response, job_fences=effective_job_fences
    )
    if not precheck.allowed:
        return DiffRepairApplyResult(
            mode=DIFF_REPAIR_MODE_FULL_FALLBACK,
            applied=False,
            fallback_reason="fence_denied:" + ",".join(precheck.denied_paths),
            apply_id="",
            snapshot_id="",
            files_modified=0,
            errors=tuple(f"{path}: {reason}" for path, reason in precheck.reasons),
        )

    patch = diff_repair_response_to_patch(response)
    apply_result = apply_structured_patch(
        patch,
        Path(repo_path),
        data_dir=str(data_dir) if data_dir else None,
        job_id=getattr(job, "id", None),
        job=job,
        intent_id=intent_id,
    )

    if apply_result.success:
        return DiffRepairApplyResult(
            mode=DIFF_REPAIR_MODE_DIFF,
            applied=True,
            fallback_reason="",
            apply_id=apply_result.apply_id,
            snapshot_id=apply_result.snapshot_id,
            files_modified=apply_result.files_modified,
            errors=(),
        )

    # A failed apply normally rolled back from the durable snapshot inside
    # source_apply, so files_modified is 0 by fact and not by convention. When
    # the rollback ITSELF failed the applicator names it, and reporting 0 would
    # be a claim this seam cannot make (R-0316): the real count goes out instead.
    rollback_incomplete = any(
        "rollback_incomplete" in error for error in apply_result.errors
    )
    return DiffRepairApplyResult(
        mode=DIFF_REPAIR_MODE_FULL_FALLBACK,
        applied=False,
        fallback_reason="apply_failed:" + "; ".join(apply_result.errors[:3]),
        apply_id=apply_result.apply_id,
        snapshot_id=apply_result.snapshot_id,
        files_modified=apply_result.files_modified if rollback_incomplete else 0,
        errors=tuple(apply_result.errors),
        rollback_incomplete=rollback_incomplete,
    )
