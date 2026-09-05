"""
Tests for apps.cli.command_catalog — command catalog integrity.

Coverage:
  - Every public grouped command has one catalog entry
  - Every catalog entry belongs to exactly one group
  - No duplicate grouped command paths
  - No duplicate command ids
  - No sensitive terms in descriptions/examples
  - Mutation/execution classification present for every command
  - JSON-support claims tested for representative commands
  - Group coverage
"""

from __future__ import annotations

import re

import pytest

from apps.cli.command_catalog import (
    CATALOG,
    GROUPS,
    _is_list_command,
    get_command,
    get_commands_for_group,
    get_group,
)

# ---------------------------------------------------------------------------
# Structural integrity
# ---------------------------------------------------------------------------


class TestCatalogIntegrity:
    def test_no_duplicate_command_ids(self) -> None:
        ids = [cmd.command_id for cmd in CATALOG]
        assert len(ids) == len(set(ids)), f"Duplicate command_ids: {[x for x in ids if ids.count(x) > 1]}"

    def test_no_duplicate_grouped_paths(self) -> None:
        paths = [(cmd.group_id, cmd.subcommand) for cmd in CATALOG]
        assert len(paths) == len(set(paths)), f"Duplicate paths: {[x for x in paths if paths.count(x) > 1]}"

    def test_every_command_belongs_to_known_group(self) -> None:
        for cmd in CATALOG:
            assert cmd.group_id in GROUPS, f"{cmd.command_id} has unknown group: {cmd.group_id}"

    def test_every_group_has_at_least_one_command(self) -> None:
        for gid in GROUPS:
            cmds = get_commands_for_group(gid)
            assert len(cmds) >= 1, f"Group {gid} has no commands"

    def test_command_id_format(self) -> None:
        for cmd in CATALOG:
            assert "." in cmd.command_id, f"command_id must be group.subcommand: {cmd.command_id}"
            group, sub = cmd.command_id.split(".", 1)
            assert group == cmd.group_id, f"command_id prefix mismatch: {cmd.command_id}"
            assert sub == cmd.subcommand, f"command_id suffix mismatch: {cmd.command_id}"


class TestCatalogClassification:
    def test_every_command_has_action_class(self) -> None:
        valid = {"read_only", "write_metadata", "approval_gate", "apply_write", "test_execution", "controlled_builder_execution", "dev_helper", "local_state_change"}
        for cmd in CATALOG:
            assert cmd.action_class in valid, f"{cmd.command_id} has invalid action_class: {cmd.action_class}"

    def test_mutating_commands_flagged(self) -> None:
        """Commands that may_mutate_repo or may_execute_commands must not be read_only."""
        for cmd in CATALOG:
            if cmd.may_mutate_repo or cmd.may_execute_commands:
                assert cmd.action_class != "read_only", (
                    f"{cmd.command_id} mutates/executes but is classified as read_only"
                )


class TestCatalogExpensive:
    """F114 T003 - is_expensive is explicit and reviewable, never inferred."""

    def test_is_expensive_is_a_bool_on_every_entry(self) -> None:
        for cmd in CATALOG:
            assert isinstance(cmd.is_expensive, bool), (
                f"{cmd.command_id}.is_expensive must be a bool"
            )

    def test_exactly_job_run_is_marked_expensive_so_far(self) -> None:
        marked = sorted(cmd.command_id for cmd in CATALOG if cmd.is_expensive)
        assert marked == ["job.run"], (
            f"F114 T003 has only marked job.run so far; found {marked}"
        )

    def test_job_run_is_expensive(self) -> None:
        assert get_command("job.run").is_expensive is True

    def test_job_run_has_a_yes_flag_to_skip_the_cost_confirmation(self) -> None:
        args = get_command("job.run").args
        yes_args = [a for a in args if a.name == "--yes"]
        assert len(yes_args) == 1, "job.run must declare exactly one --yes arg"
        assert yes_args[0].is_flag is True, "job.run's --yes must be a flag, not a valued option"


class TestListCommandOptions:
    """F262 T001 - every list-shaped command carries the shared listing flags."""

    def test_every_list_command_carries_all_four_flags(self) -> None:
        list_commands = [c for c in CATALOG if _is_list_command(c)]
        assert list_commands, "no list-shaped commands found in CATALOG"
        for cmd in list_commands:
            missing = {"--sort", "--since", "--until", "--limit"} - {a.name for a in cmd.args}
            assert not missing, f"{cmd.command_id} is missing list flags: {missing}"

    def test_every_list_command_has_exactly_one_desc_flag(self) -> None:
        list_commands = [c for c in CATALOG if _is_list_command(c)]
        for cmd in list_commands:
            desc_args = [a for a in cmd.args if a.name == "--desc"]
            assert len(desc_args) == 1, f"{cmd.command_id} must declare exactly one --desc arg"
            assert desc_args[0].is_flag is True, f"{cmd.command_id}'s --desc must be a flag"

    def test_the_parser_builds_for_every_list_command(self) -> None:
        """Building the whole parser tree once is the cheapest proof that no
        command anywhere in the catalog - list-shaped or not - has two ArgDefs
        sharing a flag name, which is exactly the collision class this
        round's add-only-if-missing design avoids by construction."""
        from apps.cli.grouped import build_parser

        build_parser()


class TestCatalogSensitivity:
    """No sensitive content in catalog descriptions."""

    #: Credential PREFIXES. Short and alphanumeric, so they are matched at a
    #: token boundary: a plain substring scan fires on ordinary prose
    #: ("task-scoped" contains "sk-").
    FORBIDDEN_PREFIXES = ("sk-", "ghp_", "xoxb-")

    #: Terms that are sensitive wherever they appear.
    FORBIDDEN = (
        "password=", "BEGIN PRIVATE KEY",
        "raw_stdout", "raw_stderr", "diff_preview", "approval_reason",
        "api_key=", "secret=",
    )

    def _violations(self, text: str) -> list[str]:
        lower = text.lower()
        found = [bad for bad in self.FORBIDDEN if bad.lower() in lower]
        found += [
            p for p in self.FORBIDDEN_PREFIXES
            if re.search(rf"(?<![0-9a-z]){re.escape(p.lower())}", lower)
        ]
        return found

    def test_no_sensitive_terms_in_descriptions(self) -> None:
        for cmd in CATALOG:
            found = self._violations(cmd.description)
            assert not found, (
                f"{cmd.command_id} description contains forbidden terms: {found}"
            )

    def test_no_sensitive_terms_in_arg_help(self) -> None:
        for cmd in CATALOG:
            for arg in cmd.args:
                found = self._violations(arg.help)
                assert not found, (
                    f"{cmd.command_id} arg '{arg.name}' help contains forbidden: {found}"
                )


class TestCatalogJSONSupport:
    """JSON-support claims match actual command catalog entries."""

    def test_json_commands_have_json_arg(self) -> None:
        for cmd in CATALOG:
            if cmd.supports_json:
                arg_names = [a.name for a in cmd.args]
                assert "--json" in arg_names, (
                    f"{cmd.command_id} claims supports_json but has no --json arg"
                )

    def test_known_json_commands(self) -> None:
        expected_json = {
            "brain.graph", "brain.node", "brain.context",
            "policy.contract", "policy.token",
            "worker.list", "test.discover",
            "project.show", "project.context", "patch.list",
        }
        for cid in expected_json:
            cmd = get_command(cid)
            assert cmd.supports_json, f"{cid} should support JSON"


class TestCatalogLookups:
    def test_get_group(self) -> None:
        g = get_group("job")
        assert g.id == "job"

    def test_get_group_missing(self) -> None:
        with pytest.raises(KeyError):
            get_group("nonexistent")

    def test_get_command(self) -> None:
        cmd = get_command("brain.graph")
        assert cmd.group_id == "brain"

    def test_get_command_missing(self) -> None:
        with pytest.raises(KeyError):
            get_command("brain.nonexistent")

    def test_get_commands_for_group(self) -> None:
        cmds = get_commands_for_group("patch")
        assert len(cmds) == 7
        subs = {c.subcommand for c in cmds}
        assert subs == {
            "list", "show", "approve", "reject", "apply", "revert", "approve-hunks"}


# ---------------------------------------------------------------------------
# Group coverage — required groups from spec
# ---------------------------------------------------------------------------


class TestRequiredGroups:
    REQUIRED = ("job", "project", "patch", "test", "brain", "policy", "worker", "ui", "dev")

    def test_all_required_groups_exist(self) -> None:
        for gid in self.REQUIRED:
            assert gid in GROUPS, f"Missing required group: {gid}"


class TestRequiredCommands:
    """Key commands from the spec must exist."""

    REQUIRED = (
        "job.create", "job.list", "job.show", "job.attach-repo", "job.permit",
        "job.permissions", "job.run-next",
        "project.create", "project.list", "project.show", "project.attach-repo",
        "project.attach-job", "project.context",
        "patch.list", "patch.show", "patch.approve", "patch.reject", "patch.apply",
        "test.discover", "test.run",
        "brain.graph", "brain.node", "brain.view", "brain.context",
        "brain.trust", "brain.timeline",
        "policy.contract", "policy.token",
        "worker.list",
        "ui.start", "ui.latest", "ui.status", "ui.stop", "ui.open",
    )

    def test_all_required_commands_exist(self) -> None:
        catalog_ids = {cmd.command_id for cmd in CATALOG}
        for cid in self.REQUIRED:
            assert cid in catalog_ids, f"Missing required command: {cid}"
