"""DECISION amend1011b D8: every role resolves through the provider adapters; none is tied to one vendor."""

from __future__ import annotations

import pytest

from packages.orchestration.fake_deliverable import DeliverableFakeProvider
from packages.orchestration.pingpong_provider import (
    ClaudeCliProvider,
    OllamaPingPongProvider,
    create_provider,
)
from packages.orchestration.role_config import KNOWN_ROLES, resolve_role_config

# amend1015c D6: the name "fake" builds the fake that writes its task's deliverable file.
_ADAPTERS = {"fake": DeliverableFakeProvider, "ollama": OllamaPingPongProvider, "claude-cli": ClaudeCliProvider}


@pytest.mark.parametrize("role", KNOWN_ROLES)
@pytest.mark.parametrize("provider", sorted(_ADAPTERS))
def test_every_role_takes_the_provider_the_operator_configures(role, provider):
    resolved = resolve_role_config(role, {"provider": provider})

    assert resolved.provider == provider


@pytest.mark.parametrize("provider", sorted(_ADAPTERS))
def test_a_configured_provider_name_dispatches_to_its_own_adapter(provider):
    assert type(create_provider(provider)) is _ADAPTERS[provider]


def test_the_planner_builder_and_reviewer_can_each_name_a_different_vendor():
    cli = {"planner": {"provider": "ollama"}, "builder": {"provider": "claude-cli"},
           "reviewer": {"provider": "fake"}}

    resolved = {role: resolve_role_config(role, cli).provider for role in cli}

    assert resolved == {"planner": "ollama", "builder": "claude-cli", "reviewer": "fake"}
