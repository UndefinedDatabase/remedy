# F315 T001 — the inventory of the claude-cli call path and its seams

Read-only investigation, read at `4747f2c67`. Every factual sentence names `path:line`. Section 7
is a proposal for DECISION F315 D2, not a decision.

## 1. What the provider does today

`ClaudeCliProvider` is the class at `packages/orchestration/pingpong_provider.py:881`, running to
the file's end at `:1574`. One row per method or code path:

- **`build()`** (`:1348`) / **`_build_impl()`** (`:1368`). BUILDS by calling `self._call(...)`
  (non-structured, single prompt, no schema). MAPS the raw text into `BuilderOutput`: a
  bullet-list heuristic reads `files_changed` out of the text, and the resume outcome and stream
  refs are attached. OWNS the exception-to-typed-error mapping on failure, via `_resume_refused_error`
  (`:762`) when a resume was requested and refused, and `_exit_detail` (`:753`) for the exit code
  and stderr tail.
- **`review()`** (`:1425`) / **`_review_impl()`** (`:1453`, 103 lines, a structure-ledger row —
  see §6). Two paths: the structured path calls `_call_reviewer_structured`; the legacy path
  appends `_REVIEWER_JSON_SCHEMA` to the prompt (schema literal near `:199`-`212`) and calls
  `_call`, then parses with `_parse_reviewer_json` (`:594`-`671`, builds the `malformed_output:`
  error on failure, `:620,631,645`) or, for the structured envelope, `_parse_reviewer_structured`.
  MAPS the verdict/findings/confidence through `_unwrap_envelope` and `normalize_reviewer_verdict`
  (`:523`). OWNS the same exception mapping as `build()`.
- **`_call()`** (`:1143`). BUILDS the argv via `build_claude_cli_args` (imported from
  `claude_cli_command.py`, see below) and runs it through `_guarded_cli_run` (`:856`, wraps
  `exec_guard.run_guarded`), called at `:1167`. MAPS the result text via `_extract_cli_result_text`
  (`:678`) and the usage via `token_actuals.parse_cli_result_detailed`. OWNS the
  `subprocess.TimeoutExpired`-to-`RuntimeError` translation and the nonzero-exit raise
  (`_CliNonZeroExit`, `:738`).
- **`_call_streamed()`** (`:1058`). BUILDS the same argv with streaming on; `_allocate_stream_call_dir`
  (`:992`) picks the per-call evidence directory at `:1083`. Delegates spawn/capture to
  `stream_evidence.run_streamed_command`, which OWNS the watchdog, the process-group kill and the
  byte cap (see `structure-ledger-v1.md:373`, 142 lines). MAPS via that module's usage/envelope
  helpers. OWNS re-raising `_StreamNonZeroExit` (`:769`) and the streaming-specific cap error.
- **`_call_reviewer_structured()`** (`:1214`, 133 lines, a structure-ledger row — see §6). BUILDS
  the same argv plus a JSON schema argument. MAPS the envelope (streamed or not) into a structured
  outcome, classifying a `config` failure (an unrecognized `--json-schema` option, detected by
  `_looks_like_unknown_json_schema_option`, `:696`, used at `:1308`) separately from a `parse`
  failure (native retry exhausted / missing `structured_output`) and from a raised provider error.
  Calls `_usage_actuals_dict` (`:711`) at `:1300`. OWNS nothing new; reuses `_guarded_cli_run`.
- **Session resume**: threaded as the `resume` kwarg into `build_claude_cli_args(...,
  resume_session=resume)`. `claude_cli_command.py:66` defines `build_claude_cli_args`; `:63` defines
  `_CLI_SESSION_REF_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z_-]{0,127}")`, checked at `:103` and
  raising `ValueError` when `resume_session` does not fully match. OWNED by the loop, which decides
  what `resume` value to offer; the provider only forwards it and classifies a refusal via
  `_resume_refused_error` (`:762`, called from `build`/`review` at `:1415` and `:1547`).
- **Parse retry**: not inside the provider. Per `docs/system/worker-adapter-contract-v2.md:18`, the
  reviewer's single parse retry on a `malformed_output:`-prefixed error is owned by
  `pingpong_loop.py`; the provider only produces that prefixed error (`pingpong_provider.py:566`,
  `:620`, `:631`, `:645`, `:1496`).
- **Transport retry, pacing, evidence booking**: owned entirely outside this class, by
  `packages/orchestration/pingpong_provider_call.py`. `_call_with_retry` (a structure-ledger row,
  140 lines, `structure-ledger-v1.md:370`) retries on timeout, nonzero exit and rate-limit, paced
  through a rate governor; `_record_attempt` books every real call as a `ProviderAttempt`. F315's
  feature file names this loop machinery as the explicit Do-not-touch.
- **Failure classification for post-mortems**: `packages/orchestration/failure_postmortem.py`'s
  `_classify_error_text` is the shared text predicate both the provider's wider classification path
  and `ClaudeCliReferenceAdapter.classify_claude_cli_error` call (see §2) — the same function, one
  definition, two callers.
- **Construction**: `create_provider(name, ...)` (`:1560`) is the bare-name factory; its
  `"claude-cli"` branch builds `ClaudeCliProvider` directly (see §3 for every caller).

## 2. The adapter's faces against those rows

`ClaudeCliReferenceAdapter` is defined at `packages/providers/adapters/claude_cli_reference.py:62`,
file ends at `:148`. Its module docstring (`:1`-`12`) states plainly: it wraps today's call path
and re-implements none of it; the loop still calls `ClaudeCliProvider` directly today and is not
rewired through it (that rewiring is this feature, F315).

- **`build_invocation()`** (`:90`-`107`). Reproduces the argv-build half of the provider's `_call`
  / `_call_streamed` / `_call_reviewer_structured`: it calls the *exact same* `build_claude_cli_args`
  (imported at `:26`) at `:101`. The write-mode rule it applies at `:96` (`write_mode =
  self._write_mode if role == "builder" else "none"`) is the same per-role rule
  `role_provider_factory.py:81`-`84` applies today (see §3) — restated explicitly here rather than
  read from that module. The JSON schema it builds at `:97`-`100` from `options.output_schema` is
  the same shape the provider builds ad hoc per call site (e.g. near `pingpong_provider.py:1469`
  before structured review), but built through `InvocationOptions` instead of a call-site literal.
  Differences: `InvocationOptions` (`packages/contracts/adapter_contract.py:74`-`80`) carries only
  `model`, `output_schema`, `resume_ref`, `max_output_chars` — "carries no timeout by construction"
  per its own docstring (`:75`) — so a caller using this adapter must resolve and pass
  `self._claude_path` (constructor default `"claude"`, `:68`) itself, where the provider resolves
  its own binary path via `shutil.which` and caches `_cli_version` (`pingpong_provider.py:1027`-`1037`,
  not reproduced here). `InvocationOptions` also carries nothing for `stream_evidence_dir`,
  `stream_rel_prefix` or `stream_counters` — the per-call evidence directory the provider allocates
  via `_allocate_stream_call_dir` (`:992`) has no face on this adapter at all; evidence placement
  stays entirely a loop/provider concern.
- **`map_stream()`** (`:112`-`123`). Reproduces the per-line mapping `_call_streamed` performs,
  built from the same `redact_stream_payload`/`normalize_stream_object` functions (imported from
  `stream_evidence.py` at `:28`) the provider's capture path uses. Difference: this method takes a
  `tuple[str, ...]` of complete lines handed to it after the fact, where the provider's
  `run_streamed_command` (`stream_evidence.py`, 142-line ledger row) captures incrementally,
  line-by-line, as the child process emits them, enforcing a byte cap and an `on_cap` termination
  hook during capture. The adapter cannot itself enforce that cap or terminate a live process — by
  construction, per the contract's rule that an adapter never opens a process (docstring `:6`-`9`;
  `worker-adapter-contract-v2.md` states the same rule for every adapter).
- **`map_usage()`** (`:127`-`138`). Calls the same `parse_cli_result_detailed` (imported at `:29`
  from `token_actuals.py`) the provider's `_call` uses, then separately re-parses the raw JSON to
  read `payload["usage"]` as `raw_counters` (`:132`-`137`) — an extra step versus the provider's
  `_usage_actuals_dict` (`pingpong_provider.py:711`), which already holds the parsed object and
  does not need to re-derive it. No functional gap found; same inputs, same answer shape
  (`AdapterUsage`, `adapter_contract.py:106`-`110`).
- **`classify_error()`** (`:142`-`143`) delegates to the module-level `classify_claude_cli_error`
  (`:42`-`59`), which calls `_classify_error_text` (imported at `:27`) — the same predicate the
  provider's wider failure classification reads. One method-only addition: a `malformed_output:`-
  prefixed text maps straight to `FailureClass.PARSE` (`:52`-`53`); the provider's own code produces
  that exact prefix (§1) but never calls this classifier on it today — this is new wiring the
  adapter supplies, not a reproduction of an existing provider code path. `ADAPTER_ERROR_CLASSES`
  (`adapter_contract.py:52`) excludes `IO_FAILURE`; a failure the shared predicates would read as
  I/O folds to `FailureClass.UNKNOWN` here (`classify_claude_cli_error:59`), where the provider's
  wider classification can still report it as I/O.
- **`capabilities()`** (`:83`-`86`) and **`isolation()`** (`:145`-`147`). No provider equivalent:
  `max_context_tokens` is always `0` ("nothing today measures a context size", comment `:82`), and
  `isolation()` always answers `None`, reserved for a later feature (comment `:145`).
- No adapter method validates session-resume itself; `resume_ref` passes straight through to
  `build_claude_cli_args` at `:104`, which performs the `_CLI_SESSION_REF_PATTERN` check
  (`claude_cli_command.py:103`) exactly as the provider's own call does, since both reach the same
  function.

## 3. Who builds the provider

`grep -rn "ClaudeCliProvider(" packages apps tests` finds exactly two PRODUCTION construction
sites, both under `packages/orchestration/`:
- `packages/orchestration/pingpong_provider.py:1568`, inside `create_provider` (`:1560`-`1574`).
- `packages/orchestration/role_provider_factory.py:82` and `:84`, inside `create_role_provider`
  (`:25`-`122`): the `"claude-cli"` branch (`:67`-`84`) builds `ClaudeCliProvider` directly and
  does not go through `create_provider`/`make_provider` for this name; `make_provider` (default
  `create_provider`, `:34`) is used only for the `else` branch (`:91`).

Every other `ClaudeCliProvider(` hit is a test construction, across roughly a dozen files under
`tests/orchestration/` (`test_claude_cli_command.py`, `test_pingpong_cli.py`,
`test_provider_evidence_integration.py`, `test_stream_evidence_integration.py`,
`test_session_resume.py`, `test_claude_cli_resume.py`, `test_claude_cli_exec_guard.py`,
`test_claude_cli_failure_detail.py`, `test_run_manifest.py`, `test_provider_mode.py`,
`test_relaunch_session_resume.py`, `test_structured_cli_envelope.py`).

**`create_role_provider` callers.** Defined `role_provider_factory.py:25`. Called from
`pingpong_loop.py:3928`, inside the shim `_create_provider_with_cwd` (`:3920`-`3928`, whose
docstring at `:3921`-`3927` states explicitly that it forwards `create_provider` as
`make_provider` so a test that replaces `pingpong_loop.create_provider` still reaches every
provider the module builds); and recursively from itself at `role_provider_factory.py:100` inside
the local `build_link` closure (`:99`-`111`), for one failover chain link. Both under
`packages/orchestration/`.

**`_create_provider_with_cwd` callers.** Defined `pingpong_loop.py:3920`. Called at `:2945`
(builder provider) and `:2948` (reviewer provider) inside `run_pingpong`, and passed by reference
at `:2959` into the tier-escalation ladder (`tier_escalation.py`). All under
`packages/orchestration/`. `tests/orchestration/test_role_provider_factory.py:152`-`168`
(`test_create_provider_with_cwd_reaches_a_create_provider_a_test_replaced`) proves this is already
a single observable funnel: it monkeypatches `pingpong_loop.create_provider` and calls
`pingpong_loop._create_provider_with_cwd("fake", role="builder", staging_dir=None)` directly,
confirming the fake reaches the caller unchanged.

**Entry points from which a job's builder/reviewer calls start**, all under `apps/` or
`packages/orchestration/`:
- `remedy job run` → `apps/cli/commands/do_cmd.py:484` (`_cmd_job_run`) → `run_job`
  (`packages/orchestration/pingpong_job.py:2444`) → inside `run_job`, `run_pingpong`
  (`pingpong_job.py:3415`) → `_create_provider_with_cwd` (`pingpong_loop.py:2945`/`2948`).
- `remedy do` → `apps/cli/commands/do_cmd.py` (`_cmd_do`/`_cmd_do_order`, `:155`/`:148` per the
  structure ledger's rows) → `packages/orchestration/do_sequence.py:484` (`plan_order_job`, which
  builds and plans the jobs) → `do_sequence.py:912`-`955` (`_run_the_walks_jobs`, the walker that
  actually runs each planned job) → `run_job(job_id, ...)` at `do_sequence.py:955` → the same
  `run_pingpong` → `_create_provider_with_cwd` chain as above.
- **The supervisor** imports no provider directly. `packages/orchestration/serve_runs.py:86`-`88`
  (`job_run_argv`) builds `[sys.executable, "-m", "apps.cli.main", "job", "run", job_id]`, and the
  `JobRunner` class (`:199`) `subprocess.Popen`s it at `:248`; `OrderLauncher` similarly `Popen`s
  `[..., "do", "run", ...]` at `:751`. The supervisor reaches `ClaudeCliProvider` only by
  re-spawning the CLI as a brand-new process, which re-enters the two entry-point chains above —
  `serve_runs.py` never imports `pingpong_provider` or a concrete adapter itself.
- **Failover links**: internal to the same seam. `role_provider_factory.py`'s `build_link`
  (`:99`-`111`) recursively calls `create_role_provider` with `with_failover=False`; there is no
  separate entry point for a failover link's provider construction.

## 4. Candidate seams

The guard (`tests/contracts/test_adapter_import_guard.py`) parses every `.py` file under
`packages/orchestration/` and `packages/contracts/` (`GUARDED_TREES`, `:21`) with `ast.walk`
(`:39`, which does not stop at a `FunctionDef`, so a function-body import is caught too, proved by
the fixture test at `:72`-`78`) and fails the test (`:68`-`69`) on any `import packages.providers.
adapters...` or `from packages.providers.adapters... import X`, including `from packages.providers
import adapters` (the join-by-dot case, `:47`-`50`, proved at `:86`-`88`). `FORBIDDEN_PREFIX =
"packages.providers.adapters"` (`:24`). The checker only reads literal `ast.Import`/`ast.ImportFrom`
nodes (`:40`,`:44`); it does **not** parse a dynamic `importlib.import_module(...)` call, which
would pass the guard's letter while violating the rule its module docstring states (`:4`-`12`:
a concrete adapter is reached "through the registry linkage... that only the wiring layer
[`apps/cli/commands/worker.py`] and each adapter's own tests import"). DECISION F315 D1 (landed in
this round's C1 commit) already names that dynamic-import route as REJECTED, "the dishonest
route" — proposals below do not reopen it.

Candidates, factually, marked as PROPOSALS (none chosen here):

- **(a) Widen the existing injection seam.** `create_role_provider` already takes `make_provider:
  Callable[..., PingPongProvider] = create_provider` (`role_provider_factory.py:34`), and
  `_create_provider_with_cwd` already forwards `pingpong_loop`'s own `create_provider` through it
  (`pingpong_loop.py:3928`). Today the `"claude-cli"` branch (`role_provider_factory.py:67`-`84`)
  does **not** go through `make_provider` at all — it constructs `ClaudeCliProvider` by name
  directly — so this branch itself would need to change to call something injected instead.
  **Where filled**: an `apps/`-layer caller would need to supply the adapter-backed callable; today
  nothing fills `make_provider` from `apps/` — `pingpong_loop.py` is the only caller of
  `create_role_provider`, so a new parameter would need threading through four more functions:
  `_cmd_job_run`/`run_job`/`run_pingpong`/`_create_provider_with_cwd`/`create_role_provider`.
  **Call paths carried**: every entry point in §3 (`remedy job run` and `remedy do` alike, since
  both bottom out at the same `run_pingpong` → `_create_provider_with_cwd` funnel).
  **Test observability**: a test that replaces the injected callable at the top of the chain (the
  same pattern `test_role_provider_factory.py:152`-`168` already proves reachable) would see every
  builder/reviewer call, because `_create_provider_with_cwd` is the single funnel every entry point
  passes through. **Cycle risk**: none by itself — the object or factory closure crosses the
  boundary as data; nothing under `packages/orchestration/` needs to import
  `packages.providers.adapters` to receive it.
- **(b) A registry-resolution step at the `apps/` boundary.** `packages/providers/adapters/
  adapter_registry.py` already resolves an `adapter_ref` to a concrete adapter for `remedy worker
  show`, reached only from `apps/cli/commands/worker.py` per the import guard's own docstring
  (`:6`-`7`). `packages/orchestration/` cannot import this registry directly (the guard's
  `FORBIDDEN_PREFIX` matches `packages.providers.adapters.adapter_registry` too). This is not a
  distinct seam from (a): the registry only decides WHICH adapter object `apps/` builds before
  handing it down; where orchestration *receives* it is still the (a) injection point.
- **(c) Dynamic string-based import inside `packages/orchestration/`.** Would pass the guard's AST
  check (it only matches literal `Import`/`ImportFrom` nodes, `:40`,`:44`) while violating the
  rule the guard's docstring states. REJECTED by DECISION F315 D1 already; recorded here only
  because the block asks every candidate to be named.
  Not viable: `ClaudeCliReferenceAdapter`'s own module imports FROM `packages.orchestration.*`
  (`claude_cli_command`, `failure_postmortem`, `stream_evidence`, `token_actuals`; imports at
  `claude_cli_reference.py:26`-`29`). Any seam where `packages/orchestration/` also imported
  something FROM the adapter module — even a shared base class or callback type defined there —
  would risk the import cycle the guard exists to prevent. `packages/contracts/adapter_contract.py`
  is the one place both sides already share types, and it already imports FROM orchestration
  (`FailureClass` from `failure_postmortem`, stream constants from `stream_evidence`, `UsageActuals`
  from `token_actuals`) — establishing contracts/orchestration as the side that may be imported BY
  the adapter, never the reverse. A seam filled by the adapter calling back into orchestration
  would invert that direction.

Seam (a) (with (b) folded into it) is the only candidate found that both respects the guard and
gives a test full observability of every builder/reviewer call, because it extends the existing
single funnel `test_role_provider_factory.py:152`-`168` already proves reachable, rather than
opening a second one.

## 5. The goldens and tests that pin today's behaviour

- `tests/contracts/test_claude_cli_reference.py` — the adapter's own goldens; docstring (`:1`-`7`)
  states it compares the adapter against the EXISTING functions it wraps (`build_claude_cli_args`,
  `parse_cli_result_detailed`, `capture_stream_evidence`, `_classify_error_text`), never a second
  re-derived notion of the call path. Must stay green unmodified: T002/T003 must not change what
  these wrapped functions return.
- `tests/orchestration/test_claude_cli_command.py` — pins `build_claude_cli_args`'s argv shape.
- `tests/orchestration/test_claude_cli_resume.py` — pins resume threading through `build`/`review`
  and `supports_resume`.
- `tests/orchestration/test_claude_cli_exec_guard.py` — pins `_guarded_cli_run`'s equivalence to
  the pre-exec-guard spawn, against a real fake-CLI subprocess.
- `tests/orchestration/test_claude_cli_failure_detail.py` — pins exit-code/stderr-tail propagation
  into `BuilderOutput`/`ReviewerOutput`.
- `tests/orchestration/test_pingpong_cli.py` — pins the staging-cwd binding for both roles and
  directly imports/calls `_create_provider_with_cwd`.
- `tests/orchestration/test_provider_evidence_integration.py` — pins `_call`'s JSON-usage parsing
  into usage actuals and its heuristic fallback.
- `tests/orchestration/test_stream_evidence_integration.py` — pins the streamed capture/mapping
  path end to end against a fake `claude` binary.
- `tests/orchestration/test_structured_cli_envelope.py` — pins native `structured_output` envelope
  handling against recorded envelopes.
- `tests/orchestration/test_structured_outputs.py` — pins the broader structured-output engine
  (builder/reviewer/planner) against fake providers.
- `tests/orchestration/test_token_actuals.py` — pins `parse_cli_result_detailed` parsing directly.
- `tests/orchestration/test_session_resume.py` — pins `supports_resume` across every concrete
  provider, `ClaudeCliProvider` included.
- `tests/orchestration/test_relaunch_session_resume.py` — pins that a relaunched/parked task's
  first calls actually resume.
- `tests/orchestration/test_role_provider_factory.py` — pins the `create_role_provider`/
  `_create_provider_with_cwd` seam itself, including the funnel-observability test cited in §4.
- `tests/orchestration/test_model_failover.py` — pins the failover walk calling `create_role_
  provider` correctly and reaching `_create_provider_with_cwd` per link.
- `tests/orchestration/test_provider_mode.py`, `test_provider_neutrality.py` — pin provider-name
  to class selection neutrality.
- `tests/orchestration/test_worktree_cleanup_paths.py`, `test_worktree_resume_cli.py` — pin
  cleanup/recovery around a provider-construction failure, monkeypatching
  `_create_provider_with_cwd`.
- `tests/orchestration/test_run_manifest.py` — pins provider fingerprints for `ClaudeCliProvider`
  calls into the run manifest.
- `tests/orchestration/test_job_stop_integration.py`, `test_failure_wiring.py`,
  `test_job_task_runner.py`, `test_self_use_runner.py`, `tests/cli/test_job_run_session_resume.py`,
  `tests/run_side_effect_counters.py` — broader real-loop integration tests that construct real
  `run_job`/CLI-dispatch paths with fake providers but assert on the same seams (funnel, retry,
  stop, resume wiring) T002/T003 would touch.

All of the above must pass unmodified after T002 and T003, per the block's requirement.

## 6. The structure ledger

Read at `docs/system/structure-ledger-v1.md`, which `tests/test_structure_ratchet.py` pins exactly:

- `packages/orchestration/pingpong_provider.py` — file row, 1574 lines (`:467`). Boundary named
  (`:248`-`254`): "the claude CLI's command line, the output contracts, the parsing of the
  reviewer's answer, the fake provider and the Ollama provider, each to a module of its own." Steps
  (1) `claude_cli_command.py` and (2) the Ollama provider and (3) the fake provider are already
  done; the remaining named pieces — "the output contracts" (`BuilderOutput`/`ReviewerOutput`) and
  "the parsing of the reviewer's answer" (`_unwrap_envelope`, `normalize_reviewer_verdict`,
  `_parse_reviewer_structured`, `_parse_reviewer_json`) — are exactly what T002/T003 touch. Since
  this file already has a row, the change must shrink it or route through a module door the
  boundary already names, not grow it (`docs/roadmap/features/T8_F315.md`'s own Do-not-touch names
  the structure ledger explicitly).
- `ClaudeCliProvider._call_reviewer_structured` — function row, 133 lines (`:388`). No boundary
  named in the ledger's "### Functions" prose (only functions a feature has already claimed or
  past 300 lines get a named boundary, per the ledger's own rule at `:39`-`40`). A direct T002/T003
  touch point: where structured-output mapping would move toward `map_usage`/`classify_error`.
  "No boundary named."
- `ClaudeCliProvider._review_impl` — function row, 103 lines (`:445`). "No boundary named," same
  reasoning; this is the body that would call `build_invocation`/`map_usage`/`classify_error`
  instead of `_call`/`_call_reviewer_structured` directly.
- `pingpong_provider_call.py::_call_with_retry` — function row, 140 lines (`:370`). "No boundary
  named." Not itself touched by F315 (the loop keeps owning retry per the feature file's Do-not-
  touch), but it is the direct consumer of whatever `build()`/`review()` return.
- `packages/orchestration/pingpong_loop.py` — file row, 4909 lines (`:457`), and `run_pingpong`
  function row, 1230 lines (`:300`). Both have named boundaries (file `:208`-`217`; function
  `:58`-`66`). The file's step (6), "the construction of the two role providers is one block whose
  two calls share their options," is marked done — that is the `_create_provider_with_cwd` pair at
  `pingpong_loop.py:2945`/`2948` §3 describes; filling the seam here extends an already-named block
  rather than opening an undocumented one.
- `packages/providers/adapters/claude_cli_reference.py` (148 lines), `packages/contracts/
  adapter_contract.py`, `tests/contracts/test_adapter_import_guard.py` — no file or function row;
  none are near the ledger's thresholds (100 lines/function, 1,000 lines/file). "No boundary
  named" because none are listed at all.
- `role_provider_factory.py::create_role_provider` (98 lines, `:25`-`122`) — under the 100-line
  threshold, not listed. "No boundary named."

## 7. Proposal (for DECISION F315 D2, not a decision)

The seam §4 narrows to (a): widen `create_role_provider`'s existing `make_provider` injection point
so the `"claude-cli"` branch (`role_provider_factory.py:67`-`84`) can be filled, from `apps/`, with
a callable that builds invocations through `ClaudeCliReferenceAdapter` and spawns/maps through the
loop's existing transport (`_guarded_cli_run`/`run_streamed_command`) rather than through
`ClaudeCliProvider`'s own `_call`/`_call_streamed`/`_call_reviewer_structured`. This is chosen over
a new, second funnel because `test_role_provider_factory.py:152`-`168` already proves the existing
funnel (`_create_provider_with_cwd` → `create_role_provider` → `make_provider`) is observable
end-to-end by a test that replaces one callable at the top, so T002 needs no new observability
mechanism — only a new object passed through the same channel. It also keeps `packages/
orchestration/` importing nothing from `packages.providers.adapters`: the `apps/` layer builds the
adapter instance (or a thin factory closing over it) and hands it down as plain data, the same way
`pingpong_loop.create_provider` is handed down today.

T002 would move the BUILD half of `build()`/`review()` — the argv construction `_call`/
`_call_streamed`/`_call_reviewer_structured` currently each redo — onto
`ClaudeCliReferenceAdapter.build_invocation`, while `_guarded_cli_run`/`run_streamed_command`
keep spawning exactly as today (unchanged, so every goldens test in §5 that asserts on spawn
behaviour, exit codes or stream capture keeps passing). The MAP half — usage, stream events, error
classification — would move onto `map_usage`/`map_stream`/`classify_error`, called with the raw
process output the loop already has. What becomes a duplicate and retires: once both halves route
through the adapter, `ClaudeCliProvider`'s own copies of argv assembly inside `_call`/
`_call_streamed`/`_call_reviewer_structured` and its own usage/stream mapping become the adapter's
functions called a second way, and should retire in favor of one call, per the Replacing-is-
deleting rule in `AGENTS.md`; `_parse_reviewer_json`/`_parse_reviewer_structured`/
`normalize_reviewer_verdict` stay, since they operate on the loop's own verdict shape, not on
anything the adapter's contract maps.

T003 would carry session-resume and the parse-retry signal through the same seam: `resume_ref` is
already an `InvocationOptions` field (`adapter_contract.py:79`) the adapter already threads
(§2), so T003's work is mostly making `_review_impl`'s retry read the adapter's
`malformed_output:`-classified `FailureClass.PARSE` (already produced by `classify_claude_cli_error`,
`claude_cli_reference.py:52`-`53`) instead of pattern-matching the raw string itself, and retiring
whichever of `ClaudeCliProvider`'s own classification branches become unreachable once the adapter
is the single classifier called.

The test that replaces the adapter and sees the loop follow it: extend
`test_role_provider_factory.py`'s existing pattern (`:152`-`168`) with a fake
`ClaudeCliReferenceAdapter`-shaped object injected at the same `make_provider`/new-parameter seam,
asserting that a full `run_job` for a `claude-cli` role calls the fake's `build_invocation`/
`map_usage`/`map_stream`/`classify_error` for every builder and reviewer call the job makes,
exactly as `test_role_provider_factory.py:152`-`168` already proves `create_provider` is reached
for the whole-provider case today.
