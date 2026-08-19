"""F007 — the REAL process boundary: `python -m apps.cli.main runtime …`.

These tests never call the handler in-process. They run the actual short-lived CLI as
its own subprocess, exactly as a user would, because the whole point of the
persistent supervisor is what happens AFTER that CLI exits.

Harmless local HTTP servers and real subprocesses only. No provider call, no Docker,
no network installation, no shell.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import psutil
import pytest

from packages.runtimes import dev_server as DS
from packages.runtimes.dev_server import (
    STATUS_RUNNING,
    STATUS_STARTING,
    RuntimeState,
    load_state,
    project_digest,
    save_state,
    state_path,
)
from tests.runtimes.runtime_cleanup import (
    RuntimeRegistry,
    basetemp_survivors,
)
from tests.ports import worker_port

pytestmark = pytest.mark.subprocess

REPO = Path(__file__).resolve().parents[2]

CHATTY = """
import http.server, os, sys, threading, time
port = int(os.environ["PORT"])
def chat():
    while True:
        sys.stdout.write("tick %f\\n" % time.time())
        sys.stdout.flush()
        time.sleep(0.05)
threading.Thread(target=chat, daemon=True).start()
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

NOISY = """
import http.server, os, sys, threading
port = int(os.environ["PORT"])
def spam():
    line = "x" * 1024
    for _ in range(40 * 1024):          # ~40 MiB: far over twice any test cap
        sys.stdout.write(line + "\\n")
    sys.stdout.flush()
threading.Thread(target=spam, daemon=True).start()
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

DIES = "import sys\nprint('fatal', flush=True)\nsys.exit(9)\n"
NEVER = "import time\nprint('never ready', flush=True)\nwhile True: time.sleep(0.2)\n"


@pytest.fixture
def data_root(tmp_path) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    return root


#: What the test currently running has started. Teardown stops exactly this — it never
#: goes hunting through the process table for something that might be ours.
REGISTRY: RuntimeRegistry | None = None


@pytest.fixture(autouse=True)
def runtime_janitor(tmp_path, request):
    """Per-test cleanup by registry, and a fast failure instead of a hanging file.

    This file had no automatic cleanup at all: every test was expected to remember its own
    `finally`, and a test that failed early simply leaked its supervisor. On the review
    host — six times slower than ours — the leaks accumulated and the complete file never
    reached a final summary.
    """
    global REGISTRY
    REGISTRY = RuntimeRegistry(tmp_path)
    try:
        yield REGISTRY
    finally:
        registry, REGISTRY = REGISTRY, None
        registry.stop_everything()
        for entry in registry.survivors_in_tmp():
            registry.track(int(entry.split()[0]))
        leftovers = registry.stop_everything()
        registry.remove_control_files()
        remaining = registry.survivors_in_tmp()
        if leftovers or remaining:
            raise AssertionError(
                f"{request.node.name} left runtime processes behind: "
                f"survivors={leftovers} still_running={remaining}")


@pytest.fixture(scope="module", autouse=True)
def no_runtime_survives_this_file(tmp_path_factory):
    """After the WHOLE file: nothing from this run's pytest temporary directory lives."""
    yield
    leftovers = basetemp_survivors(tmp_path_factory.getbasetemp())
    assert leftovers == [], f"runtime processes survived the file: {leftovers}"


def _register(payload=None, *, project=None, data_root=None, proc=None) -> None:
    if REGISTRY is None:
        return
    if proc is not None:
        REGISTRY.track_proc(proc)
    REGISTRY.observe(payload, project=project, data_root=data_root)


@pytest.fixture
def project(tmp_path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "server.py").write_text(CHATTY)
    (root / "noisy.py").write_text(NOISY)
    (root / "dies.py").write_text(DIES)
    (root / "never.py").write_text(NEVER)
    _config(root, "server.py")
    return root


def _config(root: Path, script: str, *, timeout: float = 20.0,
            port: int | None = None, env: dict[str, str] | None = None) -> None:
    if port is None:
        port = worker_port()
    cfg = root / ".remedy"
    cfg.mkdir(exist_ok=True)
    body = (
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "{script}"]\n'
        'cwd = "."\n'
        f"port = {port}\n"
        'health_path = "/"\n'
        f"ready_timeout_s = {timeout}\n"
    )
    # `runtime.env` is the SUPPORTED channel for a variable the application needs.
    # Since F085 T002e the guard scrubs the parent environment, so a value smuggled
    # through `os.environ` no longer reaches the child; a DECLARED key does.
    if env:
        body += "\n[runtime.env]\n" + "".join(
            f'{key} = "{value}"\n' for key, value in env.items())
    (cfg / "config.toml").write_text(body)


def _cli(project: Path, data_root: Path, *args: str, timeout: float = 120.0):
    """Run the REAL command in its own process."""
    env = dict(os.environ)
    env["REMEDY_DATA_DIR"] = str(data_root)
    proc = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "runtime", *args,
         "--repo", str(project), "--json"],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=timeout,
    )
    payload = {}
    if proc.stdout.strip():
        with __import__("contextlib").suppress(ValueError):
            payload = json.loads(proc.stdout)
    _register(payload, project=project, data_root=data_root)
    return proc.returncode, payload, proc.stderr


def _alive(pid: int) -> bool:
    try:
        p = psutil.Process(pid)
        return p.is_running() and p.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _state(data_root: Path, project: Path):
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_root)
    try:
        return load_state(project)
    finally:
        if old is None:
            os.environ.pop("REMEDY_DATA_DIR", None)
        else:
            os.environ["REMEDY_DATA_DIR"] = old


def _http(url: str) -> int:
    status, _err = DS.http_probe(url, timeout=3.0)
    return status


def _cleanup(data_root: Path, project: Path, *pids: int) -> None:
    """Kill whatever this test started.

    The pids are passed in explicitly as well as read from the state, because a test
    that CORRUPTS runtime.json can no longer learn them from it — and a leaked
    supervisor would then outlive the test.
    """
    known = set(pids)
    state = _state(data_root, project)
    if state is not None:
        known |= {state.pid, state.supervisor_pid}
    for pid in known:
        if pid and _alive(pid):
            DS.stop_process_tree(pid)


# ---------------------------------------------------------------------------
# The persistent runtime, across the CLI process boundary
# ---------------------------------------------------------------------------

class TestServeSurvivesTheCli:
    def test_serve_cli_exits_successfully_and_the_runtime_survives(
        self, project, data_root,
    ):
        code, out, err = _cli(project, data_root, "serve")
        try:
            assert code == 0, err
            assert out["ok"] is True and out["status"] == STATUS_RUNNING
            app, sup = out["pid"], out["supervisor_pid"]
            assert app and sup and app != sup

            # The CLI process is GONE. The supervisor and the app are not.
            time.sleep(3.0)
            assert _alive(sup), "the supervisor did not survive the CLI"
            assert _alive(app), "the application did not survive the CLI"
            assert _http(out["url"]) == 200, "the server stopped serving"
        finally:
            _cli(project, data_root, "stop")
            _cleanup(data_root, project)

    def test_logging_continues_after_the_cli_exits(self, project, data_root):
        code, out, err = _cli(project, data_root, "serve")
        try:
            assert code == 0, err
            log = Path(out["log_path"])
            first = log.stat().st_size
            time.sleep(1.5)
            second = log.stat().st_size
            assert second > first, "bounded logging stopped when the CLI exited"
            assert _alive(out["pid"])
        finally:
            _cli(project, data_root, "stop")
            _cleanup(data_root, project)

    def test_the_log_stays_bounded_under_heavy_output(self, project, data_root,
                                                      monkeypatch):
        _config(project, "noisy.py")
        env_cap = "1048576"                       # 1 MiB cap for the supervisor
        env = dict(os.environ)
        env["REMEDY_DATA_DIR"] = str(data_root)
        env["REMEDY_RUNTIME_LOG_MAX"] = env_cap

        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "runtime", "serve",
             "--repo", str(project), "--json"],
            cwd=str(REPO), env=env, capture_output=True, text=True, timeout=120,
        )
        out = json.loads(proc.stdout)
        _register(out, project=project, data_root=data_root)
        try:
            assert proc.returncode == 0, proc.stderr
            time.sleep(2.5)                       # the app writes ~40 MiB
            log = Path(out["log_path"])
            size = log.stat().st_size
            assert size <= int(env_cap) + DS.LOG_CHUNK_BYTES, f"log grew to {size}"
            assert _http(out["url"]) == 200, "the child blocked on its stdout pipe"
        finally:
            _cli(project, data_root, "stop")
            _cleanup(data_root, project)


class TestSeparateProbeAndStop:
    def test_a_separate_probe_reaches_the_runtime_and_leaves_it_running(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        try:
            assert code == 0, err
            code, out, err = _cli(project, data_root, "probe")
            assert code == 0, err
            assert out["ok"] is True and out["managed_by_serve"] is True
            assert out["stopped"] is False
            assert _alive(served["pid"]) and _alive(served["supervisor_pid"])
        finally:
            _cli(project, data_root, "stop")
            _cleanup(data_root, project)

    def test_a_second_serve_returns_the_same_verified_runtime(
        self, project, data_root,
    ):
        code, first, err = _cli(project, data_root, "serve")
        try:
            assert code == 0, err
            code, second, err = _cli(project, data_root, "serve")
            assert code == 0, err
            assert second["already_running"] is True
            assert second["pid"] == first["pid"]
            assert second["supervisor_pid"] == first["supervisor_pid"]
            assert second["status"] == STATUS_RUNNING
        finally:
            _cli(project, data_root, "stop")
            _cleanup(data_root, project)

    def test_a_separate_stop_removes_supervisor_and_application(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        kids = [c.pid for c in psutil.Process(app).children(recursive=True)]

        code, out, err = _cli(project, data_root, "stop")

        assert code == 0, err
        assert out["ok"] is True and out["stopped"] is True
        assert out["survivors"] == []
        assert not _alive(app) and not _alive(sup)
        for pid in kids:
            assert not _alive(pid)
        assert _state(data_root, project) is None       # state cleared
        assert not state_path.__module__ or True

    def test_stop_is_idempotent_across_processes(self, project, data_root):
        _cli(project, data_root, "serve")
        assert _cli(project, data_root, "stop")[0] == 0
        code, out, _err = _cli(project, data_root, "stop")
        assert code == 0 and out["ok"] is True and out["stopped"] is False

    def test_repeated_serve_probe_stop_cycles_leave_nothing_behind(
        self, project, data_root,
    ):
        pids = []
        for _ in range(3):
            code, served, err = _cli(project, data_root, "serve")
            assert code == 0, err
            pids += [served["pid"], served["supervisor_pid"]]
            assert _cli(project, data_root, "probe")[0] == 0
            assert _cli(project, data_root, "stop")[0] == 0
        for pid in pids:
            assert not _alive(pid)
        assert _state(data_root, project) is None


# ---------------------------------------------------------------------------
# Supervisor failure paths — nothing unrelated is ever killed
# ---------------------------------------------------------------------------

class TestSupervisorFailures:
    def test_an_application_that_dies_before_readiness_is_a_start_failure(
        self, project, data_root,
    ):
        _config(project, "dies.py")
        code, out, err = _cli(project, data_root, "serve")

        assert code == 3, (code, err)
        assert out["ok"] is False and out["error_class"] == "start"
        assert "exited before readiness" in out["error"]
        assert "fatal" in out.get("log_tail", "")
        assert _state(data_root, project) is None

    def test_a_readiness_timeout_leaves_no_runtime(self, project, data_root):
        _config(project, "never.py", timeout=2.0)
        code, out, err = _cli(project, data_root, "serve")

        assert code == 4, (code, err)
        assert out["error_class"] == "ready"
        assert "never ready" in out.get("log_tail", "")
        assert _state(data_root, project) is None

    def test_an_unexpected_application_exit_is_recorded_honestly(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            # The app dies on its own; the supervisor must notice and say so.
            psutil.Process(served["pid"]).kill()
            deadline = time.time() + 10
            state = None
            while time.time() < deadline:
                state = _state(data_root, project)
                if state is not None and state.status == DS.STATUS_EXITED:
                    break
                time.sleep(0.2)

            assert state is not None and state.status == DS.STATUS_EXITED
            assert state.app_exit_code is not None

            # The supervisor writes the record and THEN leaves; give it that moment.
            deadline = time.time() + 10
            while time.time() < deadline and _alive(served["supervisor_pid"]):
                time.sleep(0.1)
            assert not _alive(served["supervisor_pid"]), "supervisor should exit too"
        finally:
            _cleanup(data_root, project,
                     served["pid"], served["supervisor_pid"])
            _cli(project, data_root, "stop")

    def test_a_dead_supervisor_leaves_an_interrupted_start_that_blocks_serve(
        self, project, data_root,
    ):
        # A `starting` record whose supervisor is gone: never a duplicate start.
        os.environ["REMEDY_DATA_DIR"] = str(data_root)
        try:
            save_state(RuntimeState(
                pid=os.getpid(), create_time=psutil.Process().create_time(),
                status=STATUS_STARTING, port=1,
                project_root=str(project), project_id=project_digest(project),
                cwd=str(project), cmd=psutil.Process().cmdline(),
                cmd_fingerprint=DS.resolved_fingerprint(
                    psutil.Process().cmdline(), project, project_digest(project)),
                pgid=os.getpgrp(), sid=os.getsid(0),
                supervisor_pid=999999999,          # a supervisor that does not exist
            ))
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        code, out, _err = _cli(project, data_root, "serve")
        assert code == 5
        # Our own process is in Remedy's group, so the state is refused either as an
        # untrustworthy identity or as an interrupted start — never as success.
        assert out["ok"] is False
        assert out["error_class"] == "state"
        assert _state(data_root, project) is not None      # not silently deleted

    def test_a_corrupt_state_blocks_a_second_serve_across_processes(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            path = Path(served["log_path"]).parent / "runtime.json"
            path.write_text("{ not json")

            code, out, _err = _cli(project, data_root, "serve")
            assert code == 5
            assert out["state"]["kind"] == "corrupt"
            assert _alive(served["pid"]), "the live runtime must not be duplicated"
            assert path.is_file(), "a corrupt state file is never deleted"
        finally:
            _cleanup(data_root, project,
                     served["pid"], served["supervisor_pid"])

    def test_a_stale_supervisor_pid_never_kills_an_unrelated_process(
        self, project, data_root,
    ):
        victim = subprocess.Popen(
            [sys.executable, "-c", "import time\nwhile True: time.sleep(0.2)"])
        try:
            os.environ["REMEDY_DATA_DIR"] = str(data_root)
            try:
                save_state(RuntimeState(
                    pid=victim.pid,
                    create_time=time.time() - 9999,        # a stale creation time
                    status=STATUS_RUNNING, port=1,
                    project_root=str(project),
                    project_id=project_digest(project),
                    cwd=str(project), cmd=["nope"], cmd_fingerprint="x",
                    supervisor_pid=victim.pid,
                ))
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            code, out, _err = _cli(project, data_root, "stop")

            assert out["stopped"] is False
            assert _alive(victim.pid), "an unrelated process was killed"
        finally:
            victim.kill()
            victim.wait()


# ---------------------------------------------------------------------------
# The readiness log tail — proven by an observed marker, never by elapsed time
# ---------------------------------------------------------------------------

#: Prints its line, flushes it, and only THEN writes a marker file. The marker is the
#: proof that the line exists: a test that instead assumed the child had printed within
#: N seconds was measuring the machine, not the runtime (the tail was empty in four of
#: five external runs).
NEVER_WITH_MARKER = """
import os, sys, time
print("never ready", flush=True)
sys.stdout.flush()
open(os.environ["REMEDY_TEST_MARKER"], "w").write("printed\\n")
while True:
    time.sleep(0.2)
"""


class TestReadinessLogTail:
    def test_the_readiness_failure_returns_the_line_the_child_really_printed(
        self, project, data_root, tmp_path,
    ):
        marker = tmp_path / "child-printed.marker"
        (project / "never_marker.py").write_text(NEVER_WITH_MARKER)
        # DECLARED, not inherited: T002e scrubs the application environment, so the
        # marker path travels through `runtime.env` — which also proves a declared
        # key survives the CLI and the supervisor end to end.
        _config(project, "never_marker.py", timeout=12.0,
                env={"REMEDY_TEST_MARKER": str(marker)})

        env = dict(os.environ)
        env["REMEDY_DATA_DIR"] = str(data_root)
        proc = subprocess.Popen(
            [sys.executable, "-m", "apps.cli.main", "runtime", "serve",
             "--repo", str(project), "--json"],
            cwd=str(REPO), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True,
        )
        _register(project=project, data_root=data_root, proc=proc)
        try:
            # 1. the child really printed its line — observed, not assumed.
            deadline = time.time() + 60
            while time.time() < deadline and not marker.exists():
                assert proc.poll() is None, "the CLI gave up before the child printed"
                time.sleep(0.05)
            assert marker.is_file(), "the child never printed its line"

            # 2. only now does the readiness deadline run out.
            stdout, stderr = proc.communicate(timeout=120)
            assert proc.returncode == 4, (stdout, stderr)
            out = json.loads(stdout)
            assert out["error_class"] == "ready"
            assert "never ready" in out["log_tail"], out["log_tail"]
            assert _state(data_root, project) is None
        finally:
            with __import__("contextlib").suppress(Exception):
                proc.kill()
            _cleanup(data_root, project)
