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
from dataclasses import dataclass
from pathlib import Path

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
DISP_EXCLUDE_SAFE_CONTEXT = "exclude_safe_context"   # F5 (round 21): unchanged sensitive context
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
#: F5 (round 23): the review-package build-output basename prefix (a prior `remedy-review-*.zip` and
#: its `.sha256` sidecar). Classified EXCLUDE_SAFE_CONTEXT so a prior output cannot recurse.
_BUILD_OUTPUT_PREFIX = "remedy-review-"

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
#: F9/F10 (round 20): the Evidence tree is bounded DURING the no-follow inventory walk, before the
#: whole tree is copied, and the directed-chain generated artifacts are bounded as members too.
MAX_EVIDENCE_AGGREGATE_BYTES = 2 * 1024 * 1024 * 1024   # 2 GiB across staged Evidence
MAX_GENERATED_MEMBER_BYTES = 16 * 1024 * 1024          # plan / expectation / manifest each ≤ 16 MiB


def classify_bundle_path(rel: str, *, changed: bool, kind: str | None = None,
                         source_class: str | None = None, is_authoritative_source=None) -> str:
    """The ONE bundle-safety disposition of one repository path (F7, r19; F6/F7, r20).

    The decision is made from the path alone, BEFORE any read, and it is the SAME policy for a
    changed member and for unchanged bundle context (round 20 F7): a sensitive path — a `.env`, a
    key, a certificate, a log, an old archive, a binary — never enters the package whether or not it
    is part of the reviewed change. Operator state is always context. ``kind``/``source_class`` are
    accepted so every caller invokes one signature; ``is_authoritative_source`` is ignored
    (disposition is independent of authority).
    """
    norm = rel.replace("\\", "/")
    if norm.startswith(_OPERATOR_STATE_PREFIX):
        return DISP_OPERATOR_CONTEXT
    base = norm.rsplit("/", 1)[-1]
    low = base.lower()
    # F5 (round 23): a PRIOR review package (or its .sha256 sidecar) is a build output, identified
    # explicitly — never packaged (a previous output must not recurse into the new one), and never
    # silently absent: it gets an explicit safe-context exclusion.
    if base.startswith(_BUILD_OUTPUT_PREFIX):
        return DISP_EXCLUDE_SAFE_CONTEXT
    _sensitive = (base in _SENSITIVE_NAMES or low in _SENSITIVE_NAMES
                  or any(low.endswith(sfx) for sfx in _SENSITIVE_SUFFIXES))
    if _sensitive:
        # F5 (round 21): a CHANGED sensitive path is a hard block (its bytes were part of the review
        # and must never enter); an UNCHANGED sensitive context path is safely EXCLUDED with an
        # explicit disposition — never packaged, never silently absent.
        return DISP_BLOCK_SENSITIVE if changed else DISP_EXCLUDE_SAFE_CONTEXT
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
    #: F4 (round 23): the exact uncompressed byte length bound after the snapshot read.
    expected_size: int | None = None

    def to_json(self) -> dict:
        # F2 (round 19): the packaged plan carries NO local absolute source_root.
        return {"archive_path": self.archive_path, "kind": self.kind, "mode": self.mode,
                "authoritative": self.authoritative, "source_class": self.source_class,
                "content_sha256": self.expected_sha256, "expected_size": self.expected_size,
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
class ExcludedRecordV1:
    """F5 (round 21): an unchanged sensitive CONTEXT path that is safely EXCLUDED — never packaged,
    but recorded with an explicit disposition so it never silently disappears."""
    path: str
    disposition: str
    reason: str

    def to_json(self) -> dict:
        return {"path": self.path, "disposition": self.disposition, "reason": self.reason}


@dataclass(frozen=True)
class ArchivePlanV1:
    repository_members: tuple[ArchiveMemberV1, ...] = ()
    evidence_members: tuple[ArchiveMemberV1, ...] = ()
    tombstones: tuple[TombstoneRecordV1, ...] = ()
    blocked_records: tuple[BlockedRecordV1, ...] = ()
    excluded_records: tuple[ExcludedRecordV1, ...] = ()
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
                "excluded_records": [e.to_json() for e in self.excluded_records],
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
                       review_subject_raw_sha256: str | None = None,
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
    excluded: list[ExcludedRecordV1] = []

    def _is_operator_state(p: str) -> bool:
        return p.replace("\\", "/").startswith(_OPERATOR_STATE_PREFIX)

    def _is_auth(p: str) -> bool:
        # F2 (round 20): `.agent` operator state is FORCIBLY non-authoritative even if a forged
        # Content Proof names it. Authority is the proof set MINUS operator state, always.
        return p in authoritative_paths and not _is_operator_state(p)

    def _source_class(p: str, auth: bool) -> str:
        if _is_operator_state(p):
            return SOURCE_OPERATOR_CONTEXT
        return SOURCE_REPOSITORY

    # 1. The reviewed change — every ReviewSubject file, one disposition each.
    for f in subject.files:
        disp = classify_bundle_path(f.path, changed=True, kind=f.kind)
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
        # F5 (round 21): ONE disposition owner. An unchanged sensitive context path is SAFELY
        # EXCLUDED with an explicit record (never packaged, never silently absent); a CHANGED
        # sensitive path is caught in the subject loop above.
        disp = classify_bundle_path(rel, changed=False)
        if disp == DISP_EXCLUDE_SAFE_CONTEXT:
            excluded.append(ExcludedRecordV1(
                path=rel, disposition=DISP_EXCLUDE_SAFE_CONTEXT,
                reason="unchanged sensitive context (secret/key/log/archive/binary); excluded"))
            continue
        auth = _is_auth(rel)
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
            # F5 (round 21): a FIFO/socket/device context path gets an EXPLICIT BLOCK_UNSUPPORTED
            # record — it cannot silently disappear before the ArchivePlan.
            blocked.append(BlockedRecordV1(
                path=rel, reason=f"BLOCK_UNSUPPORTED: context path is a special file "
                                 f"({stat.filemode(st.st_mode)}), which the package cannot "
                                 f"represent as a member"))

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

    # F2 (round 21): the subject identity is the RAW packaged bytes' sha256, passed in explicitly —
    # never a hash of a reserialized `subject.to_json()` (which differs from the packaged member).
    # A missing raw sha (direct callers / context-only builds) keeps the legacy reserialized value.
    if review_subject_raw_sha256 is not None:
        subj_sha = review_subject_raw_sha256
    else:
        subj_sha = _sha256_hex(_json.dumps(subject.to_json(), sort_keys=True).encode())
    auth_sha = _sha256_hex(_json.dumps(sorted(authoritative_paths)).encode())
    return ArchivePlanV1(
        repository_members=tuple(sorted(members.values(), key=lambda m: m.archive_path)),
        evidence_members=tuple(evidence_members),
        tombstones=tuple(sorted(tombstones, key=lambda t: t.path)),
        blocked_records=tuple(sorted(blocked, key=lambda b: b.path)),
        excluded_records=tuple(sorted(excluded, key=lambda e: e.path)),
        review_subject_sha256=subj_sha, authority_set_sha256=auth_sha)
