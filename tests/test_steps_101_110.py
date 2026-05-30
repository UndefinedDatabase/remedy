"""
Tests for Steps 101-110 — UX Contract Reset, Semantic Zoom Direction,
Forward Flow, Task Ribbon, Live Growth, Reviewer Loop, Context/Patch Closure.

Coverage:
  - Smoke contract: new UX markers in index.html
  - Zoom direction: zoom_in_reveals_more, monotonic visible_counts_by_zoom
  - Forward flow: LEFT→RIGHT rank-based layout
  - Task progress ribbon: build_task_progress, status mapping
  - Human node labels: user_title, user_kind in view model
  - Reviewer recommendation loop: run, accept, reject, list, store
  - Source context: text/binary detection, budget
  - Source apply: test loop exists in autorun
  - CLI: review group registration, --after-task arg
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job(task_count: int = 3):
    job = MagicMock()
    job.id = uuid4()
    job.name = "test-job"
    job.state.value = "active"
    job.tasks = []
    job.artifacts = []
    job.metadata = {}
    for i in range(task_count):
        t = MagicMock()
        t.id = uuid4()
        t.task_type = "test_task"
        t.status.value = "completed" if i == 0 else "pending"
        t.metadata = {}
        job.tasks.append(t)
    return job


# ---------------------------------------------------------------------------
# Step 101 — Smoke/UX Contract Reset
# ---------------------------------------------------------------------------

class TestSmokeContractReset:
    def test_index_html_has_brain_canvas_marker(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "remedy-brain-canvas" in html

    def test_index_html_has_task_ribbon_marker(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "remedy-task-ribbon" in html

    def test_index_html_has_task_item_marker(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "remedy-task-item" in html

    def test_index_html_has_semantic_zoom_marker(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "semantic-zoom" in html

    def test_index_html_has_zoom_in_reveals_more(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "zoom-in-reveals-more" in html

    def test_index_html_has_forward_flow(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "forward-flow" in html

    def test_index_html_has_node_detail_card(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "node-detail-card" in html

    def test_index_html_has_reduced_motion(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "reduced-motion" in html

    def test_index_html_has_remedy_light(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "remedy-light" in html

    def test_smoke_script_uses_new_markers(self):
        smoke = (Path(__file__).parent.parent / "scripts" / "remedy_smoke.sh").read_text()
        assert "remedy-brain-canvas" in smoke
        assert "remedy-task-ribbon" in smoke
        assert "zoom-in-reveals-more" in smoke

    def test_smoke_script_no_old_panels(self):
        smoke = (Path(__file__).parent.parent / "scripts" / "remedy_smoke.sh").read_text()
        # Old markers should not appear as primary checks
        assert "'what-happened': 'what-happened' in html" not in smoke
        assert "'explore-brain': 'explore-brain' in html" not in smoke


# ---------------------------------------------------------------------------
# Step 102 — Correct Semantic Zoom Direction
# ---------------------------------------------------------------------------

class TestSemanticZoomDirection:
    def test_zoom_policy_direction(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["zoom_policy"]["direction"] == "zoom_in_reveals_more"

    def test_zoom_policy_fields(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        policy = vm["zoom_policy"]
        assert policy["zoom_out_reduces_complexity"] is True
        assert policy["full_graph_requires_explicit_toggle"] is True

    def test_visible_counts_monotonic_non_decreasing(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(5), [])
        counts = vm["visible_counts_by_zoom"]
        assert isinstance(counts, list)
        assert len(counts) > 0
        for i in range(1, len(counts)):
            assert counts[i] >= counts[i - 1], f"counts[{i}]={counts[i]} < counts[{i-1}]={counts[i-1]}"

    def test_renderer_zoom_direction_in_source(self):
        """Verify renderer.ts maps higher scale to higher zoom level."""
        src = (Path(__file__).parent.parent / "apps" / "ui" / "src" / "brain" / "renderer.ts").read_text()
        # In correct mapping: scale < 0.2 → 0 (fewest nodes when zoomed out)
        assert "if (scale < 0.2) return 0;" in src
        # And scale >= 1.8 → 6 (most nodes when zoomed in)
        assert "return 6;" in src


# ---------------------------------------------------------------------------
# Step 103 — Forward Flow Layout
# ---------------------------------------------------------------------------

class TestForwardFlowLayout:
    def test_layout_direction_right(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        assert vm["direction"] == "RIGHT"

    def test_node_ranks_non_negative(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(3), [])
        for node in vm["nodes"]:
            assert node["rank"] >= 0


# ---------------------------------------------------------------------------
# Step 104 — Task Progress Ribbon
# ---------------------------------------------------------------------------

class TestTaskProgressRibbon:
    def test_build_task_progress_returns_tasks(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(3)
        result = build_task_progress(job, [])
        assert result["version"] == 1
        assert len(result["tasks"]) == 3

    def test_task_status_mapping(self):
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(3)
        result = build_task_progress(job, [])
        statuses = [t["status"] for t in result["tasks"]]
        assert "completed" in statuses
        assert "pending" in statuses

    def test_ribbon_css_classes_in_html(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "remedy-task-completed" in html
        assert "remedy-task-active" in html
        assert "remedy-task-future" in html
        assert "remedy-task-reviewer-suggested" in html

    def test_ribbon_collapsible(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "ribbon-collapse" in html
        assert "ribbon-expand" in html
        assert ".collapsed" in html


# ---------------------------------------------------------------------------
# Step 105 — Human Node Labels
# ---------------------------------------------------------------------------

class TestHumanNodeLabels:
    def test_nodes_have_user_title(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        for node in vm["nodes"]:
            assert "user_title" in node
            assert isinstance(node["user_title"], str)
            assert len(node["user_title"]) > 0

    def test_nodes_have_user_kind(self):
        from packages.orchestration.ui_view_model import build_brain_view_model
        vm = build_brain_view_model(_make_job(), [])
        for node in vm["nodes"]:
            assert "user_kind" in node


# ---------------------------------------------------------------------------
# Step 106 — Atmospheric Motion
# ---------------------------------------------------------------------------

class TestAtmosphericMotion:
    def test_renderer_has_particle_code(self):
        src = (Path(__file__).parent.parent / "apps" / "ui" / "src" / "brain" / "renderer.ts").read_text()
        assert "PARTICLE_COUNT" in src
        assert "particleLayer" in src

    def test_reduced_motion_guard(self):
        src = (Path(__file__).parent.parent / "apps" / "ui" / "src" / "brain" / "renderer.ts").read_text()
        assert "prefers-reduced-motion" in src

    def test_reduced_motion_css(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "prefers-reduced-motion: reduce" in html


# ---------------------------------------------------------------------------
# Step 107 — Live Growth UX
# ---------------------------------------------------------------------------

class TestLiveGrowthUX:
    def test_ui_server_live_state_has_active_task(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job(2)
        result = _build_live_state_json(job)
        assert "active_task_id" in result

    def test_ui_server_has_task_progress_handler(self):
        src = (Path(__file__).parent.parent / "packages" / "orchestration" / "ui_server.py").read_text()
        assert '"task-progress"' in src
        assert "_build_task_progress_json" in src

    def test_follow_toggle_in_html(self):
        html = (Path(__file__).parent.parent / "apps" / "ui" / "index.html").read_text()
        assert "follow-toggle" in html

    def test_main_ts_has_ribbon_polling(self):
        src = (Path(__file__).parent.parent / "apps" / "ui" / "src" / "main.ts").read_text()
        assert "task-progress" in src
        assert "renderRibbon" in src


# ---------------------------------------------------------------------------
# Step 108 — Reviewer Recommendation Loop
# ---------------------------------------------------------------------------

class TestReviewerLoop:
    def test_run_reviewer_returns_list(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job(2)
        recs = run_reviewer(job)
        assert isinstance(recs, list)

    def test_run_reviewer_with_custom_fn(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job(2)

        def custom_reviewer(context):
            return [{"title": "Add test", "task_type": "test", "reason": "coverage", "risk": "low"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        assert len(recs) == 1
        assert recs[0].title == "Add test"

    def test_store_and_list_recommendations(self):
        from packages.orchestration.reviewer import run_reviewer, store_recommendations, list_recommendations
        job = _make_job(1)

        def custom_reviewer(context):
            return [{"title": "Fix bug", "task_type": "fix", "reason": "regression"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        stored = list_recommendations(job)
        assert len(stored) == 1
        assert stored[0]["title"] == "Fix bug"
        assert stored[0]["status"] == "pending"

    def test_accept_recommendation(self):
        from packages.orchestration.reviewer import (
            run_reviewer, store_recommendations, accept_recommendation,
        )
        job = _make_job(1)

        def custom_reviewer(context):
            return [{"title": "Add docs", "task_type": "docs", "reason": "missing"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        rec_id = job.metadata["reviewer_recommendations"][0]["id"]
        initial_task_count = len(job.tasks)
        ok = accept_recommendation(job, rec_id)
        assert ok is True
        assert len(job.tasks) == initial_task_count + 1
        assert job.metadata["reviewer_recommendations"][0]["status"] == "accepted"

    def test_reject_recommendation(self):
        from packages.orchestration.reviewer import (
            run_reviewer, store_recommendations, reject_recommendation,
        )
        job = _make_job(1)

        def custom_reviewer(context):
            return [{"title": "Refactor", "task_type": "refactor", "reason": "tech debt"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        rec_id = job.metadata["reviewer_recommendations"][0]["id"]
        initial_task_count = len(job.tasks)
        ok = reject_recommendation(job, rec_id)
        assert ok is True
        assert len(job.tasks) == initial_task_count  # No new task
        assert job.metadata["reviewer_recommendations"][0]["status"] == "rejected"

    def test_reject_nonexistent(self):
        from packages.orchestration.reviewer import reject_recommendation
        job = _make_job(0)
        ok = reject_recommendation(job, "nonexistent")
        assert ok is False

    def test_max_recommendations(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job(1)

        def many_recs(context):
            return [{"title": f"rec-{i}", "task_type": "test"} for i in range(20)]

        recs = run_reviewer(job, reviewer_fn=many_recs, max_recommendations=3)
        assert len(recs) == 3

    def test_recommendation_fields(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job(1)

        def custom_reviewer(context):
            return [{"title": "t", "task_type": "test", "reason": "r", "risk": "high", "priority": "critical"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        r = recs[0]
        assert r.risk == "high"
        assert r.priority == "critical"
        assert r.source == "reviewer"
        assert r.status == "pending"


# ---------------------------------------------------------------------------
# Step 108b — Review CLI Commands
# ---------------------------------------------------------------------------

class TestReviewCLI:
    def test_review_group_in_catalog(self):
        from apps.cli.command_catalog import CATALOG, GROUPS
        assert "review" in GROUPS
        cmd_ids = [c.command_id for c in CATALOG]
        assert "review.run" in cmd_ids
        assert "review.list" in cmd_ids
        assert "review.accept" in cmd_ids
        assert "review.reject" in cmd_ids

    def test_review_handlers_registered(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "review.run" in handlers
        assert "review.list" in handlers
        assert "review.accept" in handlers
        assert "review.reject" in handlers

    def test_after_task_arg_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        run_cmd = next(c for c in CATALOG if c.command_id == "review.run")
        arg_names = [a.name for a in run_cmd.args]
        assert "--after-task" in arg_names


# ---------------------------------------------------------------------------
# Step 109 — Source Context Finalization
# ---------------------------------------------------------------------------

class TestSourceContextFinalization:
    def test_text_binary_detection_exists(self):
        src = (Path(__file__).parent.parent / "packages" / "orchestration" / "source_context.py").read_text()
        assert "_is_text_file" in src

    def test_inject_source_context_budget(self):
        from packages.orchestration.source_context import inject_source_context
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "main.py").write_text("x = 1\n")
            ctx = inject_source_context(_make_job(), p, budget=100)
            assert ctx.estimated_tokens <= 200  # reasonable budget


# ---------------------------------------------------------------------------
# Step 110 — Structured Patch/Apply/Test Loop
# ---------------------------------------------------------------------------

class TestPatchApplyTestLoop:
    def test_autorun_has_test_phase(self):
        src = (Path(__file__).parent.parent / "packages" / "orchestration" / "autorun.py").read_text()
        assert "test" in src.lower()
        assert "run_tests" in src or "test_execution" in src

    def test_apply_structured_patch_import(self):
        from packages.orchestration.source_apply import apply_structured_patch
        assert callable(apply_structured_patch)

    def test_revert_apply_import(self):
        from packages.orchestration.source_apply import revert_apply
        assert callable(revert_apply)
