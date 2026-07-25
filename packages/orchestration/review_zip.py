"""F8/F9/F10 (round 17) — build the review ZIP from an EXACT, path-safe file model.

The review ZIP was assembled with `find -print | sort | zip -@`. That pipeline is newline-delimited
end to end, so a filename containing a newline is silently truncated or dropped — the typed
ReviewSubject is NUL-safe, the archive that is supposed to represent it is not, and a path can go
missing between them with nothing to notice. The post-build check (`unzip -Z1 | grep`) has the same
blind spot.

This module replaces the repository-file archive stage with a `zipfile` builder driven by an
EXPLICIT list of relative POSIX paths (discovered NUL-safely upstream), plus:

* F9 — containment decided by `os.path.commonpath`, not a string prefix, so a sibling directory
  `repo-evil` is never mistaken for being inside `repo`;
* F10 — after the archive is written it is REOPENED and its member set compared exactly against
  the model: no authoritative path omitted, no unlisted path present, no duplicate.

Symlinks are never followed: a repository file that is a symlink is recorded by policy (its target
text), never dereferenced into the archive.
"""
from __future__ import annotations

import hashlib
import os
import zipfile
from pathlib import Path


class ReviewZipError(Exception):
    """The archive cannot be built or verified safely. Never downgraded to a warning."""


# --------------------------------------------------------------------------- names


def validate_archive_name(name: str) -> None:
    """A ZIP archive member name must be a safe RELATIVE POSIX path.

    Newline, tab, quote, leading-dash and Unicode characters are all FINE — preserving them is the
    point. What is refused is anything that changes WHERE the member lands: an absolute path, a
    `..` segment, an empty segment (`a//b`), a `.` segment, a drive/backslash, or a NUL.
    """
    if not name:
        raise ReviewZipError("empty archive name")
    if name.startswith("/"):
        raise ReviewZipError(f"absolute archive name: {name!r}")
    if "\\" in name:
        raise ReviewZipError(f"backslash in archive name: {name!r}")
    if "\0" in name:
        raise ReviewZipError(f"NUL in archive name: {name!r}")
    segments = name.split("/")
    for seg in segments:
        if seg == "":
            raise ReviewZipError(f"empty path segment in archive name: {name!r}")
        if seg in (".", ".."):
            raise ReviewZipError(f"relative path segment {seg!r} in archive name: {name!r}")


def contained(root: str | Path, candidate: str | Path) -> bool:
    """Is `candidate` inside `root`, decided by PATH COMPONENTS?

    F9: `candidate.startswith(root)` accepts `/tmp/x/repo-evil` for root `/tmp/x/repo` — a sibling
    whose name merely starts with the root's. `os.path.commonpath` compares real components, so a
    sibling, a different drive, or an unrelated tree is refused. Paths are resolved with symlinks
    first, so a symlinked descendant that escapes the root is refused too.
    """
    try:
        r = os.path.realpath(str(root))
        c = os.path.realpath(str(candidate))
    except OSError:
        return False
    if c == r:
        return True
    try:
        return os.path.commonpath([r, c]) == r
    except ValueError:
        # Different drives / mixed absolute-relative — not comparable, so not contained.
        return False


# --------------------------------------------------------------------------- reading NUL lists


def read_nul_list(path: str | Path) -> list[str]:
    """Read a NUL-delimited list of relative paths (from `find -print0` / `git ls-files -z`)."""
    raw = Path(path).read_bytes()
    if not raw:
        return []
    parts = raw.split(b"\0")
    out: list[str] = []
    for p in parts:
        if not p:
            continue
        out.append(p.decode("utf-8", errors="surrogateescape"))
    return out


# --------------------------------------------------------------------------- building

#: Deterministic member timestamp — two builds of the same tree produce byte-identical metadata.
_FIXED_TS = (1980, 1, 1, 0, 0, 0)
_S_IFREG = 0o100000
_S_IFLNK = 0o120000


def _require_utf8_archive_name(name: str) -> None:
    """A ZIP member name must be valid UTF-8 — the archive stores Unicode names.

    F18 filename-byte policy: a NUL list is decoded with ``surrogateescape``, so an
    undecodable byte path round-trips as surrogates and would raise an uncontrolled
    ``UnicodeEncodeError`` deep inside ``zipfile``. Refuse it HERE, safely and named.
    """
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        raise ReviewZipError(
            f"archive name is not valid UTF-8 (undecodable repository byte path): {name!r}") \
            from None


def _write_regular(zf: zipfile.ZipFile, arcname: str, data: bytes, mode: int) -> None:
    info = zipfile.ZipInfo(filename=arcname, date_time=_FIXED_TS)
    info.create_system = 3                                       # Unix — where type/perm bits live
    info.external_attr = (_S_IFREG | (mode & 0o7777)) << 16      # F2: real file-type + perm bits
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def _write_symlink(zf: zipfile.ZipFile, arcname: str, target: bytes) -> None:
    info = zipfile.ZipInfo(filename=arcname, date_time=_FIXED_TS)
    info.create_system = 3
    info.external_attr = (_S_IFLNK | 0o777) << 16                # canonical symlink member
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, target)


def build_review_zip(*, out_path: str | Path, repo_root: str | Path,
                     repo_files: list[str], evidence_root: str | Path | None,
                     evidence_files: list[str], manifest_rel: str,
                     manifest_disk: str | Path) -> dict:
    """Convenience wrapper: build a context-only plan (no ReviewSubject) and archive it.

    Used where there is no authoritative subject to drive the plan — every repo/evidence file is
    non-authoritative bundle context. Production packaging goes through `build_archive_plan` +
    `build_review_zip_from_plan` so the authoritative subset is typed; this keeps the direct-call
    path (and its tests) exercising the same builder and verifier.
    """
    from packages.orchestration.archive_plan import build_archive_plan
    from packages.orchestration.review_subject import ReviewSubjectV1

    plan = build_archive_plan(
        repo_root=repo_root, subject=ReviewSubjectV1(), repo_context_rel=repo_files,
        evidence_root=evidence_root, evidence_rel=evidence_files,
        authoritative_paths=set())
    return build_review_zip_from_plan(out_path=out_path, plan=plan, manifest_rel=manifest_rel,
                                      manifest_disk=manifest_disk)


class SnapshotMember:
    """One member's IMMUTABLE snapshot — read ONCE through the anchored no-follow reader, then never
    reopened. The bytes packaged and the bytes hashed are the same object (F3/F5, round 20)."""
    __slots__ = ("arcname", "kind", "mode", "data", "sha256", "link_target", "authoritative",
                 "source_class")

    def __init__(self, arcname, kind, mode, data, sha256, link_target, authoritative,
                 source_class):
        self.arcname = arcname
        self.kind = kind
        self.mode = mode
        self.data = data
        self.sha256 = sha256
        self.link_target = link_target
        self.authoritative = authoritative
        self.source_class = source_class


def snapshot_plan_members(plan) -> dict:
    """Phase 1 (round 20): read EVERY plan source member ONCE into an immutable in-memory snapshot.

    A BLOCKED plan is refused before a byte is read. Each member is read through the anchored,
    atomically no-follow, stability-checked reader; the planned mode is bound to the opened source
    (F4); a symlink's exact target is escape/subject-checked (F6); an authoritative member is held
    to the ReviewSubject's declared hash / link target; per-member and aggregate byte caps apply.
    After this phase, the source tree is never read again — the returned bytes are the single source.
    """
    from packages.common import secure_fs as _fs
    from packages.orchestration.archive_plan import (
        MAX_MEMBER_BYTES,
        MAX_SYMLINK_TARGET_BYTES,
        MAX_TOTAL_UNCOMPRESSED_BYTES,
    )
    from packages.orchestration.review_subject import symlink_escapes_repository

    if plan.blocked:
        reasons = "; ".join(f"{b.path}: {b.reason}" for b in plan.blocked_records[:4])
        raise ReviewZipError(f"the archive plan is BLOCKED and cannot be packaged: {reasons}")

    snapshot: dict[str, SnapshotMember] = {}
    total_bytes = 0
    for member in plan.all_members():
        arcname = member.archive_path
        if arcname in snapshot:
            raise ReviewZipError(f"duplicate planned member: {arcname!r}")
        if not contained(member.source_root, str(Path(member.source_root) / member.source_rel)):
            raise ReviewZipError(f"planned member escapes its root: {arcname!r}")
        vf = _fs.read_verified_relative(
            member.source_root, member.source_rel,
            expected_kind=("symlink" if member.kind == "symlink" else "regular"),
            max_bytes=MAX_MEMBER_BYTES,
            expected_mode=(None if member.kind == "symlink" else member.mode),
            error_cls=ReviewZipError, noun="archive member")
        total_bytes += len(vf.data)
        if total_bytes > MAX_TOTAL_UNCOMPRESSED_BYTES:
            raise ReviewZipError("archive exceeds the total uncompressed byte limit")
        if member.kind == "symlink":
            target = vf.data.decode("utf-8", errors="surrogateescape")
            if len(vf.data) > MAX_SYMLINK_TARGET_BYTES:
                raise ReviewZipError(f"symlink {arcname!r} target is too long")
            if symlink_escapes_repository(member.source_root, arcname, target):
                raise ReviewZipError(
                    f"symlink {arcname!r} target {target[:60]!r} points outside the repository")
            if member.expected_link_target is not None and target != member.expected_link_target:
                raise ReviewZipError(
                    f"symlink {arcname!r} target {target!r} != the declared "
                    f"{member.expected_link_target!r}")
            snapshot[arcname] = SnapshotMember(
                arcname, "symlink", 0o777, vf.data, hashlib.sha256(vf.data).hexdigest(),
                target, member.authoritative, member.source_class)
        else:
            digest = hashlib.sha256(vf.data).hexdigest()
            if member.expected_sha256 is not None and digest != member.expected_sha256:
                raise ReviewZipError(
                    f"member {arcname!r} hashes to {digest[:12]} but the plan declared "
                    f"{str(member.expected_sha256)[:12]}")
            snapshot[arcname] = SnapshotMember(
                arcname, "regular", member.mode & 0o7777, vf.data, digest, None,
                member.authoritative, member.source_class)
    return snapshot


def build_review_zip_from_snapshot(*, out_path: str | Path, snapshot: dict,
                                   generated_members: dict) -> dict:
    """Phase 4 (round 20): write the ZIP ENTIRELY from immutable in-memory bytes.

    ``snapshot`` maps arcname -> SnapshotMember (source bytes). ``generated_members`` maps arcname
    -> (bytes, mode) for the directed-chain artifacts (plan, expectation, manifest). NOTHING is
    reopened by path here, so a source or generated file forged on disk after phase 1/generation
    cannot reach the archive. Returns the exact typed model for the reopen verifier.
    """
    from packages.orchestration.archive_plan import MAX_GENERATED_MEMBER_BYTES

    seen: set[str] = set()
    model: dict[str, dict] = {}

    def _claim(arcname: str) -> None:
        validate_archive_name(arcname)
        _require_utf8_archive_name(arcname)
        if len(arcname.encode("utf-8")) > 4096:      # MAX_ARCHIVE_NAME_BYTES
            raise ReviewZipError(f"archive name is too long: {arcname[:40]!r}...")
        if arcname in seen:
            raise ReviewZipError(f"duplicate archive member: {arcname!r}")
        seen.add(arcname)

    # F1 (round 33): the builder writes into a caller-provided PRIVATE temp path and never deletes a
    # public destination — atomic no-replace publication is the coordinator's responsibility
    # (safe_publish.publish_atomically). The path here is created/truncated by ZipFile 'w'.
    out_path = Path(out_path)

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname in sorted(snapshot):
            m = snapshot[arcname]
            _claim(arcname)
            if m.kind == "symlink":
                _write_symlink(zf, arcname, m.data)
                model[arcname] = {"kind": "symlink", "mode": 0o777, "link_target": m.link_target,
                                  "authoritative": m.authoritative, "size": len(m.data)}
            else:
                _write_regular(zf, arcname, m.data, m.mode)
                model[arcname] = {"kind": "regular", "mode": m.mode & 0o7777, "sha256": m.sha256,
                                  "authoritative": m.authoritative, "size": len(m.data)}
        for arcname in sorted(generated_members):
            data, mode = generated_members[arcname]
            if len(data) > MAX_GENERATED_MEMBER_BYTES:
                raise ReviewZipError(f"generated member {arcname!r} exceeds the generated-byte cap")
            _claim(arcname)
            _write_regular(zf, arcname, data, mode)
            model[arcname] = {"kind": "regular", "mode": mode & 0o7777,
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "authoritative": False, "size": len(data)}

    return {"members": sorted(model), "model": model}


def _read_manifest_no_follow(manifest_disk: str | Path) -> bytes:
    """F6 (round 20): read the manifest through the anchored no-follow reader, so a manifest path
    that is a symlink to an external secret is refused, never followed by a plain ``read_bytes``."""
    from packages.common import secure_fs as _fs
    p = Path(manifest_disk)
    vf = _fs.read_verified_relative(str(p.parent), p.name, expected_kind="regular",
                                    error_cls=ReviewZipError, noun="manifest")
    return vf.data


def build_review_zip_from_plan(*, out_path: str | Path, plan, manifest_rel: str,
                               manifest_disk: str | Path | None = None,
                               manifest_bytes: bytes | None = None,
                               generated_members: dict | None = None) -> dict:
    """Convenience two-phase build: snapshot every source member, then write the ZIP from the
    immutable bytes plus the manifest (and any other generated members) as in-memory bytes.

    The manifest is a generated member: passed directly as ``manifest_bytes`` where the caller has
    them, or read ONCE through the no-follow reader from ``manifest_disk`` (F6) — never a plain
    ``Path.read_bytes`` that would follow a symlinked manifest.
    """
    snapshot = snapshot_plan_members(plan)
    gen = dict(generated_members or {})
    if manifest_bytes is None:
        if manifest_disk is None:
            raise ReviewZipError("no manifest bytes or path supplied")
        manifest_bytes = _read_manifest_no_follow(manifest_disk)
    gen[manifest_rel] = (manifest_bytes, 0o644)
    return build_review_zip_from_snapshot(out_path=out_path, snapshot=snapshot,
                                          generated_members=gen)


# --------------------------------------------------------------------------- verifying


def verify_review_zip(out_path: str | Path, expected: dict) -> list[str]:
    """F6/F10: reopen the archive and hold every member to the TYPED model — kind, mode, bytes.

    Round 17 checked names, bodies and symlink text; a regular member containing the correct link
    text passed as a symlink, and a mode was never checked. This verifies the exact name multiset,
    the unix file TYPE and permission bits from `external_attr`, the deterministic timestamp, and
    then the body (hash for a regular, target text for a symlink) — so a member's declared kind and
    mode must match what was actually written.
    """
    from packages.orchestration.archive_plan import (
        MAX_COMPRESSION_RATIO,
        MAX_MEMBER_BYTES,
        MAX_TOTAL_UNCOMPRESSED_BYTES,
    )
    problems: list[str] = []
    model: dict[str, dict] = expected["model"]
    total_uncompressed = 0

    with zipfile.ZipFile(out_path, "r") as zf:
        infos = zf.infolist()
        names = [i.filename for i in infos]
        if len(names) != len(set(names)):
            problems.append("archive contains duplicate member names")
        actual = set(names)
        expected_set = set(model)
        for missing in sorted(expected_set - actual):
            problems.append(f"expected member missing from archive: {missing!r}")
        for extra in sorted(actual - expected_set):
            problems.append(f"unexpected member in archive: {extra!r}")

        by_name = {i.filename: i for i in infos}
        for name in sorted(actual & expected_set):
            info = by_name[name]
            want = model[name]
            if name.endswith("/") or (info.external_attr >> 16) & 0o170000 == 0o040000:
                problems.append(f"member {name!r} is a directory entry")
                continue
            if info.date_time != _FIXED_TS:
                problems.append(f"member {name!r} has a non-deterministic timestamp "
                                f"{info.date_time}")
            # F4 (round 23): the exact uncompressed byte length is verified from the ZIP itself.
            if "size" in want and info.file_size != want["size"]:
                problems.append(f"member {name!r} uncompressed size {info.file_size} != expected "
                                f"{want['size']}")
            # F11 (round 19): the ZIP-level metadata policy — one create_system, an allowed
            # compression method, no encryption, no unsupported general-purpose flags.
            if info.create_system != 3:              # 3 = Unix; the type/perm bits live there
                problems.append(f"member {name!r} has create_system {info.create_system}, not "
                                f"Unix(3)")
            if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                problems.append(f"member {name!r} uses an unexpected compression method "
                                f"{info.compress_type}")
            if info.flag_bits & 0x1:                 # bit 0 = encrypted
                problems.append(f"member {name!r} is encrypted")
            # F12 (round 19): bound the READ before decompressing — a hostile archive whose header
            # claims a small compressed size can still expand into gigabytes of RAM. Reject a member
            # whose uncompressed size exceeds the per-member cap, whose expansion ratio is bomb-like,
            # or that would push the aggregate past the total cap.
            if info.file_size > MAX_MEMBER_BYTES:
                problems.append(f"member {name!r} uncompressed size {info.file_size} exceeds the "
                                f"per-member cap")
                continue
            if (info.compress_size > 0 and info.file_size > (1 << 20)
                    and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO):
                problems.append(f"member {name!r} expands "
                                f"{info.file_size // max(info.compress_size, 1)}x — a decompression "
                                f"bomb")
                continue
            total_uncompressed += info.file_size
            if total_uncompressed > MAX_TOTAL_UNCOMPRESSED_BYTES:
                problems.append("archive total uncompressed size exceeds the aggregate cap")
                break
            file_type = (info.external_attr >> 16) & 0o170000
            perm = (info.external_attr >> 16) & 0o7777
            data = zf.read(name)
            if want["kind"] == "symlink":
                if file_type != _S_IFLNK:
                    problems.append(f"member {name!r} is not a symlink type (a regular member "
                                    f"cannot satisfy a symlink record)")
                    continue
                # F11: a symlink member's permission bits are verified too — an S_IFLNK|0644
                # must not pass a planned 0777 symlink.
                if perm != (want["mode"] & 0o7777):
                    problems.append(f"symlink member {name!r} mode {perm:o} != expected "
                                    f"{want['mode'] & 0o7777:o}")
                if data.decode("utf-8", errors="surrogateescape") != want["link_target"]:
                    problems.append(f"symlink member {name!r} target changed after build")
            else:
                if file_type != _S_IFREG:
                    problems.append(f"member {name!r} is not a regular-file type (a symlink "
                                    f"member cannot satisfy a regular record)")
                    continue
                if perm != (want["mode"] & 0o7777):
                    problems.append(f"member {name!r} mode {perm:o} != expected "
                                    f"{want['mode'] & 0o7777:o}")
                if hashlib.sha256(data).hexdigest() != want["sha256"]:
                    problems.append(f"member {name!r} hash changed after build")
    return problems
