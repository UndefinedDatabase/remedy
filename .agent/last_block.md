── STEP T003 rule and record / F031 — ROUND R42 ───────────────────────
Goal:        Record R41's PASS, register the two findings its gate raised,
             repair the 51-line plan R41 shipped, and land DECISION F031 D19
             with its roadmap mirror. No code and no test changes this round.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the two findings, in their own commit · C3 the R41 gate entry
             · C4 DECISION F031 D19 · C5 the feature-file amendment · C6
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r42.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `docs/roadmap/features/T5_F031.md`,
             `.agent/handoff.md`. NO FILE UNDER `apps/`, `tests/` or
             `packages/` — a single path there is a block condition, not a
             deviation.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, say so in the handback and finish the
    round anyway — a corrected slice destroys the transport proof, and stopping
    early would lose the record this round exists to write. This wording
    replaces R41's "STOP and say so", which R-0692 records as unmeetable beside
    constraint 2.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The findings
    land at C2 BEFORE the gate entry at C3, so a session that dies mid-round
    still leaves the record complete. No pair may be reordered.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R41. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 4. THE FINDINGS AND THE DECISION ARE THE REVIEWER'S TEXT. You never write a
    `Done:` paragraph, never edit a finding's wording, and never edit D19.
    R-0692 and R-0693 are registered here and deliberately NOT fixed here: the
    plan repair R-0692 asks for IS C1's slice, and R-0693's repair is the
    three-round programme D19 rules, which starts at R43.
 5. THE FOUR APPEND TARGETS EACH GAIN EXACTLY ONE BLOCK OF TEXT, appended as
    ONE newline plus the slice, and nothing anywhere else in those files
    changes. `.agent/live_review.md` twice, `.agent/decisions.md` once,
    `docs/roadmap/features/T5_F031.md` once. `.agent/plan.md` is the only
    WHOLE-FILE replacement.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 7. SCRATCH LIVES UNDER `.remedy-wt/` and is removed BY ITS EXACT PATH, never by
    a glob. Nothing under `.remedy-wt/` is ever committed. This round needs no
    worktree; if you create none, report that rather than reporting a removal
    you did not perform. `.remedy-wt/f031-r42-block.md` is the reviewer's own
    scratch copy of this block — leave it alone, do not delete it.
 8. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, brace literals containing a quote character, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through `python3 - <<'PY'`, read real exit codes from
    `subprocess.run(...).returncode`, build dicts with `dict(key=value)` rather
    than a brace literal, and copy with `shutil.copyfile`. Keep each heredoc
    modest in size — a very long one is rejected by the parser outright.

Done when — run every gate yourself and record its REAL exit code. G1 through G8
run at commits STRICTLY EARLIER than C6, so the handback can quote them; the
push is ordered after C6 and its reading is NOT written into the handback — the
reviewer takes that reading at the next gate.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3,
     C4 and C5. `.agent/STOP` read from disk before C0a and before C6, both
     ABSENT. Report the sha256, byte count and line count of this block as saved
     at C0a, as mirrored at C0b, and as read off disk at C5 — all three must be
     EQUAL — and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE — the `<<<SLICE` and `<<<END`
     lines count toward PROSE, not CONTENT, which is the convention R40's and
     R41's readers both used. PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R42 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` STRICTLY UNDER 50. This gate is why the
     round exists: R41 shipped 51 and R-0692 records it, so a red here is a
     block condition rather than a declared deviation.
 G4. THE TWO LEDGER APPENDS, EACH PROVED SEPARATELY. `.agent/live_review.md` at
     C2 equals its pre-commit blob plus ONE newline plus FINDINGS42, and at C3
     equals ITS pre-commit blob plus ONE newline plus LEDGER42 — report both
     byte counts and the sum for EACH; the pre-commit blob for C2 is 825662
     bytes. For EACH, confirm with a SECOND, independent reader: split on blank
     lines, report how the unit count moves from 343, and check that the last
     unit equals that slice's final paragraph. FINDINGS42 IS TWO PARAGRAPHS
     SEPARATED BY A BLANK LINE, so its in-slice ordered-swap control is REAL —
     run it and report it FALSE. LEDGER42 is a single paragraph, so its own
     reversal is the identity: declare that degenerate and run the swap
     CROSS-SLICE against FINDINGS42's last paragraph instead, FALSE both ways.
     For EACH, flip ONE byte IN MEMORY and report that both readers REJECT it.
     Never mutate the tracked file.
 G5. THE LEDGER SETS. Report at three points — before C2, after C2, after C3 —
     the line-anchored counts of `^- R-\d+ — `, `^Done: R-\d+ — `,
     `^Landed: R-`, `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, plus the ids
     ADDED and REMOVED as SETS at each step, whether all ids are DISTINCT, and
     the maximum id. Across C2 `^- R-\d+ — ` moves 252 to 254 with ADDED exactly
     the pair `R-0692` and `R-0693` and REMOVED empty; across C3 it does not
     move. `^Gate: F\d+ R\d+ — ` moves 22 to 23 across C3 with the ADDED key
     exactly `F031 R41`. `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and
     `^Gate: R\d+ — ` stays 19 at all three points. Report the open set as
     `^- R-\d+ — ` minus `^Done: R-\d+ — `: 247 before C2 and 249 after C3.
 G6. THE DECISION AND THE AMENDMENT, EACH PROVED THE SAME WAY. `.agent/decisions.md`
     at C4 equals its pre-commit blob of 599241 bytes plus ONE newline plus
     DECISION19, and `docs/roadmap/features/T5_F031.md` at C5 equals its
     pre-commit blob of 9804 bytes plus ONE newline plus AMEND42. Report both
     byte counts and the sum for EACH, and confirm each with the blank-line
     reader: decisions.md moves from 1439 units and the feature file from 21,
     and in EACH the last unit equals that slice's final paragraph. Report
     `^## DECISION F031 D\d+ ` in `.agent/decisions.md` as 18 before C4 and 19
     after, and `^## Design amendments ` in the feature file as 3 before C5 and
     4 after. Flip ONE byte IN MEMORY for EACH and report that both readers
     REJECT it.
 G7. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1, in `.agent/live_review.md` at C3, in
     `.agent/decisions.md` at C4 and in the feature file at C5, against a
     CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only 3afdb209..C5` and compare it BOTH WAYS against this
     block's change set — the range covers R41's four paths as well, so state
     the expected union rather than the five paths this round writes. Report
     each commit's insertions from `git diff --numstat`, confirm each is
     single-parent and under 500. Report `git ls-files .remedy-wt` as 0 and
     `git worktree list` as 1 line at C5. Report the reflog for this round's
     commits: every operation prefix must read `commit`, and `amend`, `rebase`
     and `cherry` must be 0 each.
 G8. THE READERS, THE DOCS GATES AND THE CANARY, in the PRIMARY checkout at C5
     and SERIALLY — never two pytest processes alive at once, which produces
     false reds. This round rewrites `.agent/` state, which the four state
     readers read, and it edits `docs/roadmap/**`, which the two docs gates
     read. Run and report the real exit code and count of each:
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, `tests/docs/`,
     `tests/orchestration/test_roadmap_index.py`, and the canary
     `tests/cli/test_golden_path.py`. At `59521bf5` these read 480, 52, 21, 16,
     295, 30 and 42. ALSO run `tests/ui_contracts/`, which must be UNCHANGED at
     556 passed with 4 skipped — this round adds no test, so any movement there
     is a real finding and not a number to absorb. Any other movement is a
     reported number, not a silence. ON ANY RED, CAPTURE THE `FAILED` NODE IDS
     BEFORE ANYTHING ELSE and re-run that suite ALONE five more times, reporting
     every reading and every node id. The reviewer saw ONE unexplained red of
     `tests/orchestration/test_test_runner.py` in 20 dry-run executions of this
     round's own slices and could not reproduce it; a red you cannot reproduce
     is reported WITH its node ids, never absorbed and never retried into
     silence.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G7, the item-status table covering C0a,
             C0b, C1, C2, C3, C4, C5, C6 and the push, ONE LINE PER GATE for G1
             through G8 with its real exit code, an explicit line for R-0692 and
             R-0693 saying what was registered and that neither was fixed here,
             the open-findings count, and the next expected action. THE NEXT
             ACTION SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from
             disk first, then the Open PR Gate, then review this round's
             handback, then R43 — the endpoint's third derived key and the card
             that renders no button the door refuses. That order is Phase 1 of
             docs/agents/self_drive_protocol.md and a handoff that inverts it
             sends the next session past a sentinel it must honour. Derive your
             line cap from AGENTS.md yourself, from the commit count you
             actually made; if the mandated content genuinely does not fit,
             declare the DECISION D15 overage with its stated cause. Then push
             with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R42
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D19.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R42 records R41's PASS, registers the two findings that gate raised, repairs the
51-line plan R41 shipped, and lands DECISION F031 D19 with its roadmap mirror.
It is a state round: no code, no test. Neither finding is fixed here — R-0692's
repair IS this file, and R-0693's is the three-round programme D19 rules.

## Next Steps
1. R43: `build_decision_inbox` gains a third derived key and the card renders no
   button the door refuses — D19 clause one and clause three.
2. R44: the `fp:`-prefixed dispatch DECISION F009 D5 planned and did not ship,
   reusing `flight_plan.resolve_flight_plan_approval`. Then R45: the
   clarification FORM over `payload.clarifications`.
3. The integration-gate round per `docs/agents/integration_gate.md`, then
   closure per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- SEVEN OF THE EIGHT PRODUCING TYPES CANNOT BE ANSWERED THROUGH THE DOOR, and
  every one ships an enabled button today. `escalation.find_task_decision`
  matches escalation records alone, so at `59521bf5` every id but a task
  decision's is answered 409. R-0693 measures it and D19 rules the repair.
- NO DOM HARNESS REACHES THE INBOX MARKUP. `apps/ui/vitest.config.ts` collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  and by `tsc --noEmit`, never by a rendered click. R-0689, R-0690 and R-0691
  guard that gap, and a source guard pins containment, not completeness.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- Open findings, by the rule DECISION F009 D10 requires — every `^- R-\d+ — `
  paragraph minus every `^Done: R-\d+ — ` line — the set is 247 at `59521bf5`
  and this round takes it to 249.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685, R-0691, R-0692 and R-0693; R-0495, R-0574 and R-0693 are the Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R42

<<<SLICE FINDINGS42
- R-0692 — Medium, REVIEWER-BLOCK DEFECT, A WHOLE-FILE PLAN SLICE WAS EMITTED AT 51 LINES AGAINST ITS OWN BLOCK'S UNDER-50 CLAUSE, AND `.agent/plan.md` HAS BEEN OVER THE AGENTS.md CAP ON DISK SINCE `813aa914`. Raised by the reviewer against its OWN R41 block. THE MEASUREMENT, re-run at `59521bf5`: `.agent/plan.md` at `813aa914` is byte-equal to PLANF031R41 newline-included at 3002 bytes, the minus-trailing-newline control is FALSE, `^## Goal$` is 1 and `^## Next Steps$` is 1 — every clause of G3 holds except `wc -l`, which reads 51 against a clause requiring strictly under 50, and AGENTS.md's own `plan.md` rule ("keep it short (<50 lines)") is therefore broken on disk at HEAD. THIS IS THE THIRD OCCURRENCE OF ONE CLASS: R-0423 recorded a 52-line slice against an under-50 constraint, R-0654 recorded a 51-line slice against an at-most-50 clause of the same gate, and both wrote the same remedy — measure a whole-file slice against the cap that binds its TARGET before emission. WHAT IS NEW AND WHAT MAKES THIS MEDIUM RATHER THAN LOW IS THAT THE REMEDY ALREADY REACHED THE CHECKLIST AND STILL DID NOT BIND: docs/agents/planner_reviewer_prompt.md §3 item 3 reads "Count every authored full-replacement text against its own file's cap before emission: `.agent/plan.md` under 50 lines (AGENTS.md)" and the R41 block was emitted anyway, so the failure is not a missing rule but an unexecuted one, and no gate in this repository reads the reviewer's compliance with §3 before a block is delegated. THE WORKER IS NOT AT FAULT: item 3's own last sentence rules that "a worker required to apply a slice byte for byte cannot trim it, so an oversize replacement lands a live rule violation on disk and the worker is right to declare it rather than fix it", which is exactly what the R41 worker did. A SECOND DEFECT OF THE SAME BLOCK IS RECORDED HERE RATHER THAN SEPARATELY, because it has one repair: R41's constraint 1 says "If a slice looks wrong, STOP and say so in the handback", while its constraint 2 says the finding must land at C2 before the gate entry at C3 "so a session that dies mid-round still leaves the record complete" — a worker that obeyed the STOP literally would have lost the record the round existed to write, and R-0654's worker DID halt at C1 on this same conjunction and was ruled correct, so the two precedents point opposite ways. THE FIX IS THIS ROUND: C1 of R42 carries a plan slice measured under 50 before emission, and R42's constraint 1 replaces "STOP and say so" with "say so in the handback and finish the round anyway". No code and no test is involved in either half.

- R-0693 — High, SEVEN OF THE EIGHT PRODUCING DECISION TYPES CANNOT BE ANSWERED THROUGH THE WRITE DOOR, AND THE INBOX SHIPS AN ENABLED BUTTON FOR EVERY ONE OF THEM. Raised by the reviewer at the R41 gate while measuring the seam the clarification FORM round would have built on. THE MEASUREMENT, run in-memory at `59521bf5` against stub jobs and never against a stored job: `packages/orchestration/ui_server.py::_dispatch_decision_resolve` calls `escalation.answer_task_decision` and nothing else, and a None return is audited `rejected_state` and answered 409 at line 3634, which that method's own docstring states. `escalation.find_task_decision` iterates `escalation_records(job)` alone, so of the eight branches of `decision_queue.list_decisions` only branch 8 — task decisions, whose id IS `record["decision_id"]` — can be found. Probed directly, `answer_task_decision` returned None for `pa:i1`, `sr:s1`, `tf:t1`, `dirty_repo`, `budget:b1`, `mem:k1` and `fp:approval`, and returned a record for `td:abc12345`. `apps/ui/src/components/panels/DecisionInboxCard.tsx` renders EVERY entry of `decision.answers` as an enabled `<button>` whose `onClick` posts `answer.value` through `answerDecisionCard`, and `decisionCard.ts::decisionAnswers` falls back to `next_actions` as `kind: "command"` when the payload carries no `options` — so a flight-plan card offers a button labelled `remedy decision resolve abcdef12 fp:approval --reason approve` which posts that CLI line as the answer text and is refused 409. THE FEATURE'S OWN ACCEPTANCE IS UNMEETABLE AS WRITTEN while this stands: T5_F031 requires that "every producer type renders and answers correctly from fixtures" and that answering "round-trips through the write channel into the same effects the CLI produces". PART OF THIS IS AN UNSHIPPED HALF OF ANOTHER FEATURE'S OWN PLAN: `.agent/decisions.md` records under F009 that "`decision.resolve` dispatches — a task decision to `escalation.answer_task_decision` followed by `save_job`, an `fp:`-prefixed id to `resolve_flight_plan_approval` — and the seam is gone when that round ends", and `flight_plan.resolve_flight_plan_approval` exists and its docstring says it was extracted "so the UI write door can reach the SAME code the CLI has always run" — yet `grep resolve_flight_plan_approval packages/orchestration/ui_server.py` returns nothing and the CLI is its only caller. HIGH BECAUSE IT IS OPERATOR-VISIBLE AND SILENT ON THE WAY IN: the button looks live, the failure is a toast after a round trip, and the operator has no way to learn from the surface which of their questions this door can take. DECISION F031 D19, landed at C4 of this round, rules the repair in three rounds and none of it happens here.
<<<END FINDINGS42

<<<SLICE LEDGER42
Gate: F031 R41 — the F031 R41 entry. R41 PASSED ON EVERY GATE IT COULD CONTROL AND ITS ONE RED IS THE REVIEWER'S OWN, AND THE REVIEWER RE-RAN ALL SEVEN GATES ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly. G1: the block is byte-identical at sha256 `0a70adced995e7ed78d9d14cdd91ea660f13192ea77413918ca50dab8fe4fe38` over 20004 bytes and 184 lines as the C0a blob, as the C0b blob and as both working copies read off disk, C0a and C0b resolving to the SAME git blob `491e5cd3` — the thirteenth round running that transport held. G2: 3 slices, TOTAL 184, CONTENT 53, PROSE 131 against caps of 490 and 400, markers counted as PROSE by both readers as R40 agreed. G3 IS THE RED AND IT IS THE BLOCK AUTHOR'S: `.agent/plan.md` at `813aa914` is byte-equal to PLANF031R41 at 3002 bytes with the minus-newline control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and `wc -l` reads 51 against a clause requiring strictly under 50 — the two clauses of the reviewer's own gate cannot both hold, the worker shipped the slice byte for byte as constraint 1 requires and declared the breach rather than trimming it, which docs/agents/planner_reviewer_prompt.md §3 item 3 rules is the correct choice, and the defect is registered as R-0692 against the reviewer. G4: 817669 + 1 + 2338 = 820008 against an actual 820008 and 820008 + 1 + 5653 = 825662 against an actual 825662, each pre-commit blob a byte-exact prefix and each whole-file identity TRUE, blank-line units 341 to 342 to 343 with the last unit equal to each slice's paragraph, both cross-slice swaps FALSE, both in-memory byte flips REJECTED by both readers, and the single-paragraph in-slice reversals correctly declared degenerate rather than reported as passing controls. G5: `^- R-\d+ — ` 251 to 252 to 252 with ADDED across C2 exactly `R-0691`, ADDED across C3 EMPTY, REMOVED EMPTY at both, all ids DISTINCT at all three points and the maximum `R-0691`; `^Done: R-\d+ — ` 5, `^Landed: R-` 0 and `^Gate: R\d+ — ` 19 throughout; `^Gate: F\d+ R\d+ — ` 21 to 21 to 22 with the ADDED key exactly `F031 R40`; open set 246 before C2 and 247 after C3. G6: markers 0 and 0 in the plan at `813aa914` and the ledger at `51a1b735` against a live CONTROL of 3 and 3 over the C0a blob; the change set is exact in BOTH directions at 4 paths over `3afdb209`..`51a1b735`, all under `.agent/`, declared-minus-range exactly `.agent/handoff.md` which C4 writes; insertions 184, 112, 17, 2 and 2, each single-parent and each far under 500, the handback itself 35; every reflog prefix reads `commit` so `amend`, `rebase` and `cherry` are 0 each; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. G7: the four state readers, the canary and the contracts suite re-run SERIALLY by the reviewer in the primary checkout at REAL exit 0 and at 480, 52, 21, 16, 42 and 556 passed with 4 skipped — every reading IDENTICAL to the `3afdb209` baseline, as a round that adds no test must show. THE HANDBACK ITSELF WAS AUDITED AS AN ARTIFACT: every `+/-` cell equals `git diff --numstat`, the item-status table covers all seven ordered items, one line per gate carries a real exit code, and its 85 lines sit inside the 100-line tier that six tabled commits earn. NO BLOCK CONDITION AROSE: nothing fabricated, no false green — the red gate is declared, not claimed — no missing table, no unverified completion claim and no silent scope change. R41 registered R-0691, recorded R40's PASS, and cost the branch one finding that belongs to the block author rather than to the worker.
<<<END LEDGER42

<<<SLICE DECISION19
## DECISION F031 D19 (2026-08-27) — the card offers no answer the door will refuse, and the door learns the one verb F009 extracted for it

CHOSEN, THE ENDPOINT DERIVES ANSWERABILITY AND THE BROWSER NEVER GUESSES IT.
`packages/orchestration/decision_inbox.py::build_decision_inbox` gains a THIRD
derived key beside `age_seconds` and `blocked_count`, computed with the SAME
predicate the door runs — whether `escalation.find_task_decision` finds the
decision's id — so the rule that decides what may be posted is written once, on
the side that owns the record. The docstring's "exactly two extra keys" sentence
moves with the code. The alternative of branching on `card.type` in
`decisionCard.ts` is REJECTED: `decisionAnswers` carries the architecture line
"MUST NOT branch on `card.type`", which is what lets a type this repository has
never produced render generically, and a second copy of the door's rule in the
browser is exactly the drift that line exists to prevent.

CHOSEN, A CARD THE DOOR CANNOT TAKE SHOWS ITS CLI LINE AS TEXT, NOT AS A BUTTON.
The `next_actions` strings are already the exact command an operator can paste —
`escalation.task_decision_answer_command` and `decision_queue`'s own `_actions`
build them for that purpose — so they stay visible and stop being posted. The
alternative of posting anyway and rendering the 409 is REJECTED: that is
R-0693's defect stated as a design, and it teaches the operator only by failing.

CHOSEN, F031 BUILDS THE `fp:`-PREFIXED DISPATCH RATHER THAN ROUTING IT AWAY.
`.agent/decisions.md` records under F009 that the door would dispatch an
`fp:`-prefixed id to `resolve_flight_plan_approval`, and that function exists
with a docstring saying it was extracted "so the UI write door can reach the
SAME code the CLI has always run" — so this is an unshipped CALL SITE for a verb
already built for this caller, not a new capability, and it touches neither the
nonce nor the audit behaviour `.agent/context.md` puts out of scope. Routing it
to F009 as DECISION F031 D14 routed the blank-answer check is REJECTED here for
one reason: F009 is CLOSED, and without this dispatch T003's clarification form
has no destination and the feature's own Acceptance stays unmeetable.

CHOSEN, THE OTHER SIX PREFIXES STAY UNANSWERABLE IN THE BROWSER FOR NOW. `pa:`,
`sr:`, `tf:`, `dirty_repo`, the budget id and `mem:` have no package-level
resolve verb at all, so each is a feature rather than a call site. They render,
they show their CLI line, and F031 claims nothing else about them.

CHOSEN, THE PROGRAMME IS THREE ROUNDS AND THE FORM IS LAST. R43 the derived key
and the card; R44 the `fp:` dispatch; R45 the clarification FORM over
`payload.clarifications`, whose records are `id`, `question`, `default_answer`
and `impact` and whose answers reach the CLI's `--answer <id>=<value>` semantics
through `apps/cli/commands/decision.py::parse_answer_options`. Building the form
first is REJECTED: it would post into a 409 and add a second false affordance.

REVERSE IT by deleting the third derived key, restoring the unconditional button
and dropping the `fp:` branch from the door. Nothing in the read endpoint's
existing two keys or in the CLI changes, so the reversal touches no other
feature.
<<<END DECISION19

<<<SLICE AMEND42
## Design amendments (F031 R42, 2026-08-27)

> This ruling SUPERSEDES the sentences it names above, on the same terms as the
> R5, R11 and R18 sections: the originals stay so this file records what was
> planned and then what was ruled. Rationale, alternatives and the reversal path
> are in `.agent/decisions.md` under DECISION F031 D19.

- **D19 — the card offers no answer the door will refuse.** "Acceptance" says
  "every producer type renders and answers correctly from fixtures" and "Goal &
  Done" says answering "round-trips through the write channel". Measured at
  `59521bf5`, `ui_server.py::_dispatch_decision_resolve` calls only
  `escalation.answer_task_decision`, whose `find_task_decision` matches
  escalation records alone, so of the eight producing branches of
  `list_decisions` only task decisions can be answered; the other seven are
  refused 409 while `DecisionInboxCard.tsx` renders an enabled button for each.
  Finding R-0693 carries the measurement. The read endpoint therefore derives a
  THIRD key saying whether the door can take this card, the card renders a
  non-answerable decision's `next_actions` as pasteable TEXT rather than as a
  posting button, and F031 ships the `fp:`-prefixed dispatch to
  `flight_plan.resolve_flight_plan_approval` that DECISION F009 D5 planned and
  did not land. "Answers correctly from fixtures" is read as TASK DECISIONS plus
  flight-plan approvals when this feature closes; `pa:`, `sr:`, `tf:`,
  `dirty_repo`, the budget id and `mem:` have no package-level resolve verb and
  are out of F031's scope. The clarification form of T003 lands after the
  dispatch, not before it.
<<<END AMEND42
