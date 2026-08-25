# Decisions

## 2026-08-03: F071 R3 — gate evidence is written OUTSIDE the repo during the run
The first branch gate run wrote its log to `.agent/gate_f071_r3/branch_run.txt`
inside the repo and reported four failures — two in
`test_run_manifest_logical_identity.py`, two in
`test_job_rerun_workspace_identity.py`. All four compare
`remedy_worktree_digest` values, and the log was being appended to WHILE the
suite ran, so the worktree digest genuinely changed mid-run. The tests were
right; the harness was wrong.

Re-running with the log in the session scratchpad and copying the evidence into
`.agent/gate_f071_r3/` after both runs finished: 15383 passed, exit 0, zero
failures.

`docs/agents/integration_gate.md` constrains evidence NAMES (`.txt`, never
`.log` — R-0169) but says nothing about evidence LOCATION during the run. No
doc was amended here: authoring gate-procedure amendments is the reviewer's
call, so the observation is recorded in `.agent/gate_f071_r3/attribution.txt`
and in the handback for the reviewer to register or discard.

## 2026-08-03: F071 R3 — the version fast-forward, the ONE exception to one-update-one-version
The R1 decision "one update produces exactly ONE version" still describes the
normal path and is still pinned by a test. R-0175 found the case it does not
cover: `refresh_mission_dossier` writes `dossier_v<N>.md` before
`dossier_state.json`, so a process that dies between the two leaves the archive
one ahead of the live state. The next refresh then recomputes a version number
the archive already holds, and — as soon as any fact has drifted, which one new
ledger entry is enough to cause — the R-0173 never-overwrite guard raises. It
raises again on every retry: the mission is wedged until a human deletes
evidence files.

Three options were available and two are wrong. Making the guard lenient would
undo R-0173 and let audit evidence be destroyed. Writing the state file first
would only move the tear (state ahead of archive, a version number silently
skipped, and a rendered document no archived file matches). So: RECONCILE
before writing. `latest = latest_dossier_version(...)`; if the updated
dossier's version is `<= latest`, fast-forward it to `latest + 1`.

What this costs: in a torn run one version number is consumed without a
corresponding update, so version numbers are a monotonic high-water mark rather
than an update counter. What it buys: the archive stays append-only, the
never-overwrite guard stays intact and untouched, and a torn write HEALS on the
next refresh instead of wedging the mission. That trade matches the module's
own stance elsewhere — `load_dossier_state` treats an unreadable state file as
absent for exactly the same reason: degraded, but never a dead loop.

The failure class is the one the F075 gauntlet names (harness death mid-write,
operator addition 2026-08-03); the reconcile is what makes this module survive
it rather than merely detect it.

## 2026-08-03: F071 R2 — the compression rule check judges the REBUILT document
R-0172's root cause was a mismatch of levels: the check read the answer's raw
id lists while `_rebuild` carried items PER SECTION, so an open risk returned
under `milestones` satisfied the check and then vanished from the rebuild. The
fix is not a bigger check but a check at the right level — `_check_rules`
builds the document first and judges THAT, and `compress_dossier` returns the
very object that was judged. `compression_rule_violation` keeps its signature
and delegates, so the public predicate and the compressed result can never
disagree.

General form worth keeping: validate the artifact you are about to write, not
the message you received. A check on the input passes for reasons the output
does not share.

## 2026-08-03: F071 R2 — a stored dossier version is immutable, and retries are free
R-0173: `write_dossier_version` promised versions are never overwritten and
then overwrote unconditionally. Two behaviors were possible; both are wrong
alone. Refusing every rewrite makes an idempotent retry an error; allowing
every rewrite destroys audit evidence. So: byte-identical rewrite is a no-op
returning the path, differing content raises `ValueError` naming the path and
the version, and the original bytes are left intact.

## 2026-08-03: F071 T003 — the live state is JSON; the markdown is the audit trail
The dossier reaches disk as `dossier_v<N>.md` for humans to diff. The next
iteration needs the STRUCTURED document back, and parsing the markdown would
make the state a hostage of the renderer — a formatting change would silently
alter recovered facts. So `dossier_state.json` holds the live state and the
markdown versions stay a pure projection. An unreadable state file reads as
ABSENT, not as an error: a mission then starts a fresh dossier from its own
goal, which is degraded but never a dead loop.

## 2026-08-03: F071 T003 — the loop's compression provider is a SEPARATE seam
F070 records "one provider call per iteration". A compression call would be a
second one, so `update_mission_dossier` takes `call_fn` and DEFAULTS IT TO
NONE: out of the box an over-budget dossier keeps its honest flag rather than
spending a call the loop's budget never authorized. Compression is opt-in by
the caller that wants to pay for it. The wiring itself is two lines — the
`dossier` seam of `assemble_context` already existed and was built for this.

## 2026-08-03: F071 T003 — the recall harness lives in the package, not the tests
The feature file names the harness a deliverable other features reuse (F079).
A harness only the test file can reach is not a deliverable, so
`run_recall_harness`, `RECALL_FIXTURE_FACTS` and `recall_report` are public in
`mission_dossier`. It reports PER FACT — answerable, missing, compressed away —
and `recall_report` deliberately prints no verdict word: the asymmetry between
open facts (must survive) and resolved ones (may compress away) is the
measurement, and collapsing it to pass/fail would hide it.

## 2026-08-03: F071 T002 — the compression contract has NO goal field
"Never drop the goal" is one of the three verbatim compression rules. A rule
that only ever appears in a prompt is a hope. `DossierCompression` therefore
declares `milestones`, `risks`, `decisions` and `next_step` and nothing else:
the provider has no channel through which to change, shorten or omit the goal,
and `_rebuild` copies the goal from the dossier that went in. Same idiom as
`OrchestratorMove` — the authority boundary is the schema's shape, not its
prose. The other two rules ("keep every open item", "merge resolved risks
away") CANNOT be expressed as absent fields, so they are enforced after
validation by `compression_rule_violation`, which refuses the answer and hands
the caller the honest over-budget fallback.

For the same reason the answer carries TEXT only, no state field: a compression
cannot promote a milestone to done or reopen a closed risk. `resolved` and
`outcome` are carried over from the previous dossier by id.

## 2026-08-03: F071 T002 — exactly one call, no parse retry
The feature specifies ONE compression provider call. `run_structured_call` is
used with `allow_parse_retry=False`, so "one call" is true of the code and not
only of the prose. A retry would buy nothing here: the fallback is already a
complete, correct, honestly-flagged document, so there is no partial result to
salvage. This is the deliberate difference from the mission compiler and the
orchestrator loop, which both allow the single retry.

`dossier_compress_draft_v1` is NOT registered in `schemas.models.SCHEMA_REGISTRY`
— the same call the `dod_draft_v1` / `mission_plan_draft_v1` precedents make. A
compression answer never leaves this module and is never persisted under its
tag; what reaches disk is the rewritten dossier markdown.

## 2026-08-03: F071 T001 — the budget counts on the labeled ESTIMATE basis
P6 says label the counting basis and never invent a counter. The dossier's size
is counted through the EXISTING seam, `token_economy.estimate_text_tokens`, and
every count travels as a `DossierTokenCount` carrying `basis` and the actuals
feature's own confidence vocabulary (`low` — F003 established that a count with
no provider-measured usage behind it is a character heuristic).

What was deliberately NOT done: using a provider call's `UsageActuals` as the
dossier's token count. Those actuals measure a whole prompt, not this document,
so reporting them as the dossier's size would be a more authoritative-looking
number that is not about the thing it names. A call's measured actuals are
recorded separately, as that CALL's cost, through the existing
`orchestrator_loop.measure_call_cost`.

The over-budget FLAG is likewise excluded from the counted body: counting it
would make the budget check depend on its own previous verdict.

## 2026-08-03: F071 T001 — one update produces one version
`update()` advances the version by exactly one, whether or not a compression
ran. The alternative — a second version for the compressed rewrite — would let
a reader diff pre- against post-compression directly, but it makes "the live
prompt uses the newest" ambiguous within a single iteration. Version N-1 is
still on disk, so `diff dossier_v<N-1>.md dossier_v<N>.md` shows what the
iteration appended AND what the compression dropped, which is the audit the
feature asks for.

## 2026-08-03: F070 T003 — `mission run` gains a MODE, it does not replace one
`remedy mission run` already existed: a facade over the dogfood run loop
(`dogfood_run.run_mission_loop`), keyed on a RUN id, covered by
tests/cli/test_worker_facade_cmd.py. F070's feature file mandates the same
spelling — `remedy mission run <id> [--iterations N]` — for the orchestrator
loop, keyed on a MISSION id. Same collision F047 hit with `job resume`
(2026-07-26), same resolution: ONE command, two modes on the same name, and a
test asserting the catalog registers `mission.run` exactly once.

The discriminator is RESOLVED, never guessed from the id's shape: if the
positional names a mission record in the selected project, the orchestrator
loop runs; otherwise the pre-F070 facade runs untouched. Every failure to
resolve (no project, no mission area, ambiguous prefix) means "not a mission",
so the older path stays the default in every uncertain case and no existing
invocation changes behavior. `--iterations` and `--no-llm` are additive and
apply to the mission mode only.

`remedy mission ledger <id>` is a new command id with no collision, read-only,
beside `mission show`.

## 2026-08-03: F070 T003 — `make_structured_call_fn` gained an optional model
The CLI must build the orchestrator's provider call through the SAME factory
the mission plan command uses (ordered), and `orchestrator.model` must
actually select the model — otherwise the config key documents an intention
rather than a behavior. The factory took no model, so it gained an OPTIONAL
`model=` that forwards to `OllamaPlanner(model=...)`. Omitted, every existing
caller resolves the model exactly as before; the parameter's only production
user is the orchestrator role. This is a config surface, not a routing-policy
change — `docs/agents/model_routing_policy.md` is still untouched.

## 2026-08-03: F070 T003 — iteration numbering belongs to the MISSION
Found by the e2e fixture, not by review: a mission run twice left a ledger
numbered 1,2,3,4,1,2,3. `next_iteration_index` now reads the highest number on
disk and the loop starts one past it, exactly as F047 fixed cycle numbering
(`long_run_executor.next_cycle_index`, decisions.md 2026-07-26) after a
resumed run overwrote the killed process's records. `step` still counts the
current invocation — that is what `limits` bounds and what
`MissionRunResult.iterations` reports.

## 2026-08-03: F070 R1 — the branch was rebuilt to keep every commit under 500 lines
Two commits landed over the AGENTS.md 500-line limit — the context-assembly
commit at 541 and the era-corpus commit at 712 changed lines. AGENTS.md allows a
declared oversize commit only when it is the ONLY one in its feature, and
neither was inseparable, so they were split rather than declared.

The branch was rebuilt from `170e2691` and force-pushed (it had no PR and no
other consumer). Each oversize commit became two: protocol reader + move-schema
tests / context assembly, and era detectors + fixtures / era detector tests.
The evaluate-step commit was split the same way when it measured 506. Proof
that nothing was lost: `git diff f070-oversize-backup HEAD` is EMPTY — the
rebuilt tip is byte-identical to the pre-rebuild tip. The backup branch existed
only to carry that proof and was deleted once it passed; both facts are in the
handback's external actions.

## 2026-08-03: F070 T002 — milestone attribution is read from the loop's OWN ledger
The evaluator has to know which job served which milestone, and the mission
record cannot say: `MissionJobLink` carries a job id, a role and a timestamp,
and F069 recorded (2026-08-02) why adding a milestone id there would mean
changing job creation.

It does not have to. Every `dispatch_job` ledger entry ALREADY stores the
milestone id (in the move payload) beside the job id it produced (in the
outcome), because the ledger records the whole decision. `dispatched_job_for`
reads the attribution back out of the loop's own artifact. Cost: none — job
creation stays exactly as F056 left it, and no schema moves. Limit: a milestone
dispatched outside the loop is invisible to it, which is correct — the loop
evaluates what the loop decided.

## 2026-08-03: F070 T001 — the CLI is deferred to T003, deliberately
The order permits `remedy mission run <id> [--iterations N]` and
`remedy mission ledger <id>` to land in T003 if they fit more cleanly there,
and they do: T003 is the end-to-end round whose acceptance IS a mission running
unattended and a human reading its ledger, so the commands get exercised by
their own acceptance criterion instead of by a test written to have one. R1 is
already a fourteen-commit bundle; adding a CLI surface here would widen it
without the end-to-end fixture that gives the surface its shape.

Everything the commands need is public and stable now: `run_mission`,
`loop_limits_from_config`, `read_ledger` and `render_ledger`. The deferral is a
routing choice, not a missing capability.

## 2026-08-03: F070 T001 — the protocol document lives in docs/agents/
`docs/agents/orchestrator_protocol.md`, registered in `docs/README.md`. The
orchestrator is a ROLE, and that directory already holds the role contracts
(`worker_conventions.md`, `reviewer_conventions.md`,
`planner_reviewer_prompt.md`). Putting the internalized orchestrator's job
description beside the human roles' own is what makes the A7 handover legible:
the same reader compares the two in one place.

The alternative, `docs/system/`, describes what IS BUILT; this document is an
instruction to a model, not a description of a mechanism. `packages/` was
rejected outright — a prompt in code is the thing this feature exists to stop.

## 2026-08-03: F070 T001 — `orchestrator` joins KNOWN_ROLES; routing policy untouched
The loop calls `resolve_role_config("orchestrator")`, and an unknown role there
warns (some tests run with `warnings.simplefilter("error")`), so the role is
registered. Its built-in defaults are deliberately IDENTICAL to every other
role's — `test_each_known_role_resolves` pins that — because raising the
orchestrator to a top-tier model is a CONFIGURATION act through the new
`orchestrator.model` key, not a change to
`docs/agents/model_routing_policy.md`, which this feature must not touch.

`tests/orchestration/test_role_config.py::test_all_six_roles_present` pinned
the tuple exactly and was renamed to `..._seven_...` with the new entry added.
Declared here rather than done quietly: a pinned contract test changed, and the
contract it pins genuinely grew by one role.

## 2026-08-03: F070 Phase 2 — the verb map (inspection only, no production code)
Recorded BEFORE any F070 code. Rule A6: the loop SEQUENCES these; a diff that
reimplements one is a defect. Every verb the order enumerates exists.

| Verb the loop needs | file:symbol |
|---|---|
| mission record load | `mission_state.py:load_mission` / `save_mission` / `resolve_mission_id` |
| mission plan read | `mission_compiler.py:mission_plan_of` / `plan_version_of` |
| mission plan write | `mission_state.py:set_mission_plan` |
| mission status write | `mission_state.py:set_mission_status` |
| mission↔job link | `mission_state.py:link_job_to_mission` / `mission_for_job` |
| dispatch a job into a mission | `mission_state.py:continue_mission` (creates the job, builds it verify-first, links it) |
| run a dispatched follow-up | `mission_state.py:execute_mission_followup` |
| intake | `intake.py:run_intake` (+ `heuristic_intake` fallback) |
| flight-plan generation | `flight_plan.py:plan_job_llm` → `map_flight_plan_to_tasks` |
| plan approval gate state | `flight_plan.py:flight_plan_blocks_execution` / `flight_plan_approval_open` |
| plan approval (human) | `apps/cli/commands/decision.py` `fp:approval` resolve path |
| plan approval (--yes / auto) | `apps/cli/commands/do_cmd.py:298-318` — INLINE, see the extraction note below |
| multi-cycle executor entry | `long_run_executor.py:run_cycles` (+ `limits_from_config`, `CycleLimits`) |
| DoD compile (F061) | `dod_compiler.py:compile_dod`; per-milestone wrapper `mission_compiler.py:compile_milestone_dod` / `attach_milestone_dods` |
| DoD evaluation | `dod_gate.py:evaluate_dod` / `run_job_gate` / `load_dod` / `load_gate_result` |
| report writer | `run_report.py:write_final_report` (+ `collect_report_sources`, `render_report`) |
| escalation | `escalation.py:enqueue_task_decision` / `answer_task_decision` / `open_task_decisions` / `answered_task_decisions` |
| open decisions view | `decision_queue.py:list_decisions` / `open_decisions` |
| postmortems | `failure_postmortem.py:write_postmortem` / `build_job_rollup` / `classify` |
| config lookup for a model role | `role_config.py:resolve_role_config` (+ `KNOWN_ROLES`); config keys via `config.py:get_config().get(<key>)` |
| stop-request check | `safe_points.py:stop_requested` / `should_stop` / `consume_stop` |
| structured call + schema registry | `structured_outputs.py:run_structured_call`; `schemas/models.py:SCHEMA_REGISTRY`; `schemas/validation.py:validate_response` |

Two gaps found by the inspection, neither of them a missing verb:

1. **`--yes` auto-approval is not a verb yet.** The semantics the loop needs
   (approve the flight plan, run every open clarification on its documented
   default, write the assumption log, stamp `_approval_audit.mode="auto_yes"`)
   exist only INLINE in `do_cmd.py`. A6 says extract, not copy — so it is
   extracted into `flight_plan.py` and `do_cmd.py` is switched to call it, in
   its OWN commit (AGENTS.md: never mix refactoring with a feature).
2. **The dossier does not exist.** F071 (Mission dossier) is unclaimed;
   `Mission.dossier_ref` is documented as RESERVED and is `""` on every record.
   The dossier is NOT in this phase's enumerated verb list, so this is not an
   If-Blocked stop — but the order still requires "dossier first" in the
   context prefix and a dossier update every iteration. Resolution below.

## 2026-08-03: F070 T001 — the dossier is a SEAM, not a document this feature invents
The loop takes a `dossier` callable (a port) and calls it first, so the
cache-stable prefix discipline is real from day one. Its DEFAULT renders the
facts the mission record already holds (goal, status, plan origin, milestone
outcomes, done/open counts) — it invents no new document, no new file format
and no new persistence, and it says on its face that it is a stand-in until
F071 lands. `Mission.dossier_ref` is read when non-empty and preferred over
the stand-in, which is exactly the hand-off point F071 plugs into.

The alternative — writing a dossier document here — would be building F071
inside F070 and would be the second mechanism A6 forbids.
Recorded as a declared assumption; flagged in the handback.

## 2026-08-03: F069 R2 gate — copying apps/ui/dist is necessary but not sufficient
The doc's §3 remedy (COPY `apps/ui/node_modules` and `apps/ui/dist`, never
symlink, plus `REMEDY_UI_NO_AUTO_BUILD=1`) was followed exactly, and eight
`tests/ui_server/test_live_state.py::TestUIServerIntegration` ids STILL failed at
base with "ERROR: React UI not built".

Cause, from the evidence: the base worktree's `apps/ui/dist/index.html` carries a
mtime LATER than the copy that created it (09:05 vs 09:03), so a UI auto-build
ran inside the base worktree DURING the run and rewrote `dist` while xdist
workers were reading it — `_get_frontend_dist()` sees no `index.html` for the
duration of the rewrite and `start_ui_server` refuses to start. This is the F053
R3 hazard (decisions.md 2026-07-31) with the blast radius contained: because
`dist` was copied rather than symlinked, the rewrite stayed inside the throwaway
worktree instead of reaching the primary checkout.

`REMEDY_UI_NO_AUTO_BUILD=1` did not prevent it. The variable is read by
`_auto_build_frontend`, so it stops the build the ui_server code path triggers —
but something in the base run still rebuilt. Worth a look before the next gate;
recorded here rather than chased inside a feature round.

Attribution was therefore done empirically, which is what §3 actually asks for:
with `dist` in place, `tests/ui_server/test_live_state.py` re-run AT BASE gives
42 passed / exit 0, so all eight `comm -23` ids are environment-class by direct
per-id evidence. They are base-only; `comm -13` (branch-only) was empty.

## 2026-08-02: F069 T003 — "in progress" is per-MISSION, because the record has no
## per-milestone attribution
The order's rule is "a milestone counts as in progress as soon as any real job
attributable to it exists on the mission record". The record cannot express
that attribution: `MissionJobLink` carries `job_id`, `role` and `created_at`,
and nothing else. Adding a milestone id to the link means changing job
creation — explicitly in this feature's Do-not-touch list.

The conservative reading was taken instead and documented at the rule's home
(`mission_compiler.milestones_in_progress`): once ANY job is linked to the
mission, EVERY milestone of its current plan counts as in progress, and a
recompile is refused. A mission with no plan yet has no milestones, so the
FIRST compilation is always allowed even when jobs are already linked. Erring
this way costs a refused recompile; erring the other way would rewrite the
route under work already running. Recorded as a declared deviation.

## 2026-08-02: F069 T002 — the milestone DoD goes through a flight-plan VIEW
Rule A6 makes `compile_dod` the only DoD mechanism, and it takes
`(intake, FlightPlan)`. A milestone is not a flight plan, so
`milestone_flight_plan` projects one: one task per `jobs_draft` outline, plus a
final task whose single acceptance line IS the milestone's outcome and which
depends on all of them. The projection is never persisted and never scheduled —
it lives for the length of one `compile_dod` call. The alternative was writing a
milestone-shaped DoD builder here, which is precisely the second mechanism A6
forbids.

## 2026-08-02: F069 T001 — `mission_plan_v1` needed the compact-tag exemption widened
`tests/orchestration/schemas/test_schemas.py::test_tags_are_compact` pins every
registered `schema_v` at <= 6 chars, with `flight_plan_v1` (14) as the one named
exemption. The F069 order fixes the tag as `mission_plan_v1` (15), so the guard
went red the moment the tag was registered.

Resolved by widening the NAMED exemption set to two entries and raising the
exempted bound to 15 — not by raising the general limit, and not by renaming the
ordered tag. Both exempted tags name a PLAN a human reads in evidence, where
`fp1`/`mp1` would be a riddle; every other tag still has to stay compact. The
guard's intent (tags travel in prompts, so keep them cheap) is intact, and the
exemption list stays a list a reviewer can read at a glance.

## 2026-08-02: F069 T001 — the MissionPlan schema is a LEAF module, like the DoD's
`mission_plan_schema.py` sits beside `dod_schema.py` and imports only
`structured_base` + pydantic, so `schemas/models.py` can import it to register
`mission_plan_v1` in `SCHEMA_REGISTRY` without a cycle. That registration is
required for the same reason the DoD's is: a `mission_plan_v1` payload is
PERSISTED (on the mission record), so its tag has to resolve from the registry
alone. `mission_plan_draft_v1` is deliberately NOT registered — it never leaves
the compiler's own call.

Consequence: the token-band literal is spelled out in the leaf rather than
imported from `schemas.models` (which imports this module). Same four bands,
documented at the definition.

## 2026-07-31: F053 R4 — `.agent/context.md` is pinned by TWO tests, not one
R-0162 was diagnosed as the "Steps" token, and the authored replacement fixed
exactly that: `test_context_md_no_stale_steps` passes and the whole
`test_dashboard_contract.py` file is green (70 passed). But `.agent/context.md`
is asserted on by a SECOND contract test in a different file:

    tests/regression/test_resource_safety.py:117
    TestContextIncludesResourceSafety::test_context_mentions_resource_safety
    assert "resource" in text.lower() or "pytest" in text.lower()

The authored text carries neither token (0 occurrences of each), so the full
suite went from one red id to a different one. The R1 version had passed this
test only incidentally — it carried a "## Gates" section naming pytest
commands, which satisfied the substring without anyone having decided to.

Not fixed in R4: the round block forbids further fixes after the first red, so
this is handed back for a corrected authored text. Recorded because the lesson
is bigger than the token: the state-file contract for a given file is spread
across at least two test files, and grepping only the one that just failed is
how a repair round produces the next red. Before authoring any `.agent` state
replacement, grep the whole suite for reads of that path — not just the test
that is currently failing.

## 2026-07-31: F053 R3 gate — base parity by symlink is defeated by the UI auto-build
The gate doc offers two ways to handle the environment-coupled base failures:
restore `apps/ui/node_modules` + `apps/ui/dist` parity in the throwaway base
worktree, or attribute every `comm -23` id by direct evidence. Parity was
attempted first, by symlinking both from the primary checkout.

It did not hold. The ui_server tests trigger an auto-build, that auto-build ran
`npm install` inside the base worktree, and npm REPLACED the `node_modules`
symlink with a real (partial, exit-217) install — so the base run failed the
same six ids anyway. Two consequences worth recording:

1. The symlink is also a WRITE path. The auto-build wrote through the `dist`
   symlink into the PRIMARY checkout's `apps/ui/dist`, rebuilding it. `dist` is
   gitignored so the repo stayed clean and `tests/ui_server/` still passes 259,
   but a throwaway worktree sharing a writable artifact directory with the
   primary is not the isolation it looks like. A copy, not a symlink, is the
   safer reading of the doc's "share or copy".
2. Attribution was therefore done properly instead, and empirically: with the
   symlink restored AND `REMEDY_UI_NO_AUTO_BUILD=1`, all six ids pass at base
   (17 passed). That is per-id direct evidence that none of them is a genuine
   base failure, which is what the doc actually asks for.

## 2026-07-31: F053 T002 — `remedy job report` gains modes, it does not replace one
`remedy job report <id>` already existed: a progress/evidence view with
`--json`, asserted on by tests/cli/test_open_decisions_view.py,
tests/orchestration/test_job_fulfillment.py and referenced as a next-action
string inside job.py itself. The R2 block asked for that command to render the
F053 run report, which would have changed the output of a covered command.

Resolved the same way F047 resolved the identical `job resume` collision (see
the 2026-07-26 entry below): ONE command, several modes on the same name.
`--final` and `--interim` render the F053 report; the bare invocation and
`--json` behave exactly as before. A test asserts the catalog registers
`job.report` exactly once and that the bare view still prints the pre-F053
output. The dispatch lambda is one line away from the replacement reading if
the reviewer prefers it; flagged in the handback rather than decided silently.

## 2026-07-31: F053 T002 — the report writer hangs off _apply_terminal
Every terminal transition in `run_cycles` already funnels through
`_apply_terminal`, so hooking the writer there makes "exactly one report per
terminal job" true by construction instead of by remembering to call a writer
on five separate break paths. `REPORTED_TERMINALS` names the five that end a
run; `max_cycles_reached` is deliberately excluded because it maps to
JOB_RUNNING — the job still has pending work, and a "final" report would lie
about the run being over.

The cost is that `_apply_terminal` now performs I/O. It is contained:
`write_final_report` never raises, records its own failure on the job under
`report_error`, and returns None. A run that finished is finished whether or
not its account could be written — the report is an account of the run, not a
gate on it. `write_report=False` keeps a terminal transition available without
a write, for callers that only want the state change.

## 2026-07-31: F053 T002 — the report file is overwritten, never appended
One fixed `report.md` in the job's evidence area, beside the `cycles/`
directory rather than in an area of its own. A resumed job that finishes again
REGENERATES the file, so it always describes the run as it actually ended
(feature-file acceptance). Red-proved in a throwaway worktree: switching the
write to an append fails three tests.

## 2026-07-31: F053 — the STATUS mirror is an INPUT, not a read (inspect finding)
The feature file states that ALL inputs already exist as structured data. The
inspect step disproved that for exactly one source: the milestone distance and
the capability lines are specified to come from "the STATUS mirror", and there
is NO production reader of `docs/roadmap/STATUS.md` anywhere in `packages/`.
The only production references to that path are a write FENCE
(`scope_fences.py:80`, "execution ledger (operator territory)") and a noise-
filter comment (`evidence_index.py:113`). `self_dogfood._detect_roadmap`
(self_dogfood.py:350) is registry-only by its own docstring — it tests module
existence, it does not read the ledger. Every other source the report renders
was confirmed present and is listed in the run_report.py module docstring.

Rather than write a STATUS parser inside a Tier 1 report feature (it is a
different concern, and the file is fenced operator territory),
`ReportSources.status_mirror` is the input seam and both dependent sections
render "not recorded" until a producer exists. That is the feature's own rule
for a missing source, applied to its own gap rather than papered over. The
routing of that producer — T002, a new slice, or a feature-file amendment — is
a reviewer decision, raised in the handback rather than decided by the worker.

## 2026-07-31: F053 T001 — render_report keeps its specified signature, plus a sources seam
`T1_F053.md` Design fixes `render_report(job, mode=final|interim) -> str`, but a
renderer that reaches for a job and a data root cannot have byte-stable
goldens. The module therefore splits in two: `render_report_from_sources` is
the pure function (no clock, no disk, no randomness — the caller supplies
`rendered_at`), and `render_report(job, mode, *, sources=None)` keeps the
specified signature and collects when nothing is injected. The goldens test
the pure half. Determinism is pinned by a double-render test rather than left
as a property nobody checks.

`collect_report_sources` deliberately reads ONLY the in-memory job this round.
The evidence-area sources (cycle records, postmortems, manifest) land with the
terminal-state writer in T002, so T001 adds no new disk reads and no new
failure modes to the run loop.

## 2026-07-31: F053 T001 — momentum is unknown with no cycles, never forward
The mechanical definition covers "closes items" and "recurs", but not the
zero-cycle case. Defaulting that to forward would print a green momentum line
for a run that produced no evidence at all — an invented judgement of exactly
the kind P6 forbids. `momentum_flag` returns `unknown` and the section renders
"not recorded".

## 2026-07-30: F052 — which existing repair loop the cycle triggers
The inspect step found TWO repair worlds. The ping-pong loop
(`pingpong_loop.run_pingpong`) does run bounded repair rounds, but it drives
them from its OWN reviewer inside one invocation, has no seam to inject
externally built findings, and belongs to the `pingpong_job.JobPlan` model —
none of its inputs (repo path, builder/reviewer providers, test command) exist
at the `run_cycles` seam, which works on `packages.core.models.Job`. The two
core-Job repair modules are human-gated PROPOSAL flows by explicit contract
(`repair_loop` v0/v1: "No real provider. No automatic apply. No test
execution."; `repair_loop_v2`: "NO model/provider/worker execution").

The loop that IS reachable and does execute is
`builder_bridge.run_builder_bridge_loop` — same core-Job world, takes a
`build_fn(repair_context) -> BuilderOutput` compatible with the cycle's
provider seam, already emits `repair_loop_cycle_started` /
`repair_context_created` / `repair_loop_succeeded` evidence, and already
consumes `repair_context.build_repair_context` findings. F052 therefore
TRIGGERS that loop with `max_cycles=1` per cycle-level round: the round cap
belongs to the cycle (`cycles.repair_rounds`) so the cycle can re-run its own
verify after each round, which the feature file requires. No second repair
mechanism was written (A6).

## 2026-07-30: F052 — CycleLimits.repair_rounds defaults to 0, the config key to 2
Defaulting the dataclass field to 2 silently turned every existing direct
`CycleLimits(...)` construction into a self-healing one, spending provider
calls the caller never asked for. The product surface goes through
`limits_from_config`, which supplies the configured default (2), so the shipped
behavior is the feature; a hand-built limits object gets exactly the bounds it
named. The divergence is deliberate and documented on the field.

## 2026-07-30: F052 R1 — the bundle was committed as four commits, not two
The T001+T002 diff came to 875 lines, over the AGENTS.md 500-line commit limit,
and it was genuinely separable rather than inseparable — so it was split into
four green steps instead of declaring an oversize commit: verify
classification, the repair seam + findings payload + cap, the loop trigger, and
the T002 assertions. Each step is independently green.

## 2026-07-26: F047 gate — live_review.md needs a real "## Steps" section
The integration gate produced exactly two reproducible branch-only failures,
both asserting `"Steps" in .agent/live_review.md`
(`test_test_runner.py::TestNoBroadExceptAndDegradedSignals` and
`test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs`). The base
passed them only by accident: F046's live_review.md happened to contain the
substring inside prose — the sentence about plan.md missing its "## Next
Steps" section. The F047 rewrite legitimately dropped that sentence and with
it the token.

Fixed as a declared state-file deviation, same class as F046's plan.md
"## Next Steps" repair at its own gate: live_review.md now carries a real
`## Steps` section listing the feature's rounds and their ranges. The
reviewer-authored finding and verdict text is untouched — the section is
purely additive. Nothing in the two tests was changed; the contract was met,
not weakened.

## 2026-07-26: F047 T003 — cycle numbering belongs to the JOB, not the process
The kill test's exactly-once assertion came out short (3 of 5 tasks), and the
cause was a real defect, not a test artifact: `run_cycles` numbered cycles
`len(cycles) + 1` within ONE invocation, so a resumed run started again at 1
and wrote `cycle_0001.json` / `checkpoint_0001.json` straight over the records
the killed process had left. The evidence area silently lost the pre-kill
history — precisely what F047 exists to preserve, and what makes exactly-once
unprovable.

Fix: `next_cycle_index(job_id)` reads the highest index already persisted (in
BOTH the cycles/ and checkpoints/ areas, since either can be switched off
independently) and the loop starts one past it. A `first_cycle_index` seam
lets tests pin an exact number. `max_cycles` is unchanged and still bounds one
invocation only. A fresh job still starts at 1, so nothing about F046's
single-pass default moves.

## 2026-07-26: F047 T003 — exactly-once is proven from evidence, not from counters
`CycleRecord` gained `executed_task_ids`. Without it there was nothing on disk
naming WHICH tasks a cycle ran, only how many — and a counter living in the
test process cannot see what the killed process did. The ids are written to
`cycles/*.json`, so the assertion spans both processes and reads only durable
state. A task that executed but failed verification is rolled back to PENDING
and will legitimately appear again in a later cycle; the field records
executions, not successes, which keeps it honest.

## 2026-07-26: F047 T003 — the torn checkpoint is written explicitly, on purpose
The atomic write (temp file, fsync, rename) makes a genuinely half-written
checkpoint impossible to produce on demand: a kill leaves either the old file
or the new one. Racing a SIGKILL against the rename to try would be a flake
generator. The test writes a truncated file instead, because the property
under test is that the LOADER survives one and falls back to the previous
valid checkpoint — identical either way, and deterministic.

## 2026-07-26: F047 `job resume` EXTENDS the existing command, it does not shadow it
`remedy job resume` already existed: an event-replay resume with a REQUIRED
`--checkpoint <id>`, handled by `_cmd_resume` (apps/cli/commands/job.py).
Adding a second catalog entry with command_id "job.resume" produced a
duplicate — `get_command` returned the new one while the dispatch dict's
later key silently kept the old handler. Caught by the T002 dispatch test,
not by any existing catalog test (nothing asserts command_id uniqueness).

Resolution: ONE command, two modes on the same name — which is also the
spelling the feature file mandates (`remedy job resume <id>`), and which
wraps the existing part rather than duplicating it (A6). `--checkpoint` is
now optional: given, the event-replay path runs completely unchanged; absent
(previously an argparse error, so no existing invocation changes behavior),
the F047 cycle-checkpoint path runs. The T002 suite pins both branches and
asserts the catalog registers "job.resume" exactly once.

The two "checkpoints" are genuinely different objects and the docstrings say
so: an event-replay checkpoint is DERIVED from run-log events; an F047
checkpoint is WRITTEN at a cycle boundary under the job's evidence area.

## 2026-07-26: F047 checkpoint record shape — pointer + self-verifying envelope
The record is `{"record": {...body...}, "content_hash": "sha256:<hex>"}`.
The hash covers the canonical encoding of the body only (sorted keys, no
incidental spacing), so it can be recomputed and compared without a second
source of truth. The body REFERENCES the persisted job snapshot (data-root-
relative path + sha256) rather than copying it — the persisted job already
is checkpoint v1; a checkpoint adds only what the job file cannot answer
(worktree head, spend, verify digest, next intent). An unreadable snapshot
yields empty path and empty digest: an unmeasured digest is reported as
unmeasured, never as a match.

## 2026-07-26: F047 load_latest_valid distinguishes "none" from "all corrupt"
`None` means the job was never checkpointed — the resume path degrades
honestly to plain continuation. `AllCheckpointsCorruptError` means
checkpoints exist and not one verifies, which is a louder and different
situation. Collapsing both into `None` would let a job whose entire
checkpoint history was destroyed silently resume as if it had never been
checkpointed. Skipped files are logged and LEFT ON DISK; retention never
prunes a file that does not verify, because a corrupted checkpoint is
forensic evidence and retention is not the mechanism that discards it.

## 2026-07-26: F047 inspection notes — the four parts this feature wraps (A6)
Recorded BEFORE any code was written; all four exist as the order describes.

1. Atomic write helper (temp file + fsync + os.replace):
   `packages/orchestration/storage.py::_atomic_write_job(path, data)` —
   same package, already the writer behind `save_job`. It is reused
   verbatim by `checkpoints.py`; no second atomic writer is introduced.
   (The repo has ~25 per-module `_atomic_write` copies; the storage one
   is the only text/JSON writer in the orchestration persistence layer,
   which is exactly what a checkpoint record is. The leading underscore
   is kept — renaming it would be a refactor mixed into a feature
   branch, and ruff's selected rule set (E,F,W,I,UP) has no private-
   member rule.) Note: F046's `write_cycle_record` uses a plain
   `path.write_text`; checkpoints deliberately do NOT copy that.
2. Cycle boundary hook: `packages/orchestration/long_run_executor.py`,
   `run_cycles` step 5 ("Persist the job, then the cycle's own evidence
   record", ~line 635) — after `save_fn(job)` and `write_cycle_record`,
   before `_emit(..., LEDGER_EVENT_CYCLE_COMPLETED, ...)`. That is where
   the checkpoint write attaches, so a checkpoint only ever describes a
   job state that is already persisted.
3. F046 cycle evidence area: `long_run_executor.cycle_evidence_dir` =
   `pingpong_job.job_evidence_dir(job_id) / "cycles"`, itself
   `data_paths.jobs_dir() / <job_id> / "evidence"`. Checkpoints go under
   the SAME area, sibling directory `checkpoints/`.
4. Resume-time checks to consume, not bypass:
   * pending stop request — `packages/orchestration/safe_points.py`:
     `stop_requested(job_id)` to detect, `consume_stop(job_id)` to
     archive + acknowledge in one go (the archive/acknowledge pair is
     what the job runner uses when it has something durable in between).
   * plan-approval gate — `packages/orchestration/flight_plan.py`:
     `flight_plan_blocks_execution(job)` returning "pending"/"rejected",
     used exactly as `_cmd_job_run_cycles` uses it in
     `apps/cli/commands/job.py` (exit 3 with the resolve/replan hint).
   Worktree head for the head-match check: the persisted job plan's
   `worktree_head` via `pingpong_job.load_job_plan(job_id)`; the live
   value comes from `worktrees.snapshot(handle)`. `packages.core.models.Job`
   has no worktree field — that is why the plan is the source.

## 2026-07-26: F034 answered_by stays human|default|""; "planner" is derived
The feature specifies exactly three answered_by values. A planner-declared
A9 assumption is neither human- nor default-answered, so it keeps
answered_by="" and is recognised by having a non-empty answer — the
assumption log derives the source "planner" from that shape
(clarification_source). This keeps the persisted contract as specified
while the log still distinguishes all three sources the golden test needs.

## 2026-07-26: F034 the planner echoing an intake question does not close it
carry_intake_clarifications treats the intake as authoritative for what is
open: an intake clarification always becomes an unanswered entry, even if
the plan echoed that same question back with an answer. Otherwise a model
that answers its own question would silently remove the human touchpoint.
Planner entries that are NOT intake questions are preserved as assumptions.

## 2026-07-26: F034 interactive-input guard is AST-based, not textual
A regex over source text flagged prose — "mission needs user input (e.g.
acceptance criteria)" in progress_ledger.py and a comment in
token_economy.py both matched `input\s*\(`. A guard that cries wolf gets
muted or allowlisted, which defeats it. The guard parses each module and
looks for real Call/Attribute/Import nodes, so the allowlist can stay
genuinely empty. Spacing tricks (`input ('x')`) are still caught.

## 2026-07-26: F034 conditional-answer predicates deliberately skipped
The feature file lists machine-checkable predicates over run state
(registered comparator set) as part of the clarification design. The
orchestrator brief and this round's scope mark them OPTIONAL. They need a
comparator registry, an evaluation point in the runner, and evidence
plumbing — none of which is trivially cheap, and none of which the DONE
criteria (unattended --yes with recorded defaults + guard test) require.
Skipped and recorded here; the rest of F034 does not depend on them.

## 2026-07-26: F016 clustering groups by matched FILE, not by raw path tokens
The feature file says "greedy grouping by shared files_hint tokens". Grouping
directly on token sets merges everything: `src/parser/core.py` and
`src/runner/loop.py` share the token "src", so every acceptance item in a
repo with a `src/` tree would land in one cluster and nothing would ever
split. An acceptance item therefore still MATCHES files by token overlap
(that part is unchanged), but two items group only when they matched the
same files_hint entry. File extensions are stripped before tokenizing for
the same reason — otherwise two unrelated `.py` files look related.

## 2026-07-26: F016 merge safety also refuses cycle-closing merges
The ordered rule is "no task OUTSIDE the run depends on a non-last member".
That rule alone does not prevent a cycle: if outside task X depends on the
LAST member and some member depends on X, contracting the group into one
node makes that node depend on itself. The T003 revalidation would catch it,
but aborting throws away the whole normalization for one bad group. The
merge step therefore checks per group whether the group's dependency
ancestors and dependents intersect, and skips just that group.

## 2026-07-26: F016 uses the "aborted" kind for a refused merge too
A merge that dependency safety refuses is recorded as kind="aborted" with a
reason starting "merge skipped: ...", the same kind the whole-plan
revalidation abort uses. The four kinds are fixed by the feature order
(split | merge | aborted | unsplittable_flag), so a refused merge either
reuses "aborted" or goes unrecorded; showing the approver what was
considered and declined is worth the shared kind, and the reason text
distinguishes the two cases.

## 2026-07-25: R-0116 — intake timeout removed; OllamaPlanner.raw_call is the single config surface
make_provider_call_fn previously hardcoded `timeout=15.0` on the Ollama client.
After R-0116, the function delegates to OllamaPlanner.raw_call, which builds
the client from `self.host` with NO explicit timeout — Ollama's default applies.
The `client.list()` health check in make_provider_call_fn still constructs its
own client (bare `ollama.Client(host=planner.host)`) for the availability probe,
also without a hardcoded timeout. Rationale: the original 15s literal was a
one-off workaround for subprocess test speed (resolved by --no-llm in _run_do);
forcing a timeout that differs from the planner's own timeout would create a
second configuration surface. If a timeout is needed, it should come through
config (env var or toml), same as temperature/num_predict.

## 2026-07-24: T002a transport extraction skipped — run_structured_call is importable (F013)
`_call_with_retry` in pingpong_loop.py is deeply coupled to `PingPongResult` and
`_record_attempt` (private helper). Extracting it creates circular imports
(provider_call → pingpong_loop for PingPongResult, pingpong_loop → provider_call
for the function). Feature spec says "extract one if none is importable" — and
`run_structured_call` IS directly importable from `structured_outputs.py`. Intake
uses `run_structured_call` for schema validation + parse retry; transport failures
(provider timeout) cause `call_fn` to raise, caught by `run_intake` and routed to
`heuristic_intake`. No second transport-retry system needed.

## 2026-07-24: project adopt takes explicit job_id, not bulk (F148 R-0103)
`remedy project adopt <job_id>` adopts exactly one job. Short 8-char IDs
resolved via Core store filename prefix match (same pattern as job stop
R-0097). Already-scoped jobs rejected with exit 2 naming current owner.
No bulk/--all path — spec forbids automatic mass claiming.

## 2026-07-24: Creation guard wired at CLI layer only (F148 R-0099)
Both `_cmd_create_job` (job.py) and `_cmd_do` (do_cmd.py) now resolve via
`select_project(flag, cwd)` with full precedence (flag/env/cwd). No
resolvable project → error exit 3 with fix-it hint. Library functions
(`run_do`, `run_autorun`) keep permissive `project_id: str | None = None`
parameters — test harnesses and internal callers pass project_id directly
without going through select_project. Existing subprocess tests updated
with fixture project registration (14 tests in test_do_runtime.py).

## 2026-07-24: project_id field placement on Job model (F148 T001)
`project_id: str | None = None` added to Job model between `metadata` and
`fences`. Type is `str` (not UUID) to match project registry's string-based
job_ids list and avoid cross-package UUID import coupling. `None` means
legacy (no project attribution). Pydantic default handles backward compat:
old JSON without the field loads with `project_id=None`.

## 2026-07-24: Legacy do_run path gets optional project_id (F148 T001)
The v1 `run_do` path (called from `_cmd_do` when not in golden-path mode)
previously had no project context. Added `project_id: str | None = None`
parameter. The CLI resolves project via `select_project(flag, repo)` before
calling `run_do`. If no project is resolvable and no `--project` flag was
given, `project_id` is None — the legacy path permits this because it
predates project identity. The golden path (`_cmd_do_mission`) continues
to require a project (exits 3 if missing).

## 2026-07-24: continue_from_node prefers Job.project_id over metadata (F148 T001)
Changed `parent_project_id` resolution from `parent_job.metadata.get("project_id")`
to `parent_job.project_id or parent_job.metadata.get("project_id")`.
The model field is authoritative; metadata fallback covers pre-F148 jobs
that stored project_id only in metadata.

## 2026-07-24: project_scope.py placement — packages/orchestration/ (F148 T002)
Module placed beside storage.py and project_registry.py in
`packages/orchestration/`. Exports: `ProjectScope` (scope dataclass),
`resolve_scope` (CLI flag/env/cwd precedence), `job_in_scope` (predicate),
`scoped_jobs` (THE single listing helper). Legacy rule implemented per
spec: None-project jobs visible only under --all-projects or when
exactly one project exists.

/review-remedy command added — reviewer bootstraps review rounds from disk, operator no longer relays completion reports

## 2026-07-23: Config template lives in init_cmd.py, written before registry (F081 T002)
`_CORE_TEMPLATE`, `_RUNTIME_ACTIVE`, `_RUNTIME_SKIP` are module-level string constants
in `apps/cli/commands/init_cmd.py`. Config file is written BEFORE project registry so
that a registry failure still leaves a valid `remedy.toml`. Handler reports each step
as `[created|exists|skipped]` with no early return. Runtime detection calls
`detect_runtimes(root)` from `packages/runtimes/runtime_config.py` — exactly 1 result
fills `[runtime]`, 0 or >1 produces commented-out section + `[skipped]` message.

## 2026-07-23: Ignore hygiene reuses .git/info/exclude (no new mechanism) (F081 T003)
`_ensure_ignore_entry` in init_cmd.py uses the same `.git/info/exclude`
mechanism as `ensure_ignored` in worktrees.py. Inline implementation (not
importing `_git` private helper) to avoid coupling. Entries added:
`.remedy-wt/` (always), data-dir and workspaces (only if inside repo).
Decision: reuse existing exclude pattern, not a sibling mechanism.
The `_ensure_ignore_entry` duplication vs worktrees.ensure_ignored is a
deliberate low-risk scope tradeoff: refactoring F006-shared code inside
F081 would widen the blast radius with no functional benefit. Both
implementations use the identical `.git/info/exclude` append-if-absent
pattern. If a shared helper is warranted later, it belongs in a dedicated
refactor, not in a feature branch.

## 2026-07-23: Runtime table written to .remedy/config.toml, not remedy.toml (R-0080)
Two config systems exist: `config.py` reads `remedy.toml` `[remedy]` table only;
`runtime_config.py` reads `.remedy/config.toml` `[runtime]` section. init now writes
each table to the file its loader reads: `[remedy]` → `remedy.toml`, `[runtime]` →
`.remedy/config.toml`. On no-marker repos, `.remedy/config.toml` gets the commented
`[runtime]` example (not omitted) so users have a template to fill in. `.remedy/` is
the project config directory, NOT the data root (which is do-not-touch).

## 2026-07-23: `remedy init` uses the _DEFAULT_COMMAND pattern (F081)
No top-level command pattern exists in the CLI. `remedy init` is implemented
as group "init" with subcommand "run", and `_DEFAULT_COMMAND["init"] = "run"`
in grouped.py so `remedy init --project-name foo` auto-maps to
`remedy init run --project-name foo`. Matches the existing `do`/`ui` pattern.

## 2026-07-23: /build-remedy is a command, not a skill
A command fires only on explicit `/build-remedy` invocation. A skill description
could auto-trigger from the agent's skill-matching heuristic — deliberately
avoided. The command bootstraps Window 1 (planner/reviewer) from
docs/agents/planner_reviewer_prompt.md.

## 2026-07-23: Legacy remedy-reviewer.md subagent deleted
Superseded by split_workflow.md Window 1. The subagent from the retired
parallel-review system risked a conflicting reviewer path. Git history
preserves it.

## 2026-07-23: Legacy parallel-reviewer artifacts deleted; reviewer is fully read-only
self_run_goal_*.md, job_workflow_readiness.md, post_apply_smoke_5361.md deleted.
These were superseded by docs/agents/split_workflow.md which codifies the
two-window lifecycle. The reviewer (Window 1) is now fully read-only by
design; all writes are authored by the reviewer and applied verbatim by the
worker (Window 2). Git history preserves the legacy files.

## 2026-07-23: R4 test count discrepancy — documentation error, not test deletion (Phase 1)
Handoff docs (.agent/context.md, .agent/live_review.md) claimed 499 tests green
(95 in test_project_resolution.py, 13 in test_f146_package_pipeline_e2e.py).
Evidence run produced 495 (93 resolution, 11 f146_e2e). Investigation confirmed
the committed test files always had 93 and 11 test methods — git log and method
counts prove no tests were ever deleted. The 95/13 numbers were never real;
they were documentation errors in .agent/ state files. Corrected to verified
actuals: 93 + 11 = 104 (was claimed 95 + 13 = 108), total 495 (was 499).
Evidence ZIP (remedy-review-20260723-141827-READY_FOR_REVIEW.zip) generated with
correct 495 count. Commits: all R4 production code unchanged.

## 2026-06-13: UI `npm run lint` is pre-existing broken; rely on typecheck/vitest/build (Block 1180-1192)
`apps/ui/eslint.config.js` (unchanged since the Steps 172-201 UI rebuild) registers no
TypeScript parser, so eslint parses every `.ts/.tsx` with espree and fails with parse errors
on ALL files — including untouched legacy ones. `@typescript-eslint` is not installed.
This block forbids new dependencies, so the proper fix (add the TS parser/plugin) is out of
scope. Quality gates used instead: `npm run typecheck` (tsc), `npm run test:unit` (vitest),
`npm run build` (vite). Lint remains a pre-existing repo blocker, documented for a future
dedicated branch.

## 2026-05-05: Project Constitution v1 is read-only extraction, not enforcement (Step 21)
Constitution extracts policy signals from known project files using purely lexical matching.
No subprocess, no eval, no recursive scan, no secrets. It is not consulted by task execution
in v1 — it is a structured metadata layer for future Context Inspector, Verifier Marketplace,
MCP Quarantine, Autonomy Modes, and Memory/MemPalace. The optional constitution parameter
was added to summarize_cockpit and summarize_trust_report rather than loading inside those
functions, to keep them pure and testable without a live repo.

## 2026-05-05: Trust Report v1 is read-only and text-first (Step 20)
Trust Report assembles evidence across Job JSON, Artifact metadata, JSONL run logs,
Permissions, and Approval Queue into one auditable plain-text document. It is intentionally
read-only with no apply/autonomy behavior. The design prepares for future Replay, Live
Cockpit, MemPalace, and MCP Quarantine reports by establishing a clean summary contract
(what was requested / planned / run / created / verified / decided / NOT done) without
coupling to any execution-side behavior. Redaction policy is inherited from run-log
contract: no raw exception text, no raw artifact content, no full diff text.

## 2026-05-05: v1 intent IDs are index-based; patch_intent_explanations must be stable (Step 19.1)
Intent IDs encode the 0-based index into artifact.metadata["patch_intent_explanations"].
This is simple and stable for v1 (intents are generated once per task run, never reordered).
Builders must treat patch_intent_explanations as append-only after creation — reordering
would misalign existing approval decisions with the wrong intents. This is documented as
an explicit invariant in architecture.md. Future multi-intent or regenerated-intent workflows
must move to content-hash-based stable IDs (e.g. SHA256 of target_path + action + intent).

## 2026-05-05: Approval states: latest decision wins (Step 19)
Approving a rejected intent (or vice versa) overwrites the stored state. No "un-decide"
operation exists. This is safe for v1 because no apply step exists — no state is
irrecoverable. The policy is documented in the CLI help text and module docstring.

## 2026-05-05: Approval raw reason text NOT logged to run log (Step 19)
The user-supplied --reason text is stored in artifact.metadata["patch_intent_approvals"]
but never written to run log events. Run logs record reason_present=True|False only.
This matches the general redaction policy: user-supplied strings may contain sensitive text.

## 2026-05-05: Intent ID format "<artifact_short_id>-<idx>" (Step 19)
Intent IDs use the first 8 hex chars of the artifact UUID + 0-based index into the
patch_intent_explanations list. rfind("-") is used to parse — robust against the 8-char
hex portion potentially containing no dashes (since it's hex, it won't, but defensive code).
Index-based v1 chosen over hash-based: simpler, stable, human-readable in the CLI.

## 2026-05-04: interrupted run → can_auto_continue=False (Step 18.1)
An interrupted run (task_run_started with no terminal event) causes _can_auto_continue to
return (False, "interrupted run detected — inspect timeline before continuing"). Previously
it returned True. The boolean must be conservative: a future autonomy controller must never
treat interrupted=True as a green light to continue. The Next best action section still guides
the human to inspect the timeline and then resume manually — human guidance is preserved,
machine-readable signal is conservative.

## 2026-05-04: repo_generated_write attention item fires only on explicit denial (Step 18)
repo_generated_write defaults to False (opt-in). The cockpit attention item
("Repo writes are denied — allow with: remedy set-permission …") should NOT fire
just because the permission hasn't been granted — that is the expected initial state for
most jobs. It fires only when the user has explicitly called set_permission(..., allow=False).
Detection: check job.metadata.get("permissions", {}).get("repo_generated_write") == "deny".

## 2026-05-04: Cockpit reuses load_run_events from timeline.py (Step 18)
Both views read the same JSONL files. Sharing load_run_events avoids duplicating the
file-reading logic. The CLI calls load_run_events once and passes events to
summarize_cockpit. This is the same "load once, render separately" pattern as timeline.

## 2026-05-04: Cockpit signal extraction: one pass for interrupts, second pass for last events (Step 18)
_extract_signals does two forward passes over the event list. The first detects interrupted
runs (task_run_started without a terminal event). The second collects the last occurrence
of each relevant event type. Two passes are clearer than interleaving the two accumulation
patterns. Events are short — no performance concern.

## 2026-05-03: ValidationError must be caught before ValueError in exception handlers (Step 17.1)
In Pydantic v2, `pydantic.ValidationError` inherits from `ValueError`. If `except ValueError`
appears first, it silently swallows `ValidationError` and the `except ValidationError` block is
dead code. Fix: reorder so `except ValidationError` precedes `except ValueError`, with inline
comment. This was the original Step 16.1 fix — re-applied after merge loss.

## 2026-05-03: planning_failed uses fixed message + error_category, never str(exc) (Step 17.1)
Raw exception messages may contain server URLs, tokens, connection strings, or other sensitive
text. Logging `message=str(exc)` violates the run-log redaction policy. Fix: always log
`message="planning failed"` (stable, safe) and `metadata.error_category=type(exc).__name__`.
The Timeline renderer reads only `error_category`; never renders `message` as diagnostic text.

## 2026-05-03: _fail() closure in _cmd_run_next_task_local (Step 17.1)
A local `_fail(outcome, **meta)` helper closes over `log`, `pending_task`, and `pending_task_type`
to emit `task_run_failed` from any of the 5 early-exit paths without repeating the full log.log()
call. Preserves the terminal-event invariant without code duplication.

## 2026-05-03: Timeline uses sequential event processing with task-block accumulation (Step 17)
Events are processed in timestamp order. When task_run_started is seen, a "task block"
is opened and subsequent events are accumulated until a terminal event (task_run_completed,
task_run_failed, task_run_noop). The block is then rendered as a compact multi-line summary.
Events outside a task block are rendered individually. This matches the natural event structure
without requiring a pre-grouping pass and handles multiple retries of the same task_id naturally.

## 2026-05-03: load_run_events takes data_dir (parent of runs/) not runs_root (Step 17)
`data_dir` maps to REMEDY_DATA_DIR — the same value used by storage.py and workspace.py.
`load_run_events` appends `runs/<job_id>/` internally. The CLI resolves data_dir from the
REMEDY_DATA_DIR env var or the repo-local default, matching run_log.py's resolution order.

## 2026-05-03: summarize_timeline is pure — events pre-loaded by caller (Step 17)
Separating load from render makes summarize_timeline trivially testable (pass crafted dicts).
The CLI loads events and passes them in. This also allows future callers (web server, TUI) to
load events differently without changing the renderer.

## 2026-05-03: Unknown events render as "○ <name>" rather than being silenced or crashing (Step 17)
Silencing unknown events would hide bugs and make logs harder to diagnose. Crashing would
break the timeline on log format evolution. Rendering with the INFO symbol is honest: the
event is present and acknowledged; its semantics are just not yet implemented in the renderer.

## 2026-05-03: Run Logs v1 — one JSONL file per CLI invocation (Step 16)
Each CLI invocation creates a RunLogWriter with a fresh run_id (UUID4 hex). All events
from that invocation share the same run_id, forming a chronological session trail.
Multiple invocations for the same job produce separate files under <job_id>/: history
accumulates across retries without overwriting earlier sessions. Enables resume,
diagnostics, and future cockpit/timeline UX without a database.

## 2026-05-03: Redaction policy: no full content or prompts in run logs (Step 16)
Run logs store only IDs, counts, outcomes, metadata labels (task_type, model, risk levels,
verifier profile, check names). Full artifact content, prompts, workspace file contents,
and diff previews are excluded. The authoritative full content lives in job artifacts and
workspace files; the run log is the lightweight observability layer only.

## 2026-05-03: log= appended to CLI output for plan-job-local and run-next-task-local (Step 16)
The log path is appended to the existing summary output line (two spaces before "log=")
for both commands, including the noop case. create-job does not print log= because its
stdout is machine-parsed (bare job UUID); adding log= would break scripts that capture it.

## 2026-05-03: RunLogWriter creates the job directory eagerly, file is created on first write (Step 16)
mkdir in __init__; file created on first append(). If a command exits before writing any
events (e.g. workspace_write denial happens before any log.log() calls), no JSONL file is
produced but the directory exists. This is intentional — the directory is cheap and the
denial case is covered by the permission error output, not the run log.

## 2026-05-02: Verifier Profiles v1 checks run inside workspace block, after check 6 (Step 15)
Profile-driven checks (required_sections, min_proposed_changes, forbidden_phrases) are
placed inside the `if contract.require_workspace_file:` block in verify_task_output,
after workspace file is confirmed present and non-empty (but not gated on require_proposed_changes).
This means they are skipped if workspace file is missing or empty — both of which are
hard infrastructure failures where semantic content checks are irrelevant. Profile checks
read artifact.content, not the workspace file. All four check types run unconditionally
once the workspace gate passes; no early returns within profile checks.

## 2026-05-02: Profile verifier_profile field added to _ROUTE_RULES 4-tuple (Step 15)
_ROUTE_RULES changed from list[tuple[str, str, str | None]] to list[tuple[str, str, str | None, str]].
The fourth element is the verifier_profile name. get_task_type_spec and iter_task_type_specs
now read it from the rule. is_known_task_type uses `kw, _, _, _` unpacking.
All three callers (task_registry, test_task_registry, test_patch_intent) updated.
Single source of truth: routing and profile are co-located in the same rule entry.

## 2026-05-02: generic profile fallback is permissive by design (Step 15)
Unknown task types (and None profile names) fall back to the generic profile, which has
no forbidden_phrases and min_proposed_changes=1. This ensures no new verification failures
are introduced for task types that were passing before Step 15. The profile escalation is
intentional and conservative: unknown → generic, not unknown → strictest.

## 2026-04-28: Step 11 uses a structured preview block, not unified_diff
A real unified_diff was considered but rejected: artifact proposed changes are
bullet-point descriptions of changes, not actual file content. Diffing them against
the current file would produce a misleading all-removal + all-addition diff.
The structured block (header + existing context + labeled additions) is honest
about what it is — a proposal preview, not a diff from current to new state.

## 2026-04-28: PatchDryRunResult is a dataclass, not a Pydantic model
It is a transient, in-memory object used only for CLI output and compact metadata
storage. Pydantic overhead and serialization coupling are not needed. The CLI
converts it to a plain dict before storing in artifact.metadata.

## 2026-04-28: dry_run_block computed inside if vr.passed block, printed after save_job
Storing the formatted string (not a function reference) avoids a second late import
after save_job. The explanation is printed immediately after the main summary line
so the user sees it in context with the job/task summary.

## 2026-04-28: artifact_content extraction mirrors task_runner logic but stays local
_extract_proposed_lines in patch_intent.py duplicates the section-boundary logic
from task_runner._extract_proposed_changes. This is intentional — importing private
helpers across modules creates invisible coupling. Both copies are small and the
comment in patch_intent.py documents the parallel.

## 2026-04-28: Step 10.9 continues on feature/step10-patch-intent (PR #10)
Minor hygiene pass before Step 11 (patch apply). Same branch and PR. No new tests,
no behavior changes — comments and one additional assertion only.

## 2026-04-28: KEEP IN SYNC comments include the exact test file path
"enforced by TestKeywordSync in tests/test_patch_intent.py" removes all ambiguity
for a developer editing either rule table without first checking the test suite.

## 2026-04-28: private-import comment added to all three TestKeywordSync test methods
Each test method imports _INTENT_RULES and _REPO_PATH_RULES directly. The comment
explains that this is intentional (testing the contract) rather than accidental.

## 2026-04-28: Step 10.8 continues on feature/step10-patch-intent (PR #10)
Post-failure state accuracy and sync hardening are final refinements of the
Patch Intent v1 reliability work. Same branch and PR.

## 2026-04-28: verifier-failure test uses real finalize_task
The prior version mocked finalize_task as a no-op, leaving the task lifecycle
untested. Using the real finalize_task confirms both behaviors together: patch
intent is skipped (vr.passed=False) AND the task correctly rolls back to PENDING.
All finalize_task invariants are satisfied by the test setup (task.output_artifact_ids
is populated, artifact is in job.artifacts, task.status is RUNNING).

## 2026-04-28: KEEP IN SYNC comments are placed at the definition site
Both rule tables now carry a KEEP IN SYNC comment pointing to the other table.
This makes the contract visible to anyone editing either file, regardless of
whether they remember to check the test suite first.

## 2026-04-28: Step 10.7 continues on feature/step10-patch-intent (PR #10)
Template mapping sync and verifier-failure skip coverage are final reliability
checks for Patch Intent v1. Same branch and PR as Steps 10–10.6.

## 2026-04-28: keyword→template mapping must be identical between both tables
Two tables can have identical keyword sets and identical ordering but still route
a given task type to different paths if a template string differs. The mapping
test (test_intent_rules_and_repo_rules_full_mapping_matches) catches this by
comparing {keyword: template} dicts directly.

## 2026-04-28: verifier-failure skip is tested via assert_not_called
The `if vr.passed:` guard prevents any patch intent code from running on verifier
failure. The test patches derive_patch_intents and verify_patch_intent_set as
named mocks and calls assert_not_called() on both after the CLI function returns.
This is an explicit behavioral contract, not just an absence of metadata keys.

## 2026-04-28: Step 10.6 continues on feature/step10-patch-intent (PR #10)
Rule ordering and CLI coverage hotfix is an in-scope refinement of Step 10.5.
Same purpose (patch intent reliability), same PR. No new branch.

## 2026-04-28: Keyword ordering is part of the rule-table contract
Both _INTENT_RULES and _REPO_PATH_RULES are first-match-wins. A keyword promoted
or demoted in one table but not the other silently changes routing semantics.
The ordering test (test_intent_rules_and_repo_rules_keyword_order_matches) uses a
direct list comparison — simple, deterministic, failure message is clear.

## 2026-04-28: CLI-level patch intent test uses module-attribute patching
_cmd_run_next_task_local uses late `from X import Y` imports for all heavy
dependencies. Patching the module attributes (e.g. packages.orchestration.
patch_intent.verify_patch_intent_set) intercepts the lookup at import time inside
the function — no need to patch at the apps.cli.main namespace. Only
verify_patch_intent_set is mocked to inject errors; derive_patch_intents runs
normally so the full patch-intent derivation path is exercised.

## 2026-04-28: Step 10.5 continues on feature/step10-patch-intent (PR #10)
Reliability hotfix is an in-scope refinement of Patch Intent v1 (Step 10). Same
purpose (patch intent observability and guard hardening), same PR. No new branch.

## 2026-04-28: derive_patch_intents raises RuntimeError (not ValueError) for invariant violations
task_id=None and artifact.id=None are programming errors (invariant violations), not
user-input errors. RuntimeError is the correct signal for internal invariant failures.
ValueError is reserved for user-facing or schema-level validation. Both guards added.

## 2026-04-28: Patch intent verification errors are non-fatal (warn + record)
Turning verify_patch_intent_set failures into hard task failures would require a new
exit code or a new failure mode in the existing task contract system. Since patch
intents are proposals only (never applied), a non-fatal warning + metadata record is
the correct conservative position. This preserves the existing task completion model.

## 2026-04-28: patch_intent_errors recorded in artifact.metadata (not logged only)
Recording errors in metadata makes them auditable in job JSON (show-job), consistent
with how verification_failures is recorded on task artifacts. CLI stderr warning is an
operator signal; metadata is the durable record.

## 2026-04-28: Keyword sync enforced by test, not by shared module
The keyword sets in _INTENT_RULES and _REPO_PATH_RULES are identical today. A shared
module is not needed yet — the two tables serve different purposes (workspace patch
proposals vs. repo file writes) and may diverge intentionally in a future step.
A focused sync test (TestKeywordSync) is the smallest reliable change and will catch
any accidental divergence at test time.

## 2026-04-28: Null-byte check uses `continue` after recording error
After detecting a null byte, further checks on the same path (absolute check, traversal
check, .md check) are unreliable because the path itself is malformed. Short-circuiting
with `continue` is consistent with the empty-path guard above it.

## 2026-04-27: Step 10 on new branch feature/step10-patch-intent
Patch Intent v1 has a clearly different purpose (structured change proposals), review scope,
and feature boundary from the permission model (Steps 9–9.6). New branch from main is correct.

## 2026-04-27: Patch intent derivation uses task_type keyword match only (not free-form LLM text)
Raw LLM strings can contain arbitrary path references. Keying derivation on task_type —
using the same conservative keyword table as repo_applicator — ensures the target_path is
always predictable and never injected from model output. This is intentionally limiting;
future steps can expand derivation safely with more explicit input handling.

## 2026-04-27: PatchIntentSet can be empty; no file written when intents is empty
Most task types do not match documentation keywords (e.g. "write_tests", "implement_feature").
An empty PatchIntentSet is valid and expected. No workspace file is written in that case.
patch_intent_count and patch_intent_file are not set in artifact metadata if no intents.

## 2026-04-27: verify_patch_intent_set is a pure function returning list[str] (not VerificationResult)
Keeping it separate from the existing VerificationResult/TaskContract hierarchy avoids
coupling patch intent verification to the Task Contract v1 system. A simple list of error
strings is sufficient and testable in isolation. Integration into VerificationResult is
deferred to a later step if needed.

## 2026-04-27: Patch intents derived only when vr.passed
Deriving intents from a failed task execution risks capturing incomplete/wrong output.
Tying derivation to verification-passed ensures intents represent only confirmed builder output.

## 2026-04-27: no-pending-tasks early check added before workspace_write guard
workspace_write denial should only block actual work. If there are no pending tasks, the
job is complete (or was never planned) and should exit(0) cleanly regardless of permissions.
Fix: check any(t.status==PENDING) before the workspace_write guard.

## 2026-04-27: mf dead branch removed (file_info always set after Step 9.6)
After Step 9.6, mf is always a MaterializedFile when we reach the output line:
- result.changed=True (returned early if False)
- workspace_write confirmed (exited early if denied)
- materialize_task_output returns None only when result.changed=False
The `if mf is not None else ""` guard is genuinely dead code; simplifying it.

## 2026-04-27: Step 9.6 continues on feature/step9-permission-model (PR Continuity Rule)
Enforcement ordering fix is a correctness fix for the workspace_write gate introduced
in Step 9.5. Same purpose (permission model), same PR (#9). No new branch.

## 2026-04-27: workspace_write check moved before builder instantiation (not after)
Step 9.5 placed the check after run_next_task returned, wasting an LLM call when denied.
The fix: check immediately before `start = time.monotonic()` (after imports, before
OllamaBuilder() is instantiated). Denial exits non-zero with no state mutation.
The late materialization conditional is removed — check has already passed by that point.

## 2026-04-27: show-permissions labels ALL capabilities ([active] and [reserved])
Asymmetric labeling (reserved gets a label, active gets nothing) was confusing — users
couldn't easily distinguish active from unlabeled. Adding [active] to all rows makes
the status column consistent and self-explanatory.

## 2026-04-27: Step 9.5 continues on feature/step9-permission-model (PR Continuity Rule)
Permission model honesty / CLI UX hotfix is a direct in-scope refinement of Step 9.
Same purpose (permission model), same review scope, same PR (#9). No new branch.

## 2026-04-27: workspace_write is enforced in the CLI, not in task_runner.py
The gate is a single conditional in _cmd_run_next_task_local before materialize_task_output.
Enforcing inside task_runner.py would require adding a Job parameter to materialize_task_output
(signature change, more invasive). CLI-level gate is sufficient: if denied, mf=None,
verifier fails on workspace_file_in_metadata, task rolls back to PENDING. This is honest.

## 2026-04-27: Reserved capabilities print a CLI notice; they are not blocked from being set
Preventing set-permission for reserved capabilities would require extra validation that serves
no safety purpose (setting them is harmless since no code path checks them). Persisting the
setting with a notice is user-friendly and preserves future compatibility when the capability
becomes active — the user's grant will take effect automatically.

## 2026-04-27: show-permissions is a dedicated CLI command (not buried in show-job JSON)
show-job dumps raw job JSON — useful for debugging but verbose and requires jq/parsing to
extract permissions. A dedicated show-permissions command is one line per capability and
labeled clearly. Minimal code, maximum clarity.

## 2026-04-27: effective_permissions() is a pure helper in permissions.py
No storage access, no CLI dependency. Takes job (already loaded by caller), returns list of
dicts. Testable in isolation. The CLI formats and prints; permissions.py owns the logic.

## 2026-04-25: Step 9 on new branch feature/step9-permission-model
Permission model is clearly unrelated to repo attachment/applicator (different purpose,
review scope, merge intent). All Step 8.x work is merged to main. New branch correct.

## 2026-04-25: Capability as str, Enum — Capability("foo") raises ValueError
Using str, Enum makes capability values self-documenting strings and makes invalid
values fail at construction time. The CLI catches the ValueError and prints a clear
error with the valid capability list.

## 2026-04-25: workspace_write is allowed by default
workspace_write is always needed for local task execution; requiring explicit opt-in
would break the existing flow and add friction with no security benefit in the current
local-only model. All other capabilities default to deny.

## 2026-04-25: check_and_apply_to_repo lives in repo_applicator.py, not permissions.py
It combines permission checking with repo application logic and must import from both
modules. Placing it in repo_applicator (which already imports Artifact and Path) is
cleaner than importing repo_applicator logic into permissions.py or creating a third
module for a single function. No circular import: permissions.py imports Job via
TYPE_CHECKING only; repo_applicator.py imports permissions at function call time.

## 2026-04-25: check_and_apply_to_repo mutates artifact.metadata on denial
Recording repo_application_skipped_reason directly on the artifact is consistent with
how verification_failures and verification_passed are recorded (finalize_task). The
artifact is the authoritative record of what happened during task execution. The caller
(CLI) persists the job after this call, which saves the annotation.

## 2026-04-25: repo_overwrite and shell_exec are defined but unused in Step 9
They exist to make the capability namespace stable and to allow CLI experimentation.
Granting them has no effect because no code path checks them yet. This is intentional
and documented. Preventing them from being set would require extra validation that
serves no safety purpose in the current implementation.

## 2026-04-25: Step 8.6 continues on feature/step8-repo-attachment (PR Continuity Rule)
Routing and boundary hotfix is an in-scope correctness fix for the repo applicator
introduced in Step 8. Same branch, same PR.

## 2026-04-25: _REPO_PATH_RULES: docs/remedy/ keywords moved before plain docs/ keywords
Substring match on "doc" would match compound types like "spec_document" before "spec"
got a chance to match. Fix: evaluate all docs/remedy/ entries first. readme stays first
as a special case. Within each group, "documentation" appears before "doc" since "doc"
is a substring of "documentation". Order is now explicit and documented with comments.

## 2026-04-25: _write_to_repo resolves repo_root internally before boundary comparison
target = (repo_root / path).resolve() produces a real absolute path. Comparing it to
an unresolved repo_root (e.g. a symlink) with is_relative_to() would always return False
even for legitimately in-bounds paths. Resolving repo_root inside _write_to_repo makes
the boundary check self-contained — callers no longer need to pre-resolve.

## 2026-04-25: Stale-path guard added to apply_task_output_to_repo (return [])
Moved from CLI-only to the function itself. Benefit: the guard is now testable directly
without invoking the full CLI+Ollama stack. The CLI's explicit re-validation + warning
is retained as defense in depth (user-visible stderr signal); the function-level guard
prevents silent filesystem writes if the CLI guard is somehow bypassed.

## 2026-04-25: Step 8.5 continues on feature/step8-repo-attachment (PR Continuity Rule)
Rule hardening is an in-scope refinement of the repo applicator introduced in Step 8.
Same branch, same PR. No new branch created.

## 2026-04-25: Removed 5 broad keywords from _REPO_PATH_RULES
Removed: implementation, prepare, define, summarize, summary.
These all match task types that produce code or non-doc output (e.g. write_implementation,
define_api_endpoint, prepare_data_migration). The false-positive risk outweighs any benefit.
Added changelog and guide as clearly documentation-oriented replacements.

## 2026-04-25: Stale repo path check lives in the CLI, not in repo_applicator.py
The re-validation (exists + is_dir) before calling apply_task_output_to_repo is in the CLI.
Reason: repo_applicator.py has no concept of "attached repo" — it just writes to a path.
The CLI is the caller responsible for policy decisions (warn vs fail vs skip). Putting it
there keeps apply_task_output_to_repo a pure boundary-safe writer with no policy.

## 2026-04-25: Stale repo path → warn + skip, never fail task completion
Task completion is defined by workspace verification, not repo application (established
in Step 8). A stale repo path is a user-environment issue, not a task failure. The CLI
prints a warning to stderr and skips the repo write; the task is still marked COMPLETED.

## 2026-04-24: Step 8 branches from feature/step6-workspace-runtime (not main)
Step 8 depends on workspace runtime, verifier gate, and diagnostic semantics introduced
in Steps 6–7.6 which are not yet merged to main (PR #7 open). Branching from main would
miss those changes entirely. Branched from feature/step6-workspace-runtime to form a PR
chain. This is documented as a necessary exception to the "branch from main" default.

## 2026-04-24: repo_applicator uses keyword matching on task_type (not exact match)
task_type values come from LLM output and are not guaranteed to match exact strings. A
keyword substring match (case-insensitive) against a static table is inspectable, fast,
and does not require config. Each entry maps a keyword to a path template. First match
wins; order is from most-specific to least-specific keyword.

## 2026-04-24: No overwriting existing repo files in Step 8
The conservative rule: if the target path exists, skip silently and return []. This
prevents Remedy from accidentally clobbering user-edited docs on retry. A future
permission-gated step can relax this for explicitly approved paths.

## 2026-04-24: Repo application is workspace-only fallback (not a failure condition)
If no repo is attached, or the task type is ineligible, or the target file already
exists, run-next-task-local continues without error. Repo application is opportunistic —
task completion is defined by workspace verification only, not by repo writes.

## 2026-04-24: _sanitize_path_component duplicated in repo_applicator.py
The same sanitization regex appears in both task_runner.py and repo_applicator.py. The
function is tiny (3 lines) and importing a private helper across modules is worse style
than a local copy. If this pattern grows, extract it to a shared utility in a later step.

## 2026-04-24: repo_applicator content is section-aware (excludes Notes and Risks)
Uses the same section-header state machine as _extract_proposed_changes in task_runner.py.
Notes and Risks appear in artifact.content with the same "  - " prefix as proposed
changes; section-aware extraction is the only correct approach.

## 2026-04-24: finalize_task carry-in: raise RuntimeError on invariant violations
Two invariant violations in the failure branch that were previously silent are now
explicit RuntimeErrors: (1) empty output_artifact_ids before clear, (2) artifact ID
captured but not found in job.artifacts. Both represent bugs in run_next_task. Silent
skip would hide the bug; raising makes it visible immediately. The conditions cannot
occur in normal operation.

## 2026-04-24: finalize_task captures artifact ID before clearing output_artifact_ids
The failure branch in finalize_task previously scanned job.artifacts by task_id after
clearing output_artifact_ids. Because multiple failed artifacts can accumulate in
job.artifacts with the same task_id, the scan would find the first (stale) artifact
instead of the current attempt's artifact. Fix: capture output_artifact_ids[0] before
clear(), then look up by artifact ID (not task_id). This ensures failure metadata
(verification_passed, verification_failures) is always annotated on the current attempt's
artifact, not a stale earlier one.

## 2026-04-24: Step 7.6 continues on feature/step6-workspace-runtime (PR #7)
Diagnostic artifact fix is a correctness fix for the verifier gate introduced in Step 7.
Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: Step 7.5 continues on feature/step6-workspace-runtime (PR #7)
Retry semantics hotfix is clearly in-scope for the same PR — it is a correctness fix
for the verifier gate introduced in Step 7. Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: materialize_task_output uses task.output_artifact_ids[0] not task_id scan
The previous implementation found the artifact by scanning job.artifacts for the first
entry with matching task_id. After a failed verification + retry, the stale failed
artifact sits earlier in job.artifacts and would be found first, causing materialization
to write to the wrong artifact object. The fix: locate artifact via
task.output_artifact_ids[0] (always the current attempt's artifact after finalize_task
has cleared the list on failure). This also removes the separate task_index lookup —
both task_obj and task_index come from one pass over job.tasks.

## 2026-04-24: finalize_task clears task.output_artifact_ids on verification failure
Failed artifact IDs must not persist in task.output_artifact_ids after rollback. If they
did, the next run_next_task would append the new artifact ID but the verifier would still
check index [0] (the stale one). Clearing on failure means [0] always refers to the
most recent attempt. The failed artifact stays in job.artifacts for diagnostics; it is
simply no longer reachable from the task.

## 2026-04-24: CLI exits with code 1 on verification failure
Matches the existing CLI discipline: non-zero exit for any failure that should stop
automation pipelines. save_job is called before sys.exit(1) so the rolled-back state
is persisted (task=PENDING, failure metadata in artifact) before the process terminates.

## 2026-04-24: Step 7 continues on feature/step6-workspace-runtime (PR #7)
Step 7 (verifier gate) is in-scope for the same PR. The workspace runtime branch
encompasses: workspace creation, materialization hardening, runtime boundary safety, and
now the verifier gate. All are part of the same "safe task execution" feature progression.
Per Pull Request Continuity Rule, no new branch.

## 2026-04-24: verify_task_output is pure; finalize_task handles mutation
Separating the pure check from the state mutation makes verify_task_output testable
in isolation and composable — callers can inspect the VerificationResult before deciding
whether to finalize. This mirrors the annotate_* pattern established in Step 5.5.

## 2026-04-24: No FAILED task state in Step 7
Verification failure rolls the task back to PENDING rather than introducing a FAILED state.
Reasons: keeps the state machine simple; PENDING tasks are retryable without extra tooling;
FAILED would require additional handling in the CLI and sequencing logic. FAILED can be
introduced in a later step if retry exhaustion or terminal failure semantics are needed.

## 2026-04-24: TaskContract Pydantic model — all flags True by default
Step 7 always runs all checks. The model exists to name the concept and reserve space for
per-task contract customization (e.g. skip workspace checks for tasks that don't materialize).
Using a Pydantic model rather than a bool parameter keeps the interface stable as new checks
are added.

## 2026-04-24: test_context_includes_prior_task_summaries rewritten to set state directly
With the verifier gate, tasks stay RUNNING after run_next_task — they no longer appear as
"prior completed tasks". The test was rewritten to manually set tasks 0 and 1 to COMPLETED
with artifacts, isolating _build_execution_context from the full execution+verification flow.
This is cleaner and more focused on what the test actually verifies.

## 2026-04-23: Step 6.7 continues on feature/step6-workspace-runtime (PR #7)
Runtime boundary hardening and final schema fixes are in-scope for PR #7 — same feature
boundary (workspace runtime, materialization). Per Pull Request Continuity Rule, no new branch.

## 2026-04-23: Workspace boundary check lives in runtime.write(), not only in callers
_sanitize_path_component in task_runner.py removes traversal before forming relative_path,
but callers could bypass it or a future caller could skip it entirely. Enforcing the check
inside write() makes the runtime a safe boundary regardless of call site. Uses resolve() +
is_relative_to() — two standard library calls, no sandbox framework.

## 2026-04-23: Root stored as resolved Path in LocalWorkspaceRuntime.__init__
Calling resolve() on the root at construction time ensures the is_relative_to() comparison
is always against a canonical absolute path. Consistent regardless of env var or symlinks.

## 2026-04-23: Missing task_id in materialize raises RuntimeError (not silent 0)
The old fallback of next(..., 0) would silently mislabel an orphan task as index 0,
producing a wrong filename. Like annotate_task_result, this is an invariant violation
that must not be silently swallowed — raise RuntimeError with a diagnostic message.

## 2026-04-23: BuilderOutput.proposed_changes min_length=1
Symmetric with PlannerOutput.proposed_tasks (min_length=1). An empty proposed_changes
produces an artifact with no content — useless and likely a provider bug. Rejected at
the model boundary before reaching orchestration.

## 2026-04-23: Step 6.5 continues on feature/step6-workspace-runtime (PR #7)
Workspace materialization hardening is in-scope for PR #7 — same feature boundary
(workspace runtime, file materialization). Per Pull Request Continuity Rule, no new branch.

## 2026-04-23: _extract_proposed_changes uses section-header state machine, not prefix-only
Original approach grabbed all "  - " lines from artifact.content, mixing Notes and Risks
into the Proposed Changes output. A simple state machine keyed on known section headers
("Proposed Changes:", "Notes:", "Risks:") is correct and adds zero dependencies.

## 2026-04-23: Filename = index + safe_type + short_id (not task_type alone)
task_type alone is not collision-safe (two tasks can share a type) and is not path-safe
(user-supplied, arbitrary string). Index ensures ordering; short_id (task UUID[:8]) ensures
uniqueness. Format: {index:03d}_{safe_type}_{short_id}.txt. Readable and deterministic.

## 2026-04-23: _sanitize_path_component is local to task_runner.py
Only used by materialize_task_output. Keeping it local avoids premature abstraction.
If workspace.py ever needs its own path policy, it can define one separately.

## 2026-04-23: Materialization ordering documented, not enforced by transactions
materialize → save_job is the conservative ordering. Documenting it in the docstring
and architecture.md makes the contract explicit for future callers. No transaction
mechanism is added — overkill for a local dev tool at this stage.

## 2026-04-23: Step 6 on new branch (feature/step6-workspace-runtime)
Workspace runtime and file materialization have a different purpose (filesystem output)
and review scope from Step 5/5.5 (execution hardening, context, metadata). New branch
created from main after PR #6 merged.

## 2026-04-23: materialize_task_output re-derives proposed_changes from artifact content
The builder's proposed_changes are already serialized into artifact.content (lines starting
with "  - "). Re-parsing artifact.content avoids storing proposed_changes redundantly in
metadata or changing RunTaskResult/BuilderOutput signatures. Simple and zero-schema-change.

## 2026-04-23: workspace_file metadata key records absolute path
Stored as str (not Path) since Pydantic artifact metadata is dict[str, Any] and str
is unambiguous across platforms. Callers can convert to Path as needed.

## 2026-04-23: LocalWorkspaceRuntime is injected, not instantiated in orchestration
runtime.write() is the only filesystem operation in task_runner.py. Injecting the runtime
keeps orchestration testable and swappable — a future Docker or sandboxed runtime can
drop in with no orchestration changes.

## 2026-04-23: PlannerOutput.proposed_tasks min_length=1
An empty proposed_tasks list produces an unrunnable job with zero tasks. Rejected at the
model boundary before reaching orchestration. Symmetric with BuilderOutput.proposed_changes
min_length=1 (added in Step 5.7).

## 2026-04-22: Step 5.5 continues on feature/step5-task-execution (PR #6)
Execution hardening (failure rollback, richer context, metadata cleanup) is in-scope
for the same feature boundary as Step 5 (task execution). Per Pull Request
Continuity Rule, no new branch was created.

## 2026-04-22: Builder failure rolls task back to PENDING, not FAILED
FAILED state exists in RunState but using it requires deciding how to surface and
re-run failed tasks — deferred to a later step. Rolling back to PENDING is the
conservative safe choice: the job can be re-attempted cleanly without state repair.
original_job_state is captured before mutation so both task and job are fully restored.

## 2026-04-22: annotate_task_result raises RuntimeError on changed-without-artifact
Previously silently returned. A changed=True result with no matching artifact means
run_next_task has a bug. Silent no-op would hide it; raising makes the bug visible
immediately. The condition cannot occur in normal operation.

## 2026-04-22: annotate_planning_result finds artifact by name+task_id, not index 0
Index 0 was fragile — artifacts can accumulate from multiple calls or be reordered.
Finding by name="planning_output" and task_id=None is unambiguous. Kept as no-op if
not found (valid: job might have no planning artifact when annotation is called on a
partially-migrated job).

## 2026-04-22: TaskExecutionContext passed to builder (not a raw string)
Provides job context, planning summary, and prior task summaries to the builder.
Separating input context from Job prevents provider from mutating state. Small and
serializable (Pydantic model). Lives in orchestration/ so providers depend on it.

## 2026-04-22: task_type deduplication via _2/_3 suffix
Duplicate task_type values from LLM planners confuse downstream task selection.
Simple suffix append is localized to plan_job_with_llm, requires no schema change,
and is deterministic. Does not redesign the planner schema.

## 2026-04-19: Step 5 on new branch (feature/step5-task-execution)
Task execution has different purpose, review scope, and feature boundary from
Step 4 (planning/provider config). New branch created from main per AGENTS.md.
PR #5 merged before rebasing this branch.

## 2026-04-19: annotate_task_result finds artifact by task_id, not by index
Blindly using job.artifacts[-1] or job.artifacts[0] would break if a planning
artifact precedes the task artifact or artifacts accumulate across calls.
Finding by task_id == result.task_id is unambiguous and safe regardless of order.

## 2026-04-19: RunTaskResult.task_id is UUID | None (not opaque object)
Typed as UUID | None in the dataclass. task_id=None signals no-op (no task ran).
Caller can always check result.changed first before using task_id.

## 2026-04-18: Role-specific env vars with backward-compat fallback (Step 4.6)
REMEDY_OLLAMA_PLANNER_MODEL takes priority over REMEDY_OLLAMA_MODEL. The generic var is kept as a fallback so existing setups are not broken. Precedence: constructor arg > REMEDY_OLLAMA_PLANNER_MODEL > REMEDY_OLLAMA_MODEL > default. Same pattern will apply to future roles (executor, verifier).

## 2026-04-18: annotate_planning_result called in CLI, not inside plan_job_with_llm
Elapsed time must be measured around the call_planner invocation, which happens inside plan_job_with_llm. Passing elapsed_ms into plan_job_with_llm would mix orchestration and timing concerns. Measuring in the CLI and annotating after the call keeps the functions focused and keeps annotate_planning_result independently testable.

## 2026-04-18: temperature/num_predict passed as Ollama options only when set
Sending these only when the user has configured them preserves Ollama model defaults otherwise. An empty options dict would be harmless but is avoided for clarity.

## 2026-04-18: PlannerOutput lives in orchestration/, not in the provider
Orchestration imports PlannerOutput to perform the transformation. If PlannerOutput lived in the provider, orchestration would depend on the provider — inverting the correct dependency direction. All providers depend on orchestration/planner_models.py.

## 2026-04-18: plan_job_with_llm accepts a callable, not a provider object
Provider is injected as `call_planner: Callable[[str], PlannerOutput]`. No provider protocol or ABC needed yet. This keeps orchestration completely decoupled and makes testing trivial (pass a lambda). Can be formalised into a protocol if multiple providers need a shared interface in a later step.

## 2026-04-18: ollama is an optional dep, imported lazily inside OllamaPlanner.plan()
Core remedy must remain usable without Ollama installed. The lazy import with clear ImportError message makes the missing-dep case user-friendly. Importing the provider module itself is safe; only calling .plan() requires ollama.

## 2026-04-18: CLI imports plan_job_with_llm and OllamaPlanner inside the function
Deferred imports in _cmd_plan_job_local prevent ollama-related import errors when the CLI module is loaded. Follows the same pattern as the lazy provider import.

## 2026-04-18: acceptance_checks not mapped to Task.acceptance_checks yet
PlannerOutput.acceptance_checks is job-level, not task-level. Mapping them to individual Tasks would require a decision about which task owns which check — deferred to a later step. Currently preserved in artifact content and metadata.

## 2026-04-18: Step 4 on new branch (feature/step4-ollama-planner)
Real provider integration has a different purpose, review scope, and feature boundary from Step 3/3.5 (orchestration skeleton + semantics). New branch correct per AGENTS.md.

## 2026-04-18: PlanJobResult is a dataclass, not a Pydantic model
It is a return type, not a domain model — no serialization or validation needed. A dataclass is the minimal correct choice. If this type ever needs to be persisted or serialized, it should be promoted to a Pydantic model at that point.

## 2026-04-18: PLANNED state added to RunState
Distinct from PENDING: PENDING = no planning yet; PLANNED = tasks generated, awaiting execution. Step 3 previously reused PENDING after planning, which was semantically ambiguous. The new state makes the lifecycle unambiguous without adding new orchestration logic.

## 2026-04-18: Step 3.5 continues on feature/step3-orchestration-skeleton (PR #4)
Step 3.5 (planning semantics hardening) is in-scope for PR #4: same feature boundary (orchestration skeleton), same review scope, same merge intent. Per Pull Request Continuity Rule, no new branch was created.

## 2026-04-15: Use `typing.Protocol` for interfaces
Protocol-based interfaces (structural subtyping) require no inheritance, keeping core completely decoupled from providers. Any class matching the signature satisfies the contract.

## 2026-04-15: Provider directories are empty stubs
`packages/providers/claude_agent/`, `docker_runtime/`, `mempalace/` exist as empty packages with `__init__.py` only. No implementation until later steps to avoid scope drift.

## 2026-04-15: contracts/ imports from core/ models
Verifier and LLMWorker interfaces need AcceptanceCheck and Task/Artifact types. The contracts package is allowed to depend on core models — both are internal, zero external deps. The dependency flows one way: contracts → core.

## 2026-04-15: LLMWorker.execute takes Task, returns Artifact
Replacing prompt-centric generate(prompt: str) with execute(task: Task) -> Artifact enforces the artifact-driven architecture at the contract level. Raw strings are a provider concern, not an interface concern.

## 2026-04-15: LLMWorker.stream returns AsyncIterator[str]
Streaming full Artifact objects is a more complex problem deferred to a later step. str tokens are kept for now as a pragmatic compromise; this is documented.

## 2026-04-15: Artifact.content kept as str
Binary artifact support (str | bytes) is a non-trivial serialization question. Deferred to Step 2 or later. Documented as a known limitation.

## 2026-04-15: Task.output_artifact_ids is list[UUID]
Task references artifact IDs, not embedded Artifact objects, to avoid circular model issues and keep the models flat.

## 2026-04-15: Step 3 on new branch (feature/step3-orchestration-skeleton)
Step 3 (orchestration logic) is clearly unrelated to Step 2/2.5 (packaging + CLI). PR #3 was merged before creating the new branch, per AGENTS.md starting-a-new-feature workflow.

## 2026-04-15: plan_job mutates Job in place
Pydantic v2 models are mutable by default. Mutation + return avoids deep-copy complexity and is consistent with how the CLI uses the result (save_job after plan_job). The function signature returns Job to make the behavior explicit.

## 2026-04-15: Idempotency guard checks tasks OR artifacts
If either is non-empty, planning is skipped entirely. This is strict but safe — prevents partial re-planning. A partially-planned job (tasks but no artifact) would be unusual and is better fixed manually.

## 2026-04-15: Job state is PENDING after planning (not a new state)
After plan_job, the job returns to PENDING. This represents "has tasks, awaiting execution". RunState values are not extended in Step 3 — the available states are sufficient for now. A PLANNED state could be added in a later step if needed.

## 2026-04-15: Step 2.5 continues on feature/step2-packaging-cli (PR #3)
Step 2.5 (storage + CLI hardening) is an in-scope extension of Step 2 (same feature boundary). Per the Pull Request Continuity Rule, continued on the existing branch and PR rather than creating a new one.

## 2026-04-15: Step 2 on new branch (feature/step2-packaging-cli)
Step 2 (packaging + CLI) has a distinct purpose, merge scope, and feature boundary from Step 1.5 (contracts hardening). New branch is correct per AGENTS.md "clearly unrelated" criteria.

## 2026-04-15: hatchling as build backend
Minimal, modern, zero-config for simple package layouts. `packages = ["packages", "apps"]` exposes both top-level dirs as importable packages.

## 2026-04-15: Storage is repo-root-relative (not CWD-relative)
_resolve_data_dir() uses Path(__file__).resolve() to find the repo root, avoiding CWD fragility. REMEDY_DATA_DIR env var overrides for non-standard setups.

## 2026-04-15: list_jobs silently skips corrupted files
Corrupted JSON files are skipped without raising. Acceptable for local dev tool; can be hardened to warn/error in a later step.

## 2026-04-15: Storage was CWD-relative (superseded)
.data/jobs/ is relative to the working directory where the CLI is invoked. Simple and deterministic for single-user local use. No config system yet.

## 2026-04-15: Job.user_prompt field added
CLI requires a prompt field on Job to persist the user's input. Added as str | None = None — pure data, no orchestration logic.

## 2026-04-29: classify_risk is non-blocking and has no side effects
Risk classification is a one-shot mapping (action → risk level string). It is
intentionally non-blocking: a future step can use risk_level to prompt for
user confirmation, but Step 12 only stores and surfaces it. The "overwrite"
case is reserved and not yet produced by any code path — it is classified now
so the function is complete and future code paths don't need to change classify_risk.

## 2026-04-29: risk_level stored in both patch_intent_explanations and patch_intent_risks
patch_intent_explanations is a per-intent dict (file, action, risk, reason, summary);
patch_intent_risks is a flat list of risk strings, one per intent.
The flat list makes it easy for operators to scan risk levels without parsing dicts
(e.g. "are there any high-risk changes?"). Both keys are in artifact.metadata.

## 2026-04-29: "preview-only" and unknown actions map to "unknown" risk
When no repository is attached, the file may or may not exist — risk cannot be
determined. Mapping to "unknown" rather than inventing a level (e.g. "low") is
honest: the caller must attach a repo and re-run to get a meaningful risk signal.

## 2026-04-30: RISK_* constants defined in patch_intent.py (single source of truth)
Freeform strings scattered across classify_risk, tests, and CLI are error-prone.
Named constants (RISK_LOW/MEDIUM/HIGH/UNKNOWN) and a frozenset (RISK_LEVELS) give
one canonical definition. PatchDryRunResult.__post_init__ validates against RISK_LEVELS,
making invalid risk levels a loud construction-time failure rather than a silent
propagation. Tests import the constants so they stay in sync automatically.

## 2026-04-30: PatchDryRunResult.__post_init__ raises ValueError (not a Literal type)
Literal[...] would require changing the field annotation and adding a Pydantic validator
or a TypeVar constraint — heavier than needed for a dataclass. __post_init__ raises
ValueError with a clear message. Callers producing PatchDryRunResult (only
generate_dry_run_preview) already pass a value from classify_risk, which always returns
a member of RISK_LEVELS. The guard catches bugs in future callers, not the current path.

## 2026-04-30: format_dry_run_explanations uses "\n\n".join(blocks) for multi-result spacing
Original "\n".join(parts) across all results produced one dense block with no visual
separation between intents. Building a list of per-result blocks and joining with "\n\n"
is the minimal correct change: one blank line between blocks, no trailing newline, no
leading newline. Tested by assert "\n\n" in text in test_multiple_results_all_appear.

## 2026-04-30: RISK_UNKNOWN is conservative by design — documented in code and docs
Both the module docstring and the classify_risk docstring now explicitly state that
RISK_UNKNOWN must NOT be equated with RISK_LOW by future approval/autonomy modes.
This pre-empts a common mistake: treating an absence of evidence (no repo attached)
as evidence of absence (no risk). The architecture.md section echoes the same note.

## 2026-04-30: generate_dry_run_preview owns its own boundary check (Step 12.6)
verify_patch_intent_set already rejects ".." components in target_path. The boundary
check in generate_dry_run_preview (resolve both sides + is_relative_to) is defence in
depth: it catches symlink escapes and any edge-case path that static split-based checks
miss. The rule is "check at the use site" — the function that reads from the filesystem
is responsible for confirming it stays inside its root, regardless of upstream validation.

## 2026-04-30: truncate_preview extracted to patch_intent.py (Step 12.6)
The inline combined_preview[:2000] in the CLI required the caller to know the internal
constant _MAX_PREVIEW_CHARS. truncate_preview(text) moves the cap to the module that
owns the constant. CLI callers import the function, not the constant — implementation
detail stays local to patch_intent.py. No behaviour change; same 2 000-character cap.

## 2026-04-30: diff_preview omitted from CLI terminal output (documented Step 12.6)
format_dry_run_explanations renders the concise block (file/action/risk/reason/summary)
only. The full diff_preview per intent can be several lines; printing it for every intent
in a multi-intent job would produce cluttered terminal output with low signal-to-noise.
The full preview is stored in patch_intent_diff_preview metadata for tooling/guarded mode
to surface intentionally. This is not a bug — it is a deliberate noise-control decision.

## 2026-04-30: patch_intent_risks consumers must validate against RISK_LEVELS (Step 12.8)
Documented in architecture.md. Rationale: PatchDryRunResult.__post_init__ validates at
write time, but Step 13+ will read the stored list and act on it. Defensive re-validation
at the consumption site protects against: (a) metadata written by older code before the
RISK_LEVELS constant existed, (b) hand-edited or test-fabricated records, (c) new risk
levels added in future patches before all consumers are updated. Unknown values must fall
back to RISK_UNKNOWN (conservative), never to RISK_LOW.

## 2026-04-30: Skipped optional triple-run elimination in TestPatchIntentRisksCLI (Step 12.8)
The three focused tests each call _run_risk_scenario, running the full CLI mock 3×. Making
them share a single run would require a class-scoped pytest fixture, but class-scoped
fixtures cannot depend on function-scoped fixtures (tmp_path, monkeypatch, capsys). Adding
a conftest.py or session fixture would sacrifice clarity. Three fast runs (<0.4s total) are
preferable. Documented here so the duplication is intentional, not an oversight.

## 2026-05-01: Task Type Registry v1 — keyword-backed internal, registry-first public API (Step 13)
The registry uses an ordered keyword list internally (v1) — identical semantics to
the former _INTENT_RULES / _REPO_PATH_RULES tables. This preserves routing correctness
while eliminating the duplication. The public API (get_task_type_spec) returns a fully
resolved TaskTypeSpec with repo_route substituted; callers never see {safe_type}.

## 2026-05-01: task_type remains open — unknown fallback is conservative (Step 13)
task_type is not an enum. LLM-generated task types that don't match any keyword return
a fallback spec with repo_route=None and capabilities={"unknown_task_type"}. This is
the safe default: no repo writes, no elevated autonomy. Future step must not promote
unknown_task_type to a permissive path without explicit registry entry.

## 2026-05-01: _INTENT_RULES and _REPO_PATH_RULES removed — single source (Step 13)
Both duplicated keyword tables are gone. TestKeywordSync now tests routing parity at
the function level: both _derive_target_path and _resolve_repo_path call
get_task_type_spec and must return the same result. This is a structural guarantee,
not a copy-sync check. The KEEP IN SYNC comments are no longer needed.

## 2026-05-01: repo_applicator._sanitize_path_component removed (Step 13)
_resolve_repo_path now returns a fully-resolved path from get_task_type_spec; no local
sanitization needed in repo_applicator. patch_intent keeps its own local copy for
materialize_patch_intents workspace filenames (different use site, not routing).

## 2026-05-01: ArtifactKind defaults to UNKNOWN — explicit at creation sites (Step 14)
The default kind=UNKNOWN is a backward-compatibility affordance, not the preferred state.
Every creation site (job_runner, llm_planner, task_runner) sets kind explicitly. Unknown
stays as the default only so old persisted JSON without 'kind' deserializes safely.

## 2026-05-01: planning_artifact prefers explicit kind over legacy name convention (Step 14)
The helper checks kind=PLANNING first (explicit path, Step 14+), then falls back to
name="planning_output" and task_id=None (legacy convention, pre-Step-14). The explicit
path is preferred because: (a) it is the intended stable signal, (b) it does not depend
on a name string that could change. The fallback is deliberate and documented.

## 2026-05-01: artifact_index helpers accept Sequence[Artifact], not Job (Step 14)
Accepting a sequence rather than a Job makes the helpers composable: callers can pass
job.artifacts, a filtered slice, or any other artifact list. No coupling to Job required.

## 2026-06-08: Sole-change generic tests require timestamp ordering (Steps 840-849)
Intent/task-linked tests remain valid without timestamps because their linkage is explicit.
Generic tests can verify a sole applied change only when both apply and test timestamps parse
and the parsed test time is at or after parsed apply time. Missing/invalid ordering is incomplete,
not verified. Parsed datetime comparison is required so timezone offsets cannot create false order.

## 2026-06-08: Steps 810-839 cherry-picked as Proof Chain dependency (Steps 840-849)
After merging the open PR, main lacked the Proof Chain v1/truth-closure files referenced by this task.
The branch cherry-picked Steps 810-824 and 825-839 before applying the ordering closure so the current
block is reviewable against the expected Proof Chain baseline.

## 2026-06-08: Reviewer findings beat worker self-report (Steps 850-864)
GPT5.5 Medium handled narrow Proof Chain ordering logic well, but overclaimed final PASS while
`.agent/live_review.md` still contained a blocking file-provenance finding. Future agents must
read `.agent/live_review.md` before final handoff and treat reviewer findings as authoritative
until resolved in code and tests.

## 2026-06-08: MCP remains inactive by default (Steps 850-864)
Claude Code and VS Code MCP config files were added with empty server maps only. No MCP server is
installed or active. Pi MCP is documented as extension/package-driven; `pi-mcp-adapter` and
`mcporter` were audited by package metadata but not installed.

## 2026-07-09: Two deferred evidence-metadata hardening notes (F003 accepted, not reopened)
F003 was externally accepted (PASS_WITH_RISKS). Two runtime-evidence metadata gaps were observed
and are deliberately NOT fixed under F003, because they do not affect the accepted token/cost
totals (provider_evidence and token_truth carry valid actuals; totals reconcile exactly):

1. Runtime `task_runs/<task>/task_execution_evidence.json` reports
   `actual_provider_available=false` and `actual_token_usage_available=false` even though
   `provider_evidence.json` and `token_truth.json` contain valid provider actuals.
2. Runtime `prompt_trace_summary.json` reports some role/model metadata as unknown although the
   raw `prompt_trace.jsonl` contains it.

Both are evidence-surface metadata defects, not measurement defects. Deferred as hardening
candidates for the later evidence/replay work — preferably F140 or F163. Do not reopen F003.

## 2026-07-09: F004 stream redaction composes, not replaces, the prompt corpus
While building `stream_evidence.py` the existing `prompt_trace.redact_prompt_text`
was found to MISS several real secret shapes, because its patterns disallow the
hyphens/underscores that appear inside modern provider keys:

- `sk-ant-api03-…` (real Anthropic key format) — unredacted
- `AWS_SECRET_ACCESS_KEY=…` (the `SECRET` token is not immediately followed by `=`)
- `-----BEGIN … PRIVATE KEY-----` blocks, JWTs, `xox*-` Slack tokens

F004's binding rule is "no secrets in raw streams, ever", so `redact_stream_line`
COMPOSES the existing helper with a stream-specific corpus (sensitive JSON keys,
provider key shapes, env assignments, private-key headers) rather than trusting
it alone. Redaction stays textual so a stream line remains valid JSON.

The prompt path is deliberately NOT changed here: that is F003-accepted behaviour
and altering it is out of F004 scope. Hardening `redact_prompt_text` with the same
corpus is a follow-up candidate and should be raised as its own item — the gap is
security-relevant and affects prompt traces today.

## 2026-07-10: F004 accepted (PASS_WITH_RISKS) — three deferred hardening notes
F004 (raw stream evidence) received external acceptance `PASS_WITH_RISKS`. Manual
completion job `621369b56e834cd4`; accepted ZIP
`remedy-review-20260709-225052-READY_FOR_REVIEW.zip`. The following non-blocking
notes are recorded as later hardening items and MUST NOT reopen F004:

1. `missing_tests_gate` treats `.jsonl` fixtures as test files requiring direct
   coverage. A fixture is data, not an executable test; the gate should not demand
   a verification run keyed on it.
2. A changed task with no task-local test files may receive `NEEDS_TESTS` even
   when verification is genuinely supplied through another explicit scope. The
   gate's `covered = bool(related_tests) and not uncovered_tests` is vacuously
   false for a code-only task and should recognize cross-scope verification.
3. `job_evidence.py` reads each exported stream artifact fully into memory while
   copying/hashing it. Bounded at 50 MB/task, so acceptable for F004; stream the
   copy+hash later for very large artifacts.

Preferred home for (1) and (2): the evidence/replay hardening work (F140/F163).
(3) is a local streaming optimization in `job_evidence.py`.

## 2026-07-10: F005 reuses the existing PlannerOutput shape, adds schema_v (Steps 5961-6020)
`planner_models.PlannerOutput` is already a Pydantic model consumed by
`llm_planner.plan_job_with_llm`. F005 adds a `schema_v`-bearing schema model in the
new `schemas/` package rather than inventing a second planner taxonomy; the schema
model round-trips to/from the existing `PlannerOutput` so the planner path keeps its
current downstream contract. Same principle for the reviewer verdict: the schema
model mirrors the accepted verdict/findings/confidence/summary shape already parsed
by `_parse_reviewer_json`, not a new one (anti-goal A6: no new taxonomies).

## 2026-07-10: F005 FINDINGS correction — mandatory schema_v, hard retry cap, native schemas (Steps 5961-6020)
External review returned FINDINGS on the first F005 package. Six corrections, no
new taxonomy or gate:
1. `schema_v` is a REQUIRED response field (bare `Literal`, no default); the
   model's version is a `SCHEMA_V` ClassVar so the field never needs a default.
   Missing schema_v is now a `parse` failure (was silently defaulted).
2. The single-retry maximum is a hard safety rule: `run_structured_call` takes a
   boolean `allow_parse_retry` (no integer knob); three+ calls are impossible.
3. Provider-native schema enforcement: Claude CLI `--json-schema` (via
   `build_claude_cli_args(json_schema=)`) and Ollama `format=` (via
   `OllamaPlanner.plan_raw`). The reviewer sends a SHORT instruction, not a
   duplicated schema, and fails clearly if the CLI lacks the option — no
   prompt-only pretense. The capability probe (`claude --help`) is cwd-pinned
   like every other CLI call.
4. `plan-job-local` uses the structured planner by default; legacy `planner.plan`
   only under `REMEDY_PLANNER_FREETEXT=1`; missing structured capability fails
   (error_category=config), never a silent legacy fallback.
5. Prompt trace records one entry per actual provider call (reviewer initial +
   parse-retry; planner initial + retry), each carrying `schema_v`.
6. Parse exhaustion is classified `parse` in run-log/result evidence
   (`error_category=parse`, `ReviewerOutput.error_class`), not the exception
   class name. `parse` already exists in F005 / is required by F010.

Pre-F005 CLI-reviewer unit tests (fake bins without --json-schema / schema_v)
were pinned to the legacy free-text reviewer via `REMEDY_REVIEWER_FREETEXT=1`;
they validate transport/usage/safety, not F005 schema enforcement, which has its
own dedicated fake-provider tests.

## 2026-07-10: F005 runtime FINDINGS correction — native structured_output envelope (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260710-231042 (reviewed
job 2f1ca41f52564511). Seven runtime corrections, no new taxonomy or gate:
- Claude Code's structured result carries the object in `structured_output`, not a
  string `result`. `token_actuals.parse_cli_envelope` parses the envelope ONCE
  (value, usage, subtype). The CLI reviewer prefers `structured_output` in
  structured mode; a success envelope without it, or a malformed one, is `parse`.
- The F004 stream path (`final_result_text`) compact-serializes `structured_output`
  so streamed and non-stream yield the same validated value; normalized events
  still never copy the model response.
- `subtype=error_max_structured_output_retries` is a structured parse/validation
  failure → error_class `parse` (JSON + stream), not `provider_error`; it triggers
  Remedy's one parse retry and its Usage/cost are retained so the failed attempt
  counts toward 2/2/2 totals.
- Finding 5: the reviewer effective `-p` prompt is built once in the loop
  (`_reviewer_effective_prompt`) and recorded; provider sends it verbatim, so
  `prompt_sha256 == sha256(sent)` for initial and retry. Schema is out-of-band via
  `--json-schema`, never duplicated into the prompt.
- Finding 6: removed the `claude --help` preflight (help omits flags; absence is
  not proof). `--json-schema` support is proven by the real invocation; an
  unknown-option stderr → `config`; ordinary provider errors stay provider errors.
All proven with recorded envelopes / mocked subprocess; zero provider calls.

## 2026-07-11: F005 runtime FINDINGS #2 — stream classification + per-call traces (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260710-235823 (reviewed
job 997bcc036c12415e). Two corrections, no new taxonomy or gate:
1. The stream path previously reduced the final result to text + usage, losing
   is_error/subtype/errors, so an ordinary streamed provider error (e.g.
   subtype=error_during_execution) was misclassified as `parse` merely because the
   extracted text was empty. `stream_evidence.final_result_envelope()` now returns
   the COMPLETE final-result record (structured_output, legacy text, is_error,
   subtype, errors, usage/cost, raw line/byte refs) read back from the persisted
   redacted raw line, and the streamed structured Reviewer classifies exactly like
   the JSON path. Class is never inferred from an empty result string. Normalized
   events still copy no model response text.
2. `_call_with_retry()` may invoke the provider more than once (F001 transport
   retry), but only one reviewer trace was recorded up front. It now takes a narrow
   `on_call(transport_attempt, is_transport_retry)` callback fired immediately
   before every real call, and the single logical parse retry runs through the same
   helper with `is_parse_retry=True`. Result: one trace per ACTUAL provider call,
   reviewer traces == reviewer ProviderAttempts, transport retries of the parse
   retry stay ONE logical parse retry, and every trace prompt hash equals the sent
   string. This reuses the existing retry mechanism — no second retry system.
All proven with recorded stream envelopes, fake CLI executables and fake providers;
zero provider calls.

## 2026-07-11: F005 FINDINGS #3 — envelope-before-exit-code, planner pre-call traces (Steps 5961-6020)
External review returned FINDINGS on ZIP remedy-review-20260711-115512 (reviewed
job c4def4a3074d4a7c). Two corrections, no new taxonomy or gate:
1. The streamed CLI can emit a valid final result envelope (e.g. a native
   structured-output failure carrying Usage/cost) and THEN exit nonzero. Reading
   the return code first threw that envelope away, so exhaustion+exit1 became a
   provider_error with null usage. `_call_streamed()` now parses events, Usage and
   the FinalStreamResult BEFORE interpreting the exit code, and raises a typed
   `_StreamNonZeroExit` carrying the envelope/usage/returncode/stderr. The
   structured Reviewer classifies from the envelope: exhaustion -> parse (+usage)
   on exit 0 or 1; any other is_error -> provider_error; a "successful" structured
   result contradicted by a nonzero exit is rejected as provider_error (we do not
   trust an inconsistent process). The raw stream is parsed in exactly one place.
2. Planner traces were written by `call_recorder` AFTER `plan_raw()` returned, so a
   provider/network exception produced a real call with NO trace — violating "every
   call logs its schema_v". The split on_call/call_recorder API is replaced by ONE
   pre-call callback `on_call(attempt, schema_v, is_parse_retry, effective_prompt)`
   fired immediately before every real call. Traces now persist for success,
   invalid JSON and raised exceptions alike; no provider call still means no trace.
Both proven with fake executables and fake planners; zero provider calls.

## 2026-07-11: F006 — worktree isolation replaces copy staging (Steps 6021-6080)
- The run workspace IS a git worktree for a git target; nothing is copied. The
  filtered-copy staging path survives ONLY as the non-git fallback, so the
  historic "self-run dirties the main checkout" risk is structurally impossible.
- `.remedy-wt/` is excluded via `.git/info/exclude`, not `.gitignore`: the rule
  that protects the checkout must not itself dirty that checkout. (The repo's own
  `.gitignore` also lists it, for humans.)
- In a worktree `.git` is a FILE, not a directory, so the staged-change scanner
  needed an explicit file-level skip — otherwise the gitdir pointer would have
  been reported as a run change.
- Locks live under `<data>/projects/<sha256(repo path)[:16]>/locks/`. A short
  digest of the resolved repository path is a sufficient stable project id; F146
  is deliberately not implemented here.
- `remove()` keeps the result branch by default and there is no merge path at
  all: the branch plus `result.diff` is the entire hand-off, and merging stays a
  deliberate human action.

## F007 — Runtime harness

- Runtime state identity is PID **plus** process creation time **plus** a command
  fingerprint. A PID alone is not identity: the OS recycles PIDs, and `runtime stop`
  must never kill an innocent process that inherited one. A mismatch clears the
  stale state and reports it, killing nothing.
- A busy port is never fought over. The harness picks a free port and reports the
  EFFECTIVE port; killing whatever owns the requested port would be a footgun.
- Detection reads checked-in files only (package.json, pyproject.toml, requirements)
  and never imports project code. Two candidate runtimes is ambiguity, and ambiguity
  blocks with "configuration required" rather than guessing.
- `.remedy/config.toml [runtime]` is the canonical binding for F007. The general
  `remedy.toml` config system is deliberately NOT migrated or replaced.
- The project digest is F006's resolved-path digest. F146 (the project registry) is
  not implemented here.
- F008 (SSE stream, hook, polling fallback) is Tier 5 and depends on F146: no
  endpoint, EventSource, hook or UI work belongs on this branch.

## 2026-07-23: large-mode commands added
build-remedy-large and review-remedy-large — bigger default bundles;
closure and circling rules unchanged.

## 2026-07-24: Reword commit 40a722a — scanner false-positive on "/review-remedy" (R-0083)
Operator-approved reword via filter-branch: "add /review-remedy command" → "add
review-remedy slash command". The _contains_local_path scanner in review_subject.py
false-positives on slash-command names in commit subjects, blocking make_review_zip.
Separate fix tracked as R-0083 (not F081 scope).

## 2026-07-24: R-0093 — argv-level bare detection replaces value-equality guard (F147)
Golden-path detection moved from value-equality checks in _cmd_do to
argv scanning in grouped.py. After the mission token, any arg starting
with "-" that is not --json or --repo (+ its value) makes the
invocation non-bare. Passed as `args._truly_bare`. This is immune to
the "flag typed at its default value" problem: `do "x" --autonomy-level 1`
has a "-"-starting token → legacy path.

Default reconciliation: the catalog ArgDef for do.run --autonomy-level
says default="2", the handler fallback says `or 2`, the old _is_bare_mission
guard said `== 1` (wrong). With argv-level detection, the check is gone
and the catalog default="2" is authoritative. The handler fallback `or 2`
matches. No code change needed — the three-source conflict is resolved by
removing the value from the detection path entirely.

## 2026-07-24: R-0092 — job_stop_cmd falls back to Core Job store (F147)
Two job stores exist: pingpong_job (task_jobs/) for v1 executor jobs, and
storage (jobs/) for Core Jobs created by the golden-path `remedy do "<mission>"`.
`_load_job` in job_stop_cmd.py previously only queried pingpong_job.load_job_plan,
making golden-path jobs invisible to the kill switch. Fix: fallback to
storage.load_job on pingpong miss, with _CoreJobAdapter mapping state.value →
.status and providing empty stop_* fields (golden-path jobs have no stop
metadata yet). Exit codes and output contract identical for both stores.
The split is structural: merging stores would require a schema migration
across persisted jobs — not in scope for F147.

## 2026-07-24: R-0085 — injection marker approach for bare-mission detection (F147)
grouped.py sets `args._injected_default = True` when the `run` subcommand was
auto-injected by `_DEFAULT_COMMAND`. `_cmd_do` checks `injected_default` first:
bare `remedy do "x"` → golden path; explicit `remedy do run "x"` or any non-default
flag → legacy path. This is robust because the marker tracks what actually happened
at parse time, not what flag combinations look like after defaults are applied.
Alternative considered: argparse None-sentinel defaults for every flag — fragile
because it requires maintaining sentinels across 20+ parameters and any new flag
would silently break detection. Injection marker is one bit, set once.

## 2026-07-24: operator decisions (post-F147 meta-review)
Amendment approved: bootstrap-block rules do not bind long-lived worker
sessions; AGENTS.md is the only auto-loaded surface — adding the
artifact-build-attempt honesty rule there ensures all future sessions
inherit it without needing to read closure-protocol docs first.
R-0097 accepted as a gap fix (not part of F148): short-id resolution in
`remedy job stop` is a golden-path usability defect found by the
operator's live probe; fixing it before F148 starts avoids carrying a
known break into the next feature's smoke tests.
Closure-protocol additions: evidence-dir commit ordering (F147 attempt-2
lesson), producer pitfalls (output_hash / base_commit SHA), and
byte-identical self-check duty for reviewer-authored text.
Hygiene chore scheduled as its OWN gap item: 3 catalog-classification
test failures, 2 job_stop_integration failures, ruff-432 backlog —
explicitly NOT part of F148.

## 2026-07-26: F046 T001 — terminal-status mapping and the loop seams
Core `RunState` has no BLOCKED member, so the pingpong `JOB_*` string is the
authoritative terminal status and is written to `job.metadata`
(`cycle_terminal_status` / `cycle_job_status`). `blocked` maps to
`RunState.PAUSED`, not FAILED: "no ready task and not green" also covers a job
awaiting a decision — nothing failed, and the job must stay resumable.
`max_cycles_reached` is a sixth, non-stop-cause terminal that leaves job state
untouched; that is what makes `max_cycles=1` behave exactly like today's single
pass (JOB_RUNNING is in the mapping table for this reason).
A9 defaults taken: a job with zero tasks is `blocked` ("no_tasks"), never
"green"; a cycle with no verify step configured records `not_run` and does NOT
claim a pass; a failed task step or failed verification ends the cycle (retry
inside a cycle would be a retry policy, which is out of scope); the rollout cap
lives in the caller, so `run_cycles` honors `limits.max_cycles` verbatim and
tests can drive a five-cycle fixture.

## 2026-07-26: F046 T002 — where the rollout cap lives, and what "byte-identical" means
The cap is enforced in the CALLER (`resolve_max_cycles` / the CLI), not inside
`run_cycles`, so the loop honors `limits.max_cycles` verbatim and the five-cycle
fixture can drive it. `CYCLE_SAFETY_CAP = 1` trims flag AND config; the CLI
names the origin of a trimmed value instead of honoring it silently.
`remedy job run <id>` delegates to `_cmd_run_next_task_local` whenever the
resolved count is one, so single-cycle CLI behavior IS today's single pass by
construction — it cannot drift. The library-level regression test asserts the
delta is exactly two additive metadata keys (`cycle_terminal_status`,
`cycle_job_status`) plus the cycle evidence record; that additive trace is the
feature itself and is stated rather than hidden behind the word "identical".
Cycle records reuse `pingpong_job.job_evidence_dir` so there is no second
evidence convention. The data-root fixture in the slice suite is autouse: cycle
records are written by default, and a test that reached the repository's real
`.data/` would pollute it.

## 2026-07-26: F046 integration gate — plan.md keeps its Next Steps section
The F046 plan.md rewrite dropped `## Next Steps`, which AGENTS.md requires
("Must contain: Goal, Current Step, Next Steps") and which two dashboard
contract tests assert. That omission was the ONLY reproducible branch-only
failure in the integration gate (2 tests, both asserting `"Steps" in
plan.md`); the base plan.md still had the section, which is exactly why the
failures were branch-only. The section was restored — a state-file edit, no
production code, permitted in a gate round. Deviation from the verbatim
plan.md text dictated at feature start is recorded here rather than applied
silently. The three sibling failures (context.md wants `## Active Branch` and
the word "Steps"; live_review.md wants "Steps") fail identically on base and
were deliberately NOT swept up: they are pre-existing, not F046-attributable,
and belong on the backlog.

## 2026-07-29: F252 D8 — the intake call_fn was driving the flight-plan call
`make_provider_call_fn()` bound Ollama's NATIVE `format=` schema to
`JobIntake` and `do_cmd` reused that same callable for `plan_job_llm`. The
provider therefore answered every planning attempt (retry included) in
intake shape, and validation reported exactly `schema_v: Input should be
'flight_plan_v1'; tasks: Field required; goal: Extra inputs are not
permitted`. Fix: `make_structured_call_fn(model_cls)` is the general
factory, `make_provider_call_fn()` is its JobIntake-bound alias, and both
flight-plan call sites (`do`, `do replan`) build a FlightPlan-bound
callable.

With the schema bug gone, `remedy do` in `tests/cli/test_scoped_listings.py`
performs a REAL flight-plan call (~72s measured), so the file's 30s
subprocess timeout — not scoping behavior — decided the verdict. Its
`_create_job` fixture now passes `--no-llm`, the convention the golden-path
canary already enforces for every subprocess `do` (`_run_do` appends the
flag unconditionally). No assertion was weakened; the file asserts nothing
about planning.

## 2026-07-29: F252 D10 — the fixture, not `test discover`, was broken
The catalog label ("discover-commands CLI rc=1 / non-JSON") is the symptom.
Diagnosis: both `_create_job_with_repo` fixtures in
`tests/test_command_discovery.py` ran `job create` against a bare
REMEDY_DATA_DIR with no registered project. Since F148 that exits 3 ("no
project found"), and the fixtures ignored the return code, so `job_id` was
`""` and every downstream `test discover ""` failed with `invalid job ID`.
Verified against product code: with a registered project, `test discover
<id> --json` returns rc=0 and a schema-v1 JSON document — no product defect.
Requiring a project is intentional F148 behavior, so making `job create`
project-less would be a product CHANGE and belongs to class D5, not here.
The fixtures now register the target repo and assert the rc, so a future
break is loud instead of silently producing an empty id.

## 2026-07-29: F252 D11 — translate BudgetConfigError at the fence boundary
`_load_fence_spec_effective` detected malformed fence config by scanning
`load_config().load_report.warnings` for "Malformed TOML". config.py now
fails closed EARLIER: `_load_toml(..., fail_closed_for_budgets=True)` raises
`BudgetConfigError`, so that diagnostic is never produced and the exception
escaped the fence API unchanged. Fix: catch `BudgetConfigError` around the
`load_config` call and re-raise as `FenceConfigError` with the existing
"refusing to default to allow-all on malformed config" message. The
diagnostic scan stays for the paths that still report rather than raise
(e.g. no TOML parser available). No behavior other than the exception TYPE
changes — the config was already fail-closed.

## 2026-07-29: F252 D9 — catalog classification drift, three distinct causes
1. `job.budget` carried `action_class="read_metadata"`, a value in neither the
   `ActionClass` Literal nor the integrity test's valid set — a one-off typo
   for a read-only "show" command, now `read_only` like `job.show`.
2. `do.job-evidence` executes `--verification-command` (`may_execute_commands
   =True`) while classified `read_only`, which catalog integrity forbids. It
   is now `test_execution`, like `test.run`. `tests/orchestration/
   test_job_evidence.py` asserted BOTH `read_only` and `may_execute_commands
   is True` in the same block — a contradiction that predates the
   verification-command feature; that assertion is updated with the catalog.
3. The `ActionClass` Literal listed 6 values while the catalog used 8; it is
   a plain type alias with no runtime validation, which is why the drift went
   unseen. Added `local_state_change` and `controlled_builder_execution` —
   both already in use and in the test's valid set.
Test-side: `TestCatalogSensitivity` scanned for `sk-` by substring and fired
on the word "task-scoped". Credential PREFIXES now match at a token boundary
(`(?<![0-9a-z])`); the field-name terms keep the plain substring scan, so no
check got weaker.

## 2026-07-29: F252 D7 — the shared module is the seam, not a private alias
`dev_server` re-exports only the redaction names it actually uses
(`_scrub_paths`, `_basename`, `_ABS_PREFIX_RE`); `_ABS_PATH_RE` and
`_FILE_URI_RE` were dropped when path redaction moved to
`packages/common/path_redaction.py`. Restoring private aliases purely so
tests can reach them would rebuild a seam the product does not have, so the
tests were pointed at the owning module instead: `test_supervisor_
portability.py` imports `ABS_PATH_RE` from `packages.common.path_redaction`
(2 use sites, both test-side path detectors). `test_the_shared_module_is_
the_one_f007_uses` kept its anti-drift intent and got stronger: three
identity assertions over the names dev_server really holds, plus a
behavioral check that a file URI does not survive `_redact`.

## 2026-07-29: F252 D5 — the creation guard is documented, so the tests moved
docs/system/project-scoping-v0.md ("Creation guard") and T0_F148 both specify
that `remedy job create` requires a resolvable project and exits 3 with a
fix-it hint; library functions stay permissive. Every D5 id is a fixture or
expectation written before that guard, so all 11 are honest test updates —
no product change:
- `TestCreateJobTaskType._env` (7 ids) now saves a RemyProject and exports
  REMEDY_PROJECT; these tests are about --task-type, not resolution.
- `test_attach_project_job_sets_metadata` creates the job under a SECOND
  project and attaches it to the first, so the asserted metadata can only
  come from attach — the old version would have passed trivially.
- `test_create_job_with_missing_project_warns` /
  `…_does_not_set_metadata` asserted the pre-F148 warn-and-continue path.
  Renamed to `…_exits_3` / `…_writes_no_job` and rewritten against the
  documented guard: exit 3, the fix-it text, no traceback, and no job file
  on disk (stricter than the old metadata check).
- `test_test_runner.py::test_permit_runtime_stderr` builds and registers the
  target repo before `job create`, D10 precedent.
Also fixed in the same file: `test_attach_project_repo_idempotent_message`
(catalogued D14) passed a bare directory to a path that has required a git
repo since F146 — the fixture now runs `git init`.

## 2026-07-29: F252 D13 — retired contract in tests, four real producer bugs
The 9 root-selection ids encode a contract Remedy retired on purpose:
01e2018 replaced mtime-based root-dir auto-selection with a hard error ("it
cannot distinguish features"), bd93397 downgraded that to warn-and-ignore so
code snapshots still build. Those tests now assert the live behaviour —
`remedy-job-evidence-*` root dirs are ignored with a counted warning naming
both remedies, `current_evidence` is null, nothing lands under `evidence/`,
and explicit `--evidence-dir` still selects. Tests whose NAME claimed
auto-selection were renamed; the explicit-selection tests are untouched.
Four product bugs surfaced behind the other two ids:
1. `build_manual_completion_gates` filtered caller runs to the v1.1 key set
   but stamped `schema_version: 1.1.0` without FILLING it — the coordinator
   rejected `runs[0]` and the final verifier lost its test total. Now
   normalized through `_vt_run_v11`, same derivations as `_run_verifications`.
2. …and dropped `head_sha`; the producer threads the bundle's head commit in.
3. `commit_execution_gate.json` hardcoded `runtime_integration_gate: PASS`
   while the packaged gate could say BLOCKED. The verdict is now read back
   from the artifact just written, with coherent non_pass/blocked/issues.
4. The runtime-integration gate is a SELF check — every pattern it looks for
   lives in Remedy's own tree — but the manual producer pointed it at the
   subject repo, so it reported "source file not found" for any non-Remedy
   target. It now scans Remedy's installed source root.
Test-side for the same id: the fixture declares `review_feature_id` (without
one the gate runs every historical feature's execution bindings) and lists
`node_ids` for the tests its run claims passed.
Fifth product bug, behind the last id: `_scrub_paths` dropped the FIRST LINE
of every text it redacted — aimed at pytest's rootdir banner, but applied
unconditionally, so any single-line command output was scrubbed to "". The
helper now only redacts.

## 2026-07-29: F252 slice E — a runtime port override, so the real-runtime tests stop fighting the product default
F251 closed 11 of 13 F-A ids with a per-worker test port, and stopped on the
two that drive the REAL apps/ui runtime of THIS repository: their port comes
from the product (config, else detection), so the only test-side fix would
have been editing the repository under test. Product change:
`REMEDY_RUNTIME_PORT` overrides the resolved port for ONE process, in
`resolve_spec`, validated like any other port and applied to both the config
and the detection path. The repository's own configuration is untouched, so
`remedy runtime serve` still means 5173 for an operator.
The runtime STATE file is repo-scoped and stays shared, so
`test_apps_ui_probe.py` also serializes across xdist workers on a file lock
kept in the system temp dir (not the repo — an untracked file there would
show up in `git status` and in the packaging detritus checks).
Verified: the four candidate ids green 3x consecutively, `tests/runtimes/`
green under `-n 4`, and no listener on the product default 5173 during or
after the runs.

## 2026-07-29: F252 D6 — real models instead of half-specced MagicMocks
`MagicMock(spec=Job)` pins attribute NAMES only: every field a test does not
set answers with another MagicMock, so product code comparing a budget or
reading fences fails on the mock, not on the behaviour under test
("'>' not supported between MagicMock and int"; "job_fences.allow must be a
list, got MagicMock"). All three builders now construct real `Job` models
(`test_test_execution_service._make_job` / `_make_contract` /
`TestExecuteTestRunGates._make_job_with_repo`, and
`test_test_runner._make_approved_job` reuses the file's existing real-Job
helper). No assertion changed; the gates under test now actually run. The
remaining MagicMock task fixtures in test_test_runner._make_job are untouched
— those tests pass and do not reach model-reading product code.

## 2026-07-29: F252 D4 remainder — context.md is maintained; the step-range pins retire
`.agent/context.md` was still F046-era. Rewritten to current reality (active
branch, F252 scope boundaries and constraints, resource-safety note, pointer
to plan.md), which turns the three content ids green:
`test_context_md_references_current_branch`, `test_context_md_no_stale_steps`,
`test_context_mentions_resource_safety`.
The other two ids asserted `Steps?\s+\d+-\d+` in context.md AND plan.md — the
numbered-step workflow that docs/roadmap/STATUS.md replaced with roadmap
features and rounds. plan.md is reviewer-authored and cmp-verified this
round, so it cannot be hand-edited to satisfy a retired convention, and
inventing a step range in context.md would be fabrication. Both assertions
now pin the LIVE contract: the feature id (`F\d{3}`), plus `## Active Branch`
and `feature/` for context.md and the AGENTS.md-required `## Goal` /
`## Next Steps` for plan.md. Nothing became optional.
Standing risk unchanged (F251 R2 finding): these ids read LIVE state files,
so ordinary bookkeeping still moves them. Recorded, not adjusted.

## 2026-07-29: F252 D1 — the docs moved, the tests did not
Every D1 id read an ist-doc at its pre-restructure flat path
(`docs/<name>.md`); all of them now live under `docs/system/` or
`docs/guides/` with `docs/README.md` as the index. No doc is missing, so the
fix is the path in the test — ten documents across nine test files.
`tests/cli/test_product_spine.py` needed more than a path: its `_read_doc`
helper returned `""` for a missing file, so every assertion over a moved doc
was passing against an empty string. It now resolves docs/system, docs/guides
and docs/ in order and RAISES when the doc is absent — which turned six
further ids green once they started reading real text.

## 2026-07-29: F252 D14 (the 13 README pins) — the README stopped being a spec dump
bd2f8ad deliberately replaced a 222-line spec-dump README with a concise
overview ("condensed pitch, <=120 lines"), deleting the F012 contract prose
and the per-feature `| F010 … externally accepted` table. Thirteen pins still
asserted that deleted text, so they pinned a documentation design the repo
had already retired.
- The twelve `TestF012Round*IsPinned::test_..._readme_states_...` ids now pin
  the same contract in the document that owns it, `T0_F012.md` — every one of
  those classes already reads that file for its sibling assertions, and where
  the exact phrase survives there (root of trust, raw-byte identity, gate
  matrix, review subject, typed transaction) the phrase itself is asserted.
- `test_the_readme_reports_the_accepted_foundation_and_no_later_feature` is
  now a cross-check against the ledger: every feature the README lists in an
  "Accepted …:" block must carry `- [x]` in STATUS.md. That fails on real
  drift instead of on layout, and it caught the drift it was meant to: the
  README still said "13 of 250 features accepted. Next: F081". Updated to the
  ledger's truth (24 of 252, Tier 0 complete, the eight accepted Tier 1
  items, F252 in progress) in this same commit.
Two named clauses ("F012 must never be called accepted yet", the same for
F017) were dropped: STATUS.md carries `- [x]` for both, and the general
cross-check subsumes them.

## 2026-07-29: F252 D14 (misc) — six retired contracts and two product bugs
Retired contracts, repinned to what the product does today:
- `test_no_new_product_dependency`: `fresh_evidence_gate.py` genuinely reads
  `.agent/live_review.md` (it is the gate OVER development state) and is
  allowlisted with that reason; `repair_attest.py` only NAMES the file in a
  docstring to say it is excluded, so the scanner now strips docstrings — a
  module may document the boundary it honours.
- `test_run_log_event_has_exact_metadata_keys` / `…_scope_is_project`: F146
  (2727114) made `project context` strictly read-only and removed its RunLog
  write. The pin is now that read-only contract.
- `TestUiRebuildSpecDocument` (3 ids): the v2 spec delegates palette,
  forbidden words and zoom levels to `docs/ui/design_reference/`. The pins
  follow the delegation and require the target file to exist, so a dead
  pointer still fails.
- `test_full_chain_order`: since the proof-chain hardening, unlinked test
  evidence is never claimed as proof of a change; the fixture's test event now
  names the intent it tested.
- `test_root_style_evidence_still_readable_but_deprecated` → `…_is_ignored…`:
  same retirement as D13.
- `test_default_out_goes_to_hidden_dir_and_indexes`: the bare
  `Path.cwd().glob("remedy-job-evidence-*")` also caught legacy dirs an
  operator left in the checkout; it now looks for pollution from THIS export.
- `test_viewer_sanity_block_has_no_bare_assert`: BARE means "without a
  message"; the blanket ban on the word forbade the fixed form too.
- The three `invalid_job_id` ids: that token is a stop_reason of the test
  execution service. The job CLI reports a bad id on stderr and exits
  non-zero; the pins now assert exit code, the named stderr error, no
  traceback and NO partial JSON on stdout.
- `test_the_cli_resumes_a_16_char_jobplan_id`: max-tasks is an F012 material
  control carried in RunInvocation, not a bare kwarg.
- `tests/test_test_runner.py::TestCliRunTestsLocal`: D5/D10 fixture
  precedent — register a project before `job create`.
Product bugs:
1. `project_registry.resolve_project` swallowed EVERY exception around
   `repo_root`; now the named failures only (WorktreeError, OSError,
   SubprocessError) — a defect is no longer hidden as "no project".
2. `pingpong_loop._build_provider_evidence` omitted provider_call_count /
   actual_call_count / cost_call_count when no usage was measured, although
   ProviderTokenEvidenceV1 REQUIRES them for execution_mode='provider_backed'.
   token_truth.json therefore refused to build and the artifact-contract gate
   went BLOCKED on a clean export. Zero is the honest count; the one test that
   asserted the ABSENCE of those fields now asserts the schema.

## 2026-07-29: F252 D3 + D12 — the two operator-decision classes, executed
D3 (10 ids): the pre-rebuild `apps/ui/src/components/graph/legacy/*.tsx`
sources these assert (RemedyBrainFlow.tsx, semanticZoom.ts, the organic
layout, the old index.html markers) are not in the tree — the graph directory
holds the rebuilt components instead. Nothing to fix before the UI is rebuilt,
so each id carries `@pytest.mark.skip` with its own reason string and the
backlog reference "Tier 5 UI build (F019+)". No file deleted, no assertion
weakened, no blanket directory skip.
D12 (1 id): git history answers it — 219dd32 deleted
`.claude/agents/remedy-reviewer.md` deliberately as finding R-0074
("superseded by split workflow Window 1"). A reasoned removal, so per the
round's rule it is quarantined rather than restored; the skip names the
commit, the finding, and the document that now carries the read-only
reviewer contract (docs/agents/planner_reviewer_prompt.md).

## 2026-07-29: F252 R4 — closure stopped at the README/STATUS ordering conflict
The closure block sequences the README status sync (step 3) BEFORE the STATUS
`[x]` (step 8, Rule A4's last commit). Those two cannot disagree in any
committed state: the ledger cross-check added in R2 requires every feature
named in an "Accepted …:" README block to carry `- [x]` in STATUS.md, so
appending "F252 standing-red paydown" while STATUS still reads `- [~] F252`
fails `test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
("README claims F252 accepted; STATUS does not").
The block anticipated this and ordered a STOP rather than a self-chosen
reordering, so: README reverted, branch green and clean, no evidence job, no
zip, no STATUS edit, no PR. The natural resolution is to fold the README sync
into the step-8 commit — which also satisfies Rule A4 — but that is the
reviewer's call, recorded in .agent/last_block.md as options (a)/(b)/(c).

## 2026-08-01: paydown-0801 — closure-candidate carrier + two F056 candidates settled

Operator finding (accepted 2026-08-01): the two CANDIDATES parked at the
F056 closure were silently dropped by the next session — the
closure-candidate rule mandated a carry but defined no DISK vehicle;
candidates lived only in the closing session's chat brief, which a fresh
window never reads. Three DECISIONs, applied in a single-session
micro-round (round type per planner_reviewer_prompt.md §3), each
reversible by any later relay:

1. Disk vehicle: closure candidates are ALSO written to
   .agent/candidates.md inside the closure commit; the Window-1
   bootstrap reads it; a non-empty file at feature-claim time is a
   block condition. Amended: STATUS_closure_protocol.md
   (Closure-candidate findings) + planner_reviewer_prompt.md §1
   step 4. Alternative considered: keep brief-only carry — rejected,
   it is exactly what lost the F056 pair.
2. Evidence-protocol drift (F056 candidate a, resolved inline, no
   R-id spent): the protocol ordered an evidence-dir commit after the
   READY zip while .gitignore excludes remedy-job-evidence-*/ and the
   F050–F061 closures committed none. Amended the protocol to match
   standing practice: the evidence dir is NOT committed; the durable
   pointer is package name + SHA-256 + evidence job id in the STATUS
   line. Alternative considered: start committing evidence dirs —
   rejected: contradicts .gitignore, the F147 attempt-2 lesson, and
   six closures of precedent.
3. PR-number reporting (F056 candidate b, resolved inline, no R-id
   spent): handback_template.md "External actions" now states that PR
   create entries include the resulting PR number — settles the F056
   miss (that closure handoff omitted the PR number).

## 2026-08-04: F075 T001 — evaluator interfaces (module, evidence layout, order schema)

Four interface decisions, recorded before the code they bind (T1_F075.md
T001 asks for exactly these):

1. **Module split.** The pass definition lives in
   `packages/orchestration/gauntlet_evaluator.py` — an importable, pure
   module with no execution and no provider calls; the CLI
   `scripts/self_run_gauntlet.py` stays thin. Alternative considered:
   logic inside the script — rejected, `--dry-run` against recorded
   evidence is only a proof if the judged code is the same code the real
   campaign will use, and a script is not importable by the tests that
   prove it.
2. **Recorded-evidence layout consumed.** `<evidence-dir>/<run-dir>/`
   with `run.json` (required, `gauntlet_run_version: 1`) and an optional
   `dod_result.json` holding the stored `dod_gate.GateResult` JSON
   verbatim. Run order is the sorted run-directory name — a property of
   the bytes on disk, so two readers produce the same matrix. `run.json`
   carries: order_id, kind, terminal_status, wall_seconds, tokens{in,out},
   operator_interventions[], data_root_hash_before/after, postmortems[],
   open_decisions[], era_defects[], injections[], evidence_links{}.
   Alternative considered: one flat JSON per campaign — rejected, failed
   attempts are KEPT and a per-run directory is what links into that
   run's own evidence.
3. **The DoD verdict has one author.** The evaluator asks
   `dod_gate.gate_blocker` for the blocker line through a small adapter
   over the stored JSON instead of re-deriving it from the same fields
   (A6: the gauntlet reimplements no product verb). A run with no stored
   gate result fails `dod_blocking_green` with the honest reason that no
   gate ran — never a silent pass.
4. **Injection dispositions are a closed set.** Accepted:
   `ledgered_failure`, `retry_within_budget`, `escalated` (F051
   semantics). Named mishandlings: `silent_success`,
   `corrupted_artifact_accepted`. Anything else is `unclassified` and
   fails. An unknown injection *class* is malformed evidence, not a new
   failure mode — the four classes are frozen by the operator addition
   of 2026-08-03.

Also frozen here: an empty evidence directory does NOT pass. Vacuous
truth is the single most likely way this gate would lie about 10/10.

## 2026-08-04: F075 T002 — where the frozen ten live, and what freezes them

1. **Location: `scripts/gauntlet_orders/`**, beside the CLI that runs them.
   Alternative considered: the tests fixture area — rejected, these are
   campaign INPUT rather than test data, and filing real input as test
   data is how it quietly becomes editable mid-campaign (exactly what
   T1_F075.md A9 forbids).
2. **Order-file schema (`gauntlet_order_version: 1`)**: id, kind, title,
   `rationale` (prose: why this order probes a risk no other order
   probes), `risk_probed` (slug), goal, milestones[], budget
   {max_iterations, max_tokens, max_wall_seconds} — all three required
   and positive, because an unbounded run cannot fail a budget — and an
   optional `injections[]` naming the harness-failure classes this order
   injects. The rationale is a FIELD rather than a JSON comment so a test
   can assert it is present and distinct.
3. **Freeze mechanism**: `manifest.json` carries
   `gauntlet_order_set_version: 1`, one sha256 per order file, and a
   `set_hash` over the `<sha256>  <file>` lines in manifest order. Order
   is part of the hash on purpose — reordering changes which order
   `--only 3` selects, so it is a change to the set. `load_order_set`
   refuses on the first mismatch rather than reporting a soft finding:
   running a campaign against a set the manifest does not describe proves
   nothing about either.
4. **Regenerating the manifest is a deliberate human act.** No script
   rewrites it as a side effect of loading — the whole point is that an
   edit is loud. Bumping the set version resets the gauntlet count.

## 2026-08-04: F075 T003a — injection seams, and the one that is missing

**Finding for the reviewer (no R-id claimed — Window 1 assigns it):
`orchestrator_loop.run_mission` has no exception boundary.** Its body
(lines 698–886) contains no `try`/`except` at all, `execute_move` wraps
none around `dispatch`, and `structured_outputs.run_structured_call`
retries PARSE failures only — never an exception. Verified by running
the real code, not by reading it:

- a raising `call_fn` propagates out at `orchestrator_loop.py:834` →
  `structured_outputs.py:158` (`RuntimeError` escaped `run_mission`);
- a raising `update_dossier` propagates out at
  `orchestrator_loop.py:811` (`OSError` escaped `run_mission`).

In both cases the iteration leaves NO ledger entry, NO F010 postmortem
and NO terminal — the loop cannot degrade a failure it never catches.

Consequence for T003a: three of the four harness-failure injection
classes (provider API error mid-move, harness death mid-dispatch,
harness death mid-write) cannot be driven honestly today. The seams
themselves all exist and are already public parameters of `run_mission`
(`call_fn`, `dispatch`, `update_dossier`) — what is missing is the
boundary that turns a raised failure at one of them into a classified
postmortem plus an honest terminal or an F051 escalation. Per the
round's HARD RULE this is a product change of its own, with its own
tests, and was NOT smuggled into the harness.

Decisions taken:
1. **Blocked classes are REFUSED, not silently skipped.**
   `gauntlet_injection.check_injections_supported` raises
   `MissingSeamError` naming the class, its seam and the missing
   boundary. Alternative considered: run g06/g08/g09 without their
   injections — rejected, a run.json that omits a declared injection is
   a lie by omission in exactly the artifact a human trusts when
   flipping defaults.
2. **No harness-side `except` around the seam to fake resilience.**
   If the runner absorbed the raise itself, the gauntlet would be
   grading its own crutch rather than the product. The runner still
   catches a crashed `run_mission` at the CAMPAIGN level — a crashed
   run is a FAILED run, recorded as such — which is harness
   bookkeeping, not product resilience.
3. **`truncated_model_response` is injectable today** and is driven at
   the `call_fn` seam: the first attempt of move 1 returns a payload cut
   mid-object. It RETURNS rather than raises, so `run_structured_call`
   classifies it parse-class and re-prompts once — the real
   retry-within-budget path. The disposition is read off what the
   product did: no re-prompt → `silent_success`; re-prompted and the
   mission reached a green terminal → `retry_within_budget`; re-prompted
   without recovery → `ledgered_failure`.
4. **Injectors are decorators around the production callable** the
   runner would have passed anyway — no product edit, no test-only
   branch on a production path.

## 2026-08-04: F075 R3 — R-0179 closed-set tightening (pre-freeze)

`injection_never_fired` joins `REJECTED_DISPOSITIONS`. A declared fault
that never fired proves nothing about degrading it, so settling it as
`ledgered_failure` — an ACCEPTED class — let a run count flawless while
its evidence claimed a failure-handling that never happened.

This CHANGES the pass definition's closed set. It is allowed without an
ADR because it lands BEFORE any campaign has run: T1_F075.md freezes the
definition at campaign time, and attempt 1 has not started (R2's attempt
was refused at preflight, zero runs recorded). Any later change to this
set needs an ADR. Alternative considered: leave it and rely on
INJECT_ON_MOVE=1 making a never-fired injection unreachable in practice
— rejected, that is an accident of one constant defending a pass
criterion, not a rule.

## 2026-08-04: F075 R3 — the run_mission exception boundary (product change)

Built per the R2 verdict's DECISION. Four naming/shape decisions:

1. **Terminal name: `iteration_failed`** (new constant, alongside the
   existing honest terminals). Alternatives considered: reuse `aborted`
   — rejected, that means the orchestrator DECIDED to give up, and a
   crash is not a decision; reuse `invalid_move` — rejected, that means
   the provider answered with something unusable, and here the work
   itself threw. The reader of a matrix must be able to tell those three
   apart.
2. **Scope of the catch: `except Exception`, once per iteration**, around
   the iteration's own work (refresh -> assemble -> provider call ->
   evaluate -> execute). `KeyboardInterrupt` and `SystemExit` derive
   from `BaseException` and are therefore NOT caught — an operator
   stopping Remedy is not a failure to classify. The safe point and the
   mission-record read stay OUTSIDE the boundary: reading a stop request
   is not the iteration's work.
3. **No retry in the boundary.** One catch, then the run ends. Transport
   retries live below `call_fn` (F001) and a second attempt here would
   hide them; `run_structured_call` keeps its single PARSE retry, which
   is a different thing.
4. **Post-mortem placement: `<mission evidence>/iteration_<n>/`**, scope
   `job`. `write_postmortem` is create-only by design, so two failing
   iterations in one mission would otherwise collide over the account of
   the first. `record_iteration_failure` never raises: a post-mortem that
   could not be written is reported in the run's detail rather than
   becoming a second, louder failure on top of the first.

Escalation was considered and NOT used: F051's escalation asks a human a
QUESTION (the twice-refused-move path). A raised failure is not a
question, it is a failure to ledger — so the boundary ends the run on an
honest terminal and leaves escalation where its semantics actually apply.

**Campaign observation, not fixed here:** a realistic HTTP-level provider
error ("HTTP 503 from the host", "connection refused") classifies as
`unknown` — `failure_postmortem` recognises missing binaries and timeouts
but not transport status codes. That will cost the injected
provider-API-error order its `no_unknown_postmortems` criterion. Left
alone deliberately: bending the injected error text to force a nicer
class would be gaming the gate, and finding exactly this kind of thing is
what attempt 1 is for (a targeted fix order in R4+).

## 2026-08-04: F075 R3 — unblocking the three raise-class injections

1. **One decorator shape for all four.** `RaiseOnceInjector` raises once at
   its seam then delegates to the production callable, mirroring
   `TruncatedResponseInjector`. `build_injectors` now returns an
   `InjectedSeams` triple (call_fn / dispatch / update_dossier) instead of
   just a call_fn, and `RunnerDeps` gained `dispatch_fn` /
   `update_dossier_fn` defaulting to `run_mission`'s own defaults
   (`continue_mission`, `update_mission_dossier`) so a wrapper decorates
   the real path rather than a stub.
2. **Dispositions come from `RunOutcomeFacts`** — the run's terminal plus
   the number of post-mortems collected — never from the injector's own
   view. `iteration_failed` + a post-mortem = `ledgered_failure`;
   `escalated` = `escalated`; a GREEN terminal after the fault fired =
   `silent_success`; an honest terminal with NO post-mortem =
   `unclassified`, because the terminal alone is not the whole contract.
3. **Realistic error text, deliberately not tuned.** The injected messages
   are what a real 503 / killed process would say. A message invented to
   earn a nicer `failure_postmortem` class would be gaming the gate.
4. **`BLOCKED_INJECTIONS` kept as an empty mapping** rather than deleted,
   with its refusal path and test intact: an unknown class must still be
   refused before the first provider call, which is what stopped R2's
   campaign from spending tokens it could not judge.

**Test-safety lesson (self-inflicted, recorded so it is not repeated):**
once the preflight stopped refusing, the R2-era CLI test
`test_a_live_campaign_refuses_while_an_injection_class_is_blocked` fell
through to `cli.main(["--live", ...])` with PRODUCTION deps and started a
real ten-order campaign inside pytest. It was killed within ~2 minutes.
Host isolation HELD (run_order enters `isolated_environment` before it
creates anything, so every write landed in the run's own data root under
tmp_path; `git status` clean, real data root untouched), but real provider
calls were made. The live CLI path is now exercised ONLY with doubles or a
monkeypatched order set, and the two obsolete tests were replaced by
preflight-level ones that cannot start a campaign.

## 2026-08-04: F075 R3 — attempt 1's matrix had to be written after the fact

The block's Phase 6 step 3 assumed `--live ... --format both` leaves
`matrix.md` + `matrix.json` in the campaign root. It did not: `--format`
only chose what reached stdout, and `--out` (which writes files) was not
part of the ordered invocation. The campaign therefore finished with its
report existing only on a terminal — a campaign nobody could archive.

Resolved WITHOUT rerunning anything. The evaluator and the report are
pure functions of the recorded evidence, so the matrix was re-derived
from the run directories attempt 1 had already written and PROVEN
byte-identical to what the live invocation printed (compared against the
captured stdout: `printed == md + js` -> True). No provider was called
again, no run was repeated, no order was edited.

Gap fixed in the same round: `--live` now always calls `write_matrix`
into the campaign root, with a test. `--format` keeps meaning "what
reaches stdout" and `--out` keeps meaning "also write here".

**Observation for the reviewer, not fixed:** `RunVerdict.to_json` — and
therefore the matrix — reports the `injections_degraded` criterion but not
which fault got which disposition; that detail lives only in each run's
`run.json`. Surfacing it would change the golden matrix bytes, so it is
left for a ruling rather than taken unilaterally.

## 2026-08-04: F075 R4 — R-0185, transport and machine classes

Inspected the F001 taxonomy first: `provider_timeouts.is_timeout_error` /
`is_nonzero_exit_error` (both retry predicates) plus F010's local
`is_provider_unavailable_error` (a MISSING BINARY, deliberately not a
retry predicate). Three provider classes already exist. Decisions:

1. **`ConnectionError` -> `PROVIDER_UNAVAILABLE`**, an existing class, not
   a new one. The provider did not serve the call; whether the binary is
   absent or the socket died is different EVIDENCE for the same fact.
   Recognised by type and by a new local predicate
   `is_provider_connection_error` (refused/reset/aborted/closed, broken
   pipe, HTTP 500/502/503/504). The F001 retry predicates are untouched —
   widening those would change retry behaviour, which is not this finding.
2. **New enum member `IO_FAILURE = "io_failure"`** for the machine under
   us: a killed process, a full disk, an unreadable device. Not a parallel
   spelling of any `provider_*` class — nothing about the provider went
   wrong. Recognised by a bare `OSError` and by a narrow text predicate.
   Alternative considered: reuse `STOPPED` — rejected, that is F011's
   deliberate kill switch, and calling a crash a deliberate stop is a lie.
3. **Ordering matters and is commented in the code.** In Python 3.10
   `TimeoutError`, `ConnectionError` and `FileNotFoundError` are all
   `OSError` subclasses, so the bare-`OSError` rule is LAST; in the text
   path a provider reading wins over a machine reading, because a provider
   error that also mentions a pipe is still a provider error.

Two existing tests were touched, both by EXTENSION rather than weakening:
- `test_every_enum_member_is_reachable` gained a producing signal for
  `IO_FAILURE`. Without it the test correctly fails — a class nothing can
  produce should not exist.
- `test_a_class_it_cannot_determine_is_recorded_as_unknown` (mine, R3) used
  "HTTP 503 from the host" as its unclassifiable example. That WAS the
  dishonest unknown R-0185 fixes, so the input became a genuinely
  unrecognisable message. The assertion is unchanged and the falsification
  still stands: `ValueError`/`RuntimeError`/`KeyError` and nonsense text
  all still classify as `unknown`.

## 2026-08-04: F075 R4 — R-0183, unmeasured cost is not a measured zero

`RunEvidence` gained `tokens_measured`. Measured means someone actually
counted: the `tokens` object is present, at least one side of it was
recorded, and the run did not itself declare `tokens_source:
"unmeasured"`. A run that really spent zero stays MEASURED — relabelling
a true zero would be the same lie in the other direction (test pins it).

Rendering only; no pass criterion moved:
- markdown: the tokens column says `unmeasured`, and the per-run line
  reads `· tokens unmeasured` instead of `0 in / 0 out`.
- json: `tokens_in`/`tokens_out` are `null`, and every run payload now
  carries `tokens_source` ("measured" | "unmeasured") so a machine reader
  never has to guess whether a zero was counted.

**Golden regeneration declared:** `golden/matrix.json` +9 lines — one
`tokens_source` key per recorded run. `golden/matrix.md` is byte-identical
because every recorded fixture carries a measured `tokens` object; the new
wording only appears when a run is unmeasured, which the new tests cover
with their own evidence rather than by editing the fixtures.

## 2026-08-04: F075 R4 — R-0184 diagnosis: the loop dispatches jobs but never runs them

One cheap live run, `--live <scratch>/diag-r0184 --only 1 --format json`,
exit 1, terminal `iteration_limit`. It reproduces attempt 1's g01 exactly,
so the finding is not a one-off.

**(a) What moves does the model produce.** Well-formed, schema-valid, and
reasonable. Six iterations, six `dispatch_job` moves for the SAME
milestone. Iteration 1, verbatim from the run's ledger (trimmed):

    {"iteration": 1,
     "move": {"kind": "dispatch_job",
              "payload": {"milestone_id": "M001",
                          "step": "identify_location_of_hardcoded_retry_backoff_cap_..."},
              "rationale": "M001 is the first milestone and is ready; need to
                            locate and refactor the hard-coded backoff cap ...",
              "schema_v": "om1"},
     "outcome": {"status": "dispatched",
                 "detail": "job d18005fc-... dispatched for M001"}}

The model is not the blocker. Every move parsed, none was refused, and the
rationale is on-topic.

**(b) Do dispatched jobs run and finish.** No. All six job records sit at
`state = planned` with their tasks built and never touched:

    1e384c8b state=planned tasks=2   7e7bfae7 state=planned tasks=2
    81df99a0 state=planned tasks=2   a0268bd5 state=planned tasks=2
    b092254d state=planned tasks=2   d18005fc state=planned tasks=1

`execute_move`'s dispatch branch is `create = dispatch or continue_mission`
— which creates the job, builds its plan verify-first, links it to the
mission and auto-approves the plan gate. Creation is where it stops.
Nothing in `run_mission` executes the job it just created.

**(c) Why `declare_milestone_done` / `declare_mission_achieved` is never
reached.** Because it never becomes true. `evaluate_milestone_done` wants a
finished job with a released gate; the job never leaves `planned`, so the
orchestrator's only remaining useful move is to dispatch again. The mission
record after six iterations: `status=active`, `_milestones_done=None`,
`job_links=6` — six jobs for one milestone. `evaluate_dispatch` refuses an
already-DONE milestone, an unknown one, and unmet dependencies; it does NOT
refuse a milestone that already has an in-flight job, so the loop is free to
re-dispatch forever.

**(d) Why the DoD gate never runs.** Never invoked at all — not invoked and
failing. No `dod.json` and no `dod_result.json` exists anywhere under the
run's data root. `run_job_gate` has exactly one caller in the tree,
`job_fulfillment.py:1003`, which is part of JOB EXECUTION. No execution, no
gate. That is why `dod_blocking_green` was red on all ten runs of attempt 1
with the honest reason "the DoD gate never produced a verdict".

**Root cause.** `orchestrator_loop.py`'s own module docstring states the verb
map: "`mission_state.continue_mission` dispatches, `long_run_executor`
executes, `dod_gate` evaluates". The loop imports `long_run_executor` only
for `next_cycle_index` (line 377, ledger numbering). It never calls
`run_cycles`. T1_F070's Design specifies the iteration as "pick or shape the
next job as a Flight Plan -> run it through the multi-cycle executor ->
evaluate against the milestone's DoD"; the built loop implements the first
step and the last, and omits the middle one.

**Decision fork -> rule 2c: STOP with the analysis.** This is not a bounded
wiring bug. Closing it means running each dispatched job through
`long_run_executor.run_cycles` inside the loop with the order's budgets,
stop/safe-point handling and cycle accounting, then letting the DoD gate
produce its verdict, plus a re-dispatch guard in `evaluate_dispatch` so one
milestone cannot accumulate six jobs. That is the missing half of F070's
design — a product feature with its own tests, and precisely the kind of
change the gauntlet exists to demand rather than to smuggle. Explicitly NOT
done here: no `orchestrator.model` change (the model is not the blocker and
config defaults by machine are do-not-touch), no order edits, no weakening
of the pass definition.

Attempt 2 therefore does NOT run this round: Phase 5 is gated on a green
2a+3, and this is 2c.

## 2026-08-04: F075 R5 — R-0186 execution wiring, and the third link that is missing

Built: (1) a dispatch now RUNS its job, (2) the re-dispatch guard.

1. **`execute` seam on `run_mission`/`execute_move`**, defaulting to the new
   `execute_dispatched_job`, which is a thin call to the EXISTING
   `long_run_executor.run_cycles` with `limits_from_config` (so the F046
   rollout cap still applies exactly as for `remedy job run`),
   `default_task_step`, the job's own budgets and `unattended=True`. No second
   executor: a test asserts the function's source names `run_cycles`,
   `limits_from_config` and `default_task_step`. The move outcome records
   `terminal=`/`job_status=`/`stop=` so the next iteration's context shows why
   a milestone is or is not claimable.
2. **Re-dispatch guard** in `evaluate_dispatch`: a milestone whose job is
   `pending`/`planned`/`running` refuses a second dispatch and the refusal says
   what to do instead. `paused` is deliberately EXCLUDED — see below.
3. **Test-safety (R-0182):** the executor default builds a real
   `OllamaBuilder`, so every test that dispatches must inject the seam exactly
   as it already injects `dispatch`. 29 call sites in
   `test_orchestrator_loop.py` gained `execute=_executed`; `test_mission_e2e.py`
   gained `_no_execution`. Discovered the honest way: the first Phase-2 gate
   run HUNG on a real provider call and was killed.

**`paused` is not guarded, and that is a finding-shaped fact, not a
convenience.** The move schema has five kinds — dispatch_job,
wait_on_decisions, declare_milestone_done, declare_mission_achieved,
abort_with_reason — and NO resume kind. Refusing a dispatch for a paused job
would leave the loop with no legal move that advances the milestone after a
human answers its decision: a deadlock in place of a defect. Re-dispatch is
therefore the only forward path out of a paused job today. Recorded for the
reviewer; NOT fixed here (a resume verb is its own reviewed change).

`test_mission_e2e.py`'s executor double also sets the job it "ran" to
`paused` and saves it. A real executor always takes a job out of `planned`;
the double previously left it there, which is only invisible while nothing
executes. That is test fidelity restored, not an assertion weakened — no
assertion in that file changed.

### The third link: the DoD gate is not reachable from real execution

Phase 2's premise was "the gate verdict comes from the EXISTING job-execution
path (job_fulfillment -> run_job_gate)". Verified in source, it does not exist:

- `run_job_gate` has exactly ONE caller, `job_fulfillment.run_job_fulfill`.
- `run_job_fulfill` has NO production caller — only tests. The CLI merely
  READS fulfillment records (`list_fulfillment_records`).
- `job_fulfillment`'s module docstring: "Job Fulfillment Spine **v0** ... v0
  supports **fixture-demo mode only** (deterministic, no real provider)", and
  its `fixture_plan_tasks` hardcodes two tasks ("Update CHANGELOG.md", "Add
  verification evidence summary") regardless of the job.
- `dod_gate.store_dod` — the only way a job gets a DoD for the gate to read —
  has NO caller anywhere in `packages/` or `apps/`. Milestone DoDs are written
  into the MISSION's evidence area by `attach_milestone_dods`, never attached
  to the dispatched job. `run_job_gate` on such a job returns None by design
  ("a job with no stored DoD ... changes nothing").

So a DoD verdict cannot be produced by executing a job today, and the two ways
to make one appear are both refused here: calling the fixture-demo spine would
make the gauntlet grade a demo (the R2 "grading its own crutch" rule), and
calling `run_job_gate` from the loop is explicitly forbidden by this round's
own order ("do not call the gate from the loop directly"). Attaching the DoD at
dispatch plus a production fulfillment invocation is new product work of the
same class as the R2 seam and the R4 2c — it is NOT this round's ordered scope.

Consequence: Phase 3's hard gate (terminal `achieved` AND `dod_result.json`
present) cannot be met by construction. The run was still executed as ordered,
because whether execution now advances jobs and reaches `achieved` is real
evidence the reviewer needs; its trail is recorded below.

## 2026-08-04: F075 R5 Phase 3 — re-proof evidence, and the STOP

`--live <scratch>/reproof-r0186 --only 1 --format json`, exit 1, terminal
`waiting_on_decisions`, no `dod_result.json`. Phase 3 requires `achieved`
AND a gate verdict, so rule 3.3 applies: STOP, both trails recorded here.

**What R-0186 demonstrably fixed** (ledger of the re-proof run, verbatim
details, trimmed):

    it1: dispatch_job -> dispatched
         job 0db084c6 ... dispatched for M001; executed:
         terminal=all_green job_status=completed
    it2: dispatch_job -> dispatched
         job 20fba26e ... dispatched for M001; executed:
         terminal=max_cycles_reached job_status=running
    it3: dispatch_job -> refused
         milestone M001 already has job 20fba26e in flight (state running);
         a second job for it is refused. Instead: wait_on_decisions, or
         declare_milestone_done once that job finishes and its gate releases
    it4: wait_on_decisions -> waiting_on_decisions

Job states after the run: `0db084c6 completed` (1 task), `20fba26e running`
(2 tasks). Compare the R4 diagnostic run, same order, same model: six
`dispatch_job` moves, six jobs, ALL `planned`, nothing executed, nothing
refused. So: jobs now really execute (a job reached `completed` through
`run_cycles`), and the six-identical-dispatches loop is gone — the guard
refused the third dispatch with the message it was built to give.

**Why the run still did not reach `achieved` — two blockers, neither in
this round's scope:**

1. **`CYCLE_SAFETY_CAP = 1` (and `DEFAULT_MAX_CYCLES = 1`).** A job needing
   more than one cycle ends `max_cycles_reached` with `job_status=running` —
   never a terminal state — and `evaluate_milestone_done` refuses a claim
   whose job "is in state 'running', which is not terminal". The loop has no
   resume kind, so that job can never finish. The cap's own docstring says it
   stands "until the F075 milestone gate raises it": the gate is expected to
   raise the cap, and the cap prevents the gate from passing. That
   chicken-and-egg is a reviewer DECISION — raising it is a config default by
   machine, explicitly do-not-touch for the worker.
2. **No DoD verdict is reachable** (recorded in full above): `store_dod` has
   no caller, and `run_job_gate`'s only caller is the v0 fixture-demo spine.
   Note the nuance: `evaluate_milestone_done` refuses only on
   `gate_released is False`, and an absent DoD leaves it `None` — so a claim
   is not blocked by the missing gate. It is blocked by blocker 1. But the
   gauntlet's `dod_blocking_green` criterion still cannot be satisfied by any
   run, because no run can produce a gate verdict at all.

Not done, deliberately: no change to `CYCLE_SAFETY_CAP` or any config
default; no call from the loop into `run_job_gate`; no use of the fixture-demo
spine; no order edits; no weakening of the pass definition. Campaign attempt 2
did NOT run — Phase 4 is gated on a green Phase 3.

## 2026-08-04: F075 R6 — R-0187 cycles experiment vehicle + order-set v2

1. **`experiment_max_cycles` on `resolve_max_cycles` / `limits_from_config`.**
   Keyword-only, documented as existing for exactly one caller (the F075
   gauntlet runner), and deliberately NOT reachable from config or a CLI
   flag — a caller must pass it in code, by name. `ResolvedCycles.source`
   becomes `"experiment"` and a new `to_json()` carries `over_cap`, so a run
   past the rollout cap is a fact on disk rather than an inference. F046's
   shipped clamping is untouched; both directions are pinned
   (flag 99 -> 1 capped, config 99 -> 1 capped, override 6 -> 6 uncapped,
   nothing passed -> exactly today's default).
2. **`JobExecution` carrier.** `CycleLoopResult` is a frozen dataclass, so the
   resolved cycles could not be attached to it. `execute_dispatched_job` now
   returns a small frozen carrier with the three fields the loop already read
   plus `resolved_cycles`. Test doubles expose the same attribute names, so
   the seam stays substitutable. Alternative considered: mutating the
   executor's result type — rejected, that is F046's contract, not F075's.
3. **Order-set v2.** Every order's budget gains a required `max_cycles`, chosen
   from the order's own rationale rather than copied: doc orders 3, pure-code
   and test-add 4, app-feature-with-smoke 5, two-milestone 8; the injection
   orders match their non-injected twin. Manifest is
   `gauntlet_order_set_version: 2` with fresh per-file digests and set hash
   `b17540c381312b2c5dd40140396d1a489c0001c342572bb3276fc1ca9c6b994c`.
   Per T1_F075.md A9 a set re-issue RESETS the campaign count — which costs
   nothing: no attempt has ever passed. Every existing freeze/tamper pin holds
   against v2 unchanged.
4. **Runner pass-through.** `RunnerDeps.execute_fn(max_cycles) -> execute seam`,
   production default `_default_execute_fn`, bound at `run_order` from
   `order.budget["max_cycles"]`. `run.json` records `cycles_budget` and
   `cycles_resolved` (read back off the ledger's `cycles=<n>/<source>` marks —
   the runner re-derives nothing).

One existing test was touched, by EXTENSION not weakening:
`test_an_unknown_set_version_is_refused` used the literal `2` as its unknown
version, which set v2 turned into the real one; the example became
`GAUNTLET_ORDER_SET_VERSION + 1` and the assertion is unchanged.
`test_the_set_is_frozen_at_version_one` was renamed to
`..._at_the_declared_set_version` — its body already compared against the
constant, so only a now-false NAME changed.

## 2026-08-04: F075 R6 — R-0188 the production DoD path

Shapes inspected first: `store_dod(job_id, DoD)` writes `dod.json` into the
job's evidence area; `run_job_gate(job_id, worktree_root)` reads that file,
evaluates, AND persists via `save_gate_result` — so it is already the single
author of a verdict; `load_gate_result(job_id)` reads the same place. F069
compiles each milestone's DoD into the MISSION's evidence area as
`dod_<milestone>.json` and records the filename in the milestone's `dod_ref`.

1. **`attach_milestone_dod` at dispatch.** Copies the milestone's existing
   `dod_ref` artifact onto the job via `store_dod`. Nothing is recompiled — a
   test asserts the function's source never mentions `compile_milestone_dod`.
   No `dod_ref`, or an artifact that will not parse, stores NOTHING and returns
   False: the gate stays un-run for that job, which is the honest absence the
   evaluator already reports, never an invented definition of done.
2. **`run_gate_for_job` at production completion**, called from
   `execute_dispatched_job` after `run_cycles` returns. It calls `run_job_gate`
   and nothing else — a test asserts `save_gate_result` does not appear in its
   source, so the verdict keeps one author and the fixture-demo fulfillment
   spine is untouched. `None` (no stored DoD) is passed through as "not gated",
   not as green.
3. **Where the checks run.** The job's own workspace
   (`workspaces_dir()/<job id>`), created if absent. A gauntlet mission has no
   repository checkout, and pointing its checks at one would run a mission's
   commands against the operator's tree. A check that cannot run is recorded
   red with a reason — an honest verdict rather than a missing one.
4. **The outcome detail now carries the gate**: `gate=released`,
   `gate=blocked (<blocker>)`, or `gate=not-run`. "Not run" is said out loud
   rather than left to look like a pass.

No existing test's assertion pinned the old gate-less behaviour — the loop,
e2e, era, injection, runner and dod_gate suites are green unedited (316).
Test-fixture note: the DoD used by the new tests names `python3`, because the
gate only executes allow-listed executables; a check naming anything else is
refused before it runs, which is the allowlist working, not an obstacle.

## 2026-08-04: F075 R6 Phase 4 — re-proof evidence, and the STOP

`--live <scratch>/reproof-r6 --only 1 --format json`, exit 1, terminal
`iteration_limit`. `dod_result.json` IS present in the run dir — but
`released: false`. Phase 4 requires `achieved` AND a released verdict, so
rule 4.3 applies: STOP, trail recorded here, Phase 5 not run.

**Everything R-0187 and R-0188 wired is working, verbatim from the ledger:**

    it1: dispatch_job -> dispatched
         job 412be9f0 ... dispatched for M001; DoD attached; executed:
         terminal=all_green job_status=completed cycles=4/experiment OVER-CAP
         gate=blocked (dod_blocking_red:acc-001)

- `DoD attached` — `store_dod` now has a real caller; the milestone's compiled
  artifact reaches the job (R-0188.1).
- `cycles=4/experiment OVER-CAP` — the order's v2 budget reached the executor
  through the explicit override, and the run records it. `run.json` carries
  `cycles_budget: 4`, `cycles_resolved: ["cycles=4/experiment"]` (R-0187).
- `executed: terminal=all_green job_status=completed` — jobs run and finish.
- `gate=blocked (...)` — the gate RUNS and produces a persisted verdict. Before
  R-0188 no run in the project's history could produce one at all.

**Why it is blocked — the next blocker, and it is not in this round's scope.**
The verdict's one red check:

    acc-001  kind=pytest  blocking=True  status=failed  reason=nonzero_exit
      no tests ran in 0.00s
      ERROR: file or directory not found: tests

The gauntlet's missions have NO REPOSITORY. The runner creates a project
record with `repo_paths: []` and `canonical_repo_path: None`, and the job's
workspace contains only what the run itself produced
(`['.pytest_cache', 'task_output']`). The orders say "in the sample project",
but no sample project is materialised, so a milestone whose DoD is "the unit
suite is green" can never release: there is nothing to test.

That is a harness gap of the same class as the R2 seam, the R4 2c and the R5
3.3 — a missing piece of the campaign's world, needing its own reviewed
design (what repository the ten orders operate on, how it is materialised per
run, and how it stays isolated from the operator's tree). Not smuggled in
here.

Second observation, recorded not fixed: the six-dispatch pattern reappears,
but for a DIFFERENT reason than R-0184. Every job now reaches `completed`, so
the re-dispatch guard correctly allows a retry; the model retries because the
gate blocked. Retrying a milestone whose DoD failed is defensible, but it
spends the whole iteration budget on identical attempts. Whether the loop
should escalate after N identical failed attempts is a reviewer call.

Not done, deliberately: no change to CYCLE_SAFETY_CAP or any config default;
no repository invented for the orders; no order edits; no weakening of the
pass definition; the campaign (Phase 5) NOT run.

## 2026-08-04: F075 R7 — R-0189 the sample-project world

**Goal-vs-template audit.** Every one of the ten goals was checked against the
template BEFORE freezing v3; each names something that really exists:

| Order | What the goal names | Where it lives in the template |
| --- | --- | --- |
| g01 | a hard-coded retry backoff cap | `sampleproj/retry.py` `BACKOFF_CAP_SECONDS = 30` |
| g02 | config precedence (arg > env > file) | `sampleproj/config.py` `resolve()`, `ENV_VARS` |
| g03 | a CLI with progress output to suppress | `sampleproj/cli.py` prints progress to stdout, errors to stderr |
| g04 | env vars + precedence rules to document | `config.ENV_VARS` + `README.md` "Configuration" |
| g05 | duplicated path normalisation, two call sites | identical block in `importer.py` and `report.py`, both marked |
| g06 | a public parse entry point returning None | `sampleproj/parsing.py` `parse_record()` |
| g07 | exact user-facing error text | `sampleproj/errors.py` message constants |
| g08 | an import command writing to a target dir | `cli.py import` + `importer.import_records` / `plan_import` |
| g09 | a report writer, and a CLI that renders it | `sampleproj/report.py` + `cli.py report` |
| g10 | a release history, next version unstated | `CHANGELOG.md` (0.1.0/0.2.0/0.3.0); no next version anywhere |

No goal had to be dropped and NO order was edited. The template's own suite is
30 tests, green, offline, ~0.05s.

Decisions:
1. **A copy per run, never the original.** `materialise_sample_project` copies
   the template into `<run_dir>/workspace`, then `git init` + one baseline
   commit inside the COPY. The baseline exists because a mission's work is a
   DIFF: without it, "no file outside the touched module changed" has nothing
   to measure from. Build droppings (`__pycache__`, `.pytest_cache`, `.git`)
   are not copied — they are not the project.
2. **The project record points there.** `_default_make_project` now sets
   `repo_paths` and `canonical_repo_path` to the run's workspace, and the
   execute seam binds that path as the DoD checks' `worktree_root`. The
   operator's tree is never a mission workspace; two runs cannot see each
   other's edits (both pinned by tests).
3. **Freeze via manifest v3.** `template_tree_digest` hashes sorted relative
   paths plus contents, and it is folded into the set hash — the world shapes
   a mission's outcome exactly as much as the order does, so a retouched
   template is a changed campaign. `load_order_set` refuses on a mismatch
   before a token is spent, and a manifest with no `template_digest` is
   refused outright. `run.json` records the digest used. Set v3 hash:
   `c267ccabf9b021c9c1f01c126d09c1308436457a22a0373ef490ebd989aaebb6`,
   template digest `1c4f41bf991a5b3626a72d5de60eba76948e82ec3181cff1f2dc4d5dd4ef0454`.
   Count reset per A9 — nothing lost, no attempt has passed.
4. **`conftest.py` at the template root** inserts its own directory on
   `sys.path`, so a materialised copy runs `python3 -m pytest tests -q` with no
   install and no outside PYTHONPATH. Proven by running the suite from a
   scratch copy, not by assuming it.

Two existing tests changed, both because a literal became reality:
`test_the_set_is_at_version_two` -> `..._three`, and
`test_the_set_hash_matches_the_listed_digests` now also passes the template
digest (the set hash covers it in v3). No assertion was weakened.

## 2026-08-04: F075 R7 — R-0190 escalate the second blocked completion

`BLOCKED_COMPLETIONS_BEFORE_ESCALATION = 2`, matching the loop's own
refuse-once-then-escalate rule: the FIRST block is a legitimate, informed
retry (the context already carries the blocker), and the second says the retry
did not work. `blocked_completion(move, outcome)` reads the streak off the
outcome the loop already writes (`gate=blocked (<blocker>)`) rather than
re-deriving anything; a released or un-run gate, or a different milestone,
resets it. The escalation goes through the EXISTING `hand_over` seam — the
same F051 verb the twice-refused path uses, pinned by a test that injects it —
and its detail names the milestone, both blockers, and the iterations the
run keeps instead of spending on a third identical dispatch.

The streak is per milestone on purpose: two blocked milestones are two first
attempts, not a stuck loop. All nine tests are provider-free (R-0182), and the
loop, e2e, era and injection suites are green UNEDITED (259).

## 2026-08-04: F075 R7 Phase 4 — re-proof evidence, and the STOP

`--live <scratch>/reproof-r7 --only 1 --format json`, exit 1, terminal
`iteration_limit`. The DoD verdict is RELEASED. Phase 4 requires `achieved`
AND a released verdict, so rule 4.3 applies: STOP, trail recorded here,
Phase 5 not run.

**The gate releases — the first time in this feature's history.**

    dod_result.json: released: true, blocking_red: [], error: ""
      check acc-001  kind=pytest  status=passed  exit_code=0
    run.json: cycles_budget 4, cycles_resolved ["cycles=4/experiment"],
              template_digest 1c4f41bf991a5b3626a72d5de60eba76948e82ec3181cff1f2dc4d5dd4ef0454

R-0189 did what it was for: the mission had a real checkout, the suite ran in
it, and `acc-001` — the same check that read "file or directory not found:
tests" in R6 — passed with exit 0. Every ledger entry reads:

    dispatch_job -> dispatched :: job ... dispatched for M001; DoD attached;
    executed: terminal=all_green job_status=completed
    cycles=4/experiment OVER-CAP gate=released

**Why it still did not reach `achieved`.** Six iterations, six dispatches of
M001, every one completing with a RELEASED gate — and the model never chose
`declare_milestone_done`. Mission end state: `status: active`,
`_milestones_done: None`, `job_links: 6`. R-0190 correctly did not fire: it
escalates a blocked STREAK, and nothing here was blocked.

The gap is now a single missing guard, symmetric with the two already built:
`evaluate_dispatch` refuses a second job while one is IN FLIGHT (R-0186) and
the loop escalates two consecutive BLOCKED completions (R-0190), but nothing
refuses a dispatch for a milestone whose latest job COMPLETED with a RELEASED
gate — the one case where the only correct move is `declare_milestone_done`.
The refusal message would say exactly that, the same way the in-flight refusal
already tells the model what to do instead.

Not built here: it is not this round's ordered scope, and Phase 4.3 says stop
rather than keep going. Recorded for the reviewer as the next fix.

Not done, deliberately: no change to CYCLE_SAFETY_CAP or any config default;
no order or template edits (v3 stays frozen at set hash
c267ccabf9b021c9c1f01c126d09c1308436457a22a0373ef490ebd989aaebb6); no
weakening of the pass definition; the campaign (Phase 5) NOT run.

## 2026-08-04: F075 R8 — R-0191 the released-gate dispatch guard

`evaluate_dispatch` now refuses a `dispatch_job` for a milestone whose LATEST
linked job COMPLETED with a RELEASED gate. That completes the triad the
campaign uncovered one leg at a time:

| Milestone's latest job | Guard | What the loop does |
| --- | --- | --- |
| in flight (pending/planned/running) | R-0186 | refuse; wait or declare when it finishes |
| completed, gate BLOCKED twice in a row | R-0190 | escalate through the existing F051 hand_over |
| completed, gate RELEASED | R-0191 | refuse; declare_milestone_done |

Decisions:
1. **The verdict is read, never re-derived.** `collect_milestone_evidence`
   already asks `dod_gate.load_gate_result` for the latest job the ledger
   attributes to the milestone, so `evidence.gate_released` IS the real
   verdict, and a newer un-released job supersedes an older released one by
   construction. A test asserts the guard's source never mentions
   `blocking_red` or `checks` — it trusts the gate's answer.
2. **Only `gate_released is True` fires it.** `None` (no stored DoD) means
   nothing was proven, so a further dispatch is legitimate; `False` belongs to
   R-0190. Two guards arguing over one fact would be worse than the hole.
3. **The loop does NOT declare the milestone itself.** The claim is the
   model's move and carries the model's accountability — the loop refuses the
   move that cannot help and names the one that can. The existing
   first-refusal re-prompt carries that sentence back, and the
   second-refusal escalation already exists if it is ignored. Alternative
   considered: auto-declaring on a released gate — rejected, it would make the
   loop assert a milestone is done on the model's behalf, which is exactly the
   authority boundary F070 was built to keep.

Nine tests, all provider-free (R-0182), including the end-to-end one: a model
that follows the refusal reaches `achieved`, and `dispatched.seen == []`
proves no job was created for work already finished. The loop, e2e, era,
injection and runner suites are green UNEDITED (307).

## 2026-08-04: F075 R8 Phase 3 — re-proof evidence, and the STOP

`--live <scratch>/reproof-r8 --only 1 --format json`, exit 1, terminal
`escalated`. The gate is RELEASED (`acc-001 passed`), so Phase 3's second
requirement holds — but `achieved` does not. Rule 3.3: STOP, trail here,
campaign not run.

**R-0191 works, and the model obeyed it.** Three iterations, verbatim:

    it1: dispatch_job -> dispatched
         job fe02e963 ... DoD attached; executed: terminal=all_green
         job_status=completed cycles=4/experiment OVER-CAP gate=released
    it2: dispatch_job -> refused
         milestone M001 is already finished: job fe02e963 completed and its
         Definition of Done RELEASED. Another job would repeat work that is
         already proven. Instead: declare_milestone_done for M001
    it3: declare_milestone_done -> escalated
         refused twice in a row (no job was ever dispatched for milestone
         M001, so there is nothing whose outcome could meet its Definition of
         Done); escalated: td:55642ed3

The R7 failure mode is gone: six identical dispatches became one dispatch,
one refusal, and the model took the instruction and claimed the milestone.

**What blocked it — a latent defect the guard exposed.**
`orchestrator_loop.dispatched_job_for` walks every ledger entry whose move
kind is `dispatch_job` for the milestone and keeps the LAST one's
`outcome.job_id`:

    for entry in read_ledger(...):
        if move.get("kind") != "dispatch_job":            continue
        if payload.get("milestone_id") != milestone_id:   continue
        job_id = str((entry.get("outcome") or {}).get("job_id", "") or "")

A REFUSED dispatch is still a `dispatch_job` move — and its outcome carries no
`job_id`, so it overwrites the real attribution with "". At it3 the evidence
therefore said "no job was ever dispatched", `evaluate_milestone_done`
correctly refused a claim it could not verify, and the second-refusal rule
escalated. The mission ends with 1 open decision, so it would fail
`no_open_decisions` too.

The defect is pre-existing — nothing refused a dispatch before R-0191, so no
ledger ever carried a refused `dispatch_job` entry for a milestone that also
had a real one. The fix is one condition: a dispatch entry with no `job_id`
(equivalently, an outcome whose status is not `dispatched`) is not a dispatch
and must not erase the attribution. Not applied here: Phase 3.3 says commit
nothing further, and this needs its own tests — including the exact
refused-then-claim sequence above.

Not done, deliberately: no order or template edits (v3 frozen at set hash
c267ccabf9b021c9c1f01c126d09c1308436457a22a0373ef490ebd989aaebb6, template
digest 1c4f41bf...); no config default touched; no weakening of the pass
definition; the campaign (Phase 4) NOT run.

## 2026-08-04: F075 R9 — R-0192 a refused dispatch is not a dispatch

One condition in `dispatched_job_for`: an entry whose outcome carries no
`job_id` is skipped instead of overwriting the answer. Everything else in the
function is untouched — same ledger walk, same milestone filter, same
last-wins rule among entries that actually produced a job.

Why it was wrong: the move kind and milestone id of a REFUSED dispatch are
identical to a real one, and only the outcome tells them apart. Before R-0191
nothing refused a dispatch, so no ledger ever held a refusal beside a real
dispatch and the unconditional overwrite was never exercised. The R8 re-proof
is the whole story: `declare_milestone_done` refused with "no job was ever
dispatched for milestone M001" for a milestone whose job had completed with a
released gate.

Five tests, all provider-free: real-then-refused keeps the attribution;
latest-REAL-wins across interleaved refusals; only-refusals still answers ""
honestly (absence must stay sayable); another milestone's dispatch is not
borrowed; and the R8 sequence replayed end-to-end — dispatch, refused dispatch
(R-0191 still firing), declare — now reaching `milestone_done` and then
`achieved`. That last test derives its evidence from the REAL
`dispatched_job_for`, which is what makes it load-bearing rather than a mock
agreeing with itself.

Nothing else rode along in the commit. Loop, e2e and era suites green
UNEDITED (237).

## 2026-08-04: F075 R9 Phase 3 — re-proof evidence, and the STOP

`--live <scratch>/reproof-r9 --only 1 --format json`, exit 1, terminal
`iteration_limit`. Gate RELEASED, ZERO open decisions — two of Phase 3's
three requirements hold, `achieved` does not. Rule 3.3: STOP, trail here,
campaign not run.

**R-0192 works live, and the whole chain now closes for a milestone.**

    it1: dispatch_job -> dispatched   job 336057db ... DoD attached; executed:
         terminal=all_green job_status=completed cycles=4/experiment OVER-CAP
         gate=released
    it2: dispatch_job -> refused      milestone M001 is already finished: job
         336057db completed and its Definition of Done RELEASED ...
    it3: declare_milestone_done -> milestone_done   milestone M001 recorded as done
    it4: dispatch_job -> dispatched   job 75115e49 ... for M002 ... gate=released
    it5: dispatch_job -> refused      milestone M002 is already finished ...
    it6: declare_milestone_done -> milestone_done   milestone M002 recorded as done

`dod_result.json`: released true, `acc-001 passed`. Mission record:
`_milestones_done: ['M001', 'M002']`. The R8 blocker is gone — the declare
move that was refused with "no job was ever dispatched" now succeeds, twice.

**Why not `achieved`: a budget-versus-plan-shape mismatch, not a defect.**
The order g01 states ONE milestone; the mission compiler expanded its goal
into THREE (`M001, M002, M003`). The loop currently spends THREE iterations
per milestone — dispatch, the R-0191 refusal, then the declare — so three
milestones plus the final `declare_mission_achieved` need ten iterations
against g01's budget of six. It got two milestones done and ran out.

Two things a reviewer could rule on, neither of them mine to take:

1. **The refused dispatch costs an iteration.** The model dispatches, is
   refused with "declare_milestone_done", then declares. If it declared
   straight off a released gate each milestone would cost two iterations, and
   three milestones would fit in seven. The guard makes the model CORRECT; it
   does not yet make it economical. Options include carrying the released-gate
   fact more visibly in the assembled context, or not counting a refused
   iteration against the budget — both are product changes with their own
   tests.
2. **Order budgets were set in R1, when nothing executed.** `max_iterations`
   6 for g01 predates execution, the DoD path and the guards. Raising them is
   an order edit — forbidden mid-campaign, and set v3 is frozen (set hash
   c267ccabf9b021c9c1f01c126d09c1308436457a22a0373ef490ebd989aaebb6), so a
   re-issue would be v4 with another count reset. Reviewer's call.

Not done, deliberately: no order or template edits, no budget changes, no
config default touched, no weakening of the pass definition; the campaign
(Phase 4) NOT run.

## 2026-08-04: F075 R10 — R-0193 the released-gate context directive

A new context section, `## Milestones ready to declare`, carrying one line per
milestone whose latest job COMPLETED with a RELEASED gate:

    - M001: job <id> completed and its Definition of Done RELEASED. The
      correct next move is declare_milestone_done for M001.

Decisions:
1. **The same facts the guard reads.** `released_milestone_directives` calls
   the loop's own `observe` seam — the very one `evaluate_move` uses — so the
   context and the R-0191 refusal can never disagree about which milestone is
   ready. A test that substitutes the seam substitutes both.
2. **Only a proven fact earns a line.** `gate_released is True` and job state
   `completed`. An absent verdict proves nothing; a blocked one is R-0190's
   business; an in-flight job is R-0186's. Four parametrised cases pin that
   nothing else produces a directive, and a milestone already recorded done is
   not re-announced.
3. **The section is absent when there is nothing to say** — no empty heading,
   so the context stays byte-stable for a mission with nothing ready (the
   cache-prefix discipline F070 set).
4. **Guidance, not guarantee.** The R-0191 refusal is untouched and its own
   test still asserts it fires. The directive saves an iteration; the guard is
   what makes correctness non-optional.
5. **A directive is never worth a crash.** An `observe` that raises is caught
   and simply produces no line.

Economics, pinned by test rather than asserted in prose: a model that follows
the context reaches `achieved` in five iterations for two milestones — two
each plus the final claim — with `OUTCOME_REFUSED` absent from the ledger. R9's
live run spent three per milestone because the refusal was where the model
learned the milestone was finished.

Twelve tests, all provider-free (R-0182). Loop, e2e and era suites green
UNEDITED (249).

## 2026-08-04: F075 R10 Phase 3/4 — v4 budgets, and the first flawless run

**R-0194, what changed and what did not.** Ten orders, budget values only.
`max_iterations` 6 → 12 (one-milestone orders) and 12/14 → 22 (the two
two-milestone orders); `max_tokens` and `max_wall_seconds` re-sized with them;
`max_cycles` UNTOUCHED — R9 measured those right (every job reached all_green
at its budgeted cycles), and an edit without evidence is the guess v4 exists to
replace. Every non-budget key was proven byte-identical to v3 mechanically
before the commit. Template digest unchanged (1c4f41bf…), so the world the
missions run in is the same world; set hash e50916bf…, version 4, count resets
per A9 (nothing lost — no attempt had passed).

Sizing rule, recorded per order in a new `budget_rationale` field: the
PESSIMISTIC path. Three iterations per milestone (dispatch, the R-0191 refusal,
the declare) plus one to achieve, over the compiler's observed expansion, plus
margin — so a run that ignores the R-0193 directive still fits. Three tests pin
it: a floor from the measured shape, a ceiling five above it (a budget nothing
can fail does not measure economy), and the frozen cycles.

**Phase 4 re-proof — the first flawless run in this feature's history.**
`--only 1`, isolated data root outside the repo, 472s:

    terminal_status achieved · open_decisions [] · released true (acc-001 passed)
    all nine criteria true · flawless true

Nine iterations, and the ledger contains no refusal at all:

    it1 dispatch M001 gate=released · it2 declare M001
    it3 dispatch M002 gate=released · it4 declare M002
    it5 dispatch M003 gate=released · it6 declare M003
    it7 dispatch M004 gate=released · it8 declare M004
    it9 achieved — every milestone is done and the mission goal is met

R-0193 does what it claimed: two iterations per milestone, the guard never
needed. R-0192's chain now runs four times in one mission instead of twice.

**One observation the reviewer should hold, not act on.** The compiler shaped
FOUR milestones this time, not R9's three — the expansion is not a constant.
Four milestones cost 9 iterations direct (fits 12 with room) but would cost 13
if the model fell back to the refusal path, which does NOT fit. The budget is
sized for the direct path plus margin, and the direct path is now the
product's behaviour rather than a hope — but a campaign order that expands to
five milestones AND ignores the directive can still hit iteration_limit. That
is the gate measuring economy, which is its job; noting it so a v5 is an
evidence decision rather than a reflex.

## 2026-08-05: F075 R10 Phase 5 — set-v4 campaign, attempt 02: 3/10

ONE invocation, ten orders, isolated data root outside the repo, matrix in
`.agent/gauntlet/attempt-02/`. Set hash e50916bf…, template digest 1c4f41bf…
(unchanged from v3). Attempt 01 was 0/10.

    g01 pure-code-change        FLAWLESS   achieved          7 it,  3 milestones
    g02 test-add                           iteration_limit  12 it,  6 milestones
    g03 small-app-feature-smoke            iteration_limit  12 it,  6 milestones
    g04 doc-generation                     iteration_limit  12 it,  6 milestones
    g05 two-milestone-mission   FLAWLESS   achieved          5 it,  2 milestones
    g06 provider-api-error                 iteration_failed  1 it,  0 milestones
    g07 truncated-model-response FLAWLESS  achieved         11 it,  5 milestones
    g08 harness-death-mid-dispatch         iteration_failed  1 it,  0 milestones
    g09 harness-death-mid-write            iteration_failed  1 it,  0 milestones
    g10 escalate-then-finish               iteration_limit  12 it,  6 milestones

Held in ALL TEN runs: `start_command_only`, `no_unknown_postmortems`,
`no_open_decisions`, `host_data_root_untouched` (hash before == after),
`no_era_defect_classes`, `injections_degraded`, `evidence_well_formed`. Zero
refusals anywhere — R-0193's direct path carried every one of the 74 iterations
this campaign spent. Only two criteria ever failed: `terminal_green` (7 runs)
and `dod_blocking_green` (the 3 that died before any gate ran).

### Finding A — the compiler's plan expansion is erratic, so no static budget fits

Same order, same frozen world, different plan shape every time. g01 expanded a
one-milestone goal into 3 here, 4 in this round's re-proof, 3 in R9. g02/g03/g04
each expanded into at least 7. g05 did not expand at all: two stated milestones
became two.

Every one of the four `iteration_limit` runs finished six milestones cleanly at
exactly two iterations each and then ran out of budget mid-plan. Nothing
misbehaved — the runs were economical and correct, and still could not finish.

v4 sized `max_iterations` from a measured expansion factor of 3. The real factor
ranges from 1 to at least 7 and varies between runs of the SAME order. A static
per-order budget cannot track that: set it for the worst case and the
anti-slack test becomes meaningless, set it for the average and half the
campaign dies. R-0194 was the right correction to R1's guess and it is not
enough. The fix belongs in the product — bound or stabilise the expansion, or
derive the bound from the compiled plan rather than from the order — not in a
v5 of the budgets.

### Finding B — the exception boundary ends the mission where the pass definition requires it to continue

`orchestrator_loop.py:984-993`: the R3 boundary classifies the failure, writes
the postmortem, ledgers it, sets `terminal=True` and RETURNS. One transport
blip is a dead mission.

Three runs prove it, on two distinct failure classes: g06 (`provider_unavailable`
at `call_fn` call 1), g08 and g09 (`io_failure` at `dispatch` and at
`update_dossier`, call 1). Each ledgered correctly with `disposition
"ledgered_failure"` and no unknown postmortem — the degradation is exactly right
— and each mission was over after ONE iteration, having completed no milestone,
so no DoD verdict exists and `dod_blocking_green` fails as an absence.

g07 is the counter-example that makes this a defect rather than a design choice:
its truncation injection is handled BELOW the boundary (parse-class refused,
re-prompted once, `disposition "retry_within_budget"`) and the mission ran on to
`achieved` and FLAWLESS. Degrade-and-continue already exists in this codebase;
the boundary is what refuses it.

g06's own rationale states the bar: "Flawless means ledgered and retried within
budget — never a move silently skipped." With today's boundary, g06/g08/g09
cannot reach `achieved`, so three of ten runs are unwinnable by construction.
Direction (a reviewer decision, NOT taken here): ledger, write the postmortem,
and continue the loop until a budget or a repeat-failure rule stops it. NO retry
inside the boundary — transport retries live below `call_fn` (F001).

## 2026-08-05: F075 R11 — R-0196 the boundary continues on retryable classes

Campaign attempt 02 showed three missions dying at iteration 1 on transient
faults, with zero milestones and therefore no DoD verdict at all — while g07's
truncation, handled below the boundary, recovered and finished flawless. The
boundary now makes that distinction itself.

Decisions:
1. **The set is NARROW and named**: `provider_unavailable` and `io_failure`,
   compared by VALUE so F010 can add a class without it being silently retried
   here. A timeout is a provider fault and is deliberately NOT in the set — the
   ruling named two classes, not "anything provider-shaped". `unknown` above
   all still ends the run: retrying a fault Remedy cannot name is how a budget
   disappears without an account of itself.
2. **A new OUTCOME_, not a TERMINAL_.** `OUTCOME_ITERATION_RETRYING` keeps the
   spent iteration on the ledger, so a run that succeeded on the second attempt
   still says out loud that the first one failed. The post-mortem is written
   exactly as before.
3. **Two in a row on the SAME milestone escalates**, mirroring R-0190 and the
   refuse-once rule. The milestone comes from `working_milestone` — the first
   not yet done, the same plan order the loop follows — because the exception
   may be raised before any move exists. Any executed move clears the streak.
4. **Still no retry in the boundary.** The next iteration re-decides from a
   fresh context, which is not re-issuing the call that raised; transport
   retries stay below `call_fn` (F001).

`gauntlet_injection.settle` needed the new shape, not a new rule: a green
terminal now means "swallowed" only when NO post-mortem was written, and
"recovered" (`retry_within_budget`) when one was. Same question it always
asked — did the run keep an account of the fault — on a shape the product can
now produce. The closed disposition set is untouched.

Three existing tests asserted the old terminal and were updated with the reason
stated inline; their subject (the failure CLASS) is unchanged. 14 new tests.
Gate: loop/e2e/era/injection/runner 338, exit 0.

## 2026-08-05: F075 R11 — R-0197 the compiler honors the order's declared shape

`compile_mission_plan` and `plan_mission` gain `max_milestones: int | None`.
`None` is today's behaviour exactly, pinned by a test that compares the two
prompts for equality rather than by inspection.

Decisions:
1. **The cap is enforced twice, in the two places that can disagree.** The
   prompt states the lower ceiling, AND the draft is validated against it. A
   prompt alone is a request; a validator alone wastes a call it could have
   prevented.
2. **The validator is a SUBCLASS of `MissionPlanDraft`**, so an over-cap draft
   is a parse-class failure like any other invalid answer: F001's single retry
   re-prompts with the reason (proven: the second prompt names the cap and the
   draft's actual count), and a second over-cap answer takes the deterministic
   fallback. No new retry path and no new failure mode were invented for this.
   The subclass keeps `MissionPlanDraft`'s name so the protocol the provider is
   shown is unchanged — only the validation is stricter.
3. **The caller can only make the plan SMALLER.** `resolve_milestone_cap`
   clamps into `[1, MAX_MISSION_MILESTONES]`, so F069's outer bound still wins
   and a caller cannot argue past the schema.
4. **The runner passes `len(order.milestones) + 1`** — derived, never
   hard-coded, pinned as a function over 1/2/4 declared milestones. The
   headroom exists because a compiler that finds a genuine prerequisite should
   be able to say so; what it may not do is turn a one-milestone order into
   seven and spend the budget rediscovering that.

The DAG discipline and the deterministic fallback are untouched, both pinned by
their own tests. 8 compiler tests + 2 runner tests. Gate: compiler/runner 154,
exit 0.

## 2026-08-05: F075 R11 Phase 4 — both re-proofs green

Fresh isolated roots outside the repo, one order each.

**Re-proof 1 (`--only 6`) — R-0196 live.** Every required fact present:

    terminal achieved · open_decisions [] · dod released true
    injection: raised at call_fn call 1: ConnectionError: provider API error
      mid-move: HTTP 503; ledgered with 1 post-mortem(s), then the run
      recovered and finished
    disposition retry_within_budget   post-mortem class provider_unavailable

    it1 iteration_failed_retrying | ConnectionError ... HTTP 503
    it2 dispatched                | job e2185f24 ... all_green, gate released
    it3 milestone_done            | M001 recorded as done
    it4 achieved                  | every milestone is done

In attempt 02 this same order ended `iteration_failed` at iteration 1 with zero
milestones and no DoD verdict at all. The fault now costs one iteration and the
mission finishes. The disposition is read off the product's own facts — a green
terminal WITH a post-mortem — not asserted by the harness.

**Re-proof 2 (`--only 2`) — R-0197 live.**

    compiled milestones ['M001', 'M002'] · origin provider · compiled true
    terminal achieved · open_decisions [] · dod released true · 5 iterations
    against g02's v4 budget of 12

g02 declares ONE milestone, so the cap was 2 and the compiler produced exactly
2 — within `declared + 1`. In attempt 02 the same order compiled at least SEVEN
and died on `iteration_limit` after six milestones. Two iterations per
milestone plus the achieve, so the v4 budgets now have real headroom rather
than being a guess against an unbounded shape.

Preconditions for attempt 03 re-verified: set version 4, set hash
e50916bf… equal to the recomputation, `preflight_injections -> []`.

## 2026-08-05: F075 R11 Phase 5 — attempt 03: 10/10 FLAWLESS

ONE invocation, ten orders, set v4 (hash e50916bf…, template 1c4f41bf…),
isolated data root outside the repo. `passed: true`, `failure_kinds: []`.

    run                            terminal    it done retry open
    g01 pure-code-change           achieved     5    2     0    0
    g02 test-add                   achieved     3    1     0    0
    g03 small-app-feature-smoke    achieved     5    2     0    0
    g04 doc-generation             achieved     5    2     0    0
    g05 two-milestone-mission      achieved     7    3     0    0
    g06 provider-api-error         achieved     4    1     1    0
    g07 truncated-model-response   achieved     5    2     0    0
    g08 harness-death-mid-dispatch achieved     6    2     1    0
    g09 harness-death-mid-write    achieved     8    3     1    0
    g10 escalate-then-finish       achieved     5    2     0    0

All nine criteria true in all ten runs. Every run finished well inside its v4
budget; the largest was g09 at 8 iterations against 22.

Both R11 changes are visible in the evidence rather than merely asserted:

* **R-0196** — the `retry` column is `iteration_failed_retrying` entries.
  Exactly the three raise-class injections produced one each, and each of
  those runs went on to `achieved`. All four injections FIRED and all four
  settled `retry_within_budget`, with post-mortems `provider_unavailable`
  (g06) and `io_failure` (g08, g09); g07's truncation re-prompted once as
  before. Nothing settled `never_fired` or `silent_success`.
* **R-0197** — plan shapes are now bounded by the orders: 1–3 milestones per
  run against declared shapes of 1 or 2. Attempt 02's same orders compiled to
  as many as seven.

Comparison: attempt 01 = 0/10, attempt 02 = 3/10, attempt 03 = 10/10.

**Observation for Window 1, NOT acted on.** The campaign process read ~872 GB
from disk while writing ~2 MB, sustaining ~12 MB/s with system I/O pressure
near 15%. Nothing is wrong with the results — the isolation held and the host
data root hashed identical before and after in every run — but the read volume
is out of all proportion to a 2 MB evidence tree, which suggests a large tree
is being hashed or listed once per iteration. Worth a finding ID; touching it
mid-campaign was not an option and the campaign is now complete.

## 2026-08-05 — F075 R12: where the ADR lands, and what it proposes

**The repository had no ADR convention.** Inspected before choosing: no
`docs/adr/`, no `*adr*` or `*decision*` file anywhere under `docs/`, no ADR
section in `docs/README.md`. The only prior art is the instruction in the
source itself — `CYCLE_SAFETY_CAP`'s comment says the F075 gate raises it *"via
an explicit change with an ADR"* — and `.agent/decisions.md`, which is
task-scoped state and therefore the wrong home for a record a human must find
months from now.

**Decision: `docs/adr/`, a new subcategory of `docs/`, registered in
`docs/README.md`.** Rejected alternatives: `.agent/` (ephemeral task state, not
durable knowledge — the ADR outlives this feature); `docs/system/` (that
directory describes what IS BUILT, and a PROPOSED ADR describes what is not
built yet); `docs/roadmap/` (agents may not touch ROADMAP.md, and the roadmap
is the target plan, not a decision log). `docs/adr/` follows the precedent
already set by `docs/agents/` and `docs/ui/`: subcategories of `docs/` that are
neither built-state specs nor roadmap. The status line carries the boundary —
PROPOSED, applied by a human, never accepted by machine.

Files: `docs/adr/0001-raise-cycle-safety-cap.md` and its ready-to-apply
`0001-raise-cycle-safety-cap.diff` (verified with `git apply --check`;
generated from a real edit that was then reverted, so the context lines are
exact rather than hand-written).

**The proposal: `CYCLE_SAFETY_CAP` 1 -> 8, `DEFAULT_MAX_CYCLES` stays 1.** 8 is
the largest cycle budget attempt 03 granted (g05 and g09) and completed under.
Stated as a limitation rather than glossed: per-run cycle CONSUMPTION is not
recoverable — it lived in each run's `gauntlet_run.json` under the campaign
root outside the repo (R-0176), which has since been reclaimed; only the
matrices are committed. So the ADR argues from the proven CEILING (budgets
3-8, ten `achieved`) plus the committed iteration usage, and declines to invent
a measured-max-plus-margin number the evidence does not carry.

**NOT applied, deliberately.** The working tree after this phase carries the
diff FILE, not the change: `git status` is clean of any
`long_run_executor.py` modification and the suite is green with the cap still
at 1. Three assertions pin it there; the new one,
`test_the_rollout_cap_is_still_one_until_adr_0001_is_applied`, names ADR-0001
in its docstring so the human applying the ADR finds every pin by grep.

## 2026-08-08: F104 R1 — two decisions taken at the candidate sweep

**F104 D1 — commit-size counting is INSERTIONS.** The F103 closure review
raised, as a candidate rather than a finding, that AGENTS.md Commit Discipline
says "If a diff exceeds 500 lines" without saying whether a line is an
insertion or an insertion-or-deletion. F103 R7's commit `68bd9f3f` was
+308/-277 = 585 changed lines: over the cap by the churn reading, under it by
the insertions reading. This is not an edge case — every round's
`.agent/last_block.md` and `.agent/handoff.md` save is a full-file rewrite, so
the churn reading is unmeetable by construction for a verbatim single-file
state save.

Chosen: the cap counts INSERTIONS, and a verbatim single-file `.agent/**` state
rewrite is exempt outright. Applied to AGENTS.md Commit Discipline in this same
round.

Alternatives considered: (a) count insertions+deletions and grant the state
files a standing exception — rejected, because it silently re-scores every
past verdict in this repository as a violation; (b) leave it undefined and
judge case by case — rejected, that is exactly the ambiguity that cost the F103
closure a paragraph of argument. Reverse it by deleting the bullet from
AGENTS.md; nothing else depends on it.

**F104 D2 — the money flag is `--max-cost-usd`.** `docs/roadmap/features/
T2_F104.md` names the flag `--budget-usd` in its Goal while its own Design
section names the field `max_cost_usd`, and the three sibling flags already
shipped are `--max-total-tokens`, `--max-provider-calls` and
`--max-wall-clock-minutes`.

Chosen: `--max-cost-usd`, and the feature file's Goal line is amended to match
in this same round. One spelling per concept, and the flag now greps to its own
field and config key (AGENTS.md Code Discoverability). Alternative considered:
ship `--budget-usd` as the Goal literally says and let the field keep its own
name — rejected as synonym drift across a single feature. Reverse it by
re-amending the feature file and renaming the flag; no released surface depends
on either name yet.

## DECISION F104 D3 + D4 — predicted cost has a derived band and no invented price (2026-08-09)

Context: T2_F104's Design says expected cost is "band→tokens class default ×
configured price basis", which reads as though a task carries a band. It does
not: `JobTask` has no band field, and the only band vocabulary in the repo is
`TokenBand` (low/medium/high/unknown) in
`packages/orchestration/token_economy.py`, alongside
`estimate_task_token_band(task_type, context_estimate)`.

D3 — the band is DERIVED, not stored. The predictive check derives the band at
the dispatch safe point from `estimate_task_token_band()` over the next task's
context estimate. Alternatives considered: (a) add a `band` field to `JobTask`
— rejected, it changes a persisted model and every plan written before it would
carry a null anyway, which is the same missing-band case with more migration;
(b) always use the largest class default — rejected as needlessly blunt when a
context estimate exists. A task whose band cannot be derived takes the feature
file's own A9 path: the LARGEST class default, with the basis label saying the
band was missing, because over-stopping beats overspending.

D4 — the price basis has no default. `budget.price_basis_usd_per_1k_tokens` is
unset unless an operator sets it; with it unset the predictive path is inert and
labels itself `estimate_basis=no_price_basis`. Alternative considered: ship a
plausible default price — rejected under P6. A default price is a number nobody
measured, and every prediction derived from it would be a fabrication wearing an
honest label. An inert predictor is safe because the reactive check is the
backstop and is unchanged.

Reverse either decision by deleting its half of this entry and the matching
lines in `docs/roadmap/features/T2_F104.md`.

## DECISION F104 D5 — cost-side call counts are validated against the cost side (2026-08-09)

Context: finding R-0224. `BudgetCounters` carried a single call-count invariant,
`unpriced_call_count <= provider_calls`, written when every counter came from one
source: the run accumulator in `pingpong_job.run_job`. F104's ledger bridge broke
that assumption by feeding `unpriced_call_count` from the F103 SQLite ledger while
`provider_calls` kept counting attempts in the current run. The two disagree
legitimately — the accumulator skips `provider == "fake"` attempts and starts from
whatever `budget_actuals` were persisted, the ledger holds one row per finalized
task run across every run of the job — so the invariant fired on healthy data.

D5 — the counter object now carries BOTH cost-side counts, `priced_call_count` and
`unpriced_call_count`, and the cross-source check is gone. What survives is the
cost-side contradiction check: a positive `measured_cost_usd` with nothing priced
to explain it is still an error.

Alternatives considered: (a) clamp the unpriced count to `provider_calls` —
rejected, it understates how many calls went unpriced, which dresses poorly
measured data as well measured and is the P6 failure in mirror image; (b) stop
passing `unpriced_call_count` from the ledger at all — rejected, the unpriced
notation surviving the trip is an F104 acceptance criterion, and dropping it would
make `cost_description` claim a precision it does not have; (c) widen
`provider_calls` to the ledger total — rejected, `provider_calls` is the basis of
the `max_provider_calls` limit and moving it would change an unrelated F018 limit.

Why it matters beyond the bug: the raise was swallowed by the ledger read's own
broad `except Exception`, so the failure mode was not a crash but a silent
downgrade to "no cost known" — the money limit quietly ceasing to enforce for
exactly the mixed-priced jobs it was added for.

Reverse this decision by restoring the `unpriced_call_count > provider_calls`
check and dropping `priced_call_count`.

## DECISION F104 D6 — the context estimate is the task text, not the built prompt (2026-08-09)

Context: R4 wires the predictive check into `run_job`'s task-dispatch safe point.
`predict_next_task_cost` needs a band, DECISION F104 D3 says the band is DERIVED
there, and deriving it needs a context estimate for the next task. The obvious
source is the prompt that task will actually run on — `_build_task_prompt(job,
task, previous_summaries)`, which already computes a `tokens_estimated` figure a
few lines below the safe point.

D6 — the estimate comes from the task's OWN text (`title`, `body`, `acceptance`)
plus the `tokens_estimated` of prior task proof summaries, via the pure
`derive_next_task_token_band` in `budget_guard.py`. The prompt is NOT built.

Alternative considered: build the prompt above the safe point and use its real
token count. Rejected. The safe point exists to guarantee that a stop is consumed
BEFORE any work for the next task begins; moving the prompt build above it moves
work ahead of that guarantee, and the guarantee — not the accuracy of an estimate
— is the safety property. It would also make the most safety-critical code in the
loop depend on a builder that can raise.

The cost of the choice is stated rather than hidden: the estimate is a FLOOR. It
omits whatever the prompt adds around the task text, so it can only UNDER-predict,
never over-predict. That is the conservative direction here — an under-prediction
fails to stop early and the reactive check in `evaluate_budget` catches the
overrun, which is exactly the backstop's job; an over-prediction would stop
healthy jobs that were never going to breach.

Reverse this decision by moving the `_build_task_prompt` call above the safe point
and passing its `tokens_estimated` as the context estimate, then deleting the D6
lines here and in `docs/roadmap/features/T2_F104.md`.

## DECISION F104 D7 — R5 repairs instead of starting T003 (2026-08-09)

Context: the reviewer passed R4 and registered two findings against it — R-0225
(High: `max_cost_usd` is missing from the CLOSED `run_manifest._BUDGET_ALLOWED_KEYS`,
so a money-limited job cannot write its F012 manifest and therefore cannot
FINALIZE a stop) and R-0226 (Medium: no F104 test ever drove a money-limited job
to a terminal `JOB_STOPPED`, which is how R-0225 survived two reviewed rounds).
R5 was planned as T003 — display, docs and estimate labels.

D7 — R5 is spent repairing R-0225 and R-0226. T003 moves to R6, the integration
gate to R7, closure to R8. A display round that renders spent, remaining and the
next-task expectation out of a stop path that cannot finalize would be polish on
a broken feature: the numbers would be correct and the limit would still not stop
anything.

Alternative considered: fold the manifest fix into the T003 round to save a
relay. Rejected — a change to the shared F012 manifest schema and a user-facing
display slice in one branch is exactly the mixed diff AGENTS.md bars, and the
schema change has its own blast radius (the run-manifest gate) that a display
round would not run.

Reverse this decision by renumbering the remaining rounds; nothing depends on the
numbering.

## DECISION F104 D8 — an ist-doc IS owed for the job-budget stop path (2026-08-09)

Context: R6 was chartered to decide whether `docs/` owes a document for the job-budget
stop path. Nothing under `docs/system/` or `docs/guides/` mentions `max_cost_usd`,
`max_total_tokens` or `remedy job budget` — a grep for all three returns nothing. The
stop reason `predicted_budget_exhausted:max_cost_usd` therefore lives only in the
feature file, which is the TARGET plan, and in the code.

D8 — F104 writes `docs/system/job-budget-enforcement-v0.md` and registers it in
`docs/README.md`. AGENTS.md Documentation Updates requires `docs/` to be updated when a
feature introduces behavior that is not yet documented, and a limit that silently kills
a running job is exactly that. The doc is scoped to what F104 built plus the F018 limits
it extends — it does not attempt to document all of F018.

Alternative considered: extend `docs/system/run-contract-v1.md`. Rejected — the budgets
named there are the F011-era loop/test/runtime caps of a single run contract, a
different concept from per-job budget limits, and merging them would make one doc
describe two unrelated mechanisms.

Reverse this decision by deleting the doc and its two `docs/README.md` rows.

## DECISION F105 D2 — step blocks are capped at 240 lines (2026-08-09)

Context: F105 R4's commit `ea48ea89` carried 523 insertions, 23 over the AGENTS.md
cap. The cause was not the work: C1 mandates writing the step block to BOTH
`.agent/authored/<round>.md` and `.agent/last_block.md`, so a block of N lines costs
2N insertions in one inseparable commit. The R4 block was 263 lines. It was declared
with its inseparability reason and verified to be the only oversize commit in F105
(previous maximum 486, `5d7b9fce`), so it is accepted under the AGENTS.md exception —
which by construction may be used at most ONCE per feature. F105's allowance is now
spent, and a second oversize commit on this branch would be a Medium finding.

D2 — every F105 step block from R5 on is at most 240 authored lines, so block plus
`last_block.md` clears 500 insertions with room to spare. The cause and the fix both
sit with the reviewer's authoring, not with the worker: when a round needs more
authored content than that, it is split into two rounds instead of one long block.
R5 and R6 are exactly that split — the repair and the discoverability block, which
together would have overrun the cap.

Alternative considered: exempt the C1 pair from the counting rule the way AGENTS.md
exempts a SINGLE `.agent/**` state-file rewrite. Rejected — the exemption exists
because a one-file verbatim save is indivisible, while block LENGTH is a free choice
of the author, and an exemption would remove the only pressure keeping blocks short.

Reverse this decision by deleting this entry.

## DECISION F105 D3 (2026-08-09) — the schema tail stays unregistered

The segment manifest F105 T003 records covers the composed BASE prompt only.
For intake, plan, mission and orchestrator, `run_structured_call` wraps that
base through `build_schema_prompt` or `native_schema_prompt` and sends the
wrapped string, so the manifest describes a strict PREFIX of the bytes that
leave the process. Registering the tail was considered and rejected: the tail
is generated BELOW every builder, and pulling it into the registry would make
each builder compose after its own return value, inverting the seam T001 exists
to provide.

Instead the prefix is made VISIBLE rather than left implicit. Every trace entry
records `segment_manifest_chars` beside `prompt_chars`, and the gap between
them IS the unregistered tail, so a reader sees the coverage instead of
assuming it. The F105 acceptance line "the segment manifest appears in call
evidence for every role" is therefore true as written and honest about scope.
Landed in code at R12 (`packages/orchestration/prompt_trace.py`); recorded here
at R13, the first `.agent/`-only round after it.

Reverse this decision by deleting this entry.

## DECISION F105 D4 — the mission rules segment is CAP-SCOPED (2026-08-09)

`build_mission_prompt` interpolates `{max_milestones}` into the middle of its
rules list, and `packages/orchestration/gauntlet_runner.py:505` varies that cap
per caller (`max_milestones=len(order.milestones) + 1`). Registering the rules
as a rank-1 CONVENTIONS segment therefore cannot make the F105 acceptance claim
"identical prefix bytes across consecutive calls within a role" true
unconditionally. It is true PER CAP VALUE.

A byte-preserving split into a constant head and a parameterised tail was
considered and rejected: both interpolations sit mid-list, the segment delimiter
is a plain blank line (DECISION F105 D1), and the rules list contains no blank
line to split on. Any split reaching them would insert bytes the pre-migration
prompt does not have — precisely the content change T003 must not make.

D4 — the rules are registered WHOLE as `mission_rules`, and the cap scoping is
made visible instead of assumed. A one-line WHY comment sits directly above the
constant, where a reader searches, and
`tests/orchestration/test_mission_prompt_golden.py` pins the scope: equal caps
produce an identical `mission_rules` hash, different caps produce different
`mission_rules` hashes while every other segment hash is unchanged. The claim
becomes testable rather than hopeful, and its honest limit is on disk.

Reverse this decision by deleting this entry.

## DECISION F105 D5 — the step block is counted once, cap 400 (2026-08-09)

Context: finding R-0243. DECISION F105 D2 caps a step block at 240 lines because
C1 wrote the block to BOTH `.agent/authored/<round>.md` and
`.agent/last_block.md` in ONE commit, so N authored lines cost 2N insertions
against the AGENTS.md 500 cap. But the mandated record content of a reviewed
round — the gate verdict, the registrations and resolutions, the header pair and
the verbatim `.agent/plan.md` — costs roughly 150 lines before any feature work
is described, leaving under 90 for instruction. R14 and R15 both degraded into
record-only rounds and merged no feature change. The cap had begun doing harm.

D5 — C1 splits in two. C1a commits `.agent/authored/<round>.md` ALONE and its N
insertions count normally against the 500 cap. C1b rewrites
`.agent/last_block.md` ALONE, which is the verbatim rewrite of a SINGLE
`.agent/**` state file named in the AGENTS.md Commit Discipline exemption list,
and is therefore exempt exactly as written. The step-block cap becomes 400
authored lines, measured by the reviewer BEFORE delegation and stated in the
block itself.

This does not revive the alternative D2 rejected. D2 declined to exempt the C1
PAIR from counting, on the ground that block length is a free authorial choice
and an exemption would remove the only pressure keeping blocks short. That
pressure survives in full: C1a still meets the 500-line ceiling and 400 sits 100
under it. What ends is the DOUBLE counting, an accounting artifact of writing one
artifact twice in one commit rather than any measure of how long the block is.
Splitting an oversize commit is also the remedy AGENTS.md prescribes in its own
words, so no rule is reinterpreted and no exemption is widened.

Reverse this decision by deleting this entry, and restore D2's 240 with it.

## DECISION F105 D6 — the plan rewrite closes a round (2026-08-09)

Context: finding R-0242, open since R14 and declared as a deviation by every
worker since. AGENTS.md's Commit Gate item 1 verifies `.agent/plan.md` against
the current work before EVERY commit. Every block on this branch rewrites
`.agent/plan.md` in its LAST commit, so the intermediate commits of a round
carry the PREVIOUS round's plan. Read literally, each of those commits fails
item 1; read as the branch has actually run for eighteen rounds, none of them
does. An unpersisted convention is exactly the class this loop registers as a
finding, so it gets a rule or it gets abandoned.

D6 — within one delegated round, `.agent/plan.md` is rewritten in the round's
LAST commit and the Commit Gate's plan check is satisfied for the round's
intermediate commits from C1b onward by `.agent/last_block.md`, which carries
the round's plan verbatim. C1a is the exception, and it is covered differently
rather than not at all: it precedes C1b — DECISION D5 split them in that order
so the block is counted once — and what it commits is
`.agent/authored/<round>.md`, the block's OWN verbatim copy, so for that one
commit the plan of record and the commit content are the same bytes and agree
by construction. The plan of record for an in-flight round is the block;
`.agent/plan.md` states where the FEATURE stands, and mid-round it stands
nowhere new yet.

Amended at F105 R20 to fix finding R-0248. The original text said the block is
"committed BEFORE any of them at C1b", which a reader can falsify with one
`git log`: C1a comes first. The mechanism was sound; the word "any" overclaimed
its reach.

The alternative — rewrite `.agent/plan.md` first — was rejected because it
makes the file claim work that has not landed. A plan that reads "step 3 is
complete" in the commit before step 3 is written is a worse record than one
that is a round behind, and it would resolve R-0242 by manufacturing the
overclaim class this repository's Proof Chain exists to prevent. Being one
round behind is visible and honest; being one round ahead is not.

Scope: one round, one worker. It exempts nothing across rounds — a round that
ends without rewriting `.agent/plan.md` still fails item 1, and D6 is not a
licence to leave the file stale. Blocks stop declaring the ordering as a
deviation and cite this entry instead.

Reverse this decision by deleting this entry.

## DECISION F105 D7 — the protocol document is hashed per call (2026-08-09)

Context: `.agent/t003_inventory.md` hands migration-order step 4 an open
question it calls the read-per-call hashing question.
`orchestrator_protocol_text` reads `docs/agents/orchestrator_protocol.md` from
disk on EVERY call to `build_orchestrator_system_prompt`, and the segment
registry hashes whatever text it is handed. Registering the document as a
segment therefore re-reads and re-hashes, once per iteration, a file that does
not change within a run. The alternative was to read and hash it once — at
import, or at first registration — and reuse the digest for the rest of the
run.

D7 — the document is read and hashed PER CALL. The manifest has exactly one
job: to record the bytes that were actually sent. A digest cached at
registration records the bytes that were sent the FIRST time, so if the
document is edited mid-run the manifest reports a hash for text that no
provider ever received. That is the overclaim class the Proof Chain exists to
prevent, and a manifest that can lie about its own subject is worth less than
no manifest, because it is believed. What the caching would buy is one read of
a small file per iteration, set against a loop that already assembles a
dossier, reads the mission record, reads the stop file and appends a ledger
entry every iteration.

Worth stating because it is the obvious objection: this costs no cache hits.
Re-reading unchanged bytes yields the same bytes, so the composed prefix stays
byte-identical across iterations and the provider cache still hits it. Only a
genuine edit produces a different hash and a miss, and that miss is CORRECT —
the prompt really did change, and F105's whole argument is that a miss should
be explainable rather than mysterious.

Scope: this site. It sets no rule for segments whose source is expensive to
read. A future segment backed by something costly may cache its digest, and
when it does it declares the staleness window it is accepting, in its own
entry.

Reverse this decision by deleting this entry.

## DECISION F105 D8 — the pre-emission block checklist (2026-08-09)

Context: finding R-0250. Round 20's authored block carried four defects, every
one of them mechanical and every one of them catchable by looking at the block's
own bytes before sending it: it ran 471 lines against DECISION D5's 400-line
cap; its `.agent/plan.md` replacement ran 56 lines against AGENTS.md's <50; one
of its done-when gates required a grep to return 0 for a phrase the same block
deliberately wrote into that same file; and one pair was declared APPEND when
its TO edits the FROM line. The worker caught all four, declared all four, and
worked around them correctly — the round was not damaged. What it cost was a
round's worth of deviations spent proving reviewer mistakes, and the
zero-gate defect was the fifth of its kind across F104 and F105.

D8 — the four checks become a numbered checklist in
docs/agents/planner_reviewer_prompt.md §3, run mechanically on a block's final
bytes before it is emitted. Recurrence, not severity, is the argument: no single
instance of these justifies a rule, and five instances of one of them do. The
checks are cheap — three counts and one substring test — and they are the kind
of thing a reviewer is certain it will remember and then does not.

The alternative, a validator script that lints a block before emission, was
rejected FOR NOW rather than on the merits. It would be strictly better, and it
would also be production code written by the reviewer role to police the
reviewer role, which the split workflow does not currently have a shape for. If
the checklist proves insufficient, that script is the next move and this entry
is where it should be argued.

Scope: reviewer-authored blocks. It adds no obligation to workers and changes
no verification tier. It is a pre-flight check on text the reviewer is about to
send, nothing more.

Reverse this decision by deleting this entry and the §3 checklist it installs.

## DECISION F105 D9 — the schema tail stays outside the registry (2026-08-09)

Context: `.agent/plan.md` has carried, since R17, an open question that step 5
was not allowed to start without: does the schema tail appended by
`packages/orchestration/structured_outputs.py` — `build_schema_prompt` in
legacy mode, `native_schema_prompt` in native mode — become a registered rank-4
segment? Until it is answered, every T003 manifest describes fewer bytes than
the call actually sent, which sounds like an overclaim.

D9 — it does NOT become a registered segment during T003. Three reasons, in
order of weight.

1. It is appended by `run_structured_call`, shared infrastructure that every
   structured caller in the repository reaches, not by any of the six builders.
   Registering it there widens T003's change set from one builder per round to
   every structured call site, which AGENTS.md Scope Control bars.
2. It cannot affect the property T003 exists to create. The tail is a SUFFIX
   joined with exactly `PROMPT_SEGMENT_DELIMITER`, so the composed text is a
   strict PREFIX of the bytes sent and the cacheable prefix is byte-identical
   either way.
3. Its bytes are attempt-dependent — the parse-retry hint is part of them — so
   its honest rank is 5 STEERING, which sorts last. Registering it would move
   nothing.

What the decision COSTS is the honesty of the manifest, and that is paid in the
same round rather than deferred: the C3 pin turns reason 2 from a claim into a
test. A manifest that is a proven strict prefix is a true statement about the
call; an unproven one is the overclaim the plan was right to flag.

Rejected alternative: register the tail now at the structured-call layer. It is
the correct end state and it is where a follow-up should put it — but it is a
different feature's change set, and doing it inside a per-builder migration
round would mix a refactor of shared infrastructure with a feature step, which
AGENTS.md Commit Discipline forbids in one commit and Scope Control forbids in
one round.

Scope: T003 only. It adds no obligation to workers, changes no verification
tier, and leaves the tail exactly where it is today.

Reverse this decision by deleting this entry; the pin test in
`tests/orchestration/test_prompt_segments.py` stays useful either way.

## DECISION F105 D10 — red-proofs are ordered only where they can go red (2026-08-10)

Context: finding R-0252. R22's gate F ordered a mutation red-proof against a
branch of `_drop_one_newline_per_segment_boundary` that no composed prompt can
reach, so the mutation could only ever come back green. The worker ran it,
reported green, probed the branch over all 64 optional-argument combinations to
show WHY, and declared it. Nothing was damaged; a round again spent a declared
deviation proving a reviewer mistake, and this is the sixth instance of the
unsatisfiable-gate class across F104 and F105.

What makes it worth its own decision rather than a note under D8 is that D8's
four items cannot catch it. They are checks on the block's own bytes — count
the lines, check a zero-gate against the block's own TO slices, count a
replacement against its file's cap, test whether a TO contains its FROM. All
four are answerable by reading the block alone. Reachability is a property of
the CODE the block points at, so it is a different kind of check and belongs as
its own item.

D10 — §3's checklist gains a fifth item: order a mutation red-proof only where
the mutated branch is reachable by the tests meant to go red, and when that is
not obvious, order the PROBE ("replace the branch with a raise, report whether
anything fails") rather than asserting the colour. The probe is strictly more
informative than a guess: it returns the same evidence whether the branch is
live or dead, and it cannot produce a gate the worker has to declare its way
out of.

The alternative — drop the red-proof when reachability is uncertain — was
rejected. Red-proofs are the only thing separating a test that pins behaviour
from a test that merely runs, and F105's own R-0229 was found exactly this way.
Fewer red-proofs is the wrong direction; better-aimed ones is the right one.

Scope: reviewer-authored blocks, as with D8. It adds no obligation to workers
and changes no verification tier.

Reverse this decision by deleting this entry and §3 checklist item 5.

D11 — the orchestrator prompt's evidence sink lives INSIDE `run_mission`, not
in `remedy mission run`. The mission-plan site put its sink in `plan_mission`,
a package function, and `.agent/plan.md` carried the orchestrator site as two
rounds: `mission_cmd.py` first, `gauntlet_runner.py` second. Reading the
callers dissolved the second round. `run_mission` has TWO production callers —
`apps/cli/commands/mission_cmd.py:366` and `packages/orchestration/
gauntlet_runner.py:514` through `deps.run_mission` — and it already owns the
mission's evidence directory, because `append_ledger_entry` writes the ledger
into it every iteration. A sink in the CLI would have left every gauntlet run
with no orchestrator prompt evidence at all, and the gate would have been green
the whole time: the F104 R-0220 class, where the caller is the thing nobody
checked.

Placing it in `run_mission` also settles WHEN the write happens. The loop has
several return paths and a boundary that turns a raise into a terminal, so a
single flush after the loop would lose the calls a crashed or stopped run had
already made. The append therefore happens per iteration, immediately after the
provider call, exactly as the ledger entry does a few lines away — one
durability rule for both records of the same iteration.

The alternative — flush once from each caller, copying `plan_mission` literally
— was rejected on both counts: it duplicates the sink per caller and it trades
the ledger's durability for a shape that only looks consistent.

Consequence, stated so it is not mistaken for an omission: the gauntlet's
orchestrator rows land in evidence from this round on, but carry an EMPTY
provider label until `gauntlet_runner.py:514` names it. Unlabeled is honest;
mislabeled would not be. That is a one-line round, no longer a wiring round.

Reverse this decision by deleting this entry, dropping the append from
`run_mission`, and flushing a caller-owned `traces` list in each of the two
callers instead.

D12 — §3's pre-emission checklist gains a SEVENTH item: before ordering a change
that ADDS a string to a file, grep the suite for tests that COUNT that string
over that whole file. R33 lost two of its items to a guard nobody looked at:
`test_mission_compiler.py` asserted `source.count('provider_kind="ollama"') == 1`
over all of `mission_cmd.py`, so a correct second call site could not land
(finding R-0258, the seventh instance of the unsatisfiable-gate class).

The four earlier items read the block's own bytes, item 5 reads the code the
block points at, item 6 reads the file the block writes into. This one reads the
TESTS that already guard that file — a fourth place, which is why it is a
seventh item and not a clause bolted onto item 6.

The alternative — forbid file-wide `source.count(...)` guards outright — was
rejected: they are the only cheap way to pin a CLI wiring line no behavioural
test reaches (F105 R28 introduced them deliberately). The defect is the SCOPE,
not the technique, so the rule is "scope the guard to its call site".

Reverse this decision by deleting this entry and §3 checklist item 7.

D13 — Remedy deliberately does NOT label the provider on the gauntlet's
`run_mission` call. D11 left it as "a one-line round"; reading the call site
retires that plan. `apps/cli/commands/mission_cmd.py` can honestly name Ollama
because `_orchestrator_call_fn` is unconditionally `make_structured_call_fn`.
The gauntlet's call_fn arrives through `deps.move_call_fn()`, a substitutable
seam whose default is Ollama but whose whole purpose is being replaced, so a
hardcoded label there would write a guess into evidence every time a caller
substituted the seam.

An EMPTY label already means "the caller did not name it", which `run_mission`'s
docstring states, and which is exactly true of the gauntlet. Unlabelled is
honest; mislabelled is not, and this repository records unmeasured cost as
unmeasured rather than estimating it into the record.

The alternative — thread a provider label through the deps object so the
gauntlet reports the provider it actually used — is the RIGHT fix and is not
rejected, only deferred: it is a deps-shape change, not a one-liner, and F105 is
about prompt composition. The absence is documented at the call site so a reader
searching for the missing label finds the reason instead of a gap.

Reverse this decision by threading the label through `GauntletDeps` and passing
it at that call site.

D14 — T004 renders the cache-read share the ledger ACTUALLY carries, names the
gap, and does not fix the producer. This answers all five open questions at the
end of `.agent/t004_inventory.md`, which the R42 investigation raised and which
no later round should re-derive.

Q1, the role column: NO, T004 does not fix
`packages/orchestration/pingpong_loop.py:3970` first. F105's goal is prompt
COMPOSITION; rewriting who writes a role into token accounting is a different
feature's change and would put an unreviewed producer edit under a prompt
feature's PR. The view therefore reports per role over what the ledger holds and
states, in its own output, that production rows currently carry one role. A
reader learns the truth including its limit — which is this repository's rule for
every figure it prints.

Q2, one row per task run: MOOT under Q1 and deliberately left so. No row splits,
no role becomes a list, and the view does NOT reach into
`token_accounting.json`'s `by_role` behind the ledger's back. The ledger is the
mirror this surface reads (stats_ledger_cmd's own stated contract); adding a
second, richer path for one subcommand would give the same question two answers.

Q3, fixtures: the evidence-tree-backfilled shape
(`tests/cli/test_stats_cost.py:121`), NOT the directly-written ledger
(`tests/orchestration/test_token_ledger.py:909`). Only the first exercises the
producer path, and a fixture that skips the producer would render green over
exactly the gap R-0266 names.

Q4, the measured-zero collapse: YES, a finding against the actuals feature —
registered as R-0265, not worked around inside T004. A workaround inside the
view would be a second place where "reported 0" and "not reported" are guessed
apart, and the guess would be invisible.

Q5, vocabulary: the EXISTING word `unmeasured`
(`apps/cli/commands/stats_ledger_cmd.py:44`). One spelling per concept
(AGENTS.md, Code Discoverability Conventions); the feature file's phrase "not
reported" is prose describing that word, not a second one to introduce.

The alternative considered and rejected for now: fix the producer inside T004 so
the per-role figure is real. It is the RIGHT eventual fix and R-0266 records it
as such; it is rejected HERE because it is a token-accounting change that would
ride into a prompt-composition PR unreviewed by anyone reading that PR's title.

Reverse this decision by deleting this entry and re-scoping T004 to include the
producer fix, with R-0266 closed in the same round.

D15 — a cache-read share needs TWO words for "no number here", not one.
DECISION D14 Q5 ruled that a figure nobody reported prints the existing word
`unmeasured`, and that stands. But a SHARE has a second way to have no value:
a bucket whose inputs WERE reported and are both zero divides 0 by 0. Printing
`unmeasured` there would blame a provider for a figure it did in fact report —
the P6 lie pointing the other way — and printing `0.0%` would invent a
measurement. That case prints `undefined`, defined beside `UNMEASURED` in
`apps/cli/commands/stats_ledger_cmd.py` with the reason above it.

The alternative considered and rejected: one word for both, on the "one
spelling per concept" rule (AGENTS.md). Rejected because they are two
concepts, not one spelling of one — "nobody measured this" and "this measured
to nothing" differ exactly where a reader's next action differs.

Reverse this decision by deleting `UNDEFINED_SHARE` and returning `UNMEASURED`
for the zero-denominator case, with the test that pins the two words dropped.

## DECISION F105 D16 (2026-08-12) — the Open PR Gate does not block a
## closure PR

Chosen: PR #189 (`docs/amend0810-clerical` -> `main`) is stop-and-report and
stays untouched — not merged, not commented on, not modified — because it
does not originate from a `feature/*` branch. It does NOT block creating the
F105 closure pull request. The AGENTS.md Open PR Gate fires "before creating
a new feature branch or starting a new unrelated task"; closing F105 is
neither, it is the completion of the branch already in hand. The closure
protocol already leaves the closure PR unmerged until the next feature's
start, where the gate will see both PRs and correctly stop-and-report.

Alternatives considered. (a) Wait for the operator before closing: rejected —
from 2026-08-13 the operator reaches this machine only over SSH from a phone
(docs/agents/self_drive_protocol.md), so a finished feature would stall
indefinitely on an action the operator must take for #189 either way, and
every later session would re-derive F105's state from scratch. (b) Merge #189
to clear the gate: FORBIDDEN — a non-`feature/*` PR is stop-and-report and
merging it is outside any agent's authority here.

Reverse this decision by closing the F105 pull request; the branch and every
commit on it survive untouched.

Operator note, not a blocker: PR #189 and this branch both modify
`docs/agents/reviewer_conventions.md`, so whichever merges second may need a
conflict resolution.

## DECISION F107 D1 (2026-08-12) — two Design bullets are DEFERRED, on the record

Context: finding R-0291. The feature file's Design promises that the compiled
context "becomes a registry segment with its manifest hash in evidence", and
defines tier 1 as the files_hint AND the fence allow scope. Neither holds on
disk. `register_compiled_context_segment` exists and is unit-tested but has no
production caller; the run path in `pingpong_loop.py` passes a rendered context
string and a category label, not a registered segment, and writes no manifest
into evidence. The CLI's tier 1 is the files_hint alone. Both gaps are
deliberate and documented at the source — `context_compiler.py:66-68` states
the deferral outright — but a deferral recorded only in a module docstring is
invisible to the operator, and §4.7 requires a spec deviation to be loud,
persisted and reversible.

Chosen: DEFER both, close F107 on its DONE sentence, and record the deferral
here and in the feature file's Built State. F107's DONE sentence is about
selection, shrink and the omissions record — all three are built, tested and
reviewed. Wiring the manifest into run evidence belongs with the evidence
schema, and merging fence allow-globs into tier 1 belongs with F017's fence
semantics; each is a round of its own with its own gate.

Alternatives considered: (a) wire both inside F107 — rejected, it widens a
feature already at seventeen rounds and drags F017 semantics into a context
feature; (b) amend the Design bullets to match the code — rejected, that edits
the target plan to fit what was built, which is exactly backwards, and the
capability is wanted, only later.

Reverse this decision by wiring `register_compiled_context_segment` into the
run path with its manifest recorded in evidence, and by merging the fence allow
scope into the CLI's tier-1 seed; the Design bullets then need no change,
because they already describe the intended end state.

## DECISION F107 D2 (2026-08-12) — the omission vocabulary gains a fifth reason

Context: finding R-0292. The Design enumerates the omission reasons as
`budget|distance|binary|size`. None of the four honestly describes a file that
decodes cleanly but cannot be parsed: it is not binary, not distant, not over a
size cap and not budget-demoted, yet its signature rendering is empty and the
record must say why.

Chosen: add `unparseable` as a fifth reason and amend the Design enumeration in
the same round as the code, so the plan and the disk never disagree. The word
appears in the feature file, the user guide and the module, and is pinned by
the vocabulary test that already guards the other four.

Alternatives considered: (a) reuse `binary` — rejected as dishonest, the file
decodes fine; (b) drop the file entirely instead of recording it — rejected, an
unparseable file's path and existence are still context the model can use, and
dropping it would lose more than it explains.

Reverse this decision by removing the constant and its three tests; the
Edge-cases clause "signature-skipped with reason" would then have no carrier
again, which is the state R-0292 recorded.

## DECISION F107 D3 (2026-08-12) — the blocked package is unblocked by MOVING scratch, not by editing the packager and not by deleting evidence

Context: finding R-0295. F107's closure needs a review zip; the build published
one and then rejected it, exit 1, because 1834 of its 10534 members came from
two scratch trees under `.remedy-wt/` that carry `.data/` and `.git/` path
components. The review subject itself is correct. Three ways out existed and
they are not equally safe.

Chosen: MOVE `.remedy-wt/r11gate` and `.remedy-wt/r9gate` to
`/home/decodeux/remedy-scratch-archive/f107/`, outside the repository, then
rebuild the evidence bundle and the zip at the round's final head. This changes
no tracked file, destroys nothing, and is reversed by moving the two
directories back. The scratch stays on the same machine and stays readable, so
the R-0288 rule that a gate's raw records remain re-derivable still holds — the
path changes, the record does not.

Alternatives considered: (a) add `-path './.remedy-wt'` to the packager's prune
list — the correct DURABLE fix and the one R-0295 names, rejected HERE because
`scripts/make_review_zip.sh` is not F107's code: a packaging change made inside
a context-compiler feature is exactly the scope drift AGENTS.md forbids, and it
would ship a production change whose own tests and gate this feature never
planned. (b) delete the two scratch trees — rejected outright: deletion is
irreversible, it destroys the raw records of F107's own R9 and R11 gates, and
no closure is worth trading evidence for convenience.

Reverse this decision by moving both directories back from the archive. The
follow-up that owns the packager should then apply alternative (a), after which
neither the move nor this decision is needed again.

## DECISION F107 D3a (2026-08-12) — the D3 archive moves INSIDE the repo, to a path the packager already prunes

Context: finding R-0297. D3 chose to move the two offending scratch trees to
`/home/decodeux/remedy-scratch-archive/`, outside the repository. That path is
unreachable: this session's permission layer denies every filesystem access
outside `/home/decodeux/Repos/remedy`, for the worker and for the reviewer
alike. D3's REASONING survives intact — move rather than delete, and do not
edit a packager this feature does not own — only its destination was wrong.

Chosen: archive to `.remedy-wt/.cache/f107-archive/` instead. The path is
inside the repository, so it is reachable; `.gitignore:235` already ignores all
of `.remedy-wt/`, so nothing enters the review subject; and the packager's own
prune list matches it — `scripts/make_review_zip.sh:236` prunes
`-path './*/.cache'`, which `./.remedy-wt/.cache` satisfies, so `find` never
descends into it and the 1834 unsafe members never reach the archive. Both
properties were verified by the reviewer against the disk before this block was
emitted, which is exactly what R-0297 says should have happened the first time.
This is strictly better than D3's original target for the R-0288 rule as well:
the raw gate records stay inside the repo's own scratch directory, where the
protocol says scratch lives, rather than migrating to a private sibling path
that a later reader would have no reason to look in.

Alternatives considered: (a) `.data/remedy-scratch-archive/` — pruned and
ignored too, rejected because `.data` is the application's data root and agent
scratch does not belong in it; (b) widen the session sandbox to reach the
original path — rejected, a permission boundary is not an obstacle to route
around, and nothing about this feature justifies loosening one; (c) delete the
trees — rejected for the same reason D3 rejected it, and the reason has not
weakened: they are F107's own R9 and R11 raw gate records.

Reverse this decision by moving the two directories back from
`.remedy-wt/.cache/f107-archive/` to `.remedy-wt/`. The durable fix R-0295
names — one `-path './.remedy-wt'` line in the packager's prune list — retires
D3, this amendment and the move together.

## DECISION F115 D2 (2026-08-13) — the planner call site needs a COMPOSER built, not a composition threaded

Context: F115 D1 committed to wiring the three unwired `build_trace_entry` call
sites through the prompt-segment registry so live ledger rows stop resolving to
an empty manifest. Two are done — the builder at `pingpong_loop.py:2795` (R2)
and the reviewer at `pingpong_loop.py:2987` (R4). Both were mechanical: a
`compose_*_prompt` function already existed beside the call site, the legacy
`_build_*_prompt` wrapper already returned `compose_*_prompt(...).text`, and
the round only had to compose at the call site and hand the `ComposedPrompt`
to the trace entry. The sent bytes could not change, and the goldens proved it.

The planner site is NOT that shape, and this is recorded before it is ordered
so no round discovers it mid-flight. The facts, read at the F115 R5 gate:

* The trace entry is built at `apps/cli/commands/job.py:236`, inside the
  `_record_plan_call` callback, from an `effective_prompt` STRING.
* That string arrives through `make_structured_planner`
  (`packages/orchestration/structured_planner.py:59`), whose contract is
  `on_call(attempt, schema_v, is_parse_retry, effective_prompt)`
  (`structured_planner.py:68`) — a string, by design, because the engine is
  provider-agnostic and driven by an injected `call_fn`.
* The prompt itself is built in `plan_job_with_llm` at
  `packages/orchestration/llm_planner.py:107-109`: `prompt = job.user_prompt or
  job.name`, then `prompt = f"{prompt}\n\n{memory_section}"` when recalled
  memory exists. It is two concatenated parts and nothing else.
* There is NO composer to reuse: `grep -c 'ComposedPrompt'
  packages/orchestration/llm_planner.py` prints 0. Unlike the builder and the
  reviewer, no registry-backed function exists to call.

Chosen: a later round BUILDS `compose_planner_prompt` in `llm_planner.py` over
the two parts that already exist — the job prompt at TASK rank and the recalled
memory section at JOB_CONTEXT rank — and threads the resulting `ComposedPrompt`
out to `_record_plan_call` through an explicit optional hook on
`plan_job_with_llm`, leaving `call_planner` still receiving the same string.
The sent bytes stay identical because `compose_prompt_segments` joins with the
two-character `PROMPT_SEGMENT_DELIMITER` (`prompt_segments.py:188`), which is
exactly the `\n\n` the current concatenation already uses — that identity is
the round's first gate, not an assumption, and if it does not hold the round
stops rather than changing what the planner sends.

Alternatives considered: (a) widen `on_call` to carry a `ComposedPrompt` —
rejected, it changes a provider-agnostic engine contract for one caller's
telemetry; (b) compose in `job.py` instead, duplicating the prompt assembly at
the CLI — rejected, two places would build the planner prompt and could drift,
which is the exact failure `_build_reviewer_prompt` was collapsed into
`compose_reviewer_prompt` to prevent; (c) accept a permanently empty planner
manifest and report those rows "unattributed" — rejected as the default, but it
remains the honest fallback if the byte-identity gate fails, and F115 already
owes "unattributed" rendering for historical rows regardless.

Reverse this decision by deleting this entry. Nothing in the tree depends on it
yet: it is a plan for a round that has not run.

## DECISION F115 D3 (2026-08-13) — the planner segments rank so composition reproduces the sent order

Supersedes the RANK ASSIGNMENT in DECISION F115 D2 and nothing else in it: the
composer, the optional hook, the untouched `on_call` contract and the
byte-identity-first gate all stand as D2 recorded them.

Context: `compose_prompt_segments` sorts by `(int(rank), registration index)`
ascending, and `SegmentStabilityRank.JOB_CONTEXT` is 3 against TASK's 4, so D2's
ranks compose the memory section BEFORE the job prompt. The sent bytes are the
other order: `llm_planner.py:107-109` builds `prompt` from `job.user_prompt or
job.name`, then appends `f"\n\n{memory_section}"`. D2's ranks and D2's identity
gate contradict each other; the gate is the load-bearing half.

Chosen: `planner_job_prompt` at `SegmentStabilityRank.TASK` and
`planner_memory_context` at `SegmentStabilityRank.STEERING` — the only pair of
DISTINCT ranks that reproduces the existing order. The scale's declared meaning
is cache stability, "stable prefixes first, volatile tails last"
(`prompt_segments.py:52`), and a per-job memory recall already sitting in the
prompt's tail belongs there on both readings.

Alternatives: (a) both segments at TASK rank, letting the registration-index
tie-break carry the order — rejected, it makes a tie-break load-bearing where a
rank states the same thing explicitly; (b) memory at DOSSIER or CONVENTIONS —
rejected, both are below TASK and reverse the order as JOB_CONTEXT does;
(c) keep D2's ranks and let the sent bytes change — rejected outright, F115 D1
is that the manifest describes what was sent, and a telemetry feature may not
edit the prompt it measures.

Reverse by deleting this entry and restoring D2's ranks — which also means
accepting a changed planner prompt, so the two are one decision.

## DECISION F115 D4 — the manifest gets its own table, not a ledger column (2026-08-13)

Context, from `.agent/f115_inventory.md` section "## T001 persistence inventory
(R7)", every citation re-read by the reviewer at the R8 gate: a `calls` row is
ONE FINALIZED TASK RUN keyed `"<job_id>:<task_id>"` (`token_ledger.py:178-192`,
DECISION F103 D16), while a segment manifest belongs to ONE PROVIDER CALL
(`prompt_trace.py:74-83`). The mapping is one-to-many. Three constraints then
decide the shape rather than merely colour it:

1. `verify_ledger` compares a stored row against a record re-derived from
   evidence by WHOLE-DATACLASS EQUALITY (`token_ledger.py:688-701`), so any
   column added to `_CALL_COLUMNS` must be reproducible by
   `call_record_from_evidence` — or every row reads as drift.
2. The live ledger hook fires BEFORE `prompt_trace.jsonl` is copied into
   `task_runs/<task_id>/`: `_record_finalized_call_in_ledger` at
   `pingpong_evidence.py:517-525`, the copy at `:527-536`. A later backfill
   reads that same tree WITH the file present. An evidence-derived manifest
   column would therefore be NULL live and non-NULL on backfill, which is
   constraint 1 firing on every row the feature cares about.
3. `record_call` writes `INSERT OR IGNORE` (`token_ledger.py:425-428`), which
   never UPDATEs, so a manifest cannot be attached to an existing row later.

Chosen: a NEW table `call_segments`, added as migration step 2, with
`SCHEMA_VERSION` bumped to 2. One row per segment of one composed prompt, its
value columns mirroring `ComposedPrompt.manifest_as_dicts()` one for one
(`prompt_segments.py:107-121` — name, rank, sha256, chars, tokens_estimated),
keyed by the ledger row's `call_id` plus `trace_seq`, the zero-based position of
the trace line within that task run's entries. `calls`, `CallRecord` and
`_CALL_COLUMNS` are not touched, so constraint 1 cannot fire and no existing
row's verify result moves. Backfill tolerance is STRUCTURAL rather than coded: a
pre-F115 row simply has no `call_segments` rows, and "no rows" is what the
report renders as unattributed — never guessed, and never a fabricated zero.

Alternatives considered. (a) An aggregate manifest column on `calls` — rejected
by constraints 1 and 2, and it would squash a one-to-many relation into a single
value, losing exactly the per-segment detail the feature exists to show. (b) A
reference to the trace file — rejected because the row ALREADY carries one:
`evidence_ref` is `"task_runs/<task_id>"` (`token_ledger.py:547-549`), which is
exactly the directory the trace file is copied into (`pingpong_evidence.py:533`),
so the option adds no information the row lacks; and a JSONL path cannot be
aggregated in SQL, which is precisely what T002's queries need.

Scope: this decision lands SCHEMA ONLY. Nothing writes to `call_segments` yet —
the writer is the next round. An inert table is what makes this a separately
reviewable commit rather than a schema change smuggled in beside its consumer.

Reverse by deleting the `2:` entry from `_MIGRATIONS`, restoring the version
constant to 1, and dropping the docstring bullet that names the table. A ledger
already migrated keeps an empty unused table, which no code reads.

## DECISION F115 D5 — `until` is EXCLUSIVE, so a period is half-open (2026-08-13)

`--until` is the second end of the report period T003 needs, and its boundary
reading is a real choice with a real failure mode. It is settled as EXCLUSIVE:
`_cost_filters` emits `ts_utc < ?`, so a period is `[since, until)`.

Why exclusive. The prior-period comparison the feature file asks for is the
equal-length window immediately before `since` — that is, `[since - d, since)`
where `d = until - since`. Two adjacent windows must partition the calls
between them exactly once. With an INCLUSIVE end, a call whose `ts_utc` equals
the shared boundary falls into BOTH windows: it is added to the current period
and to the one it is being compared against, and the comparison then reports a
difference that is an artifact of the boundary rather than a fact about the
run. That is the same class of defect P6 forbids elsewhere in this feature —
a number a reader cannot tell apart from a measurement.

It also matches `since`, which is already `>=`. One end closed and one end
open is the only pairing under which concatenating periods is lossless and
duplicate-free, and it is the reading every calendar-period query in the
report will inherit.

Alternatives considered. (a) Inclusive `<=` — rejected above; it would also
make `--until 2026-08-09` mean "through the instant 2026-08-09T00:00:00" and
nothing later that day, which is a boundary users misread in the opposite
direction. (b) Day-granular truncation of `until`, so `--until 2026-08-09`
means "through the end of that day" — rejected because it would give `until` a
different comparison shape than `since`, which is a plain lexicographic
`ts_utc` compare, and two filters on one column that parse their arguments
differently is a trap this module has no reason to set.

Scope: the QUERY LAYER only. Nothing validates an `until` string at this
layer, exactly as nothing validates `since` here; the CLI owns that, and the
CLI is not in this round. The prior-period comparison this decision exists to
serve is also not in this round — it is the next one.

Reverse by changing `ts_utc < ?` to `ts_utc <= ?` in `_cost_filters`, deleting
the half-open sentence from the two query docstrings, and updating the
boundary test that names the excluded call. Nothing else depends on the
reading.

## DECISION F115 D6 — the prior period reuses the current period's `since` STRING (2026-08-13)

The prior-period comparison needs the equal-length window immediately before
`[since, until)`. The arithmetic is obvious; the SERIALISATION is not, and it
is where this would have gone wrong.

The prior window is `[parsed_since - d, since)` where `d = until - since`. Its
opening bound is computed and must be serialised. Its CLOSING bound is not
computed at all: it is the ORIGINAL `since` string, byte for byte, passed
through untouched.

Why that matters. `_cost_filters` compares `ts_utc` LEXICOGRAPHICALLY — that is
the whole reason `ts_utc` is TEXT rather than an epoch number, and `query_cost`
says so in its own docstring. Two windows abut correctly only if the boundary
they share is the SAME STRING on both sides. Round-tripping it through
`fromisoformat` and `.isoformat()` does not guarantee that: `"2026-08-01"`
comes back as `"2026-08-01T00:00:00"`, and `"...+00:00"` and `"...Z"` are the
same instant in two spellings. Every one of those round-trips still happens to
order correctly against a well-formed `ts_utc`, which is precisely the danger —
it would work by formatting luck, and the first ledger written in a different
ISO-8601 shape would silently double-count or drop the boundary call. Passing
the original bytes through makes the partition property of DECISION F115 D5
hold by construction instead.

Four cases yield no prior window at all, and each states its own reason rather
than returning a bare None: an open-ended period has no length to mirror; an
unparseable end is never guessed at; a naive end paired with an aware one is a
`TypeError` from `datetime`, and inventing an offset to avoid it would be
fabricating the user's timezone; and a period whose end is at or before its
start has an empty or inverted prior window. A fifth case is not an error but
still not a comparison: a prior window that EXISTS and holds zero calls. It is
reported as "read, and empty", which is the P6 distinction between not having
looked and having looked and found nothing.

Alternatives considered. (a) Return `None` for every unavailable case —
rejected because the report must print WHY there is no comparison, and a bare
None cannot say. (b) Normalise both ends to a canonical UTC spelling before
comparing — rejected as a larger change with a wider blast radius: it would
alter how `since` itself filters, which is pinned by existing tests and by both
goldens, for a benefit this feature does not need.

Reverse by deleting `PriorReportPeriod` and `prior_report_period` and dropping
the two comparison parameters from the renderers. Nothing else reads them: the
CLI that will call them is a later round.

## DECISION F115 D7 (2026-08-13) — the packager edit this session did not make is neither committed nor destroyed; it is stashed at closure, not now

ID note, declared deviation: the R20 block ordered this entry as DECISION
F115 D4. That ID has been taken since the R8 gate by "the manifest gets its
own table, not a ledger column" (this file, above). Two different decisions
under one ID would corrupt the ledger and break every citation of the older
one, so this entry takes the next free ID, D7. Wherever the R20 block text and
the R19 verdict entry in `.agent/live_review.md` say "DECISION F115 D4" about
`scripts/make_review_zip.sh`, they mean this entry. The body below is the
block's, verbatim.

Context: `git status --porcelain` has carried ` M scripts/make_review_zip.sh`
since 12:03 on 2026-08-13. The change is one line, `-path './.remedy-wt' -o \`,
added to the `find` prune list — precisely the durable fix finding R-0295 named
and DECISION F107 D3a deferred to "the follow-up that owns the packager". No
commit of this session touches the file and no agent of this session wrote it.

Chosen: leave it untouched through the integration gate, then, in the closure
round and only there, `git stash push -m "f115-closure: operator's make_review_zip.sh prune-list edit" -- scripts/make_review_zip.sh`
immediately before the review zip is built, and leave the stash in place. Three
facts force this. The closure protocol's precondition 5 requires a clean tree
and its zip rule says a package built from a dirty tree is INVALID, so closure
cannot proceed around it. Committing it onto this branch is the scope drift
DECISION F107 D3 already rejected in writing — a packaging change inside a
feature that does not own the packager. And discarding it destroys another
actor's uncommitted work, which no closure is worth. A stash is none of the
three: the bytes survive intact, no tracked file and no history changes, and
one command puts it back.

Alternatives considered: (a) commit it here — rejected, F107 D3's reasoning has
not weakened; (b) `git checkout --` it — rejected outright, irreversible
destruction of work this session did not author; (c) stash it NOW — rejected,
the gate does not need a clean tree and every hour it stays visible is another
hour the operator can claim it; (d) close with a dirty tree — rejected, it
produces an invalid package and a false closure record.

Reverse this decision with `git stash pop`, or by dropping the stash after the
packager's owning feature lands the same line.

## DECISION F045 D1 (2026-08-13) — loops live in a TOP-LEVEL `[[loop]]` table, not under `[remedy]`

`[[loop]]` is a top-level array of tables in `remedy.toml`, never
`[[remedy.loop]]` and never a new dotted directory convention. `load_config`
in `packages/orchestration/config.py` reads only `parsed["remedy"]`
(`_extract_remedy_table`), flattens that table to dotted keys and appends
`"Unknown key in <path>: <key>"` to `load_report.warnings` for every key absent
from `_KEY_SPEC_MAP`. `_flatten_toml` does not recurse into lists, so
`[[remedy.loop]]` would arrive as the flat key `loop` and make every config
load emit a spurious unknown-key warning. Top-level keeps the existing config
system byte-for-byte unchanged and lets `loop_spec.py` own its own table.

Alternatives considered: (a) `[[remedy.loop]]` — rejected, the warning above;
(b) a `.remedy/loops/` directory — rejected, the feature file's Orchestrator
brief explicitly forbids inventing a second config location; (c) a separate
loops file — rejected for the same reason, and configuration that is
versionable in one file is the feature's stated point.

Reverse this decision by moving the table key and teaching `config.py` to
ignore it. `tests/orchestration/test_loop_spec.py` pins it with a test that
goes red if the table moves under `[remedy]`.

## DECISION F045 D2 (2026-08-13) — the deadline contract is mirrored, not imported

`LoopBudgets.deadline` is validated in `loop_spec.py` by
`datetime.fromisoformat` plus a REQUIRED `tzinfo`, deliberately mirroring the
contract of the private `budget_resolution._parse_deadline` instead of
importing a private helper or widening `budget_resolution.py`, which belongs to
F018/F104 and which this feature does not own.

Alternatives considered: (a) import the private helper — rejected, a private
name is not an API and the coupling would be invisible to its owner;
(b) promote it to public API here — rejected, that is a change to another
feature's module inside this feature's branch.

Reverse this decision by promoting that helper to public API in a round that
legitimately opens `budget_resolution.py`, then calling it from both places.

## DECISION F045 D3 (2026-08-13) — T002 materializes the JOB action; action dispatch is T003's

T002 delivers `loop_to_job`, which takes a loop whose action kind is `job` and
produces an ordinary PLANNED job with `loop_ref` provenance. It does not
dispatch across action kinds, so it makes no claim about the mission action at
all — no user-visible "not supported yet" limit is invented. Dispatch belongs
to `run_loop` in T003, which is where the CLI, the last-run display and the
end-to-end fixture live, and which is the round that legitimately reads the
Mission model's provenance surface. The feature's Acceptance line is
job-shaped ("Fixture loop runs as a normal job with loop_ref visible in
evidence and report"), so nothing in Acceptance waits on this.

Alternatives considered: (a) dispatch both kinds in T002 — rejected, it would
require reading and extending the Mission provenance surface in a round scoped
to job materialization; (b) raise a "mission actions are not materialized yet"
error — rejected, that is a fabricated limit shipped to users for a path the
feature does support.

Reverse this decision by moving dispatch into T002 and reducing T003 to the
CLI surface.

## DECISION F045 D4 (2026-08-13) — `action.mission` is a GOAL TEMPLATE, validated like `goal_template`

`LoopAction.mission` carries a mission's GOAL as operator-authored text, not a
mission id and not a reference to an already-stored mission. A loop that named
an id could not be versioned in the config file this feature requires: the id
does not exist until the mission is created, and it differs per machine. The
text therefore accepts the same `{project}` and `{date}` placeholders as
`action.goal_template`, and `loop_spec._semantic_errors` rejects any OTHER
placeholder at VALIDATION time, mirroring the goal_template rule directly above
it. The feature file's A9 line — "Goal templates may reference simple variables
(project slug, date); undefined variables fail validation, not runtime" — is
written about goal templates; applying it to only one of the two
operator-authored templates in the same table would be an accident, not a
design.

Alternatives considered: (a) `action.mission` names a stored mission id —
rejected, ids are per-machine runtime values and cannot live in versioned
config; (b) leave the mission text unvalidated — rejected, an undefined
placeholder would then reach run time, which A9 forbids for the sibling field.

Reverse this decision by deleting the `action.mission` branch in
`_semantic_errors` and treating the field as an opaque string.

## DECISION F045 D5 (2026-08-13) — a mission-action loop records `loop_ref` on the JOB, not on the Mission

A loop firing produces one JOB. A `Mission` is a persistent goal whose chain
GROWS: `mission_state.continue_mission` (`mission_state.py:893`) appends
follow-up jobs that have nothing to do with any loop. A `loop_ref` on the
mission record would therefore claim an entire growing chain came from one
loop, and would stop being true the first time an operator types a follow-up.
The job is the unit that actually came from the loop, evidence and reports are
job-shaped, and the feature's Acceptance line asks for `loop_ref` visible in
evidence and report. So the provenance stays on the job, under the
`LOOP_REF_METADATA_KEY` metadata key T002 established, and the mission remains
reachable from that same job through `metadata["mission_id"]` and through
`mission_state.mission_for_job`. `mission_state.py` is not touched at all.

Explicitly NOT the reason: schema cost. `Mission`'s own class docstring records
the F069 precedent — `mission_plan` is "ADDITIVE and OPTIONAL", "which is why
:data:`MISSION_SCHEMA_VERSION` does NOT move for it" — so a `loop_ref: str = ""`
field could have been added without a bump. This paragraph exists because the
first draft of this decision asserted the opposite and was refused at the R3
gate (finding R-0348). The decision rests on where provenance is TRUE, not on
what recording it elsewhere would cost.

Alternatives considered: (a) add an additive optional `loop_ref` to `Mission` —
rejected, it attributes a whole chain to one firing and edits another feature's
module from inside this branch; (b) record nothing on the mission path —
rejected, Acceptance requires `loop_ref` in evidence.

Reverse this decision by adding `loop_ref: str = ""` to `Mission` as an
additive optional field — no version bump, per the `mission_plan` precedent —
and writing it in the mission path; the job-side key stays either way, because
evidence reads the job. Do NOT reverse it by bumping
`MISSION_SCHEMA_VERSION`: `Mission.from_json` raises `unknown mission schema
version` for any value but the current one, so a bump invalidates every mission
already stored.

## DECISION F045 D6 (2026-08-14) — an explicit save callable overrides root; root steers only the DEFAULT save

`_materialize_loop_job` takes both `save` and `root`. When `save` is given it is
called with the job ALONE and `root` is not consulted at all; only the default
save reaches `storage.save_job(job, root)`. So a caller chooses one of two
things — where the job goes, or that it goes nowhere — and never both.

`save` exists so a caller can capture the job without a store behind it at all,
and every current caller passes a one-argument list-appender. Giving `save` a
second, root parameter would break all of them, and it would ask a test double
to honour a path it has no store behind. The annotation
`Callable[[Job], None]` is therefore load-bearing, not incidental.

Alternative considered and rejected: drop `save` entirely and make every test
pass `root`. Rejected because the store round-trip is the subject of only three
tests; forcing the other twenty through a real store would make every one of
them slower and none of them stricter.

Reverse this decision by changing `save`'s annotation from
`Callable[[Job], None]` to one that also takes the root, and updating every
caller in `tests/orchestration/test_loop_run.py`.

## DECISION F045 D7 (2026-08-14) — `remedy loop run --yes` confirms MATERIALIZATION, never execution

WHAT: `remedy loop run <name>` materializes the named loop through
`loop_run.run_loop` and stops. The job it produces is PLANNED. `--yes` skips
the interactive confirmation and NOTHING else: it does not approve execution,
it does not change the job's state, and it does not run a task.

WHY this reading and not the other. The feature file lists the surface as
`run <name> [--yes]` (`docs/roadmap/features/T2_F045.md`, the CLI bullet) and
never says what `--yes` approves, so the flag's meaning is decided here. The
module the command calls has already decided it. From
`packages/orchestration/loop_run.py`'s module docstring, read at the
definition: "APPROVAL SEMANTICS, the load-bearing part of T002: the job stops
at PLANNED. Nothing here executes a task, approves a plan, or implies
``--yes``. ``LoopSpec.unattended`` is RECORDED in metadata so it is auditable,
and it changes NOTHING about the job's state — a loop reaches the operator's
approval gate exactly like a typed goal." A `--yes` that approved EXECUTION
would contradict that sentence from the caller's side while the callee kept
honouring it. Of the two readings, "confirm the materialization" is the one
the repository's own rules already select, and it is the smaller change: it
adds a prompt, not an execution path. (R-0348's counter-measure: a decision
that states what another module requires quotes the sentence that establishes
it instead of paraphrasing it.)

CONSEQUENCE for the operator: after `loop run` the job exists, is planned, and
is theirs to start. Nothing was executed and no provider was called. The
command says so itself — its last line names the command that would start the
job, with that job's id in it, so the stop-at-PLANNED contract is visible
rather than implied.

HOW TO REVERSE: if `--yes` should ever mean "and run it", it must go through
the same approval path a typed goal uses, and it must REFUSE for a loop whose
spec is not `unattended`. Changing this command alone would let a config file
start execution — a `[[loop]]` table written once could then run work without
ever reaching the operator's approval gate — which is exactly what the current
semantics exist to prevent.

## DECISION F045 D8 (2026-08-14) — closure precondition 2 is met by the integration gate's own definition of green, not by a zero on the suite's failure counter

WHAT was decided. `docs/roadmap/STATUS_closure_protocol.md` precondition 2
requires the "full relevant suite green". At F045's closure the full suite ends
`5 failed, 16769 passed, 19 skipped`, exit 1. F045 closes anyway, with the five
named in the STATUS verdict as PASS_WITH_RISKS and recorded here, because the
word doing the work in that precondition is RELEVANT and the five are not.

WHY this reading and not the other. `docs/agents/integration_gate.md` step 3
defines the gate's question as `comm -13 base_failed.txt branch_failed.txt` —
the failures the BRANCH introduces — and step 4 makes only "a reproducible
branch-only failure coupled to feature code" a blocker. F045's `comm -13` is
EMPTY. The five ids are `tests/orchestration/test_role_conventions.py`
parametrizations raising `PromptSegmentError: prompt segment
'reviewer_conventions' is over its token cap: 954 tokens estimated, cap 800`.
`packages/orchestration/role_conventions.py` maps that segment to
`docs/agents/reviewer_conventions.md`; `git diff main..HEAD` shows this branch
never touched that file, and the document is byte-identical to its state at
F115's accepted HEAD `705feeb19c871db6313828d76ad4e1d9e0cc4d58`, whose ancestor
`a85e82f5` (2026-08-12) is the merge that grew it past the cap. So F115 closed
over these same five ids, on the same condition, and the condition belongs to
`main` rather than to any feature branch.

The alternative — read precondition 2 as a literal zero on the failure counter
— was rejected because it makes closure depend on a defect no feature branch
may repair. AGENTS.md forbids mixing an unrelated fix into a feature branch
("Never mix unrelated features or fixes in the same branch", "no while-I'm-here
edits"), so F045 cannot lawfully fix `reviewer_conventions.md`. Under the
literal reading, EVERY feature would be blocked by a document none of them
touch, and the roadmap would stall on an unrelated file — a deadlock the
protocol's own "Failure honesty" section never contemplates, since it lists
repair, `[!]`, or an operator decision, and the repair is out of scope by rule.

CONSEQUENCE. The over-cap document is recorded as a closure CANDIDATE in
`.agent/candidates.md` rather than as an F045 finding (no R-id is spent — the
protocol's "Closure-candidate findings" rule), so the next feature's first
reviewed round must register or resolve it. It deserves its own branch: the
segment is 154 tokens over an 800-token cap, and trimming a reviewer-facing
conventions document is a content decision, not a mechanical one.

HOW TO REVERSE. Delete this decision and treat precondition 2 as a literal
zero. Doing so requires fixing `docs/agents/reviewer_conventions.md` first, in
its own branch, because otherwise nothing can close at all — which is precisely
the outcome this decision exists to avoid.

## DECISION F057 D1 (2026-08-14) — Rule A2's open-finding bar is read per review record, and the reset CARRIES open findings instead of dropping them

F057 is claimed with R-0361 open. Rule A2 (ROADMAP.md:27) says no new feature
is started while findings are open, so this decision states the reading under
which the claim proceeds, and pays for it structurally rather than by
exception.

WHY this reading and not the literal one. Six of the last seven closures in
`docs/roadmap/STATUS.md` are PASS_WITH_RISKS — F104, F105, F107, F111, F115 and
F045 — and a PASS_WITH_RISKS closure by construction leaves findings open. Read
literally, A2 would have blocked every feature claim since F103, including the
five the ledger records as accepted. The literal reading is therefore not the
one this project has been operating under, and adopting it now would stall the
roadmap on findings the closure protocol already decided were acceptable to
accept. A2's enforceable content is that a REVIEW RECORD does not close over
unresolved work, which the closure protocol's PASS_WITH_RISKS path already
gates.

WHAT IS WRONG WITH THE PRACTICE, and what this decision fixes. The practice did
not just read A2 narrowly; it erased A2's input. At the F045 closure the
reviewer recorded the open set as R-0350, R-0354 and R-0358, and the very next
record — `git show f789ebc8:.agent/live_review.md` — contains none of them. The
reset dropped three live findings without resolving, deferring or naming them.
So from this branch on, a reset CARRIES the open set forward verbatim: this
record reproduces R-0361 byte for byte out of `21c8148e:.agent/live_review.md`,
and a carried finding stays open until reviewer-authored `Done:` text closes it.
Carrying costs one line per open finding and makes A2 measurable again; dropping
costs nothing and makes it meaningless.

WHY A2 ITSELF IS NOT AMENDED HERE. AGENTS.md forbids agents editing
`docs/roadmap/ROADMAP.md` unless the operator explicitly requests it, so the
reading lives here and in the operator brief, where the operator can veto it at
any later relay. Nothing waits for an answer
(docs/agents/planner_reviewer_prompt.md §4 item 7).

SCOPE, stated so it cannot drift. This decision authorises the F057 claim and
the carry-forward. It does NOT resolve R-0361, and it does NOT recover R-0350,
R-0354 or R-0358 — that recovery and the matching rule text in
`docs/agents/planner_reviewer_prompt.md` §1 belong to their own paydown branch,
because AGENTS.md forbids mixing an unrelated fix into a feature branch. This is
the same routing DECISION F045 D8 used for the reviewer-conventions repair.

HOW TO REVERSE. Delete this decision and read A2 literally. Doing so requires
first resolving R-0361 and recovering R-0350, R-0354 and R-0358 on a paydown
branch, because otherwise no feature can be claimed at all.

## DECISION F057 D2 (2026-08-14) — the governor's acquire() contract: stop is read before cooldown, and every wait is evidence

CONTEXT. T002 builds `ProviderRateGovernor.acquire()` in
`packages/orchestration/rate_governor.py`. Three of its choices are not
derivable from the feature file and would otherwise be re-litigated at T003,
when the seam in `_call_with_retry` starts calling it.

CHOSEN. (1) `acquire()` probes `stop_check` BEFORE it reads any cooldown, and
again before every wait slice, so a stop request can never be delayed by a
pacing decision. The feature file's acceptance criterion is "a stop request
during a wait interrupts the wait immediately"; reading the cooldown first
would satisfy the words while adding a slice of latency to every stop.
(2) A wait that ends in a stop or in a deadline still records its
`RateLimitWaitEvent`. Time was really spent, and evidence that omitted it would
make a paced-then-stopped run look like a run that never waited.
(3) `retry_after_s` is honoured verbatim when the provider sends one, and the
exponential is used only in its absence — a provider that states its own
recovery time knows better than a backoff curve, and `parse_retry_after_seconds`
already rejects negatives and anything over `MAX_RETRY_AFTER_S`, so the verbatim
path cannot be fed an absurd number.

ALTERNATIVES CONSIDERED. Returning a bare bool from `acquire()`: rejected
because "did not wait" and "was stopped mid-wait" are different facts to the
caller and to the report line, and a bool erases the difference. Holding a lock
across the wait so N acquirers queue fairly: rejected as v1 scope — the feature
file says implement single-flight now, and a lock held across a wait serializes
callers a later tier will want concurrent.

HOW TO REVERSE. Delete this decision and change the three behaviours in
`acquire()`; the tests named in the R4 block pin each one, so reversing means
deleting those tests deliberately rather than discovering the change later.

## DECISION F057 D3 (2026-08-14) — the seam PACES the first call, it never terminates it

CONTEXT. T003 inserts `acquire()` into `_call_with_retry`. The retry path already
has a stop probe that returns the last `out`; the FIRST call has no probe of any
kind, so a terminating one there changes F011/F018 behaviour rather than adding
to it (`.agent/f057_t003_seam_inventory.md` section 2).

CHOSEN. Before the first call the seam WAITS out a running cooldown and then
makes the call regardless of the acquire outcome. Before a RETRY it waits and
returns the existing `out` when the outcome is not granted, joining the terminal
path the stop probe already owns. `_call_with_retry` cannot say "no call was
made" without fabricating a provider output, and the loop above already owns
termination; the wait is interruptible, so a stop during a first-call wait ends
that wait immediately, which is the acceptance criterion the feature file states.

ALTERNATIVES CONSIDERED. Aborting the first call on a stopped acquire: the only
available return value is a fabricated `out`, which is worse than a stop honoured
one call later. Skipping the first call outright while a cooldown runs: an
unpaced run by another name.

HOW TO REVERSE. Delete the first-call acquire; the retry-path acquire stands on
its own and the C4 tests name the two paths separately.

## DECISION F057 D4 (2026-08-14) — deadline_s stays None at the seam in v1; the budget is enforced through stop_check

CONTEXT. `acquire(deadline_s=...)` wants an absolute value on the injected
monotonic scale. `grep -n monotonic packages/orchestration/pingpong_loop.py`
returns nothing, and neither `JobBudgets` nor `BudgetCounters` is reachable from
`_call_with_retry`, whose only budget-shaped input is the opaque `stop_check`;
the two epochs are unrelated (inventory section 3).

CHOSEN. Pass no deadline. The budget is already enforced through the same
`stop_check` that `acquire` re-probes before every wait slice: the job's
`_stop_check` rebuilds its counters on every call and `evaluate_budget`
recomputes `now` and `elapsed` from `started_at` on every evaluation
(`packages/orchestration/budget_guard.py`), so a wall-clock or deadline breach
arising DURING a wait is seen at the next slice boundary. The governor's own
cooldown cap bounds the wait on top of that.

ALTERNATIVES CONSIDERED. Threading `JobBudgets` down as a new parameter: the
larger change, buying no behaviour `stop_check` does not already deliver.
Passing a POSIX timestamp into a monotonic parameter: inventing a scale, exactly
what the inventory warns against.

HOW TO REVERSE. Thread the deadline in and pass it. `acquire` already implements
DEADLINE_EXCEEDED and its tests already pin it, so reversing is wiring.

## DECISION F057 D5 (2026-08-14) — an empty provider skips the governor entirely

CONTEXT. `_call_with_retry` takes `provider: str = ""` and the loop itself writes
`provider=builder_name or ""`, so a falsy provider is reachable. The governor
keys its cooldowns, streaks and reasons on the raw string, so an empty key would
put every unnamed provider into ONE shared bucket.

CHOSEN. When `provider` is falsy the seam does not call the governor at all — no
observe, no acquire, no wait event. That keeps the feature's "providers without
limit signals behave exactly as today" promise trivially true for unnamed
providers, and makes the shared-bucket bug unreachable rather than unlikely.

ALTERNATIVES CONSIDERED. A sentinel key such as "unknown": it merges genuinely
different providers under one cooldown — the same bug, only harder to see.

HOW TO REVERSE. Delete the falsy-provider guard at both seam sites; the C4 test
named for it fails immediately, which is the point.

## DECISION F077 D1 (2026-08-14) — a trip always pauses; only the decision degrades on a jobless mission

CONTEXT. `enqueue_task_decision` (`packages/orchestration/escalation.py`) is
task-scoped and has no jobless guard, and no decision path in the repository
attaches to a MISSION — every producer branch of `list_decisions` is job- or
global-scoped. `evaluate_no_progress` and `evaluate_goal_drift` fire only off
`dispatched_entries`, which requires a non-empty `outcome.job_id`, so only
`burn_anomaly` can trip with no job to attach to.

CHOSEN. The pause is unconditional; the decision is best-effort. The watchdog
attaches through `mission.latest_link()` and the job's first task, exactly as
`escalate_repeated_refusal` (`packages/orchestration/orchestrator_loop.py`)
already does, and on a jobless or taskless mission it still writes `paused` and
still writes the ledger entry, recording the attachment failure as prose in the
entry's `outcome.detail` — the same shape `escalate_repeated_refusal` uses for
its three guard returns.

ALTERNATIVES CONSIDERED. Refusing to trip on a jobless mission (inventory §1
option c) is cheaper, but it trades a SAFETY stop for a reporting convenience:
a burn anomaly on a jobless mission is exactly the runaway the feature exists to
stop. A mission-anchored decision store (option b) needs a new `DECISION_TYPES`
member, a ninth `list_decisions` branch and a mission entry point for the three
`remedy decision` verbs — a schema change T002 should not carry.

HOW TO REVERSE. Make the attachment failure an early return before the pause.
The D1 test named for the jobless path fails immediately, which is the point.

## DECISION F077 D2 (2026-08-14) — F077's dedup wins, implemented in the watchdog and not in escalation.py

CONTEXT. `packages/orchestration/escalation.py`'s module docstring declines
dedup as policy — "Two tasks raising the same question produce TWO records
(deduplication is a human call, feature-file A9)" — while F077 requires one
decision per trip class, deduped within a mission until resolved. All three
existing writers enqueue unconditionally, and `enqueue_task_decision` builds a
fixed key set with no extras argument, so there is nowhere on the stored record
to hang a typed dedup key.

CHOSEN. F077's requirement wins, and the dedup lives at the WATCHDOG's layer.
`escalation.py` is not touched and keeps enqueuing whatever it is asked to; the
watchdog asks only when it should. Before enqueuing, it reads
`open_mission_decisions(mission)` — which returns the stored record dicts, each
carrying a `question`, filtered to `ESCALATION_STATUS_OPEN` across every linked
job — and skips the enqueue when a record's `question` already starts with the
marker `[watchdog:<kind>]`. The marker is a literal prefix on the question text
because that is the one caller-controlled field on the record.

ALTERNATIVES CONSIDERED. Adding dedup inside `enqueue_task_decision` reverses a
documented policy for every caller to serve one of them. A new stored key needs
`enqueue_task_decision` to accept extras — a signature change on a shared writer
for a single feature's benefit.

HOW TO REVERSE. Delete the marker scan in the watchdog. Escalation is untouched,
so nothing else in the repository changes behaviour.

## DECISION F077 D3 (2026-08-14) — the decision's own open/answered state IS the dedup state

CONTEXT. "Deduped until resolved" needs a notion of resolved. Inventory §3 lists
four candidates and all four are unbuilt.

CHOSEN. Option (a): no new state at all. Suppression means "an open decision
carrying this trip's marker exists". Answering it through
`answer_task_decision` flips the record to `ESCALATION_STATUS_ANSWERED`, which
removes it from `open_task_decisions` and therefore from
`open_mission_decisions`, and the suppression lifts on the next evaluation with
no bookkeeping. `remedy decision resolve` already reaches it, because
`_cmd_decision_resolve` (`apps/cli/commands/decision.py`) dispatches on the
`td:` prefix the escalation writer produces.

ALTERNATIVES CONSIDERED. A key on the mission record touches `Mission`'s
serialization. A file under `mission_evidence_dir` is a second source of truth
beside the queue, which `decision_queue.py`'s own docstring rules out. Deriving
it from the ledger is append-only and elegant but has no notion of "answered",
which is precisely the notion the requirement is about.

HOW TO REVERSE. Introduce an explicit dedup store and read it instead. The
marker scan is one function and it is the only reader.

## DECISION F077 D4 (2026-08-14) — the missing `mission resume` verb is T003's, not T002's

CONTEXT. `_status_for_verb` (`apps/cli/commands/mission_cmd.py`) maps exactly
`achieve`, `abandon` and `pause`; `apps/cli/command_catalog.py` registers the
matching three, and a search for `mission.resume` or `mission.activate` across
`apps/` and `packages/` returns nothing. A paused mission has NO supported path
back to active, so a watchdog pause is terminal for the run in practice.

CHOSEN. T002 ships the pause and the deduped decision without a resume verb, and
T003 — the slice that owns the manual CLI — adds `mission resume` alongside the
watchdog command. The feature file is NOT amended: its acceptance sentence
"resume clears exactly that trip's dedup" stays true across T002 and T003
together, because D3 makes the clearing a consequence of answering the decision
rather than of the verb, and the verb only restores `active`.

ALTERNATIVES CONSIDERED. Adding the verb inside T002 widens a pause-and-decide
slice into CLI and catalog work. Shipping the pause with no route out at all,
and not writing the gap down, is how a session rediscovers it in the round that
can least afford the detour.

HOW TO REVERSE. Move the verb into T002's change set. It is one `_status_for_verb`
entry, one catalog registration and its test.

## DECISION F077 D5 (2026-08-14) — the evidence triple rides in `move.payload`, and the renderer prints it for free

CONTEXT. `MoveOutcome.to_json` emits only `status`, `detail` and — when set —
`job_id`, so the triple has no home there. Inventory §4 offers prose in
`detail`, a raw dict bypassing `MoveOutcome`, or a new `MoveOutcome` field that
`render_ledger` would not print. Five loop precedents pass `move={}` for entries
with no model move behind them.

CHOSEN. The `watchdog_tripped` entry takes
`move={"kind": "watchdog_tripped", "payload": trip.to_json()}`, a real
`MoveOutcome` for the outcome, `context_digest=""`, and the precedent zero cost
`{"calls": 0, "usage": None, "usage_source": USAGE_UNMEASURED}`. This was
checked against the reader rather than assumed: `render_ledger` prints
`move.get("kind", "unknown")` and then every key of `move["payload"]` in
`sorted` order, so `kind`, `what`, `since_iteration` and `numbers` appear in the
human ledger with NO change to the renderer. It also keeps `move["kind"]` a
total lookup for the existing bare-subscript reader in the suite.

The departure from the `move={}` precedent is deliberate and narrow: those five
entries are ones where a model move was EXPECTED and absent, whereas a watchdog
trip is an action of its own with a name. An empty move would be a claim that
nothing happened.

Re-entrancy, checked against the evaluators rather than assumed: the entry is
inert to a later watchdog pass. `dispatched_entries` skips it because its kind
is not `dispatch_job`; `evaluate_no_progress` neither counts nor clears on it
because it is neither a dispatch nor a `declare_milestone_done`; and
`measured_tokens` returns `None` for it because the cost carries no `usage`
dict, so it cannot drag a burn baseline. R8 pins each of those three with a
test.

ALTERNATIVES CONSIDERED. Prose in `detail` loses the numbers to string parsing.
A raw outcome dict bypassing `MoveOutcome` gives the entry a shape no other
entry has. A new `MoveOutcome` field is invisible to the renderer, which is the
one surface a human reads.

HOW TO REVERSE. Move the payload into `outcome`. `render_ledger` stops printing
the triple, which is the visible cost and the reason not to.

## DECISION F077 D6 (2026-08-14) — the iteration number is a parameter, defaulted, never guessed

CONTEXT. `run_mission` computes `base = next_iteration_index(...)` ONCE before
the loop and then uses `iteration = base + step - 1`, while
`next_iteration_index` re-reads the file and returns one past the highest
recorded. An external append mid-run therefore takes a number the loop is
already going to reuse, and the ledger ends up with a duplicate.

CHOSEN. The T002 action takes `iteration: int | None = None` and falls back to
`next_iteration_index(...)` only when the caller passes nothing. A manual
out-of-band audit gets a correct number; the loop, when R9 wires it in, passes
its OWN current number and no collision is possible. The hazard is closed at the
API boundary in the round that creates the boundary, rather than left for the
wiring round to discover.

ALTERNATIVES CONSIDERED. Always calling `next_iteration_index` guarantees the
collision the inventory warns about. Always requiring the caller to pass one
makes the manual CLI path carry loop bookkeeping it has no business knowing.

HOW TO REVERSE. Drop the parameter. The R9 wiring is the only caller that
passes it.

## DECISION F077 D7 (2026-08-14) — the stale docstrings are repaired to what is true TODAY, not to what T002 will make true

CONTEXT. Finding R-0384. Three sites claim no autonomous status write happens:
`set_mission_status` (`packages/orchestration/mission_state.py`),
`_cmd_mission_set_status` (`apps/cli/commands/mission_cmd.py`), and — found by
grepping the suite rather than by trusting the finding's own count — the
`TestStatusTransitions` class docstring in `tests/cli/test_mission_cmd.py`. All
three have been false since `mission_achieved` and `execute_move` landed.

CHOSEN. All three are repaired in R7, and each new text names ONLY the callers
that exist at R7: the three human verbs and the loop's two terminal moves. The
watchdog sentence is deliberately NOT written yet. The T002 inventory §5
proposes an amendment reading "and — since F077 — the autonomy watchdog, which
writes `paused`"; applying that in R7 would replace a false claim with a
different false claim, because no such caller exists until R8. R8 adds the
watchdog clause in the same commit as the watchdog.

ALTERNATIVES CONSIDERED. Repairing all three in R8 alongside the writer keeps
one commit, but leaves a known-false docstring on disk across a round for no
gain. Repairing only the two the finding named leaves the third to be found
again by whoever greps next.

HOW TO REVERSE. Restore the sentences from git history. Nothing reads them
programmatically — no test asserts any of the three, which is why they went
stale unnoticed.

## DECISION F077 D8 (2026-08-14) — T002's action ships UNWIRED, and the four e2e ledger guards are R9's declared bill

CONTEXT. Inventory §7 names four whole-ledger guards in
`tests/orchestration/test_mission_e2e.py` that a new entry kind breaks: a
`numbers == [1, 2, 3, 4, 5, 6, 7]` list equality, a seven-kind move list that
also subscripts `e["move"]["kind"]` bare, a universally quantified
`context_digest`/`cost` assertion that a zero-cost entry fails, and
`len(e2e["open_at_pause"]) == 1` over the whole mission queue. None of them
breaks while the watchdog is not called by `run_mission`.

CHOSEN. R8 builds the pause, the decision and the ledger entry as a callable
action with unit tests and adds NO call site in `orchestrator_loop.py`. R9 adds
the call site and pays all four guards in that same round. The split is recorded
here so that R8's green gate is not read as a working feature: a passing R8
proves the action is correct in isolation and proves NOTHING about the loop,
and the handback and brief for R8 must say exactly that.

ALTERNATIVES CONSIDERED. Building and wiring in one round puts a new entry
shape, a new decision writer, a dedup rule and four rewritten whole-file
assertions in one diff, where a failure in any one of them is ambiguous between
the action and the wiring.

HOW TO REVERSE. Merge R8 and R9 into one round. The guard repairs are the same
work either way; only the diagnosis cost changes.

## DECISION F077 D9 (2026-08-14) — D8's four-guard bill is re-measured as a probe, not carried as a prediction

CONTEXT. DECISION F077 D8 states that wiring `act_on_trips` into `run_mission`
breaks four whole-ledger guards in `tests/orchestration/test_mission_e2e.py` and
that the wiring round pays them. That is a PREDICTION about a colour, made
before the evaluators existed in the shape they now have. Read against the
scripted e2e scenario — `dispatch_job`, `declare_milestone_done`,
`dispatch_job`, `wait_on_decisions`, `dispatch_job`, `declare_milestone_done`,
`declare_mission_achieved` — none of the three tripwires plausibly fires:
`evaluate_no_progress` clears its run on every `declare_milestone_done` and the
longest surviving streak in that ledger is two against a default threshold of
three; `evaluate_burn_anomaly` returns `None` below `burn_min_samples +
burn_window`, which is 5 + 3 = 8 measured entries against a seven-iteration run
whose entries carry no measured `usage`; and `evaluate_goal_drift` needs a
dispatch on a milestone the plan never named, which a scripted run does not
produce. If nothing trips, no ledger entry is added and all four guards stay
green.

CHOSEN. The wiring round orders the MEASUREMENT and not the colour. It runs
`tests/orchestration/test_mission_e2e.py` at the base commit and again after the
wiring, reports both numbers, and repairs only what is actually red. A green
second run is a correct outcome that costs the round nothing and closes D8's
open bill by measurement. This follows the standing rule that a red-proof is a
probe: order the colour and a worker either fabricates it or changes code to
meet it, and both are worse than the declared deviation an honest worker is
forced into.

ALTERNATIVES CONSIDERED. Ordering the four repairs as D8 wrote them would make
a worker rewrite four correct assertions to accommodate an entry that never
arrives — a silent, permanent weakening of the strongest whole-ledger guards in
the suite, bought with no defect fixed. Deleting D8 instead of amending it would
erase the reasoning that correctly kept R8 unwired; D8's split was right and only
its forecast about the guards was not.

HOW TO REVERSE. Delete this decision and treat D8's four-guard clause as
binding again. Anything that makes the e2e scenario trip a tripwire — a lowered
threshold default, a scripted run with three same-milestone dispatches, a
milestone dropped from the plan — brings the bill back on its own, which is why
the probe is ordered every time rather than resolved once.

## DECISION F077 D10 (2026-08-14) — the watchdog's ledger entry takes its OWN iteration number, and the loop stops passing its one

CONTEXT. Finding R-0388. DECISION F077 D6 gave `act_on_trips` an `iteration`
parameter defaulting to `next_iteration_index`, and said the loop "passes its
OWN current number and no collision is possible". The R10 wiring did exactly
that, and the ledger of a tripped three-iteration run reads `[1, 2, 3, 3]`. The
collision D6 was written about — an external append racing the loop's
precomputed `base` — is real and is still closed. The collision the loop itself
creates by labelling two entries with one number is a different one, and D6 did
not consider it.

CHOSEN. `run_mission` stops passing `iteration`, so the trip is numbered from
`next_iteration_index` — one past the highest recorded — and a tripped run reads
`[1, 2, 3, 4]`. The parameter STAYS on both `act_on_trips` and `watchdog_pass`,
because T003's manual `remedy mission watchdog` path is an out-of-band caller
that may legitimately know its own number; only the loop stops supplying one.
This is safe for precisely one reason, and it is worth stating because it is the
thing that would break if the loop's shape changed: a trip always pauses the
mission, and `run_mission`'s next iteration hits its top-of-loop status check
and returns `mission_not_active` WITHOUT recording an entry, so the number the
watchdog takes can never be one the loop goes on to write.

ALTERNATIVES CONSIDERED. Keeping the duplicate and rewriting both guards would
retire the "numbered once" invariant across two test files to accommodate one
new entry kind — spending a property three mechanisms rely on, including
`next_iteration_index` itself, to avoid changing one argument. Numbering the
trip `iteration + 1` explicitly at the call site computes by hand the number
`next_iteration_index` already returns from the record, and would drift the
moment anything else appended.

HOW TO REVERSE. Restore `iteration=iteration` at the `run_mission` call site and
revert the two tests. The evidence a trip carries is unaffected either way: the
observing iteration is named by the trip's own `since_iteration` and its
`numbers` payload, never by the entry's number, which is why this decision costs
no information.

## DECISION F077 D11 (2026-08-14) — the ledger's `iteration` is not a unique key, and D10 is withdrawn unimplemented

CONTEXT. Findings R-0388 and R-0391. DECISION F077 D10 ordered `run_mission` to
stop passing its own iteration number to `watchdog_pass`, so a trip would be
numbered one past the entry that caused it. It rested on two premises and both
are false. The first, that the ledger holds one entry per iteration number:
`_record` has eleven call sites in `run_mission`, and the executed move's entry
and the blocked-completion escalation's entry fire in the same pass at the same
number, shipped and green since F075 R-0190. The second, that a trip always
ends the run before another entry can be written: `run_mission`'s safe point
calls `_record` and returns BEFORE the top-of-loop status check, so a stop
requested after a trip writes an entry at exactly the number D10 hands the trip.
The worker measured it — `[1, 2, 3, 4, 4]` with the repair against
`[1, 2, 3, 3, 4]` without it — and halted rather than applying it.

CHOSEN. D10 is withdrawn without ever being implemented. DECISION F077 D6 stands
unchanged: `run_mission` passes its own iteration number, and a trip is recorded
as belonging to the iteration that produced the evidence for it. The `iteration`
field is documented, here, as an ATTRIBUTION and not a key — it answers "which
iteration does this entry belong to", a question with more than one correct
answer per number, and the ledger's ordering is its file order. The only change
this round makes is to the one test that encoded the imagined invariant.

ALTERNATIVES CONSIDERED. Making `iteration` genuinely unique would mean giving
every one of the eleven `_record` call sites its own number, retiring the
attribution meaning that the R-0190 escalation entry and the F077 trip entry
both depend on, and rewriting the guards that currently read the field as an
iteration count — a large change to a shipped audit format, bought to satisfy a
property nothing needs. Adding a separate sequence field beside `iteration`
gives the ledger two numbers where readers cope with one, and the F077 entry is
not the reason to introduce it; if a real need for row identity appears, it
arrives with its own feature and its own migration of the record shape.

HOW TO REVERSE. Re-apply D10 by restoring the `iteration=iteration` argument's
removal at the `run_mission` call site — which was never removed, so reversing
this decision is a change, not a revert. Any such attempt must first answer the
safe-point path this decision names, because that path is what made D10 unsafe
independently of whether its invariant existed.

## DECISION F077 D12 (2026-08-14) — the trip leads `mission show`, not `mission report`

CONTEXT. The feature file's T003 reads "the manual CLI + report surfacing (a
paused-by-watchdog mission's report leads with the trip) + tests", and the
obvious reading is `remedy mission report`. The R13 inventory measured that
surface and it is not what the name suggests: `mission.report`'s handler is
`_cmd_mission_report` in `apps/cli/commands/worker_facade_cmd.py`, its catalog
entry takes a RUN id rather than a mission id, and its renderer
`build_mission_morning_report` fills a `MissionMorningReport` from a
`DogfoodRun` without ever importing `mission_state`, calling `load_mission` or
reading a ledger. Its `mission_status` field is a false friend — the dogfood
contract's verdict, never one of the four `MISSION_STATUS_*` constants — so it
can never read `paused`. There is no insertion point there for a trip.

CHOSEN. The paused-by-watchdog trip leads `remedy mission show`, the
mission-facing surface that already loads the Mission, and `remedy mission
watchdog` prints the full evidence triple on demand. `mission report` is left
exactly as it is. R14 builds the watchdog command and the resume verb; R15
adds the lead block to `_cmd_mission_show` and its tests. The feature file is
NOT amended: its sentence says "a mission's report", not "the `mission report`
command", and `mission show` is that report for a mission.

ALTERNATIVES CONSIDERED. Giving `_cmd_mission_report` the resolve-or-facade
branch that `_cmd_mission_run` already carries would satisfy the literal
reading, but it puts mission-facing code in the worker facade and turns two
green exact-set guards red in the same commit (inventory Q6). Leading the
run-loop summary instead reaches only whoever runs the loop, never the human
who asks about the mission afterwards, which is the case the pause exists for.
Dropping the report surface entirely would leave T003's own sentence unmet.

HOW TO REVERSE. Delete the lead block from `_cmd_mission_show` and its tests;
nothing else depends on it. The `mission watchdog` command is independent of
this decision and survives its reversal.

## DECISION F082 D1 (2026-08-14) — F082 repairs `measure_tokens` rather than recording around it

CONTEXT. The R2 inventory established, and the reviewer confirmed writer to
reader, that `gauntlet_runner.py::measure_tokens` sums `prompt_tokens` and
`completion_tokens` while the only producer of the `cost.usage` body it reads,
`orchestrator_loop.py::measure_call_cost`, writes `input_tokens` and
`output_tokens`. A measured run therefore yields `{"in": 0, "out": 0}` and
`run.json` never gets `tokens_source: unmeasured`. Registered as R-0407.
F082's per-order record carries a `cost` field, and that field reads this
function.

DECISION. F082 repairs the key reading inside T001, additively: the function
accepts BOTH spellings, preferring the production one, and continues to return
`None` when nothing was measured. AGENTS.md forbids mixing an unrelated fix
into a feature branch, and this one is not unrelated — it is the source of the
feature's headline metric, and a bench that reports a known-false zero as a
measured cost would be a fabricated live indicator, which is a block condition
in its own right.

ALTERNATIVES CONSIDERED. (a) Leave it and label the bench's cost basis
UNKNOWN: rejected, because the wrong number would still be written into
`run.json` for every gauntlet run, and F082 would be knowingly building on it.
(b) Route it to a paydown branch and block F082 until that lands: rejected as
disproportionate for a two-line additive repair whose blast radius is one
function, and it would leave the defect live meanwhile. (c) Change
`measure_call_cost` to write the older spelling instead: rejected, because that
writer feeds consumers beyond the gauntlet and the newer spelling is the one
the rest of the token machinery uses.

HOW TO REVERSE. Restore the two summing lines in `measure_tokens` to read only
`prompt_tokens`/`completion_tokens` and delete the regression test in
`tests/orchestration/test_capability_bench.py` that names `input_tokens`.
Nothing else depends on this decision.

## DECISION F082 D2 (2026-08-14) — the bench freeze binds each order's VERSION to its digest

CONTEXT. F082's acceptance says "Changing an order file without bumping its
version fails validation." The gauntlet's freeze does not give that for free.
`gauntlet_orders.load_order_set` compares each order file's sha256 against the
digest recorded for it in `manifest.json`, so an edit alone DOES fail — but the
obvious repair is to recompute the manifest digest, and that passes with no
version bump anywhere. R2 Q3 confirmed there is no per-order version field at
all: `GauntletOrder` carries `id`, `file_name` and `sha256`, and the only
version constants are module-level and set-wide.

DECISION. Each bench order file carries its own `bench_order_version` integer,
and the manifest records, per order, a `digests` map from version string to the
sha256 of the bytes published under that version. Validation requires that the
order file's CURRENT digest equals `digests[str(version)]`. Editing the bytes
without bumping the version therefore fails, because the new bytes do not match
the digest recorded for the version the file still claims; bumping the version
requires adding a new entry to the map, which is a deliberate act and leaves the
previous pair in place as the series' own history. Changing an order starts a
new series, which is the comparability honesty the feature file asks for.

ALTERNATIVES CONSIDERED. (a) Reuse the gauntlet's single-digest manifest
unchanged: rejected, it is exactly the mechanism that permits a silent
recompute. (b) Derive the version from git history of the order file: rejected,
validation must hold in an exported evidence bundle where no git history is
present. (c) Store only the newest (version, digest) pair rather than a map:
rejected, it loses the series history that makes an old bench row's basis
readable, at no saving worth having.

HOW TO REVERSE. Drop the `digests` map from the manifest and compare against a
single `sha256` per order, matching the gauntlet's shape, and delete the
version-binding tests in `tests/orchestration/test_bench_orders.py`.

## DECISION F082 D3 (2026-08-14) — the missing two orders get a bench-owned fixture, never an edit to the gauntlet's

CONTEXT. F082's Design names five frozen orders. R4's survey found only three
expressible: `scripts/gauntlet_sample_project` is a pure-Python CLI project
with no HTTP surface and no web asset, so the API-endpoint and frontend-widget
capabilities have nothing to be written against (finding R-0411). The obvious
repair — add an `http.server` route and a static asset to that project — is
BLOCKED, and the block is structural rather than stylistic. The gauntlet's
manifest records a `template_digest`, `gauntlet_orders.load_order_set` compares
it against `template_tree_digest(template_dir)`, and the module's own history
states that a changed template is a changed set: editing that project would
turn the gauntlet's frozen ten red until its manifest were rewritten and
`GAUNTLET_ORDER_SET_VERSION` bumped, which by that module's comment RESETS the
campaign count. F082's Do-not-touch list forbids exactly this class of damage.

DECISION. The two missing capabilities are recovered, when they are recovered,
by a SEPARATE bench-owned fixture — a `scripts/bench_sample_project/` — and
never by editing the gauntlet's template. R4's inventory answer S2 establishes
that this is reachable without touching an order: an order cannot select a
template, because `run_order` calls the seam as `deps.materialise(run_dir)`
with one positional argument, so the template is a property of the
`RunnerDeps` a CAMPAIGN is given. The bench therefore supplies its own
`materialise` and its own template, which is additive in the same sense R2 Q11
established for everything else in this feature. Until that fixture exists,
F082's delivered set is three orders and its Built State says three.

ALTERNATIVES CONSIDERED. (a) Add the HTTP and frontend surface to the shared
sample project: rejected, it breaks the gauntlet's freeze and resets a campaign
count that belongs to another feature. (b) Ship three orders and amend the
feature file's Design down to three permanently: rejected, the two capabilities
are the ones that probe surfaces the CLI orders cannot reach, and dropping them
quietly would make the bench measure less while reading as complete. (c) Block
F082 until the fixture exists: rejected as disproportionate — the trend
machinery, the history and the CLI are all buildable and testable against three
orders, and the fixture is additive when it lands.

HOW TO REVERSE. Delete `scripts/bench_sample_project/` and the bench's own
`materialise` dependency, and the bench falls back to the gauntlet template
with three expressible orders — the state this decision starts from.

## DECISION F083 D1 — a red stage is inventory data, not a round blocker (2026-08-15)

Scope: the stage-runtime measurement of F083 R2, and nothing else.

R2 measures the wall time of each candidate CI stage by running it. If a stage
run reports failures, the worker records the real exit code, the real counts and
the failing node ids in `.agent/f083_inventory.md` and CONTINUES the round,
rather than treating the red as the G8 "any red gate ends the round" case.

Why: this round's product is a DESCRIPTION of the repository as it is. A red
stage is a fact about the repository and therefore part of the description —
suppressing it would make the inventory less true, and stopping on it would make
F083 unable to inventory the very condition it exists to detect. R-0205, carried
into F083 by its own feature file, records that live-state contract tests turn
red for reasons unrelated to the change under review; an inventory that cannot
survive that is an inventory that cannot be taken on this repository.

Limits: this exception covers the stage-runtime measurement only. Every ordered
gate in the R2 block still ends the round when it is red, and no later round
inherits this exception without ruling it again. Reverse this decision by
deleting this section.

## DECISION F083 D2 — the stage set, ruled from R2's measurements (2026-08-15)

R2's inventory closed with six open questions. Four of them are already decided
by its own measured data plus the feature file's Do-not-touch list, and leaving
them open would make R4 guess. They are ruled here. Two are NOT ruled, and the
reason each is deferred is stated.

RULED.

D2.1 — The stage set is exactly the five selections Q4 defines: `fast`,
`standard`, `ui`, `smoke` and `excluded`. Reason: measured, they cover the suite
(union 17007 against a suite of 17007, uncovered 0), and no sixth selection is
needed to reach any test.

D2.2 — `safety` and `architecture` do NOT become stages of their own. Reason:
Q4's open question 2 measured them as set intersections over the same node ids —
`architecture`'s 71 items all sit inside `fast`, and `safety`'s 33 split 21 into
`fast` and 12 into `standard`. Promoting either would introduce overlaps the
five-stage set does not have, and `safety` would straddle two stages. They stay
markers, usable for ad-hoc selection, and the stage runner does not name them.

D2.3 — The `standard ∩ smoke` overlap of 8 is ACCEPTED and documented, not
removed. Reason: every one of the 8 ids is in `tests/cli/test_pytest_runner.py`,
which the conftest lists in both `SUBPROCESS_FILES` and `SMOKE_FILES`; removing
the overlap means editing marker semantics, which the F083 feature file's
Do-not-touch list forbids. The stage runner therefore MAY run those 8 twice and
the summary table says so — a documented double-run beats a silent marker edit.

D2.4 — The `determinism` and `budgets` stages the feature file names are NOT
marker selections. Reason: Q8 recorded that neither name exists among the nine
declared markers, so making them selections requires declaring new markers and
assigning them across the tree, which is the same marker-semantics change D2.3
refuses. They are script invocations the stage runner calls and whose exit code
it folds into the summary, exactly as the feature file's own design paragraph
describes the budgets stage.

DEFERRED, with the reason.

D2.5 — Per-stage parallelism is NOT pinned here. Q5 measured `fast` at 391.8 s
serial for 3970 items and `standard` at 134.1 s under `-n auto` for 12546, so the
cost is dominated by serialization rather than by selection — but that single
reading does not say what `-n auto` does to `fast`, and the three small stages
may lose more to worker startup than they gain. R4 measures each of the five both
ways, once, and pins the setting per stage from that measurement. Pinning it now
would be a guess dressed as a decision.

D2.6 — The feature file's `ui-contract` and `live-provider` spellings are NOT
corrected now. Reason: `docs/roadmap/features/T2_F083.md` is edited in the round
that brings its Built State current before closure; correcting prose in a round
that writes no other doc would be scope drift, and the inventory already records
what exists under which name. Q3's record is the interim answer.

Reverse any part of this decision by deleting its numbered paragraph.

## DECISION F083 D4 — determinism does NOT become a stage of its own (2026-08-16)

R11 measured it and `.agent/f083_inventory.md` `## Q9` records it: the glob
`tests/orchestration/test_run_manifest_*.py` matches forty-five files collecting
850 tests, and a Python set operation over collected node ids puts all 850 inside
the 12579 ids the `standard` stage selects, with 0 ids outside.

CHOSEN: the determinism suite stays inside `standard`, and the ABSENCE is
documented where a reader would search for it — the `packages/orchestration/
ci_stages.py` module docstring, in this repository's own "Remedy deliberately
does NOT X because Y" idiom (AGENTS.md, Code Discoverability Conventions).

ALTERNATIVES CONSIDERED AND REJECTED: a new `determinism` marker, rejected
because assigning it across the tree is a marker-semantics change and
`docs/roadmap/features/T2_F083.md`'s Do not touch list forbids it; a
path-selected determinism stage, rejected because it buys nothing `standard`
does not already do and doubles the wall cost of 850 tests. Re-running 850
already-green tests to fill a stage name is decoration, not a check.

This SUPERSEDES the `determinism` half of D2.4 above, which left the shape open
by calling it a script invocation. `docs/roadmap/features/T2_F083.md` is amended
in the same commit: the Design stage list loses `determinism` and the T002 line
says the stage was ruled out rather than built.

Reverse this decision by narrowing `standard`'s expression and adding the stage
in the same commit — never by adding the stage alone, which would re-run the 850.

## DECISION F083 D5 — the twenty-six ruff errors are RATCHETED, not fixed (2026-08-16)

Finding R-0468 measured 26 errors from `python3 -m ruff check .` at the
repository root under this repository's own `pyproject.toml`, none of them
introduced by the F083 branch, while no CI stage ran a linter at all.

CHOSEN: the `budgets` stage carries a DOCUMENTED lint ceiling of 26
(`LINT_ERROR_CEILING` in `packages/orchestration/ci_budgets.py`) that fails when
the count RISES. The debt is frozen and visible instead of silently growing, and
the ceiling is a RATCHET: the number may only be lowered, never raised. A live
test marked `subprocess` runs the linter under the repository's own config — no
substituted flag and no `--isolated`, because a reading taken under a different
config is a reading of a different repository (finding R-0463).

ALTERNATIVES CONSIDERED AND REJECTED: fix all 26 now, rejected as scope drift —
it is a mass edit across files this feature does not otherwise touch, which
AGENTS.md Scope Control forbids as its own activity, and 25 of the 26 are
auto-fixable import hygiene that would churn a suite that was just stabilised;
leave lint out of CI entirely, rejected because it leaves this feature's own
Acceptance line green while `ruff check .` is red.

The twenty-sixth error is NOT import hygiene. It is a live `NameError` on a
guard's refusal path in `packages/orchestration/gauntlet_injection.py`, and it is
registered as finding R-0482 in `.agent/live_review.md` rather than frozen
without comment. D5 freezes it deliberately: the fix is a production change in an
unrelated module and belongs to a branch of its own.

This also SUPERSEDES the `budgets` half of D2.4 above. D2.4 assumed the stage
would be a script invocation because `budgets` is not a declared marker; the
stage that landed instead selects BY PATH through the new `CiStage.test_paths`
field, which needs no new marker and therefore touches no marker semantics.

Reverse this decision by lowering the ceiling to 0 and fixing the errors in a
branch of their own.

## DECISION F083 D6 — the tsc check resolves the LOCAL compiler or it skips (2026-08-16)

Finding R-0480 observed `tests/ui_server/test_dashboard_contract.py::
TestJobSummaryCommandContract::test_typescript_compiles` red on the first run of
the module and green on the second, and blamed a cold `npx` cache. R19 measured
that hypothesis as `## Q13` of `.agent/f083_inventory.md` and FALSIFIED it: the
cache is the per-user directory `/home/decodeux/.npm`, it is warm, and the
deliberately cold run is green. The real variable is `apps/ui/node_modules`,
which `.gitignore` excludes and which is therefore absent from every fresh clone
and every new `git worktree`. With no local TypeScript, `npx tsc` resolves the
deprecated `tsc@2.0.4` stub out of the user cache, whose bin ends in
`process.exitCode = 1` — so the assertion `result.returncode == 0` was grading a
nine-year-old stub's exit code and reporting it as a TypeScript verdict. The
first-run/second-run flip is intra-module ORDERING: the test sits above
`TestAutoBuildBehavior::test_auto_build_runs_by_default`, which really runs
`npm install`.

CHOSEN: the test resolves `apps/ui/node_modules/.bin/tsc` explicitly and runs
THAT binary; when the binary is absent it SKIPS with a message naming the missing
directory and the exact install command `npm ci --prefix apps/ui`. This is not a
new policy — it is this feature's own documented edge case, "UI toolchain absent
locally: the ui stage reports skipped with the install hint locally but is
REQUIRED hosted", finally implemented instead of merely written down.

ALTERNATIVES CONSIDERED AND REJECTED: `npx --yes`, rejected because Q13 measured
it and it changes nothing — the stub resolves either way; having the test run
`npm ci` itself, rejected because a test that installs a toolchain is a build
step wearing a test's name and it would put a network install inside the `fast`
stage; leaving the `npx` form and amending Acceptance, rejected because it keeps
a green that is a stub's exit code.

CONSEQUENCE FOR T003, recorded so it cannot be forgotten: hosted rigor is now
load-bearing. The hosted workflow MUST run `npm ci --prefix apps/ui` before the
`ui` stage, or the check skips hosted as well and the Acceptance line "Clean
checkout: `remedy ci` green locally and hosted" is met by a skip rather than by a
compile. T003 owns that step; it is also recorded in
`docs/roadmap/features/T2_F083.md`.

Reverse this decision by restoring the `npx` invocation.

## DECISION amend0816 D1 — an unmarked test may not reach a live provider (2026-08-16)

CONTEXT: F083's Acceptance asked for `remedy ci` green LOCALLY AND HOSTED with
the same stage results. Only the local half was ever checked. The first hosted
run, on closure PR #202, was red: ten failures in `fast`, every other stage
green. Reproduced exactly — same ten node ids, same 3958 passed / 7 skipped /
13091 deselected — in a throwaway venv with `pip install -e ".[dev]"` and no
`ollama` package.

CAUSE: `packages/orchestration/intake.py::make_structured_call_fn` selects
between the LLM branch and the deterministic fallback by really calling
`ollama.Client(host).list()`. Eight of the ten tests mock only what sits BEHIND
that factory (`plan_job_llm`, `make_provider_call_fn`), so the branch under test
was chosen by whether a server happened to run on the machine. The other two read
the repository's own `.git/HEAD` through the `self execute` branch guard, and
`actions/checkout` leaves a pull_request build detached, which that guard refuses.

CHOSEN: the autouse fixture `tests/conftest.py::_no_live_ollama_reach` refuses
`ollama.Client` construction for every test WITHOUT the `real_ollama` marker,
raising in `__init__` so no socket opens and no timeout is waited out. The
hosted environment becomes the one every unmarked test sees. A test that wants
the LLM branch must mock the FACTORY; a test that asserts something about a live
server carries the marker and runs in the `excluded` stage. The eight mocks were
completed and the two guard tests were given their own checkout on a feature
branch via a new `cwd` seam in `tests/cli/runtime_helpers.py::run_grouped_cli`.

ALTERNATIVES CONSIDERED AND REJECTED: pointing `REMEDY_OLLAMA_HOST` at a dead
port, rejected because it still opens a socket and makes every unmarked test pay
a connect, and because an env var is not enforcement — nothing stops the next
test from resolving a different host; marking the ten `real_ollama`, rejected
because they assert nothing about a live server, so the marker would move honest
coverage out of CI to make CI green; installing `ollama` on the runner, rejected
because it makes the runner mirror one developer's machine instead of the other
way round, and a server would still have to be started for the probe to succeed.

CONSEQUENCE: a test that silently depends on a live provider now fails on the
machine that writes it, not on a runner weeks later. Two of the repaired tests
(`test_execute_idempotent`, `test_integrity_json`) were passing hosted VACUOUSLY
— both assertions hold when execution is blocked — and now exercise the path
they name.

Reverse this decision by deleting the fixture; the drift returns with the next
test that mocks half the provider path.

## DECISION F085 D2 — the streaming seam takes the guard's CHILD half, not `run_guarded` (2026-08-17)

CONTEXT: `stream_evidence.run_streamed_command` is T002a's last unmigrated spawn.
The other two sites became `run_guarded` calls, and this one cannot: it iterates
stdout line by line into `capture_stream_evidence`, which writes evidence files as
the lines arrive and stops the child at a byte cap through an `on_cap` callback,
while `run_guarded` buffers both streams through `_StreamPump` and returns bytes at
the end. Incremental capture is what that seam exists to do, so the difference is
the feature and not a gap.

CHOSEN: split `ExecGuardPolicy`'s effect in two and share only the half that is
actually common. `exec_guard.plan_child_spawn(policy)` returns a `ChildSpawnPlan` —
the cwd, the resolved environment, the fork-to-exec `preexec_fn` and the names of
the rlimits enforced and unsupported — and BOTH supervisors pass it to their own
`Popen`. The PARENT half stays with whoever spawns: `run_guarded` keeps its
`wait4` supervision, its deadline and its pumps, and `run_streamed_command` keeps
the watchdog, process group, byte cap and stderr tail it already had. One
implementation of what a policy does TO A CHILD; two supervisors, because there
really are two.

ALTERNATIVES CONSIDERED AND REJECTED: teaching `run_guarded` a streaming mode,
rejected because it rewrites the supervision of a module T001 had just proven and
buys nothing the streaming seam does not already have; duplicating the rlimit and
scrub logic inside `stream_evidence.py`, rejected because T003 adds a network
posture to exactly that child half and a second copy is a second thing to forget;
leaving the seam unguarded and naming it in T003's limitations document, rejected
because T2_F085's Edge-cases section makes the per-class rlimit VALUES config with
per-project overrides, and a class whose only streaming site cannot receive a
configured value leaves the policy table with a hole no document closes honestly.

CONSEQUENCE: what this seam gains in stage 1 is narrow and worth stating plainly —
the rlimit `preexec_fn` and a place for the values T003 configures. It already had
a wall deadline, an output cap, a cwd pin and a killable process group. Its policy
sets no environment allowlist, for the same reason `_cli_exec_policy` sets none:
the child is the operator's authenticated `claude` CLI and reads its credentials
from the inherited environment. That is a stage-1 gap and it is owed to T003's
limitations document, not to this decision.

Reverse this decision by inlining `plan_child_spawn` back into `run_guarded` and
dropping `run_streamed_command`'s `policy` keyword; the seam returns to spawning a
child under no limits at all.

## DECISION F085 D3 — the `test`-class seam gains an `extra_env` overlay (2026-08-17)

Ruled by the reviewer at the R38 gate under docs/agents/planner_reviewer_prompt.md §4
item 7. R38 records the ruling; R39 applies it in code, and no call site migrates in
either. Reverse it before R39 by deleting this section, or after R39 by dropping the
`extra_env` parameter from `test_command_exec_policy` and `run_guarded_test_command`
and restoring `env=None`; the seam then returns to passing keys through and setting
none.

CONTEXT, measured at c3201976. Two of the twelve `test`-class sites are still on a bare
spawn, and both build their child environment the same way: `ci_run.py` line 78 overlays
`PYTEST_TIMEOUT_ENV_VAR` onto a copy of `os.environ` so each CI stage gets its own
budget, and `builder_bridge.py` line 219 overlays `PYTHONDONTWRITEBYTECODE`. The seam
offered only `extra_env_keys`, which widens the allowlist while the scrub SOURCE stays
`os.environ`, so a key the parent lacks reaches the child absent. `.agent/plan.md` at
c3201976 recorded this blocker for `builder_bridge.py` alone; it belongs to both.

CHOSEN: an `extra_env` mapping whose entries become the scrub SOURCE overlay and whose
keys join the allowlist for that call only. `scrub_child_env` keeps `FORBIDDEN_ENV_KEYS`
as the floor, so the knob cannot smuggle a secret past it, and a test pins that.

ALTERNATIVES CONSIDERED AND REJECTED: adding the two variables to
`TEST_COMMAND_ENV_ALLOWLIST`, rejected because passing a key through is not setting it —
the parent does not hold the per-stage value, and a shared allowlist is the wrong home
for one caller's variable; having each site export the variable into its own process
before spawning, rejected because that mutates the parent's environment for every
concurrent caller and outlives the call; leaving both sites unmigrated and naming them in
T003's limitations document, rejected because Amendment F085 D1's class table puts the
whole `test` class under stage-1 containment and two unguarded sites would make that row
false.

CONSEQUENCE, stated plainly rather than minimised: once R39 lands this, a caller can SET
any variable not in `FORBIDDEN_ENV_KEYS`, which is strictly more power than passing one
through, and the guard's floor is the only thing keeping that honest — so R39 owes a test
that a forbidden key handed to `extra_env` still does not reach the child. The knob
changes nothing for a caller that does not pass it: the default is `None` and the policy
stays byte-identical to today's.

## DECISION F085 D4 — the `ci_run.py` stage spawn migrates with output re-emitted and the wall as a backstop (2026-08-17)

Ruled by the reviewer at the R41 gate under docs/agents/planner_reviewer_prompt.md §4
item 7. R42 records the ruling; R43 applies it in code, and `builder_bridge.py` follows
in a later round. Reverse it before R43 by deleting this section, or after R43 by
restoring `_run_via_subprocess` to `subprocess.run(command, check=False, cwd=cwd,
env={**os.environ, PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)})` and dropping the re-emit.

CONTEXT, measured at 0e2cdacd. `.agent/handoff.md` at 93226220 named ONE behavioural
delta for this migration — that `_run_via_subprocess` streams the child's stdout and
stderr to the console through inherited fds and returns only the returncode, while
`run_guarded_test_command` CAPTURES both streams and returns them as bytes. Two more were
measured at 0e2cdacd and are equally load-bearing. First, the seam takes a WALL timeout
and raises `subprocess.TimeoutExpired`, whereas today the per-stage budget travels to the
CHILD as `REMEDY_PYTEST_TIMEOUT_SEC` and the runner self-terminates with exit code 124,
which `run_ci_stage` reads to set `note="timed out"`. Second, the seam SCRUBS the child
environment to `TEST_COMMAND_ENV_ALLOWLIST`, where today the child inherits a full copy of
`os.environ`. A migration that addressed only the output would have changed the other two
silently.

MEASURED, not assumed, before this ruling: a pytest child spawned through
`run_guarded_test_command` with the per-stage budget supplied via the `extra_env` overlay
that landed at dce66faa received 9 environment keys, read the budget back correctly, and
ran `tests/cli/test_golden_path.py` to `42 passed` at returncode 0 in 20.7 s. The
allowlist scrub does not break a pytest child in this repository, which is what made the
env delta rulable rather than a blocker.

CHOSEN, in three parts. OUTPUT: capture, then re-emit — the guarded call keeps both
streams and `_run_via_subprocess` writes them to `sys.stdout.buffer` and
`sys.stderr.buffer` before returning, so the operator still sees every stage's output and
the guard still gets its size cap. What is LOST is live streaming: output appears when a
stage ENDS rather than as it is produced, so a long stage looks silent while it runs.
Stated plainly rather than minimised, because a CI runner that appears hung is a real
cost to whoever is watching it. WALL: a backstop set ABOVE the child's own budget, never
equal to it — the child keeps `REMEDY_PYTEST_TIMEOUT_SEC` and its 124 exit code, so the
timeout that produces a readable pytest report stays the operative one, and the guard's
wall only catches a child that ignores its own budget. ENV: the allowlist plus the
per-stage budget through `extra_env`, which is precisely the capability DECISION F085 D3
added and R39 landed.

ALTERNATIVES CONSIDERED AND REJECTED: capturing without re-emitting, rejected because a CI
runner whose stage output vanishes is worse than an unguarded one; keeping the live stream
by handing inherited fds through the guard, rejected because the output cap is enforced
WHILE the guard reads the pipes and an inherited fd is never read by the guard, so the cap
would silently not apply and the migration would buy nothing; setting the guard's wall
equal to `stage.timeout_sec`, rejected because the two deadlines would race and the guard
would sometimes win, replacing an informative pytest report with a bare kill; leaving
`ci_run.py` unmigrated and naming it in T003's limitations document, rejected because
Amendment F085 D1's class table puts the whole `test` class under stage-1 containment and
an unguarded site would make that row false.

CONSEQUENCE, stated plainly. R43 owes three tests it does not have today: that a stage's
captured output actually reaches the console, that the per-stage budget still arrives in
the child, and that a wall trip maps to the `timed out` note rather than to a bare
non-zero. The size of the grace margin between the child's budget and the guard's wall is
NOT ruled here — it is R43's to choose and to justify in code, because choosing it needs a
measurement of how long a stage takes to die on its own budget, and no such measurement
exists at 0e2cdacd. `tests/orchestration/test_ci_run.py` exercises the real
`_run_via_subprocess` for the budget pass-through, so that test changes with the
implementation and is the first place a silent regression would show.

## DECISION F085 D5 — the 400-line block cap counts a block's PROSE, not the slices it transports (2026-08-17)

Ruled by the reviewer at the R44 gate under docs/agents/planner_reviewer_prompt.md §4 item 7,
which routes a wrong spec to planning as a loud, persisted, reversible decision rather than as
a question to the operator. Reverse it by deleting this section; checklist item 1 then returns
to counting every line of a block.

THE PROBLEM IS MEASURED, not anticipated. DECISION F105 D5 caps a step block at 400 lines and
checklist item 1 requires the split BEFORE emission. Three consecutive rounds have now been
shaped by that cap rather than by their work: R42 and R43 each ended with more open findings
than they started and neither moved a line of production code, and R43's own record states the
cause — the `ci_run.py` migration and its record together measured 487. R44 re-authored that
same pair from scratch with the FROM slices narrowed to the changed lines, the docstrings
pointed at DECISION F085 D4 instead of restating it, one redundant test dropped and the
finding registrations deferred, and still measured 462 before this ruling was added to it.
The cap has stopped bounding verbosity and started bounding how much code a round may carry.

WHAT THE CAP IS FOR, and therefore what it should count. Item 1's stated reason is that a
worker must save a block VERBATIM, so an oversize block cannot be fixed downstream and becomes
a declared deviation on a round that did nothing wrong. That reason bites on the text the
reviewer writes ABOUT the work — goal, constraints, gates — which can always be shorter. It
does not bite on an authored SLICE: a slice is content that must land in the repository byte
for byte, and shortening it does not make the block safer, it makes the change smaller or the
code less documented.

CHOSEN: the 400-line cap counts a block's PROSE — every line outside a BEGIN-/END- marker
pair, the marker lines included, since those are the reviewer's own. Slices are counted and
REPORTED, never capped by this rule. Every other cap stands untouched: an authored
`.agent/plan.md` text under 50 lines, a handback under 60 or with a stated cause, a commit
under 500 insertions. A block states BOTH numbers, its prose count and its total, so nothing
is hidden by the change of unit.

ALTERNATIVES CONSIDERED AND REJECTED: raising the cap to a larger single number, rejected
because it licenses longer PROSE, which is the half that actually grew and the half item 1
exists to bound; splitting every code round into a record round and a code round, rejected as
already measured — that is what R42 and R43 were, and it produced two rounds of process and no
product; trimming the authored code's documentation to fit, rejected because this repository's
discoverability conventions make the WHY beside a definition load-bearing, and a cap paid for
in comments is paid for in the thing those comments protect.

CONSEQUENCE, stated plainly. The reviewer gains room and loses the mechanical pressure that
kept blocks short, so the honest reading is that this moves a hard limit onto the reviewer's
judgement for one half of the block. R45 owes the counter-measure: a stated budget for a
RECORD slice, which is the slice class that grew, alongside the checklist item 16 widening
R-0537 named. The R44 block is the first measured under this counting and declares both of its
numbers in its own constraints.

## DECISION F085 D6 — a block is budgeted at 480 lines TOTAL, because the commit that saves it is capped at 500 insertions (2026-08-17)

Ruled by the reviewer at the R45 gate under docs/agents/planner_reviewer_prompt.md §4 item 7.
Reverse it by deleting this section; D5's 400-line PROSE cap then stands alone and the total
is again unbudgeted. This decision AMENDS nothing in AGENTS.md and weakens nothing there: the
500-insertion commit cap is untouched and remains the higher authority.

THE PROBLEM IS MEASURED, and it is finding R-0546. DECISION F085 D5 lifted the 400-line cap off
a block's authored SLICES so a round could carry code again, and its CHOSEN paragraph left "a
commit under 500 insertions" standing; the two sentences are individually correct and were
never read against each other. A block is saved by C0a as a NEW file under `.agent/authored/`,
where insertions EQUAL lines, and DECISION F105 D5 rules that path counts normally rather than
claiming the `.agent/**` single-artifact exemption. The commit cap has therefore always been a
hard ceiling on a block's TOTAL size, and D5's first application produced a 516-line block that
spent the branch's one AGENTS.md declared-oversize allowance — measured at 981d08d0, exactly
one of the 268 commits on this branch exceeds 500.

CHOSEN: a block is budgeted at 490 lines TOTAL and its PROSE stays capped at 400 by D5. The ten
lines of margin are not an estimate of anything — C0b's insertions are bounded above by the
block's own line count, so the mirror needs no allowance — they exist because a reviewer's
hand-shaped artifact must not sit within a rounding error of a hard repository cap that no
downstream actor can relax. Both numbers are MEASURED at emission and stated in the block's
constraints, and the worker re-measures both from the committed file and reports them; the
disagreement between those two readings is what makes drift visible, and stating only one of
them is what produced R-0542. A RECORD SLICE IS BUDGETED AT 140 LINES — the counter-measure D5
named as owed and did not supply. The record is the slice class that actually grew and the one
whose growth is least visible, a gate entry having no natural stopping point. A round whose
record would exceed 140 lines splits the registrations into their own round rather than
deferring them, which is what R43 and R44 each did under pressure from the wrong cap.

ALTERNATIVES CONSIDERED AND REJECTED: splitting C0a across two commits, for the reason R44's
handback gave — it puts a truncated block on disk at an intermediate commit while constraint 1
makes those exact bytes the source every slice is extracted from; claiming the `.agent/**`
single-artifact exemption for `.agent/authored/`, because DECISION F105 D5 rules that path
counts normally and this decision may not reverse another feature's ruling; raising the
AGENTS.md 500-insertion cap, because AGENTS.md is the highest authority and §4 item 7 routes a
wrong FEATURE spec to planning, never a repository rule to the reviewer.

CONSEQUENCE. 490 against 400 leaves at most 90 lines of slice in a block whose prose runs to
the cap, which is not enough for a migration; that is intentional, since it prices prose
against product at emission, where the reviewer can still shorten the prose, rather than at
commit time, where nobody can. The R45 block ran over this budget in draft and was cut to fit
before emission, dropping a checklist edit to R46, which is the rule working as intended.

## DECISION F085 D6 — correction to the ruled figure (2026-08-17)

DECISION F085 D6, applied at 812626d3, is internally inconsistent: its heading says 480 lines
TOTAL and its CHOSEN and CONSEQUENCE paragraphs say 490. THE RULED FIGURE IS 490. The CHOSEN
paragraph is the operative one — it carries the reasoning for the margin and the CONSEQUENCE
paragraph computes from it, while the heading is a leftover from an earlier draft in which the
margin was justified differently. Finding R-0547 registers the defect.

D6 is not edited, because appending a correction is how landed text stays honest in this
repository and overwriting it is worse than a dated wrong sentence — docs/agents/planner_reviewer_prompt.md
§3 checklist item 20. A reader who reaches the D6 heading reaches this section too, since both
live in `.agent/decisions.md` and this one is later.

Reverse this correction by deleting this section, which restores the ambiguity rather than the
480; reverse D6 itself by deleting D6, which returns the block cap to DECISION F085 D5's
400-line PROSE rule with no budget on the total.

## DECISION F085 D7 — the open-findings count (2026-08-19)

CHOSEN. The open-findings count over `.agent/live_review.md` is OPEN = REGISTERED − DONE, where
REGISTERED counts lines matching `^- R-\d+ — ` and DONE counts lines matching `^Done: R-\d+ — `. A
`Landed: R-\d+ — ` line is NOT a resolution and is NEVER subtracted: docs/agents/planner_reviewer_prompt.md
§4 item 4 defines it as a worker's record of an UNREVIEWED fix, written so that a session dying between
a fix and its review leaves a state no reader can mistake for a resolution, and the reviewer replaces
it with authored `Done:` text at the next gate. A finding whose fix has landed but has not been
reviewed is therefore OPEN, and it stops being open when the reviewer says so and not when the worker
does. Finding R-0566 registers the defect this settles.

ALTERNATIVE CONSIDERED and rejected: OPEN = REGISTERED − DONE − LANDED, which several blocks of this
feature carried in their arithmetic constraints. It is undetectable while no `Landed:` line exists —
which was true at every SHA this feature measured before R71 — and it silently closes a finding on the
worker's authority, which is precisely the authority §4 item 4 withholds. It was never a considered
choice; it was an unexamined formula, which is why it is written down now rather than argued about
again.

CONSEQUENCE. A round that lands a fix without a reviewer resolution does not reduce the open count, so
the count stops moving until review happens — which is the honest reading and is meant to be visible.
Blocks that state an expected open count state which formula produced it. Where a round both registers
and resolves one finding, the count is unchanged and that is not an error.

Reverse this decision by deleting this section, which returns the formula to whatever each block
asserts and restores the ambiguity R-0566 was registered for.

## DECISION amend0820-gate-autonomy A1 — loopback is exempt from the deny-network posture (2026-08-20)

CHOSEN by the operator on 2026-08-20, applied at commit f882c727 on
`feature/f085-sandbox-hardening`. `exec_guard.DENIED_NETWORK_NO_PROXY` is
`localhost,127.0.0.1,::1` and is written into both `NO_PROXY` spellings of
`DENIED_NETWORK_ENV`. Every other host — loopback or not — still goes through
`DENIED_NETWORK_PROXY_URL`, the closed discard port.

WHY. The posture as shipped emptied `NO_PROXY`, so no host was exempt and an HTTP
request a guarded `test`-class child made to a server IT HAD JUST STARTED went to the
closed proxy. That is how this repository's runtime, smoke and CLI suites judge
readiness. Hosted CI run 32301614177 measured the cost: 62 failures across the `fast`
and `standard` stages, every one of them `[Errno 111] Connection refused` against a
server whose own log line said `ready`. The sandbox exists to deny the EXTERNAL
network; it was denying the suite its own test server.

ALTERNATIVE CONSIDERED and rejected: leave the posture and stop running those suites
under the guard. It would move the network policy out of one table and into a
per-suite exception list, and it would delete coverage the guard was built to have.

CONSEQUENCE. The deny is measured where it still applies — a really-listening server
on 127.0.0.2, which the exemption does not name — and the exemption is measured
directly by `test_a_guarded_test_command_still_reaches_the_loopback_the_exemption_names`.
`docs/system/exec-guard-limitations-v0.md` states the exemption in its own words, and
`docs/roadmap/features/T2_F085.md` carries it as an amendment section. A future reader
must not describe stage 1 as denying "all" network access to a guarded child.

Reverse this decision by restoring the empty string in `DENIED_NETWORK_NO_PROXY` and
deleting the amendment section in the feature file, which returns 62 tests to red.

## DECISION amend0820-gate-autonomy A2 — a red or running CI check is work, not a blocker (2026-08-20)

CHOSEN by the operator on 2026-08-20. AGENTS.md's Open PR Gate now carries the
exception in its own words. A session that reaches the gate and finds the open PR
not merge-ready no longer ends there when the reason is its CI check: a RUNNING
check is waited on with `gh run watch --exit-status` up to 60 minutes, and a RED one
makes repairing that branch the session's work order, with commits on the open PR's
branch explicitly allowed. Only an UNREADABLE state — `gh` permissions missing, or
GitHub unreachable — still ends the session with a report.

The three grants a session needs to read that state are in `.claude/settings.json`:
`Bash(gh run:*)`, `Bash(gh api:*)` and `Bash(gh pr checks:*)`. They are added to the
TRACKED settings file rather than the untracked local one, so a fresh checkout has
them; nothing was removed, and permission allow-rules union across settings files.

WHY. F085's own gate ran out of session three times over a red check nobody could
read: `.agent/plan.md` at 4c2d707b recorded "WHICH CI stage is red is unknown,
because `gh run` and `gh api` are denied in this sandbox". The block was never a
judgement that the work could not proceed — it was a missing permission, and the
protocol turned that into a stop.

CONSEQUENCE. A session can now spend most of its budget repairing someone else's red
branch, which is intended: an unmerged PR blocks every later feature by the gate
itself. The repair rules of DECISION amend0820-gate-autonomy A1's round still bind —
no test deleted, no assertion weakened, no ceiling raised — and a stage budget is
re-derived by the rule `tests/orchestration/test_ci_stages.py` states rather than
raised by hand.

Reverse this decision by deleting the exception paragraph from AGENTS.md's Open PR
Gate, which returns the gate to stop-and-report on any failing check.

## DECISION F086 D1 — the wheel carries the built UI explicitly, and installed mode never builds it (2026-08-20)

CHOSEN. T001 makes the built UI a declared wheel artifact rather than a file that
happens to be lying around. Three parts, and the first is useless without the other
two. (a) `pyproject.toml` gains an explicit carry for `apps/ui/dist` under
`[tool.hatch.build.targets.wheel]` — `artifacts` or `force-include`, whichever the
installed hatchling honours, chosen by MEASUREMENT and not by documentation — because
that directory is untracked and matched by the generic `dist/` ignore at
`.gitignore:13`, and a build backend that respects VCS ignores will otherwise omit it
however carefully it was built first. (b) A packaging-time guard REFUSES to produce a
wheel whose `apps/ui/dist/index.html` is absent, so the failure is loud at build time
instead of silent at serve time; the feature file's "never ship a wheel with an empty
UI directory silently" is this clause. (c) `_get_frontend_dist()` in
`packages/orchestration/ui_server.py` resolves the asset directory in BOTH modes —
package-relative when installed, repository-relative in a checkout — with a test per
mode, because its three `.parent` hops land on the environment's `site-packages`
parent once installed and there is no repository root there to find.

Additionally, and rules the hazard R3's inventory surfaced as its open question 4:
in INSTALLED mode the missing-assets path does NOT spawn npm. `_load_frontend()`
today answers a missing `dist/` by running `npm install` and `npm run build`, and
`apps/ui/package.json` IS a wheel member, so that path is reachable from a user's
environment where no `node_modules` exists and no toolchain is promised. Installed
mode degrades to the honest "UI assets not built" message the feature file expects to
already exist; auto-build stays a CHECKOUT-mode convenience. The mode test is the same
one part (c) introduces, so this costs no second mechanism.

ALTERNATIVE CONSIDERED and rejected: ship the UI SOURCE and build on first serve,
which is close to today's accidental behaviour — the wheel already carries 65 files
under `apps/ui/src/` and a 182948-byte `package-lock.json` but no build output. It is
rejected because it makes every installed user's first serve depend on a network, a
node toolchain and an npm lockfile resolution, turning a packaging problem into a
runtime one, and because it cannot satisfy the feature's own DONE condition that the
UI serve work in a fresh virtualenv. Whether the wheel should keep shipping that
source at all is left to T003's wheel-size budget and is NOT ruled here.

CONSEQUENCE. The wheel stops being buildable from a bare `git worktree`: producing a
releasable artifact now requires the UI to be built first, which is a real constraint
on CI and on any human cutting a release, and it is deliberate — it is the only way the
guard in (b) can be honest. The measured baseline T001 must move is a wheel of 414
members and 2038283 bytes carrying 0 members under `apps/ui/dist/`.

Reverse this decision by deleting this section and the explicit carry it rules, which
returns the wheel to whatever the backend's default file selection produces — today,
a wheel with no UI.

## DECISION F086 D2 — one version literal, read through package metadata, honest in a checkout (2026-08-20)

CHOSEN. T002 keeps `pyproject.toml` as the single place a version NUMBER is written —
it is `version = "0.1.0"` at `pyproject.toml:7` today, and R3 measured the wheel's
METADATA agreeing with it — and `remedy --version` reads it back through
`importlib.metadata.version("remedy")` rather than through a second literal in Python
source. No `__version__` constant is introduced to be kept in sync, because a second
literal is the defect this decision exists to prevent. There is no `--version` flag
under `apps/` today; T002 adds one, and it prints the version, the git sha embedded at
build time, the Python version and the platform, as the feature file's Design asks.

In a CHECKOUT the distribution is frequently not installed and the embedded sha does
not exist, so the command reports the version it can prove and says `dev` for the build
info rather than inventing a sha or crashing. That is the feature file's "checkout mode
reports dev honestly" and it is a REQUIREMENT, not a fallback: a version command that
reports a stale or fabricated sha is worse than one that admits it is a working tree.

ALTERNATIVE CONSIDERED and rejected: generate a `_version.py` at build time as the
single source. It reads more simply at the call site, but it puts a generated file on
the import path where a stale copy in a checkout outranks the metadata and reports a
version nobody built — the precise failure mode the honest-`dev` clause exists to
avoid.

CONSEQUENCE. `remedy --version` is only fully truthful for an INSTALLED distribution,
which is the mode the release gate cares about, and the checkout mode is deliberately
less informative rather than differently informative. The release gate T003 builds can
then compare a tag against exactly one number, read from the artifact it is about to
publish.

Reverse this decision by deleting this section, which returns the version story to a
single literal with no reader and no `--version` flag.

## DECISION F086 D3 — the dual-mode resolver is withdrawn; the carry mechanism is `artifacts` (2026-08-20)

CHOSEN, and it AMENDS DECISION F086 D1 rather than replacing it. Part (c) of D1
required `_get_frontend_dist()` to resolve the asset directory in two modes,
package-relative when installed and repository-relative in a checkout, on the
stated premise that "its three `.parent` hops land on the environment's
`site-packages` parent once installed and there is no repository root there to
find". That premise is FALSE, and the R3 inventory's open question 4 carries the
same error. The hops land on the wheel ROOT, not its parent:
`packages/orchestration/ui_server.py` has exactly three ancestors up to the
archive root, and `apps/` is a sibling of `packages/` at that same root — the
identical geometry a checkout has. Measured three ways at `72e07381`: from an
extracted wheel the function returned that extraction's own `apps/ui/dist`; from
an independent copy of `packages/` plus `apps/ui/dist` laid out the same way and
placed first on `sys.path` with the working directory outside the repository, it
returned that copy's directory; and from the checkout it returned the checkout's.
In every case the loaded module's `__file__` was printed first, so the reading
could not have come from the wrong copy. No dual-mode code is therefore written,
because the single expression already satisfies both modes, and a second
resolution path would be untested surface added to satisfy a measurement error.

KEPT from part (c): the test per mode. The property is load-bearing for the
feature's own DONE condition and nothing currently pins it, so a regression that
broke installed-mode resolution would be invisible until a user's first serve. A
test that constructs a wheel-root-shaped layout and asserts the resolver follows
it is cheap, and it is the artifact that would have caught the premise error
years earlier than a human would.

CONFIRMED and now MEASURED, part (a): the explicit carry is real and both
candidate mechanisms work. From a probe worktree OUTSIDE the repository with
`apps/ui/dist` present, `pyproject.toml` AS COMMITTED AT `72e07381` produces 414
members and 0 under `apps/ui/dist/`; `artifacts = ["apps/ui/dist/**"]` produces 417 members,
2155470 bytes and 3; a `force-include` table produces 417 members, 2155479 bytes
and 3. `artifacts` is chosen: it needs no source-to-target path mapping, and it
is the smaller of the two artifacts by nine bytes. R6's measurement could not
choose between them because its control was vacuous, which is finding R-0574.

STILL OWED, part (b), and this decision sharpens why. The carry does not make an
absent UI loud: measured at `72e07381`, a build with `artifacts` applied and no
`apps/ui/dist` present exits 0 and produces the same 414-member wheel with 0 UI
files. So landing the carry alone is a strict improvement — with assets present
the wheel now ships them, where before it never did — but it does NOT satisfy
D1's "never ship a wheel with an empty UI directory silently", and no release may
be cut until the packaging-time guard exists.

ALTERNATIVE CONSIDERED and rejected: keep part (c) as written and build the
dual-mode resolver anyway, on the grounds that it is harmless. Rejected because
it is not harmless — it would add a branch no environment reaches, and a branch
no environment reaches is a branch no test can honestly red-prove, which this
repository has already paid for once (finding R-0252).

Reverse this decision by deleting this section, which restores D1 part (c) as
written and reopens the choice between `artifacts` and `force-include`.

## DECISION F086 D4 — the install smoke is written here and executed elsewhere (2026-08-20)

CHOSEN. The T2_F086 install smoke is ONE module, `tests/test_install_smoke.py`,
carrying the `smoke` and `slow` markers, which SELF-SKIPS unless the environment
variable `REMEDY_INSTALL_SMOKE` is set. Its execution host is a machine with
network access and permission to spawn an interpreter it just installed — a
GitHub runner or the operator's own shell — and never a self-drive round.

MEASURED, at R17, which is why this is a decision and not a preference: this
session's permission layer refuses to execute an interpreter under `.remedy-wt/`,
so `python3 -m venv .remedy-wt/probe-venv` succeeds and the resulting
`.remedy-wt/probe-venv/bin/python` cannot be run. A wheel install also needs the
network to resolve `pydantic>=2.0` and `psutil>=5.9`, which `pyproject.toml`
declares. Neither constraint is a property of one round; both hold for every
round of this workflow.

WHY OPT-IN RATHER THAN A NEW CI STAGE. `tests/orchestration/test_ci_stages.py`
pins the stage tuple to `("fast", "standard", "ui", "smoke", "budgets",
"excluded")`, so a new stage is a change to that pin as well; and the existing
`smoke` stage already selects `smoke`-marked tests. The opt-in variable mirrors
what `real_ollama` already does for tests the default suite must not run, which
is the pattern this repository has and the reason the marker exists.

WHAT THIS DECISION DELIBERATELY DOES NOT RULE. It does not name the CI stage that
sets the variable. That choice needs the smoke's real wall-clock, and the `smoke`
stage carries a 300 s `timeout_sec` which AGENTS.md forbids raising by hand — a
budget is re-derived by the rule `tests/orchestration/test_ci_stages.py` states,
from a re-measured maximum. Choosing the stage before measuring the duration
would be exactly the blind raise that rule exists to prevent, so it waits.

CONSEQUENCE, stated plainly so no later reader mistakes a written test for a
passing one: until that variable is set somewhere real, F086's DONE condition —
"a wheel built from a clean checkout installs into a fresh virtualenv where the
golden path and the UI serve work" — is UNPROVEN. The closure round names it as
unproven rather than counting a skipped test as coverage.

ALTERNATIVE CONSIDERED and rejected: put the smoke in the release workflow
instead, as a step of `release.yml`. Rejected because that workflow is manual and
rarely dispatched, so a packaging regression would surface at release time, which
is the latest and most expensive moment to learn about it.

Reverse this decision by deleting this section, which reopens the choice between
an opt-in marker, a new CI stage, and a release-workflow step.

## DECISION F255 D1 — the teacher joins BOTH role vocabularies (2026-08-20)

CHOSEN. `teacher` is added to `KNOWN_ROLES` in
`packages/orchestration/role_config.py`, taking it from seven names to eight,
AND to the `ConventionsRole` enum in
`packages/orchestration/role_conventions.py`, because the teacher needs a model
(the first vocabulary) and a persisted behaviour document (the second). The
frozen pin `test_all_seven_roles_present` in
`tests/orchestration/test_role_config.py` is renamed and its tuple extended IN
THE SAME COMMIT as the vocabulary change, never in a follow-up: a ledger-style
count and its test pin land together (finding R-0151).

MEASURED at R2, which is why this is a decision and not a preference: the
registration says the teacher is "resolved through the same role_config
mechanism as orchestrator/worker/reviewer", but `worker` is NOT in
`KNOWN_ROLES` — it exists only as `ConventionsRole.WORKER`. The registration
names two vocabularies as if they were one, and this decision separates them.

DELIBERATELY NOT EXTENDED: `_ROLE_OVERRIDE_ROLES` in `apps/cli/commands/do_cmd.py`
and the `_ROLE_PROMPT_KEYS` / `_ROLE_ESTIMATED_KEYS` maps in
`packages/orchestration/token_cost_policy.py`. Those three lists describe the
roles that perform the BUILD and carry per-role prompt columns; the teacher
neither builds nor is charged against those columns, and its spend is attributed
by the ledger `role` column instead (DECISION F255 D3). A role added to a list
whose meaning it does not share is how a vocabulary rots.

ALTERNATIVE CONSIDERED and rejected: add `teacher` to `KNOWN_ROLES` alone.
Rejected because `role_conventions.py` is where a role's rules are persisted,
and a teacher with no conventions document is a prompt with no written rules —
exactly the state AGENTS.md exists to prevent for every other role.

Reverse this decision by deleting this section and removing the name from both
tuples, which restores the seven-name pin.

## DECISION F255 D2 — F255 does NOT close its own event-vocabulary dependency (2026-08-20)

CHOSEN. Stage 1 narration keys to an EXPLICITLY ENUMERATED subset of run-log
event names, declared in ONE place inside the teacher's own module and pinned by
a test. Every event outside that set is narrated as unknown, under the feature's
own honesty rule for grounding source 1 — "asserts only what evidence shows,
says unknown where it is silent". F255 does NOT build a repo-wide named-event
registry and does NOT make the emitter enforce one.

MEASURED at R2: `RunEvent.event` at `packages/orchestration/run_log.py:66` is an
unconstrained `str` and `RunLogWriter.log` validates nothing; 39 distinct event
names are emitted from 14 files; `EVENT_METADATA_SCHEMAS` covers the METADATA
KEYS of seven event types and has ZERO production callers. The registration's
declared dependency, "stable ledger event vocabulary (Tier 2)", is therefore NOT
satisfied today, and this decision refuses to pretend otherwise.

ALTERNATIVE CONSIDERED and rejected: close the dependency first — introduce the
registry and make every emitter use it. Rejected for THIS feature because it
edits the 14 emitting files and every event name in the repository, which is a
Tier 2 infrastructure feature in its own right and is nowhere in F255's scope.
Widening a Tier 5 feature into a Tier 2 refactor is the scope drift AGENTS.md
forbids, and doing it inside a teaching feature would bury it.

CONSEQUENCE, stated plainly so no later text overclaims: F255's narration is
only as stable as the names it enumerates. A rename in an unrelated module
degrades narration for that event to "unknown" rather than breaking the run —
which is the failure mode the honesty rule prefers — and the enumerated set is a
test pin, so such a rename surfaces as a RED TEST rather than as silence.

Reverse this decision by deleting this section, which reopens the choice between
an enumerated subset and a repo-wide registry.

## DECISION F255 D3 — teacher spend is REPORTED per role, and no new limit axis is built (2026-08-20)

CHOSEN. Teacher spend is separated by the `role` column that already exists on
the F103 ledger's `calls` table, and is read with `query_cost(by="role")`. F255
adds NO new budget limit and NO new limit axis. Stage 1 is declared zero-token
and charges nothing; Stage 2 charges under the role name `teacher`.

MEASURED at R2: a "pool" concept does not exist anywhere in
`packages/orchestration/` — the only two hits are an unrelated local variable.
Attribution runs on `_CALL_COLUMNS`'s `role` field; `COST_GROUP_KEYS` is exactly
`("role", "model", "day")`; and all five enforceable limits in `_LIMIT_ORDER`
are JOB-scoped, none of them per-role.

WHAT THIS DECISION DELIBERATELY DOES NOT RULE, and says so rather than letting a
later round discover it: the registration's phrase "its OWN budget pool" is
satisfied in the REPORTING sense and explicitly NOT in the LIMIT sense. No text
in this feature may claim the teacher is capped. If a cap is wanted later it is
a new axis in `budget_guard.py`, ruled then, on its own evidence.

ALTERNATIVE CONSIDERED and rejected: add a per-role limit axis now. Rejected
because it changes the enforcement path that every job already depends on, in
order to cap a role that by construction cannot influence the run — the largest
blast radius in the feature bought for the smallest gain.

Reverse this decision by deleting this section, which reopens per-role limits.

## DECISION F255 D4 — read-only is proven BEHAVIOURALLY, because the annotation proves nothing (2026-08-20)

CHOSEN. The teacher's hard read-only invariant is proven by a BEHAVIOURAL test —
the command runs and the bytes on disk are unchanged — modelled on
`tests/orchestration/test_job_budgets.py:1352`, whose comment states the standard
exactly: `action_class="read_only"` has to be true of the bytes on disk. The
`action_class="read_only"` declaration is carried as well, but it is the label,
never the guarantee.

MEASURED at R2: `ActionClass` is a `typing.Literal` at
`apps/cli/command_catalog.py:31`; a `Literal` annotation is not checked when the
frozen dataclass is constructed; and NO code path anywhere branches on
`action_class == "read_only"` to permit or deny an operation. The only
non-declaration uses are one serialization and one comment. Enforcement today is
the test suite, and only one test in it is behavioural.

CONSEQUENCE: the registration's "Hard invariants: ActionClass read_only" names a
DECLARATION. Any later sentence in this feature claiming that the annotation
enforces the invariant is false, and this decision is the reason a reviewer may
say so without re-deriving it.

ALTERNATIVE CONSIDERED and rejected: build catalog-wide runtime enforcement, so
`read_only` is checked at dispatch for every command. Rejected as out of scope —
it is a trust-core change touching every command's dispatch path, and F255 is a
Tier 5 teaching feature. It is worth doing: it is registered as a closure
candidate of this feature rather than silently dropped.

Reverse this decision by deleting this section.

## DECISION F255 D5 — F255 ships `remedy teach` and does NOT build `do watch` (2026-08-20)

CHOSEN. The feature's CLI surface is `remedy teach`. F255 does NOT build
`remedy do watch`, and it STATES its own isolation rules instead of inheriting
rules that were never written. The rules it states, taken from what the run log
actually is: the teacher opens the append-only JSONL run log READ-ONLY, re-reads
it whole through the existing production reader
`packages/orchestration/timeline.py:68`, tolerates a malformed trailing line by
dropping that line, holds no lock, and has no write path to the run at all.

MEASURED at R2: the `do` group holds fifteen commands and none is `watch`; no
`teach` command exists; and the searches that establish both are recorded in
`.agent/f255_inventory.md`. The registration's phrase "same isolation rules as
watch" therefore refers to rules that do not exist, and its CLI phrase
`remedy do watch --learn` names a command that does not exist.

ALTERNATIVE CONSIDERED and rejected: build `do watch --learn` as the
registration literally says. Rejected because `do watch` is a general live-run
viewer that is useful independently of teaching; building it inside F255 would
silently widen a teaching feature into a cockpit feature, which the
registration's own Non-goals forbid — "cockpit panel ships with Tier 5, not
before". A feature that grows a second feature inside itself cannot be reviewed
against its own Done condition.

CONSEQUENCE: the registration's CLI phrase is SUPERSEDED. R4 writes the
superseding text into `docs/roadmap/features/T5_F255.md` itself, so the feature
file and this ruling never disagree on disk — a decision that lives only here
while the feature file still says `do watch` is the R-0417 staleness class.

Reverse this decision by deleting this section and restoring the `do watch`
phrasing in the feature file.

## DECISION F255 D6 — the handback token cap is withdrawn; the LINE cap is the operative bound (2026-08-20)

CHOSEN, ruling finding R-0602. The sentence "Hard cap: this file stays ≤800
tokens — ≤1600 in the >10-commit LARGE case" is REMOVED from
`docs/agents/handback_template.md`. The line cap in that same file — ≤60, ≤100
when a >5-commit table requires it, ≤160 in the LARGE case — becomes the single
operative bound on a handback's size, and the template says so explicitly.

MEASURED: over the twelve most recent commits that rewrote `.agent/handoff.md`,
every one exceeds the token cap, in a band from 1306 to 2983 by the chars/4
estimate — 1.6x to 3.7x — while the LINE cap in the same document is met by all
of them. Two caps on one artifact disagreed, and only one was ever obeyed.

WHY WITHDRAW RATHER THAN RAISE. Raising the number to fit current practice
blesses whatever the last round happened to write and must be raised again the
next time a bundle grows. The line cap already scales with commit count, is
measured with `wc -l` and needs no tokenizer, whereas a token cap depends on an
estimator nobody has agreed on — chars/4 is itself a guess, and the true count
differs per model. A cap that cannot be measured identically by two readers
cannot be enforced by either.

ALTERNATIVE CONSIDERED and rejected: restate the cap at 3000 tokens. Rejected
for the reason above — it is the current maximum dressed as a rule, and it would
still leave two caps that can disagree.

WHERE THIS LANDS: the template edit is NOT made by this round, whose change set
is `.agent/` only. It lands in the docs round that follows the feature-file
amendment, and until it lands no round is failed against the 800-token number
and no handback claims to meet it.

Reverse this decision by deleting this section and restoring the removed
sentence.

## DECISION F255 D7 — a teacher question is a ledger row with a NULL task_id (2026-08-21)

CONTEXT. F255's acceptance requires Stage 2 to record exactly one ledger call
attributed to role `teacher`, and DECISION F255 D3 rules that teacher spend is
REPORTED through the `role` column the F103 ledger already carries. But
`packages/orchestration/token_ledger.py` states two invariants that such a write
breaks as written, both read at `8d8e7a5c`: a row is ONE FINALIZED TASK RUN keyed
`"<job_id>:<task_id>"` (DECISION D16), and the module has exactly ONE call site,
`pingpong_evidence.write_evidence_bundle`, because it never parses provider
output itself. A teacher question is neither a task nor a run, and it has no
`task_runs/<task_id>/provider_evidence.json`.

CHOSEN. Widen the row's identity by exactly one class rather than fabricate a
task run: a teacher question is a row whose `task_id` is NULL, and that NULL is
what MARKS the class. The schema already permits it — `job_id` and `task_id` are
both nullable and `call_id` alone is the primary key — so no migration is needed.
`packages/orchestration/teacher_spend.py` is the one writer, it takes no
`task_id` parameter at all, and it parses no provider output: it records figures
its caller was given. The `token_ledger` docstring is amended at C4 of the same
round, so the ruling and the module never disagree on disk.

ALTERNATIVES CONSIDERED and rejected. Giving the question a synthetic
`<job_id>:<task_id>` identity so the existing seam takes it unchanged — rejected
because it invents exactly the ids and the evidence file the actuals path exists
to refuse, and it would make a question indistinguishable from a task run in
every later query. Giving teacher spend its own table — rejected because D3
already rules that the separation IS the `role` column, and `query_cost(by=
"role")` would then answer a question that omits the teacher entirely.

CONSEQUENCE. `query_cost(by="role")` reports a `teacher` bucket beside the
mission roles with no change to that function. A NULL `task_id` now READS as
"not a task run"; every row that has one keeps its D16 meaning untouched.

Reverse this decision by deleting this section, deleting
`packages/orchestration/teacher_spend.py` and its test, and restoring the two
amended bullets of the `token_ledger` module docstring.

## DECISION F255 D8 — the teacher gets its OWN model transport, because no generic one exists (2026-08-21)

CONTEXT. T004 requires Stage 2 to answer through the teacher role's own model,
and the reviewer measured the provider surface at `2e5b8299` before assuming one
was available. `packages/providers/` holds `claude_agent`, `docker_runtime`,
`mempalace`, `ollama_builder` and `ollama_planner`; every one is role-specific.
The closest thing to a general call is `OllamaPlanner.raw_call`, and it is not
general in either direction: it takes a REQUIRED `schema` and passes it as
`format=`, and it resolves its model, host, temperature and num_predict from the
PLANNER's configuration surface. A teacher answer is prose, not a schema, and
borrowing the planner's configuration would make `teacher.model` decorative.

CHOSEN. Build one narrow transport owned by the teacher, in
`packages/orchestration/teacher_model.py`, behind an INJECTABLE seam: a `call`
parameter defaulting to `ollama_teacher_call`. The transport sends one free-text
chat with no schema, resolves its model through `resolve_role_config("teacher")`
and its host through the existing `ollama.host` config. `TEACHER_TRANSPORTS`
names the providers the teacher can call and holds `ollama` alone, because that
is the only one this round builds. Every test injects the seam, so the suite
never opens a socket and never needs a running Ollama.

ALTERNATIVES CONSIDERED and rejected. Calling `OllamaPlanner.raw_call` with a
permissive schema — rejected because it bills the teacher's question to the
planner's configuration and puts the planner's system prompt in front of a tutor
answer. Adding a generic completion provider under `packages/providers/` —
rejected as a strictly larger change than F255 needs, and one that would outlive
this feature's review; a future feature that needs it can lift this transport.
Refusing all Q&A until such a provider exists — rejected because it would leave
T004's acceptance unreachable and the seam R13 built still uncalled.

CONSEQUENCE. `teacher.model` becomes load-bearing for the first time. A provider
outside `TEACHER_TRANSPORTS` is refused honestly rather than mis-called, which is
the behaviour DECISION F255 D9 defines.

Reverse this decision by deleting this section, deleting
`packages/orchestration/teacher_model.py` and its test, and removing the
`teach.ask` handler and catalog entry.

## DECISION F255 D9 — Stage 2 refuses on NO USABLE TRANSPORT, not on "no model configured" (2026-08-21)

CONTEXT. The feature file's Edge cases say "With no model configured, Stage 2
refuses with an honest message and Stage 1 keeps working". Read against
`packages/orchestration/role_config.py` at `2e5b8299`, that state cannot occur:
`resolve_role_config` fills an unset model from `default_model_for_provider`, and
`DEFAULT_PROVIDER` is `ollama`, so EVERY role resolves to a model whether or not
anyone configured one. A test driving "no model configured" would therefore
assert a branch no configuration reaches — the vacuous gate this project keeps
paying for.

CHOSEN. Keep the honest refusal and re-point its CONDITION at something real.
Stage 2 refuses when the resolved provider is not in `TEACHER_TRANSPORTS`, when
that transport's dependency is absent, or when the call fails — and every refusal
names the provider and the model it refused for, so the operator can act on it.
`teacher_qa.no_model_refusal` keeps its job and its wording unchanged; only what
triggers it is corrected. Stage 1 keeps working, because Stage 1 is offline by
construction, and the refusal says so.

ALTERNATIVES CONSIDERED and rejected. Adding a sentinel "unconfigured" model so
the spec's literal words become reachable — rejected because it invents a state
to satisfy a sentence, and every other role would inherit it. Refusing whenever
`teacher.model` is absent from the config file — rejected because it would refuse
the default configuration that works, which is the opposite of honest.

CONSEQUENCE. A REFUSAL IS NEVER BILLED: no model was called, so no ledger row is
written, and a row claiming one would be the fabrication `token_ledger` refuses.
The feature file records this supersession beside its earlier three.

Reverse this decision by deleting this section and restoring the Edge-cases
sentence as the implemented condition.

## DECISION F255 D10 — `teach.ask` declares write_metadata, and its read-only proof names the ledger (2026-08-21)

CONTEXT. The Scope block lists "Hard invariants: ActionClass read_only", and
`teach.narrate` earns that declaration with the behavioural proof DECISION F255
D4 required. But DECISION F255 D3 requires Stage 2 to record teacher spend and
DECISION F255 D7 shapes that row, so `teach ask` writes
`<data_root>/projects/<project_id>/ledger.sqlite` and its sqlite sidecars. A
`read_only` declaration on that command would be false, and DECISION F255 D4
exists precisely because a declaration proves nothing while a false one misleads
the permission layer that reads the catalog.

CHOSEN. `teach.ask` declares `action_class="write_metadata"`, the class the
catalog already uses for commands that write Remedy's own records and not the
user's repository. `teach.narrate` keeps `read_only` unchanged. The invariant the
Scope actually means — never influencing the RUN — is proven for ask the same
behavioural way it was proven for narrate, with the ledger file and its sidecars
EXCLUDED BY EXPLICIT NAME and the exclusion itself asserted, so any other write
still fails the test.

ALTERNATIVES CONSIDERED and rejected. Declaring `read_only` and arguing the
ledger is not part of the run — rejected because the catalog's classes describe
what a command WRITES, not what it means to write, and a permission layer cannot
read intent. Moving the ledger write out of the command into a later batch —
rejected because it would separate the cost from the question that incurred it
and reintroduce the uncalled seam this round exists to close.

CONSEQUENCE. The teacher group now holds one `read_only` command and one
`write_metadata` command, and F255's read-only claim is stated where it is true
rather than everywhere.

Reverse this decision by deleting this section and changing the `teach.ask`
entry's `action_class` back to `read_only`.

## DECISION F008 D1 — the server becomes threaded in its own round before T001, and seq is the ledger position (2026-08-21)

CONTEXT. The feature file's Orchestrator brief dispatches T001's
server-capability question as a findings order before anything is built, and
R3 discharged it by measuring the source at `da2aabf9` rather than reading the
feature file's own prediction. Both predictions were false, and finding R-0612
records the measurement: `packages/orchestration/ui_server.py` instantiates
`http.server.HTTPServer` bare with no threading mixin anywhere under
`packages/` or `apps/`, so it serves one request at a time; and `LedgerEvent`
carries none of a seq, an index or any ordered field, its enumeration position
being spent inside `_make_event_id` and discarded. T001 as sliced assumed the
opposite of both.

CHOSEN. Two rulings, one for each measurement.

1. Making the UI server threaded is a PREREQUISITE ROUND before T001, not a
   step inside it. It is production code on the single path every existing
   cockpit feature already uses, so it carries its own commit, its own
   behavioural test — a slow request must stop blocking a concurrent one, an
   assertion that fails today — and its own gate over the state-reader four
   and the dashboard contract, which are the suites that would show a
   regression there.
2. The stream EXPOSES the ledger's own position as `seq` and assigns nothing.
   T001 adds the position to the read path rather than minting a parallel
   counter, so "the stream must not renumber" is satisfied by construction
   instead of by discipline, and `event_id` keeps its present meaning as an
   opaque digest rather than being pressed into service as an ordinal.

ALTERNATIVES CONSIDERED and rejected. Folding the threading change into T001 —
rejected because a blocking-server fix and a new endpoint would land in one
diff, and a regression in either could not be attributed to the right half.
Serving the stream from a second, separate threaded server on its own port —
rejected because it doubles the auth surface the token model has to cover and
splits the cockpit across two origins for no gain the first option does not
give. Persisting a new `seq` field onto every ledger event — rejected because
it rewrites the ledger format, which this feature's Do-not-touch section
excludes by name, and because the position it would persist is the one already
available for free. Deriving order from `timestamp` — rejected because
timestamps are strings of unspecified resolution here and two events can share
one, which is precisely the gap-detection failure T002 must prove absent.

CONSEQUENCE. T001 is preceded by one prerequisite round, so the feature is one
round longer than its Task slicing implies; the feature file's "How it fits"
section now states measured facts where it stated predictions; and the
Do-not-touch line on the ledger format is preserved rather than negotiated.

Reverse this decision by deleting this section, restoring the two predictions
in `docs/roadmap/features/T5_F008.md` and resolving R-0612 as rejected.


## DECISION F008 D2 — the delayed badge is a pill VARIANT, and the endpoint wiring is its own round (2026-08-21)

CHOSEN, two rulings the R29 block depends on.
1. DELAYED and RECONNECTING are VARIANTS of the existing `LiveStatusPill`, not
   a new visual language, so no assumption_log entry is owed. The design
   reference already gives this component variants — `component_spec.md` reads
   "LiveStatusPill (exists) — pulse dot; REPLAY variant (violet) for scrub
   state" — so a label swap plus an accent dot is the mechanism it documents.
   The accent `--remedy-orange-400` already exists in
   `apps/ui/src/styles/tokens.css` and in the reference's own `tokens.css`; no
   token, font, icon, glyph or asset source is added, leaving `assets_spec.md`
   untouched.
2. R29 ships the badge and R30 the wiring, where R28's handback proposed one
   round for both. `BrainStreamHostDeps` needs four real adapters —
   `openSource`, `readSnapshotSeq`, `readTail`, `schedule` — over the endpoint
   T001 and T002 built, and owes its own vitest tests. Bundling them would put
   a new transport adapter and a new visual surface in one diff, where a
   regression could not be attributed to the right half.

ALTERNATIVES REJECTED. An assumption_log entry anyway — no such file exists
here, so it would CREATE the register rather than append to it. A fourth
`BrainStreamStatus` member — rejected at R19, and R-0624 records why. A
REQUIRED `streamStatus` — `RemedyApp` holds none until R30, so it would force
callers to invent one.

CONSEQUENCE. The badge is reachable and gated at R29 while nothing yet supplies
a live value, which the pill's WHY comment states where a reader would look for
the absence. R30 then changes one prop at one call site.

Reverse ruling 1 by writing that assumption_log entry and citing this section
as the reading it overrides; ruling 2 by folding R30 back into one round.

## DECISION F008 D3 — the cockpit subscribes in RemedyShell, not RemedyApp

Chosen: `useBrainStream` is called in `RemedyShell` with `dashboard.jobId`.

Alternatives considered. (a) Call it in `RemedyApp`, as `.agent/plan.md` said
from R30 until this round. `RemedyApp` reads its job id from the URL and returns
an error screen when that id is empty, but a React hook cannot be called
conditionally, so the stream would open against `/api/jobs//events/stream`
whenever the URL carried no job — a request the server answers 404 and a
reconnect loop the badge would then report. (b) Pass the id down and subscribe
lower still, in `RightLivePanel`: rejected because the panel is a presentation
surface and the status already reaches it as a prop.

`RemedyShell` renders only after `RemedyApp` has loaded a dashboard, so
`dashboard.jobId` is a job the server has already answered for. The seam
`RightLivePanel` gained at R29 — an optional `streamStatus` — is unchanged by
this choice, and `RemedyApp.tsx` is not touched at all, which is the narrowest
blast radius of the three.

The feature file names no call site, so this decides an implementation question
rather than amending a spec. Reverse it by moving the call and passing the id
down; nothing else in the client depends on where the hook is called.

## DECISION F009 D1 — the command-channel contract test lives in `tests/ui_server/` (2026-08-21)

The feature file's Do not touch section named `tests/ui_contract/test_command_channel.py`. Measured at R2: that directory does not exist. Two candidates do — `tests/ui_contracts/`, whose modules are Python files asserting over React `.tsx` SOURCE, and `tests/ui_server/`, which holds every HTTP route contract this server has, including `test_sse_stream.py` and `test_auth_redaction.py`.

CHOSEN: `tests/ui_server/test_command_channel.py`. The surface under test is an HTTP route on `_RemedyHandler`, which is what every module in that directory already tests, and AGENTS.md's discoverability rules ask for one spelling per concept and a test file named after the source it covers.

ALTERNATIVES: (a) create `tests/ui_contract/` as the feature file names it — rejected, it would be a third directory one character from an existing one, which is precisely the synonym drift those rules forbid. (b) `tests/ui_contracts/` — rejected, its subject is component source, not server behaviour.

REVERSE by moving the file and restoring the feature-file line; C4 of this round is the amendment and it is a two-line pair.

## DECISION F009 D2 — POST authenticates by bearer plus CSRF, and the GET routes keep their query token (2026-08-21)

Measured at R2: the only authentication is a query-string token compared inside `do_GET`, the React client appends that token as a query parameter, and no bearer or CSRF handling exists anywhere in the server or the client.

CHOSEN: the new POST route requires `Authorization: Bearer <token>` AND an `X-Remedy-CSRF` header double-submitted against the served app; the existing GET routes keep the query parameter unchanged in this feature. Two token transports therefore coexist deliberately, and the code says so where a reader would search.

WHY THE GET HALF DOES NOT MIGRATE, and this is a technical constraint rather than a scope preference: the cockpit consumes the event stream through the browser `EventSource` API, which cannot set request headers at all. A bearer-only server would make the F008 stream unauthenticatable. The query token is what a stream can carry, and a header is what a write must carry so it cannot be replayed out of a URL, a referrer or a shell history.

ALTERNATIVES: (a) migrate every route to bearer — rejected on the EventSource constraint above. (b) accept the query token on POST too — rejected: it puts a mutating credential in URLs and defeats the CSRF pair's purpose.

REVERSE by deleting the two header checks and reading the query token in the POST path; nothing else depends on the choice.

## DECISION F009 D3 — the token comparison becomes constant-time, for both doors, inside this feature (2026-08-21)

Measured at R2: the comparison is a plain `!=` and `secrets.compare_digest` occurs zero times in the module.

CHOSEN: T001 replaces that comparison with `secrets.compare_digest` for the existing GET check AND the new POST check. This is the one line this feature changes outside its own new surface, and it is declared here rather than discovered in review.

WHY IT IS IN SCOPE: the feature's own Acceptance requires that unauthenticated attempts fail closed. Putting a write door behind a token whose comparison leaks its prefix in timing, while leaving the weaker half untouched because it predates the feature, would be shipping a knowingly weaker guard on the same secret. The change is two lines and the `tests/ui_server/` suite already covers both paths.

ALTERNATIVES: (a) leave it and register a finding — rejected, a finding routes work to a paydown branch that has no scheduled round, and this feature is the reason it now matters. (b) constant-time on POST only — rejected, both doors accept the same secret.

REVERSE by restoring `!=`; the behaviour is identical for every non-attacker input.

## DECISION F009 D4 — the exposed subset is catalog ids, declared beside the catalog (2026-08-21)

Measured at R2: the catalog is `apps/cli/command_catalog.py` with 340 entries over 60 groups, no UI-exposed subset exists as a declared thing, and the UI server never imports the catalog. Measured by the reviewer at R3: the three commands the feature file names map onto only TWO `command_id` values — `job.stop` and `decision.resolve` — because plan approval has no id of its own and reaches the CLI as a `fp:`-prefixed decision id routed inside `decision.resolve`.

CHOSEN: a `UI_EXPOSED_COMMANDS` frozenset of `command_id` values declared in `apps/cli/command_catalog.py` beside `CATALOG`, holding `job.stop` and `decision.resolve`. The API's `command` field IS a catalog `command_id`; plan approval reaches the channel as `decision.resolve` carrying a `decision_id` argument with the `fp:` prefix, exactly as the CLI spells it. The endpoint imports that set, which is the single source the feature file's How-it-fits section requires.

ALTERNATIVES: (a) invent a third API command name for plan approval — rejected, it would be a second spelling for one concept and the prefix routing would still have to exist underneath. (b) declare the subset in the server — rejected, it separates the subset from the catalog it constrains.

REVERSE by deleting the frozenset and inlining the two ids at the endpoint.

## DECISION F009 D5 — the effect table, and the plan-approval extraction lands as its own commit (2026-08-21)

Measured at R2: `safe_points.request_stop` is an importable package function with no CLI coupling; `escalation.answer_task_decision` is likewise importable and does not persist, its CLI caller invoking `save_job` afterwards; the plan approval is inline CLI code that mutates the flight plan, calls `save_job`, writes an assumptions log and prints; and `decision_queue.py` is a read-only aggregation with no write target at all.

CHOSEN: stop maps to `request_stop`. A decision answer maps to `answer_task_decision` followed by `save_job`. Plan approval maps to a NEW package-level function extracted from `apps/cli/commands/decision.py`, keeping the CLI as its first caller so the extraction is provably behaviour-preserving; the printing stays in the CLI and does not move into the package. That extraction is a refactor, so per AGENTS.md it is ITS OWN COMMIT and lands before any endpoint code calls it.

WHAT "QUEUE-ONLY SIDE EFFECTS" MEANS HERE, since the feature file's phrase does not resolve against the source: the handler may import exactly the three effect functions plus the audit writer, and nothing that opens a file, spawns a process or writes storage directly. The import guard asserts that set, and the per-command tests assert that the effect function was called and that no other file under the job's tree changed.

ALTERNATIVES: (a) duplicate the approval guard sequence in the handler — rejected, it is the coupling the P3 contract exists to prevent and it would drift from the CLI. (b) build a real queue for decision answers to enqueue into — rejected as this feature's work; nothing consumes such a queue today and inventing one would widen F009 into the machinery it is supposed to reuse.

REVERSE by re-inlining the extracted function into the CLI command.

## DECISION F009 D6 — the audit record: per-job, private, append-only, and its fields are fixed here (2026-08-21)

Measured at R2: `commands_audit.jsonl` exists nowhere, while `docs/roadmap/features/T5_F035.md` and `docs/roadmap/features/T9_F167.md` already plan to READ it. Two later features therefore depend on this choice, which is why it is ruled now rather than at T002.

CHOSEN: `commands_audit.jsonl` in the per-job control directory `job_control_dir(job_id)` — the private 0o700 directory `safe_points` already owns — written through `packages.common.secure_fs` with the 0o600 file mode that directory's other files use. One JSON object per line, append-only, never rewritten. Fields, in this order: `ts`, `token_fp`, `command`, `args_hash`, `nonce`, `outcome`.

EVERY ATTEMPT IS AUDITED, not only accepted ones: the feature's Acceptance requires wrong or missing auth to be audited as rejected, so `outcome` carries the rejection reason and a rejected attempt writes a record before the response is sent.

ALTERNATIVES: (a) the evidence export directory — rejected, it is packaged into review zips and an audit log carrying token fingerprints does not belong in a shareable artefact. (b) the run log — rejected, it is per RUN and keyed to a run id, while this record is per JOB and must survive across runs.

REVERSE by changing the path helper; the field set is the half two other features depend on and should be changed only with them.

## DECISION F009 D7 — the token fingerprint is a truncated digest, and rotation deliberately changes it (2026-08-21)

The feature file asks for fingerprints "stable per token id, not raw tokens". Measured at R2: there is no token-id concept in this repository — `start_ui_server` mints a token per run with `secrets.token_urlsafe(24)` — so "token id" has no referent and is read here as the token VALUE.

CHOSEN: `token_fp` is `"tf:" + sha256(token.encode()).hexdigest()[:16]`. It never carries the raw value, which the redaction denylist in `packages/orchestration/stream_evidence.py` forbids writing at all.

ROTATION CHANGES THE FINGERPRINT, and that is the intended reading rather than a limitation: the audit answers which credential acted, not which human, and a rotated token is a different credential. A record that survived rotation would be claiming an identity this system does not model.

ALTERNATIVES: (a) a random per-token id stored beside the token — rejected, it adds a persisted mapping for no gain. (b) the full digest — rejected, sixteen hex characters distinguish every token a job will ever see and keep the line readable.

REVERSE by changing the helper; the field name does not change.

## DECISION F009 D8 — the nonce store is one create-only file per nonce, and the window is the job (2026-08-21)

Measured at R2: no nonce, replay-window or deduplication machinery exists; the run log is append-only and per run, so it cannot return a body; and the closest in-repo precedent is `request_stop`, which publishes create-only so a race converges on one record.

CHOSEN: `commands_nonce/<nonce>.json` inside the same per-job control directory, one file per nonce, holding the response body that was returned. Publication is CREATE-ONLY through the same `secure_fs` path `request_stop` uses: the loser of a race reads the winner's file and returns the SAME body, which is exactly the "a seen nonce returns the ORIGINAL result, idempotent, not an error" contract the feature file states. The replay window is the JOB's lifetime — the directory dies with the job — rather than a duration.

ALTERNATIVES: (a) a time-bounded window with a sweeper — rejected, it adds a background concern and a clock dependency to buy an expiry nobody has asked for. (b) a single map file — rejected, concurrent writers would have to lock it, where one file per nonce gets atomicity from the filesystem, which is the precedent that already works here.

The nonce is a client-supplied string and becomes a PATH component, so it is validated against a strict character class and a length bound before it is used, the way `validate_job_id` guards the job segment of the same directory. A nonce that fails validation is a typed 4xx and is audited as rejected.

REVERSE by replacing the directory with another store; the endpoint contract does not change.

## DECISION F009 D9 — the rate limit is a typed config key, per token and job (2026-08-21)

The feature file says "rate limit per token+job (config)" without naming a config source. Measured at R2: the only limiter is `packages/orchestration/rate_governor.py`, which is OUTBOUND and per provider and inherits nothing here, and the only inbound precedent is the hard-coded `SSE_MAX_STREAMS_PER_JOB`. Measured by the reviewer at R3: `packages/orchestration/config.py` is a typed system with `ConfigKeySpec`, env-over-TOML-over-default precedence and a `get_config()` accessor, so "config" resolves to it.

CHOSEN: a `ConfigKeySpec` declaring the maximum accepted commands per token fingerprint and job per minute, with a built-in default, resolved through `get_config()`. The key is the pair `(token_fp, job_id)`. Exceeding it REFUSES with a typed 429 and audits the attempt as rejected — it does not wait, which is what the outbound governor does and would be wrong for an inbound request holding a connection.

ALTERNATIVES: (a) a module constant like the SSE cap — rejected, the feature file says config and a typed key costs one spec entry. (b) reuse `ProviderRateGovernor` — rejected, it is keyed by provider, it waits rather than refuses, and its own docstring states it neither coordinates across processes nor orders acquirers fairly.

REVERSE by deleting the key spec and reading a module constant.

## DECISION F009 D10 — an open-finding count is stated with the rule that produced it, or not at all (2026-08-21)

Finding R-0632 records that "N findings are open" carries at least three live meanings in this repository — every registered paragraph not answered by a `Done:` line, the small set of findings the current feature must still act on, and the raw registered total — and that three authored texts in the F009 session each stated a different number without naming which they meant.

CHOSEN: the open set is the one `docs/agents/planner_reviewer_prompt.md` §3 item 10 already defines — every line-anchored `^- R-\d+ — ` paragraph minus every line-anchored `^Done: R-\d+ — ` line — and a state file that states a count states BOTH the rule and the commit it was measured at, in the same sentence. Measured at `ab6eeba1` that count is 196. A narrower set may still be stated and is often the useful one, but it is named as what it is — "the findings this feature must still act on" — and never called "open" unqualified.

ALTERNATIVES: (a) add a trailing `OPEN.` marker to every unresolved paragraph and count that — rejected, it would require editing 105 landed paragraphs in an append-only record, which §3 item 20 forbids outright, and the reviewer measured that the marker is currently decoration: 92 of 197 paragraphs carry it while 6 of the 7 ids the F008 closure called open do not. (b) stop stating the number anywhere — rejected, it is genuinely useful in a handback, and item 10 already requires the set to be recomputed at every emission, so the derivation costs nothing beyond naming it.

WHY NO SWEEP: the landed sentences are not rewritten. `.agent/context.md` and `.agent/handoff.md` are rewritten wholesale every round and will carry the ruled form from the next rewrite onward; `.agent/live_review.md` is append-only and is corrected by dating rather than editing.

REVERSE by deleting this decision and R-0632's fix clause; nothing depends on the count.

## DECISION F009 D11 — the `X-Remedy-CSRF` header carries the server token (2026-08-21)

D2 ruled that the POST door requires `Authorization: Bearer <token>` AND an `X-Remedy-CSRF` header "double-submitted against the served app", without fixing what value that header carries. There is no cookie to double-submit against: the shell at `/` is served without a token and the React client reads the token from the URL query — `apps/ui/src/RemedyApp.tsx` line 10 at `b6d80e8e` — so the only secret the app holds is the server token itself.

CHOSEN: `X-Remedy-CSRF` carries that same server token, compared constant-time as bytes by the same helper the bearer check uses. A cross-site page cannot set a custom header on a cross-origin request without a preflight this server never grants, so the header's PRESENCE is what defeats CSRF; requiring its VALUE additionally makes the door fail closed on a half-wired client instead of silently accepting one.

ALTERNATIVES: (a) accept any non-empty `X-Remedy-CSRF` — rejected, it makes a wiring bug indistinguishable from a working client. (b) mint a separate CSRF secret and embed it in the shell — rejected for this feature: it adds a second secret to serve, rotate and redact, against no attacker the first one does not already stop, and the shell embeds the token by plain string substitution today.

REVERSE by dropping the value comparison and checking only that the header is present; nothing else about the route changes.

## DECISION F009 D12 — a command outside the exposed subset is a typed 400 on the `command` field (2026-08-21)

D4 ruled the exposed subset a `UI_EXPOSED_COMMANDS` frozenset of catalog `command_id` values and ruled that the endpoint imports it, without fixing what the door answers when a well-formed request names an id outside it. The door already has two refusal vocabularies at `98592b72`: 403 with `{"error": ...}` for a credential that fails, and 400 with `{"error": ..., "field": ...}` for a request whose shape is wrong.

CHOSEN: an unexposed `command_id` is 400 with `field` set to `command`, reusing the shape D.4 of the R6 contract established. It is a statement about the request the client sent, and the field it must change to send a different one is `command`.

ALTERNATIVES: (a) 403 — rejected, it means "your credential failed" on this door, and a client that retried authentication on a policy refusal would be chasing the wrong repair. (b) 404 — rejected, a command id is not a resource this API exposes at a URL, and a 404 on the commands path already means the JOB did not resolve. (c) a distinct 422 — rejected, it adds a third vocabulary for a case the second already covers.

THE REFUSAL DELIBERATELY DOES NOT DISTINGUISH an id that is absent from the catalog entirely from one that exists but is not UI-exposed. Both are "not a command this door accepts", and separating them would let an unauthenticated-but-credentialed caller enumerate the CLI surface through the write door.

REVERSE by giving the unexposed case its own status; the field name does not change.

## DECISION F009 D13 — the rate limit is consulted only for a request that would otherwise be accepted (2026-08-21)

D9 ruled the limit a typed `ConfigKeySpec` keyed by the pair (token fingerprint, job id) and ruled that exceeding it refuses with 429, without fixing WHERE in the door's decision order the limit is consulted. That position is observable, so it is ruled rather than left to the implementation. The door's order at `43b438e3` is credentials, then job resolution, then request shape, then the UI-exposed subset, then the seam.

CHOSEN: the limit is consulted LAST, immediately before the seam, and only a request that passes every earlier check spends budget. D9's own words are "the maximum accepted commands", and this is the reading that makes them true.

WHY IT IS NOT CONSULTED EARLIER, which is the tempting alternative because an early check is cheaper: budget is spent per token fingerprint, and a client that is mid-rollout or simply buggy would otherwise lock ITSELF out of a job by sending malformed bodies — a self-inflicted denial of service produced by the guard rather than prevented by it. The cheapness argument does not survive contact with the threat model either: the fingerprint is derived from the server token, so anyone able to spend budget at all already holds the credential that grants full read access and every write this door exposes. The limit exists to bound the RATE of accepted change, not to defend the parser.

ALTERNATIVES: (a) consult it immediately after the credentials — rejected on the self-lockout argument above. (b) count every request that reaches the door regardless of outcome — rejected for the same reason, and it would make the 429 depend on traffic the client cannot see.

CONSEQUENCE FOR D6, stated here so the audit round does not have to rediscover it: a 429 is a REJECTION and is audited as one, and because the limit sits last, an audited 429 always names a command that was well formed and UI-exposed.

REVERSE by moving the call earlier in `_handle_command_submission`; the key, the window and the status do not change.

## DECISION F009 D14 — what an audited attempt requires, and the three fields D6 left unfixed (2026-08-21)

D6 ruled the audit record's path, its mode, its append-only shape and its field ORDER — `ts`, `token_fp`, `command`, `args_hash`, `nonce`, `outcome` — and ruled that every attempt is audited rather than only accepted ones. Building it surfaced three halves that ruling does not fix and one ordering hazard it cannot have foreseen, and two later features already plan to READ this file, so they are ruled here rather than left to the implementation.

FIRST, WHICH ATTEMPTS REACH A RECORD AT ALL. Read at `f7f43edf`, and the round that carries this decision changes neither half: `_handle_command_submission` decides credentials BEFORE it resolves the job, deliberately, so an unauthenticated caller never learns which jobs exist. A record is per job and lives in `job_control_dir(job_id)`, so auditing a refusal that happened before the job resolved means reaching that directory on behalf of a caller who has presented nothing. CHOSEN: an attempt whose bearer or CSRF check failed is audited ONLY into a job control directory that ALREADY EXISTS, opened with `create=False`, and writes nothing at all when it does not; an attempt that has passed both credential checks is audited with `create=True`. The check ORDER does not change and neither does any status code. ALTERNATIVES: (a) resolve the job before the credentials so every rejection can be audited — rejected, it hands an unauthenticated caller a job-existence oracle through the 404-versus-403 split, which is the property the current order exists to protect. (b) audit pre-credential refusals with `create=True` — rejected, it lets an unauthenticated caller create an arbitrary control directory per request, which is litter an attacker steers and a resource this door must not spend on a caller it has already refused. The cost is stated plainly rather than hidden: a wrong-credential attempt against a job that has never had a control directory leaves no record, and the Acceptance line "wrong or missing auth is audited as rejected" is met for every job the cockpit has actually operated on and not for one it has not.

SECOND, THE `args_hash` FORMAT. CHOSEN: `"ah:" + sha256(secure_fs.json_bytes(args)).hexdigest()[:16]`, the prefix matching `token_fp`'s `tf:` so a reader can tell the two digests apart on a line, and `json_bytes` because it already sorts keys, which is what makes the hash stable across two clients that spell the same object in different orders. The raw `args` are NEVER written: they are client-supplied and may name paths or ids that the redaction denylist would have to reason about, and the hash answers the only question this record needs to answer, which is whether two attempts carried the same arguments.

THIRD, THE `outcome` VOCABULARY, which is the field the two reading features consume. CHOSEN: a closed set of lowercase tokens — `rejected_token`, `rejected_csrf`, `rejected_job`, `rejected_shape`, `rejected_command`, `rejected_rate`, and `not_implemented` for the 501 that the seam at the end of that same function answers at `f7f43edf`. `accepted` is reserved and is written by the round that retires the seam, because nothing is accepted while a 501 stands and a record claiming otherwise would be false. Every token names the CHECK that refused, never the client's message, so the vocabulary cannot drift with a wording change.

FOURTH, WHAT A FAILED AUDIT WRITE DOES. CHOSEN: for a REJECTION it changes nothing — the refusal the door had already decided is sent unchanged, and the exception is swallowed at the call site rather than propagating, because turning a 403 into a 500 would let a full disk convert a correctly-refused attempt into a server fault. The accepted case is deliberately NOT ruled here: nothing is accepted until the seam is retired, and whether a command may take effect when its audit record cannot be written is a question about effects, which the round that lands the effect table answers with the effects in front of it.

REVERSE by deleting the audit call sites; the record's path, mode and field order come from D6 and are unchanged by this decision.

## DECISION F009 D15 — the nonce record is published only by an accepted command, and a replay spends no rate budget (2026-08-22)

D8 ruled the nonce store's shape — `commands_nonce/<nonce>.json` in the job's control directory, one create-only file per nonce holding the response body that was returned, the replay window being the job's lifetime. It did not fix WHEN a record is published or WHERE the lookup sits in the door's decision order, and both are observable, so both are ruled here rather than left to the implementation.

FIRST, WHAT MAY PUBLISH. Read at `db50d0bb`, the door's last act is a 501 seam: `_handle_command_submission` authenticates, resolves, validates, checks the exposed subset and the rate limit, and then answers 501 because DECISION F009 D5's effect table does not exist yet. CHOSEN: a nonce record is published ONLY for a command that was ACCEPTED, so while the seam stands nothing publishes at the door at all, and the publish call site lands in the round that retires the seam — the same round that writes D14's reserved `accepted` audit outcome. ALTERNATIVES: (a) publish the 501 body under the nonce, so the store is exercised end to end now — rejected, and this is the whole reason the decision exists: D8's contract is that a seen nonce returns the ORIGINAL result, so a published 501 would be returned for that nonce forever, freezing a transient seam into a permanent answer for the one client that retried during it, and the bug would outlive the seam by the lifetime of the job. (b) publish at the seam but expire such records when the seam retires — rejected, it buys nothing and adds a migration to a store whose whole appeal is that it has none. THE COST IS STATED: until T003 the door's lookup can only miss, so its tests seed the store through this module's own publish function, which is production code exercised by production means rather than a test-only path.

SECOND, WHERE THE LOOKUP SITS AND WHAT IT SPENDS. CHOSEN: the lookup runs after the UI-exposed subset check and BEFORE the rate limit, and a replay that hits returns the stored body while spending NO budget. WHY NOT AFTER THE LIMIT, which would be the simpler insertion: D9's own words are "the maximum accepted commands", and a replay accepts nothing new — it returns a decision the server already made. Charging it would penalise a client for the server's own idempotency guarantee, and the client that retries after a network timeout is precisely the case a nonce exists to serve, so a limit that punished it would break the contract it sits next to. ALTERNATIVES: (a) charge a replay like any request — rejected on the argument above. (b) place the lookup first, before the credentials — rejected outright, it would answer an unauthenticated caller out of the store and turn the nonce into an oracle for other clients' responses.

THIRD, THE NONCE'S CHARACTER CLASS. It becomes a FILENAME, so it is validated before it is used: CHOSEN, `safe_points.is_safe_id`, the same `_ID_RE` that already guards the job segment of the same directory, checked in `_read_command_payload` beside the existing non-empty check. A nonce that fails it is the 400 on field `client_nonce` that shape errors already produce and is audited `rejected_shape` — so D14's closed outcome vocabulary is UNCHANGED and gains no token.

REVERSE by moving the publish call and the lookup; the store's path, shape and window come from D8 and are unchanged by this decision.

## DECISION F009 D16 — T003 lands in four rounds and the 501 seam retires one command at a time (2026-08-22)

Measured at `1e7539be`: `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` holds exactly TWO ids, `job.stop` and `decision.resolve` — not the three effects DECISION F009 D5's table names. The plan approval is not a third id: it arrives as `decision.resolve` carrying an `fp:`-prefixed `decision_id`, which is the same dispatch `_cmd_decision_resolve` already performs in the CLI, and that command's catalog args are `job_id`, `decision_id`, `--reason`, `--answer` and `--as-mission`. `resolve_flight_plan_approval` landed in `packages/orchestration/flight_plan.py` at `c204f0b5`, so all three effect functions D5 names now exist as importable package functions.

CHOSEN: the rest of T003 lands in FOUR rounds, and the 501 seam retires PER COMMAND rather than in one step. FIRST, `job.stop` dispatches to `safe_points.request_stop`; that same round writes D14's reserved `accepted` outcome, adds the `publish_nonce_result` call site with R-0637's bound applied AT PUBLICATION, moves R-0636's replay audit token off `not_implemented`, and ships the tests for that id's effect. `decision.resolve` keeps answering 501 and keeps auditing `not_implemented` through that round, which stays the honest token for a command this door has not yet dispatched. SECOND, `decision.resolve` dispatches — a task decision to `escalation.answer_task_decision` followed by `save_job`, an `fp:`-prefixed id to `resolve_flight_plan_approval` — and the seam is gone when that round ends. THIRD, the `command.accepted` SSE event. FOURTH, the queue-only import guard, the per-command side-effect assertions and the route-walking 405 test. Then the integration gate and closure.

WHY IT IS CUT THIS WAY, measured rather than estimated: DECISION F085 D6 caps a step block at 490 lines TOTAL and AGENTS.md DECISION F104 D1 caps a commit at 500 insertions. The dispatch, the publication, the two finding fixes, the accepted-event emission and the tests for all of it do not fit one block, and a block that does not fit is not delivered — it becomes a declared deviation on a round that did nothing wrong. Splitting by COMMAND rather than by LAYER keeps every round independently testable end to end: each retires the seam for one id and ships the tests that prove that id's effect, instead of landing a half-wired mechanism no test can reach.

WHY R-0636 AND R-0637 ARE BOTH PAID IN THE FIRST OF THE FOUR: each is a one-line change that depends on the publish call site, and that is the round which introduces it. Their fix clauses in `.agent/live_review.md` already say so; deferring either would leave a published record unbounded for a round and buy nothing.

ALTERNATIVES: (a) one round for all of T003 — rejected on the two caps above, which are measurements and not preferences. (b) split by LAYER, a dispatch module first and the wiring second — rejected because D5 rules that the handler imports the effect functions directly and that the import guard asserts exactly that set, so an intermediate dispatch module would change the very property the guard exists to assert. (c) retire the seam for both ids at once and defer only the tests — rejected outright: it would leave an accepting-but-unproven door on disk between two rounds, which is the one state this feature's Acceptance exists to make impossible.

REVERSE by collapsing the remaining rounds back into a single block, which is possible only if both caps change; the effect mapping itself comes from D5 and is unchanged by this decision.

## DECISION F009 D17 — D16's first round splits in two, and the audit vocabulary lands a round before its writer (2026-08-22)

Measured at `de1e5c00` by the reviewer, before this round was delegated: retiring the 501 seam for `job.stop` alone moves far more than the door. `tests/ui_server/test_command_channel.py` mentions the literal `501` on 21 lines, and its `_post_command` helper submits `job.stop` by default — `test_the_seam_is_audited_as_not_implemented` asserts exactly that — so roughly seventeen pinned sites change status the moment that one id dispatches, including `test_every_exposed_command_reaches_the_seam`, which loops over both exposed ids and must split because after that round one of them dispatches and the other still answers 501. Two further pins sit outside that file: `tests/orchestration/test_command_audit.py` fixes `OUTCOMES` as an exact tuple and separately asserts `"accepted" not in OUTCOMES`.

CHOSEN: DECISION F009 D16's FIRST round becomes two, so D16's four become five and nothing else in its ordering changes. Round one — this one — lands only what the dispatch DEPENDS on, with no door edit at all: the nonce store's publication bound, which pays R-0637, and the `accepted` and `replayed` tokens in `command_audit.OUTCOMES` with the pin that fixes them. Round two edits `packages/orchestration/ui_server.py`, migrates the seam pins in `tests/ui_server/test_command_channel.py` and pays R-0636. Rounds three, four and five are D16's second, third and fourth unchanged.

WHY, measured rather than estimated: DECISION F085 D6 caps a step block at 490 lines TOTAL. The dispatch, the publication call site, the two finding fixes and roughly seventeen test-pin migrations do not fit in one, and D16 itself rules that a block which does not fit is not delivered — it becomes a declared deviation on a round that did nothing wrong. The cut also keeps D16's own criterion intact: each round is independently testable end to end. This one ships two package functions with their own tests and leaves the door provably unchanged, which is a stronger property than a half-wired dispatch, not a weaker one.

WHY THE VOCABULARY MOVES EARLY, and why that is not a claim about behaviour. `accepted` and `replayed` enter the closed set here while NO caller writes either, and the door's own guard — `tests/ui_server/test_command_channel.py` asserting that no record the door wrote carries `accepted` — stays TRUE and unedited, which is what keeps the gap visible rather than papered over. The reviewer ran that file against this change in a disposable worktree at the round base and it passed unmodified. Landing the vocabulary here buys round two a change set of one production file and one test file.

WHY R-0637 IS PAID HERE THOUGH ITS OWN FIX CLAUSE SAYS OTHERWISE. That clause reads "owed by the round that retires the seam, in the same commit that adds the publish call site". Paying it one round EARLIER is strictly stronger and not a deviation from its intent: the bound is in force BEFORE any door path can reach publication, so the window in which an unreplayable record could be written is never opened rather than merely closed on arrival. R-0636 does NOT move, because its fix genuinely depends on the door caller it names.

ALTERNATIVES: (a) keep D16's four rounds and let the first exceed the block cap — rejected on the cap, which is a measurement and not a preference. (b) split by LAYER instead, landing a dispatch module first — rejected for the same reason D16 rejected it: DECISION F009 D5 rules that the handler imports the effect functions directly and that the import guard asserts exactly that set. (c) migrate the seam pins in THIS round and dispatch in the next — rejected because a test pinning a status the door does not yet return is a test asserting a falsehood, and the suite would have to be red between the two rounds.

REVERSE by collapsing rounds one and two back into a single block, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5 and the round ordering from D16, and neither is altered here.

## DECISION F009 D18 — D17's round two splits again, and what an ACCEPTED command answers, audits and publishes (2026-08-22)

Measured by the reviewer at `e7c621fc`, before this round was delegated: DECISION F009 D17's round two does not fit. `tests/ui_server/test_command_channel.py` mentions the literal `501` on 21 lines and reaches the door through `_post_command`, whose body defaults to `job.stop`, so the dispatch moves most of those sites; `safe_points.request_stop` returns a `StopSignal` whose fields nothing has ever put on the wire; and D14 clause four ruled what a failed audit write does for a REJECTION while explicitly leaving the accepted case open. DECISION F085 D6 caps a step block at 490 lines TOTAL, and the FROM/TO pairs for those migrations plus a dispatch plus the tests for its effect do not fit inside one.

CHOSEN: D17's round two becomes two, so D16's five rounds become six and nothing else in its ordering changes. Round one — this one — touches no door: it rules the four questions below and lands the third vocabulary token they require. Round two edits `packages/orchestration/ui_server.py`, migrates the seam pins and pays R-0636. Rounds three onward are D16's second, third and fourth unchanged.

FIRST, WHAT AN ACCEPTED COMMAND ANSWERS. CHOSEN: status 200 with `{"command": <id>, "outcome": "accepted", ...}` plus the fields that command's own effect produces — for `job.stop`, `request_id` from the returned `StopSignal`. Each id in the exposed subset declares its own accepted body rather than sharing one envelope, because D5's three effects return three different things and a common shape would either drop what the caller needs or invent fields the effect never produced. The `outcome` field carries the same token the audit line carries, so a client and a later reader of `commands_audit.jsonl` describe the same event with the same word.

SECOND, THE ORDER OF THE THREE WRITES. CHOSEN: dispatch, then the `accepted` audit line, then the nonce publication. The effect runs first because the response body is not known until it returns; the audit line precedes the publication because the record of what the door did must not depend on a store the client controls the key of; and the publication is last because D8's contract is that a replay returns the ORIGINAL result, which does not exist until the other two have happened. ALTERNATIVE: audit `accepted` before dispatching — rejected, it writes a claim the effect may then falsify by raising.

THIRD, WHAT A FAILED WRITE DOES ON THE ACCEPTED PATH, which D14 clause four left open. CHOSEN: both later writes fail SOFT. A failed audit write changes nothing about the response, exactly as for a rejection, because the effect is already durable and refusing after the fact would report a stop that really was requested as not requested. A publication that returns None — which R-0637's bound now makes reachable — also changes nothing, and its stated cost is that a client retrying that nonce re-executes the command; that is tolerable only because every effect in D5's table is idempotent at its own layer, `request_stop` provably so, and the round that dispatches `decision.resolve` must re-examine this clause against that effect rather than inherit it.

FOURTH, A DISPATCH THAT RAISES. CHOSEN: a new closed-set token `rejected_effect`, audited with `create=True`, answered 500 through the existing safe-error path with no exception text on the wire. Without it a failed effect is either unaudited, which breaks D6's "every attempt is audited", or recorded as `accepted`, which is false; and T5_F035 and T9_F167 both read this file to count what the door did, so the distinction has to exist in the vocabulary rather than in a reader's inference. The token lands HERE, one round before its writer, for the reason D17 gave for `accepted` and `replayed`: it keeps the round that retires the seam to the door alone.

ALTERNATIVES for the split itself: (a) keep D17's round two whole and exceed the block cap — rejected on the cap, which is a measurement and not a preference. (b) migrate the seam pins in this round and dispatch in the next — rejected for the reason D17 already gave, that a test pinning a status the door does not yet return asserts a falsehood.

REVERSE by collapsing these two rounds back into one, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5, the round ordering from D16 and D17, and none of them is altered here.

## DECISION F009 D19 — the `job.stop` dispatch round splits in two, and the effect assertions get their own file (2026-08-22)

Measured by the reviewer at `6101ca20`, before this round was delegated, by counting the strings the migration must move in `tests/ui_server/test_command_channel.py`: `[0] == 501` occurs 9 times and every one of them submits `job.stop` through `_post_command`, so all 9 become 200; `assert status == 501` occurs 7 times, of which the `decision.resolve` case keeps the seam and the loop over both exposed ids must split; `"not_implemented"` occurs 5 times, of which one is the raising-writer test whose second seam call becomes a REPLAY rather than an acceptance, because both of its loops submit the SAME default nonce. Three of those are uniform byte-string transformations the block can order once each and count; the remainder need their own FROM/TO pairs, and the door's own dispatch, the effect assertions and the plan and ledger slices sit beside them. Summed as slices plus the prose a done-when list needs, that block exceeds the 490 lines DECISION F085 D6 caps a step block at.

CHOSEN: DECISION F009 D18's round two becomes two, so D16's six rounds become seven and nothing else in its ordering changes. ROUND ONE lands the door — `packages/orchestration/ui_server.py` dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order of effect, audit line, publication — pays R-0636 by moving the replay audit token to `replayed`, and migrates every seam pin that must move for the suite to stay green, including the three counted uniform transformations. That round is self-testing rather than half-wired: the audit test asserting the outcome `accepted` for a `job.stop` passes only if the door really dispatched, so D16's rule that no round leaves a mechanism no test can reach is met by the migration itself. ROUND TWO adds the dedicated effect assertions in a NEW file, `tests/ui_server/test_command_dispatch.py` — that the stop request the dispatch published exists and carries the door's source, that the nonce record holds the body the client received, and that a retry of the same nonce is audited `replayed` — which is purely additive and touches no existing test.

WHY THE CUT IS HERE AND NOT ELSEWHERE. A cut between the door and the pins was already rejected by D17 and is rejected again for the same reason: a test pinning a status the door does not yet return asserts a falsehood, and the suite would be red between the two rounds. A cut between the pins that MUST move and the assertions that MAY be added later has neither problem — the suite is green at every commit of both rounds, and the second round adds a file rather than editing one.

ALTERNATIVES: (a) keep D18's round two whole and exceed the block cap — rejected on the cap, which is a measurement and not a preference, and on D16's own rule that a block which does not fit is not delivered. (b) raise the 490-line cap instead of splitting — rejected here because the cap is DECISION F085 D6's and a cap change must be measured against every other artifact it crosses rather than lifted for the one round it inconveniences; the reviewer records instead that this feature has now split three times on that single constraint, which is a fact a later reader should weigh before the next feature is planned the same way.

REVERSE by collapsing these two rounds back into one, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5, the write order from D18, and the round ordering from D16, D17 and D18, and none of them is altered here.

## DECISION F009 D20 — what `job.stop`'s dispatch passes to `request_stop`, what a raised effect answers on the wire, and the MEASURED shape of the pin migration (2026-08-22)

FIRST, THE TWO ARGUMENTS THE CLIENT DOES NOT SUPPLY. `safe_points.request_stop(job_id, reason, source)` takes two values that no part of a command submission names. CHOSEN: `source` is a new constant `COMMAND_EFFECT_SOURCE` carrying the value `ui`, and `reason` is the `reason` member of `args` when it is a `str` and the empty string otherwise. The source is fixed rather than client-supplied because it is the field that tells a stop asked for through the UI apart from one asked for by `remedy job stop`, and a client that could set it could erase that distinction inside the archived signal itself. The reason DEGRADES rather than raising because `args` is client-supplied and DECISION F009 D14's shape check types the object but not its contents; `_bounded` in `safe_points` already truncates an over-long one, so the only case left to rule is a non-string, and answering 500 for it would turn a well-formed request into a server fault. ALTERNATIVE: reject a non-string reason as a 400 shape error — rejected because `args` is per-command and this door deliberately does not know any command's argument schema, which is the property DECISION F009 D5's import guard exists to keep.

SECOND, WHAT A RAISED EFFECT PUTS ON THE WIRE. DECISION F009 D18 clause four already ruled the token `rejected_effect`, the `create=True` audit and the status 500; it did not name the body. CHOSEN: a new constant `COMMAND_EFFECT_FAILED_MESSAGE` carrying the sentence "command could not be carried out", sent through the existing `_safe_error` path. The exception's own text never reaches the wire: it is written by code this door does not own and may name a control path the client has no business learning.

THIRD, THE MEASURED SHAPE OF THE PIN MIGRATION, which corrects this decision's predecessor. Finding R-0638 records that DECISION F009 D19 called three string migrations uniform when only one of them is. MEASURED at `aa1e2780`, first by reading every site and then by applying the R19 block's own slices to a throwaway tree: 14 FROM/TO pairs are applied FIRST, and only then do three ordered replacements run over what is left — `[0] == 501` to `[0] == 200` at 9 sites, `status == 501` to `status == 200` at 4, and the quoted `not_implemented` to the quoted `accepted` at 4. The two counts that differ from D19's are not a correction of its arithmetic but a consequence of the ordering: the pairs consume the sites whose destination differs, and that is precisely what leaves the remainder single-valued and the replacement safe. RULE, binding on every later round of this feature: a block may order a repository-wide string replacement only over a remainder it has first made single-valued, and the count it states must be one a dry run PRINTED rather than one a grep suggested.

REVERSE the first clause by making `source` client-supplied, which requires re-reading D14's shape check first; the second by pinning a different message, which no test outside this feature reads; the third only by finding a site the measurement missed, in which case that site is the correction and this paragraph is the record of how the count was taken.

## DECISION F009 D21 — the `decision.resolve` effect, D18 clause three re-examined, and a refusal that did not raise (2026-08-22)

Measured by the reviewer at `09d473d6`, before this round was delegated, by reading `packages/orchestration/escalation.py`, `apps/cli/commands/decision.py` and the door's own seam: `answer_task_decision(job, decision_id, *, answer, source, now)` mutates an in-memory `Job` and returns the updated record or None, and it is `storage.save_job(job)` that persists it — the CLI's own answer path calls exactly that pair in exactly that order. The door already holds a freshly loaded `Job` from `_load_job`, so no second load is needed.

FIRST, THE EFFECT AND WHERE IT BECOMES DURABLE. CHOSEN: both calls ARE the effect and both sit inside the dispatch method that DECISION F009 D18's `try` already wraps. `save_job` is NOT one of D18's two post-effect writes. This is the substantive difference from `job.stop` and the reason D18 refused to let this round inherit its clause three: `safe_points.request_stop` is durable the moment it returns, so an audit line or a publication failing on top of it fails on top of a completed effect, whereas a `decision.resolve` whose `save_job` failed has changed NOTHING on disk. Treating `save_job` as a post-effect soft write would answer 200 for an answer no later reader can find. A raise from EITHER call is D18 clause four's `rejected_effect` and 500, unchanged.

SECOND, D18's CLAUSE THREE, RE-EXAMINED AS D18 REQUIRES RATHER THAN INHERITED. D18 made the soft failure of the nonce publication conditional on every effect in D5's table being idempotent at its own layer, and named this round as the one that must check that against this effect. MEASURED in `escalation.py`: `answer_task_decision` returns None when the decision is absent OR when its status is not OPEN, so an answer is written ONCE and a re-run cannot overwrite the one the run acted on. CHOSEN: clause three STANDS, with its cost restated for this command rather than assumed from the other. A lost publication cannot produce a SECOND answer — the dangerous reading of non-idempotency does not arise here — it can only make a client's retry of that same nonce miss the replay lookup, re-run the effect, be refused by the paragraph below, and receive a refusal for a command that in fact SUCCEEDED. A misleading refusal is strictly safer than a duplicate write.

ALTERNATIVE to that clause: fail the request when the publication fails. Rejected — it would report an answer that IS durable as one that is not, which is the same falsehood D18 rejected for `job.stop`, merely in the opposite direction.

THIRD, A REFUSAL THAT DID NOT RAISE, which no existing token covers. `answer_task_decision` returning None is not an exception, so `rejected_effect` — D18 clause four's token, defined as a dispatch that RAISED — does not describe it, and `accepted` would be false. CHOSEN: a new closed-set token `rejected_state`, audited with `create=True`, answered 409. The name states the CHECK that refused, as D14 requires of every token in the set: the decision is not in a state that can be answered. T5_F035 and T9_F167 read `commands_audit.jsonl` to count what the door DID, and an effect that ran and declined has to be distinguishable from one that broke.

FOURTH, WHERE THE TOKEN LANDS, AND WHY THIS ROUND EXISTS AT ALL. CHOSEN: `rejected_state` lands in `packages/orchestration/command_audit.py` in THIS round, one round ahead of the door that writes it — the convention D17 set for `accepted` and `replayed` and D18 followed for `rejected_effect` — so that the round retiring the 501 seam changes the door alone and the exact-tuple pin in `tests/orchestration/test_command_audit.py` moves in its own commit rather than in the commit that rewrites the door's control flow. THE BLOCK CAP IS NOT THE REASON THIS TIME AND IS NOT CLAIMED AS ONE: the reviewer estimated the combined round and it fits under DECISION F085 D6's 490, so unlike D18 and D19 this split is a convention rather than a measurement, and it is recorded as such. The wire constant for the 409 body lands WITH the door, as D20's two constants did, because it lives in the door's module and no other module reads it.

FIFTH, `not_implemented` SURVIVES ITS WRITER. When R23 removes the seam, the token STAYS in `OUTCOMES`. Audit files already on disk carry lines whose `outcome` is `not_implemented`, and the vocabulary is what a later reader validates a line against; removing it would make a record this door really wrote fail validation under a version of the code that came after it. The tuple is append-only for that reason, which is also why its order is pinned rather than sorted.

ALTERNATIVES for the third clause: (a) reuse `rejected_shape` for the None return — rejected, D14 binds that token to the REQUEST's shape and this door deliberately does not know any command's argument schema (D20), so it cannot tell a malformed `decision_id` from a well-formed one naming an absent decision. (b) answer 404 — rejected, the door already answers 404 for a missing JOB, and one status for two referents makes them indistinguishable to a client that must decide whether to retry. (c) split None into two tokens, absent and already-answered — rejected, `answer_task_decision` collapses both into one return value and the door would have to call `find_task_decision` first, a second read for a distinction no reading feature has asked for.

REVERSE the first clause by moving `save_job` out of the effect, which requires re-reading D18 clause three first; the third by retiring `rejected_state`, which T5_F035 and T9_F167 would then have to be told about; the fifth by removing `not_implemented` once no audit file predating R23 can still be read.

## DECISION F009 D22 — `answer_source` is not this door's to name, and the 501 becomes a guard (2026-08-22)

Measured by the reviewer at `9a47166c`, before this round was delegated, by reading `packages/orchestration/escalation.py` end to end rather than only the function DECISION F009 D5 names: `answer_task_decision(job, decision_id, *, answer, source=ANSWER_SOURCE_HUMAN, now)` writes its `source` argument into the record's `answer_source` field, and `escalation.py` lines 362-366 then COUNT that field into exactly two buckets — `ANSWER_SOURCE_HUMAN` is `"human"` and `ANSWER_SOURCE_DEFAULT` is `"default"` — emitting "Sources: N human, M default, K unresolved" into the escalation assumption log.

FIRST, AND THIS IS THE TRAP. CHOSEN: `_dispatch_decision_resolve` does NOT pass `source`. It takes the function's default, `human`. A person answering a question through the UI IS a human answering it, and the door is the TRANSPORT rather than the decider. Had this round inherited DECISION F009 D20's rule for `request_stop` and passed `COMMAND_EFFECT_SOURCE`, the record would carry `answer_source="ui"`, which is in NEITHER bucket: the assumption log's table would print "ui" in its Source column while the summary line beneath it counted the answer as neither human nor default, silently under-reporting every decision ever answered through this door.

WHY THIS IS NOT D20 GENERALISED, stated because the two fields share a name and a later round will be tempted. `request_stop`'s `source` names WHICH TRANSPORT asked — that is exactly the distinction D20 protected, a UI stop against a `remedy job stop` — and it is free-form inside the archived signal. `answer_source` names WHO DECIDED, over a closed two-value vocabulary that is counted. Attributing the transport into a field that means the decider is a category error, and the fact that both arguments are spelled `source` is the entire reason it is easy to make.

WHERE THE DOOR'S OWN ATTRIBUTION LIVES, since it is not lost: `commands_audit.jsonl`, per DECISION F009 D6, records `token_fp`, `command`, `args_hash`, `nonce` and `outcome` for every attempt at this door. A reader asking "was this decision answered through the UI?" answers it there, which is where D6 deliberately put it, rather than by widening a counted field in the job record.

SECOND, WHAT THE 501 BECOMES. DECISION F009 D21 said the seam goes; MEASURED while writing the dispatch, deleting it outright leaves the handler with no branch for an id that `_command_is_ui_exposed` admitted and no dispatch clause matches, so such a request would fall off the end of the method with NO response written at all. CHOSEN: the 501 stays as a GUARD rather than a placeholder, with a new constant `COMMAND_NOT_DISPATCHED_MESSAGE`, still audited `not_implemented`. It is unreachable while `UI_EXPOSED_COMMANDS` holds exactly the two ids this door dispatches, and a test reaches it by monkeypatching that frozenset to hold a third — which is precisely the mistake the guard exists to catch. This also supersedes D21's fifth clause by giving `not_implemented` a live writer rather than only a historical one; the clause's reasoning, that on-disk records must stay validatable, is unaffected and still holds.

THIRD, WHAT THE 409 PUTS ON THE WIRE. CHOSEN: `_safe_error(409, COMMAND_DECISION_STATE_MESSAGE)` with the message "decision is not open", carrying `error` and nothing else. Every other refusal this door issues — 400, 403, 429, 500 — goes out through `_safe_error` with exactly that shape; the deleted 501 seam was the only exception, and it is being deleted. A client knows which command it submitted, and its correlation key is the nonce it chose. CONSEQUENCE, stated because it is the whole of the pin migration: both surviving 501 pins asserted `body["command"]`, and neither can after this round.

FOURTH, WHAT THE EFFECT READS OUT OF `args`. CHOSEN: `decision_id` and `answer`, each taken from `args` when it is a `str` and degraded to `""` otherwise, exactly as DECISION F009 D20 ruled for `reason` and for the same reason — D14 types `args` as an object but never types what is inside it, and this door deliberately knows no command's argument schema. A `decision_id` of `""` matches no record, so `answer_task_decision` returns None and the request is refused 409 rather than raising, which is the same degradation path by construction.

FIFTH, WHAT THIS ROUND DELIBERATELY DOES NOT TEST, stated because DECISION F009 D16 forbids leaving a mechanism no test can reach and this round leaves two. MEASURED by the reviewer while assembling the block: the door, the two pin migrations and the three tests that would cover the new paths sum to 522 lines, over DECISION F085 D6's 490 cap, so the block does not fit and by D16's own rule a block that does not fit is not delivered. CHOSEN: this round lands the door and ONLY the two pin migrations that must move with it, both of which reach the 409 refusal path; the 200 acceptance path and the 501 guard are reached by NO test until the next round, which adds them purely additively together with the disk-level effect assertions in `tests/ui_server/test_command_dispatch.py`. That is exactly the cut DECISION F009 D19 made between R19 and R20 for `job.stop`, for the same measured reason, and it is the FOURTH time this feature has split on that single constraint — a fact recorded here rather than argued, because a later reader weighing how to plan a feature of this shape should have the count. The gap is explicit and scheduled rather than discovered: until that round lands, `save_job` running and the accepted body's `decision_id` field are asserted by nothing.

ALTERNATIVES: (a) pass `source="ui"` and widen the assumption log's vocabulary to three values — rejected, it changes a published artefact's meaning for every existing job to record something D6 already records elsewhere. (b) answer 404 rather than 409 for an absent decision — rejected by D21 already, and unchanged here. (c) delete the 501 and let an undispatched exposed id fall through — rejected, an unanswered request is the worst failure mode this door has and the guard costs four lines.

REVERSE the first clause by passing an explicit `source`, which requires first widening `ANSWER_SOURCE_*` and the two tallies that read them; the second by deleting the guard once a mechanism exists that makes an exposed-but-undispatched id impossible by construction; the third by giving refusals a richer body, which is a door-wide change rather than this command's.

## DECISION F009 D23 — the `command.accepted` event: where it is written, when, and what it carries (2026-08-22)

Measured by the reviewer at `cd77e969`, before this round was delegated, by reading the F008 stream end to end rather than only the door: `iter_sse_frames` is driven by `lambda: _load_events(job)`, `_load_events` calls `timeline.load_run_events(resolve_data_root(), job.id)`, and that function globs `<data root>/runs/<job id>/*.jsonl`. The stream therefore has no queue and no subscriber of its own — it is a TAIL of the job's run log, and the only way to put an event on it is to append one there.

FIRST, THE WRITER. CHOSEN: `timeline.append_run_event`, the wrapper this repository's other event writers already reach for — `autorun.py`, `do_run.py`, `builder_bridge.py`, `event_replay.py`, `job_fulfillment.py` and `repair_loop.py` among them, measured at `cd77e969`. ALTERNATIVES: (a) a new publish/subscribe seam inside `ui_server.py` — rejected, it would make the SSE stream and the cursor endpoint two contracts where `_safe_event_summary` deliberately keeps them one. (b) `commands_audit.jsonl` — rejected, and this is DECISION F009 D6's rejected alternative (b) read in the other direction: that record is per JOB and must outlive a run, while this is a live NOTIFICATION, so the two artefacts want opposite storage and both choices stand.

SECOND, WHEN. CHOSEN: LAST, after the publication DECISION F009 D18 orders third, making the emission D18's FOURTH write. A client that sees this frame will replay its nonce, and a client that replays before the publication lands gets a MISS — which sends it back through the door and runs the effect a second time. The ordering is the whole guard: `request_stop` is idempotent but `answer_task_decision` followed by `save_job` is not obliged to be.

THIRD, HOW IT FAILS. CHOSEN: SOFT, catching `OSError`, `RuntimeError`, `ValueError` and `TypeError` and returning, for D18 clause three's reason — the effect is already durable, so a full disk must not turn an accepted command into a 500 reporting it as refused. The caught set is spelled out rather than written as `except Exception`, which `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals` guarded this module against at `cd77e969`.

FOURTH, WHAT IT CARRIES. CHOSEN: `outcome="accepted"` as a NAMED parameter of `RunLogWriter.log` — not metadata, because `_safe_event_summary` reads `outcome` at the top level and a value one level down arrives on the wire as the empty string — plus the command id in metadata, which that summary drops. The frame is therefore `{seq, event, timestamp, outcome}` and carries no args, no nonce and no token: the stream is the job's own channel and D6 keeps this door's attribution in the audit file.

FIFTH, WHICH EXITS EMIT. CHOSEN: only the two ACCEPTED exits. A refusal announces nothing, and a replay announces nothing a second time — a replay REPEATS an acceptance rather than being one, which is the rule finding R-0636 already forced on the audit vocabulary, applied here so the UI cannot count a retry after a timeout as a second write.

REVERSE the first by moving the call behind a seam of its own; the second by re-ordering the two calls, which the replay-race argument above is the case against; the third by letting the exception escape, which converts a notification failure into a server fault; the fourth by widening `_safe_event_summary`, which would change both transports at once and is F008's contract rather than this door's; the fifth by emitting on refusals, which the tests this round ships forbid.

## DECISION F009 D24 — the P3 import contract: what the door may reach, stated as a set (2026-08-22)

Measured by the reviewer at `c98d57f0`, before this round was delegated, by walking `_RemedyHandler` with `ast` rather than by reading it: the write door is twelve methods and every import any of them makes is FUNCTION-SCOPED, so the door's import surface is exactly thirteen `(module, name)` pairs and an AST scan over those methods is exact rather than approximate. That is the fact this decision is built on, and it is what makes the guard cheap.

FIRST, ALLOWLIST OR DENYLIST. CHOSEN: BOTH, with the allowlist as the mechanism. The scan's union must EQUAL a named frozen set, so a new import is a failing test until a decision adds it; the forbidden-module set then says WHY that allowlist is the shape it is. ALTERNATIVES: (a) denylist alone — rejected, it passes silently on any import nobody thought to forbid, which is the whole failure mode of a contract enforced by convention. (b) allowlist alone — rejected, it pins the present without stating the rule, so a later reader cannot tell a ruled entry from an accident.

SECOND, `save_job`. CHOSEN: `packages.orchestration.storage` is reachable for the single name `save_job` and no other. DECISION F009 D21 rules that `answer_task_decision` and `save_job` are BOTH one effect, because the answer is durable only once `save_job` returns, so banning it would ban the effect table D5 already ruled. Any OTHER name out of that module is the "handler touching storage directly" the feature file's Acceptance forbids, and the guard says so as its own test.

THIRD, WHERE THE GUARD LIVES. CHOSEN: `tests/ui_server/test_command_channel.py`, as a class beside the file's existing non-HTTP classes. DECISION F009 D1 rules that file the command channel's contract home, and this is a contract over the same door; the repo's guard-test pattern in `tests/test_no_interactive_guard.py` keeps the scan in the test rather than in production, so no production line exists only to be checked.

FOURTH, THE VACUITY TEST. CHOSEN: the method list is itself asserted against the class. A guard of this shape dies by scanning nothing — rename a method and the union becomes empty, the equality against a non-empty allowlist then fails loudly, but a rename plus an allowlist trimmed to match would pass while guarding nothing. `test_every_named_method_exists` is what makes that a two-step mistake instead of a one-step one, and the red proof this round runs exercises it.

REVERSE the first by deleting either half and keeping the other; the second by removing `save_job` once the effect table stops naming it; the third by moving the class to its own module, which costs a rename and nothing else; the fourth by deleting that one test, which is also how to make the guard vacuous, so the two are deliberately the same act.

## DECISION F009 D25 — the 405 proof is a WALK over derived routes, not a list (2026-08-22)

Measured by the reviewer at `a164317b`, before this round was delegated, by reading `do_GET` end to end rather than by grepping it: the server dispatches four routes by a bare `path ==` or prefix comparison, thirteen job endpoints out of a single `handlers` dict literal, and six more STRUCTURALLY, by splitting `path` on "/" and comparing the parts — `events-since`, the SSE stream at `events/stream`, and three `nodes/<node>/…detail` routes. An AST scan for `path ==` literals alone therefore finds four of twenty-three, which is the trap this decision exists to avoid: such a scan reports a confident, small, WRONG inventory and a walk built on it would prove almost nothing while looking rigorous.

FIRST, WHERE THE WALK'S ROUTE LIST COMES FROM. CHOSEN: derive what can be derived, spell out the rest, and gate the boundary. The thirteen job endpoints are read out of the `handlers` dict literal by AST, so adding an endpoint puts it in the walk with no test edit at all; the four literal routes are read the same way and compared for EQUALITY against a named set; the six structural routes are written out, because nothing exists to derive them from. ALTERNATIVES: (a) a fully hand-written list — rejected, it proves the list rather than the server and goes stale silently. (b) a fully derived list — rejected as impossible, since a structural match has no literal to extract, and pretending otherwise is how the four-of-twenty-three inventory gets shipped.

SECOND, THE DRIFT TEST. CHOSEN: the derived literal set must EQUAL the named set, and every derived endpoint must appear among the walked paths. A route added as a new `path ==` comparison then fails the equality immediately, and a route added to the dict is walked automatically rather than being missed. The remaining hole is a new STRUCTURAL route, which neither half can see; it is named here as the known limit rather than papered over, and the sentence a reader will search for is in the class docstring.

THIRD, WHAT THE WALK ASSERTS. CHOSEN: for every walked path, POST, PUT and DELETE each answer 405 AND carry the body `{"error": "method not allowed"}`, plus a count assertion that the walk ran the number of requests it claims. A status-only walk passes against a server that answers 405 by accident from a different code path, and a walk that silently iterates an empty list is the vacuous case this repository keeps paying for.

FOURTH, THE OTHER HALF OF THE CLAIM. CHOSEN: the same class asserts that the commands path DOES answer 200, that an unknown path is 405 rather than 404 for a mutating verb, and that four near misses of the commands path — a trailing segment, a singular spelling, a missing job id and a case change — are all 405. "Every OTHER route is 405" is only meaningful beside a demonstration that this one is not, and the near misses are where a fail-open would actually arrive.

REVERSE the first by hand-writing the list, which reintroduces exactly the staleness the derivation removes; the second by deleting the drift test, which is also how to make the walk stop covering the server, so the two are deliberately the same act; the third by dropping to a status-only assertion; the fourth by removing the near-miss cases, which is the only part of this a later round might reasonably move into its own module.

## CORRECTION to DECISION F009 D25 — its route inventory, re-measured (2026-08-22)

D25's opening paragraph gives the inventory as "four routes by a bare `path ==` or prefix comparison, thirteen job endpoints out of a single `handlers` dict literal, and six more STRUCTURALLY", and concludes "an AST scan for `path ==` literals alone therefore finds four of twenty-three". Re-measured at `a164317b` by script, with the same AST predicate `_do_get_route_facts` uses in `tests/ui_server/test_command_channel.py`: the literal-equality set is `/`, `/api/state` and `/api/layers` — THREE — the `/assets/` route being a `startswith` prefix no literal scan can reach; the `handlers` dict yields thirteen; and the structural routes are the FIVE that same sentence enumerates, which is also exactly what `_walkable_paths` walks. So the walk covers twenty-two paths and sixty-six requests, and a literals-only scan finds three of twenty-two.

Every CHOSEN clause of D25 stands unchanged, and so does its argument: a literals-only inventory still comes back confidently small and wrong, at three of twenty-two rather than four of twenty-three. Registered as finding R-0644. The original paragraph is left standing rather than repaired, because this record is append-only (docs/agents/planner_reviewer_prompt.md §3 item 20).

## DECISION F021 D1 (2026-08-22) — the humanize catalog's coverage test is keyed on the kinds the STREAM can carry, because no "Part E kind list" exists

CONTEXT, measured at `4a7b5cbf` and recorded in `.agent/f021_inventory.md`: the feature file's T001 slice orders "coverage test against the Part E kind list", and there is no such list. `RunEvent.event` is an unvalidated free string; four defined kind sets exist — `NARRATED_EVENTS`, `EVENT_METADATA_SCHEMAS`, `TRACE_EVENT_KINDS` and `_STREAM_EVENT_KINDS` — and they are pairwise disjoint; and of the distinct literals actually passed at run-log emission sites, only one appears in any of those four sets. A coverage test written against any one of them would pass while covering almost nothing that reaches a reader, which is the silently-vacuous-gate class of R-0438 arriving through a specification instead of a gate.

CHOSEN: T001 defines its own authoritative constant — the set of kinds the humanize catalog claims to cover — in the humanize module itself, and the coverage test asserts that the catalog's key set EQUALS that constant, so a kind added to one and not the other goes red. That constant is seeded from the emission literals that can be enumerated STATICALLY. The emission sites that compute their kind name at runtime cannot be enumerated by any test, and they are covered instead by the feature file's own unknown-kind rule: an unrecognised kind renders an honest generic line and is never dropped. That rule therefore stops being a nicety and becomes the load-bearing half of the contract, so T001 ships a test for the generic path beside the coverage test.

ALTERNATIVES CONSIDERED. Key the test on the union of the four defined sets: rejected, because the union describes almost nothing the stream actually carries, so the test would be green and worthless. Make `RunEvent.event` a closed enum at the source: rejected for THIS feature, because it edits the event schema far beyond the one field D2 permits and would touch every emission site; it is the right long-term fix and belongs to a feature that owns the schema. Skip the coverage test: rejected, the feature file names drift protection as T001's purpose.

REVERSE IT by deleting the constant and the equality assertion; the catalog and the generic-line rule stand without them.

## DECISION F021 D2 (2026-08-22) — jump-to-node gets ONE additive field on the SSE envelope, and the feature file's Do-not-touch is narrowed to permit exactly it

CONTEXT, measured at `4a7b5cbf`: `_safe_event_summary` in `packages/orchestration/ui_server.py` returns exactly `seq`, `event`, `timestamp` and `outcome`, dropping `RunEvent.task_id` and the event metadata. The feature file's "How it fits" asserts that events already carry the linkage the reducer used; they do not. Its Goal & Done requires feed rows to click-jump to their node, and its Do-not-touch bans the event schema, so as written the file forbids the only route to its own acceptance criterion — a contradiction internal to the specification, not a trade-off.

CHOSEN: add ONE additive field carrying the task or node linkage to `_safe_event_summary`, and narrow the Do-not-touch ban to permit exactly that field and nothing else. The seam is the right one and says so in its own docstring: it has ONE writer, and a field added there reaches the cursor endpoint and the SSE stream together, so the two transports cannot drift. The field is additive, so every existing consumer keeps working. The client side must also stop discarding the payload, which is a client change and not a schema one.

ALTERNATIVES CONSIDERED. Drop jump-to-node from F021: rejected, it is named in Goal & Done and in T003, so dropping it silently reduces the feature to less than its acceptance criteria. Resolve the node client-side by matching on timestamp or seq: rejected, it invents a second mapping the reducer does not use, which is exactly the "one source" property the feature file asks for and would be wrong whenever two events share a timestamp. Add the whole event metadata blob: rejected, it widens the schema change from one field to an unbounded one and carries data the feed does not need.

REVERSE IT by removing the field and restoring the blanket Do-not-touch line; jump-to-node then has to leave the feature with it.

## DECISION F021 D3 (2026-08-22) — T001's coverage constant is DERIVED from the Python sources by a contract test rather than hand-seeded, and D1's seeding reading is corrected

CONTEXT, measured by the reviewer at `91d14c88` over `packages/`, `apps/` and `scripts/`. DECISION F021 D1 seeds T001's authoritative coverage constant from "the emission literals that can be enumerated STATICALLY", and supports that with "of the distinct literals actually passed at run-log emission sites, only one appears in any of those four sets". Both readings come from `.agent/f021_inventory.md` at `4a7b5cbf`, which named its own scope as an AST sweep of `packages/**/*.py` and was correct within it; D1 dropped the scope and kept the number. The same AST predicate over all three roots reads 82 emission call sites, 60 distinct string-constant names and 11 event arguments that are not string constants, and 15 of the 60 lie in the four defined sets — every one of `NARRATED_EVENTS`' eleven among them, emitted from `apps/cli/commands/job.py` and its siblings. A second omission compounds it: `_load_events` in `packages/orchestration/ui_server.py` has TWO branches, and the JobPlan branch `_load_job_plan_events` writes the trace event kind straight into the envelope's `event` field, so `TRACE_EVENT_KINDS` and the values of `_STREAM_EVENT_KINDS` in `packages/orchestration/agent_run_trace.py` — 16 and 6 names, whose intersection with the 60 is empty — also reach a reader. With `command.accepted`, emitted through the module constant `COMMAND_ACCEPTED_EVENT` rather than as a call-site literal, the vocabulary that can be enumerated statically is 83 names, not 23. D1's own text is NOT rewritten here: `.agent/decisions.md` is append-only and §3 checklist item 20 makes the dated correction the counter-measure rather than an edit.

CHOSEN: the coverage constant is DERIVED rather than written down. T001 ships a pytest contract test under `tests/ui_contracts/` that re-derives the static kind set from the Python sources — the AST predicate above over the three roots, plus `TRACE_EVENT_KINDS`, plus the values of `_STREAM_EVENT_KINDS`, plus the value of any module-level string constant a run-log call site passes by name — and asserts it EQUALS the key set of the catalog in `apps/ui/src/api/humanize.ts`, read as source text in the manner the files under `tests/ui_contracts/` already use for the stream hook. Drift then goes red from EITHER side: a new Python emitter with no catalog entry, and a catalog entry no emitter can produce. D1's unknown-kind rule stands exactly as ruled and carries the 11 runtime-computed names, which no static derivation can reach, so T001 still ships the generic-path test beside the coverage test.

ALTERNATIVES CONSIDERED. Hand-list the names in the humanize module as D1's constant, corrected to 83: rejected, it is the same maintenance contract with none of the drift protection, because a hand list is exactly the artefact that was wrong here and nothing would ever re-measure it. Generate the TypeScript constant from Python at build time: rejected, `apps/ui` has no generator step and adding one is a build-system change far outside F021. Keep the 23 `packages/` literals and route the rest to the generic line: rejected, it would send `task_run_started` and `verification_passed` — names the feature file's Goal quotes as examples of the story it wants — into the fallback that exists for names nobody can enumerate.

REVERSE IT by deleting the contract test and its equality assertion; the catalog and the unknown-kind rule stand without them, which is the reversal D1 already described.

## DECISION F021 D4 (2026-08-22) — T002 adds no DOM test environment; its rules go into node-testable `.ts` modules and its components are gated by a Python source contract

CONTEXT, measured by the reviewer at `fc56d4cc`. `apps/ui/vitest.config.ts` sets `environment: "node"` with `include: ["src/**/*.test.ts"]`, so no `.tsx` test is collected and no DOM exists to render into; `find apps -name '*.test.tsx' -not -path '*/node_modules/*'` returns 0 files, and `jsdom`, `testing-library` and `happy-dom` occur 0 times in `apps/ui/package.json` and `apps/ui/vitest.config.ts`. T002 is component work, so the naive reading is that the environment must change. It must not, because this repository has already answered the question and written the answer down at the seam: the header comment of `apps/ui/src/api/useBrainStream.ts` states that it is "deliberately the ONLY part of it that is React at all: every rule this client has lives in brainStream.ts, brainStreamDriver.ts, brainStreamRunner.ts and brainStreamSession.ts, where the node-environment vitest can reach it", and that what remains is "gated by a tests/ui_contracts/ source contract, the style this repository uses for every React component". `tests/ui_contracts/` holds eleven such Python contract modules, `test_remedy_shell_stream.py` among them. The brain-stream family is that pattern at scale: six logic modules, each with a `.test.ts` neighbour the node vitest collects, behind one thin hook.

CHOSEN: T002 changes neither `environment` nor `include`. Every rule T002 needs becomes a pure module under `apps/ui/src/` with a `.test.ts` neighbour — the projection of a stream event into a feed row, the ACTION-class subset the NowCard shows, the recency state of the activity dot, and the scroll discipline as a `(pinnedToBottom, newEventArrived) -> shouldScroll` function. The `.tsx` components read an already-projected view and render it, and their structure is gated by a new Python source contract under `tests/ui_contracts/` written in the manner of `test_remedy_shell_stream.py`. The scroll rule is called out because it is the acceptance criterion that sounds least like a pure function and is one: "never yank a reader who has scrolled up" is entirely a decision about whether to scroll, and the only DOM left after that decision is a single `scrollTop` assignment no assertion is worth.

ALTERNATIVES CONSIDERED. Add `jsdom` and `@testing-library/react` and widen `include` to `.test.tsx`: rejected, it introduces a second test environment and three devDependencies into a package that deliberately has neither, to buy assertions about markup that the Python source contracts already make more cheaply and in the language every other gate in this repository is written in; it also stacks a React-DOM test suite on top of `apps/ui`'s lint config, which finding R-0622 measures as parsing none of the TypeScript it is aimed at, so the new files would be as unlinted as the old ones. Rewrite the components as render functions returning plain data: rejected, that is the chosen option with an extra layer of indirection and no additional coverage. Gate the feed through the Python source contracts ALONE: rejected, a source contract can assert that a component maps over its rows, and it cannot assert that the scroll never yanks — which the Acceptance section names outright.

REVERSE IT by adding `jsdom` and `@testing-library/react` to `apps/ui` devDependencies, setting `environment: "jsdom"` and widening `include` to `src/**/*.test.{ts,tsx}`. The `.ts` logic modules and their tests stay valid under that change, so the reversal is purely additive and costs no rewrite of anything T002 ships.

## DECISION F021 D5 (2026-08-22) — the fan-out is a bounded event ring inside the existing brain-stream runner, published on the existing view

CONTEXT, measured by the reviewer at `fc56d4cc`. The single subscription the feature file's Orchestrator brief demands ALREADY EXISTS and is not what is missing: `useBrainStream` occurs at three lines across `apps/ui/src/` — its definition, its import in `apps/ui/src/components/shell/RemedyShell.tsx`, and the one call in that shell — and the shell passes `stream.status` down into `RightLivePanel`. What is missing is the events themselves. `BrainStreamView` in `apps/ui/src/api/brainStreamRunner.ts` carries `status`, `lastSeq` and `gapDetected` and nothing else, and `BrainStreamState` in `apps/ui/src/api/brainStream.ts` adds only `attempt`: the runner dispatches every event and RETAINS none of them. That is why `ActivityFeedCard` is fed a `RemedyActivityItem[]` off the REST dashboard today — the current feed is a second DATA PATH rather than a second connection, and it is not live.

CHOSEN: T002 adds to `BrainStreamState` a `recent` ring of at most 500 projected rows, appended on dispatch and dropped from the front past the bound, and publishes it on `BrainStreamView` under the object-identity contract `createBrainStreamRunner` already documents — `view()` returns the SAME object until something visible changes, because `useSyncExternalStore` compares snapshots with `Object.is` and re-renders forever otherwise. The rows reach the feed and the NowCard by being passed down from the ONE `useBrainStream` call `RemedyShell` already makes, exactly as `stream.status` is passed down today. No second `useBrainStream` call, no new hook, and no `EventSource` constructed outside `apps/ui/src/api/brainStreamDeps.ts`. The drop past the bound is OBSERVABLE and never silent: once the ring has dropped anything, the feed says so and points at the timeline, which is what this feature file's own edge-case paragraph requires of a bounded window. The bound is a number rather than a promise because nothing upstream supplies one — `packages/orchestration/ui_server.py` caps concurrent streams per job at `SSE_MAX_STREAMS_PER_JOB = 4` and caps event COUNT nowhere — and 500 is far past the five rows the current card shows and far short of a memory concern.

ALTERNATIVES CONSIDERED. Call `useBrainStream` a second time in `RightLivePanel`: rejected outright, because that hook builds one session per call and each session opens its own `EventSource`, which is the second connection the Orchestrator brief rejects as an architecture line. A module-level singleton store outside React: rejected, it re-introduces exactly the connection-lifetime bug the cleanup comment in `useBrainStream` exists to prevent, and it makes two jobs on one page impossible. Keep feeding the feed from the REST dashboard's activity list: rejected, it is not the live stream, so the NowCard's recency dot would be honest about nothing and the feature's Goal — that the STREAM becomes a story a human can follow — would go unmet while looking met. An unbounded log: rejected, a long job grows it without limit and the feature file already calls for a bounded window.

REVERSE IT by deleting the `recent` field from `BrainStreamState` and `BrainStreamView` and restoring `ActivityFeedCard`'s dashboard-fed props. The graph, the status badge and the gap detection read none of it, so nothing else on the surface changes.


## DECISION F021 D9 (2026-08-22) — the NowCard badge lights on RUNNING AND RECENT, never on either alone

CONTEXT, measured by the reviewer at `baf079b1`. `recency.ts` exports `isLiveByRecency`, whose own comment calls it "the single source R21 gives BOTH the badge and the dot", and until now nothing read it: R28 wired the DOT to `recencyLevel` and left the badge on `deriveAgentStatus`'s `isRunning`. The two candidate sources disagree in opposite directions, and each disagreement is visible on the same card. `isLiveByRecency` is true for `fresh` and `fading`, so it stays true for `QUIET_WINDOW_MS` — 30 seconds — after the last ACTION row arrived, INCLUDING after the job has ended; `deriveAgentStatus` returns `status: "Working"` if and only if `dashboard.live.running === true`, and "Idle" otherwise. So a badge fed by recency alone renders "Live" beside the word "Idle" for up to 30 seconds after every run — the exact rendering R-0652 was raised for, with a fuse instead of a latch — while a badge fed by `isRunning` alone renders "Live" beside a dot that has faded to idle whenever a running job has been quiet for 30 seconds.

CHOSEN: the CONJUNCTION. The badge lights only when `isRunning` AND `isLiveByRecency(level)`, so it can never contradict either the status word beside it or the dot below it. Because `deriveAgentStatus` returns "Working" on exactly the condition that makes `isRunning` true, the badge is now structurally incapable of appearing next to "Idle", "Blocked" or "Needs your decision" — the R-0652 guarantee is enforced by the conjunction rather than by a comment. The dot keeps reading the recency level ALONE and is unchanged: it answers "how long since the agent last did something", which stays a true and useful answer after a job ends, and it is the surface where the quiet window belongs.

ALTERNATIVES CONSIDERED. Recency alone: rejected, it reintroduces R-0652's rendering for 30 seconds after every run, and R28's reviewer dry run turned the existing pin red on exactly that change, which is how this question was found rather than shipped. `isRunning` alone, the status quo: rejected, it lets the badge claim life while the dot beside it has faded, so the card contradicts itself in the other direction and `isLiveByRecency` stays dead code the design reference calls load-bearing. Widening `QUIET_WINDOW_MS` or adding a job-ended reset to `recency.ts`: rejected, both push a UI concern into a pure rule whose whole value is that it is a function of two numbers, and neither removes the contradiction — they only shorten it.

REVERSE IT by restoring `{isRunning && <span` in `AgentNowCard.tsx` and the pin that names it in `tests/ui_contracts/test_brain_stream_ring.py`. The dot, the tokens, the CSS and `recency.ts` are untouched by this decision and by its reversal.

## DECISION F021 D10 (2026-08-22) — the feed's newest edge is the TOP, and the live window is deliberately taller than its box

CONTEXT: `apps/ui/src/api/feedScroll.ts` has existed since R17 as a pure rule — `shouldFollowNewest`, `nextFeedScroll`, `shouldShowNewRowsPill` over a `distanceFromNewest` in pixels — and nothing imported it. R31 wires it into `ActivityFeedCard.tsx`. Two things had to be ruled before that wiring could be written, because the design sources disagree in wording and the built feed disagrees with both in direction. CHOSEN: (1) `distanceFromNewest` is `scrollTop`, because the live feed renders NEWEST FIRST — `recent.slice(-LIVE_ROWS_SHOWN).reverse()`, a line tests/ui_contracts/test_brain_stream_ring.py has pinned since R16 — so the newest row sits at the TOP of the box and offset 0 IS the newest edge. docs/ui/design_reference/component_spec.md says "autoscroll pinned-to-bottom" and docs/roadmap/features/T5_F021.md says "auto-scroll pinned to newest"; the second is the roadmap layer, which AGENTS.md's documentation-boundary rule makes the authority for planning, and "newest" resolves correctly in a newest-first list while "bottom" does not. (2) The affordance is labelled `Jump to live` with the unseen count beside it, the exact wording T5_F021.md binds, rather than component_spec.md's "↓ new" pill — an arrow pointing down would point AWAY from the newest edge under (1), and taking the roadmap file's wording introduces no glyph, no icon and no asset, so no assets_spec.md change and no design-fidelity deviation is owed. (3) `LIVE_ROWS_SHOWN` rises from 5 to 40. The feature file's binding CSS gives the feed `max-height:52vh;overflow:auto`, and a window of 5 rows can never overflow a box that tall, so the never-yank rule and the pill would both remain unreachable in the product — headless in a second sense, after having been headless in the first since R17. The ring still holds BRAIN_RECENT_LIMIT at 500 and the timeline is still the archive. ALTERNATIVES CONSIDERED: flipping the feed to newest-LAST to match component_spec.md's "bottom" wording literally, rejected because it would rewrite behaviour R16 pinned and vitest covers, to gain nothing an axis convention does not already give; and keeping 5 rows with a shorter box, rejected because the box height is the one thing the feature file states as binding CSS. HOW TO REVERSE: (1) and (2) reverse together by rendering the feed newest-last, passing `scrollHeight - clientHeight - scrollTop` as `distanceFromNewest` and restoring the "↓ new" label; (3) reverses by restoring the constant to 5. `feedScroll.ts` itself changes under none of these — it is a pure function of a distance, and which end of the box that distance is measured from is this decision, not that module's.

## DECISION F021 D11 (2026-08-22) — the disabled steering input ships the design reference's sentence, not the feature file's paraphrase

CONTEXT, measured at `78c72880`: two binding-looking documents give this one tooltip two different texts. `docs/ui/design_reference/ux_spec.md` §11.3 specifies the activity card's input as "DISABLED until steering exists (tooltip: "Steering arrives with a later feature — watching only for now.")". `docs/roadmap/features/T5_F021.md` says instead: 'Steering input: rendered, disabled, tooltip "steering lands with F030"'. Both want an honest disabled control; they disagree on the words a user reads.

CHOSEN: the ux_spec sentence ships verbatim, as the constant `STEERING_DISABLED_REASON` in `ActivityFeedCard.tsx`. `.agent/context.md` states the precedence this feature works under — "docs/ui/design_reference/ is binding for every visual surface" — and a tooltip is a visual surface. The feature file's own Goal states the requirement as "the steering input renders DISABLED with the honest tooltip until its backing feature exists", which is a property and not a string; its quoted phrase reads as a paraphrase of that property rather than as competing copy. The reference sentence is also the better one for the reader it addresses: it says what will happen and what is happening now, and it does not make a user decode a roadmap id.

ALTERNATIVES CONSIDERED. Ship the feature file's phrase: rejected, it inverts the stated precedence and would put the shipped surface at odds with the document the round is gated against. Merge both, naming F030 inside the reference sentence: rejected, it edits binding copy to carry an internal identifier, which is the same category error as the first. Ship neither and hide the input until F030: rejected outright, because ux_spec §11.3 places the control on this surface and the feature file's own brief calls for "visible honesty over hidden UI".

REVERSE IT by changing the constant and the contract's `REASON` together; they are asserted equal, so neither can drift alone.

## Rescued from the F021 review record (F022 R1)

These rulings were taken during F021 and recorded ONLY in `.agent/live_review.md`, which is rebuilt at every feature claim. F022 R1 moved them here verbatim, extracted by script from that file at `c34ef32b` and never retyped, immediately before the rebuild that would otherwise have deleted them. Finding R-0669 registers the defect this rescue works around. The paragraphs below are the originals; their round context is in the `Gate:` paragraphs of that file at `c34ef32b`, which git history keeps.

DECISION F021 D6, 2026-08-22, taken by the reviewer under §4 item 7 and recorded here rather than asked: THE SINGLE WIRING ROUND THE PLAN CARRIED SINCE R19 IS UNBUILDABLE AS WRITTEN AND IS REPLACED BY FOUR SMALLER ONES. The plan ordered R22 to make `recency.ts` the NowCard's liveness source AND to drive the feed's scroll container from `feedScroll.ts`. `recencyLevel(lastActionAtMs: number | null, nowMs: number)` takes two NUMBERS, and measured at `bf0c50bf` this client holds no numeric instant at all: `FeedRow.timestamp` is a STRING that `feedRowOf` copies out of the safe envelope, `_safe_event_summary` fills it from the run log's own `timestamp`, and `ui_server.py` passes that through unparsed and empty where the log carries none. CHOSEN: stamp each frame on ARRIVAL from the CLIENT's clock, installed as an injected dependency — R22 the clock, R23 the frame event's `receivedAtMs`, R24 the ring's row, R25 the NowCard's badge and dot, R26 the feed's scroll container and pill. Both operands of the subtraction then sit on ONE clock, so the skew case cannot arise. CONSIDERED AND REJECTED: parsing the envelope's string, because a server clock running BEHIND the client yields a large positive elapsed and the dot reads a working agent as idle — the exact failure `recency.ts` names as the one it must never make — and an empty or unparsable stamp yields NaN, which falls through every window comparison to `idle` for the same wrong reason. CONSIDERED AND REJECTED: holding the stamp in the NowCard as component state, which touches no existing file but resets on every remount and measures when the CARD first saw an action rather than when the CLIENT received it. REVERSE THIS by deleting this paragraph and restoring the plan's single R22; the cost is that the dot has no honest number to read.

DECISION F021 D7 — THE RING ROUND MOVES FROM R25 TO R26 AND R25 BECOMES THE DISCHARGE ROUND. CHOSEN: spend this round on the record — promote R-0656's rule into §3 as checklist item 32, record R24, and register and repair the gap above — and give the ring a round with nothing else in it. WHY: R-0656 recurred in the block written immediately after the one registering it, which is exactly the ⚠️ condition docs/agents/planner_reviewer_prompt.md §2 defines, and §2's prescribed response to ⚠️ is that the reviewer APPLIES smaller steps rather than offering the operator a choice. R-0654 through R-0659 are all defects in the reviewer's own block text or record and none is a worker's execution error, so adding the ring's pairs to a block already carrying a checklist amendment and three ledger paragraphs is the change most likely to produce the next one. ALTERNATIVES CONSIDERED: folding the promotion into the ring round, which does fit the 490-line budget and was rejected because it puts a code change and three record obligations into one block against a ⚠️ momentum flag; and deferring the promotion until after the ring, rejected because the recurrence paragraph at `bdc242b4` states the reviewer owes it BEFORE R25 and a rule living only in a finding body has now demonstrably failed to bind twice. HOW TO REVERSE: any later relay may order the ring and the record in one block; D7 binds no round after R26, and DECISION F021 D5 still governs the ring's append placement whenever it runs.

DECISION F021 D8 — A VITEST RED CONTROL IS NOW REACHABLE, SO THE FEATURE'S BEHAVIOURAL TESTS STOP BEING UNPROVED. CHOSEN: run destructive vitest and tsc checks inside a disposable `git worktree` with `apps/ui/node_modules` SYMLINKED from the primary checkout, and require a mutation red proof of any vitest case a round newly relies on. WHY: this chain has recorded since R-0518 that "no vitest case has been mutation-proved" because a fresh worktree has no `node_modules`, and guardrail G5 forbids mutating the primary checkout — so the strongest guard the UI has was also the least proven. MEASURED BEFORE THIS ROUND WAS DESIGNED, at `d121dd09` in a disposable worktree: with the symlink in place `npx tsc --noEmit` exits 0 and `npm run test:unit` reads 15 files and 209 tests all passing, identical to the primary checkout; forcing `overflow` to 0 in `receiveBrainFrame` turned exactly 2 of those red and restoring the byte returned all 209 to green. A SYMLINK AND NEVER A COPY: `shutil.copytree` defaults to `symlinks=False` and dereferences npm's bin shims, which is the mechanism R-0591 registered, so the argument is named here rather than left to the caller. R-0518 STAYS OPEN and is NOT resolved by this entry — a worktree still ships no `node_modules` of its own and a round that forgets the symlink still reads a false red — but the limitation it describes no longer blocks a red proof. HOW TO REVERSE: drop the symlink step and the vitest red-proof obligation from later blocks; nothing else depends on it, and the Python source contracts remain the durable seam pins they were.

## DECISION F022 D1 (2026-08-23) — the budget tick envelope: where it emits, what it carries, and why the basis is not a new vocabulary

CONTEXT, measured by the reviewer at `5f53471f` and recorded in `.agent/f022_inventory.md` at that commit. `docs/roadmap/features/T5_F022.md` says the budget guard "already evaluates spent-vs-limits at safe points" and that the tick emits "at those same evaluations", which reads as though every evaluation site is a candidate. The inventory measures four production call sites of `evaluate_budget`. Three of them — `apps/cli/commands/job.py:2127`, `:2172` and `:2221` — sit inside `_cmd_job_budget`, the handler the dispatch table binds to `job.budget` at `apps/cli/commands/job.py:2374`, so they run when a human asks for a budget report and never during a job. The fourth, `packages/orchestration/safe_points.py:616`, sits inside `should_stop`, whose own docstring at lines 601-602 calls it "the SINGLE entry point for safe-point evaluation", and which the run path reaches from `packages/orchestration/long_run_executor.py:1389` and `:1403`, `packages/orchestration/pingpong_job.py:1970` and `apps/cli/commands/do_cmd.py:793`.

CHOSEN (1), THE EMISSION SITE, AND IT IS ABOVE THE EXHAUSTION TEST. The tick emits in `should_stop`, immediately after the `evaluate_budget` call at `packages/orchestration/safe_points.py:616` and BEFORE the `if evaluation.exhausted` test at `:617`. Emitting inside that branch would fire the ticker only at exhaustion, which is the one moment a live cost ticker is no longer needed. The three `_cmd_job_budget` sites emit nothing: a reporting command that ticked would write ledger events for a read. Note a consequence rather than a bug: `should_stop` returns at `:606` on an operator stop, before the budget block, so a safe point stopped by the operator evaluates no budget and emits no tick. No evaluation, no figure — stated here so a later round does not read the gap as a defect.

CHOSEN (2), THE PAYLOAD CARRIES ABSOLUTE VALUES ONLY, AND CURRENCY ONLY WHEN PRICED. Fields: `spent_tokens` always; `spent_usd` only when a cost figure exists; `limit_tokens` and `limit_usd` only when that limit is configured; `basis`; `unmeasured_calls`. An absent limit is an ABSENT KEY, never null and never zero, so the acceptance criterion that the limitless variant never fabricates a denominator is enforced by the envelope's shape rather than by the client's care. `_LIMIT_ORDER` at `packages/orchestration/budget_guard.py:245` fixes five limit kinds, of which cost is one, so a job may be budget-limited with no money limit at all and the spent-only variant is the normal case rather than the edge.

CHOSEN (3), THE BASIS IS THE TWO BOOLEANS THAT ALREADY EXIST, NOT A THIRD SPELLING. `BudgetEvaluation` at `packages/orchestration/budget_guard.py:216` already carries `token_lower_bound` at `:223` and `cost_lower_bound` at `:225`, the second commented "True when the cost figure is a floor, not a total: some call was unpriced". `basis` is therefore an object with one key per figure, each reading `actual` or `lower_bound`, and the cost key additionally able to read `absent`, mapped mechanically from those two fields plus the presence of a cost figure. The feature file's basis strings — "estimated — class defaults", "actuals with N unmeasured calls" — are DISPLAY text, composed in the client from this object and `unmeasured_calls`, and are not transported.

CHOSEN (4), NO CLIENT ARITHMETIC BEYOND THE FILL RATIO. The client computes the fill of spent against the configured limit and nothing else: no currency conversion, no price constant, no summation, no unit scaling. The tick carries every figure the display needs as an absolute value. This is the feature file's verbatim order material and it is testable as an ABSENCE, which is how T002 should gate it: no price-like constant under `apps/ui/src`.

CONSEQUENCE THIS DECISION BINDS, found by the R3 inventory. A `budget`-named tick is genuinely additive on the transport — `_safe_event_summary` at `packages/orchestration/ui_server.py:2748` passes the ledger event name through against no whitelist, and `sse_event_frame` emits no SSE event field — but it is NOT additive on the humanize catalog, where `apps/ui/src/api/humanizeCatalog.ts` is pinned EQUAL to the Python static vocabulary by `tests/ui_contracts/test_humanize_catalog.py:222`. The round that emits the first such event therefore adds the catalog key in the SAME commit and gates that suite, which no F022 round had gated before this one. The dotted name needs no new rule: `command.accepted`, at `packages/orchestration/ui_server.py:3119`, is already in that vocabulary.

ALTERNATIVES CONSIDERED. Emit at all four evaluation sites: rejected, three of them are a CLI report and would put ledger writes on a read path. Emit inside the exhaustion branch, where the evaluation is already consumed: rejected for the reason in (1) — it is the smallest diff and it produces a ticker that ticks once, at the end. A single flat basis enum such as actuals or estimated or mixed: rejected, it loses WHICH of the two figures is a floor, and the display must mark the spend and the cost independently. Carry the display sentence on the wire: rejected, it moves copy into the backend and makes the honesty text untranslatable and untestable at the component level. Send a null cost limit for a limitless job: rejected, a null denominator is the fake denominator the acceptance criteria forbid, and an absent key cannot be divided by accident.

REVERSE IT by deleting the emission from `should_stop` and the humanize-catalog key together; they are pinned equal, so neither can drift alone. Rulings (2), (3) and (4) reverse independently of the site choice in (1), and none of them binds MetricsBar's other metrics, which this feature does not touch.

## DECISION F022 D2 (2026-08-23) — the tick's WRITER, its file, and the transport gap D1 did not reach

CONTEXT, measured by the reviewer at `94694b3f` by building the change end to end in a disposable worktree before this block was written. DECISION F022 D1 ruled WHERE the tick emits and WHAT it carries. It ruled neither HOW it is written nor whether what it carries survives the journey to a client, and both gaps are load-bearing: the first would have shipped a ticker that is silently dead on the main long-running job shape, and the second is the difference between a feature and an event nobody can render.

CHOSEN (1), THE WRITER IS `RunLogWriter` AND NOT `timeline.append_run_event`. Every other one-shot emitter in this repository — `_emit_command_accepted_event` at `packages/orchestration/ui_server.py:3619` is the model — takes the short route through `append_run_event`, and that route cannot serve this call site. `append_run_event` resolves its id with `UUID(str(job_id))` at `packages/orchestration/timeline.py:63`, while a JobPlan's `job_id` is `uuid4().hex[:16]` at `packages/orchestration/pingpong_job.py:205` — sixteen hex characters, which `UUID()` rejects with `ValueError`. Measured in the worktree: the ping-pong shaped id emits ONE tick through `RunLogWriter` and would have emitted NONE through `append_run_event`, and because the emission fails soft the loss would have been silent. `RunLogWriter.__init__` does only `str(job_id)` at `packages/orchestration/run_log.py:112`, and `packages/orchestration/pingpong_job.py:2887` already logs through it with exactly that id, so this is the repository's own precedent rather than a new mechanism.

CHOSEN (2), THE EVENT NAME IS AN INLINE LITERAL AT THE CALL SITE. `tests/ui_contracts/test_humanize_catalog.py` builds the Python stream vocabulary by an AST walk whose `_event_argument` keeps a name only when it is an `ast.Constant` string, so a module constant is an `ast.Name` and is invisible to it. `command.accepted` survives as a constant only through a hard-coded hatch that names `ui_server.py` and reaches nothing else. Measured: with the literal inline the derived vocabulary moves from 83 kinds to 84 and equals the catalog exactly; with the catalog line deleted the pin fails naming `budget.tick`, so the pin is not merely green, it BITES.

CHOSEN (3), ALL OF A JOB'S TICKS SHARE ONE RUN-LOG FILE. `RunLogWriter` mints a fresh run id per instance and the emitter is constructed per evaluation, so the default would leave one `.jsonl` file per safe point for the length of a long job. A stable run id is passed instead. Nothing in this repository parses a run-log file name — `load_run_events` at `packages/orchestration/timeline.py:79` globs `*.jsonl` and sorts by timestamp — so the stable name costs nothing and was measured to produce exactly one file per job across the probe runs.

CHOSEN (4), IT FAILS SOFT AND THE ROUND'S TESTS PIN THAT IT DOES. A notification that breaks the run it reports on is worse than a missing frame, which is `_emit_command_accepted_event`'s own stated reason. Note a consequence rather than a bug, measured at the base and unchanged by this round: `apps/cli/commands/do_cmd.py:793` calls `should_stop` with an EMPTY job id, and that call raises `StopControlError` out of `validate_job_id` BEFORE the budget block is reached — at the base commit as well as after this change. That path therefore evaluates no budget and emits no tick, and it did not begin doing so here. It is recorded as an open question for the branch that owns that file, not as F022 work.

THE GAP THIS DECISION OPENS AND R6 CLOSES. `_safe_event_summary` at `packages/orchestration/ui_server.py:2748` returns exactly `{seq, event, timestamp, outcome, task_id}` and DROPS the event's `metadata`, which is where every figure D1 ruled lives. A client subscribing to the stream today would receive `budget.tick` frames carrying no spend, no limit and no basis, so D1's payload is correct and, on its own, unreachable. That is not a defect of D1 and it is not repaired here: the summary's key set is pinned by an exact equality at `tests/ui_server/test_sse_stream.py:90` and its frames are a golden byte stream at `:353`, so widening it unconditionally turns both red. R6 widens it CONDITIONALLY, by event kind, which leaves every existing frame byte-identical and both pins green. The round map is split accordingly and `.agent/plan.md` carries the risk.

ALTERNATIVES CONSIDERED. Route through `append_run_event` and normalise the job id to a UUID first: rejected, it would invent an identity the rest of the run log does not use and would break the join with ping-pong's own events. Give each tick its own run id, as every other writer does: rejected, those writers are one-per-invocation while this one is one-per-safe-point, and the file count is unbounded in the length of the job. Emit the display sentence on the wire so the client needs no basis object: rejected by D1 already, and rejected again here because it would move copy into the backend. Widen `_safe_event_summary` unconditionally in this round: rejected, it turns an exact key-set pin and a golden byte stream red in the same commit as a new emitter, which would leave two independent changes sharing one red and no way to tell which caused it.

REVERSE IT by deleting the emitter, its call and the catalog key together — they are pinned equal and none can drift alone — which also reverses D1's clause (1). Rulings (2), (3) and (4) reverse independently of the writer choice in (1). The transport paragraph rules nothing yet; it records a measured gap and names the round that closes it.

## DECISION F022 D3 (2026-08-23) — the tick's figures cross the envelope, for that kind alone and through a whitelist

CONTEXT, measured by the reviewer at `9b854cf5` by applying this change end to end in a disposable worktree before this block was written. DECISION F022 D1 ruled the tick's payload and DECISION F022 D2 ruled its writer. Neither reached the transport, and the transport is where the payload stopped: `_safe_event_summary` at `packages/orchestration/ui_server.py` returns exactly `{seq, event, timestamp, outcome, task_id}` and drops the event's `metadata`, which is where every figure D1 rules lives. Until this round a client subscribing to the stream received `budget.tick` frames carrying no spend, no limit and no basis — a correct payload nobody could render.

CHOSEN (1), THE WIDENING IS CONDITIONAL ON THE EVENT KIND. The summary gains its extra key for `budget.tick` and for nothing else, so every other kind's frame is byte-identical to what it was. This is not caution for its own sake: `tests/ui_server/test_sse_stream.py` asserts the summary's key set with an exact set equality, and it pins a GOLDEN BYTE STREAM that it rebuilds from the frame writers rather than transcribing, so the golden cannot be edited into agreement without a code change. Measured: the key-set assertion feeds the summary an event named `x` and the golden's events are named `e0` and `e1`, so neither is a tick, and with the conditional widening applied both files stay green at 66 and 100 passed. An unconditional widening turns both red in the same commit as a new feature, which would leave two independent changes sharing one failure.

CHOSEN (2), THE PAYLOAD IS WHITELISTED KEY BY KEY, AT BOTH LEVELS. The `safe` in `_safe_event_summary` is load-bearing — it is a redaction boundary, and this repository carries a `redaction_patterns` module of forbidden field names and secret patterns because event metadata is not trusted input. Passing a tick's metadata through wholesale would make any key a run-log writer ever placed on a tick reachable by any stream subscriber. The outer fields D1 rules are copied by name, and the two keys inside `basis` are copied by name as well, because a nested pass-through is the same leak one level down. Measured in the worktree: a plausible secret placed in a tick's metadata does not appear anywhere in the serialised summary, and neither does an unnamed key placed inside `basis`.

CHOSEN (3), AN ABSENT KEY STAYS ABSENT AND A MALFORMED TICK YIELDS AN EMPTY PAYLOAD. No default, no null and no zero is supplied for a limit the tick never carried, so the acceptance criterion that a limitless job never renders a fabricated denominator survives the last hop as well as the first. A tick with no metadata, or with metadata that is not a dict, produces an empty payload and raises nothing: the summary is built for every event on the stream and may not fail on one.

CHOSEN (4), NO CLIENT CHANGE THIS ROUND. The TypeScript envelope type and the COST metric that reads it are T002's work. Landing them here would put a UI slice in the same commit as a transport change and would mix the two rounds' evidence.

ALTERNATIVES CONSIDERED. Widen unconditionally and update the two pins: rejected under (1), and rejected more strongly because the golden exists to make a wire-format change a deliberate edit, so editing it to accommodate an incidental one is exactly the discipline it was built to enforce. Send the whole metadata dict for ticks only: rejected under (2) — the condition limits WHICH events leak, not WHAT leaks from them. Add a second endpoint for tick figures rather than widening the envelope: rejected, the summary's docstring records that the cursor endpoint and the SSE stream are one consumer contract over two transports with ONE writer, and a second endpoint would give the ticker a different resume story from the feed it rides beside. Have the client re-read the ledger for figures it saw a tick for: rejected, it turns one push into a poll and reintroduces the client-side arithmetic D1's clause four forbids.

REVERSE IT by deleting the conditional branch and its whitelist helper together; nothing else in the summary changes and every existing frame is already unaffected. Ruling (2) survives any reversal of (1) that keeps a payload at all, and rulings (3) and (4) are independent of both.

## DECISION F022 D4 (2026-08-23) — the client's cost reading: one denominator, one estimate marker, two thresholds, and no arithmetic beyond the ratio

CONTEXT, measured by the reviewer at `d97cdbb2`. DECISION F022 D1 ruled the tick's payload, D2 its writer and D3 its passage across the envelope. The figures now reach a client that has no vocabulary for them: `RemedyMetricKey` at `apps/ui/src/api/types.ts:3` is a closed union of seven strings and `RemedyMetric.value` is `number | "—"`, with `suffix` a display string, `tooltip` a `Record<string, number>`, `state` a three-value union and `unknown` a boolean — nowhere for a limit, a basis or a threshold. The feature file's Design and its Goal & Done also disagree on the surface: Design rules the fill against "the strongest configured limit (usd preferred when both)" while Done requires "the warn threshold triggers per tokens". Both are satisfiable at once, and this decision says how, so that no round has to guess.

CHOSEN (1), THE UNIT IS CHOSEN BY WHICH LIMIT EXISTS, USD FIRST. When `limit_usd` and `spent_usd` are both present the metric is in usd; otherwise when `limit_tokens` and `spent_tokens` are both present it is in tokens; otherwise there is no usable denominator and clause 3 applies. That is Design's "usd preferred when both" read as a statement about the LIMITS, and it satisfies Done's "warn threshold triggers per tokens" exactly, because a job configured with a token limit alone lands in the tokens unit and takes its threshold from the token fill. The denominator is ALWAYS the limit of the unit shown: the other unit's limit is never substituted, because a dollar spend over a token limit is a fabricated ratio wearing a real number's clothes.

CHOSEN (2), THE ESTIMATE MARKER READS THE BASIS OF THE FIGURE ACTUALLY SHOWN. A usd metric reads `basis.cost`, a tokens metric reads `basis.tokens`, and `estimated` is false ONLY for the exact string `"actual"`. `"lower_bound"`, `"absent"`, any unrecognised string and a missing or non-object `basis` all mark the figure estimated, because unknown provenance is not an actual and the `~` is cheap while a false claim of exactness is not. The tooltip text is composed in the client from that vocabulary; DECISION F022 D1 clause four already forbids a display sentence on the wire, and this decision does not reopen it.

CHOSEN (3), NO LIMIT MEANS NO DENOMINATOR ANYWHERE. A missing limit, a limit that is not a finite number, and a limit of zero all produce the spent-only variant: `fill` null, `level` null, `limitless` true, and no tooltip line naming a limit. A zero limit is included deliberately — it is the shape that would otherwise divide by zero and render `Infinity` as a fill — and the acceptance criterion is that a limitless job never renders a fabricated denominator, which is a statement about what the user SEES and therefore binds the tooltip as much as the bar.

CHOSEN (4), THE THRESHOLDS ARE ON THE RATIO AND THEY ARE TWO. `fill >= 1` is `"exceeded"`, `fill >= 0.85` is `"warn"`, anything less is `"normal"`, and `level` is null whenever `fill` is. The comparisons are inclusive at both boundaries so that exactly 85% warns and exactly 100% is exceeded; a bar that waited for 85.1% would tell the truth late, and the budget stop the feature file mentions lands moments after 100% either way.

CHOSEN (5), THE ONLY ARITHMETIC IS THE RATIO AND ONE PERCENTAGE OF IT. `costMetricOf` divides spend by limit and multiplies that ratio by 100 for the tooltip's percentage, and does nothing else numeric. It never sums figures, never converts tokens to money, never applies a rate and never carries a price constant — the backend is the single arithmetic home and this is the whole of the client's share. The permitted numeric literals are therefore `0`, `1`, `100`, `0.85`, and the formatting constants `2`, `1000` and `1000000`; the test file's source guard enumerates exactly those.

ALTERNATIVES CONSIDERED. Compute the render decisions inside `TopMetricsBar.tsx`: rejected — the vitest config collects `src/**/*.test.ts` under a node environment, so a rule that lived in the component would ship with no test that can reach it, and F021 already established the pure-module shape for exactly this reason. Show the TIGHTEST fill across both limits rather than preferring usd: rejected, because "tightest" changes unit mid-run as spending moves and a metric whose unit flickers is worse than one that is merely conservative; the tooltip enumerates both fills, so nothing is hidden. Let an absent limit fall back to the other unit's limit: rejected under clause 1. Emit the composed tooltip strings from the backend: rejected, it reopens D1 clause four and puts display copy in the ledger.

REVERSE IT by deleting `apps/ui/src/api/costMetric.ts` with its test file and narrowing `RemedyMetricKey` back to seven strings; nothing else reads either. Clauses 1 to 4 are independent of each other and any one can be re-ruled alone, while clause 5 is a consequence of the no-client-arithmetic rule the feature file's Acceptance section already binds and cannot be reversed here.

## DECISION F022 D5 (2026-08-23) — the COST metric is drawn from the view and decides nothing, and its threshold is never colour alone

CONTEXT, measured by the reviewer at `142af5e4`. DECISION F022 D4 put every render decision into `costMetricOf`, and nothing draws them. `TopMetricsBar.tsx` is generic over the array it is handed, hardcodes no metric list and falls back to `ChartGlyph` for an unknown key, so an eighth metric already renders; what it cannot do is show a formatted string, a prefix, a limit-relative fill or a threshold. Three of this repository's own authorities bear on how it should: `docs/ui/design_reference/ux_spec.md` §10 specifies the metrics bar's track as 6px, radius 3, `--remedy-blue-100` base with a 350ms width transition, `docs/ui/design_reference/assets_spec.md` line 179 already specifies the budget/cost glyph as a coin — circle plus inner cent-bar, stroke, 16 DOM — with a warn tint at or above 85 per cent of budget, and §14 of the same spec rules that a state change is never colour alone.

CHOSEN (1), THE COMPONENT IS A FIELD LOOKUP AND ITS ONLY ARITHMETIC IS THE CLAMP. Every branch reads a field of `CostMetricView`: `display` for the value, `estimated` for the marker, `fill` for the track's width, `level` for its treatment, `tooltip` for the rows. The component formats nothing, chooses no unit, picks no denominator and composes no sentence. The one number it computes is the track's width — an already-computed ratio expressed as a percentage and clamped into the track — because a fill over 100 per cent must render as a full bar rather than overflow its container. Where the render appears to need a value the view does not carry, that is the view's gap and it is a finding, never a computation moved back into the component.

CHOSEN (2), THE EIGHTH SEGMENT IS ADDED AND THE DEVIATION IS RECORDED HERE. `ux_spec.md` §10 opens "One hero glass card; 4 segments" while the shipped bar renders seven, so the built state already departs from that count and this round makes it eight. The departure is deliberate and pre-existing: the four-segment sentence describes an earlier composition, while the same section's binding rules — the divider, the icon disc, the kicker, the 30/700 value, the track, the honest em dash — are followed exactly by every segment including this one. THE ROUTE FOR THIS RECORD IS ITSELF THE POINT: the feature file's header orders visual deviations into an `assumption_log`, and finding R-0665 measured that no such file exists anywhere in this repository while seventy-six tracked documents name it — re-measured at `142af5e4`, where `git ls-tree -r --name-only` matches no path containing `assumption` and `git grep -l assumption_log -- docs/` still returns seventy-six. F022 therefore records its visual deviations as DECISIONs in `.agent/decisions.md`, which is the operative decision record this workflow actually reads, and says so rather than writing to a file that is not there. R-0665 stays OPEN; this is a route, not its fix.

CHOSEN (3), THE THRESHOLD IS NEVER COLOUR ALONE. `ux_spec.md` §14 rules that a state change never happens by colour only, and a money bar is the worst place to break that: the reader who cannot distinguish the warn tint from the normal one is exactly the reader a budget warning is for. At `warn` and at `exceeded` the metric therefore carries the level in its ACCESSIBLE NAME in words, and the track carries a non-colour signal of its own beside the tint. The estimate marker is a separate channel from the threshold and the two may never be driven from one another: a `~` that appeared at 85 per cent would claim the figure had become an estimate, which is a false statement about provenance rather than a loud one about spend.

CHOSEN (4), THE TINTS COME FROM THE PRIMITIVES BOTH SHEETS ALREADY CARRY. `--remedy-orange-400` at `warn` and `--remedy-red-500` at `exceeded`, each defined exactly once in `apps/ui/src/styles/tokens.css` and exactly once in `docs/ui/design_reference/tokens.css` — measured, because those two sheets are known to disagree elsewhere and finding R-0661 is what that costs. No new token is minted, no literal hex enters a cost rule, and `assets_spec.md` needs no amendment because the glyph this round draws is one it already specifies.

CHOSEN (5), THE COST TRACK FOLLOWS THE SPEC AND THE PROGRESS TRACK IS LEFT ALONE. The new track is 6px at radius 3 over `--remedy-blue-100` with a 350ms transition, as §10 rules. The neighbouring `.progressTrack` is 5px over an rgba base at 600ms and predates that sentence; it is out of this feature's scope and MetricsBar's other metrics are on its Do-not-touch list, so the two will differ on disk until a round owns that file for its own reasons. Saying so here is cheaper than a reader discovering it and assuming one of them is a typo.

CORRECTION TO DECISION F022 D4, appended here because §3 checklist item 20 forbids rewriting a landed paragraph. D4's REVERSE clause names deleting `costMetric.ts` with its test file and narrowing `RemedyMetricKey`, and adds "nothing else reads either". That is incomplete and the completed form is: also remove the optional `cost?: CostMetricView` field from `RemedyMetric` and the `import type { CostMetricView } from "./costMetric";` line above it in `apps/ui/src/api/types.ts`, without which the reversal leaves an import of a deleted module and `npm run typecheck` goes red. Registered as finding R-0672.

ALTERNATIVES CONSIDERED. Give the threshold its own token pair rather than reusing the primitives: rejected, a token minted for one metric is a token the reference does not carry, which is the R-0661 divergence created deliberately instead of inherited. Signal the threshold by colour alone and rely on the tooltip: rejected under clause 3 — a tooltip is a hover, and a state a keyboard reader cannot reach is a state it does not have. Reuse `.progressTrack` for the cost fill: rejected under clause 5, since the two specs differ and sharing the rule would silently migrate the progress metric's appearance inside a cost feature. Put the formatting in the component and keep the module pure of strings: rejected under clause 1 and D4 clause 5, because the format is part of what "renders honestly" means — `"—"` versus `"$0.00"` is the whole of the no-fake-zeros rule.

REVERSE IT by deleting the cost rules from `TopMetricsBar.module.css`, the cost branches from `TopMetricsBar.tsx`, `CoinGlyph` from `RemedyGlyphs.tsx` and `tests/ui_contracts/test_cost_metric_render.py` entirely, and by dropping the goldens describe block from `costMetric.test.ts`. That is the whole of this round's production surface and it is stated here as a complete list, which is the obligation R-0672 exists to remember.

## DECISION F022 D6 — where the live tick is held, and how it reaches the bar

CONTEXT. `costMetricOf` has been correct since R7 and drawn since R8 and has no
production caller: measured at `a8952614` by reading every `.ts` and `.tsx`
under `apps/ui/src` except `*.test.ts` and `*.test.tsx`, the only non-test file
containing `costMetricOf(` is `costMetric.ts` itself. The tick reaches the
client already — `_safe_event_summary` puts a `budget` key on a `budget.tick`
frame and on no other kind — and nothing reads it.

CHOSEN. The latest tick's figures are held as ONE field on `BrainStreamState`,
folded in `receiveBrainFrame` behind the replay guard, carried forward BY
REFERENCE on every non-tick frame, published on `BrainStreamView` and compared
there with `===`. The shell composes the bar's metrics through one pure
function, `metricsWithCostTicker`, which calls `costMetricOf` and decides
nothing else.

WHY. `receiveBrainFrame` is the single ingest point every frame passes through
and the only place a reconnect replay has already been ruled on, so a fold there
inherits the replay guard instead of re-deriving it. Reference-carrying is not
an optimisation: the runner's `publish` compares with `===`, so a fresh object
of equal content would announce a change nobody made and re-render the cockpit
on every heartbeat. A pure composition function keeps the wiring under the
node-environment vitest, which cannot render React — the same reason
`cockpitLogic.ts` and `brainStream.ts` were extracted from their components.

ALTERNATIVES CONSIDERED. A second store subscribed to the same stream: rejected,
because `tests/ui_contracts/test_brain_stream_ring.py` pins exactly one
`useBrainStream(` call site and a second subscription is a second socket.
Deriving the figures inside `TopMetricsBar` from the feed ring: rejected,
because `FeedRow` deliberately drops the `budget` payload and widening it would
put the whole envelope behind a projection built for a feed. Fetching the
figures over the dashboard endpoint: rejected, because a ticker that polls is
not live and the transport already carries the value.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. Delete `apps/ui/src/api/budgetTick.ts` and
`apps/ui/src/api/budgetTick.test.ts`; delete `apps/ui/src/api/costTicker.ts` and
`apps/ui/src/api/costTicker.test.ts`; in `apps/ui/src/api/brainStream.ts` remove
the `budget` field from `BrainStreamState`, its `null` seed in
`initialBrainStreamState` and the fold in `receiveBrainFrame`; in
`apps/ui/src/api/brainStreamRunner.ts` remove the `budget` field from
`BrainStreamView`, its seed in `cachedView` and its comparison in `publish`; in
`apps/ui/src/api/remedyApi.ts` remove the eighth `cost` entry from the `metrics`
literal and the deliberate-absence comment in `normalizeApiFailure`; in
`apps/ui/src/components/shell/RemedyShell.tsx` pass `dashboard.metrics` to
`TopMetricsBar` unwrapped; drop the budget cases from
`apps/ui/src/api/brainStream.test.ts` and
`apps/ui/src/api/brainStreamRunner.test.ts`, and restore the seven-key
assertions and the original test name in `apps/ui/src/api/remedyApi.test.ts`;
remove the wiring class from `tests/ui_contracts/test_cost_metric_render.py`.
The R-0671 assertion in `apps/ui/src/api/costMetric.test.ts` is NOT part of this
decision and a reversal keeps it. That is every production and test path this
round's Change set holds, which is what R-0672 and its recurrence require of a
reversal instruction and what DECISION F022 D5 did not do.

## DECISION F022 D7 — the source of the terminal reconciliation's ledger figure

CONTEXT. `docs/roadmap/features/T5_F022.md` orders the terminal reconciliation
to "fetch the ledger's job figure (the stats endpoint)". Measured at `3e1d3fae`:
`packages/orchestration/ui_server.py` dispatches its job endpoints from one
`handlers` dict plus `events-since`, and no `stats` endpoint is among them. The
spec names a source that has never existed, so T003b could not be built as
written.

REJECTED, and this is the substantive half of the ruling. The dashboard payload
already carries `token_usage`, which reads like the ledger figure. It is not
one. `_build_token_usage` sums `metadata.estimated_tokens` across the job's
events and returns `"estimated": True` with `"source": "event_metadata"`,
attributing tokens to `context`, `memory`, `repair`, `planner` and `other` from
kinds such as `source_context_injected` and `project_memory_recalled`. The
ticker's figures are `BudgetCounters.measured_token_total` and
`measured_cost_usd`, which count PROVIDER CALLS. The two populations are
disjoint in intent and in practice, so a delta between them measures neither
drift nor drop — it measures the difference between two unrelated questions.
Rendering it under the words "final (ledger)" would be the fabricated honesty
moment this feature exists to prevent, and it would be indistinguishable on
screen from a real one.

CHOSEN. The ledger figure is the LAST `budget.tick` in the job's run log.
`_emit_budget_tick` writes every tick through `RunLogWriter` under the stable
run id `budget-ticks`, so that log is the ledger's own record of the final
measured figures, already in the whitelisted shape
`_budget_tick_summary_payload` puts on the wire. The server exposes it as a
final-figure section; the client renders it at terminal in place of the live
value.

CONSEQUENTLY THE DELTA IS A TRANSPORT STATEMENT, never a second arithmetic. Both
sides of the comparison are the SAME quantity from the same producer: what the
client received over the stream, against what the ledger holds. A delta
therefore means frames were missed — an SSE gap, a disconnect, a ring overflow,
or a final tick emitted after the client stopped listening — which is exactly
what a reader deserves to be told, and it is measurable rather than guessed. The
client still performs no money arithmetic: it compares two figures the backend
produced and labels the difference.

ALTERNATIVES CONSIDERED. Adding the `stats` endpoint the spec names: rejected,
because it would be a new public surface invented to satisfy a sentence rather
than a need, and the figures already exist. Treating the last tick the CLIENT
holds as final: rejected, because it makes the reconciliation vacuous — the
client would compare a value with itself and could never show a delta, which is
the R-0438 vacuous-gate shape arriving in a feature. Recomputing the final
figure from the event stream in the client: rejected, because the UI never
computes money, which is this feature's founding constraint.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. In `docs/roadmap/features/T5_F022.md` restore the
Terminal-reconciliation bullet's previous wording, which named the stats
endpoint and which this round's C5 replaced whole. In `.agent/live_review.md`
nothing is reversed, because the map repair at C2 and the ledger entry at C3
record round history rather than this decision. This decision ships no code, so
no production path is reversed here; a later round that builds against it
reverses its own paths under its own decision. That is every path this round's
Change set holds, which is what R-0672 and its recurrence require of a reversal
instruction.

## DECISION F022 D8 — when the ledger figure replaces the live one, and what the delta says

CONTEXT. DECISION F022 D7 ruled the SOURCE of the terminal reconciliation: the
last `budget.tick` in the job's run log, served as the dashboard's
`budget_final`. It deliberately ruled nothing about WHEN the client swaps the
live value for that one, nor about what counts as a delta worth showing, because
no client code existed to rule over. Measured at `5d3e6045`: the shell holds the
latest received tick on `stream.budget` and hands it to the bar through
`metricsWithCostTicker`, while `budget_final` reaches the payload and has NO
client reader at all — the dashboard type does not name it.

CHOSEN, clause by clause.

1. THE TRIGGER is terminal AND a ledger figure: the reconciliation runs exactly
when the dashboard's `live.running` is false and the ledger figure is not null.
While the job runs, the ledger's last tick and the client's last tick are the
same event, so rendering one as "final" would claim a finality the run has not
earned — and it would do so in the feature built to stop exactly that.

2. THE FIGURE SHOWN IS THE LEDGER'S, and it is rendered through `costMetricOf`
like any other tick. The reconciliation module chooses no unit, no denominator,
no marker and no threshold; it hands the ledger payload to the module that
already owns those rules. This is what keeps the arithmetic home single, and
`tests/ui_contracts/test_cost_metric_render.py` enforces it independently, as
measured at `5d3e6045`.

3. THE DELTA IS LABELLED WHEN THE DISPLAYS DIFFER, and it is named rather than
computed. The comparison is between the ledger view's `display` string and the
received view's `display` string. Comparing the DISPLAYS rather than the raw
figures is the deliberate half: both sides are the same producer's counters, so
a real missed frame moves the shown value, while a difference below the display
precision would render as a label naming two identical figures — a sentence that
contradicts itself on the reader's screen and teaches them to ignore the next
one. ACCEPTED COST, stated rather than hidden: a transport gap smaller than two
decimal places, or smaller than the token formatter's own rounding, is not
surfaced. The figure shown is the ledger's and therefore correct either way;
what is lost is only the notice, and a notice nobody can verify against the
screen is worth less than the trust it spends.

4. AN ABSENT SIDE IS ABSENT. No received figure at terminal renders the ledger
figure with NO label, because a label naming an em dash as the live estimate
would invent a reading the client never took. No ledger figure changes nothing
at all and the live tile stands, which is the same honesty rule that stops a
limitless job fabricating a denominator.

ALTERNATIVES CONSIDERED. Comparing the raw figures: rejected for the
self-contradicting on-screen label clause 3 describes. Reconciling whenever a
ledger figure exists, without the running check: rejected because it claims
finality mid-run. Rendering the difference itself as a magnitude: rejected twice
over, because the feature file's own wording names both values rather than their
difference, and a magnitude is the second arithmetic D7's closing clause forbids
the client. Holding the reconciliation in `costTicker.ts` instead of a new
module: rejected because that module's contract is the LIVE tick, and a second
responsibility there would put the terminal rules where nobody searching for
them would look.

REVERSE IT path by path, derived from this round's Change set rather than from
the files most in mind. Delete `apps/ui/src/api/costReconciliation.ts` and
`apps/ui/src/api/costReconciliation.test.ts`. In `apps/ui/src/api/types.ts`
remove `budgetFinal` from `RemedyDashboard` and `costFinalNote` from
`RemedyMetric`. In `apps/ui/src/api/remedyApi.ts` remove the `budget_final`
mapping, and in `apps/ui/src/api/remedyApi.test.ts` its three cases. In
`apps/ui/src/components/shell/RemedyShell.tsx` unwrap the call so
`metricsWithCostTicker(dashboard.metrics, stream.budget)` is again the whole
argument. In `apps/ui/src/components/metrics/TopMetricsBar.tsx` remove the note
render, and in `tests/ui_contracts/test_cost_metric_render.py` the class that
pins it. In `.agent/plan.md` and `.agent/live_review.md` nothing is reversed:
those record round history rather than this decision. That is every path this
round's Change set holds, which is what R-0672 and its recurrence require of a
reversal instruction.

## DECISION amend0825 D1 (2026-08-25) — the job-less run answers only the budget

The bare `remedy do run` ping-pong path evaluates the BUDGET GUARD directly at
its safe point instead of calling `safe_points.should_stop`, and asks the
operator-stop layer nothing at all.

WHY. `should_stop`'s first act is the operator-stop lookup, which is addressed
by job id: `remedy job stop <id>` writes a request under
`<data_root>/control/<job-id>/`. This path mints no job, persists no job record
and prints no id, so an operator has no target to name and the run has nothing
to look up. The reviewed build asked anyway with a hardcoded `""`, and
`validate_job_id` correctly refused it, so every budgeted `remedy do run` died
with `StopControlError: invalid job id ''` before the first provider call.

ALTERNATIVES CONSIDERED. Minting a real job id for this path and threading it
through: rejected for this round — it makes the job-less path a job path, which
is a behaviour change to what `remedy do run` IS, not a repair of a crash, and
`remedy do job-run` already exists for operators who want a stoppable run.
Weakening `validate_job_id` to accept an empty id: rejected outright, and the
operator order forbids it; the id rule is what keeps a control path off
`<control>/` root. Emitting a budget tick anyway: rejected, because a tick is
filed under `<data_root>/runs/<job-id>/` and there is no id to file it under —
the F022 ticker has nothing to attach to on a run with no job.

CONSEQUENCE. A budgeted `remedy do run` cannot be stopped by an operator
mid-run; it can only be stopped by its budget or by the terminal. That is not
new — no such stop ever worked on this path — but it is now the deliberate,
documented shape rather than a crash that hid the question.

REVERSE IT by restoring the `should_stop` call in `_cmd_do_pingpong._stop_check`
in `apps/cli/commands/do_cmd.py` together with the `operator` branch it had, and
deleting `tests/cli/test_do_cmd_pingpong_budget.py`'s two budget classes. The
crash returns with it.

## DECISION amend0825 D2 (2026-08-25) — a second resolver, not a widened one

`data_paths.resolve_job_id` is unchanged and still searches the classic store
only; the new `resolve_any_job_id` searches both stores and returns a `str`.

WHY. `resolve_job_id` returns a `UUID`, and a task-job id is `uuid4().hex[:16]`
— sixteen hex characters, which `UUID()` rejects. Widening the function
therefore means changing its return type, and thirty call sites across
`apps/cli/commands/` consume it. The two stores mint different id shapes, so
one function that returns a `UUID` is CORRECT for the store it searches; the
honest fix is a second function whose signature says it covers both.

ALTERNATIVES CONSIDERED. Changing `resolve_job_id` to return `str`: rejected on
blast radius, and because it would silently strip the parse guarantee its
existing callers rely on. Teaching `teach_cmd` to try one resolver and then the
other: rejected because `resolve_job_id` exits the process on no match, so the
second attempt is unreachable. Making the task-job store's ids UUIDs: rejected
as a data migration far outside this order.

CONSEQUENCE. Two resolvers exist and a reader must pick. The docstrings state
which store each covers and the module's Public API block lists both with that
distinction, which is the counter-measure.

REVERSE IT by deleting `resolve_any_job_id`, `task_jobs_dir`,
`_classic_job_id_matches`, `_task_job_id_matches` and `_exit_ambiguous` from
`packages/orchestration/data_paths.py` and restoring the inlined body of
`resolve_job_id`; restoring the two `resolve_job_id` call sites in
`apps/cli/commands/teach_cmd.py` and its exit-code docstring paragraph;
restoring the literal `resolve_data_root() / "task_jobs"` in
`packages/orchestration/pingpong_job.py:_jobs_dir`; and deleting
`TestTeachReachesTaskJobs` from `tests/cli/test_teach_cmd.py`.

## DECISION amend0825 D3 (2026-08-25) — the doctor's fixtures read the live table

`tests/cli/test_worker_facade_cmd.py` derives its dead-model fixture id from
`MODEL_ALIASES` via `a_builtin_model_id()` instead of spelling one.

WHY. Eight tests spelled `claude-opus-4-20250514` to make the doctor warn about
a built-in default. The 2026-08-25 repoint moved the table off that string, and
all eight became vacuous in the same instant: they declared a string dead that
no alias pointed at any more, so no warning fired and the assertions failed on
an empty list. A fixture that names what it is testing ABOUT must read it from
the thing under test, or the next repoint silently repeats this.

CONSEQUENCE. These tests now depend on `claude-flagship` existing in the table.
That is a weaker coupling than the id, and `test_every_alias_resolves_to_a_
non_empty_id` already pins it.

REVERSE IT by deleting `a_builtin_model_id` from
`tests/cli/test_worker_facade_cmd.py` and putting the current
`resolve_model_alias("claude-flagship")` value back at its nine call sites.
