── STEP T002/WIRING-2 — F021 ──
Goal:        Put the arrival stamp ON THE TRANSPORT EVENT. R22 installed the
             clock as an injected dependency and nothing consumed it; this round
             the host reads it once per frame and the driver's event union
             carries the value. The driver stays a PURE reducer — it transports
             the number and never asks what time it is — so the ring can read an
             instant at R24 without a clock of its own. Still nothing renders:
             the NowCard is R25 and the feed's scroll container is R26.

Fortschritt: ~89 % (T002 — die Uhr ist injiziert, der Frame traegt ab dieser
             Runde seinen Ankunftsstempel; es fehlen Ring, NowCard und Feed)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R22 verdict
             and the two findings it surfaced · C3 the six TypeScript pairs ·
             C4 the source contract · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r23.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/brainStreamDriver.ts`,
             `apps/ui/src/api/brainStreamHost.ts`,
             `apps/ui/src/api/brainStreamDriver.test.ts`,
             `apps/ui/src/api/brainStreamRunner.test.ts`,
             `apps/ui/src/api/brainStreamHost.test.ts` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C4) ·
             `.agent/handoff.md` (C5).
             Resolve any count in this block against that list. NO component, no
             CSS and no `docs/` file is touched this round.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it. R22's worker did exactly that twice and both
    reports became the findings this round registers.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit because the plan must be current before it (§3
    checklist item 23). ROUND BASE is `16186186` — resolve its full form with
    `git rev-parse` and report it — and it is the commit every "round base" in
    this block names.
 3. THIS ROUND REGISTERS EXACTLY TWO FINDINGS AND RESOLVES NONE. Before: 218
    open, maximum R-0655. RECORD23 registers R-0656 and R-0657, so after C2: 220
    open, maximum R-0657, next free R-0658. Both are defects of the REVIEWER's
    own R22 block text, surfaced by that round's worker; §3 checklist item 30's
    search of the open set found no entry describing either, and they are two
    ids rather than one because they break different rules in different places.
 4. PAIR FORM AND ITS PROOF. Every pair below is given as a FROM and a TO. The
    reviewer ran the containment test MECHANICALLY over all six before emission
    and it printed `TO contains FROM: false` for EVERY one, so all six are
    REWRITES and each one's proof is the pair of counts G4 orders. This is the
    opposite shape from R22, whose twelve pairs all printed `true` — do not
    carry that round's reading over (§3 checklist item 15).
 5. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R23) is the slice PLUS one
    terminator. An APPEND to a record (RECORD23, CONTRACTSTAMP) is one newline,
    then the slice, then one terminator, so the target keeps exactly one.
 6. THE LEDGER IS APPEND-ONLY. No older entry is opened or edited (R-0470).
 7. Run no formatter or linter that rewrites a file in place. Create and merge
    NO pull request: F021 is mid-feature. Push the branch after C5. Run NO
    destructive check and create NO worktree: the red control for C4's contract
    was already reproduced by the reviewer and is re-run by it at the verdict.
 8. C4 CARRIES THE APPEND ALONE. No pair targets
    `tests/ui_contracts/test_brain_stream_ring.py` this round, so the prefix
    reading G5 orders is reachable — R-0657 records what happened when R22
    bundled a mid-file pair into the same commit as its append and made that
    same clause unmeetable.
 9. Block size, measured on these final bytes AFTER the last edit: TOTAL 357
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 230 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading
     is ordered NOWHERE — §3 item 31 leaves it to the next session. Report also,
     as the reading THIS round owes from the last, that the R22 handback commit
     `16186186` is single-parent and touches `.agent/handoff.md` alone at 51
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r23.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r23.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the whole texts, `<<<PAIR `/`<<<FROM`/`<<<TO`/
     `<<<ENDPAIR` for the pairs. Report how many pairs, how many whole-text
     slices, and how many CONTENT lines that extractor printed — state each as
     the number YOU measured and never as a number this block predicts — and
     re-measure constraint 9's two numerals from that same blob against caps.
 G4  THE SIX REWRITES AT C3. For EACH, report over its target file: the FROM's
     count at the round base, which must be EXACTLY 1; and at C3, the FROM's
     count, which must be EXACTLY 0, and the TO's count, which must be EXACTLY
     1. Report the six rows as a table, not as a sentence. All six are REWRITES
     by the measurement constraint 4 states, so all three counts are owed for
     every one of them.
 G5  THE CONTRACT APPEND at C4, as ORDERED EQUALITY (R-0531, because this slice
     is CODE and its lines repeat structurally): the C3 blob of
     `tests/ui_contracts/test_brain_stream_ring.py` is a byte-exact PREFIX of
     the C4 file, the remainder is EXACTLY one newline plus CONTRACTSTAMP plus
     one newline, and the lines C4's diff ADDS to that file are exactly the
     slice's lines IN ORDER. Constraint 8 is what makes the prefix half
     reachable. Report the remainder's sha256, bytes and lines, and the file's
     bytes and lines before and after. Report also that EXACTLY TWO blank lines
     precede the new top-level class, counted rather than delegated to a linter
     that does not evaluate E301-E306 outside preview (R-0558).
 G6  `.agent/plan.md` at C1 equals PLANF021R23 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R23 at 47 lines, so the file is 47 lines and
     `wc -l` must read EXACTLY 47, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 47, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G7  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD23 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list followed
     by RECORD23's own units, ELEMENTWISE over the whole list, not at the tail;
     report N at both points and RECORD23's unit count as the number YOU
     measured. NEGATIVE CONTROL: alter one printable byte of the C2 file's FIRST
     paragraph at equal length; BOTH readers must REJECT it and ACCEPT the true
     file. Name the offset and the change.
 G8  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R23`; the MAXIMUM registered id. Two ids
     are minted and none resolved, so `- R-` reads 218 then 220 with both
     DISTINCT, the maximum R-0655 then R-0657, `Done: R-` and `Landed: ` 0 at
     both, `Gate: R` keys 21 then 22 both DISTINCT, `Gate: R23` 0 then 1.
 G9  THE SUITES, at C4 in the PRIMARY checkout, SERIALLY, from the directory
     each command names — a shell left elsewhere makes the pytest ones exit 4
     having run no test, which is vacuous and not green. Never run two at once.
     Report each one's exit code, its working directory, and its total, counting
     BY PASSED PLUS SKIPPED:
       in `apps/ui`: `npx tsc --noEmit` — exit 0 with output EMPTY. THIS IS THE
       LOAD-BEARING GATE OF THIS ROUND: every one of the six pairs changes a
       TYPE or a literal that must satisfy one, and vitest does not typecheck.
       in `apps/ui`: `npm run test:unit` — 15 files and 209 tests, UNCHANGED
       from the base: this round adds no vitest case, and the four test-file
       pairs only feed the new required field to literals that already existed.
       from the repository root: `python3 -m pytest tests/ui_contracts/ -q -rf`
       — 473, the base's 469 plus the FOUR cases CONTRACTSTAMP adds.
       from the repository root: `python3 -m pytest tests/ui_server/
       tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511, and they READ
       `.agent/plan.md`, so they are the gate that C1 did not break it.
       from the repository root: `python3 -m pytest tests/cli/test_golden_path.py
       -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/roadmap/` path.
 G10 RANGE, executed at C4 and covering the round base to C4 — NOT to C5,
     because C5 writes the file that must quote this gate and §3 checklist item
     31 forbids ordering a reading the quoting artefact cannot hold. Report: the
     base-to-C4 path set against the ten non-handoff paths of `Change:`, the
     difference EMPTY both ways; every commit single-parent; `git show --numstat`
     and `git diff --numstat` agreeing cell by cell with the handback's
     `## Commits` table (§3 item 28), any disagreement reported rather than
     reconciled; insertions under the 500 cap; `git ls-files .remedy-wt` 0; `git
     worktree list` ending with the primary checkout alone — NO worktree is
     created this round; and `gh pr list --state open --json
     number,headRefName` — expected EMPTY — with the statement that neither `gh
     pr create` nor `gh pr merge` was run.
     THE MARKER CLAUSE IS LINE-ANCHORED and scoped to the files a SLICE LANDED
     IN — `.agent/plan.md`, `.agent/live_review.md`, the five `apps/ui` files
     and `tests/ui_contracts/test_brain_stream_ring.py`, each of which must read
     0 for every one of the four marker prefixes.
     `.agent/authored/f021-r23.md` and `.agent/last_block.md` ARE the block and
     read nonzero BY CONSTRUCTION; they are not in scope.
     THE REFLOG CLAUSE NAMES ITS FIELD (R-0613): read `git reflog --format=%gs`,
     take the OPERATION only — the text BEFORE the first `:` — and scope to THIS
     ROUND'S rows. Report that every such row's operation is `commit` and that
     `amend`, `rebase` and `cherry` each occur 0 times in that OPERATION field.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, ONE
            LINE PER GATE with transcripts kept out of the file (R-0582), and
            the `Fortschritt:` line verbatim across all three of its lines.
            Report its own `wc -l` against the 60-line cap, with a DECISION D15
            line declaring any overage and its mandated cause. Every
            `## Commits` heading carries that commit's FULL subject, and where a
            commit cannot name its own SHA the role and reason go INSIDE the
            heading (R-0494). `## Next` states that the next round is R24, which
            puts the stamp on the RING's row — `feedRow.ts` gains
            `receivedAtMs` on `FeedRow` and `feedRowOf` takes it, and
            `brainStream.ts`'s `receiveBrainFrame` threads it from the event
            this round created — and that R24 is the first round to touch the
            ring, whose append placement DECISION F021 D5 governs.

<<<SLICE PLANF021R23
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
R23 puts the arrival stamp on the TRANSPORT EVENT: the host reads the clock R22
injected, once per frame, and `BrainStreamEvent`'s frame member carries the
number. The driver stays a pure reducer that transports it without asking the
time. Nothing renders yet.

## Next Steps
1. R24: the ring's row carries the stamp — `FeedRow` gains `receivedAtMs`,
   `feedRowOf` takes it and `receiveBrainFrame` threads it. First round to touch
   the ring, whose append placement DECISION F021 D5 governs.
2. R25: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
3. R26: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R27, the row click-jump, and T003's
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
- A block states pair shapes it MEASURED for its own pairs and never carries the
  previous round's reading over: R22's twelve were all APPEND, R23's six are all
  REWRITE (R-0656 and R-0657 are the cost of the reviewer's own drift here).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654, R-0655, R-0656 and R-0657 stay
  routed to a paydown branch.
<<<END PLANF021R23

<<<SLICE RECORD23
- R-0656 — Low, A GATE COUNTED THE BLOCK'S OWN WHOLE-TEXT SLICES AND STATED TWO WHERE ITS EXTRACTOR READS THREE. Raised by the reviewer against its own R22 block, and caught by that round's WORKER, which reported it in the handback rather than silently reconciling a numeral constraint 1 forbade it to touch. R22's G3 ordered the slices extracted "by their marker LINES — `<<<SLICE `/`<<<END ` for the two whole texts", and the block carries THREE such texts: PLANF021R22, RECORD22 and CONTRACTSTAMP's predecessor CONTRACTCLOCK. The block's own arithmetic was right — constraint 8's CONTENT of 162 lines and PROSE of 255 count all three, and both the worker's extractor and the reviewer's independent one read `pairs 12 | whole-text slices 3 | CONTENT 162` from the committed C0a blob at `1580fded` — so only the word "two" was wrong. This is the R-0402 / R-0436 / R-0526 family: a hand-counted numeral about the author's OWN parts, standing beside a measurement that was correct. §3 checklist item 11 forbids exactly this and item 16 sweeps it from headings into any quantifying sentence, and a gate's own text is the one place neither item was applied. Low: no gate read the numeral, the extraction it describes is unambiguous without it, and the round's counts were all correct.

  FIX, applied by this entry: STANDING, BINDING THE REVIEWER — a clause naming a KIND of slice states no count of that kind. Write "for the whole texts" and never "for the two whole texts"; where a count is genuinely owed, the block orders the WORKER to report the number IT measured, which is the form R23's own G3 uses. The reviewer's pre-emission sweep runs the extractor over the final bytes and reads every numeral in the block against what it printed, not against what the author remembers writing.

- R-0657 — Low, A GATE ORDERED A PREFIX READING OVER A COMMIT THE SAME BLOCK ALSO GAVE A MID-FILE EDIT, MAKING THE CLAUSE UNMEETABLE BY CONSTRUCTION. Raised by the reviewer against its own R22 block, and caught by that round's WORKER, which measured the clause False and declared it rather than quietly gating something else. R22's G5 ordered, for the contract append, that "the pre-commit blob of `tests/ui_contracts/test_brain_stream_ring.py` is a byte-exact PREFIX of the post-commit file". Its C4 commit carried BOTH the CONTRACTCLOCK append AND the pair CONTRACTHOSTPATH, which inserts `HOST = API_DIR / "brainStreamHost.ts"` at line 28 — a mid-file insertion — so the C3 blob cannot be a prefix of the C4 file whatever the append does, and the worker reported False. The append itself was sound: measured by the reviewer at the verdict, the C4 file is byte-identical to an independent reconstruction from the reviewer's own slice bytes at sha256 66ba001cc3fca36eabc064caa7297d13f10b9f722992484af58b9e2363dc32a3, C4's diff deletes 0 lines, and the two blank lines before the new class are present. So the round lost nothing but a declared deviation proving a reviewer mistake. This is the §3 checklist item 18 and item 27 family — a recipe read against the property it must establish — arriving through the COMMIT PARTITION rather than through the recipe's own words, which is why neither item caught it: both halves were individually sound and only their placement in one commit was wrong.

  FIX, applied by this entry: STANDING, BINDING THE REVIEWER — when a block orders an ORDERED-EQUALITY or PREFIX reading over a file, that file receives NOTHING ELSE in the same commit, and the block says so as a constraint the worker can check before it starts. R23's constraint 8 is that clause, and its C4 carries the append alone. Where a round genuinely needs both, it gives them separate commits and gates each on its own property; the prefix reading is never weakened to accommodate a bundled pair.

Gate: R23 — the R22 entry. R22 PASSED ON EVERY ONE OF ITS TEN GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK, AND IT SURFACES THE TWO FINDINGS REGISTERED IMMEDIATELY ABOVE — BOTH OF THEM DEFECTS IN THE REVIEWER'S OWN BLOCK TEXT, FOUND BY THE WORKER. R22 installed the client clock as an injected dependency of the brain-stream transport: `BrainStreamEnv`, `BrainStreamHostDeps` and `BrainStreamGlobals` each learned `now()`, `createBrainStreamHostDeps` forwards it and `browserBrainStreamEnv` binds it from the injected global, so `RemedyShell.tsx`'s `browserBrainStreamEnv(window)` still compiles because `window.Date` satisfies the new member structurally. Nothing consumes the clock yet by design. WHY THE CLOCK AT ALL, recorded as DECISION F021 D6 at `33b44b4a`: `recencyLevel` takes two NUMBERS and this client held no numeric instant, because `FeedRow.timestamp` is a server-clock STRING `ui_server.py` passes through unparsed, so parsing it would let a server running behind read as a dead agent — the one failure `recency.ts` says it must never make. TRANSPORT HELD ACROSS ALL THREE COPIES at sha256 d36c446a31dd7b1dafda420f97ee58511bc1c96f01601da4c730e8315449f136 over 26881 bytes and 417 lines. SLICES: the reviewer's own extractor read 12 pairs and 3 whole-text slices over 162 CONTENT lines from the committed C0a blob, TOTAL 417 against DECISION F085 D6's 490 and PROSE 255 against D5's 400, both equal to that block's constraint 8. ALL TWELVE PAIRS APPLIED EXACTLY AS AUTHORED: every ANCHOR occurred exactly once in its target at the round base and ANCHOR-plus-newline-plus-ADD exactly once at the commit that applied it, measured by the reviewer over the committed blobs, and no FROM-zero count was ordered because the containment test had printed true for all twelve. THE PLAN WRITE HELD: `.agent/plan.md` at `0f100c6c` is byte-equal to PLANF021R22 plus one terminating newline and NOT to the bare slice, `wc -l` reads exactly 46 — the MEASURED value that block ordered — with `^## Goal$` 1 and `^## Next Steps$` 1. THE LEDGER APPEND HELD UNDER BOTH READERS: base blob a byte-exact prefix of the C2 file, remainder sha256 43408753c14e405b6159deb4c69fb43575f75b9bf55271175e8865d3ae6c6e82 over 5163 bytes and 4 lines, the file 529237 B / 1136 L before and 534400 B / 1140 L after, units 249 to 251 ELEMENTWISE equal with RECORD22 exactly 2 units, a negative control at offset 5 inside the FIRST paragraph rejected by BOTH readers while both accepted the true file, and 0 deleted lines in the diff. THE SETS MOVED ONLY AS ORDERED: `- R-` 218 at BOTH points all DISTINCT, maximum R-0655 at both, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 20 to 21 both DISTINCT, `Gate: R22` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially: `npx tsc --noEmit` in `apps/ui` exit 0 with output EMPTY; `npm run test:unit` 15 files and 209 tests, the base's 207 plus the two cases DEPSFORWARDCASE and BROWSERNOWCASE add; `tests/ui_contracts/` 465 passed plus 4 skipped = 469, the base's 465 plus the four CONTRACTCLOCK adds; the three state-reading suites 511; the canary 42. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE at `16186186`: green first at 39 passed, then with `      return globals.Date.now();` replaced by `      return Date.now();` — a target the reviewer confirmed occurs EXACTLY ONCE, whole-line and indent-agnostic counts agreeing — exactly 2 failed and 37 passed, the failures being `TestTheTransportClockIsInjected::test_the_browser_environment_reads_the_clock_off_its_global` and `::test_no_module_in_the_transport_chain_calls_the_clock_directly`, and restoring the byte returned it to 39 passed. THE RANGE HELD: six commits base to C4, every one single-parent, the path set EQUAL to that block's ten non-handoff `Change:` paths with both differences EMPTY, insertions 417, 358, 19, 4, 38 and 37 every one under the 500 cap and each agreeing cell by cell with the handback's tables, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the LINE-ANCHORED marker sweep 0 in all eight files a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. WHY R22 IS PASS: every applied byte is reproducible from the committed block — the contract file at C4 equals an independent reconstruction from the reviewer's own slice bytes, digest for digest — the red control fails in the reviewer's own worktree on the named tests, and both of the round's discrepancies were defects in the ORDER rather than in the work, declared by a worker that applied what it was given and said so.
<<<END RECORD23

<<<PAIR DRIVEREVENTSTAMP apps/ui/src/api/brainStreamDriver.ts
<<<FROM
/** What the transport tells the driver. `unsupported` is the fallback trigger:
 *  no EventSource in this environment, or the stream failed to construct. */
export type BrainStreamEvent =
  | { kind: "opened" }
  | { kind: "frame"; frame: BrainStreamFrame }
<<<TO
/** What the transport tells the driver. `unsupported` is the fallback trigger:
 *  no EventSource in this environment, or the stream failed to construct.
 *
 *  A frame carries `receivedAtMs`: the instant the HOST saw it, read from the
 *  clock R22 injected. T5_F021's activity dot subtracts two numbers, and the
 *  envelope's own `timestamp` is a server-clock string ui_server.py passes
 *  through unparsed and empty where the run log has none — so a server running
 *  behind would read as a dead agent. Stamping on arrival keeps both operands
 *  on ONE clock. The driver only CARRIES the value; the ring consumes it. */
export type BrainStreamEvent =
  | { kind: "opened" }
  | { kind: "frame"; frame: BrainStreamFrame; receivedAtMs: number }
<<<ENDPAIR

<<<PAIR HOSTTELLSTAMP apps/ui/src/api/brainStreamHost.ts
<<<FROM
    dispatch({ kind: "frame", frame });
<<<TO
    dispatch({ kind: "frame", frame, receivedAtMs: deps.now() });
<<<ENDPAIR

<<<PAIR DRIVERTESTFRAME apps/ui/src/api/brainStreamDriver.test.ts
<<<FROM
function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } } };
}
<<<TO
function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } }, receivedAtMs: 0 };
}
<<<ENDPAIR

<<<PAIR RUNNERTESTFRAME apps/ui/src/api/brainStreamRunner.test.ts
<<<FROM
function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } } };
}
<<<TO
function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } }, receivedAtMs: 0 };
}
<<<ENDPAIR

<<<PAIR HOSTTESTONEFRAME apps/ui/src/api/brainStreamHost.test.ts
<<<FROM
      { kind: "frame", frame: { seq: 4, event: JSON.parse(payload(4)) } },
<<<TO
      { kind: "frame", frame: { seq: 4, event: JSON.parse(payload(4)) }, receivedAtMs: 1000 },
<<<ENDPAIR

<<<PAIR HOSTTESTPOLLFRAMES apps/ui/src/api/brainStreamHost.test.ts
<<<FROM
      { kind: "frame", frame: { seq: 6, event: null } },
      { kind: "frame", frame: { seq: 7, event: null } },
<<<TO
      { kind: "frame", frame: { seq: 6, event: null }, receivedAtMs: 1000 },
      { kind: "frame", frame: { seq: 7, event: null }, receivedAtMs: 1000 },
<<<ENDPAIR

<<<SLICE CONTRACTSTAMP

class TestEveryFrameIsStampedOnArrival:
    """The dot subtracts two numbers, so a frame must reach the client carrying
    one. The stamp is taken in the HOST — the one place a real clock legitimately
    lives — and travels on the transport event, so the driver stays a pure
    reducer and the ring can read the instant without asking what time it is.
    Pinning the SEAM rather than a value: a behavioural test cannot see which
    clock the number came from."""

    def test_the_transport_event_carries_the_arrival_stamp(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "receivedAtMs: number" in code, (
            "the frame event must declare the stamp it carries"
        )

    def test_the_host_stamps_from_the_injected_clock(self):
        code = strip_ts_comments(HOST.read_text())
        assert "receivedAtMs: deps.now()" in code, (
            "the stamp comes from the injected clock, never a real one"
        )

    def test_the_driver_does_not_stamp_anything_itself(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "now()" not in code, (
            "the driver is a pure reducer; only the host reads a clock"
        )

    def test_only_one_module_dispatches_a_stamped_frame(self):
        sites = 0
        for path in (HOST, DRIVER, STATE, DEPS):
            sites += strip_ts_comments(path.read_text()).count('kind: "frame", frame')
        assert sites == 1, (
            f"exactly one dispatch site may stamp a frame, found {sites}"
        )
<<<END CONTRACTSTAMP
