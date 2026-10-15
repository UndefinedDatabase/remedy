"""
Domain tests: ui_contracts/test_responsive.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry


def _make_job(**overrides) -> JobPlan:
    defaults = {
        "job_id": str(uuid4()),
        "job_title": "test-job",
        "user_prompt": "test prompt",
        "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return JobPlan(**defaults)


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────


def _make_job_s74(**overrides) -> JobPlan:
    defaults = {
        "job_id": str(uuid4()),
        "job_title": "test-job",
        "user_prompt": "test prompt",
        "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return JobPlan(**defaults)


def _get_viewer_html():
    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain

    job = _make_job()
    events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.job_id),
                "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
    graph = build_project_brain(job, events)
    data = build_brain_viewer_data(job, graph, events)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        html_path = write_brain_viewer_files(data, out)
        return html_path.read_text(), data, out


# ---------------------------------------------------------------------------
# Step 91 — ELK Directional Layout
# ---------------------------------------------------------------------------


class TestBrainViewerShell:
    def _get_html(self):
        import tempfile
        from pathlib import Path

        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
            write_brain_viewer_files,
        )
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job()
        events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.job_id),
                    "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
        graph = build_project_brain(job, events)
        data = build_brain_viewer_data(job, graph, events)
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            html_path = write_brain_viewer_files(data, out)
            return html_path.read_text()

    def test_viewer_html_has_shell(self):
        html = self._get_html()
        assert "remedy-shell" in html

    def test_viewer_html_has_data_island(self):
        html = self._get_html()
        assert 'type="application/json"' in html

    def test_viewer_html_static_fallback(self):
        html = self._get_html()
        assert "static-fallback" in html

    def test_viewer_html_no_external_assets(self):
        html = self._get_html()
        # Allow data: URIs but no external
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\s]+)', html)
        assert urls == [], f"external URLs found: {urls}"

    def test_viewer_html_no_trademark(self):
        html = self._get_html().lower()
        assert "assassin" not in html
        assert "abstergo" not in html

    def test_viewer_html_no_raw_leaks(self):
        html = self._get_html()
        for forbidden in ("stdout", "stderr", "raw_output", "Traceback",
                          "diff_preview", "approval_reason"):
            assert forbidden not in html

    def test_viewer_html_reduced_motion(self):
        html = self._get_html()
        assert "prefers-reduced-motion" in html

    def test_viewer_html_has_proof_chain(self):
        html = self._get_html()
        assert "remedy-proof-chain" in html or "proof-chain" in html

    def test_viewer_html_has_decision_panel(self):
        html = self._get_html()
        assert "remedy-decision-panel" in html or "decision-panel" in html

    def test_viewer_html_has_readiness_panel(self):
        html = self._get_html()
        assert "remedy-readiness-panel" in html or "readiness-panel" in html

    def test_viewer_html_has_timeline(self):
        html = self._get_html()
        assert "remedy-timeline" in html or "timeline" in html

    def test_viewer_html_has_node_detail(self):
        html = self._get_html()
        # Detail panel must exist
        assert "detail" in html.lower()

    def test_viewer_html_has_error_panel(self):
        html = self._get_html()
        assert "err-panel" in html or "error" in html.lower()

    def test_viewer_data_valid_json(self):
        import json

        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
            export_brain_viewer_json,
        )
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        graph = build_project_brain(job, [])
        data = build_brain_viewer_data(job, graph, [])
        j = export_brain_viewer_json(data)
        s = json.dumps(j)
        parsed = json.loads(s)
        assert "graph" in parsed
        assert "node_details" in parsed


# ── Step 74: UX Quality Gate ────────────────────────────────────────────


class TestInteractiveControls:
    def test_search_input_exists(self):
        html, _, _ = _get_viewer_html()
        assert 'id="search-input"' in html

    def test_filter_buttons_exist(self):
        html, _, _ = _get_viewer_html()
        assert 'data-filter="blocker"' in html
        assert 'data-filter="proof"' in html
        assert 'data-filter="decision"' in html
        assert 'data-filter="all"' in html

    def test_filter_rail_exists(self):
        html, _, _ = _get_viewer_html()
        assert 'id="filter-rail"' in html
        assert 'id="zone-filters"' in html
        assert 'id="status-filters"' in html

    def test_detail_panel_exists(self):
        html, _, _ = _get_viewer_html()
        assert 'id="dp"' in html
        assert 'id="db"' in html

    def test_next_action_rail_exists(self):
        html, _, _ = _get_viewer_html()
        assert 'id="next-action-rail"' in html
        assert 'na-card' in html or 'na-cards' in html

    def test_copy_buttons_exist(self):
        html, _, _ = _get_viewer_html()
        assert 'copy-btn' in html

    def test_no_eval(self):
        html, _, _ = _get_viewer_html()
        # No eval() in the script
        assert "eval(" not in html

    def test_no_external_assets(self):
        html, _, _ = _get_viewer_html()
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\\s]+)', html)
        assert urls == [], f"external URLs: {urls}"

    def test_data_island_safe(self):
        html, _, _ = _get_viewer_html()
        assert 'type="application/json"' in html

    def test_reduced_motion_present(self):
        html, _, _ = _get_viewer_html()
        assert "prefers-reduced-motion" in html

    def test_static_fallback_present(self):
        html, _, _ = _get_viewer_html()
        assert "static-fallback" in html

    def test_keyboard_slash_search(self):
        html, _, _ = _get_viewer_html()
        # JS should handle "/" key
        assert "'/'" in html or '\\u002f' in html.lower() or "key==='/'" in html

    def test_escape_clears(self):
        html, _, _ = _get_viewer_html()
        assert "'Escape'" in html or "Escape" in html

    def test_focus_visible(self):
        html, _, _ = _get_viewer_html()
        assert "focus-visible" in html


# ── Step 79: Viewer Preview & Share ─────────────────────────────────────


class TestViewerPreview:
    def test_viewer_path_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        job = _make_job_s74()
        save_job_plan(job)

        import io

        from apps.cli.commands.brain import _cmd_viewer_path
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_viewer_path(str(job.job_id), json_output=True)
        finally:
            sys.stdout = old
        out = buf.getvalue()
        j = json.loads(out)
        assert j["version"] == 1
        assert "index_path" in j
        assert "node_count" in j

    def test_viewer_path_text(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        job = _make_job_s74()
        save_job_plan(job)

        import io

        from apps.cli.commands.brain import _cmd_viewer_path
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_viewer_path(str(job.job_id), json_output=False)
        finally:
            sys.stdout = old
        out = buf.getvalue().strip()
        assert out.endswith("index.html")

    def test_export_viewer(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        job = _make_job_s74()
        save_job_plan(job)

        from apps.cli.commands.brain import _cmd_export_viewer
        export_dir = tmp_path / "exported"
        import io
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_export_viewer(str(job.job_id), str(export_dir))
        finally:
            sys.stdout = old

        assert (export_dir / "index.html").exists()
        assert (export_dir / "viewer_data.json").exists()
        assert (export_dir / "viewer_manifest.json").exists()

        manifest = json.loads((export_dir / "viewer_manifest.json").read_text())
        assert manifest["version"] == 1
        assert manifest["safe_to_share"] is True
        for key in ("job_id", "created_at", "index_path", "viewer_data_path",
                     "node_count", "edge_count", "detail_count", "style_version",
                     "redaction_summary"):
            assert key in manifest, f"manifest missing: {key}"

    def test_open_graceful_fallback(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.pingpong_job import save_job_plan
        job = _make_job_s74()
        save_job_plan(job)

        # Mock subprocess.Popen to raise
        import subprocess
        original_popen = subprocess.Popen
        def fake_popen(*a, **kw):
            raise FileNotFoundError("no opener")
        monkeypatch.setattr(subprocess, "Popen", fake_popen)

        import io

        from apps.cli.commands.brain import _cmd_brain_open
        old_out = sys.stdout
        old_err = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        try:
            _cmd_brain_open(str(job.job_id))
        finally:
            sys.stdout = old_out
            sys.stderr = old_err

    def test_no_server(self):
        html, _, _ = _get_viewer_html()
        # No http server references
        assert "http.server" not in html
        assert "localhost:" not in html
        assert "0.0.0.0" not in html

    def test_no_lan_url(self):
        html, _, _ = _get_viewer_html()
        urls = re.findall(r'https?://\d+\.\d+\.\d+\.\d+', html)
        assert urls == []

    def test_catalog_commands_exist(self):
        from apps.cli.command_catalog import get_command
        assert get_command("brain.open") is not None
        assert get_command("brain.viewer-path") is not None
        assert get_command("brain.export-viewer") is not None

    def test_viewer_handlers_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "brain.open" in handlers
        assert "brain.viewer-path" in handlers
        assert "brain.export-viewer" in handlers


# ---------------------------------------------------------------------------
# No popup on load
# ---------------------------------------------------------------------------


class TestViewerGuidanceRail:
    """The static viewer's own guidance rail; the cockpit's guidance cards went with the old face
    (amend1015f D27)."""

    def test_viewer_guidance_rail(self):
        html, _, _ = _get_viewer_html()
        assert "guidance-rail" in html
        assert "guide-card" in html


class TestLegacyViewerQuarantine:
    def test_brain_viewer_docstring_legacy(self):
        import packages.orchestration.brain_viewer as bv
        assert "Legacy" in (bv.__doc__ or ""), "brain_viewer.py not marked as legacy"
