"""Tests for packages.orchestration.role_provider_factory — F058 T002, first part: the failover
walk wired at the seam where a run builds a role's provider (DECISION F058 D2).
"""

from __future__ import annotations

import pathlib
import warnings

from packages.orchestration.model_failover import FailoverLink, FailoverProvider
from packages.orchestration.pingpong_provider import ClaudeCliProvider, FakeProvider
from packages.orchestration.role_provider_factory import create_role_provider


def _configure_chains_toml(monkeypatch, tmp_path, toml_body: str) -> None:
    """Make `model_failover.chains` resolve from *toml_body*, the way
    tests/orchestration/test_model_failover.py's own `_configure_chains_toml` does: real TOML,
    written to a pytest `tmp_path`, resolved by the real `load_config`.
    """
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text(toml_body, encoding="utf-8")
    loaded = load_config(
        project_path=toml_file,
        user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)


class TestNoChainIsUnwrapped:
    def test_fake_provider_with_no_chain_is_a_fake_provider(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        provider = create_role_provider("fake", role="builder", staging_dir=None)
        assert isinstance(provider, FakeProvider)

    def test_claude_cli_builder_with_no_chain_keeps_its_write_mode(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        provider = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            write_mode="allowed-tools",
        )
        assert isinstance(provider, ClaudeCliProvider)
        assert provider.write_mode == "allowed-tools"


class TestChainWraps:
    def test_a_builder_chain_wraps_the_builder_but_not_the_reviewer(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "mid-model"
tier = "mid"
''')
        builder = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
        )
        assert isinstance(builder, FailoverProvider)
        assert isinstance(builder.primary, ClaudeCliProvider)
        assert builder.links == (FailoverLink("claude-cli", "mid-model", "mid"),)

        reviewer = create_role_provider("claude-cli", role="reviewer", staging_dir=None)
        assert not isinstance(reviewer, FailoverProvider)

    def test_a_link_built_through_build_link_carries_its_own_write_mode_and_model(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "mid-model"
tier = "mid"
''')
        builder = create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            write_mode="allowed-tools",
        )
        assert isinstance(builder, FailoverProvider)
        link = builder.links[0]
        link_provider = builder.build_link(link)
        assert isinstance(link_provider, ClaudeCliProvider)
        assert not isinstance(link_provider, FailoverProvider)
        assert link_provider.write_mode == "allowed-tools"
        assert link_provider.model == "mid-model"


class TestRefusedChain:
    def test_a_refused_chain_gives_the_bare_provider_and_exactly_one_warning(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "ollama"
model = "llama"
tier = "cheap"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            provider = create_role_provider(
                "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            )
        assert isinstance(provider, ClaudeCliProvider)
        assert not isinstance(provider, FailoverProvider)
        assert len(caught) == 1


class TestPingpongLoopReachesReplacedCreateProvider:
    def test_create_provider_with_cwd_reaches_a_create_provider_a_test_replaced(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        from packages.orchestration import pingpong_loop

        sentinel = object()

        def fake_create_provider(name, *, model=""):
            return sentinel

        monkeypatch.setattr(pingpong_loop, "create_provider", fake_create_provider)
        result = pingpong_loop._create_provider_with_cwd(
            "fake", role="builder", staging_dir=None,
        )
        assert result is sentinel
