"""F296 T001 — one task's next repair round runs on the next model tier when the evidence asks.

A task whose builder keeps failing on a cheaper tier gets its next repair round one tier up along
`MODEL_TIERS`, and its reviewer is raised with it, so it is never weaker than the builder (the first
hard rule of docs/agents/model_routing_policy.md). Four kinds of evidence trigger the step, each
counted only over the rounds the current tier served (DECISION F296 D2):

* `test_failed` — the project's tests ran red in `model_escalation.after_failures` rounds in a row;
* `review_failed` — the reviewer answered `needs_repair` or `fail` in as many rounds in a row, or
  the two kinds mixed: the last round names the reason;
* `no_progress` — two red runs in a row with one failure, which the repair loop otherwise stops on
  (`verified_repair.REASON_TEST_FAILURE_UNCHANGED`);
* `watchdog_tripped` — a red run whose execution guard enforced one of its limits, the one watchdog
  inside a task's loop.

The models each tier runs on are the operator's, read from `model_escalation.tiers`; a run whose
builder or reviewer is not one of them never escalates, because its tier is not known.

Every call an escalated provider serves carries an `EscalatedCall`: the tier the role came from and
the tier it ran on, the reason, the round the step began in, and the provider and model that served
it. The run's record of each call, its cost booking, a relaunch's session guard, the run report's
line and the job's `worker.escalated` event all read it (T002a, DECISION F296 D3). A run whose
roles both run on tier models records its tiers and its steps as `tier_ladder`, which
`packages/orchestration/tier_outcomes.py` turns into the outcome per task class and tier (T002b,
DECISION F296 D4).

Remedy deliberately does not escalate on `provider_unavailable`: an unreachable provider is F058's
failover, which keeps the tier and discloses what served the call. It never steps down, never adds a
round the run's own round and repair caps do not allow, never overrides a stop the job's budget
ordered, and does nothing unless `model_escalation.enabled` is true.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.config_keys_model_routing import (
    ESCALATION_AFTER_FAILURES_CONFIG_KEY,
    ESCALATION_AFTER_FAILURES_DEFAULT,
    ESCALATION_ENABLED_CONFIG_KEY,
    ESCALATION_TIERS_CONFIG_KEY,
)
from packages.orchestration.model_routing import MODEL_TIERS, model_tier_rank
from packages.orchestration.provider_names import ROLE_PROVIDER_NAMES
from packages.orchestration.verified_repair import REASON_TEST_FAILURE_UNCHANGED

#: The evidence that may move a task one tier up, in the order a round is read for it.
ESCALATION_TRIGGERS: tuple[str, ...] = ("watchdog_tripped", "no_progress", "test_failed", "review_failed")

#: Failure classes refused as a trigger BY NAME: an unreachable provider is F058's failover.
REFUSED_ESCALATION_TRIGGERS: frozenset[str] = frozenset({"provider_unavailable"})

#: The two keys one tier's table holds; any other key is refused.
TIER_MODEL_KEYS: tuple[str, ...] = ("provider", "model")

#: The prefix of the repair-decision reason when an escalation turns a no-progress stop into a round.
ESCALATION_REASON_PREFIX: str = "tier_escalation:"

#: A test run's tripped limit that ran no test at all, so it is no evidence about the builder (R-1343).
_LIMIT_THAT_RAN_NOTHING: str = "sandbox_unavailable"


@dataclass(frozen=True)
class TierModel:
    """The provider and model one tier runs on."""

    provider: str
    model: str


class EscalationTiersError(ValueError):
    """A `model_escalation.tiers` table that cannot be used. Every message starts the same way."""


# WHY: one tier per model, so a run's builder and reviewer each read as exactly one tier.
def parse_escalation_tiers(raw: Mapping[str, Any]) -> dict[str, TierModel]:
    """Return the tier-to-model table `raw` describes, or RAISE :class:`EscalationTiersError`.

    `raw` is the `[remedy.model_escalation.tiers]` sub-table: a tier of `MODEL_TIERS` to a table of
    exactly `provider` and `model`. A provider Remedy cannot create, an empty model, and one model
    named for two tiers are refused, the last because it would give one model two tiers.
    """
    tiers: dict[str, TierModel] = {}
    seen: dict[TierModel, str] = {}
    for tier, entry in raw.items():
        where = f"{ESCALATION_TIERS_CONFIG_KEY}: {tier!r}"
        if tier not in MODEL_TIERS:
            raise EscalationTiersError(f"{where} is not a tier; the tiers are {', '.join(MODEL_TIERS)}")
        if not isinstance(entry, Mapping):
            raise EscalationTiersError(f"{where} must be a table, got {type(entry).__name__}")
        unknown = sorted(key for key in entry if key not in TIER_MODEL_KEYS)
        if unknown:
            raise EscalationTiersError(
                f"{where} has unknown key {unknown[0]!r}; a tier holds exactly {', '.join(TIER_MODEL_KEYS)}")
        provider, model = entry.get("provider"), entry.get("model")
        if provider not in ROLE_PROVIDER_NAMES:
            raise EscalationTiersError(
                f"{where} names provider {provider!r}, which Remedy cannot create; known providers: "
                f"{', '.join(sorted(ROLE_PROVIDER_NAMES))}")
        if not isinstance(model, str) or not model:
            raise EscalationTiersError(f"{where} must set model to a non-empty string")
        pair = TierModel(provider=provider, model=model)
        if pair in seen:
            raise EscalationTiersError(f"{where} repeats the model of tier {seen[pair]!r} ({provider} {model})")
        seen[pair] = tier
        tiers[tier] = pair
    return tiers


@dataclass(frozen=True)
class EscalationPolicy:
    """What the configuration says about escalation, read once per run."""

    enabled: bool = False
    after_failures: int = ESCALATION_AFTER_FAILURES_DEFAULT
    tiers: Mapping[str, TierModel] = field(default_factory=dict)

    def tier_of(self, provider: str, model: str) -> str | None:
        """The tier whose model is `provider` `model`, or None when no tier names it."""
        return next((tier for tier, pair in self.tiers.items() if pair == TierModel(provider, model)), None)


def resolve_escalation_policy() -> EscalationPolicy:
    """Return the policy this project's configuration declares.

    Unset keys answer the defaults: off, two failing rounds, no tiers. A threshold that is not a whole
    number of at least 1, and a tiers table that cannot be used, each give exactly one `UserWarning`
    naming the fault; the threshold then answers its default and the table none, so no task escalates
    on a table Remedy could not read.
    """
    from packages.orchestration.config import get_config

    config = get_config()
    after = config.get(ESCALATION_AFTER_FAILURES_CONFIG_KEY)
    if after is None:
        after = ESCALATION_AFTER_FAILURES_DEFAULT
    elif isinstance(after, bool) or not isinstance(after, int) or after < 1:
        warnings.warn(f"{ESCALATION_AFTER_FAILURES_CONFIG_KEY}: expected a whole number of at least 1, got "
                      f"{after!r}; using {ESCALATION_AFTER_FAILURES_DEFAULT}", stacklevel=2)
        after = ESCALATION_AFTER_FAILURES_DEFAULT
    raw = config.get(ESCALATION_TIERS_CONFIG_KEY)
    tiers: dict[str, TierModel] = {}
    if isinstance(raw, Mapping) and raw:
        try:
            tiers = parse_escalation_tiers(raw)
        except EscalationTiersError as exc:
            warnings.warn(f"{exc}; no task escalates", stacklevel=2)
    return EscalationPolicy(enabled=config.get(ESCALATION_ENABLED_CONFIG_KEY) is True,
                            after_failures=after, tiers=tiers)


def next_model_tier(tier: str) -> str | None:
    """The tier one step up from `tier` along `MODEL_TIERS`, or None at the top. Never a step down."""
    rank = model_tier_rank(tier)
    return MODEL_TIERS[rank + 1] if rank + 1 < len(MODEL_TIERS) else None


def is_escalation_trigger(failure_class: str) -> bool:
    """Whether `failure_class` may move a task up a tier; `provider_unavailable` never does."""
    return failure_class not in REFUSED_ESCALATION_TRIGGERS and failure_class in ESCALATION_TRIGGERS


def round_failure_class(rd: Any) -> str | None:
    """The escalation evidence one finished round carries, or None for a round that did not fail."""
    if rd.test_passed is False:
        tripped = getattr(rd, "test_tripped_limit", "") or ""
        return "watchdog_tripped" if tripped and tripped != _LIMIT_THAT_RAN_NOTHING else "test_failed"
    verdict = getattr(getattr(rd, "reviewer_output", None), "verdict", "")
    return "review_failed" if verdict in ("needs_repair", "fail") else None


def escalation_trigger(rounds_on_tier: Sequence[Any], decision_reason: str, after_failures: int) -> str | None:
    """The trigger the rounds the current tier served give, read in `ESCALATION_TRIGGERS` order."""
    if not rounds_on_tier:
        return None
    last = round_failure_class(rounds_on_tier[-1])
    if last == "watchdog_tripped":
        return last
    if decision_reason == REASON_TEST_FAILURE_UNCHANGED and len(rounds_on_tier) >= 2:
        return "no_progress"
    recent = [round_failure_class(rd) for rd in rounds_on_tier[-after_failures:]]
    if last is not None and len(recent) == after_failures and None not in recent:
        return last
    return None


@dataclass(frozen=True)
class TierEscalation:
    """One step up: the round it serves, its reason, and each role's tier before and after."""

    round: int
    reason: str
    builder_from: str
    builder_to: str
    reviewer_from: str
    reviewer_to: str

    def to_json(self) -> dict[str, Any]:
        """The run record's entry for this step (T002b, DECISION F296 D4)."""
        return {"round": self.round, "reason": self.reason, "builder_from": self.builder_from,
                "builder_to": self.builder_to, "reviewer_from": self.reviewer_from,
                "reviewer_to": self.reviewer_to}


@dataclass(frozen=True)
class EscalatedCall:
    """What every call an escalated provider serves carries (T002a, DECISION F296 D3)."""

    escalated_from: str
    tier: str
    reason: str
    round: int
    provider: str
    model: str

    def to_json(self) -> dict[str, Any]:
        """The record's keys: the tier the role came from and ran on, why, the round it began, and who served."""
        return {"escalated_from": self.escalated_from, "tier": self.tier, "reason": self.reason,
                "round": self.round, "provider": self.provider, "model": self.model}


# WHY: the stamp rides on each answer, so the record, the booking and the event need no loop edit.
class EscalatedProvider:
    """A role's provider on an escalated tier: every answer it gives carries its `EscalatedCall`."""

    def __init__(self, inner: Any, call: EscalatedCall) -> None:
        self._inner = inner
        self.escalated_call = call

    def __getattr__(self, item: str) -> Any:
        if item.startswith("_"):
            raise AttributeError(item)
        return getattr(self._inner, item)

    def build(self, prompt: str, **kwargs: Any) -> Any:
        out = self._inner.build(prompt, **kwargs)
        out.tier_escalation = self.escalated_call
        return out

    def review(self, prompt: str, **kwargs: Any) -> Any:
        out = self._inner.review(prompt, **kwargs)
        out.tier_escalation = self.escalated_call
        return out


def escalated_call_of(out: Any) -> EscalatedCall | None:
    """The `EscalatedCall` a provider's answer carries, or None for an answer of an unescalated call."""
    call = getattr(out, "tier_escalation", None)
    return call if isinstance(call, EscalatedCall) else None


def escalation_started_in(rd: Any) -> EscalatedCall | None:
    """The builder's `EscalatedCall` of the round an escalation began in, else None."""
    call = escalated_call_of(getattr(rd, "builder_output", None))
    return call if call is not None and call.round == rd.round_number else None


#: How the run report says why a task moved up, by trigger.
ESCALATION_REASON_WORDS: dict[str, str] = {
    "watchdog_tripped": "a test run was stopped at one of its limits",
    "no_progress": "its tests failed twice with the same failure",
    "test_failed": "its tests kept failing",
    "review_failed": "its reviews kept asking for repairs",
}


def escalation_report_lines(run_record: Mapping[str, Any]) -> list[str]:
    """One line per escalation the calls of a run record carry, in round order (T002a)."""
    began: dict[int, dict[str, Mapping[str, Any]]] = {}
    for round_data in run_record.get("rounds") or []:
        for role in ("builder", "reviewer"):
            entry = (round_data.get(role) or {}).get("escalation")
            if isinstance(entry, Mapping):
                began.setdefault(int(entry.get("round") or 0), {}).setdefault(role, entry)
    lines = []
    for number in sorted(began):
        builder, reviewer = began[number].get("builder"), began[number].get("reviewer")
        if builder is None:
            continue
        why = ESCALATION_REASON_WORDS.get(str(builder.get("reason")), "the evidence asked for it")
        kept = f"the reviewer was raised to {reviewer.get('tier')} with it" if reviewer else "the reviewer kept its tier"
        lines.append(f"Escalation: from round {number} the builder ran on the {builder.get('tier')} tier instead of "
                     f"{builder.get('escalated_from')}, because {why}; {kept}.")
    return lines


# WHY: the one object a run keeps about its tiers, so `run_pingpong` calls it at two places only.
class TaskTierLadder:
    """The tiers one task's run stands on, and the escalations it took.

    Built once per run from the run's builder and reviewer names and models; `after_review` reads
    each repair decision and, when the evidence asks and the next tier can be built, prepares the
    next round's providers; `start_round` hands them to the loop once.
    """

    def __init__(self, policy: EscalationPolicy, roles: dict[str, tuple[str, str]],
                 make: Callable[..., Any], write_mode: str, options: Mapping[str, Any],
                 record: dict[str, Any] | None = None) -> None:
        self.policy = policy
        self.roles = dict(roles)
        self.tiers = {role: policy.tier_of(*pair) for role, pair in roles.items()}
        self.escalations: list[TierEscalation] = []
        self._make, self._write_mode, self._options = make, write_mode, dict(options)
        self._tier_start = 0
        self._pending: dict[str, tuple[str, str, Any]] = {}
        self._fresh: frozenset[str] = frozenset()
        # The run record's `tier_ladder`, filled only when both roles run on tier models (DECISION F296 D4).
        self._record = record if record is not None and None not in self.tiers.values() else None
        if self._record is not None:
            self._record.update(enabled=policy.enabled, builder_tier=self.tiers["builder"],
                                reviewer_tier=self.tiers["reviewer"], escalations=[])

    @classmethod
    def for_run(cls, builder_name: str, builder_model: str, reviewer_name: str, reviewer_model: str,
                make: Callable[..., Any], write_mode: str, options: Mapping[str, Any],
                result: Any = None) -> TaskTierLadder:
        roles = {"builder": (builder_name or "", builder_model or ""),
                 "reviewer": (reviewer_name or "", reviewer_model or "")}
        return cls(resolve_escalation_policy(), roles, make, write_mode, options,
                   getattr(result, "tier_ladder", None))

    @property
    def reviewer_raised(self) -> bool:
        """Whether any escalation of this run raised the reviewer."""
        return any(e.reviewer_to != e.reviewer_from for e in self.escalations)

    def resumes(self, role: str, provider: Any) -> bool:
        """Whether `role`'s provider may resume last round's session: never the round it was swapped."""
        return role not in self._fresh and bool(getattr(provider, "supports_resume", False))

    def after_review(self, decision: Any, rounds: Sequence[Any], *, rounds_left: int) -> TierEscalation | None:
        """Decide one step up after a round's repair decision; a no-progress stop becomes its round."""
        builder_tier, reviewer_tier = self.tiers["builder"], self.tiers["reviewer"]
        repairs = decision.repair_decision == "repair" or decision.reason == REASON_TEST_FAILURE_UNCHANGED
        if not (self.policy.enabled and repairs and rounds_left > 0) or builder_tier is None or reviewer_tier is None:
            return None
        reason = escalation_trigger(rounds[self._tier_start:], decision.reason, self.policy.after_failures)
        target = next_model_tier(builder_tier)
        if reason is None or not is_escalation_trigger(reason) or target is None or target not in self.policy.tiers:
            return None
        raised = target if model_tier_rank(reviewer_tier) < model_tier_rank(target) else reviewer_tier
        pending: dict[str, tuple[str, str, Any]] = {}
        try:
            for role, tier, current in (("builder", target, builder_tier), ("reviewer", raised, reviewer_tier)):
                if tier != current:
                    pair = self.policy.tiers[tier]
                    extra = {"write_mode": self._write_mode} if role == "builder" else {}
                    call = EscalatedCall(escalated_from=current, tier=tier, reason=reason,
                                         round=len(rounds) + 1, provider=pair.provider, model=pair.model)
                    built = self._make(pair.provider, role=role, model=pair.model, **extra, **self._options)
                    pending[role] = (pair.provider, pair.model, EscalatedProvider(built, call))
        except RuntimeError as exc:
            warnings.warn(f"tier escalation to {target} not taken: {exc}", stacklevel=2)
            return None
        step = TierEscalation(round=len(rounds) + 1, reason=reason, builder_from=builder_tier, builder_to=target,
                              reviewer_from=reviewer_tier, reviewer_to=raised)
        if decision.repair_decision != "repair":
            decision.repair_decision, decision.reason = "repair", ESCALATION_REASON_PREFIX + reason
        self.escalations.append(step)
        if self._record is not None:
            self._record["escalations"].append(step.to_json())
        self.tiers.update(builder=target, reviewer=raised)
        self._tier_start, self._pending = len(rounds), pending
        return step

    def start_round(self, builder_provider: Any, reviewer_provider: Any) -> tuple[Any, ...] | None:
        """The six values a round's roles run on when this round escalated, else None, once.

        In order: the builder's provider name, model and provider, then the reviewer's; a role the
        step did not raise keeps the values it had.
        """
        pending, self._pending = self._pending, {}
        self._fresh = frozenset(pending)
        if not pending:
            return None
        for role, (name, model, _) in pending.items():
            self.roles[role] = (name, model)
        builder = pending.get("builder", (*self.roles["builder"], builder_provider))
        reviewer = pending.get("reviewer", (*self.roles["reviewer"], reviewer_provider))
        return (*builder, *reviewer)
