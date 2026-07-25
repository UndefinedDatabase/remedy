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
