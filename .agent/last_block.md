── STEP T003/4 — F008 SSE event stream — ROUND 20 ────────────────────────────
Goal:
 Make the driver the SINGLE AUTHORITY on what the client does next, and write
 the record R19 left open. `start()` stops calling `host.connect` itself and
 dispatches the opening event instead, so `perform` issues the effect the
 driver chose — R-0627's fix. This is NOT a pure refactor and the block does
 not claim it is: after the fallback has engaged, a restart now POLLS where it
 used to reopen a stream, which is the defect's whole point, so a new test
 pins that behaviour. R19's verdict and R-0626's resolution land with it.

Bundle, in this commit order:
 C0a  save this block verbatim to `.agent/authored/f008-r20.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R20, applied whole
 C2   `.agent/live_review.md` <- LEDGER20, appended
 C3   `apps/ui/src/api/brainStreamRunner.ts` <- IMPORTFROM->IMPORTTO,
      STARTFROM->STARTTO and COMMENTFROM->COMMENTTO, all three pairs
 C4   `apps/ui/src/api/brainStreamRunner.test.ts` <- RESTARTTEST, appended
 C5   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r20.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamRunner.ts`,
 `apps/ui/src/api/brainStreamRunner.test.ts`, `.agent/handoff.md`.

Slice convention:
 The authored units below are PLANF008R20, LEDGER20, IMPORTFROM, IMPORTTO,
 COMMENTFROM, COMMENTTO, STARTFROM, STARTTO, STARTOLD and RESTARTTEST — ten,
 each delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of the slice. Every slice is
 newline-terminated with no trailing whitespace on any line. Three of them are
 FROM/TO pairs. MEASURED by the reviewer's script, not asserted: each pair
 prints `TO contains FROM: false`, so all three are REWRITES and G7 orders the
 FROM-zero counts that only a rewrite can satisfy.
 STARTOLD IS NOT APPLIED TO ANY FILE. It is G10's mutation text and exists only
 inside the disposable worktree; a commit containing it is a defect. Nine
 slices are applied, one is a red-control input.

Why C3 carries THREE pairs and not one:
 `apps/ui/tsconfig.json` sets `noUnusedLocals: true`, and line 97 is the ONLY
 use of the `resumeEventId` import in this module — the reviewer grepped it:
 the identifier occurs on lines 5 and 97 and nowhere else. Dropping the call
 without IMPORTFROM would therefore turn `npm run typecheck` RED, so the import
 line is part of the same indivisible edit. COMMENTFROM retires a sentence that
 became false when R19 shipped no hook: the comment promises "R19's hook", and
 the hook is now R21's work.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, apply it as written and say
    so in the handback's deviations section — do not fix it.
 2. The commit order above is fixed: no extra commit, no dropped commit, no
    reordering. C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. No dependency is added and no
    file is created. In particular DO NOT add jsdom, happy-dom or a testing
    library: neither is installed, the hook that would need one is R21's work,
    and a dependency decision is not smuggled in beside a refactor.
 4. C3 and C4 are separate commits and stay separate: AGENTS.md forbids mixing
    a refactor with the test that pins it. At C3 the runner suite still holds
    11 tests; the twelfth arrives at C4.
 5. R-0627 is FIXED here but gets NO `Done:` paragraph: only reviewer-authored
    text sets a resolution (§4 item 4) and R21 owes that paragraph, exactly as
    R19 left R-0626's resolution to this round. Write no `Landed:` line either
    — LEDGER20 already covers the round. No finding id is minted this round:
    R-0628 stays free.
 6. R-0622 stays OPEN — do not add a TypeScript parser to make lint green.
 7. The post-C5 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md`: C5 cannot state
    facts about itself (R-0371).
 8. Two test processes never run at once. G8's counting suites run in the
    PRIMARY checkout: a fresh worktree has no `apps/ui/node_modules`, so its
    counts are untrustworthy both ways (R-0518). Where G9 needs `node_modules`
    in a worktree it SYMLINKS the primary one — never a copy, which dereferences
    npm's bin shims and manufactures failures (R-0591); the session guard
    rejects `ln` by form, so use `os.symlink`. `npx` inside a worktree can turn
    that symlink into a real directory: if it does, REMOVE the directory rather
    than unlinking it, and never touch the primary checkout's `node_modules`.
 9. The reviewer's OWN base readings, each produced by RUNNING the tool at
    `1f10de78` before this block was written rather than recalled (the R-0625
    counter-measure). In `apps/ui`: `npx vitest run` exits 0 at 7 files and 114
    tests; `npm run --silent typecheck` exits 0 with no output;
    `npm run --silent lint` EXITS 1 at `55 problems (53 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here. From the
    root the state readers plus canary exit 0 at 465 and `tests/ui_contracts/`
    at 397, both passed-plus-skipped — that split moves run to run at an
    unchanged tree, so a bare passed count is never a gate.
 10. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it and leave it
    open. `gh pr list --state open` returned `[]` at the R20 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after each
     of C0a, C0b, C1, C2, C3 and C4. Report each reading; per constraint 7 the
     post-C5 readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of the scratch block you
     were given, of `.agent/authored/f008-r20.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r20.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines, and that no slice carries trailing whitespace on any line.
     Expected, all ten: PLANF008R20 833e3762 at 49 lines, LEDGER20 0321b69d,
     IMPORTFROM 601f32f9, IMPORTTO 850c11a7, COMMENTFROM 2e897c87,
     COMMENTTO d454a7f0, STARTFROM f2dbae03, STARTTO d59f9ccd,
     STARTOLD 79858850, RESTARTTEST feed12b4.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R20. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER20 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
     normalised first, has as its LAST TWO units, in order, LEDGER20's two
     paragraphs. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another ASCII byte and report that BOTH readings reject it and both accept
     the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 199 at BOTH — no finding is minted this round —
     `^Done: R-\d+ — ` 4 then 5, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 19
     then 20 over that many DISTINCT keys, `^- R-0628 — ` 0 at both. Report the
     `Done:` ids at C2 — R-0620, R-0621, R-0623, R-0624 and R-0626, no others.
     HEADER SWEEP at C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match, and that the R20 pair
     occurs EXACTLY ONCE.
 G7  The three pairs, CONSTRUCTIVELY, in `apps/ui/src/api/brainStreamRunner.ts`
     between the `1f10de78` blob and C3. For EACH of IMPORTFROM/IMPORTTO,
     STARTFROM/STARTTO and COMMENTFROM/COMMENTTO report: the FROM occurs
     EXACTLY ONCE at `1f10de78` and 0 times at C3, and the TO 0 times at
     `1f10de78` and exactly once at C3. Then apply ALL THREE replacements to the
     `1f10de78` blob in one pass and report that the result is BYTE-EQUAL to the
     C3 blob — report both sha256 values and whether they match. The reviewer
     built that value in a throwaway worktree and it is
     3b823c0e7e1d16e518f9545f9ece5b0ca1f0130de8f2131d5b48991797ab4626 over 3895
     bytes; the base blob is fefd47e6 over 3915. Report also
     the count of `host.connect(` in that file, which reads 2 at `1f10de78` and
     1 at C3 — that ONE remaining call is inside `perform`, and it is the whole
     property R-0627 asks for. Report the count of `resumeEventId`, which reads
     2 then 0, the import going with the call. `git show --numstat` for that
     path at C3 is 3/3, NOT 4/4: COMMENTFROM and COMMENTTO share their first
     line, so three pairs change three lines. The file's line count is
     UNCHANGED at 107.
 G8  The test append, C4 against C3. Report that the C3 blob of
     `apps/ui/src/api/brainStreamRunner.test.ts` is a byte-exact PREFIX of the
     C4 blob and that the remainder equals a newline plus RESTARTTEST — report
     its sha256, bytes and lines, which the reviewer measured at 5bb52e85 over
     638 bytes and 15 lines. Report `^  it(` line-anchored in that file: 11
     at C3 and 12 at C4, and `^describe(` 5 then 6. `git show --numstat` at C4
     is 15/0 — fifteen inserted lines, ZERO deletions, an append touching no
     existing line.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY. Report the
     exit code and counts of each. In `apps/ui` AT C4: `npx vitest run` exits 0
     at 7 files and 115 tests — 114 at the base plus RESTARTTEST's single `it`,
     and the arithmetic is the point: any other total means something moved that
     this round did not order. `npm run --silent typecheck` exits 0 with NO
     output, which is the reading IMPORTFROM exists to protect. From the
     repository root AT C4:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. Report also `npm run --silent lint` at C4: it EXITS 1
     at `55 problems (53 errors, 2 warnings)`, UNCHANGED from constraint 9's
     base reading because this round adds no file. If any of these fails,
     report the real values and STOP.
 G10 RED CONTROLS — the colour, never a count — in ONE disposable worktree
     created at C4 under the gitignored `.remedy-wt/`, the primary checkout
     NEVER touched and `apps/ui/node_modules` reached by the symlink constraint
     8 names. Run BOTH, restoring byte-exactly between them, each verified by
     sha256, and report each mutated string occurs EXACTLY ONCE before it is
     mutated:
     (a) THE FIX IS LOAD-BEARING AND THE NEW TEST IS WHAT CATCHES IT. In
         `brainStreamRunner.ts` replace the whole STARTTO slice with the whole
         STARTOLD slice and report the exit code and the NAMES of the failing
         tests from `npx vitest run src/api/brainStreamRunner.test.ts`. It
         EXITS 1 and names EXACTLY ONE test, RESTARTTEST's
         `restarting after the fallback engaged > polls on the driver's
         authority instead of reopening a stream`. That single name is the
         reading that matters: the other eleven stay GREEN, which is what
         proves the round changed the ONE behaviour it declared and no other.
         WHY STARTOLD AND NOT STARTFROM — the reviewer measured both. Restoring
         STARTFROM reintroduces `resumeEventId`, whose import IMPORTTO removed,
         so the module fails to resolve and ALL TWELVE tests go red on a load
         error that says nothing about behaviour. STARTOLD is the pre-R20
         behaviour written without that identifier: every existing test starts
         a runner whose `lastSeq` is null, where the old `resumeEventId(state)`
         evaluated to exactly `null`, so STARTOLD is behaviourally identical to
         the old code everywhere the suite reaches. Do NOT mutate the bare
         string `dispatch({ kind: "timer" });` either — the reviewer measured
         it at THREE occurrences in this file, so it is not a targeted control.
     (b) THE NEW TEST'S POLL ASSERTION IS LIVE. Restore, then in
         `brainStreamRunner.ts` replace `case "poll":` with
         `case "poll": if (false)` and report the exit code and failing names.
         It EXITS 1 and RESTARTTEST's test is among them. Restore byte-exactly.
     After BOTH, report that the restored file's sha256 equals the C4 blob's and
     that `npx vitest run src/api/brainStreamRunner.test.ts` EXITS 0 at 12
     passed. REMOVE the worktree before writing C5.
 G11 The range. Report `git diff --name-only 1f10de78..C4` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — six paths, none on
     either side alone. The full `1f10de78..C5` reading belongs to the ROUND
     REPORT (constraint 7, R-0371). Report that every commit in the range has
     exactly ONE parent, and BOTH numstat cells per path from
     `git show --numstat`, cross-checked against `git diff --numstat`, every
     insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (§3 item 28).
 G12 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2, the runner at C3,
     the runner test at C4 and `.agent/handoff.md` at C5. Each is 0.
 G13 Reflog. Count THIS round's own entries by the OPERATION before the first
     `:` in `%gs`. All six pre-C5 entries are `commit`; report `amend`,
     `rebase` and `cherry` at 0, and assert no total.
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2, C3, C4 and C5 — "exactly one row"
     scoping to that TABLE, not to the whole file. Measure its line count with
     `wc -l` BEFORE committing it; this round has seven commits, so the cap is
     100 lines, and an overage carries a DECISION D15 stated-cause line naming
     the real count and the mandated content that caused it. One line per gate
     here; the raw transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~87 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R20
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
R20 makes the driver the single authority on what the client does next and
writes the record R19 left open. `start()` stops calling `host.connect`
itself and dispatches the opening event, so `perform` issues the effect the
driver chose — R-0627's fix. It is not a pure refactor: after the fallback has
engaged a restart now polls where it used to reopen a stream, so a new test
pins that. The round also writes the R19 verdict and resolves R-0626, whose
rename of the driver's gap local landed at `c1051495`.

## Next Steps
1. R21 adds the thin React `useBrainStream` hook over the runner and the
   visible delayed badge. Neither jsdom nor a testing library is installed, so
   R21 opens with that dependency decision and owns it.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `1f10de78` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622 and it routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 there and ARE the gates. Repository-wide
  `ruff check .` is RED too and is not a gate; this round changes no Python.
- `noUnusedLocals` is on, so dropping the `resumeEventId` call orphans its
  import and turns typecheck red. R20 carries the import line for that reason:
  one indivisible edit, not scope drift.
- R21 is the round where a gate this repository owns stops covering the code:
  no React component can be rendered here today. The runner is framework-free
  so the hook has almost no branch left to get wrong, but the BADGE is a
  visual surface and docs/ui/design_reference/ is binding for it, any
  deviation owed an assumption_log entry with a technical reason.
- R-0627's fix lands here and its `Done:` paragraph is owed by R21, exactly as
  R19 left R-0626's resolution to this round.
<<<END PLANF008R20

<<<SLICE LEDGER20
Done: R-0626 — RESOLVED at `c1051495` by renaming the driver's `frame`-case local from `opened` to `gapOpened`, so the module no longer spells two live concepts one way inside one `switch`: `case "opened":` keeps the transport meaning A CONNECTION OPENED and the local now says A GAP OPENED, which is the two-to-four-word domain name AGENTS.md's Code Discoverability Conventions ask for. RE-MEASURED BY THE REVIEWER at the R20 gate rather than read back out of the handback: the pair is a strict rewrite — `TO contains FROM: false` — so replacing the single `1f10de78`-parent occurrence constructively reproduces the C3 blob byte for byte at sha256 6ad92c6ed57b0bfbace61d4a50015172fd33136b21451442924a4bac817b62cc, the bare identifier `opened` reads 2 then 0, `gapOpened` 0 then 2, the quoted `"opened"` 2 at BOTH because the transport event kind is deliberately NOT renamed, and the file is 92 lines at both revisions. THE RENAME LEFT THE BRANCH LIVE, not merely compiling: in a disposable worktree with `node_modules` symlinked, `effects: gapOpened ?` occurs exactly once and replacing it with `effects: false ?` EXITS 1 naming `a gap in the sequence > asks for a snapshot exactly once, not once per later frame` and `the polling fallback > a gap over the fallback still asks for a snapshot and resumes by polling` from the driver's own tests and `a gap in the sequence > asks the host for a snapshot exactly once` from the runner's — at least one from EACH file — with the file restored byte-exactly and the same run then EXITING 0 at 25 passed. A name defect is cheap to fix and expensive to leave: this one sat two `case` labels apart from the word it collided with.

Gate: R20 — the R19 entry. R19 PASSED and no finding is registered against its work — the second consecutive round on this branch for which that is true. EVERY GATE WAS RE-RUN BY THE REVIEWER, never read back out of the handback. TRANSPORT PROVED PRIMARY: the reviewer authored the R19 block in the same session, so `.remedy-wt/f008-r19.md` still existed at review time and was compared disk-to-disk against `.agent/authored/f008-r19.md` at `3fa93165` and `.agent/last_block.md` at `2bb7c786` — all three EQUAL at sha256 24707cae04dd47d149ae9d5f7a4b0d2bba46d8870b527c341c5ba0175304b6e0 over 21673 bytes and 235 lines. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching and none carrying trailing whitespace: PLANF008R19 52a03f9d, LEDGER19 35597ada, OPENEDFROM b1ede53e and OPENEDTO fcf7e651. THE PLAN LANDED FIRST at `b0770e34`, byte-equal at 48 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `055b203a` is a byte-exact prefix of the `b0770e34` blob plus a 6890-byte remainder equal to a newline plus LEDGER19, agreed by an INDEPENDENT blank-line split of the whole file into 226 units whose LAST THREE are LEDGER19's paragraphs in order, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS MOVED AS ORDERED — 198 to 199 registered, `Done:` 3 to 4 over exactly R-0620, R-0621, R-0623 and R-0624, `Landed:` 0 at both, `Gate: R` 18 to 19 over that many DISTINCT keys, R-0627 0 then 1 and R-0628 0 at both — so R-0624's resolution landed and only the one ordered id was minted; eighteen of the nineteen headers match the `Gate: R<n> — the R<n-1> entry.` shape and the single non-match is the F255 entry, correctly shaped for what it records. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 7 files and 114 tests, `npm run --silent typecheck` exits 0 silently, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 397 — every one identical to the base, which for a rename is the property under test. LINT IS RED AND DECLARED, never repaired: 55 problems, 53 errors, 2 warnings, unchanged because the round adds no file, which is R-0622. SIX single-parent commits, insertions 235, 134, 19, 6, 2 and 37, every one under 500 and every cell equal to the handback's `+/-` column including the deletions; zero lines beginning with a slice marker in all four targets; this round's six reflog operations all `commit`, with amend, rebase and cherry at 0; a 77-line handback within the 100 that six commits allow, its item-status table naming C0a through C4 exactly once each; the tree clean and the primary checkout the only worktree, G9's disposable one removed. ONE CORRECTION TO THE REVIEWER'S OWN R-0627 TEXT, made here rather than left to be discovered: that finding says "no behaviour is wrong" and that "the existing tests keep their assertions unchanged". The second clause holds and R20's gate proves it. The FIRST is too strong — `start()` today reopens a stream unconditionally, while the driver would return a `poll` effect once the fallback has engaged, so the fix R20 lands CHANGES what a restart does in that state. No test covered it because nothing calls `start()` twice, which is exactly why R20 adds one.
<<<END LEDGER20

<<<SLICE IMPORTFROM
import { initialBrainStreamState, resumeEventId } from "./brainStream";
<<<END IMPORTFROM

<<<SLICE IMPORTTO
import { initialBrainStreamState } from "./brainStream";
<<<END IMPORTTO

<<<SLICE COMMENTFROM
/** Remedy deliberately gives this no change callback yet: nothing subscribes
 *  until R19's hook exists, and a listener with no reader is untestable. */
<<<END COMMENTFROM

<<<SLICE COMMENTTO
/** Remedy deliberately gives this no change callback yet: nothing subscribes
 *  until the R21 hook exists, and a listener with no reader is untestable. */
<<<END COMMENTTO

<<<SLICE STARTFROM
      stopped = false;
      host.connect(resumeEventId(state));
<<<END STARTFROM

<<<SLICE STARTTO
      stopped = false;
      dispatch({ kind: "timer" });
<<<END STARTTO

<<<SLICE STARTOLD
      stopped = false;
      host.connect(null);
<<<END STARTOLD

<<<SLICE RESTARTTEST
/** The driver is the only author of a `connect`. A restart after the fallback
 *  engaged must therefore resume on the fallback's terms, not reopen a stream
 *  the client already learned it cannot have (finding R-0627). */
describe("restarting after the fallback engaged", () => {
  it("polls on the driver's authority instead of reopening a stream", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    runner.stop();
    runner.start();
    expect(host.connects).toEqual([null]);
    expect(host.waits()).toEqual([3000, 3000]);
    expect(runner.view().status).toBe("delayed");
  });
});
<<<END RESTARTTEST
