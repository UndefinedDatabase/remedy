"""Guard: PhaseTimeline matches target screenshot contract.

Ensures:
- Phase header always uses PhaseGlyph (never replaced with TaskDoneGlyph)
- TaskDoneGlyph only in rail markers
- No fallbackEventsFromTasks
- Event rail absent when no real events
- Six phase icons visible
- Correct icon glyphs
- No overflow: hidden
- State classes exist
- Timeline CSS structure is correct
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
TIMELINE_TSX = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.tsx"
TIMELINE_CSS = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "PhaseTimeline.module.css"
GLYPHS_TSX = ROOT / "apps" / "ui" / "src" / "components" / "icons" / "RemedyGlyphs.tsx"
UI_SERVER = ROOT / "packages" / "orchestration" / "ui_server.py"
TYPES_TS = ROOT / "apps" / "ui" / "src" / "api" / "types.ts"
NORMALIZER_TS = ROOT / "apps" / "ui" / "src" / "api" / "remedyApi.ts"


class TestPhaseHeaderAlwaysUsesPhaseGlyph:
    """Phase icons must NEVER be replaced with checkmarks in header."""

    def test_header_uses_phase_glyph_not_task_done_glyph(self):
        content = TIMELINE_TSX.read_text()
        # Find phaseHeader section — look for the className reference to end of its div
        header_match = re.search(r'(styles\.phaseHeader.*?)(styles\.rail|styles\.eventRail)', content, re.DOTALL)
        assert header_match, "phaseHeader section not found"
        header = header_match.group(1)
        assert "PhaseGlyph" in header, "phaseHeader must use PhaseGlyph"
        # TaskDoneGlyph must NOT appear in header
        assert "TaskDoneGlyph" not in header, (
            "TaskDoneGlyph must NOT appear in phaseHeader — done state is visual class, not icon replacement"
        )

    def test_task_done_glyph_only_in_rail_marker(self):
        content = TIMELINE_TSX.read_text()
        # TaskDoneGlyph should only appear in import or rail markers
        occurrences = [m.start() for m in re.finditer(r'<TaskDoneGlyph', content)]
        for pos in occurrences:
            context = content[max(0, pos - 300):pos + 100]
            assert "phaseMarker" in context or "markerCheck" in context or "rail" in context.lower(), (
                f"<TaskDoneGlyph at position {pos} appears outside rail marker context"
            )


class TestNoFakeEventsFromTasks:
    """Event rail must not create dots from tasks."""

    def test_no_fallback_events_from_tasks(self):
        content = TIMELINE_TSX.read_text()
        assert "fallbackEventsFromTasks" not in content, (
            "fallbackEventsFromTasks must be removed — events come only from backend"
        )

    def test_event_rail_always_rendered(self):
        content = TIMELINE_TSX.read_text()
        assert "eventRail" in content, "Event rail must exist in JSX"
        # Event rail must NOT be wrapped in hasEvents conditional
        # It should be unconditionally rendered; only dots are conditional on real events
        rail_section = content[content.index("eventRail"):content.index("eventRail") + 500]
        assert "hasEvents" not in rail_section, (
            "Event rail must be always rendered, not wrapped in hasEvents conditional"
        )

    def test_no_task_to_event_mapping_in_timeline(self):
        content = TIMELINE_TSX.read_text()
        assert "KIND_TYPE" not in content, (
            "KIND_TYPE mapping (task kind to event type) must not exist in PhaseTimeline"
        )

    def test_normalizer_does_not_create_events_from_tasks(self):
        content = NORMALIZER_TS.read_text()
        assert "fallbackEventsFromTasks" not in content
        # normalizeTimelineEvents should return [] for missing data, not create from tasks
        assert "normalizeTimelineEvents" in content


class TestCanonicalPhases:
    def test_six_canonical_phases(self):
        content = TIMELINE_TSX.read_text()
        match = re.search(r'CANONICAL_PHASES[^=]*=\s*\[([^\]]+)\]', content)
        assert match, "CANONICAL_PHASES not found"
        phases = re.findall(r'"(\w+)"', match.group(1))
        assert phases == ["job", "planning", "build", "test", "review", "finalized"]

    def test_phase_header_is_grid_six_columns(self):
        content = TIMELINE_CSS.read_text()
        assert "repeat(6, 1fr)" in content, "Phase header must be 6-column grid"


class TestTimelineCSS:
    def test_no_overflow_hidden(self):
        content = TIMELINE_CSS.read_text()
        # Find .timeline rule
        timeline_match = re.search(r'\.timeline\s*\{([^}]+)\}', content)
        assert timeline_match, ".timeline CSS rule not found"
        timeline_css = timeline_match.group(1)
        assert "overflow: hidden" not in timeline_css, (
            "Timeline must not use overflow: hidden — it clips glow effects"
        )

    def test_has_event_rail_with_dashed_line(self):
        content = TIMELINE_CSS.read_text()
        assert "eventRailLine" in content or "eventRail" in content
        assert "dashed" in content, "Event line must be dashed"

    def test_has_phase_icon_shell(self):
        content = TIMELINE_CSS.read_text()
        assert "phaseIconShell" in content, "Must have phaseIconShell class"
        shell_match = re.search(r'\.phaseIconShell\s*\{([^}]+)\}', content)
        assert shell_match, "phaseIconShell CSS rule not found"
        assert "border-radius" in shell_match.group(1)

    def test_state_classes_exist(self):
        content = TIMELINE_CSS.read_text()
        assert ".isDone" in content, "isDone class must exist"
        assert ".isCurrent" in content, "isCurrent class must exist"
        assert ".isPending" in content, "isPending class must exist"

    def test_event_dots_have_borders(self):
        content = TIMELINE_CSS.read_text()
        dot_match = re.search(r'\.eventDot\s*\{([^}]+)\}', content)
        assert dot_match, "eventDot CSS rule not found"
        assert "border" in dot_match.group(1), "Event dots must have borders"


class TestTimelineIcons:
    def test_build_icon_is_code_glyph(self):
        content = GLYPHS_TSX.read_text()
        assert "polyline" in content, "Build icon must use polyline for code brackets"
        assert "M7 4L4 12h8L9 4" not in content, "Build icon must not be triangle"

    def test_review_icon_is_person(self):
        content = GLYPHS_TSX.read_text()
        assert "M4 4h8v3H4z M6 10h4" not in content, "Review icon must not be old document"

    def test_six_phase_icons_defined(self):
        content = GLYPHS_TSX.read_text()
        for phase in ["job", "planning", "build", "test", "review", "finalized"]:
            # Keys can be unquoted in object literals: `job:` or `"job":`
            assert f'{phase}:' in content or f'"{phase}"' in content, (
                f"PhaseGlyph must define icon for '{phase}'"
            )


class TestTimelineTypes:
    def test_timeline_event_has_state_and_title(self):
        content = TYPES_TS.read_text()
        assert "RemedyTimelineEvent" in content
        assert "title: string" in content, "RemedyTimelineEvent must have title field"
        assert "state: RemedyState" in content, "RemedyTimelineEvent must have state field"

    def test_timeline_phase_type_exists(self):
        content = TYPES_TS.read_text()
        assert "RemedyTimelinePhase" in content

    def test_dashboard_has_timeline_events(self):
        content = TYPES_TS.read_text()
        assert "timelineEvents" in content


class TestBackendPhases:
    def test_backend_has_six_phases(self):
        content = UI_SERVER.read_text()
        phase_ids = re.findall(r'"id":\s*"(\w+)".*?"source":\s*"derived"', content)
        assert "job" in phase_ids, "Backend must include 'job' phase"
        assert "finalized" in phase_ids, "Backend must include 'finalized' phase"
        assert len(phase_ids) >= 6

    def test_backend_timeline_events_have_title_and_state(self):
        content = UI_SERVER.read_text()
        assert '"title"' in content, "Backend timeline events must have title"
        assert '"state"' in content, "Backend timeline events must have state"
        assert '"cycle"' in content, "Backend timeline events must have cycle"

    def test_finalized_gate_checks_pending_tasks(self):
        content = UI_SERVER.read_text()
        assert "pending_task_count" in content, "Finalized gate must check pending tasks"
        assert "blocked_task_count" in content, "Finalized gate must check blocked tasks"
        assert "pending_approvals" in content, "Finalized gate must check pending approvals"


class TestOrchestratorLoopContract:
    def test_orchestrator_loop_doc_exists(self):
        doc = ROOT / "docs" / "orchestrator-loop.md"
        assert doc.exists(), "docs/orchestrator-loop.md must exist"
        content = doc.read_text()
        assert "Build/Test/Review" in content, "Must describe iterative loop"
        assert "Finalized" in content, "Must describe finalized gate"
        assert "proposed" in content.lower(), "Must describe proposed tasks"

    def test_proposed_task_type_exists(self):
        content = TYPES_TS.read_text()
        assert "RemedyProposedTask" in content, "RemedyProposedTask type must exist"
        assert "RemedyProposedTaskSource" in content
        assert "RemedyProposedTaskStatus" in content


SHELL_CSS = ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.module.css"
COMMAND_CSS = ROOT / "apps" / "ui" / "src" / "components" / "command" / "CommandBar.module.css"
FILTER_CSS = ROOT / "apps" / "ui" / "src" / "components" / "graph" / "GraphFilterChips.module.css"
DOCK_CSS = ROOT / "apps" / "ui" / "src" / "components" / "rail" / "SideIconDock.module.css"
METRICS_CSS = ROOT / "apps" / "ui" / "src" / "components" / "metrics" / "TopMetricsBar.module.css"


class TestVisualRegressionA6:
    """Tests for the exact visual regression from addendum A6."""

    def test_event_rail_rendered_without_has_events_gate(self):
        content = TIMELINE_TSX.read_text()
        # Legend must also be always rendered
        assert "legend" in content
        # Neither eventRail nor legend should be inside a hasEvents conditional
        lines = content.split("\n")
        in_has_events = False
        for line in lines:
            stripped = line.strip()
            if "hasEvents" in stripped and "&&" in stripped:
                in_has_events = True
            if in_has_events and ("eventRail" in stripped or "legend" in stripped):
                pytest.fail(f"eventRail or legend inside hasEvents block: {stripped}")
            if in_has_events and stripped.startswith(")"):
                in_has_events = False

    def test_legend_always_rendered(self):
        content = TIMELINE_TSX.read_text()
        assert "styles.legend" in content, "Legend must be in JSX"

    def test_done_phases_use_phase_glyph_in_header(self):
        content = TIMELINE_TSX.read_text()
        header_match = re.search(r'(styles\.phaseHeader.*?)(styles\.rail)', content, re.DOTALL)
        assert header_match
        header = header_match.group(1)
        assert "PhaseGlyph" in header
        assert "TaskDoneGlyph" not in header

    def test_timeline_css_border_radius_28(self):
        content = TIMELINE_CSS.read_text()
        timeline_match = re.search(r'\.timeline\s*\{([^}]+)\}', content)
        assert timeline_match
        assert "border-radius: 28px" in timeline_match.group(1), "Timeline must have border-radius: 28px"

    def test_shell_timeline_row_height_at_least_150(self):
        content = SHELL_CSS.read_text()
        # Check the grid-template-rows has a timeline row with min >= 150
        match = re.search(r'clamp\((\d+)px.*?(\d+)px\)\s*;', content)
        # Last clamp in grid-template-rows
        clamps = re.findall(r'clamp\((\d+)px', content)
        assert any(int(v) >= 150 for v in clamps), (
            f"Shell timeline row must have min >= 150px, found clamps: {clamps}"
        )

    def test_command_buttons_are_circular(self):
        content = COMMAND_CSS.read_text()
        assert "border-radius: 50%" in content or "border-radius: 999px" in content, (
            "Command bar buttons must be circular (50% or 999px)"
        )

    def test_filter_chips_are_pills(self):
        content = FILTER_CSS.read_text()
        assert "border-radius: 999px" in content, "Filter chips must be pill shaped"

    def test_dock_buttons_are_circular(self):
        content = DOCK_CSS.read_text()
        assert "border-radius: 50%" in content or "border-radius: 999px" in content, (
            "Dock buttons must be circular"
        )

    def test_metric_icon_shell_rounded(self):
        content = METRICS_CSS.read_text()
        icon_match = re.search(r'\.iconBox\s*\{([^}]+)\}', content)
        assert icon_match, "iconBox CSS rule not found"
        assert "border-radius" in icon_match.group(1)
        # Must be >= 10px, not 4px or 0
        radius_match = re.search(r'border-radius:\s*(\d+)px', icon_match.group(1))
        assert radius_match and int(radius_match.group(1)) >= 10, (
            "Metric icon shell border-radius must be >= 10px"
        )

    def test_finalized_gate_checks_unresolved_proposals(self):
        content = UI_SERVER.read_text()
        assert "unresolved_proposals" in content, (
            "Finalized gate must check unresolved proposed tasks"
        )
