── STEP T003 guard-reach repair / F031 — ROUND R40 ────────────────────
Goal:        Register the two findings the R39 gate raised and fix both. Neither
             is a product defect: the card is correct as it stands. Both are
             GUARD-REACH defects — an assertion whose NAME claims a property its
             predicate does not reach — and the reviewer proved each by mutating
             the shipped component in a disposable worktree and watching the
             whole contract suite stay green.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the two findings, in their own commit · C3 the R39 gate entry
             · C4 the guard repair · C5 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r40.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. NO FILE UNDER `apps/` — this round changes no
             production code, and a single path under `apps/` is a block
             condition, not a deviation. No file under `docs/`, `packages/` or
             `apps/cli/`, and no other file under `tests/`.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, STOP and say so in the handback
    instead of correcting it — a corrected slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. The findings land
    at C2 BEFORE any fix, so a session that dies mid-round still leaves the
    record complete. C3 and C4 may not be reordered around it.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R39. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 4. THE TEST CHANGE IS DESCRIBED, NOT SLICED. S1 through S3 fix the properties;
    you write the Python under AGENTS.md's self-review loop and choose the exact
    strings. G7 requires you to PROVE each new assertion can fail.
 5. THE TWO FINDINGS ARE THE REVIEWER'S TEXT. You never write a `Done:`
    paragraph and never edit a finding's wording. When a fix lands, the record
    of it is this round's handback and the NEXT gate's entry, not a resolution
    you author.
 6. THE COMPONENT IS NOT EDITED TO SUIT THE GUARD. If an assertion you write
    cannot reach a property without reshaping `DecisionInboxCard.tsx`, STOP and
    say so in the handback. The component passed its gate; the guard is what is
    short here, and widening the change set to make a test easier is a silent
    scope change and a block condition.
 7. THE LEDGER SETS MOVE TWICE, AND ONLY AS STATED. Across C2 `^- R-\d+ — `
    moves 249 to 251, the ids ADDED are exactly `R-0689` and `R-0690`, the ids
    REMOVED are EMPTY, and all ids stay DISTINCT. Across C3
    `^Gate: F\d+ R\d+ — ` moves 20 to 21 with the ADDED key exactly `F031 R39`.
    Across BOTH, `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 244 before C2 and 246 after.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
 9. SCRATCH LIVES UNDER `.remedy-wt/` and is removed BY ITS EXACT PATH, never
    by a glob. Nothing under `.remedy-wt/` is ever committed.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, and every form of environment assignment. Route anything
    that counts, hashes or compares through `python3 - <<'PY'`, read real exit
    codes from `subprocess.run(...).returncode`, and copy with
    `shutil.copyfile`. Keep each heredoc modest in size — a very long one is
    rejected by the parser outright.

Spec — the guard repair, all of it inside
`tests/ui_contracts/test_decision_answer_wiring.py`:
 S1. PIN THE HELPER BODIES, WHERE "ONLY ITS OWN" IS ACTUALLY IMPLEMENTED
     (R-0689). Today every assertion about the in-flight set reads CALL SITES.
     Add assertions that read the BODY of `withAnswerKey` and the BODY of
     `withoutAnswerKey` out of comment-stripped source — extract each body, do
     not sweep the whole file, or a match anywhere else would satisfy them.
     Each body must be shown to COPY before it changes (`new Set(sending)`), to
     touch ONLY the passed key (`next.add(answerKey)`, `next.delete(answerKey)`),
     and to contain NO bulk operation — `.clear(` is the one the reviewer
     proved, and a body that assigns a fresh empty set instead reaches the same
     defect, so exclude that too.
 S2. PIN THE PROPERTY, NOT THE SPELLING (R-0690). The existing
     `test_the_region_is_never_conditionally_created` forbids the single literal
     `outcome === null ? null :`, which is one spelling of a family. Over
     comment-stripped source, take the region BETWEEN the answer button's
     closing tag and the opening tag of the paragraph carrying
     `aria-live="polite"`, and require it to hold no conditional operator at all
     — `?`, `&&` and `||` are the three that can gate a JSX child. On the
     shipped component that region is whitespace once comments are stripped, so
     the assertion is tight rather than lucky. Keep the existing assertion, and
     RENAME it to say what it really pins — the specific shape R-0686 was
     registered against — so no reader takes its old name for the guarantee S2
     now makes.
 S3. THE GUARDS GROW, NEVER SHRINK. Keep every assertion the file already
     carries; one RENAME is ordered by S2 and no other existing assertion's
     text may change. The file collects 25 at `14fde389` and must collect more
     after C4.

Done when — run every gate yourself and record its REAL exit code. G1 through
G8 run at commits STRICTLY EARLIER than C5, so the handback can quote them; the
push is ordered after C5 and its reading is NOT written into the handback — the
reviewer takes that reading at the next gate.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both
     ABSENT. Report the sha256, byte count and line count of this block as
     saved at C0a, as mirrored at C0b, and as read off disk at C4 — all three
     must be EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. Say explicitly whether your extractor counts the
     `<<<SLICE` and `<<<END` lines as CONTENT or as PROSE — the convention here
     is that MARKERS ARE PROSE, and R39's two readers differed by exactly the
     six marker lines. PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R40 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` strictly under 50.
 G4. THE TWO APPENDS, EACH PROVED SEPARATELY. `.agent/live_review.md` at C2
     equals its pre-commit blob plus ONE newline plus FINDINGS40, and at C3
     equals ITS pre-commit blob plus ONE newline plus LEDGER40 — report both
     byte counts and the sum for EACH; the pre-commit blob for C2 is 809140
     bytes. For EACH, confirm with a SECOND, independent reader: split on blank
     lines, report how the unit count moves from 338, check the last units equal
     that slice's paragraphs IN ORDER, and report the SWAPPED comparison FALSE.
     LEDGER40 IS A SINGLE PARAGRAPH, so its own reversal is the identity and
     that control is degenerate — run the swap CROSS-SLICE against FINDINGS40's
     paragraphs instead and report it FALSE both ways, rather than reporting a
     passing control it cannot be. For EACH, flip ONE byte IN MEMORY and report
     that both readers REJECT it. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report every count constraint 7 names at three points —
     before C2, after C2, after C3 — plus the ids ADDED and REMOVED as sets at
     each step, whether all ids are DISTINCT, and the maximum id. Report the
     open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C3,
     against a CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only 14fde389..C4` and compare it BOTH WAYS against the
     change set above. Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and under 500. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C4.
     Report the reflog for this round's commits: every operation prefix must
     read `commit`, and `amend`, `rebase` and `cherry` must be 0 each.
 G7. THE GUARDS ARE PROVED, NOT ASSERTED. At C4 run, in `apps/ui`,
     `npx tsc --noEmit` (REAL exit 0) and `npx vitest run` (REAL exit 0,
     reporting the file and test counts, which MUST read 30 and 448 exactly as
     they do at `14fde389`, because this round edits nothing they compile), and
     `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q`
     (REAL exit 0, reporting the collected count, which must EXCEED 25). Then,
     in a DISPOSABLE WORKTREE at C4 under `.remedy-wt/r40red` and never in the
     primary checkout, prove EACH NEW assertion can fail. Two of the mutations
     are named for you because the reviewer already ran them at `14fde389` and
     both left the ENTIRE contract suite green — that is what the findings are:
     (a) replace the single occurrence of `next.delete(answerKey);` in
     `withoutAnswerKey` with `next.clear();`, which must now fail an S1
     assertion; (b) wrap the paragraph carrying `aria-live="polite"` in
     `{outcome === null ? undefined : ( ... )}`, leaving the inner ternary in
     place, which must now fail the S2 assertion. Choose your own mutation for
     every other new assertion. For each, before you mutate, count the exact
     bytes you are about to change IN THE FILE you change them in and report the
     count, which must be 1; if it is not 1, choose a longer unique string and
     report that instead. Report WHICH node ids failed and HOW MANY for each,
     restore, and confirm the file is byte-identical to C4 afterwards. A new
     assertion that stays GREEN under its own mutation is a guard that pins
     nothing — declare it plainly rather than adjusting the mutation until it
     goes red. Remove the worktree by its exact path and report
     `git worktree list` back to 1 line.
 G8. THE READERS AND THE CANARY, in the PRIMARY checkout at C4 and SERIALLY —
     never two pytest processes alive at once, which produces false reds. Run
     and report the real exit code and count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/ui_contracts/`, and
     the canary `tests/cli/test_golden_path.py`. At `14fde389` these read 480,
     52, 21, 16, 550 passed with 4 skipped, and 42; `tests/ui_contracts/` MUST
     grow by exactly the increase in G7's collected count for that one file —
     TEST FUNCTIONS, not assertions — and any other movement is a reported
     number, not a silence.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G6, the item-status table covering
             C0a, C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER GATE for
             G1 through G8 with its real exit code, an explicit line for each of
             R-0689 and R-0690 saying what changed, the open-findings count, and
             the next expected action. Derive your line cap from AGENTS.md
             yourself, from the commit count you actually made; if the mandated
             content genuinely does not fit, declare the DECISION D15 overage
             with its stated cause. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R40
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D18.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R40 registers the two findings the R39 gate raised and fixes both. Neither is a
product defect — the card is correct as it stands — and both are guard-reach
defects the reviewer proved by mutating the shipped component and watching the
whole contract suite stay green. The round also records R39's PASS.

## Next Steps
1. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
2. The integration-gate round per `docs/agents/integration_gate.md`, whose block
   also carries the checklist items R-0683, R-0377, R-0419, R-0429, R-0560,
   R-0582, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NO DOM HARNESS REACHES THE INBOX MARKUP, and it is now the source of a second
  round of findings. The shipped vitest config collects `src/**/*.test.ts`, so
  the wiring is gated by comment-stripped SOURCE reading and by `tsc --noEmit`,
  never by a rendered click. R-0686 and R-0687 got past R38 that way; R-0689 and
  R-0690 are the same blindness one level down, in the guards written to close
  them.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 244 at
  `14fde389` and this round takes it to 246.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685, R-0689 and R-0690; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R40

<<<SLICE FINDINGS40
- R-0689 — Medium, A SETTLE GUARD THAT READS ONLY THE CALL SITE LEAVES THE FUNCTION THAT IMPLEMENTS "ONLY ITS OWN" ENTIRELY UNPINNED. Raised by the reviewer at the R39 gate against `tests/ui_contracts/test_decision_answer_wiring.py` as committed at `f93e1008`. THE MEASUREMENT, run by the reviewer in a disposable worktree at `14fde389` and never in the primary checkout: replacing the single occurrence of `next.delete(answerKey);` in `withoutAnswerKey` with `next.clear();` — one word — makes a settled send clear EVERY in-flight key, which reinstates R-0687 exactly as it was registered, and `python3 -m pytest tests/ui_contracts/ -q` stayed at REAL exit 0 with 549 passed and 5 skipped, the guard file's own 25 among them. The assertion named for this property, `test_a_press_removes_only_its_own_key_when_it_settles`, requires the literal call `setSendingKeys((sofar) => withoutAnswerKey(sofar, answerKey))`, and the mutation does not touch that line; no assertion in the file reads either helper's BODY, and the bodies are where "only its own" is actually implemented. THE WORKER IS NOT AT FAULT AND ITS RED PROOF IS CORRECT AS RUN: G7 of the R39 block ordered a revert of "the ONE specific change that assertion pins", the call site IS what that assertion pins, and R5 of the worker's proof reverted exactly that and went red. THE DEFECT IS THE GUARD'S REACH, NOT THE PROOF — and it is the general shape this repository keeps meeting, a gate on the SHAPE that cannot fail on a false sentence. THE FIX: assert over each helper's extracted BODY that it copies before it changes, that it touches only the passed key, and that it carries no bulk operation.

- R-0690 — Low, AN ASSERTION NAMED "NEVER CONDITIONALLY CREATED" FORBIDS ONE SPELLING OF CONDITIONAL CREATION. Raised by the reviewer at the R39 gate against `tests/ui_contracts/test_decision_answer_wiring.py` as committed at `f93e1008`. THE MEASUREMENT, same disposable worktree at `14fde389`: wrapping the paragraph that carries `aria-live="polite"` in `{outcome === null ? undefined : ( ... )}` while leaving the inner `{outcome === null ? "" : outcome.sentence}` in place reinstates R-0686 — the region is once again created together with its first sentence — and the guard file stayed at REAL exit 0 with all 25 passing. `test_the_region_is_never_conditionally_created` forbids the literal `outcome === null ? null :` alone, and `undefined` is not `null`. THE SEVERITY IS LOW ON PURPOSE AND THE REASON IS PART OF THE FINDING: the surviving mutation is contrived, since it leaves a now-dead inner ternary no refactorer would write, and the NATURAL regressions are all caught — `{outcome && (<p ...>{outcome.sentence}</p>)}` drops the inner ternary and fails the sibling assertion at once. What is wrong is narrower than "the guard is broken": the assertion's NAME and docstring claim the whole family while its predicate holds one member of it, and a name that overclaims is how a later reader stops looking. THE FIX: pin the property — over comment-stripped source, the region between the answer button's closing tag and the paragraph's opening tag holds no conditional operator — and rename the surviving literal check to say the single shape it really pins.
<<<END FINDINGS40

<<<SLICE LEDGER40
Gate: F031 R39 — the F031 R39 entry. R39 PASSED ON EVERY ONE OF ITS EIGHT GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, including all seven per-commit insertion counts, every cell of its `## Commits` table and all eight suite counts. THIS IS THE ROUND THAT MADE THE ANSWER OUTCOME REALLY ANNOUNCED: the paragraph carrying `aria-live="polite"` is now rendered from a decision row's FIRST render with an empty sentence and only its TEXT is conditional, its empty state collapsed by `.decisionOutcomeQuiet { position: absolute; }` with a CSS WHY comment naming `display: none`, `visibility: hidden` and the `hidden` attribute as the three mechanisms excluded because each removes the node from the accessibility tree; `sendingKey: string | null` became `sendingKeys: ReadonlySet<string>` with exactly two writers, so a press adds and a settle removes ONLY its own key and `disabled={sendingKeys.has(answerKey)}` reads its own key alone; and `decisionAnswerFlow.ts`'s header now names `DecisionInboxCard.tsx` instead of a round number, at +1/-1. TRANSPORT HELD for the eleventh round running: the C0a blob, the C0b blob and both working copies read off disk are ALL FOUR byte-identical at sha256 `0fa1108a24dffcaea736a42474feaafba2d74871f910b0b8e1ecb5a94b99cad9` over 25411 bytes and 234 lines, C0a and C0b resolving to the SAME git blob `5754c75c`. THE CAPS HELD UNDER BOTH READINGS, AND THE ONE NUMBER THE TWO READERS DISAGREED ON IS RECORDED HERE SO IT STOPS RECURRING: the handback reports 3 slices, TOTAL 234, CONTENT 54, PROSE 180, while the reviewer's own extractor read CONTENT 60 and PROSE 174 — the difference is exactly the six `<<<SLICE`/`<<<END` marker lines, the convention in this repository is that MARKERS ARE PROSE, so 54 and 180 stand, and 234 <= 490 and 180 <= 400 hold under either reading. THE PLAN at `403ff14f` equals PLANF031R39 exactly at 2807 bytes and 48 lines, minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1. THE TWO APPENDS ARE EXACT: 798884 + 1 + 5435 = 804320 against an actual 804320, and 804320 + 1 + 4819 = 809140 against an actual 809140, each pre-commit blob a byte-exact prefix, blank-line units 334 to 337 to 338 with the last units equal to each slice's paragraphs IN ORDER and the swaps FALSE. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 246 to 249 to 249 with ADDED across C2 exactly {`R-0686`, `R-0687`, `R-0688`}, ADDED across C3 EMPTY, REMOVED EMPTY at both, all 249 DISTINCT, maximum `R-0688`; `^Done: R-\d+ — ` 5 throughout, `^Landed: R-` 0 throughout, `^Gate: R\d+ — ` 19 throughout, `^Gate: F\d+ R\d+ — ` 19 to 19 to 20 with the ADDED key exactly `F031 R38`; open set 241 before C2 and 244 after C3. MARKERS 0 and 0 in the plan at `403ff14f` and the ledger at `f71893d8` against a live CONTROL of 3 and 3. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 9 paths, nothing under `docs/`, `packages/` or `apps/cli/`, one path under `tests/` and one under `apps/ui/src/api/`. THE SEVEN COMMITS ARE EACH SINGLE-PARENT at insertions 234, 153, 12, 6, 2, 170 and 45, each under the 500 DECISION F104 D1 counts; the reflog reads `commit` in every prefix, so `amend`, `rebase` and `cherry` are 0 each; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE GATES THE REVIEWER RE-RAN: `npx tsc --noEmit` REAL exit 0 with no diagnostic, `npx vitest run` REAL exit 0 at 30 files and 448 tests IDENTICAL to base, and the six Python suites SERIALLY at 480, 52, 21, 16, 550 passed with 4 skipped, and canary 42 — `tests/ui_contracts/` moving 541 to 550, which is EXACTLY the 9 test functions the guard file gained, 16 to 25, the 16 confirmed by collecting that file in a worktree at `279cd819`. THE ONE DEVIATION THE WORKER DECLARED IS ACCEPTED AND IS NOT A BLOCK CONDITION: S5 said "keep every assertion the file already carries" while S3 ordered the very expression `test_the_buttons_are_not_unconditionally_disabled` quoted, so the two could not both be met on that line; the worker kept the assertion's PROPERTY over the new shape, deleted nothing, grew the file 16 to 25, and flagged the conflict rather than resolving it silently — which is the shape this workflow wants. THE REVIEWER THEN RAN THREE MUTATIONS THE BLOCK NEVER ORDERED, and two of them survived, which is where this round's findings come from. The one that discriminated: turning `.decisionOutcomeQuiet` into `display: none` failed exactly `test_the_empty_region_is_collapsed_out_of_flow` and `test_the_outcome_rules_never_use_a_mechanism_that_removes_the_node` at REAL exit 1, 2 failed and 23 passed. The two that survived are registered as R-0689, where `next.delete(answerKey)` becoming `next.clear()` reinstates R-0687 with the WHOLE contract suite green, and R-0690, where the live region can be conditionally created again through `undefined` with all 25 guards green. NEITHER IS A PRODUCT DEFECT — the shipped card is correct — and neither is a block condition: no fabricated value, no false live indicator, no missing table, no unverified claim, no silent scope change. R39 shipped a real fix for all three of R38's findings and its guards were merely shorter than their own names; R40 lengthens them.
<<<END LEDGER40
