"""DECISION F280 D3 — `remedy job budget <id> set <field> <value>`, the one budget write.

Deleting `contract set` left no command that raises `max_test_runs`, so `remedy test run` was
refused for every job nobody fixed by hand (R-0906); deleting `token budget-set` left the per-job
token budget profile with no writer (R-0909). Every test here drives `apps.cli.grouped.main`
against its own data root and reads the result back through the function that consults it.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from apps.cli.grouped import main
from packages.orchestration.data_paths import job_record_path
from packages.orchestration.pingpong_job import JobPlan, require_job_plan, save_job_plan
from packages.orchestration.run_contract import (
    ContractAction,
    RunUsage,
    build_default_run_contract,
    evaluate_run_action,
    load_contract,
    save_contract,
)
from packages.orchestration.test_execution_service import TestExecutionRequest, execute_test_run
from packages.orchestration.token_economy import load_token_budget_profile, token_economy_report

#: What a zero or exhausted test-run budget names as its next safe action (S5).
_TEST_BUDGET_NEXT = "remedy job budget <job_id> set max_test_runs <n>"
_SET_FORM = "remedy job budget <job_id> set <field> <value>"


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _job(tmp_path: Path, *, budgets: dict | None = None) -> JobPlan:
    """A persisted job allowed to run tests against an empty repository, with no contract."""
    repo = tmp_path / "repo"
    repo.mkdir(exist_ok=True)
    job = JobPlan(job_title="budget set")
    job.metadata["target_repo"] = str(repo)
    job.metadata["permissions"] = {"repo_test_run": "allow"}
    job.budgets = budgets
    save_job_plan(job)
    return job


def _cli(*argv: str) -> int:
    try:
        main(list(argv))
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1
    return 0


def _profiles(data_root: Path) -> list[Path]:
    return sorted(data_root.rglob("budget_profile.json"))


def _test_run(job: JobPlan):
    return execute_test_run(TestExecutionRequest(job_id=job.job_id, source="cli_v1"))


class TestR0906TheTestRunBudget:
    def test_raising_max_test_runs_takes_test_run_past_the_contract_gate(
            self, data_root, tmp_path, capsys):
        job = _job(tmp_path)
        refused = _test_run(job)
        assert (refused.status, refused.stop_reason) == ("blocked", "contract_exhausted")

        assert _cli("job", "budget", job.job_id, "set", "max_test_runs", "2") == 0

        assert load_contract(require_job_plan(job.job_id)).max_test_runs == 2
        # The empty repository stops the run at discovery, AFTER the contract gate.
        assert _test_run(job).stop_reason == "no_test_command_discovered"
        assert capsys.readouterr().out == (
            f"Job {job.job_id}: max_test_runs 0 -> 2 (run_contract).\n")
        assert _profiles(data_root) == []

    def test_a_persisted_contract_keeps_every_other_field(self, data_root, tmp_path):
        job = _job(tmp_path)
        save_contract(job, replace(build_default_run_contract(job), max_loops=7, notes="kept"))
        save_job_plan(job)

        assert _cli("job", "budget", job.job_id, "set", "max_test_runs", "3") == 0

        stored = load_contract(require_job_plan(job.job_id))
        assert (stored.max_test_runs, stored.max_loops, stored.notes) == (3, 7, "kept")

    def test_json_names_job_field_old_new_and_store(self, data_root, tmp_path, capsys):
        job = _job(tmp_path)
        assert _cli("job", "budget", job.job_id, "set", "max_loops", "4", "--json") == 0
        assert json.loads(capsys.readouterr().out) == {
            "job_id": job.job_id, "field": "max_loops", "old": 10, "new": 4,
            "store": "run_contract"}


class TestR0909TheTokenBudgetProfile:
    def test_max_context_tokens_reads_back_through_the_token_economy_report(
            self, data_root, tmp_path, capsys):
        job = _job(tmp_path)
        record = job_record_path(job.job_id).read_bytes()

        assert _cli("job", "budget", job.job_id, "set", "max_context_tokens", "1234") == 0

        assert token_economy_report(job.job_id)["budget_profile"]["max_context_tokens"] == 1234
        assert load_token_budget_profile(job.job_id).max_context_tokens == 1234
        assert capsys.readouterr().out == (
            f"Job {job.job_id}: max_context_tokens 32000 -> 1234 (token_budget_profile).\n")
        assert job_record_path(job.job_id).read_bytes() == record


class TestRefusals:
    @pytest.mark.parametrize(("argv", "names"), [
        (("set", "max_widgets", "3"), "Settable: max_loops, max_test_runs"),
        (("set", "max_test_runs", "-1"), "max_test_runs must be >= 0"),
        (("set", "max_context_tokens", "0"), "max_context_tokens must be >= 1"),
        (("set", "max_test_runs", "two"), "Settable: max_loops, max_test_runs"),
        (("set", "max_total_tokens", "5000"), "remedy job run <job_id> --max-total-tokens <value>"),
        (("raise", "max_test_runs", "2"), _SET_FORM),
        (("set", "max_test_runs"), _SET_FORM),
    ], ids=["unknown-field", "contract-below-floor", "token-below-floor", "non-integer",
            "job-budgets-field", "action-not-set", "missing-value"])
    def test_each_exits_2_names_the_way_out_and_writes_no_store(
            self, data_root, tmp_path, capsys, argv, names):
        job = _job(tmp_path)
        record = job_record_path(job.job_id).read_bytes()

        assert _cli("job", "budget", job.job_id, *argv) == 2

        assert names in capsys.readouterr().err
        assert job_record_path(job.job_id).read_bytes() == record
        assert _profiles(data_root) == []

    def test_an_unknown_job_gets_the_show_forms_not_found_error(self, data_root, capsys):
        missing = "00000000-0000-4000-8000-000000000000"
        assert _cli("job", "budget", missing) == 1
        shown = capsys.readouterr().err

        assert _cli("job", "budget", missing, "set", "max_test_runs", "2") == 1

        assert capsys.readouterr().err == shown == f"Error: No job matches {missing!r}. Try: remedy job list.\n"
        assert not job_record_path(missing).exists()
        assert _profiles(data_root) == []


class TestTheShowFormIsUnchanged:
    def test_plain_job_budget_prints_the_limits_and_writes_nothing(
            self, data_root, tmp_path, capsys):
        job = _job(tmp_path, budgets={"max_total_tokens": 5000})
        record = job_record_path(job.job_id).read_bytes()

        assert _cli("job", "budget", job.job_id) == 0

        assert capsys.readouterr().out == (
            f"Budget for job {job.job_id[:8]} (job_plan):\n"
            "  max_total_tokens:      5000\n"
            "  counters:              no_runs\n")
        assert job_record_path(job.job_id).read_bytes() == record
        assert _profiles(data_root) == []


class TestTheRefusalNamesTheWrite:
    def test_a_zero_test_budget_names_job_budget_set(self):
        decision = evaluate_run_action(
            build_default_run_contract(JobPlan(job_title="zero")), ContractAction.RUN_TEST)
        assert (decision.allowed, decision.next_safe_action) == (False, _TEST_BUDGET_NEXT)

    def test_an_exhausted_test_budget_names_job_budget_set(self):
        contract = replace(build_default_run_contract(JobPlan(job_title="spent")), max_test_runs=2)
        decision = evaluate_run_action(
            contract, ContractAction.RUN_TEST, usage=RunUsage(test_runs_used=2))
        assert decision.reason == "Test runs 2 >= max_test_runs 2"
        assert decision.next_safe_action == _TEST_BUDGET_NEXT

    def test_test_run_names_the_write_with_the_jobs_id(self, data_root, tmp_path):
        job = _job(tmp_path)
        result = _test_run(job)
        assert result.next_safe_action == _TEST_BUDGET_NEXT
        assert result.contract_guidance == f"remedy job budget {job.job_id} set max_test_runs <n>"
