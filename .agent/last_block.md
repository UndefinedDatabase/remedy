── STEP R16/1 — F008 SSE event stream · T003 BEGINS ────────────
Goal:        Build T003's client-side RULES as a pure module, not yet as a
             React hook: the status surface live | reconnecting | delayed, the
             Last-Event-ID resume position, seq gap detection and the reconnect
             backoff schedule. `apps/ui/vitest.config.ts` sets
             `environment: "node"` and collects `src/**/*.test.ts`, and the app
             carries no jsdom and no testing library, so a hook cannot be
             rendered under any gate this repository owns;
             `apps/ui/src/cockpitLogic.ts` states that precedent in its own
             header comment and is the shape this module follows. R16 also
             records the R15 verdict (PASS), resolves R-0620 and R-0621, and
             registers R-0622.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 resolve R-0620 and R-0621, register R-0622 and record the R15
             verdict · C3 the stream module · C4 its tests · C5 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r16.md            (C0a, new)
             - .agent/last_block.md                   (C0b, rewrite)
             - .agent/plan.md                         (C1, rewrite)
             - .agent/live_review.md                  (C2, append)
             - apps/ui/src/api/brainStream.ts         (C3, new)
             - apps/ui/src/api/brainStream.test.ts    (C4, new)
             - .agent/handoff.md                      (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r16.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback. Each of your
    last four rounds caught a real reviewer defect exactly that way; keep
    doing it.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers, trailing newline
    INCLUDED. PLANF008R16 is the ENTIRE content of `.agent/plan.md`.
    BRAINSTREAM and STREAMTESTS are each the ENTIRE content of a file that
    does not yet exist, so neither is a pair and no FROM is searched for.
    LEDGER16 is a newline plus its body, appended after exactly one blank
    line. Every file ends with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5. `.agent/plan.md`
    advances at C1, ahead of the ledger commit (section 3 item 23). C3
    precedes C4 because C4's file imports C3's; committing the test first
    would land a knowingly red commit.
 4. LEDGER16 carries FOUR paragraphs, blank-line separated, applied together
    in C2: `Done: R-0620`, `Done: R-0621`, the R-0622 registration and the
    `Gate: R16` entry holding the R15 verdict. R-0622 is the only id minted,
    so the next free id becomes R-0623. These are the FIRST two `Done:` lines
    this record carries — before C2 it holds none — which is why G6 reads that
    count moving from 0 to 2 rather than staying flat.
 5. SCOPE. No Python changes at all this round. No React component, no hook,
    no `EventSource` construction, no polling loop, no CSS, and no new entry
    in `apps/ui/package.json` — the module is framework-free and imports
    nothing. T003's hook and its polling fallback are R17's work, and any POST
    surface belongs to the next feature. R-0622 is REGISTERED and NOT fixed:
    adding a lint parser is a change to that package's dependency set and
    routes to a paydown branch.
 6. `git status --porcelain` is empty after each of C0a through C4, and
    `git worktree list` names the primary checkout alone once G9's worktree is
    removed. READINGS OF STATE AT OR AFTER C5 GO IN THE ROUND REPORT, NEVER IN
    THE HANDBACK FILE: the tree state after the handback commit cannot be
    recorded inside that commit, and a gate that orders it anyway is finding
    R-0371, now three instances deep. Base bytes reach a tool by
    `git show <sha>:<path>` or a disposable worktree under the gitignored
    `.remedy-wt/`, never by overwrite-and-restore in the primary checkout
    (self_drive_protocol G5).
 7. Two test processes never run at once. G8's counting suites run in the
    PRIMARY checkout: a fresh worktree has no `apps/ui/node_modules`, so both
    its pytest and its vitest readings are untrustworthy in both directions
    (R-0518). Where G9 needs `node_modules` inside a worktree it SYMLINKS the
    primary one — `ln -s`, never a copy, because a copy dereferences npm's bin
    shims and manufactures its own failures (R-0591).
 8. The reviewer's own readings at `22dd8d31`, RE-DERIVED by the gates below
    rather than trusted. In `apps/ui`: `npx vitest run` exits 0 at 4 files and
    71 tests, `npm run --silent typecheck` exits 0 with no output, and
    `npm run --silent lint` EXITS 1 at `49 problems (47 errors, 2 warnings)` —
    that last one is R-0622, is NOT a gate (R-0364), and is not to be repaired
    as a side effect of this round. From the repository root the combined
    state-reader suite including the canary exits 0 at 465 passed-plus-skipped.
    Count by passed-plus-skipped, never by a bare passed count.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. T003 is
    half-built at the end of this round, so the branch is not closeable. It is
    pushed and left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     each of C0a through C4. Report each reading. Per constraint 6 the post-C5
     porcelain and the final `git worktree list` belong to the ROUND REPORT.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block you were given, of `.agent/authored/f008-r16.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r16.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R16. Its line count is under 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — those four are what
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER16 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the C2 file, its terminating newline
     normalised first, has as its LAST FOUR units, in order, the four
     paragraphs of LEDGER16. NEGATIVE CONTROL: flip one byte of the remainder
     and report that BOTH readings reject it, and that both accept the
     unflipped bytes.
 G6  The sets, at C1 and C2. Report line-anchored counts in
     `.agent/live_review.md`: `^- R-\d+ — ` reads 193 then 194,
     `^Done: R-\d+ — ` reads 0 then 2, `^Landed: ` is 0 at both,
     `^Gate: R\d+ — ` reads 15 then 16 with the sixteen keys DISTINCT,
     `^- R-0622 — ` reads 0 then 1 and `^- R-0623 — ` is 0 at both. Report
     that the two `Done:` ids at C2 are exactly R-0620 and R-0621. Report that
     LEDGER16's `Gate:` header matches the shape of the entries already in the
     file, as a pattern match over `^Gate: R(\d+) — the R(\d+) entry\.`
     requiring the second number to be one less than the first and the R16
     pair to occur exactly once (section 3 item 26). Report the number of
     `^Gate: ` lines that do NOT match; it is 1, and that line is
     `Gate: R1 — the F255 R21 entry.`
 G7  The two new files. Report that `apps/ui/src/api/brainStream.ts` and
     `apps/ui/src/api/brainStream.test.ts` are both ABSENT at `22dd8d31`,
     using `git ls-tree 22dd8d31 -- <path>` per path and reporting its empty
     output. Report the sha256, bytes and lines of the C3 blob of the first
     and of the C4 blob of the second, and whether each is BYTE-EQUAL to
     BRAINSTREAM and to STREAMTESTS respectively. Because both files are new,
     the whole of each commit's diff is additions: report that
     `git show --numstat` gives each path its slice's own line count against 0
     deletions.
 G8  The suites are green in the PRIMARY checkout, run SERIALLY, never two
     test processes at once. Report the exit code and the counts of each, at
     C4. In `apps/ui`: `npx vitest run` exits 0 at 5 files and 89 tests, and
     `npm run --silent typecheck` exits 0. From the repository root:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped — that suite is gated because
     `tests/ui_contracts/test_ux_quality.py::test_no_scanlines_in_frontend`
     rglobs every `.ts` under `apps/ui/src` and therefore READS both files
     this round adds. Its passed/skipped SPLIT moves between runs at an
     unchanged tree, so report the SUM and never a bare passed count.
     RECONCILE THE ARITHMETIC RATHER THAN
     ASSERTING A BARE TOTAL: report the number of lines matching `^  it(` in
     STREAMTESTS, and report that 71 plus that number equals the vitest total.
     Report also `npm run --silent lint`: it EXITS 1 at
     `51 problems (49 errors, 2 warnings)`, which is constraint 8's base
     reading plus exactly two errors, one `Parsing error` per new file,
     because eslint reaches both and parses neither. That is R-0622 and NOT a
     regression; report the real numbers either way and repair nothing. If any
     identity fails, report the real values and stop.
 G9  RED CONTROL, the colour and not a count, in a disposable worktree created
     at C4 under `.remedy-wt/`, with the primary checkout never touched and
     `apps/ui/node_modules` reached by the symlink constraint 7 names. Apply
     each of these three mutations to the worktree's copy of
     `apps/ui/src/api/brainStream.ts` SEPARATELY, restoring the file
     byte-exactly between them, and report for each the exit code and the
     NAMES of the failing tests from
     `npx vitest run src/api/brainStream.test.ts`:
     (a) `String(state.lastSeq)` becomes `String(state.lastSeq + 1)`;
     (b) in the `const isGap =` line, the whole right-hand side becomes
     `false`;
     (c) in `brainBackoffDelayMs`, the `Math.min(...)` call becomes its first
     argument alone.
     Report the occurrence count of each byte string you replace in that file
     at C3 BEFORE mutating; each is exactly 1. Each mutation EXITS 1 and each
     names at least one failing test. Report that the restored file EXITS 0,
     and remove the worktree before the handback.
 G10 The range. Report `git diff --name-only 22dd8d31..C4` and that it equals
     the Change list MINUS `.agent/handoff.md` exactly — six paths, none on
     either side alone. The full `22dd8d31..C5` reading belongs to the ROUND
     REPORT (constraint 6). Report that every commit in the range has exactly
     one parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, with every insertion under
     500 and every cell equal to the `+/-` column of your `## Commits` table,
     cell by cell (section 3 item 28).
 G11 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `apps/ui/src/api/brainStream.ts` at C3,
     `apps/ui/src/api/brainStream.test.ts` at C4 and `.agent/handoff.md` at
     C5. Each is 0.
 G12 Report this round's own reflog entries counted by the OPERATION before
     the first `:` in `%gs`: `amend`, `rebase` and `cherry` are each 0. Assert
     no total. An unstage is not a history rewrite (R-0608).
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md and the item-status table, naming C0a,
     C0b, C1, C2, C3, C4 and C5 exactly once each. Measure it with `wc -l`
     BEFORE writing it: this round's seven commits allow 100 lines, and an
     overage needs a DECISION D15 stated-cause line naming the real count.

Handback:    completion report + rewrite `.agent/handoff.md`. Its state block
             repeats this Fortschritt line verbatim:
             `~72 % (T001 ✅ · T002 ✅ · T003 angefangen) — Schätzung`.
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R16
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
R16 BEGINS T003 with the client-side RULES alone, as a pure module rather than
as a React hook. `apps/ui/vitest.config.ts` sets `environment: "node"` and
collects `src/**/*.test.ts`, and the app carries no jsdom and no testing
library, so nothing here can render a hook; `apps/ui/src/cockpitLogic.ts`
states that same precedent in its own header comment. A new pure module beside
the existing API client therefore holds the status surface live |
reconnecting | delayed, the Last-Event-ID resume position, seq gap detection
and the reconnect backoff schedule, with a test file pinning each. R16 also
records the R15 verdict, resolves R-0620 and R-0621, and registers R-0622.

## Next Steps
1. R17 wraps that module in the React `useBrainStream` hook, adds T003's
   polling fallback on the same interface and the fixture live-job
   end-to-end.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `22dd8d31` it exits 1 with 49 problems, and every error is a
  `Parsing error` because that eslint configuration parses no TypeScript at
  all. That defect is R-0622 and routes to a paydown branch. `npm run
  typecheck` and `npx vitest run` both exit 0 at that same commit and ARE the
  gates this round runs.
- Repository-wide `ruff check .` is RED and is not a gate (R-0364). This round
  changes no Python, so it moves that reading in neither direction.
- No open finding is a code defect of F008 reachable from the HTTP path. The
  open set lives in `.agent/live_review.md` and this file does not repeat it;
  R-0620 and R-0621 leave it this round and R-0622 enters it.
<<<END PLANF008R16
<<<SLICE LEDGER16
Done: R-0620 — RESOLVED at `8a80ffce` by exactly the one-line fix the finding's own body prescribed: `resolve_sse_start` now opens `text = "" if last_event_id is None else str(last_event_id).strip()`, so only a MISSING header falls back to the cursor and the integer 0 is read as the position it is. THE REVIEWER RE-DERIVED IT rather than reading it back: applying the R15 block's FIXFROM/FIXTO pair to the `305bc30c` blob of `packages/orchestration/ui_server.py`, the FROM occurring exactly once, yields a file BYTE-EQUAL to the C4 blob at sha256 dbf7b3b4, and three new cases pin `(0, "7")` to 1, `(4, "7")` to 5 and `(None, "7")` to 7. THE RED PROOF IS THE COLOUR AND NOT A COUNT, re-run by the reviewer in its own disposable worktree at `1dc011a2` with the primary checkout never touched and `mod.__file__` proved to resolve inside that worktree: with the `305bc30c` blob of that file written back in and the tests left at `1dc011a2`, `pytest tests/ui_server/test_sse_stream.py -k ResumeStartTypes` EXITS 1 and `test_an_integer_zero_is_a_position_and_not_an_absence` fails on `assert 7 == 1`, while `test_an_integer_header_resumes_one_past_it` and `test_none_is_the_only_absence` SURVIVE — the finding's own claim that only the falsy position was ever broken, demonstrated rather than asserted; restored, the same command EXITS 0 at 3 passed. It stays LOW on resolution for the reason it was registered Low: the sole production caller passes `self.headers.get(SSE_LAST_EVENT_ID_HEADER)`, whose value is a string or `None`, so nothing reachable over the wire behaved wrongly on any day. What the fix buys is that the annotation, the docstring and the behaviour now agree, which is what makes the T003 client a safe next caller.

Done: R-0621 — RESOLVED at `75f02ef3` by widening the hammer helper rather than by renaming the test to match what it did. `_hammer` gains a `last_event_id` parameter so a caller can hand it a client that ALREADY holds part of the ledger, and the test — now `test_a_resume_crosses_a_ledger_that_grew_between_connections` — seeds the second client with the id the first one kept and asserts it receives exactly ids 2 through 9, no duplicate of 1 and no gap at 6, with the two transcripts concatenated byte-equal to the whole ledger. THE REVIEWER PROVED THE REPAIR HAS TEETH rather than trusting that it does: in a disposable worktree at `1dc011a2`, dropping the `+ 1` from `resolve_sse_start` — a byte string occurring exactly once in `packages/orchestration/ui_server.py` — drives `pytest tests/ui_server/test_sse_stream.py -k DisconnectHammer` to EXIT 1 with four failures INCLUDING this repaired test, and the restored file EXITS 0 at 5 passed. That is the reading the finding needed, because the defect it names is a test that passes for the wrong reason: a rename alone would have left the same hole under a truer name. NOTE FOR THE RECORD, not a new finding: the R15 round fixed both this and R-0620 without writing a `Landed:` line for either, so between `75f02ef3` and this paragraph the ledger showed two findings as open whose fixes were already on disk. Section 4 item 4 of `docs/agents/planner_reviewer_prompt.md` reserves that marker for a fix the reviewer has not yet resolved, and these two were reviewer-ORDERED in the block that fixed them, so the window was one round wide and closed by this commit; it is recorded here so the next reader knows the absence was reasoned about rather than overlooked.

- R-0622 — Medium — A LINT CONFIGURATION THAT PARSES NONE OF THE LANGUAGE IT IS AIMED AT, SO THE RULES IT EXISTS TO ENFORCE EVALUATE ON ZERO FILES. `apps/ui/package.json` carries `"lint": "eslint src --ext .ts,.tsx"`, and `apps/ui/eslint.config.js` selects `src/**/*.{ts,tsx}` and enables the `react-hooks` recommended rule set — but it sets no `languageOptions.parser`, and `typescript-eslint` appears in neither the dependencies nor the devDependencies of that package. ESLint therefore parses every TypeScript file with its default JavaScript parser and stops at the first type annotation. MEASURED BY THE REVIEWER at `22dd8d31`, not inferred: `npm run --silent lint` in `apps/ui` EXITS 1 reporting `49 problems (47 errors, 2 warnings)`, and every one of those errors is the `Parsing error` class — `npx eslint src/cockpitLogic.ts src/api/remedyApi.test.ts` returns exactly two problems, `Parsing error: Unexpected token {` and `Parsing error: Unexpected token :`, one per file, which is the same result every `.ts` file in this app produces. WHY MEDIUM RATHER THAN LOW, and why it is registered in THIS feature: the rule set that never evaluates is `react-hooks`, and R17 adds the `useBrainStream` hook — `react-hooks/exhaustive-deps` is precisely the rule that catches the stale-closure bug a reconnecting EventSource hook is prone to, and it will be as silent on that file as it is on every other. It is not vacuous in the R-0438 sense, because it exits 1 loudly rather than passing while blind; the cost is that the loudness is uniform and uninformative, so no one can tell a real finding from the parse failure. THE FIX, out of this feature's scope and routed to a paydown branch: add `typescript-eslint` to `apps/ui` devDependencies and give the `src/**/*.{ts,tsx}` block its parser, then re-measure the problem set and fix or scope whatever real findings appear underneath. F008 must not carry it, because changing that package's dependency set is neither a stream endpoint nor a client rule, and this round gates `npm run typecheck` and `npx vitest run` — both exit 0 at `22dd8d31` — instead of pretending a red lint is a gate (R-0364).

Gate: R16 — the R15 entry. R15 PASSED. No finding is registered against its work: every gate it reported was RE-DERIVED by the reviewer off disk rather than read back out of the handback, and every value matched. TRANSPORT PROVED BY THE DIGEST FALLBACK, declared as such because this is a new session and the previous reviewer's scratch original no longer exists (section 4 item 9): `.agent/authored/f008-r15.md` at `68915bd9` and `.agent/last_block.md` at `ea466d98` are EQUAL at sha256 68062e589fe762d605ce977b0922dd141fc45be26210975e82cd2c7bc4fca5ef over 36909 bytes and 377 lines, which is the value the handback names. ELEVEN SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching: PLANF008R15 da4f29b2, R0371FROM d999949c, R0371TO 844b7e06, LEDGER15 83183124, FIXFROM 025c3c5d, FIXTO 55cc7e7a, HAMMERFROM 5c201fcf, HAMMERTO 0f4f0ec4, GROWFROM a83d4938, GROWTO 1dbb14fe and TESTS15 ca994615. THE PLAN LANDED FIRST at `9980764c`, byte-equal to PLANF008R15 at 46 lines under the 50-line cap, which is checklist item 23 met rather than claimed. THE R-0371 WIDENING IS CONSTRUCTIVE: R0371FROM occurs exactly once at `9980764c` and replacing that one occurrence with R0371TO yields a file byte-equal to the `03ecfea1` blob at 042e3f65, the line count being 1030 at both because a one-line slice replaced a one-line slice. THE APPEND at `42347aaf` is a byte-exact prefix plus a 5926-byte remainder equal to a newline plus LEDGER15, agreed by an INDEPENDENT blank-line split into 212 units whose LAST TWO are LEDGER15's paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped ACCEPTED by both. THE SETS MOVED AS ORDERED — 192, 192, 193 registered, `Done:` and `Landed:` 0 at all three, `Gate: R` 14, 14, 15 over fifteen DISTINCT keys, R-0621 nowhere then once, R-0622 nowhere — so the edit minted nothing and only the append did, and the fifteenth `Gate:` header matched the `Gate: R<n> — the R<n-1> entry.` shape with exactly one non-match, that being the F255 entry which is correctly shaped for what it records. BOTH CODE PAIRS ARE CONSTRUCTIVE: each FROM occurs exactly once in its `305bc30c` blob and the rebuilt files are byte-equal to the C4 and C5 blobs at dbf7b3b4 and 68e9b29b. THE TEST APPEND at `1dc011a2` is a byte-exact prefix whose remainder is TWO newlines plus TESTS15 at 642 bytes and NOT one. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: the SSE file exits 0 at 65, the state readers including the canary exit 0 at 465 and `tests/docs/` exits 0 at 295, reconciling 62 plus 3 and 462 plus 3 exactly against TESTS15's three `def test_` lines. RUFF EQUAL ACROSS THE CHANGE as a rule-code multiset read through `--stdin-filename` with nothing written to the checkout: `{}` against `{}` in the default configuration and `{E306: 3}` against `{E306: 3}` under `--preview`, the three being pre-existing and neither added nor removed, behind a control the reviewer re-ran in BOTH configurations after its own first extractor came back blind on the bare-code form — the same trap the handback declared, reproduced and avoided. NINE single-parent commits, insertions 377, 261, 20, 1, 4, 1, 16, 16 and 50, every one under 500 and every cell equal to the handback's `+/-` column including the deletions; zero marker lines in all five targets; a reflog whose operations are `commit` 40 times with amend, rebase and cherry at 0; an 89-line handback under the 100 lines nine commits allow; the tree clean with the primary checkout the only worktree and the branch pushed at `22dd8d31`.
<<<END LEDGER16
<<<SLICE BRAINSTREAM
// Pure, framework-free client state for the SSE brain stream.
// Extracted from the React hook for the same reason cockpitLogic.ts was
// extracted from the panels: the node-environment vitest cannot render React,
// so the reconnect, gap and status rules live here where they can be tested.

/** What the cockpit badge shows: a live stream, a retrying one, or polling. */
export type BrainStreamStatus = "live" | "reconnecting" | "delayed";

/** One frame as the server sends it: the ledger position IS the event id. */
export interface BrainStreamFrame {
  seq: number;
  event: unknown;
}

export interface BrainStreamState {
  status: BrainStreamStatus;
  /** The last seq the client actually HOLDS; null before the first frame. */
  lastSeq: number | null;
  /** A seq discontinuity was seen and no snapshot has repaired it yet. */
  gapDetected: boolean;
  /** Consecutive failed connection attempts; reset by a successful open. */
  attempt: number;
}

/** A client that holds nothing yet, and does not pretend to be live. */
export function initialBrainStreamState(): BrainStreamState {
  return { status: "reconnecting", lastSeq: null, gapDetected: false, attempt: 0 };
}

/** The `Last-Event-ID` value: the last frame HELD, never the next one wanted.
 *  The server adds the one — `resolve_sse_start` returns `int(text) + 1` — so
 *  a client sending its next-wanted seq would skip an event on every
 *  reconnect. Null means "send no header", which resumes from the cursor. */
export function resumeEventId(state: BrainStreamState): string | null {
  return state.lastSeq === null ? null : String(state.lastSeq);
}

/** An open connection is the only thing that makes the badge say live. */
export function openBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "live", attempt: 0 };
}

/** A dropped connection counts an attempt; the badge stops claiming live. */
export function failBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "reconnecting", attempt: state.attempt + 1 };
}

/** The fallback transport is honest about being slower than the stream. */
export function degradeBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "delayed" };
}

/** Applying a frame advances the held position and reports a discontinuity.
 *  A gap is `seq !== lastSeq + 1` — the disconnect hammer forbids both the
 *  duplicate and the hole, and the client must SEE the hole to ask for a
 *  snapshot. The first frame of a fresh client can carry any seq, because a
 *  resume from a cursor starts mid-ledger, so it never reports a gap. A frame
 *  at or behind the held position is a replay and is dropped. */
export function receiveBrainFrame(
  state: BrainStreamState,
  frame: BrainStreamFrame,
): BrainStreamState {
  if (state.lastSeq !== null && frame.seq <= state.lastSeq) return state;
  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;
  return {
    ...state,
    status: state.status === "delayed" ? "delayed" : "live",
    lastSeq: frame.seq,
    gapDetected: state.gapDetected || isGap,
    attempt: 0,
  };
}

/** A snapshot refetch is what repairs a gap: the held position jumps to the
 *  snapshot's own seq and the discontinuity is cleared. */
export function repairBrainGap(
  state: BrainStreamState,
  snapshotSeq: number,
): BrainStreamState {
  return { ...state, lastSeq: snapshotSeq, gapDetected: false };
}

/** Backoff floor and ceiling, named so the schedule and its tests cannot drift. */
export const BRAIN_BACKOFF_BASE_MS = 250;
export const BRAIN_BACKOFF_CAP_MS = 8000;

/** Reconnect backoff: doubling from the base, capped so a long outage still
 *  retries about every eight seconds rather than drifting into minutes. */
export function brainBackoffDelayMs(attempt: number): number {
  if (attempt <= 0) return 0;
  return Math.min(BRAIN_BACKOFF_BASE_MS * 2 ** (attempt - 1), BRAIN_BACKOFF_CAP_MS);
}
<<<END BRAINSTREAM
<<<SLICE STREAMTESTS
import { describe, it, expect } from "vitest";
import {
  BRAIN_BACKOFF_CAP_MS, brainBackoffDelayMs, degradeBrainStream, failBrainStream,
  initialBrainStreamState, openBrainStream, receiveBrainFrame, repairBrainGap, resumeEventId,
} from "./brainStream";
import type { BrainStreamState } from "./brainStream";

/** Drive a state through a run of seqs, as the transport would deliver them. */
function drive(state: BrainStreamState, seqs: number[]): BrainStreamState {
  return seqs.reduce((s, seq) => receiveBrainFrame(s, { seq, event: { seq } }), state);
}

describe("initialBrainStreamState", () => {
  it("holds nothing and does not claim to be live", () => {
    const s = initialBrainStreamState();
    expect(s.lastSeq).toBeNull();
    expect(s.status).toBe("reconnecting");
    expect(s.gapDetected).toBe(false);
  });
});

describe("resumeEventId", () => {
  it("sends no header before the first frame", () => {
    expect(resumeEventId(initialBrainStreamState())).toBeNull();
  });
  it("sends the last seq HELD, not the next one wanted", () => {
    // The server adds the one, so a next-wanted seq would skip an event.
    expect(resumeEventId(drive(initialBrainStreamState(), [0, 1, 2]))).toBe("2");
  });
  it("zero is a position and is still sent", () => {
    // The client half of the server-side rule that zero is not an absence.
    expect(resumeEventId(drive(initialBrainStreamState(), [0]))).toBe("0");
  });
});

describe("receiveBrainFrame", () => {
  it("a contiguous run reports no gap and ends live", () => {
    const s = drive(openBrainStream(initialBrainStreamState()), [0, 1, 2, 3]);
    expect(s.lastSeq).toBe(3);
    expect(s.gapDetected).toBe(false);
    expect(s.status).toBe("live");
  });
  it("the first frame of a fresh client is never a gap", () => {
    // A resume from a cursor starts mid-ledger; that is not a discontinuity.
    expect(drive(initialBrainStreamState(), [7]).gapDetected).toBe(false);
  });
  it("a hole in the sequence is detected", () => {
    expect(drive(initialBrainStreamState(), [0, 1, 4]).gapDetected).toBe(true);
  });
  it("a replayed frame is dropped and does not move the held position", () => {
    const s = drive(initialBrainStreamState(), [0, 1, 1]);
    expect(s.lastSeq).toBe(1);
    expect(s.gapDetected).toBe(false);
  });
  it("a detected gap stays set while later frames arrive cleanly", () => {
    expect(drive(initialBrainStreamState(), [0, 3, 4, 5]).gapDetected).toBe(true);
  });
  it("frames over the fallback stay labelled delayed", () => {
    const s = drive(degradeBrainStream(initialBrainStreamState()), [0, 1]);
    expect(s.status).toBe("delayed");
    expect(s.lastSeq).toBe(1);
  });
});

describe("repairBrainGap", () => {
  it("a snapshot clears the discontinuity and sets the held position", () => {
    const fixed = repairBrainGap(drive(initialBrainStreamState(), [0, 4]), 9);
    expect(fixed.gapDetected).toBe(false);
    expect(fixed.lastSeq).toBe(9);
    expect(resumeEventId(fixed)).toBe("9");
  });
});

describe("the status surface", () => {
  it("moves through live, reconnecting and delayed and back to live", () => {
    let s = openBrainStream(initialBrainStreamState());
    expect(s.status).toBe("live");
    s = failBrainStream(s);
    expect(s.status).toBe("reconnecting");
    s = degradeBrainStream(s);
    expect(s.status).toBe("delayed");
    s = openBrainStream(s);
    expect(s.status).toBe("live");
  });
  it("a successful open resets the attempt count", () => {
    const s = openBrainStream(failBrainStream(failBrainStream(initialBrainStreamState())));
    expect(s.attempt).toBe(0);
  });
  it("each drop counts one attempt", () => {
    expect(failBrainStream(failBrainStream(initialBrainStreamState())).attempt).toBe(2);
  });
});

describe("brainBackoffDelayMs", () => {
  it("the first attempt does not wait", () => {
    expect(brainBackoffDelayMs(0)).toBe(0);
  });
  it("doubles from the base delay", () => {
    expect([1, 2, 3, 4].map((n) => brainBackoffDelayMs(n))).toEqual([250, 500, 1000, 2000]);
  });
  it("is capped so a long outage keeps retrying", () => {
    expect(brainBackoffDelayMs(20)).toBe(BRAIN_BACKOFF_CAP_MS);
  });
  it("never decreases as attempts grow", () => {
    const d = [0, 1, 2, 3, 4, 5, 6, 7, 8].map((n) => brainBackoffDelayMs(n));
    expect(d).toEqual([...d].sort((a, b) => a - b));
  });
});
<<<END STREAMTESTS
