"""F115 T003c — `remedy stats report`, the cost report in a user's hands.

The corpus is the one ``tests/cli/test_stats_cost.py`` already builds: its
``data_root``, ``project_id`` and ``ledger_path`` fixtures are IMPORTED rather
than re-invented, so there is one description of "a temporary data root with a
registered project" in this suite and not two that can drift apart. Only the
evidence tree is new, because this command needs what the cost view never did:
calls in TWO adjacent windows, a second job that exists in only one of them, and
a prompt trace so the segment breakdown has something to break down.

What is asserted, one property per test:

  * the command is in the catalog, has a handler, and dispatches from an
    argparse-shaped namespace — the `--help` the sandbox refuses to run, proven
    the way the suite proves it;
  * markdown carries the cost table, the segment section and the comparison;
  * `--json` parses and carries ``report_version`` and ``comparison``;
  * a closed period compares against the window before it, whose ``until`` is
    the ``--since`` string BYTE FOR BYTE (DECISION F115 D6);
  * an open-ended period says why it cannot compare, and every delta is null —
    never a zero;
  * a bad `--until` names `--until` and not `--since`;
  * `--job` filters the PRIOR query too: a job that did not exist in the
    previous window yields an empty prior that says so.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

import tests.cli.test_stats_cost as LEDGER_CLI
from apps.cli.command_catalog import get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import stats_ledger_cmd as CMD
from tests.cli.test_stats_cost import (  # noqa: F401 - reused pytest fixtures
    data_root,
    ledger_path,
    project_id,
)

#: The job that spans both windows, so the prior period has something in it.
JOB_SPANNING = "job-report-spanning"

#: The job that exists ONLY in the current window. Filtering to it is how the
#: "the prior query carries the same job filter" property becomes observable.
JOB_LATE_ONLY = "job-report-late-only"

#: The period under test and the window that abuts it: `[2026-08-02, 2026-08-03)`
#: is one day long, so its prior is `[2026-08-01T00:00:00, 2026-08-02)`.
SINCE = "2026-08-02"
UNTIL = "2026-08-03"


def _task_run(runs: Path, task_id: str, *, ts: str, role: str, model: str) -> None:
    """One finalized, measured task run plus the prompt trace F115 reads."""
    LEDGER_CLI._write_json_file(runs / task_id / "provider_evidence.json", {
        "schema_version": "1.0.0",
        "task_id": task_id,
        "execution_mode": "provider_backed",
        "provider_call_count": 1,
        "actual_call_count": 1,
        "cost_call_count": 1,
        "actual_prompt_tokens": 900,
        "actual_completion_tokens": 100,
        "actual_total_tokens": 1000,
        "actual_cache_read_tokens": 50,
        "actual_cache_creation_tokens": 25,
        "total_cost_usd": 0.5,
        "actual_model_verified": True,
        "builder_actual_model": model,
        "ts_utc": ts,
    })
    LEDGER_CLI._write_json_file(runs / task_id / "token_accounting.json", {"role": role})
    (runs / task_id / "prompt_trace.jsonl").write_text(
        json.dumps({
            "task_id": task_id,
            "segment_manifest": [
                {"name": "system_rules", "rank": 0, "sha256": "a" * 64,
                 "chars": 400, "tokens_estimated": 100},
                {"name": "task_context", "rank": 1, "sha256": "b" * 64,
                 "chars": 200, "tokens_estimated": 50},
            ],
        }) + "\n",
        encoding="utf-8",
    )


@pytest.fixture
def evidence_dirs(tmp_path) -> tuple[Path, Path]:
    """Two evidence trees: one job over both days, one only on the second."""
    spanning = tmp_path / "evidence" / JOB_SPANNING
    LEDGER_CLI._write_json_file(spanning / "manifest.json",
                                {"bundle_type": "job_evidence", "job_id": JOB_SPANNING})
    _task_run(spanning / "task_runs", "T001",
              ts="2026-08-01T09:00:00+00:00", role="builder", model="claude-opus-5")
    _task_run(spanning / "task_runs", "T002",
              ts="2026-08-02T09:00:00+00:00", role="builder", model="claude-opus-5")

    late = tmp_path / "evidence" / JOB_LATE_ONLY
    LEDGER_CLI._write_json_file(late / "manifest.json",
                                {"bundle_type": "job_evidence", "job_id": JOB_LATE_ONLY})
    _task_run(late / "task_runs", "T003",
              ts="2026-08-02T10:00:00+00:00", role="reviewer", model="claude-cli")
    return spanning, late


@pytest.fixture
def report_ledger(evidence_dirs, project_id, ledger_path, capsys) -> Path:
    """The ledger after both jobs are mirrored — every report test starts here."""
    for base in evidence_dirs:
        CMD._cmd_stats_backfill_ledger(evidence_dir=str(base), project=project_id)
    capsys.readouterr()
    return ledger_path


class TestReportRegistration:
    """The wiring, proven through the catalog and the handler table.

    The `remedy` binary is refused in this session's sandbox, so `remedy stats
    report --help` is never invoked here. These are the same three checks the
    ledger CLI suite already uses in its place.
    """

    def test_the_command_is_in_the_stats_group_as_a_read_only_view(self):
        entry = get_command("stats.report")

        assert entry.group_id == "stats"
        assert entry.subcommand == "report"
        assert entry.action_class == "read_only"
        assert entry.supports_json is True

    def test_it_declares_both_period_bounds_and_no_all_projects_flag(self):
        names = [arg.name for arg in get_command("stats.report").args]

        assert names == ["--since", "--until", "--job", "--by", "--label",
                         "--project", "--json"]
        assert "--all-projects" not in names

    def test_the_description_says_why_there_is_no_all_projects_report(self):
        description = get_command("stats.report").description

        assert "--all-projects" in description
        assert "segment breakdown" in description

    def test_the_handler_resolves_and_dispatches_from_a_namespace(
        self, report_ledger, project_id, capsys
    ):
        assert "stats.report" in CMD.COMMAND_HANDLERS
        assert "stats.report" in collect_all_handlers()

        CMD.COMMAND_HANDLERS["stats.report"](argparse.Namespace(
            since=SINCE, until=UNTIL, job=None, by="role", label="R17",
            project=project_id, json=True))

        assert json.loads(capsys.readouterr().out)["filters"]["by"] == "role"


class TestReportRendering:
    def test_the_markdown_carries_all_three_sections(self, report_ledger,
                                                     project_id, capsys):
        CMD._cmd_stats_report(since=SINCE, until=UNTIL, by="role",
                              label="F115 R17", project=project_id)
        out = capsys.readouterr().out

        assert out.startswith("# Cost report — F115 R17\n")
        assert "## Cost" in out
        assert "## Where the tokens went" in out
        assert "## Compared to the previous period" in out
        assert "| system_rules |" in out

    def test_the_json_parses_and_carries_its_version_and_comparison(
        self, report_ledger, project_id, capsys
    ):
        CMD._cmd_stats_report(since=SINCE, until=UNTIL, project=project_id,
                              json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["report_version"] == 3
        assert "comparison" in payload
        assert payload["filters"] == {
            "since": SINCE, "until": UNTIL, "job": "", "by": None,
            "timezone": "UTC"}


class TestPriorPeriodComparison:
    def test_a_closed_period_compares_against_the_window_that_abuts_it(
        self, report_ledger, project_id, capsys
    ):
        CMD._cmd_stats_report(since=SINCE, until=UNTIL, project=project_id,
                              json_output=True)
        comparison = json.loads(capsys.readouterr().out)["comparison"]

        assert comparison["available"] is True
        # BYTE FOR BYTE, not a re-serialisation: the two windows abut only under
        # the same lexicographic compare `_cost_filters` performs (F115 D6).
        assert comparison["prior"]["until"] == SINCE
        assert comparison["prior"]["since"] == "2026-08-01T00:00:00"
        assert comparison["prior"]["total"]["calls"] == 1
        assert comparison["deltas"]["calls"] == 1

    def test_an_open_ended_period_states_its_reason_and_nulls_every_delta(
        self, report_ledger, project_id, capsys
    ):
        CMD._cmd_stats_report(since=SINCE, project=project_id, json_output=True)
        comparison = json.loads(capsys.readouterr().out)["comparison"]

        assert comparison["available"] is False
        assert "open-ended period has no length to mirror" in comparison["reason"]
        assert comparison["prior"] is None
        assert set(comparison["deltas"]) == {
            "tokens_in", "tokens_out", "cache_read", "cache_write", "cost_usd",
            "calls"}
        for name, value in comparison["deltas"].items():
            assert value is None, name
            assert value != 0, name

    def test_a_job_filter_narrows_the_prior_query_too(self, report_ledger,
                                                      project_id, capsys):
        CMD._cmd_stats_report(since=SINCE, until=UNTIL, job=JOB_LATE_ONLY,
                              project=project_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["total"]["calls"] == 1
        comparison = payload["comparison"]
        # The prior window WAS read; it simply holds no call of this job. Saying
        # "read and holds no call at all" is the P6 distinction a column of
        # zeros would erase.
        assert comparison["available"] is False
        assert "read and holds no call at all" in comparison["reason"]
        assert all(value is None for value in comparison["deltas"].values())


class TestPeriodBoundValidation:
    def test_a_bad_until_names_until_and_not_since(self, report_ledger,
                                                   project_id, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_report(since=SINCE, until="next tuesday",
                                  project=project_id)

        assert exc.value.code == CMD.EXIT_USAGE
        err = capsys.readouterr().err
        assert "--until" in err
        assert "--since" not in err
