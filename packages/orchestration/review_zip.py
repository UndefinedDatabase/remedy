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
import posixpath
import stat
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
    info.external_attr = (_S_IFREG | (mode & 0o7777)) << 16      # F2: real file-type + perm bits
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def _write_symlink(zf: zipfile.ZipFile, arcname: str, target: bytes) -> None:
    info = zipfile.ZipInfo(filename=arcname, date_time=_FIXED_TS)
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
        is_authoritative_source=lambda _p: False)
    return build_review_zip_from_plan(out_path=out_path, plan=plan, manifest_rel=manifest_rel,
                                      manifest_disk=manifest_disk)


def build_review_zip_from_plan(*, out_path: str | Path, plan, manifest_rel: str,
                               manifest_disk: str | Path) -> dict:
    """Build the archive from ONE typed ArchivePlanV1 (F1) and return the exact member model.

    Every member is read through the anchored, atomically no-follow reader (F3), written with its
    planned kind and mode (F2), and — for an authoritative member — checked against the content
    hash / link target the ReviewSubject declared. The returned model is what `verify_review_zip`
    holds the reopened archive to (F6).

    A BLOCKED plan is refused before a single byte is written.
    """
    from packages.common import secure_fs as _fs

    if plan.blocked:
        reasons = "; ".join(f"{b.path}: {b.reason}" for b in plan.blocked_records[:4])
        raise ReviewZipError(f"the archive plan is BLOCKED and cannot be packaged: {reasons}")

    seen: set[str] = set()
    model: dict[str, dict] = {}       # arcname -> {kind, mode, sha256|link_target, authoritative}

    def _claim(arcname: str) -> None:
        validate_archive_name(arcname)
        _require_utf8_archive_name(arcname)
        if arcname in seen:
            raise ReviewZipError(f"duplicate archive member: {arcname!r}")
        seen.add(arcname)

    out_path = Path(out_path)
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for member in plan.all_members():
            arcname = member.archive_path
            _claim(arcname)
            if not contained(member.source_root, str(Path(member.source_root)
                                                     / member.source_rel)):
                raise ReviewZipError(f"planned member escapes its root: {arcname!r}")
            vf = _fs.read_verified_relative(
                member.source_root, member.source_rel,
                expected_kind=("symlink" if member.kind == "symlink" else "regular"),
                error_cls=ReviewZipError, noun="archive member")
            if member.kind == "symlink":
                target = vf.data.decode("utf-8", errors="surrogateescape")
                if member.authoritative and member.expected_link_target is not None \
                        and target != member.expected_link_target:
                    raise ReviewZipError(
                        f"authoritative symlink {arcname!r} target {target!r} != the subject's "
                        f"{member.expected_link_target!r}")
                _write_symlink(zf, arcname, vf.data)
                model[arcname] = {"kind": "symlink", "mode": 0o777, "link_target": target,
                                  "authoritative": member.authoritative}
            else:
                digest = hashlib.sha256(vf.data).hexdigest()
                if member.authoritative and member.expected_sha256 is not None \
                        and digest != member.expected_sha256:
                    raise ReviewZipError(
                        f"authoritative file {arcname!r} hashes to {digest[:12]} but the subject "
                        f"declared {str(member.expected_sha256)[:12]}")
                _write_regular(zf, arcname, vf.data, member.mode)
                model[arcname] = {"kind": "regular", "mode": member.mode & 0o7777,
                                  "sha256": digest, "authoritative": member.authoritative}

        _claim(manifest_rel)
        mbytes = Path(manifest_disk).read_bytes()
        _write_regular(zf, manifest_rel, mbytes, 0o644)
        model[manifest_rel] = {"kind": "regular", "mode": 0o644,
                               "sha256": hashlib.sha256(mbytes).hexdigest(),
                               "authoritative": False}

    return {"members": sorted(model), "model": model}


# --------------------------------------------------------------------------- verifying


def verify_review_zip(out_path: str | Path, expected: dict) -> list[str]:
    """F6/F10: reopen the archive and hold every member to the TYPED model — kind, mode, bytes.

    Round 17 checked names, bodies and symlink text; a regular member containing the correct link
    text passed as a symlink, and a mode was never checked. This verifies the exact name multiset,
    the unix file TYPE and permission bits from `external_attr`, the deterministic timestamp, and
    then the body (hash for a regular, target text for a symlink) — so a member's declared kind and
    mode must match what was actually written.
    """
    problems: list[str] = []
    model: dict[str, dict] = expected["model"]

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
            file_type = (info.external_attr >> 16) & 0o170000
            perm = (info.external_attr >> 16) & 0o7777
            data = zf.read(name)
            if want["kind"] == "symlink":
                if file_type != _S_IFLNK:
                    problems.append(f"member {name!r} is not a symlink type (a regular member "
                                    f"cannot satisfy a symlink record)")
                    continue
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
