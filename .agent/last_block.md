── STEP CODE ROUND / F031 — ROUND R47 ─────────────────────────────────
Goal:        Make the flight-plan approval answerable THROUGH THE WRITE DOOR —
             the half of DECISION F009 D5 that was planned and never shipped —
             and retire the duplicate contract guard R-0696 names. When this
             round ends, `grep resolve_flight_plan_approval
             packages/orchestration/ui_server.py` returns a line, an `fp:`
             card's answer strip offers the two words the door accepts, and
             `answerable_by_decision_resolve` is TRUE for exactly the cards the
             door would take.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the R46 verdict · C3 DECISION F031 D24 · C4 retire the
             duplicate guard · C5 the `Done:` line for R-0696 · C6 the door's
             `fp:` dispatch · C7 the `options` payload · C8 the predicate
             mirror · C9 the browser-side proof · C10 handback · then push.
Change:      Exactly these paths, nothing else.
             `.agent/authored/f031-r47.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md`,
             `.agent/handoff.md`, `packages/orchestration/ui_server.py`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_inbox.py`,
             `tests/ui_contracts/test_decision_answer_wiring.py`,
             `tests/ui_server/test_command_channel.py`,
             `tests/ui_server/test_command_dispatch.py`,
             `tests/orchestration/test_decision_inbox.py`,
             `tests/orchestration/test_bundled_clarification.py`,
             `apps/ui/src/api/decisionCard.test.ts`.
             NO FILE UNDER `docs/` CHANGES and that is checked, not assumed:
             the reviewer grepped `docs/` for `decision.resolve`,
             `_dispatch_decision_resolve`, `write door` and `write channel`
             and every hit outside `docs/roadmap/` was
             `docs/ui/design_reference/codebase_audit.md`, which does not name
             this command at all. No ist-doc holds a dispatch table this round
             would make stale.
             THE TWO `tests/ui_server/` FILES ARE BOTH LISTED BECAUSE THE REPO
             SPLITS THEM ON PURPOSE, and S12 obeys that split rather than
             inventing one. `test_command_dispatch.py`'s own module docstring
             states the boundary: its sibling `test_command_channel.py` "pins
             what the door ANSWERS", while it pins "the three writes DECISION
             F009 D18 orders behind that answer". Putting all of S12 in one
             file would collapse a distinction that file says exists so that a
             right status over an effect that never ran stays detectable.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. Slices are `.agent/` text ONLY. The production code below is
    DESCRIBED as a numbered SPEC, not sliced: you write that code yourself,
    reading each named file before you touch it, and AGENTS.md's file-editing
    safety rules bind every one of those edits.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6, C7, C8, C9,
    C10. Two orderings are load-bearing and neither may be swapped. C5's
    `Done:` line asserts a deletion that C4 makes, so it lands AFTER it. C8
    flips the predicate to TRUE for `fp:` cards, and it lands AFTER C6 gives
    the door something to accept and AFTER C7 gives the browser a value it can
    post — a predicate that turns true first would re-ship R-0693's enabled
    button for the length of two commits.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R46. That is
    ordered: the plan becomes current at C1.
 4. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own, never edit a finding's wording, never edit D24. If the SPEC reads
    wrong to you, say so in the handback and implement it as written anyway —
    except where item 9 applies.
 5. THE LEDGER SETS MOVE EXACTLY THREE TIMES. Across C2 `^Gate: F\d+ R\d+ — `
    moves 27 to 28 with the ADDED key exactly `F031 R46`. Across C3
    `^## DECISION F031 D\d+ ` moves 23 to 24. Across C5 `^Done: R-\d+ — `
    moves 5 to 6 with the ADDED id exactly `R-0696`. Across the WHOLE round
    `^- R-\d+ — ` stays 257, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 252 before C2 and 251 after C5.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C10. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP. Never create it, never delete it.
 7. NOTHING UNDER `.remedy-wt/` IS EVER COMMITTED and `git status --porcelain`
    reads 0 lines at every commit. `.remedy-wt/f031-r47-block.md` is the
    reviewer's scratch copy — leave it alone, do not delete it. Any red-proof
    or mutation you choose to run for your own confidence runs in a disposable
    `git worktree` and never in the primary checkout; if you create one, remove
    it before C10 and say so in the handback.
 8. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, and copy with `shutil.copyfile`. Keep
    each heredoc modest in size. Run pytest SERIALLY — never two pytest
    processes alive at once.
 9. NEVER WEAKEN AN ASSERTION TO MAKE A GATE GREEN. S9 changes two existing
    assertions and it is the only such change this block orders; both stay
    EXACT equality. If any other existing test turns red, that is a finding to
    report in the handback, not a test to edit — stop, write the handback and
    hand back, because a red you were not told to expect is exactly the
    ambiguity G8 of the self-drive protocol ends the round on.

SPEC — the production code. Read each file before editing it.
 S1. `packages/orchestration/ui_server.py::_dispatch_decision_resolve` gains an
     `fp:` branch taken BEFORE the existing `answer_task_decision` call,
     entered when the `decision_id` it already reads from `args` starts with
     `fp:`. Nothing else in that method changes: the `args` degradation rules
     its docstring states, the task-decision path, and the return shape all
     stay as they are.
 S2. THE BRANCH REFUSES BY RETURNING None, which the caller already answers 409
     `rejected_state` at `ui_server.py:3632`, in exactly two cases, and it
     refuses in NO other case. (a) `job.flight_plan` is not a dict, or its
     `_approval` is not the string `"pending"`. (b) The `answer` read from
     `args` is not exactly `"approve"` or exactly `"reject"` — strict equality
     against those two literals, NO case folding and NO trimming, mirroring
     `apps/cli/commands/decision.py:299`, which the reviewer read and which
     compares `reason not in ("approve", "reject")`.
 S3. ON ACCEPTANCE the branch calls
     `flight_plan.resolve_flight_plan_approval(job, reason=<the answer>,
     answers={}, questions=<the open questions>)`, where the questions come
     from `flight_plan.open_clarification_questions(fp.get(
     "clarifications_resolved"))` — the same call
     `apps/cli/commands/decision.py:308` makes. IT DOES NOT CALL `save_job`.
     That is not an omission: `resolve_flight_plan_approval` calls `save_job`
     itself on both of its arms, at `packages/orchestration/flight_plan.py:824`
     and `:831`, which the reviewer read. A second save would write the same
     object twice. Put that reason in a comment where a reader searching for
     the missing `save_job` will land, because the task-decision branch three
     lines away DOES call it and the difference will otherwise read as a bug.
 S4. `answers={}` IS DELIBERATE AND DECISION F031 D24 RULES IT: through this
     door every open clarification takes its own `default_answer`. The
     docstring says that in plain words — an operator approving from the inbox
     is accepting the defaults — and names R48 as where a FORM gives them any
     other choice. Do not invent a way to pass answers here.
 S5. THE ACCEPTED BODY is `{"command": payload["command"], "outcome":
     "accepted", "decision_id": <the id as a string>}` — the same three keys
     the task-decision return already builds, so the client sees one shape.
 S6. `--as-mission` IS DELIBERATELY NOT REACHABLE THROUGH THIS DOOR, and the
     docstring says so where a reader would search for it: F056 makes the
     mission opt-in an explicit flag whose default is NO, so a door that
     cannot carry the flag creates no mission and silently creating one would
     be the opposite of that default.
 S7. `packages/orchestration/decision_queue.py`, in the PENDING arm of branch 7
     ONLY — the `_fp_approval == "pending"` block that begins at line 246 —
     sets `_payload["options"] = ["approve", "reject"]` unconditionally,
     before the `HumanDecision` is constructed. THE RESOLVED ARM AT LINE 299 IS
     UNTOUCHED: a resolved plan offers nothing to answer.
 S8. `options` IS NOT A NEW VOCABULARY, and the one-line WHY comment above S7's
     assignment says so: branch 8 already exports an `"options"` key in its
     payload at line 356, and `apps/ui/src/api/decisionCard.ts::decisionAnswers`
     prefers `payload.options` over `next_actions` for EVERY card without
     branching on the card's type. That preference is why S7 is the entire
     browser-side production change — the answer strip becomes two
     `kind: "option"` affordances whose values are exactly the two literals S2
     accepts, and no `.tsx` or non-test `.ts` file is edited this round.
 S9. `tests/orchestration/test_bundled_clarification.py` asserts
     `bundled.payload == {}` at line 385 and `d.payload == {}` at line 406 for
     a pending fp decision. BOTH become the same EXACT equality against the new
     truth, `== {"options": ["approve", "reject"]}`. Neither test's intent
     changes, neither assertion is loosened, and neither may become a subset
     check, an `in`, or a key-count assertion. These two lines are the only
     existing assertions this block orders changed.
S10. `packages/orchestration/decision_inbox.py::_answerable_by_decision_resolve`
     gains the mirror of S2: an id starting `fp:` is answerable if and only if
     `job.flight_plan` is a dict whose `_approval` is `"pending"` — the SAME
     two conditions, read the same way. Ids that do not start `fp:` keep the
     existing `find_task_decision` plus open-status read, unchanged.
S11. S10 IS NOT THE `card.type` BRANCH THAT DOCSTRING FORBIDS, and it must say
     why in one sentence, because the next reader will think it is: the door
     itself dispatches on the ID PREFIX, so mirroring the door means reading
     the prefix. A type branch would read `flight_plan_approval` — which the
     RESOLVED card also carries while the door refuses it — and would be wrong
     for exactly the reason the existing note about answered task decisions
     gives.
S12. TESTS FOR THE DOOR, SPLIT ACROSS THE TWO FILES BY THE BOUNDARY THEIR OWN
     DOCSTRINGS DRAW. In `tests/ui_server/test_command_channel.py`, which pins
     WHAT THE DOOR ANSWERS: an approval answered 200 with S5's three keys; a
     rejection answered the same; a plan that is not pending answered 409 with
     a `rejected_state` audit line; and an `answer` that is neither literal
     answered 409 with that same audit line — for that last one use the full
     CLI line `remedy decision resolve <id> fp:approval --reason approve`,
     because that is precisely what R-0693 measured the browser posting before
     this round, so the test pins the old bug shut. In
     `tests/ui_server/test_command_dispatch.py`, which pins THE EFFECT BEHIND
     the answer: one test that an accepted approval really reached
     `resolve_flight_plan_approval` and left the plan `_approval` reading
     `approved` on disk, and one that `save_job` ran EXACTLY ONCE for it —
     that count being the only guard on S3's deliberate omission, and a
     guard that belongs in the effect file rather than the answer file.
S13. TESTS FOR THE PREDICATE, in `tests/orchestration/test_decision_inbox.py`:
     a pending flight plan gives `answerable_by_decision_resolve` TRUE on the
     `fp:approval` card; an approved plan gives FALSE on the resolved
     `fp:approval` card; and the existing task-decision cases still read as
     they did, which you confirm by the suite count rather than by editing
     them.
S14. THE BROWSER-SIDE PROOF, one test in `apps/ui/src/api/decisionCard.test.ts`:
     feed `decisionAnswers` a card shaped like the endpoint's PENDING
     `fp:approval` — `payload` carrying `options: ["approve", "reject"]` and
     `answerable_by_decision_resolve: true` — and assert it gives EXACTLY two
     answers, both `kind: "option"`, with values `approve` then `reject` in
     that order, each carrying `posts: true`. This is the only evidence
     available that the browser half of this round works, because no DOM
     harness reaches the component.
S15. C4 RETIRES THE DUPLICATE R-0696 NAMES by deleting the function
     `test_the_region_after_the_button_still_carries_no_conditional_operator`
     from `tests/ui_contracts/test_decision_answer_wiring.py`, where it begins
     at line 457. KEEP `test_the_region_is_created_under_no_conditional_operator_at_all`
     at line 285. The reviewer measured which is which rather than guessing:
     `git log -S` puts the keeper in `05bdeae1` and the deleted one in
     `9236e617`, the R45 commit, so the NEWER is retired exactly as §3 item 30
     rules for a duplicate. Delete the function and its body and the blank line
     that separated it from its neighbour, and nothing else in that file — the
     shared reader `jsx_between_answer_button_and_live_paragraph` at line 95
     STAYS, because the keeper calls it.

Done when — run every gate yourself and record its REAL exit code. G1 through G9
run at commits STRICTLY EARLIER than C10, so the handback can quote them; the
push is ordered after C10 and its reading is NOT written into the handback.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after every commit from C0a to C9.
     `.agent/STOP` read from disk before C0a and before C10, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at
     C0a, as mirrored at C0b, and as read off disk at C9 — all three must be
     EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE must be at most 400 and
     TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R47 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with
     `git show <rev>:<path>` into memory; never write a past blob over a
     tracked file to read it. `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus LEDGER47; `.agent/decisions.md` at
     C3 equals ITS pre-commit blob plus ONE newline plus DECISION24;
     `.agent/live_review.md` at C5 equals whatever C2 left plus ONE newline
     plus DONE696, which you READ rather than take from this block. The
     reviewer measured the two BASE blobs at `a73c137e` itself:
     `.agent/live_review.md` is 863212 bytes and `.agent/decisions.md` is
     608934. If either reads differently before C2 or C3, something moved that
     this round did not order — stop and hand back. For EACH append report both
     byte counts and the sum. Then confirm EACH with a
     SECOND, independent reader: split the whole file on blank lines, let N be
     the number of paragraphs YOUR SCRIPT COUNTS in that slice — never a number
     this block asserts — and compare the LAST N units of the file against the
     slice's N paragraphs IN ORDER. Report N and the unit count before and
     after for each. THE NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH,
     which is the position a tail-only reading cannot see: flip ONE byte IN
     MEMORY inside paragraph 1 of each slice and report that BOTH readers
     REJECT it. For any slice whose N is 1, say so and note that paragraph 1 is
     also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at four points — before C2, after C2, after C3,
     after C5 — the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     and gate keys ADDED and REMOVED as SETS at each step, whether all ids are
     DISTINCT, and the maximum id. Every movement constraint 5 names is checked
     here, INCLUDING the ones that must NOT move. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C5. Also report
     `^## DECISION F031 D\d+ ` in `.agent/decisions.md` before and after C3.
 G6. THE DUPLICATE IS GONE AND ITS NEIGHBOUR IS NOT. At C4 report, over
     `tests/ui_contracts/test_decision_answer_wiring.py`, the line-anchored
     count of `^    def test_` before and after, the SET of names REMOVED and
     the SET ADDED, and confirm REMOVED is exactly
     {`test_the_region_after_the_button_still_carries_no_conditional_operator`}
     and ADDED is EMPTY. The reviewer counted the deleted name in that file at
     `a73c137e` with its own script and it reads 1, so the deletion has a
     single target and cannot take a neighbour with it. Confirm
     `jsx_between_answer_button_and_live_paragraph` is still DEFINED and still
     CALLED: the reviewer counted that name at `a73c137e` and it reads 3 — one
     definition and two calls — so it must read exactly 2 at C4. Then run
     `python3 -m pytest tests/ui_contracts/ -q` and report the real exit code
     and count: it reads 562 passed with 4 skipped at `a73c137e`, measured by
     the reviewer, and must read 561 passed with 4 skipped at C4. A different
     number means you deleted something else — stop and hand back.
 G7. THE DOOR AND THE PREDICATE, PROVED BY A RED CONTROL, NOT BY A GREEN COUNT.
     At C9, in a DISPOSABLE WORKTREE and never in the primary checkout, make
     the door's `fp:` branch accept ANY answer string — that is, delete S2's
     clause (b) alone — and report that `tests/ui_server/` turns RED at a real
     exit code of 1, naming which tests fail. Restore, then in the same
     worktree make `_answerable_by_decision_resolve` return the OLD value for
     `fp:` ids — that is, delete S10's branch alone — and report that
     `tests/orchestration/test_decision_inbox.py` turns RED at a real exit code
     of 1, naming which tests fail. Report the colour of each mutation as a
     REAL exit code, never as a word, and confirm the worktree is removed
     afterwards and `git worktree list` is back to 1 line. If EITHER mutation
     leaves its suite GREEN, that is a finding to report in the handback and
     the round hands back on it: a guard that survives the deletion of what it
     guards is not a guard.
     BOTH MUTATIONS ARE NAMED SEMANTICALLY — "S2's clause (b)", "S10's branch"
     — rather than as a byte string with a measured occurrence count, and that
     is deliberate rather than an omission of the standing rule for destructive
     controls. That rule binds a control that deletes or replaces bytes in an
     EXISTING file at a known SHA, where the reviewer can count the target
     itself; here the target is code THIS ROUND writes, so no such count can
     exist when this block is written. You supply it instead: before each
     mutation, report the exact lines you removed and confirm you removed
     nothing else.
 G8. THE SUITES, SERIALLY, IN THE PRIMARY CHECKOUT AT C9, one pytest process at
     a time, each with its REAL exit code and count. The canary
     `tests/cli/test_golden_path.py` 42; `tests/ui_server/` 480 at `a73c137e`
     and HIGHER at C9 by exactly S12's new tests, which you state as a number;
     `tests/orchestration/test_test_runner.py` 52;
     `tests/regression/test_resource_safety.py` 21;
     `tests/orchestration/test_integrity_gate.py` 16;
     `tests/orchestration/test_decision_inbox.py` 34 at `a73c137e` and higher
     at C9 by exactly S13's new tests; `tests/orchestration/test_bundled_clarification.py`
     38 and UNCHANGED at 38, because S9 edits two assertions and adds no test;
     `tests/cli/test_decision_answers.py` 29 and UNCHANGED;
     `tests/cli/test_plan_approval.py` 27 and UNCHANGED. Every one of those
     `a73c137e` readings was measured by the reviewer, not copied. The last
     three are ordered BECAUSE S7 changes a payload the CLI path also reads: if
     any of them moves, S7 changed CLI semantics, which `.agent/context.md`
     forbids, and that is a hand-back. Then the browser side at C9: `npx tsc
     --noEmit` and `npx vitest run`, each with its REAL exit code, reporting
     the file and test counts — 30 files and 454 tests at `a73c137e` — and the
     count must rise by exactly S14's one test.
 G9. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C5 and
     `.agent/decisions.md` at C3, against a CONTROL count over the C0a blob,
     which is not 0. Compare the path set of `git diff --name-only a73c137e..C9`
     BOTH WAYS against this round's expected set and report both residues,
     which must BOTH be EMPTY. THE EXPECTED SET FOR THAT RANGE IS THE CHANGE
     LINE'S LIST MINUS `.agent/handoff.md`, and the exclusion is the point of
     saying so: the handback is written at C10, which is OUTSIDE a range
     ending at C9, so an expected set that kept it would leave a residue that
     is not a defect and would read as one.
     Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and under 500. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C9.
     Report the reflog FOR THIS ROUND'S OWN COMMITS ONLY: every operation
     prefix must read `commit`, and among those entries `amend`, `rebase` and
     `cherry` must be 0 each. Do not count those words over the whole reflog,
     which holds this repository's entire history and is not what this gate
     asks.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C10: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G9, the item-status table covering
             C0a, C0b and C1 through C9, C10 and the push, ONE LINE PER GATE
             for G1 through G9 with its real exit code, an explicit line naming
             R-0696 as FIXED at C4 and recorded at C5, the open-findings count,
             and the next expected action. Say plainly how S12's tests split
             across the two `tests/ui_server/` files and why. Derive
             your line cap from AGENTS.md yourself, from the commit count you
             actually made; if the mandated content genuinely does not fit,
             declare the DECISION D15 overage with its stated cause. Then push
             with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R47
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D24.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R47 makes the flight-plan approval answerable through the write door, which is
the half of DECISION F009 D5 that was planned and never shipped: the door
dispatches an `fp:`-prefixed id to `flight_plan.resolve_flight_plan_approval`,
the pending decision carries `approve` and `reject` as payload options, and
`_answerable_by_decision_resolve` mirrors the door's own two conditions. The
round also retires the duplicate contract guard R-0696 named.

## Next Steps
1. R48: the clarification FORM over `payload.clarifications`, which is what lets
   an operator answer a question instead of accepting its default.
2. A reviewer-file round landing the §3 checklist item R-0694, R-0695 and R-0696
   share: a block reads the TARGET — a predicate's refusal conditions, a test
   file's existing guards, a payload's exact-equality assertions — before
   ordering anything against it.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR
  once this round lands. R-0693 measures the gap and names `fp:` as the one
  round R47 closes; the rest are outside F031's scope, and the inbox tells the
  truth about every one of them rather than offering a button that is refused.
- APPROVING FROM THE INBOX ACCEPTS EVERY CLARIFICATION DEFAULT. DECISION F031
  D24 rules that and R48 is where an operator gains any other choice; the
  endpoint says so in its own docstring and nothing in the browser claims more.
- NO DOM HARNESS REACHES THE INBOX MARKUP, so the browser half is evidenced
  only by `apps/ui/src/api/decisionCard.test.ts` over `decisionAnswers` and by
  the comment-stripped source guards in
  `tests/ui_contracts/test_decision_answer_wiring.py`.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 at `a73c137e`
  and this round takes it to 251.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R47

<<<SLICE LEDGER47
Gate: F031 R46 — the F031 R46 entry. R46 PASSED ON EVERY ONE OF ITS SEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM AVAILABLE TO THIS WORKFLOW for the fourth round running: the reviewer's OWN scratch original `.remedy-wt/f031-r46-block.md`, the C0a blob, the C0b blob, `.agent/last_block.md` at C4 and the same file read off disk are ALL FIVE byte-identical at sha256 `fdd7f22e…6f69b0` over 23159 bytes and 226 lines, with C0a and C0b resolving to the SAME git blob `bb822e3e`. THE EXTRACTION printed 4 slices, CONTENT 75 and TOTAL 226, so PROSE was 151 against 400 and TOTAL 226 against 490. THE PLAN at C1 is byte-equal to PLANF031R46 at 2814 bytes with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 48 against a cap that is STRICTLY under 50. THE THREE APPENDS ARE EXACT: 854809 + 1 + 2880 = 857690 and 857690 + 1 + 5521 = 863212 in the ledger, and 607381 + 1 + 1552 = 608934 in `.agent/decisions.md`; blank-line units 351 to 352, 352 to 353 and 1461 to 1466; N counted by the reviewer's own script at 1, 1 and 5, with the first two noted as slices whose paragraph 1 is also the last; both whole-file identities TRUE on all three, and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on all three. THE SETS MOVED ONLY WHERE CONSTRAINT 5 ALLOWED, AND THE ONES THAT MUST NOT MOVE DID NOT: `^- R-\d+ — ` 256 to 257 to 257 with the ADDED id across C2 exactly `R-0696` and NOTHING removed at either step; `^Done: R-\d+ — ` 5 at all three points, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; `^Gate: F\d+ R\d+ — ` 26 to 26 to 27 with the ADDED key across C3 exactly `F031 R45`; all ids DISTINCT with the maximum `R-0696`; open set 251 before C2 and 252 after C3; `^## DECISION F031 D\d+ ` 22 before C4 and 23 after. NOTHING EXECUTABLE MOVED AND THE REVIEWER PROVED IT RATHER THAN READING IT BACK: `git diff --name-only d53bdb9b..98e033e0` is 5 paths, every one beginning with `.agent/` and none outside it, and `git diff --stat` restricted to `apps/`, `packages/`, `tests/` and `docs/` is EMPTY for all four. THE FIVE SUITES A STATE REWRITE CAN BREAK WERE RE-RUN SERIALLY IN THE PRIMARY CHECKOUT, one pytest process at a time, each at a REAL exit code of 0: the canary `tests/cli/test_golden_path.py` 42, `tests/ui_server/` 480, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16 — every count equal to its `d53bdb9b` reading. MARKERS are 0 and 0 in all three written targets against a live CONTROL of 4 and 4 over the C0a blob, and the path set matches BOTH WAYS with both residues EMPTY. THE SEVEN COMMITS ARE EACH SINGLE-PARENT at insertions 226, 161, 27, 2, 2, 26 and 32, every one far under 500, and the six figures the handback tables agree cell for cell with `git diff --numstat` including the deletion column at -0, -273, -27, -0, -0 and -0; the reflog SCOPED to those seven entries reads `commit` on every one, so `amend`, `rebase` and `cherry` are 0 each among them; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE HANDBACK WAS AUDITED AS AN ARTIFACT: 75 lines against the 100-line tier seven tabled commits earn, one line per gate carrying a real exit code, an item-status table covering all eight ordered items, the plain statement that the round changed no executable file, the explicit R-0696 line saying it was registered and deliberately not fixed, the open count 252, and a next-action section naming Phase 1 rule 1 before the Open PR Gate exactly as the self-drive protocol requires. THE ONE THING THE HANDBACK DID NOT NUMBER IS THE ONE THING IT COULD NOT: C5's own `+/-` cell reads "per numstat" rather than a figure, which is correct rather than a lapse — a handoff cannot table the numstat of the commit that writes it, and inventing the number would have been the self-referential value §3 forbids. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. R46 put the R45 verdict, the finding it raised and the decision that re-numbered the programme on disk, which is the whole of what a record round owes.
<<<END LEDGER47

<<<SLICE DONE696
Done: R-0696 — FIXED at C4 of R47 by deleting `test_the_region_after_the_button_still_carries_no_conditional_operator` from `tests/ui_contracts/test_decision_answer_wiring.py`, retiring the NEWER of the pair exactly as §3 item 30 rules for a duplicate. The reviewer measured which was newer rather than assuming it: `git log -S` puts the surviving `test_the_region_is_created_under_no_conditional_operator_at_all` in `05bdeae1` and the deleted one in `9236e617`, the R45 commit whose item S10 ordered it. The shared reader `jsx_between_answer_button_and_live_paragraph` STAYS, because the keeper calls it, and the property is still pinned once. The root cause the finding names — three consecutive rounds ordering something against a file the block had not read — is NOT closed by this line: it closes when the §3 checklist gains the item, which the plan's step 2 carries.
<<<END DONE696

<<<SLICE DECISION24
## DECISION F031 D24 (2026-08-27) — the write door approves a flight plan on the defaults, and the inbox offers the two words the door takes

THE GAP DECISION F009 D5 LEFT: that entry rules that `decision.resolve`
dispatches "an `fp:`-prefixed id to `resolve_flight_plan_approval`, and the seam
is gone when that round ends". The extraction shipped and the dispatch did not,
which finding R-0693 measured — `resolve_flight_plan_approval` exists, its
docstring says it was extracted "so the UI write door can reach the SAME code
the CLI has always run", and the CLI remained its only caller.

CHOSEN, THE DOOR APPROVES ON THE DEFAULTS. The `fp:` branch passes
`answers={}`, so every open clarification takes its own `default_answer`. An
operator approving from the inbox is accepting the defaults, the endpoint's
docstring says exactly that, and R48's FORM over `payload.clarifications` is
where any other choice comes from. The alternative — holding the dispatch back
until the FORM exists — keeps a blocker decision unanswerable through the only
surface the operator has, to protect a choice that today's card cannot offer
anyway.

CHOSEN, THE ANSWER VOCABULARY IS THE CLI'S. The door accepts exactly `approve`
and `reject`, by strict equality, mirroring `apps/cli/commands/decision.py`'s
own `reason not in ("approve", "reject")`. The pending decision therefore
carries those two strings as `payload.options`, and `decisionAnswers` — which
prefers options over next actions for every card, without branching on type —
turns them into the card's affordances. That is why no component changes: the
browser already renders whatever the payload offers.

CONSIDERED AND REJECTED: parsing the `next_actions` CLI line the card used to
post. It would make the door reverse-engineer its own help text, and a
punctuation change in a printed hint would silently become a refused approval.

REVERSE IT by deleting the `fp:` branch from `_dispatch_decision_resolve`, the
`options` assignment from the pending arm of `decision_queue`, and the `fp:`
mirror from `_answerable_by_decision_resolve` — the three land as three commits
so that reversal is three reverts.
<<<END DECISION24
