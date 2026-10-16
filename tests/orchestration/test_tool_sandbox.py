"""The tool sandbox against the REAL kernel boundary (DECISION amend1016sb D1 to D6).

Every test here runs Bubblewrap for real on temporary directories with synthetic secrets; nothing
mocks the sandbox invocation. Where this machine cannot run the sandbox the tests SKIP with a
reason that says so: a skipped test here is NOT a verified boundary. The two fail-closed tests at
the end replace `bwrap` on purpose and run everywhere.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import textwrap
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

import packages.orchestration.pi_provider as PP
import packages.orchestration.tool_sandbox as TS
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded, run_guarded_test_command

SECRET = "SYNTHETIC-SECRET-7f3a91"


@pytest.fixture
def sandbox_ready():
    try:
        TS.require_sandbox()
    except TS.SandboxUnavailable as exc:
        pytest.skip(f"NOT VERIFIED: the tool sandbox cannot run here ({exc.state}: {exc.message}); "
                    "a skipped isolation test is not a passed one")


@pytest.fixture
def world(tmp_path, sandbox_ready):
    """A workspace, a private file and another repository beside it, as on a real host."""
    ws, other = tmp_path / "ws", tmp_path / "other-repo"
    ws.mkdir()
    other.mkdir()
    (ws / "src.txt").write_text("inside\n")
    (other / "notes.txt").write_text(SECRET)
    (other / ".git").mkdir()
    secret = tmp_path / "id_synthetic"
    secret.write_text(SECRET)
    os.symlink(secret, ws / "link-to-secret")
    return ws, secret, other


def sh(ws: Path, script: str, timeout: float = 60, **env_extra) -> subprocess.CompletedProcess:
    """One `test`-class command in *ws*, through the production seam."""
    return run_guarded_test_command(["/bin/sh", "-c", script], timeout_sec=timeout, cwd=str(ws),
                                    extra_env=env_extra or None)


def _alive(marker: str) -> list[str]:
    found = []
    for pid in os.listdir("/proc"):
        try:
            if marker.encode() in Path(f"/proc/{pid}/cmdline").read_bytes():
                found.append(pid)
        except OSError:
            continue
    return found


# --- the workspace keeps working --------------------------------------------------------------

def test_reading_changing_creating_and_testing_inside_the_workspace_work(world):
    ws, _secret, _other = world
    done = sh(ws, "cat src.txt && echo changed >> src.txt && mkdir -p out && echo artifact > out/a.txt"
                  " && python3 -c 'import sys; sys.exit(0 if open(\"out/a.txt\").read() else 1)'"
                  " && echo built > /tmp/scratch && cat /tmp/scratch")
    assert done.returncode == 0, done.stderr
    assert b"inside" in done.stdout and b"built" in done.stdout
    assert (ws / "src.txt").read_text() == "inside\nchanged\n"
    assert (ws / "out" / "a.txt").read_text() == "artifact\n"


def test_git_reads_its_worktree_but_cannot_redirect_it(tmp_path, sandbox_ready):
    repo, wt = tmp_path / "repo", tmp_path / "repo" / ".remedy-wt" / "job"
    repo.mkdir()
    git = ["git", "-c", "user.email=t@example.com", "-c", "user.name=t"]
    subprocess.run([*git, "init", "-q", str(repo)], check=True)
    (repo / "a.txt").write_text("one\n")
    (repo / "private-in-main-checkout.txt").write_text(SECRET)
    subprocess.run([*git, "-C", str(repo), "add", "a.txt"], check=True)
    subprocess.run([*git, "-C", str(repo), "commit", "-qm", "c"], check=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", "--detach", str(wt)], check=True)
    link = (wt / ".git").read_text()
    done = sh(wt, "echo two >> a.txt; git diff --stat; cat ../../private-in-main-checkout.txt;"
                  " echo 'gitdir: /tmp/evil' > .git; rm -f .git; mkdir .git")
    assert b"a.txt" in done.stdout and SECRET.encode() not in done.stdout
    assert (wt / ".git").read_text() == link            # the link Remedy's host git follows is unchanged


# --- nothing outside the workspace exists -------------------------------------------------------

def test_a_secret_another_repository_and_a_symlink_to_a_private_file_are_unreadable(world):
    ws, secret, other = world
    done = sh(ws, f"cat {secret}; cat link-to-secret; ls {other}; cat {other}/notes.txt; ls ~; true")
    assert SECRET.encode() not in done.stdout and b"notes.txt" not in done.stdout


def test_nothing_outside_the_workspace_is_writable(world, tmp_path):
    ws, _secret, other = world
    sh(ws, f"echo x > {tmp_path}/escaped; echo x > {other}/escaped; echo x > /usr/escaped;"
           f" echo x > /etc/escaped; touch $HOME/kept-inside; true")
    assert not (tmp_path / "escaped").exists() and not (other / "escaped").exists()
    assert not Path("/usr/escaped").exists() and not Path("/etc/escaped").exists()


def test_a_recursive_search_of_the_whole_disk_finds_only_what_is_inside(world):
    """The incident's own command, accidental or not: `grep -r` from the root. The system
    directories are skipped only to keep the test fast; they are read-only and hold no secret."""
    ws, _secret, _other = world
    (ws / "control.txt").write_text(SECRET)
    done = sh(ws, f"grep -rls {SECRET} / --exclude-dir=usr --exclude-dir=proc --exclude-dir=dev; true")
    found = done.stdout.decode().split()
    assert found == [str(ws / "control.txt")]


def test_host_environment_secrets_do_not_reach_the_sandbox(world, monkeypatch):
    ws, _secret, _other = world
    for key in ("GITHUB_TOKEN", "REMEDY_API_TOKEN", "AWS_SECRET_ACCESS_KEY", "SSH_AUTH_SOCK"):
        monkeypatch.setenv(key, SECRET)
    done = sh(ws, "env; ls /run/user 2>&1; true")
    assert SECRET.encode() not in done.stdout
    assert b"HOME=/tmp/home" in done.stdout


# --- the network is private; the model endpoint is the one path -------------------------------

def test_no_host_or_external_endpoint_is_reachable(world):
    ws, _secret, _other = world
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        probe = textwrap.dedent(f"""\
            import socket
            for target in (("127.0.0.1", {port}), ("1.1.1.1", 53), ("10.0.0.1", 80)):
                try:
                    socket.create_connection(target, timeout=3).close(); print("REACHED", target)
                except OSError:
                    pass
        """)
        done = run_guarded_test_command([sys.executable, "-c", probe], timeout_sec=60, cwd=str(ws))
    assert b"REACHED" not in done.stdout and done.returncode == 0, done.stderr


class _Endpoint(BaseHTTPRequestHandler):
    seen: list[str] = []

    def _answer(self) -> None:
        _Endpoint.seen.append(f"{self.command} {self.path}")
        self.send_response(200)
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"ok")

    do_GET = do_POST = do_DELETE = _answer

    def log_message(self, *_args) -> None:
        return


def test_the_model_endpoint_is_reached_only_through_the_relay_and_only_for_model_requests(world):
    ws, _secret, _other = world
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Endpoint)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    _Endpoint.seen = []
    probe = textwrap.dedent("""\
        import urllib.request
        base = "http://127.0.0.1:11434"
        for method, path in (("GET", "/v1/models"), ("POST", "/v1/chat/completions"),
                             ("DELETE", "/api/delete"), ("POST", "/api/pull"), ("GET", "/api/tags")):
            req = urllib.request.Request(base + path, data=b"{}" if method == "POST" else None,
                                         method=method)
            try:
                print(method, path, urllib.request.urlopen(req, timeout=10).status)
            except OSError as e:
                print(method, path, getattr(e, "code", "refused"))
    """)
    try:
        with TS.provider_sandbox(str(ws), f"http://127.0.0.1:{server.server_address[1]}") as (spec, pre):
            done = run_guarded([*pre, sys.executable, "-I", "-S", "-c", probe], ExecGuardPolicy(
                wall_timeout_seconds=60, cwd=str(ws), env_allowlist=("PATH",), sandbox=spec))
    finally:
        server.shutdown()
        server.server_close()
    lines = done.stdout.decode().splitlines()
    assert lines == ["GET /v1/models 200", "POST /v1/chat/completions 200", "DELETE /api/delete 403",
                     "POST /api/pull 403", "GET /api/tags 403"], done.stderr
    assert _Endpoint.seen == ["GET /v1/models", "POST /v1/chat/completions"]


def test_the_relay_admits_only_whole_model_request_heads():
    admit = TS.admit_provider_request
    assert admit(b"POST /v1/chat/completions HTTP/1.1\r\nHost: x\r\nContent-Length: 2")[0] == "POST"
    assert admit(b"POST /v1/chat/completions HTTP/1.1\r\nHost: x")[2] == []      # Host is replaced
    assert admit(b"GET /v1/models?x=1 HTTP/1.1")[1] == "/v1/models?x=1"
    for refused in (b"POST /api/generate HTTP/1.1", b"DELETE /api/delete HTTP/1.1",
                    b"POST /v1/chat/completions HTTP/2", b"POST  /v1/chat/completions HTTP/1.1",
                    b"POST /v1/chat/completions HTTP/1.1\r\n folded: header",
                    b"POST /v1/chat/completions HTTP/1.1\r\nbad header"):
        assert admit(refused) is None


# --- deadlines, detached children and cancellation ---------------------------------------------

def test_a_detached_child_does_not_outlive_its_sandbox(world):
    ws, _secret, _other = world
    marker = f"{4000 + os.getpid() % 900}.{int(time.time()) % 89 + 10}"
    done = sh(ws, f"setsid sleep {marker} & nohup sleep {marker} >/dev/null 2>&1 & echo started")
    assert done.returncode == 0 and b"started" in done.stdout
    time.sleep(0.3)
    assert _alive(marker) == []


def test_an_endless_command_ends_at_its_deadline_with_its_whole_tree(world):
    ws, _secret, _other = world
    marker = f"{5000 + os.getpid() % 900}.{int(time.time()) % 89 + 10}"
    started = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        sh(ws, f"setsid sleep {marker} & while :; do sleep {marker}; done", timeout=1)
    assert time.monotonic() - started < 10
    time.sleep(0.3)
    assert _alive(marker) == []


def test_a_cancel_ends_the_running_sandbox_within_about_a_second(world):
    ws, _secret, _other = world
    marker = f"{6000 + os.getpid() % 900}.{int(time.time()) % 89 + 10}"
    stop_at = time.monotonic() + 0.5
    started = time.monotonic()
    done = run_guarded(["/bin/sh", "-c", f"setsid sleep {marker} & sleep {marker}"], ExecGuardPolicy(
        wall_timeout_seconds=60, cwd=str(ws), env_allowlist=("PATH",),
        sandbox=TS.SandboxSpec(str(ws)), cancel_check=lambda: time.monotonic() >= stop_at))
    assert (done.classification, done.tripped_limit) == ("cancelled", "cancelled")
    assert time.monotonic() - started < 5
    time.sleep(0.3)
    assert _alive(marker) == []


def test_the_tool_shell_ends_one_command_at_its_deadline_and_says_so(world):
    ws, _secret, _other = world
    files = {"tool-shell.sh": PP._TOOL_SHELL.format(limit=1)}
    with TS.provider_sandbox(str(ws), "http://127.0.0.1:9", files=files) as (spec, _pre):
        started = time.monotonic()
        done = run_guarded(["/run/remedy/tool-shell.sh", "-c", "echo before; sleep 30; echo after"],
                           ExecGuardPolicy(wall_timeout_seconds=60, cwd=str(ws), env_allowlist=("PATH",),
                                           sandbox=spec))
    assert done.returncode == 124 and time.monotonic() - started < 10
    assert done.stdout == b"before\n" and b"tool deadline of 1 seconds" in done.stderr


# --- fail closed --------------------------------------------------------------------------------

def _without_a_working_bwrap(tmp_path, monkeypatch, script: str | None) -> Path:
    bindir = tmp_path / "fakebin"
    bindir.mkdir()
    if script is not None:
        (bindir / "bwrap").write_text(script)
        (bindir / "bwrap").chmod(0o755)
    (bindir / "pi").write_text("#!/bin/sh\necho 9.9.9\n")     # Pi is present; only the sandbox is not
    (bindir / "pi").chmod(0o755)
    for tool in ("sh", "true", "git", "python3"):
        real = Path(f"/usr/bin/{tool}")
        if real.exists():
            (bindir / tool).symlink_to(real)
    monkeypatch.setenv("PATH", str(bindir))
    monkeypatch.setattr(TS, "_READY_BWRAP", None)
    return bindir


@pytest.mark.parametrize("script, state", [
    (None, TS.SANDBOX_MISSING),
    ("#!/bin/sh\necho 'bwrap: No permission to create new namespace' >&2\nexit 1\n", TS.SANDBOX_UNSUPPORTED),
])
def test_a_missing_or_broken_sandbox_refuses_and_runs_nothing(tmp_path, monkeypatch, script, state):
    _without_a_working_bwrap(tmp_path, monkeypatch, script)
    ws = tmp_path / "ws"
    ws.mkdir()
    with pytest.raises(TS.SandboxUnavailable) as raised:
        TS.require_sandbox()
    assert raised.value.state == state and raised.value.hint
    done = sh(ws, "touch ran-anyway")
    assert done.returncode == 126 and b"refused to run without the tool sandbox" in done.stderr
    assert not (ws / "ran-anyway").exists()
    with pytest.raises(PP.PiUnavailable, match="tool sandbox"):
        PP.pi_preflight(model=PP.PI_DEFAULT_MODEL, workspace=str(ws), role="builder", check_endpoint=False)
    reported = TS.sandbox_self_test()
    assert reported[0] == state and reported[2]


def test_the_self_test_passes_every_check_on_a_ready_machine(sandbox_ready):
    state, detail, hint = TS.sandbox_self_test()
    assert (state, hint) == (TS.SANDBOX_READY, ""), detail
    assert json.dumps(detail)


# --- the real Pi harness inside the sandbox, against a scripted model endpoint -----------------

class _ScriptedModel(BaseHTTPRequestHandler):
    """An OpenAI-compatible endpoint that asks for one bash call, then answers. No real model."""

    command_text = ""
    requests: list[dict] = []

    def do_POST(self) -> None:
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        _ScriptedModel.requests.append(body)
        if len(_ScriptedModel.requests) == 1:
            delta = {"role": "assistant", "tool_calls": [{"index": 0, "id": "call_1", "type": "function",
                     "function": {"name": "bash", "arguments": json.dumps({"command": self.command_text})}}]}
            finish = "tool_calls"
        else:
            delta, finish = {"role": "assistant", "content": "finished"}, "stop"
        chunks = [{"id": "s", "object": "chat.completion.chunk", "created": 0, "model": "scripted",
                   "choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
                  {"id": "s", "object": "chat.completion.chunk", "created": 0, "model": "scripted",
                   "choices": [{"index": 0, "delta": {}, "finish_reason": finish}],
                   "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}]
        data = b"".join(b"data: " + json.dumps(c).encode() + b"\n\n" for c in chunks) + b"data: [DONE]\n\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *_args) -> None:
        return


def test_the_real_pi_harness_works_inside_and_its_shell_commands_are_bounded(world, monkeypatch, tmp_path):
    import shutil

    if not shutil.which("pi"):
        pytest.skip("NOT VERIFIED: the real Pi harness is not installed here")
    ws, secret, _other = world
    _ScriptedModel.requests = []
    _ScriptedModel.command_text = f"echo hello > made.txt; cat {secret}; sleep 60; echo never"
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ScriptedModel)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", f"http://127.0.0.1:{server.server_address[1]}")
    monkeypatch.setenv("REMEDY_PI_TOOL_TIMEOUT_SECONDS", "3")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    started = time.monotonic()
    try:
        out = PP.PiProvider(role="builder", cwd=str(ws), model="scripted").build("work", timeout_sec=120)
    finally:
        server.shutdown()
        server.server_close()
    assert not out.error and out.raw_text == "finished"
    assert time.monotonic() - started < 40
    assert (ws / "made.txt").read_text() == "hello\n"
    tool_result = " ".join(str(m.get("content")) for m in _ScriptedModel.requests[1]["messages"]
                           if m.get("role") == "tool")
    assert "No such file" in tool_result and "tool deadline of 3 seconds" in tool_result
    assert "never" not in tool_result and SECRET not in json.dumps(_ScriptedModel.requests)


def test_a_job_stop_ends_a_running_pi_call(world, monkeypatch, tmp_path):
    from types import SimpleNamespace

    from packages.orchestration.safe_points import request_stop

    ws, _secret, _other = world
    bindir = tmp_path / "bin"
    bindir.mkdir()
    (bindir / "pi").write_text("#!/bin/sh\n[ \"$1\" = --version ] && { echo 9.9.9; exit 0; }\nsleep 60\n")
    (bindir / "pi").chmod(0o755)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job_id = "a1b2c3d4e5f60718"
    PP.bind_job_clock(SimpleNamespace(job_id=job_id, budgets=None, first_running_at=None))
    try:
        request_stop(job_id, reason="operator stop", source="cli")
        started = time.monotonic()
        out = PP.PiProvider(role="builder", cwd=str(ws)).build("x", timeout_sec=60)
    finally:
        PP._JOB_STOP_REQUESTED.set(None)
        PP._JOB_TIME_LEFT.set(None)
    assert "pi_cancelled" in out.error and time.monotonic() - started < 10



# --- the mounts cannot be steered out of the workspace (review of PR 346) ----------------------

def test_a_planted_git_link_exposes_no_other_repository(tmp_path, sandbox_ready):
    """A copied workspace has no git link of its own; one the model writes must expose nothing."""
    other, ws = tmp_path / "other", tmp_path / "ws"
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    (other / ".git" / "marker-of-the-other-repo").write_text(SECRET)
    ws.mkdir()
    (ws / ".git").write_text(f"gitdir: {other / '.git'}\n")
    done = sh(ws, f"cat {other}/.git/marker-of-the-other-repo; ls {other}/.git; true")
    assert SECRET.encode() not in done.stdout and b"HEAD" not in done.stdout


def test_the_home_or_a_parent_of_it_is_never_a_writable_workspace(tmp_path, sandbox_ready):
    for root in (os.path.expanduser("~"), "/", "/usr"):
        done = run_guarded(["/bin/sh", "-c", "touch should-not-exist"], ExecGuardPolicy(
            wall_timeout_seconds=30, cwd=str(tmp_path), env_allowlist=("PATH",),
            sandbox=TS.SandboxSpec(root)))
        assert done.returncode == 126 and done.classification == "sandbox_unavailable"
        assert b"is not a job workspace" in done.stderr
    assert not (tmp_path / "should-not-exist").exists()


def test_a_symlinked_toolchain_or_venv_in_the_workspace_leads_nowhere(world, tmp_path):
    ws, secret, _other = world
    private = tmp_path / "private-venv"
    (private / "bin").mkdir(parents=True)
    (private / "pyvenv.cfg").write_text("home = /usr/bin\n")
    (private / "bin" / "token.txt").write_text(SECRET)
    os.symlink(private, ws / ".venv")
    done = sh(ws, f"cat {private}/bin/token.txt; true",
              PATH=f"{ws}/.venv/bin:/usr/bin:/bin", VIRTUAL_ENV=f"{ws}/.venv")
    assert SECRET.encode() not in done.stdout
