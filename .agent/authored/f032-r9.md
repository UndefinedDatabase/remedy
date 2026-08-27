STEP R9 / F032 — T002d: THE STOP REASON, AND THE SESSION'S CLOSE
Goal:        UPGRADE THE FOURTH PRODUCER, FIX WHAT R8 EXPOSED, AND CLOSE THE
             SESSION. The stop-reason branch copies a structured record into a
             card and drops every identifier on it: the stop's own id, its
             reason code and the file it is about are all right there. This
             round gives that branch its refs and its one unkeyed outcome and
             adds `stop_reason` to `TRIPLE_REQUIRED_TYPES`. It also books the
             R8 verdict and registers and fixes `R-0713`: the patch-approval
             summary was written with a `'?'` default that can never fire,
             because the key is present and empty rather than absent, so a
             patch intent naming no file renders `Patch intent for  awaits
             approval.` SESSION 2 ENDS WITH THIS ROUND. YOU CREATE NO PULL
             REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R8 verdict and `R-0713` · C3 the `R-0713` fix · C4
             the stop-reason triple and the gate set · C5 its tests · C6 the
             session-closing handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r9.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G7 orders a disposable
             worktree and G8 orders a push. NOTHING under `apps/` or `docs/` is
             written. NO EXISTING TEST FILE other than the one this feature
             created is edited — in particular
             `tests/orchestration/test_decision_inbox.py` is NOT touched. If a
             guard elsewhere goes red, that is a real finding and you hand back
             rather than edit it.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r9.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r9.md` — with `shutil.copyfile` or a read-then-write
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
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. `R-0713` is
    REGISTERED at C2 and FIXED at C3, in that order and never the reverse —
    findings persist first so nothing is lost if the session dies mid-repair.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R8. That is
    ordered: the plan becomes current at C1.
 6. `.agent/live_review.md` IS APPEND-ONLY AND IS WRITTEN ONCE THIS ROUND, AT
    C2, AS A PURE APPEND. Nothing already in it is rewritten, deleted,
    renumbered or touched. An append-only record is corrected by appending.
 7. YOU AUTHOR NO RECORD TEXT OF YOUR OWN THIS ROUND. You mint no finding id,
    write no `Gate:` paragraph, no `Done:` paragraph and no `Landed:` line. The
    only text entering `.agent/live_review.md` is the LEDGER9 slice, which the
    reviewer wrote. If this round's work makes you believe a NEW finding
    exists, DO NOT register it — describe it in the handback under Deviations
    and let the reviewer mint it.
 8. THE LEDGER SETS MOVE AS FOLLOWS. Across C2: `^Gate: F\d+ R\d+ — ` moves 60
    to 61 with the ADDED key exactly `F032 R8`; `^- R-\d+ — ` moves 273 to 274
    with the ADDED id exactly `R-0713`; `^Done: R-\d+ — ` stays 23,
    `^Landed: R-` stays 1 and `^Gate: R\d+ — ` stays 19. The open set moves 250
    to 251 and the maximum id `R-0712` to `R-0713`. Across C3, C4 and C5 EVERY
    ONE OF THOSE COUNTS IS UNCHANGED.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. THE ONLY DESTRUCTIVE WORK IS G7's, AND IT IS ISOLATED. Both mutation
    red-proofs run ONLY inside a disposable `git worktree` created under
    `.remedy-wt/`, never in the primary checkout, which reads
    `git status --porcelain` 0 lines at every commit. DELETE EVERY
    `__pycache__` IN THAT WORKTREE BEFORE EACH RUN and pass `-B` to python:
    R7 measured a mutation whose restored file matched the mutated one in size
    and mtime second, and a stale cached module reported a colour one test
    wrong. Remove the worktree and prune before the handback.
11. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE
    `c23e7cc633fb2adf8b6dce5b1c576a8440055e52` was measured by the reviewer at
    that commit. It is a REFERENCE to report against, NOT a target to
    reproduce. Where your measurement differs, report BOTH and reconcile
    NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R9 is a whole-file
    replacement of `.agent/plan.md`; LEDGER9 is an append.
14. YOUR HANDBACK IS THE SESSION-CLOSING ONE AND IS THE ONLY RETURN CHANNEL
    THIS SESSION HAS. Its `## Session` section states that this is SESSION 2 of
    F032, that R9 is the round, and that SESSION 2 ENDS HERE with four
    delegated rounds, R6 through R9. Session 1 was R1 through R5. Nine rounds
    and two sessions are inside the soft limit of 25 rounds or 7 sessions, so
    do NOT emit a limit report. The handback has NO LENGTH CAP — amend0827 rule
    3 withdrew every tier — so do not declare, measure or apologise for its
    length. Its `## Next` section is the most load-bearing text you write this
    round: name Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the
    `.agent/STOP` re-read from disk — before anything else, then the Open PR
    Gate, then the remaining T002 producers.

Spec — T002d, the stop-reason card, and the `R-0713` fix.
 S1. READ FIRST. In `packages/orchestration/decision_queue.py` the stop-reason
     branch iterates `derive_stop_reasons(job, events)` and builds a decision
     for each record whose `status` is `active`, copying `severity`, `source`,
     `related_node_id`, `related_intent_id`, `related_file`, `safe_summary`,
     `next_actions` and `created_at` straight across. The reviewer ran that
     function at `c23e7cc633fb` against a job with no target repo and measured
     the record it yields: `id` `'derived_no_repo'`, `reason_code`
     `'no_target_repo'`, `source` `'readiness'`, `related_file` `''`,
     `severity` `'blocker'`. `StopReason` also carries `job_id`, `status` and
     `resolved_at`. `type="stop_reason",` occurs EXACTLY ONCE in that file at
     that commit.
 S2. THE FIX FOR `R-0713`, AND IT IS ONE LINE. The patch-approval summary reads
     `pi.get('target_path', '?')`, and a default only fires when the KEY IS
     ABSENT; `list_patch_intents` always sets `target_path`, to the empty string
     when the explanation named no file. The reviewer demonstrated this at
     `c23e7cc633fb`: an intent with no `file` key yields `target_path` `''` and
     the card renders `Patch intent for  awaits approval.` — two spaces and no
     subject. R8 already computed `_pa_target_path` for the ref guard directly
     above; use that value, falling back to `'?'` when it is empty, so the
     placeholder the line was always written to show finally shows. Do not
     change the sentence otherwise.
 S3. THE REFS COME FROM THE STOP RECORD. Always emit a ref of kind `failure`
     targeting the record's `id` — the value the decision id is already built
     from — labelled as the stop record that raised this decision. Emit a
     SECOND ref of kind `failure` targeting `reason_code`, labelled as the
     reason code the run recorded, ONLY when that value is non-empty. Emit a
     THIRD ref of kind `file` targeting `related_file`, labelled as the file
     this stop is about, ONLY when that value is non-empty — the record the
     reviewer measured has it EMPTY, so this guard is load-bearing rather than
     defensive. Never emit a ref whose target is the empty string.
 S4. THE OUTCOME IS UNKEYED. This branch carries no `payload` and copies the
     record's own `next_actions`, which are command lines rather than option
     words, so DECISION F032 D3's optionless case applies and rule (h) requires
     EXACTLY ONE outcome keyed `UNKEYED_OPTION`. Amendment A3 puts growing an
     options list here out of F032's scope, exactly as it did for the patch
     approval at R8, so DO NOT add a `payload` to this branch. The outcome
     states what clearing the named blocker buys and what it costs — the run
     continues from where it stopped with the work already done still in place,
     at the cost that until it is cleared the run makes no further progress, and
     that a blocker cleared without understanding why it fired can fire again.
     THE EXACT WORDING IS YOURS. It must not be, or contain as its whole value,
     any member of `BOILERPLATE_PHRASES`.
 S5. `stop_reason` JOINS THE GATE SET IN THE SAME COMMIT AS ITS TRIPLE. In
     `packages/orchestration/decision_evidence.py`, `TRIPLE_REQUIRED_TYPES`
     becomes a frozenset holding exactly `token_budget`, `test_failure`,
     `patch_approval` and `stop_reason`.
 S6. THE TESTS GO IN `tests/orchestration/test_decision_evidence.py`, the file
     this feature created, and nowhere else. Update the exact-membership
     assertion so it names all four enforced types. For `R-0713`, assert the
     RENDERED `safe_summary` of a patch-approval card whose intent names NO
     file, and assert the case that already worked still does — a test must fail
     if the fix is reverted to `pi.get('target_path', '?')`, and its name should
     say so. For the stop reason, add tests driving the REAL branch through
     `list_decisions`: the no-target-repo case the reviewer measured, which has
     an EMPTY `related_file`, and a case carrying a related file. Assert the
     rendered ref kinds, targets and labels in both, the single unkeyed
     outcome's text, and that no ref carries an empty target in either. Assert
     the exported card's `evidence_status` is `present`. Assert that a
     `stop_reason` decision built WITHOUT a triple raises
     `DecisionEvidenceError`. PIN THE CONDITIONAL: a test must fail if the
     `related_file` ref is emitted unconditionally.

Done when:
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report `git status --porcelain` line count
     after EACH of C0a through C6, each 0; report whether `.agent/STOP` exists
     at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r9.md`, of the committed `.agent/authored/f032-r9.md`
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
     PLANF032R9 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`.
 G5. THE LEDGER APPEND. Prove `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus the LEDGER9 slice, byte for byte,
     and report the arithmetic as three numbers summing to the result; report
     that the pre-commit blob is a byte PREFIX of the result. The reviewer
     measured the base at `c23e7cc633fb` as 1065424 bytes over 423 blank-line
     units. Then run a SECOND, INDEPENDENT structural reader: split the whole
     file on blank lines, let N be the number of paragraphs in the LEDGER9
     slice as YOUR script counts them, and compare the LAST N units of the file
     against those N paragraphs IN ORDER. As a NEGATIVE CONTROL flip ONE byte
     inside the FIRST appended paragraph, in memory only, and report that BOTH
     readers REJECT it; never mutate the tracked file. Report every count
     constraint 8 names, before and after C2, INCLUDING the non-movers, and the
     ids and gate keys ADDED as SETS.
 G6. THE CODE, LINTED AND READ BACK BY BEHAVIOUR. After C4 run `python3 -m ruff
     check packages/orchestration/decision_queue.py
     packages/orchestration/decision_evidence.py` and report the REAL exit code
     and output VERBATIM; the reviewer measured `All checks passed!` at exit 0
     at the round base. Then, in a python heredoc: drive `list_decisions` over a
     patch intent that names NO file and report its `safe_summary` VERBATIM,
     and over one that names a file and report the same, so the `R-0713` fix is
     read back on both shapes. Then drive `list_decisions` over a job whose
     stop reason has an EMPTY `related_file` and over one that has a related
     file, and for each report VERBATIM the decision's id, its `payload`, every
     ref as a kind/target/label triple, and the outcome as
     option/expected_outcome/downside. Report the value of
     `TRIPLE_REQUIRED_TYPES`.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. After C5 run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` and
     report the REAL exit code and summary VERBATIM. Then create ONE disposable
     worktree at the C5 commit under `.remedy-wt/`, run that same scoped
     command there UNMUTATED FIRST as the CONTROL and report its real exit code
     and summary. Then, in that worktree and one at a time, restoring between
     them and honouring constraint 10's cache rule: (a) revert the `R-0713` fix
     to the `pi.get('target_path', '?')` form; (b) make the `related_file` ref
     of S3 unconditional, so a stop record with none emits a ref with an empty
     target. Report the REAL exit code and summary for each, AND re-run the
     CONTROL after the last restoration to show the files really came back.
     BEFORE APPLYING EACH, report the count of the exact bytes you are about to
     change IN THE FILE YOU CHANGE THEM IN, at the commit the worktree sits at;
     if any count is not 1, widen the string until it is and report the string
     you used. REPORT THE COLOUR AND THE COUNT YOU OBSERVE — this block names no
     expected number of failures and no test name. IF EITHER MUTATION LEAVES THE
     RUN GREEN, say so plainly: that is a real finding about the tests. Remove
     the worktree and prune. Then, in the primary checkout, run as ONE pytest
     process the nine decision-schema guard files
     `tests/orchestration/test_decision_inbox.py`
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
     THE ROUND TURNS ON: `stop_reason` becomes enforced at C4 and
     `_fixture_stop_reason` in the inbox guard drives that branch with a record
     whose `related_file` is EMPTY, so a triple the branch builds wrongly shows
     up here as a raise rather than as a card.
 G8. STRUCTURE, THE CANARY, THE PR GATE AND THE PUSH. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the REAL
     exit code and summary VERBATIM; the reviewer measured `42 passed` at exit
     0 at the round base. Compare the path set of `git diff --name-only
     c23e7cc6..C5` BOTH WAYS against this round's expected set — the Change
     line's list MINUS `.agent/handoff.md` — and report both residues EMPTY.
     Report `git diff --stat c23e7cc6..C5` restricted to `apps/` and to `docs/`
     and confirm each EMPTY. Report each commit's insertions from `git diff
     --numstat` for C0a through C5, confirm each single-parent and under 500.
     Line-anchored `^<<<SLICE ` and `^<<<END ` are 0 and 0 in each of
     `.agent/plan.md`, `.agent/live_review.md`,
     `packages/orchestration/decision_queue.py`,
     `packages/orchestration/decision_evidence.py` and
     `tests/orchestration/test_decision_evidence.py`, against a CONTROL over
     the C0a blob which is not 0. `.agent/handoff.md` is DELIBERATELY NOT in
     that list and you do not measure it: it quotes this block's own gate text,
     so a zero-count over it is unmeetable by construction. Report `git
     ls-files .remedy-wt` 0 lines, `git worktree list` 1 line, and `git branch
     --list "tmp/*"` 0 lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C6, run `git push origin feature/f032-evidence-triple`. ITS OUTCOME
     IS NOT A VALUE OF ANY FILE THIS ROUND WRITES, so `.agent/handoff.md`
     states the push only as an INTENT under `## External actions`, with NO
     exit code and NO remote tip; report the real exit code and the resulting
     remote tip in your completion report instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C6: the `## Session` section constraint 14 orders, feature and
             round, branch, the round base SHA `c23e7cc6`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S6, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY which decision types
             the gate enforces after this round and which still carry the legacy
             placeholder, and that `R-0713` is FIXED IN CODE but still OPEN in
             the record until a reviewer authors its `Done:` text.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R9
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
R9 closes session 2. It upgrades the stop-reason producer, which copied a
structured record into a card and cited none of its identifiers, and it
registers and fixes `R-0713`: the patch-approval summary's `'?'` default can
never fire, because `list_patch_intents` always sets `target_path` and leaves
it EMPTY rather than absent, so an intent naming no file rendered a card with
no subject at all. Four of the eight producing types are enforced after this
round.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R8 verdict and R-0713 | ordered | findings persist before repair |
| C3 the R-0713 fix | ordered | S2, one line |
| C4 the stop-reason triple and the gate set | ordered | S3 to S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the session-closing handback | ordered | |

## Next Steps
1. Next session: re-read `.agent/STOP` from disk, then the Open PR Gate, then
   author `Done: R-0713` against the fix this round landed.
2. T002 finishes with memory-review, repo-dirty and the two branches that
   already carry an options list. Repo-dirty's event carries the thinnest
   evidence of the eight; the flight plan has two arms and only one offers
   options, so enforcing that type needs a ruling on what a RESOLVED decision
   owes.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- `R-0713` is fixed in code but stays OPEN in the record until a reviewer
  authors its `Done:` text.
- Four types are enforced from this round on, so a later change that regresses
  any of their triples raises instead of rendering. That is the intent.
<<<END PLANF032R9

<<<SLICE LEDGER9
Gate: F032 R8 — the F032 T002c PATCH-APPROVAL entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself at `c23e7cc633fb`. TRANSPORT IS PROVED END TO END: the reviewer computed sha256 `2330a04d4f4aa3bea3709684b667e217719dcf9d994b52da7baf9f95950c51e3` over 30021 bytes and 356 lines BEFORE delegating, and the committed `.agent/authored/f032-r8.md` blob carries exactly that digest, with C0a and C0b the SAME git blob `2289deea8679`; the chain runs from a value the reviewer held independently through the saved copy to its mirror, and claims nothing about the bytes of any prompt. EXTRACTION printed 2 regions at 46 and 3 content lines, CONTENT 49, TOTAL 356, PROSE 307. THE PLAN at C1 is byte-equal to PLANF032R8 with the minus-newline control FALSE and `wc -l` 46. THE LEDGER APPEND is 1059172 + 1 + 6251 = 1065424 with the base a byte PREFIX, the second reader counted N 2 and found the last two units EQUAL IN ORDER to the slice's paragraphs, and a byte flipped inside the FIRST appended paragraph was REJECTED by both readers. THE SETS MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 59 to 60 adding exactly `F032 R7`, `^Done: R-\d+ — ` 22 to 23 adding exactly `R-0712`, while `^- R-\d+ — ` stayed 273, `^Landed: R-` stayed 1 and `^Gate: R\d+ — ` stayed 19; the open set 251 to 250, maximum `R-0712` at both points, and no id resolved that was never registered. THE PRODUCER NOW CITES WHAT IT ALWAYS HAD: the patch-approval branch emits a `decision` ref for the intent id, which `list_patch_intents` builds from the artifact's short id and the explanation's index so it is never empty, and a `file` ref for the target path ONLY when that path is non-empty. THE OPTIONLESS SHAPE IS A RULING APPLIED, NOT INVENTED, and the round is right to have applied it: this branch's `next_actions` are two full `remedy patch` command lines rather than two option words, so giving it `payload.options` would have CHANGED what the browser renders as answers, and amendment A3 puts growing an options list out of F032's scope — where DECISION F032 D6 moved the budget stop's options only because its `next_actions` were ALREADY the two option words. THE MUTATIONS BOTH KILLED TESTS AND THE REVIEWER REPRODUCED BOTH IN ITS OWN WORKTREE, with `__pycache__` purged and `-B` passed per the constraint R7's cache incident produced: control a REAL exit 0 at `55 passed`, dropping the type from the gate set exit 1 at `2 failed, 53 passed`, and making the file ref unconditional exit 1 at `4 failed, 51 passed` — the latter naming the omission test and all three `[no-target]` parametrizations — with a second control after both restorations again `55 passed`. THE SWEEP IS FINALLY COMPLETE, AND IT IS COMPLETE BECAUSE IT WAS ORDERED AS A PROPERTY RATHER THAN AS A LIST: the worker searched by phrase across the three live scopes, counted the branches by an AST walk rather than from prose, corrected the test docstring to `five-branch` and APPENDED to amendment A3 rather than rewriting its measurement, and reported two further hits it correctly left alone as outside the property. The reviewer re-ran that search and finds ZERO stale-count sentences remaining in all three scopes, against three that stood when R8 began. THE GUARDS DID NOT MOVE: the nine decision-schema guard files `324 passed`, `tests/docs/` `295 passed` and the golden-path canary `42 passed`, each a REAL exit 0 with zero `^FAILED` lines, and `ruff check` `All checks passed!` at exit 0. NOTHING ELSE MOVED: both path residues EMPTY over the eight-path set, `apps/` EMPTY, insertions 356, 194, 18, 4, 58, 6, 153 and 160 across the eight commits, each single-parent and under 500, markers 0 and 0 in all six written files against a CONTROL of 2 and 2, `.remedy-wt` 0 tracked, worktree 1 line, `tmp/*` 0, the Open PR Gate `[]`, and the remote tip equal to the local tip. THE WORKER FOUND A DEFECT IT WAS NOT LOOKING FOR AND DECLARED IT INSTEAD OF FIXING IT, which is the behaviour this workflow is built to get: the patch-approval summary's `'?'` default cannot fire, and that is `R-0713`, registered by the round after this one. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0713 — Low — the patch-approval card's placeholder can never appear, so an intent that names no file renders a summary with no subject and a double space. `packages/orchestration/decision_queue.py` builds that card with `safe_summary=f"Patch intent for {pi.get('target_path', '?')} awaits approval."`, and a `dict.get` default fires only when the KEY IS ABSENT. `list_patch_intents` always sets `target_path`, to the empty string when the explanation named no `file`, so the `'?'` the line was written to show is unreachable and the card reads `Patch intent for  awaits approval.` The reviewer measured this at `c23e7cc633fb` by DEMONSTRATION rather than by reading: an artifact whose only explanation is a `preview-only` entry with no `file` key yields `target_path` `''` with the key PRESENT, and `list_decisions` over that job renders exactly that sentence. IT WAS FOUND BY THE R8 WORKER, which was upgrading this very branch, noticed the neighbouring line, and DECLARED IT UNDER DEVIATIONS RATHER THAN REPAIRING IT because the line sat outside its spec items — the correct call, and the reason it is registered here rather than having landed silently. SEVERITY IS LOW: nothing is corrupted, the card appears, the evidence refs are unaffected because R8's `file` ref is correctly guarded on the same value, and only the one-line summary loses its subject. It is the THIRD member of a family this feature keeps meeting — `R-0711` said the wrong true thing, `R-0712` read a key nobody writes, and this one guards on absence where the real shape is present-and-empty — and the family's common cause is that these summaries were written from an assumed record shape rather than from the record the producer actually yields. FIX, in this same round: use the `_pa_target_path` value R8 already computes directly above for the ref guard, falling back to `'?'` when it is empty, and pin the rendered summary for both the named-file and the no-file case. OPEN.
<<<END LEDGER9
