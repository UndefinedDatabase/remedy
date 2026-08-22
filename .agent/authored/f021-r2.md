── STEP INVENTORY — F021 ──
Goal:        Record the R1 verdict, then MEASURE the ground F021 builds on and
             write what was measured to `.agent/f021_inventory.md`: which module
             owns the F008 SSE subscription and how a second consumer would
             attach to it, where the event kinds a feed must humanize are
             DEFINED, and what the graph already exposes that a feed row could
             call to focus a node. This round MEASURES and RECORDS. It builds no
             feature code: nothing under `apps/ui/src/components/`, nothing under
             `packages/`, and no new test file.

Fortschritt: ~5 % (T001 offen · T002 offen · T003 offen; R1 hat das Feature
             beansprucht, diese Runde vermisst den Boden — Humanize-Katalog,
             Feed und NowCard werden ab R4 gebaut) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R1 verdict ·
             C3 the inventory document and the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r2.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/f021_inventory.md` (NEW, C3) and `.agent/handoff.md` (C3).
             That list is SIX paths; resolve any count in this block against this
             list rather than against a numeral written elsewhere.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (§3 checklist item
    23). C3 is last and carries the handback, so its own row is measured on
    staged content.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NOTHING. It writes no `- R-`
    entry, no `Done:` line and no `Landed:` line. The next free id is R-0649
    when the round ends, and R-0648 stays the maximum registered id.
 4. ONE APPEND AND ONE WHOLE-FILE REPLACEMENT. PLANF021R2 replaces
    `.agent/plan.md` at C1 in full. RECORD1 appends to `.agent/live_review.md`
    at C2, based on the ROUND BASE. There is NO FROM/TO pair this round, so no
    containment reading is owed and none is stated.
 5. THE INVENTORY IS YOURS TO WRITE, and it is the one artefact of this round
    that is not an authored slice. Nothing in it may be copied from the feature
    file, from this block, or from any `.agent/` document: every claim it makes
    is a reading you took from the SOURCE, and every claim NAMES the file it was
    read from and the symbol it was read at. Where you looked and found nothing,
    write that the thing is ABSENT and name where you looked — a deliberate
    absence is a finding this feature needs, and AGENTS.md's Code
    Discoverability section says text search cannot find code that does not
    exist. Prefer naming a SYMBOL plus its distinguishing text over a bare line
    number, because a line number dies to the next edit above it (§3 item 9).
 6. WHAT TO MEASURE, and nothing beyond it. Answer each of these five questions
    in its own section of `.agent/f021_inventory.md`, in this order:
      (a) THE SUBSCRIPTION. Which module opens the F008 SSE connection, what
          symbol does it export, and what does a consumer receive? Start from
          `apps/ui/src/api/useBrainStream.ts` and the `brainStream*` modules
          beside it in `apps/ui/src/api/`, and follow what they import. Report
          whether ONE connection is opened per mount or per consumer, quoting
          the construct you read it from. The feature file's Orchestrator brief
          rejects a second EventSource, so the question this section answers is
          whether a second consumer can attach WITHOUT opening one.
      (b) THE EVENT ENVELOPE. What fields does a single streamed event carry —
          in particular whether it carries a monotonic `seq`, a kind
          discriminator, and anything a row could resolve to a graph node?
          Report the TypeScript type or the runtime shape, and name the file.
      (c) THE EVENT KINDS. Where is the set of kinds DEFINED — one list, several,
          or nowhere? Look on BOTH sides of the seam: the client modules of (a),
          and the server that emits them, whose entry point is
          `packages/orchestration/ui_server.py`. Report the kinds you can
          enumerate from a definition, and state explicitly whether an
          authoritative single list exists. If there is no single list, say so —
          that absence decides how T001's coverage test can be written at all.
      (d) THE GRAPH's FOCUS SURFACE. What does the graph expose that a feed row
          could call to focus a node, and what identifies a node? Read
          `apps/ui/src/components/graph/ForceBrainGraph.tsx`,
          `apps/ui/src/components/graph/buildForceBrainModel.ts` and
          `apps/ui/src/components/graph/forceBrainTypes.ts`. Report the node-id
          type and whether any focus, select or highlight entry point EXISTS
          today; if none does, say ABSENT and name what would have to be added.
      (e) THE TEST CONVENTION. How are the existing frontend tests written and
          run — the runner, the file-naming pattern, and where they live? Read
          at least `apps/ui/src/api/brainStreamSession.test.ts` and
          `apps/ui/src/components/graph/buildForceBrainModel.test.ts`, and name
          the command that runs them. T001 ships a coverage test, so this
          section decides what that test looks like.
 7. NO PRODUCTION FILE IS EDITED. You may READ anything. Do not create, modify
    or delete a file under `apps/`, `packages/` or `tests/`, and do not run any
    formatter or linter that rewrites a file in place. The change set of
    constraint's `Change:` list is the whole of what this round writes.
 8. Do NOT create a pull request and do NOT merge one. F021 opens its pull
    request at closure, exactly as F009 did.
 9. Block size, measured on these final bytes: TOTAL 226 lines against DECISION
    F085 D6's 490, and PROSE — TOTAL minus the slice CONTENT lines — 181
    against DECISION F085 D5's 400. Marker lines count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again immediately before
     C3; the branch is `feature/f021-live-activity-feed`; and
     `git status --porcelain` prints 0 lines after each of C0a, C0b, C1 and C2.
     C3's own reading goes in the round report, because a commit cannot report
     the tree state that follows it (§3 checklist item 14).
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r2.md` at C0a, over
     `.agent/last_block.md` at C0b, and over the bytes you received are all
     equal. Write C0b FROM the committed C0a blob, never from the received text
     a second time, and report the digest with the byte and line counts.
 G3  SLICES: extract the slices from the COMMITTED C0a blob by their
     `<<<SLICE `/`<<<END ` marker LINES and report how many slices and how many
     CONTENT lines that extractor printed. Re-measure constraint 9's two
     numerals from that same blob and report both against their caps.
 G4  `.agent/plan.md` at C1 is byte-equal to PLANF021R2, proved with `cmp` at
     exit 0 against the slice extracted from the committed C0a blob, with a
     NEGATIVE CONTROL against RECORD1 that must exit 1. Report both exit codes,
     plus `^## Goal$` 1 and `^## Next Steps$` 1 and `wc -l` at most 50.
 G5  THE APPEND at C2, under TWO INDEPENDENT READERS. Reader (a): the round-base
     blob of `.agent/live_review.md` is a byte-exact PREFIX of the C2 file and
     the remainder is EXACTLY one newline plus RECORD1 — report the remainder's
     sha256, its byte count and its line count, and the file's byte and line
     counts before and after. Reader (b): split BOTH blobs on the blank line
     into units, report N at each point, and confirm the LAST unit at C2 equals
     RECORD1 while the base's last unit does not. NEGATIVE CONTROL: replace one
     printable byte of the FIRST paragraph of the C2 file at equal length and
     confirm BOTH readers REJECT that mutant while BOTH ACCEPT the true file —
     the control probes the HEAD of the region, not its tail (R-0631). Run the
     destructive half inside a disposable worktree under `.remedy-wt/`, never in
     the primary checkout, and remove and prune it before the handback.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then at C2:
     `- R-` entries and how many are DISTINCT; `Done: R-` lines; `Landed: `
     lines; `Gate: R` keys and how many are DISTINCT; `Gate: R2` occurrences;
     and the MAXIMUM registered id. Report each as a number at BOTH points.
     Nothing is minted this round, so the maximum id reads R-0648 at both.
 G7  THE INVENTORY IS NON-EMPTY AND ANSWERS ALL FIVE QUESTIONS: report
     `wc -l` of `.agent/f021_inventory.md` at C3 and confirm it carries one
     section per item of constraint 6, (a) through (e), each naming at least one
     file it was read from. Report, for each of the five, the count of distinct
     source paths it cites. This gate is a SHAPE check and cannot judge whether
     a reading is TRUE; the reviewer re-measures the readings themselves against
     the source, so do not treat a green here as agreement.
 G8  THE CONTRACT SUITES, run in the PRIMARY checkout and SERIALLY, never two
     pytest processes at once, after C3: `python3 -m pytest tests/ui_server/
     tests/orchestration/test_test_runner.py
     tests/regression/test_resource_safety.py -q -rf`. Report the exit code and
     the passed-plus-skipped total, counting BY PASSED PLUS SKIPPED because
     data-dependent skips in `tests/ui_server/` move the split run to run.
 G9  CANARY, run serially and after G8 has finished:
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`. Report the exit
     code and the total.
 G10 NO PRODUCTION FILE CHANGED: report that the range from the round base to C3
     holds 0 paths beginning `apps/`, `packages/` or `tests/`, and that
     `git status --porcelain` is empty. If your measurement work created any
     scratch file, it lives under `.remedy-wt/` and `git ls-files .remedy-wt`
     still reads 0.
 G11 RANGE, executed after C3 because it reads C3: the range from the round base
     to C3 lists exactly the paths of this block's `Change:` list, with the set
     difference EMPTY in both directions. Report both differences. Then: every
     commit single-parent; `git show --numstat` and `git diff --numstat`
     agreeing cell by cell with the handback's own `## Commits` table (§3
     checklist item 28); every insertion count under the 500 cap; leading
     `<<<SLICE ` and `<<<END ` reading 0 LINES in both files a slice lands in;
     and this round's reflog rows classified with `amend`, `rebase` and `cherry`
     each 0.
 G12 NO PULL REQUEST: report the output of `gh pr list --state open --json
     number,headRefName` and state that neither `gh pr create` nor
     `gh pr merge` was run.
 G13 THE HANDBACK carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, ONE LINE PER GATE with the transcripts
     kept in the round report rather than in the file (R-0582), and the block's
     `Fortschritt:` line verbatim across all three of its lines. Its own `wc -l`
     is reported against the 60-line cap a five-commit round allows, with a
     DECISION D15 line declaring any overage and naming the mandated content
     that caused it. Every commit heading in the `## Commits` table carries the
     commit's FULL subject; where a commit cannot name its own SHA, write the
     role and the reason INSIDE the heading rather than leaving the absence to
     be explained in a channel that ends with this session — that omission is
     finding R-0494, recorded against R1 in RECORD1 below.

Handback:   completion report + rewrite `.agent/handoff.md`.

<<<SLICE PLANF021R2
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps every Part E event kind to a plain line, a NowCard shows the newest
ACTION-class event with a recency-driven activity dot, and feed rows carry their
seq and click-jump to their node in the graph. DONE when the catalog covers every
Part E kind and an unknown kind renders an honest generic line rather than
vanishing, the feed renders fixture streams per the binding CSS, jump-to-node
focuses the right node, and the steering input renders DISABLED with its honest
tooltip until F030 lands.

## Current Step
R2 records the R1 verdict and then MEASURES the ground this feature builds on,
writing what it measured to `.agent/f021_inventory.md`: the F008 subscription and
whether a second consumer can attach without a second connection, the event
envelope, where the event kinds are defined, what the graph exposes for focusing
a node, and how the frontend tests are written and run. It builds nothing.

## Next Steps
1. R3 record R2 and rule the feed's shape as a DECISION on the measured ground:
   the humanize catalog's module and its coverage-test contract, the ACTION-class
   subset the NowCard reads, and the disabled-steering flag.
2. R4 onward the built work, in the T001 then T002 then T003 order the feature
   file's Task slicing names, starting with the catalog and its coverage test
   because the feature file's Orchestrator brief calls T001 headless-first.

## Risks
- The inventory may find NO single authoritative list of event kinds. T001's
  coverage test is specified against that list, so its absence is a design
  question for R3 rather than something a builder should improvise.
- F021 is a UI feature, so docs/ui/design_reference/ is binding for every visual
  surface and assets_spec.md is the asset authority; any visual deviation needs
  an assumption_log entry with a technical reason.
- One SSE subscription with client-side fan-out is an architecture line from the
  feature file's Orchestrator brief: a second EventSource is rejected.
- The open set carried into this record at R1 holds no code defect of F021;
  R-0403, R-0607, R-0608, R-0609, R-0611 and R-0613 stay routed to a paydown
  branch.
<<<END PLANF021R2

<<<SLICE RECORD1
Gate: R2 — the R1 entry. R1 PASSED. The reviewer re-executed every gate off disk and additionally rebuilt the round's one scripted artefact INDEPENDENTLY rather than checking the worker's arithmetic, which is the strongest reading this workflow has available and the reason this entry is short on caveats. TRANSPORT HELD IN ITS STRONGEST FORM, not the digest fallback: `.agent/authored/f021-r1.md` at `20de6de9`, `.agent/last_block.md` at `ae2e9ee0` and the bytes the reviewer EMITTED, still on disk at `.remedy-wt/f021-r1.md`, are all sha256 c8573f268d14618a3cc9c1b287f8ebe951423e38278a7101e9078a8f559ea242 over 29655 bytes and 350 lines, so §4.9's primary cmp-against-scratchpad proof was available and was used. The reviewer's own extraction out of the committed C0a blob printed 8 slices over 144 CONTENT lines, and constraint 9's numerals re-measure as 350 TOTAL and 206 PROSE, under DECISION F085 D6's 490 and D5's 400. THE APPLIED TEXTS ARE BYTE-EQUAL DISK TO DISK: `.agent/plan.md` at `407ee134` equals PLANF021R1 at 43 lines against the 50-line cap, `.agent/context.md` at `52b2158e` equals CONTEXTF021R1 at 50 lines, and `.agent/candidates.md` at `e064d226` equals CANDIDATES1 at 12 lines, each with a negative control that differs. THE LEDGER RESET IS THE REVIEWER'S OWN RECONSTRUCTION AND NOT A CHECK OF THE WORKER'S: the reviewer re-ran the constraint 6 algorithm over `.agent/live_review.md` at the round base `4548995d`, classified 213 FINDING, 3 RESOLUTION, 0 LANDED, 34 GATE and 4 HEADER units, carried the 210 FINDING units whose id carries no resolution, appended R0648 and GATE1 to LRHEAD, and the result is BYTE-IDENTICAL to the file committed at `02ce7aa7` at sha256 18822d6d39348b7a8e2bfe0b97234b20d029c24ed040627b11feb5472e72e404. Every one of the 210 carried findings is therefore verbatim, not merely counted. THE SETS AGREE under a second, line-anchored reader at C2 of that round: 211 entries all DISTINCT, `Done: R-` 0, `Landed: ` 0, `Gate: R` keys 1 over 1 DISTINCT, `Gate: R1` 1, maximum registered id R-0648 with R-0648 the only id present at C3 that was absent at the base, and R-0406, R-0634 and R-0637 absent from the new record exactly as intended. R-0585 and R-0493 are both still carried OPEN, which matters because R1 deliberately declined to mint ids for two defects those two findings already hold. THE ROADMAP CLAIM HELD, line-anchored, base then C5: `^- \[~\] ` 0 then 1, `^- \[~\] F021 — ` 0 then 1, `^- \[ \] F021 — ` 1 then 0, and `^- \[x\] ` 55 at BOTH points, so the claim moved one marker and disturbed no accepted row. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout after the round landed: `tests/ui_server/` with `test_test_runner.py`, `test_resource_safety.py` and `test_integrity_gate.py` at exit 0 and 527 passed; `tests/docs/` with `test_roadmap_index.py` at exit 0 and 325 passed; and the canary `tests/cli/test_golden_path.py` at exit 0 and 42 passed. THE RANGE HELD: seven commits, every one single-parent, the range path set EQUAL to the block's declared set with the difference empty in both directions and 0 paths beginning `packages/`, `apps/` or `tests/`, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's table at 350/0, 309/286, 34/27, 34/38, 23/101, 4/27 and C5's two rows, every insertion under the 500 cap, zero leading marker LINES in all five slice targets, `git ls-files .remedy-wt` 0, and the round's reflog rows classified with `amend`, `rebase` and `cherry` each 0. ONE DEFECT IS RECORDED, AND IT GOES TO R-0494 RATHER THAN TO A NEW ID, because §3 checklist item 30 requires the open set to be searched for the DEFECT before an id is minted and that search returned R-0494 holding exactly this class — a reading that exists only in a channel which dies with the session. The R1 handback's `## Commits` heading for its final commit reads `### C5 docs(roadmap): claim F021 in the roadmap ledger`, while that commit's real subject at `5179725f` is `docs(roadmap): claim F021 in the roadmap ledger and hand back R1`, four words longer; the handback names no SHA for it, which is correct and unavoidable under R-0149 since a commit cannot carry its own identifier, but it also gives no marker for the absence and no reason for the truncation, and the worker's explanation of both was delivered only in its final message. The F009 R34 handback shows the form that survives, writing `### C3 (SHA in the round report) ` followed by the FULL subject, so the absence is flagged on disk and the subject stays true. Nothing false was recorded and no number is wrong — the `+/-` cells of that row are exact and the reviewer verified them — which is why this is evidence against an OPEN Low finding rather than a new one, and why R1's verdict is PASS. The counter-measure is APPLIED in the block this entry is committed by, whose G13 requires every commit heading to carry the full subject and to state a missing SHA's reason inside the heading itself.
<<<END RECORD1
