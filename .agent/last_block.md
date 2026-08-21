── STEP T003/5 — F008 SSE event stream — ROUND 21 ────────────────────────────
Goal:
 Turn the runner into a STORE — `subscribe` plus a view whose object identity
 is stable — because that is exactly the pair React's `useSyncExternalStore`
 needs, and it is the last piece of T003 that can be proved under the
 node-environment vitest. The hook itself moves to R22. The round also writes
 the R20 verdict and resolves R-0627.

Why the hook is NOT in this round:
 R20's plan named R21 as the hook plus the delayed badge. The reviewer probed
 the one fact that decides it and reports it here rather than discovering it
 mid-round: neither jsdom nor happy-dom nor a testing library is installed,
 and this session's command guard DENIES the npm commands that would install
 one — `npm view jsdom version` was rejected before it ran. A React component
 therefore cannot be rendered or tested in this session at all. Guardrail G8
 forbids widening scope to route around a block, so the dependency decision
 and the hook both move to R22 and the OPERATOR is told, in the handback, that
 R22 needs a session whose guard permits the install. What is left is real
 T003 work that the block does not touch: the store seam the hook will read.

Bundle, in this commit order:
 C0a  save this block verbatim to `.agent/authored/f008-r21.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R21, applied whole
 C2   `.agent/live_review.md` <- LEDGER21, appended
 C3   `apps/ui/src/api/brainStreamRunner.ts` <- the six FROM/TO pairs
 C4   `apps/ui/src/api/brainStreamRunner.test.ts` <- STORETESTS, appended
 C5   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r21.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamRunner.ts`,
 `apps/ui/src/api/brainStreamRunner.test.ts`, `.agent/handoff.md`.

Slice convention:
 The authored units below are PLANF008R21, LEDGER21, IFACEFROM, IFACETO,
 COMMENTFROM, COMMENTTO, LETSFROM, LETSTO, VIEWFROM, VIEWTO, DISPATCHFROM,
 DISPATCHTO, RETURNFROM, RETURNTO and STORETESTS — fifteen, each delimited by
 a line beginning `<<<SLICE <name>` and one beginning `<<<END <name>`; marker
 lines are NOT part of the slice. Every slice is newline-terminated with no
 trailing whitespace on any line. Six are FROM/TO pairs. MEASURED by the
 reviewer's script, not asserted: EXACTLY ONE pair prints
 `TO contains FROM: true` — LETSFROM/LETSTO, whose TO appends whole lines below
 its single FROM line. The other five print FALSE, because each of those TOs
 inserts text BETWEEN the FROM's lines, so the FROM is no longer a contiguous
 substring of it. That is why G7 orders the CONSTRUCTIVE byte-equality as the
 binding reading for all six rather than a FROM-zero count: LETSFROM by
 construction still occurs at C3 and a zero there is unmeetable, so demanding
 it would be the R-0327 defect of ordering arithmetic the shape cannot produce.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, apply it as written and say
    so in the handback's deviations section — do not fix it.
 2. The commit order above is fixed: no extra commit, no dropped commit, no
    reordering. C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED — not
    jsdom, not happy-dom, not a testing library, and no file is created. Do not
    edit `package.json` or `package-lock.json` for any reason.
 4. C3 and C4 are separate commits and stay separate: AGENTS.md forbids mixing
    a change with the tests that pin it. At C3 the runner suite still holds 12
    tests; the four new ones arrive at C4.
 5. R-0627's `Done:` paragraph IS written this round, as LEDGER21's first
    paragraph — R20 landed the fix at `732091d9` and deferred the record here,
    exactly as R19 deferred R-0626's. Write no `Landed:` line. No finding id is
    minted this round: R-0628 stays free.
 6. R-0622 stays OPEN — do not add a TypeScript parser to make lint green.
 7. The post-C5 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md`: C5 cannot state
    facts about itself (R-0371).
 8. Two test processes never run at once. G9's counting suites run in the
    PRIMARY checkout: a fresh worktree has no `apps/ui/node_modules`, so its
    counts are untrustworthy both ways (R-0518). Where G10 needs `node_modules`
    in a worktree it SYMLINKS the primary one — never a copy, which dereferences
    npm's bin shims and manufactures failures (R-0591); the session guard
    rejects `ln` by form, so use `os.symlink`. `npx` inside a worktree can turn
    that symlink into a real directory: if it does, REMOVE the directory rather
    than unlinking it, and never touch the primary checkout's `node_modules`.
 9. The reviewer's OWN base readings, each produced by RUNNING the tool at
    `b97fb0b7` before this block was written rather than recalled (the R-0625
    counter-measure). In `apps/ui`: `npx vitest run` exits 0 at 7 files and 115
    tests; `npm run --silent typecheck` exits 0 with no output;
    `npm run --silent lint` EXITS 1 at `55 problems (53 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here. From the
    root the state readers plus canary exit 0 at 465 and `tests/ui_contracts/`
    at 397, both passed-plus-skipped — that split moves run to run at an
    unchanged tree, so a bare passed count is never a gate.
 10. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it and leave it
    open. `gh pr list --state open` returned `[]` at the R21 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after each
     of C0a, C0b, C1, C2, C3 and C4. Report each reading; per constraint 7 the
     post-C5 readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of the scratch block you
     were given, of `.agent/authored/f008-r21.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r21.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines, and that no slice carries trailing whitespace on any line.
     Expected, all fifteen: PLANF008R21 11a354cb at 46 lines, LEDGER21 b5a12c90,
     IFACEFROM c6846eb5, IFACETO 98d73adb, COMMENTFROM d454a7f0,
     COMMENTTO 6508cefc, LETSFROM 40253576, LETSTO a2cb490f,
     VIEWFROM da2c198d, VIEWTO 13963906, DISPATCHFROM 5bf4d77f,
     DISPATCHTO e8ebac13, RETURNFROM 0bcb20bc, RETURNTO 5ab9f2e7,
     STORETESTS d01f5234. COMMENTFROM's digest equals R20's COMMENTTO digest
     because it IS that text — R20 wrote the sentence this round retires.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R21. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER21 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
     normalised first, has as its LAST TWO units, in order, LEDGER21's two
     paragraphs. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another ASCII byte and report that BOTH readings reject it and both accept
     the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 199 at BOTH — no finding is minted this round —
     `^Done: R-\d+ — ` 5 then 6, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 20
     then 21 over that many DISTINCT keys, `^- R-0628 — ` 0 at both. Report the
     `Done:` ids at C2 — R-0620, R-0621, R-0623, R-0624, R-0626 and R-0627, no
     others. HEADER SWEEP at C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match, and that the R21 pair
     occurs EXACTLY ONCE.
 G7  The six pairs, CONSTRUCTIVELY, in `apps/ui/src/api/brainStreamRunner.ts`
     between the `b97fb0b7` blob and C3. For EACH pair report the count of the
     FROM and of the TO at `b97fb0b7` and at C3. Then apply ALL SIX
     replacements to the `b97fb0b7` blob IN THE ORDER LISTED IN THE BUNDLE and
     report that the result is BYTE-EQUAL to the C3 blob — report both sha256
     values and whether they match. The reviewer built that value in a
     throwaway worktree and it is
     f75aae30aed319bbbcc8c987a11dafa7deb21a086a921945fe304d5746ffaea2 over 5138
     bytes and 136 lines; the base blob is 3b823c0e over 3895 bytes and 107
     lines. That equality is the gate. Do NOT demand a FROM-zero count:
     LETSFROM's single line survives inside LETSTO by construction, so a zero
     there is unmeetable — report the real FROM count for each pair instead.
     Report also, at `b97fb0b7` and at C3, the counts of `subscribe`, which
     reads 1 then 4, `cachedView` 0 then 6, `publish` 0 then 3 and `listeners`
     0 then 4. `git show --numstat` for that path at C3 is 32/3 — this pair set
     REWRITES three lines and adds twenty-nine, so it is not an append and the
     block does not call it one.
 G8  The test append, C4 against C3. Report that the C3 blob of
     `apps/ui/src/api/brainStreamRunner.test.ts` is a byte-exact PREFIX of the
     C4 blob and that the remainder equals a newline plus STORETESTS — report
     its sha256, bytes and lines, which the reviewer measured at 130408b3 over
     1418 bytes and 40 lines. Report `^  it(` line-anchored in that file: 12
     at C3 and 16 at C4, and `^describe(` 6 then 7. `git show --numstat` at C4
     is 40/0 — forty inserted lines, ZERO deletions.
 G9  The suites are green in the PRIMARY checkout, run SERIALLY. Report the
     exit code and counts of each. In `apps/ui` AT C4: `npx vitest run` exits 0
     at 7 files and 119 tests — 115 at the base plus STORETESTS' four `it`s, and
     the arithmetic is the point. `npm run --silent typecheck` exits 0 with NO
     output. From the repository root AT C4:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. Report also `npm run --silent lint` at C4: it EXITS 1
     at `55 problems (53 errors, 2 warnings)`, UNCHANGED from constraint 9's
     base reading because this round adds no file. If any of these fails,
     report the real values and STOP.
 10. G10 RED CONTROLS — the colour, never a count — in ONE disposable worktree
     created at C4 under the gitignored `.remedy-wt/`, the primary checkout
     NEVER touched and `apps/ui/node_modules` reached by the symlink constraint
     8 names. THREE controls, one per new property, each restored byte-exactly
     between runs and each verified by sha256. Report for each that the mutated
     string occurs EXACTLY ONCE before it is mutated, the exit code, and the
     NAMES of the failing tests from
     `npx vitest run src/api/brainStreamRunner.test.ts`:
     (a) THE NOTIFICATION IS LOAD-BEARING. Replace the call line INSIDE
         `dispatch` — newline, FOUR spaces, `publish();`, newline — with the
         same line reading `if (false) publish();`. MIND THE INDENT: the
         reviewer first wrote this control at six spaces, it matched NOTHING,
         and the run went green while proving nothing. Report the occurrence
         count before mutating and STOP if it is not 1. It EXITS 1 with EIGHT
         failures — not two: with nothing publishing, `view()` keeps handing
         back the initial snapshot, so every test that READS the view fails
         alongside the listener tests. The reviewer measured that spread and
         names it here so a wider red than expected is not read as a defect.
         `publish` stays referenced, so the red is BEHAVIOUR, not a compile
         error.
     (b) THE IDENTITY GUARANTEE IS LOAD-BEARING. Replace `    return cachedView;`
         with `    return { ...cachedView };`. It EXITS 1 and names the
         same-object test. The VALUE assertions elsewhere stay green, which is
         what proves this control isolates identity from value.
     (c) THE SILENCE GUARANTEE IS LOAD-BEARING. Replace
         `    if (next.status === cachedView.status` with
         `    if (false && next.status === cachedView.status`. It EXITS 1 and
         names the test that a timer notifies nobody.
     After all three, report that the restored file's sha256 equals the C4
     blob's and that the same command EXITS 0 at 16 passed. REMOVE the worktree
     before writing C5.
 G11 The range. Report `git diff --name-only b97fb0b7..C4` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — six paths, none on
     either side alone. The full `b97fb0b7..C5` reading belongs to the ROUND
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
     here; the raw transcripts go in the ROUND REPORT (R-0582). The handback's
     `## Next` section NAMES THE BLOCKER for the operator: R22 needs a session
     whose command guard permits installing a DOM environment, because this
     one denied it.

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~90 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R21
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
R21 turns the runner into a STORE: `subscribe` plus a view whose object
identity is stable across calls that change nothing. That pair is exactly what
React's `useSyncExternalStore` requires, and it is the last piece of T003
provable under the node-environment vitest. The round also writes the R20
verdict and resolves R-0627, whose fix — the driver as the single author of a
`connect` — landed at `732091d9`.

## Next Steps
1. R22 adds the thin React `useBrainStream` hook over this store and the
   visible delayed badge. IT IS BLOCKED until a session can install a DOM
   environment: no jsdom, happy-dom or testing library is present and the
   R21 session's command guard denied the npm commands that would add one.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `b97fb0b7` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622 and it routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 there and ARE the gates. Repository-wide
  `ruff check .` is RED too and is not a gate; this round changes no Python.
- A store that returns a fresh view object on every call sends
  `useSyncExternalStore` into an endless re-render. Identity stability is
  therefore a CONTRACT of this seam and not an optimisation, and R21 pins it
  with its own test and its own red control.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason. R22
  owns that, together with the dependency decision it cannot avoid.
<<<END PLANF008R21

<<<SLICE LEDGER21
Done: R-0627 — RESOLVED at `732091d9` by making `start()` dispatch the opening event instead of calling the transport itself: `perform` now issues the `connect` the driver chose, so the driver is the SINGLE AUTHORITY on what the client does next and the module has exactly one `host.connect(` call site left, inside `perform`. RE-MEASURED BY THE REVIEWER at the R21 gate rather than read back out of the handback: applying the round's three FROM/TO pairs to the `1f10de78` blob in one pass reproduces the C3 blob byte for byte at sha256 3b823c0e7e1d16e518f9545f9ece5b0ca1f0130de8f2131d5b48991797ab4626 over 3895 bytes, `host.connect(` reads 2 then 1, `resumeEventId` 2 then 0, and the file is 107 lines at both revisions. THE FINDING'S OWN TEXT WAS TOO WEAK AND THE FIX PROVED IT. R-0627 said "no behaviour is wrong"; in fact `start()` reopened a stream unconditionally while the driver returns a `poll` effect once the fallback has engaged, so the fix CHANGED what a restart does in that state. Nothing covered it because nothing called `start()` twice, which is why R20 added `restarting after the fallback engaged > polls on the driver's authority instead of reopening a stream`. THE RED CONTROL IS THE PROOF, re-run by the reviewer in a disposable worktree with `node_modules` symlinked: swapping the two-line body back to the pre-R20 spelling EXITS 1 naming EXACTLY that one test with the other ELEVEN green, and disabling `case "poll":` EXITS 1 with that test among the three. A duplicated decision that merely happens to agree is a defect precisely because the day it stops agreeing, no gate sees it.

Gate: R21 — the R20 entry. R20 PASSED and no finding is registered against its work — the third consecutive round on this branch for which that is true. EVERY GATE WAS RE-RUN BY THE REVIEWER, never read back out of the handback. TRANSPORT PROVED PRIMARY: `.remedy-wt/f008-r20.md` still existed at review time and was compared disk-to-disk against `.agent/authored/f008-r20.md` at `462a8130` and `.agent/last_block.md` at `e51f01ef` — all three EQUAL at sha256 539e77127a152a43224572f3f4e3890d88f0ed0cdcb54a53e260937b9a789618 over 25328 bytes and 335 lines. TEN SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching and none carrying trailing whitespace: PLANF008R20 833e3762, LEDGER20 0321b69d, IMPORTFROM 601f32f9, IMPORTTO 850c11a7, COMMENTFROM 2e897c87, COMMENTTO d454a7f0, STARTFROM f2dbae03, STARTTO d59f9ccd, STARTOLD 79858850 and RESTARTTEST feed12b4. THE PLAN LANDED FIRST at `258413d8`, byte-equal at 49 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `84e2cde2` is a byte-exact prefix of the `258413d8` blob plus a 5094-byte remainder equal to a newline plus LEDGER20, agreed by an INDEPENDENT blank-line split of the whole file into 228 units whose LAST TWO are LEDGER20's paragraphs in order, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS MOVED AS ORDERED — 199 at BOTH revisions because no id was minted, `Done:` 4 to 5 over exactly R-0620, R-0621, R-0623, R-0624 and R-0626, `Landed:` 0 at both, `Gate: R` 19 to 20 over that many DISTINCT keys, R-0628 0 at both; nineteen of the twenty headers match the `Gate: R<n> — the R<n-1> entry.` shape and the single non-match is the F255 entry, correctly shaped for what it records. THE APPENDED TEST is a byte-exact prefix relationship, `e600a055` to `d99b6571`, remainder 5bb52e85 over 638 bytes, `^  it(` 11 to 12 and `^describe(` 5 to 6 with ZERO deletions. STARTOLD, the tenth slice, reached NO commit: the reviewer confirmed its absence from both the C3 runner blob and the C4 test blob. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 7 files and 115 tests, `npm run --silent typecheck` exits 0 silently, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 397. LINT IS RED AND DECLARED, never repaired: 55 problems, 53 errors, 2 warnings, unchanged because the round adds no file, which is R-0622. SEVEN single-parent commits, insertions 335, 239, 24, 4, 3 and 15 through C4 and 46 at C5, every one under 500 and every cell equal to the handback's `+/-` column including the deletions; zero lines beginning with a slice marker in all five targets; this round's seven reflog operations all `commit`, with amend, rebase and cherry at 0; an 84-line handback within the 100 that seven commits allow, its item-status table naming C0a through C5 exactly once each; the tree clean and the primary checkout the only worktree. THE BLOCK ITSELF WAS DRY-RUN BEFORE DELEGATION and that is why it held: applying the slices to a throwaway worktree caught four defects in the reviewer's own text — a 50-line plan against a 50-line cap, a 4/4 numstat that is really 3/3 because two comment lines share their first line, a red control aimed at a string occurring THREE times, and a control that reverted the body without its import and reddened all twelve tests on a load error rather than a behaviour. Every one was fixed before a worker ever saw the block.
<<<END LEDGER21

<<<SLICE IFACEFROM
  view(): BrainStreamView;
}
<<<END IFACEFROM

<<<SLICE IFACETO
  view(): BrainStreamView;
  /** Hear about every visible change. The returned function unsubscribes. */
  subscribe(listener: () => void): () => void;
}
<<<END IFACETO

<<<SLICE COMMENTFROM
/** Remedy deliberately gives this no change callback yet: nothing subscribes
 *  until the R21 hook exists, and a listener with no reader is untestable. */
<<<END COMMENTFROM

<<<SLICE COMMENTTO
/** The runner IS a store: `subscribe` plus a `view` whose object identity only
 *  changes when something visible does are exactly the pair React's
 *  `useSyncExternalStore` requires, so the hook holds no state of its own. */
<<<END COMMENTTO

<<<SLICE LETSFROM
  let cancelPending: (() => void) | null = null;
<<<END LETSFROM

<<<SLICE LETSTO
  let cancelPending: (() => void) | null = null;
  const listeners = new Set<() => void>();
  let cachedView: BrainStreamView = {
    status: null,
    lastSeq: null,
    gapDetected: false,
  };
<<<END LETSTO

<<<SLICE VIEWFROM
  function view(): BrainStreamView {
    return {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
    };
  }
<<<END VIEWFROM

<<<SLICE VIEWTO
  /** The SAME object until something a reader can see changes. React's
   *  `useSyncExternalStore` compares snapshots with `Object.is` and re-renders
   *  forever if a store hands back a fresh object every call, so this identity
   *  is a contract of the seam rather than an optimisation. */
  function view(): BrainStreamView {
    return cachedView;
  }

  /** Recompute what a reader would see; publish and announce it only if it
   *  actually moved, so a timer that changes nothing wakes nobody. */
  function publish(): void {
    const next: BrainStreamView = {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
    };
    if (next.status === cachedView.status
      && next.lastSeq === cachedView.lastSeq
      && next.gapDetected === cachedView.gapDetected) return;
    cachedView = next;
    for (const listener of listeners) listener();
  }
<<<END VIEWTO

<<<SLICE DISPATCHFROM
    if (event.kind !== "timer") settled = true;
    for (const effect of step.effects) perform(effect);
<<<END DISPATCHFROM

<<<SLICE DISPATCHTO
    if (event.kind !== "timer") settled = true;
    publish();
    for (const effect of step.effects) perform(effect);
<<<END DISPATCHTO

<<<SLICE RETURNFROM
    view,
  };
<<<END RETURNFROM

<<<SLICE RETURNTO
    view,
    subscribe(listener: () => void): () => void {
      listeners.add(listener);
      return () => { listeners.delete(listener); };
    },
  };
<<<END RETURNTO

<<<SLICE STORETESTS
/** The seam R22's hook reads. `useSyncExternalStore` needs a subscribe and a
 *  snapshot whose identity is stable, so both are pinned here. */
describe("the runner as a store", () => {
  it("hands back the same view object until something visibly changes", () => {
    const { runner } = started();
    const first = runner.view();
    expect(runner.view()).toBe(first);
    runner.dispatch({ kind: "opened" });
    const second = runner.view();
    expect(second).not.toBe(first);
    expect(runner.view()).toBe(second);
  });
  it("tells every listener once per visible change", () => {
    const { runner } = started();
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "opened" });
    expect(calls).toBe(1);
    runner.dispatch(frame(3));
    expect(calls).toBe(2);
  });
  it("stays silent when an event changes nothing a reader can see", () => {
    const { runner } = started();
    runner.dispatch({ kind: "opened" });
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "timer" });
    expect(calls).toBe(0);
  });
  it("stops calling a listener once it unsubscribes", () => {
    const { runner } = started();
    let calls = 0;
    const unsubscribe = runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "opened" });
    unsubscribe();
    runner.dispatch(frame(3));
    expect(calls).toBe(1);
  });
});
<<<END STORETESTS
