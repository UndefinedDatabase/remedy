# Worker adapter contract v1: what any builder or reviewer backend provides

> Status (F151, 2026-10-23): the contract `packages/contracts/adapter_contract.py`, its
> conformance kit `packages/contracts/adapter_conformance_kit.py`, the claude-cli reference adapter
> `packages/providers/adapters/claude_cli_reference.py`, the adapter registry, the `adapter_ref`
> link of the worker list and the import guard are built. The ping-pong loop still calls its
> providers directly; no job runs through an adapter yet. DECISIONs F151 D1 to D5 in
> `.agent/decisions.md`; the feature is `docs/roadmap/features/T8_F151.md`.

Remedy's neutrality promise needs one interface that every vendor's backend fills in the same way,
so that adding a backend never touches orchestration. This page names that interface, the kit
that proves an implementation honours it, and the one implementation that exists today.

## Who owns what
The loop and its seams own everything that touches the outside world or decides to try again:
spawning the process or sending the request (`exec_guard.run_guarded`, the provider SDKs), the
timeout of a call (`provider_timeouts.compute_timeout`), transport retries
(`pingpong_provider_call._call_with_retry`), the reviewer's one parse retry (`pingpong_loop.py`),
failover between models (`model_failover.FailoverProvider`), rate pacing (`rate_governor`) and
the per-call evidence (`ProviderAttempt`, the token ledger, the stream capture).

An adapter only BUILDS an invocation and MAPS what came back. It receives no timeout, never
sleeps, never loops on a failure and never opens a process or a socket. Remedy deliberately keeps
retries out of adapters, because a second retry loop inside one would multiply the loop's own and
hide attempts from the per-call evidence.

## The contract
`WorkerAdapter` is a runtime-checkable protocol with an `adapter_id` (lower-case letters, digits
and hyphens) and six methods:

| Method | Answers |
|---|---|
| `capabilities(model)` | `AdapterCapabilities`: `vision`, `json_schema`, `session_resume`, `streaming`, `tool_use` as booleans and `max_context_tokens` (0 when not declared), for that model |
| `build_invocation(role, prompt_parts, options)` | a `CliInvocation` (argv and stdin text) or an `HttpInvocation` (method, URL, headers, JSON body); `role` is `builder` or `reviewer`, anything else raises `ValueError`; `InvocationOptions` carries the model, an output schema, a resume reference and an output limit, and no timeout |
| `map_stream(raw_lines)` | events whose `event_type` is one of the stream vocabulary of `stream_evidence.py`; empty for an adapter that does not stream |
| `map_usage(raw)` | `AdapterUsage`: the existing `UsageActuals` plus the provider's own usage counters unchanged, or `None` when the output holds no usage |
| `classify_error(error_text, exit_code)` | a member of `FailureClass`: provider unavailable, provider timeout, provider non-zero exit, parse or unknown |
| `isolation()` | reserved for the worker config isolation feature; `None` until that feature shapes it |

Flags are declared honestly: an adapter declares only what its tests prove.

## The conformance kit
`run_adapter_conformance(adapter, samples)` checks seven dimensions in order — capabilities,
invocation, stream, usage, errors, isolation and transport — and returns every failure, each with
its dimension and a detail; an empty answer means the adapter conforms.
`check_conformance_dimension` checks one. The caller supplies `AdapterSamples`: recorded raw stream
lines with their expected events, a recorded usage output with its expected answer, and error
texts with their expected class, at least one unavailable and one timeout among them. The kit
carries its own canonical prompt parts, which every invocation must carry.

The transport dimension reads the source of every class in the adapter's class chain and refuses
any name, attribute, argument or function that spells a retry, a timeout, a sleep or a backoff,
and any use of a process or network module; a member of `FailureClass` is the one exemption.
`adapter_transport_violations(source)` is that check for one class's source. The kit's own tests
fail a broken toy adapter on each check, one break at a time.

## The reference adapter
`ClaudeCliReferenceAdapter` (`adapter_id` `claude-cli`) wraps today's claude-cli functions and
re-implements none of them: the argv is `build_claude_cli_args`'s, the stream events come from
`redact_stream_payload` and `normalize_stream_object`, the usage from `parse_cli_result_detailed`,
and the error classes from the shared predicates the failure post-mortem reads. A line that is not
a JSON object maps to no event, because counting malformed lines is the capture's evidence. Its
tests compare it against those same functions on the recorded streams under
`tests/orchestration/fixtures/stream/`, and it passes the kit streaming and not streaming.

## The worker list and the registry
The v1 worker list, `packages/orchestration/worker_adapters.py`, DESCRIBES a worker: its roles,
mode and status. Its `adapter_ref` names the v2 adapter that EXECUTES the contract for it, and a
record without a reference is a worker still awaiting its adapter; today only `claude_code` names
one, `claude-cli`. `packages/providers/adapters/adapter_registry.py` resolves a reference to its
adapter, and `remedy worker show claude_code` prints the adapter and its declared capabilities;
`remedy workers --json` and `remedy worker show --json` carry `adapter_ref` for every record.

## The import guard
Orchestration and the contracts layer import the contract and never a concrete adapter.
`tests/contracts/test_adapter_import_guard.py` parses every file under `packages/orchestration/`
and `packages/contracts/` and fails on any import of `packages.providers.adapters` or a module
beneath it, whether named as the module or as a name imported from its parent, at the top of a
file or inside a function; only the wiring layer under `apps/` and the
adapters' own tests reach a concrete adapter.
