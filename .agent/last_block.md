── STEP RECORD — F021 ──
Goal:        Close this session's record honestly. R20 PASSED all fifteen gates
             under the reviewer's own re-measurement, and its own verdict is
             still unrecorded. R20 also left a FALSE NUMERAL in the append-only
             ledger: RECORD20's FIX paragraph, committed at `acb688a9`, says the
             R20 block's G4 orders 47 when it orders 43. The reviewer corrected
             G4's numerals after drafting that paragraph and did not sweep the
             prose that quoted them. This round records the verdict, registers
             that defect, and CORRECTS the numeral the only way an append-only
             record permits — in a new entry, leaving `acb688a9` untouched
             (R-0470). NO CODE CHANGES. This is the session's last round.

Fortschritt: ~87 % (T002 — Feed, NowCard, Scroll- und Recency-Regel stehen als
             reine Funktionen; es fehlen nur noch ihre Verdrahtung und T003)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R20 verdict,
             R-0655 and the numeral correction · C3 handback. THERE IS NO CODE
             COMMIT THIS ROUND: C3 IS THE HANDBACK, not a fourth change.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r21.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3).
             Resolve any count in this block against that list. NO file under
             `apps/` or `tests/` is touched: if you find yourself editing one,
             STOP.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger commit because the plan must be current before it (§3 checklist item
    23). ROUND BASE is `a2740317` — resolve its full form with `git rev-parse`
    and report it — and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. Before this
    round: 217 open, maximum R-0654. RECORD21 registers R-0655 and records the
    R20 gate, so after C2: 218 open, maximum R-0655, next free R-0656. R-0655 is
    NEW rather than filed against R-0654 because §3 checklist item 30's search of
    the open set for the DEFECT found no entry about a CORRECTION that failed to
    sweep the prose quoting the corrected value; R-0654 is about two clauses of
    one gate contradicting each other, which is a different door.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R21) is the slice PLUS one
    terminator. An APPEND (RECORD21) is one newline, then the slice, then one
    terminator, so the target keeps exactly one. THIS ROUND HAS NO FROM/TO PAIR
    AND NO CODE SLICE.
 5. THE LEDGER IS APPEND-ONLY AND `acb688a9` IS NOT EDITED. The false numeral
    stays where it was written; RECORD21 states the correction. R-0470 settled
    that closing the distance between a claim and the bytes by editing the bytes
    is how a record stops being one. If you find yourself opening an older entry,
    STOP.
 6. Run no formatter or linter that rewrites a file in place. Create and merge NO
    pull request: F021 is mid-feature and its wiring round has not run. Push the
    branch after C3.
 7. Block size, measured on these final bytes AFTER the last edit: TOTAL 227
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 179 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C3; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1 and C2. C3's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next session. Report also, as the
     reading THIS round owes from the last, that the R20 handback commit
     `a2740317` is single-parent and touches `.agent/handoff.md` alone at 57
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r21.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r21.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 7's two numerals from that
     same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R21 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R21 at 43 lines, so the file is 43 lines and
     `wc -l` must read EXACTLY 43, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 43, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus RECORD21
     plus one newline — report its sha256, byte and line counts, and the file's
     byte and line counts before and after. Reader (b), SET-WISE: strip the one
     trailing terminator from BOTH blobs, split each on the blank line into units,
     and confirm the C2 unit LIST equals the base list followed by RECORD21's own
     units, ELEMENTWISE over the whole list, not at the tail; report N at both
     points and RECORD21's unit count, measured by the reviewer as THREE — the
     finding, its FIX line and the gate entry. NEGATIVE CONTROL: alter one
     printable byte of the C2 file's FIRST paragraph at equal length; BOTH readers
     must REJECT it and ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R21`; the MAXIMUM registered id. ONE id is
     minted and none resolved, so `- R-` reads 217 then 218 with both DISTINCT,
     the maximum R-0654 then R-0655, `Done: R-` and `Landed: ` 0 at both,
     `Gate: R` keys 19 then 20 both DISTINCT, `Gate: R21` 0 then 1.
 G7  THE CORRECTION IS PRESENT AND THE OLD ENTRY IS UNTOUCHED. Report, over the
     C2 file: the string `EXACTLY 47` occurs exactly TWICE — the original in
     RECORD20 and the VERBATIM QUOTATION of it inside R-0655, which the reviewer
     measured before ordering this clause — and the string `EXACTLY 43` occurs
     exactly ONCE, in RECORD21's FIX line.
     Then report that `git diff <round base>..C2 -- .agent/live_review.md`
     contains NO deletion line: every changed line is an addition, which is what
     append-only means and what proves `acb688a9` was not edited. State the count
     of deleted lines, which must be 0.
 G8  THE SUITES THAT READ `.agent/plan.md`, at C2 in the PRIMARY checkout,
     SERIALLY, from the REPOSITORY ROOT — a shell left elsewhere makes these exit
     4 having run no test, which is vacuous and not green. Never run two at once.
     Report each one's exit code, the working directory, and the total, counting
     BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, and they READ
       `.agent/plan.md`, so they are the gate that C1 did not break it.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 465, and it must be
       UNCHANGED: this round adds no test and touches no source, so any movement
       means a path outside `Change:` was written.
     No docs gate is owed: the `Change:` list holds no `docs/` path. NEITHER
     `npx tsc --noEmit` NOR `npm run test:unit` is ordered this round, because no
     file under `apps/` is touched; do not run them and do not report them.
 G9  RANGE, executed at C2 and covering the round base to C2 — NOT to C3, because
     C3 writes the file that must quote this gate and §3 checklist item 31 forbids
     ordering a reading the quoting artefact cannot hold. Report: the base-to-C2
     path set against the four non-handoff paths of `Change:`, the difference
     EMPTY both ways; every commit single-parent; `git show --numstat` and `git
     diff --numstat` agreeing cell by cell with the handback's `## Commits` table
     (§3 item 28), any disagreement reported rather than reconciled; insertions
     under the 500 cap; `git ls-files .remedy-wt` 0; `git worktree list` ending
     with the primary checkout alone — NO worktree is created this round, since
     nothing is red-proved; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh pr
     create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a SLICE LANDED IN
     — `.agent/plan.md` and `.agent/live_review.md`, each of which must read 0.
     `.agent/authored/f021-r21.md` and `.agent/last_block.md` ARE the block and
     read nonzero BY CONSTRUCTION; they are not in scope, exactly as R20's worker
     read it.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2 and C3, the round base SHA, ONE LINE PER
            GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report its
            own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit cannot
            name its own SHA the role and reason go INSIDE the heading (R-0494).
            `## Next` states that THIS SESSION IS OVER and that the NEXT session
            begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347); that
            rule 2 will find NO open pull request so rule 5 applies and F021
            continues on this branch; that R21's own verdict is UNRECORDED and
            the next round's C2 owes it; and that the next round is R22, THE
            WIRING ROUND — `recency.ts` becomes the ONE liveness source for the
            NowCard's badge AND its new dot, and `feedScroll.ts` drives the feed's
            scroll container and the new-rows pill component_spec.md line 86
            binds. State plainly that R22 is the largest component change of this
            feature, that it is the first round to need CSS, and that
            `docs/ui/design_reference/assets_spec.md` is the asset authority for
            any new dot or pill styling.

<<<SLICE PLANF021R21
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
R21 records R20, which PASSED all fifteen gates, registers R-0655 and corrects
in a NEW entry the false numeral R20 left in the ledger. No code changes: the
four pure rules are built and the wiring round has not begun.

## Next Steps
1. R22 is THE WIRING ROUND and the largest component change of this feature:
   `recency.ts` becomes the ONE liveness source for the NowCard's badge AND its
   new dot, and `feedScroll.ts` drives the feed's scroll container and the
   new-rows pill component_spec.md line 86 binds. It is the first round needing
   CSS, so `docs/ui/design_reference/assets_spec.md` is the asset authority.
2. R23 gives each row its click-jump to the node, then T003: the disabled
   steering input with its honest tooltip.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. R22 wires four rules at once and is where that
  gap bites hardest; consider splitting it if its block exceeds the cap.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A gate that names a line count states the MEASURED value, never a bound the
  slice was not checked against (R-0654); and a numeral corrected in one place
  is swept everywhere the block quotes it (R-0655).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654 and R-0655 stay routed to a
  paydown branch.
<<<END PLANF021R21

<<<SLICE RECORD21
- R-0655 — Low, A NUMERAL WAS CORRECTED IN THE GATE THAT ORDERS IT AND NOT IN THE PROSE THAT QUOTES IT, SO THE LEDGER ENTRY CONDEMNING UNMEASURED NUMERALS CONTAINS ONE. Raised by the reviewer against its own R20 block, and caught by that round's WORKER, which reported it in the handback rather than silently fixing a slice constraint 1 forbade it to touch. While drafting R20 the reviewer wrote both G4 and the R-0654 FIX paragraph against an ESTIMATED plan-slice length of 47 lines, then measured the slice at 43, corrected G4's three occurrences, and did not sweep the FIX paragraph. So `acb688a9` now carries "this block's G4 says the slice is 47 lines, so the file is 47, and orders `wc -l` to read EXACTLY 47" while G4 as committed at `3df59508` orders 43 and the file at `476ad9e3` measures 43. The claim is false about a block in the same commit range, inside the very finding that exists to stop unmeasured numerals reaching gates. This is the R-0486 class — the correction carries the old fact — arriving in ledger prose instead of in a gate. Low and not Medium: no gate reads that sentence, every gate R20 ordered was satisfiable and satisfied, the reviewer re-measured all fifteen independently, and the correction below makes the record self-consistent for any reader who reads the ledger in order, which is the only order it can be read in. But it is a false sentence in an append-only record, and the record is the product.

  FIX, applied by this entry: THE CORRECTION IS THAT R20's G4 ORDERS EXACTLY 43, THE PLANF021R20 SLICE MEASURES 43 LINES, AND `.agent/plan.md` AT `476ad9e3` READS 43 — the "47" in RECORD20's FIX paragraph is wrong in all three of its occurrences and is superseded here. `acb688a9` is deliberately NOT edited (R-0470). Standing, binding the reviewer: when a measured value replaces an estimated one, sweep every occurrence in the block INCLUDING slice bodies, and re-measure the replacement text rather than the original — the correction is where the next wrong number lands.

Gate: R21 — the R20 entry. R20 PASSED ON EVERY ONE OF ITS FIFTEEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES THE ONE FINDING REGISTERED IMMEDIATELY ABOVE. R20 built the activity dot's rule as a PURE function in `apps/ui/src/api/recency.ts` — `none` before anything has acted, `fresh` inside the fresh window, `fading` until the quiet window closes, `idle` after it, and `fresh` rather than `idle` when the clocks disagree, because under skew the honest failure is to over-report life and never to declare a working agent dead — with its vitest and a source contract, wiring nothing, and it redid the work R19 halted before reaching. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 3de736c0f4a30fb168d1e70160d180eede89dfe45c1fe55c7549146f1f51b6e3 over 30944 bytes and 459 lines. SLICES: 7 over 183 CONTENT lines, TOTAL 459 against DECISION F085 D6's 490 and PROSE 276 against D5's 400, both equal to that block's constraint 9. THE REPAIRED GATE WORKED: R19 died because its G4 ordered `cmp` against a 51-line slice AND `wc -l` at most 50; R20's G4 named the MEASURED value instead, the extractor read PLANF021R20 at 43, `.agent/plan.md` at `476ad9e3` is byte-equal to that slice plus one terminating newline and NOT to the bare slice, and `wc -l` read exactly 43 — satisfiable and satisfied. EVERY OTHER SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `recency.ts` at `a71e5452` is 2012 bytes / 44 lines / sha256 14f990bd090c7c858bb51ba6222203fd32b5811f53eae086c69c2d70775e2d49 and `recency.test.ts` 1643 bytes / 58 lines / sha256 d7a227d3dd4fe4734f5aa8b12bb52cdf4ac83f876a5820d5382cdc7503a93913, each equal to its slice plus one terminator and not the bare slice, and BOTH ABSENT from `git ls-tree` at the round base, so the round created them; the ledger append at `acb688a9` is the base blob plus one newline plus RECORD20 plus one newline, remainder sha256 b0b8be5827568aac5c63adec4eb9aa84c6d2c62e10359b980a913a5059c89a71 over 4812 bytes and 6 lines, units 243 to 246 ELEMENTWISE equal with RECORD20 exactly 3 units, and a negative control at offset 2 of the FIRST paragraph that BOTH readers rejected while both accepted the true file; and the contract append is the CONTRACTPATHS5-substituted base blob (13067 bytes, from 13034 B / 294 L) plus one newline plus CONTRACTRECENCY plus one newline, remainder sha256 e1212600fdfe595b3c02e3bacb1d3fa777ec9523ad158fd11e55ce9417ee5a88 over 1307 bytes and 31 lines — A DIGEST THE REVIEWER PREDICTED FROM ITS OWN DRY RUN BEFORE DELEGATING AND WHICH THE APPLIED BYTES REPRODUCED EXACTLY — with EXACTLY TWO blank lines before the new top-level class, counted rather than delegated to a linter that does not evaluate E301-E306 outside preview. THE ONE PAIR BEHAVED BY SHAPE: CONTRACTPATHS5 is append-shaped and read FROM 1 / TO 0 at the round base and FROM 1 / TO 1 at C3. THE LEDGER MOVED ONLY AS ORDERED: `- R-` 216 to 217 all DISTINCT at both points, maximum R-0653 to R-0654, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 18 to 19 both DISTINCT, `Gate: R20` 0 to 1, and `Gate: R19` 0 at BOTH points — R19 halted before its C2, so it has no gate entry of its own and never will. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: `tests/ui_contracts/` 465, the ordered rise of exactly 4 over the base's 461 that CONTRACTRECENCY's four cases predict; the three state-reading suites 511; the canary 42; `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY; and `npm run test:unit` 15 files and 207 tests, the base's 14 and 196 plus one file and the ELEVEN cases an ANCHORED `it(` scan had counted before delegation. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `a71e5452`: green first at 35 passed, then with `    return "none";` replaced by `    return "idle";` — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 34 passed, the failure being `TestTheRecencyRuleIsPureAndHeadless::test_the_pre_stream_state_is_not_idle`. THAT CONTRACT ASSERTS THE WHOLE RETURN STATEMENT AND NOT THE BARE TOKEN `"none"` FOR A MEASURED REASON: the token also appears in the `RecencyLevel` union, so the reviewer verified on its dry run that a looser guard SURVIVES this exact mutation, and tightened the assertion before delegating. THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, `git show --numstat` and `git diff --numstat` agreeing cell by cell with the handback's tables, insertions 459, 98, 21, 6 and 134 every one under the 500 cap, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the LINE-ANCHORED marker sweep 0 in every file a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE WORKER DECLARED NO SEQUENCE DEVIATION AND EARNED CREDIT FOR THE FINDING ABOVE: it applied a slice it could see was wrong, byte for byte, because constraint 1 told it to, and reported the defect instead — the same discipline R19's worker showed when it halted rather than choose between two contradictory clauses. WHY R20 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself, the append digest matched a prediction made before delegation, the red control fails in the reviewer's own worktree on the one named test, and the gate that killed R19 was repaired by measurement and then held.
<<<END RECORD21
