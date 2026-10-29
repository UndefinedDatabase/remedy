"""F321 — low findings never block; a medium blocked verdict is repaired; the config names the rounds."""
from __future__ import annotations

import types
from pathlib import Path

import pytest

from packages.orchestration.execution_config import configured_repair_rounds, resolve_job_execution_config
from packages.orchestration.pingpong_job import validate_job_task_result
from packages.orchestration.pingpong_loop import (
    REASON_ONLY_LOW_FINDINGS,
    make_repair_decision,
    run_pingpong,
)
from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding
from packages.orchestration.pingpong_provider_fake import FakeProvider


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _decide(verdict: str, severities: tuple[str, ...], *, used: int = 0, allowed: int = 2):
    return make_repair_decision(
        round_num=used + 1, reviewer_verdict=verdict, tests_passed=None,
        finding_count=len(severities), repair_rounds_allowed=allowed, repair_rounds_used=used,
        is_repair=used > 0, coherence_error=None, finding_severities=severities)


def test_blocked_with_one_low_finding_passes() -> None:
    # Job 4b90ef2ed0274960 of 2026-10-28: blocked on one low finding, one repair round left.
    decision = _decide("blocked", ("low",), used=1)
    assert decision.repair_decision == "pass_no_repair"
    assert decision.reason == REASON_ONLY_LOW_FINDINGS
    assert _decide("needs_repair", ("low", "LOW")).repair_decision == "pass_no_repair"


def test_blocked_with_a_medium_finding_is_repaired_while_rounds_remain() -> None:
    # Job 92af245f83d246d3: blocked on one medium finding.
    assert _decide("blocked", ("medium", "low"), used=1).repair_decision == "repair"
    assert _decide("blocked", ("medium",), used=2).repair_decision == "stop_exhausted"


def test_high_and_blocker_findings_still_stop() -> None:
    assert _decide("blocked", ("high",)).repair_decision == "stop_blocked"
    assert _decide("blocked", ("blocker", "low")).repair_decision == "stop_blocked"
    assert _decide("blocked", ()).repair_decision == "stop_blocked"


def test_failed_tests_still_dominate_low_findings() -> None:
    decision = make_repair_decision(
        round_num=1, reviewer_verdict="blocked", tests_passed=False, finding_count=1,
        repair_rounds_allowed=2, repair_rounds_used=0, is_repair=False, coherence_error=None,
        finding_severities=("low",))
    assert decision.repair_decision == "repair"


class _LowBlockingReviewer(FakeProvider):
    """A reviewer that blocks with one low finding, as the reviewers of 2026-10-28 did."""

    def _review_impl(self, prompt, *, timeout_sec=120, max_output_chars=50000):
        self._review_count += 1
        return ReviewerOutput(
            verdict="blocked", summary="Still no test run.", provider="fake",
            findings=[ReviewFinding(id="R-0001", severity="low", summary="tests still have not been run")])


def test_a_run_blocked_on_low_findings_ends_passed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    result = run_pingpong("Fix README", str(repo), builder_provider=FakeProvider(pass_on_round=1),
                          reviewer_provider=_LowBlockingReviewer(), max_rounds=3, repair_rounds=2)
    assert result.final_status == "staged_review_passed"
    _ok, reasons = validate_job_task_result(result)
    # The run's staging is cleaned up after it; only the review's reading is this test's question.
    assert not [reason for reason in reasons if reason.startswith("reviewer_verdict")], reasons


def test_task_result_with_low_findings_only_is_valid(tmp_path: Path) -> None:
    def result(severity: str):
        review = ReviewerOutput(verdict="blocked", summary="s", findings=[
            ReviewFinding(id="R-1", severity=severity, summary="x")])
        return types.SimpleNamespace(
            final_status="staged_review_passed", staged_files=["a.py"], target_mutated=False,
            rounds=[types.SimpleNamespace(test_passed=None, reviewer_output=review)],
            staging_path=str(tmp_path))
    assert validate_job_task_result(result("low")) == (True, [])
    assert validate_job_task_result(result("medium"))[1] == ["reviewer_verdict=blocked"]


class _Config:
    def __init__(self, value, source):
        self.value, self.source = value, source

    def get(self, key):
        # Every other key reads as unset, so its own default applies.
        return self.value if key == "cycles.repair_rounds" else None

    def get_source(self, key):
        return types.SimpleNamespace(value=self.source if key == "cycles.repair_rounds" else "default")


def test_config_key_names_a_jobs_repair_rounds() -> None:
    assert configured_repair_rounds(_Config(3, "user")) == (3, "config")
    assert configured_repair_rounds(_Config(2, "default")) == (2, "default")
    assert configured_repair_rounds(_Config(99, "env")) == (10, "config")
    resolved = resolve_job_execution_config(None, config=_Config(1, "project"))
    assert (resolved.repair_rounds_allowed, resolved.repair_rounds_source) == (1, "config")
    explicit = resolve_job_execution_config(None, repair_rounds=0, repair_rounds_source="http",
                                            config=_Config(3, "user"))
    assert (explicit.repair_rounds_allowed, explicit.repair_rounds_source) == (0, "http")


def test_a_planned_job_records_its_rounds(tmp_path: Path) -> None:
    from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, save_job_plan

    repo = tmp_path / "repo"
    repo.mkdir()
    job = parse_job_file("# Job: Demo\n\n## Task 1\nFix README.\n\nAcceptance:\n- fixed\n", str(repo))
    job.repair_rounds_allowed, job.repair_rounds_source = 0, ""
    save_job_plan(job)
    loaded = load_job_plan(str(job.job_id))
    assert loaded is not None
    assert (loaded.repair_rounds_allowed, loaded.repair_rounds_source) in ((2, "default"), (2, "config"))
