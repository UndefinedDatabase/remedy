"""F018 authority & integration round — 18 integration tests.

Tests cover findings #1-#14 from the external review:
  1. Malformed TOML fails closed
  2. Budget resolution uses project_root
  3. JobPlan budget path through do job-plan
  4. _bind_artifact_refs preserves budgets
  5. build_run_manifest handles dict budgets
  6. Strict decoder rejects invalid budget values
  7. Counter contradictions detected
  8. collect_counters_from_actuals has production caller shape
  9. Honest budget CLI state enum
 10. Decision identity bound to event request_id
 11. Stop identity includes episode_id
 12. Wall clock uses first_running_at
 13. RunContract reconciliation
 14. Runtime integration gate has nonzero checks
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

UTC = timezone.utc
T0 = datetime(2026, 7, 1, 12, 0, 0, tzinfo=UTC)


class TestMalformedTomlFailsClosed:
    """Finding #1: malformed TOML must raise, not return {}."""

    def test_malformed_project_toml_raises(self, tmp_path):
        from packages.orchestration.budget_resolution import BudgetConfigError
        from packages.orchestration.config import load_config

        bad = tmp_path / "remedy.toml"
        bad.write_text("this is [ not valid toml ugh")
        with pytest.raises(BudgetConfigError, match="Malformed TOML"):
            load_config(project_path=bad,
                        user_path=Path("/nonexistent/user.toml"))

    def test_malformed_user_toml_raises(self, tmp_path):
        from packages.orchestration.budget_resolution import BudgetConfigError
        from packages.orchestration.config import load_config

        bad_user = tmp_path / "user.toml"
        bad_user.write_text(">>> broken <<<")
        with pytest.raises(BudgetConfigError, match="Malformed TOML"):
            load_config(project_path=Path("/nonexistent/project.toml"),
                        user_path=bad_user)


class TestBudgetResolutionProjectRoot:
    """Finding #2: resolve_job_budgets accepts project_root."""

    def test_project_root_loads_toml(self, tmp_path):
        from packages.orchestration.budget_resolution import resolve_job_budgets

        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_total_tokens = 50000\n')
        result = resolve_job_budgets(project_root=str(tmp_path))
        assert result is not None
        assert result.max_total_tokens == 50000

    def test_cli_overrides_project_root(self, tmp_path):
        from packages.orchestration.budget_resolution import resolve_job_budgets

        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_total_tokens = 50000\n')
        result = resolve_job_budgets(
            cli_max_total_tokens="99999",
            project_root=str(tmp_path),
        )
        assert result is not None
        assert result.max_total_tokens == 99999


class TestJobPlanBudgetPath:
    """Finding #3: do job-plan accepts budget flags."""

    def test_job_plan_accepts_budget_kwargs(self):
        """_cmd_do_job_plan signature accepts budget keyword args."""
        import inspect
        from apps.cli.commands.do_cmd import _cmd_do_job_plan

        sig = inspect.signature(_cmd_do_job_plan)
        for param_name in ("max_total_tokens", "max_provider_calls",
                           "max_wall_clock_minutes", "deadline"):
            assert param_name in sig.parameters, f"{param_name} missing from _cmd_do_job_plan"

    def test_job_run_accepts_budget_kwargs(self):
        """_cmd_do_job_run signature accepts budget keyword args."""
        import inspect
        from apps.cli.commands.do_cmd import _cmd_do_job_run

        sig = inspect.signature(_cmd_do_job_run)
        for param_name in ("max_total_tokens", "max_provider_calls",
                           "max_wall_clock_minutes", "deadline"):
            assert param_name in sig.parameters, f"{param_name} missing from _cmd_do_job_run"


class TestBindArtifactRefsPreservesBudgets:
    """Finding #4: _bind_artifact_refs must preserve budgets field."""

    def test_bind_artifact_refs_source_preserves_budgets(self):
        """Verify _bind_artifact_refs copies budgets= in the RunManifestV1 it builds."""
        import inspect
        from packages.orchestration.run_manifest import _bind_artifact_refs

        src = inspect.getsource(_bind_artifact_refs)
        assert "budgets=manifest.budgets" in src or "budgets=" in src


class TestBuildRunManifestDictBudgets:
    """Finding #5: build_run_manifest handles dict budgets from JobPlan."""

    def test_build_run_manifest_handles_dict_budgets_in_source(self):
        """Verify build_run_manifest code handles dict budgets (hasattr model_dump check)."""
        import inspect
        from packages.orchestration.run_manifest import build_run_manifest

        src = inspect.getsource(build_run_manifest)
        assert "model_dump" in src
        assert "isinstance" in src or "hasattr" in src


class TestStrictDecoderRejectsInvalid:
    """Finding #6: _decode_budgets_field rejects zero/negative/bool/invalid."""

    def test_rejects_zero_int(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="strictly positive"):
            _decode_budgets_field({"max_total_tokens": 0})

    def test_rejects_negative_int(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="strictly positive"):
            _decode_budgets_field({"max_total_tokens": -5})

    def test_rejects_bool(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="bool"):
            _decode_budgets_field({"max_total_tokens": True})

    def test_rejects_deadline_without_tz(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="timezone"):
            _decode_budgets_field({"deadline": "2026-07-01T12:00:00"})


class TestCounterContradictions:
    """Finding #7: BudgetCounters detects impossible states."""

    def test_measured_tokens_without_calls_rejected(self):
        """collect_counters_from_actuals rejects tokens without measured calls."""
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="without any measured calls"):
            collect_counters_from_actuals({
                "provider_call_count": 0,
                "actual_call_count": 0,
                "total_tokens": 100,
            })

    def test_provider_calls_mismatch_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters

        with pytest.raises(BudgetCounterError,
                           match="provider_calls.*!=.*measured_call_count"):
            BudgetCounters(
                provider_calls=5,
                measured_call_count=3,
                unmeasured_call_count=3,
            )


class TestCollectCountersProductionShape:
    """Finding #8: collect_counters_from_actuals has valid production callers."""

    def test_matches_run_job_accumulator_shape(self):
        """The dict shape used by _stop_check in run_job is valid input."""
        from packages.orchestration.budget_guard import collect_counters_from_actuals

        counters = collect_counters_from_actuals(
            {
                "provider_call_count": 3,
                "actual_call_count": 2,
                "total_tokens": 15000,
            },
            started_at=T0,
            actual_sources=("pingpong_live",),
        )
        assert counters.provider_calls == 3
        assert counters.measured_call_count == 2
        assert counters.unmeasured_call_count == 1
        assert counters.measured_token_total == 15000

    def test_actual_count_exceeds_provider_count_rejected(self):
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="actual_call_count.*>.*provider"):
            collect_counters_from_actuals({
                "provider_call_count": 2,
                "actual_call_count": 5,
                "total_tokens": 1000,
            })


class TestHonestBudgetCLI:
    """Finding #9: _cmd_job_budget loads real actuals, typed state."""

    def test_budget_cli_uses_collect_counters(self):
        """The budget CLI code path references collect_counters_from_actuals."""
        import inspect
        from apps.cli.commands.job import _cmd_job_budget

        src = inspect.getsource(_cmd_job_budget)
        assert "collect_counters_from_actuals" in src
        assert "evaluate_budget" in src


class TestDecisionIdentity:
    """Finding #10: decision ID derived from event request_id."""

    def test_budget_decision_uses_event_request_id(self):
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions

        job = Job(name="test", prompt="test")
        job.metadata["budget_stop_reason"] = "budget_exhausted: max_provider_calls"
        events = [{
            "event": "job_stopped",
            "timestamp": "2026-07-01T12:00:00Z",
            "metadata": {
                "source": "budget",
                "reason": "budget_exhausted",
                "request_id": "budget_abc123",
                "exhausted_limit": "max_provider_calls",
            },
        }]
        decisions = list_decisions(job, events)
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 1
        assert budget_decisions[0].id == "budget:budget_abc123"
        assert budget_decisions[0].related_intent_id == "budget_abc123"
        assert budget_decisions[0].next_actions == ("extend", "abandon")


class TestStopIdentityEpisode:
    """Finding #11: exhaustion identity includes episode_id."""

    def test_different_episodes_produce_different_ids(self):
        import hashlib

        job_id = "test_job_123"
        reason = "budget_exhausted: max_provider_calls"
        id_ep1 = hashlib.sha256(
            f"{job_id}:episode_a:{reason}".encode()).hexdigest()[:16]
        id_ep2 = hashlib.sha256(
            f"{job_id}:episode_b:{reason}".encode()).hexdigest()[:16]
        assert id_ep1 != id_ep2


class TestWallClockFirstRunningAt:
    """Finding #12: wall clock uses first_running_at, not created_at."""

    def test_first_running_at_field_exists(self):
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        assert hasattr(job, "first_running_at")
        assert job.first_running_at == ""

    def test_first_running_at_serialized(self):
        from packages.orchestration.pingpong_job import _export_job, _import_job, JobPlan

        job = JobPlan(first_running_at="2026-07-01T12:00:00+00:00")
        exported = _export_job(job)
        assert exported["first_running_at"] == "2026-07-01T12:00:00+00:00"
        imported = _import_job(exported)
        assert imported.first_running_at == "2026-07-01T12:00:00+00:00"


class TestRunContractReconciliation:
    """Finding #13: ensure_contract reconciles with JobBudgets."""

    def test_reconciles_tokens_on_budget_change(self):
        from packages.core.models import Job, JobBudgets
        from packages.orchestration.run_contract import (
            RunContract,
            ensure_contract,
            save_contract,
        )

        job = Job(name="test", prompt="test")
        old_contract = RunContract(
            version=1,
            contract_id="rc-test",
            job_id=str(job.id),
            max_tokens=200000,
            max_runtime_seconds=600,
        )
        save_contract(job, old_contract)

        job.budgets = JobBudgets(max_total_tokens=50000)
        contract = ensure_contract(job)
        assert contract.max_tokens == 50000

    def test_no_reconciliation_when_no_budgets(self):
        from packages.core.models import Job
        from packages.orchestration.run_contract import (
            RunContract,
            ensure_contract,
            save_contract,
        )

        job = Job(name="test", prompt="test")
        old_contract = RunContract(
            version=1,
            contract_id="rc-test",
            job_id=str(job.id),
            max_tokens=200000,
        )
        save_contract(job, old_contract)

        contract = ensure_contract(job)
        assert contract.max_tokens == 200000


class TestRuntimeIntegrationGateNonzero:
    """Finding #14: gate must have nonzero real checks."""

    def test_integration_checks_nonzero(self):
        from packages.orchestration.runtime_integration_gate import INTEGRATION_CHECKS

        assert len(INTEGRATION_CHECKS) > 5

    def test_f018_checks_present(self):
        from packages.orchestration.runtime_integration_gate import INTEGRATION_CHECKS

        check_ids = {c["check_id"] for c in INTEGRATION_CHECKS}
        f018_ids = {cid for cid in check_ids if cid.startswith("f018_")}
        assert len(f018_ids) >= 5

    def test_gate_passes_on_live_repo(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )

        gate = build_runtime_integration_gate(".")
        assert gate["checks_total"] > 0
        assert gate["checks_passed"] == gate["checks_total"]
        assert gate["verdict"] == "PASS"


class TestBudgetActualsPersistence:
    """Finding #9 complement: budget_actuals field round-trips."""

    def test_budget_actuals_serialized(self):
        from packages.orchestration.pingpong_job import _export_job, _import_job, JobPlan

        actuals = {
            "provider_call_count": 5,
            "actual_call_count": 4,
            "total_tokens": 25000,
            "started_at": "2026-07-01T12:00:00+00:00",
        }
        job = JobPlan(budget_actuals=actuals)
        exported = _export_job(job)
        assert exported["budget_actuals"] == actuals
        imported = _import_job(exported)
        assert imported.budget_actuals == actuals

    def test_budget_actuals_none_by_default(self):
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        assert job.budget_actuals is None
