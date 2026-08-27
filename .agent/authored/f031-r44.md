── STEP T001 the answerable key, repaired / F031 — ROUND R44 ──────────
Goal:        Repair the key R43 landed. `answerable_by_decision_resolve` reports
             True for an ALREADY-ANSWERED task decision, which the write door
             refuses 409, so the helper gains the OPEN condition the door itself
             applies — with the test that discriminates it. Also record R43's
             verdict, register R-0695 and land DECISION F031 D21.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the finding · C3 the R43 gate entry · C4 DECISION F031 D21 ·
             C5 the repair with its test · C6 handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r44.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `packages/orchestration/decision_inbox.py`,
             `tests/orchestration/test_decision_inbox.py`, `.agent/handoff.md`.
             NO FILE UNDER `apps/` and NO FILE UNDER `docs/` — the browser half
             is R45's, and R-0694's and R-0695's shared repair in
             `docs/agents/planner_reviewer_prompt.md` is a reviewer-file round
             this block deliberately does not open.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof, and stopping
    early would lose the record this round exists to write.
 2. THE CODE IS DESCRIBED, NOT SLICED. Section S below is a numbered SPEC, not
    an authored text: you write the Python yourself to satisfy it, in the
    surrounding file's own idiom. The byte-for-byte rule of constraint 1 binds
    the marked SLICES and nothing else; report how many your extractor found.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The finding
    lands at C2 BEFORE the gate entry at C3, and C5 lands after both. No pair
    may be reordered. LEDGER44 and FINDINGS44 state facts about THIS round's
    own commits, and this constraint is what makes them true on landing.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R43. That is
    ordered: the plan becomes current at C1, the first substantive commit.
 5. THE FINDING AND THE DECISION ARE THE REVIEWER'S TEXT. You never write a
    `Done:` paragraph, never edit a finding's wording, never edit D21. R-0695 is
    registered here and its CODE half is fixed here at C5; its PROCESS half —
    a `docs/agents/planner_reviewer_prompt.md` §3 item it shares with R-0694 —
    is not in this round's change set and stays OPEN.
 6. THE LEDGER SETS MOVE ONCE EACH. Across C2 `^- R-\d+ — ` moves 255 to 256
    with the id ADDED exactly `R-0695` and none REMOVED. Across C3
    `^Gate: F\d+ R\d+ — ` moves 24 to 25 with the ADDED key exactly `F031 R43`.
    Across both, `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
    `^Gate: R\d+ — ` stays 19. The open set is 250 before C2 and 251 after.
 7. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 8. DESTRUCTIVE VERIFICATION IS ISOLATED. Every mutation and every red control
    of gate G7 runs inside a disposable `git worktree` under `.remedy-wt/`,
    NEVER in the primary checkout, and the worktree is removed BY ITS EXACT PATH
    when G7 ends. Nothing under `.remedy-wt/` is ever committed, and
    `.remedy-wt/f031-r44-block.md` is the reviewer's scratch copy — leave it
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
 S1. In `packages/orchestration/decision_inbox.py`, widen the existing import of
     `find_task_decision` from `packages.orchestration.escalation` to also bring
     in `ESCALATION_STATUS_OPEN`. Both names are module-level in that file and
     the import stays acyclic for the reason R43's round measured.
 S2. `_answerable_by_decision_resolve` returns True only when the record EXISTS
     AND its status is `ESCALATION_STATUS_OPEN` — the door's own two conditions,
     read from the same record the door reads. Keep the helper's body to that
     one reading and that one comparison; do not branch on the card's `type`,
     and do not read the card's own `status` key, because the door reads the
     escalation record and this helper exists to mirror the door.
 S3. Correct the helper's docstring where the new condition makes it stale. Its
     present MEASURED paragraph stops at `find_task_decision`; the door's refusal
     of a non-OPEN record lives in `escalation.answer_task_decision`, which
     returns None unless `record.get("status")` is `ESCALATION_STATUS_OPEN`, and
     `ui_server._dispatch_decision_resolve` answers that None 409
     `rejected_state`. Say that the predicate is TWO conditions and name where
     each is enforced. Finding R-0695 carries the measurement.
 S4. The deliberate-absence paragraph that R43 landed STAYS, and gains the one
     fact that now distinguishes the two predicates: a type check and the door's
     predicate no longer coincide, because an ANSWERED task decision still yields
     a card of type `task_decision` while the door refuses it. That is the
     fixture S6 builds, and it is why this file no longer relies on an absence.
 S5. `build_decision_inbox` and the module docstring are UNCHANGED — the key,
     its spelling, its position and the two keys beside it all stay as R43 left
     them. This round changes what the key SAYS, never what the document holds.
 S6. In `tests/orchestration/test_decision_inbox.py`, add to section (g) one
     test that ANSWERS a task decision through `escalation.answer_task_decision`
     and then asserts, on the card the SAME job yields afterwards, that
     `status` is `resolved`, that a second `answer_task_decision` call returns
     None — the door's real refusal, asserted rather than assumed — and that
     `answerable_by_decision_resolve` is False. Assert it is True BEFORE the
     answer in the same test, so the test pins the transition and not one state.
     Widen that file's existing `escalation` import to bring in
     `answer_task_decision`; build no new fixture, use `_fixture_task_decision`.
 S7. Nothing else changes in either file. No existing test is deleted, no
     assertion is weakened, no fixture is edited, and
     `ANSWERABLE_DECISION_TYPES` keeps its present value and its comment.

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
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R44 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE APPENDS, EACH PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. Read every non-current revision with `git show <rev>:<path>`
     into memory; never write a past blob over a tracked file to read it.
     `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus FINDINGS44; at C3 equals ITS pre-commit blob plus ONE
     newline plus LEDGER44; `.agent/decisions.md` at C4 equals its pre-commit
     blob plus ONE newline plus DECISION21. The pre-commit blob for C2 is 841494
     bytes and for C4 is 603923 bytes. For EACH append report both byte counts
     and the sum. Then confirm EACH with a SECOND, independent reader: split the
     whole file on blank lines, let N be the number of paragraphs YOUR SCRIPT
     COUNTS in that slice — never a number this block asserts — and compare the
     LAST N units of the file against the slice's N paragraphs IN ORDER. Report
     N and the unit count before and after for each. THE NEGATIVE CONTROL GOES
     ON THE FIRST APPENDED PARAGRAPH, which is the position a tail-only reading
     cannot see: flip ONE byte IN MEMORY inside paragraph 1 of each slice and
     report that BOTH readers REJECT it. For any slice whose N is 1, say so and
     note that paragraph 1 is also the last. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     ADDED and REMOVED as SETS at each step, whether all ids are DISTINCT, and
     the maximum id. Every movement constraint 6 names is checked here. Report
     the open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after
     C3. Also report `^## DECISION F031 D\d+ ` in `.agent/decisions.md` as 20
     before C4 and 21 after.
 G6. THE SPEC, ITEM BY ITEM. For EACH of S1 through S7 report DONE or NOT DONE
     with the file and line where it landed. For S5 report the evidence rather
     than the word: `git diff` over C5 restricted to
     `packages/orchestration/decision_inbox.py` must show NO change inside
     `build_decision_inbox` and NO change to the module docstring, and you state
     which hunks the diff actually contains. Report `python3 -m ruff check` on
     both changed files at its REAL exit code, and the count of `assert`
     statements the test file holds before and after.
 G7. THE TESTS, THE RED CONTROL AND THE MUTATIONS. In the PRIMARY checkout at C5
     run `python3 -m pytest tests/orchestration/test_decision_inbox.py -q` and
     report its REAL exit code and collected count; at `46ae059f` that file
     collects 33. Then, INSIDE A DISPOSABLE WORKTREE and never in the primary
     checkout, run these, one at a time, restoring the tree between them and
     re-checking byte-equality with the original after each restore. EVERY ONE
     of them edits `packages/orchestration/decision_inbox.py` and no other file,
     and each names bytes that occur exactly once in it:
     (a) THE RED CONTROL — keep S6's new test, and change ONLY the helper's
         return so it reads `find_task_decision(job, str(decision_id)) is not
         None` again, leaving the import and every other line in place;
     (b) make `_answerable_by_decision_resolve` return `True` unconditionally;
     (c) make it return `False` unconditionally.
     For EACH report the REAL exit code and the `FAILED` NODE IDS the run
     printed. Do NOT predict which test fails, do not predict how many fail, and
     do not name an expected colour — report what the run printed. A mutation
     that does not change the outcome is a finding you write into the handback,
     not a number to adjust.
 G8. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C3,
     `.agent/decisions.md` at C4 and BOTH files C5 touches, against a CONTROL
     count over the C0a blob, which is not 0. Report
     `git diff --name-only 46ae059f..C5` and compare it BOTH WAYS against this
     round's expected path set. Report each commit's insertions from
     `git diff --numstat`, confirm each is single-parent and under 500. Report
     `git ls-files .remedy-wt` as 0 and `git worktree list` as 1 line at C5,
     AFTER G7's worktree has been removed. Report the reflog FOR THIS ROUND'S
     OWN COMMITS ONLY: every operation prefix must read `commit`, and among
     those entries `amend`, `rebase` and `cherry` must be 0 each. Do not count
     those words over the whole reflog, which holds this repository's entire
     history and is not what this gate asks.
 G9. THE STATE READERS AND THE CANARY, in the PRIMARY checkout at C5 and
     SERIALLY — never two pytest processes alive at once. Run and report the
     real exit code and count of each: `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, and the canary
     `tests/cli/test_golden_path.py`. At `46ae059f` these read 480, 52, 21, 16
     and 42. ALSO run `tests/ui_contracts/`, which must be UNCHANGED at 556
     passed with 4 skipped — this round touches no file under `apps/`. ON ANY
     RED, capture the `FAILED` node ids BEFORE anything else and re-run that
     suite ALONE five more times, reporting every reading and every node id; a
     red you cannot reproduce is reported WITH its node ids, never absorbed.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G8, the item-status table covering C0a,
             C0b, C1, C2, C3, C4, C5, C6, each of S1 through S7 and the push,
             ONE LINE PER GATE for G1 through G9 with its real exit code, an
             explicit line for R-0695 saying what was registered, that its CODE
             half landed at C5 and that its PROCESS half stays OPEN, the
             open-findings count, and the next expected action. THE NEXT ACTION
             SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review this round's handback,
             then R45 — the browser half of D19, the model field and the card
             that renders no button the door refuses. Derive your line cap from
             AGENTS.md yourself, from the commit count you actually made; if the
             mandated content genuinely does not fit, declare the DECISION D15
             overage with its stated cause. Then push with
             `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R44
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D21.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R44 repairs the key R43 landed. `answerable_by_decision_resolve` reported True
for an ALREADY-ANSWERED task decision, which the door refuses 409, so the helper
gains the OPEN condition the door itself applies, with the test that
discriminates it. The round also records R43's PASS, registers R-0695 and lands
DECISION F031 D21, which moves the browser half to R45.

## Next Steps
1. R45: the browser half of D19 — `DecisionCardModel` gains the field and
   `DecisionInboxCard` renders a non-answerable card's `next_actions` as
   pasteable TEXT rather than as a posting button.
2. R46: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R47: the
   clarification FORM over `payload.clarifications`.
3. A reviewer-file round landing the §3 checklist item R-0694 and R-0695 share.
4. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one still ships an enabled button until R45. R-0693 measures it, D19
  rules it, and the wire carries the fact from R43 on.
- THE DOOR'S PREDICATE IS TWO CONDITIONS, NOT ONE: the record must EXIST and be
  OPEN. R43 encoded only the first, no fixture answered a decision before
  reading the card, and the suite stayed green over a value that was false for
  every answered task decision. R-0695 carries the measurement.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so R45's component change will be gated by
  comment-stripped SOURCE reading and by `tsc --noEmit`, never by a rendered
  click. R-0689, R-0690 and R-0691 are the guards written against that gap.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 250 at `46ae059f`
  and this round takes it to 251.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R44

<<<SLICE FINDINGS44
- R-0695 — Medium, THE ANSWERABILITY KEY REPORTS TRUE FOR AN ALREADY-ANSWERED TASK DECISION, WHICH THE WRITE DOOR REFUSES 409. Raised by the reviewer at the R43 gate against its OWN R43 block, whose section S item S2 ordered the helper's body verbatim, so the worker wrote exactly what it was given and the defect is the spec's. THE MEASUREMENT, run by the reviewer in memory at `46ae059f` against a `_fixture_task_decision`-shaped job and never against a stored job: the card reports `answerable_by_decision_resolve` True while its `status` reads `open`; after `escalation.answer_task_decision` accepts one answer, `decision_queue.list_decisions` still yields a card for that record — branch 8 appends unconditionally and lets `is_open` decide only the status, the severity and the next actions — the card's `status` reads `resolved`, a SECOND `answer_task_decision` call returns None, and `answerable_by_decision_resolve` STILL reads True. So the key is false in exactly the state the door refuses. THE CAUSE IS A PREDICATE OF TWO CONDITIONS ENCODED AS ONE: `ui_server._dispatch_decision_resolve` accepts only what `escalation.answer_task_decision` accepts, and that function returns None unless the record EXISTS and `record.get("status")` equals `ESCALATION_STATUS_OPEN`, while `_answerable_by_decision_resolve` tests existence alone through `find_task_decision`. R43's docstring traced the route to the record correctly and stopped one line short of the guard, and the conclusion it drew — that the key says whether the door can answer this card — does not follow from the premise it measured. NO TEST CATCHES IT, AND THE REVIEWER PROVED THAT RATHER THAN ASSUMING IT: adding the missing OPEN condition inside a disposable worktree leaves `tests/orchestration/test_decision_inbox.py` at 33 passed and REAL exit 0, so nothing in that file discriminates the door's predicate from mere existence — every one of the eight `PRODUCING_FIXTURES` builds an OPEN record and none answers one. THE FACT WAS ALREADY IN THE OPEN SET when the R43 block was written: R-0685 states in as many words that `answer_task_decision` is "enforced by returning `None` for any record not OPEN", so the measurement this finding reports was on disk, unread, in the same file the block appends to — which is the second consecutive round whose defect is a block emitted without consulting the open set, the root cause R-0694 and R-0692 both name. NOTHING FALSE HAS RENDERED YET AND THAT IS WHY THIS IS MEDIUM RATHER THAN HIGH: the key is one round old, no browser code reads it until R45, and DECISION F031 D20's split at the wire is what bought the round in which to catch it. THE FIX HAS TWO HALVES. The CODE half is R44's C5 — the helper takes the door's second condition, and a test answers a decision and pins the transition from True to False. The PROCESS half is the §3 checklist item this shares with R-0694, requiring a block that computes a value from another module's predicate to read that predicate's OWN refusal conditions and not merely its route to the data; that item lands in `docs/agents/planner_reviewer_prompt.md`, the reviewer's file, which is in no feature round's change set, and this finding stays OPEN until it does.
<<<END FINDINGS44

<<<SLICE LEDGER44
Gate: F031 R43 — the F031 R43 entry. R43 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM: the C0a blob, the C0b blob, the working copy at C5 and the working copy at the gate are ALL FOUR byte-identical at sha256 `e75fd033eea7922a3d4c222c906a9ce3f84b7f0697aefaf314a54d566a3d4c70` over 26648 bytes and 293 lines, with C0a and C0b resolving to the SAME git blob `2b7bd186`. THE EXTRACTION printed 4 slices, CONTENT 72 and TOTAL 293, so PROSE was 221 against 400 and TOTAL 293 against 490. THE PLAN at `dfce9f74` is byte-equal to PLANF031R43 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 49, strictly under 50. THE THREE APPENDS ARE EXACT AND R-0631'S CLAUSE WAS APPLIED BY HAND FOR THE FIRST TIME: 834598 + 1 + 2735 = 837334 and 837334 + 1 + 4159 = 841494 in the ledger and 602495 + 1 + 1427 = 603923 in `.agent/decisions.md`, blank-line units 346 to 347 to 348 and 1446 to 1450, N counted by the reviewer's own script at 1, 1 and 4, every whole-file identity TRUE, and the byte flip placed on the FIRST appended paragraph REJECTED by BOTH readers on all three — which is the position the tail-only wording R-0694 registered could not see. THE SETS MOVED ONLY WHERE CONSTRAINT 6 ALLOWED: `^- R-\d+ — ` 254 to 255 to 255 with ADDED across C2 exactly {`R-0694`} and REMOVED EMPTY, all ids DISTINCT and the maximum `R-0694`; `^Done: R-\d+ — ` 5, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; `^Gate: F\d+ R\d+ — ` 23 to 23 to 24 with the ADDED key exactly `F031 R42`; `^## DECISION F031 D\d+ ` 19 to 20; open set 249 before C2 and 250 after C3. MARKERS 0 and 0 in all five written targets against a live CONTROL of 4 and 4. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 10 paths over `59521bf5`..`f86c0b8f`, the eight commits are each SINGLE-PARENT at insertions 293, 224, 22, 2, 2, 22, 65 and 61, every one far under 500, and every reflog entry for those eight reads `commit:`, so `amend`, `rebase` and `cherry` are 0 each among them; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE CODE IS WHAT SECTION S ORDERED, ITEM BY ITEM: the import is acyclic — `escalation.py` imports only `__future__` and `collections.abc` at module level — the helper's body is the single `is not None` expression S2 fixed, the deliberate absence is documented in as many words, the third key sits beside the two existing ones with their order untouched, and the reviewer's own sweep of `packages/orchestration/decision_inbox.py` for the word `two` or a standalone `2` returns 0 lines, so S5's staleness sweep really is complete. `python3 -m ruff check` on both changed files is REAL exit 0, and the test file's `assert` statements counted by AST move 18 to 21. THE TESTS AND THE MUTATIONS REPRODUCED EXACTLY: 33 passed at REAL exit 0 against 25 at `5b810e33`, mutation (a) 7 failed and 26 passed at REAL exit 1, mutation (b) 17 failed and 16 passed at REAL exit 1, both run only inside a disposable worktree with the primary checkout at 0 porcelain lines throughout. THE SUITES THE REVIEWER RE-RAN SERIALLY IN THE PRIMARY CHECKOUT are `tests/ui_server/` 480, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, the canary 42 and `tests/ui_contracts/` 556 passed with 4 skipped — every reading at REAL exit 0 and identical to the `5b810e33` baseline, and the unreproduced `test_test_runner.py` red of earlier rounds did not recur. THE HANDBACK WAS AUDITED AS AN ARTIFACT: all eight `+/-` cells equal `git diff --numstat` exactly, the item-status table covers every ordered item, one line per gate carries a real exit code, and its 117 lines carry the DECISION D15 stated-cause line the tier requires. THE WORKER ALSO CAUGHT THE BLOCK'S OWN DEFECT and reported it rather than correcting it, exactly as constraint 1 requires: R43's constraint 2 said "the five marked SLICES" over a block carrying four, which is the §3 item 32 class — a clause naming a KIND of the block's own parts and giving it a numeral — recurring under the very item written to forbid it, and the reviewer's extractor confirms 4 against a marker control of 4. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing table, no unverified completion claim and no silent scope change. THE ONE DEFECT OF SUBSTANCE IS THE REVIEWER'S OWN SPEC AND IS REGISTERED AS R-0695: S2 fixed the helper's body as an existence test, while the door refuses any record that is not OPEN, so the key R43 shipped is false for every answered task decision — routed to planning under §4.7 as a wrong spec rather than held against a worker that executed it faithfully, and repaired at R44's C5.
<<<END LEDGER44

<<<SLICE DECISION21
## DECISION F031 D21 (2026-08-27) — the answerability key mirrors the door's REFUSAL conditions, not its route to the record, and the browser half moves to R45

SUPERSEDING A ROUND ATTRIBUTION IN DECISION F031 D20: that entry rules "R44
lands the browser half — the model field and the card that renders a
non-answerable decision's `next_actions` as text". The key R43 landed, read at
`46ae059f`, is false for an answered task decision, so R44 becomes the endpoint
repair, the browser half
becomes R45, the `fp:` dispatch R46 and the clarification FORM R47. D20's split
at the wire is not weakened by this — it is what made the repair cheap, because
the fact was caught on the wire before any component rendered it.

CHOSEN, THE KEY IS COMPUTED FROM WHAT THE DOOR REFUSES. A derived key that
claims another module will accept something is computed from that module's
REFUSAL conditions in full, not from its route to the data. `answer_task_decision`
refuses on two conditions — no record, or a record that is not OPEN — so
`_answerable_by_decision_resolve` tests both, reading the escalation record the
door reads rather than the card's own `status` field, so the two cannot drift.
Nothing else D19 CHOSE changes: not the key's name, not the refusal to branch on
`card.type`, not the scope ruling that leaves six prefixes out of F031.

CONSIDERED AND REJECTED: reading the card's `status` key instead. It is the same
value today, derived by `list_decisions` from the same record, but it is a
SECOND derivation of the door's input and would make the inbox agree with itself
rather than with the door — which is the failure this entry exists to correct.

REVERSE IT by narrowing the helper back to an existence test, which the test
R44 adds will refuse; that refusal is the evidence for this entry.
<<<END DECISION21
