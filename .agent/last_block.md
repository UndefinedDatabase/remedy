── STEP T002-wiring/1 — F077 Autonomy watchdog · R10 ────────────

Goal:        Give `act_on_trips` its call site in `run_mission`, prove the pause
             actually stops the next iteration from dispatching, and make D7's
             watchdog docstring clause true in the same commit as the caller.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r10.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   append the authored GATE-R9 slice to `.agent/live_review.md`
  C2   append the authored DECISION-D9 slice to `.agent/decisions.md`
  C3   the wiring: `watchdog_pass`, the `run_mission` call site, the two
       docstring clauses, and the new tests
  C4   mirror the round into `.agent/plan.md` and `.agent/context.md`
  C5   handback: rewrite `.agent/handoff.md`

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r10.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/decisions.md`,
             `packages/orchestration/watchdog.py`,
             `packages/orchestration/orchestrator_loop.py`,
             `packages/orchestration/mission_state.py`,
             `apps/cli/commands/mission_cmd.py`,
             `tests/orchestration/test_watchdog.py`,
             `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`.
             Twelve files. `tests/orchestration/test_mission_e2e.py` is NOT in
             this list and is touched ONLY if gate 8's probe reports it red —
             see Done-when 8, which is the sole authority for that file.

C3, in detail:
  (a) In `packages/orchestration/watchdog.py`, after `act_on_trips`, add ONE
      new public function:

          def watchdog_pass(project_id, mission_id, *, iteration=None,
                            root=None, now=None) -> list[TripAction]

      It reads the mission's ledger, resolves thresholds from config, evaluates
      all three tripwires over that ledger, and returns `act_on_trips(...)` on
      whatever tripped — returning `[]` without writing anything when nothing
      did. Every heavy import lives INSIDE the body, exactly as `act_on_trips`
      does it: a module-level import of `orchestrator_loop` recreates the cycle
      this whole design exists to avoid. Give it the one-line WHY comment
      directly above the definition, in the file's own idiom.
  (b) In `packages/orchestration/orchestrator_loop.py`, inside `run_mission`,
      call `watchdog_pass` on the ledger the iteration just extended, passing
      the loop's OWN `iteration` (DECISION F077 D6), `root` and `now`. The
      insertion point is immediately AFTER this existing four-line sequence and
      BEFORE the `R-0190` blocked-completion block:

          _record(iteration, context.digest, move.model_dump(), outcome, cost)
          if outcome.terminal:
              result.terminal, result.detail = outcome.status, outcome.detail
              return result

      `_record(iteration, context.digest, move.model_dump(), outcome, cost)`
      occurs MORE THAN ONCE in this function; the four-line sequence above is
      the unique one. Verify that uniqueness by grep and report the count you
      measured — do not navigate by line number, this branch has moved them.
      A terminal iteration is deliberately NOT watched: the run is already over
      and pausing it would say nothing. Import `watchdog_pass` inside the
      function body, never at module level.
  (c) In `packages/orchestration/mission_state.py`, apply pair MS-DOCSTRING.
  (d) In `apps/cli/commands/mission_cmd.py`, apply pair CMD-DOCSTRING.
  (e) In `tests/orchestration/test_watchdog.py`, add tests that pin the seam
      through the REAL default config thresholds — no monkeypatched threshold,
      no injected stub:
        1. a scripted `run_mission` whose moves dispatch THREE times in a row
           on ONE milestone with no `declare_milestone_done` between them
           trips `no_progress`: the mission ends `paused`, the ledger carries
           exactly one `watchdog_tripped` entry, and exactly one open decision
           carries the `[watchdog:no_progress]` marker;
        2. the ACCEPTANCE claim, which is the point of the round: after that
           trip, a SECOND `run_mission` invocation on the same mission
           dispatches nothing — assert its terminal is `mission_not_active` and
           that the ledger gained no `dispatch_job` entry;
        3. the negative control, so neither of the above can pass vacuously: a
           scripted run that trips nothing leaves ZERO `watchdog_tripped`
           entries in its ledger and leaves the mission `active`.
      Follow the existing fixtures and scripted-`call_fn` idiom already in
      `tests/orchestration/`; do not invent a new harness.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. One logical step per commit.
    500-INSERTION cap per commit (the `+` column only, DECISION F104 D1).
  - The F077 Do-not-touch list holds: no repair logic, no class-expectation
    anomaly detection, no loop policy. The watchdog's only writes stay the
    mission status, one escalation record, and the ledger append. A diff where
    the watchdog "helpfully" fixes anything is rejected on sight.
  - Do NOT add a new seam parameter to `run_mission`. The tests force a trip
    through the SCRIPTED MOVES under default config, which is what makes them
    evidence about the production path rather than about a stub.
  - Do NOT change any threshold default, any config key, or `act_on_trips`.
  - Out of scope, named so it is not improvised into the diff: a mission that
    is resumed AFTER its decision is answered still carries the tripping run in
    its ledger and will trip again on the next pass. That is real, it is
    `mission resume` semantics, and DECISION F077 D4 assigned `mission resume`
    to T003. Record it in `.agent/plan.md` under Risks; do NOT solve it here.
  - Repository-wide `ruff check` is RED on main with pre-existing errors and is
    NOT a gate (R-0364); ruff is gated scoped to the files this round changes.
  - Destructive checks (gate 13) run ONLY inside a disposable `git worktree`
    under `.remedy-wt/`, never in the primary checkout, which must satisfy
    `git status --porcelain` == empty at handback.
  - `.agent/STOP`: re-check it from disk before you start and again at handback.
    If it appears, finish the half-written commit, hand off, and stop.
  - You never write a `Done:` paragraph in `.agent/live_review.md`. If you fix
    something the reviewer has not yet resolved, mark it
    `Landed: R-XXXX — <one line: what changed, which commit>` and nothing else.

Done when: every gate below has been RUN by you and its REAL value recorded in
the handback. "Green" as a word is a finding. The round's base commit is
`24600478` (R-0368: the base is the handback this round starts from).

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r10.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R9 — PASS' .agent/live_review.md` → 1.
      `grep -c '^## Steps' .agent/live_review.md` → 1.
      `grep -c '^## DECISION F077 D9 ' .agent/decisions.md` → 1.
  4.  Recompute the open-finding set MECHANICALLY from `.agent/live_review.md`
      — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — and
      report the count and the names. Report what you measure, unadjusted; if
      it is not nineteen, say the number you got and do not reconcile it.
  5.  `python3 -c "import packages.orchestration.orchestrator_loop"` → exit 0.
      `python3 -c "import packages.orchestration.watchdog"` → exit 0. Both
      prove no module-level cycle was created.
  6.  BASELINE FIRST, at `24600478`, then again at your HEAD, and report BOTH
      numbers for each:
        `python3 -m pytest tests/orchestration/test_watchdog.py -q`
        `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      Also `grep -c "def test_" tests/orchestration/test_watchdog.py` so no test
      is silently collected twice or skipped.
  7.  `python3 -m pytest tests/cli/test_mission_cmd.py -q` → report the number.
  8.  THE PROBE — this gate orders a MEASUREMENT, not a colour, and no expected
      number is stated anywhere in this block on purpose. Run
      `python3 -m pytest tests/orchestration/test_mission_e2e.py -q` at
      `24600478` FIRST and record the number. Run it again at your HEAD after
      C3 and record that number. REPORT BOTH.
        - If the second run is GREEN: the four guards DECISION F077 D8 predicted
          would break did not break. Change NOTHING in that file, say so
          plainly in the handback, and name which of the three tripwires you
          confirmed stayed inert in that scenario and why.
        - If the second run is RED: name every failing test with its real
          assertion error, repair ONLY what is actually red, and add
          `tests/orchestration/test_mission_e2e.py` to the change set as a
          declared, reasoned addition.
      Either outcome is a correct round. A worker who reports a green probe is
      telling the truth about a reviewer's arithmetic, and that is worth more
      than a repair that had nothing to repair.
  9.  `ruff check` over ONLY the files this round changed under `packages/`,
      `apps/` and `tests/` → report the exact output.
  10. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → report the
      number.
  11. State-file contract readers, whose assertions your `.agent/plan.md` and
      `.agent/context.md` edits must not break:
      `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → report the number. Before authoring either state edit, grep every test
      that reads that path and validate the draft against ALL of it (R-0162).
  12. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count` and the
      `high_blockers_open` message.
  13. RED-PROOF, AS A PROBE. In a disposable `git worktree` under `.remedy-wt/`
      at your HEAD, DELETE the `watchdog_pass` call you added in C3(b) and run
      `python3 -m pytest tests/orchestration/test_watchdog.py -q`. Report
      whether any test failed and WHICH. Then remove and prune the worktree and
      re-prove gate 1. A green result here means the new tests do not reach the
      call site and is a real finding about the tests, not about the loop — say
      so if that is what you measure.
  14. Insertions per commit, measured with `git show --numstat`, reported per
      commit. None over 500.
  15. `test -e .agent/STOP` → report ABSENT or PRESENT, checked before the round
      and again at handback.
  16. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.
  17. Trailing-whitespace scan over every touched file → none; all
      newline-terminated.

Handback:    completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch,
             per-commit changed-files tables, the REAL verification values
             above, the item-status table covering C0a C0b C1 C2 C3 C4 C5, open
             findings count, next expected action. Repeat the brief's
             Fortschritt line verbatim, including the Schätzung label:
             `~70 % (T001 ✅ · T002 Aktion ✅ unverdrahtet · Verdrahtung R10 · T003 offen) — Schätzung`
             The ≤60-line cap applies; if the mandated content genuinely does
             not fit, carry a "Deviations, declared" line naming the real line
             count and the specific mandated content that caused it (DECISION
             D15). Never drop a mandated section to meet the cap.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

<<<BEGIN GATE-R9>>>
Gate: R9 — PASS. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. R9 was STATE ONLY and the reviewer re-executed all sixteen of its gates rather than reading them: `cmp .agent/authored/f077-r9.md .agent/last_block.md` exits 0 with the shared sha256 `8a46da65639b2776cfbb97532ffad404f733acfb4ddffff90fbeef31715e0446` over 99 lines, so the block the worker was given and the block on disk are the same bytes. The two appended slices were traced rather than trusted: each was re-extracted from the COMMITTED `.agent/authored/f077-r9.md` at `b86dcfd3` and confirmed to be a verbatim substring of it, present EXACTLY once in `.agent/live_review.md`, at 1937 and 5789 bytes — the two numbers the handback declared, which measure as 1925 and 5759 CHARACTERS, the difference being UTF-8 em dashes and not a discrepancy. `git show --numstat b71c66db -- .agent/live_review.md` reads `4 0`, so the deletion column is zero and nothing above the append moved. The open set was recomputed mechanically from the record instead of carried forward (checklist item 10): 21 registered minus 2 resolved gives NINETEEN open — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378, R-0379, R-0380, R-0381, R-0382, R-0385, R-0386 — exactly the set the handback names, with no duplicate id. `git diff --name-only c4be17e8..HEAD` returns six files, all under `.agent/`, and `git diff --stat c4be17e8..HEAD -- packages/ apps/ tests/ docs/` is empty, so a state-only round stayed state-only. Per-commit insertions measure 99, 91, 34 and 95, none over 500. Suites re-run by the reviewer at this HEAD: the canary `42 passed`, `tests/orchestration/test_watchdog.py` `25 passed`, and the state-file contract readers `216 passed` — a broader selection than the worker's three-file `142 passed`, and green over the wider set. `integrity check --json` reports `passed: true` with `high_blockers_open` at "no open blocker/high findings". The tree is clean, `git worktree list` is one line, and the branch is in sync with origin. The handback's declared 130 lines measures at 130 by both `wc -l` and `grep -c ""`, and every touched file is newline-terminated with zero trailing whitespace, so the declaration is accurate and the DECISION D15 stated cause is the mandated content it names. No finding is registered against R9. Per §4.13 this verdict had no on-disk home when R9 closed the session — R9 was the LAST round of that session and a round cannot record the gate on itself — so it is written here at the start of R10 rather than treated as a missing gate. What this gate does NOT say, and it is the same sentence R8 earned: `act_on_trips` still has no caller at `24600478`, so nothing in a running mission reaches it, and every PASS on this branch so far is a statement about the action in isolation.
<<<END GATE-R9>>>

<<<BEGIN DECISION-D9>>>
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
<<<END DECISION-D9>>>

<<<BEGIN PAIR MS-DOCSTRING — APPEND-shaped, file packages/orchestration/mission_state.py>>>
FROM:
    ``packages.orchestration.orchestrator_loop``.  A status on disk is
    therefore NOT evidence that a human put it there.
TO:
    ``packages.orchestration.orchestrator_loop``.  A status on disk is
    therefore NOT evidence that a human put it there.

    Since F077 there is a third writer.  The autonomy watchdog's
    ``watchdog.act_on_trips`` writes ``paused`` when a tripwire fires, and
    ``orchestrator_loop.run_mission`` calls it once per continuing iteration,
    so a mission can pause with no human and no terminal move involved.
<<<END PAIR MS-DOCSTRING>>>

<<<BEGIN PAIR CMD-DOCSTRING — APPEND-shaped, file apps/cli/commands/mission_cmd.py>>>
FROM:
    loop — see ``mission_state.set_mission_status`` for the full caller list —
    so F056's "nothing moves on its own" holds for this COMMAND, not for the
    status field.
TO:
    loop — see ``mission_state.set_mission_status`` for the full caller list —
    so F056's "nothing moves on its own" holds for this COMMAND, not for the
    status field.

    Since F077 the autonomy watchdog writes ``paused`` the same way and with no
    human in the loop either, so the status field has three kinds of writer and
    this command is only one of them.
<<<END PAIR CMD-DOCSTRING>>>

Both pairs are APPEND-shaped: each TO literally CONTAINS its FROM. The proof is
therefore FROM exactly 1x in the file afterwards, and each TO-ONLY line exactly
1x AMONG THE LINES THAT COMMIT'S DIFF ADDS — not a whole-file count, and not a
"FROM 0x" count, which is unattainable by construction for an append. Zero
marker lines (`<<<BEGIN`, `<<<END`, `FROM:`, `TO:`) may reach any target file.

── STATE MIRROR — C4 ─────────────────────────────────────────────

`.agent/plan.md` (≤50 lines, keeps `## Goal` and `## Next Steps`): set Current
Step to R10 describing this round; Next Steps to R11 (T003 CLI, `mission
resume`, report surface) and R12 (integration gate, then closure); update the
open-findings sentence to the count YOU measured at gate 4, naming the findings;
and add to Risks the post-resume re-trip named in Constraints above, in one or
two lines, as T003's work.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): update the Scope
paragraph so it describes the watchdog as WIRED at this commit rather than
pending, and extend the `## Steps` line so R10 reads as done and R11/R12 remain
ahead. Change nothing else in either file.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather than
routing around it. If anything in this block contradicts AGENTS.md or contradicts
the code you find on disk, STOP, write the contradiction into the handback, and
end the round — do not widen your own scope to resolve it, and do not guess.
──────────────────────────────────────────────────────────────────
