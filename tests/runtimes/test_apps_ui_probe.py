"""F007 T003 — the runtime harness against the REAL apps/ui Vite dev server.

Selectable on its own:

    python3 -m pytest -q -m subprocess tests/runtimes/test_apps_ui_probe.py

No `npm install` and no network access: the test uses the dependencies already
installed in apps/ui/node_modules. If they are absent the test reports that concrete
integration blocker instead of quietly substituting a fake server.
"""
from __future__ import annotations

import json
from pathlib import Path

import psutil
import pytest

from apps.cli.commands import runtime_cmd
from packages.runtimes import dev_server as DS
from packages.runtimes.dev_server import DevServer, load_state
from packages.runtimes.runtime_config import detect_runtimes, resolve_spec

pytestmark = [pytest.mark.subprocess, pytest.mark.slow]

REPO = Path(__file__).resolve().parents[2]
UI = REPO / "apps" / "ui"

_missing_deps = not (UI / "node_modules" / ".bin" / "vite").exists()
requires_ui_deps = pytest.mark.skipif(
    _missing_deps,
    reason=(
        "INTEGRATION BLOCKER: apps/ui dependencies are not installed "
        "(apps/ui/node_modules/.bin/vite is missing). Install them once, outside "
        "the test run — this test must never run npm install itself."
    ),
)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _alive(pid: int) -> bool:
    try:
        proc = psutil.Process(pid)
        return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def _vite_spec():
    """The detected Vite runtime for THIS repository's apps/ui."""
    detected = [d for d in detect_runtimes(REPO) if d.kind == "vite"]
    assert detected, "apps/ui must be detected as a vite runtime"
    spec = detected[0].spec
    assert Path(spec.cwd) == UI
    return spec


class TestDetectApsUi:
    def test_the_real_apps_ui_is_detected_as_vite(self):
        spec = _vite_spec()
        assert spec.source == "detected:vite"
        assert "{port}" in spec.cmd
        assert spec.cmd[0] in ("npm", "pnpm", "yarn")
        assert spec.health_path == "/"

    def test_the_repository_itself_resolves_a_runtime(self):
        # apps/ui is the only node app here, so resolution is unambiguous.
        spec = resolve_spec(REPO)
        assert Path(spec.cwd) == UI


@requires_ui_deps
class TestRealViteProbe:
    def test_the_harness_starts_apps_ui_and_becomes_ready(self, tmp_path):
        spec = _vite_spec()
        server = DevServer(spec, REPO)
        state = server.start()
        try:
            result = server.wait_ready()

            assert result.ok, f"apps/ui never became ready: {result.error}\n{result.log_tail}"
            assert result.status_code == 200
            assert result.port == state.port > 0          # the EFFECTIVE port
            assert state.url.startswith(f"http://127.0.0.1:{state.port}")
            logs = server.logs()
            assert logs.strip(), "runtime logs must exist"
            assert Path(state.log_path).is_file()
        finally:
            server.stop()

        assert not _alive(state.pid)
        assert load_state(REPO) is None

    def test_a_one_shot_probe_leaves_no_process_and_no_state(self, capsys):
        runtime_cmd._cmd_runtime_probe(str(REPO), json_output=True)
        out = json.loads(capsys.readouterr().out)

        assert out["ok"] is True and out["status_code"] == 200
        assert out["stopped"] is True and out["managed_by_serve"] is False
        assert out["port"] > 0
        assert not _alive(out["pid"])                      # process tree is gone
        assert load_state(REPO) is None                    # no stale state

    def test_a_second_probe_runs_cleanly(self, capsys):
        runtime_cmd._cmd_runtime_probe(str(REPO), json_output=True)
        first = json.loads(capsys.readouterr().out)
        runtime_cmd._cmd_runtime_probe(str(REPO), json_output=True)
        second = json.loads(capsys.readouterr().out)

        assert first["ok"] and second["ok"]
        assert not _alive(first["pid"]) and not _alive(second["pid"])
        assert load_state(REPO) is None

    def test_serve_then_stop_removes_the_whole_vite_process_tree(self, capsys):
        runtime_cmd._cmd_runtime_serve(str(REPO), json_output=True)
        served = json.loads(capsys.readouterr().out)
        try:
            assert served["ok"] and _alive(served["pid"])
            kids = [c.pid for c in psutil.Process(served["pid"]).children(recursive=True)]
        finally:
            runtime_cmd._cmd_runtime_stop(str(REPO), json_output=True)
            stopped = json.loads(capsys.readouterr().out)

        assert stopped["stopped"] is True and stopped["survivors"] == []
        assert not _alive(served["pid"])
        for pid in kids:
            assert not _alive(pid), f"vite child {pid} survived the stop"
        assert load_state(REPO) is None


@requires_ui_deps
class TestRealViteAcrossTheCliBoundary:
    """The real product command, in its own process, against the real Vite server."""

    def _cli(self, data_root, *args, timeout=180.0):
        import os
        import subprocess
        import sys

        env = dict(os.environ)
        env["REMEDY_DATA_DIR"] = str(data_root)
        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "runtime", *args,
             "--repo", str(REPO), "--json"],
            cwd=str(REPO), env=env, capture_output=True, text=True, timeout=timeout,
        )
        payload = {}
        if proc.stdout.strip():
            import contextlib as _c
            with _c.suppress(ValueError):
                payload = json.loads(proc.stdout)
        return proc.returncode, payload, proc.stderr

    def test_vite_survives_the_serve_cli_and_is_probed_and_stopped_separately(
        self, tmp_path,
    ):
        import time

        data_root = tmp_path / "remedy_data"
        data_root.mkdir()

        code, served, err = self._cli(data_root, "serve")
        try:
            assert code == 0, err
            app, sup = served["pid"], served["supervisor_pid"]
            assert app and sup and app != sup

            # The serve CLI has exited. Vite must still be serving.
            time.sleep(3.0)
            assert _alive(sup) and _alive(app)
            status, _err = DS.http_probe(served["url"], timeout=5.0)
            assert status == 200, "Vite died when the serve CLI exited"

            code, probed, err = self._cli(data_root, "probe")
            assert code == 0, err
            assert probed["ok"] is True and probed["stopped"] is False
            assert _alive(app), "the probe must not stop a served runtime"

            code, stopped, err = self._cli(data_root, "stop")
            assert code == 0, err
            assert stopped["stopped"] is True and stopped["survivors"] == []
            assert not _alive(app) and not _alive(sup)
        finally:
            for pid in (served.get("pid"), served.get("supervisor_pid")):
                if pid and _alive(pid):
                    DS.stop_process_tree(pid)
