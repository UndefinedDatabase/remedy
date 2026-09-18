"""Job apply — apply reviewed job workspace changes into target repo.

Applying is a separate explicit human-approved action.
Never auto-applies. Requires --approve flag.
A plain apply copies files and makes no git commit and no push. The exceptions
are the operator's own flags, each needing --approve and each run under the
operator's identity, configuration and hooks: ``--commit-with-history``
(DECISION F270 D2) runs ``git merge --no-ff`` of the job branch onto the
operator's current branch instead of copying; ``--commit "<message>"`` and
``--commit-auto`` (DECISION F270 D3) copy, then land ONE commit of exactly the
copied files; ``--push`` then pushes what landed to the branch's configured
upstream, never forced. Never a git reset of a branch, a git checkout or a
forced push.

Public API:
    apply_job(job_id, target_repo, *, approve, dry_run, test_command,
              skip_blocked, commit_with_history, commit_message, commit_auto,
              push) -> JobApplyResult
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.exec_guard import run_guarded_test_command
from packages.orchestration.pingpong_evidence import (
    _redact_json_value,
    _redact_secrets,
    _sanitize_path,
)

_BLOCKED_PREFIXES = (
    ".git/", ".git\\",
    ".env", "node_modules/", "node_modules\\",
    "__pycache__/", "__pycache__\\",
    ".mypy_cache/", ".pytest_cache/", ".ruff_cache/",
    ".tox/", "dist/", "build/", ".eggs/",
    ".cache/", "htmlcov/",
)

_BLOCKED_EXACT = frozenset({
    ".git", ".env", ".gitignore",
})

_UNSAFE_EXTENSIONS = frozenset({
    ".pem", ".key", ".p12", ".pfx", ".jks",
})

_MAX_FILE_SIZE = 1_000_000
_TEST_OUTPUT_CAP = 10000


def _is_blocked_path(rel_path: str) -> str:
    """Return block reason or empty string if path is allowed."""
    norm = rel_path.replace("\\", "/")

    if ".." in norm.split("/"):
        return "path_traversal"

    if os.path.isabs(rel_path):
        return "absolute_path"

    if norm in _BLOCKED_EXACT or norm.rstrip("/") in _BLOCKED_EXACT:
        return f"blocked_path: {norm}"

    base = os.path.basename(norm)
    if base == ".env" or base.startswith(".env.") or base.startswith(".env-"):
        return "secret_file"

    for prefix in _BLOCKED_PREFIXES:
        p = prefix.replace("\\", "/")
        if norm.startswith(p) or norm == p.rstrip("/"):
            return f"blocked_path: {p.rstrip('/')}"

    suffix = os.path.splitext(norm)[1].lower()
    if suffix in _UNSAFE_EXTENSIONS:
        return "private_key_file"

    return ""


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()


def _validate_source_containment(
    workspace: Path,
    rel_path: str,
) -> str:
    """Validate that a workspace source file is safe to read.

    Returns empty string if safe, or reason string if blocked.
    Blocks symlinks, escapes, non-regular files.
    """
    ws_resolved = workspace.resolve()
    src = workspace / rel_path

    if src.is_symlink():
        return f"source_is_symlink: {rel_path}"

    try:
        src_resolved = src.resolve()
    except OSError:
        return f"source_resolve_failed: {rel_path}"

    if not str(src_resolved).startswith(str(ws_resolved) + os.sep) and src_resolved != ws_resolved:
        return f"source_escapes_workspace: {rel_path}"

    if not src_resolved.exists():
        return f"source_missing: {rel_path}"

    if not src_resolved.is_file():
        return f"source_not_regular_file: {rel_path}"

    current = src.parent
    while current != workspace and current != current.parent:
        if current.is_symlink():
            return f"parent_symlink_in_path: {rel_path}"
        current = current.parent

    return ""


def _validate_dest_containment(
    target: Path,
    rel_path: str,
) -> str:
    """Validate that a target destination path is safe to write.

    Returns empty string if safe, or reason string if blocked.
    Blocks ALL destination symlinks — even those resolving inside target.
    Writing through a symlink changes a different path than the planned one.
    """
    try:
        dest_resolved = (target / rel_path).resolve()
    except OSError:
        return f"dest_resolve_failed: {rel_path}"

    target_resolved = target.resolve()
    if not str(dest_resolved).startswith(str(target_resolved) + os.sep) and dest_resolved != target_resolved:
        return f"dest_escapes_target: {rel_path}"

    dest = target / rel_path
    if dest.is_symlink():
        return f"dest_is_symlink: {rel_path}"

    current = dest.parent
    while current != target and current != current.parent:
        if current.exists() and current.is_symlink():
            return f"dest_parent_symlink: {rel_path}"
        current = current.parent

    return ""


# ---------------------------------------------------------------------------
# Baseline readiness model
# ---------------------------------------------------------------------------

@dataclass
class FileReadiness:
    """Per-file baseline readiness status for applying."""
    path: str = ""
    kind: str = ""  # created | modified
    baseline_status: str = ""
    workspace_status: str = ""


def _consolidate_file_proofs(
    job: Any,
) -> dict[str, dict[str, Any]]:
    """Consolidate file proofs across all tasks: earliest baseline, latest final hash."""
    consolidated: dict[str, dict[str, Any]] = {}
    for t in job.tasks:
        if not t.apply_manifest:
            continue
        for proof in t.apply_manifest.applied_file_proofs:
            if proof.path not in consolidated:
                consolidated[proof.path] = {
                    "existed_before_job": proof.existed_before_job,
                    "baseline_sha256": proof.baseline_sha256,
                    "final_workspace_sha256": proof.final_workspace_sha256,
                    # The reviewed change includes the file mode, so drift detection
                    # must see it: an external chmod on an otherwise untouched
                    # target file would silently be reverted by applying.
                    "baseline_mode": proof.baseline_mode,
                    "final_mode": proof.final_mode,
                }
            else:
                consolidated[proof.path]["final_workspace_sha256"] = (
                    proof.final_workspace_sha256
                )
                consolidated[proof.path]["final_mode"] = proof.final_mode
    return consolidated


def _check_baseline_readiness(
    target: Path,
    workspace: Path,
    planned_files: list[str],
    proofs: dict[str, dict[str, Any]],
) -> tuple[bool, list[str], list[FileReadiness]]:
    """Baseline-aware readiness check.

    Returns (clean, block_reasons, file_readiness_list).
    """
    blocks: list[str] = []
    readiness: list[FileReadiness] = []

    for rel_path in planned_files:
        proof = proofs.get(rel_path)
        target_file = target / rel_path
        ws_file = workspace / rel_path

        if proof is None:
            if target_file.exists():
                blocks.append(f"missing_baseline_for_existing_file: {rel_path}")
                readiness.append(FileReadiness(
                    path=rel_path,
                    kind="modified",
                    baseline_status="missing_baseline_for_existing_file",
                    workspace_status="unknown",
                ))
            else:
                readiness.append(FileReadiness(
                    path=rel_path,
                    kind="created",
                    baseline_status="target_missing_as_expected",
                    workspace_status="unknown",
                ))
            continue

        existed = proof["existed_before_job"]
        baseline_hash = proof["baseline_sha256"]
        final_hash = proof["final_workspace_sha256"]

        ws_current_hash = _hash_file(ws_file)
        if ws_current_hash != final_hash:
            blocks.append(f"workspace_changed_since_review: {rel_path}")
            readiness.append(FileReadiness(
                path=rel_path,
                kind="modified" if existed else "created",
                baseline_status="unknown",
                workspace_status="workspace_changed_since_review",
            ))
            continue

        ws_status = "final_hash_matches"

        if existed:
            kind = "modified"
            if not target_file.exists():
                blocks.append(f"target_deleted_since_job: {rel_path}")
                readiness.append(FileReadiness(
                    path=rel_path, kind=kind,
                    baseline_status="target_deleted_since_job",
                    workspace_status=ws_status,
                ))
                continue
            current_target_hash = _hash_file(target_file)
            baseline_mode = proof.get("baseline_mode", "")
            current_mode = _mode_of(target_file)
            if current_target_hash != baseline_hash:
                blocks.append(f"target_changed_since_job: {rel_path}")
                b_status = "target_changed_since_job"
            elif baseline_mode and current_mode != baseline_mode:
                # Content still matches the baseline, but somebody chmod'ed the
                # target after the job ran. Applying would silently revert that.
                blocks.append(f"target_mode_changed_since_job: {rel_path}")
                b_status = "target_mode_changed_since_job"
            else:
                b_status = "target_matches_baseline"
        else:
            kind = "created"
            if target_file.exists():
                blocks.append(f"target_created_since_job: {rel_path}")
                b_status = "target_created_since_job"
            else:
                b_status = "target_missing_as_expected"

        readiness.append(FileReadiness(
            path=rel_path, kind=kind,
            baseline_status=b_status,
            workspace_status=ws_status,
        ))

    return len(blocks) == 0, blocks, readiness


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

@dataclass
class TaskApplySummary:
    """Per-task apply readiness summary."""
    task_id: str = ""
    title: str = ""
    status: str = ""
    run_id: str = ""
    reviewer_verdict: str = ""
    test_passed: bool | None = None
    repair_rounds_used: int = 0
    repair_rounds_allowed: int = 0
    applied_files: list[str] = field(default_factory=list)


@dataclass
class JobApplyResult:
    """Result of a job apply attempt."""
    job_id: str = ""
    job_apply_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: str = ""  # blocked, dry_run, approved_apply_started, applied, applied_test_failed, applied_push_failed, applied_record_update_failed
    approved: bool = False
    dry_run: bool = False
    target_repo: str = ""
    job_status: str = ""
    job_title: str = ""
    job_workspace_path: str = ""
    task_summaries: list[TaskApplySummary] = field(default_factory=list)
    files_planned: list[str] = field(default_factory=list)
    files_applied: list[str] = field(default_factory=list)
    files_blocked: list[str] = field(default_factory=list)
    files_skipped: list[str] = field(default_factory=list)
    #: True when the operator passed --skip-blocked, i.e. acknowledged the blocked
    #: set and asked for the remainder anyway. ``files_blocked`` still names every
    #: path that was withheld, so an apply that skipped is never silent.
    skip_blocked: bool = False
    file_readiness: list[FileReadiness] = field(default_factory=list)
    blocked_reason: str = ""
    blocked_reasons: list[str] = field(default_factory=list)
    target_guard_ok: bool = False
    target_clean: bool = False
    execution_config: dict[str, Any] = field(default_factory=dict)
    context_strategy: str = ""
    post_test_command: str = ""
    post_test_passed: bool | None = None
    post_test_summary: str = ""
    started_at: str = ""
    finished_at: str = ""
    # F006 fidelity + honest temp cleanup
    source_changed_files: list[str] = field(default_factory=list)
    reviewed_task_files: list[str] = field(default_factory=list)
    unexpected_source_files: list[str] = field(default_factory=list)
    missing_source_files: list[str] = field(default_factory=list)
    modes_applied: dict[str, str] = field(default_factory=dict)
    temporary_worktree_removed: bool = False
    temporary_registration_removed: bool = False
    cleanup_status: str = ""          # "" | "clean" | "failed"
    cleanup_error: str = ""
    # DECISION F270 D2 (6): the operator's --commit-with-history merge of the job branch.
    commit_with_history: bool = False
    merged_branch: str = ""           # remedy/job-<job id>
    target_branch: str = ""           # the operator's branch the merge landed on
    history_commits: list[str] = field(default_factory=list)
    merge_commit: str = ""
    merge_conflicts: list[str] = field(default_factory=list)
    #: The operator's tip before the merge; named in the undo sentence, not a record field.
    history_previous_head: str = ""
    # DECISION F270 D3 (6): --commit "<message>", --commit-auto and --push.
    commit_message_mode: str = ""     # "" | "message" | "auto" | "history"
    #: The operator's --commit line; it is in the commit itself, not a record field.
    commit_message: str = ""
    commit_sha: str = ""              # the commit (or merge commit) that landed
    push: bool = False                # --push was given
    pushed: bool = False
    push_remote: str = ""             # the remote's name, never its URL
    push_ref: str = ""                # the upstream ref pushed to
    push_error: str = ""


# ---------------------------------------------------------------------------
# DECISION F270 D2: --commit-with-history merges the job branch
# ---------------------------------------------------------------------------

#: The reason prefix of every --commit-with-history refusal; the rest is ONE sentence.
HISTORY_REFUSED = "history_merge_refused"

#: Wall-clock ceiling of one git command of the history merge.
HISTORY_GIT_TIMEOUT_SEC = 120

#: How many dirty paths a refusal names before saying how many more there are.
HISTORY_PATHS_NAMED = 10


def _history_git(target: Path, *args: str,
                 env: dict[str, str] | None = None) -> tuple[int, str, str]:
    """One git call in the target for the merge, the commit or the push; never raises.

    Returns ``(returncode, stdout, stderr)``, the returncode being -1 when git
    could not finish (a timeout, a missing binary). ``env``, when given,
    replaces the environment and closes stdin, so git can prompt no one.
    """
    extra: dict[str, Any] = {"env": env, "stdin": subprocess.DEVNULL} if env is not None else {}
    try:
        proc = subprocess.run(
            ["git", *args], cwd=str(target), capture_output=True, text=True,
            timeout=HISTORY_GIT_TIMEOUT_SEC, **extra,
        )
    except subprocess.TimeoutExpired:
        return -1, "", f"git {args[0]} timed out after {HISTORY_GIT_TIMEOUT_SEC}s"
    except OSError as exc:
        return -1, "", f"git {args[0]} could not run: {type(exc).__name__}: {exc}"
    return proc.returncode, proc.stdout, proc.stderr


def _named_paths(paths: list[str]) -> str:
    named = ", ".join(paths[:HISTORY_PATHS_NAMED])
    if len(paths) > HISTORY_PATHS_NAMED:
        named += f" and {len(paths) - HISTORY_PATHS_NAMED} more"
    return named


def _job_branch_refusal(job: Any, target: Path) -> str:
    """The sentence refusing a job branch that is not the reviewed work, or "".

    DECISION F270 D2 (2): the branch must exist, its tip must be the job's
    ``worktree_head``, and the diff from ``job_initial_tree`` to the tip's tree
    must hash to ``result_diff_sha256``. The diff is read in text mode and
    re-encoded exactly as ``worktrees.write_tree_diff`` wrote ``result.diff``.
    """
    branch = getattr(job, "worktree_branch", "") or ""
    rc, out, _err = (_history_git(target, "rev-parse", "-q", "--verify",
                                  f"refs/heads/{branch}^{{commit}}")
                     if branch else (1, "", ""))
    if rc != 0:
        return (f"The job branch {branch or '(none recorded)'} does not exist in "
                f"the target, so there are no task commits to merge.")
    tip = out.strip()
    head = getattr(job, "worktree_head", "") or ""
    if tip != head:
        return (f"The job branch {branch} points at {tip[:12]}, not at the job's "
                f"recorded head {head[:12] or '(none)'}, so it is not the reviewed work.")
    initial = getattr(job, "job_initial_tree", "") or ""
    rc, text, _err = (_history_git(target, "diff", "--no-color", "--no-ext-diff",
                                   "--src-prefix=a/", "--dst-prefix=b/",
                                   initial, f"{tip}^{{tree}}")
                      if initial else (1, "", ""))
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest() if rc == 0 else ""
    if not digest or digest != getattr(job, "result_diff_sha256", ""):
        return (f"The tip of {branch} does not hold the changes of the job's reviewed "
                f"result.diff, so it is not the reviewed work.")
    return ""


#: The operator's own unfinished operations, besides a merge, that git marks by a ref.
_OPERATION_HEADS = (("CHERRY_PICK_HEAD", "a cherry-pick"), ("REVERT_HEAD", "a revert"))

#: The directories git keeps while a rebase (or ``git am``) is unfinished.
_REBASE_DIRS = ("rebase-merge", "rebase-apply")


def _checkout_refusals(target: Path, *, landing: str, what: str) -> tuple[list[str], bool]:
    """The operator checkout's refusals every ``--commit…`` flag shares; ``(sentences, stop)``.

    DECISION F270 D2 (2) and D3 (2): a target below its repository's top
    level, a detached HEAD, the operator's own merge, rebase, cherry-pick or
    revert in progress, and a dirty tree. ``landing`` says what lands ("the
    task commits"), ``what`` the act ("merge into"). Reads only. ``stop`` is
    True when the target is not a repository's top level, because nothing
    after that can be asked.
    """
    rc, top, _err = _history_git(target, "rev-parse", "--show-toplevel")
    if rc != 0 or Path(top.strip()).resolve() != target.resolve():
        return [f"{target} is not the top level of a git repository, so there is no "
                f"branch to {what}; a plain --approve copies the files."], True
    refusals: list[str] = []
    if _history_git(target, "symbolic-ref", "-q", "HEAD")[0] != 0:
        refusals.append(f"The target is on a detached HEAD; check out the branch "
                        f"{landing} should land on and re-run.")
    if _history_git(target, "rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0:
        # Remedy's abort must only ever abort Remedy's own merge.
        refusals.append("The target is in the middle of a merge of its own; finish or "
                        "abort it and re-run.")
    for head, operation in _OPERATION_HEADS:
        if _history_git(target, "rev-parse", "-q", "--verify", head)[0] == 0:
            refusals.append(f"The target is in the middle of {operation} of its own; "
                            f"finish or abort it and re-run.")
    for name in _REBASE_DIRS:
        rc, path, _err = _history_git(target, "rev-parse", "--git-path", name)
        if rc == 0 and path.strip() and (target / path.strip()).exists():
            refusals.append("The target is in the middle of a rebase of its own; finish "
                            "or abort it and re-run.")
            break
    rc, out, err = _history_git(target, "status", "--porcelain", "--untracked-files=all")
    dirty = [line[3:] for line in out.splitlines() if line.strip()]
    if rc != 0:
        refusals.append(f"git status failed in the target ({err.strip()[:150]}), so "
                        f"its tree cannot be shown clean.")
    elif dirty:
        refusals.append(f"The target has uncommitted changes in {_named_paths(dirty)}; "
                        f"commit or stash them and re-run.")
    return refusals, False


def _history_refusals(
    job: Any, target: Path, *, skip_blocked: bool, skipped: list[str],
) -> list[str]:
    """Every sentence refusing --commit-with-history here; empty when the merge may run.

    DECISION F270 D2 (2). Reads the target and the job branch only and writes
    nothing. A staging job and a target that is not a repository's top level
    end the list at once, because nothing after them can be asked.
    """
    if getattr(job, "isolation_mode", "copy") != "worktree":
        return [f"Job {job.job_id} ran in a staging copy, not on a git branch, so it "
                f"has no task commits to merge and nothing was copied; a plain "
                f"--approve copies its files."]
    refusals, stop = _checkout_refusals(target, landing="the task commits",
                                        what="merge into")
    if stop:
        return refusals
    if skip_blocked:
        refusals.append("--commit-with-history merges the whole job branch and cannot "
                        "leave protected paths out, so it does not combine with "
                        "--skip-blocked.")
    if skipped:
        refusals.append(f"The copy would skip {_named_paths(skipped)}, and a merge "
                        f"cannot leave a file out; a plain --approve copies the rest.")
    branch_refusal = _job_branch_refusal(job, target)
    if branch_refusal:
        refusals.append(branch_refusal)
    return refusals


def build_history_merge_message(job: Any, commit_count: int, target_branch: str) -> str:
    """The merge commit's message (DECISION F270 D2 (3)).

    A first line of at most 72 characters, one body sentence naming both
    branches, the contract line of DECISION F270 D1 (3), then the
    ``Remedy-Job`` and ``Co-authored-by`` trailers.
    """
    from packages.orchestration import worktrees as W
    from packages.orchestration.pingpong_job import _task_commit_contract_line

    noun = "task commit" if commit_count == 1 else "task commits"
    subject = f"Merge the {commit_count} {noun} of Remedy job {str(job.job_id)[:8]}"
    body = (f"This merges {job.worktree_branch}, the reviewed work of Remedy job "
            f"{job.job_id}, onto {target_branch} with one commit per applied task.")
    return (f"{subject}\n\n{body}\n\n{_task_commit_contract_line(job)}\n\n"
            f"{W.REMEDY_JOB_TRAILER}: {job.job_id}\n"
            f"Co-authored-by: {W.REMEDY_COMMIT_NAME} <{W.REMEDY_COMMIT_EMAIL}>\n")


def _quoted_git_output(stdout: str, stderr: str) -> str:
    """Git's (and a refusing hook's) own words on one line, without git's merge advice."""
    lines = [ln.strip() for ln in (stderr + "\n" + stdout).splitlines()]
    kept = [ln for ln in lines if ln and not ln.startswith("Not committing merge")]
    return " ".join(kept)[:300] or "no output"


def _merge_job_branch(job: Any, result: JobApplyResult, target: Path) -> str:
    """``git merge --no-ff --no-log`` of the job branch as the operator; "" or ONE sentence.

    DECISION F270 D2 (3) and (4). The operator's environment, identity,
    configuration and hooks are used unchanged. The verified tip sha is merged,
    so a branch moved after the check cannot slip in. A failed merge is
    aborted with ``git merge --abort`` and HEAD, the status and ``MERGE_HEAD``
    are proved back where they were; Remedy never runs ``git reset``.
    """
    branch = job.worktree_branch
    rc, before, err = _history_git(target, "rev-parse", "HEAD")
    before = before.strip()
    if rc != 0 or not before:
        return f"The target's HEAD could not be read ({err.strip()[:150]}), so nothing was merged."
    result.history_previous_head = before
    result.merged_branch = branch
    result.target_branch = _history_git(target, "symbolic-ref", "-q", "--short", "HEAD")[1].strip()
    rc, out, err = _history_git(target, "rev-list", "--reverse",
                                f"{job.worktree_base_commit}..{job.worktree_head}")
    if rc != 0:
        return f"The task commits of {branch} could not be listed ({err.strip()[:150]}), so nothing was merged."
    result.history_commits = out.split()
    message = build_history_merge_message(job, len(result.history_commits), result.target_branch)
    rc, out, err = _history_git(target, "merge", "--no-ff", "--no-log", "--no-edit",
                                "-m", message, job.worktree_head)
    if rc == 0:
        merged = _history_git(target, "rev-parse", "HEAD", "HEAD^1", "HEAD^2")[1].split()
        result.merge_commit = merged[0] if merged else ""
        if merged[1:] != [before, job.worktree_head]:
            return (f"git merge reported success but HEAD {result.merge_commit[:12]} is "
                    f"not a merge of {before[:12]} and {job.worktree_head[:12]}.")
        return ""
    unmerged = _history_git(target, "diff", "--name-only", "--diff-filter=U")[1]
    result.merge_conflicts = [p for p in unmerged.splitlines() if p.strip()]
    if _history_git(target, "rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0:
        _history_git(target, "merge", "--abort")
    after = _history_git(target, "rev-parse", "HEAD")[1].strip()
    status = _history_git(target, "status", "--porcelain", "--untracked-files=all")[1]
    in_merge = _history_git(target, "rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0
    if after != before or status.strip() or in_merge:
        return (f"git merge of {branch} failed and the target could not be restored "
                f"(HEAD {after[:12]}, status {status.strip()[:120]!r}); Remedy resets "
                f"nothing, so inspect it by hand.")
    if result.merge_conflicts:
        return (f"Merging {branch} conflicts in {_named_paths(result.merge_conflicts)}, "
                f"so the merge was aborted and your files are exactly as they were.")
    return (f"git merge of {branch} was refused (\"{_quoted_git_output(out, err)}\"), "
            f"so the merge was aborted and nothing changed.")


def _merge_undo_sentence(result: JobApplyResult) -> str:
    """DECISION F270 D2 (5): what landed, and the one command that undoes it."""
    prev = result.history_previous_head
    return (f"The merge commit {result.merge_commit} is on {result.target_branch}, "
            f"whose previous tip was {prev}; nothing was pushed, Remedy undoes nothing "
            f"itself, and `git reset --keep {prev}` undoes the merge.")


def _note_merge_undo(result: JobApplyResult) -> None:
    """After a merge, put the undo sentence in the record of a failed verification or post-test."""
    if result.merge_commit:
        result.blocked_reasons.append(_merge_undo_sentence(result))


# ---------------------------------------------------------------------------
# DECISION F270 D3: --commit "<message>", --commit-auto and --push
# ---------------------------------------------------------------------------

#: The reason prefix of every --commit / --commit-auto refusal and of a flag clash.
COMMIT_REFUSED = "commit_refused"

#: The reason prefix of every --push refusal.
PUSH_REFUSED = "push_refused"

#: The verbs a --commit-auto first line may start with (DECISION F270 D3 (4)).
COMMIT_AUTO_VERBS = (
    "Add", "Apply", "Build", "Change", "Clean", "Create", "Document", "Extend",
    "Fix", "Implement", "Improve", "Make", "Merge", "Move", "Refactor", "Remove",
    "Rename", "Replace", "Support", "Test", "Update", "Use", "Write",
)

#: The fewest words a --commit-auto first line may have.
COMMIT_AUTO_MIN_WORDS = 3

#: The flag each commit mode is spelled as on the command line.
COMMIT_MODE_FLAGS = {"message": "--commit", "auto": "--commit-auto",
                     "history": "--commit-with-history"}


def commit_flags_refusal(commit_message: str | None, commit_auto: bool,
                         commit_with_history: bool, push: bool) -> tuple[str, str]:
    """``(mode, refusal)`` for the ``--commit…`` flags and ``--push``, read before the job.

    DECISION F270 D3 (1): the three ``--commit…`` flags are mutually
    exclusive, ``--push`` needs one of them, and a ``--commit`` message must be
    one non-empty line. ``mode`` is ``""``, ``message``, ``auto`` or
    ``history``; ``refusal`` is ``""`` or the prefixed reason of ONE sentence.
    """
    given = [mode for mode, on in (("message", commit_message is not None),
                                   ("auto", commit_auto),
                                   ("history", commit_with_history)) if on]
    if len(given) > 1:
        flags = " and ".join(COMMIT_MODE_FLAGS[m] for m in given)
        return "", (f"{COMMIT_REFUSED}: {flags} each decide how the applied work is "
                    f"committed, so only one of them may be given and nothing was applied.")
    mode = given[0] if given else ""
    if push and not mode:
        return "", (f"{PUSH_REFUSED}: --push pushes what --commit, --commit-auto or "
                    f"--commit-with-history lands, so it is refused alone and nothing "
                    f"was applied.")
    if mode == "message":
        line = (commit_message or "").strip()
        if not line:
            return mode, (f"{COMMIT_REFUSED}: --commit needs the first line of the commit "
                          f"message and the one given is empty, so nothing was applied.")
        if "\n" in line or "\r" in line:
            return mode, (f"{COMMIT_REFUSED}: --commit takes one line, the commit's first "
                          f"line, because Remedy writes the body, the contract line and the "
                          f"trailers, so nothing was applied.")
    return mode, ""


def commit_subject_problem(line: str) -> str:
    """``""`` when ``line`` passes the --commit-auto rule, else why it does not.

    DECISION F270 D3 (4): one line of at most 72 characters, at least three
    words, the first one of :data:`COMMIT_AUTO_VERBS` — so neither an id alone
    (``T002``) nor a label without a verb passes.
    """
    from packages.orchestration.pingpong_job import TASK_COMMIT_SUBJECT_MAX

    if not line.strip() or "\n" in line or "\r" in line:
        return "it is not one line"
    if len(line) > TASK_COMMIT_SUBJECT_MAX:
        return f"it is {len(line)} characters long, over {TASK_COMMIT_SUBJECT_MAX}"
    words = line.split()
    if words[0] not in COMMIT_AUTO_VERBS:
        return f"its first word {words[0]!r} is not one of the verbs {', '.join(COMMIT_AUTO_VERBS)}"
    if len(words) < COMMIT_AUTO_MIN_WORDS:
        return f"it has {len(words)} words, fewer than {COMMIT_AUTO_MIN_WORDS}"
    return ""


def _mission_goal(job: Any) -> str:
    """The goal of the job's mission, whitespace-collapsed, or ``""``."""
    from packages.orchestration.mission_state import mission_for_job

    try:
        mission = mission_for_job(str(job.job_id))
    except Exception:
        return ""
    return " ".join(str(getattr(mission, "goal", "") or "").split()) if mission else ""


def build_auto_commit_subject(job: Any) -> str:
    """The --commit-auto first line (DECISION F270 D3 (4)).

    The mission's goal, else the job's title, else ``Apply the <n> tasks of
    Remedy job <id8>``: the first candidate that, with its first letter
    capitalised and cut by the per-task commits' own fitter, passes
    :func:`commit_subject_problem`.
    """
    from packages.orchestration.pingpong_job import fit_commit_subject

    for candidate in (_mission_goal(job), " ".join((job.job_title or "").split())):
        if candidate:
            subject = fit_commit_subject("", candidate[:1].upper() + candidate[1:])
            if not commit_subject_problem(subject):
                return subject
    n = len(job.tasks)
    return f"Apply the {n} {'task' if n == 1 else 'tasks'} of Remedy job {str(job.job_id)[:8]}"


def build_apply_commit_message(job: Any, subject: str, files: list[str], *,
                               list_tasks: bool) -> str:
    """The message of a --commit or --commit-auto commit (DECISION F270 D3 (4)).

    The first line; one body sentence naming the job; with ``list_tasks``
    (``--commit-auto``) the task titles; the contract line of DECISION F270
    D1 (3) as the last body line; the ``Remedy-Job`` and ``Co-authored-by``
    trailers.
    """
    from packages.orchestration import worktrees as W
    from packages.orchestration.pingpong_job import _task_commit_contract_line

    n = len(files)
    body = (f"This commits the {n} {'file' if n == 1 else 'files'} that Remedy job "
            f"{job.job_id} changed, as reviewed and applied.")
    titles = "\n".join(f"- {' '.join((t.title or 'untitled task').split())}"
                       for t in job.tasks)
    tasks = f"\n\n{titles}" if list_tasks and titles else ""
    return (f"{subject}\n\n{body}{tasks}\n\n{_task_commit_contract_line(job)}\n\n"
            f"{W.REMEDY_JOB_TRAILER}: {job.job_id}\n"
            f"Co-authored-by: {W.REMEDY_COMMIT_NAME} <{W.REMEDY_COMMIT_EMAIL}>\n")


def _commit_refusals(target: Path, planned: list[str]) -> list[str]:
    """Every sentence refusing --commit / --commit-auto here; reads only.

    DECISION F270 D3 (2): the shared checkout refusals, then a copied path the
    target's ``.gitignore`` matches. A staging job is not refused: the commit
    holds only the copied files.
    """
    refusals, stop = _checkout_refusals(target, landing="the commit", what="commit on")
    if stop or not planned:
        return refusals
    rc, out, err = _history_git(target, "check-ignore", "--", *planned)
    if rc == 0:
        ignored = [p for p in out.splitlines() if p.strip()]
        refusals.append(f"The target's .gitignore matches {_named_paths(ignored)}, so a "
                        f"commit cannot hold it; a plain --approve copies it.")
    elif rc != 1:
        refusals.append(f"git check-ignore failed in the target ({err.strip()[:150]}), so "
                        f"the copied paths cannot be shown committable.")
    return refusals


def _branch_upstream(target: Path) -> tuple[str, str, str]:
    """``(branch, remote, merge ref)`` of the target's current branch; ``""`` where git has none."""
    branch = _history_git(target, "symbolic-ref", "-q", "--short", "HEAD")[1].strip()
    if not branch:
        return "", "", ""
    remote = _history_git(target, "config", "--get", f"branch.{branch}.remote")[1].strip()
    merge = _history_git(target, "config", "--get", f"branch.{branch}.merge")[1].strip()
    return branch, remote, merge


def _push_refusals(job: Any, target: Path) -> list[str]:
    """Every sentence refusing --push here; reads only (DECISION F270 D3 (5)).

    No upstream, an upstream that is a local branch, a mission contract that
    cannot be read, and any blocking criterion of the job's whole mission that
    is not ``met`` — an ``open`` criterion is not green.
    """
    from packages.orchestration.mission_contract import (
        contract_blockers,
        read_mission_contract,
    )
    from packages.orchestration.mission_state import mission_for_job

    refusals: list[str] = []
    branch, remote, merge = _branch_upstream(target)
    if branch and (not remote or not merge):
        remotes = _history_git(target, "remote")[1].split()
        name = (remotes[0] if len(remotes) == 1
                else "origin" if "origin" in remotes else "<remote>")
        refusals.append(f"The branch {branch} has no upstream to push to; "
                        f"`git push --set-upstream {name} {branch}` sets one.")
    elif branch and remote == ".":
        refusals.append(f"The upstream of {branch} is the local branch {merge}, and "
                        f"--push never writes another branch of this repository.")
    try:
        mission = mission_for_job(str(job.job_id))
        blockers = contract_blockers(read_mission_contract(mission) if mission else None)
    except Exception as exc:
        return refusals + [f"The mission's contract cannot be read "
                           f"({type(exc).__name__}: {str(exc)[:120]}), so no push can be "
                           f"shown safe."]
    if blockers:
        refusals.append(f"The mission's blocking contract criteria {', '.join(blockers)} "
                        f"are not met, so nothing is pushed.")
    return refusals


def _flag_refusals(job: Any, result: JobApplyResult, target: Path, planned: list[str],
                   *, skip_blocked: bool, skipped: list[str]) -> list[str]:
    """Every prefixed refusal of the operator's ``--commit…`` and ``--push`` flags; reads only.

    DECISION F270 D2 (2) and D3 (2), (5): checked after every existing gate
    and again right before anything is written.
    """
    mode = result.commit_message_mode
    if mode == "history":
        found = [f"{HISTORY_REFUSED}: {s}" for s in _history_refusals(
            job, target, skip_blocked=skip_blocked, skipped=skipped)]
    elif mode in ("message", "auto"):
        found = [f"{COMMIT_REFUSED}: {s}" for s in _commit_refusals(target, planned)]
    else:
        return []
    if result.push:
        found += [f"{PUSH_REFUSED}: {s}" for s in _push_refusals(job, target)]
    return found


def _commit_applied_files(job: Any, result: JobApplyResult, target: Path,
                          applied: list[str]) -> str:
    """ONE commit of exactly ``applied`` on the operator's branch, as the operator; "" or ONE sentence.

    DECISION F270 D3 (3). ``git add`` then ``git commit --only`` of those
    paths under the operator's identity, configuration and hooks. A commit
    that fails takes the paths back out of the index and leaves the copied
    files in the tree; Remedy never moves the branch. A commit that landed
    must have the previous tip as its parent and touch no other path.
    """
    rc, before, err = _history_git(target, "rev-parse", "HEAD")
    before = before.strip()
    if rc != 0 or not before:
        return f"The target's HEAD could not be read ({err.strip()[:150]}), so nothing was committed."
    result.history_previous_head = before
    result.target_branch = _history_git(target, "symbolic-ref", "-q", "--short", "HEAD")[1].strip()
    subject = (build_auto_commit_subject(job) if result.commit_message_mode == "auto"
               else result.commit_message.strip())
    message = build_apply_commit_message(job, subject, applied,
                                         list_tasks=result.commit_message_mode == "auto")
    rc, out, err = _history_git(target, "add", "--", *applied)
    if rc == 0:
        rc, out, err = _history_git(target, "commit", "-q", "--only", "-m", message,
                                    "--", *applied)
    if rc != 0:
        _history_git(target, "restore", "--staged", "--", *applied)
        return (f"git commit of the {len(applied)} copied file(s) was refused "
                f"(\"{_quoted_git_output(out, err)}\"), so they are copied and not committed.")
    heads = _history_git(target, "rev-parse", "HEAD", "HEAD^")[1].split()
    result.commit_sha = heads[0] if heads else ""
    touched = _history_git(target, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z",
                           result.commit_sha)[1].split("\0")
    stray = sorted({p for p in touched if p} - set(applied))
    if heads[1:] != [before]:
        return (f"git commit reported success but HEAD {result.commit_sha[:12]} is not one "
                f"commit on the previous tip {before[:12]}.")
    if stray:
        return (f"git commit reported success but {result.commit_sha[:12]} also touches "
                f"{_named_paths(stray)}, which Remedy did not copy.")
    return ""


def _commit_undo_sentence(result: JobApplyResult) -> str:
    """What a --commit / --commit-auto commit left, and the one command that undoes it."""
    prev = result.history_previous_head
    return (f"The commit {result.commit_sha} is on {result.target_branch}, whose "
            f"previous tip was {prev}; nothing was pushed, Remedy undoes nothing itself, "
            f"and `git reset --keep {prev}` undoes the commit.")


def _push_landed_commit(result: JobApplyResult, target: Path) -> None:
    """``git push --porcelain <remote> <landed sha>:<upstream ref>``; never forced; records the outcome.

    DECISION F270 D3 (5). Only to the branch's configured upstream, with no
    credential prompt and a timeout. A failure is recorded, never raised: the
    commit stays where it landed.
    """
    branch, remote, merge = _branch_upstream(target)
    named = remote in _history_git(target, "remote")[1].split()
    result.push_remote = remote if named else ("(not a named remote)" if remote else "")
    result.push_ref = merge
    if branch != result.target_branch or not named or not merge or not result.commit_sha:
        result.push_error = (f"the branch or its upstream changed after the commit "
                             f"({branch or 'detached HEAD'}, upstream "
                             f"{result.push_remote or 'none'} {merge or 'none'}), so "
                             f"nothing was pushed")
        return
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    rc, out, err = _history_git(target, "push", "--porcelain", remote,
                                f"{result.commit_sha}:{merge}", env=env)
    if rc == 0:
        result.pushed = True
    else:
        result.push_error = _quoted_git_output(out, err)


# ---------------------------------------------------------------------------
# Apply logic
# ---------------------------------------------------------------------------

def _block(
    result: JobApplyResult,
    reason: str,
    *,
    persist: bool = True,
) -> JobApplyResult:
    result.status = "blocked"
    result.blocked_reason = reason
    result.blocked_reasons.append(reason)
    result.finished_at = datetime.now(timezone.utc).isoformat()
    return result


def _safe_persist(
    job_id: str,
    result: JobApplyResult,
    applied: list[str],
    *,
    final: bool = False,
) -> None:
    """Persist job apply record, structuring any failure after target mutation.

    ``final=True`` is the one post-cleanup write: a failure there is reported
    honestly rather than pretending a durable record (or a durable preview) exists.
    """
    try:
        _persist_job_apply_record(job_id, result)
    except OSError as exc:
        if final and not applied:
            original_status = result.status
            result.status = "record_update_failed"
            result.blocked_reason = (
                f"job_apply_record_update_failed: {exc} — "
                f"original_status={original_status}; no durable record exists"
            )
            result.blocked_reasons.append(result.blocked_reason)
            result.finished_at = datetime.now(timezone.utc).isoformat()
            return
        if applied:
            original_status = result.status
            original_reason = result.blocked_reason
            result.status = "applied_record_update_failed"
            result.blocked_reason = (
                f"job_apply_record_update_failed: {exc} — "
                f"original_status={original_status}, "
                f"original_reason={original_reason}, "
                f"target files may have changed ({len(applied)} applied)"
            )
            result.finished_at = datetime.now(timezone.utc).isoformat()


def _run_post_test(
    command: str,
    target: Path,
    *,
    timeout_sec: int = 120,
) -> tuple[bool, str]:
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return False, f"Invalid test command: {exc}"
    try:
        # Guarded since F085 T002b: rlimits, an env allowlist, a pinned cwd and the
        # guard's own wall deadline replace the bare spawn. The observable outcome is
        # unchanged — same returncode, same TimeoutExpired, same FileNotFoundError —
        # except that the guard hands back BYTES, which the decode below turns into
        # the str this function has always returned.
        proc = run_guarded_test_command(
            argv,
            timeout_sec=timeout_sec,
            cwd=str(target),
        )
    except FileNotFoundError:
        return False, f"Test command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return False, f"Test command timed out after {timeout_sec}s"

    output = (proc.stdout or b"").decode("utf-8", "replace") + (proc.stderr or b"").decode("utf-8", "replace")
    if len(output) > _TEST_OUTPUT_CAP:
        output = output[:_TEST_OUTPUT_CAP] + "\n[OUTPUT TRUNCATED]"
    passed = proc.returncode == 0
    summary = f"exit={proc.returncode}"
    if output.strip():
        last_lines = output.strip().splitlines()[-5:]
        summary += " | " + " ".join(last_lines)
    return passed, summary


# ---------------------------------------------------------------------------
# F006: materialize an apply source from the verified JobPlan hand-off
# ---------------------------------------------------------------------------

@dataclass
class ApplySource:
    """A temporary, read-only materialization of a completed job's hand-off."""

    path: Path
    repo: Path
    temp_root: Path
    materialized: bool = False


def _materialize_apply_source(job: Any) -> tuple[ApplySource | None, str]:
    """Deprecated shim kept for callers/tests that only want (source, error).

    The lifecycle owner is :func:`_materialize_apply_source_owned`, which never
    cleans up behind the caller's back: a temporary worktree that could not be
    removed must reach the caller, not vanish into a discarded return value.
    """
    source, err = _materialize_apply_source_owned(job)
    if source is not None and err:
        # A partially materialized source with an error: the OWNER cleans it up.
        return None, err
    return source, err


def _materialize_apply_source_owned(job: Any) -> tuple[ApplySource | None, str]:
    """Rebuild the completed job's result from base commit + verified result.diff.

    The execution worktree is deliberately disposable: after a clean cleanup the
    authoritative hand-off is the recorded base commit plus the job directory's
    ``result.diff`` (hash- and size-verified). This creates a TEMPORARY DETACHED
    git worktree at the recorded base commit, ``git apply --check``s the diff and
    then applies it. The original execution worktree is never recreated at its
    recorded path, no branch is merged, nothing is committed and nothing is pushed.
    """
    import subprocess
    import tempfile

    from packages.orchestration.job_evidence import job_result_diff_source

    src, err = job_result_diff_source(job)
    if src is None:
        return None, f"job_result_diff_invalid: {err}"

    repo = Path(job.repo_path)
    base = getattr(job, "worktree_base_commit", "")
    if not base:
        return None, "job_result_diff_invalid: no recorded base commit"

    from packages.orchestration import worktrees as W
    if not W.is_git_repo(repo):
        return None, f"target_not_git_repository: {repo}"
    if not W.commit_exists(repo, base):
        return None, f"base_commit_missing: {base[:12]}"

    temp_root = Path(tempfile.mkdtemp(prefix="remedy-job-apply-"))
    ws = temp_root / "source"
    source = ApplySource(path=ws, repo=repo, temp_root=temp_root)

    # From here on a temporary directory (and possibly a registered worktree) may
    # exist, so the SOURCE is always returned — even on failure — and the caller
    # owns the checked cleanup. Nothing is cleaned up and discarded here.
    try:
        proc = subprocess.run(
            ["git", "worktree", "add", "--detach", str(ws), base],
            cwd=str(repo), capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            return source, f"apply_worktree_failed: {proc.stderr.strip()[:200]}"
        source.materialized = True

        diff_arg = str(src)
        check = subprocess.run(
            ["git", "apply", "--check", diff_arg], cwd=str(ws),
            capture_output=True, text=True, timeout=120,
        )
        if check.returncode != 0:
            return source, f"job_diff_not_applicable: {check.stderr.strip()[:200]}"

        applied = subprocess.run(
            ["git", "apply", diff_arg], cwd=str(ws),
            capture_output=True, text=True, timeout=120,
        )
        if applied.returncode != 0:
            return source, f"job_diff_apply_failed: {applied.stderr.strip()[:200]}"
    except Exception as exc:
        return source, f"apply_materialization_error: {type(exc).__name__}: {exc}"

    return source, ""


def _run_cleanup_git(argv: list[str], *, cwd: str, timeout: int) -> tuple[bool, str]:
    """Run one cleanup git command. NEVER raises: returns (ok, error_text).

    A cleanup step that explodes (timeout, missing git, any OS error) must not
    abort the rest of the cleanup or replace the apply outcome — it must be
    recorded and the remaining steps must still run.
    """
    try:
        proc = subprocess.run(
            argv, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"{' '.join(argv[:3])} timed out after {timeout}s"
    except FileNotFoundError as exc:
        return False, f"{' '.join(argv[:3])} could not run: FileNotFoundError: {exc}"
    except OSError as exc:
        return False, f"{' '.join(argv[:3])} failed: {type(exc).__name__}: {exc}"
    except Exception as exc:                      # last resort: still no raise
        return False, f"{' '.join(argv[:3])} failed: {type(exc).__name__}: {exc}"
    if proc.returncode != 0:
        return False, f"{' '.join(argv[:3])} failed: {proc.stderr.strip()[:150]}"
    return True, ""


def _failed_cleanup(error: str) -> dict[str, Any]:
    """A cleanup result for the case where cleanup itself could not be completed."""
    return {
        "temporary_worktree_removed": False,
        "temporary_registration_removed": False,
        "cleanup_status": "failed",
        "cleanup_error": error,
    }


def _cleanup_apply_source(source: ApplySource | None) -> dict[str, Any]:
    """Remove the temporary apply worktree — and SAY what actually happened.

    TOTAL function: it never raises. Every step (remove, prune, physical delete,
    inventory, path check) is guarded independently, each failure is recorded, and
    the remaining steps still run — a cleanup exception must never escape and take
    the apply result, the applied-file list and the durable record with it.
    """
    out: dict[str, Any] = {
        "temporary_worktree_removed": False,
        "temporary_registration_removed": False,
        "cleanup_status": "clean",
        "cleanup_error": "",
    }
    if source is None:
        return out

    import shutil

    errors: list[str] = []
    try:
        if source.materialized:
            ok, err = _run_cleanup_git(
                ["git", "worktree", "remove", "--force", str(source.path)],
                cwd=str(source.repo), timeout=120,
            )
            if not ok:
                errors.append(err)
            ok, err = _run_cleanup_git(
                ["git", "worktree", "prune"],
                cwd=str(source.repo), timeout=60,
            )
            if not ok:
                errors.append(err)

        # Best-effort secondary cleanup — a failure is still recorded.
        try:
            if source.temp_root.exists():
                shutil.rmtree(source.temp_root)
        except Exception as exc:
            errors.append(
                f"temporary directory not deleted: {type(exc).__name__}: {exc}")

        try:
            from packages.orchestration import worktrees as W
            registered = W._worktree_registered(source.repo, source.path)
        except Exception as exc:
            registered = True
            errors.append(f"worktree inventory failed: {type(exc).__name__}: {exc}")
        out["temporary_registration_removed"] = not registered
        if registered:
            errors.append(f"temporary worktree {source.path.name} is still registered")

        try:
            still_there = source.path.exists()
        except Exception as exc:
            still_there = True
            errors.append(f"path check failed: {type(exc).__name__}: {exc}")
        out["temporary_worktree_removed"] = not still_there
        if still_there:
            errors.append(
                f"temporary worktree directory {source.path.name} still exists")
    except Exception as exc:                      # belt and braces: never raise
        errors.append(f"cleanup aborted: {type(exc).__name__}: {exc}")

    if errors:
        out["cleanup_status"] = "failed"
        out["cleanup_error"] = "; ".join(errors)
    return out


def apply_job(
    job_id: str,
    target_repo: str = ".",
    *,
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
    skip_blocked: bool = False,
    commit_with_history: bool = False,
    commit_message: str | None = None,
    commit_auto: bool = False,
    push: bool = False,
) -> JobApplyResult:
    """Apply reviewed job workspace changes into target repo.

    Without --approve, returns dry-run preview only. Never auto-applies.
    A plain apply makes no git commit and no push; there is never a git
    reset of a branch, a checkout or a forced push. The operator's flags are
    the exceptions, each refused with one sentence that changes nothing, and
    each previewing without --approve with every refusal the real run would
    meet. ``commit_with_history`` (DECISION F270 D2) replaces the copy of
    files, and only the copy, with a ``git merge --no-ff`` of the job branch
    onto the operator's current branch. ``commit_message`` (``--commit``) and
    ``commit_auto`` (``--commit-auto``, DECISION F270 D3) copy as a plain
    apply does and, after the verification and the post-test pass, land ONE
    commit of exactly the copied files. ``push`` then pushes what landed to
    the branch's upstream, never forced. The three ``--commit…`` flags are
    mutually exclusive and ``push`` needs one; a clash is refused before the
    job is read.

    Every applied file must come from a task apply manifest.
    No workspace fallback scanning. Baseline-aware target safety.

    ``skip_blocked`` is the operator's SECOND, explicit decision, taken after
    reading the blocked list — it does not weaken the fence. See
    ``_apply_from_workspace`` for what it does and, more importantly, does not
    change.
    """
    from packages.orchestration.pingpong_job import (
        JOB_COMPLETED,
        TASK_APPLIED,
        _export_execution_config,
        load_job_plan,
    )

    result = JobApplyResult(
        job_id=job_id,
        approved=approve,
        dry_run=dry_run,
        target_repo=str(Path(target_repo).resolve()),
        post_test_command=test_command,
        skip_blocked=skip_blocked,
        commit_with_history=commit_with_history,
        commit_message=commit_message or "",
        push=push,
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    # --- DECISION F270 D3 (1): the flags themselves, before the job is read ---
    mode, flags_refusal = commit_flags_refusal(commit_message, commit_auto,
                                               commit_with_history, push)
    result.commit_message_mode = mode
    if flags_refusal:
        return _block(result, flags_refusal)

    # --- Load job ---
    job = load_job_plan(job_id)
    if job is None:
        return _block(result, f"job_not_found: {job_id}")

    result.job_status = job.state
    result.job_title = job.job_title
    result.job_workspace_path = job.job_workspace_path or ""

    ec = _export_execution_config(job.execution_config)
    result.execution_config = ec or {}
    result.context_strategy = (
        job.execution_config.context_strategy
        if job.execution_config else "unknown"
    )

    # --- Task summaries ---
    for t in job.tasks:
        result.task_summaries.append(TaskApplySummary(
            task_id=t.task_id,
            title=t.title,
            status=t.status,
            run_id=t.run_id,
            reviewer_verdict=t.reviewer_verdict,
            test_passed=t.test_passed,
            repair_rounds_used=t.repair_rounds_used,
            repair_rounds_allowed=t.repair_rounds_allowed,
            applied_files=(
                t.apply_manifest.applied_files
                if t.apply_manifest else []
            ),
        ))

    # --- Readiness gates ---
    if job.state != JOB_COMPLETED:
        return _block(result, f"job_not_completed: status={job.state}")

    for t in job.tasks:
        if t.status != TASK_APPLIED:
            return _block(result, f"task_not_applied: {t.task_id} status={t.status}")
        if not t.run_id:
            return _block(result, f"task_missing_run_id: {t.task_id}")
        if t.reviewer_verdict != "pass":
            return _block(result, f"reviewer_not_pass: {t.task_id} verdict={t.reviewer_verdict}")
        if t.test_passed is False:
            return _block(result, f"tests_failed: {t.task_id}")

    # --- Target guard ---
    tg = job.target_guard
    if tg and tg.target_mutated:
        return _block(result, "target_mutated_during_job")
    result.target_guard_ok = True

    # --- Require explicit apply manifests, no fallback ---
    for t in job.tasks:
        if not t.apply_manifest:
            return _block(result, f"missing_apply_manifest: {t.task_id}")
        if t.apply_manifest.status != "applied":
            return _block(result, f"apply_manifest_not_applied: {t.task_id} status={t.apply_manifest.status}")

    # --- Apply source ---
    # F006: a completed worktree job has NO live workspace by design (a clean
    # cleanup removed it). Its hand-off is the recorded base commit plus the
    # verified result.diff, materialized into a TEMPORARY detached worktree here.
    # This function is the single lifecycle owner: from the moment a temporary
    # directory may exist, every exit path runs the checked cleanup, records its
    # result on the returned object, and persists that final record exactly once.
    apply_source: ApplySource | None = None
    out = result
    try:
        if getattr(job, "isolation_mode", "copy") == "worktree":
            apply_source, perr = _materialize_apply_source_owned(job)
            if perr:
                out = _block(result, perr, persist=False)
            else:
                out = _apply_from_workspace(
                    job, result, apply_source.path, target_repo,
                    approve=approve, dry_run=dry_run, test_command=test_command,
                    skip_blocked=skip_blocked,
                    persist_final=False,
                    commit_with_history=commit_with_history,
                )
        else:
            ws_path = job.job_workspace_path
            if not ws_path:
                return _block(result, "no_job_workspace_path")
            workspace = Path(ws_path)
            if not workspace.is_dir():
                return _block(result, f"workspace_missing: {ws_path}")
            return _apply_from_workspace(
                job, result, workspace, target_repo,
                approve=approve, dry_run=dry_run, test_command=test_command,
                skip_blocked=skip_blocked,
                commit_with_history=commit_with_history,
            )
    finally:
        if apply_source is not None:
            try:
                cleanup = _cleanup_apply_source(apply_source)
            except Exception as exc:
                # _cleanup_apply_source is total, but a cleanup bug must still
                # never destroy the apply outcome or the durable record.
                cleanup = _failed_cleanup(
                    f"cleanup raised unexpectedly: {type(exc).__name__}: {exc}")
            out.temporary_worktree_removed = cleanup["temporary_worktree_removed"]
            out.temporary_registration_removed = cleanup["temporary_registration_removed"]
            out.cleanup_status = cleanup["cleanup_status"]
            out.cleanup_error = cleanup["cleanup_error"]

    if apply_source is not None and out.cleanup_status == "failed":
        # Never claim a clean run. The apply outcome and the applied-file list
        # are preserved: the target WAS touched if the status says so. A cleanup
        # failure during a materialization failure reports BOTH.
        if out.status == "applied":
            out.status = "applied_cleanup_failed"
        elif out.status == "dry_run":
            out.status = "dry_run_cleanup_failed"
        elif out.status == "blocked" and not out.files_applied:
            out.status = "materialization_failed_cleanup_failed"
        out.blocked_reasons = list(out.blocked_reasons) + [
            f"temporary_apply_cleanup_failed: {out.cleanup_error}"
        ]

    # ONE final persistence, after cleanup, for every materialized outcome — so the
    # persisted record's cleanup fields and status match the object the CLI got.
    if apply_source is not None:
        _safe_persist(job_id, out, out.files_applied, final=True)
    return out


def _reviewed_files_and_proofs(job: Any) -> tuple[list[str], dict[str, Any]]:
    from packages.orchestration.pingpong_job import (
        _latest_task_proofs,
        _reviewed_task_files,
    )
    return _reviewed_task_files(job), _latest_task_proofs(job)


def _check_source_coverage(job: Any, result: JobApplyResult, workspace: Path) -> str:
    """The materialized source's changed paths must equal the reviewed file set.

    An extra file in the root diff (a finalization hook writing ``rogue.txt``) would
    otherwise be materialized into the apply source and quietly ignored, so the
    hand-off, the task evidence and the apply would all disagree. Any extra or
    missing path blocks.
    """
    import subprocess

    proc = subprocess.run(
        ["git", "status", "--porcelain", "-z", "--untracked-files=all"],
        cwd=str(workspace), capture_output=True, text=True, timeout=120,
    )
    if proc.returncode != 0:
        return f"apply_source_inspect_failed: {proc.stderr.strip()[:150]}"
    changed = sorted({
        entry[3:] for entry in proc.stdout.split("\0") if len(entry) > 3
    })
    reviewed, _proofs = _reviewed_files_and_proofs(job)

    result.source_changed_files = changed
    result.reviewed_task_files = reviewed
    result.unexpected_source_files = sorted(set(changed) - set(reviewed))
    result.missing_source_files = sorted(set(reviewed) - set(changed))

    if result.unexpected_source_files or result.missing_source_files:
        return (
            "apply_coverage_failed: "
            f"unexpected={result.unexpected_source_files} "
            f"missing={result.missing_source_files}"
        )
    return ""


def _mode_of(path: Path) -> str:
    from packages.orchestration import worktrees as W
    return W.file_mode(path)


def _apply_from_workspace(
    job: Any,
    result: JobApplyResult,
    workspace: Path,
    target_repo: str,
    *,
    approve: bool,
    dry_run: bool,
    test_command: str,
    skip_blocked: bool = False,
    persist_final: bool = True,
    commit_with_history: bool = False,
) -> JobApplyResult:
    """The existing baseline-aware apply, against a resolved source.

    ``commit_with_history`` (DECISION F270 D2) leaves every gate below as it
    is; its refusals are checked after them and again right before the merge,
    and the merge takes the place of the file copy only.

    ``persist_final=False`` means an outer owner (the temporary-worktree lifecycle)
    will write the ONE final record after cleanup, so this function must not write
    a record that would later disagree with the returned object.

    ``skip_blocked`` CHANGES ONE DECISION AND NOTHING ELSE: whether a non-empty
    blocked set aborts the whole apply. It does not widen what may be written.
    Every blocked path is still detected by the same ``_is_blocked_path``,
    ``_validate_dest_containment`` and ``_validate_source_containment`` checks, is
    still kept out of ``planned``, is still never opened for writing, and is still
    named in ``files_blocked`` and in the summary. What it buys is the operator's
    second explicit decision, taken AFTER reading that list: apply the remainder
    as its own atomic change set. That is a different question from "apply
    everything or nothing", and answering it does not make the fence weaker —
    a silent skip would, and this is the opposite of silent.
    """
    job_id = job.job_id

    def _persist_outcome(applied_files: list[str]) -> None:
        if persist_final:
            _safe_persist(job_id, result, applied_files, final=True)

    # --- Target repo exists ---
    target = Path(target_repo).resolve()
    if not target.is_dir():
        return _block(result, f"target_not_directory: {target_repo}")

    # --- Fidelity: the materialized source must be EXACTLY the reviewed work ---
    if getattr(job, "isolation_mode", "copy") == "worktree":
        cov_err = _check_source_coverage(job, result, workspace)
        if cov_err:
            return _block(result, cov_err)

    # --- Collect files from apply manifests only ---
    all_applied: list[str] = []
    for t in job.tasks:
        if t.apply_manifest and t.apply_manifest.applied_files:
            all_applied.extend(t.apply_manifest.applied_files)

    if not all_applied:
        return _block(result, "no_files_in_apply_manifests")

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_files: list[str] = []
    for f in all_applied:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    # --- Validate each file ---
    planned: list[str] = []
    blocked: list[str] = []
    skipped: list[str] = []

    for rel_path in unique_files:
        block_reason = _is_blocked_path(rel_path)
        if block_reason:
            blocked.append(f"{rel_path}: {block_reason}")
            continue

        dest_reason = _validate_dest_containment(target, rel_path)
        if dest_reason:
            blocked.append(f"{rel_path}: {dest_reason}")
            continue

        src_reason = _validate_source_containment(workspace, rel_path)
        if src_reason:
            blocked.append(f"{rel_path}: {src_reason}")
            continue

        ws_file = workspace / rel_path
        try:
            size = ws_file.stat().st_size
        except OSError:
            skipped.append(f"{rel_path}: unreadable")
            continue

        if size > _MAX_FILE_SIZE:
            skipped.append(f"{rel_path}: too_large ({size})")
            continue

        planned.append(rel_path)

    result.files_planned = planned
    result.files_blocked = blocked
    result.files_skipped = skipped

    if blocked and not skip_blocked:
        return _block(result, f"blocked_paths: {blocked}")

    if not planned:
        # Reached with a non-empty blocked set only when --skip-blocked was passed
        # and EVERY file was blocked: there is no remainder to apply, so the
        # honest answer is still a block rather than an empty success.
        return _block(result, "no_files_to_apply")

    # --- Baseline-aware readiness check ---
    proofs = _consolidate_file_proofs(job)
    clean, block_reasons, readiness = _check_baseline_readiness(
        target, workspace, planned, proofs,
    )
    result.file_readiness = readiness
    result.target_clean = clean
    if not clean:
        return _block(result, f"baseline_check_failed: {block_reasons}")

    # --- Mode fidelity: the source must still carry the reviewed file mode ---
    _reviewed, mode_proofs = _reviewed_files_and_proofs(job)
    mode_blocks: list[str] = []
    for rel_path in planned:
        proof = mode_proofs.get(rel_path)
        expected = getattr(proof, "final_mode", "") if proof else ""
        if not expected:
            continue
        actual = _mode_of(workspace / rel_path)
        if actual != expected:
            mode_blocks.append(
                f"{rel_path}: source mode {actual} != reviewed {expected}"
            )
    if mode_blocks:
        return _block(result, f"mode_check_failed: {mode_blocks}")

    # --- DECISION F270 D2 (2), D3 (2) and (5): the --commit… and --push refusals, after every gate ---
    flag_refusals = _flag_refusals(job, result, target, planned,
                                   skip_blocked=skip_blocked, skipped=skipped)
    if flag_refusals and approve and not dry_run:
        _block(result, flag_refusals[0])
        result.blocked_reasons.extend(flag_refusals[1:])
        return result

    # --- Dry-run or unapproved: preview only ---
    if dry_run or not approve:
        # A preview with a flag names every refusal the real run would meet.
        result.blocked_reasons.extend(flag_refusals)
        result.status = "dry_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_outcome([])
        return result

    # --- Preflight job apply record writability ---
    try:
        record_dir = _job_apply_records_dir() / job_id
        record_dir.mkdir(parents=True, exist_ok=True)
        test_file = record_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
    except OSError as exc:
        return _block(result, f"job_apply_record_not_writable: {exc}")

    # --- Recheck baseline readiness immediately before apply ---
    clean2, blocks2, _ = _check_baseline_readiness(
        target, workspace, planned, proofs,
    )
    if not clean2:
        return _block(result, f"baseline_check_before_apply_failed: {blocks2}")

    # --- Durable pre-apply record ---
    result.status = "approved_apply_started"
    result.files_applied = []
    try:
        _persist_job_apply_record(job_id, result)
    except OSError as exc:
        return _block(result, f"pre_apply_record_failed: {exc}")

    # --- The same refusals, again, right before anything is written ---
    late = _flag_refusals(job, result, target, planned,
                          skip_blocked=skip_blocked, skipped=skipped)
    if late:
        result.status = "blocked"
        result.blocked_reason = late[0]
        result.blocked_reasons.extend(late)
        result.files_applied = []
        result.finished_at = datetime.now(timezone.utc).isoformat()
        _persist_outcome([])
        return result

    # --- DECISION F270 D2 (3)/(4): the merge replaces the copy, and only the copy ---
    applied: list[str] = []
    if commit_with_history:
        why = _merge_job_branch(job, result, target)
        if why:
            result.status = "blocked"
            result.blocked_reason = (f"post_merge_check_failed: {why}" if result.merge_commit
                                     else f"{HISTORY_REFUSED}: {why}")
            result.blocked_reasons.append(result.blocked_reason)
            _note_merge_undo(result)
            result.files_applied = list(planned) if result.merge_commit else []
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(result.files_applied)
            return result
        applied = list(planned)
        result.modes_applied = {p: _mode_of(workspace / p) for p in planned}

    # --- Apply files (the copy; a merge has already written them) ---
    for rel_path in ([] if commit_with_history else planned):
        ws_file = workspace / rel_path

        src_reason = _validate_source_containment(workspace, rel_path)
        if src_reason:
            result.status = "blocked"
            result.blocked_reason = f"source_unsafe_at_apply: {rel_path}: {src_reason}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

        dest_reason = _validate_dest_containment(target, rel_path)
        if dest_reason:
            result.status = "blocked"
            result.blocked_reason = f"dest_unsafe_at_apply: {rel_path}: {dest_reason}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

        dest = target / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = ws_file.read_bytes()
            dest.write_bytes(content)
            reviewed_mode = _mode_of(ws_file)
            if reviewed_mode == "100755":
                dest.chmod(dest.stat().st_mode | 0o111)
            else:
                dest.chmod(dest.stat().st_mode & ~0o111)
            result.modes_applied[rel_path] = reviewed_mode
            applied.append(rel_path)
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"write_failed: {rel_path}: {exc}"
            result.files_applied = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    result.files_applied = applied

    # --- Post-apply verification ---
    for rel_path in applied:
        ws_file = workspace / rel_path
        dest = target / rel_path
        try:
            if ws_file.read_bytes() != dest.read_bytes():
                result.status = "blocked"
                result.blocked_reason = f"post_apply_mismatch: {rel_path}"
                _note_merge_undo(result)
                result.finished_at = datetime.now(timezone.utc).isoformat()
                _persist_outcome(applied)
                return result
            src_mode, dst_mode = _mode_of(ws_file), _mode_of(dest)
            if src_mode != dst_mode:
                # A filesystem that cannot represent the reviewed mode must block,
                # not claim a faithful apply.
                result.status = "blocked"
                result.blocked_reason = (
                    f"post_apply_mode_mismatch: {rel_path}: "
                    f"target {dst_mode} != reviewed {src_mode}"
                )
                _note_merge_undo(result)
                result.finished_at = datetime.now(timezone.utc).isoformat()
                _persist_outcome(applied)
                return result
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"post_apply_verify_failed: {rel_path}: {exc}"
            _note_merge_undo(result)
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    # --- Post-apply tests ---
    if test_command:
        passed, summary = _run_post_test(test_command, target)
        result.post_test_passed = passed
        result.post_test_summary = summary
        if not passed:
            result.status = "applied_test_failed"
            _note_merge_undo(result)
            if result.commit_message_mode in ("message", "auto"):
                flag = COMMIT_MODE_FLAGS[result.commit_message_mode]
                result.blocked_reasons.append(
                    f"The post-test failed, so {flag} made no commit and nothing was "
                    f"pushed; the {len(applied)} copied file(s) are in the working tree, "
                    f"not committed.")
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    # --- DECISION F270 D3 (3): ONE commit of exactly the copied files, after they verified and tested ---
    if result.commit_message_mode in ("message", "auto"):
        why = _commit_applied_files(job, result, target, applied)
        if why:
            result.status = "blocked"
            result.blocked_reason = f"commit_failed: {why}"
            result.blocked_reasons.append(result.blocked_reason)
            if result.commit_sha:
                result.blocked_reasons.append(_commit_undo_sentence(result))
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result
    elif result.merge_commit:
        result.commit_sha = result.merge_commit

    # --- DECISION F270 D3 (5): push what landed; a failed push leaves it landed and says so ---
    if result.push and result.commit_sha:
        _push_landed_commit(result, target)
        if not result.pushed:
            result.status = "applied_push_failed"
            result.blocked_reasons.append(
                f"The push of {result.commit_sha[:12]} failed "
                f"({result.push_error}); the commit stays on {result.target_branch}, "
                f"so push it by hand once the cause is fixed.")
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_outcome(applied)
            return result

    result.status = "applied"
    result.finished_at = datetime.now(timezone.utc).isoformat()
    _persist_outcome(applied)
    return result


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _job_apply_records_dir() -> Path:
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root() / "job_apply_records"


def _persist_job_apply_record(
    job_id: str,
    result: JobApplyResult,
) -> None:
    """Persist job apply record. Raises on write failure for approved applies."""
    record_dir = _job_apply_records_dir() / job_id
    record_dir.mkdir(parents=True, exist_ok=True)
    record_file = record_dir / f"{result.job_apply_id}.json"
    data = export_job_apply_json(result)
    record_file.write_text(json.dumps(data, indent=2) + "\n")


def load_job_apply_record(job_id: str, job_apply_id: str) -> dict[str, Any] | None:
    record_file = _job_apply_records_dir() / job_id / f"{job_apply_id}.json"
    if not record_file.exists():
        return None
    try:
        return json.loads(record_file.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Export / summary (redacted, baseline-aware)
# ---------------------------------------------------------------------------

def export_job_apply_json(result: JobApplyResult) -> dict[str, Any]:
    raw = {
        "job_id": result.job_id,
        "job_apply_id": result.job_apply_id,
        "status": result.status,
        "approved": result.approved,
        "dry_run": result.dry_run,
        "target_repo": _sanitize_path(result.target_repo),
        "job_status": result.job_status,
        "job_title": result.job_title,
        "job_workspace_path": _sanitize_path(result.job_workspace_path),
        "source_changed_files": result.source_changed_files,
        "reviewed_task_files": result.reviewed_task_files,
        "unexpected_source_files": result.unexpected_source_files,
        "missing_source_files": result.missing_source_files,
        "modes_applied": result.modes_applied,
        "temporary_worktree_cleanup": {
            "temporary_worktree_removed": result.temporary_worktree_removed,
            "temporary_registration_removed": result.temporary_registration_removed,
            "cleanup_status": result.cleanup_status,
            "cleanup_error": result.cleanup_error,
        },
        "task_summaries": [
            {
                "task_id": ts.task_id,
                "title": ts.title,
                "status": ts.status,
                "run_id": ts.run_id,
                "reviewer_verdict": ts.reviewer_verdict,
                "test_passed": ts.test_passed,
                "repair_rounds_used": ts.repair_rounds_used,
                "repair_rounds_allowed": ts.repair_rounds_allowed,
                "applied_files": ts.applied_files,
            }
            for ts in result.task_summaries
        ],
        "files_planned": result.files_planned,
        "files_applied": result.files_applied,
        "files_blocked": result.files_blocked,
        "files_skipped": result.files_skipped,
        "skip_blocked": result.skip_blocked,
        "file_readiness": [
            {
                "path": fr.path,
                "kind": fr.kind,
                "baseline_status": fr.baseline_status,
                "workspace_status": fr.workspace_status,
            }
            for fr in result.file_readiness
        ],
        "blocked_reason": result.blocked_reason,
        "blocked_reasons": result.blocked_reasons,
        "target_guard_ok": result.target_guard_ok,
        "target_clean": result.target_clean,
        "execution_config": result.execution_config,
        "context_strategy": result.context_strategy,
        "post_test_command_present": bool(result.post_test_command),
        "post_test_passed": result.post_test_passed,
        "post_test_summary": result.post_test_summary,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "commit_with_history": result.commit_with_history,
        "merged_branch": result.merged_branch,
        "target_branch": result.target_branch,
        "history_commits": result.history_commits,
        "merge_commit": result.merge_commit,
        "merge_conflicts": result.merge_conflicts,
        "commit_message_mode": result.commit_message_mode,
        "commit_sha": result.commit_sha,
        "push": result.push,
        "pushed": result.pushed,
        "push_remote": result.push_remote,
        "push_ref": result.push_ref,
        "push_error": result.push_error,
    }
    return _redact_json_value(raw)


def _blocked_path_names(files_blocked: list[str]) -> list[str]:
    """The bare paths out of ``files_blocked``, whose entries read ``path: reason``."""
    return [entry.split(":", 1)[0].strip() for entry in files_blocked]


def _next_step_for_apply(result: JobApplyResult) -> str:
    """The honest ``Next:`` line a stalled apply owes its operator.

    Every other stalled surface in Remedy ends with one — `remedy do`,
    `remedy status`, the orchestrator's ``next_safe_action``, the proof chain —
    and a blocked apply used to print its reason and stop, leaving the
    operator's only remaining move to go and read the source.

    The line names the route that ACTUALLY applies to the block in hand.
    ``--skip-blocked`` lifts a protected-path block and nothing else, so it is
    offered where it is true and explicitly ruled out where it is not.
    """
    reason = result.blocked_reason or ""

    if result.merge_commit:
        return (f"Next: inspect the merge commit {result.merge_commit[:12]} on "
                f"{result.target_branch}; if it must go, run `git reset --keep "
                f"{result.history_previous_head}` yourself.")

    if reason.startswith(f"{HISTORY_REFUSED}:"):
        return ("Next: do what the sentence above asks and re-run with "
                "--commit-with-history, or re-run without it to copy the files and "
                "commit them yourself.")

    if result.commit_sha:
        return (f"Next: inspect the commit {result.commit_sha[:12]} on "
                f"{result.target_branch}; if it must go, run `git reset --keep "
                f"{result.history_previous_head}` yourself.")

    if reason.startswith((f"{COMMIT_REFUSED}:", f"{PUSH_REFUSED}:")):
        return ("Next: do what the sentence above asks and re-run, or re-run with "
                "--approve alone to copy the files and commit them yourself.")

    if reason.startswith("commit_failed:"):
        return ("Next: the files are copied and not committed; fix what git said, then "
                "commit them yourself.")

    if reason.startswith("blocked_paths:"):
        names = _blocked_path_names(result.files_blocked)
        listed = ", ".join(names) if names else "the paths listed above"
        remaining = len(result.files_planned)
        return (
            f"Next: remove {listed} from the job workspace and re-run, or re-run "
            f"with --skip-blocked to apply the remaining {remaining} file(s) and "
            f"deliberately leave {listed} not applied."
        )

    if reason == "no_files_to_apply" and result.files_blocked:
        names = _blocked_path_names(result.files_blocked)
        listed = ", ".join(names) if names else "every file"
        return (
            f"Next: every file in this job is protected ({listed}), so there is no "
            f"remainder for --skip-blocked to apply. Remove the protected path(s) "
            f"from the job workspace and re-run."
        )

    return (
        "Next: resolve the blocked reason above and re-run. --skip-blocked lifts a "
        "protected-path block only and does not apply to this one."
    )


def summarize_job_apply(result: JobApplyResult) -> str:
    lines = [
        f"Job: {result.job_id}",
        f"Title: {result.job_title}",
        f"Job apply record: {result.job_apply_id}",
        f"Status: {result.status}",
        f"Approved: {result.approved}",
        f"Target: {_sanitize_path(result.target_repo)}",
    ]
    if result.cleanup_status:
        lines.append(f"Temp worktree cleanup: {result.cleanup_status}")
        if result.cleanup_error:
            lines.append(f"  Cleanup error: {result.cleanup_error}")

    if result.cleanup_status == "failed":
        # Never let a reader infer the damage from a status string alone: say
        # plainly whether the target was touched, which files, and what is left over.
        lines.append("")
        if result.files_applied:
            lines.append("The target was changed.")
            lines.append(f"Files applied: {result.files_applied}")
        else:
            lines.append("The target was NOT changed"
                         + (" (dry-run only)." if result.dry_run or not result.approved
                            else "."))
        lines.append("Temporary apply cleanup failed.")
        lines.append(f"Cleanup error: {result.cleanup_error}")
        if not result.temporary_registration_removed:
            lines.append(
                "A temporary git worktree registration may remain "
                "(check `git worktree list`)."
            )
        if not result.temporary_worktree_removed:
            lines.append("A temporary apply directory may remain on disk.")
        lines.append("Manual cleanup is required.")

    if result.task_summaries:
        lines.append("")
        lines.append("Tasks:")
        for ts in result.task_summaries:
            verdict = ts.reviewer_verdict or "none"
            test = "passed" if ts.test_passed else ("failed" if ts.test_passed is False else "n/a")
            lines.append(f"  {ts.task_id}: {ts.title} — {ts.status} "
                         f"(reviewer: {verdict}, tests: {test})")

    if result.status == "dry_run":
        lines.append("")
        lines.append("Dry-run preview only. No target files changed.")
        if result.file_readiness:
            lines.append(f"Would apply {len(result.files_planned)} file(s):")
            for fr in result.file_readiness:
                lines.append(f"  {fr.path} [{fr.kind}] "
                             f"baseline={fr.baseline_status} ws={fr.workspace_status}")
        prefixes = (HISTORY_REFUSED, COMMIT_REFUSED, PUSH_REFUSED)
        refusals = [r.split(": ", 1)[1] for r in result.blocked_reasons
                    if r.split(":", 1)[0] in prefixes]
        flag = COMMIT_MODE_FLAGS.get(result.commit_message_mode, "")
        if flag:
            lines.append("")
            if refusals:
                lines.append(f"With --approve, {flag}{' --push' if result.push else ''} "
                             f"would be refused:")
                lines.extend(f"  {r}" for r in refusals)
            else:
                if result.commit_message_mode == "history":
                    lines.append("With --approve, --commit-with-history merges the job "
                                 "branch onto your current branch with git merge --no-ff "
                                 "instead of copying files.")
                else:
                    lines.append(f"With --approve, {flag} copies the files and then "
                                 f"commits exactly them on your current branch, as you.")
                if result.push:
                    lines.append("With --approve, --push then pushes that branch to its "
                                 "configured upstream, never forced.")
        lines.append("")
        flag_words = (f"--commit {shlex.quote(result.commit_message)}"
                      if result.commit_message_mode == "message" else flag)
        lines.append(
            f"To apply: remedy job apply {result.job_id}"
            f" --repo <target> --approve"
            + (f" {flag_words}" if flag_words else "")
            + (" --push" if result.push else "")
        )

    elif result.status == "applied":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s):")
        for f in result.files_applied:
            lines.append(f"  {f}")
        if result.skip_blocked and result.files_blocked:
            # Never let a partial apply read as a whole one: say what was
            # withheld, in the same breath as what was applied.
            lines.append(
                f"--skip-blocked deliberately left {len(result.files_blocked)} "
                f"protected path(s) not applied; they were not written to the target "
                f"and are listed below."
            )
        if result.post_test_passed is not None:
            lines.append(
                f"Post-test: {'passed' if result.post_test_passed else 'FAILED'}"
            )
        lines.append("")
        pushed = (f"Pushed it to {result.push_remote} {result.push_ref}, never forced."
                  if result.pushed else "Nothing was pushed.")
        if result.merge_commit:
            lines.append(
                f"Merged {len(result.history_commits)} task commit(s) of "
                f"{result.merged_branch} onto {result.target_branch} as merge commit "
                f"{result.merge_commit}. {pushed}")
        elif result.commit_sha:
            lines.append(
                f"Committed the {len(result.files_applied)} copied file(s) on "
                f"{result.target_branch} as {result.commit_sha}, as you. {pushed}")
        else:
            lines.append("No commits or pushes were made. Review and commit manually.")

    elif result.status == "applied_push_failed":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s) and landed "
                     f"{result.commit_sha} on {result.target_branch}, but the push to "
                     f"{result.push_remote or '(no remote)'} {result.push_ref or '(no ref)'} "
                     f"failed: {result.push_error}")
        lines.append("The commit stays where it landed and nothing was forced; push it "
                     "by hand once the cause is fixed.")

    elif result.status == "applied_test_failed":
        lines.append("")
        lines.append(f"Applied {len(result.files_applied)} file(s) but post-test FAILED.")
        if result.merge_commit:
            lines.append(_merge_undo_sentence(result))
        else:
            if result.commit_message_mode in ("message", "auto"):
                lines.append(f"{COMMIT_MODE_FLAGS[result.commit_message_mode]} made no "
                             f"commit and nothing was pushed.")
            lines.append("Manual review required. Changes are in working tree, not committed.")

    elif result.status == "applied_record_update_failed":
        lines.append("")
        lines.append(f"WARNING: Applied {len(result.files_applied)} file(s) but job apply record update FAILED.")
        lines.append(f"Reason: {result.blocked_reason}")
        lines.append("Target files may have changed. Manual review required.")
        lines.append("Pre-apply record exists. Final record could not be written.")

    elif result.status == "approved_apply_started":
        lines.append("")
        lines.append("Apply in progress. This status should not appear in final output.")

    elif result.status == "blocked":
        lines.append("")
        lines.append(f"BLOCKED: {result.blocked_reason}")
        if result.merge_commit:
            lines.append(_merge_undo_sentence(result))
        elif result.commit_sha:
            lines.append(_commit_undo_sentence(result))

    if result.files_blocked:
        lines.append("")
        lines.append("Blocked files:")
        for f in result.files_blocked:
            lines.append(f"  {f}")

    if result.files_skipped:
        lines.append("")
        lines.append("Skipped files:")
        for f in result.files_skipped:
            lines.append(f"  {f}")

    # A blocked apply ALWAYS ends with its next step, after the file lists so
    # the operator reads the paths before the route through them.
    if result.status == "blocked":
        lines.append("")
        lines.append(_next_step_for_apply(result))

    return _redact_secrets("\n".join(lines) + "\n")
