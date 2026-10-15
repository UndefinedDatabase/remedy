"""
Domain tests: ui_contracts/test_graph_architecture.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

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


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────


def _make_job_s74(**overrides) -> JobPlan:
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


class TestVisualSystem:
    def test_design_tokens_present(self):
        from packages.orchestration.brain_viewer_theme import DESIGN_TOKENS
        required_vars = [
            "--remedy-bg", "--remedy-fg", "--remedy-teal", "--remedy-cyan",
            "--remedy-panel", "--remedy-muted", "--remedy-risk", "--remedy-warning",
            "--remedy-proof", "--remedy-memory",
        ]
        for var in required_vars:
            assert var in DESIGN_TOKENS, f"missing token: {var}"

    def test_css_variables_in_css(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        for var in ["--remedy-bg", "--remedy-fg", "--remedy-teal", "--remedy-cyan",
                     "--remedy-panel", "--remedy-muted", "--remedy-risk",
                     "--remedy-warning", "--remedy-proof", "--remedy-memory"]:
            assert var in REMEDY_CSS, f"missing CSS var: {var}"

    def test_required_classes(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        required_classes = [
            "remedy-shell", "remedy-orbit-bg", "remedy-particle-field",
            "remedy-glass-panel", "remedy-proof-chain", "remedy-node-card",
            "remedy-node-status", "remedy-timeline", "remedy-decision-panel",
            "remedy-readiness-panel",
        ]
        for cls in required_classes:
            assert cls in REMEDY_CSS, f"missing class: {cls}"

    def test_no_external_urls(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "http://" not in REMEDY_CSS
        assert "https://" not in REMEDY_CSS
        assert "cdn." not in REMEDY_CSS.lower()

    def test_no_trademark_assets(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        lower = REMEDY_CSS.lower()
        assert "assassin" not in lower
        assert "abstergo" not in lower
        assert "ubisoft" not in lower

    def test_reduced_motion(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        assert "prefers-reduced-motion" in REMEDY_CSS

    def test_status_classes_exist(self):
        from packages.orchestration.brain_viewer_theme import STATUS_CLASSES
        assert "verified" in STATUS_CLASSES
        assert "blocked" in STATUS_CLASSES
        assert "pending" in STATUS_CLASSES
        assert "running" in STATUS_CLASSES
        assert "memory" in STATUS_CLASSES
        assert "future" in STATUS_CLASSES

    def test_get_status_class(self):
        from packages.orchestration.brain_viewer_theme import get_status_class
        assert "verified" in get_status_class("completed")
        assert "risk" in get_status_class("blocked")
        assert "decision" in get_status_class("pending")
        assert "memory" in get_status_class("anything", "memory_placeholder")

    def test_layer_classes(self):
        from packages.orchestration.brain_viewer_theme import LAYER_CLASSES
        assert "job" in LAYER_CLASSES
        assert "patch_intent" in LAYER_CLASSES
        assert "test_run" in LAYER_CLASSES
        assert "decision_queue" in LAYER_CLASSES

    def test_no_raw_leaks_in_css(self):
        from packages.orchestration.brain_viewer_theme import REMEDY_CSS
        for forbidden in ("stdout", "stderr", "raw_output", "Traceback",
                          "diff_preview", "approval_reason", "command_output"):
            assert forbidden not in REMEDY_CSS


# ── Step 73: Brain Viewer Shell ─────────────────────────────────────────


class TestSpatialLayout:
    def test_nodes_have_zone(self):
        _, data, _ = _get_viewer_html()
        for node in data.graph["nodes"]:
            assert "zone" in node, f"node {node['id']} missing zone"

    def test_layout_deterministic(self):
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
        )
        from packages.orchestration.project_brain import build_project_brain
        job = _make_job_s74()
        events = []
        graph = build_project_brain(job, events)
        d1 = build_brain_viewer_data(job, graph, events)
        d2 = build_brain_viewer_data(job, graph, events)
        assert d1.positions == d2.positions

    def test_zone_labels_in_viewer(self):
        html, _, _ = _get_viewer_html()
        assert "zone-label" in html

    def test_zone_map_covers_types(self):
        from packages.orchestration.brain_viewer import _ZONE_MAP
        required = ["job", "task", "artifact", "patch_intent", "memory_placeholder",
                     "mcp_placeholder", "decision_queue", "test_run"]
        for t in required:
            assert t in _ZONE_MAP, f"missing zone for {t}"

    def test_future_nodes_muted(self):
        html, _, _ = _get_viewer_html()
        assert "future-edge" in html or "future" in html

    def test_edge_types_distinguished(self):
        html, _, _ = _get_viewer_html()
        assert "proof-edge" in html
        assert "blocked-edge" in html
        assert "future-edge" in html

    def test_no_raw_leaks_in_viewer(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        html, _, _ = _get_viewer_html()
        findings = find_forbidden_surface_tokens(html)
        assert findings == []


# ---------------------------------------------------------------------------
# Step 240 — Better data normalization
# ---------------------------------------------------------------------------
