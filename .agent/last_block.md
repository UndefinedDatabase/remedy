── STEP T003/3 — F008 SSE event stream — ROUND 19 ────────────────────────────
Goal:
 A SMALL round that closes the record R18 left open and clears the last naming
 defect out of T003's pure layer before any React file is added: write the R18
 verdict, resolve R-0624, register R-0627, and land R-0626's rename of the
 driver's `opened` local to `gapOpened`. No behaviour changes.

Bundle, in this commit order:
 C0a  save this block verbatim to `.agent/authored/f008-r19.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R19, applied whole
 C2   `.agent/live_review.md` <- LEDGER19, appended
 C3   `apps/ui/src/api/brainStreamDriver.ts` <- OPENEDFROM replaced by OPENEDTO
 C4   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r19.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/api/brainStreamDriver.ts`,
 `.agent/handoff.md`.

Slice convention:
 The authored units below are PLANF008R19, LEDGER19, OPENEDFROM and OPENEDTO,
 each delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of the slice. Every slice is
 newline-terminated with no trailing whitespace on any line. OPENEDFROM and
 OPENEDTO are a two-line FROM/TO pair. MEASURED, not asserted: the containment
 test prints `TO contains FROM: false`, so the pair is a REWRITE and G7 orders
 the FROM-zero count that only a rewrite can satisfy.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, apply it as written and say
    so in the handback's deviations section — do not fix it.
 2. The commit order above is fixed: no extra commit, no dropped commit, no
    reordering. C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. No dependency is added, no file
    is created, and no other occurrence of `opened` in the repository moves.
 4. The C3 edit is a RENAME of a local `const` and its single use. It changes
    no behaviour, so the suite counts at C3 equal the base counts exactly.
 5. R-0626 is FIXED here but gets NO `Done:` paragraph: only reviewer-authored
    text sets a resolution (§4 item 4) and R20 owes that paragraph, exactly as
    R18 left R-0624's resolution to this round. Write no `Landed:` line either
    — LEDGER19 already covers the round.
 6. R-0622 stays OPEN — do not add a TypeScript parser to make lint green.
    R-0627 is REGISTERED and NOT fixed here; its fix belongs to R20.
 7. The post-C4 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md`: C4 cannot state
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
    `f484d47a` before this block was written rather than recalled (the R-0625
    counter-measure). In `apps/ui`: `npx vitest run` exits 0 at 7 files and 114
    tests; `npm run --silent typecheck` exits 0 with no output;
    `npm run --silent lint` EXITS 1 at `55 problems (53 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here. From the
    root the state readers plus canary exit 0 at 465 and `tests/ui_contracts/`
    at 397, both passed-plus-skipped — that split moves run to run at an
    unchanged tree, so a bare passed count is never a gate.
 10. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it and leave it
    open. `gh pr list --state open` returned `[]` at the R19 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after each
     of C0a, C0b, C1, C2 and C3. Report each reading; per constraint 7 the
     post-C4 readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of the scratch block you
     were given, of `.agent/authored/f008-r19.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r19.md` by their marker lines, take the COUNT from that
     listing, and report each slice's newline-INCLUDED sha256, bytes and lines.
     Expected: PLANF008R19 52a03f9d, LEDGER19 35597ada, OPENEDFROM b1ede53e, OPENEDTO fcf7e651.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R19. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER19 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating newline
     normalised first, has as its LAST THREE units, in order, LEDGER19's three
     paragraphs. NEGATIVE CONTROL: flip one byte of the remainder and report
     that BOTH readings reject it and both accept the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 198 then 199, `^Done: R-\d+ — ` 3 then 4,
     `^Landed: ` 0 at both, `^Gate: R\d+ — ` 18 then 19 over that many DISTINCT
     keys, `^- R-0627 — ` 0 then 1, `^- R-0628 — ` 0 at both. Report the `Done:`
     ids at C2 — R-0620, R-0621, R-0623 and R-0624, no others. HEADER SWEEP at
     C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match, and that the R19 pair
     occurs EXACTLY ONCE.
 G7  The rename pair, CONSTRUCTIVELY. In `apps/ui/src/api/brainStreamDriver.ts`
     report: OPENEDFROM occurs EXACTLY ONCE in the `23a5088c` blob and 0 times
     at C3; OPENEDTO 0 times at `23a5088c` and exactly once at C3; and that
     replacing that one occurrence in the `23a5088c` blob yields a file
     BYTE-EQUAL to the C3 blob — report both sha256 values and whether they
     match. Report also, at `23a5088c` and at C3, the count of the bare
     identifier `opened` (the regex `(?<![\"\w])opened(?![\"\w])`), which reads
     2 then 0; the count of the quoted `"opened"`, which is 2 at BOTH because
     the transport event kind is NOT renamed; and the count of `gapOpened`,
     which reads 0 then 2. `git show --numstat` for that path at C3 is 2/2, and
     the file's line count is UNCHANGED at 92.
 G8  The suites are green in the PRIMARY checkout, run SERIALLY. Report the
     exit code and counts of each. In `apps/ui` AT C3: `npx vitest run` exits 0
     at 7 files and 114 tests, and `npm run --silent typecheck` exits 0. From
     the repository root AT C3:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. Report also `npm run --silent lint` at C3: it EXITS 1
     at `55 problems (53 errors, 2 warnings)`, UNCHANGED from constraint 9's
     base reading because this round adds no file. EVERY ONE of these equals
     the base exactly — that identity is the point of gate G8 this round, since
     a rename that moved any count would not be a rename. If any identity
     fails, report the real values and STOP.
 G9  RED CONTROL — the colour, never a count — in a disposable worktree created
     at C3 under the gitignored `.remedy-wt/`, the primary checkout NEVER
     touched and `apps/ui/node_modules` reached by the symlink constraint 8
     names. The rename must leave the snapshot branch LIVE, not merely
     compiling: report that `effects: gapOpened ?` occurs EXACTLY ONCE in
     `apps/ui/src/api/brainStreamDriver.ts`, replace it with
     `effects: false ?`, and report the exit code and the NAMES of the failing
     tests from
     `npx vitest run src/api/brainStreamDriver.test.ts src/api/brainStreamRunner.test.ts`.
     It EXITS 1 and names at least one test from EACH of those two files.
     Restore the file BYTE-EXACTLY, verified by sha256, report that the restored
     run EXITS 0, and REMOVE the worktree before writing C4.
 G10 The range. Report `git diff --name-only f484d47a..C3` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — five paths, none on
     either side alone. The full `f484d47a..C4` reading belongs to the ROUND
     REPORT (constraint 7, R-0371). Report that every commit in the range has
     exactly ONE parent, and BOTH numstat cells per path from
     `git show --numstat`, cross-checked against `git diff --numstat`, every
     insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (§3 item 28).
 G11 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2, the driver at C3 and
     `.agent/handoff.md` at C4. Each is 0.
 G12 Reflog. Count THIS round's own entries by the OPERATION before the first
     `:` in `%gs`. All five pre-C4 entries are `commit`; report `amend`,
     `rebase` and `cherry` at 0, and assert no total.
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2, C3 and C4 — "exactly one row" scoping
     to that TABLE, not to the whole file. Measure its line count with `wc -l`
     BEFORE committing it; this round has six commits, so the cap is 100 lines,
     and an overage carries a DECISION D15 stated-cause line naming the real
     count and the mandated content that caused it. One line per gate here; the
     raw transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~85 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R19
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
R19 is a SMALL round that closes the record R18 left open and clears the last
naming defect out of T003's pure layer before a React file is added. It writes
the R18 verdict, resolves R-0624 — whose fix landed at `d3d5d1aa`, where the
runner declines to report a status until a transport event has resolved —
registers R-0627, and lands R-0626's rename of the driver's `opened` local to
`gapOpened`. No behaviour changes: the rename is proved neutral by the suite
staying at its count and by the snapshot branch still going red when forced.

## Next Steps
1. R20 adds the thin React `useBrainStream` hook over the runner and the
   visible delayed badge — the first surface that RENDERS the runner's view,
   and the round that must satisfy docs/ui/design_reference/ for the badge.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364):
  measured at `f484d47a` it exits 1 with 55 problems, every error a
  `Parsing error`, because that eslint config installs no TypeScript parser.
  That is R-0622, it routes to a paydown branch, and each new `.ts` file adds
  one more. `npm run typecheck` and `npx vitest run` both exit 0 there and ARE
  the gates. Repository-wide `ruff check .` is RED too and is not a gate; this
  round changes no Python.
- R20 is the round where a gate this repository owns stops covering the code:
  no React component can be rendered here. The runner is framework-free so the
  hook has almost no branch left to get wrong, but the BADGE is a visual
  surface and docs/ui/design_reference/ is binding for it, with any deviation
  owed an assumption_log entry carrying a technical reason. If the hook cannot
  be kept trivial, the honest move is a jsdom dependency and its own round.
- R-0626's fix lands here and its `Done:` paragraph is owed by R20, exactly as
  R18 left R-0624's resolution to this round.
<<<END PLANF008R19

<<<SLICE LEDGER19
Done: R-0624 — RESOLVED at `d3d5d1aa` by making the honest value EXIST without widening the union the feature file fixes. `createBrainStreamRunner` holds a private `settled` flag, `view()` returns `status: settled ? state.status : null`, and `settled` turns true only on an event the TRANSPORT produced — a `timer`, being the runner's own bookkeeping, never resolves it. So a client that has never connected reports NO status rather than the `reconnecting` that claimed a history it did not have, `BrainStreamStatus` still has exactly the three members `docs/roadmap/features/T5_F008.md` names, and no feature-file amendment was needed. RE-MEASURED BY THE REVIEWER at the R19 gate rather than read back out of the handback: in a disposable worktree at `8e7101cb` with `node_modules` symlinked, replacing `status: settled ? state.status : null` with `status: state.status` EXITS 1 naming both `a runner that has not connected > reports no status at all rather than claiming a reconnect` and `> is not resolved by a stray timer, which is its own bookkeeping`, and replacing `if (event.kind !== "timer") settled = true;` with `settled = true;` EXITS 1 naming the second of those. Both restored byte-exactly, the file EXITS 0 at 11 passed. The deferral R-0624 declared is therefore discharged one round early: the fix did not need the badge after all, because the runner — not the hook — is what a badge reads.

- R-0627 — Low — ONE ACTION SPELLED TWO WAYS IN THE SAME MODULE, SO THE DRIVER STOPS BEING THE SINGLE AUTHORITY ON WHAT THE CLIENT DOES NEXT. In `apps/ui/src/api/brainStreamRunner.ts` at `d3d5d1aa`, `start()` calls `host.connect(resumeEventId(state))` DIRECTLY, while every other connect in the module arrives as a `connect` effect the driver returned and `perform` executed. FOUND AND DECLARED BY THE WORKER as an observation it was not asked for — the fifth consecutive round in which a worker's declaration rather than a gate is what put a reviewer-authored defect on the record. IT IS CORRECT TODAY and the tests pin it: `a runner that has not connected > reports no status at all rather than claiming a reconnect` asserts `host.connects` equals `[null]` after `start()`. WHY IT IS STILL A DEFECT: the driver exists so that what the client does next is decided in ONE place, and `start` is now a second place that happens to agree. `stepBrainStream(state, { kind: "timer" })` already returns exactly that effect for a fresh state — the reviewer measured it, and the test `is not resolved by a stray timer` records the two spellings producing the same call, `[null, null]`, without naming that as the property under test. If the driver's opening effect ever changes, `start` diverges silently and no gate in this repository sees it. WHY LOW: no behaviour is wrong, the duplication is two lines apart from the code it duplicates, and the module is not yet imported by anything. THE FIX, routed to R20 and named in this round's plan: `start()` dispatches the opening event and lets `perform` issue the effect, so the driver is the only author of a `connect`; the existing tests keep their assertions unchanged, which is what makes the change safe to land beside the hook.

Gate: R19 — the R18 entry. R18 PASSED. No finding is registered against its work, and R-0627 above is a defect in the reviewer's own authored RUNNER text that the worker declared, not a defect of the round. EVERY IDENTITY THE BLOCK PREDICTED WAS MET — the first round on this branch in three for which that is true, R17 and R16 each having carried one that was not. TRANSPORT PROVED PRIMARY, not by the digest fallback: the reviewer authored this block in the same session, so `.remedy-wt/f008-r18.md` still existed at review time and was compared disk-to-disk against `.agent/authored/f008-r18.md` at `fe8a2495` and `.agent/last_block.md` at `a18c59bd` — all three EQUAL at sha256 884a5512e56e51b9b474f9deae1638b428456d2c598a166ec846a1630aa34e7d over 32768 bytes and 490 lines. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest matching: PLANF008R18 95960376, LEDGER18 a6db99e5, RUNNER fefd47e6 and RUNNERTESTS e600a055. THE PLAN LANDED FIRST at `4de89c5a`, byte-equal at 48 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008` — the four properties `tests/ui_server/test_dashboard_contract.py` and `tests/orchestration/test_test_runner.py` actually assert about that file. THE APPEND at `23a5088c` is a byte-exact prefix of the `4de89c5a` blob plus an 8921-byte remainder equal to a newline plus LEDGER18, agreed by an INDEPENDENT blank-line split of the whole file into 223 units whose LAST FOUR are LEDGER18's paragraphs in order, with a one-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS MOVED AS ORDERED — 196 to 198 registered, `Done:` 2 to 3 over exactly R-0620, R-0621 and R-0623, `Landed:` 0 at both, `Gate: R` 17 to 18 over that many DISTINCT keys, R-0625 and R-0626 each 0 then 1, R-0627 0 at both — so this record's THIRD resolution landed and only the two ordered ids were minted; seventeen of the eighteen headers match the `Gate: R<n> — the R<n-1> entry.` shape with the second numeral one below the first, and the single non-match is the F255 entry, correctly shaped for what it records. BOTH NEW FILES ARE ABSENT at `2c3abc5e` by `git ls-tree` and byte-equal to their slices at `d3d5d1aa` and `8e7101cb`, 107 and 148 lines against 0 deletions. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 7 files and 114 tests, `npm run --silent typecheck` exits 0 silently, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 397. THE ARITHMETIC RECONCILES: RUNNERTESTS holds 11 lines matching `^  it(` and 103 plus 11 is 114. LINT IS RED AND DECLARED, never repaired: 55 problems against the base's 53, exactly two more errors, one `Parsing error` per new file, which is R-0622. ALL FOUR RED CONTROLS RE-RUN BY THE REVIEWER against the `8e7101cb` tree in its own disposable worktree, the primary checkout untouched: each mutated byte string occurs exactly once, each mutation EXITS 1 naming the tests the block predicted and no others, each file restored byte-exactly, and the restored file EXITS 0 at 11 passed. SEVEN single-parent commits, insertions 490, 403, 24, 8, 107, 148 and 41 in that order, every one under 500 and every cell equal to the handback's `+/-` column including the deletions; zero lines beginning with a slice marker in all five targets; the last forty reflog operations all `commit`, with amend, rebase and cherry at 0; an 82-line handback within the 100 that seven commits allow, its item-status table naming C0a through C5 exactly once each; the tree clean with the primary checkout the only worktree.
<<<END LEDGER19

<<<SLICE OPENEDFROM
      const opened = next.gapDetected && !state.gapDetected;
      return { state: next, effects: opened ? [{ kind: "snapshot" }] : [] };
<<<END OPENEDFROM

<<<SLICE OPENEDTO
      const gapOpened = next.gapDetected && !state.gapDetected;
      return { state: next, effects: gapOpened ? [{ kind: "snapshot" }] : [] };
<<<END OPENEDTO
