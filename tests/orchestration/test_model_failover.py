"""Tests for packages.orchestration.model_failover — F058 T001 (the chains' key, parse and
hard-rule validation) and T002, first part (the failover walk, DECISION F058 D2).
"""

from __future__ import annotations

import pathlib
import shutil
import warnings
from dataclasses import dataclass

import pytest

from packages.orchestration.config import (
    ConfigSource,
    ConfigValue,
    RemedyConfig,
    all_key_specs,
    get_key_spec,
    validate_config,
)
from packages.orchestration.model_failover import (
    FAILOVER_CHAINS_CONFIG_KEY,
    FAILOVER_LINK_KEYS,
    FAILOVER_LOCAL_ROLES,
    FAILOVER_REASON_PROVIDER_UNAVAILABLE,
    FAILOVER_RULE_NAMES,
    LOCAL_PROVIDERS,
    RULE_CORE_ROLE_ON_LOCAL_PROVIDER,
    FailoverChainError,
    FailoverChainRefused,
    FailoverChainViolation,
    FailoverDisclosure,
    FailoverLink,
    FailoverLinkAttempt,
    FailoverProvider,
    build_failover_chains,
    failover_report_line,
    is_failover_trigger,
    parse_failover_chains,
    resolve_failover_chains,
    validate_failover_chains,
)
from packages.orchestration.model_routing import (
    HARD_RULE_NAMES,
    MODEL_TIERS,
    RULE_ORCHESTRATION_BELOW_TOP_TIER,
    RULE_REVIEWER_WEAKER_THAN_WORKER,
    RULE_SAFETY_CLASS_BELOW_MID_TIER,
    TASK_CLASS_TIERS,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from packages.orchestration.role_config import KNOWN_ROLES


def _configure_chains_toml(monkeypatch, tmp_path, toml_body: str) -> None:
    """Make `model_failover.chains` resolve from *toml_body*.

    Written the way tests/orchestration/test_role_config.py's `_configure_override_table`
    configures its own table-valued key: real TOML, written to a pytest `tmp_path`, resolved by
    the real `load_config`, so the precedence chain and the table-valued flatten are exercised
    rather than stubbed. Nothing is written to the repository root.
    """
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text(toml_body, encoding="utf-8")
    loaded = load_config(
        project_path=toml_file,
        user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)


class TestConstants:
    def test_local_providers_is_ollama(self):
        assert LOCAL_PROVIDERS == frozenset({"ollama"})

    def test_the_local_roles_are_exactly_the_cheap_tier_roles(self):
        assert FAILOVER_LOCAL_ROLES == {"teacher", "summary", "study"}

    def test_failover_rule_names_is_the_hard_rules_then_the_local_rule(self):
        assert FAILOVER_RULE_NAMES == (*HARD_RULE_NAMES, RULE_CORE_ROLE_ON_LOCAL_PROVIDER)


class TestParseFailoverChains:
    def test_a_valid_three_role_table_round_trips_every_field_in_order(self):
        raw = {
            "builder": [{"provider": "claude-cli", "model": "sonnet", "tier": "mid"}],
            "teacher": [{"provider": "ollama", "model": "llama", "tier": "cheap"}],
            "reviewer": [
                {"provider": "claude-cli", "model": "sonnet", "tier": "mid"},
                {"provider": "claude-cli", "model": "opus", "tier": "top"},
            ],
        }
        chains = parse_failover_chains(raw)
        assert list(chains) == ["builder", "teacher", "reviewer"]
        assert chains["builder"] == (FailoverLink("claude-cli", "sonnet", "mid"),)
        assert chains["teacher"] == (FailoverLink("ollama", "llama", "cheap"),)
        assert chains["reviewer"] == (
            FailoverLink("claude-cli", "sonnet", "mid"),
            FailoverLink("claude-cli", "opus", "top"),
        )

    def test_an_empty_list_is_an_empty_chain(self):
        assert parse_failover_chains({"builder": []}) == {"builder": ()}

    def test_a_role_known_roles_lacks_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"nope": []})
        assert str(excinfo.value) == (
            "model_failover.chains: 'nope' is not a known role; known roles: "
            f"{', '.join(sorted(KNOWN_ROLES))}"
        )

    def test_an_entry_that_is_not_a_list_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": {"provider": "x"}})
        assert str(excinfo.value) == "model_failover.chains: 'builder' must be a list of links, got dict"

    def test_a_link_that_is_not_a_mapping_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": ["not-a-table"]})
        assert str(excinfo.value) == "model_failover.chains: 'builder' link 1 must be a table, got str"

    def test_a_link_key_not_in_failover_link_keys_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [
                {"provider": "claude-cli", "model": "sonnet", "tier": "mid", "extra": "x"},
            ]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 1 has unknown key 'extra'; a link holds "
            f"exactly {', '.join(FAILOVER_LINK_KEYS)}"
        )

    def test_a_missing_provider_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [{"model": "sonnet", "tier": "mid"}]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 1 must set provider to a non-empty string"
        )

    def test_a_non_string_provider_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [{"provider": 1, "model": "sonnet", "tier": "mid"}]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 1 must set provider to a non-empty string"
        )

    def test_an_empty_provider_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [{"provider": "", "model": "sonnet", "tier": "mid"}]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 1 must set provider to a non-empty string"
        )

    def test_a_missing_model_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [{"provider": "claude-cli", "tier": "mid"}]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 1 must set model to a non-empty string"
        )

    def test_a_missing_tier_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [{"provider": "claude-cli", "model": "sonnet"}]})
        assert str(excinfo.value) == (
            f"model_failover.chains: 'builder' link 1 must set tier to one of {MODEL_TIERS!r}, got None"
        )

    def test_a_tier_model_tiers_does_not_name_is_refused(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains(
                {"builder": [{"provider": "claude-cli", "model": "sonnet", "tier": "huge"}]}
            )
        assert str(excinfo.value) == (
            f"model_failover.chains: 'builder' link 1 must set tier to one of {MODEL_TIERS!r}, "
            "got 'huge'"
        )

    def test_a_repeated_link_names_both_positions(self):
        with pytest.raises(FailoverChainError) as excinfo:
            parse_failover_chains({"builder": [
                {"provider": "claude-cli", "model": "sonnet", "tier": "mid"},
                {"provider": "claude-cli", "model": "sonnet", "tier": "top"},
            ]})
        assert str(excinfo.value) == (
            "model_failover.chains: 'builder' link 2 repeats link 1 (claude-cli sonnet)"
        )


class TestCoreNeverLocal:
    def test_a_builder_link_on_ollama_is_refused(self):
        chains = parse_failover_chains(
            {"builder": [{"provider": "ollama", "model": "llama", "tier": "cheap"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "builder", 1, FailoverLink("ollama", "llama", "cheap"),
                RULE_CORE_ROLE_ON_LOCAL_PROVIDER,
            ),
        )

    def test_a_teacher_link_on_ollama_at_cheap_passes(self):
        chains = parse_failover_chains(
            {"teacher": [{"provider": "ollama", "model": "llama", "tier": "cheap"}]}
        )
        assert validate_failover_chains(chains) == ()


class TestOrchestrationBelowTopTier:
    @pytest.mark.parametrize("role", ["orchestrator", "planner"])
    def test_a_link_below_top_is_refused(self, role):
        chains = parse_failover_chains(
            {role: [{"provider": "claude-cli", "model": "sonnet", "tier": "mid"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                role, 1, FailoverLink("claude-cli", "sonnet", "mid"),
                RULE_ORCHESTRATION_BELOW_TOP_TIER,
            ),
        )

    @pytest.mark.parametrize("role", ["orchestrator", "planner"])
    def test_a_top_link_passes(self, role):
        chains = parse_failover_chains(
            {role: [{"provider": "claude-cli", "model": "opus", "tier": "top"}]}
        )
        assert validate_failover_chains(chains) == ()


class TestSafetyRelevantClassBelowMidTier:
    def test_a_builder_link_at_cheap_is_refused_with_a_custom_safety_set(self):
        chains = parse_failover_chains(
            {"builder": [{"provider": "claude-cli", "model": "sonnet", "tier": "cheap"}]}
        )
        assert validate_failover_chains(
            chains, safety_relevant_classes=frozenset({"standard_build"})
        ) == (
            FailoverChainViolation(
                "builder", 1, FailoverLink("claude-cli", "sonnet", "cheap"),
                RULE_SAFETY_CLASS_BELOW_MID_TIER,
            ),
        )

    def test_the_same_link_passes_with_the_default_empty_safety_set(self):
        chains = parse_failover_chains(
            {"builder": [{"provider": "claude-cli", "model": "sonnet", "tier": "cheap"}]}
        )
        assert validate_failover_chains(chains) == ()


class TestReviewerNotWeakerThanWorker:
    def test_a_reviewer_link_at_cheap_is_refused_against_the_shipped_table(self):
        chains = parse_failover_chains(
            {"reviewer": [{"provider": "claude-cli", "model": "haiku", "tier": "cheap"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "reviewer", 1, FailoverLink("claude-cli", "haiku", "cheap"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
        )

    def test_a_builder_link_at_top_is_refused_while_standard_review_routes_weaker(self):
        chains = parse_failover_chains(
            {"builder": [{"provider": "claude-cli", "model": "opus", "tier": "top"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "builder", 1, FailoverLink("claude-cli", "opus", "top"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
        )

    def test_a_reviewer_link_at_mid_is_refused_when_a_builder_link_is_top(self):
        chains = parse_failover_chains({
            "builder": [{"provider": "claude-cli", "model": "opus", "tier": "top"}],
            "reviewer": [{"provider": "claude-cli", "model": "sonnet", "tier": "mid"}],
        })
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "builder", 1, FailoverLink("claude-cli", "opus", "top"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
            FailoverChainViolation(
                "reviewer", 1, FailoverLink("claude-cli", "sonnet", "mid"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
        )

    def test_a_repair_link_at_top_is_refused_like_a_workers(self):
        chains = parse_failover_chains(
            {"repair": [{"provider": "claude-cli", "model": "opus", "tier": "top"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "repair", 1, FailoverLink("claude-cli", "opus", "top"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
        )

    def test_a_final_verifier_link_counts_on_the_reviewer_side(self):
        chains = parse_failover_chains(
            {"final_verifier": [{"provider": "claude-cli", "model": "haiku", "tier": "cheap"}]}
        )
        assert validate_failover_chains(chains) == (
            FailoverChainViolation(
                "final_verifier", 1, FailoverLink("claude-cli", "haiku", "cheap"),
                RULE_REVIEWER_WEAKER_THAN_WORKER,
            ),
        )

    def test_a_builder_link_at_top_passes_when_standard_review_is_routed_to_top(self):
        chains = parse_failover_chains(
            {"builder": [{"provider": "claude-cli", "model": "opus", "tier": "top"}]}
        )
        effective_tiers = dict(TASK_CLASS_TIERS)
        effective_tiers["standard_review"] = "top"
        assert validate_failover_chains(chains, effective_tiers=effective_tiers) == ()


class TestThreeViolationsTwoRoles:
    def test_build_failover_chains_raises_with_all_three_in_order(self):
        raw = {
            "builder": [
                {"provider": "ollama", "model": "llama-a", "tier": "cheap"},
                {"provider": "ollama", "model": "llama-b", "tier": "cheap"},
            ],
            "orchestrator": [
                {"provider": "claude-cli", "model": "sonnet", "tier": "mid"},
            ],
        }
        with pytest.raises(FailoverChainRefused) as excinfo:
            build_failover_chains(raw)
        expected = (
            FailoverChainViolation(
                "builder", 1, FailoverLink("ollama", "llama-a", "cheap"),
                RULE_CORE_ROLE_ON_LOCAL_PROVIDER,
            ),
            FailoverChainViolation(
                "builder", 2, FailoverLink("ollama", "llama-b", "cheap"),
                RULE_CORE_ROLE_ON_LOCAL_PROVIDER,
            ),
            FailoverChainViolation(
                "orchestrator", 1, FailoverLink("claude-cli", "sonnet", "mid"),
                RULE_ORCHESTRATION_BELOW_TOP_TIER,
            ),
        )
        assert excinfo.value.violations == expected
        assert str(excinfo.value) == (
            "model_failover.chains: refused — "
            "builder link 1 (ollama llama-a, tier cheap): core_role_on_local_provider; "
            "builder link 2 (ollama llama-b, tier cheap): core_role_on_local_provider; "
            "orchestrator link 1 (claude-cli sonnet, tier mid): orchestration_below_top_tier"
        )


class TestResolveFailoverChains:
    def test_unset_gives_empty_and_no_warning(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, "")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert resolve_failover_chains() == {}
        assert caught == []

    def test_a_valid_table_gives_its_chains(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.teacher]]
provider = "ollama"
model = "llama"
tier = "cheap"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = resolve_failover_chains()
        assert result == {"teacher": (FailoverLink("ollama", "llama", "cheap"),)}
        assert caught == []

    def test_a_refused_table_gives_empty_with_one_warning(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "ollama"
model = "llama"
tier = "cheap"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = resolve_failover_chains()
        assert result == {}
        assert len(caught) == 1
        assert str(caught[0].message) == (
            "model_failover.chains: refused — builder link 1 (ollama llama, tier cheap): "
            "core_role_on_local_provider; no role fails over"
        )

    def test_a_table_that_does_not_parse_gives_empty_with_one_warning(self, monkeypatch, tmp_path):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.nope]]
provider = "ollama"
model = "llama"
tier = "cheap"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = resolve_failover_chains()
        assert result == {}
        assert len(caught) == 1
        assert str(caught[0].message) == (
            "model_failover.chains: 'nope' is not a known role; known roles: "
            f"{', '.join(sorted(KNOWN_ROLES))}; no role fails over"
        )

    def test_a_project_tiers_override_routing_standard_review_to_top_admits_a_top_link(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "opus"
tier = "top"

[remedy.model_routing.task_class_tiers]
standard_review = "top"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = resolve_failover_chains()
        assert result == {"builder": (FailoverLink("claude-cli", "opus", "top"),)}
        assert caught == []

    def test_the_same_chain_without_the_override_is_refused_as_reviewer_weaker_than_worker(
        self, monkeypatch, tmp_path
    ):
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "opus"
tier = "top"
''')
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = resolve_failover_chains()
        assert result == {}
        assert len(caught) == 1
        assert str(caught[0].message) == (
            "model_failover.chains: refused — builder link 1 (claude-cli opus, tier top): "
            "reviewer_weaker_than_worker; no role fails over"
        )


class TestRegistry:
    def test_model_failover_chains_is_a_dict_key_with_entry_type_list(self):
        spec = get_key_spec(FAILOVER_CHAINS_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is dict
        assert spec.entry_type is list

    def test_the_three_model_routing_keys_are_consecutive(self):
        keys = [spec.key for spec in all_key_specs()]
        i = keys.index("model_routing.task_class_tiers")
        assert keys[i:i + 3] == [
            "model_routing.task_class_tiers",
            "model_routing.promotion_evidence",
            "model_failover.chains",
        ]

    def test_validate_config_reports_an_entry_that_is_not_a_list(self):
        config = RemedyConfig(values={
            FAILOVER_CHAINS_CONFIG_KEY: ConfigValue(
                key=FAILOVER_CHAINS_CONFIG_KEY,
                value={"builder": "not-a-list"},
                source=ConfigSource.PROJECT,
            ),
        })
        found = validate_config(config)
        assert (
            f"{FAILOVER_CHAINS_CONFIG_KEY}: expected list entries, got 'builder' = 'not-a-list'"
            in found
        )


# ---------------------------------------------------------------------------
# T002, first part — the failover walk (DECISION F058 D2)
# ---------------------------------------------------------------------------

@dataclass
class _RecordedCall:
    """What a stub provider's `build` or `review` was asked, for an exact-value assertion."""

    prompt: str
    timeout_sec: int
    max_output_chars: int
    resume: str | None


class _StubProvider:
    """A small stand-in provider: records every call's keyword arguments and returns a real
    `BuilderOutput` or `ReviewerOutput` carrying the error this test configured. Never a network
    or a real CLI.
    """

    def __init__(
        self,
        name: str,
        *,
        supports_resume: bool = True,
        build_error: str = "",
        review_error: str = "",
        review_error_class: str = "",
    ) -> None:
        self._name = name
        self._supports_resume = supports_resume
        self._build_error = build_error
        self._review_error = review_error
        self._review_error_class = review_error_class
        self.build_calls: list[_RecordedCall] = []
        self.review_calls: list[_RecordedCall] = []
        self.last_build_output: BuilderOutput | None = None
        self.last_review_output: ReviewerOutput | None = None
        # An attribute besides name/supports_resume/build/review, for the test that a
        # FailoverProvider hands an arbitrary attribute through to its primary.
        self.begin_stream_call = "primary-stream-hook"

    @property
    def name(self) -> str:
        return self._name

    @property
    def supports_resume(self) -> bool:
        return self._supports_resume

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        self.build_calls.append(_RecordedCall(prompt, timeout_sec, max_output_chars, resume))
        out = BuilderOutput(error=self._build_error)
        self.last_build_output = out
        return out

    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        self.review_calls.append(_RecordedCall(prompt, timeout_sec, max_output_chars, resume))
        out = ReviewerOutput(error=self._review_error, error_class=self._review_error_class)
        self.last_review_output = out
        return out


class TestIsFailoverTrigger:
    @pytest.mark.parametrize("error", [
        "provider_error: RuntimeError: claude CLI not found on PATH. Install Claude Code CLI to "
        "use --builder-provider claude-cli or --reviewer-provider claude-cli.",
        "provider_error: ConnectionError: connection refused",
        "provider_error: HTTP 503 Service Unavailable",
    ])
    def test_true_for_a_provider_unavailable_or_connection_error(self, error):
        assert is_failover_trigger(BuilderOutput(error=error)) is True

    def test_false_for_no_error(self):
        assert is_failover_trigger(BuilderOutput(error="")) is False

    def test_false_for_a_timeout(self):
        assert is_failover_trigger(BuilderOutput(error="claude CLI timed out after 600s")) is False

    def test_false_for_a_nonzero_exit(self):
        assert is_failover_trigger(BuilderOutput(error="claude CLI exited 1")) is False

    def test_false_for_a_rate_limit_even_when_it_also_reads_not_found(self):
        out = BuilderOutput(error="provider_error: HTTP 429 not found rate limit")
        assert is_failover_trigger(out) is False

    def test_false_for_a_parse_failure(self):
        out = ReviewerOutput(error="reviewer output not found", error_class="parse")
        assert is_failover_trigger(out) is False

    def test_false_for_a_malformed_output(self):
        assert is_failover_trigger(BuilderOutput(error="malformed_output: model not found")) is False

    def test_false_for_a_timeout_that_also_reads_as_unavailable(self):
        out = BuilderOutput(error="provider_error: HTTP 504 Gateway Timeout")
        assert is_failover_trigger(out) is False

    def test_false_for_a_nonzero_exit_that_also_reads_as_unavailable(self):
        out = BuilderOutput(error="claude CLI exited 1: connection refused")
        assert is_failover_trigger(out) is False


class TestFailoverProviderWalk:
    def test_a_primary_that_serves_returns_its_output_unchanged_and_never_calls_build_link(self):
        primary = _StubProvider("claude-cli")

        def build_link(link):
            raise AssertionError("build_link must not be called when the primary serves")

        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=(FailoverLink("claude-cli", "opus", "top"),), build_link=build_link,
        )
        out = fp.build("do it")
        assert out is primary.last_build_output
        assert not hasattr(out, "failover_disclosure")

    def test_primary_unavailable_first_link_serves_discloses_one_attempt(self):
        primary = _StubProvider(
            "claude-cli", build_error="provider_error: ConnectionError: connection refused",
        )
        link_provider = _StubProvider("claude-cli-2")
        link = FailoverLink("claude-cli", "opus", "top")
        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=(link,), build_link=lambda the_link: link_provider,
        )
        out = fp.build("do it", timeout_sec=30, max_output_chars=999, resume="sess-1")

        assert primary.build_calls == [_RecordedCall("do it", 30, 999, "sess-1")]
        assert link_provider.build_calls == [_RecordedCall("do it", 30, 999, None)]
        assert out is link_provider.last_build_output

        expected_attempt = FailoverLinkAttempt(position=1, provider="claude-cli", model="opus", error="")
        expected = FailoverDisclosure(
            role="builder",
            intended_provider="claude-cli",
            intended_model="sonnet",
            primary_error="provider_error: ConnectionError: connection refused",
            attempts=(expected_attempt,),
            used=expected_attempt,
        )
        assert out.failover_disclosure == expected
        assert out.failover_disclosure.to_json() == {
            "reason": FAILOVER_REASON_PROVIDER_UNAVAILABLE,
            "role": "builder",
            "intended": {"provider": "claude-cli", "model": "sonnet"},
            "used": {"position": 1, "provider": "claude-cli", "model": "opus", "error": ""},
            "primary_error": "provider_error: ConnectionError: connection refused",
            "attempts": [{"position": 1, "provider": "claude-cli", "model": "opus", "error": ""}],
        }

    def test_first_link_unavailable_second_link_serves(self):
        primary = _StubProvider(
            "claude-cli", build_error="provider_error: ConnectionError: connection refused",
        )
        link1 = _StubProvider(
            "l1", build_error="provider_error: ConnectionError: connection refused",
        )
        link2 = _StubProvider("l2")
        chain = (
            FailoverLink("claude-cli", "m1", "mid"),
            FailoverLink("claude-cli", "m2", "mid"),
        )

        def build_link(link):
            return link1 if link.model == "m1" else link2

        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=chain, build_link=build_link,
        )
        out = fp.build("do it")
        assert out is link2.last_build_output
        assert len(out.failover_disclosure.attempts) == 2
        assert out.failover_disclosure.used.position == 2

    def test_a_build_link_raising_runtimeerror_is_recorded_and_the_next_link_serves(self):
        primary = _StubProvider(
            "claude-cli", build_error="provider_error: ConnectionError: connection refused",
        )
        link2 = _StubProvider("l2")
        chain = (
            FailoverLink("nope", "m1", "mid"),
            FailoverLink("claude-cli", "m2", "mid"),
        )

        def build_link(link):
            if link.provider == "nope":
                raise RuntimeError("Unknown provider: 'nope'")
            return link2

        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=chain, build_link=build_link,
        )
        out = fp.build("do it")
        assert out.failover_disclosure.attempts[0].error == (
            "provider_error: RuntimeError: Unknown provider: 'nope'"
        )
        assert out is link2.last_build_output
        assert out.failover_disclosure.used.position == 2

    def test_every_link_unavailable_returns_the_primarys_own_output(self):
        primary = _StubProvider(
            "claude-cli", build_error="provider_error: ConnectionError: connection refused",
        )
        link1 = _StubProvider(
            "l1", build_error="provider_error: ConnectionError: connection refused",
        )
        link2 = _StubProvider(
            "l2", build_error="provider_error: ConnectionError: connection refused",
        )
        chain = (
            FailoverLink("claude-cli", "m1", "mid"),
            FailoverLink("claude-cli", "m2", "mid"),
        )

        def build_link(link):
            return link1 if link.model == "m1" else link2

        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=chain, build_link=build_link,
        )
        out = fp.build("do it")
        assert out is primary.last_build_output
        assert out.failover_disclosure.used is None
        assert [attempt.model for attempt in out.failover_disclosure.attempts] == ["m1", "m2"]

    def test_review_walks_the_same_way_and_a_timed_out_link_is_returned_as_is(self):
        primary = _StubProvider(
            "claude-cli", review_error="provider_error: ConnectionError: connection refused",
        )
        link1 = _StubProvider("l1", review_error="claude CLI timed out after 600s")
        link = FailoverLink("claude-cli", "m1", "mid")
        fp = FailoverProvider(
            primary, role="reviewer", intended_provider="claude-cli", intended_model="sonnet",
            links=(link,), build_link=lambda the_link: link1,
        )
        out = fp.review("look at it")
        assert out is link1.last_review_output
        assert out.error == "claude CLI timed out after 600s"
        assert out.failover_disclosure.used.position == 1

    def test_name_supports_resume_primary_links_and_other_attrs_reach_the_primary(self):
        primary = _StubProvider("claude-cli", supports_resume=True)
        link = FailoverLink("claude-cli", "m1", "mid")
        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=(link,), build_link=lambda the_link: primary,
        )
        assert fp.name == "claude-cli"
        assert fp.supports_resume is True
        assert fp.primary is primary
        assert fp.links == (link,)
        assert fp.begin_stream_call == primary.begin_stream_call

    def test_supports_resume_is_false_when_the_primary_answers_false(self):
        primary = _StubProvider("claude-cli", supports_resume=False)
        link = FailoverLink("claude-cli", "m1", "mid")
        fp = FailoverProvider(
            primary, role="builder", intended_provider="claude-cli", intended_model="sonnet",
            links=(link,), build_link=lambda the_link: primary,
        )
        assert fp.supports_resume is False


class TestFailoverReportLine:
    def test_no_rounds_gives_none(self):
        assert failover_report_line({"rounds": []}) is None

    def test_rounds_without_a_failover_give_none(self):
        run_record = {
            "rounds": [{"builder": {"error": ""}, "reviewer": {"verdict": "pass"}}],
        }
        assert failover_report_line(run_record) is None

    def test_one_served_builder_call(self):
        run_record = {"rounds": [{"builder": {"failover": {"used": {"position": 1}}}}]}
        assert failover_report_line(run_record) == (
            "Failover: 1 call was served by a backup model because its usual provider could "
            "not be reached. The run's record names every model tried."
        )

    def test_one_call_that_ran_out(self):
        run_record = {"rounds": [{"builder": {"failover": {"used": None}}}]}
        assert failover_report_line(run_record) == (
            "Failover: 1 call found no backup model that could be reached. "
            "The run's record names every model tried."
        )

    def test_two_served_and_one_ran_out_together(self):
        run_record = {
            "rounds": [
                {
                    "builder": {"failover": {"used": {"position": 1}}},
                    "reviewer": {"failover": {"used": None}},
                },
                {
                    "reviewer": {"failover": {"used": {"position": 1}}},
                },
            ],
        }
        assert failover_report_line(run_record) == (
            "Failover: 2 calls were served by backup models because their usual provider "
            "could not be reached. 1 call found no backup model that could be reached. "
            "The run's record names every model tried."
        )


class TestFailoverThroughARealRun:
    """T002, DECISION F058 D3 — the walk proven or exhausted through a real
    `run_pingpong` call. `shutil.which` is patched to answer `None` for `"claude"`, so
    `claude-cli` always fails with the one error its own missing-binary check raises;
    no real CLI ever runs.
    """

    def _demo_repo(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        return repo

    def _no_real_cli(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.pingpong_provider.shutil.which",
            lambda name: None if name == "claude" else shutil.which(name),
        )

    def test_a_primary_that_is_down_is_served_by_its_chain(self, monkeypatch, tmp_path):
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        self._no_real_cli(monkeypatch)
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "fake"
model = "stand-in"
tier = "mid"
''')
        result = run_pingpong(
            "Fix README", str(self._demo_repo(tmp_path)),
            builder_name="claude-cli", builder_model="primary-model", reviewer_name="fake",
        )

        assert result.final_status != "provider_unavailable"
        record = export_pingpong_json(result)
        failover = record["rounds"][0]["builder"]["failover"]
        assert failover["reason"] == FAILOVER_REASON_PROVIDER_UNAVAILABLE
        assert failover["intended"] == {"provider": "claude-cli", "model": "primary-model"}
        assert failover["used"] == {
            "position": 1, "provider": "fake", "model": "stand-in", "error": "",
        }
        assert failover["primary_error"].startswith(
            "provider_error: RuntimeError: claude CLI not found on PATH"
        )

    def test_a_chain_that_runs_out_leaves_the_primarys_own_failure(self, monkeypatch, tmp_path):
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        self._no_real_cli(monkeypatch)
        _configure_chains_toml(monkeypatch, tmp_path, '''
[[remedy.model_failover.chains.builder]]
provider = "claude-cli"
model = "other-model"
tier = "mid"
''')
        result = run_pingpong(
            "Fix README", str(self._demo_repo(tmp_path)),
            builder_name="claude-cli", builder_model="primary-model", reviewer_name="fake",
        )

        assert result.final_status == "provider_unavailable"
        record = export_pingpong_json(result)
        failover = record["rounds"][0]["builder"]["failover"]
        assert result.error == failover["primary_error"]
        assert failover["used"] is None
        assert [a["provider"] for a in failover["attempts"]] == ["claude-cli"]
        assert [a["model"] for a in failover["attempts"]] == ["other-model"]

    def test_the_same_run_without_a_chain_discloses_nothing(self, monkeypatch, tmp_path):
        from packages.orchestration.pingpong_loop import export_pingpong_json, run_pingpong

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        self._no_real_cli(monkeypatch)
        _configure_chains_toml(monkeypatch, tmp_path, "")
        result = run_pingpong(
            "Fix README", str(self._demo_repo(tmp_path)),
            builder_name="claude-cli", builder_model="primary-model", reviewer_name="fake",
        )

        record = export_pingpong_json(result)
        for round_data in record["rounds"]:
            for role in ("builder", "reviewer"):
                entry = round_data.get(role)
                if entry:
                    assert "failover" not in entry
