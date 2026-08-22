── STEP T002/WIRING-1 — F021 ──
Goal:        Give the brain-stream transport an INJECTED CLOCK. The activity dot
             R20 built is a pure function of two NUMBERS, and this client holds
             no numeric instant anywhere: a row's `timestamp` is a server-clock
             STRING that `ui_server.py` passes through unparsed and empty when
             the run log carries none. Parsing it would let a server clock that
             runs behind read as a dead agent, which is the one failure
             `recency.ts` says it must never make. So the stamp will be taken on
             ARRIVAL, on the client's own clock, and this round installs the
             clock as a dependency: `BrainStreamEnv`, `BrainStreamHostDeps` and
             `BrainStreamGlobals` each learn `now()`, and the real environment
             binds it from the injected global. NOTHING CONSUMES IT YET — the
             frame event carries it at R23 and the ring's row at R24.

Fortschritt: ~88 % (T002 — die vier reinen Regeln stehen; die Verdrahtung ist in
             vier kleine Runden zerlegt, R22 legt die Uhr als Abhaengigkeit)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R21 verdict
             and DECISION F021 D6 · C3 the twelve TypeScript pairs · C4 the
             source contract · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r22.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/brainStreamHost.ts`,
             `apps/ui/src/api/brainStreamDeps.ts`,
             `apps/ui/src/api/brainStreamHost.test.ts`,
             `apps/ui/src/api/brainStreamSession.test.ts`,
             `apps/ui/src/api/brainStreamDeps.test.ts` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C4) ·
             `.agent/handoff.md` (C5).
             Resolve any count in this block against that list. NO component,
             no CSS and no `docs/` file is touched this round.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger commit because the plan must be current before it (§3
    checklist item 23). ROUND BASE is `bf0c50bf` — resolve its full form with
    `git rev-parse` and report it — and it is the commit every "round base" in
    this block names.
 3. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. Before and after: 218
    open, maximum R-0655, next free R-0656. The plan defect this round repairs
    is routed to PLANNING as DECISION F021 D6 under §4 item 7, not minted as an
    id: a wrong plan is a spec fault, and §3 checklist item 30's search of the
    open set found no entry describing it.
 4. PAIR FORM AND ITS PROOF. Every pair below is given as an ANCHOR and an ADD.
    The TO is the ANCHOR, then one newline, then the ADD; nothing else changes.
    The reviewer ran the containment test MECHANICALLY over all twelve pairs
    before emission and it printed `TO contains FROM: true` for every one, so
    all twelve are APPEND-shaped and NO "FROM 0x" count is ordered for any of
    them (§4.9, §3 checklist item 15). Each ANCHOR was measured to occur
    EXACTLY ONCE in its own target file at the round base.
 5. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE write (PLANF021R22) is the slice PLUS one
    terminator. An APPEND to a record (RECORD22, CONTRACTCLOCK) is one newline,
    then the slice, then one terminator, so the target keeps exactly one.
 6. THE LEDGER IS APPEND-ONLY. No older entry is opened or edited (R-0470).
 7. Run no formatter or linter that rewrites a file in place. Create and merge
    NO pull request: F021 is mid-feature. Push the branch after C5. Run NO
    destructive check and create NO worktree: the red control for C4's contract
    was already reproduced by the reviewer and is re-run by it at the verdict.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 417
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 255 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C5; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2, C3 and C4. C5's own reading
     is ordered NOWHERE — §3 item 31 leaves it to the next session. Report also,
     as the reading THIS round owes from the last, that the R21 handback commit
     `bf0c50bf` is single-parent and touches `.agent/handoff.md` alone at 41
     insertions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r22.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you read, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r22.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their marker LINES —
     `<<<SLICE `/`<<<END ` for the two whole texts, `<<<PAIR `/`<<<ANCHOR`/
     `<<<ADD`/`<<<ENDPAIR` for the twelve pairs. Report how many pairs, how many
     whole-text slices, and how many CONTENT lines that extractor printed, and
     re-measure constraint 8's two numerals from that same blob against caps.
 G4  THE PAIRS AT C3 AND C4. For EACH of the twelve, report over its target
     file: the ANCHOR's count at the round base, which must be EXACTLY 1; and
     at the commit that applied it, the count of ANCHOR-plus-newline-plus-ADD,
     which must be EXACTLY 1. No FROM-zero count is ordered — constraint 4 says
     why. Report the twelve rows as a table, not as a sentence.
 G5  THE CONTRACT APPEND at C4, as ORDERED EQUALITY (R-0531, because this slice
     is CODE and its lines repeat structurally): the pre-commit blob of
     `tests/ui_contracts/test_brain_stream_ring.py` is a byte-exact PREFIX of
     the post-commit file, the remainder is EXACTLY one newline plus
     CONTRACTCLOCK plus one newline, and the lines C4's diff ADDS to that file
     are exactly the slice's lines IN ORDER. Report the remainder's sha256,
     bytes and lines, and the file's bytes and lines before and after.
 G6  `.agent/plan.md` at C1 equals PLANF021R22 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare slice
     that must exit 1. Report both exit codes, that the last byte is a newline,
     `^## Goal$` 1 and `^## Next Steps$` 1. THE LINE-COUNT CLAUSE IS MEASURED:
     the reviewer counted PLANF021R22 at 46 lines, so the file is 46 lines and
     `wc -l` must read EXACTLY 46, satisfying AGENTS.md's "keep it short (<50
     lines)". If the count you measure is not 46, STOP and report — do NOT trim
     the file to reach it, which is the error R-0654 records.
 G7  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD22 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list followed
     by RECORD22's own units, ELEMENTWISE over the whole list, not at the tail;
     report N at both points and RECORD22's unit count, measured by the reviewer
     as TWO — the gate entry and the DECISION. NEGATIVE CONTROL: alter one
     printable byte of the C2 file's FIRST paragraph at equal length; BOTH
     readers must REJECT it and ACCEPT the true file. Name the offset and the
     change.
 G8  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R22`; the MAXIMUM registered id. NO id
     is minted and none resolved, so `- R-` reads 218 at BOTH points with both
     DISTINCT, the maximum R-0655 at both, `Done: R-` and `Landed: ` 0 at both,
     `Gate: R` keys 20 then 21 both DISTINCT, `Gate: R22` 0 then 1.
 G9  THE SUITES, at C4 in the PRIMARY checkout, SERIALLY, from the directory
     each command names — a shell left elsewhere makes the pytest ones exit 4
     having run no test, which is vacuous and not green. Never run two at once.
     Report each one's exit code, its working directory, and its total, counting
     BY PASSED PLUS SKIPPED:
       in `apps/ui`: `npx tsc --noEmit` — exit 0 with output EMPTY. THIS IS THE
       LOAD-BEARING GATE OF THIS ROUND. Vitest does not typecheck: the
       reviewer's own dry run was GREEN under vitest while `tsc` was RED on a
       deps literal in `brainStreamSession.test.ts` the block had missed, and
       the twelfth pair exists because `tsc` caught it.
       in `apps/ui`: `npm run test:unit` — 15 files and 209 tests, the base's 15
       and 207 plus the TWO cases DEPSFORWARDCASE and BROWSERNOWCASE add.
       from the repository root: `python3 -m pytest tests/ui_contracts/ -q -rf`
       — 469, the base's 465 plus the FOUR cases CONTRACTCLOCK adds.
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
     `.agent/authored/f021-r22.md` and `.agent/last_block.md` ARE the block and
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
            heading (R-0494). `## Next` states that the next round is R23, which
            puts `receivedAtMs` on the frame event — `brainStreamDriver.ts`'s
            event union and `brainStreamHost.ts`'s `tell`, stamped from the
            clock THIS round installed — and that DECISION F021 D6 in
            `.agent/live_review.md` at C2 holds the four-round decomposition.

<<<SLICE PLANF021R22
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
R22 gives the transport an INJECTED CLOCK. DECISION F021 D6 replaced the single
wiring round with four, because `recencyLevel` takes two NUMBERS and this client
holds no numeric instant: a row's `timestamp` is a server-clock string that
`ui_server.py` passes through unparsed. R22 adds `now()` to the environment, the
deps and the host contract; nothing consumes it yet.

## Next Steps
1. R23: the frame event carries `receivedAtMs`, stamped by the host from that
   clock — `brainStreamDriver.ts` and `brainStreamHost.ts` with their tests.
2. R24: the ring's row carries the stamp — `feedRow.ts` and `brainStream.ts`.
3. R25: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
4. R26: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R27, the row click-jump, and T003's
   disabled steering input.
5. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK: R22's dry run was
  green under vitest while `tsc` was red on a deps literal it had missed, so
  `tsc` is the load-bearing gate of every round in this chain.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654 and R-0655 stay routed to a
  paydown branch.
<<<END PLANF021R22

<<<SLICE RECORD22
Gate: R22 — the R21 entry. R21 PASSED ON EVERY ONE OF ITS NINE GATES, EACH RE-MEASURED INDEPENDENTLY BY THE REVIEWER RATHER THAN READ BACK FROM THE HANDBACK. R21 was a record-only round: it recorded R20's verdict, registered R-0655 and corrected in a NEW entry the false numeral R20 left in this ledger, touching no code. TRANSPORT HELD ACROSS ALL FOUR COPIES at sha256 d7ed04859b43ec3a52e6993e96605b13c54fd86849865372a539d70e176c0599 over 22534 bytes and 227 lines. SLICES: the reviewer's own marker-line extractor read 2 slices over 48 CONTENT lines from the committed C0a blob, TOTAL 227 against DECISION F085 D6's 490 and PROSE 179 against D5's 400, both equal to that block's constraint 7. THE PLAN WRITE HELD: `.agent/plan.md` at `e317ed2c` is byte-equal to PLANF021R21 plus one terminating newline and NOT to the bare slice, `wc -l` reads exactly 43 — the MEASURED value that block ordered — with `^## Goal$` 1 and `^## Next Steps$` 1. THE LEDGER APPEND HELD UNDER BOTH READERS: the base blob at `a2740317` is a byte-exact prefix of the `ff33eab4` file, remainder sha256 5b19434918b0663d6d58a3ae5044f99a6b4fdf013772f0a637d5218c263c3aac over 7741 bytes and 6 lines, the file 521496 B / 1130 L before and 529237 B / 1136 L after, units 246 to 249 ELEMENTWISE equal with RECORD21 exactly 3 units, and a negative control at offset 5 inside the FIRST paragraph that BOTH readers rejected while both accepted the true file. THE SETS MOVED ONLY AS ORDERED: `- R-` 217 to 218 all DISTINCT at both points, maximum R-0654 to R-0655, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 19 to 20 both DISTINCT, `Gate: R21` 0 to 1. THE CORRECTION LANDED AND THE OLD ENTRY SURVIVED UNEDITED: over the C2 file `EXACTLY 47` occurs exactly twice, at lines 1128 and 1132 — RECORD20's original and the verbatim quotation of it inside R-0655 — and `EXACTLY 43` exactly once at line 1134, while `git diff a2740317..ff33eab4 -- .agent/live_review.md` adds 6 lines and DELETES 0, so `acb688a9`'s blob is byte-identical at both commits. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root and counting by passed plus skipped: the three state-reading suites 511, the canary 42, and `tests/ui_contracts/` 461 passed plus 4 skipped = 465, UNCHANGED as ordered. THE RANGE HELD: four commits base to C2, every one single-parent, the path set EQUAL to that block's four non-handoff `Change:` paths with both differences EMPTY, insertions 227, 143, 16 and 6 every one under the 500 cap and each agreeing cell by cell with the handback's `## Commits` table, `git ls-files .remedy-wt` 0, `git worktree list` the primary checkout alone, `gh pr list --state open` EMPTY, the LINE-ANCHORED marker sweep 0 in both files a slice landed in, and the reflog read BY OPERATION every row `commit` with `amend`, `rebase` and `cherry` each 0 in that field. THE HANDBACK DECLARED ITS OWN OVERAGE HONESTLY at 71 lines against the 60-line cap with a DECISION D15 cause naming only mandated content, and the `Fortschritt:` line is present verbatim across all three of its lines. WHY R21 IS PASS: every slice is byte-identical to the slices the reviewer extracted itself from the committed blob, both ledger readers accept the true file and reject a same-length mutant, and every numeral the round reports was re-derived by the reviewer rather than copied.

DECISION F021 D6, 2026-08-22, taken by the reviewer under §4 item 7 and recorded here rather than asked: THE SINGLE WIRING ROUND THE PLAN CARRIED SINCE R19 IS UNBUILDABLE AS WRITTEN AND IS REPLACED BY FOUR SMALLER ONES. The plan ordered R22 to make `recency.ts` the NowCard's liveness source AND to drive the feed's scroll container from `feedScroll.ts`. `recencyLevel(lastActionAtMs: number | null, nowMs: number)` takes two NUMBERS, and measured at `bf0c50bf` this client holds no numeric instant at all: `FeedRow.timestamp` is a STRING that `feedRowOf` copies out of the safe envelope, `_safe_event_summary` fills it from the run log's own `timestamp`, and `ui_server.py` passes that through unparsed and empty where the log carries none. CHOSEN: stamp each frame on ARRIVAL from the CLIENT's clock, installed as an injected dependency — R22 the clock, R23 the frame event's `receivedAtMs`, R24 the ring's row, R25 the NowCard's badge and dot, R26 the feed's scroll container and pill. Both operands of the subtraction then sit on ONE clock, so the skew case cannot arise. CONSIDERED AND REJECTED: parsing the envelope's string, because a server clock running BEHIND the client yields a large positive elapsed and the dot reads a working agent as idle — the exact failure `recency.ts` names as the one it must never make — and an empty or unparsable stamp yields NaN, which falls through every window comparison to `idle` for the same wrong reason. CONSIDERED AND REJECTED: holding the stamp in the NowCard as component state, which touches no existing file but resets on every remount and measures when the CARD first saw an action rather than when the CLIENT received it. REVERSE THIS by deleting this paragraph and restoring the plan's single R22; the cost is that the dot has no honest number to read.
<<<END RECORD22

<<<PAIR HOSTDEPSNOW apps/ui/src/api/brainStreamHost.ts
<<<ANCHOR
  schedule(ms: number, resume: () => void): () => void;
<<<ADD
  /** The client's own clock. Injected like every other capability here, so a
   *  test hands it a counter and a browser hands it Date.now, and no module in
   *  this chain has to reach for a global to learn what time it is. */
  now(): number;
<<<ENDPAIR

<<<PAIR ENVNOW apps/ui/src/api/brainStreamDeps.ts
<<<ANCHOR
  setTimer(ms: number, resume: () => void): () => void;
<<<ADD
  /** The client's own clock, carried beside the transport whose frames it will
   *  stamp. Injected for the same reason the timer is: real time is the one
   *  dependency a headless test cannot wait for. */
  now(): number;
<<<ENDPAIR

<<<PAIR DEPSRETURNNOW apps/ui/src/api/brainStreamDeps.ts
<<<ANCHOR
    schedule(ms: number, resume: () => void): () => void {
      return env.setTimer(ms, resume);
    },
<<<ADD
    now(): number {
      return env.now();
    },
<<<ENDPAIR

<<<PAIR GLOBALSDATE apps/ui/src/api/brainStreamDeps.ts
<<<ANCHOR
  clearTimeout(handle: unknown): void;
<<<ADD
  /** Taken as an injected global like the others rather than called directly,
   *  so a test can present a clock it controls without touching real time.
   *  `window.Date` satisfies this structurally, which is what keeps
   *  RemedyShell.tsx's `browserBrainStreamEnv(window)` compiling unchanged. */
  Date: { now(): number };
<<<ENDPAIR

<<<PAIR BROWSERNOW apps/ui/src/api/brainStreamDeps.ts
<<<ANCHOR
    setTimer(ms: number, resume: () => void): () => void {
      const handle = globals.setTimeout(resume, ms);
      return (): void => { globals.clearTimeout(handle); };
    },
<<<ADD
    now(): number {
      return globals.Date.now();
    },
<<<ENDPAIR

<<<PAIR HOSTFAKENOW apps/ui/src/api/brainStreamHost.test.ts
<<<ANCHOR
    schedule(ms: number, resume: () => void): () => void {
      waits.push(ms);
      resume();
      return () => { events.push({ kind: "timer" }); };
    },
<<<ADD
    now(): number {
      return 1000;
    },
<<<ENDPAIR

<<<PAIR SESSIONFAKENOW apps/ui/src/api/brainStreamSession.test.ts
<<<ANCHOR
    schedule(ms: number, resume: () => void): () => void {
      waits.push({ ms, resume });
      return () => {};
    },
<<<ADD
    now(): number {
      return 2000;
    },
<<<ENDPAIR

<<<PAIR RECORDERNOW apps/ui/src/api/brainStreamDeps.test.ts
<<<ANCHOR
      setTimer(ms: number, _resume: () => void): () => void {
        timers.push(ms);
        return (): void => { timers.push(-ms); };
      },
<<<ADD
      now(): number {
        return 4242;
      },
<<<ENDPAIR

<<<PAIR DEPSFORWARDCASE apps/ui/src/api/brainStreamDeps.test.ts
<<<ANCHOR
  it("hands the backoff straight to the environment's timer", () => {
    const r = recorder();
    const cancel = createBrainStreamHostDeps("job-1", r.env).schedule(250, () => {});
    cancel();
    expect(r.timers).toEqual([250, -250]);
  });
<<<ADD

  it("reads the clock through the environment rather than a real one", () => {
    const r = recorder();
    expect(createBrainStreamHostDeps("job-1", r.env).now()).toBe(4242);
  });
<<<ENDPAIR

<<<PAIR GLOBALSFAKEDATE apps/ui/src/api/brainStreamDeps.test.ts
<<<ANCHOR
      setTimeout(resume: () => void, _ms: number): unknown { resume(); return "handle"; },
      clearTimeout(handle: unknown): void { cleared.push(handle); },
<<<ADD
      Date: { now: (): number => 777 },
<<<ENDPAIR

<<<PAIR BROWSERNOWCASE apps/ui/src/api/brainStreamDeps.test.ts
<<<ANCHOR
  it("cancels a scheduled resume through the global it was given", () => {
    const g = globals();
    let resumed = 0;
    browserBrainStreamEnv(g).setTimer(10, () => { resumed += 1; })();
    expect(resumed).toBe(1);
    expect(g.cleared).toEqual(["handle"]);
  });
<<<ADD

  it("reads the clock off the injected global, never a real one", () => {
    expect(browserBrainStreamEnv(globals()).now()).toBe(777);
  });
<<<ENDPAIR

<<<PAIR CONTRACTHOSTPATH tests/ui_contracts/test_brain_stream_ring.py
<<<ANCHOR
DRIVER = API_DIR / "brainStreamDriver.ts"
<<<ADD
HOST = API_DIR / "brainStreamHost.ts"
<<<ENDPAIR

<<<SLICE CONTRACTCLOCK

class TestTheTransportClockIsInjected:
    """T5_F021's activity dot needs to know how long ago the agent last acted.
    The envelope's own `timestamp` is a server-clock STRING that ui_server.py
    passes through unparsed, and empty when the run log carries none, so the
    dot is stamped on ARRIVAL instead — both operands on one clock, so a skewed
    server can never read as a dead agent. That stamp is only honest if the
    clock is injected: a module calling Date.now() directly cannot be tested
    without waiting for real time, and this suite pins the seam rather than the
    value."""

    def test_the_host_contract_asks_for_a_clock(self):
        code = strip_ts_comments(HOST.read_text())
        assert "now(): number;" in code, (
            "BrainStreamHostDeps must name the clock it is handed"
        )

    def test_the_environment_carries_the_clock_to_the_deps(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "return env.now();" in code, (
            "createBrainStreamHostDeps forwards the injected clock, never its own"
        )

    def test_the_browser_environment_reads_the_clock_off_its_global(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "return globals.Date.now();" in code, (
            "the one real clock is bound from the injected global, as EventSource is"
        )

    def test_no_module_in_the_transport_chain_calls_the_clock_directly(self):
        for path in (HOST, DEPS, DRIVER, STATE):
            code = strip_ts_comments(path.read_text())
            assert "Date.now()" not in code.replace("globals.Date.now()", ""), (
                f"{path.name} reads a real clock; inject it instead"
            )
<<<END CONTRACTCLOCK
