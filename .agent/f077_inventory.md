# F077 T001 inventory — the loop ledger, the pause seam, the milestone link

Read-only investigation for F077 T001 (round R2). Nothing under `packages/`,
`apps/`, `tests/` or `docs/` was changed. Every answer names a FILE and a
SYMBOL; line numbers are deliberately omitted (R-0353 — line numbers move,
symbols survive). Quotes are verbatim from the working tree at commit
`362ae3b2`, with ONE normalisation: leading indentation is stripped to the
markdown code-block margin, so a quoted line's own indentation is not evidence.
Where a quote is a fragment of a longer line it is shown inline in backticks,
never as a block; where a block is elided the elision is marked `...`.

Headline: the pause guard IS re-evaluated every iteration from a freshly
re-read record, and the milestone link exists only in the loop's own ledger,
not on the job — both tripwires are therefore buildable as specified.

---

## Q1 — the loop's iteration ledger

**File:** `packages/orchestration/orchestrator_loop.py`
**Storage:** one JSON object per line in `ledger.jsonl`, append-only.

| Role | Symbol | Notes |
|---|---|---|
| entry type | `LedgerEntry` | `@dataclass(frozen=True)` |
| append | `append_ledger_entry` | opens the file in `"a"` mode |
| read | `read_ledger` | returns `list[dict[str, Any]]` |
| path | `ledger_path` | `mission_evidence_dir(...) / LEDGER_FILENAME` |
| next index | `next_iteration_index` | one past the highest recorded |
| cost measurement | `measure_call_cost` | returns the `cost` dict |
| filename | `LEDGER_FILENAME` | `"ledger.jsonl"` |
| human render | `render_ledger` | prints move, payload, outcome, cost |
| in-loop writer | `_record` (nested in `run_mission`) | the only call site |

All six pointers the R1 block gave verified against the file; none had drifted.

**`LedgerEntry` fields — ALL of them, in declaration order:**

- `iteration: int`
- `context_digest: str`
- `move: dict[str, Any]`
- `outcome: dict[str, Any]`
- `cost: dict[str, Any] = field(default_factory=dict)`
- `protocol_version: str = PROTOCOL_VERSION`  (`PROTOCOL_VERSION = "v1"`)
- `recorded_at: str = ""`

`LedgerEntry.to_json` writes exactly those seven keys, so the on-disk shape and
the dataclass cannot drift. Deciding line:

    "protocol_version": self.protocol_version,

**Read-back.** `read_ledger` is deliberately lossy-tolerant rather than strict:

    """Every entry, in order. A torn or unreadable line is SKIPPED, not raised.

A line that will not `json.loads` is `continue`d, and a body that is not a
`dict` is dropped. Consequence for T001: **iteration numbers can have gaps**,
and an evaluator must not infer "N consecutive iterations" from list position.
`next_iteration_index` reads `max(...)` of the recorded `iteration` values, so
numbering is per-MISSION and survives multiple `run_mission` invocations:

    Iteration numbering belongs to the MISSION, not to one ``run_mission``

**Nested shapes actually written by the loop:**

- `move` — `OrchestratorMove.model_dump()`, i.e. `schema_v`, `kind`, `payload`
  (a flat `dict[str, str]`), `rationale`. Written as `{}` for the entries the
  loop records without a model move (stop, no-provider, invalid-move,
  escalation, iteration failure).
- `outcome` — `MoveOutcome.to_json()`, i.e. `status`, `detail`, and `job_id`
  **only when non-empty**; `to_json` guards it with `if self.job_id:` before
  `body["job_id"] = self.job_id`.
- `cost` — see below.

**Cost measurement: yes, by `measure_call_cost(outcome)`.** It returns
`calls`, `parse_retried`, `response_chars`, `schema_v`, `usage`,
`usage_source`. When the provider reported a usage block, `usage` is
`{input_tokens, output_tokens, cache_read, cache_creation, total_cost_usd}`
and `usage_source` is `"measured"`; otherwise:

    cost["usage"] = None
    cost["usage_source"] = USAGE_UNMEASURED

with `USAGE_UNMEASURED = "unmeasured"`. The parse is delegated to
`packages/orchestration/token_actuals.py`, symbol `parse_cli_result`, via
`from packages.orchestration.token_actuals import parse_cli_result`.

Iterations that never reached the provider (the safe-point stop, the
no-provider terminal) hard-code `{"calls": 0, "usage": None, "usage_source":
USAGE_UNMEASURED}`.

---

## Q2 — the pause seam

**Status writer:** `set_mission_status`, in
`packages/orchestration/mission_state.py`. It validates against
`MISSION_STATUSES`, then `replace(mission, status=status)` and `save_mission`
(which writes atomically via `_atomic_write`). Its docstring:

    """Set a mission's status.  Only ever called by an explicit human command.

Callers today: `apps/cli/commands/mission_cmd.py` (`_cmd_mission_set_status`,
verb mapped by `_status_for_verb`, whose table row is
`"pause": MISSION_STATUS_PAUSED,`) and
`orchestrator_loop.execute_move` for `MISSION_STATUS_ABANDONED`. `paused` is
written by **nothing** in `packages/` today — the CLI verb is its only writer.

**The guard: re-evaluated EVERY iteration, from a record RE-READ from disk.**

Enclosing function: `run_mission` in
`packages/orchestration/orchestrator_loop.py`. The loop structure that settles
it — the guard sits inside the `for step in ...` body, after the safe point and
before any of the iteration's work, and `load_mission` is called on each pass
(elided, `...` marks omitted lines):

    for step in range(1, bounds.max_iterations + 1):
        iteration = base + step - 1
        ... stop_requested / consume_stop ...
        mission = load_mission(pid, mission_id, root)
        if mission.status != MISSION_STATUS_ACTIVE:
            result.terminal = TERMINAL_NOT_ACTIVE

The deciding line is the assignment, not the comparison:

    mission = load_mission(pid, mission_id, root)

`load_mission` re-reads `mission_record_path(...).read_text(...)` and rebuilds
a frozen `Mission` from JSON, so there is no cached object and no in-memory
staleness. The name `mission` is rebound before the guard on every pass; the
value assembled into that iteration's context is the same fresh object.

**Verdict for T002's acceptance.** "Trip on iteration k pauses before iteration
k+1 dispatches" already holds structurally: a watchdog that calls
`set_mission_status(..., MISSION_STATUS_PAUSED)` between iterations is observed
at the top of the next pass, before `refresh`, before `assemble_context`,
before the provider call and before `execute_move`. **No prerequisite change to
the loop is needed** for the pause to be seen. This answer is NOT entry-only.

Three consequences T002 must plan around, all read off the same block:

1. The guard returns `result` **directly** — not `build_boundary_handoff(result,
   root)`, which the stop path and the iteration-limit path both use. A
   watchdog pause therefore produces **no boundary handoff** and so no F079
   resume seed, unlike an operator stop.
2. The guard writes **no ledger entry**. `_record` is not called on that path,
   so the run's own account ends at iteration k. Anything the feature wants on
   the ledger for the pause (`watchdog_tripped`) has to be appended by the
   watchdog itself, before or as it pauses.
3. `result.iterations = step - 1` — the aborted pass is not counted.

Existing coverage: `tests/orchestration/test_orchestrator_loop.py`,
`TestTheLoopTerminals.test_a_non_active_mission_stops_immediately`, pauses the
mission **before** `run_mission` is called and asserts `result.entries == []`.
There is no existing test that pauses a mission *between* two iterations of a
live run.

---

## Q3 — the milestone link on dispatched jobs

**Answer: there is no milestone field on the job or on the mission record. The
attribution lives in the loop's ledger, and goal_drift IS buildable from it.**

`MissionJobLink` in `packages/orchestration/mission_state.py` carries exactly
three fields — `job_id: str`, `role: str`, `created_at: str` — and
`to_json` writes exactly those three. `role` is one of `MISSION_ROLE_INITIAL` /
`MISSION_ROLE_FOLLOW_UP` (`MISSION_ROLES`), which is chain position, not
milestone. `link_job_to_mission` constructs the link and passes no milestone.

The dispatch path, `execute_move` in `orchestrator_loop.py`, calls
`continue_mission` (`mission_state.continue_mission`) with the payload's
`step` only — the `milestone_id` is used for the DoD copy and the human-readable
detail, and is never handed to job creation:

    job = create(project_id, mission_id, payload["step"], root=root,

`attach_milestone_dod` does copy the milestone's compiled DoD onto the job, but
that is a DoD artifact under the job's evidence area, not a milestone id: a
milestone with no `dod_ref` "stores NOTHING", so it is not a reliable link.

The link that DOES exist is stated outright by `dispatched_job_for` in
`orchestrator_loop.py`:

    The mission record attributes a job to the MISSION, not to a milestone

and the pairing it reads is `move.payload.milestone_id` against
`outcome.job_id` on `dispatch_job` ledger entries:

    if (move.get("payload") or {}).get("milestone_id") != milestone_id:

`milestone_id` is a REQUIRED, non-blank payload key for that move kind —
`packages/orchestration/orchestrator_move_schema.py`,
`REQUIRED_PAYLOAD_KEYS`:

    MOVE_DISPATCH_JOB: ("milestone_id", "step"),

enforced at parse time by `OrchestratorMove._validate_payload`. So **every
dispatch entry on the ledger carries a milestone id by construction**, and an
entry that actually produced a job also carries `outcome.job_id`
(`MoveOutcome.job_id`, set by `execute_move`).

The "current milestone" side of goal_drift is available from the same module:
`milestone_ids(mission)` (plan order, via `mission_compiler.mission_plan_of`),
`done_milestones(mission)` (reads `MILESTONES_DONE_KEY = "_milestones_done"`
off the persisted plan body) and `mark_milestone_done` (the writer, through
`set_mission_plan`). `collect_milestone_evidence` is the existing reader that
already joins ledger attribution to job state.

**Conclusion:** goal_drift as specified ("dispatched jobs whose plan references
no current milestone") is buildable — the comparison is
`ledger dispatch_job payload.milestone_id` vs `milestone_ids(mission)`. The
feature file's parenthetical "every loop-dispatched job carries its milestone
link — assert that link exists from the loop feature" is **false as written if
read as a field on the job**; it is true only of the ledger. This is a
documentation mismatch, not a blocker.

---

## Q4 — the burn signal

**From the ledger alone: partially. Per-iteration ORCHESTRATOR call cost is
readable; the cost of the JOB each dispatch runs is not.**

Available from `read_ledger` (`packages/orchestration/orchestrator_loop.py`)
with no second source: each entry's `cost` block, produced by
`measure_call_cost` in the same module — `calls`, `parse_retried`,
`response_chars`, `schema_v`, `usage`, `usage_source`. When measured, `usage`
carries `input_tokens`, `output_tokens`, `cache_read`, `cache_creation` and
`total_cost_usd`. The parser is
`packages/orchestration/token_actuals.py`, `parse_cli_result` →
`UsageActuals`. That module's docstring names it the measured source —
`This is the source of *measured* token/cost data` — and adds that callers
`fall back to a heuristic estimate when parsing fails (returns None)`.

Two honesty constraints a trailing baseline has to survive:

- `usage` is `None` and `usage_source` is `"unmeasured"` whenever the provider
  reported nothing, and for every entry the loop writes without a call. A
  baseline must treat those as absent, never as zero — the repo's P6 rule,
  stated in `measure_call_cost` as "Remedy never writes an estimate into a
  field named ``usage``".
- `total_cost_usd` is `None` unless the provider reported one, so a USD-based
  rate is not always computable; `input_tokens`/`output_tokens` are the
  denser signal.

**Not in the ledger, and the other source if T001 wants it.** The
`cost` block measures the orchestrator's own structured call
(`run_structured_call`) only. The builder/reviewer spend of the job that
`execute_dispatched_job` runs is recorded through the job's evidence area and
aggregated by `packages/orchestration/token_ledger.py` — the sqlite ledger at
`token_ledger_path_for`, written by `record_call`/`backfill_ledger`, read by
`query_cost` (which takes a `job_id=` filter and returns a `CostReport`).
Reaching it from a mission means joining `outcome.job_id` off the ledger to
`query_cost(job_id=...)`. Note that in production `backfill_ledger` has exactly
one caller, the CLI `_cmd_stats_backfill_ledger` in
`apps/cli/commands/stats_ledger_cmd.py`, so that sqlite ledger is **not
guaranteed populated** during a live mission run; the per-task-run
`token_accounting.json` under the job's evidence dir
(`token_ledger._TOKEN_ACCOUNTING_FILENAME`) is the underlying artifact.

For a self-relative trailing baseline over the loop's own iterations, the
mission ledger alone is sufficient.

---

## Q5 — test ground

**`packages/orchestration/watchdog.py` — not present.**
**`tests/orchestration/test_watchdog.py` — not present.**
Searched: `find` for `*watchdog*` across the repo (no hits outside `.git`),
`grep -rln watchdog packages apps tests` (one hit,
`packages/orchestration/stream_evidence.py`, an unrelated local
`threading.Thread` named `watchdog` inside a timeout helper), and
`grep -rn watchdog_tripped` (only `docs/roadmap/features/T2_F077.md` and the
`.agent/` planning files). Both paths the feature file suggests are free.

**Reusable ground already in `tests/orchestration/`:**

| Path | Symbol | What it gives T001 |
|---|---|---|
| `tests/orchestration/test_orchestrator_loop.py` | `_entry` | a `LedgerEntry` factory taking an iteration number, a move kind and `**outcome`; already sets `cost` to the unmeasured shape |
| `tests/orchestration/test_orchestrator_loop.py` | `_plan` | a `MissionPlan` from `(id, depends_on)` pairs |
| `tests/orchestration/test_orchestrator_loop.py` | `mission` (pytest fixture) | a persisted mission under `tmp_path` with a compiled two-milestone plan (`M001`, `M002` depending on `M001`) |
| `tests/orchestration/test_orchestrator_loop.py` | `_move_json` | a schema-valid `OrchestratorMove` JSON string |
| `tests/orchestration/test_orchestrator_loop.py` | `_scripted`, `_FakeJob`, `_FakeCycleRun`, `_executed`, `dispatched` | the loop's dispatch/execute seam doubles |
| `tests/orchestration/test_orchestrator_loop.py` | `TestMilestoneAttributionComesFromTheLedger` | the existing pin on the Q3 attribution |
| `tests/orchestration/fixtures/mission/` | `cli_onboarding.json`, `docs_portal.json`, `payments_platform.json` | three mission+plan fixtures, loaded via `FIXTURE_DIR` in `tests/orchestration/test_mission_compiler.py` |
| `tests/orchestration/fixtures/dod/` | `api_service.json`, `cli_tool.json`, `docs_site.json` | compiled DoDs, if a fixture needs a gated job |

There is **no** fixture ledger file on disk anywhere: every ledger in the suite
is built in-process with `_entry` + `append_ledger_entry` under `tmp_path`.
There is no `conftest.py` in `tests/orchestration/`; the only one is
`tests/conftest.py`.

---

## Open questions for T001

The code does not settle these; each needs a decision before or during T001.

1. **Fixture ledgers: on disk or in-process?** The suite has no precedent for a
   ledger fixture file, and `_entry` lives inside a 2504-line test module with
   no `conftest.py` to import it from. Whether T001 adds JSONL fixtures or a
   shared factory is an open choice.
2. **What counts as "a state change in the mission plan"** for no_progress. The
   plan body's only mutable list is `MILESTONES_DONE_KEY`; `set_mission_plan`
   can rewrite the whole body, and nothing versions or timestamps it, so
   "changed since iteration k" is not directly readable from the record. The
   ledger's `declare_milestone_done` entries are the only timestamped signal.
3. **Which entries count as "dispatched"** for no_progress and goal_drift. A
   REFUSED dispatch keeps `kind == "dispatch_job"` and its `milestone_id` but
   carries no `outcome.job_id` (R-0192, encoded in `dispatched_job_for`).
   Whether a repeated *refused* dispatch is no-progress or is already handled by
   the loop's own second-refusal escalation is undecided.
4. **Gaps in iteration numbering.** `read_ledger` skips torn lines and
   `next_iteration_index` continues across runs, so consecutive list positions
   are not consecutive iterations. Whether the sliding windows count entries or
   iteration numbers is undecided.
5. **Baseline minimum sample.** The feature file says the burn tripwire is
   "inert until a minimum sample (documented)" but names no number; no config
   key exists. `CONFIG_KEY_MAX_ITERATIONS = "orchestrator.max_iterations"` is
   the only orchestrator config key in `orchestrator_loop.py`, so the
   `watchdog.*` namespace is unclaimed.
6. **Unmeasured iterations in the burn window.** `usage_source ==
   "unmeasured"` entries cannot contribute to a rate. Whether they shrink the
   window, void it, or are skipped is undecided.
7. **Where a watchdog decision attaches.** `escalate_repeated_refusal` shows
   the only existing mission→decision path: `escalation.enqueue_task_decision`
   attaches to the mission's LATEST linked job's first task, and returns a
   plain-English refusal string when the mission has no job or no task. A
   watchdog that trips before any job was dispatched has nowhere to attach a
   decision. `decision_queue.HumanDecision` is the record type; its dedup key
   for "one decision per trip class until resolved" is unspecified.
8. **`Trip` has no home yet.** The feature file names `evaluate(mission) ->
   list[Trip]` but no `Trip` type exists; whether the evidence triple ("what,
   since when, the numbers") is a dataclass or a dict is undecided.
9. **Invocation point.** The feature wants the watchdog "called by the loop
   between iterations", but the only pause-observing seam in `run_mission` is
   the top-of-iteration guard, and T002 is explicitly scoped to the loop
   integration. T001 stays pure and does not touch `run_mission`.
