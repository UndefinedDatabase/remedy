"""F103 T003 — `remedy stats cost`, `backfill-ledger` and `verify-ledger`.

The corpus is a real evidence tree and a real SQLite ledger, both under
``tmp_path``, with ``REMEDY_DATA_DIR`` pointed at a temporary data root and an
explicit project registered inside it. NOTHING here touches the repository's
real data root, and every ledger path is asserted to live under ``tmp_path``.

What is asserted:

  * the three commands are in the catalog, have handlers, and dispatch through
    those handlers with an argparse-shaped namespace;
  * the `--json` document's shape, including the basis key every figure needs;
  * `--by role|model|day` groups, and `--since`/`--job` filter;
  * BASIS LABELING: an unmeasured bucket prints the word ``unmeasured`` and a
    bare ``0`` never stands in for a figure nobody reported — in the table, in
    the JSON (where it is ``null``) and in the summary sentence;
  * `verify-ledger` exits 0 on a clean reconcile and NON-ZERO on injected drift,
    which is what makes it usable as a check;
  * `backfill-ledger` is idempotent: a second invocation adds no row.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, GROUPS, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import stats_ledger_cmd as CMD
from packages.orchestration.token_ledger import (
    LEDGER_FILENAME,
    open_ledger,
    token_ledger_path_for,
)

LEDGER_COMMANDS = ("stats.cost", "stats.backfill-ledger", "stats.verify-ledger")

JOB_ID = "job-ledger-cli"
TASK_MEASURED = "T001"      # the provider reported tokens and a cost
TASK_UNMEASURED = "T002"    # the provider reported nothing at all


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

    project = RemyProject(name="F103 Ledger CLI", slug="f103-ledger-cli")
    save_project(project)
    return str(project.id)


@pytest.fixture
def ledger_path(data_root, project_id, tmp_path) -> Path:
    path = token_ledger_path_for(project_id)
    assert tmp_path in path.parents, "the test would have written the real data root"
    return path


def _write_json_file(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


@pytest.fixture
def evidence_dir(tmp_path) -> Path:
    """Two finalized task runs: one measured on 2026-08-01, one not on 2026-08-02."""
    base = tmp_path / "evidence" / JOB_ID
    _write_json_file(base / "manifest.json",
                     {"bundle_type": "job_evidence", "job_id": JOB_ID})
    runs = base / "task_runs"

    _write_json_file(runs / TASK_MEASURED / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": TASK_MEASURED,
        "execution_mode": "provider_backed",
        "provider_call_count": 2,
        "actual_call_count": 2,
        "cost_call_count": 2,
        "actual_prompt_tokens": 1000,
        "actual_completion_tokens": 200,
        "actual_total_tokens": 1200,
        "actual_cache_read_tokens": 64,
        "actual_cache_creation_tokens": 32,
        "total_cost_usd": 0.25,
        "actual_model_verified": True,
        "builder_actual_model": "claude-opus-5",
        "ts_utc": "2026-08-01T09:00:00+00:00",
    })
    _write_json_file(runs / TASK_MEASURED / "token_accounting.json", {"role": "builder"})

    # The claude-cli case: a real call the provider reported no usage for.
    _write_json_file(runs / TASK_UNMEASURED / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": TASK_UNMEASURED,
        "execution_mode": "provider_backed",
        "provider_call_count": 1,
        "actual_call_count": 0,
        "cost_call_count": 0,
        "actual_missing_reasons": ["provider reports no ledger usage"],
        "model": "claude-cli",
        "ts_utc": "2026-08-02T09:00:00+00:00",
    })
    _write_json_file(runs / TASK_UNMEASURED / "token_accounting.json",
                     {"role": "reviewer"})
    return base


@pytest.fixture
def filled_ledger(evidence_dir, project_id, ledger_path, capsys) -> Path:
    """The ledger after one backfill — the state every query test starts from."""
    CMD._cmd_stats_backfill_ledger(evidence_dir=str(evidence_dir), project=project_id)
    capsys.readouterr()
    return ledger_path


def _row_count(path: Path) -> int:
    conn = open_ledger(path)
    try:
        return conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0]
    finally:
        conn.close()


def _table_row(text: str, first_cell: str) -> list[str]:
    """The rendered table line starting with ``first_cell``, split into cells."""
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] == first_cell:
            return parts
    raise AssertionError(f"no table row for {first_cell!r} in:\n{text}")


class TestRegistration:
    def test_the_three_commands_are_in_the_stats_group(self):
        assert "stats" in GROUPS
        ids = {c.command_id for c in CATALOG if c.group_id == "stats"}
        assert set(LEDGER_COMMANDS) <= ids
        # The group was NOT replaced: F010's command is still in it.
        assert "stats.failures" in ids

    def test_every_command_has_a_handler(self):
        handlers = collect_all_handlers()
        for command_id in LEDGER_COMMANDS:
            assert command_id in handlers
            assert command_id in CMD.COMMAND_HANDLERS

    def test_the_action_classes_tell_the_truth_about_writing(self):
        assert get_command("stats.cost").action_class == "read_only"
        assert get_command("stats.verify-ledger").action_class == "read_only"
        # Backfill WRITES the ledger, so it may not claim to be read-only.
        assert get_command("stats.backfill-ledger").action_class == "write_metadata"

    def test_the_declared_arguments(self):
        cost = get_command("stats.cost")
        assert {a.name for a in cost.args} >= {
            "--since", "--job", "--by", "--project", "--all-projects", "--json"}
        assert cost.supports_json is True
        for command_id in ("stats.backfill-ledger", "stats.verify-ledger"):
            entry = get_command(command_id)
            assert {a.name for a in entry.args} >= {"evidence_dir", "--json"}

    def test_the_exit_code_contract_is_in_the_description(self):
        description = get_command("stats.verify-ledger").description.lower()
        assert "exits 0" in description and "non-zero" in description

    def test_the_handlers_dispatch_from_a_namespace(self, filled_ledger, project_id,
                                                   evidence_dir, capsys):
        CMD.COMMAND_HANDLERS["stats.cost"](argparse.Namespace(
            since=None, job=None, by="role", project=project_id,
            all_projects=False, json=True))
        assert json.loads(capsys.readouterr().out)["filters"]["by"] == "role"

        CMD.COMMAND_HANDLERS["stats.verify-ledger"](argparse.Namespace(
            evidence_dir=str(evidence_dir), project=project_id,
            all_projects=False, json=True))
        assert json.loads(capsys.readouterr().out)["has_drift"] is False

        CMD.COMMAND_HANDLERS["stats.backfill-ledger"](argparse.Namespace(
            evidence_dir=str(evidence_dir), project=project_id,
            all_projects=False, json=True))
        assert json.loads(capsys.readouterr().out)["scanned"] == 2


class TestCostJsonShape:
    def test_the_document_carries_its_figures_basis_and_provenance(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cost(project=project_id, by="role", json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert set(payload) >= {
            "version", "scope", "ledgers_read", "filters", "basis", "total", "rows"}
        assert payload["filters"] == {"since": "", "job": "", "by": "role"}
        assert payload["ledgers_read"] == [str(filled_ledger)]
        assert payload["basis"]["measured_calls"] == 1
        assert payload["basis"]["unmeasured_calls"] == 1
        assert payload["basis"]["fully_measured"] is False

        for row in [payload["total"], *payload["rows"]]:
            assert set(row) >= {
                "bucket", "calls", "tokens_in", "tokens_out", "cache_read",
                "cache_write", "cost_usd", "measured_calls", "unmeasured_calls",
                "basis"}

    def test_the_json_output_is_stable(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, json_output=True)
        first = json.loads(capsys.readouterr().out)
        CMD._cmd_stats_cost(project=project_id, json_output=True)
        assert json.loads(capsys.readouterr().out) == first

    def test_the_grand_total_matches_the_evidence(self, filled_ledger, project_id,
                                                  capsys):
        CMD._cmd_stats_cost(project=project_id, json_output=True)
        total = json.loads(capsys.readouterr().out)["total"]
        assert total["calls"] == 2
        assert total["tokens_in"] == 1000
        assert total["tokens_out"] == 200
        assert total["cost_usd"] == pytest.approx(0.25)
        assert total["basis"] == "mixed"


class TestCostGrouping:
    def test_by_role(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, by="role", json_output=True)
        rows = json.loads(capsys.readouterr().out)["rows"]
        assert [row["bucket"] for row in rows] == ["builder", "reviewer"]

    def test_by_model(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, by="model", json_output=True)
        rows = json.loads(capsys.readouterr().out)["rows"]
        assert [row["bucket"] for row in rows] == ["claude-cli", "claude-opus-5"]

    def test_by_day(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, by="day", json_output=True)
        rows = json.loads(capsys.readouterr().out)["rows"]
        assert [row["bucket"] for row in rows] == ["2026-08-01", "2026-08-02"]

    def test_the_since_filter(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, since="2026-08-02", json_output=True)
        assert json.loads(capsys.readouterr().out)["total"]["calls"] == 1

    def test_the_job_filter(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id, job=JOB_ID, json_output=True)
        assert json.loads(capsys.readouterr().out)["total"]["calls"] == 2
        CMD._cmd_stats_cost(project=project_id, job="job-that-never-ran",
                            json_output=True)
        assert json.loads(capsys.readouterr().out)["total"]["calls"] == 0

    def test_an_unknown_grouping_is_a_usage_error(self, filled_ledger, project_id,
                                                  capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_cost(project=project_id, by="provider")
        assert exc.value.code == CMD.EXIT_USAGE
        assert "not a grouping" in capsys.readouterr().err

    def test_an_invalid_since_is_a_usage_error(self, filled_ledger, project_id,
                                               capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_cost(project=project_id, since="last tuesday")
        assert exc.value.code == CMD.EXIT_USAGE


class TestBasisLabeling:
    """Every figure names its basis, and no unmeasured figure renders as 0."""

    def test_the_human_table_prints_the_unmeasured_word_not_a_zero(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cost(project=project_id, by="role")
        out = capsys.readouterr().out

        reviewer = _table_row(out, "reviewer")
        # bucket, calls, then the five figures, then the basis column.
        assert reviewer[1] == "1"
        assert reviewer[2:7] == [CMD.UNMEASURED] * 5, reviewer
        assert "0" not in reviewer[2:7], "a bare 0 stood in for an unmeasured figure"
        assert reviewer[7] == "unknown"

        builder = _table_row(out, "builder")
        assert builder[2:7] == ["1000", "200", "64", "32", "0.2500"]
        assert builder[7] == "provider_reported"

    def test_the_human_output_names_the_basis_counts_in_words(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cost(project=project_id)
        out = capsys.readouterr().out
        assert "1 of 2 call(s) reported usage (provider_reported)" in out
        assert "1 reported none (unknown)" in out

    def test_a_partly_unmeasured_total_says_so_in_words(self, filled_ledger,
                                                        project_id, capsys):
        CMD._cmd_stats_cost(project=project_id)
        out = capsys.readouterr().out
        assert "PARTLY UNMEASURED" in out
        assert "NOT a complete total" in out

    def test_a_fully_unmeasured_scope_says_so_too(self, filled_ledger, project_id,
                                                  capsys):
        CMD._cmd_stats_cost(project=project_id, since="2026-08-02")
        out = capsys.readouterr().out
        assert "FULLY UNMEASURED" in out
        assert CMD.UNMEASURED in out

    def test_no_price_is_ever_claimed(self, filled_ledger, project_id, capsys):
        CMD._cmd_stats_cost(project=project_id)
        assert "No price is computed" in capsys.readouterr().out

    def test_the_json_unmeasured_figure_is_null_and_not_zero(
        self, filled_ledger, project_id, capsys
    ):
        CMD._cmd_stats_cost(project=project_id, by="role", json_output=True)
        payload = json.loads(capsys.readouterr().out)
        reviewer = next(r for r in payload["rows"] if r["bucket"] == "reviewer")

        for figure in ("tokens_in", "tokens_out", "cache_read", "cache_write",
                       "cost_usd"):
            assert reviewer[figure] is None, figure
            assert reviewer[figure] != 0, figure
        assert reviewer["basis"] == "unknown"
        assert reviewer["unmeasured_calls"] == reviewer["calls"] == 1

    def test_an_empty_scope_is_honest_rather_than_a_zero_report(self, data_root,
                                                               project_id, capsys):
        CMD._cmd_stats_cost(project=project_id)
        out = capsys.readouterr().out
        assert "No ledger on disk for this scope" in out
        assert not token_ledger_path_for(project_id).exists(), "a query created a ledger"


class TestBackfillLedger:
    def test_it_records_the_evidence_into_the_project_ledger(
        self, evidence_dir, project_id, ledger_path, capsys
    ):
        CMD._cmd_stats_backfill_ledger(evidence_dir=str(evidence_dir),
                                       project=project_id)
        out = capsys.readouterr().out

        assert ledger_path.is_file()
        assert _row_count(ledger_path) == 2
        assert "scanned:  2" in out and "recorded: 2" in out

    def test_it_is_idempotent_across_two_invocations(self, evidence_dir, project_id,
                                                     ledger_path, capsys):
        CMD._cmd_stats_backfill_ledger(evidence_dir=str(evidence_dir),
                                       project=project_id, json_output=True)
        first = json.loads(capsys.readouterr().out)
        rows_after_first = _row_count(ledger_path)

        CMD._cmd_stats_backfill_ledger(evidence_dir=str(evidence_dir),
                                       project=project_id, json_output=True)
        second = json.loads(capsys.readouterr().out)

        assert second["scanned"] == first["scanned"] == 2
        assert second["recorded"] == first["recorded"] == 2
        assert second["failed"] == 0
        assert _row_count(ledger_path) == rows_after_first == 2

    def test_a_missing_evidence_directory_is_a_usage_error(self, tmp_path,
                                                           project_id, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_backfill_ledger(evidence_dir=str(tmp_path / "nope"),
                                           project=project_id)
        assert exc.value.code == CMD.EXIT_USAGE
        assert "evidence directory not found" in capsys.readouterr().err

    def test_all_projects_is_refused_because_backfill_writes(self, evidence_dir,
                                                             project_id, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_backfill_ledger(evidence_dir=str(evidence_dir),
                                           all_projects=True)
        assert exc.value.code == CMD.EXIT_USAGE
        assert "read-only aggregation" in capsys.readouterr().err
        assert not token_ledger_path_for(project_id).exists()


class TestVerifyLedger:
    def test_a_clean_reconcile_exits_zero(self, filled_ledger, evidence_dir,
                                          project_id, capsys):
        CMD._cmd_stats_verify_ledger(evidence_dir=str(evidence_dir),
                                     project=project_id)          # no SystemExit
        out = capsys.readouterr().out
        assert "Clean: the ledger agrees with the evidence files." in out

    def test_injected_drift_exits_non_zero(self, filled_ledger, evidence_dir,
                                           project_id, capsys):
        conn = sqlite3.connect(str(filled_ledger))
        try:
            conn.execute("DELETE FROM calls WHERE task_id = ?", (TASK_UNMEASURED,))
            conn.commit()
        finally:
            conn.close()

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_verify_ledger(evidence_dir=str(evidence_dir),
                                         project=project_id)

        assert exc.value.code == CMD.EXIT_DRIFT
        assert exc.value.code != 0
        out = capsys.readouterr().out
        assert f"missing: {JOB_ID}:{TASK_UNMEASURED}" in out
        assert "DRIFT" in out

    def test_drift_is_visible_in_json_too(self, filled_ledger, evidence_dir,
                                          project_id, capsys):
        conn = sqlite3.connect(str(filled_ledger))
        try:
            conn.execute("DELETE FROM calls WHERE task_id = ?", (TASK_MEASURED,))
            conn.commit()
        finally:
            conn.close()

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_verify_ledger(evidence_dir=str(evidence_dir),
                                         project=project_id, json_output=True)

        assert exc.value.code == CMD.EXIT_DRIFT
        payload = json.loads(capsys.readouterr().out)
        assert payload["missing_rows"] == [f"{JOB_ID}:{TASK_MEASURED}"]
        assert payload["has_drift"] is True

    def test_it_writes_nothing(self, filled_ledger, evidence_dir, project_id):
        before = filled_ledger.read_bytes()
        rows = _row_count(filled_ledger)

        CMD._cmd_stats_verify_ledger(evidence_dir=str(evidence_dir),
                                     project=project_id)

        assert _row_count(filled_ledger) == rows
        assert filled_ledger.read_bytes() == before


class TestNothingTouchesTheRealDataRoot:
    def test_every_ledger_this_suite_uses_lives_under_tmp_path(
        self, filled_ledger, tmp_path, data_root
    ):
        assert tmp_path in filled_ledger.parents
        assert filled_ledger.name == LEDGER_FILENAME
        assert tmp_path in data_root.parents or data_root.parent == tmp_path

    def test_reading_leaves_no_sidecar_files_behind(self, filled_ledger, project_id,
                                                    capsys):
        before = sorted(p.name for p in filled_ledger.parent.iterdir())

        CMD._cmd_stats_cost(project=project_id, by="day")
        capsys.readouterr()

        assert sorted(p.name for p in filled_ledger.parent.iterdir()) == before
