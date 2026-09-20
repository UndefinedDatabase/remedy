"""The data root's disk footprint, per top-level child and per class (F276 T001).

``footprint(root)`` walks the tree ONCE with ``os.scandir``, never follows a
symlink (a link counts as one file of its own ``lstat`` size), shells out to
nothing and writes nothing. A missing root, or a file that vanishes between the
listing and its ``lstat``, is not an error: it is simply not counted. Each child is
classed through ``data_paths.classify_data_child``, so the registry there is the
only place a class is decided.

Public API::

    footprint(root) -> DataFootprint
    child_usage(path) -> (bytes, files)
    export_footprint_json(fp) -> dict
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import classify_data_child

#: The three class labels a child can carry, in report order.
FOOTPRINT_CLASSES: tuple[str, ...] = ("ephemeral", "durable", "unclassified")


@dataclass(frozen=True)
class ChildFootprint:
    """One top-level child of the data root: its class, bytes and file count."""

    name: str
    data_class: str
    bytes: int
    files: int


@dataclass(frozen=True)
class DataFootprint:
    """The whole data root: every child, sorted by name, and the totals."""

    root: str
    exists: bool
    children: tuple[ChildFootprint, ...]

    def class_totals(self) -> dict[str, tuple[int, int]]:
        """``{class: (bytes, files)}`` for every class in FOOTPRINT_CLASSES."""
        totals = {c: (0, 0) for c in FOOTPRINT_CLASSES}
        for child in self.children:
            b, f = totals[child.data_class]
            totals[child.data_class] = (b + child.bytes, f + child.files)
        return totals

    @property
    def total_bytes(self) -> int:
        return sum(c.bytes for c in self.children)

    @property
    def total_files(self) -> int:
        return sum(c.files for c in self.children)


def _lstat_size(entry: os.DirEntry[str]) -> int | None:
    try:
        return entry.stat(follow_symlinks=False).st_size
    except OSError:
        return None


def _subtree_usage(top: str) -> tuple[int, int]:
    """(bytes, files) under one directory; a directory itself counts no bytes."""
    total_bytes = total_files = 0
    pending = [top]
    while pending:
        current = pending.pop()
        try:
            with os.scandir(current) as it:
                entries = list(it)
        except OSError:
            continue
        for entry in entries:
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError:
                continue
            if is_dir:
                pending.append(entry.path)
                continue
            size = _lstat_size(entry)
            if size is not None:
                total_bytes += size
                total_files += 1
    return total_bytes, total_files


def child_usage(path: Path | str) -> tuple[int, int]:
    """(bytes, files) of ONE data-root child: a directory's whole subtree, or itself.

    A symlink is never followed — it counts as one file of its own ``lstat`` size —
    and a path that cannot be stat'ed counts as nothing. ``data_reclaim`` measures a
    reclaim candidate with this, so a candidate's bytes and its ``data usage`` bytes
    are one number produced by one function.
    """
    p = os.fspath(path)
    try:
        st = os.lstat(p)
    except OSError:
        return (0, 0)
    if os.path.isdir(p) and not os.path.islink(p):
        return _subtree_usage(p)
    return (st.st_size, 1)


def footprint(root: Path | str) -> DataFootprint:
    """Measure the data root, read-only, in one walk."""
    root_str = os.fspath(root)
    try:
        with os.scandir(root_str) as it:
            top = sorted(it, key=lambda e: e.name)
    except OSError:
        return DataFootprint(root=root_str, exists=False, children=())
    children = []
    for entry in top:
        kind = classify_data_child(entry.name) or "unclassified"
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError:
            continue
        if is_dir:
            size, files = _subtree_usage(entry.path)
        else:
            lsize = _lstat_size(entry)
            if lsize is None:
                continue
            size, files = lsize, 1
        children.append(ChildFootprint(entry.name, kind, size, files))
    return DataFootprint(root=root_str, exists=True, children=tuple(children))


def export_footprint_json(fp: DataFootprint) -> dict[str, Any]:
    """The stable machine shape `remedy data usage --json` prints."""
    totals = fp.class_totals()
    return {
        "version": 1,
        "root": fp.root,
        "exists": fp.exists,
        "classes": {c: {"bytes": b, "files": f} for c, (b, f) in totals.items()},
        "children": [
            {"name": c.name, "class": c.data_class, "bytes": c.bytes, "files": c.files}
            for c in fp.children
        ],
        "total": {"bytes": fp.total_bytes, "files": fp.total_files},
    }
