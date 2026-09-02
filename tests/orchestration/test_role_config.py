"""Tests for packages.orchestration.role_config — role-based runtime configuration."""

from __future__ import annotations

import warnings

import pytest

from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.role_config import (
    DEFAULT_EFFORT,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    KNOWN_ROLES,
    RoleConfig,
    default_model_for_provider,
    resolve_role_config,
)


class TestDefaults:
    def test_defaults_preserve_current_behavior(self):
        cfg = resolve_role_config("builder")
        assert cfg.role == "builder"
        assert cfg.provider == DEFAULT_PROVIDER == "ollama"
        assert cfg.model == DEFAULT_MODEL == resolve_model_alias("ollama-default")
        assert cfg.effort == DEFAULT_EFFORT == "medium"

    def test_defaults_with_empty_sources(self):
        cfg = resolve_role_config("reviewer", cli_args={}, config_file={})
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == DEFAULT_MODEL
        assert cfg.effort == DEFAULT_EFFORT


class TestConfigFile:
    def test_config_file_overrides_defaults(self):
        cfg = resolve_role_config(
            "builder",
            config_file={"provider": "claude", "model": "opus", "effort": "high"},
        )
        assert cfg.provider == "claude"
        assert cfg.model == "opus"
        assert cfg.effort == "high"

    def test_config_file_partial_override_keeps_defaults(self):
        cfg = resolve_role_config("builder", config_file={"model": "custom"})
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == "custom"
        assert cfg.effort == DEFAULT_EFFORT

    def test_config_file_nested_by_role(self):
        cfg = resolve_role_config(
            "reviewer",
            config_file={"reviewer": {"model": "reviewer-model"}, "builder": {"model": "x"}},
        )
        assert cfg.model == "reviewer-model"


class TestCliOverride:
    def test_cli_overrides_defaults(self):
        cfg = resolve_role_config("repair", cli_args={"model": "cli-model"})
        assert cfg.model == "cli-model"

    def test_cli_nested_by_role(self):
        cfg = resolve_role_config(
            "repair",
            cli_args={"repair": {"provider": "claude"}},
        )
        assert cfg.provider == "claude"


class TestPrecedence:
    def test_cli_overrides_config_file(self):
        cfg = resolve_role_config(
            "builder",
            cli_args={"model": "cli-model"},
            config_file={"model": "file-model", "provider": "claude"},
        )
        # CLI wins for model; config_file still supplies provider.
        assert cfg.model == "cli-model"
        assert cfg.provider == "claude"

    def test_full_precedence_chain(self):
        cfg = resolve_role_config(
            "builder",
            cli_args={"effort": "max"},
            config_file={"provider": "claude", "effort": "low"},
        )
        assert cfg.provider == "claude"   # from config file
        assert cfg.model == resolve_model_alias("claude-flagship")  # provider-aware default
        assert cfg.effort == "max"         # CLI overrides config file


class TestUnknownRole:
    def test_unknown_role_warns_not_crashes(self):
        with pytest.warns(UserWarning):
            cfg = resolve_role_config("nonexistent")
        assert cfg.role == "nonexistent"
        assert cfg.provider == DEFAULT_PROVIDER

    def test_unknown_role_still_honors_overrides(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = resolve_role_config("mystery", cli_args={"model": "m"})
        assert cfg.model == "m"

    def test_known_roles_do_not_warn(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            resolve_role_config("builder")  # must not raise


class TestAllRoles:
    @pytest.mark.parametrize("role", KNOWN_ROLES)
    def test_each_known_role_resolves(self, role):
        cfg = resolve_role_config(role)
        assert cfg.role == role
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == DEFAULT_MODEL
        assert cfg.effort == DEFAULT_EFFORT

    def test_all_nine_roles_present(self):
        assert KNOWN_ROLES == (
            "builder",
            "reviewer",
            "repair",
            "design_worker",
            "test_worker",
            "final_verifier",
            # F070: the mission orchestrator. Same built-in defaults as every
            # other role — the top-tier model is a config act, not a routing
            # policy change (test_each_known_role_resolves pins that).
            "orchestrator",
            # F255: the teacher role. A read-only narrator and tutor;
            # same built-in defaults as every other role.
            "teacher",
            # F108 T002: the artifact-summary generation-call role, registered
            # so F110 (model routing by task class) has a named routing
            # target; same built-in defaults as every other role.
            "summary",
        )

    def test_per_role_config_is_independent(self):
        cfg = resolve_role_config(
            "test_worker",
            config_file={
                "builder": {"model": "builder-model"},
                "test_worker": {"model": "test-model"},
            },
        )
        assert cfg.model == "test-model"


class TestRoleConfigModel:
    def test_frozen(self):
        cfg = resolve_role_config("builder")
        with pytest.raises((AttributeError, TypeError)):
            cfg.model = "x"  # type: ignore[misc]

    def test_direct_construction_defaults(self):
        cfg = RoleConfig(role="builder")
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == DEFAULT_MODEL
        assert cfg.effort == DEFAULT_EFFORT


class TestProviderAwareDefaults:
    """Every expected id is READ from the alias table, never spelled.

    These tests assert which built-in default a provider resolves to, so the
    expected value must come from the table that decides it. Spelling the id
    instead made five of them fail the moment an operator repointed
    `claude-flagship` on 2026-08-25 — they were asserting the STRING rather
    than the contract, and the contract ("claude-cli defaults to the flagship
    alias") had not changed at all. The ollama cases below already read the
    table; the Claude ones had been left behind when F254 landed.
    """

    def test_claude_cli_defaults_to_the_flagship_alias(self):
        cfg = resolve_role_config("builder", cli_args={"provider": "claude-cli"})
        assert cfg.provider == "claude-cli"
        assert cfg.model == resolve_model_alias("claude-flagship")

    def test_claude_defaults_to_the_flagship_alias(self):
        cfg = resolve_role_config("builder", cli_args={"provider": "claude"})
        assert cfg.model == resolve_model_alias("claude-flagship")

    def test_ollama_defaults_to_the_alias_default(self):
        cfg = resolve_role_config("builder", cli_args={"provider": "ollama"})
        assert cfg.model == resolve_model_alias("ollama-default")

    def test_fake_provider_default(self):
        cfg = resolve_role_config("builder", cli_args={"provider": "fake"})
        assert cfg.model == resolve_model_alias("fake")

    def test_explicit_model_overrides_provider_default(self):
        cfg = resolve_role_config(
            "builder",
            cli_args={"provider": "claude-cli", "model": "claude-sonnet-4-20250514"},
        )
        assert cfg.model == "claude-sonnet-4-20250514"

    def test_config_file_provider_sets_model_default(self):
        cfg = resolve_role_config("reviewer", config_file={"provider": "claude-cli"})
        assert cfg.model == resolve_model_alias("claude-flagship")

    def test_config_file_model_overrides_provider_default(self):
        cfg = resolve_role_config(
            "reviewer",
            config_file={"provider": "claude-cli", "model": "my-model"},
        )
        assert cfg.model == "my-model"

    def test_default_model_for_provider_helper(self):
        assert default_model_for_provider("claude-cli") == resolve_model_alias("claude-flagship")
        assert default_model_for_provider("claude") == resolve_model_alias("claude-flagship")
        assert default_model_for_provider("ollama") == resolve_model_alias("ollama-default")
        assert default_model_for_provider("unknown") == DEFAULT_MODEL

    def test_provider_from_config_model_from_cli(self):
        cfg = resolve_role_config(
            "builder",
            cli_args={"model": "custom-model"},
            config_file={"provider": "claude-cli"},
        )
        assert cfg.provider == "claude-cli"
        assert cfg.model == "custom-model"
