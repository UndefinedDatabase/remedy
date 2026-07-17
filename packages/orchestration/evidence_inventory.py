"""F8 (round 19) / F1,F3,F9,F10 (round 20) — the typed, no-follow Evidence inventory and snapshot.

Evidence used to be discovered with ``find -type f`` and staged with ``cp``. Both are unsafe:

* ``find -type f`` SILENTLY SKIPS a symlink — a symlink evidence artifact is simply absent from
  the package with nothing said about it, the same parallel-truth failure the repository side had.
* ``cp`` FOLLOWS a symlink — a symlink named ``token.json`` that points at ``/etc/passwd`` (or at a
  provider-secret file outside the evidence tree) is copied into the package as a regular file
  carrying OUTSIDE bytes.

The evidence tree is walked with anchored, ``O_NOFOLLOW`` reads. A symlink, FIFO, socket, or device
anywhere in the tree is BLOCKED (the build fails closed, it is never skipped or followed), a
directory component that is itself a symlink cannot redirect the walk, and every regular member is
staged from the EXACT verified bytes — the same bytes the archive later packages and re-hashes.

Round 20 makes the staging the SINGLE byte source and the immutable snapshot of record:

* ``stage_evidence_snapshot`` copies once, HASHES each member's staged bytes, and returns a typed
  ``StagedMember`` inventory (relative_path, kind, mode, size, sha256, source_class);
* the count and aggregate-byte limits are enforced DURING the walk, before the whole tree is
  copied, so an over-limit tree stops early;
* nothing after staging reopens the original ``EVIDENCE_DIR`` — every consumer reads the snapshot.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from packages.common import secure_fs
from packages.orchestration.archive_plan import (
    MAX_EVIDENCE_AGGREGATE_BYTES,
    MAX_EVIDENCE_MEMBERS,
    MAX_MEMBER_BYTES,
    SOURCE_EVIDENCE,
)

# Evidence never legitimately carries compiled artifacts; keep the historical exclusion.
_SKIP_SUFFIXES = (".pyc", ".pyo")

#: The typed snapshot artifact name, written into the staging root.
SNAPSHOT_INVENTORY_NAME = "evidence_snapshot_inventory.json"


class EvidenceInventoryError(RuntimeError):
    """An evidence tree that cannot be safely inventoried (a symlink/FIFO member, an oversized
    file, an over-limit tree, an unreadable component). The build fails closed rather than skip or
    follow it."""


@dataclass(frozen=True)
class StagedMember:
    """One staged Evidence member — the immutable record of what was copied and its identity."""
    relative_path: str
    kind: str                       # always "regular" (non-regular members BLOCK)
    mode: int                       # 0o644 / 0o755
    size: int
    sha256: str
    source_class: str = SOURCE_EVIDENCE

    def to_json(self) -> dict:
        return {"relative_path": self.relative_path, "kind": self.kind, "mode": self.mode,
                "size": self.size, "sha256": self.sha256, "source_class": self.source_class}


def _walk_regular(parent_fd: int, prefix: str, *, on_file, error_cls, max_bytes: int) -> None:
    """Recurse ``parent_fd`` (a held, anchored directory fd), no-follow. Directories are traversed;
    regular files are handed to ``on_file(rel, name, parent_fd)``; anything else BLOCKS."""
    for name in sorted(os.listdir(parent_fd)):
        rel = f"{prefix}/{name}" if prefix else name
        try:
            st = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise error_cls(f"evidence member {rel!r} could not be inspected: "
                            f"{type(exc).__name__}: {exc}") from exc
        if stat.S_ISDIR(st.st_mode):
            child = secure_fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=error_cls,
                                                noun="evidence directory")
            try:
                _walk_regular(child, rel, on_file=on_file, error_cls=error_cls,
                              max_bytes=max_bytes)
            finally:
                os.close(child)
        elif stat.S_ISREG(st.st_mode):
            if name.endswith(_SKIP_SUFFIXES):
                continue
            on_file(rel, name, parent_fd)
        else:
            raise error_cls(
                f"refusing evidence member {rel!r}: it is not a regular file or directory "
                f"({stat.filemode(st.st_mode)}). Evidence symlinks/FIFOs/devices are never "
                f"skipped or followed — the package fails closed.")


def stage_evidence_snapshot(src_root: str | Path, dest_dir: str | Path, *,
                            source_class: str = SOURCE_EVIDENCE,
                            max_bytes: int = MAX_MEMBER_BYTES,
                            max_members: int = MAX_EVIDENCE_MEMBERS,
                            max_aggregate_bytes: int = MAX_EVIDENCE_AGGREGATE_BYTES,
                            error_cls=EvidenceInventoryError) -> list[StagedMember]:
    """No-follow copy every regular file under ``src_root`` into ``dest_dir``, hashing the staged
    bytes and returning the typed ``StagedMember`` inventory.

    F9/F10 (round 20): the member-count and aggregate-byte limits are checked DURING the walk,
    BEFORE the whole tree is copied — an over-limit tree stops early. The sha256 recorded is the
    sha256 of the bytes actually written to staging, so the archive that later packages the staged
    bytes and the inventory that describes them cannot disagree.
    """
    src_root = str(src_root)
    dest_dir = str(dest_dir)
    members: list[StagedMember] = []
    stats = {"count": 0, "bytes": 0}

    def _stage(rel: str, name: str, parent_fd: int) -> None:
        stats["count"] += 1
        if stats["count"] > max_members:
            raise error_cls(f"evidence tree exceeds the member-count limit ({max_members}) "
                            f"at {rel!r} — refusing before copying the rest")
        vf = secure_fs.read_verified_file_at(parent_fd, name, expected_kind="regular",
                                             max_bytes=max_bytes, error_cls=error_cls,
                                             noun="evidence file")
        stats["bytes"] += len(vf.data)
        if stats["bytes"] > max_aggregate_bytes:
            raise error_cls(f"evidence tree exceeds the aggregate-byte limit "
                            f"({max_aggregate_bytes}) at {rel!r} — refusing before copying the rest")
        dest = os.path.join(dest_dir, rel)
        os.makedirs(os.path.dirname(dest) or dest_dir, exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(vf.data)
        mode = 0o755 if (vf.mode & 0o111) else 0o644
        members.append(StagedMember(relative_path=rel, kind="regular", mode=mode,
                                    size=len(vf.data),
                                    sha256=hashlib.sha256(vf.data).hexdigest(),
                                    source_class=source_class))

    root_fd = secure_fs.anchor_root(src_root, error_cls=error_cls, noun="evidence root",
                                    create=False)
    try:
        _walk_regular(root_fd, "", on_file=_stage, error_cls=error_cls, max_bytes=max_bytes)
    finally:
        os.close(root_fd)
    members.sort(key=lambda m: m.relative_path)
    return members


def stage_evidence_tree(src_root: str | Path, dest_dir: str | Path, *,
                        max_bytes: int = MAX_MEMBER_BYTES,
                        error_cls=EvidenceInventoryError) -> list[str]:
    """Back-compat: stage and return only the sorted relative-path list (no hashes)."""
    return [m.relative_path for m in
            stage_evidence_snapshot(src_root, dest_dir, max_bytes=max_bytes, error_cls=error_cls)]


def write_snapshot_inventory(dest_root: str | Path, members: list[StagedMember]) -> str:
    """Write the typed ``evidence_snapshot_inventory.json`` into ``dest_root`` and return its path.

    The inventory is the immutable record the ArchivePlan consumes: every Evidence ArchiveMember's
    expected hash comes from here, so a member cannot be verified from one version and packaged from
    another. The inventory file itself is a generated member bound by the directed hash chain.
    """
    path = os.path.join(str(dest_root), SNAPSHOT_INVENTORY_NAME)
    body = {"inventory_v": 1,
            "member_count": len(members),
            "members": [m.to_json() for m in members]}
    with open(path, "wb") as fh:
        fh.write((json.dumps(body, indent=2, sort_keys=True) + "\n").encode())
    return path


def list_regular_tree(root: str | Path, *, prefix: str = "",
                      max_bytes: int = MAX_MEMBER_BYTES,
                      error_cls=EvidenceInventoryError) -> list[str]:
    """Sorted relative paths of every REGULAR file under ``root``, blocking any non-regular member.

    Used to build the archive's evidence file list from a typed walk instead of ``find -type f``,
    so the list and the tree cannot disagree and a symlink cannot slip in unnamed.
    """
    root = str(root)
    found: list[str] = []

    def _record(rel: str, name: str, parent_fd: int) -> None:
        found.append(f"{prefix}/{rel}" if prefix else rel)

    root_fd = secure_fs.anchor_root(root, error_cls=error_cls, noun="evidence staging root",
                                    create=False)
    try:
        _walk_regular(root_fd, "", on_file=_record, error_cls=error_cls, max_bytes=max_bytes)
    finally:
        os.close(root_fd)
    found.sort()
    return found
