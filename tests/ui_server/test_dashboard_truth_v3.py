"""Tests for dashboard truth contract fixes (Step 293)."""
from __future__ import annotations

from packages.core.models import Job
from packages.orchestration.ui_server import (
    _build_dashboard,
    _task_test_status,
    _event_backed_actor,
)


class TestNextActionCommand:
    def test_next_action_has_command_field(self):
        job = Job(name="test")
        dash = _build_dashboard(job)
        assert "command" in dash["next_action"]

    def test_next_action_command_is_runnable(self):
        job = Job(name="test")
        dash = _build_dashboard(job)
        cmd = dash["next_action"]["command"]
        assert cmd and isinstance(cmd, str)
        assert cmd.startswith("remedy ")


class TestTaskTestStatusScoped:
    def test_none_when_no_events(self):
        assert _task_test_status("t1", []) == "none"

    def test_pass_when_task_test_passes(self):
        events = [
            {"event": "test_run_completed", "metadata": {"task_id": "t1", "exit_code": 0}},
        ]
        assert _task_test_status("t1", events) == "pass"

    def test_fail_when_task_test_fails(self):
        events = [
            {"event": "test_run_completed", "metadata": {"task_id": "t1", "exit_code": 1}},
        ]
        assert _task_test_status("t1", events) == "fail"

    def test_scoped_to_task_id(self):
        events = [
            {"event": "test_run_completed", "metadata": {"task_id": "t2", "exit_code": 0}},
        ]
        assert _task_test_status("t1", events) == "none"
        assert _task_test_status("t2", events) == "pass"

    def test_uses_latest_event(self):
        events = [
            {"event": "test_run_completed", "metadata": {"task_id": "t1", "exit_code": 0}},
            {"event": "test_run_completed", "metadata": {"task_id": "t1", "exit_code": 1}},
        ]
        assert _task_test_status("t1", events) == "fail"


class TestGraphSummaryFromRealData:
    def test_graph_summary_present(self):
        job = Job(name="test")
        dash = _build_dashboard(job)
        gs = dash["graph_summary"]
        assert "node_count" in gs
        assert "edge_count" in gs
        assert gs["source"] == "project_brain"

    def test_graph_summary_honest_for_empty_job(self):
        job = Job(name="empty")
        dash = _build_dashboard(job)
        gs = dash["graph_summary"]
        assert isinstance(gs["node_count"], int)
        assert gs["full_graph_requires_explicit_toggle"] is True


class TestEventBackedActor:
    def test_empty_events(self):
        assert _event_backed_actor([]) == ""

    def test_builder_after_patch_applied(self):
        events = [{"event": "patch_intent_applied"}]
        assert _event_backed_actor(events) == "Builder"

    def test_user_after_approval(self):
        events = [{"event": "patch_intent_approved"}]
        assert _event_backed_actor(events) == "User"

    def test_system_for_unknown(self):
        events = [{"event": "some_unknown_event"}]
        assert _event_backed_actor(events) == "System"

    def test_uses_last_event(self):
        events = [
            {"event": "patch_intent_applied"},
            {"event": "human_decision_requested"},
        ]
        assert _event_backed_actor(events) == "User"
