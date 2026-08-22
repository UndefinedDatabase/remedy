── STEP RECORD — F021 ──
Goal:        Discharge everything the RECORD owes before the ring is touched.
             R24 PASSED all nine gates under the reviewer's own re-measurement
             and its verdict is unrecorded. R-0656's rule still lives only in a
             finding body, where it has now failed to bind twice, so this round
             promotes it into docs/agents/planner_reviewer_prompt.md §3 as
             checklist item 32. And probing the `Gate: R` key sequence turned up
             a six-round-old hole: R18 PASSED, its verdict was authored in full
             as R19's RECORD19 slice, and R19 HALTED before the commit that
             would have applied it, so this ledger never received it. That text
             survives byte for byte on disk and this round appends it. NO CODE
             CHANGES — the ring moves to R26 by DECISION F021 D7, which RECORD25
             states in full.

Fortschritt: ~89 % (T002 — Uhr injiziert und Ankunftsstempel auf dem Transport-
             Event; es fehlen Ring, NowCard und Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 checklist item 32
             · C3 the R24 verdict, R-0659, the recovered R18 verdict and D7 · C4
             handback. THERE IS NO CODE COMMIT THIS ROUND: C4 IS THE HANDBACK,
             not a fifth change.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r25.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) ·
             `docs/agents/planner_reviewer_prompt.md` (C2) ·
             `.agent/live_review.md` (C3) · `.agent/handoff.md` (C4).
             Resolve any count in this block against that list. NO file under
             `apps/` or `tests/` is touched: if you find yourself editing one,
             STOP.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    both the docs commit and the ledger commit because the plan must be current
    before them (§3 checklist item 23), and PLANF021R25 describes the state this
    round ENDS in — including R-0659, which C3 mints — so it reads forward to
    commits this constraint fixes (§3 item 20, the R-0524 carve-out). ROUND BASE
    is `1ae04893` — resolve its full form with `git rev-parse` and report it —
    and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. Before this
    round: 221 open, maximum R-0658. RECORD25 registers R-0659 and records the
    R24 gate, so after C3: 222 open, maximum R-0659, next free R-0660. R-0656 is
    NOT resolved by the promotion and its paragraph is NOT edited: item 32 is the
    counter-measure landing, and the finding stays open for the paydown branch.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice and every pair half is
    quoted WITHOUT a trailing newline. A WHOLE-FILE write (PLANF021R25) is the
    slice PLUS one terminator. An APPEND to a record (RECORD25) is one newline,
    THEN the slice, then one terminator, so the target keeps exactly one — which
    means the diff of that commit ADDS the separator line first and then the
    slice's lines (R-0658). A PAIR is applied by replacing the FROM bytes with
    the TO bytes in place, adding no newline of its own.
 5. PAIR SHAPE, MEASURED NOT ASSERTED (§3 item 15). The reviewer ran the
    containment test on ITEM32 and its output was `TO contains FROM: true`, so
    ITEM32 is APPEND-SHAPED. The §4.9 FROM-0x count is therefore NOT ordered and
    must not be reported; the obligation is the one G5 states. The reviewer also
    measured FROM at exactly 1 occurrence in the target at the round base.
 6. THE LEDGER IS APPEND-ONLY. `acb688a9`, the R20 entry and every other older
    paragraph stay exactly as written. The R20 entry's sentence about `Gate: R19`
    is NOT corrected in place — R-0659 and the recovered verdict are new
    paragraphs that name it (R-0470), and the key `Gate: R19` must remain at 0
    occurrences in this file.
 7. ONE FILE, ONE PROPERTY, ONE COMMIT (R-0657). C2 gives
    `docs/agents/planner_reviewer_prompt.md` the ITEM32 pair and NOTHING else;
    C3 gives `.agent/live_review.md` the RECORD25 append and NOTHING else. Do not
    bundle them, and do not touch either file in any other commit.
 8. Run no formatter or linter that rewrites a file in place. Create and merge NO
    pull request: F021 is mid-feature and the ring round has not run. Push the
    branch after C4. Create NO worktree and run no destructive check.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 303
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 219 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next session. Report also, as the
     reading THIS round owes from the last, that the R24 handback commit
     `1ae04893` is single-parent and touches `.agent/handoff.md` alone at 33
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r25.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r25.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts and `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pair. Report how many whole texts, how many pairs and
     how many CONTENT lines that extractor printed, each as a number YOU
     measured and never as one this block predicts, and re-measure constraint 9's
     two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R25 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R25 at 49 lines, so the file is 49 lines and
     `wc -l` must read EXACTLY 49, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 49, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G5  THE ITEM32 PAIR at C2, which constraint 5 measured APPEND-SHAPED. Report,
     over `docs/agents/planner_reviewer_prompt.md`: FROM exactly 1 at the round
     base and exactly 1 at C2; TO 0 at the round base and exactly 1 at C2; and
     the ORDERED-EQUALITY reading, which for a pair carries no separator — the
     lines C2's diff ADDS are exactly the TO lines that are not FROM lines, IN
     ORDER, and its deletion count is 0. Report the added-line count and the
     TO-only count as the two numbers YOU measured. Report also that the file's
     checklist numbers run consecutively with no duplicate, that item 32 sits
     between item 31 and the "Why this is on disk and not a habit" paragraph, and
     the file's line count before and after.
 G6  THE LEDGER APPEND at C3, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C3 file, and the remainder is EXACTLY one newline
     plus RECORD25 plus one newline — report its sha256, byte and line counts,
     and the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C3 unit LIST equals the base list followed
     by RECORD25's own units, ELEMENTWISE over the whole list, not at the tail;
     report N at both points and RECORD25's unit count as the number YOU
     measured. NEGATIVE CONTROL: alter one printable byte of the C3 file's FIRST
     paragraph at equal length; BOTH readers must REJECT it and ACCEPT the true
     file. Name the offset and the change.
 G7  THE LEDGER SETS, line-anchored at line start, at the round base then C3:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R25`; `Gate: R19`; the MAXIMUM registered id.
     ONE id is minted and none resolved, so `- R-` reads 221 then 222 with both
     DISTINCT, the maximum R-0658 then R-0659, `Done: R-` and `Landed: ` 0 at
     both, `Gate: R` keys 23 then 24 both DISTINCT, `Gate: R25` 0 then 1, and
     `Gate: R19` 0 at BOTH — the recovered verdict is appended under this round's
     key and must NOT reintroduce the R19 key, which constraint 6 forbids.
     Report also that `- R-0656` occurs exactly ONCE at BOTH points: item 32 is
     its promotion, not a second registration.
 G8  THE OLDER ENTRIES ARE UNTOUCHED. Report that `git diff <round base>..C3 --
     .agent/live_review.md` contains NO deletion line: every changed line is an
     addition, which is what append-only means. State the count of deleted lines,
     which must be 0. Report also that the blob of `.agent/live_review.md` at
     `acb688a9` is a byte-exact PREFIX of the C3 file, which proves every entry
     from that commit onward survives exactly as written.
 G9  THE SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the REPOSITORY
     ROOT — a shell left elsewhere makes these exit 4 having run no test, which is
     vacuous and not green. Never run two at once. Report each one's exit code,
     the working directory, and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, and they READ
       `.agent/plan.md`, so they are the gate that C1 did not break it.
       `python3 -m pytest tests/docs/ -q -rf` — 295. This round's `Change:` list
       holds a `docs/` path, so the docs gate is owed; the reviewer measured it
       green at the round base and green again with this block applied.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 473, and it must be
       UNCHANGED: this round adds no test and touches no source, so any movement
       means a path outside `Change:` was written.
     NEITHER `npx tsc --noEmit` NOR `npm run test:unit` is ordered this round,
     because no file under `apps/` is touched; do not run them and do not report
     them.
 G10 RANGE, executed at C3 and covering the round base to C3 — NOT to C4, because
     C4 writes the file that must quote these gates and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C3 path set against the five non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` table (§3 item 28), any disagreement reported rather than
     reconciled; insertions under the 500 cap; `git ls-files .remedy-wt` 0; `git
     worktree list` ending with the primary checkout alone — NO worktree is
     created this round; and `gh pr list --state open --json number,headRefName`
     — expected EMPTY — with the statement that neither `gh pr create` nor `gh pr
     merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a SLICE OR PAIR
     LANDED IN — `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` and
     `.agent/live_review.md` — and covers EVERY marker prefix this block uses,
     which G3 names and you count for yourself: each file must read 0, and so
     must any line starting `<<<`. `.agent/authored/f021-r25.md` and
     `.agent/last_block.md` ARE the block and read nonzero BY CONSTRUCTION; they
     are not in scope.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE PER
            GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit cannot
            name its own SHA the role and reason go INSIDE the heading (R-0494).
            `## Next` states that THIS SESSION IS OVER and that the NEXT session
            begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); that
            rule 2 will find NO open pull request so rule 5 applies and F021
            continues on this branch; that R25's own verdict is UNRECORDED and
            the next round's ledger commit owes it; and that the next round is
            R26, THE RING ROUND, moved there by DECISION F021 D7 — `FeedRow`
            gains `receivedAtMs`, `feedRowOf` takes it, and `receiveBrainFrame`
            threads it from the transport event R23 stamped. State plainly that
            R26 is the first round to touch the ring, whose append placement
            DECISION F021 D5 governs, and that the reviewer's promotion debt is
            now DISCHARGED: R-0656's rule is §3 checklist item 32 as of C2, so a
            later block reads it from the checklist rather than from a finding
            body.

<<<SLICE PLANF021R25
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R25 discharges what the record owes before any new code, per DECISION F021 D7.
It promotes R-0656's rule into docs/agents/planner_reviewer_prompt.md §3 as
checklist item 32, records R24's verdict, and repairs a gap R19's halt left: R18
PASSED and its verdict was authored in full, but R19 stopped before the commit
that would have applied it. NO CODE CHANGES.

## Next Steps
1. R26 is THE RING ROUND, moved from R25 by DECISION F021 D7: `FeedRow` gains
   `receivedAtMs`, `feedRowOf` takes it, and `receiveBrainFrame` threads it from
   the transport event. First round to touch the ring, whose append placement
   DECISION F021 D5 governs.
2. R27: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
3. R28: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R29, the row click-jump, and T003's
   disabled steering input.
4. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` is the
  load-bearing gate of every round in this chain.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- R-0654 through R-0659 are ALL defects in the reviewer's own block text or
  record rather than in any worker's execution, and R-0656 recurred one round
  after it was registered. That is why R25 promotes it to the checklist.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay routed to a
  paydown branch.
<<<END PLANF021R25

<<<SLICE RECORD25
- R-0659 — Medium, A HALTED ROUND'S UNWRITTEN VERDICT WAS NEVER INHERITED, SO A PASSING ROUND'S RECORD HAS BEEN ABSENT FROM THIS APPEND-ONLY LEDGER SINCE R19. Raised by the reviewer against an earlier session of its own role, while probing the `Gate: R` key sequence before authoring R25. Every reviewed round records its verdict in this file, written by the NEXT round's ledger commit (DECISION F085 D9, docs/agents/planner_reviewer_prompt.md §4 item 13). R18's verdict was therefore owed by R19's C2, and the reviewer had authored it in full as that block's RECORD19 slice — but R19 HALTED at C1 on the gate contradiction R-0654 registers, so C2 was never made and the authored text never reached this file. R20 then wrote `Gate: R20 — the R19 entry` and accounted for the missing key in its own terms: "`Gate: R19` never appears in this ledger and never will, because R19's record is THIS entry." That sentence is true of R19's own record and silently wrong about R18's, which R19's C2 also owed and which no later round picked up — so the gap reads on the page as a considered absence. MEASURED AT `1ae04893`, not inferred: the line-anchored `Gate: R` keys are R1 through R18 and R20 through R24, R19 absent, and the string `R18 PASSED` occurs 0 times in the whole file, so the verdict is absent rather than merely misfiled. Medium: this ledger is the workflow's product, a reader searching it for R18 finds nothing, and the paragraph nearest the gap positively asserts the absence is by design — the R-0228 class §4 item 13 names, arriving through a HALT rather than through a round line. Not High because the verdict text survived intact on disk and is recovered below from those bytes rather than reconstructed from anyone's memory.

  FIX, applied by this entry: the recovered verdict is appended immediately below, taken from the byte-preserved authored slice. STANDING, BINDING THE REVIEWER — when a round HALTS before its ledger commit, the next block's ledger commit inherits BOTH records: the halted round's own verdict AND whatever that round's C2 was carrying for the round before it. Before authoring any block whose predecessor halted, the reviewer reads the `Gate: R` key sequence for gaps and resolves each gap to the round it actually covers; a gap that is genuinely correct by construction is written as a statement about THAT round and never as a general promise about a key, which is the form that hid this one. Recovery is always an APPEND: `acb688a9`, the R20 entry and every other older paragraph stay exactly as written (R-0470).

RECOVERED — THE R18 VERDICT, AUTHORED AT R19 AND LOST TO THAT ROUND'S HALT. The text after the colon below is the RECORD19 slice of the R19 block, byte-preserved in `.agent/authored/f021-r19.md` at `9d6b087a` at sha256 aa2198b737cb3505b177954d7b15f83133c83b9c2e2b583d3e8f3b8139b7c9dd, reproduced with its original opening `Gate: R19 — the R18 entry. ` removed and this heading in its place, because that key must not enter the ledger at R25 and the R20 entry has already ruled it will never appear. It is reviewer-authored text and no worker wrote it. BEFORE REPRODUCING IT THE REVIEWER RE-MEASURED FOUR OF ITS CLAIMS AT THE SHAs IT NAMES, AND ALL FOUR HOLD: `.agent/authored/f021-r18.md` at `824387a8` is sha256 907d24aff162f3aa88e53145319d222a582e4f1e6db60d47252901fee225a85f over 30318 bytes and 357 lines and `.agent/last_block.md` at `a451ac73` is byte-identical to it; `.agent/plan.md` at `2d4cc31b` reads 48 lines; `apps/ui/src/components/panels/AgentNowCard.tsx` at `674d1420` is 1859 bytes over 37 lines at sha256 f1e4e3fd72aa18402660e1f96933deca007d78543509b65ac9e71943247febee; and in that same blob the token `isActive` occurs 0 times while `newestActionRow` occurs twice. The claims the reviewer did NOT re-measure are reproduced as what they are — the R19 reviewer's readings, dated to the SHAs they name — and are not re-certified here. THE R18 VERDICT AS AUTHORED: R18 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT REGISTERS NO FINDING BECAUSE IT LEFT NO DEFECT. R18 retired R-0652: the NowCard's live badge went back to the agent's own `isRunning` flag, R16's detail line `liveAction ? liveAction.line : detail` untouched, and the repair is pinned by a contract whose red control RESTORES the latching form and fails on it. THE REPAIR IS MEASURED, NOT ASSERTED: at C3 the token `isActive` occurs 0 times in `AgentNowCard.tsx` while `newestActionRow` still occurs twice, so the ring still feeds the detail line and no longer feeds the badge. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f021-r18.md`, `.agent/authored/f021-r18.md` at `824387a8` and `.agent/last_block.md` at `a451ac73` are ALL FOUR byte-identical, counting the received bytes, at sha256 907d24aff162f3aa88e53145319d222a582e4f1e6db60d47252901fee225a85f over 30318 bytes and 357 lines. SLICES: 4 over 114 CONTENT lines, TOTAL 357 against DECISION F085 D6's 490 and PROSE 243 against D5's 400, both equal to that block's constraint 8. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `2d4cc31b` equals PLANF021R18 plus one terminating newline and NOT the bare slice, at 48 lines with `## Goal` and `## Next Steps` once each; `AgentNowCard.tsx` at `674d1420` equals ANCFILE2 plus one terminator and not the bare slice, at 1859 bytes / 37 lines / sha256 f1e4e3fd72aa18402660e1f96933deca007d78543509b65ac9e71943247febee against 1517 bytes and 33 lines at the round base where `git ls-tree` DOES list it, so it REPLACED a tracked file; the ledger append at `9b4b37e8` is the base blob plus one newline plus RECORD18 plus one newline, remainder sha256 a22bd1349739924a8e42817ae890cfdb4f24b5e950bef23aedcb90eec71c5c83 over 7898 bytes and 6 lines, units 240 to 243 ELEMENTWISE equal with RECORD18 exactly 3 units, and a negative control at offset 2 of the FIRST paragraph — the byte `L` set to `X` at equal length — that BOTH readers rejected while both accepted the true file; and the contract append needed NO pair, the base blob itself being the byte-exact prefix, remainder sha256 8ec6fe0866ae7fc87263f43289894e80dfa4f81e7b8dcedf389bd0e5f2ae23c8 over 1072 bytes and 25 lines — A DIGEST THE REVIEWER PREDICTED FROM ITS OWN DRY RUN BEFORE DELEGATING AND WHICH THE APPLIED BYTES REPRODUCED EXACTLY — with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 215 to 216 all DISTINCT at both points, maximum R-0652 to R-0653, `Done: R-` and `Landed: ` 0 at both — this ledger has no such line convention, which is why the R-0652 repair is stated in the Gate paragraph and R-0652's own paragraph is NOT edited, per R-0470 — `Gate: R` keys 17 to 18 both DISTINCT, `Gate: R18` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 461 at 457 passed and 4 skipped, the ordered rise of exactly 3 over the base's 458 that CONTRACTBADGE's three cases predict; the three state-reading suites 511; the canary 42; `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY; and `npm run test:unit` 14 files and 196 tests, UNCHANGED from the round base exactly as a round that adds no vitest case must read. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `674d1420`: green first at 31 passed, then with the badge line replaced by the latching form R16 had shipped — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 30 passed, the failure being `TestTheNowCardBadgeTracksTheAgent::test_the_badge_reads_the_running_flag` with the assertion "the live badge must track the agent, not the presence of a row". THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's six non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's tables, insertions 357, 238, 21, 6 and 32 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, and the reflog read BY OPERATION over this round's rows every one `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE MARKER SWEEP WAS LINE-ANCHORED: 0 anchored in every one of the four files a slice landed in, while `.agent/live_review.md` reads 2 under the containment reading. THE WORKER DECLARED NO DEVIATION and none was found; its handback's 93 lines against the 60-line cap are within the 100 AGENTS.md permits for more than five commits, with mandated content as the stated cause. WHY R18 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, both predicted digests were reproduced by the applied bytes, the red control fails in the reviewer's own worktree on the one named test, and the defect R-0652 named is measurably gone rather than merely described as fixed.

DECISION F021 D7 — THE RING ROUND MOVES FROM R25 TO R26 AND R25 BECOMES THE DISCHARGE ROUND. CHOSEN: spend this round on the record — promote R-0656's rule into §3 as checklist item 32, record R24, and register and repair the gap above — and give the ring a round with nothing else in it. WHY: R-0656 recurred in the block written immediately after the one registering it, which is exactly the ⚠️ condition docs/agents/planner_reviewer_prompt.md §2 defines, and §2's prescribed response to ⚠️ is that the reviewer APPLIES smaller steps rather than offering the operator a choice. R-0654 through R-0659 are all defects in the reviewer's own block text or record and none is a worker's execution error, so adding the ring's pairs to a block already carrying a checklist amendment and three ledger paragraphs is the change most likely to produce the next one. ALTERNATIVES CONSIDERED: folding the promotion into the ring round, which does fit the 490-line budget and was rejected because it puts a code change and three record obligations into one block against a ⚠️ momentum flag; and deferring the promotion until after the ring, rejected because the recurrence paragraph at `bdc242b4` states the reviewer owes it BEFORE R25 and a rule living only in a finding body has now demonstrably failed to bind twice. HOW TO REVERSE: any later relay may order the ring and the record in one block; D7 binds no round after R26, and DECISION F021 D5 still governs the ring's append placement whenever it runs.

Gate: R25 — the R24 entry. R24 PASSED ON EVERY ONE OF ITS NINE GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK. R24 was a record-only round: it recorded R23's verdict, registered R-0658 and wrote the R-0656 recurrence down beside the finding it belongs to instead of minting a second id, touching no file under `apps/` or `tests/`. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 346b25d8566baed4e44b42d1b08623012e51bec90c902972ebd152577c898d06 over 23071 bytes and 230 lines, the `.agent/authored/f021-r24.md` blob at `09702f93` and the `.agent/last_block.md` blob at `675c12bb` among them. SLICES: the reviewer's own marker-line extractor read the whole texts PLANF021R24 and RECORD24 over 54 CONTENT lines from the committed C0a blob, TOTAL 230 against DECISION F085 D6's 490 and PROSE 176 against D5's 400, both equal to that block's constraint 7, and no pair existed. THE PLAN WRITE HELD: `.agent/plan.md` at `946a888a` is byte-equal to PLANF021R24 plus one terminating newline and NOT to the bare slice, `wc -l` reads exactly 47 — the MEASURED value that block ordered — with `^## Goal$` 1 and `^## Next Steps$` 1. THE LEDGER APPEND HELD UNDER BOTH READERS: the base blob is a byte-exact PREFIX of the C2 file, the remainder is EXACTLY one newline plus RECORD24 plus one terminator at sha256 ea9ca6bdae0b5f3fba246f316ac543519e4c44aacb43a93a251c5c341c711e63 over 8153 bytes and 8 lines, the file 542933 B / 1150 L before and 551086 B / 1158 L after, units 256 to 260 ELEMENTWISE equal over the whole list with RECORD24 exactly 4 units, and the negative control at offset 4 of the FIRST paragraph — the byte `v` set to `X` at equal length — was REJECTED by both readers while both accepted the true file. THE SETS MOVED ONLY AS ORDERED: `- R-` 220 to 221 all DISTINCT at both points, maximum R-0657 to R-0658, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 22 to 23 both DISTINCT, `Gate: R24` 0 to 1, and `- R-0656` exactly ONCE at BOTH points, so the recurrence paragraph named that finding without minting it again. THE OLDER ENTRIES ARE UNTOUCHED: the C2 diff adds 8 lines and DELETES 0. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY from the repository root and counted BY PASSED PLUS SKIPPED: the three state-reading suites 511, the canary 42, and `tests/ui_contracts/` 469 passed plus 4 skipped = 473, UNCHANGED as a round touching no source must read; neither `npx tsc --noEmit` nor `npm run test:unit` was run, as that block ordered. THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's `Change:` list with both differences EMPTY, insertions 230, 152, 15, 8 and 33 every one under the 500 cap, `git show --numstat` and `git diff --numstat` agreeing cell by cell with every cell of the handback's `## Commits` tables — the handback declining to table its own commit's numbers rather than guessing them, which is what §3 checklist item 28 asks for — `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored in both files a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE ONE DECLARED DEVIATION IS AN HONEST NON-READING, NOT A DEFECT: that block's G1 ordered `git status --porcelain` after each of C0a, C0b, C1 and C2, the worker took it after C0b, C1 and C2 but not after C0a, and rather than reconstruct an unreachable state it said so and offered the nearest real evidence it had printed — the C0b pre-commit self-review showing exactly one dirty line, ` M .agent/last_block.md`. Reporting a missing reading as missing is the behaviour this workflow wants; the reviewer confirms the tree is clean at `1ae04893` now. WHY R24 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, both ledger readers accept the true file and reject a same-length mutant, every numeral the handback reports was re-derived independently rather than copied, and the round's only gap in evidence was declared instead of filled in.
<<<END RECORD25

<<<PAIR ITEM32 docs/agents/planner_reviewer_prompt.md
<<<FROM
      recurred in two consecutive rounds — the second of them authored by the
      reviewer who had registered it.
<<<TO
      recurred in two consecutive rounds — the second of them authored by the
      reviewer who had registered it.
  32. **A clause naming a KIND of the block's own parts states no COUNT of that
      kind.** Finding R-0656, and its recurrence one round later inside the very
      round that registered it. A gate or a constraint that names a CATEGORY of
      the block's own slices — the whole texts, the marker prefixes, the pairs —
      names that category and gives no numeral for it. The numeral is
      hand-counted while the extraction standing beside it is measured, so the
      two drift apart the moment the block is edited, and the hand-counted half
      is the one nobody re-reads. Where a count is genuinely owed, the block
      orders the WORKER to report the number IT measured rather than naming one
      itself. Items 11 and 16 are the same family and neither reaches this case:
      item 11 forbids the numeral in a CONVENTION PARAGRAPH and item 16 in a
      HEADING or any quantifying sentence, while a GATE's own text is neither.
      That is where R-0656 landed, and then landed again — R22's G3 ordered the
      extraction "for the two whole texts" over a block carrying three, and
      R23's G10 bound the marker sweep to "every one of the four marker
      prefixes" over the six that block's G3 names, as the recurrence paragraph
      committed at `bdc242b4` records — and in each the block's arithmetic was
      right while only the adjective was wrong, which is why no gate the block
      ordered could see it and the WORKER caught each. This is an item rather
      than a habit for the reason the list itself exists: R-0656's FIX clause
      stated exactly this counter-measure in a finding BODY, and the class
      recurred in the next block the reviewer wrote.
<<<ENDPAIR
