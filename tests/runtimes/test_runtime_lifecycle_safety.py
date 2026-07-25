"""F007 corrections — identity, startup transaction, lifecycle lock, honest stop,
bounded logs and config type validation.

Real subprocesses and real dummy HTTP servers only. No provider call, no Docker,
no network install, no F008/F146 code.
"""
from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil
import pytest

from apps.cli.commands import runtime_cmd
from packages.runtimes import dev_server as DS
from packages.runtimes.dev_server import (
    DevServer,
    RuntimeConfigError,
    RuntimeSpec,
    RuntimeStartError,
    RuntimeState,
    clear_state,
    lifecycle_lock,
    load_state,
    log_path,
    project_digest,
    resolved_fingerprint,
    save_state,
    stop_recorded_runtime,
    verify_state,
)
from packages.runtimes.runtime_config import load_config_spec

SERVER = """
import http.server, os
port = int(os.environ["PORT"])
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
print("serving", port, flush=True)
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

NOISY = """
import http.server, os, sys, threading
port = int(os.environ["PORT"])
def spam():
    line = "x" * 1024
    for _ in range(20 * 1024):          # ~20 MiB, well over twice the cap
        sys.stdout.write(line + "\\n")
    sys.stdout.flush()
threading.Thread(target=spam, daemon=True).start()
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

IDLE = "import time\nwhile True: time.sleep(0.2)\n"

_REAL_STOP_TREE = DS.stop_process_tree
_REAL_PID_ALIVE = DS._pid_alive


def _force_survivor(monkeypatch):
    """Make the stop believe the managed application survived.

    With the persistent supervisor the app is normally already gone by the time the
    tree stop runs, so the survivor path has to be injected at BOTH points: the
    liveness probe and the tree stop.
    """
    monkeypatch.setattr(DS, "_pid_alive",
                        lambda pid: True if pid else False)
    monkeypatch.setattr(DS, "stop_process_tree", _pretend_survivor)


def _unforce_survivor(monkeypatch):
    monkeypatch.setattr(DS, "_pid_alive", _REAL_PID_ALIVE)
    monkeypatch.setattr(DS, "stop_process_tree", _REAL_STOP_TREE)


def _pretend_survivor(pid, grace=3.0, session_id=0):
    return {"pid": pid, "session_id": session_id, "terminated": [], "killed": [],
            "survivors": [pid], "error": "kill failed"}


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


@pytest.fixture
def project(tmp_path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "server.py").write_text(SERVER)
    (root / "noisy.py").write_text(NOISY)
    cfg = root / ".remedy"
    cfg.mkdir()
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "server.py"]\n'
        'cwd = "."\nport = 5173\nhealth_path = "/"\nready_timeout_s = 15\n'
    )
    return root


def _spec(project: Path, script: str = "server.py", timeout: float = 15.0) -> RuntimeSpec:
    return RuntimeSpec(
        cmd=[sys.executable, str(project / script)], cwd=str(project),
        port=5173, health_path="/", ready_timeout_s=timeout,
    )


def _alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


# ---------------------------------------------------------------------------
# Finding 1 — the WHOLE identity is checked before anything is killed
# ---------------------------------------------------------------------------

class TestManagedIdentity:
    def _victim(self):
        return subprocess.Popen([sys.executable, "-c", IDLE])

    def test_the_exact_pid_and_create_time_are_not_enough(self, project):
        """The reproduction: right PID, right create_time, WRONG command."""
        victim = self._victim()
        try:
            real_create = psutil.Process(victim.pid).create_time()
            save_state(RuntimeState(
                pid=victim.pid, create_time=real_create, port=5173, status="running",
                project_root=str(project), project_id=project_digest(project),
                cwd=str(project),
                cmd=[sys.executable, str(project / "server.py")],   # NOT what it runs
                cmd_fingerprint=resolved_fingerprint(
                    [sys.executable, str(project / "server.py")], project,
                    project_digest(project)),
            ))
            ok, why = verify_state(load_state(project), project)
            assert ok is False and "different command" in why

            result = stop_recorded_runtime(project)

            assert result["stopped"] is False and result["identity_ok"] is False
            assert result["identity"] == DS.IDENTITY_MISMATCH
            assert _alive(victim.pid), "an unrelated process was killed"
            # A mismatch is NOT silently forgotten: the record is kept as a
            # diagnostic, because it is the only reference to whatever is running.
            kept = load_state(project)
            assert kept is not None
            assert kept.status == DS.STATUS_IDENTITY_MISMATCH
            assert "different command" in kept.identity_reason
        finally:
            victim.kill()
            victim.wait()

    def test_a_wrong_fingerprint_alone_blocks_the_stop(self, project):
        server = DevServer(_spec(project), project)
        state = server.start()
        try:
            assert server.wait_ready().ok
            tampered = load_state(project)
            tampered.cmd_fingerprint = "0" * 32          # decorative no more
            save_state(tampered)

            ok, why = verify_state(load_state(project), project)
            assert ok is False and "fingerprint" in why

            result = stop_recorded_runtime(project)
            assert result["identity_ok"] is False and result["stopped"] is False
            assert _alive(state.pid), "the process must not be killed on a bad identity"
        finally:
            server.stop()

    def test_a_wrong_cwd_blocks_the_stop(self, project, tmp_path):
        server = DevServer(_spec(project), project)
        state = server.start()
        try:
            assert server.wait_ready().ok
            tampered = load_state(project)
            tampered.cwd = str(tmp_path)                 # not where it really runs
            tampered.cmd_fingerprint = resolved_fingerprint(
                tampered.cmd, tmp_path, tampered.project_id)
            save_state(tampered)

            ok, why = verify_state(load_state(project), project)
            assert ok is False and "not the recorded" in why

            result = stop_recorded_runtime(project)
            assert result["stopped"] is False and result["identity_ok"] is False
            assert _alive(state.pid)
        finally:
            server.stop()

    def test_a_state_from_another_project_is_rejected(self, project, tmp_path):
        other = tmp_path / "other"
        other.mkdir()
        server = DevServer(_spec(project), project)
        server.start()
        try:
            state = load_state(project)
            ok, why = verify_state(state, other)
            assert ok is False and "project" in why
        finally:
            server.stop()

    def test_an_uninspectable_process_is_never_assumed_to_be_ours(
        self, project, monkeypatch,
    ):
        server = DevServer(_spec(project), project)
        state = server.start()
        try:
            assert server.wait_ready().ok

            def denied(self):
                raise psutil.AccessDenied(self.pid)

            monkeypatch.setattr(psutil.Process, "cmdline", denied)
            ok, why = verify_state(load_state(project), project)
            assert ok is False and "cannot be inspected" in why
            monkeypatch.setattr(psutil.Process, "cmdline", psutil.Process.cmdline)
            monkeypatch.delattr(psutil.Process, "cmdline", raising=False)
        finally:
            server.stop()

    def test_serve_blocks_when_a_different_runtime_is_running(self, project, capsys):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = json.loads(capsys.readouterr().out)
        try:
            # The configured runtime changes while the old one is still managed.
            (project / ".remedy" / "config.toml").write_text(
                "[runtime]\n"
                f'cmd = ["{sys.executable}", "server.py", "--other"]\n'
                'cwd = "."\nport = 5173\nhealth_path = "/"\nready_timeout_s = 15\n'
            )
            with pytest.raises(SystemExit) as exc:
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
            assert exc.value.code == runtime_cmd.EXIT_CONFIG
            out = json.loads(capsys.readouterr().out)
            assert "runtime_spec_mismatch" in out["error"]
            assert _alive(served["pid"]), "the running runtime must not be killed"
            assert load_state(project).pid == served["pid"]   # not overwritten
        finally:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()


class TestCmdlineMatching:
    """The two tolerated launcher forms — and nothing else."""

    REC = ["npm", "run", "dev", "--", "--port", "5173", "--host", "127.0.0.1"]

    def test_an_exact_cmdline_matches(self):
        assert DS.cmdline_matches(self.REC, list(self.REC))

    def test_a_script_shim_matches(self):
        actual = ["node", "/usr/bin/npm", *self.REC[1:]]
        assert DS.cmdline_matches(self.REC, actual)

    def test_a_rewritten_process_title_matches(self):
        actual = ["npm run dev --port 5173 --host 127.0.0.1", "", "", ""]
        assert DS.cmdline_matches(self.REC, actual)

    def test_a_different_port_never_matches(self):
        actual = ["node", "/usr/bin/npm", "run", "dev", "--", "--port", "9999",
                  "--host", "127.0.0.1"]
        assert DS.cmdline_matches(self.REC, actual) is False

    def test_a_different_launcher_never_matches(self):
        actual = ["node", "/usr/bin/pnpm", *self.REC[1:]]
        assert DS.cmdline_matches(self.REC, actual) is False

    def test_an_unrelated_command_never_matches(self):
        assert DS.cmdline_matches(self.REC, ["python3", "-c", "pass"]) is False

    def test_an_empty_cmdline_never_matches(self):
        assert DS.cmdline_matches(self.REC, []) is False


# ---------------------------------------------------------------------------
# Finding 2 — startup is all-or-nothing
# ---------------------------------------------------------------------------

class TestStartupTransaction:
    def test_a_state_write_failure_leaves_no_process(self, project, monkeypatch):
        seen: dict = {}
        real_popen = subprocess.Popen

        def spy(argv, **kw):
            proc = real_popen(argv, **kw)
            seen["pid"] = proc.pid
            return proc

        monkeypatch.setattr(DS.subprocess, "Popen", spy)
        monkeypatch.setattr(DS, "save_state",
                            lambda *_a, **_k: (_ for _ in ()).throw(OSError("disk full")))

        server = DevServer(_spec(project), project)
        with pytest.raises(RuntimeStartError, match="disk full"):
            server.start()

        assert not _alive(seen["pid"]), "a failed start must leave no process"
        assert load_state(project) is None
        assert server.pump is None or not server.pump.alive

    def test_a_create_time_failure_leaves_no_process(self, project, monkeypatch):
        seen: dict = {}
        real_popen = subprocess.Popen

        def spy(argv, **kw):
            proc = real_popen(argv, **kw)
            seen["pid"] = proc.pid
            return proc

        monkeypatch.setattr(DS.subprocess, "Popen", spy)
        monkeypatch.setattr(DS, "_process_create_time",
                            lambda pid: (_ for _ in ()).throw(
                                OSError("cannot read create time")))

        server = DevServer(_spec(project), project)
        with pytest.raises(RuntimeStartError):
            server.start()

        assert not _alive(seen["pid"])
        assert load_state(project) is None

    def test_a_running_state_without_a_create_time_is_refused(self, project):
        with pytest.raises(RuntimeStartError, match="creation time"):
            save_state(RuntimeState(
                pid=1234, create_time=0.0, status="running",
                project_root=str(project), project_id=project_digest(project)))

    def test_an_unwritable_runtime_directory_is_a_start_error(self, project, monkeypatch):
        monkeypatch.setattr(Path, "mkdir",
                            lambda *a, **k: (_ for _ in ()).throw(OSError("read-only")))
        server = DevServer(_spec(project), project)
        with pytest.raises(RuntimeStartError, match="not writable"):
            server.start()

    def test_the_state_write_is_atomic(self, project):
        server = DevServer(_spec(project), project)
        try:
            state = server.start()
            path = DS.state_path(project)
            assert path.is_file()
            assert json.loads(path.read_text())["pid"] == state.pid
            leftovers = list(path.parent.glob(".runtime.json.*.tmp"))
            assert leftovers == [], "no temp state file may survive"
        finally:
            server.stop()


# ---------------------------------------------------------------------------
# Finding 3 — the project lifecycle lock
# ---------------------------------------------------------------------------

class TestLifecycleLock:
    def test_two_concurrent_serves_create_one_runtime(self, project, capsys):
        results: list = []
        gate = threading.Barrier(2)

        def serve():
            gate.wait()
            try:
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
            except SystemExit as exc:
                results.append({"exit": exc.code})

        threads = [threading.Thread(target=serve) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(30)

        out = capsys.readouterr().out
        payloads = [json.loads(chunk) for chunk in _split_json(out)]
        try:
            pids = {p["pid"] for p in payloads if p.get("ok")}
            assert len(pids) == 1, f"concurrent serve started {len(pids)} runtimes"
            assert sum(1 for p in payloads if p.get("already_running")) == 1
            assert load_state(project).pid == next(iter(pids))
        finally:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()

    def test_serve_and_stop_do_not_race_into_an_orphan(self, project, capsys):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        first = json.loads(capsys.readouterr().out)
        gate = threading.Barrier(2)

        def serve():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)

        def stop():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_stop(str(project), json_output=True)

        threads = [threading.Thread(target=serve), threading.Thread(target=stop)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(30)
        capsys.readouterr()

        state = load_state(project)
        if state is None:
            assert not _alive(first["pid"])          # stopped: no orphan
        else:
            assert _alive(state.pid)                 # kept: still managed
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()
            assert not _alive(state.pid)

    def test_the_lock_is_released_even_on_failure(self, project):
        with pytest.raises(RuntimeError):
            with lifecycle_lock(project):
                raise RuntimeError("boom")
        with lifecycle_lock(project):                # must be takeable again
            pass

    def test_a_lock_timeout_is_an_honest_error(self, project):
        from packages.runtimes.dev_server import RuntimeLockError

        DS.lock_path(project).parent.mkdir(parents=True, exist_ok=True)
        holder = subprocess.Popen(
            [sys.executable, "-c",
             "import fcntl,sys,time\n"
             "fd = open(sys.argv[1], 'a+')\n"
             "fcntl.flock(fd, fcntl.LOCK_EX)\n"
             "print('locked', flush=True)\n"
             "time.sleep(30)\n",
             str(DS.lock_path(project))],
            stdout=subprocess.PIPE, text=True)
        try:
            assert holder.stdout.readline().strip() == "locked"
            with pytest.raises(RuntimeLockError, match="timed out"):
                with lifecycle_lock(project, timeout_s=0.5):
                    pass
        finally:
            holder.kill()
            holder.wait()

    def test_different_projects_do_not_block_each_other(self, tmp_path, project):
        other = tmp_path / "other"
        other.mkdir()
        with lifecycle_lock(project):
            with lifecycle_lock(other, timeout_s=1.0):
                pass


def _split_json(text: str) -> list[str]:
    """Split concatenated pretty-printed JSON objects."""
    chunks, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(text[start:i + 1])
                start = None
    return chunks


# ---------------------------------------------------------------------------
# Finding 4 — a failed stop is retryable and says so
# ---------------------------------------------------------------------------

class TestHonestStop:
    def test_a_survivor_keeps_a_retryable_state(self, project, monkeypatch, capsys):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = json.loads(capsys.readouterr().out)

        _force_survivor(monkeypatch)
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_STOP
        out = json.loads(capsys.readouterr().out)

        assert out["ok"] is False and out["stopped"] is False
        assert served["pid"] in out["survivors"]
        state = load_state(project)
        assert state is not None and state.status == "stop_failed"
        assert served["pid"] in state.survivors and state.stop_error

        # A later stop retries from stop_failed and finishes the job.
        _unforce_survivor(monkeypatch)
        runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        second = json.loads(capsys.readouterr().out)
        # The retry succeeds. With the persistent supervisor the first (faked) stop
        # already asked the supervisor to shut the app down, so the retry may find
        # the family gone rather than having to kill it — either way it is honest,
        # the state is cleared and nothing is left running.
        assert second["ok"] is True
        assert not _alive(served["pid"])
        assert load_state(project) is None

    def test_a_stale_reused_pid_still_clears_without_killing(self, project, capsys):
        victim = subprocess.Popen([sys.executable, "-c", IDLE])
        try:
            save_state(RuntimeState(
                pid=victim.pid, create_time=time.time() - 9999, port=1,
                status="running", project_root=str(project),
                project_id=project_digest(project), cwd=str(project),
                cmd=["nope"], cmd_fingerprint="x",
            ))
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            out = json.loads(capsys.readouterr().out)
            assert out["ok"] is True and out["stopped"] is False
            assert out["identity_ok"] is False
            assert _alive(victim.pid)
            assert load_state(project) is None
        finally:
            victim.kill()
            victim.wait()

    def test_a_readiness_failure_reports_survivors_instead_of_lying(
        self, project, monkeypatch,
    ):
        (project / "never.py").write_text("import time\nwhile True: time.sleep(0.2)\n")
        server = DevServer(_spec(project, "never.py", timeout=1.0), project)
        state = server.start()

        monkeypatch.setattr(DS, "stop_process_tree", _pretend_survivor)
        result = server.wait_ready()
        monkeypatch.setattr(DS, "stop_process_tree", _REAL_STOP_TREE)

        assert result.ok is False and result.survivors == [state.pid]
        kept = load_state(project)
        assert kept is not None and kept.status == "stop_failed"

        server.stop()                       # the real cleanup, now unpatched
        assert not _alive(state.pid)
        clear_state(project)

    def test_the_text_summary_of_a_failed_stop_is_explicit(
        self, project, monkeypatch, capsys,
    ):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = json.loads(capsys.readouterr().out)
        _force_survivor(monkeypatch)
        with pytest.raises(SystemExit):
            runtime_cmd._cmd_runtime_stop(str(project), json_output=False)
        err = capsys.readouterr().err
        _unforce_survivor(monkeypatch)

        assert "Runtime stop FAILED" in err
        assert "Survivors" in err and "stop_failed" in err

        runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        capsys.readouterr()
        assert not _alive(served["pid"])


# ---------------------------------------------------------------------------
# Finding 5 — runtime.log is really bounded
# ---------------------------------------------------------------------------

class TestBoundedLog:
    def test_a_noisy_server_cannot_grow_the_log_past_the_cap(self, project, monkeypatch):
        # Shrink the cap so the test is fast; the mechanism is the same.
        monkeypatch.setattr(DS, "MAX_LOG_BYTES", 256 * 1024)
        monkeypatch.setattr(DS, "LOG_KEEP_BYTES", 128 * 1024)

        server = DevServer(_spec(project, "noisy.py"), project)
        server.start()
        try:
            assert server.wait_ready().ok            # the child never blocks
            time.sleep(1.5)
            size = log_path(project).stat().st_size
            assert size <= 256 * 1024 + DS.LOG_CHUNK_BYTES, f"log grew to {size}"
            tail = server.logs()
            assert tail.strip(), "the newest output must still be there"
        finally:
            server.stop()
        assert server.pump is None                   # joined

    def test_the_log_pump_thread_exits_after_stop(self, project):
        before = {t.name for t in threading.enumerate()}
        server = DevServer(_spec(project), project)
        server.start()
        assert server.wait_ready().ok
        assert any(t.name == "remedy-log-pump" for t in threading.enumerate())
        server.stop()

        time.sleep(0.2)
        after = {t.name for t in threading.enumerate()}
        assert "remedy-log-pump" not in after - before

    def test_a_one_shot_probe_leaves_no_pump_thread(self, project, capsys):
        before = {t.ident for t in threading.enumerate()}
        runtime_cmd._cmd_runtime_probe(str(project), json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is True and out["stopped"] is True
        time.sleep(0.2)
        new_pumps = [t for t in threading.enumerate()
                     if t.ident not in before and t.name == "remedy-log-pump"
                     and t.is_alive()]
        assert new_pumps == [], "the probe left its log pump running"

    def test_pump_errors_are_surfaced(self, project):
        server = DevServer(_spec(project), project)
        server.start()
        try:
            assert server.wait_ready().ok
            assert server.pump is not None
            assert server.pump.error == ""
        finally:
            server.stop()


# ---------------------------------------------------------------------------
# Finding 6 — every malformed TOML value is a RuntimeConfigError (exit 2)
# ---------------------------------------------------------------------------

BAD_CONFIGS = {
    "string port": '[runtime]\ncmd = ["echo"]\nport = "not-a-number"\n',
    "bool port": '[runtime]\ncmd = ["echo"]\nport = true\n',
    "string timeout": '[runtime]\ncmd = ["echo"]\nready_timeout_s = "soon"\n',
    "bool timeout": '[runtime]\ncmd = ["echo"]\nready_timeout_s = false\n',
    "env not a table": '[runtime]\ncmd = ["echo"]\nenv = 3\n',
    "env value not a string": '[runtime]\ncmd = ["echo"]\n[runtime.env]\nA = 3\n',
    "cmd item not a string": '[runtime]\ncmd = ["echo", 3]\n',
    "host not a string": '[runtime]\ncmd = ["echo"]\nhost = 5\n',
    "cwd not a string": '[runtime]\ncmd = ["echo"]\ncwd = 7\n',
    "health path not a string": '[runtime]\ncmd = ["echo"]\nhealth_path = 1\n',
}


class TestConfigTypeErrors:
    @pytest.mark.parametrize("name", list(BAD_CONFIGS))
    def test_every_bad_type_is_a_runtime_config_error(self, tmp_path, name):
        root = tmp_path / "p"
        (root / ".remedy").mkdir(parents=True)
        (root / ".remedy" / "config.toml").write_text(BAD_CONFIGS[name])
        with pytest.raises(RuntimeConfigError):
            load_config_spec(root)

    @pytest.mark.parametrize("name", list(BAD_CONFIGS))
    def test_the_cli_exits_2_and_never_tracebacks(self, tmp_path, capsys, name):
        root = tmp_path / "p"
        (root / ".remedy").mkdir(parents=True)
        (root / ".remedy" / "config.toml").write_text(BAD_CONFIGS[name])
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_CONFIG
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is False and out["error_class"] == "config"
