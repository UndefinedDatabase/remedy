"""
Domain tests: ui_contracts/test_responsive.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from http.client import HTTPConnection
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4
import json
import os
import pytest
import re
import signal
import socket
import sys
import tempfile
import threading
import time

from packages.core.models import Job, RunState, Task

ROOT = Path(__file__).resolve().parent.parent.parent

UI_SRC = ROOT / "apps" / "ui" / "src"

UI_ROOT = ROOT / "apps" / "ui"


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


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────


def _make_job_s74(**overrides) -> Job:
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


def _make_job_s80(**overrides: object) -> Job:
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




class TestBrainViewerShell:
    def _get_html(self):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data, write_brain_viewer_files,
        )
        from packages.orchestration.project_brain import build_project_brain
        import tempfile
        from pathlib import Path

        job = _make_job()
        events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.id),
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
            build_brain_viewer_data, export_brain_viewer_json,
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


# ── Step 76: Spatial Layout ─────────────────────────────────────────────




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
        job = _make_job_s74()
        cards = build_guidance_cards(job, [])
        assert len(cards) >= 1
        for c in cards:
            assert c.id
            assert c.title
            assert c.severity in ("high", "medium", "low", "info")
            assert c.command

    def test_export_guidance_json(self):
        from packages.orchestration.guidance import build_guidance_cards, export_guidance_json
        job = _make_job_s74()
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
        job = _make_job_s74()
        cards = build_guidance_cards(job, [])
        j = export_guidance_json(job, cards)
        for card in j["cards"]:
            for key in ("id", "title", "severity", "why_it_matters",
                        "safe_next_action", "command", "related_node_type"):
                assert key in card, f"missing key: {key}"

    def test_summarize_guidance(self):
        from packages.orchestration.guidance import build_guidance_cards, summarize_guidance
        job = _make_job_s74()
        cards = build_guidance_cards(job, [])
        text = summarize_guidance(job, cards)
        assert "Guidance" in text

    def test_guidance_no_raw_leaks(self):
        from packages.orchestration.guidance import build_guidance_cards, export_guidance_json
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        job = _make_job_s74()
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
        job = _make_job_s74()
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
        job = _make_job_s74()
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
        job = _make_job_s74()
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
        job = _make_job_s74()
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
        job = _make_job_s74()
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




class TestProgressiveBrainExplorer:
    """Test the progressive brain explorer modes and disclosure."""

    def test_journey_layer_default(self):
        """Journey is default layer (replaces proof-path as default mode)."""
        html = _get_app_html()
        assert "journey" in html
        assert "remedy-layer-switcher" in html

    def test_diagnostics_layer_available(self):
        """Diagnostics layer available (replaces system-map/full-graph modes)."""
        html = _get_app_html()
        assert "diagnostics" in html

    def test_detail_card_hidden_by_default(self):
        html = _get_app_html()
        assert "detail-card" in html
        # Not visible by default
        assert "display: none" in html or "display:none" in html.replace(" ", "")

    def test_node_click_shows_detail(self):
        """Clicking a node should show detail card."""
        html = _get_app_html()
        assert "detail-card" in html
        # Detail card gets .visible class on click
        assert "visible" in html

    def test_journey_graph_present(self):
        """Journey graph area exists in shell."""
        html = _get_app_html()
        assert "remedy-journey-shell" in html
        assert "remedy-node" in html

    def test_checklist_in_shell(self):
        """Checklist sidebar present (replaces cluster/expandable nodes)."""
        html = _get_app_html()
        assert "remedy-checklist" in html

    def test_no_raw_leaks_in_explorer(self):
        html = _get_app_html()
        for forbidden in ("raw_output", "command_output", "Traceback", "MUST_NOT_RENDER"):
            assert forbidden not in html


# ---------------------------------------------------------------------------
# Smoke script structural tests
# ---------------------------------------------------------------------------




class TestFrontendBuild:
    def test_dist_index_exists(self):
        index = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "index.html"
        assert index.is_file(), "apps/ui/index.html not found — source entry point missing"

    def test_dist_has_js_bundles(self):
        dist = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "dist" / "assets"
        if not dist.is_dir():
            pytest.skip("dist/assets/ not built")
        js_files = list(dist.glob("*.js"))
        assert len(js_files) >= 1, "No JS bundles in dist/assets/"

    def test_package_json_deps(self):
        pkg = Path(__file__).resolve().parent.parent.parent / "apps" / "ui" / "package.json"
        data = json.loads(pkg.read_text())
        deps = data.get("dependencies", {})
        assert "react" in deps
        # Current graph architecture: Canvas/Force (not React Flow)
        assert "react-force-graph-2d" in deps
        assert "d3-force" in deps


# ---------------------------------------------------------------------------
# UX Anti-Regression (Quality Gate v2)
# ---------------------------------------------------------------------------




class TestLegacyViewerQuarantine:
    def test_brain_viewer_docstring_legacy(self):
        import packages.orchestration.brain_viewer as bv
        assert "Legacy" in (bv.__doc__ or ""), "brain_viewer.py not marked as legacy"

    def test_ui_app_shell_docstring_legacy(self):
        import packages.orchestration.ui_app_shell as shell
        assert "Legacy" in (shell.__doc__ or ""), "ui_app_shell.py not marked as legacy"


# ---------------------------------------------------------------------------
# Server: static asset serving and new API endpoints
# ---------------------------------------------------------------------------




class TestFrontendBuildV2:
    def test_dist_exists(self):
        index = Path(__file__).parent.parent.parent / "apps" / "ui" / "index.html"
        assert index.is_file(), "Source index.html must exist"

    def test_force_graph_in_package(self):
        """Current graph uses react-force-graph-2d + d3-force, not @xyflow/react."""
        pkg = Path(__file__).parent.parent.parent / "apps" / "ui" / "package.json"
        data = json.loads(pkg.read_text())
        deps = data.get("dependencies", {})
        assert "react-force-graph-2d" in deps, "react-force-graph-2d must be a dependency"
        assert "d3-force" in deps, "d3-force must be a dependency for force graph"

    def test_no_dark_background(self):
        tokens = Path(__file__).parent.parent.parent / "apps" / "ui" / "src" / "styles" / "tokens.css"
        css = tokens.read_text()
        assert "#ecf2fb" in css, "Light background token must be present"
        for dark in ["#0a0e14", "#0d1117", "#1a1a2e", "#000000"]:
            assert dark not in css




class TestShellLayoutComponents:
    """Shell layout and top-level components exist."""

    def test_shell_exists(self):
        assert (UI_SRC / "components" / "shell" / "RemedyShell.tsx").is_file()

    def test_shell_css_module(self):
        assert (UI_SRC / "components" / "shell" / "RemedyShell.module.css").is_file()

    def test_left_brand_rail(self):
        assert (UI_SRC / "components" / "rail" / "LeftBrandRail.tsx").is_file()

    def test_remedy_logo(self):
        assert (UI_SRC / "components" / "rail" / "RemedyLogo.tsx").is_file()

    def test_side_icon_dock(self):
        assert (UI_SRC / "components" / "rail" / "SideIconDock.tsx").is_file()
        content = (UI_SRC / "components" / "rail" / "SideIconDock.tsx").read_text(encoding="utf-8")
        assert "aria-label" in content

    def test_top_metrics_bar(self):
        assert (UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx").is_file()
        content = (UI_SRC / "components" / "metrics" / "TopMetricsBar.tsx").read_text(encoding="utf-8")
        assert "Open" in content or "open" in content
        assert "Progress" in content or "progress" in content

    def test_command_bar(self):
        # New design pack: the command bar is a local jump-to filter (editable
        # input, no chat/LLM/mutation) — see test_command_bar_no_mutation.
        assert (UI_SRC / "components" / "command" / "CommandBar.tsx").is_file()
        content = (UI_SRC / "components" / "command" / "CommandBar.tsx").read_text(encoding="utf-8")
        assert "placeholder" in content
        assert "onJump" in content

    def test_command_bar_no_mutation(self):
        content = (UI_SRC / "components" / "command" / "CommandBar.tsx").read_text(encoding="utf-8")
        assert "POST" not in content
        assert "PUT" not in content
        assert "DELETE" not in content

    def test_reduced_motion_provider(self):
        assert (UI_SRC / "components" / "shell" / "ReducedMotionProvider.tsx").is_file()
        content = (UI_SRC / "components" / "shell" / "ReducedMotionProvider.tsx").read_text(encoding="utf-8")
        assert "prefers-reduced-motion" in content


# ---------------------------------------------------------------------------
# Steps 180-183 — Graph components
# ---------------------------------------------------------------------------




class TestRightPanelCards:
    """Right live panel components."""

    def test_right_live_panel(self):
        assert (UI_SRC / "components" / "panels" / "RightLivePanel.tsx").is_file()

    def test_live_status_pill(self):
        f = UI_SRC / "components" / "panels" / "LiveStatusPill.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "LIVE" in content

    def test_agent_now_card(self):
        f = UI_SRC / "components" / "panels" / "AgentNowCard.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Agent" in content

    def test_activity_feed_card(self):
        f = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Activity" in content
        # No mutation
        assert "POST" not in content

    def test_task_checklist_card(self):
        f = UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Tasks" in content
        assert "completed" in content

    def test_no_add_task_button(self):
        # New design pack: the "+ Add Task" placeholder was removed; task
        # creation is CLI-only. The propose affordance copies a command instead.
        f = UI_SRC / "components" / "panels" / "AddTaskButton.tsx"
        assert not f.exists(), "AddTaskButton.tsx must be removed (no UI task creation)"
        checklist = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text(encoding="utf-8")
        assert "remedy task propose" in checklist


# ---------------------------------------------------------------------------
# Steps 189-191 — Timeline + Detail + Layers
# ---------------------------------------------------------------------------




class TestDataUiMarkerPresence:
    """All required data-ui markers exist in source."""

    MARKERS = [
        ("top-metrics-bar", "components/metrics/TopMetricsBar.tsx"),
        ("right-live-panel", "components/panels/RightLivePanel.tsx"),
        ("task-checklist-card", "components/panels/TaskChecklistCard.tsx"),
        ("remedy-visual-v2", "components/shell/RemedyShell.tsx"),
        ("brain-graph-stage", "components/graph/BrainGraphStage.tsx"),
        ("force-brain-graph", "components/graph/ForceBrainGraph.tsx"),
        ("command-bar", "components/command/CommandBar.tsx"),
        ("phase-timeline", "components/timeline/PhaseTimeline.tsx"),
        ("left-brand-rail", "components/rail/LeftBrandRail.tsx"),
    ]

    @pytest.mark.parametrize("marker,path", MARKERS)
    def test_marker_in_source(self, marker, path):
        f = UI_SRC / path
        assert f.is_file(), f"missing {path}"
        assert marker in f.read_text(), f"marker '{marker}' not in {path}"


# ---------------------------------------------------------------------------
# Step 228 — Dependency swap
# ---------------------------------------------------------------------------




class TestResponsiveCssGridShell:
    """Shell uses responsive CSS grid, not fixed frame."""

    def test_no_fixed_1678_frame(self):
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "1678" not in css
        assert "926" not in css
        assert "aspect-ratio" not in css

    def test_uses_css_grid_clamp(self):
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "clamp(" in css
        assert "grid-template-columns" in css

    def test_has_media_queries(self):
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "@media" in css


# ---------------------------------------------------------------------------
# Step 230 — Single left rail
# ---------------------------------------------------------------------------




class TestSingleLeftRailNoLayerSwitcher:
    """One left rail, no default LayerSwitcher."""

    def test_no_layer_switcher_in_shell(self):
        tsx = (UI_SRC / "components" / "shell" / "RemedyShell.tsx").read_text()
        assert "LayerSwitcher" not in tsx

    def test_left_rail_has_dock(self):
        tsx = (UI_SRC / "components" / "rail" / "LeftBrandRail.tsx").read_text()
        assert "SideIconDock" in tsx


# ---------------------------------------------------------------------------
# Steps 231-238 — Force brain graph
# ---------------------------------------------------------------------------




class TestRightPanelResponsiveGrid:
    """Right panel uses responsive grid."""

    def test_panel_css_layout(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "flex-direction: column" in css or "grid-template-rows" in css

    def test_task_list_scrolls(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "overflow" in css


# ---------------------------------------------------------------------------
# Step 243 — UI start command
# ---------------------------------------------------------------------------




class TestUiStartAutoBuildCommand:
    """remedy ui start works with auto-build."""

    def test_ui_server_has_auto_build(self):
        code = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text()
        assert "_auto_build_frontend" in code

    def test_cli_ui_command(self):
        code = (ROOT / "apps" / "cli" / "commands" / "ui.py").read_text()
        assert "ui.start" in code
        assert "open_browser" in code


# ---------------------------------------------------------------------------
# No popup on load
# ---------------------------------------------------------------------------

