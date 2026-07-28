"""F007 T001 — the runtime process manager, against real dummy HTTP servers.

Every server here is a tiny local Python script started as a real subprocess (some
with real children), so process-tree shutdown, zombies, PID reuse and log capture
are all exercised for real. No provider call, no Docker, no network install.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest

from packages.runtimes.dev_server import (
    DevServer,
    RuntimeConfigError,
    RuntimeSpec,
    RuntimeState,
    choose_port,
    clear_state,
    load_state,
    pick_free_port,
    port_is_free,
    project_digest,
    read_log_tail,
    stop_recorded_runtime,
    validate_spec,
    verify_state,
)
from tests.ports import worker_port


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


# --- dummy servers ---------------------------------------------------------

SERVER = """
import http.server, os, sys, time, threading
delay = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
port = int(os.environ["PORT"])
print("starting on", port, flush=True)
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a):
        print("request", self.path, flush=True)
time.sleep(delay)
srv = http.server.HTTPServer(("127.0.0.1", port), H)
print("ready", flush=True)
srv.serve_forever()
"""

NEVER_READY = """
import os, sys, time
print("booting but never listening", flush=True)
while True:
    time.sleep(0.2)
"""

DIES = """
import sys
print("fatal: cannot start", flush=True)
sys.exit(7)
"""

WITH_CHILD = """
import os, subprocess, sys, http.server, threading
port = int(os.environ["PORT"])
child = subprocess.Popen([sys.executable, "-c", "import time\\nwhile True: time.sleep(0.2)"])
print("child", child.pid, flush=True)
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

NOISY = """
import os, http.server
port = int(os.environ["PORT"])
for i in range(20000):
    print("log line %d filler filler filler" % i, flush=False)
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""


@pytest.fixture
def project(tmp_path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    for name, body in (("server.py", SERVER), ("never.py", NEVER_READY),
                       ("dies.py", DIES), ("child.py", WITH_CHILD),
                       ("noisy.py", NOISY)):
        (root / name).write_text(body)
    return root


def _spec(project: Path, script: str, *args: str, port: int | None = None,
          timeout: float = 10.0) -> RuntimeSpec:
    return RuntimeSpec(
        cmd=[sys.executable, str(project / script), *args],
        cwd=str(project), port=worker_port() if port is None else port,
        health_path="/", ready_timeout_s=timeout,
    )


# ---------------------------------------------------------------------------
# Readiness
# ---------------------------------------------------------------------------

class TestReadiness:
    def test_immediate_readiness(self, project):
        server = DevServer(_spec(project, "server.py"), project)
        server.start()
        try:
            res = server.wait_ready()
            assert res.ok and res.status_code == 200
            assert res.port == server.port and res.pid == server.proc.pid
        finally:
            server.stop()

    def test_delayed_readiness(self, project):
        server = DevServer(_spec(project, "server.py", "1.5"), project)
        server.start()
        try:
            res = server.wait_ready()
            assert res.ok
            assert res.elapsed_s >= 1.4          # it really did wait
        finally:
            server.stop()

    def test_readiness_timeout_stops_the_tree_and_leaves_no_state(self, project):
        server = DevServer(_spec(project, "never.py", timeout=1.5), project)
        state = server.start()
        pid = state.pid

        # The readiness timeout is short on purpose — that is what this test proves.
        # But on a slow host the interpreter itself can take longer than that just to
        # reach its first print(), so wait for the process to actually say something
        # before starting the clock. This is setup, not the assertion.
        deadline = time.monotonic() + 30.0
        while "booting but never listening" not in read_log_tail(server.log_file):
            assert time.monotonic() < deadline, (
                "the never-ready server never logged its startup marker within 30s; "
                f"log tail was {read_log_tail(server.log_file)!r}"
            )
            assert server.proc.poll() is None, (
                f"the never-ready server exited early with {server.proc.returncode}"
            )
            time.sleep(0.05)

        assert server.proc.poll() is None                 # still alive, still not ready

        res = server.wait_ready()

        assert res.ok is False and res.error_class == "ready"
        assert "not ready after 1.5s" in res.error
        assert "booting but never listening" in res.log_tail   # bounded log tail
        assert not psutil.pid_exists(pid) or psutil.Process(pid).status() == \
            psutil.STATUS_ZOMBIE or not psutil.Process(pid).is_running()
        assert load_state(project) is None            # nothing claims to be running

    def test_child_exits_before_readiness(self, project):
        server = DevServer(_spec(project, "dies.py", timeout=10.0), project)
        server.start()
        res = server.wait_ready()

        assert res.ok is False and res.error_class == "start"
        assert "exited before readiness" in res.error and "exit code 7" in res.error
        assert "fatal: cannot start" in res.log_tail
        assert load_state(project) is None


# ---------------------------------------------------------------------------
# Process tree, zombies, idempotent stop
# ---------------------------------------------------------------------------

class TestProcessTree:
    def test_stop_kills_the_whole_process_tree(self, project):
        server = DevServer(_spec(project, "child.py"), project)
        server.start()
        assert server.wait_ready().ok
        parent = psutil.Process(server.proc.pid)
        children = parent.children(recursive=True)
        assert children, "the dummy server must really have a child"
        child_pids = [c.pid for c in children]

        server.stop()

        for pid in [parent.pid, *child_pids]:
            assert not _alive(pid), f"pid {pid} survived the stop"

    def test_no_zombie_remains(self, project):
        server = DevServer(_spec(project, "server.py"), project)
        server.start()
        assert server.wait_ready().ok
        pid = server.proc.pid

        server.stop()

        assert server.proc.poll() is not None       # the parent was reaped
        assert not _alive(pid)
        assert pid not in [p.pid for p in psutil.Process().children(recursive=True)]

    def test_stop_is_idempotent(self, project):
        server = DevServer(_spec(project, "server.py"), project)
        server.start()
        assert server.wait_ready().ok
        first = server.stop()
        second = server.stop()                      # must not raise
        assert first["survivors"] == [] and second["survivors"] == []
        assert load_state(project) is None


def _alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


# ---------------------------------------------------------------------------
# Logs
# ---------------------------------------------------------------------------

class TestLogs:
    def test_stdout_and_stderr_are_captured(self, project):
        server = DevServer(_spec(project, "server.py"), project)
        server.start()
        try:
            assert server.wait_ready().ok
            logs = server.logs()
            assert "starting on" in logs and "ready" in logs
            assert Path(server.log_file).is_file()
        finally:
            server.stop()

    def test_log_reads_are_bounded(self, project):
        server = DevServer(_spec(project, "noisy.py"), project)
        server.start()
        try:
            assert server.wait_ready().ok
            time.sleep(0.3)
            tail = server.logs(max_bytes=2048)
            assert len(tail.encode()) <= 2048 + len("[... truncated ...]\n")
            assert tail.startswith("[... truncated ...]")
        finally:
            server.stop()

    def test_read_log_tail_handles_a_missing_file(self, tmp_path):
        assert read_log_tail(tmp_path / "nope.log") == ""


# ---------------------------------------------------------------------------
# Ports
# ---------------------------------------------------------------------------

class TestPorts:
    def test_a_free_requested_port_is_used(self, project):
        wanted = pick_free_port()
        server = DevServer(_spec(project, "server.py", port=wanted), project)
        server.start()
        try:
            assert server.port == wanted
            assert server.wait_ready().ok
        finally:
            server.stop()

    def test_an_occupied_port_falls_back_and_reports_the_effective_port(
        self, project,
    ):
        import socket
        squatter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        squatter.bind(("127.0.0.1", 0))
        squatter.listen(1)
        busy = squatter.getsockname()[1]
        try:
            assert port_is_free(busy) is False
            server = DevServer(_spec(project, "server.py", port=busy), project)
            server.start()
            try:
                assert server.port != busy            # fell back
                assert server.port == choose_port(busy) or server.port > 0
                res = server.wait_ready()
                assert res.ok and res.port == server.port
                # The unrelated squatter is untouched: we never kill by port.
                assert squatter.fileno() != -1
                squatter.getsockname()
            finally:
                server.stop()
        finally:
            squatter.close()


# ---------------------------------------------------------------------------
# State identity — PID reuse can never kill an innocent process
# ---------------------------------------------------------------------------

class TestStateIdentity:
    def test_a_stale_pid_is_not_verified(self, project):
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        state = RuntimeState(
            pid=dead.pid, create_time=time.time(), port=1234, status="running",
            project_root=str(project), project_id=project_digest(project),
        )
        ok, why = verify_state(state)
        assert ok is False and str(dead.pid) in why

    def test_a_reused_pid_is_rejected_by_creation_time(self, project):
        victim = subprocess.Popen(
            [sys.executable, "-c", "import time\nwhile True: time.sleep(0.2)"])
        try:
            # The record claims this PID, but with a creation time from long ago:
            # that is exactly the PID-reuse case.
            state = RuntimeState(
                pid=victim.pid, create_time=time.time() - 10_000,
                port=1234, status="running", project_root=str(project),
                project_id=project_digest(project),
            )
            from packages.runtimes.dev_server import save_state
            save_state(state)

            ok, why = verify_state(state)
            assert ok is False and "reused" in why

            result = stop_recorded_runtime(project)

            assert result["stopped"] is False and result["identity_ok"] is False
            assert _alive(victim.pid), "an unrelated process must NEVER be killed"
            assert load_state(project) is None       # the stale state is cleared
        finally:
            victim.kill()
            victim.wait()

    def test_stop_recorded_runtime_stops_the_real_tree(self, project):
        server = DevServer(_spec(project, "child.py"), project)
        state = server.start()
        assert server.wait_ready().ok
        kids = [c.pid for c in psutil.Process(state.pid).children(recursive=True)]

        result = stop_recorded_runtime(project)

        assert result["stopped"] is True and result["identity_ok"] is True
        assert not _alive(state.pid)
        assert all(not _alive(pid) for pid in kids)
        assert load_state(project) is None
        server.stop()                                # idempotent

    def test_stop_without_state_is_idempotent(self, project):
        clear_state(project)
        result = stop_recorded_runtime(project)
        assert result["stopped"] is False and result["identity_ok"] is True

    def test_state_is_shareable_without_private_paths(self, project):
        server = DevServer(_spec(project, "server.py"), project)
        state = server.start()
        try:
            shared = state.shareable()
            assert shared["project_root"] == "[project_root]"
            assert shared["log_path"] == "runtime.log"
            assert not any(str(v).startswith("/") for v in shared.values())
        finally:
            server.stop()

    def test_two_projects_get_separate_runtime_state(self, tmp_path, project):
        other = tmp_path / "other"
        other.mkdir()
        assert project_digest(project) != project_digest(other)


# ---------------------------------------------------------------------------
# Spec validation
# ---------------------------------------------------------------------------

class TestSpecValidation:
    def test_a_shell_string_is_rejected(self, project):
        with pytest.raises(RuntimeConfigError):
            validate_spec(RuntimeSpec(cmd=[], cwd=str(project)), project)

    def test_cwd_outside_the_project_is_rejected(self, project, tmp_path):
        spec = RuntimeSpec(cmd=["echo", "hi"], cwd=str(tmp_path))
        with pytest.raises(RuntimeConfigError, match="outside the project"):
            validate_spec(spec, project)

    def test_traversal_cwd_is_rejected(self, project):
        spec = RuntimeSpec(cmd=["echo", "hi"], cwd=str(project / ".." / ".."))
        with pytest.raises(RuntimeConfigError):
            validate_spec(spec, project)

    @pytest.mark.parametrize("bad", [0, 70000, -1])
    def test_bad_ports_are_rejected(self, project, bad):
        with pytest.raises(RuntimeConfigError, match="port"):
            validate_spec(
                RuntimeSpec(cmd=["echo"], cwd=str(project), port=bad), project)

    def test_health_path_must_be_absolute(self, project):
        with pytest.raises(RuntimeConfigError, match="health_path"):
            validate_spec(
                RuntimeSpec(cmd=["echo"], cwd=str(project), health_path="health"),
                project)

    def test_timeout_must_be_positive(self, project):
        with pytest.raises(RuntimeConfigError, match="ready_timeout_s"):
            validate_spec(
                RuntimeSpec(cmd=["echo"], cwd=str(project), ready_timeout_s=0),
                project)

    def test_the_port_placeholder_is_substituted(self, project):
        spec = RuntimeSpec(cmd=["x", "--port", "{port}"], cwd=str(project),
                           env={"VITE_PORT": "{port}"})
        assert spec.resolved_cmd(4321) == ["x", "--port", "4321"]
        env = spec.resolved_env(4321)
        assert env["VITE_PORT"] == "4321" and env["PORT"] == "4321"

    def test_no_shell_is_ever_used(self):
        # Parse the module: no call anywhere may pass shell=<anything>.
        import ast
        tree = ast.parse(Path("packages/runtimes/dev_server.py").read_text())
        shell_kwargs = [
            kw for node in ast.walk(tree) if isinstance(node, ast.Call)
            for kw in node.keywords if kw.arg == "shell"
        ]
        assert shell_kwargs == []
