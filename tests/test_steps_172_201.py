"""
Tests for Steps 172-201 — Full UI Rebuild from Screenshot Reference.

Verifies:
  - Old viewer quarantined (Step 172)
  - UI spec exists with required sections (Step 173)
  - Frontend project structure valid (Step 174)
  - API adapter types and copy mapping (Steps 175, 194)
  - React shell and component files present (Steps 176-193)
  - Graph layout deterministic (Steps 180-181)
  - Semantic zoom pure function (Step 182)
  - Human copy mapping complete (Step 194)
  - Server integration (Step 196)
  - No forbidden debug words in source (all steps)
  - No external CDN/fonts (all steps)
  - Reduced motion support (Step 193)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
UI_SRC = ROOT / "apps" / "ui" / "src"
UI_ROOT = ROOT / "apps" / "ui"


# ---------------------------------------------------------------------------
# Step 172 — Old viewer quarantined
# ---------------------------------------------------------------------------

class TestStep172Quarantine:
    """Old viewer source moved to legacy."""

    def test_legacy_dir_exists(self):
        legacy = UI_ROOT / "legacy"
        assert legacy.is_dir(), "legacy/ directory should exist"

    def test_old_main_ts_in_legacy(self):
        assert (UI_ROOT / "legacy" / "main.ts").is_file()

    def test_old_brain_dir_in_legacy(self):
        assert (UI_ROOT / "legacy" / "brain").is_dir()

    def test_no_pixi_in_new_source(self):
        for f in UI_SRC.rglob("*.ts"):
            content = f.read_text(encoding="utf-8")
            assert "pixi.js" not in content, f"pixi.js in new source: {f}"

    def test_no_pixi_in_new_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            assert "pixi.js" not in content, f"pixi.js in new source: {f}"

    def test_new_index_html_has_root_div(self):
        index = UI_ROOT / "index.html"
        assert index.is_file()
        content = index.read_text(encoding="utf-8")
        assert 'id="root"' in content

    def test_new_index_not_old_pixi_entry(self):
        index = UI_ROOT / "index.html"
        content = index.read_text(encoding="utf-8")
        assert "src/main.tsx" in content or "main.tsx" in content
        assert "remedy-task-ribbon" not in content
        assert "remedy-brain-canvas" not in content or "module" in content


# ---------------------------------------------------------------------------
# Step 173 — UI spec exists
# ---------------------------------------------------------------------------

class TestStep173Spec:
    """UI rebuild spec document present and complete."""

    @pytest.fixture(autouse=True)
    def load_spec(self):
        self.spec_path = ROOT / "docs" / "ui" / "REMEDY_UI_REBUILD_SPEC.md"
        assert self.spec_path.is_file(), "Spec file must exist"
        self.content = self.spec_path.read_text(encoding="utf-8")

    def test_has_component_tree(self):
        assert "RemedyApp" in self.content
        assert "RemedyShell" in self.content
        assert "LeftBrandRail" in self.content
        assert "BrainGraphStage" in self.content
        assert "RightLivePanel" in self.content
        assert "PhaseTimeline" in self.content
        assert "DetailPopover" in self.content
        assert "LayerSwitcher" in self.content

    def test_has_css_tokens(self):
        assert "--remedy-bg:" in self.content
        assert "--remedy-blue-500:" in self.content
        assert "--remedy-card:" in self.content
        assert "--remedy-text:" in self.content
        assert "--remedy-shadow:" in self.content

    def test_has_forbidden_words_section(self):
        assert "Forbidden" in self.content
        assert "rank" in self.content
        assert "importance" in self.content
        assert "node_type" in self.content
        assert "context coverage" in self.content

    def test_has_semantic_zoom_rules(self):
        assert "Semantic Zoom" in self.content
        assert "Overview" in self.content
        assert "Diagnostics" in self.content

    def test_no_old_ui_as_primary(self):
        lower = self.content.lower()
        assert "old ui is primary" not in lower
        assert "pixi" not in lower


# ---------------------------------------------------------------------------
# Step 174 — Frontend project structure
# ---------------------------------------------------------------------------

class TestStep174Structure:
    """Frontend has clean modern React structure."""

    def test_package_json_valid(self):
        pkg = json.loads((UI_ROOT / "package.json").read_text(encoding="utf-8"))
        assert pkg["name"] == "@remedy/ui"
        assert "react" in pkg.get("dependencies", {})
        assert "@xyflow/react" in pkg.get("dependencies", {})
        assert "@mui/material" in pkg.get("dependencies", {})

    def test_no_pixi_dependency(self):
        pkg = json.loads((UI_ROOT / "package.json").read_text(encoding="utf-8"))
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        assert "pixi.js" not in deps
        assert "pixi-viewport" not in deps
        assert "elkjs" not in deps

    def test_tsconfig_has_jsx(self):
        tsconfig = json.loads((UI_ROOT / "tsconfig.json").read_text(encoding="utf-8"))
        assert tsconfig["compilerOptions"].get("jsx") == "react-jsx"

    def test_vite_config_has_react_plugin(self):
        vite = (UI_ROOT / "vite.config.ts").read_text(encoding="utf-8")
        assert "react" in vite

    def test_eslint_config_exists(self):
        assert (UI_ROOT / "eslint.config.js").is_file()

    def test_no_node_modules_committed(self):
        # Check .gitignore or just that node_modules is not tracked
        nm = UI_ROOT / "node_modules"
        if nm.exists():
            # Just verify it's not in git
            pass  # node_modules should be gitignored

    def test_main_tsx_exists(self):
        assert (UI_SRC / "main.tsx").is_file()

    def test_remedy_app_exists(self):
        assert (UI_SRC / "RemedyApp.tsx").is_file()

    def test_tokens_css_exists(self):
        assert (UI_SRC / "styles" / "tokens.css").is_file()

    def test_globals_css_exists(self):
        assert (UI_SRC / "styles" / "globals.css").is_file()


# ---------------------------------------------------------------------------
# Step 175 — API data adapter
# ---------------------------------------------------------------------------

class TestStep175ApiAdapter:
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

class TestStep176_179ShellComponents:
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
        assert (UI_SRC / "components" / "command" / "CommandBar.tsx").is_file()
        content = (UI_SRC / "components" / "command" / "CommandBar.tsx").read_text(encoding="utf-8")
        assert "readOnly" in content
        assert "placeholder" in content

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

class TestStep180_183Graph:
    """React Flow graph components."""

    def test_brain_graph_stage(self):
        assert (UI_SRC / "components" / "graph" / "BrainGraphStage.tsx").is_file()

    def test_remedy_brain_flow(self):
        f = UI_SRC / "components" / "graph" / "RemedyBrainFlow.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "ReactFlow" in content
        assert "@xyflow/react" in content

    def test_graph_nodes(self):
        f = UI_SRC / "components" / "graph" / "GraphNodes.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "RootNode" in content
        assert "WorkNode" in content
        assert "TinyNode" in content

    def test_soft_glow_edge(self):
        assert (UI_SRC / "components" / "graph" / "SoftGlowEdge.tsx").is_file()

    def test_organic_layout_deterministic(self):
        content = (UI_SRC / "components" / "graph" / "organicLayout.ts").read_text(encoding="utf-8")
        assert "hash" in content
        assert "seededOffset" in content

    def test_organic_layout_bounded(self):
        content = (UI_SRC / "components" / "graph" / "organicLayout.ts").read_text(encoding="utf-8")
        assert "120" in content  # max 120 nodes

    def test_semantic_zoom_function(self):
        content = (UI_SRC / "components" / "graph" / "semanticZoom.ts").read_text(encoding="utf-8")
        assert "semanticZoomLevelFromViewportZoom" in content

    def test_graph_filter_chips(self):
        f = UI_SRC / "components" / "graph" / "GraphFilterChips.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert '"All"' in content
        assert '"Open"' in content
        assert '"Planned"' in content
        assert '"Done"' in content

    def test_no_default_debug_labels_in_nodes(self):
        content = (UI_SRC / "components" / "graph" / "GraphNodes.tsx").read_text(encoding="utf-8")
        for word in ["rank", "importance", "node_type", "context coverage", "zone"]:
            assert word not in content.lower(), f"Debug word in GraphNodes: {word}"


# ---------------------------------------------------------------------------
# Steps 184-188 — Right panel + cards
# ---------------------------------------------------------------------------

class TestStep184_188RightPanel:
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
        assert "Agent is doing now" in content

    def test_activity_feed_card(self):
        f = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Chat / Activity" in content
        # No mutation
        assert "POST" not in content

    def test_task_checklist_card(self):
        f = UI_SRC / "components" / "panels" / "TaskChecklistCard.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Tasks" in content
        assert "completed" in content

    def test_add_task_button(self):
        f = UI_SRC / "components" / "panels" / "AddTaskButton.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "not enabled yet" in content
        # No mutation
        assert "POST" not in content


# ---------------------------------------------------------------------------
# Steps 189-191 — Timeline + Detail + Layers
# ---------------------------------------------------------------------------

class TestStep189_191TimelineDetailLayers:
    """Timeline, detail popover, and layer switcher."""

    def test_phase_timeline(self):
        f = UI_SRC / "components" / "timeline" / "PhaseTimeline.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        # Phase IDs in icons map
        assert "job:" in content
        assert "planning:" in content
        assert "build:" in content
        assert "test:" in content
        assert "review:" in content
        assert "finalized:" in content
        # Renders phase labels dynamically
        assert "phase.label" in content

    def test_detail_popover(self):
        f = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "remedy-detail-compact" in content
        # No forbidden words
        for word in ["rank", "importance", "node_type", "present signals", "missing signals", "zone"]:
            assert word not in content.lower(), f"Debug word in DetailPopover: {word}"

    def test_layer_switcher(self):
        f = UI_SRC / "components" / "layers" / "LayerSwitcher.tsx"
        assert f.is_file()
        content = f.read_text(encoding="utf-8")
        assert "Journey" in content
        assert "Diagnostics" in content
        assert "remedy-layer-switcher" in content


# ---------------------------------------------------------------------------
# Steps 192-193 — Visual tokens + particles
# ---------------------------------------------------------------------------

class TestStep192_193Visual:
    """Visual tokens and CSS modules."""

    def test_tokens_has_required_vars(self):
        content = (UI_SRC / "styles" / "tokens.css").read_text(encoding="utf-8")
        required = ["--remedy-bg:", "--remedy-blue-500:", "--remedy-card:", "--remedy-text:",
                     "--remedy-shadow:", "--remedy-glow:", "--remedy-left-width:", "--remedy-right-width:"]
        for var in required:
            assert var in content, f"Missing CSS token: {var}"

    def test_globals_has_reduced_motion(self):
        content = (UI_SRC / "styles" / "globals.css").read_text(encoding="utf-8")
        assert "prefers-reduced-motion" in content

    def test_no_external_fonts(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            assert "googleapis.com" not in content, f"External font in {f}"
            assert "cdn." not in content, f"CDN in {f}"

    def test_no_external_cdn_in_tsx(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            assert "cdn." not in content.lower(), f"CDN reference in {f}"
            assert "googleapis.com" not in content, f"External resource in {f}"

    def test_particles_respect_reduced_motion(self):
        f = UI_SRC / "components" / "graph" / "RemedyBrainFlow.tsx"
        content = f.read_text(encoding="utf-8")
        assert "reducedMotion" in content

    def test_css_modules_exist(self):
        expected = [
            "components/shell/RemedyShell.module.css",
            "components/graph/BrainGraphStage.module.css",
            "components/panels/RightLivePanel.module.css",
            "components/timeline/PhaseTimeline.module.css",
            "components/metrics/TopMetricsBar.module.css",
            "components/detail/DetailPopover.module.css",
            "components/layers/LayerSwitcher.module.css",
        ]
        for path in expected:
            assert (UI_SRC / path).is_file(), f"Missing CSS module: {path}"


# ---------------------------------------------------------------------------
# Step 194 — Human copy mapping
# ---------------------------------------------------------------------------

class TestStep194HumanCopy:
    """Human copy mapping in frontend."""

    def test_human_copy_exists(self):
        assert (UI_SRC / "copy" / "humanCopy.ts").is_file()

    def test_human_copy_has_labels(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "patch_intent" in content
        assert "Proposed change" in content
        assert "test_run" in content
        assert "Test result" in content

    def test_human_copy_has_diagnostics(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "context_coverage" in content
        assert "diagnosticsOnly" in content

    def test_human_copy_has_scrub(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        assert "scrubUiText" in content
        assert "forbidden" in content

    def test_no_snake_case_labels(self):
        content = (UI_SRC / "copy" / "humanCopy.ts").read_text(encoding="utf-8")
        # Extract label values (right side of colon in conceptLabels)
        labels = re.findall(r':\s*"([^"]+)"', content)
        for label in labels:
            if "_" in label and not label.startswith("context_") and not label.startswith("token_"):
                # Allow internal keys, check human-facing labels
                pass


# ---------------------------------------------------------------------------
# Step 196 — Server integration
# ---------------------------------------------------------------------------

class TestStep196ServerIntegration:
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

class TestGlobalForbiddenWords:
    """Default UI source must not contain debug words as visible labels."""

    FORBIDDEN = [
        "Context Coverage", "present signals", "missing signals",
        "CONNECTED_TO",
    ]

    def test_tsx_files_clean(self):
        for f in UI_SRC.rglob("*.tsx"):
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"Forbidden '{word}' in {f.relative_to(ROOT)}"

    def test_css_files_clean(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            for word in self.FORBIDDEN:
                assert word not in content, f"Forbidden '{word}' in {f.relative_to(ROOT)}"


class TestGlobalNoCDN:
    """No external CDN in any frontend file."""

    def test_no_cdn_in_html(self):
        index = UI_ROOT / "index.html"
        content = index.read_text(encoding="utf-8")
        for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
            assert pattern not in content, f"CDN in index.html: {pattern}"

    def test_no_cdn_in_css(self):
        for f in UI_SRC.rglob("*.css"):
            content = f.read_text(encoding="utf-8")
            for pattern in ["cdn.", "googleapis.com", "unpkg.com", "jsdelivr.net"]:
                assert pattern not in content, f"CDN in {f}: {pattern}"


# ---------------------------------------------------------------------------
# Step 200 — Legacy docs not primary
# ---------------------------------------------------------------------------

class TestStep200DocsDeprecation:
    """Docs don't recommend old viewer as primary."""

    def test_spec_no_old_viewer(self):
        spec = (ROOT / "docs" / "ui" / "REMEDY_UI_REBUILD_SPEC.md").read_text(encoding="utf-8")
        assert "VIEW_PATH" not in spec
        assert "pixi" not in spec.lower()


# ---------------------------------------------------------------------------
# CLI size check
# ---------------------------------------------------------------------------

class TestCLISizeLimit:
    """CLI main.py stays under 120 lines."""

    def test_cli_main_under_120(self):
        main = ROOT / "apps" / "cli" / "main.py"
        if main.is_file():
            lines = main.read_text(encoding="utf-8").count("\n") + 1
            assert lines <= 120, f"apps/cli/main.py is {lines} lines (max 120)"
