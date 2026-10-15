"""What `job_apply` says and checks about a job that started from a dirty working tree (amend1014b).

Split out of `job_apply` because that file's size is a ratchet row that may not rise: the baseline
helpers live here, and so do two blocks of old `job_apply` that moved out to pay for them (the
mode-fidelity check and the cleanup-failed summary). `job_apply` names these functions through
its imports; nothing here writes the target.
"""
from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

#: The one token and reason prefix for a target that moved after the job captured its start state.
#: Nothing is applied and the target's bytes are never overwritten.
TARGET_CHANGED_DURING_RUN = "target_changed_during_run"


def target_changed_sentence(reason: str) -> str:
    """The sentence of a target-changed refusal, naming the changed paths (never a bare token)."""
    from packages.orchestration.job_apply import _named_paths

    paths: list[str] = []
    for entry in re.findall(r"'([^']+)'", reason):
        head, _sep, tail = entry.partition(": ")
        paths.append(tail if head.startswith(("target_", "workspace_", "missing_")) else head)
    named = _named_paths(sorted(set(paths))) if paths else "a reviewed file"
    return (f"{TARGET_CHANGED_DURING_RUN}: {named} changed in the target after the job captured "
            f"its start state, so nothing was applied and the target was not overwritten.")


def note_start_baseline(job: Any, result: Any, applied: list[str]) -> None:
    """Say which applied files carried the person's earlier edit, and which dirty paths were kept."""
    from packages.orchestration.dirty_baseline import job_start_baseline

    start = job_start_baseline(job)
    dirty = [e["path"] for e in start.get("entries", [])]
    kept = [e["path"] for e in start.get("preserved", [])]
    result.baseline_files_applied = sorted(set(applied) & set(dirty))
    result.preserved_dirty_paths = sorted((set(dirty) - set(applied)) | set(kept))


def baseline_drift_refusal(job: Any, target: Path) -> str:
    """A dirty-start job refuses when the target's HEAD or branch moved. "" when fine."""
    from packages.orchestration.dirty_baseline import baseline_drift, job_start_baseline

    start = job_start_baseline(job)
    moved = [m for m in baseline_drift(target, start) if m.startswith(("HEAD ", "the branch"))] if start else []
    return f"{TARGET_CHANGED_DURING_RUN}: {'; '.join(moved)}" if moved else ""


def history_baseline_refusals(job: Any) -> list[str]:
    """The history merge cannot carry a baseline: its branch holds a commit of the person's files."""
    from packages.orchestration.dirty_baseline import job_start_baseline

    if not job_start_baseline(job).get("commit"):
        return []
    return ["The job started from a dirty working tree, so its branch holds a baseline commit of "
            "your uncommitted files; a merge would commit them. Use --commit-auto, which commits "
            "only the reviewed files."]


def apply_base_commit(job: Any) -> str:
    """The commit result.diff is relative to: the baseline commit of a dirty start, else the target base."""
    from packages.orchestration.dirty_baseline import job_start_baseline

    return job_start_baseline(job).get("commit") or getattr(job, "worktree_base_commit", "")


def baseline_report_lines(result: Any) -> list[str]:
    """The disclosure an applied summary carries for a dirty start; [] for a clean one."""
    from packages.orchestration.job_apply import _named_paths

    lines: list[str] = []
    if result.baseline_files_applied:
        lines.append(
            f"{_named_paths(result.baseline_files_applied)} already held uncommitted edits when "
            f"the job started, so the file{' (and any commit of it)' if result.commit_sha else ''} "
            f"contains those edits as well as the reviewed change.")
    if result.preserved_dirty_paths:
        lines.append(f"Left uncommitted and byte-identical: {_named_paths(result.preserved_dirty_paths)}.")
    return lines


def mode_fidelity_blocks(
    mode_proofs: dict[str, Any], planned: list[str], workspace: Path, mode_of: Callable[[Path], str],
) -> list[str]:
    """The source must still carry the reviewed file mode; one sentence per file that does not."""
    blocks: list[str] = []
    for rel_path in planned:
        proof = mode_proofs.get(rel_path)
        expected = getattr(proof, "final_mode", "") if proof else ""
        if expected and mode_of(workspace / rel_path) != expected:
            blocks.append(f"{rel_path}: source mode {mode_of(workspace / rel_path)} != reviewed {expected}")
    return blocks


def cleanup_failed_lines(result: Any) -> list[str]:
    """Never let a reader infer the damage from a status string alone: say plainly whether the
    target was touched, which files, and what is left over."""
    lines = [""]
    if result.files_applied:
        lines += ["The target was changed.", f"Files applied: {result.files_applied}"]
    else:
        lines.append("The target was NOT changed"
                     + (" (dry-run only)." if result.dry_run or not result.approved else "."))
    lines += ["Temporary apply cleanup failed.", f"Cleanup error: {result.cleanup_error}"]
    if not result.temporary_registration_removed:
        lines.append("A temporary git worktree registration may remain (check `git worktree list`).")
    if not result.temporary_worktree_removed:
        lines.append("A temporary apply directory may remain on disk.")
    return lines + ["Manual cleanup is required."]


def blocked_path_names(files_blocked: list[str]) -> list[str]:
    """The bare paths out of ``files_blocked``, whose entries read ``path: reason``."""
    return [entry.split(":", 1)[0].strip() for entry in files_blocked]
