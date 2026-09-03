"""
Role-based runtime configuration for Remedy.

Resolves the runtime settings (provider, model, effort) for each orchestration
role. Values come from three sources, highest precedence first:

  1. CLI args      — per-invocation overrides
  2. Config file   — persisted project/user preferences
  3. Provider-aware built-in defaults

Provider-aware defaults: the default model depends on which provider is
selected. Claude providers default to Opus; Ollama keeps its own default.

THIS IS ALSO WHERE F110'S ROUTING SEAM IS WIRED, and it is wired ONCE.
:func:`resolve_role_config` calls
``packages.orchestration.model_routing.route_role_call`` and carries what that
seam recorded on the :class:`RoleConfig` it already returns, so every production
call that resolves a role's runtime configuration routes — the whole
``ROLE_CONFIG_CALL_SITES`` inventory that module declares funnels through this
one function. The dependency runs CONFIG -> POLICY and never back: model_routing
imports nothing from here, and its own docstring forbids the inverse.

THE TABLE THAT SEAM ROUTES AGAINST IS THE **EFFECTIVE** ONE, not the shipped one:
:func:`resolve_effective_task_class_tiers` reads ``model_routing.task_class_tiers``
from the configuration and lays it over the seed mapping, so a project can
re-tier a class it is allowed to re-tier. It cannot re-tier one a hard rule
protects — such a map is REFUSED, one warning names the key and every violated
rule, and the shipped table is used (DECISION F110 D5).

Remedy deliberately does NOT select a model from the routed tier here. The seam
answers a TIER, and F110 maps no tier to a MODEL ID at all — which concrete model
serves a tier is a configuration question that feature deliberately leaves open.
So the wiring changes what a call RECORDS and nothing about which model runs:
``provider``, ``model`` and ``effort`` are resolved by exactly the precedence
chain above, unchanged. A reader searching HERE for the code that turns a routed
tier into a model id will not find it, and that absence is deliberate. Configuring
the override table above does not weaken that sentence by one word: the table
moves which TIER a call records, never which model runs.

Public API::

    KNOWN_ROLES: tuple of recognised role names
    TASK_CLASS_TIERS_CONFIG_KEY: the config key carrying the override table
    RoleConfig: resolved provider/model/effort for one role
    RoleConfig.routed_call: what F110's seam recorded for this role's calls,
        or None when the role inherits its class and none was supplied
    resolve_effective_task_class_tiers() -> dict, the shipped table with the
        configured overrides laid over it, or the shipped table on refusal
    resolve_routed_call_evidence(role, originating_task_class=None)
        -> dict | None, the seam call that swallows exactly one exception
    resolve_role_config(role, cli_args=None, config_file=None,
        originating_task_class=None) -> RoleConfig
    resolve_orchestrator_model() -> str
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from dataclasses import dataclass, field

from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.model_routing import (
    TASK_CLASS_TIERS,
    OriginatingTaskClassRequired,
    OverrideRefused,
    build_effective_task_class_tiers,
    route_role_call,
)

# ---------------------------------------------------------------------------
# Defaults (provider-aware)
# ---------------------------------------------------------------------------

DEFAULT_PROVIDER = "ollama"
DEFAULT_EFFORT = "medium"

#: Which ROLE a provider's built-in default model plays. The concrete ids live
#: in packages/orchestration/model_aliases.py — the single source — so an
#: upgrade repoints one alias there instead of editing this table.
_PROVIDER_DEFAULT_MODELS: dict[str, str] = {
    "ollama": resolve_model_alias("ollama-default"),
    "claude-cli": resolve_model_alias("claude-flagship"),
    "claude": resolve_model_alias("claude-flagship"),
    "fake": resolve_model_alias("fake"),
    "fixture": resolve_model_alias("fixture"),
}

DEFAULT_MODEL = _PROVIDER_DEFAULT_MODELS[DEFAULT_PROVIDER]

#: Roles that Remedy knows how to configure.
#:
#: ``orchestrator`` (F070) is the mission loop's decision layer. It is listed
#: here so the loop's calls resolve without the unknown-role warning — and for
#: nothing else: its built-in defaults are deliberately the SAME as every other
#: role's, because raising the orchestrator to a top-tier model is a
#: CONFIGURATION act (`orchestrator.model`), not a change to the routing policy
#: in docs/agents/model_routing_policy.md.
#: ``teacher`` (F255) narrates a running mission and answers operator questions.
#: It is listed here so its calls resolve without the unknown-role warning. It is
#: read-only by construction and never influences a run, which is why it carries
#: no CLI override flags and no per-role budget limit (DECISION F255 D1 and D3).
#: ``summary`` (F108 T002) is the schema-validated generation-call role behind
#: ``generate_artifact_summary`` (packages/orchestration/artifact_summary.py). It
#: is registered here so F110 (model routing by task class) has a named target
#: for its routing table, per docs/roadmap/features/T3_F108.md's Orchestrator
#: brief. It carries no CLI override flags or per-role budget limit of its
#: own. ``summary_call_fn`` (packages/orchestration/artifact_summary.py,
#: F108 T003a) is the one production caller of ``resolve_role_config`` for
#: this role, feeding the resolved model into ``make_structured_call_fn``;
#: ``generate_artifact_summary`` itself still takes ``call_fn`` as a direct
#: parameter and never resolves through this module directly.
KNOWN_ROLES: tuple[str, ...] = (
    "builder",
    "reviewer",
    "repair",
    "design_worker",
    "test_worker",
    "final_verifier",
    "orchestrator",
    "teacher",
    "summary",
)

#: Resolvable fields on a RoleConfig, in declaration order.
_FIELDS: tuple[str, ...] = ("provider", "model", "effort")


def default_model_for_provider(provider: str) -> str:
    """Return the default model for a given provider name."""
    return _PROVIDER_DEFAULT_MODELS.get(provider, DEFAULT_MODEL)


@dataclass(frozen=True)
class RoleConfig:
    """Resolved runtime configuration for a single role."""

    role: str
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL
    effort: str = DEFAULT_EFFORT

    #: WHAT F110'S ROUTING SEAM RECORDED for a call by this role. The keys are
    #: exactly ``model_routing.ROUTED_CALL_EVIDENCE_FIELDS`` — task_class, tier,
    #: reason, promoted_by — so this module introduces no second spelling of any
    #: of them. ``None`` when the role INHERITS its task class and no originating
    #: class was supplied; see :func:`resolve_routed_call_evidence`.
    #:
    #: WHY ``compare=False``, and it is not a style choice: a frozen dataclass
    #: derives ``__hash__`` from its COMPARED fields, so an unqualified dict field
    #: makes ``hash(RoleConfig(...))`` raise ``TypeError: unhashable type:
    #: 'dict'``. Excluding it keeps RoleConfig exactly as hashable and as
    #: comparable as it has always been — two configs for one role still compare
    #: on provider, model and effort, and evidence about HOW a call was routed is
    #: not part of WHAT was resolved.
    routed_call: dict[str, str | None] | None = field(default=None, compare=False)


def _role_section(source: object, role: str) -> dict:
    """Extract the override mapping for ``role`` from a config source.

    A source may be either:
      * role-scoped and flat — ``{"provider": ..., "model": ...}``, or
      * nested by role — ``{"builder": {"provider": ...}, ...}``.

    Returns an empty dict when the source is missing or has no entry for the role.
    """
    if not isinstance(source, dict):
        return {}
    nested = source.get(role)
    if isinstance(nested, dict):
        return nested
    return source


#: THE CONFIG KEY CARRYING THE PER-PROJECT OVERRIDE TABLE, spelled ONCE in this
#: module and shared by the read and by the refusal warning. A warning naming a
#: key other than the key actually read would send an operator to the wrong line
#: of their remedy.toml; a test pins this constant against config.py's registry,
#: so the two modules cannot drift apart silently.
TASK_CLASS_TIERS_CONFIG_KEY: str = "model_routing.task_class_tiers"


# WHY A REFUSED MAP WARNS AND ROUTES SEEDED RATHER THAN RAISING — DECISION F110 D5
# (.agent/decisions.md, 2026-09-03): resolve_role_config is the function all seven
# inventoried call sites share, so letting OverrideRefused escape would turn one
# typo in remedy.toml into an outage on every provider call. The hard rules still
# WIN — the offending override does not take effect — and the operator is told
# WHICH rule refused it rather than left wondering why a setting did nothing.
def resolve_effective_task_class_tiers() -> dict[str, str]:
    """Return the task-class-to-tier table this project actually routes against.

    Reads :data:`TASK_CLASS_TIERS_CONFIG_KEY` from the configuration and lays it
    over :data:`packages.orchestration.model_routing.TASK_CLASS_TIERS` through
    :func:`packages.orchestration.model_routing.build_effective_task_class_tiers`,
    which is the ONE place an override map becomes a routing table and therefore
    the one place the hard rules can still win before anything routes.

    NOTHING CONFIGURED RETURNS THE SHIPPED TABLE UNCHANGED — the key unset, or an
    explicitly empty table — so a project with no overrides routes exactly as it
    did before this key existed. The same answer is given for a value that is not
    a mapping at all: an environment variable cannot carry a table, so a bare
    string can arrive on that path, and
    :func:`packages.orchestration.config.validate_config` already reports that
    SHAPE fault. Handing such a value to the builder would raise inside a config
    resolution, which is exactly the fault DECISION F110 D5 exists to prevent.

    A map the builder REFUSES raises
    :class:`packages.orchestration.model_routing.OverrideRefused`. That is caught,
    ONE :class:`UserWarning` is emitted naming the config key and EVERY violated
    rule it carries, and the SHIPPED table is returned. Routing seeded is the
    conservative direction: every hard rule this feature enforces protects a
    class from being routed DOWN, so the shipped table is never the cheaper
    answer.

    ``get_config`` is imported inside the body on purpose: this module has no
    module-level import of config and is itself imported early by others — the
    idiom :func:`resolve_orchestrator_model` already established here.
    """
    from packages.orchestration.config import get_config

    configured = get_config().get(TASK_CLASS_TIERS_CONFIG_KEY)
    if not isinstance(configured, Mapping) or not configured:
        return TASK_CLASS_TIERS
    try:
        return build_effective_task_class_tiers(dict(configured))
    except OverrideRefused as refused:
        warnings.warn(
            f"{TASK_CLASS_TIERS_CONFIG_KEY}: per-project model-routing overrides "
            f"REFUSED; routing against the shipped table instead. Violated "
            f"rules: "
            f"{', '.join(violation.rule_name for violation in refused.violations)}.",
            stacklevel=2,
        )
        return TASK_CLASS_TIERS


# WHY EXACTLY ONE EXCEPTION IS SWALLOWED, AND ONLY HERE: ``repair`` is the sole
# member of model_routing.TASK_CLASS_INHERITING_ROLES and also a member of
# KNOWN_ROLES, so ``resolve_role_config("repair")`` is an ordinary config
# resolution that has always worked and that the F110 wiring must not break. A
# config resolver has no ORIGINATING TASK to name, so ``None`` is that role's
# honest answer at this layer rather than a guessed class. Every DIRECT caller of
# route_role_call still gets the raise, unchanged.
def resolve_routed_call_evidence(
    role: str,
    originating_task_class: str | None = None,
) -> dict[str, str | None] | None:
    """Return what F110's routing seam RECORDS for a call by ``role``.

    Delegates to
    :func:`packages.orchestration.model_routing.route_role_call` and returns its
    mapping unchanged, so the declared class, the tier, the reason and what
    promoted it come from that ONE seam and cannot disagree with it. The table
    that seam routes against is :func:`resolve_effective_task_class_tiers`, so a
    per-project override reaches every routed call through this one argument and
    through no second path.

    Returns ``None`` when — and only when — the seam raises
    :class:`packages.orchestration.model_routing.OriginatingTaskClassRequired`:
    the role inherits its task class from the work that provoked the call, and no
    such class was supplied. NO OTHER EXCEPTION IS CAUGHT, deliberately; a broken
    routing table must surface rather than be recorded as a missing evidence line.
    """
    effective_tiers = resolve_effective_task_class_tiers()
    try:
        return route_role_call(role, originating_task_class, effective_tiers)
    except OriginatingTaskClassRequired:
        return None


def resolve_role_config(
    role: str,
    cli_args: object | None = None,
    config_file: object | None = None,
    originating_task_class: str | None = None,
) -> RoleConfig:
    """Resolve the runtime configuration for ``role``.

    Precedence (highest first): ``cli_args`` > ``config_file`` > provider-aware
    defaults.

    When the provider is resolved but no model is explicitly set, the model
    defaults to the provider-specific default (e.g. Opus for claude-cli,
    the configured local default for ollama).

    Args:
        role: The role name (see :data:`KNOWN_ROLES`).
        cli_args: Optional per-invocation overrides — either a flat mapping of
            ``provider``/``model``/``effort`` or a mapping keyed by role.
        config_file: Optional persisted overrides, same shape as ``cli_args``.
        originating_task_class: The task class of the work that PROVOKED this
            call. Supplied only for a role in
            ``model_routing.TASK_CLASS_INHERITING_ROLES`` — ``repair`` today —
            and ignored for every other role, which declares its own class.
            LAST AND DEFAULTED so that no existing caller has to change.

    Unknown roles emit a warning (rather than raising) and still resolve against
    the supplied overrides, falling back to the built-in defaults.

    The returned config also carries ``routed_call``, what F110's routing seam
    recorded for this role — see :func:`resolve_routed_call_evidence`. Routing is
    RECORDING and not SELECTING: provider, model and effort are resolved by the
    precedence chain above and by nothing else.
    """
    if role not in KNOWN_ROLES:
        warnings.warn(
            f"Unknown role {role!r}; using default runtime configuration. "
            f"Known roles: {', '.join(KNOWN_ROLES)}.",
            stacklevel=2,
        )

    cli = _role_section(cli_args, role)
    cfg = _role_section(config_file, role)

    resolved: dict[str, str] = {}
    for field_name in _FIELDS:
        value = cli.get(field_name)
        if value is None:
            value = cfg.get(field_name)
        if value is not None:
            resolved[field_name] = value

    # Provider-aware model default: if provider is set but model is not,
    # use the provider's default model instead of the global default.
    if "model" not in resolved:
        provider = resolved.get("provider", DEFAULT_PROVIDER)
        resolved["model"] = default_model_for_provider(provider)

    return RoleConfig(
        role=role,
        routed_call=resolve_routed_call_evidence(role, originating_task_class),
        **resolved,
    )


# The orchestrator's model must have ONE answer: `orchestrator.model` when the
# operator set it, and otherwise the same resolution every other role gets —
# which is what config.py already promises the key means, stated here in code.
def resolve_orchestrator_model() -> str:
    """Return the model id the ``orchestrator`` role should run on.

    ``orchestrator.model`` (packages/orchestration/config.py) is the ONLY
    orchestrator-specific routing surface, and its own documented promise is
    that "Unset means the role resolves exactly like every other one". So a set,
    non-empty value wins, and anything else — unset, empty, whitespace-only, or
    not a string at all — falls through to
    :func:`resolve_role_config` for the ``orchestrator`` role. Callers that need
    the orchestrator's model ask HERE rather than reading the config key
    themselves, so the key stays the operator-facing surface without also being
    a second, rival resolver.

    ``get_config`` is imported inside the body on purpose: this module has no
    module-level import of config and is itself imported early by others.
    """
    from packages.orchestration.config import get_config

    configured = get_config().get("orchestrator.model")
    if isinstance(configured, str) and configured.strip():
        return configured

    return resolve_role_config("orchestrator").model
