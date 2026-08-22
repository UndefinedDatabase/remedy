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
        # New design pack: event chips use custom code/flask/person glyphs.
        content = TIMELINE_TSX.read_text()
        assert "CodeOrbGlyph" in content
        assert "FlaskGlyph" in content
        assert "PersonGlyph" in content

    def test_timeline_no_fake_micro_events(self):
        content = TIMELINE_TSX.read_text()
        assert "Array.from({ length: 28" not in content

    def test_timeline_has_progress_track(self):
        css = TIMELINE_CSS.read_text()
        assert "railFill" in css or "trackProgress" in css


class TestFiveMetrics:
    def test_metrics_bar_is_flex_row(self):
        # New design pack: metric bar is a flex row of 7 metrics
        # (open/planned/done/progress/tests/proof/tokens), not a 5-column grid.
        css = (ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.module.css").read_text()
        bar_match = re.search(r"\.bar\s*\{([^}]+)\}", css)
        assert bar_match and "display: flex" in bar_match.group(1)
        tsx = METRICS_TSX.read_text()
        assert "tests:" in tsx and "proof:" in tsx  # icon map covers new metrics

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


class TestGraphStableViewBox:
    """Graph must use stable viewBox, not dynamic scaling."""

    def test_stable_viewbox(self):
        content = GRAPH_CANVAS.read_text()
        assert "STAGE_W" in content or 'viewBox="' in content
        assert "Math.min(...xs)" not in content

    def test_root_fixed_radius(self):
        content = GRAPH_CANVAS.read_text()
        assert "ROOT_R" in content

    def test_no_dynamic_viewbox_from_nodes(self):
        content = GRAPH_CANVAS.read_text()
        assert "minX" not in content or "STAGE_W" in content


class TestGraphKeyboardAccess:
    """Graph nodes must be keyboard accessible."""

    def test_task_nodes_focusable(self):
        content = GRAPH_CANVAS.read_text()
        assert "tabIndex" in content

    def test_task_nodes_have_aria_label(self):
        content = GRAPH_CANVAS.read_text()
        assert "aria-label" in content


class TestGraphTooltipNearNode:
    """Tooltip should appear near hovered node, not fixed bottom."""

    def test_tooltip_uses_node_position(self):
        content = GRAPH_CANVAS.read_text()
        assert "tooltipPos" in content or "hovered.x" in content


class TestAgentNowTruth:
    """Agent card must not claim working when idle."""

    def test_agent_idle_not_working(self):
        # Agent status logic now lives in the pure cockpitLogic module.
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "panels" / "AgentNowCard.tsx").read_text()
        logic = (ROOT / "apps" / "ui" / "src" / "cockpitLogic.ts").read_text()
        assert '"Builder is working"' not in tsx and '"Builder is working"' not in logic
        assert "Idle" in logic

    def test_agent_no_mui_icons(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "panels" / "AgentNowCard.tsx").read_text()
        assert "@mui" not in tsx


class TestLogoUsesRemedyMark:
    """Logo must use custom RemedyMark, not NetworkLogoIcon."""

    def test_logo_uses_remedy_mark(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "rail" / "RemedyLogo.tsx").read_text()
        assert "RemedyMark" in tsx
        assert "NetworkLogoIcon" not in tsx


class TestTokenTooltipLayering:
    """Token tooltip must not be clipped."""

    def test_metrics_bar_overflow_visible(self):
        css = (ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.module.css").read_text()
        bar_match = re.search(r"\.bar\s*\{([^}]+)\}", css)
        assert bar_match
        assert "overflow: visible" in bar_match.group(1)


class TestGraphEmptyState:
    """Graph must show empty state when no tasks."""

    def test_empty_state_exists(self):
        content = GRAPH_CANVAS.read_text()
        assert "emptyState" in content

    def test_empty_state_checks_tasks_length(self):
        content = GRAPH_CANVAS.read_text()
        assert "tasks.length === 0" in content


class TestGraphSmallLayout:
    """Graph must handle small task counts well."""

    def test_small_radial_layout(self):
        content = GRAPH_CANVAS.read_text()
        assert "tasks.length <= 8" in content or "radial" in content.lower()


class TestGraphSelectedNode:
    """Graph must support selected node highlight."""

    def test_selected_node_prop(self):
        content = GRAPH_CANVAS.read_text()
        assert "selectedNodeId" in content

    def test_select_ring_style(self):
        css = (ROOT / "apps" / "ui" / "src" / "components" / "graph" / "BrainGraphCanvas.module.css").read_text()
        assert "selectRing" in css


class TestNoMuiInPrimaryDashboard:
    """Primary dashboard components must not import MUI."""

    def test_metrics_no_mui(self):
        content = METRICS_TSX.read_text()
        assert "@mui" not in content

    def test_command_bar_no_mui(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "command" / "CommandBar.tsx").read_text()
        assert "@mui" not in tsx

    def test_activity_feed_no_mui(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "panels" / "ActivityFeedCard.tsx").read_text()
        assert "@mui" not in tsx

    def test_task_checklist_no_mui(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "panels" / "TaskChecklistCard.tsx").read_text()
        assert "@mui" not in tsx

    def test_side_icon_dock_no_mui(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "rail" / "SideIconDock.tsx").read_text()
        assert "@mui" not in tsx

    def test_degraded_banner_no_mui(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "shell" / "DegradedBanner.tsx").read_text()
        assert "@mui" not in tsx


class TestTaskOutcomeFields:
    """Task items must include outcome fields in types."""

    def test_outcome_summary_in_types(self):
        types = (ROOT / "apps" / "ui" / "src" / "api" / "types.ts").read_text()
        assert "outcomeSummary" in types

    def test_changed_files_in_types(self):
        types = (ROOT / "apps" / "ui" / "src" / "api" / "types.ts").read_text()
        assert "changedFilesCount" in types

    def test_test_status_in_types(self):
        types = (ROOT / "apps" / "ui" / "src" / "api" / "types.ts").read_text()
        assert "testStatus" in types


class TestDetailPanelOutcome:
    """Task detail must show outcome, not internal machinery."""

    def test_no_next_safe_action(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx").read_text()
        assert "Next safe action" not in tsx

    def test_has_outcome_section(self):
        # New design pack: the outcome section is labeled "Result".
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx").read_text()
        assert "Result" in tsx

    def test_no_cli_command_primary(self):
        tsx = (ROOT / "apps" / "ui" / "src" / "components" / "detail" / "DetailPopover.tsx").read_text()
        assert "next.command" not in tsx


class TestEveryCustomPropertyResolves:
    """R-0661. A `var(--x)` with no definition and no fallback makes a browser
    drop the whole declaration silently, and nothing in this repository renders
    CSS, so the failure is invisible to every other suite. F021 R31 shipped
    exactly that and the pill rendered square.

    This is an ALLOWLIST rather than an emptiness assertion on purpose: four
    properties were already unresolved before F021 began, each needing a value
    decided against the design reference, and R-0364 forbids ordering a gate
    that is red before the round that adds it. The set may shrink freely; it
    cannot grow without turning this red."""

    KNOWN_UNRESOLVED = {
        "--remedy-mono",
        "--remedy-warning-bg",
        "--remedy-warning-border",
        "--remedy-warning-fg",
    }

    def _unresolved(self):
        css_root = ROOT / "apps" / "ui" / "src"
        defined, used = set(), {}
        for path in sorted(css_root.rglob("*.css")):
            text = path.read_text(encoding="utf-8")
            defined.update(re.findall(r"(--remedy-[a-z0-9-]+)\s*:", text))
            for name in re.findall(r"var\(\s*(--remedy-[a-z0-9-]+)", text):
                used.setdefault(name, set()).add(path.name)
        return {name: files for name, files in used.items() if name not in defined}

    def test_the_unresolved_set_has_not_grown(self):
        unresolved = self._unresolved()
        new = set(unresolved) - self.KNOWN_UNRESOLVED
        assert not new, (
            "these custom properties are used but never defined under "
            f"apps/ui/src, so the declarations using them are dropped: "
            f"{ {name: sorted(unresolved[name]) for name in sorted(new)} }"
        )

    def test_the_pill_radius_is_defined(self):
        tokens = (ROOT / "apps" / "ui" / "src" / "styles" / "tokens.css").read_text()
        assert "--remedy-radius-pill:" in tokens, (
            "the jump-to-live pill (DECISION F021 D10) asks for this token; "
            "docs/ui/design_reference/tokens.css defines it as 999px"
        )
