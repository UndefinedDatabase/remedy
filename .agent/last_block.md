── STEP RECORD+REPAIR — F021 ──
Goal:        Record R26, which PASSED all twelve gates under the reviewer's own
             re-measurement, and repair the one defect it surfaced. That defect
             is the REVIEWER's: R26's FEEDTESTSHIM pair anchored on an import
             line without reading what followed it, so the applied
             `feedRow.test.ts` carries a function between two imports. It
             compiles and every test passes; the repair is a move of the same
             nine lines. Registered as R-0660, fixed, and resolved in this round.

Fortschritt: ~92 % (T002 — Uhr, Ankunftsstempel und Ring verdrahtet; es fehlen
             NowCard-Punkt und Feed-Scroll)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R26 verdict
             and R-0660 · C3 the repair · C4 the resolution · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r27.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2 and C4)
             · `apps/ui/src/api/feedRow.test.ts` (C3) · `.agent/handoff.md` (C5).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice and pair half BYTE FOR BYTE. Never retype, rewrap, reflow,
    reindent or whitespace-adjust one. If a slice looks wrong, STOP and say so in
    the handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commits because the plan must be current before them (§3
    checklist item 23). The FINDING PERSISTS BEFORE THE FIX (§4.4): C2 registers
    R-0660, C3 repairs it, C4 resolves it — so a session dying mid-round leaves
    the finding on disk rather than a silent repair. PLANF021R27 describes the
    state this round ENDS in, including the resolution C4 writes, so it reads
    forward to commits this constraint fixes (§3 item 20, the R-0524 carve-out).
    ROUND BASE is `457346b6` — resolve its full form with `git rev-parse`.
 3. THIS ROUND REGISTERS EXACTLY ONE FINDING AND RESOLVES THAT SAME ONE. Before
    this round: 222 open, maximum R-0659. C2 registers R-0660 and records the R26
    gate; C4 adds the only `Done:` line this ledger has ever carried. After C4:
    223 registered, maximum R-0660, next free R-0661, `Done: R-` exactly 1.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice and pair half is quoted
    WITHOUT a trailing newline. A WHOLE-FILE write (PLANF021R27) is the slice PLUS
    one terminator. A LEDGER append (RECORD27 at C2, DONE660 at C4) is ONE
    newline, then the slice, then one terminator — so each of those commits' diffs
    ADDS the separator line first and then the slice's lines (R-0658). A PAIR is
    applied by replacing the FROM bytes with the TO bytes in place, adding no
    newline of its own.
 5. PAIR SHAPE, MEASURED NOT ASSERTED (§3 item 15). The reviewer ran the
    containment test on SHIMMOVE and its output was `TO contains FROM: false`, so
    SHIMMOVE is a REWRITE and does carry the §4.9 FROM-zero reading. The reviewer
    measured its FROM at exactly 1 occurrence in the target at the round base.
    SHIMMOVE REORDERS AND CHANGES NOTHING ELSE: its FROM and TO hold the SAME
    nine lines, and the only difference is where the import sits. If you find any
    other difference between them, STOP and report — that is the one property
    this repair depends on.
 6. ONE FILE, ONE PROPERTY, ONE COMMIT (R-0657). C2 and C4 each give
    `.agent/live_review.md` ONE append and nothing else, which is what makes each
    a byte-exact prefix of the next. C3 gives `feedRow.test.ts` the pair alone.
 7. THE LEDGER IS APPEND-ONLY. R-0660's own paragraph is NOT edited by C4; the
    resolution is a NEW `Done:` paragraph appended after it (R-0470).
 8. Run no formatter or linter that rewrites a file in place. `npm run lint` is
    RED tree-wide at every commit under R-0622 and is NOT a gate of this round —
    do not run it and do not report it. Create and merge NO pull request. Push
    the branch after C5. Create NO worktree and run no destructive check: this
    round's repair is behaviour-free and its guards are the typecheck and the
    unit suite, both of which the reviewer measured before delegating.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 274
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice and
    pair CONTENT lines — 202 against DECISION F085 D5's 400. Markers count as
    prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain` prints
     0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next session. Report also, as
     the reading THIS round owes from the last, that the R26 handback commit
     `457346b6` is single-parent and touches `.agent/handoff.md` alone at 64
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r27.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r27.md` are all equal. Write C0b
     FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts and `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pair. Report how many whole texts, how many pairs and
     how many CONTENT lines that extractor printed, each as a number YOU
     measured and never as one this block predicts, and re-measure constraint 9's
     two numerals from that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R27 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted from
     the committed C0a blob, with a NEGATIVE CONTROL against the bare slice that
     must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R27 at 48 lines, so the file is 48 lines and
     `wc -l` must read EXACTLY 48, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 48, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G5  THE TWO LEDGER APPENDS, each under TWO INDEPENDENT READERS — C2 carrying
     RECORD27 and C4 carrying DONE660. Read each base blob with
     `git show <sha>:<path>` into memory or scratch under `.remedy-wt/`; never
     overwrite a tracked file to read an older revision. Reader (a): the earlier
     blob is a byte-exact PREFIX of the later file and the remainder is EXACTLY
     one newline plus the slice plus one newline — report each remainder's
     sha256, byte and line counts, and the file's counts before and after.
     Reader (b), SET-WISE: strip the one trailing terminator from BOTH blobs,
     split each on the blank line into units, and confirm the later unit LIST
     equals the earlier list followed by that slice's own units, ELEMENTWISE over
     the whole list, not at the tail; report N at each point and each slice's
     unit count as the number YOU measured. NEGATIVE CONTROL, once, against the
     C4 file: alter one printable byte of its FIRST paragraph at equal length;
     BOTH readers must REJECT it and ACCEPT the true file. Name the offset and
     the change. Report also that neither the C2 nor the C4 diff deletes a line.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base, then C2,
     then C4: `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `;
     `Gate: R` keys and how many DISTINCT; `Gate: R27`; the MAXIMUM registered
     id. So `- R-` reads 222, 223, 223 with all DISTINCT throughout; the maximum
     R-0659, R-0660, R-0660; `Landed: ` 0 at all three; `Gate: R` keys 25, 26, 26
     all DISTINCT; `Gate: R27` 0, 1, 1. `Done: R-` reads 0, 0, then 1 — this is
     the FIRST `Done:` line this ledger has carried, so report the count at all
     three points rather than only the last.
 G7  THE REPAIR at C3, over `apps/ui/src/api/feedRow.test.ts`: SHIMMOVE's FROM 1
     at the round base and 0 at C3, TO 0 at the round base and 1 at C3. THE MOVE
     CHANGES NOTHING BUT ORDER — report that the SORTED MULTISET of the file's
     lines is IDENTICAL at the round base and at C3, which is the property that
     makes this repair behaviour-free, and report the file's line count at both
     points, which must be equal. Report also that the file's first lines are its
     imports with NO definition among them: state the line numbers of every line
     matching `^import ` and of the `function feedRowOf` line, and confirm every
     import number is lower than the function's.
 G8  TYPECHECK AND UNIT TESTS at C3, in the PRIMARY checkout, from `apps/ui`, run
     SERIALLY and never two at once. `npx tsc --noEmit` must exit 0 with EMPTY
     output. `npm run test:unit` must exit 0; report the file and test totals it
     prints. The reviewer read 15 files and 212 tests at the round base and this
     repair adds no case, so both totals must be UNCHANGED — any movement means
     the move was not behaviour-free and is a finding, not something to accept.
 G9  THE PYTHON SUITES, at C4 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left elsewhere makes these exit 4 having run no
     test, which is vacuous and not green. Report each exit code, the working
     directory and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 476, UNCHANGED, and it is
       the gate that C3 did not disturb the ring's seam pins.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, the gate that C1
       did not break `.agent/plan.md`.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G10  RANGE, executed at C4 and covering the round base to C4 — NOT to C5, because
     C5 writes the file that must quote these gates and §3 checklist item 31
     forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C4 path set against the five non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` tables (§3 item 28), any disagreement reported rather than
     reconciled; every insertion count under the 500 cap; `git ls-files
     .remedy-wt` 0; `git worktree list` ending with the primary checkout ALONE —
     NO worktree is created this round; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a slice or pair
     LANDED IN — `.agent/plan.md`, `.agent/live_review.md` and
     `apps/ui/src/api/feedRow.test.ts` — and covers EVERY marker prefix this
     block uses, which G3 names and you count for yourself: each must read 0, as
     must any line starting `<<<`. The two block mirrors ARE the block and read
     nonzero by construction.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, ONE LINE
            PER GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all three of its lines. Report its
            own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause; where the count also
            passes the 100-line tier AGENTS.md grants for more than five commit
            tables, name BOTH bounds as R26's handback did. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit cannot
            name its own SHA the role and reason go INSIDE the heading (R-0494).
            `## Next` states that THIS SESSION IS OVER; that the NEXT session
            begins at docs/agents/self_drive_protocol.md Phase 1 rule 1 — the
            `.agent/STOP` check — BEFORE rule 2's Open PR Gate (R-0347), which
            will find NO open pull request so rule 5 applies and F021 continues
            on this branch; that R27's own verdict is UNRECORDED and the next
            round's ledger commit owes it; and that R28 builds the NowCard's
            recency dot from `recency.ts` with the CSS
            `docs/ui/design_reference/assets_spec.md` governs, the first round
            able to subtract two instants on ONE clock.

<<<SLICE PLANF021R27
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
R27 records R26, which PASSED all twelve gates, and repairs the one defect that
round surfaced: the reviewer's own FEEDTESTSHIM slice inserted a function
BETWEEN two import statements in `feedRow.test.ts`, which compiles and tests
green but leaves an import stranded below a definition. Registered as R-0660 and
fixed in the same round, because the repair is a move and nothing depends on it.

## Next Steps
1. R28: the NowCard's recency dot — `recency.ts` drives BOTH the badge and the
   dot, with the CSS `docs/ui/design_reference/assets_spec.md` governs. This is
   the first round able to subtract two instants on ONE clock, which is what
   R22 through R26 built.
2. R29: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R30, the row click-jump, and T003's
   disabled steering input.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- VITEST IS MUTATION-PROVABLE since DECISION F021 D8: symlink
  `apps/ui/node_modules` into a disposable worktree and both `npx tsc --noEmit`
  and `npm run test:unit` run there, so a red control satisfies guardrail G5.
- `npm run lint` is RED across the whole tree at every commit, this branch's
  included: the eslint config has no TypeScript parser, so it reports a parsing
  error per file and is blind to style. That is R-0622, still open, and it is
  why no lint gate can catch a defect of the R-0660 shape.
- A worktree lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more case
  there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open once R-0660 closes; R-0364, R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay
  routed to a paydown branch.
<<<END PLANF021R27

<<<SLICE RECORD27
- R-0660 — Low, AN AUTHORED SLICE INSERTED A FUNCTION BETWEEN TWO IMPORT STATEMENTS, LEAVING AN IMPORT STRANDED BELOW A DEFINITION. Raised by the reviewer against its own R26 block, and caught by that round's WORKER, which applied the slice byte for byte as constraint 1 required and flagged it in the handback rather than tidying it. R26's FEEDTESTSHIM pair anchored its FROM on the single line `import { feedRowOf } from "./feedRow";` in `apps/ui/src/api/feedRow.test.ts` and its TO appended a comment and a shim function after it — but a SECOND import, `import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";`, followed that anchor on the next line, so the applied file carries its imports on lines 1, 2 and 10 with a function definition at 7 through 9. It compiles and runs: measured at `457346b6`, `npx tsc --noEmit` exits 0 with empty output and `npm run test:unit` reads 15 files and 212 tests all passing, because ES module imports are hoisted and TypeScript does not order them. THE DEFECT IS THE REVIEWER'S PAIR DESIGN, not the worker's application: an anchor chosen for uniqueness was not read against what FOLLOWS it, which no containment test and no FROM-count can surface, since both were correct. Low: nothing is broken, no gate is false, and the repair is a move of nine lines. It is a finding because the file is production test code a later reader edits, and because `npm run lint` is red tree-wide under R-0622 and could not have caught it.

  FIX, applied by this round's own repair commit and resolved below: the shim and its comment move BELOW the last import, leaving the import block contiguous. STANDING, BINDING THE REVIEWER — a pair whose TO INSERTS lines after its anchor is read against the lines that FOLLOW that anchor in the target, not only against the anchor's own uniqueness. Where the insertion belongs after a RUN of like lines — an import block, a constant block, a decorator stack — the FROM spans to the END of that run, which is the §3 checklist item 17 reading (a pair that changes a structure's arity spans the whole structure) applied to a run the eye does not register as a structure. The reviewer's dry run applies the block and then READS the applied region, rather than only running the gates over it: R26's dry run was green on tsc, vitest and the contract suite and still shipped this, because every gate it ran was blind to statement order.

Gate: R27 — the R26 entry. R26 PASSED ON EVERY ONE OF ITS TWELVE GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES THE FINDING REGISTERED IMMEDIATELY ABOVE. R26 IS THE RING ROUND: `FeedRow` gained `receivedAtMs`, `feedRowOf` took it as a REQUIRED parameter with no default anywhere, `receiveBrainFrame` threaded it, and `stepBrainStream` handed over the stamp R23 put on the transport event — so the arrival instant now reaches the ring the recency dot reads, and both of that dot's operands sit on ONE clock. All six TypeScript files moved in a single commit `7eb82ed0`, as they had to: between any two halves of an arity change the typecheck is red. TRANSPORT HELD ACROSS ALL COPIES at sha256 8c57ed2d6ba2f60dd466c84e83209f92829fa738082fccb5a18a4659714dd059 over 32107 bytes and 490 lines. SLICES: the reviewer's own extractor read the whole texts PLANF021R26, RECORD26 and CONTRACTRINGSTAMP and 16 pairs over 180 CONTENT lines from the committed C0a blob, TOTAL 490 against DECISION F085 D6's 490 — at the cap exactly — and PROSE 310 against D5's 400, both equal to that block's constraint 11. EVERY PAIR BEHAVED BY ITS MEASURED SHAPE: all sixteen FROMs occurred exactly once at the round base; the fourteen REWRITES read FROM 0 and TO 1 after; FEEDROWRET and CONTRACTPATHROW, measured APPEND-shaped before emission, read FROM 1 and TO 1 and were never asked for a zero count. THE PLAN WRITE HELD: `.agent/plan.md` at `9ba0f2ef` is byte-equal to PLANF021R26 plus one terminating newline and NOT to the bare slice, `wc -l` exactly 48. THE CONTRACT APPEND HELD AS ORDERED EQUALITY BECAUSE C4 CARRIED IT ALONE (R-0657): the `024727c2` blob is a byte-exact PREFIX of the `350cb7bc` file, remainder sha256 910eba3e8773a44a36557c408a8a9e57794a3e82e4880d04701cbdc3e07f6aa3 over 1360 bytes and 29 lines, the file 399 to 428 lines, 0 deletions, and the 29 added lines are the append convention's TWO blank separators followed by the slice's 27 lines ELEMENTWISE and IN ORDER — the R-0658 reading, stated as the convention produces it and met exactly. EXACTLY TWO blank lines precede the new top-level class, counted directly rather than delegated to a linter that is preview-blind to E301-E306 and, under R-0622, cannot parse these files at all. THE LEDGER APPEND HELD UNDER BOTH READERS: remainder sha256 84c68a86710d8c786977d6888384b25a3fa0b2f70647a6071f352345a2b04d77 over 6200 bytes and 4 lines, the file 566016 B / 1168 L before and 572216 B / 1172 L after, units 265 to 267 ELEMENTWISE equal with RECORD26 exactly 2 units, and a negative control at offset 4 of the FIRST paragraph REJECTED by both readers while both accepted the true file. THE SETS DID NOT MOVE, as a round minting nothing must read: `- R-` 222 at BOTH points all DISTINCT, maximum R-0659 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 24 to 25 both DISTINCT, `Gate: R26` 0 to 1, and the C5 diff deletes 0 lines. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the PRIMARY checkout: `npx tsc --noEmit` exit 0 with output EMPTY; `npm run test:unit` 15 files and 212 tests, the base's 209 plus this round's new cases; `tests/ui_contracts/` 472 passed plus 4 skipped = 476, the base's 473 plus CONTRACTRINGSTAMP's cases; the three state-reading suites 511; the canary 42. THE RED CONTROL WAS REPRODUCED BY THE REVIEWER ITSELF, in its own disposable worktree at `457346b6` with `apps/ui/node_modules` SYMLINKED per DECISION F021 D8 — the first vitest mutation proof this feature has been able to take. Green first at tsc 0, vitest 212 and pytest 471 passed plus 5 skipped. Then, with the single line `  const appended = [...state.recent, feedRowOf(frame, receivedAtMs)];` — confirmed EXACTLY ONCE in that file, whole-line and indent-agnostic counts agreeing — replaced by the same line passing a literal `0`, ALL THREE WENT RED: `npx tsc --noEmit` exit 2 with `src/api/brainStream.ts(89,3): error TS6133: 'receivedAtMs' is declared but its value is never read.`; vitest exit 1 with exactly 2 failures, `the row carries the arrival stamp the transport handed in` and `each row keeps its OWN stamp as the ring fills`; and pytest exit 1 with exactly 3, `test_the_projection_is_called_inside_receive_brain_frame`, `test_the_replay_guard_returns_before_the_append` and `test_the_ring_threads_the_stamp_into_the_row`. Restoring the byte returned all three to green. THE RANGE HELD: eight commits base to C6, every one single-parent, the path set EQUAL to that block's twelve `Change:` paths with both differences EMPTY, insertions 490, 411, 18, 44, 3, 29, 4 and 64 every one under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone with the G11 worktree removed and pruned, `gh pr list --state open` EMPTY, the marker sweep 0 line-anchored in all nine files a slice or pair landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE HANDBACK DECLARED ITS OWN OVERAGE HONESTLY at 101 lines, naming BOTH the 60-line cap and the 100-line tier AGENTS.md grants for more than five commit tables, with mandated content as the stated cause and no section dropped. WHY R26 IS PASS: every applied byte is reproducible from the committed block by the reviewer's own extractor, the contract remainder and the ledger remainder both matched digests the reviewer computed before delegating, three independent guards fail under one mutation and recover on restore, and the round's only defect was in the reviewer's pair design, declared by a worker that applied what it was given and said so.
<<<END RECORD27

<<<SLICE DONE660
Done: R-0660 — RESOLVED by this round. The shim and its comment now sit BELOW the last import of `apps/ui/src/api/feedRow.test.ts`, so the file's imports are contiguous on its first lines and no definition separates them. The move is behaviour-free by construction — the same nine lines in a different order, no character of the shim or of any test case altered — and the round's gates re-measure `npx tsc --noEmit` at exit 0 with empty output and `npm run test:unit` at 15 files and 212 tests, both identical to the readings taken at `457346b6` before the move. The standing rule the finding states is not resolved by this line and binds every later block: read a pair's anchor against what FOLLOWS it, and span the FROM to the end of a run of like lines.
<<<END DONE660

<<<PAIR SHIMMOVE apps/ui/src/api/feedRow.test.ts
<<<FROM
import { feedRowOf as projectRow } from "./feedRow";

// The cases below predate the arrival stamp and assert nothing about it, so
// they call through a shim supplying a fixed one. The stamp's own contract is
// the last case in this file, which calls `projectRow` directly.
function feedRowOf(frame: { seq: number; event: unknown }) {
  return projectRow(frame, 0);
}
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";
<<<TO
import { feedRowOf as projectRow } from "./feedRow";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

// The cases below predate the arrival stamp and assert nothing about it, so
// they call through a shim supplying a fixed one. The stamp's own contract is
// the last case in this file, which calls `projectRow` directly.
function feedRowOf(frame: { seq: number; event: unknown }) {
  return projectRow(frame, 0);
}
<<<ENDPAIR
