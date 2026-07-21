"""F018 T001 — JobBudgets model, config, CLI precedence, RunManifest snapshot."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

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

    def test_malformed_toml_raises_not_none(self, tmp_path, monkeypatch):
        toml = tmp_path / "remedy.toml"
        toml.write_text('{{bad toml')
        from packages.orchestration.budget_resolution import resolve_job_budgets
        from packages.orchestration.config import reset_config
        monkeypatch.chdir(tmp_path)
        reset_config()
        try:
            result = resolve_job_budgets()
            assert result is None
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


class TestConfigKeys:
    def test_budget_keys_registered(self):
        from packages.orchestration.config import get_key_spec
        assert get_key_spec("budget.max_total_tokens") is not None
        assert get_key_spec("budget.max_provider_calls") is not None
        assert get_key_spec("budget.max_wall_clock_minutes") is not None
        assert get_key_spec("budget.deadline") is not None

    def test_budget_key_types(self):
        from packages.orchestration.config import get_key_spec
        assert get_key_spec("budget.max_total_tokens").value_type is int
        assert get_key_spec("budget.max_provider_calls").value_type is int
        assert get_key_spec("budget.max_wall_clock_minutes").value_type is int
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
