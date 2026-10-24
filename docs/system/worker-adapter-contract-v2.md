# Worker adapter contract v2: what any builder or reviewer backend provides

> Status (F151, 2026-10-23): the contract `packages/contracts/adapter_contract.py`, its
> conformance kit `packages/contracts/adapter_conformance_kit.py`, the claude-cli reference adapter
> `packages/providers/adapters/claude_cli_reference.py`, the adapter registry, the `adapter_ref`
> link of the worker list and the import guard are built. DECISIONs F151 D1 to D5 in
> `.agent/decisions.md`; the feature is `docs/roadmap/features/T8_F151.md`.
> Status (F315, 2026-10-23): every claude-cli call a job makes takes its command line from the
> installed adapter, through the worker adapter slot below, and a call that is not streamed takes
> its usage from the adapter too; the stream and the error classes stay with the evidence capture
> and the failure post-mortem (DECISIONs F315 D2 and D3).

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
and hyphens) and seven methods:

| Method | Answers |
|---|---|
| `capabilities(model)` | `AdapterCapabilities`: `vision`, `json_schema`, `session_resume`, `streaming`, `tool_use` as booleans and `max_context_tokens` (0 when not declared), for that model |
| `build_invocation(role, prompt_parts, options)` | a `CliInvocation` (argv and stdin text) or an `HttpInvocation` (method, URL, headers, JSON body); `role` is `builder` or `reviewer`, anything else raises `ValueError`; `InvocationOptions` carries the model, an output schema, a resume reference and an output limit, and no timeout |
| `map_stream(raw_lines)` | events whose `event_type` is one of the stream vocabulary of `stream_evidence.py`; empty for an adapter that does not stream |
| `map_usage(raw)` | `AdapterUsage`: the existing `UsageActuals` plus the provider's own usage counters unchanged, or `None` when the output holds no usage |
| `classify_error(error_text, exit_code)` | a member of `FailureClass`: provider unavailable, provider timeout, provider non-zero exit, parse or unknown |
| `isolation()` | a `WorkerIsolation` declaring how this adapter keeps the operator's own configuration and secrets out of a worker's call (DECISION F152 D3) |
| `sandbox_default()` | a `WorkerSandboxDefault` declaring the adapter's default sandbox profile as TOML text and whether its process runs inside the tool sandbox (DECISION F162 D4) |

Flags are declared honestly: an adapter declares only what its tests prove.

## The conformance kit
`run_adapter_conformance(adapter, samples)` checks eight dimensions in order — capabilities,
invocation, stream, usage, errors, isolation, sandbox and transport — and returns every failure,
each with its dimension and a detail; an empty answer means the adapter conforms.
`check_conformance_dimension` checks one. The caller supplies `AdapterSamples`: recorded raw stream
lines with their expected events, a recorded usage output with its expected answer, and error
texts with their expected class, at least one unavailable and one timeout among them. The kit
carries its own canonical prompt parts, which every invocation must carry.

The transport dimension reads the source of every class in the adapter's class chain and refuses
any name, attribute, argument or function that spells a retry, a timeout, a sleep or a backoff,
and any use of a process or network module; a member of `FailureClass` is the one exemption. It
reads the module-level functions of the class's own module that a class calls by name too, so a
transport hidden in a helper beside the class fails like one written inside it, and a class whose
source cannot be read fails the dimension instead of being skipped (amend1023 D4).
`adapter_transport_violations(source)` is that check for one source. The kit's own tests
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
The worker list, `packages/orchestration/worker_adapters.py`, is the worker adapter contract v2's
list of workers: it DESCRIBES a worker, its roles, mode and status. Its `adapter_ref` names the
adapter that EXECUTES the contract for it, and a record without a reference is a worker still
awaiting its adapter; today only `claude_code` names one, `claude-cli`, and its status reads
`available`. `ollama` and `pi_dev` run today through Remedy's own call paths and say in their notes
that they have no adapter yet. `packages/providers/adapters/adapter_registry.py` resolves a
reference to its adapter, and `remedy worker show claude_code` prints the adapter and its declared
capabilities; `remedy worker list --json` and `remedy worker show --json` carry `adapter_ref` for
every record, and `remedy worker show --json` also carries `capabilities`, the same flags the text
prints with `max_context_tokens`, or `null` for a worker without an adapter (amend1023 D4).

## The import guard
Orchestration and the contracts layer import the contract and never a concrete adapter.
`tests/contracts/test_adapter_import_guard.py` parses every file under `packages/orchestration/`
and `packages/contracts/` and fails on any import of `packages.providers.adapters` or a module
beneath it, whether named as the module or as a name imported from its parent, at the top of a
file or inside a function; only the wiring layer under `apps/` and the
adapters' own tests reach a concrete adapter.

## The worker adapter slot
`packages/orchestration/worker_adapter_slot.py` is how a concrete adapter reaches the loop without
an import the guard refuses. `main` in `apps/cli/grouped.py` calls `install_worker_adapters` with
the registry's classes before any command runs, so every job a command starts, the supervisor's
included, finds them; `tests/conftest.py` installs the same registry for tests that call the loop
directly. `installed_worker_adapter(adapter_ref, **settings)` builds the installed adapter for a
provider's binary path, write mode and streaming flag, and `adapter_cli_argv` returns the command
line it builds for one call of a role. `ClaudeCliProvider` takes the command line of its builder
call, its free-text and structured reviewer calls and its streamed calls from there; the reviewer's
write mode is the adapter's rule, read-only. An empty slot raises `WorkerAdapterNotInstalled`,
which the provider reports as a provider error: Remedy deliberately keeps no second command-line
builder as a fallback. The provider's own version probe is not a call the adapter builds.

`adapter_usage_actuals(adapter_ref, raw, **settings)` answers the usage the installed adapter's
`map_usage` maps from a call's output, and when the adapter answers none, the reason the shared
envelope reader gives (`is_error`, `usage_missing`, `parse_failed`, `empty_input`), which the
provider records and acts on as before. A call that is not streamed reads its usage there. Remedy
deliberately leaves two faces of the contract outside the loop's path: a streamed call's events
are normalised by the evidence capture while the process runs, and a failed call's class is set by
the failure post-mortem from every signal it has, of every provider alike; both are per-call
evidence the loop owns, and the adapter's `map_stream` and `classify_error` answer the same
functions for the kit and for `remedy worker show`.

## Worker isolation
Every claude-cli adapter declares `isolation()` (DECISION F152 D3): method `tool_flag`,
`--setting-sources project,local` and `--strict-mcp-config` appended to the call line, and a
cleaned environment carrying the shell/process names a worker needs plus the model's own
credential and proxy variables — no throwaway home, because the operator's login lives under the
operator's own home. `adapter_child_env` builds that environment and both `_cli_exec_policy` and
`_stream_exec_policy` in `pingpong_provider.py` set it as `env=`, leaving `env_allowlist` `None` so
it reaches the child exactly as built. `create_role_provider` writes one line per claude-cli
provider build to `worker_isolation.jsonl` beside the run's `capability_decisions.jsonl`, always,
naming the method, whether it applied, the home kind, the environment digest, the names kept and
the declaration's own ADR reference. `declared_isolation` refuses an installed adapter that
carries no `isolation()` member at all, so an adapter never runs with the operator's whole
environment by a quiet fallback (DECISION F152 D4 (1)). `run_isolation_ab`, also in
`packages/orchestration/worker_isolation.py`, is the throwaway-home pair's first caller: it builds
an adapter's own declared command line once, runs it twice against one poisoned throwaway home —
un-isolated with the operator's whole environment, isolated with the declaration's own flags and
environment — and reports whether the declared isolation actually hid the poison (DECISION F152 D4
(2)). Its stand-in proof runs in every selection against a test double standing in for `claude`,
together with two red controls that show the utility can fail when a declaration or a command line
really does leak. The run against the real binary waits for the operator's permission to spend a
paid call, the question DECISION F152 D4 (4) still holds open.

The conformance kit's isolation dimension also refuses an adapter whose declared record is
missing or carries no status line, and refuses a command line that drops its declared `tool_args`
while the declaration applies, an HTTP invocation exempt from that second check (DECISION F152 D5
(1)). An adapter failing either check does not certify, which is the handshake F156's certificate
reads. `worker doctor` adds four `isolation_<provider_id>_*` checks — declaration, record, home
and flags — right after a worker's own executable check and only once that executable is found,
reading the worker's `--help` through the replaceable `read_tool_help` rather than any paid call
(DECISION F152 D5 (2) and (3)).

## Sandbox default
Every adapter declares `sandbox_default()` (DECISION F162 D4): a `WorkerSandboxDefault` carrying
its default sandbox profile as TOML text and whether its process runs inside the tool sandbox,
with a reason required whenever it does not. The claude-cli adapter's default is an API allowlist
naming `api.anthropic.com`, every ulimit unlimited except `nofile` at 1024, and `tool_sandbox`
false, because the claude command line keeps its login in the operator's home, which the tool
sandbox hides (DECISION F152 D3). The allowlist is declarative, not enforced: DECISION F162 D3 (4)
already records an allowlist as unenforced, so a host the tool also reaches makes no recorded
promise false. The conformance kit's sandbox dimension refuses a `sandbox_default()` answer that
is not a `WorkerSandboxDefault`, and refuses a declared profile whose TOML `parse_sandbox_profile`
cannot parse, naming the parser's own refusal text.
Both claude-cli spawn policies compile that default through `adapter_exec_policy` in the worker
adapter slot (DECISION F162 D5): outside the tool sandbox, so for the claude-cli default it adds an
open-files limit of 1024 and nothing else. Every claude-cli provider build writes one line to
`worker_sandbox.jsonl` beside `worker_isolation.jsonl`, naming the profile, the runner, whether the
process runs inside the tool sandbox, and each dimension's enforced or unenforced state with its
reason.

## The capability matrix
`packages/contracts/capability_matrix.py` holds a declarative register,
`CAPABILITY_REQUIREMENTS`, mapping each capability-consuming feature to the adapter capability it
needs and to one registered degradation. A feature asks the register through `require_or_degrade`
or `capability_matrix_for`, never an adapter's `capabilities()` directly: both functions take the
resolved `(adapter, model)` pair and call `capabilities(model)` themselves, so a mid-job failover
that changes the pair changes what the next read sees. The resulting `CapabilityDecision` is one of
three modes: `native`, every required capability present; `degraded`, at least one absent and the
entry's registered fallback runs instead, named by its `strategy` token; or `unavailable`, at least
one absent and the entry has no fallback, which is legal only for a feature that may refuse
outright.

The three entries the register holds since DECISION F157 D3 (4): `reviewer_schema_gate` requires
`json_schema` and degrades to `schema_in_prompt`; `parked_session_resume` requires
`session_resume` and degrades to `full_context_resend`; `stream_evidence_capture` requires
`streaming` and degrades to `buffered_output`. No planner is an entry, because neither the Ollama
planner nor `ClaudeCliPlanner` builds its call through an installed adapter today. Three declared
capabilities have no consumer yet — `vision`, `tool_use` and `max_context_tokens` — and
`CAPABILITY_NO_CONSUMER_NOTES` records why for each.

Two guards in `tests/contracts/test_capability_matrix.py` keep the register honest: the read guard
sweeps every file under `packages/` and `apps/` and fails on a `.capabilities(` call outside
`packages/contracts/capability_matrix.py`, `packages/contracts/adapter_conformance_kit.py` and
`apps/cli/commands/worker.py`, so a consumer cannot bypass the register by reading an adapter
directly; the consumer guard fails any `require_or_degrade(` call whose first argument is not a
string literal naming a registered key, so an unregistered or dynamically built key cannot reach
the lookup silently.

A later round has the run's report and `remedy run show` print the evidence
`capability_degradation_entries` produces under the name `CAPABILITY_DEGRADATIONS_FIELD`
(`"capability_degradations"`) (DECISION F157 D3 (3)).

`remedy worker show` is the register's first consumer: its text answer prints a `Degradations:`
line directly after `Capabilities:`, reading `none` when every decision for that adapter is
native, or else every non-native decision joined by `, `, each `<feature_key> as <strategy>` when
degraded or `<feature_key> unavailable` when unavailable; a worker with no adapter carries neither
line. Its JSON answer carries `capability_matrix`, the list of the register's decisions in
register order, or `null` without an adapter.

`packages/orchestration/capability_routes.py` is the second consumer, and the first routed one. It
holds three routes — `stream_capture_route`, `reviewer_schema_route` and `parked_resume_route` —
each calling `require_or_degrade` with its register key as a string literal on the role's installed
adapter and model; a stream is the one registered feature a run opts into, decided only when the
run requested stream evidence, while every claude-cli build is asked about resuming whether or not
it offers a parked session to resume (DECISION F157 D6 (1) and (3)). `routed_claude_cli_build` is
`create_role_provider`'s one call for a claude-cli build's whole set of decisions: it reads the
resume route for every role, the reviewer-schema route for the reviewer, and the stream route when
the run requested one, and it records every decision it read in a single line, but only when at
least one of them is not native — an all-native build writes nothing. The recorded line carries
`role`, `provider`, `model` and `decisions`, written beside the run as `capability_decisions.jsonl`
in the evidence directory `create_role_provider` receives; a failover link built mid-run writes its
own line, so the evidence follows the pair. `ClaudeCliProvider` reads `routed_reviewer_schema` and
`routed_parked_resume` on every call that needs them, with the operator switch
`REMEDY_REVIEWER_FREETEXT` that `structured_outputs.py` owns still kept in force beside the route.
`read_capability_degradations(evidence_dir)` reads the evidence file back into the run's
degradations, `capability_degradation_entries` over every decision across every line. A run's
degradations name what its provider pair runs in its fallback whenever that feature is used: for
`parked_session_resume`, that the provider resumes no session, so every call of that provider sends
its full context (DECISION F157 D6 (2)).

`packages/orchestration/capability_evidence.py` reads a run's or a job task's degradations back
across every directory a build may have written to (DECISION F157 D5 (2)); what it reads back
names what the provider pair runs in its fallback whenever that feature is used, and for
`parked_session_resume` that the provider resumes no session, so every call of that provider sends
its full context (DECISION F157 D6 (2)). `remedy run show`'s JSON answer always carries the list
under `capability_degradations`, and its text prints a `Degradations:` line, worded through
`format_capability_degradations`, only when that list is not empty. The job report prints the same
wording under a task whose own evidence names a degradation, right after that task's steering
lines, and prints nothing for a task or a job with none.
