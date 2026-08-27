── STEP RECORD ROUND / F031 — ROUND R49 ───────────────────────────────
Goal:        Persist what the R48 gate produced. Register findings R-0700,
             R-0701 and R-0702, record R48's PASS, and advance the plan. NO
             CODE CHANGES: this round writes only `.agent/` state, because a
             verdict and three findings that live in a session rather than on
             disk are lost when it ends. R48 left the branch GREEN and this
             round must not disturb that.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the three findings · C3 the R48 gate entry · C4 handback ·
             then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r49.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. NO FILE UNDER `apps/`, `packages/`, `tests/`
             OR `docs/` — the repairs R-0701 and R-0702 name belong to a code
             round and this one deliberately does not start them.
             `.agent/decisions.md` IS NOT IN THIS CHANGE SET: no decision is
             ruled this round, and the plan's renumbering of the clarification
             FORM needs none, because round attributions in `.agent/plan.md`
             are rewritten state rather than a ruling.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. The findings land at
    C2 BEFORE the gate entry at C3. No pair may be reordered. LEDGER49 states
    facts about THIS round's own commits, and this constraint is what makes
    them true on landing.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R48. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph,
    never edit a finding's wording. ALL THREE FINDINGS ARE REGISTERED HERE AND
    DELIBERATELY NOT FIXED HERE: R-0701's repair edits
    `tests/ui_server/test_command_dispatch.py` and R-0702's edits
    `packages/orchestration/ui_server.py`, neither of which is in this round's
    change set, and R-0700 is a rule about handbacks that this round's own
    handback obeys rather than repairs.
 5. THE LEDGER SETS MOVE ONCE EACH. Across C2 `^- R-\d+ — ` moves 260 to 263
    with the ids ADDED exactly `R-0700`, `R-0701` and `R-0702` and none
    REMOVED. Across C3 `^Gate: F\d+ R\d+ — ` moves 29 to 30 with the ADDED key
    exactly `F031 R48`. Across both, `^Done: R-\d+ — ` stays 6, `^Landed: R-`
    stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 254 before C2 and
    257 after C3.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
 7. NOTHING IS VERIFIED BY MUTATION THIS ROUND, because nothing executable
    changes. No `git worktree` is created. `.remedy-wt/f031-r49-block.md` is the
    reviewer's scratch copy — leave it alone. Earlier rounds' scratch under
    `.remedy-wt/` (`r47*`, `r48*`) is also left alone; never delete anything
    there by glob. Nothing under `.remedy-wt/` is ever committed and
    `git status --porcelain` reads 0 lines at every commit.
 8. YOUR HANDBACK OBEYS THE CAP THAT R-0700 IS ABOUT. AGENTS.md gives ≤60 lines,
    or ≤100 when per-commit tables of more than 5 commits require it. There is
    no tier above 100. This round makes FIVE commits, so derive your cap from
    that and stay inside it; if the MANDATED content genuinely does not fit,
    write the DECISION D15 "Deviations, declared" line naming your actual line
    count and the specific mandated content that caused the overage. Do not
    invent a tier.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`. Run
    pytest SERIALLY — never two pytest processes alive at once.

Done when — run every gate yourself and record its REAL exit code. G1 through G7
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at
     C0a, as mirrored at C0b, and as read off disk at C3 — all three must be
     EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R49 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with
     `git show <rev>:<path>` into memory; never write a past blob over a
     tracked file to read it. `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus FINDINGS49; at C3 equals ITS OWN
     pre-commit blob — which you READ rather than take from this block — plus
     ONE newline plus LEDGER49. The reviewer measured the BASE blob at
     `4f474e19` itself: `.agent/live_review.md` is 878135 bytes. If it reads
     differently before C2, something moved that this round did not order —
     stop and hand back. For EACH append report both byte counts and the sum.
     Then confirm EACH with a SECOND, independent reader: split the whole file
     on blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in
     that slice — never a number this block asserts — and compare the LAST N
     units of the file against the slice's N paragraphs IN ORDER. Report N and
     the unit count before and after for each. THE NEGATIVE CONTROL GOES ON THE
     FIRST APPENDED PARAGRAPH, which is the position a tail-only reading cannot
     see: flip ONE byte IN MEMORY inside paragraph 1 of each slice and report
     that BOTH readers REJECT it. For any slice whose N is 1, say so and note
     that paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     and gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 5 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. NOTHING EXECUTABLE MOVED, PROVED RATHER THAN ASSERTED, AND THE TIP IS
     STILL GREEN. Report `git diff --name-only 4f474e19..C3` and confirm that
     EVERY path in it begins with `.agent/`, listing any that does not. Report
     `git diff --stat 4f474e19..C3` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` and confirm each of the four is EMPTY. Then, in the
     PRIMARY checkout at C3, run SERIALLY — never two pytest processes alive at
     once — the canary `python3 -m pytest tests/cli/test_golden_path.py -q` and
     the four state readers `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`, reporting each REAL exit
     code and count. At `4f474e19` the reviewer measured these itself at 42,
     486, 52, 21 and 16, every one at exit 0. These five are ordered BECAUSE
     this round rewrites `.agent/` state and those suites read it; a round that
     touches no code can still turn them red.
 G7. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1 and `.agent/live_review.md` at C3, against
     a CONTROL count over the C0a blob, which is not 0. Compare the path set of
     G6 BOTH WAYS against this round's expected set — the Change line's list
     MINUS `.agent/handoff.md`, excluded because the handback is written at C4,
     outside a range ending at C3 — and report both residues EMPTY. Report each
     commit's insertions from `git diff --numstat`, confirm each is
     single-parent and under 500. Report `git ls-files .remedy-wt` as 0 and
     `git worktree list` as 1 line at C3. Report the reflog FOR THIS ROUND'S
     OWN COMMITS ONLY: every operation prefix must read `commit`, and among
     those entries `amend`, `rebase` and `cherry` must be 0 each. Do not count
     those words over the whole reflog, which holds this repository's entire
     history and is not what this gate asks.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G7, the item-status table covering
             C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE for G1
             through G7 with its real exit code, an explicit line naming
             R-0700, R-0701 and R-0702 as registered and deliberately NOT fixed
             here, the open-findings count, and the next expected action. SAY
             PLAINLY THAT THIS ROUND CHANGED NO EXECUTABLE FILE AND THAT THE
             BRANCH TIP IS GREEN. THE NEXT ACTION SECTION NAMES, IN THIS ORDER:
             re-read `.agent/STOP` from disk first, then the Open PR Gate, then
             review this round's handback, then R50. Obey constraint 8's cap.
             Then push with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R49
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D25.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R49 is a RECORD ROUND and changes no executable file: it registers R-0700,
R-0701 and R-0702 and records R48's PASS. THE FLIGHT-PLAN APPROVAL IS NOW
ANSWERABLE END TO END — the door dispatches an `fp:` id to
`resolve_flight_plan_approval`, the pending card offers the two words that door
accepts, and the answerability key mirrors both of its refusal conditions — and
the branch tip is green at 486 in `tests/ui_server/` and 455 under vitest.

## Next Steps
1. R50: retire the stale round number R-0702 names in
   `packages/orchestration/ui_server.py`, extract the duplicated helper R-0701
   names, then land the clarification FORM over `payload.clarifications`.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R50's FORM is where an operator gains any other choice.
- SIX ROUNDS RAISED A REVIEWER-SPEC DEFECT WITH ONE ROOT CAUSE — a block
  ordering something against a file it had not read. Step 2 above is the fix
  and it is the highest-value work left in this feature.
- A ROUND NUMBER IS BAKED INTO SHIPPED PRODUCTION TEXT (R-0702) and went stale
  within one round of landing. The lesson generalises past this instance: a
  docstring names the DECISION or the feature, never the round.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 254 at `4f474e19`
  and this round takes it to 257.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R49

<<<SLICE FINDINGS49
- R-0700 — Medium, A HANDBACK RAN TO 160 LINES AGAINST A 100-LINE MAXIMUM AND JUSTIFIED IT WITH A TIER AGENTS.md DOES NOT DEFINE, INSTEAD OF DECLARING THE OVERAGE THE RULES PROVIDE FOR. Raised by the reviewer at the R48 gate. THE MEASUREMENT, read at `4f474e19`: `wc -l .agent/handoff.md` is 160, and the file carries a `## Deviations & assumptions` section but no "Deviations, declared" line naming its line count and the mandated content that caused the overage. The worker's own report states the reasoning: "Handback is 160 lines, inside the >10-commit tier (11 commits); no D15 overage declared." AGENTS.md defines no such tier. Its handoff rule gives ≤60 lines, "≤100 when per-commit tables of >5 commits require it", and then ONE further allowance — the DECISION D15 stated-cause overage, which requires the handback to carry a line naming its actual length and the specific mandated content that did not fit. A round with eleven commits plainly earns that allowance; what it does not earn is a silent tier. WHY MEDIUM AND NOT LOW: the cap is not about aesthetics, it is the mechanism that makes an overage VISIBLE and therefore reviewable, and an invented tier removes exactly that signal — a reviewer scanning for a declaration finds none and concludes the cap was met. THE PRECEDENT WAS AVAILABLE AND RECENT: R47's worker, on the immediately preceding round, declared its own 185-line handback as a D15 overage with the cause named, so the mechanism was demonstrated one handback earlier in the same feature. PART OF THE CAUSE IS THE REVIEWER'S BLOCK, which said only "Derive your line cap from AGENTS.md yourself, from the commit count you actually made" — wording that invites a worker to infer a tier from a commit count rather than to read the two the rule actually states. The R49 block replaces that sentence with the cap stated outright and the instruction not to invent a tier, and that is where the fix belongs: in the block's wording, not in a repair commit.

- R-0701 — Low, A TWENTY-ONE-LINE TEST HELPER IS BYTE-IDENTICAL IN TWO CLASSES OF THE SAME FILE. Raised by the reviewer at the R48 gate, and declared by the worker before the reviewer reached it. THE MEASUREMENT, read at `4f474e19`: `tests/ui_server/test_command_dispatch.py` defines `_start_server` twice, once in `TestJobStopDispatchEffects` and once in the new `TestFlightPlanApprovalDispatchEffects`, and the reviewer's own script extracted both bodies and compared them — BYTE-IDENTICAL at 21 lines each. THE WORKER'S REASON FOR NOT EXTRACTING IT IS SOUND AND THE REVIEWER ACCEPTS IT: AGENTS.md forbids mixing a refactor into another commit, and C6 was a test-adding commit, so extracting a shared helper there would have been exactly that mix. It declared the duplication in its handback rather than leaving it to be found, which is the required behaviour and is why this is Low rather than a deviation. WHY IT IS STILL WORTH AN ID: two copies of a server-start helper drift, and the failure mode is quiet — a timeout raised in one copy and not the other makes one class flaky on a slow runner while its sibling stays green, and the divergence reads as an environment problem rather than as a duplicate. THE FIX IS A REFACTOR IN ITS OWN COMMIT, extracting `_start_server` to a module-level helper both classes call, and it lands at R50 where it can be the commit AGENTS.md asks it to be.

- R-0702 — Medium, SHIPPED PRODUCTION TEXT NAMES A FUTURE ROUND NUMBER, AND IT WENT STALE WITHIN ONE ROUND OF LANDING. Raised by the reviewer at the R48 gate, against text the reviewer's own R47 block ordered. THE MEASUREMENT, read at `4f474e19`: `packages/orchestration/ui_server.py` line 3701, inside `_dispatch_decision_resolve`'s docstring, reads "Round R48's form over `payload.clarifications` is where any other choice comes from". R48 has now happened and was not the form — it was the repair round for R47's own defects — so the sentence is false in shipped code. `.agent/decisions.md` carries the same attribution twice, at the lines where DECISION F031 D23 and D24 name R48 as the FORM's round, and those two are correct as written because a decisions entry is a dated record of what was decided THEN; the docstring is not, because a docstring describes what is true NOW. WHY MEDIUM: nothing executes differently and no test can catch it — a stale sentence in a docstring is invisible to every gate this repository runs — but it misdirects the next reader of the door, which is precisely the audience that docstring was extended to serve. THE ROOT CAUSE GENERALISES PAST THIS INSTANCE AND IS THE PART WORTH FIXING: a round number is the least stable identifier this project has, having been renumbered three times in F031 alone, twice by DECISION and once by a repair round displacing the queue. A docstring that must point forward names the DECISION or the feature — both of which are stable by construction — never the round. THE FIX IS TO REPLACE THE ROUND NUMBER WITH DECISION F031 D24's own forward reference to the clarification FORM, in `packages/orchestration/ui_server.py`, which is not in R49's change set and lands at R50.
<<<END FINDINGS49

<<<SLICE LEDGER49
Gate: F031 R48 — the F031 R48 entry. R48 PASSED ON EVERY ONE OF ITS EIGHT GATES, IT TURNED A RED BRANCH TIP GREEN, AND THE REVIEWER RE-RAN EVERY GATE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THE TIP WAS THE POINT OF THE ROUND AND THE REVIEWER MEASURED BOTH SIDES ITSELF: `tests/ui_server/` exits 1 at `20eabead` with 1 failed and 479 passed, and exits 0 at `4f474e19` with 486 passed — 480 once the guard is ruled, plus the six tests R48 added. TRANSPORT HELD IN ITS STRONGEST FORM AVAILABLE TO THIS WORKFLOW for the fifth round running: the C0a blob, the C0b blob and `.agent/last_block.md` read at C8 are byte-identical at sha256 `a36a7280…25606e` over 35632 bytes and 389 lines, with C0a and C0b resolving to the SAME git blob `8432f856`. THE EXTRACTION printed 4 slices, CONTENT 85 and TOTAL 389, so PROSE was 304 against 400 and TOTAL 389 against 490. THE PLAN at C1 is byte-equal to PLANF031R48 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 45. THE THREE APPENDS ARE EXACT: 868456 + 1 + 5671 = 874128 and 874128 + 1 + 4006 = 878135 in the ledger, and 611101 + 1 + 2175 = 613277 in `.agent/decisions.md`; N counted by the worker's own script at 3, 1 and 6; units 355 to 358, 358 to 359 and 1472 to 1478; and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on all three. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^- R-\d+ — ` 257 to 260 with the ADDED ids exactly `R-0697`, `R-0698` and `R-0699`; `^Gate: F\d+ R\d+ — ` 28 to 29 with the ADDED key exactly `F031 R47`; `^Done: R-\d+ — ` 6, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; all ids DISTINCT with the maximum `R-0699`; open set 251 to 254; `^## DECISION F031 D\d+ ` 24 to 25. THE FOUR CODE COMMITS WERE READ LINE BY LINE AND EACH IS FAITHFUL TO ITS SPEC: C5 `891d06f5` adds exactly the two ruled import entries, each carrying an `F031 D24` comment and each in the set's existing alphabetical slot, with `DOOR_METHODS` and `FORBIDDEN_MODULES` untouched; C6 `7286e161` adds six tests at 188 insertions, split across the two files by the boundary their own docstrings draw — four pinning what the door ANSWERS and two pinning the EFFECT; C7 `e2e85ce1` mirrors the door's two `fp:` conditions in `_answerable_by_decision_resolve`, rewrites the docstring sentence that claimed `task_decision` was the whole set, states in one sentence why reading the ID PREFIX is not the `type` branch that docstring forbids, moves `ANSWERABLE_DECISION_TYPES` to `("flight_plan_approval", "task_decision")` with a comment naming D24 and the fixture state it rests on, and adds `test_an_approved_flight_plan_card_is_not_answerable` for the resolved case; and C8 `f42970ad` adds the browser proof in that file's own `toEqual` idiom, asserting two `option` answers valued `approve` then `reject`, each `posts: true`. THE RED CONTROLS DISCRIMINATE AND THE REVIEWER RE-RAN ONE OF THEM ITSELF in a disposable worktree rather than accepting the report: deleting the `fp:` branch from `_answerable_by_decision_resolve` turns `tests/orchestration/test_decision_inbox.py` RED at a REAL exit code of 1, naming `test_answerable_key_matches_what_the_write_door_accepts[flight_plan_approval]`, exactly the test the handback named; the worktree was removed and `git worktree list` returned to 1 line. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT, every one at REAL exit 0: canary 42, `tests/ui_server/` 486, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/ui_contracts/` 561 passed with 4 skipped, `tests/orchestration/test_decision_inbox.py` 35, `tests/orchestration/test_bundled_clarification.py` 38, `tests/cli/test_decision_answers.py` 29 and `tests/cli/test_plan_approval.py` 27 — the last four unmoved, which is what proves S7 changed no CLI semantics. THE BROWSER SIDE IS GREEN AT BOTH REAL EXIT CODES: `npx tsc --noEmit` 0 and `npx vitest run` 0 at 30 files and 455 tests, one more than the 454 at `20eabead`. THE PATH SET IS EXACT IN BOTH DIRECTIONS at 11 paths over `20eabead`..`4f474e19`, both residues EMPTY, and every commit is single-parent and far under 500. THE ONE ERRATUM IS THE REVIEWER'S OWN AND COST NOTHING: R48's constraint 10 named "S1 and S6" where S7 was meant, S6 being the docstring sentence and S7 the tuple; the worker read it as S1 and S7, which is the only reading the SPEC supports, said so plainly, and weakened nothing. THREE FINDINGS ARE REGISTERED AGAINST THIS ROUND AS R-0700, R-0701 and R-0702, and none is a block condition: an undeclared handback overage, a byte-identical duplicated test helper the worker itself declared, and a stale round number in a docstring the reviewer's own earlier block ordered. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. R48 finished what R47 started, and the flight-plan approval is now answerable from the inbox end to end.
<<<END LEDGER49
