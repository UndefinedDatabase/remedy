── STEP T003/3 — F008 SSE event stream — ROUND 18 ────────────────────────────
Goal:
 T003 continues with the effect RUNNER: the loop that PERFORMS what R17's pure
 driver decides. Effects become calls on an INJECTED host, so the reconnect,
 gap and polling-fallback cycle runs headless under the node-environment
 vitest against a recording host and a hand-fired clock. R18 also fixes R-0624
 inside that runner, records the R17 verdict, resolves R-0623 and registers
 R-0625 and R-0626.

Bundle, in this commit order:
 C0a  save this block verbatim to `.agent/authored/f008-r18.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R18, applied whole
 C2   `.agent/live_review.md` <- LEDGER18, appended
 C3   `apps/ui/src/api/brainStreamRunner.ts` <- RUNNER, a new file
 C4   `apps/ui/src/api/brainStreamRunner.test.ts` <- RUNNERTESTS, a new file
 C5   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r18.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamRunner.ts`,
 `apps/ui/src/api/brainStreamRunner.test.ts`, `.agent/handoff.md`.

Slice convention:
 The authored units below are PLANF008R18, LEDGER18, RUNNER and RUNNERTESTS,
 each delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of the slice. Every slice is
 newline-terminated with no trailing whitespace on any line.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, apply it as written and say
    so in the handback's deviations section — do not fix it.
 2. The commit order above is fixed: no extra commit, no dropped commit, no
    reordering. C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. No dependency is added — in
    particular no eslint parser and no jsdom.
 4. C3 lands the runner before C4 lands its tests. C3 is untested, never red:
    it adds a new module no other module imports yet.
 5. WRITE NO `Done:` PARAGRAPH FOR R-0624, though C3 lands its fix: only
    reviewer-authored text sets a resolution (§4 item 4) and R19 owes that
    paragraph, exactly as R17 left R-0623's resolution to this round. LEDGER18
    already covers the round, so write no `Landed:` line either.
 6. R-0622 stays OPEN — do not add a TypeScript parser to make lint green.
    R-0625 and R-0626 are REGISTERED and NOT fixed here.
 7. The post-C5 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md`: C5 cannot state
    facts about itself (R-0371).
 8. Two test processes never run at once. G8's counting suites run in the
    PRIMARY checkout: a fresh worktree has no `apps/ui/node_modules`, so its
    counts are untrustworthy both ways (R-0518). Where G9 needs `node_modules`
    in a worktree it SYMLINKS the primary one — never a copy, which dereferences
    npm's bin shims and manufactures failures (R-0591); the session guard
    rejects `ln` by form, so use `os.symlink`.
 9. The reviewer's OWN base readings, each produced by RUNNING the tool at
    `2c3abc5e` before this block was written rather than recalled (the R-0625
    counter-measure). In `apps/ui`: `npx vitest run` exits 0 at 6 files and 103
    tests; `npm run --silent typecheck` exits 0 with no output;
    `npm run --silent lint` EXITS 1 at `53 problems (51 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here. From the
    root the state readers plus canary exit 0 at 465 and `tests/ui_contracts/`
    at 397, both passed-plus-skipped — that split moves run to run at an
    unchanged tree, so a bare passed count is never a gate.
 10. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it and leave it
    open. `gh pr list --state open` returned `[]` at the R18 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after each
     of C0a, C0b, C1, C2, C3 and C4. Report each reading; per constraint 7 the
     post-C5 readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of the scratch block you
     were given, of `.agent/authored/f008-r18.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r18.md` by their marker lines, take the COUNT from that
     listing, and report each slice's newline-INCLUDED sha256, bytes and lines.
     Expected: PLANF008R18 95960376, LEDGER18 a6db99e5, RUNNER fefd47e6, RUNNERTESTS e600a055.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R18. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER18 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
     normalised first, has as its LAST FOUR units, in order, LEDGER18's four
     paragraphs. NEGATIVE CONTROL: flip one byte of the remainder and report
     that BOTH readings reject it and both accept the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 196 then 198, `^Done: R-\d+ — ` 2 then 3,
     `^Landed: ` 0 at both, `^Gate: R\d+ — ` 17 then 18 over that many
     DISTINCT keys, `^- R-0625 — ` and `^- R-0626 — ` each 0 then 1,
     `^- R-0627 — ` 0 at both. Report the `Done:` ids at C2 — R-0620, R-0621 and
     R-0623, no others. HEADER SWEEP at C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match, and that the R18 pair
     occurs EXACTLY ONCE.
 G7  The two new files. Report that `git ls-tree 2c3abc5e -- <path>` returns
     EMPTY output for each of `apps/ui/src/api/brainStreamRunner.ts` and
     `apps/ui/src/api/brainStreamRunner.test.ts`, so both are ABSENT at base.
     Report each file's sha256, bytes and lines at its own commit and whether
     it is BYTE-EQUAL to its slice, and `git show --numstat` for each: the
     insertions equal that slice's own line count against 0 deletions.
 G8  The suites are green in the PRIMARY checkout, run SERIALLY. Report the
     exit code and counts of each. In `apps/ui` AT C4: `npx vitest run` exits
     0 at 7 files and 114 tests, and `npm run --silent typecheck` exits 0.
     From the repository root AT C4:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped — the second gated because its
     `test_no_scanlines_in_frontend` rglobs every `.ts` under `apps/ui/src`
     and therefore READS both new files. RECONCILE THE ARITHMETIC RATHER THAN
     ASSERTING A BARE TOTAL: report the number of lines matching `^  it\(` in
     RUNNERTESTS, and that 103 plus that number equals the C4 vitest total.
     Report also `npm run --silent lint` at C4: it EXITS 1 at `55 problems
     (53 errors, 2 warnings)`, constraint 9's base reading plus exactly two
     errors, one `Parsing error` per new file. That is R-0622, not a regression;
     report the real numbers either way and repair nothing. If any identity
     above fails, report the real values and STOP — unless it is false of the
     BASE commit too, which makes it reviewer arithmetic and not a red gate (the
     R-0336 / R-0367 / R-0625 class): then declare it and continue.
 G9  RED CONTROLS — the colour, never a count — in a disposable worktree
     created at C4 under the gitignored `.remedy-wt/`, the primary checkout
     NEVER touched and `apps/ui/node_modules` reached by the symlink
     constraint 8 names. Report the occurrence count of each byte string you
     replace in `apps/ui/src/api/brainStreamRunner.ts` BEFORE mutating; each
     is exactly 1. Apply each mutation SEPARATELY, restore the file
     BYTE-EXACTLY between them, and for each report the exit code and the
     NAMES of the failing tests, running
     `npx vitest run src/api/brainStreamRunner.test.ts`:
     (a) `status: settled ? state.status : null` becomes `status: state.status`;
     (b) `if (event.kind !== "timer") settled = true;` becomes `settled = true;`;
     (c) `arm(effect.ms, () => { host.pollOnce(); dispatch({ kind: "timer" }); });` becomes `arm(effect.ms, () => { dispatch({ kind: "timer" }); });`;
     (d) the two lines `    if (stopped) return;` and `    const step` at the head of `dispatch` become `    const step` alone.
     Each EXITS 1 and names at least one failing test. Report that the
     restored file EXITS 0, and REMOVE the worktree before writing C5.
 G10 The range. Report `git diff --name-only 2c3abc5e..C4` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — six paths, none on
     either side alone. The full `2c3abc5e..C5` reading belongs to the ROUND
     REPORT (constraint 7, R-0371). Report that every commit in the range has
     exactly ONE parent, and BOTH numstat cells per path from
     `git show --numstat`, cross-checked against `git diff --numstat`, every
     insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (§3 item 28).
 G11 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2, the runner at C3,
     its test file at C4 and `.agent/handoff.md` at C5. Each is 0.
 G12 Reflog. Count THIS round's own entries by the OPERATION before the first
     `:` in `%gs`. All six pre-C5 entries are `commit`; report `amend`, `rebase`
     and `cherry` at 0, and assert no total.
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2, C3, C4 and C5 — "exactly one row"
     scoping to that TABLE, not to the whole file. Measure its line count with
     `wc -l` BEFORE committing it; seven commits allow 100 lines, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; the raw
     transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~85 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R18
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map; this file repeats
none of them.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat, and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the client transcript byte-equals the
ledger's envelope sequence, the heartbeat holds cadence, and the fallback
engages on a disabled EventSource and recovers to live.

## Current Step
R18 CONTINUES T003 with the effect RUNNER: the loop that PERFORMS what R17's
driver decides. Effects become calls on an INJECTED host — connect, snapshot,
poll, schedule — so the reconnect, gap and fallback cycle runs headless under
the node-environment vitest against a recording host and a hand-fired clock.
That is the feature file's "fake job streaming into a headless client" at the
client-logic level, and it is what keeps R19's React hook thin enough to be
honest. R18 also fixes R-0624 by declining to report a status before the first
transport event resolves, records the R17 verdict, resolves R-0623 and
registers R-0625 and R-0626.

## Next Steps
1. R19 adds the thin React `useBrainStream` hook subscribing to the runner,
   the visible delayed badge and R-0626's rename; the badge is what finally
   renders the runner's view.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `2c3abc5e` it exits 1 with 53 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622, it routes to a paydown branch, and each new `.ts` file adds
  one more. `npm run typecheck` and `npx vitest run` both exit 0 there and ARE
  the gates. Repository-wide `ruff check .` is RED too and is not a gate; this
  round changes no Python.
- No React hook can be rendered by any gate this repository owns. R18 adds
  none: the runner is framework-free on purpose, so R19's hook has no branch
  left to get wrong. If that stops being true, the honest move is a jsdom
  dependency and its own round, never an untested hook.
- R-0624's fix lands here and its `Done:` paragraph is owed by R19, exactly as
  R17 left R-0623 to this round.
<<<END PLANF008R18

<<<SLICE LEDGER18
Done: R-0623 — RESOLVED at `b3c80044` by asserting the LITERAL on both sides: the cap test now reads `expect(BRAIN_BACKOFF_CAP_MS).toBe(8000)` beside `expect(brainBackoffDelayMs(20)).toBe(8000)`, so the constant is pinned by a value that does not move with it. RE-MEASURED BY THE REVIEWER at the R18 gate rather than read back out of the handback: in a disposable worktree with `node_modules` symlinked, raising `BRAIN_BACKOFF_CAP_MS` from 8000 to 60000 EXITS 1 against the `b3060d71` tree naming exactly `brainBackoffDelayMs > is capped so a long outage keeps retrying`, while the SAME mutation against the `eb2e011c` blob of `apps/ui/src/api/brainStream.test.ts` — verified byte-identical to the `4b8c289a` blob — EXITS 0 at 18 passed. That contrast IS the resolution: the same command against two trees, red on the pinned one and green on the one that pinned nothing. The comment R-0623 found false is now true of both constants it names.

- R-0625 — Medium — A MEASURED COUNT MIS-TRANSCRIBED INTO AN APPEND-ONLY RECORD, SO THE AUDIT TRAIL CARRIES A FALSE READING OF A COMMIT NOBODY WILL RE-RUN. The `Gate: R17` entry committed at `4b8c289a` states, as the reviewer's own re-derivation of R16, that `npx vitest run` "exits 0 at 6 files and 89 tests". The TEST total is right and the FILE count is wrong. MEASURED AT THE R18 GATE, not reasoned: `git ls-tree -r eb2e011c -- apps/ui/src` lists exactly FIVE paths ending `.test.ts` — `api/brainStream.test.ts`, `api/remedyApi.test.ts`, `cockpitLogic.test.ts`, `components/graph/buildForceBrainModel.test.ts` and `components/prompt/promptTraceLens.test.ts` — and `apps/ui/vitest.config.ts` at that same commit includes `src/**/*.test.ts` and nothing else, so a sixth file had nowhere to come from. FOUND BY THE WORKER, which hit the same numeral again in gate G9 of the R17 block, declared the deviation and CONTINUED rather than stopping, on the reading that a false identity about the BASE commit is reviewer arithmetic and not a red gate. That reading was right, and this is the fourth consecutive round in which a worker's declaration rather than a gate is what put a reviewer-authored defect on the record. WHY MEDIUM RATHER THAN LOW: no code is wrong and no gate was weakened, but `.agent/live_review.md` is what a later session reads to learn what was verified, and a wrong count there is indistinguishable from a right one without re-running a commit that has already been reviewed and closed. THE FIX IS THIS PARAGRAPH AND EXPLICITLY NOT A REWRITE: §3 item 20 of `docs/agents/planner_reviewer_prompt.md` rules that appending a dated correction is how this record stays honest and that overwriting landed text is worse than a dated wrong sentence, and item 26 repeats it for a header — so the landed entry stands and the correct reading is here. THE CORRECTED VALUE: R16's `apps/ui` suite at `eb2e011c` is FIVE files and 89 tests. THE COUNTER-MEASURE, owed to §3 as a checklist item and not to this body, which binds nothing (the R-0452 class): a numeral a block states about ANOTHER commit's tool output is produced by RUNNING that tool at that commit before emission, never by recollection — R-0364 applied to a value rather than to a colour. It routes to the paydown branch that already carries the promotions owed for R-0387 and R-0573, because no F008 round has a `docs/agents/**` path in its change set.

- R-0626 — Low — ONE SPELLING CARRYING TWO CONCEPTS INSIDE ONE `switch`, IN THE MODULE WHERE BOTH MEANINGS ARE LIVE. In `apps/ui/src/api/brainStreamDriver.ts` at `2d49be87`, the `frame` case reads `const opened = next.gapDetected && !state.gapDetected;`, where `opened` means A GAP OPENED, while `case "opened":` five lines above is the transport event meaning A CONNECTION OPENED. AUTHORED BY THE REVIEWER in the R17 block's DRIVER slice and applied byte for byte as constraint 1 required; FOUND AND DECLARED BY THE WORKER as an objection it was never asked for. THE BEHAVIOUR IS CORRECT AND PROVED SO: red control (b) of the R17 gate replaces that line with `const opened = false;` and EXITS 1, naming `a gap in the sequence > asks for a snapshot exactly once, not once per later frame` and `the polling fallback > a gap over the fallback still asks for a snapshot and resumes by polling` — re-run by the reviewer at the R18 gate, not read back. WHAT IS WRONG IS THE NAME: AGENTS.md's Code Discoverability Conventions require one spelling per concept repo-wide and forbid synonym drift, and a name colliding with the event kind it sits beside is the sharper form of that defect, because the reader who misreads it is reading the two lines together. WHY LOW: it is a local `const` with no callers, so no other module can resolve it wrongly, and the collision costs a reader a second glance rather than a wrong belief about behaviour. WHY NOT FIXED BY THE ROUND THAT REGISTERS IT: R18's change set is the runner and the state files, and R19 edits this module's consumer anyway, so the rename lands beside work that already reads these lines. THE FIX, routed to R19 and named in this round's plan: `gapOpened`, which carries the two-to-four-word domain-name rule AGENTS.md states and cannot be confused with the event kind.

Gate: R18 — the R17 entry. R17 PASSED. No finding is registered against its work: every gate it reported was RE-DERIVED by the reviewer off disk rather than read back out of the handback, and every value matched. Two findings ARE registered this round, R-0625 and R-0626 above, and BOTH are defects in the reviewer's own authored text that the worker declared — the round did exactly what its block ordered, and its one declared deviation was correct. TRANSPORT PROVED BY THE DIGEST FALLBACK, declared as such because this is a new session and the previous reviewer's scratch original no longer exists (section 4 item 9): `.agent/authored/f008-r17.md` at `d8d21cc7` and `.agent/last_block.md` at `debaa1f0` are EQUAL at sha256 5d90c4a54fd6cb2807a9b744d414a422fa2437e1ebb5d631ba4db5449087de9d over 34888 bytes and 490 lines, which is the value the handback names. SIX SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching: PLANF008R17 8ff56a6d, LEDGER17 dc331d6f, CAPFROM 23996c0e, CAPTO a53bfa48, DRIVER 570ca900 and DRIVERTESTS 7e36247f. THE PLAN LANDED FIRST at `16b48915`, byte-equal to PLANF008R17 at 49 lines under the 50-line cap. THE APPEND at `4b8c289a` is a byte-exact prefix of the `16b48915` blob plus a 7568-byte remainder equal to a newline plus LEDGER17, agreed by an INDEPENDENT blank-line split of the whole file into 219 units whose LAST THREE are LEDGER17's paragraphs in order. THE SETS MOVED AS ORDERED between `16b48915` and `4b8c289a` — 194 to 196 registered, `Done:` 2 at both over exactly the ids R-0620 and R-0621, `Landed:` 0 at both, `Gate: R` 16 to 17 over seventeen DISTINCT keys, R-0623 and R-0624 each 0 then 1, R-0625 0 at both — so the round minted exactly the two ids it was ordered to mint; sixteen of the seventeen headers match the `Gate: R<n> — the R<n-1> entry.` shape with the second numeral one below the first, and the single non-match is the F255 entry, which is correctly shaped for what it records. THE CAP PAIR IS CONSTRUCTIVE: CAPFROM occurs exactly once in the `4b8c289a` blob and zero times at `b3c80044`, CAPTO the reverse, `TO contains FROM` is false, and replacing that one occurrence rebuilds a file byte-equal to the `b3c80044` blob at sha256 7bea89dc. BOTH NEW FILES ARE ABSENT at `eb2e011c` by `git ls-tree` and byte-equal to their slices at `2d49be87` and `b3060d71`, 92 and 119 lines against 0 deletions. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 6 files and 103 tests, `npm run --silent typecheck` exits 0 silently, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 397. THE ARITHMETIC RECONCILES: DRIVERTESTS holds 14 lines matching `^  it(` and 89 plus 14 is 103. LINT IS RED AND DECLARED, never repaired: 53 problems against the base's 51, exactly two more errors, one `Parsing error` per new file, which is R-0622 and not a regression. ALL FOUR RED CONTROLS RE-RUN BY THE REVIEWER in its own disposable worktree with `node_modules` symlinked and the primary checkout untouched: each mutated byte string occurs exactly once, each mutation EXITS 1 naming the tests the block predicted, the restored files EXIT 0 at 32 passed, and both halves of the R-0623 proof reproduce. EIGHT single-parent commits, insertions 490, 385, 25, 6, 5, 92, 119 and 50 in that order, every one under 500 and every cell equal to the handback's `+/-` column including the deletions; zero lines beginning with a slice marker in all six targets; the last forty reflog operations all `commit`, with amend, rebase and cherry at 0; the tree clean with the primary checkout the only worktree.
<<<END LEDGER18

<<<SLICE RUNNER
// Effect interpretation for the brain stream: the loop that PERFORMS what
// brainStreamDriver decides, by turning its effects into calls on an INJECTED
// host. That is what lets the whole connect, backoff, snapshot and poll cycle
// run under the node-environment vitest — no EventSource, no timer, no React.
import { initialBrainStreamState, resumeEventId } from "./brainStream";
import type { BrainStreamStatus } from "./brainStream";
import { stepBrainStream } from "./brainStreamDriver";
import type { BrainStreamEffect, BrainStreamEvent } from "./brainStreamDriver";

/** What the runner asks of its environment: an EventSource, setTimeout and two
 *  api reads in production, four recorders in a test. */
export interface BrainStreamHost {
  /** Open a stream from the resume position; frames arrive via `dispatch`. */
  connect(lastEventId: string | null): void;
  /** Refetch the state snapshot; its position arrives as a `snapshot` event. */
  requestSnapshot(): void;
  /** Read the events tail once, on the polling fallback's cadence. */
  pollOnce(): void;
  /** Run `resume` after `ms`. The returned function cancels that pending run. */
  schedule(ms: number, resume: () => void): () => void;
}

/** What a badge reads. `status` is NULL until the first transport event has
 *  resolved, because a client that has never connected has no honest status and
 *  the initial `reconnecting` would claim a history it does not have (finding
 *  R-0624). Null is not a fourth status: the union the feature file fixes is
 *  untouched and the runner simply declines to report before it knows. */
export interface BrainStreamView {
  status: BrainStreamStatus | null;
  lastSeq: number | null;
  gapDetected: boolean;
}

export interface BrainStreamRunner {
  start(): void;
  dispatch(event: BrainStreamEvent): void;
  stop(): void;
  view(): BrainStreamView;
}

/** Remedy deliberately gives this no change callback yet: nothing subscribes
 *  until R19's hook exists, and a listener with no reader is untestable. */
export function createBrainStreamRunner(host: BrainStreamHost): BrainStreamRunner {
  let state = initialBrainStreamState();
  let settled = false;
  let stopped = false;
  let cancelPending: (() => void) | null = null;

  function view(): BrainStreamView {
    return {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
    };
  }

  /** At most one timer outstanding: a second wait armed over a pending one
   *  would double the reconnect rate the backoff exists to bound. */
  function arm(ms: number, resume: () => void): void {
    if (cancelPending !== null) cancelPending();
    cancelPending = host.schedule(ms, () => {
      cancelPending = null;
      if (!stopped) resume();
    });
  }

  function perform(effect: BrainStreamEffect): void {
    switch (effect.kind) {
      case "connect":
        host.connect(effect.lastEventId);
        return;
      case "snapshot":
        host.requestSnapshot();
        return;
      case "wait":
        arm(effect.ms, () => { dispatch({ kind: "timer" }); });
        return;
      case "poll":
        arm(effect.ms, () => { host.pollOnce(); dispatch({ kind: "timer" }); });
        return;
    }
  }

  /** A `timer` is the runner's own bookkeeping, so it never resolves the
   *  status: only an event the TRANSPORT produced says what to show. */
  function dispatch(event: BrainStreamEvent): void {
    if (stopped) return;
    const step = stepBrainStream(state, event);
    state = step.state;
    if (event.kind !== "timer") settled = true;
    for (const effect of step.effects) perform(effect);
  }

  return {
    start(): void {
      stopped = false;
      host.connect(resumeEventId(state));
    },
    dispatch,
    stop(): void {
      stopped = true;
      if (cancelPending !== null) cancelPending();
      cancelPending = null;
    },
    view,
  };
}
<<<END RUNNER

<<<SLICE RUNNERTESTS
import { describe, it, expect } from "vitest";
import { createBrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamHost, BrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamEvent } from "./brainStreamDriver";

interface ArmedTimer { ms: number; resume: () => void; spent: boolean }

/** Records every call and holds its timers until fired by hand, so the
 *  reconnect and poll cadences are read as data instead of waited for. */
class RecordingHost implements BrainStreamHost {
  connects: (string | null)[] = [];
  snapshots = 0;
  polls = 0;
  timers: ArmedTimer[] = [];

  connect(lastEventId: string | null): void { this.connects.push(lastEventId); }
  requestSnapshot(): void { this.snapshots += 1; }
  pollOnce(): void { this.polls += 1; }
  schedule(ms: number, resume: () => void): () => void {
    const armed: ArmedTimer = { ms, resume, spent: false };
    this.timers.push(armed);
    return () => { armed.spent = true; };
  }

  /** Fire the newest live timer — the only one the runner treats as pending. */
  tick(): void {
    for (let i = this.timers.length - 1; i >= 0; i -= 1) {
      const armed = this.timers[i];
      if (!armed.spent) { armed.spent = true; armed.resume(); return; }
    }
    throw new Error("no live timer to fire");
  }

  live(): number { return this.timers.filter((t) => !t.spent).length; }
  waits(): number[] { return this.timers.map((t) => t.ms); }
}

function started(): { host: RecordingHost; runner: BrainStreamRunner } {
  const host = new RecordingHost();
  const runner = createBrainStreamRunner(host);
  runner.start();
  return { host, runner };
}

function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } } };
}

describe("a runner that has not connected", () => {
  it("reports no status at all rather than claiming a reconnect", () => {
    const host = new RecordingHost();
    const runner = createBrainStreamRunner(host);
    expect(runner.view().status).toBe(null);
    runner.start();
    expect(runner.view().status).toBe(null);
    expect(host.connects).toEqual([null]);
  });
  it("is not resolved by a stray timer, which is its own bookkeeping", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "timer" });
    expect(runner.view().status).toBe(null);
    expect(host.connects).toEqual([null, null]);
  });
  it("resolves the status on the first transport event", () => {
    const { runner } = started();
    runner.dispatch({ kind: "opened" });
    expect(runner.view().status).toBe("live");
  });
});

describe("a dropped connection", () => {
  it("arms the backoff and reconnects from the frame it holds", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(7));
    runner.dispatch({ kind: "closed" });
    expect(host.waits()).toEqual([250]);
    expect(host.connects).toEqual([null]);
    host.tick();
    expect(host.connects).toEqual([null, "7"]);
  });
  it("lengthens the armed wait on every further drop", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    expect(host.waits()).toEqual([250, 500, 1000]);
  });
  it("keeps at most one timer live so the rate stays bounded", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    expect(host.timers.length).toBe(2);
    expect(host.live()).toBe(1);
  });
});

describe("a gap in the sequence", () => {
  it("asks the host for a snapshot exactly once", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(0));
    runner.dispatch(frame(4));
    runner.dispatch(frame(5));
    expect(host.snapshots).toBe(1);
  });
  it("reconnects from the healed position once the snapshot lands", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(0));
    runner.dispatch(frame(4));
    runner.dispatch({ kind: "snapshot", seq: 9 });
    expect(host.connects).toEqual([null, "9"]);
    expect(runner.view().gapDetected).toBe(false);
    expect(runner.view().lastSeq).toBe(9);
  });
});

describe("the polling fallback", () => {
  it("engages on an unsupported transport and labels itself delayed", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    expect(runner.view().status).toBe("delayed");
    expect(host.waits()).toEqual([3000]);
  });
  it("reads the tail once per tick and re-arms the next one", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    host.tick();
    expect(host.polls).toBe(1);
    expect(host.live()).toBe(1);
    host.tick();
    expect(host.polls).toBe(2);
    expect(host.connects).toEqual([null]);
  });
});

describe("stopping the runner", () => {
  it("cancels the pending timer and ignores every later event", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.stop();
    expect(host.live()).toBe(0);
    runner.dispatch({ kind: "opened" });
    expect(runner.view().status).toBe("reconnecting");
    expect(host.connects).toEqual([null]);
  });
});
<<<END RUNNERTESTS
