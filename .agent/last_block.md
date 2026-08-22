── STEP RECORD — F021 ──
Goal:        Close this session's record honestly. R23 PASSED all ten gates
             under the reviewer's own re-measurement, and its verdict is still
             unrecorded. R23's worker also declared two more defects in the
             REVIEWER's block text: one new — an ordered-equality clause that
             ignores the append convention's own separator newline — and one
             that is R-0656 recurring in the very next block it was registered
             in. This round records the verdict, registers the new defect, and
             writes the recurrence down beside the finding it belongs to rather
             than minting a second id for one door (§3 checklist item 30). NO
             CODE CHANGES. This is the session's last round.

Fortschritt: ~89 % (T002 — Uhr injiziert und Ankunftsstempel auf dem Transport-
             Event; es fehlen Ring, NowCard und Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R23 verdict,
             R-0658 and the R-0656 recurrence · C3 handback. THERE IS NO CODE
             COMMIT THIS ROUND: C3 IS THE HANDBACK, not a fourth change.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r24.md` (NEW, C0a) · `.agent/last_block.md`
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
    23). ROUND BASE is `c76f90ac` — resolve its full form with `git rev-parse`
    and report it — and it is the commit every "round base" in this block names.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES NONE. Before this
    round: 220 open, maximum R-0657. RECORD24 registers R-0658 and records the
    R23 gate, so after C2: 221 open, maximum R-0658, next free R-0659. The
    marker-count recurrence gets NO id of its own: §3 checklist item 30 rules
    that an OPEN finding already describing the defect takes the new evidence,
    and R-0656 is that finding.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R24) is the slice PLUS one
    terminator. An APPEND (RECORD24) is one newline, then the slice, then one
    terminator, so the target keeps exactly one. THIS ROUND HAS NO FROM/TO PAIR
    AND NO CODE SLICE.
 5. THE LEDGER IS APPEND-ONLY. `acb688a9` and every other older entry stay
    exactly as written; R-0656 is NOT edited to carry its own recurrence, which
    is why the recurrence is a new paragraph naming it (R-0470).
 6. Run no formatter or linter that rewrites a file in place. Create and merge
    NO pull request: F021 is mid-feature and the ring round has not run. Push
    the branch after C3. Create NO worktree and run no destructive check.
 7. Block size, measured on these final bytes AFTER the last edit: TOTAL 230
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 176 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C3; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1 and C2. C3's own reading is ordered
     NOWHERE — §3 item 31 leaves it to the next session. Report also, as the
     reading THIS round owes from the last, that the R23 handback commit
     `c76f90ac` is single-parent and touches `.agent/handoff.md` alone at 55
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r24.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r24.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES. Report how many whole-text slices and how many
     CONTENT lines that extractor printed — state each as the number YOU
     measured, never as one this block predicts — and re-measure constraint 7's
     two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R24 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R24 at 47 lines, so the file is 47 lines and
     `wc -l` must read EXACTLY 47, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 47, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, and the remainder is EXACTLY one newline
     plus RECORD24 plus one newline — report its sha256, byte and line counts,
     and the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list followed
     by RECORD24's own units, ELEMENTWISE over the whole list, not at the tail;
     report N at both points and RECORD24's unit count as the number YOU
     measured. NEGATIVE CONTROL: alter one printable byte of the C2 file's FIRST
     paragraph at equal length; BOTH readers must REJECT it and ACCEPT the true
     file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R24`; the MAXIMUM registered id. ONE id is
     minted and none resolved, so `- R-` reads 220 then 221 with both DISTINCT,
     the maximum R-0657 then R-0658, `Done: R-` and `Landed: ` 0 at both,
     `Gate: R` keys 22 then 23 both DISTINCT, `Gate: R24` 0 then 1.
     Report also that `- R-0656` occurs exactly ONCE at BOTH points: the
     recurrence paragraph names that finding and must not have minted it again.
 G7  THE OLDER ENTRIES ARE UNTOUCHED. Report that `git diff <round base>..C2 --
     .agent/live_review.md` contains NO deletion line: every changed line is an
     addition, which is what append-only means. State the count of deleted
     lines, which must be 0. Report also that the blob of `.agent/live_review.md`
     at `a8215a65` — the commit that registered R-0656 — is a byte-exact PREFIX
     of the C2 file, which proves that entry survives exactly as written.
 G8  THE SUITES THAT READ `.agent/plan.md`, at C2 in the PRIMARY checkout,
     SERIALLY, from the REPOSITORY ROOT — a shell left elsewhere makes these exit
     4 having run no test, which is vacuous and not green. Never run two at once.
     Report each one's exit code, the working directory, and the total, counting
     BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, and they READ
       `.agent/plan.md`, so they are the gate that C1 did not break it.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 473, and it must be
       UNCHANGED: this round adds no test and touches no source, so any movement
       means a path outside `Change:` was written.
     No docs gate is owed: the `Change:` list holds no `docs/` path. NEITHER
     `npx tsc --noEmit` NOR `npm run test:unit` is ordered this round, because no
     file under `apps/` is touched; do not run them and do not report them.
 G9  RANGE, executed at C2 and covering the round base to C2 — NOT to C3, because
     C3 writes the file that must quote this gate and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C2 path set against the four non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` table (§3 item 28), any disagreement reported rather than
     reconciled; insertions under the 500 cap; `git ls-files .remedy-wt` 0; `git
     worktree list` ending with the primary checkout alone — NO worktree is
     created this round; and `gh pr list --state open --json number,headRefName`
     — expected EMPTY — with the statement that neither `gh pr create` nor `gh pr
     merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a SLICE LANDED IN
     — `.agent/plan.md` and `.agent/live_review.md` — and covers EVERY marker
     prefix this block uses, which G3 names and you count for yourself: each file
     must read 0. `.agent/authored/f021-r24.md` and `.agent/last_block.md` ARE
     the block and read nonzero BY CONSTRUCTION; they are not in scope.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2 and C3, the round base SHA, ONE LINE PER
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
            continues on this branch; that R24's own verdict is UNRECORDED and
            the next round's C2 owes it; and that the next round is R25, THE RING
            ROUND — `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it, and
            `receiveBrainFrame` threads it from the transport event R23 stamped.
            State plainly that R25 is the first round to touch the ring, whose
            append placement DECISION F021 D5 governs, and that the reviewer's
            standing obligation before R25 is to promote R-0656's rule into
            docs/agents/planner_reviewer_prompt.md §3, because a rule that lives
            only in a finding body is a rule the next block does not read.

<<<SLICE PLANF021R24
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
R24 records R23, which PASSED all ten gates, registers R-0658 and writes down a
recurrence of R-0656 beside that finding rather than minting a second id. No
code changes: the clock is injected and every transport frame now carries its
arrival instant, but nothing consumes the stamp yet.

## Next Steps
1. R25 is THE RING ROUND: `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it,
   and `receiveBrainFrame` threads it from the transport event. First round to
   touch the ring, whose append placement DECISION F021 D5 governs.
2. R26: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
3. R27: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R28, the row click-jump, and T003's
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
- The reviewer's block text is where this feature's last four findings came
  from, all caught by workers: R-0654 through R-0658. Before R25 the reviewer
  promotes R-0656's rule into planner_reviewer_prompt.md §3.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653 through R-0658 stay routed to a
  paydown branch.
<<<END PLANF021R24

<<<SLICE RECORD24
- R-0658 — Low, AN ORDERED-EQUALITY GATE COUNTED THE SLICE'S LINES AND FORGOT THE SEPARATOR ITS OWN APPEND CONVENTION ADDS. Raised by the reviewer against its own R23 block, and caught by that round's WORKER, which measured both readings and declared the difference rather than picking whichever made the gate pass. R23's G5 ordered that "the lines C4's diff ADDS to that file are exactly the slice's lines IN ORDER", while constraint 5 of the same block defines an append to a record as one newline, THEN the slice, then one terminator. So the diff necessarily adds the separator line as well: measured at `3cd2eeeb`, the diff adds 35 lines while CONTRACTSTAMP is 34, `added[0]` is the empty separator and `added[1:]` equals the slice elementwise and in order. The two clauses of one block therefore contradict each other by exactly one line, and no round can satisfy both as written. The applied bytes were never in doubt — the reviewer rebuilt the whole C4 file independently from its own slice bytes and it matched the committed blob at sha256 4b32d1d84dad72053c96e208040705fa234c7bd6c5fc377021306b99de0a80ef, with 0 deleted lines and exactly two blank lines before the new class — so this cost a declared deviation and nothing else. Low: the property was met, the discrepancy is one line and mechanically explained, and the worker reported both numbers. It is a finding because §4.9's ordered-equality reading is the strongest proof this workflow has for a code append, and a gate that cannot be satisfied exactly is one a later round will be tempted to satisfy approximately.

  FIX, applied by this entry: STANDING, BINDING THE REVIEWER — an ordered-equality clause states the added-line list as the CONVENTION produces it: the separator line, then the slice's lines in order. Write "the lines the diff ADDS are the append convention's separator followed by the slice's lines IN ORDER", and where the count matters, order the WORKER to report the two numbers it measured rather than naming either. The clause and the convention paragraph are read against each other before emission, which is the §3 checklist item 18 discipline applied to two clauses of the reviewer's own block instead of to a recipe and its property.

RECURRENCE of R-0656, which stays OPEN and is NOT edited: the defect it registers reappeared in the very next block, in the round that registered it. R23's G10 bound the marker sweep to "every one of the four marker prefixes" while that block's G3 names six — `<<<SLICE `, `<<<END `, `<<<PAIR `, `<<<FROM`, `<<<TO` and `<<<ENDPAIR` — because R23's pairs are FROM/TO rewrites where R22's were ANCHOR/ADD appends, and the numeral was carried over from the earlier shape without being re-counted. R23's worker refused to guess the partition, swept all six line-anchored plus any `^<<<`, and reported 0 in all eight files, so the sweep was strictly wider than ordered and nothing escaped it. NO NEW ID IS MINTED: §3 checklist item 30 rules that an open finding describing the defect takes the new evidence, and R-0656 describes exactly this — a hand-counted numeral about the block's own parts standing beside a correct measurement. What this recurrence proves is that R-0656's FIX clause, written as finding prose, bound nothing one round later. The counter-measure is promotion: the reviewer owes an amendment putting that rule into docs/agents/planner_reviewer_prompt.md §3 before R25, because a rule that lives only in a finding body is a rule the next block does not read. Recorded here rather than in R-0656 itself because this ledger is append-only and the older entry is the record (R-0470).

Gate: R24 — the R23 entry. R23 PASSED ON EVERY ONE OF ITS TEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES BOTH ENTRIES ABOVE. R23 put the arrival stamp on the TRANSPORT EVENT: `BrainStreamEvent`'s frame member gained `receivedAtMs`, `createBrainStreamHost`'s `tell` dispatches `receivedAtMs: deps.now()` from the clock R22 injected, and the driver carries the number without ever reading a clock, so it stays the pure reducer DECISION F021 D5 depends on. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 f3b960d05beb4a87807e72037dd0514aeb6605567493951c100d2450b9329b40 over 28934 bytes and 357 lines. SLICES: the reviewer's own extractor read 6 pairs and 3 whole-text slices over 127 CONTENT lines from the committed C0a blob, TOTAL 357 against DECISION F085 D6's 490 and PROSE 230 against D5's 400, both equal to that block's constraint 9. ALL SIX PAIRS ARE REWRITES AND BEHAVED AS ONE: every FROM occurred exactly once in its target at the round base, and at `ba396370` every FROM reads 0 and every TO reads 1 — the shape opposite to R22's twelve appends, measured for this block rather than carried over. THE PLAN WRITE HELD: `.agent/plan.md` at `fbb5a5ee` is byte-equal to PLANF021R23 plus one terminating newline and NOT to the bare slice, `wc -l` reads exactly 47 — the MEASURED value that block ordered — with `^## Goal$` 1 and `^## Next Steps$` 1. THE CONTRACT APPEND HELD AS ORDERED EQUALITY, THE READING R22 COULD NOT TAKE: because R23's constraint 8 gave C4 the append ALONE, the C3 blob IS a byte-exact prefix of the C4 file, remainder sha256 db6d3ede over 1531 bytes and 35 lines, the file 16125 B / 363 L before and 17656 B / 398 L after, 0 deleted lines, and exactly two blank lines before the new top-level class counted rather than delegated to a linter that is preview-blind to E301-E306. THE LEDGER APPEND HELD UNDER BOTH READERS: base blob a byte-exact prefix, remainder sha256 5ea20810 over 8533 bytes and 10 lines, the file 534400 B / 1140 L before and 542933 B / 1150 L after, units 251 to 256 ELEMENTWISE equal with RECORD23 exactly 5 units, and a negative control at offset 4 of the FIRST paragraph rejected by BOTH readers while both accepted the true file. THE SETS MOVED ONLY AS ORDERED: `- R-` 218 to 220 all DISTINCT at both points, maximum R-0655 to R-0657, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 21 to 22 both DISTINCT, `Gate: R23` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially: `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY; `npm run test:unit` 15 files and 209 tests, UNCHANGED as ordered because this round added no vitest case; `tests/ui_contracts/` 469 passed plus 4 skipped = 473, the base's 469 plus the four CONTRACTSTAMP adds; the three state-reading suites 511; the canary 42. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `c76f90ac`: green first at 43 passed, then with `    dispatch({ kind: "frame", frame, receivedAtMs: deps.now() });` replaced by the same line stamping a literal 0 — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 1 failed and 42 passed, the failure being `TestEveryFrameIsStampedOnArrival::test_the_host_stamps_from_the_injected_clock`, and restoring the byte returned it to 43 passed. THE RANGE HELD: six commits base to C4, every one single-parent, the path set EQUAL to that block's ten non-handoff `Change:` paths with both differences EMPTY, insertions 357, 210, 17, 10, 15 and 35 every one under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the marker sweep 0 in all eight files a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE WORKER RE-MEASURED ITS OWN HANDBACK RATHER THAN SHIPPING A DRAFTED NUMERAL, correcting 76 to 91 lines to a fixed point with a DECISION D15 cause — the R-0486 discipline applied by a worker to itself. WHY R23 IS PASS: every applied byte is reproducible from the committed block, the contract file at C4 equals an independent reconstruction digest for digest, the red control fails in the reviewer's own worktree on the one named test, and both of the round's discrepancies were defects in the ORDER rather than in the work, declared by a worker that applied what it was given and said so.
<<<END RECORD24
