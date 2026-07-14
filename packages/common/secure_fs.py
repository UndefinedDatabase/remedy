"""Directory-FD-anchored filesystem primitives — the ONE implementation.

F010 learned these rules the hard way, on a review host where `O_NOFOLLOW` was accepted and
quietly ignored: a flag the kernel takes and disregards is not a guarantee, and a path
validated by name and then reopened by name is a check-then-use race. F011 then reinvented
the same problem in a weaker form. So the rules live here once, and both features call them.

The guarantee, for every directory component and every file we touch:

1. inspect the entry with ``os.stat(..., dir_fd=…, follow_symlinks=False)`` — never the
   thing it points at. A symlink is refused HERE, in our code;
2. require the type we expect (directory, or regular file);
3. open it relative to a descriptor we already hold, with ``O_NOFOLLOW`` as defence in
   depth — never as the argument;
4. ``os.fstat`` what we actually opened;
5. require ``(st_dev, st_ino)`` to be the SAME inode we inspected.

Step 5 is the guarantee. It catches an ignored `O_NOFOLLOW` (the opened inode is the
symlink's target, not the entry we looked at) and it catches an entry swapped between the
check and the open. Without the primitives these rules are built from, we **fail closed**:
there is no best-effort mode.

Callers pass their own exception class and a noun, so an F010 failure still sounds like a
post-mortem problem and an F011 failure still sounds like a stop-control problem.
"""
from __future__ import annotations

import contextlib
import os
import secrets
import stat
from pathlib import Path
from typing import Any, Callable

__all__ = [
    "SecureFsError",
    "MissingComponent",
    "DIR_FD_SUPPORTED",
    "require_platform",
    "lexical_parts",
    "open_verified_dir",
    "anchor_root",
    "anchor_destination",
    "writable_by_mode_fd",
    "require_writable_dir",
    "read_verified_file",
    "write_file_atomically",
    "unlink_at",
    "list_dir_names",
]


class SecureFsError(RuntimeError):
    """Containment could not be guaranteed. Nothing was written."""


class MissingComponent(Exception):
    """The component is not there (yet). The caller decides whether to create it."""


#: Not "does the CONSTANT exist" — that was the false positive. These are the primitives the
#: guarantee is actually made of.
DIR_FD_SUPPORTED = (
    os.open in getattr(os, "supports_dir_fd", set())
    and os.mkdir in getattr(os, "supports_dir_fd", set())
    and os.link in getattr(os, "supports_dir_fd", set())
    and os.unlink in getattr(os, "supports_dir_fd", set())
    and os.stat in getattr(os, "supports_dir_fd", set())
    and os.stat in getattr(os, "supports_follow_symlinks", set())
)

OPEN_DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)

ErrorCls = Callable[[str], BaseException]


def require_platform(error_cls: ErrorCls = SecureFsError, noun: str = "file") -> None:
    """No semantic guarantee, no write."""
    if not DIR_FD_SUPPORTED:
        raise error_cls(
            f"this platform cannot guarantee {noun} containment (no directory-fd "
            f"stat/open/mkdir/link/unlink with follow_symlinks=False); refusing to write")


def lexical_parts(directory: Path | str, root: Path | str, *,
                  error_cls: ErrorCls = SecureFsError, noun: str = "path") -> list[str]:
    """The destination's components below the root — LEXICALLY.

    Lexically, because ``resolve()`` answers the wrong question: asked "did the caller route
    me through a symlink?", it cheerfully reports where the symlink POINTS.
    """
    requested = Path(os.path.normpath(str(directory)))
    root_norm = Path(os.path.normpath(str(root)))
    try:
        rel = requested.relative_to(root_norm)
    except ValueError:
        raise error_cls(
            f"{noun} directory escapes its trusted root: {requested} !< {root_norm}"
        ) from None
    parts = [p for p in rel.parts if p != "."]
    if any(p == ".." for p in parts):
        raise error_cls(f"{noun} directory traverses upwards: {directory}")
    return parts


def open_verified_dir(name: str, dir_fd: int | None = None, *,
                      error_cls: ErrorCls = SecureFsError, noun: str = "path") -> int:
    """Open ONE directory component and prove it is the thing we inspected."""
    try:
        pre = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError as exc:
        raise MissingComponent(name) from exc
    except OSError as exc:
        raise error_cls(
            f"{noun} path {name!r} could not be inspected: "
            f"{type(exc).__name__}: {exc}") from exc

    if stat.S_ISLNK(pre.st_mode):
        raise error_cls(f"refusing to write through a symlinked path component: {name}")
    if not stat.S_ISDIR(pre.st_mode):
        raise error_cls(f"{noun} path is not a directory: {name}")

    try:
        fd = os.open(name, OPEN_DIR_FLAGS, dir_fd=dir_fd)
    except FileNotFoundError as exc:
        raise MissingComponent(name) from exc
    except OSError as exc:
        raise error_cls(
            f"refusing to open {noun} path {name!r}: {type(exc).__name__}: {exc}") from exc

    try:
        post = os.fstat(fd)
    except OSError as exc:
        os.close(fd)
        raise error_cls(
            f"{noun} path {name!r} could not be verified after opening: "
            f"{type(exc).__name__}: {exc}") from exc

    if (not stat.S_ISDIR(post.st_mode)
            or (post.st_dev, post.st_ino) != (pre.st_dev, pre.st_ino)):
        os.close(fd)
        raise error_cls(
            f"{noun} path {name!r} is not the directory it claimed to be (a symlink was "
            f"followed, or the entry changed between the check and the open); refusing "
            f"to write")
    return fd


def anchor_root(root: Path | str, *, error_cls: ErrorCls = SecureFsError,
                noun: str = "path", create: bool = False,
                dir_mode: int = 0o700) -> int:
    """Open the trusted root — verifying EVERY component of the way there.

    The first version of this function verified the root's final component and then opened
    its parent by raw path name (``os.open(parent, …)``). That was the same check-then-use
    hole one level up: with ``real/link -> outside``, a trusted root of ``real/link/control``
    was "verified" — and the whole control area landed in ``outside``. Because F010's
    post-mortem writer and F011's stop control share this helper, the same symlink redirected
    both.

    So there is no trusted parent any more. We start at the filesystem root, which nothing
    can redirect, and walk down: each component is stat'ed without following symlinks,
    required to be a directory, opened relative to the descriptor we already hold, `fstat`'d,
    and required to be the same ``(st_dev, st_ino)`` we inspected. The parent fd is closed
    only once the child fd is held. A relative root is made absolute against the process's
    CWD first — the same semantics the callers already assumed — and then walked identically.

    With ``create=True`` a MISSING component is created through the descriptor we hold (mode
    ``dir_mode``) and immediately verified the same way. Nothing is ever created by name, so a
    validation that ultimately fails leaves nothing behind outside the verified chain.
    """
    require_platform(error_cls, noun)

    root_abs = Path(os.path.normpath(os.path.abspath(str(root))))
    parts = [p for p in root_abs.parts if p not in ("", os.sep)]

    try:
        current = open_verified_dir(os.sep, error_cls=error_cls, noun=noun)
    except MissingComponent as exc:                 # a machine without "/" is not our problem
        raise error_cls(f"the filesystem root is not usable for {noun} anchoring") from exc

    try:
        for part in parts:
            try:
                child = open_verified_dir(part, dir_fd=current, error_cls=error_cls,
                                          noun=noun)
            except MissingComponent:
                if not create:
                    raise error_cls(f"the {noun} root does not exist: {root_abs}") from None
                # Mode bits, not `os.access` (which lies to root).
                require_writable_dir(current, error_cls=error_cls, noun=noun, label=part)
                try:
                    os.mkdir(part, dir_mode, dir_fd=current)
                except FileExistsError:
                    pass                            # a concurrent creator; verify below
                except OSError as exc:
                    raise error_cls(
                        f"the {noun} root could not be created: "
                        f"{type(exc).__name__}: {exc}") from exc
                try:
                    child = open_verified_dir(part, dir_fd=current, error_cls=error_cls,
                                              noun=noun)
                except MissingComponent as exc:
                    raise error_cls(
                        f"the {noun} root vanished after creation: {part}") from exc
            os.close(current)
            current = child
    except BaseException:
        os.close(current)
        raise
    return current


def anchor_destination(directory: Path | str, root: Path | str, *,
                       error_cls: ErrorCls = SecureFsError, noun: str = "path",
                       create: bool = True, dir_mode: int = 0o700) -> int:
    """Walk from the trusted root to the destination on VERIFIED directory handles.

    Missing components are created THROUGH the held parent fd (with ``dir_mode`` — private,
    never the process umask's idea of 0755) and then verified the same way, so a symlink
    slipped in between the ``mkdir`` and the open is caught by the identity comparison
    rather than followed. The returned fd IS the destination; everything after happens
    through it. The caller closes it.
    """
    require_platform(error_cls, noun)
    root_norm = Path(os.path.normpath(str(root)))
    parts = lexical_parts(directory, root_norm, error_cls=error_cls, noun=noun)

    current = anchor_root(root_norm, error_cls=error_cls, noun=noun)
    try:
        for part in parts:
            try:
                child = open_verified_dir(part, dir_fd=current, error_cls=error_cls,
                                          noun=noun)
            except MissingComponent:
                if not create:
                    raise
                # Mode bits, not `os.access`: the review host runs as root, and root is told
                # that a 0o500 directory is writable. It is not, and we will not pretend it
                # is just because the kernel would let us through.
                require_writable_dir(current, error_cls=error_cls, noun=noun, label=part)
                try:
                    os.mkdir(part, dir_mode, dir_fd=current)
                except FileExistsError:
                    pass                        # someone else won the race; verify below
                except OSError as exc:
                    raise error_cls(
                        f"{noun} directory could not be created: "
                        f"{type(exc).__name__}: {exc}") from exc
                try:
                    child = open_verified_dir(part, dir_fd=current, error_cls=error_cls,
                                              noun=noun)
                except MissingComponent as exc:
                    raise error_cls(
                        f"{noun} directory vanished after creation: {part}") from exc
            os.close(current)
            current = child
    except BaseException:
        os.close(current)
        raise
    return current


def writable_by_mode_fd(dir_fd: int) -> bool:
    """Does the directory DECLARE itself writable to its owner?

    ``os.access`` lies to root — it calls a 0o500 directory writable, and the review host
    runs as root. The declared mode bits do not lie, and they are read from the fd we
    already hold rather than from a name that may have been swapped since.
    """
    try:
        return bool(os.fstat(dir_fd).st_mode & stat.S_IWUSR)
    except OSError:
        return False


def require_writable_dir(dir_fd: int, *, error_cls: ErrorCls = SecureFsError,
                         noun: str = "path", label: str = "") -> None:
    if not writable_by_mode_fd(dir_fd):
        try:
            mode = oct(os.fstat(dir_fd).st_mode & 0o777)
        except OSError:
            mode = "unknown"
        raise error_cls(f"{noun} directory is read-only ({mode}){f': {label}' if label else ''}")


def read_verified_file(name: str, dir_fd: int, *, max_bytes: int = 0,
                       error_cls: ErrorCls = SecureFsError,
                       noun: str = "file") -> bytes | None:
    """Read a file THROUGH a held directory fd — proving what we opened. None if absent."""
    try:
        pre = os.stat(name, dir_fd=dir_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise error_cls(
            f"the existing {noun} could not be inspected: "
            f"{type(exc).__name__}: {exc}") from exc

    if stat.S_ISLNK(pre.st_mode):
        raise error_cls(
            f"refusing to read a symlinked {noun}: it must live where it claims to, not "
            f"point out of it")
    if not stat.S_ISREG(pre.st_mode):
        raise error_cls(f"the existing {noun} is not a regular file")
    if max_bytes and pre.st_size > max_bytes:
        raise error_cls(f"the existing {noun} is implausibly large ({pre.st_size} bytes)")

    try:
        fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=dir_fd)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise error_cls(
            f"the existing {noun} could not be read safely: "
            f"{type(exc).__name__}: {exc}") from exc
    try:
        post = os.fstat(fd)
        if (not stat.S_ISREG(post.st_mode)
                or (post.st_dev, post.st_ino) != (pre.st_dev, pre.st_ino)):
            raise error_cls(
                f"the existing {noun} is not the file it claimed to be (a symlink was "
                f"followed, or it changed between the check and the open)")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            if max_bytes and total > max_bytes:
                raise error_cls(f"the existing {noun} is implausibly large")
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        os.close(fd)


def write_file_atomically(dir_fd: int, name: str, data: bytes, *, create_only: bool,
                          file_mode: int = 0o600, error_cls: ErrorCls = SecureFsError,
                          noun: str = "file") -> bool:
    """Write ``name`` through a held directory fd. Private, atomic, no temp file left.

    ``create_only`` publishes with ``os.link`` — an existing file is NOT overwritten and
    ``False`` is returned, so the caller can compare and decide. Otherwise ``os.replace``
    publishes, which is atomic but does overwrite. Both go through an unpredictable
    ``O_EXCL`` temp file created with the FINAL mode (never briefly world-readable), a
    full-byte write loop, and an ``fsync`` before publication.
    """
    require_writable_dir(dir_fd, error_cls=error_cls, noun=noun, label=name)

    tmp_name = f".{name}.{os.getpid()}.{secrets.token_hex(8)}.tmp"
    tmp_created = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        try:
            fd = os.open(tmp_name, flags, file_mode, dir_fd=dir_fd)
        except OSError as exc:
            raise error_cls(
                f"{noun} could not be written: {type(exc).__name__}: {exc}") from exc
        tmp_created = True
        try:
            written = 0
            while written < len(data):
                try:
                    chunk = os.write(fd, data[written:])
                except OSError as exc:
                    raise error_cls(
                        f"{noun} could not be written: {type(exc).__name__}: {exc}"
                    ) from exc
                if chunk <= 0:
                    raise error_cls(f"{noun} write made no progress at byte {written}")
                written += chunk
            os.fsync(fd)
        finally:
            os.close(fd)

        if create_only:
            try:
                os.link(tmp_name, name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
            except FileExistsError:
                return False                    # the caller owns the conflict, not us
            except OSError as exc:
                raise error_cls(
                    f"{noun} could not be published: {type(exc).__name__}: {exc}") from exc
        else:
            try:
                os.replace(tmp_name, name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
            except OSError as exc:
                raise error_cls(
                    f"{noun} could not be published: {type(exc).__name__}: {exc}") from exc
            tmp_created = False                 # replace consumed it
        return True
    finally:
        if tmp_created:
            with contextlib.suppress(OSError):
                os.unlink(tmp_name, dir_fd=dir_fd)


def unlink_at(name: str, dir_fd: int, *, error_cls: ErrorCls = SecureFsError,
              noun: str = "file") -> bool:
    """Remove a name through a held directory fd. False when it was not there."""
    try:
        os.unlink(name, dir_fd=dir_fd)
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        raise error_cls(
            f"{noun} could not be removed: {type(exc).__name__}: {exc}") from exc


def list_dir_names(dir_fd: int, *, error_cls: ErrorCls = SecureFsError,
                   noun: str = "directory") -> list[str]:
    """List entries through a held fd — no second path resolution, no glob."""
    try:
        return sorted(os.listdir(dir_fd))
    except OSError as exc:
        raise error_cls(
            f"{noun} could not be listed: {type(exc).__name__}: {exc}") from exc


def json_bytes(payload: Any, *, indent: int = 2, sort_keys: bool = True) -> bytes:
    import json

    return (json.dumps(payload, indent=indent, sort_keys=sort_keys) + "\n").encode("utf-8")
