── STEP RECORD ROUND / F031 — ROUND R46 ───────────────────────────────
Goal:        Persist what the R45 gate produced. Register finding R-0696, record
             R45's verdict, land DECISION F031 D23 moving the remaining
             programme by one, and advance the plan. NO CODE CHANGES: this round
             writes only `.agent/` state, because a verdict and a finding that
             live in a session rather than on disk are lost when it ends.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the finding · C3 the R45 gate entry · C4 DECISION F031 D23 ·
             C5 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r46.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `.agent/handoff.md`. NO FILE UNDER `apps/`,
             `packages/`, `tests/` OR `docs/` — R-0696's own repair is R47's
             work and this round deliberately does not start it.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof, and stopping
    early would lose the record this round exists to write.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. The finding lands
    at C2 BEFORE the gate entry at C3. No pair may be reordered. LEDGER46 and
    FINDINGS46 state facts about THIS round's own commits, and this constraint
    is what makes them true on landing.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R45. That is
    ordered: the plan becomes current at C1, the first substantive commit.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph,
    never edit a finding's wording, never edit D23. R-0696 is registered here
    and deliberately NOT FIXED here: its repair deletes a test from
    `tests/ui_contracts/test_decision_answer_wiring.py`, which is not in this
    round's change set.
 5. THE LEDGER SETS MOVE ONCE EACH. Across C2 `^- R-\d+ — ` moves 256 to 257
    with the id ADDED exactly `R-0696` and none REMOVED. Across C3
    `^Gate: F\d+ R\d+ — ` moves 26 to 27 with the ADDED key exactly `F031 R45`.
    Across both, `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 251 before C2 and 252 after.
    `^## DECISION F031 D\d+ ` is 22 before C4 and 23 after.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 7. NOTHING IS VERIFIED BY MUTATION THIS ROUND, because nothing executable
    changes. No `git worktree` is created. `.remedy-wt/f031-r46-block.md` is the
    reviewer's scratch copy — leave it alone, do not delete it. Nothing under
    `.remedy-wt/` is ever committed and `git status --porcelain` reads 0 lines
    at every commit.
 8. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, build dicts with `dict(key=value)`, and
    copy with `shutil.copyfile`. Keep each heredoc modest in size.

Done when — run every gate yourself and record its REAL exit code. G1 through G7
run at commits STRICTLY EARLIER than C5, so the handback can quote them; the
push is ordered after C5 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4. `.agent/STOP` read from disk before C0a and before C5, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C4 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R46 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with `git show <rev>:<path>`
     into memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus FINDINGS46; at C3 equals ITS OWN pre-commit blob plus ONE newline plus
     LEDGER46; `.agent/decisions.md` at C4 equals ITS pre-commit blob plus ONE
     newline plus DECISION23. The pre-commit blob for C2 is 854809 bytes and for
     C4 is 607381 bytes; C3's is whatever C2 left, which you read rather than
     take from this block. For EACH append report both byte counts and the sum.
     Then confirm EACH with a SECOND, independent reader: split the whole file on
     blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in that
     slice — never a number this block asserts — and compare the LAST N units of
     the file against the slice's N paragraphs IN ORDER. Report N and the unit
     count before and after for each. THE NEGATIVE CONTROL GOES ON THE FIRST
     APPENDED PARAGRAPH, which is the position a tail-only reading cannot see:
     flip ONE byte IN MEMORY inside paragraph 1 of each slice and report that
     BOTH readers REJECT it. For any slice whose N is 1, say so and note that
     paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids and
     gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 5 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3. Also report
     `^## DECISION F031 D\d+ ` in `.agent/decisions.md` before and after C4.
 G6. NOTHING EXECUTABLE MOVED, PROVED RATHER THAN ASSERTED. Report
     `git diff --name-only d53bdb9b..C4` and confirm that EVERY path in it
     begins with `.agent/`, listing any that does not.
     Report `git diff --stat d53bdb9b..C4` restricted to `apps/`, `packages/`,
     `tests/` and `docs/` and confirm each of the four is EMPTY. Then, in the
     PRIMARY checkout at C4, run the canary
     `python3 -m pytest tests/cli/test_golden_path.py -q` and the four state
     readers `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py` and
     `tests/orchestration/test_integrity_gate.py`, SERIALLY — never two pytest
     processes alive at once — reporting each REAL exit code and count. At
     `d53bdb9b` these read 42, 480, 52, 21 and 16. These five are ordered
     BECAUSE this round rewrites `.agent/` state and those suites read it; a
     round that touches no code can still turn them red.
 G7. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C3 and
     `.agent/decisions.md` at C4, against a CONTROL count over the C0a blob,
     which is not 0. Compare the path set of G6 BOTH WAYS against this round's
     expected set. Report each commit's insertions from `git diff --numstat`,
     confirm each is single-parent and under 500. Report `git ls-files
     .remedy-wt` as 0 and `git worktree list` as 1 line at C4. Report the reflog
     FOR THIS ROUND'S OWN COMMITS ONLY: every operation prefix must read
     `commit`, and among those entries `amend`, `rebase` and `cherry` must be 0
     each. Do not count those words over the whole reflog, which holds this
     repository's entire history and is not what this gate asks.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G7, the item-status table covering C0a,
             C0b, C1, C2, C3, C4, C5 and the push, ONE LINE PER GATE for G1
             through G7 with its real exit code, an explicit line for R-0696
             saying what was registered and that it was deliberately NOT fixed
             here, the open-findings count, and the next expected action. SAY
             PLAINLY THAT THIS ROUND CHANGED NO EXECUTABLE FILE. THE NEXT ACTION
             SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review this round's handback,
             then R47 — retire the duplicate guard R-0696 names and land the
             `fp:`-prefixed dispatch. Derive your line cap from AGENTS.md
             yourself, from the commit count you actually made; if the mandated
             content genuinely does not fit, declare the DECISION D15 overage
             with its stated cause. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R46
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D23.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R46 is a RECORD ROUND and changes no executable file: it registers R-0696,
records R45's PASS and lands DECISION F031 D23, which moves the rest of the
programme by one. DECISION F031 D19 is now COMPLETE on both sides of the wire —
the endpoint derives answerability and the browser renders a refused answer as
pasteable text rather than as a button the write door would turn away.

## Next Steps
1. R47: retire the duplicate contract guard R-0696 names, then land the
   `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship, reusing
   `flight_plan.resolve_flight_plan_approval`.
2. R48: the clarification FORM over `payload.clarifications`.
3. A reviewer-file round landing the §3 checklist item R-0694, R-0695 and R-0696
   share: a block reads the TARGET — a predicate's refusal conditions, a test
   file's existing guards — before ordering anything against it.
4. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  The inbox no longer CLAIMS they can, which is what D19 bought; R47 is where
  the `fp:` prefix gains a real dispatch. R-0693 measures the gap.
- NO DOM HARNESS REACHES THE INBOX MARKUP, so the component is guarded only by
  comment-stripped SOURCE reading in
  `tests/ui_contracts/test_decision_answer_wiring.py` and by `tsc --noEmit`.
  The R45 gate measured what that buys: a component ignoring `answer.posts`
  leaves `vitest` GREEN at 454 and turns those guards RED, so the guards are
  load-bearing and deleting one silently un-tests the render.
- THREE CONSECUTIVE ROUNDS RAISED A REVIEWER-SPEC DEFECT, not a worker defect —
  R-0694, R-0695 and R-0696 — and all three have one root cause: the block was
  written without reading the thing it ordered against. Step 3 above is the fix.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `d53bdb9b`
  and this round takes it to 252.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R46

<<<SLICE FINDINGS46
- R-0696 — Low, A BLOCK ORDERED A CONTRACT GUARD THE TARGET FILE ALREADY CARRIED, SO THE SUITE GAINED A TEST FUNCTIONALLY IDENTICAL TO ONE SITTING BESIDE IT. Raised by the reviewer at the R45 gate against its OWN R45 block, and reported by the worker before the reviewer reached it. THE MEASUREMENT, read at `9236e617`: `tests/ui_contracts/test_decision_answer_wiring.py` now holds `test_the_region_after_the_button_still_carries_no_conditional_operator` and `test_the_region_is_created_under_no_conditional_operator_at_all`, and the two call the SAME reader `jsx_between_answer_button_and_live_paragraph` over the same comment-stripped source, iterate the same three operators `?`, `&&` and `||`, and make the same assertion; only the failure message differs. THE CAUSE IS IN THE BLOCK, NOT IN THE ROUND: R45's section S item S10 ordered a guard "that the region between the last `</button>` and the outcome `<p` still holds none of `?`, `&&`, `||`" and added "the last one re-uses the reader already in that file" — the reviewer named the READER it had read and never asked whether a TEST already called it, which is the one question that would have settled it. The worker applied S10 as written, because constraint 1 forbids correcting a slice or an item, and said so in its handback rather than silently dropping the item; that is the required behaviour and it is why this costs a duplicate rather than a silent deviation. WHY THIS IS LOW: nothing false landed, no coverage was lost, and `tests/ui_contracts/` is green at 562 passed with 4 skipped. The cost is maintenance and it is real but small — two tests now pin one property, so a later change to the reader or to the forbidden operator set must be made in two places, and a change made in one leaves the pair silently disagreeing about what the file guards. THE FIX IS TO RETIRE THE NEWER TEST AND KEEP THE OLDER, by the same rule §3 item 30 already gives for duplicate finding ids: the older entry is the record, the newer is the duplicate, and both resolutions say which is which. That deletion is in `tests/ui_contracts/test_decision_answer_wiring.py`, which is not in R46's change set, so it lands at R47. THE ROOT CAUSE IS THE THIRD INSTANCE IN THREE ROUNDS AND THAT IS THE PART WORTH FIXING: R-0694 was a fix clause the block never read, R-0695 was a predicate whose refusal conditions the block never read, and this is a test file whose existing guards the block never read. §3 item 6 binds a zero-gate to the TARGET's existing content and item 7 binds an addition to the guards that would make it unsatisfiable; neither reaches an addition the target already SATISFIES, because nothing fails and nothing is unsatisfiable — the block simply asked for something already there. The item those three share is one sentence: before ordering anything against a file, read that file for what it already does.
<<<END FINDINGS46

<<<SLICE LEDGER46
Gate: F031 R45 — the F031 R45 entry. R45 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM AVAILABLE TO THIS WORKFLOW for the third round running: the reviewer's OWN scratch original `.remedy-wt/f031-r45-block.md`, the C0a blob, the C0b blob and `.agent/last_block.md` read off disk at C5 are ALL FOUR byte-identical at sha256 `8ecba3dc5c9448c79a756387d6c4a6e385ffe89c4d94988c4559d03f08f1d847` over 28416 bytes and 338 lines, with C0a and C0b resolving to the SAME git blob `ca19a764`. THE EXTRACTION printed 3 slices, CONTENT 75 and TOTAL 338, so PROSE was 263 against 400 and TOTAL 338 against 490. THE PLAN at `4be48407` is byte-equal to PLANF031R45 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48 — a bound the reviewer's OWN DRY RUN caught at 50 and trimmed to 48 BEFORE emission, the cap being STRICTLY under 50. THE APPENDS ARE EXACT: 849619 + 1 + 5189 = 854809 in the ledger and 605733 + 1 + 1647 = 607381 in `.agent/decisions.md`, blank-line units 350 to 351 and 1455 to 1461, N counted by the reviewer's own script at 1 and 6, both whole-file identities TRUE, and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on both. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED, AND THE ONES THAT MUST NOT MOVE DID NOT: `^- R-\d+ — ` 256 to 256 with NOTHING added and NOTHING removed, `^Done: R-\d+ — ` 5, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout, all ids DISTINCT and the maximum `R-0695`; `^Gate: F\d+ R\d+ — ` 25 to 26 with the ADDED key exactly `F031 R44`; `^## DECISION F031 D\d+ ` 21 to 22; open set 251 before C2 and 251 after. MARKERS 0 and 0 in all eight written targets against a live CONTROL of 3 and 3. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 10 paths over `f98a91cd`..`9236e617`, with both residues EMPTY. THE EIGHT COMMITS ARE EACH SINGLE-PARENT at insertions 338, 248, 25, 2, 27, 102, 153 and 57, every one under 500; the reviewer read the reflog for ALL EIGHT rather than the seven G8 scoped, every entry reads `commit:`, so `amend`, `rebase` and `cherry` are 0 each among them; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE MODEL HALF IS WHAT S1 THROUGH S5 ORDERED: `posts` is computed ONCE per card from a strict `=== true`, stamped on all three branches of `decisionAnswers`, and `answerableByDecisionResolve` reads the same comparison, so a card and its answers cannot disagree; the one stale sentence S5 asked for was found and corrected, the `DecisionInboxEntry` docstring's "plus the two keys" becoming "three". THE BROWSER HALF IS WHAT S6 THROUGH S9 ORDERED: a refused answer renders as a `<code>` carrying `answer.value` with no button chrome and `user-select: all`, the button remains the ternary's TRUE arm so the guard region stays clean, and the component's header now says what is true of a posting answer rather than of every answer. NO ASSERTION WAS WEAKENED ANYWHERE, WHICH THE ROUND PROVED RATHER THAN PROMISED: `toMatchObject(` is 0 across all 30 files matching `apps/ui/src/**/*.test.ts` at both C4 and C5, `it(` grew 36 to 42 and `toEqual(` grew 15 to 19 in `apps/ui/src/api/decisionCard.test.ts`, and `def test_` grew 31 to 37 in the contract file. THE TOOLCHAIN IS GREEN AT BOTH CODE COMMITS: `npx tsc --noEmit` REAL exit 0 and `npx vitest run` REAL exit 0 at 30 files and 454 tests, against 448 at `f98a91cd`. THE RED CONTROLS DISCRIMINATE, AND THE REVIEWER ADDED A THIRD THE BLOCK DID NOT ORDER: `=== true` widened to `!== false` fails 11 tests at REAL exit 1, `posts` stamped true unconditionally fails 13 at REAL exit 1, and — the reading that matters most for a component no suite renders — a component changed to ignore `answer.posts` and always emit a button leaves `vitest` GREEN at 454 and turns `tests/ui_contracts/test_decision_answer_wiring.py` RED at REAL exit 1, naming `test_the_card_discriminates_on_the_per_answer_posts_flag` and `test_the_conditional_sits_before_the_button_and_never_after_it`. So the guards S10 added are LOAD-BEARING rather than decorative, which is the only evidence available that a browser change is tested at all here. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT are `tests/ui_server/` 480, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, the canary 42 and `tests/ui_contracts/` 562 passed with 4 skipped — every reading at REAL exit 0, and the contract suite grown by exactly the 6 guards S10 adds. THE HANDBACK WAS AUDITED AS AN ARTIFACT: all TEN `+/-` cells equal `git diff --numstat` exactly, the item-status table covers all twenty ordered items, one line per gate carries a real exit code, and its 93 lines sit inside the 100-line tier eight tabled commits earn. THE ONE DEFECT OF THE ROUND IS THE REVIEWER'S OWN AND IS REGISTERED AS R-0696: S10 ordered a guard the target file already carried, so one of the six new tests duplicates a neighbour — the worker applied it as written and flagged it, which is exactly what constraint 1 asks of it. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. R45 completed DECISION F031 D19 across the wire, and the inbox now tells the truth about which of its cards the write door will take.
<<<END LEDGER46

<<<SLICE DECISION23
## DECISION F031 D23 (2026-08-27) — a record round takes R46, and the remaining programme moves by one

SUPERSEDING A ROUND ATTRIBUTION IN DECISION F031 D21: that entry rules "the
`fp:` dispatch R46 and the clarification FORM R47". The R45 gate produced a
verdict and a finding, and `docs/agents/planner_reviewer_prompt.md` §4 item 4
requires findings to persist FIRST, in their own commit, before any repair — so
the record cannot wait for a round that also ships code without risking exactly
what that rule exists to prevent.

CHOSEN, THE RECORD GETS ITS OWN ROUND. R46 writes only `.agent/` state. The
`fp:` dispatch becomes R47, which also retires the duplicate guard R-0696 names,
and the clarification FORM becomes R48. Nothing any earlier entry CHOSE changes:
not the answerability key, not the predicate it is computed from, not the
refusal to branch on `card.type`, not the scope ruling that leaves six prefixes
out of F031. Only the round numbers move, for the third time in this feature and
for the same reason each time — a round is sized against the code, never against
the sentence that named it.

CONSIDERED AND REJECTED: folding the record commits into R47's block. It would
put a finding's registration behind a code change in the same round, which is
the ordering §4 item 4 forbids, and it would leave the R45 verdict off disk for
the length of a session that might not survive to write it.

REVERSE IT by merging R46's commits into R47 and renumbering back, which costs
nothing on disk — this entry moves labels, not work.
<<<END DECISION23
