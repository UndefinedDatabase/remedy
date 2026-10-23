"""The worker adapter conformance kit (F151 T002, DECISION F151 D2 (4)).

Every adapter's own test suite imports this and runs ``run_adapter_conformance``
against a real instance plus recorded :class:`AdapterSamples`. A dimension that
conforms returns no failures; a broken adapter fails on exactly the dimension
its break belongs to. The kit catches no exception of its own except the one
``build_invocation("planner", ...)`` is contracted to raise — an adapter that
raises anywhere else fails its caller's test loudly, by design.
"""
from __future__ import annotations

import ast
import inspect
import json
import re
import textwrap
from dataclasses import dataclass

from packages.contracts.adapter_contract import (
    ADAPTER_ERROR_CLASSES,
    ADAPTER_ROLES,
    STREAM_EVENT_TYPES,
    AdapterCapabilities,
    AdapterUsage,
    CliInvocation,
    HttpInvocation,
    InvocationOptions,
    WorkerAdapter,
)
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.token_actuals import UsageActuals

#: The seven faces a worker adapter is checked against, in the order every run checks them.
CONFORMANCE_DIMENSIONS = (
    "capabilities", "invocation", "stream", "usage", "errors", "isolation", "transport",
)

#: Three short, ASCII, quote-and-newline-free sentences every conforming invocation must carry.
CANONICAL_PROMPT_PARTS = (
    "Summarize the attached diff in one paragraph.",
    "List every file the change touches.",
    "State whether the tests still pass.",
)

_ADAPTER_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")

#: Identifier substrings an adapter class may never spell — the loop owns every one of these.
_FORBIDDEN_NAME_SUBSTRINGS = ("retry", "retries", "timeout", "sleep", "backoff")

#: Module roots an adapter class may never touch directly — transport and process/network access
#: belong to the loop's exec guard and the provider SDKs it calls, never to the adapter itself.
_FORBIDDEN_MODULE_ROOTS = frozenset({
    "subprocess", "socket", "urllib", "http", "requests", "httpx",
    "anthropic", "ollama", "asyncio", "time",
})


@dataclass(frozen=True)
class ConformanceFailure:
    """One broken promise: which dimension, and what about it failed."""

    dimension: str
    detail: str


@dataclass(frozen=True)
class ErrorSample:
    """One recorded failure text/exit-code pair and the class it must classify to."""

    error_text: str
    exit_code: int | None
    expected: FailureClass


@dataclass(frozen=True)
class AdapterSamples:
    """Recorded fixtures the kit replays against an adapter under test.

    ``error_samples`` must include at least one expected ``PROVIDER_UNAVAILABLE`` and one
    expected ``PROVIDER_TIMEOUT`` sample — the ``errors`` dimension checks for both.
    """

    model: str
    stream_lines: tuple[str, ...]
    expected_stream_events: tuple[dict, ...]
    usage_raw: str
    expected_usage: AdapterUsage | None
    error_samples: tuple[ErrorSample, ...]


def _check_capabilities(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    failures: list[ConformanceFailure] = []
    if not _ADAPTER_ID_RE.fullmatch(adapter.adapter_id):
        failures.append(ConformanceFailure(
            "capabilities", f"adapter_id {adapter.adapter_id!r} does not match ^[a-z][a-z0-9-]*$"))

    first = adapter.capabilities(samples.model)
    second = adapter.capabilities(samples.model)
    if not isinstance(first, AdapterCapabilities):
        failures.append(ConformanceFailure(
            "capabilities", f"capabilities() did not return an AdapterCapabilities: {first!r}"))
        return failures

    for flag in ("vision", "json_schema", "session_resume", "streaming", "tool_use"):
        value = getattr(first, flag)
        if not isinstance(value, bool):
            failures.append(ConformanceFailure("capabilities", f"{flag} is not a bool: {value!r}"))

    tokens = first.max_context_tokens
    if isinstance(tokens, bool) or not isinstance(tokens, int):
        failures.append(ConformanceFailure(
            "capabilities", f"max_context_tokens is not an int: {tokens!r}"))
    elif tokens < 0:
        failures.append(ConformanceFailure(
            "capabilities", f"max_context_tokens is negative: {tokens!r}"))

    if first != second:
        failures.append(ConformanceFailure(
            "capabilities", "two calls to capabilities() with the same model were not equal"))
    return failures


def _carried_text(invocation: CliInvocation | HttpInvocation) -> str:
    if isinstance(invocation, CliInvocation):
        return "\n".join(invocation.argv) + "\n" + invocation.stdin_text
    return json.dumps(invocation.body, sort_keys=True)


def _check_invocation(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    failures: list[ConformanceFailure] = []
    options = InvocationOptions(model=samples.model)

    for role in ADAPTER_ROLES:
        first = adapter.build_invocation(role, CANONICAL_PROMPT_PARTS, options)
        second = adapter.build_invocation(role, CANONICAL_PROMPT_PARTS, options)
        if first != second:
            failures.append(ConformanceFailure(
                "invocation", f"build_invocation({role!r}, ...) is not deterministic"))

        if isinstance(first, CliInvocation):
            if not first.argv or not all(isinstance(a, str) for a in first.argv) or not first.argv[0]:
                failures.append(ConformanceFailure(
                    "invocation",
                    f"{role}: CliInvocation.argv must be a non-empty tuple of strings whose "
                    f"first element is non-empty: {first.argv!r}"))
                continue
        elif isinstance(first, HttpInvocation):
            if first.method not in ("GET", "POST"):
                failures.append(ConformanceFailure(
                    "invocation", f"{role}: HttpInvocation.method must be GET or POST: {first.method!r}"))
            if not (first.url.startswith("http://") or first.url.startswith("https://")):
                failures.append(ConformanceFailure(
                    "invocation", f"{role}: HttpInvocation.url must begin http:// or https://: {first.url!r}"))
            if not isinstance(first.body, dict):
                failures.append(ConformanceFailure(
                    "invocation", f"{role}: HttpInvocation.body must be a dict: {first.body!r}"))
                continue
        else:
            failures.append(ConformanceFailure(
                "invocation",
                f"{role}: build_invocation returned neither a CliInvocation nor an "
                f"HttpInvocation: {first!r}"))
            continue

        carried = _carried_text(first)
        for part in CANONICAL_PROMPT_PARTS:
            if part not in carried:
                failures.append(ConformanceFailure(
                    "invocation", f"{role}: prompt part {part!r} is missing from the carried text"))

    try:
        adapter.build_invocation("planner", CANONICAL_PROMPT_PARTS, options)
    except ValueError:
        pass
    else:
        failures.append(ConformanceFailure(
            "invocation", "build_invocation('planner', ...) did not raise ValueError"))
    return failures


def _check_stream(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    failures: list[ConformanceFailure] = []
    caps = adapter.capabilities(samples.model)
    result = adapter.map_stream(samples.stream_lines)

    if not isinstance(result, tuple):
        failures.append(ConformanceFailure("stream", f"map_stream did not return a tuple: {result!r}"))
        return failures

    if not caps.streaming:
        if result != ():
            failures.append(ConformanceFailure(
                "stream", f"map_stream must be empty when streaming is false, got {result!r}"))
        return failures

    if not samples.stream_lines:
        failures.append(ConformanceFailure(
            "stream", "samples.stream_lines must be non-empty when streaming is true"))

    for event in result:
        if not isinstance(event, dict):
            failures.append(ConformanceFailure("stream", f"event is not a dict: {event!r}"))
            continue
        if event.get("event_type") not in STREAM_EVENT_TYPES:
            failures.append(ConformanceFailure(
                "stream", f"event_type {event.get('event_type')!r} is not in STREAM_EVENT_TYPES"))

    if result != samples.expected_stream_events:
        failures.append(ConformanceFailure(
            "stream", "map_stream(samples.stream_lines) does not equal samples.expected_stream_events"))
    return failures


def _check_usage(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    failures: list[ConformanceFailure] = []
    result = adapter.map_usage(samples.usage_raw)

    if result != samples.expected_usage:
        failures.append(ConformanceFailure(
            "usage", "map_usage(samples.usage_raw) does not equal samples.expected_usage"))

    if result is not None:
        if not isinstance(result, AdapterUsage):
            failures.append(ConformanceFailure(
                "usage", f"map_usage's non-None answer is not an AdapterUsage: {result!r}"))
        else:
            if not isinstance(result.actuals, UsageActuals):
                failures.append(ConformanceFailure(
                    "usage", f"AdapterUsage.actuals is not a UsageActuals: {result.actuals!r}"))
            if not isinstance(result.raw_counters, dict) or not result.raw_counters:
                failures.append(ConformanceFailure(
                    "usage", f"AdapterUsage.raw_counters must be a non-empty dict: {result.raw_counters!r}"))

    if adapter.map_usage("") is not None:
        failures.append(ConformanceFailure("usage", 'map_usage("") must be None'))
    return failures


def _check_errors(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    failures: list[ConformanceFailure] = []
    expected_classes = {sample.expected for sample in samples.error_samples}
    if FailureClass.PROVIDER_UNAVAILABLE not in expected_classes:
        failures.append(ConformanceFailure(
            "errors", "samples.error_samples has no expected PROVIDER_UNAVAILABLE sample"))
    if FailureClass.PROVIDER_TIMEOUT not in expected_classes:
        failures.append(ConformanceFailure(
            "errors", "samples.error_samples has no expected PROVIDER_TIMEOUT sample"))

    for sample in samples.error_samples:
        got = adapter.classify_error(sample.error_text, sample.exit_code)
        if got not in ADAPTER_ERROR_CLASSES:
            failures.append(ConformanceFailure(
                "errors",
                f"classify_error({sample.error_text!r}, {sample.exit_code!r}) returned {got!r}, "
                f"outside ADAPTER_ERROR_CLASSES"))
        elif got != sample.expected:
            failures.append(ConformanceFailure(
                "errors",
                f"classify_error({sample.error_text!r}, {sample.exit_code!r}) returned {got!r}, "
                f"expected {sample.expected!r}"))
    return failures


def _check_isolation(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    # The protocol types isolation() as always returning None; this runtime check exists
    # precisely to catch a broken implementation that violates that statically-declared promise.
    result = adapter.isolation()  # type: ignore[func-returns-value]
    if result is not None:
        return [ConformanceFailure("isolation", f"isolation() must return None, got {result!r}")]
    return []


def _lowered_contains_forbidden(text: str) -> bool:
    lowered = text.lower()
    return any(bad in lowered for bad in _FORBIDDEN_NAME_SUBSTRINGS)


def _transport_source_failures(source: str) -> list[str]:
    """Every forbidden name or module use in one class's own source, as detail strings."""
    tree = ast.parse(source)
    details: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if _lowered_contains_forbidden(node.id):
                details.append(f"name {node.id!r} at line {node.lineno}")
            if node.id in _FORBIDDEN_MODULE_ROOTS:
                details.append(f"use of {node.id!r} at line {node.lineno}")
        elif isinstance(node, ast.Attribute):
            if _lowered_contains_forbidden(node.attr):
                details.append(f"attribute .{node.attr} at line {node.lineno}")
        elif isinstance(node, ast.arg):
            if _lowered_contains_forbidden(node.arg):
                details.append(f"argument {node.arg!r} at line {node.lineno}")
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            if _lowered_contains_forbidden(node.name):
                details.append(f"function {node.name!r} at line {node.lineno}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname or alias.name
                if _lowered_contains_forbidden(bound):
                    details.append(f"import alias {bound!r} at line {node.lineno}")
                if alias.name.split(".")[0] in _FORBIDDEN_MODULE_ROOTS:
                    details.append(f"import of {alias.name!r} at line {node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound = alias.asname or alias.name
                if _lowered_contains_forbidden(bound):
                    details.append(f"import alias {bound!r} at line {node.lineno}")
            if node.module and node.module.split(".")[0] in _FORBIDDEN_MODULE_ROOTS:
                details.append(f"import from {node.module!r} at line {node.lineno}")
    return details


def _check_transport(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    source = textwrap.dedent(inspect.getsource(type(adapter)))
    return [ConformanceFailure("transport", detail)
            for detail in _transport_source_failures(source)]


_DIMENSION_CHECKS = {
    "capabilities": _check_capabilities,
    "invocation": _check_invocation,
    "stream": _check_stream,
    "usage": _check_usage,
    "errors": _check_errors,
    "isolation": _check_isolation,
    "transport": _check_transport,
}


def check_conformance_dimension(
    adapter: WorkerAdapter, samples: AdapterSamples, dimension: str,
) -> tuple[ConformanceFailure, ...]:
    """Every failure of one dimension; empty when the adapter conforms to it."""
    if dimension not in CONFORMANCE_DIMENSIONS:
        raise ValueError(f"unknown conformance dimension: {dimension!r}")
    if not isinstance(adapter, WorkerAdapter):
        return (ConformanceFailure(dimension, "adapter is not a WorkerAdapter"),)
    return tuple(_DIMENSION_CHECKS[dimension](adapter, samples))


def run_adapter_conformance(
    adapter: WorkerAdapter, samples: AdapterSamples,
) -> tuple[ConformanceFailure, ...]:
    """Every dimension's failures, concatenated in CONFORMANCE_DIMENSIONS order."""
    failures: list[ConformanceFailure] = []
    for dimension in CONFORMANCE_DIMENSIONS:
        failures.extend(check_conformance_dimension(adapter, samples, dimension))
    return tuple(failures)
