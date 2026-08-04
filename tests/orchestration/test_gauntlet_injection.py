"""F075 — the injection driver: four faults, dispositions read off the product.

Two shapes of fault. ``truncated_model_response`` RETURNS a payload cut
mid-object and the product's parse-class path is expected to notice. The other
three RAISE at a seam, and since the R3 boundary landed the loop is expected to
turn that into a classified post-mortem, a ledger entry and the honest
``iteration_failed`` terminal.

Every disposition here is derived from what the product DID — its terminal and
whether a post-mortem exists — never from what the injector hoped. That is the
whole point: an injector that graded its own work would prove nothing.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.gauntlet_evaluator import (
    CRITERION_INJECTIONS_DEGRADED,
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
    REJECTED_DISPOSITIONS,
    evaluate_run,
)
from packages.orchestration.gauntlet_evidence import load_run
from packages.orchestration.gauntlet_injection import (
    BLOCKED_INJECTIONS,
    INJECTION_ERRORS,
    INJECTION_SEAMS,
    SUPPORTED_INJECTIONS,
    MissingSeamError,
    RaiseOnceInjector,
    RunOutcomeFacts,
    TruncatedResponseInjector,
    build_injectors,
    check_injections_supported,
    injection_json,
)
from packages.orchestration.orchestrator_loop import (
    TERMINAL_ACHIEVED,
    TERMINAL_ESCALATED,
    TERMINAL_ITERATION_FAILED,
)
from tests.orchestration.test_gauntlet_evidence import FLAWLESS_BODY, RELEASED_GATE

RAISE_CLASSES = (
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
)

LEDGERED_FACTS = RunOutcomeFacts(terminal=TERMINAL_ITERATION_FAILED, postmortems=1)
GREEN_FACTS = RunOutcomeFacts(terminal=TERMINAL_ACHIEVED)


def counting_call_fn(answers: list[str]):
    """A provider double: hands out prepared answers and records its prompts."""
    seen: list[tuple[str, int]] = []

    def _call(prompt: str, attempt: int) -> str:
        seen.append((prompt, attempt))
        return answers[min(len(seen) - 1, len(answers) - 1)]

    _call.seen = seen  # type: ignore[attr-defined]
    return _call


# ---------------------------------------------------------------------------
# truncated_model_response — the fault that RETURNS
# ---------------------------------------------------------------------------

def test_the_first_attempt_of_the_first_move_is_truncated() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    assert injector("prompt", 0).endswith('"M0')
    assert injector.injected is True
    assert injector.inner.seen == []  # type: ignore[attr-defined]


def test_the_retry_reaches_the_real_provider() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    assert injector("prompt", 1) == "real answer"
    assert injector.recovery_attempts == 1


def test_a_refused_and_recovered_injection_is_retry_within_budget() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    injector("prompt", 1)
    record = injector.settle(GREEN_FACTS)
    assert record.disposition == DISPOSITION_RETRIED
    assert "re-prompted 1x" in record.detail


def test_a_refused_but_unrecovered_injection_is_a_ledgered_failure() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    injector("prompt", 1)
    assert injector.settle(LEDGERED_FACTS).disposition == DISPOSITION_LEDGERED


def test_a_truncated_payload_the_loop_never_re_prompted_is_a_silent_success() -> None:
    """No re-prompt means the truncated text validated and was executed."""
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    record = injector.settle(GREEN_FACTS)
    assert record.disposition == DISPOSITION_SILENT_SUCCESS
    assert "accepted without a re-prompt" in record.detail


def test_only_the_named_move_is_truncated() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["a", "b"]), on_move=2)
    assert injector("p", 0) == "a"
    assert injector("p", 0).endswith('"M0')
    assert injector.moves_seen == 2


# ---------------------------------------------------------------------------
# The three faults that RAISE
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name", RAISE_CLASSES)
def test_a_raise_class_injector_raises_once_then_delegates(name: str) -> None:
    calls: list[tuple] = []

    def inner(*args, **kwargs):
        calls.append(args)
        return "real result"

    injector = RaiseOnceInjector(injection_class=name, inner=inner)
    error_cls, message = INJECTION_ERRORS[name]
    with pytest.raises(error_cls, match=message[:30]):
        injector("a", "b")
    assert calls == []
    assert injector("a", "b") == "real result"
    assert calls == [("a", "b")]


@pytest.mark.parametrize("name", RAISE_CLASSES)
def test_a_raise_class_detail_names_the_seam_it_fired_at(name: str) -> None:
    injector = RaiseOnceInjector(injection_class=name, inner=lambda *a: None)
    with pytest.raises(Exception):
        injector()
    assert INJECTION_SEAMS[name] in injector.record.detail


@pytest.mark.parametrize("name", RAISE_CLASSES)
def test_a_caught_and_classified_raise_is_a_ledgered_failure(name: str) -> None:
    """The R3 boundary's contract: honest terminal + a post-mortem written."""
    injector = RaiseOnceInjector(injection_class=name, inner=lambda *a: None)
    with pytest.raises(Exception):
        injector()
    record = injector.settle(LEDGERED_FACTS)
    assert record.disposition == DISPOSITION_LEDGERED
    assert TERMINAL_ITERATION_FAILED in record.detail


@pytest.mark.parametrize("name", RAISE_CLASSES)
def test_a_green_terminal_after_the_fault_fired_is_a_silent_success(name: str) -> None:
    """The failure this criterion exists to catch: success claimed over a fault."""
    injector = RaiseOnceInjector(injection_class=name, inner=lambda *a: None)
    with pytest.raises(Exception):
        injector()
    record = injector.settle(GREEN_FACTS)
    assert record.disposition == DISPOSITION_SILENT_SUCCESS
    assert "swallowed" in record.detail


def test_an_escalated_run_settles_as_escalated() -> None:
    injector = RaiseOnceInjector(injection_class=RAISE_CLASSES[0],
                                 inner=lambda *a: None)
    with pytest.raises(Exception):
        injector()
    record = injector.settle(RunOutcomeFacts(terminal=TERMINAL_ESCALATED))
    assert record.disposition == DISPOSITION_ESCALATED


def test_an_honest_terminal_with_no_postmortem_is_unclassified() -> None:
    """The terminal alone is not the whole contract — the record must exist."""
    injector = RaiseOnceInjector(injection_class=RAISE_CLASSES[0],
                                 inner=lambda *a: None)
    with pytest.raises(Exception):
        injector()
    record = injector.settle(RunOutcomeFacts(terminal=TERMINAL_ITERATION_FAILED))
    assert record.disposition == "unclassified"
    assert "0 post-mortem(s)" in record.detail


@pytest.mark.parametrize("name", RAISE_CLASSES)
def test_a_raise_class_injection_that_never_fired_is_rejected(name: str) -> None:
    injector = RaiseOnceInjector(injection_class=name, inner=lambda *a: None,
                                 on_call=3)
    injector()
    record = injector.settle(LEDGERED_FACTS)
    assert record.disposition == DISPOSITION_NEVER_FIRED
    assert DISPOSITION_NEVER_FIRED in REJECTED_DISPOSITIONS


# ---------------------------------------------------------------------------
# R-0179: a never-fired injection fails the run
# ---------------------------------------------------------------------------

def test_an_injection_that_never_fired_is_a_rejected_disposition() -> None:
    """R-0179: it used to settle as ledgered_failure — an ACCEPTED class — so a
    run that never exercised its declared fault could still count flawless."""
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real"]), on_move=3)
    injector("prompt", 0)
    record = injector.settle(GREEN_FACTS)
    assert record.disposition == DISPOSITION_NEVER_FIRED
    assert "never fired" in record.detail


def test_a_never_fired_injection_fails_the_run_through_the_evaluator(
        tmp_path: Path) -> None:
    """End to end: the evidence a never-fired injection writes is not flawless."""
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real"]), on_move=3)
    injector("prompt", 0)
    block = injection_json([injector], GREEN_FACTS)

    run_dir = tmp_path / "run-01"
    run_dir.mkdir()
    (run_dir / "run.json").write_text(json.dumps(dict(
        FLAWLESS_BODY, injections=block)), encoding="utf-8")
    (run_dir / "dod_result.json").write_text(json.dumps(RELEASED_GATE),
                                             encoding="utf-8")

    verdict = evaluate_run(load_run(run_dir))
    assert verdict.flawless is False
    assert verdict.criteria[CRITERION_INJECTIONS_DEGRADED] is False
    assert verdict.failures[0].injection_class == INJECTION_TRUNCATED_MODEL_RESPONSE


# ---------------------------------------------------------------------------
# Wiring the seams
# ---------------------------------------------------------------------------

def test_an_order_with_no_injections_gets_its_callables_back_untouched() -> None:
    call, dispatch, refresh = counting_call_fn(["x"]), (lambda *a: 1), (lambda *a: 2)
    seams = build_injectors([], call_fn=call, dispatch=dispatch,
                            update_dossier=refresh)
    assert (seams.call_fn, seams.dispatch, seams.update_dossier) == (
        call, dispatch, refresh)
    assert seams.injectors == []


@pytest.mark.parametrize("name,attr", [
    (INJECTION_TRUNCATED_MODEL_RESPONSE, "call_fn"),
    (INJECTION_PROVIDER_API_ERROR_MID_MOVE, "call_fn"),
    (INJECTION_HARNESS_DEATH_MID_DISPATCH, "dispatch"),
    (INJECTION_HARNESS_DEATH_MID_WRITE, "update_dossier"),
])
def test_each_class_wraps_exactly_its_own_seam(name: str, attr: str) -> None:
    originals = {"call_fn": counting_call_fn(["x"]),
                 "dispatch": (lambda *a: 1),
                 "update_dossier": (lambda *a: 2)}
    seams = build_injectors([name], **originals)
    assert getattr(seams, attr) is not originals[attr]
    for other in set(originals) - {attr}:
        assert getattr(seams, other) is originals[other]
    assert len(seams.injectors) == 1


def test_build_injectors_without_a_provider_wraps_nothing() -> None:
    """No provider is an honest terminal, not something to decorate."""
    seams = build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE], call_fn=None)
    assert seams.call_fn is None and seams.injectors == []


def test_injection_json_is_the_run_json_block() -> None:
    seams = build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE],
                            call_fn=counting_call_fn(["real"]))
    seams.injectors[0]("p", 0)
    seams.injectors[0]("p", 1)
    block = injection_json(seams.injectors, GREEN_FACTS)
    assert block[0]["class"] == INJECTION_TRUNCATED_MODEL_RESPONSE
    assert block[0]["disposition"] == DISPOSITION_RETRIED
    assert block[0]["detail"]


# ---------------------------------------------------------------------------
# The closed set, and the refusal that guards it
# ---------------------------------------------------------------------------

def test_every_class_is_supported_since_the_boundary_landed() -> None:
    assert set(SUPPORTED_INJECTIONS) == set(INJECTION_CLASSES)
    assert BLOCKED_INJECTIONS == {}


def test_an_unknown_injection_class_is_still_refused() -> None:
    """The guard stays: a class nobody can drive must never run un-injected."""
    with pytest.raises(MissingSeamError, match="unknown injection class"):
        check_injections_supported(["cosmic_ray"])


def test_build_injectors_refuses_before_wrapping_anything() -> None:
    with pytest.raises(MissingSeamError):
        build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE, "cosmic_ray"],
                        call_fn=counting_call_fn(["real"]))


def test_every_raise_class_has_a_seam_and_an_error() -> None:
    assert set(INJECTION_SEAMS) == set(RAISE_CLASSES)
    assert set(INJECTION_ERRORS) == set(RAISE_CLASSES)
