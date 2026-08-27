STEP CODE ROUND / F031 — ROUND R64
Goal:        Record the R63 verdict, then land the MARKUP half of the
             clarification form: the card holds a field per open clarification,
             keys each one with `decisionClarificationFieldKey`, collects them
             with `collectDecisionClarificationAnswers` and passes the map to
             `answerDecisionCard`, which has accepted it since R61 and which no
             caller has filled until now. The stylesheet gains the field rules
             and the contract guard moves with the call string it pins.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R63 gate entry · C3 the stylesheet rules · C4 the card and
             the guard that pins it · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r64.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `apps/ui/src/components/panels/RightLivePanel.module.css`,
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. NOTHING under `apps/ui/src/api/` — the two
             modules R63 landed are used AS THEY ARE and neither is edited.
             Nothing under `packages/` or `docs/`, and no test file under
             `tests/` other than the one named. `.agent/decisions.md` is not in
             it either.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. No pair may be
    reordered and none may be merged. C3 lands the stylesheet BEFORE the markup
    that names its classes, so no commit in this round renders an unstyled
    field.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R63. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER64 carries the R63 gate entry
    and nothing else. NO FINDING IS RESOLVED AND NONE IS REGISTERED.
 5. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 44 to 45
    with the ADDED key exactly `F031 R63`. `^- R-\d+ — ` stays 268,
    `^Done: R-\d+ — ` stays 16, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19. The open set is 252 before C2 and 252 after C2.
 6. THE DEFAULT IS SHOWN AND NEVER SENT. A field starts EMPTY. A question's
    `defaultAnswer` is rendered as VISIBLE TEXT beside the field and never
    becomes the input's value, because the server's
    `_validated_clarification_answers` reads a blank or absent answer as "accept
    this question's default" (DECISION F031 D24) — so an untouched form must
    post nothing for that question, and prefilling the default would post the
    default as though the operator had typed it. This is the round's central
    rule and G8 is the proof of it.
 7. THE CARD ADDS NO RULE THAT ALREADY HAS AN OWNER. It does not trim a value,
    does not drop a blank one, does not build the `answers` key and does not
    decide what an empty map means. `collectDecisionClarificationAnswers` owns
    the collection, `decisionAnswer.ts`'s `clarificationAnswersArg` owns the
    trimming and the omission. Read `apps/ui/src/api/decisionClarificationForm.ts`
    in full before you write S2 — its header names every absence you must not
    fill in here.
 8. THE EXISTING GUARDS STAY GREEN AND YOU DO NOT WEAKEN ONE TO PASS. In
    particular `tests/ui_contracts/test_decision_answer_wiring.py` reads the
    region between the LAST `</button>` before the LAST `aria-live="polite"` and
    rejects `?`, `&&` and `||` anywhere in it (finding R-0690), and it forbids
    the substrings `decision.status` and `switch (` anywhere in the
    comment-stripped card (DECISION F031 D5). THE FIELD BLOCK THEREFORE GOES
    ABOVE THE ANSWER STRIP, between the chips row and
    `<div className={styles.decisionAnswers}>`, and adds NO `aria-live`. Deleting
    or loosening any assertion in that file other than the ONE call string S5
    moves is a block condition, not a repair.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
10. DESTRUCTIVE WORK IS ISOLATED. G8's mutation runs ONLY inside a disposable
    git worktree under `.remedy-wt/` and never in the primary checkout. pytest
    runs there directly with the worktree as `cwd`; the reviewer measured that
    itself at base, where the guard file alone is exit 0 at 36 passed. Remove
    the worktree and prune before C5.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.

Spec — C3 is S1, C4 is S2 through S5:
 S1. `RightLivePanel.module.css` gains the field rules, written in the idiom of
     the `.decision*` rules already there and using this repository's own tokens
     rather than invented values — `docs/ui/design_reference/` is binding for
     this feature. Each selector sits ALONE on its line and its rule is a single
     block, because the guard's `css_rule_body` reader matches the last line of
     the text before `{` against the selector exactly. Add exactly these, and no
     other rule: `.decisionClarifications` (the block that holds the fields),
     `.decisionClarification` (one question's group), `.decisionClarificationQuestion`
     (the label), `.decisionClarificationInput` (the text input, which carries a
     `:focus-visible` rule in the same shape `.decisionFilterChip:focus-visible`
     already uses), and `.decisionClarificationMeta` (the default-and-impact
     line). The input must not restyle itself into a control it is not: no
     `cursor: pointer`.
 S2. `DecisionInboxCard.tsx` imports `decisionClarificationFieldKey` and
     `collectDecisionClarificationAnswers` from `../../api/decisionClarificationForm`
     and holds ONE new piece of state, the flat store of typed text keyed by the
     field key. Its `useState` carries a WHY comment saying that the store is
     flat and holds every card's fields at once, which is exactly why the
     collector iterates a decision's own questions rather than the store.
 S3. Two FIXED AFFORDANCE LABELS are declared as `const` at the top of the file
     beside `DECISION_JUMP_LABEL`, in that same style and each with its own WHY
     comment: one prefixing the shown default, one prefixing the shown impact.
     No other string this file invents may reach the markup — the question text,
     the default and the impact are all FIELDS of the model, exactly as the
     file's header rule requires.
 4b. NOT USED.
 S4. The field block renders inside the `<article>`, ABOVE
     `<div className={styles.decisionAnswers}>`, only when the decision carries
     at least one clarification. For each clarification it renders a `<label>`
     bound to the input by `htmlFor`/`id` carrying the question's own text, a
     text `<input>` whose value is `clarificationValues[fieldKey] ?? ""` and
     whose change handler stores the typed text under the field key WITHOUT
     touching any other key, and the meta line showing the default and the
     impact behind the two S3 labels. THE REACT KEY OF EACH FIELD PAIRS THE
     CLARIFICATION'S POSITION WITH ITS FIELD KEY: the endpoint does not
     guarantee distinct question ids — neither `open_clarification_questions` in
     `packages/orchestration/flight_plan.py` nor `cardClarifications` in
     `decisionCard.ts` deduplicates them — and a key built from the id alone
     would let React reuse one node for two questions. Carry that reason as the
     key's WHY comment, and say in the SAME comment that the collected MAP still
     collapses a duplicate id to one entry, because the write door's contract is
     keyed by question id and this component does not get to change that.
     Collect the map ONCE per decision row, beside `jumpNodeId`, into a `const`
     named `clarificationAnswers`, and pass that const as the FOURTH argument of
     the existing `answerDecisionCard` call. Nothing else in the call changes and
     the two refusal paths, the in-flight set and the outcome region are all
     left exactly as they are.
 S5. `tests/ui_contracts/test_decision_answer_wiring.py` moves with the call it
     pins and grows the guards this markup needs. MOVE the one existing
     assertion that pins `answerDecisionCard(target, decision, answer.value)` to
     the four-argument call string S4 produces, and change no other existing
     assertion. Then ADD, each as its own test and each against the
     COMMENT-STRIPPED source: the card imports both functions from
     `../../api/decisionClarificationForm`; the input's value is read from the
     store under the field key and pins the exact expression S4 names, so a
     fallback to the default cannot be spelled there; the card never uses
     `defaultAnswer` as an input value anywhere; the field block sits BEFORE the
     answer strip, asserted by comparing the source position of the
     clarifications block against that of `styles.decisionAnswers`; and each of
     the five S1 classes the card names has a NON-EMPTY rule body in the
     stylesheet, read with the existing `css_rule_body` helper. STATE IN THE
     HANDBACK HOW MANY TESTS YOU ADDED — G7 compares that number against the
     suite's own rise.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C5, so the handback can quote them; the
push is ordered after C5 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C4 — all three must be EQUAL —
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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R64 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE APPENDED
     REGION. `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE
     newline plus LEDGER64. The reviewer measured the base blob at `3de459cc`
     itself: `.agent/live_review.md` is 968790 bytes over 392 blank-line units.
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
     `git diff --name-only 3de459cc..C4` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C5, outside a range ending at C4 — and report
     both residues EMPTY. Report `git diff --stat 3de459cc..C4` restricted to
     `packages/`, `docs/` and `apps/ui/src/api/` and confirm each is EMPTY —
     `docs/` WHOLE, not only its subtrees. Report `git diff --name-only
     3de459cc..C4 -- tests/` and confirm the ONLY path it prints is
     `tests/ui_contracts/test_decision_answer_wiring.py`. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md` at C1,
     `.agent/live_review.md` at C2 and all three files C3 and C4 touch, against a
     CONTROL count over the C0a blob, which is not 0. Report each commit's
     insertions from `git diff --numstat` for C0a through C4, confirm each is
     single-parent and under 500. Report `git ls-files .remedy-wt` as 0 lines,
     `git worktree list` as 1 line, and `git ls-files --others
     --exclude-standard` as 0 lines at C4.
 G7. THE TYPES, THE SUITE, THE GUARDS AND THE STATE READERS, ALL IN THE PRIMARY
     CHECKOUT AT C4, each a REAL exit code. From `apps/ui`: `npx tsc --noEmit`,
     which must be 0. From `apps/ui`: `npx vitest run`, which must be 0 — report
     its FILE count and its TEST count, which the reviewer measured itself at
     `3de459cc` as 31 files and 488 tests and which must be UNMOVED, because no
     file under `apps/ui/src/api/` changed and no vitest file was added. Then,
     run SERIALLY and never two pytest processes alive at once:
     `pytest tests/ui_contracts/`, reporting passed and skipped — the reviewer
     measured 561 passed and 4 skipped at `3de459cc`, and the rise must EQUAL
     the number of tests S5 says you added, with the skip count UNMOVED at 4;
     then the canary `tests/cli/test_golden_path.py`; then `tests/ui_server/`;
     then `tests/orchestration/test_test_runner.py`; then
     `tests/regression/test_resource_safety.py`; then
     `tests/orchestration/test_integrity_gate.py`. At `3de459cc` the reviewer
     measured those five itself at 42, 489, 52, 21 and 16, every one at exit 0.
     Any movement in any of them is unexplained: stop and hand back.
 G8. THE RED CONTROL, IN A DISPOSABLE WORKTREE ONLY, PROVING CONSTRAINT 6. Add a
     worktree under `.remedy-wt/` at C4. FIRST the UNMUTATED control: run
     `pytest tests/ui_contracts/test_decision_answer_wiring.py` with the
     WORKTREE as `cwd` and report its REAL exit code, which must be 0, and its
     test count; the reviewer measured that same command at base itself at exit
     0 and 36 passed, so it must now read 36 plus the tests S5 added. THEN
     mutate exactly ONE thing INSIDE THE WORKTREE and nothing else: make the
     input's value fall back to the question's `defaultAnswer` instead of the
     empty string, which is precisely the prefill constraint 6 forbids. Re-run
     the SAME command and report its REAL exit code, which must be NON-ZERO.
     Then name which of YOUR OWN tests changed colour under that mutation and
     which survived it, and say for each survivor WHY it survives — a test that
     cannot see this mutation is not a defect, but reporting it as if it had
     failed would be. Finally remove the worktree and prune, and report
     `git worktree list` as 1 line and `git status --porcelain` as 0 lines in
     the PRIMARY checkout.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` ITSELF and
             agreeing cell for cell with G6's readings, the item-status table
             covering C0a, C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER
             GATE for G1 through G8 with its real exit code, the open-findings
             count AFTER this round, and the next expected action. AGENTS.md
             gives the handback 60 lines at most, or 100 when per-commit tables
             of MORE THAN FIVE commits require it; COUNT THE COMMITS THE BUNDLE
             ORDERS AND DERIVE YOUR CAP YOURSELF, then write NO BLANK LINE
             between a `###` commit heading and its table, none between a `##`
             heading and its first line, and none between one commit block and
             the next. Declare DECISION D15 only if the MANDATED content still
             does not fit in that shape, and if you do, name what actually
             caused it. SAY PLAINLY THAT NO FILE UNDER `apps/ui/src/api/`,
             `packages/` OR `docs/` CHANGED, THAT THE ONLY FILE UNDER `tests/`
             THAT CHANGED IS THE ONE GUARD S5 NAMES, THAT NO FINDING MOVED IN
             EITHER DIRECTION, AND THAT THE OPEN COUNT IS UNCHANGED AT THE
             NUMBER G5 MEASURED. Say in ONE sentence that the clarification form
             is now answerable end to end from the card, and name what is still
             NOT reachable so the sentence cannot be read as more than it is.
             Name the next expected action as the integration-gate round per
             `docs/agents/integration_gate.md`, giving it NO round number: §3
             item 35 forbids numbering a round that has not begun. Then push
             with `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R64
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
R64 records the R63 verdict and lands the MARKUP half of the clarification form:
the card holds a field per open clarification, keys each with the R63 module's
key rule, collects them with its collection rule and passes the map to
`answerDecisionCard`. The stylesheet gains the field rules and the contract
guard moves with the call string it pins. No finding moves in either direction.

## Next Steps
1. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT IS SHOWN AND MUST NEVER BE SENT. A blank or absent answer is what
  the server reads as "accept this question's default" (DECISION F031 D24), so
  a prefilled field would post the default as though it had been typed. The
  field starts empty and the default is visible text beside it.
- THE QUESTION IDS ARE NOT GUARANTEED DISTINCT. Neither
  `open_clarification_questions` nor `cardClarifications` deduplicates them, so
  a React key pairs the clarification's POSITION with its field key; the
  collected map still collapses a duplicate to one entry, because the write
  door's contract is keyed by question id.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  R-0693 measures the gap; the rest are outside F031's scope, and the inbox
  tells the truth about every one of them rather than offering a refused button.
- THIS FILE NAMES NO ROUND NUMBER IT HAS NOT BEGUN. Twice a pre-assigned label
  went stale the moment a round was inserted ahead of it; a step is named by
  what it does, and its number is knowable only when it starts.
- A WORKTREE VITEST RUN OVER THE WHOLE SUITE IS RED AT BASE. A worktree carries
  no `apps/ui/node_modules`, so `react/jsx-dev-runtime` cannot resolve for the
  one test that reaches a `.tsx`; every worktree vitest run is scoped to
  `src/api/` and passes the primary checkout's config. pytest in a worktree
  needs no such care and the reviewer measured it green at base.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `3de459cc`
  and this round moves it by nothing.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R64

<<<SLICE LEDGER64
Gate: F031 R63 — the F031 R63 entry. R63 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G8, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk. THIS WAS THE FORM RULE HALF OF THE CLARIFICATION FORM: a NEW pure module `apps/ui/src/api/decisionClarificationForm.ts` carrying `decisionClarificationFieldKey` and `collectDecisionClarificationAnswers`, plus its own vitest file, and NOTHING ELSE — no component, no stylesheet and no file under `tests/`, `packages/` or `docs/` changed, no finding was resolved and none minted, and the open set is 252 at both points. THE TRANSPORT PROOF COVERS THE SAVED COPY, ITS MIRROR AND THE WORKING COPY AND NOT THE EMITTED BYTES, per §3 item 37: sha256 `690f1c19…89ac7fef` over 22366 bytes and 280 lines, C0a and C0b the SAME git blob `d1b8c206f3fa`, the working copy matching both, and no line of the block a run of one repeated character. THE EXTRACTION printed 2 slices at 48 and 1 content lines with CONTENT 49 and TOTAL 280, so PROSE 231 against 400 and TOTAL 280 against 490. THE PLAN at `3273ec11` is byte-equal to PLANF031R63 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48. THE APPEND IS EXACT: 965756 + 1 + 3033 = 968790 and the committed blob is 968790; N counted by the reviewer's own script is 1, units 391 to 392, the last unit matches the slice's one paragraph, and a byte flipped IN MEMORY inside the FIRST appended paragraph is REJECTED by BOTH readers. THE SETS MOVED EXACTLY WHERE CONSTRAINT 5 ALLOWED: `^Gate: F\d+ R\d+ — ` 43 to 44 with the ADDED key exactly `F031 R62`, and `^- R-\d+ — ` 268, `^Done: R-\d+ — ` 16, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 every one UNMOVED, all 268 ids DISTINCT and the maximum id `R-0707`. THE CODE IS WHAT S1 THROUGH S3 DESCRIBED AND NOTHING MORE, read by the reviewer as a diff: the key pairs the decision's position, its id and the question's id; the collector iterates the DECISION'S OWN `clarifications` and never the flat store, keys the map by the clarification's own id, answers the empty string for an untouched field through an `Object.prototype.hasOwnProperty` test rather than a truthiness one, and returns an empty object for a decision carrying none. CONSTRAINT 7 HELD AND THE HEADER PROVES IT WHERE A READER WOULD SEARCH: the module trims nothing, drops no blank, omits no empty map and substitutes no default, and its header names `clarificationAnswersArg` and `_validated_clarification_answers` as the sole owners of those rules under DECISION F031 D24, with DECISION F031 D5 given as the reason the rules are not in the card. CONSTRAINT 6 HELD: `git diff` over the range restricted to `apps/ui/src/components/panels/DecisionInboxCard.tsx` is EMPTY, so the card is byte-identical and the new module has no caller yet BY ORDER. THE TESTS BUILD THEIR MODELS THROUGH THE REAL `buildDecisionCardModel` PROJECTION rather than through hand-written literals, so a case cannot drift from the model the card renders — that is why this colour is evidence and not decoration. THE GATES THE REVIEWER RE-RAN ITSELF, every one a REAL exit code: `npx tsc --noEmit` 0; `npx vitest run` 0 at 31 files and 488 tests, a rise of exactly +1 file and +7 tests over the base 30 and 481 and EQUAL to the worker's own count of the cases it added; and serially `tests/ui_contracts/` 561 passed and 4 skipped UNMOVED, the canary 42, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16, every count EQUAL to the base reading at `4cb80429`. THE RED CONTROL WAS RE-RUN BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, scoped to `src/api/` and with the primary's config named as §3 item 33 requires, because a worktree carries no `apps/ui/node_modules` and an unscoped run is RED AT BASE on `react/jsx-dev-runtime`: the UNMUTATED control is a REAL exit 0 at 28 files and 463 passed, and with `collected[clarification.id]` changed to `collected[fieldKey]` the run is exit 1 at 4 failed and 459 passed. THE FOUR THAT TURNED RED ARE THE FOUR THAT ASSERT THE WHOLE MAP, and the THREE THAT SURVIVED SURVIVE FOR A STATED REASON THE REVIEWER CONFIRMED: two exercise the key function alone and never call the collector, and the third iterates zero clarifications so the mutated assignment never executes — the worker reported all three as survivors WITH those reasons rather than claiming seven reds, which is the correct reading of its own control. The reviewer's worktree was removed and pruned, and `git worktree list` reads 1 line with `git status --porcelain` 0. NOTHING ELSE MOVED: both path residues EMPTY over the six-path change set, `packages/`, `tests/`, `docs/` — the last WHOLE — and `apps/ui/src/components/` each EMPTY in the range, markers 0 and 0 in the plan, the ledger and BOTH new files against a CONTROL of 2 and 2, and insertions 280, 191, 19, 2 and 176 with each commit single-parent and under 500. THE HANDBACK COMMIT'S OWN NUMBERS, WHICH §3 ITEM 31 ROUTES HERE: `3de459cc` adds 36 lines and removes 28 in `.agent/handoff.md`, and that handoff is 60 lines against the 100 a six-commit bundle earns, so NO DECISION D15 DECLARATION WAS MADE OR NEEDED — the third handback running to fit its tier without one. THE HANDBACK'S PER-COMMIT TABLE AGREES CELL FOR CELL with `git diff --numstat`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.
<<<END LEDGER64
