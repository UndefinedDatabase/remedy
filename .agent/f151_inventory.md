# F151 T001 — the inventory of the worker call path and its owners

Read at `4232c579e` (the merge of pull request 382, F133's closure). Read-only: no file but this one
changed. Every factual sentence names `path:line` at that commit unless a different commit is named.

## 1. What was deleted

`git show 3384dd535 --stat` (F275 R16 C3, "delete the main builder adapter module group") removed
`packages/orchestration/main_builder_adapter.py` (964 lines), `apps/cli/commands/main_builder_adapter_cmd.py`
(143 lines) and `apps/cli/commands/worker_facade_cmd.py` (218 of its lines), plus docs and tests, netting
2519 deletions against 13 insertions. Its last content
(`git show 3384dd535^:packages/orchestration/main_builder_adapter.py:1-54`) shows it was an external
builder SESSION RAIL: metadata, request packages and session-lifecycle records for Claude Code / Pi.dev /
OpenCode / a generic CLI builder, kept untrusted until an "External Builder Sandbox" intake — never a
call to a provider, model or subprocess (`main_builder_adapter.py:11-24` old). It is not the ping-pong
loop's provider path; it was a separate, disabled-by-default session-package layer.

`git show 1abe8ac21 --stat` (F275 R20 C4, "delete the worker_registry module group") removed
`packages/orchestration/worker_registry.py` (1035 lines) and `apps/cli/commands/route_policy_cmd.py`
(196 lines), plus docs and tests, netting 2218 deletions against 45 insertions. Its last content
(`git show 1abe8ac21^:packages/orchestration/worker_registry.py:1-44,70-217,436`) provided `WorkerSpec`
(kind/cost/risk tiers, `enabled`/`user_selectable`), `RoutePolicy`, `is_placeholder()` (a spec is a
placeholder when disabled, cloud-tier, or `kind` is Ollama/cloud candidate — `worker_registry.py:206-216`
old) and `evaluate_worker_selection` — all METADATA + POLICY, never an execution
(`worker_registry.py:11-26` old).

Every surviving reference, checked today: `grep -rln worker_registry|main_builder_adapter --include=*.py
packages apps tests docs` returns nothing — no code or doc under those four trees names either module.
`grep -rln WorkerSpec|RoutePolicy|is_placeholder` (same trees) is equally empty: the types these two
modules defined do not survive either, in any file. The only module still bearing a similar name is
`packages/orchestration/worker_adapters.py` (142 lines), a data-only `WorkerProviderSpec` list unrelated
in shape to either deleted module (see §6).

## 2. The call path today

A role's config: `packages/orchestration/role_config.py:92` sets `DEFAULT_PROVIDER = "ollama"`;
`:153` lists `KNOWN_ROLES`; `:172-188` give per-role provider/model overrides; `:215-236` define
`RoleConfig` (`provider`, `model`, `effort`, `routed_call`); `:420` `resolve_role_config` merges them.
`provider_names.py:11` spells the only five legal provider names once:
`{"fake", "claude", "claude-cli", "ollama", "pi"}`.

The build seam: `role_provider_factory.py:25` `create_role_provider` constructs a `ClaudeCliProvider` for
`name == "claude-cli"` (`:67-84`), a `PiProvider` via `pi_provider.make_pi_provider` for `name == "pi"`
(`:85-89`), or defers to `pingpong_provider.create_provider` for any other name (`:90-91`); when the
role's configured chain is non-empty it wraps the result in a `model_failover.FailoverProvider`
(`:93-122`). `pingpong_provider.py:1560-1574` `create_provider` builds `fake` (deliverable fake,
`:1562-1564`), `claude` (`ClaudeProvider`, direct Anthropic SDK, `:1565-1566`) and `ollama`
(`OllamaPingPongProvider`, `:1569-1571`).

Five concrete `PingPongProvider` implementations exist (the protocol: `pingpong_provider.py:162-187`,
`build`/`review` returning `BuilderOutput`/`ReviewerOutput`, `:66-155`): `ClaudeProvider` (direct API,
`:322-499`, non-streaming, `supports_resume=False` at `:363-364`), `ClaudeCliProvider` (local `claude`
subprocess, `:881-1560`, `supports_resume=True` at `:1014-1017`), `OllamaPingPongProvider`
(`pingpong_provider_ollama.py:33-96`, local HTTP via the `ollama` package, stateless,
`supports_resume=False` at `:78-81`), `PiProvider` (`pi_provider.py:614-657`, the Pi harness run as a
subprocess, `supports_resume=False`), and the fake/deliverable provider (`fake_deliverable.py`, test-only).

Every real call goes through one seam regardless of provider: `pingpong_loop.py:3216-3231` (builder) and
`:3547-3567`/`:3606-3630` (reviewer, including its own resume-fallback repeat) and `:3670-3686` (the
reviewer's single parse retry) all call `_call_with_retry` from `pingpong_provider_call.py:143`, passing
a zero-argument lambda that invokes `provider.build(...)` or `provider.review(...)`. Timeouts are computed
by the loop itself before any of these calls: `pingpong_loop.py:2823-2824` calls
`provider_timeouts.compute_timeout("builder"|"reviewer", ...)`.

## 3. The contract's faces, mapped

**Capabilities.** No typed `capabilities()` record exists anywhere today. The closest things are
data-only and unverified: `worker_adapters.py:29-40`'s `WorkerProviderSpec.supported_roles`/
`execution_mode` (never checked against what a provider actually does), and `provider_names.py:11`'s
flat name set. Nothing declares vision, JSON-schema support, session-resume or streaming per
model/provider pair; `resolve_role_config` (`role_config.py:420`) knows provider and model strings only.
T002 adds this face from nothing — there is no legacy shape to reconcile it with.

**Invocation building, per provider, today:**
- claude-cli: `claude_cli_command.py:66-113` `build_claude_cli_args` builds the CLI argv
  (`-p <prompt> --output-format json|stream-json`, `--model`, `--json-schema`, `--resume`,
  `--allowedTools`/`--dangerously-skip-permissions`, then `claude_cli_launch_switches` at `:46-59`
  appends `--safe-mode`/`--tools`). `pingpong_provider.py:1161-1164` calls it from `_call`.
- claude (direct API): `pingpong_provider.py:350-356` `_request_parts` splits the prompt into a cached
  system block plus remainder; `:391-422` `_call` sends it via the `anthropic` SDK client
  (`:372-389` `_get_client`).
- ollama: `pingpong_provider_ollama.py:97-99` `_call_options` and `:101-` `_call` build a chat request
  for the local `ollama` package (HTTP under the hood to `REMEDY_OLLAMA_HOST`, default
  `http://localhost:11434`, `:30,69-71`), with `format_schema` for native structured output (`:107,111`).
- pi: `pi_provider.py:355` `build_pi_argv` builds the Pi CLI's argv; `:850` `make_pi_provider` and
  `:614-657` `PiProvider` wrap it the same way claude-cli is wrapped.
No invocation builder lives outside its own provider module today; none is shared.

**Stream mapping.** Only claude-cli streams today: `ClaudeCliProvider._call` (`pingpong_provider.py:1143
-1160`) dispatches to `_call_streamed` (`:1058`) when `self._stream_evidence` is set, else takes the
buffered `--output-format json` path. The event vocabulary a stream is mapped onto is
`stream_evidence.py:63-72` (`EVENT_TOOL_USE`, `EVENT_TOOL_RESULT`, `EVENT_API_RETRY`, `EVENT_TOKEN_USAGE`,
`EVENT_RESULT`, `EVENT_PROVIDER_ERROR`, `EVENT_MALFORMED`, `EVENT_CAP_REACHED`, `EVENT_DEGRADED`), built
by `normalize_stream_object` (`:293-376`). The other four providers (direct API, ollama, pi, fake) never
stream; each returns one buffered answer. The Edge-cases note in the feature file ("map_stream may
declare non-streaming") matches this: a contract-side buffered fallback, not a gap to close by force.

**Usage mapping.** `token_actuals.py:51` `parse_cli_result_detailed` and `:148` `parse_cli_envelope`
parse the claude-cli JSON envelope; `pingpong_provider.py:1189-1208` turns the parsed `UsageActuals` into
the `usage_actuals` dict carried on `BuilderOutput`/`ReviewerOutput` (`input_tokens`, `output_tokens`,
`cache_read`, `cache_creation`, `total_cost_usd`, `num_turns`, `duration_ms`, `session_id`,
`cli_version`, `parse_source="claude_cli_json"`) — raw counters kept, not discarded, exactly what the
design note (T8_F151.md's `map_usage`) asks. When parsing fails, `usage_actuals=None` and
`actual_missing_reason` names why (`:1205-1208`). The direct-API and ollama/pi providers do not yet
populate the same dict shape from their own raw responses at the same fidelity — each provider owns its
own partial mapping; there is no single `map_usage(raw)` function today.

**Isolation.** claude-cli and pi run as real subprocesses under `exec_guard.run_guarded`:
`pingpong_provider.py:813-824` `_cli_exec_policy` pins `cwd` to the role's staging dir, sets a wall
timeout and zero core size, but sets no `sandbox` — the child inherits the operator's environment and
credentials by design (`:816-824`, comment: "the child is the operator's authenticated `claude` CLI").
Bubblewrap sandboxing (`exec_guard.py:585-649`, `test_command_exec_policy`/`run_guarded_test_command`,
`SandboxSpec`) exists today but is applied only to TEST commands the model's own candidate proposes,
never to the provider call itself. ollama and the direct API are plain network calls (local HTTP, or
HTTPS to Anthropic) with no process or filesystem isolation construct at all. F152 is explicitly where
an isolation declaration gets specified; today there is no declared shape, only this ad hoc mix.

## 4. The error taxonomy

Two layers classify failures today, for different audiences. `provider_timeouts.py:103`
`is_timeout_error`, `:122` `is_nonzero_exit_error` and `:134` `should_retry` decide, per call, whether
`pingpong_provider_call.py:143` `_call_with_retry`'s bounded transport retry fires (`:205-244`): timeout
or non-zero exit, never a review reject (`:219-224`), plus a rate limit when a governor is active
(`:226-239`). A reached stream cap is a deliberate termination, never retried (`:212-213`).

For the FINAL, un-retried failure, `failure_postmortem.py:79-123` `FailureClass` is the one enum every
layer maps onto: `PROVIDER_TIMEOUT`, `PROVIDER_UNAVAILABLE`, `PROVIDER_NONZERO_EXIT`, `PARSE`, `CONFIG`,
plus non-provider classes (`IO_FAILURE`, `RESOURCE_LIMIT`, `SANDBOX_UNAVAILABLE`, ...). `:137-153`
`is_provider_unavailable_error` reads for "the executable is not there"; `:156-174`
`is_provider_connection_error` reads for "reachable-shaped but did not answer" (connection
refused/reset, HTTP 5xx, "overloaded"); both map to `PROVIDER_UNAVAILABLE`. A schema-validation failure
is tagged `error_class="parse"` on the output itself (`pingpong_provider.py` `ReviewerOutput.error_class`,
`:131-134`), not detected by text matching.

`model_failover.py:346-363` `is_failover_trigger` is narrower than either postmortem predicate: it
excludes a parse error (`:351-352`), a `malformed_output:` prefix (`:353-354`), a timeout and most rate
limits (`:357-359`), and fires only on `is_provider_unavailable_error`/`is_provider_connection_error`
(`:363`) — the one gap `FailoverProvider` (`:447`) owns. A refusal (a reviewer verdict of
`needs_repair`/`fail`/`blocked` without a `provider_error:`-prefixed error) is never retried and never
fails over; it is the loop's normal repair path (`pingpong_provider_call.py:219-224`).

A malformed answer gets its own single bounded retry, inside the loop and nowhere else:
`pingpong_loop.py:3645-3686` fires exactly once when `reviewer_out.error` starts with
`"malformed_output:"`, builds a retry prompt from the parse hint or a legacy excerpt (`:3659-3665`), and
calls `_call_with_retry` again with `is_parse_retry=True` (`:3670-3686`) — so a parse retry's own
transport retries are booked but never counted as a second parse retry.

## 5. Ownership table

| Concern | Module : function |
|---|---|
| Invocation building (CLI argv / HTTP request) | per-provider: `claude_cli_command.py:66`, `pingpong_provider.py:350-422` (direct API), `pingpong_provider_ollama.py:101`, `pi_provider.py:355` |
| Process spawn / exec policy | `exec_guard.py:365-495` `plan_child_spawn`/`run_guarded`; called by `pingpong_provider.py:856` `_guarded_cli_run` |
| Timeout computation | `pingpong_loop.py:2823-2824` `compute_timeout`, policy in `provider_timeouts.py:21-103` |
| Transport retry (bounded, per logical call) | `pingpong_provider_call.py:143-282` `_call_with_retry` |
| Parse retry (bounded, reviewer only) | `pingpong_loop.py:3645-3686` |
| Failover across providers/models | `model_failover.py:268-363,447` `FailoverProvider`/`resolve_failover_chains`/`is_failover_trigger` |
| Rate-limit pacing | `rate_governor.py` `ProviderRateGovernor`, consulted inside `_call_with_retry` (`pingpong_provider_call.py:191-263`) |
| Per-call evidence (`ProviderAttempt`) | `pingpong_provider_call.py:38-54,84-121` `ProviderAttempt`/`_record_attempt`, written onto `PingPongResult.provider_attempts` |
| Token ledger (usage_actuals) | `token_actuals.py:16-148`; carried on `BuilderOutput`/`ReviewerOutput.usage_actuals` (`pingpong_provider.py:79,137`) |
| Final-failure classification | `failure_postmortem.py:79-334` |

Every place an adapter could re-implement a retry or a timeout, which the Acceptance forbids: any new
`packages/workers/adapter_api.py` implementation that calls `time.sleep`/loops on its own exception, or
reads a `timeout_sec` it did not receive as an argument from the loop. None of today's five providers do
this themselves — `_call`/`_call_impl` in each one makes exactly one attempt and returns; every retry
loop above is outside the provider object, in `_call_with_retry` or the loop. T002's conformance kit
must assert a toy adapter that DOES retry internally fails the kit (feature file's "broken toy").

## 6. The v1 list and the guard

`worker_adapters.py:29-40` defines `WorkerProviderSpec` (`provider_id`, `display_name`,
`supported_roles`, `execution_mode`, `status`, `notes` — frozen dataclass); `:47-88` lists five records
(`ollama` status `"available"`; `claude_code`, `pi_dev`, `copilot`, `openai_api` status `"future"`).
Consumers: `apps/cli/commands/worker.py:24-30,53-58,231-238` (`remedy workers`, `worker show`,
`worker doctor` — all read-only CLI display/probe commands) and
`packages/orchestration/project_brain.py:109,625-637` (`_build_worker_adapter_nodes`, a graph-display
node per spec for the brain viewer, metadata only). Tests: `tests/test_worker_adapters.py`,
`tests/orchestration/test_command_discovery.py`, `tests/cli/test_worker.py`. No running job reads
`worker_adapters.py`: `grep -n worker_adapters packages/orchestration/pingpong_loop.py
role_provider_factory.py role_config.py` returns nothing — the five `WorkerProviderSpec` records never
reach `create_provider`/`create_role_provider`; they describe providers the call path does not consult.

Modules under `packages/orchestration/` that import a concrete provider today (what an import guard of
"orchestration imports only the contract" would bind): `empty_diff_gate.py`, `pingpong_loop.py`,
`pingpong_provider.py`, `pingpong_provider_fake.py`, `pingpong_provider_ollama.py`, `pi_provider.py`,
`role_provider_factory.py`, `verified_repair.py` (`grep -rln "from packages.orchestration.pingpong_provider
import\|pingpong_provider_ollama import\|claude_cli_command import" packages/orchestration/*.py`).

Existing import guard shape to follow: `tests/orchestration/test_import_reachability.py:1-66` — a
STATIC `ast`-based walk from named entry points, checked against a generated allowlist file
(`import_reachability_allowlist.txt`) as a ratchet (shrinks on deletion, reds on a new orphan or a new
edge), never by importing the module under test (`:13-16`, "importing the cockpit runs module-level side
effects"). A new "orchestration imports only the contract" guard should be the same shape: parse every
`packages/orchestration/*.py` with `ast`, assert none but the contract/kit/reference-adapter modules
import a concrete provider module, generate its own allowlist, with a violation fixture proving it reds.

## 7. Names

Every module/class/command with `adapter` in its name or docstring, today: `main_builder_adapter.py`
(deleted, §1); `worker_registry.py` (deleted, §1); `worker_adapters.py` (surviving, data-only list, §6);
`agent_loop.py:101` `AgentAdapterSpec` (a THIRD, unrelated metadata-only "external agent adapter" shape,
`dry_run_only=True`, consumed only by `apps/cli/commands/brain.py`'s display); `project_brain.py:625`
`_build_worker_adapter_nodes` (reads `worker_adapters.py`, §6); `brain_detail.py:1163`
`_detail_worker_adapter` (same graph, detail view); `feature_mission_adapter.py` (unrelated: compiles a
roadmap feature file into a mission, nothing to do with providers — `:1-18`). `apps/cli/commands/worker.py`
and `apps/cli/command_catalog.py` carry the `worker` command group that reads `worker_adapters.py`.

`adapter` is already a crowded, overloaded word in this tree (four unrelated things use it). Proposed
names for DECISION F151 D2, each checked to grep to itself: `packages/workers/provider_contract.py`
(the typed contract: capabilities/build_invocation/map_stream/map_usage/isolation — avoids "adapter"
entirely, since the thing being contracted is a provider, and the repo already spells that word
`pingpong_provider.py`/`provider_names.py`); `packages/workers/provider_conformance_kit.py` (the
pytest-importable suite); `packages/workers/claude_cli_reference_provider.py` (T003's reference wrap over
today's `ClaudeCliProvider`, named for what it wraps rather than for being "the adapter"). None of these
collide with an existing name; `grep -rln` for each (once written) should return only its own file and
its test. Checked against `docs/system/structure-ledger-v1.md:248-254`: `pingpong_provider.py` is a
listed file with one undone structural note beyond its three done steps — none that this new package
touches, since the new modules live under `packages/workers/`, not `packages/orchestration/`.

## 8. Proposal (for DECISION F151 D2, not a decision)

Per face, what T002/T003 wraps or builds fresh:
- **Capabilities**: not present today (§3); T002 builds `capabilities(role, model)` fresh, honest-flags
  only, starting from what each of the five providers is OBSERVED to support (`supports_resume`,
  streaming only for claude-cli, no vision/json_schema declared anywhere today).
- **Invocation building**: wraps the four real builders named in §3 unchanged — `build_claude_cli_args`
  (claude-cli), `_request_parts`/SDK call (direct API), the ollama `_call`, `build_pi_argv` (pi) — each
  behind one `build_invocation()` per adapter; no new argv/request logic, only a shared return shape.
- **Stream mapping**: wraps `stream_evidence.py`'s existing `EVENT_*` vocabulary and
  `normalize_stream_object` unchanged for claude-cli; the other four declare non-streaming per the Edge
  Cases note, which the existing non-stream path already serves.
- **Usage mapping**: wraps `token_actuals.py`'s parse for claude-cli unchanged (its goldens exist
  already, recorded in whatever `tests/` fixtures capture a real claude-cli JSON envelope — a search for
  recorded `cli_version`/`usage` fixtures under `tests/orchestration/` is T002's own task, not this one's);
  the other three providers need their own raw-to-`usage_actuals` mapping made explicit, which is new
  work, not a wrap.
- **Isolation**: nothing to wrap — today's isolation is ad hoc per provider (§3) and F152 is where the
  declaration shape is designed; T002/T003 reserve the face without filling it, exactly as the feature
  file already says.
- **What retires**: nothing in `packages/orchestration/` is deleted by T002 — `worker_adapters.py` stays
  as the v1 descriptive list until T003's registry linkage decides its relationship to `adapter_ref`
  (feature file, "Design"); no code following this inventory restores `main_builder_adapter.py` or
  `worker_registry.py` (DECISION F151 D1).
