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

import dataclasses
import hashlib
import stat
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs

#: The environment variable through which an operator SUPPLIES the declared base.
#:
#: F6 (round 16): it is read at the TOP LEVEL only — never inside the resolver. The resolver used
#: to read it itself and then decide, from the PROCESS CWD, whether the declaration was "really"
#: about the repository it had been handed. That made the CWD an authorization token: standing in
#: the wrong directory silently discarded an intentional declaration and produced an EMPTY legacy
#: subject, with no error. The CWD is not a credential and cannot say what a review is OF.
#:
#: The declaration now travels EXPLICITLY: the CLI/packager reads it once and passes it, with the
#: resolved repository root, to `resolve_review_subject`. Children never inherit it — see
#: `child_env_without_declaration`.
REVIEW_BASE_ENV = "REMEDY_REVIEW_BASE"

#: F5 (round 16): the typed KIND of a path in the review subject.
#:
#: Round 15 hashed every dirty path with `read_bytes()`, which FOLLOWS symlinks: `repo/link.txt ->
#: /tmp/outside.txt` put the outside file's bytes in the content proof, while the ZIP collector
#: (`find -type f`) never packaged the link at all. The proof described a file the package did not
#: contain, sourced from outside the repository entirely.
#:
#: So a path's kind is inspected with `lstat` and recorded, and each kind has exactly one honest
#: proof: a regular file hashes its OWN bytes; a symlink hashes its literal target TEXT (never the
#: bytes it points at); everything else is refused rather than guessed at.
KIND_REGULAR = "regular"
KIND_SYMLINK = "symlink"
KIND_DELETED = "deleted"
KIND_DIRECTORY = "directory"
KIND_SPECIAL = "special"
VALID_FILE_KINDS = frozenset({KIND_REGULAR, KIND_SYMLINK, KIND_DELETED, KIND_DIRECTORY,
                              KIND_SPECIAL})

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
    #: F5 (round 16): WHAT this path is NOW (the CURRENT side). `regular` for a committed record
    #: whose content git already proved; the working-tree kinds are inspected with `lstat` and
    #: never followed. Kept as `kind` for back-compat; `current_kind` is its explicit synonym.
    kind: str = KIND_REGULAR
    #: For a symlink: the literal target text, exactly as stored. Never resolved, never read
    #: through. `None` for every other kind.
    link_target: str | None = None
    #: F3 (round 17): the kind and git mode at the BASE side of the change. A modify from a
    #: symlink to a regular file, or a mode-only 100644->100755 change, is provable only when
    #: BOTH sides are recorded. `None`/`""` when there is no base side (an added file).
    base_kind: str | None = None
    base_mode: str = ""
    current_mode: str = ""

    @property
    def current_kind(self) -> str:
        """The explicit name for `kind` — WHAT this path is on the current side."""
        return self.kind

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {"path": self.path, "status": self.status,
                               "base_sha256": self.base_sha256,
                               "current_sha256": self.current_sha256,
                               "kind": self.kind}
        if self.old_path is not None:
            out["old_path"] = self.old_path
        if self.link_target is not None:
            out["link_target"] = self.link_target
        if self.base_kind is not None:
            out["base_kind"] = self.base_kind
        if self.base_mode:
            out["base_mode"] = self.base_mode
        if self.current_mode:
            out["current_mode"] = self.current_mode
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


def inspect_path_kind(full: Path) -> tuple[str, str | None]:
    """The typed KIND of a working-tree path, inspected WITHOUT following it.

    Returns `(kind, link_target)`. `lstat` is the whole point: `is_file()`/`read_bytes()` answer
    "what does this point AT", and a review needs "what IS this". A dirty `link.txt ->
    /tmp/outside.txt` was hashed as its target's bytes — content from outside the repository
    entering the proof, while the ZIP (built with `find -type f`) omitted the link entirely.
    """
    try:
        st = os.lstat(full)
    except OSError:
        return KIND_DELETED, None
    if stat.S_ISLNK(st.st_mode):
        try:
            return KIND_SYMLINK, os.readlink(full)
        except OSError:
            return KIND_SPECIAL, None
    if stat.S_ISREG(st.st_mode):
        return KIND_REGULAR, None
    if stat.S_ISDIR(st.st_mode):
        return KIND_DIRECTORY, None
    return KIND_SPECIAL, None                # FIFO, socket, device, anything else


def symlink_escapes_repository(repo_root: str | Path, path: str, target: str) -> bool:
    """Does a symlink point outside the repository — absolutely, or by traversal?

    Decided LEXICALLY on the recorded target text, exactly as F010 requires: `resolve()` answers
    where a link points, not whether the caller was routed through one, and resolving would also
    touch the outside filesystem this check exists to avoid.
    """
    if not target:
        return True
    if target.startswith("/") or target.startswith("~"):
        return True
    root = Path(os.path.normpath(str(repo_root)))
    here = (root / path).parent
    dest = Path(os.path.normpath(str(here / target)))
    try:
        dest.relative_to(root)
    except ValueError:
        return True
    return False


def _sha256_blob(repo_root: str | Path, rev: str, path: str) -> str | None:
    """The content hash of a path AS OF a commit — the only way to prove a deleted file."""
    r = _git(repo_root, ["show", f"{rev}:{path}"], binary=True)
    if r.returncode != 0:
        return None
    return hashlib.sha256(r.stdout).hexdigest()


def _split_nul(raw: str) -> list[str]:
    return [p for p in raw.split("\0") if p != ""]


def _toplevel(path: str | Path | None) -> str:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       cwd=str(path) if path else None, capture_output=True, text=True,
                       timeout=_TIMEOUT)
    return r.stdout.strip() if r.returncode == 0 else ""



#: F3 (round 17): git tree modes → the typed file kind. A committed symlink is stored as a
#: 120000 blob whose CONTENT is its target text — git already holds it, so it is never read
#: through the filesystem. A submodule (160000) is a gitlink, not a file we can hash.
_GIT_MODE_TO_KIND = {
    "100644": KIND_REGULAR,
    "100755": KIND_REGULAR,          # executable — a mode difference, still a regular file
    "120000": KIND_SYMLINK,
    "160000": KIND_SPECIAL,          # submodule gitlink
    "040000": KIND_DIRECTORY,
}


def _git_mode_to_kind(mode: str) -> str:
    """The typed kind for a git tree mode. An unknown mode is `special`, never assumed regular."""
    return _GIT_MODE_TO_KIND.get((mode or "").zfill(6), KIND_SPECIAL)


def _committed_symlink_target(repo_root: str | Path, rev: str, path: str) -> str | None:
    """A committed symlink's target text — its BLOB content, read from git, never followed."""
    r = _git(repo_root, ["show", f"{rev}:{path}"], binary=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def _committed_records(repo_root: str | Path, base: str, head: str) -> list[ReviewFileV1]:
    """The committed delta, from ONE canonical git command that also carries MODES.

    `--raw -z` is NUL-delimited (a path with a space, newline or quote survives) AND reports the
    source/destination modes, so a committed symlink or a mode-only change is provable. Each raw
    record is `:<srcmode> <dstmode> <srcsha> <dstsha> <status>` then the path(s), NUL-separated.

    F3 (round 17): kinds come from those modes, never from `kind=regular` defaults. A committed
    symlink's target is read from its git BLOB (`git show <rev>:<path>`), never through the
    working tree — and an absolute or escaping committed symlink is recorded truthfully so
    `validate_subject_path_kinds` can block it.
    """
    r = _git(repo_root, ["diff", "--raw", "-z", "--find-renames", "--abbrev=40",
                         f"{base}..{head}"])
    if r.returncode != 0:
        raise ReviewSubjectError(
            f"cannot read the committed delta {base}..{head}: {r.stderr.strip()[:200]}")
    fields = _split_nul(r.stdout)
    out: list[ReviewFileV1] = []
    i = 0
    while i < len(fields):
        meta = fields[i]
        if not meta.startswith(":"):
            raise ReviewSubjectError(f"malformed raw diff record near {meta!r}")
        # ":100644 100755 <src40> <dst40> M" — status letter may carry a rename score (R100).
        parts = meta[1:].split()
        if len(parts) < 5:
            raise ReviewSubjectError(f"malformed raw diff meta {meta!r}")
        src_mode, dst_mode, _src_sha, _dst_sha, code = parts[0], parts[1], parts[2], parts[3], \
            parts[4]
        letter = code[0]
        status = _GIT_STATUS_MAP.get(letter)
        if status is None:
            raise ReviewSubjectError(f"unsupported git status {code!r} in the committed delta")
        base_kind = _git_mode_to_kind(src_mode)
        cur_kind = _git_mode_to_kind(dst_mode)

        if letter in ("R", "C"):
            if i + 2 >= len(fields):
                raise ReviewSubjectError(f"malformed rename record near {meta!r}")
            old_path, new_path = fields[i + 1], fields[i + 2]
            i += 3
            out.append(ReviewFileV1(
                path=new_path, status=status, old_path=old_path,
                base_sha256=_sha256_blob(repo_root, base, old_path),
                current_sha256=_sha256_blob(repo_root, head, new_path),
                kind=cur_kind, base_kind=base_kind,
                base_mode=src_mode, current_mode=dst_mode,
                link_target=(_committed_symlink_target(repo_root, head, new_path)
                             if cur_kind == KIND_SYMLINK else None)))
            continue

        if i + 1 >= len(fields):
            raise ReviewSubjectError(f"malformed status record near {meta!r}")
        path = fields[i + 1]
        i += 2
        added, deleted = letter == "A", letter == "D"
        out.append(ReviewFileV1(
            path=path, status=status,
            base_sha256=(None if added else _sha256_blob(repo_root, base, path)),
            current_sha256=(None if deleted else _sha256_blob(repo_root, head, path)),
            kind=(KIND_DELETED if deleted else cur_kind),
            base_kind=(None if added else base_kind),
            base_mode=("" if added else src_mode),
            current_mode=("" if deleted else dst_mode),
            link_target=(_committed_symlink_target(repo_root, head, path)
                         if (not deleted and cur_kind == KIND_SYMLINK) else None)))
    return out


def _head_kind_and_mode(repo_root: str | Path, head: str, path: str) -> tuple[str | None, str]:
    """The kind and git mode of a path AS OF `head`, from `git ls-tree` — never the filesystem."""
    r = _git(repo_root, ["ls-tree", "-z", head, "--", path])
    if r.returncode != 0 or not r.stdout.strip():
        return None, ""
    # "<mode> <type> <sha>\t<path>" — mode is the first field.
    mode = r.stdout.split()[0] if r.stdout.split() else ""
    return _git_mode_to_kind(mode), mode


def _dirty_current_record(repo_root: str | Path, path: str,
                          base_sha: str | None, base_kind: str | None,
                          base_mode: str, *, status: str,
                          old_path: str | None = None) -> ReviewFileV1:
    """One dirty record, inspecting the WORKING-TREE side without ever following it (F5, r16),
    while carrying its BASE side forward (F5, r17)."""
    full = Path(repo_root) / path
    kind, target = inspect_path_kind(full)
    common = dict(path=path, old_path=old_path, base_sha256=base_sha,
                  base_kind=base_kind, base_mode=base_mode)
    if kind == KIND_DELETED:
        return ReviewFileV1(status=STATUS_DELETED, current_sha256=None, kind=KIND_DELETED,
                            **common)
    if kind == KIND_REGULAR:
        # F3 (round 18): hash through the anchored, atomically no-follow reader. `_sha256_file`
        # reopened the path by name, so a regular file swapped to an external symlink between the
        # lstat above and the read would have hashed OUTSIDE bytes. If the swap happens, the
        # reader refuses and the record carries no current hash — unproven, which blocks at
        # packaging — rather than laundering outside content into the proof.
        try:
            vf = _fs.read_verified_relative(repo_root, path, expected_kind="regular",
                                            error_cls=ReviewSubjectError, noun="dirty file")
            return ReviewFileV1(status=status,
                                current_sha256=hashlib.sha256(vf.data).hexdigest(),
                                kind=KIND_REGULAR, **common)
        except ReviewSubjectError:
            return ReviewFileV1(status=status, current_sha256=None, kind=KIND_REGULAR, **common)
    if kind == KIND_SYMLINK:
        # The LINK's own content is its target text. Hashing what it points at would read outside
        # the repository and describe bytes the package does not carry.
        return ReviewFileV1(
            status=status,
            current_sha256=hashlib.sha256((target or "").encode("utf-8")).hexdigest(),
            kind=KIND_SYMLINK, link_target=target, **common)
    # A directory or special file has no honest content proof; recorded, blocked at packaging.
    return ReviewFileV1(status=status, current_sha256=None, kind=kind, **common)


def _dirty_records(repo_root: str | Path, head: str = "HEAD") -> list[ReviewFileV1]:
    """Uncommitted changes, NUL-safe, with FULL base-side proofs (F5, round 17).

    A dirty deletion used to carry `base_sha256: null` — no tombstone at all, so nothing said what
    was removed. A dirty rename lost its old path and base hash. Both are resolved here against
    the declared HEAD with git blob reads (never the working tree): a deletion records the HEAD
    blob it removed, a rename records old path + both hashes + both kinds.
    """
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
        old_path = None
        if code[0] in ("R", "C") or code[1] in ("R", "C"):
            # porcelain -z: a rename/copy is `XY NEW\0OLD\0` — NEW in `entry`, OLD next.
            if i < len(fields):
                old_path = fields[i]
                i += 1
        if not path:
            continue

        if old_path is not None:
            # A (staged) rename: prove both ends against HEAD.
            base_kind, base_mode = _head_kind_and_mode(repo_root, head, old_path)
            rec = _dirty_current_record(
                repo_root, path, base_sha=_sha256_blob(repo_root, head, old_path),
                base_kind=base_kind, base_mode=base_mode,
                status=STATUS_RENAMED, old_path=old_path)
        else:
            # A modification or deletion of a path that (usually) exists at HEAD.
            base_kind, base_mode = _head_kind_and_mode(repo_root, head, path)
            base_sha = _sha256_blob(repo_root, head, path) if base_kind is not None else None
            rec = _dirty_current_record(
                repo_root, path, base_sha=base_sha, base_kind=base_kind, base_mode=base_mode,
                status=STATUS_DIRTY)
        out.append(rec)
    return out


def validate_subject_path_kinds(subject: "ReviewSubjectV1",
                                repo_root: str | Path) -> list[str]:
    """F5: which path kinds may appear in an AUTHORITATIVE review subject.

    The policy is deliberately conservative where a proof cannot be made honest:

    * `regular` — always fine, hashed from its own bytes;
    * `symlink` pointing INSIDE the repository — fine, proven by its target text and packaged as
      metadata, so the package and the proof agree;
    * `symlink` pointing OUTSIDE (absolute, `~`, or escaping by traversal) — BLOCKED. Its target
      is not part of the review, must not be read, and its local absolute path must not enter the
      ZIP. Blocking beats following it or silently omitting it, which is what happened before;
    * `directory`, `special` (FIFO/socket/device) — BLOCKED. There is nothing to hash and nothing
      honest to package.
    """
    problems: list[str] = []
    for f in subject.files:
        if f.kind not in VALID_FILE_KINDS:
            problems.append(f"review subject file {f.path!r} has an unsupported kind {f.kind!r}")
        elif f.kind == KIND_SYMLINK:
            if symlink_escapes_repository(repo_root, f.path, f.link_target or ""):
                problems.append(
                    f"review subject file {f.path!r} is a symlink pointing outside the "
                    f"repository; its target is not part of this review and is not read")
        elif f.kind in (KIND_DIRECTORY, KIND_SPECIAL):
            problems.append(
                f"review subject file {f.path!r} is a {f.kind}, which carries no content proof "
                f"and cannot be packaged as a file")
    return problems


#: F7 (round 16): the packaged patch directory, one canonical `<full-sha>.patch` per commit.
COMMIT_PATCH_DIRNAME = "review_commit_patches"


def commit_patch_bytes(repo_root: str | Path, sha: str) -> bytes:
    """The EXACT bytes whose sha256 the commit chain records.

    One helper, so the recorded hash, the packaged file and the packager's recomputation can
    never be three slightly different things. `git diff-tree -p` with the same flags
    `resolve_commit_chain` uses — no `--color`, no pager, no locale-dependent decoration.
    """
    r = _git(repo_root, ["diff-tree", "-p", "--no-color", sha], binary=True)
    if r.returncode != 0:
        raise ReviewSubjectError(f"cannot read the patch for commit {sha[:12]}")
    return r.stdout or b""


def commit_patch_filename(sha: str) -> str:
    """`<full-commit-sha>.patch` — the full sha, so no two commits can share a file."""
    if not (len(sha) == 40 and all(c in "0123456789abcdef" for c in sha)):
        raise ReviewSubjectError(f"refusing to name a patch after {sha[:20]!r}: not a commit sha")
    return f"{sha}.patch"


def read_declared_base(env: dict[str, str] | None = None) -> str | None:
    """Read the operator's base declaration — the ONE place it is read.

    F6 (round 16): the TOP LEVEL (the CLI, the packager) calls this once and then passes the
    value explicitly. Nothing downstream reads the environment, so nothing downstream has to
    guess, from its own CWD, whether a declaration was meant for it.
    """
    raw = (env if env is not None else os.environ).get(REVIEW_BASE_ENV, "")
    v = (raw or "").strip()
    return v or None


def child_env_without_declaration(env: dict[str, str] | None = None) -> dict[str, str]:
    """A child environment with the base declaration REMOVED.

    F6: the declaration is inherited by every child process, so an export's verification
    subprocess — a pytest run against its own temporary repository, say — would otherwise be
    handed a base that was never about it. Observed exactly that in round 15: an unrelated job's
    evidence lost its content proof entirely. A child that needs a base is given one explicitly.
    """
    out = dict(env if env is not None else os.environ)
    out.pop(REVIEW_BASE_ENV, None)
    return out


#: F7 (round 17): the EXACT allowed field sets for the externally-shared artifacts. An unknown
#: field is a blocking schema error, never ignored — a packager that ignores unknown fields is a
#: packager that would ship an injected `secret`/`path` field untouched.
_REVIEW_FILE_FIELDS = frozenset({"path", "status", "base_sha256", "current_sha256", "old_path",
                                 "kind", "link_target", "base_kind", "base_mode",
                                 "current_mode"})
_REVIEW_FILE_REQUIRED = frozenset({"path", "status", "base_sha256", "current_sha256", "kind"})
_REVIEW_COMMIT_FIELDS = frozenset({"commit", "parents", "tree", "subject", "changed_files",
                                   "patch_sha256"})
_REVIEW_SUBJECT_FIELDS = frozenset({"subject_v", "base_commit", "head_commit", "base_is_ancestor",
                                    "commits", "files"})
_VALID_STATUSES = frozenset({STATUS_ADDED, STATUS_MODIFIED, STATUS_DELETED, STATUS_RENAMED,
                             STATUS_COPIED, STATUS_TYPE_CHANGED, STATUS_DIRTY})

#: F4 (round 18): the closed git-mode vocabulary a ReviewFile may carry, plus the empty string
#: for a side that does not exist (an added file has no base mode, a deleted one no current mode).
_VALID_GIT_MODES = frozenset({"", "100644", "100755", "120000", "160000", "040000"})
#: The kinds a base side (or a committed current side read from a git mode) may name. `deleted` is
#: a status, never a `base_kind`; `directory`/`special` come from real git modes (040000/160000).
_VALID_BASE_KINDS = frozenset({KIND_REGULAR, KIND_SYMLINK, KIND_DIRECTORY, KIND_SPECIAL})


def _is_hex40(v: Any) -> bool:
    return isinstance(v, str) and len(v) == 40 and all(c in "0123456789abcdef" for c in v)


def _is_hex64(v: Any) -> bool:
    return isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v)


def _is_hex64_or_none(v: Any) -> bool:
    if v is None:
        return True
    return _is_hex64(v)


def _metadata_is_safe(v: Any) -> bool:
    """A metadata STRING value carries no local path, secret or control character.

    F4: a known field with an arbitrary string is still a leak — `base_kind: "SECRET-/home/alice"`
    has an allowed KEY. Reuse the established F012 scanners rather than a new weaker regex.
    """
    if not isinstance(v, str):
        return True
    try:
        from packages.orchestration.run_manifest import (
            _contains_local_path, _contains_secret,
        )
        if _contains_secret(v) or _contains_local_path(v):
            return False
    except Exception:
        pass
    return not any(ord(c) < 32 and c not in "\t\n" for c in v)


def _safe_rel_path(p: Any) -> bool:
    """A relative POSIX path: no absolute, no `..` segment, no NUL. Newlines/tabs are fine."""
    if not isinstance(p, str) or not p:
        return False
    if p.startswith("/") or "\0" in p or "\\" in p:
        return False
    return not any(seg in ("", "..", ".") for seg in p.split("/"))


def validate_review_file_schema(d: Any, *, where: str = "review file") -> list[str]:
    """Strict schema for one ReviewFileV1 record as serialized in `review_subject.json`."""
    problems: list[str] = []
    if not isinstance(d, dict):
        return [f"{where} is not an object"]
    extra = set(d) - _REVIEW_FILE_FIELDS
    if extra:
        problems.append(f"{where} has unknown field(s) {sorted(extra)}")
    for req in _REVIEW_FILE_REQUIRED:
        if req not in d:
            problems.append(f"{where} is missing required field {req!r}")
    if not _safe_rel_path(d.get("path")):
        problems.append(f"{where} path {d.get('path')!r} is not a safe relative path")
    if d.get("status") not in _VALID_STATUSES:
        problems.append(f"{where} status {d.get('status')!r} is not a supported status")
    kind = d.get("kind")
    if kind not in VALID_FILE_KINDS:
        problems.append(f"{where} kind {kind!r} is not a supported kind")
    for hf in ("base_sha256", "current_sha256"):
        if not _is_hex64_or_none(d.get(hf)):
            problems.append(f"{where} {hf} is not a lowercase sha256 or null")
    lt = d.get("link_target")
    if kind == KIND_SYMLINK:
        if not isinstance(lt, str) or not lt:
            problems.append(f"{where} is a symlink but has no link_target")
    elif lt is not None:
        problems.append(f"{where} is {kind!r} but carries a link_target")
    if "old_path" in d and d["old_path"] is not None and not _safe_rel_path(d["old_path"]):
        problems.append(f"{where} old_path {d.get('old_path')!r} is not a safe relative path")

    # F4 (round 18): the round-17 typed fields must be CLOSED too. A known key with an arbitrary
    # string (`base_kind: "SECRET-/home/alice"`, `base_mode: "999999"`, `current_mode: "evil"`)
    # was accepted because only the KEY was checked.
    bk = d.get("base_kind")
    if bk is not None and bk not in _VALID_BASE_KINDS:
        problems.append(f"{where} base_kind {bk!r} is not a supported kind")
    for mf in ("base_mode", "current_mode"):
        mv = d.get(mf, "")
        if not isinstance(mv, str) or mv not in _VALID_GIT_MODES:
            problems.append(f"{where} {mf} {mv!r} is not a supported git mode")
    # A current symlink must carry the symlink git mode; a current regular must not.
    if kind == KIND_SYMLINK and d.get("current_mode", "") not in ("", "120000"):
        problems.append(f"{where} is a symlink but current_mode {d.get('current_mode')!r} "
                        f"is not the symlink mode")
    if kind == KIND_REGULAR and d.get("current_mode", "") == "120000":
        problems.append(f"{where} is regular but carries the symlink current_mode")
    for meta_field in ("base_kind", "base_mode", "current_mode"):
        if not _metadata_is_safe(d.get(meta_field)):
            problems.append(f"{where} {meta_field} carries a secret, local path or control text")
    problems.extend(_review_file_coherence(d, where=where))
    return problems


def _review_file_coherence(d: dict, *, where: str) -> list[str]:
    """F9 (round 19): the record must be internally COHERENT, not merely field-typed.

    Round 18 closed each field in isolation, so a record could still be self-contradictory: a
    `modified`/`added` regular file with `current_sha256: null` (nothing to package as its content),
    a `deleted` path with no `base_sha256` (no tombstone naming what was removed), a base
    `symlink` whose `base_mode` is `100644` (a regular-file mode), a `copied` file with no
    `old_path`, or a `type_changed` record whose base and current kinds are the same. Each is now
    rejected so an incoherent subject can never drive a package.
    """
    problems: list[str] = []
    status = d.get("status")
    kind = d.get("kind")
    base_kind = d.get("base_kind")
    base_sha = d.get("base_sha256")
    current_sha = d.get("current_sha256")
    base_mode = d.get("base_mode", "") or ""
    current_mode = d.get("current_mode", "") or ""

    # A present content-bearing side must carry its hash; an absent side must not.
    if kind in (KIND_REGULAR, KIND_SYMLINK) and current_sha is None:
        problems.append(f"{where} is a {kind} but carries no current_sha256")
    if kind in (KIND_DELETED, KIND_DIRECTORY, KIND_SPECIAL) and current_sha is not None:
        problems.append(f"{where} is {kind} but carries a current_sha256")

    # base/current git mode must name the same kind as the side it describes.
    if current_mode and _GIT_MODE_TO_KIND.get(current_mode) != kind:
        problems.append(f"{where} current_mode {current_mode!r} does not match kind {kind!r}")
    if base_mode and base_kind is not None and _GIT_MODE_TO_KIND.get(base_mode) != base_kind:
        problems.append(f"{where} base_mode {base_mode!r} does not match base_kind {base_kind!r}")

    # status ↔ base/current presence matrix.
    if status == STATUS_ADDED:
        if base_sha is not None:
            problems.append(f"{where} is added but carries a base_sha256")
        if base_kind is not None or base_mode:
            problems.append(f"{where} is added but carries a base side")
    if status in (STATUS_MODIFIED, STATUS_TYPE_CHANGED) and base_sha is None:
        problems.append(f"{where} is {status} but carries no base_sha256")
    if status == STATUS_DELETED:
        if base_sha is None:
            problems.append(f"{where} is deleted but carries no base_sha256 tombstone")
        if current_sha is not None:
            problems.append(f"{where} is deleted but carries a current_sha256")
        if kind != KIND_DELETED:
            problems.append(f"{where} is deleted but kind is {kind!r}")
    if status in (STATUS_RENAMED, STATUS_COPIED) and not d.get("old_path"):
        problems.append(f"{where} is {status} but names no old_path")
    if status == STATUS_TYPE_CHANGED and base_kind is not None and base_kind == kind:
        problems.append(f"{where} is type_changed but base and current kind are both {kind!r}")
    return problems


def validate_review_commit_schema(d: Any, *, where: str = "review commit") -> list[str]:
    """F4 (round 18): strict schema for one ReviewCommitV1 record. Round 17 never validated the
    embedded commit list, so `commits: [{"EXTRA_SECRET": "/home/alice/..."}]` was accepted."""
    problems: list[str] = []
    if not isinstance(d, dict):
        return [f"{where} is not an object"]
    extra = set(d) - _REVIEW_COMMIT_FIELDS
    if extra:
        problems.append(f"{where} has unknown field(s) {sorted(extra)}")
    for sf in ("commit", "tree"):
        if not _is_hex40(d.get(sf)):
            problems.append(f"{where} {sf} is not a full lowercase sha")
    parents = d.get("parents")
    if not isinstance(parents, list) or not all(_is_hex40(p) for p in parents):
        problems.append(f"{where} parents is not a list of full lowercase shas")
    subj = d.get("subject")
    if not isinstance(subj, str) or len(subj) > 4096 or not _metadata_is_safe(subj):
        problems.append(f"{where} subject is missing, too long, or carries a secret/path/control")
    cf = d.get("changed_files")
    if not isinstance(cf, list) or not all(_safe_rel_path(p) for p in cf):
        problems.append(f"{where} changed_files is not a list of safe relative paths")
    elif cf != sorted(cf) or len(set(cf)) != len(cf):
        problems.append(f"{where} changed_files is not sorted-unique")
    if not _is_hex64(d.get("patch_sha256")):
        problems.append(f"{where} patch_sha256 is not a lowercase sha256")
    return problems


def validate_review_subject_schema(d: Any) -> list[str]:
    """Strict RECURSIVE schema for `review_subject.json` — exact fields, closed enums, safe paths,
    validated commit and file subobjects, no duplicate paths (F4, round 18)."""
    problems: list[str] = []
    if not isinstance(d, dict):
        return ["review_subject.json is not an object"]
    extra = set(d) - _REVIEW_SUBJECT_FIELDS
    if extra:
        problems.append(f"review_subject.json has unknown field(s) {sorted(extra)}")
    if d.get("subject_v") != SUBJECT_VERSION:
        problems.append(f"review_subject.json subject_v {d.get('subject_v')!r} != "
                        f"{SUBJECT_VERSION}")
    if not isinstance(d.get("base_is_ancestor"), bool):
        problems.append("review_subject.json base_is_ancestor is not a boolean")
    # F4: base/HEAD are FULL lowercase shas, or the exact legacy-empty form (no declared base).
    base, head = d.get("base_commit"), d.get("head_commit")
    declared = bool(base) or bool(head)
    if declared:
        for cf, cv in (("base_commit", base), ("head_commit", head)):
            if not _is_hex40(cv):
                problems.append(f"review_subject.json {cf} is not a full lowercase sha")
        if not d.get("base_is_ancestor"):
            problems.append("review_subject.json declares a base but base_is_ancestor is false")
    else:
        if base != "" or head != "" or d.get("base_is_ancestor") is not False:
            problems.append("review_subject.json legacy form must have empty base/head and "
                            "base_is_ancestor false")
    for i, c in enumerate(d.get("commits") or []):
        problems.extend(validate_review_commit_schema(c, where=f"review_subject commit[{i}]"))
    paths: list[str] = []
    for i, f in enumerate(d.get("files") or []):
        problems.extend(validate_review_file_schema(f, where=f"review_subject file[{i}]"))
        if isinstance(f, dict):
            paths.append(str(f.get("path")))
    if len(set(paths)) != len(paths):
        problems.append("review_subject.json lists a path more than once")
    return problems


def decode_review_subject_from_json(d: Any) -> "ReviewSubjectV1":
    """Strict-decode a serialized `review_subject.json` into a typed ReviewSubjectV1.

    The strict schema is the ONLY untrusted entry (F4): a record that fails it never becomes a
    typed object. Used by the packager to drive the ArchivePlan from the same object the review
    subject records, so the archive and the subject cannot disagree.
    """
    problems = validate_review_subject_schema(d)
    if problems:
        raise ReviewSubjectError("; ".join(problems)[:400])
    files = tuple(ReviewFileV1(
        path=f["path"], status=f["status"], base_sha256=f.get("base_sha256"),
        current_sha256=f.get("current_sha256"), old_path=f.get("old_path"),
        kind=f.get("kind", KIND_REGULAR), link_target=f.get("link_target"),
        base_kind=f.get("base_kind"), base_mode=f.get("base_mode", ""),
        current_mode=f.get("current_mode", "")) for f in (d.get("files") or []))
    commits = tuple(ReviewCommitV1(
        commit=c["commit"], parents=tuple(c["parents"]), tree=c["tree"], subject=c["subject"],
        changed_files=tuple(c["changed_files"]), patch_sha256=c["patch_sha256"])
        for c in (d.get("commits") or []))
    return ReviewSubjectV1(
        base_commit=d.get("base_commit", ""), head_commit=d.get("head_commit", ""),
        base_is_ancestor=bool(d.get("base_is_ancestor")), commits=commits, files=files)


def merge_review_file_state(committed: ReviewFileV1 | None,
                            dirty: ReviewFileV1) -> ReviewFileV1:
    """F2 (round 17): the ONE lossless, typed merge of a committed and a dirty record.

    A path can be both committed (base..HEAD) and dirty (HEAD..working-tree). The working tree is
    the later truth, so its CURRENT side wins — but its base side is empty (dirty records now
    resolve their own HEAD base, so this mostly agrees), and the committed record may carry the
    ORIGINAL base (base..HEAD) that predates HEAD. The previous inline reconstruction rebuilt a
    bare `ReviewFileV1(path, status, base_sha256, current_sha256, old_path)` and silently dropped
    `kind`, `link_target`, `base_kind` and the modes — so a dirty symlink over a committed regular
    file came back a regular file, and the package then hashed it as one.

    The rule, field by field:

    * current side (kind, mode, hash, link_target, status) — the DIRTY record's, it is what the
      file is now;
    * base side (base_sha256, base_kind, base_mode) — the COMMITTED record's when it has one
      (the change under review started at the review base, not at HEAD), else the dirty record's
      HEAD-resolved base;
    * old_path — whichever side renamed;
    * a committed DELETION is never silently resurrected: if HEAD/base deleted the file and the
      working tree also has it absent, it stays deleted.
    """
    if committed is None:
        return dirty

    # Prefer the committed base side (base..HEAD) — the review's actual starting point — but never
    # lose a base the dirty side resolved when the committed side had none.
    base_sha = committed.base_sha256 if committed.base_sha256 is not None else dirty.base_sha256
    base_kind = committed.base_kind if committed.base_kind is not None else dirty.base_kind
    base_mode = committed.base_mode or dirty.base_mode
    old_path = dirty.old_path or committed.old_path

    # A committed deletion that the working tree also shows absent stays a deletion.
    if committed.status == STATUS_DELETED and dirty.kind == KIND_DELETED:
        return dataclasses.replace(dirty, status=STATUS_DELETED, base_sha256=base_sha,
                                   base_kind=base_kind, base_mode=base_mode, old_path=old_path)

    return dataclasses.replace(
        dirty, base_sha256=base_sha, base_kind=base_kind, base_mode=base_mode,
        old_path=old_path)


def resolve_review_subject(repo_root: str | Path,
                           declared_base: str | None = None) -> ReviewSubjectV1:
    """THE review-subject resolver. Every consumer calls this; nobody re-implements it.

    `declared_base` is passed EXPLICITLY by the top level (F6, round 16) — the resolver reads no
    environment and consults no CWD. When no base is declared the subject is the dirty tree
    exactly as it was before round 14 — a documented, unchanged legacy path, so an ordinary job
    is untouched.

    When a base IS declared it is VERIFIED, because a review is worthless if nobody knows what it
    is a review OF:

    * `git rev-parse --verify <base>^{commit}` — an unresolvable base raises rather than silently
      shrinking the subject to the dirty tree;
    * `git merge-base --is-ancestor <base> HEAD` — a non-ancestral base raises rather than pulling
      unrelated branches' files into the review.
    """
    root = Path(repo_root)
    # F6 (round 16): the resolver reads NO environment. A base is declared by the caller or it is
    # not declared at all — there is no third, ambient state whose applicability has to be
    # guessed from the process CWD.
    base_in = (declared_base or "").strip()
    explicit = bool(base_in)

    # A declared base is ALWAYS honoured and ALWAYS verified — which is what keeps a typo'd or
    # non-ancestral base a blocking error rather than a silently smaller review. An export for an
    # unrelated repository is simply never handed one (F6).
    inside = _git(root, ["rev-parse", "--is-inside-work-tree"])
    if inside.returncode != 0:
        if base_in and explicit:
            raise ReviewSubjectError(
                f"a review base ({base_in!r}) was declared but {root} is not a git work tree")
        return ReviewSubjectV1()

    dirty = _dirty_records(root, "HEAD")
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

    # A path may be both committed and dirty; the working tree is the later truth. The merge is
    # LOSSLESS and TYPED (F2, round 17) — the previous inline reconstruction dropped `kind` and
    # `link_target`, so a dirty symlink over a committed regular file came out as a regular file.
    by_path: dict[str, ReviewFileV1] = {f.path: f for f in committed}
    for d in dirty:
        by_path[d.path] = merge_review_file_state(by_path.get(d.path), d)
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
