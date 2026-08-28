STEP R7 / F032 — T002b: THE TEST-FAILURE CARD LEARNS TO NAME THE TEST
Goal:        FIX A DEFECT THIS ROUND FOUND, THEN GIVE THAT PRODUCER ITS
             RECEIPTS. The test-failure branch reads the failing command out of
             the event key `command`, and no producer in this repository ever
             writes that key: the emitter writes `command_safe`, which the
             repair loop reads correctly twice. So every test-failure card in
             production renders `Test '?' failed.` — a blocker asking a human to
             look at a test it cannot name. That is `R-0712`, registered and
             fixed here. The same round gives the branch a real triple and adds
             `test_failure` to `TRIPLE_REQUIRED_TYPES`, and retires two comments
             R6 falsified. YOU CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the R6 verdict and `R-0712` · C3 the `R-0712` fix · C4
             the test-failure triple, the gate set and the two retired
             comments · C5 its tests · C6 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r7.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/decision_queue.py`,
             `packages/orchestration/decision_evidence.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G7 orders a disposable
             worktree and G8 orders a push. NOTHING under `apps/` or `docs/` is
             written. NO EXISTING TEST FILE other than the one this feature
             created is edited — in particular
             `tests/orchestration/test_decision_inbox.py` is NOT touched, and
             the fix in S2 is deliberately shaped so that it does not need to
             be. If a guard elsewhere goes red, that is a real finding and you
             hand back rather than edit it.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r7.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r7.md` — with `shutil.copyfile` or a read-then-write
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
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. `R-0712` is
    REGISTERED at C2 and FIXED at C3, in that order and never the reverse —
    findings persist first so nothing is lost if the session dies mid-repair.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R6. That is
    ordered: the plan becomes current at C1.
 6. `.agent/live_review.md` IS APPEND-ONLY AND IS WRITTEN ONCE THIS ROUND, AT
    C2, AS A PURE APPEND. Nothing already in it is rewritten, deleted,
    renumbered or touched. An append-only record is corrected by appending.
 7. YOU AUTHOR NO RECORD TEXT OF YOUR OWN THIS ROUND. You mint no finding id,
    write no `Gate:` paragraph, no `Done:` paragraph and no `Landed:` line. The
    only text entering `.agent/live_review.md` is the LEDGER7 slice, which the
    reviewer wrote. If this round's work makes you believe a NEW finding
    exists, DO NOT register it — describe it in the handback under Deviations
    and let the reviewer mint it.
 8. THE LEDGER SETS MOVE AS FOLLOWS. Across C2: `^Gate: F\d+ R\d+ — ` moves 58
    to 59 with the ADDED key exactly `F032 R6`; `^- R-\d+ — ` moves 272 to 273
    with the ADDED id exactly `R-0712`; `^Done: R-\d+ — ` stays 22,
    `^Landed: R-` stays 1 and `^Gate: R\d+ — ` stays 19. The open set moves 250
    to 251 and the maximum id `R-0711` to `R-0712`. Across C3, C4 and C5 EVERY
    ONE OF THOSE COUNTS IS UNCHANGED.
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
    `8c481088d511f9ec67ecd66ca697b59a6c553fc0` was measured by the reviewer at
    that commit. It is a REFERENCE to report against, NOT a target to
    reproduce. Where your measurement differs, report BOTH and reconcile
    NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R7 is a whole-file
    replacement of `.agent/plan.md`; LEDGER7 is an append. The two retired
    comments of S5 are edits you make to source you have read, not slices.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 2
    of F032 and that R7 is the round. Session 1 was rounds R1 through R5; this
    session began at R6. The soft limit is 25 rounds or 7 sessions, whichever
    comes first, and neither is near. The handback has NO LENGTH CAP —
    amend0827 rule 3 withdrew every tier — so do not declare, measure or
    apologise for its length.

Spec — T002b, the test-failure card.
 S1. READ FIRST. In `packages/orchestration/decision_queue.py` the
     test-failure branch selects events named `test_run_completed` whose
     `metadata.status` is `failed`, takes the last three, and for each reads
     `meta.get("command", "?")` into `cmd` and
     `meta.get("test_run_id", "unknown")` into the decision id. At
     `8c481088d511` the reviewer measured `cmd = str(meta.get("command", "?"))`
     as occurring EXACTLY ONCE in that file, and likewise
     `safe_summary=f"Test '{cmd}' failed."` and `type="test_failure",`.
 S2. THE FIX FOR `R-0712`, and it is a READ, not a rename. The producer of this
     event is `test_execution_service._safe_event_meta`, which writes the key
     `command_safe` and never `command`; `packages/orchestration/repair_loop.py`
     reads `command_safe` from the same event at two places. So the branch must
     prefer `command_safe`, FALL BACK to `command`, and only then to `"?"`.
     THE FALLBACK IS DELIBERATE AND IS NOT DEAD CODE: `_fixture_test_failure` in
     `tests/orchestration/test_decision_inbox.py` writes `command`, that file is
     outside this round's change set, and a read of `command_safe` alone would
     leave it rendering the placeholder. Say so in a comment at the site, naming
     the producer key and the reason the older key is still honoured.
 S3. THE REFS COME FROM THE SAME EVENT. Always emit a ref of kind `failure`
     targeting the test run id — the value the decision id is already built
     from, including its `unknown` default, which is honest rather than empty —
     labelled as the test run that failed. Emit a SECOND ref of kind `failure`
     targeting the command resolved by S2, labelled as the command that was
     run, ONLY when that value is non-empty and is not the `"?"` placeholder.
     Never emit a ref whose target is the empty string.
 S4. THE OUTCOME IS UNKEYED, because this branch offers no options: it carries
     no `payload` and its `next_actions` are instructions rather than choices,
     so DECISION F032 D3's optionless case applies and rule (h) requires
     EXACTLY ONE outcome keyed `UNKEYED_OPTION`. It states what reading the
     failure buys and what it costs, in this producer's own terms — reading the
     named run's output shows which assertion failed, so the repair targets the
     real cause instead of a guess, at the cost of the job staying blocked while
     that happens and of a failure caused by the environment rather than the
     change spending that time for nothing. THE EXACT WORDING IS YOURS. It must
     not be, or contain as its whole value, any member of `BOILERPLATE_PHRASES`.
     DO NOT add a `payload` to this branch.
 S5. `test_failure` JOINS THE GATE SET IN THE SAME COMMIT AS ITS TRIPLE. In
     `packages/orchestration/decision_evidence.py`, `TRIPLE_REQUIRED_TYPES`
     becomes a frozenset holding exactly `token_budget` and `test_failure`. TWO
     COMMENTS IN THAT SAME FILE ARE NOW FALSE AND ARE RETIRED IN THIS COMMIT:
     the `#:` block above `UNKEYED_OPTION` and the docstring of
     `evidence_triple_problems` each say that SIX of the eight producing
     branches carry no options list, and R6 gave the budget stop one, so three
     branches now carry an options list and five do not. Correct both to the
     number you MEASURE, and state the count as the reviewer's measurement
     rather than trusting this sentence: count the branches in
     `decision_queue.list_decisions` that set an `options` key. Retire nothing
     else.
 S6. THE TESTS GO IN `tests/orchestration/test_decision_evidence.py`, the file
     this feature created, and nowhere else. Update the exact-membership
     assertion so it names both enforced types. Then add tests driving the REAL
     branch through `list_decisions` from a `test_run_completed` event whose
     `metadata.status` is `failed`: one carrying `command_safe` as the real
     producer writes it, one carrying only the older `command` key, and one
     carrying neither. Assert the RENDERED `safe_summary` in all three — the
     first two naming the command, the third being the honest placeholder — and
     assert the ref kinds and targets and the single unkeyed outcome's text.
     PIN THE DEFECT ITSELF: a test must fail if the branch goes back to reading
     `command` first, and its name should say so. Assert the exported card's
     `evidence_status` is `present`. And assert that a `test_failure` decision
     built WITHOUT a triple raises `DecisionEvidenceError`.

Done when:
 G1. HYGIENE, BASE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a and
     confirm it is the round base named in constraint 12; report the branch is
     `feature/f032-evidence-triple`; report `git status --porcelain` line count
     after EACH of C0a through C6, each 0; report whether `.agent/STOP` exists
     at the two readings constraint 9 orders.
 G2. TRANSPORT. Report the sha256, byte count and line count of
     `.remedy-wt/f032-r7.md`, of the committed `.agent/authored/f032-r7.md`
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
     PLANF032R7 under the convention of constraint 2, and report the same
     comparison with the trailing newline removed as a NEGATIVE CONTROL, which
     must be FALSE. Report `wc -l` and that it is under 50, and the counts of
     `^## Goal$` and `^## Next Steps$`.
 G5. THE LEDGER APPEND. Prove `.agent/live_review.md` at C2 equals its
     pre-commit blob plus ONE newline plus the LEDGER7 slice, byte for byte,
     and report the arithmetic as three numbers summing to the result; report
     that the pre-commit blob is a byte PREFIX of the result. The reviewer
     measured the base at `8c481088d511` as 1051985 bytes over 419 blank-line
     units. Then run a SECOND, INDEPENDENT structural reader: split the whole
     file on blank lines, let N be the number of paragraphs in the LEDGER7
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
     at the round base. Then, in a python heredoc, drive `list_decisions` THREE
     times with a `test_run_completed` event whose `metadata.status` is
     `failed`: once with `command_safe` and a `test_run_id`, once with the older
     `command` key instead, once with neither. For each, report VERBATIM the
     decision's id, its `safe_summary`, its `payload`, every ref as a
     kind/target/label triple, and the outcome as option/expected_outcome/
     downside. Report the value of `TRIPLE_REQUIRED_TYPES`. Report the count you
     measured for S5 of branches setting an `options` key, and quote the
     replacement text of each of the two retired comments.
 G7. TESTS GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. After C5 run
     `python3 -m pytest tests/orchestration/test_decision_evidence.py -q` and
     report the REAL exit code and summary VERBATIM. Then create ONE disposable
     worktree at the C5 commit under `.remedy-wt/`, run that same scoped
     command there UNMUTATED FIRST as the CONTROL and report its real exit code
     and summary. Then, in that worktree and one at a time, restoring between
     them: (a) make the command read prefer `command` over `command_safe`,
     which is the `R-0712` defect restored; (b) remove `test_failure` from
     `TRIPLE_REQUIRED_TYPES`, leaving `token_budget` alone. Report the REAL exit
     code and summary for each. BEFORE APPLYING EACH, report the count of the
     exact bytes you are about to change IN THE FILE YOU CHANGE THEM IN, at the
     commit the worktree sits at; if any count is not 1, widen the string until
     it is and report the string you used. REPORT THE COLOUR AND THE COUNT YOU
     OBSERVE — this block names no expected number of failures and no test
     name. IF EITHER MUTATION LEAVES THE RUN GREEN, say so plainly: that is a
     real finding about the tests. Remove the worktree and prune. Then, in the
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
     THE ROUND TURNS ON: `test_failure` becomes enforced at C4, and
     `_fixture_test_failure` in the inbox guard drives that branch, so a triple
     the branch fails to build shows up here as a raise rather than as a card.
 G8. STRUCTURE, THE CANARY, THE PR GATE AND THE PUSH. Run
     `python3 -m pytest tests/cli/test_golden_path.py -q` and report the REAL
     exit code and summary VERBATIM; the reviewer measured `42 passed` at exit
     0 at the round base. Compare the path set of `git diff --name-only
     8c481088..C5` BOTH WAYS against this round's expected set — the Change
     line's list MINUS `.agent/handoff.md` — and report both residues EMPTY.
     Report `git diff --stat 8c481088..C5` restricted to `apps/` and to `docs/`
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
             round, branch, the round base SHA `8c481088`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S6, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY which decision types
             the gate enforces after this round and which still carry the legacy
             placeholder, and that `R-0712` is FIXED IN CODE but still OPEN in
             the record until a reviewer authors its `Done:` text.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R7
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
R7 continues T002 with the test-failure producer, and it starts by repairing
what reading that branch exposed. The card names the failing command from the
event key `command`, which no producer writes — the emitter writes
`command_safe` — so every such card in production reads `Test '?' failed.`
That is `R-0712`, registered and fixed here, and the branch then gets its refs
and its one unkeyed outcome and joins the enforced set.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R6 verdict and R-0712 | ordered | findings persist before repair |
| C3 the R-0712 fix | ordered | S2, the command read |
| C4 the triple, the gate set, two retired comments | ordered | S3 to S5 |
| C5 its tests | ordered | S6, then the red-proofs |
| C6 the handback | ordered | |

## Next Steps
1. T002 continues with the repo-dirty and patch-approval producers, each
   joining `TRIPLE_REQUIRED_TYPES` in the commit that gives it a real triple.
2. Then memory-review and stop-reason, then the two branches that already
   carry an options list.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- Two types are enforced from this round on, so a later change that regresses
  either triple raises instead of rendering. That is the intent.
- The inbox guard's own test-failure fixture writes the older `command` key,
  so the fix keeps reading it; the new tests cover the real producer's key.
<<<END PLANF032R7

<<<SLICE LEDGER7
Gate: F032 R6 — the F032 T002a BUDGET-STOP entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself at `8c481088d511`. TRANSPORT IS PROVED END TO END FOR THE FIRST TIME THIS FEATURE, AND THAT IS WORTH STATING PRECISELY: the reviewer computed the block's sha256 `7018fa817a638c7cb3b4612326fa85fc477c063abd525a295739048a0f873492` over 30984 bytes and 404 lines BEFORE delegating, and the committed `.agent/authored/f032-r6.md` blob carries exactly that digest, with C0a and C0b the SAME git blob `8a69c3970dce`. The chain therefore runs from a value the reviewer held independently through the worker's saved copy to its mirror, which is stronger than three readings of the worker's own output; it does NOT claim the bytes of any prompt. EXTRACTION from the committed blob printed 4 regions at 45, 3, 40 and 12 content lines, CONTENT 100, TOTAL 404, PROSE 304, both caps met. THE PLAN at C1 is byte-equal to PLANF032R6 with the minus-newline control FALSE, `wc -l` 45, `^## Goal$` and `^## Next Steps$` each 1. THE THREE APPENDS EACH PROVE base plus ONE newline plus slice with the base a byte PREFIX, and the reviewer reproduced all three from the committed blobs: `.agent/live_review.md` 1047137 + 1 + 4847 = 1051985, `.agent/decisions.md` 639470 + 1 + 2601 = 642072, and `docs/roadmap/features/T5_F032.md` 9364 + 1 + 846 = 10211. THE SECOND, INDEPENDENT LEDGER READER counted N 2 and found the last two blank-line units EQUAL IN ORDER to the slice's two paragraphs, with a byte flipped inside the FIRST appended paragraph REJECTED by both readers. THE SETS MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 57 to 58 adding exactly `F032 R5`, `^Done: R-\d+ — ` 21 to 22 adding exactly `R-0711`, while `^- R-\d+ — ` stayed 272, `^Landed: R-` stayed 1 and `^Gate: R\d+ — ` stayed 19; the open set 251 to 250 and the maximum id `R-0711`. `^## DECISION F032 D\d+ ` moved 5 to 6 adding exactly `D6`, `^## DECISION ` 163 to 164, and the feature file gained `A6` while `^## Design amendments$` stayed 1. THE PRODUCER IS REAL AND THE REVIEWER READ IT BACK BY BEHAVIOUR: the budget branch builds one `failure` ref for the stop reason it always has, adds a `failure` ref for the exhausted limit and a `decision` ref for the request id ONLY when the stop event carried them, and keys one outcome to `extend` and one to `abandon`; `ruff check` over both modules is `All checks passed!` at a REAL exit 0. THE FALLBACK WORDING WAS CAUGHT BEFORE IT SHIPPED, by the reviewer's own pre-emission dry run rather than by a gate: interpolating the limit as a bare word renders `a raised the exhausted limit`, so the block ordered a whole noun phrase and the worker built one, which the reason-only test pins. THE MUTATIONS BOTH KILLED TESTS AND THE REVIEWER REPRODUCED BOTH IN ITS OWN DISPOSABLE WORKTREE: the unmutated control is a REAL exit 0 at `36 passed`, emptying `TRIPLE_REQUIRED_TYPES` is exit 1 at `2 failed, 34 passed`, and replacing one downside with the boilerplate `-` is exit 1 at `8 failed, 28 passed` — the second failing at the emit gate itself, which is the proof that the gate is live for this type end to end. THE GUARDS DID NOT MOVE: the nine decision-schema guard files `324 passed`, `tests/orchestration/test_f018_authority_integration.py` `114 passed` with its three `("extend", "abandon")` assertions intact, and the golden-path canary `42 passed`, each a REAL exit 0 with zero `^FAILED` lines. NOTHING ELSE MOVED: both path residues EMPTY over the nine-path set, `apps/` EMPTY, insertions 404, 318, 21, 4, 54, 78, 196 and 78 across the eight commits, each single-parent and under 500, markers 0 and 0 in all seven written files against a CONTROL of 4 and 4, `.remedy-wt` 0 tracked, worktree 1 line, `tmp/*` 0, the Open PR Gate `[]`, and the remote tip equal to the local tip. THE ONE DEFECT THE ROUND LEFT BEHIND IS THE REVIEWER'S AND IS RECORDED AGAINST `R-0593` RATHER THAN GIVEN AN ID OF ITS OWN, per §3 checklist item 30: `R-0593` is OPEN and already holds the class "a comment this round falsified is retired at its source", its fix clause binds the next block that adds a capability an existing comment calls absent, and this block's S5 named only two such comments when four sentences were falsified. The two it missed are in `packages/orchestration/decision_evidence.py`, above `UNKEYED_OPTION` and in the docstring of `evidence_triple_problems`, both saying SIX of the eight producing branches carry no options list where R6 made it five; the WORKER FOUND BOTH, declared them under Deviations and correctly did not fix them, because S5 said retire nothing else. R7's S5 orders the retirement. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0712 — Medium — the test-failure card cannot name the test, because it reads a metadata key no producer writes. `packages/orchestration/decision_queue.py` builds that card with `cmd = str(meta.get("command", "?"))` and renders `safe_summary=f"Test '{cmd}' failed."`, while the only emitter that can produce the event this branch selects — `test_execution_service._safe_event_meta`, which the branch's own filter reaches by requiring `metadata.status == "failed"` — writes the key `command_safe` and never `command`. The reviewer measured this at `8c481088d511` by DEMONSTRATION rather than by reading: building the event exactly as `_safe_event_meta` builds it and running `list_decisions` over it yields `safe_summary` `"Test '?' failed."`, and the same event with the key renamed to `command` yields `"Test 'pytest tests/orchestration -q' failed."` The sibling consumer of that same event has it right in two places — `packages/orchestration/repair_loop.py` reads `meta.get("command_safe", "")` at its failure-context builder and again at its command display — so the key is settled and this branch is simply reading the wrong one. THE DEFECT WAS INVISIBLE BECAUSE THE FIXTURE MIRRORS THE BUG: `_fixture_test_failure` in `tests/orchestration/test_decision_inbox.py` writes `"command": "pytest -q"`, so the guard that drives every producing type exercises the reader's key rather than the emitter's, and the only assertion over that card is that it APPEARS. SEVERITY IS MEDIUM AND NOT LOW, which is the distinction against the neighbouring `R-0711`: that card said something true but unhelpful, while this one is a `blocker`-severity decision whose entire informational payload is a placeholder, on every test failure in production. It is not High because nothing is corrupted, the card still appears, and `next_actions` still routes the human to the run. FIX, in this same round: prefer `command_safe`, keep `command` as a fallback so the inbox guard's fixture is not silently broken by a change outside its file, and pin the rendered summary for the producer's key, the older key and the neither case. THE LESSON IS THE FIXTURE, NOT THE READ: a test fixture written from the READER's side cannot fail on a reader that disagrees with every writer, and F032's remaining producer upgrades each read event metadata the same way. OPEN.
<<<END LEDGER7
