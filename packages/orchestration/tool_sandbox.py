"""The tool sandbox: one operating-system boundary around model-controlled execution (amend1016sb).

On 2026-10-16 a local Pi builder ran `grep -r "HYG-replaced" /` for nine minutes: Pi's working
directory had never been a boundary, and its tools ran with the operator's full rights. Since
DECISION amend1016sb D1, every Pi call and every untrusted project command (the `test` and
`dod-process` classes of `exec_guard`) runs inside Bubblewrap (`bwrap`), which builds the boundary
from kernel namespaces without root, a daemon or a container image:

- the filesystem is an empty root with the system directories (`/usr` and its merged links), a
  short list of `/etc` entries and the toolchain directories on the command's `PATH`, all
  read-only; the job workspace is the ONE writable tree; `/tmp` and `HOME` are private tmpfs.
  The operator's home, other repositories, keys and credentials do not exist inside, and a
  workspace symlink to them resolves to nothing;
- a git worktree's metadata (`<repo>/.git`) is visible read-only, so `git diff` works, and the
  workspace's own `.git` entry is mounted read-only over itself, so nothing inside can redirect
  the git commands Remedy later runs on the host;
- process, network, IPC, UTS and cgroup namespaces are private: the complete process tree,
  detached children included, dies with the call, and only the sandbox's own loopback exists;
- the environment is the caller's allowlist with `HOME` and `TMPDIR` replaced.

The model endpoint is the one network path: `ProviderRelay` (trusted, host side) listens on a
Unix socket inside a private directory bound into the sandbox, admits only the two model
requests Pi makes, and talks to the configured http endpoint; `sandbox_relay.py` carries Pi's TCP
connections inside the sandbox to that socket.

Remedy deliberately has NO unsafe mode: a missing or broken sandbox refuses the work with the
state `missing_prerequisite`, `unsupported_configuration` or `failed_self_test` and a next step,
and never falls back to an unconfined process. Linux only; macOS has no supported backend here,
and Windows runs Remedy inside WSL2 (docs/system/tool-sandbox-v1.md).
"""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

SANDBOX_READY = "ready"
SANDBOX_MISSING = "missing_prerequisite"
SANDBOX_UNSUPPORTED = "unsupported_configuration"
SANDBOX_FAILED = "failed_self_test"

#: Where the sandbox's private home and the trusted per-call directory appear inside it.
SANDBOX_HOME = "/tmp/home"
SANDBOX_RUN_DIR = "/run/remedy"
#: The port Pi reaches its model at INSIDE the sandbox; the network namespace is private, so it
#: never collides with a host service.
SANDBOX_PROVIDER_PORT = 11434

_SYSTEM_DIRS = ("/usr", "/bin", "/sbin", "/lib", "/lib32", "/lib64", "/libx32", "/nix")
#: The `/etc` entries programs need to start, resolve users and verify TLS, and nothing else.
_ETC_ENTRIES = ("passwd", "group", "hosts", "nsswitch.conf", "ld.so.cache", "ld.so.conf",
                "ld.so.conf.d", "localtime", "timezone", "ssl", "pki", "ca-certificates",
                "ca-certificates.conf", "alternatives", "gitconfig", "mime.types", "os-release",
                "protocols", "services")
#: The requests a sandboxed Pi may send to its model endpoint, and no other.
_ADMITTED_REQUESTS = frozenset({("POST", "/v1/chat/completions"), ("GET", "/v1/models")})
_DROPPED_HEADERS = frozenset({b"host", b"connection", b"keep-alive", b"proxy-connection",
                              b"proxy-authorization", b"upgrade", b"te"})
_MAX_HEAD_BYTES = 64 * 1024
_CHUNK = 65536
_PROBE_TIMEOUT_SEC = 20

INSTALL_HINT = (
    "install Bubblewrap with your package manager (Debian and Ubuntu: `sudo apt install "
    "bubblewrap`; Fedora: `sudo dnf install bubblewrap`; Arch: `sudo pacman -S bubblewrap`; "
    "openSUSE: `sudo zypper install bubblewrap`), then run `remedy doctor health`")
USERNS_HINT = (
    "this system refuses unprivileged user namespaces, which Bubblewrap needs; allow them "
    "(Debian: `sudo sysctl kernel.unprivileged_userns_clone=1`; Ubuntu 23.10 and later: the "
    "AppArmor profile for bwrap in docs/system/tool-sandbox-v1.md), then run `remedy doctor health`")
PLATFORM_HINT = (
    "Remedy isolates model-controlled tools on Linux only; on Windows run Remedy inside WSL2, and "
    "on macOS no supported sandbox exists yet, so Pi jobs are refused there")


class SandboxUnavailable(RuntimeError):
    """The sandbox cannot run here: `state` is one of the three refusal states, `hint` the next step."""

    def __init__(self, state: str, message: str, hint: str) -> None:
        super().__init__(f"{message}; {hint}")
        self.state = state
        self.message = message
        self.hint = hint


def _under(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def workspace_root_for(cwd: str) -> str:
    """The writable tree for a command started in *cwd*: its git worktree root, else *cwd* itself."""
    here = Path(cwd).resolve()
    for candidate in (here, *here.parents):
        if os.path.lexists(candidate / ".git"):
            return str(candidate)
    return str(here)


def _git_metadata_dirs(workspace: str) -> list[str]:
    """The git directories a worktree at *workspace* reads, from Remedy's own `.git` link.

    A model can write a `.git` file into a copied workspace, so the link alone proves nothing.
    Only a worktree whose git directory points BACK to this workspace (`<gitdir>/gitdir`, which
    `git worktree add` writes inside the repository, where no sandbox can write) is trusted;
    anything else exposes nothing.
    """
    link = Path(workspace) / ".git"
    if link.is_symlink() or not link.is_file():
        return []
    text = link.read_text(encoding="utf-8", errors="replace").strip()
    if not text.startswith("gitdir:"):
        return []
    gitdir = (Path(workspace) / text[len("gitdir:"):].strip()).resolve()
    back = gitdir / "gitdir"
    if not back.is_file() or Path(back.read_text(encoding="utf-8").strip()).resolve() != link.resolve():
        return []
    common = gitdir
    if (gitdir / "commondir").is_file():
        common = (gitdir / (gitdir / "commondir").read_text(encoding="utf-8").strip()).resolve()
    if not ((common / "objects").is_dir() and (common / "HEAD").exists()):
        return []
    return [str(common)] + ([] if _under(str(gitdir), str(common)) else [str(gitdir)])


def _toolchain_dirs(path_value: str, workspace: str) -> list[str]:
    """The `PATH` directories outside the system ones, each with its sibling `lib`, read-only.

    A toolchain under the home (`~/.local/bin`, `~/.nvm/.../bin`, a pyenv) keeps working; the
    home itself, its ancestors, anything inside the workspace and anything inside another git
    working tree (a repository's own `bin` or virtual environment) are never added this way.
    """
    home = os.path.realpath(os.path.expanduser("~"))
    found: list[str] = []
    prefix = os.path.realpath(sys.base_prefix)
    for entry in [*path_value.split(os.pathsep), os.path.join(prefix, "bin")]:
        # Judged BEFORE symlinks resolve: a path in the workspace is already there, and a symlink
        # in it must never lead a bind out of it.
        if not entry or not os.path.isabs(entry) or _under(os.path.normpath(entry), workspace):
            continue
        real = os.path.realpath(entry)
        candidates = [real] + ([os.path.join(os.path.dirname(real), "lib")]
                               if os.path.basename(real) == "bin" else [])
        for path in candidates:
            if (not os.path.isdir(path) or path == "/" or _under(home, path)
                    or _under(path, workspace) or any(_under(path, d) for d in _SYSTEM_DIRS)
                    or any(_under(path, d) for d in found) or _inside_git_tree(path)):
                continue
            found.append(path)
    return found


def _virtualenv_dir(value: str, workspace: str) -> str:
    """A project's virtual environment outside the workspace, or "": one with `pyvenv.cfg`, never
    a path inside the workspace (judged before symlinks resolve) and never the home or above."""
    if not value or not os.path.isabs(value) or _under(os.path.normpath(value), workspace):
        return ""
    real = os.path.realpath(value)
    home = os.path.realpath(os.path.expanduser("~"))
    if _under(home, real) or not os.path.isfile(os.path.join(real, "pyvenv.cfg")):
        return ""
    return real


def _inside_git_tree(path: str) -> bool:
    return any(os.path.lexists(os.path.join(d, ".git")) for d in (path, *map(str, Path(path).parents)))


def _remedy_code_dirs() -> list[str]:
    """Remedy's own importable code (`packages`, `apps`), read-only: a DoD check may run one of
    Remedy's modules (`python3 -m packages.orchestration.contract_hygiene`). Every Remedy root
    this interpreter imports from counts (an editable install puts its checkout on `sys.path`),
    but only these two folders of it, never the checkout around them, whose data root holds
    tokens."""
    roots = {Path(__file__).resolve().parents[2]}
    roots |= {Path(entry).resolve() for entry in sys.path
              if entry and (Path(entry) / "packages" / "orchestration" / "pingpong_job.py").is_file()}
    return [str(root / name) for root in sorted(roots) for name in ("packages", "apps")
            if (root / name).is_dir() and not any(_under(str(root), d) for d in _SYSTEM_DIRS)]


@dataclass(frozen=True)
class SandboxSpec:
    """One sandboxed command: its writable workspace and the trusted extra mounts.

    `mounts` are `(host path, sandbox path, writable)`; only Remedy's own code adds them (the
    per-call run directory of a Pi call). `setenv` overrides the inherited environment.
    """

    workspace: str
    mounts: tuple[tuple[str, str, bool], ...] = ()
    setenv: tuple[tuple[str, str], ...] = ()

    def _program_exists(self, program: str, path_value: str, cwd: str) -> bool:
        """Whether *program* will be found inside: on `PATH`, relative to *cwd*, or in a mount."""
        if "/" not in program:
            return any(os.access(os.path.join(d, program), os.X_OK)
                       for d in path_value.split(os.pathsep) if d)
        for source, target, _writable in self.mounts:
            if _under(program, target):
                program = source + program[len(target):]
        return os.path.exists(os.path.join(cwd, program))

    def wrap(self, argv: Sequence[str], env: Mapping[str, str] | None, cwd: str | None) -> list[str]:
        """The `bwrap` argument vector that runs *argv* inside this sandbox."""
        bwrap = require_sandbox()
        workspace = os.path.realpath(self.workspace)
        home = os.path.realpath(os.path.expanduser("~"))
        if workspace == "/" or _under(home, workspace) or any(_under(workspace, d) for d in _SYSTEM_DIRS):
            raise SandboxUnavailable(SANDBOX_FAILED, f"{workspace} is not a job workspace",
                                     "a sandboxed command needs the job's own working copy")
        source = env if env is not None else os.environ
        path_value = source.get("PATH", "/usr/bin:/bin")
        if not self._program_exists(argv[0], path_value, cwd or workspace):
            # The shape Popen raises for a missing program, so callers keep `tool_unavailable`.
            raise FileNotFoundError(2, "No such file or directory", argv[0])
        # A project's own virtual environment (F299 hands it over as VIRTUAL_ENV) may live in the
        # target checkout outside the worktree; it is the one such tree exposed, read-only.
        venv = _virtualenv_dir(source.get("VIRTUAL_ENV", ""), workspace)
        args = [bwrap, "--unshare-all", "--die-with-parent", "--new-session",
                "--hostname", "remedy-sandbox", "--proc", "/proc", "--dev", "/dev",
                "--tmpfs", "/tmp", "--dir", SANDBOX_HOME, "--dir", SANDBOX_RUN_DIR]
        for path in _SYSTEM_DIRS:
            if os.path.islink(path):
                args += ["--symlink", os.readlink(path), path]
            elif os.path.isdir(path):
                args += ["--ro-bind", path, path]
        for entry in _ETC_ENTRIES:
            args += ["--ro-bind-try", f"/etc/{entry}", f"/etc/{entry}"]
        toolchain = _toolchain_dirs(path_value, workspace)
        extra = [venv] if venv else []
        for path in (*toolchain, *extra, *_remedy_code_dirs(), *_git_metadata_dirs(workspace)):
            if not _under(path, workspace):
                args += ["--ro-bind", path, path]
        args += ["--bind", workspace, workspace]
        if os.path.lexists(os.path.join(workspace, ".git")) and not os.path.islink(
                os.path.join(workspace, ".git")):
            args += ["--ro-bind", os.path.join(workspace, ".git"), os.path.join(workspace, ".git")]
        for host_path, target, writable in self.mounts:
            args += ["--bind" if writable else "--ro-bind", host_path, target]
        # The environment inside is EXPLICIT: the caller's allowlisted one (a policy without an
        # allowlist gets PATH and the locale only, never the whole parent environment), with
        # the sandbox's own home and temp directory.
        inner = dict(env) if env is not None else {
            k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL") if k in os.environ}
        inner.update({"HOME": SANDBOX_HOME, "TMPDIR": "/tmp", "TMP": "/tmp", "TEMP": "/tmp"})
        user_base = os.path.join(os.path.realpath(os.path.expanduser("~")), ".local")
        if os.path.join(user_base, "lib") in toolchain:
            # Python finds its user site from HOME, which is private now; point it at the real one.
            inner.setdefault("PYTHONUSERBASE", user_base)
        inner.update(self.setenv)
        args.append("--clearenv")
        for key, value in sorted(inner.items()):
            args += ["--setenv", key, value]
        args += ["--chdir", os.path.realpath(cwd) if cwd else workspace, "--", *argv]
        return args


_READY_BWRAP: str | None = None


def require_sandbox() -> str:
    """The usable `bwrap` path, or SandboxUnavailable; a success is remembered for the process."""
    global _READY_BWRAP
    if _READY_BWRAP and os.path.exists(_READY_BWRAP):
        return _READY_BWRAP
    if not sys.platform.startswith("linux"):
        raise SandboxUnavailable(SANDBOX_UNSUPPORTED, f"no sandbox backend exists for {sys.platform}",
                                 PLATFORM_HINT)
    bwrap = shutil.which("bwrap")
    if not bwrap:
        raise SandboxUnavailable(SANDBOX_MISSING, "Bubblewrap (bwrap) is not installed", INSTALL_HINT)
    try:
        done = subprocess.run([bwrap, "--unshare-all", "--die-with-parent", "--ro-bind", "/", "/",
                               "--", "true"], capture_output=True, text=True,
                              timeout=_PROBE_TIMEOUT_SEC, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SandboxUnavailable(SANDBOX_FAILED, f"bwrap could not be started ({exc})",
                                 INSTALL_HINT) from exc
    if done.returncode != 0:
        detail = (done.stderr.strip().splitlines() or ["no diagnostic"])[-1][:200]
        raise SandboxUnavailable(SANDBOX_UNSUPPORTED, f"bwrap cannot create a sandbox: {detail}",
                                 USERNS_HINT)
    _READY_BWRAP = bwrap
    return bwrap


# ---------------------------------------------------------------------------
# The provider relay — the one network path out of a Pi sandbox (D3)
# ---------------------------------------------------------------------------

def _read_head(conn: socket.socket) -> tuple[bytes, bytes]:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(_CHUNK)
        if not chunk or len(data) + len(chunk) > _MAX_HEAD_BYTES:
            return b"", b""
        data += chunk
    head, _, rest = data.partition(b"\r\n\r\n")
    return head, rest


def admit_provider_request(head: bytes) -> tuple[str, str, list[bytes]] | None:
    """`(method, target, kept header lines)` for an admitted request head, else None.

    Admitted: `POST /v1/chat/completions` and `GET /v1/models` over HTTP/1.x, nothing else, so a
    model-controlled command cannot pull, delete or create models through the relay.
    """
    lines = head.split(b"\r\n")
    parts = lines[0].split(b" ")
    if len(parts) != 3 or parts[2] not in (b"HTTP/1.0", b"HTTP/1.1"):
        return None
    method, target = parts[0].decode("ascii", "replace"), parts[1].decode("ascii", "replace")
    if (method, target.split("?", 1)[0]) not in _ADMITTED_REQUESTS:
        return None
    kept: list[bytes] = []
    for line in lines[1:]:
        name, sep, _value = line.partition(b":")
        if not sep or not name or name != name.strip() or b"\n" in line or b"\r" in line:
            return None
        if name.lower() not in _DROPPED_HEADERS:
            kept.append(line)
    return method, target, kept


def _pump(source: socket.socket, sink: socket.socket) -> None:
    try:
        while data := source.recv(_CHUNK):
            sink.sendall(data)
    except OSError:
        pass    # one side went away; the connection ends either way
    finally:
        try:
            sink.shutdown(socket.SHUT_WR)
        except OSError:
            pass    # already closed


class ProviderRelay:
    """Trusted host side of a Pi sandbox's model connection, alive for one call.

    Every connection is one request: the relay checks its head, rewrites `Host`, forces
    `Connection: close` (so a second request cannot follow on the same connection unchecked)
    and carries the body and the answer. A refused request gets a 403 and never reaches the
    endpoint. The endpoint's address and any key stay here; the sandbox sees only the socket.
    """

    def __init__(self, upstream: str) -> None:
        parts = urlsplit(upstream)
        # Remedy deliberately relays plain http only: Ollama speaks it, and the supervisor's own
        # import closure stays free of ssl (test_serve_daemon). An https endpoint is refused here.
        if parts.scheme != "http" or not parts.hostname:
            raise ValueError(f"the model endpoint {upstream!r} is not an http:// URL; the tool "
                             "sandbox relays plain http to the configured endpoint only")
        self._host = parts.hostname
        self._port = parts.port or 80
        self._netloc = parts.netloc.rsplit("@", 1)[-1]
        self._prefix = parts.path.rstrip("/")
        self.directory = ""
        self.socket_path = ""
        self._server: socket.socket | None = None
        self._open: set[socket.socket] = set()
        self._lock = threading.Lock()

    def __enter__(self) -> ProviderRelay:
        self.directory = tempfile.mkdtemp(prefix="remedy-sandbox-")
        self.socket_path = os.path.join(self.directory, "provider.sock")
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(16)
        self._server = server
        threading.Thread(target=self._accept, daemon=True).start()
        return self

    def __exit__(self, *_exc: object) -> None:
        if self._server is not None:
            self._server.close()
        with self._lock:
            for conn in list(self._open):
                conn.close()
        shutil.rmtree(self.directory, ignore_errors=True)

    def _accept(self) -> None:
        assert self._server is not None
        while True:
            try:
                client, _ = self._server.accept()
            except OSError:
                return      # closed at the end of the call
            threading.Thread(target=self._serve, args=(client,), daemon=True).start()

    def _connect(self) -> socket.socket:
        upstream = socket.create_connection((self._host, self._port), timeout=30)
        upstream.settimeout(None)
        return upstream

    def _serve(self, client: socket.socket) -> None:
        upstream: socket.socket | None = None
        with self._lock:
            self._open.add(client)
        try:
            client.settimeout(30)
            head, rest = _read_head(client)
            admitted = admit_provider_request(head) if head else None
            if admitted is None:
                body = b"remedy: the sandbox admits only the model requests\n"
                client.sendall(b"HTTP/1.1 403 Forbidden\r\nConnection: close\r\nContent-Length: "
                               + str(len(body)).encode() + b"\r\n\r\n" + body)
                return
            method, target, headers = admitted
            client.settimeout(None)
            upstream = self._connect()
            with self._lock:
                self._open.add(upstream)
            new_head = (f"{method} {self._prefix}{target} HTTP/1.1\r\nHost: {self._netloc}\r\n"
                        .encode() + b"".join(h + b"\r\n" for h in headers)
                        + b"Connection: close\r\n\r\n")
            upstream.sendall(new_head + rest)
            forward = threading.Thread(target=_pump, args=(client, upstream), daemon=True)
            forward.start()
            _pump(upstream, client)
        except OSError:
            pass    # an endpoint or a client that went away ends this one request
        finally:
            with self._lock:
                for conn in (client, upstream):
                    if conn is not None:
                        self._open.discard(conn)
                        conn.close()


def relay_script_path() -> str:
    """The stdlib-only script that runs first inside a Pi sandbox."""
    from packages.orchestration import sandbox_relay

    return os.path.realpath(sandbox_relay.__file__)


def sandbox_python() -> str:
    """The interpreter that runs `sandbox_relay.py` inside: this one, by its real path."""
    return os.path.realpath(sys.executable)


@contextmanager
def provider_sandbox(workspace: str, upstream: str, *, files: Mapping[str, str] | None = None,
                     writable: Sequence[str] = ()) -> Iterator[tuple[SandboxSpec, list[str]]]:
    """A Pi call's sandbox: `(spec, argv prefix)`, with the relay alive until the block ends.

    *files* are written into the per-call run directory (`/run/remedy` inside, read-only) before
    the sandbox starts; a name ending in `.sh` is made executable. Each subdirectory named in
    *writable* is mounted writable (Pi keeps locks in its agent directory), while the files
    Remedy wrote into it stay read-only. The argv prefix starts `sandbox_relay.py`, which runs
    the command appended to it.
    """
    with ProviderRelay(upstream) as relay:
        # The relay script is COPIED in: a file mounted into the read-only run directory would
        # need a mount point bwrap cannot create there.
        written = {**(files or {}), "relay.py": Path(relay_script_path()).read_text(encoding="utf-8")}
        for name in writable:
            (Path(relay.directory) / name).mkdir(parents=True, exist_ok=True)
        for name, text in written.items():
            target = Path(relay.directory) / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            if name.endswith(".sh"):
                target.chmod(0o755)
        mounts = [(relay.directory, SANDBOX_RUN_DIR, False)]
        for name in writable:
            mounts.append((f"{relay.directory}/{name}", f"{SANDBOX_RUN_DIR}/{name}", True))
            mounts += [(f"{relay.directory}/{f}", f"{SANDBOX_RUN_DIR}/{f}", False)
                       for f in written if _under(f, name)]
        spec = SandboxSpec(workspace=workspace, mounts=tuple(mounts))
        yield spec, [sandbox_python(), "-I", "-S", f"{SANDBOX_RUN_DIR}/relay.py", str(SANDBOX_PROVIDER_PORT),
                     f"{SANDBOX_RUN_DIR}/provider.sock", "--"]


# ---------------------------------------------------------------------------
# The self-test `remedy doctor health` and `remedy worker doctor` run (D5)
# ---------------------------------------------------------------------------

_PROBE = r"""
import json, os, socket, sys, urllib.request
ws, secret, other, host_port = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
r = {}
def denied(fn):
    try:
        fn(); return False
    except OSError:
        return True
open(os.path.join(ws, "probe.txt"), "w").write("ok")
r["workspace_write"] = open(os.path.join(ws, "probe.txt")).read() == "ok"
r["tmp_write"] = not denied(lambda: open("/tmp/probe", "w").write("ok"))
r["secret_denied"] = denied(lambda: open(secret).read())
r["symlink_denied"] = denied(lambda: open(os.path.join(ws, "link")).read())
r["other_repo_denied"] = denied(lambda: os.listdir(other))
r["write_outside_denied"] = denied(lambda: open(os.path.join(other, "x"), "w"))
def connect():
    s = socket.create_connection(("127.0.0.1", host_port), timeout=3); s.close()
r["host_port_denied"] = denied(connect)
try:
    with urllib.request.urlopen("http://127.0.0.1:%d/v1/models" % PORT, timeout=10) as a:
        r["provider_reached"] = a.status == 200
except OSError:
    r["provider_reached"] = False
try:
    urllib.request.urlopen("http://127.0.0.1:%d/api/delete" % PORT, data=b"{}", timeout=10)
    r["provider_filtered"] = False
except OSError as e:
    r["provider_filtered"] = getattr(e, "code", 0) == 403
r["tools"] = all(os.path.exists(p) for p in ("/bin/sh", "/usr/bin/timeout"))
print(json.dumps(r))
""".replace("PORT", str(SANDBOX_PROVIDER_PORT))

_SELF_TEST_NAMES = {
    "workspace_write": "the workspace is writable", "tmp_write": "the private /tmp is writable",
    "secret_denied": "a file outside the workspace is unreadable",
    "symlink_denied": "a workspace symlink to a private file leads nowhere",
    "other_repo_denied": "another repository is invisible",
    "write_outside_denied": "nothing outside the workspace is writable",
    "host_port_denied": "a host network service is unreachable",
    "provider_reached": "the model endpoint answers through the relay",
    "provider_filtered": "the relay refuses a non-model request",
    "tools": "sh and timeout exist inside", "cancelled": "a cancelled sandbox leaves no process",
}


class _ModelsAnswer(threading.Thread):
    """A one-purpose HTTP endpoint on the host for the self-test: `GET /v1/models` answers 200."""

    def __init__(self) -> None:
        super().__init__(daemon=True)
        from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                self.send_response(200 if self.path == "/v1/models" else 404)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"{}")

            def log_message(self, *_args: object) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)

    def run(self) -> None:
        self.server.serve_forever()


def _cancel_leaves_nothing(workspace: str) -> bool:
    """A sandbox ended at its deadline takes its detached children with it."""
    from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded

    marker = f"{3000 + os.getpid() % 997}.{int(time.time()) % 89 + 10}"
    run_guarded(["/bin/sh", "-c", f"setsid sleep {marker} & sleep {marker}"], ExecGuardPolicy(
        wall_timeout_seconds=1.0, cwd=workspace, sandbox=SandboxSpec(workspace=workspace)))
    time.sleep(0.3)
    for pid in os.listdir("/proc"):
        try:
            if marker.encode() in Path(f"/proc/{pid}/cmdline").read_bytes():
                return False
        except OSError:
            continue
    return True


def sandbox_self_test() -> tuple[str, str, str]:
    """`(state, detail, hint)` from a real sandbox run on synthetic files; runs no model."""
    try:
        require_sandbox()
    except SandboxUnavailable as exc:
        return exc.state, exc.message, exc.hint
    with tempfile.TemporaryDirectory(prefix="remedy-sandbox-test-") as base, \
            socket.socket() as listener:
        ws, secret, other = (os.path.join(base, n) for n in ("ws", "secret.txt", "other"))
        os.makedirs(ws)
        os.makedirs(other)
        Path(secret).write_text("synthetic secret", encoding="utf-8")
        os.symlink(secret, os.path.join(ws, "link"))
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        answer = _ModelsAnswer()
        answer.start()
        try:
            upstream = f"http://127.0.0.1:{answer.server.server_address[1]}"
            with provider_sandbox(ws, upstream) as (spec, prefix):
                argv = spec.wrap([*prefix, sandbox_python(), "-I", "-S", "-c", _PROBE, ws, secret,
                                  other, str(listener.getsockname()[1])], None, ws)
                done = subprocess.run(argv, capture_output=True, text=True,
                                      timeout=_PROBE_TIMEOUT_SEC * 3, check=False)
            results = json.loads(done.stdout.strip().splitlines()[-1])
            results["cancelled"] = _cancel_leaves_nothing(ws)
        except (OSError, ValueError, IndexError, subprocess.SubprocessError) as exc:
            return SANDBOX_FAILED, f"the sandbox self-test could not run ({exc})", INSTALL_HINT
        finally:
            answer.server.shutdown()
            answer.server.server_close()
    failed = [_SELF_TEST_NAMES[k] for k in _SELF_TEST_NAMES if results.get(k) is not True]
    if failed:
        return (SANDBOX_FAILED, "the sandbox self-test failed: not true that " + "; ".join(failed),
                "do not run Pi jobs; report this output (docs/system/tool-sandbox-v1.md)")
    return SANDBOX_READY, f"Bubblewrap at {require_sandbox()} passed {len(_SELF_TEST_NAMES)} checks", ""
