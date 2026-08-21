── STEP T003/8 — F008 SSE event stream — ROUND 31 ────────────────────────────
Round base — the SHA every range gate in this block measures from: 82e30bb5
 (R30's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R30 verdict — PASS, every gate re-run by the reviewer out of the
 committed blobs — and build the real `BrainStreamHostDeps` factory over the
 endpoint T001 and T002 shipped: the cursor arithmetic, the two request paths
 and the envelope readers, with their own vitest tests. Binding that
 environment to the browser's globals and wiring `useBrainStream` into
 `RemedyApp` are deliberately NOT in this round; they land in R32.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r31.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R31, applied whole
 C2   `.agent/live_review.md` <- LEDGER31, appended
 C3   `apps/ui/src/api/brainStreamDeps.ts` <- DEPS, a NEW file
 C4   `apps/ui/src/api/brainStreamDeps.test.ts` <- DEPSTEST, a NEW file
 C5   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r31.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamDeps.ts`,
 `apps/ui/src/api/brainStreamDeps.test.ts`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r31.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r31.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, and every
 count this block orders over a slice is taken over those newline-INCLUDED
 bytes.

Pair shape (§3 item 15):
 This block orders NO FROM/TO pair, so the containment test has no input and no
 APPEND or REWRITE label is derived. PLANF008R31 is a whole-file write, LEDGER31
 an append, and DEPS and DEPSTEST each CREATE a file: at emission
 `git ls-tree 82e30bb5 -- apps/ui/src/api/brainStreamDeps.ts
 apps/ui/src/api/brainStreamDeps.test.ts` printed NOTHING, and that reading is
 what G7 orders reproduced (item 24).

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23), and C3 precedes C4 so the
    module lands before the suite that imports it.
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED:
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened. The
    two new modules import only from `./brainStream`, `./brainStreamHost` and
    `vitest`, all three of which already resolve at the round base.
 4. NO FINDING ID IS MINTED: R-0630 stays free. The reviewer re-ran every gate
    R30 ordered and found no defect, so this round registers none. R-0368,
    R-0429, R-0553, R-0622, R-0628 and R-0629 stay OPEN and none is resolved
    here: write no `Done:` and no `Landed:` line for any of them.
 5. The post-C5 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G8's suites run in the PRIMARY
    checkout (R-0518). G9's red control is the ONLY destructive check and runs
    in a disposable worktree, never in the primary checkout (protocol G5).
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    reviewer's Phase 0 probe and nothing since has created one.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there; commit nothing
    from it. Never `cd` into a worktree and leave the shell there — a later
    gate then silently measures the wrong tree (R-0463).
 9. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553). Any handback
    sentence stating "every", "no", "all" or "none" over commits, files or
    rounds names the command that produced the number. State the particular
    you measured, or nothing.
 10. THE HANDBACK'S `## Next` SECTION states, in this order: that the next
    session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
    its SECOND the Open PR Gate (Phase 1 rule 2); that R31 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0622, R-0628 and
    R-0629 are OPEN; and that R32's work is binding the injected environment to
    the browser's EventSource, fetch and timer, wiring `useBrainStream` into
    `RemedyApp` over `createBrainStreamHostDeps`, and passing its status down to
    the badge R29 built.

The reviewer's OWN readings, each produced by RUNNING the tool at the round base
`82e30bb5`, serially, not recalled (R-0625): the five-target state reader plus
canary EXITS 0 at 465 passed and 0 skipped; `python3 -m pytest
tests/ui_contracts/ -q -rf` EXITS 0 at 409 passed plus 4 skipped = 413; and in
`apps/ui`, `npm run --silent typecheck` EXITS 0 with NO output while `npx vitest
run` EXITS 0 at 9 files and 137 tests. The last two were taken in a disposable
worktree at `82e30bb5` with `apps/ui/node_modules` SYMLINKED, because a fresh
worktree has none (R-0518). `npm run lint` is RED at base, which is R-0622 and
NOT a gate (R-0364).

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2, C3 and C4. Per constraint 5 the post-C5
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r31.md`
     as received, of `.agent/authored/f008-r31.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r31.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, and that none carries trailing whitespace on any line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R31. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The append at C2, against the round base, two ways that must agree.
     (a) the base blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER31 — report its sha256 prefix, bytes and
     lines; (b) an INDEPENDENT blank-line split of the WHOLE C2 file, its
     terminating newline normalised first, has LEDGER31's paragraph as its LAST
     unit. NEGATIVE CONTROL: flip one PRINTABLE ASCII byte of the remainder to
     another printable one; BOTH readings must reject it and both accept the
     unflipped. Read the base bytes with `git show 82e30bb5:.agent/live_review.md`
     into scratch or memory, never over the tracked file (item 29).
 G6  The sets in `.agent/live_review.md`, line-anchored, each reported at the
     round base AND at C2: `^- R-\d+ — ` reads 201 at both — this round mints
     no id — `^- R-0630 — ` 0 at both, `^- R-0429 — `, `^- R-0553 — `,
     `^- R-0629 — `, `^- R-0628 — ` and `^- R-0368 — ` 1 each at both,
     `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, and `^Gate: R\d+ — `
     30 at the base and 31 at C2, over that many DISTINCT keys. HEADER SWEEP at
     C2 (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of each non-match to its first period,
     and that the R31 pair occurs EXACTLY ONCE.
 G7  The two new modules. Report that `git ls-tree 82e30bb5 -- <path>` prints
     NOTHING for each, so both are CREATED and neither is modified; and that
     `apps/ui/src/api/brainStreamDeps.ts` at C3 is BYTE-EQUAL to DEPS and
     `apps/ui/src/api/brainStreamDeps.test.ts` at C4 is BYTE-EQUAL to DEPSTEST,
     each by sha256 over the committed blob against the slice extracted from
     the committed C0a blob.
 G8  The runs, in the PRIMARY checkout, SERIALLY, never two test processes
     alive at once, AT C4 — the commit at which both new modules are final.
     In `apps/ui`: `npm run --silent typecheck` EXITS 0 with NO output, and
     `npx vitest run` EXITS 0 at 10 files and 149 tests, where the base reading
     stated above is 9 and 137. From the repository root:
     `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 413, and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     EXITS 0 at 465. Report each pytest suite's passed and skipped numbers
     SEPARATELY as well as their sum, that split moving run to run so a bare
     passed count is never a gate. If any of the four fails, report the real
     values and STOP.
 G9  The red control, at C4, in a DISPOSABLE worktree with
     `apps/ui/node_modules` SYMLINKED into it — never copied, and never the
     primary checkout. In that worktree's `apps/ui/src/api/brainStreamDeps.ts`
     the newline-terminated byte string, two leading spaces included,
     `  return heldSeq === null ? 0 : heldSeq + 1;` occurs EXACTLY ONCE; report
     that count FIRST. Replace that one occurrence with
     `  return heldSeq === null ? 0 : heldSeq;` and report that, run from that
     worktree's `apps/ui`, `npx vitest run src/api/brainStreamDeps.test.ts`
     EXITS 1 failing exactly these three, and no others:
     `the cursor arithmetic > asks for the position after the one it holds`,
     `the host deps over the real endpoints > opens the stream one position after the frame it holds`,
     `the host deps over the real endpoints > polls the tail strictly after the position it holds`.
     Then restore the file, report it byte-identical by sha256, and report the
     same command EXITING 0 at 12 passed. Remove the worktree and report
     `git worktree list` naming only the primary checkout.
 G10 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 82e30bb5..C4` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly, with none on either side
     alone; the full reading to C5 belongs to the ROUND REPORT (constraint 5).
     Walk `git rev-list --reverse 82e30bb5..C4` and report ONE reading per
     commit: that it has exactly ONE parent, and BOTH numstat cells per path
     from `git show --numstat`, cross-checked against `git diff --numstat`,
     every insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (item 28). C5's own numbers cannot exist
     while C5 is being written, so they belong to the round report (item 14).
 G11 Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in the plan at C1, the ledger at C2, each new module at C3 and
     C4, and the handback at C5 — each is 0. `.agent/last_block.md` is NOT in
     that list and is not expected to be 0, being the block's own mirror. Then
     count THIS round's own reflog entries by the OPERATION before the first
     `:` in `%gs`: every pre-C5 entry reads `commit`; report how many you
     classified and `amend`, `rebase` and `cherry` at 0. Assert no total over
     the whole reflog (R-0601).
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 10
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2, C3, C4 and C5 — "exactly one row" scoping to
     that TABLE. Measure its line count with `wc -l` BEFORE committing it; this
     round's commit count is above five, so the cap is 100, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; raw transcripts
     go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~99 % (T001 ✅ · T002 ✅ · T003 Client ✅ + Badge ✅ + Deps-Factory ✅, RemedyApp-Wiring offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R31
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R31 records the R30 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — and builds the real `BrainStreamHostDeps` factory over the
endpoint T001 and T002 shipped: `createBrainStreamHostDeps`, the cursor
arithmetic that makes a resume replay nothing and skip nothing, and the readers
for the events-since envelope, each gated by its own vitest tests. The factory
takes its environment INJECTED, so no global is read yet.

## Next Steps
1. R32 binds that environment to the browser's EventSource, fetch and timer,
   wires `useBrainStream` into `RemedyApp` over the new factory and passes its
   status down to the badge R29 built — the round in which this feature's two
   halves meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The wiring round touches `RemedyApp.tsx`, the one file every cockpit surface
  renders through, so its blast radius is wider than any round since R4.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
<<<END PLANF008R31

<<<SLICE LEDGER31
Gate: R31 — the R30 entry. R30 PASSED. It recorded the R29 verdict and amended R-0429 with the F008 R29 instance, changed no code, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r30.md` as it survived on disk, `.agent/authored/f008-r30.md` at `53261d6e` and `.agent/last_block.md` at `238684d3` are all sha256 d1c83f446b5edbe8a2c6750c2dbdb686cf593174cb80e5d9db25e9a0ec17f575 over 22431 bytes and 237 lines, so the transport proof is disk-to-disk and no digest fallback was needed. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R30 a88def95 at 40 lines, and single-line slices for R0429FROM ca7076e7, R0429TO ae857017 and LEDGER30 73a58e93 — none carrying trailing whitespace on any line and each newline-terminated. THE PLAN LANDED FIRST at `350a8f98`, byte-equal to PLANF008R30 at 40 lines under the 50-line cap, with `## Goal` and `## Next Steps` once each line-anchored and `F008` matching. THE REWRITE at `2217a333` is proved twice over: R0429FROM 1 at the round base and 0 after, R0429TO 0 then 1 — the FROM-0x/TO-1x count a rewrite owes — and, independently, the base blob (a8b66ac0, 496399 bytes) with that ONE substitution applied is BYTE-EQUAL to the C2a blob (07437afe, 498486 bytes), with 240 blank-line paragraphs before and after, EXACTLY ONE differing, and that one the `- R-0429 — ` paragraph at index 68. THE APPEND at `efd44891` is a byte-exact prefix of the C2a blob plus a 5485-byte remainder equal to a newline plus LEDGER30, agreed by an INDEPENDENT split of the whole file into 241 units whose LAST is LEDGER30's paragraph, with a one-byte printable flip at remainder offset 1 REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD — 201 findings at both ledger commits with NO id minted and R-0630 still 0, `- R-0429`, `- R-0553`, `- R-0629`, `- R-0628` and `- R-0368` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 29 at C2a and 30 at C2b over that many DISTINCT keys, 29 of 30 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R30 pair occurring exactly once. THE CORRECTION IS ITSELF CORRECT, which is the one thing a finding about a wrong numeral must not get wrong: R0429TO reports R28's ledger holding 27 `Gate: R` entries over 27 distinct keys at `1cf2280b` and 28 over 28 at `fcea57b5`, and the reviewer re-measured both revisions and read exactly those four numbers. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: the five-target state readers plus canary EXIT 0 at 465 passed and 0 skipped, and `tests/ui_contracts/` EXITS 0 at 409 passed plus 4 skipped = 413. SIX single-parent commits over `860fc9c3`..`82e30bb5`, insertions 237, 134, 13, 1, 2 and 37 in commit order — every one under 500, 237 the maximum — and every numstat cell equal to the `## Commits` column for the five rows that table gives numbers for, the handback commit's own row naming itself instead, as R-0149 requires; zero marker lines in the plan at C1, the ledger at C2a and at C2b and the handback at C3; and a 70-line handback within the 100 six commits allow. NO FINDING IS REGISTERED AGAINST R30: the reviewer re-ran the block's gates and every value reproduced, so R-0630 stays free.
<<<END LEDGER31

<<<SLICE DEPS
// The real BrainStreamHostDeps: the SSE endpoint T001 built and the
// events-since transport T002 shares with it, turned into the four functions
// createBrainStreamHost asks for. Every piece of the world it needs arrives as
// an injected BrainStreamEnv rather than as a global, so all of it runs under
// the node-environment vitest with no DOM, no socket and no network. Remedy
// deliberately does not build that env from globalThis here: binding the real
// EventSource, fetch and timer belongs with the cockpit wiring that has them.
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamHostDeps, BrainStreamSource } from "./brainStreamHost";

/** The events-since envelope, as `_build_events_since_json` in ui_server.py
 *  writes it. Only the two fields this client reads are named: `cursor` is the
 *  ledger's LENGTH as a string, and `events` carries one `_safe_event_summary`
 *  per ledger position. */
interface EventsSincePayload {
  cursor?: unknown;
  events?: unknown;
}

/** Everything the factory needs from the world, so a test hands it three
 *  functions and the cockpit hands it three different ones. */
export interface BrainStreamEnv {
  /** null in an environment with no EventSource — that null is what
   *  `createBrainStreamHost` turns into the `unsupported` its polling fallback
   *  engages on. */
  makeSource: ((url: string) => BrainStreamSource) | null;
  /** GET the path and parse its JSON body; rejects on a non-2xx status. */
  fetchJson(path: string): Promise<unknown>;
  /** setTimeout in a browser, a hand-fired fake in a test. The returned
   *  function cancels the pending resume. */
  setTimer(ms: number, resume: () => void): () => void;
}

/** The cursor arithmetic, in the ONE place that builds requests. The client
 *  holds a seq; the endpoint's `cursor` names the position to start AT; so a
 *  holder of S asks for S+1. `resolve_sse_start` adds that same one for the
 *  Last-Event-ID header, which is what makes a resume replay nothing and skip
 *  nothing whichever way the client resumes. */
export function cursorAfter(heldSeq: number | null): number {
  return heldSeq === null ? 0 : heldSeq + 1;
}

/** Turn the envelope's `cursor` — the ledger's LENGTH — into the position of
 *  its last event, which is what a resuming client HOLDS. An empty ledger has
 *  no position, and that null is what tells the driver to keep waiting rather
 *  than resume from a frame that was never sent. */
export function snapshotSeqOf(payload: unknown): number | null {
  if (payload === null || typeof payload !== "object") return null;
  const cursor = (payload as EventsSincePayload).cursor;
  const length = typeof cursor === "string" ? Number(cursor) : cursor;
  if (typeof length !== "number" || !Number.isFinite(length) || length <= 0) return null;
  return length - 1;
}

/** The frames of one events-since response, in ledger order. An entry with no
 *  numeric `seq` is DROPPED rather than renumbered: a client that invented a
 *  position would resume from a frame the server never sent. */
export function framesOf(payload: unknown): BrainStreamFrame[] {
  if (payload === null || typeof payload !== "object") return [];
  const events = (payload as EventsSincePayload).events;
  if (!Array.isArray(events)) return [];
  const frames: BrainStreamFrame[] = [];
  for (const entry of events) {
    if (entry === null || typeof entry !== "object") continue;
    const seq = (entry as { seq?: unknown }).seq;
    if (typeof seq !== "number") continue;
    frames.push({ seq, event: entry });
  }
  return frames;
}

/** Build the four functions `createBrainStreamHost` needs, for ONE job.
 *
 *  The two paths are the two transports of one envelope:
 *  `/api/jobs/<id>/events/stream` streams it, and `/api/jobs/<id>/events-since`
 *  answers the snapshot and the polling tail out of the same ledger. */
export function createBrainStreamHostDeps(jobId: string, env: BrainStreamEnv): BrainStreamHostDeps {
  const job = encodeURIComponent(jobId);
  const since = (cursor: number): string => `/api/jobs/${job}/events-since?cursor=${cursor}`;
  return {
    openSource(lastEventId: string | null): BrainStreamSource | null {
      const make = env.makeSource;
      if (make === null) return null;
      const held = lastEventId === null ? Number.NaN : Number(lastEventId);
      const from = Number.isFinite(held) ? cursorAfter(held) : 0;
      return make(`/api/jobs/${job}/events/stream?cursor=${from}`);
    },
    readSnapshotSeq(): Promise<number | null> {
      return env.fetchJson(since(0)).then(snapshotSeqOf);
    },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      return env.fetchJson(since(cursorAfter(afterSeq))).then(framesOf);
    },
    schedule(ms: number, resume: () => void): () => void {
      return env.setTimer(ms, resume);
    },
  };
}
<<<END DEPS

<<<SLICE DEPSTEST
import { describe, it, expect } from "vitest";
import { createBrainStreamHostDeps, cursorAfter, framesOf, snapshotSeqOf } from "./brainStreamDeps";
import type { BrainStreamEnv } from "./brainStreamDeps";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";

/** A source that records nothing but its own construction: these tests are
 *  about the URL the factory builds, never about what a socket does with it. */
class FakeSource implements BrainStreamSource {
  addEventListener(_type: string, _listener: (event: BrainStreamMessage) => void): void {}
  close(): void {}
}

interface Recorder {
  urls: string[];
  paths: string[];
  timers: number[];
  env: BrainStreamEnv;
}

/** `absent` gives an environment with no EventSource; `payload` is what the
 *  one injected reader answers every request with. */
function recorder(options: { absent?: boolean; payload?: unknown } = {}): Recorder {
  const urls: string[] = [];
  const paths: string[] = [];
  const timers: number[] = [];
  return {
    urls,
    paths,
    timers,
    env: {
      makeSource: options.absent === true
        ? null
        : (url: string): BrainStreamSource => { urls.push(url); return new FakeSource(); },
      fetchJson(path: string): Promise<unknown> {
        paths.push(path);
        return Promise.resolve(options.payload);
      },
      setTimer(ms: number, _resume: () => void): () => void {
        timers.push(ms);
        return (): void => { timers.push(-ms); };
      },
    },
  };
}

describe("the cursor arithmetic", () => {
  it("asks for the position after the one it holds", () => {
    expect(cursorAfter(7)).toBe(8);
    expect(cursorAfter(0)).toBe(1);
  });

  it("asks from the start when it holds nothing", () => {
    expect(cursorAfter(null)).toBe(0);
  });
});

describe("reading the events-since envelope", () => {
  it("reads the last position out of the ledger length the server sends as a string", () => {
    expect(snapshotSeqOf({ cursor: "3" })).toBe(2);
  });

  it("has no position for an empty ledger, a missing cursor or a non-object", () => {
    expect(snapshotSeqOf({ cursor: "0" })).toBeNull();
    expect(snapshotSeqOf({})).toBeNull();
    expect(snapshotSeqOf(null)).toBeNull();
    expect(snapshotSeqOf({ cursor: "not a number" })).toBeNull();
  });

  it("carries the whole summary as the frame's event, keyed by the ledger's own seq", () => {
    const frames = framesOf({ events: [{ seq: 4, event: "test_run_completed" }] });
    expect(frames).toEqual([{ seq: 4, event: { seq: 4, event: "test_run_completed" } }]);
  });

  it("drops an entry with no numeric seq rather than renumbering it", () => {
    expect(framesOf({ events: [{ event: "no seq" }, { seq: 2 }] })).toEqual([{ seq: 2, event: { seq: 2 } }]);
    expect(framesOf({ events: "not an array" })).toEqual([]);
  });
});

describe("the host deps over the real endpoints", () => {
  it("opens the stream one position after the frame it holds", () => {
    const r = recorder();
    createBrainStreamHostDeps("job-1", r.env).openSource("7");
    expect(r.urls).toEqual(["/api/jobs/job-1/events/stream?cursor=8"]);
  });

  it("opens the stream from the start when it holds nothing, and escapes the job id", () => {
    const r = recorder();
    createBrainStreamHostDeps("a/b", r.env).openSource(null);
    expect(r.urls).toEqual(["/api/jobs/a%2Fb/events/stream?cursor=0"]);
  });

  it("reports no source at all where the environment has no EventSource", () => {
    const r = recorder({ absent: true });
    expect(createBrainStreamHostDeps("job-1", r.env).openSource(null)).toBeNull();
    expect(r.urls).toEqual([]);
  });

  it("reads the snapshot position from the whole ledger", async () => {
    const r = recorder({ payload: { cursor: "5" } });
    await expect(createBrainStreamHostDeps("job-1", r.env).readSnapshotSeq()).resolves.toBe(4);
    expect(r.paths).toEqual(["/api/jobs/job-1/events-since?cursor=0"]);
  });

  it("polls the tail strictly after the position it holds", async () => {
    const r = recorder({ payload: { events: [{ seq: 9 }] } });
    const deps = createBrainStreamHostDeps("job-1", r.env);
    await expect(deps.readTail(8)).resolves.toEqual([{ seq: 9, event: { seq: 9 } }]);
    await deps.readTail(null);
    expect(r.paths).toEqual([
      "/api/jobs/job-1/events-since?cursor=9",
      "/api/jobs/job-1/events-since?cursor=0",
    ]);
  });

  it("hands the backoff straight to the environment's timer", () => {
    const r = recorder();
    const cancel = createBrainStreamHostDeps("job-1", r.env).schedule(250, () => {});
    cancel();
    expect(r.timers).toEqual([250, -250]);
  });
});
<<<END DEPSTEST
