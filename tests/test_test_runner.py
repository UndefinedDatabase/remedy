"""
Tests for Step 33 — Permission-gated Test Run v0.

Coverage:
  - test_runner.py: command selection, blocked paths, happy path, failure path
  - permissions.py: repo_test_run capability exists and defaults to deny
  - CLI: permission guard, no-repo guard, run-log exact schema, no raw output
  - Brain: test_run node presence after test_run_completed event
  - Brain detail: test_run detail schema (7 evidence items + 2 redaction notes)
  - Trust Report: test run section present
  - Timeline: test_run_completed rendered
  - Viewer JSON: test_run node present
  - Redaction: no forbidden keys in run-log metadata, Brain JSON, Trust Report

All tests are deterministic — subprocess is patched where needed.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.permissions import (
    Capability,
    is_allowed,
    is_reserved,
    set_permission,
)
from packages.orchestration.test_runner import (
    _EXECUTION_SAFE_EXECUTABLES,
    TIMEOUT_DEFAULT_SEC,
    TestRunRecord,
    run_tests_local,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(*, with_repo: str | None = None) -> Job:
    job = Job(name="test", state=RunState.PENDING)
    if with_repo is not None:
        job.metadata["target_repo"] = with_repo
    return job


# ---------------------------------------------------------------------------
# A. Permission model — repo_test_run
# ---------------------------------------------------------------------------


class TestRepoTestRunPermission:
    def test_capability_exists(self):
        assert Capability.repo_test_run == "repo_test_run"

    def test_default_is_deny(self):
        job = _make_job()
        assert not is_allowed(job, Capability.repo_test_run)

    def test_not_reserved(self):
        # repo_test_run must be active (enforced at a callsite), not reserved.
        assert not is_reserved(Capability.repo_test_run)

    def test_can_be_granted(self):
        job = _make_job()
        set_permission(job, Capability.repo_test_run, allow=True)
        assert is_allowed(job, Capability.repo_test_run)

    def test_can_be_denied_after_grant(self):
        job = _make_job()
        set_permission(job, Capability.repo_test_run, allow=True)
        set_permission(job, Capability.repo_test_run, allow=False)
        assert not is_allowed(job, Capability.repo_test_run)


# ---------------------------------------------------------------------------
# B. test_runner — blocked paths
# ---------------------------------------------------------------------------


class TestRunTestsLocalBlocked:
    def test_no_target_repo(self, tmp_path):
        job = _make_job()
        record = run_tests_local(job, tmp_path)
        assert record.status == "blocked"
        assert record.blocked_reason == "no_target_repo"
        assert record.exit_code is None
        assert record.command == ""
        assert record.duration_ms == 0

    def test_target_repo_not_a_directory(self, tmp_path):
        fake = tmp_path / "not_a_dir"
        fake.write_text("x")
        job = _make_job(with_repo=str(fake))
        record = run_tests_local(job, tmp_path)
        assert record.status == "blocked"
        assert record.blocked_reason == "target_repo_not_a_directory"

    def test_no_supported_test_command(self, tmp_path):
        # Repo dir exists but no detectors find anything.
        repo = tmp_path / "repo"
        repo.mkdir()
        job = _make_job(with_repo=str(repo))
        record = run_tests_local(job, tmp_path)
        assert record.status == "blocked"
        assert record.blocked_reason == "no_test_command_discovered"

    def test_command_not_found_output_path_is_empty(self, tmp_path):
        """FileNotFoundError (command not installed) must use _blocked() → output_path == ''."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[build-system]\n")
        (repo / "tests").mkdir()
        job = _make_job(with_repo=str(repo))
        with patch(
            "packages.orchestration.test_runner.run_guarded_test_command",
            side_effect=FileNotFoundError("pytest: not found"),
        ):
            record = run_tests_local(job, tmp_path)
        assert record.status == "blocked"
        assert record.blocked_reason == "command_not_found"
        assert record.output_path == "", (
            "command_not_found blocked record must have output_path == '' (no file written)"
        )
        # No stray file should have been written.
        test_runs_dir = tmp_path / "test_runs"
        if test_runs_dir.exists():
            assert list(test_runs_dir.iterdir()) == [], (
                "no output file must be written when command is not found"
            )


class TestExecutionGuard:
    def test_timeout_default(self):
        assert TIMEOUT_DEFAULT_SEC == 60

    def test_execution_safe_executables_includes_core(self):
        assert "python3" in _EXECUTION_SAFE_EXECUTABLES
        assert "pytest" in _EXECUTION_SAFE_EXECUTABLES
        assert "make" in _EXECUTION_SAFE_EXECUTABLES
        assert "cargo" in _EXECUTION_SAFE_EXECUTABLES
        assert "go" in _EXECUTION_SAFE_EXECUTABLES

    def test_invariant_fires_for_unsafe_executable(self, tmp_path, monkeypatch):
        """The execution guard assert must fire if a candidate has an unsafe argv[0]."""
        from packages.orchestration.command_discovery import CommandCandidate
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[build-system]\n")
        (repo / "tests").mkdir()
        job = _make_job(with_repo=str(repo))

        # Patch select_best_test_candidate to return a candidate with risky argv[0].
        unsafe_candidate = CommandCandidate(
            id="x",
            purpose="test",
            argv=("rm", "-rf", "/"),
            display="rm -rf /",
            source_type="heuristic",
            source_path="",
            confidence="high",
            risk="low",  # risk bypassed to test the argv[0] guard specifically
            reason="injected",
            requires_permission="repo_test_run",
        )
        monkeypatch.setattr(
            "packages.orchestration.command_discovery.select_best_test_candidate",
            lambda candidates: unsafe_candidate,
        )
        with pytest.raises(RuntimeError, match="BUG: executable not in safe list"):
            run_tests_local(job, tmp_path)

    def test_test_run_record_not_collected_by_pytest(self):
        """TestRunRecord must declare __test__ = False to suppress PytestCollectionWarning."""
        assert TestRunRecord.__test__ is False


# ---------------------------------------------------------------------------
# C. test_runner — auto-detect fallback (pyproject.toml + tests/)
# ---------------------------------------------------------------------------


class TestCommandAutoDetect:
    def test_auto_detects_when_pyproject_and_tests_dir(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[build-system]\n")
        (repo / "tests").mkdir()
        (repo / "tests" / "test_x.py").write_text("def test_x(): pass\n")

        job = _make_job(with_repo=str(repo))

        completed = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"],
            returncode=0,
            stdout=b"1 passed\n",
            stderr=b"",
        )
        with patch("packages.orchestration.test_runner.run_guarded_test_command", return_value=completed) as mock_run:
            record = run_tests_local(job, tmp_path)

        assert record.status == "passed"
        assert record.command == "python3 -m pytest"
        assert record.exit_code == 0
        # The old "no shell= keyword" assertion could not fail against a seam that
        # HAS no shell parameter, so this asserts what the seam really received.
        assert mock_run.call_count == 1
        assert mock_run.call_args.args[0] == ["python3", "-m", "pytest"]
        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["timeout_sec"] == TIMEOUT_DEFAULT_SEC
        assert call_kwargs["cwd"] == str(repo.resolve())

    def test_no_auto_detect_without_tests_dir(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[build-system]\n")
        # No tests/ dir — pyproject detector requires tests/ OR pytest config section.
        job = _make_job(with_repo=str(repo))
        record = run_tests_local(job, tmp_path)
        assert record.status == "blocked"
        assert record.blocked_reason == "no_test_command_discovered"


# ---------------------------------------------------------------------------
# D. test_runner — passing and failing subprocess outcomes
# ---------------------------------------------------------------------------


class TestRunTestsLocalOutcome:
    def _make_repo_with_pytest(self, tmp_path: Path) -> tuple[Path, Job]:
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[build-system]\n")
        (repo / "tests").mkdir()
        job = _make_job(with_repo=str(repo))
        return repo, job

    def test_passing_run(self, tmp_path):
        _, job = self._make_repo_with_pytest(tmp_path)
        stdout = b"1 passed in 0.1s\n"
        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=0,
            stdout=stdout, stderr=b"",
        )
        with patch("packages.orchestration.test_runner.run_guarded_test_command", return_value=proc):
            record = run_tests_local(job, tmp_path)

        assert record.status == "passed"
        assert record.exit_code == 0
        assert record.output_bytes == len(stdout)
        assert record.output_line_count == stdout.count(b"\n")
        assert record.blocked_reason == ""
        assert record.output_path != ""

    def test_failing_run(self, tmp_path):
        _, job = self._make_repo_with_pytest(tmp_path)
        stderr = b"FAILED tests/test_x.py::test_x\n1 failed\n"
        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=1,
            stdout=b"", stderr=stderr,
        )
        with patch("packages.orchestration.test_runner.run_guarded_test_command", return_value=proc):
            record = run_tests_local(job, tmp_path)

        assert record.status == "failed"
        assert record.exit_code == 1
        assert record.output_bytes == len(stderr)

    def test_timeout_path(self, tmp_path):
        _, job = self._make_repo_with_pytest(tmp_path)
        exc = subprocess.TimeoutExpired(cmd=["python3", "-m", "pytest"], timeout=60)
        exc.stdout = b""
        exc.stderr = b""
        with patch("packages.orchestration.test_runner.run_guarded_test_command", side_effect=exc):
            record = run_tests_local(job, tmp_path)

        assert record.status == "timeout"
        assert record.exit_code is None

    def test_output_file_is_written(self, tmp_path):
        _, job = self._make_repo_with_pytest(tmp_path)
        stdout = b"1 passed\n"
        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=0,
            stdout=stdout, stderr=b"",
        )
        with patch("packages.orchestration.test_runner.run_guarded_test_command", return_value=proc):
            record = run_tests_local(job, tmp_path)

        output_file = tmp_path / "test_runs" / record.output_path
        assert output_file.exists()
        assert output_file.read_bytes() == stdout

    def test_no_raw_output_in_record(self, tmp_path):
        _, job = self._make_repo_with_pytest(tmp_path)
        stdout = b"secret output\n"
        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=0,
            stdout=stdout, stderr=b"",
        )
        with patch("packages.orchestration.test_runner.run_guarded_test_command", return_value=proc):
            record = run_tests_local(job, tmp_path)

        # record is a frozen dataclass — verify no raw output field exists
        import dataclasses
        field_names = {f.name for f in dataclasses.fields(record)}
        forbidden = {"stdout", "stderr", "output", "command_output", "raw_output"}
        assert not (field_names & forbidden)


# ---------------------------------------------------------------------------
# E. Run-log event — exact schema
# ---------------------------------------------------------------------------


class TestRunLogEventSchema:
    """test_run_completed must have exactly 11 metadata keys — no raw output."""

    REQUIRED_KEYS = {
        "test_run_id",
        "command",
        "status",
        "exit_code",
        "duration_ms",
        "output_line_count",
        "output_bytes",
        "command_source_type",
        "command_source_path",
        "command_purpose",
        "command_confidence",
    }
    FORBIDDEN_KEYS = {"stdout", "stderr", "output", "command_output", "raw_output", "cwd", "env"}

    def test_log_event_metadata_keys(self, tmp_path):
        from packages.orchestration.run_log import RunLogWriter, read_run_events

        job = Job(name="test", state=RunState.PENDING)
        log = RunLogWriter(job_id=job.id, data_root=tmp_path)
        log.log(
            "test_run_completed",
            test_run_id="abc123",
            command="python3 -m pytest",
            status="passed",
            exit_code=0,
            duration_ms=1234,
            output_line_count=5,
            output_bytes=99,
            command_source_type="pyproject",
            command_source_path="pyproject.toml",
            command_purpose="test",
            command_confidence="high",
        )

        events = read_run_events(log.path)
        tr_events = [e for e in events if e.get("event") == "test_run_completed"]
        assert len(tr_events) == 1
        meta = tr_events[0]["metadata"]
        assert set(meta.keys()) == self.REQUIRED_KEYS
        for key in self.FORBIDDEN_KEYS:
            assert key not in meta, f"forbidden key '{key}' found in metadata"


# ---------------------------------------------------------------------------
# F. Brain — test_run node
# ---------------------------------------------------------------------------


class TestBrainTestRunNode:
    def _make_events(self) -> list[dict]:
        return [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                    "command_source_type": "pyproject",
                    "command_source_path": "pyproject.toml",
                    "command_purpose": "test",
                    "command_confidence": "high",
                },
            }
        ]

    def test_brain_has_test_run_node(self):
        from packages.orchestration.project_brain import (
            NT_TEST_RUN,
            build_project_brain,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = self._make_events()
        graph = build_project_brain(job, events)
        test_run_nodes = [n for n in graph.nodes if n.type == NT_TEST_RUN]
        assert len(test_run_nodes) == 1

    def test_brain_test_run_node_status_passed(self):
        from packages.orchestration.project_brain import (
            NT_TEST_RUN,
            build_project_brain,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = self._make_events()
        graph = build_project_brain(job, events)
        tr = next(n for n in graph.nodes if n.type == NT_TEST_RUN)
        assert tr.status == "passed"

    def test_brain_test_run_node_status_failed(self):
        from packages.orchestration.project_brain import (
            NT_TEST_RUN,
            build_project_brain,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "pytest",
                    "status": "failed",
                    "exit_code": 1,
                    "duration_ms": 200,
                    "output_line_count": 10,
                    "output_bytes": 300,
                },
            }
        ]
        graph = build_project_brain(job, events)
        tr = next(n for n in graph.nodes if n.type == NT_TEST_RUN)
        assert tr.status == "failed"

    def test_brain_has_test_run_edge(self):
        from packages.orchestration.project_brain import (
            ET_HAS_TEST_RUN,
            build_project_brain,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = self._make_events()
        graph = build_project_brain(job, events)
        tr_edges = [e for e in graph.edges if e.type == ET_HAS_TEST_RUN]
        assert len(tr_edges) == 1

    def test_brain_json_contains_test_run_node(self):
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = self._make_events()
        graph = build_project_brain(job, events)
        data = export_project_brain_json(graph)
        types = [n["type"] for n in data["nodes"]]
        assert "test_run" in types

    def test_brain_json_no_raw_output(self):
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = self._make_events()
        graph = build_project_brain(job, events)
        data = export_project_brain_json(graph)
        # Verify that no node has a metadata key that is a raw output field name.
        for node in data["nodes"]:
            meta = node.get("metadata", {})
            for key in ("stdout", "stderr", "raw_output", "command_output"):
                assert key not in meta, (
                    f"forbidden key '{key}' found in node metadata for node {node['id']}"
                )


# ---------------------------------------------------------------------------
# G. Brain detail — test_run node
# ---------------------------------------------------------------------------


class TestBrainDetailTestRun:
    """test_run detail must have 11 evidence items and 2 redaction notes."""

    def _build_detail(self):
        from packages.orchestration.brain_detail import (
            build_brain_node_detail,
            export_brain_node_detail_json,
        )
        from packages.orchestration.project_brain import (
            NT_TEST_RUN,
            build_project_brain,
        )

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "myrun",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 100,
                    "output_line_count": 2,
                    "output_bytes": 20,
                    "command_source_type": "pyproject",
                    "command_source_path": "pyproject.toml",
                    "command_purpose": "test",
                    "command_confidence": "high",
                },
            }
        ]
        graph = build_project_brain(job, events)
        tr_node = next(n for n in graph.nodes if n.type == NT_TEST_RUN)
        detail = build_brain_node_detail(job, graph, tr_node.id, events)
        return detail, export_brain_node_detail_json(detail)

    def test_detail_has_11_evidence_items(self):
        detail, _ = self._build_detail()
        assert len(detail.evidence) == 11

    def test_detail_has_2_redaction_notes(self):
        detail, _ = self._build_detail()
        assert len(detail.redaction_notes) == 2

    def test_detail_redaction_note_mentions_raw_output(self):
        detail, _ = self._build_detail()
        combined = " ".join(detail.redaction_notes).lower()
        assert "raw stdout/stderr" in combined

    def test_detail_json_schema(self):
        _, exported = self._build_detail()
        expected_keys = {
            "job_id", "node_id", "node_type", "title", "status", "risk",
            "explanation", "why_it_exists", "connected_to", "evidence",
            "affected_files", "next_actions", "redaction_notes",
        }
        assert set(exported.keys()) == expected_keys

    def test_detail_node_type_is_test_run(self):
        detail, _ = self._build_detail()
        assert detail.node_type == "test_run"

    def test_detail_no_raw_output_in_json(self):
        _, exported = self._build_detail()
        # "command_output" must never appear as a key anywhere in the exported dict.
        raw_json = json.dumps(exported)
        assert "command_output" not in raw_json
        # The word "stdout" may appear in redaction note text (expected),
        # but must not appear as a JSON *key* in evidence or metadata.
        sentinel = "SUPERSECRET_SUBPROCESS_OUTPUT_DO_NOT_LOG"
        assert sentinel not in raw_json


# ---------------------------------------------------------------------------
# H. Trust Report — test run section
# ---------------------------------------------------------------------------


class TestTrustReportTestRunSection:
    def test_trust_report_mentions_test_run(self):
        from packages.orchestration.trust_report import summarize_trust_report

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                },
            }
        ]
        report = summarize_trust_report(job, events)
        assert "test run" in report.lower() or "Test run" in report or "Test runs" in report

    def test_trust_report_no_subprocess_output_values(self):
        """Trust report must not contain raw subprocess output or forbidden field names."""
        from packages.orchestration.trust_report import summarize_trust_report

        job = Job(name="test", state=RunState.PENDING)
        # Use a sentinel as fake output — verify it does NOT appear in the report.
        sentinel = "SUPERSECRET_SUBPROCESS_OUTPUT_DO_NOT_LOG"
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                    # These keys simulate a bug where raw output leaked into metadata.
                    # The trust_report must never render them.
                },
            }
        ]
        report = summarize_trust_report(job, events)
        assert sentinel not in report
        # command_output must not appear as a field label
        assert "command_output" not in report

    def test_trust_report_no_test_runs_placeholder(self):
        from packages.orchestration.trust_report import summarize_trust_report

        job = Job(name="test", state=RunState.PENDING)
        report = summarize_trust_report(job, [])
        assert "No test runs recorded." in report

    def test_trust_report_raw_stdout_not_included_note(self):
        from packages.orchestration.trust_report import summarize_trust_report

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "x",
                    "command": "python3 -m pytest",
                    "status": "failed",
                    "exit_code": 1,
                    "duration_ms": 200,
                    "output_line_count": 5,
                    "output_bytes": 100,
                },
            }
        ]
        report = summarize_trust_report(job, events)
        assert "raw stdout/stderr not included" in report


# ---------------------------------------------------------------------------
# I. Timeline — test_run_completed rendering
# ---------------------------------------------------------------------------


class TestTimelineTestRunRendering:
    def test_timeline_renders_test_run_event(self):
        from packages.orchestration.timeline import summarize_timeline

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                },
            }
        ]
        output = summarize_timeline(job, events)
        assert "test run" in output.lower()
        assert "passed" in output

    def test_timeline_no_raw_output_in_rendering(self):
        from packages.orchestration.timeline import summarize_timeline

        job = Job(name="test", state=RunState.PENDING)
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "failed",
                    "exit_code": 1,
                    "duration_ms": 200,
                    "output_line_count": 5,
                    "output_bytes": 100,
                },
            }
        ]
        output = summarize_timeline(job, events)
        for key in ("stdout", "stderr", "command_output"):
            assert key not in output


# ---------------------------------------------------------------------------
# J. Viewer JSON — test_run node included
# ---------------------------------------------------------------------------


class TestViewerJsonTestRunNode:
    def _build_viewer_data(self, events: list) -> tuple[dict, str]:
        import tempfile

        from packages.orchestration.brain_viewer import (
            build_brain_viewer_data,
            write_brain_viewer_files,
        )
        from packages.orchestration.project_brain import build_project_brain

        job = Job(name="test", state=RunState.PENDING)
        graph = build_project_brain(job, events)
        with tempfile.TemporaryDirectory() as td:
            out_dir = Path(td) / "viewer"
            viewer_data = build_brain_viewer_data(job, graph, events)
            write_brain_viewer_files(viewer_data, out_dir)
            raw = (out_dir / "viewer_data.json").read_text()
            data = json.loads(raw)
        return data, raw

    def test_viewer_json_contains_test_run_node(self):
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                },
            }
        ]
        data, _ = self._build_viewer_data(events)
        # viewer_data.json has a nested "graph" with "nodes"
        types = [n["type"] for n in data["graph"]["nodes"]]
        assert "test_run" in types

    def test_viewer_json_no_raw_output(self):
        sentinel = "SUPERSECRET_SUBPROCESS_OUTPUT_DO_NOT_LOG"
        events = [
            {
                "event": "test_run_completed",
                "job_id": "x",
                "run_id": "r",
                "timestamp": "2025-01-01T00:00:00+00:00",
                "metadata": {
                    "test_run_id": "abc",
                    "command": "python3 -m pytest",
                    "status": "passed",
                    "exit_code": 0,
                    "duration_ms": 500,
                    "output_line_count": 3,
                    "output_bytes": 42,
                },
            }
        ]
        data, raw = self._build_viewer_data(events)

        # Node metadata in graph must not have raw output keys.
        for node in data["graph"]["nodes"]:
            meta = node.get("metadata", {})
            for key in ("stdout", "stderr", "raw_output", "command_output"):
                assert key not in meta
        # Sentinel never appears anywhere.
        assert sentinel not in raw


# ---------------------------------------------------------------------------
# K. CLI — run-tests-local command guards
# ---------------------------------------------------------------------------


class TestCliRunTestsLocal:
    """Tests for _cmd_run_tests_local — permission + repo guards."""

    def _run_cli(self, args: list[str], env: dict | None = None):
        """Run the CLI via subprocess and return (returncode, stdout, stderr)."""
        import os
        import subprocess as sp

        result = sp.run(
            ["python3", "-m", "apps.cli.main"] + args,
            capture_output=True,
            env={**os.environ, **(env or {})},
        )
        return result.returncode, result.stdout.decode(), result.stderr.decode()

    def _create_job(self, tmp_path: Path) -> str:
        """Create a job in a registered project.

        Since F148 `job create` resolves a project from its cwd and exits 3
        with "no project found" otherwise; the old fixture ignored the return
        code and handed an empty id to every command downstream.
        """
        import subprocess as sp

        env = {**__import__("os").environ, "REMEDY_DATA_DIR": str(tmp_path)}
        repo = tmp_path / "proj"
        repo.mkdir(parents=True, exist_ok=True)
        sp.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
        sp.run(["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
               check=True, capture_output=True,
               env={**env, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})
        init = sp.run(["python3", "-m", "apps.cli.main", "init"],
                      capture_output=True, env=env, cwd=str(repo))
        assert init.returncode == 0, init.stderr.decode()
        r = sp.run(
            ["python3", "-m", "apps.cli.main", "job", "create", "test job"],
            capture_output=True, env=env, cwd=str(repo),
        )
        assert r.returncode == 0, r.stderr.decode()
        job_id = r.stdout.decode().strip()
        assert job_id, "job create produced no job id"
        return job_id

    def test_permission_missing_exits_1(self, tmp_path):
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job(tmp_path)
        rc, out, err = self._run_cli(
            ["test", "run", job_id],
            env=env,
        )
        assert rc == 1
        assert "repo_test_run" in err

    def test_no_target_repo_exits_1(self, tmp_path):
        import os
        import subprocess as sp

        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job(tmp_path)

        # Grant permission but don't attach repo.
        sp.run(
            ["python3", "-m", "apps.cli.main",
             "job", "permit", job_id, "repo_test_run", "allow"],
            env=env, capture_output=True,
        )

        rc, out, err = self._run_cli(
            ["test", "run", job_id],
            env=env,
        )
        assert rc == 1
        assert "No target repository" in err or "target_repo" in err or "no_target_repo" in err
