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
