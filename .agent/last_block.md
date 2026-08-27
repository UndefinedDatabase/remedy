STEP R6 / F032 — T002a: THE BUDGET STOP GETS ITS RECEIPTS
Goal:        OPEN SESSION 2 AND START T002 BY UPGRADING THE FIRST PRODUCER.
             `TRIPLE_REQUIRED_TYPES` has been EMPTY since T001b, so the emit
             gate protects nothing in production. This round makes the budget
             stop carry real receipts — refs into the budget evidence it
             already computed, and one expected outcome and one downside per
             choice — and adds `token_budget` to that set in the SAME commit,
             which is what DECISION F032 D5 requires. It also books the R5
             verdict, which is PASS, and resolves `R-0711`. DECISION F032 D6
             rules where this card's options list comes from. YOU CREATE NO
             PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R5 verdict and `Done: R-0711` · C3 DECISION F032 D6
             and its feature-file amendment · C4 the budget triple, the gate
             set and the two retired comments · C5 its tests · C6 the
             handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r6.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `docs/roadmap/features/T5_F032.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G7 orders a disposable
             worktree and G8 orders a push. NOTHING under `apps/` is written.
             NO EXISTING TEST FILE other than the one this feature created is
             edited — if a guard elsewhere goes red, that is a real finding and
             you hand back rather than edit it.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r6.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r6.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    the points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations. Declaring beats fixing every time.
 3. THE PRODUCTION CODE IS SPECIFIED, NOT SLICED. Items S1 through S6 describe
    what the code must DO. You write it, in the house style of the module.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The verdict
    and the resolution land at C2, BEFORE the ruling at C3 and the code at C4 —
    the record moves first so nothing is lost if the session dies mid-round.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R5. That is
    ordered: the plan becomes current at C1.
 6. `.agent/live_review.md` AND `.agent/decisions.md` ARE APPEND-ONLY. Nothing
    already in either is rewritten, deleted, renumbered or touched. An
    append-only record is corrected by appending, never by editing.
 7. YOU AUTHOR NO RECORD TEXT OF YOUR OWN THIS ROUND. You mint no finding id,
    write no `Gate:` paragraph, no `Done:` paragraph and no `Landed:` line. The
    only text entering `.agent/live_review.md` is the LEDGER6 slice, which the
    reviewer wrote. If this round's work makes you believe a NEW finding
    exists, DO NOT register it — describe it in the handback under Deviations
    and let the reviewer mint it.
 8. THE LEDGER SETS MOVE AS FOLLOWS. Across C2: `^Gate: F\d+ R\d+ — ` moves 57
    to 58 with the ADDED key exactly `F032 R5`; `^Done: R-\d+ — ` moves 21 to
    22 with the ADDED id exactly `R-0711`; `^- R-\d+ — ` stays 272,
    `^Gate: R\d+ — ` stays 19, and `^Landed: R-` stays 1 — the R5 `Landed:`
    line is NOT removed, because this record is append-only and a superseded
    line stays where it is. The open set moves 251 to 250 and the maximum id
    stays `R-0711`. Across C3, C4 and C5 EVERY ONE OF THOSE COUNTS IS
    UNCHANGED.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. THE ONLY DESTRUCTIVE WORK IS G7's, AND IT IS ISOLATED. Both mutation
    red-proofs run ONLY inside a disposable `git worktree` created under
    `.remedy-wt/`, never in the primary checkout, which reads
    `git status --porcelain` 0 lines at every commit. Remove the worktree and
    prune before the handback.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE
    `59c8bcd0e589c1ed7b1e14941ad21e6238584b9e` was measured by the reviewer at
    that commit. It is a REFERENCE to report against, NOT a target to
    reproduce. Where your measurement differs, report BOTH and reconcile
    NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R6 is a whole-file
    replacement of `.agent/plan.md`; LEDGER6, DECISION6 and FEATURE6 are
    appends. The two retired comments of S5 are edits you make to source you
    have read, not slices.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 2
    of F032 and that R6 is the round. Session 1 was rounds R1 through R5 and
    ended at `59c8bcd0`. The soft limit is 25 rounds or 7 sessions, whichever
    comes first, and neither is near. The handback has NO LENGTH CAP —
    amend0827 rule 3 withdrew every tier — so do not declare, measure or
    apologise for its length.

Spec — T002a, the budget stop's triple.
 S1. READ FIRST. In `packages/orchestration/decision_queue.py` the budget
     branch is the one building `type="token_budget"`. At `59c8bcd0e589` it
     computes, before constructing the decision, `budget_error` (always
     non-empty at that point — the enclosing `if` tests it), and from the
     `job_stopped` event whose metadata `source` is `budget` it reads
     `_budget_request_id`, `_budget_created_at` and `_budget_limit`, the last
     from the metadata key `exhausted_limit`. Those three may each be the
     empty string; `budget_error` may not. The reviewer measured each of
     `type="token_budget",`, `next_actions=("extend", "abandon"),` and
     `safe_summary=f"Job stopped: {budget_error[:200]}",` as occurring EXACTLY
     ONCE in that file at that commit.
 S2. THE REFS ARE BUILT FROM WHAT THAT BRANCH ALREADY HAS, and every ref's
     target must be non-empty or the gate refuses it. Always emit a ref of
     kind `failure` targeting `budget_error`, labelled as the stop reason the
     budget guard recorded. Emit a SECOND ref of kind `failure` targeting the
     exhausted limit, labelled as the budget limit that was exhausted, ONLY
     when that value is non-empty. Emit a THIRD ref of kind `decision`
     targeting the request id, labelled as the request in flight when the
     budget was exhausted, ONLY when that value is non-empty. Never emit a ref
     whose target is the empty string.
 S3. THE OUTCOMES ARE KEYED PER CHOICE, one for `extend` and one for
     `abandon`. Each states what that choice does and what it costs, in this
     producer's own terms — the extend arm resumes the job from its last safe
     point with the limit raised and keeps the work already paid for, at the
     cost of spend continuing past the ceiling that was set and the same stop
     recurring if the run is not converging; the abandon arm stops the job
     with its artifacts as they are and nothing further spent, at the cost of
     the work in flight being left unfinished and a later resume paying again
     for the context this run had built. NAME THE EXHAUSTED LIMIT IN BOTH
     EXPECTED OUTCOMES when it is known, and fall back to a phrase that reads
     as English when it is not: the reviewer's dry run of the obvious
     interpolation produced `a raised the exhausted limit`, so build the
     limit phrase as a whole noun phrase rather than substituting a bare word.
     THE EXACT WORDING IS YOURS. It must not be, or contain as its whole
     value, any member of `BOILERPLATE_PHRASES`.
 S4. THE CARD STATES ITS OPTIONS WHERE THE GATE READS THEM, per DECISION F032
     D6 which C3 lands: the budget decision gains
     `payload={"options": ["extend", "abandon"]}`. `next_actions` IS NOT
     CHANGED — `tests/orchestration/test_f018_authority_integration.py` asserts
     it equals `("extend", "abandon")` at three places and those must stay
     green.
 S5. `token_budget` JOINS THE GATE SET IN THIS SAME COMMIT. In
     `packages/orchestration/decision_evidence.py`, `TRIPLE_REQUIRED_TYPES`
     becomes a frozenset holding exactly `token_budget`. TWO COMMENTS THEN
     STATE SOMETHING FALSE AND ARE RETIRED AT THEIR SOURCE, each naming what
     falsified it: `packages/orchestration/decision_queue.py` says of that set
     "which is EMPTY until T002 upgrades a producer", and the `#:` comment
     above the constant in `packages/orchestration/decision_evidence.py`
     explains its emptiness as a safety argument. Rewrite both to describe what
     the set now holds and the rule by which a type joins it. Retire nothing
     else.
 S6. THE TESTS GO IN `tests/orchestration/test_decision_evidence.py`, the file
     this feature created, and nowhere else. The existing
     `test_the_shipped_required_type_set_is_empty` asserts
     `TRIPLE_REQUIRED_TYPES == frozenset()` and is now FALSE; replace it with a
     test asserting the set's exact membership, keeping its docstring's point
     that a type joins only alongside its producer's triple. Then add tests
     driving the REAL budget branch through `list_decisions` from a
     `job_stopped` event with metadata `source` `budget`: one case where the
     reason, the exhausted limit and the request id are all present, and one
     where only the reason is. Assert the RENDERED values — the ref kinds and
     targets, and BOTH outcome options with their expected outcome and
     downside text — not merely that a triple exists. Assert that the exported
     card's `evidence_status` is `present` rather than the legacy literal.
     Assert that NO ref carries an empty target in either case. And assert
     that the enforced type really is enforced: a `token_budget` decision
     built WITHOUT a triple must raise `DecisionEvidenceError`.

Done when:
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report `git status --porcelain` line count
     after EACH of C0a through C6, each 0; report whether `.agent/STOP` exists
     at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r6.md`, of the committed `.agent/authored/f032-r6.md`
     blob and of the committed `.agent/last_block.md` blob, and report whether
     all three are EQUAL. Report the git blob hash of the C0a and C0b paths and
     whether they are the SAME blob. State plainly that this proves the scratch
     original, the saved copy and the mirror agree, and NOT the bytes of any
     prompt.
 G3. EXTRACTION AND CAPS. From the COMMITTED C0a blob, extract every region
     between a `^<<<SLICE ` line and its `^<<<END ` line. Report the NAME and
     the content-line count of each region you find, the number of regions, the
     CONTENT total, the block's TOTAL line count and PROSE as TOTAL minus
     CONTENT. Report whether PROSE is under 400 and TOTAL under 490. Report the
     number YOU measured; this block states none.
 G4. THE PLAN. Report whether `.agent/plan.md` at C1 is byte-equal to slice
     PLANF032R6 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`.
 G5. THE THREE APPENDS. For `.agent/live_review.md` at C2 and
     `.agent/decisions.md` at C3, prove EACH equals its pre-commit blob plus
     ONE newline plus its slice, byte for byte, and report the arithmetic as
     three numbers summing to the result; report that the pre-commit blob is a
     byte PREFIX of the result. The reviewer measured the bases at
     `59c8bcd0e589` as 1047137 and 639470 bytes. Then run a SECOND, INDEPENDENT
     structural reader over `.agent/live_review.md`: split the whole file on
     blank lines, let N be the number of paragraphs in the LEDGER6 slice as
     YOUR script counts them, and compare the LAST N units of the file against
     those N paragraphs IN ORDER. As a NEGATIVE CONTROL flip ONE byte inside
     the FIRST appended paragraph, in memory only, and report that BOTH readers
     REJECT it; never mutate the tracked file. For
     `docs/roadmap/features/T5_F032.md` at C3 report the same three-number
     append arithmetic; its base is 9364 bytes. Report the before and after
     counts of `^## DECISION F032 D\d+ ` and `^## DECISION `, the ADDED key,
     and that `^## Design amendments$` is still 1.
 G6. THE CODE, LINTED AND READ BACK BY BEHAVIOUR. After C4 run `python3 -m ruff
     check packages/orchestration/decision_queue.py
     packages/orchestration/decision_evidence.py` and report the REAL exit code
     and output VERBATIM; the reviewer measured `All checks passed!` at exit 0
     at the round base. Then, in a python heredoc, drive `list_decisions`
     TWICE with a `job_stopped` event whose metadata `source` is `budget`:
     once with a reason, an `exhausted_limit` and a `request_id`, once with the
     reason alone. For each, report VERBATIM the decision's id, its
     `next_actions`, its `payload`, every ref as a kind/target/label triple,
     and BOTH outcomes as option/expected_outcome/downside. Report the value of
     `TRIPLE_REQUIRED_TYPES`. Report the two comments S5 retires, quoting the
     replacement text of each.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. After C5 run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` and
     report the REAL exit code and summary VERBATIM. Then create ONE disposable
     worktree at the C5 commit under `.remedy-wt/`, run that same scoped
     command there UNMUTATED FIRST as the CONTROL and report its real exit code
     and summary. Then, in that worktree and one at a time, restoring between
     them: (a) remove `token_budget` from `TRIPLE_REQUIRED_TYPES`, leaving the
     set empty; (b) replace ONE outcome's downside text with the single
     character `-`, which `BOILERPLATE_PHRASES` holds. Report the REAL exit
     code and summary for each. BEFORE APPLYING EACH, report the count of the
     exact bytes you are about to change IN THE FILE YOU CHANGE THEM IN, at
     the commit the worktree sits at; if any count is not 1, widen the string
     until it is and report the string you used. REPORT THE COLOUR AND THE
     COUNT YOU OBSERVE — this block names no expected number of failures and no
     test name. IF EITHER MUTATION LEAVES THE RUN GREEN, say so plainly: that
     is a real finding about the tests. Remove the worktree and prune. Then, in
     the primary checkout, run as ONE pytest process the nine decision-schema
     guard files `tests/orchestration/test_decision_inbox.py`
     `tests/orchestration/test_approval_queue.py`
     `tests/orchestration/test_budget_stop_integration.py`
     `tests/orchestration/test_escalation.py`
     `tests/orchestration/test_bundled_clarification.py`
     `tests/cli/test_plan_approval.py` `tests/orchestration/test_handoff.py`
     `tests/cli/test_decision_answers.py`
     `tests/cli/test_open_decisions_view.py` with `-q`, and report the REAL
     exit code, the summary VERBATIM and the `^FAILED` count, proving your
     extractor sighted on a string containing such a line; the reviewer
     measured `324 passed` at a REAL exit 0 at the round base. Run
     `python3 -m pytest tests/orchestration/test_f018_authority_integration.py
     -q` and report the same three values.
 G8. STRUCTURE, THE CANARY, THE PR GATE AND THE PUSH. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the REAL
     exit code and summary VERBATIM; the reviewer measured `42 passed` at exit
     0 at the round base. Compare the path set of `git diff --name-only
     59c8bcd0..C5` BOTH WAYS against this round's expected set — the Change
     line's list MINUS `.agent/handoff.md` — and report both residues EMPTY.
     Report `git diff --stat 59c8bcd0..C5` restricted to `apps/` and confirm it
     EMPTY. Report each commit's insertions from `git diff --numstat` for C0a
     through C5, confirm each single-parent and under 500. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in each of `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`,
     `docs/roadmap/features/T5_F032.md`,
     `packages/orchestration/decision_queue.py`,
     `packages/orchestration/decision_evidence.py` and
     `tests/orchestration/test_decision_evidence.py`, against a CONTROL over
     the C0a blob which is not 0. `.agent/handoff.md` is DELIBERATELY NOT in
     that list and you do not measure it: it quotes this block's own gate text,
     so a zero-count over it is unmeetable by construction. Report `git
     ls-files .remedy-wt` 0 lines, `git worktree list` 1
     line, and `git branch --list "tmp/*"` 0 lines. Run `gh pr list --state
     open --json number,headRefName,baseRefName,isDraft` and report it
     VERBATIM; the reviewer read `[]` at the round base; MERGE NOTHING and
     CREATE NOTHING. After C6, run `git push origin
     feature/f032-evidence-triple`. ITS OUTCOME IS NOT A VALUE OF ANY FILE THIS
     ROUND WRITES, so `.agent/handoff.md` states the push only as an INTENT
     under `## External actions`, with NO exit code and NO remote tip; report
     the real exit code and the resulting remote tip in your completion report
     instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `59c8bcd0`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S6, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY which decision types
             are enforced by the gate after this round and which still carry the
             legacy placeholder.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R6
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D6.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R6 opens session 2 and starts T002. It books the R5 verdict and resolves
`R-0711`, then upgrades the FIRST producer: the budget stop carries refs into
the budget evidence it already computes, and one expected outcome and one
downside per choice, and `token_budget` becomes the first member of
`TRIPLE_REQUIRED_TYPES` in that same commit. DECISION F032 D6 rules where that
card's options list comes from, because the emit gate reads a decision's
options from `payload["options"]` and this branch carried none.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R5 verdict and the R-0711 resolution | ordered | the record moves first |
| C3 DECISION F032 D6 and its amendment | ordered | the ruling before the code |
| C4 the budget triple and the gate set | ordered | S1 through S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the patch-approval and repo-dirty producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then test-failure, memory-review and stop-reason, then the two branches
   that already carry an options list.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- The gate is live for one type from this round on, so a later change that
  regresses the budget triple raises instead of rendering. That is the intent.
- Seven producing types still carry the honest legacy placeholder, so the
  gate protects only `token_budget` until each is upgraded in turn.
<<<END PLANF032R6

<<<SLICE LEDGER6
Gate: F032 R5 — the F032 SESSION-CLOSING entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself at `59c8bcd0e589`. TRANSPORT HELD ACROSS THE CHAIN THIS WORKFLOW CAN ACTUALLY WALK: the reviewer's own scratch original `.remedy-wt/f032-r5.md`, the C0a blob and the C0b blob are ALL sha256 `370d580f6e28f5ffd9a74bab250e82eeb1df78e27f5495c93f4f159a67be075b` over 33067 bytes and 301 lines, with C0a and C0b the SAME git blob `47d4bbc2edcd`. THE SCRATCH ORIGINAL IS THE LOAD-BEARING LINK because the reviewer wrote it and the worker copied it, so this proof is not three readings of the worker's own output; it covers the scratch file, the saved copy and its mirror, and it does NOT claim the bytes of any prompt. THE PLAN at C1 is byte-equal to PLANF032R5 with the minus-newline control FALSE, `wc -l` 45, and `^## Goal$` and `^## Next Steps$` each 1. THE TWO APPENDS INTO THE RECORD EACH PROVE base plus ONE newline plus slice with the base a byte PREFIX: at C2 1032978 + 1 + 13775 = 1046754, and at C5 1046754 + 1 + 382 = 1047137, both reproduced by the reviewer from the committed blobs. THE SETS MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 54 to 57 adding exactly `F032 R2`, `F032 R3` and `F032 R4`, `^- R-\d+ — ` 271 to 272 adding exactly `R-0711`, `^Landed: R-` 0 to 1, while `^Done: R-\d+ — ` stayed 21 and `^Gate: R\d+ — ` stayed 19; ids DISTINCT at both points and the open set 250 to 251. THE FIX IS REAL AND THE MUTATION PROVES THE TESTS BITE: `packages/orchestration/decision_queue.py` at `510c949a` derives the memory-review summary from BOTH fields its predicate selects on and renames the local list to `memory_cards_to_review`, the reviewer read the three rendered summaries back as `Memory 'deploy-target' is stale.`, `Memory 'api-contract' is flagged for review.` and `Memory 'db-dsn' is stale and flagged for review.`, and reverting that summary to `f"Memory '{me.key}' is {me.validity}."` inside a disposable worktree turned the file RED at a REAL exit 1 with `2 failed, 25 passed`, naming `test_a_flagged_only_card_reads_as_flagged_and_never_as_active` and `test_a_stale_and_flagged_card_names_both_reasons`. THE SUITES ARE GREEN ON THE REVIEWER'S OWN RE-RUNS, SERIALLY: the scoped file `27 passed`, the nine decision-schema guard files `324 passed`, and the four state readers with the canary `620 passed`, each a REAL exit 0 with zero `^FAILED` lines, and `ruff check` over the changed module `All checks passed!` at exit 0. NOTHING ELSE MOVED: both path residues EMPTY over the six-path set, `apps/` and `docs/` each EMPTY, insertions 301, 197, 19, 8, 18, 43, 2 and 145 across the eight commits, each single-parent and under 500, markers 0 and 0 in all four written files against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, worktree 1 line, `tmp/*` 0, and the Open PR Gate read and NOT acted on at `[]`. THE ROUND'S SUBSTANCE IS THAT A FIX'S SECOND HALF WAS FOUND AND PAID FOR IN ONE ROUND: `R-0710` widened a selection predicate, and this round registered and fixed the string the newly admitted records rendered, which is the class the `R-0711` body names — a predicate widening must be read against every sentence the selected records then produce. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Done: R-0711 — RESOLVED. The memory-review card now derives its summary from BOTH fields the branch selects on, so a card flagged for review reads as flagged for review and never as active. The fix is `packages/orchestration/decision_queue.py` at `510c949a`, which computes the reason from `me.validity == "stale"` and `me.review_status == "needs_review"` independently and renames the local list to `memory_cards_to_review` so the name no longer claims the narrower set; the three cases are pinned on the RENDERED `safe_summary` at `9503c913`. THE REVIEWER VERIFIED THE FIX RATHER THAN THE REPORT: it read the three summaries back out of the real branch at `59c8bcd0e589`, and it reverted the summary expression inside a disposable worktree and measured a REAL exit 1 at `2 failed, 25 passed`, so the two tests covering the flagged-only and the both case genuinely kill the defect this finding describes. The `Landed:` line the R5 worker appended at `b672b5df` is correct and STAYS — this record is append-only and a superseded line is superseded by the paragraph beneath it, never removed. WHAT THIS FINDING LEAVES BEHIND, and it is the reason it was worth an id rather than a slip: a fix that widens a selection predicate is not finished when the predicate is right, because the code downstream of it was written under the narrower assumption and is correct only there. Every remaining T002 producer upgrade inherits that reading.
<<<END LEDGER6

<<<SLICE DECISION6
## DECISION F032 D6 (2026-08-27) — the budget stop states its options explicitly, so its outcomes can be keyed per choice

CONTEXT, measured at `59c8bcd0e589`. `docs/roadmap/features/T5_F032.md` Goal &
Done requires `expected_outcome` and `downside` PER OPTION, and its Design names
this producer's content by example: the budget stop's extend/abandon consequence
math, with the arithmetic as refs into the budget evidence. DECISION F032 D3
then narrowed the keying to "per option only where options exist", counting the
branches that carry an options list. The budget branch of
`packages/orchestration/decision_queue.py` is not one of them, and yet it does
offer the human two real choices: it sets `next_actions=("extend", "abandon")`
and carries no `payload` at all, while
`decision_evidence.enforce_decision_evidence` reads a decision's options from
`payload.get("options")` and from nowhere else. So the gate sees an OPTIONLESS
decision, and rule (h) of `evidence_triple_problems` would refuse the very
per-choice outcomes the feature file asks this producer for.

CHOSEN. The budget card states its options where the gate and the browser both
already look: `payload={"options": ["extend", "abandon"]}`, with one
`DecisionOptionOutcome` keyed to each. `next_actions` is NOT changed.

WHY THIS IS BEHAVIOUR-PRESERVING, MEASURED RATHER THAN ASSUMED.
`apps/ui/src/api/decisionCard.ts::decisionAnswers` resolves a card's answers in
the order options, then next actions, then free text, without branching on the
card's type. This card's `next_actions` are already exactly `extend` and
`abandon`, so serving those two from `payload.options` yields the same two
answers in the same order. The write door is untouched:
`decision_inbox._answerable_by_decision_resolve` branches on the decision's ID
PREFIX and on its escalation record, never on a payload, so the budget card
stays not-answerable-by-`decision.resolve` and `ANSWERABLE_DECISION_TYPES` in
`tests/orchestration/test_decision_inbox.py` remains correct for this type.

REJECTED, and why. One unkeyed outcome under `UNKEYED_OPTION`, which the gate
accepts for an optionless decision and which would have required no wire
change. It loses exactly the per-choice consequence math the feature file names
for this producer, and it would record as a design intention what is really an
omission: this card has two choices, and only its options LIST was missing.

REVERSE by deleting `payload` from the budget branch's `HumanDecision` and
collapsing its two outcomes into one keyed `UNKEYED_OPTION`; the gate accepts
that shape with no other change.
<<<END DECISION6

<<<SLICE FEATURE6
**A6 — the budget stop states its options explicitly (DECISION F032 D6).** A3
counts the branches carrying an options list and the budget stop is not among
them, yet it offers two real choices as `next_actions` while the emit gate reads
options only from `payload["options"]`. That branch therefore sets
`payload={"options": ["extend", "abandon"]}` and keys one expected outcome and
one downside to each. `next_actions` does not change, and
`apps/ui/src/api/decisionCard.ts::decisionAnswers` prefers `payload.options`
over `next_actions` without branching on type, so the browser renders the same
two answers as before. T002 upgrades the remaining producers the same way: a
type joins `TRIPLE_REQUIRED_TYPES` only in the commit that gives its producer a
real triple, which is what keeps the gate from raising on a card nobody has
upgraded yet.
<<<END FEATURE6
