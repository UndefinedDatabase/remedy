"""Tests for packages.orchestration.capability_routes — F157 T003, first routed consumer
(DECISION F157 D3): the stream route inside `create_role_provider`, its evidence file and the
reader over it.
"""

from __future__ import annotations

import json

from packages.contracts.adapter_contract import AdapterCapabilities
from packages.orchestration import worker_adapter_slot
from packages.orchestration.capability_routes import (
    CAPABILITY_DECISIONS_FILENAME,
    read_capability_degradations,
    routed_stream_evidence,
)
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


class TestRoutedStreamEvidence:
    def test_the_registry_adapter_is_native_and_writes_one_native_line(self, tmp_path):
        result = routed_stream_evidence("builder", "m", True, str(tmp_path))
        assert result is True
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["decisions"] == [
            {"feature_key": "stream_evidence_capture", "mode": "native", "strategy": None, "missing": []},
        ]

    def test_requested_false_answers_false_and_writes_nothing(self, tmp_path):
        result = routed_stream_evidence("builder", "m", False, str(tmp_path))
        assert result is False
        assert not (tmp_path / CAPABILITY_DECISIONS_FILENAME).exists()

    def test_a_reduced_adapter_degrades_and_writes_the_degraded_line(self, monkeypatch, tmp_path):
        monkeypatch.setitem(worker_adapter_slot._INSTALLED_WORKER_ADAPTERS, "claude-cli",
                             _ReducedClaudeCliAdapter)
        result = routed_stream_evidence("builder", "m", True, str(tmp_path))
        assert result is False
        lines = (tmp_path / CAPABILITY_DECISIONS_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["decisions"] == [
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]

    def test_evidence_dir_none_answers_the_same_booleans_and_writes_nothing(self):
        assert routed_stream_evidence("builder", "m", True, None) is True
        assert routed_stream_evidence("builder", "m", False, None) is False


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
