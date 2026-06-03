"""Guard: UI design does not drift from target direction.

Prevents common regressions:
- Fifth main row
- Worker/Pipeline in primary right panel
- Missing activity/tasks
- Oversized timeline
- Missing metrics
- Mutation buttons
- CLI commands in primary UX
- Fake graph nodes
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

RIGHT_PANEL = ROOT / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.tsx"
SHELL_TSX = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
SHELL_CSS = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.module.css"
TIMELINE_TSX = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.tsx"
TIMELINE_CSS = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.module.css"
METRICS_TSX = ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.tsx"
GRAPH_CANVAS = ROOT / "apps" / "ui" / "src" / "components" / "graph" / "BrainGraphCanvas.tsx"
PIPELINE_CSS = ROOT / "apps" / "ui" / "src" / "components" / "pipeline" / "Pipeline.module.css"


class TestRightPanelUserFirst:
    """Right panel shows user-facing cards, not internal machinery."""

    def test_activity_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "ActivityFeedCard" in content

    def test_tasks_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "TaskChecklistCard" in content

    def test_needs_attention_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "NeedsAttentionCard" in content

    def test_no_primary_worker_status(self):
        content = RIGHT_PANEL.read_text()
        assert "WorkerStatusMini" not in content or "advancedSection" in content

    def test_no_primary_pipeline_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "PipelinePanel" not in content or "advancedSection" in content

    def test_no_mutation_buttons(self):
        content = RIGHT_PANEL.read_text()
        assert "AddTaskButton" not in content

    def test_advanced_details_collapsed_by_default(self):
        content = RIGHT_PANEL.read_text()
        assert "showAdvanced" in content
        assert "useState(false)" in content


class TestNoProjectCardInMain:
    def test_no_project_card_in_main(self):
        content = SHELL_TSX.read_text()
        main_match = re.search(
            r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>",
            content, re.DOTALL,
        )
        assert main_match
        assert "ProjectSummaryCard" not in main_match.group(1)


class TestGraphRealNodesOnly:
    """Graph must use real task data, not fake layout dots."""

    def test_graph_canvas_exists(self):
        assert GRAPH_CANVAS.exists()

    def test_graph_uses_dashboard_tasks(self):
        content = GRAPH_CANVAS.read_text()
        assert "dashboard.tasks" in content

    def test_graph_no_layout_only_nodes(self):
        content = GRAPH_CANVAS.read_text()
        assert "sourceKind" not in content
        assert "layout_only" not in content

    def test_graph_has_hover_tooltip(self):
        content = GRAPH_CANVAS.read_text()
        assert "tooltip" in content.lower()
        assert "hovered" in content.lower() or "hoveredId" in content


class TestTimelineCanonical:
    """Timeline must render six canonical phases."""

    def test_timeline_has_six_canonical_phases(self):
        content = TIMELINE_TSX.read_text()
        assert "CANONICAL_PHASES" in content
        for phase in ("job", "planning", "build", "test", "review", "finalized"):
            assert f'"{phase}"' in content

    def test_timeline_uses_custom_glyphs(self):
        content = TIMELINE_TSX.read_text()
        assert "PhaseGlyph" in content

    def test_timeline_no_fake_micro_events(self):
        content = TIMELINE_TSX.read_text()
        assert "Array.from({ length: 28" not in content

    def test_timeline_has_progress_track(self):
        css = TIMELINE_CSS.read_text()
        assert "trackProgress" in css


class TestFiveMetrics:
    def test_metrics_grid_five_columns(self):
        css = (ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.module.css").read_text()
        assert "repeat(5" in css

    def test_token_tooltip_keyboard_accessible(self):
        content = METRICS_TSX.read_text()
        assert "tabIndex" in content


class TestNoCLIInPrimaryUX:
    """Primary UI should not show CLI commands."""

    def test_right_panel_no_remedy_worker_command(self):
        content = RIGHT_PANEL.read_text()
        primary = content.split("advancedSection")[0] if "advancedSection" in content else content
        assert "remedy worker run" not in primary

    def test_right_panel_no_remedy_patch_command(self):
        content = RIGHT_PANEL.read_text()
        primary = content.split("advancedSection")[0] if "advancedSection" in content else content
        assert "remedy patch" not in primary


class TestNoRawContentInCards:
    def test_graph_canvas_no_raw_patterns(self):
        content = GRAPH_CANVAS.read_text()
        forbidden = ["raw_output", "command_output", "raw_stdout", "raw_stderr",
                      "approval_reason", "diff_preview", "traceback"]
        for pattern in forbidden:
            assert pattern not in content

    def test_pipeline_css_no_debug_classes(self):
        content = PIPELINE_CSS.read_text()
        assert "debugWall" not in content
        assert "rawOutput" not in content
