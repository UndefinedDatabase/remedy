── STEP T003/5 — F008 SSE event stream — ROUND 23 ────────────────────────────
Goal:
 Land the REAL host behind `BrainStreamHost` — an injected EventSource, a
 snapshot read, a tail read and a scheduler — so the driver's effects reach a
 transport with no DOM anywhere. The module COMPILES this round and is NOT yet
 exercised: typecheck is its gate here and R24 brings its suite and its red
 controls. The round also records the R22 verdict.

Why the tests are not in this round:
 The adapter and its suite total 320 lines of slice, and a block is budgeted
 at 490 lines TOTAL (DECISION F085 D6) because C0a commits the block itself
 and AGENTS.md caps a commit at 500 insertions. The ruled counter-measure is
 to split by whole items rather than to shorten prose, so the suite and its
 three red controls become R24. No round may call this module proved until
 that lands; this one claims only that it typechecks.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r23.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R23, applied whole
 C2   `.agent/live_review.md` <- LEDGER23, appended
 C3   `apps/ui/src/api/brainStreamHost.ts` <- HOSTSRC, a NEW file, whole
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r23.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamHost.ts`,
 `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r23.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r23.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R23, LEDGER23 and HOSTSRC, each
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
    are not edited. No EXISTING source file is edited and NO test file is
    created: the suite for this module belongs to R24.
 4. No id is minted and no verdict beyond LEDGER23 is written: R-0629 stays
    free, R-0628 stays OPEN with no `Done:` and no `Landed:` line, R-0622
    stays OPEN and no TypeScript parser is added to make lint green.
 5. The post-C4 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G8's suites run in the PRIMARY
    checkout: a fresh worktree has no `apps/ui/node_modules` (R-0518). This
    round creates NO worktree and orders NO red control — nothing exercises
    the new module yet, so a mutation of it cannot turn any test red, and
    ordering a colour that cannot appear is the R-0252 defect.
 7. The reviewer's OWN readings, each produced by RUNNING the tool rather than
    recalled (R-0625). `git diff --name-only 37c93574..476bfdfb -- apps/ui` is
    EMPTY, so readings taken at `37c93574` describe `476bfdfb` too: in
    `apps/ui`, `npx vitest run` exits 0 at 7 files and 119 tests, typecheck
    exits 0 silently, `npm run --silent lint` EXITS 1 at `55 problems (53
    errors, 2 warnings)`. From the root the state readers plus canary exit 0
    at 465 and `tests/ui_contracts/` at 397, both passed-plus-skipped — that
    split moves run to run, so a bare passed count is never a gate. In a
    disposable worktree at `476bfdfb` carrying HOSTSRC as the only added file,
    the reviewer measured `npx tsc --noEmit` exit 0, `npx vitest run` exit 0
    at 7 files and 119 tests UNCHANGED — no test imports the module yet — and
    lint EXIT 1 at `56 problems (54 errors, 2 warnings)`, one more than the
    base because this round adds one file eslint cannot parse, which is
    R-0622 and NOT a gate (R-0364).
 8. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R23 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2 and C3. Per constraint 5 the post-C4 readings
     belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r23.md`
     as received, of `.agent/authored/f008-r23.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r23.md` with `git show`, by their marker lines,
     take the COUNT from that listing, and report each slice's
     newline-INCLUDED sha256, bytes and lines and that none carries trailing
     whitespace. Expected: PLANF008R23 377da548 at 42 lines, LEDGER23
     46ec4d5d, HOSTSRC 664ce74e at 126 lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R23. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER23 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating
     newline normalised first, has as its LAST unit LEDGER23's single
     paragraph. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another and report that BOTH readings reject it and both accept the
     unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 200 at BOTH — no id is minted — `^- R-0629 — ` 0 at
     both, `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, `^Gate: R\d+ — `
     22 then 23 over that many DISTINCT keys. HEADER SWEEP at C2: report how
     many `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with the
     second numeral one below the first, how many do not, the text of every
     non-match, and that the R23 pair occurs EXACTLY ONCE.
 G7  The new file. Report that `git ls-tree 476bfdfb --
     apps/ui/src/api/brainStreamHost.ts` is EMPTY — it did not exist at the
     base — and that its blob at C3 is BYTE-EQUAL to HOSTSRC, with both sha256
     values. Report `git show --numstat` for it at C3: 126/0, insertions
     only and ZERO deletions, the file being new. Report also that
     `git ls-tree C3 -- apps/ui/src/api/brainStreamHost.test.ts` is EMPTY:
     this round creates no test file (constraint 3).
 G8  The suites are green in the PRIMARY checkout, run SERIALLY. Report each
     exit code and its counts. In `apps/ui` AT C3: `npm run --silent typecheck`
     exits 0 with NO output — the gate this round rests on — and
     `npx vitest run` exits 0 at 7 files and 119 tests, UNCHANGED from
     constraint 7's base because no test imports the new module yet. From the
     repository root AT C3:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. Report `npm run --silent lint` at C3 too: EXIT 1 at
     `56 problems (54 errors, 2 warnings)`, constraint 7's measured value. If
     any of these fails, report the real values and STOP.
 G9  The range. Report `git diff --name-only 476bfdfb..C3` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — five paths, none on
     either side alone; the full `476bfdfb..C4` reading belongs to the ROUND
     REPORT (constraint 5). Report that every commit in the range has exactly
     ONE parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (§3 item 28).
 G10 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2, the adapter at C3
     and `.agent/handoff.md` at C4. Each is 0.
 G11 Reflog. Count THIS round's own entries by the OPERATION before the first
     `:` in `%gs`. All five pre-C4 entries are `commit`; report `amend`,
     `rebase` and `cherry` at 0, and assert no total.
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
 ~92 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store ✅, Host kompiliert, Suite+Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R23
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
R23 lands the REAL host behind `BrainStreamHost`: an injected EventSource, a
snapshot read, a tail read and a scheduler, so the driver's effects reach a
transport. Every dependency is injected, so no DOM is involved. The module
COMPILES at this round and is not yet exercised: `npm run typecheck` is its
only gate here, and R24 brings its suite and its red controls. The round also
records the R22 verdict.

## Next Steps
1. R24 pins the adapter with its own vitest suite and three red controls —
   the malformed-frame guard, the close-before-reconnect and the polling
   cursor — and only then is the module proved rather than merely compiled.
2. R25 adds the thin `useBrainStream` hook and the visible delayed badge,
   gated by typecheck and a `tests/ui_contracts/` source contract, the style
   this repository uses for every React component (R-0628).
3. Then the integration gate before closure.

## Risks
- Untested code lands at R23 by design, one round ahead of its suite. The
  ordering is deliberate — AGENTS.md forbids one commit carrying a change and
  the tests that pin it — but until R24 the adapter's only evidence is that
  it typechecks, and no round may claim more for it than that.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622.
- The adapter OWNS a socket: `close` sits on the object its factory returns
  rather than on `BrainStreamHost`, and R25's hook must call it on unmount.
<<<END PLANF008R23

<<<SLICE LEDGER23
Gate: R23 — the R22 entry. R22 PASSED. It was a record round — the R21 verdict, the registration of R-0628 and the T003 re-plan — and it changed no code, so its gates are about bytes and sets, all of them RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS with the scratch original alive this time, so the primary cmp rather than the §4.9 digest fallback: `.remedy-wt/f008-r22.md`, `.agent/authored/f008-r22.md` at `22c0a5dd` and `.agent/last_block.md` at `ffaa5c9d` are all sha256 d2db104d3bcf7203e5f16e22246b63c2be4dd263c8702dea8b1b78dbceea72cf over 18389 bytes and 197 lines, and that digest equals the one the reviewer emitted in the delegation. TWO SLICES by the reviewer's own ordered extraction out of the committed C0a blob, PLANF008R22 c7f6e97d at 2305 bytes and 43 lines and LEDGER22 b8f3fa92 at 6371 bytes, neither carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `88cfcf4d`, byte-equal to its slice at 43 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `e2dad913` is a byte-exact prefix of the `88cfcf4d` blob plus a 6372-byte remainder equal to a newline plus LEDGER22, agreed by an INDEPENDENT blank-line split of the whole file into 232 units whose LAST TWO are LEDGER22's paragraphs in order, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS MOVED AS ORDERED — findings 199 to 200 for the single minted id, `- R-0628` 0 to 1, `- R-0629` 0 at both, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 21 to 22 over that many DISTINCT keys; twenty-one of the twenty-two headers match the `Gate: R<n> — the R<n-1> entry.` shape, the single non-match is the F255 entry, and the R22 pair occurs exactly once. THE SUITES ARE THE REVIEWER'S OWN, serial, in the primary checkout: the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 393 passed plus 4 skipped. FIVE single-parent commits, insertions 197, 127, 20, 4 and 30, every one under 500 and every cell — insertion AND deletion — equal to the handback's `+/-` column, including the 127/354 mirror commit where a full-file rewrite's line counts and its numstat columns diverge (§3 item 28); zero marker lines in all three targets; four reflog operations all `commit` with amend, rebase and cherry at 0; a 60-line handback exactly at the cap five commits allow, its item-status table naming C0a through C3 exactly once each; the tree clean and the primary checkout the only worktree. THE ROUND DECLARED ITS OWN GATE-SCRIPT CORRECTION rather than hiding it: G10's first reflog parser matched zero entries and would have returned a vacuous green, and the worker rewrote it and re-ran — which is the R-0438 class caught by the party the checklist relies on least.
<<<END LEDGER23

<<<SLICE HOSTSRC
// The real environment behind BrainStreamHost: an EventSource for the stream,
// two api reads for the snapshot and the polling tail, and a scheduler for the
// backoff. Every one of them is INJECTED, so this adapter — the last piece
// between the driver and a browser — runs under the node-environment vitest
// with no DOM, no socket and no network.
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamEvent } from "./brainStreamDriver";
import type { BrainStreamHost } from "./brainStreamRunner";

/** What a source hands a listener. Only `data` is read: the ledger position
 *  travels INSIDE the payload (`_safe_event_summary` in ui_server.py writes
 *  `seq` into it), so this client never depends on `lastEventId` surviving a
 *  proxy. */
export interface BrainStreamMessage {
  data?: string;
}

/** The only part of EventSource this client uses. Structural on purpose: the
 *  browser's EventSource satisfies it as-is, and a test fake is a dozen lines
 *  with no DOM behind them. */
export interface BrainStreamSource {
  addEventListener(type: string, listener: (event: BrainStreamMessage) => void): void;
  close(): void;
}

/** Everything the adapter needs from the world, named so a test can hand it
 *  four functions and a browser can hand it four different ones. */
export interface BrainStreamHostDeps {
  /** Open a stream at the resume position, or return null where this
   *  environment has no EventSource — that null IS the `unsupported` the
   *  polling fallback engages on. */
  openSource(lastEventId: string | null): BrainStreamSource | null;
  /** The current snapshot's ledger position, or null when it has none yet. */
  readSnapshotSeq(): Promise<number | null>;
  /** The frames STRICTLY AFTER the held position; null asks from the start.
   *  The caller passes what the client HOLDS, never the next seq it wants —
   *  the cursor arithmetic belongs to whoever builds the request. */
  readTail(afterSeq: number | null): Promise<BrainStreamFrame[]>;
  /** setTimeout in a browser, a hand-fired fake in a test. */
  schedule(ms: number, resume: () => void): () => void;
}

/** The adapter OWNS its socket, so `close` sits on the returned object rather
 *  than on BrainStreamHost: the runner never opens a stream and must not be
 *  taught to close one. A React hook closes it when the component unmounts. */
export function createBrainStreamHost(
  dispatch: (event: BrainStreamEvent) => void,
  deps: BrainStreamHostDeps,
): BrainStreamHost & { close(): void } {
  let source: BrainStreamSource | null = null;
  let held: number | null = null;

  /** Every frame the client is told about moves the polling cursor too, so the
   *  fallback resumes where the stream stopped instead of replaying it. */
  function tell(frame: BrainStreamFrame): void {
    held = frame.seq;
    dispatch({ kind: "frame", frame });
  }

  /** Closing is idempotent and always forgets the socket first: an `error`
   *  arriving out of a close must not close a stream opened after it. */
  function drop(): void {
    const spent = source;
    source = null;
    if (spent !== null) spent.close();
  }

  /** A malformed frame is DROPPED, never dispatched: the seq discontinuity it
   *  leaves is what asks for a snapshot, while a parse error says nothing
   *  about whether the transport is alive. */
  function receive(message: BrainStreamMessage): void {
    if (typeof message.data !== "string") return;
    let payload: unknown;
    try {
      payload = JSON.parse(message.data);
    } catch {
      return;
    }
    if (payload === null || typeof payload !== "object") return;
    const seq = (payload as { seq?: unknown }).seq;
    if (typeof seq !== "number") return;
    tell({ seq, event: payload });
  }

  return {
    connect(lastEventId: string | null): void {
      drop();
      let opened: BrainStreamSource | null = null;
      try {
        opened = deps.openSource(lastEventId);
      } catch {
        opened = null;
      }
      if (opened === null) {
        dispatch({ kind: "unsupported" });
        return;
      }
      source = opened;
      opened.addEventListener("open", () => { dispatch({ kind: "opened" }); });
      opened.addEventListener("message", receive);
      opened.addEventListener("error", () => { drop(); dispatch({ kind: "closed" }); });
    },
    requestSnapshot(): void {
      deps.readSnapshotSeq().then(
        (seq) => {
          if (seq === null) { dispatch({ kind: "closed" }); return; }
          held = seq;
          dispatch({ kind: "snapshot", seq });
        },
        () => { dispatch({ kind: "closed" }); },
      );
    },
    pollOnce(): void {
      deps.readTail(held).then(
        (frames) => { for (const frame of frames) tell(frame); },
        () => { dispatch({ kind: "closed" }); },
      );
    },
    schedule(ms: number, resume: () => void): () => void {
      return deps.schedule(ms, resume);
    },
    close(): void {
      drop();
    },
  };
}
<<<END HOSTSRC
