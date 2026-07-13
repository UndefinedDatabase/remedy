"""F007 hardening — supervisor-first identity, portability, failure finalization.

The reviewed build required a LATER CLI process to read the detached application's
live cwd (`/proc/<pid>/cwd`). On systems where the kernel denies that, a separate
`runtime probe`/`stop` failed as `identity_unproven` (exit 5). These tests pin the
fixed behaviour: the supervisor is verified first and is the authoritative owner, an
unreadable app cwd is tolerated ONLY then, a wrong one still blocks, and nothing
unrelated is ever signalled.

Real subprocesses, harmless local HTTP servers. No provider call, no network install.
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

from apps.cli.commands import runtime_cmd
from packages.runtimes import dev_server as DS
from tests.runtimes.runtime_cleanup import (
    RuntimeRegistry,
    basetemp_survivors,
)
from packages.runtimes import runtime_supervisor as SUP
from packages.runtimes.dev_server import (
    IDENTITY_MISMATCH,
    IDENTITY_UNPROVEN,
    STATUS_RUNNING,
    VERIFIED,
    RuntimeState,
    classify_state,
    classify_supervisor,
    load_state,
    new_instance_id,
    project_digest,
    save_state,
    state_path,
)

pytestmark = pytest.mark.subprocess

REPO = Path(__file__).resolve().parents[2]

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

IDLE = "import time\nwhile True: time.sleep(0.2)\n"


@pytest.fixture
def data_root(tmp_path) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    return root


#: The registry of the test currently running. Every helper that starts a runtime records
#: what it started here, so teardown never has to go looking for it.
REGISTRY: RuntimeRegistry | None = None


@pytest.fixture(autouse=True)
def runtime_janitor(tmp_path, request):
    """Per-test cleanup by REGISTRY, not by search — and it fails fast, never hangs.

    The complete file has to reach a final summary, not only each test in isolation. The
    old janitor walked the entire process table and asked every process on the machine for
    its working directory after EVERY test; on the (much slower) review host that was
    itself a large part of the file's runtime, and one leaked supervisor per parametrised
    case did the rest. Now: stop exactly the registered process groups, reap our children,
    delete only this test's own control files, and prove — cheaply — that nothing of ours
    is left. If something IS left, the test fails with the process table instead of the
    file hanging until somebody's global timeout.
    """
    global REGISTRY
    REGISTRY = RuntimeRegistry(tmp_path)
    try:
        yield REGISTRY
    finally:
        registry, REGISTRY = REGISTRY, None
        registry.stop_everything()

        # A test that never went through a registering helper (an in-process serve, say)
        # is still this test's own: its supervisor carries `--repo <tmp>/proj` in its
        # argv, so one cheap command-line scan finds it. Stop those groups too — and only
        # those — then prove that nothing of ours is left.
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
    """Tell the current test's registry about processes a helper just created."""
    if REGISTRY is None:
        return
    if proc is not None:
        REGISTRY.track_proc(proc)
    REGISTRY.observe(payload, project=project, data_root=data_root)


@pytest.fixture
def project(tmp_path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    (root / "server.py").write_text(SERVER)
    cfg = root / ".remedy"
    cfg.mkdir()
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "server.py"]\n'
        'cwd = "."\nport = 5173\nhealth_path = "/"\nready_timeout_s = 20\n'
    )
    return root


def _cli(project: Path, data_root: Path, *args: str, timeout: float = 120.0):
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


def _with_data_root(data_root: Path, fn, *a, **kw):
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_root)
    try:
        return fn(*a, **kw)
    finally:
        if old is None:
            os.environ.pop("REMEDY_DATA_DIR", None)
        else:
            os.environ["REMEDY_DATA_DIR"] = old


def _kill(*pids: int) -> None:
    for pid in pids:
        if pid and _alive(pid):
            DS.stop_process_tree(pid)


def _deny_cwd(monkeypatch, *pids: int) -> None:
    """Make psutil refuse the live cwd of these pids — the reproduction."""
    real = psutil.Process.cwd
    targets = set(pids)

    def cwd(self):
        if self.pid in targets:
            raise psutil.AccessDenied(self.pid)
        return real(self)

    monkeypatch.setattr(psutil.Process, "cwd", cwd)


#: A REAL CLI process in which reading any process's cwd is denied — which is what the
#: external review environment does to a detached, reparented application. Injecting it
#: in the parent pytest process would prove nothing about the command that actually
#: runs; this injects it INSIDE the separate CLI process, before the command starts.
DENIED_CWD_BOOTSTRAP = """
import sys
import psutil

def _denied(self):
    raise psutil.AccessDenied(self.pid)

psutil.Process.cwd = _denied
sys.argv = {argv!r}
from apps.cli.main import main
main()
"""


def _cli_denied_cwd(project: Path, data_root: Path, *args: str,
                    timeout: float = 120.0):
    """Run the real CLI in a process that cannot inspect ANY process's cwd."""
    env = dict(os.environ)
    env["REMEDY_DATA_DIR"] = str(data_root)
    argv = ["remedy", "runtime", *args, "--repo", str(project), "--json"]
    proc = subprocess.run(
        [sys.executable, "-c", DENIED_CWD_BOOTSTRAP.format(argv=argv)],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=timeout,
    )
    payload = {}
    if proc.stdout.strip():
        with __import__("contextlib").suppress(ValueError):
            payload = json.loads(proc.stdout)
    _register(payload, project=project, data_root=data_root)
    return proc.returncode, payload, proc.stderr


# ---------------------------------------------------------------------------
# Finding 1 — a denied app cwd must not break probe/stop
# ---------------------------------------------------------------------------

class TestDeniedCwdPortability:
    def test_a_probe_succeeds_through_the_verified_supervisor(
        self, project, data_root, monkeypatch,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            _deny_cwd(monkeypatch, served["pid"], served["supervisor_pid"])
            state = _with_data_root(data_root, load_state, project)

            sup = _with_data_root(data_root, classify_supervisor, state, project)
            assert sup.classification == VERIFIED, sup.reason
            app = _with_data_root(
                data_root, classify_state, state, project, require_cwd=False)
            assert app.classification == VERIFIED, app.reason

            # The strict in-process path still refuses — it is the supervisor-first
            # path that is allowed to tolerate an unreadable cwd.
            strict = _with_data_root(data_root, classify_state, state, project)
            assert strict.classification == IDENTITY_UNPROVEN
        finally:
            monkeypatch.undo()
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_a_wrong_readable_cwd_is_still_a_mismatch(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            state.cwd = str(Path.cwd())              # not where the app really runs
            _with_data_root(data_root, save_state, state)
            check = _with_data_root(
                data_root, classify_state, state, project, require_cwd=False)
            assert check.classification == IDENTITY_MISMATCH
        finally:
            _kill(served["pid"], served["supervisor_pid"])

    def test_a_wrong_instance_id_blocks_the_supervisor(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            assert state.instance_id and len(state.instance_id) == 32
            state.instance_id = new_instance_id()     # not the one in the live argv
            _with_data_root(data_root, save_state, state)

            sup = _with_data_root(data_root, classify_supervisor, state, project)
            assert sup.classification == IDENTITY_MISMATCH
            assert "instance id" in sup.reason

            code, out, _err = _cli(project, data_root, "stop")
            assert code == 5 and out["stopped"] is False
            assert _alive(served["supervisor_pid"]), "nothing may be killed on mismatch"
        finally:
            _kill(served["pid"], served["supervisor_pid"])

    @pytest.mark.parametrize("field,value", [
        ("supervisor_pid", 999999999),
        ("supervisor_create_time", 1.0),
        ("supervisor_cmd", ["python3", "-c", "pass"]),
        ("supervisor_pgid", 1),
        ("supervisor_sid", 1),
    ])
    def test_a_wrong_supervisor_identity_component_blocks(
        self, project, data_root, field, value,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            setattr(state, field, value)
            _with_data_root(data_root, save_state, state)
            sup = _with_data_root(data_root, classify_supervisor, state, project)
            assert sup.classification != VERIFIED, field
            assert _alive(served["supervisor_pid"])
        finally:
            _kill(served["pid"], served["supervisor_pid"])


# ---------------------------------------------------------------------------
# Finding 2 — probe must not call a supervisorless runtime healthy
# ---------------------------------------------------------------------------

class TestProbeChecksTheSupervisor:
    """A dead supervisor means: never healthy, and never a guess about ownership.

    Once the supervisor is gone the application has been reparented, so no live
    relationship can prove it is still ours — and every field in runtime.json is
    mutable, so the record cannot prove it either. Automatic orphan cleanup would have
    to guess, and a wrong guess kills a stranger. It is retained instead.
    """

    def test_a_dead_supervisor_is_never_reported_healthy(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            psutil.Process(sup).kill()               # the owner disappears
            psutil.Process(sup).wait(timeout=5)
            assert _alive(app), "the app outlives its supervisor for this test"

            code, out, _err = _cli(project, data_root, "probe")

            assert code == 5, out
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert out["survivors"] == [app]
            assert out["manual_cleanup"] == [app]
            assert _alive(app), "ownership was unprovable; nothing may be killed"
            state = _with_data_root(data_root, load_state, project)
            assert state is not None
            assert state.status == DS.STATUS_SUPERVISOR_MISSING
            assert state.survivors == [app]
        finally:
            _kill(app, sup)

    def test_a_dead_supervisor_is_never_healthy_when_the_app_cwd_is_denied(
        self, project, data_root,
    ):
        """The external reproduction: the orphan's cwd cannot be read at all."""
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            psutil.Process(sup).kill()
            psutil.Process(sup).wait(timeout=5)
            assert _alive(app)

            code, out, err = _cli_denied_cwd(project, data_root, "probe")

            assert code == 5, (out, err)
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING, out
            assert _alive(app)
            kept = _with_data_root(data_root, load_state, project)
            assert kept is not None
            assert kept.status == DS.STATUS_SUPERVISOR_MISSING
        finally:
            _kill(app, sup)

    def test_stop_never_kills_an_unprovable_orphan(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            psutil.Process(sup).kill()
            psutil.Process(sup).wait(timeout=5)

            code, out, err = _cli_denied_cwd(project, data_root, "stop")

            assert code == 5, (out, err)
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert out["survivors"] == [app]
            assert _alive(app), "stop guessed at an orphan's ownership"
            assert "manually" in out["note"]
            kept = _with_data_root(data_root, load_state, project)
            assert kept is not None and kept.status == DS.STATUS_SUPERVISOR_MISSING

            # Once the operator has cleaned it up, the record clears normally.
            DS.stop_process_tree(app)
            code, out, err = _cli(project, data_root, "stop")
            assert code == 0, (out, err)
            assert _with_data_root(data_root, load_state, project) is None
        finally:
            _kill(app, sup)


# ---------------------------------------------------------------------------
# Finding 1 — the recorded app must really BELONG to the supervisor
# ---------------------------------------------------------------------------

class TestLiveApplicationOwnership:
    """Two records that match on their own prove nothing about each other.

    An unrelated process with the SAME argv in the SAME directory satisfies every field
    of the application record. If a manipulated runtime.json can point a verified
    supervisor at it, a stop falls on a stranger. Ownership therefore has to be a fact
    of the live process table: the recorded application is a descendant of the verified
    supervisor and leads its own process group.
    """

    def _victim(self, project: Path, port: int, *, own_group: bool):
        """A harmless HTTP server with the runtime's exact argv and cwd."""
        env = dict(os.environ, PORT=str(port))
        return subprocess.Popen(
            [sys.executable, "server.py"], cwd=str(project), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=own_group,      # its own group, or the test's group
        )

    def _redirect_state_to(self, data_root, project, victim_pid: int):
        """Point ONLY the application fields at the victim; the supervisor stays real."""
        state = _with_data_root(data_root, load_state, project)
        proc = psutil.Process(victim_pid)
        state.pid = victim_pid
        state.create_time = proc.create_time()
        with __import__("contextlib").suppress(OSError):
            state.pgid = os.getpgid(victim_pid)
            state.sid = os.getsid(victim_pid)
            state.session_id = state.pgid
        _with_data_root(data_root, save_state, state)
        return state

    def test_a_matching_but_unrelated_process_is_never_the_supervised_app(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        victim = self._victim(project, served["port"] + 1, own_group=True)
        try:
            state = self._redirect_state_to(data_root, project, victim.pid)

            ident = _with_data_root(data_root, DS.classify_runtime, state, project)
            assert ident.ownership == DS.OWNER_UNTRUSTED, ident.to_json()
            assert ident.supervisor.verified, "the supervisor really is ours"
            assert "descendant" in ident.reason

            # ...and no command acts on it.
            code, out, err = _cli(project, data_root, "probe")
            assert code == 5, (out, err)
            assert out.get("ok") is not True

            code, out, err = _cli(project, data_root, "stop")
            assert code == 5, (out, err)
            assert out["stopped"] is False
            assert victim.poll() is None, "an unrelated process was killed"
            assert _alive(served["pid"]), "the real app was killed via a forged record"
            assert _alive(served["supervisor_pid"])

            kept = _with_data_root(data_root, load_state, project)
            assert kept is not None                  # the diagnostic is retained
            assert kept.identity_reason
        finally:
            victim.kill()
            victim.wait(timeout=5)
            _kill(served["pid"], served["supervisor_pid"])

    def test_a_victim_in_the_tests_own_process_group_is_never_signalled(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        victim = self._victim(project, served["port"] + 2, own_group=False)
        try:
            state = self._redirect_state_to(data_root, project, victim.pid)

            ident = _with_data_root(data_root, DS.classify_runtime, state, project)
            assert ident.ownership != DS.OWNER_SUPERVISED

            code, out, err = _cli(project, data_root, "stop")
            assert code == 5
            assert victim.poll() is None
            assert _alive(served["pid"])
        finally:
            victim.kill()
            victim.wait(timeout=5)
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_a_sibling_of_the_supervisor_is_not_owned_by_it(self, project, data_root):
        """A victim started by the TEST, not by the supervisor: same argv, same cwd,
        own session — a sibling, not a descendant."""
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        victim = self._victim(project, served["port"] + 3, own_group=True)
        try:
            state = self._redirect_state_to(data_root, project, victim.pid)
            sup = _with_data_root(data_root, classify_supervisor, state, project)
            owned = _with_data_root(data_root, DS.supervisor_owns_app, state, sup)

            assert sup.verified
            assert owned.classification == IDENTITY_MISMATCH
            assert psutil.Process(victim.pid).ppid() != state.supervisor_pid
            assert victim.poll() is None
        finally:
            victim.kill()
            victim.wait(timeout=5)
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_the_real_supervised_app_is_a_child_of_its_supervisor(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            ident = _with_data_root(data_root, DS.classify_runtime, state, project)

            assert ident.ownership == DS.OWNER_SUPERVISED
            assert psutil.Process(state.pid).ppid() == state.supervisor_pid
            assert os.getpgid(state.pid) == state.pid, "the app leads its own group"

            # ...and the supervisor may still stop its own real application.
            code, out, err = _cli(project, data_root, "stop")
            assert code == 0, (out, err)
            assert out["stopped"] is True and out["survivors"] == []
            assert not _alive(served["pid"]) and not _alive(served["supervisor_pid"])
        finally:
            _kill(served["pid"], served["supervisor_pid"])


# ---------------------------------------------------------------------------
# Finding 1 — serve shares the supervisor-first contract
# ---------------------------------------------------------------------------

class TestServeIsSupervisorFirst:
    def test_a_second_serve_succeeds_when_the_app_cwd_cannot_be_read(
        self, project, data_root,
    ):
        """serve CLI A → A exits → serve CLI B → 0, already_running, same pids."""
        code, first, err = _cli_denied_cwd(project, data_root, "serve")
        assert code == 0, err
        try:
            code, second, err = _cli_denied_cwd(project, data_root, "serve")

            assert code == 0, (second, err)
            assert second["already_running"] is True
            assert second["pid"] == first["pid"]
            assert second["supervisor_pid"] == first["supervisor_pid"]
            assert second["status"] == STATUS_RUNNING
            assert second["ownership"] == DS.OWNER_SUPERVISED
            assert _alive(first["pid"]) and _alive(first["supervisor_pid"])
        finally:
            _cli(project, data_root, "stop")
            _kill(first["pid"], first["supervisor_pid"])

    def test_a_denied_cwd_probe_and_stop_work_across_processes(
        self, project, data_root,
    ):
        code, served, err = _cli_denied_cwd(project, data_root, "serve")
        assert code == 0, err
        try:
            code, out, err = _cli_denied_cwd(project, data_root, "probe")
            assert code == 0, (out, err)
            assert out["ok"] is True and out["managed_by_serve"] is True

            code, out, err = _cli_denied_cwd(project, data_root, "stop")
            assert code == 0, (out, err)
            assert out["stopped"] is True and out["survivors"] == []
            assert not _alive(served["pid"])
            assert not _alive(served["supervisor_pid"])
        finally:
            _kill(served["pid"], served["supervisor_pid"])

    def test_an_unverified_supervisor_never_yields_already_running(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            state.instance_id = new_instance_id()     # not the live supervisor's
            _with_data_root(data_root, save_state, state)

            code, out, err = _cli_denied_cwd(project, data_root, "serve")

            assert code == 5, (out, err)
            assert out["ok"] is False
            assert out["error_class"] == "state"
            assert _alive(served["pid"]), "no duplicate, and nothing killed"
            assert _alive(served["supervisor_pid"])
        finally:
            _kill(served["pid"], served["supervisor_pid"])


# ---------------------------------------------------------------------------
# Finding 3 — a post-handshake validation failure owns its cleanup
# ---------------------------------------------------------------------------

class TestPostHandshakeValidation:
    def _serve_in_process(self, project, data_root, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        return exc.value.code, json.loads(capsys.readouterr().out)

    def test_a_missing_state_after_a_success_handshake_leaves_no_orphan(
        self, project, data_root, monkeypatch, capsys,
    ):
        seen: dict = {}
        real_load = DS.load_state

        def eat_state(root):
            state = real_load(root)
            if state is not None and state.status == STATUS_RUNNING:
                seen["app"] = state.pid
                seen["sup"] = state.supervisor_pid
                return None                          # the validation cannot see it
            return state

        monkeypatch.setattr(runtime_cmd, "_state_guard", lambda *a, **k: DS.StateLoad(
            kind=DS.STATE_ABSENT, path=""))
        monkeypatch.setattr(DS, "load_state", eat_state)

        code, out = self._serve_in_process(project, data_root, monkeypatch, capsys)
        monkeypatch.setattr(DS, "load_state", real_load)

        assert code == 5
        assert "no verified running state" in out["error"]
        assert out["survivors"] == []
        assert not _alive(seen["app"]) and not _alive(seen["sup"])
        assert _with_data_root(data_root, load_state, project) is None

    def test_a_mismatched_identity_after_the_handshake_leaves_no_orphan(
        self, project, data_root, monkeypatch, capsys,
    ):
        seen: dict = {}
        real = DS.classify_supervisor

        def broken(state, project_root=None):
            if state is not None and state.status == STATUS_RUNNING:
                seen["app"] = state.pid
                seen["sup"] = state.supervisor_pid
                return DS.IdentityCheck(IDENTITY_MISMATCH, "injected mismatch")
            return real(state, project_root)

        monkeypatch.setattr(DS, "classify_supervisor", broken)
        code, out = self._serve_in_process(project, data_root, monkeypatch, capsys)
        monkeypatch.setattr(DS, "classify_supervisor", real)

        assert code == 5
        assert out["survivors"] == []
        assert not _alive(seen["app"]) and not _alive(seen["sup"])
        assert _with_data_root(data_root, load_state, project) is None


# ---------------------------------------------------------------------------
# Findings 4 + 5 — one failure finalizer; separate process groups
# ---------------------------------------------------------------------------

class TestSupervisorFinalizationAndGroups:
    def test_the_supervisor_and_the_application_are_in_different_groups(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            assert state.pgid != state.supervisor_pgid
            assert state.sid != state.supervisor_sid
            assert os.getpgid(state.pid) == state.pgid
            assert os.getpgid(state.supervisor_pid) == state.supervisor_pgid
            # ...and neither is the group of this test process.
            assert state.pgid != os.getpgrp()
            assert state.supervisor_pgid != os.getpgrp()
        finally:
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_killing_the_app_group_cannot_kill_the_supervisor(
        self, project, data_root,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _with_data_root(data_root, load_state, project)
            os.killpg(state.pgid, 9)                 # the app's WHOLE group
            time.sleep(0.5)
            assert not _alive(app)

            # The supervisor is not in that group, so it survived the kill and was
            # still able to record the truth before leaving on its own.
            deadline = time.time() + 10
            current = None
            while time.time() < deadline:
                current = _with_data_root(data_root, load_state, project)
                if current is not None and current.status == DS.STATUS_EXITED:
                    break
                time.sleep(0.2)
            assert current is not None and current.status == DS.STATUS_EXITED
            assert current.app_exit_code is not None
        finally:
            _kill(app, sup)

    def test_every_supervisor_failure_path_uses_the_common_finalizer(self):
        source = Path("packages/runtimes/runtime_supervisor.py").read_text()
        # No failure path may clear the state on its own any more.
        assert source.count("clear_state(") <= 3, (
            "state clearing must go through _finalize_failure / _finalize_log_failure "
            "/ _supervise")
        assert "_finalize_failure" in source
        for path in ("log pump failed to start",
                     "starting state could not be persisted",
                     "running state could not be persisted",
                     "handshake could not be written",
                     "supervisor failed"):
            idx = source.index(path)
            window = source[max(0, idx - 300):idx + 300]
            assert "_finalize_failure" in window or "_report_failure" in window, path

    def test_a_stop_request_for_another_runtime_is_ignored(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            req = _with_data_root(data_root, DS.stop_request_path, project)
            req.write_text("some-other-runtime\n")
            time.sleep(1.0)
            assert _alive(served["pid"]), "a foreign stop request must be ignored"
            assert _alive(served["supervisor_pid"])
        finally:
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])


# ---------------------------------------------------------------------------
# Finding 3 — a stop request must carry this runtime's EXACT instance id
# ---------------------------------------------------------------------------

class TestStopRequestValidation:
    """The reviewed supervisor rejected only a NON-EMPTY foreign id, so a zero-byte
    `runtime.stop` — which any process on the box can create — shut the runtime down.
    Only an exact instance id may stop a runtime now."""

    @pytest.mark.parametrize("name,payload", [
        ("empty file", b""),
        ("whitespace only", b"   \n\t\n"),
        ("foreign id", b"0123456789abcdef0123456789abcdef\n"),
        ("undecodable bytes", b"\xff\xfe\x00\x01"),
    ])
    def test_an_invalid_stop_request_never_stops_the_runtime(
        self, project, data_root, name, payload,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            req = _with_data_root(data_root, DS.stop_request_path, project)
            req.write_bytes(payload)
            time.sleep(1.5)

            assert _alive(app), f"{name} stopped the application"
            assert _alive(sup), f"{name} stopped the supervisor"
            state = _with_data_root(data_root, load_state, project)
            assert state is not None and state.status == STATUS_RUNNING, name
            assert not req.exists(), "the invalid request must not be left to loop on"
            assert req.with_name(req.name + ".invalid").is_file(), "quarantined"
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)

    @pytest.mark.parametrize("mangle", [
        lambda i: i[:-4],                       # a shortened id
        lambda i: i + "extra",                  # the id plus extra text
        lambda i: i[:16] + "0" * 16,            # half right
        lambda i: f"{i} stop please",           # the id inside other text
    ])
    def test_an_almost_right_instance_id_never_stops_the_runtime(
        self, project, data_root, mangle,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _with_data_root(data_root, load_state, project)
            req = _with_data_root(data_root, DS.stop_request_path, project)
            req.write_text(mangle(state.instance_id) + "\n")
            time.sleep(1.5)

            assert _alive(app) and _alive(sup)
            current = _with_data_root(data_root, load_state, project)
            assert current is not None and current.status == STATUS_RUNNING
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)

    def test_the_exact_instance_id_does_stop_the_runtime(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _with_data_root(data_root, load_state, project)
            req = _with_data_root(data_root, DS.stop_request_path, project)
            req.write_text(f"{state.instance_id}\n")

            deadline = time.time() + 20
            while time.time() < deadline and (_alive(app) or _alive(sup)):
                time.sleep(0.2)

            assert not _alive(app) and not _alive(sup)
            assert _with_data_root(data_root, load_state, project) is None
        finally:
            _kill(app, sup)


# ---------------------------------------------------------------------------
# Finding 3 — a handshake is a CLAIM, never a licence to kill a pid
# ---------------------------------------------------------------------------

class TestHandshakeCleanupIsSafe:
    """The reviewed build passed `payload["app_pid"]` straight into a kill.

    Nothing in a handshake file is identity. The only things this CLI may act on are
    the supervisor pid its OWN Popen returned and the instance id it generated itself;
    the application is only ever stopped by its supervisor, or through a fully verified
    durable state.
    """

    @pytest.fixture
    def victim(self):
        proc = subprocess.Popen([sys.executable, "-c", IDLE])
        _register(proc=proc)
        yield proc
        with __import__("contextlib").suppress(Exception):
            proc.kill()
            proc.wait(timeout=5)

    def _serve(self, project, data_root, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        return exc.value.code, json.loads(capsys.readouterr().out)

    def _forge(self, monkeypatch, mutate):
        """Let the supervisor write its real handshake, then tamper with what the CLI
        reads back — exactly what a stale or hostile file would do."""
        real = SUP.read_handshake

        def forged(path):
            payload = real(path)
            return payload if payload is None else mutate(dict(payload))

        monkeypatch.setattr(SUP, "read_handshake", forged)

    def test_a_forged_app_pid_is_never_killed(self, project, data_root, victim,
                                              monkeypatch, capsys):
        # A truthful handshake, except that it names an unrelated process as the app.
        self._forge(monkeypatch, lambda p: {**p, "app_pid": victim.pid})
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))

        runtime_cmd._cmd_runtime_serve(str(project), json_output=True)
        out = json.loads(capsys.readouterr().out)
        try:
            assert out["ok"] is True
            assert out["pid"] != victim.pid, "the payload pid became the runtime"
            assert victim.poll() is None, "an unrelated process was killed"
        finally:
            _cli(project, data_root, "stop")
            _kill(out.get("pid", 0), out.get("supervisor_pid", 0))
        assert victim.poll() is None

    @pytest.mark.parametrize("name,mutate", [
        ("wrong instance id",
         lambda p, v: {**p, "instance_id": "0" * 32, "app_pid": v}),
        ("missing instance id",
         lambda p, v: {k: val for k, val in {**p, "app_pid": v}.items()
                       if k != "instance_id"}),
        ("wrong supervisor pid",
         lambda p, v: {**p, "supervisor_pid": v, "app_pid": v}),
        ("malformed success payload",
         lambda p, v: {"ok": True, "app_pid": v}),
        ("stale success handshake",
         lambda p, v: {"ok": True, "instance_id": "stale-runtime",
                       "supervisor_pid": v, "app_pid": v, "port": 1, "url": "x"}),
    ])
    def test_an_untrustworthy_handshake_kills_nothing(
        self, project, data_root, victim, monkeypatch, capsys, name, mutate,
    ):
        self._forge(monkeypatch, lambda p: mutate(p, victim.pid))
        code, out = self._serve(project, data_root, monkeypatch, capsys)

        assert code == 5, (name, out)
        assert out["ok"] is False
        assert victim.poll() is None, f"{name}: an unrelated process was killed"
        # ...and this command's own supervisor and application are gone again.
        assert out["survivors"] == [], name
        state = _with_data_root(data_root, load_state, project)
        assert state is None, name


# ---------------------------------------------------------------------------
# Finding 4 — every runtime artifact is private
# ---------------------------------------------------------------------------

SECRET = "s3cr3t-not-for-other-users"


@pytest.fixture
def secret_project(tmp_path) -> Path:
    root = tmp_path / "secretproj"
    root.mkdir()
    (root / "server.py").write_text(SERVER)
    cfg = root / ".remedy"
    cfg.mkdir()
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "server.py"]\n'
        'cwd = "."\nport = 5173\nhealth_path = "/"\nready_timeout_s = 20\n'
        "[runtime.env]\n"
        f'API_TOKEN = "{SECRET}"\n'
    )
    return root


def _mode(path: Path) -> int:
    return path.stat().st_mode & 0o777


class TestRuntimeArtifactsArePrivate:
    def test_every_runtime_artifact_is_owner_only(self, secret_project, data_root):
        code, served, err = _cli(secret_project, data_root, "serve")
        assert code == 0, err
        try:
            rdir = _with_data_root(data_root, DS.runtime_dir, secret_project)
            assert _mode(rdir) == 0o700, oct(_mode(rdir))
            for name in ("runtime.json", "runtime.log", "runtime.lock"):
                path = rdir / name
                assert path.is_file(), name
                assert _mode(path) == 0o600, f"{name} is {oct(_mode(path))}"
            # No temporary file of a failed or finished write is left behind.
            assert not [p for p in rdir.iterdir() if p.name.endswith(".tmp")]
        finally:
            _cli(secret_project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_a_pre_existing_world_readable_artifact_is_repaired(
        self, secret_project, data_root,
    ):
        rdir = _with_data_root(data_root, DS.runtime_dir, secret_project)
        rdir.mkdir(parents=True, exist_ok=True)
        os.chmod(rdir, 0o755)
        stale = rdir / "runtime.log"
        stale.write_text("from an older, laxer build\n")
        os.chmod(stale, 0o644)

        code, served, err = _cli(secret_project, data_root, "serve")
        assert code == 0, err
        try:
            assert _mode(rdir) == 0o700
            assert _mode(rdir / "runtime.log") == 0o600
        finally:
            _cli(secret_project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_the_spec_is_private_and_removed_once_the_supervisor_has_read_it(
        self, secret_project, data_root,
    ):
        code, served, err = _cli(secret_project, data_root, "serve")
        assert code == 0, err
        try:
            rdir = _with_data_root(data_root, DS.runtime_dir, secret_project)
            spec = rdir / "runtime.spec.json"
            assert not spec.exists(), "the ingested spec was left on disk"

            # ...and no other persistent artifact carries the secret.
            for path in rdir.iterdir():
                if path.is_file():
                    body = path.read_bytes()
                    assert SECRET.encode() not in body, path.name
        finally:
            _cli(secret_project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_the_spec_file_is_written_owner_only(self, secret_project, data_root):
        # The mode is asserted at the moment of writing: the supervisor deletes the
        # file as soon as it has read it, so it cannot be inspected afterwards.
        rdir = _with_data_root(data_root, DS.ensure_runtime_dir, secret_project)
        spec = rdir / "runtime.spec.json"
        DS.atomic_write_text(spec, json.dumps({"env": {"API_TOKEN": SECRET}}))
        try:
            assert _mode(spec) == 0o600
        finally:
            spec.unlink()

    def test_a_stopped_runtime_leaves_no_handshake_stop_request_or_spec(
        self, secret_project, data_root,
    ):
        code, served, err = _cli(secret_project, data_root, "serve")
        assert code == 0, err
        try:
            assert _cli(secret_project, data_root, "stop")[0] == 0
            rdir = _with_data_root(data_root, DS.runtime_dir, secret_project)
            left = sorted(p.name for p in rdir.iterdir())
            assert "runtime.handshake.json" not in left
            assert "runtime.stop" not in left
            assert "runtime.spec.json" not in left
        finally:
            _kill(served["pid"], served["supervisor_pid"])


# ---------------------------------------------------------------------------
# Finding 5 — the Evidence-safe view leaks nothing, at any depth
# ---------------------------------------------------------------------------

class TestShareableRedaction:
    """A path does not have to start a whitespace token to be private.

    The reviewed redactor only looked at tokens beginning with `/`, so
    `--repo=/home/user/project`, `cwd=/home/user/project`, a quoted path with spaces and
    an absolute path inside a diagnostic sentence all survived — and
    `"/home/" in json.dumps(state.shareable())` was True. The redaction now works on the
    runtime's exact private VALUES, wherever they appear, and then scrubs anything else
    that still looks like a path.
    """

    def _absolutes(self, value, path="") -> list[str]:
        """Every absolute path anywhere in a nested structure."""
        found: list[str] = []
        if isinstance(value, str):
            for match in DS._ABS_PATH_RE.finditer(value):
                found.append(f"{path}={match.group(0)}")
        elif isinstance(value, (list, tuple)):
            for i, item in enumerate(value):
                found += self._absolutes(item, f"{path}[{i}]")
        elif isinstance(value, dict):
            for key, item in value.items():
                found += self._absolutes(item, f"{path}.{key}")
        return found

    def test_a_real_served_state_shares_nothing_private(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            state = _with_data_root(data_root, load_state, project)
            shared = state.shareable()
            payload = json.dumps(shared)

            assert self._absolutes(shared) == []
            for private in (str(project), str(data_root), state.project_root,
                            state.cwd, state.supervisor_cwd, state.log_path,
                            str(Path(state.log_path).parent), state.instance_id,
                            sys.executable, str(Path.home())):
                assert private not in payload, private
            assert shared["supervisor_cwd"] == "[supervisor_cwd]"
            assert shared["instance_id"] == "[redacted]"
            assert shared["log_path"] == "runtime.log"
            assert shared["url"].startswith("http://127.0.0.1:"), "URLs stay intact"
            # The LOCAL record keeps everything: that is what makes a stop safe.
            assert Path(state.supervisor_cwd).is_absolute()
            assert state.cmd_fingerprint == shared["cmd_fingerprint"]
        finally:
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_embedded_private_paths_are_removed_everywhere(self):
        state = RuntimeState(
            project_root="/home/user/project", cwd="/home/user/project",
            supervisor_cwd="/home/user/remedy",
            supervisor_cmd=["/usr/bin/python3", "-m",
                            "packages.runtimes.runtime_supervisor",
                            "--repo=/home/user/project",
                            "--config=/home/user/secret.cfg"],
            cmd=["/usr/local/bin/node", "dev", "--cwd=/home/user/project",
                 "--data=/home/user/private dir/db"],
            log_path="/home/user/.local/share/remedy/runtime.log",
            instance_id="b" * 32,
            url="http://127.0.0.1:5173/health",
            identity_reason=(
                "working directory '/home/user/private dir' cannot be inspected; "
                "cwd=/home/user/project; see \"/home/user/secret.cfg\""),
            stop_error="killpg(/home/user/project) failed",
        )
        payload = json.dumps(state.shareable())

        assert self._absolutes(state.shareable()) == []
        for private in ("/home/", "/home/user/project", "/home/user/secret.cfg",
                        "/home/user/private dir", "/usr/bin/python3",
                        "/usr/local/bin/node", "/home/user/.local/share/remedy",
                        "b" * 32):
            assert private not in payload, private
        assert "http://127.0.0.1:5173/health" in payload, "a URL is not a private path"

    def test_a_windows_style_absolute_path_is_redacted_too(self):
        state = RuntimeState(
            project_root=r"C:\Users\dev\project", cwd=r"C:\Users\dev\project",
            cmd=[r"C:\Python311\python.exe", "server.py",
                 r"--log=C:\Users\dev\private.log"],
            log_path=r"C:\Users\dev\runtime.log",
        )
        payload = json.dumps(state.shareable())

        assert r"C:\\Users\\dev" not in payload      # json-escaped backslashes
        assert "C:" not in payload.replace("[project_root]", "")

    def test_the_redaction_walks_dictionaries_and_lists_recursively(self):
        nested = {"a": ["/tmp/x", {"b": ({"c": "--conf=/etc/passwd"},
                                         ["'/root/secret file'"])}]}
        redacted = DS._redact(nested)

        assert self._absolutes(redacted) == []
        assert redacted["a"][0] == "x"
        assert redacted["a"][1]["b"][0]["c"] == "--conf=passwd"


# ---------------------------------------------------------------------------
# Finding 4 — the whole FILE terminates, and leaves nothing behind
# ---------------------------------------------------------------------------

class TestNoRuntimeProcessSurvivesThisFile:
    def test_no_test_owned_supervisor_or_application_remains(self, tmp_path_factory):
        """Every test in this file cleans up its own process groups.

        Scoped to this run's pytest temporary directory: a leak from ANOTHER suite is
        not silently swept up here, and no process outside /tmp/pytest-* is ever looked
        at, let alone signalled.
        """
        base = str(tmp_path_factory.getbasetemp())
        leftovers = []
        for proc in psutil.process_iter(["pid", "cmdline"]):
            try:
                cmdline = " ".join(proc.info["cmdline"] or [])
                cwd = ""
                with __import__("contextlib").suppress(psutil.Error):
                    cwd = proc.cwd()
            except psutil.Error:
                continue
            if base in cmdline or (cwd and base in cwd):
                if "runtime_supervisor" in cmdline or "server.py" in cmdline:
                    leftovers.append((proc.pid, cmdline[:80]))

        assert leftovers == [], f"test-owned runtime processes survived: {leftovers}"


# ---------------------------------------------------------------------------
# Finding 1 — a served runtime is revalidated AFTER the HTTP request
# ---------------------------------------------------------------------------

#: A real, separate `runtime probe` process in which the supervisor dies WHILE the
#: health URL is being fetched. The race is made deterministic inside the CLI process
#: that actually runs, not simulated in the parent.
PROBE_RACE_BOOTSTRAP = """
import sys
import psutil
from packages.runtimes import dev_server as DS

_real_probe = DS.http_probe

def racing_probe(url, timeout=3.0):
    state = DS.load_state({repo!r})
    victim = psutil.Process(state.supervisor_pid)
    victim.kill()
    victim.wait(timeout=5)
    return _real_probe(url, timeout=timeout)

DS.http_probe = racing_probe
sys.argv = {argv!r}
from apps.cli.main import main
main()
"""


class TestProbeRevalidatesAfterTheHttpRequest:
    """A 200 from the port says nothing about who OWNS the process behind it.

    The classification under the lifecycle lock is a statement about the PAST: the
    supervisor can die while the health URL is being fetched, and the application will
    keep answering happily with nobody owning its log pump or its lifecycle. So the
    runtime is classified again, under the lock, after the request — same instance, same
    pids and creation times, still `running`, still supervised — before anything may say
    ok=true.
    """

    def _probe(self, project, data_root, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        try:
            runtime_cmd._cmd_runtime_probe(str(project), json_output=True)
            code = 0
        except SystemExit as exc:
            code = exc.code
        return code, json.loads(capsys.readouterr().out)

    def _during_http(self, monkeypatch, hook):
        """Run `hook()` in the middle of the served runtime's health request."""
        real = DS.http_probe

        def racing(url, timeout=3.0):
            hook()
            return real(url, timeout=timeout)

        monkeypatch.setattr(DS, "http_probe", racing)

    def test_a_supervisor_that_dies_during_the_http_request_is_never_healthy(
        self, project, data_root, monkeypatch, capsys,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            self._during_http(monkeypatch, lambda: (psutil.Process(sup).kill(),
                                                    psutil.Process(sup).wait(timeout=5)))
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 5, out
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert out["status_code"] == 200, "the app really did answer"
            assert _alive(app), "nothing may be killed by a probe"
        finally:
            _kill(app, sup)

    def test_a_supervisor_killed_just_before_the_request_is_never_healthy(
        self, project, data_root, monkeypatch, capsys,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            # The classification happens first and still sees a live supervisor; the
            # supervisor dies before a single byte of the request goes out.
            real_classify = DS.classify_runtime

            def classify_then_kill(state, project_root=None):
                ident = real_classify(state, project_root)
                if ident.ownership == DS.OWNER_SUPERVISED and _alive(sup):
                    psutil.Process(sup).kill()
                    psutil.Process(sup).wait(timeout=5)
                return ident

            monkeypatch.setattr(DS, "classify_runtime", classify_then_kill)
            monkeypatch.setattr(runtime_cmd, "_revalidate_served",
                                runtime_cmd._revalidate_served)  # the real one
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 5, out
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert _alive(app)
        finally:
            _kill(app, sup)

    def test_an_application_that_dies_during_the_request_is_never_healthy(
        self, project, data_root, monkeypatch, capsys,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            self._during_http(monkeypatch, lambda: DS.stop_process_tree(app))
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 5, out
            assert out["ok"] is False
            assert not _alive(app)
        finally:
            _kill(app, sup)

    def test_a_state_replaced_during_the_request_is_never_healthy(
        self, project, data_root, monkeypatch, capsys,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]

        def swap():
            state = _with_data_root(data_root, load_state, project)
            state.pid = 999999999                   # a different runtime entirely
            state.create_time = 1.0
            _with_data_root(data_root, save_state, state)

        try:
            self._during_http(monkeypatch, swap)
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 5, out
            assert out["ok"] is False
            assert "different runtime instance" in out["error"]
            assert _alive(app) and _alive(sup), "nothing was killed"
        finally:
            _kill(app, sup)

    def test_an_instance_id_that_changes_during_the_request_is_never_healthy(
        self, project, data_root, monkeypatch, capsys,
    ):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]

        def swap():
            state = _with_data_root(data_root, load_state, project)
            state.instance_id = new_instance_id()
            _with_data_root(data_root, save_state, state)

        try:
            self._during_http(monkeypatch, swap)
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 5, out
            assert out["ok"] is False
            assert _alive(app) and _alive(sup)
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)

    def test_a_normal_served_probe_still_succeeds(self, project, data_root,
                                                  monkeypatch, capsys):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        try:
            code, out = self._probe(project, data_root, monkeypatch, capsys)

            assert code == 0, out
            assert out["ok"] is True
            assert out["managed_by_serve"] is True and out["stopped"] is False
            assert _alive(served["pid"]) and _alive(served["supervisor_pid"])
        finally:
            _cli(project, data_root, "stop")
            _kill(served["pid"], served["supervisor_pid"])

    def test_the_real_probe_cli_process_loses_its_supervisor_mid_request(
        self, project, data_root,
    ):
        """The same race, in the REAL separate `runtime probe` process."""
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            env = dict(os.environ, REMEDY_DATA_DIR=str(data_root))
            argv = ["remedy", "runtime", "probe", "--repo", str(project), "--json"]
            proc = subprocess.run(
                [sys.executable, "-c",
                 PROBE_RACE_BOOTSTRAP.format(repo=str(project), argv=argv)],
                cwd=str(REPO), env=env, capture_output=True, text=True, timeout=120,
            )
            out = json.loads(proc.stdout) if proc.stdout.strip() else {}

            assert proc.returncode == 5, (proc.stdout, proc.stderr)
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert not _alive(sup) and _alive(app), "the app was answering all along"
        finally:
            _kill(app, sup)


# ---------------------------------------------------------------------------
# Finding 2 — the hard stop fallback re-verifies the supervisor first
# ---------------------------------------------------------------------------

class TestHardStopFallbackRevalidation:
    """Fifteen seconds pass between the stop request and the hard fallback.

    The identity verified before that wait is a statement about the past: if the
    original supervisor exited and its pid — or its process group — was handed to
    somebody else, the old numbers now point at a stranger. So the supervisor is
    classified again from scratch immediately before any signal, and only the group
    THAT check observed is ever used.
    """

    @pytest.fixture
    def deaf_supervisor(self, monkeypatch, tmp_path, data_root, project):
        """A served runtime whose supervisor never sees the stop request.

        The request is written somewhere the supervisor does not poll, so the wait runs
        out and the destructive fallback is reached — deterministically, without killing
        anything first.
        """
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
        monkeypatch.setattr(DS, "STOP_REQUEST_TIMEOUT_S", 1.0)
        monkeypatch.setattr(DS, "stop_request_path",
                            lambda root: tmp_path / "nowhere.stop")
        yield served
        _kill(served["pid"], served["supervisor_pid"])

    def _spy_on_stop(self, monkeypatch, *, execute: bool):
        calls: list[dict] = []
        real = DS.stop_process_tree

        def spy(pid, grace=DS.GRACE_SECONDS, session_id=0):
            calls.append({"pid": pid, "session_id": session_id})
            if execute:
                return real(pid, grace, session_id)
            return {"pid": pid, "session_id": session_id, "terminated": [],
                    "killed": [], "survivors": [], "error": ""}

        monkeypatch.setattr(DS, "stop_process_tree", spy)
        return calls

    def _forge_fresh_supervisor(self, monkeypatch, check):
        """The FIRST classification is the real one; the one before the hard signal is
        the injected one — exactly the window in which a pid may be reused."""
        real = DS.classify_supervisor
        seen: list[int] = []

        def classify(state, project_root=None):
            seen.append(1)
            if len(seen) == 1:
                return real(state, project_root)
            return check

        monkeypatch.setattr(DS, "classify_supervisor", classify)

    @pytest.mark.parametrize("name,check", [
        ("creation time changed", DS.IdentityCheck(
            DS.PID_REUSED, "supervisor pid was reused")),
        ("command line changed", DS.IdentityCheck(
            DS.IDENTITY_MISMATCH, "supervisor pid runs a different command")),
        ("pid disappeared and was replaced", DS.IdentityCheck(
            DS.PID_REUSED, "supervisor pid was reused")),
        ("pgid changed", DS.IdentityCheck(
            DS.IDENTITY_MISMATCH, "supervisor lives in group 4242, not the recorded")),
        ("sid changed", DS.IdentityCheck(
            DS.IDENTITY_MISMATCH, "supervisor lives in session 4242, not the recorded")),
        ("no longer inspectable", DS.IdentityCheck(
            DS.IDENTITY_UNPROVEN, "supervisor pid cannot be inspected")),
    ])
    def test_a_stale_supervisor_identity_is_never_signalled(
        self, deaf_supervisor, project, data_root, monkeypatch, name, check,
    ):
        app, sup = deaf_supervisor["pid"], deaf_supervisor["supervisor_pid"]
        calls = self._spy_on_stop(monkeypatch, execute=False)
        self._forge_fresh_supervisor(monkeypatch, check)

        result = DS.stop_recorded_runtime(project)

        assert result["ok"] is False, name
        assert result["stopped"] is False
        assert calls == [], f"{name}: a stale identity was signalled"
        assert _alive(sup) and _alive(app), name
        assert sorted(result["survivors"]) == sorted([app, sup])
        assert result["manual_cleanup"]
        state = _with_data_root(data_root, load_state, project)
        assert state is not None
        assert state.status in (DS.STATUS_STOP_FAILED, DS.STATUS_IDENTITY_UNPROVEN)
        assert state.stop_error

    def test_an_unchanged_supervisor_identity_permits_the_hard_fallback(
        self, deaf_supervisor, project, data_root, monkeypatch,
    ):
        app, sup = deaf_supervisor["pid"], deaf_supervisor["supervisor_pid"]
        calls = self._spy_on_stop(monkeypatch, execute=True)

        result = DS.stop_recorded_runtime(project)

        assert result["ok"] is True and result["stopped"] is True
        assert result["survivors"] == []
        assert sup in [c["pid"] for c in calls], "the supervisor was never stopped"
        assert not _alive(sup) and not _alive(app)
        assert _with_data_root(data_root, load_state, project) is None

    def test_the_freshly_observed_group_is_the_one_that_is_signalled(
        self, deaf_supervisor, project, data_root, monkeypatch,
    ):
        app, sup = deaf_supervisor["pid"], deaf_supervisor["supervisor_pid"]
        state = _with_data_root(data_root, load_state, project)
        stale_pgid = state.supervisor_pgid
        fresh_pgid = stale_pgid + 4242                 # a group only the FRESH check sees

        calls = self._spy_on_stop(monkeypatch, execute=False)
        self._forge_fresh_supervisor(
            monkeypatch,
            DS.IdentityCheck(DS.VERIFIED, "", live_pgid=fresh_pgid,
                             live_sid=fresh_pgid),
        )

        DS.stop_recorded_runtime(project)

        supervisor_calls = [c for c in calls if c["pid"] == sup]
        assert supervisor_calls, "the verified supervisor was not stopped"
        assert supervisor_calls[0]["session_id"] == fresh_pgid
        assert supervisor_calls[0]["session_id"] != stale_pgid, (
            "the stale process group was used destructively")


# ---------------------------------------------------------------------------
# Finding 3 — every normal absolute-path form, on any platform
# ---------------------------------------------------------------------------

class TestCrossPlatformRedaction:
    """`C:\\Users\\Alice\\file` was redacted; `C:/Users/Alice/file` and
    `\\\\server\\share\\file` were not — and a shared Evidence artifact does not care
    which slash the operator's platform prefers."""

    def _absolutes(self, value) -> list[str]:
        if isinstance(value, str):
            return [m.group(0) for m in DS._ABS_PATH_RE.finditer(value)]
        if isinstance(value, (list, tuple)):
            return [f for item in value for f in self._absolutes(item)]
        if isinstance(value, dict):
            return [f for item in value.values() for f in self._absolutes(item)]
        return []

    def test_windows_forward_slash_paths_are_redacted(self):
        state = RuntimeState(
            project_root="C:/Users/Alice/project", cwd="C:/Users/Alice/project",
            cmd=["C:/Python311/python.exe", "server.py",
                 "--config=C:/Users/Alice/secret.ini"],
            log_path="C:/Users/Alice/runtime.log",
            identity_reason=(
                'working directory "C:/Users/Alice/private dir" cannot be inspected'),
        )
        payload = json.dumps(state.shareable())

        assert self._absolutes(state.shareable()) == []
        # Bare file names survive by design (they are not private paths); the drive,
        # the user and every directory prefix do not.
        for private in ("C:/Users", "C:/Python311", "Alice", "Users/Alice", "C:/"):
            assert private not in payload, private
        cmd = json.loads(payload)["cmd"]
        assert cmd[0] == "python.exe", "only the bare file name may survive"
        assert cmd[-1].endswith("secret.ini") and "Alice" not in cmd[-1]

    def test_unc_paths_are_redacted_in_both_slash_styles(self):
        state = RuntimeState(
            project_root=r"\\server\share\project", cwd="//server/share/project",
            supervisor_cwd=r"\\server\share\remedy",
            supervisor_cmd=[r"\\server\tools\python.exe",
                            r"--data=\\server\share\secret.txt"],
            cmd=["//server/share/node", "--conf=//server/share/secret.cfg"],
            log_path=r"\\server\share\runtime.log",
            stop_error=r"path=\\server\share\secret.txt could not be removed",
        )
        payload = json.dumps(state.shareable())

        assert self._absolutes(state.shareable()) == []
        for private in (r"\\\\server", "//server", "server\\share",
                        "server/share", "share/secret", r"share\\secret"):
            assert private not in payload, private
        sup_cmd = json.loads(payload)["supervisor_cmd"]
        assert sup_cmd[0] == "python.exe", "only the bare file name may survive"
        assert sup_cmd[-1].endswith("secret.txt") and "server" not in sup_cmd[-1]

    def test_urls_and_ordinary_text_survive_the_redaction(self):
        state = RuntimeState(
            url="http://127.0.0.1:5173/health",
            project_root="/home/user/project",
            log_error="see https://example.test/docs and the C: drive, ratio 3/4",
            log_path="/home/user/.remedy/runtime.log",
        )
        shared = state.shareable()
        payload = json.dumps(shared)

        assert shared["url"] == "http://127.0.0.1:5173/health"
        assert "https://example.test/docs" in payload
        assert "the C: drive" in payload, "a bare drive letter is ordinary text"
        assert "ratio 3/4" in payload
        assert "/home/user" not in payload


# ---------------------------------------------------------------------------
# Finding 1 — the bounded log pump is watched for the WHOLE life of the runtime
# ---------------------------------------------------------------------------

#: The supervisor is a separate process started by the serve CLI, so the failure has to
#: be injected INTO that process. The serve CLI is run with a Popen wrapper that rewrites
#: `python -m packages.runtimes.runtime_supervisor …` into `python -c <child> …`, and the
#: child installs a broken LogPump before handing over to the real supervisor main().
#: No production switch, no environment flag: the injection lives entirely in the test.
SUPERVISOR_CHILD = '''
import os, sys, threading, time
import psutil
from packages.runtimes import dev_server as DS
from packages.runtimes import runtime_supervisor as SUP

_RealPump = DS.LogPump

# The supervisor reconstructs its own argv as `python -m packages.runtimes...`; run
# through `python -c`, its LIVE command line is different, and the CLI would rightly
# refuse the runtime as an identity mismatch. So the record is made to say what the
# process REALLY is — the identity checks stay exactly as strict as in production.
_RealState = SUP.RuntimeState

class LiveState(_RealState):
    def __init__(self, **kw):
        if kw.get("supervisor_pid"):
            live = psutil.Process(os.getpid()).cmdline()
            kw["supervisor_cmd"] = live
            kw["supervisor_fingerprint"] = DS.resolved_fingerprint(
                live, kw.get("supervisor_cwd") or os.getcwd(),
                kw.get("project_id") or "")
        super().__init__(**kw)

SUP.RuntimeState = LiveState

# The one synchronisation point of every pump injection. `_supervise()` is only entered
# once the `running` state has been persisted AND the success handshake has been written
# — which is exactly the moment the serve CLI is allowed to return 0. Nothing in these
# tests infers the lifecycle phase from elapsed time: a slower machine simply waits
# longer, it does not change what is being tested. (The reviewed tests slept 0.8 s and,
# on a slower host, injected their failure BEFORE the handshake — proving nothing.)
AFTER_HANDSHAKE = threading.Event()
RELEASE = {release!r}

_real_supervise = SUP.Supervisor._supervise

def _supervise(self):
    AFTER_HANDSHAKE.set()
    return _real_supervise(self)

SUP.Supervisor._supervise = _supervise

def _mark(name, text="ok"):
    """Leave an observable trace of an injected action. A daemon thread that dies
    invisibly (the packaged race test raised NameError into DEVNULL and nobody noticed)
    must never be able to satisfy a regression."""
    with open(RELEASE + "." + name, "w") as fh:
        fh.write(str(text))

def _guard(name, body):
    """Run an injected action; record that it ran, or record why it did not."""
    def run():
        try:
            body()
        except BaseException as exc:
            _mark("error", "%s: %s: %s" % (name, type(exc).__name__, exc))
            return
        _mark(name)
    return run

def _await_handshake():
    assert AFTER_HANDSHAKE.wait(120), "the supervisor never reached _supervise()"

def _await_release():
    """Block until the runtime is REALLY up and the serve CLI has really returned.

    Two facts, both observed, neither guessed from a clock:
      * `_supervise()` was entered — so `running` was persisted and the success
        handshake was written;
      * the test released us — so the serve CLI has already exited 0.
    """
    _await_handshake()
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        if os.path.exists(RELEASE):
            return
        time.sleep(0.02)
    raise AssertionError("the test never released the injected failure")

{inject}
sys.exit(SUP.main(sys.argv[1:]))
'''

SERVE_WITH_BROKEN_PUMP = """
import sys, subprocess, time
from packages.runtimes import dev_server as DS
CHILD = {child!r}
_real_popen = subprocess.Popen

class Popen(_real_popen):
    def __init__(self, argv, *a, **kw):
        if (len(argv) > 2 and argv[1] == '-m'
                and argv[2] == 'packages.runtimes.runtime_supervisor'):
            argv = [argv[0], '-c', CHILD] + argv[3:]
        super().__init__(argv, *a, **kw)

subprocess.Popen = Popen
{parent}
sys.argv = {argv!r}
from apps.cli.main import main
main()
"""

#: Make the serve CLI's FINAL validation lose the race on purpose: it waits until the
#: supervisor has recorded a terminal state. That is the window the reviewer reproduced —
#: the handshake said "running", the durable state already says "log_failed".
PARENT_WAITS_FOR_A_TERMINAL_STATE = """
_real_load = DS.load_state

def _load_state(root):
    state = _real_load(root)
    if state is not None and state.status == DS.STATUS_RUNNING:
        deadline = time.time() + 30
        while time.time() < deadline:
            later = _real_load(root)
            if later is None or later.status != DS.STATUS_RUNNING:
                return later
            time.sleep(0.05)
    return state

DS.load_state = _load_state
"""

#: The reviewer's reproduction, made deterministic: the pump starts, the runtime reaches
#: `running`, the handshake is written, the serve CLI returns 0 — and only THEN the pump
#: records its failure while the application is still serving.
PUMP_FAILS_LATE = '''
class BrokenPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            self.error = "OSError: injected persistent pump failure"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = BrokenPump
'''

#: A pump whose THREAD simply ends after the handshake, with no error string at all.
#: Nothing drains the application's stdout any more — a runtime failure without an
#: exception.
PUMP_THREAD_DIES_SILENTLY = '''
class SilentPump(_RealPump):
    def _run(self):
        self.started.set()
        _await_release()         # ...and then the thread is simply gone. No error.

SUP.LogPump = SilentPump
'''

#: The pump fails AND the application exits at almost the same moment — both released by
#: the same handshake event, so they really do race each other and nothing else.
PUMP_FAILS_WITH_THE_APP = '''
import signal

class RacingPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            self.error = "injected pump failure racing the app"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = RacingPump

_supervise_with_event = SUP.Supervisor._supervise

def _racing_supervise(self):
    def kill_app():
        _await_release()
        os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
    threading.Thread(target=_guard("app", kill_app), daemon=True).start()
    return _supervise_with_event(self)

SUP.Supervisor._supervise = _racing_supervise
'''

#: A pump that fails the moment `_supervise()` is entered — i.e. the success handshake
#: has just been written and the serve CLI has NOT yet done its final validation. No
#: release file: this failure is deliberately allowed to win that race.
PUMP_FAILS_IMMEDIATELY = '''
class InstantlyBrokenPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_handshake()
            self.error = "OSError: injected pump failure right after the handshake"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = InstantlyBrokenPump
'''

#: The application exits the moment `_supervise()` is entered — same race, other cause.
APP_EXITS_IMMEDIATELY = '''
import signal

_supervise_with_event = SUP.Supervisor._supervise

def _killing_supervise(self):
    def kill_app():
        _await_handshake()
        os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
    threading.Thread(target=_guard("app", kill_app), daemon=True).start()
    return _supervise_with_event(self)

SUP.Supervisor._supervise = _killing_supervise
'''

#: The pump fails after the handshake and the cleanup cannot get rid of the application.
PUMP_FAILURE_LEAVES_A_SURVIVOR = '''
class BrokenPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            self.error = "injected persistent pump failure"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = BrokenPump

def refuses_to_stop(pid, grace=DS.GRACE_SECONDS, session_id=0):
    return {"pid": pid, "session_id": session_id, "terminated": [], "killed": [],
            "survivors": [pid], "error": "injected: the application could not be stopped"}
SUP.stop_process_tree = refuses_to_stop
'''

#: The pump fails after the handshake and the diagnostic cannot be persisted. Nothing
#: survived the cleanup, so the now-false `running` record may be cleared.
PUMP_FAILURE_AND_UNWRITABLE_STATE = '''
class BrokenPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            self.error = "injected persistent pump failure"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = BrokenPump

_real_save = SUP.save_state
def save_state(state):
    if state.status in (DS.STATUS_LOG_FAILED, DS.STATUS_LOG_CLEANUP_FAILED):
        raise OSError("injected: the runtime state cannot be written")
    return _real_save(state)
SUP.save_state = save_state
'''

#: The dangerous combination: the cleanup leaves a live survivor AND the diagnostic
#: cannot be written. The pre-existing record is the ONLY identity that survivor has.
PUMP_FAILURE_SURVIVOR_AND_UNWRITABLE_STATE = '''
class BrokenPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            self.error = "injected persistent pump failure"
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = BrokenPump

def refuses_to_stop(pid, grace=DS.GRACE_SECONDS, session_id=0):
    return {"pid": pid, "session_id": session_id, "terminated": [], "killed": [],
            "survivors": [pid], "error": "injected: the application could not be stopped"}
SUP.stop_process_tree = refuses_to_stop

_real_save = SUP.save_state
def save_state(state):
    if state.status in (DS.STATUS_LOG_FAILED, DS.STATUS_LOG_CLEANUP_FAILED):
        raise OSError("injected: the runtime state cannot be written")
    return _real_save(state)
SUP.save_state = save_state
'''


def _serve_with_broken_pump(project: Path, data_root: Path, inject: str,
                            release: Path, timeout: float = 240.0,
                            parent: str = ""):
    """Run the REAL serve CLI whose supervisor gets a broken LogPump.

    The failure is armed but not fired: it waits for `_supervise()` (the runtime is up
    and the handshake is written) AND for the caller to create ``release`` (the serve CLI
    has returned). No sleep decides when a lifecycle phase has been reached.
    """
    env = dict(os.environ, REMEDY_DATA_DIR=str(data_root))
    argv = ["remedy", "runtime", "serve", "--repo", str(project), "--json"]
    child = SUPERVISOR_CHILD.format(inject=inject, release=str(release))
    proc = subprocess.run(
        [sys.executable, "-c",
         SERVE_WITH_BROKEN_PUMP.format(child=child, argv=argv, parent=parent)],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=timeout,
    )
    payload = {}
    if proc.stdout.strip():
        with __import__("contextlib").suppress(ValueError):
            payload = json.loads(proc.stdout)
    _register(payload, project=project, data_root=data_root)
    return proc.returncode, payload, proc.stderr


def _await_state(data_root: Path, project: Path, statuses: tuple[str, ...],
                 timeout: float = 30.0):
    deadline = time.time() + timeout
    state = None
    while time.time() < deadline:
        state = _with_data_root(data_root, load_state, project)
        if state is not None and state.status in statuses:
            return state
        time.sleep(0.2)
    return state


class TestPersistentLogPumpHealth:
    """A runtime whose bounded log nobody drains is not a healthy runtime.

    Every injected pump failure here is released by two OBSERVED facts, never by a clock:
    the supervisor entered `_supervise()` (so `running` was persisted and the success
    handshake written), and the test created the release file (so the serve CLI has
    already returned 0). The reviewed tests slept 0.8 s instead, and on a slower host the
    pump failed BEFORE the handshake — which is why four of them failed externally.
    """

    @pytest.fixture
    def release(self, tmp_path) -> Path:
        return tmp_path / "release-the-pump-failure"

    def _serve_then_release(self, project, data_root, inject, release):
        code, served, err = _serve_with_broken_pump(
            project, data_root, inject, release)
        assert code == 0, err          # serve REALLY succeeded: running + handshake
        assert served["status"] == STATUS_RUNNING
        release.write_text("go\n")    # ...only now may the pump fail
        return served

    def test_a_post_handshake_pump_failure_ends_the_runtime_honestly(
        self, project, data_root, release,
    ):
        served = self._serve_then_release(
            project, data_root, PUMP_FAILS_LATE, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _await_state(data_root, project, (DS.STATUS_LOG_FAILED,))
            assert state is not None
            assert state.status == DS.STATUS_LOG_FAILED, state.status
            assert "injected persistent pump failure" in state.log_error
            assert state.survivors == []

            # The application family is gone, and so is the supervisor.
            deadline = time.time() + 20
            while time.time() < deadline and (_alive(app) or _alive(sup)):
                time.sleep(0.2)
            assert not _alive(app) and not _alive(sup)

            # A separate probe reports the FRESH failure and never calls it healthy.
            code, out, err = _cli(project, data_root, "probe")
            assert code == 5, (out, err)
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_LOG_FAILED
            assert "injected persistent pump failure" in out["log_error"]

            # ...and a separate stop clears the diagnostic, idempotently.
            code, out, err = _cli(project, data_root, "stop")
            assert code == 0, (out, err)
            assert _with_data_root(data_root, load_state, project) is None
            assert _cli(project, data_root, "stop")[0] == 0
        finally:
            _kill(app, sup)

    def test_a_pump_thread_that_ends_without_an_error_is_still_a_failure(
        self, project, data_root, release,
    ):
        served = self._serve_then_release(
            project, data_root, PUMP_THREAD_DIES_SILENTLY, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _await_state(data_root, project, (DS.STATUS_LOG_FAILED,))
            assert state is not None and state.status == DS.STATUS_LOG_FAILED
            assert "log pump exited unexpectedly" in state.log_error
            assert not _alive(app)
        finally:
            _kill(app, sup)

    def test_a_pump_failure_racing_the_application_exit_is_recorded_honestly(
        self, project, data_root, release,
    ):
        """BOTH injected actions must really run.

        The packaged version of this test called an undefined `_await_handshake()`; the
        helper thread died with NameError into the supervisor's DEVNULL stderr, so the
        application was never killed and only the pump failure was ever exercised. Every
        injected action now leaves an observable marker, and an exception inside one of
        them leaves an `.error` marker that fails the test.
        """
        served = self._serve_then_release(
            project, data_root, PUMP_FAILS_WITH_THE_APP, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _await_state(
                data_root, project, (DS.STATUS_LOG_FAILED, DS.STATUS_EXITED))

            pump_mark = Path(str(release) + ".pump")
            app_mark = Path(str(release) + ".app")
            error_mark = Path(str(release) + ".error")
            deadline = time.time() + 20
            while time.time() < deadline and not (pump_mark.exists()
                                                  and app_mark.exists()):
                if error_mark.exists():
                    break
                time.sleep(0.1)

            assert not error_mark.exists(), error_mark.read_text()
            assert pump_mark.is_file(), "the pump failure was never injected"
            assert app_mark.is_file(), "the application was never killed"

            assert state is not None
            assert state.status in (DS.STATUS_LOG_FAILED, DS.STATUS_EXITED)
            assert state.status != STATUS_RUNNING
            assert state.survivors == []

            # The supervisor records the outcome and THEN leaves; give it that moment
            # instead of demanding it has already vanished the instant we looked.
            deadline = time.time() + 20
            while time.time() < deadline and (_alive(app) or _alive(sup)):
                time.sleep(0.2)
            assert not _alive(app) and not _alive(sup)
        finally:
            _kill(app, sup)

    def test_a_broken_helper_thread_fails_the_regression(self, project, data_root,
                                                         release):
        """The guard itself is proven: an injected action that raises is NOT silent."""
        broken = """
class BrokenHelperPump(_RealPump):
    def start(self, timeout=5.0):
        super().start(timeout)
        def boom():
            _await_release()
            _undefined_helper()          # exactly the packaged NameError
        threading.Thread(target=_guard("pump", boom), daemon=True).start()

SUP.LogPump = BrokenHelperPump
"""
        served = self._serve_then_release(project, data_root, broken, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            error_mark = Path(str(release) + ".error")
            deadline = time.time() + 20
            while time.time() < deadline and not error_mark.exists():
                time.sleep(0.1)
            assert error_mark.is_file(), "a helper-thread failure stayed invisible"
            assert "NameError" in error_mark.read_text()
            assert not Path(str(release) + ".pump").exists()
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)

    def test_a_pump_failure_whose_cleanup_leaves_a_survivor_is_retained(
        self, project, data_root, release,
    ):
        served = self._serve_then_release(
            project, data_root, PUMP_FAILURE_LEAVES_A_SURVIVOR, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            state = _await_state(data_root, project, (DS.STATUS_LOG_CLEANUP_FAILED,))
            assert state is not None
            assert state.status == DS.STATUS_LOG_CLEANUP_FAILED
            assert state.survivors == [app]
            assert "survived the cleanup" in state.stop_error
            assert _alive(app), "the survivor is real: it is reported, not pretended away"

            code, out, err = _cli(project, data_root, "probe")
            assert code == 5, (out, err)
            assert out["runtime_status"] == DS.STATUS_LOG_CLEANUP_FAILED
            assert out["survivors"] == [app]
        finally:
            _kill(app, sup)

    def test_a_pump_failure_with_an_unwritable_state_never_leaves_running_behind(
        self, project, data_root, release,
    ):
        served = self._serve_then_release(
            project, data_root, PUMP_FAILURE_AND_UNWRITABLE_STATE, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            deadline = time.time() + 25
            while time.time() < deadline and _alive(sup):
                time.sleep(0.2)
            assert not _alive(sup) and not _alive(app), "the app family was not stopped"

            # Nothing survived, so clearing the now-false `running` record is safe.
            state = _with_data_root(data_root, load_state, project)
            assert state is None or state.status != STATUS_RUNNING, (
                "a runtime nobody owns must never be left recorded as running")

            code, out, err = _cli(project, data_root, "probe")
            assert code != 0 or out.get("managed_by_serve") is not True
        finally:
            _kill(app, sup)

    def test_a_survivor_never_loses_its_last_durable_identity(
        self, project, data_root, release,
    ):
        """The dangerous combination: a LIVE survivor, and a diagnostic that cannot be
        written. runtime.json is the only record of that process's pid, creation time,
        process group, session and instance id — deleting it would strand a live process
        that no later command could ever prove ownership of again."""
        served = self._serve_then_release(
            project, data_root, PUMP_FAILURE_SURVIVOR_AND_UNWRITABLE_STATE, release)
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            deadline = time.time() + 25
            while time.time() < deadline and _alive(sup):
                time.sleep(0.2)
            assert not _alive(sup), "the supervisor should have given up"
            assert _alive(app), "the injected cleanup failure keeps the app alive"

            # The record still exists, and still describes the live survivor exactly.
            state = _with_data_root(data_root, load_state, project)
            assert state is not None, "the survivor's only identity was deleted"
            assert state.pid == app
            assert state.create_time == served["create_time"]
            assert state.pgid == served["pgid"] and state.sid == served["sid"]
            assert state.instance_id == served["instance_id"]

            # A later probe explains the situation and asks for manual cleanup.
            code, out, err = _cli(project, data_root, "probe")
            assert code == 5, (out, err)
            assert out["ok"] is False
            assert out["runtime_status"] == DS.STATUS_SUPERVISOR_MISSING
            assert out["manual_cleanup"] == [app]
            assert _alive(app), "probe must never guess ownership of an orphan"

            # A later stop guesses nothing either.
            code, out, err = _cli(project, data_root, "stop")
            assert code == 5, (out, err)
            assert out["survivors"] == [app]
            assert _alive(app)

            # Once the operator has terminated the recorded survivor, stop clears it.
            DS.stop_process_tree(app)
            code, out, err = _cli(project, data_root, "stop")
            assert code == 0, (out, err)
            assert _with_data_root(data_root, load_state, project) is None
            assert _cli(project, data_root, "stop")[0] == 0
        finally:
            _kill(app, sup)

    def test_a_diagnostic_write_failure_with_a_real_survivor_keeps_the_record(
        self, project, data_root, tmp_path,
    ):
        """The reviewer's direct reproduction, with a real harmless sleep process."""
        victim = subprocess.Popen([sys.executable, "-c", IDLE])
        try:
            os.environ["REMEDY_DATA_DIR"] = str(data_root)
            before = RuntimeState(
                pid=victim.pid,
                create_time=psutil.Process(victim.pid).create_time(),
                pgid=os.getpgid(victim.pid), sid=os.getsid(victim.pid),
                port=1, status=STATUS_RUNNING,
                project_root=str(project), project_id=project_digest(project),
                cwd=str(project), cmd=["sleep"], cmd_fingerprint="x",
                supervisor_pid=os.getpid(), instance_id=new_instance_id(),
            )
            save_state(before)

            sup = SUP.Supervisor(spec=None, project_root=str(project),
                                 handshake=tmp_path / "hs.json",
                                 instance_id=before.instance_id)
            sup.state = before
            sup._stop_app = lambda: {"survivors": [victim.pid],
                                     "error": "injected survivor"}
            sup._remove_control_files = lambda **kw: None

            real_save = SUP.save_state
            def refuses(state):
                if state.status in (DS.STATUS_LOG_FAILED, DS.STATUS_LOG_CLEANUP_FAILED):
                    raise OSError("injected: the runtime state cannot be written")
                return real_save(state)

            SUP.save_state = refuses
            try:
                code = sup._finalize_log_failure("injected pump failure")
            finally:
                SUP.save_state = real_save

            assert code == 5
            assert victim.poll() is None, "the survivor is real and still alive"

            kept = load_state(project)
            assert kept is not None, "the survivor's only durable identity was erased"
            assert kept.pid == victim.pid
            assert kept.create_time == before.create_time
            assert kept.pgid == before.pgid and kept.sid == before.sid
            assert kept.instance_id == before.instance_id

            # The unwritable diagnostic is left as a private note — never as authority.
            note = DS.runtime_dir(project) / "runtime.log_failure.json"
            if note.exists():
                assert note.stat().st_mode & 0o777 == 0o600
                assert json.loads(note.read_text())["survivors"] == [victim.pid]
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)
            victim.kill()
            victim.wait(timeout=5)

    def test_a_healthy_long_running_pump_stays_healthy(self, project, data_root):
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            time.sleep(3.0)
            state = _with_data_root(data_root, load_state, project)
            assert state is not None and state.status == STATUS_RUNNING
            assert state.log_error == ""

            code, out, err = _cli(project, data_root, "probe")
            assert code == 0, (out, err)
            assert out["ok"] is True and out["log_error"] == ""
            assert out["runtime_status"] == STATUS_RUNNING
            assert _alive(app) and _alive(sup)
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)

    def test_a_pump_that_dies_during_the_probe_rejects_the_http_200(
        self, project, data_root, monkeypatch, capsys,
    ):
        """HTTP says 200; the pump is dead; the probe must still refuse."""
        code, served, err = _cli(project, data_root, "serve")
        assert code == 0, err
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            real = DS.http_probe

            def racing(url, timeout=3.0):
                status = real(url, timeout=timeout)
                state = _with_data_root(data_root, load_state, project)
                state.status = DS.STATUS_LOG_FAILED       # what the supervisor would do
                state.log_error = "injected persistent pump failure"
                _with_data_root(data_root, save_state, state)
                return status

            monkeypatch.setattr(DS, "http_probe", racing)
            monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
            with pytest.raises(SystemExit) as exc:
                runtime_cmd._cmd_runtime_probe(str(project), json_output=True)
            out = json.loads(capsys.readouterr().out)

            assert exc.value.code == 5
            assert out["ok"] is False
            assert out["status_code"] == 200, "the application really did answer"
            assert out["runtime_status"] == DS.STATUS_LOG_FAILED
            assert "injected persistent pump failure" in out["log_error"]
        finally:
            _cli(project, data_root, "stop")
            _kill(app, sup)


# ---------------------------------------------------------------------------
# Finding 2 — a `file:` URI is a local path wearing a scheme
# ---------------------------------------------------------------------------

class TestFileUriRedaction:
    def test_posix_file_uris_never_reach_shared_evidence(self):
        state = RuntimeState(
            identity_reason=("failed to open file:///home/alice/private/secret.txt "
                             "and file://localhost/home/alice/other.txt"),
            stop_error="see file:///home/alice/private%20folder/secret.txt",
        )
        payload = json.dumps(state.shareable())

        for private in ("/home/alice", "home/alice", "private folder", "localhost/home"):
            assert private not in payload, private
        assert "secret.txt" in payload, "a bare file name is not private"

    def test_windows_file_uris_never_reach_shared_evidence(self):
        state = RuntimeState(
            identity_reason="opened file:///C:/Users/Alice/private.txt",
            log_error="also file:///C:/Users/Alice/AppData/secret.ini",
        )
        payload = json.dumps(state.shareable())

        for private in ("C:/Users", "Users/Alice", "AppData"):
            assert private not in payload, private

    def test_unc_file_uris_never_reach_shared_evidence(self):
        state = RuntimeState(
            identity_reason=("file://server/share/private.txt and "
                             "file:////server/share/other.txt"),
        )
        payload = json.dumps(state.shareable())

        for private in ("server/share", "//server", "share/private"):
            assert private not in payload, private

    def test_http_and_https_urls_are_left_alone(self):
        state = RuntimeState(
            url="http://127.0.0.1:5173/health",
            log_error=("see https://example.test/docs/page and "
                       "http://localhost:8080/status"),
        )
        shared = state.shareable()
        payload = json.dumps(shared)

        assert shared["url"] == "http://127.0.0.1:5173/health"
        assert "https://example.test/docs/page" in payload
        assert "http://localhost:8080/status" in payload


class TestFileUriSchemeBoundary:
    """`file:` is only a scheme at a real token boundary.

    Matching any `file:` substring rewrote strings that are not file URIs at all:
    `profile:///home/alice/test.txt` came back as `protest.txt`. A scheme may only be
    preceded by a non-scheme character.
    """

    @pytest.mark.parametrize("text,expected", [
        ("file:///home/alice/x.txt", "x.txt"),
        ("prefix=file:///home/alice/x.txt", "prefix=x.txt"),
        ("(file:///home/alice/x.txt)", "(x.txt)"),
        ("FILE:///C:/Users/Alice/x.txt", "x.txt"),
        ("file://localhost/home/alice/x.txt", "x.txt"),
        ("file://server/share/x.txt", "x.txt"),
        ("file:////server/share/x.txt", "x.txt"),
        ("file:///home/alice/private%20folder/x.txt", "x.txt"),
    ])
    def test_a_real_file_uri_is_redacted(self, text, expected):
        assert DS._redact(text) == expected

    @pytest.mark.parametrize("text", [
        "profile:///home/alice/test.txt",
        "myfile://server/share/x.txt",
        "notafile:///home/alice/test.txt",
        "some.file:///home/alice/test.txt",
        "x-file:///home/alice/test.txt",
        "file2:///home/alice/test.txt",
    ])
    def test_a_string_that_is_not_a_file_uri_is_left_alone(self, text):
        assert DS._redact(text) == text

    def test_the_boundary_holds_inside_a_real_state(self):
        state = RuntimeState(
            identity_reason=("opened file:///home/alice/secret.txt but "
                             "profile:///home/alice/test.txt is not a file URI"),
            url="http://127.0.0.1:5173/health",
            log_error="https://example.test/docs stays as it is",
        )
        shared = state.shareable()
        payload = json.dumps(shared)

        assert "file:///home/alice/secret.txt" not in payload
        assert "secret.txt" in payload
        assert "profile:///home/alice/test.txt" in payload, "not a file URI: unchanged"
        assert shared["url"] == "http://127.0.0.1:5173/health"
        assert "https://example.test/docs" in payload


# ---------------------------------------------------------------------------
# Finding 1 — an EXACT terminal state survives the post-handshake race
# ---------------------------------------------------------------------------

class TestPostHandshakeTerminalState:
    """The supervisor can write a valid success handshake and, microseconds later,
    record exactly why the runtime is already over. The serve CLI used to answer
    "supervisor reported success but no verified running state exists" and DELETE that
    record — replacing a precise diagnosis with a shrug, and throwing away what a later
    probe and stop need. A known terminal state of THIS serve's own instance is now
    reported as it is, and kept.
    """

    @pytest.fixture
    def release(self, tmp_path) -> Path:
        return tmp_path / "release-the-pump-failure"

    def test_a_pump_failure_right_after_the_handshake_is_reported_exactly(
        self, project, data_root, release,
    ):
        code, out, err = _serve_with_broken_pump(
            project, data_root, PUMP_FAILS_IMMEDIATELY, release,
            parent=PARENT_WAITS_FOR_A_TERMINAL_STATE)

        assert code == 5, (out, err)
        assert out["ok"] is False and out["error_class"] == "state"
        assert out["runtime_status"] == DS.STATUS_LOG_FAILED, out
        assert "injected pump failure right after the handshake" in out["log_error"]
        assert out["stop_error"]
        assert out["survivors"] == [] and out["manual_cleanup"] == []
        assert "no verified running state" not in out["error"]

        # The diagnostic survives the CLI: that is what a later probe reads.
        state = _with_data_root(data_root, load_state, project)
        assert state is not None and state.status == DS.STATUS_LOG_FAILED
        assert state.log_error == out["log_error"]

        code, probe, err = _cli(project, data_root, "probe")
        assert code == 5, (probe, err)
        assert probe["runtime_status"] == DS.STATUS_LOG_FAILED
        assert probe["log_error"] == out["log_error"]

        # ...and an explicit stop clears it, idempotently.
        code, stopped, err = _cli(project, data_root, "stop")
        assert code == 0, (stopped, err)
        assert _with_data_root(data_root, load_state, project) is None
        assert _cli(project, data_root, "stop")[0] == 0

    def test_an_application_exit_right_after_the_handshake_is_reported_exactly(
        self, project, data_root, release,
    ):
        code, out, err = _serve_with_broken_pump(
            project, data_root, APP_EXITS_IMMEDIATELY, release,
            parent=PARENT_WAITS_FOR_A_TERMINAL_STATE)

        assert code == 5, (out, err)
        assert out["ok"] is False and out["error_class"] == "state"
        assert out["runtime_status"] == DS.STATUS_EXITED, out
        assert out["app_exit_code"] is not None
        assert out["survivors"] == []
        assert "no verified running state" not in out["error"]

        state = _with_data_root(data_root, load_state, project)
        assert state is not None and state.status == DS.STATUS_EXITED
        assert state.app_exit_code == out["app_exit_code"]

        assert _cli(project, data_root, "stop")[0] == 0
        assert _with_data_root(data_root, load_state, project) is None


# ---------------------------------------------------------------------------
# Cleanup hygiene — the emergency note lives and dies with the state it describes
# ---------------------------------------------------------------------------

class TestEmergencyNoteLifecycle:
    @pytest.fixture
    def release(self, tmp_path) -> Path:
        return tmp_path / "release-the-pump-failure"

    def test_the_note_lives_with_its_survivor_and_dies_with_the_record(
        self, project, data_root, release,
    ):
        code, served, err = _serve_with_broken_pump(
            project, data_root, PUMP_FAILURE_SURVIVOR_AND_UNWRITABLE_STATE, release)
        assert code == 0, err
        release.write_text("go\n")
        app, sup = served["pid"], served["supervisor_pid"]
        try:
            deadline = time.time() + 25
            while time.time() < deadline and _alive(sup):
                time.sleep(0.2)
            note = _with_data_root(data_root, DS.log_failure_note_path, project)

            # A survivor still depends on the record: both stay.
            assert _alive(app)
            assert _with_data_root(data_root, load_state, project) is not None
            assert note.is_file() and note.stat().st_mode & 0o777 == 0o600

            # The operator removes the survivor; the stop then clears record AND note.
            DS.stop_process_tree(app)
            assert _cli(project, data_root, "stop")[0] == 0
            assert _with_data_root(data_root, load_state, project) is None
            assert not note.exists(), "the note outlived the state it described"

            # ...and a fresh runtime never inherits an old note.
            note.write_text("{}\n")
            code, again, err = _cli(project, data_root, "serve")
            assert code == 0, err
            try:
                assert not note.exists(), "a new serve inherited a stale note"
            finally:
                _cli(project, data_root, "stop")
                _kill(again["pid"], again["supervisor_pid"])
        finally:
            _kill(app, sup)
