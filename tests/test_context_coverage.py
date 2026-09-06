"""
Context Coverage v0 tests (Step 26).

Coverage:
  context_coverage.py:
    - empty job → score low (run_logs signal absent, planned_tasks absent, etc.)
    - attached_repo metadata → attached_repo signal present
    - project_constitution with source_files → signal present
    - planned tasks → planned_tasks present
    - builder artifact → builder_artifacts present
    - patch_intent metadata → patch_intents present
    - patch_intent_created event → patch_intents present
    - verification_passed/failed event → verification_results present
    - run_logs (non-empty events) → run_logs present
    - approval event → approval_decisions present
    - project_memory always absent in v0
    - mcp_tool_context always absent in v0
    - score clamps 0..100
    - score = round(present_weight / total_weight * 100)
    - JSON schema exact keys
    - text summary: header, coverage bar, meaning, not model confidence
    - no raw artifact content
    - no event message text in detail fields
    - no approval reason text
    - no diff preview text

  CLI (remedy context):
    - text output is human readable
    - --json output parses as JSON
    - invalid UUID exits 1
    - unknown job exits 1
    - context_coverage_inspected run-log schema exact keys
    - no raw sentinels in stdout/stderr/run logs

  Brain integration:
    - context_coverage node always present in build_project_brain
    - node status: low / partial / strong based on score
    - edge job --has_context_snapshot--> context_coverage exists
    - brain --json includes context_coverage node
    - brain-node context_coverage --json has correct 13 keys
    - brain-node context_coverage detail explains meaning + not model confidence

  Brain Viewer integration:
    - viewer_data.json includes context_coverage node in graph
    - index.html contains ctx-badge element
    - no raw sentinels in viewer files
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.context_coverage import (
    ContextCoverageSnapshot,
    derive_context_coverage,
    export_context_coverage_json,
    summarize_context_coverage,
)
from packages.orchestration.project_brain import (
    ET_HAS_CONTEXT_SNAPSHOT,
    NT_CONTEXT_COVERAGE,
    build_project_brain,
)
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_ALL_SENTINELS = [
    "ARTIFACT_CONTENT_MUST_NOT_RENDER",
    "DIFF_PREVIEW_MUST_NOT_RENDER",
    "APPROVAL_REASON_MUST_NOT_RENDER",
    "EVENT_MESSAGE_MUST_NOT_RENDER",
    "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
]

_CONTEXT_JSON_KEYS = frozenset(
    {
        "version",
        "job_id",
        "scope",
        "score",
        "present_weight",
        "total_weight",
        "signals",
        "missing_keys",
    }
)

_CONTEXT_COVERAGE_INSPECTED_METADATA_KEYS = frozenset(
    {"score", "present_signal_count", "missing_signal_count", "scope"}
)

_BRAIN_NODE_DETAIL_KEYS = frozenset({
    "job_id", "node_id", "node_type", "title", "status", "risk",
    "explanation", "why_it_exists", "connected_to", "evidence",
    "affected_files", "next_actions", "redaction_notes",
})


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Coverage test job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _write_run_events(tmp_path: Path, job_id, events: list[dict]) -> None:
    runs_dir = tmp_path / "job_logs" / str(job_id)
    runs_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e) for e in events]
    (runs_dir / "ctx_test_events.jsonl").write_text("\n".join(lines) + "\n")


def _read_run_log(tmp_path: Path, job_id) -> list[dict]:
    runs_dir = tmp_path / "job_logs" / str(job_id)
    if not runs_dir.exists():
        return []
    events: list[dict] = []
    for f in sorted(runs_dir.glob("*.jsonl")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def _verification_passed_event(job_id: str, task_id: str) -> dict:
    return {
        "event": "verification_passed",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-07T10:01:00+00:00",
        "outcome": "pass",
        "metadata": {"task_id": task_id},
    }


def _approval_event(job_id: str) -> dict:
    return {
        "event": "patch_intent_approved",
        "job_id": job_id,
        "run_id": "r1",
        "timestamp": "2026-05-07T10:02:00+00:00",
        "outcome": "approved",
        "metadata": {},
    }


def _mock_constitution(*, source_files=("CLAUDE.md",)):
    """Minimal duck-typed constitution with source_files."""
    class _Con:
        pass
    c = _Con()
    c.source_files = list(source_files)
    return c


def _add_builder_artifact(job: Job) -> Artifact:
    a = Artifact(
        name="builder output",
        content="some content",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
    )
    job.artifacts.append(a)
    return a


def _add_patch_intent_artifact(job: Job) -> Artifact:
    a = Artifact(
        name="builder output",
        content="some content",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={"patch_intent_count": 1},
    )
    job.artifacts.append(a)
    return a


def _call_context_json(job_id_str: str, monkeypatch, capsys) -> dict:
    import sys

    from apps.cli.main import main
    monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", job_id_str, "--json"])
    main()
    return json.loads(capsys.readouterr().out)


# ---------------------------------------------------------------------------
# TestContextCoverageSignals
# ---------------------------------------------------------------------------


class TestContextCoverageSignals:
    def test_empty_job_score_low(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        assert snap.score < 50
        assert snap.scope == "job"

    def test_empty_job_run_logs_absent(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "run_logs")
        assert not sig.present

    def test_attached_repo_increases_score(self):
        job_without = _make_job()
        job_with = _make_job()
        job_with.metadata["target_repo"] = "/some/repo"

        snap_without = derive_context_coverage(job_without, [])
        snap_with = derive_context_coverage(job_with, [])
        assert snap_with.score > snap_without.score

    def test_attached_repo_signal_present(self):
        job = _make_job()
        job.metadata["target_repo"] = "/some/repo"
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "attached_repo")
        assert sig.present

    def test_attached_repo_absent_when_no_metadata(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "attached_repo")
        assert not sig.present

    def test_constitution_signal_present(self):
        job = _make_job()
        snap = derive_context_coverage(job, [], constitution=_mock_constitution())
        sig = next(s for s in snap.signals if s.key == "project_constitution")
        assert sig.present

    def test_constitution_absent_when_none(self):
        job = _make_job()
        snap = derive_context_coverage(job, [], constitution=None)
        sig = next(s for s in snap.signals if s.key == "project_constitution")
        assert not sig.present

    def test_constitution_absent_when_empty_source_files(self):
        job = _make_job()
        snap = derive_context_coverage(
            job, [], constitution=_mock_constitution(source_files=())
        )
        sig = next(s for s in snap.signals if s.key == "project_constitution")
        assert not sig.present

    def test_planned_tasks_signal_present(self):
        job = _make_job()
        job.tasks.append(Task(description="do something", inputs={}))
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "planned_tasks")
        assert sig.present

    def test_planned_tasks_absent_when_no_tasks(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "planned_tasks")
        assert not sig.present

    def test_builder_artifacts_signal_present(self):
        job = _make_job()
        _add_builder_artifact(job)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "builder_artifacts")
        assert sig.present

    def test_builder_artifacts_absent_for_empty_job(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "builder_artifacts")
        assert not sig.present

    def test_patch_intents_via_artifact_metadata(self):
        job = _make_job()
        _add_patch_intent_artifact(job)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert sig.present

    def test_patch_intents_via_event(self):
        job = _make_job()
        events = [{"event": "patch_intent_created", "job_id": str(job.id),
                   "run_id": "r1", "timestamp": "2026-05-07T10:00:00+00:00",
                   "outcome": "created", "metadata": {}}]
        snap = derive_context_coverage(job, events)
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert sig.present

    def test_verification_results_signal_present(self):
        job = _make_job()
        events = [_verification_passed_event(str(job.id), str(uuid4()))]
        snap = derive_context_coverage(job, events)
        sig = next(s for s in snap.signals if s.key == "verification_results")
        assert sig.present

    def test_verification_results_absent_without_events(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "verification_results")
        assert not sig.present

    def test_run_logs_signal_present(self):
        job = _make_job()
        events = [{"event": "job_created", "job_id": str(job.id),
                   "run_id": "r0", "timestamp": "2026-05-07T09:59:00+00:00",
                   "outcome": "created", "metadata": {}}]
        snap = derive_context_coverage(job, events)
        sig = next(s for s in snap.signals if s.key == "run_logs")
        assert sig.present

    def test_approval_decisions_signal_present(self):
        job = _make_job()
        events = [_approval_event(str(job.id))]
        snap = derive_context_coverage(job, events)
        sig = next(s for s in snap.signals if s.key == "approval_decisions")
        assert sig.present

    def test_project_memory_absent_when_no_approved_entries(self):
        job = _make_job()
        job.metadata["target_repo"] = "/repo"
        snap = derive_context_coverage(
            job,
            [{"event": "any", "job_id": str(job.id), "metadata": {}}],
            constitution=_mock_constitution(),
        )
        sig = next(s for s in snap.signals if s.key == "project_memory")
        assert not sig.present
        assert "no approved memory" in sig.detail

    def test_project_memory_present_when_approved_entries_exist(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        job = _make_job()
        store_memory(key="k", value="v", job_id=str(job.id), approved=True)
        snap = derive_context_coverage(
            job,
            [{"event": "any", "job_id": str(job.id), "metadata": {}}],
            constitution=_mock_constitution(),
        )
        sig = next(s for s in snap.signals if s.key == "project_memory")
        assert sig.present
        assert "approved memory" in sig.detail

    def test_mcp_tool_context_always_absent_in_v0(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "mcp_tool_context")
        assert not sig.present
        assert "MCP" in sig.detail

    def test_total_weights_sum_to_100(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        assert snap.total_weight == 100

    def test_present_weight_matches_present_signals(self):
        job = _make_job()
        job.metadata["target_repo"] = "/repo"
        snap = derive_context_coverage(job, [])
        expected = sum(s.weight for s in snap.signals if s.present)
        assert snap.present_weight == expected

    def test_score_rounds_correctly(self):
        job = _make_job()
        job.metadata["target_repo"] = "/repo"
        snap = derive_context_coverage(job, [])
        expected = round(snap.present_weight / snap.total_weight * 100)
        assert snap.score == expected

    def test_score_clamps_to_zero_minimum(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        assert snap.score >= 0

    def test_score_clamps_to_100_maximum(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        assert snap.score <= 100

    def test_missing_keys_matches_absent_signals(self):
        job = _make_job()
        snap = derive_context_coverage(job, [])
        expected = frozenset(s.key for s in snap.signals if not s.present)
        assert frozenset(snap.missing_keys) == expected


# ---------------------------------------------------------------------------
# TestContextCoverageRedaction
# ---------------------------------------------------------------------------


class TestContextCoverageRedaction:
    """Verify that sentinels never appear in signal details or summaries."""

    def _snap_with_poisoned_events(self) -> ContextCoverageSnapshot:
        job = _make_job()
        events = [
            {
                "event": "task_run_failed",
                "job_id": str(job.id),
                "run_id": "r1",
                "timestamp": "2026-05-07T10:00:00+00:00",
                "message": "EVENT_MESSAGE_MUST_NOT_RENDER",
                "outcome": "error",
                "metadata": {
                    "command_output": "RAW_COMMAND_OUTPUT_MUST_NOT_RENDER",
                },
            }
        ]
        return derive_context_coverage(job, events)

    def test_no_sentinel_in_summary(self):
        snap = self._snap_with_poisoned_events()
        text = summarize_context_coverage(snap)
        for s in _ALL_SENTINELS:
            assert s not in text, f"sentinel {s!r} found in summary"

    def test_no_sentinel_in_json_export(self):
        snap = self._snap_with_poisoned_events()
        text = json.dumps(export_context_coverage_json(snap))
        for s in _ALL_SENTINELS:
            assert s not in text, f"sentinel {s!r} found in JSON export"

    def test_no_artifact_content_in_detail(self):
        job = _make_job()
        _add_builder_artifact(job)
        snap = derive_context_coverage(job, [])
        for sig in snap.signals:
            assert "ARTIFACT_CONTENT_MUST_NOT_RENDER" not in sig.detail

    def test_no_approval_reason_in_detail(self):
        job = _make_job()
        events = [
            {
                "event": "patch_intent_approved",
                "job_id": str(job.id),
                "run_id": "r1",
                "timestamp": "2026-05-07T10:00:00+00:00",
                "outcome": "approved",
                "metadata": {"reason": "APPROVAL_REASON_MUST_NOT_RENDER"},
            }
        ]
        snap = derive_context_coverage(job, events)
        for sig in snap.signals:
            assert "APPROVAL_REASON_MUST_NOT_RENDER" not in sig.detail


# ---------------------------------------------------------------------------
# TestSummarizeContextCoverage
# ---------------------------------------------------------------------------


class TestSummarizeContextCoverage:
    def _basic_snap(self) -> ContextCoverageSnapshot:
        return derive_context_coverage(_make_job(), [])

    def test_header_present(self):
        assert "Remedy Context Coverage" in summarize_context_coverage(self._basic_snap())

    def test_coverage_percent_present(self):
        snap = self._basic_snap()
        assert f"{snap.score}%" in summarize_context_coverage(snap)

    def test_meaning_section_present(self):
        text = summarize_context_coverage(self._basic_snap())
        assert "Meaning" in text
        assert "not model confidence" in text

    def test_not_model_confidence_stated(self):
        text = summarize_context_coverage(self._basic_snap())
        assert "not model confidence" in text

    def test_coverage_bar_present(self):
        text = summarize_context_coverage(self._basic_snap())
        assert "Coverage bar" in text
        assert "█" in text or "░" in text

    def test_next_actions_present(self):
        text = summarize_context_coverage(self._basic_snap())
        assert "remedy brain" in text
        assert "remedy brain trust" in text

    def test_scope_present(self):
        text = summarize_context_coverage(self._basic_snap())
        assert "Scope: job" in text


# ---------------------------------------------------------------------------
# TestExportContextCoverageJson
# ---------------------------------------------------------------------------


class TestExportContextCoverageJson:
    def test_top_level_keys(self):
        snap = derive_context_coverage(_make_job(), [])
        exported = export_context_coverage_json(snap)
        assert set(exported.keys()) == _CONTEXT_JSON_KEYS

    def test_version_is_1(self):
        snap = derive_context_coverage(_make_job(), [])
        assert export_context_coverage_json(snap)["version"] == 1

    def test_signals_is_list(self):
        snap = derive_context_coverage(_make_job(), [])
        exported = export_context_coverage_json(snap)
        assert isinstance(exported["signals"], list)

    def test_each_signal_has_required_keys(self):
        snap = derive_context_coverage(_make_job(), [])
        exported = export_context_coverage_json(snap)
        required = {"key", "label", "present", "weight", "detail"}
        for sig in exported["signals"]:
            assert set(sig.keys()) == required

    def test_json_serialisable(self):
        snap = derive_context_coverage(_make_job(), [])
        serialised = json.dumps(export_context_coverage_json(snap))
        assert json.loads(serialised)["version"] == 1

    def test_missing_keys_is_list(self):
        snap = derive_context_coverage(_make_job(), [])
        exported = export_context_coverage_json(snap)
        assert isinstance(exported["missing_keys"], list)


# ---------------------------------------------------------------------------
# TestContextCoverageCli
# ---------------------------------------------------------------------------


class TestContextCoverageCli:
    def test_invalid_uuid_exits_1(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", "not-a-uuid"])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
        assert "invalid job ID" in capsys.readouterr().err

    def test_unknown_job_exits_1(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "context", str(uuid4())]
        )
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_text_output_human_readable(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()
        out = capsys.readouterr().out
        assert "Remedy Context Coverage" in out
        assert "not model confidence" in out

    def test_json_output_parseable(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "context", str(job.id), "--json"]
        )
        main()
        raw = capsys.readouterr().out
        parsed = json.loads(raw)
        assert parsed["version"] == 1

    def test_json_stdout_is_pure_json(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "context", str(job.id), "--json"]
        )
        main()
        raw = capsys.readouterr().out
        assert raw.startswith("{") or raw.startswith("[")
        json.loads(raw)  # must parse

    def test_run_log_event_emitted(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        logged = [e for e in events if e.get("event") == "context_coverage_inspected"]
        assert len(logged) == 1

    def test_run_log_exact_schema(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        ev = next(e for e in events if e.get("event") == "context_coverage_inspected")
        meta = ev["metadata"]
        actual = set(meta.keys())
        extra = actual - _CONTEXT_COVERAGE_INSPECTED_METADATA_KEYS
        missing = _CONTEXT_COVERAGE_INSPECTED_METADATA_KEYS - actual
        assert actual == _CONTEXT_COVERAGE_INSPECTED_METADATA_KEYS, (
            f"extra={extra!r}  missing={missing!r}"
        )

    def test_run_log_scope_is_job(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        ev = next(e for e in events if e.get("event") == "context_coverage_inspected")
        assert ev["metadata"]["scope"] == "job"

    def test_no_sentinels_in_stdout(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "context", str(job.id), "--json"]
        )
        main()
        out = capsys.readouterr().out
        for s in _ALL_SENTINELS:
            assert s not in out, f"sentinel {s!r} found in stdout"

    def test_no_sentinels_in_run_log(self, tmp_path, monkeypatch, capsys):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()
        capsys.readouterr()
        events = _read_run_log(tmp_path, job.id)
        ev = next(e for e in events if e.get("event") == "context_coverage_inspected")
        serialised = json.dumps(ev)
        for s in _ALL_SENTINELS:
            assert s not in serialised, f"sentinel {s!r} found in run log"


# ---------------------------------------------------------------------------
# TestBrainContextCoverageNode
# ---------------------------------------------------------------------------


class TestBrainContextCoverageNode:
    def test_context_coverage_node_always_present(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        cc = [n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE]
        assert len(cc) == 1

    def test_context_coverage_node_id(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert cc.id == "context_coverage"

    def test_context_coverage_node_status_low(self):
        job = _make_job()  # empty job → score low
        graph = build_project_brain(job, [])
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert cc.status == "low"

    def test_context_coverage_node_status_strong(self):
        job = _make_job()
        job.metadata["target_repo"] = "/repo"
        job.tasks.append(Task(description="do x", inputs={"task_type": "write_readme"}))
        job.tasks[0].status = RunState.COMPLETED
        _add_builder_artifact(job)
        _add_patch_intent_artifact(job)
        events = [
            _verification_passed_event(str(job.id), str(uuid4())),
            _approval_event(str(job.id)),
            {"event": "job_created", "job_id": str(job.id),
             "run_id": "r0", "timestamp": "2026-05-07T09:59:00+00:00",
             "outcome": "created", "metadata": {}},
        ]
        graph = build_project_brain(
            job, events,
            constitution=_mock_constitution(),
        )
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert cc.status in ("partial", "strong")

    def test_context_coverage_edge_exists(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        edges = [
            e for e in graph.edges
            if e.target == "context_coverage" and e.type == ET_HAS_CONTEXT_SNAPSHOT
        ]
        assert len(edges) == 1
        assert edges[0].source == str(job.id)

    def test_context_coverage_label_contains_percent(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert "%" in cc.label

    def test_context_coverage_metadata_keys(self):
        job = _make_job()
        graph = build_project_brain(job, [])
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert "score" in cc.metadata
        assert "present_signal_count" in cc.metadata
        assert "missing_signal_count" in cc.metadata
        assert "scope" in cc.metadata

    def test_brain_json_includes_context_coverage_node(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"]
        )
        main()
        brain = json.loads(capsys.readouterr().out)
        types = {n["type"] for n in brain["nodes"]}
        assert "context_coverage" in types


# ---------------------------------------------------------------------------
# TestBrainNodeContextCoverageDetail
# ---------------------------------------------------------------------------


class TestBrainNodeContextCoverageDetail:
    def test_context_coverage_node_json_keys(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"]
        )
        main()
        brain = json.loads(capsys.readouterr().out)
        cc_node = next(n for n in brain["nodes"] if n["type"] == "context_coverage")

        monkeypatch.setattr(
            sys, "argv",
            ["remedy", "brain", "node", str(job.id), cc_node["id"], "--json"],
        )
        main()
        detail = json.loads(capsys.readouterr().out)
        assert set(detail.keys()) == _BRAIN_NODE_DETAIL_KEYS

    def test_context_coverage_detail_explains_meaning(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"]
        )
        main()
        brain = json.loads(capsys.readouterr().out)
        cc_node = next(n for n in brain["nodes"] if n["type"] == "context_coverage")

        monkeypatch.setattr(
            sys, "argv",
            ["remedy", "brain", "node", str(job.id), cc_node["id"], "--json"],
        )
        main()
        detail = json.loads(capsys.readouterr().out)
        assert "not model confidence" in detail["explanation"]

    def test_context_coverage_detail_node_type(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(
            sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"]
        )
        main()
        brain = json.loads(capsys.readouterr().out)
        cc_node = next(n for n in brain["nodes"] if n["type"] == "context_coverage")

        monkeypatch.setattr(
            sys, "argv",
            ["remedy", "brain", "node", str(job.id), cc_node["id"], "--json"],
        )
        main()
        detail = json.loads(capsys.readouterr().out)
        assert detail["node_type"] == "context_coverage"


# ---------------------------------------------------------------------------
# TestBrainViewerContextCoverage
# ---------------------------------------------------------------------------


class TestBrainViewerContextCoverage:
    def _write_viewer(self, tmp_path: Path) -> Path:
        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
            write_brain_viewer_files,
        )

        job = _make_job()
        graph = build_project_brain(job, [])
        data = build_brain_viewer_data(job, graph, [])
        out_dir = tmp_path / "viewers" / str(job.id)
        return write_brain_viewer_files(data, out_dir)

    def test_viewer_data_json_has_context_coverage_node(self, tmp_path):
        index_path = self._write_viewer(tmp_path)
        parsed = json.loads((index_path.parent / "viewer_data.json").read_text())
        types = {n["type"] for n in parsed["graph"]["nodes"]}
        assert "context_coverage" in types

    def test_index_html_has_ctx_badge(self, tmp_path):
        index_path = self._write_viewer(tmp_path)
        html = index_path.read_text()
        assert "ctx-badge" in html

    def test_viewer_no_sentinels(self, tmp_path):
        index_path = self._write_viewer(tmp_path)
        for fname in ("viewer_data.json", "index.html"):
            text = (index_path.parent / fname).read_text()
            for s in _ALL_SENTINELS:
                assert s not in text, f"sentinel {s!r} in {fname}"


# ---------------------------------------------------------------------------
# TestSafeInt — Step 26.1 A
# ---------------------------------------------------------------------------


class TestSafeInt:
    """Verify that malformed patch_intent_count metadata never crashes."""

    def test_string_count_1_counts_as_present(self):
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": "1"},
        )
        job.artifacts.append(a)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert sig.present

    def test_string_not_an_int_doesnt_crash(self):
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": "not-an-int"},
        )
        job.artifacts.append(a)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert not sig.present

    def test_list_count_doesnt_crash(self):
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": []},
        )
        job.artifacts.append(a)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert not sig.present

    def test_none_count_doesnt_crash(self):
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": None},
        )
        job.artifacts.append(a)
        snap = derive_context_coverage(job, [])
        sig = next(s for s in snap.signals if s.key == "patch_intents")
        assert not sig.present

    def test_build_project_brain_with_malformed_count_doesnt_crash(self):
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": "bad"},
        )
        job.artifacts.append(a)
        graph = build_project_brain(job, [])
        assert any(n.type == NT_CONTEXT_COVERAGE for n in graph.nodes)

    def test_brain_json_with_malformed_count_is_valid_json(
        self, tmp_path, monkeypatch, capsys
    ):
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        a = Artifact(
            name="bp",
            content="x",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={"patch_intent_count": "not-a-number"},
        )
        job.artifacts.append(a)
        save_job(job)
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        raw = capsys.readouterr().out
        parsed = json.loads(raw)
        assert "nodes" in parsed


# ---------------------------------------------------------------------------
# TestV0Ceiling — Step 26.1 B
# ---------------------------------------------------------------------------


class TestV0Ceiling:
    """Without approved memory, max score is 85. With memory, max is 95 (only MCP absent)."""

    def _fully_populated_job(self):
        job = _make_job()
        job.metadata["target_repo"] = "/repo"
        job.tasks.append(Task(description="do x", inputs={"task_type": "write_readme"}))
        _add_builder_artifact(job)
        _add_patch_intent_artifact(job)
        return job

    def _fully_populated_events(self, job):
        return [
            _verification_passed_event(str(job.id), str(uuid4())),
            _approval_event(str(job.id)),
            {"event": "job_created", "job_id": str(job.id),
             "run_id": "r0", "timestamp": "2026-05-07T09:59:00+00:00",
             "outcome": "created", "metadata": {}},
        ]

    def test_fully_populated_v0_score_is_85(self):
        job = self._fully_populated_job()
        snap = derive_context_coverage(
            job,
            self._fully_populated_events(job),
            constitution=_mock_constitution(),
        )
        assert snap.score == 85

    def test_summary_mentions_95_ceiling(self):
        job = self._fully_populated_job()
        snap = derive_context_coverage(
            job,
            self._fully_populated_events(job),
            constitution=_mock_constitution(),
        )
        text = summarize_context_coverage(snap)
        assert "95%" in text

    def test_summary_mentions_v0_ceiling_explanation(self):
        snap = derive_context_coverage(_make_job(), [])
        text = summarize_context_coverage(snap)
        assert "v0" in text
        assert "maximum" in text.lower() or "95%" in text

    def test_json_score_is_integer(self):
        job = self._fully_populated_job()
        snap = derive_context_coverage(
            job,
            self._fully_populated_events(job),
            constitution=_mock_constitution(),
        )
        exported = export_context_coverage_json(snap)
        assert isinstance(exported["score"], int)

    def test_context_coverage_node_status_strong_at_85(self):
        job = self._fully_populated_job()
        graph = build_project_brain(
            job,
            self._fully_populated_events(job),
            constitution=_mock_constitution(),
        )
        cc = next(n for n in graph.nodes if n.type == NT_CONTEXT_COVERAGE)
        assert cc.status == "strong"
        assert cc.metadata["score"] == 85


# ---------------------------------------------------------------------------
# TestContextCmdStaleRepo — Step 26.1 C
# ---------------------------------------------------------------------------


class TestContextCmdStaleRepo:
    """_cmd_context mirrors _cmd_brain_view: warns on stale/invalid repo."""

    def _run_context(self, job_id_str: str, monkeypatch, capsys, tmp_path):
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", job_id_str])
        main()
        return capsys.readouterr()

    def test_stale_repo_path_warns_stderr(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent_repo")
        save_job(job)
        result = self._run_context(str(job.id), monkeypatch, capsys, tmp_path)
        assert "Warning: project constitution unavailable for context coverage." in result.err

    def test_stale_repo_exits_0(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "nonexistent_repo")
        save_job(job)
        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job.id)])
        main()  # must not raise SystemExit

    def test_file_not_dir_warns_stderr(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fake_file = tmp_path / "not_a_dir.txt"
        fake_file.write_text("x")
        job = _make_job()
        job.metadata["target_repo"] = str(fake_file)
        save_job(job)
        result = self._run_context(str(job.id), monkeypatch, capsys, tmp_path)
        assert "Warning: project constitution unavailable for context coverage." in result.err

    def test_runtime_error_doesnt_leak_secret(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration import project_constitution as _pc_mod
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path)
        save_job(job)

        real_dir = tmp_path / "repo"
        real_dir.mkdir()
        job2 = _make_job()
        job2.metadata["target_repo"] = str(real_dir)
        save_job(job2)

        def _boom(path):
            raise RuntimeError("SECRET_INTERNAL_PATH_DATA")

        monkeypatch.setattr(_pc_mod, "load_project_constitution", _boom)

        import sys

        from apps.cli.main import main
        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "context", str(job2.id)])
        main()
        result = capsys.readouterr()
        assert "SECRET_INTERNAL_PATH_DATA" not in result.err
        assert "SECRET_INTERNAL_PATH_DATA" not in result.out

    def test_no_target_repo_no_warning(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        result = self._run_context(str(job.id), monkeypatch, capsys, tmp_path)
        assert "Warning" not in result.err

    def test_valid_repo_no_warning(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        real_dir = tmp_path / "repo"
        real_dir.mkdir()
        job = _make_job()
        job.metadata["target_repo"] = str(real_dir)
        save_job(job)
        result = self._run_context(str(job.id), monkeypatch, capsys, tmp_path)
        assert "Warning" not in result.err


# ---------------------------------------------------------------------------
# TestContextCoverageDetailConfidenceKeys — Step 26.1 D
# ---------------------------------------------------------------------------


class TestContextCoverageDetailConfidenceKeys:
    """Brain-node detail for context_coverage must not claim to be a confidence score."""

    def _get_detail(self, tmp_path, monkeypatch, capsys) -> dict:
        import sys

        from apps.cli.main import main

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        monkeypatch.setattr(sys, "argv", ["remedy", "brain", "graph", str(job.id), "--json"])
        main()
        brain = json.loads(capsys.readouterr().out)
        cc_node = next(n for n in brain["nodes"] if n["type"] == "context_coverage")

        monkeypatch.setattr(
            sys, "argv",
            ["remedy", "brain", "node", str(job.id), cc_node["id"], "--json"],
        )
        main()
        return json.loads(capsys.readouterr().out)

    def test_no_confidence_key(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(tmp_path, monkeypatch, capsys)
        assert "confidence" not in detail

    def test_no_model_confidence_key(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(tmp_path, monkeypatch, capsys)
        assert "model_confidence" not in detail

    def test_no_confidence_score_key(self, tmp_path, monkeypatch, capsys):
        detail = self._get_detail(tmp_path, monkeypatch, capsys)
        assert "confidence_score" not in detail

    def test_explanation_negates_correctness_guarantee(
        self, tmp_path, monkeypatch, capsys
    ):
        detail = self._get_detail(tmp_path, monkeypatch, capsys)
        explanation = detail.get("explanation", "").lower()
        assert "not a guarantee" in explanation
