"""Tests for role_config.resolve_orchestrator_model — F110 T001c, order E.b.

THE DISCRIMINATOR IS PATCHED ON PURPOSE. At today's configuration
``resolve_role_config("orchestrator").model`` and the Ollama planner's own
default answer the SAME model id, so a test that merely compared the two live
sources would pass against the OLD code — which read ``orchestrator.model``
directly and never consulted role_config — just as readily as against the new.
Every fall-through case below therefore forces ``resolve_role_config`` to a
SENTINEL the planner default is not, and asserts the sentinel comes back. That
is what makes the seam, rather than a coincidence of configuration, the thing
under test.

No concrete model id is spelled anywhere in this file, deliberately: an id is a
configuration fact, and asserting one here would make these tests go stale the
day an operator repoints the alias table.
"""

from __future__ import annotations

import pytest

from packages.orchestration import role_config
from packages.orchestration.role_config import RoleConfig, resolve_orchestrator_model

#: A model id no real provider default is, so an assertion on it can only pass
#: because the value travelled the path the test says it did.
SENTINEL_CONFIGURED = "sentinel-configured-model:test"
SENTINEL_FROM_ROLE_CONFIG = "sentinel-role-config-model:test"

#: The one config key the orchestrator's operator override lives at, spelled
#: once so the stub below and the test that proves it was read agree by
#: construction rather than by two people typing the same string.
ORCHESTRATOR_MODEL_CONFIG_KEY = "orchestrator.model"


class _FakeConfig:
    """A permissive config double that RECORDS every key it was asked for.

    WHY IT IS PERMISSIVE. This stub used to refuse every key but
    ``orchestrator.model`` with an assertion, and that refusal was the proof of
    WHICH key ``resolve_orchestrator_model`` read. It stopped being right when
    the fall-through path gained a SECOND legitimate reader: ``resolve_role_config``
    now reads ``model_routing.task_class_tiers``, so the refusal turned a correct
    read into a test failure. The proof did not go away — it moved to
    ``TestTheOperatorOverrideKeyIsTheOneRead`` below, which reads
    :attr:`keys_read` and asserts positively. ``None`` is the right answer for
    every other key: it means "no per-project overrides", which is exactly the
    state these tests intend.
    """

    def __init__(self, value):
        self._value = value
        self.keys_read: list[str] = []

    def get(self, key):
        self.keys_read.append(key)
        if key == ORCHESTRATOR_MODEL_CONFIG_KEY:
            return self._value
        return None


def _patch_config(monkeypatch, value) -> _FakeConfig:
    """Make ``orchestrator.model`` answer ``value``; return the stub itself.

    Patched at ``packages.orchestration.config.get_config``, which is the name
    the function resolves at CALL time — it imports get_config inside its own
    body, so patching the defining module is what actually reaches it.

    ONE instance is built and the lambda hands out that same object, because a
    stub constructed afresh per call would throw away the key recording before
    any test could read it.
    """
    config = _FakeConfig(value)
    monkeypatch.setattr(
        "packages.orchestration.config.get_config",
        lambda: config,
    )
    return config


def _patch_role_config(monkeypatch, model: str) -> None:
    """Force ``resolve_role_config("orchestrator").model`` to ``model``.

    Patched on the role_config MODULE, because that is where the function looks
    the name up when it falls through.
    """
    def _fake(role, cli_args=None, config_file=None):
        assert role == "orchestrator", f"unexpected role {role!r}"
        return RoleConfig(role=role, model=model)

    monkeypatch.setattr(role_config, "resolve_role_config", _fake)


class TestConfiguredKeyWins:
    """A set, non-empty ``orchestrator.model`` outranks everything below it."""

    def test_configured_value_is_returned(self, monkeypatch):
        _patch_config(monkeypatch, SENTINEL_CONFIGURED)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        assert resolve_orchestrator_model() == SENTINEL_CONFIGURED

    def test_configured_value_wins_over_the_role_config_answer(self, monkeypatch):
        """Both sources answer, and they disagree; the config key is the winner."""
        _patch_config(monkeypatch, SENTINEL_CONFIGURED)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        result = resolve_orchestrator_model()
        assert result == SENTINEL_CONFIGURED
        assert result != SENTINEL_FROM_ROLE_CONFIG


class TestUnsetKeyFallsThroughToRoleConfig:
    """The seam this round exists to move, tested with a PATCHED discriminator."""

    def test_unset_key_returns_the_role_config_model(self, monkeypatch):
        _patch_config(monkeypatch, None)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        assert resolve_orchestrator_model() == SENTINEL_FROM_ROLE_CONFIG

    def test_unset_key_does_not_answer_from_a_rival_source(self, monkeypatch):
        """The sentinel is a value ONLY role_config could have supplied.

        The Ollama planner's built-in default is read here for exactly one
        purpose: to assert the answer is NOT it. Nothing asserts what it IS.
        """
        from packages.providers.ollama_planner.provider import _DEFAULT_MODEL

        _patch_config(monkeypatch, None)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        result = resolve_orchestrator_model()
        assert result == SENTINEL_FROM_ROLE_CONFIG
        assert result != _DEFAULT_MODEL

    @pytest.mark.parametrize("configured", [None, 0, False, [], {}, 17])
    def test_a_non_string_key_is_treated_as_unset(self, monkeypatch, configured):
        _patch_config(monkeypatch, configured)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        assert resolve_orchestrator_model() == SENTINEL_FROM_ROLE_CONFIG


class TestEmptyConfiguredValueIsUnset:
    """An empty or whitespace-only key is an operator who set nothing."""

    @pytest.mark.parametrize(
        "configured",
        ["", " ", "   ", "\t", "\n", " \t\n "],
        ids=["empty", "one-space", "spaces", "tab", "newline", "mixed-whitespace"],
    )
    def test_blank_value_falls_through_to_role_config(self, monkeypatch, configured):
        _patch_config(monkeypatch, configured)
        _patch_role_config(monkeypatch, SENTINEL_FROM_ROLE_CONFIG)

        assert resolve_orchestrator_model() == SENTINEL_FROM_ROLE_CONFIG


class TestTheAnswerIsAlwaysUsable:
    """A shape check, and it says so: it cannot discriminate between sources."""

    def test_the_unpatched_answer_is_a_non_empty_string(self):
        result = resolve_orchestrator_model()
        assert isinstance(result, str)
        assert result.strip() != ""

    def test_the_configured_answer_is_a_non_empty_string(self, monkeypatch):
        _patch_config(monkeypatch, SENTINEL_CONFIGURED)

        result = resolve_orchestrator_model()
        assert isinstance(result, str)
        assert result.strip() != ""

    def test_the_fall_through_answer_is_a_non_empty_string(self, monkeypatch):
        _patch_config(monkeypatch, None)

        result = resolve_orchestrator_model()
        assert isinstance(result, str)
        assert result.strip() != ""


class TestTheOperatorOverrideKeyIsTheOneRead:
    """The positive form of the proof the stub's old refusal carried.

    Asserting that the operator-override key is among the keys the config was
    asked for says the same thing the refusal said — this function reads THAT
    key — without also forbidding the other, legitimate readers on the
    fall-through path.
    """

    def test_the_operator_override_key_is_among_the_keys_read(self, monkeypatch):
        config = _patch_config(monkeypatch, None)

        resolve_orchestrator_model()

        assert ORCHESTRATOR_MODEL_CONFIG_KEY in config.keys_read
