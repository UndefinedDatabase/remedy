"""CLI tests: remedy project summary command.

Tests the project summary CLI surface — command catalog, JSON shape, safety.
Uses mock project/job data, no real storage dependency.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestProjectSummaryCatalog:
    """project.summary must be in command catalog."""

    def test_project_summary_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "project.summary" in ids

    def test_project_summary_is_read_only(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "project.summary")
        assert entry.action_class == "read_only"

    def test_project_summary_supports_json(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "project.summary")
        assert entry.supports_json is True


class TestProjectSummaryOutput:
    """project summary produces safe structured output."""

    def _make_project(self):
        proj = MagicMock()
        proj.id = uuid4()
        proj.name = "Test Project"
        proj.job_ids = []
        proj.repo_paths = []
        return proj

    def _make_job(self, state="planned"):
        job = MagicMock()
        job.id = uuid4()
        job.state.value = state
        job.state.__str__ = lambda s: state
        job.tasks = []
        job.artifacts = []
        job.metadata = {}
        return job

    def test_empty_project_json(self):
        from packages.orchestration.project_summary import (
            build_project_summary,
            export_project_summary_json,
        )
        proj = self._make_project()
        summary = build_project_summary(proj, [], {})
        data = export_project_summary_json(summary)
        assert data["project_id"] == str(proj.id)
        assert data["job_count"] == 0
        assert data["redaction"] == "safe_metadata_only"

    def test_project_with_jobs_json(self):
        from packages.orchestration.project_summary import (
            build_project_summary,
            export_project_summary_json,
        )
        proj = self._make_project()
        j1 = self._make_job("completed")
        j2 = self._make_job("blocked")
        proj.job_ids = [str(j1.id), str(j2.id)]

        events = {
            str(j1.id): [
                {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z", "metadata": {}},
            ],
            str(j2.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-02T00:00:00Z",
                 "outcome": "open", "metadata": {"stop_reason": "approval_required"}},
            ],
        }

        summary = build_project_summary(proj, [j1, j2], events)
        data = export_project_summary_json(summary)
        assert data["job_count"] == 2
        assert data["completed_job_count"] == 1
        assert data["blocked_job_count"] == 1
        assert len(data["blockers"]) >= 1
        assert data["redaction"] == "safe_metadata_only"

    def test_json_has_required_fields(self):
        from packages.orchestration.project_summary import (
            build_project_summary,
            export_project_summary_json,
        )
        proj = self._make_project()
        data = export_project_summary_json(build_project_summary(proj, [], {}))
        required = [
            "project_id", "job_count", "active_job_count", "completed_job_count",
            "blocked_job_count", "current_focus", "blockers", "frequently_touched_files",
            "patterns", "memory_suggestions", "suggested_next_step", "next_command",
            "redaction",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"

    def test_no_raw_leaks(self):
        from packages.orchestration.project_summary import (
            build_project_summary,
            export_project_summary_json,
        )
        proj = self._make_project()
        job = self._make_job()
        job.metadata = {"secret": "sk-secret-key-12345"}
        events = {str(job.id): [
            {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z",
             "metadata": {"raw_output": "SECRET_CONTENT", "command_output": "LEAKED"}},
        ]}
        summary = build_project_summary(proj, [job], events)
        data = export_project_summary_json(summary)
        full = json.dumps(data)
        assert "sk-secret-key" not in full
        assert "SECRET_CONTENT" not in full
        assert "LEAKED" not in full

    def test_patterns_included(self):
        from packages.orchestration.project_summary import (
            build_project_summary,
            detect_patterns,
            export_patterns_json,
            export_project_summary_json,
        )
        proj = self._make_project()
        j1 = self._make_job()
        j2 = self._make_job()
        events = {
            str(j1.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                 "metadata": {"stop_reason": "approval_required"}},
            ],
            str(j2.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                 "metadata": {"stop_reason": "approval_required"}},
            ],
        }
        summary = build_project_summary(proj, [j1, j2], events)
        patterns = detect_patterns([j1, j2], events)
        summary.patterns = export_patterns_json(patterns)
        data = export_project_summary_json(summary)
        assert len(data["patterns"]) >= 1

    def test_memory_suggestions_included(self):
        from packages.orchestration.project_summary import (
            MemorySuggestion,
            export_memory_suggestions_json,
        )
        suggestions = [
            MemorySuggestion(
                title="Frequent file",
                summary="app.py touched 5 times",
                evidence_count=5,
                requires_approval=True,
            ),
        ]
        data = export_memory_suggestions_json(suggestions)
        assert len(data) == 1
        assert data[0]["requires_approval"] is True


class TestProjectSummaryErrorPaths:
    """CLI handles invalid/missing project IDs safely."""

    def test_invalid_project_id_exits(self):
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "apps.cli.grouped", "project", "summary", "not-a-uuid"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        assert "invalid" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_missing_project_exits(self):
        import subprocess
        fake_uuid = "00000000-0000-0000-0000-000000000099"
        result = subprocess.run(
            ["python3", "-m", "apps.cli.grouped", "project", "summary", fake_uuid],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()
