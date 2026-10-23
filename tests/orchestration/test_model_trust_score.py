"""F133 T002 — the trust home measured on a constructed history (DECISION F133 D2).

Every ledger row here is written through `token_ledger.record_call`, every job record as a real
job's `tasks[].status`/`repair_rounds_used`, and every attempt and post-mortem under the task run's
own evidence tree (`provider_evidence.json`, `streams/<role>/round-NN/.../postmortem.json`) exactly
as the job path writes them — so the table is measured exactly as a project's would be.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_evidence_dir, job_record_path
from packages.orchestration.failure_postmortem import FailureClass, PostmortemV1, write_postmortem
from packages.orchestration.model_trust_score import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    MODEL_TRUST_SNAPSHOT_FILENAME,
    TRUST_COST_BASIS_MIXED,
    TRUST_COST_BASIS_PRICE_TABLE,
    TRUST_COST_BASIS_TOKENS,
    TRUST_RECOMMENDATION_LEADER,
    TRUST_RECOMMENDATION_NO_MARGIN,
    TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE,
    ModelTrustRow,
    ModelTrustTable,
    TrustConfigError,
    TrustMetric,
    build_model_trust_table,
    load_model_trust_table,
    model_trust_snapshot_path,
    model_trust_table_from_json,
    resolve_trust_settings,
    trust_leader,
)
from packages.orchestration.token_ledger import CallRecord, record_call, token_ledger_path_for

PROJECT = "11111111-2222-3333-4444-555555555555"
NOW = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
RECENT = "2026-10-15T09:00:00+00:00"
GOLDEN = Path(__file__).parent / "fixtures" / "model_trust" / "golden.json"


def _job(root: Path, job: str, tasks: dict[str, dict]) -> None:
    path = job_record_path(job, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"tasks": [
        {"task_id": task_id, "status": info.get("status", "passed"),
         "repair_rounds_used": info.get("repair_rounds_used", 0)}
        for task_id, info in tasks.items()
    ]}
    path.write_text(json.dumps(payload), encoding="utf-8")


def _attempts(root: Path, job: str, task: str, attempts: list[dict]) -> None:
    ev_dir = job_evidence_dir(job, root) / "task_runs" / task
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "provider_evidence.json").write_text(
        json.dumps({"provider_attempts": attempts}), encoding="utf-8")


def _call(root: Path, job: str, task: str | None, role: str, seq: int | None, model: str | None,
          tokens_in: int | None, tokens_out: int | None, *, cost: float | None = None,
          cost_basis: str | None = None, ts: str = RECENT) -> None:
    call_id = f"{job}:{task}:{seq}" if seq is not None else f"{job}:{task}"
    basis = cost_basis if cost_basis is not None else ("unknown" if cost is None else "provider_reported")
    assert record_call(CallRecord(
        call_id=call_id, job_id=job, task_id=task, role=role, model=model, ts_utc=ts,
        tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost, cost_basis=basis),
        path=token_ledger_path_for(PROJECT, root))


def _postmortem(root: Path, job: str, task: str, role: str, round_no: int = 1,
                 failure_class: FailureClass = FailureClass.PARSE) -> None:
    directory = (job_evidence_dir(job, root) / "task_runs" / task / "streams" / role
                 / f"round-{round_no:02d}" / "attempt")
    directory.mkdir(parents=True, exist_ok=True)
    write_postmortem(directory, PostmortemV1(
        failure_class=failure_class, signal_source="test", job_id=job, task_id=task,
        role=role, provider="fake"), root=directory)


def _task_run(root: Path, job: str, task: str, *, status: str, repair_rounds: int,
              builder_model: str, builder_calls: list[tuple[bool, float | None]],
              reviewer_model: str, reviewer_cost: float | None) -> None:
    """One job, one task: ``builder_calls`` is ``[(is_parse_retry, cost), ...]``, in call order; the
    reviewer serves with exactly one call, after every builder call, all in one task run's seq."""
    _job(root, job, {task: {"status": status, "repair_rounds_used": repair_rounds}})
    attempts = [
        {"seq": i, "round": 1, "role": "builder", "model": builder_model, "is_parse_retry": retry}
        for i, (retry, _cost) in enumerate(builder_calls, start=1)
    ]
    attempts.append({"seq": len(builder_calls) + 1, "round": 1, "role": "reviewer",
                      "model": reviewer_model, "is_parse_retry": False})
    _attempts(root, job, task, attempts)
    for i, (_retry, cost) in enumerate(builder_calls, start=1):
        _call(root, job, task, "builder", i, None, 1000, 100, cost=cost)
    _call(root, job, task, "reviewer", len(builder_calls) + 1, None, 200, 50, cost=reviewer_cost)


def _build_golden_history(root: Path) -> None:
    """A STRONG builder (20 passes), a WEAK one (15 pass, 5 fail with a format error each), a THIN
    one (3 passes) and one reviewer serving every task."""
    for k in range(1, 21):
        _task_run(root, f"jobstrong{k:03d}", "T001", status="passed", repair_rounds=0,
                  builder_model="claude-strong-v1", builder_calls=[(False, 0.02)],
                  reviewer_model="claude-reviewer-v1", reviewer_cost=0.005)
    for k in range(1, 16):
        _task_run(root, f"jobweakpass{k:03d}", "T001", status="passed", repair_rounds=1,
                  builder_model="claude-weak-v1", builder_calls=[(False, 0.015)],
                  reviewer_model="claude-reviewer-v1", reviewer_cost=0.005)
    for k in range(1, 6):
        _task_run(root, f"jobweakfail{k:03d}", "T001", status="failed", repair_rounds=3,
                  builder_model="claude-weak-v1",
                  builder_calls=[(False, 0.015), (True, 0.015)],
                  reviewer_model="claude-reviewer-v1", reviewer_cost=0.005)
    for k in range(1, 4):
        _task_run(root, f"jobthin{k:03d}", "T001", status="passed", repair_rounds=0,
                  builder_model="claude-thin-v1", builder_calls=[(False, 0.01)],
                  reviewer_model="claude-reviewer-v1", reviewer_cost=0.005)


class TestGoldenHistory:
    def test_the_measured_table_equals_the_committed_golden(self, tmp_path):
        _build_golden_history(tmp_path)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        measured = table.to_json()
        del measured["updated_at"]
        golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
        assert measured == golden


class TestWindow:
    def test_the_window_boundary_is_inclusive_at_its_start(self, tmp_path):
        in_window_ts = (NOW - timedelta(days=90)).isoformat()
        out_of_window_ts = (NOW - timedelta(days=91)).isoformat()
        _job(tmp_path, "jobin", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobin", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m-in", "is_parse_retry": False}])
        _call(tmp_path, "jobin", "T001", "builder", 1, None, 100, 10, cost=0.01, ts=in_window_ts)
        _job(tmp_path, "jobout", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobout", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m-out", "is_parse_retry": False}])
        _call(tmp_path, "jobout", "T001", "builder", 1, None, 100, 10, cost=0.01, ts=out_of_window_ts)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert table.lookup("m-in", "builder") is not None
        assert table.lookup("m-out", "builder") is None


class TestUnsettled:
    @pytest.mark.parametrize("status", ["pending", "running", "skipped", "split", "vetoed"])
    def test_every_unsettled_status_is_kept_out_of_the_outcome_metrics(self, tmp_path, status):
        _task_run(tmp_path, "jobunsettled", "T001", status=status, repair_rounds=0,
                  builder_model="m-unsettled", builder_calls=[(False, 0.01)],
                  reviewer_model="r", reviewer_cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m-unsettled", "builder")
        assert row is not None
        assert row.pass_quota == TrustMetric(value=None, n=0)
        assert row.settled_tasks == 0 and row.thin is True
        assert row.format_error_rate == TrustMetric(value=0.0, n=1)
        assert table.unsettled_tasks == 1

    def test_a_missing_job_record_is_counted_unsettled(self, tmp_path):
        _call(tmp_path, "jobgone", "T001", "builder", 1, "m-gone", 100, 10, cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m-gone", "builder")
        assert row is not None and row.settled_tasks == 0
        assert table.unsettled_tasks == 1


class TestSettlement:
    """R-1429 survivors (1) and (2): the settled-fail and settled-pass status sets."""

    def test_a_blocked_task_is_counted_as_a_settled_fail(self, tmp_path):
        from packages.orchestration.pingpong_job import TASK_BLOCKED

        _task_run(tmp_path, "jobblocked", "T001", status=TASK_BLOCKED, repair_rounds=0,
                  builder_model="m-blocked", builder_calls=[(False, 0.01)],
                  reviewer_model="r", reviewer_cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m-blocked", "builder")
        assert row is not None
        assert row.settled_tasks == 1
        assert row.pass_quota == TrustMetric(value=0.0, n=1)
        assert table.unsettled_tasks == 0

    @pytest.mark.parametrize("status", ["applied_to_job_workspace", "completed"])
    def test_a_done_status_other_than_passed_is_counted_as_a_pass(self, tmp_path, status):
        _task_run(tmp_path, f"jobdone{status}", "T001", status=status, repair_rounds=0,
                  builder_model="m-done", builder_calls=[(False, 0.01)],
                  reviewer_model="r", reviewer_cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m-done", "builder")
        assert row is not None
        assert row.pass_quota == TrustMetric(value=1.0, n=1)
        assert table.unsettled_tasks == 0


class TestAttribution:
    def test_a_role_served_by_two_models_is_attributed_to_the_last_calls_model(self, tmp_path):
        _job(tmp_path, "jobswap", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobswap", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "model-a", "is_parse_retry": False},
            {"seq": 2, "round": 1, "role": "builder", "model": "model-b", "is_parse_retry": False},
        ])
        _call(tmp_path, "jobswap", "T001", "builder", 1, None, 100, 10, cost=0.01)
        _call(tmp_path, "jobswap", "T001", "builder", 2, None, 200, 20, cost=0.02)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row_a = table.lookup("model-a", "builder")
        row_b = table.lookup("model-b", "builder")
        assert row_a.format_error_rate == TrustMetric(value=0.0, n=1)
        assert row_a.pass_quota == TrustMetric(value=None, n=0)
        assert row_b.format_error_rate == TrustMetric(value=0.0, n=1)
        assert row_b.pass_quota == TrustMetric(value=1.0, n=1)
        assert row_b.cost_per_pass == TrustMetric(value=0.03, n=1)

    def test_a_verified_ledger_model_wins_over_the_attempts(self, tmp_path):
        _job(tmp_path, "jobverified", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobverified", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "attempt-model", "is_parse_retry": False},
        ])
        _call(tmp_path, "jobverified", "T001", "builder", 1, "verified-model", 100, 10, cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert table.lookup("verified-model", "builder") is not None
        assert table.lookup("attempt-model", "builder") is None

    def test_an_unjoinable_row_is_counted_unattributed_not_guessed(self, tmp_path):
        # A pre-R0807 one-row-per-task-run call_id: no seq, so no attempt join is even attempted.
        _job(tmp_path, "joblegacy", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _call(tmp_path, "joblegacy", "T001", "builder", None, None, 100, 10, cost=0.01)
        # A per-call row whose evidence file is simply missing.
        _job(tmp_path, "jobmissingev", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _call(tmp_path, "jobmissingev", "T001", "builder", 1, None, 100, 10, cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert table.unattributed_calls == 2
        assert table.rows == ()


class TestFormatErrors:
    def test_a_parse_retry_and_a_postmortem_each_mark_their_own_call_once(self, tmp_path):
        _job(tmp_path, "jobfmt", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobfmt", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m", "is_parse_retry": False},
            {"seq": 2, "round": 1, "role": "builder", "model": "m", "is_parse_retry": True},
            {"seq": 3, "round": 2, "role": "builder", "model": "m", "is_parse_retry": False},
        ])
        _call(tmp_path, "jobfmt", "T001", "builder", 1, None, 100, 10, cost=0.01)
        _call(tmp_path, "jobfmt", "T001", "builder", 2, None, 100, 10, cost=0.01)
        _call(tmp_path, "jobfmt", "T001", "builder", 3, None, 100, 10, cost=0.01)
        _postmortem(tmp_path, "jobfmt", "T001", "builder", round_no=2)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        # seq 1 (the parse retry's earlier call) and seq 3 (the last call, with its own
        # post-mortem) are each marked exactly once; seq 2, the retry itself, never is.
        assert row.format_error_rate == TrustMetric(value=2 / 3, n=3)

    def test_a_later_rounds_parse_retry_is_not_charged_to_an_earlier_rounds_call(self, tmp_path):
        """R-1429 survivor (3): the retry's own round must match the earlier call's round."""
        _job(tmp_path, "jobroundcross", {"T001": {"status": "passed", "repair_rounds_used": 1}})
        _attempts(tmp_path, "jobroundcross", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m", "is_parse_retry": False},
            {"seq": 2, "round": 2, "role": "builder", "model": "m", "is_parse_retry": True},
        ])
        _call(tmp_path, "jobroundcross", "T001", "builder", 1, None, 100, 10, cost=0.01)
        _call(tmp_path, "jobroundcross", "T001", "builder", 2, None, 100, 10, cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        # seq 1 belongs to round 1; round 2's own retry never charges a different round's call.
        # seq 2 is the retry itself and carries no post-mortem, so it is never marked either.
        assert row.format_error_rate == TrustMetric(value=0.0, n=2)

    def test_a_postmortem_of_a_class_other_than_parse_charges_nothing(self, tmp_path):
        """R-1429 survivor (4): only a `parse`-class post-mortem may mark a format error."""
        from packages.orchestration.failure_postmortem import FailureClass

        _job(tmp_path, "jobotherclass", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobotherclass", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m", "is_parse_retry": False},
        ])
        _call(tmp_path, "jobotherclass", "T001", "builder", 1, None, 100, 10, cost=0.01)
        _postmortem(tmp_path, "jobotherclass", "T001", "builder", round_no=1,
                    failure_class=FailureClass.PROVIDER_TIMEOUT)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.format_error_rate == TrustMetric(value=0.0, n=1)


class TestCostBases:
    def _one_pass(self, root: Path, job: str, model: str, *, tokens_in: int | None,
                  tokens_out: int | None, cost: float | None, cost_basis: str | None = None) -> None:
        _job(root, job, {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(root, job, "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": model, "is_parse_retry": False},
        ])
        _call(root, job, "T001", "builder", 1, None, tokens_in, tokens_out, cost=cost,
              cost_basis=cost_basis)

    def test_provider_reported_when_every_call_has_a_cost(self, tmp_path):
        self._one_pass(tmp_path, "jobcost", "m", tokens_in=100, tokens_out=10, cost=0.03)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_basis == COST_BASIS_PROVIDER_REPORTED
        assert row.cost_per_pass == TrustMetric(value=0.03, n=1)

    def test_tokens_when_every_call_has_tokens_but_not_every_cost(self, tmp_path):
        self._one_pass(tmp_path, "jobtokens", "m", tokens_in=100, tokens_out=10, cost=None)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_basis == TRUST_COST_BASIS_TOKENS
        assert row.cost_per_pass == TrustMetric(value=110.0, n=1)

    def test_unknown_with_no_value_when_neither_is_complete(self, tmp_path):
        self._one_pass(tmp_path, "jobunknown", "m", tokens_in=None, tokens_out=None, cost=None)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_basis == COST_BASIS_UNKNOWN
        assert row.cost_per_pass == TrustMetric(value=None, n=1)

    def test_a_metric_with_n_zero_has_no_value(self, tmp_path):
        _task_run(tmp_path, "jobnopass", "T001", status="failed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)],
                  reviewer_model="r", reviewer_cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_per_pass == TrustMetric(value=None, n=0)

    def test_price_table_calls_are_labelled_price_table(self, tmp_path):
        """DECISION F133 D3 (2): the ledger's own `price_table` basis is read, not ignored."""
        self._one_pass(tmp_path, "jobpricetable", "m", tokens_in=100, tokens_out=10, cost=0.04,
                       cost_basis=TRUST_COST_BASIS_PRICE_TABLE)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_basis == TRUST_COST_BASIS_PRICE_TABLE
        assert row.cost_per_pass == TrustMetric(value=0.04, n=1)

    def test_mixed_bases_among_priced_calls_are_labelled_mixed(self, tmp_path):
        """DECISION F133 D3 (2): priced calls that do not share one basis are `mixed`."""
        _job(tmp_path, "jobmixed", {"T001": {"status": "passed", "repair_rounds_used": 0}})
        _attempts(tmp_path, "jobmixed", "T001", [
            {"seq": 1, "round": 1, "role": "builder", "model": "m", "is_parse_retry": False},
            {"seq": 2, "round": 1, "role": "builder", "model": "m", "is_parse_retry": False},
        ])
        _call(tmp_path, "jobmixed", "T001", "builder", 1, None, 100, 10, cost=0.01,
              cost_basis=COST_BASIS_PROVIDER_REPORTED)
        _call(tmp_path, "jobmixed", "T001", "builder", 2, None, 100, 10, cost=0.02,
              cost_basis=TRUST_COST_BASIS_PRICE_TABLE)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        assert row.cost_basis == TRUST_COST_BASIS_MIXED
        assert row.cost_per_pass == TrustMetric(value=0.03, n=1)

    def test_a_call_with_a_figure_but_basis_unknown_is_treated_as_unpriced(self, tmp_path):
        """R-1430: a call carrying a cost figure but basis `unknown` is never counted as priced."""
        self._one_pass(tmp_path, "jobfigureunknown", "m", tokens_in=100, tokens_out=10, cost=0.05,
                       cost_basis=COST_BASIS_UNKNOWN)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        row = table.lookup("m", "builder")
        # Not priced, but every call's tokens are known, so the basis falls to `tokens`.
        assert row.cost_basis == TRUST_COST_BASIS_TOKENS
        assert row.cost_per_pass == TrustMetric(value=110.0, n=1)


class TestThin:
    def test_thin_at_floor_minus_one_and_not_at_the_floor(self, tmp_path):
        for k in range(4):
            _task_run(tmp_path, f"jobthinner{k}", "T001", status="passed", repair_rounds=0,
                      builder_model="m-thin", builder_calls=[(False, 0.01)],
                      reviewer_model="r", reviewer_cost=0.01)
        for k in range(5):
            _task_run(tmp_path, f"jobfat{k}", "T001", status="passed", repair_rounds=0,
                      builder_model="m-fat", builder_calls=[(False, 0.01)],
                      reviewer_model="r", reviewer_cost=0.01)
        table = build_model_trust_table(PROJECT, now=NOW, sample_floor=5, root=tmp_path)
        assert table.lookup("m-thin", "builder").thin is True
        assert table.lookup("m-fat", "builder").thin is False


class TestTrustLeader:
    """DECISION F133 D3 (1): the clear leader among a role's eligible rows."""

    def _row(self, model: str, *, pass_quota: float | None, thin: bool = False, n: int = 25) -> ModelTrustRow:
        return ModelTrustRow(
            role="builder", model=model, pass_quota=TrustMetric(value=pass_quota, n=n),
            repair_need=TrustMetric(value=0.0, n=n), format_error_rate=TrustMetric(value=0.0, n=n),
            cost_per_pass=TrustMetric(value=0.01, n=n), cost_basis=COST_BASIS_PROVIDER_REPORTED,
            settled_tasks=n, thin=thin)

    def _table(self, rows: tuple[ModelTrustRow, ...]) -> ModelTrustTable:
        return ModelTrustTable(
            project_id=PROJECT, updated_at=NOW.isoformat(), window_days=90, sample_floor=20,
            window_start=(NOW - timedelta(days=90)).isoformat(), ledger_present=True, rows=rows,
            unattributed_calls=0, unsettled_tasks=0)

    def test_the_leader_at_exactly_the_margin(self):
        table = self._table((self._row("a", pass_quota=0.80), self._row("b", pass_quota=0.70)))
        rec = trust_leader(table, "builder")
        assert rec.reason == TRUST_RECOMMENDATION_LEADER
        assert rec.leader == "a" and rec.runner_up == "b"
        assert rec.leader_pass_quota == 0.80 and rec.runner_up_pass_quota == 0.70

    def test_just_below_the_margin_is_no_leader(self):
        table = self._table((self._row("a", pass_quota=0.799), self._row("b", pass_quota=0.70)))
        rec = trust_leader(table, "builder")
        assert rec.reason == TRUST_RECOMMENDATION_NO_MARGIN
        assert rec.leader is None and rec.runner_up is None

    def test_a_thin_row_is_never_a_leader(self):
        table = self._table((self._row("a", pass_quota=0.95, thin=True), self._row("b", pass_quota=0.70)))
        rec = trust_leader(table, "builder")
        assert rec.reason == TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE
        assert rec.leader is None

    def test_fewer_than_two_eligible_rows(self):
        table = self._table((self._row("a", pass_quota=0.95),))
        rec = trust_leader(table, "builder")
        assert rec.reason == TRUST_RECOMMENDATION_TOO_FEW_ELIGIBLE
        assert rec.leader is None and rec.runner_up is None

    def test_a_tie_is_no_leader(self):
        table = self._table((self._row("a", pass_quota=0.80), self._row("b", pass_quota=0.80)))
        rec = trust_leader(table, "builder")
        assert rec.reason == TRUST_RECOMMENDATION_NO_MARGIN
        assert rec.leader is None


class TestBuildModelTrustTable:
    def test_a_missing_ledger_is_an_empty_table_and_creates_nothing(self, tmp_path):
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert not table.ledger_present and table.rows == ()
        assert not token_ledger_path_for(PROJECT, tmp_path).parent.exists()

    def test_the_measurement_is_read_only_on_the_ledger(self, tmp_path):
        _build_golden_history(tmp_path)
        folder = token_ledger_path_for(PROJECT, tmp_path).parent

        def state() -> dict[str, str]:
            return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())}

        before = state()
        build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert state() == before

    def test_to_json_round_trips_through_model_trust_table_from_json(self, tmp_path):
        _build_golden_history(tmp_path)
        table = build_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert model_trust_table_from_json(table.to_json()) == table


class TestSnapshot:
    def test_a_fresh_snapshot_is_reused_and_a_stale_one_is_measured_again(self, tmp_path):
        _task_run(tmp_path, "jobsnap1", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        first = load_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        path = model_trust_snapshot_path(PROJECT, tmp_path)
        assert path.name == MODEL_TRUST_SNAPSHOT_FILENAME
        assert path.parent == token_ledger_path_for(PROJECT, tmp_path).parent
        assert model_trust_table_from_json(json.loads(path.read_text(encoding="utf-8"))) == first
        _task_run(tmp_path, "jobsnap2", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        fresh = load_model_trust_table(PROJECT, now=NOW + timedelta(minutes=59), root=tmp_path)
        assert fresh == first and fresh.lookup("m", "builder").settled_tasks == 1
        stale = load_model_trust_table(PROJECT, now=NOW + timedelta(minutes=61), root=tmp_path)
        assert stale.lookup("m", "builder").settled_tasks == 2
        assert stale.updated_at == (NOW + timedelta(minutes=61)).isoformat()

    def test_the_age_limit_is_the_configured_one(self, tmp_path):
        _task_run(tmp_path, "jobage", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        load_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        _task_run(tmp_path, "jobage2", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        later = NOW + timedelta(seconds=120)
        assert load_model_trust_table(PROJECT, now=later, max_age_seconds=60, root=tmp_path).lookup(
            "m", "builder").settled_tasks == 2

    def test_a_snapshot_built_with_another_window_or_floor_is_not_used(self, tmp_path):
        _task_run(tmp_path, "jobwf", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        load_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert load_model_trust_table(PROJECT, now=NOW, sample_floor=2, root=tmp_path).sample_floor == 2
        assert load_model_trust_table(PROJECT, now=NOW, window_days=30, root=tmp_path).window_days == 30

    def test_an_unreadable_or_future_snapshot_is_measured_again(self, tmp_path):
        _task_run(tmp_path, "jobbad", "T001", status="passed", repair_rounds=0,
                  builder_model="m", builder_calls=[(False, 0.01)], reviewer_model="r",
                  reviewer_cost=0.01)
        path = model_trust_snapshot_path(PROJECT, tmp_path)
        path.write_text("{not json", encoding="utf-8")
        assert load_model_trust_table(PROJECT, now=NOW, root=tmp_path).ledger_present
        assert json.loads(path.read_text(encoding="utf-8"))["updated_at"] == NOW.isoformat()
        future = load_model_trust_table(PROJECT, now=NOW - timedelta(minutes=5), root=tmp_path)
        assert future.updated_at == (NOW - timedelta(minutes=5)).isoformat()

    def test_no_ledger_writes_no_snapshot(self, tmp_path):
        token_ledger_path_for(PROJECT, tmp_path).parent.mkdir(parents=True)
        table = load_model_trust_table(PROJECT, now=NOW, root=tmp_path)
        assert not table.ledger_present
        assert not model_trust_snapshot_path(PROJECT, tmp_path).exists()


class TestResolveTrustSettings:
    def test_the_defaults_equal_the_modules_own_constants(self):
        assert resolve_trust_settings() == {"window_days": 90, "sample_floor": 20, "max_age_seconds": 3600}

    def test_a_malformed_value_raises_the_typed_error(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_MODEL_ROUTING_TRUST_SAMPLE_FLOOR", "-1")
        with pytest.raises(TrustConfigError):
            resolve_trust_settings()


def test_cost_basis_constants_match_the_ledgers_own_vocabulary():
    from packages.orchestration.token_ledger import COST_BASIS_PRICE_TABLE as LEDGER_PRICE_TABLE
    from packages.orchestration.token_ledger import COST_BASIS_PROVIDER_REPORTED as LEDGER_REPORTED
    from packages.orchestration.token_ledger import COST_BASIS_UNKNOWN as LEDGER_UNKNOWN

    assert COST_BASIS_PROVIDER_REPORTED == LEDGER_REPORTED
    assert COST_BASIS_UNKNOWN == LEDGER_UNKNOWN
    assert TRUST_COST_BASIS_PRICE_TABLE == LEDGER_PRICE_TABLE
