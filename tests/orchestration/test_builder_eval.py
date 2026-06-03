"""Tests: builder eval harness, prompt variants, small-repo eval set.

Fixture mode always runs in CI. Real Ollama mode opt-in via REMEDY_REAL_OLLAMA_EVAL=1.
"""

from __future__ import annotations

import json
import os

import pytest

from packages.orchestration.builder_eval import (
    EvalCase,
    EvalMetrics,
    EvalRecord,
    EvalReport,
    aggregate_records,
    export_eval_report_json,
    run_fixture_eval,
    run_single_eval,
    standard_eval_cases,
)
from packages.orchestration.builder_models import BuilderOutput


def _make_output(patch_text: str | None = None) -> BuilderOutput:
    return BuilderOutput(
        summary="Test",
        proposed_changes=["Change"],
        structured_patch_text=patch_text,
    )


STANDARD_CASES: list[EvalCase] = standard_eval_cases()


class TestEvalRecord:
    """Single eval record creation and safety."""

    def test_valid_patch_record(self):
        record = run_single_eval("default", STANDARD_CASES[0].builder_output, fixture_name="valid")
        assert record.parse_success is True
        assert record.eval_id != ""
        assert record.redaction == "safe_metadata_only"
        assert record.output_hash != ""

    def test_prose_record(self):
        record = run_single_eval("default", STANDARD_CASES[2].builder_output, fixture_name="prose")
        assert record.parse_success is False
        assert record.parse_error_kind == "prose_only"
        assert record.stop_reason == "provider_output_prose_only"

    def test_unsafe_path_record(self):
        record = run_single_eval("default", STANDARD_CASES[5].builder_output, fixture_name="unsafe")
        assert record.parse_success is False
        assert record.unsafe_rejected is True

    def test_shell_command_record(self):
        record = run_single_eval("default", STANDARD_CASES[6].builder_output, fixture_name="shell")
        assert record.parse_success is False
        assert record.unsafe_rejected is True
        assert record.parse_error_kind == "unsafe_shell_command"

    def test_no_raw_output_in_record(self):
        text = json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "SECRET=abc123\n"}]})
        record = run_single_eval("default", _make_output(text), fixture_name="secret")
        record_str = str(vars(record))
        assert "SECRET=abc123" not in record_str
        assert "abc123" not in record_str


class TestAggregateMetrics:
    """Metrics aggregation from eval records."""

    def test_empty_records(self):
        metrics = aggregate_records([])
        assert metrics.total_cases == 0
        assert metrics.parse_success_rate == 0.0

    def test_mixed_records(self):
        records = [
            run_single_eval("v1", case.builder_output, fixture_name=case.name)
            for case in STANDARD_CASES
        ]
        metrics = aggregate_records(records)
        assert metrics.total_cases == len(STANDARD_CASES)
        assert metrics.parse_success_count > 0
        assert metrics.parse_success_count < metrics.total_cases
        assert 0.0 < metrics.parse_success_rate < 1.0
        assert metrics.unsafe_rejection_count >= 2
        assert len(metrics.failure_counts_by_error_kind) > 0

    def test_failure_taxonomy_preserved(self):
        records = [
            run_single_eval("v1", case.builder_output, fixture_name=case.name)
            for case in STANDARD_CASES
        ]
        metrics = aggregate_records(records)
        assert "prose_only" in metrics.failure_counts_by_error_kind
        assert "unsafe_shell_command" in metrics.failure_counts_by_error_kind

    def test_stop_reason_counts(self):
        records = [
            run_single_eval("v1", case.builder_output, fixture_name=case.name)
            for case in STANDARD_CASES
        ]
        metrics = aggregate_records(records)
        assert len(metrics.stop_reason_counts) > 0


class TestFixtureEval:
    """Full fixture evaluation run."""

    def test_default_variant(self):
        report = run_fixture_eval("default", STANDARD_CASES)
        assert report.version == 1
        assert report.prompt_variant == "default"
        assert report.redaction == "safe_metadata_only"
        assert len(report.records) == len(STANDARD_CASES)
        assert report.metrics.total_cases == len(STANDARD_CASES)

    def test_two_variants_comparable(self):
        report_v1 = run_fixture_eval("strict_schema", STANDARD_CASES)
        report_v2 = run_fixture_eval("repair_aware", STANDARD_CASES)
        assert report_v1.metrics.total_cases == report_v2.metrics.total_cases
        assert report_v1.prompt_variant != report_v2.prompt_variant

    def test_recommendation_present(self):
        report = run_fixture_eval("default", STANDARD_CASES)
        assert report.recommendation != ""


class TestExportSafety:
    """Exported JSON must contain no raw provider output."""

    def test_export_shape(self):
        report = run_fixture_eval("default", STANDARD_CASES)
        data = export_eval_report_json(report)
        assert data["version"] == 1
        assert "metrics" in data
        assert "records" in data
        assert data["redaction"] == "safe_metadata_only"
        assert data["metrics"]["total_cases"] == len(STANDARD_CASES)

    def test_export_no_raw_content(self):
        cases = [
            EvalCase(
                name="secret_content",
                category="success",
                builder_output=_make_output(
                    json.dumps({"file_ops": [{"path": "a.py", "action": "create", "content": "API_KEY=sk-12345\n"}]})
                ),
            ),
        ]
        report = run_fixture_eval("default", cases)
        data = export_eval_report_json(report)
        full_json = json.dumps(data)
        assert "API_KEY" not in full_json
        assert "sk-12345" not in full_json

    def test_export_records_have_redaction(self):
        report = run_fixture_eval("default", STANDARD_CASES[:2])
        data = export_eval_report_json(report)
        for record in data["records"]:
            assert record["redaction"] == "safe_metadata_only"


class TestSmallRepoEvalFixtures:
    """Small-repo fixture scenarios produce valid eval records."""

    def test_missing_function_fixture(self):
        from tests.orchestration.small_repo_fixtures import fixture_patch_missing_function

        patch = fixture_patch_missing_function()
        output = BuilderOutput(
            summary="Fix missing function",
            proposed_changes=["Add hello()"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        record = run_single_eval("default", output, fixture_name="missing_function")
        assert record.parse_success is True
        assert record.target_path_count == 1

    def test_wrong_return_fixture(self):
        from tests.orchestration.small_repo_fixtures import fixture_patch_wrong_return

        patch = fixture_patch_wrong_return()
        output = BuilderOutput(
            summary="Fix wrong return",
            proposed_changes=["Fix return value"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        record = run_single_eval("default", output, fixture_name="wrong_return")
        assert record.parse_success is True

    def test_repair_cycle_fixtures(self):
        from tests.orchestration.small_repo_fixtures import (
            fixture_patch_repair_cycle1,
            fixture_patch_repair_cycle2,
        )

        for name, patch_fn in [
            ("repair_cycle1", fixture_patch_repair_cycle1),
            ("repair_cycle2", fixture_patch_repair_cycle2),
        ]:
            patch = patch_fn()
            output = BuilderOutput(
                summary="Repair",
                proposed_changes=["Fix"],
                structured_patch_text=json.dumps(patch),
                structured_patch_format="json",
            )
            record = run_single_eval("default", output, fixture_name=name)
            assert record.parse_success is True

    def test_unsafe_path_fixture(self):
        output = BuilderOutput(
            summary="Hack",
            proposed_changes=["Modify passwd"],
            structured_patch_text=json.dumps({
                "file_ops": [{"path": "../../../etc/passwd", "action": "modify", "content": "x\n"}]
            }),
        )
        record = run_single_eval("default", output, fixture_name="unsafe_path")
        assert record.parse_success is False
        assert record.unsafe_rejected is True


@pytest.mark.skipif(
    not os.environ.get("REMEDY_REAL_OLLAMA_EVAL"),
    reason="Set REMEDY_REAL_OLLAMA_EVAL=1 for real Ollama evaluation",
)
class TestRealOllamaEval:
    """Real Ollama eval — opt-in only, not required for CI."""

    def test_real_ollama_eval_produces_record(self):
        from packages.providers.ollama_builder.provider import OllamaBuilder
        from packages.orchestration.builder_models import TaskExecutionContext
        from uuid import uuid4

        ctx = TaskExecutionContext(
            job_id=uuid4(),
            task_id=uuid4(),
            job_prompt="Add hello function",
            task_type="code_change",
            task_description="Add def hello(): return 'hello' to app.py",
        )
        try:
            builder = OllamaBuilder()
            output = builder.build(ctx)
        except (ImportError, Exception):
            pytest.skip("Ollama unavailable")
            return

        record = run_single_eval(
            "default", output,
            fixture_name="real_ollama_hello",
            provider="ollama",
            model=builder.model,
        )
        assert record.eval_id != ""
        assert record.provider == "ollama"
        assert record.redaction == "safe_metadata_only"
        record_str = str(vars(record))
        assert "def hello" not in record_str
