"""The working tree at invocation is the baseline (operator amendment amend1014b, DECISION D5, D6).

A target repository need not be clean for `remedy do`. At command start this module captures what
the person can SEE of the paths the job may change (its deliverables): their bytes, executable bit
or symlink target, or absence. The job's isolated workspace is then seeded from those bytes and
committed on the job's own branch, so the proposed result is the delta from that start state and
not from `HEAD`, and the apply compares the target against the same bytes.

Every OTHER dirty path (an unrelated source file, an untracked `.env`, a private key) is preserved
dirt: only its name is recorded. Remedy deliberately does not open it, copy it into the workspace
or store it in a Git object, because the workspace is exposed to the agent and the job branch
persists; sensitive paths are decided by name alone (`sensitive_paths`), never by `.gitignore`.

Remedy deliberately does NOT stash, reset, check out target paths, commit, or touch the target's
index to build this baseline: it only reads the target, and every write lands in the job
workspace. A state the capture cannot represent exactly (an unmerged path, a submodule or nested
repository, a special file, a very large dirty set) is refused with the actual reason; the old
"commit or stash first" answer is kept only for the history merge, which cannot carry a baseline.
"""
from __future__ import annotations

import hashlib
import os
import stat
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.sensitive_paths import sensitive_path_category

#: Bounds, so a repository with a huge dirty set is refused instead of copied into a workspace.
MAX_BASELINE_PATHS = 500
MAX_BASELINE_FILE_BYTES = 10 * 1024 * 1024
MAX_BASELINE_TOTAL_BYTES = 100 * 1024 * 1024
#: `git status` XY pairs that mean an unresolved merge.
_UNMERGED = frozenset({"DD", "AU", "UD", "UA", "DU", "AA", "UU"})
_GITLINK_MODE = "160000"
#: The commit identity of the baseline commit on the job's own branch; never the target's.
_BASELINE_COMMIT_ARGS = ("-c", "user.name=remedy", "-c", "user.email=remedy@localhost",
                         "-c", "commit.gpgsign=false")


class DirtyBaselineUnsupported(RuntimeError):
    """The target holds a state the baseline cannot represent exactly; the message says which."""


@dataclass(frozen=True)
class BaselineEntry:
    """One dirty path as the person sees it: a file, a symlink, or absent."""

    path: str
    kind: str                # "file" | "symlink" | "absent"
    sha256: str = ""         # of the bytes, or of the link target text
    executable: bool = False
    content: bytes = b""     # held in memory for the seed; never serialized

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "kind": self.kind, "sha256": self.sha256,
                "executable": self.executable}


@dataclass(frozen=True)
class DirtyBaseline:
    """The captured start state: HEAD, branch, and the dirty paths with their bytes."""

    head: str
    branch: str
    entries: tuple[BaselineEntry, ...]
    digest: str
    #: ``(path, category)`` of each dirty path left alone; the category is "" for ordinary paths.
    preserved: tuple[tuple[str, str], ...] = ()

    @property
    def paths(self) -> list[str]:
        return [e.path for e in self.entries]

    def to_dict(self) -> dict[str, Any]:
        return {"head": self.head, "branch": self.branch, "digest": self.digest,
                "entries": [e.to_dict() for e in self.entries],
                "preserved": [{"path": p, "category": c} for p, c in self.preserved]}


def _git(repo: str | Path, *args: str) -> bytes:
    done = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, timeout=60, check=False)
    if done.returncode != 0:
        raise DirtyBaselineUnsupported(
            f"git {args[0]} failed in the target ({done.stderr.decode('utf-8', 'replace').strip()[:150]}), "
            f"so its working tree cannot be captured.")
    return done.stdout


def _status_entries(repo: str | Path) -> list[tuple[str, str]]:
    """``(XY, path)`` for every path `git status` lists; a rename lists both of its paths."""
    raw = _git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    fields = raw.split(b"\0")
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(fields):
        item = fields[i]
        i += 1
        if len(item) < 4:
            continue
        xy, path = item[:2].decode("ascii", "replace"), item[3:].decode("utf-8", "surrogateescape")
        out.append((xy, path))
        if "R" in xy or "C" in xy:           # the next field is the rename's original path
            if i < len(fields) and fields[i]:
                out.append((" D", fields[i].decode("utf-8", "surrogateescape")))
            i += 1
    return out


def _is_remedy_owned(repo: Path, rel: str) -> bool:
    """Remedy's own artifacts and tool-cache noise are not the person's source."""
    from packages.orchestration.human_change import _classify

    return _classify(repo, rel) != "content"


def _check_representable(repo: Path, rel: str) -> os.stat_result | None:
    """lstat of *rel* (None when absent); raises when a baseline could never represent it. Opens nothing."""
    try:
        info = os.lstat(repo / rel)
    except FileNotFoundError:
        return None
    if stat.S_ISDIR(info.st_mode):
        raise DirtyBaselineUnsupported(
            f"{rel} is a directory that is a nested repository or submodule; a baseline cannot "
            f"represent it, so commit or remove it first.")
    if not (stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)):
        raise DirtyBaselineUnsupported(f"{rel} is a special file (not a regular file or symlink), "
                                       f"which a baseline cannot represent.")
    return info


def _read_entry(repo: Path, rel: str) -> BaselineEntry:
    """Read one deliverable path's bytes; only ever called for a path that is not sensitive."""
    info = _check_representable(repo, rel)
    if info is None:
        return BaselineEntry(rel, "absent")
    full = repo / rel
    if stat.S_ISLNK(info.st_mode):
        target = os.readlink(full)
        return BaselineEntry(rel, "symlink", hashlib.sha256(target.encode("utf-8", "surrogateescape")).hexdigest(),
                             content=target.encode("utf-8", "surrogateescape"))
    if info.st_size > MAX_BASELINE_FILE_BYTES:
        raise DirtyBaselineUnsupported(
            f"{rel} is {info.st_size} bytes, over the {MAX_BASELINE_FILE_BYTES}-byte limit for a "
            f"file in a captured baseline.")
    data = full.read_bytes()
    return BaselineEntry(rel, "file", hashlib.sha256(data).hexdigest(),
                         executable=bool(info.st_mode & stat.S_IXUSR), content=data)


def _gitlink_paths(repo: Path, paths: list[str]) -> list[str]:
    if not paths:
        return []
    listing = _git(repo, "ls-files", "-s", "-z", "--", *paths).split(b"\0")
    return [rec.split(b"\t", 1)[1].decode("utf-8", "surrogateescape")
            for rec in listing if rec.startswith(_GITLINK_MODE.encode()) and b"\t" in rec]


def _digest(head: str, branch: str, entries: list[BaselineEntry]) -> str:
    h = hashlib.sha256(f"{head}\n{branch}\n".encode())
    for e in sorted(entries, key=lambda x: x.path):
        h.update(f"{e.path}\0{e.kind}\0{e.sha256}\0{int(e.executable)}\n".encode("utf-8", "surrogateescape"))
    return h.hexdigest()


def _normal_path(path: str) -> str:
    return os.path.normpath(path.replace("\\", "/")) if path.strip() else ""


def capture_dirty_baseline(repo_path: str | Path, deliverables: Iterable[str] = ()) -> DirtyBaseline:
    """Capture the dirty state of the job's *deliverables*; raises DirtyBaselineUnsupported with the reason.

    Reads only: no stash, no reset, no checkout, no index write. A dirty deliverable that is not
    sensitive becomes a seeded entry (its bytes are read); every other dirty path is listed as
    preserved by name and is never opened. No deliverables means nothing is seeded.
    """
    repo = Path(repo_path)
    head = _git(repo, "rev-parse", "HEAD").decode().strip()
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").decode().strip()
    listed = _status_entries(repo)
    unmerged = sorted({p for xy, p in listed if xy in _UNMERGED})
    if unmerged:
        raise DirtyBaselineUnsupported(
            f"The target has unresolved merge conflicts in {', '.join(unmerged[:5])}; resolve them first.")
    paths = sorted({p for _xy, p in listed if not _is_remedy_owned(repo, p)})
    if len(paths) > MAX_BASELINE_PATHS:
        raise DirtyBaselineUnsupported(
            f"The target has {len(paths)} uncommitted paths, over the {MAX_BASELINE_PATHS} a "
            f"captured baseline can hold; commit most of them first.")
    gitlinks = _gitlink_paths(repo, paths)
    if gitlinks:
        raise DirtyBaselineUnsupported(
            f"The target has changes in the submodule {', '.join(gitlinks[:3])}, which a baseline "
            f"cannot represent.")
    wanted = {_normal_path(d) for d in deliverables}
    seeded = [p for p in paths if _normal_path(p) in wanted and not sensitive_path_category(p)]
    for rel in paths:
        _check_representable(repo, rel)                       # lstat only: no path is opened here
    entries = [_read_entry(repo, p) for p in seeded]
    total = sum(len(e.content) for e in entries)
    if total > MAX_BASELINE_TOTAL_BYTES:
        raise DirtyBaselineUnsupported(
            f"The target's uncommitted files hold {total} bytes, over the {MAX_BASELINE_TOTAL_BYTES} "
            f"a captured baseline can hold.")
    preserved = tuple((p, sensitive_path_category(p)) for p in paths if p not in seeded)
    return DirtyBaseline(head=head, branch=branch, entries=tuple(entries),
                         digest=_digest(head, branch, entries), preserved=preserved)


def _safe_destination(workspace: Path, rel: str) -> Path:
    if os.path.isabs(rel) or ".." in Path(rel).parts or Path(rel).parts[:1] == (".git",):
        raise DirtyBaselineUnsupported(f"{rel} is not a path a baseline may write into a workspace.")
    return workspace / rel


def seed_workspace_from_baseline(baseline: DirtyBaseline, workspace: str | Path) -> bool:
    """Write the baseline into the job workspace and commit it on the job's own branch.

    Returns True when a baseline commit was made. After it, the workspace's HEAD IS the start
    state, so `git diff HEAD` is the delta the job made. The commit uses Remedy's identity and
    skips hooks: it is bookkeeping on a branch Remedy owns, not the person's history.
    """
    ws = Path(workspace)
    for e in baseline.entries:
        dest = _safe_destination(ws, e.path)
        if e.kind == "absent":
            if dest.is_symlink() or dest.exists():
                dest.unlink()
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_symlink() or dest.exists():
            dest.unlink()
        if e.kind == "symlink":
            os.symlink(e.content.decode("utf-8", "surrogateescape"), dest)
            continue
        dest.write_bytes(e.content)
        mode = dest.stat().st_mode
        dest.chmod(mode | stat.S_IXUSR if e.executable else mode & ~(stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    if not baseline.entries:
        return False
    # Only the seeded deliverable paths are staged; a path the person deleted is un-staged by name
    # (and a path that never existed in the workspace is not an error).
    present = [e.path for e in baseline.entries if e.kind != "absent"]
    gone = [e.path for e in baseline.entries if e.kind == "absent"]
    for args, names in ((["add", "-A"], present), (["rm", "-r", "-q", "--cached", "--ignore-unmatch"], gone)):
        if names:
            subprocess.run(["git", *args, "--", *names], cwd=str(ws), capture_output=True, check=True, timeout=60)
    quiet = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(ws), check=False, timeout=60)
    if quiet.returncode == 0:
        return False
    subprocess.run(["git", *_BASELINE_COMMIT_ARGS, "commit", "-q", "--no-verify", "-m",
                    f"remedy: working-tree baseline {baseline.digest[:12]}"],
                   cwd=str(ws), capture_output=True, check=True, timeout=60)
    return True


def baseline_drift(repo_path: str | Path, recorded: dict[str, Any]) -> list[str]:
    """What moved in the target since the baseline was captured, as named reasons; [] when nothing.

    Checks the repository property that matters to a commit (HEAD and the branch) and each
    captured path. Reads only.
    """
    repo = Path(repo_path)
    moved: list[str] = []
    try:
        head = _git(repo, "rev-parse", "HEAD").decode().strip()
        branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").decode().strip()
    except DirtyBaselineUnsupported as exc:
        return [str(exc)]
    if head != recorded.get("head"):
        moved.append(f"HEAD moved from {str(recorded.get('head'))[:12]} to {head[:12]}")
    if branch != recorded.get("branch"):
        moved.append(f"the branch changed from {recorded.get('branch')} to {branch}")
    for item in recorded.get("entries", []):
        try:
            now = _read_entry(repo, item["path"])
        except DirtyBaselineUnsupported:
            moved.append(item["path"])
            continue
        if (now.kind, now.sha256, now.executable) != (item["kind"], item["sha256"], item["executable"]):
            moved.append(item["path"])
    return moved


def job_start_baseline(job: Any) -> dict[str, Any]:
    """The dirty start a job recorded (no file bytes), or {} for a job that started clean.

    It lives inside the job's `target_last_known` record, so no job field or serializer grew.
    """
    return (getattr(job, "target_last_known", None) or {}).get("start_baseline") or {}


def job_deliverable_paths(job: Any) -> tuple[list[str], list[str]]:
    """``(declared, named)`` repository paths the job may change.

    *declared* are the tasks' recorded deliverables and `files_hint` entries: explicit targets,
    which a sensitive path may never be. *named* are path-like tokens in the task text; they only
    widen what a dirty file may be seeded, and a sensitive one among them is simply skipped.
    """
    from packages.orchestration.task_deliverables import explicit_order_paths, task_deliverable

    declared: list[str] = []
    named: list[str] = []
    for task in getattr(job, "tasks", None) or []:
        plan_hints = (task.inputs.get("plan") or {}).get("files_hint") or []
        for raw in [task_deliverable(task), *task.files_hint, *plan_hints]:
            raw = str(raw).strip()
            if raw:
                declared.extend(explicit_order_paths(raw) if " " in raw else [raw])
        named.extend(explicit_order_paths(" ".join([task.title, task.body, task.acceptance])))
    return list(dict.fromkeys(declared)), list(dict.fromkeys(named))


def sensitive_target_refusal(paths: Iterable[str]) -> str:
    """The one sentence refusing a job whose declared target is a sensitive path, else "". Names the category only."""
    for rel in paths:
        if category := sensitive_path_category(rel):
            return (f"The order targets {rel}, {category}. Remedy does not let a job read or "
                    f"change such a path, so nothing was run and nothing was copied.")
    return ""


def seed_job_workspace(job: Any, handle: Any, baseline: DirtyBaseline) -> None:
    """Seed the job's worktree from the captured deliverables and record the start on the job.

    Nothing is recorded for a clean target. A target with only preserved dirt records the names
    (no commit), so the apply report can say what it left alone.
    """
    from packages.orchestration import worktrees as W

    if not baseline.entries and not baseline.preserved:
        return
    commit = ""
    if seed_workspace_from_baseline(baseline, handle.path):
        commit = W.snapshot(handle)
        job.worktree_head = commit
    job.target_last_known = {"start_baseline": {**baseline.to_dict(), "commit": commit}}


def create_seeded_worktree(job: Any, worktree_id: str) -> Any:
    """Create the job's worktree and record it on the job, seeded from its dirty deliverables only.

    The checks come first, so a sensitive target or a state the capture cannot represent leaves
    no worktree behind.
    """
    from packages.orchestration import worktrees as W

    declared, named = job_deliverable_paths(job)
    if refusal := sensitive_target_refusal(declared):
        raise DirtyBaselineUnsupported(refusal)
    baseline = capture_dirty_baseline(job.repo_path, [*declared, *named])
    handle = W.create(worktree_id, job.repo_path)
    job.isolation_mode = "worktree"
    job.worktree_branch = handle.branch
    job.worktree_path = handle.relative_path
    job.worktree_base_commit = handle.base_commit
    job.worktree_head = handle.head_commit
    job.worktree_cleanup_status = "active"
    seed_job_workspace(job, handle, baseline)
    return handle
