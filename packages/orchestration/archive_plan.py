"""F1/F7 (round 18) — ONE typed ArchivePlanV1 drives the review package.

The package used to be assembled from two disagreeing sources: the typed ReviewSubject on one
side, and an independent `find -type f` list on the other. `find -type f` does not match symlinks,
so a safe authoritative symlink was ABSENT from the archive while the Content Proof (which knew
about it) and the ZIP verification (which checked only the find list) both reported PASS. The
subject said one thing; the archive was built from another.

The ArchivePlan is the single source of truth. Every ReviewSubject file receives exactly one typed
disposition — a regular member, a symlink member, a tombstone, or a BLOCK — and the repository
context files chosen by the bundle policy ride alongside as explicitly non-authoritative members.
The builder writes the plan; the post-build verifier holds the archive to the plan. Nothing
rediscovers an authoritative path.
"""
from __future__ import annotations

import stat
from dataclasses import dataclass, field
from pathlib import Path

from packages.common import secure_fs as _fs
from packages.orchestration.review_subject import (
    KIND_DELETED,
    KIND_DIRECTORY,
    KIND_REGULAR,
    KIND_SPECIAL,
    KIND_SYMLINK,
    ReviewSubjectV1,
    symlink_escapes_repository,
)

PLAN_VERSION = 1

#: Canonical ZIP member kinds.
MEMBER_REGULAR = "regular"
MEMBER_SYMLINK = "symlink"

#: The two unix permission sets a regular member may carry — a plain file or an executable one.
MODE_REGULAR = 0o644
MODE_EXECUTABLE = 0o755
MODE_SYMLINK = 0o777

#: git tree mode → the ZIP member (kind, unix perm bits).
_GIT_MODE_TO_MEMBER = {
    "100644": (MEMBER_REGULAR, MODE_REGULAR),
    "100755": (MEMBER_REGULAR, MODE_EXECUTABLE),
    "120000": (MEMBER_SYMLINK, MODE_SYMLINK),
}


class ArchivePlanError(Exception):
    """The package cannot be planned safely. Never downgraded to a warning."""


@dataclass(frozen=True)
class ArchiveMemberV1:
    """One planned ZIP member, fully typed BEFORE anything is written or read."""
    archive_path: str
    kind: str                       # MEMBER_REGULAR | MEMBER_SYMLINK
    mode: int                       # unix permission bits (0o644 / 0o755 / 0o777)
    authoritative: bool             # part of the ReviewSubject's change, vs. bundle context
    source_root: str                # the anchored root this member is read under
    source_rel: str                 # the path relative to source_root
    #: For an authoritative record, the content hash / link target the ReviewSubject declared.
    expected_sha256: str | None = None
    expected_link_target: str | None = None

    def to_json(self) -> dict:
        return {"archive_path": self.archive_path, "kind": self.kind, "mode": self.mode,
                "authoritative": self.authoritative,
                "expected_sha256": self.expected_sha256,
                "expected_link_target": self.expected_link_target}


@dataclass(frozen=True)
class TombstoneRecordV1:
    """A deleted authoritative path: no ZIP member, but an explicit record that it is gone."""
    path: str
    base_sha256: str | None

    def to_json(self) -> dict:
        return {"path": self.path, "base_sha256": self.base_sha256}


@dataclass(frozen=True)
class BlockedRecordV1:
    """An authoritative path the package cannot honestly represent — the package is BLOCKED."""
    path: str
    reason: str

    def to_json(self) -> dict:
        return {"path": self.path, "reason": self.reason}


@dataclass(frozen=True)
class ArchivePlanV1:
    repository_members: tuple[ArchiveMemberV1, ...] = ()
    evidence_members: tuple[ArchiveMemberV1, ...] = ()
    tombstones: tuple[TombstoneRecordV1, ...] = ()
    blocked_records: tuple[BlockedRecordV1, ...] = ()
    plan_v: int = PLAN_VERSION

    @property
    def blocked(self) -> bool:
        return bool(self.blocked_records)

    def all_members(self) -> tuple[ArchiveMemberV1, ...]:
        return self.repository_members + self.evidence_members

    def to_json(self) -> dict:
        return {"plan_v": self.plan_v,
                "repository_members": [m.to_json() for m in self.repository_members],
                "evidence_members": [m.to_json() for m in self.evidence_members],
                "tombstones": [t.to_json() for t in self.tombstones],
                "blocked_records": [b.to_json() for b in self.blocked_records]}


def _member_kind_mode_for(f) -> tuple[str, int] | None:
    """The ZIP (kind, mode) a ReviewSubject file's CURRENT side maps to, or None if unpackageable."""
    if f.kind == KIND_SYMLINK:
        return (MEMBER_SYMLINK, MODE_SYMLINK)
    if f.kind == KIND_REGULAR:
        mapped = _GIT_MODE_TO_MEMBER.get(f.current_mode or "")
        if mapped is not None:
            return mapped
        # A dirty regular file has no git mode; default to a plain file. Executability of a dirty
        # file is not part of a committed change and is not asserted.
        return (MEMBER_REGULAR, MODE_REGULAR)
    return None


def build_archive_plan(*, repo_root: str | Path, subject: ReviewSubjectV1,
                       repo_context_rel: list[str], evidence_root: str | Path | None,
                       evidence_rel: list[str], is_authoritative_source) -> ArchivePlanV1:
    """Assemble the one typed plan.

    * ``subject`` — the authoritative change; each file gets exactly one disposition.
    * ``repo_context_rel`` — the repository bundle policy's context files (the bulk of the ZIP).
      An authoritative path missing from this list (e.g. a symlink `find -type f` skipped) is
      still planned as a member from the subject; a context path that is not authoritative rides
      along non-authoritatively.
    * ``is_authoritative_source(rel)`` — the shared policy predicate: is this repo path part of a
      task's attestable source change? Used to catch a changed path the bundle policy EXCLUDES
      (an `.env`, a key, a log) — that must BLOCK, never silently vanish.
    """
    repo_root = Path(repo_root)
    context = set(repo_context_rel)
    members: dict[str, ArchiveMemberV1] = {}
    tombstones: list[TombstoneRecordV1] = []
    blocked: list[BlockedRecordV1] = []

    # 1. The authoritative subset — every ReviewSubject file, one disposition each.
    authoritative_paths: set[str] = set()
    for f in subject.files:
        authoritative_paths.add(f.path)
        if f.status == "deleted" or f.kind == KIND_DELETED:
            tombstones.append(TombstoneRecordV1(path=f.path, base_sha256=f.base_sha256))
            continue
        if f.kind in (KIND_DIRECTORY, KIND_SPECIAL):
            blocked.append(BlockedRecordV1(
                path=f.path, reason=f"authoritative path is a {f.kind}, which the package cannot "
                                     f"represent as a file"))
            continue
        if f.kind == KIND_SYMLINK and symlink_escapes_repository(
                repo_root, f.path, f.link_target or ""):
            blocked.append(BlockedRecordV1(
                path=f.path, reason="authoritative symlink points outside the repository"))
            continue
        km = _member_kind_mode_for(f)
        if km is None:
            blocked.append(BlockedRecordV1(
                path=f.path, reason=f"authoritative path has unpackageable kind {f.kind!r}"))
            continue
        kind, mode = km
        members[f.path] = ArchiveMemberV1(
            archive_path=f.path, kind=kind, mode=mode, authoritative=True,
            source_root=str(repo_root), source_rel=f.path,
            expected_sha256=(f.current_sha256 if kind == MEMBER_REGULAR else None),
            expected_link_target=(f.link_target if kind == MEMBER_SYMLINK else None))

    # 2. A CHANGED path the bundle policy excluded must block, not disappear. `is_authoritative_
    #    source` is the shared predicate; a subject path it accepts but the context list omits
    #    (and which is not otherwise planned) is a silent drop.
    for f in subject.files:
        if f.path in members or any(t.path == f.path for t in tombstones):
            continue
        if any(b.path == f.path for b in blocked):
            continue
        if is_authoritative_source(f.path):
            blocked.append(BlockedRecordV1(
                path=f.path, reason="authoritative changed path is excluded by the bundle "
                                    "policy and would be silently omitted"))

    # 3. The repository context — every bundle file, typed at plan time from its on-disk kind.
    #    An authoritative regular/symlink already planned above wins; context only ADDS.
    for rel in repo_context_rel:
        if rel in members:
            continue
        # A context path must be a safe relative path under the root — a `..` or absolute entry
        # is a hostile archive name, blocked, never silently skipped.
        if rel.startswith("/") or any(seg in ("", "..", ".") for seg in rel.split("/")):
            blocked.append(BlockedRecordV1(
                path=rel, reason="repository bundle path is not a safe relative path"))
            continue
        disk = repo_root / rel
        try:
            st = disk.lstat()
        except OSError:
            continue
        if stat.S_ISLNK(st.st_mode):
            members[rel] = ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_SYMLINK, mode=MODE_SYMLINK,
                authoritative=rel in authoritative_paths, source_root=str(repo_root),
                source_rel=rel)
        elif stat.S_ISREG(st.st_mode):
            mode = MODE_EXECUTABLE if (st.st_mode & 0o111) else MODE_REGULAR
            members[rel] = ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_REGULAR, mode=mode,
                authoritative=rel in authoritative_paths, source_root=str(repo_root),
                source_rel=rel)
        else:
            blocked.append(BlockedRecordV1(
                path=rel, reason="repository bundle path is neither a regular file nor a symlink"))

    evidence_members: list[ArchiveMemberV1] = []
    if evidence_root is not None:
        for rel in evidence_rel:
            evidence_members.append(ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=False,
                source_root=str(evidence_root), source_rel=rel))

    return ArchivePlanV1(
        repository_members=tuple(sorted(members.values(), key=lambda m: m.archive_path)),
        evidence_members=tuple(evidence_members),
        tombstones=tuple(sorted(tombstones, key=lambda t: t.path)),
        blocked_records=tuple(sorted(blocked, key=lambda b: b.path)))
