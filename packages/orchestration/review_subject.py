"""The REVIEW SUBJECT — what change is actually being presented for review.

Round 14 taught the Evidence layer that a COMMITTED change is still the change under review, via
`REMEDY_REVIEW_BASE`. It did so with three lines inline in `job_evidence`, and independent review
found what that cost:

* an invalid base (`git diff NO_SUCH_BASE..HEAD` -> exit 128) was SILENTLY IGNORED: the subject
  quietly became "just the dirty files", so a typo in the base produced a smaller review than the
  operator asked for, with no error anywhere;
* a NON-ANCESTOR base was accepted, so `git diff foreign..HEAD` dragged unrelated files
  (`other.txt`) into the subject — a review of work nobody did on this branch;
* a committed DELETION could never be proven, because the proof only hashed files that still
  exist. The path was in the subject and absent from every proof set;
* nothing about the base was RECORDED, so no reader could check which base a package was built
  against;
* and the only test of the algorithm re-implemented it, which tests the copy, not the product.

So the subject is one typed, verified object, resolved by one helper, recorded as a durable fact:

    ReviewSubjectV1(subject_v, base_commit, head_commit, base_is_ancestor, commits, files)

The environment may SUPPLY the base; the resolved full SHA is what becomes the fact. An invalid or
non-ancestral base is a blocking Evidence error, never a silent downgrade.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: The environment variable that SUPPLIES the declared base. It is read in exactly one place — the
#: resolver below — so no module can invent its own view of the subject.
REVIEW_BASE_ENV = "REMEDY_REVIEW_BASE"

SUBJECT_VERSION = 1

#: `git diff --name-status -z` status letters we model explicitly.
STATUS_ADDED = "added"
STATUS_MODIFIED = "modified"
STATUS_DELETED = "deleted"
STATUS_RENAMED = "renamed"
STATUS_COPIED = "copied"
STATUS_TYPE_CHANGED = "type_changed"
STATUS_DIRTY = "dirty"

_GIT_STATUS_MAP = {
    "A": STATUS_ADDED,
    "M": STATUS_MODIFIED,
    "D": STATUS_DELETED,
    "R": STATUS_RENAMED,
    "C": STATUS_COPIED,
    "T": STATUS_TYPE_CHANGED,
}

_TIMEOUT = 30


class ReviewSubjectError(Exception):
    """The declared review subject cannot be trusted. Never downgraded to a warning."""


@dataclass(frozen=True)
class ReviewFileV1:
    """One file in the review subject, with the proof its status allows.

    A deleted file has no current content — that is the POINT of recording it, not a reason to
    drop it. `base_sha256` is its tombstone: what it was before it was removed.
    """
    path: str
    status: str
    base_sha256: str | None = None
    current_sha256: str | None = None
    old_path: str | None = None

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {"path": self.path, "status": self.status,
                               "base_sha256": self.base_sha256,
                               "current_sha256": self.current_sha256}
        if self.old_path is not None:
            out["old_path"] = self.old_path
        return out


@dataclass(frozen=True)
class ReviewCommitV1:
    """One commit on the base-exclusive ancestry path to HEAD."""
    commit: str
    parents: tuple[str, ...]
    tree: str
    subject: str
    changed_files: tuple[str, ...]
    patch_sha256: str

    def to_json(self) -> dict[str, Any]:
        return {"commit": self.commit, "parents": list(self.parents), "tree": self.tree,
                "subject": self.subject, "changed_files": list(self.changed_files),
                "patch_sha256": self.patch_sha256}


@dataclass(frozen=True)
class ReviewSubjectV1:
    """The typed, verified account of what is being reviewed."""
    base_commit: str = ""
    head_commit: str = ""
    base_is_ancestor: bool = False
    commits: tuple[ReviewCommitV1, ...] = ()
    files: tuple[ReviewFileV1, ...] = field(default_factory=tuple)
    subject_v: int = SUBJECT_VERSION

    @property
    def declared(self) -> bool:
        """True when a base was declared — i.e. committed work is part of the subject."""
        return bool(self.base_commit)

    def paths(self) -> list[str]:
        return sorted({f.path for f in self.files})

    def to_json(self) -> dict[str, Any]:
        return {"subject_v": self.subject_v, "base_commit": self.base_commit,
                "head_commit": self.head_commit, "base_is_ancestor": self.base_is_ancestor,
                "commits": [c.to_json() for c in self.commits],
                "files": [f.to_json() for f in self.files]}


def _git(repo_root: str | Path, args: list[str], *, binary: bool = False):
    return subprocess.run(["git", *args], cwd=str(repo_root), capture_output=True,
                          text=not binary, timeout=_TIMEOUT)


def _sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _sha256_blob(repo_root: str | Path, rev: str, path: str) -> str | None:
    """The content hash of a path AS OF a commit — the only way to prove a deleted file."""
    r = _git(repo_root, ["show", f"{rev}:{path}"], binary=True)
    if r.returncode != 0:
        return None
    return hashlib.sha256(r.stdout).hexdigest()


def _split_nul(raw: str) -> list[str]:
    return [p for p in raw.split("\0") if p != ""]


def _committed_records(repo_root: str | Path, base: str, head: str) -> list[ReviewFileV1]:
    """The committed delta, from ONE canonical git command.

    `--name-status -z` is NUL-delimited, so a path containing a space, a newline or a quote comes
    back intact; parsing git's human-formatted output would corrupt exactly those paths.
    """
    r = _git(repo_root, ["diff", "--name-status", "-z", "--find-renames", f"{base}..{head}"])
    if r.returncode != 0:
        raise ReviewSubjectError(
            f"cannot read the committed delta {base}..{head}: {r.stderr.strip()[:200]}")
    fields = _split_nul(r.stdout)
    out: list[ReviewFileV1] = []
    i = 0
    while i < len(fields):
        code = fields[i]
        letter = code[0]
        status = _GIT_STATUS_MAP.get(letter)
        if status is None:
            raise ReviewSubjectError(f"unsupported git status {code!r} in the committed delta")
        if letter in ("R", "C"):
            # Rename/copy carry BOTH paths: <code>\0<old>\0<new>
            if i + 2 >= len(fields):
                raise ReviewSubjectError(f"malformed rename record near {code!r}")
            old_path, new_path = fields[i + 1], fields[i + 2]
            i += 3
            out.append(ReviewFileV1(
                path=new_path, status=status, old_path=old_path,
                base_sha256=_sha256_blob(repo_root, base, old_path),
                current_sha256=_sha256_blob(repo_root, head, new_path)))
            continue
        if i + 1 >= len(fields):
            raise ReviewSubjectError(f"malformed status record near {code!r}")
        path = fields[i + 1]
        i += 2
        out.append(ReviewFileV1(
            path=path, status=status,
            base_sha256=(None if letter == "A" else _sha256_blob(repo_root, base, path)),
            current_sha256=(None if letter == "D"
                            else _sha256_blob(repo_root, head, path))))
    return out


def _dirty_records(repo_root: str | Path) -> list[ReviewFileV1]:
    """Uncommitted changes, NUL-safe, hashed from the working tree."""
    r = _git(repo_root, ["status", "--porcelain", "-z", "-u"])
    if r.returncode != 0:
        return []
    out: list[ReviewFileV1] = []
    fields = r.stdout.split("\0")
    i = 0
    while i < len(fields):
        entry = fields[i]
        i += 1
        if not entry.strip():
            continue
        code, path = entry[:2], entry[3:]
        if code[0] in ("R", "C"):
            # porcelain -z puts the ORIGIN path in the next field for a rename.
            if i < len(fields):
                i += 1
        if not path:
            continue
        full = Path(repo_root) / path
        exists = full.is_file()
        out.append(ReviewFileV1(
            path=path,
            status=STATUS_DELETED if not exists else STATUS_DIRTY,
            base_sha256=None,
            current_sha256=_sha256_file(full) if exists else None))
    return out


def resolve_review_subject(repo_root: str | Path,
                           declared_base: str | None = None) -> ReviewSubjectV1:
    """THE review-subject resolver. Every consumer calls this; nobody re-implements it.

    `declared_base` defaults to the `REMEDY_REVIEW_BASE` environment value. When no base is
    declared the subject is the dirty tree exactly as it was before round 14 — a documented,
    unchanged legacy path, so an ordinary job is untouched.

    When a base IS declared it is VERIFIED, because a review is worthless if nobody knows what it
    is a review OF:

    * `git rev-parse --verify <base>^{commit}` — an unresolvable base raises rather than silently
      shrinking the subject to the dirty tree;
    * `git merge-base --is-ancestor <base> HEAD` — a non-ancestral base raises rather than pulling
      unrelated branches' files into the review.
    """
    root = Path(repo_root)
    base_in = declared_base if declared_base is not None else os.environ.get(REVIEW_BASE_ENV, "")
    base_in = (base_in or "").strip()

    inside = _git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside.returncode != 0:
        if base_in:
            raise ReviewSubjectError(
                f"a review base ({base_in!r}) was declared but {root} is not a git work tree")
        return ReviewSubjectV1()

    dirty = _dirty_records(root)
    if not base_in:
        # The documented legacy path: no declared base, no committed delta, no base/head facts.
        return ReviewSubjectV1(files=tuple(dirty))

    resolved = _git(root, ["rev-parse", "--verify", f"{base_in}^{{commit}}"])
    if resolved.returncode != 0:
        raise ReviewSubjectError(
            f"the declared review base {base_in!r} does not resolve to a commit: "
            f"{resolved.stderr.strip()[:200]}")
    base = resolved.stdout.strip()

    head_r = _git(root, ["rev-parse", "--verify", "HEAD^{commit}"])
    if head_r.returncode != 0:
        raise ReviewSubjectError("HEAD does not resolve to a commit")
    head = head_r.stdout.strip()

    if _git(root, ["merge-base", "--is-ancestor", base, head]).returncode != 0:
        raise ReviewSubjectError(
            f"the declared review base {base[:12]} is not an ancestor of HEAD {head[:12]}: its "
            f"delta would carry files from work that is not on this branch")

    committed = _committed_records(root, base, head)
    commits = resolve_commit_chain(root, base, head)

    # A path may be both committed and dirty; the working tree is the later truth, so it wins,
    # but the committed record's base_sha256 is kept — the file's history does not vanish.
    by_path: dict[str, ReviewFileV1] = {f.path: f for f in committed}
    for d in dirty:
        prior = by_path.get(d.path)
        by_path[d.path] = ReviewFileV1(
            path=d.path, status=d.status,
            base_sha256=prior.base_sha256 if prior else None,
            current_sha256=d.current_sha256,
            old_path=prior.old_path if prior else None)
    files = tuple(sorted(by_path.values(), key=lambda f: f.path))
    return ReviewSubjectV1(base_commit=base, head_commit=head, base_is_ancestor=True,
                           commits=tuple(commits), files=files)


def resolve_commit_chain(repo_root: str | Path, base: str,
                         head: str) -> list[ReviewCommitV1]:
    """The base-exclusive ancestry path to HEAD, oldest first.

    `--ancestry-path` keeps the list to commits that actually lie between the two, so an unrelated
    commit reachable by some other route cannot appear in a package's history.
    """
    r = _git(repo_root, ["rev-list", "--ancestry-path", "--reverse", f"{base}..{head}"])
    if r.returncode != 0:
        raise ReviewSubjectError(
            f"cannot read the commit chain {base}..{head}: {r.stderr.strip()[:200]}")
    out: list[ReviewCommitV1] = []
    for sha in [s.strip() for s in r.stdout.splitlines() if s.strip()]:
        meta = _git(repo_root, ["show", "-s", "--format=%H%x00%P%x00%T%x00%s", sha])
        if meta.returncode != 0:
            raise ReviewSubjectError(f"cannot read commit {sha[:12]}")
        parts = meta.stdout.split("\0")
        if len(parts) < 4:
            raise ReviewSubjectError(f"cannot read commit {sha[:12]} metadata")
        commit, parents_raw, tree, subject = parts[0], parts[1], parts[2], parts[3].strip()
        names = _git(repo_root, ["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", sha])
        changed = tuple(sorted(_split_nul(names.stdout))) if names.returncode == 0 else ()
        patch = _git(repo_root, ["diff-tree", "-p", "--no-color", sha], binary=True)
        patch_sha = hashlib.sha256(patch.stdout if patch.returncode == 0 else b"").hexdigest()
        out.append(ReviewCommitV1(
            commit=commit, parents=tuple(p for p in parents_raw.split() if p), tree=tree,
            subject=subject, changed_files=changed, patch_sha256=patch_sha))
    return out


def validate_commit_chain(subject: ReviewSubjectV1) -> list[str]:
    """The chain is ordered, connected, ends at HEAD, and explains the committed subject."""
    problems: list[str] = []
    if not subject.declared:
        return problems
    prev: str | None = None
    for c in subject.commits:
        if prev is not None and prev not in c.parents:
            problems.append(
                f"commit {c.commit[:12]} does not descend from {prev[:12]}: the packaged history "
                f"is not one ordered path")
        prev = c.commit
    if subject.commits:
        if subject.base_commit not in subject.commits[0].parents:
            problems.append(
                f"the first packaged commit {subject.commits[0].commit[:12]} does not descend "
                f"from the declared base {subject.base_commit[:12]}")
        if subject.commits[-1].commit != subject.head_commit:
            problems.append(
                f"the packaged history ends at {subject.commits[-1].commit[:12]}, not at the "
                f"review head {subject.head_commit[:12]}")
    elif subject.base_commit != subject.head_commit:
        problems.append("the subject declares a base different from HEAD but carries no commits")
    return problems
