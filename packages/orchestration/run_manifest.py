"""F012 — the deterministic run-input manifest (hardened).

Every completed or stopped job EPISODE records ONE immutable `RunManifestV1`: a versioned,
canonical, hashable snapshot of the INPUTS that episode was given — the input snapshot
captured at episode START (config, environment, Remedy code identity incl. a dirty-tree flag,
target/base identity, models and provider versions actually used), plus the per-call input
fingerprints recorded as the episode ran. A job can have several episodes (a stopped attempt,
then a resumed completed run); a small index names them all and the latest.

The honesty rule is load-bearing and pinned by a docs test and the CLI:

    Inputs are reproducible and verified; LLM outputs are recorded, not promised.

What "verified" means precisely:

* the manifest records INPUTS, never a promise about LLM output;
* `remedy job rerun --check-manifest` freshly reconstructs the CURRENT would-be inputs
  (current target HEAD/tree, current config/env/models, current Remedy identity) — it does
  NOT reuse the recorded historical values;
* per-call assembled-prompt reconstruction that would require a worktree replay (F140) is a
  declared CAPABILITY GAP: the check reports INCOMPLETE coverage and never claims "same
  inputs" for a dimension it did not verify.

No database. No provider generation call. Call fingerprints are the providers' own
`prepared_input` (the exact request each transport received), never a re-hash from a
different code path.
"""
from __future__ import annotations

import contextlib
import dataclasses
import errno
import hashlib
import json
import os
import platform
import re
import secrets
import stat
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration import manifest_schema as _S
from packages.orchestration.call_identity import (
    CallIdentity,
    canonical_call_number,
    parse_canonical_call_number,
)

MANIFEST_VERSION = 1

MANIFEST_FILENAME = "run_manifest.json"          # the latest episode, at the evidence root
MANIFEST_INTEGRITY_FILE = "manifest_integrity.json"
MANIFESTS_SUBDIR = "run_manifests"               # run_manifests/<episode_id>/run_manifest.json
MANIFEST_INDEX_FILENAME = "run_manifest_index.json"
CALLS_SUBDIR = "calls"                           # per-episode call-input fingerprint artifacts
#: F1 (round 12): the per-episode canonical Run Call LEDGERS. A count plus a self-asserted hash
#: proves nothing — the bytes it names have to be IN the verified tree, or a stored reference can
#: quietly claim a shorter ledger and validate.
LEDGERS_SUBDIR = "call_ledgers"

MANIFEST_DIR_MODE = 0o700
MANIFEST_FILE_MODE = 0o600

UNAVAILABLE = "unavailable"
REDACTED = "[REDACTED]"

#: The durable marker a job created/first-run under F012 carries. Its presence is how a
#: completed/stopped job WITHOUT a manifest is judged blocking (marked) vs legacy (unmarked).
MANIFEST_REQUIRED_VERSION = 1

_SECRET_TERMS = ("token", "key", "secret", "password", "credential")
_VERSION_PROBE_TIMEOUT_S = 5
_VERSION_PROBE_MAX_CHARS = 200

COVERAGE_COMPLETE = "complete"
COVERAGE_INCOMPLETE = "incomplete"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ManifestError(RuntimeError):
    """The manifest could not be built, written or read safely."""


class ManifestConflictError(ManifestError):
    """A different manifest already exists for this episode."""


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------


def is_secret_key(key: str) -> bool:
    low = str(key or "").lower()
    return any(term in low for term in _SECRET_TERMS)


def _safe_scalar(value: Any) -> Any:
    from packages.orchestration.failure_postmortem import safe_text

    return safe_text(value) if isinstance(value, str) else value


# ---------------------------------------------------------------------------
# Finalized call (identity + fingerprint)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FinalizedCall:
    """One finalized logical provider call: unique identity + the exact input fingerprint."""

    identity: CallIdentity
    fingerprint: str                 # the provider's prepared_input fingerprint (exact sent)
    prepared_input: dict[str, Any]   # the fingerprint components, for the artifact
    fingerprint_source: str          # provider_transport | loop_fallback
    ok: bool
    artifact: str = ""               # episode-relative ref to the call-input artifact file
    artifact_sha256: str = ""        # sha256 of the canonical artifact bytes (F3 integrity)

    def to_json(self) -> dict[str, Any]:
        return {
            "identity": self.identity.to_json(),
            "fingerprint": self.fingerprint,
            "prepared_input": self.prepared_input,
            "fingerprint_source": self.fingerprint_source,
            "ok": self.ok,
            "artifact": self.artifact,
            "artifact_sha256": self.artifact_sha256,
        }

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "FinalizedCall":
        """F14: TRUSTED in-memory canonical data ONLY. Untrusted disk records MUST use
        ``decode_finalized_call_v1``."""
        return cls(
            identity=CallIdentity.from_trusted_json(d.get("identity") or {}),
            fingerprint=str(d.get("fingerprint", "")),
            prepared_input=dict(d.get("prepared_input") or {}),
            fingerprint_source=str(d.get("fingerprint_source", "")),
            ok=bool(d.get("ok", True)),
            artifact=str(d.get("artifact", "")),
            artifact_sha256=str(d.get("artifact_sha256", "")),
        )

    def canonical_artifact_bytes(self) -> bytes:
        """The EXACT bytes of this call's artifact file — the single source both the writer
        and the integrity check derive from, so tampering with identity, fingerprint,
        prepared_input or ok changes the hash."""
        return _fs.json_bytes({
            "identity": self.identity.to_json(),
            "fingerprint": self.fingerprint,
            "prepared_input": self.prepared_input,
            "fingerprint_source": self.fingerprint_source,
            "ok": self.ok,
        }, sort_keys=True)

    def sort_key(self) -> tuple:
        return self.identity.key()


@dataclass(frozen=True)
class FinalizedCallContext:
    """What the single ``on_call_finalized`` seam carries. F012 records the input; F010's
    post-mortem writer, on a terminal failure, describes the SAME ``identity.call_id``."""

    identity: CallIdentity
    fingerprint: str
    prepared_input: dict[str, Any]
    fingerprint_source: str
    ok: bool


def on_call_finalized(ctx: FinalizedCallContext, sink: list) -> None:
    """Record one finalized logical call. The manifest's call set is built ONLY from what this
    seam produces — never by walking call directories."""
    sink.append(FinalizedCall(
        identity=ctx.identity,
        fingerprint=ctx.fingerprint,
        prepared_input=dict(ctx.prepared_input),
        fingerprint_source=ctx.fingerprint_source,
        ok=ctx.ok,
    ))


# ---------------------------------------------------------------------------
# Probes and current-state inspection
# ---------------------------------------------------------------------------


def _run_probe(argv: list[str], cwd: str | None = None) -> str:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, shell=False,
                              timeout=_VERSION_PROBE_TIMEOUT_S, cwd=cwd)
    except Exception:
        return UNAVAILABLE
    if proc.returncode != 0 or not proc.stdout or not proc.stdout.strip():
        return UNAVAILABLE
    from packages.orchestration.failure_postmortem import safe_text

    return safe_text(proc.stdout.strip())[:_VERSION_PROBE_MAX_CHARS]


def probe_provider_version(provider: str, cwd: str | None = None) -> str:
    import shutil

    name = (provider or "").strip().lower()
    if name in ("", "fake"):
        return UNAVAILABLE
    exe = "claude" if name.startswith("claude") else name
    path = shutil.which(exe)
    if not path:
        return UNAVAILABLE
    return _run_probe([path, "--version"], cwd=cwd)


def _remedy_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_sha(v: str) -> bool:
    return len(v) == 40 and all(c in "0123456789abcdef" for c in v)


#: A worktree-identity component either succeeded (bytes), or explicitly did not. It is NEVER
#: mapped to empty bytes: a failed `git diff` that reads as "no diff" would make a dirty tree
#: look clean, which is exactly the fail-open bug F3 exists to close.
GIT_OK = "ok"
GIT_UNAVAILABLE = "unavailable"     # not a git repo / git missing
GIT_INCOMPLETE = "incomplete"       # a component failed (nonzero, timeout, unsupported file)


@dataclass(frozen=True)
class WorktreeIdentity:
    """The strict content identity of a git worktree — Remedy's or the target's.

    ``status`` is ``ok`` only when every component was collected; ``unavailable`` when the
    path is not a usable git repo; ``incomplete`` when a component failed (a git error, a
    timeout, an untracked special file) — never silently clean. The comparison treats
    ``incomplete``/``unavailable`` as a coverage problem, never as equality."""

    status: str
    head: str                       # HEAD commit sha, or "unavailable"
    digest: str                     # content digest (only meaningful when status == ok)
    problems: tuple[str, ...] = ()
    #: F4: True when the tree has staged/unstaged/untracked/submodule changes, False when a
    #: successful collection found none, None when the identity is unavailable/incomplete.
    #: ``problems`` means COLLECTION FAILURE, not dirtiness.
    dirty: bool | None = None

    def to_json(self) -> dict[str, Any]:
        return {"status": self.status, "head": self.head, "digest": self.digest,
                "problems": list(self.problems), "dirty": self.dirty}

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "WorktreeIdentity":
        return cls(status=str(d.get("status", GIT_UNAVAILABLE)),
                   head=str(d.get("head", "")), digest=str(d.get("digest", "")),
                   problems=tuple(d.get("problems") or []), dirty=d.get("dirty"))


#: F7 (round 12): every configured helper git might EXECUTE during a read-only inspection.
#:
#: A "read-only" verification that runs arbitrary repository-configured commands is not read-only:
#: `core.fsmonitor` alone was enough to make `worktree_identity()` execute a script and still
#: report `status=ok, problems=[]`. Reading a repository must never mean running its code.
#:
#: `filter.*.process` is disabled by pointing it at `false` AND clearing `required`, so a
#: required-but-disabled filter cannot turn into a silent success.
_HELPER_NEUTRALIZING_ARGS: tuple[str, ...] = (
    "-c", "core.fsmonitor=false",
    "-c", "core.fsmonitorHookVersion=0",
    "-c", "core.hooksPath=/dev/null",
    "-c", "diff.external=",
    "-c", "core.sshCommand=false",
    "-c", "protocol.ext.allow=never",
    "-c", "uploadpack.packObjectsHook=",
)

#: F7: the config a repository can point at a program, discovered per repo and neutralized.
_HELPER_CONFIG_PATTERN = r"^(filter\..*\.(clean|smudge|process|required)|diff\..*\.(command|textconv)|core\.fsmonitor)$"


def _git_helper_env() -> dict[str, str]:
    """F7: a constrained environment for read-only inspection.

    Global and system git config can point at helpers too, and they are not facts about the
    repository F012 is hashing — so they are taken out of the picture entirely rather than
    trusted to be harmless.
    """
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_OPTIONAL_LOCKS"] = "0"        # never take a lock for a read
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = ""
    env["GIT_ALLOW_PROTOCOL"] = "none"
    env.pop("GIT_EXTERNAL_DIFF", None)
    env.pop("GIT_SSH_COMMAND", None)
    return env


def _helper_neutralizing_args(cwd: str, env: dict[str, str]) -> list[str]:
    """F7 (round 12): discover this repository's configured helpers and neutralize each one.

    The clean/smudge substitution keeps the identity meaningful: it digests the RAW working-tree
    bytes, and both sides of every comparison are captured the same way, so drift detection is
    unaffected while no configured command ever runs.
    """
    args = list(_HELPER_NEUTRALIZING_ARGS)
    try:
        proc = subprocess.run(
            ["git", "config", "--name-only", "--get-regexp", _HELPER_CONFIG_PATTERN],
            capture_output=True, shell=False, timeout=5, cwd=cwd, env=env)
    except Exception:
        return args
    if proc.returncode != 0:
        return args                     # nothing configured (git exits 1)
    for name in proc.stdout.decode("utf-8", "replace").split():
        name = name.strip()
        if name.endswith((".clean", ".smudge")):
            args += ["-c", f"{name}=cat"]          # a passthrough, never the configured command
        elif name.endswith(".process"):
            args += ["-c", f"{name}=false"]
        elif name.endswith(".required"):
            args += ["-c", f"{name}=false"]        # a disabled filter must not be "required"
        elif name.endswith((".command", ".textconv")):
            args += ["-c", f"{name}="]
        elif name == "core.fsmonitor":
            args += ["-c", "core.fsmonitor=false"]
    return args


def _git_bytes(repo_path: str, args: list[str], *, timeout: int = 15):
    """Run one git plumbing command. Returns ``(ok, bytes, problem)`` — a failure is NEVER
    an empty success. Local paths in error text are redacted.

    F6/F7 (round 12): the command runs with ``cwd`` bound to the caller's already-verified
    directory (``repo_path`` may be an fd-bound `/proc/self/fd/N` path, which cannot be swapped
    out from under us), and with every configured helper neutralized.
    """
    env = _git_helper_env()
    try:
        proc = subprocess.run(
            ["git", *_helper_neutralizing_args(repo_path, env), *args],
            capture_output=True, shell=False, timeout=timeout, cwd=repo_path, env=env)
    except subprocess.TimeoutExpired:
        return False, b"", f"git {args[0]} timed out"
    except Exception as exc:
        return False, b"", f"git {args[0]} failed: {type(exc).__name__}"
    if proc.returncode != 0:
        return False, b"", f"git {args[0]} exited {proc.returncode}"
    return True, proc.stdout, ""


def inspect_contained_workspace_identity(canonical_root: str | Path,
                                         claimed_workspace_path: str | Path
                                         ) -> WorktreeIdentity:
    """F6 (round 12): containment must stay BOUND through the actual inspection.

    Verifying a path and then handing back an ordinary ``Path`` proves nothing: the name can be
    renamed and replaced with a symlink to another repository between the check and the read, and
    the inspection then runs against — and reports facts from — that outside repository. Exactly
    that was reproduced: the swapped-in outside repo's HEAD was observed.

    So the final workspace directory descriptor is OPENED under an anchored, no-follow traversal
    of the canonical root and HELD OPEN for the whole inspection; git runs with its cwd bound to
    that open description (``/proc/self/fd/N``), which no rename can redirect. The identity of the
    held directory is re-checked after the inspection, so a concurrent replacement is reported
    rather than believed.

    Fails CLOSED where an fd-bound cwd cannot be guaranteed.
    """
    from packages.orchestration import worktrees as _wt      # noqa: F401  (import symmetry)

    if not hasattr(os, "O_DIRECTORY") or not Path("/proc/self/fd").is_dir():
        # No fd-bound cwd available: refuse rather than fall back to a name-based inspection.
        return WorktreeIdentity(
            GIT_UNAVAILABLE, UNAVAILABLE, "",
            ("this platform cannot bind an inspection to a verified directory handle; "
             "refusing to inspect a workspace by name",))
    fd = _open_contained_workspace_fd(canonical_root, claimed_workspace_path)
    if fd is None:
        return WorktreeIdentity(
            GIT_UNAVAILABLE, UNAVAILABLE, "",
            ("job workspace is absent, symlinked, or outside the canonical worktree root",))
    try:
        before = os.fstat(fd)
        # The fd-bound path: the kernel resolves it to the OPEN DESCRIPTION, so renaming or
        # replacing the directory's NAME cannot redirect this inspection.
        bound = f"/proc/self/fd/{fd}"
        # git's cwd is bound to the OPEN DESCRIPTION; the untracked-file reads reuse the same
        # held descriptor rather than re-resolving any name.
        identity = worktree_identity(bound, root_dir_fd=fd)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino):
            return WorktreeIdentity(
                GIT_INCOMPLETE, UNAVAILABLE, "",
                ("the job workspace changed identity during inspection",))
        return identity
    finally:
        os.close(fd)


def _open_contained_workspace_fd(canonical_root: str | Path,
                                 claimed: str | Path) -> int | None:
    """Anchored, no-follow traversal from the canonical root to the claimed workspace, returning
    the HELD descriptor of the final directory (the caller closes it). ``None`` when the path is
    absent, symlinked, or outside the root.

    F7 (round 13): containment is decided LEXICALLY, by the one canonical helper, BEFORE anything
    is opened. ``Path.relative_to`` does not normalize, so ``root/sub/../../outside`` used to come
    back as the components ``sub, .., .., outside`` — and since ``..`` is neither a symlink nor a
    non-directory, every no-follow identity check below passed it and the walk stepped out of the
    root one level per component. The escape was reproduced end to end: the outside repository's
    HEAD was read and reported ``status=ok``.

    ``secure_fs.lexical_parts`` normalizes first and then asks whether the result is still under
    the root, so a traversal is refused before a descriptor exists — which is also why
    ``resolve()`` is the wrong tool here (it answers "where does this point", not "did you route
    me through a link"). ``open_verified_dir`` refuses ``..`` on its own as defence in depth.
    """
    root = Path(canonical_root)
    try:
        parts = _fs.lexical_parts(claimed, root, error_cls=ManifestError,
                                  noun="job workspace")
    except Exception:
        return None
    if not parts:
        # The root itself is not a workspace; an empty relative path names no target.
        return None
    try:
        fd = _fs.anchor_root(root, error_cls=ManifestError, noun="job workspace", create=False)
    except Exception:
        return None
    for part in parts:
        try:
            nxt = _fs.open_verified_dir(part, dir_fd=fd, error_cls=ManifestError,
                                        noun="job workspace")
        except Exception:
            os.close(fd)
            return None
        os.close(fd)
        fd = nxt
    return fd


def worktree_identity(repo_path: str, *, root_dir_fd: int | None = None
                      ) -> WorktreeIdentity:
    """One strict git-worktree content identity, shared by Remedy and the target.

    Hashes the committed tree, the staged and unstaged BINARY diffs (which encode content,
    renames, copies, mode and deletions), every untracked entry (regular file → bytes+mode;
    symlink → the LINK TARGET TEXT + a marker, never followed; special/FIFO/socket/device →
    marked unsupported, never opened; directory that git reports → its contained files), and
    submodule status. Any component failure makes the whole identity ``incomplete``."""
    if not repo_path or not Path(repo_path).is_dir():
        return WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "",
                                ("path is not a directory",))
    ok_head, head_out, head_problem = _git_bytes(repo_path, ["rev-parse", "HEAD"], timeout=5)
    head = head_out.decode("utf-8", "replace").strip() if ok_head else ""
    if not _is_sha(head):
        return WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "",
                                (head_problem or "no HEAD commit",))

    import stat as _stat

    problems: list[str] = []
    dirty = False                        # F4: any real change flips this
    h = hashlib.sha256()

    ok_tree, tree_out, tp = _git_bytes(repo_path, ["rev-parse", "HEAD^{tree}"], timeout=5)
    if not ok_tree:
        problems.append(tp)
    h.update(b"head_tree\0")
    h.update(tree_out.strip())

    for label, args in (("unstaged", ["diff", "--binary", "--no-ext-diff"]),
                        ("staged", ["diff", "--cached", "--binary", "--no-ext-diff"])):
        ok, out, prob = _git_bytes(repo_path, args)
        h.update(f"\0{label}\0".encode())
        if not ok:
            problems.append(f"{label}: {prob}")
            h.update(b"\0FAILED\0")          # a failed component is not an empty one
            h.update(prob.encode())
        else:
            if out.strip():
                dirty = True
            h.update(out)

    ok_u, others, up = _git_bytes(repo_path, ["ls-files", "--others", "--exclude-standard",
                                              "-z"])
    h.update(b"\0untracked\0")
    if not ok_u:
        problems.append(f"untracked: {up}")
        h.update(b"\0FAILED\0")
        h.update(up.encode())
    root_fd: int | None = None
    owns_root_fd = False
    if root_dir_fd is not None:
        # F6 (round 12): the caller already HOLDS a verified descriptor for this directory —
        # anchoring by name again would reintroduce exactly the swap this fd exists to prevent
        # (and an fd-bound path legitimately contains a symlink component, which the anchored
        # walker refuses by design).
        root_fd = root_dir_fd
    else:
        owns_root_fd = True
        try:
            root_fd = _fs.anchor_root(repo_path, error_cls=ManifestError, noun="worktree")
        except ManifestError as exc:
            problems.append(f"cannot anchor worktree root: {exc}")
    try:
        for rel in sorted(p for p in others.split(b"\0") if p):
            dirty = True                     # any untracked entry means dirty
            h.update(b"path\0")
            h.update(rel)
            rel_text = rel.decode("utf-8", "surrogateescape")
            # F3: read the untracked entry through VERIFIED directory FDs, never by name. This
            # closes the lstat-then-open race: what we fstat after opening must be the same
            # inode we no-follow-stat'd, so a swap to an external symlink between the two is
            # caught and nothing outside the repo is ever read.
            if root_fd is None:
                h.update(b"\0no-anchor\0")
                continue
            try:
                content, kind = _read_untracked_verified(root_fd, rel_text)
            except _UntrackedRace:
                h.update(b"\0race\0")
                problems.append("an untracked entry changed during collection")
                continue
            except _UntrackedSymlink as exc:
                h.update(b"\0symlink\0")
                h.update(str(exc).encode("utf-8", "surrogateescape"))   # link text, never target
                continue
            except _UntrackedSpecial:
                h.update(b"\0special\0")
                problems.append("an untracked special file cannot be content-hashed")
                continue
            except _UntrackedMissing:
                h.update(b"\0vanished\0")
                problems.append("an untracked entry disappeared during collection")
                continue
            except ManifestError:
                h.update(b"\0error\0")
                problems.append("an untracked entry could not be read safely")
                continue
            except OSError as exc:
                # F9: any bounded file-I/O failure (permission denied, read error, fstat
                # failure) folds into a typed INCOMPLETE result — never an empty success and
                # never an escaping exception. The error TYPE is recorded, but no raw local
                # path is leaked into the diagnostic.
                h.update(b"\0ioerror\0")
                h.update(type(exc).__name__.encode())
                problems.append(f"an untracked entry raised {type(exc).__name__} during read")
                continue
            h.update(f"\0{kind}\0".encode())
            h.update(hashlib.sha256(content).digest())
    finally:
        # F9: the root FD is ALWAYS closed, even if the loop raises — no descriptor leak.
        if root_fd is not None and owns_root_fd:
            os.close(root_fd)          # never close a descriptor the CALLER still holds

    ok_s, subm, sp = _git_bytes(repo_path, ["submodule", "status"])
    if not ok_s:
        problems.append(f"submodules: {sp}")
    elif subm.strip():
        dirty = True
        h.update(b"\0submodules\0")
        h.update(subm)

    status = GIT_OK if not problems else GIT_INCOMPLETE
    dirty_val: bool | None = dirty if status == GIT_OK else None
    return WorktreeIdentity(status, head, h.hexdigest(), tuple(problems), dirty=dirty_val)


class _UntrackedRace(Exception):
    pass


class _UntrackedSymlink(Exception):
    pass


class _UntrackedSpecial(Exception):
    pass


class _UntrackedMissing(Exception):
    pass


def _read_untracked_verified(root_fd: int, rel: str) -> tuple[bytes, str]:
    """Read an untracked file's bytes through held, symlink-refusing directory FDs.

    Walks every parent component with ``open_verified_dir`` (a symlinked parent is refused),
    then no-follow stats the final entry, requires a regular file, opens it ``O_NOFOLLOW`` and
    ``fstat``s it. F7: it captures the FULL identity+content metadata (dev, ino, type, size,
    mtime_ns, ctime_ns) after the open and again after the read, and requires them IDENTICAL —
    so a SAME-SIZE in-place rewrite during hashing (which cannot leave ``mtime_ns``/``ctime_ns``
    unchanged) is detected and raised as a race, never returned as a stable ok read of mixed
    bytes. A symlink raises ``_UntrackedSymlink`` carrying the LINK TEXT."""
    import stat as _stat

    def _meta(st: os.stat_result) -> tuple:
        return (st.st_dev, st.st_ino, _stat.S_IFMT(st.st_mode), st.st_size,
                st.st_mtime_ns, st.st_ctime_ns)

    parts = [p for p in rel.replace("\\", "/").split("/") if p and p != "."]
    if not parts or any(p == ".." for p in parts):
        raise ManifestError(f"unsafe untracked path {rel!r}")
    cur = os.dup(root_fd)
    try:
        for comp in parts[:-1]:
            try:
                nxt = _fs.open_verified_dir(comp, dir_fd=cur, error_cls=ManifestError,
                                            noun="worktree")
            except _fs.MissingComponent:
                raise _UntrackedMissing(rel) from None
            os.close(cur)
            cur = nxt
        name = parts[-1]
        try:
            pre = os.stat(name, dir_fd=cur, follow_symlinks=False)
        except FileNotFoundError:
            raise _UntrackedMissing(rel) from None
        if _stat.S_ISLNK(pre.st_mode):
            try:
                target = os.readlink(name, dir_fd=cur)
            except OSError:
                target = "\0unreadable-link\0"
            raise _UntrackedSymlink(target)
        if not _stat.S_ISREG(pre.st_mode):
            raise _UntrackedSpecial(rel)
        fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=cur)
        try:
            post = os.fstat(fd)
            if (not _stat.S_ISREG(post.st_mode)
                    or (post.st_dev, post.st_ino) != (pre.st_dev, pre.st_ino)):
                raise _UntrackedRace(rel)
            before = _meta(post)
            chunks: list[bytes] = []
            total = 0
            while True:
                b = os.read(fd, 1 << 20)
                if not b:
                    break
                chunks.append(b)
                total += len(b)
                if total > (256 << 20):        # a quarter-GB untracked file: refuse, not hang
                    raise ManifestError("untracked file too large to hash")
            # F7: any material metadata change across the read — size OR mtime_ns OR ctime_ns —
            # means the file was mutated while we hashed it. The bytes we have are not a stable
            # snapshot; refuse them rather than return a mixed-content digest as ``ok``.
            if _meta(os.fstat(fd)) != before:
                raise _UntrackedRace(rel)
            data = b"".join(chunks)
            return data, f"regfile-{oct(post.st_mode & 0o777)}"
        finally:
            os.close(fd)
    finally:
        os.close(cur)


def remedy_worktree_identity() -> WorktreeIdentity:
    return worktree_identity(str(_remedy_repo_root()))


# --- backward-compatible scalar accessors (used by the snapshot) ---

def remedy_git_sha() -> str:
    wt = remedy_worktree_identity()
    return wt.head if _is_sha(wt.head) else UNAVAILABLE


def remedy_dirty() -> bool | None:
    """F4: the typed dirty state (True/False/None), NOT whether collection had problems."""
    return remedy_worktree_identity().dirty


def target_head(repo_path: str) -> str:
    wt = worktree_identity(repo_path)
    return wt.head if _is_sha(wt.head) else UNAVAILABLE


def target_tree(repo_path: str) -> str:
    wt = worktree_identity(repo_path)
    return wt.digest if wt.status == GIT_OK else UNAVAILABLE


def _config_snapshot() -> list[dict[str, Any]]:
    from packages.orchestration.config import all_key_specs, get_config

    cfg = get_config()
    out: list[dict[str, Any]] = []
    for spec in all_key_specs():
        cv = cfg.get_value(spec.key)
        if cv is None:
            continue
        secret = bool(spec.secret) or bool(spec.env_only) or is_secret_key(spec.key)
        value: Any = (REDACTED if cv.value is not None else None) if secret \
            else _safe_scalar(cv.value)
        out.append({"key": spec.key, "value": value, "source": cv.source.value})
    return sorted(out, key=lambda e: e["key"])


def _environment_snapshot() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for name in sorted(os.environ):
        if not name.startswith("REMEDY_"):
            continue
        out.append({"key": name,
                    "value": REDACTED if is_secret_key(name)
                    else _safe_scalar(os.environ[name])})
    return sorted(out, key=lambda e: e["key"])


def _models_for_job(job: Any) -> dict[str, str]:
    ec = getattr(job, "execution_config", None)
    if ec is None:
        return {}

    def _pm(provider: str, model: str) -> str:
        provider = (provider or "").strip() or UNAVAILABLE
        model = (model or "").strip()
        return f"{provider}/{model}" if model else provider

    models = {"builder": _pm(ec.builder, ec.builder_model),
              "reviewer": _pm(ec.reviewer, ec.reviewer_model)}
    if (ec.repair_provider or "").strip() or (ec.repair_model or "").strip():
        models["repair"] = _pm(ec.repair_provider or ec.builder, ec.repair_model)
    return models


# ---------------------------------------------------------------------------
# Start-time input snapshot (F12)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InputSnapshot:
    """The immutable inputs a run EPISODE started with — captured at episode start, not
    re-probed at the end. The check candidate builds a FRESH one through the same resolver."""

    remedy_git_sha: str
    remedy_dirty: bool | None           # F4: True/False/None — tri-state, not "has problems"
    remedy_worktree: dict[str, Any]     # F2: strict Remedy source content identity
    target_base_commit: str
    target_head: str
    target_tree: str
    target_worktree: dict[str, Any]     # F3: strict target worktree identity + status
    job_initial_tree: str
    episode_start_workspace_tree: str   # F4: workspace tree at THIS episode's start
    #: F10 (round 11): the STRICT content identity of the job workspace at this episode's start,
    #: using the same digest as the other worktrees. A git tree object alone cannot be compared
    #: read-only against a live workspace (computing one WRITES objects), so the record that a
    #: check compares against has to be an identity, not a tree hash.
    episode_start_workspace_identity: dict[str, Any]
    job_file_sha256: str
    job_input: dict[str, Any]           # F1: complete job-input definition
    models: dict[str, str]
    provider_versions: dict[str, str]
    config: list[dict[str, Any]]
    environment: list[dict[str, Any]]
    python_version: str
    platform: str
    pythonhashseed: str

    def to_json(self) -> dict[str, Any]:
        return {
            "remedy_git_sha": self.remedy_git_sha,
            "remedy_dirty": self.remedy_dirty,
            "remedy_worktree": self.remedy_worktree,
            "target_base_commit": self.target_base_commit,
            "target_head": self.target_head,
            "target_tree": self.target_tree,
            "target_worktree": self.target_worktree,
            "job_initial_tree": self.job_initial_tree,
            "episode_start_workspace_tree": self.episode_start_workspace_tree,
            "episode_start_workspace_identity": self.episode_start_workspace_identity,
            "job_file_sha256": self.job_file_sha256,
            "job_input": self.job_input,
            "models": dict(sorted(self.models.items())),
            "provider_versions": dict(sorted(self.provider_versions.items())),
            "config": sorted(self.config, key=lambda e: str(e.get("key", ""))),
            "environment": sorted(self.environment, key=lambda e: str(e.get("key", ""))),
            "python_version": self.python_version,
            "platform": self.platform,
            "pythonhashseed": self.pythonhashseed,
        }

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "InputSnapshot":
        """F14: TRUSTED in-memory data ONLY — untrusted records use ``decode_input_snapshot_v1``."""
        return cls(
            remedy_git_sha=str(d.get("remedy_git_sha", "")),
            remedy_dirty=(None if d.get("remedy_dirty") is None
                          else bool(d.get("remedy_dirty"))),
            remedy_worktree=dict(d.get("remedy_worktree") or {}),
            target_base_commit=str(d.get("target_base_commit", "")),
            target_head=str(d.get("target_head", "")),
            target_tree=str(d.get("target_tree", "")),
            target_worktree=dict(d.get("target_worktree") or {}),
            job_initial_tree=str(d.get("job_initial_tree", "")),
            episode_start_workspace_tree=str(d.get("episode_start_workspace_tree", "")),
            episode_start_workspace_identity=dict(
                d.get("episode_start_workspace_identity") or {}),
            job_file_sha256=str(d.get("job_file_sha256", "")),
            job_input=dict(d.get("job_input") or {}),
            models={str(k): str(v) for k, v in (d.get("models") or {}).items()},
            provider_versions={str(k): str(v)
                               for k, v in (d.get("provider_versions") or {}).items()},
            config=sorted((dict(e) for e in (d.get("config") or [])),
                          key=lambda e: str(e.get("key", ""))),
            environment=sorted((dict(e) for e in (d.get("environment") or [])),
                               key=lambda e: str(e.get("key", ""))),
            python_version=str(d.get("python_version", "")),
            platform=str(d.get("platform", "")),
            pythonhashseed=str(d.get("pythonhashseed", "")),
        )


def _job_workspace_identity(job: Any) -> WorktreeIdentity:
    """F10/F11 (round 11): the strict identity of THIS job's workspace.

    The JobPlan's path is a CLAIM, not a trust root: it is only used after being proven to live
    under the canonical worktree root with no symlinked component anywhere on the way. A job with
    no workspace (planning-only, a pre-work stop that never acquired one, or a completed job
    whose worktree was cleaned) honestly reports an unavailable identity WITH a typed reason,
    rather than an empty string a reader would have to guess about.
    """
    repo = str(getattr(job, "repo_path", "") or "")
    ws_path = str(getattr(job, "job_workspace_path", "") or "")
    if not ws_path or not repo:
        return WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "",
                                ("no job workspace is named",))
    from packages.orchestration import worktrees as _wt

    try:
        root = _wt.worktrees_root_for(repo)
    except Exception:
        return WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "",
                                ("the canonical worktree root is unavailable",))
    _contained, state = contained_workspace_path(Path(ws_path), repo)
    if _contained is None and state == WS_ABSENT:
        return WorktreeIdentity(GIT_UNAVAILABLE, UNAVAILABLE, "",
                                ("job workspace is absent",))
    # F6 (round 12): the inspection is bound to a HELD descriptor from here on.
    return inspect_contained_workspace_identity(root, Path(ws_path))


#: F11 (round 11): why a workspace could not be inspected. ABSENT is not a failure — a completed
#: job legitimately cleans its worktree — but ESCAPES is: something is there and it is not where
#: it claims to be.
WS_OK = "ok"
WS_ABSENT = "absent"
WS_ESCAPES = "escapes"


def contained_workspace_path(candidate: Path, repo: str | Path) -> tuple[Path | None, str]:
    """F11 (round 11): resolve a job workspace ONLY through the canonical worktree root, with no
    symlinked component anywhere on the way — parents included.

    The persisted path is not its own trust root: a final component that looks normal says
    nothing about its parents, and ONE symlinked parent is enough to walk a "check" into an
    entirely different repository and report its contents as this job's inputs.

    Returns ``(path, WS_OK)``, ``(None, WS_ABSENT)`` when nothing is there, or
    ``(None, WS_ESCAPES)`` when something is there but is not contained.
    """
    from packages.orchestration import worktrees as _wt

    try:
        root = Path(_wt.worktrees_root_for(repo))
    except Exception:
        return None, WS_ESCAPES
    try:
        rel = Path(candidate).relative_to(root)
    except ValueError:
        return None, WS_ESCAPES          # outside the canonical root entirely
    if not rel.parts:
        return None, WS_ESCAPES
    try:
        root_fd = _fs.anchor_root(root, error_cls=ManifestError, noun="job workspace",
                                  create=False)
    except _fs.MissingComponent:
        return None, WS_ABSENT
    except Exception:
        return None, WS_ESCAPES
    fd = root_fd
    try:
        for part in rel.parts:
            # Anchored, no-follow: every component is verified, so a symlinked PARENT is refused
            # exactly like a symlinked final component.
            try:
                nxt = _fs.open_verified_dir(part, dir_fd=fd, error_cls=ManifestError,
                                            noun="job workspace")
            except _fs.MissingComponent:
                return None, WS_ABSENT
            except Exception:
                return None, WS_ESCAPES
            if fd != root_fd:
                os.close(fd)
            fd = nxt
        return root / rel, WS_OK
    finally:
        if fd != root_fd:
            os.close(fd)
        os.close(root_fd)


def build_input_snapshot(job: Any, *, probe_versions: bool = True,
                         inspect_target: bool = True) -> InputSnapshot:
    """Capture the current inputs — used at episode START and by the check CANDIDATE."""
    repo = getattr(job, "repo_path", "") or ""
    models = _models_for_job(job)
    provider_versions: dict[str, str] = {}
    if probe_versions:
        seen: set[str] = set()
        for target in models.values():
            provider = target.split("/", 1)[0]
            if provider and provider not in seen:
                seen.add(provider)
                provider_versions[provider] = probe_provider_version(provider,
                                                                     cwd=repo or None)
    rwt = remedy_worktree_identity()
    twt = worktree_identity(repo) if inspect_target else WorktreeIdentity(
        GIT_UNAVAILABLE, UNAVAILABLE, "", ("target not inspected",))
    return InputSnapshot(
        remedy_git_sha=rwt.head if _is_sha(rwt.head) else UNAVAILABLE,
        remedy_dirty=rwt.dirty,          # F4: typed tri-state, NOT bool(problems)
        remedy_worktree=rwt.to_json(),
        target_base_commit=str(getattr(job, "worktree_base_commit", "") or UNAVAILABLE),
        target_head=twt.head if _is_sha(twt.head) else UNAVAILABLE,
        target_tree=twt.digest if twt.status == GIT_OK else UNAVAILABLE,
        target_worktree=twt.to_json(),
        # F10 (round 11): NEVER a silent empty string. A value the product genuinely does not
        # have (a non-git target has no tree object) is recorded as the explicit UNAVAILABLE
        # marker, so a reader is told "there is nothing here" instead of having to guess whether
        # the field was dropped, lost, or never existed.
        job_initial_tree=str(getattr(job, "job_initial_tree", "") or "") or UNAVAILABLE,
        episode_start_workspace_tree=(
            str(getattr(job, "episode_start_workspace_tree", "") or "") or UNAVAILABLE),
        # F10/F11 (round 11): the workspace's STRICT content identity — the thing a later
        # check-only comparison can actually recompute without writing a single git object.
        episode_start_workspace_identity=_job_workspace_identity(job).to_json(),
        job_file_sha256=str(getattr(job, "job_file_sha256", "") or ""),
        job_input=build_job_input_definition(job),
        models=models,
        provider_versions=provider_versions,
        config=_config_snapshot(),
        environment=_environment_snapshot(),
        python_version=platform.python_version(),
        platform=platform.platform(),
        pythonhashseed=os.environ.get("PYTHONHASHSEED", "") or "",
    )


EPISODE_SNAPSHOT_VERSION = 1

SNAPSHOT_OK = "ok"
SNAPSHOT_FAILED = "failed"

# The capture phases an episode-start snapshot can be taken in.
PHASE_EPISODE_START = "episode_start"
PHASE_PRE_WORK_STOP = "pre_work_stop"
#: F7/F10 (round 11): a planning-only episode never acquires a workspace and never dispatches a
#: task, so its snapshot is captured in an explicit PLANNING phase. Giving it its own phase is
#: what lets the lifecycle matrix refuse "completed + planning_only" and lets the identity rules
#: ask for exactly the subset a planning-only record can honestly carry.
PHASE_PLANNING_ONLY = "planning_only"
VALID_CAPTURE_PHASES = frozenset({PHASE_EPISODE_START, PHASE_PRE_WORK_STOP,
                                  PHASE_PLANNING_ONLY})
VALID_SNAPSHOT_STATUS = frozenset({SNAPSHOT_OK, SNAPSHOT_FAILED})


@dataclass(frozen=True)
class EpisodeInputSnapshotV1:
    """F1/F11: the typed, versioned, EPISODE-OWNED input snapshot.

    Captured exactly once, at a named phase of a specific episode, and then IMMUTABLE. It is
    NOT a bare dict and NOT re-probed at episode end: the finalized manifest consumes this
    exact object. A capture FAILURE is recorded as ``status == "failed"`` with problems — it is
    never silently replaced by a terminal re-probe, and the finalizer treats a failed/foreign
    snapshot as a BLOCKING recording error (honest incomplete coverage), never fabricated
    completeness."""

    snapshot_v: int
    episode_id: str
    captured_at: str
    capture_phase: str
    status: str                          # ok | failed
    problems: tuple[str, ...]
    input: InputSnapshot | None          # the captured inputs; None only when status==failed

    def wrapper_shape_is_valid(self) -> bool:
        """F10: the WRAPPER-ONLY predicate — version/episode/phase/timestamp/status coherence.
        It says nothing about the nested input. Never use it for a trust decision."""
        return not validate_episode_input_snapshot(self)

    def is_ok(self) -> bool:
        """F10: FULLY valid — the wrapper AND its nested payload.

        A wrapper-only check is not enough: a snapshot carrying a raw secret, an unknown field
        or a broken job-input hash relation is NOT ok, and stop/retry decisions depend on this
        predicate. Includes: wrapper validation, strict InputSnapshot validation, strict
        JobInputDefinition validation, and the embedded job-input hash relation."""
        if self.status != SNAPSHOT_OK or validate_episode_input_snapshot(self):
            return False
        if self.input is None:
            return False
        if validate_input_snapshot(self.input):
            return False
        if validate_job_input_definition(self.input.job_input):
            return False
        return True

    def to_json(self) -> dict[str, Any]:
        return {
            "snapshot_v": self.snapshot_v,
            "episode_id": self.episode_id,
            "captured_at": self.captured_at,
            "capture_phase": self.capture_phase,
            "status": self.status,
            "problems": list(self.problems),
            "input": self.input.to_json() if self.input is not None else None,
        }

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "EpisodeInputSnapshotV1":
        """F14: TRUSTED in-memory data ONLY — untrusted records use
        ``decode_episode_snapshot_v1``."""
        if not isinstance(d, dict):
            raise ManifestError("an episode snapshot must be a JSON object")
        raw_input = d.get("input")
        return cls(
            snapshot_v=int(d.get("snapshot_v", 0) or 0),
            episode_id=str(d.get("episode_id", "")),
            captured_at=str(d.get("captured_at", "")),
            capture_phase=str(d.get("capture_phase", "")),
            status=str(d.get("status", SNAPSHOT_FAILED)),
            problems=tuple(str(p) for p in (d.get("problems") or [])),
            input=InputSnapshot.from_trusted_json(raw_input) if isinstance(raw_input, dict) else None,
        )


def validate_episode_input_snapshot(w: "EpisodeInputSnapshotV1", *,
                                    expected_episode_id: str = "") -> list[str]:
    """F6: the ONE strict validator for a typed episode snapshot. Returns problems (empty ==
    valid). No normalization: an unsupported version, garbage phase, contradictory ok/failed
    state, or a foreign episode id is REJECTED, never silently accepted."""
    problems: list[str] = []
    if w.snapshot_v != EPISODE_SNAPSHOT_VERSION:
        problems.append(f"unsupported snapshot_v {w.snapshot_v!r}")
    if not _safe_component(w.episode_id):
        problems.append(f"unsafe or empty snapshot episode_id {w.episode_id!r}")
    if w.capture_phase not in VALID_CAPTURE_PHASES:
        problems.append(f"invalid capture_phase {w.capture_phase!r}")
    if not w.captured_at or not _is_iso_timestamp(w.captured_at):
        problems.append(f"invalid captured_at {w.captured_at!r}")
    if w.status not in VALID_SNAPSHOT_STATUS:
        problems.append(f"invalid snapshot status {w.status!r}")
    elif w.status == SNAPSHOT_OK:
        if w.input is None:
            problems.append("status=ok but no input snapshot")
        if w.problems:
            problems.append("status=ok but problems are present")
    elif w.status == SNAPSHOT_FAILED:
        if w.input is not None:
            problems.append("status=failed but an input snapshot is present")
        if not w.problems:
            problems.append("status=failed but no problems recorded")
    if expected_episode_id and w.episode_id != expected_episode_id:
        problems.append(f"snapshot episode_id {w.episode_id!r} != expected "
                        f"{expected_episode_id!r}")
    return problems


def _is_iso_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(str(value))
        return True
    except (ValueError, TypeError):
        return False


def capture_episode_input_snapshot(job: Any, *, episode_id: str, capture_phase: str,
                                   captured_at: str | None = None,
                                   extra_problems: tuple[str, ...] = (),
                                   ) -> EpisodeInputSnapshotV1:
    """F1/F12: capture an episode's inputs ONCE, bound to that episode + phase. On failure —
    including a ``extra_problems`` failure raised by the caller (e.g. a failed episode-start
    workspace-tree capture) — this returns a ``status=="failed"`` snapshot carrying the
    reason(s), with NO input. The caller must treat that as blocking. It NEVER falls back to a
    terminal re-probe, and a partial-but-material failure never yields an ``ok`` snapshot."""
    from packages.orchestration.failure_postmortem import safe_text

    stamp = captured_at or utc_now_iso()
    extra = tuple(safe_text(p)[:400] for p in extra_problems if p)
    try:
        snap = build_input_snapshot(job, inspect_target=True)
    except Exception as exc:             # capture failure is DATA, not a swallowed None
        return EpisodeInputSnapshotV1(
            snapshot_v=EPISODE_SNAPSHOT_VERSION, episode_id=str(episode_id or ""),
            captured_at=stamp, capture_phase=str(capture_phase or ""),
            status=SNAPSHOT_FAILED,
            problems=(safe_text(f"snapshot capture failed: {type(exc).__name__}: {exc}")[:400],)
            + extra,
            input=None)
    if extra:
        # A material sub-capture failed (F12). The inputs we DID gather are not a complete,
        # trustworthy snapshot — record failure, never an ok snapshot with a missing input.
        return EpisodeInputSnapshotV1(
            snapshot_v=EPISODE_SNAPSHOT_VERSION, episode_id=str(episode_id or ""),
            captured_at=stamp, capture_phase=str(capture_phase or ""),
            status=SNAPSHOT_FAILED, problems=extra, input=None)
    return EpisodeInputSnapshotV1(
        snapshot_v=EPISODE_SNAPSHOT_VERSION, episode_id=str(episode_id or ""),
        captured_at=stamp, capture_phase=str(capture_phase or ""),
        status=SNAPSHOT_OK, problems=(), input=snap)


def _h(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _redacted_command_identity(command: str) -> dict[str, Any]:
    """A test/CLI command can carry a secret (a token in an env-style arg). Keep a
    deterministic identity that still moves when the command changes, without serializing
    the secret: the redacted text plus a hash of the RAW command."""
    return {"redacted": _safe_scalar(command or ""), "sha256": _h(command or "")}


def build_job_input_definition(job: Any) -> dict[str, Any]:
    """The COMPLETE typed job-input definition (F1): every persisted input that can change
    which work runs, how many calls run, what prompts are assembled, what tests run, or what
    provider options are used. A single opaque job-file hash is NOT enough."""
    ec = getattr(job, "execution_config", None)

    def _g(name: str, default: Any = "") -> Any:
        if ec is not None:
            return getattr(ec, name, default)
        # A job that has not run yet carries no resolved execution config: every value IS the
        # product default, so every SOURCE is "default". Recording an empty source instead would
        # make a planning-only job's own definition invalid — and the contract says a
        # planning-only job (zero calls) has a valid manifest (T0_F012).
        if name.endswith("_source"):
            return "default"
        return default

    tasks = []
    for idx, t in enumerate(getattr(job, "tasks", [])):
        tasks.append({
            "order": idx,
            "task_id": t.task_id,
            "source_heading_number": getattr(t, "source_heading_number", 0),
            "title_sha256": _h(getattr(t, "title", "") or ""),
            "body_sha256": _h(getattr(t, "body", "") or ""),
            "acceptance_sha256": _h(getattr(t, "acceptance", "") or ""),
        })

    execution = {
        "builder": _g("builder"), "builder_source": _g("builder_source"),
        "builder_model": _g("builder_model"), "builder_model_source": _g("builder_model_source"),
        "builder_effort": _g("builder_effort"), "builder_effort_source": _g("builder_effort_source"),
        "reviewer": _g("reviewer"), "reviewer_source": _g("reviewer_source"),
        "reviewer_model": _g("reviewer_model"), "reviewer_model_source": _g("reviewer_model_source"),
        "reviewer_effort": _g("reviewer_effort"), "reviewer_effort_source": _g("reviewer_effort_source"),
        "repair_provider": _g("repair_provider"), "repair_provider_source": _g("repair_provider_source"),
        "repair_model": _g("repair_model"), "repair_model_source": _g("repair_model_source"),
        "repair_effort": _g("repair_effort"), "repair_effort_source": _g("repair_effort_source"),
        "max_rounds": _g("max_rounds", 0), "max_rounds_source": _g("max_rounds_source"),
        "repair_rounds_allowed": _g("repair_rounds_allowed", 0),
        "repair_rounds_source": _g("repair_rounds_source"),
        "test_command": _redacted_command_identity(_g("test_command")),
        "test_command_source": _g("test_command_source"),
        "claude_cli_write_mode": _g("claude_cli_write_mode"),
        "claude_cli_write_mode_source": _g("claude_cli_write_mode_source"),
        "context_strategy": _g("context_strategy"),
        # F2 invocation controls — material inputs, hashed with their source.
        "timeout_sec": _g("timeout_sec", 0), "timeout_sec_source": _g("timeout_sec_source"),
        "timeout_profile": _g("timeout_profile"),
        "timeout_profile_source": _g("timeout_profile_source"),
        "max_output_chars": _g("max_output_chars", 0),
        "max_output_chars_source": _g("max_output_chars_source"),
        "stream_evidence": bool(_g("stream_evidence", False)),
        "stream_evidence_source": _g("stream_evidence_source"),
        "max_tasks": _g("max_tasks", 0), "max_tasks_source": _g("max_tasks_source"),
    }
    return {
        "job_input_v": 1,
        "job_title_sha256": _h(getattr(job, "job_title", "") or ""),
        "job_file_sha256": str(getattr(job, "job_file_sha256", "") or ""),
        "isolation_mode": str(getattr(job, "isolation_mode", "") or ""),
        "tasks": tasks,
        "execution": execution,
    }


def job_input_definition_bytes(definition: dict[str, Any]) -> bytes:
    """F6: THE canonical byte encoding of a JobInputDefinition. Every producer and every
    verifier hashes exactly these bytes — capture, manifest construction, validation, the
    current candidate, the diff, recovery and export."""
    return json.dumps(definition, sort_keys=True, ensure_ascii=False).encode("utf-8")


def job_input_definition_sha256(definition: dict[str, Any]) -> str:
    """F6: the ONE canonical hash helper. ``manifest.job_input_sha256`` MUST equal this over the
    manifest's own EMBEDDED ``snapshot.job_input`` — so the recorded hash cannot drift from the
    definition it claims to identify."""
    return hashlib.sha256(job_input_definition_bytes(definition)).hexdigest()


def job_input_sha256(job: Any, models: dict[str, str] | None = None) -> str:
    """The identity of the COMPLETE job-input definition. ``models`` is accepted for
    backward compatibility but is now derived from the definition itself."""
    return job_input_definition_sha256(build_job_input_definition(job))


_VALID_SOURCES = frozenset({"default", "persisted", "invocation", "cli", "env",
                            "project", "user", "operator_attestation"})


def validate_job_input_definition(d: Any) -> list[str]:
    """F8 (round 10): THE ONE exact rule set for an embedded JobInputDefinition.

    There is no weaker "typed" validation sitting beside a stricter raw decoder: this function
    IS the rule set, `decode_job_input_definition_v1` calls it, and `EpisodeInputSnapshotV1.is_ok`
    calls it too. A record any one of them accepts is accepted by all of them — which is the
    whole point, because a snapshot that says `is_ok()` and then fails its own strict decode on
    the way back off disk is a lie told in two voices.

    Returns EVERY problem (the decoder raises on the first).
    """
    problems: list[str] = []

    def _t(fn, *a, **kw):
        """Run one strict primitive, keeping its exact message, accumulating instead of raising."""
        try:
            return fn(*a, **kw)
        except _S.SchemaError as exc:
            problems.append(str(exc))
            return None

    d = _t(_S.req_map, d, "job_input")
    if d is None:
        return problems
    _t(_S.no_unknown_keys, d, JOB_INPUT_TOP_FIELDS, "job_input")

    v = _t(_S.req_int, d, "job_input_v", "job_input", minimum=0, maximum=1000)
    if v is not None and v != 1:
        problems.append(f"unsupported job_input_v {d.get('job_input_v')!r}")

    # F6: REQUIRED facts, not optional decoration — an empty value is not a valid definition
    # even when the recorded hash matches its bytes.
    for f in ("job_title_sha256", "job_file_sha256"):
        val = _t(_S.req_str, d, f, "job_input", max_len=64)
        if val is not None and not _is_hex64(val):
            problems.append(f"job_input.{f} is not 64 lowercase hex")

    iso = _t(_S.req_str, d, "isolation_mode", "job_input", max_len=_S.MAX_ID_LEN)
    if iso is not None and iso not in VALID_ISOLATION_MODES:
        problems.append(f"job_input.isolation_mode {iso!r} is not a supported mode")

    tasks = _t(_S.req_list, d, "tasks", "job_input", max_len=_S.MAX_TASKS)
    seen_ids: set[str] = set()
    for i, tk in enumerate(tasks or []):
        where = f"job_input.tasks[{i}]"
        e = _t(_S.req_map, tk, where)
        if e is None:
            continue
        _t(_S.no_unknown_keys, e, JOB_INPUT_TASK_FIELDS, where)
        order = _t(_S.req_int, e, "order", where, minimum=0, maximum=_S.MAX_TASKS)
        if order is not None and order != i:
            problems.append(f"{where} order is not contiguous")
        tid = _t(_S.req_str, e, "task_id", where, max_len=_S.MAX_ID_LEN)
        if tid is not None:
            if not _safe_component(tid):
                problems.append(f"{where} unsafe task_id {tid!r}")
            if tid in seen_ids:
                problems.append(f"job_input duplicate task_id {tid!r}")
            seen_ids.add(tid)
        _t(_S.req_int, e, "source_heading_number", where, minimum=0, maximum=100000)
        for f in ("title_sha256", "body_sha256", "acceptance_sha256"):
            val = _t(_S.req_str, e, f, where, max_len=64)
            if val is not None and not _is_hex64(val):
                problems.append(f"{where}.{f} is not 64 lowercase hex")

    ex_raw = _t(_S.req_key, d, "execution", "job_input")
    if ex_raw is None:
        return problems
    ex = _t(_S.req_map, ex_raw, "job_input.execution")
    if ex is None:
        return problems
    _t(_S.no_unknown_keys, ex, JOB_INPUT_EXECUTION_FIELDS, "job_input.execution")
    missing = sorted(JOB_INPUT_EXECUTION_FIELDS - set(ex))
    if missing:
        problems.append(f"job_input.execution is missing material field(s) {missing}")
    for f in JOB_INPUT_EXECUTION_STR_FIELDS:
        if f in ex:
            _t(_S.req_str, ex, f, "job_input.execution", max_len=_S.MAX_ID_LEN,
               allow_empty=True)
    for f in JOB_INPUT_EXECUTION_INT_FIELDS:
        if f in ex:
            _t(_S.req_int, ex, f, "job_input.execution", minimum=0, maximum=10_000_000)
    for f in JOB_INPUT_EXECUTION_BOOL_FIELDS:
        if f in ex:
            _t(_S.req_bool, ex, f, "job_input.execution")
    if "context_strategy" in ex:
        _t(_S.req_str, ex, "context_strategy", "job_input.execution", max_len=_S.MAX_ID_LEN,
           allow_empty=True)
    # every value carries a source from the allowed vocabulary
    for k, v in ex.items():
        if k.endswith("_source") and v not in _VALID_SOURCES:
            problems.append(f"job_input.execution.{k} has an invalid source {v!r}")

    tc_raw = ex.get("test_command")
    if tc_raw is None and "test_command" not in ex:
        return problems
    tc = _t(_S.req_map, tc_raw, "job_input.execution.test_command")
    if tc is None:
        return problems
    _t(_S.no_unknown_keys, tc, {"redacted", "sha256"}, "job_input.execution.test_command")
    sha = _t(_S.req_str, tc, "sha256", "job_input.execution.test_command", max_len=64)
    if sha is not None and not _is_hex64(sha):
        problems.append("job_input.execution.test_command.sha256 is not 64 lowercase hex")
    red = _t(_S.req_str, tc, "redacted", "job_input.execution.test_command",
             max_len=_S.MAX_VALUE_LEN, allow_empty=True)
    # F6: the test command's stored representation is its SAFE redacted identity + hash only.
    if red is not None and (_contains_secret(red) or _contains_local_path(red)
                            or _S.has_control_chars(red)):
        problems.append(
            "job_input.execution.test_command.redacted carries a raw secret/path/control char")
    return problems


# ---------------------------------------------------------------------------
# Call collection + coverage (F10)
# ---------------------------------------------------------------------------


#: F6 (round 10): the EXACT per-task call-expectation vocabulary.
#:
#: `executed`       — THIS episode dispatched the task, so at least one finalized call must exist.
#: `prior_episode`  — the task's work happened in an EARLIER episode of the same job; this episode
#:                    legitimately publishes none of its calls.
#: `dispatched_no_calls` — the task was dispatched but ended before its first provider call could
#:                    be finalized (a failed/blocked task). Zero calls is the honest record.
#: `skipped`        — explicitly skipped; zero calls expected.
#: `not_dispatched` — never reached (pre-work stop, planning-only, or the max-tasks boundary).
EXPECT_EXECUTED = "executed"
EXPECT_PRIOR_EPISODE = "prior_episode"
EXPECT_DISPATCHED_NO_CALLS = "dispatched_no_calls"
EXPECT_SKIPPED = "skipped"
EXPECT_NOT_DISPATCHED = "not_dispatched"
#: F4 (round 12): the task ended failed/blocked BEFORE it ever owned a run. Distinct from
#: `dispatched_no_calls` (a run exists and recorded nothing) and from `not_dispatched` (never
#: reached at all) — three different truths that used to share one word.
EXPECT_FAILED_PRE_DISPATCH = "failed_pre_dispatch"
VALID_TASK_EXPECTATIONS = frozenset({
    EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE, EXPECT_DISPATCHED_NO_CALLS, EXPECT_SKIPPED,
    EXPECT_NOT_DISPATCHED, EXPECT_FAILED_PRE_DISPATCH})

#: F2 (round 16): THE closed task-status/expectation truth table.
#:
#: The expectation says what this episode owed the task; `task_status_at_finalization` says what
#: the JobPlan recorded about it. Round 12 stored both — deliberately, so a contradiction stays
#: VISIBLE instead of being normalized away — but nothing ever compared them, so a published
#: reference could say "this task was skipped" while recording that it was applied to the job
#: workspace. Reproduced: all four of `skipped` + {pending, applied_to_job_workspace, passed,
#: failed} validated and round-tripped through the writer.
#:
#: Derived from `_collect_calls`'s real behaviour, not from taste:
#:
#: * `skipped` is decided BEFORE dispatch, so it is the one expectation pinned to a single
#:   status. A skipped task owns no run and no ledger (F012's own table: "a skipped task owning
#:   a run is an integrity problem").
#: * `not_dispatched` means the task was never reached — pending, with no run.
#: * `failed_pre_dispatch` means it died before owning a run: failed or blocked only.
#: * `executed`/`prior_episode` need a run. `pending` is legitimate there — F011's mid-flight
#:   stop lets the in-flight call finish while the task returns to pending for the resume — and
#:   so are `failed`/`blocked`, which production reaches AFTER a successful run when the
#:   completion gate, the target guard or the workspace apply refuses the work.
#: * `dispatched_no_calls` means a run exists that finalized nothing, so the task cannot be
#:   `passed`/`applied`: those two are only reachable through a finalized call.
_TASK_EXPECTATION_ALLOWED_STATUSES = {
    EXPECT_SKIPPED: frozenset({"skipped"}),
    EXPECT_NOT_DISPATCHED: frozenset({"pending"}),
    EXPECT_FAILED_PRE_DISPATCH: frozenset({"failed", "blocked"}),
    EXPECT_EXECUTED: frozenset({"passed", "applied_to_job_workspace", "running", "pending",
                                "failed", "blocked"}),
    EXPECT_PRIOR_EPISODE: frozenset({"passed", "applied_to_job_workspace", "running", "pending",
                                     "failed", "blocked"}),
    EXPECT_DISPATCHED_NO_CALLS: frozenset({"failed", "blocked", "pending", "running"}),
}

#: F1 (round 17): the CONTEXT-TIGHTENED status sets. The table above is the STOPPED/worked
#: baseline — the widest an expectation is ever allowed, because a stop can legitimately leave a
#: run pending (F011's mid-flight call finishes) or blocked/failed (a post-run gate). A COMPLETED
#: episode is narrower: `run_job` sets `completed` only when EVERY task is applied or skipped
#: (`all(t.status in (TASK_APPLIED, TASK_SKIPPED))`), so an `executed` or `prior_episode` task in
#: one CANNOT be pending/running/failed/blocked — that would contradict the status it is published
#: under. The shared validator took `episode_status`/`episode_phase` since round 16 and never read
#: them, so a completed reference accepted `executed` + pending/running/failed/blocked.
_COMPLETED_WORKED_STATUSES = {
    EXPECT_EXECUTED: frozenset({"passed", "applied_to_job_workspace"}),
    EXPECT_PRIOR_EPISODE: frozenset({"passed", "applied_to_job_workspace"}),
    EXPECT_SKIPPED: frozenset({"skipped"}),
}


def _allowed_statuses_for(expectation: str, episode_status: str,
                          episode_phase: str) -> frozenset:
    """The statuses an expectation may carry IN THIS episode context.

    A completed/worked episode uses the tight set (its tasks are all applied or skipped); every
    other context uses the permissive baseline, which the per-context `_LIFECYCLE_MATRIX` already
    restricts to the expectations that context permits at all.
    """
    if episode_status == "completed" and episode_phase == PHASE_WORKED:
        tight = _COMPLETED_WORKED_STATUSES.get(expectation)
        if tight is not None:
            return tight
    return _TASK_EXPECTATION_ALLOWED_STATUSES[expectation]


#: Every task status the JobPlan can persist. A status outside this set is a forged record.
VALID_TASK_STATUSES = frozenset({"pending", "running", "passed", "applied_to_job_workspace",
                                 "blocked", "failed", "skipped"})

#: The expectations that mean "no run was ever dispatched for this task".
_EXPECTATIONS_WITHOUT_RUN = frozenset({EXPECT_SKIPPED, EXPECT_NOT_DISPATCHED,
                                       EXPECT_FAILED_PRE_DISPATCH})


def validate_task_expectation_truth(te: "TaskCallExpectationV1", *, episode_status: str = "",
                                    episode_phase: str = "") -> list[str]:
    """ONE closed truth table binding a task's expectation, its persisted status and its dispatch.

    Used by typed manifest validation, the strict decoder, CallExpectation validation, the task
    history chain, the writer's preflight and postcondition, the canonical loader, recovery and
    the Evidence export — so no boundary can be reached by a record another boundary would refuse.

    No status is ever normalized into a different expectation: a disagreement is REPORTED, with
    both persisted facts intact, exactly as round 12 intended when it started storing both.
    """
    problems: list[str] = []
    exp = te.expectation
    status = te.task_status_at_finalization

    if exp not in VALID_TASK_EXPECTATIONS:
        problems.append(f"task {te.task_id!r} has an unsupported expectation {exp!r}")
        return problems
    if not status:
        problems.append(
            f"task {te.task_id!r} records no task_status_at_finalization, so its expectation "
            f"{exp!r} cannot be checked against what the JobPlan actually said")
        return problems
    if status not in VALID_TASK_STATUSES:
        problems.append(f"task {te.task_id!r} records an unsupported task status {status!r}")
        return problems

    # F1 (round 17): the allowed set depends on the EPISODE this record lives in. A completed
    # episode's tasks are all applied or skipped, so an executed task in one cannot be
    # pending/running/failed/blocked; a stopped episode legitimately can be.
    allowed = _allowed_statuses_for(exp, episode_status, episode_phase)
    if status not in allowed:
        ctx = (f"a {episode_status}/{episode_phase} episode's " if episode_status else "a ")
        problems.append(
            f"impossible task record: task {te.task_id!r} is {exp!r} but the JobPlan recorded it "
            f"as {status!r} at finalization ({ctx}{exp!r} task can only be "
            f"{'/'.join(sorted(allowed))})")

    # The dispatch state and the run must agree with the expectation's own meaning.
    if exp in _EXPECTATIONS_WITHOUT_RUN:
        if te.run_id:
            problems.append(
                f"impossible task record: task {te.task_id!r} is {exp!r}, which is decided before "
                f"dispatch, but it names run {te.run_id!r}")
        if te.ledger_ref or te.finalized_calls_sha256:
            problems.append(
                f"impossible task record: task {te.task_id!r} is {exp!r} but seals a call ledger")
        if te.dispatch_state != DISPATCH_NEVER:
            problems.append(
                f"impossible task record: task {te.task_id!r} is {exp!r} but its dispatch state "
                f"is {te.dispatch_state!r}")
    else:
        if te.dispatch_state == DISPATCH_NEVER:
            problems.append(
                f"impossible task record: task {te.task_id!r} is {exp!r}, which requires a run, "
                f"but its dispatch state says it was never dispatched")

    if exp == EXPECT_PRIOR_EPISODE and te.dispatch_state == DISPATCH_THIS_EPISODE:
        problems.append(
            f"impossible task record: task {te.task_id!r} is {EXPECT_PRIOR_EPISODE!r} but its "
            f"dispatch state says this episode dispatched it")
    if exp == EXPECT_EXECUTED and te.dispatch_state == DISPATCH_PRIOR_EPISODE:
        problems.append(
            f"impossible task record: task {te.task_id!r} is {EXPECT_EXECUTED!r} but its "
            f"dispatch state says a prior episode dispatched it")
    return problems

#: The episode-level phase that explains a zero-call episode WITHOUT consulting the JobPlan.
PHASE_WORKED = "worked"
PHASE_PRE_WORK_STOP = "pre_work_stop"
PHASE_PLANNING_ONLY = "planning_only"
VALID_EPISODE_PHASES = frozenset({PHASE_WORKED, PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY})


#: F1: the CONTEXT a manifest is validated in. The same record is judged differently depending
#: on what it claims to be — this replaces the old "the Evidence layer will catch it" split.
#: (Declared here because the ledger contract below is mode-aware, and a default argument is
#: bound when the function is DEFINED, not when it is called.)
MODE_PREPUBLICATION = "prepublication"        # in-memory, artifacts not yet bound
MODE_PUBLISHED_REFERENCE = "published_reference"   # a stored terminal record we must trust
MODE_CURRENT_CANDIDATE = "current_candidate"      # the would-be inputs, may be incomplete


#: F1 (round 12): a run's terminal state, as the ledger records it.
LEDGER_TERMINAL_STATES = frozenset({"completed", "stopped", "failed", "blocked", "skipped"})

#: F2 (round 13): the persisted RUN's own terminal vocabulary, mapped onto the ledger's.
#:
#: The ledger describes a RUN, so its terminal state is the RUN's fact and must be read from the
#: run record. It used to be derived from the surrounding TASK's status, which is a different
#: thing that moves for its own reasons: a run can finish `staged_review_passed` and the task
#: still end `blocked` because the completion gate, the target guard or the workspace apply
#: refused it AFTERWARDS. Asking the task what the run did was asking the wrong witness.
#:
#: CLOSED on purpose: an unrecognised final_status is a recorded problem, never a default. A
#: `.get(..., "stopped")` is how an unknown outcome silently became a plausible one.
RUN_FINAL_STATUS_TO_LEDGER_STATE = {
    "staged_review_passed": "completed",
    "builder_no_changes": "completed",     # recognised by pingpong_evidence as a clean pass
    "stopped": "stopped",                  # F011
    "staged_blocked": "blocked",
    "target_mutation_blocked": "blocked",
    "review_failed": "failed",
    "review_inconsistent": "failed",
    "test_failed": "failed",
    "max_rounds_reached": "failed",
    "repair_exhausted": "failed",
    "provider_unavailable": "failed",
    "context_error": "failed",
    "run_error": "failed",
}

#: F2 (round 13): the TASK statuses that constrain what the run can have done.
#:
#: Deliberately narrow, because the reverse is not true. A task only reaches `passed`/`applied`
#: AFTER its run returned a successful result, so those two DO pin the ledger to `completed`.
#: `blocked`/`failed`/`pending`/`running` pin nothing — every one of them is reachable with a
#: successful run (post-run gates) or an unsuccessful one, and pretending otherwise would refuse
#: real production records. `skipped` may own no ledger at all: skipping happens before dispatch.
_TASK_STATUS_REQUIRES_LEDGER_STATE = {
    "passed": frozenset({"completed"}),
    "applied_to_job_workspace": frozenset({"completed"}),
}
_TASK_STATUS_FORBIDS_LEDGER = frozenset({"skipped"})

#: F6 (round 13): bounds for a ledger entry's numbers. A ledger is Evidence, and Evidence with an
#: unbounded integer in it is a denial-of-service surface and a nonsense record at once.
MAX_LEDGER_ROUND = 10_000
MAX_LEDGER_SEQUENCE = 10_000


@dataclass(frozen=True)
class CallLedgerEntryV1:
    """ONE finalized call, exactly as the run recorded it."""
    per_run_sequence: int
    call_id: str
    episode_id: str
    role: str
    round: int
    kind: str
    prepared_input_fingerprint: str
    ok: bool

    def to_json(self) -> dict[str, Any]:
        return {"per_run_sequence": self.per_run_sequence, "call_id": self.call_id,
                "episode_id": self.episode_id, "role": self.role, "round": self.round,
                "kind": self.kind,
                "prepared_input_fingerprint": self.prepared_input_fingerprint, "ok": self.ok}


@dataclass(frozen=True)
class RunCallLedgerV1:
    """F1 (round 12): the CANONICAL, immutable account of every call one run finalized.

    `CallExpectationV1` used to carry a count and a sha256 of the mutable Run JSON's
    `finalized_calls` list. Neither was in the verified tree, so a stored reference could drop a
    call, restate the count, put any 64-hex string in the hash field, and validate — reproduced
    exactly. A number that only agrees with itself is not evidence.

    The ledger is therefore an artifact like any other: canonical bytes, in the episode's exact
    allowlist, hash-bound from the manifest, verified by the loader, recovery and the export. It
    is also the sequence F140's replay needs ("serves stream N for call N", keyed by call
    sequence), which is why the per-run order is recorded rather than derived.
    """
    job_id: str
    task_id: str
    run_id: str
    terminal_state: str
    complete: bool
    entries: tuple[CallLedgerEntryV1, ...] = ()
    ledger_v: int = 1

    def to_json(self) -> dict[str, Any]:
        return {"ledger_v": self.ledger_v, "job_id": self.job_id, "task_id": self.task_id,
                "run_id": self.run_id, "terminal_state": self.terminal_state,
                "complete": self.complete,
                "entries": [e.to_json() for e in self.entries]}

    def canonical_bytes(self) -> bytes:
        return _fs.json_bytes(self.to_json(), sort_keys=True)

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def ref(self) -> str:
        return canonical_ledger_ref(self.task_id, self.run_id)


def ledger_identity_bytes(task_id: str, run_id: str) -> bytes:
    """The UNAMBIGUOUS canonical encoding of a ledger's identity.

    Unambiguous is the whole point: the identity is two independent strings, and any encoding
    that merely concatenates them with a separator is ambiguous whenever the separator can occur
    inside either one. Canonical JSON is length-delimited by construction (the quotes and the key
    names bound each field), so exactly one (task_id, run_id) pair can produce these bytes.
    """
    return _fs.json_bytes({"task_id": str(task_id), "run_id": str(run_id)}, sort_keys=True)


def canonical_ledger_ref(task_id: str, run_id: str) -> str:
    """THE ledger artifact ref — one helper, used by the writer, the readers and the validators.

    F3 (round 14): this used to be `call_ledgers/{task_id}-{run_id}.json`, which is ambiguous
    because `-` is legal inside both ids. Reproduced: `("a-b", "c")` and `("a", "b-c")` — both
    passing the safe-component schema — mapped to the SAME `call_ledgers/a-b-c.json`, and a
    crafted tree with two declared ledgers backed by ONE physical file was accepted, because the
    anchored reader built a dict keyed by filename and silently overwrote one declaration.

    The ref is now the sha256 of the unambiguous identity encoding: deterministic, recomputable
    from the ledger's own identity, collision-free, and 69 bytes — far below NAME_MAX (255)
    whatever the ids are, so the maximum legal task/run ids still produce a legal filename.

    No compatibility layer: F012 is unmerged, so no accepted record uses the old shape.
    """
    digest = hashlib.sha256(ledger_identity_bytes(task_id, run_id)).hexdigest()
    return f"{LEDGERS_SUBDIR}/{digest}.json"


def decode_run_call_ledger_v1(raw: Any) -> "RunCallLedgerV1":
    """F1: THE strict decoder for a stored ledger — exact schema, real types, no unknown field."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            _S.bounded_bytes(bytes(raw), _S.MAX_CALL_ARTIFACT_BYTES, "call ledger")
            raw = strict_json_loads(bytes(raw), where="call ledger")
        except _S.SchemaError as exc:
            raise ManifestError(f"call ledger: {exc}") from None
    d = _S.req_map(raw, "call_ledger")
    _S.no_unknown_keys(d, {"ledger_v", "job_id", "task_id", "run_id", "terminal_state",
                           "complete", "entries"}, "call_ledger")
    if _S.req_int(d, "ledger_v", "call_ledger", minimum=0, maximum=1000) != 1:
        raise _S.SchemaError(f"unsupported ledger_v {d.get('ledger_v')!r}")
    state = _S.req_str(d, "terminal_state", "call_ledger", max_len=_S.MAX_ID_LEN)
    if state not in LEDGER_TERMINAL_STATES:
        raise _S.SchemaError(f"call_ledger.terminal_state {state!r} is not a supported state")
    raw_entries = _S.req_list(d, "entries", "call_ledger", max_len=_S.MAX_CALLS_PER_EPISODE)
    entries: list[CallLedgerEntryV1] = []
    for i, e in enumerate(raw_entries):
        where = f"call_ledger.entries[{i}]"
        m = _S.req_map(e, where)
        _S.no_unknown_keys(m, {"per_run_sequence", "call_id", "episode_id", "role", "round",
                               "kind", "prepared_input_fingerprint", "ok"}, where)
        entries.append(CallLedgerEntryV1(
            per_run_sequence=_S.req_int(m, "per_run_sequence", where, minimum=1,
                                        maximum=_S.MAX_CALLS_PER_EPISODE),
            call_id=_S.req_str(m, "call_id", where, max_len=_S.MAX_ID_LEN),
            episode_id=_S.req_str(m, "episode_id", where, max_len=_S.MAX_ID_LEN),
            role=_S.req_str(m, "role", where, max_len=_S.MAX_ID_LEN),
            round=_S.req_int(m, "round", where, minimum=1, maximum=10_000),
            kind=_S.req_str(m, "kind", where, max_len=_S.MAX_ID_LEN),
            prepared_input_fingerprint=_S.req_str(m, "prepared_input_fingerprint", where,
                                                  max_len=64),
            ok=_S.req_bool(m, "ok", where)))
    return RunCallLedgerV1(
        job_id=_S.req_str(d, "job_id", "call_ledger", max_len=_S.MAX_ID_LEN),
        task_id=_S.req_str(d, "task_id", "call_ledger", max_len=_S.MAX_ID_LEN),
        run_id=_S.req_str(d, "run_id", "call_ledger", max_len=_S.MAX_ID_LEN),
        terminal_state=state, complete=_S.req_bool(d, "complete", "call_ledger"),
        entries=tuple(entries))


def validate_run_call_ledger(ledger: "RunCallLedgerV1", *,
                             mode: str = MODE_PUBLISHED_REFERENCE) -> list[str]:
    """The ledger's OWN coherence — the innermost layer of the one closed ledger contract (F8).

    F1 (round 13) — COMPLETENESS. `complete` was written but never read, so a ledger could say
    "this is a partial account of the run" and still be sealed into a published terminal
    reference as if it were the whole story. A published completed/stopped Episode is the record
    of what happened; a partial account of a run inside it is a contradiction, not a caveat. A
    PRE-publication candidate may legitimately still be filling up — that path says so explicitly
    and must report incomplete Call coverage rather than pass as determinism.

    F6 (round 13) — IDENTITY SAFETY. Entry ids were unchecked, so `call_id =
    "/home/alice/SUPERSECRET"` validated and its bytes went into the canonical record and out
    through the export. Ledger entries carry the same identity rules as every other stored F012
    identity, through the same established scanners — not a weaker local rule.
    """
    problems: list[str] = []
    for f in ("job_id", "task_id", "run_id"):
        if not _safe_component(str(getattr(ledger, f, "") or "")):
            problems.append(f"call ledger {f} is not a safe bounded component")
    if ledger.terminal_state not in LEDGER_TERMINAL_STATES:
        problems.append(f"call ledger terminal_state {ledger.terminal_state!r} is unsupported")
    if not isinstance(ledger.complete, bool):
        problems.append("call ledger 'complete' is not a boolean")
    elif not ledger.complete and mode == MODE_PUBLISHED_REFERENCE:
        # F1: the whole point. An incomplete account cannot be published as the record.
        problems.append(
            f"call ledger {ledger.task_id}/{ledger.run_id} is marked incomplete, so it cannot "
            f"be a published reference's account of that run")
    seqs = [e.per_run_sequence for e in ledger.entries]
    if seqs != list(range(1, len(seqs) + 1)):
        problems.append(f"call ledger per-run sequence is not contiguous 1..N: {seqs}")
    ids = [e.call_id for e in ledger.entries]
    if len(set(ids)) != len(ids):
        problems.append("call ledger lists a call id more than once")
    for e in ledger.entries:
        # F6: identities first — an unsafe id must never be reported only as a "mismatch".
        #
        # The two ids answer DIFFERENT questions, so they get their own established rules: a
        # call_id is a path-shaped REF under the closed canonical grammar (F4, round 14 — the
        # SAME validator the CallIdentity uses, held to this entry's own role/round/kind, so a
        # ref can never be legal in one place and not the other, and the grammar carries the
        # secret/path scanners); an episode_id is a single COMPONENT.
        problems.extend(validate_call_ref(str(e.call_id or ""), role=e.role, round=e.round,
                                          kind=e.kind, where="call ledger entry"))
        if not _safe_component(str(e.episode_id or "")):
            problems.append(
                f"call ledger entry episode_id {str(e.episode_id)[:40]!r} is not a safe bounded "
                f"component")
        if _contains_secret(str(e.episode_id or "")) or _contains_local_path(
                str(e.episode_id or "")):
            problems.append("call ledger entry episode_id carries a raw secret or local path")
        if e.role not in VALID_CALL_ROLES:
            problems.append(f"call ledger entry {e.call_id} has role {e.role!r}")
        if e.kind not in VALID_CALL_KINDS:
            problems.append(f"call ledger entry {e.call_id} has kind {e.kind!r}")
        if not _is_hex64(e.prepared_input_fingerprint):
            problems.append(f"call ledger entry {e.call_id} fingerprint is not 64 lowercase hex")
        if not isinstance(e.ok, bool):
            problems.append(f"call ledger entry {e.call_id} 'ok' is not a boolean")
        if not isinstance(e.round, int) or isinstance(e.round, bool) or not (
                1 <= e.round <= MAX_LEDGER_ROUND):
            problems.append(f"call ledger entry {e.call_id} round is out of bounds")
        if not isinstance(e.per_run_sequence, int) or isinstance(e.per_run_sequence, bool) or not (
                1 <= e.per_run_sequence <= MAX_LEDGER_SEQUENCE):
            problems.append(f"call ledger entry {e.call_id} per_run_sequence is out of bounds")
    return problems


#: F4 (round 12): what the persisted JobPlan said about this task when the episode finalized, and
#: whether it was ever dispatched. Recording BOTH is what makes a contradiction visible: a task
#: cannot be "never dispatched" and the owner of a run at the same time, and erasing the run id to
#: make the expectation look tidy is how that contradiction used to disappear.
DISPATCH_NEVER = "never_dispatched"
DISPATCH_THIS_EPISODE = "dispatched_this_episode"
DISPATCH_PRIOR_EPISODE = "dispatched_prior_episode"
VALID_DISPATCH_STATES = frozenset({DISPATCH_NEVER, DISPATCH_THIS_EPISODE,
                                   DISPATCH_PRIOR_EPISODE})


@dataclass(frozen=True)
class TaskCallExpectationV1:
    """What THIS episode expected of ONE task, recorded at finalization.

    F9 (round 11): the counts are EXACT, not a floor, and the record binds the run it is talking
    about. F1/F4 (round 12): it also names the canonical LEDGER artifact those counts came from,
    and the task's persisted status/dispatch state, so a contradictory JobPlan is an integrity
    problem rather than something the collector quietly normalizes away.
    """
    task_id: str
    expectation: str
    run_id: str = ""
    #: The exact number of calls this episode owed for this task.
    expected_call_count: int = 0
    #: The exact number the manifest actually carries for it.
    observed_call_count: int = 0
    #: sha256 over the CANONICAL LEDGER ARTIFACT ("" when the task has no run).
    finalized_calls_sha256: str = ""
    #: The episode-relative ref of that ledger artifact ("" when the task has no run).
    ledger_ref: str = ""
    #: F4: the persisted JobPlan facts this expectation was derived from.
    task_status_at_finalization: str = ""
    dispatch_state: str = DISPATCH_NEVER

    def to_json(self) -> dict[str, Any]:
        return {"task_id": self.task_id, "expectation": self.expectation,
                "run_id": self.run_id,
                "expected_call_count": self.expected_call_count,
                "observed_call_count": self.observed_call_count,
                "finalized_calls_sha256": self.finalized_calls_sha256,
                "ledger_ref": self.ledger_ref,
                "task_status_at_finalization": self.task_status_at_finalization,
                "dispatch_state": self.dispatch_state}


@dataclass(frozen=True)
class CallExpectationV1:
    """F6 (round 10): the SELF-CONTAINED proof of how many calls this episode expected.

    Zero recorded calls means two very different things — "this job genuinely had no work to do"
    and "the calls went missing" — and a manifest that cannot tell them apart is not evidence.
    So the expectation is decided at FINALIZATION, while the JobPlan and the run records are
    still in hand, and is written INTO the episode record. Later verification reads the proof out
    of the manifest itself and never has to trust a mutable JobPlan that may since have moved on.

    A published terminal reference may claim zero calls only when this record says zero were
    expected.
    """
    episode_phase: str = PHASE_WORKED
    tasks: tuple[TaskCallExpectationV1, ...] = ()
    expectation_v: int = 1

    def expected_total_min_calls(self) -> int:
        return sum(t.expected_call_count for t in self.tasks)

    def expects_zero_calls(self) -> bool:
        return self.expected_total_min_calls() == 0

    def to_json(self) -> dict[str, Any]:
        return {"expectation_v": self.expectation_v, "episode_phase": self.episode_phase,
                "tasks": [t.to_json() for t in self.tasks]}


@dataclass(frozen=True)
class CallCoverage:
    status: str                        # complete | incomplete
    problems: tuple[str, ...] = ()

    def to_json(self) -> dict[str, Any]:
        return {"status": self.status, "problems": list(self.problems)}


def _finalized_calls_seal(entries: Any) -> str:
    """F9 (round 11): a seal over a run's COMPLETE finalized-call ledger.

    The manifest records how many calls it expected of a run. Without naming WHICH ledger it
    counted, that number can only ever agree with itself. The seal is the ledger's identity:
    canonical bytes of the exact list read at finalization, hashed.
    """
    try:
        return hashlib.sha256(_fs.json_bytes(entries, sort_keys=True)).hexdigest()
    except Exception:
        return ""


def _ledger_entry(ident: CallIdentity, fc: FinalizedCall) -> "CallLedgerEntryV1":
    """One verified finalized call, as the run's ledger records it (its STORED per-run position,
    never the manifest's derived job-wide one)."""
    return CallLedgerEntryV1(
        per_run_sequence=ident.sequence, call_id=ident.call_id, episode_id=ident.episode_id,
        role=ident.role, round=ident.round, kind=ident.kind,
        prepared_input_fingerprint=fc.fingerprint, ok=fc.ok)


def _build_run_ledger(job_id: str, task_id: str, run_id: str, run: dict,
                      entries: list["CallLedgerEntryV1"]) -> tuple["RunCallLedgerV1", list[str]]:
    """F2 (round 13): the ledger describes a RUN, so it is built from the RUN's own record.

    It used to be built from the surrounding TASK's status (`_LEDGER_STATE_OF[task_status]`, with
    a `"stopped"` default for anything unrecognised). That asked the wrong witness: a run can
    finish `staged_review_passed` while its task ends `blocked` because a post-run gate refused
    it, and an unknown status quietly became "stopped". The run's `final_status` is the fact.

    A run with no terminal state yet cannot be sealed as a complete account — it is returned
    INCOMPLETE with the reason, which a published reference then refuses (F1).
    """
    state, problems = _ledger_state_for_run(run, where=f"task {task_id} run {run_id}")
    return RunCallLedgerV1(
        job_id=job_id, task_id=task_id, run_id=run_id,
        terminal_state=state or "stopped",
        complete=not problems, entries=tuple(entries)), problems


def _collect_calls(job: Any, owned_episode_id: str = "",
                   manifest_episode_id: str = "", *,
                   declared_task_ids: tuple[str, ...] = (),
                   prior_episode_ordinals: dict[str, int] | None = None,
                   prior_episode_ids: tuple[str, ...] = (),
                   episode_ordinal: int = 1,
                   episode_phase: str = PHASE_WORKED,
                   ) -> tuple[list[FinalizedCall], list[str], CallExpectationV1]:
    """Gather this EPISODE's finalized calls, VERIFYING their lineage — never normalizing it.

    F5: a persisted call is untrusted disk state, and its identity is checked AGAINST its
    containers rather than rewritten to agree with them:

    * the stored ``sequence`` is PER-RUN (each task's run numbers its own calls from 1 — that
      is the real recorded fact). It must equal its expected position WITHIN its run; a
      tampered sequence is a problem, never silently RENUMBERED into looking correct. Only a
      call whose stored sequence VERIFIES receives the manifest's derived job-wide position
      (the manifest presents one contiguous order across tasks);
    * ``job_id`` must equal the JobPlan's job id;
    * ``task_id`` must equal the owning TaskEntry's task id, and must appear exactly once in the
      EMBEDDED job-input definition (F7, round 10 — the immutable snapshot, not live state);
    * ``run_id`` must equal the containing persisted run's id;
    * role/kind/round and the PreparedCallInput must be strictly valid.

    F5 (round 10) — EPISODE MEMBERSHIP IS PROVEN, NOT ASSUMED. A call may be excluded as prior
    history ONLY when its episode is a KNOWN member of the canonical chain, has a strictly lower
    ordinal, and appears in THIS episode's exact ``prior_episode_ids``. An unknown, future or
    unindexed episode id is a BLOCKING coverage problem: "I do not recognise this episode" is
    never a reason to quietly drop a call and then report complete coverage.

    A legitimately excluded prior call STILL occupies its position in its run's sequence, because
    the stored per-run numbering counts every call the run made — across episodes.

    F6 (round 10): the returned ``CallExpectationV1`` is the self-contained proof of how many
    calls this episode expected, decided HERE, while the JobPlan and run records are in hand.
    """
    from packages.orchestration.pingpong_loop import load_run
    from packages.orchestration.pingpong_job import (
        TASK_APPLIED, TASK_BLOCKED, TASK_FAILED, TASK_PASSED, TASK_PENDING, TASK_RUNNING,
        TASK_SKIPPED,
    )

    #: Statuses that PROVE this task reached at least one finalized provider call. A failed or
    #: blocked task may honestly have none (it can die before its first call), so it is recorded
    #: as `dispatched_no_calls` rather than forced to invent one.
    REQUIRE_CALL_STATUSES = {TASK_PASSED, TASK_APPLIED, TASK_RUNNING}

    calls: list[FinalizedCall] = []
    problems: list[str] = []
    expectations: list[TaskCallExpectationV1] = []
    ledgers: list[RunCallLedgerV1] = []
    job_id = str(getattr(job, "job_id", "") or "")
    priors = dict(prior_episode_ordinals or {})
    prior_set = set(prior_episode_ids)
    #: The episode these calls must belong to. Never empty: an unowned collection would adopt
    #: whatever it found (F6, round 11).
    owns = str(owned_episode_id or manifest_episode_id or "")
    if not owns:
        raise ManifestError(
            "cannot collect calls without an owning episode id (F6: ownership is never assumed)")
    # F7: the task ids the EMBEDDED job-input definition declares (each exactly once). The live
    # `job.tasks` list is mutable and may have moved on since capture; the definition is the
    # immutable record of what this episode was actually given.
    declared = list(declared_task_ids) or [
        str(getattr(tk, "task_id", "") or "") for tk in getattr(job, "tasks", [])]
    seq = 0                       # the manifest's derived job-wide position
    seen_seq: set[tuple] = set()
    seen_logical: set[tuple] = set()

    for t in getattr(job, "tasks", []):
        task_id = str(getattr(t, "task_id", "") or "")
        status = str(getattr(t, "status", "") or "")
        run_id = getattr(t, "run_id", "") or ""
        must_have_calls = status in REQUIRE_CALL_STATUSES
        observed_here = 0
        observed_prior = 0

        if not run_id:
            # F6: a task whose status says it ran, but which carries no run to point at, is
            # MISSING evidence — not a zero-call task. Publishing it as "complete" would be the
            # manifest certifying its own blind spot.
            if must_have_calls:
                problems.append(
                    f"task {task_id} is {status!r} but has no run id, so its calls cannot be "
                    f"accounted for")
                expectations.append(TaskCallExpectationV1(
                    task_id=task_id, expectation=EXPECT_EXECUTED, run_id="",
                    expected_call_count=1, task_status_at_finalization=status,
                    dispatch_state=DISPATCH_THIS_EPISODE))
            elif status in (TASK_FAILED, TASK_BLOCKED):
                # F4 (round 12): failed/blocked with NO run is its own truth — the task never
                # reached dispatch. Calling it "not dispatched" would lose the failure; calling
                # it "dispatched_no_calls" would invent a run that never existed.
                expectations.append(TaskCallExpectationV1(
                    task_id=task_id, expectation=EXPECT_FAILED_PRE_DISPATCH, run_id="",
                    task_status_at_finalization=status, dispatch_state=DISPATCH_NEVER))
            else:
                expectations.append(TaskCallExpectationV1(
                    task_id=task_id,
                    expectation=(EXPECT_SKIPPED if status == TASK_SKIPPED
                                 else EXPECT_NOT_DISPATCHED),
                    run_id="", task_status_at_finalization=status,
                    dispatch_state=DISPATCH_NEVER))
            continue

        # F4 (round 12): the task OWNS a run, so it WAS dispatched — whatever its status says.
        # The run id is never dropped to make the expectation look tidy, and the expectation is
        # never `skipped`/`not_dispatched` while a run exists: the run is the proof of dispatch.
        #
        # `pending` + a run is NOT a contradiction: F011's mid-flight stop ("the call in flight
        # finishes, nothing new starts") legitimately leaves the task pending for the resume while
        # its run holds the finalized call. `skipped` + a run IS one — skipping happens before
        # dispatch, so a skipped task cannot own a run.
        if status == TASK_SKIPPED:
            problems.append(
                f"task {task_id} is {status!r} but owns run {run_id!r}: a skipped task is never "
                f"dispatched, so it cannot own a run")

        run_seq = 0               # the VERIFIED per-run position
        ledger_entries: list[CallLedgerEntryV1] = []
        run = load_run(run_id)
        if run is None:
            problems.append(f"missing run record for task {task_id} (run {run_id})")
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_EXECUTED, run_id=run_id,
                expected_call_count=1 if must_have_calls else 0))
            continue
        entries = run.get("finalized_calls")
        if entries is None:
            # F9: the ledger FIELD is the run's account of its own calls. Its absence is not
            # "zero calls" — it is the account missing.
            problems.append(f"task {task_id} run has no finalized_calls field")
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_EXECUTED, run_id=run_id,
                expected_call_count=1 if must_have_calls else 0))
            continue

        for entry in entries:
            try:
                # A persisted run record is UNTRUSTED disk state — strict-decode it. A wrong
                # JSON type, an unknown field or a malformed PreparedCallInput is a recorded
                # coverage PROBLEM, never normalized into a valid manifest.
                fc = decode_finalized_call_v1(entry)
            except (_S.SchemaError, ManifestError) as exc:
                problems.append(
                    f"invalid finalized-call record in task {task_id}: {str(exc)[:160]}")
                continue

            ident = fc.identity
            call_ep = ident.episode_id or ""

            # F5: LINEAGE FIRST — everything except episode membership. A call must verify
            # before it is allowed to be excluded as prior history; otherwise "it belongs to
            # another episode" becomes a way to launder a malformed record.
            lineage: list[str] = []
            if job_id and ident.job_id != job_id:
                lineage.append(f"job_id {ident.job_id!r} != job {job_id!r}")
            if ident.task_id != task_id:
                lineage.append(f"task_id {ident.task_id!r} != owning task {task_id!r}")
            if ident.run_id != run_id:
                lineage.append(f"run_id {ident.run_id!r} != containing run {run_id!r}")
            if declared.count(ident.task_id) != 1:
                lineage.append(f"task_id {ident.task_id!r} is not declared exactly once in the "
                               f"job input definition")
            # The stored sequence is the call's position WITHIN ITS RUN — verify it there.
            expected_in_run = run_seq + 1
            if ident.sequence != expected_in_run:
                lineage.append(f"stored sequence {ident.sequence} != expected in-run position "
                               f"{expected_in_run}")
            if (run_id, ident.sequence) in seen_seq:
                lineage.append(f"duplicate sequence {ident.sequence} in run {run_id}")
            lineage.extend(validate_call_identity(ident, where=f"call {ident.call_id}"))
            lineage.extend(validate_prepared_call_input(
                fc.prepared_input, where=f"call {ident.call_id} prepared_input"))
            if not fc.fingerprint:
                lineage.append("empty fingerprint")
            if lineage:
                problems.append(
                    f"task {task_id}: call lineage is invalid: {'; '.join(lineage)[:200]}")
                continue

            # F5: episode MEMBERSHIP, decided against the canonical chain.
            if not call_ep:
                problems.append(
                    f"task {task_id}: call {ident.call_id} has an empty episode_id, so it "
                    f"cannot be attributed to any episode")
                continue
            # F6 (round 11): membership is ALWAYS decided. An empty `owned_episode_id` used to
            # skip the check entirely, which meant a caller that forgot to say which episode it
            # owns silently adopted every call it could find. The owning episode falls back to
            # the manifest's own episode id — there is no mode in which ownership is unchecked.
            if call_ep != owns:
                known_ordinal = priors.get(call_ep)
                if known_ordinal is None:
                    problems.append(
                        f"task {task_id}: call {ident.call_id} claims episode {call_ep!r}, "
                        f"which is not a known episode of this job's canonical chain")
                    continue
                if known_ordinal >= episode_ordinal:
                    problems.append(
                        f"task {task_id}: call {ident.call_id} claims episode {call_ep!r} "
                        f"(ordinal {known_ordinal}), which is not strictly earlier than this "
                        f"episode (ordinal {episode_ordinal})")
                    continue
                if call_ep not in prior_set:
                    problems.append(
                        f"task {task_id}: call {ident.call_id} claims episode {call_ep!r}, "
                        f"which this episode does not list among its priors "
                        f"{list(prior_episode_ids)}")
                    continue
                # A VERIFIED call of a KNOWN, listed, strictly-earlier episode is legitimately
                # excluded — and never restamped. It still counts toward its run's sequence,
                # because the run numbered it.
                run_seq = expected_in_run
                seen_seq.add((run_id, ident.sequence))
                observed_prior += 1
                # F1: a prior-episode call is still part of THIS RUN's ledger — the run made it.
                # Dropping it would make the ledger disagree with the run it claims to describe.
                ledger_entries.append(_ledger_entry(ident, fc))
                continue

            if (ident.task_id, ident.role, ident.round, ident.kind) in seen_logical:
                problems.append(
                    f"task {task_id}: duplicate logical call slot "
                    f"{(ident.task_id, ident.role, ident.round, ident.kind)}")
                continue

            run_seq = expected_in_run
            seq += 1
            observed_here += 1
            seen_seq.add((run_id, ident.sequence))
            seen_logical.add((ident.task_id, ident.role, ident.round, ident.kind))
            # Only a call whose stored lineage VERIFIED gets the manifest's derived job-wide
            # position. Everything else about the identity is used EXACTLY as stored — no
            # restamping of ownership, and malformed data never reaches this line.
            published = dataclasses.replace(ident, sequence=seq)
            calls.append(FinalizedCall(
                identity=published, fingerprint=fc.fingerprint,
                prepared_input=fc.prepared_input, fingerprint_source=fc.fingerprint_source,
                ok=fc.ok))
            ledger_entries.append(_ledger_entry(ident, fc))

        # F1 (round 12): the CANONICAL LEDGER for this run — the immutable account of every
        # call it finalized, published as an artifact in this episode's tree. The count and the
        # hash below name THESE bytes, so a later reader can check the claim instead of taking
        # the manifest's word for it.
        #
        # F2 (round 13): its terminal state comes from the RUN's own strictly-decoded
        # `final_status`, not from the task's status. A run whose outcome cannot be read is
        # recorded as an INCOMPLETE ledger plus a coverage problem — never sealed as complete
        # with a plausible default.
        ledger, ledger_problems = _build_run_ledger(job_id, task_id, run_id, run, ledger_entries)
        problems.extend(ledger_problems)
        ledgers.append(ledger)
        seal = ledger.sha256()
        ref = ledger.ref()
        # F6: what did THIS episode expect of this task?
        if observed_here:
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_EXECUTED, run_id=run_id,
                expected_call_count=observed_here, observed_call_count=observed_here,
                finalized_calls_sha256=seal, ledger_ref=ref,
                task_status_at_finalization=status,
                dispatch_state=DISPATCH_THIS_EPISODE))
        elif observed_prior:
            # Its work happened earlier in this job; this episode owes no calls for it.
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_PRIOR_EPISODE, run_id=run_id,
                finalized_calls_sha256=seal, ledger_ref=ref,
                task_status_at_finalization=status,
                dispatch_state=DISPATCH_PRIOR_EPISODE))
        elif must_have_calls:
            # F6: the run exists and is readable, and it recorded NOTHING for a task whose own
            # status says it ran. That is missing evidence, not a zero-call task.
            problems.append(
                f"task {task_id} is {status!r} but its run {run_id} recorded no finalized "
                f"calls for this episode")
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_EXECUTED, run_id=run_id,
                expected_call_count=1, finalized_calls_sha256=seal, ledger_ref=ref,
                task_status_at_finalization=status,
                dispatch_state=DISPATCH_THIS_EPISODE))
        else:
            # Dispatched but it never reached a finalized call — the run EXISTS, and that is what
            # proves dispatch happened, so it is named and sealed. This covers a failed/blocked
            # task AND F011's mid-flight stop, where the task is `pending` for the resume while
            # its run already holds work.
            expectations.append(TaskCallExpectationV1(
                task_id=task_id, expectation=EXPECT_DISPATCHED_NO_CALLS, run_id=run_id,
                finalized_calls_sha256=seal, ledger_ref=ref,
                task_status_at_finalization=status,
                dispatch_state=DISPATCH_THIS_EPISODE))

    expectation = CallExpectationV1(episode_phase=episode_phase,
                                    tasks=tuple(expectations))
    return calls, problems, expectation, tuple(ledgers)




# ---------------------------------------------------------------------------
# The manifest record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunManifestV1:
    job_id: str
    episode_id: str
    created_at: str
    status: str                          # completed | stopped | planned
    # F4: the FULL typed episode snapshot wrapper is embedded — version, owning episode id,
    # captured-at, capture phase, capture status and problems — so the manifest is
    # self-contained and does not depend on mutable JobPlan state to know its own snapshot's
    # ownership and capture facts.
    episode_snapshot: EpisodeInputSnapshotV1
    job_input_sha256: str
    calls: tuple[FinalizedCall, ...]
    coverage: CallCoverage
    # F6 (round 10): the SELF-CONTAINED proof of how many calls this episode expected. Zero
    # recorded calls is only ever "complete" when this record says zero were expected.
    call_expectation: CallExpectationV1 = field(default_factory=CallExpectationV1)
    #: F1 (round 12): the canonical Run Call LEDGERS this episode publishes — one per run it
    #: accounted for. They are artifacts in the episode's exact allowlist, so the expectation's
    #: counts and hashes name bytes a reader can verify rather than a promise it must accept.
    call_ledgers: tuple[RunCallLedgerV1, ...] = ()
    prior_episode_ids: tuple[str, ...] = ()
    # F5: a NON-TIME episode order. Ordinals are 1-based, contiguous and strictly increasing;
    # the latest episode is the one with the maximum ordinal. previous_episode_id names the
    # immediately preceding episode (the one with ordinal-1), or "" for the first episode.
    episode_ordinal: int = 1
    previous_episode_id: str = ""
    # F5: a stopped manifest's terminal metadata — the stop REQUEST id, kept SEPARATE from the
    # episode id. The episode id is the active execution episode; the request id names which
    # stop produced this stopped record. Empty for non-stopped manifests.
    stop_request_id: str = ""
    budgets: dict[str, Any] | None = None
    manifest_v: int = MANIFEST_VERSION

    @property
    def snapshot(self) -> InputSnapshot | None:
        """The captured input snapshot (the wrapper's ``input``). ``None`` only for a failed
        capture, which a terminal manifest never carries."""
        return self.episode_snapshot.input

    def to_json(self) -> dict[str, Any]:
        return {
            "manifest_v": self.manifest_v,
            "job_id": self.job_id,
            "episode_id": self.episode_id,
            "created_at": self.created_at,
            "status": self.status,
            "episode_snapshot": self.episode_snapshot.to_json(),
            "job_input_sha256": self.job_input_sha256,
            "calls": [c.to_json() for c in sorted(self.calls, key=lambda c: c.sort_key())],
            "coverage": self.coverage.to_json(),
            "call_expectation": self.call_expectation.to_json(),
            "call_ledgers": [lg.to_json()
                             for lg in sorted(self.call_ledgers,
                                              key=lambda x: (x.task_id, x.run_id))],
            "prior_episode_ids": list(self.prior_episode_ids),
            "episode_ordinal": self.episode_ordinal,
            "previous_episode_id": self.previous_episode_id,
            "stop_request_id": self.stop_request_id,
            "budgets": self.budgets,
        }

    def canonical_bytes(self) -> bytes:
        return _fs.json_bytes(self.to_json(), sort_keys=True)

    def record_sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

    def provenance_projection(self) -> dict[str, Any]:
        """F1: the RECORD/PROVENANCE projection — which job/episode/run/call actually produced
        this Evidence, plus its lifecycle. It carries every execution identity, the terminal
        status, the stop request, the ordinal/history and the artifact refs. It is what
        ``record_sha256`` and the index integrity chain are about. It is NEVER the input
        identity: two identical runs legitimately differ here."""
        return {
            "manifest_v": self.manifest_v,
            "job_id": self.job_id,
            "episode_id": self.episode_id,
            "created_at": self.created_at,
            "status": self.status,
            "stop_request_id": self.stop_request_id,
            "episode_ordinal": self.episode_ordinal,
            "previous_episode_id": self.previous_episode_id,
            "prior_episode_ids": list(self.prior_episode_ids),
            "call_expectation": self.call_expectation.to_json(),
            "call_ledgers": [{"task_id": lg.task_id, "run_id": lg.run_id,
                              "sha256": lg.sha256()}
                             for lg in sorted(self.call_ledgers,
                                              key=lambda x: (x.task_id, x.run_id))],
            "calls": [
                {**c.identity.to_json(), "artifact": c.artifact,
                 "artifact_sha256": c.artifact_sha256}
                for c in sorted(self.calls, key=lambda c: c.sort_key())
            ],
        }

    def provenance_sha256(self) -> str:
        raw = json.dumps(self.provenance_projection(), sort_keys=True,
                         ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def logical_input_projection(self) -> dict[str, Any]:
        """F1/F2: the LOGICAL INPUT projection — ONLY the material inputs an execution was
        given, so two separately executed but otherwise identical runs hash the same.

        Deliberately EXCLUDED (provenance or outcome, never input): job id, episode id, run id,
        the provider-generated call id, artifact paths, the terminal status, the stop request
        id, the episode ordinal/history, and every timestamp.
        """
        snap = self.snapshot
        if snap is None:                 # a failed-capture manifest has no inputs to compare
            return {"manifest_v": self.manifest_v, "snapshot": "failed",
                    "job_input_sha256": self.job_input_sha256}
        return {
            "manifest_v": self.manifest_v,
            "remedy_git_sha": snap.remedy_git_sha,
            "remedy_dirty": snap.remedy_dirty,
            "remedy_worktree_digest": (snap.remedy_worktree or {}).get("digest", ""),
            "target_base_commit": snap.target_base_commit,
            "target_head": snap.target_head,
            "target_tree": snap.target_tree,
            "target_worktree_digest": (snap.target_worktree or {}).get("digest", ""),
            "job_initial_tree": snap.job_initial_tree,
            # F8 (round 12): the workspace's LOGICAL input is its typed IDENTITY, not the git
            # tree-object id. The reference recorded a 40-hex tree while the candidate recorded a
            # 64-hex content digest, and the projection compared the two fields directly — so an
            # identical workspace produced blocking drift. Two different things had been sharing
            # one field name; only one of them can be recomputed read-only, so that is the one
            # the identity uses. `episode_start_workspace_tree` stays as provenance.
            "episode_start_workspace_identity": _workspace_identity_projection(
                snap.episode_start_workspace_identity),
            "job_file_sha256": snap.job_file_sha256,
            "job_input_sha256": self.job_input_sha256,
            "models": dict(sorted(snap.models.items())),
            "config": sorted(snap.config, key=lambda e: str(e.get("key", ""))),
            "environment": sorted(snap.environment, key=lambda e: str(e.get("key", ""))),
            # F1: calls keyed LOGICALLY — task/sequence/role/round/kind + the actual provider
            # transport fingerprint. No run/call/episode id, no artifact path.
            "calls": [
                {"task_id": c.identity.task_id, "sequence": c.identity.sequence,
                 "role": c.identity.role, "round": c.identity.round,
                 "kind": c.identity.kind, "fingerprint": c.fingerprint}
                for c in sorted(self.calls, key=lambda c: c.identity.logical_key())
            ],
        }

    #: Back-compat alias — the input comparison IS the logical projection.
    def comparison_projection(self) -> dict[str, Any]:
        return self.logical_input_projection()

    def logical_input_sha256(self) -> str:
        raw = json.dumps(self.logical_input_projection(), sort_keys=True,
                         ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def call_keys(self) -> list[tuple]:
        return [c.identity.key() for c in self.calls]

    @classmethod
    def from_trusted_json(cls, d: dict[str, Any]) -> "RunManifestV1":
        """F14: TRUSTED in-memory canonical data ONLY. Every untrusted disk record — root
        mirror, episode, recovery, export — MUST use ``decode_run_manifest_v1``."""
        if not isinstance(d, dict):
            raise ManifestError("a manifest must be a JSON object")
        if d.get("manifest_v") != MANIFEST_VERSION:
            raise ManifestError(
                f"unsupported manifest_v {d.get('manifest_v')!r} "
                f"(this build reads {MANIFEST_VERSION})")
        cov = d.get("coverage") or {}
        # F6: the manifest MUST embed the full ``episode_snapshot`` wrapper. F012 is not merged,
        # so there is no accepted historical F012-v1 record to be compatible with — a manifest
        # lacking the wrapper is a SCHEMA error, never a synthesized ``ok`` snapshot whose
        # version/ownership/phase/status would be INVENTED. (Pre-F012 jobs stay legacy because
        # they carry no F012 marker and no manifest at all, not because of a fake wrapper here.)
        if not isinstance(d.get("episode_snapshot"), dict):
            raise ManifestError(
                "manifest is missing its episode_snapshot wrapper (F6: no synthetic legacy "
                "snapshot fallback — a marked F012 manifest must embed the full wrapper)")
        episode_snapshot = EpisodeInputSnapshotV1.from_trusted_json(d["episode_snapshot"])
        return cls(
            job_id=str(d.get("job_id", "")),
            episode_id=str(d.get("episode_id", "")),
            created_at=str(d.get("created_at", "")),
            status=str(d.get("status", "")),
            episode_snapshot=episode_snapshot,
            job_input_sha256=str(d.get("job_input_sha256", "")),
            calls=tuple(sorted((FinalizedCall.from_trusted_json(e) for e in (d.get("calls") or [])),
                               key=lambda c: c.sort_key())),
            coverage=CallCoverage(
                status=str(cov.get("status", COVERAGE_INCOMPLETE)),
                problems=tuple(cov.get("problems") or [])),
            prior_episode_ids=tuple(d.get("prior_episode_ids") or []),
            episode_ordinal=int(d.get("episode_ordinal", 1) or 1),
            previous_episode_id=str(d.get("previous_episode_id", "") or ""),
            stop_request_id=str(d.get("stop_request_id", "") or ""),
        )


_ID_OK = None


def _safe_component(value: str) -> bool:
    """A path-component-safe string: no separators, no traversal, no absolute paths."""
    global _ID_OK
    if _ID_OK is None:
        import re
        _ID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
    v = str(value or "")
    return bool(_ID_OK.match(v)) and ".." not in v and "/" not in v and "\\" not in v


_VALID_STATUS = frozenset({"completed", "stopped", "planned"})


#: F7 (round 11): THE lifecycle matrix, derived from the committed JobPlan/F011/F012 contract.
#:
#: `run_job` sets `completed` only when EVERY task is applied-or-skipped (a max-tasks boundary
#: PAUSES the job instead, and a paused job is not a finished run and gets no manifest). So a
#: completed episode cannot contain a task that was never dispatched, or one that was dispatched
#: and never reached a call — those states describe a job that did not complete.
#:
#: A stop (F011) is different by design: "the call in flight finishes, nothing new starts", so a
#: stopped episode legitimately carries undispatched tasks, and a task that died before its first
#: finalized call.
_LIFECYCLE_MATRIX: dict[tuple[str, str], dict[str, Any]] = {
    ("planned", PHASE_PLANNING_ONLY): {
        "capture": PHASE_PLANNING_ONLY,
        "expectations": {EXPECT_NOT_DISPATCHED},
        "zero_calls": True,
        "stop_request": False,
    },
    ("stopped", PHASE_PRE_WORK_STOP): {
        "capture": PHASE_PRE_WORK_STOP,
        # F5 (round 12): a pre-work stop on a RESUMED job is the normal case — episode 1 finished
        # T001, episode 2 is asked to stop before it starts anything. Its already-completed tasks
        # are `prior_episode` (proven against the canonical chain), and the rest are
        # `not_dispatched`. Permitting only `not_dispatched` rejected an ordinary resume.
        "expectations": {EXPECT_NOT_DISPATCHED, EXPECT_PRIOR_EPISODE},
        "zero_calls": True,
        "stop_request": True,
    },
    ("completed", PHASE_WORKED): {
        "capture": PHASE_EPISODE_START,
        # No `not_dispatched` and no `dispatched_no_calls`: a completed job has every task
        # applied or skipped, so either state would contradict the status it is published under.
        "expectations": {EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE, EXPECT_SKIPPED},
        "zero_calls": None,          # allowed, but only via the all-skipped/prior-episode proof
        "stop_request": False,
    },
    ("stopped", PHASE_WORKED): {
        "capture": PHASE_EPISODE_START,
        "expectations": {EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE, EXPECT_SKIPPED,
                         EXPECT_NOT_DISPATCHED, EXPECT_DISPATCHED_NO_CALLS,
                         EXPECT_FAILED_PRE_DISPATCH},
        "zero_calls": None,
        "stop_request": True,
    },
}

#: Expectations that own a run, and therefore must name it and seal its ledger.
_EXPECTATIONS_WITH_RUN = frozenset({EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE,
                                    EXPECT_DISPATCHED_NO_CALLS})
#: F4 (round 12): expectations that mean the task never owned a run at all.
_EXPECTATIONS_WITHOUT_RUN = frozenset({EXPECT_SKIPPED, EXPECT_NOT_DISPATCHED,
                                       EXPECT_FAILED_PRE_DISPATCH})


#: F10 (round 11): the material identities a WORKED episode must carry. A worked episode ran real
#: provider calls against a real workspace; every one of these is an input that decided what it
#: did, so an empty string here is not "unknown", it is a hole in the record where an input
#: should be.
_WORKED_REQUIRED_IDENTITIES = (
    "remedy_git_sha", "target_base_commit", "job_initial_tree",
    "episode_start_workspace_tree", "job_file_sha256",
)


def validate_snapshot_phase_identities(snap: "InputSnapshot", *, capture_phase: str
                                       ) -> list[str]:
    """F10 (round 11): what a snapshot must carry depends on HOW it was captured.

    A worked episode must carry every material identity — a silent empty string would let a
    manifest claim to pin the inputs of a run whose workspace it never recorded. A pre-work stop
    or a planning-only episode legitimately has no workspace to identify, but it must say so in a
    TYPED way (an `unavailable` identity with a problem), never by leaving a blank the reader has
    to interpret.
    """
    problems: list[str] = []
    if capture_phase == PHASE_EPISODE_START:
        for f in _WORKED_REQUIRED_IDENTITIES:
            if not str(getattr(snap, f, "") or ""):
                problems.append(
                    f"a worked episode must record {f}; an empty value is a missing material "
                    f"identity, not an unknown one (an unobtainable value is recorded as "
                    f"{UNAVAILABLE!r})")
        wid = snap.episode_start_workspace_identity or {}
        status = str(wid.get("status", ""))
        if status == GIT_OK:
            if not str(wid.get("digest", "") or ""):
                problems.append("episode_start_workspace_identity is ok but carries no digest")
        elif status in (GIT_UNAVAILABLE, GIT_INCOMPLETE):
            # An identity the product could not obtain (a non-git target, a cleaned workspace)
            # is allowed — but only when it SAYS SO, with a reason. That is the difference
            # between an honest gap and a hole.
            if not (wid.get("problems") or []):
                problems.append(
                    "a worked episode reports an unavailable episode_start_workspace_identity "
                    "but gives no reason (an unavailable value must be explained, never blank)")
        else:
            problems.append(
                f"a worked episode must record an episode_start_workspace_identity with a "
                f"supported status; {status!r} is not one")
    elif capture_phase in (PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY):
        wid = snap.episode_start_workspace_identity or {}
        status = str(wid.get("status", ""))
        if status not in (GIT_OK, GIT_UNAVAILABLE, GIT_INCOMPLETE):
            problems.append(
                f"a {capture_phase} episode must state its workspace identity explicitly; "
                f"{status!r} is not a supported status")
        if status != GIT_OK and not (wid.get("problems") or []):
            problems.append(
                f"a {capture_phase} episode reports an unavailable workspace identity but gives "
                f"no reason (an unavailable value must be explained, never blank)")
    return problems


#: F4 (round 13): the ledger fields that must equal their manifest call's, exactly. Named once so
#: a future replay-material field is added to the comparison DELIBERATELY rather than forgotten:
#: F140 serves "stream N for call N" keyed by this order, so anything it replays on must be here.
LEDGER_CALL_BIJECTION_FIELDS = ("call_id", "episode_id", "role", "round", "kind",
                                "prepared_input_fingerprint", "ok")


def declared_job_input_task_ids(manifest: "RunManifestV1") -> list[str]:
    """The task ids the EMBEDDED, immutable JobInputDefinition declares."""
    out: list[str] = []
    ji = getattr(getattr(manifest.episode_snapshot, "input", None), "job_input", None)
    if isinstance(ji, dict) and isinstance(ji.get("tasks"), list):
        for t in ji["tasks"]:
            if isinstance(t, dict):
                out.append(str(t.get("task_id", "")))
    return out


def validate_ledger_set(manifest: "RunManifestV1") -> list[str]:
    """F2/F5 (round 14): the ledger SET is exactly the set the expectation accounts for.

    Every individual ledger could be perfectly formed while the SET carried a passenger. A
    fabricated ledger — `task_id=GHOST, run_id=ghostrun, complete=true, entries=[]` — belonged to
    no embedded JobInputDefinition task, no CallExpectation entry and no Manifest Call, and it was
    accepted by typed validation, the writer, the canonical loader and the verified tree. Nothing
    asked what it was doing there, because every check walked FROM the ledgers OUTWARD instead of
    asking whether the ledgers were exactly what the record accounts for.

    The contract is set equality, in both directions:

        expected_ledger_keys = {(task_id, run_id) for each CallExpectation task owning a run}
        actual_ledger_keys   == expected_ledger_keys

    plus: every ledger's task is declared exactly once in the embedded JobInputDefinition, no
    duplicate key, no duplicate canonical ref, and every ref is the one recomputed from the
    ledger's own identity (F3 — so a ref can never be an alias for another ledger's artifact).
    """
    problems: list[str] = []
    expected: set[tuple] = {(t.task_id, t.run_id)
                            for t in manifest.call_expectation.tasks if t.run_id}
    actual: list[tuple] = [(lg.task_id, lg.run_id) for lg in manifest.call_ledgers]

    seen: set[tuple] = set()
    for key in actual:
        if key in seen:
            problems.append(f"two call ledgers for {key[0]}/{key[1]}")
        seen.add(key)

    for key in sorted(seen - expected):
        problems.append(
            f"call ledger {key[0]}/{key[1]} is accounted for by no call_expectation task that "
            f"owns that run: a published manifest carries the ledgers its own record explains, "
            f"and nothing else")
    for key in sorted(expected - seen):
        problems.append(
            f"call_expectation says task {key[0]!r} owns run {key[1]!r}, but the manifest "
            f"carries no ledger for it")

    declared = declared_job_input_task_ids(manifest)
    for lg in manifest.call_ledgers:
        n = declared.count(lg.task_id)
        if n != 1:
            problems.append(
                f"call ledger {lg.task_id}/{lg.run_id} names a task declared {n} time(s) in the "
                f"embedded job input definition (must be exactly once)")

    # F3: refs are collision-free AND recomputable, checked BEFORE anything keys a dict by them.
    by_ref: dict[str, tuple] = {}
    for lg in manifest.call_ledgers:
        ref = canonical_ledger_ref(lg.task_id, lg.run_id)
        if lg.ref() != ref:
            problems.append(
                f"call ledger {lg.task_id}/{lg.run_id} does not sit at the ref recomputed from "
                f"its own identity")
        prior = by_ref.get(ref)
        if prior is not None and prior != (lg.task_id, lg.run_id):
            problems.append(
                f"call ledgers {prior[0]}/{prior[1]} and {lg.task_id}/{lg.run_id} claim the same "
                f"artifact ref {ref!r}: two different runs cannot be backed by one file")
        by_ref[ref] = (lg.task_id, lg.run_id)
    return problems


def _ledger_state_for_run(run: dict, *, where: str) -> tuple[str, list[str]]:
    """F2 (round 13): the ledger's terminal state, STRICTLY DECODED from the run's own record.

    Returns (state, problems). The run is untrusted disk state, so a missing, non-string or
    unrecognised `final_status` is a recorded problem — never a plausible default.
    """
    raw = run.get("final_status")
    if raw is None:
        return "", [f"{where}: run record has no final_status, so its terminal state is unknown"]
    if not isinstance(raw, str):
        return "", [f"{where}: run final_status is not a string"]
    if not raw:
        # A run that has not finished has no terminal state to record.
        return "", [f"{where}: run has not reached a terminal state"]
    state = RUN_FINAL_STATUS_TO_LEDGER_STATE.get(raw)
    if state is None:
        return "", [f"{where}: run final_status {raw[:40]!r} is not a recognised terminal status"]
    return state, []


def _ordered_manifest_entries_for_run(manifest: "RunManifestV1", task_id: str,
                                      run_id: str) -> list:
    """This run's current-episode manifest calls, in the manifest's canonical job-wide order."""
    return [c for c in sorted(manifest.calls, key=lambda c: c.sort_key())
            if c.identity.task_id == task_id and c.identity.run_id == run_id]


def validate_call_ledgers(manifest: "RunManifestV1", *,
                          mode: str = MODE_PUBLISHED_REFERENCE) -> list[str]:
    """F1 (round 12): the Manifest's calls and its LEDGERS must be the same account.

    Reproduced before this existed: drop a call, restate the counts, put any 64-hex string in the
    hash field — and the reference validated. The ledger closes that by being real bytes with a
    bijection: every current-episode manifest call maps to exactly ONE ledger entry, and every
    ledger entry is either that call or a proven prior-episode one. Nothing is left over on
    either side.
    """
    problems: list[str] = []
    ledgers = list(manifest.call_ledgers)
    problems.extend(validate_ledger_set(manifest))
    by_key: dict[tuple, RunCallLedgerV1] = {}
    for lg in ledgers:
        problems.extend(validate_run_call_ledger(lg, mode=mode))
        if lg.job_id != manifest.job_id:
            problems.append(f"call ledger {lg.task_id}/{lg.run_id} belongs to job "
                            f"{lg.job_id!r}, not {manifest.job_id!r}")
        key = (lg.task_id, lg.run_id)
        if key in by_key:
            problems.append(f"two call ledgers for {lg.task_id}/{lg.run_id}")
        by_key[key] = lg

    # Every expectation that names a ledger must name one that EXISTS, with matching bytes.
    for te in manifest.call_expectation.tasks:
        if not te.ledger_ref and not te.finalized_calls_sha256:
            continue
        lg = by_key.get((te.task_id, te.run_id))
        if lg is None:
            problems.append(
                f"call_expectation for {te.task_id!r} names ledger {te.ledger_ref!r} but the "
                f"manifest carries no such ledger")
            continue
        if te.ledger_ref != lg.ref():
            problems.append(
                f"call_expectation for {te.task_id!r} names ledger ref {te.ledger_ref!r}, but "
                f"its ledger is at {lg.ref()!r}")
        if te.finalized_calls_sha256 != lg.sha256():
            problems.append(
                f"call_expectation for {te.task_id!r} seals a ledger hash that is not its "
                f"ledger's canonical bytes")

    # THE BIJECTION: current-episode manifest calls <-> ledger entries.
    for c in manifest.calls:
        lg = by_key.get((c.identity.task_id, c.identity.run_id))
        if lg is None:
            problems.append(
                f"call {c.identity.call_id} has no ledger for {c.identity.task_id}/"
                f"{c.identity.run_id}")
            continue
        matches = [e for e in lg.entries if e.call_id == c.identity.call_id]
        if len(matches) != 1:
            problems.append(
                f"call {c.identity.call_id} maps to {len(matches)} ledger entries (must be "
                f"exactly one)")
            continue
        e = matches[0]
        # F3/F4 (round 13): the EXACT field set, compared field by field. `ok` used to be absent
        # from this comparison, so a ledger could record a call as failed while the manifest
        # published it as successful — two accounts of the same call disagreeing, both sealed,
        # both validating. Whatever F140 replays on must be compared here.
        expected = {"call_id": c.identity.call_id, "episode_id": c.identity.episode_id,
                    "role": c.identity.role, "round": c.identity.round,
                    "kind": c.identity.kind, "prepared_input_fingerprint": c.fingerprint,
                    "ok": c.ok}
        for field_name in LEDGER_CALL_BIJECTION_FIELDS:
            got = getattr(e, field_name)
            want = expected[field_name]
            if got != want:
                problems.append(
                    f"ledger entry {e.call_id} {field_name} {got!r} != its manifest call's "
                    f"{want!r}")

    published_ids = {c.identity.call_id for c in manifest.calls}
    prior = set(manifest.prior_episode_ids)
    for lg in ledgers:
        for e in lg.entries:
            if e.call_id in published_ids:
                continue
            # Not published HERE: it may only be a proven prior-episode call.
            if e.episode_id == manifest.episode_id:
                problems.append(
                    f"ledger entry {e.call_id} belongs to this episode but the manifest does "
                    f"not publish it")
            elif e.episode_id not in prior:
                problems.append(
                    f"ledger entry {e.call_id} names episode {e.episode_id!r}, which is neither "
                    f"this episode nor one of its priors")
        # F4 (round 13): ORDER IS EVIDENCE. Every entry could match its call one-for-one while
        # the SEQUENCE said something else entirely — swap two entries' per_run_sequence and the
        # ledger stayed contiguous, every field still matched, and the reference validated. But
        # the order IS the claim ("the builder ran, then the reviewer"), and F140's replay serves
        # stream N for call N by it. So this episode's ledger entries, read in their recorded
        # order, must be exactly the manifest's calls for that run in canonical order.
        ordered_calls = _ordered_manifest_entries_for_run(manifest, lg.task_id, lg.run_id)
        here_entries = [e for e in sorted(lg.entries, key=lambda x: x.per_run_sequence)
                        if e.episode_id == manifest.episode_id]
        if [e.call_id for e in here_entries] != [c.identity.call_id for c in ordered_calls]:
            problems.append(
                f"call ledger {lg.task_id}/{lg.run_id} orders this episode's calls "
                f"{[e.call_id for e in here_entries]}, but the manifest publishes them "
                f"{[c.identity.call_id for c in ordered_calls]}")
        # This episode's entries are the ledger's SUFFIX: the run's earlier calls came first.
        if here_entries:
            tail = sorted(lg.entries, key=lambda x: x.per_run_sequence)[-len(here_entries):]
            if [e.call_id for e in tail] != [e.call_id for e in here_entries]:
                problems.append(
                    f"call ledger {lg.task_id}/{lg.run_id} does not end with this episode's "
                    f"calls; a prior-episode entry cannot come after them")

        # The counts the expectation states must be the ledger's own truth.
        te = next((x for x in manifest.call_expectation.tasks
                   if x.task_id == lg.task_id and x.run_id == lg.run_id), None)
        if te is not None:
            here = sum(1 for e in lg.entries if e.episode_id == manifest.episode_id)
            if te.expected_call_count != here:
                problems.append(
                    f"call_expectation for {lg.task_id!r} expects {te.expected_call_count} "
                    f"call(s) but its ledger records {here} for this episode")
            # F2 (round 13): the ledger's terminal state must agree with the task lifecycle the
            # expectation recorded. The run record itself is bound at finalization (where the run
            # is in hand); this is the half a STORED reference can still be held to.
            status = te.task_status_at_finalization
            if status in _TASK_STATUS_FORBIDS_LEDGER:
                problems.append(
                    f"task {lg.task_id!r} is {status!r} at finalization, so it can own no call "
                    f"ledger: skipping happens before dispatch")
            required = _TASK_STATUS_REQUIRES_LEDGER_STATE.get(status)
            if required and lg.terminal_state not in required:
                problems.append(
                    f"call ledger {lg.task_id}/{lg.run_id} says its run ended "
                    f"{lg.terminal_state!r}, but the task reached {status!r}, which is only "
                    f"reachable after a successful run ({'/'.join(sorted(required))})")
    return problems


def validate_call_expectation(exp: "CallExpectationV1", *, status: str, capture_phase: str,
                              stop_request_id: str, calls: tuple | list,
                              declared_task_ids: list[str],
                              require_exact_tasks: bool = True) -> list[str]:
    """F7/F8/F9 (round 11): the expectation record must describe a lifecycle that can exist.

    A record saying "this run completed" and "this task was never dispatched" is not a record of
    anything that happened; the product cannot produce it. Publishing such a combination is how
    a manifest ends up internally consistent and externally false. So the matrix is exact and
    closed, and every impossible combination is refused at the boundary.
    """
    problems: list[str] = []
    if exp.expectation_v != 1:
        problems.append(f"unsupported call_expectation.expectation_v {exp.expectation_v!r}")
    if exp.episode_phase not in VALID_EPISODE_PHASES:
        problems.append(f"call_expectation.episode_phase {exp.episode_phase!r} is not a "
                        f"supported phase")
        return problems

    rule = _LIFECYCLE_MATRIX.get((status, exp.episode_phase))
    if rule is None and status in _VALID_STATUS:
        problems.append(
            f"impossible lifecycle: a {status!r} episode cannot have expectation phase "
            f"{exp.episode_phase!r}")
        rule = None

    if rule is not None:
        if capture_phase and capture_phase != rule["capture"]:
            problems.append(
                f"impossible lifecycle: a {status!r}/{exp.episode_phase!r} episode requires the "
                f"snapshot capture phase {rule['capture']!r}, but it was captured as "
                f"{capture_phase!r}")
        if rule["stop_request"] and not stop_request_id:
            problems.append(
                f"a {status!r}/{exp.episode_phase!r} episode must carry its stop request id")
        if not rule["stop_request"] and stop_request_id:
            problems.append(
                f"a {status!r}/{exp.episode_phase!r} episode must not carry a stop request id")
        if rule["zero_calls"] and calls:
            problems.append(
                f"a {status!r}/{exp.episode_phase!r} episode must record zero calls, but it "
                f"carries {len(calls)}")
        for te in exp.tasks:
            if te.expectation in VALID_TASK_EXPECTATIONS and \
                    te.expectation not in rule["expectations"]:
                problems.append(
                    f"impossible lifecycle: task {te.task_id!r} is {te.expectation!r} in a "
                    f"{status!r}/{exp.episode_phase!r} episode, which cannot happen "
                    f"(allowed: {sorted(rule['expectations'])})")

    # F8: the proof covers EXACTLY the embedded definition's tasks — same ids, same order, no
    # ghost, no omission. This holds even when the definition declares none.
    exp_ids = [te.task_id for te in exp.tasks]
    if len(exp_ids) != len(set(exp_ids)):
        problems.append(f"call_expectation lists a task more than once: {exp_ids}")
    if require_exact_tasks and exp_ids != list(declared_task_ids):
        problems.append(f"call_expectation tasks {exp_ids} are not exactly the embedded "
                        f"job_input tasks {list(declared_task_ids)}")

    observed: dict[str, int] = {}
    run_of: dict[str, set] = {}
    for c in calls:
        tid = c.identity.task_id
        observed[tid] = observed.get(tid, 0) + 1
        run_of.setdefault(tid, set()).add(c.identity.run_id)

    for te in exp.tasks:
        if te.expectation not in VALID_TASK_EXPECTATIONS:
            problems.append(f"call_expectation for {te.task_id!r} has an unsupported "
                            f"expectation {te.expectation!r}")
            continue
        # F2 (round 16): THE closed truth table — the expectation must agree with the task status
        # the JobPlan actually recorded. Both facts were stored since round 12; nothing compared
        # them, so `skipped` + `applied_to_job_workspace` published cleanly.
        problems.extend(validate_task_expectation_truth(
            te, episode_status=status, episode_phase=exp.episode_phase))
        seen = observed.get(te.task_id, 0)
        # F9: EXACT counts, not a floor.
        if te.observed_call_count != seen:
            problems.append(
                f"call_expectation for {te.task_id!r} records {te.observed_call_count} observed "
                f"call(s) but the manifest carries {seen}")
        if te.expected_call_count != seen:
            problems.append(
                f"call_expectation for {te.task_id!r} expected exactly {te.expected_call_count} "
                f"call(s) but the manifest carries {seen}")
        if te.expectation == EXPECT_EXECUTED and te.expected_call_count < 1:
            problems.append(f"call_expectation for {te.task_id!r} says it executed but expects "
                            f"no calls")
        if te.expectation != EXPECT_EXECUTED and te.expected_call_count:
            problems.append(f"call_expectation for {te.task_id!r} is {te.expectation!r} but "
                            f"expects {te.expected_call_count} call(s)")
        # F9: the run binding — a task that owns a run names it, and the calls agree.
        if te.expectation in _EXPECTATIONS_WITH_RUN:
            if not te.run_id:
                problems.append(
                    f"call_expectation for {te.task_id!r} is {te.expectation!r} but names no "
                    f"run id")
            if not _is_hex64(te.finalized_calls_sha256):
                problems.append(
                    f"call_expectation for {te.task_id!r} is {te.expectation!r} but carries no "
                    f"finalized-call ledger seal")
        else:
            # F4 (round 12): a task that was never dispatched owns no run — and a record that
            # names one anyway is a CONTRADICTION between two persisted facts, not a field to
            # tidy away. (`_collect_calls` reports it; the validator refuses to publish it.)
            if te.run_id:
                problems.append(
                    f"call_expectation for {te.task_id!r} is {te.expectation!r} but names run "
                    f"{te.run_id!r}: a task cannot be both never dispatched and the owner of a "
                    f"run")
            if te.finalized_calls_sha256 or te.ledger_ref:
                problems.append(
                    f"call_expectation for {te.task_id!r} is {te.expectation!r} and must not "
                    f"seal a ledger it has none of")
        # F4: the persisted lifecycle facts this expectation was derived from must be present
        # and coherent.
        if te.dispatch_state not in VALID_DISPATCH_STATES:
            problems.append(
                f"call_expectation for {te.task_id!r} has an unsupported dispatch_state "
                f"{te.dispatch_state!r}")
        elif te.expectation in _EXPECTATIONS_WITHOUT_RUN and \
                te.dispatch_state != DISPATCH_NEVER:
            problems.append(
                f"call_expectation for {te.task_id!r} is {te.expectation!r} but its "
                f"dispatch_state says {te.dispatch_state!r}")
        elif te.expectation == EXPECT_PRIOR_EPISODE and \
                te.dispatch_state != DISPATCH_PRIOR_EPISODE:
            problems.append(
                f"call_expectation for {te.task_id!r} is a prior-episode task but its "
                f"dispatch_state says {te.dispatch_state!r}")
        foreign = run_of.get(te.task_id, set()) - {te.run_id}
        if foreign:
            problems.append(
                f"call_expectation for {te.task_id!r} names run {te.run_id!r}, but its calls "
                f"were recorded under {sorted(foreign)}")
    return problems


def validate_run_manifest(manifest: "RunManifestV1", *, published: bool = True,
                          mode: str | None = None) -> list[str]:
    """One strict validator used at every read/write/diff/export boundary (F7). Returns the
    list of problems (empty == valid). Never normalizes silently."""
    if mode is None:
        mode = MODE_PUBLISHED_REFERENCE if published else MODE_PREPUBLICATION
    published = mode in (MODE_PUBLISHED_REFERENCE,)
    problems: list[str] = []
    if manifest.manifest_v != MANIFEST_VERSION:
        problems.append(f"unsupported manifest_v {manifest.manifest_v}")
    if not _safe_component(manifest.job_id):
        problems.append("unsafe or empty job_id")
    if not _safe_component(manifest.episode_id):
        problems.append("unsafe or empty episode_id")
    if manifest.status not in _VALID_STATUS:
        problems.append(f"invalid status {manifest.status!r}")
    # F7: created_at must be a timezone-aware UTC ISO-8601 timestamp — never naive.
    if not _is_utc_timestamp(manifest.created_at):
        problems.append(f"created_at is not a UTC-aware timestamp: {manifest.created_at!r}")
    # F7: job_input_sha256 must be exactly 64 lowercase hex.
    if not _is_hex64(manifest.job_input_sha256):
        problems.append("job_input_sha256 is not 64 lowercase hex")

    seen_ids: set[tuple] = set()
    seen_artifacts: set[str] = set()
    calls = sorted(manifest.calls, key=lambda c: c.identity.sequence)
    # F7 (round 10): every Call is BOUND to the EMBEDDED job-input definition. The definition is
    # the immutable record of which tasks this episode was given; a call naming a task that is
    # not in it describes work no recorded input asked for, so the manifest cannot be a faithful
    # account of its own inputs. The binding uses the snapshot's definition (immutable) — never a
    # later, mutable `job.tasks` list.
    declared_task_ids: list[str] = []
    _ji = getattr(getattr(manifest.episode_snapshot, "input", None), "job_input", None)
    if isinstance(_ji, dict) and isinstance(_ji.get("tasks"), list):
        for _t in _ji["tasks"]:
            if isinstance(_t, dict):
                declared_task_ids.append(str(_t.get("task_id", "")))

    for i, c in enumerate(calls, start=1):
        ident = c.identity
        key = ident.key()
        if key in seen_ids:
            problems.append(f"duplicate call identity: {key}")
        seen_ids.add(key)
        if declared_task_ids:
            count = declared_task_ids.count(ident.task_id)
            if count != 1:
                problems.append(
                    f"call {ident.call_id} task_id {ident.task_id!r} appears {count} times in "
                    f"the embedded job_input task list {declared_task_ids} (must be exactly once)")
        if ident.sequence != i:
            problems.append(f"call sequence not contiguous at position {i} "
                            f"(got {ident.sequence})")
        if ident.job_id and ident.job_id != manifest.job_id:
            problems.append(f"call {ident.call_id} job_id != manifest job_id")
        if ident.episode_id and ident.episode_id != manifest.episode_id:
            problems.append(f"call {ident.call_id} episode_id != manifest episode_id")
        for f in ("task_id", "run_id", "role", "kind", "call_id"):
            if not str(getattr(ident, f, "")):
                problems.append(f"call at seq {ident.sequence} has empty {f}")
        # F9: every identity component is strict, bounded and path-safe.
        problems.extend(validate_call_identity(ident, where=f"call {ident.call_id}"))
        # F7: the fingerprint is BOUND to the prepared input — recomputed from the recorded
        # transport components — so a tampered fingerprint or component set is rejected.
        problems.extend(validate_prepared_call_input(
            c.prepared_input, where=f"call {ident.call_id} prepared_input"))
        if not _is_hex64(c.fingerprint):
            problems.append(f"call {ident.call_id} fingerprint is not 64 lowercase hex")
        elif isinstance(c.prepared_input, dict) and \
                c.prepared_input.get("fingerprint") != c.fingerprint:
            problems.append(f"call {ident.call_id} fingerprint != prepared_input.fingerprint")
        if c.fingerprint_source not in VALID_FINGERPRINT_SOURCES:
            problems.append(f"call {ident.call_id} has an invalid fingerprint_source "
                            f"{c.fingerprint_source!r}")
        # F11: the recorded prepared input is bounded, so the writer can never create a record
        # the exporter would later refuse for size alone.
        try:
            if len(_fs.json_bytes(c.prepared_input, sort_keys=True)) > \
                    _S.MAX_PREPARED_INPUT_BYTES:
                problems.append(f"call {ident.call_id} prepared_input exceeds the size limit")
        except Exception:
            problems.append(f"call {ident.call_id} prepared_input is not serializable")
        # F8: a PUBLISHED call must carry a real, canonically-named, hash-bound artifact.
        ref = c.artifact
        if published:
            expected_ref = canonical_artifact_ref(ident)
            if not ref:
                problems.append(f"call {ident.call_id} has no artifact ref")
            elif ref != expected_ref:
                problems.append(f"call {ident.call_id} artifact ref {ref!r} != canonical "
                                f"{expected_ref!r}")
            if not _is_hex64(getattr(c, "artifact_sha256", "") or ""):
                problems.append(f"call {ident.call_id} artifact_sha256 is not 64 lowercase hex")
            elif hashlib.sha256(c.canonical_artifact_bytes()).hexdigest() != c.artifact_sha256:
                problems.append(f"call {ident.call_id} artifact_sha256 does not match its "
                                f"canonical bytes")
        elif ref and not _is_hex64(getattr(c, "artifact_sha256", "") or ""):
            problems.append(f"call {ident.call_id} artifact_sha256 is not 64 lowercase hex")
        if ref:
            if ".." in ref or ref.startswith("/") or "\\" in ref:
                problems.append(f"unsafe artifact ref {ref!r}")
            name = ref.split("/")[-1]
            if name in seen_artifacts:
                problems.append(f"duplicate artifact filename {name!r}")
            seen_artifacts.add(name)

    if published and len(seen_artifacts) != len(calls):
        problems.append(f"artifact count {len(seen_artifacts)} != call count {len(calls)}")

    # F10: coverage is a CLOSED enum with coherent problems.
    if manifest.coverage.status not in (COVERAGE_COMPLETE, COVERAGE_INCOMPLETE):
        problems.append(f"invalid coverage status {manifest.coverage.status!r}")
    elif manifest.coverage.status == COVERAGE_COMPLETE and manifest.coverage.problems:
        problems.append("coverage is complete yet declares problems")
    elif manifest.coverage.status == COVERAGE_INCOMPLETE and not manifest.coverage.problems:
        problems.append("coverage is incomplete yet declares no problem")

    # F1: a PUBLISHED terminal reference must have COMPLETE coverage. A stored completed/stopped
    # record whose own coverage says "incomplete" is manifest CORRUPTION (integrity, exit 1) —
    # not something for a second Evidence-only rule to catch later. A CURRENT CANDIDATE may be
    # incomplete (historic provider inputs are not always reconstructable → exit 5).
    # F6 (round 10): the expectation proof is validated against the EMBEDDED definition, so a
    # stored reference can be judged entirely on its own contents.
    # F10 (round 11): the snapshot must carry the identities its own capture phase requires.
    _snap_in = getattr(manifest.episode_snapshot, "input", None)
    if _snap_in is not None:
        problems.extend(validate_snapshot_phase_identities(
            _snap_in, capture_phase=getattr(manifest.episode_snapshot, "capture_phase", "")))

    # F8 (round 13): ONE ledger contract, carrying the caller's mode. A published reference is
    # held to completeness; a prepublication candidate is judged as what it is.
    problems.extend(validate_call_ledgers(manifest, mode=mode))

    exp = manifest.call_expectation
    problems.extend(validate_call_expectation(
        exp, status=manifest.status,
        capture_phase=getattr(manifest.episode_snapshot, "capture_phase", ""),
        stop_request_id=manifest.stop_request_id,
        calls=calls, declared_task_ids=declared_task_ids,
        require_exact_tasks=(mode == MODE_PUBLISHED_REFERENCE)))

    if mode == MODE_PUBLISHED_REFERENCE and manifest.status in ("completed", "stopped"):
        # F6: zero calls is a CLAIM, and a published reference has to prove it. The proof is the
        # embedded expectation record — never the mutable JobPlan, which may have moved on.
        if not calls and not exp.expects_zero_calls():
            problems.append(
                "a published terminal reference records zero calls, but its call_expectation "
                "does not prove zero calls were expected")
        if not calls and not exp.tasks and declared_task_ids:
            problems.append(
                "a published terminal reference records zero calls and carries no "
                "call_expectation proof at all")
        if manifest.coverage.status != COVERAGE_COMPLETE:
            problems.append(
                f"a published {manifest.status} reference manifest must have complete call "
                f"coverage; incomplete coverage is manifest corruption "
                f"({'; '.join(manifest.coverage.problems)[:200]})")
    for p in manifest.coverage.problems:
        if len(p) > _S.MAX_PROBLEM_LEN:
            problems.append("a coverage problem exceeds the length limit")

    prior = list(manifest.prior_episode_ids)
    if len(prior) != len(set(prior)):
        problems.append("duplicate prior_episode_ids")
    for pe in prior:
        if not _safe_component(pe):
            problems.append(f"unsafe prior_episode_id {pe!r}")
        if pe == manifest.episode_id:
            problems.append("prior_episode_ids contains this episode (self reference)")

    # F5: the non-time episode ordinal. It is 1-based; previous_episode_id is set iff the
    # episode is not the first, must differ from this episode, and must be one of its priors.
    if manifest.episode_ordinal < 1:
        problems.append(f"episode_ordinal must be >= 1 (got {manifest.episode_ordinal})")
    prev = manifest.previous_episode_id
    if prev:
        if prev == manifest.episode_id:
            problems.append("previous_episode_id is this episode (self reference)")
        if not _safe_component(prev):
            problems.append(f"unsafe previous_episode_id {prev!r}")
        if prev not in set(prior):
            problems.append("previous_episode_id is not among prior_episode_ids")
        if manifest.episode_ordinal == 1:
            problems.append("first episode (ordinal 1) must have no previous_episode_id")
    elif manifest.episode_ordinal > 1:
        problems.append(f"episode ordinal {manifest.episode_ordinal} has no "
                        f"previous_episode_id")

    # F4: the embedded episode snapshot must be valid and bound to THIS episode. A terminal
    # (completed/stopped) manifest additionally requires a fully ``ok`` snapshot — a
    # failed-capture snapshot may never back a terminal record.
    for p in validate_episode_input_snapshot(manifest.episode_snapshot,
                                             expected_episode_id=manifest.episode_id):
        problems.append(f"episode_snapshot: {p}")
    if manifest.status in ("completed", "stopped") and not manifest.episode_snapshot.is_ok():
        problems.append(f"a {manifest.status} manifest requires a valid ok episode snapshot")
    # F5/F7: the InputSnapshot payload itself is strictly validated (required worktree fields,
    # redundant-fact agreement, unique config/env keys, REMEDY_* only, no absolute paths or raw
    # secrets, bounds).
    if manifest.episode_snapshot.input is not None:
        snap = manifest.episode_snapshot.input
        for p in validate_input_snapshot(snap):
            problems.append(f"input_snapshot: {p}")
        # F6: the recorded job-input hash is BOUND to the manifest's OWN embedded definition.
        # A tampered hash — or a tampered definition — can no longer agree with itself.
        for p in validate_job_input_definition(snap.job_input):
            problems.append(f"job_input: {p}")
        try:
            expected = job_input_definition_sha256(snap.job_input)
        except Exception:
            expected = ""
            problems.append("job_input definition is not canonically serializable")
        if expected and manifest.job_input_sha256 != expected:
            problems.append("job_input_sha256 does not match the embedded job-input definition")
        # F11: bound the embedded payloads exactly as the exporter will.
        try:
            if len(job_input_definition_bytes(snap.job_input)) > _S.MAX_JOB_INPUT_BYTES:
                problems.append("job_input definition exceeds the size limit")
            if len(_fs.json_bytes(snap.to_json(), sort_keys=True)) > \
                    _S.MAX_INPUT_SNAPSHOT_BYTES:
                problems.append("input snapshot exceeds the size limit")
        except Exception:
            problems.append("input snapshot is not canonically serializable")

    # F5/F7: the stop request id is stopped-only terminal metadata, kept SEPARATE from the
    # episode id, and must be a SAFE bounded request id (no separators/traversal/spaces/paths).
    if manifest.status == "stopped":
        if not manifest.stop_request_id:
            problems.append("a stopped manifest must record its stop_request_id")
        elif not _is_safe_request_id(manifest.stop_request_id):
            problems.append(f"unsafe stop_request_id {manifest.stop_request_id!r}")
    elif manifest.stop_request_id:
        problems.append(f"non-stopped manifest carries a stop_request_id "
                        f"{manifest.stop_request_id!r}")
    return problems


# ---------------------------------------------------------------------------
# F4 — strict raw-JSON decoders (the ONLY entry for untrusted manifest bytes)
# ---------------------------------------------------------------------------


def decode_prepared_call_input_v1(raw: Any) -> "PreparedCallInput":
    """F4/F7: strictly decode a PreparedCallInput. Real JSON types only; bounded."""
    from packages.orchestration.call_identity import PreparedCallInput

    d = _S.req_map(raw, "prepared_input")
    # F8: EXACT field set — an unknown field (a smuggled secret/path note) is refused, never
    # carried through into canonical manifest bytes.
    _S.no_unknown_keys(d, PREPARED_CALL_INPUT_FIELDS, "prepared_input")
    return PreparedCallInput(
        prompt_sha256=_S.req_str(d, "prompt_sha256", "prepared_input", max_len=64),
        prompt_len_bytes=_S.req_int(d, "prompt_len_bytes", "prepared_input", minimum=0,
                                    maximum=64 * 1024 * 1024),
        schema_sha256=_S.req_str(d, "schema_sha256", "prepared_input", max_len=64,
                                 allow_empty=True),
        model=_S.req_str(d, "model", "prepared_input", max_len=_S.MAX_ID_LEN),
        mode=_S.req_str(d, "mode", "prepared_input", max_len=_S.MAX_ID_LEN),
        options_sha256=_S.req_str(d, "options_sha256", "prepared_input", max_len=64),
        fingerprint=_S.req_str(d, "fingerprint", "prepared_input", max_len=64),
    )


def _no_duplicate_keys(pairs):
    """F11: reject a JSON object with DUPLICATE keys — the stdlib silently keeps the last one,
    which lets two different raw byte strings decode to the same object."""
    seen: set[str] = set()
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in seen:
            raise _S.SchemaError(f"duplicate JSON key {k!r}")
        seen.add(k)
        out[k] = v
    return out


def _reject_json_constant(name: str):
    """F9: STANDARD JSON only — ``NaN`` / ``Infinity`` / ``-Infinity`` are Python extensions, not
    JSON. A record carrying one is not readable by a conforming parser, so it is refused."""
    raise _S.SchemaError(f"non-standard JSON constant {name!r}")


def strict_json_loads(raw: bytes | str, *, where: str = "record") -> Any:
    """F9/F11: parse untrusted JSON strictly — duplicate keys rejected, the non-standard
    ``NaN``/``Infinity`` constants rejected, and invalid UTF-8 surfaced as a bounded
    ``ManifestError`` rather than a raw ``UnicodeDecodeError``."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            text = bytes(raw).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ManifestError(
                f"unreadable {where}: not valid UTF-8 ({exc.reason})") from None
    else:
        text = raw
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_reject_json_constant)
    except _S.SchemaError:
        raise
    except (ValueError, UnicodeDecodeError) as exc:
        raise ManifestError(f"unreadable {where}: {exc}") from None


def require_canonical_bytes(raw: bytes, obj: Any, *, where: str) -> None:
    """F11: THE raw-byte trust rule — ``raw bytes == canonical_bytes(strictly_decoded_object)``.

    Decoding normalizes; that normalization must never hide raw-byte drift. Anything stored and
    later trusted (root mirror, episode manifest, index, call artifact) must be byte-for-byte the
    canonical encoding of what it decodes to — so noncanonical whitespace/key order, an unknown
    field that vanished during decode, or a duplicate key can never survive."""
    canonical = _fs.json_bytes(obj.to_json() if hasattr(obj, "to_json") else obj,
                              sort_keys=True)
    if bytes(raw) != canonical:
        raise ManifestError(
            f"{where}: stored bytes are not the canonical encoding of the record they decode "
            f"to (noncanonical formatting, an unknown field, or raw-byte drift)")


#: F6: the isolation modes a job may declare — the real product vocabulary from
#: ``JobPlan.isolation_mode`` ("worktree" for a job-owned git worktree, "copy" for the
#: non-git filtered-copy fallback).
VALID_ISOLATION_MODES = frozenset({"worktree", "copy"})

#: F7: the EXACT JobInputDefinitionV1 schema.
JOB_INPUT_TOP_FIELDS = frozenset({"job_input_v", "job_title_sha256", "job_file_sha256",
                                  "isolation_mode", "tasks", "execution"})
JOB_INPUT_TASK_FIELDS = frozenset({"order", "task_id", "source_heading_number",
                                   "title_sha256", "body_sha256", "acceptance_sha256"})
#: The EXACT material execution field set. Every value has a paired ``_source``. This list and
#: ``ExecutionConfig``'s dataclass fields are kept in lockstep by a guard test, so a future
#: material field cannot be added without updating F012's hashed definition.
JOB_INPUT_EXECUTION_STR_FIELDS = (
    "builder", "builder_model", "builder_effort",
    "reviewer", "reviewer_model", "reviewer_effort",
    "repair_provider", "repair_model", "repair_effort",
    "claude_cli_write_mode", "timeout_profile",
)
JOB_INPUT_EXECUTION_INT_FIELDS = ("max_rounds", "repair_rounds_allowed", "timeout_sec",
                                  "max_output_chars", "max_tasks")
JOB_INPUT_EXECUTION_BOOL_FIELDS = ("stream_evidence",)
#: ``repair_rounds_allowed`` pairs with ``repair_rounds_source`` — not ``*_allowed_source``.
_JOB_INPUT_SOURCE_OF = {"repair_rounds_allowed": "repair_rounds_source"}


def _source_field(name: str) -> str:
    return _JOB_INPUT_SOURCE_OF.get(name, f"{name}_source")


JOB_INPUT_EXECUTION_FIELDS = frozenset(
    list(JOB_INPUT_EXECUTION_STR_FIELDS) + list(JOB_INPUT_EXECUTION_INT_FIELDS)
    + list(JOB_INPUT_EXECUTION_BOOL_FIELDS)
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_STR_FIELDS]
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_INT_FIELDS]
    + [_source_field(f) for f in JOB_INPUT_EXECUTION_BOOL_FIELDS]
    + ["test_command", "test_command_source", "context_strategy"])


def decode_job_input_definition_v1(raw: Any) -> dict[str, Any]:
    """F7/F8: strictly decode the EXACT JobInputDefinitionV1 schema.

    The RULES live in `validate_job_input_definition` — this is the raw-JSON entry point that
    applies them and raises. There is exactly ONE rule set, so the strict decoder and the typed
    `is_ok()` predicate can never disagree about the same record (F8, round 10).

    A minimal/incomplete definition ({tasks: [], execution: {}}) is REJECTED even when its hash
    matches: the hash proves the bytes were not tampered with, not that the definition is the
    complete material input set.
    """
    problems = validate_job_input_definition(raw)
    if problems:
        raise _S.SchemaError(problems[0] if len(problems) == 1
                             else "; ".join(problems)[:400])
    return dict(raw)


def decode_call_identity_v1(raw: Any) -> CallIdentity:
    d = _S.req_map(raw, "identity")
    _S.no_unknown_keys(d, {"job_id", "task_id", "run_id", "sequence", "role", "round",
                           "kind", "call_id", "episode_id"}, "identity")
    return CallIdentity(
        job_id=_S.req_str(d, "job_id", "identity", max_len=_S.MAX_ID_LEN),
        task_id=_S.req_str(d, "task_id", "identity", max_len=_S.MAX_ID_LEN),
        run_id=_S.req_str(d, "run_id", "identity", max_len=_S.MAX_ID_LEN),
        sequence=_S.req_int(d, "sequence", "identity", minimum=1,
                            maximum=_S.MAX_CALLS_PER_EPISODE),
        role=_S.req_str(d, "role", "identity", max_len=_S.MAX_ID_LEN),
        round=_S.req_int(d, "round", "identity", minimum=1, maximum=10_000),
        kind=_S.req_str(d, "kind", "identity", max_len=_S.MAX_ID_LEN),
        call_id=_S.req_str(d, "call_id", "identity", max_len=_S.MAX_ID_LEN),
        episode_id=_S.req_str(d, "episode_id", "identity", max_len=_S.MAX_ID_LEN,
                              allow_empty=True),
    )


def decode_finalized_call_v1(raw: Any) -> FinalizedCall:
    """F4: strictly decode one finalized call. ``ok`` must be a real JSON boolean."""
    d = _S.req_map(raw, "call")
    _S.no_unknown_keys(d, {"identity", "fingerprint", "prepared_input", "fingerprint_source",
                           "ok", "artifact", "artifact_sha256"}, "call")
    prepared = decode_prepared_call_input_v1(_S.req_key(d, "prepared_input", "call"))
    return FinalizedCall(
        identity=decode_call_identity_v1(_S.req_key(d, "identity", "call")),
        fingerprint=_S.req_str(d, "fingerprint", "call", max_len=256),
        prepared_input=prepared.to_json(),
        fingerprint_source=_S.req_str(d, "fingerprint_source", "call", max_len=_S.MAX_ID_LEN),
        ok=_S.req_bool(d, "ok", "call"),
        artifact=_S.req_str(d, "artifact", "call", max_len=_S.MAX_SHORT_TEXT,
                            allow_empty=True),
        artifact_sha256=_S.req_str(d, "artifact_sha256", "call", max_len=64,
                                   allow_empty=True),
    )


#: F6: the EXACT InputSnapshot field set — nothing else may appear.
INPUT_SNAPSHOT_FIELDS = frozenset({
    "remedy_git_sha", "remedy_dirty", "remedy_worktree", "target_base_commit", "target_head",
    "target_tree", "target_worktree", "job_initial_tree", "episode_start_workspace_tree",
    "episode_start_workspace_identity",
    "job_file_sha256", "job_input", "models", "provider_versions", "config", "environment",
    "python_version", "platform", "pythonhashseed"})
#: F6: the EXACT WorktreeIdentity record field set.
WORKTREE_FIELDS = frozenset({"status", "head", "digest", "problems", "dirty"})


def decode_input_snapshot_v1(raw: Any) -> "InputSnapshot":
    """F4/F6: strictly decode an InputSnapshot as an EXACT RECURSIVE schema.

    No Boolean/integer coercion, bounded lists, and — critically — NO unknown field at any
    level: not at the top, not inside a worktree record, not inside a config/environment entry.
    An unknown key is exactly how a canary (``"EXTRA_SECRET": "…/home/alice"``) previously rode
    into the canonical manifest bytes and the Evidence export."""
    d = _S.req_map(raw, "input_snapshot")
    _S.no_unknown_keys(d, INPUT_SNAPSHOT_FIELDS, "input_snapshot")

    def _entries(key: str, max_len: int, allowed: set[str]) -> list[dict[str, Any]]:
        items = _S.req_list(d, key, "input_snapshot", max_len=max_len)
        out: list[dict[str, Any]] = []
        for i, it in enumerate(items):
            e = _S.req_map(it, f"input_snapshot.{key}[{i}]")
            _S.no_unknown_keys(e, allowed, f"input_snapshot.{key}[{i}]")
            k = _S.req_str(e, "key", f"input_snapshot.{key}[{i}]", max_len=_S.MAX_ID_LEN)
            if _S.has_control_chars(k):
                raise _S.SchemaError(f"input_snapshot.{key}[{i}].key has control characters")
            v = e.get("value", None)
            if v is not None and not isinstance(v, (str, int, float, bool)):
                raise _S.SchemaError(
                    f"input_snapshot.{key}[{i}].value must be a scalar or null, got "
                    f"{type(v).__name__}")
            if isinstance(v, str) and len(v) > _S.MAX_VALUE_LEN:
                raise _S.SchemaError(f"input_snapshot.{key}[{i}].value is too long")
            out.append(dict(e))
        return out

    def _worktree(key: str) -> dict[str, Any]:
        w = _S.req_map(_S.req_key(d, key, "input_snapshot"), f"input_snapshot.{key}")
        where = f"input_snapshot.{key}"
        _S.no_unknown_keys(w, WORKTREE_FIELDS, where)          # F6: exact worktree schema
        _S.req_str(w, "status", where, max_len=_S.MAX_ID_LEN)
        _S.req_str(w, "head", where, max_len=_S.MAX_ID_LEN, allow_empty=True)
        _S.req_str(w, "digest", where, max_len=_S.MAX_ID_LEN, allow_empty=True)
        _S.opt_bool_or_null(w, "dirty", where)
        _S.req_str_list(w, "problems", where, max_len=_S.MAX_PROBLEMS)
        return dict(w)

    def _str_map(key: str) -> dict[str, str]:
        m = _S.req_map(_S.req_key(d, key, "input_snapshot"), f"input_snapshot.{key}")
        out: dict[str, str] = {}
        for k, v in m.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise _S.SchemaError(f"input_snapshot.{key}: expects string->string")
            if len(v) > _S.MAX_VALUE_LEN:
                raise _S.SchemaError(f"input_snapshot.{key}.{k}: value too long")
            out[k] = v
        return out

    return InputSnapshot(
        remedy_git_sha=_S.req_str(d, "remedy_git_sha", "input_snapshot", max_len=_S.MAX_ID_LEN),
        remedy_dirty=_S.opt_bool_or_null(d, "remedy_dirty", "input_snapshot"),
        remedy_worktree=_worktree("remedy_worktree"),
        target_base_commit=_S.req_str(d, "target_base_commit", "input_snapshot",
                                      max_len=_S.MAX_ID_LEN),
        target_head=_S.req_str(d, "target_head", "input_snapshot", max_len=_S.MAX_ID_LEN),
        target_tree=_S.req_str(d, "target_tree", "input_snapshot", max_len=_S.MAX_ID_LEN,
                               allow_empty=True),
        target_worktree=_worktree("target_worktree"),
        job_initial_tree=_S.req_str(d, "job_initial_tree", "input_snapshot",
                                    max_len=_S.MAX_ID_LEN, allow_empty=True),
        episode_start_workspace_tree=_S.req_str(d, "episode_start_workspace_tree",
                                                "input_snapshot", max_len=_S.MAX_ID_LEN,
                                                allow_empty=True),
        episode_start_workspace_identity=_worktree("episode_start_workspace_identity"),
        job_file_sha256=_S.req_str(d, "job_file_sha256", "input_snapshot", max_len=64,
                                   allow_empty=True),
        job_input=decode_job_input_definition_v1(
            _S.req_key(d, "job_input", "input_snapshot")),      # F6/F7: its own exact schema
        models=_str_map("models"),
        provider_versions=_str_map("provider_versions"),
        config=_entries("config", _S.MAX_CONFIG_ENTRIES, {"key", "value", "source"}),
        environment=_entries("environment", _S.MAX_ENV_ENTRIES, {"key", "value"}),
        python_version=_S.req_str(d, "python_version", "input_snapshot",
                                  max_len=_S.MAX_ID_LEN, allow_empty=True),
        platform=_S.req_str(d, "platform", "input_snapshot", max_len=_S.MAX_SHORT_TEXT,
                            allow_empty=True),
        pythonhashseed=_S.req_str(d, "pythonhashseed", "input_snapshot",
                                  max_len=_S.MAX_ID_LEN, allow_empty=True),
    )


def decode_episode_snapshot_v1(raw: Any) -> "EpisodeInputSnapshotV1":
    """F4: strictly decode the episode-snapshot wrapper."""
    d = _S.req_map(raw, "episode_snapshot")
    _S.no_unknown_keys(d, {"snapshot_v", "episode_id", "captured_at", "capture_phase",
                           "status", "problems", "input"}, "episode_snapshot")
    raw_input = _S.req_key(d, "input", "episode_snapshot")
    return EpisodeInputSnapshotV1(
        snapshot_v=_S.req_int(d, "snapshot_v", "episode_snapshot", minimum=0, maximum=1000),
        episode_id=_S.req_str(d, "episode_id", "episode_snapshot", max_len=_S.MAX_ID_LEN),
        captured_at=_S.req_str(d, "captured_at", "episode_snapshot", max_len=_S.MAX_ID_LEN),
        capture_phase=_S.req_str(d, "capture_phase", "episode_snapshot",
                                 max_len=_S.MAX_ID_LEN),
        status=_S.req_str(d, "status", "episode_snapshot", max_len=_S.MAX_ID_LEN),
        problems=_S.req_str_list(d, "problems", "episode_snapshot", max_len=_S.MAX_PROBLEMS),
        input=None if raw_input is None else decode_input_snapshot_v1(raw_input),
    )


def decode_call_expectation_v1(raw: Any) -> "CallExpectationV1":
    """F6 (round 10): strictly decode the embedded call-expectation proof.

    The proof is only worth as much as its own schema: a vague or unknown expectation value
    would let a zero-call reference explain itself with a word nobody defined.
    """
    d = _S.req_map(raw, "manifest.call_expectation")
    _S.no_unknown_keys(d, {"expectation_v", "episode_phase", "tasks"},
                       "manifest.call_expectation")
    if _S.req_int(d, "expectation_v", "manifest.call_expectation", minimum=0,
                  maximum=1000) != 1:
        raise _S.SchemaError(
            f"unsupported expectation_v {d.get('expectation_v')!r}")
    phase = _S.req_str(d, "episode_phase", "manifest.call_expectation", max_len=_S.MAX_ID_LEN)
    if phase not in VALID_EPISODE_PHASES:
        raise _S.SchemaError(f"manifest.call_expectation.episode_phase {phase!r} is not a "
                             f"supported phase")
    tasks_raw = _S.req_list(d, "tasks", "manifest.call_expectation", max_len=_S.MAX_TASKS)
    tasks: list[TaskCallExpectationV1] = []
    for i, tk in enumerate(tasks_raw):
        where = f"manifest.call_expectation.tasks[{i}]"
        e = _S.req_map(tk, where)
        _S.no_unknown_keys(e, {"task_id", "expectation", "run_id", "expected_call_count",
                               "observed_call_count", "finalized_calls_sha256", "ledger_ref",
                               "task_status_at_finalization", "dispatch_state"}, where)
        exp = _S.req_str(e, "expectation", where, max_len=_S.MAX_ID_LEN)
        if exp not in VALID_TASK_EXPECTATIONS:
            raise _S.SchemaError(f"{where}.expectation {exp!r} is not a supported expectation")
        tasks.append(TaskCallExpectationV1(
            task_id=_S.req_str(e, "task_id", where, max_len=_S.MAX_ID_LEN),
            expectation=exp,
            run_id=_S.req_str(e, "run_id", where, max_len=_S.MAX_ID_LEN, allow_empty=True),
            expected_call_count=_S.req_int(e, "expected_call_count", where, minimum=0,
                                           maximum=_S.MAX_CALLS_PER_EPISODE),
            observed_call_count=_S.req_int(e, "observed_call_count", where, minimum=0,
                                           maximum=_S.MAX_CALLS_PER_EPISODE),
            finalized_calls_sha256=_S.req_str(e, "finalized_calls_sha256", where, max_len=64,
                                              allow_empty=True),
            ledger_ref=_S.req_str(e, "ledger_ref", where, max_len=_S.MAX_VALUE_LEN,
                                  allow_empty=True),
            task_status_at_finalization=_S.req_str(e, "task_status_at_finalization", where,
                                                   max_len=_S.MAX_ID_LEN, allow_empty=True),
            dispatch_state=_S.req_str(e, "dispatch_state", where, max_len=_S.MAX_ID_LEN)))
    return CallExpectationV1(episode_phase=phase, tasks=tuple(tasks))


def decode_run_manifest_v1(raw: Any) -> "RunManifestV1":
    """F4: THE strict decoder for an untrusted run-manifest record (bytes or parsed dict).

    Applies the size limit before parsing, requires real JSON types for every field, and
    refuses unknown fields — then hands the typed object to ``validate_run_manifest`` for the
    semantic invariants."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            _S.bounded_bytes(bytes(raw), _S.MAX_EPISODE_MANIFEST_BYTES, "run manifest")
        except _S.SchemaError as exc:
            raise ManifestError(f"run manifest: {exc}") from None
        try:
            raw = strict_json_loads(bytes(raw), where="run manifest")  # F11: no duplicate keys
        except _S.SchemaError as exc:
            raise ManifestError(f"run manifest: {exc}") from None
    try:
        d = _S.req_map(raw, "manifest")
        _S.no_unknown_keys(d, {"manifest_v", "job_id", "episode_id", "created_at", "status",
                               "episode_snapshot", "job_input_sha256", "calls", "coverage",
                               "call_expectation", "call_ledgers", "prior_episode_ids",
                               "episode_ordinal", "previous_episode_id",
                               "stop_request_id", "budgets"}, "manifest")
        if _S.req_int(d, "manifest_v", "manifest", minimum=0, maximum=1000) != MANIFEST_VERSION:
            raise ManifestError(
                f"unsupported manifest_v {d.get('manifest_v')!r} "
                f"(this build reads {MANIFEST_VERSION})")
        cov = _S.req_map(_S.req_key(d, "coverage", "manifest"), "manifest.coverage")
        _S.no_unknown_keys(cov, {"status", "problems"}, "manifest.coverage")
        calls_raw = _S.req_list(d, "calls", "manifest", max_len=_S.MAX_CALLS_PER_EPISODE)
        return RunManifestV1(
            job_id=_S.req_str(d, "job_id", "manifest", max_len=_S.MAX_ID_LEN),
            episode_id=_S.req_str(d, "episode_id", "manifest", max_len=_S.MAX_ID_LEN),
            created_at=_S.req_str(d, "created_at", "manifest", max_len=_S.MAX_ID_LEN),
            status=_S.req_str(d, "status", "manifest", max_len=_S.MAX_ID_LEN),
            episode_snapshot=decode_episode_snapshot_v1(
                _S.req_key(d, "episode_snapshot", "manifest")),
            job_input_sha256=_S.req_str(d, "job_input_sha256", "manifest", max_len=64),
            calls=tuple(sorted((decode_finalized_call_v1(c) for c in calls_raw),
                               key=lambda c: c.sort_key())),
            coverage=CallCoverage(
                status=_S.req_str(cov, "status", "manifest.coverage", max_len=_S.MAX_ID_LEN),
                problems=_S.req_str_list(cov, "problems", "manifest.coverage",
                                         max_len=_S.MAX_PROBLEMS)),
            call_expectation=decode_call_expectation_v1(
                _S.req_key(d, "call_expectation", "manifest")),
            call_ledgers=tuple(
                decode_run_call_ledger_v1(lg) for lg in
                _S.req_list(d, "call_ledgers", "manifest", max_len=_S.MAX_TASKS)),
            prior_episode_ids=_S.req_str_list(d, "prior_episode_ids", "manifest",
                                              max_len=_S.MAX_EPISODES,
                                              max_item_len=_S.MAX_ID_LEN),
            episode_ordinal=_S.req_int(d, "episode_ordinal", "manifest", minimum=0,
                                       maximum=_S.MAX_EPISODES),
            previous_episode_id=_S.req_str(d, "previous_episode_id", "manifest",
                                           max_len=_S.MAX_ID_LEN, allow_empty=True),
            stop_request_id=_S.req_str(d, "stop_request_id", "manifest",
                                       max_len=_S.MAX_ID_LEN, allow_empty=True),
            budgets=d.get("budgets"),
        )
    except _S.SchemaError as exc:
        raise ManifestError(f"manifest schema: {exc}") from None


def decode_index_v1(raw: Any) -> dict[str, Any]:
    """F4: strictly decode the manifest index."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            _S.bounded_bytes(bytes(raw), _S.MAX_INDEX_BYTES, "manifest index")
        except _S.SchemaError as exc:
            raise ManifestError(f"manifest index: {exc}") from None
        try:
            raw = strict_json_loads(bytes(raw), where="manifest index")  # F11: no duplicate keys
        except _S.SchemaError as exc:
            raise ManifestError(f"manifest index: {exc}") from None
    try:
        d = _S.req_map(raw, "index")
        _S.no_unknown_keys(d, {"index_v", "latest_episode_id", "episodes"}, "index")
        if _S.req_int(d, "index_v", "index", minimum=0, maximum=1000) != 1:
            raise ManifestError(f"unsupported index_v {d.get('index_v')!r}")
        eps = _S.req_list(d, "episodes", "index", max_len=_S.MAX_EPISODES)
        out_eps: list[dict[str, Any]] = []
        for i, e in enumerate(eps):
            em = _S.req_map(e, f"index.episodes[{i}]")
            _S.no_unknown_keys(em, {"episode_id", "status", "created_at", "episode_ordinal",
                                    "previous_episode_id", "record_sha256", "manifest_ref"},
                               f"index.episodes[{i}]")
            _S.req_str(em, "episode_id", f"index.episodes[{i}]", max_len=_S.MAX_ID_LEN)
            _S.req_int(em, "episode_ordinal", f"index.episodes[{i}]", minimum=0,
                       maximum=_S.MAX_EPISODES)
            out_eps.append(dict(em))
        return {"index_v": 1,
                "latest_episode_id": _S.req_str(d, "latest_episode_id", "index",
                                                max_len=_S.MAX_ID_LEN, allow_empty=True),
                "episodes": out_eps}
    except _S.SchemaError as exc:
        raise ManifestError(f"index schema: {exc}") from None


def _is_hex64(value: str) -> bool:
    v = str(value or "")
    return len(v) == 64 and all(c in "0123456789abcdef" for c in v)


#: The established redaction markers a value carries once it HAS been through the accepted
#: redactor (`failure_postmortem.safe_text` / F007's path scrubber). They are references, not
#: leaks — but they are neutralised before probing so a crafted "[path] /home/x" cannot hide a
#: raw path behind a marker.
_REDACTION_MARKERS = (REDACTED, "[runtime-data]", "[path]")


def _probe_text(value: str) -> str:
    probe = value
    for marker in _REDACTION_MARKERS:
        probe = probe.replace(marker, "M")
    return probe


def _contains_secret(value: str) -> bool:
    """F5: reuse the ESTABLISHED secret redactor as the detector — if redacting the value
    changes it, the value still carried a RAW secret. No weaker regex is invented here."""
    if not isinstance(value, str) or not value:
        return False
    try:
        from packages.orchestration.stream_evidence import redact_text
        probe = _probe_text(value)
        return redact_text(probe) != probe
    except Exception:
        return False


def _contains_local_path(value: str) -> bool:
    """F5: reuse the ESTABLISHED path scrubber (F007's accepted detector, via ``safe_text``) —
    if scrubbing the marker-neutralised value changes it, a RAW local/home/temp path is still
    present. An already-redacted reference such as ``[runtime-data]/jobs/x`` is a reference and
    stays safe."""
    if not isinstance(value, str) or not value:
        return False
    try:
        from packages.orchestration.failure_postmortem import safe_text
        probe = _probe_text(value)
        return safe_text(probe) != probe
    except Exception:
        return value.startswith("/") or value.startswith("~/")


#: The provider transport modes a PreparedCallInput may declare (F7).
VALID_CALL_MODES = frozenset({"api-structured", "api-legacy", "cli-native", "cli-legacy",
                              "fake"})
#: F8: the EXACT PreparedCallInput field set — one definition used by the decoder and the
#: validator so no boundary can silently accept an extra field.
PREPARED_CALL_INPUT_FIELDS = frozenset({"prompt_sha256", "prompt_len_bytes", "schema_sha256",
                                        "model", "mode", "options_sha256", "fingerprint"})
VALID_CALL_ROLES = frozenset({"builder", "reviewer"})
VALID_CALL_KINDS = frozenset({"attempt", "parse-retry"})
VALID_FINGERPRINT_SOURCES = frozenset({"provider_transport", "loop_fallback"})


def validate_prepared_call_input(raw: Any, *, where: str = "prepared_input") -> list[str]:
    """F7: strict PreparedCallInput validation — and the fingerprint BINDING.

    The recorded ``fingerprint`` must be exactly the transport fingerprint RECOMPUTED from the
    recorded components, so a tampered fingerprint (or tampered components) is rejected. The
    original prompt bytes are never required — only the internally recorded components."""
    problems: list[str] = []
    if not isinstance(raw, dict):
        return [f"{where} is not an object"]
    # F8: EXACT field set at EVERY boundary — provider-produced, persisted run JSON, manifest
    # decode, artifact validation, recovery and export all apply this same check.
    extra = sorted(set(raw) - PREPARED_CALL_INPUT_FIELDS)
    if extra:
        problems.append(f"{where} carries unknown field(s) {extra}")
    missing = sorted(PREPARED_CALL_INPUT_FIELDS - set(raw))
    if missing:
        problems.append(f"{where} is missing {missing}")
        return problems
    if not _is_hex64(raw.get("prompt_sha256", "")):
        problems.append(f"{where}.prompt_sha256 is not 64 lowercase hex")
    plen = raw.get("prompt_len_bytes")
    if isinstance(plen, bool) or not isinstance(plen, int) or plen < 0 \
            or plen > 64 * 1024 * 1024:
        problems.append(f"{where}.prompt_len_bytes is not a bounded non-negative integer")
    for f in ("model", "mode"):
        v = raw.get(f)
        if isinstance(v, str) and (_contains_secret(v) or _contains_local_path(v)
                                   or _S.has_control_chars(v)):
            problems.append(f"{where}.{f} carries a secret/path/control character")
    schema_sha = raw.get("schema_sha256", "")
    if schema_sha and not _is_hex64(schema_sha):
        problems.append(f"{where}.schema_sha256 must be empty or 64 lowercase hex")
    model = raw.get("model", "")
    if not isinstance(model, str) or not model or len(model) > _S.MAX_ID_LEN:
        problems.append(f"{where}.model is empty or unbounded")
    if raw.get("mode") not in VALID_CALL_MODES:
        problems.append(f"{where}.mode {raw.get('mode')!r} is not a supported transport mode")
    if not _is_hex64(raw.get("options_sha256", "")):
        problems.append(f"{where}.options_sha256 is not 64 lowercase hex")
    fp = raw.get("fingerprint", "")
    if not _is_hex64(fp):
        problems.append(f"{where}.fingerprint is not 64 lowercase hex")
    if problems:
        return problems
    # The binding: recompute the transport fingerprint from the recorded components.
    recomputed = hashlib.sha256(json.dumps({
        "prompt_sha256": raw["prompt_sha256"],
        "prompt_len_bytes": raw["prompt_len_bytes"],     # F9: bound into the fingerprint
        "schema_sha256": raw.get("schema_sha256", ""),
        "model": raw["model"],
        "mode": raw["mode"],
        "options_sha256": raw["options_sha256"],
    }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if recomputed != fp:
        problems.append(f"{where}.fingerprint does not match its recorded components")
    return problems


#: F4 (round 14): THE closed canonical call-ref grammar.
#:
#: A call ref is the identity F010's post-mortems, F012's manifests and F140's replay all use to
#: name the same call, so "not absolute" was never enough — `calls//builder`, `calls/./builder`,
#: `calls/builder/` and `home/alice` all passed, and none of them names a call. Production emits
#: exactly two shapes, verified by running it (`shared_call_id`, `_allocate_stream_call_dir`, and
#: F010's committed layouts):
#:
#:     calls/<role>/round-NN/<kind>              — fallback / fake provider calls
#:     streams/<role>/round-NN/<kind>-II         — streamed CLI provider calls (F004/F010)
#:
#: Both encode role, round and kind, so the ref is not merely well-formed: it must AGREE with the
#: CallIdentity it belongs to. `rel_prefix = f"streams/{role}"` is set whenever streaming is on,
#: so the namespace is never empty in production.
CALL_REF_NAMESPACES = frozenset({"calls", "streams"})
CALL_REF_SEGMENTS = 4
MAX_CALL_REF_SEGMENT_LEN = 64
_ROUND_SEGMENT_RE = None
_STREAM_INDEX_RE = None


def _call_ref_res():
    global _ROUND_SEGMENT_RE, _STREAM_INDEX_RE
    if _ROUND_SEGMENT_RE is None:
        import re
        # The digits are extracted here and CANONICALITY is decided by
        # `parse_canonical_call_number` — one rule, shared with the generators.
        _ROUND_SEGMENT_RE = re.compile(r"^round-(\d{1,6})$")
        _STREAM_INDEX_RE = re.compile(r"^(\d{1,6})$")
    return _ROUND_SEGMENT_RE, _STREAM_INDEX_RE


def canonical_call_ref(*, namespace: str, role: str, round: int, kind: str,
                       index: int | None = None) -> str:
    """Build a call ref from its parts, in the one canonical spelling.

    F2 (round 15): the reconstruction `parse_call_ref` compares against, and the same function the
    generators' format is pinned to — so "what production writes" and "what the validator accepts"
    are one definition rather than two that happen to agree today.
    """
    last = kind if index is None else f"{kind}-{canonical_call_number(index)}"
    return f"{namespace}/{role}/round-{canonical_call_number(round)}/{last}"


def parse_call_ref(cid: str) -> tuple[dict | None, list[str]]:
    """Decompose a call ref under the closed grammar. Returns (fields, problems).

    `fields` carries the role/round/kind the ref ENCODES, so the caller can hold the ref and its
    CallIdentity to each other rather than trusting either alone.
    """
    problems: list[str] = []
    cid = cid or ""
    if not cid:
        return None, ["call ref is empty"]
    if len(cid) > _S.MAX_ID_LEN:
        return None, [f"call ref is longer than {_S.MAX_ID_LEN} bytes"]
    if _S.has_control_chars(cid):
        return None, ["call ref carries a control character"]
    if "\\" in cid:
        return None, ["call ref carries a backslash (POSIX relative form only)"]
    if cid.startswith("/") or cid.startswith("~"):
        return None, ["call ref is absolute or home-relative (relative POSIX form only)"]
    if _contains_secret(cid) or _contains_local_path(cid):
        return None, ["call ref carries a raw secret or local path"]

    segments = cid.split("/")
    if len(segments) != CALL_REF_SEGMENTS:
        return None, [f"call ref has {len(segments)} segment(s); the canonical form has "
                      f"{CALL_REF_SEGMENTS}: <namespace>/<role>/round-NN/<kind>"]
    for seg in segments:
        if not seg:
            return None, ["call ref has an empty segment (no repeated or trailing slash)"]
        if seg in (os.curdir, os.pardir):
            return None, [f"call ref has a {seg!r} segment"]
        if len(seg) > MAX_CALL_REF_SEGMENT_LEN:
            return None, [f"call ref segment {seg[:20]!r} exceeds "
                          f"{MAX_CALL_REF_SEGMENT_LEN} bytes"]

    namespace, role, round_seg, last = segments
    if namespace not in CALL_REF_NAMESPACES:
        problems.append(f"call ref namespace {namespace!r} is not one of "
                        f"{sorted(CALL_REF_NAMESPACES)}")
    if role not in VALID_CALL_ROLES:
        problems.append(f"call ref role {role!r} is not a supported role")
    round_re, index_re = _call_ref_res()
    m = round_re.match(round_seg)
    round_no = 0
    if not m:
        problems.append(f"call ref round segment {round_seg!r} is not `round-NN`")
    else:
        # F2 (round 15): CANONICAL text, not merely a readable number. `int()` reads `01`, `001`
        # and `000001` as the same round, which handed one call three names.
        parsed = parse_canonical_call_number(m.group(1))
        if parsed is None:
            problems.append(
                f"call ref round segment {round_seg!r} is not the canonical spelling of its "
                f"round (one round has exactly one text form: 1 -> 01, 10 -> 10, 100 -> 100)")
        else:
            round_no = parsed

    kind, index = last, None
    if namespace == "streams":
        # `parse-retry-03` — the kind itself contains a dash, so split on the LAST one.
        head, sep, tail = last.rpartition("-")
        if not sep or not index_re.match(tail):
            problems.append(f"streamed call ref {last!r} does not end in the attempt index "
                            f"`<kind>-II` the streaming layout assigns")
        else:
            parsed_idx = parse_canonical_call_number(tail)
            if parsed_idx is None:
                problems.append(
                    f"streamed call ref {last!r} does not carry the canonical spelling of its "
                    f"attempt index (index 0 is not a call, and 001 is not a spelling of 01)")
            else:
                kind, index = head, parsed_idx
    if kind not in VALID_CALL_KINDS:
        problems.append(f"call ref kind {kind!r} is not a supported kind")
    if problems:
        return None, problems
    if round_no > MAX_LEDGER_ROUND or (index is not None and index > MAX_LEDGER_SEQUENCE):
        return None, [f"call ref round/index is outside the configured bounds"]
    # THE canonicality test: the ref must be exactly what its own parts rebuild. Anything that
    # merely parses to the same numbers — a different padding, a stray form — is a different
    # string claiming to be this call, and is refused here rather than somewhere downstream.
    rebuilt = canonical_call_ref(namespace=namespace, role=role, round=round_no, kind=kind,
                                 index=index)
    if rebuilt != cid:
        return None, [f"call ref {cid!r} is not canonical; its canonical form is {rebuilt!r}"]
    return {"namespace": namespace, "role": role, "round": round_no,
            "kind": kind, "index": index}, []


def safe_call_ref(cid: str) -> bool:
    """True when the ref satisfies the closed canonical grammar (shape only)."""
    fields, problems = parse_call_ref(cid)
    return fields is not None and not problems


def validate_call_ref(cid: str, *, role: str, round: int, kind: str,
                      where: str = "call") -> list[str]:
    """THE call-ref rule — one definition, used by the CallIdentity validator AND the ledger.

    Beyond the grammar: the ref ENCODES role, round and kind, so it must agree with the identity
    it is attached to. A ref that says `builder/round-01/attempt` on a call recorded as the
    reviewer's round-2 parse retry is two accounts of one call disagreeing, which is the same
    class of defect F3 (round 13) closed for `ok`.
    """
    fields, problems = parse_call_ref(cid)
    if fields is None:
        return [f"{where}.call_id {str(cid)[:60]!r}: {p}" for p in problems]
    if fields["role"] != role:
        problems.append(f"{where}.call_id names role {fields['role']!r} but the call is "
                        f"{role!r}'s")
    if fields["round"] != round:
        problems.append(f"{where}.call_id names round {fields['round']} but the call is round "
                        f"{round}")
    if fields["kind"] != kind:
        problems.append(f"{where}.call_id names kind {fields['kind']!r} but the call is "
                        f"{kind!r}")
    return problems


def validate_call_identity(ident: CallIdentity, *, where: str = "call") -> list[str]:
    """F9: every identity component is strict, bounded and PATH-SAFE — artifact names are built
    only from validated values, so ``role="../evil"`` can never reach a filename."""
    problems: list[str] = []
    for f in ("job_id", "task_id", "run_id"):
        v = getattr(ident, f, "")
        if not _safe_component(v):
            problems.append(f"{where}.{f} {v!r} is not a safe bounded component")
    # The call_id is a path-SHAPED reference — validated by THE shared rule (F8, round 13; the
    # closed grammar of F4, round 14), the same one the ledger uses, so the two can never drift
    # apart, and held to the role/round/kind it encodes.
    problems.extend(validate_call_ref(ident.call_id or "", role=ident.role, round=ident.round,
                                      kind=ident.kind, where=where))
    if ident.episode_id and not _safe_component(ident.episode_id):
        problems.append(f"{where}.episode_id {ident.episode_id!r} is not safe")
    if ident.role not in VALID_CALL_ROLES:
        problems.append(f"{where}.role {ident.role!r} is not a supported role")
    if ident.kind not in VALID_CALL_KINDS:
        problems.append(f"{where}.kind {ident.kind!r} is not a supported kind")
    if isinstance(ident.round, bool) or not isinstance(ident.round, int) or ident.round < 1:
        problems.append(f"{where}.round must be a positive integer")
    if isinstance(ident.sequence, bool) or not isinstance(ident.sequence, int) \
            or ident.sequence < 1:
        problems.append(f"{where}.sequence must be a positive integer")
    return problems


def canonical_artifact_ref(ident: CallIdentity) -> str:
    """F8/F9: THE artifact naming contract, built only from validated identity values."""
    return (f"{CALLS_SUBDIR}/{ident.sequence:04d}-{ident.role}-"
            f"round{ident.round:02d}-{ident.kind}.json")


def _is_utc_timestamp(value: str) -> bool:
    try:
        dt = datetime.fromisoformat(str(value))
    except (ValueError, TypeError):
        return False
    if dt.tzinfo is None:
        return False
    return dt.utcoffset() == timedelta(0)


def _is_safe_request_id(value: str) -> bool:
    try:
        from packages.orchestration.safe_points import is_safe_id
        return bool(is_safe_id(value))
    except Exception:
        v = str(value or "")
        return bool(v) and len(v) <= 64 and "/" not in v and ".." not in v and " " not in v


#: F8: a safe key — bounded, no separators/traversal/control characters, no path or secret.
_SAFE_KEY_RE = None


def _is_safe_key(key: Any, *, allow_dots: bool = True) -> bool:
    global _SAFE_KEY_RE
    if _SAFE_KEY_RE is None:
        import re
        _SAFE_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}$")
    if not isinstance(key, str) or not key or len(key) > _S.MAX_ID_LEN:
        return False
    if not allow_dots and "." in key:
        return False
    if "/" in key or "\\" in key or ".." in key or _S.has_control_chars(key):
        return False
    if _contains_secret(key) or _contains_local_path(key):
        return False
    return bool(_SAFE_KEY_RE.match(key))


def _valid_pythonhashseed(value: Any) -> bool:
    """F8: PYTHONHASHSEED is not free text. Python accepts ``random`` or an integer in
    [0, 4294967295]; unset is represented as the empty string."""
    if value in ("", None):
        return True
    if not isinstance(value, str) or len(value) > 16:
        return False
    if value == "random":
        return True
    return value.isdigit() and 0 <= int(value) <= 4294967295


def validate_input_snapshot(snap: "InputSnapshot") -> list[str]:
    """F5/F7: strict typed validation of the InputSnapshot payload. No normalization.

    Enforces what the schema CLAIMS: both worktree records carry every required field with an
    explicit supported status; the redundant facts agree (``remedy_dirty`` vs
    ``remedy_worktree.dirty``, the sha/head and head/digest pairs); and no config, environment,
    provider-version, model or platform value may carry a raw secret, an absolute/home/temp
    local path, or a control character. Secret-like keys must carry EXACTLY the redaction
    marker. The established redactor + F007 path detector are reused as the detectors."""
    problems: list[str] = []

    def _check_worktree(label: str, wt: dict[str, Any]) -> None:
        wt = wt or {}
        # F5: required fields — an empty/missing status is NOT acceptable.
        for f in ("status", "head", "digest", "dirty", "problems"):
            if f not in wt:
                problems.append(f"{label} worktree is missing required field {f!r}")
        status = wt.get("status", "")
        if status not in (GIT_OK, GIT_UNAVAILABLE, GIT_INCOMPLETE):
            problems.append(f"{label} worktree status {status!r} not allowed")
        dirty = wt.get("dirty", None)
        if dirty is not None and not isinstance(dirty, bool):
            problems.append(f"{label} worktree dirty is not bool/null")
        if status == GIT_OK and dirty is None:
            problems.append(f"{label} worktree ok but dirty is null")
        if status in (GIT_UNAVAILABLE, GIT_INCOMPLETE) and dirty is not None:
            problems.append(f"{label} worktree {status} but dirty is not null")
        probs = wt.get("problems", [])
        if not isinstance(probs, list):
            problems.append(f"{label} worktree problems is not a list")
        else:
            if len(probs) > _S.MAX_PROBLEMS:
                problems.append(f"{label} worktree declares too many problems")
            for pr in probs:
                if not isinstance(pr, str) or len(pr) > _S.MAX_PROBLEM_LEN:
                    problems.append(f"{label} worktree problem is not a bounded string")
                elif _contains_local_path(pr) or _contains_secret(pr):
                    problems.append(f"{label} worktree problem leaks a path/secret")

    rwt = snap.remedy_worktree or {}
    twt = snap.target_worktree or {}
    _check_worktree("remedy", rwt)
    _check_worktree("target", twt)

    # F5: redundant facts must AGREE — a contradiction is never tolerated silently.
    if snap.remedy_dirty != rwt.get("dirty", None):
        problems.append("remedy_dirty contradicts remedy_worktree.dirty")
    if snap.remedy_git_sha and snap.remedy_git_sha != UNAVAILABLE \
            and rwt.get("head") not in (None, "", UNAVAILABLE) \
            and snap.remedy_git_sha != rwt.get("head"):
        problems.append("remedy_git_sha contradicts remedy_worktree.head")
    if snap.target_head and snap.target_head != UNAVAILABLE \
            and twt.get("head") not in (None, "", UNAVAILABLE) \
            and snap.target_head != twt.get("head"):
        problems.append("target_head contradicts target_worktree.head")
    # target_tree is the target worktree's strict CONTENT digest; it must equal the recorded
    # digest whenever the identity is ok (it is UNAVAILABLE otherwise).
    if twt.get("status") == GIT_OK and snap.target_tree not in (UNAVAILABLE, "") \
            and twt.get("digest") and snap.target_tree != twt.get("digest"):
        problems.append("target_tree contradicts target_worktree.digest")

    for label, val in (("target_base_commit", snap.target_base_commit),
                       ("target_head", snap.target_head),
                       ("remedy_git_sha", snap.remedy_git_sha)):
        if val and val != UNAVAILABLE and not _is_sha(val):
            problems.append(f"{label} is neither a git sha nor {UNAVAILABLE!r}")
    for label, val in (("target_tree", snap.target_tree),
                       ("job_initial_tree", snap.job_initial_tree),
                       ("episode_start_workspace_tree", snap.episode_start_workspace_tree)):
        # a git tree object is 40-hex; the strict worktree digest is a 64-hex sha256.
        if val and val != UNAVAILABLE and not (_is_sha(val) or _is_hex64(val)):
            problems.append(f"{label} is neither a tree sha/digest nor {UNAVAILABLE!r}")
    if snap.job_file_sha256 and not _is_hex64(snap.job_file_sha256):
        problems.append("job_file_sha256 is not 64 lowercase hex")

    def _safe_value(what: str, key: str, value: Any) -> None:
        """F5: one safety gate for every externally-visible value."""
        if value is None or value == REDACTED:
            return
        if not isinstance(value, str):
            value = str(value)
        if len(value) > _S.MAX_VALUE_LEN:
            problems.append(f"{what} {key!r} value exceeds the length limit")
            return
        if _S.has_control_chars(value):
            problems.append(f"{what} {key!r} value contains control characters")
        if _contains_secret(value):
            problems.append(f"{what} {key!r} carries a raw secret value")
        if _contains_local_path(value):
            problems.append(f"{what} {key!r} carries a local path")

    def _keys_unique(entries: list[dict[str, Any]], what: str) -> None:
        keys = [str(e.get("key", "")) for e in entries]
        if len(keys) != len(set(keys)):
            problems.append(f"duplicate {what} keys")

    _keys_unique(snap.config, "config")
    _keys_unique(snap.environment, "environment")
    if len(snap.config) > _S.MAX_CONFIG_ENTRIES:
        problems.append("config exceeds the entry limit")
    if len(snap.environment) > _S.MAX_ENV_ENTRIES:
        problems.append("environment exceeds the entry limit")

    for e in snap.config:
        k = str(e.get("key", ""))
        v = e.get("value")
        src = e.get("source")
        if not _is_safe_key(k):                      # F8: KEYS are validated, not only values
            problems.append(f"config key {k!r} is not a safe bounded key")
        if src is not None and src not in _VALID_SOURCES:
            problems.append(f"config {k!r} has an invalid source {src!r}")
        # F5: a secret-like key must carry EXACTLY the redaction marker, never a raw value.
        if is_secret_key(k) and v is not None and v != REDACTED:
            problems.append(f"config {k!r} is secret-like but is not redacted")
        _safe_value("config", k, v)

    for e in snap.environment:
        k = str(e.get("key", ""))
        v = e.get("value")
        if k and not k.startswith("REMEDY_") and k != "PYTHONHASHSEED":
            problems.append(f"environment carries a non-REMEDY_ key {k!r}")
        elif not _is_safe_key(k, allow_dots=False):  # F8: safe bounded env key
            problems.append(f"environment key {k!r} is not a safe bounded key")
        if is_secret_key(k) and v is not None and v != REDACTED:
            problems.append(f"environment {k!r} is secret-like but is not redacted")
        _safe_value("environment", k, v)

    for role, model in (snap.models or {}).items():
        if not _is_safe_key(role):                   # F8: model ROLE keys
            problems.append(f"models key {role!r} is not a safe bounded key")
        _safe_value("models", str(role), model)
    for prov, ver in (snap.provider_versions or {}).items():
        if not _is_safe_key(prov):                   # F8: provider-version keys
            problems.append(f"provider_versions key {prov!r} is not a safe bounded key")
        _safe_value("provider_versions", str(prov), ver)
    # F8: PYTHONHASHSEED is a bounded vocabulary, never arbitrary free text.
    if not _valid_pythonhashseed(snap.pythonhashseed):
        problems.append(f"pythonhashseed {snap.pythonhashseed!r} is not a valid seed value")
    _safe_value("platform", "platform", snap.platform)
    _safe_value("python_version", "python_version", snap.python_version)

    # F11: bounds, applied exactly as the exporter will.
    try:
        if len(_fs.json_bytes(snap.to_json(), sort_keys=True)) > _S.MAX_INPUT_SNAPSHOT_BYTES:
            problems.append("input snapshot payload is oversized")
    except Exception:
        problems.append("input snapshot is not canonically serializable")
    if isinstance(snap.job_input, dict) and int(snap.job_input.get("job_input_v", 0) or 0) != 1:
        problems.append("unsupported job_input version")

    # F7: every fact recorded TWICE must agree. A contradiction between the snapshot's scalar
    # view and the typed job-input definition is an integrity error, never a silent preference.
    ji = snap.job_input if isinstance(snap.job_input, dict) else {}
    ji_file = str(ji.get("job_file_sha256", "") or "")
    if ji_file and snap.job_file_sha256 and ji_file != snap.job_file_sha256:
        problems.append("job_file_sha256 contradicts job_input.job_file_sha256")
    ex = ji.get("execution") if isinstance(ji.get("execution"), dict) else {}
    problems.extend(validate_models(snap.models, ex))
    return problems


#: F9 (round 10): the EXACT `models` role vocabulary. Builder and Reviewer always run; Repair is
#: recorded ONLY when a repair provider/model is actually configured (see `_models_for_job`).
REQUIRED_MODEL_ROLES = ("builder", "reviewer")
OPTIONAL_MODEL_ROLES = ("repair",)


def _declared_role_provider(ex: dict[str, Any], role: str) -> str:
    """The provider the EMBEDDED execution definition declares for a role.

    Repair falls back to the builder's provider when only a repair MODEL is pinned — that is
    what production records, so it is what agreement is checked against.
    """
    if role == "repair":
        return str(ex.get("repair_provider") or ex.get("builder") or "")
    return str(ex.get(role) or "")


def _declared_role_model(ex: dict[str, Any], role: str) -> str:
    return str(ex.get("repair_model") if role == "repair" else ex.get(f"{role}_model") or "")


def validate_models(models: Any, ex: dict[str, Any]) -> list[str]:
    """F9 (round 10): the `models` map is an EXACT schema, and every role it names must agree
    with the embedded Execution definition.

    `models[role]` is the scalar view ("<provider>", or "<provider>/<model>" when a model is
    pinned); the definition records the same facts separately. Both describe ONE role, so a
    contradiction means at most one of them is the input that actually ran — an integrity error,
    never a preference. Absence is explicit: Builder and Reviewer are always recorded; Repair is
    recorded exactly when the definition activates a repair provider/model.
    """
    problems: list[str] = []
    if not isinstance(models, dict):
        return ["models is not an object"]
    if not isinstance(ex, dict) or not ex:
        return problems               # no definition to agree with; other rules report that

    known = set(REQUIRED_MODEL_ROLES) | set(OPTIONAL_MODEL_ROLES)
    for role in sorted(set(models) - known):
        problems.append(f"models has unknown role {role!r}")
    # ABSENCE IS SYMMETRIC: a role appears in `models` exactly when the definition declares a
    # provider for it. A planning-only job has no execution config, so it declares no providers
    # and records no models — and that agreement is itself the check (T0_F012: "Planning-only
    # job (zero calls): valid manifest").
    for role in REQUIRED_MODEL_ROLES:
        declared = str(ex.get(role) or "").strip()
        recorded = str(models.get(role, "") or "").strip()
        if declared and not recorded:
            problems.append(f"models is missing the required role {role!r}, which "
                            f"job_input.execution declares as {declared!r}")
        elif recorded and not declared:
            problems.append(f"models records the role {role!r} but job_input.execution "
                            f"declares no provider for it")

    repair_active = bool(str(ex.get("repair_provider") or "").strip()
                         or str(ex.get("repair_model") or "").strip())
    if repair_active and not str(models.get("repair", "") or ""):
        problems.append("job_input.execution activates a repair provider/model but models "
                        "records no repair role")
    if not repair_active and "repair" in models:
        problems.append("models records a repair role that job_input.execution does not "
                         "activate")

    for role in sorted(set(models) & known):
        recorded = str(models.get(role, "") or "")
        if not recorded:
            continue
        provider_part, _, model_part = recorded.partition("/")
        declared_provider = _declared_role_provider(ex, role)
        if declared_provider and provider_part != declared_provider:
            problems.append(f"models.{role} provider contradicts "
                            f"job_input.execution.{'repair_provider' if role == 'repair' else role}")
        declared_model = _declared_role_model(ex, role)
        # An UNSET declared model means "the provider's default" — there is no second fact to
        # contradict. A pinned model must match what the scalar view recorded.
        if declared_model and model_part != declared_model:
            problems.append(f"models.{role} contradicts job_input.execution.{role}_model")
    return problems


def _require_valid_manifest(manifest: "RunManifestV1", where: str, *,
                            published: bool = True, mode: str | None = None) -> None:
    probs = validate_run_manifest(manifest, published=published, mode=mode)
    if probs:
        raise ManifestError(f"invalid run manifest ({where}): {'; '.join(probs)[:400]}")


def _assert_unique_calls(calls: list[FinalizedCall]) -> None:
    seen: set[tuple] = set()
    for c in calls:
        k = c.identity.key()
        if k in seen:
            raise ManifestError(f"duplicate call identity in manifest: {k}")
        seen.add(k)


def build_run_manifest(job: Any, *, status: str, episode_id: str, created_at: str,
                       episode_snapshot: "EpisodeInputSnapshotV1 | None" = None,
                       prior_episode_ids: tuple[str, ...] = (),
                       owned_episode_id: str = "",
                       prior_episode_ordinals: dict[str, int] | None = None,
                       episode_ordinal: int = 1,
                       previous_episode_id: str = "",
                       stop_request_id: str = "") -> RunManifestV1:
    # F1/F4: NO terminal re-probe. The episode-start snapshot WRAPPER is REQUIRED and must be a
    # valid ``ok`` snapshot bound to THIS episode; a caller that lost it (a failed capture) must
    # surface that as blocking, not rebuild a fresh one at the end.
    if episode_snapshot is None:
        raise ManifestError(
            "cannot build a run manifest without the episode-start input snapshot "
            "(F1: the finalizer never re-probes a fresh snapshot at episode end)")
    snap_problems = validate_episode_input_snapshot(episode_snapshot,
                                                    expected_episode_id=episode_id)
    if snap_problems or not episode_snapshot.is_ok():
        raise ManifestError(
            "the episode-start snapshot is invalid or a failed capture (F1/F4/F6): "
            + "; ".join(snap_problems or list(episode_snapshot.problems))[:300])
    snap = episode_snapshot.input
    # F7 (round 10): the task list a Call is bound to comes from the IMMUTABLE embedded
    # definition, never from the live `job.tasks` list — the JobPlan is mutable and may have
    # been re-planned since this episode's snapshot was captured.
    declared_task_ids = tuple(
        str(tk.get("task_id", "")) for tk in (snap.job_input.get("tasks") or [])
        if isinstance(tk, dict))
    # F7: and if live state HAS moved on, finalizing against it would silently record work the
    # snapshot never described. That is a blocking contradiction, not a merge.
    live_task_ids = tuple(str(getattr(tk, "task_id", "") or "")
                          for tk in getattr(job, "tasks", []))
    if declared_task_ids and live_task_ids and live_task_ids != declared_task_ids:
        raise ManifestError(
            f"the job's task list {list(live_task_ids)} no longer matches the episode-start "
            f"snapshot's job-input definition {list(declared_task_ids)} (F7: tasks were added, "
            f"removed or reordered after capture; this episode cannot be finalized against a "
            f"definition it did not run)")
    # F6 (round 10): a pre-work stop and a planning-only job are the two phases that genuinely
    # expect zero calls. The phase is read from the snapshot's own capture phase and the
    # terminal status — both immutable facts of this record.
    # F7 (round 11): the phase is read from the snapshot's own capture phase — the immutable
    # fact of HOW this episode was captured — never guessed from the status.
    capture = getattr(episode_snapshot, "capture_phase", "")
    if capture == PHASE_PRE_WORK_STOP:
        phase = PHASE_PRE_WORK_STOP
    elif capture == PHASE_PLANNING_ONLY:
        phase = PHASE_PLANNING_ONLY
    else:
        phase = PHASE_WORKED
    calls, problems, expectation, ledgers = _collect_calls(
        job, owned_episode_id=owned_episode_id, manifest_episode_id=episode_id,
        declared_task_ids=declared_task_ids,
        prior_episode_ordinals=prior_episode_ordinals,
        prior_episode_ids=tuple(prior_episode_ids),
        episode_ordinal=int(episode_ordinal),
        episode_phase=phase)
    _assert_unique_calls(calls)
    coverage = CallCoverage(
        status=COVERAGE_COMPLETE if not problems else COVERAGE_INCOMPLETE,
        problems=tuple(sorted(problems)))
    return RunManifestV1(
        job_id=str(getattr(job, "job_id", "")),
        episode_id=episode_id,
        created_at=created_at,
        status=status,
        episode_snapshot=episode_snapshot,
        # F6: the hash is bound to the EMBEDDED, episode-start job-input definition — never
        # recomputed from live job state, whose resolved sources may have shifted since capture.
        job_input_sha256=job_input_definition_sha256(snap.job_input),
        calls=tuple(calls),
        coverage=coverage,
        call_expectation=expectation,
        call_ledgers=ledgers,
        prior_episode_ids=tuple(prior_episode_ids),
        episode_ordinal=int(episode_ordinal),
        previous_episode_id=str(previous_episode_id or ""),
        stop_request_id=str(stop_request_id or ""),
    )


# ---------------------------------------------------------------------------
# Write (episode dir + call artifacts + index), exactly-once
# ---------------------------------------------------------------------------


def episode_dir_name(episode_id: str) -> str:
    from packages.orchestration.safe_points import validate_job_id

    return validate_job_id(episode_id)


def _identity_ok(existing: dict[str, Any], payload: dict[str, Any]) -> bool:
    def strip(d: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in d.items() if k != "created_at"}

    return strip(existing) == strip(payload)


def _bind_artifact_refs(manifest: RunManifestV1) -> RunManifestV1:
    calls_with_refs: list[FinalizedCall] = []
    for c in sorted(manifest.calls, key=lambda c: c.sort_key()):
        artifact_rel = f"{CALLS_SUBDIR}/{c.identity.sequence:04d}-{c.identity.role}-" \
                       f"round{c.identity.round:02d}-{c.identity.kind}.json"
        bound = FinalizedCall(
            identity=c.identity, fingerprint=c.fingerprint,
            prepared_input=c.prepared_input, fingerprint_source=c.fingerprint_source,
            ok=c.ok, artifact=artifact_rel)
        calls_with_refs.append(FinalizedCall(
            identity=bound.identity, fingerprint=bound.fingerprint,
            prepared_input=bound.prepared_input, fingerprint_source=bound.fingerprint_source,
            ok=bound.ok, artifact=artifact_rel,
            artifact_sha256=hashlib.sha256(bound.canonical_artifact_bytes()).hexdigest()))
    return RunManifestV1(
        job_id=manifest.job_id, episode_id=manifest.episode_id,
        created_at=manifest.created_at, status=manifest.status,
        episode_snapshot=manifest.episode_snapshot,
        job_input_sha256=manifest.job_input_sha256, calls=tuple(calls_with_refs),
        coverage=manifest.coverage,
        # F6: binding artifact refs changes WHERE the inputs are stored, never what this
        # episode expected — the proof travels through untouched.
        call_expectation=manifest.call_expectation,
        call_ledgers=manifest.call_ledgers,
        prior_episode_ids=manifest.prior_episode_ids,
        episode_ordinal=manifest.episode_ordinal,
        previous_episode_id=manifest.previous_episode_id,
        stop_request_id=manifest.stop_request_id)


def _decode_existing_episode(raw: bytes, episode_id: str) -> RunManifestV1:
    """F3: read an ALREADY-STORED episode strictly. Malformed, noncanonical or invalid stored
    bytes are a ``ManifestConflictError`` — the writer never silently accepts a record its own
    canonical loader would reject."""
    try:
        existing = decode_run_manifest_v1(raw)
        require_canonical_bytes(raw, existing, where=f"episode {episode_id}")
        _require_valid_manifest(existing, f"existing episode {episode_id}",
                                mode=MODE_PUBLISHED_REFERENCE)
    except (ManifestError, _S.SchemaError) as exc:
        raise ManifestConflictError(
            f"an unreadable or noncanonical run manifest already exists for episode "
            f"{episode_id!r}: {exc}") from None
    return existing


#: F4 (round 10): episodes are published from a PRIVATE staging area that lives OUTSIDE the
#: canonical episode namespace, so an in-flight or crashed publication can never be mistaken for
#: an episode, never enter the export allowlist, and never collide with another writer's name.
STAGING_SUBDIR = ".run_manifest_staging"

#: F1 (round 11): the private per-job control area — the append lock lives here. Like staging, it
#: sits OUTSIDE the canonical Manifest namespace, so no reader, allowlist or Evidence export ever
#: sees it.
CONTROL_SUBDIR = ".run_manifest_control"
APPEND_LOCK_NAME = "append.lock"
#: Bounded: a wedged holder must surface as a diagnosable error, never a hang.
APPEND_LOCK_TIMEOUT_SEC = 30.0


@dataclass(frozen=True)
class VerifiedCanonicalChain:
    """F4 (round 11): a chain that has been FULLY verified, as a TYPE.

    A loose ``dict`` of episode dataclasses proves nothing about how it was obtained — it may
    have come from a permissive read, or from before a tamper. Making the verified chain its own
    type means the projection writer cannot be handed anything else by accident: if you hold one
    of these, every episode in it was strict-decoded, canonical-byte checked and artifact-verified
    through anchored reads, and the set was proven to be one linear 1..N history.
    """
    episodes: dict[str, RunManifestV1]
    latest: RunManifestV1

    @property
    def ordinals(self) -> list[int]:
        return sorted(m.episode_ordinal for m in self.episodes.values())

    def ordered(self) -> list[RunManifestV1]:
        return sorted(self.episodes.values(), key=lambda m: m.episode_ordinal)


#: F1 (round 15): the TERMINAL task states, taken from the committed JobPlan contract rather than
#: invented here. F011: "A task that already reached `applied_to_job_workspace` is durable and is
#: **never** rolled back. Nothing is converted to `skipped`." And `run_job` proves it: the resume
#: loop `continue`s past `applied`/`passed`/`skipped` (it "continues at the first pending task,
#: rerunning no completed work"), and the stop path refuses to roll those three back.
#:
#: Everything else — `pending`, `running`, `failed`, `blocked` — is NOT terminal here: a stopped
#: task legitimately returns to `pending` and its resume starts a NEW run. Binding those would
#: refuse real records, which is why this set is exactly three.
TERMINAL_TASK_STATES = frozenset({"applied_to_job_workspace", "passed", "skipped"})


def validate_task_lifecycle_chain(ordered_manifests: list["RunManifestV1"]) -> list[str]:
    """F1 (round 15): a task's history is MONOTONIC across the episode chain.

    Round 14 froze a run's ledger, so a later episode could no longer rewrite work it admitted to.
    It could still deny the work ever happened. Reproduced against the full writer: episode 1
    recorded T001 as `executed` / `applied_to_job_workspace` / run `rT001` with a terminal ledger
    and a call artifact; episode 2 — same immutable JobInput task — recorded it as `skipped`, with
    no run, no ledger and no calls. Every check passed: both manifests validated, both writes
    succeeded, the canonical loader and the verified tree accepted the chain. The finality rule
    never fired because there was no second ledger to compare; the omission WAS the erasure.

    So the chain is asked the question no single episode can answer: does each task's history only
    ever move forward?

    * **Terminal with a run** (`applied_to_job_workspace` / `passed`): every later episode must
      represent it as `prior_episode`, naming the SAME run id and the SAME frozen ledger
      ref/hash. It may not become skipped, not-dispatched, failed-pre-dispatch or runless.
    * **Skipped** (a terminal job decision — `_block_job` skips the remaining pending tasks):
      later episodes keep that meaning. The committed contract does NOT allow reactivation — the
      resume loop `continue`s past it — so a skipped task gaining a run is refused rather than
      modelled.
    * **Non-terminal** (a stop returns the task to `pending`): it MAY start a new run later. The
      earlier run and its ledger stay in their earlier immutable episode; nothing here forbids the
      new work, because forbidding it would break F011's resume.
    * **Identity**: every episode carries the same immutable JobInput task ids, in the same order.
      An addition, a removal or a reordering is refused, so two tasks can never trade places.
    """
    problems: list[str] = []
    ordered = sorted(ordered_manifests, key=lambda m: m.episode_ordinal)
    if not ordered:
        return problems

    # The immutable task list, as the FIRST episode's embedded definition declares it.
    baseline_ids = declared_job_input_task_ids(ordered[0])
    for m in ordered[1:]:
        ids = declared_job_input_task_ids(m)
        if ids != baseline_ids:
            problems.append(
                f"episode {m.episode_id}: its embedded job input declares tasks {ids}, but "
                f"episode {ordered[0].episode_id} declared {baseline_ids}: the task list is "
                f"immutable across a job's episodes — no addition, removal or reordering")

    # history[task_id] = (episode_id, the expectation that established the terminal state)
    settled: dict[str, tuple[str, TaskCallExpectationV1]] = {}
    for m in ordered:
        for te in m.call_expectation.tasks:
            prior = settled.get(te.task_id)
            if prior is not None:
                owner, was = prior
                if was.task_status_at_finalization == "skipped":
                    # Terminal job decision. The resume loop never revisits it.
                    if te.expectation != EXPECT_SKIPPED or te.run_id:
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} was recorded as "
                            f"skipped by episode {owner}, but this episode says "
                            f"{te.expectation!r}"
                            + (f" and names run {te.run_id!r}" if te.run_id else "")
                            + ": a skipped task is a terminal job decision and the committed "
                              "resume contract never reactivates it")
                else:
                    # Terminal WITH a run: applied/passed. It happened; it keeps having happened.
                    if te.expectation != EXPECT_PRIOR_EPISODE:
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} completed in episode "
                            f"{owner} (status {was.task_status_at_finalization!r}, run "
                            f"{was.run_id!r}), so this episode must carry it as "
                            f"{EXPECT_PRIOR_EPISODE!r} — it says {te.expectation!r}. A later "
                            f"episode cannot un-happen earlier work")
                    if te.run_id != was.run_id:
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} names run "
                            f"{te.run_id!r}, but episode {owner} completed it under run "
                            f"{was.run_id!r}")
                    if te.ledger_ref != was.ledger_ref:
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} names ledger "
                            f"{te.ledger_ref!r}, but episode {owner} sealed "
                            f"{was.ledger_ref!r}")
                    if te.finalized_calls_sha256 != was.finalized_calls_sha256:
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} seals a different "
                            f"ledger hash than episode {owner} did: a completed run's account "
                            f"is frozen")
                    # F2 (round 17): the terminal STATUS is frozen too. The chain bound the run
                    # id, ledger ref and ledger hash, but not `task_status_at_finalization`, so a
                    # later `prior_episode` record could keep the same run and ledger while
                    # rewriting the status a task finished with — `applied_to_job_workspace` in
                    # episode 1 becoming `failed` in episode 2. The status a task completed under
                    # is part of what completed.
                    if (te.task_status_at_finalization
                            != was.task_status_at_finalization):
                        problems.append(
                            f"episode {m.episode_id}: task {te.task_id!r} records status "
                            f"{te.task_status_at_finalization!r}, but episode {owner} completed "
                            f"it as {was.task_status_at_finalization!r}: a completed task's "
                            f"terminal status is frozen, a later episode cannot rewrite it")
                continue

            if te.task_status_at_finalization in TERMINAL_TASK_STATES:
                settled[te.task_id] = (m.episode_id, te)
    return problems


def validate_ledger_chain(ordered_manifests: list["RunManifestV1"]) -> list[str]:
    """F5 (round 13): a run's ledger history is CONTINUOUS across the episodes that carry it.

    No single manifest can prove this, and that is exactly where the hole was. Episode 2's ledger
    for a run could contain an entry saying `call_id=ghost-prior, episode_id=ep1` — a call present
    in no ep1 manifest, no ep1 call artifact and no ep1 ledger — and every check passed, because
    each one only ever asked "is ep1 a known prior?". History was a claim nobody read back.

    The rule, applied per (task, run) across the chain in ordinal order:

    * the first COMPLETE ledger for a run FREEZES that run's whole account (F1, round 14): a
      later episode may repeat that exact object and nothing else — no extension, no shrink, no
      reorder, no terminal-state change, no `complete` change, no header change. Later work
      belongs to a NEW run id, which is what production already does (`PingPongResult.run_id` is
      a fresh `uuid4().hex[:16]` per execution);
    * an incomplete ledger (never publishable — F1, round 13) may still grow, but only as an
      exact EXTENSION: the earlier entry list is a PREFIX, field for field, in order;
    * no prior entry may be removed, reordered, invented or altered;
    * every entry attributed to an earlier episode resolves to exactly one canonical call
      published by THAT episode (and therefore to its verified call artifact);
    * every new suffix entry belongs to the current episode.

    Takes the manifests in ordinal order (the caller holds a verified chain) and returns problems.
    """
    problems: list[str] = []
    ordered = sorted(ordered_manifests, key=lambda m: m.episode_ordinal)
    # Which episode published which call — keyed by the call's FULL identity.
    #
    # A `call_id` is a path-shaped ref RELATIVE TO ITS RUN (`calls/builder/round-01/attempt`), so
    # it is unique within a run and deliberately NOT across the job: every task's first builder
    # call carries that exact string. Keying this map on the call_id alone made two unrelated
    # tasks collide, and a real stop-then-resume was refused because the last writer of the
    # string "owned" it. The identity that is actually unique is (task, run, call_id).
    published_by: dict[tuple, str] = {}
    for m in ordered:
        for c in m.calls:
            published_by[(c.identity.task_id, c.identity.run_id, c.identity.call_id)] = \
                m.episode_id
    seen: dict[tuple, tuple] = {}         # (task, run) -> the entries established so far

    for m in ordered:
        for lg in m.call_ledgers:
            key = (lg.task_id, lg.run_id)
            entries = tuple(sorted(lg.entries, key=lambda e: e.per_run_sequence))
            for e in entries:
                if e.episode_id == m.episode_id:
                    continue
                # A prior-episode entry is a claim about history: make it resolve.
                owner = published_by.get((lg.task_id, lg.run_id, e.call_id))
                if owner is None:
                    problems.append(
                        f"episode {m.episode_id}: ledger {lg.task_id}/{lg.run_id} claims prior "
                        f"call {e.call_id!r} in episode {e.episode_id!r}, but no episode in the "
                        f"canonical chain published that call")
                elif owner != e.episode_id:
                    problems.append(
                        f"episode {m.episode_id}: ledger {lg.task_id}/{lg.run_id} attributes "
                        f"call {e.call_id!r} to episode {e.episode_id!r}, but it was published "
                        f"by {owner!r}")
            prev = seen.get(key)
            if prev is None:
                seen[key] = (lg, entries)
                continue
            prev_lg, prev_entries = prev

            # F1 (round 14): A COMPLETE TERMINAL LEDGER IS FINAL.
            #
            # The round-13 rule compared the entry PREFIX, which permitted exactly the thing the
            # three facts forbid: episode 1 could publish `complete=true, terminal_state=completed,
            # [Call 1]` and episode 2 could republish the SAME run as `terminal_state=failed,
            # [Call 1, Call 2]` — an extension of a run that had already declared itself finished,
            # inside Evidence that is supposed to be immutable. Reproduced: both manifests
            # validated and the whole chain was accepted.
            #
            # `complete=true` means "this is the entire account of that run", and every state in
            # LEDGER_TERMINAL_STATES means "the run ended". So the ledger object is frozen whole —
            # header included — not merely its entry prefix. Later episodes may repeat it, and
            # only byte-for-byte.
            #
            # This is what production already does: `PingPongResult.run_id` is a fresh
            # `uuid4().hex[:16]` per execution, so later work is a NEW run. Verified against a
            # real stop-then-resume: T001's terminal ledger appears in both episodes with an
            # identical sha256, while the resumed task's new work arrives under a new run id.
            if prev_lg.complete:
                if lg.sha256() != prev_lg.sha256():
                    problems.append(
                        f"episode {m.episode_id}: ledger {lg.task_id}/{lg.run_id} differs from "
                        f"the COMPLETE {prev_lg.terminal_state!r} ledger an earlier episode "
                        f"already published for that run. A finished run's account is frozen: a "
                        f"later episode may repeat it byte-for-byte and nothing else, and later "
                        f"work belongs to a new run id")
                continue

            # An INCOMPLETE ledger has not claimed to be the whole account yet, so it may still
            # grow — but only as an exact extension of what is already recorded. (A published
            # reference can never contain one: F1, round 13.)
            if len(entries) < len(prev_entries):
                problems.append(
                    f"episode {m.episode_id}: ledger {lg.task_id}/{lg.run_id} has "
                    f"{len(entries)} entries, fewer than the {len(prev_entries)} an earlier "
                    f"episode already established: a run's history cannot shrink")
            else:
                head = entries[:len(prev_entries)]
                if head != prev_entries:
                    problems.append(
                        f"episode {m.episode_id}: ledger {lg.task_id}/{lg.run_id} does not "
                        f"extend the ledger an earlier episode established — its first "
                        f"{len(prev_entries)} entries are not that ledger, entry for entry")
                seen[key] = (lg, entries)
    return problems


def _open_control_fd(ev: Path, root: str | Path) -> int:
    return _fs.anchor_destination(ev / CONTROL_SUBDIR, Path(root), error_cls=ManifestError,
                                  noun="run-manifest control", create=True,
                                  dir_mode=MANIFEST_DIR_MODE)


@contextlib.contextmanager
def append_claim(evidence_dir: str | Path, *, root: str | Path,
                 timeout_sec: float = APPEND_LOCK_TIMEOUT_SEC):
    """F1 (round 11): serialize EVERY append for one job, preflight through postcondition.

    The atomic directory rename only serializes writers racing for the SAME episode name. Two
    writers publishing DIFFERENT episode ids can each read the same chain, each compute "the next
    ordinal is N+1", and each succeed — leaving a chain with a duplicate ordinal that the
    canonical loader rejects. The rename cannot help: the two names never collide.

    So the whole state transition — load chain, validate, decide the next ordinal, stage, publish,
    revalidate, write projections, assert the postcondition — is held under ONE per-job advisory
    lock. `flock` is released by the kernel when the fd closes, so an exception, a kill, or a
    crashed process can never leave a permanent claim.

    READERS never take this lock: they validate canonical state instead, so a wedged writer can
    never block verification.
    """
    ctl_fd = _open_control_fd(Path(evidence_dir), root)
    lock_fd = None
    try:
        lock_fd = _fs.exclusive_lock_fd(APPEND_LOCK_NAME, ctl_fd, timeout_sec=timeout_sec,
                                        file_mode=MANIFEST_FILE_MODE, error_cls=ManifestError,
                                        noun="run-manifest append lock")
        yield lock_fd
    finally:
        if lock_fd is not None:
            _fs.release_lock_fd(lock_fd)
        os.close(ctl_fd)


def load_verified_canonical_chain_for_write(
        evidence_dir: str | Path, *, job_id: str,
        exclude: str = "") -> VerifiedCanonicalChain | None:
    """F2/F4 (round 11): THE full-chain validation every writer path shares.

    Every writer path — first episode, append, idempotent retry, concurrent convergence, Stop
    retry, recovery, Root/Index repair — must agree about what "the existing chain is fine" means.
    Before round 11 the append path checked everything while the idempotent path checked almost
    nothing, so retrying an unchanged episode over a chain whose PRIOR artifact had been tampered
    with returned success and the loader then rejected the tree. Success has to mean the same
    thing on every path or it means nothing.

    Validates, for every existing episode: the manifest (strict decode + canonical bytes), its
    exact root allowlist, EVERY declared call artifact (present, canonical, hash-bound), no
    undeclared artifact, no symlinked component, job ownership — then the SET: unique ids, unique
    contiguous ordinals 1..N, and the exact linear history.

    ``exclude`` omits one episode id (the candidate being published). Returns ``None`` when no
    episode exists yet. Raises ``ManifestError`` on any problem.
    """
    chain: dict[str, RunManifestV1] = {}
    for eid in _enumerate_episode_dirs_anchored(evidence_dir):
        if eid == exclude:
            continue
        if not _safe_component(eid):
            raise ManifestError(f"unsafe episode dir name {eid!r}")
        # The recovery loader is the anchored strict reader: schema, canonical bytes, every
        # declared artifact verified, undeclared artifacts refused, ownership checked.
        m = load_episode_record_for_recovery(evidence_dir, eid, expected_job_id=job_id)
        if m.episode_id != eid:
            raise ManifestError(f"episode dir {eid} holds manifest for {m.episode_id}")
        chain[eid] = m
    if not chain:
        return None
    problems = _validate_chain_set(chain)
    if problems:
        raise ManifestError("the canonical episode chain is broken: "
                            + "; ".join(problems)[:400])
    ordered = sorted(chain.values(), key=lambda m: m.episode_ordinal)
    return VerifiedCanonicalChain(episodes=chain, latest=ordered[-1])


def _validate_chain_set(chain: dict[str, RunManifestV1]) -> list[str]:
    """The whole-set invariants: unique ordinals, contiguous 1..N, exact linear history."""
    problems = _validate_episode_graph(chain)
    ords = sorted(m.episode_ordinal for m in chain.values())
    if len(set(ords)) != len(ords):
        problems.append(f"duplicate episode ordinals: {ords}")
    elif ords and ords != list(range(1, len(ords) + 1)):
        problems.append(f"episode ordinals are not 1..N contiguous: {ords}")
    return problems


def _validate_candidate_against_chain(candidate: RunManifestV1,
                                      chain: VerifiedCanonicalChain | None) -> list[str]:
    """F1: the new episode must extend the canonical chain EXACTLY."""
    problems: list[str] = []
    episodes = chain.episodes if chain else {}
    n = len(episodes)
    if candidate.episode_ordinal != n + 1:
        problems.append(
            f"new episode {candidate.episode_id} has ordinal {candidate.episode_ordinal}, but "
            f"the canonical chain has {n} episode(s), so the next ordinal is {n + 1}")
    by_ordinal = {m.episode_ordinal: eid for eid, m in episodes.items()}
    expected_prev = by_ordinal.get(n, "")
    if candidate.previous_episode_id != expected_prev:
        problems.append(
            f"new episode {candidate.episode_id} names previous "
            f"{candidate.previous_episode_id!r}, but the current latest episode is "
            f"{expected_prev!r}")
    expected_priors = [by_ordinal[o] for o in range(1, n + 1) if o in by_ordinal]
    if list(candidate.prior_episode_ids) != expected_priors:
        problems.append(
            f"new episode {candidate.episode_id} lists priors "
            f"{list(candidate.prior_episode_ids)}, which is not exactly the existing chain "
            f"{expected_priors} in ascending order")
    return problems


def _verify_published_episode_tree(ev: Path, ep_name: str, expected: RunManifestV1) -> None:
    """F3 (round 11): a published episode directory must be COMPLETE, not merely present.

    Used after losing a directory race: the winner may carry an identical `run_manifest.json` and
    yet have no `calls/` at all. "Its manifest matches mine" is not the same as "it is the episode
    I was about to publish", and treating the two as equal is how a writer reports success over a
    tree its own loader rejects.
    """
    root_fd = _open_dir_anchored_or_missing(ev)
    if root_fd is None:
        raise ManifestConflictError(f"episode {ep_name} vanished while it was being verified")
    try:
        stored = _read_episode_manifest_anchored(root_fd, ep_name)   # strict + canonical bytes
        if stored != expected:
            raise ManifestConflictError(
                f"a different manifest raced episode {expected.episode_id!r}")
        # The exact root allowlist + every declared artifact, and no undeclared extras.
        problems = validate_episode_artifacts_anchored(root_fd, ep_name, stored)
        if problems:
            raise ManifestConflictError(
                f"another writer published an INCOMPLETE episode {expected.episode_id!r} and "
                f"this writer will not repair it: {'; '.join(problems)[:200]}")
    except ManifestConflictError:
        raise
    except (ManifestError, _S.SchemaError) as exc:
        raise ManifestConflictError(
            f"another writer published an unreadable episode {expected.episode_id!r}: "
            f"{str(exc)[:160]}") from None
    finally:
        os.close(root_fd)


def _stage_episode(stage_fd: int, bound: RunManifestV1, data: bytes) -> None:
    """Build the COMPLETE episode under a private staging name."""
    try:
        os.mkdir(CALLS_SUBDIR, MANIFEST_DIR_MODE, dir_fd=stage_fd)
    except OSError as exc:
        raise ManifestError(f"cannot create the staging calls dir: {exc}") from exc
    calls_fd = _fs.open_verified_dir(CALLS_SUBDIR, dir_fd=stage_fd, error_cls=ManifestError,
                                     noun="run-manifest")
    try:
        for c in bound.calls:
            name = c.artifact.split("/", 1)[1]
            body = c.canonical_artifact_bytes()   # the exact bytes artifact_sha256 covers
            # F5: even in our own private staging directory the create-only Boolean is checked —
            # no path may ignore it. Here a collision can only mean the record declares the same
            # artifact twice, which is a record bug, not a race.
            if not _fs.write_file_atomically(calls_fd, name, body, create_only=True,
                                             file_mode=MANIFEST_FILE_MODE,
                                             error_cls=ManifestError, noun="call artifact"):
                raise ManifestError(
                    f"call artifact {name!r} is declared more than once by episode "
                    f"{bound.episode_id}")
    finally:
        os.close(calls_fd)
    # F1 (round 12): the canonical LEDGERS are staged exactly like the call artifacts — they are
    # part of the immutable episode, not a side note about it.
    if bound.call_ledgers:
        try:
            os.mkdir(LEDGERS_SUBDIR, MANIFEST_DIR_MODE, dir_fd=stage_fd)
        except OSError as exc:
            raise ManifestError(f"cannot create the staging ledger dir: {exc}") from exc
        led_fd = _fs.open_verified_dir(LEDGERS_SUBDIR, dir_fd=stage_fd,
                                       error_cls=ManifestError, noun="run-manifest")
        try:
            for lg in bound.call_ledgers:
                name = lg.ref().split("/", 1)[1]
                if not _fs.write_file_atomically(led_fd, name, lg.canonical_bytes(),
                                                 create_only=True,
                                                 file_mode=MANIFEST_FILE_MODE,
                                                 error_cls=ManifestError, noun="call ledger"):
                    raise ManifestError(
                        f"call ledger {name!r} is declared more than once by episode "
                        f"{bound.episode_id}")
        finally:
            os.close(led_fd)
    if not _fs.write_file_atomically(stage_fd, MANIFEST_FILENAME, data, create_only=True,
                                     file_mode=MANIFEST_FILE_MODE, error_cls=ManifestError,
                                     noun="run manifest"):
        raise ManifestError("the staged episode record already exists")


def write_run_manifest(evidence_dir: str | Path, manifest: RunManifestV1, *,
                       root: str | Path) -> Path:
    """Write one EPISODE's manifest (with its call-input artifacts and the index update),
    contained and exactly once.

    The publication model (rounds 10-11):

    1. the candidate is validated and its canonical bytes round-tripped BEFORE anything is
       written;
    2. the whole state transition runs under ONE per-job APPEND CLAIM (F1), so two writers can
       never both decide they are ordinal N+1;
    3. the COMPLETE existing chain is loaded and fully validated through one shared function —
       on every path, including an idempotent retry (F2);
    4. the candidate must extend that chain exactly;
    5. the complete episode is built under a private STAGING name outside the canonical episode
       namespace and published with ONE atomic rename; a lost race verifies the winner's WHOLE
       tree, not just its manifest (F3);
    6. the chain is RELOADED and revalidated after publication, and the derived projections are
       written only from that verified object (F4);
    7. the writer postcondition is asserted before returning.

    Idempotent for the same episode content; conflicting content raises ``ManifestConflictError``
    without touching what is already published.
    """
    if root is None or str(root) == "":
        raise ManifestError("a run manifest needs an explicit trusted evidence root")

    ev = Path(evidence_dir)
    _require_valid_manifest(manifest, "write", published=False)
    bound = _bind_artifact_refs(manifest)
    ep_name = episode_dir_name(bound.episode_id)
    ep_dir = ev / MANIFESTS_SUBDIR / ep_name
    payload = bound.to_json()
    data = _fs.json_bytes(payload, sort_keys=True)

    # F12: PRE-PUBLICATION ROUND-TRIP. No immutable episode may be created from data the
    # canonical reader would immediately reject.
    _require_valid_manifest(bound, "write (bound)", mode=MODE_PUBLISHED_REFERENCE)
    if len(data) > _S.MAX_EPISODE_MANIFEST_BYTES:
        raise ManifestError(
            f"episode record is {len(data)} bytes, over the "
            f"{_S.MAX_EPISODE_MANIFEST_BYTES}-byte canonical limit; refusing to publish a "
            f"record the canonical reader would reject")
    roundtripped = decode_run_manifest_v1(data)             # strict decode of the exact bytes
    if roundtripped != bound:
        raise ManifestError("the bound record does not survive a strict decode round-trip")
    if _fs.json_bytes(roundtripped.to_json(), sort_keys=True) != data:
        raise ManifestError("re-serializing the decoded record does not reproduce its bytes")
    _total = len(data)
    for _c in bound.calls:
        _abytes = _c.canonical_artifact_bytes()
        if len(_abytes) > _S.MAX_CALL_ARTIFACT_BYTES:
            raise ManifestError(
                f"call artifact for {_c.identity.call_id} is {len(_abytes)} bytes, over the "
                f"{_S.MAX_CALL_ARTIFACT_BYTES}-byte limit")
        _total += len(_abytes)
    if _total > _S.MAX_TREE_BYTES:
        raise ManifestError(
            f"the projected manifest tree is {_total} bytes, over the "
            f"{_S.MAX_TREE_BYTES}-byte limit")

    # F3 (round 10): the trusted root resolves (and creates) the evidence dir before anything is
    # enumerated, read or written.
    _root_fd = _contained_root_fd(ev, root, create=True)
    os.close(_root_fd)

    # F1: ONE claim for the whole transition.
    with append_claim(ev, root=root):
        # F11 (round 12): hygiene, under the claim, before any staging of our own.
        cleanup_abandoned_stages(ev, root=root)

        # ---- F3 (round 12): is this episode ALREADY published? ------------------------
        # Asked BEFORE the chain is loaded, and WITHOUT excluding the candidate: excluding an
        # older episode from its own chain is what made an exact ep1 retry report
        # "ep2 references unknown prior ep1". An episode that already exists is not a candidate
        # for anything — it is history, and history is only ever compared, never recomputed.
        existing_raw = _read_existing_episode_bytes(ev, root, ep_name)

        if existing_raw is not None:
            # The WHOLE chain, with the existing episode INCLUDED — a retry must be judged
            # against the chain as it really is (F2: a tampered/missing artifact in ANY episode
            # blocks the retry instead of returning a success the loader contradicts).
            verified = load_verified_canonical_chain_for_write(ev, job_id=bound.job_id)
            if verified is None:
                raise ManifestError("the episode chain vanished during the retry")
            canonical = _decode_existing_episode(existing_raw, bound.episode_id)
            if not _identity_ok(canonical.to_json(), payload):
                raise ManifestConflictError(
                    f"a different manifest already exists for episode "
                    f"{bound.episode_id!r}; refusing to overwrite it")
            # F2 (round 12): a PUBLISHED episode's members are IMMUTABLE. Episodes are published
            # atomically as complete directories, so a missing artifact afterwards is not a
            # partial write — it is corruption, tamper or storage loss, and quietly recreating it
            # would erase the only evidence that something went wrong. Verify; never repair.
            _require_complete_episode(ev, ep_name, canonical)

            # F3: an EXACT retry of a non-latest episode changes nothing. The chain is already
            # verified above, so the only work left is derived-projection recovery — and only
            # when the projections are actually out of date.
            if not _projections_match(ev, verified):
                _mirror_and_index(ev, verified, root=Path(root))
            _assert_writer_postcondition(ev, root=root, job_id=bound.job_id,
                                         latest=verified.latest)
            return ep_dir / MANIFEST_FILENAME

        # ---- a NEW episode: it must extend the canonical chain exactly ----------------
        chain = load_verified_canonical_chain_for_write(ev, job_id=bound.job_id)
        problems = _validate_candidate_against_chain(bound, chain)
        if problems:
            raise ManifestError(
                "the new episode does not extend the canonical chain: "
                + "; ".join(problems)[:400])
        canonical = _publish_staged_episode(ev, root, ep_name, bound, data, payload)

        # ---- F4: RELOAD and revalidate the COMPLETE chain, then project from THAT ------
        verified = load_verified_canonical_chain_for_write(ev, job_id=bound.job_id)
        if verified is None:
            raise ManifestError("the episode chain vanished during publication")
        if verified.latest.episode_id != canonical.episode_id and \
                canonical.episode_ordinal > verified.latest.episode_ordinal:
            raise ManifestError("the published episode is not part of the verified chain")
        _mirror_and_index(ev, verified, root=Path(root))
        _assert_writer_postcondition(ev, root=root, job_id=bound.job_id,
                                     latest=verified.latest)
    return ep_dir / MANIFEST_FILENAME


def _read_existing_episode_bytes(ev: Path, root: str | Path, ep_name: str) -> bytes | None:
    ms_fd = _open_manifests_fd(ev, root)
    try:
        try:
            ep_fd = _fs.open_verified_dir(ep_name, dir_fd=ms_fd, error_cls=ManifestError,
                                          noun="run-manifest")
        except _fs.MissingComponent:
            return None
        try:
            return _fs.read_verified_file(
                MANIFEST_FILENAME, ep_fd, max_bytes=_S.MAX_EPISODE_MANIFEST_BYTES,
                error_cls=ManifestError, noun="run manifest")
        finally:
            os.close(ep_fd)
    finally:
        os.close(ms_fd)


def _projections_match(ev: Path, verified: VerifiedCanonicalChain) -> bool:
    """Are the derived Root/Index already exactly what this verified chain projects?

    Used by the F3 no-op path: an exact retry of an already-published episode must not rewrite
    the projections for the sake of it — but if they are missing or stale (a crash between the
    episode and its projections), rebuilding them IS the documented derived-projection recovery.
    """
    try:
        index, root_fd = load_index_verified(ev)
    except Exception:
        return False
    try:
        if index is None:
            return False
        expected = {"index_v": 1, "latest_episode_id": verified.latest.episode_id,
                    "episodes": [_index_entry(m) for m in verified.ordered()]}
        if index != expected:
            return False
        mirror = _fs.read_verified_file(MANIFEST_FILENAME, root_fd,
                                        max_bytes=_S.MAX_EPISODE_MANIFEST_BYTES,
                                        error_cls=ManifestError, noun="run manifest")
    except Exception:
        return False
    finally:
        os.close(root_fd)
    return mirror == verified.latest.canonical_bytes()


def _require_complete_episode(ev: Path, ep_name: str, m: RunManifestV1) -> None:
    """F2: this episode's exact root allowlist + every declared artifact must hold."""
    root_fd = _open_dir_anchored_or_missing(ev)
    if root_fd is None:
        raise ManifestError("evidence directory does not exist")
    try:
        problems = validate_episode_artifacts_anchored(root_fd, ep_name, m)
        if problems:
            raise ManifestError(
                f"episode {ep_name} is not a complete canonical episode: "
                + "; ".join(problems)[:300])
    finally:
        os.close(root_fd)


def _assert_writer_postcondition(ev: Path, *, root: str | Path, job_id: str,
                                 latest: RunManifestV1) -> None:
    """F4/F12 (round 11): a successful public writer operation must NEVER leave a state its own
    reader rejects. This is the last thing every write does, so the promise is checked rather
    than assumed."""
    problems = validate_index_and_tree(ev, job_id=job_id)
    if problems:
        raise ManifestError(
            "writer postcondition failed — the published tree is not canonically readable: "
            + "; ".join(problems)[:300])
    reread = load_latest_manifest_verified(ev, job_id=job_id)
    if reread.episode_id != latest.episode_id:
        raise ManifestError(
            f"writer postcondition failed — the canonical latest is {reread.episode_id!r}, "
            f"not the published {latest.episode_id!r}")


def _open_manifests_fd(ev: Path, root: str | Path) -> int:
    """The anchored `run_manifests/` handle, created if needed."""
    return _fs.anchor_destination(ev / MANIFESTS_SUBDIR, Path(root), error_cls=ManifestError,
                                  noun="run-manifest", create=True,
                                  dir_mode=MANIFEST_DIR_MODE)


#: F2 (round 12): there is no artifact "settlement" any more.
#:
#: A published episode is atomic and complete, so every one of its members is IMMUTABLE from the
#: instant the rename lands. `_settle_existing_artifacts` used to rewrite a missing artifact on an
#: idempotent retry, which meant a deleted artifact came back and the loader went green — erasing
#: the only evidence of corruption, tamper or storage loss. Published members are now VERIFIED
#: (`_require_complete_episode`) and never repaired; only a private, unpublished stage is ever
#: written to.


#: F11 (round 12): a stage is only ever cleaned up when it is unambiguously abandoned debris.
#: The bound is deliberately conservative — deleting an ACTIVE writer's stage would destroy an
#: episode mid-publication, which is far worse than leaving a directory behind.
STAGING_STALE_SECONDS = 24 * 60 * 60
STAGING_CLEANUP_MAX_ITEMS = 64
_STAGING_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}\.[0-9]+\.[0-9a-f]{16}$")


def cleanup_abandoned_stages(evidence_dir: str | Path, *, root: str | Path,
                             stale_seconds: float = STAGING_STALE_SECONDS) -> list[str]:
    """F11 (round 12): remove clearly-abandoned private staging directories.

    Crash debris is invisible to every canonical reader (that is the point of staging living
    outside the namespace), so this is hygiene, not correctness — and it is written to fail safe:

    * it runs UNDER the append claim, so no writer of THIS job can be staging concurrently;
    * only names matching the exact staging format are considered;
    * a stage whose owning PID is still alive is never touched;
    * a stage younger than `stale_seconds` is never touched;
    * it never looks at, or deletes, anything in the canonical episode namespace;
    * a cleanup failure is reported, never raised over the caller's real work.

    Returns the names it removed.
    """
    removed: list[str] = []
    try:
        stage_root_fd = _fs.anchor_destination(Path(evidence_dir) / STAGING_SUBDIR, Path(root),
                                               error_cls=ManifestError, noun="run-manifest",
                                               create=False, dir_mode=MANIFEST_DIR_MODE)
    except (_fs.MissingComponent, Exception):
        return removed                      # nothing staged, nothing to clean
    try:
        names = sorted(_fs.list_dir_names(stage_root_fd, error_cls=ManifestError,
                                          noun="run-manifest"))[:STAGING_CLEANUP_MAX_ITEMS]
        now = time.time()
        for name in names:
            if not _STAGING_NAME.match(name):
                continue                    # not ours to reason about
            try:
                st = os.stat(name, dir_fd=stage_root_fd, follow_symlinks=False)
            except OSError:
                continue
            if not stat.S_ISDIR(st.st_mode):
                continue                    # never follow or delete a symlink here
            if (now - st.st_mtime) < stale_seconds:
                continue                    # too fresh to call abandoned
            if _pid_is_alive(_stage_pid(name)):
                continue                    # an ACTIVE writer owns it
            with contextlib.suppress(Exception):
                _fs.remove_tree_at(name, stage_root_fd, error_cls=ManifestError,
                                   noun="run-manifest staging")
                removed.append(name)
    except Exception:
        return removed                      # hygiene never breaks the caller's real work
    finally:
        os.close(stage_root_fd)
    return removed


def _stage_pid(name: str) -> int:
    try:
        return int(name.rsplit(".", 2)[1])
    except (IndexError, ValueError):
        return -1


def _pid_is_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True                         # exists, owned by someone else
    except OSError:
        return True                         # unsure → treat as alive and leave it alone


def _publish_staged_episode(ev: Path, root: str | Path, ep_name: str,
                            bound: RunManifestV1, data: bytes,
                            payload: dict[str, Any]) -> RunManifestV1:
    """F4 (round 10): atomic staged publication of ONE complete episode.

    The episode is assembled under an unpredictable private name in `.run_manifest_staging/`,
    which is OUTSIDE the canonical episode namespace — so no reader, exporter or allowlist ever
    sees a half-built episode, and two writers cannot touch each other's files. The single
    `rename` is the only moment `run_manifests/<episode>` comes into existence: it either
    appears complete or it does not appear at all.
    """
    stage_root_fd = _fs.anchor_destination(ev / STAGING_SUBDIR, Path(root),
                                           error_cls=ManifestError, noun="run-manifest",
                                           create=True, dir_mode=MANIFEST_DIR_MODE)
    stage_name = f"{ep_name}.{os.getpid()}.{secrets.token_hex(8)}"
    published = False
    try:
        try:
            os.mkdir(stage_name, MANIFEST_DIR_MODE, dir_fd=stage_root_fd)
        except OSError as exc:
            raise ManifestError(f"cannot create the staging episode dir: {exc}") from exc
        stage_fd = _fs.open_verified_dir(stage_name, dir_fd=stage_root_fd,
                                         error_cls=ManifestError, noun="run-manifest")
        try:
            _stage_episode(stage_fd, bound, data)
        finally:
            os.close(stage_fd)

        # The rename must cross from the staging dir into `run_manifests/`; both are anchored
        # handles under the same trusted root, so this is one atomic directory publication.
        ms_fd = _open_manifests_fd(ev, root)
        try:
            try:
                os.rename(stage_name, ep_name, src_dir_fd=stage_root_fd, dst_dir_fd=ms_fd)
                published = True
            except (FileExistsError, NotADirectoryError):
                published = False
            except OSError as exc:
                if exc.errno not in (errno.ENOTEMPTY, errno.EEXIST):
                    raise ManifestError(
                        f"the episode could not be published: {exc}") from exc
                published = False
            if published:
                return bound
            # ---- We LOST the publication race. Someone else's episode is there now. -------
            # We have touched nothing inside it: our artifacts only ever existed under our own
            # staging name.
            #
            # F3 (round 11): only a COMPLETE, canonically equivalent winner is idempotent
            # success. A winner carrying our exact manifest but no `calls/` is not "the same
            # episode" — it is a broken tree, and converging onto it would report success over
            # something the canonical loader rejects. We verify the winner's WHOLE tree, and we
            # never repair it: adding our files to another writer's episode is exactly the
            # contamination the staging model exists to prevent.
            _verify_published_episode_tree(ev, ep_name, bound)
            return bound
        finally:
            os.close(ms_fd)
    finally:
        if not published:
            # Clean up ONLY our own private staging name. Never a published episode.
            with contextlib.suppress(Exception):
                _fs.remove_tree_at(stage_name, stage_root_fd, error_cls=ManifestError,
                                   noun="run-manifest staging")
        os.close(stage_root_fd)


def _write_call_artifacts(dir_fd: int, manifest: RunManifestV1) -> None:
    try:
        os.mkdir(CALLS_SUBDIR, MANIFEST_DIR_MODE, dir_fd=dir_fd)
    except FileExistsError:
        pass
    except OSError as exc:
        raise ManifestError(f"cannot create the calls dir: {exc}") from exc
    calls_fd = _fs.open_verified_dir(CALLS_SUBDIR, dir_fd=dir_fd, error_cls=ManifestError,
                                     noun="run-manifest")
    try:
        for c in manifest.calls:
            name = c.artifact.split("/", 1)[1]
            body = c.canonical_artifact_bytes()      # the exact bytes artifact_sha256 covers
            existing = _fs.read_verified_file(name, calls_fd, error_cls=ManifestError,
                                              noun="call artifact")
            if existing is not None:
                # F10: an immutable artifact that already exists must be IDENTICAL. A
                # tampered artifact is a conflict, never silently accepted or repaired.
                if existing != body:
                    raise ManifestConflictError(
                        f"existing call artifact {name!r} differs from the canonical bytes; "
                        f"refusing to overwrite an immutable artifact")
                continue
            # F3 (round 10): the pre-read said "absent", but between that read and this write
            # another writer may have created it. `create_only` publishes with `os.link`, which
            # returns False rather than clobbering — and that Boolean is the ONLY thing standing
            # between us and reporting success over someone else's bytes. Verify it.
            if not _fs.write_file_atomically(calls_fd, name, body, create_only=True,
                                             file_mode=MANIFEST_FILE_MODE,
                                             error_cls=ManifestError, noun="call artifact"):
                raced = _fs.read_verified_file(name, calls_fd, error_cls=ManifestError,
                                               noun="call artifact")
                if raced is None:
                    raise ManifestConflictError(
                        f"call artifact {name!r} was created and removed by another writer "
                        f"while this episode was being published")
                if raced != body:
                    # Different bytes under an immutable name: two writers disagree about the
                    # same call's input. Neither may win by accident.
                    raise ManifestConflictError(
                        f"another writer published a DIFFERENT call artifact {name!r} for this "
                        f"episode; refusing to report success over it")
                # Identical bytes — the other writer published exactly what we would have.
    finally:
        os.close(calls_fd)


def canonical_index_bytes(index: dict[str, Any]) -> bytes:
    """F2: THE canonical Index encoding. The writer emits exactly these bytes and every reader
    requires the stored bytes to equal them."""
    return _fs.json_bytes(index, sort_keys=True)


def require_canonical_index_bytes(raw: bytes, index: dict[str, Any]) -> None:
    if bytes(raw) != canonical_index_bytes(index):
        raise ManifestError(
            "manifest index: stored bytes are not the canonical encoding of the index they "
            "decode to (noncanonical formatting, an unknown field, or raw-byte drift)")


def _index_entry(manifest: RunManifestV1) -> dict[str, Any]:
    return {
        "episode_id": manifest.episode_id,
        "status": manifest.status,
        "created_at": manifest.created_at,
        "episode_ordinal": manifest.episode_ordinal,
        "previous_episode_id": manifest.previous_episode_id,
        "record_sha256": manifest.record_sha256(),
        "manifest_ref": f"{MANIFESTS_SUBDIR}/{episode_dir_name(manifest.episode_id)}/"
                        f"{MANIFEST_FILENAME}",
    }


# ---------------------------------------------------------------------------
# F3/F4 — recovery from the IMMUTABLE episode records (source of truth)
#
# The three durable layers are, in trust order:
#   1. the immutable per-episode manifest + its call artifacts  (SOURCE OF TRUTH);
#   2. the derived root mirror + run_manifest_index.json         (derived projection);
#   3. the JobPlan checkpoint.
# They are NOT committed atomically together. A failure in a DERIVED projection (2) is fully
# recoverable from the immutable episodes (1); a failure BEFORE an immutable episode exists
# leaves no false episode. Readers/CLI keep rejecting an inconsistent chain — only the
# writer/retry path uses recovery, and only to REBUILD the derived projection from (1).
# ---------------------------------------------------------------------------


def _contained_root_fd(evidence_dir: str | Path, root: str | Path, *,
                       create: bool = False) -> int:
    """F3: anchor the EXPLICIT trusted root and walk to ``evidence_dir`` THROUGH it.

    The untrusted ``evidence_dir`` is never independently anchored as a new root: it is resolved
    only RELATIVE to the trusted root, so an absolute path outside the root, a sibling, a ``../``
    traversal, or a symlink inside the root pointing outside is REFUSED rather than written to.
    Returns the destination fd (caller closes it)."""
    if root is None or str(root) == "":
        raise ManifestError("a trusted evidence root is required")
    root_norm = Path(os.path.normpath(os.path.abspath(str(root))))
    ev_norm = Path(os.path.normpath(os.path.abspath(str(evidence_dir))))
    try:
        rel = ev_norm.relative_to(root_norm)
    except ValueError:
        raise ManifestError(
            f"evidence directory {ev_norm.name!r} is outside the trusted root "
            f"{root_norm.name!r}") from None
    if any(part == ".." for part in rel.parts):
        raise ManifestError("evidence directory escapes the trusted root")
    # anchor_destination walks from the trusted root on VERIFIED handles, refusing every
    # symlinked component on the way (so a symlink inside the root pointing outside is caught).
    return _fs.anchor_destination(ev_norm, root_norm, error_cls=ManifestError,
                                  noun="run-manifest", create=create,
                                  dir_mode=MANIFEST_DIR_MODE)


def load_episode_record_for_recovery(evidence_dir: str | Path, episode_id: str, *,
                                     expected_job_id: str = "") -> RunManifestV1:
    """F3: load ONE immutable episode record trusting ONLY the episode manifest and its declared
    artifacts — NOT a possibly missing/stale root mirror or index. Every component is anchored
    (no symlink follow / outside read), the manifest schema is validated and every declared call
    artifact is verified; undeclared artifacts are rejected. This is the loader the writer/retry
    recovery path uses when the derived index/mirror is broken."""
    if not _safe_component(episode_id):
        raise ManifestError(f"unsafe episode id {episode_id!r}")
    root_fd = _open_dir_anchored_or_missing(evidence_dir)   # F15: anchored existence
    if root_fd is None:
        raise ManifestError("evidence directory does not exist")
    try:
        m = _read_episode_manifest_anchored(root_fd, episode_id)     # schema-validated
        if expected_job_id and m.job_id != expected_job_id:
            raise ManifestError(
                f"episode {episode_id} job_id {m.job_id!r} != expected {expected_job_id!r}")
        art = validate_episode_artifacts_anchored(root_fd, episode_id, m)
        if art:
            raise ManifestError("; ".join(art)[:400])
        return m
    finally:
        os.close(root_fd)


def _enumerate_episode_dirs_anchored(evidence_dir: str | Path) -> list[str]:
    root_fd = _open_dir_anchored_or_missing(evidence_dir)   # F15: anchored existence
    if root_fd is None:
        return []
    try:
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            return []
        try:
            return sorted(_fs.list_dir_names(subs_fd, error_cls=ManifestError,
                                             noun="run-manifest"))
        finally:
            os.close(subs_fd)
    finally:
        os.close(root_fd)


def rebuild_manifest_mirror_and_index_from_canonical_episodes(
        evidence_dir: str | Path, *, root: str | Path, job_id: str = "") -> str:
    """F3/F4: rebuild the derived root mirror + index PURELY from the immutable episode records.

    Round 11: this is a WRITER path, so it takes the per-job append claim and uses the SAME
    shared full-chain validation every other writer path uses — every episode strict-decoded and
    canonical-byte checked, every declared artifact verified, no undeclared artifact, ownership,
    unique contiguous ordinals and the exact linear history — then writes the projections from
    the verified object and asserts the writer postcondition. It never overwrites an immutable
    episode and refuses to guess through a malformed or ambiguous set. Returns the latest id.
    """
    # F3: the trusted root is not a formality — the evidence directory is resolved (and, if
    # missing, created) ONLY through it. An outside/sibling/traversal/symlinked path is refused
    # here, before anything is enumerated, read or written.
    contained_fd = _contained_root_fd(evidence_dir, root, create=True)
    os.close(contained_fd)
    ev = Path(evidence_dir)
    with append_claim(ev, root=root):
        chain = load_verified_canonical_chain_for_write(ev, job_id=job_id)
        if chain is None:
            raise ManifestError("no canonical episodes to rebuild the mirror/index from")
        _mirror_and_index(ev, chain, root=Path(root))
        _assert_writer_postcondition(ev, root=root, job_id=job_id, latest=chain.latest)
        return chain.latest.episode_id


def _mirror_and_index(evidence_dir: Path, chain: VerifiedCanonicalChain, *,
                      root: Path) -> None:
    """Publish the DERIVED projections (root mirror + index) from a VERIFIED chain.

    F4 (round 11): this takes a ``VerifiedCanonicalChain`` — not a loose list of episode
    dataclasses. The projections say "this is the canonical history"; they may only ever be
    derived from a set that has been proven to BE one, through anchored strict reads, with every
    artifact verified, immediately beforehand. Accepting anything else would let a projection
    outrun the evidence it claims to summarise.

    The Index is never loaded permissively and mutated: it is RECONSTRUCTED from the verified
    episodes and re-emitted as exact canonical bytes, so an unknown field or noncanonical
    formatting in a previous Index cannot survive an append.
    """
    if not isinstance(chain, VerifiedCanonicalChain):
        raise ManifestError(
            "the derived projections may only be written from a VerifiedCanonicalChain "
            "(F4: a projection must never be derived from an unverified episode set)")
    ordered = chain.ordered()
    latest = chain.latest
    index = {
        "index_v": 1,
        "latest_episode_id": latest.episode_id,
        "episodes": [_index_entry(m) for m in ordered],
    }
    ev_fd = _fs.anchor_root(evidence_dir, error_cls=ManifestError, noun="run-manifest",
                            create=True, dir_mode=MANIFEST_DIR_MODE)
    try:
        # F2: the mirror is byte-for-byte the latest canonical episode; the Index is exactly the
        # canonical Index bytes.
        _fs.write_file_atomically(ev_fd, MANIFEST_FILENAME, latest.canonical_bytes(),
                                  create_only=False, file_mode=MANIFEST_FILE_MODE,
                                  error_cls=ManifestError, noun="run manifest")
        _fs.write_file_atomically(ev_fd, MANIFEST_INDEX_FILENAME, canonical_index_bytes(index),
                                  create_only=False, file_mode=MANIFEST_FILE_MODE,
                                  error_cls=ManifestError, noun="manifest index")
    finally:
        os.close(ev_fd)


def read_run_manifest(path: str | Path) -> RunManifestV1:
    """F15: read ONE manifest file through ANCHORED, symlink-refusing handles and the STRICT
    decoder — never a name-based ``Path.is_file()`` + ``read_text()``. Kept for direct-file
    callers (tests/tools); production trust paths use the canonical loaders."""
    p = Path(os.path.normpath(os.path.abspath(str(path))))
    parent_fd = _open_dir_anchored_or_missing(p.parent)
    if parent_fd is None:
        raise ManifestError(f"no run manifest at {p.name}")
    try:
        raw = _fs.read_verified_file(p.name, parent_fd,
                                     max_bytes=_S.MAX_EPISODE_MANIFEST_BYTES,
                                     error_cls=ManifestError, noun="run manifest")
    finally:
        os.close(parent_fd)
    if raw is None:
        raise ManifestError(f"no run manifest at {p.name}")
    manifest = decode_run_manifest_v1(raw)          # F13: strict, never permissive
    require_canonical_bytes(raw, manifest, where=f"run manifest {p.name}")
    _require_valid_manifest(manifest, "read", mode=MODE_PUBLISHED_REFERENCE)
    return manifest


def read_index(evidence_dir: str | Path) -> dict[str, Any]:
    """F11/F12: read the index through the ANCHORED, STRICT canonical path — no name-based
    ``Path.is_file()`` precheck and no permissive ``json.loads``. A genuinely absent index is
    ``{"index_v": 1, "episodes": []}``; a PRESENT but malformed/noncanonical index raises, so a
    caller can never mistake corruption for absence."""
    try:
        index, root_fd = load_index_verified(evidence_dir)
    except _fs.MissingComponent:
        return {"index_v": 1, "episodes": []}
    os.close(root_fd)
    if index is None:
        return {"index_v": 1, "episodes": []}
    return index


# ---------------------------------------------------------------------------
# Anchored read-only Evidence traversal + verified trust chain (F8, F9, F11)
# ---------------------------------------------------------------------------


def _anchored_read(dir_fd: int, name: str, *, noun: str = "run-manifest") -> bytes | None:
    return _fs.read_verified_file(name, dir_fd, error_cls=ManifestError, noun=noun)


def load_index_verified(evidence_dir: str | Path):
    """Read the index through an ANCHORED evidence-root fd (no symlinked parent is followed),
    parse it, and return ``(index_dict, root_fd)``. The caller closes ``root_fd``. Missing
    index → ``(None, root_fd)``."""
    # F15: existence is an ANCHORED decision — a missing dir raises MissingComponent (the
    # caller distinguishes it), a symlinked/unsafe one raises rather than being followed.
    root_fd = _open_dir_anchored_or_missing(evidence_dir)
    if root_fd is None:
        raise _fs.MissingComponent(str(evidence_dir))
    try:
        raw = _anchored_read(root_fd, MANIFEST_INDEX_FILENAME, noun="manifest index")
    except Exception:
        os.close(root_fd)
        raise
    if raw is None:
        return None, root_fd
    try:
        index = decode_index_v1(raw)                  # F4: strict raw-JSON decode + bounds
        # F2: the stored Index bytes must BE the canonical encoding of what they decode to —
        # a pretty-printed or unknown-field-bearing Index is refused, not silently normalized.
        require_canonical_index_bytes(raw, index)
    except ManifestError:
        os.close(root_fd)
        raise
    except _S.SchemaError as exc:
        os.close(root_fd)
        raise ManifestError(f"unreadable manifest index: {exc}") from None
    return index, root_fd


def _read_episode_manifest_anchored(root_fd: int, episode_id: str) -> RunManifestV1:
    """Open ``run_manifests/<episode_id>/run_manifest.json`` through held, symlink-refusing
    directory fds and return the validated manifest."""
    if not _safe_component(episode_id):
        raise ManifestError(f"unsafe episode id {episode_id!r}")
    try:
        subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                        error_cls=ManifestError, noun="run-manifest")
    except _fs.MissingComponent as exc:
        raise ManifestError(f"{MANIFESTS_SUBDIR}/ is missing") from None
    try:
        ep_fd = _fs.open_verified_dir(episode_id, dir_fd=subs_fd,
                                      error_cls=ManifestError, noun="run-manifest")
    except _fs.MissingComponent as exc:
        raise ManifestError(f"episode {episode_id} directory is missing") from None
    finally:
        os.close(subs_fd)
    try:
        raw = _anchored_read(ep_fd, MANIFEST_FILENAME)
    finally:
        os.close(ep_fd)
    if raw is None:
        raise ManifestError(f"episode {episode_id} has no manifest")
    manifest = decode_run_manifest_v1(raw)          # F4: strict raw-JSON decode
    # F11: the stored bytes must BE the canonical encoding of what they decode to.
    require_canonical_bytes(raw, manifest, where=f"episode {episode_id}")
    _require_valid_manifest(manifest, f"episode {episode_id}",
                            mode=MODE_PUBLISHED_REFERENCE)
    return manifest


def _validate_episode_graph(by_id: dict[str, "RunManifestV1"]) -> list[str]:
    """F6/F8: prove the prior-episode references form the CANONICAL linear history.

    F6: every edge (episode -> a prior_episode_id) must point at a KNOWN episode with a STRICTLY
    LOWER ordinal — never itself, never a future/equal ordinal, never an unknown id; a DFS also
    rejects any cycle directly.

    F8: the history is not merely an arbitrary DAG — it is TOTAL and ORDERED. For an episode of
    ordinal N: ``prior_episode_ids`` is EXACTLY every episode of ordinal 1..N-1 in ascending
    order, and ``previous_episode_id`` is exactly the ordinal-(N-1) episode. An episode may not
    skip its immediate predecessor, and every episode but the first has exactly one.

    F5 (round 13): the LEDGER history is validated here too, because this is the one place that
    holds the whole chain. A ledger's account of a run spans episodes, so no single manifest can
    check it — and while nobody read it back, a later episode could invent, alter or drop a prior
    call and still validate. Every seam that proves a chain (writer preflight, writer
    postcondition, recovery, canonical loader, verified tree builder, Evidence export) reaches
    this function, so the rule lands at all of them at once instead of six times over."""
    problems: list[str] = []
    problems.extend(validate_ledger_chain(list(by_id.values())))
    # F1 (round 15): a task's history is monotonic. Round 14 stopped a later episode rewriting a
    # run it admitted to; this stops it DENYING the run ever happened by omitting the ledger
    # entirely — an erasure no per-episode check and no ledger comparison could see.
    problems.extend(validate_task_lifecycle_chain(list(by_id.values())))
    ord_of = {eid: m.episode_ordinal for eid, m in by_id.items()}
    by_ordinal = {m.episode_ordinal: eid for eid, m in by_id.items()}
    for eid, m in by_id.items():
        seen_edge: set[str] = set()
        for pe in m.prior_episode_ids:
            if pe in seen_edge:
                problems.append(f"episode {eid} lists prior {pe} more than once")
            seen_edge.add(pe)
            if pe == eid:
                problems.append(f"episode {eid} references itself as a prior")
            elif pe not in by_id:
                problems.append(f"episode {eid} references unknown prior {pe}")
            elif ord_of.get(pe, 0) >= m.episode_ordinal:
                problems.append(
                    f"episode {eid} (ordinal {m.episode_ordinal}) references prior {pe} "
                    f"with ordinal {ord_of.get(pe)} — not strictly earlier (cycle/future)")

        # F8: the EXACT ascending history + immediate predecessor.
        n = m.episode_ordinal
        expected_prior = [by_ordinal[o] for o in range(1, n) if o in by_ordinal]
        if list(m.prior_episode_ids) != expected_prior:
            problems.append(
                f"episode {eid} prior_episode_ids {list(m.prior_episode_ids)} is not the exact "
                f"ascending history {expected_prior}")
        expected_prev = by_ordinal.get(n - 1, "") if n > 1 else ""
        if (m.previous_episode_id or "") != expected_prev:
            problems.append(
                f"episode {eid} previous_episode_id {m.previous_episode_id!r} is not the "
                f"immediate predecessor {expected_prev!r} (ordinal {n - 1})")

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {eid: WHITE for eid in by_id}

    def _dfs(node: str, stack: list[str]) -> bool:
        color[node] = GRAY
        for pe in by_id[node].prior_episode_ids:
            if pe not in by_id:
                continue
            if color[pe] == GRAY:
                problems.append("cycle in prior-episode graph: "
                                + " -> ".join(stack + [node, pe]))
                return True
            if color[pe] == WHITE and _dfs(pe, stack + [node]):
                return True
        color[node] = BLACK
        return False

    for eid in by_id:
        if color[eid] == WHITE and _dfs(eid, []):
            break
    return problems


def validate_episode_artifacts_anchored(root_fd: int, episode_id: str,
                                        manifest: "RunManifestV1") -> list[str]:
    """F7: verify an episode's per-call artifacts through the CANONICAL anchored trust chain.

    Reads each ``calls/<artifact>`` ONLY through held, symlink-refusing directory fds; every
    artifact must exist, hash to its declared ``artifact_sha256`` and equal the manifest's
    canonical bytes; no undeclared artifact may sit in ``calls/``. No ``Path`` reads. This is
    the single validator the index checker, the latest/episode loaders and export all call, so
    a call artifact never enters the trust chain by a weaker path (F084/F140 reuse it too)."""
    problems: list[str] = []
    if not _safe_component(episode_id):
        return [f"unsafe episode id {episode_id!r}"]
    try:
        subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                        error_cls=ManifestError, noun="run-manifest")
    except _fs.MissingComponent:
        return [f"{MANIFESTS_SUBDIR}/ is missing"]
    try:
        ep_fd = _fs.open_verified_dir(episode_id, dir_fd=subs_fd,
                                      error_cls=ManifestError, noun="run-manifest")
    except _fs.MissingComponent:
        os.close(subs_fd)
        return [f"episode {episode_id} directory is missing"]
    finally:
        os.close(subs_fd)
    try:
        declared_calls = [c for c in manifest.calls if c.artifact]
        try:
            calls_fd = _fs.open_verified_dir(CALLS_SUBDIR, dir_fd=ep_fd,
                                             error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            if declared_calls:
                return [f"episode {episode_id}: {CALLS_SUBDIR}/ missing but manifest declares "
                        f"{len(declared_calls)} call artifact(s)"]
            return problems
        try:
            on_disk = set(_fs.list_dir_names(calls_fd, error_cls=ManifestError,
                                             noun="run-manifest"))
            declared_names: set[str] = set()
            for c in declared_calls:
                name = c.artifact.split("/", 1)[1] if "/" in c.artifact else c.artifact
                declared_names.add(name)
                raw = _fs.read_verified_file(name, calls_fd, error_cls=ManifestError,
                                             noun="call artifact")
                if raw is None:
                    problems.append(f"episode {episode_id}: missing call artifact {name!r}")
                    continue
                if hashlib.sha256(raw).hexdigest() != c.artifact_sha256:
                    problems.append(
                        f"episode {episode_id}: call artifact {name!r} sha256 mismatch")
                if raw != c.canonical_artifact_bytes():
                    problems.append(
                        f"episode {episode_id}: call artifact {name!r} bytes are not canonical")
            extra = on_disk - declared_names
            if extra:
                problems.append(f"episode {episode_id}: undeclared call artifacts "
                                f"{sorted(extra)}")
        finally:
            os.close(calls_fd)
        # F1 (round 12): the LEDGERS are canonical members of the episode, verified exactly like
        # the call artifacts — present, canonical, hash-bound, and nothing undeclared beside them.
        problems.extend(_validate_episode_ledgers_anchored(ep_fd, episode_id, manifest))
    finally:
        os.close(ep_fd)
    return problems


def _validate_episode_ledgers_anchored(ep_fd: int, episode_id: str,
                                       manifest: "RunManifestV1") -> list[str]:
    problems: list[str] = []
    # F3 (round 14): duplicate refs are detected BEFORE any dict is keyed by them. The old
    # comprehension silently dropped a declaration when two ledgers mapped to one filename, so a
    # crafted tree with one physical file backing two ledgers read as complete and consistent.
    declared: dict[str, RunCallLedgerV1] = {}
    for lg in manifest.call_ledgers:
        name = lg.ref().split("/", 1)[1]
        prior = declared.get(name)
        if prior is not None:
            problems.append(
                f"episode {episode_id}: call ledgers {prior.task_id}/{prior.run_id} and "
                f"{lg.task_id}/{lg.run_id} both claim artifact {name!r}; refusing to read one "
                f"file as two ledgers")
            continue
        declared[name] = lg
    try:
        led_fd = _fs.open_verified_dir(LEDGERS_SUBDIR, dir_fd=ep_fd, error_cls=ManifestError,
                                       noun="run-manifest")
    except _fs.MissingComponent:
        if declared:
            problems.append(
                f"episode {episode_id}: {LEDGERS_SUBDIR}/ is missing but the manifest declares "
                f"{len(declared)} call ledger(s)")
        return problems
    except ManifestError as exc:
        return [f"episode {episode_id}: {LEDGERS_SUBDIR}/ {exc}"]
    try:
        on_disk = set(_fs.list_dir_names(led_fd, error_cls=ManifestError, noun="run-manifest"))
        for name, lg in sorted(declared.items()):
            raw = _fs.read_verified_file(name, led_fd, max_bytes=_S.MAX_CALL_ARTIFACT_BYTES,
                                         error_cls=ManifestError, noun="call ledger")
            if raw is None:
                problems.append(f"episode {episode_id}: missing call ledger {name!r}")
                continue
            if raw != lg.canonical_bytes():
                problems.append(
                    f"episode {episode_id}: call ledger {name!r} bytes are not the manifest's "
                    f"canonical ledger")
            try:
                stored = decode_run_call_ledger_v1(raw)          # strict, untrusted bytes
            except (ManifestError, _S.SchemaError) as exc:
                problems.append(f"episode {episode_id}: unreadable call ledger {name!r}: "
                                f"{str(exc)[:120]}")
                continue
            if stored != lg:
                problems.append(
                    f"episode {episode_id}: call ledger {name!r} does not match the manifest's")
        extra = on_disk - set(declared)
        if extra:
            problems.append(f"episode {episode_id}: undeclared call ledgers {sorted(extra)}")
    finally:
        os.close(led_fd)
    return problems


def validate_index_and_tree(evidence_dir: str | Path, *, job_id: str = "") -> list[str]:
    """Strict index trust-chain validation (F8) over ANCHORED, symlink-refusing reads (F9).

    Verifies every index invariant: version, unique episode ids, safe refs, each indexed
    manifest resolves and its directory name/job/status/created_at/record hash match the
    entry, exactly-one latest, root mirror equals the latest canonical episode, no extra
    unindexed episode dir, no missing indexed episode, no self-referential prior episode.
    Returns the list of problems (empty == valid)."""
    problems: list[str] = []
    try:
        index, root_fd = load_index_verified(evidence_dir)
    except ManifestError as exc:
        return [str(exc)]
    if index is None:
        os.close(root_fd)
        return ["no run_manifest_index.json"]
    try:
        if index.get("index_v") != 1:
            problems.append(f"unsupported index_v {index.get('index_v')}")
        entries = index.get("episodes")
        if not isinstance(entries, list) or not entries:
            problems.append("index has no episodes")
            entries = entries if isinstance(entries, list) else []

        ids = [str(e.get("episode_id", "")) for e in entries]
        if len(ids) != len(set(ids)):
            problems.append("duplicate episode ids in index")
        refs = [str(e.get("manifest_ref", "")) for e in entries]
        if len(refs) != len(set(refs)):
            problems.append("duplicate manifest refs in index")

        by_id: dict[str, RunManifestV1] = {}
        for e in entries:
            eid = str(e.get("episode_id", ""))
            ref = str(e.get("manifest_ref", ""))
            if not _safe_component(eid):
                problems.append(f"unsafe indexed episode id {eid!r}")
                continue
            expect_ref = f"{MANIFESTS_SUBDIR}/{eid}/{MANIFEST_FILENAME}"
            if ref != expect_ref:
                problems.append(f"episode {eid} ref {ref!r} != canonical {expect_ref!r}")
            try:
                m = _read_episode_manifest_anchored(root_fd, eid)
            except ManifestError as exc:
                problems.append(f"episode {eid}: {exc}")
                continue
            by_id[eid] = m
            if m.episode_id != eid:
                problems.append(f"episode dir {eid} holds manifest for {m.episode_id}")
            if job_id and m.job_id != job_id:
                problems.append(f"episode {eid} job_id {m.job_id} != owning job {job_id}")
            if str(e.get("status", "")) != m.status:
                problems.append(f"episode {eid} index status != manifest status")
            if str(e.get("created_at", "")) != m.created_at:
                problems.append(f"episode {eid} index created_at != manifest created_at")
            if str(e.get("record_sha256", "")) != m.record_sha256():
                problems.append(f"episode {eid} index record_sha256 != actual manifest hash")
            # F5: the index's ordinal/previous MUST match the canonical manifest's — the index
            # cannot claim a different order than the signed episode records.
            if int(e.get("episode_ordinal", 0) or 0) != m.episode_ordinal:
                problems.append(f"episode {eid} index ordinal != manifest ordinal")
            if str(e.get("previous_episode_id", "") or "") != m.previous_episode_id:
                problems.append(f"episode {eid} index previous_episode_id != manifest")
            for pe in m.prior_episode_ids:
                if pe == eid:
                    problems.append(f"episode {eid} lists itself as a prior episode")
            # F7: the episode's call artifacts must be the canonical anchored trust chain.
            problems.extend(validate_episode_artifacts_anchored(root_fd, eid, m))

        # F5: ordinals must be UNIQUE, 1-based and CONTIGUOUS across the canonical episodes,
        # and the latest must be the MAXIMUM-ordinal episode. This is what makes a rollback
        # (re-pointing latest at an older, lower-ordinal episode) detectable.
        ordinals = [(eid, m.episode_ordinal) for eid, m in by_id.items()]
        ords = [o for _, o in ordinals]
        if len(ords) != len(set(ords)):
            problems.append("duplicate episode ordinals")
        if ords and sorted(ords) != list(range(1, len(ords) + 1)):
            problems.append(f"episode ordinals are not 1..N contiguous: {sorted(ords)}")
        max_ord_id = ""
        if ordinals:
            max_ord_id = max(ordinals, key=lambda t: t[1])[0]
        # F6: the prior-episode graph must be a DAG that respects the ordinal order (every edge
        # points to a strictly-lower, existing ordinal; no self/cycle/future/unknown).
        problems.extend(_validate_episode_graph(by_id))

        latest = str(index.get("latest_episode_id", ""))
        if ids.count(latest) != 1:
            problems.append("latest_episode_id is not present exactly once")
        elif max_ord_id and latest != max_ord_id:
            problems.append(f"latest_episode_id {latest} is not the max-ordinal episode "
                            f"{max_ord_id} (episode rollback)")
        if latest in by_id:
            # root mirror must equal the latest canonical episode
            try:
                raw = _anchored_read(root_fd, MANIFEST_FILENAME)
            except ManifestError as exc:
                raw = None
                problems.append(str(exc))
            if raw is None:
                problems.append("no root manifest mirror")
            else:
                try:
                    root_m = decode_run_manifest_v1(raw)      # F13: strict root mirror
                    # F11: the mirror's stored bytes must be canonical...
                    require_canonical_bytes(raw, root_m, where="root mirror")
                    # ...and byte-for-byte identical to the latest canonical episode bytes.
                    if bytes(raw) != by_id[latest].canonical_bytes():
                        problems.append("root mirror bytes != latest canonical episode bytes")
                except (ValueError, ManifestError, _S.SchemaError) as exc:
                    problems.append(f"root manifest mirror is unreadable: {exc}")

        # no extra unindexed episode directory / no missing indexed one
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
            try:
                on_disk = {n for n in _fs.list_dir_names(subs_fd, error_cls=ManifestError,
                                                         noun="run-manifest")}
            finally:
                os.close(subs_fd)
            extra = on_disk - set(ids)
            if extra:
                problems.append(f"unindexed episode directories: {sorted(extra)}")
            missing = set(ids) - on_disk
            if missing:
                problems.append(f"indexed episodes missing on disk: {sorted(missing)}")
        except ManifestError as exc:
            problems.append(str(exc))
    finally:
        os.close(root_fd)
    return problems


@dataclass(frozen=True)
class CanonicalLoadResult:
    """F10: a typed result for the CLI canonical load. ``kind`` is one of ``ok`` (a valid latest
    manifest is attached), ``no_manifest`` (the evidence tree carries NO F012 manifest artifacts
    at all — a legacy/uncovered job), or ``integrity_error`` (manifest artifacts exist but the
    trust chain is inconsistent/partial — exit 1, never mistaken for a missing manifest)."""
    kind: str
    manifest: "RunManifestV1 | None" = None
    detail: str = ""


def _open_dir_anchored_or_missing(path: str | Path) -> int | None:
    """F16: open a directory by walking from ``/`` on VERIFIED handles.

    Returns the fd, or ``None`` when a component is GENUINELY ABSENT — which is how a legacy
    job with no evidence directory stays distinguishable from an unsafe one. A symlinked or
    otherwise unverifiable component raises ``ManifestError`` and is never followed. No
    name-based ``Path.is_dir()`` trust decision is involved."""
    p = Path(os.path.normpath(os.path.abspath(str(path))))
    parts = [x for x in p.parts if x not in ("", os.sep)]
    cur = _fs.open_verified_dir(os.sep, error_cls=ManifestError, noun="run-manifest")
    try:
        for comp in parts:
            try:
                nxt = _fs.open_verified_dir(comp, dir_fd=cur, error_cls=ManifestError,
                                            noun="run-manifest")
            except _fs.MissingComponent:
                return None
            os.close(cur)
            cur = nxt
        fd, cur = cur, None
        return fd
    finally:
        if cur is not None:
            os.close(cur)


def load_latest_manifest_for_cli(evidence_dir: str | Path, *, job_id: str = ""
                                 ) -> CanonicalLoadResult:
    """F1/F10/F16: load the latest manifest for the CLI through ANCHORED reads only.

    NOTHING escapes: every expected failure for untrusted/corrupt disk state — a ManifestError,
    a bounded OSError, malformed JSON, an unsupported schema — becomes a typed
    ``integrity_error`` once ANY manifest artifact is present, so the public CLI exits 1 instead
    of emitting a traceback. A tree with no manifest artifacts at all stays the legacy
    ``no_manifest``. Programming errors are NOT swallowed. There is no name-based
    ``Path.is_dir()`` trust decision: the anchored root API decides existence, and a symlinked
    parent is refused rather than followed."""
    # F16: existence is decided by the ANCHORED api, never `Path.is_dir()`.
    try:
        root_fd = _open_dir_anchored_or_missing(evidence_dir)
    except (ManifestError, OSError) as exc:
        # Present but not safely anchorable (symlinked component, permission failure) — an
        # integrity problem, never a missing manifest.
        return CanonicalLoadResult("integrity_error", detail=str(exc))
    if root_fd is None:
        return CanonicalLoadResult("no_manifest", detail="no evidence directory")
    try:
        has_index = _anchored_read(root_fd, MANIFEST_INDEX_FILENAME,
                                   noun="manifest index") is not None
        has_mirror = _anchored_read(root_fd, MANIFEST_FILENAME) is not None
        has_episodes = False
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
            try:
                has_episodes = bool(_fs.list_dir_names(subs_fd, error_cls=ManifestError,
                                                       noun="run-manifest"))
            finally:
                os.close(subs_fd)
        except _fs.MissingComponent:
            has_episodes = False
    except (ManifestError, _S.SchemaError, OSError, ValueError) as exc:
        return CanonicalLoadResult("integrity_error", detail=str(exc))
    finally:
        os.close(root_fd)

    if not (has_index or has_mirror or has_episodes):
        return CanonicalLoadResult("no_manifest", detail="no run manifest artifacts present")
    try:
        m = load_latest_manifest_verified(evidence_dir, job_id=job_id)
    except (ManifestError, _S.SchemaError) as exc:
        return CanonicalLoadResult("integrity_error", detail=str(exc))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        return CanonicalLoadResult("integrity_error", detail=f"{type(exc).__name__}: {exc}")
    return CanonicalLoadResult("ok", manifest=m)


#: F11: the export ceilings are NOT a separate contract — they are the SAME shared limits the
#: writer, decoder, typed validation, recovery and canonical loader apply, so a record the
#: writer accepts can never be refused by the exporter for size alone.
MANIFEST_MAX_FILE_BYTES = _S.MAX_EPISODE_MANIFEST_BYTES
MANIFEST_MAX_TREE_BYTES = _S.MAX_TREE_BYTES


def build_verified_manifest_tree(evidence_dir: str | Path, *, job_id: str = ""
                                 ) -> tuple[dict[str, bytes], list[str]]:
    """F5: VALIDATE FIRST, then return ONLY the allowlisted verified bytes for export.

    Unlike a blind copy-everything read, this determines the EXACT declared set from the index
    and each episode manifest, then anchored-reads ONLY those files — the root mirror, the index,
    each indexed episode manifest, and each call artifact its manifest declares — verifying every
    hash and canonical byte string and enforcing per-file / whole-tree size ceilings. An extra
    episode directory, an undeclared call artifact, a missing declared file, or an oversized file
    is a PROBLEM and its bytes are NOT included. The caller copies the returned map only when
    ``problems`` is empty, so undeclared/secret/oversized data can never enter the bundle."""
    files: dict[str, bytes] = {}
    problems: list[str] = []
    total = 0

    def _bounded_read(dir_fd: int, name: str, noun: str) -> bytes | None:
        try:
            return _fs.read_verified_file(name, dir_fd, max_bytes=MANIFEST_MAX_FILE_BYTES,
                                          error_cls=ManifestError, noun=noun)
        except ManifestError as exc:
            problems.append(f"{noun} {name!r}: {exc}")
            return None

    try:
        index, root_fd = load_index_verified(evidence_dir)
    except _fs.MissingComponent:
        return {}, ["evidence directory does not exist"]
    except (ManifestError, _S.SchemaError, OSError, ValueError, UnicodeDecodeError) as exc:
        # F2: the contract is (files, problems) — a malformed/oversized/unreadable index is a
        # PROBLEM, never an escaping exception, and no unverified bytes are returned.
        return {}, [f"manifest index: {exc}"]
    try:
        if index is None:
            return {}, []                        # no index → nothing declared to export
        declared_eids = [str(e.get("episode_id", "")) for e in index.get("episodes", [])]

        idx_raw = _bounded_read(root_fd, MANIFEST_INDEX_FILENAME, "manifest index")
        if idx_raw is not None:
            files[MANIFEST_INDEX_FILENAME] = idx_raw
            total += len(idx_raw)
        mir_raw = _bounded_read(root_fd, MANIFEST_FILENAME, "run-manifest")
        if mir_raw is not None:
            files[MANIFEST_FILENAME] = mir_raw
            total += len(mir_raw)

        # Detect EXTRA (unindexed) episode directories — they are never copied.
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            subs_fd = None
        on_disk_eids: set[str] = set()
        if subs_fd is not None:
            try:
                on_disk_eids = set(_fs.list_dir_names(subs_fd, error_cls=ManifestError,
                                                      noun="run-manifest"))
            finally:
                os.close(subs_fd)
        extra_eps = on_disk_eids - set(declared_eids)
        if extra_eps:
            problems.append(f"unindexed episode directories (not exported): {sorted(extra_eps)}")
        # F14: the manifest tree root allows EXACTLY the mirror, the index and the
        # run_manifests/ directory. Any other member is rejected, not merely skipped.
        try:
            root_members = set(_fs.list_dir_names(root_fd, error_cls=ManifestError,
                                                  noun="run-manifest"))
        except ManifestError:
            root_members = set()
        allowed_root = {MANIFEST_FILENAME, MANIFEST_INDEX_FILENAME, MANIFESTS_SUBDIR,
                        MANIFEST_INTEGRITY_FILE}
        extra_root = {m for m in root_members - allowed_root
                      if m.startswith("run_manifest")}
        if extra_root:
            problems.append(f"unexpected manifest-tree root member(s): {sorted(extra_root)}")

        for eid in declared_eids:
            if not _safe_component(eid):
                problems.append(f"unsafe indexed episode id {eid!r}")
                continue
            e_files, e_problems, e_bytes = _verified_episode_export(root_fd, eid, _bounded_read)
            files.update(e_files)
            problems.extend(e_problems)
            total += e_bytes

        if total > MANIFEST_MAX_TREE_BYTES:
            problems.append(f"manifest tree exceeds the export ceiling ({total} bytes)")
    except (ManifestError, _S.SchemaError, OSError, ValueError, UnicodeDecodeError) as exc:
        return {}, [*problems, f"manifest tree: {exc}"]   # F2: no unverified bytes escape
    finally:
        os.close(root_fd)
    return files, problems


def _verified_episode_export(root_fd: int, eid: str, bounded_read
                             ) -> tuple[dict[str, bytes], list[str], int]:
    files: dict[str, bytes] = {}
    problems: list[str] = []
    total = 0
    try:
        subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                        error_cls=ManifestError, noun="run-manifest")
    except _fs.MissingComponent:
        return files, [f"{MANIFESTS_SUBDIR}/ missing for episode {eid}"], 0
    try:
        try:
            ep_fd = _fs.open_verified_dir(eid, dir_fd=subs_fd, error_cls=ManifestError,
                                          noun="run-manifest")
        except _fs.MissingComponent:
            return files, [f"indexed episode {eid} missing on disk"], 0
    finally:
        os.close(subs_fd)
    try:
        m_raw = bounded_read(ep_fd, MANIFEST_FILENAME, "run manifest")
        if m_raw is None:
            return files, [f"episode {eid} has no manifest"], 0
        try:
            manifest = decode_run_manifest_v1(m_raw)         # F13: strict export decode
            _require_valid_manifest(manifest, f"episode {eid}")
        except (ValueError, ManifestError) as exc:
            return files, [f"episode {eid} manifest invalid: {exc}"], 0
        rel_m = f"{MANIFESTS_SUBDIR}/{eid}/{MANIFEST_FILENAME}"
        files[rel_m] = m_raw
        total += len(m_raw)

        # F14: an episode directory allows EXACTLY ``run_manifest.json`` and ``calls/``. An
        # extra file, directory, temp file or editor backup is REJECTED (and never copied).
        try:
            members = set(_fs.list_dir_names(ep_fd, error_cls=ManifestError,
                                             noun="run-manifest"))
            # F1 (round 12): `call_ledgers/` is a canonical member of the episode.
            extra_members = members - {MANIFEST_FILENAME, CALLS_SUBDIR, LEDGERS_SUBDIR}
            if extra_members:
                problems.append(f"episode {eid}: unexpected member(s) in the episode root: "
                                f"{sorted(extra_members)}")
        except ManifestError as exc:
            problems.append(f"episode {eid}: could not enumerate the episode root: {exc}")

        declared = {c.artifact.split("/", 1)[1] if "/" in c.artifact else c.artifact: c
                    for c in manifest.calls if c.artifact}
        # F1 (round 12): export the LEDGERS — verified, allowlisted, hash-bound.
        led_declared = {lg.ref().split("/", 1)[1]: lg for lg in manifest.call_ledgers}
        try:
            led_fd = _fs.open_verified_dir(LEDGERS_SUBDIR, dir_fd=ep_fd,
                                           error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            led_fd = None
            if led_declared:
                problems.append(f"episode {eid}: {LEDGERS_SUBDIR}/ missing but "
                                f"{len(led_declared)} ledger(s) declared")
        if led_fd is not None:
            try:
                led_on_disk = set(_fs.list_dir_names(led_fd, error_cls=ManifestError,
                                                     noun="run-manifest"))
                led_extra = led_on_disk - set(led_declared)
                if led_extra:
                    problems.append(f"episode {eid}: undeclared call ledgers (not exported): "
                                    f"{sorted(led_extra)}")
                for name, lg in sorted(led_declared.items()):
                    raw = bounded_read(led_fd, name, "call ledger")
                    if raw is None:
                        problems.append(f"episode {eid}: missing call ledger {name!r}")
                        continue
                    if raw != lg.canonical_bytes():
                        problems.append(f"episode {eid}: call ledger {name!r} is not the "
                                        f"manifest's canonical ledger")
                        continue
                    files[f"{MANIFESTS_SUBDIR}/{eid}/{LEDGERS_SUBDIR}/{name}"] = raw
                    total += len(raw)
            finally:
                os.close(led_fd)

        try:
            calls_fd = _fs.open_verified_dir(CALLS_SUBDIR, dir_fd=ep_fd,
                                             error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            if declared:
                problems.append(f"episode {eid}: {CALLS_SUBDIR}/ missing but "
                                f"{len(declared)} artifact(s) declared")
            return files, problems, total
        try:
            on_disk = set(_fs.list_dir_names(calls_fd, error_cls=ManifestError,
                                             noun="run-manifest"))
            extra = on_disk - set(declared)
            if extra:
                problems.append(f"episode {eid}: undeclared call artifacts (not exported): "
                                f"{sorted(extra)}")
            for name, call in declared.items():
                raw = bounded_read(calls_fd, name, "call artifact")
                if raw is None:
                    problems.append(f"episode {eid}: missing/oversized call artifact {name!r}")
                    continue
                if hashlib.sha256(raw).hexdigest() != call.artifact_sha256:
                    problems.append(f"episode {eid}: artifact {name!r} sha256 mismatch")
                    continue
                if raw != call.canonical_artifact_bytes():
                    problems.append(f"episode {eid}: artifact {name!r} bytes are not canonical")
                    continue
                files[f"{MANIFESTS_SUBDIR}/{eid}/{CALLS_SUBDIR}/{name}"] = raw
                total += len(raw)
        finally:
            os.close(calls_fd)
    finally:
        os.close(ep_fd)
    return files, problems, total


#: The tree reader's word for "there is nothing here at all" — genuine ABSENCE, which for an
#: unmarked pre-F012 job is legacy/uncovered rather than corruption.
_NO_EVIDENCE_DIR = "evidence directory does not exist"


def manifest_tree_is_present(evidence_dir: str | Path) -> tuple[bool, list[str]]:
    """F10: does ANY manifest artifact exist for this job?

    Presence is decided on the RAW anchored tree, NOT on the verified allowlist: a tree broken
    badly enough that nothing survives verification (a missing index leaves no episode declared)
    still EXISTS, and must be validated rather than waved through as "legacy". Only a genuinely
    empty tree — or no evidence directory at all — is absence.

    Returns ``(present, problems)``.
    """
    files, problems = read_manifest_tree_bytes_anchored(evidence_dir)
    problems = [p for p in problems if p != _NO_EVIDENCE_DIR]
    return (bool(files) or bool(problems)), problems


def read_manifest_tree_bytes_anchored(evidence_dir: str | Path,
                                      ) -> tuple[dict[str, bytes], list[str]]:
    """F8: read the WHOLE manifest tree (root mirror, index, every episode manifest and its
    call artifacts) as bundle-relative bytes, ONLY through held, symlink-refusing directory
    fds. Never a ``Path`` read, so the export copies verified bytes and can never be lured into
    reading a file outside the evidence tree — even when the job is BLOCKED. Returns
    ``(files, problems)``; ``files`` maps bundle-relative path -> exact verified bytes."""
    files: dict[str, bytes] = {}
    problems: list[str] = []
    # F12: existence is decided by the ANCHORED probe — this helper advertises anchored safety,
    # so it must not make an initial name-based trust decision.
    root_fd = _open_dir_anchored_or_missing(evidence_dir)
    if root_fd is None:
        return files, [_NO_EVIDENCE_DIR]
    try:
        raw = _anchored_read(root_fd, MANIFEST_FILENAME)
        if raw is not None:
            files[MANIFEST_FILENAME] = raw
        idx_raw = _anchored_read(root_fd, MANIFEST_INDEX_FILENAME, noun="manifest index")
        if idx_raw is not None:
            files[MANIFEST_INDEX_FILENAME] = idx_raw
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            return files, problems
        try:
            names = sorted(_fs.list_dir_names(subs_fd, error_cls=ManifestError,
                                              noun="run-manifest"))
            for eid in names:
                if not _safe_component(eid):
                    problems.append(f"unsafe episode dir name {eid!r}")
                    continue
                try:
                    ep_fd = _fs.open_verified_dir(eid, dir_fd=subs_fd,
                                                  error_cls=ManifestError, noun="run-manifest")
                except _fs.MissingComponent:
                    continue
                except ManifestError as exc:
                    # A symlinked episode component is REFUSED, not followed — the outside tree
                    # it points at never enters ``files`` (F8). Record the refusal and move on.
                    problems.append(f"episode {eid}: {exc}")
                    continue
                try:
                    m_raw = _anchored_read(ep_fd, MANIFEST_FILENAME)
                    if m_raw is None:
                        problems.append(f"episode {eid} has no manifest")
                        continue
                    files[f"{MANIFESTS_SUBDIR}/{eid}/{MANIFEST_FILENAME}"] = m_raw
                    try:
                        calls_fd = _fs.open_verified_dir(CALLS_SUBDIR, dir_fd=ep_fd,
                                                         error_cls=ManifestError,
                                                         noun="run-manifest")
                    except _fs.MissingComponent:
                        calls_fd = None
                    except ManifestError as exc:
                        problems.append(f"episode {eid}: {CALLS_SUBDIR}/ {exc}")
                        calls_fd = None
                    if calls_fd is not None:
                        try:
                            for cname in sorted(_fs.list_dir_names(
                                    calls_fd, error_cls=ManifestError, noun="run-manifest")):
                                c_raw = _anchored_read(calls_fd, cname, noun="call artifact")
                                if c_raw is not None:
                                    files[f"{MANIFESTS_SUBDIR}/{eid}/{CALLS_SUBDIR}/"
                                          f"{cname}"] = c_raw
                        finally:
                            os.close(calls_fd)
                finally:
                    os.close(ep_fd)
        finally:
            os.close(subs_fd)
    finally:
        os.close(root_fd)
    return files, problems


def load_latest_manifest_verified(evidence_dir: str | Path, *, job_id: str = ""
                                  ) -> RunManifestV1:
    """The canonical latest-episode loader (F11). Validates the whole index trust chain and
    returns the latest canonical episode manifest. Raises ``ManifestError`` if the index,
    episodes and root mirror disagree — the CLI turns that into an integrity error, never a
    drift/incomplete verdict."""
    problems = validate_index_and_tree(evidence_dir, job_id=job_id)
    if problems:
        raise ManifestError("manifest trust chain is inconsistent: "
                            + "; ".join(problems)[:400])
    index, root_fd = load_index_verified(evidence_dir)
    try:
        latest = str(index.get("latest_episode_id", ""))
        return _read_episode_manifest_anchored(root_fd, latest)
    finally:
        os.close(root_fd)


def load_episode_manifest_verified(evidence_dir: str | Path, episode_id: str, *,
                                   expected_job_id: str = "") -> RunManifestV1:
    """F9: load ONE named episode's manifest through the ANCHORED trust chain.

    The whole index+tree is validated first (so a rollback / broken graph / tampered artifact
    is an integrity error, not silently loaded), then the requested episode's canonical record
    is read via held, symlink-refusing fds and its artifacts re-verified. Every production
    idempotent-retry / repair / export path uses this instead of a raw ``Path`` read, so no
    trust read can follow a symlink out of the evidence tree."""
    problems = validate_index_and_tree(evidence_dir, job_id=expected_job_id)
    if problems:
        raise ManifestError("manifest trust chain is inconsistent: "
                            + "; ".join(problems)[:400])
    if not _safe_component(episode_id):
        raise ManifestError(f"unsafe episode id {episode_id!r}")
    index, root_fd = load_index_verified(evidence_dir)
    try:
        if index is None:
            raise ManifestError("no run_manifest_index.json")
        ids = {str(e.get("episode_id", "")) for e in index.get("episodes", [])}
        if episode_id not in ids:
            raise ManifestError(f"episode {episode_id} is not in the index")
        m = _read_episode_manifest_anchored(root_fd, episode_id)
        if expected_job_id and m.job_id != expected_job_id:
            raise ManifestError(
                f"episode {episode_id} job_id {m.job_id!r} != expected {expected_job_id!r}")
        art = validate_episode_artifacts_anchored(root_fd, episode_id, m)
        if art:
            raise ManifestError("; ".join(art)[:400])
        return m
    finally:
        os.close(root_fd)


def ensure_evidence_root_anchored(evidence_dir: str | Path) -> None:
    """F11: create the Evidence root through the ANCHORED (walk-from-/) creator, never a
    name-based ``mkdir(parents=True)`` that could traverse an unverified symlink chain."""
    fd = _fs.anchor_root(evidence_dir, error_cls=ManifestError, noun="run-manifest",
                         create=True, dir_mode=MANIFEST_DIR_MODE)
    os.close(fd)


def episode_manifest_exists_anchored(evidence_dir: str | Path, episode_id: str) -> bool:
    """F11: decide whether an episode manifest already exists using ONLY anchored,
    symlink-refusing directory fds — never ``Path.is_file()`` on an unverified name."""
    if not _safe_component(episode_id):
        raise ManifestError(f"unsafe episode id {episode_id!r}")
    root_fd = _open_dir_anchored_or_missing(evidence_dir)   # F15: anchored existence
    if root_fd is None:
        return False
    try:
        try:
            subs_fd = _fs.open_verified_dir(MANIFESTS_SUBDIR, dir_fd=root_fd,
                                            error_cls=ManifestError, noun="run-manifest")
        except _fs.MissingComponent:
            return False
        try:
            try:
                ep_fd = _fs.open_verified_dir(episode_id, dir_fd=subs_fd,
                                              error_cls=ManifestError, noun="run-manifest")
            except _fs.MissingComponent:
                return False
            try:
                return _anchored_read(ep_fd, MANIFEST_FILENAME) is not None
            finally:
                os.close(ep_fd)
        finally:
            os.close(subs_fd)
    finally:
        os.close(root_fd)


def read_canonical_episode_order(evidence_dir: str | Path, *, job_id: str = ""
                                 ) -> list[dict[str, Any]]:
    """F10: the CANONICAL episode order, read + fully validated through the anchored trust
    chain, in ASCENDING ordinal order. Each entry is ``{episode_id, episode_ordinal,
    previous_episode_id, status, created_at}`` taken from the signed episode manifests. Returns
    ``[]`` when no index exists yet (the first episode). Raises ``ManifestError`` if the on-disk
    trust chain is inconsistent — a caller must NEVER derive the next ordinal from a broken or
    tampered index."""
    try:
        index, root_fd = load_index_verified(evidence_dir)
    except _fs.MissingComponent:                  # F15: genuinely absent, not an integrity fault
        return []
    if index is None:
        os.close(root_fd)
        return []
    os.close(root_fd)
    problems = validate_index_and_tree(evidence_dir, job_id=job_id)
    if problems:
        raise ManifestError("cannot derive episode order from an inconsistent index: "
                            + "; ".join(problems)[:400])
    index, root_fd = load_index_verified(evidence_dir)
    try:
        order: list[dict[str, Any]] = []
        for eid in sorted({str(e.get("episode_id", "")) for e in index.get("episodes", [])}):
            m = _read_episode_manifest_anchored(root_fd, eid)
            order.append({
                "episode_id": m.episode_id,
                "episode_ordinal": m.episode_ordinal,
                "previous_episode_id": m.previous_episode_id,
                "status": m.status,
                "created_at": m.created_at,
            })
    finally:
        os.close(root_fd)
    order.sort(key=lambda e: int(e["episode_ordinal"]))
    return order


# ---------------------------------------------------------------------------
# Current-state candidate (F1, F2)
# ---------------------------------------------------------------------------


def _job_is_resumable(job: Any) -> bool:
    """F12: a job whose next episode would RESUME into the existing job-owned worktree — i.e. a
    stopped/blocked/planned/running job, as opposed to a completed job whose worktree may have
    been intentionally cleaned (the documented rerun-from-recorded-target case)."""
    status = str(getattr(job, "status", "") or "")
    if status != "completed":
        return True
    # A completed job that still owns an un-cleaned worktree is still resumable-ish; the
    # documented target-based semantics apply only once the worktree was cleaned.
    return str(getattr(job, "worktree_cleanup_status", "") or "") not in ("clean", "")


def build_current_candidate(reference: RunManifestV1, job: Any) -> RunManifestV1:
    """Build the manifest the CURRENT environment WOULD produce, for check mode.

    Freshly inspects the current target repo and resolves current config/env/models; does NOT
    reuse the reference's historical values, and does NOT reconstruct per-call assembled
    prompts (a worktree replay — F140), so calls are empty and coverage INCOMPLETE.

    F11: the episode-start WORKSPACE tree is a material input to the next episode. For a
    resumable job whose job-owned worktree still exists, this freshly recomputes that tree from
    the CURRENT workspace instead of trusting the historical ``episode_start_workspace_tree`` —
    so a workspace mutation is detected as drift. If the workspace exists but cannot be
    reconstructed, coverage is INCOMPLETE (never a false "same"). A completed/cleaned job whose
    workspace is gone follows the documented rerun-from-recorded-target semantics."""
    snap = build_input_snapshot(job, inspect_target=True)
    workspace_problems: list[str] = []
    ws_path = str(getattr(job, "job_workspace_path", "") or "")
    # F11/F12 (round 11): the workspace is a material input, and inspecting it must not CHANGE
    # it. The old check ran `git add -A` + `git write-tree`, which writes blobs and tree objects
    # into the repository being inspected and can fire clean filters — a "check" that mutates the
    # thing it is checking is not a check. It also trusted the persisted path, so one symlinked
    # PARENT walked it into an entirely different repository.
    #
    # Now: resolve through the CANONICAL worktree root with anchored, no-follow traversal (every
    # component verified, parents included), then compare the STRICT read-only content identity —
    # the same digest every other worktree uses.
    resumable = _job_is_resumable(job)
    if ws_path:
        contained, ws_state = contained_workspace_path(Path(ws_path),
                                                       getattr(job, "repo_path", "") or "")
        if contained is None:
            reason = ("is absent" if ws_state == WS_ABSENT
                      else "is symlinked or resolves outside the canonical worktree root")
            if ws_state == WS_ESCAPES or resumable:
                # Neutralise the historical value so it can never read as "same": either
                # something untrustworthy is there, or a resumable job's workspace has gone.
                snap = dataclasses.replace(snap,
                                           episode_start_workspace_identity=WorktreeIdentity(
                                               GIT_UNAVAILABLE, UNAVAILABLE, "",
                                               (f"workspace {reason}",)).to_json())
            # A COMPLETED job whose worktree was intentionally cleaned keeps the documented
            # rerun-from-recorded-target semantics: its absent workspace is not drift.
            if ws_state == WS_ESCAPES:
                # Something IS there and it is not where it claims to be. Never inspect it.
                workspace_problems.append(
                    "the job workspace named by the JobPlan is symlinked or resolves outside "
                    "the canonical worktree root; refusing to inspect it")
            elif resumable:
                # F12: a RESUMABLE job's named workspace must be PROVEN now — a missing one is
                # incomplete coverage, never a quiet downgrade to the completed-job
                # rerun-from-recorded-target semantics.
                workspace_problems.append(
                    "the resumable job workspace named by the JobPlan is missing")
            else:
                # A COMPLETED job whose worktree was intentionally cleaned: the documented
                # rerun-from-recorded-target semantics apply. Absence is not a problem, and it is
                # not drift either — so the candidate carries the RECORDED identity forward
                # rather than reporting the cleanup as an input change.
                snap = dataclasses.replace(
                    snap,
                    episode_start_workspace_identity=dict(
                        getattr(reference.snapshot, "episode_start_workspace_identity", {})
                        or {}))
        else:
            # F8 (round 12): EXACTLY ONE workspace read per candidate. `build_input_snapshot`
            # already inspected the CURRENT workspace through the held-handle API above, so
            # re-inspecting here would read it twice — and two reads of a live directory are two
            # different moments, which is precisely the ambiguity this record exists to remove.
            wid = WorktreeIdentity.from_json(snap.episode_start_workspace_identity or {})
            if wid.status != GIT_OK:
                workspace_problems.append(
                    f"the current job-workspace identity is {wid.status}: "
                    f"{'; '.join(wid.problems)[:120]}")
    # A job that names NO workspace (a pre-work stop that never acquired one, or a
    # planning-only job) has nothing to prove: there is no input there to compare.

    # A reference with no calls (a genuine zero-call / planning-only job) has nothing per-call
    # to reconstruct, so coverage is trivially COMPLETE and the check can reach exit 0. A
    # reference WITH calls cannot be per-call reconstructed in check-only mode (worktree
    # replay is F140), so coverage is INCOMPLETE and the check reports exit 5.
    if reference.calls:
        coverage = CallCoverage(
            status=COVERAGE_INCOMPLETE,
            problems=("per-call prompt reconstruction requires worktree replay (F140); "
                      "not performed in check-only mode",) + tuple(workspace_problems))
    elif workspace_problems:
        coverage = CallCoverage(status=COVERAGE_INCOMPLETE, problems=tuple(workspace_problems))
    else:
        coverage = CallCoverage(status=COVERAGE_COMPLETE)
    candidate_snapshot = EpisodeInputSnapshotV1(
        snapshot_v=EPISODE_SNAPSHOT_VERSION, episode_id=reference.episode_id,
        captured_at=utc_now_iso(), capture_phase=PHASE_EPISODE_START,
        status=SNAPSHOT_OK, problems=(), input=snap)
    return RunManifestV1(
        job_id=str(getattr(job, "job_id", "")),
        episode_id=reference.episode_id,
        created_at=utc_now_iso(),
        status=reference.status,
        episode_snapshot=candidate_snapshot,
        # F6: bound to this candidate's OWN embedded definition.
        job_input_sha256=job_input_definition_sha256(snap.job_input),
        calls=(),
        coverage=coverage,
        # F6: the candidate re-derives today's INPUTS; it does not re-decide what the recorded
        # episode expected. It carries the reference's proof so the two are compared like for
        # like (the expectation is provenance, and never part of the logical input identity).
        call_expectation=reference.call_expectation,
        call_ledgers=reference.call_ledgers,
        prior_episode_ids=reference.prior_episode_ids,
        episode_ordinal=reference.episode_ordinal,
        previous_episode_id=reference.previous_episode_id,
        stop_request_id=reference.stop_request_id,
    )


# ---------------------------------------------------------------------------
# Structured diff (F5 unique keys, F6/F10 coverage)
# ---------------------------------------------------------------------------

DIFF_VERSION = 1


def _entry(field: str, category: str, ref: Any, cand: Any) -> dict[str, Any]:
    return {"field": field, "category": category, "reference": ref, "candidate": cand}


#: F9 (round 12): the material identities a run's INPUT coverage depends on. If any of them is
#: unavailable on either side, we do not know the inputs — whatever the calls say.
_INPUT_COVERAGE_IDENTITIES = ("remedy_git_sha", "target_base_commit", "target_head",
                             "target_tree", "job_initial_tree", "job_file_sha256")


def _input_coverage(rs: Any, cs: Any, worktrees: tuple) -> dict[str, Any]:
    """F9 (round 12): is the MATERIAL INPUT record complete on both sides?

    Separate from call coverage on purpose: a check can compare every call it has and still not
    know what the run was given. Honest `unavailable` values are why this dimension exists — they
    keep the record truthful, and this keeps them from quietly adding up to determinism.
    """
    problems: list[str] = []
    for side, snap in (("reference", rs), ("candidate", cs)):
        if snap is None:
            problems.append(f"the {side} carries no input snapshot")
            continue
        for f in _INPUT_COVERAGE_IDENTITIES:
            val = str(getattr(snap, f, "") or "")
            if not val or val == UNAVAILABLE:
                problems.append(f"{side} {f} is {UNAVAILABLE}")
        wid = getattr(snap, "episode_start_workspace_identity", None) or {}
        status = str(wid.get("status", ""))
        if status and status != GIT_OK:
            problems.append(
                f"{side} episode_start_workspace_identity is {status}"
                + (f" ({'; '.join(wid.get('problems') or [])[:80]})" if wid.get("problems")
                   else ""))
    for wt in worktrees:
        if (wt or {}).get("status", GIT_OK) != GIT_OK:
            problems.append(f"a worktree identity is {(wt or {}).get('status')}")
    return {"input_status": COVERAGE_COMPLETE if not problems else COVERAGE_INCOMPLETE,
            "problems": sorted(set(problems))[:20]}


def _workspace_identity_projection(wid: dict[str, Any] | None) -> dict[str, Any]:
    """F8 (round 12): the workspace identity's MATERIAL part — what it is, not how it was found.

    `status`/`digest`/`dirty` decide whether two workspaces are the same input. `head` follows
    the digest, and `problems` describes a collection failure, not the workspace — including it
    would make an unrelated diagnostic look like drift.
    """
    wid = wid or {}
    return {"status": str(wid.get("status", "")), "digest": str(wid.get("digest", "")),
            "dirty": wid.get("dirty"), "head": str(wid.get("head", ""))}


def diff_manifests(reference: RunManifestV1, candidate: RunManifestV1) -> dict[str, Any]:
    """Pure structured diff. Never mutates. Deterministically ordered. Unique call keys.

    ``verification_complete`` is True only when the per-call inputs were actually compared.
    ``same_inputs`` is True only when there is no blocking drift AND verification is complete;
    it is ``None`` when coverage is incomplete. ``same_inputs is True`` implies
    ``logical_input_match is True``."""
    blocking: list[dict[str, Any]] = []
    informational: list[dict[str, Any]] = []
    warnings: list[str] = []

    if reference.manifest_v != candidate.manifest_v:
        warnings.append(f"manifest version differs: {reference.manifest_v} vs "
                        f"{candidate.manifest_v}")

    rs, cs = reference.snapshot, candidate.snapshot
    for f, cat in (("remedy_git_sha", "remedy_code"),
                   ("target_base_commit", "base_commit"), ("target_head", "base_commit"),
                   ("target_tree", "base_commit"),
                   ("job_initial_tree", "base_commit"),
                   ("job_file_sha256", "prompt")):
        rv, cv = getattr(rs, f), getattr(cs, f)
        if rv != cv:
            blocking.append(_entry(f, cat, rv, cv))
    # F8 (round 12): the workspace is compared on its typed IDENTITY. `episode_start_workspace_tree`
    # is provenance — the reference records a git tree object there and a candidate cannot
    # recompute one read-only, so comparing that field made an identical workspace look drifted.
    rwsi = _workspace_identity_projection(rs.episode_start_workspace_identity)
    cwsi = _workspace_identity_projection(cs.episode_start_workspace_identity)
    if rwsi != cwsi:
        blocking.append(_entry("episode_start_workspace_identity", "base_commit",
                               rwsi.get("digest") or rwsi.get("status"),
                               cwsi.get("digest") or cwsi.get("status")))
    # F2: Remedy's own source CONTENT (staged/unstaged/untracked), not just the sha + a bool.
    rw, cw = (rs.remedy_worktree or {}), (cs.remedy_worktree or {})
    if rw.get("digest") != cw.get("digest"):
        blocking.append(_entry("remedy_worktree_digest", "remedy_code",
                               rw.get("digest"), cw.get("digest")))
    # F3: an incomplete/unavailable worktree identity on EITHER side is a coverage problem,
    # never silent equality.
    for label, wt in (("reference", rw), ("candidate", cw)):
        if wt.get("status") and wt.get("status") != GIT_OK:
            warnings.append(f"{label} Remedy worktree identity is {wt.get('status')}: "
                            f"{'; '.join(wt.get('problems') or [])[:200]}")
    rtw, ctw = (rs.target_worktree or {}), (cs.target_worktree or {})
    for label, wt in (("reference", rtw), ("candidate", ctw)):
        if wt.get("status") and wt.get("status") == GIT_INCOMPLETE:
            warnings.append(f"{label} target worktree identity is incomplete: "
                            f"{'; '.join(wt.get('problems') or [])[:200]}")
    if reference.job_input_sha256 != candidate.job_input_sha256:
        blocking.append(_entry("job_input_sha256", "prompt",
                               reference.job_input_sha256, candidate.job_input_sha256))
    if reference.created_at != candidate.created_at:
        informational.append(_entry("created_at", "timestamp",
                                    reference.created_at, candidate.created_at))
    for f, cat in (("python_version", "platform"), ("platform", "platform")):
        if getattr(rs, f) != getattr(cs, f):
            informational.append(_entry(f, cat, getattr(rs, f), getattr(cs, f)))

    for role in sorted(set(rs.models) | set(cs.models)):
        if rs.models.get(role) != cs.models.get(role):
            blocking.append(_entry(f"models.{role}", "model",
                                   rs.models.get(role), cs.models.get(role)))
    for prov in sorted(set(rs.provider_versions) | set(cs.provider_versions)):
        if rs.provider_versions.get(prov) != cs.provider_versions.get(prov):
            informational.append(_entry(f"provider_versions.{prov}", "tool_version",
                                        rs.provider_versions.get(prov),
                                        cs.provider_versions.get(prov)))

    rcfg = {e["key"]: e for e in rs.config}
    ccfg = {e["key"]: e for e in cs.config}
    for key in sorted(set(rcfg) | set(ccfg)):
        r, c = rcfg.get(key), ccfg.get(key)
        if r is None or c is None:
            blocking.append(_entry(f"config.{key}", "config_value",
                                   r and r.get("value"), c and c.get("value")))
            continue
        if r.get("value") != c.get("value"):
            blocking.append(_entry(f"config.{key}", "config_value",
                                   r.get("value"), c.get("value")))
        if r.get("source") != c.get("source"):
            blocking.append(_entry(f"config.{key}.source", "config_source",
                                   r.get("source"), c.get("source")))

    renv = {e["key"]: e.get("value") for e in rs.environment}
    cenv = {e["key"]: e.get("value") for e in cs.environment}
    for key in sorted(set(renv) | set(cenv)):
        if renv.get(key) != cenv.get(key):
            blocking.append(_entry(f"environment.{key}", "environment",
                                   renv.get(key), cenv.get(key)))

    coverage = _diff_calls(reference, candidate, blocking)
    # F9 (round 12): TWO dimensions, reported separately. "We compared every call" and "we know
    # every material input" are different claims, and a manifest can honestly have one without
    # the other — an `unavailable` identity is better than an empty string, but it is still not a
    # complete deterministic input record, and it must never add up to "same inputs".
    input_coverage = _input_coverage(rs, cs, (rw, cw, rtw, ctw))
    call_status = COVERAGE_COMPLETE if coverage.get("calls_compared") else COVERAGE_INCOMPLETE
    coverage["input_status"] = input_coverage["input_status"]
    coverage["call_status"] = call_status
    coverage["input_problems"] = input_coverage["problems"]
    if input_coverage["input_status"] != COVERAGE_COMPLETE:
        coverage["worktree_identity_incomplete"] = True
    verification_complete = (call_status == COVERAGE_COMPLETE
                            and input_coverage["input_status"] == COVERAGE_COMPLETE)

    if blocking:
        same_inputs: Any = False
    elif verification_complete:
        same_inputs = True
    else:
        same_inputs = None

    logical_match = (reference.logical_input_sha256() == candidate.logical_input_sha256())
    if same_inputs is True and not logical_match:
        blocking.append(_entry("__invariant__", "internal",
                               "same_inputs=true", "logical_input_match=false"))
        same_inputs = False

    return {
        "version": DIFF_VERSION,
        "same_inputs": same_inputs,
        "verification_complete": verification_complete,
        "logical_input_match": logical_match,
        "blocking": sorted(blocking, key=lambda e: e["field"]),
        "informational": sorted(informational, key=lambda e: e["field"]),
        "coverage": coverage,
        "warnings": sorted(warnings),
    }


def _diff_calls(reference: RunManifestV1, candidate: RunManifestV1,
                blocking: list[dict[str, Any]]) -> dict[str, Any]:
    # A genuine zero-call job on both sides with complete coverage IS fully verified (there
    # are simply no per-call inputs to compare).
    if (not reference.calls and not candidate.calls
            and reference.coverage.status == COVERAGE_COMPLETE
            and candidate.coverage.status == COVERAGE_COMPLETE):
        return {"calls_compared": True, "reference_call_count": 0, "candidate_call_count": 0}
    if candidate.coverage.status != COVERAGE_COMPLETE or not candidate.calls:
        return {
            "calls_compared": False,
            "reference_call_count": len(reference.calls),
            "candidate_call_count": len(candidate.calls),
            "reason": "candidate did not reconstruct per-call prompt inputs "
                      "(check-only mode does not re-execute; worktree replay is F140)",
            "reference_coverage": reference.coverage.to_json(),
            "candidate_coverage": candidate.coverage.to_json(),
        }
    # F1: compare calls through the STABLE LOGICAL key (task, sequence, role, round, kind).
    # The random execution identifiers (job/episode/run/call id) are provenance — two identical
    # runs differ there legitimately, and that must never read as input drift.
    rmap = {c.identity.logical_key(): c.fingerprint for c in reference.calls}
    cmap = {c.identity.logical_key(): c.fingerprint for c in candidate.calls}
    for key in sorted(set(rmap) | set(cmap)):
        field = "call." + ".".join(str(x) for x in key)
        if key not in cmap:
            blocking.append(_entry(field, "missing_call", rmap[key], None))
        elif key not in rmap:
            blocking.append(_entry(field, "extra_call", None, cmap[key]))
        elif rmap[key] != cmap[key]:
            blocking.append(_entry(field, "prompt", rmap[key], cmap[key]))
    r_order = [c.identity.logical_key() for c in
               sorted(reference.calls, key=lambda c: c.identity.logical_key())]
    c_order = [c.identity.logical_key() for c in
               sorted(candidate.calls, key=lambda c: c.identity.logical_key())]
    if r_order != c_order and len(r_order) == len(c_order):
        blocking.append(_entry("call_order", "call_order",
                               [list(x) for x in r_order], [list(x) for x in c_order]))
    return {"calls_compared": True,
            "reference_call_count": len(reference.calls),
            "candidate_call_count": len(candidate.calls)}
