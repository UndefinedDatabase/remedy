"""Guard: PhaseTimeline matches target screenshot contract.

Ensures the timeline has correct structure, icons, CSS properties,
and the backend produces all 6 canonical phases plus timeline events.
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


class TestTimelineStructure:
    def test_canonical_phases_are_six(self):
        content = TIMELINE_TSX.read_text()
        match = re.search(r'CANONICAL_PHASES\s*=\s*\[([^\]]+)\]', content)
        assert match, "CANONICAL_PHASES not found"
        phases = re.findall(r'"(\w+)"', match.group(1))
        assert phases == ["job", "planning", "build", "test", "review", "finalized"]

    def test_phase_header_is_grid_six_columns(self):
        content = TIMELINE_CSS.read_text()
        assert "repeat(6, 1fr)" in content, "Phase header must be 6-column grid"

    def test_has_event_rail_with_dashed_line(self):
        content = TIMELINE_CSS.read_text()
        assert "eventLine" in content or "eventRail" in content, "Must have event rail"
        assert "dashed" in content, "Event line must be dashed"

    def test_has_phase_icon_shell_rounded(self):
        content = TIMELINE_CSS.read_text()
        assert "phaseIconShell" in content, "Must have phaseIconShell class"
        shell_match = re.search(r'\.phaseIconShell\s*\{([^}]+)\}', content)
        assert shell_match, "phaseIconShell CSS rule not found"
        assert "border-radius" in shell_match.group(1), "phaseIconShell must have border-radius"

    def test_legend_has_three_entries(self):
        content = TIMELINE_TSX.read_text()
        legend_entries = re.findall(r'legendEntry', content)
        assert len(legend_entries) >= 3, "Legend must have at least 3 entries"

    def test_event_dots_have_borders(self):
        content = TIMELINE_CSS.read_text()
        dot_match = re.search(r'\.eventDot\s*\{([^}]+)\}', content)
        assert dot_match, "eventDot CSS rule not found"
        assert "border" in dot_match.group(1), "Event dots must have borders"


class TestTimelineIcons:
    def test_build_icon_is_code_glyph(self):
        content = GLYPHS_TSX.read_text()
        assert "polyline" in content or "line" in content, "Build icon must use polyline/line for code glyph"
        # Must NOT be a triangle
        assert "M7 4L4 12h8L9 4" not in content, "Build icon must not be triangle"

    def test_review_icon_is_person(self):
        content = GLYPHS_TSX.read_text()
        assert "circle" in content.lower() or "Circle" in content, "Review icon must have circle (head)"
        # Must NOT be old document icon
        assert "M4 4h8v3H4z M6 10h4" not in content, "Review icon must not be old document"


class TestTimelineTypes:
    def test_timeline_event_type_exists(self):
        content = TYPES_TS.read_text()
        assert "RemedyTimelineEvent" in content, "RemedyTimelineEvent type must exist"
        assert "RemedyTimelineEventKind" in content, "RemedyTimelineEventKind type must exist"

    def test_dashboard_has_timeline_events(self):
        content = TYPES_TS.read_text()
        assert "timelineEvents" in content, "RemedyDashboard must have timelineEvents field"


class TestBackendPhases:
    def test_backend_has_six_phases(self):
        content = UI_SERVER.read_text()
        phase_ids = re.findall(r'"id":\s*"(\w+)".*?"source":\s*"derived"', content)
        assert "job" in phase_ids, "Backend must include 'job' phase"
        assert "finalized" in phase_ids, "Backend must include 'finalized' phase"
        assert len(phase_ids) >= 6, f"Backend must have at least 6 phases, found {len(phase_ids)}"

    def test_backend_has_timeline_events(self):
        content = UI_SERVER.read_text()
        assert "_build_timeline_events" in content, "Backend must have _build_timeline_events"
        assert "timeline_events" in content, "Dashboard payload must include timeline_events"
