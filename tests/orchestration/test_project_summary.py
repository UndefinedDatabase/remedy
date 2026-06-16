"""Tests: project-level brain summary, patterns, model quality rollup, memory suggestions.

All outputs verified for safe metadata only — no raw content.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from packages.orchestration.project_summary import (
    ProjectBrainSummary,
    ProjectPattern,
    build_project_model_summary,
    build_project_summary,
    detect_patterns,
    export_memory_suggestions_json,
    export_patterns_json,
    export_project_summary_json,
    suggest_memory_updates,
)

# -- Minimal stubs for testing without real storage --

@dataclass
class _FakeJob:
    id: Any = None
    state: Any = "planned"
    tasks: list = field(default_factory=list)
    artifacts: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()


@dataclass
class _FakeProject:
    id: Any = None
    name: str = "Test Project"
    job_ids: list = field(default_factory=list)
    repo_paths: list = field(default_factory=list)

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()


@dataclass
class _FakeScorecard:
    total_cases: int = 0
    usable_patch_rate: float = 0.0
    safe_rejection_rate: float = 0.0
    outcome_accuracy: float = 0.0
    average_tokens: float = 0.0
    average_latency_ms: float = 0.0
    needs_real_model_check: bool = True
    provider: str = "fixture"
    model: str = "mock"
    prompt_profile: str = "default"


class TestProjectSummary:
    """Step 400: Project brain summary."""

    def test_empty_project(self):
        project = _FakeProject()
        summary = build_project_summary(project, [], {})
        assert summary.job_count == 0
        assert summary.active_job_count == 0
        assert summary.redaction == "safe_metadata_only"

    def test_one_job_project(self):
        job = _FakeJob()
        project = _FakeProject(job_ids=[str(job.id)])
        events = {str(job.id): [
            {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z", "metadata": {}},
        ]}
        summary = build_project_summary(project, [job], events)
        assert summary.job_count == 1
        assert summary.latest_event_at == "2026-06-01T00:00:00Z"

    def test_multi_job_project(self):
        j1 = _FakeJob(state="completed")
        j2 = _FakeJob(state="blocked")
        j3 = _FakeJob(state="planned")
        project = _FakeProject(job_ids=[str(j.id) for j in [j1, j2, j3]])
        summary = build_project_summary(project, [j1, j2, j3], {})
        assert summary.completed_job_count == 1
        assert summary.blocked_job_count == 1
        assert summary.active_job_count == 1

    def test_blocked_job_appears_in_blockers(self):
        job = _FakeJob(state="blocked")
        events = {str(job.id): [
            {"event": "stop_reason_recorded", "timestamp": "2026-06-01T00:00:00Z",
             "outcome": "open", "metadata": {"stop_reason": "approval_required"}},
        ]}
        project = _FakeProject(job_ids=[str(job.id)])
        summary = build_project_summary(project, [job], events)
        assert len(summary.blockers) >= 1
        assert "approval_required" in summary.blockers[0]

    def test_no_raw_leaks(self):
        job = _FakeJob(metadata={"secret_key": "sk-12345"})
        events = {str(job.id): [
            {"event": "task_created", "timestamp": "2026-06-01T00:00:00Z",
             "metadata": {"raw_output": "SECRET DATA"}},
        ]}
        project = _FakeProject(job_ids=[str(job.id)])
        summary = build_project_summary(project, [job], events)
        data = export_project_summary_json(summary)
        full = json.dumps(data)
        assert "sk-12345" not in full
        assert "SECRET DATA" not in full
        assert data["redaction"] == "safe_metadata_only"

    def test_export_shape(self):
        project = _FakeProject()
        summary = build_project_summary(project, [], {})
        data = export_project_summary_json(summary)
        assert "version" in data
        assert "project_id" in data
        assert "redaction" in data
        assert "suggested_next_step" in data


class TestPatternDetection:
    """Step 401: Repeated pattern detection."""

    def test_no_patterns_empty(self):
        patterns = detect_patterns([], {})
        assert patterns == []

    def test_repeated_stop_reason(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-01T00:00:00Z",
                 "metadata": {"stop_reason": "approval_required"}},
            ],
            str(j2.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-02T00:00:00Z",
                 "metadata": {"stop_reason": "approval_required"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        stop_patterns = [p for p in patterns if p.kind == "repeated_stop_reason"]
        assert len(stop_patterns) >= 1
        assert stop_patterns[0].count >= 2

    def test_repeated_file_touch(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "patch_intent_applied", "timestamp": "2026-06-01",
                 "metadata": {"target_path": "app.py"}},
            ],
            str(j2.id): [
                {"event": "patch_intent_applied", "timestamp": "2026-06-02",
                 "metadata": {"target_path": "app.py"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        file_patterns = [p for p in patterns if p.kind == "frequently_touched_file"]
        assert len(file_patterns) >= 1
        assert "app.py" in file_patterns[0].related_file_paths

    def test_repeated_parse_failure(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "builder_patch_parsed", "timestamp": "2026-06-01",
                 "metadata": {"parse_success": False, "error_kind": "prose_only"}},
            ],
            str(j2.id): [
                {"event": "builder_patch_parsed", "timestamp": "2026-06-02",
                 "metadata": {"parse_success": False, "error_kind": "prose_only"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        parse_patterns = [p for p in patterns if p.kind == "repeated_parse_failure"]
        assert len(parse_patterns) >= 1

    def test_single_occurrence_low_severity(self):
        job = _FakeJob()
        events = {str(job.id): [
            {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
             "metadata": {"stop_reason": "test_failed_after_apply"}},
        ]}
        patterns = detect_patterns([job], events)
        assert all(p.count < 2 or p.severity in ("low", "medium") for p in patterns)

    def test_no_raw_leaks_in_patterns(self):
        j1 = _FakeJob()
        events = {str(j1.id): [
            {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
             "metadata": {"stop_reason": "test_failed", "raw_output": "LEAKED"}},
            {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
             "metadata": {"stop_reason": "test_failed", "raw_output": "LEAKED2"}},
        ]}
        patterns = detect_patterns([j1], events)
        full = json.dumps(export_patterns_json(patterns))
        assert "LEAKED" not in full


class TestModelQualityRollup:
    """Step 402: Model quality at project level."""

    def test_empty_scorecards(self):
        ms = build_project_model_summary([])
        assert ms.confidence == "low"
        assert "no" in ms.recommendation.lower()

    def test_fixture_only_low_confidence(self):
        sc = _FakeScorecard(total_cases=7, outcome_accuracy=0.8, needs_real_model_check=True)
        ms = build_project_model_summary([sc])
        assert ms.confidence == "low"
        assert ms.needs_real_model_check is True

    def test_real_data_medium_confidence(self):
        sc = _FakeScorecard(total_cases=7, outcome_accuracy=0.8, needs_real_model_check=False)
        ms = build_project_model_summary([sc])
        assert ms.confidence == "medium"

    def test_real_data_high_confidence(self):
        sc = _FakeScorecard(total_cases=20, outcome_accuracy=0.9, needs_real_model_check=False)
        ms = build_project_model_summary([sc])
        assert ms.confidence == "high"

    def test_multiple_scorecards_aggregate(self):
        sc1 = _FakeScorecard(total_cases=5, outcome_accuracy=0.6)
        sc2 = _FakeScorecard(total_cases=5, outcome_accuracy=0.8)
        ms = build_project_model_summary([sc1, sc2])
        assert ms.sample_count == 10

    def test_no_raw_leaks(self):
        sc = _FakeScorecard(total_cases=5, outcome_accuracy=0.7)
        ms = build_project_model_summary([sc])
        assert ms.redaction == "safe_metadata_only"


class TestMemorySuggestions:
    """Step 403: Safe memory update suggestions."""

    def test_no_suggestions_when_no_patterns(self):
        summary = ProjectBrainSummary()
        suggestions = suggest_memory_updates(summary, [])
        assert suggestions == []

    def test_frequent_file_suggestion(self):
        summary = ProjectBrainSummary()
        pattern = ProjectPattern(
            kind="frequently_touched_file", count=4,
            related_file_paths=["app.py"], related_job_ids=["j1"],
        )
        suggestions = suggest_memory_updates(summary, [pattern])
        assert len(suggestions) >= 1
        assert "app.py" in suggestions[0].title

    def test_recurring_blocker_suggestion(self):
        summary = ProjectBrainSummary()
        pattern = ProjectPattern(
            kind="repeated_stop_reason", count=3,
            summary="'approval_required' stopped 3 times",
            suggested_attention="Investigate approval",
            related_job_ids=["j1", "j2"],
        )
        suggestions = suggest_memory_updates(summary, [pattern])
        assert len(suggestions) >= 1

    def test_blocked_jobs_suggestion(self):
        summary = ProjectBrainSummary(blocked_job_count=3)
        suggestions = suggest_memory_updates(summary, [])
        assert len(suggestions) >= 1
        assert "blocked" in suggestions[0].title.lower()

    def test_all_suggestions_require_approval(self):
        summary = ProjectBrainSummary(blocked_job_count=3)
        pattern = ProjectPattern(
            kind="frequently_touched_file", count=5,
            related_file_paths=["x.py"], related_job_ids=["j1"],
        )
        suggestions = suggest_memory_updates(summary, [pattern])
        for s in suggestions:
            assert s.requires_approval is True

    def test_suggestions_bounded(self):
        patterns = [
            ProjectPattern(
                kind="frequently_touched_file", count=3,
                related_file_paths=[f"file{i}.py"], related_job_ids=["j1"],
            )
            for i in range(20)
        ]
        summary = ProjectBrainSummary()
        suggestions = suggest_memory_updates(summary, patterns)
        assert len(suggestions) <= 10

    def test_export_shape(self):
        summary = ProjectBrainSummary(blocked_job_count=2)
        suggestions = suggest_memory_updates(summary, [])
        data = export_memory_suggestions_json(suggestions)
        for s in data:
            assert "requires_approval" in s
            assert s["requires_approval"] is True


# -- Step 411: Stronger pattern detection --

class TestStrongerPatterns:
    """Extended pattern types: test failure, permission, provider, repair."""

    def test_repeated_test_failure(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "test_run_completed", "timestamp": "2026-06-01",
                 "metadata": {"status": "failed"}},
            ],
            str(j2.id): [
                {"event": "test_run_completed", "timestamp": "2026-06-02",
                 "metadata": {"status": "failed"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        test_patterns = [p for p in patterns if p.kind == "repeated_test_failure"]
        assert len(test_patterns) >= 1
        assert test_patterns[0].count >= 2

    def test_repeated_permission_block(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                 "metadata": {"stop_reason": "permission_denied"}},
            ],
            str(j2.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                 "metadata": {"stop_reason": "permission_denied"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        perm_patterns = [p for p in patterns if p.kind == "repeated_permission_block"]
        assert len(perm_patterns) >= 1

    def test_repeated_provider_unavailable(self):
        j1 = _FakeJob()
        j2 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-01",
                 "metadata": {"stop_reason": "provider_unavailable"}},
            ],
            str(j2.id): [
                {"event": "stop_reason_recorded", "timestamp": "2026-06-02",
                 "metadata": {"stop_reason": "provider_unavailable"}},
            ],
        }
        patterns = detect_patterns([j1, j2], events)
        prov_patterns = [p for p in patterns if p.kind == "repeated_provider_unavailable"]
        assert len(prov_patterns) >= 1

    def test_repeated_repair_exhaustion(self):
        j1 = _FakeJob()
        events = {
            str(j1.id): [
                {"event": "repair_loop_stopped", "timestamp": "2026-06-01",
                 "metadata": {"reason": "repair_budget_exhausted"}},
                {"event": "repair_loop_stopped", "timestamp": "2026-06-02",
                 "metadata": {"reason": "repair_budget_exhausted"}},
            ],
        }
        patterns = detect_patterns([j1], events)
        repair_patterns = [p for p in patterns if p.kind == "repeated_repair_exhaustion"]
        assert len(repair_patterns) >= 1

    def test_one_off_not_over_severity(self):
        job = _FakeJob()
        events = {str(job.id): [
            {"event": "test_run_completed", "timestamp": "2026-06-01",
             "metadata": {"status": "failed"}},
        ]}
        patterns = detect_patterns([job], events)
        test_patterns = [p for p in patterns if p.kind == "repeated_test_failure"]
        assert len(test_patterns) == 0


# -- Step 413: Docs --

class TestProjectBrainDocs:
    """Project brain docs exist and are accurate."""

    def test_docs_exist(self):
        from pathlib import Path
        docs = Path(__file__).resolve().parents[2] / "docs" / "project-brain.md"
        assert docs.exists()

    def test_docs_mention_commands(self):
        from pathlib import Path
        text = (Path(__file__).resolve().parents[2] / "docs" / "project-brain.md").read_text()
        assert "remedy project summary" in text
        assert "remedy project show" in text

    def test_docs_no_auto_memory_claim(self):
        from pathlib import Path
        text = (Path(__file__).resolve().parents[2] / "docs" / "project-brain.md").read_text()
        assert "approval" in text.lower()
        assert "does not auto-write" in text.lower() or "require" in text.lower()

    def test_docs_commands_catalog_valid(self):
        import re
        from pathlib import Path

        from apps.cli.command_catalog import CATALOG

        text = (Path(__file__).resolve().parents[2] / "docs" / "project-brain.md").read_text()
        cmds = re.findall(r"remedy (\w+) (\w[\w-]*)", text)
        catalog_groups = {e.group_id for e in CATALOG}
        for group, _sub in cmds:
            assert group in catalog_groups, f"Command group '{group}' not in catalog"
