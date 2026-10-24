"""Tests for packages.orchestration.role_provider_factory — F058 T002, first part: the failover
walk wired at the seam where a run builds a role's provider (DECISION F058 D2).
"""

from __future__ import annotations

import json
import pathlib
import time
import warnings

from packages.orchestration.model_failover import FailoverLink, FailoverProvider
from packages.orchestration.pingpong_provider import BuilderOutput, ClaudeCliProvider
from packages.orchestration.pingpong_provider_fake import FakeProvider
from packages.orchestration.role_provider_factory import create_role_provider
from packages.orchestration.sandbox_profiles import WORKER_SANDBOX_FILENAME
from packages.orchestration.worker_isolation import WORKER_ISOLATION_FILENAME


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
        assert isinstance(builder._primary, ClaudeCliProvider)
        assert builder._links == (FailoverLink("claude-cli", "mid-model", "mid"),)

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
        link = builder._links[0]
        link_provider = builder._build_link(link)
        assert isinstance(link_provider, ClaudeCliProvider)
        assert not isinstance(link_provider, FailoverProvider)
        assert link_provider.write_mode == "allowed-tools"
        assert link_provider.model == "mid-model"


class _FixedAnswerProvider:
    """A stand-in provider: `build` answers the one error it was made with."""

    supports_resume = False
    name = "stub"

    def __init__(self, error: str) -> None:
        self._error = error

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        return BuilderOutput(error=self._error)


class TestCooldownIsConfigured:
    def test_the_wrapper_holds_the_primary_for_the_configured_45_seconds(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[remedy.model_failover]
cooldown_s = 45

[[remedy.model_failover.chains.builder]]
provider = "claude"
model = "mid-model"
tier = "mid"
''')

        def make_provider(name, *, model=""):
            return _FixedAnswerProvider("provider_error: ConnectionError: connection refused"
                                    if name == "primary" else "")

        builder = create_role_provider(
            "primary", role="builder", staging_dir=None, make_provider=make_provider,
        )
        assert isinstance(builder, FailoverProvider)
        # Read from the wrapper's own field (R-1294), bracketed by the clock the wrapper uses by
        # default (time.monotonic).
        before = time.monotonic()
        out = builder.build("do it")
        after = time.monotonic()
        assert out.error == ""
        assert before + 45 <= builder._held_until <= after + 45


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


class TestWorkerIsolationEvidence:
    """DECISION F152 D3 (4): one worker_isolation.jsonl line per claude-cli provider build."""

    def test_a_build_with_an_evidence_directory_writes_exactly_one_line(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="claude-x", stream_evidence_dir=str(tmp_path / "evidence"),
        )
        lines = (tmp_path / "evidence" / WORKER_ISOLATION_FILENAME).read_text(
            encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["role"] == "builder"
        assert record["provider"] == "claude-cli"
        assert record["model"] == "claude-x"
        assert record["method"] == "tool_flag"
        assert record["applied"] is True
        assert record["home"] == "operator"
        assert isinstance(record["env_digest"], str) and len(record["env_digest"]) == 64
        assert record["adr_ref"] == "docs/adr/0002-claude-cli-worker-isolation.md"

    def test_a_build_without_a_directory_writes_nothing(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="claude-x", stream_evidence_dir=None,
        )
        assert not (tmp_path / "evidence").exists()
        assert not any(tmp_path.rglob(WORKER_ISOLATION_FILENAME))


class TestWorkerSandboxEvidence:
    """DECISION F162 D5 (4): one worker_sandbox.jsonl line per claude-cli provider build."""

    def test_a_claude_cli_build_writes_exactly_one_sandbox_line(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        create_role_provider(
            "claude-cli", role="builder", staging_dir=str(tmp_path / "staging"),
            model="claude-x", stream_evidence_dir=str(tmp_path / "evidence"),
        )
        lines = (tmp_path / "evidence" / WORKER_SANDBOX_FILENAME).read_text(
            encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["role"] == "builder"
        assert record["provider"] == "claude-cli"
        assert record["model"] == "claude-x"
        assert record["profile"] == "claude-cli"
        assert record["runner"] == "process"
        assert record["tool_sandbox"] is False

    def test_a_non_claude_cli_build_writes_none(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        create_role_provider(
            "fake", role="builder", staging_dir=None, stream_evidence_dir=str(tmp_path / "evidence"),
        )
        assert not any(tmp_path.rglob(WORKER_SANDBOX_FILENAME))
