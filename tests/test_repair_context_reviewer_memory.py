"""Tests for Steps 147-154 — Blocker/advisory split, commit-readiness ready,
repair context, repair loop, reviewer, memory candidates, live UI v2, UX polish.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _make_job(*, tasks=None, name="test", metadata=None):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry
    job = JobPlan(job_title=name)
    if metadata:
        job.metadata = dict(metadata)
    if tasks:
        for t in tasks:
            task_type = t.get("type", "readme_draft")
            inputs = dict(t.get("metadata", {}))
            inputs.setdefault("task_type", task_type)
            task = TaskEntry(
                title=t.get("description", task_type),
                inputs=inputs,
            )
            if "status" in t:
                task.status = RunState(t["status"])
            job.tasks.append(task)
    return job


# =========================================================================
# Step 147 — Dev status blocker/advisory split
# =========================================================================

class TestDevStatusBlockerAdvisorySplit:
    """Dev status keeps hard blockers apart from advisories."""

    def test_dev_status_schema_has_advisories(self):
        """dev status JSON must have 'advisories' key."""
        import contextlib
        import io

        from apps.cli.commands.dev import _dev_status
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _dev_status(json_output=True)
        data = json.loads(buf.getvalue())
        assert "advisories" in data
        assert "remaining_blockers" in data
        assert isinstance(data["advisories"], list)

    def test_worker_cleanup_unavailable_is_advisory(self):
        """ollama missing = advisory, not blocker."""
        import contextlib
        import io

        from apps.cli.commands.dev import _dev_status
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


# =========================================================================
# Step 149 — Repair context v1
# =========================================================================

class TestRepairContextSafeSummary:
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


# =========================================================================
# Step 151 — Reviewer recommendation v1
# =========================================================================

def _two_recommendations(context: dict) -> list[dict]:
    """A deterministic reviewer; the module's own fixture had test callers only (R-0908)."""
    return [{"title": "Add edge case tests", "task_type": "test_improvement", "risk": "low"},
            {"title": "Add type hints to calc.py", "task_type": "code_quality", "risk": "low"}]


class TestReviewerRecommendations:
    """A supplied reviewer's recommendations come back pending; nothing is appended to the job."""

    def test_supplied_reviewer_returns_two(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job(tasks=[
            {"type": "readme_draft", "status": "completed"},
        ])
        recs = run_reviewer(job, reviewer_fn=_two_recommendations)
        assert len(recs) == 2
        assert recs[0].title == "Add edge case tests"
        assert recs[1].title == "Add type hints to calc.py"
        assert all(r.status == "pending" for r in recs)

    def test_default_reviewer_returns_empty(self):
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job()
        recs = run_reviewer(job)
        assert recs == []

    def test_reviewer_no_auto_append(self):
        """Reviewer must NOT auto-append tasks; only accept does."""
        from packages.orchestration.reviewer import run_reviewer
        job = _make_job()
        task_count_before = len(job.tasks)
        run_reviewer(job, reviewer_fn=_two_recommendations)
        assert len(job.tasks) == task_count_before
