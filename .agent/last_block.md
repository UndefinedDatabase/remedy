── STEP T001 the answerable key / F031 — ROUND R43 ────────────────────
Goal:        Land DECISION F031 D19's first clause — the read endpoint derives
             whether the write door can answer a card — with its tests and its
             red proofs, and record R42's verdict and the one finding its gate
             raised. Code round: one source file, one test file, plus state.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the finding · C3 the R42 gate entry · C4 DECISION F031 D20 ·
             C5 the endpoint key with its tests · C6 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r43.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `packages/orchestration/decision_inbox.py`,
             `tests/orchestration/test_decision_inbox.py`, `.agent/handoff.md`.
             NO FILE UNDER `apps/` and NO FILE UNDER `docs/` — the browser half
             is R44's and the feature file already carries D19's mirror.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof, and stopping
    early would lose the record this round exists to write.
 2. THE CODE IS DESCRIBED, NOT SLICED. Section S below is a numbered SPEC, not
    an authored text: you write the Python yourself to satisfy it, in the
    surrounding file's own idiom — module-level imports, a WHY docstring above
    each definition, `from __future__ import annotations` already present. The
    byte-for-byte rule of constraint 1 binds the five marked SLICES only.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The finding
    lands at C2 BEFORE the gate entry at C3. No pair may be reordered.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R42. That is
    ordered: the plan becomes current at C1.
 5. THE FINDING AND THE DECISION ARE THE REVIEWER'S TEXT. You never write a
    `Done:` paragraph, never edit a finding's wording, never edit D20. R-0694 is
    registered here and deliberately NOT fixed here: its repair is a new item in
    docs/agents/planner_reviewer_prompt.md §3, which is the reviewer's file and
    is not in this round's change set.
 6. THE LEDGER SETS MOVE ONCE EACH. Across C2 `^- R-\d+ — ` moves 254 to 255
    with the id ADDED exactly `R-0694` and none REMOVED. Across C3
    `^Gate: F\d+ R\d+ — ` moves 23 to 24 with the ADDED key exactly `F031 R42`.
    Across both, `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 249 before C2 and 250 after.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. Every mutation of gate G7 runs inside
    a disposable `git worktree` under `.remedy-wt/`, NEVER in the primary
    checkout, and the worktree is removed BY ITS EXACT PATH when G7 ends.
    Nothing under `.remedy-wt/` is ever committed, and
    `.remedy-wt/f031-r43-block.md` is the reviewer's scratch copy — leave it
    alone, do not delete it. `git status --porcelain` reads 0 lines at every
    commit, which is what isolation buys.
 9. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, build dicts with `dict(key=value)`, and
    copy with `shutil.copyfile`. Keep each heredoc modest in size.

S. THE SPEC for C5. Write both files to satisfy every numbered item; the item
numbers are the contract, the wording is not a text to copy.
 S1. In `packages/orchestration/decision_inbox.py`, add a module-level import of
     `find_task_decision` from `packages.orchestration.escalation`. It is
     acyclic: `escalation.py` imports nothing from `packages.orchestration` at
     module level, and `decision_queue` already pulls it in before this module
     loads.
 S2. Add a private helper `_answerable_by_decision_resolve(job, decision_id)`
     returning `bool`, defined as `find_task_decision(job, str(decision_id)) is
     not None` and NOTHING else. Its docstring carries the measurement, not a
     claim: `ui_server._dispatch_decision_resolve` calls
     `escalation.answer_task_decision` and nothing else, that function reaches a
     record only through `find_task_decision`, and `find_task_decision` iterates
     the job's ESCALATION RECORDS alone — so of the eight producing branches of
     `list_decisions` only `task_decision` mints an id that list holds. Finding
     R-0693 carries the measurement and DECISION F031 D19 rules the key.
 S3. The docstring ALSO records the deliberate absence, because a reader will
     search this file for it: Remedy deliberately does NOT branch on the card's
     `type` here, and no fixture in this repository can tell the two predicates
     apart — branch 8 derives its id FROM the escalation record, so type and
     door-answerability coincide on every buildable fixture. The door's own
     predicate is used because it is the door's rule, not because a test can
     currently catch the difference. Say that in as many words.
 S4. In `build_decision_inbox`, set a THIRD derived key on every card,
     `card["answerable_by_decision_resolve"]`, from S2's helper applied to the
     decision's own id. The two existing keys and their order are unchanged.
 S5. Sweep the file for every sentence the new key makes stale and correct each:
     the module docstring's "the two things a card needs", the
     `build_decision_inbox` docstring's "exactly two extra keys", and any other
     count of the additive keys the file states. Report in the handback how many
     such sentences you found and where — the reviewer will grep for the words
     `two` and `2` in that file and compare.
 S6. In `tests/orchestration/test_decision_inbox.py`, rename
     `test_card_keys_are_the_export_keys_plus_exactly_two` to say THREE, add the
     new key to that test's `expected` set, and correct the section comment
     above it, which states the same count in prose.
 S7. Add to that file a module-level `ANSWERABLE_DECISION_TYPES` naming the
     types the door can answer, and a test parametrized over the EXISTING
     `PRODUCING_DECISION_TYPES` asserting, for each type's own card, that
     `card["answerable_by_decision_resolve"]` equals `decision_type in
     ANSWERABLE_DECISION_TYPES`. Build no new fixture: the eight
     `PRODUCING_FIXTURES` already exist and the assertion must run against them.
     The reviewer measured every value against those same fixtures at
     `5b810e33`: `task_decision` alone is True.
 S8. Extend `test_card_appears_for_each_producing_type` with the presence of the
     new key and `isinstance(card["answerable_by_decision_resolve"], bool)`,
     beside the two presence assertions it already makes.
 S9. Nothing else changes in either file. No existing test is deleted, no
     assertion is weakened, no fixture is edited.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R43 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE THREE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus FINDINGS43; at C3 equals ITS pre-commit blob plus ONE
     newline plus LEDGER43; `.agent/decisions.md` at C4 equals its pre-commit
     blob plus ONE newline plus DECISION20. The pre-commit blob for C2 is 834598
     bytes and for C4 is 602495 bytes. For EACH append report both byte counts
     and the sum. Then confirm EACH with a SECOND, independent reader, and apply
     finding R-0631's fix clause rather than a tail-only check: split the whole
     file on blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS
     in that slice — never a number this block asserts — and compare the LAST N
     units of the file against the slice's N paragraphs IN ORDER. Report N and
     the unit count before and after for each. THE NEGATIVE CONTROL GOES ON THE
     FIRST APPENDED PARAGRAPH, which is the position a tail-only reading cannot
     see: flip ONE byte IN MEMORY inside paragraph 1 of each slice and report
     that BOTH readers REJECT it. For any slice whose N is 1, say so and note
     that paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     ADDED and REMOVED as SETS at each step, whether all ids are DISTINCT, and
     the maximum id. Every movement constraint 6 names is checked here. Report
     the open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after
     C3. Also report `^## DECISION F031 D\d+ ` in `.agent/decisions.md` as 19
     before C4 and 20 after.
 G6. THE SPEC, ITEM BY ITEM. For EACH of S1 through S9 report DONE or NOT DONE
     with the file and line where it landed. Then report, over
     `packages/orchestration/decision_inbox.py` at C5, every line containing the
     word `two` or the standalone numeral `2`, so the reviewer can see S5's
     sweep rather than take it on trust. Report `python3 -m ruff check` on both
     changed files at its REAL exit code, and the count of `assert` statements
     the test file holds before and after.
 G7. THE TESTS AND THEIR RED PROOFS. In the PRIMARY checkout at C5 run
     `python3 -m pytest tests/orchestration/test_decision_inbox.py -q` and
     report its REAL exit code and collected count; at `5b810e33` that file
     collects 25. Then, INSIDE A DISPOSABLE WORKTREE and never in the primary
     checkout, run TWO mutations, one at a time, restoring between them:
     (a) make `_answerable_by_decision_resolve` return `True` unconditionally;
     (b) delete the assignment S4 adds, leaving the helper in place.
     For EACH mutation report the REAL exit code and the `FAILED` NODE IDS the
     run printed. Do NOT predict which test fails, do not predict how many fail,
     and do not name an expected colour — report what the run printed. A
     mutation that does not change the outcome is a finding you write into the
     handback, not a number to adjust.
 G8. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C3,
     `.agent/decisions.md` at C4 and BOTH files C5 touches, against a CONTROL
     count over the C0a blob, which is not 0. Report
     `git diff --name-only 59521bf5..C5` and compare it BOTH WAYS against the
     expected union of R42's paths and this round's. Report each commit's
     insertions from `git diff --numstat`, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 and `git worktree list` as
     1 line at C5, AFTER G7's worktree has been removed. Report the reflog for
     this round's commits: every operation prefix must read `commit`, and
     `amend`, `rebase` and `cherry` must be 0 each.
 G9. THE STATE READERS AND THE CANARY, in the PRIMARY checkout at C5 and
     SERIALLY — never two pytest processes alive at once. Run and report the
     real exit code and count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, and the canary
     `tests/cli/test_golden_path.py`. At `5b810e33` these read 480, 52, 21, 16
     and 42. ALSO run `tests/ui_contracts/`, which must be UNCHANGED at 556
     passed with 4 skipped — this round touches no file under `apps/`. ON ANY
     RED, capture the `FAILED` node ids BEFORE anything else and re-run that
     suite ALONE five more times, reporting every reading and every node id; the
     reviewer saw one unreproduced red of `test_test_runner.py` in 20 dry-run
     executions while preparing R42, and a red you cannot reproduce is reported
     WITH its node ids, never absorbed.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G8, the item-status table covering C0a,
             C0b, C1, C2, C3, C4, C5, C6, each of S1 through S9 and the push,
             ONE LINE PER GATE for G1 through G9 with its real exit code, an
             explicit line for R-0694 saying what was registered and that it was
             deliberately NOT fixed here, the open-findings count, and the next
             expected action. THE NEXT ACTION SECTION NAMES, IN THIS ORDER:
             re-read `.agent/STOP` from disk first, then the Open PR Gate, then
             review this round's handback, then R44 — the browser half of D19,
             the model field and the card that renders no button the door
             refuses. Derive your line cap from AGENTS.md yourself, from the
             commit count you actually made; if the mandated content genuinely
             does not fit, declare the DECISION D15 overage with its stated
             cause. Then push with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R43
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D20.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R43 lands DECISION F031 D19's first clause: `build_decision_inbox` gains a third
derived key saying whether the write door's `decision.resolve` can answer this
card, computed with the door's OWN predicate rather than a type check. It also
records R42's PASS, registers R-0694 and lands D20, which splits D19's R43 into
an endpoint round and a browser round because one round cannot hold both.

## Next Steps
1. R44: the browser half of D19 — `DecisionCardModel` gains the field and
   `DecisionInboxCard` renders a non-answerable card's `next_actions` as
   pasteable TEXT rather than as a posting button.
2. R45: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R46: the
   clarification FORM over `payload.clarifications`.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one still ships an enabled button until R44. R-0693 measures it, D19
  rules it, and this round only makes the fact visible on the wire.
- NO FIXTURE CAN TELL THE DOOR'S PREDICATE FROM A TYPE CHECK, because branch 8
  derives its id FROM the escalation record, so the two coincide everywhere.
  R43's guard against that drift is a documented deliberate absence, not a test,
  and the block says so rather than implying coverage it does not have.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so R44's component change will be gated by
  comment-stripped SOURCE reading and by `tsc --noEmit`, never by a rendered
  click. R-0689, R-0690 and R-0691 are the guards written against that gap.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 249 at `5b810e33`
  and this round takes it to 250.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R43

<<<SLICE FINDINGS43
- R-0694 — Low, A FIX CLAUSE THAT SAYS "BINDING ON THE NEXT BLOCK" LIVES ONLY IN LEDGER PROSE, SO THE NEXT BLOCK DID NOT APPLY IT. Raised by the reviewer against its OWN R42 block while re-running that round's G4. R-0631 is OPEN and ends with a clause labelled binding on the next block that orders a multi-paragraph append: reading (b) must compare the LAST N blank-line units against the slice's N paragraphs IN ORDER, with N counted by the script rather than asserted by the block, and the negative control must be applied to the FIRST appended paragraph, because that is the position a tail-only reading cannot see. THE R42 BLOCK ORDERED THREE MULTI-PARAGRAPH APPENDS — FINDINGS42 at two paragraphs, DECISION19 at seven and AMEND42 at three — and its G4 and G6 both said only "check that the last unit equals that slice's final paragraph", which is exactly the tail-only wording R-0631 forbids, and neither gate placed its byte flip on the first appended paragraph. THE MEASUREMENT, run by the reviewer at `5b810e33` against the committed blobs: with one byte flipped in FINDINGS42's FIRST paragraph the whole-file reader REJECTS and the last-unit reader ACCEPTS; with the same flip in the FINAL paragraph both REJECT. So the gate as worded certified less than its sentence claimed, for the second time in the same family. NOTHING FALSE LANDED AND THAT IS WHY THIS IS LOW: the R42 worker implemented its second reader as a whole-prefix comparison — stricter than the gate demanded — and reported units 0–342 unchanged beside the last-unit check, so every flip it ran really was rejected by both of its readers and the appends really were total. WHAT IS ACTUALLY WRONG IS WHERE THE RULE LIVES, and that is a different repair from R-0631's own, which is why this carries its own id rather than amending that entry: R-0631's remedy was written as finding prose and never reached docs/agents/planner_reviewer_prompt.md §3, and a standing rule that lives only in a ledger paragraph binds nobody — the R42 author did not grep the open set for binding clauses before emitting, and no gate anywhere reads the reviewer's compliance with §3 or with the open set before a block is delegated. That is the same root cause R-0692 names for §3 item 3, now with a second instance in the same round, which is what raises it from an accident to a pattern. THE FIX IS A NEW §3 CHECKLIST ITEM stating R-0631's clause as a rule the pre-emission checklist carries, so the wording lives where blocks are actually checked; docs/agents/planner_reviewer_prompt.md is the reviewer's own file and is not in R43's change set, so the item lands with the reviewer, not with this round's worker. R43's own G4 already applies the clause by hand.
<<<END FINDINGS43

<<<SLICE LEDGER43
Gate: F031 R42 — the F031 R42 entry. R42 PASSED ON EVERY ONE OF ITS EIGHT GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, including all eight per-commit insertion counts, every cell of its `## Commits` table and all eight suite counts. TRANSPORT WAS PROVED END TO END FOR THE FIRST TIME ON THIS BRANCH: the block the reviewer authored in `.remedy-wt/`, the C0a blob, the C0b blob and both working copies at C5 are ALL FIVE byte-identical at sha256 `e5c6458b420a0730f40fd3788e7c66e568d09a2e8fbdab495841060af88a94ae` over 28680 bytes and 301 lines, with C0a and C0b resolving to the SAME git blob `e5402d9d` — the reviewer compared its own scratch file against the committed blob rather than trusting the worker's reading of it. THE CAPS HELD: 5 slices, TOTAL 301, CONTENT 126, PROSE 175 against 490 and 400. G3 IS GREEN AND THAT IS THE POINT OF THE ROUND: `.agent/plan.md` at `b75a5dc9` is byte-equal to PLANF031R42 at 2932 bytes with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` 49 — STRICTLY under 50, so the breach R-0692 registered against the R41 block is repaired on disk. THE FOUR APPENDS ARE EXACT: 825662 + 1 + 5345 = 831008 and 831008 + 1 + 3589 = 834598 in the ledger, 599241 + 1 + 3253 = 602495 in `.agent/decisions.md` and 9804 + 1 + 1647 = 11452 in the feature file, each pre-commit blob a byte-exact prefix and each whole-file identity TRUE, blank-line units 343 to 345 to 346, 1439 to 1446 and 21 to 24, every last unit equal to its slice's final paragraph, FINDINGS42's real two-paragraph in-slice swap FALSE, both cross-slice swaps FALSE and every in-memory byte flip REJECTED. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^- R-\d+ — ` 252 to 254 to 254 with ADDED across C2 exactly {`R-0692`, `R-0693`} and REMOVED EMPTY, all ids DISTINCT and the maximum `R-0693`; `^Done: R-\d+ — ` 5, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; `^Gate: F\d+ R\d+ — ` 22 to 22 to 23 with the ADDED key exactly `F031 R41`; `^## DECISION F031 D\d+ ` 18 to 19 and `^## Design amendments ` 3 to 4; open set 247 before C2 and 249 after C3. MARKERS 0 and 0 in all four written targets against a live CONTROL of 5 and 5. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 8 paths over `3afdb209`..`398e60e9`, the range-minus-union residue exactly `.agent/handoff.md` which C6 writes, and NOT ONE PATH under `apps/`, `tests/` or `packages/`, which is what a state round must show. THE EIGHT COMMITS ARE EACH SINGLE-PARENT at insertions 301, 239, 23, 4, 2, 49, 26 and 48, each far under 500; every reflog prefix reads `commit`, so `amend`, `rebase` and `cherry` are 0 each; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT are `tests/ui_server/` 480, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, the canary 42 and `tests/ui_contracts/` 556 passed with 4 skipped — every reading at REAL exit 0 and IDENTICAL to the `59521bf5` baseline, and the one unreproduced red the reviewer had seen in 20 dry-run executions did not recur. THE HANDBACK WAS AUDITED AS AN ARTIFACT: every `+/-` cell equals `git diff --numstat`, the item-status table covers all nine ordered items, one line per gate carries a real exit code, and its 95 lines sit inside the 100-line tier eight tabled commits earn. THE ONE DEFECT OF THE ROUND IS THE REVIEWER'S OWN AND IS REGISTERED AS R-0694: R42's G4 and G6 used a tail-only second reader over multi-paragraph appends, which R-0631's open fix clause forbids, and the worker's stricter implementation is the only reason it cost nothing. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. R42 repaired R-0692's breach, registered R-0693 with the measurement that reshapes the rest of the feature, and put DECISION F031 D19 and its roadmap mirror on disk.
<<<END LEDGER43

<<<SLICE DECISION20
## DECISION F031 D20 (2026-08-27) — D19's programme splits the endpoint from the browser, and the round numbers move by one

SUPERSEDING A ROUND ATTRIBUTION IN DECISION F031 D19: that entry's last CHOSEN
paragraph reads "R43 the derived key and the card; R44 the `fp:` dispatch; R45
the clarification FORM". Sized against the code rather than against the
sentence, R43 as written spans two languages, six files and two test harnesses —
the Python endpoint with its contract tests, the TypeScript model with its unit
tests, and the component with a `tsc --noEmit` and a `vitest` gate on top of the
state readers. That is not one reviewable round, and the block cap of 490 lines
would decide the split by accident rather than by choice.

CHOSEN, THE SPLIT IS AT THE WIRE. R43 lands the endpoint's third derived key and
its tests alone, so the fact travels on the wire before anything renders it. R44
lands the browser half — the model field and the card that renders a
non-answerable decision's `next_actions` as text. R45 becomes the `fp:` dispatch
and R46 the clarification FORM. Nothing D19 CHOSE changes: not the key, not the
predicate it is computed from, not the refusal to branch on `card.type`, not the
scope ruling that leaves six prefixes out of F031. Only the round numbers move.

REVERSE IT by rejoining the two halves in one round, which the block cap will
refuse; that refusal is the evidence for this entry.
<<<END DECISION20
