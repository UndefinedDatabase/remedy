# F031 Inventory — the decision inbox as the source has it today

> MEASURED, not recalled. Every answer below was produced by a command run
> against the working tree at the round base named in `.agent/handoff.md`, and
> every answer names the file and the SYMBOL it was read from rather than a bare
> line number. Where a thing does not exist, the answer says so and names the
> command whose empty output proves it. This file is state, not documentation:
> it is superseded by the T-slices it exists to plan.

## Q1 — the queue store
Which module owns the decision queue, is it file-based, and what is its public
read surface?
ANSWER: `packages/orchestration/decision_queue.py` owns it, and it is NOT
file-based. The module does no I/O of any kind: grepping it for the literals
open-paren, Path-paren and dunder-all prints nothing, and its own module
docstring calls the queue "a read-only aggregation" and "Not a second source of
truth". `list_decisions` re-derives every item on each call from an
already-loaded job object plus its event list. Durability lives upstream, not
here: `enqueue_task_decision` in `packages/orchestration/escalation.py` stores
task-decision records on the job under `JOB_METADATA_ESCALATIONS_KEY`, and
`save_job` in `packages/orchestration/storage.py` writes the job. The public
read surface is the ten names the module docstring's `Public API` block lists,
each of them defined in that same file: `HumanDecision`, `list_decisions`,
`get_decision`, `explain_decisions`, `export_decision_json`,
`build_decision_summary`, `sort_open_decisions_first`, `open_decisions`,
`render_open_decisions_lines` and `open_decisions_next_action`. The module
declares no dunder-all — same grep, no hit.

## Q2 — the decision types
What is the exact set of decision types the queue recognises, where is it
defined, and how many members does it have?
ANSWER: `DECISION_TYPES`, a frozenset in
`packages/orchestration/decision_queue.py`. Importing it in a one-line Python
command and printing its length and its sorted members gives 10:
`flight_plan_approval`, `memory_review`, `patch_approval`, `repo_dirty`,
`revert_missing`, `stop_reason`, `task_decision`, `test_failure`,
`token_budget` and `worker_approval`. The most recently added is
`task_decision`, held a second time as `DECISION_TYPE_TASK_DECISION` in
`packages/orchestration/escalation.py`. The set is advisory rather than
enforced: the `type` field of `HumanDecision` is annotated plain `str`, and a
repository-wide grep for `DECISION_TYPES` over Python sources finds importers
only under `tests/` — no production module reads it.

## Q3 — the producers
Which call sites actually WRITE a decision into the queue, and which of the Q2
types does each produce?
ANSWER: There is no external writer. Every decision is constructed inside
`list_decisions` in `packages/orchestration/decision_queue.py`: a
repository-wide grep over Python sources for the constructor call `HumanDecision`
followed by an open paren finds production hits in that one module and nowhere
else under `packages/` or `apps/`, and counting them in that file gives 9 —
nine constructions across the eight numbered branches of that one function,
because the flight-plan branch builds either an open or a resolved card. Branch
by branch, with the upstream symbol each reads and the Q2 type it emits:
`list_patch_intents` with `APPROVAL_PENDING` from
`packages/orchestration/approval_queue.py` gives `patch_approval`;
`derive_stop_reasons` from `packages/orchestration/stop_reasons.py` gives
`stop_reason`; the `test_run_completed` events whose metadata status is failed,
last three only, give `test_failure`; the last `git_status_read` event when its
metadata is dirty gives `repo_dirty`; the job's budget stop fields or a
`job_stopped` event whose metadata source is budget give `token_budget`;
`list_memory` from `packages/memory/local_gateway.py`, stale or needs_review,
first five, gives `memory_review`; the job's flight-plan approval marker with
`open_clarification_questions` from `packages/orchestration/flight_plan.py`
gives `flight_plan_approval`, once open and once resolved; and
`escalation_records` from `packages/orchestration/escalation.py` gives
`task_decision`. Two Q2 types have NO producer: `worker_approval` and
`revert_missing`. Proof: a repository-wide grep over Python sources for either
name returns exactly one line, the `DECISION_TYPES` declaration itself.

## Q4 — the CLI surface
What decision commands exist, what are their command ids, and which module
implements them?
ANSWER: Four, all in the `decision` group. Grepping
`apps/cli/command_catalog.py` for the anchored literal command-id assignment
prefixed `decision.` prints exactly `decision.list`, `decision.show`,
`decision.resolve` and `decision.explain`; their `CommandEntry` action classes
are `read_only`, `read_only`, `write_metadata` and `read_only`. They are
implemented in `apps/cli/commands/decision.py`, whose `COMMAND_HANDLERS` maps
those same four ids to `_cmd_decision_list`, `_cmd_decision_show`,
`_cmd_decision_resolve` and `_cmd_decision_explain`. `_cmd_decision_resolve`
dispatches on the decision id's prefix: `sr:` to `resolve_stop_reason`, the
`_ESCALATION_PREFIX` value `td:` to `answer_task_decision` plus `save_job`, and
`fp:` to `resolve_flight_plan_approval`; every other id is refused with the
message that it "is derived and cannot be directly resolved".

## Q5 — the blocked-subtree computation
Which symbol computes what a waiting task blocks downstream, in which module,
and what does it take and return?
ANSWER: `blocked_downstream` in `packages/orchestration/dag_schedule.py`,
named in that module's export list. It takes a sequence of `Task` and an
iterable of seed `UUID` values and returns a set of `UUID`: the transitive
dependents of the seeds, with the seeds themselves excluded and any COMPLETED
task excluded, walking the edges that `build_graph` in the same module resolves.
Grepping for the symbol across `packages/` and `apps/` gives its production call
sites: `ready_tasks` and `skipped_blocked_tasks` in
`packages/orchestration/long_run_executor.py` — `awaiting_downstream_tasks` in
that same file reaches it by delegating to `skipped_blocked_tasks` — and
`execute_mission_followup` in `packages/orchestration/mission_state.py`. NONE of
them is the decision queue: that same grep returns no hit in
`packages/orchestration/decision_queue.py`, so no `HumanDecision` field carries
a blocked-subtree size today. The math F031 needs exists; the wiring from it to
a decision does not.

## Q6 — the decision event kinds
Does the event stream carry a decision-requested or decision-resolved event kind
today, on the Python side and in the TypeScript humanize catalog? Name the
search you ran and its result on each side.
ANSWER: No, on both sides, for the kinds the feature file names. A
repository-wide grep over Python sources for the four-way alternation of
`decision.requested`, `decision_requested`, `decision.resolved` and
`decision_resolved` returns no hit for any requested/resolved kind of those
spellings; its only hits carry the differently-named kind
`human_decision_requested`. Grepping repo-wide over Python and TypeScript
sources for `human_decision_requested` or `human_decision_resolved` returns 7
lines in 3 files, and NOT ONE OF THEM IS AN EMITTER:
`packages/orchestration/project_summary.py` filters on it;
`packages/orchestration/ui_server.py` holds it as a key in two actor maps and in
the timeline-label map that `_build_timeline_events` reads, and counts it in
`_build_dashboard` and in `_build_live_state_json`; the seventh line is an
inline fixture in `tests/ui_server/test_dashboard_truth_v3.py`.
`human_decision_resolved` has zero hits — that kind does not exist at all. The
requested kind is likewise absent from
`packages/orchestration/event_schemas.py`, where a case-insensitive grep for
"decision" prints only `agent_loop_cycle_decision` and the payload field names
`decision` and `final_decision`. TypeScript side: grepping
`apps/ui/src/api/humanizeCatalog.ts` for "decision" prints exactly two catalog
entries, `agent_loop_cycle_decision` and `contract_decision`, neither of which
is a requested/resolved kind, and grepping `apps/ui/src` for `human_decision`
prints nothing. The strings `decision.requested` and `decision.resolved` exist
in this repository only inside `docs/roadmap/features/T5_F031.md`.

## Q7 — the write channel
Is there already a write-channel command that resolves a decision? Name the
command id, the constant that holds it, and the dispatch symbol.
ANSWER: Yes, and it is already live. The command id is `decision.resolve`,
held by the constant `DECISION_RESOLVE_COMMAND_ID` in
`packages/orchestration/ui_server.py`, and it is one of exactly two members of
`UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` — the other is
`job.stop`, so this id is half the browser-reachable write surface. The dispatch
symbol is `_dispatch_decision_resolve`, a method of `_RemedyHandler` in
`packages/orchestration/ui_server.py`, reached from that class's
`_handle_command_submission`. Its effect is `answer_task_decision` from
`packages/orchestration/escalation.py` followed by `save_job` from
`packages/orchestration/storage.py`; a `None` return means the decision is
absent or no longer open, and the caller answers 409 carrying
`COMMAND_DECISION_STATE_MESSAGE`. Scope worth naming for F031: that effect
resolves task decisions ONLY, because `answer_task_decision` looks its record up
through `find_task_decision` over the escalation records — the CLI's `sr:` and
`fp:` branches have no counterpart in this module.

## Q8 — the UI today
Does any inbox or decision component exist under `apps/ui/src`? Name the search
and its result.
ANSWER: No. A case-insensitive grep of `apps/ui/src` for "inbox" prints 0
lines — there is no inbox component, module or identifier of any casing in the
UI source. There is no decision component either: the closest surfaces are
`apps/ui/src/components/panels/NeedsAttentionCard.tsx`, whose heading reads
"Needs your decision" but whose only body copy is "A patch is waiting for
approval before it can be applied.", and the matching "Needs your decision"
status string in `apps/ui/src/cockpitLogic.ts` — both are patch-approval, and
neither reads the decision queue. Nothing could read it anyway: in
`packages/orchestration/ui_server.py`, the `do_GET` method of `_RemedyHandler`
has four route predicates, and its per-job endpoint table is a 13-key `handlers`
map whose keys are dashboard, brain, brain-view-model, live-state,
task-progress, next-action, guide, events, readiness, context-budget, story,
checklist and diagnostics — there is no decisions endpoint. What the UI gets
today is the two integer counters built on the dead event kind in Q6.

## Q9 — the dependencies
F031 depends on F009, F050 and F051. For each, give the STATUS mark and the one
thing it left behind that F031 will build on.
ANSWER: Read from `docs/roadmap/STATUS.md` at the base by grepping it for
the three feature ids. F009 — the single write channel — is marked `[x]`,
accepted 2026-08-22, and leaves behind the POST write door:
`_handle_command_submission` and `DECISION_RESOLVE_COMMAND_ID` in
`packages/orchestration/ui_server.py` together with `UI_EXPOSED_COMMANDS` in
`apps/cli/command_catalog.py`, so a card's answer path already exists and is
already the UI's only write. F050 — DAG scheduling — is marked `[x]`, accepted
2026-07-30, and leaves behind `packages/orchestration/dag_schedule.py`, whose
`blocked_downstream` is exactly the blocked-subtree math an inbox card's size
field needs (Q5). F051 — escalate instead of block — is marked `[x]`, accepted
2026-07-30, and leaves behind `packages/orchestration/escalation.py` with
`enqueue_task_decision`, `answer_task_decision` and
`awaiting_decision_task_ids`, the `task_decision` member of `DECISION_TYPES`,
and the branch-only pausing in `ready_tasks` in
`packages/orchestration/long_run_executor.py`, which withholds an awaiting task
and its downstream while independent branches keep running.

## Observations
Defects or surprises found while measuring, each with its measurement. No
finding id is minted here (block constraint 8); the reviewer rules these.
ANSWER: Six, each with the measurement that produced it.
(1) THE QUEUE IS NOT FILE-BASED, which contradicts this round's own step block
and the C1 plan text, both of which say "the file-based decision queue".
Measurement: grepping `packages/orchestration/decision_queue.py` for
open-paren, Path-paren and dunder-all prints nothing, and the module docstring
says "a read-only aggregation". No file holds a queue; the job record holds the
records the queue derives from.
(2) `human_decision_requested` IS READ BUT NEVER WRITTEN. Measurement: the
repo-wide grep in Q6 returns 7 lines in 3 files, 6 of them readers and 1 a test
fixture; no production module emits it, and it is absent from
`packages/orchestration/event_schemas.py`. Consequence read straight off the
source: `decision_count` in `_build_dashboard` and the `open_decisions` sum in
`_build_live_state_json`, both in `packages/orchestration/ui_server.py`, count a
predicate no producer can satisfy, so both are always 0 in production. The badge
F031 exists to drive is currently a constant zero.
(3) `human_decision_resolved` DOES NOT EXIST — zero hits in that same grep — so
the resolved half of the pair has no kind at all, not even a dead one.
(4) TWO DECLARED DECISION TYPES ARE DEAD. `worker_approval` and
`revert_missing` each occur exactly once in the whole Python source, on the
`DECISION_TYPES` line that declares them, so they are neither produced nor
consumed.
(5) `DECISION_TYPES` CONSTRAINS NOTHING. The `type` field of `HumanDecision` is
annotated `str`, and the repository-wide grep for `DECISION_TYPES` over Python
sources finds importers only under `tests/`, so a producer emitting an unlisted
type would not be caught anywhere.
(6) A COMMENT DESCRIBES A ROUTE THE WRITE DOOR DOES NOT IMPLEMENT. The comment
above `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` says plan approval
"arrives here as `decision.resolve` carrying an `fp:`-prefixed decision id",
but grepping `packages/orchestration/ui_server.py` for the literal `fp:` prints
nothing, and `_dispatch_decision_resolve` calls only `answer_task_decision`,
which resolves escalation records through `find_task_decision`. An `fp:` id sent
to that door therefore returns None and is answered 409 rather than approving a
plan. Recorded as measured, not ruled.
