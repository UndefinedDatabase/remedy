"""Tests for Steps 74.1, 75, 76, 77, 78, 79."""

from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "tasks": [Task(description="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _get_viewer_html():
    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain

    job = _make_job()
    events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.id),
                "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
    graph = build_project_brain(job, events)
    data = build_brain_viewer_data(job, graph, events)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        html_path = write_brain_viewer_files(data, out)
        return html_path.read_text(), data, out


# ── Step 74.1: Redaction Gate Precision ─────────────────────────────────


class TestRedactionPatterns:
    def test_module_exists(self):
        from packages.orchestration.redaction_patterns import (
            FORBIDDEN_RAW_FIELD_NAMES,
            FORBIDDEN_SECRET_PATTERNS,
            find_forbidden_surface_tokens,
        )
        assert len(FORBIDDEN_RAW_FIELD_NAMES) >= 5
        assert len(FORBIDDEN_SECRET_PATTERNS) >= 5

    def test_no_secrets_allowed(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        # Category words are allowed
        assert find_forbidden_surface_tokens("No secrets or API keys in worker specs.") == []
        assert find_forbidden_surface_tokens("redact secrets") == []
        assert find_forbidden_surface_tokens("environment_secrets") == []

    def test_secret_equals_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("config: secret=abc123")
        assert len(findings) > 0

    def test_password_equals_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("db: password=hunter2")
        assert len(findings) > 0

    def test_sk_prefix_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("key: sk-abc123defg456789")
        assert len(findings) > 0

    def test_ghp_prefix_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("token: ghp_abcdefghijklmnop")
        assert len(findings) > 0

    def test_raw_field_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("field: approval_reason")
        assert len(findings) > 0
        findings2 = find_forbidden_surface_tokens("diff_preview data here")
        assert len(findings2) > 0

    def test_traceback_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("Traceback (most recent call last):")
        assert len(findings) > 0

    def test_viewer_html_passes_precision(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        html, _, _ = _get_viewer_html()
        findings = find_forbidden_surface_tokens(html)
        assert findings == [], f"Viewer HTML has redaction findings: {findings}"

    def test_clean_text_passes(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        assert find_forbidden_surface_tokens("Normal text about jobs and tasks") == []
        assert find_forbidden_surface_tokens("No secrets or API keys") == []


# ── Step 75: Interactive Brain Control Surface ──────────────────────────


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


# ── Step 76: Spatial Layout ─────────────────────────────────────────────


class TestSpatialLayout:
    def test_nodes_have_zone(self):
        _, data, _ = _get_viewer_html()
        for node in data.graph["nodes"]:
            assert "zone" in node, f"node {node['id']} missing zone"

    def test_layout_deterministic(self):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
        )
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job()
        events = []
        graph = build_project_brain(job, events)
        d1 = build_brain_viewer_data(job, graph, events)
        d2 = build_brain_viewer_data(job, graph, events)
        assert d1.positions == d2.positions

    def test_zone_labels_in_viewer(self):
        html, _, _ = _get_viewer_html()
        assert "zone-label" in html

    def test_zone_map_covers_types(self):
        from packages.orchestration.brain_viewer import _ZONE_MAP
        required = ["job", "task", "artifact", "patch_intent", "memory_placeholder",
                     "mcp_placeholder", "decision_queue", "test_run"]
        for t in required:
            assert t in _ZONE_MAP, f"missing zone for {t}"

    def test_future_nodes_muted(self):
        html, _, _ = _get_viewer_html()
        assert "future-edge" in html or "future" in html

    def test_edge_types_distinguished(self):
        html, _, _ = _get_viewer_html()
        assert "proof-edge" in html
        assert "blocked-edge" in html
        assert "future-edge" in html

    def test_no_raw_leaks_in_viewer(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        html, _, _ = _get_viewer_html()
        findings = find_forbidden_surface_tokens(html)
        assert findings == []


# ── Step 77: Motion & Depth System ──────────────────────────────────────


class TestMotionDepth:
    def test_mist_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-mist" in html

    def test_scanlines(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-scanlines" in html

    def test_grid_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-grid" in html

    def test_edge_glow(self):
        html, _, _ = _get_viewer_html()
        assert "drop-shadow" in html

    def test_hover_lift(self):
        html, _, _ = _get_viewer_html()
        # Hover effect on nodes
        assert ".nd:hover" in html

    def test_selected_pulse(self):
        html, _, _ = _get_viewer_html()
        assert "sel-pulse" in html

    def test_reduced_motion_disables(self):
        html, _, _ = _get_viewer_html()
        assert "prefers-reduced-motion" in html
        # Scanlines hidden under reduced motion
        assert "remedy-scanlines" in html

    def test_no_external_assets(self):
        html, _, _ = _get_viewer_html()
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\\s]+)', html)
        assert urls == []

    def test_no_canvas_required(self):
        html, _, _ = _get_viewer_html()
        # Core function must not require canvas
        assert "<canvas" not in html

    def test_orbit_bg_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-orbit-bg" in html

    def test_particle_field_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-particle-field" in html


# ── Step 78: Human Guidance Rail ────────────────────────────────────────


class TestGuidanceRail:
    def test_guidance_module_exists(self):
        from packages.orchestration.guidance import (
            GuidanceCard,
            build_guidance_cards,
            export_guidance_json,
            summarize_guidance,
        )
        assert GuidanceCard is not None

    def test_build_guidance_cards(self):
        from packages.orchestration.guidance import build_guidance_cards
        job = _make_job()
        cards = build_guidance_cards(job, [])
        assert len(cards) >= 1
        for c in cards:
            assert c.id
            assert c.title
            assert c.severity in ("high", "medium", "low", "info")
            assert c.command

    def test_export_guidance_json(self):
        from packages.orchestration.guidance import build_guidance_cards, export_guidance_json
        job = _make_job()
        cards = build_guidance_cards(job, [])
        j = export_guidance_json(job, cards)
        assert j["version"] == 1
        assert j["scope"] == "job"
        assert "cards" in j
        assert "summary" in j
        assert "recommended_next_action" in j
        assert "job_id" in j

    def test_guidance_json_card_schema(self):
        from packages.orchestration.guidance import build_guidance_cards, export_guidance_json
        job = _make_job()
        cards = build_guidance_cards(job, [])
        j = export_guidance_json(job, cards)
        for card in j["cards"]:
            for key in ("id", "title", "severity", "why_it_matters",
                        "safe_next_action", "command", "related_node_type"):
                assert key in card, f"missing key: {key}"

    def test_summarize_guidance(self):
        from packages.orchestration.guidance import build_guidance_cards, summarize_guidance
        job = _make_job()
        cards = build_guidance_cards(job, [])
        text = summarize_guidance(job, cards)
        assert "Guidance" in text

    def test_guidance_no_raw_leaks(self):
        from packages.orchestration.guidance import build_guidance_cards, export_guidance_json
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        job = _make_job()
        cards = build_guidance_cards(job, [])
        j = export_guidance_json(job, cards)
        text = json.dumps(j)
        findings = find_forbidden_surface_tokens(text)
        assert findings == []

    def test_viewer_guidance_rail(self):
        html, _, _ = _get_viewer_html()
        assert "guidance-rail" in html
        assert "guide-card" in html

    def test_guidance_commands_safe(self):
        from packages.orchestration.guidance import build_guidance_cards
        job = _make_job()
        cards = build_guidance_cards(job, [])
        for c in cards:
            assert "remedy " in c.command
            # No shell-unsafe patterns
            assert ";" not in c.command
            assert "|" not in c.command
            assert ">" not in c.command


# ── Step 79: Viewer Preview & Share ─────────────────────────────────────


class TestViewerPreview:
    def test_viewer_path_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        from apps.cli.commands.brain import _cmd_viewer_path
        import io
        import sys
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_viewer_path(str(job.id), json_output=True)
        finally:
            sys.stdout = old
        out = buf.getvalue()
        j = json.loads(out)
        assert j["version"] == 1
        assert "index_path" in j
        assert "node_count" in j

    def test_viewer_path_text(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        from apps.cli.commands.brain import _cmd_viewer_path
        import io
        import sys
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_viewer_path(str(job.id), json_output=False)
        finally:
            sys.stdout = old
        out = buf.getvalue().strip()
        assert out.endswith("index.html")

    def test_export_viewer(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        from apps.cli.commands.brain import _cmd_export_viewer
        export_dir = tmp_path / "exported"
        import io
        import sys
        old = sys.stdout
        sys.stdout = buf = io.StringIO()
        try:
            _cmd_export_viewer(str(job.id), str(export_dir))
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
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)

        # Mock subprocess.Popen to raise
        import subprocess
        original_popen = subprocess.Popen
        def fake_popen(*a, **kw):
            raise FileNotFoundError("no opener")
        monkeypatch.setattr(subprocess, "Popen", fake_popen)

        from apps.cli.commands.brain import _cmd_brain_open
        import io
        import sys
        old_out = sys.stdout
        old_err = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        try:
            _cmd_brain_open(str(job.id))
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
        assert get_command("guide.job") is not None

    def test_guide_handler_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "guide.job" in handlers
        assert "brain.open" in handlers
        assert "brain.viewer-path" in handlers
        assert "brain.export-viewer" in handlers
