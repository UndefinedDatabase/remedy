"""F075 T003a — deterministic harness-failure injection at the loop's existing seams.

The operator addition of 2026-08-03 asks the gauntlet to inject four harness
failures and require that each one degrades to a LEDGERED failure, a retry
within budget, or an escalation — never a silent success, never a corrupted
artifact accepted downstream (T1_F075.md, Acceptance).

Injection happens ONLY through seams :func:`orchestrator_loop.run_mission`
already exposes to its callers — ``call_fn`` (the provider transport),
``dispatch`` (how a job is created) and ``update_dossier`` (the write). Nothing
here edits product code, and nothing here adds a test-only branch to a
production path: an injector is a decorator around the production callable the
runner would have passed anyway.

All four classes are driveable since F075 R3 added the ``run_mission``
exception boundary (the R2 verdict's DECISION). Two shapes:

* ``truncated_model_response`` RETURNS a payload cut mid-object, so
  ``structured_outputs.run_structured_call`` classifies it parse-class and
  re-prompts once — the retry-within-budget path.
* the other three RAISE at their seam. The loop's boundary turns the raise
  into a classified F010 post-mortem, the iteration's ledger entry and the
  honest ``iteration_failed`` terminal. That is a LEDGERED failure, which the
  criterion accepts; a run that instead reached a green terminal with the
  fault swallowed is the ``silent_success`` this exists to catch.

**Every disposition is read off what the product DID** — its terminal and
whether a post-mortem was written — never off what the injector hoped. An
injection that never fired is rejected outright (R-0179).
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.gauntlet_evaluator import (
    DISPOSITION_ESCALATED,
    DISPOSITION_LEDGERED,
    DISPOSITION_NEVER_FIRED,
    DISPOSITION_RETRIED,
    DISPOSITION_SILENT_SUCCESS,
    INJECTION_CLASSES,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_TRUNCATED_MODEL_RESPONSE,
)
from packages.orchestration.orchestrator_loop import (
    TERMINAL_ACHIEVED,
    TERMINAL_ESCALATED,
    TERMINAL_ITERATION_FAILED,
)

#: Every injection class can be driven since the R3 boundary landed.
SUPPORTED_INJECTIONS: tuple[str, ...] = INJECTION_CLASSES

#: Kept EMPTY on purpose rather than deleted: the refusal path and its test are
#: what stop a future class from being run un-injected, and an empty mapping
#: says "nothing is blocked today" where a reader will look for it.
BLOCKED_INJECTIONS: dict[str, str] = {}

#: Which seam each raise-class injection fires at — the same public
#: ``run_mission`` parameters the runner already passes.
INJECTION_SEAMS: dict[str, str] = {
    INJECTION_PROVIDER_API_ERROR_MID_MOVE: "call_fn",
    INJECTION_HARNESS_DEATH_MID_DISPATCH: "dispatch",
    INJECTION_HARNESS_DEATH_MID_WRITE: "update_dossier",
}

#: What each raise-class injection raises. Realistic wording on purpose: the
#: text is what ``failure_postmortem`` classifies from, so a message invented to
#: earn a nicer class would be gaming the gate rather than measuring it.
INJECTION_ERRORS: dict[str, tuple[type[Exception], str]] = {
    INJECTION_PROVIDER_API_ERROR_MID_MOVE: (
        ConnectionError,
        "provider API error mid-move: the model host returned HTTP 503 and "
        "closed the connection"),
    INJECTION_HARNESS_DEATH_MID_DISPATCH: (
        OSError,
        "harness death mid-dispatch: killed between the move and the dispatch"),
    INJECTION_HARNESS_DEATH_MID_WRITE: (
        OSError,
        "harness death mid-write: killed while writing the dossier"),
}

#: Which move call the fault fires on. Fixed rather than random: the gauntlet's
#: whole claim is that the same set produces the same evidence.
INJECT_ON_MOVE = 1

#: What a truncated model response looks like — a payload cut mid-object, which
#: is what a dropped connection actually leaves behind.
TRUNCATED_PAYLOAD = '{"kind": "dispatch_job", "payload": {"milestone_id": "M0'


class MissingSeamError(RuntimeError):
    """An order asks for an injection class the product cannot yet degrade.

    Raised instead of running the order un-injected: evidence that silently
    omits a declared injection is a lie by omission, and the run.json it would
    write is exactly the artifact a human trusts when flipping defaults.
    """


@dataclass(frozen=True)
class RunOutcomeFacts:
    """What the product actually did, which is the only input to a disposition.

    ``postmortems`` is the count the runner collected from the run's own
    isolated root: "a post-mortem was written" is the difference between a
    ledgered failure and a fault that vanished.
    """

    terminal: str = ""
    postmortems: int = 0

    @property
    def terminal_ok(self) -> bool:
        return self.terminal == TERMINAL_ACHIEVED


@dataclass
class InjectionRecord:
    """One injected event and what the product did with it."""

    injection_class: str
    disposition: str = ""
    detail: str = ""

    def to_json(self) -> dict[str, str]:
        return {"class": self.injection_class,
                "disposition": self.disposition,
                "detail": self.detail}


@dataclass
class TruncatedResponseInjector:
    """Truncate the FIRST attempt of one move call, then behave normally.

    The product is expected to notice: ``run_structured_call`` validates every
    response and re-prompts once on a parse-class failure. Three outcomes, all
    observable from here without asking the loop anything:

    * the truncated text was refused and the retry answered -> ``retry_within_budget``
    * the truncated text was refused and nothing recovered -> ``ledgered_failure``
    * the truncated text VALIDATED and was executed -> ``silent_success``, the
      failure this whole criterion exists to catch
    """

    inner: Callable[[str, int], str]
    on_move: int = INJECT_ON_MOVE
    moves_seen: int = 0
    injected: bool = False
    #: Attempts observed for the move the fault fired on, after the injection.
    recovery_attempts: int = 0
    record: InjectionRecord = field(
        default_factory=lambda: InjectionRecord(INJECTION_TRUNCATED_MODEL_RESPONSE))

    def __call__(self, prompt: str, attempt: int) -> str:
        if attempt == 0:
            self.moves_seen += 1
        if self.moves_seen == self.on_move and attempt == 0 and not self.injected:
            self.injected = True
            self.record.detail = (
                f"move {self.on_move} attempt 1 returned a payload cut mid-object "
                f"({len(TRUNCATED_PAYLOAD)} chars)")
            return TRUNCATED_PAYLOAD
        if self.injected and self.moves_seen == self.on_move:
            self.recovery_attempts += 1
        return self.inner(prompt, attempt)

    def settle(self, facts: RunOutcomeFacts) -> InjectionRecord:
        """Fill in the disposition once the run is over. Never guesses.

        The run's terminal is the difference between "refused and recovered"
        and "refused and stopped" — both acceptable, but not the same fact.
        """
        if not self.injected:
            # R-0179: rejected, not accepted. A declared fault that never fired
            # proves nothing about degrading it, and the run must not count.
            self.record.disposition = DISPOSITION_NEVER_FIRED
            self.record.detail = ("the injection never fired: the run made fewer "
                                  f"than {self.on_move} move calls")
            return self.record
        if self.recovery_attempts == 0:
            # The loop never asked again, so the truncated payload was accepted.
            self.record.disposition = DISPOSITION_SILENT_SUCCESS
            self.record.detail += "; accepted without a re-prompt"
            return self.record
        self.record.disposition = (DISPOSITION_RETRIED if facts.terminal_ok
                                   else DISPOSITION_LEDGERED)
        self.record.detail += (f"; refused parse-class and re-prompted "
                               f"{self.recovery_attempts}x")
        return self.record


@dataclass
class RaiseOnceInjector:
    """Raise ONCE at a seam, then behave exactly like the callable it wraps.

    The same decorator shape as the truncation injector, over the three seams
    that fail by raising. ``inner`` is the production callable the runner would
    have passed anyway, so after the fault the run continues through the real
    path rather than a stub.
    """

    injection_class: str
    inner: Callable[..., Any]
    on_call: int = INJECT_ON_MOVE
    calls_seen: int = 0
    injected: bool = False
    record: InjectionRecord = field(default_factory=lambda: InjectionRecord(""))

    def __post_init__(self) -> None:
        if not self.record.injection_class:
            self.record = InjectionRecord(self.injection_class)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls_seen += 1
        if self.calls_seen == self.on_call and not self.injected:
            self.injected = True
            error_cls, message = INJECTION_ERRORS[self.injection_class]
            seam = INJECTION_SEAMS[self.injection_class]
            self.record.detail = (f"raised at {seam} call {self.on_call}: "
                                  f"{error_cls.__name__}: {message}")
            raise error_cls(message)
        return self.inner(*args, **kwargs)

    def settle(self, facts: RunOutcomeFacts) -> InjectionRecord:
        """Read the disposition off the product's terminal and its post-mortems.

        * ``iteration_failed`` with a post-mortem written -> ``ledgered_failure``:
          the loop caught the fault, classified it and ended honestly.
        * ``escalated`` -> ``escalated``, F051's own path.
        * a GREEN terminal after the fault fired -> ``silent_success``: the run
          claimed success over a failure nothing recorded.
        * ``iteration_failed`` with NO post-mortem -> unclassified, because the
          honest terminal alone is not the whole contract.
        """
        if not self.injected:
            self.record.disposition = DISPOSITION_NEVER_FIRED
            self.record.detail = (f"the injection never fired: the run made "
                                  f"fewer than {self.on_call} calls at "
                                  f"{INJECTION_SEAMS[self.injection_class]}")
            return self.record
        if facts.terminal_ok:
            self.record.disposition = DISPOSITION_SILENT_SUCCESS
            self.record.detail += ("; the run still reached a green terminal, so "
                                   "the fault was swallowed")
            return self.record
        if facts.terminal == TERMINAL_ESCALATED:
            self.record.disposition = DISPOSITION_ESCALATED
            self.record.detail += "; escalated to a human"
            return self.record
        if facts.terminal == TERMINAL_ITERATION_FAILED and facts.postmortems:
            self.record.disposition = DISPOSITION_LEDGERED
            self.record.detail += (f"; ledgered as {TERMINAL_ITERATION_FAILED} "
                                   f"with {facts.postmortems} post-mortem(s)")
            return self.record
        self.record.disposition = "unclassified"
        self.record.detail += (f"; ended as {facts.terminal or '(none)'} with "
                               f"{facts.postmortems} post-mortem(s)")
        return self.record


def check_injections_supported(injections: tuple[str, ...] | list[str]) -> None:
    """Refuse an order whose declared injections cannot be driven honestly."""
    for name in injections:
        if name in SUPPORTED_INJECTIONS:
            continue
        if name in BLOCKED_INJECTIONS:
            raise MissingSeamError(
                f"{name} cannot be injected at {BLOCKED_INJECTIONS[name]}: "
                f"{MISSING_SEAM}")
        raise MissingSeamError(f"unknown injection class {name!r}; the four are "
                               f"{', '.join(INJECTION_CLASSES)}")


@dataclass
class InjectedSeams:
    """The three seam callables after wrapping, plus the injectors to settle."""

    call_fn: Callable[[str, int], str] | None = None
    dispatch: Callable[..., Any] | None = None
    update_dossier: Callable[..., Any] | None = None
    injectors: list[Any] = field(default_factory=list)


def build_injectors(injections: tuple[str, ...] | list[str], *,
                    call_fn: Callable[[str, int], str] | None = None,
                    dispatch: Callable[..., Any] | None = None,
                    update_dossier: Callable[..., Any] | None = None,
                    ) -> InjectedSeams:
    """Wrap the production callables for every injection an order declares.

    Every seam is checked BEFORE anything is wrapped, so a refused order never
    gets a half-built call chain. An order with no injections gets its
    callables back untouched — the decorator is never in a path it is not
    needed in.
    """
    check_injections_supported(injections)
    seams = InjectedSeams(call_fn=call_fn, dispatch=dispatch,
                          update_dossier=update_dossier)
    for name in injections:
        if name == INJECTION_TRUNCATED_MODEL_RESPONSE:
            if seams.call_fn is None:
                continue  # no provider is an honest terminal, not a thing to wrap
            injector = TruncatedResponseInjector(inner=seams.call_fn)
            seams.call_fn = injector
        elif name == INJECTION_PROVIDER_API_ERROR_MID_MOVE:
            if seams.call_fn is None:
                continue
            injector = RaiseOnceInjector(injection_class=name, inner=seams.call_fn)
            seams.call_fn = injector
        elif name == INJECTION_HARNESS_DEATH_MID_DISPATCH:
            if seams.dispatch is None:
                continue
            injector = RaiseOnceInjector(injection_class=name, inner=seams.dispatch)
            seams.dispatch = injector
        elif name == INJECTION_HARNESS_DEATH_MID_WRITE:
            if seams.update_dossier is None:
                continue
            injector = RaiseOnceInjector(injection_class=name,
                                         inner=seams.update_dossier)
            seams.update_dossier = injector
        else:  # pragma: no cover - check_injections_supported already refused
            continue
        seams.injectors.append(injector)
    return seams


def injection_json(injectors: list[Any], facts: RunOutcomeFacts) -> list[dict[str, Any]]:
    """The ``injections[]`` block of a run.json, settled against the outcome."""
    return [injector.settle(facts).to_json() for injector in injectors]
