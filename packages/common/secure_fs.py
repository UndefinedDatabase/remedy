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
import errno
import fcntl
import os
import secrets
import stat
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

__all__ = [
    "SecureFsError",
    "exclusive_lock_fd",
    "release_lock_fd",
    "publish_dir_atomically",
    "remove_tree_at",
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


def require_single_component(name: str, *, error_cls: ErrorCls = SecureFsError,
                             noun: str = "path") -> None:
    """One real directory component — never a traversal, never a path.

    ``..`` is not a symlink and IS a directory, so every no-follow identity check below happily
    opens it and walks the caller straight out of the tree one level per component. Anchored
    traversal is only a containment guarantee if what it traverses are components; the check
    therefore belongs HERE, at the single opener every anchored walk goes through, rather than in
    each caller's loop where one forgotten call reopens the hole.

    ``os.sep`` is the documented exception: an absolute walk bootstraps from the real root.
    """
    if name == os.sep:
        return
    if not name or name in (os.curdir, os.pardir):
        raise error_cls(f"refusing to open {noun} component {name!r}: not a real component")
    if os.sep in name or (os.altsep and os.altsep in name) or "\0" in name:
        raise error_cls(f"refusing to open {noun} component {name!r}: not a single component")


def open_verified_dir(name: str, dir_fd: int | None = None, *,
                      error_cls: ErrorCls = SecureFsError, noun: str = "path") -> int:
    """Open ONE directory component and prove it is the thing we inspected."""
    require_single_component(name, error_cls=error_cls, noun=noun)
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


class VerifiedFile:
    """The typed, no-follow result of reading one path: what it IS, and its bytes.

    F3 (round 18): for a regular file, ``data`` is its own bytes; for a symlink, ``data`` is its
    literal target text (never the bytes it points at). ``kind`` and ``mode`` come from the fd/
    lstat that produced ``data``, not from a separate earlier check that a swap could invalidate.
    """
    __slots__ = ("kind", "data", "mode", "st_dev", "st_ino")

    def __init__(self, kind: str, data: bytes, mode: int, st_dev: int, st_ino: int) -> None:
        self.kind = kind
        self.data = data
        self.mode = mode
        self.st_dev = st_dev
        self.st_ino = st_ino


def read_verified_file_at(parent_fd: int, name: str, *, expected_kind: str,
                          max_bytes: int = 0, expected_mode: int | None = None,
                          error_cls: ErrorCls = SecureFsError,
                          noun: str = "file") -> VerifiedFile:
    """Read ONE component ``name`` relative to a HELD, anchored ``parent_fd`` — atomically typed.

    F3 (round 18): the vulnerable shape was ``lstat(path)`` then ``open(path)``/``read_bytes(path)``
    by NAME — an attacker swaps ``path`` to an external symlink in the window and the second call
    follows it, so outside bytes are hashed or archived. Here every step operates on ``name``
    RELATIVE TO the same held directory descriptor, and the regular path opens with ``O_NOFOLLOW``
    then re-``fstat``s the OPEN descriptor's ``(st_dev, st_ino)`` against the pre-open lstat: an
    ignored ``O_NOFOLLOW`` or a between-check swap changes the inode and is refused, never read.

    ``expected_kind`` is ``"regular"`` or ``"symlink"``. A path that is not the expected kind is
    refused — a regular file swapped to a symlink cannot satisfy a regular read, and vice versa.
    """
    if expected_kind not in ("regular", "symlink"):
        raise error_cls(f"unsupported expected kind {expected_kind!r} for {noun}")
    try:
        pre = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        raise error_cls(f"the {noun} {name!r} is absent") from None
    except OSError as exc:
        raise error_cls(f"the {noun} {name!r} could not be inspected: "
                        f"{type(exc).__name__}: {exc}") from exc

    if expected_kind == "symlink":
        if not stat.S_ISLNK(pre.st_mode):
            raise error_cls(f"the {noun} {name!r} was expected to be a symlink but is not")
        try:
            target = os.readlink(name, dir_fd=parent_fd)   # never follows
            post = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise error_cls(f"the symlink {noun} {name!r} could not be read safely: "
                            f"{type(exc).__name__}: {exc}") from exc
        if (not stat.S_ISLNK(post.st_mode)
                or (post.st_dev, post.st_ino) != (pre.st_dev, pre.st_ino)):
            raise error_cls(f"the symlink {noun} {name!r} changed during the read")
        return VerifiedFile("symlink", target.encode("utf-8", errors="surrogateescape"),
                            post.st_mode, post.st_dev, post.st_ino)

    # regular
    if stat.S_ISLNK(pre.st_mode):
        raise error_cls(f"refusing to read a symlinked {noun} {name!r} as a regular file")
    if not stat.S_ISREG(pre.st_mode):
        raise error_cls(f"the {noun} {name!r} is not a regular file")
    if max_bytes and pre.st_size > max_bytes:
        raise error_cls(f"the {noun} {name!r} is implausibly large ({pre.st_size} bytes)")
    try:
        fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
    except OSError as exc:
        raise error_cls(f"the {noun} {name!r} could not be opened safely (a symlink was swapped "
                        f"in?): {type(exc).__name__}: {exc}") from exc
    try:
        initial = os.fstat(fd)
        if (not stat.S_ISREG(initial.st_mode)
                or (initial.st_dev, initial.st_ino) != (pre.st_dev, pre.st_ino)):
            raise error_cls(f"the {noun} {name!r} is not the file it claimed to be (a symlink "
                            f"was followed, or it changed between the check and the open)")
        # F4 (round 19): the OPENED file's EXECUTABILITY must match what the caller planned. A plan
        # for 0755 whose source is now non-executable (or a 0644 plan whose source is executable)
        # is refused — the mode is bound to the bytes, not merely written into ZIP metadata. Only
        # the executable bit is canonical for a review member: the exact group/other bits (0664,
        # 0640, …) are working-tree noise the ZIP normalizes to 0644/0755.
        if expected_mode is not None:
            src_exec = bool(initial.st_mode & 0o111)
            want_exec = bool(expected_mode & 0o111)
            if src_exec != want_exec:
                raise error_cls(
                    f"the {noun} {name!r} is {'executable' if src_exec else 'not executable'}, "
                    f"but the plan expected {'executable' if want_exec else 'a plain file'}")
        if max_bytes and initial.st_size > max_bytes:
            raise error_cls(f"the {noun} {name!r} is implausibly large ({initial.st_size} bytes)")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            total += len(chunk)
            if max_bytes and total > max_bytes:
                raise error_cls(f"the {noun} {name!r} is implausibly large")
            chunks.append(chunk)
        # F5 (round 19): STABLE same-inode read. A file modified in place during a multi-chunk read
        # returns mixed old/new bytes with no error. Re-fstat the SAME open descriptor and require
        # its identity, type, mode, size and mtime/ctime nanoseconds unchanged across the read; any
        # drift means the bytes are a torn mixture and must be discarded, never hashed or archived.
        final = os.fstat(fd)
        if ((final.st_dev, final.st_ino) != (initial.st_dev, initial.st_ino)
                or not stat.S_ISREG(final.st_mode)
                or (final.st_mode & 0o7777) != (initial.st_mode & 0o7777)
                or final.st_size != initial.st_size
                or final.st_size != total
                or final.st_mtime_ns != initial.st_mtime_ns
                or final.st_ctime_ns != initial.st_ctime_ns):
            raise error_cls(
                f"the {noun} {name!r} changed while it was being read (a torn read); "
                f"refusing the mixed bytes")
        return VerifiedFile("regular", b"".join(chunks), final.st_mode, final.st_dev,
                            final.st_ino)
    finally:
        os.close(fd)


def open_anchored_parent(root: Path | str, rel: str, *, error_cls: ErrorCls = SecureFsError,
                         noun: str = "file") -> tuple[int, str]:
    """Traverse a relative path's DIRECTORY components under an anchored root, no-follow.

    Returns ``(parent_fd, basename)`` — the caller reads ``basename`` with
    ``read_verified_file_at`` and then closes ``parent_fd``. Every component is opened relative to
    the descriptor above it with ``O_NOFOLLOW`` identity checks, so a symlinked directory
    component cannot redirect the walk.
    """
    parts = lexical_parts(str(Path(root) / rel), root, error_cls=error_cls, noun=noun)
    if not parts:
        raise error_cls(f"{noun} names no path under the root: {rel!r}")
    fd = anchor_root(root, error_cls=error_cls, noun=noun, create=False)
    try:
        for comp in parts[:-1]:
            nxt = open_verified_dir(comp, dir_fd=fd, error_cls=error_cls, noun=noun)
            os.close(fd)
            fd = nxt
    except MissingComponent as exc:
        # A missing PARENT directory is an absent file, reported in the caller's own error type
        # rather than leaking a bare FileNotFoundError/MissingComponent past its `except`.
        os.close(fd)
        raise error_cls(f"{noun} {rel!r} is absent (missing parent {exc})") from None
    except Exception:
        os.close(fd)
        raise
    return fd, parts[-1]


def read_verified_relative(root: Path | str, rel: str, *, expected_kind: str,
                           max_bytes: int = 0, expected_mode: int | None = None,
                           error_cls: ErrorCls = SecureFsError,
                           noun: str = "file") -> VerifiedFile:
    """The whole anchored no-follow read of a repo-relative path — traverse, read, close."""
    parent_fd, base = open_anchored_parent(root, rel, error_cls=error_cls, noun=noun)
    try:
        return read_verified_file_at(parent_fd, base, expected_kind=expected_kind,
                                     max_bytes=max_bytes, expected_mode=expected_mode,
                                     error_cls=error_cls, noun=noun)
    finally:
        os.close(parent_fd)


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


def exclusive_lock_fd(name: str, dir_fd: int, *, timeout_sec: float = 30.0,
                      poll_sec: float = 0.005, file_mode: int = 0o600,
                      error_cls: ErrorCls = SecureFsError,
                      noun: str = "lock") -> int:
    """Acquire an EXCLUSIVE advisory lock on ``name`` through a held directory fd.

    The lock is `flock`-based, so the kernel releases it when the holder's file description is
    closed — including on an abrupt process death. Nothing has to be cleaned up afterwards, and
    a crashed writer can never leave a permanent claim behind.

    Returns the held fd; the caller MUST call ``release_lock_fd``. Blocks up to ``timeout_sec``
    and then raises rather than waiting forever, so a wedged holder surfaces as a bounded,
    diagnosable error instead of a hang.
    """
    require_platform(error_cls, noun)
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(name, flags, file_mode, dir_fd=dir_fd)
    except OSError as exc:
        raise error_cls(f"{noun} could not be opened: {type(exc).__name__}: {exc}") from exc
    deadline = time.monotonic() + max(0.0, timeout_sec)
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except OSError:
            if time.monotonic() >= deadline:
                os.close(fd)
                raise error_cls(
                    f"{noun} is held by another writer and did not become available within "
                    f"{timeout_sec:g}s")
            time.sleep(poll_sec)


def release_lock_fd(fd: int) -> None:
    """Release and close a lock fd. Safe to call once, from a ``finally``."""
    try:
        with contextlib.suppress(OSError):
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        with contextlib.suppress(OSError):
            os.close(fd)


def publish_dir_atomically(staging_name: str, final_name: str, dir_fd: int, *,
                           error_cls: ErrorCls = SecureFsError,
                           noun: str = "directory") -> bool:
    """Publish a FULLY-BUILT staging directory under ``final_name`` through a held fd.

    ``rename`` of a directory onto a non-empty directory fails on POSIX, so an existing
    published directory is never silently replaced and ``False`` is returned — the caller owns
    the conflict, exactly as ``write_file_atomically(create_only=True)`` does for files. This is
    what makes an episode publication all-or-nothing: everything is built and verified under an
    unpredictable private name first, and the single rename is the only moment the canonical
    name exists at all.
    """
    try:
        os.rename(staging_name, final_name, src_dir_fd=dir_fd, dst_dir_fd=dir_fd)
        return True
    except (FileExistsError, NotADirectoryError):
        return False
    except OSError as exc:
        # ENOTEMPTY (and on some systems EEXIST) — the destination is a published directory.
        if exc.errno in (errno.ENOTEMPTY, errno.EEXIST):
            return False
        raise error_cls(
            f"{noun} could not be published: {type(exc).__name__}: {exc}") from exc


def remove_tree_at(name: str, dir_fd: int, *, error_cls: ErrorCls = SecureFsError,
                   noun: str = "directory") -> None:
    """Remove a directory subtree through held fds, never following a symlink.

    Used ONLY to clean up a private staging directory this process created under an
    unpredictable name: it never touches a published name, so a losing writer can never delete a
    winner's file.
    """
    try:
        sub_fd = os.open(name, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
                         | getattr(os, "O_NOFOLLOW", 0), dir_fd=dir_fd)
    except FileNotFoundError:
        return
    except OSError as exc:
        raise error_cls(f"{noun} could not be cleaned: {exc}") from exc
    try:
        try:
            entries = os.listdir(sub_fd)
        except OSError as exc:
            raise error_cls(f"{noun} could not be cleaned: {exc}") from exc
        for entry in entries:
            try:
                st = os.stat(entry, dir_fd=sub_fd, follow_symlinks=False)
            except FileNotFoundError:
                continue
            if stat.S_ISDIR(st.st_mode):
                remove_tree_at(entry, sub_fd, error_cls=error_cls, noun=noun)
            else:
                with contextlib.suppress(OSError):
                    os.unlink(entry, dir_fd=sub_fd)
    finally:
        os.close(sub_fd)
    with contextlib.suppress(OSError):
        os.rmdir(name, dir_fd=dir_fd)


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
    """Canonical JSON bytes — STANDARD JSON only.

    ``allow_nan=False`` refuses ``NaN`` / ``Infinity`` / ``-Infinity``: Python emits those as
    bare words that are NOT valid JSON, so any other reader would reject the record we just
    published (and a non-finite float has no place in an input identity or a hash).
    """
    import json

    return (json.dumps(payload, indent=indent, sort_keys=sort_keys,
                       allow_nan=False) + "\n").encode("utf-8")
