"""Tests for packages.orchestration.role_config — role-based runtime configuration."""

from __future__ import annotations

import ast
import pathlib
import warnings

import pytest

from packages.orchestration import role_config as role_config_module
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.model_routing import (
    DYNAMIC_ROLE_MARKER,
    ROLE_CONFIG_CALL_SITES,
    ROLE_CONFIG_RESOLVER_NAME,
    ROLE_TASK_CLASSES,
    ROUTED_CALL_EVIDENCE_FIELDS,
    TASK_CLASS_INHERITING_ROLES,
    TASK_CLASS_TIERS,
    TOP_TIER,
    UNDECLARED_ROLE_TASK_CLASS,
    UNKNOWN_CLASS_REASON,
    OriginatingTaskClassRequired,
    resolve_task_class_tier,
    route_role_call,
)
from packages.orchestration.role_config import (
    DEFAULT_EFFORT,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    KNOWN_ROLES,
    RoleConfig,
    default_model_for_provider,
    resolve_orchestrator_model,
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


# ---------------------------------------------------------------------------
# F110 T001, the wiring round: what resolve_role_config RECORDS about routing
# ---------------------------------------------------------------------------
# Every expected class, tier and reason below is READ from model_routing rather
# than spelled, for the reason TestProviderAwareDefaults' docstring already
# gives for this file: a spelled expectation asserts the STRING and not the
# CONTRACT, and goes red the day somebody legitimately re-tiers a class.


class TestRoutedCallEvidenceForDeclaredRoles:
    """Every DECLARED role carries the routing seam's evidence on its config."""

    @pytest.mark.parametrize("role", sorted(ROLE_TASK_CLASSES))
    def test_declared_role_records_its_declared_class(self, role):
        cfg = resolve_role_config(role)
        assert cfg.routed_call is not None
        assert tuple(cfg.routed_call) == ROUTED_CALL_EVIDENCE_FIELDS
        assert cfg.routed_call["task_class"] == ROLE_TASK_CLASSES[role]

    @pytest.mark.parametrize("role", sorted(ROLE_TASK_CLASSES))
    def test_declared_role_records_the_tier_the_seam_answers(self, role):
        cfg = resolve_role_config(role)
        tier, reason = resolve_task_class_tier(ROLE_TASK_CLASSES[role])
        assert cfg.routed_call["tier"] == tier
        assert cfg.routed_call["reason"] == reason

    @pytest.mark.parametrize("role", sorted(ROLE_TASK_CLASSES))
    def test_declared_role_ignores_a_supplied_originating_class(self, role):
        # A declared class IS the declaration; the inventory is not advisory.
        supplied = sorted(TASK_CLASS_TIERS)[0]
        cfg = resolve_role_config(role, originating_task_class=supplied)
        assert cfg.routed_call["task_class"] == ROLE_TASK_CLASSES[role]


class TestRoutedCallEvidenceForInheritingRoles:
    """The inheriting role answers None WITHOUT an origin and routes WITH one.

    The two originating classes used below are chosen because their tiers
    DIFFER — a test below asserts exactly that, so a helper that routed a FIXED
    class could not pass this group by accident.
    """

    def test_the_inheriting_roles_are_known_roles(self):
        # The whole point of the None answer: these resolutions already worked.
        assert TASK_CLASS_INHERITING_ROLES <= set(KNOWN_ROLES)

    @pytest.mark.parametrize("role", sorted(TASK_CLASS_INHERITING_ROLES))
    def test_inheriting_role_records_nothing_without_an_origin(self, role):
        cfg = resolve_role_config(role)
        assert cfg.routed_call is None
        # ...and the ordinary config resolution is untouched by that absence.
        assert cfg.role == role
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == DEFAULT_MODEL
        assert cfg.effort == DEFAULT_EFFORT

    @pytest.mark.parametrize("origin", ["architecture", "format"])
    @pytest.mark.parametrize("role", sorted(TASK_CLASS_INHERITING_ROLES))
    def test_inheriting_role_records_the_originating_class(self, role, origin):
        cfg = resolve_role_config(role, originating_task_class=origin)
        assert cfg.routed_call is not None
        assert tuple(cfg.routed_call) == ROUTED_CALL_EVIDENCE_FIELDS
        assert cfg.routed_call["task_class"] == origin
        tier, reason = resolve_task_class_tier(origin)
        assert cfg.routed_call["tier"] == tier
        assert cfg.routed_call["reason"] == reason

    def test_the_two_origins_really_do_route_to_different_tiers(self):
        # THE DISCRIMINATOR. Without this, one fixed tier could satisfy the
        # parametrized case above for both origins.
        architecture_tier, _ = resolve_task_class_tier("architecture")
        format_tier, _ = resolve_task_class_tier("format")
        assert architecture_tier != format_tier

    def test_the_seam_itself_still_raises_for_a_direct_caller(self):
        # Only the CONFIG layer swallows it, and only this one exception.
        for role in sorted(TASK_CLASS_INHERITING_ROLES):
            with pytest.raises(OriginatingTaskClassRequired):
                route_role_call(role)


class TestRoutedCallEvidenceForUndeclaredRoles:
    """The undeclared role warns — now from BOTH layers — and routes conservatively."""

    def test_undeclared_role_routes_conservatively(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = resolve_role_config("nonexistent")
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.routed_call["task_class"] == UNDECLARED_ROLE_TASK_CLASS
        assert cfg.routed_call["reason"] == UNKNOWN_CLASS_REASON
        assert cfg.routed_call["tier"] == TOP_TIER

    def test_both_layers_warn_and_every_warning_is_a_user_warning(self):
        # TWO warnings are raised for such a role now — role_config's own
        # unknown-role warning and model_routing's undeclared-class one. The
        # assertion is on their CATEGORY and on both messages being present,
        # never on a count of ONE: a count of one is what this wiring falsified.
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            resolve_role_config("nonexistent")
        assert len(caught) >= 2
        assert all(issubclass(w.category, UserWarning) for w in caught)
        messages = [str(w.message) for w in caught]
        assert any("Unknown role" in m for m in messages)
        assert any(UNDECLARED_ROLE_TASK_CLASS in m for m in messages)


class TestRoleConfigStaysHashableAndComparable:
    """``compare=False`` on the new field pinned as a PROPERTY, not as a style.

    A frozen dataclass derives ``__hash__`` from its COMPARED fields, so a dict
    field left in the comparison makes ``hash()`` raise ``TypeError: unhashable
    type: 'dict'``. These tests are what make dropping ``compare=False`` a red
    suite rather than a silent regression in something no caller declared.
    """

    def test_a_resolved_config_with_real_evidence_is_hashable(self):
        cfg = resolve_role_config("builder")
        assert cfg.routed_call is not None  # real evidence, not None
        assert isinstance(hash(cfg), int)
        assert len({cfg, resolve_role_config("builder")}) == 1

    def test_configs_compare_on_provider_model_and_effort(self):
        # Same role, DIFFERENT routed_call payloads (None against a full
        # mapping), identical provider/model/effort: the same RESOLUTION.
        without_origin = resolve_role_config("repair")
        with_origin = resolve_role_config("repair", originating_task_class="format")
        assert without_origin.routed_call != with_origin.routed_call
        assert without_origin == with_origin
        assert hash(without_origin) == hash(with_origin)

    def test_a_directly_constructed_config_records_nothing(self):
        cfg = RoleConfig(role="builder")
        assert cfg.routed_call is None


class TestWiringChangedNoResolution:
    """The wiring RECORDS; it does not SELECT. Provider, model and effort stand."""

    @pytest.mark.parametrize("role", KNOWN_ROLES)
    def test_every_known_role_resolves_exactly_as_before(self, role):
        cfg = resolve_role_config(role)
        assert cfg.role == role
        assert cfg.provider == DEFAULT_PROVIDER
        assert cfg.model == DEFAULT_MODEL
        assert cfg.effort == DEFAULT_EFFORT

    def test_a_config_file_override_still_wins_over_the_defaults(self):
        cfg = resolve_role_config(
            "builder",
            config_file={"provider": "claude-cli", "effort": "high"},
        )
        assert cfg.provider == "claude-cli"
        assert cfg.model == resolve_model_alias("claude-flagship")
        assert cfg.effort == "high"
        # ...and the routing evidence is unmoved by a CONFIG override, because a
        # configuration choice is not a policy choice.
        assert cfg.routed_call["task_class"] == ROLE_TASK_CLASSES["builder"]

    def test_the_orchestrator_model_resolver_still_answers(self):
        assert isinstance(resolve_orchestrator_model(), str)


class TestCallSiteInventoryUnmoved:
    """The wiring adds no CALL to the resolver — it changes what that call DOES.

    Both assertions compare against :data:`ROLE_CONFIG_CALL_SITES` itself. A
    spelled numeral here would have to be re-typed by every future round that
    adds a call site, which is the rot the inventory constant exists to stop.
    """

    def test_role_config_holds_the_inventoried_number_of_resolver_calls(self):
        source = pathlib.Path(role_config_module.__file__).read_text(encoding="utf-8")
        found = [
            node
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == ROLE_CONFIG_RESOLVER_NAME
        ]
        declared = [
            pair
            for pair in ROLE_CONFIG_CALL_SITES
            if pair[0] == "packages/orchestration/role_config.py"
        ]
        assert declared, "the inventory names no call site in role_config.py"
        assert len(found) == len(declared)

    def test_every_literal_role_of_the_inventory_still_resolves_and_routes(self):
        for path, role in ROLE_CONFIG_CALL_SITES:
            if role == DYNAMIC_ROLE_MARKER:
                continue
            cfg = resolve_role_config(role)
            assert cfg.role == role
            assert cfg.routed_call is not None, path
