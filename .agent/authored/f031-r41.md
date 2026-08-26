── STEP T003 record and hand off / F031 — ROUND R41 ───────────────────
Goal:        Register the one finding the R40 gate raised, record R40's PASS,
             and leave the branch in a state the next session can resume from
             without reading this one. No code and no test changes this round.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the plan
             · C2 the finding, in its own commit · C3 the R40 gate entry · C4
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f031-r41.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/handoff.md`. NO FILE OUTSIDE `.agent/` — a single path
             under `apps/`, `tests/`, `docs/`, `packages/` or anywhere else is a
             block condition, not a deviation.

Constraints:
 1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. If a slice looks wrong, STOP and say so in the handback
    instead of correcting it — a corrected slice destroys the transport proof.
 2. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4. The finding lands at C2
    BEFORE the gate entry, so a session that dies mid-round still leaves the
    record complete. C2 and C3 may not be reordered.
 3. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R40. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 4. THE FINDING IS THE REVIEWER'S TEXT. You never write a `Done:` paragraph and
    never edit a finding's wording. R-0691 is registered here and deliberately
    NOT fixed here — its fix is routed to the integration-gate round, which the
    plan slice says in as many words.
 5. THE LEDGER SETS MOVE TWICE, AND ONLY AS STATED. Across C2 `^- R-\d+ — `
    moves 251 to 252, the id ADDED is exactly `R-0691`, the ids REMOVED are
    EMPTY, and all ids stay DISTINCT. Across C3 `^Gate: F\d+ R\d+ — ` moves 21
    to 22 with the ADDED key exactly `F031 R40`. Across BOTH,
    `^Done: R-\d+ — ` stays 5, `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays
    19. The open set is 246 before C2 and 247 after.
 6. RE-READ `.agent/STOP` FROM DISK before C0a and again before C4. If it exists
    at either reading, finish the commit in hand, write the handback and STOP.
    Never create it, never delete it.
 7. SCRATCH LIVES UNDER `.remedy-wt/` and is removed BY ITS EXACT PATH, never by
    a glob. Nothing under `.remedy-wt/` is ever committed. This round needs no
    worktree; if you create none, report that rather than reporting a removal
    you did not perform.
 8. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `cp`, and every form of environment assignment. Route anything
    that counts, hashes or compares through `python3 - <<'PY'`, read real exit
    codes from `subprocess.run(...).returncode`, and copy with
    `shutil.copyfile`. Keep each heredoc modest in size — a very long one is
    rejected by the parser outright.

Done when — run every gate yourself and record its REAL exit code. G1 through G6
run at commits STRICTLY EARLIER than C4, so the handback can quote them; the
push is ordered after C4 and its reading is NOT written into the handback — the
reviewer takes that reading at the next gate.
 G1. BRANCH, CLEANLINESS, TRANSPORT. Branch is `feature/f031-decision-inbox`.
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2 and
     C3. `.agent/STOP` read from disk before C0a and before C4, both ABSENT.
     Report the sha256, byte count and line count of this block as saved at C0a,
     as mirrored at C0b, and as read off disk at C3 — all three must be EQUAL —
     and say whether C0a and C0b are the same git blob.
 G2. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES, never from the prompt. Report how many slices your
     extractor printed, the CONTENT line total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE — the `<<<SLICE` and `<<<END`
     lines count toward PROSE, not CONTENT, and R40's two readers agreed on that
     convention. PROSE must be at most 400 and TOTAL at most 490.
 G3. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF031R41 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, and `wc -l` strictly under 50.
 G4. THE TWO APPENDS, EACH PROVED SEPARATELY. `.agent/live_review.md` at C2
     equals its pre-commit blob plus ONE newline plus FINDINGS41, and at C3
     equals ITS pre-commit blob plus ONE newline plus LEDGER41 — report both
     byte counts and the sum for EACH; the pre-commit blob for C2 is 817669
     bytes. For EACH, confirm with a SECOND, independent reader: split on blank
     lines, report how the unit count moves from 341, and check the last unit
     equals that slice's paragraph. BOTH SLICES ARE SINGLE PARAGRAPHS this
     round, so an in-slice ordered-swap control is degenerate for each — a
     one-element reversal is the identity. Run the swap CROSS-SLICE instead,
     FINDINGS41's paragraph against LEDGER41's, and report it FALSE both ways,
     rather than reporting a passing control neither slice can produce. For
     EACH, flip ONE byte IN MEMORY and report that both readers REJECT it. Never
     mutate the tracked file.
 G5. THE LEDGER SETS. Report every count constraint 5 names at three points —
     before C2, after C2, after C3 — plus the ids ADDED and REMOVED as sets at
     each step, whether all ids are DISTINCT, and the maximum id. Report the
     open set as `^- R-\d+ — ` minus `^Done: R-\d+ — ` before C2 and after C3.
 G6. MARKERS, PATHS, COMMITS. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0
     and 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md` at C3,
     against a CONTROL count over the C0a blob, which is not 0. Report
     `git diff --name-only 3afdb209..C3` and compare it BOTH WAYS against the
     change set above. Report each commit's insertions from `git diff --numstat`,
     confirm each is single-parent and under 500. Report `git ls-files .remedy-wt`
     as 0 and `git worktree list` as 1 line at C3. Report the reflog for this
     round's commits: every operation prefix must read `commit`, and `amend`,
     `rebase` and `cherry` must be 0 each.
 G7. THE STATE READERS AND THE CANARY, in the PRIMARY checkout at C3 and
     SERIALLY — never two pytest processes alive at once, which produces false
     reds. This round rewrites `.agent/` state, which is exactly what these
     four read. Run and report the real exit code and count of each:
     `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
     `tests/regression/test_resource_safety.py`,
     `tests/orchestration/test_integrity_gate.py`, and the canary
     `tests/cli/test_golden_path.py`. At `3afdb209` these read 480, 52, 21, 16
     and 42. ALSO run `tests/ui_contracts/`, which must be UNCHANGED at 556
     passed with 4 skipped — this round adds no test, so any movement there is a
     real finding and not a number to absorb. Any other movement is a reported
     number, not a silence.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C4: feature and round, branch, the per-commit changed-files table
             with the `+/-` column taken from `git diff --numstat` itself and
             agreeing cell for cell with G6, the item-status table covering C0a,
             C0b, C1, C2, C3, C4 and the push, ONE LINE PER GATE for G1 through
             G7 with its real exit code, an explicit line for R-0691 saying what
             was registered and that it was deliberately NOT fixed here, the
             open-findings count, and the next expected action. THE NEXT ACTION
             SECTION NAMES, IN THIS ORDER: re-read `.agent/STOP` from disk
             first, then the Open PR Gate, then review this round's handback,
             then the clarification FORM round. That order is Phase 1 of
             docs/agents/self_drive_protocol.md and a handoff that inverts it
             sends the next session past a sentinel it must honour. Derive your
             line cap from AGENTS.md yourself, from the commit count you
             actually made; if the mandated content genuinely does not fit,
             declare the DECISION D15 overage with its stated cause. Then push
             with `git push origin feature/f031-decision-inbox`.
──────────────────────────────────────────────────────────────────────

<<<SLICE PLANF031R41
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
R41 registers the one finding the R40 gate raised and records R40's PASS. It is
a state round: no code, no test. R-0691 is registered and deliberately NOT fixed
here — a substring guard cannot hold an "and nothing else" clause, so the repair
is a naming repair and it is routed to the integration-gate round rather than
earning a fourth consecutive round of guard hardening.

## Next Steps
1. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
2. The integration-gate round per `docs/agents/integration_gate.md`, whose block
   also carries the checklist items R-0683, R-0377, R-0419, R-0429, R-0560,
   R-0582, R-0583, R-0633 and R-0691 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- NO DOM HARNESS REACHES THE INBOX MARKUP, and it has now produced findings in
  three consecutive rounds. The shipped vitest config collects
  `src/**/*.test.ts`, so the wiring is gated by comment-stripped SOURCE reading
  and by `tsc --noEmit`, never by a rendered click. R-0686 and R-0687 were the
  markup itself; R-0689, R-0690 and R-0691 are the guards written to close them.
  A guard over source text pins what a string CONTAINS and what an enumerated
  list EXCLUDES; it cannot pin "and nothing else", and a name that says
  otherwise is the recurring defect.
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the seam DECISION F031 D18 chose
  carries no handle, so when the submit wins the 20-second timer still fires.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires — every
  `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 246 at
  `3afdb209` and this round takes it to 247.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684,
  R-0685 and R-0691; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R41

<<<SLICE FINDINGS41
- R-0691 — Low, AN ASSERTION NAMED "AND NOTHING ELSE" CHECKS A PRESENCE AND AN EXCLUSION LIST, WHICH IS NOT THE SAME CLAIM. Raised by the reviewer at the R40 gate against `tests/ui_contracts/test_decision_answer_wiring.py` as committed at `05bdeae1`. THE MEASUREMENT, run by the reviewer in a disposable worktree at `3afdb209` and never in the primary checkout: adding a second, foreign key inside `withAnswerKey` — `next.add(answerKey);` followed by `next.add(answerKey + "-x");` — marks an answer in flight that nobody pressed and disables a button the operator never touched, which is R-0687's consequence reached from the other side, and `python3 -m pytest tests/ui_contracts/test_decision_answer_wiring.py -q` stayed at REAL exit 0 with all 31 passing. `test_the_add_helper_adds_the_passed_key_and_nothing_else` requires `next.add(answerKey)` to be PRESENT and `test_neither_helper_carries_a_bulk_operation` excludes `.clear(` and `new Set()`; neither can see an extra operation that is on the enumerated list of neither. The remover carries the same gap by the same construction. THE WORKER IS NOT AT FAULT AND ITS SIX RED PROOFS ARE CORRECT AS RUN: S1 of the R40 block ordered "touch ONLY the passed key", which is an obligation no substring predicate can fully discharge, and the worker wrote the strongest pair of predicates that shape allows — presence plus an exclusion list — and proved each capable of failing. THE SEVERITY IS LOW AND THE REASON IS PART OF THE FINDING: the surviving mutation is contrived, no refactorer writes a second `add` of a synthesised key, and every natural regression the reviewer tried was caught, including the two that survived R39 and a decoy `aria-live` node planted to misaim the R40 reader. WHAT IS ACTUALLY WRONG IS THE NAME: "and nothing else" is a completeness claim, the predicate underneath it is a containment claim, and a reader who trusts the name stops looking. THE FIX IS A NAMING FIX, NOT MORE GUARD: rename both assertions to say what they hold — that the helper adds, or deletes, the key it was handed — and state the residual in the class docstring, so the next reader knows a source guard's reach ends where "and nothing else" begins. Routed to the integration-gate round; three consecutive rounds of guard hardening is enough, and this one changes no behaviour.
<<<END FINDINGS41

<<<SLICE LEDGER41
Gate: F031 R40 — the F031 R40 entry. R40 PASSED ON EVERY ONE OF ITS EIGHT GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, including all seven per-commit insertion counts, every cell of its `## Commits` table and all eight suite counts. THIS IS THE ROUND THAT GAVE THE GUARDS THE REACH THEIR NAMES CLAIMED. R-0689 is FIXED: the new class `TestTheInFlightHelpersTouchOnlyTheirOwnKey` reads the EXTRACTED BODY of `withAnswerKey` and of `withoutAnswerKey` through a brace-matching reader `ts_function_body` rather than sweeping the file, and pins per body that it copies before it changes, that it names the key it was handed, and that it carries no bulk operation — with a cross-check that neither body is the other's, which is the failure mode a brace reader actually has. R-0690 is FIXED: `jsx_between_answer_button_and_live_paragraph` takes the comment-stripped source between the answer button's closing tag and the `<p` carrying the last `aria-live="polite"`, and the new `test_the_region_is_created_under_no_conditional_operator_at_all` forbids `?`, `&&` and `||` anywhere in it, while the old literal check is kept VERBATIM and only renamed to `test_the_null_ternary_shape_r0686_was_registered_against_is_absent` — the rename is the single deletion in the whole commit. TRANSPORT HELD for the twelfth round running: the C0a blob, the C0b blob and both working copies read off disk are ALL FOUR byte-identical at sha256 `236f665d12e4dc7d9dda32a512b531dc9b982f3038fd698ce42027bc1a8e8f7a` over 24444 bytes and 241 lines, C0a and C0b resolving to the SAME git blob `662d158d`. THE CAPS HELD AND BOTH READERS AGREED THIS TIME, which is the R39 lesson landing: 3 slices, TOTAL 241, CONTENT 52, PROSE 189, markers counted as PROSE by the worker's extractor and by the reviewer's alike, against caps of 490 and 400. THE PLAN at `ef3bd0d3` equals PLANF031R40 exactly at 2771 bytes and 48 lines, minus-newline control FALSE, `^## Goal$` 1, `^## Next Steps$` 1. THE TWO APPENDS ARE EXACT: 809140 + 1 + 3246 = 812387 against an actual 812387, and 812387 + 1 + 5281 = 817669 against an actual 817669, each pre-commit blob a byte-exact prefix, blank-line units 338 to 340 to 341 with the last units equal to each slice's paragraphs IN ORDER, the in-slice swap FALSE for FINDINGS40 and the cross-slice swap FALSE for the single-paragraph LEDGER40, whose own reversal the worker correctly declared degenerate rather than reporting as a passing control. THE SETS MOVED ONLY WHERE CONSTRAINT 7 ALLOWED: `^- R-\d+ — ` 249 to 251 to 251 with ADDED across C2 exactly {`R-0689`, `R-0690`}, ADDED across C3 EMPTY, REMOVED EMPTY at both, all 251 DISTINCT, maximum `R-0690`; `^Done: R-\d+ — ` 5 throughout, `^Landed: R-` 0 throughout, `^Gate: R\d+ — ` 19 throughout, `^Gate: F\d+ R\d+ — ` 20 to 20 to 21 with the ADDED key exactly `F031 R39`; open set 244 before C2 and 246 after C3. MARKERS 0 and 0 in the plan at `ef3bd0d3` and the ledger at `cbb021d6` against a live CONTROL of 3 and 3. THE CHANGE SET IS EXACT IN BOTH DIRECTIONS at 6 paths over the full range and 5 over `14fde389`..`05bdeae1`, declared-minus-range exactly `.agent/handoff.md` which C4 writes, and — the constraint this round existed to honour — NOT ONE PATH UNDER `apps/`: the component was not edited to suit a guard. THE SIX COMMITS BEFORE THE HANDBACK ARE EACH SINGLE-PARENT at insertions 241, 139, 13, 4, 2 and 103, each under the 500 DECISION F104 D1 counts, the handback itself 42; the reflog reads `commit` in every prefix, so `amend`, `rebase` and `cherry` are 0 each; `git ls-files .remedy-wt` is 0 and `git worktree list` is 1 line. THE GATES THE REVIEWER RE-RAN: `npx tsc --noEmit` REAL exit 0 with no diagnostic, `npx vitest run` REAL exit 0 at 30 files and 448 tests IDENTICAL to base as a round touching no compiled file must be, the guard file at 31 collected against 25 at base, and the state readers and canary SERIALLY at 480, 52, 21, 16, 556 passed with 4 skipped, and 42 — `tests/ui_contracts/` moving 550 to 556, which is EXACTLY the 6 test functions the guard file gained. THE REVIEWER THEN RAN FOUR MUTATIONS OF ITS OWN AND THREE WENT RED, INCLUDING BOTH THAT SURVIVED R39: `next.delete(answerKey)` becoming `next.clear()` now fails `::test_the_remove_helper_deletes_the_passed_key_and_nothing_else` and `::test_neither_helper_carries_a_bulk_operation` at REAL exit 1, 2 failed and 29 passed; wrapping the live paragraph in `{outcome === null ? undefined : ( ... )}` now fails `::test_the_region_is_created_under_no_conditional_operator_at_all` at REAL exit 1; and the same wrap PLUS a decoy `<p aria-live="polite">` planted after it — an attempt to misaim the new reader's `rindex` at the wrong node — fails identically, so the reader's aim survives the attack its own docstring worries about. The fourth survived and is registered as R-0691. THE ONE DEVIATION THE WORKER DECLARED IS ACCEPTED AND IS NOT A BLOCK CONDITION: S2 said the region between the button and the paragraph "is whitespace once comments are stripped" while on disk it is whitespace plus the bare `{}` the stripper leaves where the JSX comment stood; the worker shipped the assertion exactly as ordered rather than rewording the spec or touching the component, and `{}` holds none of `?`, `&&` or `||`, so the assertion is tight and the reviewer's sentence was merely imprecise. NO BLOCK CONDITION AROSE: no fabricated value, no false live indicator, no missing table, no unverified claim, no silent scope change. R40 closed both of R39's findings and left one narrower than either.
<<<END LEDGER41
