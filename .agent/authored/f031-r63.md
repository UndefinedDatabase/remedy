STEP CODE ROUND / F031 — ROUND R63
Goal:        Record the R62 verdict, then land the FORM RULE half of the
             clarification form: ONE NEW PURE MODULE under `apps/ui/src/api/`
             that names a clarification field's key and collects one decision's
             field values into the map `answerDecisionCard` has accepted since
             R61, together with its own vitest file. NO COMPONENT, NO STYLESHEET
             AND NO FILE UNDER `tests/` CHANGES THIS ROUND. The markup half that
             calls the module is the NEXT round and is not started here.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R62 gate entry · C3 the form-rule module and its vitest
             file · C4 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r63.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/api/decisionClarificationForm.ts` (NEW),
             `apps/ui/src/api/decisionClarificationForm.test.ts` (NEW),
             `.agent/handoff.md`. NOTHING under `apps/ui/src/components/`,
             nothing under `tests/`, `packages/` or `docs/`, and no stylesheet.
             `.agent/decisions.md` is not in it either.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R62. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER63 carries the R62 gate entry
    and nothing else. NO FINDING IS RESOLVED AND NONE IS REGISTERED.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 43 to 44
    with the ADDED key exactly `F031 R62`. `^- R-\d+ — ` stays 268,
    `^Done: R-\d+ — ` stays 16, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 252 before C2 and 252 after C2.
 6. THE TWO PRODUCTION FILES ARE NEW AND NO EXISTING FILE IS EDITED AT C3. You
    add no import to any component, you change no call site, and
    `apps/ui/src/components/panels/DecisionInboxCard.tsx` is BYTE-IDENTICAL at
    the end of this round. The new module is reachable only from its own test
    until the markup half lands, and that is ordered, not an oversight — say so
    in the handback rather than wiring a caller to make it look used.
 7. THE MODULE DUPLICATES NO RULE THAT ALREADY HAS AN OWNER. It does NOT trim a
    value, does NOT drop a blank one, does NOT omit an empty map and does NOT
    substitute a default answer. `decisionAnswer.ts`'s `clarificationAnswersArg`
    already trims, drops blanks and omits the `answers` key, and the server's
    `_validated_clarification_answers` reads an ABSENT `answers` as "accept
    every default" (DECISION F031 D24). A SECOND OWNER OF THOSE RULES IS THE
    DEFECT, not the safety. Read both of those files before you write S1.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 9. DESTRUCTIVE WORK IS ISOLATED AND THE WORKTREE HAS NO `node_modules`. The red
    control of G8 runs ONLY inside a disposable git worktree under `.remedy-wt/`
    and never in the primary checkout. A worktree vitest run over the WHOLE
    suite is RED AT BASE: `apps/ui/node_modules` does not exist there, so
    `react/jsx-dev-runtime` cannot resolve for the one test that reaches a
    `.tsx`, and the reviewer measured that red itself. SCOPE every worktree
    vitest run to `src/api/` and pass the PRIMARY checkout's config, running the
    command from the PRIMARY's `apps/ui` directory:
    `npx vitest run src/api/ --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts`.
    Remove the worktree and prune before C4.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.

Spec — C3 ships these two NEW files and edits nothing:
 S1. `apps/ui/src/api/decisionClarificationForm.ts`, opening with a header
     comment in the idiom of its neighbours in that directory. It names WHAT the
     module is — the field-key and collection rules of the clarification form —
     and WHY the rules live here rather than in the card: DECISION F031 D5,
     because the shipped vitest config collects `src/**/*.test.ts` only and this
     repository has no DOM harness, so a rule written inside
     `DecisionInboxCard.tsx` would ship untested. It also writes down the
     deliberate absences constraint 7 names, in the "Remedy deliberately does
     NOT ..." form this repository uses, so a reader searching this file for the
     trimming rule finds the sentence that sends them to its real owner.
 S2. `export function decisionClarificationFieldKey(decisionIndex: number,
     decisionId: string, questionId: string): string`. It pairs the decision's
     POSITION with its id and then with the question's id, for the reason
     `decisionAnswerKey` in the card already pairs position with id: two cards
     may carry one id, and a key built from the id alone would let one card's
     field hold another card's answer. Carry that reason as its WHY comment.
 S3. `export function collectDecisionClarificationAnswers(...)`, answering
     `Record<string, string>`. It takes the flat store of field values, the
     decision's POSITION, and the decision itself, and answers ONE ENTRY PER
     CLARIFICATION the decision carries, keyed by that clarification's OWN id
     and valued by the text stored under the S2 key for it, or the EMPTY STRING
     when no field was touched. A decision carrying no clarification collects an
     empty object. IT READS NO KEY IT DID NOT COMPUTE, so a value stored under a
     DIFFERENT decision's field key can never reach the map. It answers the
     stored text RAW, per constraint 7. Type the decision parameter so that it
     accepts a `DecisionCardModel` and names only the fields it reads.
 S4. `apps/ui/src/api/decisionClarificationForm.test.ts`, in the idiom of the
     api tests beside it. Cover each of these as its OWN case: the key pairs all
     three parts; two decisions sharing one id get DIFFERENT keys for the same
     question; the collector keys the map by the QUESTION id and not by the
     field key; an untouched field collects the empty string; a decision with no
     clarification collects an empty object; a value stored under another
     decision's field key does not leak in; and a value with surrounding
     whitespace is carried UNTRIMMED. STATE IN THE HANDBACK HOW MANY CASES YOU
     ADDED — G7 compares that number against the suite's own rise.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C3 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob. Report also whether any
     line of the block as saved is a run of a single repeated character, which
     must come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS:
     the saved copy, its mirror and the working copy, all three your own output,
     and NOT the bytes that were emitted to you. §3 item 37 is why.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, each slice's own line count, the CONTENT line total, the
     TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE PROSE.
     PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R63 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER63. The reviewer measured the base blob at `4cb80429`
     itself: `.agent/live_review.md` is 965756 bytes over 391 blank-line units.
     If it reads differently before C2, something moved that this round did not
     order — stop and hand back. Report both byte counts and the sum. Then
     confirm with a SECOND, independent reader, as §3 item 36 requires: split
     the whole file on blank lines, let N be the number of paragraphs YOUR
     SCRIPT COUNTS in that slice — never a number this block asserts — and
     compare the LAST N units of the file against the slice's N paragraphs IN
     ORDER. Report N and the unit count before and after. THE NEGATIVE CONTROL
     GOES ON THE FIRST APPENDED PARAGRAPH: flip ONE byte IN MEMORY inside
     paragraph 1 and report that BOTH readers REJECT it. Never mutate the
     tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id. Every movement constraint 5 names is
     checked here, INCLUDING the ones that must NOT move. Report the open set at
     both points.
 G6. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only 4cb80429..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat 4cb80429..C3` restricted to
     `packages/`, `tests/`, `docs/` and `apps/ui/src/components/` and confirm
     each is EMPTY — `docs/` WHOLE, not only its subtrees, because this round
     touches no documentation at all. Report `git diff 4cb80429..C3 --
     apps/ui/src/components/panels/DecisionInboxCard.tsx` EMPTY, which is
     constraint 6's byte-identical claim. Line-anchored `^<<<SLICE ` and
     `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1, in `.agent/live_review.md`
     at C2 and in BOTH new files at C3, against a CONTROL count over the C0a
     blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 lines, `git worktree list`
     as 1 line, and `git ls-files --others --exclude-standard` as 0 lines at C3.
 G7. THE TYPES, THE SUITE, THE GUARDS AND THE STATE READERS, ALL IN THE PRIMARY
     CHECKOUT AT C3, each a REAL exit code. From `apps/ui`: `npx tsc --noEmit`,
     which must be 0. From `apps/ui`: `npx vitest run`, which must be 0 —
     report its FILE count and its TEST count, and confirm the rise over the
     base EQUALS the number of cases S4 says you added; at `4cb80429` the
     reviewer measured 30 files and 481 tests itself. Then, run SERIALLY and
     never two pytest processes alive at once: `pytest tests/ui_contracts/`,
     which the reviewer measured itself at 561 passed and 4 skipped and which
     must be UNMOVED because no file under `tests/` changed; then the canary
     `tests/cli/test_golden_path.py`; then `tests/ui_server/`; then
     `tests/orchestration/test_test_runner.py`; then
     `tests/regression/test_resource_safety.py`; then
     `tests/orchestration/test_integrity_gate.py`. At `4cb80429` the reviewer
     measured those five itself at 42, 489, 52, 21 and 16, every one at exit 0.
     Any movement in any of them is unexplained: stop and hand back.
 G8. THE RED CONTROL, IN A DISPOSABLE WORKTREE ONLY. Add a worktree under
     `.remedy-wt/` at C3 and run the SCOPED command constraint 9 gives. FIRST
     the UNMUTATED control: report its REAL exit code, which must be 0, and its
     file and test counts; at `4cb80429` the reviewer measured that scoped
     control itself at exit 0, 27 files and 456 passed, so it must now read 28
     files and 456 plus the cases S4 added. THEN mutate exactly ONE thing INSIDE
     THE WORKTREE and nothing else: make `collectDecisionClarificationAnswers`
     key its map by the FIELD KEY instead of by the clarification's own id.
     Re-run the SAME scoped command and report its REAL exit code, which must be
     NON-ZERO. Then name which of YOUR OWN cases changed colour under that
     mutation and which survived it, and say for each survivor WHY it survives —
     a case that cannot see this mutation is not a defect, but reporting it as
     if it had failed would be. Finally remove the worktree and prune, and
     report `git worktree list` as 1 line and `git status --porcelain` as 0
     lines in the PRIMARY checkout.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G6's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE
             for G1 through G8 with its real exit code, the open-findings count
             AFTER this round, and the next expected action. AGENTS.md gives the
             handback 60 lines at most, or 100 when per-commit tables of MORE
             THAN FIVE commits require it; COUNT THE COMMITS THE BUNDLE ORDERS
             AND DERIVE YOUR CAP YOURSELF, then write NO BLANK LINE between a
             `###` commit heading and its table, none between a `##` heading and
             its first line, and none between one commit block and the next.
             Declare DECISION D15 only if the MANDATED content still does not
             fit in that shape, and if you do, name what actually caused it. SAY
             PLAINLY THAT NO FILE OUTSIDE `.agent/` AND `apps/ui/src/api/`
             CHANGED, THAT NO FINDING MOVED IN EITHER DIRECTION, THAT THE OPEN
             COUNT IS UNCHANGED AT THE NUMBER G5 MEASURED, AND THAT THE NEW
             MODULE HAS NO CALLER YET BY ORDER OF CONSTRAINT 6. Name the next
             expected action as the MARKUP half — the card holding a field per
             open clarification, keying each by `decisionClarificationFieldKey`,
             collecting with `collectDecisionClarificationAnswers` and passing
             the map to `answerDecisionCard`, with
             `tests/ui_contracts/test_decision_answer_wiring.py` moving with the
             call string it pins and the stylesheet gaining the field rules.
             Give it NO round number: §3 item 35 forbids numbering a round that
             has not begun. Then push with
             `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R63
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1-D26.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R63 records the R62 verdict and lands the FORM RULE half of the clarification
form: one new pure module under `apps/ui/src/api/` names a field's key and
collects one decision's field values into the map the flow has accepted since
R61, with its own vitest file. No component, no stylesheet and no file under
`tests/` changes, and no finding moves in either direction.

## Next Steps
1. The MARKUP half: the card holds a field per open clarification, keys each by
   `decisionClarificationFieldKey`, collects them with
   `collectDecisionClarificationAnswers` and passes the map to
   `answerDecisionCard`. `tests/ui_contracts/test_decision_answer_wiring.py`
   pins the card's call string, so that round moves the guard with the call it
   pins, and the stylesheet gains the field rules.
2. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE RULE LANDS ONE ROUND BEFORE ITS ONLY CALLER. The module is reachable from
  its own vitest file alone until the markup half lands; that is ordered, and
  DECISION F031 D5 is why the rule is not written inside the card instead.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- A WORKTREE VITEST RUN OVER THE WHOLE SUITE IS RED AT BASE. A worktree carries
  no `apps/ui/node_modules`, so `react/jsx-dev-runtime` cannot resolve for the
  one test that reaches a `.tsx`; every worktree run is scoped to `src/api/`
  and passes the primary checkout's config.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `4cb80429`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R63

<<<SLICE LEDGER63
Gate: F031 R62 — the F031 R62 entry. R62 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS A RECORD ROUND AND THE LAST OF ITS SESSION: NO FILE OUTSIDE `.agent/` CHANGED, no production code, no `docs/` file and no decision entry, no finding was resolved and none minted, and the open set is 252 at both points. THE TRANSPORT PROOF COVERS THE SAVED COPY, ITS MIRROR AND THE WORKING COPY AND NOT THE EMITTED BYTES, per §3 item 37: sha256 `13557d48…72a53a6a` over 18240 bytes and 198 lines, C0a and C0b the SAME git blob `471a17b5ed46`, the working copy matching both, and no line of the block a run of one repeated character. THE EXTRACTION printed 2 slices at 46 and 1 content lines with CONTENT 47 and TOTAL 198, so PROSE 151 against 400 and TOTAL 198 against 490. THE PLAN at `676c4ab1` is byte-equal to PLANF031R62 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 46. THE APPEND IS EXACT: 960745 + 1 + 5010 = 965756 and the committed blob is 965756; N counted by the reviewer's own script is 1, units 390 to 391, the last unit matches the slice's one paragraph, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^Gate: F\d+ R\d+ — ` 42 to 43 with the ADDED key exactly `F031 R61`, and `^- R-\d+ — ` 268, `^Done: R-\d+ — ` 16, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 every one UNMOVED, all ids DISTINCT and the maximum id `R-0707`. NOTHING ELSE MOVED: both path residues EMPTY over the four-path change set, `apps/`, `packages/`, `tests/` and `docs/` — the last WHOLE — each EMPTY in the range, markers 0 and 0 in the plan and the ledger against a CONTROL of 2 and 2, insertions 198, 115, 13 and 2 with each commit single-parent and under 500, and `git ls-files .remedy-wt` 0 lines, `git worktree list` 1 line and `git ls-files --others --exclude-standard` 0 lines. THE STATE READERS THE REVIEWER RE-RAN ITSELF, serially and every one a REAL exit code 0: the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16, every count EQUAL to the base reading at `81a9fad6`, and nothing moved. THE HANDBACK COMMIT'S OWN NUMBERS, WHICH §3 ITEM 31 ROUTES HERE: `4cb80429` adds 30 lines and removes 74 in `.agent/handoff.md`, and that handoff is 52 lines against the 60 a five-commit bundle earns, so NO DECISION D15 DECLARATION WAS MADE OR NEEDED — the second handback running to fit its tier without one, and the repair R-0582 asked for is holding. THE HANDBACK'S PER-COMMIT TABLE AGREES CELL FOR CELL with `git diff --numstat`, and the four SESSION SHAs it names resolve to real verdict commits `816ef101`, `798a75a0`, `a2d7250f` and `17b31a36`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER63
