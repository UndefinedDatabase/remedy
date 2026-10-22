"""F296 T002b, DECISION F296 D4 — what each model tier did for a task, as evidence and in the ledger.

The rows are read from constructed run records first, then from a real escalating run that a job's
evidence export writes beside the task's other evidence and mirrors into the cost ledger.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from packages.orchestration import tier_outcomes
from packages.orchestration.tier_outcomes import (
    TIER_OUTCOMES_FILENAME,
    TierOutcomeRow,
    TierOutcomeSummary,
    query_tier_outcomes,
    record_tier_outcomes,
    rows_from_evidence_file,
    tier_outcome_rows,
    write_task_tier_outcomes,
)
from tests.orchestration.test_tier_escalation import TestARealRun


def _attempt(round_number, role, cost=0.01, *, retry=False):
    return {"round": round_number, "role": role, "is_retry": retry, "is_parse_retry": False,
            "total_cost_usd": cost}


def _record(*, escalations=(), attempts=None, final_status="staged_review_passed", total=3):
    return {
        "run_id": "run-1", "final_status": final_status, "total_rounds": total,
        "tier_ladder": {"enabled": True, "builder_tier": "cheap", "reviewer_tier": "cheap",
                        "escalations": list(escalations)},
        "provider_evidence": {"provider_attempts": attempts if attempts is not None else [
            _attempt(1, "builder"), _attempt(1, "reviewer"), _attempt(2, "builder", retry=True),
            _attempt(2, "builder"), _attempt(2, "reviewer"), _attempt(3, "builder", 0.1),
            _attempt(3, "reviewer", 0.1)]},
    }


STEP = {"round": 3, "reason": "test_failed", "builder_from": "cheap", "builder_to": "mid",
        "reviewer_from": "cheap", "reviewer_to": "mid"}


def _rows(record, task_class="standard_build"):
    return tier_outcome_rows(record, job_id="job-1", task_id="T001", task_class=task_class)


class TestTheRows:
    def test_an_escalated_run_gives_one_row_per_tier(self):
        cheap, mid = _rows(_record(escalations=[STEP]))
        assert (cheap.tier, cheap.reviewer_tier, cheap.first_round, cheap.last_round, cheap.rounds) == (
            "cheap", "cheap", 1, 2, 2)
        assert (cheap.outcome, cheap.reason, cheap.retries, cheap.cost_usd, cheap.cost_basis) == (
            "escalated", "test_failed", 1, 0.05, "provider_reported")
        assert (mid.tier, mid.reviewer_tier, mid.first_round, mid.last_round, mid.rounds) == ("mid", "mid", 3, 3, 1)
        assert (mid.outcome, mid.reason, mid.retries, mid.cost_usd) == ("staged_review_passed", "", 0, 0.2)
        assert {row.task_class for row in (cheap, mid)} == {"standard_build"}

    def test_a_run_that_never_moved_gives_one_row_with_its_status(self):
        (row,) = _rows(_record(final_status="repair_exhausted", total=2,
                               attempts=[_attempt(1, "builder"), _attempt(2, "builder")]))
        assert (row.tier, row.rounds, row.outcome, row.reason, row.cost_usd) == (
            "cheap", 2, "repair_exhausted", "", 0.02)

    def test_a_tier_whose_calls_did_not_all_report_a_cost_has_none(self):
        attempts = [_attempt(1, "builder"), _attempt(1, "reviewer", None), _attempt(2, "builder", True)]
        (row,) = _rows(_record(attempts=attempts, total=2))
        assert (row.cost_usd, row.cost_basis) == (None, "unknown")
        (empty,) = _rows(_record(attempts=[], total=1))
        assert (empty.cost_usd, empty.cost_basis) == (None, "unknown")

    def test_a_run_without_known_tiers_gives_no_row(self):
        assert _rows({"run_id": "r", "rounds": []}) == []
        assert _rows({"tier_ladder": {"builder_tier": None, "reviewer_tier": "mid"}}) == []

    def test_two_escalations_give_three_rows_in_round_order(self):
        top = {**STEP, "round": 5, "reason": "no_progress", "builder_from": "mid", "builder_to": "top",
               "reviewer_from": "mid", "reviewer_to": "top"}
        rows = _rows(_record(escalations=[top, STEP], attempts=[], total=5))
        assert [(r.tier, r.first_round, r.last_round, r.outcome, r.reason) for r in rows] == [
            ("cheap", 1, 2, "escalated", "test_failed"), ("mid", 3, 4, "escalated", "no_progress"),
            ("top", 5, 5, "staged_review_passed", "")]


class TestTheLedger:
    def test_the_rows_round_trip_and_a_re_export_replaces_its_own(self, tmp_path):
        path = tmp_path / "ledger.sqlite"
        rows = _rows(_record(escalations=[STEP]))
        assert record_tier_outcomes(rows, path=path) == 2
        record_tier_outcomes(rows, path=path)
        other = _rows(_record(final_status="repair_exhausted", attempts=[]), task_class="boilerplate")
        record_tier_outcomes([TierOutcomeRow(**{**r.__dict__, "task_id": "T002"}) for r in other], path=path)
        assert query_tier_outcomes(path=path) == [
            TierOutcomeSummary(task_class="boilerplate", tier="cheap", task_runs=1, outcomes={"repair_exhausted": 1},
                               rounds=3, retries=0, cost_usd=None, priced_runs=0),
            TierOutcomeSummary(task_class="standard_build", tier="cheap", task_runs=1, outcomes={"escalated": 1},
                               rounds=2, retries=1, cost_usd=0.05, priced_runs=1),
            TierOutcomeSummary(task_class="standard_build", tier="mid", task_runs=1,
                               outcomes={"staged_review_passed": 1}, rounds=1, retries=0, cost_usd=0.2,
                               priced_runs=1),
        ]

    def test_the_table_carries_its_own_schema_key(self, tmp_path):
        import sqlite3

        path = tmp_path / "ledger.sqlite"
        record_tier_outcomes([], path=path)
        with sqlite3.connect(path) as conn:
            meta = dict(conn.execute("SELECT key, value FROM meta").fetchall())
        assert meta[tier_outcomes.TIER_OUTCOMES_SCHEMA_KEY] == "1"


class TestTheEvidence:
    def test_the_file_is_written_read_back_and_mirrored(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        task = SimpleNamespace(task_id="T001", task_class="standard_build")
        out = tmp_path / "task_runs" / "T001"
        out.mkdir(parents=True)
        written = write_task_tier_outcomes(_record(escalations=[STEP]), task, out, "task_runs/T001", "proj-1", "job-1")
        assert written == {f"task_runs/T001/{TIER_OUTCOMES_FILENAME}": str(out / TIER_OUTCOMES_FILENAME)}
        on_disk = json.loads((out / TIER_OUTCOMES_FILENAME).read_text(encoding="utf-8"))
        assert [row["tier"] for row in on_disk["rows"]] == ["cheap", "mid"]
        assert rows_from_evidence_file(out / TIER_OUTCOMES_FILENAME) == _rows(_record(escalations=[STEP]))
        assert [(s.tier, s.task_runs) for s in query_tier_outcomes(project_id="proj-1")] == [("cheap", 1), ("mid", 1)]

    def test_no_ledger_target_writes_the_file_and_touches_no_ledger(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        task = SimpleNamespace(task_id="T001", task_class="standard_build")
        written = write_task_tier_outcomes(_record(), task, tmp_path, "task_runs/T001", None, "job-1")
        assert list(written) == [f"task_runs/T001/{TIER_OUTCOMES_FILENAME}"]
        assert not (tmp_path / "data").exists()

    def test_a_run_without_tiers_writes_nothing(self, tmp_path):
        task = SimpleNamespace(task_id="T001", task_class="standard_build")
        assert write_task_tier_outcomes({"rounds": []}, task, tmp_path, "task_runs/T001", "p", "job-1") == {}
        assert list(tmp_path.iterdir()) == []

    def test_a_mirror_that_fails_never_fails_the_export(self, tmp_path, monkeypatch, caplog):
        def broken(rows, **kwargs):
            raise OSError("disk full")

        monkeypatch.setattr(tier_outcomes, "record_tier_outcomes", broken)
        task = SimpleNamespace(task_id="T001", task_class="standard_build")
        written = write_task_tier_outcomes(_record(), task, tmp_path, "task_runs/T001", "proj-1", "job-1")
        assert list(written) == [f"task_runs/T001/{TIER_OUTCOMES_FILENAME}"]
        assert "tier outcome mirror FAILED" in caplog.text

    def test_a_job_export_writes_the_rows_of_a_real_escalated_run(self, monkeypatch, tmp_path):
        from packages.orchestration.job_evidence import _write_task_run_evidence

        result, _, _ = TestARealRun()._run(monkeypatch, tmp_path)
        task = SimpleNamespace(task_id="T001", run_id=result.run_id, task_class="standard_build", status="passed")
        written: dict[str, str] = {}
        _write_task_run_evidence(task, str(tmp_path / "evidence"), written, ledger_project_id="proj-1", job_id="job-1")
        assert f"task_runs/T001/{TIER_OUTCOMES_FILENAME}" in written
        assert [(s.task_class, s.tier, s.outcomes) for s in query_tier_outcomes(project_id="proj-1")] == [
            ("standard_build", "cheap", {"escalated": 1}), ("standard_build", "mid", {"staged_review_passed": 1})]


@pytest.mark.parametrize("enabled", ["true", "false"])
def test_a_run_on_tier_models_records_its_tiers_whether_or_not_it_may_escalate(monkeypatch, tmp_path, enabled):
    _, _, record = TestARealRun()._run(monkeypatch, tmp_path, enabled=enabled)
    expected = [{**STEP}] if enabled == "true" else []
    assert record["tier_ladder"] == {"enabled": enabled == "true", "builder_tier": "cheap", "reviewer_tier": "cheap",
                                     "escalations": expected}


def test_a_run_off_the_tier_models_records_no_tiers(monkeypatch, tmp_path):
    import packages.orchestration.pingpong_loop as loop

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    result = loop.run_pingpong("Fix README", str(repo), builder_name="fake", reviewer_name="fake")
    assert "tier_ladder" not in loop.export_pingpong_json(result)
