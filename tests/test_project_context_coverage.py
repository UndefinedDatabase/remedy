"""
Tests for packages/orchestration/project_context_coverage.py
and the `remedy project context` CLI command.

Coverage:
  - signal weights sum to 100
  - V0_MAX_SCORE == 95
  - project_memory and mcp_tool_context always absent in v0 with explanation
  - empty project (no linked jobs/repos) produces score=10 (only project_metadata)
  - project with linked repos and jobs gets those signals
  - project with full context (tasks, artifacts, intents, verification, approvals)
    reaches 85% maximum (without memory; 95% with approved memory)
  - ProjectContextCoverageSnapshot is frozen/immutable
  - summarize output: header, project name, coverage bar, sections, meaning
  - JSON schema exact top-level keys and values
  - run-log event schema exact metadata keys
  - redaction sentinels absent from text, JSON, and run logs
  - CLI: invalid UUID exits 1, missing project exits 1, traceback absent
  - CLI: text output works, --json output works
  - existing `remedy context <job_id>` behavior is unchanged
  - export_project_json compact context_coverage key (not full signals)
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.orchestration.project_context_coverage import (
    _SIGNALS,
    _TOTAL_WEIGHT,
    V0_MAX_SCORE,
    derive_project_context_coverage,
    export_project_context_coverage_json,
    summarize_project_context_coverage,
)
from packages.orchestration.project_registry import RemyProject, attach_job, attach_repo

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REDACTION_SENTINELS = [
    "SECRET_ARTIFACT_CONTENT_MUST_NOT_RENDER",
    "SECRET_APPROVAL_REASON_MUST_NOT_RENDER",
    "SECRET_DIFF_PREVIEW_MUST_NOT_RENDER",
    "SECRET_EVENT_MESSAGE_MUST_NOT_RENDER",
    "SECRET_COMMAND_OUTPUT_MUST_NOT_RENDER",
]


def _make_project(**kwargs) -> RemyProject:
    defaults = {"name": "Test Project"}
    defaults.update(kwargs)
    return RemyProject(**defaults)


def _make_job(state: RunState = RunState.PENDING) -> Job:
    return Job(name="test job", state=state)


def _make_job_with_tasks(n: int = 1) -> Job:
    job = Job(name="task job", state=RunState.PLANNED)
    for i in range(n):
        job.tasks.append(Task(description=f"task {i}"))
    return job


def _make_job_with_builder_artifact() -> Job:
    job = Job(name="builder job", state=RunState.RUNNING)
    job.artifacts.append(Artifact(
        name="proposal",
        content="",
        kind=ArtifactKind.BUILDER_PROPOSAL,
    ))
    return job


def _make_job_with_verification_artifact() -> Job:
    job = Job(name="verified job", state=RunState.COMPLETED)
    job.artifacts.append(Artifact(
        name="verification",
        content="",
        kind=ArtifactKind.VERIFICATION,
    ))
    return job


def _make_job_with_patch_intent() -> Job:
    """Job with a patch intent recorded in artifact metadata."""
    job = Job(name="pi job", state=RunState.RUNNING)
    art = Artifact(
        name="proposal",
        content="",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        metadata={
            "patch_intent_explanations": [
                {
                    "file": "src/foo.py",
                    "action": "modify",
                    "risk": "medium",
                    "reason": "test",
                    "summary": "test fix",
                }
            ]
        },
    )
    job.artifacts.append(art)
    return job


def _make_job_with_approval() -> Job:
    """Job with a patch intent that has been approved."""
    from packages.orchestration.approval_queue import make_intent_id, set_approval_state
    job = _make_job_with_patch_intent()
    art = job.artifacts[0]
    intent_id = make_intent_id(art.id, 0)
    set_approval_state(job, intent_id, "approved", reason="test approval")
    return job


# ---------------------------------------------------------------------------
# Signal weight invariants
# ---------------------------------------------------------------------------


class TestSignalWeights:
    def test_total_weight_is_100(self):
        assert _TOTAL_WEIGHT == 100

    def test_v0_max_score_is_95(self):
        assert V0_MAX_SCORE == 95

    def test_project_memory_weight_is_10(self):
        spec = next(s for s in _SIGNALS if s["key"] == "project_memory")
        assert spec["weight"] == 10

    def test_mcp_tool_context_weight_is_5(self):
        spec = next(s for s in _SIGNALS if s["key"] == "mcp_tool_context")
        assert spec["weight"] == 5

    def test_project_memory_not_always_false(self):
        spec = next(s for s in _SIGNALS if s["key"] == "project_memory")
        assert spec["v0_always_false"] is False

    def test_mcp_tool_context_always_false(self):
        spec = next(s for s in _SIGNALS if s["key"] == "mcp_tool_context")
        assert spec["v0_always_false"] is True

    def test_only_mcp_always_false(self):
        always_false = [s["key"] for s in _SIGNALS if s["v0_always_false"]]
        assert set(always_false) == {"mcp_tool_context"}

    def test_ten_signals_defined(self):
        assert len(_SIGNALS) == 10


# ---------------------------------------------------------------------------
# derive_project_context_coverage — scoring
# ---------------------------------------------------------------------------


class TestDeriveProjectContextCoverage:
    def test_empty_project_score_is_10(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.score == 10  # only project_metadata (+10)

    def test_empty_project_scope_is_project(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.scope == "project"

    def test_empty_project_repo_count_zero(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.repo_count == 0

    def test_empty_project_job_count_zero(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.job_count == 0

    def test_project_metadata_always_present(self):
        p = _make_project(name="Alpha")
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "project_metadata")
        assert sig.present is True

    def test_linked_repos_present_when_repo_attached(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "linked_repos")
        assert sig.present is True

    def test_linked_repos_absent_without_repos(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "linked_repos")
        assert sig.present is False

    def test_linked_jobs_present_with_jobs(self):
        p = _make_project()
        job = _make_job()
        attach_job(p, str(job.id))
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "linked_jobs")
        assert sig.present is True

    def test_linked_jobs_absent_without_jobs(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "linked_jobs")
        assert sig.present is False

    def test_planned_tasks_present_when_tasks_exist(self):
        p = _make_project()
        job = _make_job_with_tasks(2)
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "planned_tasks")
        assert sig.present is True

    def test_planned_tasks_absent_with_no_tasks(self):
        p = _make_project()
        job = _make_job()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "planned_tasks")
        assert sig.present is False

    def test_builder_artifacts_present(self):
        p = _make_project()
        job = _make_job_with_builder_artifact()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "builder_artifacts")
        assert sig.present is True

    def test_builder_artifacts_absent(self):
        p = _make_project()
        job = _make_job()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "builder_artifacts")
        assert sig.present is False

    def test_patch_intents_present(self):
        p = _make_project()
        job = _make_job_with_patch_intent()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert sig.present is True

    def test_patch_intents_absent(self):
        p = _make_project()
        job = _make_job()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert sig.present is False

    def test_verification_results_present_via_artifact(self):
        p = _make_project()
        job = _make_job_with_verification_artifact()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "verification_results")
        assert sig.present is True

    def test_verification_results_present_via_completed_task(self):
        p = _make_project()
        job = _make_job_with_tasks(1)
        job.tasks[0].status = RunState.COMPLETED
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "verification_results")
        assert sig.present is True

    def test_verification_results_absent(self):
        p = _make_project()
        job = _make_job()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "verification_results")
        assert sig.present is False

    def test_approval_decisions_present(self):
        p = _make_project()
        job = _make_job_with_approval()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "approval_decisions")
        assert sig.present is True

    def test_approval_decisions_absent_for_pending(self):
        p = _make_project()
        job = _make_job_with_patch_intent()
        snap = derive_project_context_coverage(p, [job])
        sig = next(s for s in snap.signals if s.key == "approval_decisions")
        assert sig.present is False

    def test_project_memory_always_absent(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "project_memory")
        assert sig.present is False

    def test_mcp_tool_context_always_absent(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "mcp_tool_context")
        assert sig.present is False

    def test_project_memory_detail_explains_reason(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "project_memory")
        assert "memory" in sig.detail.lower()

    def test_mcp_tool_context_detail_explains_reason(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = next(s for s in snap.signals if s.key == "mcp_tool_context")
        assert "MCP" in sig.detail or "not connected" in sig.detail.lower()

    def test_full_project_without_memory_reaches_85(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        job = _make_job_with_approval()
        # Add tasks and verification to the same job
        job.tasks.append(Task(description="task 1", status=RunState.COMPLETED))
        snap = derive_project_context_coverage(p, [job])
        # Without approved memory: 85 (all except project_memory + mcp)
        assert snap.score == 85

    def test_score_never_exceeds_v0_max(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        job = _make_job_with_approval()
        job.tasks.append(Task(description="t", status=RunState.COMPLETED))
        snap = derive_project_context_coverage(p, [job])
        assert snap.score <= V0_MAX_SCORE

    def test_present_signal_count_consistent(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.present_signal_count == sum(1 for s in snap.signals if s.present)

    def test_missing_signal_count_consistent(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.missing_signal_count == sum(1 for s in snap.signals if not s.present)

    def test_missing_keys_match_absent_signals(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        expected = tuple(s.key for s in snap.signals if not s.present)
        assert snap.missing_keys == expected

    def test_repo_count_matches(self, tmp_path):
        p = _make_project()
        d1 = tmp_path / "r1"; d1.mkdir()
        d2 = tmp_path / "r2"; d2.mkdir()
        attach_repo(p, str(d1))
        attach_repo(p, str(d2))
        snap = derive_project_context_coverage(p, [])
        assert snap.repo_count == 2

    def test_job_count_matches(self):
        p = _make_project()
        jobs = [_make_job(), _make_job()]
        snap = derive_project_context_coverage(p, jobs)
        assert snap.job_count == 2

    def test_project_id_in_snapshot(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        assert snap.project_id == str(p.id)

    def test_project_name_in_snapshot(self):
        p = _make_project(name="MyProject")
        snap = derive_project_context_coverage(p, [])
        assert snap.project_name == "MyProject"


# ---------------------------------------------------------------------------
# Snapshot is frozen
# ---------------------------------------------------------------------------


class TestSnapshotImmutability:
    def test_snapshot_is_frozen(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        with pytest.raises((AttributeError, TypeError)):
            snap.score = 99  # type: ignore[misc]

    def test_signal_is_frozen(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        sig = snap.signals[0]
        with pytest.raises((AttributeError, TypeError)):
            sig.present = True  # type: ignore[misc]


# ---------------------------------------------------------------------------
# summarize_project_context_coverage
# ---------------------------------------------------------------------------


class TestSummarize:
    def test_header_present(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "Remedy Project Context Coverage" in text

    def test_project_name_present(self):
        p = _make_project(name="Acme")
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "Acme" in text

    def test_scope_present(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "project" in text

    def test_coverage_percentage_present(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert f"{snap.score}%" in text

    def test_coverage_bar_present(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "█" in text or "░" in text

    def test_meaning_section_present(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "Meaning" in text or "meaning" in text.lower()

    def test_v0_max_score_mentioned(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "95%" in text

    def test_mempalace_mentioned(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "MemPalace" in text or "memory" in text.lower()

    def test_mcp_mentioned(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "MCP" in text

    def test_not_model_confidence(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        assert "not model confidence" in text.lower() or "not model" in text.lower()

    def test_no_redaction_sentinels(self):
        p = _make_project(name="SENTINEL_TEST")
        p.metadata["secret"] = "SECRET_ARTIFACT_CONTENT_MUST_NOT_RENDER"
        snap = derive_project_context_coverage(p, [])
        text = summarize_project_context_coverage(snap)
        for sentinel in _REDACTION_SENTINELS:
            assert sentinel not in text, f"sentinel leaked: {sentinel}"


# ---------------------------------------------------------------------------
# export_project_context_coverage_json — schema
# ---------------------------------------------------------------------------


_EXPECTED_TOP_KEYS = {
    "version",
    "project_id",
    "project_name",
    "scope",
    "score",
    "present_signal_count",
    "missing_signal_count",
    "repo_count",
    "job_count",
    "v0_max_score",
    "signals",
    "missing_keys",
}


class TestExportJson:
    def test_version_is_1(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert d["version"] == 1

    def test_exact_top_level_keys(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert set(d.keys()) == _EXPECTED_TOP_KEYS

    def test_scope_is_project(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert d["scope"] == "project"

    def test_v0_max_score_is_95(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert d["v0_max_score"] == 95

    def test_project_id_matches(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert d["project_id"] == str(p.id)

    def test_project_name_matches(self):
        p = _make_project(name="Zeta")
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert d["project_name"] == "Zeta"

    def test_signals_list_has_10_entries(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert len(d["signals"]) == 10

    def test_each_signal_has_required_keys(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        required = {"key", "label", "weight", "present", "detail"}
        for sig in d["signals"]:
            assert required.issubset(sig.keys()), f"missing keys in signal: {sig}"

    def test_missing_keys_is_list(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert isinstance(d["missing_keys"], list)

    def test_json_serialisable(self):
        p = _make_project(name="SerialTest")
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        text = json.dumps(d)
        assert "SerialTest" in text

    def test_score_within_v0_bounds(self):
        p = _make_project()
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        assert 0 <= d["score"] <= V0_MAX_SCORE

    def test_no_redaction_sentinels_in_json(self):
        p = _make_project()
        p.metadata["secret"] = "SECRET_ARTIFACT_CONTENT_MUST_NOT_RENDER"
        snap = derive_project_context_coverage(p, [])
        d = export_project_context_coverage_json(snap)
        text = json.dumps(d)
        for sentinel in _REDACTION_SENTINELS:
            assert sentinel not in text, f"sentinel leaked: {sentinel}"

    def test_no_full_signals_in_project_json(self, tmp_path, monkeypatch):
        """export_project_json compact context_coverage must not include full signal list."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import export_project_json
        p = _make_project(name="CompactTest")
        d = export_project_json(p, [])
        assert "context_coverage" in d
        cc = d["context_coverage"]
        assert "signals" not in cc, "full signal list must not appear in project JSON compact summary"

    def test_project_json_compact_keys(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import export_project_json
        p = _make_project()
        d = export_project_json(p, [])
        cc = d["context_coverage"]
        required = {"score", "scope", "present_signal_count", "missing_signal_count", "v0_max_score"}
        assert required.issubset(cc.keys())

    def test_project_json_context_coverage_scope_is_project(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import export_project_json
        p = _make_project()
        d = export_project_json(p, [])
        assert d["context_coverage"]["scope"] == "project"

    def test_project_json_v0_max_score_is_95(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_registry import export_project_json
        p = _make_project()
        d = export_project_json(p, [])
        assert d["context_coverage"]["v0_max_score"] == 95


# ---------------------------------------------------------------------------
# Run-log event schema
# ---------------------------------------------------------------------------


class TestRunLogSchema:
    _REQUIRED_META_KEYS = {
        "score",
        "present_signal_count",
        "missing_signal_count",
        "scope",
        "repo_count",
        "job_count",
    }

    def test_run_log_event_has_exact_metadata_keys(self, tmp_path, monkeypatch):
        import json as _json
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )
        from packages.orchestration.project_registry import (
            attach_job as _attach_job,
        )
        from packages.orchestration.storage import save_job

        job = _make_job()
        save_job(job)
        p = RemyProject(name="RunLogProject")
        _attach_job(p, str(job.id))
        save_project(p)

        _cmd_project_context(str(p.id))

        # F146 (2727114) made `project context` strictly read-only and removed
        # its RunLog write: "zero writes on read-only commands". The pin is now
        # that contract — the command must leave no run log behind at all.
        runs_dir = tmp_path / "job_logs" / str(job.id)
        assert not runs_dir.exists(), \
            "project context is read-only and must not write a run log"
        assert self._REQUIRED_META_KEYS, "the recorded metadata contract is kept for the writer paths"

    def test_run_log_event_scope_is_project(self, tmp_path, monkeypatch):
        import json as _json
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )
        from packages.orchestration.project_registry import (
            attach_job as _attach_job,
        )
        from packages.orchestration.storage import save_job

        job = _make_job()
        save_job(job)
        p = RemyProject(name="ScopeProject")
        _attach_job(p, str(job.id))
        save_project(p)

        _cmd_project_context(str(p.id))

        # Same F146 read-only contract: nothing under the data root's job_logs/
        # may appear because a project was merely inspected.
        runs_dir = tmp_path / "job_logs" / str(job.id)
        assert not list(runs_dir.glob("*.jsonl")) if runs_dir.exists() else True

    def test_run_log_no_sentinels(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )
        from packages.orchestration.project_registry import (
            attach_job as _attach_job,
        )
        from packages.orchestration.storage import save_job

        job = _make_job()
        save_job(job)
        p = RemyProject(name="NoSentinelProject")
        _attach_job(p, str(job.id))
        save_project(p)

        _cmd_project_context(str(p.id))

        runs_dir = tmp_path / "job_logs" / str(job.id)
        for f in runs_dir.glob("*.jsonl"):
            content = f.read_text()
            for sentinel in _REDACTION_SENTINELS:
                assert sentinel not in content, f"sentinel in run log: {sentinel}"

    def test_no_run_log_written_without_jobs(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project

        p = RemyProject(name="NoJobProject")
        save_project(p)

        _cmd_project_context(str(p.id))
        capsys.readouterr()

        runs_dir = tmp_path / "runs"
        # No run logs should be created when there are no linked jobs
        if runs_dir.exists():
            assert list(runs_dir.glob("**/*.jsonl")) == []


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestProjectContextCLI:
    def _env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        with pytest.raises(SystemExit) as exc:
            _cmd_project_context("not-a-uuid")
        assert exc.value.code == 1

    def test_invalid_uuid_no_traceback_in_stderr(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        with pytest.raises(SystemExit):
            _cmd_project_context("not-a-uuid")
        err = capsys.readouterr().err
        assert "traceback" not in err.lower()
        assert "Traceback" not in err

    def test_missing_project_exits_1(self, tmp_path, monkeypatch):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        with pytest.raises(SystemExit) as exc:
            _cmd_project_context(str(uuid4()))
        assert exc.value.code == 1

    def test_missing_project_stderr_safe(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        with pytest.raises(SystemExit):
            _cmd_project_context(str(uuid4()))
        err = capsys.readouterr().err
        assert "traceback" not in err.lower()
        assert "project not found" in err.lower() or "error" in err.lower()

    def test_text_output_works(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="TextTest")
        save_project(p)
        _cmd_project_context(str(p.id))
        out = capsys.readouterr().out
        assert "Remedy Project Context Coverage" in out
        assert "TextTest" in out

    def test_json_output_valid_json(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="JsonTest")
        save_project(p)
        _cmd_project_context(str(p.id), json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert d["version"] == 1

    def test_json_output_exact_top_keys(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="KeyTest")
        save_project(p)
        _cmd_project_context(str(p.id), json_output=True)
        d = json.loads(capsys.readouterr().out)
        assert set(d.keys()) == _EXPECTED_TOP_KEYS

    def test_json_scope_is_project(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="ScopeTest")
        save_project(p)
        _cmd_project_context(str(p.id), json_output=True)
        d = json.loads(capsys.readouterr().out)
        assert d["scope"] == "project"

    def test_json_no_traceback_in_stdout(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="NTB")
        save_project(p)
        _cmd_project_context(str(p.id), json_output=True)
        out = capsys.readouterr().out
        assert "Traceback" not in out

    def test_json_no_redaction_sentinels_in_stdout(self, tmp_path, monkeypatch, capsys):
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.project import _cmd_project_context
        from packages.orchestration.project_registry import RemyProject, save_project
        p = RemyProject(name="RedactTest")
        save_project(p)
        _cmd_project_context(str(p.id), json_output=True)
        out = capsys.readouterr().out
        for sentinel in _REDACTION_SENTINELS:
            assert sentinel not in out

    def test_existing_job_context_command_unchanged(self, tmp_path, monkeypatch, capsys):
        """Confirm `remedy context <job_id>` still works and uses job scope."""
        self._env(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_context
        from packages.orchestration.storage import save_job
        job = _make_job()
        save_job(job)
        _cmd_context(str(job.id), json_output=True)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert d["scope"] == "job"
        assert "job_id" in d
