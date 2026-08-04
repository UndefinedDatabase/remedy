"""F075 T003a — the injection driver, and the seam it is honest about missing.

Two things are proven here. First, that the one injectable class really drives
the product's own parse-class path and is classified from what the product did,
not from what the harness hoped. Second — and this is the point of the file —
that the three classes whose failure the loop cannot yet absorb are REFUSED,
loudly, instead of quietly running their orders un-injected.
"""
from __future__ import annotations

import pytest

from packages.orchestration.gauntlet_evaluator import (
    DISPOSITION_LEDGERED,
    DISPOSITION_RETRIED,
    DISPOSITION_SILENT_SUCCESS,
    INJECTION_CLASSES,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_TRUNCATED_MODEL_RESPONSE,
)
from packages.orchestration.gauntlet_injection import (
    BLOCKED_INJECTIONS,
    MISSING_SEAM,
    SUPPORTED_INJECTIONS,
    MissingSeamError,
    TruncatedResponseInjector,
    build_injectors,
    check_injections_supported,
    injection_json,
)


def counting_call_fn(answers: list[str]):
    """A provider double: hands out prepared answers and records its prompts."""
    seen: list[tuple[str, int]] = []

    def _call(prompt: str, attempt: int) -> str:
        seen.append((prompt, attempt))
        return answers[min(len(seen) - 1, len(answers) - 1)]

    _call.seen = seen  # type: ignore[attr-defined]
    return _call


# ---------------------------------------------------------------------------
# The one class that can be driven today
# ---------------------------------------------------------------------------

def test_the_first_attempt_of_the_first_move_is_truncated() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    first = injector("prompt", 0)
    assert first.endswith('"M0')
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
    record = injector.settle(terminal_ok=True)
    assert record.disposition == DISPOSITION_RETRIED
    assert "re-prompted 1x" in record.detail


def test_a_refused_but_unrecovered_injection_is_a_ledgered_failure() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    injector("prompt", 1)
    record = injector.settle(terminal_ok=False)
    assert record.disposition == DISPOSITION_LEDGERED


def test_a_truncated_payload_the_loop_never_re_prompted_is_a_silent_success() -> None:
    """No re-prompt means the truncated text validated and was executed."""
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real answer"]))
    injector("prompt", 0)
    record = injector.settle(terminal_ok=True)
    assert record.disposition == DISPOSITION_SILENT_SUCCESS
    assert "accepted without a re-prompt" in record.detail


def test_an_injection_that_never_fired_says_so_rather_than_claiming_a_pass() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["real"]), on_move=3)
    injector("prompt", 0)
    record = injector.settle(terminal_ok=True)
    assert record.disposition == DISPOSITION_LEDGERED
    assert "never fired" in record.detail


def test_only_the_named_move_is_truncated() -> None:
    injector = TruncatedResponseInjector(inner=counting_call_fn(["a", "b"]), on_move=2)
    assert injector("p", 0) == "a"
    assert injector("p", 0).endswith('"M0')
    assert injector.moves_seen == 2


def test_build_injectors_wraps_only_when_an_order_asks_for_it() -> None:
    call = counting_call_fn(["real"])
    same, none_wrapped = build_injectors([], call)
    assert same is call and none_wrapped == []

    wrapped, injectors = build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE], call)
    assert wrapped is not call
    assert len(injectors) == 1


def test_build_injectors_without_a_provider_wraps_nothing() -> None:
    """No provider is an honest terminal, not something to decorate."""
    wrapped, injectors = build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE], None)
    assert wrapped is None and injectors == []


def test_injection_json_is_the_run_json_block() -> None:
    _, injectors = build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE],
                                   counting_call_fn(["real"]))
    injectors[0]("p", 0)
    injectors[0]("p", 1)
    block = injection_json(injectors, terminal_ok=True)
    assert block == [{"class": INJECTION_TRUNCATED_MODEL_RESPONSE,
                      "disposition": DISPOSITION_RETRIED,
                      "detail": block[0]["detail"]}]
    assert block[0]["detail"]


# ---------------------------------------------------------------------------
# The seam this round could not honestly cross
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("blocked", [
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
])
def test_a_blocked_class_is_refused_and_names_its_seam(blocked: str) -> None:
    with pytest.raises(MissingSeamError) as exc:
        check_injections_supported([blocked])
    assert BLOCKED_INJECTIONS[blocked] in str(exc.value)
    assert "no exception boundary" in str(exc.value)


def test_the_blocked_and_supported_classes_together_are_the_four() -> None:
    assert set(SUPPORTED_INJECTIONS) | set(BLOCKED_INJECTIONS) == set(INJECTION_CLASSES)
    assert not set(SUPPORTED_INJECTIONS) & set(BLOCKED_INJECTIONS)


def test_the_missing_seam_names_the_function_and_the_fix() -> None:
    assert "run_mission" in MISSING_SEAM
    assert "execute_move" in MISSING_SEAM
    assert "failure_postmortem.classify" in MISSING_SEAM


def test_an_unknown_injection_class_is_refused_too() -> None:
    with pytest.raises(MissingSeamError, match="unknown injection class"):
        check_injections_supported(["cosmic_ray"])


def test_build_injectors_refuses_before_wrapping_anything() -> None:
    """A blocked order never gets a half-built call chain."""
    with pytest.raises(MissingSeamError):
        build_injectors([INJECTION_TRUNCATED_MODEL_RESPONSE,
                         INJECTION_HARNESS_DEATH_MID_WRITE],
                        counting_call_fn(["real"]))
