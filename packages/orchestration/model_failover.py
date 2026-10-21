"""F058 — per-role model failover chains: their parse and hard rules, the walk, the report line.

A chain is read from `model_failover.chains` and checked against the three hard rules of
`packages/orchestration/model_routing.py` and this feature's own, "core never local" (DECISION
F058 D1); the parse and the checks are pure functions of their arguments. `FailoverProvider`
wraps a role's provider and, when the provider is unavailable, tries the chain's links in order
and discloses what served the call (DECISIONs F058 D2 to D4); `create_role_provider` in
`packages/orchestration/role_provider_factory.py` decides which roles it wraps.
"""

from __future__ import annotations

import time
import warnings
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from packages.orchestration.config_keys_model_routing import (
    FAILOVER_CHAINS_CONFIG_KEY,
    FAILOVER_COOLDOWN_CONFIG_KEY,
    FAILOVER_COOLDOWN_DEFAULT_S,
)
from packages.orchestration.failure_postmortem import (
    is_provider_connection_error,
    is_provider_unavailable_error,
)
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
from packages.orchestration.provider_names import ROLE_PROVIDER_NAMES
from packages.orchestration.provider_timeouts import is_timeout_error
from packages.orchestration.rate_governor import (
    RATE_LIMIT_REASON_OVERLOADED,
    classify_rate_limit_reason,
)
from packages.orchestration.role_config import KNOWN_ROLES

# ---------------------------------------------------------------------------
# The chain vocabulary
# ---------------------------------------------------------------------------

#: The three keys a link table may carry; a link naming any other key is refused.
FAILOVER_LINK_KEYS: tuple[str, ...] = ("provider", "model", "tier")

#: Providers this feature treats as LOCAL, for the core-never-local rule below.
LOCAL_PROVIDERS: frozenset[str] = frozenset({"ollama", "pi"})

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
            # R-1288: a name no provider answers to is refused here, not when the failover fires.
            if provider not in ROLE_PROVIDER_NAMES:
                raise FailoverChainError(
                    f"model_failover.chains: {role!r} link {position} names provider {provider!r}, "
                    f"which Remedy cannot create; known providers: "
                    f"{', '.join(sorted(ROLE_PROVIDER_NAMES))}"
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


# ---------------------------------------------------------------------------
# The cooldown — the sticky window, DECISION F058 D4
# ---------------------------------------------------------------------------


def resolve_failover_cooldown_s() -> int:
    """Return the configured cooldown in whole seconds, or :data:`FAILOVER_COOLDOWN_DEFAULT_S`.

    Unset answers the default with no warning. A value that is an `int` (never a `bool`) of at
    least 0 is returned as given. Anything else gives exactly one `UserWarning` naming the fault
    and the default, and the default is returned: one mistake in `remedy.toml` never blocks a
    provider call.
    """
    from packages.orchestration.config import get_config

    value = get_config().get(FAILOVER_COOLDOWN_CONFIG_KEY)
    if value is None:
        return FAILOVER_COOLDOWN_DEFAULT_S
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    warnings.warn(
        f"{FAILOVER_COOLDOWN_CONFIG_KEY}: expected a whole number of seconds of at least 0, "
        f"got {value!r}; using {FAILOVER_COOLDOWN_DEFAULT_S}",
        stacklevel=2,
    )
    return FAILOVER_COOLDOWN_DEFAULT_S


# ---------------------------------------------------------------------------
# The walk — T002, DECISION F058 D2
# ---------------------------------------------------------------------------

# WHY: the reason string a disclosure carries, so evidence and the run report agree on one spelling.
FAILOVER_REASON_PROVIDER_UNAVAILABLE: str = "failover:provider_unavailable"


# WHY: the one gap failover owns — not a timeout, a non-zero exit, a rate limit or a parse
# failure, each already handled by a retry, the governor or the single parse retry.
def is_failover_trigger(out: Any) -> bool:
    """Return True when `out.error` is exactly the provider-unavailable gap this feature owns."""
    error = getattr(out, "error", "") or ""
    if not error:
        return False
    if getattr(out, "error_class", "") == "parse":
        return False
    if error.startswith("malformed_output:"):
        return False
    # A rate limit waits and retries (DECISION F058); an overloaded service is the outage this
    # feature owns, not a quota (operator amendment amend1014-luna-mission-fixes B.5).
    reason = classify_rate_limit_reason(error)
    if is_timeout_error(error) or (reason is not None and reason != RATE_LIMIT_REASON_OVERLOADED):
        return False
    # A claude-cli that exits non-zero carries its last stderr lines in the error since
    # amend0921: an outage read there is the gap; any other non-zero exit is not (operator
    # amendment amend1014-luna-mission-fixes B.5).
    return is_provider_unavailable_error(error) or is_provider_connection_error(error)


# WHY: one line of the disclosure's audit trail — what a link was asked, and what it answered.
@dataclass(frozen=True)
class FailoverLinkAttempt:
    """One link of a chain, tried once, and what it answered."""

    position: int
    provider: str
    model: str
    error: str

    def to_json(self) -> dict[str, Any]:
        """Return the JSON-ready shape evidence and the run report both read."""
        return {
            "position": self.position,
            "provider": self.provider,
            "model": self.model,
            "error": self.error,
        }


# WHY: one real provider call a failed-over call made, so each is booked on its own (R-1276).
@dataclass(frozen=True)
class FailoverCall:
    """A provider and model the walk really called, and its answer — `None` for the answer the
    walk returns, which the booking reads from that answer itself."""

    provider: str
    model: str
    output: Any = None


# WHY: what a failed-over call discloses — the model Remedy meant to use versus the one it did.
@dataclass(frozen=True)
class FailoverDisclosure:
    """The intended provider and model, every attempt tried, and the link that served the call —
    or none, when the chain ran out and the primary's own failure stands."""

    role: str
    intended_provider: str
    intended_model: str
    primary_error: str
    attempts: tuple[FailoverLinkAttempt, ...]
    used: FailoverLinkAttempt | None
    reason: str = FAILOVER_REASON_PROVIDER_UNAVAILABLE
    primary_skipped: bool = False

    def to_json(self) -> dict[str, Any]:
        """Return the JSON-ready shape evidence and the run report both read."""
        return {
            "reason": self.reason,
            "role": self.role,
            "intended": {"provider": self.intended_provider, "model": self.intended_model},
            "used": self.used.to_json() if self.used is not None else None,
            "primary_error": self.primary_error,
            "primary_skipped": self.primary_skipped,
            "attempts": [attempt.to_json() for attempt in self.attempts],
        }


# WHY: a stream hint or a stable prefix is duck-typed — a provider that has no such method needs none.
def _hand_hint(provider: Any, method: str, *args: Any) -> None:
    """Call ``provider.<method>(*args)`` when the provider has that method, the loop's own hint shape."""
    hint = getattr(provider, method, None)
    if callable(hint):
        hint(*args)


# WHY: a failed-over call is several real calls, and each one is booked (R-1276).
def _with_calls(out: Any, calls: list[FailoverCall]) -> Any:
    """Attach to `out` every real call behind it as `failover_calls`, when there was more than one."""
    if len(calls) > 1:
        out.failover_calls = tuple(
            FailoverCall(call.provider, call.model, None if call.output is out else call.output)
            for call in calls
        )
    return out


# WHY: the walk itself — wraps a role's provider and, on a trigger, tries each link in order
# before letting the primary's own failure stand (DECISION F058 D2).
class FailoverProvider:
    """Wrap a role's primary provider; on a failover trigger, walk its chain in order."""

    def __init__(
        self,
        primary: Any,
        *,
        role: str,
        intended_provider: str,
        intended_model: str,
        links: tuple[FailoverLink, ...],
        build_link: Callable[[FailoverLink], Any],
        cooldown_s: float = 0.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._primary = primary
        self._role = role
        self._intended_provider = intended_provider
        self._intended_model = intended_model
        self._links = links
        self._build_link = build_link
        self._cooldown_s = cooldown_s
        self._clock = clock
        # WHY: no hold exists yet, and never will unless a call below sets it (DECISION F058 D4).
        self._held_until: float = float("-inf")
        # WHY: the session guard — True for the rest of this wrapper's life once a link has
        # served a call, so a backup's session is never handed to the primary (DECISION F058 D4).
        self._resume_disabled = False
        # WHY: each link is built once and kept, so its stream directories number on (R-1278).
        self._built_links: dict[int, Any] = {}
        # WHY: the stream hint and the stable prefix the loop gave the next call; a link hears them too.
        self._stream_call: tuple[int, str] | None = None
        self._stable_prefix: Any = None

    @property
    def name(self) -> str:
        return self._primary.name

    @property
    def supports_resume(self) -> bool:
        if self._resume_disabled:
            return False
        return bool(getattr(self._primary, "supports_resume", False))

    def begin_stream_call(self, round_no: int, kind: str = "attempt") -> None:
        """Declare the next call's round and kind to the primary and to every link that call reaches (R-1278)."""
        self._stream_call = (round_no, kind)
        _hand_hint(self._primary, "begin_stream_call", round_no, kind)

    def offer_stable_prefix(self, prefix: Any) -> None:
        """Offer the next prompt's stable prefix to the primary and to every link that call reaches (R-1278)."""
        self._stable_prefix = prefix
        _hand_hint(self._primary, "offer_stable_prefix", prefix)

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            raise AttributeError(item)
        return getattr(self._primary, item)

    def _call_link(
        self,
        link: FailoverLink,
        position: int,
        method: str,
        prompt: str,
        *,
        timeout_sec: int,
        max_output_chars: int,
    ) -> tuple[Any | None, FailoverLinkAttempt]:
        """Call one link with no session (DECISION F058 D4 (3)); `None` output means build failed.

        A link is built on its first call and kept (R-1278); one that cannot be built is tried
        again on the next call that reaches it. Before it is called it hears the round, the kind
        and the stable prefix the loop gave this call.
        """
        provider = self._built_links.get(position)
        if provider is None:
            try:
                provider = self._build_link(link)
            except RuntimeError as exc:
                return None, FailoverLinkAttempt(
                    position=position,
                    provider=link.provider,
                    model=link.model,
                    error=f"provider_error: {type(exc).__name__}: {exc}",
                )
            self._built_links[position] = provider
        if self._stream_call is not None:
            _hand_hint(provider, "begin_stream_call", *self._stream_call)
        if self._stable_prefix is not None:
            _hand_hint(provider, "offer_stable_prefix", self._stable_prefix)
        link_out = getattr(provider, method)(
            prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=None
        )
        attempt = FailoverLinkAttempt(
            position=position,
            provider=link.provider,
            model=link.model,
            error=getattr(link_out, "error", "") or "",
        )
        return link_out, attempt

    def _disclosure(
        self,
        primary_error: str,
        attempts: list[FailoverLinkAttempt],
        used: FailoverLinkAttempt | None,
        *,
        primary_skipped: bool = False,
    ) -> FailoverDisclosure:
        """The one disclosure builder: the intended provider and model are always this wrapper's."""
        return FailoverDisclosure(
            role=self._role,
            intended_provider=self._intended_provider,
            intended_model=self._intended_model,
            primary_error=primary_error,
            attempts=tuple(attempts),
            used=used,
            primary_skipped=primary_skipped,
        )

    def _walk_links(
        self,
        method: str,
        prompt: str,
        attempts: list[FailoverLinkAttempt],
        calls: list[FailoverCall],
        *,
        primary_error: str,
        primary_skipped: bool,
        timeout_sec: int,
        max_output_chars: int,
    ) -> Any | None:
        """The one link loop: the first link that answers ends the walk, disclosed; None when all trigger.

        A link serves only when its answer carries no error (R-1286): a link that answers with a
        timeout, a non-zero exit, a rate limit or a stream cap ends the walk with that failure, which
        the transport retries own, and neither holds the primary down nor turns resume off. A link
        that serves outside a hold opens one; a link that serves during a hold leaves it as it is.
        Every link that was really called joins `calls` (R-1276).
        """
        for position, link in enumerate(self._links, start=1):
            link_out, attempt = self._call_link(
                link, position, method, prompt,
                timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            attempts.append(attempt)
            if link_out is not None:
                calls.append(FailoverCall(link.provider, link.model, link_out))
            if link_out is None or is_failover_trigger(link_out):
                continue
            served = not attempt.error
            if served:
                self._resume_disabled = True
                if not primary_skipped:
                    self._held_until = self._clock() + self._cooldown_s
            link_out.failover_disclosure = self._disclosure(
                primary_error, attempts, attempt if served else None, primary_skipped=primary_skipped,
            )
            return link_out
        return None

    def _run_with_failover(
        self,
        method: str,
        prompt: str,
        *,
        timeout_sec: int,
        max_output_chars: int,
        resume: str | None,
    ) -> Any:
        attempts: list[FailoverLinkAttempt] = []
        calls: list[FailoverCall] = []
        held = self._clock() < self._held_until
        if held:
            # While the primary is held down: every link first, the primary only when all trigger.
            link_out = self._walk_links(
                method, prompt, attempts, calls, primary_error="", primary_skipped=True,
                timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            if link_out is not None:
                return _with_calls(link_out, calls)
        out = getattr(self._primary, method)(
            prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume
        )
        calls.append(FailoverCall(self._intended_provider, self._intended_model, out))
        if not is_failover_trigger(out):
            if held:
                self._held_until = float("-inf")
            return _with_calls(out, calls)
        if not held:
            if resume:
                # The run's own resume fallback calls again at full content with no session
                # (DECISION F058 D4 (3)); walking the chain here would hand a backup a session
                # it never opened.
                return out
            link_out = self._walk_links(
                method, prompt, attempts, calls, primary_error=getattr(out, "error", "") or "",
                primary_skipped=False, timeout_sec=timeout_sec, max_output_chars=max_output_chars,
            )
            if link_out is not None:
                return _with_calls(link_out, calls)
        out.failover_disclosure = self._disclosure(getattr(out, "error", "") or "", attempts, None)
        return _with_calls(out, calls)

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> Any:
        return self._run_with_failover(
            "build", prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume
        )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> Any:
        return self._run_with_failover(
            "review", prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume
        )


# WHY: the one line `remedy run show` prints for a run in which a call failed over, so silence
# is never possible when a backup model served or a chain ran out (DECISION F058 D3).
def failover_report_line(run_record: Mapping[str, Any]) -> str | None:
    """Count a run record's served and ran-out failover calls and answer one report line.

    `None` when no round's builder or reviewer entry carries a `failover` mapping. Otherwise
    one plain sentence per nonzero count, served before ran-out, followed always by the last
    sentence naming the record as the full detail.
    """
    served = 0
    ran_out = 0
    for round_data in run_record.get("rounds") or []:
        for role in ("builder", "reviewer"):
            entry = round_data.get(role)
            if not isinstance(entry, Mapping):
                continue
            failover = entry.get("failover")
            if not isinstance(failover, Mapping):
                continue
            if failover.get("used"):
                served += 1
            else:
                ran_out += 1

    if served == 0 and ran_out == 0:
        return None

    sentences: list[str] = []
    if served == 1:
        sentences.append(
            "1 call was served by a backup model because its usual provider could not be reached."
        )
    elif served > 1:
        sentences.append(
            f"{served} calls were served by backup models because their usual provider could "
            f"not be reached."
        )
    if ran_out == 1:
        sentences.append("1 call found no backup model that served it.")
    elif ran_out > 1:
        sentences.append(f"{ran_out} calls found no backup model that served them.")
    sentences.append("The run's record names every model tried.")
    return "Failover: " + " ".join(sentences)
