"""F022 T001a — the budget tick every safe-point evaluation emits.

`should_stop` evaluates the budget at every safe point. DECISION F022 D1 rules
that each evaluation also emits ONE `budget.tick` run-log event carrying the
absolute figures the MetricsBar renders, and that the emission sits ABOVE the
exhaustion test so the evaluation that stops a job still reports its spend.
DECISION F022 D2 rules HOW it is written: through `RunLogWriter` rather than
`timeline.append_run_event`, under a stable run id so one job keeps one file, with
the event name as an inline literal, and failing soft.

These tests hold the emission to the promises a renderer depends on: absent limits
are absent KEYS rather than fabricated denominators, an estimated figure says so in
its basis, the cadence is one tick per call into one file, the ping-pong job-id
shape emits at all, and no tick can break the run it reports on.

Nothing here touches a developer's data dir: the run log is redirected with
`REMEDY_DATA_DIR` and the stop-control area is a `tmp_path` of the test's own.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import JobBudgets
from packages.orchestration.budget_guard import BudgetCounters, evaluate_budget
from packages.orchestration.run_log import RunLogWriter
from packages.orchestration.safe_points import (
    BUDGET_TICK_RUN_ID,
    _budget_tick_payload,
    should_stop,
)

TICK_EVENT = "budget.tick"


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    """The run log's root, redirected away from the developer's real data dir."""
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def control(tmp_path) -> Path:
    """A stop-control root of our own, so no test reads a real control area."""
    return tmp_path / "control"


def _counters(
    *,
    tokens: int = 1200,
    measured_calls: int = 3,
    unmeasured_calls: int = 0,
    cost: float | None = None,
    priced_calls: int = 0,
    unpriced_calls: int = 0,
) -> BudgetCounters:
    """Counters that satisfy `BudgetCounters`' own validation.

    `provider_calls` must equal measured + unmeasured, a positive token total needs
    a measured call, and a measured call needs a source out of
    `VALID_ACTUAL_SOURCES`.
    """
    return BudgetCounters(
        provider_calls=measured_calls + unmeasured_calls,
        measured_token_total=tokens,
        measured_call_count=measured_calls,
        unmeasured_call_count=unmeasured_calls,
        actual_sources=("token_actuals",) if measured_calls else (),
        measured_cost_usd=cost,
        priced_call_count=priced_calls,
        unpriced_call_count=unpriced_calls,
    )


def _tick_files(root: Path, job_id: str) -> list[Path]:
    """Every run-log file this job has, whatever it holds."""
    job_dir = root / "runs" / job_id
    return sorted(job_dir.glob("*.jsonl")) if job_dir.is_dir() else []


def _ticks(root: Path, job_id: str) -> list[dict]:
    """The job's `budget.tick` events, in file order."""
    events: list[dict] = []
    for path in _tick_files(root, job_id):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                event = json.loads(line)
                if event.get("event") == TICK_EVENT:
                    events.append(event)
    return events


class TestTickPayload:
    def test_priced_job_with_both_limits_emits_one_full_tick(self, data_root, control):
        """T1 — one tick per call, carrying every figure a renderer needs."""
        job_id = str(uuid4())
        result = should_stop(
            job_id,
            budgets=JobBudgets(max_total_tokens=10_000, max_cost_usd=5.0),
            counters=_counters(cost=0.42, priced_calls=3),
            control_root_path=control,
        )
        assert result.should_stop is False

        emitted = _ticks(data_root, job_id)
        assert len(emitted) == 1, f"expected exactly one tick, got {len(emitted)}"
        payload = emitted[0]["metadata"]
        assert payload["spent_tokens"] == 1200
        assert payload["spent_usd"] == 0.42
        assert payload["limit_tokens"] == 10_000
        assert payload["limit_usd"] == 5.0
        assert payload["unmeasured_calls"] == 0
        assert payload["basis"] == {"tokens": "actual", "cost": "actual"}

    def test_a_limitless_money_side_leaves_the_keys_out(self, data_root, control):
        """T2 — an absent limit is an absent KEY, never a null and never a zero."""
        job_id = str(uuid4())
        should_stop(
            job_id,
            budgets=JobBudgets(max_total_tokens=10_000),
            counters=_counters(cost=None),
            control_root_path=control,
        )

        emitted = _ticks(data_root, job_id)
        assert len(emitted) == 1
        payload = emitted[0]["metadata"]
        assert "limit_usd" not in payload, "a limitless job must not carry a denominator"
        assert "spent_usd" not in payload, "an unpriced run must not carry a money figure"
        assert payload["basis"]["cost"] == "absent"
        assert payload["limit_tokens"] == 10_000

    def test_no_budgets_and_no_counters_emit_nothing(self, data_root, control):
        """T3 — no evaluation, no figure. Not a zeroed tick: no tick."""
        without_budgets = str(uuid4())
        should_stop(
            without_budgets,
            budgets=None,
            counters=_counters(),
            control_root_path=control,
        )
        assert _tick_files(data_root, without_budgets) == []

        without_counters = str(uuid4())
        should_stop(
            without_counters,
            budgets=JobBudgets(max_total_tokens=10_000),
            counters=None,
            control_root_path=control,
        )
        assert _tick_files(data_root, without_counters) == []

    def test_unmeasured_calls_make_the_token_basis_a_lower_bound(self, data_root, control):
        """T4 — an estimated token figure says so, and says how many calls are dark."""
        job_id = str(uuid4())
        should_stop(
            job_id,
            budgets=JobBudgets(max_total_tokens=10_000),
            counters=_counters(tokens=500, measured_calls=1, unmeasured_calls=2),
            control_root_path=control,
        )

        payload = _ticks(data_root, job_id)[0]["metadata"]
        assert payload["basis"]["tokens"] == "lower_bound"
        assert payload["unmeasured_calls"] == 2
        assert payload["spent_tokens"] == 500

    def test_an_unpriced_call_makes_the_cost_basis_a_lower_bound(self, data_root, control):
        """T5 — money measured with a call unpriced is a floor, not a total."""
        job_id = str(uuid4())
        should_stop(
            job_id,
            budgets=JobBudgets(max_total_tokens=10_000, max_cost_usd=5.0),
            counters=_counters(cost=0.42, priced_calls=2, unpriced_calls=1),
            control_root_path=control,
        )

        payload = _ticks(data_root, job_id)[0]["metadata"]
        assert payload["basis"]["cost"] == "lower_bound"
        assert payload["spent_usd"] == 0.42


class TestTickCadenceAndShape:
    def test_a_pingpong_shaped_job_id_still_emits(self, data_root, control):
        """T6 — the regression test for DECISION F022 D2 clause one.

        A JobPlan's `job_id` is `uuid4().hex[:16]`, which `UUID()` rejects. Routing
        this emission through `timeline.append_run_event` would raise `ValueError`
        before the write, the soft failure would swallow it, and the ticker would be
        silently dead on the one job shape that runs long enough to need it.
        """
        job_id = uuid4().hex[:16]
        with pytest.raises(ValueError):
            UUID(job_id)

        should_stop(
            job_id,
            budgets=JobBudgets(max_total_tokens=10_000),
            counters=_counters(),
            control_root_path=control,
        )

        emitted = _ticks(data_root, job_id)
        assert len(emitted) == 1, (
            "a ping-pong shaped job id emitted no tick: the emission is not going "
            "through RunLogWriter"
        )
        assert emitted[0]["job_id"] == job_id

    def test_an_exhausted_budget_still_ticks_and_still_stops(self, data_root, control):
        """T7 — DECISION F022 D1's 'above the exhaustion test' ruling, pinned.

        'Still' is a comparison, so both arms are measured here: the evaluation that
        does NOT exhaust ticks, the one that DOES ticks as well, and the decision the
        second one returns is untouched by the notification beside it.
        """
        job_id = str(uuid4())
        budgets = JobBudgets(max_total_tokens=1_000)

        under = should_stop(
            job_id,
            budgets=budgets,
            counters=_counters(tokens=400, measured_calls=1),
            control_root_path=control,
        )
        assert under.should_stop is False

        over = should_stop(
            job_id,
            budgets=budgets,
            counters=_counters(tokens=1_400, measured_calls=2),
            control_root_path=control,
        )
        assert over.should_stop is True
        assert over.reason == "budget_exhausted:max_total_tokens"
        assert over.source == "budget"

        emitted = _ticks(data_root, job_id)
        assert len(emitted) == 2, (
            "the evaluation below the limit and the one above it must BOTH tick; "
            f"got {len(emitted)}"
        )
        assert [e["metadata"]["spent_tokens"] for e in emitted] == [400, 1_400]

    def test_three_calls_write_three_ticks_into_one_file(self, data_root, control):
        """T8 — one job keeps ONE run-log file, however long it runs."""
        job_id = str(uuid4())
        for _ in range(3):
            should_stop(
                job_id,
                budgets=JobBudgets(max_total_tokens=10_000),
                counters=_counters(),
                control_root_path=control,
            )

        files = _tick_files(data_root, job_id)
        assert len(files) == 1, f"expected one run-log file, got {[p.name for p in files]}"
        assert files[0].name == f"{BUDGET_TICK_RUN_ID}.jsonl"
        assert len(_ticks(data_root, job_id)) == 3

    def test_a_failing_write_never_changes_the_decision(self, data_root, control, monkeypatch):
        """T9 — the tick fails soft: a broken notification is not a broken run."""
        job_id = str(uuid4())
        budgets = JobBudgets(max_total_tokens=10_000)

        healthy = should_stop(
            job_id,
            budgets=budgets,
            counters=_counters(),
            control_root_path=control,
        )
        assert healthy.should_stop is False
        assert len(_ticks(data_root, job_id)) == 1, (
            "the control arm wrote nothing, so the arm below proves nothing"
        )

        def _refuse(*args, **kwargs):
            raise OSError("disk is full")

        monkeypatch.setattr(
            "packages.orchestration.run_log.RunLogWriter", _refuse
        )
        despite = should_stop(
            job_id,
            budgets=budgets,
            counters=_counters(),
            control_root_path=control,
        )
        assert despite.should_stop is False
        assert despite == healthy, "the failed write changed the safe-point decision"
        assert len(_ticks(data_root, job_id)) == 1, "the failed write must add nothing"


class TestPayloadKeysNeverCollide:
    def test_no_payload_key_is_a_named_parameter_of_the_writer(self, data_root, control):
        """T10 — a colliding key would be hijacked out of `metadata`.

        The parameter names are read out of `RunLogWriter.log`'s own signature so
        this test tracks the signature rather than a transcription of it.
        """
        named = {
            name
            for name, parameter in inspect.signature(RunLogWriter.log).parameters.items()
            if name != "self" and parameter.kind is not inspect.Parameter.VAR_KEYWORD
        }
        assert "outcome" in named and "message" in named, (
            "the signature reader found no named parameter, so the disjointness "
            "assertion below is about the empty set"
        )

        job_id = str(uuid4())
        budgets = JobBudgets(max_total_tokens=10_000, max_cost_usd=5.0)
        counters = _counters(cost=0.42, priced_calls=3)
        should_stop(job_id, budgets=budgets, counters=counters, control_root_path=control)

        emitted = _ticks(data_root, job_id)
        assert len(emitted) == 1
        landed = set(emitted[0]["metadata"])
        built = set(_budget_tick_payload(evaluate_budget(budgets, counters)))
        assert landed == built, (
            "every payload key must arrive in metadata; a key missing here was "
            f"hijacked into the envelope: {sorted(built - landed)}"
        )
        assert not (landed & named), (
            f"payload keys collide with the writer: {sorted(landed & named)}"
        )
