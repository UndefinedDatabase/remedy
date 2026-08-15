"""Tests for the append-only bench history and its regression rules (F082 T002).

The goldens under ``fixtures/bench_history/`` are written in exactly the line
shape ``BenchHistoryEntry.to_json()`` produces. Three of them — ``flat``,
``improving`` and ``degrading`` — are three runs over the same two order ids;
``varied`` is four runs over one order id and is the only one whose trailing
values are not all equal, which is what lets a test see the trailing MEDIAN and
the threshold multiplier at all (R-0415). None carries a timestamp, so they are
comparable byte for byte and these tests do not depend on when they run.

Expected numbers are READ OFF the goldens inside each test rather than restated
as literals here: a literal copied out of a fixture stops testing the fixture
the moment either drifts.
"""
from __future__ import annotations

import statistics
from pathlib import Path

from packages.orchestration.bench_history import (
    REGRESSION_COST,
    REGRESSION_PASS_DROP,
    REGRESSION_WALL,
    append_bench_run,
    bench_history_path_for,
    bench_regressions,
    load_bench_history,
)
from packages.orchestration.capability_bench import BenchRecord

GOLDEN_DIR = Path(__file__).resolve().parent / "fixtures" / "bench_history"

SERIES = "f082-bench"


def a_record(order_id: str, *, passed: bool = True, cin: int = 1000,
             cout: int = 200, wall: float = 40.0) -> BenchRecord:
    """One bench row of the shape `capability_bench.build_bench_record` returns."""
    return BenchRecord(
        order_id=order_id,
        series=SERIES,
        passed=passed,
        cost={"in": cin, "out": cout},
        wall_s=wall,
        repair_rounds=None,
        postmortem_classes=(),
    )


def latest_rows(entries: tuple) -> list[BenchRecord]:
    """The rows of the highest ``run_seq`` in ``entries``, in file order."""
    top = max(entry.run_seq for entry in entries)
    return [entry.record for entry in entries if entry.run_seq == top]


def test_a_rerun_appends_and_never_rewrites_the_bytes_already_there(
        tmp_path: Path) -> None:
    """Append-only proven as BYTES, not as a line count: run 1 survives verbatim."""
    path = tmp_path / "nested" / "bench_history.jsonl"

    first_seq = append_bench_run([a_record("ord-a"), a_record("ord-b")], path=path)
    after_first = path.read_bytes()
    second_seq = append_bench_run([a_record("ord-a"), a_record("ord-b")], path=path)
    after_second = path.read_bytes()

    assert (first_seq, second_seq) == (1, 2)
    assert after_second.startswith(after_first)
    assert len(after_second) > len(after_first)


def test_an_empty_run_writes_nothing_and_spends_no_sequence_number(
        tmp_path: Path) -> None:
    path = tmp_path / "bench_history.jsonl"

    assert append_bench_run([], path=path) == 0
    assert not path.exists()


def test_history_path_sits_under_the_data_roots_project_area(tmp_path: Path) -> None:
    assert bench_history_path_for("some-id", root=tmp_path) == (
        tmp_path / "projects" / "some-id" / "bench_history.jsonl"
    )


def test_reading_never_raises_on_a_corrupt_line_or_a_missing_file(
        tmp_path: Path) -> None:
    """One bad line costs one row, not the whole history."""
    good = GOLDEN_DIR / "flat.jsonl"
    lines = good.read_text(encoding="utf-8").splitlines()
    damaged = tmp_path / "bench_history.jsonl"
    damaged.write_text("\n".join([lines[0], "{not json", *lines[2:]]) + "\n",
                       encoding="utf-8")

    entries = load_bench_history(damaged)

    assert len(entries) == len(lines) - 1
    assert load_bench_history(tmp_path / "nothing-here.jsonl") == ()


def test_a_flat_history_warns_about_nothing() -> None:
    entries = load_bench_history(GOLDEN_DIR / "flat.jsonl")

    assert len({entry.run_seq for entry in entries}) == 3
    assert bench_regressions(entries, series=SERIES) == ()


def test_an_improving_history_warns_about_nothing() -> None:
    entries = load_bench_history(GOLDEN_DIR / "improving.jsonl")

    assert bench_regressions(entries, series=SERIES) == ()


def test_a_single_run_has_nothing_to_regress_against() -> None:
    entries = load_bench_history(GOLDEN_DIR / "degrading.jsonl")
    first_run = tuple(entry for entry in entries if entry.run_seq == 1)

    assert first_run
    assert bench_regressions(first_run, series=SERIES) == ()


def test_a_degrading_history_warns_about_the_one_degraded_order_with_numbers() -> None:
    entries = load_bench_history(GOLDEN_DIR / "degrading.jsonl")
    rows = latest_rows(entries)
    degraded = next(row for row in rows if row.passed is False)
    unchanged = [row.order_id for row in rows if row.order_id != degraded.order_id]

    found = bench_regressions(entries, series=SERIES)

    assert found
    assert {warning.order_id for warning in found} == {degraded.order_id}
    for other in unchanged:
        assert other not in {warning.order_id for warning in found}
    assert {warning.kind for warning in found} == {
        REGRESSION_PASS_DROP, REGRESSION_COST, REGRESSION_WALL,
    }

    assert degraded.cost is not None
    expected_cost = float(sum(degraded.cost.values()))
    cost_warning = next(w for w in found if w.kind == REGRESSION_COST)
    assert cost_warning.latest == expected_cost
    assert degraded.order_id in cost_warning.describe()
    assert str(expected_cost) in cost_warning.describe()

    wall_warning = next(w for w in found if w.kind == REGRESSION_WALL)
    assert wall_warning.latest == degraded.wall_s
    assert str(degraded.wall_s) in wall_warning.describe()


def test_the_trailing_median_ignores_one_catastrophic_run() -> None:
    """The baseline is the MEDIAN of the trailing runs and not their mean (R-0415).

    ``varied.jsonl`` carries the one catastrophic run the ``_median`` docstring
    exists for, so its trailing values are NOT all equal and the two statistics
    disagree. Asserting the computed ``baseline`` says which of them the rule
    used; a warn/no-warn boundary alone would only test the fixture.
    """
    entries = load_bench_history(GOLDEN_DIR / "varied.jsonl")
    top = max(entry.run_seq for entry in entries)
    trailing = [entry.record for entry in entries if entry.run_seq < top]
    trailing_costs = [float(sum(row.cost.values())) for row in trailing if row.cost is not None]
    trailing_walls = [float(row.wall_s) for row in trailing if row.wall_s is not None]

    assert len(trailing_costs) == len(trailing_walls) == len(trailing) > 0
    # The fixture must stay discriminating: an edit that flattens it fails HERE
    # rather than quietly going blind again.
    assert statistics.median(trailing_costs) != statistics.mean(trailing_costs)
    assert statistics.median(trailing_walls) != statistics.mean(trailing_walls)

    found = bench_regressions(entries, series=SERIES)

    cost_warning = next(w for w in found if w.kind == REGRESSION_COST)
    assert cost_warning.baseline == statistics.median(trailing_costs)
    assert cost_warning.baseline != statistics.mean(trailing_costs)

    wall_warning = next(w for w in found if w.kind == REGRESSION_WALL)
    assert wall_warning.baseline == statistics.median(trailing_walls)
    assert wall_warning.baseline != statistics.mean(trailing_walls)


def test_a_larger_multiplier_silences_the_same_history() -> None:
    """The threshold multiplier is load-bearing: same entries, larger x, no warning."""
    entries = load_bench_history(GOLDEN_DIR / "varied.jsonl")

    assert bench_regressions(entries, series=SERIES)
    assert bench_regressions(entries, series=SERIES, multiplier=3.0) == ()
