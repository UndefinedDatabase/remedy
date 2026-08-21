── STEP T003/5 — F008 SSE event stream — ROUND 24 ────────────────────────────
Goal:
 Pin the stream host R23 landed: twelve tests over an injected source, an
 injected snapshot read, an injected tail read and an injected scheduler, plus
 three red controls. Only with this round is the adapter PROVED rather than
 merely compiled. The round also records the R23 verdict.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r24.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R24, applied whole
 C2   `.agent/live_review.md` <- LEDGER24, appended
 C3   `apps/ui/src/api/brainStreamHost.test.ts` <- HOSTTESTS, a NEW file, whole
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r24.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamHost.test.ts`,
 `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r24.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r24.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R24, LEDGER24 and HOSTTESTS, each
 delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of the slice. Every slice is
 newline-terminated with no trailing whitespace on any line. There is NO
 FROM/TO pair: one slice replaces a file whole, one is appended and one
 CREATES a file, so the obligations are byte equality and an ordered append,
 never a containment reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED — not
    jsdom, not happy-dom, not a testing library; `apps/ui/package.json` and
    `apps/ui/package-lock.json`, the only manifests this repository tracks,
    are not edited. `apps/ui/src/api/brainStreamHost.ts` IS NOT EDITED: this
    round adds the tests that pin it and changes nothing they measure. If a
    test fails, report the failure — do not adjust the module to suit it.
 4. No id is minted and no verdict beyond LEDGER24 is written: R-0629 stays
    free, R-0628 stays OPEN with no `Done:` and no `Landed:` line, R-0622
    stays OPEN and no TypeScript parser is added to make lint green.
 5. The post-C4 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G8's suites run in the PRIMARY
    checkout: a fresh worktree has no `apps/ui/node_modules` (R-0518). G9's
    worktree reaches it by SYMLINK — never a copy, which dereferences npm's
    bin shims (R-0591); the guard rejects `ln` by form, so use `os.symlink`.
    If `npx` turns that symlink into a real directory, REMOVE the directory
    rather than unlinking it, and never touch the primary `node_modules`.
 7. The reviewer's OWN readings, each produced by RUNNING the tool rather than
    recalled (R-0625). At `b6a1c4d1` in `apps/ui`: `npx vitest run` exits 0 at
    7 files and 119 tests, `npm run --silent typecheck` exits 0 silently,
    `npm run --silent lint` EXITS 1 at `56 problems (54 errors, 2 warnings)`.
    From the root at `b6a1c4d1` the state readers plus canary exit 0 at 465
    and `tests/ui_contracts/` at 397, both passed-plus-skipped — that split
    moves run to run, so a bare passed count is never a gate. In a disposable
    worktree at `b6a1c4d1` carrying HOSTTESTS as the only added file, the
    reviewer measured `npx tsc --noEmit` exit 0, `npx vitest run` exit 0 at 8
    files and 131 tests, that file alone at 12, lint EXIT 1 at `57 problems
    (55 errors, 2 warnings)` — one more than this base because the round adds
    one file eslint cannot parse, which is R-0622 and NOT a gate (R-0364) —
    and all three of G9's controls red, each with exactly one failure.
 8. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R24 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2 and C3. Per constraint 5 the post-C4 readings
     belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r24.md`
     as received, of `.agent/authored/f008-r24.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r24.md` with `git show`, by their marker lines,
     take the COUNT from that listing, and report each slice's
     newline-INCLUDED sha256, bytes and lines and that none carries trailing
     whitespace. Expected: PLANF008R24 063f969b at 38 lines, LEDGER24
     9243828b, HOSTTESTS 5281e235 at 194 lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R24. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER24 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating
     newline normalised first, has as its LAST unit LEDGER24's single
     paragraph. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another and report that BOTH readings reject it and both accept the
     unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 200 at BOTH — no id is minted — `^- R-0629 — ` 0 at
     both, `^- R-0628 — ` 1 at both, `^Done: R-\d+ — ` 6 at both, `^Landed: `
     0 at both, `^Gate: R\d+ — ` 23 then 24 over that many DISTINCT keys.
     HEADER SWEEP at C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below
     the first, how many do not, the text of every non-match, and that the R24
     pair occurs EXACTLY ONCE.
 G7  The new file. Report that `git ls-tree b6a1c4d1 --
     apps/ui/src/api/brainStreamHost.test.ts` is EMPTY — it did not exist at
     the base — and that its blob at C3 is BYTE-EQUAL to HOSTTESTS, with both
     sha256 values. Report `git show --numstat` for it at C3: 194/0,
     insertions only and ZERO deletions, the file being new. Report also that
     `git diff --name-only b6a1c4d1..C3 -- apps/ui/src/api/brainStreamHost.ts`
     is EMPTY: the module under test was not touched (constraint 3).
 G8  The suites are green in the PRIMARY checkout, run SERIALLY. Report each
     exit code and its counts. In `apps/ui` AT C3: `npx vitest run` exits 0 at
     8 files and 131 tests — the 119 of constraint 7 plus HOSTTESTS' twelve
     `it`s, and the arithmetic is the point — `npx vitest run
     src/api/brainStreamHost.test.ts` alone reads 12, and
     `npm run --silent typecheck` exits 0 with NO output. From the repository
     root AT C3:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. Report `npm run --silent lint` at C3 too: EXIT 1 at
     `57 problems (55 errors, 2 warnings)`, constraint 7's measured value. If
     any of these fails, report the real values and STOP.
 G9  RED CONTROLS — the colour, never a count — in ONE disposable worktree
     created at C3 under the gitignored `.remedy-wt/`, the primary checkout
     NEVER touched and `node_modules` reached by constraint 6's symlink. Each
     control deletes ONE whole line of `src/api/brainStreamHost.ts` in THAT
     worktree — the module, never the test — and each is restored byte-exactly
     and verified by sha256 before the next runs. Report for each that the
     deleted bytes occur EXACTLY ONCE before the deletion, the exit code, and
     the failing test NAMES from
     `npx vitest run src/api/brainStreamHost.test.ts`. Each EXITS 1 with
     EXACTLY ONE failure and eleven passing, as the reviewer measured at
     `b6a1c4d1`:
     (a) `    if (typeof seq !== "number") return;` — four leading spaces, in
         `receive` — names `an open stream > drops a malformed frame instead
         of dispatching a broken one`.
     (b) `      drop();` — six leading spaces, the FIRST statement of
         `connect`, occurring once at that indent — names `reconnecting >
         closes the previous socket before opening the next`.
     (c) `    held = frame.seq;` — four leading spaces, in `tell` — names `the
         polling fallback > asks from the position the stream reached and
         surfaces each frame in order`.
     After all three, report that the restored module's sha256 equals its
     `b6a1c4d1` blob and that the same command EXITS 0 at 12 passed. REMOVE
     the worktree before writing C4.
 G10 The range. Report `git diff --name-only b6a1c4d1..C3` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — five paths, none on
     either side alone; the full `b6a1c4d1..C4` reading belongs to the ROUND
     REPORT (constraint 5). Report that every commit in the range has exactly
     ONE parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (§3 item 28).
 G11 Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, the
     test file at C3 and `.agent/handoff.md` at C4 — each is 0. Then count
     THIS round's own reflog entries by the OPERATION before the first `:` in
     `%gs`: all five pre-C4 entries are `commit`; report `amend`, `rebase` and
     `cherry` at 0, and assert no total.
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2, C3 and C4 — "exactly one row"
     scoping to that TABLE, not the whole file. Measure its line count with
     `wc -l` BEFORE committing it; six commits make the cap 100 lines, and an
     overage carries a DECISION D15 stated-cause line naming the real count and
     the mandated content that caused it. One line per gate here; the raw
     transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~94 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R24
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the transcript byte-equals the ledger's
envelope sequence, the heartbeat holds cadence, and the fallback engages on a
disabled EventSource and recovers to live.

## Current Step
R24 pins the stream host R23 landed: twelve tests over an injected source, an
injected snapshot read, an injected tail read and an injected scheduler, plus
three red controls — the malformed-frame guard, the close-before-reconnect and
the polling cursor. Only with this round is the adapter proved rather than
merely compiled. The round also records the R23 verdict.

## Next Steps
1. R25 adds the thin `useBrainStream` hook and the visible delayed badge,
   gated by typecheck and a `tests/ui_contracts/` source contract, the style
   this repository uses for every React component (R-0628).
2. Then the integration gate before closure.

## Risks
- The adapter OWNS a socket: `close` sits on the object its factory returns
  rather than on `BrainStreamHost`, so R25's hook must call it on unmount or
  a remounting cockpit leaks one EventSource per mount.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
<<<END PLANF008R24

<<<SLICE LEDGER24
Gate: R24 — the R23 entry. R23 PASSED. It landed `apps/ui/src/api/brainStreamHost.ts` — the real host behind the `BrainStreamHost` seam — and recorded the R22 verdict, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS by the primary comparison, the scratch original being alive: `.remedy-wt/f008-r23.md`, `.agent/authored/f008-r23.md` at `467b32b9` and `.agent/last_block.md` at `0b2f5cf7` are all sha256 3696b3b558ae5118a9d73589f025fd24af99047dc2b65e9067578efa19c9bc24 over 21363 bytes and 344 lines, equal to the digest the reviewer emitted in the delegation. THREE SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R23 377da548 at 2355 bytes and 42 lines, LEDGER23 46ec4d5d at 2892 bytes, HOSTSRC 664ce74e at 4990 bytes and 126 lines — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `46028e49`, byte-equal to its slice at 42 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `7696ed84` is a byte-exact prefix of the `46028e49` blob plus a 2893-byte remainder equal to a newline plus LEDGER23, agreed by an INDEPENDENT blank-line split of the whole file into 233 units whose LAST unit is LEDGER23's single paragraph, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS HELD WHERE THEY SHOULD — findings 200 at both revisions because no id was minted, `- R-0628` 1 at both and still OPEN, `- R-0629` 0 at both, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 22 to 23 over that many DISTINCT keys, twenty-two of the twenty-three headers matching the `Gate: R<n> — the R<n-1> entry.` shape with the F255 entry the single non-match, and the R23 pair occurring exactly once. THE NEW FILE IS PROVED BY CONSTRUCTION: `git ls-tree 476bfdfb` is EMPTY for it, its C3 blob is BYTE-EQUAL to HOSTSRC at 664ce74e, its numstat is 126 insertions and ZERO deletions, and `git ls-tree 96d316a6` is EMPTY for the test path, so the round created no test file. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npm run --silent typecheck` exits 0 with no output — the gate this round rested on — `npx vitest run` exits 0 at 7 files and 119 tests UNCHANGED because nothing imports the module yet, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 393 passed plus 4 skipped. LINT IS RED AND DECLARED at 56 problems, 54 errors and 2 warnings — one above the base because the round adds one file eslint cannot parse, exactly the value the block predicted, which is R-0622 and not a gate. SIX single-parent commits, insertions 344, 292, 25, 2, 126 and 37, every one under 500 and every cell equal to the handback's `+/-` column; zero marker lines in all four targets; five reflog operations all `commit` with amend, rebase and cherry at 0; a 67-line handback within the 100 that six commits allow, its item-status table naming C0a through C4 exactly once each; the tree clean and the primary checkout the only worktree. WHAT THE ROUND DID NOT CLAIM IS THE POINT OF IT: the module COMPILES and is not yet exercised, the block said so in three places, the handback repeated it, and the twelve tests and three red controls that make it proved are this round's work.
<<<END LEDGER24

<<<SLICE HOSTTESTS
import { describe, it, expect } from "vitest";
import { createBrainStreamHost } from "./brainStreamHost";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamEvent } from "./brainStreamDriver";

/** A hand-driven EventSource: its listeners fire when the TEST says so, never
 *  when a socket does, which is what lets this suite run with no DOM. */
class FakeSource implements BrainStreamSource {
  listeners = new Map<string, ((event: BrainStreamMessage) => void)[]>();
  closes = 0;

  addEventListener(type: string, listener: (event: BrainStreamMessage) => void): void {
    const bucket = this.listeners.get(type) ?? [];
    bucket.push(listener);
    this.listeners.set(type, bucket);
  }

  close(): void { this.closes += 1; }

  emit(type: string, event: BrainStreamMessage = {}): void {
    for (const listener of this.listeners.get(type) ?? []) listener(event);
  }
}

interface Harness {
  events: BrainStreamEvent[];
  sources: FakeSource[];
  opens: (string | null)[];
  tails: (number | null)[];
  waits: number[];
  host: ReturnType<typeof createBrainStreamHost>;
}

/** `absent` gives an environment with no EventSource at all. */
function harness(options: { absent?: boolean; snapshot?: number | null; tail?: BrainStreamFrame[] } = {}): Harness {
  const events: BrainStreamEvent[] = [];
  const sources: FakeSource[] = [];
  const opens: (string | null)[] = [];
  const tails: (number | null)[] = [];
  const waits: number[] = [];
  const host = createBrainStreamHost((event) => { events.push(event); }, {
    openSource(lastEventId: string | null): BrainStreamSource | null {
      opens.push(lastEventId);
      if (options.absent === true) return null;
      const source = new FakeSource();
      sources.push(source);
      return source;
    },
    readSnapshotSeq(): Promise<number | null> {
      return options.snapshot === undefined
        ? Promise.reject(new Error("no snapshot"))
        : Promise.resolve(options.snapshot);
    },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      tails.push(afterSeq);
      return options.tail === undefined
        ? Promise.reject(new Error("no tail"))
        : Promise.resolve(options.tail);
    },
    schedule(ms: number, resume: () => void): () => void {
      waits.push(ms);
      resume();
      return () => { events.push({ kind: "timer" }); };
    },
  });
  return { events, sources, opens, tails, waits, host };
}

/** Let the adapter's own `then` callbacks run before the assertions do. */
async function settle(): Promise<void> {
  await Promise.resolve();
  await Promise.resolve();
}

function payload(seq: number): string {
  return JSON.stringify({ seq, event: "task_started", timestamp: "", outcome: "" });
}

describe("an open stream", () => {
  it("carries the resume position to the source and reports the open", () => {
    const h = harness();
    h.host.connect("7");
    expect(h.opens).toEqual(["7"]);
    h.sources[0].emit("open");
    expect(h.events).toEqual([{ kind: "opened" }]);
  });
  it("surfaces a frame with the position the payload carries", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("message", { data: payload(4) });
    expect(h.events).toEqual([
      { kind: "frame", frame: { seq: 4, event: JSON.parse(payload(4)) } },
    ]);
  });
  it("drops a malformed frame instead of dispatching a broken one", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("message", { data: "{not json" });
    h.sources[0].emit("message", { data: JSON.stringify({ event: "no seq" }) });
    h.sources[0].emit("message", {});
    expect(h.events).toEqual([]);
  });
  it("reports a closed transport and lets its socket go", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("error");
    expect(h.events).toEqual([{ kind: "closed" }]);
    expect(h.sources[0].closes).toBe(1);
  });
});

describe("an environment without EventSource", () => {
  it("reports unsupported rather than pretending to connect", () => {
    const h = harness({ absent: true });
    h.host.connect(null);
    expect(h.events).toEqual([{ kind: "unsupported" }]);
  });
});

describe("reconnecting", () => {
  it("closes the previous socket before opening the next", () => {
    const h = harness();
    h.host.connect(null);
    h.host.connect("3");
    expect(h.sources[0].closes).toBe(1);
    expect(h.sources[1].closes).toBe(0);
    expect(h.opens).toEqual([null, "3"]);
  });
});

describe("the snapshot read", () => {
  it("carries the repaired position and moves the polling cursor with it", async () => {
    const h = harness({ snapshot: 12, tail: [] });
    h.host.requestSnapshot();
    await settle();
    expect(h.events).toEqual([{ kind: "snapshot", seq: 12 }]);
    h.host.pollOnce();
    await settle();
    expect(h.tails).toEqual([12]);
  });
  it("reports a closed transport when the read fails or holds no position", async () => {
    const failed = harness();
    failed.host.requestSnapshot();
    const empty = harness({ snapshot: null });
    empty.host.requestSnapshot();
    await settle();
    expect(failed.events).toEqual([{ kind: "closed" }]);
    expect(empty.events).toEqual([{ kind: "closed" }]);
  });
});

describe("the polling fallback", () => {
  it("asks from the position the stream reached and surfaces each frame in order", async () => {
    const h = harness({ tail: [{ seq: 6, event: null }, { seq: 7, event: null }] });
    h.host.connect(null);
    h.sources[0].emit("message", { data: payload(5) });
    h.host.pollOnce();
    await settle();
    expect(h.tails).toEqual([5]);
    expect(h.events.slice(1)).toEqual([
      { kind: "frame", frame: { seq: 6, event: null } },
      { kind: "frame", frame: { seq: 7, event: null } },
    ]);
  });
  it("reports a closed transport when the tail read fails", async () => {
    const h = harness();
    h.host.pollOnce();
    await settle();
    expect(h.events).toEqual([{ kind: "closed" }]);
    expect(h.tails).toEqual([null]);
  });
});

describe("closing the host", () => {
  it("closes the open socket once, however often it is asked", () => {
    const h = harness();
    h.host.connect(null);
    h.host.close();
    h.host.close();
    expect(h.sources[0].closes).toBe(1);
  });
});

describe("scheduling", () => {
  it("runs through the injected scheduler rather than a timer of its own", () => {
    const h = harness();
    const cancel = h.host.schedule(250, () => { h.events.push({ kind: "opened" }); });
    expect(h.waits).toEqual([250]);
    expect(h.events).toEqual([{ kind: "opened" }]);
    cancel();
    expect(h.events).toEqual([{ kind: "opened" }, { kind: "timer" }]);
  });
});
<<<END HOSTTESTS
