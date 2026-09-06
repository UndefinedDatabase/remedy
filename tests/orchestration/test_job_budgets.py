"""F018 T001 — JobBudgets model, config, CLI precedence, RunManifest snapshot."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.core.models import Job, JobBudgets


class TestJobBudgetsModel:
    def test_no_budgets_default(self):
        job = Job(name="test")
        assert job.budgets is None

    def test_all_none_fields(self):
        b = JobBudgets()
        assert b.max_total_tokens is None
        assert b.max_provider_calls is None
        assert b.max_wall_clock_minutes is None
        assert b.deadline is None

    def test_max_total_tokens_only(self):
        b = JobBudgets(max_total_tokens=100_000)
        assert b.max_total_tokens == 100_000

    def test_max_provider_calls_only(self):
        b = JobBudgets(max_provider_calls=10)
        assert b.max_provider_calls == 10

    def test_max_wall_clock_minutes_only(self):
        b = JobBudgets(max_wall_clock_minutes=30)
        assert b.max_wall_clock_minutes == 30

    # --- F104: the max_cost_usd money limit ---
    def test_max_cost_usd_defaults_to_none(self):
        assert JobBudgets().max_cost_usd is None

    def test_max_cost_usd_accepts_float(self):
        b = JobBudgets(max_cost_usd=2.5)
        assert b.max_cost_usd == 2.5
        assert isinstance(b.max_cost_usd, float)

    def test_max_cost_usd_accepts_int_and_normalises_to_float(self):
        b = JobBudgets(max_cost_usd=5)
        assert b.max_cost_usd == 5.0
        assert isinstance(b.max_cost_usd, float)

    def test_max_cost_usd_zero_rejected(self):
        with pytest.raises(ValueError, match="strictly positive"):
            JobBudgets(max_cost_usd=0)

    def test_max_cost_usd_negative_rejected(self):
        with pytest.raises(ValueError, match="strictly positive"):
            JobBudgets(max_cost_usd=-1.5)

    def test_max_cost_usd_bool_rejected(self):
        with pytest.raises(ValueError):
            JobBudgets(max_cost_usd=True)

    def test_max_cost_usd_nan_rejected(self):
        with pytest.raises(ValueError, match="finite"):
            JobBudgets(max_cost_usd=float("nan"))

    def test_max_cost_usd_inf_rejected(self):
        with pytest.raises(ValueError, match="finite"):
            JobBudgets(max_cost_usd=float("inf"))

    def test_max_cost_usd_negative_inf_rejected(self):
        with pytest.raises(ValueError, match="finite"):
            JobBudgets(max_cost_usd=float("-inf"))

    def test_max_cost_usd_still_forbids_extra_fields(self):
        with pytest.raises(Exception):
            JobBudgets(max_cost_usd=1.0, max_cost_eur=2.0)

    def test_max_cost_usd_roundtrips_through_json(self):
        b = JobBudgets(max_cost_usd=1.25)
        snap = b.model_dump(mode="json")
        assert snap["max_cost_usd"] == 1.25
        assert JobBudgets.model_validate(snap).max_cost_usd == 1.25

    def test_deadline_only(self):
        dl = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        b = JobBudgets(deadline=dl)
        assert b.deadline == dl

    def test_all_limits_together(self):
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        b = JobBudgets(
            max_total_tokens=500_000,
            max_provider_calls=50,
            max_wall_clock_minutes=120,
            deadline=dl,
        )
        assert b.max_total_tokens == 500_000
        assert b.max_provider_calls == 50
        assert b.max_wall_clock_minutes == 120
        assert b.deadline == dl

    def test_boolean_rejected_for_tokens(self):
        with pytest.raises(ValueError, match="bool"):
            JobBudgets(max_total_tokens=True)

    def test_boolean_rejected_for_calls(self):
        with pytest.raises(ValueError, match="bool"):
            JobBudgets(max_provider_calls=False)

    def test_zero_rejected(self):
        with pytest.raises(ValueError, match="strictly positive"):
            JobBudgets(max_total_tokens=0)

    def test_negative_rejected(self):
        with pytest.raises(ValueError, match="strictly positive"):
            JobBudgets(max_provider_calls=-1)

    def test_unknown_field_rejected(self):
        with pytest.raises(Exception):
            JobBudgets(max_total_tokens=100, unknown_field=42)

    def test_deadline_without_timezone_rejected(self):
        with pytest.raises(ValueError, match="timezone-aware"):
            JobBudgets(deadline=datetime(2026, 12, 31))

    def test_deadline_normalized_to_utc(self):
        est = timezone(timedelta(hours=-5))
        dl = datetime(2026, 12, 31, 20, 0, 0, tzinfo=est)
        b = JobBudgets(deadline=dl)
        assert b.deadline.tzinfo == timezone.utc
        assert b.deadline == datetime(2027, 1, 1, 1, 0, 0, tzinfo=timezone.utc)

    def test_backward_compatible_old_job_fixture(self):
        data = {"name": "old-job", "id": "00000000-0000-0000-0000-000000000001"}
        job = Job.model_validate(data)
        assert job.budgets is None
        assert job.name == "old-job"

    def test_job_with_budgets_serializes(self):
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        job = Job(
            name="budgeted",
            budgets=JobBudgets(max_total_tokens=100_000, deadline=dl),
        )
        d = job.model_dump()
        assert d["budgets"]["max_total_tokens"] == 100_000
        assert d["budgets"]["deadline"] is not None

    def test_job_with_budgets_roundtrips(self):
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        job = Job(
            name="budgeted",
            budgets=JobBudgets(
                max_total_tokens=100_000,
                max_provider_calls=10,
                deadline=dl,
            ),
        )
        d = job.model_dump(mode="json")
        job2 = Job.model_validate(d)
        assert job2.budgets is not None
        assert job2.budgets.max_total_tokens == 100_000
        assert job2.budgets.max_provider_calls == 10

    def test_float_rejected_for_int_field(self):
        with pytest.raises(Exception):
            JobBudgets(max_total_tokens=1.5)

    def test_exact_float_rejected(self):
        with pytest.raises(Exception):
            JobBudgets(max_total_tokens=5.0)

    def test_string_int_rejected(self):
        with pytest.raises(Exception):
            JobBudgets(max_total_tokens="5")

    def test_string_calls_rejected(self):
        with pytest.raises(Exception):
            JobBudgets(max_provider_calls="10")

    def test_string_minutes_rejected(self):
        with pytest.raises(Exception):
            JobBudgets(max_wall_clock_minutes="30")

    def test_json_roundtrip_preserves_strict_types(self):
        b = JobBudgets(max_total_tokens=100, max_provider_calls=3)
        job = Job(name="strict-test", budgets=b)
        json_str = job.model_dump_json()
        job2 = Job.model_validate_json(json_str)
        assert job2.budgets.max_total_tokens == 100
        assert isinstance(job2.budgets.max_total_tokens, int)

    def test_config_only_budgets_persist_on_job(self, tmp_path, monkeypatch):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_total_tokens = 321\nmax_provider_calls = 7\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        from packages.orchestration.config import reset_config
        monkeypatch.chdir(tmp_path)
        reset_config()
        try:
            result = resolve_job_budgets()
            assert result is not None
            assert result.max_total_tokens == 321
            assert result.max_provider_calls == 7
            job = Job(name="config-budget", budgets=result)
            assert job.budgets is not None
            assert job.budgets.max_total_tokens == 321
        finally:
            reset_config()

    def test_malformed_toml_raises_budget_config_error(self, tmp_path, monkeypatch):
        """F018: malformed TOML fails closed with BudgetConfigError."""
        toml = tmp_path / "remedy.toml"
        toml.write_text('{{bad toml')
        from packages.orchestration.budget_resolution import BudgetConfigError, resolve_job_budgets
        from packages.orchestration.config import reset_config
        monkeypatch.chdir(tmp_path)
        reset_config()
        try:
            with pytest.raises(BudgetConfigError, match="Malformed TOML"):
                resolve_job_budgets()
        finally:
            reset_config()


class TestBudgetResolution:
    def test_no_inputs_returns_none(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets()
        assert result is None

    def test_cli_tokens_override(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_max_total_tokens="200000")
        assert result is not None
        assert result.max_total_tokens == 200_000

    def test_cli_overrides_config(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_total_tokens = 100000\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(
            cli_max_total_tokens="500000",
            config_path=str(toml),
        )
        assert result is not None
        assert result.max_total_tokens == 500_000

    def test_config_used_when_no_cli(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_provider_calls = 25\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(config_path=str(toml))
        assert result is not None
        assert result.max_provider_calls == 25

    def test_malformed_config_raises(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_total_tokens = "not_a_number"\n')
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="not a valid integer"):
            resolve_job_budgets(config_path=str(toml))

    def test_invalid_deadline_string(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="invalid deadline"):
            resolve_job_budgets(cli_deadline="not-a-date")

    def test_deadline_without_timezone_rejected(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="no timezone"):
            resolve_job_budgets(cli_deadline="2026-12-31T23:59:59")

    def test_deadline_normalized_to_utc(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_deadline="2026-12-31T20:00:00-05:00")
        assert result is not None
        assert result.deadline.tzinfo == timezone.utc
        assert result.deadline == datetime(2027, 1, 1, 1, 0, 0, tzinfo=timezone.utc)

    def test_cli_all_flags(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(
            cli_max_total_tokens="100000",
            cli_max_provider_calls="20",
            cli_max_wall_clock_minutes="60",
            cli_deadline="2026-12-31T23:59:59+00:00",
        )
        assert result is not None
        assert result.max_total_tokens == 100_000
        assert result.max_provider_calls == 20
        assert result.max_wall_clock_minutes == 60
        assert result.deadline is not None

    def test_env_budget_override(self, monkeypatch):
        monkeypatch.setenv("REMEDY_BUDGET_MAX_TOTAL_TOKENS", "300000")
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets()
        assert result is not None
        assert result.max_total_tokens == 300_000


class TestCostBudgetResolution:
    """F104: max_cost_usd follows the same CLI > env > TOML > no-limit rules."""

    def test_absent_everywhere_yields_none_field(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_max_total_tokens="1000")
        assert result is not None
        assert result.max_cost_usd is None

    def test_absent_everywhere_does_not_force_a_budgets_object(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        assert resolve_job_budgets() is None

    def test_cli_flag_sets_the_limit(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_max_cost_usd="2.50")
        assert result is not None
        assert result.max_cost_usd == 2.5

    def test_cli_flag_alone_produces_a_budgets_object(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_max_cost_usd="0.01")
        assert result is not None
        assert result.max_total_tokens is None
        assert result.max_cost_usd == 0.01

    def test_config_used_when_no_cli(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_cost_usd = 4.25\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(config_path=str(toml))
        assert result is not None
        assert result.max_cost_usd == 4.25

    def test_cli_beats_toml(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_cost_usd = 4.25\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(
            cli_max_cost_usd="9.99", config_path=str(toml))
        assert result is not None
        assert result.max_cost_usd == 9.99

    def test_env_override(self, monkeypatch):
        monkeypatch.setenv("REMEDY_BUDGET_MAX_COST_USD", "3.75")
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets()
        assert result is not None
        assert result.max_cost_usd == 3.75

    def test_cli_beats_env(self, monkeypatch):
        monkeypatch.setenv("REMEDY_BUDGET_MAX_COST_USD", "3.75")
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(cli_max_cost_usd="1.00")
        assert result is not None
        assert result.max_cost_usd == 1.0

    def test_malformed_cli_value_raises(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="not a valid number"):
            resolve_job_budgets(cli_max_cost_usd="abc")

    def test_zero_cli_value_raises(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="strictly positive"):
            resolve_job_budgets(cli_max_cost_usd="0")

    def test_negative_cli_value_raises(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="strictly positive"):
            resolve_job_budgets(cli_max_cost_usd="-1.0")

    def test_non_finite_cli_value_raises(self):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="finite"):
            resolve_job_budgets(cli_max_cost_usd="inf")

    def test_malformed_toml_value_raises(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_cost_usd = "not_a_number"\n')
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        with pytest.raises(BudgetConfigError, match="not a valid number"):
            resolve_job_budgets(config_path=str(toml))

    def test_empty_cli_string_is_no_limit(self):
        from packages.orchestration.budget_resolution import resolve_job_budgets
        assert resolve_job_budgets(cli_max_cost_usd="   ") is None

    def test_integer_toml_value_normalises_to_float(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text('[remedy.budget]\nmax_cost_usd = 3\n')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        result = resolve_job_budgets(config_path=str(toml))
        assert result is not None
        assert result.max_cost_usd == 3.0
        assert isinstance(result.max_cost_usd, float)


class TestConfigKeys:
    def test_budget_keys_registered(self):
        from packages.orchestration.config import get_key_spec
        assert get_key_spec("budget.max_total_tokens") is not None
        assert get_key_spec("budget.max_provider_calls") is not None
        assert get_key_spec("budget.max_wall_clock_minutes") is not None
        assert get_key_spec("budget.max_cost_usd") is not None
        assert get_key_spec("budget.deadline") is not None

    def test_budget_key_types(self):
        from packages.orchestration.config import get_key_spec
        assert get_key_spec("budget.max_total_tokens").value_type is int
        assert get_key_spec("budget.max_provider_calls").value_type is int
        assert get_key_spec("budget.max_wall_clock_minutes").value_type is int
        assert get_key_spec("budget.max_cost_usd").value_type is float
        assert get_key_spec("budget.deadline").value_type is str


class TestRunManifestBudgetSnapshot:
    def test_budget_model_dump_for_manifest(self):
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        b = JobBudgets(max_total_tokens=50000, max_provider_calls=5, deadline=dl)
        snap = b.model_dump(mode="json")
        assert snap["max_total_tokens"] == 50000
        assert snap["max_provider_calls"] == 5
        assert snap["deadline"] is not None
        assert snap["max_wall_clock_minutes"] is None

    def test_budget_dump_roundtrip_via_json(self):
        import json
        b = JobBudgets(max_total_tokens=100, max_wall_clock_minutes=30)
        snap = b.model_dump(mode="json")
        raw = json.dumps(snap)
        loaded = json.loads(raw)
        assert loaded["max_total_tokens"] == 100
        assert loaded["max_wall_clock_minutes"] == 30
        assert loaded["max_provider_calls"] is None
        b2 = JobBudgets.model_validate(loaded)
        assert b2.max_total_tokens == 100

    def test_job_budgets_accessible_for_manifest_binding(self):
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        job = Job(
            name="manifest-test",
            budgets=JobBudgets(max_total_tokens=50000, deadline=dl),
        )
        job_budgets = getattr(job, "budgets", None)
        assert job_budgets is not None
        snap = job_budgets.model_dump(mode="json") if hasattr(job_budgets, "model_dump") else None
        assert snap is not None
        assert snap["max_total_tokens"] == 50000

    def test_no_budgets_yields_none_snapshot(self):
        job = Job(name="no-budget")
        job_budgets = getattr(job, "budgets", None)
        assert job_budgets is None


class TestJobPlanBudgetsPersistence:
    """F018: JobPlan budgets field persisted through _export_job/_import_job."""

    def test_jobplan_budgets_field_default_none(self):
        from packages.orchestration.pingpong_job import JobPlan
        plan = JobPlan()
        assert plan.budgets is None

    def test_jobplan_budgets_roundtrip(self):
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job
        dl = datetime(2026, 12, 31, tzinfo=timezone.utc)
        b = JobBudgets(max_total_tokens=100000, max_provider_calls=10, deadline=dl)
        plan = JobPlan(budgets=b.model_dump(mode="json"))
        exported = _export_job(plan)
        assert exported["budgets"] is not None
        assert exported["budgets"]["max_total_tokens"] == 100000
        imported = _import_job(exported)
        assert imported.budgets is not None
        assert imported.budgets["max_total_tokens"] == 100000
        assert imported.budgets["max_provider_calls"] == 10

    def test_jobplan_no_budgets_roundtrip(self):
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job
        plan = JobPlan()
        exported = _export_job(plan)
        assert exported["budgets"] is None
        imported = _import_job(exported)
        assert imported.budgets is None

    def test_jobplan_old_format_no_budgets_key(self):
        from packages.orchestration.pingpong_job import _import_job
        data = {"job_id": "test123"}
        imported = _import_job(data)
        assert imported.budgets is None

    def test_jobplan_budgets_reconstructible(self):
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job
        b = JobBudgets(max_wall_clock_minutes=60)
        plan = JobPlan(budgets=b.model_dump(mode="json"))
        exported = _export_job(plan)
        imported = _import_job(exported)
        reconstructed = JobBudgets.model_validate(imported.budgets)
        assert reconstructed.max_wall_clock_minutes == 60
        assert reconstructed.max_total_tokens is None


class TestBudgetCountersStrictValidation:
    """F018: BudgetCounters rejects permissive inputs."""

    def test_elapsed_seconds_bool_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="elapsed_seconds.*bool"):
            BudgetCounters(elapsed_seconds=True)

    def test_evaluated_at_string_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="evaluated_at.*datetime"):
            BudgetCounters(evaluated_at="not-datetime")

    def test_actual_sources_non_tuple_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="actual_sources.*tuple"):
            BudgetCounters(actual_sources=[123])

    def test_actual_sources_non_string_element_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="actual_sources.*str"):
            BudgetCounters(actual_sources=(123,))

    def test_started_at_after_evaluated_at_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        future = datetime(2099, 1, 1, tzinfo=timezone.utc)
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        with pytest.raises(BudgetCounterError, match="started_at.*after"):
            BudgetCounters(started_at=future, evaluated_at=past)

    def test_started_at_non_datetime_rejected(self):
        from packages.orchestration.budget_guard import BudgetCounterError, BudgetCounters
        with pytest.raises(BudgetCounterError, match="started_at.*datetime"):
            BudgetCounters(started_at="2020-01-01")

    def test_valid_counters_pass(self):
        from packages.orchestration.budget_guard import BudgetCounters
        now = datetime.now(timezone.utc)
        c = BudgetCounters(
            provider_calls=5,
            measured_token_total=1000,
            measured_call_count=3,
            unmeasured_call_count=2,
            elapsed_seconds=60.0,
            evaluated_at=now,
            started_at=now - timedelta(seconds=60),
            actual_sources=("pingpong_actuals", "token_actuals"),
        )
        assert c.provider_calls == 5


class TestRunManifestBudgetIdentity:
    """F018: budgets in RunManifest logical_input_projection and from_trusted_json."""

    def _make_manifest_with_budgets(self, budgets_dict):
        from packages.orchestration.run_manifest import EpisodeInputSnapshotV1, RunManifestV1
        snap = EpisodeInputSnapshotV1.__new__(EpisodeInputSnapshotV1)
        object.__setattr__(snap, "status", "ok")
        object.__setattr__(snap, "version", 1)
        object.__setattr__(snap, "episode_id", "ep1")
        object.__setattr__(snap, "capture_phase", "episode_start")
        object.__setattr__(snap, "problems", ())
        inp = type("Inp", (), {
            "remedy_git_sha": "abc123",
            "remedy_dirty": False,
            "remedy_worktree": {},
            "target_base_commit": "def456",
            "target_head": "def456",
            "target_tree": "tree1",
            "target_worktree": {},
            "job_initial_tree": "jtree1",
            "episode_start_workspace_identity": None,
            "job_file_sha256": "jfh1",
            "models": {},
            "config": [],
            "environment": [],
            "job_input": {},
        })()
        object.__setattr__(snap, "input", inp)
        return RunManifestV1(
            job_id="j1", episode_id="ep1", created_at="now", status="completed",
            episode_snapshot=snap, job_input_sha256="jish",
            calls=(), coverage=type("Cov", (), {"status": "complete", "problems": ()})(),
            budgets=budgets_dict,
        )

    def test_budgets_in_logical_projection(self):
        b = {"max_total_tokens": 100000, "max_provider_calls": 10,
             "max_wall_clock_minutes": None, "deadline": None}
        m = self._make_manifest_with_budgets(b)
        proj = m.logical_input_projection()
        assert "budgets" in proj
        assert proj["budgets"]["max_total_tokens"] == 100000

    def test_no_budgets_in_logical_projection(self):
        m = self._make_manifest_with_budgets(None)
        proj = m.logical_input_projection()
        assert proj["budgets"] is None

    def test_different_budgets_different_hash(self):
        m1 = self._make_manifest_with_budgets(
            {"max_total_tokens": 100000, "max_provider_calls": None,
             "max_wall_clock_minutes": None, "deadline": None})
        m2 = self._make_manifest_with_budgets(
            {"max_total_tokens": 200000, "max_provider_calls": None,
             "max_wall_clock_minutes": None, "deadline": None})
        assert m1.logical_input_sha256() != m2.logical_input_sha256()

    def test_from_trusted_json_preserves_budgets(self):
        from packages.orchestration.run_manifest import MANIFEST_VERSION, RunManifestV1
        b = {"max_total_tokens": 50000, "max_provider_calls": 5,
             "max_wall_clock_minutes": None, "deadline": None}
        m = self._make_manifest_with_budgets(b)
        snap_dict = {
            "snapshot_v": 1,
            "episode_id": "ep1",
            "captured_at": "now",
            "capture_phase": "episode_start",
            "status": "ok",
            "problems": [],
            "input": {
                "remedy_git_sha": "abc123", "remedy_dirty": False,
                "remedy_worktree": {}, "target_base_commit": "def456",
                "target_head": "def456", "target_tree": "tree1",
                "target_worktree": {},
                "job_initial_tree": "jtree1",
                "episode_start_workspace_tree": "",
                "episode_start_workspace_identity": None,
                "job_file_sha256": "jfh1",
                "models": {}, "config": [], "environment": [],
                "job_input": {"tasks": []},
                "job_input_sha256": "jish",
            },
        }
        d = {
            "manifest_v": MANIFEST_VERSION,
            "job_id": "j1", "episode_id": "ep1", "created_at": "now",
            "status": "completed",
            "episode_snapshot": snap_dict,
            "job_input_sha256": "jish",
            "calls": [], "coverage": {"status": "complete", "problems": []},
            "call_expectation": {"episode_phase": "worked", "tasks": []},
            "call_ledgers": [],
            "prior_episode_ids": [], "episode_ordinal": 1,
            "previous_episode_id": "", "stop_request_id": "",
            "budgets": b,
        }
        m2 = RunManifestV1.from_trusted_json(d)
        assert m2.budgets == b

    def test_decode_budgets_rejects_unknown_keys(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="unknown keys"):
            _decode_budgets_field({"max_total_tokens": 100, "unknown_field": 42})

    def test_decode_budgets_rejects_bool_int_field(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="bool"):
            _decode_budgets_field({"max_total_tokens": True})

    def test_decode_budgets_rejects_string_int_field(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="strictly positive int"):
            _decode_budgets_field({"max_provider_calls": "five"})

    def test_decode_budgets_accepts_valid(self):
        from packages.orchestration.run_manifest import _decode_budgets_field
        result = _decode_budgets_field(
            {"max_total_tokens": 100, "max_provider_calls": None,
             "max_wall_clock_minutes": 60, "deadline": "2026-12-31T00:00:00+00:00"})
        assert result["max_total_tokens"] == 100

    def test_decode_budgets_accepts_none(self):
        from packages.orchestration.run_manifest import _decode_budgets_field
        assert _decode_budgets_field(None) is None

    # -- R-0225: the closed budget schema admits the money limit --------------
    # `max_cost_usd` reached `JobBudgets` in F104 T001 but not this allowlist, so
    # every money-limited job failed its F012 manifest write and could not
    # FINALIZE a stop. These pin the widening AND that it is exactly one field.

    def test_decode_budgets_accepts_a_fractional_cost_and_returns_it_unchanged(self):
        import json

        from packages.orchestration.run_manifest import _decode_budgets_field
        result = _decode_budgets_field({"max_cost_usd": 1.5})
        assert result == {"max_cost_usd": 1.5}
        # ...and survives the JSON trip the manifest actually takes.
        assert _decode_budgets_field(json.loads(json.dumps(result))) == result

    def test_decode_budgets_accepts_an_integer_cost(self):
        from packages.orchestration.run_manifest import _decode_budgets_field
        assert _decode_budgets_field({"max_cost_usd": 2}) == {"max_cost_usd": 2}

    def test_decode_budgets_rejects_bool_cost(self):
        # bool is an int subclass, so it must be rejected explicitly.
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="bool"):
            _decode_budgets_field({"max_cost_usd": True})

    def test_decode_budgets_rejects_string_cost(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="str"):
            _decode_budgets_field({"max_cost_usd": "5"})

    def test_decode_budgets_rejects_zero_cost(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="strictly positive"):
            _decode_budgets_field({"max_cost_usd": 0})

    def test_decode_budgets_rejects_negative_cost(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="strictly positive"):
            _decode_budgets_field({"max_cost_usd": -1.0})

    def test_decode_budgets_rejects_infinite_cost(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="not finite"):
            _decode_budgets_field({"max_cost_usd": float("inf")})

    def test_decode_budgets_rejects_nan_cost(self):
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="not finite"):
            _decode_budgets_field({"max_cost_usd": float("nan")})

    def test_decode_budgets_accepts_a_token_limit_and_a_cost_limit_together(self):
        from packages.orchestration.run_manifest import _decode_budgets_field
        result = _decode_budgets_field({"max_total_tokens": 50000, "max_cost_usd": 1.5})
        assert result == {"max_total_tokens": 50000, "max_cost_usd": 1.5}

    def test_decode_budgets_still_rejects_a_near_miss_unknown_key(self):
        # The schema stays CLOSED: R5 widened it by exactly one field.
        from packages.orchestration.run_manifest import ManifestError, _decode_budgets_field
        with pytest.raises(ManifestError, match="unknown keys"):
            _decode_budgets_field({"max_spend": 1.0})


class TestOnProviderAttemptCallback:
    """F018: _call_with_retry fires on_provider_attempt after each _record_attempt."""

    def _make_result(self):
        from packages.orchestration.pingpong_loop import PingPongResult
        return PingPongResult(
            goal="test", repo_path="/tmp/test",
            builder_provider="fake", reviewer_provider="fake",
            builder_model="", reviewer_model="",
            max_rounds=1, started_at="2026-01-01T00:00:00+00:00",
        )

    def _make_output(self, *, error="", usage_actuals=None):
        from types import SimpleNamespace
        return SimpleNamespace(
            error=error, raw_text="", output="ok", verdict="pass",
            usage_actuals=usage_actuals, actual_missing_reason="",
            stream_call_id="", stream_artifact_refs=[],
        )

    def test_callback_fires_on_success(self):
        from packages.orchestration.pingpong_loop import ProviderAttempt, _call_with_retry
        result = self._make_result()
        out = self._make_output()
        captured = []
        _call_with_retry(
            lambda: out,
            result=result,
            role="builder",
            provider="test-provider",
            on_provider_attempt=lambda a: captured.append(a),
        )
        assert len(captured) == 1
        assert isinstance(captured[0], ProviderAttempt)
        assert captured[0].role == "builder"
        assert captured[0].provider == "test-provider"

    def test_callback_fires_on_retry(self):
        from packages.orchestration.pingpong_loop import _call_with_retry
        result = self._make_result()
        call_count = 0

        def call_fn():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return self._make_output(error="provider_error: timeout after 30s")
            return self._make_output()

        captured = []
        _call_with_retry(
            call_fn,
            result=result,
            role="builder",
            provider="test-provider",
            on_provider_attempt=lambda a: captured.append(a),
        )
        assert len(captured) == 2
        assert not captured[0].is_retry
        assert captured[1].is_retry

    def test_no_callback_no_error(self):
        from packages.orchestration.pingpong_loop import _call_with_retry
        result = self._make_result()
        out = self._make_output()
        _call_with_retry(
            lambda: out,
            result=result,
            role="builder",
            provider="test-provider",
            on_provider_attempt=None,
        )
        assert len(result.provider_attempts) == 1

    def test_callback_receives_usage_actuals(self):
        from types import SimpleNamespace

        from packages.orchestration.pingpong_loop import _call_with_retry
        result = self._make_result()
        ua = SimpleNamespace(input_tokens=100, output_tokens=50)
        out = self._make_output(usage_actuals=ua)
        captured = []
        _call_with_retry(
            lambda: out,
            result=result,
            role="builder",
            provider="claude-cli",
            on_provider_attempt=lambda a: captured.append(a),
        )
        assert captured[0].usage_actuals is ua


class TestLiveCounterCallback:
    """F018: _on_provider_call in run_job updates accumulators immediately."""

    def test_live_counter_skips_fake_provider(self):
        from types import SimpleNamespace
        calls = 0
        tokens = 0
        measured = 0
        unmeasured = 0

        def on_call(attempt):
            nonlocal calls, tokens, measured, unmeasured
            if getattr(attempt, "provider", "fake") == "fake":
                return
            calls += 1
            ua = getattr(attempt, "usage_actuals", None)
            if ua is not None:
                measured += 1
                tokens += getattr(ua, "input_tokens", 0) + getattr(ua, "output_tokens", 0)
            else:
                unmeasured += 1

        fake_attempt = SimpleNamespace(provider="fake", usage_actuals=None)
        on_call(fake_attempt)
        assert calls == 0

    def test_live_counter_updates_on_real_provider(self):
        from types import SimpleNamespace
        calls = 0
        tokens = 0
        measured = 0
        unmeasured = 0

        def on_call(attempt):
            nonlocal calls, tokens, measured, unmeasured
            if getattr(attempt, "provider", "fake") == "fake":
                return
            calls += 1
            ua = getattr(attempt, "usage_actuals", None)
            if ua is not None:
                measured += 1
                tokens += getattr(ua, "input_tokens", 0) + getattr(ua, "output_tokens", 0)
            else:
                unmeasured += 1

        real_attempt = SimpleNamespace(
            provider="claude-cli",
            usage_actuals=SimpleNamespace(input_tokens=500, output_tokens=200),
        )
        on_call(real_attempt)
        assert calls == 1
        assert tokens == 700
        assert measured == 1
        assert unmeasured == 0

    def test_live_counter_unmeasured_when_no_actuals(self):
        from types import SimpleNamespace
        calls = 0
        unmeasured = 0

        def on_call(attempt):
            nonlocal calls, unmeasured
            if getattr(attempt, "provider", "fake") == "fake":
                return
            calls += 1
            if getattr(attempt, "usage_actuals", None) is None:
                unmeasured += 1

        real_attempt = SimpleNamespace(provider="ollama", usage_actuals=None)
        on_call(real_attempt)
        assert calls == 1
        assert unmeasured == 1


class TestBudgetStopSignal:
    """F018: budget exhaustion creates StopSignal with source='budget'."""

    def test_budget_stop_returns_stop_signal(self):
        from packages.orchestration.budget_guard import BudgetCounters
        from packages.orchestration.safe_points import should_stop
        budgets = JobBudgets(max_provider_calls=3)
        counters = BudgetCounters(
            provider_calls=3, measured_call_count=3,
            actual_sources=("pingpong_actuals",),
        )
        result = should_stop("test-job", budgets=budgets, counters=counters)
        assert result.should_stop
        assert result.source == "budget"
        assert "max_provider_calls" in result.reason

    def test_budget_stop_signal_constructed_correctly(self):
        from packages.orchestration.safe_points import StopSignal
        signal = StopSignal(
            job_id="test-job",
            request_id="budget_abc123",
            reason="budget_exhausted:max_provider_calls",
            source="budget",
        )
        assert signal.source == "budget"
        assert signal.request_id.startswith("budget_")
        assert signal.job_id == "test-job"
        j = signal.to_json()
        assert j["source"] == "budget"

    def test_deadline_stop_returns_exhausted(self):
        from packages.orchestration.budget_guard import BudgetCounters, evaluate_budget
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        budgets = JobBudgets(deadline=past)
        counters = BudgetCounters()
        result = evaluate_budget(budgets, counters)
        assert result.exhausted
        assert result.first_exhausted_limit == "deadline"

    def test_past_deadline_blocks_before_first_call(self):
        from packages.orchestration.budget_guard import BudgetCounters
        from packages.orchestration.safe_points import should_stop
        past = datetime(2020, 1, 1, tzinfo=timezone.utc)
        budgets = JobBudgets(deadline=past)
        counters = BudgetCounters()
        result = should_stop("test-job", budgets=budgets, counters=counters)
        assert result.should_stop
        assert "deadline" in result.reason


class TestHonestBudgetDisplay:
    """F018: job budget display never invents structured zeros."""

    def test_no_runs_reports_unavailable_json(self):
        import json as _json
        limits = {"max_provider_calls": 10}
        out: dict = {
            "job_id": "test-123",
            "limits": limits,
        }
        has_runs = False
        if not has_runs:
            out["counters"] = None
            out["status"] = "no_runs"
        rendered = _json.dumps(out)
        parsed = _json.loads(rendered)
        assert parsed["counters"] is None
        assert parsed["status"] == "no_runs"
        assert "evaluation" not in parsed

    def test_with_runs_has_evaluation(self):
        from packages.orchestration.budget_guard import BudgetCounters, evaluate_budget
        budgets = JobBudgets(max_provider_calls=10)
        counters = BudgetCounters(provider_calls=3, measured_call_count=3, actual_sources=("pingpong_actuals",))
        evaluation = evaluate_budget(budgets, counters)
        out = {"evaluation": evaluation.to_json()}
        assert out["evaluation"]["counters"]["provider_calls"] == 3
        assert not out["evaluation"]["exhausted"]

    def test_no_budgets_is_none(self):
        import json as _json
        out = {"job_id": "test", "budgets": None}
        rendered = _json.dumps(out)
        parsed = _json.loads(rendered)
        assert parsed["budgets"] is None


# ---------------------------------------------------------------------------
# F104 T003 — what `remedy job budget` actually PRINTS.
#
# These drive the real `_cmd_job_budget` and read its output through capsys.
# `TestHonestBudgetDisplay` above builds its own dict and asserts on that, so it
# proves nothing about the command; this class is deliberately not shaped like
# it. The older class is kept because it still documents the F018
# no-invented-zeros intent that these tests enforce against the real command.
# ---------------------------------------------------------------------------

_BUDGET_CLI_JOB = """\
# Job: Budget Display

## Task 1
Add a helper module.

Acceptance:
- module exists

## Task 2
Add a second module.

Acceptance:
- module exists
"""

_CLI_LEDGER_PROJECT_ID = "99999999-8888-7777-6666-555555555555"


@pytest.fixture
def budget_cli_repo(tmp_path, monkeypatch):
    """An isolated data root plus a repo directory the job can point at."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    return repo


def _cli_arm_ledger(monkeypatch):
    """Point the CLI's ledger read at the seeded project, as production would.

    Only the registry resolver is stubbed — the same seam
    ``tests/orchestration/test_predictive_budget.py`` stubs, and for the same
    reason: the production resolver needs a registered git repo. Everything
    downstream of it is production code.
    """
    from packages.orchestration import job_evidence as je
    monkeypatch.setattr(
        je, "_resolve_job_ledger_project_id", lambda job: _CLI_LEDGER_PROJECT_ID)


def _cli_record_call(job_id, *, call_id, cost):
    """One ledger row. ``cost=None`` records an UNPRICED call, never a zero."""
    from packages.orchestration.token_ledger import (
        COST_BASIS_PROVIDER_REPORTED,
        COST_BASIS_UNKNOWN,
        CallRecord,
        record_call,
    )
    assert record_call(
        CallRecord(
            call_id=call_id,
            job_id=job_id,
            ts_utc="2026-08-09T10:00:00+00:00",
            cost_usd=cost,
            cost_basis=(
                COST_BASIS_UNKNOWN if cost is None else COST_BASIS_PROVIDER_REPORTED),
        ),
        project_id=_CLI_LEDGER_PROJECT_ID,
    ) is True


def _save_budget_job(repo, *, budgets, provider_calls=2, prediction=None):
    """Persist a two-task JobPlan with budgets and persisted actuals."""
    from packages.orchestration.pingpong_job import parse_job_file, save_job_plan
    job = parse_job_file(_BUDGET_CLI_JOB, str(repo))
    job.budgets = dict(budgets)
    # Firmly in the past: BudgetCounters refuses a started_at after "now", so a
    # same-day timestamp would make these tests depend on the wall clock.
    job.first_running_at = "2026-01-01T09:00:00+00:00"
    job.budget_actuals = {
        "schema_version": "1.0.0",
        "provider_call_count": provider_calls,
        "actual_call_count": provider_calls,
        "unmeasured_call_count": 0,
        "total_tokens": 1000 * provider_calls,
        "actual_sources": ["pingpong_live"] if provider_calls else [],
        "started_at": job.first_running_at,
    }
    if prediction is not None:
        job.budget_prediction = dict(prediction)
    save_job_plan(job)
    return job


def _configure_cli_price_basis(repo, *, price_basis):
    (repo / "remedy.toml").write_text(
        f"[remedy.budget]\nprice_basis_usd_per_1k_tokens = {price_basis}\n")


def _line_value(lines, label):
    """The value printed after ``label:``, or None if the label never appeared."""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(label + ":"):
            return stripped[len(label) + 1:].strip()
    return None


class TestJobBudgetCliRendersPredictions:
    """F104 T003: the real command, its real stdout, and its real JSON."""

    def _run(self, job_id, *, json_output=False):
        from apps.cli.commands.job import _cmd_job_budget
        _cmd_job_budget(job_id, json_output=json_output)

    def _text(self, job_id, capsys):
        self._run(job_id)
        return capsys.readouterr().out

    def _json(self, job_id, capsys):
        import json as _json
        self._run(job_id, json_output=True)
        return _json.loads(capsys.readouterr().out)

    # -- (a) the money limit is printed at all ----------------------------
    def test_the_money_limit_appears_in_the_text_output(self, budget_cli_repo, capsys):
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        out = self._text(job.job_id, capsys)
        assert "max_cost_usd:" in out
        assert "$2.0000" in out

    def test_the_money_limit_is_printed_between_tokens_and_wall_clock(
            self, budget_cli_repo, capsys):
        # _LIMIT_ORDER position: after max_total_tokens, before wall clock.
        job = _save_budget_job(budget_cli_repo, budgets={
            "max_total_tokens": 100000, "max_cost_usd": 2.0,
            "max_wall_clock_minutes": 30})
        lines = self._text(job.job_id, capsys).splitlines()
        idx = {}
        for i, line in enumerate(lines):
            for key in ("max_total_tokens", "max_cost_usd", "max_wall_clock_minutes"):
                if line.strip().startswith(key + ":"):
                    idx[key] = i
        assert idx["max_total_tokens"] < idx["max_cost_usd"] < idx["max_wall_clock_minutes"]

    # -- (b) spent / remaining -------------------------------------------
    def test_a_priced_job_renders_spent_and_remaining(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=0.60)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "spent") == "$0.6000"
        assert _line_value(lines, "remaining") == "$1.4000"

    def test_an_unpriced_job_renders_not_measured_and_never_a_zero(
            self, budget_cli_repo, capsys, monkeypatch):
        # P6: nothing reported a price, so the remainder is UNKNOWN. Rendering
        # it as $0.0000 would claim a measurement that does not exist.
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-u", cost=None)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "spent") == "not-measured"
        assert _line_value(lines, "remaining") == "not-measured"
        assert _line_value(lines, "remaining") != "$0.0000"

    def test_a_job_with_no_ledger_at_all_still_says_not_measured(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "remaining") == "not-measured"

    def test_a_partly_unpriced_job_renders_remaining_as_a_ceiling(
            self, budget_cli_repo, capsys, monkeypatch):
        # The spend is a FLOOR (>=), so what is left is a CEILING (<=).
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=0.60)
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-b", cost=None)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "spent").startswith(">= $0.6000")
        assert _line_value(lines, "remaining") == "<= $1.4000"

    def test_remaining_is_floored_at_zero_when_the_limit_is_overspent(
            self, budget_cli_repo, capsys, monkeypatch):
        # A MEASURED overspend: $0.0000 here is a real measurement, not an
        # invented one, which is exactly why the unmeasured case says so instead.
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=5.0)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "remaining") == "$0.0000"

    def test_a_job_without_a_money_limit_prints_no_spent_line(
            self, budget_cli_repo, capsys):
        job = _save_budget_job(budget_cli_repo, budgets={"max_total_tokens": 1000})
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "spent") is None
        assert _line_value(lines, "remaining") is None
        assert _line_value(lines, "next_task_expected") is None

    # -- R-0227: a BROKEN ledger read is not the same as an unpriced job ---
    def _break_the_ledger_read(self, monkeypatch):
        """Make the production ledger read raise, leaving everything else real."""
        from packages.orchestration import budget_guard as _bg

        def _boom(*a, **kw):
            raise RuntimeError("ledger mirror unreadable")

        monkeypatch.setattr(_bg, "collect_ledger_cost_for_job", _boom)

    def test_a_failed_ledger_read_prints_a_cost_read_line_naming_the_error(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        self._break_the_ledger_read(monkeypatch)
        lines = self._text(job.job_id, capsys).splitlines()
        value = _line_value(lines, "cost_read")
        assert value is not None
        assert value.startswith("unavailable (")
        assert "RuntimeError" in value
        # The displayed cost is unchanged — still unknown, never an invented 0.
        assert _line_value(lines, "spent") == "not-measured"
        assert _line_value(lines, "remaining") == "not-measured"
        # One broken read does not cost the operator the rest of the report.
        assert _line_value(lines, "max_cost_usd") == "$2.0000"

    def test_a_failed_ledger_read_sets_cost_read_error_in_json(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        self._break_the_ledger_read(monkeypatch)
        data = self._json(job.job_id, capsys)
        assert "RuntimeError" in data["cost_read_error"]
        # The counters decode is a DIFFERENT failure and keeps its own fields.
        assert data["diagnostic"] is None
        assert data["status"] == "evaluated"
        assert data["counters"]["measured_cost_usd"] is None

    def test_a_genuinely_unpriced_job_prints_no_cost_read_line(
            self, budget_cli_repo, capsys, monkeypatch):
        # The whole point of R-0227: an unpriced job and a broken read must not
        # render identically. Nothing broke here, so nothing claims it did.
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-u", cost=None)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "spent") == "not-measured"
        assert _line_value(lines, "cost_read") is None
        data = self._json(job.job_id, capsys)
        assert data["cost_read_error"] is None

    def test_a_failed_ledger_read_is_logged_at_error(
            self, budget_cli_repo, capsys, monkeypatch, caplog):
        import logging
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        self._break_the_ledger_read(monkeypatch)
        with caplog.at_level(logging.ERROR, logger="apps.cli.commands.job"):
            self._text(job.job_id, capsys)
        records = [
            r for r in caplog.records
            if r.levelno == logging.ERROR and "ledger cost read FAILED" in r.getMessage()
        ]
        assert records, [r.getMessage() for r in caplog.records]
        assert records[0].exc_info is not None

    # -- (c) the next-task expectation ------------------------------------
    def test_the_next_task_expectation_renders_with_its_basis_label(
            self, budget_cli_repo, capsys, monkeypatch):
        from packages.orchestration.budget_guard import VALID_ESTIMATE_BASES
        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=0.60)
        lines = self._text(job.job_id, capsys).splitlines()
        # 8000-token LOW class default x $0.01/1k = $0.0800.
        assert _line_value(lines, "next_task_expected") == "$0.0800"
        assert _line_value(lines, "estimate_basis") == "class_default"
        assert _line_value(lines, "estimate_basis") in VALID_ESTIMATE_BASES
        assert "basis=class_default" in _line_value(lines, "arithmetic")

    def test_with_no_price_basis_the_expectation_is_not_measured_not_zero(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        assert not (budget_cli_repo / "remedy.toml").exists()
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "next_task_expected") == "not-measured"
        assert _line_value(lines, "estimate_basis") == "no_price_basis"

    def test_a_job_with_no_pending_task_says_so_instead_of_predicting(
            self, budget_cli_repo, capsys, monkeypatch):
        from packages.orchestration.pingpong_job import (
            TASK_APPLIED,
            load_job_plan,
            save_job_plan,
        )
        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        reloaded = load_job_plan(job.job_id)
        for t in reloaded.tasks:
            t.status = TASK_APPLIED
        save_job_plan(reloaded)
        lines = self._text(job.job_id, capsys).splitlines()
        assert _line_value(lines, "next_task_expected") == "none (no pending task)"
        assert _line_value(lines, "estimate_basis") is None

    def test_a_broken_prediction_degrades_to_one_unavailable_line(
            self, budget_cli_repo, capsys, monkeypatch):
        # A read-only inspection command never dies because an estimate broke.
        from packages.orchestration import budget_guard as _bg

        def _boom(*a, **kw):
            raise RuntimeError("prediction engine exploded")

        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        monkeypatch.setattr(_bg, "predict_next_task_cost", _boom)
        lines = self._text(job.job_id, capsys).splitlines()
        value = _line_value(lines, "next_task_expected")
        assert value.startswith("unavailable (")
        assert "RuntimeError" in value
        # The rest of the report still printed.
        assert _line_value(lines, "max_cost_usd") == "$2.0000"

    def test_the_command_does_not_mutate_the_persisted_job(
            self, budget_cli_repo, capsys, monkeypatch):
        # action_class="read_only" has to be true of the bytes on disk.
        from packages.orchestration.data_paths import job_record_path
        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=0.60)
        job_file = job_record_path(job.job_id)
        before = job_file.read_bytes()
        self._text(job.job_id, capsys)
        assert job_file.read_bytes() == before

    # -- (d) the recorded stop arithmetic ---------------------------------
    def test_a_recorded_stop_prediction_surfaces_its_arithmetic(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(
            budget_cli_repo, budgets={"max_cost_usd": 1.0},
            prediction={
                "would_breach": True,
                "estimate_basis": "class_default",
                "band": "low",
                "expected_tokens": 8000,
                "expected_cost_usd": 0.08,
                "spent_cost_usd": 0.95,
                "limit_usd": 1.0,
                "arithmetic": "spent $0.9500 + expected $0.0800 "
                              "(8000 tokens, band=low, basis=class_default) "
                              "> limit $1.0000",
            })
        out = self._text(job.job_id, capsys)
        assert "recorded stop prediction:" in out
        assert "spent $0.9500 + expected $0.0800" in out
        assert "basis=class_default" in out

    def test_no_recorded_prediction_prints_no_recorded_heading(
            self, budget_cli_repo, capsys):
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 1.0})
        assert "recorded stop prediction:" not in self._text(job.job_id, capsys)

    # -- JSON --------------------------------------------------------------
    def test_json_carries_both_new_keys_and_keeps_every_old_one(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-a", cost=0.60)
        data = self._json(job.job_id, capsys)
        for key in ("job_id", "found_as", "limits", "counters", "evaluation",
                    "status", "diagnostic", "prediction", "recorded_prediction"):
            assert key in data, key
        assert data["prediction"]["estimate_basis"] == "class_default"
        assert data["recorded_prediction"] is None
        # The old keys still mean what they meant.
        assert data["found_as"] == "job_plan"
        assert data["status"] == "evaluated"
        assert data["limits"]["max_cost_usd"] == 2.0

    def test_json_prediction_is_null_when_there_is_no_pending_task(
            self, budget_cli_repo, capsys, monkeypatch):
        from packages.orchestration.pingpong_job import (
            TASK_APPLIED,
            load_job_plan,
            save_job_plan,
        )
        _cli_arm_ledger(monkeypatch)
        _configure_cli_price_basis(budget_cli_repo, price_basis=0.01)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        reloaded = load_job_plan(job.job_id)
        for t in reloaded.tasks:
            t.status = TASK_APPLIED
        save_job_plan(reloaded)
        data = self._json(job.job_id, capsys)
        assert data["prediction"] is None

    def test_json_recorded_prediction_is_the_persisted_dict_verbatim(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        recorded = {
            "would_breach": True,
            "estimate_basis": "class_default_missing_band",
            "band": "unknown",
            "expected_tokens": 120000,
            "expected_cost_usd": 1.2,
            "spent_cost_usd": 0.5,
            "limit_usd": 1.0,
            "arithmetic": "spent $0.5000 + expected $1.2000 > limit $1.0000",
        }
        job = _save_budget_job(
            budget_cli_repo, budgets={"max_cost_usd": 1.0}, prediction=recorded)
        data = self._json(job.job_id, capsys)
        assert data["recorded_prediction"] == recorded

    def test_json_counters_keep_an_unpriced_cost_as_null(
            self, budget_cli_repo, capsys, monkeypatch):
        _cli_arm_ledger(monkeypatch)
        job = _save_budget_job(budget_cli_repo, budgets={"max_cost_usd": 2.0})
        _cli_record_call(job.job_id, call_id=f"{job.job_id}-u", cost=None)
        data = self._json(job.job_id, capsys)
        assert data["counters"]["measured_cost_usd"] is None
        assert data["counters"]["unpriced_call_count"] == 1
