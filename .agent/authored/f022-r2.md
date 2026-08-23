── STEP RECORD — F022 R2 ──
Goal:        Record the F022 R1 verdict in the review record, carrying the
             reviewer's own correction to a sentence R1 landed, and point the
             plan at R3. This round BUILDS NOTHING and MINTS NOTHING: no file
             under `apps/`, `packages/` or `tests/` is touched and no new
             finding id is created.

Fortschritt: ~0 % (T001 offen · T002 offen · T003 offen; R1 hat das Feature
             beansprucht und das Record zurueckgesetzt, diese Runde schreibt nur
             das R1-Verdikt auf Platte — gebaut wird ab R4) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the ledger
             append.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f022-r2.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` and
             `.agent/handoff.md` (BOTH in C2).

Preface:     You are already on `feature/f022-live-cost-ticker`. THE ROUND BASE
             IS `e62e8747`, the R1 handback commit, and every base reading below
             is taken there. Create no branch. Run NO `gh pr create` and NO
             `gh pr merge`.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2 and is not negotiable. C1 precedes C2
    because the plan must be current before the ledger commit (§3 checklist
    item 23). C2 is the LAST commit and carries the handback.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `Done:`
    line and no `Landed:` line. The maximum registered id is `R-0669` at the
    round base and must still be `R-0669` at C2.
 4. `.agent/live_review.md` IS APPEND-ONLY THIS ROUND. The base blob must be a
    byte-exact PREFIX of the C2 file. GATE1 is appended as a single paragraph,
    separated from the existing last paragraph by exactly one blank line, and
    the file ends in exactly one newline. Nothing already in the file is
    edited, reordered or deleted — §4 item 20 forbids rewriting landed text,
    and GATE1 carries a dated correction instead, which is why this round
    exists in this shape.
 5. ONE WHOLE-FILE REPLACEMENT AND ONE APPEND. PLANF022R2 replaces
    `.agent/plan.md` at C1 in full, written as the slice plus exactly one
    terminating newline. GATE1 is the append of constraint 4.
 6. Block size, measured on these final bytes: TOTAL 165 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 127
    against DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C2; the branch is `feature/f022-live-cost-ticker`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b and C1.
     C2's own reading is owed to the next round's ledger entry (§3 item 31).
 G2  TRANSPORT: sha256 over `.agent/authored/f022-r2.md` at C0a, over
     `.agent/last_block.md` at C0b, over the source file this block was read
     from, and over the digest the delegation names are all equal. That digest
     is stated OUTSIDE this file, because a digest of these bytes cannot exist
     inside them (§3 checklist item 9). Write C0b FROM the committed C0a blob,
     never from the source a second time, and report the digest and the byte
     and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 6's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R2 plus one terminating
     newline, proved against the slice extracted from the committed C0a blob,
     with a NEGATIVE CONTROL against the BARE slice which must DIFFER. Report
     both readings, plus `^## Goal$` 1, `^## Next Steps$` 1 and `wc -l` at most
     50.
 G5  THE APPEND UNDER TWO INDEPENDENT READERS. Reader (a): the round-base blob
     of `.agent/live_review.md` is a byte-exact PREFIX of the C2 file and the
     remainder is exactly one newline plus GATE1 plus one newline — report the
     remainder's byte count. Reader (b): split the C2 file on blank lines with
     your OWN splitter and confirm the LAST unit equals GATE1 exactly, and
     report the unit count at the base and at C2. Then the NEGATIVE CONTROL,
     inside a disposable worktree under `.remedy-wt/` and never in the primary
     checkout: flip one printable byte at the START of the appended paragraph
     at unchanged length and confirm BOTH readers REJECT that mutant while
     ACCEPTING the true file. Remove the worktree and report `git worktree
     list` as a line count.
 G6  THE LEDGER SETS, line-anchored, at the round base then at C2: `^- R-\d+ — `
     and how many are DISTINCT; `^Done: R-`; `^Landed: `; `^Gate: R` and how
     many are DISTINCT; `^Gate: R1 `; and the MAXIMUM registered id. Report each
     at BOTH points. The reviewer measured the base as 230 entries all distinct,
     0, 0, 1 key distinct, 0 and `R-0669`.
 G7  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C2: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf`. Report the exit code
     and the passed-plus-skipped total. The reviewer measured this at
     `e62e8747` as exit 0 at 528 passed.
 G8  CANARY, run serially after G7: `python3 -m pytest
     tests/cli/test_golden_path.py -q -rf`. Report the exit code and the total.
     The reviewer measured it at `e62e8747` as exit 0 at 42 passed. NO docs gate
     is ordered this round because no path under `docs/` is in the change set.
 G9  RANGE, executed after C2: the range from the round base to C2 lists exactly
     the paths of this block's `Change:` list, with the set difference EMPTY in
     both directions, and 0 paths beginning `packages/`, `apps/` or `tests/`.
     Report the two set differences and that count. Then: every commit
     single-parent; `git show --numstat` and `git diff --numstat` agreeing cell
     by cell with the handback's own `## Commits` table (§3 item 28); every
     insertion count under the 500 cap; leading `<<<SLICE ` and `<<<END `
     reading 0 LINES in `.agent/plan.md` and `.agent/live_review.md`;
     `git ls-files .remedy-wt` reading 0; and this round's reflog rows
     classified with `amend`, `rebase` and `cherry` each 0.
 G10 NO PULL REQUEST IS CREATED AND NONE IS MERGED. Report the output of
     `gh pr list --state open --json number,headRefName` and state that this
     round ran neither `gh pr create` nor `gh pr merge`.
 G11 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each commit of the
     `Bundle:` list, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), and the block's
     `Fortschritt:` line verbatim across all three of its lines. Its own `wc -l`
     is reported, and a DECISION D15 line declares any overage.

Handback:   completion report + rewrite `.agent/handoff.md`.

The slices follow. Each begins with a `<<<SLICE <name>` line and ends with a
`<<<END <name>` line; neither marker line is part of the slice, and no slice
includes a terminating newline unless a gate above says it does.

<<<SLICE PLANF022R2
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
R2 records the R1 verdict on disk and nothing else. R1 PASSED, and a verdict
that exists only in a session dies with it (finding R-0571), so this round
appends the gate entry and carries the reviewer's dated correction to one
sentence R1 landed inside R-0669. It mints no id and builds nothing.

## Next Steps
1. R3 the cost inventory: where the budget guard evaluates spent-vs-limits, what
   the Part E event vocabulary already defines, and what MetricsBar renders
   today — each MEASURED in the source rather than read off the feature file.
2. R4 record R3 and rule the tick envelope as a DECISION: the payload's field
   set, the basis vocabulary and the no-client-arithmetic contract.
3. R5 onward the built work, in the T001/T002/T003 order the feature file's Task
   slicing names.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF022R2

<<<SLICE GATE1
Gate: R1 — the F022 R1 entry. R1 PASSED ON EVERY GATE, AND THE REVIEWER REBUILT THE ROUND'S ONE SCRIPTED ARTEFACT INDEPENDENTLY RATHER THAN CHECKING THE WORKER'S ARITHMETIC. TRANSPORT HELD IN ITS STRONGEST FORM, not the digest fallback: `.agent/authored/f022-r1.md` at `6e39b9c0`, `.agent/last_block.md` at `23bf7ef5` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f022-r1.md`, are all sha256 `e07ad805e616fd573108041da87c341115e79b598df6c057fdbf411aa9f730a3` over 35426 bytes and 419 lines, so §4.9's primary comparison against the reviewer's own original was available and was used. The reviewer's extraction out of the committed C0a blob printed 12 slices over 142 CONTENT lines, and constraint 10's numerals re-measure as 419 TOTAL and 277 PROSE, under DECISION F085 D6's 490 and D5's 400. THE APPLIED TEXTS ARE BYTE-EQUAL DISK TO DISK, each against the slice extracted from the committed blob and each with a negative control against the bare slice that DIFFERS: `.agent/plan.md` at `6f9a7e16`, `.agent/context.md` at `df004de7` and `.agent/candidates.md` at `f70e10c7` all equal their slice plus exactly one terminating newline. THE RESET IS THE REVIEWER'S OWN RECONSTRUCTION AND NOT A CHECK OF THE WORKER'S: the reviewer re-ran the constraint 6 ENTRY algorithm over `.agent/live_review.md` at the round base `c34ef32b`, classified 228 entries, dropped R-0660 and R-0663 as resolved, carried 226 entries of which 12 hold more than one unit and 16 continuation paragraphs in total, appended R0666, R0667, R0668, R0669 and GATE41, and the result is BYTE-IDENTICAL to the file committed at `3c5b3f26` at sha256 `0486c83d92c850852f79680086c09798d0be47ea2bb0e649543b8fa912f097ba`. Every one of the 226 carried entries was additionally confirmed to occur VERBATIM in the base blob, so nothing was summarised, rewrapped or truncated. THE ENTRY RULE EARNED ITS KEEP: a unit-level carry — the rule F021 R1 used — would have dropped all 16 of those continuation paragraphs, keeping each finding's headline while deleting the `FIX:` clause that says how to fix it, which is the failure DECISION F057 D1 was written against. THE DECISION RESCUE HELD: the base blob of `.agent/decisions.md` is a byte-exact PREFIX of the file at `388c6ccf`, the selector matched exactly the three units `DECISION F021 D6`, `D7` and `D8`, each occurs exactly once in the 5489-byte remainder, and `.agent/live_review.md` is byte-unchanged at that commit, which is what made C4's deletion safe. THE SETS AT C4, line-anchored: 230 entries all DISTINCT, `^Done: R-` 0, `^Landed: ` 0, `^Gate: R` 1 key distinct, `^Gate: R1 ` 0, maximum id `R-0669`, and the ids present at C4 but absent at the base are exactly R-0666, R-0667, R-0668 and R-0669 — nothing else was minted. THE ROADMAP CLAIM HELD, line-anchored, base then C6: `^- \[~\] ` 0 then 1, `^- \[~\] F022 — ` 0 then 1, `^- \[ \] F022 — ` 1 then 0, and `^- \[x\] ` 56 at BOTH, so the claim moved one marker and disturbed no accepted row. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/docs/` exit 0 at 295 passed; `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed; the four state readers exit 0 at 528 passed; and the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed. STRUCTURE HELD: eight commits over `c34ef32b..e62e8747`, every one single-parent, insertions 419, 392, 26, 31, 10, 38, 4 and 69, each under the 500 cap; the range path set EQUAL to the block's declared set with the difference empty in both directions and 0 paths beginning `packages/`, `apps/` or `tests/`; `^<<<SLICE ` and `^<<<END ` reading 0 in all six slice targets; `git ls-files .remedy-wt` 0; one worktree; `git status --porcelain` empty; and the round's reflog rows carrying eight `commit` operations with 0 amend, 0 rebase and 0 cherry. THE ROUND'S ONE DECLARED DEVIATION IS ACCEPTED: G7, G8 and G9 were first run against the C6 tree immediately before the C6 commit, because their numbers are mandated content of the handback C6 itself carries, and the worker then RE-RAN all four after C6 with identical results — the honest handling of §3 item 31, and the only file differing between the two runs was `.agent/handoff.md`, which none of those suites reads. TWO MEASURED DISAGREEMENTS WITH THE BLOCK WERE REPORTED BY THE WORKER RATHER THAN RECONCILED, exactly as constraint 8 required, and the reviewer re-measured both. THE FIRST IS NOT A DEFECT: constraint 7 said 12 findings carry an indented `  FIX:` paragraph, which is true of the base file's 12 such units, while the worker counted 11 among the CARRIED entries because the twelfth belongs to R-0660, which is resolved and dropped; both numbers are right and only their scope differs, and the deliverable that constraint actually ordered — multi-unit carried entries — is 12 under both readings. THE SECOND IS A DEFECT, AND IT IS THE REVIEWER'S OWN: R-0669's prose states that this reset "also drops the 16 `Recurrence:` paragraphs", and the line-anchored count is 16 at the base and 2 at C4, because R-0665's two `Recurrence:` continuations survive as units of an open entry. CORRECTION, dated 2026-08-23 and recorded here because §4 item 20 forbids rewriting landed text: the reset dropped 14 of the 16 `Recurrence:` paragraphs and carried 2, by the same survival-by-adjacency mechanism R-0669's own body describes for `DECISION F021 D7`. The finding's substance is unaffected — a ruling's survival still depends on adjacency rather than on a rule — and the sentence is wrong only in its numeral and its universal. NO ID IS MINTED FOR IT: the defect is a false quantifier in reviewer-authored text about a file the same block edited, and the reviewer searched the open set at `3c5b3f26` before deciding, finding R-0520, R-0521 and R-0524 all ABSENT from the carried record because they were resolved before the reset, so the correction lives here as the record rather than under a new id. THE VERDICT IS PASS: the shipped change is a plan, a context, a decision rescue, a scripted reset, an emptied candidates file and a roadmap row, every one of them verified byte-equal to its authored slice or byte-identical to the reviewer's own independent rebuild, and the one real defect is the reviewer's own sentence rather than the worker's execution, which deviated from nothing it did not declare.
<<<END GATE1
