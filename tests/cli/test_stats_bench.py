"""F082 T003a — `remedy stats bench`, the read view over the bench history.

The corpus is a REAL history file under ``tmp_path``, written through the
production writer :func:`packages.orchestration.bench_history.append_bench_run`
with ``REMEDY_DATA_DIR`` pointed at a temporary data root and an explicit project
registered inside it. Nothing here touches the repository's real data root, and
the history path is asserted to live under ``tmp_path`` before a byte is written.

There is deliberately NO test-only flag. The command has no ``--history`` escape
hatch, so these tests reach the file the way a user does — through
``REMEDY_DATA_DIR`` and ``--project`` — and a flag that existed only for this
file would be a finding, not a fixture.

What is asserted:

  * the command is in the catalog, adds EXACTLY ONE handler key, and declares
    itself read-only in every field a caller can inspect;
  * READING WRITES NOTHING: the history bytes are identical after both output
    modes, and a missing history is neither created nor an error;
  * `--series` is optional — omitted it takes the series of the latest run and
    NAMES it, and it names the series it did not read either way;
  * NO ABSENCE PRINTS AS A ZERO: an unmeasured figure prints the shared word in
    the table and stays ``null`` beside that word in the JSON;
  * the warnings are exactly what ``bench_regressions`` produced, rendered
    through ``BenchRegression.describe`` rather than rewritten, and the
    multiplier the flag carries is the one the comparison used;
  * fewer than two runs says WHY nothing was compared instead of reporting
    "no regressions" as if a comparison had happened.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, GROUPS, get_command
from apps.cli.commands import bench_cmd as CMD
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import stats_ledger_cmd as LEDGER
from packages.orchestration.bench_history import (
    append_bench_run,
    bench_history_path_for,
    bench_regressions,
    load_bench_history,
)
from packages.orchestration.capability_bench import BenchRecord

SERIES = "nightly"
OTHER_SERIES = "weekly"

ORDER_STEADY = "bench-01-cold-start"
ORDER_DROPPED = "bench-02-repair-loop"
ORDER_UNMEASURED = "bench-03-unmeasured"

#: The trailing figures. Two runs carry them unchanged, which is what gives the
#: third run a trailing median to be compared against.
BASE_COST = {"in": 1000, "out": 200}
BASE_WALL = 40.0
#: The third run's blow-out on ONE order: past 1.5x of both trailing medians.
BLOWN_COST = {"in": 4000, "out": 800}
BLOWN_WALL = 90.0


def _row(order_id: str, *, series: str = SERIES, passed: bool | None,
         cost: dict[str, int] | None, wall_s: float | None) -> BenchRecord:
    """One stored row. ``repair_rounds`` is None because no run records it."""
    return BenchRecord(order_id=order_id, series=series, passed=passed,
                       cost=cost, wall_s=wall_s, repair_rounds=None,
                       postmortem_classes=())


def _steady_run() -> list[BenchRecord]:
    return [
        _row(ORDER_STEADY, passed=True, cost=dict(BASE_COST), wall_s=BASE_WALL),
        _row(ORDER_DROPPED, passed=True, cost=dict(BASE_COST), wall_s=BASE_WALL),
        _row(ORDER_UNMEASURED, passed=None, cost=None, wall_s=None),
    ]


def _degraded_run() -> list[BenchRecord]:
    """One order blows both budgets, one stops passing, one stays unmeasured."""
    return [
        _row(ORDER_STEADY, passed=True, cost=dict(BLOWN_COST), wall_s=BLOWN_WALL),
        _row(ORDER_DROPPED, passed=False, cost=dict(BASE_COST), wall_s=BASE_WALL),
        _row(ORDER_UNMEASURED, passed=None, cost=None, wall_s=None),
    ]


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    """A temporary data root; the real one is never read or written."""
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def project_id(data_root) -> str:
    from packages.orchestration.project_registry import RemyProject, save_project

    project = RemyProject(name="F082 Bench CLI", slug="f082-bench-cli")
    save_project(project)
    return str(project.id)


@pytest.fixture
def history_path(data_root, project_id, tmp_path) -> Path:
    path = bench_history_path_for(project_id)
    assert tmp_path in path.parents, "the test would have written the real data root"
    return path


@pytest.fixture
def history(history_path) -> Path:
    """Four runs: ONE of ``weekly`` first, then THREE of ``nightly``.

    ``weekly`` is written first on purpose. ``run_seq`` counts runs of the FILE,
    not of a series, so writing it first is what makes the highest sequence
    number belong to ``nightly`` — the series the command must choose when
    ``--series`` is omitted.
    """
    append_bench_run(
        [_row(ORDER_STEADY, series=OTHER_SERIES, passed=True,
              cost=dict(BASE_COST), wall_s=BASE_WALL)],
        path=history_path)
    append_bench_run(_steady_run(), path=history_path)
    append_bench_run(_steady_run(), path=history_path)
    append_bench_run(_degraded_run(), path=history_path)
    return history_path


def _human(capsys, **kwargs) -> str:
    CMD._cmd_stats_bench(**kwargs)
    return capsys.readouterr().out


def _payload(capsys, **kwargs) -> dict:
    CMD._cmd_stats_bench(json_output=True, **kwargs)
    return json.loads(capsys.readouterr().out)


def _table_row(text: str, order_id: str) -> list[str]:
    """The rendered row for ``order_id`` in the LATEST run, split into cells."""
    matches = [line.split() for line in text.splitlines()
               if order_id in line.split()]
    assert matches, f"no table row for {order_id!r} in:\n{text}"
    return matches[-1]


class TestRegistration:
    def test_the_command_is_in_the_stats_group(self):
        assert "stats" in GROUPS
        ids = {c.command_id for c in CATALOG if c.group_id == "stats"}
        assert "stats.bench" in ids
        # The group was NOT replaced: the ledger commands are still in it.
        assert "stats.cost" in ids

    def test_it_adds_exactly_one_handler_key(self):
        assert set(CMD.COMMAND_HANDLERS) == {"stats.bench"}
        assert "stats.bench" in collect_all_handlers()

    def test_the_declared_contract_says_it_only_reads(self):
        entry = get_command("stats.bench")
        assert entry.action_class == "read_only"
        assert entry.may_mutate_repo is False
        assert entry.may_execute_commands is False
        assert entry.supports_json is True

    def test_the_declared_arguments_and_the_absent_one(self):
        names = {a.name for a in get_command("stats.bench").args}
        assert names >= {"--series", "--multiplier", "--project", "--json"}
        # Two projects' benches are two trends; folding them is refused by
        # having no flag that could ask for it.
        assert "--all-projects" not in names

    def test_the_handler_dispatches_from_an_argparse_namespace(
        self, history, project_id, capsys
    ):
        CMD.COMMAND_HANDLERS["stats.bench"](argparse.Namespace(
            series=None, multiplier=None, project=project_id, json=True))
        assert json.loads(capsys.readouterr().out)["series"] == SERIES


class TestReadingWritesNothing:
    def test_neither_output_mode_changes_one_byte_of_the_history(
        self, history, project_id, capsys
    ):
        before = history.read_bytes()
        _human(capsys, project=project_id)
        _payload(capsys, project=project_id)
        assert history.read_bytes() == before

    def test_a_missing_history_is_a_sentence_and_stays_missing(
        self, history_path, project_id, capsys
    ):
        assert not history_path.exists()
        text = _human(capsys, project=project_id)
        assert "nothing has been recorded yet" in text
        # An unrun bench is not an error and not a table of zeros: once the
        # path and the project id are removed, NO digit is left to be mistaken
        # for a figure. Scrubbing both is required rather than tidy — a random
        # project UUID would otherwise decide whether this assertion holds.
        scrubbed = text.replace(str(history_path), "").replace(project_id, "")
        assert not any(char.isdigit() for char in scrubbed)
        assert not history_path.exists()

    def test_a_missing_history_says_so_in_json_too(
        self, history_path, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        assert payload["history_exists"] is False
        assert payload["rows"] == []
        assert payload["series"] is None
        assert "nothing has been recorded yet" in payload["empty_reason"]
        assert not history_path.exists()


class TestSeriesChoice:
    def test_without_the_flag_it_reads_the_series_of_the_latest_run(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        assert payload["series"] == SERIES
        assert payload["series_selected_by"] == "latest_run"
        assert payload["latest_run"] == max(
            e.run_seq for e in load_bench_history(history))

    def test_it_names_the_chosen_series_and_the_one_it_did_not_read(
        self, history, project_id, capsys
    ):
        text = _human(capsys, project=project_id)
        assert SERIES in text
        assert "chosen as the series of the latest run" in text
        assert OTHER_SERIES in text
        assert "Not read" in text

    def test_the_flag_selects_the_other_series(self, history, project_id, capsys):
        payload = _payload(capsys, project=project_id, series=OTHER_SERIES)
        assert payload["series"] == OTHER_SERIES
        assert payload["series_selected_by"] == "flag"
        assert payload["series_not_read"] == [SERIES]

    def test_an_unknown_series_names_what_the_file_actually_holds(
        self, history, project_id, capsys
    ):
        text = _human(capsys, project=project_id, series="no-such-series")
        assert "No row of series no-such-series is recorded" in text
        assert SERIES in text and OTHER_SERIES in text


class TestFiguresNeverBecomeZero:
    def test_the_word_is_the_ledger_view_s_word_and_not_a_second_one(self):
        assert CMD.UNMEASURED == LEDGER.UNMEASURED

    def test_an_unmeasured_row_prints_the_word_in_every_column(
        self, history, project_id, capsys
    ):
        cells = _table_row(_human(capsys, project=project_id), ORDER_UNMEASURED)
        # Run, order, then the three figures — all three absent, none of them 0.
        assert cells[2:] == [CMD.UNMEASURED] * 3

    def test_an_unmeasured_row_stays_null_beside_its_word_in_json(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        row = [r for r in payload["rows"] if r["order_id"] == ORDER_UNMEASURED][-1]
        assert row["cost_tokens"] is None and row["cost_basis"] == CMD.UNMEASURED
        assert row["wall_s"] is None and row["wall_basis"] == CMD.UNMEASURED
        assert row["passed"] is None and row["passed_basis"] == CMD.UNMEASURED
        assert payload["unmeasured_label"] == CMD.UNMEASURED

    def test_a_measured_row_carries_the_totals_read_off_the_corpus(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        latest = payload["latest_run"]
        row = [r for r in payload["rows"]
               if r["order_id"] == ORDER_STEADY and r["run_seq"] == latest][0]
        assert row["cost_tokens"] == sum(BLOWN_COST.values())
        assert row["wall_s"] == BLOWN_WALL
        assert row["cost_basis"] == "measured"

    def test_no_repair_round_column_and_the_limit_is_stated_once(
        self, history, project_id, capsys
    ):
        text = _human(capsys, project=project_id)
        header = next(line for line in text.splitlines() if line.startswith("Run "))
        assert "epair" not in header
        assert "Repair rounds: no run records them yet" in text
        assert "repair_rounds" in _payload(capsys, project=project_id)["notes"]

    def test_no_price_is_computed_anywhere(self, history, project_id, capsys):
        text = _human(capsys, project=project_id)
        assert "usd" not in text.lower() and "$" not in text
        assert "No price is computed" in text


class TestRegressionWarnings:
    def _expected(self, history, multiplier=None):
        kwargs = {} if multiplier is None else {"multiplier": multiplier}
        return bench_regressions(load_bench_history(history), series=SERIES, **kwargs)

    def test_the_warnings_are_exactly_what_bench_regressions_produced(
        self, history, project_id, capsys
    ):
        expected = self._expected(history)
        assert len(expected) == 3, "the corpus must produce all three kinds"
        text = _human(capsys, project=project_id)
        for warning in expected:
            assert warning.describe() in text

    def test_each_warning_names_its_order_and_both_numbers(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        rendered = [w["describe"] for w in payload["regressions"]]
        assert rendered == [w.describe() for w in self._expected(history)]
        for warning in payload["regressions"]:
            assert warning["order_id"] in warning["describe"]
            assert str(warning["latest"]) in warning["describe"]
            assert str(warning["baseline"]) in warning["describe"]

    def test_the_blown_order_is_named_and_the_steady_one_is_not(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id)
        warned = {w["order_id"] for w in payload["regressions"]}
        assert ORDER_STEADY in warned and ORDER_DROPPED in warned
        # Unmeasured never warns: absence is not a regression.
        assert ORDER_UNMEASURED not in warned

    def test_a_larger_multiplier_silences_the_threshold_warnings(
        self, history, project_id, capsys
    ):
        payload = _payload(capsys, project=project_id, multiplier="10")
        assert payload["multiplier"] == 10.0
        kinds = {w["kind"] for w in payload["regressions"]}
        # A pass drop is not a threshold comparison, so it survives the raise.
        assert kinds == {"pass_drop"}
        assert [w["describe"] for w in payload["regressions"]] == [
            w.describe() for w in self._expected(history, multiplier=10.0)]

    def test_an_unusable_multiplier_is_a_usage_error(self, history, project_id):
        for bad in ("not-a-number", "0", "-1"):
            with pytest.raises(SystemExit) as excinfo:
                CMD._cmd_stats_bench(project=project_id, multiplier=bad)
            assert excinfo.value.code == CMD.EXIT_USAGE


class TestTooFewRunsSaysWhy:
    @pytest.fixture
    def one_run(self, history_path) -> Path:
        append_bench_run(_steady_run(), path=history_path)
        return history_path

    def test_one_run_yields_no_warning_and_names_the_reason(
        self, one_run, project_id, capsys
    ):
        assert bench_regressions(load_bench_history(one_run), series=SERIES) == ()
        text = _human(capsys, project=project_id)
        assert "No comparison was made" in text
        # "no regressions" would claim a comparison that never happened.
        assert "No regression:" not in text

    def test_json_says_it_compared_nothing_and_why(self, one_run, project_id, capsys):
        comparison = _payload(capsys, project=project_id)["comparison"]
        assert comparison["compared"] is False
        assert comparison["runs_compared"] == 1
        assert "at least two" in comparison["reason"]
