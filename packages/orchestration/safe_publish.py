"""Round 32 F4 — the ONE no-clobber publication boundary, shared by the direct Python coordinator and
the shell wrapper. An output path may be written ONLY when it is a safe, non-colliding location:

* never a TRACKED project file (git would lose it);
* never a symlink, directory, FIFO, socket or device;
* never an already-existing regular file (a timestamped package name is unique per invocation, so any
  pre-existing file at the path is a foreign collision unless explicit current-run ownership is proven).

The check itself is the security boundary; an overwrite-capable ``mv``/``open`` is never the boundary.
On refusal every pre-existing byte is preserved exactly (nothing is opened, truncated or moved).
"""
from __future__ import annotations

import os
import stat
import subprocess


class PublishCollisionError(Exception):
    """A packaging output path collides with a tracked/unsafe/foreign filesystem entry."""


def _is_tracked(path: str, repo_root: str) -> bool:
    try:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repo_root))
    except ValueError:
        return False
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", "--", rel],
                           cwd=repo_root, capture_output=True, timeout=10)
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # If git cannot be consulted we CANNOT prove the path is untracked — refuse (fail closed).
        raise PublishCollisionError(
            f"cannot determine tracked status of {path!r}; refusing to publish")


def assert_publishable(path: str, repo_root: str, *, owned_paths: frozenset = frozenset()) -> None:
    """Raise ``PublishCollisionError`` unless ``path`` is a safe output location. ``owned_paths`` is the
    set of repo-root-relative paths THIS invocation legitimately produces (its temp ZIP → final ZIP
    rename), which may already exist as this run's own regular file."""
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        st = None
    except OSError as exc:
        raise PublishCollisionError(f"cannot stat output path {path!r}: {exc}")

    if _is_tracked(path, repo_root):
        raise PublishCollisionError(
            f"refusing to write output over TRACKED project file {path!r}")

    if st is not None:
        mode = st.st_mode
        if stat.S_ISLNK(mode):
            raise PublishCollisionError(f"refusing to write output over a symlink: {path!r}")
        if stat.S_ISDIR(mode):
            raise PublishCollisionError(f"refusing to write output over a directory: {path!r}")
        if not stat.S_ISREG(mode):
            raise PublishCollisionError(
                f"refusing to write output over a non-regular file (FIFO/socket/device): {path!r}")
        # A pre-existing regular file is a foreign collision unless this run owns the path.
        rel = os.path.basename(path)
        abs_rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repo_root)) \
            if repo_root else path
        if rel not in owned_paths and abs_rel not in owned_paths and path not in owned_paths:
            raise PublishCollisionError(
                f"refusing to overwrite a pre-existing foreign output file: {path!r}")


def atomic_reserve(path: str) -> int:
    """Exclusively create ``path`` (``O_CREAT|O_EXCL``) and return the fd. Raises
    ``PublishCollisionError`` if it already exists — a no-clobber reservation two concurrent
    invocations cannot both win."""
    try:
        return os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        raise PublishCollisionError(f"output path already reserved/created: {path!r}")
