── STEP T003-build/2 of 2 — F077 Autonomy watchdog · R15 ─────────

Goal:        Record R14's verdict and the one finding it earned, then finish
             T003: a paused-by-watchdog mission's report LEADS with the trip,
             under DECISION F077 D12. After this round T003 is complete and
             R16 is the integration gate.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r15.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   FINDINGS FIRST, own commit: append the authored GATE-R14 slice, then the
       authored FINDING-R393 slice, to the END of `.agent/live_review.md`, in
       that order
  C2   `packages/orchestration/watchdog.py`: `latest_trips_from_ledger`, a pure
       reader over ledger entries; tests in `tests/orchestration/test_watchdog.py`
  C3   `apps/cli/commands/mission_cmd.py`: the trip lead in `_cmd_mission_show`,
       text and JSON; tests in `tests/cli/test_mission_cmd.py`
  C4   mirror the round into `.agent/plan.md` and `.agent/context.md`
  C5   handback: rewrite `.agent/handoff.md`

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r15.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`,
             `.agent/handoff.md`, `packages/orchestration/watchdog.py`,
             `apps/cli/commands/mission_cmd.py`,
             `tests/orchestration/test_watchdog.py`,
             `tests/cli/test_mission_cmd.py`.
             Ten files. `apps/cli/command_catalog.py` is NOT in this set: this
             round adds no command. `packages/orchestration/mission_state.py`
             is NOT in it either — see C3 for why the lead does not go into
             `render_mission_chain`.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. 500-INSERTION cap per commit.
  - `.agent/plan.md` stays UNDER 50 lines. It is 43 now.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    The GATE-R14 and FINDING-R393 slices are reviewer text, applied verbatim
    from the COMMITTED `.agent/authored/f077-r15.md`.
  - The residual `Landed: R-0384` stays. It is open finding R-0380's evidence.
  - `mission show` STAYS READ-ONLY. The lead is rendered from what the ledger
    already RECORDS; it never calls `evaluate_mission`, `watchdog_pass` or
    `act_on_trips`, and it writes nothing. Re-evaluating on a read would make
    `show` disagree with the trip that actually caused the pause, and
    `remedy mission watchdog` is the re-evaluation surface.
  - Do NOT change `evaluate_mission`, `evaluate_ledger`, the three evaluators,
    `act_on_trips`, `watchdog_pass`, `_status_for_verb`, the catalog, or any
    threshold. C2 ADDS a function; it changes none.
  - Do NOT touch `apps/cli/commands/worker_facade_cmd.py` — the two exact-set
    guards of inventory Q6 — and do not go near `mission report`. DECISION
    F077 D12 settled that surface; reopening it is outside this round.
  - `.agent/STOP`: re-check from disk before you start and again at handback.
  - Destructive checks run ONLY in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout.

Done when: every gate below has been RUN by you and its REAL value recorded.
"Green" as a word is a finding. The round's base commit is `9ef5c62b`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r15.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R14 — ' .agent/live_review.md` → 1.
      `grep -c '^- R-0393 — ' .agent/live_review.md` → 1.
      `grep -c '^Landed: ' .agent/live_review.md` → 1, NOT 0.
  4.  Recompute the open-finding set MECHANICALLY — every `^- R-\d+ — `
      paragraph minus every `^Done: R-\d+ — ` line — and report the count and
      the names. The reviewer measured 23 open at `9ef5c62b`, and C1 registers
      R-0393, so 24 is the expected reading. Report what you measure,
      unadjusted, and name the next free id.
  5.  `python3 -m pytest tests/orchestration/test_watchdog.py tests/orchestration/test_mission_e2e.py -q`
      → report the number. The reviewer measured `56 passed` at `9ef5c62b`;
      C2 adds tests, so it GROWS.
  6.  `python3 -m pytest tests/cli/test_mission_cmd.py -q` → report the number.
      The reviewer measured `92 passed` at `9ef5c62b`; C3 adds tests.
  7.  `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_worker_facade_cmd.py -q`
      → report the number. The reviewer measured `576 passed` at `9ef5c62b`.
      This round adds NO test to these three files and no catalog entry, so
      576 is the expected reading and anything else is leakage.
  8.  `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      → report the number. The reviewer measured `196 passed` at `9ef5c62b`.
  9.  Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `9ef5c62b`.
  10. `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → report BOTH numbers. The reviewer measured `216 passed, 16661
      deselected` at `9ef5c62b`. PASSED is expected to stay 216; DESELECTED is
      expected to grow by exactly the tests this round adds. Run this AFTER
      drafting both state files and BEFORE committing C4, and grep every test
      that READS `.agent/plan.md` or `.agent/context.md` first, validating the
      drafts against all of it (R-0162).
  11. `python3 -m ruff check packages/orchestration/watchdog.py apps/cli/commands/mission_cmd.py tests/orchestration/test_watchdog.py tests/cli/test_mission_cmd.py`
      → the reviewer measured `All checks passed!` at `9ef5c62b` for exactly
      this scoped set. Repository-wide `ruff check` is red with pre-existing
      errors (R-0364) and is NOT a gate.
  12. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count`, `high_blockers_open`.
      `handler_import` read `handlers=336` at `9ef5c62b`; this round adds no
      handler, so it should still read 336.
  13. RED-PROOF, in a disposable worktree at HEAD under `.remedy-wt/`, never in
      the primary checkout. Report the SAME `-k` selection for the green run
      and for each mutated run — a before/after pair measured over different
      selections is not a pair, which is exactly finding R-0393. Two mutations,
      run and reverted one at a time:
      (a) in `latest_trips_from_ledger`, return the FIRST entry per kind rather
      than the last;
      (b) in `_cmd_mission_show`, drop the paused condition so the lead renders
      for every mission.
      For EACH, report WHICH test names failed and the exact failure line —
      the colour you observe, never a count you predict. A mutation that leaves
      the suite green is a real finding about the tests and is reported as one.
      Remove the worktree and `git worktree prune` before the handback.
  14. `wc -l .agent/plan.md` → under 50.
  15. Insertions per commit via `git show --numstat`, per commit. None over 500.
  16. `test -e .agent/STOP` → ABSENT or PRESENT, before the round and at
      handback.
  17. `git diff --check 9ef5c62b..HEAD` → no output; every touched file
      newline-terminated.
  18. `git diff --name-only 9ef5c62b..HEAD` → exactly the ten files of the
      change set, and nothing else.
  19. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    completion report + rewrite `.agent/handoff.md`, item-status
             table covering C0a C0b C1 C2 C3 C4 C5, and this Fortschritt line
             verbatim:
             `~92 % (T001 ✅ · T002 ✅ · T003 ✅ CLI, resume und Report) — Schätzung`
             ≤60 lines, or a "Deviations, declared" line naming the real count
             and the mandated content that caused it (DECISION D15). Never
             drop a section. The Next section names, in this order: (1) Phase
             1 rule 1 of docs/agents/self_drive_protocol.md — re-read
             `.agent/STOP` from disk BEFORE rule 2's Open PR Gate; (2) rule 2,
             noting there is NO open PR for this branch and one is created at
             closure, not before; (3) that R16 is the INTEGRATION GATE per
             docs/agents/integration_gate.md and owes R15's own `Gate: R15 — `
             paragraph as its FIRST commit; (4) that closure follows R16 per
             docs/roadmap/STATUS_closure_protocol.md and still owes an ist-doc
             for the watchdog registered in `docs/README.md`, which no round
             has written yet; (5) the open-finding count and names you measured
             at gate 4 and the next free id.

── C2 — `latest_trips_from_ledger`, a pure reader ────────────────

The lead must show what actually caused THIS pause, and the ledger already
records it: `act_on_trips` writes one entry per trip whose `move` is
`{"kind": MOVE_WATCHDOG_TRIPPED, "payload": trip.to_json()}` (DECISION F077 D5),
and `Trip.to_json` emits exactly `kind`, `what`, `since_iteration`, `numbers`.
So the reader reconstructs, it does not re-evaluate.

Add to `packages/orchestration/watchdog.py`, placed with the other pure
accessors ABOVE `evaluate_no_progress` — it is a reader, not an evaluator:

    def latest_trips_from_ledger(
        entries: Sequence[dict[str, Any]],
    ) -> list[Trip]:

Behaviour, and each clause is a test below:
  - it walks `entries` in LEDGER ORDER and keeps, per trip `kind`, the trip
    carried by the LAST `watchdog_tripped` entry of that kind. Ledger order is
    file order (DECISION F077 D11: `iteration` is an attribution, never a key),
    so "latest" means last in the sequence and nothing is sorted by number;
  - it returns them in the module's FIXED kind order —
    `TRIP_NO_PROGRESS`, `TRIP_BURN_ANOMALY`, `TRIP_GOAL_DRIFT` — the same
    order `evaluate_ledger` reports, so two readings of one mission read the
    same way;
  - it TOLERATES a torn entry and never raises: an entry whose `move` is not a
    dict, whose kind is not `MOVE_WATCHDOG_TRIPPED`, whose `payload` is not a
    dict, or whose payload is missing any of the four `Trip` fields, is
    SKIPPED. That matches what every evaluator in this module already does.
    Reuse `_sub_dict` and `_move_kind` rather than re-reading the dicts by
    hand.
  - it writes nothing and imports nothing — it is pure over its argument, like
    `evaluate_ledger`.

A one-line WHY comment sits directly above the definition, per AGENTS.md Code
Discoverability: it exists so a REPORT can name the trip that paused a mission
without re-running the watchdog.

Tests in `tests/orchestration/test_watchdog.py`, reusing the file's existing
`_entry`-style builders where they fit:
  - an empty ledger returns `[]`, and a ledger with no watchdog entry returns
    `[]`;
  - one trip entry returns one `Trip` whose four fields survive the round trip
    through the ledger payload;
  - TWO entries of the SAME kind return ONE trip, and it is the LATER one —
    assert on a field that differs between them, not on the length alone;
  - three kinds in scrambled ledger order come back in the fixed kind order;
  - a torn entry — payload missing `numbers` — is skipped, the healthy entry
    beside it still comes back, and nothing raises.

── C3 — the lead, in `_cmd_mission_show` ─────────────────────────

DECISION F077 D12 put the lead here. It goes in the CLI handler and NOT in
`mission_state.render_mission_chain`, for a reason worth writing down in the
code: `render_mission_chain` takes a `Mission` and nothing else, and the trips
live in the LEDGER, which `orchestrator_loop` owns — and `orchestrator_loop`
imports `mission_state`. Reaching the ledger from the renderer would invert
that dependency and create the very cycle `watchdog.py` keeps its imports
inside function bodies to avoid. `render_mission_chain` stays pure.

In `_cmd_mission_show`, after `_load_mission_or_exit`:
  - resolve the trips ONCE: an empty list unless
    `mission.status == MISSION_STATUS_PAUSED`, in which case `read_ledger`
    then `latest_trips_from_ledger`. Both imports go INSIDE the body, as this
    file's other handlers do;
  - JSON: the existing object gains ONE top-level key beside `version` and
    `mission` — `"watchdog_trips": [trip.to_json() for trip in trips]` —
    always present, `[]` when there is no lead. The `mission` sub-object is
    NOT touched: `mission resume`'s `test_the_json_shape_matches_show`
    compares it against this command's, and that comparison must keep holding;
  - text: when `trips` is non-empty, the lead prints BEFORE the first line
    `render_mission_chain` returns; when it is empty, the output is
    BYTE-IDENTICAL to today's. The lead names, per trip, the `kind`, the
    `since_iteration`, the `what` sentence and every `numbers` key in `sorted`
    order, then one pointer line naming `remedy mission watchdog <id>` as
    where the full evidence lives, then a blank line before the chain.

Wording is yours, but the first line must make the cause unmistakable at a
glance — a human reading `mission show` on a stalled mission should not have
to know the word "watchdog" to understand that something stopped it and that
it is waiting for them.

Tests in `tests/cli/test_mission_cmd.py`, in that file's own style:
  - a paused mission with a `watchdog_tripped` entry LEADS with the trip:
    assert the lead's text appears, and assert its index in stdout is BEFORE
    the index of the `Mission <id>` line — "leads with" is an ORDER claim and
    an unordered assertion does not test it;
  - the same mission's `--json` carries `watchdog_trips` with that trip's
    `kind` and its `numbers`, and `body["mission"]` still matches what it was;
  - an ACTIVE mission whose ledger contains a `watchdog_tripped` entry gets NO
    lead — the pause is the condition, not the history;
  - a mission paused BY HAND, with no watchdog entry anywhere, gets no lead
    and its `watchdog_trips` is `[]`;
  - a fresh mission's `--json` carries `watchdog_trips == []`.

Build the paused-with-trip fixture by writing a real ledger entry through
`append_ledger_entry` and then `remedy mission pause`, not by hand-editing a
mission record: the test is worth more if the entry it reads is the shape the
product writes.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

Both slices are ONE physical line each, appended to the END of
`.agent/live_review.md`, GATE-R14 first, each separated from its neighbour by
one blank line, matching the file's existing shape.

<<<BEGIN GATE-R14>>>
Gate: R14 — PASS. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. Every one of the twenty ordered gates was re-run by the reviewer against the disk and every value reproduces: tree clean and `git worktree list` one line; `^Gate: R13 — ` 1, `^Landed: ` 1, `^## DECISION F077 D12 ` 1; the open set recomputed from the record is 27 registered minus 4 `Done:` = 23 with no duplicate id and next free `R-0393`; `test_watchdog.py` plus `test_mission_e2e.py` 56 passed, `test_mission_cmd.py` 92 passed, the catalog plus grouped-CLI plus worker-facade trio 576 passed and unmoved, `test_orchestrator_loop.py` 196 passed and unmoved, the canary 42 passed, the contract readers 216 passed with 16661 deselected — the deselected delta of exactly +13 equals the 13 tests this round adds, 4 in `test_watchdog.py` and 9 in `test_mission_cmd.py`; scoped `ruff check` over the five owned files `All checks passed!`; `integrity check --json` passed=true fail_count=0 check_count=5 with `handler_import` now reading `handlers=336`, which is 334 plus the two new handlers; `wc -l .agent/plan.md` 43; per-commit insertions 364, 316, 2, 125, 122, 83 and 64 with the handback's own 102, none over 500; `git diff --check` silent; the range touches exactly the twelve ordered files; and the branch is pushed with its remote at the same SHA. Transport is proven end to end rather than internally: the committed `.agent/authored/f077-r14.md`, `.agent/last_block.md` and the reviewer's own pre-emission original under `.remedy-wt/` are all byte-identical at sha256 `32e1a40869ac0cd89c68bf411ac29c37b4e8052df8744c5fcebdf6867955d4d4`, 364 lines, so the block the worker executed is provably the block the reviewer authored. Every authored slice was re-extracted by the reviewer from the COMMITTED authored file and counted against its target: GATE-R13 appears exactly 1x in `.agent/live_review.md`, DECISION-D12 exactly 1x in `.agent/decisions.md`, and the DOCSTRING pair is a REWRITE whose FROM is now 0x and whose TO is 1x in `apps/cli/commands/mission_cmd.py`, the shape the block declared. The diff was read bottom-up and matches the orders exactly: `evaluate_mission` is the read-only twin placed above `watchdog_pass`, whose body is now that call plus `act_on_trips` and whose inner imports moved with the code that needed them; `mission.watchdog` is `read_only` and `mission.resume` is `write_metadata`, both registered in `mission_cmd.py` and not in the guarded facade. The reviewer ran its own red-proof of its own choosing, in a disposable worktree it created, mutated and removed: with `evaluate_mission` made to call `set_mission_status`, `test_evaluate_mission_writes_nothing_at_all` fails on `AssertionError: assert 'paused' == 'active'`, so the feature file's independence criterion is genuinely pinned by a test rather than asserted in prose; and the worker's mutation (a) was reproduced independently as `1 failed, 8 passed` on `test_pause_then_resume_leaves_the_mission_active` at `assert 'Status: active' in '…Status: paused\n'`. The worker's five declared deviations were each checked and each is correct behaviour: the C0a/C0b split was forced by a 680-insertion shared stage against a 500 cap; the deselected drift and the `handlers=336` reading are real measured numbers reported unadjusted; the three docstring and comment repairs each fix a sentence the ordered change itself made false, which is the opposite of scope drift; and the 134-line handoff carries its DECISION D15 cause with no section dropped. What this gate does NOT say: the full suite did not run, so nothing here is a claim about the rest of the repository — that is R16's integration gate — and no round has yet written an ist-doc for the watchdog under `docs/`, which closure still owes.
<<<END GATE-R14>>>

<<<BEGIN FINDING-R393>>>
- R-0393 — Low — R14's red-proof transcript reports a green baseline and a mutated run measured over DIFFERENT `-k` selections, so the pair it presents is not a like-for-like comparison. The handback's gate 14 says the worktree "was proven green first (`-k "Resume or Watchdog"` → `9 passed, 83 deselected`)" and then reports mutation (a) as `1 failed, 3 passed, 88 deselected`. Those totals cannot be paired: `--collect-only` at HEAD gives `9/92` for `-k "Resume or Watchdog"` and `4/92` for `-k "Resume"`, so the mutated run selected four tests where the baseline selected nine. Both numbers are real and neither is fabricated — the reviewer reproduced the mutation independently at the wider selection and observed `1 failed, 8 passed`, the same failing test on the same assertion — which is why this is Low and not a block condition. It is registered because a red-proof is not a number, it is a PAIR: the whole evidentiary weight of "this test catches that break" rests on the two runs differing in exactly one variable, and a narrowed selection between them is a second variable that a later reader cannot rule out without re-running the proof themselves. The residual risk was real rather than theoretical: at the narrower selection the transcript's own honest note — that `test_the_json_shape_matches_show` survives the mutation by construction — is indistinguishable from the five tests that simply were not run. From here, a red-proof states ONE selection string and uses it for the green run and every mutated run, or it declares the change of scope in the same sentence as the numbers.
<<<END FINDING-R393>>>

── STATE MIRROR — C4 ─────────────────────────────────────────────

`.agent/plan.md` (UNDER 50 lines; it is 43 now, and it keeps `## Goal`,
`## Current Step`, `## Next Steps` and `## Risks`): Current Step becomes R15,
naming that R14's verdict and R-0393 landed in C1 and what C2 and C3 built.
Next Steps become R16 (the integration gate per docs/agents/integration_gate.md,
carrying R15's own gate paragraph as its first commit) and then closure per
docs/roadmap/STATUS_closure_protocol.md — and the closure line names the ist-doc
the watchdog still lacks under `docs/`, registered in `docs/README.md`. The
open-findings sentence carries the count, the names and the next free id YOU
measured at gate 4. Keep every existing risk.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): add
`latest_trips_from_ledger` and the `_cmd_mission_show` lead to the In-scope
list; record that `render_mission_chain` stays out of scope and why; update the
open-findings count and next free id; and extend the `## Steps` line with R15
and R16. Change nothing else.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather than
routing around it. Gate 13's selection string is stated once and used for every
run in that gate — that requirement IS finding R-0393 and this round is the
first that has to satisfy it.
──────────────────────────────────────────────────────────────────
