"""Tests for the bench dry run (F082 T001, last item).

The dry run is the join from a frozen order file to a bench row over evidence
that was already recorded, so these tests point at the SAME recorded fixture
directory ``tests/orchestration/test_gauntlet_evidence.py`` names as
``RECORDED_DIR`` and the evaluator's own dry-run proof runs against. Nothing
here executes an order.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.orchestration.bench_dry_run import (
    EVIDENCE_MISSING_CLASS,
    dry_run_from_order_set,
    dry_run_rows,
)
from packages.orchestration.bench_orders import load_bench_order_set
from packages.orchestration.gauntlet_evaluator import evaluate_evidence_dir
from packages.orchestration.gauntlet_evidence import RUN_FILENAME, run_dirs

RECORDED_DIR = Path(__file__).resolve().parent / "fixtures" / "gauntlet" / "recorded"

SERIES = "f082-dry-run"


def recorded_order_ids() -> tuple[str, ...]:
    """The order ids the recorded runs claim, read off the bodies themselves."""
    ids = []
    for run_dir in run_dirs(RECORDED_DIR):
        body = json.loads((run_dir / RUN_FILENAME).read_text(encoding="utf-8"))
        ids.append(str(body["order_id"]))
    return tuple(ids)


def write_run(directory: Path, body: dict[str, Any] | str) -> None:
    """Write one run directory, either a real body or raw bytes that are not JSON."""
    directory.mkdir(parents=True)
    text = body if isinstance(body, str) else json.dumps(body)
    (directory / RUN_FILENAME).write_text(text, encoding="utf-8")


def a_body(order_id: str, **overrides: Any) -> dict[str, Any]:
    """A recorded run.json body of the shape `gauntlet_runner._evidence_body` writes."""
    body: dict[str, Any] = {
        "gauntlet_run_version": 1,
        "order_id": order_id,
        "kind": "cold_start",
        "terminal_status": "done",
        "wall_seconds": 41.5,
        "postmortems": [],
        "tokens": {"in": 900, "out": 210},
    }
    body.update(overrides)
    return body


def test_every_recorded_run_becomes_a_row_in_the_order_asked_for() -> None:
    ids = recorded_order_ids()
    assert len(ids) == 9

    rows = dry_run_rows(order_ids=ids, evidence_dir=RECORDED_DIR, series=SERIES)

    assert tuple(row.order_id for row in rows) == ids
    assert {row.series for row in rows} == {SERIES}
    # One spot value read off the real recorded bytes rather than recomputed.
    by_id = {row.order_id: row for row in rows}
    injected = by_id["fx-04-provider-api-error-mid-move"]
    assert injected.cost == {"in": 133900, "out": 30400}
    assert injected.wall_s == 803.75


def test_each_row_passed_equals_the_evaluators_own_flawless() -> None:
    """Pass is not re-decided in the bench — prove the wiring, not a table."""
    expected = {run.order_id: run.flawless
                for run in evaluate_evidence_dir(RECORDED_DIR).runs}

    rows = dry_run_rows(order_ids=recorded_order_ids(),
                        evidence_dir=RECORDED_DIR, series=SERIES)

    assert {row.order_id: row.passed for row in rows} == expected
    # The recorded set is deliberately mixed, so this is not a vacuous compare.
    assert True in expected.values() and False in expected.values()


def test_frozen_order_set_against_foreign_evidence_gives_missing_rows() -> None:
    """The real bench set: no recorded run names any of its ids, so every row fails."""
    orders = load_bench_order_set()

    rows = dry_run_from_order_set(evidence_dir=RECORDED_DIR, series=SERIES)

    assert tuple(row.order_id for row in rows) == tuple(o.id for o in orders)
    for row in rows:
        assert row.passed is False
        assert row.cost is None
        assert row.wall_s is None
        assert row.repair_rounds is None
        assert row.postmortem_classes == (EVIDENCE_MISSING_CLASS,)


def test_unreadable_evidence_never_raises_and_takes_the_missing_row(
        tmp_path: Path) -> None:
    write_run(tmp_path / "run-01-good", a_body("ord-good"))
    write_run(tmp_path / "run-02-broken", "{not json at all")

    rows = dry_run_rows(order_ids=("ord-good", "ord-broken"),
                        evidence_dir=tmp_path, series=SERIES)

    good, broken = rows
    assert good.order_id == "ord-good"
    assert good.cost == {"in": 900, "out": 210}
    assert good.wall_s == 41.5
    assert broken.order_id == "ord-broken"
    assert broken.cost is None
    assert broken.postmortem_classes == (EVIDENCE_MISSING_CLASS,)


def test_rows_follow_order_ids_not_the_directory_sort() -> None:
    first, second = recorded_order_ids()[:2]

    rows = dry_run_rows(order_ids=(second, first),
                        evidence_dir=RECORDED_DIR, series=SERIES)

    assert tuple(row.order_id for row in rows) == (second, first)
