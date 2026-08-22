── STEP RECORD-AND-CLOSE — F021 ──
Goal:        Record the R3 verdict and close this SESSION cleanly. The reviewer's
             session ends at its stated round cap with the verdict on disk and a
             handoff that names the next session's first action, which
             docs/agents/self_drive_protocol.md calls a SUCCESS rather than a
             failure. This round BUILDS NOTHING and touches no file under
             `apps/`, `packages/` or `tests/`.

Fortschritt: ~10 % (T001 offen · T002 offen · T003 offen; R1 beansprucht, R2
             vermessen, R3 entschieden, R4 schreibt das Verdikt und schließt die
             Session — gebaut wird ab R5) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R3 verdict ·
             C3 the session handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r4.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3).
             That list is FIVE paths; resolve any count in this block against
             this list rather than against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (§3 checklist item
    23). C3 carries only the handback.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. R-0648 stays the maximum
    registered id and R-0649 is the next free one. The one defect this round
    records is the REVIEWER'S OWN, in the R3 block's G5, and it is recorded as
    evidence against the OPEN finding R-0631 inside RECORD3 rather than under a
    new id, because §3 checklist item 30 requires the open set to be searched
    for the DEFECT first and that search returned R-0631 holding exactly it.
 4. ONE APPEND AND ONE WHOLE-FILE REPLACEMENT. PLANF021R4 replaces
    `.agent/plan.md` at C1 in full. RECORD3 appends to `.agent/live_review.md`
    at C2, based on the ROUND BASE. There is NO FROM/TO pair this round, so no
    containment reading is owed and none is stated. RECORD3 is ONE blank-line
    unit; the reviewer measured that on the slice's own bytes before emission,
    which is the property G5's reader (b) below depends on and which the R3
    block asserted without measuring.
 5. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and run no
    formatter or linter that rewrites a file in place.
 6. Do NOT create a pull request and do NOT merge one. The branch stays open and
    unmerged: F021 is mid-feature, so there is nothing to open a pull request
    for and nothing to merge. Push the branch.
 7. THE HANDBACK IS ALSO THE SESSION HANDOFF. Beyond the mandated sections it
    states, in its `## Next` section and in this order, the three things the next
    session needs and cannot recompute cheaply: (a) that the next session's FIRST
    action is docs/agents/self_drive_protocol.md Phase 1 rule 1, the `.agent/STOP`
    check, BEFORE rule 2's Open PR Gate — naming rule 1 ahead of rule 2 is
    required by that protocol's Phase 2 and by finding R-0347; (b) that the Open
    PR Gate will find NO open pull request, so rule 5 applies and F021 continues;
    (c) that the next round is R5 and its work is T001 — the humanize catalog
    module, the coverage test DECISION F021 D1 rules, the honest generic line for
    an unrecognised kind, and goldens — built headless-first per the feature
    file's Orchestrator brief, and that `.agent/f021_inventory.md` at `4a7b5cbf`
    is the measured ground it starts from.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 192
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 149 against DECISION F085 D5's 400. Marker lines count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C3; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     C3's own reading goes in the round report (§3 checklist item 14).
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r4.md` at C0a, over
     `.agent/last_block.md` at C0b, and over the bytes you received are all
     equal. Write C0b FROM the committed C0a blob. Report the digest with the
     byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 8's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R4, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD3 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE APPEND at C2, under TWO INDEPENDENT READERS, with reader (b) stated as
     the R3 round proved it must be. Reader (a): the round-base blob of
     `.agent/live_review.md` is a byte-exact PREFIX of the C2 file and the
     remainder is EXACTLY one newline plus RECORD3 — report the remainder's
     sha256, byte count and line count, and the file's byte and line counts
     before and after. Reader (b), the SET-WISE form: split BOTH blobs on the
     blank line into units and confirm that the C2 unit LIST equals the base
     unit list followed by RECORD3's own units, compared ELEMENTWISE over the
     whole list and not at the tail — report N at both points. NEGATIVE CONTROL:
     replace one printable byte of the FIRST paragraph of the C2 file at equal
     length and confirm BOTH readers REJECT that mutant while BOTH ACCEPT the
     true file. Reader (b) in its elementwise form CAN reject a first-paragraph
     mutant; the tail-only form the R3 block ordered could not, which is finding
     R-0631 and is recorded in RECORD3. Run the destructive half inside a
     disposable worktree under `.remedy-wt/`, never in the primary checkout, and
     remove and prune it before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R4` occurrences;
     and the MAXIMUM registered id. Report each at BOTH points. Nothing is
     minted, so the maximum reads R-0648 at both and `Gate: R4` reads 0 then 1.
 G7  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY after C3:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED. No docs
     gate is ordered this round because the change set holds no
     `docs/roadmap/**` path — check that against the `Change:` list before you
     accept this sentence.
 G8  CANARY, run serially and after G7 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G9  NO PRODUCTION FILE CHANGED: report that the range from the round base to C3
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git ls-files .remedy-wt` reads 0.
 G10 RANGE, executed after C3: the range from the round base to C3 lists exactly
     the paths of this block's `Change:` list, with the set difference EMPTY in
     both directions. Report both differences. Then: every commit single-parent;
     `git show --numstat` and `git diff --numstat` agreeing cell by cell with
     the handback's own `## Commits` table (§3 checklist item 28); every
     insertion count under the 500 cap; leading `<<<SLICE ` and `<<<END `
     reading 0 LINES in both files a slice lands in; and this round's reflog rows
     classified with `amend`, `rebase` and `cherry` each 0.
 G11 NO PULL REQUEST: report `gh pr list --state open --json number,headRefName`
     and state that neither `gh pr create` nor `gh pr merge` was run. The
     expected reading is an EMPTY list, which is also the fact constraint 7(b)
     tells the next session to expect.
 G12 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), the block's
     `Fortschritt:` line verbatim across all three of its lines, and the three
     items constraint 7 requires in its `## Next` section. Its own `wc -l` is
     reported against the 60-line cap a five-commit round allows, with a
     DECISION D15 line declaring any overage and naming the mandated content
     that caused it. Every commit heading in the `## Commits` table carries that
     commit's FULL subject, and where a commit cannot name its own SHA the role
     and the reason are written INSIDE the heading rather than left to a channel
     that ends with this session — that omission is finding R-0494.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R4
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps the streamed event kinds to plain lines, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers the
kind set DECISION F021 D1 rules and an unknown kind renders an honest generic
line rather than vanishing, the feed renders fixture streams per the binding CSS,
jump-to-node focuses the right node, and the steering input renders DISABLED with
its honest tooltip until F030 lands.

## Current Step
R4 records the R3 verdict and closes the reviewer's session at its stated round
cap, leaving the verdict on disk and a handoff that names the next session's
first action. It builds nothing. The branch is mid-feature and carries no pull
request by design.

## Next Steps
1. R5 builds T001 headless-first: the humanize catalog module, the coverage test
   DECISION F021 D1 rules, the honest generic line for an unrecognised kind, and
   goldens. `.agent/f021_inventory.md` at `4a7b5cbf` is the measured ground.
2. R6 rules the two remaining infrastructure DECISIONS before T002 needs them —
   the frontend test environment, which today collects no component test, and
   the single-subscription fan-out.
3. R7 onward T002 then T003, in the feature file's Task slicing order.

## Risks
- T002 cannot be tested until the frontend test environment changes: measured at
  `4a7b5cbf`, `apps/ui/vitest.config.ts` sets `environment: "node"` and
  `include: ["src/**/*.test.ts"]`, so no `.test.tsx` is collected at all. R6
  rules it; R5 does not need it because T001 is a pure module.
- Jump-to-node needs the additive envelope field DECISION F021 D2 permits. That
  is the one production seam this feature opens, and it stays one field.
- The open set carried into this record at R1 holds no code defect of F021;
  R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown
  branch.
<<<END PLANF021R4

<<<SLICE RECORD3
Gate: R4 — the R3 entry. R3 PASSED, AND THE ONE DEFECT IT SURFACED IS THE REVIEWER'S OWN GATE RATHER THAN THE WORKER'S WORK. THE ARTEFACTS WERE REBUILT INDEPENDENTLY, NOT CHECKED: the reviewer re-derived all three of this round's applied artefacts from the round base and every one is byte-identical to what landed. `.agent/live_review.md` at `d49cad70` equals the base blob plus one newline plus RECORD2; `.agent/decisions.md` at `14060467` equals the base blob plus one newline plus DECIDE1; and `docs/roadmap/features/T5_F021.md` at `1674333f` equals the base file with AMENDA, AMENDB and AMENDC applied in that order with count=1 each. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r3.md` at `a0fa3380`, `.agent/last_block.md` at `12e0c51d` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r3.md`, are all sha256 e25b8baffc8537e2de1d849e8320ede2c32355bc71d5471ce58fa11e5feb808d over 23380 bytes and 274 lines, so §4.9's primary cmp-against-scratchpad proof was available and used rather than the digest fallback. `.agent/plan.md` at `4e6d5539` is byte-equal to PLANF021R3 at 42 lines against the 50-line cap. THE SETS HELD line-anchored at C2: 211 entries all DISTINCT, `Done: R-` 0, `Landed: ` 0, `Gate: R` keys 3 over 3 DISTINCT, `Gate: R3` 1, maximum registered id R-0648 — nothing was minted. THE DECISION HEADINGS went 110 to 112 with `^## DECISION F021 D1 ` and `^## DECISION F021 D2 ` each reading exactly 1 at C3, so the append landed once and not twice. THE THREE PAIRS each read FROM exactly 1 at the round base and FROM 0 with TO 1 at C4, and the feature file went 97 to 109 lines at a numstat of 21 insertions and 9 deletions. THE RANGE HELD: six commits, every one single-parent, the range path set EQUAL to the block's declared seven with the difference empty in both directions, and 0 paths beginning `apps/`, `packages/` or `tests/` — the property a specification round most needs to prove about itself. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: `tests/docs/` with `test_roadmap_index.py` at exit 0 and 325 passed, and the canary `tests/cli/test_golden_path.py` at exit 0 and 42 passed. THE DEFECT, RECORDED AS EVIDENCE AGAINST THE OPEN FINDING R-0631 AND NOT UNDER A NEW ID because §3 checklist item 30 requires the open set to be searched for the DEFECT before minting and that search returned R-0631 holding precisely this shape: the R3 block's G5 ordered a two-reader append proof whose reader (b) read "confirm the LAST unit equals the slice", and that clause is wrong in TWO independent ways, both of which the WORKER found and declared rather than quietly patching. FIRST it is unmeetable by construction for one of the two files it governs: DECIDE1 spans 10 blank-line units, so no single last unit can ever equal it, and the gate could not have passed for C3 under any correct execution. SECOND, and worse, it is vacuous where it does pass: a reader that inspects only the tail cannot see a mutation in the head, so for `.agent/live_review.md` reader (b) ACCEPTS an equal-length one-byte mutant of the FIRST paragraph while the true file is also accepted — the reviewer reproduced both readings directly, and reader (a) rejects that same mutant correctly. A two-reader gate whose second reader cannot fail on the region the negative control probes is a one-reader gate wearing a second reader's clothes, which is exactly what R-0631 registered one feature ago and exactly what this block reintroduced while citing R-0631 in the same sentence. THE COUNTER-MEASURE IS APPLIED IN THE BLOCK THIS ENTRY IS COMMITTED BY: its G5 states reader (b) SET-WISE — the new unit list equals the base unit list followed by the slice's own units, compared elementwise over the whole list rather than at the tail — which is the form the worker measured beside the broken clause and which rejects a first-paragraph mutant. That form is also what constraint 4 of this block measures on the slice's own bytes before emission, because the tail form's other failure was an unmeasured assumption that a slice is one unit. WHY R3 IS PASS AND NOT FAIL: the appends themselves are proved independently by reader (a) and by the reviewer's own byte-identical reconstruction, no gate was weakened, no expected value was adjusted, nothing false was recorded, and the round returned a correct result together with an honest account of the reviewer's error — which is the behaviour this workflow exists to produce.
<<<END RECORD3
