── STEP T002 PART 5C / F040 — ROUND 12 ────────────────────────
Goal:        Extend `DigestVisibilityPort` (DECISION F040 D8) with the two
             last-seen methods D8 already names but no round has yet added,
             and build the browser-local STORAGE EDGE that implements all
             four of the port's methods — dismissal and last-seen, both
             keyed per job — the first localStorage-backed module in this
             client. Pin it with a REAL vitest guard (this is a `.ts` file,
             collected by the runner unlike `DigestHeroCard.tsx`), red proved
             by mutation inside a disposable worktree via the F256 D6 route
             R11 already used successfully for exactly this node_modules
             problem.
Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R11 verdict and R-0756's resolution) ·
             C3 extend the port interface · C4 the storage edge · C5 its
             guard · C6 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r12.md`                       (C0a, new)
               `.agent/last_block.md`                               (C0b)
               `.agent/plan.md`                                     (C1)
               `.agent/live_review.md`                              (C2)
               `apps/ui/src/api/digestVisibility.ts`                (C3)
               `apps/ui/src/api/browserDigestPort.ts`      (C4, new)
               `apps/ui/src/api/browserDigestPort.test.ts` (C5, new)
               `.agent/handoff.md`                                  (C6)
             NOTHING ELSE IS EDITED. `jobDigest.ts`, `digestCardCopy.ts`,
             `DigestHeroCard.tsx`, `DigestHeroCard.module.css`,
             `RemedyShell.tsx`, `digestVisibility.test.ts` and every file
             under `docs/roadmap/` are READ ONLY. The mount, `loadJobDigest`
             and the layout CSS are explicitly NOT this round's — PLAN12
             routes them to the next round, and constraint 9 forbids
             reaching for them here.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the objection in the handback. Never repair a slice.
    The two NEW files are a SPEC, not a slice — the code is yours to write —
    and this constraint does not bind them; constraint 8 below binds them
    instead.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6 and it is fixed.
    Every claim any slice makes about this round's own landed change rests on
    this ordering constraint and on nothing else (§3 item 20, R-0524
    carve-out).
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD12 IS APPENDED, never inserted. Measured directly rather than
    assumed: `.agent/live_review.md` at the branch tip this round opens on
    (`d649c330`) carries NO trailing newline at all — its last byte is the
    period ending R-0756's own registration paragraph. The append is one
    newline followed by the slice's bytes regardless of what the base's own
    trailing byte is; G3 re-measures the base rather than trusting this
    paragraph.
 5. THE BLOCK ARRIVES AS A FILE, NOT AS TYPED TEXT. It is on disk at
    `.remedy-wt/f040-r12-block.md`, written there by the reviewer. Copy it to
    both destinations with `shutil.copyfile` and never retype it. Because
    that original survives, G1 is a `cmp` against it rather than a chain of
    the worker's own outputs, and the transport proof this round therefore
    does cover the emitted bytes (§3 item 37). Two lines of the frame are
    runs of the single character `─`: the STEP line's trailing run is 24
    characters and the closing line is 62. Their lengths are stated because a
    run has none a reader recovers by eye; nothing appliable lives in the
    frame either way.
 6. THE PORT INTERFACE EXTENSION IS EXACTLY TWO NEW METHOD SIGNATURES, added
    to `DigestVisibilityPort` in `digestVisibility.ts`, and nothing else in
    that file's RULE LOGIC changes — `digestVisibility()` itself, its
    partition tables, its exported types other than the interface, and its
    header comment's absences list are untouched in substance. The header
    comment's paragraph about the port ("DECLARED HERE AND IMPLEMENTED
    NOWHERE IN THIS FILE") may gain one sentence naming that last-seen now
    flows through the same port DECISION F040 D8 already named for it; no
    other prose in that file is rewritten. This is a SPEC edit — the exact
    wording is yours — governed by G5 below rather than a byte pair.
 7. THE NEW STORAGE EDGE READS NO CLOCK AND OPENS NO SOCKET. Every instant it
    persists arrives as a parameter — `writeDismissal`'s `dismissedAtMs` and
    `writeLastSeen`'s `seenAtMs` are both given, never taken from `Date.now`
    — because the ONE clock read for this feature already lives at
    `DigestHeroCard.tsx`'s dismiss handler (constraint 7 of the R11 block)
    and a second read here would be a second edge for a value DECISION F040
    D8 already assigns one home. `Date.now`, `fetch` and `XMLHttpRequest`
    occur zero times in `browserDigestPort.ts`'s executable source.
 8. THE STORAGE EDGE TAKES ITS STORAGE INJECTED, NEVER THE GLOBAL DIRECTLY.
    The exported factory's parameter is typed against the DOM lib's own
    `Storage` interface (`Pick<Storage, "getItem" | "setItem">`, or the two
    full methods — your call, document which and why) rather than a
    bespoke interface invented for this file: `Storage` already has exactly
    this shape, and inventing a parallel type would be a second name for one
    thing. This is what makes the module testable without `vi.stubGlobal`,
    which R-0724's own reading holds this repository does not do — no test
    under `apps/ui/src` patches a global today, and this file does not start.
    A REAL binder that closes over `window.localStorage` belongs at the
    MOUNT, next round, exactly where `browserBrainStreamEnv(window)` binds
    its own globals for `RemedyShell.tsx` to call — this round builds and
    guards ONLY the injectable factory, never a bound instance of it, so
    `window` and `localStorage` (the identifier) occur ZERO times in
    `browserDigestPort.ts`.
 9. NO MOUNT, NO FETCH, NO CSS. `RemedyShell.tsx`, `loadJobDigest` and any
    layout stylesheet are the next round's, per PLAN12 step 2, and are not
    reached for here even partially.
10. THE FOUR KEYS ARE NAMESPACED AND DISTINCT PER JOB AND PER CONCERN. Reading
    or writing dismissal for one job must never read or write last-seen for
    that job or either concern for a DIFFERENT job — G6's guard proves this
    with two distinct job ids and both concerns, not asserted from the key
    format alone.
11. A STORED VALUE THAT DOES NOT PARSE TO A FINITE NUMBER READS AS ABSENT
    (`null`), never as `NaN` or a thrown exception — the same "an absence is a
    state, not an error" posture `digestVisibility.ts`'s own `DigestDismissal`
    already takes. G6 proves this against a corrupt stored string, paired
    with a positive control proving a valid stored string is read back
    exactly.
12. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree`, removed
    before the handback, with `git worktree list` showing one line. The
    primary checkout satisfies `git status --porcelain` empty at every
    commit.
13. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C6. If it appears, finish the commit in hand, write the handback and
    stop.
14. `npx vitest` and `npm run test:unit` are REFUSED to this session class as
    a DIRECT shell spelling. Reach vitest and tsc through the pytest nodes
    named in G7, and reach the worktree mutation route of G6 through a
    Python driver's `subprocess.run`, never through a bare shell line —
    R-0724's reading: the refusal binds the CALLER'S spelling, not the
    environment.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C6 (§3 item 31), and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk, against the reviewer's
    own surviving original: report the sha256 and byte length of
    `.remedy-wt/f040-r12-block.md`, of `.agent/authored/f040-r12.md` and of
    `.agent/last_block.md`, and that all three are equal. Report the digest
    you MEASURED; this block asserts no digest of itself, which it could not
    do.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN12 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a): the base blob is a byte PREFIX of
    the committed file and base + one newline + slice reconstructs it whole.
    Reading (b), independent and structural: split the slice on blank lines,
    COUNT the paragraphs into N, and compare the committed file's LAST N
    blank-line units against those N paragraphs IN ORDER. Negative control:
    inside the disposable worktree, flip one byte in the FIRST appended
    paragraph and report that both readings REJECT it and both ACCEPT the
    unflipped bytes. N is counted by the script and never asserted.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids matching
    `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R11 — `. Report ADDED and REMOVED for each set and the open
    count (registered minus resolved, both distinct) before and after; report
    that `R-0756` moves from open to resolved and that no other id's status
    changes.
 G5 THE PORT INTERFACE'S SHAPE, at C3. Over `digestVisibility.ts` with
    comments stripped: parse `DigestVisibilityPort`'s member list and report
    it has exactly four methods — `readDismissal`, `writeDismissal`,
    `readLastSeen`, `writeLastSeen` — with the two new signatures matching
    `readLastSeen(jobId: string): number | null` and
    `writeLastSeen(jobId: string, seenAtMs: number): void` modulo whitespace.
    Report that `digestVisibility`'s own function body is BYTE-IDENTICAL
    before and after this commit (diff the function's own span, not the
    whole file) and that every exported type other than the interface is
    unchanged. Report that `DigestVisibilityInput`, `DigestVisibility` and
    `DigestVisibilityReason` still exist with the same members they had at
    `HEAD` before this round (read at C3's parent).
 G6 THE STORAGE EDGE'S SHAPE, ITS GUARD AND ITS RED PROOF, at C5.
    First, over `browserDigestPort.ts` with comments stripped and quoted
    literals blanked: `window` and `localStorage` each occur ZERO times in
    the executable source, `Date.now` occurs zero times, `fetch` and
    `XMLHttpRequest` occur zero times — each absence paired with a salted
    positive control proving the scan can see the token when it is really
    there. Report the exported names.
    Second, `python3 -m pytest -q` is not this gate's route — this file is
    `.ts` with a `.test.ts` sibling, so its own colour comes from vitest, not
    from a pytest text guard; run it through G7 below, not here.
    Third, THE RED PROOF, run through a Python driver's `subprocess.run`
    (never a bare `npx vitest` shell line, per constraint 14), by the
    worktree route DECISION F256 D6 fixes: mutate inside a disposable
    worktree, run vitest FROM THE PRIMARY `apps/ui` so module resolution
    finds the primary's `node_modules`, and name the worktree's mutated file
    by ABSOLUTE path in a scratch vitest config under `.remedy-wt/` whose
    `cacheDir` also points inside `.remedy-wt/`, exporting a PLAIN OBJECT.
    Report, in this order, the UNMUTATED CONTROL's real exit code and test
    count, then for EACH of these four mutations of `browserDigestPort.ts` —
    reverting to the control and re-confirming its colour before the next —
    the real exit code and the node ids that DIED:
      (a) swap the dismissal and last-seen key strings for one job (so a
          dismissal read returns what was written as a last-seen instant);
      (b) make `writeDismissal` write under the SAME key for every job id
          (drop the job id from the key), so two jobs' dismissals collide;
      (c) remove the finite-number guard, so a corrupt stored string is
          returned as `NaN` instead of `null`;
      (d) make `readLastSeen` read the dismissal key instead of its own.
    Assert each anchor is UNIQUE in the file before replacing it, and report
    the count. For each, report that the bytes on disk differ from the
    original AND that the DECLARATION differs after comment stripping.
    Restore and report byte equality to the committed file after each.
 G7 VITEST AND THE TYPECHECK, at C5, through the pytest nodes and not through
    a bare shell line (constraint 14):
      python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    Report each REAL exit code, and report PASSED or SKIPPED explicitly for
    both — a skip is not a type check and is not vitest. Report the vitest
    node's own test-file and test count, RE-MEASURED at this round's own base
    `d649c330` rather than trusting any earlier round's figure, and report
    that the post-commit count rose by exactly the number of tests
    `browserDigestPort.test.ts` adds and by exactly one file.
 G8 THE SUITES, THE TOOLCHAIN AND THE TREE, at C5:
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    Report each REAL exit code. Then report `git status --porcelain`, the
    count from `git ls-files --others --exclude-standard`, `git worktree
    list`, and the `+` column of `git diff --numstat` for each commit from
    C0a through C5. C6's own insertion count is not orderable here and is not
    ordered (§3 item 14). Those insertion numbers are ALSO required by
    docs/agents/handback_template.md in the `+/-` column of the handback's
    `## Commits` table (§3 item 28): take every cell from THIS gate's output
    and say in the handback that you did.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 3 of F040 — the round
             (12), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations, and the open-findings
             count. Then `git push -u origin feature/f040-completion-digest`.
             Create no pull request, merge nothing, force-push nothing, touch
             no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN12
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 12.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D10 | done | rounds 2-9 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | round 8, PASS |
| T002 the card's copy rules and the §17 screen | done | round 9, PASS |
| T002 the card component and its guard | done | round 11, PASS |
| T002 the storage edge (dismissal + last-seen) | done | this round |
| T002 the mount, the data load and the layout | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round extends `DigestVisibilityPort` (DECISION F040 D8) with the two
   last-seen methods D8 already names but no round had yet added, and builds
   the browser-local storage edge implementing all four — dismissal and
   last-seen, both keyed per job — pinned by a real vitest guard with a
   worktree mutation red-proof (the F256 D6 route R11 already used).
2. The next round MOUNTS the card into `RemedyShell.tsx`: `loadJobDigest`
   (paired with `jobDigestPath`, following `loadDiffEnvelope`'s shape in
   `remedyApi.ts` — `jobDigest.ts` itself may keep no fetch, per its own
   header), `latestActivityMs` read from the brain stream's `recent` ring
   buffer via `newestActionRow(...).receivedAtMs`, a real `window`-bound
   instance of this round's storage edge, and the card mounted as a sibling
   of the shell div rather than inside `<main>`, which
   `tests/ui_contracts/test_main_layout_guard.py` pins to exactly four
   children. `onOpenDecisions` and `onPrimaryAction` render but stay inert
   that round too: `JobDigestPrimaryAction` carries only `label` and
   `rule_id`, no task or decision id to focus, so wiring DECISION F040 D5's
   "in-page action using the focus mechanism F021 shipped for feed rows"
   needs its own resolution design and its own round.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- R-0756 is RESOLVED this round (RECORD12): R11 built and proved the fix,
  and this round's append is where the append-only ledger records it.
- `browserDigestPort.ts` is this repository's first localStorage-backed
  module; a real browser can refuse a write (private mode, quota) and this
  round does not guard that case — no shipped sibling establishes how this
  codebase wants a storage failure to degrade, so it is left to whichever
  round first meets it in practice rather than guessed here.
<<<END PLAN12

<<<BEGIN RECORD12
Gate: F040 R11 — T002 PART 5A/5B, THE HERO CARD COMPONENT, ITS GUARD, AND THE R-0756 REPAIR. VERDICT PASS. THIS ROUND SPANNED TWO WORKER INVOCATIONS: a prior instance landed C0a through C5 (commits `492b0835`..`0919a0f0`) and was interrupted before C6 by a process-level cause external to the protocol — `.agent/STOP` was confirmed ABSENT throughout by the session that finished the round, so the interruption is not attributed to the sentinel. That session made C6 and C7 and ran every gate; nothing in C0a-C5 was re-made. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3. TRANSPORT: recomputing sha256 over `.remedy-wt/f040-r11-block.md`, `.agent/authored/f040-r11.md` and `.agent/last_block.md` independently gives `5441e20e5da2ea72464b5e48a8bf2fe2a46efdb049e91754b082cb5342821a5f` over 31757 bytes for all three, matching the handback. THE PLAN: `.agent/plan.md` at HEAD reads byte-for-byte as the PLAN11 slice quoted in `.agent/last_block.md`, read directly rather than assumed. THE LEDGER: independently computed by script over `.agent/live_review.md` at HEAD — 317 distinct ids matching `^- R-\d+ — `, 54 distinct matching `^Done: R-\d+`, open (registered minus resolved) 263, `R-0756` present in the registered set and ABSENT from the resolved set — all four numbers match the handback exactly. THE COMPONENT: `DigestHeroCard.tsx` was read in full by the reviewer; every import, the three `styles.<name>` references against `DigestHeroCard.module.css`'s three declared classes, the single `Date.now()` at the dismiss handler, the absence of `localStorage`/`sessionStorage`/`fetch`/`XMLHttpRequest`, the `hasOwnership &&` gate and the `digestCtaText(...)` wrapping of `primary_action.label` are all present exactly as G5 of the R11 block reports. THE GUARD'S OWN RED PROOF: the reviewer independently reproduced mutation (d) — deleting the `hasOwnership && (` gate — inside a fresh disposable worktree built for this review alone (`.remedy-wt/wt-review-r11`, removed after), and got the SAME failure the handback reports: `TestOwnershipIsOmittedWhenEmpty::test_the_emptiness_check_actually_gates_the_ownership_section` red at exit 1, 24 passed, tree restored and the worktree removed, `git worktree list` back to one line. THE SIX SUITES OF G7/G8 WERE ALL INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT, not merely read from the transcript: `tests/ui_contracts/` 783 passed, 4 skipped; `tests/ui_contracts/test_digest_hero_card.py` alone 25 passed; `tests/ui_server/` 515 passed; `tests/docs/` 295 passed; `tests/cli/test_golden_path.py` 42 passed; the vitest-foundation node 4 passed with `test_vitest_passes` explicitly PASSED; the typescript node 1 passed, 73 deselected, with `test_typescript_compiles` explicitly PASSED — every figure matches the handback's own claim exactly. G2, G3 and G7's worktree-vitest repair proof (R-0756 itself) were read and cross-checked against the diff and the block's own procedure rather than independently re-executed byte-for-byte; nothing in that reading contradicts the handback and the diff each gate is anchored to (C1's plan rewrite, C4's two-test replacement) is exactly the shape each gate's claim requires. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated, the tree is clean and pushed, and the one defect this round targeted, R-0756, is repaired and proved. No new finding is raised by this review.

Done: R-0756 — RESOLVED, by the fix R11 already built and proved, recorded here because the append-only ledger could not carry `Done: R-0756` in the same append that registered it (R11's own C2). THE FIX: `apps/ui/src/api/digestCardCopy.test.ts`'s `digestStateLabel` prototype-chain test now probes `"constructor"` — the value that survives the key fold and really reaches `Object.prototype` — instead of the blind `"toString"`, and keeps `"toString"`/`"TOSTRING"` beside it in a second test stating in its own words why the fold defeats them. No production code changed; `digestCardCopy.ts` was correct before and after. PROVED at R11's G7, by the F256 D6 worktree route: the unmutated control ran 39/39 passed at real exit 0; replacing the own-property guard in the WORKTREE'S COPY of `digestCardCopy.ts` with `DIGEST_STATE_LABELS[key] ?? UNREADABLE_STATE_LABEL` turned the guard-removal probe red at real exit 1, naming the node id `digestStateLabel > does not read a state off the prototype chain` as the one that died; the restored tree returned to 39/39 at real exit 0; the primary checkout's production module was never touched. The reviewer did not re-run this worktree route independently this round (G3 above notes the reading rather than re-execution) but did independently confirm the diff that produces it (`318ebec6`) matches exactly what the fix requires. No production code is touched by this closure.
<<<END RECORD12

SPEC — `apps/ui/src/api/digestVisibility.ts` (C3, edit — the interface only)

Add exactly two method signatures to `DigestVisibilityPort`:

  readLastSeen(jobId: string): number | null;
  writeLastSeen(jobId: string, seenAtMs: number): void;

Place them after the two existing methods, inside the same interface body.
Extend the interface's own doc comment by one sentence naming that the
last-seen instant DECISION F040 D8 already assigns to browser-local storage
now flows through this same port — your own words, short. Change nothing
else in the file: `digestVisibility()`'s body, its partition tables, and
every other exported type are untouched. This is a SPEC edit, not a byte
pair; G5 parses the result rather than comparing it to fixed bytes.

SPEC — `apps/ui/src/api/browserDigestPort.ts` (C4, new file)

Write the header comment the way this feature's other API modules write
theirs: what the file is, why it exists, and its deliberate absences named
where a reader would search for them (no clock, no socket, no direct global
— constraints 7 and 8 above are exactly that list).

EXPORT one factory function, `browserDigestVisibilityPort`, taking one
parameter typed against the DOM lib's `Storage` interface (state in the
header comment which slice of it you require and why) and returning a value
satisfying `DigestVisibilityPort` (import the type from `./digestVisibility`
rather than restating its shape).

BEHAVIOUR:
  - Four keys, one per (job, concern) pair, each a pure function of the job
    id and a fixed per-concern segment — pick your own key format, document
    it in the header, and make the two concerns and any two distinct job ids
    produce four DISTINCT keys (constraint 10).
  - `readDismissal`/`readLastSeen` parse the stored string as a number and
    return it; a missing key OR a value that does not parse to a finite
    number both return `null` — an absence, never a thrown exception or a
    `NaN` (constraint 11).
  - `writeDismissal`/`writeLastSeen` store the given instant as a string
    under that pair's own key and read no clock of their own (constraint 7).

SPEC — `apps/ui/src/api/browserDigestPort.test.ts` (C5, new file)

Real vitest, this file IS collected by the runner (unlike a `.tsx`). Follow
the shape `digestVisibility.test.ts` already establishes in this directory:
`describe`/`it`/`expect` from `"vitest"`, a small fake satisfying the
`Storage` slice `browserDigestPort.ts` actually requires (a `Map`-backed
object is enough; do not import a DOM testing library, this package ships
none). Import nothing from `digestVisibility.test.ts` — a shared import
would couple two guards that should each stay readable and breakable on
their own. Cover, each as its own `it` with a name stating the property:
  - a written dismissal reads back exactly, for one job;
  - a written last-seen reads back exactly, for one job;
  - two DIFFERENT job ids' dismissals do not collide (writing one leaves the
    other's read at `null` until it is itself written);
  - a job's own dismissal and its own last-seen do not collide (writing one
    leaves the other at `null` until it is itself written);
  - reading a key that was never written answers `null`;
  - reading a key whose stored value does not parse to a finite number (a
    fake pre-seeded with a non-numeric string) answers `null` rather than
    throwing or answering `NaN` — paired with a positive control proving a
    numeric string round-trips through the SAME read path exactly.
