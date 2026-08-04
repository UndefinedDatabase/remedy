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

**Three of the four classes are not injectable yet, and this module says so
rather than pretending.** ``run_mission`` contains no ``try``/``except``: a
seam that RAISES propagates out of the loop, so the run leaves no ledger entry
for the iteration, no postmortem and no terminal — the loop cannot degrade what
it never catches. Injecting those classes today would measure the harness's own
``except``, not the product's resilience, and a gauntlet that grades its own
crutch is worse than one that admits a gap. See :data:`MISSING_SEAM` for the
exact product change that unblocks them.

Only ``truncated_model_response`` degrades under today's code: a truncated
payload RETURNS rather than raises, so ``structured_outputs.run_structured_call``
classifies it parse-class and re-prompts once — the retry-within-budget path
the criterion is asking about.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.gauntlet_evaluator import (
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

#: The injection classes that can be driven against today's product code.
SUPPORTED_INJECTIONS: tuple[str, ...] = (INJECTION_TRUNCATED_MODEL_RESPONSE,)

#: The classes whose seam exists but whose FAILURE MODE the loop cannot yet
#: absorb, mapped to the seam each one would fire at. The seam is not what is
#: missing — the boundary that turns a raised failure at that seam into a
#: classified postmortem and an honest terminal is.
BLOCKED_INJECTIONS: dict[str, str] = {
    INJECTION_PROVIDER_API_ERROR_MID_MOVE: "call_fn (the orchestrator provider call)",
    INJECTION_HARNESS_DEATH_MID_DISPATCH: "dispatch (execute_move -> continue_mission)",
    INJECTION_HARNESS_DEATH_MID_WRITE: "update_dossier (the per-iteration refresh)",
}

#: The one product change that unblocks the three. Stated here, in code, where
#: the next reader of this module will be standing when they ask why.
MISSING_SEAM = (
    "orchestrator_loop.run_mission has no exception boundary: its body contains "
    "no try/except, and execute_move wraps no try/except around dispatch. A "
    "raised provider error, a death mid-dispatch and a death mid-write all "
    "propagate out of run_mission, so the iteration leaves no ledger entry, no "
    "F010 postmortem and no honest terminal. Injecting those classes would "
    "measure the harness's own except-block instead of the product's "
    "resilience. Needed (its own reviewed change, with its own tests): a "
    "boundary in run_mission that classifies a raised failure through "
    "failure_postmortem.classify, writes the postmortem, appends the ledger "
    "entry for the iteration, and ends the run on an honest terminal or an "
    "F051 escalation."
)

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

    def settle(self, *, terminal_ok: bool) -> InjectionRecord:
        """Fill in the disposition once the run is over. Never guesses.

        ``terminal_ok`` says whether the mission reached a green terminal, which
        is the difference between "refused and recovered" and "refused and
        stopped" — both acceptable, but not the same fact.
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
        self.record.disposition = (DISPOSITION_RETRIED if terminal_ok
                                   else DISPOSITION_LEDGERED)
        self.record.detail += (f"; refused parse-class and re-prompted "
                               f"{self.recovery_attempts}x")
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


def build_injectors(injections: tuple[str, ...] | list[str],
                    call_fn: Callable[[str, int], str] | None,
                    ) -> tuple[Callable[[str, int], str] | None,
                               list[TruncatedResponseInjector]]:
    """Wrap the production ``call_fn`` for every supported injection an order declares.

    Returns the (possibly wrapped) call_fn and the injectors, which the runner
    settles after the run to learn each disposition. An order with no
    injections gets its call_fn back untouched — the decorator is never in the
    path it is not needed in.
    """
    check_injections_supported(injections)
    injectors: list[TruncatedResponseInjector] = []
    wrapped = call_fn
    for name in injections:
        if name == INJECTION_TRUNCATED_MODEL_RESPONSE and wrapped is not None:
            injector = TruncatedResponseInjector(inner=wrapped)
            injectors.append(injector)
            wrapped = injector
    return wrapped, injectors


def injection_json(injectors: list[TruncatedResponseInjector], *,
                   terminal_ok: bool) -> list[dict[str, Any]]:
    """The ``injections[]`` block of a run.json, settled against the outcome."""
    return [injector.settle(terminal_ok=terminal_ok).to_json()
            for injector in injectors]
