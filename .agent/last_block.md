── STEP T002 the browser half of D19 / F031 — ROUND R45 ───────────────
Goal:        Carry answerability into the browser. `DecisionCardModel` gains the
             endpoint's third key, every answer gains a `posts` flag derived
             from it, and `DecisionInboxCard` renders a non-posting answer as
             PASTEABLE TEXT instead of a button the door would refuse. Also
             record R44's verdict and land DECISION F031 D22.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R44 gate entry · C3 DECISION F031 D22 · C4 the model half
             · C5 the browser half · C6 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r45.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `apps/ui/src/api/decisionCard.ts`,
             `apps/ui/src/api/decisionCard.test.ts`,
             `apps/ui/src/components/panels/DecisionInboxCard.tsx`,
             `apps/ui/src/components/panels/RightLivePanel.module.css`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `.agent/handoff.md`. NO FILE UNDER `packages/` and NO FILE UNDER
             `docs/` — the endpoint is done and R-0695's process half is a
             reviewer-file round this block does not open.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof, and stopping
    early would lose the record this round exists to write.
 2. THE CODE IS DESCRIBED, NOT SLICED. Section S below is a numbered SPEC, not
    an authored text: you write the TypeScript, the CSS and the Python yourself
    to satisfy it, in each surrounding file's own idiom. The byte-for-byte rule
    of constraint 1 binds the marked SLICES and nothing else; report how many
    your extractor found.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The model half
    at C4 lands BEFORE the browser half at C5, so `vitest` is green again at C4
    and the component consumes a field that already exists. No pair may be
    reordered. LEDGER45 states facts about THIS round's own commits, and this
    constraint is what makes them true on landing.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R44. That is
    ordered: the plan becomes current at C1, the first substantive commit.
 5. THE GATE ENTRY AND THE DECISION ARE THE REVIEWER'S TEXT. You never write a
    `Done:` paragraph, never edit LEDGER45, never edit D22. NO FINDING IS
    REGISTERED THIS ROUND: R44 passed every gate and raised none, so
    `^- R-\d+ — ` does not move and the open set stays where C2 finds it.
 6. THE LEDGER SETS MOVE ONCE. Across C2 `^Gate: F\d+ R\d+ — ` moves 25 to 26
    with the ADDED key exactly `F031 R44`. Across C2, `^- R-\d+ — ` stays 256,
    `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 251 before C2 and 251 after. `^## DECISION F031 D\d+ `
    is 21 before C3 and 22 after.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. Every red control of gate G7 runs
    inside a disposable `git worktree` under `.remedy-wt/`, NEVER in the primary
    checkout, and the worktree is removed BY ITS EXACT PATH when G7 ends. A
    fresh worktree has NO `apps/ui/node_modules` and a symlink is refused in
    this session, so populate it with
    `shutil.copytree(src, dst, symlinks=True)` — `symlinks=True` is ORDERED, not
    optional, because the default dereferences npm's bin shims and manufactures
    failures the control would then report as real (finding R-0591). Nothing
    under `.remedy-wt/` is ever committed, and `.remedy-wt/f031-r45-block.md` is
    the reviewer's scratch copy — leave it alone, do not delete it.
    `git status --porcelain` reads 0 lines at every commit.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, build dicts with `dict(key=value)`, and
    copy with `shutil.copyfile` or `shutil.copytree`. Run `npx` through
    `subprocess.run` with `cwd="apps/ui"`, never through a `cd` compound.

S. THE SPEC. Write every file to satisfy every numbered item; the item numbers
are the contract, the wording is not a text to copy. S1–S5 are C4, S6–S10 are C5.
 S1. In `apps/ui/src/api/decisionCard.ts`, `DecisionInboxEntry` gains an optional
     `answerable_by_decision_resolve?: boolean` — the endpoint's OWN spelling,
     unrenamed, for the reason DECISION F031 D1 gives.
 S2. `DecisionAnswer` gains `posts: boolean` with a WHY comment: whether pressing
     this affordance may POST, false when the write door would refuse the
     decision, in which case the value is shown as pasteable text instead.
 S3. `DecisionCardModel` gains `answerableByDecisionResolve: boolean`, the
     camel-case projection of S1's key, carried so the component never has to
     read the raw entry.
 S4. `decisionAnswers` computes `posts` ONCE from
     `card.answerable_by_decision_resolve === true` and stamps it on EVERY answer
     it returns, in all three branches — options, next actions and the free-text
     fallback. The strict `=== true` is deliberate: an ABSENT key must give
     false, so a payload from an older server never renders a posting button.
     This function still MUST NOT branch on `card.type`; a derived boolean the
     server computed is data, exactly as `blocked_count` is.
 S5. `buildDecisionCardModel` sets `answerableByDecisionResolve` from the same
     `=== true` reading. Then sweep this file for every sentence the third key
     makes stale — the `DecisionInboxEntry` docstring says "plus the two keys
     `build_decision_inbox` adds" — and correct each. Report in the handback how
     many such sentences you found and where. In
     `apps/ui/src/api/decisionCard.test.ts`, UPDATE every assertion the new
     fields break: at the reviewer's dry run 9 tests in that file failed, 2 under
     `buildDecisionCardModel` and 7 under `decisionAnswers`, all of them whole-
     object or whole-array equalities. ADD the new fields to their expected
     literals. DO NOT weaken an assertion to make it pass — `toMatchObject` is 0
     across every file matching `apps/ui/src/**/*.test.ts` today and must still
     be 0 when you are done. ADD tests pinning: the key TRUE gives `posts` true
     on every answer, the key FALSE gives `posts` false on every answer, and the
     key ABSENT gives `posts` false.
 S6. In `apps/ui/src/components/panels/DecisionInboxCard.tsx`, an answer whose
     `posts` is false renders NOT as a `<button>` but as pasteable text carrying
     `answer.value`, in a `<code>` element with its own class. An answer whose
     `posts` is true renders exactly the button it renders today, unchanged in
     every attribute. Keep the `<p>` outcome paragraph EXACTLY where it is, one
     per answer, rendered from the row's first render — finding R-0686 and the
     guards `tests/ui_contracts/test_decision_answer_wiring.py` already carries
     bind here and this round must leave every one of them green.
 S7. THE CONDITIONAL GOES BEFORE THE BUTTON, NEVER BETWEEN THE BUTTON AND THE
     PARAGRAPH. `jsx_between_answer_button_and_live_paragraph` in that contract
     file reads everything between the LAST `</button>` and the outcome `<p` and
     forbids `?`, `&&` and `||` in it. The reviewer measured the shape this
     block asks for and it passes; a shape with the ternary's `?` after the
     button's closing tag does not. If your rendering needs the other order, do
     NOT reorder the guard — say so in the handback and keep this order.
 S8. The component's HEADER comment currently promises that the buttons "ship
     ENABLED and a press really reaches `/api/jobs/<job_id>/commands`". That is
     now true only of a posting answer. Correct that paragraph to say what is
     now true, and record the deliberate absence a reader will search for: this
     component still does NOT branch on a decision's `type` or `status` — it
     reads a per-answer boolean the model derived — so DECISION F031 D5's rule
     is intact and the guard that pins it stays green.
 S9. In `apps/ui/src/components/panels/RightLivePanel.module.css`, add the
     rule for S6's class beside the existing `.decisionAnswer` rule at line 256.
     It is TEXT, not a control: no button chrome, `--remedy-font-mono`, a muted
     colour, and `user-select: all` so one click selects the whole command —
     "pasteable" is the point of the affordance, not a description of it. Use
     only tokens `apps/ui/src/styles/tokens.css` already defines; the reviewer
     measured that no new token is owed.
 S10. In `tests/ui_contracts/test_decision_answer_wiring.py`, ADD guards — do not
     edit or delete an existing one — pinning what S6 and S7 establish: that the
     component renders `answer.posts` as the discriminator, that a `<code>`
     element carrying `answer.value` exists, that the class S9 adds really has a
     rule in the stylesheet, and that the region between the last `</button>`
     and the outcome `<p` still holds none of `?`, `&&`, `||`. The last one
     re-uses the reader already in that file. WITHOUT S10 THE TEXT BRANCH IS
     UNGUARDED: today's guards do not forbid the wrong order, they merely fail
     to require the right one, and the reviewer measured that difference.
 S11. Nothing else changes in any file. No existing test is deleted, no assertion
     weakened, no fixture edited, and no file under `packages/` or `docs/` is
     touched.

Done when — run every gate yourself and record its REAL exit code. G1 through G9
run at commits STRICTLY EARLIER than C6, so the handback can quote them; the
push is ordered after C6 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3,
     C4 and C5. `.agent/STOP` read from disk before C0a and before C6, both
     ABSENT. Report the sha256, byte count and line count of this block as saved
     at C0a, as mirrored at C0b, and as read off disk at C5 — all three must be
     EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R45 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with `git show <rev>:<path>`
     into memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob plus ONE newline
     plus LEDGER45; `.agent/decisions.md` at C3 equals ITS pre-commit blob plus
     ONE newline plus DECISION22. The pre-commit blob for C2 is 849619 bytes and
     for C3 is 605733 bytes. For EACH append report both byte counts and the sum.
     Then confirm EACH with a SECOND, independent reader: split the whole file on
     blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in that
     slice — never a number this block asserts — and compare the LAST N units of
     the file against the slice's N paragraphs IN ORDER. Report N and the unit
     count before and after for each. THE NEGATIVE CONTROL GOES ON THE FIRST
     APPENDED PARAGRAPH, which is the position a tail-only reading cannot see:
     flip ONE byte IN MEMORY inside paragraph 1 of each slice and report that
     BOTH readers REJECT it. For any slice whose N is 1, say so and note that
     paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report before C2 and after C2 the line-anchored counts of
     `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: R\d+ — ` and
     `^Gate: F\d+ R\d+ — `, plus the ids and gate keys ADDED and REMOVED as SETS,
     whether all ids are DISTINCT, and the maximum id. Every movement constraint
     6 names is checked here, INCLUDING the ones that must NOT move. Report the
     open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` at both points. Also
     report `^## DECISION F031 D\d+ ` in `.agent/decisions.md` before and after
     C3.
 G6. THE SPEC, ITEM BY ITEM. For EACH of S1 through S11 report DONE or NOT DONE
     with the file and line where it landed. Report, over
     `apps/ui/src/api/decisionCard.ts` at C4, every line containing the word
     `two`, so the reviewer can see S5's staleness sweep rather than take it on
     trust. Report `toMatchObject(` counted over every file matching
     `apps/ui/src/**/*.test.ts` at C4 and at C5 — it is 0 today and must be 0 at
     both. Report the count of `it(` in
     `apps/ui/src/api/decisionCard.test.ts` before and after C4, and the count of
     `def test_` in `tests/ui_contracts/test_decision_answer_wiring.py` before
     and after C5; both must GROW and neither file may lose one.
 G7. THE UI TOOLCHAIN AND ITS RED CONTROLS. In the PRIMARY checkout run, through
     `subprocess.run` with `cwd="apps/ui"`: `npx tsc --noEmit` and
     `npx vitest run --reporter=basic`, at C4 and again at C5, reporting the REAL
     exit code and the test-file and test totals each time. At `f98a91cd` these
     read exit 0 with 30 files and 448 tests. THEN, INSIDE A DISPOSABLE WORKTREE
     populated per constraint 8 and never in the primary checkout, run these red
     controls, one at a time, restoring the tree between them and re-checking
     byte-equality with the original after each restore:
     (a) in `apps/ui/src/api/decisionCard.ts`, change S4's `=== true` to
         `!== false`, so an ABSENT key would render a posting button;
     (b) in the same file, stamp `posts: true` on every answer unconditionally.
     For EACH report the REAL exit code of `npx vitest run` and the FAILING TEST
     NAMES the run printed. Do NOT predict which test fails, do not predict how
     many fail, and do not name an expected colour — report what the run printed.
     A control that does not change the outcome is a finding you write into the
     handback, not a number to adjust: it means the tests S5 adds do not
     discriminate, and the reviewer wants to know that far more than it wants a
     green line.
 G8. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `.agent/decisions.md` at C3 and EVERY file C4 and C5 touch, against a
     CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only f98a91cd..C5` and compare it BOTH WAYS against this
     round's expected path set. Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and under 500. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C5,
     AFTER G7's worktree has been removed. Report the reflog FOR THIS ROUND'S
     OWN COMMITS ONLY: every operation prefix must read `commit`, and among
     those entries `amend`, `rebase` and `cherry` must be 0 each. Do not count
     those words over the whole reflog, which holds this repository's entire
     history and is not what this gate asks.
 G9. THE STATE READERS, THE CONTRACTS AND THE CANARY, in the PRIMARY checkout at
     C5 and SERIALLY — never two pytest processes alive at once. Run and report
     the real exit code and count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, the canary
     `tests/cli/test_golden_path.py`, and `tests/ui_contracts/`. At `f98a91cd`
     these read 480, 52, 21, 16, 42 and 556 passed with 4 skipped;
     `tests/ui_contracts/` MUST GROW by exactly the guards S10 adds and you
     report both numbers. ON ANY RED, capture the `FAILED` node ids BEFORE
     anything else and re-run that suite ALONE five more times, reporting every
     reading and every node id; a red you cannot reproduce is reported WITH its
     node ids, never absorbed.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G8, the item-status table covering C0a,
             C0b, C1, C2, C3, C4, C5, C6, each of S1 through S11 and the push,
             ONE LINE PER GATE for G1 through G9 with its real exit code, the
             open-findings count, and the next expected action. THE NEXT ACTION
             SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review this round's handback,
             then R46 — the `fp:`-prefixed dispatch DECISION F009 D5 planned and
             did not ship, reusing `flight_plan.resolve_flight_plan_approval`.
             Derive your line cap from AGENTS.md yourself, from the commit count
             you actually made; if the mandated content genuinely does not fit,
             declare the DECISION D15 overage with its stated cause. Then push
             with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R45
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D22.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R45 carries answerability into the browser, which is DECISION F031 D19's second
clause and the half D20 split off. `DecisionCardModel` gains the endpoint's third
key, every answer gains a `posts` flag derived from it, and `DecisionInboxCard`
renders a non-posting answer as pasteable TEXT rather than as a button the write
door would refuse. It also records R44's PASS and lands DECISION F031 D22.

## Next Steps
1. R46: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R47: the
   clarification FORM over `payload.clarifications`.
2. A reviewer-file round landing the §3 checklist item R-0694 and R-0695 share:
   a block computing a value from another module's predicate reads that
   predicate's OWN refusal conditions, not merely its route to the data.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- AFTER THIS ROUND THE INBOX STILL OFFERS NO WAY TO ANSWER SEVEN OF THE EIGHT
  PRODUCING TYPES — it stops LYING about them, which is D19's whole claim, and
  R46 is where the `fp:` prefix gains a real dispatch. R-0693 measures the gap.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts` and no DOM environment ships, so this round's component
  change is gated by comment-stripped SOURCE reading in
  `tests/ui_contracts/test_decision_answer_wiring.py` and by `tsc --noEmit`.
- THE REGION GUARD FORBIDS AN OPERATOR, NOT AN ORDER: the reader between the
  last `</button>` and the outcome `<p` rejects `?`, `&&` and `||`, so a correct
  render written in the other order goes red for an unrelated-looking reason.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `f98a91cd`
  and this round does not move it.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R45

<<<SLICE LEDGER45
Gate: F031 R44 — the F031 R44 entry. R44 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM AVAILABLE TO THIS WORKFLOW: the reviewer's OWN scratch original `.remedy-wt/f031-r44-block.md`, the C0a blob, the C0b blob and `.agent/last_block.md` read off disk at C5 are ALL FOUR byte-identical at sha256 `87e21495a88fef3c7aed52b8a6ec42f5a96e49859d4cda083cf04177d481275f` over 28458 bytes and 300 lines, with C0a and C0b resolving to the SAME git blob `d84e4272` — the reviewer compared its own scratch file against the committed blob rather than trusting the worker's reading of it. THE EXTRACTION printed 4 slices, CONTENT 76 and TOTAL 300, so PROSE was 224 against 400 and TOTAL 300 against 490. THE PLAN at `0cbf4911` is byte-equal to PLANF031R44 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 47, strictly under 50. THE THREE APPENDS ARE EXACT AND R-0631'S CLAUSE WAS APPLIED AGAIN: 841494 + 1 + 3235 = 844730 and 844730 + 1 + 4888 = 849619 in the ledger and 603923 + 1 + 1809 = 605733 in `.agent/decisions.md`, blank-line units 348 to 349 to 350 and 1450 to 1455, N counted by the reviewer's own script at 1, 1 and 5, every whole-file identity TRUE, and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on all three. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^- R-\d+ — ` 255 to 256 to 256 with ADDED across C2 exactly {`R-0695`} and REMOVED EMPTY, all ids DISTINCT and the maximum `R-0695`; `^Done: R-\d+ — ` 5, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; `^Gate: F\d+ R\d+ — ` 24 to 24 to 25 with the ADDED key exactly `F031 R43`; `^## DECISION F031 D\d+ ` 20 to 21; open set 250 before C2 and 251 after C3. MARKERS 0 and 0 in all five written targets against a live CONTROL of 4 and 4. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 7 paths over `46ae059f`..`50e97f81`, with the range-minus-expected and expected-minus-range residues BOTH EMPTY, and NOT ONE PATH under `apps/` or `docs/`. THE EIGHT COMMITS ARE EACH SINGLE-PARENT at insertions 300, 194, 20, 2, 2, 28, 59 and 52, every one far under 500; the reviewer read the reflog for ALL EIGHT rather than the seven G8 scoped, and every entry reads `commit:`, so `amend`, `rebase` and `cherry` are 0 each among them; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE CODE IS WHAT SECTION S ORDERED, AND S5 WAS PROVED BY AST RATHER THAN BY EYE: the module docstring, `build_decision_inbox`, `_decision_age_seconds` and `_blocked_subtree_size` are all byte-identical between C4 and C5 under `ast.unparse`, only `_answerable_by_decision_resolve` changed, and the diff over that file holds exactly two hunks — so the round changed what the key SAYS and nothing the document HOLDS. `python3 -m ruff check` on both changed files is REAL exit 0, and the test file's `assert` statements counted by AST move 21 to 27. THE TESTS AND THE CONTROLS REPRODUCED EXACTLY: 34 passed at REAL exit 0 against 33 at `46ae059f`; the existence-only red control failed at REAL exit 1 with exactly one FAILED node id, `test_answerable_key_goes_false_once_the_decision_has_been_answered`, which is the new test and therefore the discriminator R-0695 said the suite lacked; `return True` failed 8 and `return False` failed 2, both at REAL exit 1. Every control ran only inside a disposable worktree, the tree was restored byte-equal after each, and the primary checkout read 0 porcelain lines throughout. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT are `tests/ui_server/` 480, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, the canary 42 and `tests/ui_contracts/` 556 passed with 4 skipped — every reading at REAL exit 0 and identical to the `46ae059f` baseline. THE DEFECT R-0695 REGISTERED IS GONE, AND THE REVIEWER PROVED IT WITH THE SAME PROBE THAT FOUND IT: at `50e97f81` an answered task decision's card reads `status` `resolved` and `answerable_by_decision_resolve` FALSE while a second `answer_task_decision` returns None, where at `46ae059f` the same probe read TRUE against the same None. THE HANDBACK WAS AUDITED AS AN ARTIFACT: all eight `+/-` cells equal `git diff --numstat` exactly, the item-status table covers all sixteen ordered items, one line per gate carries a real exit code, and its 97 lines sit inside the 100-line tier eight tabled commits earn. THE WORKER ALSO CAUGHT ITS OWN DRAFT ERROR AND MEASURED RATHER THAN SHIPPED IT: a DECISION D15 stated-cause line claiming 106 lines against the cap was removed once the file measured 97, so a false declaration never reached disk — which is the R-0526 class defeated by measurement before emission rather than by a reviewer afterwards. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. R44 registered R-0695, repaired its CODE half in the same round, and left its PROCESS half OPEN and named.
<<<END LEDGER45

<<<SLICE DECISION22
## DECISION F031 D22 (2026-08-27) — answerability reaches the renderer as a PER-ANSWER flag, and a refused affordance is pasteable text rather than a disabled button

CHOSEN, THE FLAG IS STAMPED ON THE ANSWER, NOT READ FROM THE CARD BY THE
MARKUP. `decisionAnswers` computes `posts` once from the endpoint's
`answerable_by_decision_resolve` and stamps it on every affordance it returns,
and the component projects that boolean. DECISION F031 D5 rules every real
branch into `decisionCard.ts`, where the shipped vitest config can reach it, and
a component reading the card's key directly would put the rule in markup no
suite renders. The reading is strict `=== true`, so a payload from a server
older than R43 renders no posting button at all.

CHOSEN, A REFUSED AFFORDANCE IS SHOWN AS PASTEABLE TEXT. The value stays on
screen — it is the exact `remedy` command that answers the question — and it is
selectable, so the operator can still act on it in a terminal. The affordance
simply stops claiming the browser will do it for them.

CONSIDERED AND REJECTED: a DISABLED button. It keeps the control's shape while
removing its function, which is the shape R-0693 already found dishonest, and a
disabled control is skipped by keyboard navigation, so the command would become
unreachable for exactly the operators most likely to want to paste it.

CONSIDERED AND REJECTED: hiding a refused answer entirely. That loses the
question, which is the one thing this inbox exists not to do.

REVERSE IT by stamping `posts: true` unconditionally in `decisionAnswers`, which
the tests R45 adds will refuse; that refusal is the evidence for this entry.
<<<END DECISION22
