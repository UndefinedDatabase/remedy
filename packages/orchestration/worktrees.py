"""Worktree isolation per run (F006).

Every run executes inside its own git worktree at ``<repo>/.remedy-wt/<job-id>``
on its own branch ``remedy/<job-id>``. The normal checkout is never mutated, and
the result is handed back as a branch plus a deterministic ``result.diff`` — there
is NEVER an automatic merge.

Safety rules enforced here:

* job ids are validated, so a crafted id cannot escape ``.remedy-wt/``;
* a worktree or branch that belongs to a different job is refused, never reused;
* creation is idempotent only when the existing worktree matches the same job and
  the same repository;
* removal keeps the result branch by default;
* an ``fcntl`` lock under the user data area prevents two processes claiming the
  same worktree, two jobs claiming the same branch, and cleanup while another
  process owns the worktree.
"""
from __future__ import annotations

import fcntl
import hashlib
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: Where worktrees live, relative to the repository root.
WORKTREE_DIRNAME = ".remedy-wt"

#: Branch namespace for run results.
BRANCH_PREFIX = "remedy/"

#: A job id must be a plain, filesystem- and ref-safe token. This is what stops
#: ``../../etc`` or ``a/b`` from ever reaching a path or a branch name.
_SAFE_JOB_ID_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")


class WorktreeError(RuntimeError):
    """A worktree operation failed for a reason the caller must handle."""


class WorktreeLockError(WorktreeError):
    """Another process already holds this job's worktree lock."""


class WorktreeConflictError(WorktreeError):
    """The worktree or branch exists but belongs to a different job/repository."""


@dataclass
class WorktreeHandle:
    """A claimed worktree. Carries everything evidence needs about the run."""

    job_id: str
    repo_path: str            # resolved main checkout
    path: str                 # resolved worktree path
    branch: str               # remedy/<job-id>
    base_commit: str = ""     # main-checkout HEAD the worktree branched from
    head_commit: str = ""     # worktree HEAD (== base_commit until committed)
    lock_path: str = ""
    created: bool = False     # True when this call created it (vs. reattached)
    #: File descriptor of the held lock. Not serialized.
    _lock_fd: int | None = field(default=None, repr=False, compare=False)

    @property
    def relative_path(self) -> str:
        """Repository-relative worktree path — safe to put in shared evidence."""
        return f"{WORKTREE_DIRNAME}/{self.job_id}"

    def to_evidence(self) -> dict[str, Any]:
        """Shareable record: no absolute private path ever leaves this."""
        return {
            "job_id": self.job_id,
            "worktree_branch": self.branch,
            "worktree_path": self.relative_path,   # repo-relative, shareable
            "base_commit": self.base_commit,
            "worktree_head": self.head_commit,
            "lock_id": Path(self.lock_path).name if self.lock_path else "",
        }


# ---------------------------------------------------------------------------
# Validation and git plumbing
# ---------------------------------------------------------------------------

def validate_job_id(job_id: str) -> str:
    """Return the job id, or raise if it could escape a path or a ref name."""
    jid = str(job_id or "")
    if not _SAFE_JOB_ID_RE.match(jid):
        raise WorktreeError(
            f"unsafe job id {job_id!r}: must match {_SAFE_JOB_ID_RE.pattern}"
        )
    return jid


def branch_for(job_id: str) -> str:
    return f"{BRANCH_PREFIX}{validate_job_id(job_id)}"


def _git(repo: str | Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=60,
    )
    if check and proc.returncode != 0:
        raise WorktreeError(
            f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.strip()[:300]}"
        )
    return proc.stdout


def repo_root(repo_path: str | Path) -> Path:
    """Resolve the main checkout root. Raises when it is not a git repository."""
    out = _git(repo_path, "rev-parse", "--show-toplevel").strip()
    if not out:
        raise WorktreeError(f"{repo_path} is not a git repository")
    return Path(out).resolve()


def worktree_path_for(repo: str | Path, job_id: str) -> Path:
    """The worktree path for a job, validated to stay inside ``.remedy-wt/``."""
    root = Path(repo).resolve()
    base = (root / WORKTREE_DIRNAME).resolve()
    path = (base / validate_job_id(job_id)).resolve()
    # Defence in depth: even with a validated id, never return a path outside base.
    if path.parent != base:
        raise WorktreeError(f"worktree path for {job_id!r} escapes {WORKTREE_DIRNAME}/")
    return path


def is_git_repo(repo_path: str | Path) -> bool:
    try:
        repo_root(repo_path)
        return True
    except (WorktreeError, OSError):
        return False


def ensure_ignored(root: Path) -> None:
    """Make sure ``.remedy-wt/`` never shows up as a change in the main checkout.

    Written to ``.git/info/exclude`` rather than ``.gitignore``: the ignore rule
    must not itself dirty the working tree of the repository we are protecting.
    """
    git_dir = _git(root, "rev-parse", "--git-common-dir").strip()
    exclude = (Path(git_dir) if os.path.isabs(git_dir) else root / git_dir) / "info" / "exclude"
    entry = f"{WORKTREE_DIRNAME}/"
    try:
        existing = exclude.read_text(encoding="utf-8") if exclude.is_file() else ""
        if entry not in existing.split():
            exclude.parent.mkdir(parents=True, exist_ok=True)
            with exclude.open("a", encoding="utf-8") as fh:
                if existing and not existing.endswith("\n"):
                    fh.write("\n")
                fh.write(f"{entry}\n")
    except OSError:
        pass  # best effort: a read-only git dir must not fail the run


# ---------------------------------------------------------------------------
# Locking
# ---------------------------------------------------------------------------

def project_id(repo_path: str | Path) -> str:
    """Stable id for a repository, derived from its resolved path.

    Deliberately NOT F146: a short, deterministic digest is enough to give each
    checkout its own lock namespace.
    """
    resolved = str(Path(repo_path).resolve())
    return hashlib.sha256(resolved.encode()).hexdigest()[:16]


def locks_dir(repo_path: str | Path) -> Path:
    """``<data root>/projects/<project-id>/locks`` — the user data area."""
    from packages.orchestration.data_paths import projects_dir
    return projects_dir() / project_id(repo_path) / "locks"


def lock_path_for(repo_path: str | Path, job_id: str) -> Path:
    return locks_dir(repo_path) / f"{validate_job_id(job_id)}.lock"


def _acquire_lock(repo_path: str | Path, job_id: str) -> tuple[int, Path]:
    """Take an exclusive, non-blocking fcntl lock for this job's worktree."""
    path = lock_path_for(repo_path, job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as exc:
        os.close(fd)
        raise WorktreeLockError(
            f"worktree for job {job_id!r} is already claimed by another process"
        ) from exc
    os.ftruncate(fd, 0)
    os.write(fd, f"{os.getpid()}\n".encode())
    return fd, path


def release_lock(handle: WorktreeHandle) -> None:
    """Release the handle's lock. Safe to call twice."""
    fd = handle._lock_fd
    if fd is None:
        return
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    handle._lock_fd = None


# ---------------------------------------------------------------------------
# Worktree inventory
# ---------------------------------------------------------------------------

def list_worktrees(repo: str | Path) -> list[dict[str, str]]:
    """Parse ``git worktree list --porcelain`` into records."""
    out = _git(repo, "worktree", "list", "--porcelain")
    records: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in out.splitlines():
        if not line.strip():
            if cur:
                records.append(cur)
                cur = {}
            continue
        key, _, value = line.partition(" ")
        cur[key] = value
    if cur:
        records.append(cur)
    return records


def _branch_exists(repo: str | Path, branch: str) -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=str(repo), capture_output=True, text=True,
    )
    return proc.returncode == 0


def _branch_checked_out_at(repo: str | Path, branch: str) -> Path | None:
    """The worktree currently holding ``branch``, or None when nothing does."""
    ref = f"refs/heads/{branch}"
    for rec in list_worktrees(repo):
        if rec.get("branch") == ref and rec.get("worktree"):
            return Path(rec["worktree"]).resolve()
    return None


def _worktree_registered(repo: str | Path, path: Path) -> bool:
    target = str(path.resolve())
    return any(r.get("worktree") == target for r in list_worktrees(repo))


def commit_exists(repo: str | Path, sha: str) -> bool:
    if not sha:
        return False
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=str(repo), capture_output=True, text=True,
    )
    return proc.returncode == 0


def is_ancestor(repo: str | Path, ancestor: str, descendant: str) -> bool:
    """True when ``ancestor`` is in the history of ``descendant``.

    Used by recovery to prove a rediscovered branch really grew from the base
    commit the run recorded, instead of trusting the name alone.
    """
    if not (ancestor and descendant):
        return False
    proc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(repo), capture_output=True, text=True,
    )
    return proc.returncode == 0


# ---------------------------------------------------------------------------
# Public operations
# ---------------------------------------------------------------------------

def create(job_id: str, repo: str | Path) -> WorktreeHandle:
    """Claim (or re-attach to) this job's worktree and branch.

    Idempotent ONLY for the same job in the same repository: an existing worktree
    or branch that belongs to a different job is a conflict, never a silent reuse.
    """
    jid = validate_job_id(job_id)
    root = repo_root(repo)
    branch = branch_for(jid)
    path = worktree_path_for(root, jid)

    fd, lock = _acquire_lock(root, jid)
    try:
        ensure_ignored(root)
        base_commit = _git(root, "rev-parse", "HEAD").strip()
        registered = _worktree_registered(root, path)

        if path.exists() and not registered:
            # A stale directory left behind by a crash: git does not know it.
            raise WorktreeConflictError(
                f"{path} exists but is not a registered worktree; "
                f"run recover() to reconcile it"
            )

        if registered:
            # Re-attach: it must be THIS job's branch, in THIS repository.
            actual = _git(path, "rev-parse", "--abbrev-ref", "HEAD").strip()
            if actual != branch:
                raise WorktreeConflictError(
                    f"worktree {path} is on branch {actual!r}, not {branch!r}"
                )
            handle = WorktreeHandle(
                job_id=jid, repo_path=str(root), path=str(path), branch=branch,
                base_commit=base_commit, lock_path=str(lock), created=False,
                _lock_fd=fd,
            )
            handle.head_commit = snapshot(handle)
            return handle

        if _branch_exists(root, branch):
            # The branch survives cleanup by design; reuse it for the SAME job —
            # but never steal it from a worktree that is currently holding it.
            holder = _branch_checked_out_at(root, branch)
            if holder is not None and holder != path:
                raise WorktreeConflictError(
                    f"branch {branch!r} is already checked out at {holder}, "
                    f"not at this job's worktree"
                )
            _git(root, "worktree", "add", str(path), branch)
        else:
            _git(root, "worktree", "add", "-b", branch, str(path), base_commit)

        handle = WorktreeHandle(
            job_id=jid, repo_path=str(root), path=str(path), branch=branch,
            base_commit=base_commit, lock_path=str(lock), created=True,
            _lock_fd=fd,
        )
        handle.head_commit = snapshot(handle)
        return handle
    except Exception:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
        except OSError:
            pass
        raise


def snapshot(handle: WorktreeHandle) -> str:
    """Current worktree HEAD sha. Also refreshes ``handle.head_commit``."""
    sha = _git(handle.path, "rev-parse", "HEAD").strip()
    handle.head_commit = sha
    return sha
