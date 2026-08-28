STEP R5 / F032 — THE MEMORY-REVIEW SUMMARY, AND THE SESSION'S RECORD
Goal:        FIX THE DEFECT R4 EXPOSED AND CLOSE THE SESSION'S RECORD. When
             `R-0710`'s fix made memory cards flagged `needs_review` reach the
             inbox at last, it also made them arrive under a summary that reads
             `Memory 'x' is active.` — the card's one line states the card's
             VALIDITY, which for the newly surfaced half is not the reason the
             card exists. A decision whose whole purpose is human review must
             say what it is asking about. That is `R-0711`, registered and
             fixed here. The same round books the reviewer's verdicts on R2, R3
             and R4, which are PASS, PASS and PASS, and ends the session with a
             handoff. YOU CREATE NO PULL REQUEST AND MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the ledger append, three verdicts and one new finding ·
             C3 the summary fix · C4 its tests · C5 the one `Landed:` line ·
             C6 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r5.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `packages/orchestration/decision_queue.py`,
             `tests/orchestration/test_decision_evidence.py`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G7 orders a disposable
             worktree and G8 orders a push. NOTHING under `apps/` or `docs/` is
             written. NO EXISTING TEST FILE other than the one this feature
             created is edited — if a guard elsewhere goes red, that is a real
             finding and you hand back rather than edit it.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r5.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r5.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own; G2 has you measure
    four points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations. Declaring beats fixing every time.
 3. THE PRODUCTION CODE IS SPECIFIED, NOT SLICED. Items S1 through S4 describe
    what the code must DO. You write it, in the house style of the module.
 4. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5, C6. The finding
    is REGISTERED at C2 and FIXED at C3, in that order and never the reverse —
    findings persist first so nothing is lost if the session dies mid-repair.
 5. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R4. That is
    ordered: the plan becomes current at C1.
 6. `.agent/live_review.md` IS APPEND-ONLY AND IS WRITTEN TWICE THIS ROUND, AT
    C2 AND AT C5, EACH TIME AS A PURE APPEND. Nothing already in it is
    rewritten, deleted, renumbered or touched at either commit. An append-only
    record is corrected by appending.
 7. THE C5 LINE IS THE ONLY TEXT OF YOUR OWN THAT ENTERS THE RECORD, AND ITS
    SHAPE IS FIXED. Append exactly one line, of the form
    `Landed: R-0711 — <one line: what changed, which commit>`, preceded by one
    blank line. You never author a `Done:` paragraph, never write a `Gate:`
    paragraph and never mint a finding id: `Done:` is reserved for the
    reviewer's authored text, so a surviving `Landed:` line correctly reads as
    a fix that has not yet been through a gate. That is what it should look
    like when this session ends.
 8. THE LEDGER SETS MOVE AS FOLLOWS. Across C2: `^Gate: F\d+ R\d+ — ` moves 54
    to 57 with the ADDED keys exactly `F032 R2`, `F032 R3` and `F032 R4`;
    `^- R-\d+ — ` moves 271 to 272 with the ADDED id exactly `R-0711`;
    `^Done: R-\d+ — ` stays 21, `^Landed: R-` stays 0 and `^Gate: R\d+ — `
    stays 19; the open set moves 250 to 251 and the maximum id `R-0710` to
    `R-0711`. Across C5: `^Landed: R-` moves 0 to 1 and EVERY OTHER COUNT
    ABOVE IS UNCHANGED.
 9. RE-READ `.agent/STOP` FROM DISK before C0a and again before C6. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
10. THE ONLY DESTRUCTIVE WORK IS G7's, AND IT IS ISOLATED. The mutation
    red-proof runs ONLY inside a disposable `git worktree` created under
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
12. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `9d1bb06e` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
13. THERE ARE NO FROM/TO REPLACEMENT PAIRS. PLANF032R5 is a whole-file
    replacement of `.agent/plan.md`; LEDGER5 is an append.
14. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F032, that R5 is the round, and that SESSION 1 ENDS HERE with five
    delegated rounds. The handback has NO LENGTH CAP — amend0827 rule 3
    withdrew every tier — so do not declare, measure or apologise for its
    length. THIS IS THE SESSION-CLOSING HANDBACK and the next session reads it
    first, so its `## Next` section is the most load-bearing text you write
    this round: name Phase 1 rule 1 of docs/agents/self_drive_protocol.md — the
    `.agent/STOP` re-read — before anything else, then the Open PR Gate, then
    T002.

Spec — the `R-0711` fix.
 S1. IN `packages/orchestration/decision_queue.py`, the memory-review branch
     currently builds `safe_summary=f"Memory '{me.key}' is {me.validity}."`.
     Replace the reason with one derived from BOTH fields the predicate reads,
     so the card says why it is in the inbox: when the card is stale AND
     flagged for review, name both; when it is stale only, name stale; when it
     is flagged only, say it is flagged for review. Choose the exact wording
     yourself — it is human-facing text and it must read as a sentence — but a
     card selected because `review_status == "needs_review"` MUST NOT render a
     summary whose only stated fact is `active`.
 S2. RENAME THE LOCAL `stale` LIST to something that describes what it now
     holds, since it no longer holds only stale cards. This is a name in code
     this round is editing anyway, which is the only kind of rename AGENTS.md's
     Code Discoverability Conventions permit; do not touch any other name.
 S3. KEEP THE `[:5]` CAP AND THE BRANCH'S EXISTING BEHAVIOUR OTHERWISE. No
     other line of that branch changes, `DECISION_TYPES` is untouched, and the
     `try`/`except` around it is untouched.
 S4. TESTS, ADDED TO `tests/orchestration/test_decision_evidence.py`, which is
     where this feature's memory-branch tests already live. Add one test per
     case: a card that is stale only, a card that is flagged for review only,
     and a card that is both — each asserting on the RENDERED `safe_summary`
     string, not merely that a decision appeared. The flagged-only case is the
     one that was wrong, so its assertion must show the summary no longer
     reports the card as active.

Done when:
 G1. HYGIENE AND THE SENTINEL. Report `git rev-parse HEAD` before C0a, which
     must be `9d1bb06ecd78b7775d1f7ef3a6bf79f03669371c`, and
     `git branch --show-current`, which must be `feature/f032-evidence-triple`.
     Report `git status --porcelain` as a LINE COUNT after each of C0a through
     C6, each 0. Report `.agent/STOP` read from disk before C0a and before C6,
     both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f032-r5.md`, as saved at C0a, as mirrored at C0b and
     as read off disk at C4 — all four must be EQUAL — and say whether C0a and
     C0b are the same git blob. Report whether any line of the block as saved
     is a run of a single repeated character at length 4 or more, which must
     come back as none. THEN STATE IN ONE SENTENCE WHAT THIS PROOF COVERS: the
     scratch file, the saved copy, its mirror and the working copy, and NOT the
     bytes of any prompt.
 G3. EXTRACTION AND CAPS. Extract the slices from the COMMITTED C0a blob by
     their marker LINES. Report how many slices your extractor printed, each
     slice's own line count, the CONTENT total, the TOTAL line count, and PROSE
     as TOTAL minus CONTENT. MARKERS ARE PROSE. PROSE at most 400, TOTAL at
     most 490.
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF032R5 under the
     newline-INCLUDED convention, with the negative control against the slice
     MINUS its trailing newline reported FALSE, `^## Goal$` 1,
     `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER
     50.
 G5. THE LEDGER APPEND AT C2, PROVED TWICE, THE SECOND READER COVERING THE
     WHOLE APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit
     blob plus ONE newline plus LEDGER5. The reviewer measured that base blob
     at `9d1bb06e`: 1032978 bytes over 412 blank-line units. If it reads
     differently before C2, something moved this round did not order — stop and
     hand back. Report both byte counts and the sum. Then the SECOND,
     INDEPENDENT reader: split the whole file on blank lines, let N be the
     number of paragraphs YOUR SCRIPT COUNTS in that slice — never a number
     this block asserts — and compare the LAST N units against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, AT A BYTE OFFSET,
     NOT A CHARACTER OFFSET — the file carries multi-byte em dashes. Flip ONE
     byte IN MEMORY and report that BOTH readers REJECT it; never mutate the
     tracked file. Then report, before C2 and after C2, the line-anchored
     counts of `^- R-\d+ — `, `^Done: R-\d+ — `, `^Landed: R-`,
     `^Gate: R\d+ — ` and `^Gate: F\d+ R\d+ — `, the finding ids and the gate
     keys ADDED and REMOVED as SETS, whether all ids are DISTINCT, the maximum
     id at each point, and the open set at each point. Every movement
     constraint 8 names for C2 is checked here, INCLUDING the non-movers.
 G6. THE FIX, LINTED AND READ BACK BY BEHAVIOUR. After C3 run `python3 -m ruff
     check packages/orchestration/decision_queue.py` and report the REAL exit
     code and output VERBATIM; the reviewer measured `All checks passed!` at
     exit 0 at the round base. Then, in a python heredoc, build three
     `MemoryEntry` values — one stale with `review_status` left at its default,
     one active with `review_status` `needs_review`, and one that is both — run
     each through the memory branch, and report the RENDERED `safe_summary`
     string for each VERBATIM. Report also the new name of the local list S2
     orders renamed, and confirm by reading the source that `[:5]` is still
     there and that `DECISION_TYPES` is unchanged.
 G7. THE TESTS, GREEN, THEN RED UNDER MUTATION, AND THE GUARDS UNMOVED. After
     C4 run `python3 -m pytest tests/orchestration/test_decision_evidence.py -q`
     and report the REAL exit code and summary VERBATIM. Then create ONE
     disposable worktree at the C4 commit under `.remedy-wt/`, run that same
     scoped command there UNMUTATED FIRST as the CONTROL and report its real
     exit code and summary, then revert S1's summary to
     `f"Memory '{me.key}' is {me.validity}."` and report the REAL exit code and
     summary again. REPORT THE COLOUR AND THE COUNT YOU OBSERVE — this block
     names no expected number of failures and no test name. IF THE MUTATION
     LEAVES THE RUN GREEN, say so plainly: that is a real finding about the
     tests. Remove the worktree and prune. Then, in the primary checkout, run
     as ONE pytest process `python3 -m pytest
     tests/orchestration/test_decision_inbox.py
     tests/orchestration/test_approval_queue.py
     tests/orchestration/test_budget_stop_integration.py
     tests/orchestration/test_escalation.py
     tests/orchestration/test_bundled_clarification.py
     tests/cli/test_plan_approval.py tests/orchestration/test_handoff.py
     tests/cli/test_decision_answers.py tests/cli/test_open_decisions_view.py
     -q` and report the REAL exit code, the summary VERBATIM and the `^FAILED`
     count, proving your extractor sighted on a string containing such a line;
     the reviewer measured `324 passed` at a REAL exit 0 at the round base.
 G8. THE C5 APPEND, STRUCTURE, THE STATE READERS, THE OPEN PR GATE AND THE
     PUSH. For C5 report that `.agent/live_review.md` equals its pre-commit
     blob plus ONE newline plus your one `Landed:` line, that the file STARTS
     WITH that blob as a byte PREFIX, and the five line-anchored counts before
     and after, of which only `^Landed: R-` moves and only from 0 to 1. Run as
     ONE pytest process `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q` and report the REAL exit code, summary VERBATIM and `^FAILED` count;
     the reviewer measured `620 passed` at a REAL exit 0 at the round base.
     Compare the path set of `git diff --name-only 9d1bb06e..C5` BOTH WAYS
     against this round's expected set — the Change line's list MINUS
     `.agent/handoff.md` — and report both residues EMPTY. Report `git diff
     --stat 9d1bb06e..C5` restricted to `apps/` and to `docs/` and confirm each
     EMPTY. Report each commit's insertions from `git diff --numstat` for C0a
     through C5, confirm each single-parent and under 500. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in every file this round writes
     other than the two block copies, against a CONTROL over the C0a blob which
     is not 0. Report `git ls-files .remedy-wt` 0 lines, `git worktree list` 1
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
             round, branch, the round base SHA `9d1bb06e`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item AND every spec item S1
             through S4, ONE LINE PER GATE for G1 through G8 with its real exit
             code, the open-findings count after this round, and the next
             expected action. C6 cannot table its own numstat — write `self` in
             that cell, as `R-0149` requires. STATE PLAINLY that `R-0711` is
             FIXED IN CODE but still OPEN in the record, awaiting the next
             session's reviewer-authored `Done:` text, and that the `Landed:`
             line at C5 is what marks it.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R5
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D5.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R5 closes session 1. It books the reviewer's verdicts on R2, R3 and R4, all
PASS, and registers and fixes `R-0711`: `R-0710`'s repair finally let memory
cards flagged `needs_review` reach the inbox, and they arrived under a summary
reporting their VALIDITY, so a card surfaced for review announced itself as
active. T001 is complete after this round — the schema, the emit gate, the
legacy placeholder and the canary are all on disk and pinned.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 three verdicts and R-0711 | ordered | findings persist before repair |
| C3 the summary fix | ordered | S1 through S3 |
| C4 its tests | ordered | S4, then the red-proof |
| C5 the Landed line | ordered | worker's only record text |
| C6 the handback | ordered | session-closing |

## Next Steps
1. Next session: re-read `.agent/STOP` from disk, then the Open PR Gate, then
   author `Done: R-0711` against the fix this round landed.
2. T002: upgrade the producers one at a time, adding each type to
   `TRIPLE_REQUIRED_TYPES` only once its triple is real, with the content
   goldens and the anti-boilerplate assertions.
3. T003 card enrichment and the chip deep links, then the integration gate.

## Risks
- `R-0711` is fixed in code but stays OPEN in the record until a reviewer
  authors its `Done:` text; the `Landed:` line is what says so on disk.
- `TRIPLE_REQUIRED_TYPES` is still empty, so the gate protects nothing in
  production yet. That is by design and T002 is what closes it.
<<<END PLANF032R5

<<<SLICE LEDGER5
Gate: F032 R2 — the F032 SPEC-RULING entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself. TRANSPORT HELD AT FOUR POINTS: the scratch original `.remedy-wt/f032-r2.md`, the C0a blob, the C0b blob and the working copy are ALL sha256 `aff393911ae36fa1d9fd9e67e7f7b22768612aac9c7b7624b3099659d490c7a7` over 32683 bytes and 403 lines, C0a and C0b the SAME git blob `cf46ca655194`, no line a run of one repeated character at length 4 or more, and the reviewer HELD THAT DIGEST BEFORE DELEGATING; the proof covers the scratch file, the saved copy, its mirror and the working copy, and NOT the bytes of any prompt. EXTRACTION from the committed C0a blob printed 4 slices at 45, 3, 103 and 37 content lines, CONTENT 188, TOTAL 403, PROSE 215, both caps met. THE PLAN at C1 is byte-equal to PLANF032R2 with the minus-newline control FALSE and `wc -l` 45. THE THREE APPENDS EACH PROVE THE SAME WAY, base plus ONE newline plus slice, byte for byte, with the base a byte PREFIX of the result in every case: `.agent/live_review.md` 1025611 + 1 + 7366 = 1032978, `.agent/decisions.md` 626914 + 1 + 6404 = 633319, and `docs/roadmap/features/T5_F032.md` 4980 + 1 + 2310 = 7291 — every base equal to the reviewer's own reading at `d3160d00`. THE SECOND, INDEPENDENT LEDGER READER counted N 2 with units 410 before and 412 after, the last two units EQUAL IN ORDER to the slice's two paragraphs, and a one-byte flip at offset 1025622 inside the FIRST appended paragraph REJECTED by both readers. THE SETS MOVED EXACTLY AS ORDERED: `^Gate: F\d+ R\d+ — ` 53 to 54 adding exactly `F032 R1`, `^- R-\d+ — ` 270 to 271 adding exactly `R-0710`, while `^Done: R-\d+ — ` stayed 21, `^Landed: R-` stayed 0 and `^Gate: R\d+ — ` stayed 19; ids DISTINCT at both points, maximum `R-0709` to `R-0710`, open set 249 to 250. THE DECISION KEYS moved 0 to 3, adding exactly `## DECISION F032 D1`, `D2` and `D3`, with `^## DECISION ` overall 158 to 161, and the feature file gained `^## Design amendments$` 0 to 1 while `## Do not touch` still occurs exactly once. THE SUITES ARE GREEN AND THE REVIEWER RE-RAN BOTH SERIALLY: `tests/docs/` with the roadmap index at `325 passed` and the four state readers with the canary at `620 passed`, each a REAL exit 0. NOTHING ELSE MOVED: both path residues EMPTY over the six-path set, `apps/`, `packages/` and `tests/` each EMPTY, insertions 403, 321, 23, 4, 104 and 38, each single-parent and under 500, markers 0 and 0 in all four written files against a CONTROL of 4 and 4, `.remedy-wt` 0 tracked, worktree 1 line, the Open PR Gate read and NOT acted on at `[]`, and the remote tip equal to the local tip. THE ROUND'S SUBSTANCE IS THAT A SPEC WAS RULED AGAINST MEASUREMENT RATHER THAN AGAINST INTENTION. R1's inventory found three assumptions in the feature file that the source does not meet, and this round settled all three as DECISION F032 D1, D2 and D3 and mirrored them into the feature file where a builder reads them: the enforcement point is the DERIVATION point because no enqueue seam exists; F032 defines its own minimal ref and does not block on the unbuilt F066; and the triple is keyed per option only where options exist, six of the eight branches having none. THE WORKER DECLARED A CONTRADICTION IN THE REVIEWER'S OWN SLICE RATHER THAN FIXING IT: an item-status row in PLANF032R2 wrapped across two source lines and rendered as two table rows. That is the reviewer's authoring slip, it damaged nothing under `packages/`, `apps/`, `tests/` or `docs/`, and under operator amendment amend0827 rule 2 it is one dated line in `.agent/prose_slips.md` and NOT an id — it was booked there at R3 and the R3 plan rewrite cleared it. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

Gate: F032 R3 — the F032 T001a SCHEMA entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself, INCLUDING ALL FOUR MUTATION RED-PROOFS IN ITS OWN DISPOSABLE WORKTREE. TRANSPORT HELD AT FOUR POINTS at sha256 `8bdf8620e1560bb615eec3cb0a6d668f0f7c5b41e54bafd00c63942d4fdbb6a7` over 26836 bytes and 406 lines, C0a and C0b the SAME blob `38a1f9efdd63`, no repeated-character run at length 4 or more, the digest held by the reviewer before delegating; the proof covers the scratch file, the saved copy, its mirror and the working copy, and NOT the bytes of any prompt. EXTRACTION printed 4 slices at 45, 43, 4 and 13, CONTENT 105, TOTAL 406, PROSE 301. THE PLAN at C1 is byte-equal to PLANF032R3 with the control FALSE and `wc -l` 45. THE THREE APPENDS prove base plus ONE newline plus slice with the base a byte PREFIX in each case: `.agent/decisions.md` 633319 + 1 + 2738 = 636058, `.agent/prose_slips.md` 1681 + 1 + 289 = 1971, and the feature file 7291 + 1 + 933 = 8225; `^## DECISION F032 D\d+ ` moved 3 to 4 adding exactly `## DECISION F032 D4`, and `.agent/live_review.md` was NOT WRITTEN AT ALL this round, which the reviewer confirmed by comparing the file's blob at the round base and at the tip and finding them EQUAL. THE NEW MODULE IS LINT-CLEAN under the repository's own `pyproject.toml` and never `--isolated` — `python3 -m ruff check` over `packages/orchestration/decision_evidence.py` and its test file returns `All checks passed!` at a REAL exit 0 on the reviewer's own re-run. ITS SURFACE WAS READ BY IMPORT RATHER THAN BY GREP: `DECISION_EVIDENCE_REF_KINDS` is exactly `coverage`, `decision`, `failure`, `file` — deliberately F066's own vocabulary so a later migration is a rename — `NO_MATERIAL_DOWNSIDE` is the literal the feature file permits by name, `UNKEYED_OPTION` is the empty string, all three dataclasses are frozen with the ordered fields their spec names, and `NO_MATERIAL_DOWNSIDE` is NOT a member of `BOILERPLATE_PHRASES`, which is the discriminator that keeps the anti-boilerplate rule from punishing the one honest benign case. THE MUTATION RED-PROOFS ARE THE ROUND'S REAL EVIDENCE AND THE REVIEWER REPRODUCED EVERY ONE: in a disposable worktree at the test commit, the UNMUTATED CONTROL is a REAL exit 0 at `15 passed`, and disabling rule (a), rule (b), rule (f) and rule (g)'s missing-option half each turns the file RED at exit 1, the last of them naming `test_an_option_with_no_outcome_is_refused`. NO MUTATION LEFT THE RUN GREEN. THE TESTS ASSERT ON THE PROBLEM SENTENCE AND NOT MERELY ON A NON-EMPTY LIST, one rule per fixture, which is why each mutation kills a specific test rather than a diffuse count. NOTHING ELSE MOVED: both path residues EMPTY over the eight-path set, `apps/` EMPTY, `packages/` and `tests/` each holding EXACTLY the one NEW file, insertions 406, 333, 24, 49, 14, 275 and 223, each single-parent and under 500, markers 0 and 0 against a CONTROL of 4 and 4, `.remedy-wt` 0 tracked, worktree 1 line, the Open PR Gate `[]`, and the remote tip equal to the local tip. THE ONE DEVIATION IS ACCEPTED AND IS COVERAGE RATHER THAN DRIFT: the worker added a thirteenth test, `test_a_malformed_triple_produces_problems_rather_than_raising`, beyond the enumeration its spec item listed. It pins a property that spec item's own text states — that no input makes the validator raise, because the emit gate will call it on every card and an exception there would lose the decision — and nothing else covered it. A worker that notices an unpinned stated contract and pins it is doing the job. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no unverified completion claim and no silent scope change.

Gate: F032 R4 — the F032 T001b EMIT-GATE entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself, including the guard suite and two of the three mutations in its own disposable worktree. TRANSPORT HELD AT FOUR POINTS at sha256 `5c720abd6f15d426b41bea8b5b79099fcd59fe703d4ffe4e377375621ebc9436` over 27497 bytes and 415 lines, C0a and C0b the SAME blob `3519e4e4c901`, no repeated-character run at length 4 or more, the digest held by the reviewer before delegating; the proof covers the scratch file, the saved copy, its mirror and the working copy, and NOT the bytes of any prompt. EXTRACTION printed 3 slices at 45, 52 and 15, CONTENT 112, TOTAL 415, PROSE 303. THE PLAN at C1 is byte-equal to PLANF032R4. THE TWO APPENDS prove base plus ONE newline plus slice with the base a byte PREFIX: `.agent/decisions.md` 636058 + 1 + 3411 = 639470 and the feature file 8225 + 1 + 1138 = 9364, `^## DECISION F032 D\d+ ` moving 4 to 5 adding exactly `## DECISION F032 D5`, `^## Design amendments$` still 1, and `.agent/live_review.md` again NOT WRITTEN, confirmed by blob comparison at base and tip. THE WIRING IS ADDITIVE AND THE REVIEWER READ IT BY IMPORT: `HumanDecision` now has 14 fields with `evidence` LAST and defaulted `None` — which is what keeps all nine construction sites working — `export_decision_json` gained `evidence_refs`, `outcomes` and `evidence_status` and dropped nothing, a decision built with no evidence exports empty lists and the literal `recorded_before_evidence_requirements`, `TRIPLE_REQUIRED_TYPES` is EMPTY, and `DecisionEvidenceError` subclasses `ValueError`. THE SAFETY ARGUMENT IS THE EMPTY SET AND IT HELD: the round changed no existing producer's behaviour, and the worker never needed to add a type to that set to make anything pass, which its block made a stop condition. THE GUARDS INVENTORY Q8 NAMED DID NOT MOVE, and this is the gate the round existed for: the nine files carrying equality guards over the decision schema run at `324 passed`, a REAL exit 0 with zero `^FAILED` lines, on the reviewer's own re-run — including the self-adjusting card-key guard and the NON-self-adjusting document-key guard — and NO EXISTING TEST FILE WAS EDITED, which the reviewer verified by listing every path under `tests/` the round touched and finding only the file this feature created. THE MUTATIONS ALL KILLED TESTS: control a REAL exit 0 at `24 passed`, and neutralising the enforcement loop, reporting the PRESENT status for a tripleless decision, and reverting `R-0710`'s predicate each turn the file RED at exit 1, naming `test_the_canary_producer_missing_a_field_is_refused`, `test_a_tripleless_decision_exports_empty_lists_and_the_legacy_status` and `test_a_needs_review_memory_card_raises_a_memory_review_decision` respectively; the reviewer reproduced the first and the third independently. `R-0710` IS FIXED IN CODE AT `e45b5026` — the memory branch now selects on `e.validity == "stale" or e.review_status == "needs_review"` with a comment naming both fields — and the worker correctly wrote NOTHING into the record, because only reviewer text resolves a finding. THE WORKER ALSO DECLARED, RATHER THAN SILENTLY REPAIRING, THAT ITS OWN EARLIER MODULE DOCSTRING HAD BECOME FALSE: R3's text said the emit gate "lives at the derivation point, not here" while R4 put the enforcement function in that very module, and it narrowed the sentence to name the gate's CALL SITE instead. THAT IS THE RIGHT CALL and it is recorded here so the narrowing is not later read as drift. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no unverified completion claim and no silent scope change.

- R-0711 — Low — the memory-review card announces its validity where it should announce its reason, so a card surfaced for review reports itself as active. `packages/orchestration/decision_queue.py` builds that card with `safe_summary=f"Memory '{me.key}' is {me.validity}."`, and until R4 that read correctly, because the only cards the branch could select were `stale` ones. `R-0710`'s fix widened the predicate to `e.validity == "stale" or e.review_status == "needs_review"`, and `review_status` and `validity` are independent fields on `MemoryEntry` (`packages/memory/models.py:44-45`): a card flagged `needs_review` normally still has `validity` `active`, so the newly surfaced half of the branch renders `Memory 'x' is active.` — a true sentence that states the one fact which does NOT explain why a human is being asked to look. Measured by the R4 worker, which declared it under Deviations and deliberately did not widen its change set to repair it, and re-measured by the reviewer at `9d1bb06e` by reading the branch. SEVERITY IS LOW AND NOT MEDIUM, and the distinction is worth stating because the neighbouring `R-0710` is Medium: nothing on disk is wrong, no state is corrupted, the card DOES appear, and the sentence it carries is factually true — what fails is that a decision type whose entire purpose is human review gives the human no reason to act. IT IS NOT REVIEWER PROSE AND SO IT IS AN ID RATHER THAN A SLIP: the text is production output under `packages/`, rendered to a person in the inbox, which is exactly the product effect operator amendment amend0827 rule 2 reserves an id for. IT IS ALSO THE PREDICTABLE SECOND HALF OF `R-0710` AND THAT IS THE LESSON: a fix that widens a selection predicate must be read against every string the selected records then render, because the code downstream was written under the narrower predicate's assumption and is correct only under it. `R-0710`'s own fix clause asked for the predicate and a test and got both; it did not ask what the branch would SAY about the records it newly admitted, and no gate would have caught that, because every test it ordered asserts that a decision APPEARS rather than what it reads. FIX, in this same round: derive the summary's reason from BOTH fields the predicate reads, naming stale, flagged-for-review, or both as the case requires, rename the local list that no longer holds only stale cards, and pin all three cases on the RENDERED string. OPEN.
<<<END LEDGER5
