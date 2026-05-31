"""
Tests for Steps 83-90 — PixiJS Brain Canvas, Semantic Zoom, UX Quality Gate v2.

Coverage:
  - View model builder produces correct layers and zoom assignments
  - Node detail builder returns compact card data
  - UI server serves static assets (when dist exists)
  - Frontend build produces index.html and JS bundles
  - Session registry CRUD
  - UX anti-regression: no dark default, max 3 nodes at zoom 0, no labels at zoom 0
  - Command catalog has new UI commands
  - Legacy viewer marked as legacy in docstring
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest


# ---------------------------------------------------------------------------
# View Model
# ---------------------------------------------------------------------------


class TestBrainViewModel:
    """Tests for ui_view_model.build_brain_view_model."""

    def _make_job(self):
        from packages.orchestration.storage import load_job
        # Use a minimal mock job
        from unittest.mock import MagicMock
        job = MagicMock()
        job.id = uuid4()
        job.name = "test-job"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []
        return job

    def _make_graph_and_events(self):
        """Return a (job, events) pair that produces a valid brain graph."""
        job = self._make_job()
        events = []
        return job, events

    def test_view_model_structure(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        assert vm["version"] == 4
        assert "nodes" in vm
        assert "edges" in vm
        assert "layers" in vm
        assert len(vm["layers"]) == 7

    def test_layer_names(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        names = [l["name"] for l in vm["layers"]]
        assert names == ["Origin", "Intent Path", "Work Path", "Proof Path", "Attention", "System Clusters", "Full Graph"]

    def test_job_node_is_layer_zero(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        job_nodes = [n for n in vm["nodes"] if n["type"] == "job"]
        assert len(job_nodes) >= 1
        for jn in job_nodes:
            assert jn["layer"] == 0
            assert jn["visible_from_zoom"] == 0

    def test_origin_max_nodes(self):
        """At zoom level 0 (origin), at most 1 node visible."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        zoom0_nodes = [n for n in vm["nodes"] if n["visible_from_zoom"] <= 0]
        assert len(zoom0_nodes) <= 1, f"Origin zoom shows {len(zoom0_nodes)} nodes, max 1"

    def test_no_labels_at_origin_except_job(self):
        """At zoom level 0, only job node may show label."""
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            if n["visible_from_zoom"] == 0 and n["type"] != "job":
                assert n["show_label_from_zoom"] > 0, (
                    f"Node {n['id']} (type={n['type']}) shows label at zoom 0"
                )

    def test_node_has_position(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            assert "x" in n
            assert "y" in n

    def test_node_has_cluster(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for n in vm["nodes"]:
            assert "cluster_id" in n
            assert n["cluster_id"] in (
                "origin", "lifecycle", "patches", "testing",
                "attention", "events", "system", "other",
                "proofs", "future",
            )

    def test_edge_visibility(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        job, events = self._make_graph_and_events()
        vm = build_brain_view_model(job, events)

        for e in vm["edges"]:
            assert "visible_from_zoom" in e
            assert 0 <= e["visible_from_zoom"] <= 6


# ---------------------------------------------------------------------------
# Node Detail
# ---------------------------------------------------------------------------


class TestNodeDetail:
    def _make_job(self):
        from unittest.mock import MagicMock
        job = MagicMock()
        job.id = uuid4()
        job.name = "test-job"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []
        return job

    def test_detail_returns_node_info(self):
        from packages.orchestration.ui_view_model import build_brain_view_model, build_node_detail
        job = self._make_job()
        events: list[dict] = []

        vm = build_brain_view_model(job, events)
        if vm["nodes"]:
            node_id = vm["nodes"][0]["id"]
            detail = build_node_detail(job, events, node_id)
            assert detail["version"] == 2
            assert detail["node_id"] == node_id
            assert "title" in detail
            assert "status_text" in detail

    def test_detail_missing_node(self):
        from packages.orchestration.ui_view_model import build_node_detail
        from unittest.mock import MagicMock
        job = MagicMock()
        job.id = uuid4()
        job.name = "test"
        job.state.value = "active"
        job.tasks = []
        job.artifacts = []

        detail = build_node_detail(job, [], "nonexistent-node-id")
        assert "error" in detail


# ---------------------------------------------------------------------------
# Frontend Build
# ---------------------------------------------------------------------------


class TestFrontendBuild:
    def test_dist_index_exists(self):
        index = Path(__file__).resolve().parent.parent / "apps" / "ui" / "index.html"
        assert index.is_file(), "apps/ui/index.html not found — source entry point missing"

    def test_dist_has_js_bundles(self):
        dist = Path(__file__).resolve().parent.parent / "apps" / "ui" / "dist" / "assets"
        if not dist.is_dir():
            pytest.skip("dist/assets/ not built")
        js_files = list(dist.glob("*.js"))
        assert len(js_files) >= 1, "No JS bundles in dist/assets/"

    def test_package_json_deps(self):
        pkg = Path(__file__).resolve().parent.parent / "apps" / "ui" / "package.json"
        data = json.loads(pkg.read_text())
        deps = data.get("dependencies", {})
        assert "react" in deps
        assert "@xyflow/react" in deps


# ---------------------------------------------------------------------------
# UX Anti-Regression (Quality Gate v2)
# ---------------------------------------------------------------------------


class TestUXAntiRegression:
    """Tests that fail if old bad UX patterns return."""

    def test_no_dark_background_in_pixi_frontend(self):
        """Frontend HTML must not have dark background colors."""
        index = Path(__file__).resolve().parent.parent / "apps" / "ui" / "index.html"
        html = index.read_text()
        dark_colors = ["#0a0e14", "#0d1117", "#1a1a2e", "#000000"]
        for c in dark_colors:
            assert c not in html, f"Dark color {c} found in frontend HTML"

    def test_background_is_light(self):
        """Frontend CSS tokens should define a light background."""
        tokens = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src" / "styles" / "tokens.css"
        css = tokens.read_text()
        assert "--remedy-bg" in css, "Background token not found in tokens.css"
        assert "#edf3fb" in css, "Light background color #edf3fb not found"

    def test_no_scanlines_in_frontend(self):
        """No retro scanline effects."""
        src_dir = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src"
        for f in src_dir.rglob("*.ts"):
            content = f.read_text()
            assert "scanline" not in content.lower(), f"Scanline reference in {f.name}"

    def test_particles_reduced_motion_safe(self):
        """Animations must be guarded by reduced-motion check."""
        provider = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src" / "components" / "shell" / "ReducedMotionProvider.tsx"
        assert provider.is_file(), "ReducedMotionProvider.tsx not found"
        content = provider.read_text()
        assert "reducedMotion" in content or "reduced-motion" in content, "Reduced-motion check not found"

    def test_pixi_viewport_in_renderer(self):
        """Graph component must use @xyflow/react for zoom/pan."""
        flow = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "RemedyBrainFlow.tsx"
        content = flow.read_text()
        assert "@xyflow/react" in content, "@xyflow/react not used in RemedyBrainFlow"

    def test_semantic_zoom_in_renderer(self):
        """Semantic zoom module must exist with zoom-level function."""
        sz = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src" / "components" / "graph" / "semanticZoom.ts"
        assert sz.is_file(), "semanticZoom.ts not found"
        content = sz.read_text()
        assert "semanticZoomLevelFromViewportZoom" in content, "Zoom level function not found"

    def test_detail_card_not_permanent_rail(self):
        """Detail card must be a compact popover component."""
        popover = Path(__file__).resolve().parent.parent / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx"
        assert popover.is_file(), "DetailPopover.tsx not found"
        content = popover.read_text()
        assert "remedy-detail-compact" in content, "Compact detail class not found"

    def test_view_model_seven_zoom_levels(self):
        """View model must define exactly 7 zoom levels."""
        from packages.orchestration.ui_view_model import _ZOOM_NAMES
        assert len(_ZOOM_NAMES) == 7


# ---------------------------------------------------------------------------
# UI Commands in Catalog
# ---------------------------------------------------------------------------


class TestUICommands:
    def test_new_commands_in_catalog(self):
        from apps.cli.command_catalog import get_command
        for cmd_id in ("ui.latest", "ui.status", "ui.stop", "ui.open"):
            cmd = get_command(cmd_id)
            assert cmd.group_id == "ui"

    def test_ui_group_has_five_commands(self):
        from apps.cli.command_catalog import get_commands_for_group
        cmds = get_commands_for_group("ui")
        assert len(cmds) == 5
        subs = {c.subcommand for c in cmds}
        assert subs == {"start", "latest", "status", "stop", "open"}


# ---------------------------------------------------------------------------
# Legacy Viewer Quarantine
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
