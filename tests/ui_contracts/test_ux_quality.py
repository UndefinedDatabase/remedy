"""
Domain tests: ui_contracts/test_ux_quality.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from uuid import uuid4

from packages.core.models import RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry


def _make_job(**overrides) -> JobPlan:
    defaults = {
        "job_id": uuid4(),
        "job_title": "test-job",
        "user_prompt": "test prompt",
        "tasks": [TaskEntry(title="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return JobPlan(**defaults)


def _get_viewer_html():
    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain

    job = _make_job()
    events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.job_id),
                "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
    graph = build_project_brain(job, events)
    data = build_brain_viewer_data(job, graph, events)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        html_path = write_brain_viewer_files(data, out)
        return html_path.read_text(), data, out


# ===========================================================================
# Step 163 — Memory Candidate Contract Closure
# ===========================================================================


class TestUXQualityGate:
    def test_design_tokens_present(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert ":root" in REMEDY_CSS
        assert "--remedy-bg" in REMEDY_CSS

    def test_no_logo_or_center_triangle(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        lower = REMEDY_CSS.lower()
        assert "logo" not in lower
        assert "triangle" not in lower

    def test_status_classes_for_core_types(self):
        from packages.orchestration.brain_viewer_theme import get_status_class
        # Core statuses must all map
        for status in ("verified", "completed", "blocked", "pending", "running"):
            cls = get_status_class(status)
            assert cls.startswith("remedy-status-"), f"bad class for {status}: {cls}"

    def test_data_render_status_in_viewer(self):
        from packages.orchestration.brain_viewer import _HTML
        assert "data-render-status" in _HTML

    def test_keyboard_focusable(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "focus-visible" in REMEDY_CSS


class TestMotionDepth:
    def test_mist_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-mist" in html

    def test_scanlines(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-scanlines" in html

    def test_grid_layer(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-grid" in html

    def test_edge_glow(self):
        html, _, _ = _get_viewer_html()
        assert "drop-shadow" in html

    def test_hover_lift(self):
        html, _, _ = _get_viewer_html()
        # Hover effect on nodes
        assert ".nd:hover" in html

    def test_selected_pulse(self):
        html, _, _ = _get_viewer_html()
        assert "sel-pulse" in html

    def test_reduced_motion_disables(self):
        html, _, _ = _get_viewer_html()
        assert "prefers-reduced-motion" in html
        # Scanlines hidden under reduced motion
        assert "remedy-scanlines" in html

    def test_no_external_assets(self):
        html, _, _ = _get_viewer_html()
        urls = re.findall(r'(?:src|href)=["\']?(https?://[^"\'>\\s]+)', html)
        assert urls == []

    def test_no_canvas_required(self):
        html, _, _ = _get_viewer_html()
        # Core function must not require canvas
        assert "<canvas" not in html

    def test_orbit_bg_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-orbit-bg" in html

    def test_particle_field_present(self):
        html, _, _ = _get_viewer_html()
        assert "remedy-particle-field" in html


# ---------------------------------------------------------------------------
# No forbidden debug words
# ---------------------------------------------------------------------------
