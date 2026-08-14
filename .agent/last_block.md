── STEP T002-repair/1 — F077 Autonomy watchdog · R11 ─────────────

Goal:        Make the tripped ledger's iteration numbers unique again, so the
             invariant two independent guards pin — one entry per iteration,
             numbered once — survives the wiring, and the branch goes green.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r11.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   FINDINGS FIRST, own commit: append the four authored finding slices and
       then the authored GATE-R10 slice to `.agent/live_review.md`, in that
       order
  C2   append the authored DECISION-D10 slice to `.agent/decisions.md`
  C3   the repair: the call site, the two stale prose sites, and the tests
  C4   mirror the round into `.agent/plan.md` and `.agent/context.md`
  C5   handback: rewrite `.agent/handoff.md`

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r11.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`,
             `packages/orchestration/watchdog.py`,
             `packages/orchestration/orchestrator_loop.py`,
             `tests/orchestration/test_orchestrator_loop.py`,
             `tests/orchestration/test_watchdog.py`,
             `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`.
             Eleven files. `mission_state.py`, `mission_cmd.py` and
             `test_mission_e2e.py` are correct as they stand and are NOT touched.

C3, in detail:
  (a) `packages/orchestration/orchestrator_loop.py`, in `run_mission`: the
      `watchdog_pass` call STOPS passing the loop's own iteration number. Apply
      pair LOOP-CALL.
  (b) `packages/orchestration/watchdog.py`: `watchdog_pass`'s docstring
      currently argues FOR the behaviour this round removes. Apply pair
      WD-DOCSTRING. Do not change `watchdog_pass`'s signature — `iteration`
      stays a parameter, because the manual T003 CLI path will still want to
      pass one; only the LOOP stops passing it.
  (c) `tests/orchestration/test_orchestrator_loop.py`, in
      `TestTheLedgerCoversEveryIteration::test_one_entry_per_iteration_numbered_from_one`:
      this test scripts THREE identical `dispatch_job` moves on milestone M001
      under `max_iterations=3`, which is exactly the `no_progress` pattern at
      the default threshold of 3, so its ledger legitimately gains a fourth
      entry — the trip. Repair the test to the invariant it actually defends,
      and repair nothing else in that file:
        - the iteration numbers read `[1, 2, 3, 4]`;
        - those numbers are UNIQUE — assert it directly, not as a side effect
          of the list equality, because uniqueness is the property that broke;
        - the move kinds read three `dispatch_job` followed by one
          `watchdog_tripped`.
      Update the test's docstring/comment so a later reader learns WHY a
      three-iteration run leaves four entries, instead of rediscovering it.
  (d) `tests/orchestration/test_watchdog.py`: add ONE test that pins the new
      rule by intent rather than by accident — after a `no_progress` trip in a
      scripted `run_mission`, no two ledger entries share an `iteration` value,
      and the `watchdog_tripped` entry's number is strictly GREATER than every
      loop entry's. Keep the three tests you added in R10; they are correct.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. 500-INSERTION cap per commit.
  - `.agent/plan.md` must end at FEWER THAN 50 lines — finding R-0390 is that
    it is currently exactly 50, and AGENTS.md says "<50". Cut prose, never a
    mandated section.
  - You never write a `Done:` paragraph in `.agent/live_review.md`. Only the
    reviewer's authored text sets `Done:`. If you fix something not yet
    resolved by the reviewer, write `Landed: R-XXXX — <one line>` and nothing
    else. The four findings below arrive as OPEN; R-0388 and R-0390 are the two
    this round actually repairs, so mark those two `Landed:` after their fixes
    commit. R-0387 and R-0389 are against the reviewer and are NOT yours to
    close — leave them open and do not write a `Landed:` line for either.
  - Do NOT change any threshold default, any config key, `act_on_trips`, or
    `evaluate_ledger`. Do NOT add a seam parameter to `run_mission`.
  - The F077 Do-not-touch list holds: no repair logic, no class-expectation
    anomaly detection, no loop policy.
  - Repository-wide `ruff check` is RED on main and is NOT a gate (R-0364);
    ruff is gated scoped to the files this round changes.
  - `.agent/STOP`: re-check from disk before you start and again at handback.
  - Any destructive check runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout.

Why the number must move, so you can check the reasoning rather than trust it:
after a trip the mission status is `paused`, and `run_mission`'s next iteration
hits its top-of-loop status check and returns `mission_not_active` WITHOUT
recording an entry. So the number `act_on_trips` resolves from
`next_iteration_index` — one past the highest recorded — can never collide with
an entry the loop goes on to write. Verify that claim against the code before
you apply C3(a); if you find a path where the loop DOES record after a trip,
stop and report it, because then this whole repair is wrong.

Done when: every gate below has been RUN by you and its REAL value recorded.
"Green" as a word is a finding. The round's base commit is `63ce2a6d`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r11.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R10 — FAIL' .agent/live_review.md` → 1.
      `grep -c '^## Steps' .agent/live_review.md` → 1.
      `grep -c '^## DECISION F077 D10 ' .agent/decisions.md` → 1.
      Each of `^- R-0387 — `, `^- R-0388 — `, `^- R-0389 — `, `^- R-0390 — `
      → 1.
  4.  Recompute the open-finding set MECHANICALLY from `.agent/live_review.md`
      — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — and
      report the count and the names. Report what you measure, unadjusted.
      Note that `Landed:` lines do NOT resolve a finding, so R-0388 and R-0390
      stay in the open set this round; that is correct, not an error to fix.
  5.  `python3 -c "import packages.orchestration.orchestrator_loop"` → exit 0.
      `python3 -c "import packages.orchestration.watchdog"` → exit 0.
  6.  THE GATE THIS ROUND EXISTS FOR:
      `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      → report the real number. It was `1 failed, 195 passed` at `63ce2a6d`.
      Run it at the base FIRST to confirm that starting point yourself, then at
      your HEAD, and report BOTH.
  7.  `python3 -m pytest tests/orchestration/test_watchdog.py -q` → report the
      number at base and at HEAD. Also `grep -c "def test_"` on that file.
  8.  `python3 -m pytest tests/orchestration/test_mission_e2e.py -q` → report
      the number. It was 24 passed at `63ce2a6d` and this round must not move
      it; if it does, name every failing test and STOP.
  9.  `ruff check` over ONLY the files this round changed → exact output.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
  11. `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → number. Before authoring either state edit, grep every test that reads
      that path and validate the draft against ALL of it (R-0162).
  12. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count`, `high_blockers_open`.
  13. `wc -l .agent/plan.md` → report it. Must be under 50.
  14. Insertions per commit via `git show --numstat`, reported per commit. None
      over 500.
  15. `test -e .agent/STOP` → ABSENT or PRESENT, before the round and again at
      handback.
  16. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.
  17. Trailing-whitespace scan over every touched file → none; all
      newline-terminated.

Handback:    completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md, with the item-status table
             covering C0a C0b C1 C2 C3 C4 C5 and this Fortschritt line verbatim:
             `~72 % (T001 ✅ · T002 Aktion ✅ · Verdrahtung rot, Reparatur R11 · T003 offen) — Schätzung`
             ≤60 lines, or a "Deviations, declared" line naming the real count
             and the mandated content that caused it (DECISION D15). Never drop
             a mandated section to meet the cap.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

Append the four finding lines in id order, then the gate line, each as ONE
physical line, each separated from its neighbour by one blank line, matching the
file's existing shape.

<<<BEGIN FINDING-R387>>>
- R-0387 — Medium — the reviewer ran pre-emission checklist item 7 ("source guards the block never names") too narrowly and the round ended red because of it. Item 7 says to grep the suite for tests that COUNT a string over a WHOLE file before ordering a change that adds one; the reviewer instead grepped for the literal pattern `count(` and read only `tests/orchestration/test_mission_e2e.py`, the file DECISION F077 D8 happened to name. The guard that actually broke — `TestTheLedgerCoversEveryIteration::test_one_entry_per_iteration_numbered_from_one` in `tests/orchestration/test_orchestrator_loop.py` — is a whole-ledger equality of exactly the class D8 warned about, it contains no `count(` at all, and it sits in a file the R10 block DID authorise the round to gate but not to repair. Two mistakes compounded: the search pattern was a proxy for the property rather than the property itself, and the search scope was taken from a DECISION's prediction instead of from the change. The worker was left holding a red suite it was explicitly forbidden to fix, which is the outcome item 7 exists to prevent — the finding text for R-0258 says in as many words that such a guard "makes a correct SECOND call site unsatisfiable, and the worker cannot repair it without leaving its change set". From here, a block that adds an entry to any append-only record greps EVERY test file that reads that record for whole-collection equalities, not only for `count(`, and the block's Change line authorises repairing what that grep finds.
<<<END FINDING-R387>>>

<<<BEGIN FINDING-R388>>>
- R-0388 — Medium — the R10 wiring gives the watchdog's ledger entry the number of the iteration that was being observed, so a tripped run's ledger reads `[1, 2, 3, 3]` and two entries claim the same iteration. "One entry per iteration, numbered once" is not an incidental property of one test: it is pinned independently by `test_one_entry_per_iteration_numbered_from_one` in `tests/orchestration/test_orchestrator_loop.py` and by `test_every_iteration_is_numbered_once_across_both_runs` in `tests/orchestration/test_mission_e2e.py`, whose name states the invariant outright, and `next_iteration_index` derives the loop's own numbering by reading one past the highest recorded value — a field three separate mechanisms treat as a sequence key. The behaviour is deliberate rather than accidental, which is why it is a design finding and not a typo: `watchdog_pass`'s own docstring argues for it, on the ground that re-deriving the number "would number the trip one past the entry that caused it". That is true and it is the correct outcome — the trip is a distinct event appended after the entry it judges, and the evidence it carries already names the iterations it is about through `since_iteration` and its `numbers` payload, so nothing is lost by numbering the entry itself in sequence. DECISION F077 D6's closing claim that "no collision is possible" holds only for the collision it was written about, an external append racing the loop's precomputed base; it does not hold for the collision the loop itself creates by passing its own number. Repaired in this round by DECISION F077 D10.
<<<END FINDING-R388>>>

<<<BEGIN FINDING-R389>>>
- R-0389 — Low — the R10 block was 293 lines against the 240-line ceiling `.agent/context.md` carries for this feature, and the reviewer emitted it without measuring. The ceiling exists so that the block-save commit stays inside the 500-insertion cap (R-0381), and at 293 that commit was still comfortably inside it, so nothing broke on disk and the round paid nothing for it — this is registered because an unmeasured ceiling is one round away from being an exceeded cap, and because pre-emission checklist item 1 orders the count to be taken mechanically on the final bytes, which was not done. The reviewer's own constraint list in the block repeated the 240 figure to the worker while the block containing it was 293 lines long.
<<<END FINDING-R389>>>

<<<BEGIN FINDING-R390>>>
- R-0390 — Low — `.agent/plan.md` is exactly 50 lines and AGENTS.md's plan.md rule says "keep it short (<50 lines)", which 50 does not satisfy; pre-emission checklist item 3 names the same bound as "under 50 lines". The R10 block delegated plan.md's content to the worker as a description rather than authoring it as a bounded replacement, so no line count was ever computed against the cap by either role — the reviewer did not author the text and the worker was given no number to meet. Repaired in this round by cutting prose, not by dropping a mandated section.
<<<END FINDING-R390>>>

<<<BEGIN GATE-R10>>>
Gate: R10 — FAIL. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. The FAIL is `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q` reading `1 failed, 195 passed` at `63ce2a6d` against `196 passed` at the base, re-run by the reviewer rather than read from the handback, with the real assertion error `assert [1, 2, 3, 3] == [1, 2, 3]`. `LAST_REVIEWED_SHA` does not advance. Everything else in the round is sound and the failure is not the worker's: the wiring itself was read line by line and implements the block as written — `watchdog_pass` reads the ledger, resolves thresholds from config and milestone ids from the persisted plan, keeps every heavy import inside its body, and returns `act_on_trips` on what tripped; the call site sits after the terminal return so a run that is already over is not watched, and the anchor's uniqueness was measured (2 occurrences of the `_record` line, 1 followed by `if outcome.terminal:`) rather than assumed. Both docstring pairs applied append-shaped as authored. The reviewer re-ran the round's suites at this HEAD: `tests/orchestration/test_watchdog.py` `28 passed` with `grep -c "def test_"` also 28, `tests/orchestration/test_mission_e2e.py` `24 passed`, and the canary `42 passed`, which is 94 in one invocation. `cmp .agent/authored/f077-r10.md .agent/last_block.md` exits 0 over 293 lines with the shared sha256 `da0b9f66dbdc642b17adba8c2ee26fb3e6442055850bdf194d910dfb9fc7e031`. The tree is clean and `git worktree list` is one line. Three things the round got RIGHT are worth recording because each was a place it could have gone wrong instead: DECISION F077 D9's probe came back green exactly as reasoned — the e2e scenario trips no tripwire, `no_progress` clearing its run on every `declare_milestone_done` with a longest surviving streak of two against a threshold of three, `burn_anomaly` inert below eight measured entries in a seven-iteration run with no measured usage, and `goal_drift` needing a milestone the plan never named — so D8's four-guard bill was a false forecast and that file was correctly left untouched; the worker refused to repair the red guard because the block's Change line forbade the file, which is the only correct move available to it and the opposite of the scope-widening that would have made the round ungatable; and it repaired `watchdog.py`'s "It has NO caller" module clause and the matching stale comment in `test_watchdog.py` in the same commit that falsified them, unprompted, which is the R-0384 lesson applied without being told. The red-proof the block ordered in a disposable worktree reported `2 failed, 26 passed` with the call site deleted; the reviewer did not re-run it, because the red guard in `test_orchestrator_loop.py` is a stronger and freely available proof of the same claim — a test the block never touched changed colour because of the call site, which is reachability demonstrated by the production path rather than by a mutation. Four findings are registered against this round, R-0387 through R-0390, and TWO of them are against the reviewer: R-0387, the narrow item-7 grep that let the round be planned into a red suite, and R-0389, a 293-line block emitted against a 240-line ceiling without measuring. What this gate does NOT say: the watchdog is now genuinely wired and a tripped mission genuinely pauses — that much the red guard itself proves — but the ledger it leaves behind has a duplicated iteration number, so no reader should treat this branch as shippable until R-0388 is repaired.
<<<END GATE-R10>>>

<<<BEGIN DECISION-D10>>>
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
<<<END DECISION-D10>>>

<<<BEGIN PAIR LOOP-CALL — REWRITE, file packages/orchestration/orchestrator_loop.py>>>
FROM:
            # ``watchdog`` imports this module back (DECISION F077 D6 for the
            # iteration number, which is this loop's own).
            from packages.orchestration.watchdog import watchdog_pass

            watchdog_pass(pid, mission_id, iteration=iteration, root=root,
                          now=now)
TO:
            # ``watchdog`` imports this module back. The loop deliberately does
            # NOT pass its own iteration number (DECISION F077 D10): a trip is
            # a separate event appended AFTER the entry it judges, so it takes
            # the next number from the record. Passing this iteration's number
            # would put two entries in the ledger claiming to be the same one.
            from packages.orchestration.watchdog import watchdog_pass

            watchdog_pass(pid, mission_id, root=root, now=now)
<<<END PAIR LOOP-CALL>>>

<<<BEGIN PAIR WD-DOCSTRING — REWRITE, file packages/orchestration/watchdog.py>>>
FROM:
    ``iteration`` is handed straight to :func:`act_on_trips` (DECISION F077 D6).
    A caller inside a running iteration knows the number a trip belongs to, and
    re-deriving it from the ledger would number the trip one past the entry that
    caused it.
TO:
    ``iteration`` is handed straight to :func:`act_on_trips` (DECISION F077 D6)
    and is for OUT-OF-BAND callers — the manual audit path, which knows its own
    number. ``run_mission`` deliberately passes nothing (DECISION F077 D10), so
    the trip is numbered one past the entry that caused it: a trip is its own
    event, and two entries sharing one iteration number would break the "one
    entry per iteration" invariant the loop's own ``next_iteration_index``
    depends on.
<<<END PAIR WD-DOCSTRING>>>

Both pairs are REWRITES: neither TO contains its FROM verbatim. The proof is
therefore the FROM string exactly 0x in the file afterwards and the TO string
exactly 1x. Zero marker lines (`<<<BEGIN`, `<<<END`, `FROM:`, `TO:`) may reach
any target file.

── STATE MIRROR — C4 ─────────────────────────────────────────────

`.agent/plan.md` (UNDER 50 lines, keeps `## Goal` and `## Next Steps`): Current
Step R11 as this repair; Next Steps R12 (T003 CLI, `mission resume`, report
surface) and R13 (integration gate, then closure); the open-findings sentence
carries the count and names YOU measured at gate 4. Keep the post-resume
re-trip risk. Cut prose to fit; drop no mandated section.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): the Scope paragraph
describes the watchdog as wired AND its ledger numbering as repaired; the
`## Steps` line gains R11 and renumbers what follows. Also correct the block
ceiling line: R-0389 records that the 240-line figure was exceeded without
measurement, so that constraint now reads that the reviewer MEASURES the block
mechanically before emission and keeps it under 400 (DECISION F105 D5), the
cap that is actually enforceable, with 240 named as the preferred target rather
than a ceiling nobody counted. Change nothing else in either file.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather than
routing around it. If anything in this block contradicts AGENTS.md or the code
you find on disk, STOP, write the contradiction into the handback, and end the
round — do not widen your own scope to resolve it, and do not guess.
──────────────────────────────────────────────────────────────────
