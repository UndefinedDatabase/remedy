"""Local runtime harness (F007): start, probe and stop a project's dev server.

Local-first and honest by construction:

* the command is an argv list — never a shell string, never ``shell=True``;
* the server runs in its own session, so the whole process TREE can be stopped;
* a requested port that is busy is not fought over: a free port is chosen and the
  EFFECTIVE port is what gets reported and injected;
* readiness means the managed process is still alive AND its health URL answered;
* logs are captured to a file and always read back bounded;
* durable state carries a PID *plus* the process creation time and a command
  fingerprint, so a later ``runtime stop`` can never kill an unrelated process
  that happens to have inherited the PID;
* a readiness failure stops the tree and leaves no state claiming to be active.

This module deliberately contains no SSE, no HTTP server and no UI code (F008), and
no project-id registry (F146): the project digest is the same resolved-path digest
F006 already uses.
"""
from __future__ import annotations

import contextlib
import errno
import fcntl
import hashlib
import json
import os
import re
import shlex
import signal
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: How much of a log file is ever read back into memory or evidence.
LOG_TAIL_BYTES = 64 * 1024

#: Hard cap on the log FILE. The pump enforces it by trimming to the newest
#: ``LOG_KEEP_BYTES`` whenever the file grows past the cap, so runtime.log never
#: exceeds MAX_LOG_BYTES + one pump chunk (the documented rotation margin).
MAX_LOG_BYTES = 8 * 1024 * 1024
LOG_KEEP_BYTES = MAX_LOG_BYTES // 2
LOG_CHUNK_BYTES = 64 * 1024

#: HTTP statuses accepted as "the dev server answered".
READY_STATUS_MIN = 200
READY_STATUS_MAX = 399

#: Placeholder replaced with the effective port in argv and env values.
PORT_PLACEHOLDER = "{port}"

DEFAULT_HOST = "127.0.0.1"
GRACE_SECONDS = 3.0

#: Versioned schema for the effective-spec fingerprint.
SPEC_FINGERPRINT_SCHEMA = "rspec1"

#: Lifecycle statuses persisted in runtime.json.
STATUS_STARTING = "starting"
STATUS_RUNNING = "running"
STATUS_PROBING = "probing"
STATUS_STOPPED = "stopped"
STATUS_STOP_FAILED = "stop_failed"
STATUS_START_CLEANUP_FAILED = "start_cleanup_failed"
STATUS_IDENTITY_UNPROVEN = "identity_unproven"
STATUS_IDENTITY_MISMATCH = "identity_mismatch"
STATUS_STOPPING = "stopping"
STATUS_INTERRUPTED_START = "interrupted_start"
STATUS_EXITED = "exited"
STATUS_SUPERVISOR_MISSING = "supervisor_missing"
#: The bounded log pump died while the application was still running. A runtime whose
#: logs are no longer being drained is not a healthy runtime, however happily its port
#: still answers: the pipe backs up, the application eventually blocks on its own stdout,
#: and nothing is being captured in the meantime.
STATUS_LOG_FAILED = "log_failed"
#: ...and the application family could not be cleaned up after that failure.
STATUS_LOG_CLEANUP_FAILED = "log_cleanup_failed"

#: Durable diagnostics: the runtime is not usable, and the record explains why. They are
#: never silently overwritten by a new serve or probe; `runtime stop` clears them once it
#: has confirmed that supervisor, application and descendants are really gone.
LOG_FAILURE_STATUSES = frozenset({STATUS_LOG_FAILED, STATUS_LOG_CLEANUP_FAILED})

#: A record in one of these statuses owns (or may own) a live process.
LIVE_STATUSES = frozenset({
    STATUS_STARTING, STATUS_RUNNING, STATUS_PROBING, STATUS_STOPPING,
    STATUS_STOP_FAILED, STATUS_START_CLEANUP_FAILED, STATUS_INTERRUPTED_START,
    STATUS_IDENTITY_UNPROVEN, STATUS_IDENTITY_MISMATCH,
    STATUS_SUPERVISOR_MISSING, STATUS_LOG_FAILED, STATUS_LOG_CLEANUP_FAILED,
})

#: Identity classifications returned by classify_state().
VERIFIED = "verified"
DEFINITELY_GONE = "definitely_gone"
PID_REUSED = "pid_reused"
IDENTITY_MISMATCH = "identity_mismatch"
IDENTITY_UNPROVEN = "identity_unproven"


class RuntimeError_(RuntimeError):
    """Base class for runtime-harness failures."""


class RuntimeConfigError(RuntimeError_):
    """The runtime spec is missing, ambiguous or unsafe."""


class RuntimeStartError(RuntimeError_):
    """The dev server could not be started."""


class RuntimeReadyError(RuntimeError_):
    """The dev server never became ready."""


class RuntimeStopError(RuntimeError_):
    """A managed process survived the stop."""


class RuntimeLockError(RuntimeError_):
    """The project's runtime lifecycle lock could not be taken."""


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RuntimeSpec:
    """How to run one project's dev server.

    ``cmd`` is argv. ``{port}`` inside an argv item or an ``env`` value is replaced
    with the effective port, which is the only sanctioned way to bind the port.
    """

    cmd: list[str]
    cwd: str
    port: int = 5173
    health_path: str = "/"
    ready_timeout_s: float = 30.0
    host: str = DEFAULT_HOST
    env: dict[str, str] = field(default_factory=dict)
    source: str = "config"          # "config" | "detected:<kind>"

    def fingerprint(self) -> str:
        """Identity of the COMPLETE effective spec, not just its command.

        Every field that changes what the runtime IS takes part: argv, resolved cwd,
        configured port, host, health path, readiness timeout and the sorted
        environment additions. Otherwise `runtime serve` would report "already
        running" for a runtime now configured to listen elsewhere, probe a different
        path, or run with a different environment. The schema is versioned so later
        additions are deliberate.
        """
        payload = json.dumps(
            {
                "schema": SPEC_FINGERPRINT_SCHEMA,
                "cmd": [str(a) for a in self.cmd],
                "cwd": str(Path(self.cwd).resolve()),
                "port": int(self.port),
                "host": str(self.host),
                "health_path": str(self.health_path),
                "ready_timeout_s": float(self.ready_timeout_s),
                "env": sorted((str(k), str(v)) for k, v in self.env.items()),
            },
            sort_keys=True,
        )
        return f"{SPEC_FINGERPRINT_SCHEMA}:" + hashlib.sha256(
            payload.encode()).hexdigest()[:24]

    def resolved_cmd(self, port: int) -> list[str]:
        return [str(a).replace(PORT_PLACEHOLDER, str(port)) for a in self.cmd]

    def resolved_env(self, port: int) -> dict[str, str]:
        out = dict(os.environ)
        for key, value in self.env.items():
            out[str(key)] = str(value).replace(PORT_PLACEHOLDER, str(port))
        out["PORT"] = str(port)
        return out

    def to_json(self) -> dict[str, Any]:
        return {
            "cmd": list(self.cmd),
            "cwd": self.cwd,
            "port": self.port,
            "health_path": self.health_path,
            "ready_timeout_s": self.ready_timeout_s,
            "host": self.host,
            "source": self.source,
        }


def validate_spec(spec: RuntimeSpec, project_root: str | Path) -> RuntimeSpec:
    """Reject a spec that could run the wrong thing, or run it in the wrong place."""
    root = Path(project_root).resolve()

    if not spec.cmd or not all(str(a).strip() for a in spec.cmd):
        raise RuntimeConfigError("runtime.cmd must be a non-empty argv list")
    if isinstance(spec.cmd, str):                     # defensive: never a shell string
        raise RuntimeConfigError("runtime.cmd must be a list, not a shell string")

    try:
        cwd = Path(spec.cwd).resolve()
    except OSError as exc:
        raise RuntimeConfigError(f"runtime.cwd cannot be resolved: {exc}") from exc
    if not (cwd == root or root in cwd.parents):
        raise RuntimeConfigError(
            f"runtime.cwd {spec.cwd!r} resolves outside the project ({root})")
    if not cwd.is_dir():
        raise RuntimeConfigError(f"runtime.cwd {spec.cwd!r} is not a directory")

    if not (1 <= int(spec.port) <= 65535):
        raise RuntimeConfigError(f"runtime.port {spec.port!r} is out of range")
    if not str(spec.health_path).startswith("/"):
        raise RuntimeConfigError(
            f"runtime.health_path {spec.health_path!r} must start with '/'")
    if float(spec.ready_timeout_s) <= 0:
        raise RuntimeConfigError("runtime.ready_timeout_s must be positive")

    return RuntimeSpec(
        cmd=[str(a) for a in spec.cmd], cwd=str(cwd), port=int(spec.port),
        health_path=str(spec.health_path), ready_timeout_s=float(spec.ready_timeout_s),
        host=str(spec.host or DEFAULT_HOST), env=dict(spec.env), source=spec.source,
    )




# ---------------------------------------------------------------------------
# Paths, digest and the lifecycle lock
# ---------------------------------------------------------------------------

def project_digest(project_root: str | Path) -> str:
    """Resolved-path digest — the SAME helper F006 uses. This is NOT F146."""
    from packages.orchestration.worktrees import project_id
    return project_id(project_root)


def runtime_dir(project_root: str | Path) -> Path:
    from packages.orchestration.data_paths import projects_dir
    return projects_dir() / project_digest(project_root)


def state_path(project_root: str | Path) -> Path:
    return runtime_dir(project_root) / "runtime.json"


def log_path(project_root: str | Path) -> Path:
    return runtime_dir(project_root) / "runtime.log"


def lock_path(project_root: str | Path) -> Path:
    return runtime_dir(project_root) / "runtime.lock"


def handshake_path(project_root: str | Path) -> Path:
    """Private filesystem IPC for the supervisor startup handshake (no network)."""
    return runtime_dir(project_root) / "runtime.handshake.json"


def stop_request_path(project_root: str | Path) -> Path:
    """A stop request the persistent supervisor polls. Local to F007 — NOT F011."""
    return runtime_dir(project_root) / "runtime.stop"


def spec_file_path(project_root: str | Path) -> Path:
    """The effective spec handed to the supervisor. It carries the runtime ENV, so it
    may contain secrets: it is private, and the supervisor deletes it once ingested."""
    return runtime_dir(project_root) / "runtime.spec.json"


# --- privacy ---------------------------------------------------------------
#
# Every runtime artifact is local control data about this user's processes, and
# runtime.spec.json carries the configured environment — which may hold secrets. None
# of it is other users' business, so the directory is 0700 and every file 0600. The
# helpers below also REPAIR files created by an older, laxer build.

RUNTIME_DIR_MODE = 0o700
RUNTIME_FILE_MODE = 0o600

#: The files this harness manages inside the runtime directory.
RUNTIME_ARTIFACTS = (
    "runtime.json", "runtime.spec.json", "runtime.log", "runtime.lock",
    "runtime.handshake.json", "runtime.stop", "runtime.stop.invalid",
    "runtime.log_failure.json",
)


def harden_path(path: str | Path) -> None:
    """Make one existing runtime artifact owner-only. Never raises."""
    with contextlib.suppress(OSError):
        p = Path(path)
        if p.is_file() and (p.stat().st_mode & 0o777) != RUNTIME_FILE_MODE:
            os.chmod(p, RUNTIME_FILE_MODE)


def ensure_runtime_dir(project_root: str | Path) -> Path:
    """The private runtime directory, created and repaired: 0700 dir, 0600 files."""
    rdir = runtime_dir(project_root)
    rdir.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        if (rdir.stat().st_mode & 0o777) != RUNTIME_DIR_MODE:
            os.chmod(rdir, RUNTIME_DIR_MODE)
    for name in RUNTIME_ARTIFACTS:
        harden_path(rdir / name)
    return rdir


def atomic_write_bytes(path: str | Path, data: bytes) -> None:
    """Write a PRIVATE file atomically: 0600 temp file, fsync, os.replace.

    The temp file is created with the final mode, so the replaced file is never even
    briefly world-readable, and a failed write never leaves its temp file behind.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    try:
        fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                     RUNTIME_FILE_MODE)
        try:
            os.write(fd, data)
            with contextlib.suppress(OSError):
                os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, target)
    except Exception:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


def atomic_write_text(path: str | Path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def open_private_file(path: str | Path):
    """Open a runtime file for writing with owner-only permissions."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(p), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, RUNTIME_FILE_MODE)
    harden_path(p)                       # repair a pre-existing 0644 file
    return os.fdopen(fd, "wb", buffering=0)


#: How long a lifecycle transition waits for the project lock before giving up.
LOCK_TIMEOUT_S = 10.0

#: How long `runtime stop` gives a verified supervisor to shut its own runtime down
#: before it considers a hard signal. Named (not inlined) so a test can shorten it
#: without waiting out the real thing.
STOP_REQUEST_TIMEOUT_S = 15.0


@contextmanager
def lifecycle_lock(project_root: str | Path,
                   timeout_s: float = LOCK_TIMEOUT_S) -> Iterator[None]:
    """Serialize read -> verify -> start/stop -> commit for ONE project.

    Held only across a lifecycle TRANSITION — never for the lifetime of the
    server. Without it, two concurrent ``runtime serve`` calls each see "nothing
    running", start their own server, and the second one's state write orphans the
    first process. Per project: two different projects never block each other.
    """
    ensure_runtime_dir(project_root)
    path = lock_path(project_root)
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, RUNTIME_FILE_MODE)
    harden_path(path)                    # repair a lock file from an older build
    deadline = time.monotonic() + max(0.0, timeout_s)
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError as exc:
                if exc.errno not in (errno.EAGAIN, errno.EACCES):
                    raise RuntimeLockError(
                        f"runtime lock unusable: {exc}") from exc
                if time.monotonic() >= deadline:
                    raise RuntimeLockError(
                        f"another runtime lifecycle operation holds the project "
                        f"lock ({path.name}); timed out after {timeout_s}s"
                    ) from exc
                time.sleep(0.05)
        try:
            yield
        finally:
            with contextlib.suppress(OSError):
                fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        with contextlib.suppress(OSError):
            os.close(fd)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def new_instance_id() -> str:
    """A random id for one served runtime. Not a capability — an identity BINDING.

    It is generated before the supervisor exists, put into the supervisor's argv (so it
    is verifiable from the LIVE process table, not just from a file), and written into
    runtime.json, the handshake and the stop request. It never replaces the pid,
    creation time, command line, project digest or process-group checks; it is one more
    thing that must agree.
    """
    import secrets
    return secrets.token_hex(16)


def resolved_fingerprint(argv: list[str], cwd: str | Path, project_id: str) -> str:
    """Identity of a RESOLVED launch: the real argv, the real cwd, this project.

    The effective port lives inside the resolved argv, so a runtime started on a
    different port has a different fingerprint.
    """
    payload = json.dumps(
        {"argv": [str(a) for a in argv],
         "cwd": str(Path(cwd).resolve()),
         "project_id": str(project_id)},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:32]


#: Every normal absolute-path form, ANYWHERE inside a string — after `--flag=`, after
#: `key=`, inside a quote, in the middle of a diagnostic sentence:
#:
#:     /home/user/file            POSIX
#:     C:\Users\Alice\file        Windows, backslashes
#:     C:/Users/Alice/file        Windows, forward slashes
#:     \\server\share\file        UNC
#:     //server/share/file        UNC, forward slashes
#:
#: The look-behind keeps ordinary URLs intact: in ``http://127.0.0.1:5173/health`` the
#: `//` follows a colon and the path slash follows a word character, so neither starts a
#: match. A bare ``C:`` that is not followed by a separator is ordinary text, not a path,
#: and is left alone.
_PATH_TAIL = r"""[^\s'"`,;)\]}]"""
_ABS_PATH_RE = re.compile(
    rf"""(?<![\w:/\\])(?:
            \\\\{_PATH_TAIL}+                 # \\server\share\...
          | //{_PATH_TAIL}+                   # //server/share/...
          | [A-Za-z]:[\\/]{_PATH_TAIL}*       # C:\... or C:/...
          | /{_PATH_TAIL}*                    # /posix/path
        )""",
    re.VERBOSE,
)

#: What makes a command element an absolute path worth redacting by value.
_ABS_PREFIX_RE = re.compile(r"\A(?:/|\\\\|//|[A-Za-z]:[\\/])")


def _basename(token: str) -> str:
    """The bare file name of a POSIX, Windows or UNC path, on whatever host runs this."""
    from pathlib import PureWindowsPath
    text = str(token)
    if "\\" in text or re.match(r"\A[A-Za-z]:", text) or text.startswith("//"):
        return PureWindowsPath(text).name or "[path]"
    return Path(text).name or "[path]"


#: A QUOTED absolute path — the only form in which a path may legitimately contain
#: spaces, e.g. ``working directory "C:/Users/Alice/private dir" cannot be inspected``.
#: Unquoted, a space ends the path, and only its prefix (the private part) is removed.
_QUOTED_PATH_RE = re.compile(
    r"""(['"])((?:\\\\|//|[A-Za-z]:[\\/]|/)[^'"]*)\1""")

#: A `file:` URI. It LOOKS like a URL, which is exactly why the generic path scrub —
#: which deliberately leaves URLs alone — used to walk straight past
#: ``file:///home/alice/private/secret.txt``. A file URI is not a network address: it is
#: a local path wearing a scheme, and it is redacted like one.
#: The look-behind is the scheme BOUNDARY: a URI scheme may only be preceded by a
#: non-scheme character. Without it, `profile:///home/alice/x.txt` matched from its
#: `file:` onwards and came back as `protest.txt` — a string that is not a file URI at all
#: being quietly rewritten. `profile:`, `myfile:`, `notafile:` and `some.file:` are left
#: exactly as they are; `file:`, `FILE:`, `prefix=file:` and `(file:…)` are redacted.
_FILE_URI_RE = re.compile(
    r"""(?<![A-Za-z0-9+.\-])file:(?://)?[^\s'"`,;)\]}]*""", re.IGNORECASE)


def _file_uri_basename(uri: str) -> str:
    """The bare file name behind a `file:` URI, in every normal form.

    ``file:///home/alice/secret.txt``            → secret.txt
    ``file://localhost/home/alice/secret.txt``   → secret.txt
    ``file:///C:/Users/Alice/secret.txt``        → secret.txt
    ``file://server/share/secret.txt``           → secret.txt   (host is private too)
    ``file:///home/alice/private%20dir/x.txt``   → x.txt        (percent-decoded)

    Never a path operation on an arbitrary string: the URI is split first, and anything
    that does not yield a name becomes ``[path]``.
    """
    from urllib.parse import unquote, urlsplit

    try:
        parts = urlsplit(uri)
        path = unquote(parts.path or "")
    except ValueError:
        return "[path]"
    if not path:
        return "[path]"
    path = path.lstrip("/")              # /C:/Users/... and /home/... alike
    return _basename(path) or "[path]"


def _scrub_paths(value: str) -> str:
    """Reduce every absolute path — and every local file URI — to its bare file name."""
    text = _FILE_URI_RE.sub(lambda m: _file_uri_basename(m.group(0)), value)
    text = _QUOTED_PATH_RE.sub(
        lambda m: f"{m.group(1)}{_basename(m.group(2))}{m.group(1)}", text)
    return _ABS_PATH_RE.sub(lambda m: _basename(m.group(0)), text)


def _redact(value: Any, rules: list[tuple[str, str]] | None = None) -> Any:
    """Recursively strip private values and absolute paths out of a structure.

    Two passes, because either alone leaks. First the EXACT sensitive values of this
    runtime (project root, working directories, control paths, absolute command
    elements, the instance id) are replaced wherever they occur — in the middle of a
    ``--flag=…``, inside quotes, inside a diagnostic sentence, at any nesting depth.
    Then whatever still looks like an absolute path is reduced to its file name, so a
    path nobody thought of cannot ride along in a new field.
    """
    if isinstance(value, str):
        text = value
        for private, placeholder in (rules or ()):
            if private in text:
                text = text.replace(private, placeholder)
        return _scrub_paths(text)
    if isinstance(value, list):
        return [_redact(item, rules) for item in value]
    if isinstance(value, tuple):
        return tuple(_redact(item, rules) for item in value)
    if isinstance(value, dict):
        return {key: _redact(item, rules) for key, item in value.items()}
    return value


@dataclass
class RuntimeState:
    """Durable local record of a managed dev server.

    Identity is the WHOLE record — pid, creation time, resolved argv, cwd, project
    digest and the fingerprint recomputed from them. A PID alone is never identity:
    the OS recycles PIDs, and a stop must never fall on an innocent process.
    """

    pid: int = 0
    create_time: float = 0.0
    session_id: int = 0             # kept for readers of the previous shape
    pgid: int = 0                   # live os.getpgid(pid) observed at start
    sid: int = 0                    # live os.getsid(pid) observed at start
    port: int = 0
    url: str = ""
    project_root: str = ""          # local, resolved; needed for process safety
    project_id: str = ""
    cwd: str = ""                   # resolved working directory of the process
    cmd_fingerprint: str = ""       # identity of the RESOLVED launch (incl. port)
    spec_fingerprint: str = ""      # identity of the CONFIGURED spec (port-agnostic)
    cmd: list[str] = field(default_factory=list)     # the RESOLVED argv
    started_at: float = 0.0
    log_path: str = ""
    status: str = "stopped"         # "running" | "stopped" | "stop_failed"
    survivors: list[int] = field(default_factory=list)
    stop_error: str = ""
    log_error: str = ""
    identity_reason: str = ""
    # --- persistent supervisor (F007 final round) -------------------------
    # The legacy pid/create_time/cmd/cwd/pgid/sid fields describe the APPLICATION.
    # These describe the SUPERVISOR that owns it after the initiating CLI exits.
    supervisor_pid: int = 0
    supervisor_create_time: float = 0.0
    supervisor_cmd: list[str] = field(default_factory=list)
    supervisor_cwd: str = ""
    supervisor_fingerprint: str = ""
    supervisor_pgid: int = 0
    supervisor_sid: int = 0
    app_exit_code: int | None = None
    #: Random per-runtime id, generated before the supervisor starts and carried in
    #: the supervisor's argv, the handshake and the stop request. It binds those
    #: private files to THIS runtime; it is never authorization on its own.
    instance_id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "pid": self.pid,
            "create_time": self.create_time,
            "session_id": self.session_id,
            "pgid": self.pgid,
            "sid": self.sid,
            "port": self.port,
            "url": self.url,
            "project_root": self.project_root,
            "project_id": self.project_id,
            "cwd": self.cwd,
            "cmd_fingerprint": self.cmd_fingerprint,
            "spec_fingerprint": self.spec_fingerprint,
            "cmd": list(self.cmd),
            "started_at": self.started_at,
            "log_path": self.log_path,
            "status": self.status,
            "survivors": list(self.survivors),
            "stop_error": self.stop_error,
            "log_error": self.log_error,
            "identity_reason": self.identity_reason,
            "supervisor_pid": self.supervisor_pid,
            "supervisor_create_time": self.supervisor_create_time,
            "supervisor_cmd": list(self.supervisor_cmd),
            "supervisor_cwd": self.supervisor_cwd,
            "supervisor_fingerprint": self.supervisor_fingerprint,
            "supervisor_pgid": self.supervisor_pgid,
            "supervisor_sid": self.supervisor_sid,
            "app_exit_code": self.app_exit_code,
            "instance_id": self.instance_id,
        }

    def redaction_rules(self) -> list[tuple[str, str]]:
        """The exact private values of THIS runtime, longest first.

        Longest first matters: ``/home/u/proj`` has to be replaced before ``/home/u``,
        or the shorter rule would leave ``[home]/proj`` behind.
        """
        rules: list[tuple[str, str]] = []

        def add(value: Any, placeholder: str) -> None:
            text = str(value or "")
            if len(text) > 1:
                rules.append((text, placeholder))

        add(self.instance_id, "[redacted]")
        add(self.project_root, "[project_root]")
        add(self.cwd, "[project_root]")
        add(self.supervisor_cwd, "[supervisor_cwd]")
        if self.log_path:
            add(self.log_path, "[runtime_log]")
            add(str(Path(self.log_path).parent), "[runtime_dir]")
        for arg in [*self.cmd, *self.supervisor_cmd]:
            token = str(arg)
            if _ABS_PREFIX_RE.match(token):
                add(token, _basename(token))
        rules.sort(key=lambda rule: len(rule[0]), reverse=True)
        return rules

    def shareable(self) -> dict[str, Any]:
        """Evidence-safe view: no private value, anywhere, at any depth.

        Shared Evidence leaves this machine. It must not carry the operator's home
        directory, the project path, the interpreter the supervisor was launched with,
        the local control-file paths, or the runtime instance id (an identity binding
        for LOCAL process safety, with no business in a shared artifact) — and not only
        where those appear as a whole field. They also hide inside ``--repo=/home/…``,
        inside a quoted path with spaces, and inside diagnostic sentences such as
        "working directory '/home/…' cannot be inspected". So the redaction works on
        VALUES, not on token positions, and then scrubs whatever still looks like a
        path. The local runtime.json keeps all of it — that is what makes a stop safe.
        """
        rules = self.redaction_rules()
        data = _redact(self.to_json(), rules)
        data["project_root"] = "[project_root]"
        data["cwd"] = "[project_root]"
        data["supervisor_cwd"] = "[supervisor_cwd]" if self.supervisor_cwd else ""
        data["log_path"] = _basename(self.log_path) if self.log_path else ""
        data["instance_id"] = "[redacted]" if self.instance_id else ""
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> RuntimeState:
        return cls(
            pid=int(data.get("pid") or 0),
            create_time=float(data.get("create_time") or 0.0),
            session_id=int(data.get("session_id") or 0),
            pgid=int(data.get("pgid") or data.get("session_id") or 0),
            sid=int(data.get("sid") or 0),
            port=int(data.get("port") or 0),
            url=str(data.get("url") or ""),
            project_root=str(data.get("project_root") or ""),
            project_id=str(data.get("project_id") or ""),
            cwd=str(data.get("cwd") or ""),
            cmd_fingerprint=str(data.get("cmd_fingerprint") or ""),
            spec_fingerprint=str(data.get("spec_fingerprint") or ""),
            cmd=[str(a) for a in (data.get("cmd") or [])],
            started_at=float(data.get("started_at") or 0.0),
            log_path=str(data.get("log_path") or ""),
            status=str(data.get("status") or "stopped"),
            survivors=[int(p) for p in (data.get("survivors") or [])],
            stop_error=str(data.get("stop_error") or ""),
            log_error=str(data.get("log_error") or ""),
            identity_reason=str(data.get("identity_reason") or ""),
            supervisor_pid=int(data.get("supervisor_pid") or 0),
            supervisor_create_time=float(data.get("supervisor_create_time") or 0.0),
            supervisor_cmd=[str(a) for a in (data.get("supervisor_cmd") or [])],
            supervisor_cwd=str(data.get("supervisor_cwd") or ""),
            supervisor_fingerprint=str(data.get("supervisor_fingerprint") or ""),
            supervisor_pgid=int(data.get("supervisor_pgid") or 0),
            supervisor_sid=int(data.get("supervisor_sid") or 0),
            app_exit_code=(None if data.get("app_exit_code") is None
                           else int(data["app_exit_code"])),
            instance_id=str(data.get("instance_id") or ""),
        )


def save_state(state: RuntimeState) -> Path:
    """Write runtime.json ATOMICALLY: temp file, fsync, os.replace.

    A half-written state record would be an unusable identity, and an unusable
    identity is exactly what makes a later stop dangerous.
    """
    if state.status in (STATUS_RUNNING, STATUS_STARTING) and not state.create_time:
        raise RuntimeStartError(
            "refusing to persist a live state without a process creation time")
    ensure_runtime_dir(state.project_root)
    path = state_path(state.project_root)
    atomic_write_text(path, json.dumps(state.to_json(), indent=2) + "\n")
    return path


#: Typed outcomes of reading runtime.json.
STATE_ABSENT = "absent"
STATE_VALID = "valid"
STATE_CORRUPT = "corrupt"
STATE_UNREADABLE = "unreadable"


@dataclass
class StateLoad:
    """What reading runtime.json actually told us.

    "There is no state" and "I could not read the state" are different facts.
    Collapsing both into None is what let a corrupted runtime.json start a SECOND
    server beside a live one.
    """

    kind: str
    state: RuntimeState | None = None
    path: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.kind in (STATE_ABSENT, STATE_VALID)

    def to_json(self) -> dict[str, Any]:
        return {"kind": self.kind, "path": self.path, "error": self.error}


def load_state_result(project_root: str | Path) -> StateLoad:
    path = state_path(project_root)
    if not path.is_file():
        return StateLoad(kind=STATE_ABSENT, path=str(path))
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return StateLoad(kind=STATE_UNREADABLE, path=str(path),
                         error=f"{type(exc).__name__}: {exc}")
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("runtime.json is not a JSON object")
        state = RuntimeState.from_json(data)
    except (ValueError, TypeError) as exc:
        return StateLoad(kind=STATE_CORRUPT, path=str(path),
                         error=f"{type(exc).__name__}: {exc}")
    return StateLoad(kind=STATE_VALID, state=state, path=str(path))


def load_state(project_root: str | Path) -> RuntimeState | None:
    """Convenience reader. Callers that must ACT use load_state_result()."""
    return load_state_result(project_root).state


def log_failure_note_path(project_root: str | Path) -> Path:
    """The supervisor's private note about a diagnostic it could not persist.

    Written only when a log-failure cleanup left a SURVIVOR and runtime.json could not be
    updated. It is a note for a human, never signal authority — nothing reads it to decide
    what to kill — and its life is tied to the state it describes.
    """
    return runtime_dir(project_root) / "runtime.log_failure.json"


def clear_state(project_root: str | Path) -> None:
    """Remove the durable record — and the note that only described it.

    The note exists to explain a state that could not be written properly. Once that state
    is definitively gone (a stop that confirmed every process is gone), the note describes
    nothing and must not outlive it. While a survivor still depends on the state, the state
    is not cleared, so this never runs and the note stays.
    """
    with contextlib.suppress(OSError):
        state_path(project_root).unlink()
    with contextlib.suppress(OSError):
        log_failure_note_path(project_root).unlink()


def _normalize_argv(argv: list[str]) -> list[str]:
    """Strip cosmetic whitespace. Nothing else is smoothed over."""
    return [str(a).strip() for a in argv if str(a).strip()]


def cmdline_matches(recorded: list[str], actual: list[str]) -> bool:
    """Does a live process's cmdline correspond to the argv we launched?

    Exact equality is the normal case. Exactly TWO deviations are tolerated, both of
    them observed facts about real launchers rather than convenience:

    1. **script shim** — a launcher that is a script appears with its interpreter:
       ``npm run dev --port 5173`` is reported as
       ``node /usr/bin/npm run dev --port 5173``. Accepted when every ARGUMENT after
       the launcher is identical (which is what pins the port, the host and the
       script) and one of the leading executable tokens IS the recorded launcher, by
       file name.
    2. **process-title rewrite** — npm rewrites its own title, so the kernel reports
       one padded string: ``["npm run dev --port 5173 --host 127.0.0.1", "", "", …]``.
       Accepted when that title's tokens equal the recorded argv with pure separator
       tokens (``--``) removed, and the launcher matches by file name.

    Nothing else matches: a different argument, a different order, or a missing
    launcher is a mismatch — and a mismatch is never killed.
    """
    rec = _normalize_argv(recorded)
    act = _normalize_argv(actual)
    if not rec or not act:
        return False
    if act == rec:
        return True

    launcher = Path(rec[0]).name

    # (2) process-title rewrite: the whole command collapsed into one token.
    if len(act) == 1 and " " in act[0]:
        title = act[0].split()
        expected = [a for a in rec if a != "--"]
        if (len(title) == len(expected)
                and Path(title[0]).name == launcher
                and title[1:] == expected[1:]):
            return True

    # (1) script shim: interpreter(s) in front, identical argument tail.
    if len(act) <= len(rec):
        return False
    tail_len = len(rec) - 1
    if tail_len and act[-tail_len:] != rec[1:]:
        return False
    leading = act[: len(act) - tail_len] if tail_len else act
    return any(Path(tok).name == launcher for tok in leading)


@dataclass
class IdentityCheck:
    """The verdict on whether a recorded runtime really is a live managed process."""

    classification: str = IDENTITY_UNPROVEN
    reason: str = ""
    live_pgid: int = 0
    live_sid: int = 0

    @property
    def verified(self) -> bool:
        return self.classification == VERIFIED

    @property
    def may_auto_clear(self) -> bool:
        """Only a process that is CONCLUSIVELY gone, or a proven PID reuse, may have
        its record dropped automatically. Anything unproven keeps its state."""
        return self.classification in (DEFINITELY_GONE, PID_REUSED)

    def to_json(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "reason": self.reason,
            "live_pgid": self.live_pgid,
            "live_sid": self.live_sid,
        }


def classify_state(state: RuntimeState | None,
                   project_root: str | Path | None = None,
                   *, require_cwd: bool = True) -> IdentityCheck:
    """Classify a recorded runtime against the live process table.

    Every identity component must hold before anything destructive may happen:
    project root and digest, pid, creation time, cmdline, cwd, fingerprint — AND the
    live process group and session, because those are exactly what a ``killpg``
    would fall on. A component that cannot be INSPECTED gives ``identity_unproven``:
    we neither kill nor forget. A component that is inspectable and WRONG gives
    ``identity_mismatch``. Only a vanished process or a proven PID reuse is
    automatically clearable.

    ``require_cwd``: on many Linux systems a NEW process cannot read
    ``/proc/<pid>/cwd`` of a detached, reparented process — the kernel denies it even
    to the same user. Demanding it there would make a separate `runtime probe`/`stop`
    impossible. So callers that have ALREADY verified the supervisor (which owns this
    app, carries the runtime instance id in its live argv, and is itself fully checked)
    may set ``require_cwd=False``: the cwd is still compared when it is readable, and
    only an UNREADABLE cwd is tolerated. A wrong cwd is always a mismatch, and the
    stricter in-process path keeps ``require_cwd=True``.
    """
    import psutil

    if state is None or not state.pid or state.status not in LIVE_STATUSES:
        return IdentityCheck(DEFINITELY_GONE, "no live runtime recorded")

    if project_root is not None:
        wanted = str(Path(project_root).resolve())
        if state.project_root and wanted != state.project_root:
            return IdentityCheck(
                IDENTITY_MISMATCH,
                f"recorded project root {state.project_root!r} is not {wanted!r}")
        if state.project_id and state.project_id != project_digest(wanted):
            return IdentityCheck(
                IDENTITY_MISMATCH,
                "recorded project digest does not match this project")

    if not state.create_time:
        return IdentityCheck(IDENTITY_MISMATCH,
                             "recorded runtime has no process creation time")

    try:
        proc = psutil.Process(state.pid)
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
    except psutil.Error as exc:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             f"pid {state.pid} not inspectable: {exc}")

    try:
        if abs(proc.create_time() - state.create_time) > 1.0:
            return IdentityCheck(
                PID_REUSED,
                f"pid {state.pid} was reused: creation time does not match the "
                f"recorded runtime")
        if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:
            return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is not running")
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
    except psutil.Error as exc:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             f"pid {state.pid} not inspectable: {exc}")

    try:
        actual_cmd = _normalize_argv(proc.cmdline())
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
    except (psutil.AccessDenied, psutil.Error) as exc:
        return IdentityCheck(
            IDENTITY_UNPROVEN,
            f"pid {state.pid} command line cannot be inspected ({exc})")
    if not cmdline_matches(state.cmd, actual_cmd):
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"pid {state.pid} runs a different command than the recorded runtime")

    actual_cwd = ""
    try:
        actual_cwd = str(Path(proc.cwd()).resolve())
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
    except (psutil.AccessDenied, psutil.Error) as exc:
        if require_cwd:
            return IdentityCheck(
                IDENTITY_UNPROVEN,
                f"pid {state.pid} working directory cannot be inspected ({exc})")
        # Tolerated only because the caller has already verified the supervisor that
        # owns this process. Everything else still has to agree.
    if actual_cwd and state.cwd and actual_cwd != str(Path(state.cwd).resolve()):
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"pid {state.pid} runs in {actual_cwd!r}, not the recorded "
            f"{state.cwd!r}")

    expected = resolved_fingerprint(state.cmd, state.cwd or actual_cwd or ".",
                                    state.project_id)
    if not state.cmd_fingerprint or expected != state.cmd_fingerprint:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"pid {state.pid} fingerprint does not match the recorded runtime")

    # --- the process GROUP and SESSION: what a killpg would actually hit -----
    try:
        live_pgid = os.getpgid(state.pid)
        live_sid = os.getsid(state.pid)
    except (OSError, ProcessLookupError) as exc:
        return IdentityCheck(
            IDENTITY_UNPROVEN,
            f"pid {state.pid} process group cannot be inspected ({exc})")

    if state.pgid and live_pgid != state.pgid:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"pid {state.pid} lives in process group {live_pgid}, not the recorded "
            f"{state.pgid}")
    if state.sid and live_sid != state.sid:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"pid {state.pid} lives in session {live_sid}, not the recorded "
            f"{state.sid}")
    if live_pgid == os.getpgrp() or live_sid == os.getsid(0):
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"recorded runtime shares Remedy's own process group/session "
            f"({live_pgid}/{live_sid}); refusing to signal it")

    return IdentityCheck(VERIFIED, "", live_pgid=live_pgid, live_sid=live_sid)


def classify_supervisor(state: RuntimeState | None,
                       project_root: str | Path | None = None) -> IdentityCheck:
    """Same identity discipline as the application, applied to the SUPERVISOR.

    A supervisor is the process that OWNS the app after the initiating CLI exits.
    Before it is signalled, its pid, creation time, cmdline, cwd, fingerprint and
    live process group/session must all agree — and it must never be Remedy's own
    group.
    """
    import psutil

    if state is None or not state.supervisor_pid:
        return IdentityCheck(DEFINITELY_GONE, "no supervisor recorded")

    try:
        proc = psutil.Process(state.supervisor_pid)
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE,
                             f"supervisor pid {state.supervisor_pid} is gone")
    except psutil.Error as exc:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             f"supervisor pid not inspectable: {exc}")

    try:
        if state.supervisor_create_time and abs(
                proc.create_time() - state.supervisor_create_time) > 1.0:
            return IdentityCheck(
                PID_REUSED,
                f"supervisor pid {state.supervisor_pid} was reused")
        if not proc.is_running() or proc.status() == psutil.STATUS_ZOMBIE:
            return IdentityCheck(DEFINITELY_GONE,
                                 f"supervisor pid {state.supervisor_pid} is not running")
        actual_cmd = _normalize_argv(proc.cmdline())
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE,
                             f"supervisor pid {state.supervisor_pid} is gone")
    except (psutil.AccessDenied, psutil.Error) as exc:
        return IdentityCheck(
            IDENTITY_UNPROVEN,
            f"supervisor pid {state.supervisor_pid} cannot be inspected ({exc})")

    if state.supervisor_cmd and not cmdline_matches(state.supervisor_cmd, actual_cmd):
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"supervisor pid {state.supervisor_pid} runs a different command")

    # The runtime instance id must be present in the supervisor's LIVE argv, not just
    # in the file: a stale or forged runtime.json cannot conjure it into a process.
    if state.instance_id and state.instance_id not in actual_cmd:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"supervisor pid {state.supervisor_pid} does not carry this runtime's "
            f"instance id")
    if state.supervisor_pid and not state.instance_id:
        return IdentityCheck(
            IDENTITY_UNPROVEN,
            "recorded supervisor has no runtime instance id to bind it to this state")

    expected = resolved_fingerprint(
        state.supervisor_cmd, state.supervisor_cwd or ".", state.project_id)
    if state.supervisor_fingerprint and expected != state.supervisor_fingerprint:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"supervisor pid {state.supervisor_pid} fingerprint does not match")

    try:
        live_pgid = os.getpgid(state.supervisor_pid)
        live_sid = os.getsid(state.supervisor_pid)
    except (OSError, ProcessLookupError) as exc:
        return IdentityCheck(
            IDENTITY_UNPROVEN,
            f"supervisor process group cannot be inspected ({exc})")
    if state.supervisor_pgid and live_pgid != state.supervisor_pgid:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"supervisor lives in group {live_pgid}, not the recorded "
            f"{state.supervisor_pgid}")
    if state.supervisor_sid and live_sid != state.supervisor_sid:
        return IdentityCheck(
            IDENTITY_MISMATCH,
            f"supervisor lives in session {live_sid}, not the recorded "
            f"{state.supervisor_sid}")
    if live_pgid == os.getpgrp() or live_sid == os.getsid(0):
        return IdentityCheck(
            IDENTITY_MISMATCH,
            "recorded supervisor shares Remedy's own process group/session")

    return IdentityCheck(VERIFIED, "", live_pgid=live_pgid, live_sid=live_sid)


# ---------------------------------------------------------------------------
# ONE identity contract for serve, probe and stop
# ---------------------------------------------------------------------------

#: Who owns the recorded runtime right now.
OWNER_SUPERVISED = "supervised"                  # verified supervisor OWNS a verified app
OWNER_UNSUPERVISED = "unsupervised"              # no supervisor recorded (one-shot probe)
OWNER_SUPERVISOR_MISSING = "supervisor_missing"  # supervisor gone: ownership unprovable
OWNER_GONE = "gone"                              # nothing left to own
OWNER_UNTRUSTED = "untrusted"                    # do not touch, do not delete

#: How far up the process tree the supervisor is looked for. The application is the
#: supervisor's direct child, so 1 would do; a few generations are allowed for a
#: launcher shim without ever walking to init.
MAX_ANCESTRY_DEPTH = 8


def supervisor_owns_app(state: RuntimeState,
                        supervisor: IdentityCheck) -> IdentityCheck:
    """Prove a LIVE ownership relationship between the app and its supervisor.

    Two records that each match on their own prove nothing about each other. A
    manipulated runtime.json could name a verified supervisor and, beside it, an
    unrelated process that happens to run the same argv in the same directory — and a
    stop would then fall on that stranger. So while the supervisor is alive, the
    recorded application must really BE its child: its live ancestor chain has to reach
    the verified supervisor pid (whose creation time is checked again on the way), and
    the recorded pid must be the leader of the app's own process group — the group a
    ``killpg`` would take.
    """
    import psutil

    if not supervisor.verified:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             "the supervisor is not verified; ownership cannot be shown")

    try:
        app = psutil.Process(state.pid)
    except psutil.NoSuchProcess:
        return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
    except psutil.Error as exc:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             f"pid {state.pid} not inspectable: {exc}")

    # The signalled process must be the leader of its own group: a non-leader would
    # mean the group we would kill is somebody else's.
    try:
        if os.getpgid(state.pid) != state.pid:
            return IdentityCheck(
                IDENTITY_MISMATCH,
                f"pid {state.pid} does not lead its own process group; the recorded "
                f"runtime is not the process this supervisor launched")
    except (OSError, ProcessLookupError) as exc:
        return IdentityCheck(IDENTITY_UNPROVEN,
                             f"pid {state.pid} process group cannot be read ({exc})")

    node = app
    for _ in range(MAX_ANCESTRY_DEPTH):
        try:
            parent = node.parent()
        except psutil.NoSuchProcess:
            return IdentityCheck(DEFINITELY_GONE, f"pid {state.pid} is gone")
        except psutil.Error as exc:
            return IdentityCheck(
                IDENTITY_UNPROVEN,
                f"the ancestry of pid {state.pid} cannot be inspected ({exc})")
        if parent is None:
            break
        if parent.pid == state.supervisor_pid:
            try:
                if (state.supervisor_create_time
                        and abs(parent.create_time()
                                - state.supervisor_create_time) > 1.0):
                    return IdentityCheck(
                        PID_REUSED,
                        f"the parent of pid {state.pid} is not the recorded supervisor "
                        f"(pid {state.supervisor_pid} was reused)")
            except psutil.Error as exc:
                return IdentityCheck(
                    IDENTITY_UNPROVEN,
                    f"the parent of pid {state.pid} cannot be inspected ({exc})")
            return IdentityCheck(VERIFIED, "")
        if parent.pid <= 1:
            break
        node = parent

    return IdentityCheck(
        IDENTITY_MISMATCH,
        f"pid {state.pid} is not a descendant of the recorded supervisor "
        f"(pid {state.supervisor_pid}); the recorded application does not belong to it")


@dataclass
class RuntimeIdentity:
    """The single verdict `serve`, `probe` and `stop` all act on.

    Before this existed, each command decided for itself whether the application's
    live cwd was required — and `serve` still asked for it first, which is why a
    second `serve` failed on systems that deny ``/proc/<pid>/cwd`` for a detached
    process. The rule is one rule now: **classify the supervisor first**. A verified
    supervisor is the authoritative owner of the application, so the app's cwd is only
    compared when it can be READ. A wrong cwd is always a mismatch, and nothing is ever
    signalled on an unproven identity.
    """

    supervisor: IdentityCheck
    app: IdentityCheck
    ownership: str
    reason: str = ""

    @property
    def usable(self) -> bool:
        """A live, fully owned runtime a command may report and use."""
        return self.ownership in (OWNER_SUPERVISED, OWNER_UNSUPERVISED)

    @property
    def may_auto_clear(self) -> bool:
        return self.ownership == OWNER_GONE

    def to_json(self) -> dict[str, Any]:
        return {
            "ownership": self.ownership,
            "reason": self.reason,
            "supervisor": self.supervisor.to_json(),
            "app": self.app.to_json(),
        }


def classify_runtime(state: RuntimeState | None,
                     project_root: str | Path | None = None) -> RuntimeIdentity:
    """Supervisor first, then the application — and then the LINK between them.

    * supervisor verified → the app may be verified without reading its live cwd, but
      it must also be a live descendant of that supervisor and the leader of its own
      process group (:func:`supervisor_owns_app`). Two records that merely match on
      their own are not ownership: an unrelated process running the same argv in the
      same directory would satisfy them, and a stop would then kill a stranger;
    * supervisor conclusively gone → ownership can no longer be shown at all: a
      reparented process has no parent left to prove anything with, and every field in
      runtime.json is mutable. The runtime is `supervisor_missing`, and NOTHING is
      killed automatically — safety before automatic orphan cleanup;
    * supervisor unprovable or mismatched → nothing is relaxed and nothing is touched.
    """
    sup = classify_supervisor(state, project_root)

    if state is None or not state.pid:
        return RuntimeIdentity(sup, IdentityCheck(DEFINITELY_GONE,
                                                  "no live runtime recorded"),
                               OWNER_GONE, "no runtime recorded")

    recorded_supervisor = bool(state.supervisor_pid)
    supervisor_gone = sup.classification in (DEFINITELY_GONE, PID_REUSED)

    # The cwd may be skipped only for an owner we have already proved (a verified
    # supervisor). An unproven, mismatched or dead supervisor relaxes nothing.
    app = classify_state(state, project_root, require_cwd=not sup.verified)

    if not recorded_supervisor:
        if app.verified:
            return RuntimeIdentity(sup, app, OWNER_UNSUPERVISED, "")
        if app.may_auto_clear:
            return RuntimeIdentity(sup, app, OWNER_GONE, app.reason)
        return RuntimeIdentity(sup, app, OWNER_UNTRUSTED, app.reason)

    if sup.verified:
        if app.may_auto_clear:
            # The supervisor is alive but its app is gone; the supervisor itself is
            # still a managed process, so this is not "nothing to do".
            return RuntimeIdentity(sup, app, OWNER_UNTRUSTED, app.reason)
        if not app.verified:
            return RuntimeIdentity(sup, app, OWNER_UNTRUSTED, app.reason)

        owned = supervisor_owns_app(state, sup)
        if not owned.verified:
            return RuntimeIdentity(sup, owned, OWNER_UNTRUSTED, owned.reason)
        # The ownership check confirms the group; keep the live group/session numbers
        # the application check observed.
        return RuntimeIdentity(sup, app, OWNER_SUPERVISED, "")

    if supervisor_gone:
        if app.may_auto_clear:
            return RuntimeIdentity(sup, app, OWNER_GONE,
                                   f"supervisor and application are gone ({sup.reason})")
        return RuntimeIdentity(
            sup, app, OWNER_SUPERVISOR_MISSING,
            f"the supervisor is gone ({sup.reason}); the recorded application "
            f"({state.pid}) can no longer be proven to belong to this runtime, so it "
            f"is neither trusted nor signalled")

    # Supervisor unproven or mismatched: the record is the only reference to whatever
    # is running. Keep it, kill nothing.
    return RuntimeIdentity(sup, app, OWNER_UNTRUSTED, sup.reason)


def verify_state(state: RuntimeState | None,
                 project_root: str | Path | None = None) -> tuple[bool, str]:
    """Boolean view of :func:`classify_state`, kept for existing callers."""
    check = classify_state(state, project_root)
    if check.verified:
        return True, ""
    return False, check.reason or check.classification


# ---------------------------------------------------------------------------
# Ports and readiness
# ---------------------------------------------------------------------------

def port_is_free(port: int, host: str = DEFAULT_HOST) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, int(port)))
        except OSError:
            return False
    return True


def pick_free_port(host: str = DEFAULT_HOST) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def choose_port(requested: int, host: str = DEFAULT_HOST) -> int:
    """Prefer the requested port; fall back to a free one. Never kill the squatter."""
    if port_is_free(requested, host):
        return int(requested)
    return pick_free_port(host)


@dataclass
class RuntimeProbeResult:
    ok: bool = False
    status_code: int = 0
    url: str = ""
    port: int = 0
    elapsed_s: float = 0.0
    error: str = ""
    error_class: str = ""       # "" | "config" | "start" | "ready" | "stop"
    log_tail: str = ""
    pid: int = 0
    survivors: list[int] = field(default_factory=list)
    log_error: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "log_error": self.log_error,
            "status_code": self.status_code,
            "url": self.url,
            "port": self.port,
            "elapsed_s": round(self.elapsed_s, 3),
            "error": self.error,
            "error_class": self.error_class,
            "log_tail": self.log_tail,
            "pid": self.pid,
            "survivors": list(self.survivors),
        }


def http_probe(url: str, timeout: float = 3.0) -> tuple[int, str]:
    """One HTTP GET. Returns (status, error). Never raises."""
    req = urllib.request.Request(url, method="GET")  # noqa: S310 - loopback only
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return int(resp.status), ""
    except urllib.error.HTTPError as exc:
        return int(exc.code), ""
    except urllib.error.URLError as exc:
        return 0, str(exc.reason)
    except (TimeoutError, OSError) as exc:
        return 0, str(exc)


# ---------------------------------------------------------------------------
# Bounded log pump
# ---------------------------------------------------------------------------

def _process_create_time(pid: int) -> float:
    """The process creation time — the second half of a managed process's identity."""
    import psutil
    return float(psutil.Process(pid).create_time())


class LogPump:
    """Drain the child's merged stdout/stderr into a CAPPED runtime.log.

    The log file is opened SYNCHRONOUSLY by the caller before ``Popen`` — a log that
    cannot be opened is a startup failure, not an error string discovered later
    inside a thread while the server is already running. The thread then only reads
    the pipe (so the child never blocks) and trims the file to the newest
    ``keep_bytes`` whenever it passes ``max_bytes``. ``start()`` waits for the thread
    to actually be pumping, so a pump that dies immediately fails the start.
    """

    def __init__(self, stream, handle, path: Path, *,
                 max_bytes: int | None = None, keep_bytes: int | None = None):
        self.stream = stream
        self.handle = handle                 # an already-open binary file object
        self.path = Path(path)
        self.max_bytes = int(MAX_LOG_BYTES if max_bytes is None else max_bytes)
        self.keep_bytes = int(LOG_KEEP_BYTES if keep_bytes is None else keep_bytes)
        self.error: str = ""
        self.started = threading.Event()
        # Daemon by necessity: a blocked read() on the pipe of a process that
        # SURVIVED a failed stop cannot be interrupted from another thread, and a
        # non-daemon pump would hang the interpreter at exit. It is joined on every
        # normal stop.
        self._thread = threading.Thread(target=self._run, name="remedy-log-pump",
                                        daemon=True)

    @classmethod
    def open_log(cls, path: Path):
        """Open runtime.log up front, owner-only. Raises OSError — before any process
        exists, so a log that cannot be opened is a startup failure."""
        return open_private_file(path)

    def start(self, timeout: float = 5.0) -> None:
        """Start the pump and WAIT until it is really pumping (or has failed)."""
        self._thread.start()
        if not self.started.wait(timeout):
            raise RuntimeStartError("log pump did not start within its timeout")
        if self.error:
            raise RuntimeStartError(f"runtime log could not be pumped: {self.error}")

    def _run(self) -> None:
        try:
            out = self.handle
            out.write(b"")                   # prove the handle is really writable
            written = 0
            self.started.set()
            read = getattr(self.stream, "read1", None) or self.stream.read
            while True:
                # read1(): hand over whatever the child already wrote instead of
                # blocking for a full chunk. The pipe must never back up.
                chunk = read(LOG_CHUNK_BYTES)
                if not chunk:
                    break
                out.write(chunk)
                written += len(chunk)
                if written > self.max_bytes:
                    written = self._trim(out)
        except Exception as exc:            # surfaced, never swallowed
            self.error = f"{type(exc).__name__}: {exc}"
        finally:
            self.started.set()
            with contextlib.suppress(Exception):
                self.stream.close()
            with contextlib.suppress(Exception):
                self.handle.close()

    def _trim(self, out) -> int:
        """Keep only the newest bytes. Returns the new size."""
        out.flush()
        with self.path.open("rb") as fh:
            fh.seek(max(0, self.path.stat().st_size - self.keep_bytes))
            tail = fh.read()
        out.seek(0)
        out.truncate(0)
        out.write(b"[... older output dropped: log capped ...]\n")
        out.write(tail)
        out.flush()
        return self.path.stat().st_size

    def join(self, timeout: float = 5.0) -> None:
        if self._thread.is_alive():
            self._thread.join(timeout)

    @property
    def alive(self) -> bool:
        return self._thread.is_alive()


def read_log_tail(path: str | Path, max_bytes: int = LOG_TAIL_BYTES) -> str:
    """Bounded read: only ever the last ``max_bytes`` of the log."""
    p = Path(path)
    if not p.is_file():
        return ""
    try:
        size = p.stat().st_size
        with p.open("rb") as fh:
            if size > max_bytes:
                fh.seek(size - max_bytes)
            data = fh.read(max_bytes)
    except OSError as exc:
        return f"[log unavailable: {exc}]"
    text = data.decode("utf-8", errors="replace")
    if size > max_bytes:
        text = "[... truncated ...]\n" + text
    return text


# ---------------------------------------------------------------------------
# The managed dev server
# ---------------------------------------------------------------------------

class DevServer:
    """Own one dev-server process tree for one project."""

    def __init__(self, spec: RuntimeSpec, project_root: str | Path):
        self.project_root = str(Path(project_root).resolve())
        self.spec = validate_spec(spec, self.project_root)
        self.port: int = 0
        self.proc: subprocess.Popen | None = None
        self.log_file = log_path(self.project_root)
        self.pump: LogPump | None = None
        self.pump_leaked: bool = False
        self.session_id: int = 0
        self.pgid: int = 0
        self.sid: int = 0
        self.state: RuntimeState | None = None
        self._pump_error: str = ""

    @property
    def url(self) -> str:
        return f"http://{self.spec.host}:{self.port}{self.spec.health_path}"

    # -- start: all or nothing --------------------------------------------

    def start(self) -> RuntimeState:
        """Launch the server. Either a managed runtime, or NOTHING left behind.

        The log is opened BEFORE the process exists, so a log failure can never leave
        a live server with no log. Any failure after Popen — the pump handshake,
        creation time, group inspection, serialization, the atomic write — rolls the
        whole start back. If the rollback cannot kill the process, the failure SAYS
        so (survivors travel on the exception) instead of pretending the start was
        atomic. State is persisted as ``starting``: only readiness promotes it.
        """
        self.port = choose_port(self.spec.port, self.spec.host)
        argv = self.spec.resolved_cmd(self.port)
        env = self.spec.resolved_env(self.port)

        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeStartError(
                f"runtime directory not writable: {type(exc).__name__}: {exc}"
            ) from exc
        try:
            handle = LogPump.open_log(self.log_file)
        except OSError as exc:
            raise RuntimeStartError(
                f"runtime log could not be opened: {type(exc).__name__}: {exc}"
            ) from exc

        try:
            self.proc = subprocess.Popen(          # noqa: S603 - argv, never shell
                argv,
                cwd=self.spec.cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,            # own session => own process tree
            )
        except (OSError, ValueError) as exc:
            with contextlib.suppress(Exception):
                handle.close()
            raise RuntimeStartError(
                f"could not start {shlex.join(argv)}: {type(exc).__name__}: {exc}"
            ) from exc

        state: RuntimeState | None = None
        try:
            self.pump = LogPump(self.proc.stdout, handle, self.log_file)
            self.pump.start()                      # synchronous handshake

            create_time = _process_create_time(self.proc.pid)
            if not create_time:
                raise RuntimeStartError("process creation time is unavailable")

            self.pgid = os.getpgid(self.proc.pid)
            self.sid = os.getsid(self.proc.pid)
            self.session_id = self.pgid

            state = RuntimeState(
                pid=self.proc.pid,
                create_time=create_time,
                session_id=self.session_id,
                pgid=self.pgid,
                sid=self.sid,
                port=self.port,
                url=self.url,
                project_root=self.project_root,
                project_id=project_digest(self.project_root),
                cwd=str(Path(self.spec.cwd).resolve()),
                cmd_fingerprint=resolved_fingerprint(
                    argv, self.spec.cwd, project_digest(self.project_root)),
                spec_fingerprint=self.spec.fingerprint(),
                cmd=argv,
                started_at=time.time(),
                log_path=str(self.log_file),
                status=STATUS_STARTING,            # NOT running until it is ready
            )
            save_state(state)
        except Exception as exc:
            rollback = self._abort_start(state_hint=state)
            message = (str(exc) if isinstance(exc, RuntimeStartError)
                       else f"runtime start failed: {type(exc).__name__}: {exc}")
            if rollback["survivors"]:
                message += (
                    f"; ROLLBACK INCOMPLETE: managed processes survived "
                    f"{rollback['survivors']}. "
                    + ("A start_cleanup_failed state was kept: run "
                       "`remedy runtime stop` to retry."
                       if not rollback["partial_state_removed"]
                       else f"No durable state could be written: kill "
                            f"{rollback['survivors']} manually.")
                )
            err = RuntimeStartError(message)
            err.rollback = rollback                # type: ignore[attr-defined]
            raise err from exc

        self.state = state
        return state

    def mark_running(self) -> RuntimeState:
        """Promote a ``starting`` runtime to ``running`` — only after HTTP readiness.

        Nothing may report a runtime as running before it answered its health URL:
        that is what let a second `serve` claim `already_running` for a server that
        was about to time out.
        """
        if self.state is None:
            raise RuntimeStartError("no started runtime to mark running")
        self.state.status = STATUS_RUNNING
        self.state.log_error = self.pump.error if self.pump else ""
        save_state(self.state)
        return self.state

    def _abort_start(self, state_hint: RuntimeState | None = None) -> dict[str, Any]:
        """Undo a failed start — and REPORT whatever could not be undone."""
        result = stop_process_tree(self.proc.pid if self.proc else 0,
                                   session_id=self.pgid or self.session_id)
        if self.proc is not None:
            with contextlib.suppress(Exception):
                self.proc.wait(timeout=GRACE_SECONDS)
        self._close_pump()

        survivors = list(result.get("survivors") or [])
        rollback: dict[str, Any] = {
            "stopped": not survivors,
            "survivors": survivors,
            "stop_error": result.get("error", ""),
            "pump_status": "leaked" if self.pump_leaked else "joined",
            "partial_state_removed": True,
        }
        if not survivors:
            clear_state(self.project_root)
            return rollback

        # A survivor means the start was NOT all-or-nothing. Keep enough identity to
        # retry the stop, and say so.
        keep = state_hint or self.state
        if keep is not None:
            keep.status = STATUS_START_CLEANUP_FAILED
            keep.survivors = survivors
            keep.stop_error = result.get("error") or (
                f"processes survived the startup rollback: {survivors}")
            try:
                save_state(keep)
                rollback["partial_state_removed"] = False
            except Exception as exc:
                rollback["stop_error"] += f"; state not persisted: {exc}"
        return rollback

    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    # -- readiness ---------------------------------------------------------

    def wait_ready(self) -> RuntimeProbeResult:
        """Poll until the health URL answers — or the process dies, or time runs out.

        A failure stops the process tree. State is cleared ONLY when no managed
        process survived; a survivor is reported instead of being papered over.
        """
        started = time.monotonic()
        deadline = started + self.spec.ready_timeout_s
        last_error = ""
        while time.monotonic() < deadline:
            if not self.alive():
                code = self.proc.returncode if self.proc else -1
                stop = self.stop()
                return RuntimeProbeResult(
                    ok=False, port=self.port, url=self.url,
                    elapsed_s=time.monotonic() - started,
                    error=f"process exited before readiness (exit code {code})",
                    error_class="start", log_tail=self.logs(),
                    survivors=stop.get("survivors", []),
                )
            status, err = http_probe(self.url, timeout=2.0)
            if READY_STATUS_MIN <= status <= READY_STATUS_MAX:
                return RuntimeProbeResult(
                    ok=True, status_code=status, port=self.port, url=self.url,
                    elapsed_s=time.monotonic() - started,
                    pid=self.proc.pid if self.proc else 0,
                    log_error=self.pump.error if self.pump else "",
                )
            last_error = err or f"health status {status}"
            time.sleep(0.15)

        stop = self.stop()
        return RuntimeProbeResult(
            ok=False, port=self.port, url=self.url,
            elapsed_s=time.monotonic() - started,
            error=(
                f"not ready after {self.spec.ready_timeout_s}s"
                + (f": {last_error}" if last_error else "")
            ),
            error_class="ready", log_tail=self.logs(),
            survivors=stop.get("survivors", []),
        )

    def probe(self) -> RuntimeProbeResult:
        """One-shot probe of an already-running managed server."""
        started = time.monotonic()
        if not self.alive():
            return RuntimeProbeResult(
                ok=False, port=self.port, url=self.url, error="process is not running",
                error_class="start", log_tail=self.logs(),
            )
        status, err = http_probe(self.url, timeout=3.0)
        ok = READY_STATUS_MIN <= status <= READY_STATUS_MAX
        return RuntimeProbeResult(
            ok=ok, status_code=status, port=self.port, url=self.url,
            elapsed_s=time.monotonic() - started,
            error="" if ok else (err or f"health status {status}"),
            error_class="" if ok else "ready",
            log_tail="" if ok else self.logs(),
            pid=self.proc.pid if self.proc else 0,
            log_error=(self.pump.error if self.pump else "") or self._pump_error,
        )

    def logs(self, max_bytes: int = LOG_TAIL_BYTES) -> str:
        return read_log_tail(self.log_file, max_bytes)

    # -- stop --------------------------------------------------------------

    def stop(self) -> dict[str, Any]:
        """Stop the WHOLE tree and reap it. Idempotent; never raises.

        State is cleared only when nothing survived. A survivor keeps a retryable
        ``stop_failed`` record on disk instead of a comfortable lie.
        """
        # We started this process ourselves, so its group is the one we observed at
        # start — never a number read back from a file.
        result = stop_process_tree(self.proc.pid if self.proc else 0,
                                   session_id=self.pgid or self.session_id)
        if self.proc is not None:
            with contextlib.suppress(Exception):
                self.proc.wait(timeout=GRACE_SECONDS)   # reap: no zombie parent
        self._close_pump()

        if result["survivors"]:
            state = self.state or load_state(self.project_root)
            if state is not None:
                state.status = STATUS_STOP_FAILED
                state.log_error = self.pump_error
                state.survivors = list(result["survivors"])
                state.stop_error = result.get("error") or (
                    f"managed processes survived the stop: {result['survivors']}")
                with contextlib.suppress(Exception):
                    save_state(state)
        else:
            clear_state(self.project_root)
        return result

    @property
    def pump_error(self) -> str:
        """A pump failure discovered AFTER startup, surfaced by probe/stop/results."""
        return self._pump_error

    def _close_pump(self) -> None:
        """Join the log pump — and never leave it blocked on a live pipe.

        If a managed process SURVIVED the stop, its pipe never reaches EOF, so the
        pump would block forever on read() and, being non-daemon, would hang the
        interpreter at exit. So: join briefly, and if it is still blocked, close the
        read end underneath it, which makes the read fail and the thread finish.
        """
        if self.pump is None:
            return
        self.pump.join(timeout=GRACE_SECONDS)
        self._pump_error = self.pump.error
        if self.pump.alive:
            # Only possible when a managed process survived the stop and is still
            # holding the pipe open. That survivor is already reported; do NOT block
            # here trying to close a stream the pump is reading.
            self.pump_leaked = True
        else:
            self.pump_leaked = False
            if self.proc is not None and self.proc.stdout is not None:
                with contextlib.suppress(Exception):
                    self.proc.stdout.close()
        self.pump = None


# ---------------------------------------------------------------------------
# Process-tree shutdown
# ---------------------------------------------------------------------------

def _session_members(session_id: int) -> list[Any]:
    """Every live process still in the managed process group."""
    import psutil

    if not session_id:
        return []
    members = []
    for proc in psutil.process_iter(["pid"]):
        with contextlib.suppress(psutil.Error, OSError, ProcessLookupError):
            if os.getpgid(proc.pid) == session_id:
                members.append(proc)
    return members


def stop_process_tree(pid: int, grace: float = GRACE_SECONDS,
                      session_id: int = 0) -> dict[str, Any]:
    """Terminate a process and every descendant; kill whatever survives.

    Never raises. After the first sweep the managed process GROUP is enumerated
    again, so a child spawned during shutdown — one that was simply not in the first
    psutil snapshot — cannot escape. Nothing is ever killed by port.
    """
    import psutil

    out: dict[str, Any] = {
        "pid": pid, "session_id": session_id,
        "terminated": [], "killed": [], "survivors": [], "error": "",
    }
    if not pid:
        return out

    if not session_id:
        with contextlib.suppress(OSError, ProcessLookupError):
            session_id = os.getpgid(pid)
            out["session_id"] = session_id

    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        parent = None
    except psutil.Error as exc:
        out["error"] = f"{type(exc).__name__}: {exc}"
        parent = None

    family: list[Any] = []
    if parent is not None:
        try:
            family = parent.children(recursive=True) + [parent]
        except psutil.Error as exc:
            family = [parent]
            out["error"] = f"could not enumerate descendants: {exc}"

    if not family and not session_id:
        return out                     # already gone: idempotent

    for proc in family:
        with contextlib.suppress(psutil.Error):
            proc.terminate()
            out["terminated"].append(proc.pid)

    _gone, alive = psutil.wait_procs(family, timeout=grace)
    for proc in alive:
        with contextlib.suppress(psutil.Error):
            proc.kill()
            out["killed"].append(proc.pid)
    _gone2, still = psutil.wait_procs(alive, timeout=grace)

    # --- second sweep: the process GROUP, not the stale snapshot -------------
    stragglers = [p for p in _session_members(session_id) if p.pid != os.getpid()]
    if stragglers:
        with contextlib.suppress(OSError, ProcessLookupError):
            os.killpg(session_id, signal.SIGKILL)
        _gone3, stragglers = psutil.wait_procs(stragglers, timeout=grace)
    if still:
        with contextlib.suppress(OSError, ProcessLookupError):
            os.killpg(session_id or os.getpgid(pid), signal.SIGKILL)
        _gone4, still = psutil.wait_procs(still, timeout=1.0)

    survivors: set[int] = set()
    for proc in [*still, *stragglers]:
        try:
            if proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                survivors.add(proc.pid)
        except psutil.NoSuchProcess:
            continue
        except psutil.Error as exc:
            survivors.add(proc.pid)
            out["error"] = out["error"] or f"survivor not inspectable: {exc}"
    out["survivors"] = sorted(survivors)

    if parent is not None:
        with contextlib.suppress(psutil.Error, ChildProcessError):
            parent.wait(timeout=0.5)   # reap the parent if it is our child
    return out


def stop_recorded_runtime(project_root: str | Path) -> dict[str, Any]:
    """``remedy runtime stop``: classify identity FIRST, then stop what is ours.

    Rules, all of them load-bearing:

    * a corrupt or unreadable runtime.json is an infrastructure error — nothing is
      killed and nothing is deleted, because that file is the only reference to a
      process that may still be running;
    * an ``identity_unproven`` record (e.g. AccessDenied on the cmdline) keeps its
      state and kills nothing;
    * an ``identity_mismatch`` record keeps its state as a diagnostic and kills
      nothing — silently deleting it would throw away the only process reference;
    * only a definitely-gone process or a proven PID reuse is cleared automatically;
    * the killpg target is the LIVE observed process group, never the number that
      happened to be written in the file.
    """
    with lifecycle_lock(project_root):
        load = load_state_result(project_root)

        if load.kind == STATE_ABSENT:
            return {"ok": True, "stopped": False, "reason": "no runtime state",
                    "identity": DEFINITELY_GONE, "identity_ok": True,
                    "survivors": [], "state_kind": load.kind}

        if load.kind in (STATE_CORRUPT, STATE_UNREADABLE):
            return {
                "ok": False, "stopped": False, "survivors": [],
                "state_kind": load.kind,
                "identity": IDENTITY_UNPROVEN, "identity_ok": False,
                "reason": (
                    f"runtime state is {load.kind}: {load.error}. Nothing was killed "
                    f"and nothing was deleted; inspect {load.path} manually."
                ),
                "state_path": load.path,
            }

        state = load.state

        # --- ONE identity contract: supervisor first, application second ---------
        ident = classify_runtime(state, project_root)
        sup, check = ident.supervisor, ident.app
        supervisor_verified = sup.verified

        if ident.ownership == OWNER_GONE:
            clear_state(project_root)
            return {
                "ok": True, "stopped": False, "identity": check.classification,
                "identity_ok": False, "ownership": ident.ownership,
                "reason": ident.reason or check.reason, "pid": state.pid,
                "survivors": [], "state_kind": load.kind,
                "note": "recorded process is not the managed runtime; nothing killed",
            }

        if ident.ownership == OWNER_UNTRUSTED:
            # No provable owner: keep the record, kill nothing, say why. The record is
            # the only reference to whatever may still be running.
            decisive = (sup if (state.supervisor_pid and not sup.verified) else check)
            state.status = (STATUS_IDENTITY_UNPROVEN
                            if decisive.classification == IDENTITY_UNPROVEN
                            else STATUS_IDENTITY_MISMATCH)
            state.identity_reason = decisive.reason
            with contextlib.suppress(Exception):
                save_state(state)
            return {
                "ok": False, "stopped": False, "identity": decisive.classification,
                "identity_ok": False, "ownership": ident.ownership,
                "reason": decisive.reason, "pid": state.pid, "survivors": [],
                "state_kind": load.kind,
                "note": ("nothing was killed and the state was kept; resolve the "
                         "identity problem or clean up manually"),
            }

        if ident.ownership == OWNER_SUPERVISOR_MISSING:
            # The supervisor is gone, so no live relationship can prove that the
            # recorded pid is still OUR application — a reparented process has no
            # parent left to vouch for it, and every field in runtime.json is mutable.
            # Never guess: retain an explicit supervisor_missing record with the
            # survivor and identity data, and ask for manual cleanup.
            state.status = STATUS_SUPERVISOR_MISSING
            state.identity_reason = ident.reason
            state.survivors = [state.pid] if _pid_alive(state.pid) else []
            state.stop_error = ident.reason
            with contextlib.suppress(Exception):
                save_state(state)
            return {
                "ok": False, "stopped": False, "identity": check.classification,
                "identity_ok": False, "ownership": ident.ownership,
                "runtime_status": STATUS_SUPERVISOR_MISSING,
                "reason": ident.reason, "pid": state.pid,
                "survivors": list(state.survivors), "state_kind": load.kind,
                "note": ("the supervisor is gone and the application could not be "
                         f"identified; nothing was killed. Inspect pid {state.pid} "
                         f"and clean it up manually, then delete {load.path}."),
            }

        # --- controlled shutdown -------------------------------------------------
        # OWNER_SUPERVISED (a verified supervisor that really owns this app) or
        # OWNER_UNSUPERVISED (a one-shot probe runtime with no supervisor). Nothing
        # else ever reaches a signal.
        supervisor_stopped = not state.supervisor_pid
        if supervisor_verified:
            # Ask the supervisor to shut its runtime down, then wait for it to go.
            # The request carries this runtime's instance id, so a stale file from an
            # older runtime can never stop a newer one.
            req = stop_request_path(project_root)
            with contextlib.suppress(OSError):
                req.parent.mkdir(parents=True, exist_ok=True)
                _atomic_write(req, f"{state.instance_id}\n")
            deadline = time.monotonic() + STOP_REQUEST_TIMEOUT_S
            while time.monotonic() < deadline:
                if not _pid_alive(state.supervisor_pid):
                    supervisor_stopped = True
                    break
                time.sleep(0.1)
            with contextlib.suppress(OSError):
                req.unlink()
            if not supervisor_stopped:
                # It would not go quietly. Before ANY hard signal the supervisor is
                # classified AGAIN, from scratch: fifteen seconds passed while we waited,
                # and the identity we verified before that wait is a statement about the
                # past. If the original supervisor exited and its pid — or its process
                # group — was handed to somebody else, the old numbers would now point at
                # a stranger. Only a freshly verified supervisor is signalled, and only
                # through the group observed by THAT check.
                fresh = classify_supervisor(state, project_root)
                if not fresh.verified:
                    state.status = (STATUS_IDENTITY_UNPROVEN
                                    if fresh.classification == IDENTITY_UNPROVEN
                                    else STATUS_STOP_FAILED)
                    state.survivors = sorted(
                        {p for p in (state.supervisor_pid, state.pid) if _pid_alive(p)})
                    state.stop_error = (
                        f"the supervisor could not be re-verified before the hard stop "
                        f"({fresh.classification}: {fresh.reason}); nothing was "
                        f"signalled")
                    state.identity_reason = fresh.reason
                    with contextlib.suppress(Exception):
                        save_state(state)
                    return {
                        "ok": False, "stopped": False,
                        "identity": fresh.classification, "identity_ok": False,
                        "ownership": ident.ownership,
                        "reason": state.stop_error, "pid": state.pid,
                        "supervisor_stopped": False,
                        "survivors": list(state.survivors),
                        "manual_cleanup": list(state.survivors),
                        "state_kind": load.kind,
                        "note": ("the recorded supervisor identity changed while the "
                                 "stop request was pending; nothing was killed. Inspect "
                                 "the survivors and clean them up manually."),
                    }
                stop_process_tree(state.supervisor_pid, session_id=fresh.live_pgid)
                supervisor_stopped = not _pid_alive(state.supervisor_pid)

        # The application itself: signal the LIVE group we observed, never a stored
        # number, and only if it is still there. The identity is checked AGAIN here —
        # the supervisor has just exited, and this is the last moment before something
        # destructive happens.
        result = {"pid": state.pid, "session_id": check.live_pgid,
                  "terminated": [], "killed": [], "survivors": [], "error": ""}
        if _pid_alive(state.pid):
            recheck = classify_state(state, project_root, require_cwd=False)
            if recheck.verified:
                result = stop_process_tree(state.pid, session_id=recheck.live_pgid)
            else:
                result["survivors"] = [state.pid]
                result["error"] = (
                    f"the recorded application could no longer be verified before the "
                    f"stop ({recheck.classification}: {recheck.reason}); it was NOT "
                    f"signalled")

        survivors = list(result.get("survivors") or [])
        if _pid_alive(state.supervisor_pid):
            survivors.append(state.supervisor_pid)
        result["survivors"] = sorted(set(survivors))

        if result["survivors"]:
            state.status = STATUS_STOP_FAILED
            state.survivors = list(result["survivors"])
            state.stop_error = result.get("error") or (
                f"managed processes survived the stop: {result['survivors']}")
            with contextlib.suppress(Exception):
                save_state(state)
            return {
                "ok": False, "stopped": False, "identity": VERIFIED,
                "identity_ok": True, "ownership": ident.ownership,
                "pid": state.pid, "port": state.port,
                "status": STATUS_STOP_FAILED, "stop_error": state.stop_error,
                "state_kind": load.kind, "supervisor_stopped": supervisor_stopped,
                **result,
            }

        clear_state(project_root)
        return {
            "ok": True, "stopped": True, "identity": VERIFIED, "identity_ok": True,
            "ownership": ident.ownership,
            "pid": state.pid, "port": state.port, "state_kind": load.kind,
            "supervisor_stopped": supervisor_stopped or not state.supervisor_pid,
            **result,
        }


def _atomic_write(path: Path, text: str) -> None:
    """Create a private control file atomically (owner-only). Kept for callers."""
    atomic_write_text(path, text)


def _pid_alive(pid: int) -> bool:
    import psutil

    if not pid:
        return False
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
    except psutil.Error:
        return True                # cannot prove it is gone: assume it is there
