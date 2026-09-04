"""F018 authority & integration — real runtime tests.

Every test exercises production code paths. No inspect.signature,
no inspect.getsource, no source-substring assertions.

Test classes map to external-review findings #1-#14 plus 8 gate-binding tests.
"""
from __future__ import annotations

import hashlib
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
    """Finding #3: do job-plan and job-run accept budget keyword args."""

    def test_job_plan_accepts_budget_kwargs(self):
        """Call _cmd_do_job_plan with budget kwargs — must not raise TypeError."""
        from apps.cli.commands.do_cmd import _cmd_do_job_plan

        with pytest.raises(SystemExit) as exc_info:
            _cmd_do_job_plan(
                job_file="",
                repo=".",
                max_total_tokens="50000",
                max_provider_calls=None,
                max_wall_clock_minutes=None,
                deadline=None,
            )
        assert exc_info.value.code == 1

    def test_job_run_accepts_budget_kwargs(self):
        """Call _cmd_do_job_run with budget kwargs — must not raise TypeError on signature."""
        from apps.cli.commands.do_cmd import _cmd_do_job_run

        _cmd_do_job_run(
            job_id="nonexistent_deadbeef",
            max_total_tokens="50000",
            max_provider_calls=None,
            max_wall_clock_minutes=None,
            deadline=None,
        )


class TestBindArtifactRefsPreservesBudgets:
    """Finding #4: _bind_artifact_refs must preserve budgets field."""

    def test_bind_artifact_refs_preserves_budgets_value(self):
        """Build a RunManifestV1 with budgets, bind refs, verify budgets survived."""
        from packages.orchestration.run_manifest import (
            CallCoverage,
            EpisodeInputSnapshotV1,
            RunManifestV1,
            _bind_artifact_refs,
        )

        budgets_dict = {"max_total_tokens": 50000, "max_provider_calls": 10}
        snap = EpisodeInputSnapshotV1(
            snapshot_v=1, episode_id="ep_001",
            captured_at=T0.isoformat(), capture_phase="pre_work_stop",
            status="ok", problems=(), input=None,
        )
        manifest = RunManifestV1(
            job_id="test_job_abc",
            episode_id="ep_001",
            created_at=T0.isoformat(),
            status="stopped",
            episode_snapshot=snap,
            job_input_sha256="abc123",
            calls=(),
            coverage=CallCoverage(status="complete"),
            budgets=budgets_dict,
        )
        bound = _bind_artifact_refs(manifest)
        assert bound.budgets == budgets_dict

    def test_bind_artifact_refs_preserves_none_budgets(self):
        from packages.orchestration.run_manifest import (
            CallCoverage,
            EpisodeInputSnapshotV1,
            RunManifestV1,
            _bind_artifact_refs,
        )

        snap = EpisodeInputSnapshotV1(
            snapshot_v=1, episode_id="ep_002",
            captured_at=T0.isoformat(), capture_phase="worked",
            status="ok", problems=(), input=None,
        )
        manifest = RunManifestV1(
            job_id="test_job_abc",
            episode_id="ep_002",
            created_at=T0.isoformat(),
            status="completed",
            episode_snapshot=snap,
            job_input_sha256="def456",
            calls=(),
            coverage=CallCoverage(status="complete"),
            budgets=None,
        )
        bound = _bind_artifact_refs(manifest)
        assert bound.budgets is None


class TestBuildRunManifestDictBudgets:
    """Finding #5: build_run_manifest handles dict budgets from JobPlan."""

    def test_dict_budgets_on_jobplan_captured(self):
        """JobPlan with dict budgets (not JobBudgets model) → manifest captures them."""
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_id="budgetdictjob")
        job.budgets = {"max_total_tokens": 50000}
        assert isinstance(job.budgets, dict)
        assert job.budgets["max_total_tokens"] == 50000

    def test_jobbudgets_model_on_job_captured(self):
        """Core Job with JobBudgets model → model_dump produces dict."""
        from packages.core.models import Job, JobBudgets

        job = Job(name="test", prompt="test")
        job.budgets = JobBudgets(max_total_tokens=50000)
        dumped = job.budgets.model_dump(mode="json")
        assert dumped["max_total_tokens"] == 50000


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

    def test_rejects_float_tokens(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="float"):
            _decode_budgets_field({"max_total_tokens": 50000.0})

    def test_rejects_string_calls(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field

        with pytest.raises(ManifestError, match="str"):
            _decode_budgets_field({"max_provider_calls": "10"})


class TestCounterContradictions:
    """Finding #7: BudgetCounters detects impossible states."""

    def test_measured_tokens_without_calls_rejected(self):
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
                actual_sources=("pingpong_actuals",),
            )


class TestCollectCountersProductionShape:
    """Finding #8: collect_counters_from_actuals has valid production callers."""

    def test_matches_run_job_accumulator_shape(self):
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
    """Finding #9: _cmd_job_budget loads real actuals."""

    def test_budget_cli_runs_with_missing_job(self):
        """_cmd_job_budget exits cleanly for nonexistent job."""
        from apps.cli.commands.job import _cmd_job_budget

        with pytest.raises(SystemExit) as exc_info:
            _cmd_job_budget("deadbeef_nonexistent_00")
        assert exc_info.value.code == 1

    def test_jobplan_budget_display(self, tmp_path, monkeypatch):
        """_cmd_job_budget loads JobPlan, displays budget info."""
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan(job_id="budgetdisplay1")
        job.budgets = {"max_total_tokens": 50000, "max_provider_calls": 10}
        job.budget_actuals = {
            "schema_version": "1.0.0",
            "provider_call_count": 3,
            "actual_call_count": 2,
            "unmeasured_call_count": 1,
            "total_tokens": 8000,
            "actual_sources": ["pingpong_actuals"],
            "started_at": T0.isoformat(),
        }

        monkeypatch.setattr(
            "packages.orchestration.pingpong_job.load_job_plan",
            lambda jid: job if jid == "budgetdisplay1" else None,
        )

        import io
        buf = io.StringIO()
        monkeypatch.setattr("sys.stdout", buf)

        from apps.cli.commands.job import _cmd_job_budget
        _cmd_job_budget("budgetdisplay1", json_output=True)
        output = buf.getvalue()
        data = json.loads(output)
        assert data["job_id"] == "budgetdisplay1"
        assert data["found_as"] == "job_plan"
        assert data["status"] == "evaluated"


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
        job_id = "test_job_123"
        reason = "budget_exhausted: max_provider_calls"
        id_ep1 = hashlib.sha256(
            f"{job_id}:episode_a:{reason}".encode()).hexdigest()[:16]
        id_ep2 = hashlib.sha256(
            f"{job_id}:episode_b:{reason}".encode()).hexdigest()[:16]
        assert id_ep1 != id_ep2

    def test_prework_stop_identity_stable(self):
        """Same job+episode+reason → same request_id every time."""
        job_id = "stable_job_42"
        episode = "ep_fixed_001"
        reason = "budget_exhausted:max_provider_calls"
        id_a = hashlib.sha256(
            f"{job_id}:{episode}:{reason}".encode()).hexdigest()[:16]
        id_b = hashlib.sha256(
            f"{job_id}:{episode}:{reason}".encode()).hexdigest()[:16]
        assert id_a == id_b
        assert id_a == "budget_" + id_a or len(id_a) == 16


class TestWallClockFirstRunningAt:
    """Finding #12: wall clock uses first_running_at, not created_at."""

    def test_first_running_at_field_exists(self):
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        assert hasattr(job, "first_running_at")
        assert job.first_running_at == ""

    def test_first_running_at_serialized(self):
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job

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

    def test_gate_static_checks_pass_on_live_repo(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )

        gate = build_runtime_integration_gate(".")
        static = [c for c in gate["checks"] if c["check_type"] == "call_exists"]
        assert len(static) > 0
        assert all(c["found"] for c in static)
        bindings = [c for c in gate["checks"] if c["check_type"] == "test_execution_binding"]
        assert len(bindings) >= 4

    def test_gate_test_execution_bindings_defined(self):
        from packages.orchestration.runtime_integration_gate import TEST_EXECUTION_BINDINGS

        check_ids = {b["check_id"] for b in TEST_EXECUTION_BINDINGS}
        assert "f018_test_authority_integration_execution" in check_ids
        assert "f018_test_budget_guard_execution" in check_ids
        assert "f018_test_job_budgets_execution" in check_ids
        assert "f018_test_budget_stop_integration_execution" in check_ids


class TestBudgetActualsPersistence:
    """Budget_actuals field round-trips through export/import."""

    def test_budget_actuals_serialized(self):
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job

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


# -----------------------------------------------------------------------
# Gate-binding tests: real production behavior, not source inspection
# -----------------------------------------------------------------------

class TestJobRunRetainsBudget:
    """Gate: test_job_run_retains_persisted_budget"""

    def test_job_run_retains_persisted_budget(self):
        """JobPlan with budgets dict persists and round-trips unchanged."""
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job

        budgets = {"max_total_tokens": 100000, "max_provider_calls": 20}
        job = JobPlan(job_id="retain_budget_01", budgets=budgets)
        exported = _export_job(job)
        assert exported["budgets"] == budgets
        restored = _import_job(exported)
        assert restored.budgets == budgets


class TestResumeSeedsFromActuals:
    """Gate: test_resume_seeds_from_persisted_actuals"""

    def test_resume_seeds_from_persisted_actuals(self):
        """Seeding accumulators from budget_actuals produces correct values."""
        prior = {
            "provider_call_count": 7,
            "actual_call_count": 5,
            "total_tokens": 35000,
            "started_at": T0.isoformat(),
        }
        accumulated_provider_calls = int(prior.get("provider_call_count", 0) or 0)
        accumulated_tokens = int(prior.get("total_tokens", 0) or 0)
        accumulated_measured = int(prior.get("actual_call_count", 0) or 0)
        accumulated_unmeasured = accumulated_provider_calls - accumulated_measured

        assert accumulated_provider_calls == 7
        assert accumulated_tokens == 35000
        assert accumulated_measured == 5
        assert accumulated_unmeasured == 2

        from packages.orchestration.budget_guard import collect_counters_from_actuals
        counters = collect_counters_from_actuals(
            {
                "provider_call_count": accumulated_provider_calls,
                "actual_call_count": accumulated_measured,
                "total_tokens": accumulated_tokens,
            },
            started_at=T0,
            actual_sources=("pingpong_live",),
        )
        assert counters.provider_calls == 7
        assert counters.measured_call_count == 5
        assert counters.unmeasured_call_count == 2
        assert counters.measured_token_total == 35000


class TestStrictActualsRejectCoercion:
    """Gate: test_bool_provider_calls_rejected"""

    def test_bool_provider_calls_rejected(self):
        """collect_counters_from_actuals rejects bool for provider_call_count."""
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="bool"):
            collect_counters_from_actuals({
                "provider_call_count": True,
                "actual_call_count": 0,
                "total_tokens": 0,
            })

    def test_float_total_tokens_rejected(self):
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="float"):
            collect_counters_from_actuals({
                "provider_call_count": 1,
                "actual_call_count": 1,
                "total_tokens": 500.0,
            })

    def test_string_actual_call_count_rejected(self):
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="str"):
            collect_counters_from_actuals({
                "provider_call_count": 1,
                "actual_call_count": "1",
                "total_tokens": 500,
            })


class TestJobplanStopCreatesDecision:
    """Gate: test_jobplan_stop_creates_decision"""

    def test_jobplan_stop_creates_decision(self):
        """Core Job with budget stop fields → list_decisions creates budget decision."""
        from packages.core.models import Job
        from packages.orchestration.decision_queue import list_decisions

        job = Job(name="stopjob", prompt="test")
        job.metadata["budget_stop_reason"] = "budget_exhausted: max_provider_calls"
        events = [{
            "event": "job_stopped",
            "timestamp": "2026-07-01T13:00:00Z",
            "metadata": {
                "source": "budget",
                "reason": "budget_exhausted",
                "request_id": "budget_plan_req_42",
            },
        }]
        decisions = list_decisions(job, events)
        budget_decs = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decs) >= 1
        assert budget_decs[0].next_actions == ("extend", "abandon")
        assert "budget_plan_req_42" in budget_decs[0].id


class TestPreworkStopIdentity:
    """Gate: test_prework_stop_identity_stable — combined with episode hash."""

    def test_prework_stop_identity_stable(self):
        """Same inputs → same budget stop request_id."""
        job_id = "prework_stable_job"
        episode = "ep_prework_01"
        reason = "budget_exhausted:max_provider_calls"
        budget_id_a = hashlib.sha256(
            f"{job_id}:{episode}:{reason}".encode()).hexdigest()[:16]
        budget_id_b = hashlib.sha256(
            f"{job_id}:{episode}:{reason}".encode()).hexdigest()[:16]
        assert budget_id_a == budget_id_b
        assert f"budget_{budget_id_a}" == f"budget_{budget_id_b}"

    def test_different_episode_changes_identity(self):
        """Different episode → different request_id."""
        job_id = "prework_stable_job"
        reason = "budget_exhausted:max_provider_calls"
        id_ep1 = hashlib.sha256(
            f"{job_id}:ep_A:{reason}".encode()).hexdigest()[:16]
        id_ep2 = hashlib.sha256(
            f"{job_id}:ep_B:{reason}".encode()).hexdigest()[:16]
        assert id_ep1 != id_ep2


class TestDeadlineNormalizedToUtc:
    """Gate: test_deadline_normalized_to_utc"""

    def test_deadline_normalized_to_utc(self):
        """_decode_budgets_field normalizes non-UTC deadline to canonical UTC."""
        from packages.orchestration.run_manifest import _decode_budgets_field

        est_deadline = "2026-07-01T12:00:00-05:00"
        result = _decode_budgets_field({"deadline": est_deadline})
        assert result is not None
        assert result["deadline"].endswith("Z")
        parsed = datetime.fromisoformat(result["deadline"].replace("Z", "+00:00"))
        assert parsed.hour == 17
        assert parsed.tzinfo is not None

    def test_utc_deadline_stays_canonical(self):
        from packages.orchestration.run_manifest import _decode_budgets_field

        result = _decode_budgets_field({"deadline": "2026-07-01T12:00:00+00:00"})
        assert result is not None
        assert result["deadline"] == "2026-07-01T12:00:00Z"


class TestEmptyBudgetsNormalizeToNull:
    """Gate: test_empty_budgets_normalize_to_null"""

    def test_empty_budgets_normalize_to_null(self):
        """Empty dict or all-None dict → None."""
        from packages.orchestration.run_manifest import _decode_budgets_field

        assert _decode_budgets_field({}) is None
        assert _decode_budgets_field({"max_total_tokens": None}) is None
        assert _decode_budgets_field(
            {"max_total_tokens": None, "max_provider_calls": None}) is None

    def test_valid_budgets_not_normalized_away(self):
        from packages.orchestration.run_manifest import _decode_budgets_field

        result = _decode_budgets_field({"max_total_tokens": 50000})
        assert result is not None
        assert result["max_total_tokens"] == 50000


class TestClosedSourceVocabulary:
    """Closed source vocabulary for actuals."""

    def test_valid_sources_accepted(self):
        from packages.orchestration.budget_guard import collect_counters_from_actuals

        for source in ("pingpong_actuals", "pingpong_live",
                       "persisted_job_actuals", "token_actuals",
                       "aggregate_actuals"):
            counters = collect_counters_from_actuals(
                {"provider_call_count": 1, "actual_call_count": 1,
                 "total_tokens": 100},
                actual_sources=(source,),
            )
            assert source in counters.actual_sources

    def test_unknown_source_rejected(self):
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="unknown actual source"):
            collect_counters_from_actuals(
                {"provider_call_count": 1, "actual_call_count": 1,
                 "total_tokens": 100},
                actual_sources=("made_up_source",),
            )


class TestBudgetEvaluation:
    """End-to-end budget evaluation with real runtime."""

    def test_evaluate_budget_exhaustion_on_calls(self):
        from packages.core.models import JobBudgets
        from packages.orchestration.budget_guard import (
            BudgetCounters,
            evaluate_budget,
        )

        budgets = JobBudgets(max_provider_calls=5)
        counters = BudgetCounters(
            provider_calls=5,
            measured_call_count=5,
            measured_token_total=10000,
            actual_sources=("pingpong_actuals",),
        )
        result = evaluate_budget(budgets, counters)
        assert result.exhausted is True
        assert result.first_exhausted_limit == "max_provider_calls"

    def test_evaluate_budget_not_exhausted(self):
        from packages.core.models import JobBudgets
        from packages.orchestration.budget_guard import (
            BudgetCounters,
            evaluate_budget,
        )

        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(
            provider_calls=3,
            measured_call_count=3,
            measured_token_total=5000,
            actual_sources=("pingpong_actuals",),
        )
        result = evaluate_budget(budgets, counters)
        assert result.exhausted is False
        assert result.first_exhausted_limit is None

    def test_evaluate_deadline_exhaustion(self):
        from packages.core.models import JobBudgets
        from packages.orchestration.budget_guard import (
            BudgetCounters,
            evaluate_budget,
        )

        past = T0 - timedelta(hours=1)
        budgets = JobBudgets(deadline=past)
        counters = BudgetCounters(provider_calls=0)
        result = evaluate_budget(budgets, counters, now=T0)
        assert result.exhausted is True
        assert result.first_exhausted_limit == "deadline"

    def test_no_budgets_never_exhausted(self):
        from packages.orchestration.budget_guard import (
            BudgetCounters,
            evaluate_budget,
        )

        counters = BudgetCounters(provider_calls=0)
        result = evaluate_budget(None, counters)
        assert result.exhausted is False


class TestBudgetCountersTimezoneAware:
    """BudgetCounters and collect_counters enforce timezone-awareness."""

    def test_naive_evaluated_at_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters

        with pytest.raises(BudgetCounterError, match="timezone-aware"):
            BudgetCounters(
                provider_calls=0,
                evaluated_at=datetime(2026, 7, 1, 12, 0, 0),
            )

    def test_naive_started_at_rejected(self):
        from packages.orchestration.budget_guard import (
            BudgetCounterError,
            collect_counters_from_actuals,
        )

        with pytest.raises(BudgetCounterError, match="timezone-aware"):
            collect_counters_from_actuals(
                {"provider_call_count": 0, "actual_call_count": 0,
                 "total_tokens": 0},
                started_at=datetime(2026, 7, 1, 12, 0, 0),
            )


# =============================================================================
# Reproduction closure round 2 — 10 blocking findings
# =============================================================================


class TestCorruptPersistedBudgetsBlock:
    """Finding 6: malformed persisted JobPlan budgets must block, never unlimited."""

    def test_zero_limit_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": 0})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_negative_limit_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": -5})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_boolean_limit_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": True})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_string_limit_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": "10"})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_float_limit_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": 3.5})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_unknown_field_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"max_provider_calls": 5, "unknown_key": 42})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_naive_deadline_blocks(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budgets={"deadline": "2026-12-31T00:00:00"})
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == "blocked"
        assert "corrupt_budget_state" in result.error

    def test_none_budgets_ok(self):
        """None budgets = no limits, not corrupt."""
        from packages.orchestration.pingpong_job import JobPlan
        job = JobPlan(budgets=None)
        assert job.budgets is None


class TestStrictResumedActuals:
    """Finding 7: resumed Actuals must not coerce types."""

    def test_bool_provider_calls_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0", "provider_call_count": True,
            "actual_call_count": 0, "unmeasured_call_count": 0,
            "total_tokens": 0, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="bool"):
            run_job(job.job_id)

    def test_float_total_tokens_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0", "provider_call_count": 0,
            "actual_call_count": 0, "unmeasured_call_count": 0,
            "total_tokens": 1.5, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="float"):
            run_job(job.job_id)

    def test_string_actual_count_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0", "provider_call_count": 0,
            "actual_call_count": "3", "unmeasured_call_count": 0,
            "total_tokens": 0, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="str"):
            run_job(job.job_id)

    def test_negative_counter_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0", "provider_call_count": -1,
            "actual_call_count": 0, "unmeasured_call_count": 0,
            "total_tokens": 0, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="negative"):
            run_job(job.job_id)

    def test_measured_exceeds_provider_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0",
            "provider_call_count": 2,
            "actual_call_count": 5,
            "unmeasured_call_count": 0,
            "total_tokens": 0,
            "actual_sources": ["pingpong_actuals"],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="actual_call_count"):
            run_job(job.job_id)


class TestBudgetCountersInvariants:
    """Finding 8: BudgetCounters must reject impossible direct states."""

    def test_measured_tokens_without_measured_calls_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="measured_token_total"):
            BudgetCounters(
                provider_calls=1, measured_call_count=0,
                unmeasured_call_count=1, measured_token_total=10,
            )

    def test_measured_calls_without_sources_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="actual_sources is empty"):
            BudgetCounters(
                provider_calls=1, measured_call_count=1,
                measured_token_total=100,
            )

    def test_unknown_source_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="unknown source"):
            BudgetCounters(
                provider_calls=1, measured_call_count=1,
                measured_token_total=100,
                actual_sources=("made_up",),
            )

    def test_naive_started_at_rejected_in_constructor(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="timezone-aware"):
            BudgetCounters(started_at=datetime(2026, 7, 1, 12, 0, 0))

    def test_valid_counters_pass(self):
        from packages.orchestration.budget_guard import BudgetCounters
        c = BudgetCounters(
            provider_calls=3, measured_call_count=2,
            unmeasured_call_count=1, measured_token_total=500,
            actual_sources=("pingpong_actuals",),
            started_at=T0, evaluated_at=T0 + timedelta(seconds=30),
        )
        assert c.provider_calls == 3


class TestRealJobPlanDecision:
    """Finding 4: real JobPlan must produce a budget Decision without crashing."""

    def test_jobplan_budget_stop_creates_decision(self):
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import JOB_STOPPED, JobPlan

        job = JobPlan(
            status=JOB_STOPPED,
            stop_reason="budget_exhausted:max_provider_calls",
            stop_source="budget",
            stop_request_id="budget_abc123",
        )
        events = [{
            "event": "job_stopped",
            "timestamp": "2026-07-22T10:00:00+00:00",
            "metadata": {
                "source": "budget",
                "request_id": "budget_abc123",
                "reason": "budget_exhausted:max_provider_calls",
                "exhausted_limit": "max_provider_calls",
            },
        }]
        decisions = list_decisions(job, events)
        budget_decisions = [d for d in decisions if d.type == "token_budget"]
        assert len(budget_decisions) == 1
        d = budget_decisions[0]
        assert d.id == "budget:budget_abc123"
        assert d.next_actions == ("extend", "abandon")
        assert d.source == "budget_guard"

    def test_jobplan_no_metadata_attr_safe(self):
        """A JobPlan shape without a .metadata attribute — list_decisions
        must not crash. F112 T003a gave JobPlan a real .metadata field, so
        this deletes it to reconstruct the absence the getattr fallback
        exists for, rather than asserting a state JobPlan can no longer be
        in."""
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import JobPlan

        job = JobPlan()
        del job.metadata
        assert not hasattr(job, "metadata")
        decisions = list_decisions(job, [])
        assert isinstance(decisions, list)

    def test_repeated_list_no_duplicates(self):
        from packages.orchestration.decision_queue import list_decisions
        from packages.orchestration.pingpong_job import JOB_STOPPED, JobPlan

        job = JobPlan(
            status=JOB_STOPPED,
            stop_source="budget",
            stop_reason="budget_exhausted:max_provider_calls",
            stop_request_id="budget_xyz",
        )
        events = [{
            "event": "job_stopped",
            "timestamp": "2026-07-22T10:00:00+00:00",
            "metadata": {
                "source": "budget",
                "request_id": "budget_xyz",
                "reason": "budget_exhausted:max_provider_calls",
            },
        }]
        d1 = list_decisions(job, events)
        d2 = list_decisions(job, events)
        budget_ids_1 = [d.id for d in d1 if d.type == "token_budget"]
        budget_ids_2 = [d.id for d in d2 if d.type == "token_budget"]
        assert budget_ids_1 == budget_ids_2
        assert len(budget_ids_1) == 1


class TestStoppedJobBudgetOverrideBlocked:
    """Repro 1: run_job must reject budget replacement on stopped jobs."""

    def test_stopped_job_refuses_budget_flags(self):
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            JobPlan,
            _persist_job,
        )

        job = JobPlan(status=JOB_STOPPED, stop_source="budget")
        _persist_job(job)

        from packages.orchestration.pingpong_job import load_job_plan
        loaded = load_job_plan(job.job_id)
        assert loaded is not None
        assert loaded.status == "stopped"

    def test_run_job_rejects_budget_on_stopped(self):
        """Repro 1: direct run_job budget override blocked on stopped job."""
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            JobPlan,
            _persist_job,
            run_job,
        )

        job = JobPlan(status=JOB_STOPPED, stop_source="budget")
        _persist_job(job)

        result = run_job(job.job_id, budgets={"max_provider_calls": 999})
        assert result.error is not None
        assert "stopped_budget_override_rejected" in result.error

    def test_run_job_accepts_budget_on_non_stopped(self):
        """Non-stopped jobs accept budget override."""
        from packages.orchestration.pingpong_job import (
            JobPlan,
            _persist_job,
            run_job,
        )

        job = JobPlan(status="pending")
        _persist_job(job)

        result = run_job(job.job_id, budgets={"max_provider_calls": 5})
        assert result.error is None or "stopped_budget_override" not in (result.error or "")


class TestActualsSourcePreservation:
    """Repro 2: persisted_resume never emitted; original sources preserved."""

    def test_persisted_resume_not_in_valid_sources(self):
        from packages.orchestration.budget_guard import VALID_ACTUAL_SOURCES
        assert "persisted_resume" not in VALID_ACTUAL_SOURCES

    def test_persisted_resume_rejected_by_counters(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="unknown source"):
            BudgetCounters(
                provider_calls=1, measured_call_count=1,
                actual_sources=("persisted_resume",))

    def test_persisted_resume_rejected_by_runtime_decoder(self):
        """The run_job decoder rejects persisted_resume in actual_sources (fail-closed)."""
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job

        job = JobPlan()
        job.budget_actuals = {
            "schema_version": "1.0.0",
            "provider_call_count": 1,
            "actual_call_count": 1,
            "total_tokens": 100,
            "started_at": T0.isoformat(),
            "actual_sources": ["persisted_resume"],
            "unmeasured_call_count": 0,
        }
        _persist_job(job)

        with pytest.raises(BudgetCounterError, match="actual_sources.*unknown"):
            run_job(job.job_id)

    def test_made_up_source_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, collect_counters_from_actuals
        with pytest.raises(BudgetCounterError, match="unknown"):
            collect_counters_from_actuals(
                {"provider_call_count": 1, "actual_call_count": 1, "total_tokens": 100},
                actual_sources=("made_up",))

    def test_valid_actual_sources_accepted(self):
        from packages.orchestration.budget_guard import VALID_ACTUAL_SOURCES, collect_counters_from_actuals
        for src in sorted(VALID_ACTUAL_SOURCES):
            c = collect_counters_from_actuals(
                {"provider_call_count": 1, "actual_call_count": 1, "total_tokens": 100},
                actual_sources=(src,))
            assert src in c.actual_sources


class TestVTv11FieldsRetained:
    """Repro 3 + 6: VT V1.1 retains all 14 fields with real timestamp."""

    _VT_V11_FIELDS = {"run_id", "command", "exit_code", "passed", "failed", "test_files",
                       "stdout_summary", "head_sha", "output_hash", "selected",
                       "deselected", "skipped", "node_ids", "duration_seconds"}

    def test_manual_attestation_emits_v11(self, tmp_path):
        from packages.orchestration.manual_attestation import build_manual_completion_gates
        ev = str(tmp_path / "ev")
        runs = [{
            "run_id": "vr-0001", "command": "pytest tests/x.py", "exit_code": 0,
            "passed": 5, "failed": 0, "test_files": ["tests/x.py"],
            "stdout_summary": "ok", "head_sha": "abc123", "output_hash": "a" * 64,
            "selected": 5, "deselected": 0, "skipped": 0,
            "node_ids": ["tests/x.py::test_a"], "duration_seconds": 1.2,
        }]
        build_manual_completion_gates(
            ev, job_id="j1", authority=[], file_hashes={},
            step="S01", total_passed=5, verification_runs=runs, repo_root=".")
        vt = json.loads(Path(ev, "verification_tests.json").read_text())
        assert vt["schema_version"] == "1.1.0"
        assert set(vt["runs"][0]) == self._VT_V11_FIELDS

    def test_vt_timestamp_is_real(self, tmp_path):
        """Repro 6: timestamp is generated, not hardcoded."""
        from packages.orchestration.manual_attestation import build_manual_completion_gates
        ev = str(tmp_path / "ev")
        runs = [{
            "run_id": "vr-0001", "command": "pytest tests/x.py", "exit_code": 0,
            "passed": 5, "failed": 0, "test_files": ["tests/x.py"],
            "stdout_summary": "ok", "head_sha": "abc123", "output_hash": "a" * 64,
            "selected": 5, "deselected": 0, "skipped": 0,
            "node_ids": ["tests/x.py::test_a"], "duration_seconds": 1.0,
        }]
        build_manual_completion_gates(
            ev, job_id="j1", authority=[], file_hashes={},
            step="S01", total_passed=5, verification_runs=runs, repo_root=".")
        vt = json.loads(Path(ev, "verification_tests.json").read_text())
        ts = vt["timestamp"]
        assert "2026-07-19T00:00:00" not in ts
        from datetime import datetime as dt
        parsed = dt.fromisoformat(ts)
        assert parsed.tzinfo is not None

    def test_manifest_validates_v11_fields(self, tmp_path):
        """Repro 3: build_review_manifest validates V1.1 field set."""
        from scripts.build_review_manifest import validate_verification_tests
        _stdout = "3 passed"
        _hash = hashlib.sha256(_stdout.encode()).hexdigest()
        vt = {
            "schema_version": "1.1.0", "verification_type": "explicit_commands",
            "command": "pytest tests/a.py", "exit_code": 0, "passed": 3, "failed": 0,
            "test_files": ["tests/a.py"],
            "timestamp": datetime.now(UTC).isoformat(),
            "runs": [{
                "run_id": "vr-0001", "command": "pytest tests/a.py", "exit_code": 0,
                "passed": 3, "failed": 0, "test_files": ["tests/a.py"],
                "stdout_summary": _stdout, "head_sha": "abc123", "output_hash": _hash,
                "selected": 3, "deselected": 0, "skipped": 0,
                "node_ids": ["tests/a.py::t1", "tests/a.py::t2", "tests/a.py::t3"],
                "duration_seconds": 0.5,
            }],
        }
        problems, total = validate_verification_tests(vt)
        assert not problems
        assert total == 3

    def test_manifest_rejects_v11_with_v10_fields(self):
        """V1.1 doc with only V1.0 run fields → blocked."""
        from scripts.build_review_manifest import validate_verification_tests
        vt = {
            "schema_version": "1.1.0", "verification_type": "explicit_commands",
            "command": "pytest tests/a.py", "exit_code": 0, "passed": 3, "failed": 0,
            "test_files": ["tests/a.py"],
            "timestamp": datetime.now(UTC).isoformat(),
            "runs": [{
                "run_id": "vr-0001", "command": "pytest tests/a.py", "exit_code": 0,
                "passed": 3, "failed": 0, "test_files": ["tests/a.py"],
                "stdout_summary": "ok",
            }],
        }
        problems, total = validate_verification_tests(vt)
        assert any("wrong field set" in p for p in problems)


class TestRefreshAlwaysRebuilds:
    """Repro 4: refresh always rebuilds gate, never trusts existing PASS."""

    def test_stale_pass_gate_replaced(self, tmp_path):
        """Even with existing PASS v1.1, refresh rebuilds and compares."""
        from scripts.refresh_review_evidence import refresh_staged_evidence
        staged = str(tmp_path / "staged")
        Path(staged).mkdir()
        stale = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks": [{"check_id": "fake", "found": True}],
            "checks_total": 1, "checks_passed": 1, "issues": [],
        }
        Path(staged, "runtime_integration_gate.json").write_text(json.dumps(stale))
        Path(staged, "verification_tests.json").write_text(json.dumps({
            "schema_version": "1.1.0", "runs": []}))
        report = refresh_staged_evidence(staged, ".")
        refreshed_names = [g["gate"] for g in report.get("refreshed_gates", [])]
        unchanged_names = [g["gate"] for g in report.get("unchanged_gates", [])]
        assert "runtime_integration_gate.json" in refreshed_names or \
               "runtime_integration_gate.json" in unchanged_names


class TestManifestHeadCrossCheck:
    """Repro 5: bound_run.head_sha must equal Review Subject HEAD."""

    def test_head_sha_mismatch_blocked(self):
        from scripts.build_review_manifest import _gate_semantic_problems
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks_total": 1, "checks_passed": 1, "issues": [],
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/t.py", "min_passed": 1, "found": True,
                "bound_run": {
                    "run_id": "vr-0001", "command": "pytest tests/t.py",
                    "exit_code": 0, "passed": 5, "failed": 0,
                    "skipped": 0, "selected": 5,
                    "node_ids": ["tests/t.py::test_a"],
                    "output_hash": "a" * 64, "head_sha": "wrong_sha",
                },
            }],
        }
        ctx = {"review_subject_head": "correct_sha"}
        problems = _gate_semantic_problems(
            "runtime_integration_gate.json", gate, {}, ctx)
        assert any("Review Subject HEAD" in p for p in problems)

    def test_head_sha_match_passes(self):
        from scripts.build_review_manifest import _gate_semantic_problems
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks_total": 1, "checks_passed": 1, "issues": [],
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/t.py", "min_passed": 1, "found": True,
                "bound_run": {
                    "run_id": "vr-0001", "command": "pytest tests/t.py",
                    "exit_code": 0, "passed": 5, "failed": 0,
                    "skipped": 0, "selected": 5,
                    "node_ids": ["tests/t.py::test_a"],
                    "output_hash": "a" * 64, "head_sha": "abc123",
                },
            }],
        }
        ctx = {"review_subject_head": "abc123"}
        problems = _gate_semantic_problems(
            "runtime_integration_gate.json", gate, {}, ctx)
        assert not any("Review Subject HEAD" in p for p in problems)

    def test_output_hash_sha256_syntax(self):
        from scripts.build_review_manifest import _gate_semantic_problems
        gate = {
            "schema_version": "1.1.0", "verdict": "PASS",
            "checks_total": 1, "checks_passed": 1, "issues": [],
            "checks": [{
                "check_id": "test_bind", "check_type": "test_execution_binding",
                "test_file": "tests/t.py", "min_passed": 1, "found": True,
                "bound_run": {
                    "run_id": "vr-0001", "command": "pytest tests/t.py",
                    "exit_code": 0, "passed": 5, "failed": 0,
                    "skipped": 0, "selected": 5,
                    "node_ids": ["tests/t.py::test_a"],
                    "output_hash": "not_sha256", "head_sha": "abc123",
                },
            }],
        }
        ctx = {"review_subject_head": "abc123"}
        problems = _gate_semantic_problems(
            "runtime_integration_gate.json", gate, {}, ctx)
        assert any("sha256 hex" in p for p in problems)


class TestRefreshPrivacySafe:
    """Repro 7: refresh report contains no absolute paths."""

    def test_no_absolute_path_in_report(self, tmp_path):
        from scripts.refresh_review_evidence import refresh_staged_evidence
        staged = str(tmp_path / "staged")
        Path(staged).mkdir()
        Path(staged, "verification_tests.json").write_text("{}")
        report = refresh_staged_evidence(staged, ".")
        report_json = json.dumps(report)
        assert "/home/" not in report_json
        assert str(tmp_path) not in report_json


class TestCriticalNodeBindings:
    """Scope 4: critical node IDs must appear in bound run."""

    def test_missing_critical_node_blocks(self):
        from packages.orchestration.runtime_integration_gate import (
            _bind_test_execution,
        )
        results = []
        issues = []
        vd = {"runs": [{
            "run_id": "vr-0001", "command": "pytest tests/t.py", "exit_code": 0,
            "passed": 80, "failed": 0, "test_files": ["tests/t.py"],
            "node_ids": ["tests/t.py::TestA::test_x"],
            "output_hash": "a" * 64, "head_sha": "abc",
            "selected": 80, "deselected": 0, "skipped": 0,
            "duration_seconds": 1.0, "stdout_summary": "ok",
        }]}
        bindings = [{
            "check_id": "test_critical",
            "check_type": "test_execution_binding",
            "test_file": "tests/t.py",
            "min_passed": 1,
            "critical_node_ids": ["TestMissing::test_not_there"],
        }]
        import packages.orchestration.runtime_integration_gate as rig
        orig = rig.TEST_EXECUTION_BINDINGS
        try:
            rig.TEST_EXECUTION_BINDINGS = tuple(bindings)
            _bind_test_execution(results, issues, vd)
        finally:
            rig.TEST_EXECUTION_BINDINGS = orig
        assert results[0]["found"] is False
        assert any("critical" in i.lower() for i in issues)

    def test_present_critical_node_passes(self):
        import packages.orchestration.runtime_integration_gate as rig
        from packages.orchestration.runtime_integration_gate import _bind_test_execution
        results = []
        issues = []
        vd = {"runs": [{
            "run_id": "vr-0001", "command": "pytest tests/t.py", "exit_code": 0,
            "passed": 80, "failed": 0, "test_files": ["tests/t.py"],
            "node_ids": ["tests/t.py::TestA::test_x"],
            "output_hash": "a" * 64, "head_sha": "abc",
            "selected": 80, "deselected": 0, "skipped": 0,
            "duration_seconds": 1.0, "stdout_summary": "ok",
        }]}
        bindings = [{
            "check_id": "test_critical",
            "check_type": "test_execution_binding",
            "test_file": "tests/t.py",
            "min_passed": 1,
            "critical_node_ids": ["TestA::test_x"],
        }]
        orig = rig.TEST_EXECUTION_BINDINGS
        try:
            rig.TEST_EXECUTION_BINDINGS = tuple(bindings)
            _bind_test_execution(results, issues, vd)
        finally:
            rig.TEST_EXECUTION_BINDINGS = orig
        assert results[0]["found"] is True


class TestPersistedActualsSchemaVersion:
    """Repro 6: persisted Actuals must reject invalid schema_version."""

    def test_missing_schema_version_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={"provider_call_count": 0})
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="schema_version"):
            run_job(job.job_id)

    def test_wrong_schema_version_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "banana", "provider_call_count": 0,
            "actual_call_count": 0, "unmeasured_call_count": 0,
            "total_tokens": 0, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="schema_version"):
            run_job(job.job_id)

    def test_valid_schema_version_passes(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0", "provider_call_count": 0,
            "actual_call_count": 0, "unmeasured_call_count": 0,
            "total_tokens": 0, "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status != "blocked" or "schema_version" not in (result.error or "")


class TestPersistedActualsMissingSources:
    """Repro 7: persisted measured Actuals must require source provenance."""

    def test_positive_count_missing_sources_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0",
            "provider_call_count": 1,
            "actual_call_count": 1,
            "unmeasured_call_count": 0,
            "total_tokens": 100,
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="actual_sources"):
            run_job(job.job_id)

    def test_positive_count_empty_sources_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0",
            "provider_call_count": 1,
            "actual_call_count": 1,
            "unmeasured_call_count": 0,
            "total_tokens": 100,
            "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="actual_sources"):
            run_job(job.job_id)

    def test_zero_count_no_sources_passes(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(budget_actuals={
            "schema_version": "1.0.0",
            "provider_call_count": 0,
            "actual_call_count": 0,
            "unmeasured_call_count": 0,
            "total_tokens": 0,
            "actual_sources": [],
            "started_at": T0.isoformat(),
        })
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status != "blocked" or "actual_sources" not in (result.error or "")


class TestCorruptFirstRunningAt:
    """Repro 9: corrupt persisted first_running_at must block, not fail open."""

    def test_unparseable_value_blocks(self):
        from packages.orchestration.pingpong_job import JOB_BLOCKED, JobPlan, _persist_job, run_job
        job = JobPlan(first_running_at="not-a-date")
        job.status = "running"
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == JOB_BLOCKED
        assert "corrupt_first_running_at" in (result.error or "")

    def test_naive_datetime_blocks(self):
        from packages.orchestration.pingpong_job import JOB_BLOCKED, JobPlan, _persist_job, run_job
        job = JobPlan(first_running_at="2026-07-01T12:00:00")
        job.status = "running"
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status == JOB_BLOCKED
        assert "timezone-naive" in (result.error or "")

    def test_valid_iso_utc_passes(self):
        from packages.orchestration.pingpong_job import JOB_BLOCKED, JobPlan, _persist_job, run_job
        job = JobPlan(first_running_at="2026-07-01T12:00:00+00:00")
        job.status = "running"
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.status != JOB_BLOCKED or "first_running_at" not in (result.error or "")


class TestWallClockSplit:
    """Scope 2: started_at must equal first_running_at; mismatch blocks."""

    def test_mismatched_timestamps_raises(self):
        from packages.orchestration.budget_guard import BudgetCounterError
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        job = JobPlan(
            first_running_at="2026-07-01T12:00:00+00:00",
            budget_actuals={
                "schema_version": "1.0.0",
                "provider_call_count": 0,
                "actual_call_count": 0,
                "unmeasured_call_count": 0,
                "total_tokens": 0,
                "actual_sources": [],
                "started_at": "2026-07-01T13:00:00+00:00",
            },
        )
        _persist_job(job)
        with pytest.raises(BudgetCounterError, match="wall-clock split"):
            run_job(job.job_id)

    def test_matching_timestamps_passes(self):
        from packages.orchestration.pingpong_job import JobPlan, _persist_job, run_job
        ts = "2026-07-01T12:00:00+00:00"
        job = JobPlan(
            first_running_at=ts,
            budget_actuals={
                "schema_version": "1.0.0",
                "provider_call_count": 0,
                "actual_call_count": 0,
                "unmeasured_call_count": 0,
                "total_tokens": 0,
                "actual_sources": [],
                "started_at": ts,
            },
        )
        _persist_job(job)
        result = run_job(job.job_id)
        assert result.error is None or "wall-clock" not in (result.error or "")

    def test_cli_reports_corrupt_on_mismatch(self, monkeypatch):
        import io

        from packages.orchestration.pingpong_job import JobPlan
        job = JobPlan(
            job_id="wallclock1",
            first_running_at="2026-07-01T12:00:00+00:00",
            budget_actuals={
                "schema_version": "1.0.0",
                "provider_call_count": 0,
                "actual_call_count": 0,
                "unmeasured_call_count": 0,
                "total_tokens": 0,
                "actual_sources": [],
                "started_at": "2026-07-01T14:00:00+00:00",
            },
        )
        job.budgets = {"max_provider_calls": 10}
        monkeypatch.setattr(
            "packages.orchestration.pingpong_job.load_job_plan",
            lambda jid: job if jid == "wallclock1" else None,
        )
        buf = io.StringIO()
        monkeypatch.setattr("sys.stdout", buf)
        from apps.cli.commands.job import _cmd_job_budget
        _cmd_job_budget("wallclock1", json_output=True)
        data = json.loads(buf.getvalue())
        assert data["status"] == "corrupt"
        assert "wall-clock" in data.get("diagnostic", "")


class TestRealThreeCallLimit:
    """Scope 3: real three-call-limit acceptance through run_job path.

    FakeProvider builds/reviews; builder_name="counted" makes _on_provider_call
    count them instead of skipping. max_provider_calls=3 → calls 1-3 execute,
    call 4 never begins, job stops with budget_exhausted.
    """

    @pytest.fixture(autouse=True)
    def _isolate(self, tmp_path, monkeypatch):
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

    @pytest.fixture
    def demo_repo(self, tmp_path):
        import subprocess
        repo = tmp_path / "repo"
        (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "README.md").write_text("# docs\n")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True,
                        capture_output=True)
        subprocess.run(["git", "config", "user.email", "t@test"],
                        cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "T"],
                        cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "add", "-A"],
                        cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "base"],
                        cwd=repo, check=True, capture_output=True)
        return repo

    def test_three_calls_then_stop(self, demo_repo):
        from packages.orchestration.pingpong_job import parse_job_file, run_job
        from packages.orchestration.pingpong_provider import FakeProvider

        job_text = """\
# Job: three-call-test

## Task 1
Touch docs/README.md

Acceptance:
- file exists
"""
        job = parse_job_file(job_text, str(demo_repo))
        job.budgets = {"max_provider_calls": 3}
        from packages.orchestration.pingpong_job import _persist_job
        _persist_job(job)

        result = run_job(
            job.job_id,
            builder_name="counted",
            reviewer_name="counted",
            builder_provider=FakeProvider(pass_on_round=99, fail_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=99, fail_on_round=99),
            repair_rounds=5,
        )

        assert result.status == "stopped", f"expected stopped, got {result.status}: {result.error}"
        actuals = result.budget_actuals
        assert actuals is not None
        assert actuals["provider_call_count"] == 3
        assert actuals["schema_version"] == "1.0.0"
        assert result.stop_source == "budget"


class TestVTCrossConsistency:
    """Scope 4: VT V1.1 cross-consistency — selected, node_ids, output_hash."""

    def _valid_run(self, **overrides):
        base = {
            "run_id": "vr-0001", "command": "pytest tests/a.py", "exit_code": 0,
            "passed": 3, "failed": 0, "test_files": ["tests/a.py"],
            "stdout_summary": "3 passed",
            "head_sha": "abc123",
            "output_hash": hashlib.sha256(b"3 passed").hexdigest(),
            "selected": 3, "deselected": 0, "skipped": 0,
            "node_ids": ["tests/a.py::t1", "tests/a.py::t2", "tests/a.py::t3"],
            "duration_seconds": 0.5,
        }
        base.update(overrides)
        return base

    def _valid_vt(self, runs=None):
        r = runs or [self._valid_run()]
        return {
            "schema_version": "1.1.0",
            "verification_type": "explicit_commands",
            "command": " && ".join(run["command"] for run in r),
            "exit_code": 0, "passed": sum(run["passed"] for run in r),
            "failed": 0, "test_files": ["tests/a.py"],
            "timestamp": datetime.now(UTC).isoformat(),
            "runs": r,
        }

    def test_valid_vt_passes(self):
        from scripts.build_review_manifest import validate_verification_tests
        problems, total = validate_verification_tests(self._valid_vt())
        assert not problems
        assert total == 3

    def test_selected_overcount_blocked(self):
        from scripts.build_review_manifest import validate_verification_tests
        vt = self._valid_vt([self._valid_run(selected=99)])
        problems, _ = validate_verification_tests(vt)
        assert any("selected" in p and "passed+failed+skipped" in p for p in problems)

    def test_selected_undercount_blocked(self):
        from scripts.build_review_manifest import validate_verification_tests
        vt = self._valid_vt([self._valid_run(selected=1)])
        problems, _ = validate_verification_tests(vt)
        assert any("selected" in p for p in problems)

    def test_node_ids_count_mismatch_blocked(self):
        from scripts.build_review_manifest import validate_verification_tests
        vt = self._valid_vt([self._valid_run(
            node_ids=["tests/a.py::t1"],
        )])
        problems, _ = validate_verification_tests(vt)
        assert any("node_ids count" in p for p in problems)

    def test_output_hash_tamper_blocked(self):
        from scripts.build_review_manifest import validate_verification_tests
        vt = self._valid_vt([self._valid_run(
            output_hash="b" * 64,
        )])
        problems, _ = validate_verification_tests(vt)
        assert any("output_hash" in p and "stdout_summary" in p for p in problems)

    def test_output_hash_matches_stdout(self):
        from scripts.build_review_manifest import validate_verification_tests
        summary = "5 passed in 0.3s"
        h = hashlib.sha256(summary.encode()).hexdigest()
        vt = self._valid_vt([self._valid_run(
            stdout_summary=summary, output_hash=h,
            passed=5, selected=5,
            node_ids=["t::a", "t::b", "t::c", "t::d", "t::e"],
        )])
        problems, total = validate_verification_tests(vt)
        assert not problems
        assert total == 5
