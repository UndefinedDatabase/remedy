"""
Tests for Steps 227-246 — Responsive UI Rescue with Canvas Force Brain Graph.

Supersedes old Steps 208-226 pixel-lock tests.

Verifies:
  - Responsive shell (no fixed 1678×926 frame)
  - Canvas force graph via react-force-graph-2d
  - No @xyflow/react in default graph path
  - Data-ui markers correct
  - No detail popup on initial load
  - Dense task rows
  - No default LayerSwitcher in shell
  - No forbidden debug words
  - remedy ui start contract
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
UI_SRC = ROOT / "apps" / "ui" / "src"
UI_ROOT = ROOT / "apps" / "ui"


# ---------------------------------------------------------------------------
# Step 227 — Contract markers
# ---------------------------------------------------------------------------

class TestStep227ContractMarkers:
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

class TestStep228Dependencies:
    """react-force-graph-2d replaces @xyflow/react."""

    def test_package_has_force_graph(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "react-force-graph-2d" in pkg

    def test_package_has_d3_force(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "d3-force" in pkg

    def test_no_xyflow_in_package(self):
        pkg = (UI_ROOT / "package.json").read_text()
        assert "@xyflow/react" not in pkg

    def test_no_xyflow_in_default_graph(self):
        graph_dir = UI_SRC / "components" / "graph"
        for f in graph_dir.glob("*.tsx"):
            if "legacy" in str(f):
                continue
            content = f.read_text()
            assert "@xyflow/react" not in content, f"@xyflow/react in {f.name}"

    def test_no_xyflow_in_default_ts(self):
        graph_dir = UI_SRC / "components" / "graph"
        for f in graph_dir.glob("*.ts"):
            if "legacy" in str(f):
                continue
            content = f.read_text()
            assert "@xyflow/react" not in content, f"@xyflow/react in {f.name}"


# ---------------------------------------------------------------------------
# Step 229 — Responsive shell
# ---------------------------------------------------------------------------

class TestStep229ResponsiveShell:
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

class TestStep230SingleRail:
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

class TestForceGraph:
    """Canvas force graph is default."""

    def test_force_brain_graph_exists(self):
        assert (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").is_file()

    def test_force_types_exist(self):
        assert (UI_SRC / "components" / "graph" / "forceBrainTypes.ts").is_file()

    def test_build_model_exists(self):
        assert (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").is_file()

    def test_brain_stage_uses_force_graph(self):
        code = (UI_SRC / "components" / "graph" / "BrainGraphStage.tsx").read_text()
        assert "ForceBrainGraph" in code
        assert "RemedyBrainFlow" not in code
        assert "ConstellationBackdrop" not in code

    def test_force_graph_imports_force_graph_2d(self):
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "react-force-graph-2d" in code

    def test_canvas_rendering(self):
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "shadowBlur" in code
        assert "createRadialGradient" in code
        assert "quadraticCurveTo" in code

    def test_no_math_random_in_model(self):
        code = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert "Math.random" not in code

    def test_seeded_rng(self):
        code = (UI_SRC / "components" / "graph" / "buildForceBrainModel.ts").read_text()
        assert "seededRng" in code

    def test_resize_observer_hook(self):
        code = (UI_SRC / "components" / "graph" / "useGraphSize.ts").read_text()
        assert "ResizeObserver" in code

    def test_reduced_motion_respected(self):
        code = (UI_SRC / "components" / "graph" / "ForceBrainGraph.tsx").read_text()
        assert "reducedMotion" in code or "reduced-motion" in code


# ---------------------------------------------------------------------------
# Step 240 — Better data normalization
# ---------------------------------------------------------------------------

class TestStep240DataNormalization:
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

class TestStep241RightPanel:
    """Right panel uses responsive grid."""

    def test_panel_css_grid(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "grid-template-rows" in css

    def test_task_list_scrolls(self):
        css = (UI_SRC / "components" / "panels" / "RightLivePanel.module.css").read_text()
        assert "overflow" in css


# ---------------------------------------------------------------------------
# Step 243 — UI start command
# ---------------------------------------------------------------------------

class TestStep243UiStart:
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

class TestNoPopupOnLoad:
    """Detail popover does not render by default."""

    def test_app_starts_null(self):
        app = (UI_SRC / "RemedyApp.tsx").read_text()
        assert "useState<string | null>(null)" in app


# ---------------------------------------------------------------------------
# No forbidden debug words
# ---------------------------------------------------------------------------

class TestNoForbiddenDebugWords:
    FORBIDDEN = ["TODO:", "FIXME:", "HACK:", "console.log(", "debugger"]

    def test_no_forbidden_in_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            if "legacy" in str(f):
                continue
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"

    def test_no_forbidden_in_ts(self):
        for f in UI_SRC.rglob("*.ts"):
            if "legacy" in str(f) or "test" in f.name.lower():
                continue
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"forbidden '{word}' in {f.relative_to(ROOT)}"
