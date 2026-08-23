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

import ctypes
import ctypes.util
import hashlib
import os
import stat
import subprocess


class PublishCollisionError(Exception):
    """A packaging output path collides with a tracked/unsafe/foreign filesystem entry."""


class PublishSourceError(Exception):
    """The private source to be published is not the exact verified regular file/inode/bytes."""


# Round 38 F6: typed capability levels for anonymous-inode publication.
CAPABILITY_SUPPORTED = "SUPPORTED"
CAPABILITY_UNSUPPORTED_OS = "UNSUPPORTED_OS"
CAPABILITY_UNSUPPORTED_FILESYSTEM = "UNSUPPORTED_FILESYSTEM"
CAPABILITY_LINKAT_UNAVAILABLE = "LINKAT_UNAVAILABLE"
CAPABILITY_PERMISSION_DENIED = "PERMISSION_DENIED"


# ------------------------------------------------------------------------------- libc linkat binding
_AT_FDCWD = -100
_AT_EMPTY_PATH = 0x1000

_libc = None
_linkat = None


def _get_linkat():
    global _libc, _linkat
    if _linkat is not None:
        return _linkat
    libname = ctypes.util.find_library("c")
    if not libname:
        return None
    try:
        _libc = ctypes.CDLL(libname, use_errno=True)
        fn = _libc.linkat
        fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        fn.restype = ctypes.c_int
        _linkat = fn
        return fn
    except (OSError, AttributeError):
        return None


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_fd(fd: int) -> str:
    """Hash through an already-open file descriptor (seeked to 0). Race-proof: the FD is pinned to
    the inode, so a pathname swap after opening cannot change the bytes being hashed."""
    os.lseek(fd, 0, os.SEEK_SET)
    h = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1 << 20)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()


def _copy_to_fd(src_path: str, dst_fd: int) -> None:
    """Copy bytes from a named path into an open FD using O_NOFOLLOW reads."""
    try:
        src_fd = os.open(src_path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise PublishSourceError(
            f"private source {src_path!r} is not accessible (O_NOFOLLOW): {exc}") from None
    try:
        while True:
            chunk = os.read(src_fd, 1 << 20)
            if not chunk:
                break
            os.write(dst_fd, chunk)
    finally:
        os.close(src_fd)


def _linkat_anonymous(anon_fd: int, final_path: str) -> None:
    """Publish an anonymous inode to ``final_path`` via ``linkat(fd, "", AT_FDCWD, path,
    AT_EMPTY_PATH)``. No-replace: fails with ``FileExistsError`` when the target exists."""
    fn = _get_linkat()
    if fn is None:
        raise PublishSourceError(
            "linkat is unavailable on this platform; cannot publish from an anonymous inode")
    ret = fn(anon_fd, b"", _AT_FDCWD, os.fsencode(final_path), _AT_EMPTY_PATH)
    if ret != 0:
        err = ctypes.get_errno()
        if err == 17:  # EEXIST
            raise FileExistsError(f"target already exists: {final_path}")
        raise OSError(err, os.strerror(err), final_path)


def verify_source_identity(source_path: str, final_parent: str,
                           *, expected_sha256: str | None) -> int:
    """Round 35 F1: FD-retained, inode-bound source verification. Opens the private source with
    ``O_RDONLY|O_NOFOLLOW`` (so a symlink at the pathname is never followed), ``fstat``s the FD to
    confirm it is a regular file, hashes the bytes THROUGH the FD (immune to post-open pathname
    swaps), and returns the retained FD. The caller uses the FD's inode identity to verify the
    published link points to the same inode. The ``st_dev`` precheck is removed — OverlayFS reports
    different ``st_dev`` for a file and its parent even when they share a mount; a true cross-device
    situation is caught by ``os.link`` raising ``OSError(EXDEV)`` at publication time. Raises
    ``PublishSourceError`` on any mismatch; never closes the FD on success (caller must close)."""
    if expected_sha256 is None:
        raise PublishSourceError(
            "no verified source SHA-256 was bound; refusing to publish an unverified source")
    try:
        fd = os.open(source_path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise PublishSourceError(
            f"private source {source_path!r} is not accessible (O_NOFOLLOW): {exc}") from None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise PublishSourceError(
                f"private source {source_path!r} is not a regular file; refusing to publish")
        actual = _sha256_fd(fd)
        if actual != expected_sha256:
            raise PublishSourceError(
                f"private source {source_path!r} bytes changed after verification "
                f"(sha256 {actual[:12]} != verified {expected_sha256[:12]})")
    except BaseException:
        os.close(fd)
        raise
    return fd


def verify_published_identity(source_fd: int, final_path: str,
                              expected_sha256: str) -> None:
    """Round 37 F1: after anonymous-FD publication, verify the published file is the SAME inode AND
    SAME BYTES as the anonymous source. Opens the final path with O_NOFOLLOW to avoid following a
    symlink replacement."""
    src_st = os.fstat(source_fd)
    try:
        final_fd = os.open(final_path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise PublishSourceError(
            f"cannot open published path {final_path!r} for verification: {exc}") from None
    try:
        dst_st = os.fstat(final_fd)
        if (src_st.st_dev, src_st.st_ino) != (dst_st.st_dev, dst_st.st_ino):
            raise PublishSourceError(
                f"published inode ({dst_st.st_dev}:{dst_st.st_ino}) differs from anonymous source "
                f"({src_st.st_dev}:{src_st.st_ino}); the published package is not the verified bytes")
        final_hash = _sha256_fd(final_fd)
        if final_hash != expected_sha256:
            raise PublishSourceError(
                f"published bytes do not match expected hash "
                f"(sha256 {final_hash[:12]} != verified {expected_sha256[:12]})")
        source_rehash = _sha256_fd(source_fd)
        if source_rehash != expected_sha256:
            raise PublishSourceError(
                f"anonymous source bytes changed after publication (in-place mutation detected: "
                f"sha256 {source_rehash[:12]} != verified {expected_sha256[:12]})")
    finally:
        os.close(final_fd)


def git_tracked_status(path: str, repo_root: str) -> tuple[str, str]:
    """Round 33 F2: interpret ``git ls-files --error-unmatch`` by EXACT exit code, never by
    ``returncode != 0``. Returns ``(status, diagnostic)`` where status is one of ``TRACKED`` (exit 0),
    ``UNTRACKED`` (exit 1 — the exact "path is not tracked" result), ``OUTSIDE_REPO`` (the path does
    not lie under ``repo_root``, so it cannot be a tracked file OF that repository and Git is never
    consulted), ``GIT_FAILED`` (any other exit, e.g. 128 repo/index/permission error),
    ``GIT_TIMED_OUT`` or ``GIT_UNAVAILABLE``. Only ``UNTRACKED`` and ``OUTSIDE_REPO`` let publication
    proceed; every other state (including a Git-internal failure) blocks.

    ``OUTSIDE_REPO`` exists because the review package is published to the operator's archive next to
    the repository (package-hygiene amendment, 2026-08-23). Asking Git about such a path yields exit
    128 ("is outside repository"), which this function must keep reading as a hard block for paths it
    was actually asked about — so the out-of-repo case is decided by path containment BEFORE the
    subprocess runs, never by reinterpreting a Git error."""
    try:
        abs_path = os.path.abspath(path)
        abs_root = os.path.abspath(repo_root)
        rel = os.path.relpath(abs_path, abs_root)
    except ValueError:
        return "OUTSIDE_REPO", "output path is not within the repository root"
    if abs_path != abs_root and not abs_path.startswith(abs_root + os.sep):
        return "OUTSIDE_REPO", ""
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
    if status not in ("UNTRACKED", "OUTSIDE_REPO"):
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


def _cleanup_published_link(final_path: str, owned_inode: tuple[int, int]) -> None:
    """Round 37 F2: remove the final path ONLY if it is still the inode this invocation created.
    ``owned_inode`` is known from ``fstat(anonymous_fd)`` BEFORE publication — never derived from
    a post-link observation of the final path."""
    try:
        st = os.lstat(final_path)
        if (st.st_dev, st.st_ino) == owned_inode:
            os.unlink(final_path)
    except OSError:
        pass


def _create_anonymous_inode(parent: str) -> int:
    """Create an anonymous regular file in ``parent`` via ``O_TMPFILE``. Returns an open writable FD.
    Raises ``PublishSourceError`` if ``O_TMPFILE`` is not supported."""
    if not hasattr(os, "O_TMPFILE"):
        raise PublishSourceError(
            "O_TMPFILE is not available on this platform; cannot create an anonymous publication inode")
    try:
        return os.open(parent, os.O_RDWR | os.O_TMPFILE, 0o644)
    except OSError as exc:
        raise PublishSourceError(
            f"cannot create anonymous inode in {parent!r} (O_TMPFILE): {exc}") from None


def probe_anonymous_publication_capability(directory: str) -> str:
    """Round 38 F6: typed capability probe for anonymous-inode publication.

    Returns one of: SUPPORTED, UNSUPPORTED_OS, UNSUPPORTED_FILESYSTEM,
    LINKAT_UNAVAILABLE, PERMISSION_DENIED."""
    if not hasattr(os, "O_TMPFILE"):
        return CAPABILITY_UNSUPPORTED_OS
    if _get_linkat() is None:
        return CAPABILITY_LINKAT_UNAVAILABLE
    try:
        fd = os.open(directory, os.O_RDWR | os.O_TMPFILE, 0o644)
    except PermissionError:
        return CAPABILITY_PERMISSION_DENIED
    except OSError:
        return CAPABILITY_UNSUPPORTED_FILESYSTEM
    os.close(fd)
    return CAPABILITY_SUPPORTED


def publish_atomically(source_path: str, final_path: str, repo_root: str,
                       *, cleanup_source: bool = True,
                       expected_sha256: str | None = None) -> None:
    """Round 37 F1/F2: publish a private ZIP to ``final_path`` through an anonymous inode.

    The named ``source_path`` is never directly linked to the final path. Instead:
    1. An anonymous inode is created via ``O_TMPFILE`` in the final parent.
    2. Source bytes are copied into the anonymous FD.
    3. The anonymous FD is fsynced and hashed; hash must equal ``expected_sha256``.
    4. The anonymous inode identity is recorded from ``fstat(anonymous_fd)`` BEFORE publication.
    5. ``linkat(fd, "", AT_FDCWD, final, AT_EMPTY_PATH)`` publishes with no-replace semantics.
    6. Post-publication: final path opened O_NOFOLLOW, inode + hash verified against anonymous FD.
    7. On failure, cleanup uses the pre-publication inode identity (never post-race observation).

    No named source path participates in the security decision. ``expected_sha256`` is mandatory."""
    final = os.path.abspath(final_path)
    parent = os.path.dirname(final) or "."
    anon_fd = -1
    owned_inode: tuple[int, int] | None = None
    source_inode: tuple[int, int] | None = None
    published = False
    try:
        if expected_sha256 is None:
            raise PublishSourceError(
                "no verified source SHA-256 was bound; refusing to publish an unverified source")
        if not os.path.isdir(parent):
            raise PublishCollisionError(f"output parent directory does not exist: {parent!r}")

        # Round 38 F6: record source inode BEFORE copy for ownership-bound cleanup.
        try:
            src_st = os.lstat(source_path)
            source_inode = (src_st.st_dev, src_st.st_ino)
        except OSError:
            pass

        anon_fd = _create_anonymous_inode(parent)
        _copy_to_fd(source_path, anon_fd)
        os.fsync(anon_fd)
        os.fchmod(anon_fd, 0o444)

        anon_hash = _sha256_fd(anon_fd)
        if anon_hash != expected_sha256:
            raise PublishSourceError(
                f"anonymous inode bytes do not match expected hash "
                f"(sha256 {anon_hash[:12]} != verified {expected_sha256[:12]})")

        anon_st = os.fstat(anon_fd)
        owned_inode = (anon_st.st_dev, anon_st.st_ino)

        assert_publishable(final, repo_root, owned_paths=frozenset({final, final_path}))

        try:
            _linkat_anonymous(anon_fd, final)
        except FileExistsError:
            raise PublishCollisionError(
                f"another invocation already published {final_path!r}; this one loses the race")
        except OSError as exc:
            raise PublishCollisionError(f"could not publish {final_path!r}: {exc}")

        published = True
        verify_published_identity(anon_fd, final, expected_sha256)

    except (PublishSourceError, PublishCollisionError):
        if published and owned_inode is not None:
            _cleanup_published_link(final, owned_inode)
        raise
    finally:
        if anon_fd >= 0:
            os.close(anon_fd)
        if cleanup_source:
            _cleanup_source_if_owned(source_path, source_inode)


def _cleanup_source_if_owned(source_path: str,
                             owned_inode: tuple[int, int] | None) -> None:
    """Round 38 F6: unlink source ONLY if it is still the inode we recorded before copy.
    A replaced or moved source is never unlinked."""
    if owned_inode is None:
        return
    try:
        st = os.lstat(source_path)
        if (st.st_dev, st.st_ino) == owned_inode:
            os.unlink(source_path)
    except OSError:
        pass
