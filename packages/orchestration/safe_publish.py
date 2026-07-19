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


def git_tracked_status(path: str, repo_root: str) -> tuple[str, str]:
    """Round 33 F2: interpret ``git ls-files --error-unmatch`` by EXACT exit code, never by
    ``returncode != 0``. Returns ``(status, diagnostic)`` where status is one of ``TRACKED`` (exit 0),
    ``UNTRACKED`` (exit 1 — the exact "path is not tracked" result), ``GIT_FAILED`` (any other exit,
    e.g. 128 repo/index/permission error), ``GIT_TIMED_OUT`` or ``GIT_UNAVAILABLE``. Only ``UNTRACKED``
    lets publication proceed; every other state (including a Git-internal failure) blocks."""
    try:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(repo_root))
    except ValueError:
        return "GIT_FAILED", "output path is not within the repository root"
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", "-z", "--", rel],
                           cwd=repo_root, capture_output=True, text=True, timeout=10)
    except FileNotFoundError:
        return "GIT_UNAVAILABLE", "git executable not found"
    except subprocess.TimeoutExpired:
        return "GIT_TIMED_OUT", "git ls-files timed out"
    except Exception as exc:                               # pragma: no cover - defensive
        return "GIT_FAILED", f"{type(exc).__name__}: {str(exc)[:100]}"
    if r.returncode == 0:
        return "TRACKED", ""
    if r.returncode == 1:
        return "UNTRACKED", ""
    return "GIT_FAILED", f"git ls-files exit {r.returncode}: {(r.stderr or '')[:100]}"


def _assert_untracked(path: str, repo_root: str) -> None:
    status, diag = git_tracked_status(path, repo_root)
    if status == "TRACKED":
        raise PublishCollisionError(
            f"refusing to write output over TRACKED project file {path!r}")
    if status != "UNTRACKED":
        # A repository/index/permission/invocation/Git-internal failure is NEVER interpreted as
        # untracked — publication fails closed with a bounded diagnostic.
        raise PublishCollisionError(
            f"cannot determine tracked status of {path!r} ({status}: {diag}); refusing to publish")


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

    _assert_untracked(path, repo_root)

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


def publish_atomically(source_path: str, final_path: str, repo_root: str,
                       *, cleanup_source: bool = True) -> None:
    """Round 33 F1: publish an ALREADY-BUILT-AND-VERIFIED private ZIP at ``source_path`` to the public
    ``final_path`` through ONE atomic, no-replace operation — ``os.link`` fails with ``FileExistsError``
    if ``final_path`` exists, so exactly one concurrent invocation wins and no existing destination is
    ever truncated or unlinked. ``source_path`` must be on the SAME filesystem as ``final_path``. On a
    losing race (or a tracked/unsafe destination) a ``PublishCollisionError`` is raised; the caller's
    private ``source_path`` is removed (unless ``cleanup_source`` is false) so no partial reservation
    leaks. The winning ``final_path`` is the complete, byte-identical ZIP."""
    final = os.path.abspath(final_path)
    parent = os.path.dirname(final) or "."
    try:
        if not os.path.isdir(parent):
            raise PublishCollisionError(f"output parent directory does not exist: {parent!r}")
        # Advisory refusal of tracked / symlink / directory / FIFO / device / foreign destinations
        # BEFORE the atomic link; the link itself is the race-proof no-clobber boundary.
        assert_publishable(final, repo_root, owned_paths=frozenset({final, final_path}))
        try:
            os.link(source_path, final)                    # ATOMIC no-replace publication
        except FileExistsError:
            raise PublishCollisionError(
                f"another invocation already published {final_path!r}; this one loses the race")
        except OSError as exc:
            raise PublishCollisionError(f"could not publish {final_path!r}: {exc}")
    finally:
        if cleanup_source:
            try:
                os.unlink(source_path)                     # remove the now-linked private temp
            except OSError:
                pass
