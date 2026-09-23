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
    head_commit: str = ""     # worktree HEAD: base_commit until a job task's commit (F270) moves it
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


#: Wall-clock ceiling for a single git query in this module. A hung git — a
#: stale index.lock, a hook that prompts — otherwise blocks the unattended loop
#: forever, because the deadline budget is checked BETWEEN steps and cannot see
#: a step that never returns.
GIT_QUERY_TIMEOUT_SEC = 60


def _git(repo: str | Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=str(repo), capture_output=True, text=True,
        timeout=GIT_QUERY_TIMEOUT_SEC,
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


def worktrees_root_for(repo: str | Path) -> Path:
    """THE canonical root every job workspace must live under.

    F11 (round 11): the read-only manifest check resolves a workspace through this root and refuses
    anything outside it, so a persisted path can never become its own trust root.
    """
    return (Path(repo).resolve() / WORKTREE_DIRNAME).resolve()


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
    """Workspace key — a resolved-path digest for lock namespacing.

    F146 canonical identity rule: this is NOT a project identity. The project
    identity is the registry UUID (RemyProject.id). This function returns a
    deterministic digest of the resolved repo path, used ONLY for lock
    namespace and dev_server runtime directory. Do not add new call sites
    outside the worktree module and dev_server.project_digest — a guard
    test enforces this.
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
        timeout=GIT_QUERY_TIMEOUT_SEC,
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
        timeout=GIT_QUERY_TIMEOUT_SEC,
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
        timeout=GIT_QUERY_TIMEOUT_SEC,
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


def head_at(path: str | Path) -> str:
    """Current HEAD sha of a worktree PATH, claiming nothing (F047).

    ``snapshot`` needs a claimed handle, and ``create`` takes the job lock and
    may materialise a worktree — neither is acceptable for the read-only head
    comparison ``remedy job resume`` makes before it decides whether to run.
    Returns "" when the path is absent or is not a usable git worktree; the
    caller must treat "" as "unknown", never as "matches".
    """
    try:
        if not path or not Path(path).is_dir():
            return ""
        return _git(path, "rev-parse", "HEAD").strip()
    except (WorktreeError, OSError, subprocess.SubprocessError):
        return ""


#: The one identity of every commit Remedy lands on a job worktree branch (F270).
REMEDY_COMMIT_NAME = "Remedy"
REMEDY_COMMIT_EMAIL = "remedy@local"

#: The trailer keys naming the job and the task a Remedy job-branch commit belongs to.
REMEDY_JOB_TRAILER = "Remedy-Job"
REMEDY_TASK_TRAILER = "Remedy-Task"

#: Wall-clock ceiling for one ``git add`` or ``git commit`` in a job worktree.
GIT_COMMIT_TIMEOUT_SEC = 120


# DECISION F270 D1 (2): Remedy commits only on its own `remedy/` branches, never the operator's.
def commit_job_worktree(path: str | Path, message: str) -> str:
    """Commit a job worktree's COMPLETE current state on its branch; return the new HEAD sha.

    F270 T001, DECISION F270 D1 (1) and (2): ``git add -A .`` through the
    worktree's own index, then one commit authored AND committed by
    ``Remedy <remedy@local>`` — the identity is forced through the environment,
    so neither the operator's git configuration nor their ``GIT_AUTHOR_*`` /
    ``GIT_COMMITTER_*`` variables reach it — with no signing and no hook, because
    hooks gate the operator's commits, not a branch the operator never checks
    out. ``--allow-empty`` keeps one applied task one commit when it changed
    nothing. A checkout whose current branch does not start with
    ``BRANCH_PREFIX`` (the operator's own checkout, a detached HEAD) is refused
    with ``WorktreeError`` before anything is written.
    """
    where = str(path)
    branch = _git(where, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if not branch.startswith(BRANCH_PREFIX):
        raise WorktreeError(
            f"refusing to commit on branch {branch!r}: Remedy commits only on "
            f"its own {BRANCH_PREFIX!r} job branches"
        )
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": REMEDY_COMMIT_NAME,
        "GIT_AUTHOR_EMAIL": REMEDY_COMMIT_EMAIL,
        "GIT_COMMITTER_NAME": REMEDY_COMMIT_NAME,
        "GIT_COMMITTER_EMAIL": REMEDY_COMMIT_EMAIL,
    }
    steps = (
        ("add", ["add", "-A", "."], None),
        ("commit", ["-c", "core.hooksPath=/dev/null", "commit", "--no-verify",
                    "--no-gpg-sign", "--allow-empty", "--quiet", "-F", "-"], message),
    )
    for verb, args, stdin in steps:
        proc = subprocess.run(
            ["git", *args], cwd=where, env=env, input=stdin,
            capture_output=True, text=True, timeout=GIT_COMMIT_TIMEOUT_SEC,
        )
        if proc.returncode != 0:
            raise WorktreeError(
                f"git {verb} in the job worktree failed ({proc.returncode}): "
                f"{proc.stderr.strip()[:300]}"
            )
    return _git(where, "rev-parse", "HEAD").strip()


def read_head_remedy_trailers(path: str | Path) -> dict[str, str]:
    """The ``Remedy-Job`` and ``Remedy-Task`` trailers of a worktree's HEAD commit.

    DECISION F270 D1 (4): how a resumed run recognises the commit an interrupted
    run already made for a task. A key HEAD does not carry is absent.
    """
    out = _git(str(path), "log", "-1", "--format=%(trailers:only,unfold)", "HEAD")
    found: dict[str, str] = {}
    for line in out.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() in (REMEDY_JOB_TRAILER, REMEDY_TASK_TRAILER):
            found[key.strip()] = value.strip()
    return found


def worktree_matches_head(path: str | Path) -> bool:
    """True when the worktree holds no change against its HEAD commit (F270 D1 (4))."""
    return not _git(str(path), "status", "--porcelain", "--untracked-files=all").strip()


def diff(handle: WorktreeHandle) -> str:
    """Deterministic, repository-relative diff of everything the run changed.

    Covers tracked edits AND new files (``--intent-to-add`` staging of untracked
    paths), so a run that only adds files still produces a real diff. Paths are
    repository-relative because git emits them that way.
    """
    # Register untracked files so they appear in the diff, without committing.
    _git(handle.path, "add", "--intent-to-add", "--all", check=False)
    text = _git(
        handle.path, "diff", "--no-color", "--no-ext-diff", "--src-prefix=a/",
        "--dst-prefix=b/", "HEAD",
    )
    return text


def write_result_diff(handle: WorktreeHandle, out_path: str | Path) -> dict[str, Any]:
    """Persist ``result.diff`` and return its sha256/size for evidence."""
    text = diff(handle)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    out.write_bytes(data)
    return {
        "path": out.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "empty": not text.strip(),
    }


def retain_for_recovery(handle: WorktreeHandle, reason: str = "") -> dict[str, Any]:
    """Keep the worktree — and whatever it holds past its branch tip — for a later recovery.

    The git worktree stays registered and the branch stays put; only the
    in-process fcntl lock is released, so a later ``recover()`` (from
    ``remedy job resume``) can claim it. This call commits nothing and merges
    nothing: it is the safe end state whenever the branch-plus-diff hand-off
    could NOT be persisted, because a run's changes past the branch tip — all
    of a single run's, and a job task's that never reached its F270 commit —
    exist only in the worktree.
    """
    release_lock(handle)
    return {
        "worktree_removed": False,
        "branch": handle.branch,
        "branch_kept": True,
        "worktree_retained": True,
        "cleanup_status": "failed_recoverable" if reason else "retained",
        "cleanup_error": reason,
    }


def write_tree(handle: WorktreeHandle) -> str:
    """Deterministic tree object for the worktree's COMPLETE current state.

    Includes untracked files. Uses a private temporary index (``GIT_INDEX_FILE``),
    so the worktree's real index is never touched, nothing is committed, no branch
    moves and nothing is ever merged. Two such trees, taken before and after a
    task, give an exact task-local diff without a commit — and without ever
    comparing filesystem timestamps.

    R-0974: the temporary index is seeded from ``HEAD`` first, so a TRACKED file
    that ``.gitignore`` matches stays in the snapshot; ``git add -A`` into an empty
    index skips every ignored path, tracked or not.
    """
    return write_tree_at(handle.path)


def write_tree_at(path: str | Path) -> str:
    """``write_tree`` for any git checkout, a job worktree or the target itself.

    F263 T001 takes the TARGET checkout's tree with it, which is why the body
    lives here and not behind a ``WorktreeHandle``: the target has no handle.
    """
    import tempfile

    fd, tmp = tempfile.mkstemp(prefix="remedy-index-")
    os.close(fd)
    os.unlink(tmp)                       # git wants to create it itself
    env = {**os.environ, "GIT_INDEX_FILE": tmp}
    try:
        proc = subprocess.run(
            ["git", "read-tree", "HEAD"], cwd=str(path), env=env,
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            raise WorktreeError(f"git read-tree for tree snapshot failed: {proc.stderr[:200]}")
        proc = subprocess.run(
            ["git", "add", "-A", "."], cwd=str(path), env=env,
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            raise WorktreeError(f"git add for tree snapshot failed: {proc.stderr[:200]}")
        proc = subprocess.run(
            ["git", "write-tree"], cwd=str(path), env=env,
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            raise WorktreeError(f"git write-tree failed: {proc.stderr[:200]}")
        return proc.stdout.strip()
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def diff_trees(handle: WorktreeHandle, before: str, after: str) -> str:
    """Deterministic, repository-relative diff between two tree objects."""
    return _git(
        handle.path, "diff", "--no-color", "--no-ext-diff", "--src-prefix=a/",
        "--dst-prefix=b/", before, after,
    )


def changed_files_between(handle: WorktreeHandle, before: str, after: str) -> list[str]:
    out = _git(handle.path, "diff", "--name-only", before, after)
    return sorted(line.strip() for line in out.splitlines() if line.strip())


def blob_at(handle: WorktreeHandle, tree: str, rel_path: str) -> bytes | None:
    """Contents of ``rel_path`` in ``tree``, or None when it did not exist."""
    proc = subprocess.run(
        ["git", "show", f"{tree}:{rel_path}"], cwd=handle.path,
        capture_output=True, timeout=60,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def write_tree_diff(
    handle: WorktreeHandle, before: str, after: str, out_path: str | Path,
) -> dict[str, Any]:
    """Persist a tree-to-tree diff and return its sha256/size for evidence."""
    text = diff_trees(handle, before, after)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    out.write_bytes(data)
    return {
        "path": out.name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "empty": not text.strip(),
    }


# ---------------------------------------------------------------------------
# Checkpoint refs — keep an active tree object alive across git gc/prune
# ---------------------------------------------------------------------------

#: Private Remedy ref namespace. These are CHECKPOINTS, never result branches:
#: nothing is ever committed to them, merged from them or pushed.
CHECKPOINT_REF_PREFIX = "refs/remedy/checkpoints"

_SAFE_REF_COMPONENT_RE = re.compile(r"\A[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")


def validate_ref_component(part: str) -> str:
    if not _SAFE_REF_COMPONENT_RE.match(str(part or "")):
        raise WorktreeError(f"unsafe ref component {part!r}")
    return part


def checkpoint_ref(job_id: str, name: str, task_id: str = "") -> str:
    """``refs/remedy/checkpoints/job-<id>/job-initial`` or ``/tasks/<T>-start``."""
    validate_ref_component(job_id)
    validate_ref_component(name)
    if task_id:
        validate_ref_component(task_id)
        return f"{CHECKPOINT_REF_PREFIX}/{job_id}/tasks/{task_id}-{name}"
    return f"{CHECKPOINT_REF_PREFIX}/{job_id}/{name}"


def set_checkpoint_ref(repo: str | Path, ref: str, sha: str) -> None:
    """Point a checkpoint ref at a tree object, atomically (``git update-ref``).

    A raw tree SHA in job.json is NOT a durable checkpoint: an uncommitted job
    state is unreachable from any branch, so ``git gc``/``git prune`` will collect
    it. The ref makes the object reachable — without moving a branch, committing
    or merging anything.
    """
    if not ref.startswith(CHECKPOINT_REF_PREFIX + "/"):
        raise WorktreeError(f"refusing to write non-checkpoint ref {ref!r}")
    _git(repo, "update-ref", ref, sha)


def resolve_checkpoint_ref(repo: str | Path, ref: str) -> str:
    """The object the ref points at, or "" when the ref does not exist."""
    proc = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", ref],
        cwd=str(repo), capture_output=True, text=True,
        timeout=GIT_QUERY_TIMEOUT_SEC,
    )
    return proc.stdout.strip() if proc.returncode == 0 else ""


def delete_checkpoint_ref(repo: str | Path, ref: str) -> str:
    """Drop an obsolete checkpoint ref. Returns "" or an error string."""
    if not ref.startswith(CHECKPOINT_REF_PREFIX + "/"):
        return f"refusing to delete non-checkpoint ref {ref!r}"
    proc = subprocess.run(
        ["git", "update-ref", "-d", ref], cwd=str(repo),
        capture_output=True, text=True, timeout=GIT_QUERY_TIMEOUT_SEC,
    )
    if proc.returncode != 0:
        return proc.stderr.strip()[:200]
    return ""


def object_exists(repo: str | Path, sha: str) -> bool:
    if not sha:
        return False
    proc = subprocess.run(
        ["git", "cat-file", "-e", sha], cwd=str(repo),
        capture_output=True, text=True, timeout=GIT_QUERY_TIMEOUT_SEC,
    )
    return proc.returncode == 0


def mode_at(handle: WorktreeHandle, tree: str, rel_path: str) -> str:
    """The git file mode of ``rel_path`` in ``tree`` ("100644"/"100755"), or ""."""
    if not (tree and rel_path):
        return ""
    out = _git(handle.path, "ls-tree", tree, "--", rel_path, check=False)
    if not out.strip():
        return ""
    return out.split()[0]


def file_mode(path: str | Path) -> str:
    """Normalized git mode of a real file: executable bit only."""
    p = Path(path)
    if p.is_symlink():
        return "120000"
    return "100755" if os.access(p, os.X_OK) else "100644"


def remove(handle: WorktreeHandle, *, keep_branch: bool = True) -> dict[str, Any]:
    """Remove the physical worktree. The result branch is KEPT by default.

    There is never an automatic merge: the branch is the hand-off.

    The handle's lock is released on EVERY exit (``try/finally``): a git command
    that blows up half way through must not leave the run id permanently
    unclaimable, or recovery could never reach the worktree it left behind.
    Cleanup is only ever reported ``clean`` when the directory is gone AND git no
    longer has it registered.
    """
    root = Path(handle.repo_path)
    path = Path(handle.path)
    removed = False
    branch_kept = True
    error = ""

    try:
        if _worktree_registered(root, path):
            _git(root, "worktree", "remove", "--force", str(path), check=False)
            removed = True
        _git(root, "worktree", "prune", check=False)
        if path.exists():
            import shutil
            shutil.rmtree(path)          # raises: a failed delete is not a clean run
        if not keep_branch:
            _git(root, "branch", "-D", handle.branch, check=False)
            branch_kept = False
    except Exception as exc:  # noqa: BLE001 — cleanup failure is reported through the result's error field, not raised
        error = f"{type(exc).__name__}: {exc}"
    finally:
        release_lock(handle)             # always claimable again

    still_there = True
    still_registered = True
    if not error:
        try:
            still_there = path.exists()
            still_registered = _worktree_registered(root, path)
        except Exception as exc:  # noqa: BLE001 — verification failure is reported as a cleanup error
            error = f"cleanup verification failed: {type(exc).__name__}: {exc}"
    if not error:
        if still_there:
            error = f"worktree directory {path} still exists after removal"
        elif still_registered:
            error = f"worktree {path} is still registered with git after removal"

    return {
        "worktree_removed": removed and not error,
        "branch": handle.branch,
        "branch_kept": branch_kept,
        "cleanup_status": "failed" if error else "clean",
        "cleanup_error": error,
    }


def recover(job_id: str, repo: str | Path) -> WorktreeHandle | None:
    """Rediscover an interrupted run's worktree so it can be resumed or cleaned.

    Returns a handle when a worktree or its branch still exists, else None. Never
    creates a DIFFERENT branch: recovery is only ever for this job's own branch.
    """
    jid = validate_job_id(job_id)
    root = repo_root(repo)
    branch = branch_for(jid)
    path = worktree_path_for(root, jid)

    registered = _worktree_registered(root, path)
    exists = path.exists()
    has_branch = _branch_exists(root, branch)
    if not (registered or exists or has_branch):
        return None

    if exists and not registered:
        # Stale directory from a crash: let git re-adopt or drop it.
        _git(root, "worktree", "prune", check=False)
        registered = _worktree_registered(root, path)

    fd, lock = _acquire_lock(root, jid)
    handle = WorktreeHandle(
        job_id=jid, repo_path=str(root), path=str(path), branch=branch,
        base_commit=_git(root, "rev-parse", "HEAD").strip(),
        lock_path=str(lock), created=False, _lock_fd=fd,
    )
    if registered:
        try:
            actual = _git(path, "rev-parse", "--abbrev-ref", "HEAD").strip()
            if actual != branch:
                raise WorktreeConflictError(
                    f"recovered worktree {path} is on {actual!r}, not {branch!r}"
                )
            handle.head_commit = snapshot(handle)
        except Exception:
            release_lock(handle)      # never strand the lock on a failed recovery
            raise
    return handle
