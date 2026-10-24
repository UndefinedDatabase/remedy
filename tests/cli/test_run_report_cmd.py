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


_MINIMAL_RUN_RECORD = {
    "goal": "demo", "repo_path": "/x", "mode": "pingpong",
    "builder_provider": "claude-cli", "reviewer_provider": "fake",
    "max_rounds": 1, "total_rounds": 0, "resumed_from_run_id": None,
    "resume_declined": {}, "final_status": "completed", "staged_files": [],
    "changed_target_files": [], "ignored_target_noise_files": [],
    "target_noise_detected": False, "target_mutated": False, "tests_not_run": False,
    "context_categories": [], "reviewer_parse_retry_count": 0, "rounds": [],
}


def _write_minimal_run_record(run_id: str, *, job_id: str = "") -> pathlib.Path:
    """DECISION F157 D5 (2)/(3): a run's own directory, minimal enough for `_cmd_run_show`'s
    not-found check and `_print_text_report`'s defensive `.get`s, so the test is about the
    degradations line and nothing else."""
    from packages.orchestration import data_paths

    directory = data_paths.run_dir(run_id)
    directory.mkdir(parents=True, exist_ok=True)
    record = {"run_id": run_id, "job_id": job_id, **_MINIMAL_RUN_RECORD}
    (directory / "result.json").write_text(json.dumps(record), encoding="utf-8")
    return directory


_DEGRADED_LINE = json.dumps({
    "role": "builder", "provider": "claude-cli", "model": "m",
    "decisions": [
        {"feature_key": "stream_evidence_capture", "mode": "degraded",
         "strategy": "buffered_output", "missing": ["streaming"]},
    ],
})


class TestRunShowCapabilityDegradationsLine:
    """DECISION F157 D5 (3): `remedy run show` prints the line when the run's directory holds a
    degradation and none otherwise, and its JSON answer carries the list both ways."""

    def test_a_degraded_directory_prints_the_line_and_an_absent_one_prints_none(
        self, tmp_path, monkeypatch, capsys,
    ):
        from apps.cli.commands.run_report_cmd import _cmd_run_show
        from packages.orchestration.capability_routes import CAPABILITY_DECISIONS_FILENAME

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        degraded_dir = _write_minimal_run_record("run-degraded")
        (degraded_dir / CAPABILITY_DECISIONS_FILENAME).write_text(_DEGRADED_LINE + "\n", encoding="utf-8")

        _cmd_run_show("run-degraded", json_output=False)
        out = capsys.readouterr().out
        assert "Degradations: stream_evidence_capture as buffered_output" in out

        _write_minimal_run_record("run-native")
        _cmd_run_show("run-native", json_output=False)
        out2 = capsys.readouterr().out
        assert "Degradations:" not in out2

    def test_json_output_carries_the_list_both_ways(self, tmp_path, monkeypatch, capsys):
        from apps.cli.commands.run_report_cmd import _cmd_run_show
        from packages.orchestration.capability_routes import CAPABILITY_DECISIONS_FILENAME

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        degraded_dir = _write_minimal_run_record("run-degraded-json")
        (degraded_dir / CAPABILITY_DECISIONS_FILENAME).write_text(_DEGRADED_LINE + "\n", encoding="utf-8")

        _cmd_run_show("run-degraded-json", json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["capability_degradations"] == [
            {"feature_key": "stream_evidence_capture", "mode": "degraded",
             "strategy": "buffered_output", "missing": ["streaming"]},
        ]

        _write_minimal_run_record("run-native-json")
        _cmd_run_show("run-native-json", json_output=True)
        payload2 = json.loads(capsys.readouterr().out)
        assert payload2["capability_degradations"] == []
