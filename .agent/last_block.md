── STEP CLAIM — F022 ──
Goal:        Claim F022. Create the branch, preserve the three F021 DECISIONS
             that live only in the review record, reset that record carrying the
             F021 open set forward, gate F021 R41, register the three closure
             candidates F021 carried plus the defect the preservation step
             exists for, empty the candidates file, and claim F022 in the
             roadmap ledger. This round BUILDS NOTHING: no file under `apps/`,
             `packages/` or `tests/` is touched.

Fortschritt: ~0 % (T001 offen · T002 offen · T003 offen; diese Runde beansprucht
             das Feature, rettet drei Entscheidungen, setzt das Review-Record
             zurueck, gatet F021 R41 und registriert vier Findings — gebaut wird
             ab R3) — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 context · C3 the
             decision rescue · C4 the review-record reset with the F021 R41 gate
             and the four registrations · C5 empty the candidates file · C6 the
             roadmap claim and the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f022-r1.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/context.md` (C2) ·
             `.agent/decisions.md` (C3) · `.agent/live_review.md` (C4) ·
             `.agent/candidates.md` (C5) · `docs/roadmap/STATUS.md` and
             `.agent/handoff.md` (BOTH in C6). Resolve any count in this block
             against this list rather than against a numeral written elsewhere.

Preface:     Before C0a, create the branch. `main` is at `c34ef32b` — the merge
             commit of pull request #211, which the reviewer merged at the Open
             PR Gate before this block was written, after CI concluded SUCCESS
             on `3c8c62e9`, the exact commit that request carried. Run
             `git checkout main`, `git pull --ff-only`, then `git checkout -b
             feature/f022-live-cost-ticker`. NO `gh pr merge` and NO
             `gh pr create` runs this round: F022 opens its pull request at
             closure, exactly as F021 did. THE ROUND BASE IS `c34ef32b` and
             every base reading below is taken there.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes every other substantive commit because the plan must be current
    before them (§3 checklist item 23). C6 is the LAST commit and carries the
    handback. C3 precedes C4 because C4 DELETES from `.agent/live_review.md`
    the very paragraphs C3 preserves; run in the other order the rescue has no
    source. That ordering is what GATE41 and R0669 refer to when they describe
    this round's own landed change (§3 checklist item 20, R-0524 carve-out).
 3. THIS ROUND MINTS EXACTLY FOUR FINDING IDS — `R-0666`, `R-0667`, `R-0668`
    and `R-0669` — and resolves nothing. It writes no `Done:` line and no
    `Landed:` line. The reviewer searched the OPEN SET for each DEFECT before
    minting it (§3 checklist item 30), measured in `.agent/live_review.md` at
    `c34ef32b`: `dirty_file_count_total`, `dirty_source_test_files`,
    `uncovered_source_test_files` and `job_report.json` each occur 0 times, so
    no open finding describes the first or the third candidate; `zero-byte`
    occurs 0 times; and for the fourth, `reset drops` and `only in this record`
    each occur 0 times while the 23 occurrences of `decisions.md` are all
    routing clauses of unrelated findings, none of which names a DECISION
    stranded in the review record. `commit_execution_gate` occurs 3 times and
    `ready_gate_matrix` 3 times, all inside `Gate:` paragraphs reporting a
    package reading rather than inside any finding, so the second candidate has
    no open holder either.
 4. WHOLE-FILE REPLACEMENTS, A SCRIPTED APPEND, A SCRIPTED REBUILD AND A
    FROM/TO PAIR. PLANF022R1 replaces `.agent/plan.md` at C1 in full.
    CONTEXTF022R1 replaces `.agent/context.md` at C2 in full.
    `.agent/decisions.md` is APPENDED TO BY SCRIPT at C3 per constraint 5.
    `.agent/live_review.md` is REBUILT BY SCRIPT at C4 per constraint 6.
    CANDIDATES1 replaces `.agent/candidates.md` at C5 in full. The single pair
    applies at C6. Its containment reading, PRINTED BY THE REVIEWER'S OWN SCRIPT
    against `docs/roadmap/STATUS.md` at `c34ef32b` and recorded here (§3
    checklist item 15): CLAIM `TO contains FROM: false`, so REWRITE — order the
    FROM-zero count for it. CLAIM's FROM occurs EXACTLY ONCE in that file at
    `c34ef32b`; the reviewer's script printed 1. Apply it with `count=1` and
    report the occurrence count measured BEFORE the replacement.
 5. THE C3 RESCUE, specified as an algorithm and not as byte surgery, because
    the paragraphs it moves are long single lines whose retyping is exactly the
    transport risk this workflow exists to remove. Read `.agent/live_review.md`
    at the round base. Split the WHOLE file on the two-character sequence
    newline-newline into units and strip each unit of leading newlines. Select
    every unit whose first line begins `DECISION F021 D`. Append to
    `.agent/decisions.md`, in the order they occur in the source: one blank
    line, then the heading line `## Rescued from the F021 review record (F022
    R1)`, then one blank line, then a paragraph of provenance the reviewer
    authors as RESCUENOTE, then each selected unit separated from its
    neighbour by exactly one blank line, and the file ending in exactly one
    newline. Report how many units that selector matched and the first 40
    characters of each. Do NOT edit `.agent/live_review.md` in this commit.
 6. THE C4 REBUILD, likewise an algorithm. Read `.agent/live_review.md` at the
    round base and split it into units exactly as constraint 5 does. Call a
    unit a RECORD START when its first line matches `^- R-\d+ — ` or begins
    `Done: ` or `Landed: ` or `Gate: R`, and call it a BOUNDARY when it is a
    RECORD START or its first line begins `#` or `>`. An ENTRY is a unit
    matching `^- R-\d+ — ` together with every unit that follows it up to but
    excluding the next BOUNDARY. Build the new file as, in order: LRHEAD, then
    every ENTRY whose id does NOT appear in any unit whose first line matches
    `^Done: (R-\d+)`, in their original order and WITH THEIR CONTINUATION UNITS
    INTACT, then R0666, then R0667, then R0668, then R0669, then GATE41 — units
    joined with exactly one blank line between neighbours and the file ending
    in exactly one newline. Everything not carried is DROPPED; git history is
    its archive, per DECISION F057 D1 in `.agent/decisions.md` and finding
    R-0362, whose scope is the OPEN FINDING SET.
 7. WHY THE ENTRY RULE OF CONSTRAINT 6 IS NOT THE UNIT RULE F021 R1 USED, and
    this is the substance of R0669's neighbour rather than a stylistic
    preference. The F021 R1 block carried FINDING UNITS, one blank-line unit
    per finding. At `c34ef32b` that reading is no longer faithful: the reviewer
    classified this file at that commit and 12 findings carry an indented
    continuation paragraph beginning `  FIX:` as a separate unit, and R-0659
    additionally carries a flush paragraph beginning `RECOVERED — THE R18
    VERDICT`. A unit-level carry drops every one of them, keeping each
    finding's headline while deleting the clause that says how to fix it — the
    same class DECISION F057 D1 exists to forbid, which records a reset that
    dropped three live findings without resolving, deferring or naming them.
    The ENTRY rule carries them. Report, from your OWN run, how many carried
    entries hold more than one unit.
 8. Report the numbers the C3 and C4 scripts THEMSELVES printed — the selector
    match count, the entry count, the number of entries carried forward, the
    ids dropped as resolved, and the multi-unit entry count. Do not restate the
    reviewer's numerals as your own reading; if your script disagrees with a
    constraint above, that disagreement is the finding and the handback says so
    instead of reconciling it.
 9. The `.agent/` state texts must satisfy the repo's own contract tests, which
    the reviewer validated against every test that reads those paths (§4.11):
    `.agent/plan.md` carries `## Goal`, `## Next Steps`, the substring `Steps`
    and a three-digit F-id; `.agent/context.md` carries `## Active Branch`, a
    `feature/` slug, the substring `Steps`, a three-digit F-id and the
    substring `pytest`; `.agent/live_review.md` carries the substring `Steps`.
    Those properties are gated at G6 and G7, not assumed.
10. Block size, measured on these final bytes: TOTAL 419 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 277
    against DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C6; the branch is `feature/f022-live-cost-ticker`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1, C2, C3,
     C4 and C5. C6's own reading is owed to the next round's ledger entry,
     because a commit cannot report the tree state that follows it (§3 checklist
     items 14 and 31).
 G2  TRANSPORT: sha256 over `.agent/authored/f022-r1.md` at C0a, over
     `.agent/last_block.md` at C0b, over the source file this block was read
     from, and over the digest the delegation names are all equal. That digest
     is stated OUTSIDE this file, because a digest of these bytes cannot exist
     inside them (§3 checklist item 9, the R-0371 class). Write C0b FROM the
     committed C0a blob, never from the source a second time, and report the
     digest and the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 10's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF022R1 plus one terminating
     newline, `.agent/context.md` at C2 is byte-equal to CONTEXTF022R1 plus one
     terminating newline, and `.agent/candidates.md` at C5 is byte-equal to
     CANDIDATES1 plus one terminating newline — each proved by comparing
     against the slice extracted from the committed C0a blob, and each paired
     with a NEGATIVE CONTROL comparing the file against the BARE slice with no
     terminating newline, which must DIFFER. Report all six readings.
 G5  THE C3 RESCUE. Report the selector's match count and, at the round base and
     again at C3, the count of `^## Rescued from the F021 review record` and of
     `^DECISION F021 D` in `.agent/decisions.md`. The base blob must be a
     byte-exact PREFIX of the C3 file, and the appended remainder must contain
     each selected unit exactly once. Then confirm, at C3, that
     `.agent/live_review.md` is UNCHANGED from the round base — same sha256 —
     which is what makes C4's deletion safe.
 G6  THE CONTRACT PROPERTIES, line-anchored where the anchor is meaningful, at
     the commit that writes each file: in `.agent/plan.md` at C1, `^## Goal$` 1
     and `^## Next Steps$` 1 and `wc -l` at most 50; in `.agent/context.md` at
     C2, `^## Active Branch$` 1 and the substrings `feature/` and `Steps` and
     `pytest` each present and a match for `\bF\d{3}\b` present; in
     `.agent/live_review.md` at C4, the substring `Steps` present.
 G7  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C6: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py
     tests/orchestration/test_integrity_gate.py -q -rf`. Report the exit code
     and the passed-plus-skipped total, and COUNT BY PASSED PLUS SKIPPED because
     data-dependent skips in `tests/ui_server/` move the split run to run. The
     reviewer measured this at `c34ef32b` as exit 0 at 528 passed.
 G8  THE DOCS GATES, both of them, run serially after C6 because C6 touches
     `docs/roadmap/STATUS.md`: `python3 -m pytest tests/docs/ -q -rf` and
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`.
     Report both exit codes and both totals. The reviewer measured these at
     `c34ef32b` as exit 0 at 295 passed and exit 0 at 30 passed. The second is
     ordered because `tests/docs/` asserts nothing about a roadmap ledger row's
     own content, which is finding R-0493.
 G9  CANARY, run serially and after G7 and G8 have finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total. The reviewer measured it at `c34ef32b` as exit 0 at
     42 passed.
 G10 THE C4 REBUILD UNDER TWO INDEPENDENT READERS. Reader (a) is the ENTRY
     classifier of constraint 6. Reader (b) is a line-anchored count over the
     SAME two blobs: `^- R-\d+ — ` entries and `^Done: R-\d+ ` lines at the
     round base, and the same two at C4. Report both readers' numbers at both
     points and state whether they AGREE. Then TWO NEGATIVE CONTROLS, both
     inside a disposable worktree under `.remedy-wt/` and never in the primary
     checkout: first, replace one printable byte inside the FIRST carried entry
     at equal length and confirm reader (a) REJECTS that mutant while ACCEPTING
     the true file — the control must probe the head of the region, not its
     tail (R-0631); second, DELETE one continuation unit from a multi-unit
     carried entry and confirm reader (a) REJECTS that mutant too, which is the
     control that constraint 7 needs and a unit-level reader cannot fail.
     Remove the worktree before the handback and report `git worktree list` as
     a line count.
 G11 THE LEDGER SETS at C4, line-anchored at line start: `- R-` entries and how
     many are DISTINCT; `Done: R-` lines; `Landed: ` lines; `Gate: R` keys and
     how many are DISTINCT; `Gate: R1` occurrences; and the MAXIMUM registered
     id. Report each as a number. Only the four ids of constraint 3 may be
     minted, so the maximum id at C4 is `R-0669` and the next free id is
     `R-0670`. The reviewer measured the carried-forward open set at
     `c34ef32b` as 226.
 G12 THE ROADMAP LEDGER, line-anchored, at the round base then at C6:
     `^- \[~\] ` and `^- \[~\] F022 — ` and `^- \[ \] F022 — ` and `^- \[x\] `.
     Report all four at both points. The reviewer measured the base as 0, 0, 1
     and 56.
 G13 RANGE, executed after C6 because it reads C6: the range from the round base
     to C6 lists exactly the paths of this block's `Change:` list, with the set
     difference EMPTY in both directions, and 0 paths beginning `packages/`,
     `apps/` or `tests/`. Report the two set differences and that count. Then:
     every commit single-parent; `git show --numstat` and `git diff --numstat`
     agreeing cell by cell with the handback's own `## Commits` table (§3
     checklist item 28); every insertion count under the 500 cap; leading
     `<<<SLICE ` and `<<<END ` reading 0 LINES in each file a slice lands in;
     `git ls-files .remedy-wt` reading 0; and this round's reflog rows
     classified with `amend`, `rebase` and `cherry` each 0.
 G14 NO PULL REQUEST IS CREATED AND NONE IS MERGED. Report the output of
     `gh pr list --state open --json number,headRefName` and state that this
     round ran neither `gh pr create` nor `gh pr merge`.
 G15 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each commit of the
     `Bundle:` list, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), and the block's
     `Fortschritt:` line verbatim across all four of its lines. Its own `wc -l`
     is reported, and a DECISION D15 line declares any overage with the mandated
     content that caused it. Every gate above runs at a commit STRICTLY EARLIER
     than C6 except G13 and G14, whose readings are owed to the next round's
     ledger entry rather than to this file (§3 checklist item 31).

Handback:   completion report + rewrite `.agent/handoff.md`.

The slices follow. Each begins with a `<<<SLICE <name>` line and ends with a
`<<<END <name>` line; neither marker line is part of the slice, and no slice
includes a terminating newline unless a gate above says it does.

<<<SLICE PLANF022R1
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
R1 claims F022. It creates the branch, rescues the three F021 DECISIONS that
live only in the review record into `.agent/decisions.md`, resets that record
carrying the F021 open set forward by ENTRY rather than by unit, gates F021 R41,
registers R-0666, R-0667, R-0668 and R-0669, empties the candidates file and
moves the roadmap row to `[~]`. It builds nothing.

## Next Steps
1. R2 the cost inventory: where the budget guard evaluates spent-vs-limits, what
   the Part E event vocabulary already defines, and what MetricsBar renders
   today — each MEASURED in the source rather than read off the feature file.
2. R3 record R2 and rule the tick envelope as a DECISION: the payload's field
   set, the basis vocabulary and the no-client-arithmetic contract.
3. R4 onward the built work, in the T001/T002/T003 order the feature file's Task
   slicing names.

## Risks
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F022
  defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF022R1

<<<SLICE CONTEXTF022R1
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
R1 claim and reset → R2 the cost inventory → R3 the envelope DECISION → R4
onward T001, T002 and T003 in the feature file's order.
<<<END CONTEXTF022R1

<<<SLICE LRHEAD
# Live Review — F022 Live cost ticker

> Round-by-round review record for the F022 branch, reset at the feature claim.
> The F021 record closed with pull request #211, merged into `main` at this
> feature's Open PR Gate as `c34ef32b` after CI concluded SUCCESS on `3c8c62e9`.
> That branch's LAST round, R41, has no gate entry in its own record by
> construction, because a round's verdict is written by the NEXT reviewed round
> (DECISION F085 D9) and R41 was the last round F021 had; its entry is therefore
> the last `Gate:` paragraph below. Finding ids continue the monotonic R-XXXX
> series across the reset.
>
> This header carries NO next-free-id sentence, and its absence is the fix for
> R-0406 rather than an omission: `docs/agents/planner_reviewer_prompt.md` §3
> item 10 already requires every emission to recompute the ceiling mechanically
> from this record. Derive it with `max` over the line-anchored `^- R-\d+ — `
> entries below.
>
> This reset CARRIES the open set forward rather than dropping it, per DECISION
> F057 D1 in `.agent/decisions.md` and finding R-0362. The findings open when
> the F021 record closed are reproduced verbatim below, extracted BY ENTRY out
> of the previous record by script and never retyped, never rewrapped and never
> summarised. An ENTRY is a finding paragraph TOGETHER WITH the continuation
> paragraphs beneath it — the indented `FIX:` clauses and, for one finding, a
> recovered verdict — because a unit-level carry keeps each headline while
> deleting the clause that says how to fix it, which is the very failure
> DECISION F057 D1 was written against. R-0669 below registers what that
> difference cost and what still leaks.
>
> The `Gate:` paragraphs, the resolutions and the round records of the F021
> branch are DROPPED here with git history as their archive. The three
> operator-visible DECISIONS F021 D6, D7 and D8 were rescued into
> `.agent/decisions.md` by this round's own C3 BEFORE this rebuild ran, so the
> reset destroys no ruling.

## Steps
R1 claim F022 in the roadmap ledger, create the branch, rescue the F021
decisions, reset this record carrying the F021 open set forward, gate F021 R41
and register the three candidates F021 carried plus R-0669 → R2 the cost
inventory: where the budget guard evaluates spent-vs-limits, what the Part E
event vocabulary defines and what MetricsBar renders today, each MEASURED in the
source → R3 record R2 and rule the tick envelope as a DECISION → R4 onward the
built work, in the T001/T002/T003 order the feature file's Task slicing names.

## Findings
<<<END LRHEAD

<<<SLICE RESCUENOTE
These rulings were taken during F021 and recorded ONLY in `.agent/live_review.md`, which is rebuilt at every feature claim. F022 R1 moved them here verbatim, extracted by script from that file at `c34ef32b` and never retyped, immediately before the rebuild that would otherwise have deleted them. Finding R-0669 registers the defect this rescue works around. The paragraphs below are the originals; their round context is in the `Gate:` paragraphs of that file at `c34ef32b`, which git history keeps.
<<<END RESCUENOTE

<<<SLICE R0666
- R-0666 — Low, AN ALIGNMENT SUMMARY REPORTS ONE DIRTY FILE WHILE EVERY LIST IT SUMMARIZES IS EMPTY. Raised by the reviewer during the F021 closure review, carried in `.agent/candidates.md` as a closure candidate per docs/roadmap/STATUS_closure_protocol.md "Closure-candidate findings", and registered here because this is F022's first reviewed round. Measured by the reviewer at `4db0a2e4`, in the manifest inside `remedy-review-20260823-005026-READY_FOR_REVIEW.zip`: `review_subject_evidence_alignment.dirty_file_count_total` reads 1 while `dirty_source_test_files` and `uncovered_source_test_files` are both empty, `issues` is empty and the verdict is `PASS`. The package was built from a tree whose `git status --porcelain` printed 0 lines, so either that count has a source none of the lists expose or it is stale. Nothing about the F021 closure is unsound because of it — the verdict rests on the empty lists and the PASS — but a non-zero count beside three empty collections is the kind of number a later reader will either trust or panic about, and neither is justified. Low, because no false claim is asserted and no gate consumed the field. FIX: find the producer of that field, and either make it name the file it counted or derive it from the lists it sits beside. The fix edits the evidence packager, which F022 does not own, so it routes to the same paydown branch as R-0403. OPEN.
<<<END R0666

<<<SLICE R0667
- R-0667 — Low, TWO GATES IN ONE EVIDENCE PACKAGE DISAGREE ABOUT WHETHER A HUMAN MUST STILL APPROVE. Raised by the reviewer during the F021 closure review, carried in `.agent/candidates.md` as a closure candidate, and registered here because this is F022's first reviewed round. Measured by the reviewer at `4db0a2e4`: `commit_execution_gate.json` in the evidence bundle and the `commit_execution_gate` field of `final_verifier_report.json` both read `NEEDS_HUMAN_APPROVAL`, and `human_final_reviewer_required` is true, while the same package's `ready_gate_matrix.ok` is true over an empty `blocking_reasons` and `PACKAGE_STATUS` is `READY_FOR_REVIEW`. Both readings are defensible on their own terms and the closure protocol treats the ready gate as the blocker, so nothing here blocked F021; the cost is that a reader cannot tell from the package alone which authority governs. THE ADDRESS IS PART OF THE RECORD, because the F021 R40 handback got it wrong and the correction belongs with the finding: that handback located the verdict at a manifest key `gate_verdicts.commit_execution_gate`, and the package manifest carries no `gate_verdicts` key at all — the two addresses named above are where the value really lives. Low, because the value is real at both addresses and only the arbitration between them is unstated. FIX: have the packager either surface the commit-execution verdict in the manifest beside the ready gate, or record why the ready gate supersedes it. The fix edits the evidence packager, which F022 does not own, so it routes to the same paydown branch as R-0403. OPEN.
<<<END R0667

<<<SLICE R0668
- R-0668 — Low, EVERY CLOSURE BUNDLE ON THIS MACHINE CARRIES A ZERO-BYTE `job_report.json`. Raised by the reviewer during the F021 closure review, carried in `.agent/candidates.md` as a closure candidate, and registered here because this is F022's first reviewed round. The reviewer measured all thirteen `remedy-job-evidence-*` directories under `.remedy-wt/` at `4db0a2e4` and `job_report.json` is 0 bytes in every one of them, F021's included. The producer emits the file and writes nothing into it, inside a bundle whose entire purpose is evidence, and no gate notices because nothing reads it. This is not an F021 defect and it blocked nothing — the substance lives in `final_verifier_report.json`, `verification_tests.json` and `review_subject.json`, all of which the reviewer read and re-derived — but an always-empty evidence artifact is either a producer bug or a file that should not be emitted. Low, because nothing reads it and no claim rests on it. FIX: decide which, and either populate it or stop writing it. The fix edits the evidence job builder, which F022 does not own, so it routes to the same paydown branch as R-0403. OPEN.
<<<END R0668

<<<SLICE R0669
- R-0669 — Medium, AN OPERATOR-VISIBLE DECISION RECORDED IN THE REVIEW RECORD IS SCHEDULED FOR DELETION BY THE NEXT FEATURE CLAIM. Raised by the reviewer while designing this round's own reset, and registered rather than merely worked around because the workaround does not generalise. `docs/agents/planner_reviewer_prompt.md` §4 item 7 requires a re-plan to be recorded as an operator-visible DECISION "in the brief and the ledger", and AGENTS.md gives `.agent/decisions.md` as the home for meaningful decisions; nothing reconciles the two, so a reviewer who follows item 7 literally writes the ruling into `.agent/live_review.md` alone. That file is REBUILT at every feature claim and everything not carried is dropped. Measured by the reviewer at `c34ef32b`: `DECISION F021 D6`, `DECISION F021 D7` and `DECISION F021 D8` occur in `.agent/live_review.md` and NONE of the three occurs anywhere in `.agent/decisions.md`, whose only F0-series entry for this class is DECISION F057 D1. The reviewer then dry-ran this round's own C4 rule against that file at `c34ef32b` before ordering it, and the result is what makes this Medium rather than Low: D6 and D8 would have been DELETED, while D7 SURVIVES — not by design, but because it happens to sit inside the entry of R-0659, an open finding, and the ENTRY rule carries a finding's continuation paragraphs. A ruling's survival therefore depends on whether the round that recorded it also happened to register a finding immediately above it, which is luck wearing the appearance of a rule. C3 rescues all three regardless, and C3 is a one-off this block ordered rather than anything a rule requires. Medium rather than Low, because the artefact lost is a ruling the operator is entitled to veto at any later relay, because the loss is silent and no gate goes red on it, and because it has almost certainly already happened: this reset is the fourth in the R-06xx series and the earlier three carried no rescue step. The same reset also drops the 16 `Recurrence:` paragraphs and the round records, which is intended — git history is their archive per DECISION F057 D1 — and a DECISION differs precisely because it is meant to stay live until reversed. FIX: make the carrier unambiguous, by amending §4 item 7 to name `.agent/decisions.md` as the durable home and the ledger as the round-local echo, and by giving the reset a standing rescue step for any `^DECISION ` unit rather than the one-off this round ordered. The fix edits `docs/agents/planner_reviewer_prompt.md`, which F022 does not own, so it routes to the same paydown branch as R-0403. OPEN.
<<<END R0669

<<<SLICE GATE41
Gate: R41 — the F021 R41 entry. R41 PASSED AND F021 IS CLOSED AND MERGED. The reviewer re-executed that round's gates off disk in the primary checkout and every one reproduces; nothing in the handback was taken on its word. TRANSPORT HELD at sha256 `5d70acad7ce3b7bd114be8d256db6a844fe5efc99320179bc5ddcf187298c70d` over 27341 bytes and 295 lines, EQUAL across the working copy of `.agent/authored/f021-r41.md`, the committed C0a blob at `461b8e6f` and `.agent/last_block.md` at `f6bf1c16`. THE SIZE ARITHMETIC RE-MEASURES from that same blob as 11 slices over 116 CONTENT lines with 22 marker lines, so TOTAL 295 against DECISION F085 D6's 490 and PROSE 179 against D5's 400, matching the block's own constraint. THE APPLIED TEXTS ARE BYTE-EQUAL: `.agent/plan.md` equals PLANF021R41 plus exactly one terminating newline and NOT the bare slice, and `.agent/candidates.md` equals CANDIDATES plus exactly one terminating newline and NOT the bare slice. THE APPEND HELD UNDER BOTH READERS: the round-base blob of `.agent/live_review.md` is a byte-exact PREFIX of the R41 file and the remainder is exactly 9048 bytes opening `Gate: R41 — the R`; the reviewer's own blank-line split reads 308 units whose last two are the RECORD41 and DONE0663 slices in that order, each occurring exactly once. THE PAIRS HELD against `README.md`: READMEFROM1 and READMEFROM2 read FROM 0x and TO 1x as rewrites, and READMETO3 CONTAINS its FROM verbatim, so that pair is APPEND-shaped and its FROM correctly still reads 1x — the §4.9 reading rather than a FROM-zero count. THE SETS DID NOT MOVE except where intended, base then head: canonical `^- R-\d+ — ` 228 then 228, ALL DISTINCT at both with maximum R-0665; loose `^- R-` 229 then 229; `^Done: R-` 1 then 2; `^Done: R-0663 — ` 0 then 1; `^Landed: ` 0 then 0; `^Gate: R` 39 then 40; `^Gate: R41` 0 then 1; `^Recurrence: ` 16 then 16; OPEN 227 then 226. THE ROADMAP ROW MOVED CORRECTLY: `^- \[~\] F\d+ — ` 0 and `^- \[x\] F\d+ — ` 56 at the R41 head, with the STATUSLINE slice occurring exactly once. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: `tests/docs/` exit 0 at 295 passed, `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed, the four state readers exit 0 at 528 passed, and the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed. STRUCTURE HELD: five commits, every one single-parent, insertions 295, 254, 17, 4 and 162, each under the 500 cap; the handback's `## Commits` cells agree with `git diff --numstat` cell by cell, which is the §3 item 28 reading that most often drifts and did not here; `^<<<SLICE ` and `^<<<END ` read 0 in each of the five slice targets; `git ls-files .remedy-wt` 0; `git worktree list` one entry; every reflog row of the round reads `commit` with 0 amend, 0 rebase and 0 cherry; and `git status --porcelain` printed 0 lines at the head. OWED TO THIS ENTRY BECAUSE C3 COULD NOT STATE THEM ABOUT ITSELF (§3 item 31): C3's SHA is `3c8c62e9`, its insertion count is 162 across four paths, `git status --porcelain` printed 0 lines at it, and the pull request it opened is #211. ALL SEVEN OF R41'S DECLARED DEVIATIONS ARE ACCEPTED, including its 133-line handback under DECISION D15 and its declaration that `.agent/candidates.md` is a whole-file replacement whose shape no gate stated. THE CLOSURE IS COMPLETE: pull request #211 was merged into `main` at F022's Open PR Gate as `c34ef32b` with its branch deleted, its `ci` check having concluded SUCCESS on `3c8c62e9`, the exact commit the request carried. NO ID IS SPENT ON A CORRECTION HERE; the three closure candidates R41 recorded are registered above as R-0666, R-0667 and R-0668, and R-0669 registers a defect of the reset rule this round had to work around rather than anything R41 did.
<<<END GATE41

<<<SLICE CANDIDATES1
# Closure Candidates — carrier of record

> Written per docs/roadmap/STATUS_closure_protocol.md ("Closure-candidate
> findings", disk-vehicle rule, operator ruling 2026-08-01). Read at Window-1
> session bootstrap (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present at
> feature-claim time is a block condition.

EMPTY. The three candidates F021 carried were registered as findings R-0666,
R-0667 and R-0668 in `.agent/live_review.md` by F022 R1, the first reviewed
round after that closure, and this file was emptied in the same round exactly as
the closure protocol requires.
<<<END CANDIDATES1

<<<SLICE CLAIMFROM
- [ ] F022 — Live cost ticker
<<<END CLAIMFROM

<<<SLICE CLAIMTO
- [~] F022 — Live cost ticker
<<<END CLAIMTO
