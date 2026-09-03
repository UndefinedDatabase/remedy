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
    MODEL_TIERS,
    ORCHESTRATION_TASK_CLASSES,
    OVERRIDE_REASON,
    PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES,
    PROMOTION_EVIDENCE_NESTED_FIELD,
    PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE,
    PROMOTION_MINIMUM_OVERALL_PASS_RATE,
    PROMOTION_MINIMUM_RUNS_PER_FIXTURE,
    REVIEWER_WORKER_CLASS_PAIRS,
    ROLE_CONFIG_CALL_SITES,
    ROLE_CONFIG_RESOLVER_NAME,
    ROLE_TASK_CLASSES,
    ROUTED_CALL_EVIDENCE_FIELDS,
    RULE_ORCHESTRATION_BELOW_TOP_TIER,
    RULE_PROMOTION_WITHOUT_EVIDENCE,
    RULE_REVIEWER_WEAKER_THAN_WORKER,
    SAFETY_RELEVANT_CLASSES,
    TASK_CLASS_INHERITING_ROLES,
    TASK_CLASS_TIERS,
    TOP_TIER,
    UNDECLARED_ROLE_TASK_CLASS,
    UNKNOWN_CLASS_REASON,
    OriginatingTaskClassRequired,
    PromotionAssertionResults,
    is_task_class_promotion,
    model_tier_rank,
    resolve_task_class_tier,
    route_role_call,
)
from packages.orchestration.role_config import (
    DEFAULT_EFFORT,
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    KNOWN_ROLES,
    PROMOTION_EVIDENCE_CONFIG_KEY,
    TASK_CLASS_TIERS_CONFIG_KEY,
    RoleConfig,
    default_model_for_provider,
    resolve_effective_task_class_tiers,
    resolve_orchestrator_model,
    resolve_promotion_evidence,
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


# ---------------------------------------------------------------------------
# F110 R10 — the CONFIGURED override table reaches a routed call
# ---------------------------------------------------------------------------
# The two fixtures below DERIVE their role, class and tier from model_routing's
# own constants instead of spelling them. A spelled pair would still pass after
# a re-tiering that made it meaningless — the seed table moving is exactly the
# event these tests exist to survive.


def _legally_retierable_role() -> tuple[str, str, str]:
    """Return ``(role, task_class, target_tier)`` no hard rule protects.

    A DECLARED role whose class is outside :data:`ORCHESTRATION_TASK_CLASSES`,
    outside every :data:`REVIEWER_WORKER_CLASS_PAIRS` pair and outside
    :data:`SAFETY_RELEVANT_CLASSES`, moved to a STRONGER tier — stronger, so the
    move is not a promotion and needs no benchmark evidence.
    """
    paired = {name for pair in REVIEWER_WORKER_CLASS_PAIRS for name in pair}
    for role in sorted(ROLE_TASK_CLASSES):
        task_class = ROLE_TASK_CLASSES[role]
        if task_class in ORCHESTRATION_TASK_CLASSES or task_class in paired:
            continue
        if task_class in SAFETY_RELEVANT_CLASSES:
            continue
        seeded = TASK_CLASS_TIERS[task_class]
        stronger = [
            tier for tier in MODEL_TIERS
            if model_tier_rank(tier) > model_tier_rank(seeded)
        ]
        if stronger:
            return role, task_class, stronger[0]
    raise AssertionError("no declared role is re-tierable without breaking a rule")


def _illegally_demotable_role() -> tuple[str, str, str]:
    """Return ``(role, task_class, target_tier)`` an ORCHESTRATION rule pins.

    The target is the CHEAPEST tier, so the map breaks
    :data:`RULE_ORCHESTRATION_BELOW_TOP_TIER` by construction.
    """
    for role in sorted(ROLE_TASK_CLASSES):
        task_class = ROLE_TASK_CLASSES[role]
        if task_class in ORCHESTRATION_TASK_CLASSES:
            return role, task_class, MODEL_TIERS[0]
    raise AssertionError("no declared role carries an orchestration task class")


def _configure_override_table(monkeypatch, tmp_path, table) -> None:
    """Make ``model_routing.task_class_tiers`` answer *table* for this test.

    The table is written as REAL TOML to a pytest ``tmp_path`` and resolved by
    the REAL ``load_config``, so the precedence chain and the table-valued
    flatten are exercised rather than stubbed. NOTHING is written to the
    repository root: a ``remedy.toml`` there would change how every test in the
    suite resolves configuration.

    Patched at ``packages.orchestration.config.get_config``, the name
    ``resolve_effective_task_class_tiers`` resolves at CALL time — it imports
    get_config inside its own body, the idiom this module established.
    """
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    lines = [f"[remedy.{TASK_CLASS_TIERS_CONFIG_KEY}]"]
    lines += [f'{task_class} = "{tier}"' for task_class, tier in table.items()]
    toml_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    loaded = load_config(
        project_path=toml_file,
        user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    monkeypatch.setattr(
        "packages.orchestration.config.get_config", lambda: loaded
    )


class TestConfigKeyIsRegisteredWhereItIsRead:
    """The key this module reads is the key config.py registers — pinned."""

    def test_the_config_key_constant_names_a_registered_spec(self):
        from packages.orchestration.config import get_key_spec

        spec = get_key_spec(TASK_CLASS_TIERS_CONFIG_KEY)
        assert spec is not None, TASK_CLASS_TIERS_CONFIG_KEY
        assert spec.value_type is dict


class TestEffectiveTaskClassTiers:
    """The shipped table with the configured overrides laid over it."""

    def test_nothing_configured_returns_the_shipped_table(self):
        assert resolve_effective_task_class_tiers() == TASK_CLASS_TIERS

    def test_an_explicitly_empty_table_returns_the_shipped_table(
        self, monkeypatch, tmp_path
    ):
        _configure_override_table(monkeypatch, tmp_path, {})
        assert resolve_effective_task_class_tiers() == TASK_CLASS_TIERS

    def test_a_legal_table_is_laid_over_the_shipped_one(self, monkeypatch, tmp_path):
        _, task_class, tier = _legally_retierable_role()
        _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
        effective = resolve_effective_task_class_tiers()
        assert effective[task_class] == tier
        # ...and every OTHER class is untouched: an override is an overlay.
        for other, seeded in TASK_CLASS_TIERS.items():
            if other != task_class:
                assert effective[other] == seeded


class TestConfiguredOverrideReachesARoutedCall:
    """F110's whole point: a project re-tiers a class and the EVIDENCE moves."""

    def test_a_legal_override_reaches_a_routed_call(self, monkeypatch, tmp_path):
        role, task_class, tier = _legally_retierable_role()
        seeded_tier, seeded_reason = resolve_task_class_tier(task_class)
        # THE DISCRIMINATOR: without this, the seed tier could satisfy the
        # assertions below and the override would prove nothing.
        assert tier != seeded_tier
        _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
        cfg = resolve_role_config(role)
        assert cfg.routed_call is not None
        assert cfg.routed_call["task_class"] == task_class
        assert cfg.routed_call["tier"] == tier
        assert cfg.routed_call["reason"] == OVERRIDE_REASON
        assert cfg.routed_call["reason"] != seeded_reason

    def test_an_unconfigured_run_still_records_the_seed_mapping(self):
        role, task_class, _ = _legally_retierable_role()
        seeded_tier, seeded_reason = resolve_task_class_tier(task_class)
        cfg = resolve_role_config(role)
        assert cfg.routed_call["tier"] == seeded_tier
        assert cfg.routed_call["reason"] == seeded_reason


class TestRefusedOverrideWarnsAndRoutesSeeded:
    """DECISION F110 D5: the hard rules win by REFUSING, loudly, not silently.

    The rule name is asserted by READING
    :data:`RULE_ORCHESTRATION_BELOW_TOP_TIER`; a spelled name would freeze a
    string this suite does not own.
    """

    def test_an_illegal_override_warns_with_the_rule_named(self, monkeypatch, tmp_path):
        _, task_class, tier = _illegally_demotable_role()
        _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            resolve_effective_task_class_tiers()
        assert caught, "a refused override map emitted no warning at all"
        assert all(issubclass(w.category, UserWarning) for w in caught)
        messages = [str(w.message) for w in caught]
        assert any(RULE_ORCHESTRATION_BELOW_TOP_TIER in m for m in messages), messages
        assert any(TASK_CLASS_TIERS_CONFIG_KEY in m for m in messages), messages

    def test_an_illegal_override_routes_against_the_shipped_table(
        self, monkeypatch, tmp_path
    ):
        role, task_class, tier = _illegally_demotable_role()
        seeded_tier, seeded_reason = resolve_task_class_tier(task_class)
        assert tier != seeded_tier
        _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = resolve_role_config(role)
        # The override did NOT take effect — seeded tier, seeded reason.
        assert cfg.routed_call["tier"] == seeded_tier
        assert cfg.routed_call["reason"] == seeded_reason
        assert cfg.routed_call["tier"] != tier

    def test_a_refused_table_does_not_break_config_resolution(
        self, monkeypatch, tmp_path
    ):
        # THE ROUND 9 LESSON, ONE LAYER FURTHER OUT: a routing fault must not
        # become a config-resolution fault.
        role, task_class, tier = _illegally_demotable_role()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            baseline = resolve_role_config(role)
            _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
            refused = resolve_role_config(role)
        assert refused.provider == baseline.provider
        assert refused.model == baseline.model
        assert refused.effort == baseline.effort
        assert refused.role == baseline.role

    def test_every_declared_role_still_resolves_under_a_refused_table(
        self, monkeypatch, tmp_path
    ):
        _, task_class, tier = _illegally_demotable_role()
        _configure_override_table(monkeypatch, tmp_path, {task_class: tier})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for role in sorted(ROLE_TASK_CLASSES):
                cfg = resolve_role_config(role)
                assert cfg.routed_call is not None, role
                assert cfg.routed_call["tier"] == TASK_CLASS_TIERS[
                    ROLE_TASK_CLASSES[role]
                ]


# ---------------------------------------------------------------------------
# F110 T003 — the PROMOTION-EVIDENCE table reaching the builder and the seam
# ---------------------------------------------------------------------------
# The fixtures below DERIVE the class, the role, the tier, every evidence field
# name and every bar from model_routing's own constants. A spelled pair or a
# spelled field would still pass after a re-seeding or a rename that made it
# meaningless, and surviving exactly that event is why these tests exist.


def _evidence_promotable_role() -> tuple[str, str, str]:
    """Return ``(role, task_class, promoted_tier)`` a documented run can license.

    A DECLARED role whose class is seeded at :data:`TOP_TIER` and which no HARD
    rule protects — outside :data:`ORCHESTRATION_TASK_CLASSES`, outside every
    :data:`REVIEWER_WORKER_CLASS_PAIRS` pair and outside
    :data:`SAFETY_RELEVANT_CLASSES` — moved to the CHEAPEST tier, so the move IS
    a promotion and the promotion rule is the ONLY rule standing in its way.
    """
    paired = {name for pair in REVIEWER_WORKER_CLASS_PAIRS for name in pair}
    cheapest = MODEL_TIERS[0]
    for role in sorted(ROLE_TASK_CLASSES):
        task_class = ROLE_TASK_CLASSES[role]
        if task_class in ORCHESTRATION_TASK_CLASSES or task_class in paired:
            continue
        if task_class in SAFETY_RELEVANT_CLASSES:
            continue
        if TASK_CLASS_TIERS[task_class] != TOP_TIER:
            continue
        if model_tier_rank(cheapest) >= model_tier_rank(TOP_TIER):
            continue
        return role, task_class, cheapest
    raise AssertionError("no declared role carries a top-tier class a run could promote")


def _well_formed_evidence_entry(task_class: str) -> dict[str, object]:
    """Return a raw evidence entry for *task_class* that MEETS every bar.

    Every field of :data:`PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES` is set, plus the
    nested :data:`PROMOTION_EVIDENCE_NESTED_FIELD` table, so the record is
    COMPLETE — an unset field would be refused as INCOMPLETE rather than as
    unevidenced, and the test would then be proving the wrong refusal. The names
    come from those constants and from ``PromotionAssertionResults`` itself; the
    numbers come from the module's own bars, so raising a bar moves this fixture
    with it instead of leaving it quietly under one.
    """
    bars = {
        "block_level_pass_rate": PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE,
        "overall_pass_rate": PROMOTION_MINIMUM_OVERALL_PASS_RATE,
    }
    assert set(bars) == set(PromotionAssertionResults.__dataclass_fields__), bars
    entry: dict[str, object] = {}
    for field_name, expected in PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES.items():
        if field_name == "runs_per_fixture":
            entry[field_name] = PROMOTION_MINIMUM_RUNS_PER_FIXTURE
        elif expected is int:
            entry[field_name] = 12345
        elif expected is float:
            entry[field_name] = 0.5
        else:
            entry[field_name] = f"{field_name}-of-{task_class}"
    entry[PROMOTION_EVIDENCE_NESTED_FIELD] = dict(bars)
    return entry


def _toml_scalar(value: object) -> str:
    """Render *value* as a TOML scalar, REFUSING a bool.

    A bool is refused rather than rendered because ``bool`` is a subclass of
    ``int``: a fixture emitting ``true`` for an int field would be probing the
    parser's bool guard while claiming to build a well-formed record.
    """
    assert not isinstance(value, bool), value
    if isinstance(value, str):
        return f'"{value}"'
    return repr(value)


def _configure_promotion_tables(monkeypatch, tmp_path, tiers, evidence=None) -> None:
    """Make BOTH model-routing config tables answer for this test.

    ``tiers`` maps task class to tier. ``evidence`` is either a mapping of task
    class to a raw entry, or a plain STRING — the shape an environment variable
    could carry where a table belongs — or ``None`` for a key left unset. Both
    tables are written as REAL TOML to a pytest ``tmp_path`` and resolved by the
    REAL ``load_config``, so the table-valued flatten and the precedence chain
    are exercised rather than stubbed. NOTHING is written to the repository
    root: a ``remedy.toml`` there would change how every test in the suite
    resolves configuration.
    """
    from packages.orchestration.config import load_config

    lines: list[str] = []
    if tiers:
        lines.append(f"[remedy.{TASK_CLASS_TIERS_CONFIG_KEY}]")
        lines += [f'{name} = "{tier}"' for name, tier in tiers.items()]
        lines.append("")
    if isinstance(evidence, str):
        section, _, leaf = PROMOTION_EVIDENCE_CONFIG_KEY.rpartition(".")
        lines.append(f"[remedy.{section}]")
        lines.append(f"{leaf} = {_toml_scalar(evidence)}")
        lines.append("")
    elif evidence:
        for name, entry in evidence.items():
            lines.append(f"[remedy.{PROMOTION_EVIDENCE_CONFIG_KEY}.{name}]")
            for field_name, value in entry.items():
                if isinstance(value, dict):
                    inner = ", ".join(
                        f"{key} = {_toml_scalar(reading)}"
                        for key, reading in value.items()
                    )
                    lines.append(f"{field_name} = {{ {inner} }}")
                else:
                    lines.append(f"{field_name} = {_toml_scalar(value)}")
            lines.append("")

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    loaded = load_config(
        project_path=toml_file,
        user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    monkeypatch.setattr(
        "packages.orchestration.config.get_config", lambda: loaded
    )


class TestPromotableRoleIsReadFromTheShippedTables:
    """The class and the role under test come from the DATA, not from a literal."""

    def test_the_promotable_role_and_class_are_derived(self):
        role, task_class, promoted = _evidence_promotable_role()
        assert ROLE_TASK_CLASSES[role] == task_class
        assert TASK_CLASS_TIERS[task_class] == TOP_TIER
        assert model_tier_rank(promoted) < model_tier_rank(TOP_TIER)
        assert is_task_class_promotion(task_class, promoted)


class TestPromotionEvidenceReachesTheTableBuilder:
    """A documented benchmark run LICENSES a cheaper tier — and nothing else does."""

    def test_a_promotion_with_evidence_is_accepted_end_to_end(
        self, monkeypatch, tmp_path
    ):
        _, task_class, promoted = _evidence_promotable_role()
        # THE DISCRIMINATOR: without this the seed tier could satisfy the
        # assertion below and the promotion would prove nothing.
        assert promoted != TASK_CLASS_TIERS[task_class]
        _configure_promotion_tables(
            monkeypatch,
            tmp_path,
            {task_class: promoted},
            {task_class: _well_formed_evidence_entry(task_class)},
        )
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            effective = resolve_effective_task_class_tiers()
        assert effective[task_class] == promoted
        assert [str(w.message) for w in caught] == []

    def test_the_same_promotion_without_evidence_is_still_refused(
        self, monkeypatch, tmp_path
    ):
        _, task_class, promoted = _evidence_promotable_role()
        _configure_promotion_tables(monkeypatch, tmp_path, {task_class: promoted})
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            effective = resolve_effective_task_class_tiers()
        # The class comes back at its SEEDED tier, and the rule name is READ.
        assert effective[task_class] == TASK_CLASS_TIERS[task_class]
        assert effective[task_class] != promoted
        messages = [str(w.message) for w in caught]
        assert any(RULE_PROMOTION_WITHOUT_EVIDENCE in m for m in messages), messages


class TestPromotionEvidenceReachesTheSeam:
    """A routed call NAMES the run that promoted it, instead of answering None."""

    def test_a_routed_call_names_what_promoted_it(self, monkeypatch, tmp_path):
        role, task_class, promoted = _evidence_promotable_role()
        entry = _well_formed_evidence_entry(task_class)
        _configure_promotion_tables(
            monkeypatch, tmp_path, {task_class: promoted}, {task_class: entry}
        )
        cfg = resolve_role_config(role)
        assert cfg.routed_call is not None
        assert cfg.routed_call["task_class"] == task_class
        assert cfg.routed_call["tier"] == promoted
        assert cfg.routed_call["reason"] == OVERRIDE_REASON
        promoted_by = cfg.routed_call["promoted_by"]
        assert promoted_by is not None
        # THE SUBSTRINGS COME FROM THE CONFIGURED EVIDENCE, never from a literal
        # reference string this suite would then own.
        assert entry["model_id"] in promoted_by
        assert entry["corpus"] in promoted_by

    def test_the_same_role_records_no_promoter_without_evidence(
        self, monkeypatch, tmp_path
    ):
        role, task_class, promoted = _evidence_promotable_role()
        _configure_promotion_tables(monkeypatch, tmp_path, {task_class: promoted})
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = resolve_role_config(role)
        assert cfg.routed_call["tier"] == TASK_CLASS_TIERS[task_class]
        assert cfg.routed_call["promoted_by"] is None


class TestUnsetPromotionEvidenceChangesNothing:
    """No evidence configured: the reader is empty and every answer is unmoved."""

    def test_an_unset_evidence_key_reads_as_an_empty_mapping(self):
        assert resolve_promotion_evidence() == {}

    def test_an_unset_evidence_key_leaves_every_routed_answer_unchanged(self):
        for role in sorted(ROLE_TASK_CLASSES):
            cfg = resolve_role_config(role)
            # route_role_call with NO evidence is exactly the pre-wiring answer.
            assert cfg.routed_call == route_role_call(role, None, TASK_CLASS_TIERS), role
            assert cfg.routed_call["promoted_by"] is None, role


class TestMalformedPromotionEvidenceIsNotACrash:
    """DECISION F110 D5 one layer on: a shape fault must not break a resolution."""

    def test_a_bare_string_where_the_table_belongs_reads_as_empty(
        self, monkeypatch, tmp_path
    ):
        bare = "not-a-table"
        _configure_promotion_tables(monkeypatch, tmp_path, {}, bare)
        from packages.orchestration.config import get_config

        # THE DISCRIMINATOR: the key really does carry the bare string, so it is
        # the READER'S GUARD that answers empty and not an absent key.
        assert get_config().get(PROMOTION_EVIDENCE_CONFIG_KEY) == bare
        assert resolve_promotion_evidence() == {}

    def test_a_bare_string_still_resolves_a_routed_call(self, monkeypatch, tmp_path):
        role, task_class, promoted = _evidence_promotable_role()
        baseline = resolve_role_config(role)
        _configure_promotion_tables(
            monkeypatch, tmp_path, {task_class: promoted}, "not-a-table"
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cfg = resolve_role_config(role)
        # Provider, model and effort are UNCHANGED — routing records, it never
        # selects, and a malformed evidence table cannot change that.
        assert cfg.provider == baseline.provider
        assert cfg.model == baseline.model
        assert cfg.effort == baseline.effort
        assert cfg.routed_call is not None
        assert cfg.routed_call["tier"] == TASK_CLASS_TIERS[task_class]
        assert cfg.routed_call["promoted_by"] is None


# ---------------------------------------------------------------------------
# F110 ACCEPTANCE — the reviewer/worker pairing asserted on a REAL fixture round
# ---------------------------------------------------------------------------
# WHY THIS IS NOT THE SAME TEST AS test_model_routing.py's. Every existing guard
# for policy hard rule 1 judges an OVERRIDE MAP through
# validate_task_class_tier_overrides. A map the validator refuses and a ROUND
# that nevertheless routes the refused table are different failures, and only
# the second reaches a provider call. So the round below is resolved through the
# PRODUCTION resolve_role_config for BOTH halves, and the tier under test is the
# one the SEAM RECORDED on cfg.routed_call — never a tier this file computed for
# itself and then asserted against its own arithmetic.


def _declared_reviewer_worker_rounds() -> list[tuple[str, str, str, str]]:
    """Return every ``(worker_role, reviewer_role, worker_class, reviewer_class)``.

    DERIVED, never spelled: :data:`REVIEWER_WORKER_CLASS_PAIRS` supplies the
    declared class pairs and :data:`ROLE_TASK_CLASSES` supplies every role that
    declares each half, so a re-seeding or a rename moves these rounds with it.
    Several roles may declare one class — the cross product is taken, because
    the rule binds the ROUND and not the pair of names.
    """
    rounds: list[tuple[str, str, str, str]] = []
    for worker_class, reviewer_class in REVIEWER_WORKER_CLASS_PAIRS:
        workers = [r for r in sorted(ROLE_TASK_CLASSES) if ROLE_TASK_CLASSES[r] == worker_class]
        reviewers = [r for r in sorted(ROLE_TASK_CLASSES) if ROLE_TASK_CLASSES[r] == reviewer_class]
        for worker_role in workers:
            for reviewer_role in reviewers:
                rounds.append((worker_role, reviewer_role, worker_class, reviewer_class))
    return rounds


#: The fixture rounds every acceptance test below is parametrized over. Built at
#: import so an emptied pair table shows up as a collection of zero rounds, which
#: the first test below then reports as a FAILURE rather than as a green run.
DECLARED_REVIEWER_WORKER_ROUNDS = _declared_reviewer_worker_rounds()

#: pytest ids that name the round rather than its index.
_ROUND_IDS = [f"{worker}-reviewed-by-{reviewer}" for worker, reviewer, _, _ in DECLARED_REVIEWER_WORKER_ROUNDS]


def _resolve_one_fixture_round(worker_role: str, reviewer_role: str):
    """Resolve BOTH halves of one round and return ``(worker, reviewer, messages)``.

    Both halves go through the production :func:`resolve_role_config`, so what is
    under test is the routing a real run would get. Warnings are RECORDED rather
    than silenced: a refusal this feature makes is carried on a warning, and a
    test that ignored them could not tell a refused table from an accepted one.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        worker = resolve_role_config(worker_role)
        reviewer = resolve_role_config(reviewer_role)
    return worker, reviewer, [str(w.message) for w in caught]


def _recorded_tier(cfg: RoleConfig) -> str:
    """Return the tier the SEAM RECORDED for *cfg*, not one recomputed here."""
    assert cfg.routed_call is not None, cfg.role
    return cfg.routed_call["tier"]


def _round_pairing_holds(worker: RoleConfig, reviewer: RoleConfig) -> bool:
    """Policy hard rule 1 over ONE resolved round, RANKED and never compared as text."""
    return model_tier_rank(_recorded_tier(reviewer)) >= model_tier_rank(_recorded_tier(worker))


class TestDeclaredReviewerWorkerRoundsAreDerived:
    """The rounds under test come from the shipped tables, and there is at least one."""

    def test_at_least_one_round_is_declared(self):
        # AN EMPTIED PAIR TABLE IS A FAILURE, not a vacuous pass: every test
        # below is parametrized over this list, so a zero-length list would
        # silently retire the whole acceptance clause.
        assert DECLARED_REVIEWER_WORKER_ROUNDS

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_both_halves_declare_the_classes_of_a_declared_pair(
        self, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        assert ROLE_TASK_CLASSES[worker_role] == worker_class
        assert ROLE_TASK_CLASSES[reviewer_role] == reviewer_class
        assert (worker_class, reviewer_class) in REVIEWER_WORKER_CLASS_PAIRS


class TestFixtureRoundEvidenceIsComplete:
    """The Acceptance line 'every call's evidence shows class, routed model, reason'."""

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_an_unconfigured_round_records_complete_evidence_on_both_halves(
        self, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        worker, reviewer, messages = _resolve_one_fixture_round(worker_role, reviewer_role)
        assert messages == [], messages
        for cfg, task_class in ((worker, worker_class), (reviewer, reviewer_class)):
            assert cfg.model, cfg.role
            assert cfg.routed_call is not None, cfg.role
            assert tuple(cfg.routed_call) == ROUTED_CALL_EVIDENCE_FIELDS, cfg.role
            assert cfg.routed_call["task_class"] == task_class, cfg.role
            assert cfg.routed_call["tier"] == TASK_CLASS_TIERS[task_class], cfg.role
            assert cfg.routed_call["reason"] is not None, cfg.role

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_the_seeded_round_pairs_correctly(
        self, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        worker, reviewer, messages = _resolve_one_fixture_round(worker_role, reviewer_role)
        assert messages == [], messages
        assert _round_pairing_holds(worker, reviewer)


class TestDocumentedRunCheapensTheWorkerHalf:
    """A benchmark run may buy a cheaper WORKER and the round still pairs correctly."""

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_an_evidenced_worker_promotion_is_routed_and_still_pairs(
        self, monkeypatch, tmp_path, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        cheapest = MODEL_TIERS[0]
        # THE DISCRIMINATOR: without a real move the assertions below would be
        # satisfied by the seed table and would prove nothing about promotion.
        assert model_tier_rank(cheapest) < model_tier_rank(TASK_CLASS_TIERS[worker_class])
        _configure_promotion_tables(
            monkeypatch,
            tmp_path,
            {worker_class: cheapest},
            {worker_class: _well_formed_evidence_entry(worker_class)},
        )
        worker, reviewer, messages = _resolve_one_fixture_round(worker_role, reviewer_role)
        assert messages == [], messages
        assert _recorded_tier(worker) == cheapest
        assert worker.routed_call["reason"] == OVERRIDE_REASON
        assert worker.routed_call["promoted_by"]
        assert _round_pairing_holds(worker, reviewer)


class TestDemotingTheReviewerHalfIsRefusedByName:
    """Policy hard rule 1 over a ROUND, and evidence does NOT discharge it."""

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_an_unevidenced_reviewer_demotion_is_refused_and_does_not_route(
        self, monkeypatch, tmp_path, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        cheapest = MODEL_TIERS[0]
        assert model_tier_rank(cheapest) < model_tier_rank(TASK_CLASS_TIERS[reviewer_class])
        _configure_promotion_tables(monkeypatch, tmp_path, {reviewer_class: cheapest})
        worker, reviewer, messages = _resolve_one_fixture_round(worker_role, reviewer_role)
        assert messages
        assert all(RULE_REVIEWER_WEAKER_THAN_WORKER in m for m in messages), messages
        assert _round_pairing_holds(worker, reviewer)
        # THE REFUSED TABLE DID NOT ROUTE: the reviewer keeps its SEEDED tier.
        assert _recorded_tier(reviewer) == TASK_CLASS_TIERS[reviewer_class]

    @pytest.mark.parametrize(
        "worker_role,reviewer_role,worker_class,reviewer_class",
        DECLARED_REVIEWER_WORKER_ROUNDS,
        ids=_ROUND_IDS,
    )
    def test_evidence_discharges_the_promotion_rule_but_never_the_pairing_rule(
        self, monkeypatch, tmp_path, worker_role, reviewer_role, worker_class, reviewer_class
    ):
        # WITHOUT THIS CASE the whole class of test above passes while a
        # documented benchmark run is allowed to buy a WEAKER REVIEWER — which is
        # the one thing policy hard rule 1 exists to forbid. The demotion is the
        # same as the case above; only the evidence is added.
        cheapest = MODEL_TIERS[0]
        assert model_tier_rank(cheapest) < model_tier_rank(TASK_CLASS_TIERS[reviewer_class])
        _configure_promotion_tables(
            monkeypatch,
            tmp_path,
            {reviewer_class: cheapest},
            {reviewer_class: _well_formed_evidence_entry(reviewer_class)},
        )
        worker, reviewer, messages = _resolve_one_fixture_round(worker_role, reviewer_role)
        assert messages
        assert all(RULE_REVIEWER_WEAKER_THAN_WORKER in m for m in messages), messages
        # The benchmark discharged the PROMOTION rule and ONLY that one, so its
        # name is gone from every message while the hard rule's name remains.
        assert all(RULE_PROMOTION_WITHOUT_EVIDENCE not in m for m in messages), messages
        assert _round_pairing_holds(worker, reviewer)
        assert _recorded_tier(reviewer) == TASK_CLASS_TIERS[reviewer_class]
        assert reviewer.routed_call["promoted_by"] is None
