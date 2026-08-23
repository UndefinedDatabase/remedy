── STEP RECORD+INVENTORY — F022 R3 ──
Goal:        Record the F022 R2 verdict, repair the round map that R2 shifted
             without repairing it, and take the cost inventory by MEASURING the
             source. This round BUILDS NOTHING and MINTS NOTHING: no file under
             `apps/`, `packages/` or `tests/` is touched and no new finding id
             is created.

Fortschritt: ~0 % (T001 offen · T002 offen · T003 offen; R1 hat beansprucht, R2
             hat das R1-Verdikt auf Platte geschrieben, R3 raeumt die Rundenkarte
             auf und vermisst den Boden — gebaut wird ab R5) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the ledger, the
             map pair then the gate append · C3 context · C4 the cost inventory ·
             C5 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f022-r3.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/context.md` (C3) · `.agent/f022_inventory.md` (NEW, C4) ·
             `.agent/handoff.md` (C5).

Preface:     You are already on `feature/f022-live-cost-ticker`. THE ROUND BASE
             IS `66f87edc`, the R2 handback commit, and every base reading below
             is taken there. Create no branch. Run NO `gh pr create` and NO
             `gh pr merge`.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit because the plan must be current first (§3
    checklist item 23). C5 is the LAST commit and carries the handback. EVERY
    gate below runs after C4 and BEFORE C5, so the handback can quote all of
    them honestly (§3 checklist item 31); C5's own readings are owed to the next
    round's ledger entry and are not gated here.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `Done:`
    line and no `Landed:` line. The maximum registered id is `R-0669` at the
    round base and must still be `R-0669` at C4. R-0455 stays OPEN: GATE2
    records a recurrence of it, which is evidence added to an open finding and
    not a resolution.
 4. `.agent/live_review.md` AT C2 TAKES THE PAIR FIRST AND THE APPEND SECOND, in
    that order, so the append runs over a single-valued remainder (R-0639).
    Nothing else in that file is edited, reordered or deleted: §3 checklist item
    20 forbids rewriting landed finding text, which is why GATE2 carries the
    R-0455 recurrence as a dated entry of its own instead.
 5. PAIR SHAPE, MEASURED AND NOT ASSERTED. For STEPSF022 the containment test
    printed `TO contains FROM: false`, so the pair is a REWRITE and the §4.9
    rewrite obligation applies: FROM 0x and TO 1x in the target after C2.
 6. The whole-file replacements are PLANF022R3 at C1 and CONTEXTF022R3 at C3,
    each written as the slice plus exactly one terminating newline. STEPSF022 is
    the pair and GATE2 the append, and both land in C2 in the order constraint 4
    fixes.
 7. `.agent/f022_inventory.md` is YOUR OWN MEASUREMENT and carries no authored
    slice. Every row cites the `path:line` it was read at, and the file names the
    commit SHA every reading was taken at (§3 checklist item 20). It may NOT
    cite `docs/roadmap/features/T5_F022.md` as evidence for any row: that file
    states preconditions as settled fact and R-0612 is exactly that class.
 8. MEASURED DISAGREEMENTS ARE REPORTED, NEVER RECONCILED. Where a number below
    disagrees with what you measure, report BOTH and continue. Do not edit a
    slice and do not adjust your measurement to match mine.
 9. Block size, measured on these final bytes: TOTAL 294 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 191 against
    DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C5; the branch is `feature/f022-live-cost-ticker`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3
     and C4.
 G2  TRANSPORT: sha256 over `.agent/authored/f022-r3.md` at C0a, over
     `.agent/last_block.md` at C0b, over the source file this block was read
     from, and over the digest the delegation names are all equal. That digest is
     stated OUTSIDE this file, because a digest of these bytes cannot exist
     inside them (§3 checklist item 9). Write C0b FROM the committed C0a blob,
     never from the source a second time, and report the digest with the byte and
     line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two numerals
     from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R3 plus one terminating
     newline, proved against the slice extracted from the committed C0a blob,
     with a NEGATIVE CONTROL against the BARE slice which must DIFFER. Report
     both readings, plus `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` at most
     50.
 G5  THE LEDGER AT C2, UNDER TWO INDEPENDENT READERS. Reader (a), reconstruction:
     take the round-base blob of `.agent/live_review.md`, replace the STEPSF022
     FROM string with the TO string exactly once, then append one newline plus
     GATE2 plus one newline, and confirm the result is BYTE-EQUAL to the file at
     C2. Reader (b), an independent blank-line splitter: confirm the LAST unit
     equals GATE2 exactly, and report the unit count at the base and at C2.
     Report also the FROM string counted in `.agent/live_review.md` at the round
     base and at C2, and the TO string at C2. Then the NEGATIVE CONTROL, inside a
     disposable worktree under `.remedy-wt/f022r3-neg` and NEVER in the primary
     checkout: flip one printable byte at the START of the appended paragraph at
     unchanged length and confirm BOTH readers REJECT that mutant while ACCEPTING
     the true file. Remove the worktree and report `git worktree list` as a line
     count.
 G6  THE LEDGER SETS, line-anchored, at the round base then at C2: `^- R-\d+ — `
     and how many are DISTINCT; `^Done: R-`; `^Landed: `; `^Gate: R` and how many
     are DISTINCT; `^Gate: R2 `; and the MAXIMUM registered id. Report each at
     BOTH points, plus the set of ids added and the set removed. I measured the
     base as 230 entries all distinct, 0, 0, 2 distinct keys, 0 and `R-0669`.
 G7  `.agent/context.md` at C3 is byte-equal to CONTEXTF022R3 plus one
     terminating newline, with a NEGATIVE CONTROL against the BARE slice which
     must DIFFER. Report both readings, plus `wc -l`, and — because these are the
     contract readers' own assertions — that `## Active Branch` occurs once, that
     a `feature/` slug, the substring `Steps`, the substring `pytest` and the
     roadmap id `F022` are each present.
 G8  THE MAP LIVES IN ONE FILE. Count the literal `→` in `.agent/context.md` and
     in `.agent/plan.md` at the round base and again at C3, and count it in
     `.agent/live_review.md` at C2. Both of the first two must read 0 at C3. The
     base readings are ordered as the control, and they differ: I measured
     `.agent/context.md` at 3 and `.agent/plan.md` at 0, so context carries the
     duplicate map this round deletes while the plan never restated it.
 G9  THE COST INVENTORY at C4, `.agent/f022_inventory.md`, in three MEASURED
     sections. (a) Every call site of `evaluate_budget(` in this repository
     outside its own `def`, each with `path:line`, the enclosing symbol, and what
     that call does with the returned `BudgetEvaluation`. Report the count you
     measured; I measured 4 at the round base, one in
     `packages/orchestration/safe_points.py` and three in
     `apps/cli/commands/job.py`. (b) Every event-kind literal the ledger and SSE
     stream carry today, on the Python side and on the TypeScript side, each with
     the `path:line` that DEFINES it, and whether any kind whose name begins
     `budget` exists anywhere; I measured `RemedyTimelineEventKind` in
     `apps/ui/src/api/types.ts` as the three literals `llm_action`, `test` and
     `review`. (c) What `apps/ui/src/components/metrics/TopMetricsBar.tsx`
     renders today: each metric, the prop it reads, and the case-insensitive
     count of `cost`, `spent` and `usd` in that file; I measured 0 for all three
     at the round base. Report each count beside mine.
 G10 RANGE, executed after C4: the range from the round base to C4 lists exactly
     the paths of this block's `Change:` list other than `.agent/handoff.md`,
     with the set difference EMPTY in both directions, and 0 paths beginning
     `packages/`, `apps/` or `tests/`. Report the two set differences and that
     count. Then: every commit single-parent; `git show --numstat` and
     `git diff --numstat` agreeing cell by cell with the handback's own
     `## Commits` table for C0a through C4 (§3 checklist item 28), C5's row being
     owed to the next round's ledger entry; every insertion count under the 500
     cap; leading `<<<SLICE ` and `<<<END ` reading 0 LINES in `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/context.md` and `.agent/f022_inventory.md`;
     `git ls-files .remedy-wt` reading 0; and this round's reflog rows classified
     with `amend`, `rebase` and `cherry` each 0.
 G11 THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C4: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf`. Report the exit code and
     the passed-plus-skipped total. I measured this at `66f87edc` as exit 0 at
     528 passed.
 G12 CANARY, run serially after G11: `python3 -m pytest
     tests/cli/test_golden_path.py -q -rf`. Report the exit code and the total. I
     measured it at `66f87edc` as exit 0 at 42 passed. NO docs gate is ordered
     this round because no path under `docs/` is in the change set.
 G13 THE STANDING STALENESS GATE that R-0417 requires of every block and the R2
     block omitted, which is how the defect GATE2 records reached disk: for EACH
     file this round touched, re-read it end to end at C4 and report every
     sentence that states a count, a list of modules, a round map or a
     completion, together with whether it still holds at C4. Report the sentences
     you found; do NOT repair anything outside your slices, and declare any
     residual instead.
 G14 NO PULL REQUEST IS CREATED AND NONE IS MERGED. Report the output of
     `gh pr list --state open --json number,headRefName` and state that this
     round ran neither `gh pr create` nor `gh pr merge`.
 G15 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each commit of the
     `Bundle:` list, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), and this block's
     `Fortschritt:` line verbatim across all three of its lines. Its own `wc -l`
     is reported, and a DECISION D15 line declares any overage.

Handback:   completion report + rewrite `.agent/handoff.md`.

The slices follow. Each begins with a `<<<SLICE <name>` line and ends with a
`<<<END <name>` line; neither marker line is part of the slice, and no slice
includes a terminating newline unless a gate above says it does.

<<<SLICE PLANF022R3
# Plan — F022 Live cost ticker

Branch: feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge
commit of pull request #211. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
Money is visible while it burns, honestly: the MetricsBar's COST metric renders
from budget tick events {spent, limit, basis} — bar fill against the limit, a
'~' prefix plus tooltip whenever the basis is estimated, warn colour at ≥85% —
and the final figure reconciles with the ledger at terminal. DONE when the
ticker tracks a fixture stream exactly, basis changes flip the prefix and
tooltip live, the warn threshold triggers per tokens, limitless jobs render the
spent-only variant with no fake denominator, and the terminal reconciliation
displays the ledger figure with any delta labelled.

## Current Step
R3 records the R2 verdict, repairs the round map that R2 shifted without
repairing, and takes the cost inventory. The inventory MEASURES three things in
the source rather than reading them off the feature file: every call site that
evaluates spent-vs-limits, the event kinds the ledger stream carries today on
both the Python and the TypeScript side, and what the metrics bar renders now.
It mints no id and builds nothing.

## Next Steps
1. R4 record R3 and rule the tick envelope as a DECISION: the payload's field
   set, the basis vocabulary and the no-client-arithmetic contract.
2. R5 T001 the tick emission, at the evaluation sites the inventory names.
3. R6 T002 the COST metric, R7 T003 the terminal reconciliation, then the
   integration gate and closure.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- The feature file states its preconditions as settled fact, which is the R-0612
  class. The inventory measures them instead, and reports any disagreement.
<<<END PLANF022R3

<<<SLICE STEPSF022FROM
## Steps
R1 claim F022 in the roadmap ledger, create the branch, rescue the F021
decisions, reset this record carrying the F021 open set forward, gate F021 R41
and register the three candidates F021 carried plus R-0669 → R2 the cost
inventory: where the budget guard evaluates spent-vs-limits, what the Part E
event vocabulary defines and what MetricsBar renders today, each MEASURED in the
source → R3 record R2 and rule the tick envelope as a DECISION → R4 onward the
built work, in the T001/T002/T003 order the feature file's Task slicing names.
<<<END STEPSF022FROM

<<<SLICE STEPSF022TO
## Steps
R1 claim F022 in the roadmap ledger, create the branch, rescue the F021
decisions, reset this record carrying the F021 open set forward, gate F021 R41
and register the three candidates F021 carried plus R-0669 → R2 record the R1
verdict on disk → R3 record R2, repair this map, and take the cost inventory:
every call site that evaluates spent-vs-limits, the event kinds the ledger
stream carries today on both the Python and the TypeScript side, and what the
metrics bar renders now, each MEASURED in the source → R4 rule the tick envelope
as a DECISION → R5 T001 the tick emission → R6 T002 the COST metric → R7 T003
the terminal reconciliation and the delta labelling → R8 the integration gate →
R9 closure. This section is the only place the round map is stated, per
R-0447's remedy, and a round whose scope this map does not describe repairs the
map in that same block or is not emitted, per R-0455.
<<<END STEPSF022TO

<<<SLICE CONTEXTF022R3
# Context — F022 Live cost ticker

## Active Branch
feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge commit
of pull request #211 which closed F021.

## Scope
F022 only: the budget tick emission, the MetricsBar COST metric and the terminal
reconciliation. The roadmap feature file is
`docs/roadmap/features/T5_F022.md` and its Task slicing fixes the order.

## Do not touch
Budget enforcement, the pricing and basis rules, and MetricsBar's other metrics.
The feature file's own Do-not-touch section governs and is not narrowed here.

## Assumptions
- The UI never computes money. The backend is the single arithmetic home and the
  client's only arithmetic is the fill ratio.
- `budget.tick` is an ADDITIVE event kind in the Part E vocabulary; the SSE layer
  built by F008 carries it without change.
- No currency field is emitted unless a price basis exists, so no invented
  dollars reach the display.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- This is a UI feature, so `docs/ui/design_reference/` is binding and any visual
  deviation is documented with a technical reason.

## Steps
The round map lives in the `## Steps` section of `.agent/live_review.md` and is
stated there and nowhere else, per R-0447's remedy. This file names no round
numbers, so it cannot fall out of step with the map the way it did when R2 took
a scope the map did not describe.
<<<END CONTEXTF022R3

<<<SLICE GATE2
Gate: R2 — the F022 R2 entry. R2 PASSED ON EVERY GATE, AND THE REVIEWER RE-RAN EVERY ONE OF THEM INDEPENDENTLY RATHER THAN READING THE WORKER'S ARITHMETIC. TRANSPORT HELD IN ITS STRONGEST FORM, not the digest fallback: `.agent/authored/f022-r2.md` at `58224b09`, `.agent/last_block.md` at `6067feb3` and the working copy of that file are all sha256 `0bcf5d79c67bcd6f0faa5ff89c6ab1d7cbf4812ba32e097c1f727771926a96cf` over 16136 bytes and 165 lines, equal to the digest the R2 handback names. THE SLICE EXTRACTION out of the committed C0a blob printed 2 slices over 38 CONTENT lines, so constraint 6's numerals re-measure as 165 TOTAL against DECISION F085 D6's 490 and 127 PROSE against D5's 400. THE PLAN IS BYTE-EQUAL DISK TO DISK: `.agent/plan.md` at `0dcb9ea6` equals the PLANF022R2 slice plus exactly one terminating newline, the BARE-slice negative control DIFFERS, `^## Goal$` and `^## Next Steps$` occur once each, and `wc -l` is 37 under the 50-line cap AGENTS.md sets. THE APPEND HELD UNDER BOTH READERS AND UNDER A MUTANT: the round-base blob of `.agent/live_review.md` is a byte-exact PREFIX of the file at `66f87edc`; the remainder is 6356 bytes, exactly one newline plus GATE1's 6354 plus one newline; an independent blank-line splitter reads 251 units at `e62e8747` and 252 at `66f87edc` with the last equal to GATE1; and a one-byte flip at offset 470720, `G` to `H` at unchanged length, is REJECTED by both readers while both ACCEPT the true file. The reviewer ran that control in memory and wrote nothing to disk, so the primary checkout satisfied `git status --porcelain` empty throughout, which is stricter than the disposable worktree §4.10 permits. THE SETS ARE UNCHANGED WHERE THE ROUND PROMISED: 230 entries all DISTINCT at both points, `^Done: R-` 0, `^Landed: ` 0, maximum id `R-0669` at both, and the ids added and the ids removed are BOTH the empty set, while `^Gate: R` moves 1 to 2 with the distinct keys `Gate: R41` then `Gate: R41` and `Gate: R1`. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the four state readers exit 0 at 528 passed, and the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed. STRUCTURE HELD: four commits over `e62e8747`..`66f87edc`, every one single-parent, insertions 165, 96, 7 and 41, each under the 500 cap; the range path set EQUAL to the block's declared set with the difference empty in both directions and 0 paths beginning `packages/`, `apps/` or `tests/`; `git show --numstat` agreeing cell by cell with the handback's `## Commits` table, the `.agent/handoff.md` cell excepted as self-reference under R-0149; `^<<<SLICE ` and `^<<<END ` reading 0 in both slice targets; `git ls-files .remedy-wt` 0; one worktree; and the round's reflog rows carrying four `commit` operations with 0 amend, 0 rebase and 0 cherry. GATE1'S CONTENT WAS AUDITED RATHER THAN TRUSTED, because a shape gate never fails on a false sentence (R-0561), and every claim in it that the reviewer could re-derive from disk did re-derive: the R1 transport digest `e07ad805e616fd573108041da87c341115e79b598df6c057fdbf411aa9f730a3` over 35426 bytes and 419 lines reproduces at `6e39b9c0`, at `23bf7ef5` and on disk at `.remedy-wt/f022-r1.md`; the reset digest `0486c83d92c850852f79680086c09798d0be47ea2bb0e649543b8fa912f097ba` reproduces at `3c5b3f26`; the insertion list 419, 392, 26, 31, 10, 38, 4 and 69 reproduces commit for commit over the eight single-parent commits of `c34ef32b`..`e62e8747`; the roadmap counts reproduce as 0 then 1, 0 then 1, 1 then 0 and 56 at both; and GATE1's own dated correction reproduces exactly, the `Recurrence:` paragraphs reading 16 at `c34ef32b` and 2 at `3c5b3f26` under a line-anchored and an indent-agnostic count alike. THE ROUND'S ONE DECLARED DEVIATION IS ACCEPTED for the reason R1's was: G7, G8 and G9 were measured against the C2 tree immediately before C2 and re-run after it with identical results, because their numbers are mandated content of the handback C2 itself carries, and `.agent/handoff.md` was the only file differing between the two runs while no suite in either gate reads it. R3's own block removes that necessity by ordering every gate at a commit strictly earlier than the handback commit, which is what §3 checklist item 31 asks for. RECURRENCE OF R-0455, dated 2026-08-23, recorded here rather than under a new id because §3 checklist item 30 requires the open set searched for the DEFECT before an id is minted and R-0455 already holds this one. R-0455's standing rule reads that a block giving its round a scope the map does not describe repairs the map in that same block or is not emitted, and the R2 block was emitted anyway. The map in this file's `## Steps` section said the cost inventory was R2; R2 instead recorded the R1 verdict, which shifted every later round by one; and the R2 block rewrote `.agent/plan.md` to the shifted numbering while repairing neither this map nor `.agent/context.md`, whose own step list still named the unshifted rounds. Measured at `66f87edc`: this file's map and `.agent/context.md` both said the cost inventory was R2 while `.agent/plan.md` said it was R3, so the file AGENTS.md Session Resume tells the next session to read SECOND contradicted the single source R-0447's remedy designated. THE DEFECT IS THE REVIEWER'S AND NOT THE WORKER'S, twice over: the R2 block's change set already named this file, so the map repair was available inside it and was simply not ordered, and `.agent/context.md` lay outside that change set so no honest worker could have touched it. The second half is the class rather than the instance: the R2 block carried no standing staleness gate at all, and R-0417's counter-measure — every block's gate list carries one, for each file the round touched — is precisely the gate that would have surfaced both files. R3 repairs both, this file's map in its STEPS pair and `.agent/context.md` by DELETING its duplicate map rather than re-syncing it, which applies R-0447's remedy instead of restating it, and R3's own gate list carries the staleness gate again. R-0455 STAYS OPEN until that repair is reviewed. THE VERDICT IS PASS: every numeral R2 states reproduced under the reviewer's own measurement, the worker applied both slices byte for byte, declared its one deviation before the reviewer read the diff, minted nothing and resolved nothing, and the single defect the round leaves on disk was authored by the reviewer rather than executed by the worker.
<<<END GATE2
