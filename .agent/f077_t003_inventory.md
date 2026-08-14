# F077 T003 — inventory of the manual CLI, the `resume` verb and the report

> READ-ONLY. Nothing under `packages/`, `apps/`, `tests/` or `docs/` changes
> because of this file, and no part of T003 is built here. Defects found are
> written down, not repaired.
>
> **Line numbers are deliberately omitted** (R-0353, the same rule the T002
> inventory follows). Every answer names a FILE and a SYMBOL, because a symbol
> survives an edit above it and a line number does not. Every NUMBER carries the
> command that produced it. Quotes are verbatim from disk at `a9ebc920`.
>
> Where the R13 block states a fact, it was treated as a claim to CHECK. Three
> of its claims are wrong and are corrected in Q2, Q3 and Q5/Q8 below.

## Q1 — how a mission verb is wired, end to end

### The traced path: `remedy mission ledger <id>`

| Step | File | Symbol |
|---|---|---|
| 1 | `apps/cli/grouped.py` | `main` |
| 2 | `apps/cli/grouped.py` | `build_parser` |
| 3 | `apps/cli/command_catalog.py` | `GROUPS["mission"]` (`GroupDef`, `user_facing=False`) |
| 4 | `apps/cli/command_catalog.py` | `get_commands_for_group` |
| 5 | `apps/cli/command_catalog.py` | `CATALOG` → the `CommandEntry(command_id="mission.ledger", ...)` |
| 6 | `apps/cli/grouped.py` | `_add_command_args` |
| 7 | `apps/cli/grouped.py` | `cmd_parser.set_defaults(_command_id=cmd.command_id)` |
| 8 | `apps/cli/grouped.py` | `_get_dispatch_table` |
| 9 | `apps/cli/commands/__init__.py` | `collect_all_handlers` |
| 10 | `apps/cli/commands/mission_cmd.py` | `COMMAND_HANDLERS["mission.ledger"]` (a lambda) |
| 11 | `apps/cli/commands/mission_cmd.py` | `_cmd_mission_ledger` |
| 12 | `apps/cli/commands/mission_cmd.py` | `_resolve_project_id`, `_load_mission_or_exit` |
| 13 | `packages/orchestration/mission_state.py` | `resolve_mission_id`, `load_mission` |
| 14 | `packages/orchestration/orchestrator_loop.py` | `read_ledger`, `render_ledger` |

The parser is generated ENTIRELY from the catalog — `build_parser` loops `GROUPS`
then `get_commands_for_group(group_id)` and adds one subparser per entry — so
there is no hand-maintained argument table anywhere. Argument naming, verified
in `_add_command_args`: a positional `ArgDef("mission_id", ...)` becomes
`parser.add_argument("mission_id", ...)`, so the handler reads `args.mission_id`;
`_JSON_OPT` (`ArgDef("--json", ...)`) becomes `dest="json"`; `_PROJECT_SCOPE_OPT`
(`ArgDef("--project", ...)`) becomes `dest="project"`. Both shared `ArgDef`
constants already exist in `command_catalog.py` and are reused, never re-declared.

Help rendering is the same catalog walk: `_print_group_help` builds its list from
`get_commands_for_group`, and `_print_command_help` from `cmd.args`. Ordering is
declaration order — `get_commands_for_group` is a list comprehension over
`CATALOG` with no sort — so where the entry is PLACED in `CATALOG` is where it
appears in `remedy mission` help.

### The checklist R14 can order verbatim

Adding one mission verb is exactly THREE edits, in two files:

1. `apps/cli/command_catalog.py` — one `CommandEntry` inside the mission block of
   `CATALOG` (placement = help position).
2. `apps/cli/commands/mission_cmd.py` — one `_cmd_mission_<verb>` function.
3. `apps/cli/commands/mission_cmd.py` — one `COMMAND_HANDLERS` entry keyed by the
   same `command_id`, unpacking `args` into the handler's keyword arguments.

Nothing else is required, and each of these was checked rather than assumed:

- No `apps/cli/commands/__init__.py` edit — `mission_cmd` is already in
  `collect_all_handlers`'s import list.
- No parser edit, no help edit — both are generated (above).
- No `docs/` edit. `grep -rln 'mission ledger\|mission pause' docs/` returns 2
  files, both under `docs/roadmap/features/` (`T2_F077.md`, `T1_F070.md`); no
  ist-doc enumerates the mission verbs.
- `related=` is OPTIONAL and unvalidated. Proof, run in-process:
  `{r for c in CATALOG for r in c.related} - {c.command_id for c in CATALOG}`
  returns `['readiness.show']` — the catalog already ships a DANGLING related
  target, so no test can be requiring existence. Symmetry is absent too:
  `mission.ledger` names `mission.run` and `mission.show`, and `mission.show`
  names neither.
- A catalog entry with no handler is green in the test suite and fails only at
  runtime: `main` prints `Error: no handler for {command_id}` and exits 1.

Counts, from `python3 -c` against the imported modules at `a9ebc920`:
`len(CATALOG)` = 334; `len(collect_all_handlers())` = 334; catalog ids without a
handler = `[]`; handlers without a catalog id = `[]`;
`len(get_commands_for_group("mission"))` = 12 — `run, ledger, handoff, report,
start, list, continue, plan, show, achieve, abandon, pause`.
`mission_cmd.COMMAND_HANDLERS` itself holds 10 of those 12; `mission.run` and
`mission.report` live in `apps/cli/commands/worker_facade_cmd.py` instead. That
split is load-bearing for Q6.

## Q2 — the read-only evaluation entry point

The block's framing is imprecise and R14 must not order against it: the choice is
not "one of the three is side-effect free", it is "one of the three is side-effect
free and it is not callable from a mission id alone".

| Symbol | Side-effect free? | Evidence from the BODY |
|---|---|---|
| `evaluate_ledger` | **YES** | Its whole body builds a tuple of `evaluate_no_progress`, `evaluate_burn_anomaly`, `evaluate_goal_drift` and filters `None`. Each of those three reads only its `entries` argument through `_sub_dict`, `_move_kind`, `_milestone_id`, `_iteration`, `measured_tokens`, `dispatched_entries` — every one a pure accessor over dicts — and returns a frozen `Trip` or `None`. No import inside the body, no I/O, no `save_*`. |
| `act_on_trips` | **NO** | Body calls `set_mission_status`, `enqueue_task_decision`, `save_job` and `orchestrator_loop.append_ledger_entry`. Its own docstring: "WRITES, and nothing beyond them: the mission STATUS […]; ONE escalation record […]; and ONE ledger entry per trip". |
| `watchdog_pass` | **NO** | Its last statement is `return act_on_trips(...)`. It reads (`read_ledger`, `load_mission`, `watchdog_thresholds_from_config`) and then delegates the writing. |

`evaluate_ledger`'s exact signature, from disk:

```
def evaluate_ledger(
    entries: Sequence[dict[str, Any]],
    *,
    milestone_ids: Sequence[str],
    thresholds: WatchdogThresholds,
) -> list[Trip]:
```

`Trip` is a frozen dataclass with exactly four fields, and `Trip.to_json` emits
exactly those four. The evidence triple maps onto them like this:

| Evidence triple | `Trip` field | Type |
|---|---|---|
| what tripped | `kind` | `str` — one of `TRIP_NO_PROGRESS`, `TRIP_BURN_ANOMALY`, `TRIP_GOAL_DRIFT` |
| what, in one line | `what` | `str`, a rendered human sentence |
| since when | `since_iteration` | `int` |
| the numbers | `numbers` | `dict[str, Any]`, per-tripwire keys |

`numbers` keys differ per kind, read off each evaluator's `Trip(...)` construction:
`no_progress` → `repeats`, `threshold`, `milestone_id`; `burn_anomaly` →
`window_mean`, `baseline_mean`, `multiplier`, `baseline_samples`; `goal_drift` →
`milestone_id`, `known_milestones`.

### The gap R14 must close

There is NO function today that takes a mission id and returns `list[Trip]`
without writing. `watchdog_pass` is the only mission-id-shaped entry point and it
writes. A read-only `remedy mission watchdog <id>` must compose the four reads
itself — exactly `watchdog_pass`'s body minus its last statement:

```
entries   = orchestrator_loop.read_ledger(project_id, mission_id, root)
mission   = mission_state.load_mission(project_id, mission_id, root)
trips     = evaluate_ledger(entries,
                            milestone_ids=orchestrator_loop.milestone_ids(mission),
                            thresholds=watchdog_thresholds_from_config())
```

Two shapes are open to R14 — extract that composition into a named
`watchdog.evaluate_mission(...)` beside `watchdog_pass`, or inline it in the CLI
handler. This inventory does not choose; it records that the choice EXISTS and
that neither is a change to `act_on_trips`, `watchdog_pass` or `evaluate_ledger`,
all three of which the block forbids touching.

Note for the block author: `watchdog_thresholds_from_config()` reads
`packages/orchestration/config.py`'s `get_config` and writes nothing, so it is
safe inside a read-only verb.

## Q3 — the `mission resume` verb that does not exist

### What the block gets right, and what it gets wrong

Right: `_status_for_verb` (`apps/cli/commands/mission_cmd.py`) maps exactly
`achieve`, `abandon`, `pause` and has no `resume`.

Wrong: its dict is NOT the only place the verb list is encoded. There are THREE
machine-readable encodings and they can drift independently:

1. `_status_for_verb`'s dict — `apps/cli/commands/mission_cmd.py`.
2. `COMMAND_HANDLERS` — same file: three separate lambdas each passing the verb
   as a STRING LITERAL (`"achieve"`, `"abandon"`, `"pause"`) into
   `_cmd_mission_set_status`. A verb added to the dict but not here is
   unreachable; one added here but not to the dict raises `KeyError`.
3. `CATALOG` — `apps/cli/command_catalog.py`, three `CommandEntry` values
   (`mission.achieve`, `mission.abandon`, `mission.pause`).

Plus two PROSE copies that a grep for the verb list will hit and that R14 should
extend for consistency, though nothing tests them: `mission_cmd.py`'s module
docstring and `_cmd_mission_set_status`'s docstring, and
`packages/orchestration/mission_state.py`'s module docstring and
`set_mission_status`'s docstring.

Command: `grep -rn 'achieve.*abandon.*pause\|"pause"' --include=*.py apps/ packages/`
→ 8 hits, being those three encodings plus the four docstrings plus the unrelated
`job.pause` catalog entry.

### DECISION F077 D4, what it actually requires

Read from `.agent/decisions.md`. Its CHOSEN paragraph:

```
CHOSEN. T002 ships the pause and the deduped decision without a resume verb, and
T003 — the slice that owns the manual CLI — adds `mission resume` alongside the
watchdog command. The feature file is NOT amended: its acceptance sentence
"resume clears exactly that trip's dedup" stays true across T002 and T003
together, because D3 makes the clearing a consequence of answering the decision
rather than of the verb, and the verb only restores `active`.
```

Its HOW TO REVERSE names the size: "It is one `_status_for_verb` entry, one
catalog registration and its test." That is Q1's three-edit checklist minus the
handler, because `_cmd_mission_set_status` is reused.

So D4 requires: `resume` → `active`, and NOTHING about the dedup. R14 must not
order dedup clearing into the verb — D3 already placed it on the decision.

### Which status, and who else writes it

`packages/orchestration/mission_state.py` defines four status constants —
`MISSION_STATUS_ACTIVE = "active"`, `MISSION_STATUS_PAUSED = "paused"`,
`MISSION_STATUS_ACHIEVED = "achieved"`, `MISSION_STATUS_ABANDONED = "abandoned"`
— and `MISSION_STATUSES` is the tuple of all four. `set_mission_status` validates
membership, `replace(mission, status=status)`, `save_mission`. There is
deliberately NO transition table (`_cmd_mission_set_status`'s docstring: "any
valid status may follow any other"), so `paused → active` needs no new rule.

Does anything already perform that transition under another name? NO.
`grep -rn 'MISSION_STATUS_ACTIVE' --include=*.py packages/ apps/` returns 8 hits
and every one is a definition, a re-export, a DEFAULT or a COMPARISON — never an
assignment through `set_mission_status`:

- `mission_state.py` — the constant, its listing in `MISSION_STATUSES`, the
  `Mission` dataclass default, and `start_mission`'s literal `status=`.
- `orchestrator_loop.py` — an import, and `run_mission`'s safe-point comparison
  `if mission.status != MISSION_STATUS_ACTIVE:` (see Q8).
- `watchdog.py` — an import, and `act_on_trips`'s guard
  `if mission.status == MISSION_STATUS_ACTIVE:`.

A mission therefore becomes `active` exactly once, at `start_mission`, and there
is no route back. That is D4's premise, and it is still true at `a9ebc920`.

`mission.resume` as an id is free: `grep -rn 'mission.resume\|mission\.activate'
--include=*.py apps/ packages/` returns only a prose comment in
`orchestrator_loop.py` ("a mission resumed from a…"). `job.resume` already exists
as a `CommandEntry`, but the uniqueness invariant is over `(group_id,
subcommand)`, so `("mission", "resume")` does not collide with `("job",
"resume")`.

## Q4 — the dedup marker and what clears it

### Where the dedup state lives

NOT in `watchdog.py`, and not in any file of its own. Per DECISION F077 D3 the
dedup state IS the escalation record's own `status` field, and that record lives
in the JOB's metadata on disk — the job the mission's `latest_link()` names.
`watchdog_decision_marker(kind)` returns the literal `"[watchdog:<kind>]"` and is
only a PREFIX written into that record's `question` text; it is not itself state.

Chain, symbol by symbol: `watchdog.act_on_trips` → `escalation.enqueue_task_decision`
→ `escalation._stored_records` → `escalation._metadata` → the job object's
`metadata` dict → `storage.save_job`.

### Writers and readers, counted mechanically

Command: `grep -rn 'watchdog_decision_marker' --include=*.py .` → **7 hits**: the
`def` in `packages/orchestration/watchdog.py`, ONE call in the same file (inside
`act_on_trips.decide`), and 5 in `tests/orchestration/test_watchdog.py`. So the
marker has exactly one product caller.

Because the marker is not the state, the counts that matter are on the RECORD.
Command: `grep -rn 'enqueue_task_decision\|answer_task_decision\|auto_apply_safe_default'
--include=*.py apps/ packages/`:

| Role | Symbol | File |
|---|---|---|
| WRITER (creates the record, `status=ESCALATION_STATUS_OPEN`) | `enqueue_task_decision` | `packages/orchestration/escalation.py` |
| WRITER call site (watchdog) | `act_on_trips.decide` | `packages/orchestration/watchdog.py` |
| WRITER (flips `open` → `answered`) | `answer_task_decision` | `packages/orchestration/escalation.py` |
| WRITER call site (human CLI) | `_cmd_decision_resolve`, the `td:` prefix branch | `apps/cli/commands/decision.py` |
| WRITER (delegating) | `auto_apply_safe_default` → `answer_task_decision` | `packages/orchestration/escalation.py` |
| WRITER call site (unattended) | `long_run_executor` | `packages/orchestration/long_run_executor.py` |
| READER (the dedup scan) | `act_on_trips.decide`, `str(record.get("question","")).startswith(marker)` | `packages/orchestration/watchdog.py` |
| READER (feeds the scan) | `orchestrator_loop.open_mission_decisions` → `escalation.open_task_decisions` | two files |

`escalation.py`'s `__all__` also lists the three names; those are exports, not
call sites, and are excluded from the table above.

### What clears it today

**NOTHING clears the marker, and no code path is named for clearing.** What
exists is a state flip that has the same effect as a side effect:
`answer_task_decision` sets `record["status"] = ESCALATION_STATUS_ANSWERED`,
which removes the record from `open_task_decisions`, therefore from
`open_mission_decisions`, therefore from the `open_records` list the dedup scan
reads. The record and its `[watchdog:<kind>]` question TEXT stay on disk forever.
The reachable human route is `remedy decision resolve <job> <td:…> --reason "…"`.

Three consequences R14 must know, each read off a body rather than a name:

1. `auto_apply_safe_default` **cannot** clear a watchdog decision. Its first
   statement is `if not str(record.get("safe_default") or ""): return None`, and
   `act_on_trips` passes `safe_default=""` on purpose (its inline comment says
   so). So an unattended run cannot auto-answer a trip.
2. Answering does not prevent a SECOND decision. The suppression test is
   "an OPEN record whose question starts with this marker", so once answered, the
   next trip of the same class enqueues a brand-new record.
3. The dedup gates the DECISION only, never the pause. In `act_on_trips` the
   `if mission.status == MISSION_STATUS_ACTIVE: set_mission_status(..., PAUSED)`
   runs BEFORE `decide` is ever called, and the ledger append runs for every
   trip whatever `decide` returned. A suppressed trip still pauses and still
   writes an entry.

## Q5 — the report surface

### The block's premise is wrong, and this is the most consequential finding here

`mission report` is NOT a mission-facing command. Evidence:

- `grep -rn '"mission.report"' --include=*.py apps/ packages/` → the handler is
  `_cmd_mission_report` in **`apps/cli/commands/worker_facade_cmd.py`**, not in
  `mission_cmd.py`.
- Its `CommandEntry` declares `ArgDef("run_id", "Run ID")` — a RUN id, not a
  mission id — and `--job-id`.
- The renderer is `build_mission_morning_report` in
  `packages/orchestration/dogfood_run.py`. Reading its body: it calls
  `load_dogfood_run`, `list_dogfood_runs` and `evaluate_dogfood_run`, and fills a
  `MissionMorningReport` from a `DogfoodRun`. It never imports `mission_state`,
  never calls `load_mission`, never calls `read_ledger`, and never sees a
  `Mission` record.
- Its `report.mission_status` field is a FALSE FRIEND: it is assigned
  `"satisfied" if ev.satisfied else ev.status` from `evaluate_dogfood_run`, i.e.
  the dogfood contract's verdict. It is never one of the four
  `MISSION_STATUS_*` constants and will never read `paused`.
- The two objects are distinguished at runtime elsewhere in the same module:
  `_cmd_mission_run` calls `_names_a_mission(run_id, ...)` and branches to the
  F070 loop only when the positional resolves to a real mission. `_cmd_mission_report`
  has NO such branch.

So "a paused-by-watchdog mission's report leads with the trip" has **no insertion
point in `mission report` as it stands**. Making it fit means giving
`_cmd_mission_report` the same resolve-or-facade branch `_cmd_mission_run`
already has, which is a change to `worker_facade_cmd.py` — and Q6 shows that file
is the one place in this area with a hard exact-set guard.

### The candidate surfaces that DO read the mission

| Surface | File | Symbol | Reads |
|---|---|---|---|
| the run summary | `apps/cli/commands/mission_cmd.py` | `_cmd_mission_run_loop` | `run_mission` result + `read_ledger` + `render_ledger` |
| the full ledger | `apps/cli/commands/mission_cmd.py` | `_cmd_mission_ledger` | `read_ledger` + `render_ledger` |
| the mission chain | `apps/cli/commands/mission_cmd.py` | `_cmd_mission_show` | `mission_state.render_mission_chain` |

`_cmd_mission_run_loop`'s text output has a fixed shape — mission id, then
`Terminal:`, then `result.detail`, then `Iterations this run:`, then a
`TERMINAL_NO_PROVIDER` note, then the ledger block, then the `Full ledger:`
pointer. A "leads with" line would go between the mission id and `Terminal:`.

### Does the renderer have a notion of leading or priority sections?

**No.** `orchestrator_loop.render_ledger` is a single `for body in entries` loop
that appends in ledger order and joins with `\n`. There is no sort, no
partition, no header, no section concept, and its only special-casing is
per-FIELD (`if move.get("rationale")`, `if outcome.get("detail")`,
`if usage`). T003 would be INTRODUCING the notion of a leading section wherever
it puts it. Because the block forbids reordering nothing in particular here, this
is recorded as a design fact, not a defect.

One thing already works in T003's favour and should not be rebuilt: a
`watchdog_tripped` entry already renders its whole evidence triple, because
`render_ledger` prints `move["kind"]` and then every key of `move["payload"]` in
`sorted` order, and `act_on_trips` puts `trip.to_json()` in that payload
(DECISION F077 D5).

## Q6 — the guards that already constrain these files

Checklist item 7, run as work. Command:
`grep -rn '\.count(' tests/ --include=*.py` → **56 hits**, and ZERO of them read
`mission_cmd.py`, `command_catalog.py`, `worker_facade_cmd.py` or `dogfood_run.py`.
The whole-file guards in this area are `len(...) == N` and `set(...) == {...}`
instead, and there are exactly six that matter.

| Path | Test | What it pins | Verdict for R14 |
|---|---|---|---|
| `tests/cli/test_worker_facade_cmd.py` | `TestHandlerRegistry::test_all_handlers_present` | `set(worker_facade_cmd.COMMAND_HANDLERS.keys()) == expected`, an explicit 12-key literal set including `mission.report` | **BLOCKS** any new handler in `worker_facade_cmd.py` |
| `tests/cli/test_worker_facade_cmd.py` | `TestCatalogIntegration::test_all_facade_commands_have_handlers` | `len([c for c in CATALOG if c.command_id in COMMAND_HANDLERS]) == 12` | **BLOCKS** the same |
| `tests/orchestration/test_dogfood_run.py` | `TestCLIHandlers::test_handlers_registered` | `len(dogfood_cmd.COMMAND_HANDLERS) == 12` | **BLOCKS** a handler added to `dogfood_cmd.py` |
| `tests/orchestration/test_dogfood_run.py` | `TestCatalogEntries::test_dogfood_commands_in_catalog` | `len(dogfood_cmds) == 12` for `group_id == "dogfood"` | **BLOCKS** a new `dogfood.*` entry |
| `tests/orchestration/test_mission_compiler.py` | `test_the_cli_names_the_provider_it_planned_with` | `source.index("outcome = plan_mission(")` in `mission_cmd.py`, then `'provider_kind="ollama"'` within the next 200 chars | CONDITIONAL — red only if a new, textually EARLIER `outcome = plan_mission(` appears |
| `tests/orchestration/test_orchestrator_loop.py` | `test_the_cli_names_the_provider_it_runs_with` | `source.index("result = run_mission(")` in `mission_cmd.py`, same 200-char window | CONDITIONAL — same shape |
| `tests/ui_server/test_dashboard_contract.py` | `TestJobSummaryCommandContract::test_job_summary_supports_json` | `catalog.index("job.summary")`, then `supports_json=True` within 400 chars | CONDITIONAL — red only if a new entry puts the literal `job.summary` textually above the real one |

The two `source.index` guards on `mission_cmd.py` carry their own docstring
saying the scope was narrowed on purpose after R-0258, which is why they take the
FIRST occurrence rather than counting.

### The one that decides where R14 puts the handlers

`apps/cli/commands/mission_cmd.py`'s own `COMMAND_HANDLERS` — 10 keys today — has
**no size guard and no key-set guard anywhere**:
`grep -rn 'COMMAND_HANDLERS' tests/cli/test_mission_cmd.py` returns nothing.
`grep -rn '_status_for_verb' tests/` also returns nothing — the verb→status
mapping is entirely untested today.

So: register `mission.watchdog` and `mission.resume` in `mission_cmd.py`.
Registering either in `worker_facade_cmd.py` turns two green tests red in the same
commit.

### The scoped ones that are harmless (recorded so R14 does not fear them)

`tests/cli/test_mission_cmd.py`'s `test_mission_run_is_registered_exactly_once`
and `test_mission_ledger_is_registered_exactly_once` filter `CATALOG` by ONE
`command_id` before `== 1`, so a different id cannot touch them.
`test_the_mission_commands_are_in_the_catalog`,
`test_the_transition_commands_are_in_the_catalog`,
`test_every_mission_command_has_a_handler` and
`test_no_mission_command_may_execute_or_mutate_the_repo` all use `<=` subset
checks or fixed 3-id lists. `tests/cli/test_worker_facade_cmd.py`'s
`test_mission_commands_in_catalog` says so in its own docstring: "A subset, not
the whole group […] not the group's size."

No test pins the group's size or the catalog's:
`grep -rn 'len(CATALOG)' tests/` and
`grep -rn 'get_commands_for_group("mission")' tests/` both return nothing.

## Q7 — the catalog's completeness contract

The catalog-wide gate is ONE file: `tests/test_command_catalog.py`. The
`dashboard_contract` suite is not one — `python3 -m pytest tests/ -q -k
"dashboard_contract" --collect-only` reports `70/16864 tests collected (16794
deselected)`, all 70 in `tests/ui_server/test_dashboard_contract.py`, and only its
`ui.start` and `job.summary` tests touch the catalog at all.

`ActionClass` in `apps/cli/command_catalog.py` is a `Literal` of exactly eight
values: `read_only`, `write_metadata`, `approval_gate`, `apply_write`,
`test_execution`, `dev_helper`, `local_state_change`,
`controlled_builder_execution`.

### What `tests/test_command_catalog.py` demands of a new entry

| Test | Rule | Demand on `mission.watchdog` / `mission.resume` |
|---|---|---|
| `test_no_duplicate_command_ids` | ids unique | both ids are free (Q3) |
| `test_no_duplicate_grouped_paths` | `(group_id, subcommand)` unique | `("mission","watchdog")` and `("mission","resume")` are free |
| `test_every_command_belongs_to_known_group` | `group_id in GROUPS` | `"mission"` exists |
| `test_command_id_format` | `command_id.split(".",1)` must equal `(group_id, subcommand)` | `command_id="mission.watchdog"`, `group_id="mission"`, `subcommand="watchdog"` — no aliasing |
| `test_every_command_has_action_class` | one of the eight | see the precedent row below |
| `test_mutating_commands_flagged` | `may_mutate_repo or may_execute_commands` ⇒ not `read_only` | leave both `False` |
| `test_no_sensitive_terms_in_descriptions` | `description` free of `password=`, `BEGIN PRIVATE KEY`, `raw_stdout`, `raw_stderr`, `diff_preview`, `approval_reason`, `api_key=`, `secret=` (case-insensitive) and of token-boundary `sk-`, `ghp_`, `xoxb-` | ordinary prose passes; the token-boundary regex is why "task-scoped" is safe |
| `test_no_sensitive_terms_in_arg_help` | same list over every `ArgDef.help` | applies to any new `ArgDef` |
| `test_json_commands_have_json_arg` | `supports_json` ⇒ an arg literally named `--json` | reuse `_JSON_OPT` |

### Rules that DO NOT exist — R14 must not invent them as constraints

Each was proven by a command that returned nothing:

- **Description style.** No period, capital, verb-first, or length rule.
  `grep -rn 'description.endswith\|description\.startswith\|len(cmd.description)' tests/ --include=*.py`
  → no catalog hits.
- **`related=` existence or symmetry.** `grep -rn '\.related' tests/ --include=*.py`
  → 3 hits, all single-membership checks in `test_context_inspect_cli.py` and
  `test_change_proof_cli.py`. Confirmed independently in Q1 by the dangling
  `readiness.show` target.
- **Ordering.** `grep -rn sorted tests/test_command_catalog.py tests/test_grouped_cli.py`
  → no output.
- **A global catalog↔handler parity test.** None exists; every handler assertion
  found is a hard-coded id list. (The bijection is nonetheless TRUE today at 334
  ≡ 334 — Q1 — and `integrity check`'s `handler_import` check reports
  `handlers=334`.)
- **A global catalog↔parser reachability test.** None exists; reachability is
  structural, via `build_parser`.
- **A catalog→docs sync test.** Only the reverse exists: commands NAMED in
  `docs/guides/autocoder-usage.md` must exist in the catalog
  (`tests/cli/test_do_cmd_summary.py`). Adding an entry needs no doc edit.

### The tests that will exercise the new entries indirectly

`tests/test_grouped_cli.py` parametrizes over `_HELP_CONTRACT_GROUPS`, which is
every group in `GROUPS`, so `mission` is covered:
`test_group_help_lists_subcommands` asserts `cmd.subcommand in stdout` for every
entry of the group, and `test_main_entrypoint_delegates_group_help_to_grouped_cli`
repeats it through `apps.cli.main`. Both are satisfied automatically because help
renders from the catalog — but they mean a badly-formed entry fails as a HELP
test, not as a catalog test, which is where R14 should look first if it goes red.
`test_help_no_sensitive_leaks` re-scans the rendered help with a PLAIN substring
list (no token boundary, unlike `test_command_catalog.py`), so a bare `sk-`
anywhere in a description or arg help is red there even if the catalog test
passes.

### The shape the group's precedent sets

`tests/cli/test_mission_cmd.py`'s `TestPlanCatalog` and its transition-command
tests apply the same five assertions to each mission write command:
`action_class == "write_metadata"`, `supports_json is True`, the id in
`collect_all_handlers()`, `may_execute_commands is False`, `may_mutate_repo is
False`. `mission.ledger` and `mission.report` are the `read_only` precedent, both
with `supports_json=True`. Reading those across the group: a read-only
`mission watchdog` matches `mission.ledger`; a `mission resume` that moves the
status matches `mission.pause`, which is `write_metadata`.

## Q8 — what a paused mission does on the next pass

### The safe point, exactly

In `packages/orchestration/orchestrator_loop.py`, `run_mission`'s per-iteration
loop opens with TWO safe points, and the block conflates them.

The FIRST is the stop-request safe point: `stop_requested` → `consume_stop` →
build a `TERMINAL_STOPPED` `MoveOutcome` → `_record(...)` → `return
build_boundary_handoff(result, root)`. This one DOES write a ledger entry.

The SECOND is the status safe point, and it is the one Q8 asks about:

```
        mission = load_mission(pid, mission_id, root)
        if mission.status != MISSION_STATUS_ACTIVE:
            result.terminal = TERMINAL_NOT_ACTIVE
            result.detail = f"mission status is {mission.status}"
            result.iterations = step - 1
            return result
```

It does exactly four things and **writes NO ledger entry** — there is no
`_record` call between the `if` and the `return`, and it returns `result` bare
rather than through `build_boundary_handoff`. `TERMINAL_NOT_ACTIVE` is the string
`"mission_not_active"`. So the block's phrase "the ledger entry the safe point
writes" is wrong for this safe point; it describes the stop-request one above it.
Correspondingly there is no interaction between a safe-point entry and the trip
entry, because the former does not exist. What R14 needs from this is narrow:
`resume` must restore `status == "active"` and nothing else, because the status
is the ONLY thing this safe point reads.

### The re-trip risk: the code CONFIRMS it, for all three tripwires

The plan carries this as a risk. It is real, and reading the evaluators makes it
sharper than the plan states.

The order inside one iteration is: `execute_move` → `_record` → `if
outcome.terminal: return` → `watchdog_pass(...)`. So the watchdog runs at the END
of a continuing iteration, and the status safe point runs at the START of the
next one. After a resume the loop therefore completes ONE full iteration —
including a dispatch — before the watchdog can pause it again.

And it will pause it again, because `read_ledger` returns the mission's whole
history across every run and nothing prunes it:

- **`no_progress`** — its run counter is cleared only by a
  `declare_milestone_done` entry or by a change of `milestone_id`. A
  `watchdog_tripped` entry is neither: `_move_kind` returns `"watchdog_tripped"`,
  so the `MOVE_DECLARE_MILESTONE_DONE` branch is skipped and
  `dispatched_entries([entry])` is empty, which `continue`s. The run therefore
  survives the trip entry, and the FIRST dispatch after the resume makes
  `len(run) >= repeats` true again.
- **`goal_drift`** — `evaluate_goal_drift` returns on the first unknown
  milestone anywhere in the ledger. That entry is permanent, so this tripwire
  re-fires on EVERY pass until the milestone becomes known. Strongest case of the
  three.
- **`burn_anomaly`** — the trip entry itself does not disturb the window, because
  `act_on_trips` writes `cost={"calls": 0, "usage": None, ...}` and
  `measured_tokens` returns `None` for a missing `usage`, which the evaluator
  skips. So the same trailing window is compared to the same baseline on the next
  pass and re-fires until enough cheaper MEASURED iterations shift it.

And the pause is re-applied whether or not the decision was answered, because
`act_on_trips` pauses before `decide` is consulted (Q4, consequence 3). What
differs is only the decision: if the human ANSWERED it, the marker scan finds no
open record and a new decision is enqueued; if the human did not, the trip is
suppressed and only the pause and the ledger entry are written.

Net, and this is the sentence R14 must design against: **`mission resume` as D4
defines it buys exactly one iteration.** Nothing in the current code prevents the
immediate re-trip, and this inventory does not repair it — it records that D4's
verb is necessary but, on its own, not sufficient, and that R14's block should
decide explicitly whether T003 ships the verb as D4 scoped it and leaves the
re-trip to a follow-on, or widens.
