"""`budget_profiles`: the provider class of a job, the profiles and the limits a run reads (F310)."""
from __future__ import annotations

import pytest

from packages.core.models import JobBudgets
from packages.orchestration import budget_profiles as BP
from packages.orchestration.budget_resolution import BudgetConfigError
from packages.orchestration.execution_config import ExecutionConfig
from packages.orchestration.pingpong_job import JobPlan


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch, tmp_path):
    """No configuration of the operator's reaches a test: no budget variable, no user file, and a
    project file of an empty folder (the way `test_config.py` isolates the loader)."""
    import os

    for name in [n for n in os.environ if n.startswith("REMEDY_BUDGET_")]:
        monkeypatch.delenv(name)
    empty = tmp_path / "no-config"
    empty.mkdir()
    monkeypatch.setattr("packages.orchestration.config._DEFAULT_USER_PATH", empty / "user.toml")
    monkeypatch.setattr("packages.orchestration.config._DEFAULT_PROJECT_PATH", empty / "remedy.toml")


def _job(builder="pi", reviewer="pi", repair="", budgets=None, repo_path=""):
    config = ExecutionConfig(builder=builder, reviewer=reviewer, repair_provider=repair)
    return JobPlan(execution_config=config, budgets=budgets, repo_path=repo_path)


@pytest.mark.parametrize(("provider", "model", "expected"), [
    ("ollama", None, "local"),
    ("ollama", "", "local"),
    ("pi", None, "local"),
    ("pi", "muse-glimmer:latest", "local"),
    ("ollama", "muse-glimmer:latest", "local"),
    ("pi", "gpt-oss:120b-cloud", "paid"),
    ("ollama", "qwen3-coder:480b-cloud", "paid"),
    ("claude", None, "paid"),
    ("claude-cli", None, "paid"),
    ("fake", None, "paid"),
    ("no-such-provider", None, "paid"),
])
def test_provider_class_follows_where_the_model_runs(provider, model, expected):
    assert BP.provider_class(provider, model) == expected


@pytest.mark.parametrize(("job", "expected"), [
    (_job("pi", "pi"), "local"),
    (_job("pi", "claude"), "paid"),
    (_job("pi", "pi", repair="claude"), "paid"),
    (_job("pi", "pi", repair=""), "local"),
    (JobPlan(execution_config=None), "paid"),
])
def test_a_job_is_local_only_when_every_role_is(job, expected):
    assert BP.job_provider_class(job) == expected


def test_a_local_job_with_nothing_set_gets_the_local_profile():
    job = _job()
    effective = BP.effective_job_budgets(job)
    assert effective is not None
    assert (effective.max_total_tokens, effective.max_provider_calls,
            effective.max_wall_clock_minutes) == (1500000, 200, 480)
    assert effective.max_cost_usd is None and effective.deadline is None
    assert effective.min_free_disk_bytes is None
    assert job.budgets is None


def test_a_paid_job_with_nothing_set_has_no_limits():
    job = _job("claude", "claude")
    assert BP.effective_job_budgets(job) is None
    assert job.budgets is None


def test_the_jobs_own_limit_wins_and_the_profile_fills_the_rest():
    own = {"max_wall_clock_minutes": 12}
    job = _job(budgets=own)
    effective = BP.effective_job_budgets(job)
    assert (effective.max_total_tokens, effective.max_provider_calls,
            effective.max_wall_clock_minutes) == (1500000, 200, 12)
    assert job.budgets == {"max_wall_clock_minutes": 12}


def test_a_job_that_holds_a_budgets_instance_is_taken_as_it_is():
    job = _job(budgets=JobBudgets(max_provider_calls=7))
    assert BP.effective_job_budgets(job).max_provider_calls == 7


def test_a_configured_budget_beats_the_profile(monkeypatch):
    monkeypatch.setenv("REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES", "30")
    job = _job()
    assert BP.effective_job_budgets(job).max_wall_clock_minutes == 30
    assert job.budgets is None


def test_a_profile_value_can_be_configured(monkeypatch):
    monkeypatch.setenv("REMEDY_BUDGET_PROFILE_LOCAL_MAX_WALL_CLOCK_MINUTES", "600")
    job = _job()
    assert BP.effective_job_budgets(job).max_wall_clock_minutes == 600
    assert job.budgets is None


def test_the_paid_profile_reaches_a_paid_job(monkeypatch):
    monkeypatch.setenv("REMEDY_BUDGET_PROFILE_PAID_MAX_COST_USD", "2.5")
    job = _job("claude", "claude")
    assert BP.effective_job_budgets(job).max_cost_usd == 2.5
    assert job.budgets is None


def test_a_malformed_profile_value_raises(monkeypatch):
    monkeypatch.setenv("REMEDY_BUDGET_PROFILE_LOCAL_MAX_PROVIDER_CALLS", "-3")
    job = _job()
    with pytest.raises(BudgetConfigError):
        BP.effective_job_budgets(job)
    assert job.budgets is None


def test_the_offer_names_both_profiles_with_their_numbers():
    assert BP.budget_profiles_offer() == {
        "local": {"max_total_tokens": 1500000, "max_provider_calls": 200,
                  "max_wall_clock_minutes": 480},
        "paid": {"max_total_tokens": None, "max_provider_calls": None,
                 "max_wall_clock_minutes": None, "max_cost_usd": None},
    }


def _git_repo_with_a_task(tmp_path):
    import subprocess

    from packages.orchestration.pingpong_job import parse_job_file

    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "README.md").write_text("# docs\n")
    for args in (["init", "-q"], ["config", "user.email", "t@test"], ["config", "user.name", "T"],
                 ["add", "-A"], ["commit", "-qm", "base"]):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)
    return parse_job_file("# Job: profile-test\n\n## Task 1\nTouch docs/README.md\n\n"
                          "Acceptance:\n- file exists\n", str(repo))


def test_run_job_still_blocks_a_job_whose_budgets_hold_an_unknown_field():
    from packages.orchestration.pingpong_job import _persist_job, run_job

    job = JobPlan(budgets={"max_provider_calls": 5, "unknown_key": 42})
    _persist_job(job)
    result = run_job(job.job_id)
    assert result.state == "blocked"
    assert "corrupt_budget_state" in result.error


def test_run_job_judges_a_local_job_against_the_local_profile(monkeypatch, tmp_path):
    from packages.orchestration import safe_points
    from packages.orchestration.pingpong_job import _persist_job, run_job
    from packages.orchestration.pingpong_provider import FakeProvider

    job = _git_repo_with_a_task(tmp_path)
    job.execution_config = ExecutionConfig(builder="pi", reviewer="pi")
    _persist_job(job)
    seen = []
    real_should_stop = safe_points.should_stop

    def recording_should_stop(job_id, **kwargs):
        seen.append(kwargs["budgets"])
        return real_should_stop(job_id, **kwargs)

    monkeypatch.setattr(safe_points, "should_stop", recording_should_stop)
    result = run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                     reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99))
    assert seen, f"run_job never reached a safe point: {result.state} {result.error}"
    assert (seen[0].max_total_tokens, seen[0].max_provider_calls,
            seen[0].max_wall_clock_minutes) == (1500000, 200, 480)
    assert result.budgets is None


def test_a_plans_suggested_budgets_never_become_the_jobs_limits(monkeypatch, tmp_path):
    import subprocess

    from packages.orchestration.job_plan import TaskPlanResult
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.schemas.models import TaskPlan
    from tests.cli.test_plan_approval import (
        _CLI,
        _env,
        _git_repo,
        _setup_llm_mocks,
        _shape_order,
    )

    repo = _git_repo(tmp_path)
    subprocess.run([*_CLI, "init"], capture_output=True, text=True, timeout=30, cwd=str(repo),
                   env=_env(tmp_path), stdin=subprocess.DEVNULL)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    plan = TaskPlan(
        schema_v="task_plan_v1",
        tasks=[{"id": "T001", "title": "Do thing", "goal": "A goal", "acceptance": ["Done"],
                "depends_on": [], "est_tokens_band": "M", "files_hint": []}],
        risks=[],
        budgets={"max_total_tokens": 100000, "max_provider_calls": 42},
    )
    _setup_llm_mocks(monkeypatch, plan_succeeds=True)
    monkeypatch.setattr("packages.orchestration.job_plan.plan_job_llm",
                        lambda intake, call_fn, **kw: TaskPlanResult(plan=plan, source="llm", calls=1))
    monkeypatch.chdir(str(repo))

    shaped = _shape_order(repo, "test mission")

    assert load_job_plan(shaped.to_json()["job_id"]).budgets is None
