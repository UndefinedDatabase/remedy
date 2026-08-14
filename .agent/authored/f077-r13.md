── STEP T003-inventory/1 — F077 Autonomy watchdog · R13 ──────────

Goal:        Record R12's verdict and the reviewer's own miscount, then
             INVENTORY T003's surface read-only, so R14 can order the manual
             CLI, the `mission resume` verb and the report change against
             measured facts instead of guesses.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f077-r13.md`
  C0b  `cp` it to `.agent/last_block.md`
  C1   FINDINGS FIRST, own commit: append the authored GATE-R12 slice, then
       the authored FINDING-R392 slice, to `.agent/live_review.md`, in that
       order
  C2   write `.agent/f077_t003_inventory.md` — the read-only T003 inventory,
       answering the eight questions below with file-and-symbol evidence
  C3   mirror the round into `.agent/plan.md` and `.agent/context.md`
  C4   handback: rewrite `.agent/handoff.md`

Change:      EXACTLY these files, and nothing beyond them:
             `.agent/authored/f077-r13.md`, `.agent/last_block.md`,
             `.agent/live_review.md`, `.agent/f077_t003_inventory.md`,
             `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md`.
             Seven files. This round is READ-ONLY with respect to the product:
             NO file under `packages/`, `apps/`, `tests/` or `docs/` is
             touched. If the inventory tempts you to fix something you find,
             write the finding into the inventory instead — surfacing defects
             without repairing them is what this round is for.

Why an inventory round and not the build: T003 is "the manual CLI + report
surfacing + tests", and the branch has never read that surface. Three of this
feature's rounds have already been spent on assertions the reviewer inferred
rather than measured — R-0387, R-0388 and R-0391 are all that class. The
inventory is the countermeasure: R14 orders nothing that this file has not
first established with a command and a symbol.

Constraints:
  - AGENTS.md Commit Gate before EVERY commit. 500-INSERTION cap per commit.
  - `.agent/plan.md` stays UNDER 50 lines. It is 44 now; keep it there.
  - You never author a `Gate:`, a `Done:`, a `- R-NNNN` or a `Landed:` line.
    The two slices below are the reviewer's text and you apply them verbatim.
  - The inventory is EVIDENCE, not opinion. Every claim names a path and a
    SYMBOL, and every number carries the command that produced it. A question
    you cannot answer is written as UNANSWERED with the reason — never
    guessed, never softened into a plausible-sounding sentence.
  - Do NOT change any threshold default, any config key, `act_on_trips`,
    `watchdog_pass`, `evaluate_ledger`, or the `run_mission` call site.
  - `.agent/STOP`: re-check from disk before you start and again at handback.
    If it appears, finish the commit in hand, write the handoff, and end.
  - Any destructive check runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, never in the primary checkout.

Done when: every gate below has been RUN by you and its REAL value recorded.
"Green" as a word is a finding. The round's base commit is `a9ebc920`.

  1.  `git status --porcelain` → EMPTY. `git worktree list` → exactly 1 line.
  2.  `cmp .agent/authored/f077-r13.md .agent/last_block.md` → exit 0. Report
      the shared sha256 and the line count.
  3.  `grep -c '^Gate: R12 — ' .agent/live_review.md` → 1.
      `grep -c '^- R-0392 — ' .agent/live_review.md` → 1.
      `grep -c '^Landed: ' .agent/live_review.md` → 1, NOT 0. The residual
      `Landed: R-0384` is the live evidence of OPEN finding R-0380 and is
      outside this round's change set; deleting it would destroy R-0380's own
      proof. Report what you measure.
  4.  Recompute the open-finding set MECHANICALLY — every `^- R-\d+ — `
      paragraph minus every `^Done: R-\d+ — ` line — and report the count and
      the names. The reviewer measured 22 open at `a9ebc920`, and C1 registers
      R-0392, so 23 is the expected reading. Report what you measure,
      unadjusted, and name the next free id.
  5.  `grep -c '^## Q[1-8] ' .agent/f077_t003_inventory.md` → 8.
  6.  `git diff --name-only a9ebc920..HEAD -- packages apps tests docs`
      → EMPTY. This is the gate that makes the round read-only; if it prints
      anything at all, you have left your change set.
  7.  `python3 -m pytest tests/orchestration/test_orchestrator_loop.py -q`
      → report the number. The reviewer measured `196 passed` at `a9ebc920`.
      This round changes no test, so a different number is a finding — report
      the real one either way.
  8.  `python3 -m pytest tests/orchestration/test_watchdog.py tests/orchestration/test_mission_e2e.py -q`
      → report the number. The reviewer measured `52 passed` at `a9ebc920` in
      exactly this one invocation.
  9.  Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → number.
      The reviewer measured `42 passed` at `a9ebc920`.
  10. `python3 -m pytest tests/ -q -k "dashboard_contract or resource_safety or test_runner"`
      → number. The reviewer measured `216 passed, 16648 deselected` at
      `a9ebc920`. Run this AFTER drafting both state files and BEFORE
      committing C3, and grep every test that READS `.agent/plan.md` or
      `.agent/context.md` first, validating your draft against all of it
      (R-0162).
  11. `python3 -c "import sys; sys.argv=['remedy','integrity','check','--json']; from apps.cli.grouped import main; sys.exit(main())"`
      → report `passed`, `fail_count`, `check_count`, `high_blockers_open`.
  12. `wc -l .agent/plan.md` → under 50.
  13. Insertions per commit via `git show --numstat`, per commit. None over 500.
  14. `test -e .agent/STOP` → ABSENT or PRESENT, before the round and at
      handback.
  15. `git diff --check a9ebc920..HEAD` → no output; every touched file
      newline-terminated.
  16. `git push -u origin feature/f077-autonomy-watchdog`. No `gh`, no PR.

Handback:    completion report + rewrite `.agent/handoff.md`, item-status
             table covering C0a C0b C1 C2 C3 C4, and this Fortschritt line
             verbatim:
             `~78 % (T001 ✅ · T002 ✅ verdrahtet und grün · T003 inventarisiert) — Schätzung`
             ≤60 lines, or a "Deviations, declared" line naming the real count
             and the mandated content that caused it (DECISION D15). Never
             drop a section. The Next section names, in this order: (1) Phase
             1 rule 1 of docs/agents/self_drive_protocol.md — re-read
             `.agent/STOP` from disk BEFORE rule 2's Open PR Gate; (2) rule 2,
             noting there is NO open PR for this branch and one is created at
             closure, not before; (3) that R14 builds T003 against this
             inventory; (4) that R15 is the integration gate then closure;
             (5) the open-finding count and names you measured at gate 4 and
             the next free id.

── THE INVENTORY — C2, eight questions ───────────────────────────

Write `.agent/f077_t003_inventory.md`. Each question is its own `## Q<n> `
heading, in order, so gate 5 counts eight. Answer from the code, not from
this block: where this block states a fact, treat it as a claim to CHECK and
report what you actually find, including where the reviewer is wrong.

## Q1 — how a mission verb is wired, end to end
Trace ONE existing read-only mission verb — `mission ledger` is the closest
analogue to what T003 needs — from the command catalog entry through argument
parsing to its handler function, naming every file and every symbol on that
path. `apps/cli/command_catalog.py` carries a `command_id="mission.ledger"`
entry; `apps/cli/commands/mission_cmd.py` carries `_cmd_mission_ledger`.
Establish what ELSE must be edited for a new verb to exist — dispatch tables,
`related=` tuples, help rendering, anything the two files above do not cover.
The deliverable is a checklist R14 can order verbatim.

## Q2 — the read-only evaluation entry point
`packages/orchestration/watchdog.py` exposes `evaluate_ledger`, `act_on_trips`
and `watchdog_pass`. The feature file says the manual CLI is for AUDITS, so it
must not pause anything or enqueue anything. Determine which of the three is
side-effect free, prove it by reading the body rather than the name, and
record its exact signature and return shape — what a `Trip` carries, and which
fields the evidence triple (what, since when, the numbers) maps onto. If none
of the three is safely callable read-only, say so plainly; that changes T003's
shape and R14 needs to know before it orders anything.

## Q3 — the `mission resume` verb that does not exist
`_status_for_verb` in `apps/cli/commands/mission_cmd.py` maps `achieve`,
`abandon` and `pause` onto mission statuses and has no `resume`. Read
DECISION F077 D4 in `.agent/decisions.md` and report what it actually
requires. Then determine which status `resume` must set, by reading
`packages/orchestration/mission_state.py` for the status constants and
`set_mission_status`, and whether any existing caller already performs that
transition under another name. Report whether `_status_for_verb`'s dict is the
ONLY place a verb list is encoded, or whether the catalog and the parser carry
their own copies that would drift.

## Q4 — the dedup marker and what clears it
The feature's Acceptance says "resume clears exactly that trip's dedup".
`watchdog.py` has `watchdog_decision_marker`. Establish where the dedup state
actually LIVES on disk, which function writes it, which function reads it, and
what — if anything — currently clears it. Name every writer and every reader
mechanically with grep, and report the counts; do not infer the set from
function names. If nothing clears it today, that is the answer and it is the
most important sentence in this file.

## Q5 — the report surface
The catalog's `mission.run` entry lists `related=("mission.report", ...)`.
Find the report command, name its handler and the function that renders its
body, and identify the exact insertion point where "a paused-by-watchdog
mission's report leads with the trip" would go. Report whether the renderer
already has a notion of leading or priority sections, or whether T003 would be
introducing one.

## Q6 — the guards that already constrain these files
Pre-emission checklist item 7, run as WORK instead of as reviewer habit. For
`mission_cmd.py`, `command_catalog.py` and whatever Q5 names, grep the suite
for tests that count strings over the WHOLE file — every `.count(` and every
`== 1` assertion in the files that `grep -rl` returns. A guard of that shape
makes a correct second call site unsatisfiable, and R14 must know about it
BEFORE it orders one, not after the round loses an item to it. List each guard
with its path, its test name and the string it pins.

## Q7 — the catalog's completeness contract
Adding a verb usually trips a contract test before it trips a behavioural one.
Find the tests that assert the command catalog is complete, consistent, or in
sync with the parser and the help output — `tests/` for `command_catalog`,
plus whatever `dashboard_contract` covers. For each, state what it would
demand of a new `mission watchdog` and a new `mission resume` entry: required
fields, description style, `related=` symmetry, ordering. This is the list
R14's block turns into constraints.

## Q8 — what a paused mission does on the next pass
The watchdog writes `paused` with no human in the loop, and
`orchestrator_loop.run_mission`'s safe point refuses to run a mission that is
not active. Read that safe point and report exactly what it does — the status
check, what it records, and what it returns — so R14 knows what `resume` must
restore for a run to continue, and whether the ledger entry the safe point
writes interacts with the trip entry that preceded it. Note the known
follow-on the plan already carries: a mission resumed after its watchdog
decision is answered still holds the tripping run in its ledger and will trip
again on the same evidence. Report whether the code confirms that risk.

── AUTHORED SLICES — apply byte for byte ─────────────────────────

Each slice is ONE physical line, separated from its neighbour by one blank
line, matching the file's existing shape. Both are APPENDS to the end of
`.agent/live_review.md`, GATE-R12 first.

<<<BEGIN GATE-R12>>>
Gate: R12 — PASS. Verification tier: round gate plus canary plus the state-file contract readers plus `integrity check`; no full-suite claim is made. Every gate was re-run by the reviewer rather than read from the handback. The change set is exactly the eight ordered files and nothing else, confirmed by `git diff --numstat 28c50487..HEAD`; per-commit insertions are 253, 197, 7, 39, 16, 37 and 85, none over 500. The round's load-bearing claim was verified from the source and not from the worker's summary: `run_mission` spans lines 936 to 1341, `_record` is defined at line 1036 nested inside it, and the executed move's call at 1210 is unconditional after `execute_move` while the R-0190 blocked-completion escalation's call at 1253 is reached in the SAME pass whenever `outcome.terminal` is false and the streak hits `BLOCKED_COMPLETIONS_BEFORE_ESCALATION` — so two entries share one `iteration`, R-0388's invariant never existed, and DECISION F077 D11 is sound. The red-proof was run by the reviewer in a disposable worktree at `28c50487`: `1 failed, 195 passed`, failing exactly on `test_one_entry_per_iteration_numbered_from_one` with "Left contains one more item: 3", against `196 passed` at HEAD — a real colour change on the ordered test, and the import-path hazard of finding R-0337 does not apply because the range diff touches no file under `packages/` or `apps/` at all, so the imported product is byte-identical at both ends. The remaining gates at HEAD: `test_watchdog.py` plus `test_mission_e2e.py` in one invocation `52 passed`, canary `42 passed`, the contract readers `216 passed, 16648 deselected`, `integrity check --json` `passed=true fail_count=0 check_count=5`, `wc -l .agent/plan.md` 44, the tree clean and `git worktree list` one line. The open set was recomputed from the record and not carried forward: 26 registered paragraphs minus 4 `Done:` lines is 22 open with no duplicate id, matching the handback exactly. The `I001` at `test_orchestrator_loop.py:37` reproduces identically on the base blob, so it is genuinely pre-existing and correctly left unfixed. Two judgements the round made that this gate endorses: the worker reported `^Landed: ` as 1 against an ordered 0 rather than deleting the residual `Landed: R-0384`, which is the live evidence of open finding R-0380 and outside the change set; and it applied the reviewer's slices verbatim while recording their arithmetic drift as a declared deviation instead of silently correcting reviewer text. Both are the behaviour the split exists to produce. What this gate does NOT say: no production code was executed differently this round, because none changed, so nothing here is evidence about the watchdog's runtime behaviour beyond what R10 and R11 already established.
<<<END GATE-R12>>>

<<<BEGIN FINDING-R392>>>
- R-0392 — Low — the R12 block, finding R-0391, gate GATE-R11 and DECISION F077 D11 all state that `_record` has "eleven call sites", and all four are wrong by one: `grep -c '_record(iteration' packages/orchestration/orchestrator_loop.py` returns 11, but the match at line 1036 is the `def` and the calls are at 1064, 1119, 1180, 1191, 1203, 1210, 1253, 1267, 1293 and 1296 — TEN, all inside `run_mission`, which spans 936 to 1341. The reviewer read a `grep -c` total and never subtracted the definition line it had itself included in the pattern. The count is also ambiguous in a second way the record does not mention: a completely unrelated `_record` closure is defined at line 916 inside `make_orchestrator_call_recorder` and returned at 933, so "eleven `_record` call sites" is wrong whether the reader counts the ledger writer's calls or the file's `_record` symbols. Nothing downstream changes — the claim D11 actually rests on is that TWO calls fire in one pass at one `iteration`, verified independently at 1210 and 1253, and the ALTERNATIVES paragraph's argument holds unchanged at ten — which is why this is Low and not Medium. It is registered anyway because of where it sits: R-0391 is the finding whose whole lesson is that a reviewer must count the writers of a field mechanically before authoring against it, and the sentence delivering that lesson miscounts those writers. The worker measured the drift and declared it as Deviation 2 of the R12 handback rather than correcting the reviewer's text, which is correct behaviour and is the only reason it is on the record at all. From here, a count that appears in authored text is copied from the command output WITH the command's own exclusions applied — a `grep -c` that matches a definition as well as its calls is reported as both numbers or as neither.
<<<END FINDING-R392>>>

── STATE MIRROR — C3 ─────────────────────────────────────────────

`.agent/plan.md` (UNDER 50 lines; it is 44 now, and it keeps `## Goal`,
`## Current Step`, `## Next Steps` and `## Risks`): Current Step becomes R13,
this inventory round, naming that R12's verdict and R-0392 landed in C1 and
that no product file was touched. Next Steps become R14 (build T003 against
the inventory: the manual CLI, `mission resume`, the report surface and their
tests) and R15 (integration gate, then closure). The open-findings sentence
carries the count and the names YOU measured at gate 4 and the next free id.
Keep the post-resume re-trip risk and the goal_drift risk. Update the
open-findings count in the Risks section to match gate 4.

`.agent/context.md` (keeps `## Active Branch` with the `feature/` slug, the
substring `Steps`, an F-id, and `resource` or `pytest`): add
`.agent/f077_t003_inventory.md` to the In-scope list beside the T002
inventory it sits next to; update the open-findings count and next free id at
the end of the Scope paragraph to what gate 4 measured; and extend the
`## Steps` line with R13 and the renumbered R14 and R15. Change nothing else
— in particular the block-ceiling constraint line is already correct and must
not be touched.

── HANDBACK ──────────────────────────────────────────────────────

Report every gate's REAL value. Declare every deviation with its reason. If a
gate cannot run, say so with the exact command and the exact error rather
than routing around it.
──────────────────────────────────────────────────────────────────
