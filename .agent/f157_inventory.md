# F157 T001 — inventory of every capability check, its fallback and its tests

Written by the worker from reading the code at `0f811a713` (F157 round 1, DECISION F157 D1).
Every factual sentence names a `path:line`. Section 7's table is a draft for DECISION F157 D2,
marked as a proposal; nothing else here proposes or decides.

## 1. The declaration

`AdapterCapabilities` (`packages/contracts/adapter_contract.py:62-70`) is a frozen dataclass with
six fields: `vision`, `json_schema`, `session_resume`, `streaming`, `tool_use` (all `bool`), and
`max_context_tokens` (`int`). It is one face of the `WorkerAdapter` protocol
(`packages/contracts/adapter_contract.py:117-150`), whose `capabilities(model)` method
(`adapter_contract.py:126-128`) every adapter must implement.

**Declaring adapters.** Exactly one class under `packages/providers/adapters/` implements
`WorkerAdapter` today: `ClaudeCliReferenceAdapter`
(`packages/providers/adapters/claude_cli_reference.py:63-148`). Its `capabilities()`
(`claude_cli_reference.py:84-87`) returns `vision=False, json_schema=True, session_resume=True,
streaming=self._streaming, tool_use=True, max_context_tokens=0` for every model — declared, not
probed (its own comment at line 83: "nothing today measures a context size, so it stays 0"). The
registry that resolves a `WorkerProviderSpec.adapter_ref` to a concrete adapter,
`packages/providers/adapters/adapter_registry.py:16-18`, maps only `"claude-cli"` to this class.
The other provider directories under `packages/providers/`
(`claude_agent`, `claude_planner`, `docker_runtime`, `mempalace`, `ollama_builder`,
`ollama_planner`) hold no `capabilities()` method (confirmed:
`grep -rn "def capabilities" packages/providers/ packages/orchestration/` returns only
`claude_cli_reference.py:84`) and do not implement `WorkerAdapter` — they predate or sit outside
the F151 contract.

**Every reader of `capabilities(` or its field names under `packages apps`.**
`grep -rn "\.capabilities(" packages apps tests` finds exactly three non-test sites:
- `packages/contracts/adapter_conformance_kit.py:97-98` (`_check_capabilities`, calling it twice
  to prove determinism) and `:183` (`_check_stream`, reading `caps.streaming` at `:190` to decide
  whether `map_stream` must be empty) — the adapter's own conformance test harness, run by each
  adapter's test suite, never by a job.
- `apps/cli/commands/worker.py:69` (`_cmd_worker_show`), the `remedy worker show <provider_id>`
  command: resolves the adapter through the registry, calls `capabilities("")`, and prints the
  `True` flags (`worker.py:83-89`) or serializes them into JSON (`worker.py:70-75`). This is a
  read-only inspection command, not a call path.

**Plainly: no running job reads a declared capability today.** `worker_adapter_slot.py`
(`packages/orchestration/worker_adapter_slot.py`), the one seam through which orchestration
reaches an installed adapter (`adapter_cli_argv` at line 48, `adapter_usage_actuals` at line 65),
calls `build_invocation` and `map_usage` only — never `capabilities`. `grep -rn "\.capabilities("
packages/orchestration` has no hit.

## 2. The consumers, per capability

### json_schema
No call site reads `AdapterCapabilities.json_schema`. Three independent, uncoordinated decisions
about whether to use the provider's native `--json-schema`/`format=` enforcement exist instead:

- **Reviewer (claude-cli), native with a runtime probe.** `reviewer_structured_enabled()`
  (`packages/orchestration/structured_outputs.py:49-51`, env flag `REMEDY_REVIEWER_FREETEXT`)
  gates `_reviewer_effective_prompt` (`pingpong_loop.py:2469-2484`) onto `native_schema_prompt`
  (`structured_outputs.py:65-73`). The actual call,
  `ClaudeCliProvider._call_reviewer_structured` (`pingpong_provider.py:1213-1329`), sends
  `--json-schema` via `build_claude_cli_args`'s `json_schema=` parameter
  (`claude_cli_command.py:73,87-89,100-101`). Support is proven only by the invocation: an
  unknown-option stderr is classified `config` by `_looks_like_unknown_json_schema_option`
  (`pingpong_provider.py:693-705`, read at `:1304`), explicitly instead of a capability read or a
  `claude --help` preflight (`claude_cli_command.py:115-119`).
- **Ollama planner, native, hardcoded.** `apps/cli/commands/job.py:825-842` calls
  `make_structured_planner(..., native_schema=True)` (`structured_planner.py:59-86`) unconditionally
  — the planner role is always `OllamaPlanner` here (`job.py:782`), so native mode is a decision
  by provider identity, never by a capability read.
- **Claude-CLI planner, fallback, by written rationale.** `ClaudeCliPlanner`
  (`packages/providers/claude_planner/provider.py:1-45`) states in its own docstring (lines
  19-28) that it states the schema in the prompt rather than via `--json-schema`, because "the
  flag's support is proven only by the invocation and can be absent" — the same uncertainty the
  reviewer path probes for at runtime, resolved here instead by never trying the native path.
- **Every other `run_structured_call` caller takes the fallback path by omission.**
  `run_structured_call` (`structured_outputs.py:112-178`) defaults `native_schema=False`, which
  selects `build_schema_prompt`/`schema_instruction` (`structured_outputs.py:76-93`) — the full
  schema duplicated into the prompt, plus one parse retry via `validate_response`
  (`structured_outputs.py:159-172`, at most one retry per `allow_parse_retry`, lines 147-149). No
  caller below passes `native_schema=True`:
  `job_plan.py:494`, `mission_dossier.py:629`, `chat_answer.py:368`, `intake.py:245`,
  `dod_compiler.py:412`, `task_injection.py:629`, `orchestrator_loop.py:1207`,
  `chat_intent_model.py:119`, `artifact_summary.py:319`, `result_tour.py:792`,
  `mission_compiler.py:411`.
- **Tests:** `tests/orchestration/test_structured_outputs.py` (the engine, both prompt shapes, the
  retry ceiling), `tests/orchestration/test_structured_planner_cli.py` (the planner path),
  `tests/contracts/test_claude_cli_reference.py` (the adapter's declared `json_schema=True`).

### vision
**Not present today.** `grep -rln "vision\\b" packages apps --include="*.py"` outside tests hits
only the contract/kit/worker-show files already named, plus
`packages/orchestration/model_routing.py:245` — an unrelated name (see §6). No described-image
path, no native image-attachment path, and no consumer exists anywhere under `packages apps`.
No test covers a vision fallback because there is nothing to cover.

### session_resume
No call site reads `AdapterCapabilities.session_resume` either. A separate, pre-existing
per-provider-instance mechanism already does this job:

- **Native.** `supports_resume`, a property every `PingPongProvider` declares
  (abstract at `pingpong_provider.py:166`; concrete at `pingpong_provider.py:360`, `:1011`,
  `pingpong_provider_ollama.py:79-81`, `pingpong_provider_fake.py:71-72`,
  `local_endpoints.py:50`, `pi_provider.py:640`), read at `pingpong_loop.py:3084`, `:3422`,
  `:4756`, `tier_escalation.py:332`, and by `FailoverProvider.supports_resume`
  (`model_failover.py:489-492`, which also forces it `False` once a failover link has served a
  call — `self._resume_disabled`, line 477 — "a backup's session is never handed to the primary").
- **Fallback.** When a parked session is offered but `supports_resume` is false,
  `resume_declined_reasons` (`pingpong_loop.py:4750-4762`) names why — `resume_unsupported_reason`
  when the provider states one (`pingpong_provider_ollama.py:83-87`: "an Ollama chat call keeps
  no conversation between calls"), else a generic sentence. The loop then simply omits the resume
  ref and sends the full context fresh; there is no separately named "full-context resend"
  function — it is the ordinary no-resume call path. `session_sent_index.py` is dedupe
  bookkeeping for the opposite case, PROVEN sends on a session that DID resume (module docstring,
  `session_sent_index.py:8-11`); its `invalidate_on_resume_fallback`
  (`session_sent_index.py:238-`) is the one function that reacts to a resume falling back, called
  from `pingpong_loop.py:3306` (builder) and `:3630` (reviewer).
- **Tests:** `tests/orchestration/test_session_resume.py`, `test_claude_cli_resume.py`,
  `test_relaunch_session_resume.py`, `test_worktree_resume_cli.py`,
  `test_run_manifest_prework_resume.py`, `tests/cli/test_job_run_session_resume.py`.

### streaming
No call site reads `AdapterCapabilities.streaming`. Streaming is an opt-in CONFIG flag, not a
capability read:

- **Native.** `stream_evidence` (bool), read from job input (`job_input_definition.py:103,157`)
  through `execution_config.py:151,249,375` into `create_role_provider`
  (`role_provider_factory.py:76,106`) and `ClaudeCliProvider.__init__`
  (`pingpong_provider.py:893,907-908,921-922`). When true, `build_claude_cli_args` sends
  `--output-format stream-json --verbose` (`claude_cli_command.py:94-95`).
- **Fallback.** The DEFAULT (`claude_cli_command.py:86`, docstring): `--output-format json`
  (`claude_cli_command.py:96-97`), buffered, non-streaming.
- `ClaudeCliReferenceAdapter.capabilities().streaming` mirrors `self._streaming`
  (`claude_cli_reference.py:87`) but nothing couples that adapter instance's flag to the live
  `ClaudeCliProvider`'s own `_stream_evidence` setting — they are two separate objects today, so
  the mirrored value is cosmetic, not load-bearing.
- **Tests:** `tests/orchestration/test_stream_evidence.py`,
  `test_stream_evidence_integration.py`, `tests/cli/test_stream_evidence_tristate.py`,
  `tests/orchestration/test_claude_cli_command.py`.

### tool_use
No call site reads `AdapterCapabilities.tool_use`. The tools a call carries are fixed by
`write_mode`, unconditionally: `_READER_TOOLS`/`_WRITER_TOOLS`
(`claude_cli_command.py:27-28`) chosen in `claude_cli_launch_switches`
(`claude_cli_command.py:46-59`) by role and `write_mode`, never by a capability check. No
fallback exists because nothing degrades — every claude-cli call either gets its tool list or
runs with `--dangerously-skip-permissions` (`claude_cli_command.py:17,110-111`), a write-mode
choice made upstream of any capability. No test covers a tool_use fallback for the same reason.

### max_context_tokens
`AdapterCapabilities.max_context_tokens` is always `0`
(`claude_cli_reference.py:87`, comment at line 83) and no call site reads it — confirmed by the
same `.capabilities(` grep as §1. No native or fallback path exists; nothing truncates or resends
on a context-size decision keyed to this field. `tests/contracts/test_adapter_conformance_kit.py`
exercises it only as a type/sign check (non-negative int, `adapter_conformance_kit.py:109-115`).

## 3. Degradation evidence today

`EVENT_DEGRADED = "stream_degraded"` (`packages/orchestration/stream_evidence.py:72`) is a
DIFFERENT "degraded" than this feature's: it marks an internal failure of the stream-capture
machinery itself (e.g. an `on_cap` callback raising, `stream_evidence.py:447-453`, or a
post-close failure appended by `_append_degradation_events`, `stream_evidence.py:515-531`), never
a capability fallback. It is emitted twice, both inside `stream_evidence.py` itself (lines 453
and 529); `grep -rn "EVENT_DEGRADED\|stream_degraded" packages apps tests` finds no reader
anywhere — `adapter_contract.py:24,47` only imports/re-declares the constant in
`STREAM_EVENT_TYPES` (line 38-48), it does not branch on it.

`run_manifest.py`, `run_report.py` and `agent_run_trace.py` hold no "degrad" text at all
(`grep -n "degrad"` on all three: no hits) — **not present today**.

The word `degraded` is otherwise extremely busy in this tree for an UNRELATED sense — "a read
that could not be parsed, so the caller got a safe default instead of a crash" — at dozens of
sites (`load_job_plan_safe`, `list_missions_safe`, `list_job_plans_safe` and every caller of
them: `client_changes.py`, `client_digest.py`, `data_reclaim.py`, `project_brain.py`,
`repository_snapshot.py`'s `evidence_status` state machine at lines 964-992, `proof_chain.py:640`,
`apps/cli/commands/status_cmd.py`, `apps/cli/commands/event.py:163-164`, and more). None of these
is a capability degradation; §6 returns to the name collision this creates.

**The UI badge target does not exist in this repository.** `git ls-files apps/ui` returns nothing
tracked; `apps/ui/` on disk holds only `dist/`, `.data/`, `legacy/dist/` and `node_modules/` —
build output and a dependency tree, no source. `docs/ui/README.md:1-13` states plainly: "Since
2026-10-15 Remedy ships no web page. Its old cockpit, the React app under `apps/ui`, was deleted
(amend1015f D3 and D19)." (confirmed: `.agent/decisions.md:29859`, DECISION amend1015f D3).
Remedy's face is now "the universe's edition `remedy`", described by
`docs/roadmap/design/face-v1.md`, which lives in this repository and holds no badge, chip or
status-indicator reference (`grep -n "badge\|chip\|status indicator" docs/roadmap/design/face-v1.md`:
no hits) — the universe workspace that would hold such a component is a separate repository this
session cannot read. The design docs that DID govern a job-chrome badge,
`docs/archive/ui-target.md` and `docs/archive/operator-cockpit-v1.md`, are both marked DEPRECATED
in the index (`docs/README.md:213-214`).

## 4. The per-pair rule

A role's `(provider, model)` pair is resolved ONCE per role, before any call, by
`resolve_role_config` (`packages/orchestration/role_config.py:420-492`): CLI args, then config
file, then provider-aware defaults (lines 461-486), returning a `RoleConfig`.
`create_role_provider` (`role_provider_factory.py:25`) builds the concrete provider for that
pair and, when `with_failover` is true, wraps it in `FailoverProvider`
(`model_failover.py:447-507`), whose chain comes from `resolve_failover_chains()`
(`model_failover.py:286-311`, reading parsed links from `parse_failover_chains`, line 129).

A mid-job failover changes the provider: `FailoverProvider._call_link`
(`model_failover.py:509-537`) builds and calls each link in order on a trigger
(`is_failover_trigger`, line 346), and `__getattr__` (line 504-507) transparently proxies every
other attribute read — including a future `capabilities()` call — to whichever provider is
currently primary. Today nothing reads `capabilities()` through this proxy (§1); were a per-call
capability read added, the natural site is inside the provider that is about to build or send one
specific call (e.g. `ClaudeCliProvider.build`/`review` in `pingpong_provider.py`, or the bridging
point `worker_adapter_slot.adapter_cli_argv`, line 48) rather than at `resolve_role_config` time,
because the pair `resolve_role_config` resolves is the role's INTENDED pair, while `FailoverProvider`
can substitute a different one call-by-call without re-resolving the role.

## 5. Guard shapes

`tests/contracts/test_adapter_import_guard.py:1-30` is the closest existing shape for a
"consumers ask the matrix, never the adapter" rule: it walks every `.py` file under two
`GUARDED_TREES` (`packages/orchestration`, `packages/contracts`, line 21) with `ast.walk`
(function `import_guard_violations`, starting line 28) and fails on any import — top-level or
inside a function — of a `FORBIDDEN_PREFIX` (`packages.providers.adapters`, line 23) or a module
beneath it. A violation fixture would be a string literal module under a guarded tree that
imports the forbidden prefix; the test parses source text directly, so no fixture file need exist
on disk to prove the guard red.

`tests/orchestration/import_reachability_allowlist.txt` is GENERATED, never typed by hand (its
own header, lines 1-5): it is the measured closure of six entry points computed by
`tests/orchestration/test_import_reachability.py`, and `tests/test_no_orphan_modules.py:1-24`
is its mirror — a module under `packages/`, `apps/` or `scripts/` that nothing non-test imports
and no entry point names is an orphan. A new `capability_matrix.py` module must be imported from a
non-test site (or named as an entry point) in the SAME commit that adds it, or `test_no_orphan_modules`
reds.

`docs/system/structure-ledger-v1.md:1-31` pins, for every tracked file/function over the
ratchet's limits (100 lines/function, 1,000 lines/file — line 15), an exact row that
`tests/test_structure_ratchet.py` checks; a row may shrink or disappear but never grow (lines
22-27). T002/T003 touching any already-pinned row — `pingpong_loop.py`'s `run_pingpong` (1230
lines, structure-ledger-v1.md:308), `compose_builder_prompt` (211, :339),
`compose_reviewer_prompt` (184, :350); `run_manifest.py`'s several `validate_*` functions
(230-274 lines, :327-445); `stream_evidence.py`'s `capture_stream_evidence` (127, :407) and
`run_streamed_command` (142, :381) — must not add lines to that function; a new per-call
capability read belongs in a NEW module (which is also what a "no `packages/workers/`" clean
module gives for free — see §6) rather than inside one of these pinned bodies.

## 6. Names

`grep -rln "capabilit" packages apps --include="*.py"` (outside tests) hits exactly the files
already named in §1: `adapter_contract.py`, `claude_cli_reference.py`,
`adapter_conformance_kit.py`, `worker.py`. No other module, class, function or field spells
"capabilit" today.

`grep -rn "degrad" packages apps --include="*.py"` hits dozens of files (§3) — all the
read-safety sense, none the capability sense — plus the unrelated `stream_degraded` event (§3).
A new field literally named `degraded` on a run/job record would not collide on TYPE (every
existing one is a plain `bool` or `str`, same as this feature would want), but WOULD collide on
MEANING with the existing `degraded`/`evidence_status: "degraded"` convention
(`repository_snapshot.py:179,964-992`) that already means "this evidence read failed," not "this
call used a fallback."

`vision` already names an unrelated top-tier task class in `TASK_CLASS_TIERS`
(`packages/orchestration/model_routing.py:233-247`, entry at line 245) — "architecture / mission
/ vision / prompt authoring for other agents" (comment, line 242), i.e. product-vision writing,
nothing to do with image understanding.

`tool_use` already names the stream event type `EVENT_TOOL_USE = "tool_use"`
(`stream_evidence.py:63`), read at `agent_run_trace.py:185,230` and emitted at
`stream_evidence.py:325-338` — "the model invoked a tool mid-call," unrelated to whether the
model/provider CAN use tools at all.

`max_context_tokens` already names an operator-CONFIGURED token-budget ceiling in
`token_economy.py:187,198,228,269,449,720` and `apps/cli/commands/job.py:2308` — a policy cap the
economy enforces, not a model's native context window (which `AdapterCapabilities` declares and
nothing yet measures, §1). Same literal name, two unrelated meanings already, before this feature
adds a third reader.

`capability_matrix`, `require_or_degrade` and `FEATURE_REQUIREMENTS` grep to nothing under
`packages apps tests` — they appear only inside `docs/roadmap/ROADMAP.md:176` and
`docs/roadmap/features/T8_F157.md` itself (the plan describing them, not code). `packages/workers/`
does not exist: `ls packages/` lists `artifacts, common, contracts, core, memory, orchestration,
providers, runtimes, verification` — no `workers`. A module and names chosen to grep to
themselves only (AGENTS.md "Code Discoverability Conventions") therefore has a genuinely clean
slate for these four identifiers; DECISION F157 D2 picks the home and the field name for the
run/call evidence given this (the `degraded` collision above is the one constraint already found).

## 7. Draft register — a proposal for DECISION F157 D2, not a decision

One row per consumer found in §2. "Mode when absent" states what the consumer does today without
reading any capability; this feature's job is to make that same behaviour addressable by a
registered token, not to change it (DECISION F157 D1 (1), "no logic moves").

| Proposed feature key | Requires | Mode when the capability is absent | Existing fallback path | Call site | Covering tests |
|---|---|---|---|---|---|
| `schema_gate_reviewer` | `json_schema` | degraded: schema-in-prompt + 1 parse retry | `build_schema_prompt`/`schema_instruction` (`structured_outputs.py:76-93`) | `pingpong_loop.py:2469-2484`, `pingpong_provider.py:1213` | `tests/orchestration/test_structured_outputs.py` |
| `schema_gate_planner_ollama` | `json_schema` | native only — hardcoded, no fallback branch exists | `make_structured_planner(native_schema=True)` (`structured_planner.py:59`) | `apps/cli/commands/job.py:838-842` | `tests/orchestration/test_structured_planner_cli.py` |
| `schema_gate_planner_claude_cli` | `json_schema` | degraded: schema-in-prompt, by written rationale, never probed | `ClaudeCliPlanner` (`packages/providers/claude_planner/provider.py:19-28`) | same module's `plan_raw` | none found under `tests/` naming this class directly (deserves a T002/T003 check) |
| `schema_gate_general` (11 call sites) | `json_schema` | degraded: schema-in-prompt + 1 parse retry (same engine, default path) | `run_structured_call` default (`structured_outputs.py:112-178`) | `job_plan.py:494`, `mission_dossier.py:629`, `chat_answer.py:368`, `intake.py:245`, `dod_compiler.py:412`, `task_injection.py:629`, `orchestrator_loop.py:1207`, `chat_intent_model.py:119`, `artifact_summary.py:319`, `result_tour.py:792`, `mission_compiler.py:411` | `tests/orchestration/test_structured_outputs.py` |
| `session_resume` | `session_resume` | degraded: full-context resend (the ordinary no-resume call) | omission of `resume_ref`, named by `resume_declined_reasons` (`pingpong_loop.py:4750-4762`) | `pingpong_loop.py:3084,3422,4756`, `tier_escalation.py:332`, `model_failover.py:489-492` | `tests/orchestration/test_session_resume.py`, `test_claude_cli_resume.py`, `test_relaunch_session_resume.py` |
| `stream_evidence` | `streaming` | degraded: buffered `--output-format json` | `build_claude_cli_args` default branch (`claude_cli_command.py:96-97`) | `pingpong_provider.py:893-908`, `role_provider_factory.py:76,106` | `tests/orchestration/test_stream_evidence.py`, `test_stream_evidence_integration.py` |

No-consumer notes (every capability field in §2 that found no routed caller today):
- `vision` — no consumer at all (§2); any future image-attachment feature would be its first.
- `tool_use` — every call carries a fixed tool list by `write_mode`; no feature degrades on it.
- `max_context_tokens` — always `0`, declared, never read, never truncates or resends on it.

Where the feature file's design does not match the tree (facts, not decisions):
- `packages/workers/capability_matrix.py` (feature file, `T8_F157.md:35`) names a package,
  `packages/workers/`, that does not exist (§6); DECISION F157 D1 already defers the home to D2.
- The feature file's "UI badge on the job chrome" (`T8_F157.md:45,63-65`) has no live target:
  `apps/ui` is deleted (§3); T003's badge order needs a DECISION on whether it targets the
  universe workspace (out of this repository) or is deferred/dropped.
- `require_or_degrade(feature_key, adapter)` (`T8_F157.md:27`) imagines ONE function consulting
  ONE adapter's `capabilities()`; §2 and §4 show the live pair can change mid-job under
  `FailoverProvider`, so the real call signature needs the resolved pair, not just an adapter
  instance, confirming the feature file's own edge-case note (`T8_F157.md:75-78`) rather than
  contradicting it.
