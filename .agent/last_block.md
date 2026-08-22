── STEP T002 RING — F021 ──
Goal:        Thread the arrival stamp into the ring. `FeedRow` gains
             `receivedAtMs`, `feedRowOf` takes it as a REQUIRED parameter,
             `receiveBrainFrame` threads it, and the driver hands over the stamp
             R23 already put on the transport event. No default value is given
             anywhere: a default would let a caller silently ship a wrong instant,
             which is the one failure the whole R22-R26 chain exists to prevent.
             Every caller therefore moves in the SAME commit as the signature.

Fortschritt: ~92 % (T002 — Uhr, Ankunftsstempel und Ring verdrahtet; es fehlen
             NowCard-Punkt und Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the whole arity
             change across the six TypeScript files · C3 the three contract pairs
             · C4 the new contract class, ALONE · C5 the R25 verdict and DECISION
             F021 D8 · C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r26.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `apps/ui/src/api/feedRow.ts`,
             `apps/ui/src/api/brainStream.ts`,
             `apps/ui/src/api/brainStreamDriver.ts`,
             `apps/ui/src/api/feedRow.test.ts`,
             `apps/ui/src/api/brainStream.test.ts`,
             `apps/ui/src/api/actionClass.test.ts` (all C2) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3 and C4) ·
             `.agent/live_review.md` (C5) · `.agent/handoff.md` (C6).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap, reflow,
    reindent or whitespace-adjust one. If a slice looks wrong, STOP and say so in
    the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes every substantive commit because the plan must be current before
    them (§3 checklist item 23), and PLANF021R26 describes the state this round
    ENDS in — including DECISION F021 D8, which C5 records — so it reads forward
    to commits this constraint fixes (§3 item 20, the R-0524 carve-out). ROUND
    BASE is `d121dd09` — resolve its full form with `git rev-parse` and report it.
 3. C2 IS ONE COMMIT AND CANNOT BE SPLIT. `feedRowOf` and `receiveBrainFrame`
    both gain a required parameter, so between any two halves of this change
    `npx tsc --noEmit` is RED. The six files move together or not at all.
 4. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. Before this round: 222
    open, maximum R-0659. RECORD26 records the R25 gate and adds DECISION F021 D8
    and mints NO id, so after C5: 222 open, maximum R-0659, next free R-0660.
    R-0518 is NOT resolved — D8 says so in its own words and the plan repeats it.
 5. THE NEWLINE CONVENTION, PER SLICE KIND, because the three kinds differ and a
    carried-over convention is finding R-0437. Every slice and pair half is
    quoted WITHOUT a trailing newline. A WHOLE-FILE write (PLANF021R26) is the
    slice PLUS one terminator. A LEDGER append (RECORD26) is ONE newline, then
    the slice, then one terminator. THE PYTHON CLASS append (CONTRACTRINGSTAMP)
    is TWO newlines, then the slice, then one terminator, because PEP 8 wants
    exactly two blank lines before a top-level class — so that commit's diff adds
    TWO blank separator lines and then the slice's lines. A PAIR is applied by
    replacing the FROM bytes with the TO bytes in place, adding no newline.
 6. PAIR SHAPES, MEASURED NOT ASSERTED (§3 item 15). The reviewer ran the
    containment test on every pair and recorded its output per pair, never one
    reading generalised to the rest. `TO contains FROM: true` for FEEDROWRET and
    CONTRACTPATHROW, which are therefore APPEND-shaped: for those two the §4.9
    FROM-zero count is NOT ordered and must not be reported. `TO contains FROM:
    false` for every other pair, which are therefore REWRITES and do carry the
    FROM-zero reading. The reviewer also measured every FROM at exactly 1
    occurrence in its target at the round base.
 7. ONE FILE, ONE PROPERTY, ONE COMMIT (R-0657). C4 gives
    `tests/ui_contracts/test_brain_stream_ring.py` the CONTRACTRINGSTAMP append
    and NOTHING else, which is what makes the C3 blob a byte-exact prefix of the
    C4 file. C3 carries that file's three pairs and no append. Do not merge them.
 8. THE TWO EXISTING GUARDS ARE UPDATED, NEVER WEAKENED. CONTRACTCALL and
    CONTRACTGUARD retarget assertions that currently pin the literal
    `feedRowOf(frame)`; the new strings are STRICTLY more specific and still pin
    DECISION F021 D5's append placement. Deleting either, or loosening one to
    make it pass, is forbidden — AGENTS.md's amend0820 clause names that outright.
 9. DESTRUCTIVE CHECKS RUN ONLY IN A DISPOSABLE WORKTREE (guardrail G5), and per
    DECISION F021 D8 that worktree gets `apps/ui/node_modules` SYMLINKED from the
    primary checkout — `ln -s`, NEVER a copy, because `shutil.copytree` defaults
    to `symlinks=False` and dereferences npm's bin shims (R-0591). Remove the
    symlink before `git worktree remove`, and prune.
10. Run no formatter or linter that rewrites a file in place. Create and merge NO
    pull request. Push the branch after C6.
11. Block size, measured on these final bytes AFTER the last edit: TOTAL 490
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 310 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C6; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2, C3, C4 and C5. C6's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session. Report also, as
     the reading THIS round owes from the last, that the R25 handback commit
     `d121dd09` is single-parent and touches `.agent/handoff.md` alone at 51
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r26.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r26.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts and `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pairs. Report how many whole texts, how many pairs and
     how many CONTENT lines that extractor printed, each as a number YOU
     measured and never as one this block predicts, and re-measure constraint
     11's two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R26 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R26 at 48 lines, so the file is 48 lines and
     `wc -l` must read EXACTLY 48, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 48, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G5  THE PAIRS, per pair and never generalised. For each of the sixteen, report
     its FROM count in its target at the round base — every one must be 1 — and
     at the commit that applies it. For the fourteen REWRITES report FROM 0 and
     TO 1 after. For FEEDROWRET and CONTRACTPATHROW, which constraint 6 measured
     APPEND-shaped, report FROM 1 and TO 1 after and NO zero count. Report each
     applying commit's deletion count as well.
 G6  THE CONTRACT APPEND at C4, which C4 carries ALONE. The C3 blob of
     `tests/ui_contracts/test_brain_stream_ring.py` is a byte-exact PREFIX of the
     C4 file; report the remainder's sha256, byte and line counts and the file's
     line count before and after. ORDERED EQUALITY, stated as the convention
     produces it (R-0658): the lines C4's diff ADDS are the append convention's
     TWO blank separator lines followed by CONTRACTRINGSTAMP's lines IN ORDER —
     report the added-line count and the slice's own line count as the two
     numbers YOU measured, and the deletion count, which must be 0. Report also
     that EXACTLY TWO blank lines precede the new top-level class, counted
     directly rather than delegated to a linter that is preview-blind to
     E301-E306.
 G7  THE LEDGER APPEND at C5, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision.
     Reader (a): the base blob is a byte-exact PREFIX of the C5 file and the
     remainder is EXACTLY one newline plus RECORD26 plus one newline — report its
     sha256, byte and line counts, and the file's counts before and after.
     Reader (b), SET-WISE: strip the one trailing terminator from BOTH blobs,
     split each on the blank line into units, and confirm the C5 unit LIST equals
     the base list followed by RECORD26's own units, ELEMENTWISE over the whole
     list, not at the tail; report N at both points and RECORD26's unit count as
     the number YOU measured. NEGATIVE CONTROL: alter one printable byte of the
     C5 file's FIRST paragraph at equal length; BOTH readers must REJECT it and
     ACCEPT the true file. Name the offset and the change.
 G8  THE LEDGER SETS, line-anchored at line start, at the round base then C5:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R` keys
     and how many DISTINCT; `Gate: R26`; the MAXIMUM registered id. NO id is
     minted and none resolved, so `- R-` reads 222 at BOTH with both DISTINCT,
     the maximum R-0659 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R`
     keys 24 then 25 both DISTINCT, `Gate: R26` 0 then 1. Report also that the
     C5 diff has 0 deletion lines.
 G9  TYPECHECK AND UNIT TESTS, in the PRIMARY checkout, from `apps/ui`, run
     SERIALLY and never two at once. `npx tsc --noEmit` must exit 0 with EMPTY
     output — it is the load-bearing gate of this round, because vitest does not
     typecheck and the arity change is exactly what a typechecker catches.
     `npm run test:unit` must exit 0; report the file and test totals it prints.
     The reviewer read 15 files and 209 tests at the round base; report YOURS.
G10  THE PYTHON SUITES, at C5 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left elsewhere makes these exit 4 having run no
     test, which is vacuous and not green. Report each exit code, the working
     directory and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 476, which is the base's
       473 plus CONTRACTRINGSTAMP's cases. Report the passed and skipped split
       you read; in the primary checkout the skipped count is 4, and a worktree
       skips one more for want of `apps/ui/dist/`.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that C1
       did not break `.agent/plan.md`.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G11  THE RED CONTROL, in a disposable worktree at C5 under constraint 9, NEVER in
     the primary checkout. Take it green first. Then replace the single line
       `  const appended = [...state.recent, feedRowOf(frame, receivedAtMs)];`
     in `apps/ui/src/api/brainStream.ts` — the reviewer measured that byte string
     at EXACTLY 1 occurrence in that file, whole-line and indent-agnostic counts
     agreeing — with the same line passing a literal `0`, and report THREE
     readings: `npx tsc --noEmit`'s exit code and message, `npm run test:unit`'s
     failed count and the NAMES of the failing cases, and
     `python3 -m pytest tests/ui_contracts/ -q -rf`'s failed count and node ids.
     Then restore the byte, confirm the file is byte-identical to before, and
     report all three green again. Report what YOU measure: if any of the three
     does NOT go red, say so plainly — that is a finding about this block, not
     something to work around.
G12  RANGE, executed at C5 and covering the round base to C5 — NOT to C6, because
     C6 writes the file that must quote these gates and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C5 path set against the eleven non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` tables (§3 item 28), any disagreement reported rather than
     reconciled; every insertion count under the 500 cap; `git ls-files
     .remedy-wt` 0; `git worktree list` ending with the primary checkout ALONE,
     the G11 worktree having been removed and pruned; and `gh pr list --state
     open --json number,headRefName` — expected EMPTY — with the statement that
     neither `gh pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — those of `Change:` other than the two block mirrors and
     `.agent/handoff.md` — and covers EVERY marker prefix this block uses, which
     G3 names and you count for yourself: each must read 0, as must any line
     starting `<<<`. The two mirrors ARE the block and read nonzero by construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3, C4, C5 and C6, the round base SHA, ONE
            LINE PER GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report its
            own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit cannot
            name its own SHA the role and reason go INSIDE the heading (R-0494).
            `## Next` states that THIS SESSION IS OVER; that the NEXT session
            begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347), which
            will find NO open pull request so rule 5 applies and F021 continues
            on this branch; that R26's own verdict is UNRECORDED and the next
            round's ledger commit owes it; and that R27 builds the NowCard's
            recency dot from `recency.ts` with the CSS
            `docs/ui/design_reference/assets_spec.md` governs, the first round
            able to subtract two instants on ONE clock.

<<<SLICE PLANF021R26
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
R26 is THE RING ROUND. `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it as a
required parameter, `receiveBrainFrame` threads it, and the driver hands over the
stamp R23 put on the transport event. Every caller moves in the same commit,
because a signature change that leaves one behind is a red typecheck. The
arrival instant now reaches the ring, which is what the recency dot subtracts.

## Next Steps
1. R27: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs. The dot's two
   operands are now on ONE clock, which is what R22 through R26 existed to do.
2. R28: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R29, the row click-jump, and T003's
   disabled steering input.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- VITEST IS NOW MUTATION-PROVABLE (DECISION F021 D8, R26): symlinking
  `apps/ui/node_modules` into a disposable worktree makes both `npx tsc --noEmit`
  and `npm run test:unit` run there, so a red control no longer needs the primary
  checkout and guardrail G5 is satisfied. R-0518 stays OPEN — a worktree still
  has no `node_modules` of its own — but it no longer blocks a vitest red proof.
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- R-0654 through R-0659 are ALL defects in the reviewer's own block text or
  record rather than in any worker's execution. R-0656's rule is now §3 checklist
  item 32, so the next block reads it from the checklist.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay routed to a
  paydown branch.
<<<END PLANF021R26

<<<SLICE RECORD26
Gate: R26 — the R25 entry. R25 PASSED ON EVERY ONE OF ITS TEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT DISCHARGED EVERY DEBT THE RECORD WAS CARRYING. R25 promoted R-0656's rule into docs/agents/planner_reviewer_prompt.md §3 as checklist item 32, recorded R24's verdict, registered R-0659 and recovered the R18 verdict that R19's halt had stranded. TRANSPORT HELD ACROSS ALL COPIES at sha256 85ac405392030d0846796af87f0a39e8b43d1624561ff87ce1014ee77abe2613 over 34697 bytes and 303 lines — the reviewer's emitted `.remedy-wt/f021-r25.md`, the `.agent/authored/f021-r25.md` blob at `c5c9a183` and the `.agent/last_block.md` blob at `c9bc5094`. SLICES: the reviewer's own marker-line extractor read the whole texts PLANF021R25 and RECORD25 and the pair ITEM32 over 84 CONTENT lines from the committed C0a blob, TOTAL 303 against DECISION F085 D6's 490 and PROSE 219 against D5's 400, both equal to that block's constraint 9. THE PLAN WRITE HELD: `.agent/plan.md` at `d8395de9` is byte-equal to PLANF021R25 plus one terminating newline and NOT to the bare slice, `wc -l` exactly 49, `^## Goal$` 1 and `^## Next Steps$` 1. THE PAIR BEHAVED BY ITS MEASURED SHAPE: ITEM32's containment test printed true before emission, so it was ordered as an APPEND and no FROM-zero count was demanded; at `796bef72` FROM reads 1 and TO reads 1, the diff adds 22 lines and deletes 0, and those 22 added lines are ELEMENTWISE and IN ORDER the TO lines that are not FROM lines. THE CHECKLIST GREW BY EXACTLY ONE ITEM: the §3 list runs 1 through 32 consecutively with no duplicate, item 32 sits between item 31 and the "Why this is on disk and not a habit" paragraph, and the file went 944 to 966 lines. THE LEDGER APPEND HELD UNDER BOTH READERS: the base blob is a byte-exact PREFIX of the C3 file, the remainder is exactly one newline plus RECORD25 plus one terminator at sha256 6da288742762c35dba1c0619d714a18addfddf36d21245e94526999e0f21ab45 over 14930 bytes and 10 lines — A DIGEST THE REVIEWER PREDICTED FROM ITS OWN DRY RUN BEFORE DELEGATING AND WHICH THE APPLIED BYTES REPRODUCED EXACTLY — the file 551086 B / 1158 L before and 566016 B / 1168 L after, units 260 to 265 ELEMENTWISE equal over the whole list with RECORD25 exactly 5 units, and a negative control at offset 4 of the FIRST paragraph, the byte `v` set to `X` at equal length, REJECTED by both readers while both accepted the true file. THE SETS MOVED ONLY AS ORDERED: `- R-` 221 to 222 all DISTINCT at both, maximum R-0658 to R-0659, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 23 to 24 both DISTINCT, `Gate: R25` 0 to 1, `Gate: R19` 0 at BOTH — the recovery did not reintroduce the key R20 ruled would never appear — and `- R-0656` exactly ONCE at both, so item 32 is its promotion and not a second registration. THE OLDER ENTRIES ARE UNTOUCHED: the C3 diff adds 10 lines and DELETES 0, and the `acb688a9` blob is a byte-exact PREFIX of the C3 file. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY from the repository root in the PRIMARY checkout and counted BY PASSED PLUS SKIPPED: the three state-reading suites 511, `tests/docs/` 295 — owed because this round's change set holds a `docs/` path — the canary 42, and `tests/ui_contracts/` 469 passed plus 4 skipped = 473, UNCHANGED. THE RANGE HELD: five commits base to C3, every one single-parent, the path set EQUAL to the block's five non-handoff `Change:` paths with both differences EMPTY, insertions 303, 195, 16, 22 and 10 each under the 500 cap and each agreeing cell by cell with the handback's `## Commits` tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored in all three files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE WORKER DECLARED NO DEVIATION AND NONE WAS FOUND. Its one aside was itself slightly wrong and cost nothing: it reported the "Verification tiers" list as numbering 1, 2, 3, 5, which is an artefact of sweeping only BOLDED items — tier 4 exists and is simply not bolded — and it had correctly scoped its own gate reading to the §3 checklist, so the reading it certified was right. WHY R25 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, the ledger remainder matched a digest predicted before delegation, both readers reject a same-length mutant, and the round closed three record debts without touching a line of production code.

DECISION F021 D8 — A VITEST RED CONTROL IS NOW REACHABLE, SO THE FEATURE'S BEHAVIOURAL TESTS STOP BEING UNPROVED. CHOSEN: run destructive vitest and tsc checks inside a disposable `git worktree` with `apps/ui/node_modules` SYMLINKED from the primary checkout, and require a mutation red proof of any vitest case a round newly relies on. WHY: this chain has recorded since R-0518 that "no vitest case has been mutation-proved" because a fresh worktree has no `node_modules`, and guardrail G5 forbids mutating the primary checkout — so the strongest guard the UI has was also the least proven. MEASURED BEFORE THIS ROUND WAS DESIGNED, at `d121dd09` in a disposable worktree: with the symlink in place `npx tsc --noEmit` exits 0 and `npm run test:unit` reads 15 files and 209 tests all passing, identical to the primary checkout; forcing `overflow` to 0 in `receiveBrainFrame` turned exactly 2 of those red and restoring the byte returned all 209 to green. A SYMLINK AND NEVER A COPY: `shutil.copytree` defaults to `symlinks=False` and dereferences npm's bin shims, which is the mechanism R-0591 registered, so the argument is named here rather than left to the caller. R-0518 STAYS OPEN and is NOT resolved by this entry — a worktree still ships no `node_modules` of its own and a round that forgets the symlink still reads a false red — but the limitation it describes no longer blocks a red proof. HOW TO REVERSE: drop the symlink step and the vitest red-proof obligation from later blocks; nothing else depends on it, and the Python source contracts remain the durable seam pins they were.
<<<END RECORD26

<<<SLICE CONTRACTRINGSTAMP
class TestTheRingCarriesTheArrivalStamp:
    """R23 stamped the transport event; this pins the rest of the path. The ring
    is where the stamp becomes durable, so `feedRowOf` must TAKE it rather than
    read a clock, `receiveBrainFrame` must thread it, and the driver must hand
    over the event's own stamp. A behavioural test sees the number and not its
    provenance, which is why the seam is pinned here."""

    def test_the_projection_takes_the_stamp_rather_than_reading_a_clock(self):
        code = strip_ts_comments(ROW.read_text())
        assert "receivedAtMs: number" in code, (
            "FeedRow must declare the stamp and feedRowOf must take it"
        )
        assert "Date.now()" not in code, (
            "feedRow.ts must never read a real clock; the host stamps"
        )

    def test_the_ring_threads_the_stamp_into_the_row(self):
        code = strip_ts_comments(STATE.read_text())
        assert "feedRowOf(frame, receivedAtMs)" in code, (
            "receiveBrainFrame must pass the arrival instant to the projection"
        )

    def test_the_driver_hands_over_the_events_own_stamp(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "receiveBrainFrame(state, event.frame, event.receivedAtMs)" in code, (
            "the driver must thread the transport event's stamp, not invent one"
        )
<<<END CONTRACTRINGSTAMP

<<<PAIR FEEDROWFIELD apps/ui/src/api/feedRow.ts
<<<FROM
/** What one activity-feed row shows. `seq` is the ledger position the row
 *  carries and jumps to; `known` is what a dev console note counts. */
export interface FeedRow {
  seq: number;
<<<TO
/** What one activity-feed row shows. `seq` is the ledger position the row
 *  carries and jumps to; `known` is what a dev console note counts.
 *  `receivedAtMs` is the arrival instant the host stamped from the injected
 *  clock (R23). The recency dot subtracts it from that SAME clock, which the
 *  envelope's own `timestamp` could not serve: it is a server-clock string
 *  ui_server.py passes through unparsed, empty where the run log has none, so
 *  a server running behind would render as a dead agent. */
export interface FeedRow {
  seq: number;
  receivedAtMs: number;
<<<ENDPAIR

<<<PAIR FEEDROWSIG apps/ui/src/api/feedRow.ts
<<<FROM
export function feedRowOf(frame: BrainStreamFrame): FeedRow {
<<<TO
export function feedRowOf(
  frame: BrainStreamFrame,
  receivedAtMs: number,
): FeedRow {
<<<ENDPAIR

<<<PAIR FEEDROWRET apps/ui/src/api/feedRow.ts
<<<FROM
  return {
    seq: frame.seq,
<<<TO
  return {
    seq: frame.seq,
    receivedAtMs,
<<<ENDPAIR

<<<PAIR RECVSIG apps/ui/src/api/brainStream.ts
<<<FROM
export function receiveBrainFrame(
  state: BrainStreamState,
  frame: BrainStreamFrame,
): BrainStreamState {
<<<TO
export function receiveBrainFrame(
  state: BrainStreamState,
  frame: BrainStreamFrame,
  receivedAtMs: number,
): BrainStreamState {
<<<ENDPAIR

<<<PAIR RECVCALL apps/ui/src/api/brainStream.ts
<<<FROM
  const appended = [...state.recent, feedRowOf(frame)];
<<<TO
  const appended = [...state.recent, feedRowOf(frame, receivedAtMs)];
<<<ENDPAIR

<<<PAIR DRIVERTHREAD apps/ui/src/api/brainStreamDriver.ts
<<<FROM
      const next = receiveBrainFrame(state, event.frame);
<<<TO
      const next = receiveBrainFrame(state, event.frame, event.receivedAtMs);
<<<ENDPAIR

<<<PAIR TESTDRIVE apps/ui/src/api/brainStream.test.ts
<<<FROM
  return seqs.reduce((s, seq) => receiveBrainFrame(s, { seq, event: { seq } }), state);
<<<TO
  return seqs.reduce((s, seq) => receiveBrainFrame(s, { seq, event: { seq } }, seq * 10), state);
<<<ENDPAIR

<<<PAIR TESTREPLAY apps/ui/src/api/brainStream.test.ts
<<<FROM
    const again = receiveBrainFrame(s, { seq: 2, event: { seq: 2 } });
<<<TO
    const again = receiveBrainFrame(s, { seq: 2, event: { seq: 2 } }, 999);
<<<ENDPAIR

<<<PAIR TESTPROJ apps/ui/src/api/brainStream.test.ts
<<<FROM
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started", outcome: "ok" },
    });
<<<TO
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started", outcome: "ok" },
    }, 1234);
<<<ENDPAIR

<<<PAIR TESTSTAMP apps/ui/src/api/brainStream.test.ts
<<<FROM
    expect(s.recent[0].outcome).toBe("ok");
  });
});
<<<TO
    expect(s.recent[0].outcome).toBe("ok");
  });

  it("the row carries the arrival stamp the transport handed in", () => {
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started" },
    }, 1234);
    expect(s.recent[0].receivedAtMs).toBe(1234);
  });

  it("each row keeps its OWN stamp as the ring fills", () => {
    const s = drive(initialBrainStreamState(), [1, 2, 3]);
    expect(s.recent.map((r) => r.receivedAtMs)).toEqual([10, 20, 30]);
  });
});
<<<ENDPAIR

<<<PAIR ACTIONROW apps/ui/src/api/actionClass.test.ts
<<<FROM
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "" };
<<<TO
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "", receivedAtMs: 0 };
<<<ENDPAIR

<<<PAIR FEEDTESTSHIM apps/ui/src/api/feedRow.test.ts
<<<FROM
import { feedRowOf } from "./feedRow";
<<<TO
import { feedRowOf as projectRow } from "./feedRow";

// The cases below predate the arrival stamp and assert nothing about it, so
// they call through a shim supplying a fixed one. The stamp's own contract is
// the last case in this file, which calls `projectRow` directly.
function feedRowOf(frame: { seq: number; event: unknown }) {
  return projectRow(frame, 0);
}
<<<ENDPAIR

<<<PAIR FEEDTESTSTAMP apps/ui/src/api/feedRow.test.ts
<<<FROM
    const row = feedRowOf(frameOf(7, { event: "constructor" }));
    expect(row.known).toBe(false);
    expect(row.line).toBe("constructor event");
  });
});
<<<TO
    const row = feedRowOf(frameOf(7, { event: "constructor" }));
    expect(row.known).toBe(false);
    expect(row.line).toBe("constructor event");
  });

  it("carries the arrival stamp the caller supplies, unchanged", () => {
    const row = projectRow(frameOf(8, { event: "task_run_started" }), 1717);
    expect(row.receivedAtMs).toBe(1717);
  });
});
<<<ENDPAIR

<<<PAIR CONTRACTPATHROW tests/ui_contracts/test_brain_stream_ring.py
<<<FROM
STATE = API_DIR / "brainStream.ts"
<<<TO
STATE = API_DIR / "brainStream.ts"
ROW = API_DIR / "feedRow.ts"
<<<ENDPAIR

<<<PAIR CONTRACTCALL tests/ui_contracts/test_brain_stream_ring.py
<<<FROM
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "feedRowOf(frame)" in body
<<<TO
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "feedRowOf(frame, receivedAtMs)" in body
<<<ENDPAIR

<<<PAIR CONTRACTGUARD tests/ui_contracts/test_brain_stream_ring.py
<<<FROM
        guard = body.index("frame.seq <= state.lastSeq) return state;")
        assert guard < body.index("feedRowOf(frame)"), (
<<<TO
        guard = body.index("frame.seq <= state.lastSeq) return state;")
        assert guard < body.index("feedRowOf(frame, receivedAtMs)"), (
<<<ENDPAIR
