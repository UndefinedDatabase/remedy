── STEP PUBLISH — F021 ──
Goal:        Publish the bounded ring R12 built on `BrainStreamView`, so a
             reader reaches it through the ONE `useBrainStream` call the shell
             already makes. `recent` and `recentDropped` join the view;
             `publish()` compares the ring BY REFERENCE, which is sound only
             because `receiveBrainFrame` returns the identical state object
             when it drops a replay; and `cachedView` is seeded FROM the
             initial state, never from a fresh `[]`. Components are R14. The
             round also records the R12 verdict, which was PASS.

Fortschritt: ~55 % (T001 fertig · T002 fast fertig — Ring gebaut und jetzt auf
             der View veroeffentlicht, Identitaet by reference; es fehlen nur
             noch die Komponenten Feed und NowCard)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R12 verdict
             · C3 the view publication, its vitest cases and its contract ·
             C4 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r13.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/brainStreamRunner.ts` (C3) ·
             `apps/ui/src/api/brainStreamRunner.test.ts` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `a556f0c8bffec5b380d6b22b4af09575c24ed3ff` and is
    the commit every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. R12 passed every gate
    under the reviewer's own re-measurement, so RECORD12 registers nothing and
    writes no `Done:`/`Landed:` line. 213 open, max R-0650, next free R-0651.
 4. THE NEWLINE CONVENTION, PER SLICE KIND. Every slice is quoted WITHOUT a
    trailing newline. A WHOLE-FILE replacement (PLANF021R13) is the slice PLUS
    one terminator. An APPEND (RECORD12, TESTVIEW, CONTRACTVIEW) is one
    newline, then the slice, then one terminator, so the target keeps exactly
    one. A FROM/TO PAIR substitutes in place, neither side carrying a
    terminator and the file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS (R-0639). Apply the five pairs FIRST, each as ONE
    substitution of its first and only occurrence, then the three appends.
 6. THE IDENTITY CONTRACT IS THE POINT OF THIS ROUND. `publish()` compares
    `recent` with `===`, and that is correct ONLY because `receiveBrainFrame`
    returns the IDENTICAL state object — ring array included — for a frame at
    or behind the held position. Do not "fix" it into a deep or element-wise
    comparison: `useSyncExternalStore` compares snapshots with `Object.is`, and
    a view rebuilt on every call re-renders forever. Do not edit
    `apps/ui/src/api/brainStream.ts`; R12 built it and it is correct.
 7. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be
    "fixed" in passing. Create and merge NO pull request: F021 is mid-feature.
    Push the branch.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 415
    lines against DECISION F085 D6's 490, and PROSE — TOTAL minus the slice
    CONTENT lines — 242 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next round's gate. Report
     also, as the reading THIS round owes from the last, that the R12 handback
     commit `a556f0c8` is single-parent and touches `.agent/handoff.md` alone
     at 73 insertions and 61 deletions, under the 500-insertion cap.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r13.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r13.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 8's two numerals from
     that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R13 PLUS ONE TERMINATING NEWLINE, by
     `cmp` at exit 0 against that byte string built from the slice extracted
     from the committed C0a blob, with a NEGATIVE CONTROL against the bare
     slice that must exit 1. Report both exit codes, that the last byte is a
     newline, `^## Goal$` 1, `^## Next Steps$` 1, and `wc -l` at most 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD12 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list
     followed by RECORD12's own units, ELEMENTWISE over the whole list, not at
     the tail; report N at both points and RECORD12's unit count, measured by
     the reviewer as ONE. NEGATIVE CONTROL: alter one printable byte of the C2
     file's FIRST paragraph at equal length; BOTH readers must REJECT it and
     ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R13`; the MAXIMUM registered id.
     Nothing is minted, so `- R-` reads 213 at BOTH points with both DISTINCT,
     the maximum R-0650 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R`
     keys 12 then 13 both DISTINCT, `Gate: R13` 0 then 1.
 G7  THE FIVE PAIRS, at C3, counted by WHOLE-STRING search over raw bytes
     rather than line by line. Each FROM count in its target at the ROUND BASE
     must be exactly 1. At C3 the expected counts DIFFER BY PAIR SHAPE, as the
     reviewer measured on a dry run: RUNNER1 and TESTIMPORT2 are APPEND-SHAPED
     — their TO text CONTAINS their FROM text — so each reads FROM 1 and TO 1,
     and a gate demanding FROM 0 would fail on a correct application (R-0640);
     RUNNER2, RUNNER3 and RUNNER4 are REPLACING and each reads FROM 0 and TO 1.
     Report all fifteen numbers. If any FROM count at the round base is not 1,
     STOP and report rather than choosing an occurrence.
 G8  THE TWO CODE APPENDS at C3, each proven as prefix plus remainder, never by
     a per-line count — code repeats lines structurally and a count-based
     reader is satisfied by the wrong bytes (R-0531).
       `apps/ui/src/api/brainStreamRunner.test.ts` at the round base WITH
       TESTIMPORT2's substitution applied in memory is a byte-exact PREFIX of
       that file at C3, remainder EXACTLY one newline plus TESTVIEW plus one
       newline. Say the prefix side is the substituted blob.
       `tests/ui_contracts/test_brain_stream_ring.py` at the round base is a
       byte-exact PREFIX of that file at C3 — no pair touches it — remainder
       EXACTLY one newline plus CONTRACTVIEW plus one newline.
     Report each remainder's sha256, byte and line counts.
 G9  PEP 8 SPACING ON THE PYTHON APPEND. CONTRACTVIEW opens a new top-level
     class and CARRIES ITS OWN LEADING BLANK LINE — its first line is empty on
     purpose, so the append's one newline plus that blank puts exactly two
     blank lines before `class `. Do not trim it. Report the count of blank
     lines immediately before CONTRACTVIEW's `class ` line in the C3 file: it
     must be 2. Ruff in this repository does not evaluate E301-E306 outside
     preview, so this is COUNTED and not delegated to the linter (R-0558).
G10  TYPECHECK, at C3, from `apps/ui`: `npx tsc --noEmit`. Report the exit code
     and the working directory. The reviewer measured exit 0 with EMPTY output
     at the round base, so any output here is this round's doing.
G11  VITEST, at C3, from `apps/ui` in the PRIMARY checkout: `npx vitest run`. A
     fresh worktree has no `node_modules` and reports a vacuous red (R-0518),
     so this runs in the primary checkout and leaves the tree untouched. Report
     the exit code, the file count, the test count, and its RISE over the round
     base, which must be exactly the 4 cases TESTVIEW defines. The reviewer
     measured 12 files and 173 tests at the round base by counting `it(` in the
     committed sources, so the expected reading is 12 files and 177 tests. Its
     colour rests on your transcript — `npx vitest` is denied to the reviewer.
G12  THE RED CONTROL, on the Python contract, needing no `node_modules`. In a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`
     is GREEN there first — an already-red tree cannot fail honestly (R-0364).
     Then, in that worktree's `apps/ui/src/api/brainStreamRunner.ts`, seed the
     cached view from a fresh array instead of the state by replacing the line
       `    recent: state.recent,`
     that stands inside the `let cachedView` initializer — NOT the identical
     line inside `publish()`, which must be left alone — with
       `    recent: [],`
     That line occurs TWICE in the file; report the count and state that you
     changed the FIRST, the one in the initializer. Re-run. EXACTLY ONE test
     must fail, and it must be
     `TestViewPublishesTheRing::test_cached_view_is_seeded_from_the_state`.
     That mutation is the spurious-first-publish defect this round exists to
     prevent. Report the failing name, the pass and fail counts and the
     assertion text; the reviewer measured 1 failed, 12 passed on the dry run.
     Prune the worktree.
G13  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run
     no test, which is vacuous and not green. Report each one's exit code, the
     working directory, and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 439 at the round base;
       CONTRACTVIEW adds 4 test functions, which the reviewer counted by
       running that file alone on the dry run, so the total must read 443.
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
       tests/regression/test_resource_safety.py -q -rf` — 511 at base, and they
       read `.agent/plan.md`, so they also guard C1.
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf` — canary, 42.
     No docs gate is owed: the `Change:` list holds no `docs/` path.
G14  RANGE, executed at C3 and covering the round base to C3 — NOT to C4,
     because C4 writes the file that must quote this gate and §3 checklist item
     31 forbids ordering a reading the quoting artefact cannot hold. Report:
     the base-to-C3 path set against the seven non-handoff paths of `Change:`,
     the difference EMPTY both ways; every commit single-parent; `git show
     --numstat` and `git diff --numstat` agreeing cell by cell with the
     handback's `## Commits` table (§3 item 28), any disagreement reported
     rather than reconciled; insertions under the 500 cap; `<<<SLICE `/`<<<END `
     0 LINES in every file a slice landed in; `git ls-files .remedy-wt` 0;
     `git worktree list` ending with the primary checkout alone; reflog rows
     with `amend`, `rebase`, `cherry` each 0; and `gh pr list --state open
     --json number,headRefName` — expected EMPTY — with the statement that
     neither `gh pr create` nor `gh pr merge` was run.

Handback:   completion report + rewrite `.agent/handoff.md` with every mandated
            section of docs/agents/handback_template.md, an item-status row for
            each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, ONE LINE
            PER GATE with transcripts kept out of the file (R-0582), and the
            `Fortschritt:` line verbatim across all four of its lines. Report
            its own `wc -l` against the 60-line cap, with a DECISION D15 line
            declaring any overage and its mandated cause. Every `## Commits`
            heading carries that commit's FULL subject, and where a commit
            cannot name its own SHA the role and reason go INSIDE the heading
            (R-0494). `## Next` states that R14 builds the feed and NowCard
            components over the published ring, reading it from the ONE
            `useBrainStream` call `RemedyShell` already makes — no second call
            and no new `EventSource` — and that `recentDropped` above zero is
            what the dropped-rows notice renders.

<<<SLICE RUNNER1 FROM
import type { BrainStreamStatus } from "./brainStream";
<<<END RUNNER1 FROM

<<<SLICE RUNNER1 TO
import type { BrainStreamStatus } from "./brainStream";
import type { FeedRow } from "./feedRow";
<<<END RUNNER1 TO

<<<SLICE RUNNER2 FROM
export interface BrainStreamView {
  status: BrainStreamStatus | null;
  lastSeq: number | null;
  gapDetected: boolean;
}
<<<END RUNNER2 FROM

<<<SLICE RUNNER2 TO
export interface BrainStreamView {
  status: BrainStreamStatus | null;
  lastSeq: number | null;
  gapDetected: boolean;
  /** The bounded ring `receiveBrainFrame` maintains, oldest first. Compared by
   *  REFERENCE below, so it is the same array until a frame is accepted. */
  recent: readonly FeedRow[];
  /** Rows dropped past the bound. Above zero, the feed says so rather than
   *  quietly showing a window (DECISION F021 D5). */
  recentDropped: number;
}
<<<END RUNNER2 TO

<<<SLICE RUNNER3 FROM
  let cachedView: BrainStreamView = {
    status: null,
    lastSeq: null,
    gapDetected: false,
  };
<<<END RUNNER3 FROM

<<<SLICE RUNNER3 TO
  // Seeded FROM `state`, never from a fresh `[]`. `publish` compares the ring
  // by reference, and an empty literal here is a DIFFERENT array from the
  // equally empty one the initial state holds, so the first timer — which
  // changes nothing a reader can see — would announce a change nobody made.
  let cachedView: BrainStreamView = {
    status: null,
    lastSeq: null,
    gapDetected: false,
    recent: state.recent,
    recentDropped: state.recentDropped,
  };
<<<END RUNNER3 TO

<<<SLICE RUNNER4 FROM
    const next: BrainStreamView = {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
    };
    if (next.status === cachedView.status
      && next.lastSeq === cachedView.lastSeq
      && next.gapDetected === cachedView.gapDetected) return;
<<<END RUNNER4 FROM

<<<SLICE RUNNER4 TO
    const next: BrainStreamView = {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
      recent: state.recent,
      recentDropped: state.recentDropped,
    };
    if (next.status === cachedView.status
      && next.lastSeq === cachedView.lastSeq
      && next.gapDetected === cachedView.gapDetected
      && next.recent === cachedView.recent
      && next.recentDropped === cachedView.recentDropped) return;
<<<END RUNNER4 TO

<<<SLICE TESTIMPORT2 FROM
import { createBrainStreamRunner } from "./brainStreamRunner";
<<<END TESTIMPORT2 FROM

<<<SLICE TESTIMPORT2 TO
import { createBrainStreamRunner } from "./brainStreamRunner";
import { BRAIN_RECENT_LIMIT } from "./brainStream";
<<<END TESTIMPORT2 TO

<<<SLICE TESTVIEW
describe("the view publishes the ring", () => {
  it("seeds the cached view from the state, so start alone announces nothing", () => {
    const host = new RecordingHost();
    const runner = createBrainStreamRunner(host);
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.start();
    expect(calls).toBe(0);
    expect(runner.view().recent).toEqual([]);
    expect(runner.view().recentDropped).toBe(0);
  });

  it("carries each accepted frame's projected row onto the view", () => {
    const { runner } = started();
    runner.dispatch(frame(4));
    runner.dispatch(frame(5));
    expect(runner.view().recent.map((r) => r.seq)).toEqual([4, 5]);
  });

  it("holds the ring's identity across a replay, so no re-render is asked for", () => {
    const { runner } = started();
    runner.dispatch(frame(4));
    const before = runner.view();
    runner.dispatch(frame(4));
    expect(runner.view()).toBe(before);
    expect(runner.view().recent).toBe(before.recent);
  });

  it("publishes the drop count once the bound is passed", () => {
    const { runner } = started();
    for (let seq = 1; seq <= BRAIN_RECENT_LIMIT + 3; seq += 1) {
      runner.dispatch(frame(seq));
    }
    expect(runner.view().recent.length).toBe(BRAIN_RECENT_LIMIT);
    expect(runner.view().recentDropped).toBe(3);
  });
});
<<<END TESTVIEW

<<<SLICE CONTRACTVIEW

class TestViewPublishesTheRing:
    """The runner half of DECISION F021 D5. These pin the two facts a
    behavioural test states less directly: that the ring reaches the view at
    all, and that its identity is compared by reference rather than rebuilt."""

    def test_the_view_type_carries_the_ring(self):
        code = strip_ts_comments(RUNNER.read_text())
        start = code.index("export interface BrainStreamView {")
        view = code[start:code.index("}", start)]
        assert "recent: readonly FeedRow[];" in view
        assert "recentDropped: number;" in view

    def test_cached_view_is_seeded_from_the_state(self):
        code = strip_ts_comments(RUNNER.read_text())
        init = code[code.index("let cachedView"):code.index("function view()")]
        assert "recent: state.recent," in init, (
            "a fresh [] here is a different array from the initial state's "
            "ring, so the first timer would announce a change nobody made"
        )
        assert "recent: []" not in init

    def test_publish_compares_the_ring_by_reference(self):
        code = strip_ts_comments(RUNNER.read_text())
        body = code[code.index("function publish()"):code.index("function arm(")]
        assert "next.recent === cachedView.recent" in body, (
            "useSyncExternalStore compares with Object.is; a deep compare here "
            "would still hand back a fresh object and re-render forever"
        )
        assert "next.recentDropped === cachedView.recentDropped" in body

    def test_the_runner_still_does_not_project_rows_itself(self):
        code = strip_ts_comments(RUNNER.read_text())
        assert "feedRowOf" not in code, "the projection belongs behind the guard"
<<<END CONTRACTVIEW

<<<SLICE PLANF021R13
# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R13 publishes the ring on `BrainStreamView`: `recent` and `recentDropped` join
the view, `publish()` compares the ring by reference, and `cachedView` is seeded
from the initial state so the first timer announces nothing. It also records the
R12 verdict, which was PASS on every gate.

## Next Steps
1. R14 builds the feed and NowCard components over the published ring, read
   from the ONE `useBrainStream` call `RemedyShell` already makes — no second
   call, no new `EventSource`. `recentDropped` above zero renders the
   dropped-rows notice that points at the timeline.
2. R15 adds the scroll discipline that never yanks a reader who has scrolled
   up, over fixture streams, gated by a Python source contract.
3. R16 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- `useSyncExternalStore` compares with `Object.is`. Any later edit that rebuilds
  the view or the ring on every call re-renders forever; the contract tests in
  `tests/ui_contracts/test_brain_stream_ring.py` are what hold that line.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. `npx tsc --noEmit`
  and the Python source contracts ARE reviewer-runnable, so every frontend
  round carries a Python red control the reviewer reproduces itself.
- A block's newline convention is stated PER SLICE KIND: R-0650 the hard way.
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
<<<END PLANF021R13

<<<SLICE RECORD12
Gate: R13 — the R12 entry. R12 PASSED ON EVERY ONE OF ITS FOURTEEN GATES, RE-MEASURED INDEPENDENTLY RATHER THAN READ BACK, AND IT MINTS NO FINDING. R12 built the state half of the bounded ring DECISION F021 D5 rules. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r13.md`'s predecessor `.agent/authored/f021-r12.md` at `d2b91200`, `.agent/last_block.md` at `dd194642`, and the bytes the reviewer EMITTED at `.remedy-wt/f021-r12.md` are all sha256 af4a8a005381c749aa3fe625a32f3fd27a95b31a3c9880470b15981d0f1030fd over 29018 bytes and 490 lines. SLICES: 16 over 254 CONTENT lines, TOTAL 490 — exactly DECISION F085 D6's cap — and PROSE 236 against D5's 400, both equal to that block's constraint 8. EVERY SLICE APPLIED BYTE FOR BYTE, verified by the reviewer against its own emitted copy rather than against the worker's report: `.agent/plan.md` at `24c1dc09` equals PLANF021R12 plus one terminating newline and not the bare slice; `tests/ui_contracts/test_brain_stream_ring.py` at `1dae12ca` equals RINGCONTRACT plus one terminating newline and did not exist at the round base, where `git ls-tree` prints nothing; the ledger append at `8daad3b7` is the base blob plus one newline plus RECORD12's predecessor plus one newline, remainder sha256 62373553bbc74bfe4ba9e3571ff508156f22149b3bca9326bab5318f353ae381 over 3484 bytes, units 230 to 231 elementwise equal, mutation at byte offset 2 rejected by both readers; and the code append to `brainStream.test.ts` is the TESTIMPORT-substituted base blob plus one newline plus TESTRING plus one newline, remainder sha256 0f531cedd9be34f7b89460bb5eafc209265e569f871ec01a6d79c864bb32aa1b over 1598 bytes. THE SIX PAIRS BEHAVED BY SHAPE, exactly as that block's G7 predicted from the reviewer's dry run: every FROM 1 at the round base; at C3 the append-shaped SRC1 and SRC2A read FROM 1 and TO 1 while the replacing SRC2B, SRC3A, SRC3B and TESTIMPORT read FROM 0 and TO 1. THE LEDGER IS UNMOVED, as a round minting nothing requires: `- R-` 213 at both points all DISTINCT, maximum R-0650 at both, `Done: R-` and `Landed: ` 0 at both, `Gate: R` keys 11 to 12 both DISTINCT, `Gate: R12` 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially from the repository root: `tests/ui_contracts/` exit 0 with 435 passed and 4 skipped for 439, the three contract suites exit 0 with 511, the canary exit 0 with 42, and `npx tsc --noEmit` in `apps/ui` exit 0 with empty output. THE ONE GATE THE REVIEWER CANNOT RUN WAS CORROBORATED RATHER THAN ACCEPTED: `npx vitest` is denied to that session class, so the worker's reading of 12 files and 173 tests against 168 at the round base was checked by counting `it(` occurrences over the committed test sources at both commits — 168 then 173, a rise of exactly 5, equal to TESTRING's five cases. THE RED CONTROL REPRODUCED IN THE REVIEWER'S OWN DISPOSABLE WORKTREE: green first at 9 passed, then with the append moved ahead of the replay guard exactly 1 failed and 8 passed, the failure being `TestAppendSitsBehindTheReplayGuard::test_the_replay_guard_returns_before_the_append` at `assert 199 < 148`. THE RANGE HELD: six commits base to HEAD every one single-parent, the base-to-C3 path set EQUAL to that block's seven non-handoff `Change:` paths with both differences EMPTY, insertions 490, 459, 28, 2, 169 and 73 every one under the 500 cap, markers 0 in every file a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all reflog rows `commit:` — amend 0, rebase 0, cherry 0. ONE DEVIATION WAS DECLARED AND IS ACCEPTED: the worker opened a SECOND read-only worktree at the round base, with `node_modules` symlinked in, solely to MEASURE the base vitest count rather than accept a recorded figure; it was removed and pruned, and measuring a base rather than assuming it is better discipline than the block ordered, not worse. WHY R12 IS PASS: every slice is byte-identical to the reviewer's own emitted bytes, every gate reproduces under the reviewer's own execution, the one unrunnable gate is corroborated by an independent static count that agrees exactly, and the ring sits behind the replay guard where a reconnect cannot duplicate a row.
<<<END RECORD12
