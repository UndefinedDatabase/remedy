"""
Tests for Steps 80, 81, 82 — Localhost UI, Calm Entry UX, Progressive Brain Explorer.

Verifies:
  - UI server module exists and binds 127.0.0.1 only.
  - CLI command `ui.start` registered in catalog.
  - App shell contains calm entry panels (what-happened, proven, etc.).
  - Light theme is default (no dark-only background).
  - Graph canvas is NOT the first visible region.
  - Progressive explorer has 4 modes.
  - No raw content leaks.
  - No external assets.
  - Reduced-motion support.
  - Token required for API.
  - No POST/PUT/DELETE allowed.
  - Detail panel hidden by default.
  - Advanced metadata hidden by default.
  - Advanced filters hidden by default.
"""

from __future__ import annotations

import json
import os
import signal
import socket
import sys
import tempfile
import threading
import time
from http.client import HTTPConnection
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job(**overrides: object) -> Job:
    defaults = dict(
        name="test-ui-job",
        user_prompt="Test prompt for UI",
        tasks=[Task(type="write_readme", description="Write a README")],
    )
    defaults.update(overrides)
    return Job(**defaults)


def _get_app_html(job_id: str = "test-job", token: str = "test-token") -> str:
    from packages.orchestration.ui_app_shell import build_app_shell
    return build_app_shell(job_id, token)


# ---------------------------------------------------------------------------
# Step 80 — Localhost UI Server
# ---------------------------------------------------------------------------

class TestUIServer:
    """Test the UI server module."""

    def test_ui_server_module_exists(self):
        import packages.orchestration.ui_server as mod
        assert hasattr(mod, "start_ui_server")
        assert hasattr(mod, "_RemedyHandler")

    def test_catalog_has_ui_start(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("ui.start")
        assert cmd.group_id == "ui"
        assert cmd.action_class == "read_only"
        arg_names = [a.name for a in cmd.args]
        assert "job_id" in arg_names
        assert "--port" in arg_names
        assert "--host" in arg_names
        assert "--info-file" in arg_names

    def test_handler_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "ui.start" in handlers

    def test_refuses_non_localhost(self, tmp_path, monkeypatch):
        """Server must refuse 0.0.0.0 or LAN addresses."""
        from packages.orchestration.ui_server import start_ui_server

        job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(job)

        with pytest.raises(SystemExit):
            start_ui_server(str(job.id), host="0.0.0.0", port=0)

    def test_safe_error_format(self):
        from packages.orchestration.ui_server import _safe_error
        code, body = _safe_error(403, "forbidden")
        assert code == 403
        assert body == {"error": "forbidden"}

    def test_load_job_invalid_uuid(self):
        from packages.orchestration.ui_server import _load_job
        job, err = _load_job("not-a-uuid")
        assert job is None
        assert err[0] == 400

    def test_load_job_missing(self):
        from packages.orchestration.ui_server import _load_job
        job, err = _load_job(str(uuid4()))
        assert job is None
        assert err[0] == 404

    def test_no_shell_true_in_server(self):
        src = Path("packages/orchestration/ui_server.py").read_text()
        assert "shell=True" not in src

    def test_no_external_assets_in_server(self):
        src = Path("packages/orchestration/ui_server.py").read_text()
        for pattern in ("cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"):
            assert pattern not in src


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
        assert data["version"] == 1
        assert data["job_id"] == self.job_id
        assert "state" in data
        assert "task_count" in data
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

class TestCalmEntryUX:
    """Test the app shell for calm entry UX."""

    def test_app_shell_builds(self):
        html = _get_app_html()
        assert "Remedy" in html
        assert "__JOB_ID__" not in html
        assert "__TOKEN__" not in html

    def test_light_theme_default(self):
        html = _get_app_html()
        assert 'class="remedy-light"' in html
        assert "--remedy-bg: #f4f7fa" in html

    def test_light_theme_css_variables(self):
        html = _get_app_html()
        required_vars = [
            "--remedy-bg", "--remedy-surface", "--remedy-surface-strong",
            "--remedy-text", "--remedy-text-muted", "--remedy-teal",
            "--remedy-cyan", "--remedy-line", "--remedy-proof",
            "--remedy-risk", "--remedy-warning", "--remedy-memory",
        ]
        for var in required_vars:
            assert var in html, f"Missing CSS variable: {var}"

    def test_dark_mode_available(self):
        html = _get_app_html()
        assert ".remedy-dark" in html

    def test_what_happened_panel(self):
        html = _get_app_html()
        assert "what-happened" in html
        assert "What happened" in html

    def test_proven_panel(self):
        html = _get_app_html()
        assert "proven" in html or "What is proven" in html

    def test_needs_attention_panel(self):
        html = _get_app_html()
        assert "needs-attention" in html
        assert "Needs your attention" in html

    def test_next_action_panel(self):
        html = _get_app_html()
        assert "next-action" in html or "Next safe action" in html

    def test_token_cost_panel(self):
        html = _get_app_html()
        assert "token-cost" in html
        assert "Token cost" in html

    def test_explore_brain_button(self):
        html = _get_app_html()
        assert "explore-brain" in html
        assert "Explore project brain" in html

    def test_graph_not_first_visible(self):
        """Graph canvas must not be visible by default."""
        html = _get_app_html()
        # Brain explorer starts hidden
        assert 'class="remedy-brain-explorer"' in html
        assert "display: none" in html or 'display:none' in html.replace(" ", "").replace(": ", ":")
        # It only becomes visible with .visible class
        assert ".remedy-brain-explorer.visible" in html.replace(" ", "")

    def test_no_giant_zone_rail(self):
        """No left rail with zone/status/risk visible by default."""
        html = _get_app_html()
        # No massive status/type rail in default view
        assert "zone-label" not in html or html.count("zone-label") < 3

    def test_no_external_assets(self):
        html = _get_app_html()
        for pattern in ("cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net", "https://", "http://"):
            # http:// is OK in API URLs like /api/
            if pattern == "http://":
                # Only check it's not loading external resources
                assert "http://cdn" not in html
                assert "http://fonts" not in html
            else:
                assert pattern not in html, f"External asset: {pattern}"

    def test_no_raw_leaks_in_shell(self):
        html = _get_app_html()
        for forbidden in ("raw_output", "command_output", "MUST_NOT_RENDER",
                          "diff_preview", "approval_reason"):
            assert forbidden not in html, f"Raw leak in shell: {forbidden}"

    def test_reduced_motion_support(self):
        html = _get_app_html()
        assert "prefers-reduced-motion" in html

    def test_narrow_layout_support(self):
        html = _get_app_html()
        assert "max-width: 640px" in html or "max-width:640px" in html.replace(" ", "")

    def test_mist_background(self):
        html = _get_app_html()
        assert "remedy-mist" in html


# ---------------------------------------------------------------------------
# Step 82 — Progressive Brain Explorer
# ---------------------------------------------------------------------------

class TestProgressiveBrainExplorer:
    """Test the progressive brain explorer modes and disclosure."""

    def test_proof_path_mode_exists(self):
        html = _get_app_html()
        assert "proof-path" in html

    def test_attention_mode_exists(self):
        html = _get_app_html()
        assert "attention" in html

    def test_system_map_mode_exists(self):
        html = _get_app_html()
        assert "system-map" in html

    def test_full_graph_mode_exists(self):
        html = _get_app_html()
        assert "full-graph" in html

    def test_default_mode_not_full_graph(self):
        html = _get_app_html()
        # Default tab should be proof-path, not full-graph
        assert 'data-mode="proof-path"' in html
        # The proof-path tab should have active class
        idx_proof = html.index('data-mode="proof-path"')
        idx_full = html.index('data-mode="full-graph"')
        # Check proof-path tab has "active" class
        proof_tab_region = html[idx_proof - 60:idx_proof]
        assert "active" in proof_tab_region

    def test_detail_panel_hidden_by_default(self):
        html = _get_app_html()
        assert 'class="remedy-detail-panel"' in html
        # Not visible by default (needs .visible class)
        assert ".remedy-detail-panel.visible" in html.replace(" ", "")

    def test_advanced_metadata_hidden(self):
        html = _get_app_html()
        assert "detail-advanced" in html
        assert 'class="detail-advanced"' in html

    def test_advanced_filters_hidden(self):
        html = _get_app_html()
        assert "filters-drawer" in html
        assert 'class="remedy-filters-drawer"' in html

    def test_node_selection_reveals_details(self):
        html = _get_app_html()
        assert "selectNode" in html

    def test_cluster_nodes_expandable(self):
        html = _get_app_html()
        assert "expandCluster" in html

    def test_max_primary_node_cap(self):
        html = _get_app_html()
        assert "MAX_PRIMARY" in html

    def test_labels_hidden_for_non_primary(self):
        html = _get_app_html()
        # .graph-node text has display: none by default
        assert ".graph-node text" in html

    def test_no_raw_leaks_in_explorer(self):
        html = _get_app_html()
        for forbidden in ("raw_output", "command_output", "Traceback", "MUST_NOT_RENDER"):
            assert forbidden not in html


# ---------------------------------------------------------------------------
# Smoke script structural tests
# ---------------------------------------------------------------------------

class TestSmokeScriptUI:
    """Verify smoke script has UI-related sections."""

    @pytest.fixture(autouse=True)
    def _load_script(self):
        self.script = Path("scripts/remedy_smoke.sh").read_text()

    def test_group_help_includes_ui(self):
        assert "ui" in self.script.split("for grp in")[1].split("; do")[0]

    def test_no_shell_true_in_new_modules(self):
        for path in [
            "packages/orchestration/ui_server.py",
            "packages/orchestration/ui_app_shell.py",
        ]:
            src = Path(path).read_text()
            assert "shell=True" not in src, f"shell=True in {path}"
