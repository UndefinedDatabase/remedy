"""Guard: UI design does not drift from target direction.

Prevents common regressions:
- Fifth main row
- ProjectSummaryCard in main grid
- Missing project card in right panel
- Oversized timeline
- Missing metrics
- Mutation buttons
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

RIGHT_PANEL = ROOT / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.tsx"
SHELL_TSX = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
SHELL_CSS = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.module.css"
TIMELINE_CSS = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.module.css"
METRICS_TSX = ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.tsx"
PROJECT_CARD = ROOT / "apps" / "ui" / "src" / "components" / "pipeline" / "ProjectSummaryCard.tsx"
PIPELINE_CSS = ROOT / "apps" / "ui" / "src" / "components" / "pipeline" / "Pipeline.module.css"


class TestRightPanelCompact:
    """Right panel is compact operator stack."""

    def test_project_summary_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "ProjectSummaryCard" in content

    def test_pipeline_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "PipelinePanel" in content

    def test_activity_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "ActivityFeedCard" in content

    def test_tasks_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "TaskChecklistCard" in content

    def test_no_mutation_buttons_in_right_panel(self):
        content = RIGHT_PANEL.read_text()
        assert "AddTaskButton" not in content


class TestProjectCardNotInMain:
    """ProjectSummaryCard must not be in main grid."""

    def test_no_project_card_in_main(self):
        content = SHELL_TSX.read_text()
        main_match = re.search(
            r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>",
            content, re.DOTALL,
        )
        assert main_match
        assert "ProjectSummaryCard" not in main_match.group(1)


class TestProjectCardAccessible:
    """ProjectSummaryCard copy button must be keyboard accessible."""

    def test_command_uses_button_not_code(self):
        content = PROJECT_CARD.read_text()
        assert "<button" in content
        assert "aria-label" in content

    def test_null_summary_returns_null(self):
        content = PROJECT_CARD.read_text()
        assert "if (!summary) return null" in content


class TestTimelineCompact:
    """Bottom timeline should be slim."""

    def test_timeline_uses_six_phases(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.tsx").read_text()
        assert "repeat(6" in tsx or "phases.map" in tsx

    def test_timeline_phase_icon_not_oversized(self):
        css = TIMELINE_CSS.read_text()
        icon_match = re.search(r"\.phaseIcon\s*\{([^}]+)\}", css)
        assert icon_match
        icon_css = icon_match.group(1)
        size_match = re.search(r"width:\s*(\d+)px", icon_css)
        assert size_match
        assert int(size_match.group(1)) <= 28


class TestFiveMetrics:
    """Top metrics bar should have five metrics."""

    def test_metrics_grid_five_columns(self):
        css = (ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.module.css").read_text()
        assert "repeat(5" in css


class TestNoRawContentInCards:
    """UI cards must not display raw content patterns."""

    def test_project_card_no_raw_patterns(self):
        content = PROJECT_CARD.read_text()
        forbidden = ["raw_output", "command_output", "raw_stdout", "raw_stderr",
                      "approval_reason", "diff_preview", "traceback"]
        for pattern in forbidden:
            assert pattern not in content, f"ProjectSummaryCard contains '{pattern}'"

    def test_pipeline_css_no_debug_classes(self):
        content = PIPELINE_CSS.read_text()
        assert "debugWall" not in content
        assert "rawOutput" not in content
