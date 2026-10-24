"""F151 T002: the conformance kit proved by a conforming toy and one broken case per check
(DECISION F151 D2 (5), DECISION F151 D3, R-1435 to R-1437)."""
from __future__ import annotations

import dataclasses

import pytest

from packages.contracts.adapter_conformance_kit import (
    _FORBIDDEN_MODULE_ROOTS,
    _FORBIDDEN_NAME_SUBSTRINGS,
    CONFORMANCE_DIMENSIONS,
    AdapterSamples,
    ErrorSample,
    adapter_transport_violations,
    check_conformance_dimension,
    run_adapter_conformance,
)
from packages.contracts.adapter_contract import (
    ADAPTER_ROLES,
    AdapterCapabilities,
    AdapterUsage,
    CliInvocation,
    HttpInvocation,
    InvocationOptions,
    WorkerIsolation,
    WorkerSandboxDefault,
)
from packages.orchestration import worker_isolation
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.stream_evidence import EVENT_RESULT
from packages.orchestration.token_actuals import UsageActuals

#: A valid WorkerIsolation every conforming toy below answers from isolation().
_TOY_ISOLATION = WorkerIsolation(
    method="tool_flag", adr_ref="docs/adr/0002-claude-cli-worker-isolation.md",
    tool_args=("--toy-isolated",))

#: Declares no `tool_args` at all, so the kit's new flag check (D5 (1)) has nothing to check —
#: used only by toys whose own brokenness (an empty or malformed argv) cannot also end with a
#: flag, so each broken case still fails exactly its own dimension.
_TOY_ISOLATION_NO_FLAGS = WorkerIsolation(
    method="clean_env", adr_ref="docs/adr/0002-claude-cli-worker-isolation.md",
    env_allowlist=("PATH",))

#: A valid WorkerSandboxDefault every conforming toy below answers from sandbox_default()
#: (DECISION F162 D4 (1)); its TOML text is not this file's job to parse (the kit's own tests do).
_TOY_SANDBOX_DEFAULT = WorkerSandboxDefault(
    profile_toml=(
        'fs_scope = ["{workspace}"]\n'
        'net = "deny"\n'
        'allowed_binaries = "any"\n'
        'tmp_quota_mb = "unlimited"\n'
        "[ulimits]\n"
        'cpu_s = "unlimited"\n'
        'mem_mb = "unlimited"\n'
        'nofile = "unlimited"\n'
    ),
    tool_sandbox=True,
)

#: Literal pin of the kit's forbidden name substrings (R-1437's last two survivors): a word
#: dropped from the kit's own list must turn this comparison red instead of silently dropping
#: its own parametrized test along with it.
_EXPECTED_FORBIDDEN_NAME_SUBSTRINGS = ("retry", "retries", "timeout", "sleep", "backoff")

#: Literal pin of the kit's forbidden module roots, for the same reason.
_EXPECTED_FORBIDDEN_MODULE_ROOTS = frozenset({
    "subprocess", "socket", "urllib", "http", "requests", "httpx",
    "anthropic", "ollama", "asyncio", "time",
})


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
        argv = ("toy-cli", "--model", options.model, *prompt_parts, *self.isolation().tool_args)
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
        lowered = (error_text or "").lower()
        if "not found" in lowered:
            return FailureClass.PROVIDER_UNAVAILABLE
        if "timed out" in lowered:
            return FailureClass.PROVIDER_TIMEOUT
        if exit_code not in (None, 0):
            return FailureClass.PROVIDER_NONZERO_EXIT
        return FailureClass.UNKNOWN

    def isolation(self):
        return _TOY_ISOLATION

    def sandbox_default(self):
        return _TOY_SANDBOX_DEFAULT


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
            return FailureClass.PROVIDER_TIMEOUT
        return FailureClass.UNKNOWN

    def isolation(self):
        return _TOY_ISOLATION

    def sandbox_default(self):
        return _TOY_SANDBOX_DEFAULT


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


# -- Samples derived from the CLI samples, each isolating one check -----------------

_STREAM_EVENT_TYPE_OUTSIDE_SAMPLES = dataclasses.replace(
    _CLI_SAMPLES,
    expected_stream_events=tuple(
        {"event_type": "bogus_event", "line": line} for line in _CLI_SAMPLES.stream_lines),
)

_STREAM_NO_LINES_SAMPLES = dataclasses.replace(
    _CLI_SAMPLES, stream_lines=(), expected_stream_events=())

_USAGE_DICT_SAMPLES = dataclasses.replace(
    _CLI_SAMPLES, expected_usage={"raw": _CLI_SAMPLES.usage_raw})

_USAGE_ACTUALS_DICT = AdapterUsage(
    actuals={"input_tokens": 10}, raw_counters={"raw": _CLI_SAMPLES.usage_raw})
_USAGE_ACTUALS_DICT_SAMPLES = dataclasses.replace(_CLI_SAMPLES, expected_usage=_USAGE_ACTUALS_DICT)

_USAGE_RAW_COUNTERS_EMPTY = AdapterUsage(
    actuals=UsageActuals(
        input_tokens=10, output_tokens=5, cache_read=0, cache_creation=0,
        total_cost_usd=0.01, num_turns=1, duration_ms=100, session_id="sess"),
    raw_counters={})
_USAGE_RAW_COUNTERS_EMPTY_SAMPLES = dataclasses.replace(
    _CLI_SAMPLES, expected_usage=_USAGE_RAW_COUNTERS_EMPTY)

_ERROR_SAMPLES_MISSING_UNAVAILABLE = dataclasses.replace(
    _CLI_SAMPLES,
    error_samples=tuple(
        s for s in _CLI_SAMPLES.error_samples if s.expected != FailureClass.PROVIDER_UNAVAILABLE),
)

_ERROR_SAMPLES_WITH_CONFIG = dataclasses.replace(
    _CLI_SAMPLES,
    error_samples=_CLI_SAMPLES.error_samples
    + (ErrorSample("toy-cli: config-ish problem", None, FailureClass.CONFIG),),
)


# -- One broken case per kit check --------------------------------------------------


class _BrokenCapabilitiesToy(_ConformingCliToy):
    """capabilities: a non-bool flag."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), vision=1)


class _BrokenCapabilitiesBadIdToy(_ConformingCliToy):
    """capabilities: an adapter_id outside ^[a-z][a-z0-9-]*$."""

    @property
    def adapter_id(self) -> str:
        return "Bad_ID"


class _BrokenCapabilitiesWrongTypeToy(_ConformingCliToy):
    """capabilities: capabilities() returning a dict instead of an AdapterCapabilities, on its
    first call only — a later call, which every other dimension also makes, returns a real one."""

    def __init__(self):
        self._calls = 0

    def capabilities(self, model):
        self._calls += 1
        if self._calls == 1:
            return {"vision": False}
        return super().capabilities(model)


class _BrokenCapabilitiesTokensBoolToy(_ConformingCliToy):
    """capabilities: max_context_tokens as a bool."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), max_context_tokens=True)


class _BrokenCapabilitiesTokensNegativeToy(_ConformingCliToy):
    """capabilities: max_context_tokens as a negative int."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), max_context_tokens=-1)


class _BrokenCapabilitiesUnequalToy(_ConformingCliToy):
    """capabilities: unequal on the second call (a counter on the instance)."""

    def __init__(self):
        self._calls = 0

    def capabilities(self, model):
        self._calls += 1
        vision = self._calls % 2 == 0
        return dataclasses.replace(super().capabilities(model), vision=vision)


class _BrokenInvocationDropsPartToy(_ConformingCliToy):
    """invocation: a dropped prompt part."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        argv = ("toy-cli", "--model", options.model, *prompt_parts[:-1], *self.isolation().tool_args)
        return CliInvocation(argv=argv)


class _BrokenInvocationAcceptsPlannerToy(_ConformingCliToy):
    """invocation: a role accepted that should raise."""

    def build_invocation(self, role, prompt_parts, options):
        argv = ("toy-cli", "--model", options.model, *prompt_parts, *self.isolation().tool_args)
        return CliInvocation(argv=argv)


class _BrokenInvocationUnequalToy(_ConformingCliToy):
    """invocation: build_invocation unequal on the second call (a counter on the instance)."""

    def __init__(self):
        self._calls = 0

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        self._calls += 1
        extra = ("even",) if self._calls % 2 == 0 else ()
        argv = ("toy-cli", "--model", options.model, *prompt_parts, *extra, *self.isolation().tool_args)
        return CliInvocation(argv=argv)


class _BrokenInvocationEmptyArgvToy(_ConformingCliToy):
    """invocation: an empty argv."""

    def isolation(self):
        return _TOY_ISOLATION_NO_FLAGS

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return CliInvocation(argv=())


class _BrokenInvocationEmptyFirstToy(_ConformingCliToy):
    """invocation: an argv whose first element is empty."""

    def isolation(self):
        return _TOY_ISOLATION_NO_FLAGS

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return CliInvocation(argv=("", *prompt_parts))


class _BrokenInvocationHttpMethodToy(_ConformingHttpToy):
    """invocation: an HttpInvocation with a forbidden method."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        body = {"model": options.model, "parts": list(prompt_parts)}
        return HttpInvocation(method="PUT", url="https://toy.example/api", body=body)


class _BrokenInvocationHttpUrlToy(_ConformingHttpToy):
    """invocation: an HttpInvocation whose URL is not http(s)."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        body = {"model": options.model, "parts": list(prompt_parts)}
        return HttpInvocation(method="POST", url="ftp://toy.example/api", body=body)


class _BrokenInvocationHttpBodyToy(_ConformingHttpToy):
    """invocation: an HttpInvocation whose body is a list, not a dict."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return HttpInvocation(method="POST", url="https://toy.example/api", body=list(prompt_parts))


class _BrokenInvocationWrongTypeToy(_ConformingCliToy):
    """invocation: build_invocation returning neither a CliInvocation nor an HttpInvocation."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return "not-an-invocation"


class _BrokenStreamNonStreamingReturnsEventsToy(_ConformingCliToy):
    """stream: a non-streaming toy that returns events."""

    def capabilities(self, model):
        return dataclasses.replace(super().capabilities(model), streaming=False)


class _BrokenStreamEventTypeOutsideSetToy(_ConformingCliToy):
    """stream: an event type outside STREAM_EVENT_TYPES."""

    def map_stream(self, raw_lines):
        return tuple({"event_type": "bogus_event", "line": line} for line in raw_lines)


class _BrokenStreamReturnsListToy(_ConformingCliToy):
    """stream: map_stream returning a list instead of a tuple."""

    def map_stream(self, raw_lines):
        return list(super().map_stream(raw_lines))


class _BrokenStreamEventIsStrToy(_ConformingCliToy):
    """stream: an event that is a str instead of a dict."""

    def map_stream(self, raw_lines):
        return tuple(raw_lines)


class _BrokenStreamEventsUnequalToy(_ConformingCliToy):
    """stream: events in STREAM_EVENT_TYPES but unequal to samples.expected_stream_events."""

    def map_stream(self, raw_lines):
        return tuple({"event_type": EVENT_RESULT, "line": line.upper()} for line in raw_lines)


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


class _BrokenUsageUnequalToy(_ConformingCliToy):
    """usage: a usage answer unequal to samples.expected_usage."""

    def map_usage(self, raw):
        if not raw:
            return None
        return AdapterUsage(
            actuals=UsageActuals(
                input_tokens=999, output_tokens=5, cache_read=0, cache_creation=0,
                total_cost_usd=0.01, num_turns=1, duration_ms=100, session_id="sess"),
            raw_counters={"raw": raw})


class _BrokenUsageWrongTypeToy(_ConformingCliToy):
    """usage: a usage answer that is a dict instead of an AdapterUsage."""

    def map_usage(self, raw):
        if not raw:
            return None
        return {"raw": raw}


class _BrokenUsageActualsWrongTypeToy(_ConformingCliToy):
    """usage: an AdapterUsage whose actuals is a dict instead of a UsageActuals."""

    def map_usage(self, raw):
        if not raw:
            return None
        return AdapterUsage(actuals={"input_tokens": 10}, raw_counters={"raw": raw})


class _BrokenUsageRawCountersEmptyToy(_ConformingCliToy):
    """usage: an AdapterUsage whose raw_counters is an empty dict."""

    def map_usage(self, raw):
        if not raw:
            return None
        return AdapterUsage(
            actuals=UsageActuals(
                input_tokens=10, output_tokens=5, cache_read=0, cache_creation=0,
                total_cost_usd=0.01, num_turns=1, duration_ms=100, session_id="sess"),
            raw_counters={})


class _BrokenErrorsTimeoutAsUnavailableToy(_ConformingCliToy):
    """errors: a timeout classified as unavailable."""

    def classify_error(self, error_text, exit_code):
        lowered = (error_text or "").lower()
        if "timed out" in lowered:
            return FailureClass.PROVIDER_UNAVAILABLE
        return super().classify_error(error_text, exit_code)


class _BrokenErrorsClassOutsideToy(_ConformingCliToy):
    """errors: classify_error returning a class outside ADAPTER_ERROR_CLASSES."""

    def classify_error(self, error_text, exit_code):
        lowered = (error_text or "").lower()
        if "config-ish" in lowered:
            return FailureClass.CONFIG
        return super().classify_error(error_text, exit_code)


class _BrokenIsolationNotNoneToy(_ConformingCliToy):
    """isolation: a declaration that is not a WorkerIsolation."""

    def isolation(self):
        return {"sandbox": "none"}

    def build_invocation(self, role, prompt_parts, options):
        # Not self.isolation().tool_args: isolation() answers a dict here, on purpose.
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        argv = ("toy-cli", "--model", options.model, *prompt_parts, *_TOY_ISOLATION.tool_args)
        return CliInvocation(argv=argv)


class _BrokenIsolationMissingRecordToy(_ConformingCliToy):
    """isolation (D5 (1)): an adr_ref naming a record that does not exist."""

    def isolation(self):
        return dataclasses.replace(_TOY_ISOLATION, adr_ref="docs/adr/9999-does-not-exist.md")


class _BrokenIsolationDropsFlagToy(_ConformingCliToy):
    """isolation (D5 (1)): a command line that drops its own declared flag."""

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        return CliInvocation(argv=("toy-cli", "--model", options.model, *prompt_parts))


class _BrokenSandboxNotADefaultToy(_ConformingCliToy):
    """sandbox (D4 (3)): sandbox_default() answers something other than a WorkerSandboxDefault."""

    def sandbox_default(self):
        return {"profile_toml": "x", "tool_sandbox": True}


class _BrokenSandboxUnparsableToy(_ConformingCliToy):
    """sandbox (D4 (3)): a declared profile missing the required `fs_scope` key."""

    def sandbox_default(self):
        return WorkerSandboxDefault(
            profile_toml=(
                'net = "deny"\n'
                'allowed_binaries = "any"\n'
                'tmp_quota_mb = "unlimited"\n'
                "[ulimits]\n"
                'cpu_s = "unlimited"\n'
                'mem_mb = "unlimited"\n'
                'nofile = "unlimited"\n'
            ),
            tool_sandbox=True,
        )


class _RetryingBaseToy:
    """A base class a conforming toy below inherits from; only the base holds a retry loop."""

    def _attempt_with_retry(self):
        retry_count = 0
        for _attempt in range(1):
            retry_count += 1
        return retry_count


class _BrokenTransportBaseClassRetriesToy(_RetryingBaseToy, _ConformingCliToy):
    """transport: a retry loop inherited from a base class, not the adapter's own class."""


def _toy_fetch_helper():
    """A module function beside a toy; the transport it hides is the toy's own (amend1023 D4)."""
    import time

    return time.monotonic()


class _BrokenTransportModuleFunctionToy(_ConformingCliToy):
    """transport: the class itself is clean, the module function it calls touches `time`."""

    def build_invocation(self, role, prompt_parts, options):
        _toy_fetch_helper()
        return super().build_invocation(role, prompt_parts, options)


#: transport: a class built at run time has no source Python can read; it fails, never passes.
_RuntimeBuiltToy = type("_RuntimeBuiltToy", (_ConformingCliToy,), {})


_BROKEN_CASES = (
    ("capabilities", _BrokenCapabilitiesBadIdToy(), _CLI_SAMPLES,
     "does not match ^[a-z][a-z0-9-]*$"),
    ("capabilities", _BrokenCapabilitiesWrongTypeToy(), _CLI_SAMPLES,
     "did not return an AdapterCapabilities"),
    ("capabilities", _BrokenCapabilitiesToy(), _CLI_SAMPLES, "is not a bool"),
    ("capabilities", _BrokenCapabilitiesTokensBoolToy(), _CLI_SAMPLES,
     "max_context_tokens is not an int"),
    ("capabilities", _BrokenCapabilitiesTokensNegativeToy(), _CLI_SAMPLES,
     "max_context_tokens is negative"),
    ("capabilities", _BrokenCapabilitiesUnequalToy(), _CLI_SAMPLES,
     "two calls to capabilities() with the same model were not equal"),
    ("invocation", _BrokenInvocationDropsPartToy(), _CLI_SAMPLES,
     "is missing from the carried text"),
    ("invocation", _BrokenInvocationAcceptsPlannerToy(), _CLI_SAMPLES, "did not raise ValueError"),
    ("invocation", _BrokenInvocationUnequalToy(), _CLI_SAMPLES, "is not deterministic"),
    ("invocation", _BrokenInvocationEmptyArgvToy(), _CLI_SAMPLES,
     "must be a non-empty tuple of strings"),
    ("invocation", _BrokenInvocationEmptyFirstToy(), _CLI_SAMPLES,
     "whose first element is non-empty"),
    ("invocation", _BrokenInvocationHttpMethodToy(), _HTTP_SAMPLES,
     "HttpInvocation.method must be GET or POST"),
    ("invocation", _BrokenInvocationHttpUrlToy(), _HTTP_SAMPLES,
     "HttpInvocation.url must begin http:// or https://"),
    ("invocation", _BrokenInvocationHttpBodyToy(), _HTTP_SAMPLES,
     "HttpInvocation.body must be a dict"),
    ("invocation", _BrokenInvocationWrongTypeToy(), _CLI_SAMPLES,
     "build_invocation returned neither a CliInvocation nor an HttpInvocation"),
    ("stream", _BrokenStreamNonStreamingReturnsEventsToy(), _CLI_SAMPLES,
     "map_stream must be empty when streaming is false"),
    ("stream", _BrokenStreamEventTypeOutsideSetToy(), _STREAM_EVENT_TYPE_OUTSIDE_SAMPLES,
     "is not in STREAM_EVENT_TYPES"),
    ("stream", _BrokenStreamReturnsListToy(), _CLI_SAMPLES, "map_stream did not return a tuple"),
    ("stream", _ConformingCliToy(), _STREAM_NO_LINES_SAMPLES,
     "samples.stream_lines must be non-empty when streaming is true"),
    ("stream", _BrokenStreamEventIsStrToy(), _CLI_SAMPLES, "event is not a dict"),
    ("stream", _BrokenStreamEventsUnequalToy(), _CLI_SAMPLES,
     "does not equal samples.expected_stream_events"),
    ("usage", _BrokenUsageAnswersForEmptyToy(), _CLI_SAMPLES, 'map_usage("") must be None'),
    ("usage", _BrokenUsageUnequalToy(), _CLI_SAMPLES, "does not equal samples.expected_usage"),
    ("usage", _BrokenUsageWrongTypeToy(), _USAGE_DICT_SAMPLES,
     "map_usage's non-None answer is not an AdapterUsage"),
    ("usage", _BrokenUsageActualsWrongTypeToy(), _USAGE_ACTUALS_DICT_SAMPLES,
     "AdapterUsage.actuals is not a UsageActuals"),
    ("usage", _BrokenUsageRawCountersEmptyToy(), _USAGE_RAW_COUNTERS_EMPTY_SAMPLES,
     "AdapterUsage.raw_counters must be a non-empty dict"),
    ("errors", _BrokenErrorsTimeoutAsUnavailableToy(), _CLI_SAMPLES, ", expected "),
    ("errors", _ConformingCliToy(), _ERROR_SAMPLES_MISSING_UNAVAILABLE,
     "has no expected PROVIDER_UNAVAILABLE sample"),
    ("errors", _BrokenErrorsClassOutsideToy(), _ERROR_SAMPLES_WITH_CONFIG,
     "outside ADAPTER_ERROR_CLASSES"),
    ("isolation", _BrokenIsolationNotNoneToy(), _CLI_SAMPLES,
     "isolation() must return a WorkerIsolation"),
    ("isolation", _BrokenIsolationMissingRecordToy(), _CLI_SAMPLES,
     "isolation record docs/adr/9999-does-not-exist.md is missing or has no status line"),
    ("isolation", _BrokenIsolationDropsFlagToy(), _CLI_SAMPLES,
     "the command line does not end with the declared tool_args"),
    ("sandbox", _BrokenSandboxNotADefaultToy(), _CLI_SAMPLES,
     "sandbox_default() must return a WorkerSandboxDefault"),
    ("sandbox", _BrokenSandboxUnparsableToy(), _CLI_SAMPLES,
     "sandbox default profile does not parse: sandbox profile 'cli-toy' key 'fs_scope'"),
    ("transport", _BrokenTransportBaseClassRetriesToy(), _CLI_SAMPLES, "_RetryingBaseToy:"),
    ("transport", _BrokenTransportModuleFunctionToy(), _CLI_SAMPLES,
     "_BrokenTransportModuleFunctionToy calls _toy_fetch_helper: import of 'time'"),
    ("transport", _RuntimeBuiltToy(), _CLI_SAMPLES, "_RuntimeBuiltToy: its source cannot be read"),
)


@pytest.mark.parametrize(
    "dimension,toy,samples,fragment", _BROKEN_CASES,
    ids=[f"{i}-{dim}-{type(toy).__name__}" for i, (dim, toy, _s, _f) in enumerate(_BROKEN_CASES)])
def test_broken_case_fails_exactly_its_own_check(dimension, toy, samples, fragment):
    failures = run_adapter_conformance(toy, samples)
    dims = {failure.dimension for failure in failures}
    assert dims == {dimension}, failures
    assert any(fragment in failure.detail for failure in failures), failures


def test_samples_lacking_a_timeout_sample_fail_errors_for_the_conforming_toy():
    bad_samples = dataclasses.replace(
        _CLI_SAMPLES,
        error_samples=tuple(
            s for s in _CLI_SAMPLES.error_samples if s.expected != FailureClass.PROVIDER_TIMEOUT),
    )
    failures = check_conformance_dimension(_ConformingCliToy(), bad_samples, "errors")
    assert failures
    assert all(f.dimension == "errors" for f in failures)


# -- isolation (D5 (1)): the record check and the flag check, each named after what it proves ----


def test_the_conforming_cli_toys_command_line_ends_with_its_declared_flag():
    invocation = _ConformingCliToy().build_invocation(
        "builder", ("a one-line prompt",), InvocationOptions(model="toy-model"))
    tool_args = _TOY_ISOLATION.tool_args
    assert invocation.argv[-len(tool_args):] == tool_args


def test_isolation_fails_for_a_record_with_no_status_line(tmp_path, monkeypatch):
    adr_dir = tmp_path / "docs" / "adr"
    adr_dir.mkdir(parents=True)
    (adr_dir / "0003-no-status.md").write_text("# a record with no status line\n")
    # R-1461: the kit's own record check now imports and calls `has_isolation_record`, so the
    # one `_REPO_ROOT` it resolves a path against lives in `worker_isolation`, not the kit.
    monkeypatch.setattr(worker_isolation, "_REPO_ROOT", tmp_path)

    class _NoStatusLineToy(_ConformingCliToy):
        def isolation(self):
            return dataclasses.replace(_TOY_ISOLATION, adr_ref="docs/adr/0003-no-status.md")

    failures = check_conformance_dimension(_NoStatusLineToy(), _CLI_SAMPLES, "isolation")
    assert len(failures) == 1
    assert "is missing or has no status line" in failures[0].detail


def test_isolation_skips_the_flag_check_when_the_declaration_does_not_apply():
    class _NotAppliedDropsFlagToy(_ConformingCliToy):
        def isolation(self):
            return dataclasses.replace(_TOY_ISOLATION, applies=False)

        def build_invocation(self, role, prompt_parts, options):
            if role not in ADAPTER_ROLES:
                raise ValueError(role)
            return CliInvocation(argv=("toy-cli", "--model", options.model, *prompt_parts))

    assert check_conformance_dimension(_NotAppliedDropsFlagToy(), _CLI_SAMPLES, "isolation") == ()


def test_isolation_skips_the_flag_check_for_an_http_invocation():
    assert check_conformance_dimension(_ConformingHttpToy(), _HTTP_SAMPLES, "isolation") == ()


def test_check_conformance_dimension_raises_for_unknown_dimension():
    with pytest.raises(ValueError):
        check_conformance_dimension(_ConformingCliToy(), _CLI_SAMPLES, "bogus")


def test_conformance_dimensions_is_exactly_the_eight_in_order():
    assert CONFORMANCE_DIMENSIONS == (
        "capabilities", "invocation", "stream", "usage", "errors", "isolation", "sandbox",
        "transport")


# -- the kit's forbidden-word and module-root constants, pinned to literal values --------


def test_forbidden_name_substrings_is_pinned_to_its_literal_value():
    assert _FORBIDDEN_NAME_SUBSTRINGS == _EXPECTED_FORBIDDEN_NAME_SUBSTRINGS


def test_forbidden_module_roots_is_pinned_to_its_literal_value():
    assert _FORBIDDEN_MODULE_ROOTS == _EXPECTED_FORBIDDEN_MODULE_ROOTS


# -- adapter_transport_violations: one case per forbidden word and per module root -------
# Parametrized over this file's own literal constants above, not the kit's, so that a word or
# module root dropped from the kit cannot silently drop its own test along with it (R-1437).


@pytest.mark.parametrize("word", _EXPECTED_FORBIDDEN_NAME_SUBSTRINGS)
def test_adapter_transport_violations_reports_the_word_as_an_attribute(word):
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        f"        return self.{word}_value\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"attribute .{word}_value" in v for v in violations), violations


@pytest.mark.parametrize("word", _EXPECTED_FORBIDDEN_NAME_SUBSTRINGS)
def test_adapter_transport_violations_reports_the_word_as_an_arg(word):
    source = (
        "class Toy:\n"
        f"    def method(self, {word}_value):\n"
        f"        return {word}_value\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"argument {word + '_value'!r}" in v for v in violations), violations


@pytest.mark.parametrize("word", _EXPECTED_FORBIDDEN_NAME_SUBSTRINGS)
def test_adapter_transport_violations_reports_the_word_as_a_function_name(word):
    source = (
        "class Toy:\n"
        f"    def {word}_method(self):\n"
        "        return None\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"function {word + '_method'!r}" in v for v in violations), violations


@pytest.mark.parametrize("root", sorted(_EXPECTED_FORBIDDEN_MODULE_ROOTS))
def test_adapter_transport_violations_reports_the_module_root_as_a_name(root):
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        f"        return {root}\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"use of {root!r}" in v for v in violations), violations


@pytest.mark.parametrize("root", sorted(_EXPECTED_FORBIDDEN_MODULE_ROOTS))
def test_adapter_transport_violations_reports_the_module_root_as_an_import(root):
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        f"        import {root}\n"
        "        return None\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"import of {root!r}" in v for v in violations), violations


@pytest.mark.parametrize("root", sorted(_EXPECTED_FORBIDDEN_MODULE_ROOTS))
def test_adapter_transport_violations_reports_the_module_root_as_a_from_import(root):
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        f"        from {root} import something\n"
        "        return something\n"
    )
    violations = adapter_transport_violations(source)
    assert any(f"import from {root!r}" in v for v in violations), violations


def test_adapter_transport_violations_exempts_only_the_failure_class_attribute():
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        "        return FailureClass.PROVIDER_TIMEOUT\n"
    )
    assert adapter_transport_violations(source) == []


def test_adapter_transport_violations_does_not_exempt_a_lookalike_attribute():
    source = (
        "class Toy:\n"
        "    def method(self):\n"
        "        return other.PROVIDER_TIMEOUT\n"
    )
    violations = adapter_transport_violations(source)
    assert any("attribute .PROVIDER_TIMEOUT" in v for v in violations), violations


# -- run_adapter_conformance: the two run-level properties ---------------------------


def test_run_adapter_conformance_reports_not_a_worker_adapter_for_every_dimension_in_order():
    failures = run_adapter_conformance(object(), _CLI_SAMPLES)
    assert tuple(f.dimension for f in failures) == CONFORMANCE_DIMENSIONS
    assert all("not a WorkerAdapter" in f.detail for f in failures), failures


class _BrokenCapabilitiesAndTransportToy(_ConformingCliToy):
    """capabilities and transport: both broken on the same toy, to prove ordering."""

    @property
    def adapter_id(self) -> str:
        return "Bad_ID"

    def build_invocation(self, role, prompt_parts, options):
        if role not in ADAPTER_ROLES:
            raise ValueError(role)
        retry_count = 0
        for _attempt in range(1):
            retry_count += 1
        argv = ("toy-cli", "--model", options.model, *prompt_parts)
        return CliInvocation(argv=argv)


def test_run_adapter_conformance_orders_capabilities_before_transport_for_one_toy():
    failures = run_adapter_conformance(_BrokenCapabilitiesAndTransportToy(), _CLI_SAMPLES)
    dims = [f.dimension for f in failures]
    assert "capabilities" in dims and "transport" in dims
    assert dims.index("capabilities") < dims.index("transport")
