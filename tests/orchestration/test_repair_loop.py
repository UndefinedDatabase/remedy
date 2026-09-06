"""Repair loop tests — Steps 4738-4772.

Tests the Builder <> Reviewer repair cycle with smart governance.
No real Claude calls. No network. No target repo mutation.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import (
    PingPongRound,
    _build_builder_prompt,
    _build_reviewer_prompt,
    build_finding_status_map,
    export_pingpong_json,
    make_repair_decision,
    resolve_repair_rounds,
    run_final_adjudication,
    run_pingpong,
    summarize_pingpong,
    validate_reviewer_output,
)
from packages.orchestration.pingpong_provider import (
    FakeProvider,
    ReviewerOutput,
    ReviewFinding,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\nA demo project.\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "README.md").write_text("# Docs\n")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return repo


# ---------------------------------------------------------------------------
# Step 4757: Reviewer output coherence validation
# ---------------------------------------------------------------------------

class TestReviewerCoherence:
    """validate_reviewer_output catches contradictory outputs."""

    def test_pass_no_findings_valid(self):
        out = ReviewerOutput(verdict="pass", findings=[], summary="ok")
        assert validate_reviewer_output(out) is None

    def test_pass_with_findings_incoherent(self):
        out = ReviewerOutput(
            verdict="pass",
            findings=[ReviewFinding(id="R-0001", severity="medium", summary="bug")],
        )
        err = validate_reviewer_output(out)
        assert err is not None
        assert "pass verdict with" in err

    def test_needs_repair_with_findings_valid(self):
        out = ReviewerOutput(
            verdict="needs_repair",
            findings=[ReviewFinding(id="R-0001", severity="medium", summary="bug")],
        )
        assert validate_reviewer_output(out) is None

    def test_fail_no_findings_incoherent(self):
        out = ReviewerOutput(verdict="fail", findings=[])
        err = validate_reviewer_output(out)
        assert err is not None
        assert "no findings" in err

    def test_fail_no_findings_but_error_valid(self):
        out = ReviewerOutput(verdict="fail", findings=[], error="test failure evidence")
        assert validate_reviewer_output(out) is None

    def test_blocked_with_summary_valid(self):
        out = ReviewerOutput(verdict="blocked", findings=[], summary="Cannot proceed")
        assert validate_reviewer_output(out) is None

    def test_blocked_without_summary_incoherent(self):
        out = ReviewerOutput(verdict="blocked", findings=[], summary="")
        err = validate_reviewer_output(out)
        assert err is not None
        assert "blocked" in err

    def test_unknown_verdict_incoherent(self):
        out = ReviewerOutput(verdict="banana", findings=[])
        err = validate_reviewer_output(out)
        assert err is not None
        assert "unknown verdict" in err


class TestReviewerCoherenceE2E:
    """E2E: reviewer pass with findings blocked as inconsistent."""

    def test_pass_with_findings_blocks_run(self, demo_repo: Path):
        """FakeProvider builder + incoherent reviewer -> blocked."""
        builder = FakeProvider()  # Normal fake builder (modifies staging)

        class IncoherentReviewer:
            name = "incoherent_reviewer"
            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                return ReviewerOutput(
                    verdict="pass",
                    findings=[ReviewFinding(id="R-0001", severity="high", summary="Bug")],
                    summary="All good", provider="incoherent",
                )

        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=builder,
            reviewer_provider=IncoherentReviewer(),
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "review_inconsistent"
        assert "pass verdict" in result.error


# ---------------------------------------------------------------------------
# Step 4758: Repair only starts when it makes sense
# ---------------------------------------------------------------------------

class TestRepairDecisionGate:
    """Repair decisions are correct for various scenarios."""

    def test_clean_pass_no_repair(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass", tests_passed=True,
            finding_count=0, repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "pass_no_repair"

    def test_needs_repair_triggers_repair(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="needs_repair", tests_passed=True,
            finding_count=1, repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "repair"

    def test_coherence_error_blocks(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass", tests_passed=True,
            finding_count=1, repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error="pass with findings",
        )
        assert d.repair_decision == "block_inconsistent_review"

    def test_blocked_stops(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="blocked", tests_passed=True,
            finding_count=0, repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "stop_blocked"

    def test_fail_no_findings_no_test_fail_blocks(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="fail", tests_passed=True,
            finding_count=0, repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "block_inconsistent_review"

    def test_test_fail_repair_disabled_stops(self):
        d = make_repair_decision(
            round_num=1, reviewer_verdict="needs_repair", tests_passed=False,
            finding_count=1, repair_rounds_allowed=0, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "stop_test_failed_no_repair"

    def test_budget_exhausted(self):
        d = make_repair_decision(
            round_num=2, reviewer_verdict="needs_repair", tests_passed=True,
            finding_count=1, repair_rounds_allowed=1, repair_rounds_used=1,
            is_repair=True, coherence_error=None,
        )
        assert d.repair_decision == "stop_exhausted"


class TestCleanPassNoExtraCalls:
    """Clean pass causes no extra Builder/Reviewer calls."""

    def test_single_round_clean_pass(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 1
        assert result.repair_rounds_used == 0
        assert provider._build_count == 1
        assert provider._review_count == 1


# ---------------------------------------------------------------------------
# Step 4759: repair_rounds_used semantics
# ---------------------------------------------------------------------------

class TestRepairRoundsUsedSemantics:
    """Every repair Builder attempt counts as one used repair round."""

    def test_initial_build_not_counted(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        assert result.repair_rounds_used == 0

    def test_pass_after_one_repair_counts_1(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"
        assert result.repair_rounds_used == 1

    def test_exhausted_after_one_repair_counts_1(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        assert result.final_status == "repair_exhausted"
        assert result.repair_rounds_used == 1

    def test_no_repair_path_zero(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=0,
        )
        assert result.repair_rounds_used == 0


# ---------------------------------------------------------------------------
# Step 4760: Configurable default repair rounds
# ---------------------------------------------------------------------------

class TestConfigurableRepairRounds:
    """resolve_repair_rounds validates and applies defaults."""

    def test_explicit_zero(self):
        val, source = resolve_repair_rounds(0)
        assert val == 0
        assert source == "cli"

    def test_explicit_one(self):
        val, source = resolve_repair_rounds(1)
        assert val == 1
        assert source == "cli"

    def test_explicit_two(self):
        val, source = resolve_repair_rounds(2)
        assert val == 2
        assert source == "cli"

    def test_default_when_none(self):
        val, source = resolve_repair_rounds(None)
        assert 0 < val <= 10
        assert source == "default"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="must be >= 0"):
            resolve_repair_rounds(-1)

    def test_over_cap_raises(self):
        with pytest.raises(ValueError, match="must be <= 10"):
            resolve_repair_rounds(11)

    def test_ten_valid(self):
        val, source = resolve_repair_rounds(10)
        assert val == 10
        assert source == "cli"


class TestCliRepairRoundsValidation:
    """CLI validation for --repair-rounds."""

    def test_clean_pass_no_repair_even_with_default(self, demo_repo: Path):
        """Clean pass does not repair even if repair_rounds > 0."""
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"
        assert result.repair_rounds_used == 0


# ---------------------------------------------------------------------------
# Step 4761: Repair decision record per review
# ---------------------------------------------------------------------------

class TestRepairDecisionRecord:
    """Repair decisions are persisted on result."""

    def test_decisions_recorded(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert len(result.repair_decisions) == 2
        assert result.repair_decisions[0]["repair_decision"] == "repair"
        assert result.repair_decisions[0]["reason"] == "reviewer_findings_present"
        assert result.repair_decisions[1]["repair_decision"] == "pass_no_repair"
        assert result.repair_decisions[1]["reason"] == "reviewer_passed"

    def test_decision_fields(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        d = result.repair_decisions[0]
        assert "round" in d
        assert "reviewer_verdict" in d
        assert "tests_passed" in d
        assert "finding_count" in d
        assert "repair_decision" in d
        assert "reason" in d

    def test_decisions_in_json(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        data = export_pingpong_json(result)
        assert len(data["repair_loop"]["decisions"]) == 2


# ---------------------------------------------------------------------------
# Step 4762: Deterministic final adjudication
# ---------------------------------------------------------------------------

class TestFinalAdjudication:
    """run_final_adjudication produces correct classifications."""

    def test_no_findings_ready(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="pass",
            open_findings=[], tests_passed=True,
            target_mutated=False, staged_files=["a.py"],
        )
        assert adj.status == "ready"
        assert adj.promotion_allowed is True

    def test_high_findings_not_ready(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="needs_repair",
            open_findings=[ReviewFinding(id="R-0001", severity="high", summary="bug")],
            tests_passed=True, target_mutated=False, staged_files=["a.py"],
        )
        assert adj.status == "not_ready"
        assert adj.promotion_allowed is False

    def test_blocker_findings_blocked(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="needs_repair",
            open_findings=[ReviewFinding(id="R-0001", severity="blocker", summary="critical")],
            tests_passed=True, target_mutated=False, staged_files=["a.py"],
        )
        assert adj.status == "blocked"
        assert adj.promotion_allowed is False

    def test_medium_findings_human_review(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="needs_repair",
            open_findings=[ReviewFinding(id="R-0001", severity="medium", summary="minor")],
            tests_passed=True, target_mutated=False, staged_files=["a.py"],
        )
        assert adj.status == "needs_human_review"
        assert adj.promotion_allowed is False

    def test_tests_failed_not_ready(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="needs_repair",
            open_findings=[], tests_passed=False,
            target_mutated=False, staged_files=["a.py"],
        )
        assert adj.status == "not_ready"
        assert adj.promotion_allowed is False

    def test_target_mutated_blocked(self):
        adj = run_final_adjudication(
            final_status="repair_exhausted", final_verdict="pass",
            open_findings=[], tests_passed=True,
            target_mutated=True, staged_files=["a.py"],
        )
        assert adj.status == "blocked"
        assert adj.promotion_allowed is False


class TestAdjudicationE2E:
    """E2E: repair exhaustion triggers adjudication."""

    def test_exhausted_has_adjudication(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        assert result.final_status == "repair_exhausted"
        assert result.final_adjudication is not None
        assert result.final_adjudication["promotion_allowed"] is False

    def test_clean_pass_no_adjudication(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_adjudication is None


# ---------------------------------------------------------------------------
# Step 4763: Promotion readiness blocked
# ---------------------------------------------------------------------------

class TestPromotionBlocked:
    """Promotion not ready after exhausted/inconsistent."""

    def test_exhausted_blocks_promotion_artifacts(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        # Promotion artifacts should NOT be persisted
        from packages.orchestration.data_paths import pingpong_run_dir
        run_dir = pingpong_run_dir(result.run_id)
        artifacts = run_dir / "artifacts"
        assert not artifacts.exists()


# ---------------------------------------------------------------------------
# Step 4764: Full repair loop JSON schema
# ---------------------------------------------------------------------------

class TestRepairLoopJsonSchema:
    """repair_loop JSON has all required fields."""

    def test_full_schema_on_pass_after_repair(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        data = export_pingpong_json(result)
        rl = data["repair_loop"]
        assert rl["enabled"] is True
        assert rl["repair_rounds_allowed"] == 2
        assert rl["repair_rounds_used"] == 1
        assert rl["status"] == "passed_after_repair"
        assert rl["open_findings"] == []
        assert "R-0001" in rl["resolved_findings"]
        assert rl["final_reviewer_verdict"] == "pass"
        assert isinstance(rl["decisions"], list)
        assert rl["final_adjudication"] is None
        assert isinstance(rl["finding_status_map"], list)

    def test_schema_on_exhausted(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        data = export_pingpong_json(result)
        rl = data["repair_loop"]
        assert rl["status"] == "exhausted"
        assert len(rl["open_findings"]) > 0
        assert rl["final_adjudication"] is not None

    def test_schema_disabled(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=0,
        )
        data = export_pingpong_json(result)
        rl = data["repair_loop"]
        assert rl["enabled"] is False
        assert rl["status"] == "disabled"

    def test_schema_not_needed(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        data = export_pingpong_json(result)
        rl = data["repair_loop"]
        assert rl["status"] == "not_needed"


# ---------------------------------------------------------------------------
# Step 4765: Concise text report
# ---------------------------------------------------------------------------

class TestRepairTextReport:
    """Text report shows correct repair summaries."""

    def test_passed_after_repair(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        text = summarize_pingpong(result)
        assert "Repair loop: passed after" in text
        assert "Resolved findings:" in text
        assert "Open findings: none" in text

    def test_not_needed(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        text = summarize_pingpong(result)
        assert "Repair loop: not needed" in text

    def test_exhausted_with_adjudication(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        text = summarize_pingpong(result)
        assert "Repair loop: exhausted" in text
        assert "Open findings:" in text
        assert "Final adjudication:" in text
        assert "Promotion:" in text

    def test_repair_round_label(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        text = summarize_pingpong(result)
        assert "[repair]" in text

    def test_inconsistent_review_text(self, demo_repo: Path):
        builder = FakeProvider()
        class IncoherentReviewer:
            name = "incoherent_reviewer"
            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                return ReviewerOutput(
                    verdict="pass",
                    findings=[ReviewFinding(id="R-0001", severity="high", summary="Bug")],
                    summary="All good", provider="incoherent",
                )

        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=builder,
            reviewer_provider=IncoherentReviewer(),
            max_rounds=3, repair_rounds=2,
        )
        text = summarize_pingpong(result)
        assert "REVIEW INCONSISTENT" in text


# ---------------------------------------------------------------------------
# Step 4766: Finding status map
# ---------------------------------------------------------------------------

class TestFindingStatusMap:
    """build_finding_status_map produces correct entries."""

    def test_resolved_finding(self):
        rounds = [
            PingPongRound(round_number=1, kind="initial"),
            PingPongRound(
                round_number=2, kind="repair",
                input_finding_ids=["R-0001"],
                resolved_finding_ids=["R-0001"],
                remaining_finding_ids=[],
            ),
        ]
        entries = build_finding_status_map(rounds)
        assert len(entries) == 1
        assert entries[0].prior_finding_id == "R-0001"
        assert entries[0].status == "resolved"
        assert entries[0].evidence_round == 2

    def test_remaining_finding(self):
        rounds = [
            PingPongRound(round_number=1, kind="initial"),
            PingPongRound(
                round_number=2, kind="repair",
                input_finding_ids=["R-0001"],
                resolved_finding_ids=[],
                remaining_finding_ids=["R-0001"],
            ),
        ]
        entries = build_finding_status_map(rounds)
        assert any(e.status == "remaining" for e in entries)

    def test_new_finding(self):
        r2 = PingPongRound(
            round_number=2, kind="repair",
            input_finding_ids=["R-0001"],
            resolved_finding_ids=["R-0001"],
            remaining_finding_ids=[],
        )
        r2.reviewer_output = ReviewerOutput(
            verdict="needs_repair",
            findings=[ReviewFinding(id="R-NEW", severity="low", summary="New issue")],
        )
        rounds = [PingPongRound(round_number=1, kind="initial"), r2]
        entries = build_finding_status_map(rounds)
        new_entries = [e for e in entries if e.status == "new"]
        assert len(new_entries) == 1
        assert new_entries[0].prior_finding_id == "R-NEW"

    def test_in_json_export(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        data = export_pingpong_json(result)
        assert "finding_status_map" in data["repair_loop"]


# ---------------------------------------------------------------------------
# Step 4767: Strengthened re-review prompt
# ---------------------------------------------------------------------------

class TestStrengthenedReReviewPrompt:
    """Re-review prompt has all required verification instructions."""

    def test_must_verify_against_diff(self):
        findings = [ReviewFinding(id="R-0001", severity="medium", summary="Issue")]
        prompt = _build_reviewer_prompt(
            "Fix bug", "summary", prior_findings=findings, repair_round=1,
        )
        assert "diff" in prompt.lower()
        assert "tests" in prompt.lower()

    def test_must_not_pass_with_unfixed(self):
        findings = [ReviewFinding(id="R-0001", severity="medium", summary="Issue")]
        prompt = _build_reviewer_prompt(
            "Fix bug", "summary", prior_findings=findings, repair_round=1,
        )
        assert "Do NOT return pass" in prompt

    def test_test_failure_is_evidence(self):
        findings = [ReviewFinding(id="R-0001", severity="medium", summary="Issue")]
        prompt = _build_reviewer_prompt(
            "Fix bug", "summary", prior_findings=findings, repair_round=1,
        )
        assert "test failure as evidence" in prompt

    def test_initial_review_no_extra_rules(self):
        prompt = _build_reviewer_prompt("Fix bug", "summary")
        assert "Do NOT return pass" not in prompt


# ---------------------------------------------------------------------------
# Step 4768: Token accounting correctness
# ---------------------------------------------------------------------------

class TestRepairTokenAccounting:
    """Token accounting includes repair prompts correctly."""

    def test_repair_prompt_chars_nonzero(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert result.repair_prompt_chars > 0

    def test_no_repair_zero_chars(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=0,
        )
        assert result.repair_prompt_chars == 0

    def test_token_accounting_in_json(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        data = export_pingpong_json(result)
        ta = data["token_accounting"]
        assert ta["repair_prompt_tokens_estimated"] > 0


# ---------------------------------------------------------------------------
# Step 4769: E2E smart stop/continue tests
# ---------------------------------------------------------------------------

class TestSmartStopContinueE2E:
    """Fake-provider E2E for all smart stop/continue scenarios."""

    def test_clean_pass_no_repair_call(self, demo_repo: Path):
        """1. Clean pass causes no repair call."""
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"
        assert provider._build_count == 1

    def test_needs_repair_triggers_repair(self, demo_repo: Path):
        """2. Reviewer needs_repair triggers repair."""
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert len(result.rounds) == 2
        assert result.rounds[1].kind == "repair"

    def test_pass_after_repair_used_1(self, demo_repo: Path):
        """3. pass-after-one-repair uses repair_rounds_used == 1."""
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert result.repair_rounds_used == 1

    def test_pass_with_findings_blocked(self, demo_repo: Path):
        """4. Reviewer pass with findings is blocked as inconsistent."""
        builder = FakeProvider()
        class BadReviewer:
            name = "bad_reviewer"
            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                return ReviewerOutput(
                    verdict="pass",
                    findings=[ReviewFinding(id="X", severity="high", summary="bug")],
                    summary="ok", provider="bad",
                )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=builder,
            reviewer_provider=BadReviewer(),
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "review_inconsistent"

    def test_fail_no_findings_blocked(self, demo_repo: Path):
        """5. Reviewer fail with no findings and no test failure is blocked."""
        builder = FakeProvider()
        class FailNothingReviewer:
            name = "failnothing_reviewer"
            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                return ReviewerOutput(
                    verdict="fail", findings=[], summary="bad",
                    provider="failnothing",
                )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=builder,
            reviewer_provider=FailNothingReviewer(),
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "review_inconsistent"

    def test_test_fail_with_repair_continues(self, demo_repo: Path, tmp_path: Path):
        """6. Test failure with repair enabled triggers repair/review path."""
        test_script = tmp_path / "fail_test.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
            test_command=str(test_script),
        )
        assert result.rounds[0].reviewer_output is not None
        assert result.rounds[0].test_passed is False

    def test_test_fail_no_repair_stops(self, demo_repo: Path, tmp_path: Path):
        """7. Test failure with repair disabled stops immediately."""
        test_script = tmp_path / "fail_test.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=0,
            test_command=str(test_script),
        )
        assert result.final_status == "test_failed"

    def test_exhaustion_runs_adjudication(self, demo_repo: Path):
        """8. Repair budget exhaustion runs final adjudication."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        assert result.final_status == "repair_exhausted"
        assert result.final_adjudication is not None

    def test_exhausted_blocks_promotion(self, demo_repo: Path):
        """9. Exhausted repair blocks promotion readiness."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        assert result.final_adjudication["promotion_allowed"] is False

    def test_high_findings_not_ready(self, demo_repo: Path):
        """10. Open high findings classify adjudication as not_ready."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        # FakeProvider findings are "medium" severity
        assert result.final_adjudication["status"] in ("not_ready", "needs_human_review")


# ---------------------------------------------------------------------------
# Step 4770: CLI/config repair default tests
# ---------------------------------------------------------------------------

class TestCliConfigRepairDefaults:
    """CLI --repair-rounds validation."""

    def test_zero_disables(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=0,
        )
        assert result.repair_rounds_allowed == 0

    def test_one_allows_one(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=1,
        )
        assert result.repair_rounds_allowed == 1
        assert result.repair_rounds_used <= 1

    def test_two_allows_two(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=99)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=5, repair_rounds=2,
        )
        assert result.repair_rounds_allowed == 2

    def test_negative_blocked(self):
        with pytest.raises(ValueError):
            resolve_repair_rounds(-1)

    def test_over_10_blocked(self):
        with pytest.raises(ValueError):
            resolve_repair_rounds(11)

    def test_default_never_unbounded(self):
        val, _source = resolve_repair_rounds(None)
        assert val <= 10

    def test_clean_pass_no_repair_even_with_budget(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3, repair_rounds=5,
        )
        assert result.repair_rounds_used == 0
        assert result.final_status == "staged_review_passed"


# ---------------------------------------------------------------------------
# Step 4771: Preserve existing flows
# ---------------------------------------------------------------------------

class TestExistingFlowsPreserved:
    """Existing short-goal, task-file, no-repair paths still work."""

    def test_short_goal_works(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert result.final_status == "staged_review_passed"

    def test_pass_first_round_works(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            max_rounds=3,
        )
        assert result.final_status == "staged_review_passed"
        assert len(result.rounds) == 1

    def test_target_not_mutated(self, demo_repo: Path):
        original_readme = (demo_repo / "README.md").read_text()
        run_pingpong("Fix README", str(demo_repo), builder_name="fake", reviewer_name="fake")
        assert (demo_repo / "README.md").read_text() == original_readme

    def test_json_export_valid(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3,
        )
        import json
        data = export_pingpong_json(result)
        json_str = json.dumps(data)  # must not raise
        assert "run_id" in data
        assert "repair_loop" in data

    def test_provider_evidence_present(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3,
        )
        data = export_pingpong_json(result)
        assert "provider_evidence" in data

    def test_token_accounting_present(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3,
        )
        data = export_pingpong_json(result)
        assert "token_accounting" in data


# ---------------------------------------------------------------------------
# Round lifecycle state tests (updated from v1)
# ---------------------------------------------------------------------------

class TestRoundLifecycleStates:
    """PingPongRound kind, repair_of_round, finding ID tracking."""

    def test_initial_round_defaults(self):
        rd = PingPongRound(round_number=1)
        assert rd.kind == "initial"
        assert rd.repair_of_round == 0
        assert rd.input_finding_ids == []

    def test_repair_round_fields(self):
        rd = PingPongRound(
            round_number=2, kind="repair", repair_of_round=1,
            input_finding_ids=["R-0001"],
        )
        assert rd.kind == "repair"
        assert rd.repair_of_round == 1
        assert rd.input_finding_ids == ["R-0001"]

    def test_round_kinds_e2e(self, demo_repo: Path):
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="fake", reviewer_name="fake",
            max_rounds=3, repair_rounds=2,
        )
        assert result.rounds[0].kind == "initial"
        assert result.rounds[1].kind == "repair"
        assert result.rounds[1].repair_of_round == 1
        assert result.rounds[1].input_finding_ids == ["R-0001"]


# ---------------------------------------------------------------------------
# Builder repair prompt tests
# ---------------------------------------------------------------------------

class TestBuilderRepairPrompt:
    """Builder prompt includes repair instructions when findings present."""

    def test_initial_no_repair_section(self):
        prompt = _build_builder_prompt("Fix bug", "context")
        assert "REPAIR TASK" not in prompt

    def test_repair_includes_findings(self):
        findings = [
            ReviewFinding(
                id="R-0001", severity="medium",
                file="src/main.py", summary="Missing check",
                required_fix="Add null check",
            ),
        ]
        prompt = _build_builder_prompt(
            "Fix bug", "context",
            round_number=2, findings=findings,
            test_result="tests failed: 1 error",
        )
        assert "REPAIR TASK" in prompt
        assert "R-0001" in prompt
        assert "Missing check" in prompt
        assert "Add null check" in prompt
        assert "tests failed" in prompt

    def test_repair_safety_instructions(self):
        findings = [ReviewFinding(id="R-0001", severity="medium", summary="Issue")]
        prompt = _build_builder_prompt(
            "Fix bug", "context", round_number=2, findings=findings,
        )
        assert "Fix ONLY" in prompt
        assert "Do not touch the target repo" in prompt


# ---------------------------------------------------------------------------
# Steps 4781-4784: Repair Governance Correctness Closure v3 — New Tests
# ---------------------------------------------------------------------------

class TestRepairRoundsZeroTrulyDisables:
    """Step 4781: repair_rounds=0 must truly disable repair."""

    def test_explicit_zero_stops_on_findings(self, demo_repo: Path):
        """repair_rounds=0 + findings => repair_exhausted, not repair."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0,
        )
        assert result.final_status == "repair_exhausted"
        assert len(result.rounds) == 1
        assert result.repair_rounds_used == 0

    def test_explicit_zero_no_legacy_repair_decision(self, demo_repo: Path):
        """No legacy_max_rounds_behavior in decisions."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0,
        )
        for d in result.repair_decisions:
            assert d["reason"] != "legacy_max_rounds_behavior"

    def test_explicit_zero_clean_pass_still_works(self, demo_repo: Path):
        """repair_rounds=0 + clean pass => staged_review_passed."""
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0,
        )
        assert result.final_status == "staged_review_passed"

    def test_stop_repair_disabled_decision(self):
        """make_repair_decision returns stop_repair_disabled when rounds=0."""
        decision = make_repair_decision(
            round_num=1, reviewer_verdict="needs_repair",
            tests_passed=None, finding_count=2,
            repair_rounds_allowed=0, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert decision.repair_decision == "stop_repair_disabled"
        assert decision.reason == "repair_rounds_zero"

    def test_adjudication_runs_after_disabled_stop(self, demo_repo: Path):
        """repair_exhausted from disabled triggers adjudication."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0,
        )
        assert result.final_adjudication is not None
        assert result.final_adjudication["promotion_allowed"] is False


class TestCliDefaultAndExplicitZero:
    """Step 4782: CLI default and explicit-zero tests."""

    def test_resolve_none_returns_default_with_source(self):
        val, source = resolve_repair_rounds(None)
        assert val == 2
        assert source == "default"

    def test_resolve_explicit_zero_returns_cli_source(self):
        val, source = resolve_repair_rounds(0)
        assert val == 0
        assert source == "cli"

    def test_resolve_explicit_five_returns_cli_source(self):
        val, source = resolve_repair_rounds(5)
        assert val == 5
        assert source == "cli"

    def test_repair_rounds_source_on_result(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=3, repair_rounds_source="cli",
        )
        assert result.repair_rounds_source == "cli"

    def test_repair_rounds_source_in_json(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2, repair_rounds_source="default",
        )
        data = export_pingpong_json(result)
        assert data["repair_loop"]["repair_rounds_source"] == "default"


class TestInconsistentReviewAdjudication:
    """Step 4783: review_inconsistent must never adjudicate as ready."""

    def test_inconsistent_never_ready(self):
        """Even with no open findings, review_inconsistent => needs_human_review."""
        adj = run_final_adjudication(
            final_status="review_inconsistent",
            final_verdict="pass",
            open_findings=[],
            tests_passed=None,
            target_mutated=False,
            staged_files=["a.py"],
        )
        assert adj.status == "needs_human_review"
        assert adj.promotion_allowed is False

    def test_inconsistent_with_findings_still_blocked(self):
        findings = [ReviewFinding(id="R-01", severity="high", summary="Bug")]
        adj = run_final_adjudication(
            final_status="review_inconsistent",
            final_verdict="fail",
            open_findings=findings,
            tests_passed=None,
            target_mutated=False,
            staged_files=["a.py"],
        )
        assert adj.status == "needs_human_review"
        assert adj.promotion_allowed is False

    def test_inconsistent_with_passing_tests_still_blocked(self):
        adj = run_final_adjudication(
            final_status="review_inconsistent",
            final_verdict="pass",
            open_findings=[],
            tests_passed=True,
            target_mutated=False,
            staged_files=["a.py"],
        )
        assert adj.status == "needs_human_review"
        assert adj.promotion_allowed is False

    def test_inconsistent_e2e(self, demo_repo: Path):
        """E2E: incoherent reviewer => review_inconsistent => blocked adjudication."""

        class IncoherentReviewer(FakeProvider):
            def review(self, prompt, **kw):
                return ReviewerOutput(
                    verdict="pass",
                    confidence=0.9,
                    summary="Looks good",
                    findings=[ReviewFinding(id="BUG-1", severity="high", summary="Bug")],
                    provider="incoherent",
                )

        builder = FakeProvider(fail_on_round=99, pass_on_round=1)
        reviewer = IncoherentReviewer()
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=builder, reviewer_provider=reviewer,
            repair_rounds=2,
        )
        assert result.final_status == "review_inconsistent"
        assert result.final_adjudication is not None
        assert result.final_adjudication["status"] == "needs_human_review"
        assert result.final_adjudication["promotion_allowed"] is False


class TestTestFailureCoherence:
    """Step 4784: test_passed flows into coherence validation."""

    def test_fail_verdict_no_findings_tests_failed_is_coherent(self):
        """needs_repair with no findings but tests_failed => coherent (test failure is evidence)."""
        out = ReviewerOutput(
            verdict="needs_repair", confidence=0.8,
            summary="Tests failed", findings=[], provider="fake",
        )
        err = validate_reviewer_output(out, test_passed=False)
        assert err is None  # coherent — test failure is evidence

    def test_fail_verdict_no_findings_tests_passed_is_incoherent(self):
        """needs_repair with no findings and tests passed => incoherent."""
        out = ReviewerOutput(
            verdict="needs_repair", confidence=0.8,
            summary="Issues found", findings=[], provider="fake",
        )
        err = validate_reviewer_output(out, test_passed=True)
        assert err is not None
        assert "no findings" in err

    def test_fail_verdict_no_findings_tests_none_is_incoherent(self):
        """needs_repair with no findings and tests=None => incoherent."""
        out = ReviewerOutput(
            verdict="needs_repair", confidence=0.8,
            summary="Issues found", findings=[], provider="fake",
        )
        err = validate_reviewer_output(out, test_passed=None)
        assert err is not None

    def test_pass_verdict_with_findings_always_incoherent(self):
        """pass with findings => incoherent regardless of test status."""
        out = ReviewerOutput(
            verdict="pass", confidence=0.9, summary="OK",
            findings=[ReviewFinding(id="R-1", severity="low", summary="X")],
            provider="fake",
        )
        err = validate_reviewer_output(out, test_passed=True)
        assert err is not None
        assert "pass verdict with" in err


class TestReReviewRoundLabel:
    """Step 4779 verification: re-review round label is correct."""

    def test_first_repair_labeled_round_1(self, demo_repo: Path):
        """After initial review fails, re-review label should say Repair Round 1."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)

        prompts: list[str] = []
        orig_review = provider.review

        def capture_review(prompt, **kw):
            prompts.append(prompt)
            return orig_review(prompt, **kw)

        provider.review = capture_review
        run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        # Round 2 reviewer prompt should say "Repair Round 1"
        assert len(prompts) >= 2
        repair_prompt = prompts[1]
        assert "Repair Round 1" in repair_prompt
        assert "Repair Round 2" not in repair_prompt


# ---------------------------------------------------------------------------
# Steps 4788-4798: Test Evidence Dominance Closure v4 — New Tests
# ---------------------------------------------------------------------------

class TestTestFailureDominanceUnit:
    """Unit tests for test-failure dominance in make_repair_decision."""

    def test_reviewer_pass_tests_failed_triggers_repair(self):
        """Reviewer pass + tests failed + budget => repair with test_failure_evidence."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=False, finding_count=0,
            repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "repair"
        assert d.reason == "test_failure_evidence"

    def test_reviewer_pass_tests_failed_no_budget_stops(self):
        """Reviewer pass + tests failed + no budget => stop_test_failed_no_repair."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=False, finding_count=0,
            repair_rounds_allowed=0, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "stop_test_failed_no_repair"
        assert d.reason == "test_failed_repair_disabled"

    def test_reviewer_pass_tests_failed_exhausted_stops(self):
        """Reviewer pass + tests failed + exhausted => stop_exhausted."""
        d = make_repair_decision(
            round_num=2, reviewer_verdict="pass",
            tests_passed=False, finding_count=0,
            repair_rounds_allowed=1, repair_rounds_used=1,
            is_repair=True, coherence_error=None,
        )
        assert d.repair_decision == "stop_exhausted"
        assert "test_failed" in d.reason

    def test_reviewer_pass_tests_passed_is_clean_pass(self):
        """Reviewer pass + tests passed => pass_no_repair (clean pass)."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=True, finding_count=0,
            repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "pass_no_repair"
        assert d.reason == "reviewer_passed"

    def test_reviewer_pass_tests_none_is_clean_pass(self):
        """Reviewer pass + tests=None (not run) => pass_no_repair."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=None, finding_count=0,
            repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "pass_no_repair"

    def test_needs_repair_tests_failed_triggers_repair(self):
        """needs_repair + tests failed + budget => repair with test_failure_evidence."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="needs_repair",
            tests_passed=False, finding_count=2,
            repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        assert d.repair_decision == "repair"
        assert d.reason == "test_failure_evidence"


class TestTestFailureDominanceE2E:
    """E2E tests proving test-failure dominance (Step 4796)."""

    def test_tests_failed_reviewer_pass_repair_disabled(self, demo_repo: Path, tmp_path: Path):
        """1-3. Tests failed + Reviewer pass + repair_rounds=0 => not pass, no repair, no promotion."""
        test_script = tmp_path / "fail.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        # Provider that always passes review
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0, test_command=str(test_script),
        )
        # 1. final status is NOT pass
        assert result.final_status != "staged_review_passed"
        assert result.final_status == "test_failed"
        # 2. no repair call (only 1 round)
        assert len(result.rounds) == 1
        assert result.repair_rounds_used == 0
        # 3. promotion blocked
        data = export_pingpong_json(result)
        if result.final_adjudication:
            assert result.final_adjudication["promotion_allowed"] is False

    def test_tests_failed_reviewer_pass_repair_enabled(self, demo_repo: Path, tmp_path: Path):
        """4. Tests failed + Reviewer pass + repair_rounds=2 => repair starts."""
        marker = tmp_path / "toggle_marker"
        test_script = tmp_path / "toggle.sh"
        test_script.write_text(
            f"#!/bin/sh\n"
            f"if [ -f \"{marker}\" ]; then exit 0; fi\n"
            f"touch \"{marker}\"\n"
            f"exit 1\n"
        )
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2, max_rounds=3, test_command=str(test_script),
        )
        # Repair started because tests failed
        assert len(result.rounds) >= 2
        # Check decision shows test_failure_evidence
        assert any(d["reason"] == "test_failure_evidence" for d in result.repair_decisions)

    def test_repair_fixes_tests_then_pass(self, demo_repo: Path, tmp_path: Path):
        """5. Repair fixes tests + Reviewer pass => staged_review_passed."""
        marker = tmp_path / "toggle_marker2"
        test_script = tmp_path / "toggle.sh"
        test_script.write_text(
            f"#!/bin/sh\n"
            f"if [ -f \"{marker}\" ]; then exit 0; fi\n"
            f"touch \"{marker}\"\n"
            f"exit 1\n"
        )
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2, max_rounds=3, test_command=str(test_script),
        )
        assert result.final_status == "staged_review_passed"

    def test_repair_does_not_fix_tests(self, demo_repo: Path, tmp_path: Path):
        """6. Repair does not fix tests => not pass."""
        test_script = tmp_path / "always_fail.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=1, max_rounds=3, test_command=str(test_script),
        )
        assert result.final_status != "staged_review_passed"
        assert result.final_status in ("repair_exhausted", "test_failed", "max_rounds_reached")

    def test_clean_tests_reviewer_pass_no_repair(self, demo_repo: Path, tmp_path: Path):
        """7. Clean tests + Reviewer pass => no repair starts."""
        test_script = tmp_path / "pass.sh"
        test_script.write_text("#!/bin/sh\nexit 0\n")
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2, test_command=str(test_script),
        )
        assert result.final_status == "staged_review_passed"
        assert result.repair_rounds_used == 0
        assert len(result.rounds) == 1


class TestTestFailureJsonReport:
    """Step 4794: JSON report shows test-driven decisions."""

    def test_test_failure_repair_in_json(self):
        """Decision record shows test_failure_evidence."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=False, finding_count=0,
            repair_rounds_allowed=2, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        data = d.to_dict()
        assert data["repair_decision"] == "repair"
        assert data["reason"] == "test_failure_evidence"
        assert data["tests_passed"] is False
        assert data["reviewer_verdict"] == "pass"

    def test_test_failure_disabled_in_json(self):
        """Decision record shows test_failed_repair_disabled."""
        d = make_repair_decision(
            round_num=1, reviewer_verdict="pass",
            tests_passed=False, finding_count=0,
            repair_rounds_allowed=0, repair_rounds_used=0,
            is_repair=False, coherence_error=None,
        )
        data = d.to_dict()
        assert data["repair_decision"] == "stop_test_failed_no_repair"
        assert data["tests_passed"] is False


class TestTestFailureTextReport:
    """Step 4795: Text report distinguishes test-driven repair."""

    def test_text_mentions_failed_tests_trigger(self, demo_repo: Path, tmp_path: Path):
        """Text report says 'triggered by failed tests' for test-driven repair."""
        marker = tmp_path / "toggle_marker"
        test_script = tmp_path / "toggle.sh"
        test_script.write_text(
            f"#!/bin/sh\n"
            f"if [ -f \"{marker}\" ]; then exit 0; fi\n"
            f"touch \"{marker}\"\n"
            f"exit 1\n"
        )
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2, max_rounds=3, test_command=str(test_script),
        )
        summary = summarize_pingpong(result)
        assert "failed tests" in summary

    def test_text_stopped_test_failure(self, demo_repo: Path, tmp_path: Path):
        """Text report says 'stopped' when test fails with repair disabled."""
        test_script = tmp_path / "fail.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0, test_command=str(test_script),
        )
        summary = summarize_pingpong(result)
        assert "test_failed" in summary or "stopped" in summary


class TestPromotionBlockedAfterFailedTests:
    """Step 4793: No promotion artifacts when tests failed."""

    def test_no_promotion_with_reviewer_pass_tests_failed(self, demo_repo: Path, tmp_path: Path):
        """Promotion must be blocked when tests fail even if Reviewer passes."""
        test_script = tmp_path / "fail.sh"
        test_script.write_text("#!/bin/sh\nexit 1\n")
        test_script.chmod(0o755)
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=0, test_command=str(test_script),
        )
        # Not pass
        assert result.final_status != "staged_review_passed"
        # Adjudication blocks promotion
        assert result.final_adjudication is not None
        assert result.final_adjudication["promotion_allowed"] is False
        assert result.final_adjudication["status"] == "not_ready"


# ---------------------------------------------------------------------------
# Steps 4799-4806: CLI Repair Default Truth Closure v5 — New Tests
# ---------------------------------------------------------------------------

class TestCliRepairRoundsDispatch:
    """Steps 4800-4802: CLI dispatch honors omitted vs explicit --repair-rounds."""

    def test_omitted_repair_rounds_passes_none(self):
        """Step 4800: Omitted --repair-rounds reaches _cmd_do as None."""
        from unittest.mock import patch as mock_patch

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        class FakeArgs:
            goal = "Fix README"
            repo = "."
            builder = "fake"
            reviewer = "fake"
            max_rounds = 3
            mode = "staged"
            json = True
            dry_run = False
            enable_ui = False
            fixture_builder = False
            builder_provider = "none"
            test_command = ""
            provider_timeout_sec = 120
            max_output_chars = 50000
            keep_staging = False
            claude_cli_write_mode = "none"
            task_file = ""
            task_stdin = False
            scope_file = ""
            approve_scope = False
            repair_rounds = None  # omitted
            autonomy_level = 2
            project = None
            user_requested = False
            prefer_local_for_cheap_tasks = False
            prefer_ollama_for_cheap_tasks = False
            require_human_approval_for_expensive = False

        with mock_patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            COMMAND_HANDLERS["do.run"](FakeArgs())
            _, kwargs = mock_do.call_args
            assert kwargs["repair_rounds"] is None

    def test_explicit_zero_passes_zero(self):
        """Step 4801: Explicit --repair-rounds 0 reaches _cmd_do as 0."""
        from unittest.mock import patch as mock_patch

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        class FakeArgs:
            goal = "Fix README"
            repo = "."
            builder = "fake"
            reviewer = "fake"
            max_rounds = 3
            mode = "staged"
            json = True
            dry_run = False
            enable_ui = False
            fixture_builder = False
            builder_provider = "none"
            test_command = ""
            provider_timeout_sec = 120
            max_output_chars = 50000
            keep_staging = False
            claude_cli_write_mode = "none"
            task_file = ""
            task_stdin = False
            scope_file = ""
            approve_scope = False
            repair_rounds = 0  # explicit zero
            autonomy_level = 2
            project = None
            user_requested = False
            prefer_local_for_cheap_tasks = False
            prefer_ollama_for_cheap_tasks = False
            require_human_approval_for_expensive = False

        with mock_patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            COMMAND_HANDLERS["do.run"](FakeArgs())
            _, kwargs = mock_do.call_args
            assert kwargs["repair_rounds"] == 0

    def test_explicit_one_passes_one(self):
        """Step 4802: Explicit --repair-rounds 1 reaches _cmd_do as 1."""
        from unittest.mock import patch as mock_patch

        from apps.cli.commands.do_cmd import COMMAND_HANDLERS

        class FakeArgs:
            goal = "Fix README"
            repo = "."
            builder = "fake"
            reviewer = "fake"
            max_rounds = 3
            mode = "staged"
            json = True
            dry_run = False
            enable_ui = False
            fixture_builder = False
            builder_provider = "none"
            test_command = ""
            provider_timeout_sec = 120
            max_output_chars = 50000
            keep_staging = False
            claude_cli_write_mode = "none"
            task_file = ""
            task_stdin = False
            scope_file = ""
            approve_scope = False
            repair_rounds = 1  # explicit one
            autonomy_level = 2
            project = None
            user_requested = False
            prefer_local_for_cheap_tasks = False
            prefer_ollama_for_cheap_tasks = False
            require_human_approval_for_expensive = False

        with mock_patch("apps.cli.commands.do_cmd._cmd_do") as mock_do:
            COMMAND_HANDLERS["do.run"](FakeArgs())
            _, kwargs = mock_do.call_args
            assert kwargs["repair_rounds"] == 1

    def test_omitted_resolves_to_default_two(self, demo_repo: Path):
        """Omitted --repair-rounds resolves to default 2 in run_pingpong."""
        provider = FakeProvider(fail_on_round=99, pass_on_round=1)
        # Simulate what _cmd_do does: resolve_repair_rounds(None)
        val, source = resolve_repair_rounds(None)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=val, repair_rounds_source=source,
        )
        assert result.repair_rounds_allowed == 2
        assert result.repair_rounds_source == "default"
        data = export_pingpong_json(result)
        assert data["repair_loop"]["repair_rounds_allowed"] == 2
        assert data["repair_loop"]["repair_rounds_source"] == "default"

    def test_explicit_zero_disables_in_json(self, demo_repo: Path):
        """Explicit zero: repair disabled, source=cli in JSON."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        val, source = resolve_repair_rounds(0)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=val, repair_rounds_source=source,
        )
        data = export_pingpong_json(result)
        assert data["repair_loop"]["repair_rounds_allowed"] == 0
        assert data["repair_loop"]["repair_rounds_source"] == "cli"
        assert data["repair_loop"]["enabled"] is False
        # Findings present but no repair
        assert result.final_status == "repair_exhausted"

    def test_explicit_one_allows_one_repair(self, demo_repo: Path):
        """Explicit 1: exactly one repair round used."""
        provider = FakeProvider(fail_on_round=1, pass_on_round=2)
        val, source = resolve_repair_rounds(1)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=val, repair_rounds_source=source,
            max_rounds=3,
        )
        data = export_pingpong_json(result)
        assert data["repair_loop"]["repair_rounds_allowed"] == 1
        assert data["repair_loop"]["repair_rounds_source"] == "cli"
        assert result.final_status == "staged_review_passed"
        assert result.repair_rounds_used == 1
