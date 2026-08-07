"""Tests for packages.orchestration.model_aliases — the built-in model alias table.

Covers the table's own contract (resolution, loud failure, sorted accessors) and
the F254 RELOCATION: the ids role_config.py and pingpong_provider.py hand out
must be exactly the ones the alias table holds. Pure in-process assertions — no
network, no ANTHROPIC_API_KEY, no config file.
"""
from __future__ import annotations

import inspect

import pytest

from packages.orchestration import pingpong_provider, role_config
from packages.orchestration.model_aliases import (
    MODEL_ALIASES,
    builtin_model_ids,
    known_model_aliases,
    resolve_model_alias,
)


class TestResolveModelAlias:
    def test_table_is_not_empty(self):
        assert MODEL_ALIASES

    @pytest.mark.parametrize("alias", sorted(MODEL_ALIASES))
    def test_every_alias_resolves_to_a_non_empty_id(self, alias):
        resolved = resolve_model_alias(alias)
        assert isinstance(resolved, str)
        assert resolved
        assert resolved == MODEL_ALIASES[alias]

    def test_unknown_alias_raises_key_error_naming_the_alias(self):
        with pytest.raises(KeyError) as excinfo:
            resolve_model_alias("claude-nonexistent")
        message = str(excinfo.value)
        assert "claude-nonexistent" in message

    def test_unknown_alias_message_lists_the_known_aliases(self):
        with pytest.raises(KeyError) as excinfo:
            resolve_model_alias("claude-nonexistent")
        message = str(excinfo.value)
        for alias in known_model_aliases():
            assert alias in message

    def test_unknown_alias_never_falls_back_to_a_guess(self):
        # Failing loud is the point: a silent fallback would ship a model
        # nobody chose, which is the drift the table exists to stop.
        with pytest.raises(KeyError):
            resolve_model_alias("")


class TestAccessors:
    def test_known_model_aliases_are_sorted(self):
        aliases = known_model_aliases()
        assert list(aliases) == sorted(aliases)

    def test_known_model_aliases_cover_the_table(self):
        assert set(known_model_aliases()) == set(MODEL_ALIASES)

    def test_builtin_model_ids_are_sorted(self):
        ids = builtin_model_ids()
        assert list(ids) == sorted(ids)

    def test_builtin_model_ids_have_no_duplicates(self):
        ids = builtin_model_ids()
        assert len(ids) == len(set(ids))

    def test_builtin_model_ids_cover_every_value(self):
        assert set(builtin_model_ids()) == set(MODEL_ALIASES.values())


class TestRelocationIsFaithful:
    """F254: relocating the ids must not change a single resolved value."""

    def test_provider_default_models_table(self):
        assert role_config._PROVIDER_DEFAULT_MODELS == {
            "ollama": resolve_model_alias("ollama-default"),
            "claude-cli": resolve_model_alias("claude-flagship"),
            "claude": resolve_model_alias("claude-flagship"),
            "fake": resolve_model_alias("fake"),
            "fixture": resolve_model_alias("fixture"),
        }

    def test_global_default_model_is_the_ollama_alias(self):
        assert role_config.DEFAULT_MODEL == resolve_model_alias("ollama-default")

    def test_claude_provider_signature_default(self):
        signature = inspect.signature(pingpong_provider.ClaudeProvider.__init__)
        default = signature.parameters["model"].default
        assert default == resolve_model_alias("claude-workhorse")

    def test_claude_provider_instance_uses_the_workhorse_alias(self):
        # Constructing the provider does no I/O: the SDK client is created
        # lazily, so this needs neither the network nor ANTHROPIC_API_KEY.
        provider = pingpong_provider.ClaudeProvider()
        assert provider._model == resolve_model_alias("claude-workhorse")
