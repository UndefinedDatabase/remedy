STEP R8 / F032 — T002c: THE PATCH APPROVAL, AND A SWEEP THAT WAS LEFT HALF DONE
Goal:        UPGRADE THE THIRD PRODUCER AND FINISH A SWEEP TWO ROUNDS OWED.
             The patch-approval card is the richest evidence in the queue and
             cites none of it: the intent it is about and the file it would
             change are both on the record it is derived from. This round gives
             that branch its refs and its one unkeyed outcome and adds
             `patch_approval` to `TRIPLE_REQUIRED_TYPES`. It also books the R7
             verdict, resolves `R-0712`, and retires the last two sentences R6
             falsified — R6's and R7's blocks each named the comments they knew
             about and each missed one, which is `R-0593`'s class exactly. YOU
             CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R7 verdict and `Done: R-0712` · C3 the
             patch-approval triple and the gate set · C4 the stale-count
             sweep · C5 its tests · C6 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r8.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `docs/roadmap/features/T5_F032.md`, `.agent/handoff.md`. This list
             bounds what you WRITE INTO THE REPOSITORY. It does NOT bound what
             you DO: G7 orders a disposable worktree and G8 orders a push.
             NOTHING under `apps/` is written. NO EXISTING TEST FILE other than
             the one this feature created is edited — in particular
             `tests/orchestration/test_decision_inbox.py` is NOT touched. If a
             guard elsewhere goes red, that is a real finding and you hand back
             rather than edit it.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r8.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r8.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    the points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations. Declaring beats fixing every time.
 3. THE PRODUCTION CODE AND THE SWEEP ARE SPECIFIED, NOT SLICED. Items S1
    through S6 describe what the code and the prose must SAY. You write them,
    in the house style of each file.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The record
    moves at C2, before any code.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R7. That is
    ordered: the plan becomes current at C1.
 6. `.agent/live_review.md` IS APPEND-ONLY AND IS WRITTEN ONCE THIS ROUND, AT
    C2, AS A PURE APPEND. Nothing already in it is rewritten, deleted,
    renumbered or touched. `.agent/decisions.md` IS NOT WRITTEN AT ALL this
    round, and its own count of branches with an options list is a MEASUREMENT
    DATED TO THE R1 INVENTORY — it is correct as history and the sweep in S5
    deliberately does not reach it.
 7. YOU AUTHOR NO RECORD TEXT OF YOUR OWN THIS ROUND. You mint no finding id,
    write no `Gate:` paragraph, no `Done:` paragraph and no `Landed:` line. The
    only text entering `.agent/live_review.md` is the LEDGER8 slice, which the
    reviewer wrote. If this round's work makes you believe a NEW finding
    exists, DO NOT register it — describe it in the handback under Deviations
    and let the reviewer mint it.
 8. THE LEDGER SETS MOVE AS FOLLOWS. Across C2: `^Gate: F\d+ R\d+ — ` moves 59
    to 60 with the ADDED key exactly `F032 R7`; `^Done: R-\d+ — ` moves 22 to
    23 with the ADDED id exactly `R-0712`; `^- R-\d+ — ` stays 273,
    `^Landed: R-` stays 1 and `^Gate: R\d+ — ` stays 19. The open set moves 251
    to 250 and the maximum id stays `R-0712`. Across C3, C4 and C5 EVERY ONE OF
    THOSE COUNTS IS UNCHANGED.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. THE ONLY DESTRUCTIVE WORK IS G7's, AND IT IS ISOLATED. Both mutation
    red-proofs run ONLY inside a disposable `git worktree` created under
    `.remedy-wt/`, never in the primary checkout, which reads
    `git status --porcelain` 0 lines at every commit. DELETE EVERY
    `__pycache__` IN THAT WORKTREE BEFORE EACH RUN and pass `-B` to python:
    R7 measured a mutation whose restored file had the same size and mtime
    second as the mutated one, and a stale cached module reported a colour that
    was one test wrong. Remove the worktree and prune before the handback.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE
    `6286f76194c10f4b8da10f62c84f8e00efb364f6` was measured by the reviewer at
    that commit. It is a REFERENCE to report against, NOT a target to
    reproduce. Where your measurement differs, report BOTH and reconcile
    NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R8 is a whole-file
    replacement of `.agent/plan.md`; LEDGER8 is an append. The sweep of S5 is
    an edit you make to prose you have read, not a slice.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 2
    of F032 and that R8 is the round. Session 1 was rounds R1 through R5; this
    session began at R6. The soft limit is 25 rounds or 7 sessions, whichever
    comes first, and neither is near. The handback has NO LENGTH CAP —
    amend0827 rule 3 withdrew every tier — so do not declare, measure or
    apologise for its length.

Spec — T002c, the patch-approval card, and the sweep.
 S1. READ FIRST. In `packages/orchestration/decision_queue.py` the
     patch-approval branch iterates `list_patch_intents(job)` and builds a
     decision for each intent whose `state` is `APPROVAL_PENDING`. The reviewer
     ran that function at `6286f76194c1` against the fixture the inbox guard
     uses and measured the record it yields: `intent_id` `'2ad56338-0'` — the
     artifact's short id and the explanation's index, so it is ALWAYS non-empty
     and the branch already indexes it unguarded — `target_path` `'README.md'`,
     plus `action`, `risk`, `reason`, `summary`, `artifact_id`, `task_id` and
     `state`. The branch today cites NONE of it. `type="patch_approval",`
     occurs EXACTLY ONCE in that file at that commit.
 S2. THE REFS COME FROM THE INTENT RECORD. Always emit a ref of kind `decision`
     targeting `pi["intent_id"]`, labelled as the patch intent awaiting
     approval. Emit a SECOND ref of kind `file` targeting the intent's
     `target_path`, labelled as the file this patch would change, ONLY when that
     value is non-empty — `related_file` on the same card already defaults it to
     the empty string, and rule (c) of `evidence_triple_problems` refuses a ref
     that points at nothing. Never emit a ref whose target is the empty string.
 S3. THE OUTCOME IS UNKEYED, AND THAT IS A RULING THIS BLOCK IS APPLYING RATHER
     THAN INVENTING. This branch carries no `payload`, and its `next_actions`
     are two full `remedy patch` command lines rather than two option words, so
     giving it an options list would CHANGE WHAT THE BROWSER RENDERS AS ANSWERS
     — `apps/ui/src/api/decisionCard.ts::decisionAnswers` prefers
     `payload.options` over `next_actions` — and amendment A3 of
     `docs/roadmap/features/T5_F032.md` puts growing an options list for these
     branches OUT of F032's scope. DECISION F032 D6 moved the budget stop's
     options only because its `next_actions` were ALREADY the two option words,
     so nothing new was grown there. Therefore: exactly ONE outcome, keyed
     `UNKEYED_OPTION`, and DO NOT add a `payload` to this branch. The outcome
     states what settling this decision does and what the judgement costs — that
     the named file's pending change is settled either way, approving applying
     it and unblocking the task that produced it while rejecting leaves the
     working tree untouched, at the cost that the judgement is made from the
     intent's summary and target path rather than from the applied diff, so a
     patch wrong in a way the summary does not reveal is approved as easily as a
     correct one. THE EXACT WORDING IS YOURS. It must not be, or contain as its
     whole value, any member of `BOILERPLATE_PHRASES`.
 S4. `patch_approval` JOINS THE GATE SET IN THE SAME COMMIT AS ITS TRIPLE. In
     `packages/orchestration/decision_evidence.py`, `TRIPLE_REQUIRED_TYPES`
     becomes a frozenset holding exactly `token_budget`, `test_failure` and
     `patch_approval`.
 S5. THE SWEEP, AT C4, AND IT IS DEFINED BY A PROPERTY RATHER THAN BY A LIST OF
     SITES — which is the whole lesson of the two rounds that each named sites
     and each missed one. FIND every sentence in
     `packages/orchestration/`, `tests/orchestration/test_decision_evidence.py`
     and `docs/roadmap/features/T5_F032.md` that states HOW MANY producing
     branches do or do not carry an options list, by searching for the phrases
     that express it rather than for a number. REPORT WHAT YOU FIND, then
     correct each to the count you MEASURE. Two are known to the reviewer at
     `6286f76194c1` and there may be more, which is why you search rather than
     trust this list: the docstring of
     `test_an_enforced_optionless_decision_reads_no_options_from_the_payload`
     calls it "the six-branch case", and amendment A3 of the feature file says
     "Only two of the eight producing branches carry an options list". A3 IS
     CORRECTED BY APPENDING, NOT BY REWRITING ITS MEASUREMENT: leave its
     sentence standing and add one sentence naming A6 as what moved the count
     and stating the current number, because A3 recorded a true reading and the
     amendments section is a record of how the design moved. `.agent/` is NOT
     in the search scope: constraint 6 says why.
 S6. THE TESTS GO IN `tests/orchestration/test_decision_evidence.py`, the file
     this feature created, and nowhere else. Update the exact-membership
     assertion so it names all three enforced types. Then add tests driving the
     REAL branch through `list_decisions` from a job carrying a pending patch
     intent, built the way `list_patch_intents` requires — an `Artifact` whose
     metadata holds `patch_intent_explanations`. Cover the case where the intent
     names a target path and the case where it does NOT, and assert the RENDERED
     ref kinds, targets and labels in both, the single unkeyed outcome's text,
     and that NO ref carries an empty target in either. Assert the exported
     card's `evidence_status` is `present`. Assert that a `patch_approval`
     decision built WITHOUT a triple raises `DecisionEvidenceError`. PIN THE
     CONDITIONAL: a test must fail if the file ref is emitted unconditionally,
     and its name should say so.

Done when:
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report `git status --porcelain` line count
     after EACH of C0a through C6, each 0; report whether `.agent/STOP` exists
     at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r8.md`, of the committed `.agent/authored/f032-r8.md`
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
     PLANF032R8 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`.
 G5. THE LEDGER APPEND. Prove `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus the LEDGER8 slice, byte for byte,
     and report the arithmetic as three numbers summing to the result; report
     that the pre-commit blob is a byte PREFIX of the result. The reviewer
     measured the base at `6286f76194c1` as 1059172 bytes over 421 blank-line
     units. Then run a SECOND, INDEPENDENT structural reader: split the whole
     file on blank lines, let N be the number of paragraphs in the LEDGER8
     slice as YOUR script counts them, and compare the LAST N units of the file
     against those N paragraphs IN ORDER. As a NEGATIVE CONTROL flip ONE byte
     inside the FIRST appended paragraph, in memory only, and report that BOTH
     readers REJECT it; never mutate the tracked file. Report every count
     constraint 8 names, before and after C2, INCLUDING the non-movers, and the
     ids and gate keys ADDED as SETS.
 G6. THE CODE AND THE SWEEP, LINTED AND READ BACK. After C4 run `python3 -m
     ruff check packages/orchestration/decision_queue.py
     packages/orchestration/decision_evidence.py` and report the REAL exit code
     and output VERBATIM; the reviewer measured `All checks passed!` at exit 0
     at the round base. Then, in a python heredoc, drive `list_decisions` TWICE
     over a job carrying a pending patch intent: once where the intent names a
     target path, once where it does not. For each, report VERBATIM the
     decision's id, its `safe_summary`, its `payload`, every ref as a
     kind/target/label triple, and the outcome as
     option/expected_outcome/downside. Report the value of
     `TRIPLE_REQUIRED_TYPES`. FOR THE SWEEP, report the search you ran for S5,
     EVERY sentence it returned across all three scopes, and the replacement
     text of each one you changed — including any the reviewer did not name.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. After C5 run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` and
     report the REAL exit code and summary VERBATIM. Then create ONE disposable
     worktree at the C5 commit under `.remedy-wt/`, run that same scoped
     command there UNMUTATED FIRST as the CONTROL and report its real exit code
     and summary. Then, in that worktree and one at a time, restoring between
     them and honouring constraint 10's cache rule: (a) remove `patch_approval`
     from `TRIPLE_REQUIRED_TYPES`, leaving the other two; (b) make the
     `target_path` ref of S2 unconditional, so an intent with no target path
     emits a ref with an empty target. Report the REAL exit code and summary
     for each, AND re-run the CONTROL after the last restoration to show the
     file really came back. BEFORE APPLYING EACH, report the count of the exact
     bytes you are about to change IN THE FILE YOU CHANGE THEM IN, at the commit
     the worktree sits at; if any count is not 1, widen the string until it is
     and report the string you used. REPORT THE COLOUR AND THE COUNT YOU
     OBSERVE — this block names no expected number of failures and no test name.
     IF EITHER MUTATION LEAVES THE RUN GREEN, say so plainly: that is a real
     finding about the tests. Remove the worktree and prune. Then, in the
     primary checkout, run as ONE pytest process the nine decision-schema guard
     files `tests/orchestration/test_decision_inbox.py`
     `tests/orchestration/test_approval_queue.py`
     `tests/orchestration/test_budget_stop_integration.py`
     `tests/orchestration/test_escalation.py`
     `tests/orchestration/test_bundled_clarification.py`
     `tests/cli/test_plan_approval.py` `tests/orchestration/test_handoff.py`
     `tests/cli/test_decision_answers.py`
     `tests/cli/test_open_decisions_view.py` with `-q`, and report the REAL
     exit code, the summary VERBATIM and the `^FAILED` count, proving your
     extractor sighted on a string containing such a line; the reviewer
     measured `324 passed` at a REAL exit 0 at the round base. THIS IS THE GATE
     THE ROUND TURNS ON: `patch_approval` becomes enforced at C3 and
     `_fixture_patch_approval` in the inbox guard drives that branch, so a
     triple the branch fails to build shows up here as a raise rather than as a
     card.
 G8. STRUCTURE, THE CANARY, THE PR GATE AND THE PUSH. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the REAL
     exit code and summary VERBATIM; the reviewer measured `42 passed` at exit
     0 at the round base. Also run `python3 -m pytest tests/docs/ -q` and report
     the same, because C4 edits a file under `docs/roadmap/`. Compare the path
     set of `git diff --name-only 6286f761..C5` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md` — and
     report both residues EMPTY. Report `git diff --stat 6286f761..C5`
     restricted to `apps/` and confirm it EMPTY. Report each commit's insertions
     from `git diff --numstat` for C0a through C5, confirm each single-parent
     and under 500. Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in
     each of `.agent/plan.md`, `.agent/live_review.md`,
     `packages/orchestration/decision_queue.py`,
     `packages/orchestration/decision_evidence.py`,
     `tests/orchestration/test_decision_evidence.py` and
     `docs/roadmap/features/T5_F032.md`, against a CONTROL over the C0a blob
     which is not 0. `.agent/handoff.md` is DELIBERATELY NOT in that list and
     you do not measure it: it quotes this block's own gate text, so a
     zero-count over it is unmeetable by construction. Report `git ls-files
     .remedy-wt` 0 lines, `git worktree list` 1 line, and `git branch --list
     "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C6, run `git push origin feature/f032-evidence-triple`. ITS OUTCOME
     IS NOT A VALUE OF ANY FILE THIS ROUND WRITES, so `.agent/handoff.md`
     states the push only as an INTENT under `## External actions`, with NO
     exit code and NO remote tip; report the real exit code and the resulting
     remote tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `6286f761`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S6, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY which decision types
             the gate enforces after this round and which still carry the legacy
             placeholder, and list every sentence the S5 sweep changed.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R8
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
R8 upgrades the patch-approval producer, the richest evidence in the queue and
until now the least cited: the intent it is about and the file it would change
are both on the record the branch already reads. It takes the optionless shape,
because its `next_actions` are command lines rather than option words and
amendment A3 puts growing an options list out of scope. The round also books
the R7 verdict, resolves `R-0712`, and finishes the stale-count sweep that R6
and R7 each left one sentence short.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R7 verdict and Done: R-0712 | ordered | the record moves first |
| C3 the patch-approval triple and the gate set | ordered | S1 to S4 |
| C4 the stale-count sweep | ordered | S5, defined by property |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the memory-review and stop-reason producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then repo-dirty, whose event carries the thinnest evidence of the eight and
   needs its refs thought through, and the two branches that already carry an
   options list — the flight plan's resolved arm owes a ruling.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Three types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
- The flight-plan branch has two arms and only one carries options; enforcing
  that type will need a ruling on what a RESOLVED decision owes.
<<<END PLANF032R8

<<<SLICE LEDGER8
Gate: F032 R7 — the F032 T002b TEST-FAILURE entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself at `6286f76194c1`. TRANSPORT IS PROVED END TO END AGAIN: the reviewer computed sha256 `8c021ead99bd006bae021a8eec2e830973f528655ca084282910eea8ec17256a` over 29519 bytes and 335 lines BEFORE delegating, and the committed `.agent/authored/f032-r7.md` blob carries exactly that digest, with C0a and C0b the SAME git blob `bd2de27477e1`; the chain runs from a value the reviewer held independently through the saved copy to its mirror, and claims nothing about the bytes of any prompt. EXTRACTION printed 2 regions at 44 and 3 content lines, CONTENT 47, TOTAL 335, PROSE 288. THE PLAN at C1 is byte-equal to PLANF032R7 with the minus-newline control FALSE and `wc -l` 44. THE LEDGER APPEND is 1051985 + 1 + 7186 = 1059172 with the base a byte PREFIX, the second reader counted N 2 and found the last two units EQUAL IN ORDER to the slice's paragraphs, and a byte flipped inside the FIRST appended paragraph was REJECTED by both readers. THE SETS MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 58 to 59 adding exactly `F032 R6`, `^- R-\d+ — ` 272 to 273 adding exactly `R-0712`, while `^Done: R-\d+ — ` stayed 22, `^Landed: R-` stayed 1 and `^Gate: R\d+ — ` stayed 19; ids DISTINCT, open set 250 to 251, maximum `R-0711` to `R-0712`. THE FIX IS THE ROUND'S POINT AND IT IS A READ, NOT A RENAME: `cmd = str(meta.get("command_safe") or meta.get("command") or "?")`, with the older key kept because the inbox guard's own fixture writes it and that file is outside the round's change set. The reviewer drove the real branch and read back `Test 'pytest tests/orchestration -q' failed.` for the producer's key, `Test 'pytest -q' failed.` for the older one, and the honest `Test '?' failed.` for neither, with the command ref OMITTED in the third rather than pointing at a question mark. THE MUTATIONS BOTH KILLED TESTS AND THE REVIEWER REPRODUCED BOTH IN ITS OWN WORKTREE: control a REAL exit 0 at `46 passed`, restoring the `R-0712` defect exit 1 at `1 failed, 45 passed` naming `test_the_test_failure_card_reads_command_safe_first_never_command`, and dropping the type from the gate set exit 1 at `2 failed, 44 passed`; a second control after both restorations is again `46 passed`. THE WORKER CAUGHT A MEASUREMENT ERROR THAT WAS NOT ITS OWN CODE'S, AND SAID SO: its first reading of mutation (b) was `3 failed, 43 passed`, because mutation (a) swaps two dict keys of EQUAL TOTAL LENGTH, so the restored file matched the mutated one in size and mtime second and CPython served a stale `__pycache__`. It diagnosed that, purged the caches, disabled byte-code writing, re-measured, and REPORTED BOTH READINGS rather than only the clean one. The reviewer reproduced the clean readings with `-B` and per-run cache purging, and R8's block carries that as a standing constraint. THE GUARDS DID NOT MOVE: the nine decision-schema guard files `324 passed` and the golden-path canary `42 passed`, each a REAL exit 0 with zero `^FAILED` lines, and `ruff check` `All checks passed!` at exit 0. THE SWEEP ORDERED BY S5 WAS PERFORMED AND THE REVIEWER COUNTED IT INDEPENDENTLY: an AST walk of `list_decisions` finds `options` set at three branches — the budget stop, the flight plan's pending arm and the task decision — so five of the eight carry none, both corrected comments now read `five of the`, and `six of the` no longer occurs in that module. NOTHING ELSE MOVED: both path residues EMPTY over the seven-path set, `apps/` and `docs/` EMPTY, insertions 335, 183, 16, 4, 10, 44, 161 and 142 across the eight commits, each single-parent and under 500, markers 0 and 0 in all five written files against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, worktree 1 line, `tmp/*` 0, the Open PR Gate `[]`, and the remote tip equal to the local tip. THE ROUND ALSO SHOWS THE SWEEP-BY-LIST FAILING TWICE IN A ROW: R6's S5 named two falsified comments and missed two, R7's S5 named those two and missed a third, which the worker found and correctly declined to fix because the block said retire nothing else. That is `R-0593`'s class and no new id is spent on it, per §3 checklist item 30; R8's S5 is written as a PROPERTY to search for instead of a list of sites, which is the actual counter-measure. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Done: R-0712 — RESOLVED. The test-failure card now reads the key its emitter actually writes, so a blocker asking a human to look at a failing test names the command that failed. The fix is `packages/orchestration/decision_queue.py` at `a25823da`, which resolves the command as `meta.get("command_safe") or meta.get("command") or "?"` and cites it as a `failure` ref only when it resolved to something, and the three cases are pinned on the RENDERED `safe_summary` at `389429bb`. THE REVIEWER VERIFIED THE FIX RATHER THAN THE REPORT: it drove the real branch at `6286f76194c1` with an event built exactly as `test_execution_service._safe_event_meta` builds one and read back the command; and inside a disposable worktree it restored the defect by preferring `command` again and measured a REAL exit 1 at `1 failed, 45 passed`, the failing test being the one whose name states the property, so the pin is discriminating rather than incidental. THE FALLBACK IS DELIBERATE AND IS DOCUMENTED AT THE SITE: `_fixture_test_failure` in `tests/orchestration/test_decision_inbox.py` writes the older key, that file was outside the round's change set, and dropping the fallback would have left the inbox guard's own card showing the placeholder — so the fix reaches production without reaching into a file it was not licensed to edit. WHAT THIS FINDING LEAVES BEHIND is the fixture lesson rather than the key: a test fixture written from the READER's side cannot fail on a reader that disagrees with every writer, and this one had mirrored the bug since the branch was written. The remaining producer upgrades each read event metadata the same way, so each is now checked against its EMITTER rather than against the fixture that happens to feed it.
<<<END LEDGER8
