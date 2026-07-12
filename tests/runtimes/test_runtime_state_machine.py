"""F007 corrections — process-group identity, lifecycle state machine, complete spec
fingerprint, transactional logging, rollback survivors and typed state.

Real subprocesses, real process groups, real dummy HTTP servers. No provider call,
no Docker, no network install, no F008/F146 code.
"""
from __future__ import annotations

import json
import os
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
    DEFINITELY_GONE,
    IDENTITY_MISMATCH,
    IDENTITY_UNPROVEN,
    PID_REUSED,
    STATE_CORRUPT,
    STATE_UNREADABLE,
    STATUS_RUNNING,
    STATUS_STARTING,
    VERIFIED,
    DevServer,
    RuntimeSpec,
    RuntimeStartError,
    RuntimeState,
    classify_state,
    load_state,
    load_state_result,
    project_digest,
    resolved_fingerprint,
    save_state,
    state_path,
    stop_recorded_runtime,
)

SERVER = """
import http.server, os, sys, time
delay = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
port = int(os.environ["PORT"])
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
time.sleep(delay)
print("serving", port, flush=True)
http.server.HTTPServer(("127.0.0.1", port), H).serve_forever()
"""

IDLE = "import time\nwhile True: time.sleep(0.2)\n"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


@pytest.fixture
def project(tmp_path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "server.py").write_text(SERVER)
    _write_config(root)
    return root


def _write_config(root: Path, *, args: str = "", port: int = 5173,
                  health: str = "/", timeout: float = 15.0, host: str = "127.0.0.1",
                  env: str = "") -> None:
    cfg = root / ".remedy"
    cfg.mkdir(exist_ok=True)
    extra = f', "{args}"' if args else ""
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "server.py"{extra}]\n'
        'cwd = "."\n'
        f"port = {port}\n"
        f'health_path = "{health}"\n'
        f"ready_timeout_s = {timeout}\n"
        f'host = "{host}"\n'
        + env
    )


def _spec(project: Path, *args: str, timeout: float = 15.0) -> RuntimeSpec:
    return RuntimeSpec(
        cmd=[sys.executable, str(project / "server.py"), *args],
        cwd=str(project), port=5173, health_path="/", ready_timeout_s=timeout,
    )


def _alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _split_json(text: str) -> list[dict]:
    chunks, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(json.loads(text[start:i + 1]))
                start = None
    return chunks


# ---------------------------------------------------------------------------
# Finding 1 — the live process group and session are part of the identity
# ---------------------------------------------------------------------------

class TestProcessGroupIdentity:
    def test_a_corrupted_session_id_can_never_kill_another_group(self, project):
        """The reproduction: correct managed process, but a FOREIGN group id."""
        managed = subprocess.Popen([sys.executable, "-c", IDLE],
                                   start_new_session=True)
        unrelated = subprocess.Popen([sys.executable, "-c", IDLE],
                                     start_new_session=True)
        try:
            m_pgid = os.getpgid(managed.pid)
            u_pgid = os.getpgid(unrelated.pid)
            assert m_pgid != u_pgid

            save_state(RuntimeState(
                pid=managed.pid,
                create_time=psutil.Process(managed.pid).create_time(),
                port=1, status=STATUS_RUNNING,
                project_root=str(project), project_id=project_digest(project),
                cwd=str(Path.cwd()),
                cmd=[sys.executable, "-c", IDLE],
                cmd_fingerprint=resolved_fingerprint(
                    [sys.executable, "-c", IDLE], Path.cwd(),
                    project_digest(project)),
                session_id=u_pgid, pgid=u_pgid,          # <- the FOREIGN group
                sid=os.getsid(unrelated.pid),
            ))

            check = classify_state(load_state(project), project)
            assert check.classification == IDENTITY_MISMATCH
            assert "process group" in check.reason or "session" in check.reason

            result = stop_recorded_runtime(project)

            assert result["stopped"] is False
            assert result["identity"] == IDENTITY_MISMATCH
            assert _alive(unrelated.pid), "an unrelated process GROUP was killed"
            assert _alive(managed.pid), "nothing may be killed on a bad identity"
        finally:
            for proc in (managed, unrelated):
                proc.kill()
                proc.wait()

    def test_pgid_and_sid_are_both_recorded_and_verified(self, project):
        server = DevServer(_spec(project), project)
        state = server.start()
        try:
            assert state.pgid == os.getpgid(state.pid)
            assert state.sid == os.getsid(state.pid)
            check = classify_state(load_state(project), project)
            # `starting` is a live status: identity is verifiable straight away.
            assert check.classification == VERIFIED
            assert check.live_pgid == state.pgid and check.live_sid == state.sid
        finally:
            server.stop()

    def test_the_killpg_target_is_the_live_group_not_the_stored_number(
        self, project, monkeypatch,
    ):
        server = DevServer(_spec(project), project)
        state = server.start()
        assert server.wait_ready().ok
        server.mark_running()

        seen: dict = {}
        real = DS.stop_process_tree

        def spy(pid, grace=3.0, session_id=0):
            seen["session_id"] = session_id
            return real(pid, grace=grace, session_id=session_id)

        monkeypatch.setattr(DS, "stop_process_tree", spy)
        result = stop_recorded_runtime(project)
        monkeypatch.setattr(DS, "stop_process_tree", real)

        assert result["stopped"] is True
        assert seen["session_id"] == os.getpgid(os.getpid()) or True
        assert seen["session_id"] == state.pgid       # the LIVE, verified group
        assert not _alive(state.pid)

    def test_remedys_own_group_is_never_signalled(self, project):
        """A record naming a process in OUR group is a mismatch, not a target."""
        save_state(RuntimeState(
            pid=os.getpid(),
            create_time=psutil.Process(os.getpid()).create_time(),
            status=STATUS_RUNNING, port=1,
            project_root=str(project), project_id=project_digest(project),
            cwd=str(Path.cwd()),
            cmd=psutil.Process(os.getpid()).cmdline(),
            cmd_fingerprint=resolved_fingerprint(
                psutil.Process(os.getpid()).cmdline(), Path.cwd(),
                project_digest(project)),
            pgid=os.getpgrp(), sid=os.getsid(0),
        ))
        check = classify_state(load_state(project), project)
        assert check.classification == IDENTITY_MISMATCH
        assert "own process group" in check.reason
        result = stop_recorded_runtime(project)
        assert result["stopped"] is False


# ---------------------------------------------------------------------------
# Finding 2 — the lifecycle state machine
# ---------------------------------------------------------------------------

class TestLifecycleStateMachine:
    def test_two_simultaneous_probes_never_create_two_servers(self, project, capsys):
        seen_pids: list[int] = []
        gate = threading.Barrier(2)

        def probe():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_probe(str(project), json_output=True)

        threads = [threading.Thread(target=probe) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)

        payloads = _split_json(capsys.readouterr().out)
        assert len(payloads) == 2
        for p in payloads:
            assert p["ok"] is True and p["stopped"] is True
            seen_pids.append(p["pid"])
        # The two probes ran one after the other, each owning ONE server which it
        # then stopped: no server survives, and no state is left behind.
        for pid in seen_pids:
            assert not _alive(pid)
        assert load_state(project) is None

    def test_serve_during_a_probe_never_attaches_to_the_temporary_runtime(
        self, project, capsys,
    ):
        _write_config(project, args="1.0")          # 1s to become ready
        results: dict = {}
        gate = threading.Barrier(2)

        def probe():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_probe(str(project), json_output=True)

        def serve():
            gate.wait()
            time.sleep(0.2)                          # let the probe take the lock
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)

        threads = [threading.Thread(target=probe), threading.Thread(target=serve)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(90)

        payloads = _split_json(capsys.readouterr().out)
        results["probe"] = [p for p in payloads if "managed_by_serve" in p]
        results["serve"] = [p for p in payloads if "already_running" in p]
        assert results["probe"] and results["serve"]
        # The serve never claimed the probe's temporary server.
        assert results["serve"][0]["already_running"] is False
        state = load_state(project)
        assert state is not None and state.pid == results["serve"][0]["pid"]
        assert state.pid != results["probe"][0]["pid"]

        runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        capsys.readouterr()
        assert not _alive(results["serve"][0]["pid"])

    def test_a_second_serve_cannot_succeed_before_the_first_is_ready(
        self, project, capsys,
    ):
        _write_config(project, args="1.5")           # slow readiness
        gate = threading.Barrier(2)

        def serve():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)

        threads = [threading.Thread(target=serve) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(90)

        payloads = _split_json(capsys.readouterr().out)
        started = [p for p in payloads if p.get("ok") and not p.get("already_running")]
        already = [p for p in payloads if p.get("already_running")]
        try:
            assert len(started) == 1, "two serves started two runtimes"
            assert len(already) == 1
            # The second serve only ever saw a READY runtime: `running`, not `starting`.
            assert already[0]["status"] == STATUS_RUNNING
            assert already[0]["pid"] == started[0]["pid"]
        finally:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()

    def test_a_started_runtime_is_only_running_after_readiness(self, project):
        server = DevServer(_spec(project, "1.0"), project)
        state = server.start()
        try:
            assert state.status == STATUS_STARTING
            assert load_state(project).status == STATUS_STARTING
            assert server.wait_ready().ok
            promoted = server.mark_running()
            assert promoted.status == STATUS_RUNNING
            assert load_state(project).status == STATUS_RUNNING
        finally:
            server.stop()

    def test_probe_versus_stop_leaves_no_orphan(self, project, capsys):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = _split_json(capsys.readouterr().out)[0]
        gate = threading.Barrier(2)

        def probe():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_probe(str(project), json_output=True)

        def stop():
            gate.wait()
            with __import__("contextlib").suppress(SystemExit):
                runtime_cmd._cmd_runtime_stop(str(project), json_output=True)

        threads = [threading.Thread(target=probe), threading.Thread(target=stop)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)
        capsys.readouterr()

        state = load_state(project)
        if state is None:
            assert not _alive(served["pid"])
        else:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()
        assert not _alive(served["pid"])


# ---------------------------------------------------------------------------
# Finding 3 — the fingerprint covers the whole effective spec
# ---------------------------------------------------------------------------

class TestSpecFingerprint:
    BASE = dict(cmd=["npm", "run", "dev"], cwd=".", port=5173, health_path="/",
                ready_timeout_s=30.0, host="127.0.0.1")

    def _spec(self, project, **over):
        data = {**self.BASE, **over}
        data["cwd"] = str(project)
        return RuntimeSpec(**data)

    @pytest.mark.parametrize("field,value", [
        ("port", 6000),
        ("host", "127.0.0.2"),
        ("health_path", "/healthz"),
        ("ready_timeout_s", 45.0),
        ("cmd", ["npm", "run", "start"]),
        ("env", {"A": "1"}),
    ])
    def test_every_field_changes_the_fingerprint(self, project, field, value):
        base = self._spec(project)
        other = self._spec(project, **{field: value})
        assert base.fingerprint() != other.fingerprint(), field
        assert base.fingerprint().startswith("rspec1:")

    def test_an_identical_spec_has_a_stable_fingerprint(self, project):
        assert self._spec(project).fingerprint() == self._spec(project).fingerprint()

    @pytest.mark.parametrize("changed", [
        {"port": 6001}, {"health": "/healthz"}, {"timeout": 42.0},
        {"env": '[runtime.env]\nEXTRA = "1"\n'},
    ])
    def test_a_changed_config_blocks_a_second_serve(self, project, capsys, changed):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = _split_json(capsys.readouterr().out)[0]
        try:
            _write_config(
                project,
                port=changed.get("port", 5173),
                health=changed.get("health", "/"),
                timeout=changed.get("timeout", 15.0),
                env=changed.get("env", ""),
            )
            with pytest.raises(SystemExit) as exc:
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
            assert exc.value.code == runtime_cmd.EXIT_CONFIG
            out = _split_json(capsys.readouterr().out)[0]
            assert "runtime_spec_mismatch" in out["error"]
            assert _alive(served["pid"]), "the old runtime must stay alive"
            assert load_state(project).pid == served["pid"]
        finally:
            _write_config(project)
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            capsys.readouterr()


# ---------------------------------------------------------------------------
# Finding 4 — the log is opened transactionally, failures are observable
# ---------------------------------------------------------------------------

class TestLogTransaction:
    def test_a_real_log_open_failure_aborts_the_start(self, project, monkeypatch):
        # A genuine OS failure on the log file — not a patched LogPump.start().
        log = DS.log_path(project)
        log.parent.mkdir(parents=True, exist_ok=True)
        log.mkdir()                       # runtime.log is a DIRECTORY: open() fails

        seen: dict = {}
        real_popen = subprocess.Popen

        def spy(argv, **kw):
            proc = real_popen(argv, **kw)
            seen["pid"] = proc.pid
            return proc

        monkeypatch.setattr(DS.subprocess, "Popen", spy)

        server = DevServer(_spec(project), project)
        with pytest.raises(RuntimeStartError, match="log could not be opened"):
            server.start()

        assert "pid" not in seen, "no process may be started without a log"
        assert load_state(project) is None

    def test_a_pump_failure_after_startup_is_surfaced(self, project, monkeypatch):
        server = DevServer(_spec(project), project)
        server.start()
        try:
            assert server.wait_ready().ok
            server.pump.error = "OSError: log device disappeared"   # simulate later I/O
            result = server.probe()
            assert result.log_error == "OSError: log device disappeared"
            state = server.mark_running()
            assert state.log_error == "OSError: log device disappeared"
            assert load_state(project).log_error
        finally:
            server.stop()

    def test_the_pump_handshake_waits_for_the_thread(self, project):
        server = DevServer(_spec(project), project)
        server.start()
        try:
            assert server.pump is not None and server.pump.started.is_set()
            assert server.pump.error == ""
        finally:
            server.stop()


# ---------------------------------------------------------------------------
# Finding 5 — a rollback that cannot kill the process says so
# ---------------------------------------------------------------------------

class TestRollbackSurvivors:
    def _survivor_stop(self, monkeypatch):
        def pretend(pid, grace=3.0, session_id=0):
            return {"pid": pid, "session_id": session_id, "terminated": [],
                    "killed": [], "survivors": [pid], "error": "cannot kill"}
        monkeypatch.setattr(DS, "stop_process_tree", pretend)

    def test_a_state_write_failure_with_a_survivor_is_not_called_atomic(
        self, project, monkeypatch,
    ):
        seen: dict = {}
        real_popen = subprocess.Popen

        def spy(argv, **kw):
            proc = real_popen(argv, **kw)
            seen["pid"] = proc.pid
            return proc

        monkeypatch.setattr(DS.subprocess, "Popen", spy)
        monkeypatch.setattr(DS, "save_state",
                            lambda *_a, **_k: (_ for _ in ()).throw(OSError("disk full")))
        self._survivor_stop(monkeypatch)

        server = DevServer(_spec(project), project)
        with pytest.raises(RuntimeStartError) as exc:
            server.start()

        rollback = exc.value.rollback
        assert rollback["survivors"] == [seen["pid"]]
        assert rollback["stopped"] is False
        assert "ROLLBACK INCOMPLETE" in str(exc.value)
        assert str(seen["pid"]) in str(exc.value)

        monkeypatch.setattr(DS, "stop_process_tree", DS.stop_process_tree.__wrapped__
                            if hasattr(DS.stop_process_tree, "__wrapped__")
                            else _REAL_STOP)
        DS.stop_process_tree(seen["pid"])
        assert not _alive(seen["pid"])

    def test_a_clean_rollback_reports_no_survivors(self, project, monkeypatch):
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
        with pytest.raises(RuntimeStartError) as exc:
            server.start()

        rollback = exc.value.rollback
        assert rollback["survivors"] == [] and rollback["stopped"] is True
        assert rollback["partial_state_removed"] is True
        assert not _alive(seen["pid"])
        assert load_state(project) is None

    def test_a_failed_atomic_write_leaves_no_temp_file(self, project, monkeypatch):
        monkeypatch.setattr(DS.os, "replace",
                            lambda *_a: (_ for _ in ()).throw(OSError("no space")))
        with pytest.raises(OSError, match="no space"):
            save_state(RuntimeState(
                pid=1, create_time=1.0, status=STATUS_RUNNING,
                project_root=str(project), project_id=project_digest(project)))
        monkeypatch.undo()
        leftovers = list(DS.runtime_dir(project).glob(".runtime.json.*.tmp"))
        assert leftovers == []


_REAL_STOP = DS.stop_process_tree


# ---------------------------------------------------------------------------
# Finding 6 — typed state and identity classification
# ---------------------------------------------------------------------------

class TestTypedState:
    def test_a_corrupt_state_blocks_a_second_serve(self, project, capsys):
        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        served = _split_json(capsys.readouterr().out)[0]
        try:
            state_path(project).write_text("{ this is not json")

            load = load_state_result(project)
            assert load.kind == STATE_CORRUPT and load.ok is False

            with pytest.raises(SystemExit) as exc:
                runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
            assert exc.value.code == runtime_cmd.EXIT_STATE
            out = _split_json(capsys.readouterr().out)[0]
            assert out["ok"] is False and out["state"]["kind"] == STATE_CORRUPT

            # No second server was started, the first one is untouched, and the
            # corrupt file was NOT deleted.
            assert _alive(served["pid"])
            assert state_path(project).is_file()
        finally:
            state_path(project).unlink(missing_ok=True)
            DS.stop_process_tree(served["pid"])

    def test_a_corrupt_state_blocks_a_stop_without_deleting_it(self, project, capsys):
        state_path(project).parent.mkdir(parents=True, exist_ok=True)
        state_path(project).write_text("not json at all")
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_STATE
        out = _split_json(capsys.readouterr().out)[0]
        assert out["ok"] is False and out["state_kind"] == STATE_CORRUPT
        assert state_path(project).is_file()

    def test_an_unreadable_state_blocks_a_second_serve(self, project, capsys,
                                                      monkeypatch):
        state_path(project).parent.mkdir(parents=True, exist_ok=True)
        state_path(project).write_text("{}")

        real_read = Path.read_text
        target = state_path(project)

        def denied(self, *a, **k):
            if self == target:                    # only runtime.json is unreadable
                raise PermissionError("permission denied")
            return real_read(self, *a, **k)

        monkeypatch.setattr(Path, "read_text", denied)
        load = load_state_result(project)
        assert load.kind == STATE_UNREADABLE

        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_STATE

    def test_access_denied_retains_state_and_kills_nothing(self, project, monkeypatch,
                                                           capsys):
        server = DevServer(_spec(project), project)
        state = server.start()
        try:
            assert server.wait_ready().ok
            server.mark_running()

            def denied(self):
                raise psutil.AccessDenied(self.pid)

            monkeypatch.setattr(psutil.Process, "cmdline", denied)

            check = classify_state(load_state(project), project)
            assert check.classification == IDENTITY_UNPROVEN
            assert check.may_auto_clear is False

            with pytest.raises(SystemExit) as exc:
                runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
            assert exc.value.code == runtime_cmd.EXIT_STATE
            out = _split_json(capsys.readouterr().out)[0]
            assert out["ok"] is False and out["identity"] == IDENTITY_UNPROVEN

            monkeypatch.delattr(psutil.Process, "cmdline", raising=False)

            # The process was NOT killed, and its record was NOT deleted.
            assert _alive(state.pid)
            kept = load_state(project)
            assert kept is not None and kept.identity_reason
        finally:
            monkeypatch.delattr(psutil.Process, "cmdline", raising=False)
            server.stop()

    def test_a_definitely_gone_state_is_idempotently_cleanable(self, project, capsys):
        dead = subprocess.Popen([sys.executable, "-c", "pass"])
        dead.wait()
        save_state(RuntimeState(
            pid=dead.pid, create_time=time.time(), status=STATUS_RUNNING, port=1,
            project_root=str(project), project_id=project_digest(project)))

        check = classify_state(load_state(project), project)
        assert check.classification in (DEFINITELY_GONE, PID_REUSED)
        assert check.may_auto_clear is True

        runtime_cmd._cmd_runtime_stop(str(project), json_output=True)
        out = _split_json(capsys.readouterr().out)[0]
        assert out["ok"] is True and out["stopped"] is False
        assert load_state(project) is None

        runtime_cmd._cmd_runtime_stop(str(project), json_output=True)   # idempotent
        again = _split_json(capsys.readouterr().out)[0]
        assert again["ok"] is True

    def test_a_pid_reuse_is_classified_and_kills_nothing(self, project):
        victim = subprocess.Popen([sys.executable, "-c", IDLE])
        try:
            save_state(RuntimeState(
                pid=victim.pid, create_time=time.time() - 9999, status=STATUS_RUNNING,
                port=1, project_root=str(project),
                project_id=project_digest(project)))
            check = classify_state(load_state(project), project)
            assert check.classification == PID_REUSED

            result = stop_recorded_runtime(project)
            assert result["stopped"] is False
            assert _alive(victim.pid)
            assert load_state(project) is None      # a proven reuse may be cleared
        finally:
            victim.kill()
            victim.wait()
