STEP CLOSURE 1 OF 3 / F031 — DECISION INBOX
Goal:        Record the R66 verdict, resolve R-0693 — the only open High this
             feature raised, whose DECISION F031 D19 repair is on disk in full —
             and give `docs/roadmap/features/T5_F031.md` the `## Built State`
             section it has never had, which is precondition 4 of
             docs/roadmap/STATUS_closure_protocol.md. NO PRODUCTION CODE, no new
             decision, and NOTHING under `apps/`, `packages/` or `tests/`.
             STATUS.md and README.md are NOT touched here: the closure commit
             owns them and it is two rounds away.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the ledger entry and the resolution · C3 the Built State
             section · C4 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r67.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `docs/roadmap/features/T5_F031.md`, `.agent/handoff.md`. NOTHING
             under `apps/`, `packages/` or `tests/`. `.agent/decisions.md` is not
             in it, `docs/roadmap/STATUS.md` is not in it, `README.md` is not in
             it, and no file under `.agent/gate_f031_r65/` is edited.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f031-r67.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f031-r67.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G1 instead has you
    measure the scratch file, C0a, C0b and the working copy and prove all four
    EQUAL, and the reviewer holds the scratch file's value independently. Leave
    the scratch file where it is; `.remedy-wt/` is gitignored and prior rounds'
    scratch already lives there.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice looks wrong, say so in the handback
    and finish the round anyway — a corrected slice destroys the transport
    proof.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. No pair may be
    reordered and none may be merged.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R66. That is
    ordered: the plan becomes current at C1.
 5. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph of
    your own and never mint a finding id. LEDGER67 carries exactly two
    paragraphs, separated by ONE blank line: the R66 gate entry and the R-0693
    resolution. NO OTHER FINDING IS RESOLVED AND NONE IS REGISTERED.
 6. THE LEDGER SETS MOVE TWICE AND ONLY TWICE. Across C2 `^Gate: F\d+ R\d+ — `
    moves 47 to 48 with the ADDED key exactly `F031 R66`, and
    `^Done: R-\d+ — ` moves 16 to 17 with the ADDED id exactly `R-0693`.
    `^- R-\d+ — ` stays 268, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 252 before C2 and 251 after C2.
 7. THE BUILT STATE IS AN APPEND, NOT AN EDIT. `docs/roadmap/features/T5_F031.md`
    at C3 is its pre-commit bytes plus ONE newline plus BUILTSTATE67. No line
    already in that file is changed, reordered or removed — the four `## Design
    amendments` sections and everything above them are untouched, exactly as
    that file's own convention says: it records what was planned and then what
    was ruled, in that order.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 9. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree; the primary
    checkout reads `git status --porcelain` 0 lines at every commit.
10. YOUR HANDBACK FITS THE TIER ITS BUNDLE EARNS. Read the handoff.md section of
    AGENTS.md, count the commits this Bundle orders, and derive your own cap
    from that rule — do not take a number from this block. Then write NO BLANK
    LINE between a `###` commit heading and its table, none between a `##`
    heading and its first line, and none between one commit block and the next.
    Declare DECISION D15 only if the MANDATED content still does not fit in that
    shape, and if you do, name what actually caused it.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, `cd x && y`,
    and every form of environment assignment. Route anything that counts, hashes
    or compares through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. THIS IS NOT THE LAST ROUND OF ITS SESSION. Write no SESSION line and no
    session summary. The next expected action is CLOSURE 2 OF 3 — the evidence
    bundle and the review zip — and you name it by that label and by no round
    number, because §3 item 35 forbids numbering a round that has not begun.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback. Read
every non-current revision with `git show <rev>:<path>` into memory; never write
a past blob over a tracked file to read it.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block AS READ FROM
     `.remedy-wt/f031-r67.md`, as saved at C0a, as mirrored at C0b and as read
     off disk at C3 — all four must be EQUAL — and say whether C0a and C0b are
     the same git blob. Report also whether any line of the block as saved is a run of a
     single repeated character, which must come back as none. THEN STATE IN ONE
     SENTENCE WHAT THIS PROOF COVERS: the scratch file, the saved copy, its
     mirror and the working copy, and NOT the bytes of any prompt. §3 item 37.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from any other source. Report how many slices
     your extractor printed, each slice's own line count, the CONTENT line
     total, the TOTAL line count, and PROSE as TOTAL minus CONTENT. MARKERS ARE
     PROSE. PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R67 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50.
 G4. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER67. The reviewer measured the base blob at
     `eed7e010` itself: 986008 bytes over 395 blank-line units. If it reads
     differently before C2, something moved that this round did not order — stop
     and hand back. Report both byte counts and the sum. Then confirm with a
     SECOND, independent reader, as §3 item 36 requires: split the whole file on
     blank lines, let N be the number of paragraphs YOUR SCRIPT COUNTS in that
     slice — never a number this block asserts — and compare the LAST N units of
     the file against the slice's N paragraphs IN ORDER. Report N and the unit
     count before and after. THE NEGATIVE CONTROL GOES ON THE FIRST APPENDED
     PARAGRAPH: flip ONE byte IN MEMORY inside paragraph 1 and report that BOTH
     readers REJECT it. Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at two points — before C2 and after C2 — the
     line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the finding ids, the
     RESOLVED ids and the gate keys ADDED and REMOVED as SETS, whether all ids
     are DISTINCT, and the maximum id, which is `R-0707` at both points. Every
     movement constraint 6 names is checked here, INCLUDING the ones that must
     NOT move. Report the open set at both points.
 G6. THE BUILT STATE APPEND, PROVED TWICE, THE SAME WAY. `docs/roadmap/features/
     T5_F031.md` at C3 equals its pre-commit blob plus ONE newline plus
     BUILTSTATE67. The reviewer measured the base blob at `eed7e010` itself:
     11452 bytes over 197 lines and 24 blank-line units. Report both byte counts
     and the sum. Then the SECOND reader over the whole appended region: N
     paragraphs COUNTED BY YOUR SCRIPT, the last N units compared IN ORDER, the
     unit count before and after, and a one-byte flip IN MEMORY inside the FIRST
     appended paragraph REJECTED by BOTH readers. Report also that
     `^## Built State$` occurs exactly 1 time in the file at C3 and 0 times at
     `eed7e010`, and that `^## Design amendments` occurs 4 times at BOTH points.
 G7. NOTHING ELSE MOVED, MARKERS, PATHS, COMMITS. Compare the path set of
     `git diff --name-only eed7e010..C3` BOTH WAYS against this round's expected
     set — the Change line's list MINUS `.agent/handoff.md`, excluded because
     the handback is written at C4, outside a range ending at C3 — and report
     both residues EMPTY. Report `git diff --stat eed7e010..C3` restricted to
     `apps/`, `packages/` and `tests/` and confirm each is EMPTY, and the same
     restricted to `docs/roadmap/STATUS.md` and to `README.md`, each EMPTY.
     Report `git diff --name-only eed7e010..C3 -- .agent/gate_f031_r65/` as 0
     lines. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `docs/roadmap/features/T5_F031.md` at C3, against a CONTROL count over the
     C0a blob, which is not 0. Report each commit's insertions from
     `git diff --numstat` for C0a through C3, confirm each is single-parent and
     under 500. Report `git ls-files .remedy-wt` as 0 lines, `git worktree list`
     as 1 line, `git branch --list "tmp/*"` as 0 lines, and `git ls-files
     --others --exclude-standard` as 0 lines at C3.
 G8. THE CANARY, THE STATE READERS AND THE DOCS READERS. In the PRIMARY checkout
     at C3, run SERIALLY — never two pytest processes alive at once — reporting
     each REAL exit code and count: `tests/cli/test_golden_path.py` (the
     canary), `tests/ui_contracts/`, `tests/ui_server/`,
     `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/docs/` and
     `tests/orchestration/test_roadmap_index.py`. The last two are ordered
     because this round edits `docs/roadmap/**`, which `.agent/context.md` makes
     a standing constraint. At `eed7e010` the reviewer measured these itself at
     42; 566 passed and 4 skipped; 489; 52; 21; 16; 295; and 30, every one at
     exit 0. Any movement is unexplained: stop and hand back.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4, in the shape constraint 10 orders: feature and round, branch,
             the per-commit changed-files table with the `+/-` column taken from
             `git diff --numstat` ITSELF and agreeing cell for cell with G7's
             readings, the item-status table covering C0a, C0b, C1, C2, C3, C4
             and the push, ONE LINE PER GATE for G1 through G8 with its real
             exit code, the open-findings count AFTER this round, and the next
             expected action. SAY PLAINLY THAT NOTHING UNDER `apps/`,
             `packages/` OR `tests/` CHANGED, THAT THE ONLY FINDING THAT MOVED
             IS R-0693 AND IT MOVED TO RESOLVED, AND THAT THE OPEN COUNT IS THE
             NUMBER G5 MEASURED AFTER C2. Give the Built State ONE sentence:
             `docs/roadmap/features/T5_F031.md` now carries a `## Built State`
             section and closure precondition 4 is met. Make the next-action
             section CLOSURE 2 OF 3 — the feature-scoped evidence bundle and a
             FRESH review zip built from a clean tree at the reviewed head, a
             failing zip build being a closure BLOCKER — and name no round
             number for it. Then push with
             `git push origin feature/f031-decision-inbox`.

<<<SLICE PLANF031R67
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
CLOSURE 1 of 3. This round writes the R66 verdict, resolves R-0693 — the only
open High this feature raised, whose DECISION F031 D19 repair landed in full —
and gives `docs/roadmap/features/T5_F031.md` the `## Built State` section it has
never had, which is the closure protocol's precondition 4. No production code
and no new decision. STATUS.md and README.md are NOT touched here: the closure
commit owns them and it is two rounds away.

## Next Steps
1. CLOSURE 2 of 3 — the feature-scoped evidence bundle and a FRESH review zip
   built from a clean tree at the reviewed head. A failing zip build is a
   closure BLOCKER, never something to work around.
2. CLOSURE 3 of 3 — the STATUS line from `[~]` to `[x]` with the README
   capability sync in the SAME commit, the candidates file, and the pull
   request. The PR is NOT merged in this session.

## Risks
- R-0693 IS THE ONLY OPEN HIGH THIS FEATURE RAISED, and its repair is on disk:
  the `fp:` dispatch in the write door, the third endpoint key, and a card that
  posts nothing the door would refuse. R-0495 and R-0574 are inherited standing
  Highs that rode through six prior closures and ride through this one as
  documented risks, which is what PASS_WITH_RISKS means.
- SIX OF THE EIGHT PRODUCING TYPES STILL CANNOT BE ANSWERED THROUGH THE DOOR.
  DECISION F031 D19 rules them out of F031's scope, and the inbox tells the
  truth about every one of them rather than offering a refused button.
- THE PARITY CLAIM OF THE R65 GATE IS VOID AND STAYS VOID. A rebuild ran inside
  the base run window and the evidence says so; it costs nothing only because
  the base-only set is empty, so no id was owed an attribution.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 252 before this
  round and 251 after it, R-0693 being the one entry that moves.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R67

<<<SLICE LEDGER67
Gate: F031 R66 — the F031 R66 entry. R66 PASSED ON EVERY GATE ITS BLOCK ORDERED, G1 THROUGH G7, AND THE REVIEWER RE-RAN EVERY ONE ITSELF. THIS WAS A RECORD ROUND and it behaved as one: no file outside `.agent/` changed, no finding moved in either direction, and the open set is 252 at both points. THE TRANSPORT CHAIN IS INTACT: the block reads sha256 `54afd8cf…51dcb07f` over 19350 bytes and 210 lines at C0a, at C0b and off disk, all three EQUAL, with C0a and C0b the SAME git blob `3c5c87c55bce` and no line that is a run of one repeated character. EXTRACTION AND CAPS re-measured from the committed C0a blob: 2 slices at 44 and 1 content lines, CONTENT 45, TOTAL 210 and PROSE 165, both caps met. THE PLAN at C1 is byte-equal to PLANF031R66 with the minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 44. THE APPEND at C2 proves twice: 980684 + 1 + 5323 = 986008 against a committed 986008, and the second reader counted N 1 with units 394 before and 395 after, the last unit EQUAL IN ORDER to the slice's one paragraph — the reviewer's own re-run reproduced every one of those five numbers — with a one-byte flip in the first appended paragraph REJECTED by both readers. THE SETS MOVED EXACTLY ONCE: `^Gate: F\d+ R\d+ — ` 46 to 47 adding exactly `F031 R65`, while `^- R-\d+ — ` stayed 268, `^Done: R-\d+ — ` stayed 16, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; no finding id and no resolved id was added or removed; all ids DISTINCT at both points with maximum `R-0707`. NOTHING ELSE MOVED: both path residues EMPTY over the four-path set, `apps/`, `packages/`, `tests/` and `docs/` — the last WHOLE — each EMPTY, `.agent/gate_f031_r65/` 0 lines, markers 0 and 0 in both targets against a CONTROL of 2 and 2 over the C0a blob, insertions 210, 134, 20 and 2, each commit single-parent and under 500, and the worktree, scratch and untracked readings all clean. THE READERS ARE UNMOVED, re-run serially by the reviewer at `eed7e010`: the canary 42, `tests/ui_contracts/` 566 passed and 4 skipped, `tests/ui_server/` 489, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21 and `tests/orchestration/test_integrity_gate.py` 16, every one a REAL exit 0. THE CORRECTION THE ROUND EXISTED TO MAKE WAS MADE: the R65 handback's five-round SESSION line is replaced by the true three, and the block SUPPLIED those facts rather than ordering the worker to derive them, which is the repair R-0692's class asked for. THE HANDBACK IS HONEST ABOUT ITS OWN SHAPE: 54 lines against the 60 its five-commit bundle earns, every mandated section present, every `+/-` cell agreeing with `git diff --numstat`, and no DECISION D15 declaration made or needed. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Done: R-0693 — RESOLVED at F031 R67 against DECISION F031 D19, which re-scoped the acceptance sentence this finding measured against and ruled the repair in three parts; all three are on disk at `eed7e010` and the reviewer read each one itself. THE THIRD KEY EXISTS AND IS COMPUTED FROM THE DOOR'S OWN PREDICATE, not from the card's type: `packages/orchestration/decision_inbox.py::_answerable_by_decision_resolve` returns, for an `fp:`-prefixed id, whether `job.flight_plan` is a dict whose `_approval` is `"pending"`, and for every other id whether `escalation.find_task_decision` finds a record whose `status` is `ESCALATION_STATUS_OPEN` — the same two readings of the same object `_dispatch_decision_resolve` makes, so the two cannot drift apart silently, and `build_decision_inbox` carries it on every card as `answerable_by_decision_resolve` beside `age_seconds` and `blocked_count`. THE `fp:` DISPATCH SHIPPED: `grep resolve_flight_plan_approval packages/orchestration/ui_server.py` returned nothing when this finding was raised and now returns four lines, the call itself at 3777, which is the half of DECISION F009 D5 that feature planned and did not land. THE ENABLED BUTTON IS GONE: `apps/ui/src/api/decisionCard.ts` line 229 reads `const posts = card.answerable_by_decision_resolve === true;` and the card renders a non-answerable decision's `next_actions` as pasteable TEXT instead, so the surface no longer offers an affordance the door would refuse. WHAT REMAINS IS OUT OF SCOPE BY RULING AND SAID SO IN PUBLIC: `pa:`, `sr:`, `tf:`, `dirty_repo`, the budget id and `mem:` — six of the eight producing branches of `list_decisions` — have no package-level resolve verb to dispatch to, D19 reads "answers correctly from fixtures" as TASK DECISIONS PLUS FLIGHT-PLAN APPROVALS for this feature's close, and the F031 `## Built State` section written this same round names all six so a reader of the built state learns the gap without reading this ledger. THE ADJACENT MEASUREMENT R-0695 IS ALREADY RESOLVED and its fix is the `ESCALATION_STATUS_OPEN` clause quoted above, so the predicate refuses an ANSWERED task decision the way the door does. THE GUARD IS A TEST, NOT AN ABSENCE: section (g) of `tests/orchestration/test_decision_inbox.py` builds the fixtures where a type check and the door's predicate disagree, and `tests/ui_contracts/test_decision_answer_wiring.py` reads the comment-stripped source of the whole prop chain, both green at `eed7e010`.
<<<END LEDGER67

<<<SLICE BUILTSTATE67
## Built State
Measured at `eed7e010`, the branch tip this section was written against. The
F031 integration gate ran its branch command at `2d4001b4`, and every commit
between the two touches only `.agent/` state, so no file named below has changed
since the gate.

- **T001 — the read, its three derived keys and the badge:**
  `packages/orchestration/decision_inbox.py` derives the whole inbox from
  `decision_queue.list_decisions` and adds NOTHING to storage — DECISION F031 D1
  rules the queue a derived read view, so that module performs no I/O, opens no
  path and keeps no state. `build_decision_inbox` is additive over
  `export_decision_json`: each card gains exactly three keys. `age_seconds`
  reads `created_at` as UTC when it is naive and clamps at 0, so a skewed clock
  reports 0 rather than a negative age. `blocked_count` seeds
  `dag_schedule.blocked_downstream` from `payload["task_id"]`, which only the
  `task_decision` branch sets, so every other type reports 0 through
  `blocked_downstream`'s own empty-seed branch and not through a special case.
  `answerable_by_decision_resolve` mirrors the write door's job-level refusals
  and is described under T003. No input makes the function raise: an unreadable
  stamp gives a None age and a non-UUID task id gives 0, and the card still
  renders, because losing the question is worse than showing it imperfectly.
  The route is `/api/jobs/<job_id>/decisions` through
  `ui_server._build_decisions_json`, scoped BY JOB — Remedy deliberately does
  NOT take a project argument here and never reads a second job, because a
  cross-job inbox would need a scoping rule the route does not have. The badge
  is `ui_server._count_open_decisions`, re-derived from the queue rather than
  counted off the event ledger (DECISION F031 D9).

- **T002 — the cards, the generic renderer, the order and the filter:**
  `apps/ui/src/api/decisionCard.ts` is the model layer and DECISION F031 D5
  keeps every real branch there, where the shipped vitest config can reach it.
  `decisionAnswers` prefers `payload.options` over `next_actions` for EVERY card
  without branching on the card's type, which is why
  `packages/orchestration/decision_queue.py` could give the flight-plan branch an
  `options` key of `approve` and `reject` and change no component at all.
  `decisionOrder.ts` holds DECISION F031 D6's urgency rule over age and blocked
  size and it is written down nowhere else; `decisionFilter.ts` derives the type
  chips from the models rather than from a list of known types;
  `decisionFocus.ts` resolves a card to the graph node its deep link jumps to.
  `apps/ui/src/components/panels/DecisionInboxCard.tsx` is a PROJECTION and the
  architecture line is enforced there by absence: nothing in that component
  dispatches on a decision's `type` or `status`, so a decision type this
  repository has not produced yet renders on the day some producer first emits
  it. No DOM test reaches that markup — the shipped vitest config collects
  `src/**/*.test.ts` and this repository has no DOM environment — so what guards
  it instead is `tests/ui_contracts/test_decision_answer_wiring.py`, which reads
  the comment-stripped source of the whole prop chain, together with
  `tsc --noEmit`.

- **T003 — the answer, end to end through the one write door:**
  the client chain is six small modules with one job each. `decisionNonce.ts`
  mints the client nonce and nothing else does; `decisionAnswer.ts` builds the
  `decision.resolve` body; `decisionSend.ts` turns it into a request carrying
  the per-run token; `decisionSubmit.ts` is the single network call and returns
  a closed three-value outcome; `decisionOutcome.ts` words the result;
  `decisionAnswerFlow.ts` sequences them and is the only module in the chain
  that creates a timer. `decisionClarificationForm.ts` keys a clarification
  field while the operator types and collects one decision's fields on submit.
  The server side is `ui_server._dispatch_decision_resolve`, which DECISION F031
  D24 gives TWO branches: an `fp:`-prefixed id goes to
  `flight_plan.resolve_flight_plan_approval` — the half DECISION F009 D5 planned
  and did not land — and every other id to `escalation.answer_task_decision`.
  The per-run token travels as a PROP from `RemedyApp.tsx` through `RemedyShell`
  and `RightLivePanel` to the card, because one credential should have one
  source and a component that re-read the URL would be a second.

**What this feature deliberately does not answer.** Six of the eight producing
branches of `list_decisions` — `pa:`, `sr:`, `tf:`, `dirty_repo`, the budget id
and `mem:` — have no package-level resolve verb for the door to dispatch to.
DECISION F031 D19 reads "Acceptance"'s "every producer type renders and answers
correctly from fixtures" as TASK DECISIONS PLUS FLIGHT-PLAN APPROVALS for this
feature's close and rules the other six out of scope. They still RENDER, and the
inbox tells the truth about them: their `next_actions` appear as pasteable text
rather than as a button the write door would refuse with a 409. Finding R-0693
carries the measurement that produced this ruling.
<<<END BUILTSTATE67
