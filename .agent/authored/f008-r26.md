── STEP T003/6 — F008 SSE event stream — ROUND 26 ────────────────────────────
Goal:
 Land the composition seam. `brainStreamSession.ts` ties the real host to the
 runner store — the knot neither half can tie alone, since the host dispatches
 into a runner that does not exist when the host is built — and its suite
 proves start, live, frame delivery, both halves of close and the delayed
 fallback under the node-environment vitest. This round also records the R25
 PASS. The React hook over this seam is R27's work and lands nothing here.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r26.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R26, applied whole
 C2   `.agent/live_review.md` <- LEDGER26, appended
 C3   `apps/ui/src/api/brainStreamSession.ts` <- SESSION and
      `apps/ui/src/api/brainStreamSession.test.ts` <- SESSIONTESTS, both NEW
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r26.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamSession.ts`,
 `apps/ui/src/api/brainStreamSession.test.ts`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r26.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r26.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R26, LEDGER26, SESSION and SESSIONTESTS,
 each delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of a slice. Every slice is
 newline-terminated with no trailing whitespace on any line. There is NO
 FROM/TO pair here: two slices create a file that does not exist, one replaces
 a file whole and one is appended, so the obligations are byte equality and an
 ordered append, and no containment reading is claimed.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. NO EXISTING SOURCE FILE IS
    EDITED and NO DEPENDENCY IS ADDED: both code paths are NEW files, and
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened.
 4. NO FINDING ID IS MINTED and none is resolved: R-0630 stays free, R-0628,
    R-0629 and R-0622 stay OPEN, and no `Done:` and no `Landed:` line is
    written for any of them. R-0628 names the HOOK, which R27 lands, so this
    round cannot resolve it and does not try.
 5. The post-C4 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once. G8's four runs happen SERIALLY in
    the PRIMARY checkout (R-0518). G9's mutations are destructive and run ONLY
    in a disposable worktree under `.remedy-wt/` (protocol G5), removed and
    pruned before the handback. That worktree needs `apps/ui/node_modules`:
    SYMLINK it from the primary checkout with `os.symlink`, never a copy —
    `shutil.copytree` defaults to `symlinks=False` and dereferences npm's bin
    shims, which caused seven false failures at F085 R23 (R-0591). The
    reviewer took G9's own readings that way.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R26 gate.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there, as R25 did;
    commit nothing from that directory.

The reviewer's OWN readings, each produced by RUNNING the tool and not recalled
(R-0625). At `6e39f19d` in the primary checkout the state readers plus canary
exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 397 — that split
moves run to run, so a bare passed count is never a gate. In a worktree at
`369fd39e` with node_modules symlinked, vitest exits 0 at 8 files and 131 tests
and typecheck exits 0 silently; with all four slices applied there, every value
G8 and G9 order was measured at the value stated, each control seen red,
restored and re-measured byte-identical. `npm run lint` in `apps/ui` is RED at
base, which is R-0622 and NOT a gate (R-0364).

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2 and C3. Per constraint 5 the post-C4 readings
     belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r26.md`
     as received, of `.agent/authored/f008-r26.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r26.md` with `git show`, by their marker lines, take
     the COUNT from that listing, and report each slice's newline-INCLUDED
     sha256, bytes and lines and that none carries trailing whitespace.
     Expected: PLANF008R26 4ce0503e at 41 lines, LEDGER26
     8a9d2ef6 at 1, SESSION 1935909b at 38, SESSIONTESTS 5a2d6cef at 111.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R26. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER26 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
     normalised first, has as its LAST unit LEDGER26's paragraph. NEGATIVE
     CONTROL: flip one ASCII byte of the remainder and report that BOTH
     readings reject it and both accept the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 201 at BOTH — this round mints no id — `^- R-0630 — `
     0 at both, `^- R-0629 — ` 1 at both, `^- R-0628 — ` 1 at both,
     `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 25
     then 26 over that many DISTINCT keys. HEADER SWEEP at C2: report how many
     `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with the second
     numeral one below the first, how many do not, the text of every non-match
     to its first period, and that the R26 pair occurs EXACTLY ONCE.
 G7  The two code files. For EACH: `git ls-tree 6e39f19d` is EMPTY for it, so
     the round ADDS it and edits nothing; its blob at C3 is BYTE-EQUAL to its
     slice; and its `git show --numstat` cell reads that slice's own line count
     with ZERO deletions.
 G8  The green runs, in the PRIMARY checkout, SERIALLY, AT C3 — the commit at
     which both code files are final. Report each exit code and its counts:
     `npm run --silent typecheck` in `apps/ui` exits 0 with NO output;
     `npx vitest run` in `apps/ui` exits 0 at 9 files and 137 tests;
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped; and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped. If any fails, report the values and STOP.
 G9  Two red controls, in a disposable worktree at C3 per constraint 6, ONE
     mutation at a time, each restored afterwards and proved byte-identical to
     its pre-mutation sha256. Both mutate
     `apps/ui/src/api/brainStreamSession.ts`, where the reviewer counted each
     ordered byte string at exactly 1 occurrence (§3 item 25); report your own
     count before mutating, and report the failing test NAME, because the other
     control also goes red and only the name tells the two apart (R-0629).
     (a) DELETE the one line `      host.close();`: `npx vitest run` EXITS 1
         with EXACTLY ONE failure, named `closes the socket when the caller
         closes the session`, and 136 passing.
     (b) DELETE the one line `      runner.stop();`: `npx vitest run` EXITS 1
         with EXACTLY ONE failure, named `performs nothing more once it is
         closed`, and 136 passing.
 G10 The range. Report `git diff --name-only 6e39f19d..C3` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — six paths, none on
     either side alone; the full `6e39f19d`..C4 reading belongs to the ROUND
     REPORT (constraint 5). Report that every commit in the range has exactly
     ONE parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (§3 item 28).
 G11 Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or `<<<END `
     in each file this round writes outside `.agent/authored/` — the plan at
     C1, the ledger at C2, the two code files at C3 and the handback at C4 —
     each is 0. Then count THIS round's own reflog entries by the OPERATION
     before the first `:` in `%gs`: all five pre-C4 entries are `commit`; report
     `amend`, `rebase` and `cherry` at 0, and assert no total.
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2, C3 and C4 — "exactly one row"
     scoping to that TABLE. Its `## Next` states that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
     Open PR Gate (rule 2); that R26 is PENDING REVIEW; that the next free id
     is R-0630; that R-0628, R-0629 and R-0622 are OPEN; and that R27 adds
     `useBrainStream.ts` over this session plus its `tests/ui_contracts/`
     source contract. Measure its line count with `wc -l` BEFORE committing it;
     six commits make the cap 100, and an overage carries a DECISION D15
     stated-cause line naming the real count and the mandated content that
     caused it. One line per gate here; raw transcripts go in the ROUND REPORT
     (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~95 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host+Seam ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R26
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
R26 lands `brainStreamSession.ts`, the composition seam T003 has been building
toward: it ties the host to the runner store — a knot neither half can tie, the
host dispatching into a runner that does not exist when the host is built — and
gives the React hook one object to hold, whose `close` stops the runner AND the
socket. Six vitest tests pin start, live, frame delivery, both halves of close
and the delayed fallback.

## Next Steps
1. R27 adds `useBrainStream.ts` over this seam and its `tests/ui_contracts/`
   source contract — the style every React component here is gated by
   (R-0628) — with the hook closing the session on unmount, or a remounting
   cockpit leaks one EventSource per mount.
2. R28 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built.
3. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract will gate its source, and this seam carries the logic beneath.
<<<END PLANF008R26

<<<SLICE LEDGER26
Gate: R26 — the R25 entry. R25 PASSED. It recorded the R24 verdict, registered R-0629 and changed no code, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r25.md`, `.agent/authored/f008-r25.md` at `6bd98edd` and `.agent/last_block.md` at `b252f72f` are all sha256 aa5693287d3e823a12d1a0c7ea3e0454279d5b5bcd435ffc612cd2815fb9eeea over 17234 bytes and 192 lines, equal to the digest the reviewer emitted. TWO SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R25 0cc72159 at 2045 bytes and 39 lines, LEDGER25 2dd41f07 at 5758 bytes and 3 lines — neither carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `596c6f0b`, byte-equal at 39 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `0586d578` is a byte-exact prefix of the `596c6f0b` blob plus a 5759-byte remainder equal to a newline plus LEDGER25, agreed by an INDEPENDENT blank-line split of the whole file into 236 units whose LAST TWO, in order, are LEDGER25's two paragraphs, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS HELD — findings 200 to 201, `- R-0629` 0 to 1 as the only id minted, `- R-0630` 0 at both, `- R-0628` 1 at both and still OPEN, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 24 to 25 over that many DISTINCT keys, twenty-four of twenty-five headers matching the `Gate: R<n> — the R<n-1> entry.` shape with the F255 entry the single non-match, and the R25 pair occurring exactly once. THE FINDING R-0629 REGISTERS IS ITSELF TRUE, which a registration round is owed and rarely gets: `git grep -n` for the six-space `drop();` line in `apps/ui/src/api/brainStreamHost.ts` at `46ac9da4` returns exactly two hits, at lines 87 and 123, so the R24 block's "occurs EXACTLY ONCE" really was unmeetable and the worker's declared deviation really was the reviewer's error. FIVE single-parent commits, insertions 192, 107, 13 and 4 for the four commits a per-commit gate can reach, every one under 500 and EVERY CELL — insertion and deletion — equal to the `## Commits` column, which is the R-0592 defect of R24 not recurring; the handback commit's own 28 and 37 went to the round report, as §3 item 14 requires. Zero marker lines in all three targets; four reflog entries all `commit`, with amend, rebase and cherry at 0; a 58-line handback within the 60 five commits allow; the tree clean, the primary checkout the only worktree, and the branch pushed. THE SUITES ARE THE REVIEWER'S OWN, serial, in the primary checkout at the branch tip: the state readers including the canary EXIT 0 at 465 passed-plus-skipped and `tests/ui_contracts/` EXITS 0 at 393 passed plus 4 skipped, both equal to the values the block ordered. NO FINDING IS OPENED BY THIS ROUND.
<<<END LEDGER26

<<<SLICE SESSION
// The knot neither half can tie alone: the host dispatches INTO a runner that
// does not exist when the host is built, and the runner drives a host it must
// already hold. Tying it here rather than inside the React hook keeps the whole
// composition — start, subscribe, close — under the node-environment vitest,
// for the same reason the driver and the runner are not React either.
import { createBrainStreamHost } from "./brainStreamHost";
import type { BrainStreamHostDeps } from "./brainStreamHost";
import { createBrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamView } from "./brainStreamRunner";

/** Exactly what `useSyncExternalStore` needs, plus the lifetime a socket owner
 *  owes its caller. */
export interface BrainStreamSession {
  subscribe(listener: () => void): () => void;
  view(): BrainStreamView;
  start(): void;
  /** Stop the runner AND close the socket. Stopping alone silences the client
   *  while leaving its EventSource open, so a remounting cockpit would leak one
   *  connection per mount. */
  close(): void;
}

/** Compose the real adapter with the runner store. Building a session opens
 *  nothing: only `start` connects, so a session created during a render React
 *  then discards costs a closure and never a socket. */
export function createBrainStreamSession(deps: BrainStreamHostDeps): BrainStreamSession {
  const host = createBrainStreamHost((event) => { runner.dispatch(event); }, deps);
  const runner = createBrainStreamRunner(host);
  return {
    subscribe: runner.subscribe,
    view: runner.view,
    start: runner.start,
    close(): void {
      runner.stop();
      host.close();
    },
  };
}
<<<END SESSION

<<<SLICE SESSIONTESTS
import { describe, it, expect } from "vitest";
import { createBrainStreamSession } from "./brainStreamSession";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";
import type { BrainStreamFrame } from "./brainStream";

/** A hand-driven EventSource, as in brainStreamHost.test.ts: its listeners fire
 *  when the TEST says so, never when a socket does. */
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

/** The scheduler RECORDS instead of firing: the runner re-arms a poll from
 *  inside the resume it just ran, so a fake that resumed synchronously would
 *  recurse forever rather than test anything. */
function harness(options: { absent?: boolean; tail?: BrainStreamFrame[] } = {}) {
  const sources: FakeSource[] = [];
  const opens: (string | null)[] = [];
  const tails: (number | null)[] = [];
  const waits: { ms: number; resume: () => void }[] = [];
  const session = createBrainStreamSession({
    openSource(lastEventId: string | null): BrainStreamSource | null {
      opens.push(lastEventId);
      if (options.absent === true) return null;
      const source = new FakeSource();
      sources.push(source);
      return source;
    },
    readSnapshotSeq(): Promise<number | null> { return Promise.resolve(null); },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      tails.push(afterSeq);
      return Promise.resolve(options.tail ?? []);
    },
    schedule(ms: number, resume: () => void): () => void {
      waits.push({ ms, resume });
      return () => {};
    },
  });
  return { sources, opens, tails, waits, session };
}

function payload(seq: number): string {
  return JSON.stringify({ seq, event: "task_started" });
}

describe("a composed brain stream session", () => {
  it("connects on start and reports no status until the transport answers", () => {
    const h = harness();
    expect(h.opens).toEqual([]);
    h.session.start();
    expect(h.opens).toEqual([null]);
    expect(h.session.view().status).toBeNull();
  });

  it("shows live once the source opens", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("open");
    expect(h.session.view().status).toBe("live");
  });

  it("carries a frame's position into the view and wakes its subscribers", () => {
    const h = harness();
    let woken = 0;
    h.session.subscribe(() => { woken += 1; });
    h.session.start();
    h.sources[0].emit("message", { data: payload(4) });
    expect(h.session.view().lastSeq).toBe(4);
    expect(woken).toBe(1);
  });

  it("closes the socket when the caller closes the session", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("open");
    h.session.close();
    expect(h.sources[0].closes).toBe(1);
  });

  it("performs nothing more once it is closed", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("error");
    expect(h.waits).toHaveLength(1);
    h.session.close();
    h.waits[0].resume();
    expect(h.opens).toEqual([null]);
  });

  it("falls back to delayed polling where the environment has no EventSource", async () => {
    const h = harness({ absent: true });
    h.session.start();
    expect(h.session.view().status).toBe("delayed");
    expect(h.waits[0].ms).toBe(3000);
    h.waits[0].resume();
    await Promise.resolve();
    expect(h.tails).toEqual([null]);
  });
});
<<<END SESSIONTESTS
