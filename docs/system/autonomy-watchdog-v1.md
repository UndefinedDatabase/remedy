# Autonomy Watchdog v1

The autonomy watchdog is a tripwire that is independent of the thing it watches.
It is an evaluation pass over the orchestrator loop's decision ledger, and it
answers one question per trip class: is the loop repeating itself, is it burning
tokens out of proportion to its own history, is it working on something the
mission plan never named. It lives in `packages/orchestration/watchdog.py`.

## It reads; it never repairs

Independence is an acceptance criterion of this feature, not a preference: a
change in which the watchdog "helpfully" fixes what it found is rejected. When a
tripwire fires, the watchdog stops the run and hands the evidence to a human.

Its writes are exactly three, all of them in `act_on_trips`:

- the mission STATUS — once per call, and only `active` → `paused`. An achieved
  or abandoned mission is terminal and is not overwritten; an already-paused one
  needs no second write.
- ONE escalation record on the job the mission last linked, per unsuppressed
  trip, raised through `escalation.enqueue_task_decision`.
- ONE ledger entry per trip, whatever the decision outcome was — the pause and
  the record of it do not depend on whether a decision could be attached.

Nothing else is touched: not the mission plan, not its milestones, not the job
beyond that one escalation record, not the dossier.

The decision carries the options `resume` and `abort` and an impact line saying
the mission is paused until it is answered. Its `safe_default` is deliberately
empty, because that is the value `escalation.auto_apply_safe_default` applies
unattended, and a trip the automation it just stopped can auto-answer is not a
tripwire. Dedup is the whole of a literal marker on the decision question,
`watchdog_decision_marker(kind)` → `[watchdog:no_progress]` and friends: when an
open decision on the mission already starts with that marker, the trip is
suppressed and the returned `TripAction` says so in its `note`. The same applies
to the gaps — no linked job, an unreadable job, a job with no task — each is
reported in the `note`, while the pause and the ledger entry happen anyway.

## The three tripwires

| Kind | Fires when | Evidence in `numbers` |
|---|---|---|
| `no_progress` | N `dispatch_job` moves in a row on ONE milestone with no `declare_milestone_done` between them | `repeats`, `threshold`, `milestone_id` |
| `burn_anomaly` | the mean of the most recent measured iterations STRICTLY exceeds `multiplier` times the mean of the earlier ones | `window_mean`, `baseline_mean`, `multiplier`, `baseline_samples` |
| `goal_drift` | a dispatched job names a milestone that is not in the mission plan | `milestone_id`, `known_milestones` |

Every trip is a frozen `Trip` carrying `kind`, `what` (one human sentence),
`since_iteration` and `numbers`.

`no_progress` reads progress off the LEDGER rather than the plan body, because
nothing versions or timestamps the mission's milestone-done set, so the plan
cannot say WHEN it advanced. Any `declare_milestone_done` clears the run,
whatever it was about. A refused dispatch is not counted: the loop's own
second-refusal escalation already owns that event, and counting it here would
give one failure two independent alarms.

`burn_anomaly` compares the mission against its own trailing baseline, not
against a global constant, so a big mission is not permanently anomalous and a
small one is not blind. It is INERT until the ledger holds at least
`burn_min_samples + burn_window` measured entries. An entry with no measured
`cost.usage` contributes nothing rather than a zero, because a zero would drag
the baseline down and manufacture an anomaly out of missing data.

`goal_drift` is BINARY rather than counted — one job on an invented goal is
already the whole failure — and it reads the milestone from the ledger entry's
`move.payload.milestone_id`, never from the job. An entry with no milestone at
all is a torn entry, not evidence of drift.

Thresholds live in config, not in code. The four keys are registered in
`packages/orchestration/config.py`:

| Config key | Environment variable | Type | Default |
|---|---|---|---|
| `watchdog.no_progress_repeats` | `REMEDY_WATCHDOG_NO_PROGRESS_REPEATS` | int | `3` |
| `watchdog.burn_window` | `REMEDY_WATCHDOG_BURN_WINDOW` | int | `3` |
| `watchdog.burn_min_samples` | `REMEDY_WATCHDOG_BURN_MIN_SAMPLES` | int | `5` |
| `watchdog.burn_multiplier` | `REMEDY_WATCHDOG_BURN_MULTIPLIER` | float | `3.0` |

`watchdog_thresholds_from_config` resolves them ONCE, at the edge, into a frozen
`WatchdogThresholds` value that carries the same four numbers as its dataclass
defaults; a key that reads `None` takes that default rather than a guess. It is
the one function in the module that reaches outside, and it imports `get_config`
inside its body so the evaluators stay callable with no config layer present.

## The public surface

Read out of `packages/orchestration/watchdog.py`:

- `evaluate_mission(project_id, mission_id, *, root=None) -> list[Trip]` — the
  read-only half of a watchdog pass: every tripwire over one mission's ledger
  and NOT ONE WRITE, with the thresholds from config and the known milestone ids
  from the persisted mission plan.
- `act_on_trips(project_id, mission_id, trips, *, root=None, iteration=None, now=None) -> list[TripAction]`
  — the action: it pauses the mission, raises one deduped decision per trip and
  records every trip in the ledger, returning one `TripAction` per trip in the
  order given; an empty `trips` writes nothing at all.
- `watchdog_pass(project_id, mission_id, *, iteration=None, root=None, now=None) -> list[TripAction]`
  — `evaluate_mission` plus the action in one call, and the only entry point the
  running loop uses.
- `latest_trips_from_ledger(entries) -> list[Trip]` — a pure reader that
  reconstructs the newest recorded trip per kind from ledger entries already
  written, so a report can name the trip that paused a mission without
  re-running the watchdog; "newest" means last in ledger order, which is file
  order.

The three evaluators `evaluate_no_progress`, `evaluate_burn_anomaly` and
`evaluate_goal_drift`, their aggregator `evaluate_ledger`, the helpers
`dispatched_entries` and `measured_tokens`, and the `Trip`, `TripAction` and
`WatchdogThresholds` records are public as well. The evaluators and their
helpers are PURE: they read no file, write no file, mutate no mission and import
no loop. A malformed entry is SKIPPED rather than raised on — a ledger is
forensic evidence, and a tripwire that crashes on one bad line is a tripwire
that is not watching.

A trip is written to the ledger as
`move={"kind": "watchdog_tripped", "payload": trip.to_json()}` with a
`MoveOutcome` whose status is `watchdog_tripped`, an empty `context_digest` and
a zero, unmeasured cost. `render_ledger` prints every payload key in sorted
order, so the evidence triple appears in the human ledger with no change to the
renderer.

## Where it is wired

`run_mission` in `packages/orchestration/orchestrator_loop.py` calls
`watchdog_pass` once per CONTINUING iteration — after the iteration's move has
been executed and recorded, and after the terminal return, because a run that is
already over cannot be helped by pausing it. `watchdog_pass` is imported inside
that function body, since `watchdog` imports `orchestrator_loop` back.

The loop does not read the verdict. A pause is a mission STATUS, and the next
iteration's safe point already refuses to run a mission that is not active.

## The CLI surface

    remedy mission watchdog <mission_id> [--json]

The manual audit, and read-only by construction: it calls `evaluate_mission`,
prints the mission id, its status, `Tripwires fired: <n>` and then each trip with
its `since_iteration`, its sentence and its sorted numbers. It pauses nothing and
raises no decision — asking the watchdog what it sees must not itself stop a
mission. The watchdog ACTS only from inside `remedy mission run`.

    remedy mission resume <mission_id> [--json]

Marks a paused mission `active` again, and that is its whole scope: the verb
restores the status and nothing else. It does not clear the trip's dedup —
answering the open decision is what does that — and it does not clear the
evidence in the ledger.

    remedy mission show <mission_id> [--json]

Read-only, and led by why the mission stopped. When the mission status is
`paused`, the trips its ledger already RECORDS lead the text output:

    STOPPED: this mission was paused automatically and is waiting for you.
      <kind>  (since iteration <n>)
        <what>
        <number>: <value>
      Full evidence: remedy mission watchdog <mission_id>

followed by the usual mission chain. Nothing is re-evaluated here, so a reader
sees the trip that actually caused THIS pause rather than a fresh verdict over
the same ledger. A mission that is not paused prints no lead at all, so its
output is byte for byte what it was before this feature. Under `--json` the
object always carries a `watchdog_trips` array beside `mission`; the array is
empty when the mission is not paused.

## Why a tripped run's ledger repeats an iteration number

A ledger from a tripped run reads `[1, 2, 3, 3]`, and that is correct.

`run_mission` passes its OWN iteration number down to `watchdog_pass`, so a trip
is recorded as belonging to the iteration that produced the evidence for it. The
`iteration` field is an ATTRIBUTION, not a unique key: it answers "which
iteration does this entry belong to", a question with more than one correct
answer per number. `_record` has eleven call sites in `run_mission`, and the
executed move's entry and the blocked-completion escalation's entry already fire
in the same pass at the same number. The ledger's ordering is its FILE order,
never a sort on this field.

So in `[1, 2, 3, 3]` the second `3` is the watchdog entry for the trip that
iteration 3's own entry provided the evidence for. Numbering the trip one past
that entry was tried and withdrawn: it collides with the loop's safe point,
which records and returns before the top-of-loop status check.

The one caller that does NOT supply a number is a manual multi-trip audit
calling `act_on_trips` with `iteration=None`; there each append resolves a fresh
number from `next_iteration_index`, so those entries are numbered consecutively.

## Deliberate absences

- Remedy deliberately does not let the watchdog repair anything, because a
  watchdog that could edit the run it is judging would be judging its own work.
  There is no retry, no rollback and no plan surgery here: it stops, and it
  reports.
- Remedy deliberately does not do class-expectation anomaly detection here,
  because a later cost-anomaly feature owns it. `burn_anomaly` is self-relative
  against the mission's own trailing baseline only.
- Remedy deliberately does not write to mission plans, jobs or dossiers, because
  the independence rule bounds the writes to the three named above. The job the
  mission last linked receives exactly one escalation record and nothing else.
- Remedy deliberately does not read the ledger inside
  `mission_state.render_mission_chain`, because that renderer takes a `Mission`
  and nothing else: the trips live in the LEDGER, which `orchestrator_loop`
  owns, and `orchestrator_loop` imports `mission_state` — so reaching the ledger
  from the renderer would invert that dependency and build the very import cycle
  `watchdog` keeps its own imports inside function bodies to avoid. The trip
  lead therefore lives in `_cmd_mission_show` in
  `apps/cli/commands/mission_cmd.py`.

## Built by

F077 — Autonomy watchdog (`docs/roadmap/features/T2_F077.md`), on the branch
`feature/f077-autonomy-watchdog`. Its tests are
`tests/orchestration/test_watchdog.py` and, for the CLI surface,
`tests/cli/test_mission_cmd.py`.
