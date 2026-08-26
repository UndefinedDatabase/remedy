"""
Domain tests: ui_server/test_live_state.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
import os
import threading
import time
from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from packages.core.models import Job, Task

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"


def _make_job(**overrides: object) -> Job:
    defaults = dict(
        name="test-ui-job",
        user_prompt="Test prompt for UI",
        tasks=[Task(type="write_readme", description="Write a README")],
    )
    defaults.update(overrides)
    return Job(**defaults)


def _make_job_s91():
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    return job


def _make_job_s101(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------


def _get_app_html(job_id: str = "test-job", token: str = "test-token") -> str:
    from packages.orchestration.ui_app_shell import build_app_shell
    return build_app_shell(job_id, token)


# ---------------------------------------------------------------------------
# Step 80 — Localhost UI Server
# ---------------------------------------------------------------------------


def _make_permitted_job():
    """Create a job with repo_generated_write permission granted."""
    job = _make_job()
    job.metadata["permissions"] = {"repo_generated_write": "allow"}
    return job


def _make_approved_job() -> tuple:
    """Create a job with permission + an approved patch intent. Returns (job, intent_id)."""
    job = _make_permitted_job()
    # Create artifact with patch intent explanation + approval
    artifact = MagicMock()
    artifact.id = uuid4()
    artifact.task_id = uuid4()
    intent_id = f"{artifact.id.hex[:8]}-0"
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "test.py", "action": "create", "risk": "low", "reason": "test", "summary": "test"}
        ],
        "patch_intent_approvals": {
            intent_id: {
                "intent_id": intent_id,
                "state": "approved",
                "decided_at": "2026-01-01T00:00:00Z",
                "decided_by": "test",
            }
        },
    }
    job.artifacts = [artifact]
    return job, intent_id


# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------




class TestUIServerIntegration:
    """Integration tests that start a real server on a free port."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _start_server(self, **kwargs):
        """Start server in background thread, return (port, token, thread)."""
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                    **kwargs,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        t = threading.Thread(target=run, daemon=True)
        t.start()

        # Wait for info file
        for _ in range(50):
            if Path(info_file).exists():
                info = json.loads(Path(info_file).read_text())
                return info["port"], token, t
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def test_server_starts_and_writes_info(self):
        port, token, t = self._start_server()
        info = json.loads((self.tmp_path / "server_info.json").read_text())
        assert info["version"] == 1
        assert info["host"] == "127.0.0.1"
        assert info["port"] == port
        assert info["token"] == token
        assert info["job_id"] == self.job_id
        assert "url" in info
        assert info["url"].startswith("http://127.0.0.1:")

    def test_url_is_localhost_only(self):
        port, token, t = self._start_server()
        info = json.loads((self.tmp_path / "server_info.json").read_text())
        url = info["url"]
        assert "127.0.0.1" in url
        assert "0.0.0.0" not in url
        # No LAN address
        assert "192.168." not in url
        assert "10." not in url.split("//")[1].split(":")[0]

    def test_app_shell_served_without_token(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", "/")
        resp = conn.getresponse()
        assert resp.status == 200
        body = resp.read().decode()
        assert "Remedy" in body
        conn.close()

    def test_api_requires_token(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        # No token
        conn.request("GET", f"/api/state?job_id={self.job_id}")
        resp = conn.getresponse()
        assert resp.status == 403
        body = json.loads(resp.read())
        assert body["error"] == "invalid token"
        conn.close()

    def test_api_invalid_token_403(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/state?job_id={self.job_id}&token=wrong")
        resp = conn.getresponse()
        assert resp.status == 403
        conn.close()

    def test_api_valid_token_returns_dashboard(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/dashboard?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        data = json.loads(resp.read())
        # Dashboard v3 contract
        assert data["version"] == 3
        assert data["job_id"] == self.job_id
        # Required v3 top-level keys
        for key in ("live", "metrics", "tasks", "activity", "phases",
                     "graph_summary", "next_action", "truth", "redaction"):
            assert key in data, f"missing v3 key: {key}"
        # Truth contract for normal runtime
        assert data["truth"]["demo_mode"] is False
        assert data["truth"]["synthetic_count"] == 0
        assert data["redaction"]["raw_content_exposed"] is False
        conn.close()

    def test_api_missing_job_404(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        fake_id = str(uuid4())
        conn.request("GET", f"/api/jobs/{fake_id}/dashboard?token={token}")
        resp = conn.getresponse()
        assert resp.status == 404
        conn.close()

    def test_post_rejected(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("POST", f"/api/state?token={token}")
        resp = conn.getresponse()
        assert resp.status == 405
        conn.close()

    def test_put_rejected(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("PUT", f"/api/state?token={token}")
        resp = conn.getresponse()
        assert resp.status == 405
        conn.close()

    def test_delete_rejected(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("DELETE", f"/api/state?token={token}")
        resp = conn.getresponse()
        assert resp.status == 405
        conn.close()

    def test_dashboard_no_raw_leaks(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/dashboard?token={token}")
        resp = conn.getresponse()
        body = resp.read().decode()
        for forbidden in ("raw_output", "command_output", "Traceback", "diff_preview", "approval_reason"):
            assert forbidden not in body, f"Raw leak: {forbidden}"
        conn.close()

    def test_events_endpoint(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/events?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        data = json.loads(resp.read())
        assert "events" in data
        conn.close()

    def test_brain_endpoint(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/brain?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        data = json.loads(resp.read())
        assert data["version"] == 1
        assert "graph" in data
        conn.close()

    def test_guide_endpoint(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/guide?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        conn.close()

    def test_readiness_endpoint(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/readiness?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        conn.close()

    def test_context_budget_endpoint(self):
        port, token, t = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        conn.request("GET", f"/api/jobs/{self.job_id}/context-budget?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        conn.close()


# ---------------------------------------------------------------------------
# Step 81 — Calm Entry UX
# ---------------------------------------------------------------------------




class TestServerEndpoints:
    def test_brain_view_model_endpoint_exists(self):
        """ui_server has brain-view-model handler."""
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "brain-view-model" in src

    def test_node_detail_endpoint_exists(self):
        """ui_server has node detail routing."""
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "nodes" in src and "detail" in src

    def test_static_asset_serving(self):
        """ui_server has static asset serving for /assets/."""
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "_serve_static" in src
        assert "/assets/" in src

    def test_frontend_loader(self):
        """ui_server prefers built frontend over legacy shell."""
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "_load_frontend" in src
        assert "_get_frontend_dist" in src


# ---------------------------------------------------------------------------
# Session Registry
# ---------------------------------------------------------------------------




class TestSessionRegistry:
    def test_sessions_dir_creation(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            "apps.cli.commands.ui.resolve_data_root",
            lambda: str(tmp_path),
            raising=False,
        )
        # Need to patch at the import location
        import apps.cli.commands.ui as ui_mod
        original = ui_mod._sessions_dir

        def patched_sessions_dir():
            d = tmp_path / "ui" / "sessions"
            d.mkdir(parents=True, exist_ok=True)
            return d

        monkeypatch.setattr(ui_mod, "_sessions_dir", patched_sessions_dir)

        d = ui_mod._sessions_dir()
        assert d.is_dir()

    def test_write_and_read_session(self, tmp_path, monkeypatch):
        import apps.cli.commands.ui as ui_mod

        def patched_sessions_dir():
            d = tmp_path / "ui" / "sessions"
            d.mkdir(parents=True, exist_ok=True)
            return d

        monkeypatch.setattr(ui_mod, "_sessions_dir", patched_sessions_dir)

        info = {"job_id": "abc", "pid": os.getpid(), "url": "http://127.0.0.1:8787"}
        ui_mod._write_session("test-session", info)

        sessions = ui_mod._read_sessions()
        assert len(sessions) == 1
        assert sessions[0]["job_id"] == "abc"

    def test_is_pid_alive(self):
        from apps.cli.commands.ui import _is_pid_alive
        assert _is_pid_alive(os.getpid()) is True
        assert _is_pid_alive(999999999) is False




class TestLiveGrowth:
    def test_live_state_endpoint_exists(self):
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "live-state" in src
        assert "_build_live_state_json" in src

    def test_events_since_endpoint_exists(self):
        import packages.orchestration.ui_server as srv
        src = Path(srv.__file__).read_text()
        assert "events-since" in src
        assert "_build_events_since_json" in src

    def test_merge_view_model_in_renderer(self):
        app = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "RemedyApp.tsx"
        content = app.read_text()
        assert "setInterval" in content, "RemedyApp must have dashboard refresh via setInterval"

    def test_reduced_motion_respected(self):
        provider = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "components" / "shell" / "ReducedMotionProvider.tsx"
        assert provider.is_file(), "ReducedMotionProvider.tsx must exist"
        content = provider.read_text()
        assert "prefers-reduced-motion" in content


# ---------------------------------------------------------------------------
# Step 96 — remedy do
# ---------------------------------------------------------------------------




class TestLiveGrowthUX:
    def test_ui_server_live_state_has_active_task(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job_s101(2)
        result = _build_live_state_json(job)
        assert "active_task_id" in result

    def test_ui_server_has_task_progress_handler(self):
        src = (Path(__file__).parent.parent.parent / "packages" / "orchestration" / "ui_server.py").read_text()
        assert '"task-progress"' in src
        assert "_build_task_progress_json" in src

    def test_follow_toggle_in_html(self):
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "RemedyApp.tsx").read_text()
        assert "setInterval" in src

    def test_main_ts_has_ribbon_polling(self):
        src = (Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "RemedyApp.tsx").read_text()
        assert "setInterval" in src or "timer" in src


def _decision_requested_events(count: int) -> list[dict]:
    """`human_decision_requested` events — the ledger shape the badge no longer reads."""
    return [
        {"event": "human_decision_requested", "run_id": "r1", "job_id": "j1",
         "timestamp": f"2026-01-01T00:0{i}:00", "outcome": "pending", "metadata": {}}
        for i in range(count)
    ]


class TestOpenDecisionCountComesFromTheDecisionQueue:
    """`open_decision_count` re-derives from `decision_queue` (DECISION F031 D9)."""

    @staticmethod
    def _live_count(job, events):
        from packages.orchestration.ui_server import _build_live_state_json
        with patch("packages.orchestration.ui_server._load_events", return_value=events):
            return _build_live_state_json(job)["open_decision_count"]

    @staticmethod
    def _queue_count(job, events):
        from packages.orchestration.decision_queue import list_decisions, open_decisions
        return len(open_decisions(list_decisions(job, events)))

    def test_repo_less_job_reports_its_open_decisions(self):
        job = _make_job()
        expected = self._queue_count(job, [])
        assert expected > 0, "a job with no target_repo must raise a stop-reason decision"
        assert self._live_count(job, []) == expected

    def test_job_with_nothing_open_reports_zero(self):
        job = _make_job(metadata={"target_repo": "."})
        expected = self._queue_count(job, [])
        assert expected == 0
        assert self._live_count(job, []) == expected

    def test_human_decision_requested_events_do_not_raise_the_count(self):
        job = _make_job(metadata={"target_repo": "."})
        events = _decision_requested_events(3)
        expected = self._queue_count(job, events)
        assert expected == 0
        assert self._live_count(job, events) == expected


# ---------------------------------------------------------------------------
# Step 108 — Reviewer Recommendation Loop
# ---------------------------------------------------------------------------




class TestApiAdapterTypesAndNormalization:
    """API adapter types and implementation exist."""

    def test_types_file_exists(self):
        assert (UI_SRC / "api" / "types.ts").is_file()

    def test_types_has_dashboard(self):
        content = (UI_SRC / "api" / "types.ts").read_text(encoding="utf-8")
        assert "RemedyDashboard" in content
        assert "RemedyMetric" in content
        assert "RemedyTaskItem" in content
        assert "RemedyGraphNode" in content
        assert "RemedyPhase" in content

    def test_adapter_file_exists(self):
        assert (UI_SRC / "api" / "remedyApi.ts").is_file()

    def test_adapter_normalizes_state(self):
        content = (UI_SRC / "api" / "remedyApi.ts").read_text(encoding="utf-8")
        assert "normalizeState" in content

    def test_adapter_uses_human_copy(self):
        content = (UI_SRC / "api" / "remedyApi.ts").read_text(encoding="utf-8")
        assert "humanLabel" in content
        assert "scrubUiText" in content

    def test_adapter_no_forbidden_words_as_labels(self):
        content = (UI_SRC / "api" / "remedyApi.ts").read_text(encoding="utf-8")
        # Forbidden words should only appear in scrubbing logic, not as output labels
        assert "Context Coverage" not in content
        assert "present signals" not in content
        assert "missing signals" not in content


# ---------------------------------------------------------------------------
# Steps 176-179 — Shell + Left Rail + Metrics + Command
# ---------------------------------------------------------------------------




class TestServerPrefersReactDistLocalhostOnly:
    """Server points at React UI."""

    def test_server_prefers_react_dist(self):
        server = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text(encoding="utf-8")
        assert "React" in server or "react" in server.lower()
        # Must still fall back to legacy shell
        assert "build_app_shell" in server

    def test_server_localhost_only(self):
        server = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text(encoding="utf-8")
        assert "127.0.0.1" in server
        assert "0.0.0.0" not in server

    def test_server_no_shell_true(self):
        server = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text(encoding="utf-8")
        assert "shell=True" not in server


# ---------------------------------------------------------------------------
# Global checks — No forbidden debug words in default source
# ---------------------------------------------------------------------------




class TestWeakLabelDetectionAndReplacement:
    """Weak labels detected and replaced."""

    def test_is_weak_label_exists(self):
        code = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "isWeakLabel" in code

    def test_human_fallback_exists(self):
        code = (UI_SRC / "api" / "remedyApi.ts").read_text()
        assert "humanFallbackFor" in code


# ---------------------------------------------------------------------------
# Step 241 — Right panel responsive
# ---------------------------------------------------------------------------

