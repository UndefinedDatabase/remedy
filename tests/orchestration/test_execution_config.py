"""`packages/orchestration/execution_config.py` — R-1235's third step.

`_resolve_claude_cli_launch_config` reads `claude_cli.customizations` and `claude_cli.all_tools`
fresh from a configuration, with their source, for the four `ExecutionConfig` fields a job's
record now carries: `claude_cli_customizations`, `claude_cli_customizations_source`,
`claude_cli_all_tools` and `claude_cli_all_tools_source`. These tests build every configuration
with `load_config` on paths that do not exist and `monkeypatch.setenv` — never the operator's own
`remedy.toml` or `~/.config/remedy/remedy.toml`.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path

from packages.orchestration import execution_config as ecm
from packages.orchestration import run_manifest as rm
from packages.orchestration.config import load_config
from packages.orchestration.job_input_definition import build_job_input_definition

_NOWHERE = Path("/nonexistent-f306-t008/remedy-test")


def _config(monkeypatch, **env):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return load_config(project_path=_NOWHERE / "p.toml", user_path=_NOWHERE / "u.toml")


class TestTheResolverReadsFreshEachTime:
    def test_a_key_set_by_its_env_var_is_true_with_source_env(self, monkeypatch):
        cfg = _config(monkeypatch, REMEDY_CLAUDE_CLI_ALL_TOOLS="true")
        rec = ecm._resolve_claude_cli_launch_config(cfg)
        assert (rec["claude_cli_all_tools"], rec["claude_cli_all_tools_source"]) == (True, "env")

    def test_an_unset_key_is_false_with_source_default(self, monkeypatch):
        cfg = _config(monkeypatch)
        rec = ecm._resolve_claude_cli_launch_config(cfg)
        assert (rec["claude_cli_customizations"], rec["claude_cli_customizations_source"]) == (
            False, "default")

    def test_the_resolver_ignores_a_persisted_value(self, monkeypatch):
        persisted = dataclasses.replace(
            ecm.ExecutionConfig(), claude_cli_customizations=True,
            claude_cli_customizations_source="env")
        cfg = _config(monkeypatch)
        rec = ecm.resolve_job_execution_config(persisted, config=cfg)
        assert (rec.claude_cli_customizations, rec.claude_cli_customizations_source) == (
            False, "default")


class TestExportAndImport:
    def test_a_true_value_and_its_source_survive_the_round_trip(self):
        on = dataclasses.replace(
            ecm.ExecutionConfig(), claude_cli_all_tools=True, claude_cli_all_tools_source="env")
        assert ecm._import_execution_config(ecm._export_execution_config(on)) == on

    def test_an_export_without_the_four_keys_reads_back_the_defaults(self):
        exported = ecm._export_execution_config(ecm.ExecutionConfig())
        before_f306 = {k: v for k, v in exported.items()
                      if k not in ("claude_cli_customizations", "claude_cli_customizations_source",
                                   "claude_cli_all_tools", "claude_cli_all_tools_source")}
        back = ecm._import_execution_config(before_f306)
        assert (back.claude_cli_customizations, back.claude_cli_customizations_source,
               back.claude_cli_all_tools, back.claude_cli_all_tools_source) == (
            False, "default", False, "default")


class _Job:
    job_title = "t"
    job_file_sha256 = "f" * 64
    isolation_mode = "worktree"
    tasks: list = []

    def __init__(self, execution_config):
        self.execution_config = execution_config


class TestValidationOfTheFourKeys:
    def _definition(self):
        return build_job_input_definition(_Job(ecm.ExecutionConfig()))

    def test_a_definition_with_the_four_keys_validates(self):
        assert rm.validate_job_input_definition(self._definition()) == []

    def test_a_definition_written_before_the_four_keys_still_validates(self):
        d = self._definition()
        before_f306 = dict(d, execution={k: v for k, v in d["execution"].items()
                                         if k not in rm.JOB_INPUT_EXECUTION_OPTIONAL_FIELDS})
        assert rm.validate_job_input_definition(before_f306) == []

    def test_a_non_boolean_value_is_refused(self):
        d = self._definition()
        bad = dict(d, execution=dict(d["execution"], claude_cli_all_tools="true"))
        assert rm.validate_job_input_definition(bad) != []

    def test_an_unknown_source_is_refused(self):
        d = self._definition()
        bad = dict(d, execution=dict(d["execution"], claude_cli_customizations_source="guess"))
        assert rm.validate_job_input_definition(bad) != []
