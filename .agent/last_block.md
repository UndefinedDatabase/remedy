── STEP T003-build/1 of 2 — F077 Autonomy watchdog · R14 ─────────

Goal:        Record R13's verdict, then BUILD the first half of T003 against
             `.agent/f077_t003_inventory.md`: a read-only mission-shaped
             evaluation entry point, the manual `remedy mission watchdog <id>`
             audit command, and the `mission resume` verb DECISION F077 D4
             scoped. The report surface is R15 and is NOT built here.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r14.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   FINDINGS FIRST, own commit: append the authored GATE-R13 slice to the
       END of `.agent/live_review.md`. It is the ONLY slice for that file.
  C2   `packages/orchestration/watchdog.py`: extract the read-only composition
       into `evaluate_mission` and route `watchdog_pass` through it; tests in
       `tests/orchestration/test_watchdog.py`
  C3   `remedy mission watchdog <id>` — catalog entry, handler, registry entry;
       tests in `tests/cli/test_mission_cmd.py`
  C4   `remedy mission resume <id>` — verb, registry entry, catalog entry, the
       authored module-docstring pair; tests in the same test file
  C5   append the authored DECISION-D12 slice to `.agent/decisions.md`, then
       mirror the round into `.agent/plan.md` and `.agent/context.md`
  C6   handback: rewrite `.agent/handoff.md`

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r14.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
             `.agent/context.md`, `.agent/handoff.md`,
             `packages/orchestration/watchdog.py`,
             `apps/cli/command_catalog.py`,
             `apps/cli/commands/mission_cmd.py`,
             `tests/orchestration/test_watchdog.py`,
             `tests/cli/test_mission_cmd.py`.
             Twelve files. `apps/cli/commands/worker_facade_cmd.py` is NOT in
             this set and must not be touched — inventory Q6 measured two
             exact-set guards there (`test_all_handlers_present`, a 12-key
             literal set, and `test_all_facade_commands_have_handlers`, a
             `== 12`), and either registration there turns both red in the same
             commit.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. 500-INSERTION cap per commit.
  - `.agent/plan.md` stays UNDER 50 lines. It is 44 now.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    The GATE-R13, DECISION-D12 and DOCSTRING slices are reviewer text and are
    applied verbatim. If a fix lands before its resolution is authored, the
    marker is `Landed: R-XXXX — <one line>` and nothing else.
  - The residual `Landed: R-0384` stays. It is the live evidence of OPEN
    finding R-0380 and is outside this change set.
  - The watchdog stays independent: `evaluate_mission` WRITES NOTHING. No
    `set_mission_status`, no `enqueue_task_decision`, no `save_job`, no
    `append_ledger_entry`, directly or through a callee. That is the feature
    file's acceptance criterion, not a preference.
  - Do NOT change any threshold default, any config key, `evaluate_ledger`,
    `evaluate_no_progress`, `evaluate_burn_anomaly`, `evaluate_goal_drift`,
    `act_on_trips`, or `run_mission`'s call site. `watchdog_pass` changes ONLY
    as C2 describes: same name, same signature, same observable behaviour.
  - Do NOT clear, expire or touch the dedup marker in this round. DECISION
    F077 D3 makes clearing a consequence of ANSWERING the decision, and D4's
    HOW TO REVERSE scopes `resume` to "one `_status_for_verb` entry, one
    catalog registration and its test". A `resume` that clears anything is
    outside D4.
  - `.agent/STOP`: re-check from disk before you start and again at handback.
    If it appears, finish the commit in hand, write the handoff, and end.
  - Any destructive check runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout.

Done when: every gate below has been RUN by you and its REAL value recorded.
"Green" as a word is a finding. The round's base commit is `15a075c3`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r14.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R13 — ' .agent/live_review.md` → 1.
      `grep -c '^Landed: ' .agent/live_review.md` → 1, NOT 0.
  4.  Recompute the open-finding set MECHANICALLY — every `^- R-\d+ — `
      paragraph minus every `^Done: R-\d+ — ` line — and report the count and
      the names. This round registers and resolves NOTHING, so 23 open and
      next free `R-0393` is the expected reading. Report what you measure,
      unadjusted.
  5.  `grep -c '^## DECISION F077 D12 ' .agent/decisions.md` → 1.
  6.  `python3 -m pytest tests/orchestration/test_watchdog.py tests/orchestration/test_mission_e2e.py -q`
      → report the number. The reviewer measured `52 passed` at `15a075c3`;
      C2 adds tests, so the number GROWS. Report the real one.
  7.  `python3 -m pytest tests/cli/test_mission_cmd.py -q` → report the number.
      The reviewer measured `83 passed` at `15a075c3`; C3 and C4 add tests.
  8.  `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_worker_facade_cmd.py -q`
      → report the number. The reviewer measured `576 passed` at `15a075c3`.
      This round adds NO test to these three files, so a fall below 576, or
      any failure, is the catalog/help/facade contract rejecting the new
      entries — report it and stop rather than editing these files.
  9.  `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      → report the number. The reviewer measured `196 passed` at `15a075c3`.
      This round adds no test here, so 196 is the expected reading and any
      other number is the `watchdog_pass` change leaking.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `15a075c3`.
  11. `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → report BOTH numbers. The reviewer measured `216 passed, 16648
      deselected` at `15a075c3`. The PASSED number is expected to stay 216;
      the DESELECTED number is expected to grow by exactly the tests this
      round adds, because it counts the whole suite. Do not adjust either.
      Run this AFTER drafting both state files and BEFORE committing C5, and
      grep every test that READS `.agent/plan.md` or `.agent/context.md`
      first, validating your draft against all of it (R-0162).
  12. `python3 -m ruff check packages/orchestration/watchdog.py apps/cli/commands/mission_cmd.py apps/cli/command_catalog.py tests/orchestration/test_watchdog.py tests/cli/test_mission_cmd.py`
      → the reviewer measured `All checks passed!` at `15a075c3` for exactly
      this scoped set. Repository-wide `ruff check` is red with pre-existing
      errors (R-0364) and is NOT a gate.
  13. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count`, `high_blockers_open`.
  14. RED-PROOF, in a disposable worktree at HEAD under `.remedy-wt/`, never
      in the primary checkout. Two mutations, run and reverted one at a time:
      (a) in `_status_for_verb`, make `"resume"` map to `MISSION_STATUS_PAUSED`
      instead of active; (b) in `evaluate_mission`, pass `milestone_ids=()`
      unconditionally. For EACH, report WHICH test names failed and the exact
      failure line — report the colour you observe, never a count you predict.
      A mutation that leaves the suite green is a real finding about the tests
      and is reported as such, not repaired by strengthening the mutation.
      Remove the worktree and `git worktree prune` before the handback.
  15. `wc -l .agent/plan.md` → under 50.
  16. Insertions per commit via `git show --numstat`, per commit. None over 500.
  17. `test -e .agent/STOP` → ABSENT or PRESENT, before the round and at
      handback.
  18. `git diff --check 15a075c3..HEAD` → no output; every touched file
      newline-terminated.
  19. `git diff --name-only 15a075c3..HEAD` → exactly the twelve files of the
      change set, and nothing else.
  20. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    completion report + rewrite `.agent/handoff.md`, item-status
             table covering C0a C0b C1 C2 C3 C4 C5 C6, and this Fortschritt
             line verbatim:
             `~85 % (T001 ✅ · T002 ✅ · T003 halb: CLI + resume gebaut, Report offen) — Schätzung`
             ≤60 lines, or a "Deviations, declared" line naming the real count
             and the mandated content that caused it (DECISION D15). Never
             drop a section. The Next section names, in this order: (1) Phase
             1 rule 1 of docs/agents/self_drive_protocol.md — re-read
             `.agent/STOP` from disk BEFORE rule 2's Open PR Gate; (2) rule 2,
             noting there is NO open PR for this branch and one is created at
             closure, not before; (3) that R15 builds the report surface under
             DECISION F077 D12 and owes R14's own `Gate: R14 — ` paragraph as
             its FIRST commit; (4) that R16 is the integration gate then
             closure; (5) the open-finding count and names you measured at
             gate 4 and the next free id.

── C2 — the read-only entry point ────────────────────────────────

Inventory Q2 established the gap: `evaluate_ledger` is the only side-effect-free
symbol and it takes `entries`, so no mission-id-shaped read-only call exists.
`watchdog_pass` already composes exactly the reads that are missing, and then
writes. Extract that composition; do not copy it.

Add `evaluate_mission` to `packages/orchestration/watchdog.py`, placed directly
ABOVE `watchdog_pass` so a reader lands on the read-only twin first:

    def evaluate_mission(
        project_id: str,
        mission_id: str,
        *,
        root: Any = None,
    ) -> list[Trip]:

Its body is `watchdog_pass`'s current body MINUS the final `return
act_on_trips(...)`: the two inner imports, `read_ledger`, `load_mission`,
`evaluate_ledger` with `milestone_ids=orchestrator_loop.milestone_ids(mission)`
and `thresholds=watchdog_thresholds_from_config()`, returning the trip list.

`watchdog_pass` then becomes those two statements and nothing else:

    trips = evaluate_mission(project_id, mission_id, root=root)
    return act_on_trips(project_id, mission_id, trips, root=root,
                        iteration=iteration, now=now)

Its inner imports move WITH the code that needed them, so `watchdog_pass` is
left with none. Its docstring paragraph beginning "Every import lives INSIDE
this body" is therefore no longer true of it: move that paragraph to
`evaluate_mission`, where it is true, and give `watchdog_pass` one sentence
saying it is `evaluate_mission` plus the action. The `#:` comment above
`watchdog_pass` says "read the ledger, resolve the thresholds, evaluate every
tripwire, act on what tripped" — keep it accurate for the new shape.

`evaluate_mission` gets a one-line WHY comment directly above the definition,
per AGENTS.md Code Discoverability: it exists so an AUDIT can ask what the
watchdog sees without the watchdog acting on it.

Tests in `tests/orchestration/test_watchdog.py`, reusing that file's existing
fixtures and ledger builders rather than inventing new ones:
  - a mission whose ledger trips nothing returns `[]`;
  - a no_progress fixture returns exactly one `Trip` whose `kind` is
    `TRIP_NO_PROGRESS` and whose `numbers` carry `repeats`, `threshold` and
    `milestone_id`;
  - the INDEPENDENCE test, and it is the important one: over a tripping
    fixture, `evaluate_mission` leaves the mission's status unchanged, appends
    NO ledger entry (`len(read_ledger(...))` equal before and after) and opens
    NO decision — asserted on state read back from disk, not on a mock;
  - calling `evaluate_mission` twice returns equal trip lists (it is a read).

── C3 — `remedy mission watchdog <id>` ───────────────────────────

Inventory Q1's checklist, verbatim, three edits in two files:

1. `apps/cli/command_catalog.py` — one `CommandEntry` placed directly after the
   `mission.ledger` entry, so help lists it beside the other read-only mission
   verb: `command_id="mission.watchdog"`, `group_id="mission"`,
   `subcommand="watchdog"`, `action_class="read_only"`, `supports_json=True`,
   args `ArgDef("mission_id", "Mission id (or a unique prefix)")`,
   `_PROJECT_SCOPE_OPT`, `_JSON_OPT` — the two shared constants are REUSED,
   never re-declared — and `related=("mission.ledger", "mission.resume")`.
   The description says it evaluates the tripwires and reports, read-only,
   pausing nothing and raising no decision.
2. `apps/cli/commands/mission_cmd.py` — `_cmd_mission_watchdog(mission_id, *,
   project=None, json_output=False)`, modelled on `_cmd_mission_ledger`:
   `_resolve_project_id`, `_load_mission_or_exit`, then `evaluate_mission`
   imported INSIDE the body as that file's other handlers import theirs.
   JSON: `{"version": 1, "mission_id": ..., "trips": [t.to_json() ...]}`
   through `_json.dumps(..., sort_keys=True)`. Text: the mission id, its
   status, how many tripwires fired, and then per trip its `kind`, its
   `since_iteration` and every `numbers` key in `sorted` order — the evidence
   triple the feature file requires, on one screen.
3. `apps/cli/commands/mission_cmd.py` — the `COMMAND_HANDLERS` entry keyed
   `"mission.watchdog"`, in the lambda shape every neighbour uses:
   `args.mission_id`, `project=getattr(args, "project", None)`,
   `json_output=getattr(args, "json", False)`.

Tests in `tests/cli/test_mission_cmd.py`, following that file's own style —
a catalog class and a behaviour class, `_run` and `_start` reused:
  - catalog: `action_class == "read_only"`, `supports_json is True`, the id in
    `collect_all_handlers()`, `may_execute_commands is False`,
    `may_mutate_repo is False`;
  - an unrun mission reports zero tripwires and exits 0;
  - `--json` carries `version` 1, the resolved `mission_id` and a `trips` list;
  - the read-only acceptance: running the command over a mission leaves its
    status and its ledger length exactly as they were;
  - an unknown mission exits 1, says "no mission", prints no `Traceback`.

── C4 — `remedy mission resume <id>` ─────────────────────────────

DECISION F077 D4 scopes this to the status and nothing else: `resume` sets
`active`, and the dedup is D3's business. Inventory Q3 found THREE independent
encodings of the verb list; all three are edited here or the verb is either
unreachable or a `KeyError`:

1. `_status_for_verb` — add `"resume": MISSION_STATUS_ACTIVE` and add that
   constant to the function's inner import list.
2. `COMMAND_HANDLERS` — add `"mission.resume"` as a lambda into
   `_cmd_mission_set_status(args.mission_id, "resume", ...)`, exactly the shape
   the `pause` neighbour uses. No new handler function: D4's HOW TO REVERSE
   says `_cmd_mission_set_status` is reused.
3. `apps/cli/command_catalog.py` — one `CommandEntry` directly after
   `mission.pause`: `command_id="mission.resume"`, `subcommand="resume"`,
   `action_class="write_metadata"`, `supports_json=True`, the same three args
   as `mission.pause`, `related=("mission.pause", "mission.watchdog")`. The
   description says the pause is lifted and the trip is not.

Then apply the authored DOCSTRING pair below to `mission_cmd.py`'s MODULE
docstring. Its current sentence claims these verbs are "the only way a
mission's status ever moves", which F077's watchdog already made false.

Tests in `tests/cli/test_mission_cmd.py`:
  - catalog: `write_metadata`, `supports_json is True`, in
    `collect_all_handlers()`, `may_execute_commands is False`,
    `may_mutate_repo is False`;
  - `pause` then `resume` leaves the status `active`, read back through
    `mission show --json`;
  - the `--json` body of `resume` matches the shape `show` reports;
  - an unknown mission exits 1 and says so without a `Traceback`.

Do NOT extend `TestStatusTransitions._VERBS`. That tuple drives parametrized
tests asserting each verb's own status; `resume` gets its own tests so a future
reader can delete them with the verb.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

GATE-R13 is ONE physical line, appended to the END of `.agent/live_review.md`,
separated from the text above it by one blank line, matching the file's shape.

<<<BEGIN GATE-R13>>>
Gate: R13 — PASS. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. This gate is written by a NEW session, which re-ran all sixteen of R13's ordered gates against the disk itself rather than reading them out of the handback, and every one reproduces: the tree is clean and `git worktree list` is one line; `cmp .agent/authored/f077-r13.md .agent/last_block.md` is byte-identical at sha256 `ee9bb56ba6a0b41b7e6550d8a973705b55003de2115da2414bcd04b2a18fca4d`, 237 lines; `^Gate: R12 — ` 1, `^- R-0392 — ` 1 and `^Landed: ` 1; the open set recomputed mechanically is 27 registered paragraphs minus 4 `Done:` lines = 23 open with no duplicate id and next free `R-0393`; `^## Q[1-8] ` is 8; `git diff --name-only a9ebc920..HEAD -- packages apps tests docs` is EMPTY, which is the gate that makes the round read-only; `test_orchestrator_loop.py` 196 passed; `test_watchdog.py` plus `test_mission_e2e.py` in one invocation 52 passed; the canary 42 passed; the contract readers 216 passed, 16648 deselected; `integrity check --json` passed=true fail_count=0 check_count=5 with `high_blockers_open` pass; `wc -l .agent/plan.md` 44; per-commit insertions 237, 200, 4, 292, 263 and 37, none over 500, plus three later commits of 72, 7 and 8 that rewrite `.agent/handoff.md` alone and take AGENTS.md's single-state-file exemption; `git diff --check` silent; and the branch is pushed with its remote at the same SHA. The handback's own declared line count of 96 was measured and is 96, so the DECISION D15 stated-cause line is honest. The round's deliverable was audited as evidence rather than accepted as prose, because R14 is ordered against it: the reviewer independently re-derived the inventory's load-bearing claims from the source and every one held — `_status_for_verb` maps exactly `achieve`, `abandon` and `pause`; the three transition lambdas each pass their verb as a separate string literal, so the verb list really does have three independent machine-readable encodings; `tests/cli/test_worker_facade_cmd.py::TestHandlerRegistry::test_all_handlers_present` really is a 12-key literal set including `mission.report`, and `grep COMMAND_HANDLERS tests/cli/test_mission_cmd.py` and `grep -rn '_status_for_verb' tests/` both return nothing, so Q6's "register the new verbs in `mission_cmd.py`" is correct and load-bearing; `watchdog_pass`'s body is exactly the three reads plus `act_on_trips`, so Q2's extraction is available without touching the evaluators; `mission.report`'s handler really is `_cmd_mission_report` in `worker_facade_cmd.py` and its catalog entry really declares `ArgDef("run_id", ...)`, so Q5's correction stands; and `mission.watchdog` and `mission.resume` are free as ids and as `(group_id, subcommand)` pairs against a 334-entry catalog. One test the inventory did not name was checked because its name suggested an exact-set guard — `test_nothing_moves_a_status_without_one_of_these_commands` — and it is behavioural, asserting that linking a job and continuing a chain leave the status alone, so it does not constrain a new verb; Q6's claim that no test pins the group's size survives it. What this gate does NOT say: no production code changed this round and none was executed differently, so nothing here is evidence about the watchdog's runtime behaviour beyond what R10, R11 and R12 established, and the three premises the inventory corrected are corrections to the R13 BLOCK's text, not repairs to any shipped file.
<<<END GATE-R13>>>

DECISION-D12 is appended to the END of `.agent/decisions.md`, separated by one
blank line, matching that file's `## DECISION` section shape.

<<<BEGIN DECISION-D12>>>
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
<<<END DECISION-D12>>>

DOCSTRING is a REWRITE pair over `apps/cli/commands/mission_cmd.py`'s MODULE
docstring — FROM and TO are disjoint, so the proof is FROM 0x and TO 1x in the
file after the edit. FROM is two physical lines, TO is four.

<<<BEGIN DOCSTRING-FROM>>>
``achieve``/``abandon``/``pause`` are the explicit status transitions — the
only way a mission's status ever moves.
<<<END DOCSTRING-FROM>>>

<<<BEGIN DOCSTRING-TO>>>
``achieve``/``abandon``/``pause``/``resume`` are the explicit status
transitions, and ``watchdog`` reports F077's tripwires without writing
anything.  They are not the only writers: the orchestrator loop's terminal
moves and the watchdog's own pause move the status with no human in the loop.
<<<END DOCSTRING-TO>>>

── STATE MIRROR — C5 ─────────────────────────────────────────────

`.agent/plan.md` (UNDER 50 lines; it is 44 now, and it keeps `## Goal`,
`## Current Step`, `## Next Steps` and `## Risks`): Current Step becomes R14,
naming that R13's verdict landed in C1, that DECISION F077 D12 is recorded,
and what C2, C3 and C4 actually built. Next Steps become R15 (the `mission
show` lead under D12, plus R14's own gate paragraph as its first commit) and
R16 (integration gate, then closure). The open-findings sentence carries the
count, the names and the next free id YOU measured at gate 4. Keep both
existing risks and add one line: `mission resume` buys exactly one iteration
before the same evidence re-trips (inventory Q8), which D12 does not address.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): add
`packages/orchestration/watchdog.py`'s `evaluate_mission`, the two new mission
verbs and the two touched product files to the In-scope list; update the
open-findings count and next free id; and extend the `## Steps` line with R14
and the renumbered R15 and R16. Change nothing else — in particular the
block-ceiling constraint line is already correct.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather than
routing around it. If a mutation in gate 14 leaves the suite green, that is a
finding about the tests and it goes in the handback as one — do not repair it
by editing the mutation until it bites.
──────────────────────────────────────────────────────────────────
