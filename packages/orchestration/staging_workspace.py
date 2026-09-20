"""Staging Workspace — a filtered copy of the target repo in an isolated directory.

Design:
  - Filtered copy excludes: .git, .env*, node_modules, venv, __pycache__, .data
  - Symlinks resolving outside repo root are excluded (escape detection)
  - F276 T003: when the target IS a git repository, ONE ``git check-ignore
    --stdin -z`` pass over the whole candidate list decides which paths the copy
    skips, and a per-file ceiling (:data:`MAX_COPY_FILE_BYTES`) is the backstop
    for what the ignore rules miss. Both are RECORDED on :class:`StagingWorkspace`
    rather than silently applied.
  - F276 T003: :func:`release_staging_workspace` frees ONE terminal job's copy.
    ``pingpong_job._create_job_workspace_copy`` made these directories and nothing
    ever removed them; the worktree path had a cleanup path and the copy path had
    none, which is the 650 GB the feature was written for.

Public API::

    create_staging_workspace(target_repo, staging_parent, job_id) -> StagingWorkspace
    release_staging_workspace(job_id, root=None) -> StagingRelease
    staging_dir_name(job_id) -> str
    STAGING_DIR_PREFIX / STAGING_DATA_CLASS / MAX_COPY_FILE_BYTES
    GITIGNORE_FILTER_APPLIED / GITIGNORE_FILTER_NO_GIT / GITIGNORE_FILTER_FAILED
"""
from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Directories excluded from filtered copy
_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".data", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "dist", "build", ".eggs",
})

#: The data-root class these copies live in, and the prefix that precedes the job id
#: in a copy's directory name. Spelled HERE because this module is what MAKES the
#: name; ``data_reclaim._JOB_KEYED_PREFIXES`` imports the prefix rather than
#: re-spelling it, so the reclaim command and the copy cannot drift apart about what
#: a staging directory is called.
STAGING_DATA_CLASS: str = "job_workspaces"
STAGING_DIR_PREFIX: str = "staging_"

#: The hard per-file ceiling of the filtered copy, in bytes. A file STRICTLY LARGER
#: than this is not copied; one exactly at it is.
#:
#: MEASURED 2026-09-20 on the operator's own checkout — the repository that is itself
#: the target of every self-use job. The whole tree, minus the directories
#: ``_EXCLUDE_DIRS`` already skips, is 5013 files and 584 043 593 bytes, and the 2
#: files at or above 5 MiB hold 504 713 171 of them — 86.4 % of the tree — both of
#: them artifacts git already ignores: ``.coverage`` at 436 084 736 bytes and a
#: ``remedy-review-*.zip`` at 68 628 435, which is exactly the class the feature
#: file's sampled workspace named. So the ignore pass does nearly all of the work
#: and this ceiling is a BACKSTOP for what no ignore rule covers, not the main filter.
#:
#: WHY NOT 5 MiB, the figure that sample was described in: on the same checkout the
#: 5358 files git TRACKS hold 72 450 733 bytes and not one of them reaches 5 MiB —
#: but the largest, ``.agent/live_review_archive.md`` at 4 284 047 bytes, is at 82 %
#: of it and is APPEND-ONLY. A 5 MiB ceiling would begin silently dropping a file
#: this project's own workflow reads within this feature's lifetime.
#:
#: WHY 16 MiB: it is 3.9x the largest tracked file, while the two artifacts above are
#: 26x and 4x OVER it, so the backstop still catches the class it exists for even if
#: a ``.gitignore`` entry for them were lost. And nothing this large is source a task
#: can read: ``pingpong_job._TASK_BODY_LIMIT`` is 2000 characters, four orders of
#: magnitude below this, so a file over the ceiling cannot reach a builder prompt.
MAX_COPY_FILE_BYTES: int = 16 * 1024 * 1024

#: The three values :attr:`StagingWorkspace.gitignore_filter` can carry. They are
#: TOKENS, matched exactly by a reader, with the prose in ``gitignore_detail``
#: beside them — the same reason/detail split ``data_reclaim`` reports refusals with.
GITIGNORE_FILTER_APPLIED: str = "applied"
GITIGNORE_FILTER_NO_GIT: str = "no_git_repository"
GITIGNORE_FILTER_FAILED: str = "git_failed"

#: A ``check-ignore`` pass over a huge tree is one process reading one list; this
#: bounds it so a hung git can never hang a job's workspace creation.
_CHECK_IGNORE_TIMEOUT_SECONDS: float = 120.0


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------

def _is_env_file(name: str) -> bool:
    """Return True for .env, .env.*, .env-* files."""
    if name == ".env":
        return True
    if name.startswith(".env.") or name.startswith(".env-"):
        return True
    return False


def _should_exclude_dir(name: str) -> bool:
    """Check if a directory name should be excluded from filtered copy."""
    if name in _EXCLUDE_DIRS:
        return True
    # Skip hidden dot-directories
    if name.startswith(".") and name != ".":
        return True
    return False


def _is_symlink_escape(item: Path, repo_root: Path) -> bool:
    """Return True if item is a symlink resolving outside repo_root."""
    if not item.is_symlink():
        return False
    try:
        resolved = item.resolve()
        root_resolved = repo_root.resolve()
        return not resolved.is_relative_to(root_resolved)
    except (OSError, ValueError):
        return True  # Cannot resolve — treat as escape


def staging_dir_name(job_id: str) -> str:
    """The directory name ONE job's staging copy carries, prefix included."""
    return f"{STAGING_DIR_PREFIX}{job_id[:16]}"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class StagingWorkspace:
    """An isolated, filtered copy of a target repo.

    The ``excluded_*`` lists are the copy's own account of what it left behind, and
    F276 T003 adds two more to that family plus the bytes they came to:

    * ``excluded_ignored`` — paths the target repository's own ignore rules cover.
    * ``excluded_oversize`` — paths over :data:`MAX_COPY_FILE_BYTES`.
    * ``excluded_bytes`` — the summed ``st_size`` of EXACTLY those two lists, which
      is why it is not called "bytes excluded": ``excluded_dirs``,
      ``excluded_symlinks`` and ``excluded_env_files`` are never measured (a
      directory is skipped without being walked), so a total over all five would be
      a number no caller could interpret.
    * ``gitignore_filter`` / ``gitignore_detail`` — whether the ignore pass ran at
      all, as a token and its reason. A copy that ran unfiltered SAYS SO rather than
      looking like a copy of a target with nothing to ignore.
    """
    staging_dir: Path
    target_repo: Path
    job_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    files_copied: int = 0
    dirs_copied: int = 0
    excluded_dirs: list[str] = field(default_factory=list)
    excluded_symlinks: list[str] = field(default_factory=list)
    excluded_env_files: list[str] = field(default_factory=list)
    excluded_ignored: list[str] = field(default_factory=list)
    excluded_oversize: list[str] = field(default_factory=list)
    excluded_bytes: int = 0
    gitignore_filter: str = GITIGNORE_FILTER_NO_GIT
    gitignore_detail: str = ""
    active: bool = True


@dataclass(frozen=True)
class StagingRelease:
    """What :func:`release_staging_workspace` did to ONE job's staging copy.

    ``existed`` and ``released`` are separate on purpose: a SECOND release of the
    same job answers ``existed=False, released=False, reason=""``, which is a no-op
    and not a failure, while a refusal answers ``existed=True, released=False`` with
    the reason that stopped it. A caller that only checked ``released`` could not
    tell those two apart, and they are the two the lifecycle has to distinguish.
    """

    job_id: str
    path: str
    existed: bool
    released: bool
    reason: str
    detail: str
    freed_bytes: int


# ---------------------------------------------------------------------------
# The ignore pass — ONE subprocess for the whole candidate list
# ---------------------------------------------------------------------------

def _git_ignored(target_repo: Path,
                 rel_paths: list[str]) -> tuple[frozenset[str], str, str]:
    """``(ignored, filter_token, detail)`` for the WHOLE candidate list at once.

    ONE ``git check-ignore --stdin -z`` process, never one per file: the sampled
    workspace behind this feature held 76 files over 5 MB inside a tree of thousands,
    and a process per path would cost more than the copy it is meant to shorten.

    The target must hold its OWN ``.git`` for the pass to run, and that stat is not a
    convenience: a target NESTED inside another repository answers ``check-ignore``
    SUCCESSFULLY with the OUTER repository's rules, so the guard is what makes this
    pass mean the target's own ignore file. A ``.git`` FILE rather than a directory —
    a git worktree checkout — still counts, DELIBERATELY: such a checkout has its own
    ignore rules and is a target a job may legitimately be pointed at.

    ``check-ignore`` consults the index, so a TRACKED file is never reported ignored
    even when a pattern matches it — the safe direction, and the reason no tracked
    source can be dropped by this filter.

    Exit 0 means at least one path is ignored, 1 means none, and anything else is a
    failure: the copy then proceeds UNFILTERED and says so through its token.
    """
    if not (target_repo / ".git").exists():
        return (frozenset(), GITIGNORE_FILTER_NO_GIT,
                "the target holds no .git of its own, so it has no ignore rules here")
    if not rel_paths:
        return (frozenset(), GITIGNORE_FILTER_APPLIED, "")
    try:
        proc = subprocess.run(
            ["git", "check-ignore", "--stdin", "-z"],
            cwd=str(target_repo),
            input=b"\0".join(os.fsencode(p) for p in rel_paths),
            capture_output=True,
            timeout=_CHECK_IGNORE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return (frozenset(), GITIGNORE_FILTER_FAILED, f"{type(exc).__name__}: {exc}")
    if proc.returncode not in (0, 1):
        detail = proc.stderr.decode("utf-8", "replace").strip().splitlines()
        return (frozenset(), GITIGNORE_FILTER_FAILED,
                f"git check-ignore exited {proc.returncode}: "
                f"{detail[0] if detail else 'no stderr'}")
    ignored = {os.fsdecode(p) for p in proc.stdout.split(b"\0") if p}
    return (frozenset(ignored), GITIGNORE_FILTER_APPLIED, "")


@dataclass
class _Enumeration:
    """The copy's candidate list, read BEFORE anything is copied or asked of git."""

    dirs: list[Path] = field(default_factory=list)
    files: list[tuple[str, Path, int]] = field(default_factory=list)
    excluded_dirs: list[str] = field(default_factory=list)
    excluded_symlinks: list[str] = field(default_factory=list)
    excluded_env_files: list[str] = field(default_factory=list)


def _enumerate(target_repo: Path) -> _Enumeration:
    """Walk the target once, applying the filters that need no subprocess.

    The directory-name, symlink-escape and ``.env`` rules are unchanged and still
    decide here; the two F276 T003 filters cannot, because one of them needs the
    whole list in hand before it may ask git anything.
    """
    found = _Enumeration()

    def walk(src: Path) -> None:
        found.dirs.append(src)
        for item in sorted(src.iterdir()):
            rel = str(item.relative_to(target_repo))

            # Symlink escape check
            if _is_symlink_escape(item, target_repo):
                found.excluded_symlinks.append(rel)
                continue

            if item.is_dir():
                if _should_exclude_dir(item.name):
                    found.excluded_dirs.append(rel)
                    continue
                walk(item)
            elif item.is_file():
                if _is_env_file(item.name):
                    found.excluded_env_files.append(rel)
                    continue
                try:
                    size = item.stat().st_size
                except OSError:
                    size = 0
                found.files.append((rel, item, size))

    walk(target_repo)
    return found


# ---------------------------------------------------------------------------
# Filtered copy
# ---------------------------------------------------------------------------

def create_staging_workspace(
    target_repo: Path,
    staging_parent: Path,
    job_id: str,
) -> StagingWorkspace:
    """Create a filtered copy of target_repo in an isolated staging directory.

    Copies all files except excluded dirs/patterns. Preserves directory structure.
    Excludes symlinks that resolve outside repo root and .env* files.
    staging_parent should be a Remedy workspace-scoped directory.

    F276 T003: the tree is ENUMERATED first, the ignore rules are asked once for the
    whole list, and only then is anything copied. What the two new filters left
    behind is recorded on the returned :class:`StagingWorkspace`.
    """
    staging_dir = staging_parent / staging_dir_name(job_id)
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    found = _enumerate(target_repo)
    ignored, filter_token, filter_detail = _git_ignored(
        target_repo, [rel for rel, _src, _size in found.files])

    files_copied = 0
    dirs_copied = 0
    excluded_ignored: list[str] = []
    excluded_oversize: list[str] = []
    excluded_bytes = 0

    for src_dir in found.dirs:
        (staging_dir / src_dir.relative_to(target_repo)).mkdir(parents=True, exist_ok=True)
        dirs_copied += 1

    for rel, src, size in found.files:
        if rel in ignored:
            excluded_ignored.append(rel)
            excluded_bytes += size
            continue
        if size > MAX_COPY_FILE_BYTES:
            excluded_oversize.append(rel)
            excluded_bytes += size
            continue
        shutil.copy2(str(src), str(staging_dir / rel))
        files_copied += 1

    return StagingWorkspace(
        staging_dir=staging_dir,
        target_repo=target_repo,
        job_id=job_id,
        files_copied=files_copied,
        dirs_copied=dirs_copied,
        excluded_dirs=found.excluded_dirs,
        excluded_symlinks=found.excluded_symlinks,
        excluded_env_files=found.excluded_env_files,
        excluded_ignored=excluded_ignored,
        excluded_oversize=excluded_oversize,
        excluded_bytes=excluded_bytes,
        gitignore_filter=filter_token,
        gitignore_detail=filter_detail,
    )


# ---------------------------------------------------------------------------
# The release — the copy path's opposite number to the worktree's removal
# ---------------------------------------------------------------------------

def release_staging_workspace(job_id: str,
                              root: Path | None = None) -> StagingRelease:
    """Remove ONE terminal job's staging copy, under the reclaim command's own rules.

    This is ``remedy data reclaim`` narrowed to a single job and run at the moment
    the job ends, so it applies the SAME rules rather than a second spelling of
    them: ``data_reclaim.child_deletion_refusal`` decides direct-child, symlink and
    inside-the-root, ``data_reclaim.job_state_refusal`` decides resolves-and-is-
    terminal, and every reason returned is one of ``data_reclaim.REFUSAL_REASONS``.
    A path this refuses is a path the reclaim command will later judge by the same
    rules, so the two can never disagree.

    The path is DERIVED from the class registry — ``data_class_dir`` plus
    :func:`staging_dir_name` — and never read from the job record. A recorded path
    is input, not authority, and this function may delete a directory.

    IDEMPOTENT: a second call finds nothing and answers ``existed=False,
    released=False, reason=""``. That is a no-op, not an error, because the hook
    that calls it runs in a ``finally`` and a job may reach it more than once.
    """
    from packages.orchestration.data_footprint import child_usage
    from packages.orchestration.data_paths import data_class_dir, resolve_data_root
    from packages.orchestration.data_reclaim import (
        child_deletion_refusal,
        job_state_refusal,
    )

    data_root = Path(root) if root is not None else resolve_data_root()
    path = os.fspath(data_class_dir(STAGING_DATA_CLASS, data_root)
                     / staging_dir_name(job_id))

    if not os.path.lexists(path):
        return StagingRelease(job_id, path, False, False, "", "", 0)

    # Structural first, and the symlink rule inside it before anything else reads
    # through the path: a link is never followed and never deleted.
    reason, detail = child_deletion_refusal(path, data_root,
                                            data_class=STAGING_DATA_CLASS)
    if reason:
        return StagingRelease(job_id, path, True, False, reason, detail, 0)

    _state, reason, _record_exists = job_state_refusal(job_id, data_root)
    if reason:
        return StagingRelease(
            job_id, path, True, False, reason,
            f"job {job_id} is {_state or 'unresolved'}; its workspace is kept", 0)

    freed, _files = child_usage(path)
    try:
        shutil.rmtree(path)
    except OSError as exc:
        return StagingRelease(job_id, path, True, False, "delete_failed", str(exc), 0)
    return StagingRelease(job_id, path, True, True, "", "", freed)
