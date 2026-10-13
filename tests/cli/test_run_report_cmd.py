"""Tests for apps/cli/commands/run_report_cmd.py — the `run` command handlers, and the one
line `remedy run show` prints for a run in which a call failed over (T002, DECISION F058 D3).
"""

from __future__ import annotations

import json
import pathlib
import shutil


def _configure_builder_chain_toml(monkeypatch, tmp_path, toml_body: str) -> None:
    """Make `model_failover.chains` resolve from *toml_body* — the same idiom
    tests/orchestration/test_model_failover.py's own `_configure_chains_toml` uses.
    """
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text(toml_body, encoding="utf-8")
    loaded = load_config(
        project_path=toml_file,
        user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)


def _run_through_failover(monkeypatch, tmp_path, toml_body: str):
    """A run whose builder is `claude-cli` with no real CLI on PATH, through the chain
    *toml_body* configures — or no chain at all when *toml_body* is empty.
    """
    from packages.orchestration.pingpong_loop import run_pingpong

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(
        "packages.orchestration.pingpong_provider.shutil.which",
        lambda name: None if name == "claude" else shutil.which(name),
    )
    _configure_builder_chain_toml(monkeypatch, tmp_path, toml_body)
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    return run_pingpong(
        "Fix README", str(repo),
        builder_name="claude-cli", builder_model="primary-model", reviewer_name="fake",
    )


_SERVED_CHAIN_TOML = '''
[[remedy.model_failover.chains.builder]]
provider = "fake"
model = "stand-in"
tier = "mid"
'''

_RAN_OUT_CHAIN_TOML = '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "other-model"
tier = "mid"
'''


class TestRunShowFailoverLine:
    def test_a_served_call_prints_the_line_once_after_reviewer(self, tmp_path, monkeypatch, capsys):
        from apps.cli.commands.run_report_cmd import _cmd_run_show
        from packages.orchestration.model_failover import failover_report_line
        from packages.orchestration.pingpong_loop import load_run

        result = _run_through_failover(monkeypatch, tmp_path, _SERVED_CHAIN_TOML)
        data = load_run(result.run_id)
        expected = failover_report_line(data)
        assert expected is not None

        _cmd_run_show(result.run_id, json_output=False)
        lines = capsys.readouterr().out.splitlines()
        reviewer_idx = next(i for i, line in enumerate(lines) if line.startswith("Reviewer:"))
        failover_lines = [i for i, line in enumerate(lines) if line == expected]
        assert failover_lines == [reviewer_idx + 1]

    def test_a_ran_out_call_prints_the_line_once_after_reviewer(self, tmp_path, monkeypatch, capsys):
        from apps.cli.commands.run_report_cmd import _cmd_run_show
        from packages.orchestration.model_failover import failover_report_line
        from packages.orchestration.pingpong_loop import load_run

        result = _run_through_failover(monkeypatch, tmp_path, _RAN_OUT_CHAIN_TOML)
        data = load_run(result.run_id)
        expected = failover_report_line(data)
        assert expected is not None

        _cmd_run_show(result.run_id, json_output=False)
        lines = capsys.readouterr().out.splitlines()
        reviewer_idx = next(i for i, line in enumerate(lines) if line.startswith("Reviewer:"))
        failover_lines = [i for i, line in enumerate(lines) if line == expected]
        assert failover_lines == [reviewer_idx + 1]

    def test_no_chain_prints_no_failover_line(self, tmp_path, monkeypatch, capsys):
        from apps.cli.commands.run_report_cmd import _cmd_run_show

        result = _run_through_failover(monkeypatch, tmp_path, "")

        _cmd_run_show(result.run_id, json_output=False)
        lines = capsys.readouterr().out.splitlines()
        assert [line for line in lines if line.startswith("Failover:")] == []

    def test_json_output_carries_the_rounds_failover_entry_when_served(
        self, tmp_path, monkeypatch, capsys,
    ):
        from apps.cli.commands.run_report_cmd import _cmd_run_show

        result = _run_through_failover(monkeypatch, tmp_path, _SERVED_CHAIN_TOML)

        _cmd_run_show(result.run_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert "failover" in payload["rounds"][0]["builder"]

    def test_json_output_carries_the_rounds_failover_entry_when_ran_out(
        self, tmp_path, monkeypatch, capsys,
    ):
        from apps.cli.commands.run_report_cmd import _cmd_run_show

        result = _run_through_failover(monkeypatch, tmp_path, _RAN_OUT_CHAIN_TOML)

        _cmd_run_show(result.run_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert "failover" in payload["rounds"][0]["builder"]
