"""F007 T002 — the `remedy runtime` CLI: catalog, parser, handlers, exit codes.

Real dummy servers as subprocesses; no provider call, no network install.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import psutil
import pytest

from apps.cli.command_catalog import CATALOG, GROUPS, get_commands_for_group
from apps.cli.commands import collect_all_handlers, runtime_cmd
from packages.runtimes.dev_server import load_state

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

NEVER = """
import time
print("never ready", flush=True)
while True: time.sleep(0.2)
"""


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _project(tmp_path: Path, script: str, body: str, *, timeout: float = 15.0,
             port: int = 5173) -> Path:
    root = tmp_path / "proj"
    root.mkdir(exist_ok=True)
    (root / script).write_text(body)
    cfg = root / ".remedy"
    cfg.mkdir(exist_ok=True)
    (cfg / "config.toml").write_text(
        "[runtime]\n"
        f'cmd = ["{sys.executable}", "{script}"]\n'
        'cwd = "."\n'
        f"port = {port}\n"
        'health_path = "/"\n'
        f"ready_timeout_s = {timeout}\n"
    )
    return root


def _alive(pid: int) -> bool:
    try:
        p = psutil.Process(pid)
        return p.is_running() and p.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


# ---------------------------------------------------------------------------
# Catalog and parser
# ---------------------------------------------------------------------------

class TestCatalog:
    def test_the_runtime_group_exists(self):
        assert "runtime" in GROUPS
        subs = {c.subcommand for c in get_commands_for_group("runtime")}
        assert subs == {"serve", "probe", "stop"}

    def test_every_runtime_command_has_repo_and_json(self):
        for entry in get_commands_for_group("runtime"):
            names = {a.name for a in entry.args}
            assert "--repo" in names and "--json" in names
            assert entry.supports_json is True
            assert entry.may_mutate_repo is False

    def test_handlers_are_registered(self):
        handlers = collect_all_handlers()
        for cid in ("runtime.serve", "runtime.probe", "runtime.stop"):
            assert cid in handlers
            assert cid in {c.command_id for c in CATALOG}

    def test_the_cli_parser_exposes_the_group(self):
        from apps.cli.grouped import build_parser
        parser = build_parser()
        args = parser.parse_args(["runtime", "probe", "--repo", ".", "--json"])
        assert args.repo == "." and args.json is True


# ---------------------------------------------------------------------------
# serve / probe / stop
# ---------------------------------------------------------------------------

class TestServe:
    def test_serve_starts_and_leaves_the_server_running(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        out = json.loads(capsys.readouterr().out)
        try:
            assert out["ok"] is True and out["status"] == "running"
            assert out["port"] > 0 and out["url"].startswith("http://127.0.0.1:")
            assert _alive(out["pid"])
            assert Path(out["log_path"]).is_file()
            assert load_state(root).pid == out["pid"]
        finally:
            runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
            capsys.readouterr()
        assert not _alive(out["pid"])

    def test_serve_twice_returns_the_same_runtime(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        first = json.loads(capsys.readouterr().out)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        second = json.loads(capsys.readouterr().out)
        try:
            assert second["already_running"] is True
            assert second["pid"] == first["pid"] and second["port"] == first["port"]
        finally:
            runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
            capsys.readouterr()

    def test_a_readiness_timeout_exits_4_and_leaves_no_state(self, tmp_path, capsys):
        """The FAST contract of a readiness timeout: the exit code, the error class, no
        state, nothing left running.

        It deliberately does NOT assert on the log tail. With a 1.5 s deadline the child
        interpreter may not have printed its first line yet — the tail was empty in four
        of five external runs — and a test that asserts a line that need not exist yet is
        testing the machine's speed, not the runtime. The log tail is proven separately,
        against an observable marker the child writes AFTER its line
        (`tests/runtimes/test_runtime_cli_process_boundary.py`).
        """
        root = _project(tmp_path, "never.py", NEVER, timeout=1.5)
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_READY
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is False and out["error_class"] == "ready"
        assert load_state(root) is None
        assert not out.get("survivors")

    def test_a_missing_runtime_exits_2(self, tmp_path, capsys):
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_serve(str(empty), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_CONFIG
        out = json.loads(capsys.readouterr().out)
        assert out["error_class"] == "config"


class TestProbe:
    def test_a_one_shot_probe_starts_stops_and_leaves_nothing(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_probe(str(root), json_output=True)
        out = json.loads(capsys.readouterr().out)

        assert out["ok"] is True and out["status_code"] == 200
        assert out["stopped"] is True and out["managed_by_serve"] is False
        assert out["port"] > 0
        assert not _alive(out["pid"])                 # no process left behind
        assert load_state(root) is None               # no stale state left behind

    def test_a_second_probe_runs_cleanly(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_probe(str(root), json_output=True)
        first = json.loads(capsys.readouterr().out)
        runtime_cmd._cmd_runtime_probe(str(root), json_output=True)
        second = json.loads(capsys.readouterr().out)
        assert first["ok"] and second["ok"]
        assert not _alive(second["pid"])

    def test_probing_a_served_runtime_does_not_stop_it(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        served = json.loads(capsys.readouterr().out)
        try:
            runtime_cmd._cmd_runtime_probe(str(root), json_output=True)
            out = json.loads(capsys.readouterr().out)
            assert out["ok"] is True and out["managed_by_serve"] is True
            assert out["stopped"] is False
            assert _alive(served["pid"])              # still running
        finally:
            runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
            capsys.readouterr()

    def test_a_probe_timeout_exits_4(self, tmp_path, capsys):
        root = _project(tmp_path, "never.py", NEVER, timeout=1.5)
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_probe(str(root), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_READY
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is False and out["stopped"] is True
        assert load_state(root) is None

    def test_a_missing_runtime_exits_2(self, tmp_path, capsys):
        empty = tmp_path / "empty2"
        empty.mkdir()
        with pytest.raises(SystemExit) as exc:
            runtime_cmd._cmd_runtime_probe(str(empty), json_output=True)
        assert exc.value.code == runtime_cmd.EXIT_CONFIG


class TestStop:
    def test_stop_removes_the_process_and_the_state(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_serve(str(root), json_output=True)
        served = json.loads(capsys.readouterr().out)

        runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
        out = json.loads(capsys.readouterr().out)

        assert out["stopped"] is True and out["identity_ok"] is True
        assert not _alive(served["pid"])
        assert load_state(root) is None

    def test_stop_is_idempotent(self, tmp_path, capsys):
        root = _project(tmp_path, "server.py", SERVER)
        runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
        out = json.loads(capsys.readouterr().out)
        assert out["ok"] is True and out["stopped"] is False

    def test_stop_never_kills_a_reused_pid(self, tmp_path, capsys):
        import subprocess
        import time

        from packages.runtimes.dev_server import RuntimeState, project_digest, save_state

        root = _project(tmp_path, "server.py", SERVER)
        victim = subprocess.Popen(
            [sys.executable, "-c", "import time\nwhile True: time.sleep(0.2)"])
        try:
            save_state(RuntimeState(
                pid=victim.pid, create_time=time.time() - 9999, port=1234,
                status="running", project_root=str(root),
                project_id=project_digest(root),
            ))
            runtime_cmd._cmd_runtime_stop(str(root), json_output=True)
            out = json.loads(capsys.readouterr().out)

            assert out["stopped"] is False and out["identity_ok"] is False
            assert "reused" in out["reason"]
            assert _alive(victim.pid)                 # the innocent process lives
            assert load_state(root) is None
        finally:
            victim.kill()
            victim.wait()
