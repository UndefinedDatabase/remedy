"""Tests for packages.orchestration.model_failover — F058 T001: the chains' key, parse and
hard-rule validation.
"""

from __future__ import annotations

import pathlib
import warnings

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
    FAILOVER_RULE_NAMES,
    LOCAL_PROVIDERS,
    RULE_CORE_ROLE_ON_LOCAL_PROVIDER,
    FailoverChainError,
    FailoverChainRefused,
    FailoverChainViolation,
    FailoverLink,
    build_failover_chains,
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
