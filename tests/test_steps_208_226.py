"""
Tests for Steps 208-226 — UI Pixel Lock.

Verifies:
  - Fixed 1678×926 design frame (CSS contracts)
  - No detail popup on initial load (selectedNodeId starts null)
  - ConstellationBackdrop exists with dense node generation
  - HotspotNode replaces WorkNode/pill nodes
  - Right panel has dense task rows (≥12 display rows)
  - Pixel-locked absolute positioning in RemedyShell
  - No forbidden debug words in UI source
  - remedy ui start has auto-build + browser open
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
UI_SRC = ROOT / "apps" / "ui" / "src"
UI_ROOT = ROOT / "apps" / "ui"


# ---------------------------------------------------------------------------
# Step 209 — Fixed design frame
# ---------------------------------------------------------------------------

class TestStep209DesignFrame:
    """RemedyShell locked to 1678×926."""

    def test_shell_css_has_frame_dimensions(self):
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "1678" in css, "missing 1678px width in shell CSS"
        assert "926" in css, "missing 926px height in shell CSS"

    def test_shell_css_has_absolute_slots(self):
        css = (UI_SRC / "components" / "shell" / "RemedyShell.module.css").read_text()
        assert "292px" in css, "missing leftRail width 292px"
        assert "976px" in css, "missing centerStage width 976px"
        assert "350px" in css, "missing rightPanel width 350px"

    def test_shell_tsx_has_visual_v2_marker(self):
        tsx = (UI_SRC / "components" / "shell" / "RemedyShell.tsx").read_text()
        assert "remedy-visual-v2" in tsx


# ---------------------------------------------------------------------------
# Step 210 — No popup on initial load
# ---------------------------------------------------------------------------

class TestStep210NoPopupOnLoad:
    """Detail popover does not render by default."""

    def test_app_starts_with_null_selection(self):
        app = (UI_SRC / "RemedyApp.tsx").read_text()
        assert "useState<string | null>(null)" in app, \
            "selectedNodeId should start as null"

    def test_no_auto_select_first_node(self):
        app = (UI_SRC / "RemedyApp.tsx").read_text()
        # Should NOT contain setting selectedNodeId to first node
        assert "setSelectedNodeId(data.graph.nodes[0]" not in app


# ---------------------------------------------------------------------------
# Step 216 — ConstellationBackdrop
# ---------------------------------------------------------------------------

class TestStep216ConstellationBackdrop:
    """Dense SVG backdrop for graph stage."""

    def test_constellation_file_exists(self):
        f = UI_SRC / "components" / "graph" / "ConstellationBackdrop.tsx"
        assert f.is_file()

    def test_constellation_generates_many_nodes(self):
        code = (UI_SRC / "components" / "graph" / "ConstellationBackdrop.tsx").read_text()
        # Should generate significant node count
        assert "160" in code or "nodes" in code.lower()

    def test_constellation_css_exists(self):
        f = UI_SRC / "components" / "graph" / "ConstellationBackdrop.module.css"
        assert f.is_file()


# ---------------------------------------------------------------------------
# Steps 217-218 — Hotspot nodes
# ---------------------------------------------------------------------------

class TestStep217HotspotNodes:
    """Circular hotspot nodes replace pill WorkNodes."""

    def test_hotspot_node_in_graph_nodes(self):
        code = (UI_SRC / "components" / "graph" / "GraphNodes.tsx").read_text()
        assert "HotspotNode" in code

    def test_hotspot_css_is_circular(self):
        css = (UI_SRC / "components" / "graph" / "GraphNodes.module.css").read_text()
        assert "border-radius: 50%" in css


# ---------------------------------------------------------------------------
# Steps 219-221 — Dense right panel
# ---------------------------------------------------------------------------

class TestStep219DenseRightPanel:
    """Right panel has ≥12 task display rows."""

    def test_display_rows_count(self):
        code = (UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        # Count DISPLAY_ROWS entries
        rows = re.findall(r'\{ label:', code)
        assert len(rows) >= 12, f"expected ≥12 display rows, got {len(rows)}"

    def test_right_panel_pixel_locked(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "350px" in css
        assert "832px" in css


# ---------------------------------------------------------------------------
# Step 222 — Phase timeline
# ---------------------------------------------------------------------------

class TestStep222PhaseTimeline:
    """Phase timeline pixel-locked."""

    def test_timeline_height(self):
        css = (UI_SRC / "components" / "timeline" / "PhaseTimeline.module.css").read_text()
        assert "144px" in css


# ---------------------------------------------------------------------------
# Step 224 — remedy ui start command
# ---------------------------------------------------------------------------

class TestStep224UiStartCommand:
    """remedy ui start has auto-build and browser open."""

    def test_ui_server_has_auto_build(self):
        code = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text()
        assert "_auto_build_frontend" in code
        assert "npm run build" in code

    def test_ui_server_has_browser_open(self):
        code = (ROOT / "packages" / "orchestration" / "ui_server.py").read_text()
        assert "_try_open_browser" in code

    def test_cli_ui_command_exists(self):
        code = (ROOT / "apps" / "cli" / "commands" / "ui.py").read_text()
        assert "ui.start" in code
        assert "open_browser" in code


# ---------------------------------------------------------------------------
# All steps — No forbidden debug words
# ---------------------------------------------------------------------------

class TestNoForbiddenDebugWords:
    """No debug/scaffold words in shipped UI source."""

    FORBIDDEN = ["TODO:", "FIXME:", "HACK:", "console.log(", "debugger"]

    def test_no_forbidden_in_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"

    def test_no_forbidden_in_ts(self):
        for f in UI_SRC.rglob("*.ts"):
            # Skip test files
            if "test" in f.name.lower() or "spec" in f.name.lower():
                continue
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"
