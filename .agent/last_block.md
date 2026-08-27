── STEP REPAIR ROUND / F031 — ROUND R48 ───────────────────────────────
Goal:        Finish what R47 started and left red. `tests/ui_server/` FAILS on
             the branch tip at `20eabead` — one test, the door's import guard —
             because R47's block ordered two new imports into the door without
             ordering the guard that pins them. Green the tip FIRST, then land
             the three things R47 never reached: the door's own tests, the
             answerability mirror, and the browser-side proof. Register the
             three defects, all of which are the REVIEWER'S, before repairing
             any of them.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the three findings · C3 the R47 verdict · C4 DECISION F031
             D25 · C5 GREEN THE TIP · C6 the door's tests · C7 the
             answerability mirror · C8 the browser proof · C9 handback · then
             push.
Change:      Exactly these paths, nothing else.
             `.agent/authored/f031-r48.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
             `.agent/handoff.md`,
             `packages/orchestration/decision_inbox.py`,
             `tests/ui_server/test_command_channel.py`,
             `tests/ui_server/test_command_dispatch.py`,
             `tests/orchestration/test_decision_inbox.py`,
             `apps/ui/src/api/decisionCard.test.ts`.
             NO PRODUCTION FILE OUTSIDE `decision_inbox.py` CHANGES. In
             particular `packages/orchestration/ui_server.py` and
             `packages/orchestration/decision_queue.py` are FINISHED: R47
             landed both and the reviewer read both diffs and found them
             faithful to their spec. If you believe either needs a change, that
             is a finding for the handback, not an edit.
             NO FILE UNDER `docs/` CHANGES, for the reason R47's block gave and
             the reviewer re-checked: no ist-doc names this command.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. Slices are `.agent/` text ONLY. The code below is DESCRIBED
    as a numbered SPEC: you write it yourself, reading each named file before
    you touch it, and AGENTS.md's file-editing safety rules bind every edit.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C9.
    Two orderings are load-bearing. The findings land at C2 BEFORE any repair,
    which is what `docs/agents/planner_reviewer_prompt.md` §4 item 4 requires.
    And C5 greens the tip BEFORE C6 adds tests to the same suite, so that a red
    at C6 is unambiguously C6's own.
 3. RUN THE SUITE A COMMIT GATES BEFORE YOU MAKE THAT COMMIT, not after. R47's
    worker recorded this as its own lesson and it is right: it committed the
    door's code and only then ran `tests/ui_server/`, so a guard that was
    already red travelled one commit further than it needed to. For every
    commit below that touches code, run its suite on the WORKING TREE first,
    read the real exit code, and only then commit.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R47. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a finding, a `Done:`
    paragraph or a decision of your own. THREE FINDINGS ARE REGISTERED THIS
    ROUND AND NONE OF THEM IS YOURS: all three are defects in the R47 block,
    which the reviewer wrote. R47's worker executed that block correctly,
    including its refusal to edit a test to clear a red it was not told to
    expect, and the findings say so.
 6. THE LEDGER SETS MOVE EXACTLY THREE TIMES. Across C2 `^- R-\d+ — ` moves
    257 to 260 with the ADDED ids exactly `R-0697`, `R-0698` and `R-0699`.
    Across C3 `^Gate: F\d+ R\d+ — ` moves 28 to 29 with the ADDED key exactly
    `F031 R47`. Across C4 `^## DECISION F031 D\d+ ` moves 24 to 25. Across the
    WHOLE round `^Done: R-\d+ — ` stays 6, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 251 before C2 and 254 after C3.
    NO `Done:` LINE IS WRITTEN THIS ROUND for R-0697, R-0698 or R-0699: a
    finding registered and repaired inside one round is still recorded by the
    NEXT round's reviewer, who has to verify the repair first.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C9. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
 8. NOTHING UNDER `.remedy-wt/` IS EVER COMMITTED and `git status --porcelain`
    reads 0 lines at every commit. `.remedy-wt/f031-r48-block.md` is the
    reviewer's scratch copy — leave it alone. R47's worker left its own scratch
    under `.remedy-wt/r47slices/` and three `r47_*` files there; leave those
    alone too, and never delete anything under that directory by glob.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`. Run
    pytest SERIALLY — never two pytest processes alive at once.
10. NEVER WEAKEN AN ASSERTION TO MAKE A GATE GREEN. S1 and S6 each widen a
    guard's ruled set, which is the mechanism those guards document for exactly
    this case — not a weakening. Nothing else existing may change. If any other
    test turns red, that is a finding for the handback and a hand-back.

SPEC — read each file before editing it.
 S1. GREEN THE TIP (C5). `tests/ui_server/test_command_channel.py`'s
     `TestCommandDoorImportGuard.ALLOWED_IMPORTS` gains exactly two entries:
     `("packages.orchestration.flight_plan", "open_clarification_questions")`
     and `("packages.orchestration.flight_plan", "resolve_flight_plan_approval")`.
     THIS IS THE MECHANISM THAT GUARD DOCUMENTS, not a weakening of it: its own
     comment says every entry is there "because a ruled DECISION puts it there"
     and that adding one "belongs in the same commit as the decision that
     widens it". DECISION F031 D24, landed at R47's C3, is that decision, and
     it is what R47's block failed to carry into this file. Follow the existing
     idiom: each entry carries a trailing comment naming its ruling, and
     because the surrounding entries cite F009 decisions as bare `D5` and `D21`,
     yours must read `F031 D24` so the two families cannot be confused. Keep
     the set's existing ordering convention. Change NOTHING else in that class:
     `DOOR_METHODS` and `FORBIDDEN_MODULES` stay exactly as they are, and
     `packages.orchestration.flight_plan` is correctly absent from the
     forbidden set already — the reviewer checked.
 S2. TESTS FOR THE DOOR (C6), split across the two files by the boundary their
     own docstrings draw — `test_command_dispatch.py`'s module docstring says
     its sibling `test_command_channel.py` "pins what the door ANSWERS" while
     it pins "the three writes DECISION F009 D18 orders behind that answer".
     The door's `fp:` branch landed at R47's C6 with NO test of its own; that
     is finding R-0699 and this item is its repair.
 S3. IN `tests/ui_server/test_command_channel.py`, four tests of what the door
     ANSWERS: an `fp:approval` on a PENDING plan with the answer `approve`
     answered 200, whose body carries exactly `command`, `outcome` reading
     `accepted`, and `decision_id`; the same with `reject`, also 200; the same
     on a plan whose `_approval` is NOT pending, answered 409 with a
     `rejected_state` audit line; and an answer that is neither literal
     answered 409 with that same audit line. For that last one use the exact
     string `remedy decision resolve <id> fp:approval --reason approve`,
     because finding R-0693 measured that as what the browser posted before
     R47 — so the test pins the old bug shut rather than inventing a case.
 S4. IN `tests/ui_server/test_command_dispatch.py`, two tests of the EFFECT
     behind that answer: that an accepted approval really ran
     `resolve_flight_plan_approval`, evidenced by the job's `flight_plan`
     reading `_approval` == `approved` ON DISK after the request; and that
     `save_job` ran EXACTLY ONCE for it. That count is the only guard on the
     door's deliberate omission of its own `save_job` call — R47's C6 left a
     comment at that spot explaining why it is absent, and this test is what
     stops a later reader from "fixing" the absence.
 S5. THE ANSWERABILITY MIRROR (C7).
     `packages/orchestration/decision_inbox.py::_answerable_by_decision_resolve`
     gains the mirror of the door's `fp:` branch: an id starting `fp:` is
     answerable if and only if `job.flight_plan` is a dict whose `_approval` is
     `"pending"` — the SAME two conditions the door reads at
     `ui_server.py`, which you should read before writing this so the two
     cannot drift. Ids that do not start `fp:` keep the existing
     `find_task_decision` plus open-status read, unchanged. Extend that
     function's docstring: it currently states that `task_decision` "is the
     whole set", which this change makes FALSE, and leaving that sentence
     standing would be a stale claim beside correct code.
 S6. IT IS NOT A `card.type` BRANCH and the docstring must say why in one
     sentence, because that same docstring forbids one and the next reader will
     think the rule was broken: the door itself dispatches on the ID PREFIX, so
     mirroring the door means reading the prefix. A type branch would read
     `flight_plan_approval` — which the RESOLVED card also carries while the
     door refuses it — and would be wrong for exactly the reason the existing
     note about answered task decisions already gives.
 S7. `tests/orchestration/test_decision_inbox.py`'s `ANSWERABLE_DECISION_TYPES`
     becomes `("flight_plan_approval", "task_decision")`, and its comment —
     which today says `_dispatch_decision_resolve` "reaches a record only
     through `escalation.find_task_decision` … so `task_decision` is the whole
     set" — is rewritten to state what is now true and to name DECISION F031
     D24 as what changed it. THIS IS NOT WEAKENING THE PARAMETRIZED GUARD: that
     tuple is compared against the card each PRODUCING FIXTURE builds, and
     `_fixture_flight_plan_approval` builds `{"_approval": "pending"}`, which
     the door now genuinely accepts. The reviewer read that fixture rather than
     assuming its state.
 S8. THE RESOLVED CASE GETS ITS OWN TEST, a sibling of the existing
     `test_answerable_key_goes_false_once_the_decision_has_been_answered` and
     for the identical reason its docstring gives — a type check cannot tell an
     open card from a resolved one, because both carry the same `type`. Assert
     that a job whose `flight_plan._approval` reads `approved` yields an
     `fp:approval` card with `answerable_by_decision_resolve` FALSE. Without
     this, S7's tuple entry would be the only statement about the type and it
     would read as "every flight-plan card is answerable", which is false.
 S9. THE BROWSER PROOF (C8), one test in `apps/ui/src/api/decisionCard.test.ts`,
     written in that file's existing idiom — the reviewer read it: the
     neighbouring cases build a `DecisionInboxEntry` literal and compare
     `decisionAnswers(card)` with `toEqual` against the full expected array.
     Feed it a card shaped like the endpoint's PENDING `fp:approval`: `type`
     `"flight_plan_approval"`, `payload` carrying
     `options: ["approve", "reject"]`, and `answerable_by_decision_resolve`
     true. Assert `toEqual` against exactly two entries, both `kind: "option"`,
     with `label` and `value` both `approve` then both `reject` in that order,
     each carrying `posts: true`. This is the only evidence available that the
     browser half works, because no DOM harness reaches the component.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C9, so the handback can quote them; the
push is ordered after C9 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after every commit from C0a to C8.
     `.agent/STOP` read from disk before C0a and before C9, both ABSENT. Report
     the sha256, byte count and line count of this block as saved at C0a, as
     mirrored at C0b, and as read off disk at C8 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R48 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with
     `git show <rev>:<path>` into memory; never write a past blob over a
     tracked file to read it. `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus FINDINGS48; at C3 equals ITS OWN
     pre-commit blob — which you READ rather than take from this block — plus
     ONE newline plus LEDGER48; `.agent/decisions.md` at C4 equals ITS
     pre-commit blob plus ONE newline plus DECISION25. The reviewer measured
     the two BASE blobs at `20eabead` itself: `.agent/live_review.md` is 868456
     bytes and `.agent/decisions.md` is 611101. If either reads differently
     before its commit, something moved that this round did not order — stop
     and hand back. For EACH append report both byte counts and the sum. Then
     confirm EACH with a SECOND, independent reader: split the whole file on
     blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in that
     slice — never a number this block asserts — and compare the LAST N units
     of the file against the slice's N paragraphs IN ORDER. Report N and the
     unit count before and after for each. THE NEGATIVE CONTROL GOES ON THE
     FIRST APPENDED PARAGRAPH, which is the position a tail-only reading cannot
     see: flip ONE byte IN MEMORY inside paragraph 1 of each slice and report
     that BOTH readers REJECT it. For any slice whose N is 1, say so and note
     that paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at four points — before C2, after C2, after C3,
     after C4 — the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     and gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 6 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set before C2
     and after C3. Also report `^## DECISION F031 D\d+ ` in
     `.agent/decisions.md` before and after C4.
 G6. THE TIP IS GREEN AND THE GUARD STILL BITES. Run
     `python3 -m pytest tests/ui_server/ -q` at `20eabead` BEFORE C5 and report
     the REAL exit code and counts: the reviewer measured 1 failed and 479
     passed at exit 1, naming
     `TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set`.
     Run it again after C5 and report 480 passed at exit 0. Then, in a
     DISPOSABLE WORKTREE and never in the primary checkout, prove the widened
     guard still bites: remove ONE of S1's two new entries and report that the
     same test turns RED at a real exit code of 1; restore it, remove the
     other, report the same. A guard that passes with an entry missing is a
     guard that stopped reading the door. Report each colour as a REAL exit
     code, never as a word, say exactly which lines you removed for each
     mutation, and confirm the worktree is removed afterwards and
     `git worktree list` is back to 1 line.
 G7. THE NEW TESTS FAIL WITHOUT THE CODE THEY PIN. In the same disposable
     worktree at C8, run three mutations, each restored before the next.
     (a) Delete the door's `answer not in ("approve", "reject")` refusal and
     report that `tests/ui_server/` turns RED at exit 1. (b) Delete the door's
     call to `resolve_flight_plan_approval` and its return, so the `fp:` branch
     falls through, and report that `tests/ui_server/` turns RED at exit 1.
     (c) Delete S5's `fp:` branch from `_answerable_by_decision_resolve` and
     report that `tests/orchestration/test_decision_inbox.py` turns RED at exit
     1. For each, name which tests failed — do not predict the names, report
     what you observed. IF ANY MUTATION LEAVES ITS SUITE GREEN, that is a
     finding for the handback and the round hands back on it: a guard that
     survives the deletion of what it guards is not a guard.
 G8. THE SUITES AND THE PATHS, at C8, SERIALLY in the primary checkout, one
     pytest process at a time, each with its REAL exit code and count. Every
     figure below was measured by the reviewer at `20eabead`, not copied. The
     canary `tests/cli/test_golden_path.py` 42; `tests/ui_server/` 480 at C8
     — that is 479 passing plus the guard S1 repairs — RISING by exactly S3's
     and S4's six new tests, which you state as a number;
     `tests/orchestration/test_test_runner.py` 52;
     `tests/regression/test_resource_safety.py` 21;
     `tests/orchestration/test_integrity_gate.py` 16;
     `tests/ui_contracts/` 561 passed with 4 skipped and UNCHANGED;
     `tests/orchestration/test_decision_inbox.py` 34, rising by exactly S8's
     one test; `tests/orchestration/test_bundled_clarification.py` 38 and
     UNCHANGED; `tests/cli/test_decision_answers.py` 29 and UNCHANGED;
     `tests/cli/test_plan_approval.py` 27 and UNCHANGED. The last four are
     ordered because they read the same payload and the same CLI path this
     feature has been changing: if any of them moves, say so and hand back.
     Then the browser side: `npx tsc --noEmit` and `npx vitest run`, each with
     its REAL exit code, reporting file and test counts — 30 files and 454
     tests at `20eabead` — with the count rising by exactly S9's one test.
     Finally: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C3 and
     `.agent/decisions.md` at C4, against a CONTROL count over the C0a blob
     which is not 0; compare the path set of
     `git diff --name-only 20eabead..C8` BOTH WAYS against the Change line's
     list MINUS `.agent/handoff.md` — excluded because the handback is written
     at C9, outside a range ending at C8 — and report both residues EMPTY;
     report each commit's insertions from `git diff --numstat`, each
     single-parent and under 500; `git ls-files .remedy-wt` 0 and
     `git worktree list` 1 line; and the reflog FOR THIS ROUND'S OWN COMMITS
     ONLY, every operation prefix reading `commit`, with `amend`, `rebase` and
     `cherry` 0 each among those entries. Do not count those words over the
     whole reflog.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C9: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G8, the item-status table covering C0a,
             C0b, C1 through C8, C9 and the push, ONE LINE PER GATE for G1
             through G8 with its real exit code, an explicit line saying the
             branch tip was RED at `20eabead` and is GREEN at C8 with the
             measured counts on both sides, the open-findings count, and the
             next expected action. Derive your line cap from AGENTS.md
             yourself, from the commit count you actually made; if the mandated
             content genuinely does not fit, declare the DECISION D15 overage
             with its stated cause and name the mandated content that caused
             it. Then push with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R48
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
R48 finishes R47 and repairs it. R47 landed the door's `fp:` dispatch and the
`approve`/`reject` options but left `tests/ui_server/` RED on an import guard
its block never widened, and never reached the door's tests, the answerability
mirror or the browser proof. R48 registers the three defects — all three in the
reviewer's block, not in the worker's execution — greens the tip, then lands
the three missing pieces.

## Next Steps
1. R49: the clarification FORM over `payload.clarifications`, which is what lets
   an operator answer a question instead of accepting its default.
2. A reviewer-file round landing the §3 checklist item R-0694 through R-0699 now
   share: a block reads the TARGET before ordering anything against it — every
   guard whose ruled set the change widens, every constant a test compares
   against, and every fixture whose state decides an outcome.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR
  once this round lands. R-0693 measures the gap and names `fp:` as the one
  R47 and R48 close between them; the rest are outside F031's scope, and the
  inbox tells the truth about every one of them.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R49 is where an operator gains any other choice.
- SIX CONSECUTIVE ROUNDS HAVE NOW RAISED A REVIEWER-SPEC DEFECT with one root
  cause — a block ordering something against a file it had not read. Step 2
  above is the fix and it is the highest-value work left in this feature.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 251 at `20eabead`
  and this round takes it to 254.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R48

<<<SLICE FINDINGS48
- R-0697 — High, A BLOCK ORDERED TWO NEW IMPORTS INTO THE WRITE DOOR AND DID NOT WIDEN THE EQUALITY GUARD THAT PINS THE DOOR'S IMPORT SET, SO THE BRANCH TIP SHIPPED RED. Raised by the reviewer at the R47 gate against its OWN R47 block, and reported by the worker before the reviewer reached it. THE MEASUREMENT, read at `20eabead`: `python3 -m pytest tests/ui_server/ -q` exits 1 with 1 failed and 479 passed, the single failure being `tests/ui_server/test_command_channel.py::TestCommandDoorImportGuard::test_the_door_imports_exactly_the_allowed_set`, whose assertion message names the two unruled entries `('packages.orchestration.flight_plan', 'open_clarification_questions')` and `('packages.orchestration.flight_plan', 'resolve_flight_plan_approval')` with `vanished` empty. THE CAUSE IS IN THE BLOCK, NOT IN THE ROUND: R47's SPEC items S1 and S3 ordered the door to import and call `resolve_flight_plan_approval` and `open_clarification_questions`, and that guard's own comment states that every allowed entry is there "because a ruled DECISION puts it there" and that adding one "belongs in the same commit as the decision that widens it" — so the block owed C6 those two entries and never named them, because it never read `tests/ui_server/test_command_channel.py`. HIGH BECAUSE THE TIP IS RED AND WAS PUSHED: a branch whose suite fails is not reviewable, and every later round on it starts from a red baseline that masks the next real failure. THE WORKER'S CONDUCT WAS CORRECT AND IS THE REASON THIS COST ONE ROUND RATHER THAN A SILENT WEAKENING: constraint 9 of that block forbade editing a test to clear an unexpected red, so it stopped, reported the guard and its exact assertion output, and handed back with the round unfinished rather than widening the set on its own authority. THE FIX IS TO ADD THE TWO ENTRIES WITH DECISION F031 D24 NAMED AS THEIR RULING, which is the mechanism the guard documents rather than an exception to it, and it lands at R48 C5.

- R-0698 — Medium, A BLOCK ORDERED A PREDICATE'S BEHAVIOUR CHANGED WITHOUT ORDERING THE CONSTANT A PARAMETRIZED TEST COMPARES THAT PREDICATE AGAINST. Raised by the reviewer at the R47 gate against its OWN R47 block, after the worker measured it and correctly declined to commit the change. THE MEASUREMENT: `tests/orchestration/test_decision_inbox.py` defines `ANSWERABLE_DECISION_TYPES = ("task_decision",)` at line 46 and `test_answerable_key_matches_what_the_write_door_accepts` is parametrized over all eight producing types, asserting each card's `answerable_by_decision_resolve` equals whether its type is in that tuple; `_fixture_flight_plan_approval` at line 135 builds `{"_approval": "pending"}`, which the door accepts once R47's C6 landed, so R47's S10 mirror would have turned the `flight_plan_approval` parameter red. THE CAUSE IS THE SAME AS R-0697's: the block ordered a change against a file it had not read. THE WORKER'S ANALYSIS WENT ONE STEP FURTHER THAN THE FACTS SUPPORT and the reviewer records the correction here rather than leaving it in a handback: it reported that a per-type tuple "cannot express fp answerability at all" because a resolved `fp:approval` card carries the same type. That reasoning would apply equally to `task_decision`, which the tuple already holds — and the file already answers it. The tuple is compared only against the card each PRODUCING FIXTURE builds, and the resolved transition is pinned separately by `test_answerable_key_goes_false_once_the_decision_has_been_answered`, whose docstring says in as many words that a type check cannot tell the two states apart and that this is why the transition gets its own test. MEDIUM RATHER THAN HIGH because nothing landed and nothing was lost: the worker reverted its working-tree edit, committed nothing, and the branch carries no trace of it. THE FIX IS A TUPLE ENTRY, A REWRITTEN COMMENT AND A SIBLING TEST FOR THE RESOLVED CASE, landing together at R48 C7.

- R-0699 — Medium, A BLOCK'S COMMIT BUNDLE GAVE PRODUCTION CODE A SLOT AND ITS TESTS NONE, SO THE DISPATCH LANDED UNTESTED. Raised by the reviewer at the R47 gate against its OWN R47 block. THE MEASUREMENT, read at `20eabead`: `git diff --name-only a73c137e..HEAD` holds ten paths and not one is under `tests/ui_server/`, while `git show d69a1bfb --stat` shows R47's C6 changing `packages/orchestration/ui_server.py` alone at 46 insertions. So the door's whole `fp:` branch — two refusal conditions, one effect call and one response body — sits on the branch with no test naming it. THE CAUSE IS AN INTERNAL DISAGREEMENT IN THE BLOCK: its Bundle line described C6 as "the door's `fp:` dispatch" and gave no commit to S12's tests, while SPEC item S12 described six tests across two files; the worker followed the Bundle, which is the enumeration that told it when to commit. A block whose bundle and whose spec describe different work is a block that will be executed twice differently. THIS ALSO COST THE ROUND ITS RED CONTROL: R47's G7 ordered a mutation of the door's refusal clause and expected `tests/ui_server/` to turn red, which no test on the branch could have made happen — so the gate that exists to prove the guards are load-bearing had nothing to bite on and was never run. MEDIUM BECAUSE THE CODE IS CORRECT AS FAR AS THE REVIEWER CAN READ IT — the diff was read line by line at the gate and implements its spec faithfully — but "correct as read" is exactly the claim this repository does not accept in place of a run. THE FIX IS THE SIX TESTS, split across the two `tests/ui_server/` files by the boundary their own docstrings draw, landing at R48 C6, with R48's G7 running the red control R47 could not.
<<<END FINDINGS48

<<<SLICE LEDGER48
Gate: F031 R47 — the F031 R47 entry. R47 FAILED, IT LEFT THE BRANCH TIP RED, AND ALL THREE DEFECTS ARE THE REVIEWER'S OWN BLOCK RATHER THAN THE WORKER'S EXECUTION — registered in the same round as R-0697, R-0698 and R-0699. WHAT THE WORKER GOT RIGHT, stated first because it is the reason this cost one round and not a corrupted suite: transport verified before it acted, at sha256 `77cfe894…65c2d8` over 34685 bytes and 435 lines; the fixed commit order honoured; every slice applied byte for byte; and, when `tests/ui_server/` turned red on a guard the block had not mentioned, it stopped, reported the exact assertion output, reverted its uncommitted working-tree edit for the item it could not satisfy, and handed back with the round unfinished — which is precisely what constraint 9 asked of it and the opposite of what a weakened assertion would have looked like. It also volunteered a process lesson the reviewer has adopted as a standing constraint: it had committed the door's code before running the suite that gates it, and running the suite first would have caught the guard one commit earlier. WHAT LANDED AND WAS VERIFIED BY THE REVIEWER OFF DISK: ten commits `d003c4f1` through `20eabead`, each single-parent; C4 `8037f052` retiring the duplicate guard at 11 deletions, leaving `tests/ui_contracts/` at 561 passed with 4 skipped, exactly the 562 the reviewer measured at `a73c137e` minus one; C6 `d69a1bfb` implementing the door's `fp:` branch, whose diff the reviewer read line by line and found faithful to S1 through S6 — the branch sits before `answer_task_decision`, refuses on exactly the two ruled conditions with strict equality against `approve` and `reject`, calls `resolve_flight_plan_approval` with `answers={}` and the open questions, deliberately omits `save_job` with a comment saying why and citing the two lines in `flight_plan.py` that save, and returns the same three keys the task-decision path returns; and C7 `c4bad853` adding `options` to the pending arm alone with both of the ruled exact-equality assertions in `tests/orchestration/test_bundled_clarification.py` updated to the new truth and neither loosened. THE LEDGER MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 27 to 28 with the added key `F031 R46`, `^Done: R-\d+ — ` 5 to 6 with the added id `R-0696`, `^## DECISION F031 D\d+ ` 23 to 24, open set 252 to 251, and the must-not-move sets did not move. WHAT DID NOT LAND: C8 and C9 were never made, so `packages/orchestration/decision_inbox.py`, `tests/orchestration/test_decision_inbox.py`, `apps/ui/src/api/decisionCard.test.ts` and both `tests/ui_server/` files are untouched across the whole range — the reviewer confirmed each with `git diff --name-only` rather than reading it back from the handback. THE TIP IS RED AND THE REVIEWER RE-RAN IT ITSELF: `tests/ui_server/` exits 1 at `20eabead` with 1 failed and 479 passed, the failure being the door's import guard, and the reviewer read the full failure output rather than the summary line. ONE PROCEDURAL QUESTION THE WORKER ESCALATED IS RULED IN DECISION F031 D25 rather than left in a handback: AGENTS.md's "If Blocked" wants the blocker written into `.agent/plan.md`, while the block reserved that file's text to the reviewer, and the worker obeyed the block and said so instead of choosing silently. AGENTS.md wins, it says so itself, and D25 carves out the exception so the next early hand-back has an answer. THE HANDBACK IS 185 LINES against the 100-line tier, declared as a DECISION D15 stated-cause overage with its cause named; the reviewer accepts the declaration for a round that had to carry two findings, a partial gate table and a blocked-round narrative, and notes that a shorter round would not have earned it. NO BLOCK CONDITION AROSE FROM THE WORKER: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. The verdict is FAIL, the repair is R48, and the lesson is the one the last six rounds have all taught.
<<<END LEDGER48

<<<SLICE DECISION25
## DECISION F031 D25 (2026-08-27) — a worker handing back early writes the blocker into the plan, and the reviewer's slice does not stop it

THE CONFLICT R47 SURFACED, escalated by the worker rather than resolved
silently, which is why it is being ruled at all: AGENTS.md's "If Blocked"
section orders the agent to "update `.agent/plan.md` with the exact blocker",
while R47's block constrained every slice — `.agent/plan.md` among them — to be
the reviewer's text applied byte for byte and never edited. A worker that hands
back mid-round therefore had two instructions it could not both obey.

CHOSEN, AGENTS.md WINS AND THE CARVE-OUT IS EXPLICIT. AGENTS.md states that it
has the highest priority and that conflicting files lose, so the question was
already answered in principle; what was missing was permission specific enough
that a worker under a byte-for-byte constraint could act on it. A worker ending
a round early MAY append a section headed `## Blocked` to `.agent/plan.md`,
after every section the reviewer's slice supplied, naming what stopped it and
which ordered items it did and did not complete. It never edits the reviewer's
text above that section, and the next round's slice replaces the whole file
including the appended section.

WHY APPEND RATHER THAN EDIT: the transport proof for a plan slice is a
byte-for-byte comparison against the reviewer's original, and an edit inside it
destroys that proof for no gain. An append leaves the original bytes intact as a
prefix, so the same comparison still runs — against the file's first N bytes —
and the blocker still reaches the next session through the file AGENTS.md names
as the bridge.

CONSIDERED AND REJECTED: leaving the blocker in the handback alone, which is
what R47 did. It works only while `handoff.md` survives, and `plan.md` is the
file the Session Resume protocol reads second and the one AGENTS.md calls the
bridge. Two files disagreeing about whether a round finished is the state this
repository has paid for before.

REVERSE IT by deleting this entry and the `## Blocked` carve-out from the block
template, which returns the worker to reporting blockers in the handback only.
<<<END DECISION25
