"""F058 — per-role model failover chains: config key, parse and hard-rule validation (T001).

Citing DECISION F058 D1: a chain lives in `remedy.toml` under `model_failover.chains`, one entry
per role, each a list of links of exactly `provider`, `model` and `tier`, tried in order when the
role's provider is unavailable after the transport retries. Every link is checked against the
three hard rules of `packages/orchestration/model_routing.py` and against a fourth this feature
adds, "core never local": a link on a local provider is allowed only for a role whose class the
shipped table routes to the cheap tier. A refused chain table names every violated rule and the
link it belongs to; no role fails over on a refusal.

Remedy deliberately does not walk the chain here, and does not read `remedy.toml` for the walk —
T002 wires the walk at the provider seam, where a run actually builds its providers. This module
stays a pure function of its arguments, exactly like `packages/orchestration/model_routing.py`
whose docstring states the same discipline for the same reason: the hard-rule checks are tested
without a config file existing at all. The one place this module reads configuration is
:func:`resolve_failover_chains`, which imports `get_config` inside its own body, the idiom
`packages/orchestration/role_config.py` already established for its own table-valued keys.

Public API::

    FAILOVER_CHAINS_CONFIG_KEY: the config key carrying the chain table
    FAILOVER_LINK_KEYS: the three keys a link table may carry
    LOCAL_PROVIDERS: providers this feature treats as local
    FAILOVER_LOCAL_ROLES: roles the core-never-local rule exempts
    RULE_CORE_ROLE_ON_LOCAL_PROVIDER: this feature's own hard-rule name
    FAILOVER_RULE_NAMES: the four hard-rule names, in report order
    FailoverLink: one link of a chain
    FailoverChainViolation: one rule a link violates
    FailoverChainError: a chain table that cannot be used at all
    FailoverChainRefused: a chain table a hard rule refuses
    parse_failover_chains(raw) -> dict[str, tuple[FailoverLink, ...]]
    validate_failover_chains(chains, effective_tiers=None, safety_relevant_classes=...)
        -> tuple[FailoverChainViolation, ...]
    build_failover_chains(raw, effective_tiers=None) -> dict[str, tuple[FailoverLink, ...]]
    resolve_failover_chains() -> dict[str, tuple[FailoverLink, ...]]
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from packages.orchestration.model_routing import (
    HARD_RULE_NAMES,
    MODEL_TIERS,
    REVIEWER_WORKER_CLASS_PAIRS,
    ROLE_TASK_CLASSES,
    SAFETY_RELEVANT_CLASSES,
    TASK_CLASS_INHERITING_ROLES,
    TASK_CLASS_TIERS,
    check_orchestration_class_routed_to_top_tier,
    check_reviewer_not_weaker_than_worker,
    check_safety_relevant_class_not_below_mid_tier,
    model_tier_rank,
    resolve_task_class_tier_with_overrides,
)
from packages.orchestration.role_config import KNOWN_ROLES

# ---------------------------------------------------------------------------
# The chain vocabulary
# ---------------------------------------------------------------------------

#: The config key carrying the chain table — DECISION F058 D1. Spelled once here and shared by
#: the registry entry (packages/orchestration/config_keys_model_routing.py) and the resolver below.
FAILOVER_CHAINS_CONFIG_KEY: str = "model_failover.chains"

#: The three keys a link table may carry; a link naming any other key is refused.
FAILOVER_LINK_KEYS: tuple[str, ...] = ("provider", "model", "tier")

#: Providers this feature treats as LOCAL, for the core-never-local rule below.
LOCAL_PROVIDERS: frozenset[str] = frozenset({"ollama"})

#: The roles the core-never-local rule EXEMPTS: every role of ROLE_TASK_CLASSES whose class the
#: shipped table routes to the cheap tier — today teacher, summary and study. DERIVED, so a class
#: re-tiered to cheap exempts its role without a second edit here.
FAILOVER_LOCAL_ROLES: frozenset[str] = frozenset(
    role for role, task_class in ROLE_TASK_CLASSES.items()
    if TASK_CLASS_TIERS.get(task_class) == "cheap"
)

# ---------------------------------------------------------------------------
# The fourth hard rule — this feature's own
# ---------------------------------------------------------------------------

#: Violated when a link on a LOCAL provider belongs to a role FAILOVER_LOCAL_ROLES does not exempt.
#: "Core never local": a core role's call never degrades onto a local model it did not choose.
RULE_CORE_ROLE_ON_LOCAL_PROVIDER: str = "core_role_on_local_provider"

#: The policy's three hard rules, then this feature's own, in report order.
FAILOVER_RULE_NAMES: tuple[str, ...] = (*HARD_RULE_NAMES, RULE_CORE_ROLE_ON_LOCAL_PROVIDER)

# ---------------------------------------------------------------------------
# The chain shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FailoverLink:
    """One link of a role's failover chain: a provider, a model and the tier it declares."""

    provider: str
    model: str
    tier: str


@dataclass(frozen=True)
class FailoverChainViolation:
    """One hard rule that one link of a configured chain violates."""

    role: str
    position: int
    link: FailoverLink
    rule: str

    def describe(self) -> str:
        """Return the one-line description a refusal message and a test both read."""
        return (
            f"{self.role} link {self.position} ({self.link.provider} {self.link.model}, "
            f"tier {self.link.tier}): {self.rule}"
        )


class FailoverChainError(ValueError):
    """A `model_failover.chains` table that cannot be used at all. Every message starts the same way."""


class FailoverChainRefused(FailoverChainError):
    """A chain table that parses, but ONE OR MORE links violate a hard rule."""

    def __init__(self, violations: tuple[FailoverChainViolation, ...]) -> None:
        self.violations = violations
        super().__init__(
            "model_failover.chains: refused — " + "; ".join(v.describe() for v in violations)
        )


# ---------------------------------------------------------------------------
# Parsing — shape only, no policy
# ---------------------------------------------------------------------------


def parse_failover_chains(raw: Mapping[str, Any]) -> dict[str, tuple[FailoverLink, ...]]:
    """Return the chains `raw` describes, in the table's own order, or RAISE on a shape fault.

    `raw` is the `[remedy.model_failover.chains]` sub-table: role name to a list of link tables.
    Every refusal is a :class:`FailoverChainError` whose message starts `"model_failover.chains: "`
    and names the role and, for a link, its 1-based position. An empty list is an empty chain.
    """
    chains: dict[str, tuple[FailoverLink, ...]] = {}
    for role, entry in raw.items():
        if role not in KNOWN_ROLES:
            raise FailoverChainError(
                f"model_failover.chains: {role!r} is not a known role; known roles: "
                f"{', '.join(sorted(KNOWN_ROLES))}"
            )
        if not isinstance(entry, list):
            raise FailoverChainError(
                f"model_failover.chains: {role!r} must be a list of links, got "
                f"{type(entry).__name__}"
            )
        links: list[FailoverLink] = []
        seen_pairs: dict[tuple[str, str], int] = {}
        for position, link in enumerate(entry, start=1):
            if not isinstance(link, Mapping):
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} must be a table, got "
                    f"{type(link).__name__}"
                )
            for key in link:
                if key not in FAILOVER_LINK_KEYS:
                    raise FailoverChainError(
                        f"model_failover.chains: {role!r} link {position} has unknown key "
                        f"{key!r}; a link holds exactly {', '.join(FAILOVER_LINK_KEYS)}"
                    )
            provider = link.get("provider")
            if not isinstance(provider, str) or not provider:
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} must set provider to a "
                    f"non-empty string"
                )
            model = link.get("model")
            if not isinstance(model, str) or not model:
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} must set model to a "
                    f"non-empty string"
                )
            tier = link.get("tier")
            if tier not in MODEL_TIERS:
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} must set tier to one of "
                    f"{MODEL_TIERS!r}, got {tier!r}"
                )
            pair = (provider, model)
            earlier = seen_pairs.get(pair)
            if earlier is not None:
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} repeats link {earlier} "
                    f"({provider} {model})"
                )
            seen_pairs[pair] = position
            links.append(FailoverLink(provider=provider, model=model, tier=tier))
        chains[role] = tuple(links)
    return chains


# ---------------------------------------------------------------------------
# Hard-rule validation — policy, over an already-parsed chain map
# ---------------------------------------------------------------------------


def validate_failover_chains(
    chains: dict[str, tuple[FailoverLink, ...]],
    effective_tiers: Mapping[str, str] | None = None,
    safety_relevant_classes: frozenset[str] = SAFETY_RELEVANT_CLASSES,
) -> tuple[FailoverChainViolation, ...]:
    """Return EVERY hard-rule violation in `chains`, role in table order, then position, then rule.

    `effective_tiers` defaults to :data:`TASK_CLASS_TIERS`. A role's class is
    `ROLE_TASK_CLASSES.get(role)`; a role of `TASK_CLASS_INHERITING_ROLES` has none of its own and
    counts on the WORKER side of every pair of `REVIEWER_WORKER_CLASS_PAIRS` instead.
    """
    tiers = TASK_CLASS_TIERS if effective_tiers is None else effective_tiers
    role_order = list(chains)
    found: list[FailoverChainViolation] = []

    for role in role_order:
        role_class = ROLE_TASK_CLASSES.get(role)
        for position, link in enumerate(chains[role], start=1):
            if role_class is not None:
                rule = check_orchestration_class_routed_to_top_tier(role_class, link.tier)
                if rule is not None:
                    found.append(FailoverChainViolation(role, position, link, rule))
                rule = check_safety_relevant_class_not_below_mid_tier(
                    role_class, link.tier, safety_relevant_classes
                )
                if rule is not None:
                    found.append(FailoverChainViolation(role, position, link, rule))
            if link.provider in LOCAL_PROVIDERS and role not in FAILOVER_LOCAL_ROLES:
                found.append(
                    FailoverChainViolation(role, position, link, RULE_CORE_ROLE_ON_LOCAL_PROVIDER)
                )

    for worker_class, reviewer_class in REVIEWER_WORKER_CLASS_PAIRS:
        worker_roles = [
            role for role in role_order
            if ROLE_TASK_CLASSES.get(role) == worker_class or role in TASK_CLASS_INHERITING_ROLES
        ]
        reviewer_roles = [role for role in role_order if ROLE_TASK_CLASSES.get(role) == reviewer_class]

        worker_strongest, _ = resolve_task_class_tier_with_overrides(worker_class, tiers)
        for role in worker_roles:
            for link in chains[role]:
                if model_tier_rank(link.tier) > model_tier_rank(worker_strongest):
                    worker_strongest = link.tier
        reviewer_tier, _ = resolve_task_class_tier_with_overrides(reviewer_class, tiers)

        for role in reviewer_roles:
            for position, link in enumerate(chains[role], start=1):
                rule = check_reviewer_not_weaker_than_worker(worker_strongest, link.tier)
                if rule is not None:
                    found.append(FailoverChainViolation(role, position, link, rule))
        for role in worker_roles:
            for position, link in enumerate(chains[role], start=1):
                rule = check_reviewer_not_weaker_than_worker(link.tier, reviewer_tier)
                if rule is not None:
                    found.append(FailoverChainViolation(role, position, link, rule))

    def sort_key(v: FailoverChainViolation) -> tuple[int, int, int]:
        return (role_order.index(v.role), v.position, FAILOVER_RULE_NAMES.index(v.rule))

    return tuple(sorted(found, key=sort_key))


def build_failover_chains(
    raw: Mapping[str, Any],
    effective_tiers: Mapping[str, str] | None = None,
) -> dict[str, tuple[FailoverLink, ...]]:
    """Parse `raw` and validate it against the hard rules; raise :class:`FailoverChainRefused`
    with EVERY violation at once, else return the parsed chains."""
    chains = parse_failover_chains(raw)
    violations = validate_failover_chains(chains, effective_tiers)
    if violations:
        raise FailoverChainRefused(violations)
    return chains


# ---------------------------------------------------------------------------
# Reading the configured chains
# ---------------------------------------------------------------------------


def resolve_failover_chains() -> dict[str, tuple[FailoverLink, ...]]:
    """Return the chains this project's configuration declares, or `{}` when it declares none.

    Unset, or a value that is not a mapping, or an explicitly empty table all answer `{}` — the
    same three-way guard `packages/orchestration/role_config.py` applies to its own table-valued
    keys. A :class:`FailoverChainError` — a shape fault or a hard-rule refusal — gives exactly one
    `UserWarning` naming the fault and answers `{}`: no role fails over on a chain Remedy could not
    read or could not accept.
    """
    from packages.orchestration.config import get_config
    from packages.orchestration.role_config import resolve_effective_task_class_tiers

    value = get_config().get(FAILOVER_CHAINS_CONFIG_KEY)
    if not isinstance(value, Mapping) or not value:
        return {}
    try:
        return build_failover_chains(dict(value), resolve_effective_task_class_tiers())
    except FailoverChainError as exc:
        warnings.warn(f"{exc}; no role fails over", stacklevel=2)
        return {}
