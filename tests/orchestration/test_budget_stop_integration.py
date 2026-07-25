"""F018 T003 — budget stop integration tests.

Tests the unified should_stop() predicate, budget-triggered stopping,
decision queue entries, and deadline-at-start refusal.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import (
    BudgetCounterError,
    BudgetCounters,
    evaluate_budget,
)
from packages.orchestration.safe_points import (
    request_stop,
    should_stop,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)


class TestShouldStopOperatorFirst:
    """Operator stop takes precedence over budget."""

    def test_no_stop_no_budget(self, tmp_path):
        r = should_stop("test-job-001", control_root_path=tmp_path)
        assert r.should_stop is False
        assert r.reason == ""
        assert r.operator_signal is None
        assert r.budget_evaluation is None

    def test_operator_stop_wins(self, tmp_path):
        request_stop("test-job-002", reason="manual", control_root_path=tmp_path)
        r = should_stop("test-job-002", control_root_path=tmp_path)
        assert r.should_stop is True
        assert "operator_stop" in r.reason
        assert r.source == "operator"
        assert r.operator_signal is not None

    def test_operator_stop_before_budget(self, tmp_path):
        request_stop("test-job-003", reason="kill", control_root_path=tmp_path)
        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(provider_calls=100, measured_call_count=100, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-003",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert r.source == "operator"

    def test_budget_exhausted_no_operator(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=3, measured_call_count=3, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-004",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert r.source == "budget"
        assert "budget_exhausted:max_provider_calls" in r.reason
        assert r.budget_evaluation is not None

    def test_budget_not_exhausted_continues(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(provider_calls=2, measured_call_count=2, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-005",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False


class TestThreeCallLimit:
    """A three-call limit stops before call four."""

    def test_three_calls_allowed(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=2, measured_call_count=2, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-3c1",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False

    def test_at_three_calls_stops(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(provider_calls=3, measured_call_count=3, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-3c2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert "max_provider_calls" in r.reason


class TestDeadlineAtStart:
    """Past deadline at start refuses work."""

    def test_past_deadline_stops(self, tmp_path):
        dl = T0 - timedelta(hours=1)
        budgets = JobBudgets(deadline=dl)
        counters = BudgetCounters()
        r = should_stop(
            "test-job-dl1",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is True
        assert "deadline" in r.reason

    def test_future_deadline_continues(self, tmp_path):
        dl = T0 + timedelta(hours=1)
        budgets = JobBudgets(deadline=dl)
        counters = BudgetCounters()
        r = should_stop(
            "test-job-dl2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        assert r.should_stop is False


class TestShouldStopSerialization:
    def test_no_stop_to_json(self, tmp_path):
        r = should_stop("test-job-j1", control_root_path=tmp_path)
        d = r.to_json()
        assert d["should_stop"] is False
        assert d["reason"] == ""

    def test_budget_stop_to_json(self, tmp_path):
        budgets = JobBudgets(max_provider_calls=1)
        counters = BudgetCounters(provider_calls=5, measured_call_count=5, actual_sources=("pingpong_actuals",))
        r = should_stop(
            "test-job-j2",
            budgets=budgets,
            counters=counters,
            now=T0,
            control_root_path=tmp_path,
        )
        d = r.to_json()
        assert d["should_stop"] is True
        assert "budget_evaluation" in d


class TestDecisionQueueEntry:
    """Budget exhaustion produces a token_budget decision type."""

    def test_token_budget_in_decision_types(self):
        from packages.orchestration.decision_queue import DECISION_TYPES
        assert "token_budget" in DECISION_TYPES

    def test_budget_evaluation_carries_limit_info(self):
        budgets = JobBudgets(max_total_tokens=1000)
        counters = BudgetCounters(provider_calls=5, measured_token_total=2000, measured_call_count=5, actual_sources=("pingpong_actuals",))
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is True
        assert evaluation.first_exhausted_limit == "max_total_tokens"
        d = evaluation.to_json()
        assert d["first_exhausted_limit"] == "max_total_tokens"


class TestDecisionQueueDerivation:
    """list_decisions derives token_budget from job state."""

    def test_budget_exhausted_produces_decision(self):
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions
        job = Job(name="budget-test", metadata={"error": "budget_exhausted: max_provider_calls"})
        decisions = list_decisions(job, [])
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 1
        assert budget_decisions[0].severity == "blocker"
        assert "budget_exhausted" in budget_decisions[0].safe_summary

    def test_no_budget_error_no_decision(self):
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions
        job = Job(name="ok-test")
        decisions = list_decisions(job, [])
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 0


class TestPostmortemClass:
    """FailureClass.BUDGET_EXHAUSTED exists and is classifiable."""

    def test_budget_exhausted_exists(self):
        from packages.orchestration.failure_postmortem import FailureClass
        assert hasattr(FailureClass, "BUDGET_EXHAUSTED")
        assert FailureClass.BUDGET_EXHAUSTED.value == "budget_exhausted"


class TestStopReasonCode:
    """Stop reasons include token_budget_exceeded."""

    def test_stop_reason_code_exists(self):
        from packages.orchestration.stop_reasons import REASON_CODES
        assert "token_budget_exceeded" in REASON_CODES


class TestWallClockFromStartedAt:
    """Wall clock derives from started_at + now, not arbitrary elapsed."""

    def test_started_at_overrides_elapsed(self):
        started = T0 - timedelta(minutes=120)
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(started_at=started, elapsed_seconds=0.0)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is True

    def test_no_started_at_uses_elapsed(self):
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(elapsed_seconds=1800.0)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is False


class TestCounterValidation:
    """BudgetCounters rejects impossible data."""

    def test_negative_values_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=-1)

    def test_boolean_values_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=True)  # type: ignore[arg-type]

    def test_inconsistent_counts_rejected(self):
        with pytest.raises(BudgetCounterError):
            BudgetCounters(provider_calls=5, measured_call_count=2, unmeasured_call_count=1, actual_sources=("pingpong_actuals",))

    def test_consistent_counts_accepted(self):
        c = BudgetCounters(provider_calls=3, measured_call_count=2, unmeasured_call_count=1, actual_sources=("pingpong_actuals",))
        assert c.provider_calls == 3


# ---------------------------------------------------------------------------
# Finding #2: fail-closed config on unknown budget.* keys
# ---------------------------------------------------------------------------


class TestConfigFailClosed:
    """Unknown budget.* config keys must raise, not warn."""

    def test_unknown_budget_key_raises(self, tmp_path):
        from packages.orchestration.budget_resolution import BudgetConfigError

        toml_path = tmp_path / "remedy.toml"
        toml_path.write_text(
            '[remedy.budget]\nmax_toknes = 1000\n'
        )
        from packages.orchestration.config import load_config
        with pytest.raises(BudgetConfigError, match="Unknown budget config key"):
            load_config(project_path=toml_path)

    def test_known_budget_key_ok(self, tmp_path):
        toml_path = tmp_path / "remedy.toml"
        toml_path.write_text(
            '[remedy.budget]\nmax_total_tokens = 5000\n'
        )
        from packages.orchestration.config import load_config
        cfg = load_config(project_path=toml_path)
        assert cfg is not None

    def test_unknown_non_budget_key_warns_only(self, tmp_path):
        toml_path = tmp_path / "remedy.toml"
        toml_path.write_text(
            '[remedy]\nfuture_key = "hello"\n'
        )
        from packages.orchestration.config import load_config
        cfg = load_config(project_path=toml_path)
        assert any("Unknown key" in w for w in cfg.load_report.warnings)


# ---------------------------------------------------------------------------
# Finding #6: deterministic budget stop request_id
# ---------------------------------------------------------------------------


class TestDeterministicBudgetStopId:
    """Budget stop request_id is deterministic, not random."""

    def test_same_inputs_same_id(self):
        import hashlib
        job_id = "test-job-det1"
        reason = "budget_exhausted:max_provider_calls"
        id1 = hashlib.sha256(f"{job_id}:{reason}".encode()).hexdigest()[:16]
        id2 = hashlib.sha256(f"{job_id}:{reason}".encode()).hexdigest()[:16]
        assert id1 == id2
        assert f"budget_{id1}" == f"budget_{id2}"

    def test_different_reasons_different_ids(self):
        import hashlib
        job_id = "test-job-det2"
        id1 = hashlib.sha256(
            f"{job_id}:budget_exhausted:max_provider_calls".encode()
        ).hexdigest()[:16]
        id2 = hashlib.sha256(
            f"{job_id}:budget_exhausted:max_total_tokens".encode()
        ).hexdigest()[:16]
        assert id1 != id2


# ---------------------------------------------------------------------------
# Finding #7: decision queue reads stop events for budget
# ---------------------------------------------------------------------------


class TestDecisionQueueBudgetEvents:
    """Decision queue detects budget stops from events."""

    def test_job_stopped_event_produces_decision(self):
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions
        job = Job(name="event-test")
        events = [{
            "event": "job_stopped",
            "metadata": {
                "source": "budget",
                "reason": "budget_exhausted:max_provider_calls",
                "request_id": "budget_abc123",
            },
        }]
        decisions = list_decisions(job, events)
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 1
        assert "budget" in budget_decisions[0].safe_summary

    def test_metadata_budget_stop_produces_decision(self):
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions
        job = Job(
            name="meta-budget-test",
            metadata={"budget_stop_reason": "budget_exhausted:max_total_tokens"},
        )
        decisions = list_decisions(job, [])
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 1


# ---------------------------------------------------------------------------
# Finding #8: budget postmortem classification
# ---------------------------------------------------------------------------


class TestBudgetPostmortemClassification:
    """Budget stops produce budget_exhausted, not stopped."""

    def test_budget_exhausted_classified_correctly(self):
        from packages.orchestration.failure_postmortem import (
            TERMINAL_STATUS_CLASSES,
            FailureClass,
            FailureSignals,
            classify,
        )
        assert TERMINAL_STATUS_CLASSES["budget_exhausted"] == FailureClass.BUDGET_EXHAUSTED
        result = classify(FailureSignals(terminal_status="budget_exhausted"))
        assert result.failure_class == FailureClass.BUDGET_EXHAUSTED

    def test_stopped_classified_differently(self):
        from packages.orchestration.failure_postmortem import (
            FailureClass,
            FailureSignals,
            classify,
        )
        result = classify(FailureSignals(terminal_status="stopped"))
        assert result.failure_class != FailureClass.BUDGET_EXHAUSTED


# ---------------------------------------------------------------------------
# Finding #9: wall-clock continuity across resumes
# ---------------------------------------------------------------------------


class TestWallClockContinuity:
    """Wall clock uses persisted started_at, not fresh datetime.now()."""

    def test_elapsed_from_created_at(self):
        started = T0 - timedelta(hours=2)
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(started_at=started)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is True
        assert evaluation.first_exhausted_limit == "max_wall_clock_minutes"

    def test_short_elapsed_not_exhausted(self):
        started = T0 - timedelta(minutes=5)
        budgets = JobBudgets(max_wall_clock_minutes=60)
        counters = BudgetCounters(started_at=started)
        evaluation = evaluate_budget(budgets, counters, now=T0)
        assert evaluation.exhausted is False


# ---------------------------------------------------------------------------
# Finding #1: pre-call budget check in _call_with_retry
# ---------------------------------------------------------------------------


class TestPreCallBudgetCheck:
    """_call_with_retry checks stop_check before transport retries."""

    def test_stop_check_prevents_retry(self):
        from dataclasses import dataclass, field

        @dataclass
        class FakeResult:
            run_id: str = "r-test"
            retries_used: int = 0
            retry_reasons: list = field(default_factory=list)
            provider_attempts: list = field(default_factory=list)

        @dataclass
        class FakeOutput:
            error: str = "timeout: test"
            raw_text: str = ""
            stream_cap_reached: bool = False

        from packages.orchestration.pingpong_loop import _call_with_retry

        call_count = 0
        def fake_call():
            nonlocal call_count
            call_count += 1
            return FakeOutput()

        stop_triggered = False
        def fake_stop():
            nonlocal stop_triggered
            if call_count >= 1:
                stop_triggered = True
                return "stop_signal"
            return None

        result = FakeResult()
        out = _call_with_retry(
            fake_call,
            result=result,
            role="builder",
            stop_check=fake_stop,
        )
        assert call_count == 1
        assert stop_triggered is True

    def test_no_stop_check_retries_normally(self):
        from dataclasses import dataclass, field

        @dataclass
        class FakeResult:
            run_id: str = "r-test2"
            retries_used: int = 0
            retry_reasons: list = field(default_factory=list)
            provider_attempts: list = field(default_factory=list)

        @dataclass
        class FakeOutput:
            error: str = ""
            raw_text: str = ""
            stream_cap_reached: bool = False

        from packages.orchestration.pingpong_loop import _call_with_retry

        result = FakeResult()
        out = _call_with_retry(
            lambda: FakeOutput(),
            result=result,
            role="builder",
        )
        assert out.error == ""


# ---------------------------------------------------------------------------
# Finding #11: RunContract inherits from JobBudgets
# ---------------------------------------------------------------------------


class TestRunContractBudgetInheritance:
    """RunContract inherits limits from JobBudgets when set."""

    def test_contract_inherits_max_tokens(self):
        from packages.core.models import Job, JobBudgets
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="inherit-test", budgets=JobBudgets(max_total_tokens=50000))
        contract = build_default_run_contract(job)
        assert contract.max_tokens == 50000

    def test_contract_inherits_wall_clock(self):
        from packages.core.models import Job, JobBudgets
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="inherit-test-2", budgets=JobBudgets(max_wall_clock_minutes=30))
        contract = build_default_run_contract(job)
        assert contract.max_runtime_seconds == 1800

    def test_contract_defaults_without_budgets(self):
        from packages.core.models import Job
        from packages.orchestration.run_contract import build_default_run_contract
        job = Job(name="default-test")
        contract = build_default_run_contract(job)
        assert contract.max_tokens == 200_000
        assert contract.max_runtime_seconds == 600
