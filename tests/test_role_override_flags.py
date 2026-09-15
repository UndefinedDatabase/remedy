"""Per-role override flags: the CLI resolver, its validation, and the `job run` flags.

The `--builder/reviewer/repair-provider|model|effort` flags are resolved and validated in
`apps/cli/commands/do_cmd.py` (`_resolve_cli_role_configs`, `_validate_role_override`) before
any run work begins, and `job run` is the command that carries them.
"""

from __future__ import annotations

import pytest

from apps.cli.command_catalog import get_command
from apps.cli.commands.do_cmd import COMMAND_HANDLERS
from apps.cli.grouped import build_parser
from packages.orchestration.model_aliases import resolve_model_alias

# ---------------------------------------------------------------------------
# T002: CLI/config per-role model override flags
#
# --builder/reviewer/repair-provider|model|effort are validated at the CLI
# layer and passed through to role_config.resolve_role_config. Invalid values
# are rejected with exit code 2; omitting every flag preserves the built-in
# defaults (backward compatible).
# ---------------------------------------------------------------------------


class TestRoleOverrideResolver:
    """Unit tests for the CLI-layer resolver + validation."""

    def test_backward_compat_defaults_when_all_omitted(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        cfgs = _resolve_cli_role_configs()
        for role in ("builder", "reviewer", "repair"):
            assert cfgs[role] == {
                "provider": "ollama",
                "model": resolve_model_alias("ollama-default"),
                "effort": "medium",
            }

    def test_parses_and_resolves_per_role_overrides(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        cfgs = _resolve_cli_role_configs(
            builder_provider="claude",
            builder_model="opus",
            builder_effort="high",
            reviewer_effort="low",
            repair_provider="fake",
        )
        assert cfgs["builder"] == {
            "provider": "claude", "model": "opus", "effort": "high",
        }
        # Partial override keeps defaults for unset fields.
        assert cfgs["reviewer"]["effort"] == "low"
        assert cfgs["reviewer"]["provider"] == "ollama"
        assert cfgs["repair"]["provider"] == "fake"
        assert cfgs["repair"]["effort"] == "medium"

    def test_invalid_provider_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(builder_provider="bogus")
        assert exc.value.code == 2

    def test_invalid_effort_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(reviewer_effort="turbo")
        assert exc.value.code == 2

    def test_empty_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(repair_model="   ")
        assert exc.value.code == 2


class TestRoleOverrideHandlerWiring:
    """The flags reject invalid input through the real command handlers."""

    def _job_run_ns(self, **overrides):
        ns = build_parser().parse_args(["job", "run", "job-id"])
        for k, v in overrides.items():
            setattr(ns, k, v)
        return ns

    def test_job_run_rejects_invalid_role_provider(self) -> None:
        ns = self._job_run_ns(reviewer_provider="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS["job.run"](ns)
        assert exc.value.code == 2


# ---------------------------------------------------------------------------
# T003: CLI per-role flag registration (argparse layer)
#
# Verifies that --builder/reviewer/repair-provider|model|effort flags are
# reachable from the CLI for the job.run command.
# ---------------------------------------------------------------------------


class TestCliRoleFlags:
    """Verify the 9 per-role CLI flags parse correctly for job run."""

    def _parse(self, argv: list[str]):
        return build_parser().parse_args(argv)

    # --- job.run: all 9 flags parse to correct attributes --------------------

    def test_job_run_builder_provider(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--builder-provider", "claude-cli",
        ])
        assert ns.builder_provider == "claude-cli"

    def test_job_run_builder_model(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--builder-model", "claude-opus-4-20250514",
        ])
        assert ns.builder_model == "claude-opus-4-20250514"

    def test_job_run_builder_effort(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--builder-effort", "medium",
        ])
        assert ns.builder_effort == "medium"

    def test_job_run_reviewer_provider(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--reviewer-provider", "fixture",
        ])
        assert ns.reviewer_provider == "fixture"

    def test_job_run_reviewer_model(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--reviewer-model", "gpt-4o",
        ])
        assert ns.reviewer_model == "gpt-4o"

    def test_job_run_reviewer_effort(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--reviewer-effort", "high",
        ])
        assert ns.reviewer_effort == "high"

    def test_job_run_repair_provider(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--repair-provider", "ollama",
        ])
        assert ns.repair_provider == "ollama"

    def test_job_run_repair_model(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--repair-model", "codellama",
        ])
        assert ns.repair_model == "codellama"

    def test_job_run_repair_effort(self) -> None:
        ns = self._parse([
            "job", "run", "job-id-123",
            "--repair-effort", "low",
        ])
        assert ns.repair_effort == "low"

    # --- Defaults are None when flags are omitted ----------------------------

    def test_job_run_defaults_none(self) -> None:
        ns = self._parse(["job", "run", "job-id-123"])
        for attr in (
            "builder_provider", "builder_model", "builder_effort",
            "reviewer_provider", "reviewer_model", "reviewer_effort",
            "repair_provider", "repair_model", "repair_effort",
        ):
            assert getattr(ns, attr) is None, f"{attr} should default to None"

    # --- Validation through _validate_role_override --------------------------

    def test_invalid_builder_effort_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("builder", "effort", "invalid")
        assert exc.value.code == 2

    def test_empty_builder_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("builder", "model", "")
        assert exc.value.code == 2

    def test_whitespace_only_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("reviewer", "model", "   ")
        assert exc.value.code == 2

    def test_invalid_provider_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("repair", "provider", "bogus-provider")
        assert exc.value.code == 2

    def test_none_value_is_accepted(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        # Should not raise
        _validate_role_override("builder", "provider", None)
        _validate_role_override("reviewer", "model", None)
        _validate_role_override("repair", "effort", None)

    # --- Catalog registration: job run lists all 9 role flags -----------------

    def test_job_run_catalog_has_role_flags(self) -> None:
        cmd = get_command("job.run")
        arg_names = {a.name for a in cmd.args}
        for flag in (
            "--builder-provider", "--builder-model", "--builder-effort",
            "--reviewer-provider", "--reviewer-model", "--reviewer-effort",
            "--repair-provider", "--repair-model", "--repair-effort",
        ):
            assert flag in arg_names, f"job.run missing {flag}"
