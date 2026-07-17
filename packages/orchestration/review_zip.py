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


def _add_regular(zf: zipfile.ZipFile, arcname: str, disk_path: Path) -> str:
    """Add one regular file's own bytes; return the sha256 of what was written."""
    data = disk_path.read_bytes()
    # Deterministic member metadata — a fixed timestamp so two builds of the same tree match.
    info = zipfile.ZipInfo(filename=arcname, date_time=(1980, 1, 1, 0, 0, 0))
    info.external_attr = 0o644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)
    return hashlib.sha256(data).hexdigest()


def build_review_zip(*, out_path: str | Path, repo_root: str | Path,
                     repo_files: list[str], evidence_root: str | Path | None,
                     evidence_files: list[str], manifest_rel: str,
                     manifest_disk: str | Path) -> dict:
    """Build the archive from an EXACT typed model and return what was written.

    * `repo_files` — relative POSIX paths under `repo_root`;
    * `evidence_files` — relative POSIX paths (already `evidence/...`-prefixed) under
      `evidence_root`;
    * `manifest_rel` / `manifest_disk` — the `.review_zip_manifest.json` member and its source.

    Every archive name is validated and de-duplicated BEFORE anything is written; a symlink is
    never followed; the result reports the member set and per-member hashes so the caller (and
    `verify_review_zip`) can hold the archive to it.
    """
    repo_root = Path(repo_root)
    written: dict[str, str] = {}          # arcname -> sha256 (regular) or "" (symlink metadata)
    symlinks: dict[str, str] = {}         # arcname -> link target text
    seen: set[str] = set()

    def _claim(arcname: str) -> None:
        validate_archive_name(arcname)
        if arcname in seen:
            raise ReviewZipError(f"duplicate archive member: {arcname!r}")
        seen.add(arcname)

    out_path = Path(out_path)
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in repo_files:
            arcname = rel
            _claim(arcname)
            disk = repo_root / rel
            if not contained(repo_root, disk):
                raise ReviewZipError(f"repository file escapes the root: {rel!r}")
            st = os.lstat(disk)            # NEVER follow
            if stat.S_ISLNK(st.st_mode):
                # F8 policy: a symlink is recorded as its target TEXT, never dereferenced.
                target = os.readlink(disk)
                info = zipfile.ZipInfo(filename=arcname, date_time=(1980, 1, 1, 0, 0, 0))
                # 0o120000 marks a symlink member; the body is the target text.
                info.external_attr = (0o120000 | 0o777) << 16
                zf.writestr(info, target.encode("utf-8", errors="surrogateescape"))
                symlinks[arcname] = target
                written[arcname] = ""
            elif stat.S_ISREG(st.st_mode):
                written[arcname] = _add_regular(zf, arcname, disk)
            else:
                raise ReviewZipError(
                    f"repository path {rel!r} is neither a regular file nor a symlink")

        if evidence_root is not None:
            evidence_root = Path(evidence_root)
            for rel in evidence_files:
                arcname = rel
                _claim(arcname)
                disk = evidence_root / rel
                if not contained(evidence_root, disk):
                    raise ReviewZipError(f"evidence file escapes its staging root: {rel!r}")
                st = os.lstat(disk)
                if not stat.S_ISREG(st.st_mode):
                    raise ReviewZipError(f"evidence path {rel!r} is not a regular file")
                written[arcname] = _add_regular(zf, arcname, disk)

        _claim(manifest_rel)
        written[manifest_rel] = _add_regular(zf, manifest_rel, Path(manifest_disk))

    return {"members": sorted(written), "hashes": written, "symlinks": symlinks}


# --------------------------------------------------------------------------- verifying


def verify_review_zip(out_path: str | Path, expected: dict) -> list[str]:
    """F10: reopen the archive and hold every member to the typed model.

    Compares the member SET exactly (no missing, extra or duplicate), re-hashes every regular
    member against what was written, and re-reads every symlink member's target text.
    """
    problems: list[str] = []
    expected_hashes: dict[str, str] = expected["hashes"]
    expected_symlinks: dict[str, str] = expected.get("symlinks", {})

    with zipfile.ZipFile(out_path, "r") as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            problems.append("archive contains duplicate member names")
        actual = set(names)
        expected_set = set(expected_hashes)
        for missing in sorted(expected_set - actual):
            problems.append(f"expected member missing from archive: {missing!r}")
        for extra in sorted(actual - expected_set):
            problems.append(f"unexpected member in archive: {extra!r}")

        for name in sorted(actual & expected_set):
            data = zf.read(name)
            if name in expected_symlinks:
                if data.decode("utf-8", errors="surrogateescape") != expected_symlinks[name]:
                    problems.append(f"symlink member {name!r} target changed after build")
            else:
                got = hashlib.sha256(data).hexdigest()
                if got != expected_hashes[name]:
                    problems.append(f"member {name!r} hash changed after build")
    return problems
