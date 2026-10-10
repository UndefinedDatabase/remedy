"""`remedy stats calls` — tokens by kind per provider call and per landed change (F302 T004).

The corpus is run records and one job apply record written under a temporary data root that
`REMEDY_DATA_DIR` names; the command reaches them as a user does, through its handler.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import stats_calls_cmd as CMD


def _write_run(root: Path, run_id: str, job_id: str, attempts: list[dict]) -> None:
    folder = root / "runs" / run_id
    folder.mkdir(parents=True)
    (folder / "result.json").write_text(json.dumps({
        "run_id": run_id, "job_id": job_id, "finished_at": "2026-10-10T03:00:00+00:00",
        "provider_evidence": {"provider_attempts": attempts}}))


def _usage(i, o, cc, cr):
    return {"input_tokens": i, "output_tokens": o, "cache_creation_input_tokens": cc,
            "cache_read_input_tokens": cr}


@pytest.fixture()
def root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    _write_run(tmp_path, "r1", "landed-job", [
        {"role": "builder", "provider": "claude-cli", "usage": _usage(20, 8000, 40000, 600000)},
        {"role": "reviewer", "provider": "claude-cli", "usage": _usage(6, 2000, 30000, 60000)}])
    _write_run(tmp_path, "r2", "open-job", [
        {"role": "builder", "provider": "claude-cli", "usage": None}])
    records = tmp_path / "job_apply_records" / "landed-job"
    records.mkdir(parents=True)
    (records / "a1.json").write_text(json.dumps({"status": "applied"}))
    return tmp_path


def _run(capsys, **kw) -> str:
    args = argparse.Namespace(since=kw.get("since", ""), job=kw.get("job", ""), json=kw.get("json", False))
    collect_all_handlers()["stats.calls"](args)
    return capsys.readouterr().out


class TestTheCommandIsReadOnly:
    def test_it_is_in_the_catalog_and_reads_only(self):
        entry = get_command("stats.calls")
        assert (entry.group_id, entry.subcommand, entry.action_class) == ("stats", "calls", "read_only")
        assert entry.supports_json and not entry.may_mutate_repo and not entry.may_execute_commands

    def test_it_adds_exactly_one_handler(self):
        assert set(CMD.COMMAND_HANDLERS) == {"stats.calls"}

    def test_reading_writes_nothing(self, root, capsys):
        before = sorted(str(p) for p in root.rglob("*"))
        _run(capsys)
        _run(capsys, json=True)
        assert sorted(str(p) for p in root.rglob("*")) == before


class TestTheAnswer:
    def test_json_names_every_kind_per_call_by_role_and_per_landed_change(self, root, capsys):
        answer = json.loads(_run(capsys, json=True))
        assert answer["ok"] is True and answer["schema_version"] == 1 and answer["version"] == 1
        assert answer["source"] == "run records"
        builder = next(g for g in answer["groups"] if g["role"] == "builder")
        assert (builder["calls"], builder["measured_calls"]) == (2, 1)
        assert builder["per_call"] == {"input": 20, "output": 8000, "cache_creation": 40000,
                                       "cache_read": 600000}
        assert answer["landed_changes"] == 1 and answer["landed_jobs"] == ["landed-job"]
        assert answer["per_landed_change"] == {"input": 26, "output": 10000, "cache_creation": 70000,
                                               "cache_read": 660000}
        assert answer["per_landed_change_total"] == 740026

    def test_the_text_prints_a_row_per_role_and_the_landed_change(self, root, capsys):
        text = _run(capsys)
        assert "builder" in text and "reviewer" in text
        assert "Per landed change: 740,026 tokens over 1 landed job — input 26" in text

    def test_an_unmeasured_figure_prints_the_word_and_is_null(self, root, capsys):
        text = _run(capsys, job="open-job")
        all_row = next(line for line in text.splitlines() if line.startswith("all"))
        assert all_row.split() == ["all", "1", "0", *["unmeasured"] * 5]
        answer = json.loads(_run(capsys, job="open-job", json=True))
        assert answer["all"]["per_call"] is None and answer["per_landed_change"] is None
        assert answer["filters"] == {"since": "", "job": "open-job"}

    def test_an_empty_data_root_answers_ok_with_no_call(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "empty"))
        answer = json.loads(_run(capsys, json=True))
        assert answer["ok"] is True and answer["all"]["calls"] == 0 and answer["groups"] == []

    def test_since_keeps_only_the_runs_that_finished_at_or_after_it(self, root, capsys):
        assert json.loads(_run(capsys, since="2026-10-10T03:00:00Z", json=True))["all"]["calls"] == 3
        later = json.loads(_run(capsys, since="2026-10-11", json=True))
        assert later["all"]["calls"] == 0 and later["filters"]["since"] == "2026-10-11"

    def test_a_since_that_is_not_a_timestamp_exits_2(self, root, capsys):
        with pytest.raises(SystemExit) as stop:
            _run(capsys, since="yesterday", json=True)
        assert stop.value.code == 2
        assert json.loads(capsys.readouterr().out)["error"] == "invalid_argument"
