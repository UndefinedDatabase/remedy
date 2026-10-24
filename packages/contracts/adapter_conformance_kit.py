"""The worker adapter conformance kit (F151 T002, DECISION F151 D2 (4)).

Every adapter's own test suite imports this and runs ``run_adapter_conformance``
against a real instance plus recorded :class:`AdapterSamples`. A dimension that
conforms returns no failures; a broken adapter fails on exactly the dimension
its break belongs to. The kit catches no exception of its own except the one
``build_invocation("planner", ...)`` is contracted to raise, and the
``SandboxProfileError`` ``parse_sandbox_profile`` raises for a default that does
not parse (DECISION F162 D4 (3)) — an adapter that raises anywhere else fails
its caller's test loudly, by design.
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
    WorkerIsolation,
    WorkerSandboxDefault,
)
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.sandbox_profiles import SandboxProfileError, parse_sandbox_profile
from packages.orchestration.token_actuals import UsageActuals
from packages.orchestration.worker_isolation import has_isolation_record

#: The eight faces a worker adapter is checked against, in the order every run checks them.
CONFORMANCE_DIMENSIONS = (
    "capabilities", "invocation", "stream", "usage", "errors", "isolation", "sandbox", "transport",
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
    # The protocol types isolation() as always returning a WorkerIsolation; this runtime check
    # exists precisely to catch a broken implementation that violates that promise.
    result = adapter.isolation()
    if not isinstance(result, WorkerIsolation):
        return [ConformanceFailure(
            "isolation", f"isolation() must return a WorkerIsolation, got {result!r}")]
    failures: list[ConformanceFailure] = []
    # No adapter certifies without the record the handshake F156's certificate reads (D5 (1));
    # the record check itself is the doctor's own, the one definition (R-1461).
    if not has_isolation_record(result.adr_ref):
        failures.append(ConformanceFailure(
            "isolation", f"isolation record {result.adr_ref} is missing or has no status line"))
    if result.applies and result.tool_args:
        invocation = adapter.build_invocation(
            "builder", ("a one-line prompt",), InvocationOptions(model=samples.model))
        if isinstance(invocation, CliInvocation):
            tool_args = list(result.tool_args)
            if list(invocation.argv[-len(tool_args):]) != tool_args:
                failures.append(ConformanceFailure(
                    "isolation", "the command line does not end with the declared tool_args"))
    return failures


def _check_sandbox(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    # The protocol types sandbox_default() as always returning a WorkerSandboxDefault; this
    # runtime check exists precisely to catch a broken implementation that violates that promise
    # (DECISION F162 D4 (3)).
    result = adapter.sandbox_default()
    if not isinstance(result, WorkerSandboxDefault):
        return [ConformanceFailure(
            "sandbox", f"sandbox_default() must return a WorkerSandboxDefault, got {result!r}")]
    try:
        parse_sandbox_profile(adapter.adapter_id, result.profile_toml)
    except SandboxProfileError as exc:
        return [ConformanceFailure(
            "sandbox", f"sandbox default profile does not parse: {exc}")]
    return []


def _lowered_contains_forbidden(text: str) -> bool:
    lowered = text.lower()
    return any(bad in lowered for bad in _FORBIDDEN_NAME_SUBSTRINGS)


def adapter_transport_violations(source: str) -> list[str]:
    """Every forbidden name or module use in one class's own source, as detail strings.

    An ``Attribute`` whose value is the bare name ``FailureClass`` — e.g.
    ``FailureClass.PROVIDER_TIMEOUT``, the member ``classify_error`` must be able to return for a
    timeout — is exempt from the forbidden-word check; nothing else is (DECISION F151 D3 (2)).
    """
    tree = ast.parse(source)
    details: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if _lowered_contains_forbidden(node.id):
                details.append(f"name {node.id!r} at line {node.lineno}")
            if node.id in _FORBIDDEN_MODULE_ROOTS:
                details.append(f"use of {node.id!r} at line {node.lineno}")
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "FailureClass":
                continue
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


def _readable_source(target: object) -> str | None:
    """TARGET's dedented source, or None when Python cannot read it (a class built at run time)."""
    try:
        return textwrap.dedent(inspect.getsource(target))  # type: ignore[arg-type]
    except (OSError, TypeError):
        return None


# WHY (amend1023 D4): a transport hidden in a helper beside the class is still the class's transport.
def _module_functions_called(klass: type, source: str) -> list[object]:
    """The functions of KLASS's own module that SOURCE calls by bare name, and the module functions
    those call in turn, each once, in name order; an imported function belongs to another module."""
    module = inspect.getmodule(klass)
    found: dict[str, object] = {}
    pending = [source]
    while pending:
        tree = ast.parse(pending.pop())
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                continue
            value = getattr(module, node.func.id, None)
            if (node.func.id in found or not inspect.isfunction(value) or module is None
                    or value.__module__ != module.__name__):
                continue
            found[node.func.id] = value
            called = _readable_source(value)
            if called is not None:
                pending.append(called)
    return [found[name] for name in sorted(found)]


def _check_transport(adapter: WorkerAdapter, samples: AdapterSamples) -> list[ConformanceFailure]:
    """Every class of the adapter's chain, and every function of its module it calls, read for
    transport; a source Python cannot read is a failure, never a pass (amend1023 D4)."""
    failures: list[ConformanceFailure] = []
    for klass in type(adapter).__mro__:
        if klass is object or klass is WorkerAdapter:
            continue
        source = _readable_source(klass)
        if source is None:
            failures.append(ConformanceFailure(
                "transport", f"{klass.__qualname__}: its source cannot be read, so its transport cannot be checked"))
            continue
        for detail in adapter_transport_violations(source):
            failures.append(ConformanceFailure("transport", f"{klass.__qualname__}: {detail}"))
        for function in _module_functions_called(klass, source):
            name = getattr(function, "__name__", "?")
            called = _readable_source(function)
            if called is None:
                failures.append(ConformanceFailure(
                    "transport", f"{klass.__qualname__} calls {name}, whose source cannot be read"))
                continue
            for detail in adapter_transport_violations(called):
                failures.append(ConformanceFailure("transport", f"{klass.__qualname__} calls {name}: {detail}"))
    return failures


_DIMENSION_CHECKS = {
    "capabilities": _check_capabilities,
    "invocation": _check_invocation,
    "stream": _check_stream,
    "usage": _check_usage,
    "errors": _check_errors,
    "isolation": _check_isolation,
    "sandbox": _check_sandbox,
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
