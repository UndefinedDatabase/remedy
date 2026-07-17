"""F8 (round 19) — the typed, no-follow Evidence inventory.

Evidence used to be discovered with ``find -type f`` and staged with ``cp``. Both are unsafe:

* ``find -type f`` SILENTLY SKIPS a symlink — a symlink evidence artifact is simply absent from
  the package with nothing said about it, the same parallel-truth failure the repository side had.
* ``cp`` FOLLOWS a symlink — a symlink named ``token.json`` that points at ``/etc/passwd`` (or at a
  provider-secret file outside the evidence tree) is copied into the package as a regular file
  carrying OUTSIDE bytes.

The evidence tree is now walked with anchored, ``O_NOFOLLOW`` reads. A symlink, FIFO, socket, or
device anywhere in the tree is BLOCKED (the build fails closed, it is never skipped or followed),
a directory component that is itself a symlink cannot redirect the walk, and every regular member
is staged from the EXACT verified bytes — the same bytes the archive later packages and re-hashes.
"""
from __future__ import annotations

import os
import stat
from pathlib import Path

from packages.common import secure_fs
from packages.orchestration.archive_plan import MAX_MEMBER_BYTES

# Evidence never legitimately carries compiled artifacts; keep the historical exclusion.
_SKIP_SUFFIXES = (".pyc", ".pyo")


class EvidenceInventoryError(RuntimeError):
    """An evidence tree that cannot be safely inventoried (a symlink/FIFO member, an oversized
    file, an unreadable component). The build fails closed rather than skip or follow it."""


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


def stage_evidence_tree(src_root: str | Path, dest_dir: str | Path, *,
                        max_bytes: int = MAX_MEMBER_BYTES,
                        error_cls=EvidenceInventoryError) -> list[str]:
    """No-follow copy every regular file under ``src_root`` into ``dest_dir``, preserving the tree.

    Returns the sorted list of relative paths staged. Symlinks/FIFOs/devices BLOCK; a symlinked
    directory component BLOCKS; an oversized member BLOCKS. The staged bytes are exactly the
    verified no-follow bytes, so the archive that later reads ``dest_dir`` packages the same bytes.
    """
    src_root = str(src_root)
    dest_dir = str(dest_dir)
    staged: list[str] = []

    def _stage(rel: str, name: str, parent_fd: int) -> None:
        vf = secure_fs.read_verified_file_at(parent_fd, name, expected_kind="regular",
                                             max_bytes=max_bytes, error_cls=error_cls,
                                             noun="evidence file")
        dest = os.path.join(dest_dir, rel)
        os.makedirs(os.path.dirname(dest) or dest_dir, exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(vf.data)
        staged.append(rel)

    root_fd = secure_fs.anchor_root(src_root, error_cls=error_cls, noun="evidence root",
                                    create=False)
    try:
        _walk_regular(root_fd, "", on_file=_stage, error_cls=error_cls, max_bytes=max_bytes)
    finally:
        os.close(root_fd)
    staged.sort()
    return staged


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
