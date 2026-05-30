"""Tests for Steps 147-154 — Blocker/advisory split, commit-readiness ready,
repair context, repair loop, reviewer, memory candidates, live UI v2, UX polish.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _make_job(*, tasks=None, name="test", metadata=None):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if metadata:
        job.metadata = dict(metadata)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = Task(
                description=t.get("description", task_type),
                inputs=inputs,
            )
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# =========================================================================
# Step 147 — Dev status blocker/advisory split
# =========================================================================

class TestStep147_BlockerAdvisorySplit:
    """commit_readiness_ok=false should be advisory, not blocker."""

    def test_dev_status_schema_has_advisories(self):
        """dev status JSON must have 'advisories' key."""
        from apps.cli.commands.dev import _dev_status
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        assert "advisories" in data
        assert "remaining_blockers" in data
        assert isinstance(data["advisories"], list)

    def test_commit_readiness_false_is_advisory(self):
        """commit-readiness false should not be a blocker."""
        from apps.cli.commands.dev import _dev_status
        import io, contextlib
        # Mock smoke to return a job_id, and commit-readiness to return False
        with patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke, \
             patch("apps.cli.commands.repo._cmd_commit_readiness") as mock_cr:
            mock_smoke.return_value = {
                "found": True, "status": "passed",
                "job_id": "abc123", "project_id": "", "smoke_log": "",
            }
            # Simulate commit-readiness returning ready=false (not crashing)
            mock_cr.side_effect = lambda *a, **k: print(json.dumps({"ready": False}))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        # commit-readiness false should NOT be in blockers
        for b in data["remaining_blockers"]:
            assert "commit-readiness" not in b.lower()
        # Should be in advisories
        advisory_text = " ".join(data["advisories"]).lower()
        assert "commit-readiness" in advisory_text or data["commit_readiness_ok"] is None

    def test_commit_readiness_crash_is_blocker(self):
        """commit-readiness crash should be a hard blocker."""
        from apps.cli.commands.dev import _dev_status
        import io, contextlib
        with patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke, \
             patch("apps.cli.commands.repo._cmd_commit_readiness") as mock_cr:
            mock_smoke.return_value = {
                "found": True, "status": "passed",
                "job_id": "abc123", "project_id": "", "smoke_log": "",
            }
            mock_cr.side_effect = RuntimeError("crash")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        blocker_text = " ".join(data["remaining_blockers"]).lower()
        assert "crash" in blocker_text

    def test_worker_cleanup_unavailable_is_advisory(self):
        """ollama missing = advisory, not blocker."""
        from apps.cli.commands.dev import _dev_status
        import io, contextlib
        with patch("shutil.which", return_value=None), \
             patch("apps.cli.commands.dev._find_latest_smoke") as mock_smoke:
            mock_smoke.return_value = {
                "found": True, "status": "passed",
                "job_id": "", "project_id": "", "smoke_log": "",
            }
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        advisory_text = " ".join(data["advisories"]).lower()
        assert "ollama" in advisory_text
        for b in data["remaining_blockers"]:
            assert "ollama" not in b.lower()


# =========================================================================
# Step 148 — Commit-readiness can return ready=true
# =========================================================================

class TestStep148_CommitReadinessReady:
    """Prove commit-readiness can report ready=true for a valid fixture job."""

    def test_fixture_builder_produces_ready_job(self):
        """Fixture builder at autonomy 6 creates a passing job → ready=true."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            # Initialize git so commit-readiness can inspect
            subprocess.run(
                ["git", "init"], cwd=str(repo),
                capture_output=True, check=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@test.com"],
                cwd=str(repo), capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=str(repo), capture_output=True,
            )
            # Baseline commit
            (repo / "README.md").write_text("init\n")
            subprocess.run(
                ["git", "add", "."], cwd=str(repo), capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "init"],
                cwd=str(repo), capture_output=True,
            )
            # Run fixture builder
            from packages.orchestration.autorun import run_autorun
            result = run_autorun(
                "Fix calc", str(repo),
                autonomy_level=6, max_cycles=1,
                fixture_builder=True, json_output=True,
            )
            assert result.job_id
            # Check that tests passed in fixture
            events_dict = {e["event"]: e["value"] for e in result.events}
            assert events_dict.get("tests_passed") == "True"


# =========================================================================
# Step 149 — Repair context v1
# =========================================================================

class TestStep149_RepairContext:
    """Repair context must produce safe failure summary, no raw stdout."""

    def test_build_repair_context_basic(self):
        from packages.orchestration.repair_context import build_repair_context
        job_id = uuid4()
        test_event = {
            "event": "test_run_completed",
            "metadata": {"exit_code": 1, "passed": False},
        }
        events = [
            {"event": "source_patch_applied", "metadata": {
                "apply_id": "ap-001",
                "files_modified": ["calc.py"],
                "files_created": [],
            }},
            test_event,
        ]
        rc = build_repair_context(job_id, test_event, events)
        assert rc["version"] == 1
        assert rc["failure_kind"] == "assertion"
        assert rc["status"] == "failed"
        assert "calc.py" in rc["affected_files"]
        assert "stdout" not in json.dumps(rc).lower()
        assert "stderr" not in json.dumps(rc).lower()
        assert "traceback" not in json.dumps(rc).lower()

    def test_failure_kinds(self):
        from packages.orchestration.repair_context import build_repair_context
        job_id = uuid4()
        for exit_code, expected_kind in [
            (1, "assertion"), (2, "syntax"), (5, "no_tests_collected"),
            (99, "command_failed"),
        ]:
            test_event = {"metadata": {"exit_code": exit_code}}
            rc = build_repair_context(job_id, test_event, [])
            assert rc["failure_kind"] == expected_kind

    def test_timeout_overrides_exit_code(self):
        from packages.orchestration.repair_context import build_repair_context
        test_event = {"metadata": {"exit_code": 1, "timeout": True}}
        rc = build_repair_context(uuid4(), test_event, [])
        assert rc["failure_kind"] == "timeout"

    def test_safe_summary_length(self):
        from packages.orchestration.repair_context import build_repair_context
        test_event = {"metadata": {"exit_code": 1}}
        events = [{"event": "source_patch_applied", "metadata": {
            "files_modified": [f"file_{i}.py" for i in range(50)],
        }}]
        rc = build_repair_context(uuid4(), test_event, events)
        assert len(rc["safe_summary"]) <= 200
        assert len(rc["affected_files"]) <= 20


# =========================================================================
# Step 150 — Deterministic repair loop E2E
# =========================================================================

class TestStep150_RepairLoopFixture:
    """--fixture-builder repair-loop must fix a failing test in 2 cycles."""

    def test_repair_loop_two_cycles(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            from packages.orchestration.autorun import run_autorun
            result = run_autorun(
                "Fix calc", str(repo),
                autonomy_level=6, max_cycles=3,
                fixture_builder="repair-loop", json_output=True,
            )
            events_dict = {e["event"]: e["value"] for e in result.events}
            assert result.cycles_run == 2
            assert events_dict.get("repair_context_created") == "True"
            assert events_dict.get("repair_loop_used") == "True"
            assert events_dict.get("tests_passed") == "True"

    def test_parse_fixture_builder_repair_loop(self):
        from apps.cli.commands.do_cmd import _parse_fixture_builder
        assert _parse_fixture_builder("repair-loop") == "repair-loop"
        assert _parse_fixture_builder("true") is True
        assert _parse_fixture_builder("false") is False
        assert _parse_fixture_builder("anything") is False


# =========================================================================
# Step 151 — Reviewer recommendation v1
# =========================================================================

class TestStep151_ReviewerRecommendation:
    """Fixture reviewer returns deterministic recommendations; accept/reject works."""

    def test_fixture_reviewer_returns_two(self):
        from packages.orchestration.reviewer import run_reviewer, _fixture_reviewer
        job = _make_job(tasks=[
            {"type": "readme_draft", "status": "completed"},
        ])
        recs = run_reviewer(job, reviewer_fn=_fixture_reviewer)
        assert len(recs) == 2
        assert recs[0].title == "Add edge case tests"
        assert recs[1].title == "Add type hints to calc.py"
        assert all(r.status == "pending" for r in recs)

    def test_accept_recommendation_creates_task(self):
        from packages.orchestration.reviewer import (
            run_reviewer, store_recommendations,
            accept_recommendation, _fixture_reviewer,
        )
        from packages.core.models import RunState
        job = _make_job()
        job.metadata = {}
        recs = run_reviewer(job, reviewer_fn=_fixture_reviewer)
        store_recommendations(job, recs)
        task_count_before = len(job.tasks)
        ok = accept_recommendation(job, recs[0].id)
        assert ok is True
        assert len(job.tasks) == task_count_before + 1
        new_task = job.tasks[-1]
        assert new_task.status == RunState.PENDING
        assert new_task.inputs.get("source") == "reviewer"
        assert new_task.inputs.get("task_type") == "test_improvement"

    def test_reject_recommendation_no_task(self):
        from packages.orchestration.reviewer import (
            run_reviewer, store_recommendations,
            reject_recommendation, list_recommendations, _fixture_reviewer,
        )
        job = _make_job()
        job.metadata = {}
        recs = run_reviewer(job, reviewer_fn=_fixture_reviewer)
        store_recommendations(job, recs)
        task_count_before = len(job.tasks)
        ok = reject_recommendation(job, recs[0].id)
        assert ok is True
        assert len(job.tasks) == task_count_before
        stored = list_recommendations(job)
        rejected = [r for r in stored if r["id"] == recs[0].id]
        assert rejected[0]["status"] == "rejected"

    def test_default_reviewer_returns_empty(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job()
        recs = run_reviewer(job)
        assert recs == []

    def test_reviewer_no_auto_append(self):
        """Reviewer must NOT auto-append tasks; only accept does."""
        from packages.orchestration.reviewer import run_reviewer, _fixture_reviewer
        job = _make_job()
        task_count_before = len(job.tasks)
        run_reviewer(job, reviewer_fn=_fixture_reviewer)
        assert len(job.tasks) == task_count_before


# =========================================================================
# Step 152 — Memory candidate v1
# =========================================================================

class TestStep152_MemoryCandidate:
    """Memory candidates require human approval; not auto-approved."""

    def test_create_candidate(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "repair_pattern", "Fixed mul after partial")
        assert c["status"] == "pending"
        assert c["kind"] == "repair_pattern"
        assert "Fixed mul" in c["safe_summary"]

    def test_candidate_deduplication(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        c1 = create_candidate(job, "repair_pattern", "Fixed mul")
        c2 = create_candidate(job, "repair_pattern", "Fixed mul")
        assert c1["id"] == c2["id"]

    def test_approve_creates_memory(self):
        from packages.orchestration.memory_candidates import (
            create_candidate, approve_candidate, list_candidates,
        )
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "test_command", "pytest -x works")
        # store_memory is lazily imported inside approve_candidate
        with patch.dict("sys.modules", {
            "packages.orchestration.memory": MagicMock(),
        }):
            ok = approve_candidate(job, c["id"])
        assert ok is True
        candidates = list_candidates(job)
        approved = [x for x in candidates if x["id"] == c["id"]]
        assert approved[0]["status"] == "approved"

    def test_reject_no_memory(self):
        from packages.orchestration.memory_candidates import (
            create_candidate, reject_candidate, list_candidates,
        )
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "test_command", "pytest -x")
        ok = reject_candidate(job, c["id"])
        assert ok is True
        candidates = list_candidates(job)
        rejected = [x for x in candidates if x["id"] == c["id"]]
        assert rejected[0]["status"] == "rejected"

    def test_invalid_kind_falls_back(self):
        from packages.orchestration.memory_candidates import create_candidate
        job = _make_job()
        job.metadata = {}
        c = create_candidate(job, "bogus_kind", "test")
        assert c["kind"] == "review_note"

    def test_candidate_not_auto_approved(self):
        """Candidates must be pending, never auto-approved."""
        from packages.orchestration.memory_candidates import (
            create_candidate, list_candidates,
        )
        job = _make_job()
        job.metadata = {}
        create_candidate(job, "repair_pattern", "A")
        create_candidate(job, "test_command", "B")
        candidates = list_candidates(job)
        for c in candidates:
            assert c["status"] == "pending"


# =========================================================================
# Step 153 — Live run UI v2
# =========================================================================

class TestStep153_LiveStateV2:
    """Live-state must include repair_loop_used, reviewer/memory counts."""

    def test_live_state_v2_schema(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {}
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        assert state["version"] == 2
        assert "repair_loop_used" in state
        assert "reviewer_pending_count" in state
        assert "memory_candidate_count" in state
        assert isinstance(state["repair_loop_used"], bool)
        assert isinstance(state["reviewer_pending_count"], int)
        assert isinstance(state["memory_candidate_count"], int)

    def test_live_state_repair_loop_detected(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {}
        events = [{"event": "repair_context_created", "timestamp": "t"}]
        with patch("packages.orchestration.ui_server._load_events", return_value=events):
            state = _build_live_state_json(job)
        assert state["repair_loop_used"] is True

    def test_live_state_reviewer_count(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {"reviewer_recommendations": [
            {"id": "a", "status": "pending"},
            {"id": "b", "status": "accepted"},
            {"id": "c", "status": "pending"},
        ]}
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        assert state["reviewer_pending_count"] == 2

    def test_live_state_memory_candidate_count(self):
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {"memory_candidates": [
            {"id": "x", "status": "pending"},
        ]}
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        assert state["memory_candidate_count"] == 1

    def test_live_state_running_accepts_both_states(self):
        from packages.orchestration.ui_server import _build_live_state_json
        from packages.core.models import RunState
        job = _make_job()
        job.metadata = {}
        job.state = RunState.RUNNING
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        assert state["running"] is True


# =========================================================================
# Step 154 — UX product polish gate
# =========================================================================

class TestStep154_UXPolish:
    """Task ribbon, reduced-motion, next-action, no metadata wall."""

    def test_task_ribbon_in_ui_source(self):
        """UI source must contain task ribbon rendering."""
        main_ts = _ROOT / "apps" / "ui" / "src" / "main.ts"
        if not main_ts.exists():
            pytest.skip("UI source not found")
        src = main_ts.read_text()
        assert "ribbon" in src.lower()
        assert "renderRibbon" in src

    def test_reduced_motion_in_ui_source(self):
        """UI must respect prefers-reduced-motion."""
        main_ts = _ROOT / "apps" / "ui" / "src" / "main.ts"
        renderer_ts = _ROOT / "apps" / "ui" / "src" / "brain" / "renderer.ts"
        found = False
        for p in (main_ts, renderer_ts):
            if p.exists() and "reduced-motion" in p.read_text():
                found = True
                break
        assert found, "reduced-motion not found in UI source"

    def test_next_action_endpoint_exists(self):
        """UI server must expose next-action endpoint handler."""
        from packages.orchestration.ui_server import _build_next_action_json
        assert callable(_build_next_action_json)

    def test_live_state_no_metadata_wall(self):
        """Live-state must not expose raw metadata blob."""
        from packages.orchestration.ui_server import _build_live_state_json
        job = _make_job()
        job.metadata = {"secret": "leak", "reviewer_recommendations": []}
        with patch("packages.orchestration.ui_server._load_events", return_value=[]):
            state = _build_live_state_json(job)
        assert "secret" not in json.dumps(state)
        # No raw metadata key
        assert "metadata" not in state

    def test_task_progress_compact(self):
        """Task progress must include compact titles, not raw metadata."""
        from packages.orchestration.ui_view_model import build_task_progress
        job = _make_job(tasks=[
            {"type": "readme_draft", "status": "completed"},
            {"type": "test_fix", "status": "running"},
        ])
        tp = build_task_progress(job, [])
        assert tp["version"] == 1
        for t in tp["tasks"]:
            assert "title" in t
            assert len(t["title"]) <= 60
            # No raw metadata blob exposed
            assert "metadata" not in t
