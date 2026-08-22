# F009 inventory — the ground the single write channel builds on

Measured at the R2 round base `87ad9e5c` on branch
`feature/f009-single-write-channel`. Every claim below carries a `path:line`
citation into the source as it stands at that commit. Nothing here is read off
`docs/roadmap/features/T5_F009.md`; where this inventory contradicts the feature
file, the source is what was measured and the contradiction is carried to
`## Open questions for R3` rather than resolved here.

Counts described as "measured" come from an AST parse of the module named beside
them, not from a text grep. Absences name the exact command that established
them and the hit count it returned; hits inside `apps/ui/node_modules/` are
filtered out and that filtering is stated wherever it applied.

## Q1 The catalog

**Where it lives.** One module: `apps/cli/command_catalog.py:1-20`, whose own
docstring calls itself the "source of truth for Remedy's grouped CLI surface"
and states that every public CLI command has exactly one entry
(`apps/cli/command_catalog.py:2-5`). The catalog is a module-level tuple,
`CATALOG: tuple[CommandEntry, ...]` at `apps/cli/command_catalog.py:193`, closed
at `apps/cli/command_catalog.py:4801`. Three accessors form the public read API:
`get_group` at `apps/cli/command_catalog.py:4809`, `get_command` at
`apps/cli/command_catalog.py:4814` and `get_commands_for_group` at
`apps/cli/command_catalog.py:4822`.

**What declares an entry.** A frozen dataclass `CommandEntry`
(`apps/cli/command_catalog.py:72-87`) with fields `command_id`, `group_id`,
`subcommand`, `description`, `action_class`, `args`, `supports_json`,
`requires_permission`, `may_mutate_repo`, `may_execute_commands` and `related`.
`action_class` is a closed `Literal` of eight values
(`apps/cli/command_catalog.py:31-40`): `read_only`, `write_metadata`,
`approval_gate`, `apply_write`, `test_execution`, `dev_helper`,
`local_state_change`, `controlled_builder_execution`. Groups are a separate
`GroupDef` dataclass (`apps/cli/command_catalog.py:43-50`) held in a dict
`GROUPS` (`apps/cli/command_catalog.py:93-157`), and `GroupDef.user_facing`
(`apps/cli/command_catalog.py:50`) is the only visibility flag that exists — it
hides a group from default help, it does not restrict who may call it.

**Measured shape.** AST-walking the `CATALOG` tuple: **340** entries, **340**
distinct `command_id` values, spread over **60** distinct `group_id` values. By
`action_class`: `read_only` 204, `write_metadata` 107, `approval_gate` 10,
`apply_write` 7, `local_state_change` 5, `dev_helper` 3, `test_execution` 3,
`controlled_builder_execution` 1 — so **136** of the 340 entries are not
`read_only`.

**How arguments are described today.** Positionally and in prose, not by a
schema. Each entry's `args` is a tuple of `ArgDef`
(`apps/cli/command_catalog.py:53-69`) carrying `name`, `help`, `required`,
`is_option`, `default`, `is_flag` and `is_repeatable`. There is no type, no
enum, no pattern and no nested shape: `default` is typed `str | None`
(`apps/cli/command_catalog.py:61`) and every value is handed to argparse as a
string by `_add_command_args` (`apps/cli/grouped.py:63-70`), which reads
`arg.is_flag` to decide `store_true` versus a valued option. Searching the
catalog module for a declared type or schema returns nothing: the literals
`json_schema`, `schema=`, `type=` and `arg_type` occur 0, 0, 0 and 0 times in
`apps/cli/command_catalog.py`, against 587 occurrences of `ArgDef(`. The
comment at `apps/cli/command_catalog.py:62-69` records why per-argument
declaration exists at all — the same option name means different things to
different commands.

**Is a UI-exposed subset already declared?** No. `grep -rnE
"ui_exposed|UI_EXPOSED|ui-exposed|ui_subset|UI_COMMANDS" apps/cli apps/api
apps/worker packages/ --include=*.py` exits 1 with 0 hits. Nor does the UI
server know the catalog exists: `grep -rn command_catalog
packages/orchestration/ui_server.py` exits 1 with 0 hits. F009 would be
introducing the UI-exposed-subset concept, and it would also be introducing the
first import of the catalog into `packages/orchestration/ui_server.py:1-20`.
Both `job.stop` (`apps/cli/command_catalog.py:344-360`) and `decision.resolve`
(`apps/cli/command_catalog.py:2630-2643`) are present as entries, both classed
`write_metadata`.

## Q2 The current door

**The authentication, exactly.** `_RemedyHandler`
(`packages/orchestration/ui_server.py:3051`) carries a class attribute
`server_token: str = ""` (`packages/orchestration/ui_server.py:3054`). Inside
`do_GET` the token is read from the QUERY STRING — `token = (qs.get("token") or
[""])[0]` at `packages/orchestration/ui_server.py:3077` — and compared with a
plain `!=` at `packages/orchestration/ui_server.py:3078`, answering
`403 invalid token` at `packages/orchestration/ui_server.py:3079`. That
comparison is not constant-time; `secrets.compare_digest` does not appear in the
module. There is no separate authenticate function: the check is those three
lines inside `do_GET`, and it is the ONLY check — every API route below it
(`packages/orchestration/ui_server.py:3083-3195`) is reached with no further
authorisation.

**Where the token comes from.** `start_ui_server`
(`packages/orchestration/ui_server.py:3295-3303`) mints one per run with
`secrets.token_urlsafe(24)` when none is passed
(`packages/orchestration/ui_server.py:3318-3319`), binds it onto a subclass
built with `type(...)` at `packages/orchestration/ui_server.py:3325-3333`, and
publishes it inside the URL at `packages/orchestration/ui_server.py:3337` and
inside the optional info file at `packages/orchestration/ui_server.py:3346`. The
app shell itself is served WITHOUT a token
(`packages/orchestration/ui_server.py:3067-3069`), and static assets under
`/assets/` are served before the token check
(`packages/orchestration/ui_server.py:3072-3074`).

**The client half.** The React app reads job and token out of
`window.location.search` (`apps/ui/src/RemedyApp.tsx:8-11`) and refuses to load
without both (`apps/ui/src/RemedyApp.tsx:22`). Every request it makes is a GET:
`fetchJson` hard-codes `{ method: "GET", credentials: "same-origin" }`
(`apps/ui/src/api/remedyApi.ts:24-28`), the token is appended as a query
parameter (`apps/ui/src/api/remedyApi.ts:576`), and the brain-stream dependency
types its own fetch with the literal type `method: "GET"`
(`apps/ui/src/api/brainStreamDeps.ts:105`), so a POST there is a type error
rather than an omission.

**Bearer and CSRF.** Neither exists. `grep -rniE
"bearer|authorization|x-remedy-csrf|csrf" packages/orchestration/ui_server.py`
exits 1 with 0 hits. Repository-wide over `packages/ apps/` with
`node_modules` filtered out, every `Bearer` hit is a REDACTION pattern rather
than a parser — `packages/orchestration/stream_evidence.py:135`,
`packages/orchestration/provider_trust.py:535`,
`packages/orchestration/prompt_trace.py:28` and
`packages/orchestration/pingpong_evidence.py:33` — and `grep -rniE
"authorization|bearer|csrf" apps/ui/src apps/api apps/cli apps/worker` returns
nothing at all. F009 would introduce BOTH the bearer transport and the CSRF
double-submit, and it would be the first code in this server to read a request
header for authentication; today the only header read anywhere in the handler is
`Last-Event-ID` for SSE resumption
(`packages/orchestration/ui_server.py:3146`).

**The mutating verbs and the 405.** All three are one-line refusals on the
handler itself: `do_POST` at `packages/orchestration/ui_server.py:3226-3227`,
`do_PUT` at `packages/orchestration/ui_server.py:3229-3230` and `do_DELETE` at
`packages/orchestration/ui_server.py:3232-3233`, each calling
`self._send_json(*_safe_error(405, "method not allowed"))`. `_safe_error` is
`packages/orchestration/ui_server.py:235-236` and returns `(code, {"error":
message})` with no body detail. The refusal is BEFORE any routing and before the
token check, so today a 405 is returned for every path, authenticated or not,
and the handler docstring states the invariant plainly: "Read-only handler. No
POST/PUT/DELETE. Token-gated API."
(`packages/orchestration/ui_server.py:3052`). `do_HEAD`, `do_OPTIONS` and
`do_PATCH` are not defined, so those fall through to
`BaseHTTPRequestHandler`'s own 501.

## Q3 The effect backends

**stop — the "kill-switch control file" is real, and it is a per-job
control DIRECTORY holding one JSON file.** The module is
`packages/orchestration/safe_points.py:1`, whose docstring names it "F011 — the
kill switch's control protocol and safe points". The file is `stop.json`
(`packages/orchestration/safe_points.py:50`), placed under a per-job control
directory resolved by `control_root`
(`packages/orchestration/safe_points.py:199`), `job_control_dir`
(`packages/orchestration/safe_points.py:205`) and `stop_request_path`
(`packages/orchestration/safe_points.py:210`), with mode 0o700 on the directory
and 0o600 on the file (`packages/orchestration/safe_points.py:45-46`). The
WRITER is `request_stop` (`packages/orchestration/safe_points.py:348-386`);
publication is create-only via `os.link`, so two concurrent requests converge on
one request id rather than overwriting each other
(`packages/orchestration/safe_points.py:350-356`,
`packages/orchestration/safe_points.py:372-383`) — that is already the
idempotency property F009's nonce work needs for this one command. The readers
are `stop_requested` (`packages/orchestration/safe_points.py:389`),
`stop_status` (`packages/orchestration/safe_points.py:551`) and `should_stop`
(`packages/orchestration/safe_points.py:589`); the consumer side is
`acknowledge_stop` (`packages/orchestration/safe_points.py:449`) and
`consume_stop` (`packages/orchestration/safe_points.py:475`).

Invoked TODAY only from the CLI: `apps/cli/commands/job_stop_cmd.py:101` imports
it and `apps/cli/commands/job_stop_cmd.py:173` calls it, inside `_cmd_job_stop`
(`apps/cli/commands/job_stop_cmd.py:99`), wired to the catalog id `job.stop`
through `COMMAND_HANDLERS` at `apps/cli/commands/job_stop_cmd.py:192-200`. The
only other non-test reference in the repository is a prose cross-reference at
`packages/orchestration/job_queue.py:22`. So the backend is a clean, importable
function with no CLI coupling in its signature
(`packages/orchestration/safe_points.py:348-349`), and the CLI handler adds one
behaviour the function does not have: a terminal job is refused before the call
(`apps/cli/commands/job_stop_cmd.py:160-170`), which is exactly the
"validated then refused with the state named" edge case the feature file asks
for.

**decision answer — a package function exists and it is reusable.**
`answer_task_decision` at `packages/orchestration/escalation.py:277-299` takes
`(job, decision_id, *, answer, source, now)`, refuses a decision that is not
open and refuses to overwrite an answered one, returning `None` in both cases
(`packages/orchestration/escalation.py:291-293`). Its lookup helper is
`find_task_decision` (`packages/orchestration/escalation.py:171`), and
`auto_apply_safe_default` (`packages/orchestration/escalation.py:302-322`) is a
second caller. It does NOT persist: `apps/cli/commands/decision.py:251-253`
calls it and `apps/cli/commands/decision.py:262` calls `save_job` afterwards.
Invocation today is the CLI command `decision.resolve`, dispatched at
`apps/cli/commands/decision.py:377` into `_cmd_decision_resolve`
(`apps/cli/commands/decision.py:182-189`), which routes by decision-id PREFIX:
`sr:` to `resolve_stop_reason` (`apps/cli/commands/decision.py:207-214`), the
escalation prefix to `answer_task_decision`
(`apps/cli/commands/decision.py:215-266`) and `fp:` to the plan approval
(`apps/cli/commands/decision.py:267`).

**approve plan — there is NO reusable backend for the human path.** The effect
is written INLINE in the CLI handler: `fp["_approval"] = "approved"` at
`apps/cli/commands/decision.py:330`, with `fp["_approval"] = "rejected"` at
`apps/cli/commands/decision.py:349`, guarded by a check that the plan is pending
(`apps/cli/commands/decision.py:286`) and by a `--reason` that must be exactly
`approve` or `reject` (`apps/cli/commands/decision.py:300-307`), then persisted
with `save_job` at `apps/cli/commands/decision.py:332`. The only package-level
approval writer is `auto_approve_flight_plan`
(`packages/orchestration/flight_plan.py:729-754`), and it is the UNATTENDED
`--yes` path: it stamps `_approval_audit` with mode `auto_yes`
(`packages/orchestration/flight_plan.py:720-726`,
`packages/orchestration/flight_plan.py:752`) and deliberately does not persist
(`packages/orchestration/flight_plan.py:743-745`). Enumerating every writer of
that key repository-wide gives five sites and no sixth:
`apps/cli/commands/decision.py:330`, `apps/cli/commands/decision.py:349`,
`apps/cli/commands/do_cmd.py:277`, `packages/orchestration/flight_plan.py:751`
and `packages/orchestration/flight_plan.py:787`.

**What the "queues" named in the feature file actually are.**
`packages/orchestration/decision_queue.py:1-6` states it is "a read-only
aggregation" that derives decisions from existing records and is "Not a second
source of truth"; its public API
(`packages/orchestration/decision_queue.py:8-19`) contains no writer. So
"enqueue into the decision queue" has no target today — the write is
`answer_task_decision` against the Job record.
`packages/orchestration/approval_queue.py:1-6` is a DIFFERENT thing again: it is
metadata-only approval of PATCH INTENTS, stored under
`artifact.metadata["patch_intent_approvals"]`
(`packages/orchestration/approval_queue.py:25-29`), not flight-plan approval.

## Q4 The event seam

**The append.** The ledger is the append-only JSONL run log:
`packages/orchestration/run_log.py:1-8`, one event per line under
`<REMEDY_DATA_DIR>/runs/<job_id>/<run_id>.jsonl`
(`packages/orchestration/run_log.py:4-5`). The writer class is `RunLogWriter`
(`packages/orchestration/run_log.py:94`); the appending method is
`RunLogWriter.append` (`packages/orchestration/run_log.py:129-132`), which opens
the file in `"a"` mode and writes one serialized line plus a newline. The
ergonomic entry point is `RunLogWriter.log`
(`packages/orchestration/run_log.py:134-176`), which builds the event, stamps
`datetime.now(timezone.utc).isoformat()` at
`packages/orchestration/run_log.py:166` and folds unknown keyword arguments into
`metadata` (`packages/orchestration/run_log.py:174`). A one-shot convenience
wrapper exists at module level elsewhere: `append_run_event`
(`packages/orchestration/timeline.py:49-65`), which constructs a `RunLogWriter`
against `<data_dir>/runs` and calls `.log`.

**The reader the F008 stream uses.** `_load_events`
(`packages/orchestration/ui_server.py:154-160`) delegates to `load_run_events`
(`packages/orchestration/timeline.py:68-89`), which globs every `*.jsonl` under
`<data_dir>/runs/<job_id>/`, skips malformed lines and sorts by `timestamp`
(`packages/orchestration/timeline.py:79-88`). `iter_sse_frames`
(`packages/orchestration/ui_server.py:2778-2809`) polls that reader and yields
one frame per ledger position, and `_send_sse_stream`
(`packages/orchestration/ui_server.py:3197-3224`) is what drives it from the
route at `packages/orchestration/ui_server.py:3149`.

**Is an emitter reachable from an HTTP handler?** No. `grep -rnE
"run_log|append_run_event|RunLogWriter" packages/orchestration/ui_server.py`
exits 1 with 0 hits — the UI server module imports no writer, only readers, and
that is consistent with its read-only handler docstring
(`packages/orchestration/ui_server.py:3052`). F009 must introduce the emitter,
and the smallest correct seam is `append_run_event`
(`packages/orchestration/timeline.py:49`) because it needs only a data root and
a job id and it is already the one-shot form.

**The envelope's required fields.** There is no JSON Schema file for run
events; the schema IS the `RunEvent` dataclass
(`packages/orchestration/run_log.py:56-77`). Four fields have no default and are
therefore REQUIRED: `event`, `job_id`, `run_id`, `timestamp`
(`packages/orchestration/run_log.py:66-69`). Optional, defaulting to `None`:
`task_id`, `artifact_id`, `provider`, `role`, `model`, `outcome`, `message`
(`packages/orchestration/run_log.py:70-76`); `metadata` defaults to an empty
dict (`packages/orchestration/run_log.py:77`). Serialization drops `None`-valued
fields but always keeps `metadata`
(`packages/orchestration/run_log.py:79-86`). The SSE and cursor transports do
NOT carry that envelope: both narrow it through one writer,
`_safe_event_summary` (`packages/orchestration/ui_server.py:2747-2761`), to
exactly four keys — `seq`, `event`, `timestamp`, `outcome` — and the docstring
there records that a field added must reach both transports or neither
(`packages/orchestration/ui_server.py:2748-2754`). So a `command.accepted` event
would today surface to the UI as its `event` name and `outcome` only, with
`seq` taken from the ledger position (`packages/orchestration/ui_server.py:2757`,
`packages/orchestration/ui_server.py:2801`).

## Q5 Nonce, rate limit, audit

Each of the four searched separately; three of the four are absent.

**Nonce — ABSENT.** `grep -rniE nonce packages/ apps/cli apps/api apps/worker
tests/ --include=*.py` exits 0 with exactly ONE hit, and it is a false positive:
`tests/orchestration/test_worker_queue.py:169` is `class TestWorkerRunOnce:`,
matched case-insensitively on "RunOnce". `grep -rniE nonce apps/ui/src` exits 1
with 0 hits. `grep -rn client_nonce packages/ apps/cli apps/ui/src tests/` exits
1 with 0 hits. There is no nonce machinery of any kind to reuse.

**Replay window — ABSENT.** `grep -rniE "replay[_ -]?window|replay_window"
packages/ apps/ --include=*.py` exits 1 with 0 hits. The 186 hits for bare
`replay` are a different concept entirely: `packages/orchestration/event_replay.py:2`
is "Event Replay v1 — safe read model from run-log events", i.e. replaying the
LEDGER to derive state (`packages/orchestration/event_replay.py:130`), not a
request-deduplication window. Nothing there is reusable for nonce replay.

**Rate limit — EXISTS, but it points the other way.** The one implementation is
`packages/orchestration/rate_governor.py:1-9`, which normalizes PROVIDER
rate-limit/overload/throttle wording and paces OUTBOUND provider calls;
`ProviderRateGovernor` holds per-provider cooldown state and
`acquire`/`observe` are its methods (`packages/orchestration/rate_governor.py:59-69`).
It is keyed by provider, not by token or job, it waits rather than refuses, and
its call site is the provider retry seam
(`packages/orchestration/pingpong_loop.py:2219-2222`,
`packages/orchestration/pingpong_loop.py:2289`). The module also states it
deliberately does not coordinate across processes
(`packages/orchestration/rate_governor.py:14-17`) and does not fairly order
concurrent acquirers (`packages/orchestration/rate_governor.py:19-24`). For an
INBOUND per-token-and-job limiter there is nothing to reuse except the shape.

The nearest inbound limiter that does exist is the SSE slot cap:
`SSE_MAX_STREAMS_PER_JOB = 4` (`packages/orchestration/ui_server.py:2835-2837`),
enforced per job by `acquire_sse_slot`
(`packages/orchestration/ui_server.py:2843`) behind a module-level lock
(`packages/orchestration/ui_server.py:2839`) and answering 429 at the route
(`packages/orchestration/ui_server.py:3136-3140`). It is a concurrency cap, not
a rate over time, and it is not configurable — the value is a module constant.

**Per-job audit log — ABSENT under the feature file's name and under any other
name I searched.** `grep -rn commands_audit packages/ apps/cli tests/
--include=*` exits 1 with 0 hits; the only three occurrences of that string in
the repository are in roadmap feature files —
`docs/roadmap/features/T5_F009.md:50`,
`docs/roadmap/features/T5_F035.md:29` and
`docs/roadmap/features/T9_F167.md:27` — so F035 and F167 already plan to READ a
file F009 has not yet created. What exists instead is the run log itself
(`packages/orchestration/run_log.py:1-8`), which is per job and append-only but
is a run trail rather than a rejected-attempt audit, and a family of
`audit_*_safety` functions that are output-surface SCANNERS returning findings
rather than writers — for example
`packages/orchestration/token_economy.py:732` and
`packages/orchestration/managed_builder_execution.py:1585`.

**The redaction denylist — EXISTS, in two modules, and both apply.** The
narrower one is `packages/orchestration/redaction_patterns.py:1-13`, whose
public API is `FORBIDDEN_RAW_FIELD_NAMES`
(`packages/orchestration/redaction_patterns.py:24-32`),
`FORBIDDEN_SECRET_PATTERNS`
(`packages/orchestration/redaction_patterns.py:38-48`) and
`find_forbidden_surface_tokens`
(`packages/orchestration/redaction_patterns.py:67`); its secret list includes
the literal `token=` (`packages/orchestration/redaction_patterns.py:46`). The
broader one is `packages/orchestration/stream_evidence.py:104-154`, which
carries key-substring and exact-key denylists —
`packages/orchestration/stream_evidence.py:146-149` includes `authorization`
and `bearer`, and `packages/orchestration/stream_evidence.py:151-154` includes
bare `token`, `cookie` and `signature` — applied by `is_sensitive_key`
(`packages/orchestration/stream_evidence.py:161-177`) and `redact_text`
(`packages/orchestration/stream_evidence.py:180-189`). The docstring at
`packages/orchestration/stream_evidence.py:164-167` is the load-bearing part for
F009: bare `token` MUST be redacted while `input_tokens`/`output_tokens` must
not, and the rule that implements that distinction is
`packages/orchestration/stream_evidence.py:177`. A raw bearer token therefore
cannot be written to any surface these guard, which is why the feature file's
"token fingerprint" is the only writable form. The run log states its own
redaction policy in prose at `packages/orchestration/run_log.py:10-16`, but
enforces it by convention at the call site rather than by calling either
denylist — `grep -rnE "run_log|append_run_event|RunLogWriter"
packages/orchestration/ui_server.py` returning 0 hits is one half of that, and
`packages/orchestration/run_log.py:129-132` writing whatever it is given is the
other.

## Q6 The test home

**`tests/ui_contract/` does not exist.** `git ls-tree -d HEAD tests/ui_contract`
prints nothing and `ls -d tests/ui_contract` exits 2 with "No such file or
directory". The feature file's suggestion at
`docs/roadmap/features/T5_F009.md:90` names a directory this repository does not
have; the plural `tests/ui_contracts/` does exist and is a DIFFERENT surface.

**The two directories that do exist, and what they hold.** The convention is
written down at `tests/README.md:5-19`: `ui_server/` is "HTTP API: dashboard
contract, live state, brain view model, auth/redaction"
(`tests/README.md:12-13`) and `ui_contracts/` is "Python-verifiable frontend
contracts: graph architecture, UX quality gates, responsive layout"
(`tests/README.md:15-16`).

`tests/ui_server/` holds 13 test modules. Every one of them exercises the Python
server: the 405 discipline is already asserted twice, once as a unit against a
socketless handler (`tests/ui_server/test_cockpit_contract.py:15-35`) and once
over a really-bound `ThreadingHTTPServer`
(`tests/ui_server/test_live_state.py:246-268`); the SSE route, framing and
resumption live in `tests/ui_server/test_sse_stream.py:1-627`; sequence
numbering in `tests/ui_server/test_event_seq.py:1-92`; concurrency in
`tests/ui_server/test_server_concurrency.py:1-110`; redaction in
`tests/ui_server/test_prompt_trace_lens.py:1-167` and
`tests/ui_server/test_auth_redaction.py:1-113`.

`tests/ui_contracts/` holds 10 test modules and none of them touches the Python
handler; they assert facts about the React source and the design reference —
for example `tests/ui_contracts/test_brain_stream_hook.py:1-3` on the
`useBrainStream` hook, `tests/ui_contracts/test_design_drift.py:1-3` and
`tests/ui_contracts/test_main_layout_guard.py:1-3`.

**Where the contract test belongs: `tests/ui_server/`.** Three measured
reasons. It is the directory `tests/README.md:12-13` assigns to the HTTP API
including auth. The 405 route-walking test F009's T003 owes is an EXTENSION of
assertions already living there
(`tests/ui_server/test_cockpit_contract.py:22-35`), and splitting them across
two directories would leave the "every other verb answers 405" claim asserted in
two homes. And the harness the new tests need already exists there: `_dispatch`
at `tests/ui_server/test_sse_stream.py:171-187` builds a handler with
`_RemedyHandler.__new__`, sets `server_token`, `path` and `headers`, and
captures `_send_json` — the exact shape a POST-with-bearer-and-CSRF test needs,
and the reason a header-carrying test does not need a live socket. Under the
naming convention at `tests/README.md:68-72` the file would be
`tests/ui_server/test_command_channel.py`. Not created this round.

For T003's import guard, the reusable precedent is
`tests/test_no_interactive_guard.py:72-78`, an `ast.NodeVisitor` with
`visit_Import` and `visit_ImportFrom` that scans real files and keeps an
allowlist asserted empty (`tests/test_no_interactive_guard.py:131`).

## Open questions for R3

- Which directory name wins: the feature file says `tests/ui_contract/` (`docs/roadmap/features/T5_F009.md:90`), the repository has `tests/ui_contracts/` and this inventory argues for `tests/ui_server/`. R3 must rule it; nothing was created.
- "Approve plan" has no reusable backend — the human path is inline CLI code at `apps/cli/commands/decision.py:326-332`. R3 must rule whether F009 extracts a package-level function or whether the endpoint duplicates the guard sequence.
- "Enqueue into the decision queue" has no write target: `packages/orchestration/decision_queue.py:1-6` is a read-only aggregation. R3 must name the actual effect for the decision-answer command — presumably `answer_task_decision` plus `save_job` — and say what "queue-only side effects" then means for a test to assert.
- The audit record's home and format are unspecified in the source: `commands_audit.jsonl` exists nowhere (0 hits), while `docs/roadmap/features/T5_F035.md:29` and `docs/roadmap/features/T9_F167.md:27` already plan to read it. R3 must fix the path, the per-job location and the field set, because two later features depend on that choice.
- "Token fingerprint" is undefined: no fingerprint helper was found, and the denylist at `packages/orchestration/stream_evidence.py:146-154` forbids writing the raw value. R3 must rule the derivation and its stability under token rotation.
- The rate limit's key, window and configuration source are unruled. `packages/orchestration/rate_governor.py:1-9` is outbound and per provider, so nothing is inherited; the only inbound precedent is the hard-coded `SSE_MAX_STREAMS_PER_JOB` at `packages/orchestration/ui_server.py:2835-2837`, and the feature file says "config" without naming one.
- The nonce replay window's storage is unruled: the run log is append-only and per run (`packages/orchestration/run_log.py:4-5`), so a "seen nonce returns the ORIGINAL result" contract needs a store that can return a body. The create-only `os.link` idempotency at `packages/orchestration/safe_points.py:372-383` is the closest in-repo precedent.
- The auth pair's transport is unruled where it meets the existing one: the token is a QUERY parameter today (`packages/orchestration/ui_server.py:3077`, `apps/ui/src/api/remedyApi.ts:576`), and a bearer header for POST alone would leave two token transports in one server. Whether the GET routes migrate is a decision, not a measurement.
- Not settled and NOT investigated further this round, because it is outside the change set: whether the `!=` token comparison at `packages/orchestration/ui_server.py:3078` should become constant-time before a write channel sits behind it. Recorded here so R3 can route it rather than discover it late; no finding is minted by this file.
- One stale comment was measured while answering Q5 and is recorded so it is not re-derived: `packages/orchestration/rate_governor.py:26-28` says nothing outside the module and its test imports the governor, while `packages/orchestration/pingpong_loop.py:2219-2222` and `packages/orchestration/pingpong_loop.py:2289` do exactly that. It changes nothing for F009 and no id is minted here; R3 decides whether it is worth one.
