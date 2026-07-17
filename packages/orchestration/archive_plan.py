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

#: F1 (round 19): a member's SOURCE, kept distinct from its authority. A repository source file
#: that is part of the reviewed change is `authoritative=True`; operator state and bundle context
#: are not. Authority is passed in explicitly (the Content-Proof set), never inferred from mere
#: ReviewSubject membership.
SOURCE_REPOSITORY = "repository"
SOURCE_EVIDENCE = "evidence"
SOURCE_GENERATED_MANIFEST = "generated_manifest"
SOURCE_OPERATOR_CONTEXT = "operator_context"

#: F7 (round 19): the bundle-SAFETY policy — decided per path BEFORE any byte is read, kept
#: SEPARATE from the authority policy (`is_attestable_source` decides authority, never whether
#: bytes may enter). A `.env`/key/log/archive changed inside the reviewed tree is BLOCK_SENSITIVE;
#: `.agent` state is OPERATOR_CONTEXT (included, non-authoritative); a deletion is a TOMBSTONE; an
#: unrepresentable kind is BLOCK_UNSUPPORTED; everything else INCLUDE.
DISP_INCLUDE = "include"
DISP_OPERATOR_CONTEXT = "operator_context"
DISP_TOMBSTONE = "tombstone"
DISP_BLOCK_SENSITIVE = "block_sensitive"
DISP_BLOCK_UNSUPPORTED = "block_unsupported"

#: Suffixes whose CHANGED bytes must never enter the archive — secrets and heavy/opaque blobs.
_SENSITIVE_SUFFIXES = (
    ".env", ".pem", ".key", ".p12", ".pfx", ".crt", ".cer", ".der", ".keystore", ".jks",
    ".log", ".zip", ".tar", ".tar.gz", ".tgz", ".gz", ".bz2", ".7z", ".rar",
    ".pyc", ".pyo", ".so", ".o", ".a", ".dylib", ".dll", ".exe", ".bin",
)
_SENSITIVE_NAMES = frozenset({
    "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", ".env", "credentials.json",
    "service-account.json", "service_account.json", "client_secret.json",
    "firebase-adminsdk.json", "settings.local.json",
})
#: Operator-state directory prefix — included as non-authoritative context, never blocked.
_OPERATOR_STATE_PREFIX = ".agent/"

#: F12 (round 19): the bounded archive contract. Values chosen for the current Remedy repository
#: (~1,400 members, largest source file well under 1 MiB, total tree a few MiB) with generous
#: headroom for F140's recorded-stream and demo assets, while still refusing a runaway/zip-bomb
#: input. Every limit is enforced BEFORE the dangerous allocation and reported as a safe block.
MAX_REPOSITORY_MEMBERS = 20_000        # ~14x the current tree
MAX_EVIDENCE_MEMBERS = 20_000
MAX_MEMBER_BYTES = 64 * 1024 * 1024    # one regular member: 64 MiB (F140 recorded streams cap 50 MiB)
MAX_TOTAL_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024   # 2 GiB across the whole archive
MAX_SYMLINK_TARGET_BYTES = 4096        # PATH_MAX
MAX_ARCHIVE_NAME_BYTES = 4096
MAX_COMPRESSION_RATIO = 200            # a member expanding >200x on read is a bomb


def classify_bundle_path(rel: str, *, changed: bool, is_authoritative_source) -> str:
    """The bundle-safety disposition of one repository path (F7).

    `changed` is True when the path is part of the reviewed change (in the ReviewSubject).
    Sensitivity only BLOCKS a CHANGED path — an unchanged context blob is simply not in the
    bundle. Operator state is always context. The decision is made from the path alone, before
    any read.
    """
    norm = rel.replace("\\", "/")
    if norm.startswith(_OPERATOR_STATE_PREFIX):
        return DISP_OPERATOR_CONTEXT
    base = norm.rsplit("/", 1)[-1]
    low = base.lower()
    if changed:
        if base in _SENSITIVE_NAMES or low in _SENSITIVE_NAMES:
            return DISP_BLOCK_SENSITIVE
        if any(low.endswith(sfx) for sfx in _SENSITIVE_SUFFIXES):
            return DISP_BLOCK_SENSITIVE
    return DISP_INCLUDE


class ArchivePlanError(Exception):
    """The package cannot be planned safely. Never downgraded to a warning."""


@dataclass(frozen=True)
class ArchiveMemberV1:
    """One planned ZIP member, fully typed BEFORE anything is written or read."""
    archive_path: str
    kind: str                       # MEMBER_REGULAR | MEMBER_SYMLINK
    mode: int                       # unix permission bits (0o644 / 0o755 / 0o777)
    authoritative: bool             # part of the reviewed change (the Content-Proof set)
    source_root: str                # the anchored root this member is read under
    source_rel: str                 # the path relative to source_root
    #: F1 (round 19): what this member IS, distinct from whether it is authoritative.
    source_class: str = SOURCE_REPOSITORY
    #: For an authoritative record, the content hash / link target the ReviewSubject declared.
    expected_sha256: str | None = None
    expected_link_target: str | None = None

    def to_json(self) -> dict:
        # F2 (round 19): the packaged plan carries NO local absolute source_root.
        return {"archive_path": self.archive_path, "kind": self.kind, "mode": self.mode,
                "authoritative": self.authoritative, "source_class": self.source_class,
                "content_sha256": self.expected_sha256,
                "link_target": self.expected_link_target}


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
    review_subject_sha256: str = ""
    authority_set_sha256: str = ""
    plan_v: int = PLAN_VERSION

    @property
    def blocked(self) -> bool:
        return bool(self.blocked_records)

    def authoritative_members(self) -> tuple[ArchiveMemberV1, ...]:
        return tuple(m for m in self.all_members() if m.authoritative)

    def authoritative_paths(self) -> set[str]:
        return ({m.archive_path for m in self.authoritative_members()}
                | {t.path for t in self.tombstones})

    def expected_member_count(self) -> int:
        return len(self.repository_members) + len(self.evidence_members)

    def all_members(self) -> tuple[ArchiveMemberV1, ...]:
        return self.repository_members + self.evidence_members

    def to_json(self) -> dict:
        return {"plan_v": self.plan_v,
                "review_subject_sha256": self.review_subject_sha256,
                "authority_set_sha256": self.authority_set_sha256,
                "expected_member_count": self.expected_member_count(),
                "repository_members": [m.to_json() for m in self.repository_members],
                "evidence_members": [m.to_json() for m in self.evidence_members],
                "tombstones": [t.to_json() for t in self.tombstones],
                "blocked_records": [b.to_json() for b in self.blocked_records]}


def _member_kind_mode_for(f) -> tuple[str, int] | None:
    """The ZIP (kind, mode) a ReviewSubject file's CURRENT side maps to, or None if unpackageable.

    F3 (round 19): the mode comes from the file's CURRENT git mode; a dirty regular file whose
    working-tree executable bit is set maps to 0755 (the record captured it), else 0644.
    """
    if f.kind == KIND_SYMLINK:
        return (MEMBER_SYMLINK, MODE_SYMLINK)
    if f.kind == KIND_REGULAR:
        mapped = _GIT_MODE_TO_MEMBER.get(f.current_mode or "")
        if mapped is not None:
            return mapped
        return (MEMBER_REGULAR, MODE_REGULAR)
    return None


def _sha256_hex(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def build_archive_plan(*, repo_root: str | Path, subject: ReviewSubjectV1,
                       repo_context_rel: list[str], evidence_root: str | Path | None,
                       evidence_rel: list[str], authoritative_paths: set[str],
                       is_authoritative_source=None) -> ArchivePlanV1:
    """Assemble the one typed plan from the ONE authority set (F1, round 19).

    * ``subject`` — the reviewed change; each file gets one disposition.
    * ``authoritative_paths`` — THE authority set, passed in EXPLICITLY: exactly the Content-Proof
      / final-verifier / change-provenance file set (18 files, `.agent` state excluded). A member
      is `authoritative` iff its path is in this set — never inferred from ReviewSubject membership.
    * ``repo_context_rel`` — the repository bundle context files; a context path not in the
      authority set rides along as non-authoritative context.

    Bundle SAFETY (F7) is decided by `classify_bundle_path` before any read, kept separate from
    authority. `is_authoritative_source` is retained only for back-compat callers and ignored.
    """
    import json as _json

    repo_root = Path(repo_root)
    context = set(repo_context_rel)
    members: dict[str, ArchiveMemberV1] = {}
    tombstones: list[TombstoneRecordV1] = []
    blocked: list[BlockedRecordV1] = []

    def _is_auth(p: str) -> bool:
        return p in authoritative_paths

    def _source_class(p: str, auth: bool) -> str:
        if p.replace("\\", "/").startswith(_OPERATOR_STATE_PREFIX):
            return SOURCE_OPERATOR_CONTEXT
        return SOURCE_REPOSITORY

    # 1. The reviewed change — every ReviewSubject file, one disposition each.
    for f in subject.files:
        disp = classify_bundle_path(f.path, changed=True,
                                    is_authoritative_source=_is_auth)
        if f.status == "deleted" or f.kind == KIND_DELETED:
            tombstones.append(TombstoneRecordV1(path=f.path, base_sha256=f.base_sha256))
            continue
        if disp == DISP_BLOCK_SENSITIVE:
            blocked.append(BlockedRecordV1(
                path=f.path, reason="changed sensitive path (secret/key/log/archive/binary); "
                                    "its bytes must never enter the package"))
            continue
        if f.kind in (KIND_DIRECTORY, KIND_SPECIAL):
            blocked.append(BlockedRecordV1(
                path=f.path, reason=f"path is a {f.kind}, which the package cannot represent as "
                                     f"a file"))
            continue
        if f.kind == KIND_SYMLINK and symlink_escapes_repository(
                repo_root, f.path, f.link_target or ""):
            blocked.append(BlockedRecordV1(
                path=f.path, reason="symlink points outside the repository"))
            continue
        km = _member_kind_mode_for(f)
        if km is None:
            blocked.append(BlockedRecordV1(
                path=f.path, reason=f"path has unpackageable kind {f.kind!r}"))
            continue
        kind, mode = km
        auth = _is_auth(f.path)
        members[f.path] = ArchiveMemberV1(
            archive_path=f.path, kind=kind, mode=mode, authoritative=auth,
            source_root=str(repo_root), source_rel=f.path,
            source_class=_source_class(f.path, auth),
            expected_sha256=(f.current_sha256 if kind == MEMBER_REGULAR else None),
            expected_link_target=(f.link_target if kind == MEMBER_SYMLINK else None))

    # 2. The repository context — bundle files, typed at plan time from their on-disk kind.
    for rel in repo_context_rel:
        if rel in members:
            continue
        if rel.startswith("/") or any(seg in ("", "..", ".") for seg in rel.split("/")):
            blocked.append(BlockedRecordV1(
                path=rel, reason="repository bundle path is not a safe relative path"))
            continue
        auth = _is_auth(rel)
        # A CHANGED sensitive path already blocked above (it is in the subject). An UNCHANGED
        # context blob is not sensitive-blocked — it is not part of the review — but operator
        # state is still classed as context.
        sclass = _source_class(rel, auth)
        disk = repo_root / rel
        try:
            st = disk.lstat()
        except OSError:
            continue
        if stat.S_ISLNK(st.st_mode):
            members[rel] = ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_SYMLINK, mode=MODE_SYMLINK, authoritative=auth,
                source_root=str(repo_root), source_rel=rel, source_class=sclass)
        elif stat.S_ISREG(st.st_mode):
            mode = MODE_EXECUTABLE if (st.st_mode & 0o111) else MODE_REGULAR
            members[rel] = ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_REGULAR, mode=mode, authoritative=auth,
                source_root=str(repo_root), source_rel=rel, source_class=sclass)
        else:
            blocked.append(BlockedRecordV1(
                path=rel, reason="repository bundle path is neither a regular file nor a symlink"))

    evidence_members: list[ArchiveMemberV1] = []
    if evidence_root is not None:
        for rel in evidence_rel:
            evidence_members.append(ArchiveMemberV1(
                archive_path=rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR, authoritative=False,
                source_root=str(evidence_root), source_rel=rel, source_class=SOURCE_EVIDENCE))

    # F12: member-count limits, before the ZIP is built.
    if len(members) > MAX_REPOSITORY_MEMBERS:
        blocked.append(BlockedRecordV1(
            path="<archive>", reason=f"repository member count {len(members)} exceeds "
                                     f"{MAX_REPOSITORY_MEMBERS}"))
    if len(evidence_members) > MAX_EVIDENCE_MEMBERS:
        blocked.append(BlockedRecordV1(
            path="<archive>", reason=f"evidence member count {len(evidence_members)} exceeds "
                                     f"{MAX_EVIDENCE_MEMBERS}"))

    subj_sha = _sha256_hex(_json.dumps(subject.to_json(), sort_keys=True).encode())
    auth_sha = _sha256_hex(_json.dumps(sorted(authoritative_paths)).encode())
    return ArchivePlanV1(
        repository_members=tuple(sorted(members.values(), key=lambda m: m.archive_path)),
        evidence_members=tuple(evidence_members),
        tombstones=tuple(sorted(tombstones, key=lambda t: t.path)),
        blocked_records=tuple(sorted(blocked, key=lambda b: b.path)),
        review_subject_sha256=subj_sha, authority_set_sha256=auth_sha)
