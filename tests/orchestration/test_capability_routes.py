"""Tests for packages.orchestration.capability_routes — F157 T003, the claude-cli build's routed
consumers (DECISIONS F157 D3 and D4): the stream, reviewer-schema and parked-resume routes inside
`create_role_provider`, their one evidence file and the reader over it.
"""

from __future__ import annotations

import json

from packages.contracts.adapter_contract import AdapterCapabilities
from packages.orchestration import worker_adapter_slot
from packages.orchestration.capability_routes import (
    CAPABILITY_DECISIONS_FILENAME,
    read_capability_degradations,
    routed_claude_cli_build,
    routed_parked_resume,
    routed_reviewer_schema,
)
from packages.orchestration.pingpong_loop import resume_declined_reasons
from packages.orchestration.pingpong_provider import ReviewerOutput
from packages.orchestration.role_provider_factory import create_role_provider


class _ReducedClaudeCliAdapter:
    """A small claude-cli adapter, taking `**settings`, whose capabilities declare `streaming=False`
    and every other flag true (DECISION F157 D3's reduced-capability fixture)."""

    adapter_id = "claude-cli"

    def __init__(self, **settings):
        pass

    def capabilities(self, model: str) -> AdapterCapabilities:
        return AdapterCapabilities(
            vision=True, json_schema=True, session_resume=True,
            streaming=False, tool_use=True, max_context_tokens=1,
        )


class _ResumeAndSchemaReducedAdapter:
    """A small claude-cli adapter, taking `**settings`, whose capabilities declare
    `session_resume=False` and `json_schema=False`, with streaming and every other flag true
    (DECISION F157 D4's reduced-capability fixture for the reviewer-schema and parked-resume
    routes)."""

    adapter_id = "claude-cli"

    def __init__(self, **settings):
        pass

    def capabilities(self, model: str) -> AdapterCapabilities:
        return AdapterCapabilities(
            vision=True, json_schema=False, session_resume=False,
            streaming=True, tool_use=True, max_context_tokens=1,
        )


class TestRoutedClaudeCliBuild:
    def test_an_all_native_build_writes_no_file(self, tmp_path):
        result = routed_claude_cli_build("builder", "m", True, str(tmp_path))
        assert result is True
        assert not (tmp_path / CAPABILITY_DECISIONS_FILENAME).exists()

    def test_requested_false_answers_false_and_writes_nothing(self, tmp_path):
        result = routed_claude_cli_build("builder", "m", False, str(tmp_path))
        assert result is False
        assert not (tmp_path / CAPABILITY_DECISIONS_FILENAME).exists()

    def test_a_reduced_streaming_adapter_degrades_and_writes_the_full_decision_line(
        self, monkeypatch, tmp_path,
    ):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ReducedClaudeCliAdapter)
        result = routed_claude_cli_build("builder", "m", True, str(tmp_path))
        assert result is False
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["role"] == "builder"
        assert record["provider"] == "claude-cli"
        assert record["model"] == "m"
        assert record["decisions"] == [
            {"feature_key": "parked_session_resume", "mode": "native", "strategy": None, "missing": []},
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]

    def test_a_reviewer_build_with_the_resume_and_schema_reduced_adapter_writes_both_degraded(
        self, monkeypatch, tmp_path,
    ):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        result = routed_claude_cli_build("reviewer", "m", False, str(tmp_path))
        assert result is False
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["role"] == "reviewer"
        assert record["provider"] == "claude-cli"
        assert record["model"] == "m"
        assert record["decisions"] == [
            {"feature_key": "parked_session_resume", "mode": "degraded",
             "strategy": "full_context_resend", "missing": ["session_resume"]},
            {"feature_key": "reviewer_schema_gate", "mode": "degraded",
             "strategy": "schema_in_prompt", "missing": ["json_schema"]},
        ]

    def test_a_builder_build_carries_no_reviewer_schema_gate_decision(self, monkeypatch, tmp_path):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        routed_claude_cli_build("builder", "m", False, str(tmp_path))
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        feature_keys = [decision["feature_key"] for decision in record["decisions"]]
        assert feature_keys == ["parked_session_resume"]

    def test_two_degraded_builds_into_one_directory_leave_two_lines(self, monkeypatch, tmp_path):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        routed_claude_cli_build("reviewer", "m1", False, str(tmp_path))
        routed_claude_cli_build("reviewer", "m2", False, str(tmp_path))
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2

    def test_evidence_dir_none_answers_the_same_booleans_and_writes_nothing(self):
        assert routed_claude_cli_build("builder", "m", True, None) is True
        assert routed_claude_cli_build("builder", "m", False, None) is False


class TestReadCapabilityDegradations:
    def test_an_absent_file_answers_empty(self, tmp_path):
        assert read_capability_degradations(str(tmp_path)) == []

    def test_a_native_line_a_twice_degraded_line_and_a_non_json_line_give_one_entry(self, tmp_path):
        native = json.dumps({"role": "builder", "provider": "claude-cli", "model": "m", "decisions": [
            {"feature_key": "stream_evidence_capture", "mode": "native", "strategy": None, "missing": []},
        ]})
        degraded = json.dumps({"role": "builder", "provider": "claude-cli", "model": "m", "decisions": [
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]})
        path = tmp_path / CAPABILITY_DECISIONS_FILENAME
        path.write_text(f"{native}\n{degraded}\n{degraded}\nnot json\n", encoding="utf-8")
        assert read_capability_degradations(str(tmp_path)) == [
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]

    def test_a_line_holding_a_json_array_is_skipped(self, tmp_path):
        path = tmp_path / CAPABILITY_DECISIONS_FILENAME
        path.write_text("[1, 2, 3]\n", encoding="utf-8")
        assert read_capability_degradations(str(tmp_path)) == []


class TestCreateRoleProviderRoutesTheStreamSetting:
    def test_the_registry_adapter_reads_true_and_the_reduced_one_reads_false(self, monkeypatch, tmp_path):
        native_provider = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="m", stream_evidence=True, stream_evidence_dir=str(tmp_path / "evidence1"),
            with_failover=False,
        )
        assert native_provider.stream_evidence is True

        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ReducedClaudeCliAdapter)
        reduced_dir = tmp_path / "evidence2"
        reduced_provider = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="m", stream_evidence=True, stream_evidence_dir=str(reduced_dir),
            with_failover=False,
        )
        assert reduced_provider.stream_evidence is False
        lines = (reduced_dir / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["decisions"] == [
            {"feature_key": "parked_session_resume", "mode": "native", "strategy": None, "missing": []},
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]

    def test_stream_evidence_false_writes_no_file(self, tmp_path):
        evidence_dir = tmp_path / "evidence3"
        provider = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="m", stream_evidence=False, stream_evidence_dir=str(evidence_dir),
            with_failover=False,
        )
        assert provider.stream_evidence is False
        assert not evidence_dir.exists()


class TestRoutedReviewerSchema:
    def test_false_with_the_reduced_adapter(self, monkeypatch):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        assert routed_reviewer_schema("m") is False

    def test_false_under_the_freetext_env_with_the_registrys_adapter(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        assert routed_reviewer_schema("m") is False

    def test_true_otherwise(self):
        assert routed_reviewer_schema("m") is True


class TestRoutedParkedResume:
    def test_true_with_the_registrys_adapter(self):
        assert routed_parked_resume("m") is True

    def test_false_with_the_reduced_one(self, monkeypatch):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        assert routed_parked_resume("m") is False


class TestClaudeCliProviderRoutesResumeAndSchema:
    """`ClaudeCliProvider`, built through `create_role_provider`, reads both routes per call
    (DECISION F157 D4 (2))."""

    def _reviewer(self, tmp_path):
        return create_role_provider(
            "claude-cli", role="reviewer", staging_dir=str(tmp_path / "staging"),
            model="m", with_failover=False,
        )

    def test_supports_resume_true_with_the_registrys_adapter(self, tmp_path):
        assert self._reviewer(tmp_path).supports_resume is True

    def test_supports_resume_false_with_the_reduced_adapter(self, monkeypatch, tmp_path):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        assert self._reviewer(tmp_path).supports_resume is False

    def test_resume_declined_reasons_names_the_reviewer_for_the_reduced_adapter(
        self, monkeypatch, tmp_path,
    ):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        reviewer = self._reviewer(tmp_path)
        declined = resume_declined_reasons({"reviewer": "sess-1"}, builder=None, reviewer=reviewer)
        assert "reviewer" in declined

    def test_review_prepares_a_cli_native_input_with_the_registrys_adapter(self, tmp_path):
        reviewer = self._reviewer(tmp_path)
        reviewer._review_impl = lambda *args, **kwargs: ReviewerOutput()
        out = reviewer.review("prompt text")
        assert out.prepared_input.mode == "cli-native"

    def test_review_prepares_a_cli_legacy_input_with_the_reduced_adapter(self, monkeypatch, tmp_path):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ResumeAndSchemaReducedAdapter)
        reviewer = self._reviewer(tmp_path)
        reviewer._review_impl = lambda *args, **kwargs: ReviewerOutput()
        out = reviewer.review("prompt text")
        assert out.prepared_input.mode == "cli-legacy"
