"""
Focused tests for the ``remedy do job-flow`` command.

Coverage:
  - The command is registered in the command catalog (do.job-flow)
  - Argument parsing wires --job-file, --repo, --timeout-sec, --json and the
    optional provider flags through the grouped argparse tree
  - The handler is wired into do_cmd.COMMAND_HANDLERS and the aggregate table
  - The handler validates required/illegal arguments without touching the repo
"""

from __future__ import annotations

import pytest

from apps.cli.command_catalog import CATALOG, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands.do_cmd import COMMAND_HANDLERS
from apps.cli.grouped import build_parser

COMMAND_ID = "do.job-flow"


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------


class TestJobFlowCatalogEntry:
    def test_command_is_registered(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.command_id == COMMAND_ID
        assert cmd.group_id == "do"
        assert cmd.subcommand == "job-flow"

    def test_command_appears_in_catalog_tuple(self) -> None:
        ids = {c.command_id for c in CATALOG}
        assert COMMAND_ID in ids

    def test_command_supports_json(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.supports_json is True
        arg_names = {a.name for a in cmd.args}
        assert "--json" in arg_names

    def test_job_file_is_required_option(self) -> None:
        cmd = get_command(COMMAND_ID)
        job_file = next(a for a in cmd.args if a.name == "--job-file")
        assert job_file.is_option is True
        assert job_file.required is True

    def test_expected_options_present(self) -> None:
        cmd = get_command(COMMAND_ID)
        arg_names = {a.name for a in cmd.args}
        for expected in (
            "--job-file",
            "--repo",
            "--builder",
            "--reviewer",
            "--max-rounds",
            "--repair-rounds",
            "--test-command",
            "--claude-cli-write-mode",
            "--timeout-sec",
            "--out",
            "--json",
        ):
            assert expected in arg_names, f"missing option {expected}"

    def test_does_not_mutate_repo(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.may_mutate_repo is False


# ---------------------------------------------------------------------------
# Argument parsing (grouped argparse tree)
# ---------------------------------------------------------------------------


class TestJobFlowArgumentParsing:
    def _parse(self, argv: list[str]):
        return build_parser().parse_args(argv)

    def test_minimal_parse(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns._command_id == COMMAND_ID
        assert ns.job_file == "job.md"

    def test_repo_default_is_dot(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.repo == "."

    def test_timeout_sec_default(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.timeout_sec == "120"

    def test_json_flag(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md", "--json"])
        assert ns.json is True

    def test_json_defaults_false(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.json is False

    def test_full_parse(self) -> None:
        ns = self._parse([
            "do", "job-flow",
            "--job-file", "x.md",
            "--repo", "/repo",
            "--timeout-sec", "30",
            "--builder", "fake",
            "--reviewer", "fake",
            "--max-rounds", "5",
            "--repair-rounds", "2",
            "--test-command", "pytest -q",
            "--claude-cli-write-mode", "none",
            "--out", "bundle",
            "--json",
        ])
        assert ns._command_id == COMMAND_ID
        assert ns.job_file == "x.md"
        assert ns.repo == "/repo"
        assert ns.timeout_sec == "30"
        assert ns.builder == "fake"
        assert ns.reviewer == "fake"
        assert ns.max_rounds == "5"
        assert ns.repair_rounds == 2
        assert ns.test_command == "pytest -q"
        assert ns.claude_cli_write_mode == "none"
        assert ns.out == "bundle"
        assert ns.json is True


# ---------------------------------------------------------------------------
# Handler wiring
# ---------------------------------------------------------------------------


class TestJobFlowHandlerWiring:
    def test_handler_in_module_table(self) -> None:
        assert COMMAND_ID in COMMAND_HANDLERS
        assert callable(COMMAND_HANDLERS[COMMAND_ID])

    def test_handler_in_aggregate_table(self) -> None:
        table = collect_all_handlers()
        assert COMMAND_ID in table
        assert callable(table[COMMAND_ID])

    def test_every_catalog_arg_name_is_parseable(self) -> None:
        """The catalog options for the command must all be accepted by the parser."""
        cmd = get_command(COMMAND_ID)
        # Build an argv that supplies a value for every option.
        argv = ["do", "job-flow"]
        for a in cmd.args:
            if not a.is_option:
                continue
            if a.name == "--json":
                argv.append("--json")
            elif a.name == "--repair-rounds":
                argv.extend([a.name, "2"])
            else:
                argv.extend([a.name, "v"])
        ns = build_parser().parse_args(argv)
        assert ns._command_id == COMMAND_ID


# ---------------------------------------------------------------------------
# Handler argument validation (no repo mutation, fast-exit paths)
# ---------------------------------------------------------------------------


class TestJobFlowHandlerValidation:
    def _ns(self, **overrides):
        ns = build_parser().parse_args(["do", "job-flow", "--job-file", "job.md"])
        for k, v in overrides.items():
            setattr(ns, k, v)
        return ns

    def test_missing_job_file_exits_2(self) -> None:
        ns = self._ns(job_file="")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_builder_exits_2(self) -> None:
        ns = self._ns(builder="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_reviewer_exits_2(self) -> None:
        ns = self._ns(reviewer="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_write_mode_exits_2(self) -> None:
        ns = self._ns(claude_cli_write_mode="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2
