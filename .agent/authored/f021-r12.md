── STEP RING — F021 ──
Goal:        Build the bounded event ring DECISION F021 D5 rules, in the STATE
             layer only: `recent` and `recentDropped` on `BrainStreamState`,
             appended INSIDE `receiveBrainFrame` behind its existing replay
             guard, bounded at `BRAIN_RECENT_LIMIT`, the drop counted rather
             than silent. `feedRowOf` — built at R9, deliberately uncalled
             since — becomes the projection it feeds. Publishing on
             `BrainStreamView` is R13. The round also records R11's PASS.

Fortschritt: ~45 % (T001 fertig · T002 laeuft — die Projektion Frame→Zeile ist
             gebaut, dieser Block haengt den beschraenkten Ring dahinter; die
             Veroeffentlichung auf der View und die Komponenten folgen)
             — Schaetzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R11 verdict
             · C3 the ring, its vitest cases and its Python source contract ·
             C4 the handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f021-r12.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `apps/ui/src/api/brainStream.ts` (C3) ·
             `apps/ui/src/api/brainStream.test.ts` (C3) ·
             `tests/ui_contracts/test_brain_stream_ring.py` (NEW, C3) ·
             `.agent/handoff.md` (C4).
             Resolve any count in this block against that list.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger commit because the plan must be current before it (§3 checklist
    item 23). ROUND BASE is `a8bb037d9f539dfcae771d0020239cf6b75154a5` and is
    the commit every "round base" in this block names.
 3. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. R11 passed every gate
    under the reviewer's own re-measurement, so RECORD11 registers nothing and
    writes no `Done:`/`Landed:` line. 213 open, max R-0650, next free R-0651.
 4. THE NEWLINE CONVENTION, STATED PER SLICE KIND — R-0650's fix, applied and
    not merely described. Every slice is quoted WITHOUT a trailing newline. A
    WHOLE-FILE replacement (PLANF021R12) and a NEW FILE (RINGCONTRACT) are each
    the slice PLUS one terminator. An APPEND (RECORD11, TESTRING) is one
    newline, then the slice, then one terminator, so the target keeps exactly
    one. A FROM/TO PAIR substitutes in place, neither side carrying a
    terminator and the file's own untouched. The gates match each kind.
 5. PAIRS BEFORE APPENDS (R-0639). Apply the six pairs FIRST, each as ONE
    substitution of its first and only occurrence, and only then append
    TESTRING.
 6. THE RING GOES IN `receiveBrainFrame` AND NOWHERE ELSE — not in
    `stepBrainStream` in `apps/ui/src/api/brainStreamDriver.ts`, not in
    `dispatch` in `apps/ui/src/api/brainStreamRunner.ts`. That function returns
    `state` UNCHANGED for a frame at or behind the held position, so an append
    written there is the only one a reconnect replay cannot duplicate. Do NOT
    edit `brainStreamRunner.ts` at all: `recent` on `BrainStreamView` is R13's
    work, and the typecheck passes without it because the view builds its
    object field by field rather than spreading the state.
 7. Run no formatter or linter that rewrites a file in place; `npm run lint` in
    `apps/ui` is RED at base (R-0622), is not a gate here and must not be
    "fixed" in passing. Create and merge NO pull request: F021 is mid-feature.
    Push the branch.
 8. Block size, measured on these final bytes AFTER the last edit: TOTAL 490
    lines, exactly DECISION F085 D6's cap, and PROSE — TOTAL minus the slice
    CONTENT lines — 236 against DECISION F085 D5's 400. Markers count as prose.

Done when:
 G1  `.agent/STOP` is ABSENT immediately before C0a and again before C4; the
     branch is `feature/f021-live-activity-feed`; `git status --porcelain`
     prints 0 lines after each of C0a, C0b, C1, C2 and C3. C4's own reading is
     ordered NOWHERE — §3 item 31 leaves it to the next round's gate.
 G2  TRANSPORT: sha256 over `.agent/authored/f021-r12.md` at C0a, over
     `.agent/last_block.md` at C0b, over the bytes you received, and over the
     reviewer's emitted copy at `.remedy-wt/f021-r12.md` are all equal. Write
     C0b FROM the committed C0a blob. Report the digest, bytes and lines.
 G3  SLICES: extract them from the COMMITTED C0a blob by their `<<<SLICE `/
     `<<<END ` marker LINES; report how many slices and how many CONTENT lines
     that extractor printed, and re-measure constraint 8's two numerals from
     that same blob against their caps.
 G4  `.agent/plan.md` at C1 equals PLANF021R12 PLUS ONE TERMINATING NEWLINE.
     Prove it with `cmp` at exit 0 against that byte string, built from the
     slice extracted from the committed C0a blob, with a NEGATIVE CONTROL
     against the bare slice that must exit 1. Report both exit codes, that the
     last byte is a newline, `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` ≤ 50.
 G5  THE LEDGER APPEND at C2, under TWO INDEPENDENT READERS. Read the base blob
     with `git show <round base>:<path>` into memory or scratch under
     `.remedy-wt/`; never overwrite a tracked file to read an older revision
     (self_drive_protocol.md guardrail G5). Reader (a): the base blob is a
     byte-exact PREFIX of the C2 file, remainder EXACTLY one newline plus
     RECORD11 plus one newline — report its sha256, byte and line counts, and
     the file's byte and line counts before and after. Reader (b), SET-WISE:
     strip the one trailing terminator from BOTH blobs, split each on the blank
     line into units, and confirm the C2 unit LIST equals the base list
     followed by RECORD11's own units, ELEMENTWISE over the whole list, not at
     the tail; report N at both points and RECORD11's unit count, measured by
     the reviewer as ONE. NEGATIVE CONTROL: alter one printable byte of the C2
     file's FIRST paragraph at equal length; BOTH readers must REJECT it and
     ACCEPT the true file. Name the offset and the change.
 G6  THE LEDGER SETS, line-anchored at line start, at the round base then C2:
     `- R-` entries and how many DISTINCT; `Done: R-`; `Landed: `; `Gate: R`
     keys and how many DISTINCT; `Gate: R12`; the MAXIMUM registered id.
     Nothing is minted, so `- R-` reads 213 at BOTH points with both DISTINCT,
     the maximum R-0650 at BOTH, `Done: R-` and `Landed: ` 0 at both, `Gate: R`
     keys 11 then 12 both DISTINCT, `Gate: R12` 0 then 1.
 G7  THE SIX PAIRS, at C3, counted by WHOLE-STRING search over raw bytes rather
     than line by line. Each FROM count in its target at the ROUND BASE must be
     exactly 1. At C3 the expected counts DIFFER BY PAIR SHAPE, as the reviewer
     measured on a dry run: SRC1 and SRC2A are APPEND-SHAPED — their TO text
     CONTAINS their FROM text — so each reads FROM 1 and TO 1, and a gate
     demanding FROM 0 would fail on a correct application (R-0640); SRC2B,
     SRC3A, SRC3B and TESTIMPORT are REPLACING and each reads FROM 0 and TO 1.
     Report all eighteen numbers. If any FROM count at the round base is not 1,
     STOP and report rather than choosing an occurrence.
 G8  THE CODE APPEND at C3: `apps/ui/src/api/brainStream.test.ts` is, at the
     round base WITH TESTIMPORT's substitution applied in memory, a byte-exact
     PREFIX of that file at C3, remainder EXACTLY one newline plus TESTRING
     plus one newline. Report its sha256, byte and line counts, and say the
     prefix side is the substituted blob. Do NOT use a per-line count: code
     repeats lines structurally and such a reader accepts wrong bytes (R-0531).
 G9  THE NEW FILE at C3: `tests/ui_contracts/test_brain_stream_ring.py` did not
     exist at the round base — `git ls-tree <round base> -- <that path>` prints
     NOTHING — and at C3 equals RINGCONTRACT plus one terminating newline, by
     `cmp` at exit 0 with a NEGATIVE CONTROL at exit 1. Report both codes.
G10  TYPECHECK, at C3, from `apps/ui`: `npx tsc --noEmit`. Report the exit code
     and the working directory. The reviewer measured exit 0 with EMPTY output
     at the round base, and exit 0 over this block's applied `brainStream.ts`
     and its transitive imports on the dry run, so any output here is new.
G11  VITEST, at C3, from `apps/ui` in the PRIMARY checkout: `npx vitest run`. A
     fresh worktree has no `node_modules` and reports a vacuous red (R-0518),
     so this runs in the primary checkout and leaves the tree untouched. Report
     the exit code, the file count, the test count, and its RISE over the round
     base, which must be exactly the 5 cases TESTRING defines. Its colour rests
     on your transcript — `npx vitest` is denied to the reviewer — hence G12.
G12  THE RED CONTROL, on the Python contract, needing no `node_modules`. In a
     disposable worktree under `.remedy-wt/` whose name no directory already
     uses, check out C3 and confirm
     `python3 -m pytest tests/ui_contracts/test_brain_stream_ring.py -q -rf`
     is GREEN there first — an already-red tree cannot fail honestly (R-0364).
     Then, in that worktree's `apps/ui/src/api/brainStream.ts`, move the append
     AHEAD of the replay guard: take these three consecutive lines
       `  if (state.lastSeq !== null && frame.seq <= state.lastSeq) return state;`
       `  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;`
       `  const appended = [...state.recent, feedRowOf(frame)];`
     and rewrite them in the order appended, guard, isGap — that IS the
     reconnect-duplication defect D5 forbids. Re-run. EXACTLY ONE test must
     fail, and it must be
     `TestAppendSitsBehindTheReplayGuard::test_the_replay_guard_returns_before_the_append`.
     Report the failing name, the pass and fail counts and the assertion text;
     the reviewer measured 1 failed, 8 passed on the dry run. Prune the tree.
G13  THE PYTHON SUITES, at C3 in the PRIMARY checkout, SERIALLY, from the
     REPOSITORY ROOT — a shell left in `apps/ui` makes these exit 4 having run
     no test, which is vacuous and not green. Report each one's exit code, the
     working directory, and the total, counting BY PASSED PLUS SKIPPED:
       `python3 -m pytest tests/ui_contracts/ -q -rf` — 430 at the round base;
       RINGCONTRACT adds 9 test functions, which the reviewer counted by
       running that file alone on the dry run, so the total must read 439.
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
            (R-0494). `## Next` states that R13 publishes `recent` on
            `BrainStreamView`, that `publish()` compares the ring BY REFERENCE
            — sound only because `receiveBrainFrame` returns the identical
            state object when it drops a replay — and that `cachedView` is
            seeded FROM the initial state, not a fresh `[]`, or the very first
            publish fires on nothing.

<<<SLICE SRC1 FROM
// so the reconnect, gap and status rules live here where they can be tested.
<<<END SRC1 FROM

<<<SLICE SRC1 TO
// so the reconnect, gap and status rules live here where they can be tested.
import { feedRowOf } from "./feedRow";
import type { FeedRow } from "./feedRow";

// One-directional at RUNTIME though feedRow.ts names this module back: it takes
// `BrainStreamFrame` with `import type`, which TypeScript erases, so the emitted
// graph is brainStream -> feedRow -> humanize and terminates.
<<<END SRC1 TO

<<<SLICE SRC2A FROM
export interface BrainStreamState {
<<<END SRC2A FROM

<<<SLICE SRC2A TO
/** How many projected rows the ring holds. Nothing upstream supplies a bound —
 *  `packages/orchestration/ui_server.py` caps concurrent streams per job at
 *  SSE_MAX_STREAMS_PER_JOB and caps the event COUNT nowhere — so the client
 *  picks one: far past the handful a card shows, far short of a memory
 *  concern (DECISION F021 D5). */
export const BRAIN_RECENT_LIMIT = 500;

export interface BrainStreamState {
<<<END SRC2A TO

<<<SLICE SRC2B FROM
  /** Consecutive failed connection attempts; reset by a successful open. */
  attempt: number;
}

/** A client that holds nothing yet, and does not pretend to be live. */
export function initialBrainStreamState(): BrainStreamState {
  return { status: "reconnecting", lastSeq: null, gapDetected: false, attempt: 0 };
}
<<<END SRC2B FROM

<<<SLICE SRC2B TO
  /** Consecutive failed connection attempts; reset by a successful open. */
  attempt: number;
  /** The bounded ring of projected feed rows, OLDEST FIRST and at most
   *  BRAIN_RECENT_LIMIT of them. This is the feed's only data path. */
  recent: readonly FeedRow[];
  /** How many rows the ring has DROPPED past its bound. The drop is never
   *  silent: above zero the feed says so and points at the timeline. */
  recentDropped: number;
}

/** A client that holds nothing yet, and does not pretend to be live. */
export function initialBrainStreamState(): BrainStreamState {
  return {
    status: "reconnecting", lastSeq: null, gapDetected: false, attempt: 0,
    recent: [], recentDropped: 0,
  };
}
<<<END SRC2B TO

<<<SLICE SRC3A FROM
 *  at or behind the held position is a replay and is dropped. */
<<<END SRC3A FROM

<<<SLICE SRC3A TO
 *  at or behind the held position is a replay and is dropped. The projected
 *  feed row is appended HERE, behind that same early return — the only
 *  placement a reconnect replay cannot duplicate, since the runner's dispatch
 *  and the driver's reducer both see a frame before the guard has ruled on it
 *  (DECISION F021 D5). Dropping a replay returns the IDENTICAL state object,
 *  ring included, which is what lets a reader compare the ring by reference. */
<<<END SRC3A TO

<<<SLICE SRC3B FROM
  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;
  return {
    ...state,
    status: state.status === "delayed" ? "delayed" : "live",
    lastSeq: frame.seq,
    gapDetected: state.gapDetected || isGap,
    attempt: 0,
  };
}
<<<END SRC3B FROM

<<<SLICE SRC3B TO
  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;
  const appended = [...state.recent, feedRowOf(frame)];
  const overflow = Math.max(0, appended.length - BRAIN_RECENT_LIMIT);
  return {
    ...state,
    status: state.status === "delayed" ? "delayed" : "live",
    lastSeq: frame.seq,
    gapDetected: state.gapDetected || isGap,
    attempt: 0,
    recent: overflow === 0 ? appended : appended.slice(overflow),
    recentDropped: state.recentDropped + overflow,
  };
}
<<<END SRC3B TO

<<<SLICE TESTIMPORT FROM
  BRAIN_BACKOFF_CAP_MS, brainBackoffDelayMs, degradeBrainStream, failBrainStream,
  initialBrainStreamState, openBrainStream, receiveBrainFrame, repairBrainGap, resumeEventId,
<<<END TESTIMPORT FROM

<<<SLICE TESTIMPORT TO
  BRAIN_BACKOFF_CAP_MS, BRAIN_RECENT_LIMIT, brainBackoffDelayMs, degradeBrainStream,
  failBrainStream, initialBrainStreamState, openBrainStream, receiveBrainFrame,
  repairBrainGap, resumeEventId,
<<<END TESTIMPORT TO

<<<SLICE TESTRING
describe("the recent ring", () => {
  it("a fresh client holds no rows and has dropped none", () => {
    const s = initialBrainStreamState();
    expect(s.recent).toEqual([]);
    expect(s.recentDropped).toBe(0);
  });

  it("each accepted frame appends one projected row, oldest first", () => {
    const s = drive(initialBrainStreamState(), [4, 5, 6]);
    expect(s.recent.map((r) => r.seq)).toEqual([4, 5, 6]);
    expect(s.recentDropped).toBe(0);
  });

  it("a replayed frame appends nothing and returns the identical state", () => {
    const s = drive(initialBrainStreamState(), [1, 2]);
    const again = receiveBrainFrame(s, { seq: 2, event: { seq: 2 } });
    expect(again).toBe(s);
    expect(again.recent).toBe(s.recent);
    expect(again.recent.map((r) => r.seq)).toEqual([1, 2]);
  });

  it("the ring never grows past BRAIN_RECENT_LIMIT, dropping the OLDEST", () => {
    const seqs = Array.from({ length: BRAIN_RECENT_LIMIT + 5 }, (_, i) => i + 1);
    const s = drive(initialBrainStreamState(), seqs);
    expect(s.recent.length).toBe(BRAIN_RECENT_LIMIT);
    expect(s.recentDropped).toBe(5);
    expect(s.recent[0].seq).toBe(6);
    expect(s.recent[s.recent.length - 1].seq).toBe(BRAIN_RECENT_LIMIT + 5);
  });

  it("the row carries the humanized projection, not the raw envelope", () => {
    const s = receiveBrainFrame(initialBrainStreamState(), {
      seq: 3, event: { event: "task_run_started", outcome: "ok" },
    });
    expect(s.recent[0].kind).toBe("task_run_started");
    expect(s.recent[0].known).toBe(true);
    expect(s.recent[0].outcome).toBe("ok");
  });
});
<<<END TESTRING

<<<SLICE RINGCONTRACT
"""Contract tests for WHERE the recent-ring append lives.

Behaviour is pinned by vitest in brainStream.test.ts; this suite pins the fact
a behavioural test cannot. The append must sit inside `receiveBrainFrame`
behind the replay guard and appear in neither the driver nor the runner
(DECISION F021 D5): a ring appended in `dispatch` passes every behavioural test
and still duplicates a row on reconnect. Assertions run against
COMMENT-STRIPPED source, or prose above a definition would satisfy a guard
meant for the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO_ROOT / "apps" / "ui" / "src" / "api"
STATE = API_DIR / "brainStream.ts"
DRIVER = API_DIR / "brainStreamDriver.ts"
RUNNER = API_DIR / "brainStreamRunner.ts"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files hold no string literal carrying
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def receive_body(code: str) -> str:
    """`receiveBrainFrame` alone, from its signature to the next top-level
    export. Over the WHOLE file the assertions below would pass on an append
    living anywhere in it, which is the defect they exist to catch."""
    start = code.index("export function receiveBrainFrame(")
    return code[start:code.index("\nexport ", start + 1)]


class TestTheGuardsAreReal:
    def test_stripper_removes_a_comment_the_file_really_carries(self):
        raw = STATE.read_text()
        assert "// Pure, framework-free client state" in raw
        assert "Pure, framework-free client state" not in strip_ts_comments(raw)

    def test_the_body_slice_is_narrower_than_the_whole_file(self):
        code = strip_ts_comments(STATE.read_text())
        assert 0 < len(receive_body(code)) < len(code) / 2


class TestAppendSitsBehindTheReplayGuard:
    def test_the_bound_is_a_named_exported_constant(self):
        code = strip_ts_comments(STATE.read_text())
        assert "export const BRAIN_RECENT_LIMIT = 500;" in code

    def test_state_carries_the_ring_and_the_drop_count(self):
        code = strip_ts_comments(STATE.read_text())
        assert "recent: readonly FeedRow[];" in code, "the ring must be readonly"
        assert "recentDropped: number;" in code, "a silent drop is what D5 forbids"

    def test_the_projection_is_called_inside_receive_brain_frame(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "feedRowOf(frame)" in body

    def test_the_replay_guard_returns_before_the_append(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        guard = body.index("frame.seq <= state.lastSeq) return state;")
        assert guard < body.index("feedRowOf(frame)"), (
            "an append ahead of the guard duplicates a row on reconnect replay"
        )

    def test_the_bound_is_applied_where_the_append_happens(self):
        body = receive_body(strip_ts_comments(STATE.read_text()))
        assert "BRAIN_RECENT_LIMIT" in body


class TestNoSecondAppendSite:
    def test_the_driver_does_not_project_rows(self):
        code = strip_ts_comments(DRIVER.read_text())
        assert "feedRowOf" not in code, "the driver sees frames before the guard"

    def test_the_runner_does_not_project_rows(self):
        code = strip_ts_comments(RUNNER.read_text())
        assert "feedRowOf" not in code, "dispatch runs for replays too"
<<<END RINGCONTRACT

<<<SLICE PLANF021R12
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
R12 builds the STATE half of the bounded ring DECISION F021 D5 rules: `recent`
and `recentDropped` on `BrainStreamState`, appended inside `receiveBrainFrame`
behind its replay guard, bounded at `BRAIN_RECENT_LIMIT` with the drop counted.
It also records the R11 verdict, which was PASS on every gate.

## Next Steps
1. R13 publishes the ring on `BrainStreamView` in `brainStreamRunner.ts`.
   `publish()` compares `recent` BY REFERENCE, sound only because
   `receiveBrainFrame` returns the identical state object when it drops a
   replay, and `cachedView` is seeded FROM the initial state rather than from a
   fresh `[]`, or the very first publish fires on nothing.
2. R14 builds the feed and NowCard over fixture streams, with the scroll
   discipline that never yanks a reader who has scrolled up, and the
   dropped-rows notice that points at the timeline.
3. R15 onward T003: graph-focus wiring, the disabled steering input, and the
   additive envelope field DECISION F021 D2 permits.

## Risks
- The view-identity contract `createBrainStreamRunner` documents is what R13 is
  most likely to break: `useSyncExternalStore` compares with `Object.is`, so a
  freshly built array on every call re-renders forever.
- `npx vitest run` is DENIED to the reviewer's session class, so a frontend
  round's vitest colour rests on the worker's transcript. `npx tsc --noEmit`
  and the Python source contracts ARE reviewer-runnable, so every frontend
  round carries a Python red control the reviewer reproduces itself.
- A block's newline convention is stated PER SLICE KIND: R-0650 the hard way.
- No code defect of F021 is open; R-0403, R-0607, R-0608, R-0609, R-0611,
  R-0613 and R-0622 stay routed to a paydown branch.
<<<END PLANF021R12

<<<SLICE RECORD11
Gate: R12 — the R11 entry. R11 PASSED ON EVERY ONE OF ITS THIRTEEN GATES, RE-MEASURED INDEPENDENTLY BY A NEW SESSION RATHER THAN READ BACK, AND IT MINTS NO FINDING. R11 was a register-and-close round that built nothing. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f021-r11.md` at `8a03d8c6`, `.agent/last_block.md` at `b9a9f606`, that file's working copy, and the bytes the previous reviewer EMITTED, still on disk at `.remedy-wt/f021-r11.md`, are all sha256 d63a7e100cec48034b2946c4b034209d8474618d9ba912d6826abc7bc34310e3 over 21857 bytes and 250 lines. SLICES: 2 over 53 CONTENT lines, TOTAL 250 against DECISION F085 D6's 490 and PROSE 197 against D5's 400, both equal to that block's constraint 9. THE WHOLE-FILE REPLACEMENT at `54b23c4f` is PLANF021R11 plus exactly one terminating newline: `cmp` exits 0 against that byte string and 1 against the bare slice, reporting EOF after byte 2783 in line 48, so the terminator R-0650 named is measurably back. THE APPEND at `17584638` is the round-base blob plus one newline plus RECORD10 plus one newline, remainder sha256 446ae09f36b6ae1c3670a838c356e99c01a029d0d34963e596a8e0958dafddee over 5704 bytes and 6 lines, the file going 467847 bytes to 473551, units 227 plus RECORD10's own 3 to 230 elementwise equal over the whole list, with a mutation at byte offset 2 of the FIRST paragraph — `L` to `Q` at equal length — rejected by both readers while both accept the true file. THE LEDGER ROSE BY EXACTLY ONE: `- R-` 212 to 213 all DISTINCT at both points, maximum id R-0649 to R-0650, `Done: R-` 0 and `Landed: ` 0 at both, `Gate: R` keys 10 to 11 both DISTINCT, `Gate: R11` 0 to 1, `- R-0650 —` 0 to 1 — every value equal to that block's G6 prediction. THE SUITES ARE THIS REVIEWER'S OWN, run serially from the repository root: the three contract suites exit 0 with 511 passed, the canary exit 0 with 42 passed, and `tests/ui_contracts/` exit 0 with 426 passed and 4 skipped. THE RANGE HELD: five commits every one single-parent, the base-to-C2 path set EQUAL to that block's four non-handoff `Change:` paths with both differences EMPTY, 0 paths beginning `apps/`, `packages/` or `tests/`, insertions 250, 116, 10 and 6 every one under the 500 cap, markers 0 in both files a slice landed in, `git ls-files .remedy-wt` 0, `git worktree list` ending with the primary checkout alone, and all five reflog rows `commit:` — amend 0, rebase 0, cherry 0. THE READINGS §3 CHECKLIST ITEM 31 LEFT TO THIS GATE, both owed and both now taken: the R10 handback commit `4f504337` is single-parent and changes `.agent/handoff.md` alone at 44 insertions and 55 deletions, and the R11 handback commit `a8bb037d` is single-parent and changes that file alone at 60 insertions and 61 deletions; both are under the 500-insertion cap, and `git status --porcelain` reads 0 lines at `a8bb037d`, which is HEAD. R-0650'S OWN STORY WAS RE-DERIVED FROM HISTORY RATHER THAN ACCEPTED: `.agent/plan.md` ends with a newline at `7823005d`, does NOT at `b33f0305` where R10's C1 landed it, still does not at `4f504337`, and does again at `54b23c4f`; at `4f504337` it was the ONLY file among `plan.md`, `live_review.md`, `handoff.md`, `last_block.md`, `context.md` and `decisions.md` lacking a terminator, exactly as that finding claims. WHY R11 IS PASS: every gate reproduces under a second session's independent execution, the ledger arithmetic is exact, and the round fixed on disk the defect it registered rather than only describing it.
<<<END RECORD11
