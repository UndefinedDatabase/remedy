"""Tests: builder eval harness, prompt variants, scorecard, recommendations.

Fixture mode always runs in CI. Real Ollama opt-in via REMEDY_REAL_OLLAMA_EVAL=1.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.orchestration.builder_eval import (
    EvalCase,
    Scorecard,
    ScorecardEntry,
    aggregate_records,
    build_model_profile,
    build_scorecard,
    compare_profiles,
    export_eval_report_json,
    export_model_profile_json,
    export_scorecard_json,
    export_trial_result_json,
    recommend_prompt_changes,
    run_fixture_eval,
    run_single_eval,
    standard_eval_cases,
    standard_task_set,
    task_case_to_eval_case,
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
        from uuid import uuid4

        from packages.orchestration.builder_models import TaskExecutionContext
        from packages.providers.ollama_builder.provider import OllamaBuilder

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


# -- Step 393: Prompt profiles --

class TestPromptProfiles:
    """Prompt profiles must be genuinely different and contain safety rules."""

    def test_profiles_exist(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        assert "strict_minimal" in PROMPT_PROFILES
        assert "repair_aware" in PROMPT_PROFILES
        assert "context_rich" in PROMPT_PROFILES

    def test_profiles_are_different(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        texts = {p.system_text for p in PROMPT_PROFILES.values()}
        assert len(texts) == 3, "All three profiles must have different system text"

    def test_all_profiles_forbid_prose(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        for name, profile in PROMPT_PROFILES.items():
            assert "no prose" in profile.system_text.lower() or "no markdown" in profile.system_text.lower(), \
                f"Profile {name} must forbid prose"

    def test_all_profiles_forbid_shell(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        for name, profile in PROMPT_PROFILES.items():
            assert "shell" in profile.system_text.lower() or "rm" in profile.system_text.lower(), \
                f"Profile {name} must mention shell safety"

    def test_all_profiles_require_relative_paths(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        for name, profile in PROMPT_PROFILES.items():
            assert "relative" in profile.system_text.lower() or "no /" in profile.system_text, \
                f"Profile {name} must require relative paths"

    def test_profile_metadata_no_raw_prompt(self):
        from packages.providers.ollama_builder.provider import (
            PROMPT_PROFILES,
            get_prompt_profile_metadata,
        )
        for profile in PROMPT_PROFILES.values():
            meta = get_prompt_profile_metadata(profile)
            assert meta.prompt_hash != ""
            assert meta.prompt_length > 0
            assert profile.system_text not in str(vars(meta))

    def test_ollama_builder_accepts_profile(self):
        from packages.providers.ollama_builder.provider import OllamaBuilder
        builder = OllamaBuilder.__new__(OllamaBuilder)
        builder.__init__(prompt_profile="strict_minimal")
        assert builder.prompt_profile_name == "strict_minimal"
        assert builder.prompt_profile.name == "strict_minimal"

    def test_ollama_builder_default_profile(self):
        from packages.providers.ollama_builder.provider import OllamaBuilder
        builder = OllamaBuilder.__new__(OllamaBuilder)
        builder.__init__()
        assert builder.prompt_profile_name == "context_rich"


# -- Step 394: Small real-repo task set --

class TestTaskSet:
    """Task set must cover real coding situations."""

    def test_task_set_not_empty(self):
        tasks = standard_task_set()
        assert len(tasks) >= 7

    def test_task_set_has_all_outcome_types(self):
        tasks = standard_task_set()
        outcomes = {t.expected_outcome for t in tasks}
        assert "accepted" in outcomes
        assert "rejected" in outcomes
        assert "blocked" in outcomes

    def test_task_case_to_eval_case(self):
        tasks = standard_task_set()
        for task in tasks:
            case = task_case_to_eval_case(task)
            assert case.name == task.name
            assert case.category == task.expected_outcome

    def test_all_task_definitions_valid(self):
        tasks = standard_task_set()
        for task in tasks:
            assert task.name != ""
            assert task.user_task != ""
            assert task.expected_outcome in ("accepted", "rejected", "blocked")


# -- Step 395: Scorecard --

class TestScorecard:
    """Scorecard aggregates task results into quality metrics."""

    def _run_scorecard(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [
            run_single_eval("default", c.builder_output, fixture_name=c.name)
            for c in cases
        ]
        return build_scorecard(tasks, records)

    def test_scorecard_total_cases(self):
        sc = self._run_scorecard()
        assert sc.total_cases == len(standard_task_set())

    def test_scorecard_has_rates(self):
        sc = self._run_scorecard()
        assert 0.0 <= sc.usable_patch_rate <= 1.0
        assert 0.0 <= sc.safe_rejection_rate <= 1.0
        assert 0.0 <= sc.outcome_accuracy <= 1.0

    def test_rejected_cases_counted_correctly(self):
        sc = self._run_scorecard()
        rejected_entries = [e for e in sc.entries if e.expected_outcome == "rejected"]
        assert len(rejected_entries) >= 1
        for e in rejected_entries:
            assert e.safely_rejected is True
            assert e.outcome_correct is True

    def test_scorecard_entries_have_redaction(self):
        sc = self._run_scorecard()
        for e in sc.entries:
            assert e.redaction == "safe_metadata_only"

    def test_scorecard_export_no_raw(self):
        sc = self._run_scorecard()
        data = export_scorecard_json(sc)
        full = json.dumps(data)
        assert "safe_metadata_only" in full
        assert data["redaction"] == "safe_metadata_only"
        assert "needs_real_model_check" in data

    def test_scorecard_fixture_needs_real_check(self):
        sc = self._run_scorecard()
        assert sc.needs_real_model_check is True


# -- Step 396: Failure-pattern recommendations --

class TestRecommendations:
    """Recommendations based on scorecard patterns."""

    def test_prose_heavy_recommends_stricter_output(self):
        entries = [
            ScorecardEntry(case_name=f"case{i}", prompt_profile="default",
                           provider="fixture", model="mock",
                           parse_success=False, safely_rejected=False,
                           expected_outcome="accepted", outcome_correct=False,
                           stop_reason="provider_output_prose_only",
                           estimated_tokens=0, latency_ms=0,
                           output_hash="", output_length=0)
            for i in range(3)
        ]
        sc = Scorecard(entries=entries, total_cases=3)
        recs = recommend_prompt_changes(sc)
        assert any(r.pattern == "frequent_prose" for r in recs)

    def test_clean_scorecard_no_unnecessary_recs(self):
        entries = [
            ScorecardEntry(case_name="ok", prompt_profile="default",
                           provider="fixture", model="mock",
                           parse_success=True, safely_rejected=False,
                           expected_outcome="accepted", outcome_correct=True,
                           stop_reason="", estimated_tokens=10, latency_ms=1,
                           output_hash="abc", output_length=50)
        ]
        sc = Scorecard(entries=entries, total_cases=1, outcome_accuracy=1.0)
        recs = recommend_prompt_changes(sc)
        assert all(r.pattern == "no_issues_detected" for r in recs)

    def test_scorecard_export_includes_recommendations(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [
            run_single_eval("default", c.builder_output, fixture_name=c.name)
            for c in cases
        ]
        sc = build_scorecard(tasks, records)
        data = export_scorecard_json(sc)
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)


# -- Step 397: Model profile recommendation --

class TestModelProfile:
    """Model profile from scorecard data."""

    def test_fixture_profile_low_confidence(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [
            run_single_eval("default", c.builder_output, fixture_name=c.name)
            for c in cases
        ]
        sc = build_scorecard(tasks, records)
        profile = build_model_profile(sc)
        assert profile.confidence == "low"
        assert "fixture" in profile.recommendation.lower() or "real" in profile.recommendation.lower()

    def test_empty_data_profile(self):
        sc = Scorecard()
        profile = build_model_profile(sc)
        assert profile.sample_count == 0
        assert profile.confidence == "low"
        assert "no data" in profile.recommendation.lower()

    def test_profile_export_safe(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [
            run_single_eval("default", c.builder_output, fixture_name=c.name)
            for c in cases
        ]
        sc = build_scorecard(tasks, records)
        profile = build_model_profile(sc)
        data = export_model_profile_json(profile)
        assert data["redaction"] == "safe_metadata_only"
        assert "provider" in data
        assert "confidence" in data

    def test_two_profiles_comparable(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [
            run_single_eval("default", c.builder_output, fixture_name=c.name)
            for c in cases
        ]
        sc1 = build_scorecard(tasks, records, prompt_profile="strict_minimal")
        sc2 = build_scorecard(tasks, records, prompt_profile="repair_aware")
        p1 = build_model_profile(sc1)
        p2 = build_model_profile(sc2)
        assert p1.prompt_profile != p2.prompt_profile


# -- Step 427: Task set v2 --

class TestTaskSetV2:
    """Extended task set with 8 cases."""

    def test_task_set_has_eight_cases(self):
        tasks = standard_task_set()
        assert len(tasks) == 8

    def test_multi_file_case_exists(self):
        tasks = standard_task_set()
        multi = [t for t in tasks if t.name == "multi_file_change"]
        assert len(multi) == 1
        assert multi[0].patch_json is not None
        assert len(multi[0].patch_json["file_ops"]) == 2

    def test_all_expected_outcomes_present(self):
        tasks = standard_task_set()
        outcomes = {t.expected_outcome for t in tasks}
        assert outcomes == {"accepted", "rejected", "blocked"}

    def test_no_op_case_has_no_patch(self):
        tasks = standard_task_set()
        noop = [t for t in tasks if t.name == "no_change_needed"]
        assert len(noop) == 1
        assert noop[0].patch_json is None
        assert noop[0].expected_outcome == "blocked"


# -- Step 428: Instruction profiles verified --

class TestInstructionProfiles:
    """Three instruction profiles are genuinely different."""

    def test_three_profiles_exist(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        assert len(PROMPT_PROFILES) >= 3

    def test_profiles_have_different_text(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        texts = {p.system_text for p in PROMPT_PROFILES.values()}
        assert len(texts) == len(PROMPT_PROFILES)

    def test_each_profile_forbids_prose(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        for name, p in PROMPT_PROFILES.items():
            assert "no prose" in p.system_text.lower() or "no markdown" in p.system_text.lower(), \
                f"{name} must forbid prose"

    def test_each_profile_forbids_shell(self):
        from packages.providers.ollama_builder.provider import PROMPT_PROFILES
        for name, p in PROMPT_PROFILES.items():
            assert "shell" in p.system_text.lower() or "rm" in p.system_text.lower(), \
                f"{name} must mention shell safety"

    def test_metadata_no_raw_prompt(self):
        from packages.providers.ollama_builder.provider import (
            PROMPT_PROFILES,
            get_prompt_profile_metadata,
        )
        for p in PROMPT_PROFILES.values():
            meta = get_prompt_profile_metadata(p)
            assert p.system_text not in str(vars(meta))
            assert meta.prompt_hash != ""
            assert meta.prompt_length > 0


# -- Step 429: Scorecard v2 --

class TestScorecardV2:
    """Scorecard handles 8 tasks with expected outcomes."""

    def _run(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        records = [run_single_eval("default", c.builder_output, fixture_name=c.name) for c in cases]
        return build_scorecard(tasks, records)

    def test_scorecard_eight_entries(self):
        sc = self._run()
        assert sc.total_cases == 8

    def test_expected_rejection_counted_correct(self):
        sc = self._run()
        unsafe = [e for e in sc.entries if e.expected_outcome == "rejected"]
        for e in unsafe:
            assert e.safely_rejected is True
            assert e.outcome_correct is True

    def test_noop_counted_correct(self):
        sc = self._run()
        noop = [e for e in sc.entries if e.expected_outcome == "blocked"]
        for e in noop:
            assert e.parse_success is False
            assert e.outcome_correct is True

    def test_multi_file_counted(self):
        sc = self._run()
        multi = [e for e in sc.entries if e.case_name == "multi_file_change"]
        assert len(multi) == 1
        assert multi[0].parse_success is True

    def test_export_has_recommendations(self):
        sc = self._run()
        data = export_scorecard_json(sc)
        assert "recommendations" in data


# -- Step 430: Failure advice --

class TestFailureAdvice:
    """Plain failure advice from scorecard patterns."""

    def test_prose_heavy_advice(self):
        entries = [
            ScorecardEntry(case_name=f"c{i}", prompt_profile="d", provider="f", model="m",
                           parse_success=False, safely_rejected=False, expected_outcome="accepted",
                           outcome_correct=False, stop_reason="provider_output_prose_only",
                           estimated_tokens=0, latency_ms=0, output_hash="", output_length=0)
            for i in range(3)
        ]
        sc = Scorecard(entries=entries, total_cases=3)
        recs = recommend_prompt_changes(sc)
        assert any("prose" in r.pattern or "output" in r.suggestion.lower() for r in recs)

    def test_malformed_heavy_advice(self):
        entries = [
            ScorecardEntry(case_name=f"c{i}", prompt_profile="d", provider="f", model="m",
                           parse_success=False, safely_rejected=False, expected_outcome="accepted",
                           outcome_correct=False, stop_reason="structured_patch_parse_failed",
                           estimated_tokens=0, latency_ms=0, output_hash="", output_length=0)
            for i in range(3)
        ]
        sc = Scorecard(entries=entries, total_cases=3)
        recs = recommend_prompt_changes(sc)
        assert any("malformed" in r.pattern or "format" in r.suggestion.lower() for r in recs)

    def test_clean_scorecard_no_unnecessary_advice(self):
        entries = [
            ScorecardEntry(case_name="ok", prompt_profile="d", provider="f", model="m",
                           parse_success=True, safely_rejected=False, expected_outcome="accepted",
                           outcome_correct=True, stop_reason="", estimated_tokens=10,
                           latency_ms=1, output_hash="x", output_length=50)
        ]
        sc = Scorecard(entries=entries, total_cases=1, outcome_accuracy=1.0)
        recs = recommend_prompt_changes(sc)
        assert all(r.pattern == "no_issues_detected" for r in recs)


# -- Step 431: Prompt trial --

class TestPromptTrial:
    """Controlled prompt improvement trial."""

    def _run_default(self):
        tasks = standard_task_set()
        cases = [task_case_to_eval_case(t) for t in tasks]
        return tasks, [run_single_eval("default", c.builder_output, fixture_name=c.name) for c in cases]

    def test_compare_same_profile(self):
        tasks, records = self._run_default()
        result = compare_profiles(tasks, records, records, before_profile="v1", after_profile="v1")
        assert "No clear improvement" in result.improvement

    def test_compare_different_profiles(self):
        tasks, records = self._run_default()
        result = compare_profiles(tasks, records, records, before_profile="v1", after_profile="v2")
        assert result.total_tasks == len(tasks)
        assert result.redaction == "safe_metadata_only"

    def test_trial_export_safe(self):
        tasks, records = self._run_default()
        result = compare_profiles(tasks, records, records)
        data = export_trial_result_json(result)
        assert data["redaction"] == "safe_metadata_only"
        assert "before_accuracy" in data
        assert "after_accuracy" in data

    def test_trial_can_say_no_improvement(self):
        tasks, records = self._run_default()
        result = compare_profiles(tasks, records, records)
        assert "no change" in result.recommendation.lower() or "no clear" in result.improvement.lower()


# -- Step 433: CLI report --

class TestCLIReport:
    """CLI eval script works for example mode."""

    def test_example_flag_works(self):
        import subprocess
        result = subprocess.run(
            ["scripts/remedy_builder_eval.sh", "--example"],
            capture_output=True, text=True, timeout=15,
            cwd=str(Path(__file__).resolve().parents[2]),
        )
        assert result.returncode == 0
        assert "example" in result.stdout.lower() or "Provider" in result.stdout

    def test_ollama_without_env_fails(self):
        import os
        import subprocess
        env = {k: v for k, v in os.environ.items() if k != "REMEDY_REAL_OLLAMA_EVAL"}
        result = subprocess.run(
            ["scripts/remedy_builder_eval.sh", "--ollama"],
            capture_output=True, text=True, timeout=15,
            cwd=str(Path(__file__).resolve().parents[2]),
            env=env,
        )
        assert result.returncode != 0
        assert "REMEDY_REAL_OLLAMA_EVAL" in result.stderr

    def test_example_json_valid(self):
        import subprocess
        result = subprocess.run(
            ["scripts/remedy_builder_eval.sh", "--example", "--json"],
            capture_output=True, text=True, timeout=15,
            cwd=str(Path(__file__).resolve().parents[2]),
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["redaction"] == "safe_metadata_only"
        assert data["provider"] == "fixture"

    def test_example_json_has_model_profile(self):
        import subprocess
        result = subprocess.run(
            ["scripts/remedy_builder_eval.sh", "--example", "--json"],
            capture_output=True, text=True, timeout=15,
            cwd=str(Path(__file__).resolve().parents[2]),
        )
        data = json.loads(result.stdout)
        assert "model_profile" in data
        assert data["model_profile"]["confidence"] == "low"
