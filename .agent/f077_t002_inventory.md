# F077 T002 — inventory of the decision, pause and ledger paths

> READ-ONLY. Nothing under `packages/`, `apps/`, `tests/` or `docs/` changes
> because of this file, and no part of T002 is built here.
>
> **Line numbers are deliberately omitted** (R-0353). Every answer names a FILE
> and a SYMBOL, because a symbol survives an edit above it and a line number
> does not. Quotes are verbatim from disk at this commit; any elision is marked
> `[...]`.

## 1. Where a watchdog decision attaches when there is no job

### `enqueue_task_decision` — `packages/orchestration/escalation.py`

It has **no jobless or taskless guard at all**. It never returns early and never
raises on a missing job; it takes `task_id` as an argument, builds a record and
appends it. Its docstring states the no-dedup position:

```
    """Enqueue ONE decision for *task_id* and return its record.

    One call, one record — a task raising the same question twice really did
    ask twice.  Records whose question matches an existing OPEN one are
    cross-referenced in both directions (``cross_references``) so a human sees
    the pair without the code guessing they are the same call.
    """
```

The nearest thing to a guard is tolerance, not refusal. `_stored_records`
(same file) creates the list if absent, and `_metadata` (same file) falls back
to a bare `meta = {}` when `getattr(job, "metadata", None)` is not a dict,
swallowing the `AttributeError, ValueError` from assigning it back on frozen
shapes. Consequence: on a frozen or metadata-less object the record is written
into a throwaway dict and is **silently lost**. Persistence is the caller's job
— the writer never calls `save_job`.

### `escalate_repeated_refusal` — `packages/orchestration/orchestrator_loop.py`

Its docstring names the gap outright: "The decision is enqueued on the
mission's most recent job, because that is the object
``escalation.enqueue_task_decision`` attaches to; a mission with no job yet has
nowhere to attach one, and that is reported rather than papered over."

The three guards each **return a human-readable string**. None raises, none
records anything:

```
    mission = load_mission(project_id, mission_id, root)
    link = mission.latest_link()
    if link is None:
        return ("no job is linked to this mission, so the refusal cannot be "
                "attached to a decision — a human has to look at the mission")
    try:
        job = load_job(_as_uuid(link.job_id))
    except Exception as exc:
        return f"the mission's latest job could not be read to escalate: {exc}"
    tasks = list(getattr(job, "tasks", ()) or ())
    if not tasks:
        return (f"job {link.job_id} has no task to attach the decision to")
```

The happy path attaches to `tasks[0].id`, calls `save_job(job)` and returns the
decision id. In `run_mission` the returned string is interpolated into the
ledger entry's `outcome.detail` as `handle`, so a failed attachment and a
successful one produce the **same terminal and the same status** — only the
prose differs, and no decision record exists in the failure case.

### Is there any existing decision path that attaches to a MISSION?

**No.** Every producer branch of `list_decisions`
(`packages/orchestration/decision_queue.py`) is job-scoped or global-scoped:
patch approvals, stop reasons, test failures, dirty repo, token budget, memory
review, flight-plan approval, task decision. `Mission`
(`packages/orchestration/mission_state.py`) carries no decisions field.

The only mission-level symbol is a READ aggregation, `open_mission_decisions`
in `packages/orchestration/orchestrator_loop.py`, which walks `mission.job_links`
and concatenates `open_task_decisions(job)`.

**The code does not settle where a watchdog decision attaches on a jobless
mission.** Options and their consequences:

- **(a) reuse `enqueue_task_decision` on `mission.latest_link()`'s first task**,
  exactly as `escalate_repeated_refusal` does. Costs nothing new and
  `remedy decision resolve` answers it for free, because `_cmd_decision_resolve`
  (`apps/cli/commands/decision.py`) already dispatches on the `td:` prefix. But
  it degrades to a returned string on a jobless mission, and the decision id
  namespaces the trip to a task that has nothing to do with it.
- **(b) add a mission-anchored store plus a new `DECISION_TYPES` member and a
  ninth `list_decisions` branch.** Works for jobless missions, but
  `list_decisions(job, events)` takes a JOB, so the derivation surface and the
  three `remedy decision` verbs would need a mission entry point that does not
  exist today.
- **(c) refuse to trip on a jobless mission.** Cheapest and honest. Checked
  against the tripwires: `evaluate_no_progress` and `evaluate_goal_drift`
  (`packages/orchestration/watchdog.py`) both fire only off `dispatched_entries`,
  which requires a non-empty `outcome.job_id`, so a trip in those two classes
  implies a job exists. Only `evaluate_burn_anomaly` can fire with no job.

## 2. The decision record

`HumanDecision` — `packages/orchestration/decision_queue.py`, a frozen
dataclass. Fields in declaration order: `id`, `type`, `status`, `severity`,
`source`, `related_node_id`, `related_intent_id`, `related_file`,
`safe_summary`, `next_actions` (`tuple[str, ...]`), `created_at`,
`resolved_at` (`str | None`), and `payload` (`dict[str, Any]`, the only field
with a default, `field(default_factory=dict)`). The `payload` comment:

```
    #: Structured extras for decisions that carry more than a summary line.
    #: Additive (F034): every existing producer omits it and gets ``{}``.
    #: The flight-plan approval uses it to bundle the plan's open
    #: clarifications, so one decision covers the whole plan.
```

`DECISION_TYPES`, same file, verbatim:

```
DECISION_TYPES = frozenset({
    "patch_approval", "stop_reason", "test_failure", "repo_dirty",
    "token_budget", "worker_approval", "memory_review", "revert_missing",
    "flight_plan_approval",
    # F051: a task raised a question mid-run; its branch waits, the run does not.
    "task_decision",
})
```

Ten values. Nothing validates `HumanDecision.type` against the set — it is a
vocabulary, not a registry, and two members (`worker_approval`,
`revert_missing`) have no producing branch.

**What identifies a decision uniquely.** There is no central generator.
`HumanDecision.id` is a per-producer literal or f-string, and `get_decision`
(same file) matches on `d.id == decision_id` by linear scan. The one real
generator is `_next_decision_id` in `packages/orchestration/escalation.py`:

```
    """``td:<task8>`` for a task's first decision, ``td:<task8>-<n>`` after.

    Task-scoped and deterministic: no clock and no randomness, so the same
    sequence of escalations always produces the same ids across a resume.
    """
```

**Which field could carry a per-trip-class dedup key.** `HumanDecision` is
DERIVED, never stored — `list_decisions` rebuilds it on every call — so a dedup
key must live on the stored record, not on the dataclass. On the stored
escalation record, `enqueue_task_decision` builds a fixed-key dict
(`decision_id`, `task_id`, `question`, `options`, `safe_default`, `impact`,
`status`, `answer`, `answer_source`, `created_at`, `answered_at`,
`cross_references`) and accepts no extras argument. The de-facto identity today
is `question`, folded by `_normalized_question` (same file) — but it is used
only to populate `cross_references`, never to suppress. On the derived side,
`payload` is the documented additive channel, and `id` itself already acts as a
de-facto dedup key for the constant-id producers (`fp:approval`, `dirty_repo`).

**Does any existing writer dedup before enqueuing? None does.** Three writers
exist and all three enqueue unconditionally: `enqueue_task_decision` itself,
`_escalate_task` (`packages/orchestration/long_run_executor.py`) and
`escalate_repeated_refusal` (`packages/orchestration/orchestrator_loop.py`).
The module docstring of `packages/orchestration/escalation.py` declines dedup
as a matter of policy:

```
Two tasks raising the same question produce TWO records (deduplication is a
human call, feature-file A9); they cross-reference each other by decision id so
whoever answers sees the pair.
```

That is in direct tension with F077's "one decision per trip class, deduped
until resolved" and a T002 block must name which one wins.

## 3. What "until resolved" is on disk

**The answer writer** is `answer_task_decision`,
`packages/orchestration/escalation.py`. It refuses anything not currently open
(`if record is None or record.get("status") != ESCALATION_STATUS_OPEN: return
None`), then writes four keys: `record["status"] = ESCALATION_STATUS_ANSWERED`,
`record["answer"]`, `record["answer_source"]` and
`record["answered_at"] = now.isoformat()`, and calls `_record_answer_on_task`.

It does not persist; `_cmd_decision_resolve` in
`apps/cli/commands/decision.py` calls `save_job`. `auto_apply_safe_default`
(same escalation module) is the second entry point for unattended runs.

**Two vocabularies distinguish open from resolved.** On disk the marker is the
record's `status`, `ESCALATION_STATUS_OPEN` (`"open"`) versus
`ESCALATION_STATUS_ANSWERED` (`"answered"`), read by `open_task_decisions` and
`answered_task_decisions` in `escalation.py`. In the queue layer the marker is
`HumanDecision.status`, `"open"` versus `"resolved"`, read by `open_decisions`
in `decision_queue.py`; `get_decision` in the same file finds one by id.
The translation happens inside the `task_decision` branch of `list_decisions`.
`"answered"` never appears as a `HumanDecision.status` and `"resolved"` never
appears on disk.

**What "resume clears exactly that trip's dedup" would have to read — the code
does not settle this.** Two things are missing, not one: there is no dedup key
anywhere today, **and there is no mission resume verb at all**.
`_status_for_verb` in `apps/cli/commands/mission_cmd.py` maps three verbs only:

```
    return {
        "achieve": MISSION_STATUS_ACHIEVED,
        "abandon": MISSION_STATUS_ABANDONED,
        "pause": MISSION_STATUS_PAUSED,
    }[verb]
```

`apps/cli/command_catalog.py` registers `mission.achieve`, `mission.abandon`
and `mission.pause`; a search for `mission.resume` or `mission.activate` across
`apps/` and `packages/` returns nothing. A paused mission has no supported path
back to active. Options for what a clear would read:

- **(a) the decision's own resolution state.** Dedup means "an open decision of
  this trip class exists"; answering it clears the suppression with no extra
  state. Needs a class marker on the stored record, which
  `enqueue_task_decision` cannot currently write.
- **(b) a stored key on the mission record.** `Mission` has no free-form dict,
  so this touches its serialization; the `mission_plan` field is the precedent
  for an additive optional key without a schema bump.
- **(c) a file under `mission_evidence_dir`.** No schema change, but a second
  source of truth beside the queue, which `decision_queue.py`'s own docstring
  rules out.
- **(d) derive it from the ledger.** A `watchdog_tripped` entry IS the trip and
  a later entry supersedes it. Append-only and consistent with the watchdog's
  read-only stance, but it has no notion of "answered".

Whichever is chosen, T002 must also decide **who resumes**, because no verb does.

## 4. Appending `watchdog_tripped` from outside the loop

`_record` nested inside `run_mission`
(`packages/orchestration/orchestrator_loop.py`) closes over `pid`,
`mission_id`, `root`, `now` and `result`, so it is unreachable from outside:

```
    def _record(iteration: int, digest: str, move: dict[str, Any],
                outcome: MoveOutcome, cost: dict[str, Any]) -> None:
        entry = LedgerEntry(iteration=iteration, context_digest=digest,
                            move=move, outcome=outcome.to_json(), cost=cost)
        append_ledger_entry(pid, mission_id, entry, root, now=now)
        result.entries.append(entry)
```

(A second, unrelated `_record` lives at module scope inside
`make_orchestrator_call_recorder` and writes prompt traces, not ledger entries.)

**The supported external path** is the pair `_record` itself uses, both
module-level in the same file: build a `LedgerEntry` and hand it to
`append_ledger_entry(project_id, mission_id, entry, root=None, *, now=None)`,
whose docstring is the contract — "Append one entry. Never rewrites, never
truncates, never reorders."

Supporting symbols in the same module: `next_iteration_index` for numbering,
`ledger_path` / `read_ledger` / `render_ledger` on the read side, `MoveOutcome`
for the outcome shape and `USAGE_UNMEASURED` for the cost shape.

**Precedent for the `move` and `outcome` shape.** Every ledger entry the loop
writes with no model move behind it passes `{}` as `move`. The five precedents,
all inside `run_mission`: the stop-request entry passes `("", {}, outcome,
{"calls": 0, "usage": None, "usage_source": USAGE_UNMEASURED})`; the
no-provider entry passes the real digest with `{}` and the same zero cost; the
invalid-move entry passes `{}` with the MEASURED cost; the escalation entries
pass `{}` in the R-0190 blocked-gate and R-0196 boundary cases and
`move.model_dump()` only in the second-refusal case where a real move exists;
and both iteration-failure entries — terminal and `OUTCOME_ITERATION_RETRYING`
— pass `{}`.

So by precedent a `watchdog_tripped` entry takes `move={}`,
`context_digest=""` and `cost={"calls": 0, "usage": None, "usage_source":
USAGE_UNMEASURED}`.

**The evidence triple has no home, and the code does not settle where it goes.**
`MoveOutcome` is `status`, `detail`, `terminal`, `job_id`, and its `to_json`
emits only `status`, `detail` and — when set — `job_id`. `Trip.to_json`
(`packages/orchestration/watchdog.py`) emits `kind`, `what`, `since_iteration`
and `numbers`. Options: flatten the triple into `detail` as prose; bypass
`MoveOutcome` and pass a raw dict to `LedgerEntry.outcome`, which is legal
because the field is `dict[str, Any]`; or add a field to `MoveOutcome`, which
`render_ledger` would not print since it reads only status and detail.

**Numbering hazard, named here so a block does not discover it late.**
`run_mission` computes `base = next_iteration_index(pid, mission_id, root)`
ONCE before the loop and then uses `iteration = base + step - 1`, while
`next_iteration_index` re-reads the file and returns one past the highest
recorded. An external append mid-run therefore takes a number the loop is
already going to reuse.

## 5. The pause writer

`set_mission_status` — `packages/orchestration/mission_state.py`. Docstring
verbatim:

```
    """Set a mission's status.  Only ever called by an explicit human command.

    Deliberately absent: any rule that moves a mission to ``achieved`` because
    its jobs finished.  A finished job is not an achieved goal, and this
    feature does not pretend otherwise — see the module docstring.
    """
```

**The block's premise that `paused` is written only by the CLI verb holds, but
the docstring's first sentence is ALREADY false for other statuses.**
`MISSION_STATUS_PAUSED` appears outside tests only in `mission_state.py` itself
and in `apps/cli/commands/mission_cmd.py` (`_status_for_verb`, reached from the
`mission.pause` handler entry, whose body is `_cmd_mission_set_status`). But
`set_mission_status` has two autonomous callers today, both in
`packages/orchestration/orchestrator_loop.py`: `mission_achieved`, which writes
`MISSION_STATUS_ACHIEVED` for `MOVE_DECLARE_MISSION_ACHIEVED`, and
`execute_move`, which writes `MISSION_STATUS_ABANDONED` for
`MOVE_ABORT_WITH_REASON`. Neither is a human command.

So the watchdog would be the third autonomous caller and the FIRST autonomous
writer of `paused`. The docstring is stale independently of F077.

Smallest honest amendment, proposed and **not applied**:

```
    """Set a mission's status.

    Callers are the explicit human verbs (``remedy mission achieve|abandon|
    pause``), the loop's own terminal moves (``declare_mission_achieved``,
    ``abort_with_reason``), and — since F077 — the autonomy watchdog, which
    writes ``paused`` and nothing else.

    Deliberately absent: any rule that moves a mission to ``achieved`` because
    its jobs finished.  A finished job is not an achieved goal, and this
    feature does not pretend otherwise — see the module docstring.
    """
```

Note that `_cmd_mission_set_status`'s own docstring carries the same claim
("Nothing in Remedy moves a mission between statuses on its own (F056)") and
would need the same treatment; that is a second decision, not a free rider.

## 6. The loop-integration seam

**Exactly one test pauses a mission around a run:**
`TestTheLoopTerminals.test_a_non_active_mission_stops_immediately` in
`tests/orchestration/test_orchestrator_loop.py`:

```
    def test_a_non_active_mission_stops_immediately(self, tmp_path, mission,
                                                    dispatched):
        set_mission_status(PROJECT, mission.id, "paused", tmp_path)
        result = run_mission(
            mission.id, LoopLimits(max_iterations=3), project_id=PROJECT,
            call_fn=_scripted(_move_json("wait_on_decisions")), root=tmp_path,
            dispatch=dispatched, execute=_executed, control_root_path=tmp_path / "control")
        assert result.terminal == TERMINAL_NOT_ACTIVE
        assert result.entries == []
```

It pauses BEFORE the run. No existing test pauses between iterations.

**The seam already exists.** At the top of `run_mission`'s iteration loop,
after the stop-request safe point and before any work:

```
        mission = load_mission(pid, mission_id, root)
        if mission.status != MISSION_STATUS_ACTIVE:
            result.terminal = TERMINAL_NOT_ACTIVE
            result.detail = f"mission status is {mission.status}"
            result.iterations = step - 1
            return result
```

It returns without a ledger entry and without `build_boundary_handoff`, which
is why the existing test can assert `result.entries == []`.

**How to prove "a trip on iteration k pauses before iteration k+1 dispatches".**
The structural precedent is
`TestHumanOverridesWinInstantly.test_a_stop_request_between_iterations_halts_within_one_iteration`
in the same file. Its local `dispatch` double appends to a `seen` list and,
`if len(seen) == 1`, calls `request_stop(mission.id, reason="operator says
stop", control_root_path=control)` before returning `_FakeJob`; the test then
asserts `result.terminal == TERMINAL_STOPPED`, `seen == [1]` and that the
reason is in `result.detail`, under the comment "Exactly ONE dispatch: the stop
landed at the very next safe point, not at the end of the five permitted
iterations."

A T002 test copies that shape and swaps `request_stop` for whatever the
watchdog seam is, then asserts `seen == [k]` and
`result.terminal == TERMINAL_NOT_ACTIVE`.

**Fixtures and doubles available.** There is no `tests/orchestration/conftest.py`;
only `tests/conftest.py` (autouse `_reset_config_cache`, autouse
`_restore_cwd`, and `pytest_collection_modifyitems`). Everything else is local
to `tests/orchestration/test_orchestrator_loop.py`: the `mission` fixture
(a persisted mission under `tmp_path` with a two-milestone plan, `PROJECT`),
the `dispatched` fixture (records `(project_id, mission_id, step)` into
`.seen`, returns `_FakeJob`), and the helpers `_plan`, `_move_json`,
`_scripted`, `_FakeJob`, `_FakeCycleRun`, `_executed`, `_met_evidence`,
`_released`, `_finishing` and `_plan_moves`. Control signals come from
`request_stop` / `stop_requested`, driven by `control_root_path`. Every
`run_mission` call in the file passes `root=tmp_path`.

## 7. Guards no future block will name

Searched `tests/` with `rg -l` for `read_ledger|ledger_path|LEDGER_FILENAME`
and for `list_decisions|open_decisions|DECISION_TYPES`, then read every
`count(` and `== <n>` assertion in the results.

### A new LEDGER ENTRY KIND would break these

All in `tests/orchestration/test_mission_e2e.py`, class
`TestTheLedgerSpansBothRuns`, which reads the whole ledger file:

- `test_every_iteration_is_numbered_once_across_both_runs` —
  `assert numbers == [1, 2, 3, 4, 5, 6, 7]`. A whole-file list equality; an
  eighth entry breaks it, and a mid-run append also duplicates a number.
- `test_the_ledger_records_the_moves_in_the_order_they_happened` —
  `assert [e["move"]["kind"] for e in e2e["ledger"]] == [` seven kinds `]`.
  Breaks twice over: the length changes AND `e["move"]["kind"]` raises
  `KeyError` on an entry whose `move` is `{}`, because it is a bare subscript.
- `test_every_entry_carries_a_context_digest_and_cost` — universally quantified
  over the file: `assert entry["context_digest"].startswith("sha256:")` and
  `assert entry["cost"]["calls"] == 1`. A watchdog entry with the precedent
  shape (`digest=""`, `calls=0`) fails both.
- `test_no_move_was_refused` — `assert "escalated" not in statuses`. Survives a
  new kind, breaks if the watchdog reuses `TERMINAL_ESCALATED`.

In `tests/orchestration/test_orchestrator_loop.py`:

- `TestTheLedger.test_every_entry_carries_a_context_digest_and_cost` (same test
  name as the e2e one, different file) — same universal quantification over
  `read_ledger(...)`.
- `test_the_failing_iteration_still_leaves_a_ledger_entry` —
  `assert len(entries) == 1`, a whole-file count. Single-iteration run, so it
  breaks only if the watchdog evaluates before or during iteration 1.
- `test_no_provider_is_a_terminal_not_an_exception` —
  `assert len(result.entries) == 1`, same caveat.
- `test_a_non_active_mission_stops_immediately` — `assert result.entries == []`
  breaks if T002 makes the not-active return path write an entry.
- Position-sensitive: `assert statuses[-1] == TERMINAL_ACHIEVED` and
  `assert entries[-1]["outcome"]["status"] == TERMINAL_ACHIEVED` break if a
  watchdog entry is appended AFTER the terminal one;
  `assert entries[0]["outcome"]["status"] == OUTCOME_ITERATION_RETRYING` breaks
  if one is appended before the first.

Not broken: `assert statuses.count(OUTCOME_ITERATION_RETRYING) == 2` and the
other `.count(` assertions count a specific value, not the file; and
`assert [e["iteration"] for e in read_ledger(...)] == [1, 3]` in
`test_a_torn_line_costs_one_entry_not_the_history` uses `append_ledger_entry`
directly with no `run_mission`.

### A new DECISION TYPE would break nothing found

Every `DECISION_TYPES` assertion in the suite is membership only —
`assert "patch_approval" in DECISION_TYPES` and its siblings in
`tests/orchestration/test_approval_queue.py`, `tests/cli/test_plan_approval.py`,
`tests/orchestration/test_escalation.py` and
`tests/orchestration/test_budget_stop_integration.py`. There is no
`len(DECISION_TYPES) == n` anywhere.

Every decision COUNT is type-filtered before the count —
`len(dirty_decs) == 1` in `tests/orchestration/test_approval_queue.py`,
`len(derived) == 1` in `tests/orchestration/test_escalation.py`,
`len(open_decisions) == 0` in `tests/cli/test_plan_approval.py`, and the
`token_budget` filters in `tests/orchestration/test_budget_stop_integration.py`
and `tests/orchestration/test_f018_authority_integration.py`.

The one mission-scoped whole-queue count is
`TestTheEscalatedDecision.test_exactly_one_decision_is_open_when_the_run_pauses`
in `tests/orchestration/test_mission_e2e.py`, which asserts
`len(e2e["open_at_pause"]) == 1` over `open_mission_decisions`. It holds only
because the scripted e2e run never trips a tripwire; it is the single most
fragile decision guard for F077.

## Open questions for T002

1. **Attachment on a jobless mission** — reuse the task-scoped writer and accept
   the string-return degradation, add a mission-anchored store, or refuse to
   trip. §1 options (a)/(b)/(c). Only `burn_anomaly` can fire with no job.
2. **Dedup versus the A9 policy** — `escalation.py` declines dedup by design and
   F077 requires it. Which wins, and where the trip-class marker lives, given
   that `enqueue_task_decision` writes a fixed key set.
3. **What clears the dedup** — §3 options (a)-(d), all unbuilt.
4. **Who resumes a paused mission** — there is no `mission.resume` verb, so a
   watchdog pause is currently terminal for the run in practice.
5. **Where the evidence triple lives in a ledger entry** — prose in `detail`, a
   raw dict bypassing `MoveOutcome`, or a new `MoveOutcome` field that
   `render_ledger` will not print.
6. **Iteration numbering for an out-of-band entry** — `base` is computed once
   per run, so an external append collides with the loop's own numbering.
7. **Whether T002 amends the two stale docstrings** — `set_mission_status` and
   `_cmd_mission_set_status` both claim no autonomous status writes, which is
   already false for `achieved` and `abandoned`.
8. **Which existing assertions T002 budgets for** — the four
   `test_mission_e2e.py` whole-ledger guards in §7 are the hard ones.
