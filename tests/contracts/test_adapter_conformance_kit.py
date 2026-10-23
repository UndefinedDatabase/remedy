"""F151 T002: the conformance kit proved by a conforming toy and one broken toy per
dimension (DECISION F151 D2 (5))."""
from __future__ import annotations

import dataclasses

import pytest

from packages.contracts.adapter_conformance_kit import (
    CONFORMANCE_DIMENSIONS,
    AdapterSamples,
    ErrorSample,
    check_conformance_dimension,
    run_adapter_conformance,
)
from packages.contracts.adapter_contract import (
    ADAPTER_ROLES,
    AdapterCapabilities,
    AdapterUsage,
    CliInvocation,
    HttpInvocation,
)
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.stream_evidence import EVENT_RESULT
from packages.orchestration.token_actuals import UsageActuals


class _ConformingCliToy:
    """A CLI-shaped adapter conforming on every dimension."""

    @property
    def adapter_id(self) -> str:
        return "cli-toy"

    def capabilities(self, model):
        return AdapterCapabilities(
            vision=False, json_schema=True, session_resume=True,
            streaming=True, tool_use=True, max_context_tokens=100000)

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        argv = ("toy-cli", "--model", options.model, *prompt_parts)
        return CliInvocation(argv=argv)

    def map_stream(self, raw_lines):
        return tuple({"event_type": EVENT_RESULT, "line": line} for line in raw_lines)

    def map_usage(self, raw):
        if not raw:
            return None
        return AdapterUsage(
            actuals=UsageActuals(
                input_tokens=10, output_tokens=5, cache_read=0, cache_creation=0,
                total_cost_usd=0.01, num_turns=1, duration_ms=100, session_id="sess"),
            raw_counters={"raw": raw})

    def classify_error(self, error_text, exit_code):
        # FailureClass("provider_timeout") rather than the .PROVIDER_TIMEOUT attribute: the
        # transport dimension flags any attribute whose lower-cased text contains "timeout",
        # and a classifier must still be able to name the class it maps onto.
        lowered = (error_text or "").lower()
        if "not found" in lowered:
            return FailureClass.PROVIDER_UNAVAILABLE
        if "timed out" in lowered:
            return FailureClass("provider_timeout")
        if exit_code not in (None, 0):
            return FailureClass.PROVIDER_NONZERO_EXIT
        return FailureClass.UNKNOWN

    def isolation(self):
        return None


class _ConformingHttpToy:
    """An HTTP-shaped adapter conforming on every dimension; declares no streaming."""

    @property
    def adapter_id(self) -> str:
        return "http-toy"

    def capabilities(self, model):
        return AdapterCapabilities(
            vision=True, json_schema=False, session_resume=False,
            streaming=False, tool_use=False, max_context_tokens=8000)

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        body = {"model": options.model, "parts": list(prompt_parts)}
        return HttpInvocation(method="POST", url="https://toy.example/api", body=body)

    def map_stream(self, raw_lines):
        return ()

    def map_usage(self, raw):
        if not raw:
            return None
        return AdapterUsage(
            actuals=UsageActuals(
                input_tokens=2, output_tokens=2, cache_read=0, cache_creation=0,
                total_cost_usd=None, num_turns=1, duration_ms=50, session_id=""),
            raw_counters={"raw": raw})

    def classify_error(self, error_text, exit_code):
        lowered = (error_text or "").lower()
        if "unavailable" in lowered:
            return FailureClass.PROVIDER_UNAVAILABLE
        if "timed out" in lowered:
            return FailureClass("provider_timeout")
        return FailureClass.UNKNOWN

    def isolation(self):
        return None


_CLI_USAGE = AdapterUsage(
    actuals=UsageActuals(
        input_tokens=10, output_tokens=5, cache_read=0, cache_creation=0,
        total_cost_usd=0.01, num_turns=1, duration_ms=100, session_id="sess"),
    raw_counters={"raw": "usage-blob"})

_CLI_SAMPLES = AdapterSamples(
    model="toy-model",
    stream_lines=("line-1", "line-2"),
    expected_stream_events=(
        {"event_type": EVENT_RESULT, "line": "line-1"},
        {"event_type": EVENT_RESULT, "line": "line-2"},
    ),
    usage_raw="usage-blob",
    expected_usage=_CLI_USAGE,
    error_samples=(
        ErrorSample("toy-cli: not found", None, FailureClass.PROVIDER_UNAVAILABLE),
        ErrorSample("toy-cli: timed out", None, FailureClass.PROVIDER_TIMEOUT),
        ErrorSample("toy-cli: boom", 1, FailureClass.PROVIDER_NONZERO_EXIT),
    ),
)

_HTTP_SAMPLES = AdapterSamples(
    model="toy-http-model",
    stream_lines=(),
    expected_stream_events=(),
    usage_raw="",
    expected_usage=None,
    error_samples=(
        ErrorSample("provider unavailable", None, FailureClass.PROVIDER_UNAVAILABLE),
        ErrorSample("request timed out", None, FailureClass.PROVIDER_TIMEOUT),
    ),
)


def test_conforming_cli_toy_is_fully_conformant():
    assert run_adapter_conformance(_ConformingCliToy(), _CLI_SAMPLES) == ()


def test_conforming_http_toy_is_fully_conformant():
    assert run_adapter_conformance(_ConformingHttpToy(), _HTTP_SAMPLES) == ()


# -- One broken toy per dimension --------------------------------------------------


class _BrokenCapabilitiesToy(_ConformingCliToy):
    """capabilities: a non-bool flag."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), vision=1)


class _BrokenInvocationDropsPartToy(_ConformingCliToy):
    """invocation: a dropped prompt part."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        argv = ("toy-cli", "--model", options.model, *prompt_parts[:-1])
        return CliInvocation(argv=argv)


class _BrokenInvocationAcceptsPlannerToy(_ConformingCliToy):
    """invocation: a role accepted that should raise."""

    def build_invocation(self, role, prompt_parts, options):
        argv = ("toy-cli", "--model", options.model, *prompt_parts)
        return CliInvocation(argv=argv)


class _BrokenStreamNonStreamingReturnsEventsToy(_ConformingCliToy):
    """stream: a non-streaming toy that returns events."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), streaming=False)


class _BrokenStreamEventTypeOutsideSetToy(_ConformingCliToy):
    """stream: an event type outside STREAM_EVENT_TYPES."""

    def map_stream(self, raw_lines):
        return tuple({"event_type": "bogus_event", "line": line} for line in raw_lines)


class _BrokenUsageAnswersForEmptyToy(_ConformingCliToy):
    """usage: an answer for empty raw output."""

    def map_usage(self, raw):
        result = super().map_usage(raw)
        if result is not None:
            return result
        return AdapterUsage(
            actuals=UsageActuals(
                input_tokens=0, output_tokens=0, cache_read=0, cache_creation=0,
                total_cost_usd=None, num_turns=0, duration_ms=0, session_id=""),
            raw_counters={"empty": True})


class _BrokenErrorsTimeoutAsUnavailableToy(_ConformingCliToy):
    """errors: a timeout classified as unavailable."""

    def classify_error(self, error_text, exit_code):
        lowered = (error_text or "").lower()
        if "timed out" in lowered:
            return FailureClass.PROVIDER_UNAVAILABLE
        return super().classify_error(error_text, exit_code)


class _BrokenIsolationNotNoneToy(_ConformingCliToy):
    """isolation: a non-None declaration."""

    def isolation(self):
        return {"sandbox": "none"}


class _BrokenTransportLoopsOverAttemptsToy(_ConformingCliToy):
    """transport: a method that loops over attempts, naming a retry count."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        retry_count = 0
        for _attempt in range(1):
            retry_count += 1
        argv = ("toy-cli", "--model", options.model, *prompt_parts)
        return CliInvocation(argv=argv)


class _BrokenTransportNamesSubprocessToy(_ConformingCliToy):
    """transport: a method that names subprocess."""

    def classify_error(self, error_text, exit_code):
        import subprocess
        return super().classify_error(error_text, exit_code) if subprocess else FailureClass.UNKNOWN


_BROKEN_CASES = (
    ("capabilities", _BrokenCapabilitiesToy()),
    ("invocation", _BrokenInvocationDropsPartToy()),
    ("invocation", _BrokenInvocationAcceptsPlannerToy()),
    ("stream", _BrokenStreamNonStreamingReturnsEventsToy()),
    ("stream", _BrokenStreamEventTypeOutsideSetToy()),
    ("usage", _BrokenUsageAnswersForEmptyToy()),
    ("errors", _BrokenErrorsTimeoutAsUnavailableToy()),
    ("isolation", _BrokenIsolationNotNoneToy()),
    ("transport", _BrokenTransportLoopsOverAttemptsToy()),
    ("transport", _BrokenTransportNamesSubprocessToy()),
)


@pytest.mark.parametrize(
    "dimension,toy", _BROKEN_CASES,
    ids=[f"{dim}-{type(toy).__name__}" for dim, toy in _BROKEN_CASES])
def test_broken_toy_fails_exactly_its_own_dimension(dimension, toy):
    failures = run_adapter_conformance(toy, _CLI_SAMPLES)
    dims = {failure.dimension for failure in failures}
    assert dims == {dimension}, failures


def test_samples_lacking_a_timeout_sample_fail_errors_for_the_conforming_toy():
    bad_samples = dataclasses.replace(
        _CLI_SAMPLES,
        error_samples=tuple(
            s for s in _CLI_SAMPLES.error_samples if s.expected != FailureClass.PROVIDER_TIMEOUT),
    )
    failures = check_conformance_dimension(_ConformingCliToy(), bad_samples, "errors")
    assert failures
    assert all(f.dimension == "errors" for f in failures)


def test_check_conformance_dimension_raises_for_unknown_dimension():
    with pytest.raises(ValueError):
        check_conformance_dimension(_ConformingCliToy(), _CLI_SAMPLES, "bogus")


def test_conformance_dimensions_is_exactly_the_seven_in_order():
    assert CONFORMANCE_DIMENSIONS == (
        "capabilities", "invocation", "stream", "usage", "errors", "isolation", "transport")
