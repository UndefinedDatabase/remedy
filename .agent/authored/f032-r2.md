STEP R2 / F032 — APPROVAL WITH THE EVIDENCE TRIPLE
Goal:        RULE THE SPEC ONTO DISK. R1's inventory measured three things the
             feature file's Design assumes and the source does not have: there
             is no enqueue seam, there is no typed provenance vocabulary, and
             six of the eight producing branches have no options list to key a
             per-option outcome to. This round books R1's verdict, registers
             the one defect with product effect that the inventory found, and
             settles all three conflicts as DECISION F032 D1, D2 and D3 in
             `.agent/decisions.md` AND as a `## Design amendments` section in
             the feature file, so T001 is specified against the source rather
             than against a suggestion. NO PRODUCTION CODE IS WRITTEN THIS
             ROUND. YOU CREATE NO PULL REQUEST AND YOU MERGE NOTHING.
Bundle:      C0a save this block · C0b mirror it into `last_block` · C1 the
             plan · C2 the ledger append · C3 the decisions append · C4 the
             feature-file design amendments · C5 the handback · then push.
Change:      Exactly these paths, nothing else. `.agent/authored/f032-r2.md`,
             `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/decisions.md`, `docs/roadmap/features/T5_F032.md`,
             `.agent/handoff.md`. This list bounds what you WRITE INTO THE
             REPOSITORY. It does NOT bound what you DO: G8 orders a push.
             NOTHING under `apps/`, `packages/` or `tests/` is written, and
             under `docs/` ONLY `docs/roadmap/features/T5_F032.md`.
             `.agent/context.md` is NOT rewritten this round — it is accurate
             as it stands and an unbidden rewrite is exactly the churn the
             amend0827 order exists to cut.

Constraints:
 1. THIS BLOCK REACHES YOU AS A FILE, NOT AS PROSE IN A PROMPT. Read
    `.remedy-wt/f032-r2.md` from disk and copy it BYTE FOR BYTE to
    `.agent/authored/f032-r2.md` — with `shutil.copyfile` or a read-then-write
    in python, never by retyping it and never with `cp`, which this session's
    guard rejects. This block asserts NO digest of its own, because a digest
    written inside the text it measures cannot be true; G2 has you measure four
    points and prove them EQUAL, and the reviewer holds the scratch value
    independently.
 2. EVERY SLICE IS APPLIED BYTE FOR BYTE. Never retype one, never reflow one,
    never fix one. A slice's text is its content lines joined with a newline
    plus ONE trailing newline. If a slice contradicts something you measure,
    apply it anyway and DECLARE the contradiction in the handback under
    Deviations — a corrected slice destroys the transport proof. Declaring
    beats fixing every time, because a declared contradiction reaches a
    reviewer who can measure it while a silent fix reaches nobody.
 3. THE COMMIT ORDER IS FIXED: C0a, C0b, C1, C2, C3, C4, C5. Every sentence in
    GATE1 and in the DECISION texts that describes THIS round's own landed
    change depends on that order, and this constraint is what fixes it.
 4. C0a AND C0b LAND WHILE `.agent/plan.md` STILL DESCRIBES R1. That is
    ordered: the plan becomes current at C1, the FIRST substantive commit.
 5. ALL THREE APPENDS ARE APPENDS AND NOTHING IS EDITED OUT.
    `.agent/live_review.md`, `.agent/decisions.md` and
    `docs/roadmap/features/T5_F032.md` each end this round as their own
    pre-commit blob, byte for byte, plus ONE newline, plus the slice. No
    existing paragraph, heading, finding, `Done:` line or `Gate:` line in any
    of the three is rewritten, deleted, renumbered or touched. An append-only
    record is corrected by appending.
 6. EVERY SLICE IS THE REVIEWER'S TEXT. You never write a `Gate:` paragraph of
    your own, never mint a finding id and never author a `Done:` line. LEDGER2
    carries this round's gate entry and ONE newly minted finding. NO FINDING IS
    RESOLVED THIS ROUND. If you find a further defect, report it in the
    handback under Deviations and let the reviewer rule on it.
 7. THE LEDGER SETS MOVE AS FOLLOWS ACROSS C2. `^Gate: F\d+ R\d+ — ` moves 53
    to 54 with the ADDED key exactly `F032 R1`. `^- R-\d+ — ` moves 270 to 271
    with the ADDED id exactly `R-0710`. `^Done: R-\d+ — ` stays 21,
    `^Landed: R-` stays 0 and `^Gate: R\d+ — ` stays 19. The open set is 249
    before C2 and 250 after C2; the maximum id is `R-0709` before and `R-0710`
    after.
 8. RE-READ `.agent/STOP` FROM DISK before C0a and again before C5. If it
    exists at either reading, finish the commit in hand, write the handback and
    STOP.
 9. NOTHING DESTRUCTIVE IS ORDERED THIS ROUND. Create no worktree. The primary
    checkout reads `git status --porcelain` 0 lines at every commit.
10. THIS SESSION'S COMMAND GUARD rejects shell loops, `$?`, `$( )` inside a
    compound, `${...}` and every other expansion, `cp`, brace literals
    containing a quote character, `cd x && y`, file redirects, and every form
    of environment assignment. Route anything that counts, hashes or compares
    through a quoted python heredoc, read real exit codes from
    `subprocess.run(...).returncode`, and pass `cwd=` rather than `cd`. Run
    pytest SERIALLY — never two pytest processes alive at once. `--timeout` IS
    NOT AVAILABLE to pytest here: passing it exits 4 and reports no failure.
11. EVERY NUMERAL THIS BLOCK STATES ABOUT THE ROUND BASE `d3160d00` was
    measured by the reviewer at that commit. It is a REFERENCE to report
    against, NOT a target to reproduce. Where your measurement differs, report
    BOTH and reconcile NOTHING.
12. THERE ARE NO FROM/TO REPLACEMENT PAIRS IN THIS BLOCK. Every slice other
    than PLANF032R2 is an APPEND, and PLANF032R2 is a whole-file replacement of
    `.agent/plan.md`. No slice carries a FROM-zero obligation, and none is to
    be searched for as a FROM anywhere.
13. YOUR HANDBACK CARRIES A `## Session` SECTION reading that this is SESSION 1
    of F032 and that R2 is the round. The handback has NO LENGTH CAP — operator
    amendment amend0827 rule 3 withdrew every tier — so do not declare, measure
    or apologise for its length. It is VALID when its mandated sections are
    present, and DROPPING one is the finding the cap used to stand in for.

Done when:
 G1. HYGIENE, THE BRANCH AND THE SENTINEL. Report `git rev-parse HEAD` before
     C0a, which must be `d3160d000f1f43b3fe584485121cc45b96c2bdb6`, and
     `git branch --show-current`, which must be `feature/f032-evidence-triple`.
     Report `git status --porcelain` as a LINE COUNT after each of C0a, C0b,
     C1, C2, C3, C4 and C5, each 0. Report `.agent/STOP` read from disk before
     C0a and before C5, both ABSENT.
 G2. TRANSPORT. Report the sha256, byte count and line count of this block as
     read from `.remedy-wt/f032-r2.md`, as saved at C0a, as mirrored at C0b and
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
 G4. THE PLAN. `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF032R2 under the
     newline-INCLUDED convention. Run the negative control against the slice
     MINUS its trailing newline and report it FALSE. Report `^## Goal$` 1,
     `^## Next Steps$` 1, a match for `\bF\d{3}\b`, and `wc -l` STRICTLY UNDER
     50.
 G5. THE LEDGER APPEND, PROVED TWICE, THE SECOND READER COVERING THE WHOLE
     APPENDED REGION. `.agent/live_review.md` at C2 equals its pre-commit blob
     plus ONE newline plus LEDGER2. The reviewer measured that base blob at
     `d3160d00`: 1025611 bytes over 410 blank-line units. If it reads
     differently before C2, something moved this round did not order — stop and
     hand back. Report both byte counts and the sum. Then the SECOND,
     INDEPENDENT reader: split the whole file on blank lines, let N be the
     number of paragraphs YOUR SCRIPT COUNTS in that slice — never a number
     this block asserts — and compare the LAST N units against the slice's N
     paragraphs IN ORDER. Report N and the unit count before and after. THE
     NEGATIVE CONTROL GOES ON THE FIRST APPENDED PARAGRAPH, AT A BYTE OFFSET,
     NOT A CHARACTER OFFSET — the file carries multi-byte em dashes and a
     character offset lands outside the appended region where the control
     proves nothing. Flip ONE byte IN MEMORY and report that BOTH readers
     REJECT it. Never mutate the tracked file. Then report, at two points,
     before C2 and after C2, the line-anchored counts of `^- R-\d+ — `,
     `^Done: R-\d+ — `, `^Landed: R-`, `^Gate: R\d+ — ` and
     `^Gate: F\d+ R\d+ — `, the finding ids and the resolved ids ADDED and
     REMOVED as SETS, whether all ids are DISTINCT, the maximum id at each
     point, and the open set at each point. Every movement constraint 7 names
     is checked here, INCLUDING the ones that must NOT move.
 G6. THE DECISIONS APPEND AND THE FEATURE-FILE APPEND, each proved the same
     way. `.agent/decisions.md` at C3 equals its pre-commit blob plus ONE
     newline plus DECISIONS2, and `docs/roadmap/features/T5_F032.md` at C4
     equals its pre-commit blob plus ONE newline plus FEATAMEND. The reviewer
     measured those base blobs at `d3160d00` as 626914 bytes and 4980 bytes.
     For EACH of the two: report both byte counts and the sum, and report that
     the file at its commit STARTS WITH its pre-commit blob as a byte PREFIX.
     Report the line-anchored count of `^## DECISION F032 D\d+ ` in
     `.agent/decisions.md` at both points, which must move 0 to 3 with the
     ADDED keys as a SET being exactly `## DECISION F032 D1`,
     `## DECISION F032 D2` and `## DECISION F032 D3`, and the count of
     `^## DECISION ` overall, which must move 158 to 161. Report the
     line-anchored count of `^## Design amendments$` in the feature file at
     both points, which must move 0 to 1, and confirm that the line
     `## Do not touch` still occurs exactly once there after C4.
 G7. THE SUITES, run AFTER C4 and BEFORE C5, SERIALLY, never two pytest
     processes alive at once. FIRST, because this round writes
     `docs/roadmap/**`: `python3 -m pytest tests/docs/
     tests/orchestration/test_roadmap_index.py -q` from the repository root;
     the reviewer measured `325 passed` at a REAL exit 0 at the round base.
     SECOND, because this round rewrites `.agent/` state, the four state
     readers and the canary: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py
     -q`; the reviewer measured `620 passed` at a REAL exit 0 at the round
     base. For EACH run report the REAL exit code, the summary line VERBATIM,
     and the COUNT of lines matching `^FAILED`. PROVE YOUR `^FAILED` EXTRACTOR
     IS NOT BLIND by running it over a string you know contains such a line and
     reporting that it matched. IF EITHER RUN IS RED, report the failing node
     ids VERBATIM and hand back.
 G8. STRUCTURE, ARTIFACTS, THE OPEN PR GATE AND THE PUSH. Compare the path set
     of `git diff --name-only d3160d00..C4` BOTH WAYS against this round's
     expected set — the Change line's list MINUS `.agent/handoff.md`, which C5
     writes — and report both residues EMPTY. Report `git diff --stat
     d3160d00..C4` restricted to `apps/`, `packages/` and `tests/` and confirm
     each EMPTY. Report each commit's insertions from `git diff --numstat` for
     C0a through C4, confirm each single-parent and under 500. Line-anchored
     `^<<<SLICE ` and `^<<<END ` are 0 and 0 in `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md` and
     `docs/roadmap/features/T5_F032.md` at their commits, against a CONTROL
     over the C0a blob which is not 0. Report `git ls-files .remedy-wt` 0
     lines, `git worktree list` 1 line, and `git branch --list "tmp/*"` 0
     lines. Run `gh pr list --state open --json
     number,headRefName,baseRefName,isDraft` and report it VERBATIM; the
     reviewer read `[]` at the round base; MERGE NOTHING and CREATE NOTHING.
     After C5, run `git push origin feature/f032-evidence-triple`. ITS OUTCOME
     IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: C5 is authored before the
     push exists, so `.agent/handoff.md` states the push only as an INTENT
     under `## External actions`, with NO exit code and NO remote tip. Report
     the real exit code and the resulting remote tip in your completion report
     instead.
Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md at
             C5: the `## Session` section constraint 13 orders, feature and
             round, branch, the round base SHA `d3160d00`, the per-commit
             changed-files table with the `+/-` column taken from `git diff
             --numstat` ITSELF and agreeing cell for cell with G8, an
             item-status row for EVERY Bundle item, ONE LINE PER GATE for G1
             through G8 with its real exit code, the open-findings count after
             this round, and the next expected action. C5 cannot table its own
             numstat — write `self` in that cell, as `R-0149` requires, and put
             C5's own numbers nowhere.
             ANY COMMIT YOU MAKE BEYOND THE ORDERED SEQUENCE RECEIVES ITS OWN
             `## Commits` ROW AND ITS OWN ITEM-STATUS ROW, and the Deviations
             section says so in those same words.

<<<SLICE PLANF032R2
# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 from D1.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and, from this round, the design amendments that reconcile it
with the source.

## Current Step
R2 books R1's verdict and the one defect with product effect that R1's
inventory found, and rules the three conflicts between the feature file's
suggested Design and the measured source: there is no enqueue seam, there is no
typed provenance vocabulary, and six of the eight producing branches carry no
options list. Each is settled as a DECISION and written into the feature file
so T001 is specified against what the source has.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 gate F032 R1 and register R-0710 | ordered | one finding, none resolved |
| C3 DECISION F032 D1, D2 and D3 | ordered | the three spec conflicts |
| C4 feature-file design amendments | ordered | the same three, where a
  builder reads them |
| C5 the handback | ordered | |

## Next Steps
1. T001a: the evidence-triple schema and the emit gate at the derivation
   point D1 names, with the guards R1's inventory Q8 lists red-proved.
2. T001b: legacy rendering for records without a triple, and the CI canary
   that a tripleless producer must fail.
3. T002 the per-producer upgrades, then T003 card enrichment and chip links.

## Risks
- D2 builds a minimal ref type inside F032 rather than waiting for F066, which
  is unclaimed. If F066 later lands a different vocabulary, the reversal is
  named in D2 and is a rename, not a redesign.
- The open set stands at 250 after this round. None of it blocks F032.
<<<END PLANF032R2

<<<SLICE LEDGER2
Gate: F032 R1 — the F032 CLAIM AND INVENTORY entry. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran every one of them itself. TRANSPORT HELD AT FOUR POINTS: the scratch original `.remedy-wt/f032-r1.md`, the C0a blob, the C0b blob and the working copy are ALL sha256 `ae44bcac6839ea2ec4d0242d3d18a54edf7f6b12dcac7d57407d4123d9e01b59` over 25032 bytes and 404 lines, with C0a and C0b the SAME git blob `dc9584b3f222`, and no line of the block a run of a single repeated character at length 4 or more. THE REVIEWER HELD THAT DIGEST BEFORE DELEGATING, so the chain is closed at both ends rather than only at the worker's; THAT PROOF COVERS THE SCRATCH FILE, THE SAVED COPY, ITS MIRROR AND THE WORKING COPY, AND NOT THE BYTES OF ANY PROMPT, because under self-drive no gate this workflow can run reaches the emitted bytes. EXTRACTION re-measured from the committed C0a blob printed 6 slices at 46, 53, 24, 26, 1 and 1 content lines, CONTENT 151, TOTAL 404 and PROSE 253, both caps met. THE PLAN AND THE CONTEXT at C1 are byte-equal to PLANF032R1 and CTXF032R1 at 2275 and 2772 bytes, both minus-newline controls FALSE, with `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` 46 in the plan and `^## Active Branch$` 1, a `feature/` slug, an F-id and the word `Steps` present in the context. THE LEDGER RESET IS PROVED BY WHAT IT DID NOT TOUCH: LFROM occurs 1 time before C3 and 0 after, LTO 0 before and 1 after, and the whole region from the first byte of `## Findings` to end of file is 1023923 bytes at sha256 `3c0dac3dd2b4a9292722f0ec94598b9aa4c34e0ba255a28aaf896865699081d1` at BOTH points, byte-identical — the append-only half of the record was carried across a header rewrite untouched. THE SETS DID NOT MOVE AT ALL, as ordered: `^- R-\d+ — ` 270, `^Done: R-\d+ — ` 21, `^Landed: R-` 0, `^Gate: R\d+ — ` 19 and `^Gate: F\d+ R\d+ — ` 53 at both points, ids ADDED and REMOVED both EMPTY in both series, all ids DISTINCT, maximum `R-0709`, and the open set 249 before and 249 after. THE CLAIM LANDED: `docs/roadmap/STATUS.md` moved `^- \[ \] ` 197 to 196, `^- \[x\] ` 58 to 58 and `^- \[~\] ` 0 to 1 with the total `^- \[` unchanged at 255, so exactly one line changed state and no line was added or lost. THE SUITES ARE GREEN AND THE REVIEWER RE-RAN BOTH SERIALLY at `d3160d00`: `tests/docs/` with `tests/orchestration/test_roadmap_index.py` at `325 passed` and the four state readers with the canary at `620 passed`, each a REAL exit 0 with zero `^FAILED` lines, every count EQUAL to the worker's. NOTHING ELSE MOVED: both path residues EMPTY over the seven-path set, `apps/`, `packages/` and `tests/` each EMPTY and `docs/` holding `docs/roadmap/STATUS.md` alone, insertions 404, 337, 63, 1, 23 and 369, each single-parent and under 500, markers 0 and 0 in all three written state files against a CONTROL of 6 and 6 over the C0a blob, `.remedy-wt` 0 tracked lines, the worktree listing 1 line, no `tmp/*` branch, the Open PR Gate read and NOT acted on at `[]`, and the reflog carrying only `commit`, `checkout` and `pull --ff-only` operations, so no history was rewritten. NOW THE ROUND'S REAL SUBSTANCE, WHICH IS WHY THIS IS NOT A BOOKKEEPING ENTRY. `.agent/f032_inventory.md` answers Q1 through Q8 with 369 lines of cited measurement, and the reviewer verified its load-bearing claims independently rather than accepting them: `HumanDecision(` occurs 9 times in the entire repository outside `tests/`, ALL of them inside `decision_queue.list_decisions` between lines 62 and 376, which is the measurement behind Q1's answer that NO ENQUEUE SEAM EXISTS; `grep -rn "resolve_ref\|ProvenanceRef\|REF_KIND\|ref_kind" packages/ apps/` returns ZERO lines, which is Q4's answer that the typed provenance vocabulary the feature file leans on IS NOT BUILT, and `docs/roadmap/STATUS.md:136` carries `- [ ] F066 — Idea provenance` unclaimed; and six spot-checked citations — `approval_queue.py:129`, `stop_reasons.py:187`, `escalation.py:54`, `:57` and `:211`, `flight_plan.py:787`, `local_gateway.py:177` and `:331`, `decision_queue.py:62` and `:202` — each resolve to exactly the symbol the inventory names, so nothing in it is fabricated. THE INVENTORY IS ALSO HONEST ABOUT WHAT IT COULD NOT DO, which is the property that makes the rest usable: it declares that `rg` is absent and names the `grep -rlE` it substituted, that no vitest ran so its 53 `it(` cases are a source count rather than collected tests, and that no test was run against a mutated schema so every Q8 "would turn red" is read from assertion text rather than observed — an obligation it hands forward to T001 in those words. ONE DEFECT WITH PRODUCT EFFECT WAS FOUND AND IS REGISTERED BELOW AS `R-0710`; the worker measured it, declined to fix it under constraint 7 and reported it, which is the split-role model working as designed. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

- R-0710 — Medium — half of the memory-review predicate can never match, so memory cards flagged for review never reach the decision queue. `packages/orchestration/decision_queue.py:223` selects the cards branch 6 turns into `memory_review` decisions with `stale = [e for e in entries if e.validity in ("stale", "needs_review")]`. But `validity` is `Literal["active", "stale", "superseded", "contradicted"]` at `packages/memory/models.py:44`, and `"needs_review"` is a value of the SEPARATE field `review_status`, `Literal["proposed", "approved", "rejected", "needs_review"]` at `packages/memory/models.py:45`. The two fields were conflated, so `e.validity == "needs_review"` is false for every `MemoryEntry` that can exist and the second half of the predicate is dead. The branch is not wholly dead — `"stale"` is a real validity, set by `local_gateway.mark_stale` at `packages/memory/local_gateway.py:331` — which is exactly why this survived: the decision type produces cards, just never the ones a human explicitly flagged for review, and no test distinguishes the two halves. Measured by the R1 worker while answering inventory Q1 and re-measured by the reviewer at `d3160d00`; it is registered rather than fixed because R1's change set wrote nothing under `packages/` and constraint 7 forbade the worker to mint an id or repair. SEVERITY IS MEDIUM AND NOT LOW because the loss is silent and lands on the one decision type whose whole purpose is human review: a card marked `needs_review` is invisible to `remedy decision list`, to the inbox and to the dashboard, and the reviewer confirmed no test asserts either half of the predicate. IT IS ALSO NOT F032's TO FIX INCIDENTALLY: the correct repair is a one-line predicate change plus a test that pins BOTH halves, and F032 touches `decision_queue.py` in T001 anyway, so the fix belongs to the first T001 commit that opens that file — a `while I am here` edit in a round with no test for it is what AGENTS.md Scope Control forbids. FIX, binding on the T001 round that first edits `packages/orchestration/decision_queue.py`: select on `e.validity == "stale" or e.review_status == "needs_review"`, or state in a one-line WHY comment above the predicate that only `stale` is intended and drop the dead half, and pin whichever is chosen with a test that goes red when either half is removed. OPEN.
<<<END LEDGER2

<<<SLICE DECISIONS2
## DECISION F032 D1 (2026-08-27) — the triple is enforced at the DERIVATION point, because no enqueue seam exists

THE QUESTION. `docs/roadmap/features/T5_F032.md:31-33` names the enforcement
point as "the enqueue seam every producer already funnels through (one gate)".
R1's inventory measured that seam and it does not exist. All nine
`HumanDecision(...)` constructions in the repository outside `tests/` sit inside
`packages/orchestration/decision_queue.py::list_decisions` (function at `:62`),
which is a read-only derivation — its own module docstring says so at `:4-6`.
The eight producing branches derive from sixteen distinct record-creation sites
across twelve modules, and only branch 8 has an enqueue-shaped function,
`escalation.enqueue_task_decision` at `escalation.py:211`, serving that one
branch. There is nothing to gate on the way IN, because nothing is created.

CHOSEN: THE GATE SITS AT `list_decisions`, WHICH IS THE EMIT POINT. It is the
one function every decision passes through, and a decision that reaches a human
without a triple is precisely what the feature exists to prevent — so refusing
to EMIT is the property F032 actually wants, and refusing to CREATE was only
ever a means to it. `evidence_refs`, `expected_outcome` and `downside` become
required of every card the function yields, and the canary is a producing
branch that omits one and is caught there.

ALTERNATIVES CONSIDERED. Building an enqueue seam first, by routing all sixteen
creation sites through one constructor: rejected as a refactor of twelve modules
that F032 neither needs nor is scoped for, and one that AGENTS.md's own
churn-is-the-enemy rule argues against. Gating at each of the sixteen sites:
rejected because it multiplies the guard by sixteen and still cannot see a
decision that is derived rather than created.

CONSEQUENCE FOR THE FEATURE FILE'S DO-NOT-TOUCH LIST: "queue storage" names
nothing — inventory Q3 measured that no decision store exists — so that item is
vacuous rather than restrictive, and D2 settles the third name on that list.

REVERSE by deleting this decision and the `## Design amendments` entry that
mirrors it, and restoring the enqueue reading of the feature file.

## DECISION F032 D2 (2026-08-27) — F032 defines its own minimal evidence ref and does NOT wait for F066

THE QUESTION. The feature file says refs "use the typed provenance vocabulary
(file/failure/decision kinds cover the current producers; the resolver's badges
render on the chips)" and its Do-not-touch list names the "provenance resolver".
Inventory Q4 measured that neither exists: `grep -rn
"resolve_ref\|ProvenanceRef\|REF_KIND\|ref_kind" packages/ apps/` returns zero
lines. Both are the unbuilt spec `docs/roadmap/features/T3_F066.md:24-40`, and
F066 is unclaimed at `docs/roadmap/STATUS.md:136`, as is its own dependency
F063 at `:133`. F032's header declares a dependency on F031 alone.

CHOSEN: F032 DEFINES THE SMALLEST REF IT NEEDS AND SHIPS NO RESOLVER. A ref
carries a kind, a target and a label, with the kind vocabulary held as a real
constant rather than a comment — the failure mode both nearest precedents share,
`ProviderVerificationEvidenceRef` at `provider_trust_verification.py:171-177`
and `OrchestratorEvidenceRef` at `orchestrator_brain.py:87-95`, each of which
states its vocabulary only in a comment. No badge is rendered, because a badge
without a resolver would be a false live indicator; the chips render the label
and the kind, and F066 supplies resolution when it lands.

ALTERNATIVES CONSIDERED. Blocking F032 until F066 is built: rejected because
F066 is not this feature's declared dependency and is not claimable ahead of
F063, so blocking would stall a tier on an undeclared chain. Untyped strings:
rejected because the whole point is that a ref be clickable later, and an
untyped string cannot be resolved without re-parsing.

REVERSE by deleting this decision and blocking F032 on F066. When F066 lands,
the migration is a rename of this feature's kind constant onto F066's, which is
why the constant is named in one place.

## DECISION F032 D3 (2026-08-27) — the triple is per option only where options exist, and F032 grows no options list

THE QUESTION. `docs/roadmap/features/T5_F032.md:43-45` specifies
`expected_outcome: str per option` and `downside: str per option`, "keyed to the
options list — outcomes are per-choice, that's the point". Inventory Q5
measured that only two of the eight producing branches have an options list at
all: branch 7's pending arm, `payload["options"] = ["approve", "reject"]` at
`decision_queue.py:288`, and branch 8, which forwards the escalation record's
own `options` at `:365`. The other six carry only `next_actions`, which are
shell commands and prose, not choices. For six of eight, "per option" is
undefined.

CHOSEN: THE TRIPLE IS KEYED PER OPTION WHERE AN OPTIONS LIST EXISTS AND CARRIES
EXACTLY ONE UNKEYED PAIR WHERE NONE DOES. A decision with options gets one
`expected_outcome` and one `downside` per option; a decision without gets one of
each for the decision as a whole, which is the honest reading of "what happens
next" when the human is not being offered a choice. GIVING THE OTHER SIX
BRANCHES AN OPTIONS LIST IS EXPLICITLY OUT OF F032's SCOPE — it changes what
those decisions ARE, not what evidence they carry, and it belongs to the
features that own them.

ALTERNATIVES CONSIDERED. Growing options lists for all eight branches first:
rejected as a behaviour change to six subsystems smuggled in under a
documentation-shaped feature. Treating `next_actions` as the options list:
rejected because inventory Q5 measured that
`apps/ui/src/api/decisionCard.ts::decisionAnswers` at `:223` already falls back
from `payload.options` to `next_actions`, so keying outcomes to commands would
attach a consequence sentence to a shell invocation and read as though running
it were the choice.

ONE THING THIS DECISION DOES NOT SETTLE, recorded so T002 does not rediscover
it: inventory Q2 measured that branch 8 drops the escalation record's `impact`
field at `escalation.py:242` when deriving the card, and that field is the
nearest thing to an `expected_outcome` already on disk. Whether T002 forwards it
or writes a new one per producer is a T002 question, not a schema question.

REVERSE by deleting this decision and requiring an options list of every
producing branch as part of F032.
<<<END DECISIONS2

<<<SLICE FEATAMEND
## Design amendments

> Added 2026-08-27 at F032 R2, after the R1 source inventory
> (`.agent/f032_inventory.md`) measured three assumptions in the Design and
> Task-slicing sections above that the source does not meet. The sections above
> are left as written — this file records how the design MOVED, and the
> amendments below win where they conflict with it. Full reasoning, alternatives
> and reversal instructions: `.agent/decisions.md`, DECISION F032 D1, D2 and D3.

**A1 — the enforcement point is the DERIVATION point, not an enqueue seam
(DECISION F032 D1).** "The enqueue seam every producer already funnels through"
does not exist. All nine `HumanDecision(...)` constructions outside `tests/` sit
inside `packages/orchestration/decision_queue.py::list_decisions`, a read-only
derivation over sixteen record-creation sites in twelve modules; only branch 8
has an enqueue-shaped function. The gate therefore refuses to EMIT a tripleless
decision at `list_decisions`, which is the one function every decision passes
through. The Do-not-touch entry "queue storage" names nothing: there is no
decision store.

**A2 — F032 defines its own minimal evidence ref and ships no resolver
(DECISION F032 D2).** The typed provenance vocabulary and the resolver this file
leans on are the UNBUILT spec `docs/roadmap/features/T3_F066.md:24-40`; F066 is
unclaimed and so is its dependency F063. A ref carries kind, target and label,
with the kind vocabulary as a real constant. No staleness badge is rendered,
because a badge with no resolver behind it is a false live indicator. The
Do-not-touch entry "provenance resolver" is therefore vacuous for now, and F066
supplies resolution when it lands.

**A3 — per option only where options exist (DECISION F032 D3).** Only two of the
eight producing branches carry an options list. A decision with options gets one
`expected_outcome` and one `downside` per option; a decision without gets one
unkeyed pair for the decision as a whole. Growing options lists for the other six
branches is OUT of F032's scope and belongs to the features that own them.

**Carried forward for T002, not a schema question:** branch 8 drops the
escalation record's `impact` field when deriving its card, and that field is the
nearest thing to an `expected_outcome` already on disk.
<<<END FEATAMEND
