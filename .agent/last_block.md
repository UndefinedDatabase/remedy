── STEP R17/1 — F008 SSE event stream · T003 ORCHESTRATION ─────
Goal:        Give T003 its transport orchestration, still pure. R16 built the
             rules a client HOLDS; this round builds what it should DO next —
             a reducer over transport events returning effects as DATA
             (connect, wait, snapshot, poll), so the reconnect schedule, the
             gap-to-snapshot-to-resume path and the polling fallback are
             decided in code the node-environment vitest can run. Nothing
             performs an effect: no EventSource, no timer, no fetch. R17 also
             pins the backoff cap against a LITERAL (R-0623), records the R16
             verdict (PASS) and registers R-0623 and R-0624.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0623 and R-0624 and record the R16 verdict ·
             C3 pin the backoff cap · C4 the driver module · C5 its tests ·
             C6 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r17.md                  (C0a, new)
             - .agent/last_block.md                         (C0b, rewrite)
             - .agent/plan.md                               (C1, rewrite)
             - .agent/live_review.md                        (C2, append)
             - apps/ui/src/api/brainStream.test.ts          (C3, pair)
             - apps/ui/src/api/brainStreamDriver.ts         (C4, new)
             - apps/ui/src/api/brainStreamDriver.test.ts    (C5, new)
             - .agent/handoff.md                            (C6, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r17.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback: your last two
    rounds each caught a defect no gate could see, and C2 registers both.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers, trailing newline
    INCLUDED. PLANF008R17 is the ENTIRE content of `.agent/plan.md`. DRIVER
    and DRIVERTESTS are each the ENTIRE content of a file that does not yet
    exist, so neither is a pair. LEDGER17 is a newline plus its body, appended
    after exactly one blank line. Every file ends with exactly one newline.
 3. PAIR SHAPE, MEASURED NOT ASSERTED. CAPFROM/CAPTO is the only pair this
    round. The containment test was run before emission and printed
    `TO contains FROM: false`, so it is a REWRITE and owes the FROM-0x / TO-1x
    proof of G7 and NOT the append obligation. CAPFROM occurs EXACTLY ONCE in
    `apps/ui/src/api/brainStream.test.ts` at C2; if it does not, stop and say
    so rather than choosing an occurrence.
 4. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, C6.
    `.agent/plan.md` advances at C1, ahead of the ledger commit (section 3
    item 23). C3 is the R-0623 paydown and lands BEFORE the new module so its
    suite reading stays comparable with the base. C4 precedes C5 because C5
    imports C4; committing the test first would land a knowingly red commit.
 5. LEDGER17 carries THREE paragraphs, blank-line separated, applied together
    in C2: the R-0623 registration, the R-0624 registration and the
    `Gate: R17` entry holding the R16 verdict. R-0623 and R-0624 are the only
    ids minted, so the next free id becomes R-0625. NO `Done:` PARAGRAPH IS
    WRITTEN THIS ROUND, not even for R-0623 whose fix C3 lands: only
    reviewer-authored text sets Resolved (section 4 item 4), so R-0623's
    resolution is owed by R18 and G6 therefore reads the `Done:` count
    UNCHANGED at 2.
 6. SCOPE. No Python changes at all. No React component, no hook, no
    `EventSource` construction, no timer, no `fetch`, no CSS, and no new entry
    in `apps/ui/package.json`. The driver decides and returns effects; it
    never performs one. R-0624 is REGISTERED and NOT fixed — its fix needs the
    badge, which is R18's work. R-0622 likewise stays open: do not add a lint
    parser.
 7. `git status --porcelain` is empty after each of C0a through C5, and
    `git worktree list` names the primary checkout alone once G10's worktree is
    removed. READINGS OF STATE AT OR AFTER C6 GO IN THE ROUND REPORT, NEVER IN
    THE HANDBACK FILE: state after the handback commit cannot be recorded
    inside it, and a gate ordering it anyway is finding R-0371. Base bytes
    reach a tool by `git show <sha>:<path>` or a disposable worktree under the
    gitignored `.remedy-wt/`, never by overwrite-and-restore in the primary
    checkout (self_drive_protocol G5).
 8. Two test processes never run at once. G9's counting suites run in the
    PRIMARY checkout: a fresh worktree has no `apps/ui/node_modules`, so its
    counts are untrustworthy in both directions (R-0518). Where G10 needs
    `node_modules` inside a worktree it SYMLINKS the primary one — `ln -s`,
    never a copy, because a copy dereferences npm's bin shims and manufactures
    its own failures (R-0591).
 9. The reviewer's own base readings at `eb2e011c`, RE-DERIVED by the gates
    below rather than trusted. In `apps/ui`: `npx vitest run` exits 0 at 6
    files and 89 tests; `npm run --silent typecheck` exits 0 silently;
    `npm run --silent lint` EXITS 1 at `51 problems (49 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here. From the
    root the state readers plus canary exit 0 at 465 and `tests/ui_contracts/`
    at 397, both passed-plus-skipped — that split moves run to run, so a bare
    passed count is never the gate value.
 10. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it, leave it open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     each of C0a through C5. Report each reading. Per constraint 7 the post-C6
     porcelain and the final `git worktree list` belong to the ROUND REPORT.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block you were given, of `.agent/authored/f008-r17.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r17.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R17. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — those four are what
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER17 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the C2 file, its terminating newline
     normalised first, has as its LAST THREE units, in order, the three
     paragraphs of LEDGER17. NEGATIVE CONTROL: flip one byte of the remainder
     and report that BOTH readings reject it, and that both accept the
     unflipped bytes.
 G6  The sets, at C1 and C2. Report line-anchored counts in
     `.agent/live_review.md`: `^- R-\d+ — ` reads 194 then 196,
     `^Done: R-\d+ — ` is 2 at BOTH (constraint 5), `^Landed: ` is 0 at both,
     `^Gate: R\d+ — ` reads 16 then 17 with the seventeen keys DISTINCT,
     `^- R-0623 — ` and `^- R-0624 — ` each read 0 then 1, and
     `^- R-0625 — ` is 0 at both. Report that the two `Done:` ids at C2 are
     still exactly R-0620 and R-0621. Report that LEDGER17's `Gate:` header
     matches the shape of the entries already in the file, as a pattern match
     over `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to
     be one less than the first and the R17 pair to occur exactly once
     (section 3 item 26). Report the number of `^Gate: ` lines that do NOT
     match; it is 1, and that line is `Gate: R1 — the F255 R21 entry.`
 G7  The cap pair, a REWRITE per constraint 3. Report that CAPFROM occurs
     EXACTLY ONCE in `apps/ui/src/api/brainStream.test.ts` at C2 and ZERO
     times at C3, and that CAPTO occurs zero times at C2 and exactly once at
     C3. Then prove it constructively as well: replacing that one occurrence
     of CAPFROM with CAPTO in the C2 blob yields a file BYTE-EQUAL to the C3
     blob — report both sha256s.
 G8  The two new files. Report that `apps/ui/src/api/brainStreamDriver.ts` and
     `apps/ui/src/api/brainStreamDriver.test.ts` are both ABSENT at
     `eb2e011c`, using `git ls-tree eb2e011c -- <path>` per path and reporting
     its empty output. Report the sha256, bytes and lines of the C4 blob of
     the first and the C5 blob of the second, and whether each is BYTE-EQUAL
     to DRIVER and to DRIVERTESTS respectively. Both files being new, the whole
     of each commit's diff is additions: report that `git show --numstat`
     gives each path its slice's own line count against 0 deletions.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY, never two
     test processes at once. Report the exit code and counts of each. In
     `apps/ui` AT C3: `npx vitest run` exits 0 at 6 files and 89 tests — the
     cap pair changed an assertion and added no test, so this equals
     constraint 9's base reading exactly. In `apps/ui` AT C5: `npx vitest run`
     exits 0 at 7 files and 103 tests, and `npm run --silent typecheck` exits
     0. From the repository root AT C5:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped — gated because its `test_no_scanlines_in_frontend`
     rglobs every `.ts` under `apps/ui/src`, reading both new files.
     RECONCILE THE ARITHMETIC RATHER THAN ASSERTING A BARE TOTAL: report the
     number of lines matching
     `^  it(` in DRIVERTESTS, and report that 89 plus that number equals the
     C5 vitest total. Report also `npm run --silent lint` at C5: it EXITS 1 at
     `53 problems (51 errors, 2 warnings)`, which is constraint 9's base
     reading plus exactly two errors, one `Parsing error` per new file. That
     is R-0622 and NOT a regression; report the real numbers either way and
     repair nothing. If any identity fails, report the real values and stop.
 G10 RED CONTROLS, the colour and not a count, in a disposable worktree created
     at C5 under `.remedy-wt/`, with the primary checkout never touched and
     `apps/ui/node_modules` reached by the symlink constraint 8 names. Apply
     each mutation SEPARATELY to the worktree's copy of the named file,
     restoring it byte-exactly between them, and report for each the exit code
     and the NAMES of the failing tests:
     (a) in `apps/ui/src/api/brainStreamDriver.ts`, `brainBackoffDelayMs(next.attempt)` becomes `0`;
     (b) in the same file, `const opened = next.gapDetected && !state.gapDetected;` becomes `const opened = false;`;
     (c) in the same file, `return state.status === "delayed";` becomes `return false;`;
     (d) in `apps/ui/src/api/brainStream.ts`, `export const BRAIN_BACKOFF_CAP_MS = 8000;` becomes `export const BRAIN_BACKOFF_CAP_MS = 60000;` — this one is the R-0623 PROOF, and it is run against BOTH test files: it must EXIT 1 naming
     `brainBackoffDelayMs > is capped so a long outage keeps retrying`. The
     same mutation against the C2 blob of `apps/ui/src/api/brainStream.test.ts`
     EXITS 0 at 18 passed, and that contrast IS the finding — report both.
     Report the occurrence count of each byte string you replace in its named
     file BEFORE mutating; each is exactly 1. Each mutation EXITS 1 and names
     at least one failing test. Report that the restored tree EXITS 0, and
     remove the worktree before the handback.
 G11 The range. Report `git diff --name-only eb2e011c..C5` and that it equals
     the Change list MINUS `.agent/handoff.md` exactly — seven paths, none on
     either side alone. The full `eb2e011c..C6` reading belongs to the ROUND
     REPORT (constraint 7). Report that every commit in the range has exactly
     one parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, with every insertion under
     500 and every cell equal to the `+/-` column of your `## Commits` table,
     cell by cell (section 3 item 28).
 G12 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `apps/ui/src/api/brainStream.test.ts` at C3,
     `apps/ui/src/api/brainStreamDriver.ts` at C4,
     `apps/ui/src/api/brainStreamDriver.test.ts` at C5 and
     `.agent/handoff.md` at C6. Each is 0.
 G13 Report this round's own reflog entries counted by the OPERATION before
     the first `:` in `%gs`: `amend`, `rebase` and `cherry` are each 0. Assert
     no total. An unstage is not a history rewrite (R-0608).
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md, and its ITEM-STATUS TABLE holds exactly
     one row for each of C0a, C0b, C1, C2, C3, C4, C5 and C6 — that table is
     where the once-each reading is taken, the prose naturally naming a label
     many times. Measure the file with `wc -l` BEFORE writing it: this round's
     eight commits allow 100 lines, and an overage needs a DECISION D15
     stated-cause line naming the real count.

Handback:    completion report + rewrite `.agent/handoff.md`. Its state block
             repeats this Fortschritt line verbatim:
             `~80 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber ✅, Hook offen) — Schätzung`.
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R17
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
R17 CONTINUES T003 with the transport ORCHESTRATION, still pure. R16 built the
rules a client holds; a new driver module says what it should DO next, as a
reducer returning effects as DATA — connect, wait, snapshot, poll — so the
reconnect schedule, the gap-to-snapshot-to-resume path and the polling
fallback are decided in code the node-environment vitest can run. Nothing
performs an effect yet: no EventSource, no timer, no fetch. R17 also pins the
backoff cap against a LITERAL (R-0623), records the R16 verdict and registers
R-0623 and R-0624.

## Next Steps
1. R18 adds the thin React `useBrainStream` hook interpreting the driver's
   effects, the visible delayed badge and the fixture live-job end-to-end;
   R-0624's fix lands there, with the badge that exposes it.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `eb2e011c` it exits 1 with 51 problems, every error a
  `Parsing error`, because that eslint configuration installs no TypeScript
  parser. That is R-0622, it routes to a paydown branch, and each new `.ts`
  file adds one more such error. `npm run typecheck` and `npx vitest run`
  both exit 0 at that commit and ARE the gates.
- A React hook still cannot be rendered by any gate this repository owns, so
  R18's hook stays thin enough that typecheck plus the driver's tests cover
  it. If that stops being true, the honest move is a jsdom dependency and its
  own round, never an untested hook.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364); this round
  changes no Python.
- No open finding is a code defect of F008 reachable from the HTTP path; the
  open set lives in `.agent/live_review.md`, not here. R-0623 and R-0624 both
  ENTER it this round, and R-0623's fix lands here too, so R18 resolves it.
<<<END PLANF008R17
<<<SLICE LEDGER17
- R-0623 — Low — A TEST THAT PINS A CONSTANT AGAINST ITSELF, SO THE VALUE IT EXISTS TO GUARD CAN BE CHANGED TO ANYTHING WITHOUT TURNING RED. In the BRAINSTREAM slice of the F008 R16 block, authored by the reviewer and applied byte for byte at `76a89aaf`, `BRAIN_BACKOFF_BASE_MS` and `BRAIN_BACKOFF_CAP_MS` carry the comment `Backoff floor and ceiling, named so the schedule and its tests cannot drift.` — but the STREAMTESTS slice at `06c9dac1` imports only the CAP and asserts `expect(brainBackoffDelayMs(20)).toBe(BRAIN_BACKOFF_CAP_MS)`, which is the constant compared with itself. FOUND BY THE WORKER, which applied both slices unedited as constraint 1 required and declared the mismatch; that is the fourth consecutive round in which a worker's declaration, not a gate, is what put a reviewer-authored defect on the record. THE WORKER NAMED THE BASE AS THE WEAK HALF AND THE REVIEWER'S RE-MEASUREMENT INVERTS THAT, which is why this entry is worth its length: the two constants behave OPPOSITELY, and the one the comment protects least is the one it names last. RE-MEASURED, not reasoned: in a disposable worktree at `eb2e011c`, raising `BRAIN_BACKOFF_CAP_MS` from 8000 to 60000 with the R16 test file in place leaves `npx vitest run src/api/brainStream.test.ts` at EXIT 0 with 18 passed — the cap is pinned by nothing at all — while the base is hardcoded as `[250, 500, 1000, 2000]` in the same file, so changing IT does go red. The comment claims one property for both names and is false of exactly the half that matters. THE FIX, applied by this round rather than deferred: the cap test asserts the LITERAL 8000 on both sides, and the same re-measurement then EXITS 1 on the raised cap, naming `brainBackoffDelayMs > is capped so a long outage keeps retrying`. WHY LOW: no shipped behaviour was ever wrong, the cap being 8000 in the only file that defines it; what was wrong is that a gate reported protection it did not provide, which is the R-0438 vacuous-gate class arriving through an import rather than through a missing path.

- R-0624 — Low — AN INITIAL STATE THAT CLAIMS A HISTORY IT DOES NOT HAVE: A CLIENT WHICH HAS NEVER CONNECTED REPORTS `reconnecting`. `initialBrainStreamState()` in the BRAINSTREAM slice at `76a89aaf` returns `status: "reconnecting"`, and `BrainStreamStatus` is the three-member union `"live" | "reconnecting" | "delayed"` that the feature file's Design section fixes verbatim as the status surface, so the module has no member meaning "not yet attempted" and the honest value does not exist to be returned. FOUND BY THE WORKER as its second objection, raised without being asked for one. WHY IT IS REGISTERED RATHER THAN WAVED AWAY: this repository treats a status surface as a truth claim — section 4 item 5 of `docs/agents/planner_reviewer_prompt.md` makes a false live indicator a BLOCK condition — and while `reconnecting` is not a false LIVE indicator, it asserts a prior connection that never happened, which a cockpit badge would render verbatim in the first frames after mount. WHY IT IS NOT FIXED BY THE ROUND THAT REGISTERS IT, stated so the deferral is a decision and not an oversight: the defect is only OBSERVABLE where the badge is, and the badge is R18's work. Widening the union is forbidden without a feature-file amendment, and adding an `everConnected` field to the state now would ship a field with no reader for a round. THE FIX, routed to R18 and named in this round's plan: the hook does not surface a status until its first connection attempt has resolved, so the initial value is never rendered — or, if that proves impossible, the reviewer authors the feature-file amendment that adds the fourth member, as section 4 item 7 requires, rather than letting the badge lie.

Gate: R17 — the R16 entry. R16 PASSED. No finding is registered against its work: every gate it reported was RE-DERIVED by the reviewer off disk, and every value matched. Two findings ARE registered this round, R-0623 and R-0624 above, and BOTH are defects in the reviewer's own authored text that the worker declared — the round did exactly what its block ordered. TRANSPORT PROVED PRIMARY, not by the digest fallback: the reviewer authored this block in the same session, so `.remedy-wt/f008-r16.md` still existed at review time and was compared disk-to-disk against `.agent/authored/f008-r16.md` at `212c28aa` and `.agent/last_block.md` at `bbf53bf5` — all three EQUAL at sha256 5f88c012208d3c69e73ad7fc6ea82d62422bcd5221d6f0c1dac650300951f7d6 over 33473 bytes and 457 lines. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching: PLANF008R16 6c7a8637, LEDGER16 275f099c, BRAINSTREAM 82d1ec28 and STREAMTESTS e0c65062. THE PLAN LANDED FIRST at `0b3147e1`, byte-equal at 46 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and two F-ids — the four properties `tests/ui_server/test_dashboard_contract.py` and `tests/orchestration/test_test_runner.py` actually assert about that file, checked against those readers rather than against the cap alone. THE APPEND at `4e799cdc` is a byte-exact prefix plus a 9239-byte remainder equal to a newline plus LEDGER16, agreed by an INDEPENDENT blank-line split into 216 units whose LAST FOUR are LEDGER16's paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped ACCEPTED by both. THE SETS MOVED AS ORDERED — 193 to 194 registered, `Done:` 0 to 2 over exactly the ids R-0620 and R-0621, `Landed:` 0 at both, `Gate: R` 15 to 16 over sixteen DISTINCT keys, R-0622 0 to 1 and R-0623 0 at both — so this record's FIRST two resolutions landed and only one id was minted. BOTH NEW FILES ARE ABSENT at `22dd8d31` by `git ls-tree` and byte-equal to their slices at `76a89aaf` and `06c9dac1`, 92 and 108 lines against 0 deletions. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 6 files and 89 tests, `npm run --silent typecheck` exits 0 silently, the state readers including the canary exit 0 at 465 and `tests/ui_contracts/` exits 0 at 397 passed-plus-skipped — that last suite gated because its `test_no_scanlines_in_frontend` rglobs every `.ts` under `apps/ui/src` and therefore READS both new files. THE ARITHMETIC RECONCILES: STREAMTESTS holds 18 `it(` lines and 71 plus 18 is 89. LINT IS RED AND DECLARED, never repaired: 51 problems against the base's 49, exactly two more errors, one `Parsing error` per new file — which is R-0622, registered this same round. ALL THREE RED CONTROLS RE-RUN BY THE REVIEWER in its own disposable worktree with `node_modules` SYMLINKED and the primary checkout untouched: each mutated byte string occurs exactly once, each mutation EXITS 1 naming the tests the block predicted, and the restored file EXITS 0 at 18 passed. SEVEN single-parent commits, insertions 457, 411, 24, 8, 92, 108 and 42, all under 500 and every cell equal to the handback's `+/-` column; zero marker lines in all five targets; a reflog of `commit` operations alone with amend, rebase and cherry at 0; an 81-line handback under the 100 that seven commits allow, its item-status table naming C0a through C5 exactly once each. ONE NOTE ON A GATE OF MINE RATHER THAN ON THE ROUND: G13 ordered the handback to name C0a through C5 "exactly once each", and a handback names each label many times by construction — the worker read the clause as scoping to the item-status table, which is the only reading that can be satisfied, and was right to. The clause should have said so.
<<<END LEDGER17
<<<SLICE CAPFROM
    expect(brainBackoffDelayMs(20)).toBe(BRAIN_BACKOFF_CAP_MS);
<<<END CAPFROM
<<<SLICE CAPTO
    // The LITERAL is the gate. Asserting only against the imported constant
    // tracks any change to it and therefore pins nothing — the cap could be
    // raised to a minute and this test would stay green (finding R-0623).
    expect(BRAIN_BACKOFF_CAP_MS).toBe(8000);
    expect(brainBackoffDelayMs(20)).toBe(8000);
<<<END CAPTO
<<<SLICE DRIVER
// Transport orchestration for the brain stream, as a pure reducer.
// The rules in brainStream.ts say what a client HOLDS; these say what it
// should DO next — reconnect, wait, refetch a snapshot, or fall back to
// polling. Effects are returned as DATA rather than performed, so the whole
// reconnect and fallback story is testable under the node-environment vitest
// that cannot render the React hook which will interpret them.
import {
  brainBackoffDelayMs, degradeBrainStream, failBrainStream, openBrainStream,
  receiveBrainFrame, repairBrainGap, resumeEventId,
} from "./brainStream";
import type { BrainStreamFrame, BrainStreamState } from "./brainStream";

/** How often the fallback transport re-reads the events tail. */
export const BRAIN_POLL_INTERVAL_MS = 3000;

/** What the transport tells the driver. `unsupported` is the fallback trigger:
 *  no EventSource in this environment, or the stream failed to construct. */
export type BrainStreamEvent =
  | { kind: "opened" }
  | { kind: "frame"; frame: BrainStreamFrame }
  | { kind: "closed" }
  | { kind: "unsupported" }
  | { kind: "snapshot"; seq: number }
  | { kind: "timer" };

/** What the driver asks its host to do. The host performs these; the driver
 *  never touches a socket, a timer or the network itself. */
export type BrainStreamEffect =
  | { kind: "connect"; lastEventId: string | null }
  | { kind: "wait"; ms: number }
  | { kind: "snapshot" }
  | { kind: "poll"; ms: number };

export interface BrainStreamStep {
  state: BrainStreamState;
  effects: BrainStreamEffect[];
}

/** True once the fallback has engaged: `delayed` is sticky for this session,
 *  because a transport that could not be constructed will not spontaneously
 *  become constructible, and a badge that flickered back to `live` would be
 *  claiming a stream the client does not have. */
function isPolling(state: BrainStreamState): boolean {
  return state.status === "delayed";
}

/** Resume where the fallback left off, on the same rule as the stream: the
 *  two transports share one consumer contract and one resume position. */
function resumeEffect(state: BrainStreamState): BrainStreamEffect {
  return isPolling(state)
    ? { kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }
    : { kind: "connect", lastEventId: resumeEventId(state) };
}

/** Advance the client by one transport event, returning the next state and
 *  the effects the host must perform. A gap ALWAYS asks for a snapshot before
 *  anything else: replaying from a position the client never held is how a
 *  hole becomes permanent. */
export function stepBrainStream(
  state: BrainStreamState,
  event: BrainStreamEvent,
): BrainStreamStep {
  switch (event.kind) {
    case "opened":
      return { state: openBrainStream(state), effects: [] };

    case "frame": {
      const next = receiveBrainFrame(state, event.frame);
      const opened = next.gapDetected && !state.gapDetected;
      return { state: next, effects: opened ? [{ kind: "snapshot" }] : [] };
    }

    case "snapshot": {
      const healed = repairBrainGap(state, event.seq);
      return { state: healed, effects: [resumeEffect(healed)] };
    }

    case "closed": {
      if (isPolling(state)) return { state, effects: [{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }] };
      const next = failBrainStream(state);
      return { state: next, effects: [{ kind: "wait", ms: brainBackoffDelayMs(next.attempt) }] };
    }

    case "unsupported": {
      const next = degradeBrainStream(state);
      return { state: next, effects: [{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }] };
    }

    case "timer":
      return { state, effects: [resumeEffect(state)] };
  }
}
<<<END DRIVER
<<<SLICE DRIVERTESTS
import { describe, it, expect } from "vitest";
import { initialBrainStreamState, openBrainStream, resumeEventId } from "./brainStream";
import { BRAIN_POLL_INTERVAL_MS, stepBrainStream } from "./brainStreamDriver";
import type { BrainStreamEvent } from "./brainStreamDriver";
import type { BrainStreamState } from "./brainStream";

/** Run a script of transport events, collecting every effect in order. */
function runScript(state: BrainStreamState, events: BrainStreamEvent[]) {
  const effects = [];
  let current = state;
  for (const event of events) {
    const step = stepBrainStream(current, event);
    current = step.state;
    effects.push(...step.effects);
  }
  return { state: current, effects };
}

/** The last effect a script produced. `Array.prototype.at` is newer than this
 *  project's TypeScript lib target, so the index is spelled out. */
function lastOf<T>(items: T[]): T {
  return items[items.length - 1];
}

function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } } };
}

describe("a clean stream", () => {
  it("opening asks for nothing and reports live", () => {
    const step = stepBrainStream(initialBrainStreamState(), { kind: "opened" });
    expect(step.effects).toEqual([]);
    expect(step.state.status).toBe("live");
  });
  it("contiguous frames ask for nothing", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "opened" }, frame(0), frame(1), frame(2)]);
    expect(r.effects).toEqual([]);
    expect(r.state.lastSeq).toBe(2);
    expect(r.state.status).toBe("live");
  });
});

describe("a dropped connection", () => {
  it("waits the backoff and then reconnects from the frame it holds", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "opened" }, frame(0), frame(1), { kind: "closed" }]);
    expect(r.effects).toEqual([{ kind: "wait", ms: 250 }]);
    expect(r.state.status).toBe("reconnecting");
    const resumed = stepBrainStream(r.state, { kind: "timer" });
    expect(resumed.effects).toEqual([{ kind: "connect", lastEventId: "1" }]);
  });
  it("repeated drops lengthen the wait", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "closed" }, { kind: "closed" }, { kind: "closed" }]);
    expect(r.effects.map((e) => ("ms" in e ? e.ms : null))).toEqual([250, 500, 1000]);
  });
  it("a successful open resets the wait to the floor", () => {
    const dropped = runScript(initialBrainStreamState(), [{ kind: "closed" }, { kind: "closed" }]);
    const reopened = stepBrainStream(dropped.state, { kind: "opened" });
    const again = stepBrainStream(reopened.state, { kind: "closed" });
    expect(again.effects).toEqual([{ kind: "wait", ms: 250 }]);
  });
  it("a client that holds nothing reconnects with no header", () => {
    const r = runScript(initialBrainStreamState(), [{ kind: "closed" }, { kind: "timer" }]);
    expect(lastOf(r.effects)).toEqual({ kind: "connect", lastEventId: null });
  });
});

describe("a gap in the sequence", () => {
  it("asks for a snapshot exactly once, not once per later frame", () => {
    const r = runScript(openBrainStream(initialBrainStreamState()),
      [frame(0), frame(4), frame(5), frame(6)]);
    expect(r.effects).toEqual([{ kind: "snapshot" }]);
  });
  it("the snapshot heals the hole and resumes from the snapshot position", () => {
    const gapped = runScript(openBrainStream(initialBrainStreamState()), [frame(0), frame(4)]);
    const healed = stepBrainStream(gapped.state, { kind: "snapshot", seq: 9 });
    expect(healed.state.gapDetected).toBe(false);
    expect(healed.effects).toEqual([{ kind: "connect", lastEventId: "9" }]);
    expect(resumeEventId(healed.state)).toBe("9");
  });
  it("a contiguous run never asks for a snapshot", () => {
    const r = runScript(openBrainStream(initialBrainStreamState()), [frame(0), frame(1), frame(2)]);
    expect(r.effects).toEqual([]);
  });
});

describe("the polling fallback", () => {
  it("engages on an unsupported transport and labels itself delayed", () => {
    const step = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    expect(step.state.status).toBe("delayed");
    expect(step.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
  it("keeps polling rather than reconnecting once it has engaged", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const ticked = stepBrainStream(fallen.state, { kind: "timer" });
    expect(ticked.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
  it("never claims live again on frames it polls", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const r = runScript(fallen.state, [frame(0), frame(1)]);
    expect(r.state.status).toBe("delayed");
    expect(r.state.lastSeq).toBe(1);
  });
  it("a poll that drops keeps polling and does not start a backoff", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const dropped = stepBrainStream(fallen.state, { kind: "closed" });
    expect(dropped.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
    expect(dropped.state.attempt).toBe(0);
  });
  it("a gap over the fallback still asks for a snapshot and resumes by polling", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const r = runScript(fallen.state, [frame(0), frame(4)]);
    expect(lastOf(r.effects)).toEqual({ kind: "snapshot" });
    const healed = stepBrainStream(r.state, { kind: "snapshot", seq: 4 });
    expect(healed.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
});
<<<END DRIVERTESTS
