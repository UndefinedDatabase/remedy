── STEP T002 PART 5D / F040 — ROUND 13 ────────────────────────
Goal:        Build `loadJobDigest`, the FETCH half of the completion digest's
             client seam — paired with `jobDigestPath` and `decodeJobDigest`
             (both already built and already fully tested in `jobDigest.ts`
             and `jobDigest.test.ts`) the same way `loadDiffEnvelope` sits
             beside `diffEnvelopePath` in `remedyApi.ts` rather than inside
             the decode module `jobDigest.ts` itself, which promises in its
             own header to open no socket. Pure plumbing: no new decision,
             no new rule, real vitest colour.
Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R12 verdict) · C3 the loader · C4 its tests
             · C5 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r13.md`                (C0a, new)
               `.agent/last_block.md`                        (C0b)
               `.agent/plan.md`                               (C1)
               `.agent/live_review.md`                        (C2)
               `apps/ui/src/api/remedyApi.ts`                 (C3)
               `apps/ui/src/api/remedyApi.test.ts`            (C4)
               `.agent/handoff.md`                             (C5)
             NOTHING ELSE IS EDITED. `jobDigest.ts`, `jobDigest.test.ts`,
             `digestVisibility.ts`, `browserDigestPort.ts`,
             `DigestHeroCard.tsx`, `RemedyShell.tsx` and every file under
             `docs/roadmap/` are READ ONLY. The mount into `RemedyShell.tsx`
             is explicitly NOT this round's — PLAN13 routes it to the next
             round.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the objection in the handback. Never repair a slice.
    `loadJobDigest` and its tests are a SPEC, not a slice — the code is
    yours to write — and this constraint does not bind them; constraint 5
    below binds them instead.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5 and it is fixed. Every
    claim any slice makes about this round's own landed change rests on
    this ordering constraint and on nothing else (§3 item 20, R-0524
    carve-out).
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD13 IS APPENDED, never inserted. Measured directly rather than
    assumed: `.agent/live_review.md` at the branch tip this round opens on
    (`9da5d097`) is 1723955 bytes and does NOT end with a trailing newline —
    its last byte is the period ending R12's own verdict paragraph. The
    append is one newline followed by the slice's bytes; G3 re-measures the
    base rather than trusting this paragraph.
 5. `loadJobDigest` IS BUILT THE WAY `loadDiffEnvelope` IS BUILT, READ
    DIRECTLY FROM `remedyApi.ts` BEFORE WRITING ANYTHING, not from a
    paraphrase: same file, a `*Fetcher` type alias for `(path: string) =>
    Promise<unknown>`, the fetcher as a second parameter defaulting to the
    file's own private `fetchJson`, a `try { ... } catch { return <the
    total-absence answer> }` body that NEVER THROWS. The one difference
    `decodeJobDigest`'s own shape forces: `readDiffEnvelope` never returns
    `null` (an unavailable diff is still a total `DiffEnvelope` object), so
    `loadDiffEnvelope`'s catch calls `readDiffEnvelope(null)`; `decodeJobDigest`
    already returns `JobDigest | null` and IS the total-absence answer on a
    bad payload, so `loadJobDigest`'s catch returns `null` directly — do not
    invent a wrapper shape neither `jobDigest.ts` nor its own test file
    uses.
 6. NO PATH-BUILDING TEST IS DUPLICATED. `jobDigestPath` is already fully
    tested by `jobDigest.test.ts` (job scope, percent-encoding, `baseUrl`)
    at `9da5d097` — read that file before writing C4, and cover ONLY
    `loadJobDigest`'s OWN behaviour: it calls the fetcher with the address
    `jobDigestPath` builds, it decodes a real payload, and it degrades a
    rejected fetch and a junk body to the SAME `null` rather than throwing.
    A test that re-proves `jobDigestPath`'s own address-building here would
    be the second home for that rule the "the diff envelope door" tests
    beside it deliberately avoid.
 7. C4 IS AN APPEND TO AN EXISTING FILE, `remedyApi.test.ts`, placed as a new
    `describe` block immediately after "the diff envelope door" section
    (ending at `expect(fromArray.files).toEqual([]);\n  });\n});` at
    `9da5d097`), following that section's own comment-banner shape. No
    existing test in that file is touched, reordered or renamed.
 8. NO CLOCK, NO STORAGE. `loadJobDigest` reads no `Date.now`, no
    `localStorage`: it is a fetch-and-decode door and nothing else, the
    same posture `loadDiffEnvelope` already keeps.
 9. NO MOUNT. `RemedyShell.tsx` is not reached for even partially; PLAN13
    routes it to the next round.
10. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree`,
    removed before the handback, with `git worktree list` showing one line.
    The primary checkout satisfies `git status --porcelain` empty at every
    commit.
11. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C5. If it appears, finish the commit in hand, write the handback and
    stop.
12. `npx vitest` and `npm run test:unit` are REFUSED to this session class
    as a DIRECT shell spelling. Reach vitest through the pytest node named
    in G6, and reach the worktree mutation route of G5 through a Python
    driver's `subprocess.run`, never through a bare shell line.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C5 (§3 item 31), and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk, against the reviewer's
    own surviving original: report the sha256 and byte length of
    `.remedy-wt/f040-r13-block.md`, of `.agent/authored/f040-r13.md` and of
    `.agent/last_block.md`, and that all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN13 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length rather than
    taking it from this block. Reading (a): the base blob is a byte PREFIX
    of the committed file and base + one newline + slice reconstructs it
    whole. Reading (b), independent and structural: split the slice on
    blank lines, COUNT the paragraphs into N, and compare the committed
    file's LAST N blank-line units against those N paragraphs IN ORDER.
    Negative control: inside the disposable worktree, flip one byte in the
    FIRST appended paragraph and report that both readings REJECT it and
    both ACCEPT the unflipped bytes. N is counted by the script and never
    asserted.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids
    matching `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R12 — `. Report ADDED and REMOVED for each set and the
    open count (registered minus resolved, both distinct) before and after;
    report that no id's status changes this round.
 G5 THE LOADER'S SHAPE, ITS GUARD AND ITS RED PROOF, at C4.
    First, over `remedyApi.ts` with comments stripped and quoted literals
    blanked, in the function body of `loadJobDigest` only (its own brace
    span, not the whole file): `Date.now` and `localStorage` each occur
    zero times. Report the exported names `loadJobDigest` and
    `JobDigestFetcher` exist and that `loadJobDigest`'s default second
    parameter is the file's own `fetchJson`.
    Second, run through the pytest node named in G6 — real vitest colour is
    this round's guard, there is no `.py` text guard over this pair.
    Third, THE RED PROOF, run through a Python driver's `subprocess.run`
    (never a bare `npx vitest` shell line, per constraint 12), by the
    worktree route DECISION F256 D6 fixes (root at the PRIMARY `apps/ui`
    OR the primary's `node_modules` symlinked into the worktree per R12's
    own G7 deviation — either plumbing is acceptable, declare which):
    mutate `loadJobDigest` inside a disposable worktree, unmutated CONTROL
    first, then for EACH of these two mutations — reverting to the control
    and re-confirming its colour before the next — the real exit code and
    the node ids that DIED:
      (a) the `catch` block returns `undefined` instead of `null` (so a
          rejected fetch or a junk body is silently mis-typed);
      (b) the fetcher is called with a literal path rather than
          `jobDigestPath(request)`'s result (so a differently-shaped
          request no longer changes the address the loader reads).
    Assert each anchor is UNIQUE in the file before replacing it, and
    report the count. For each, report that the bytes on disk differ from
    the original AND that the DECLARATION differs after comment stripping.
    Restore and report byte equality to the committed file after each.
 G6 VITEST, at C4, through the pytest node and not through a bare shell
    line (constraint 12):
      python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
    Report the REAL exit code and that `test_vitest_passes` is explicitly
    PASSED, not merely inferred. Report the test count re-measured at this
    round's own base `9da5d097` and again at HEAD, and that it rose by
    exactly the number of new `it(` cases C4 adds and by zero files (C4 is
    an append to an EXISTING file, unlike R12's C5).
 G7 THE SUITES, THE TOOLCHAIN AND THE TREE, at C4:
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    Report each REAL exit code, and for the last one report PASSED or
    SKIPPED explicitly. Then report `git status --porcelain`, the count
    from `git ls-files --others --exclude-standard`, `git worktree list`,
    and the `+` column of `git diff --numstat` for each commit from C0a
    through C4. C5's own insertion count is not orderable here and is not
    ordered (§3 item 14). Those insertion numbers are ALSO required by
    docs/agents/handback_template.md in the `+/-` column of the handback's
    `## Commits` table (§3 item 28): take every cell from THIS gate's
    output and say in the handback that you did.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 3 of F040 — the round
             (13), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations, and the open-findings
             count. Then `git push -u origin feature/f040-completion-digest`.
             Create no pull request, merge nothing, force-push nothing, touch
             no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN13
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 13.

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
| T002 the storage edge (dismissal + last-seen) | done | round 12, PASS |
| T002 the fetch loader `loadJobDigest` | done | this round |
| T002 the mount into `RemedyShell.tsx` | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round builds `loadJobDigest` in `remedyApi.ts`, paired with
   `jobDigestPath`/`decodeJobDigest`, the way `loadDiffEnvelope` pairs with
   `diffEnvelopePath` — real vitest colour, no new decision.
2. The next round MOUNTS the card into `RemedyShell.tsx` (state, last-seen,
   the storage edge bound for real, `latestActivityMs` from the brain
   stream, a sibling of the shell div rather than a fifth `<main>` child,
   its own pytest text guard). `onOpenDecisions`/`onPrimaryAction` stay
   inert — no task/decision id exists yet to focus.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN13

<<<BEGIN RECORD13
Gate: F040 R12 — T002 PART 5C, THE PORT EXTENSION AND THE STORAGE EDGE. VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3. THE PORT INTERFACE: `digestVisibility.ts` was read directly at HEAD — `DigestVisibilityPort` carries exactly four methods, `readDismissal`, `writeDismissal`, `readLastSeen`, `writeLastSeen`, and `digestVisibility()`'s own function body is unchanged from the diff. THE STORAGE EDGE: `browserDigestPort.ts` was read in full — one shared `digestStorageKey(concern, jobId)` builder produces the four (job, concern) keys, `readStoredInstant`/`writeStoredInstant` are the only two callers of the injected `Pick<Storage, "getItem" | "setItem">`, `window` and `localStorage` occur zero times in its executable source, and a corrupt stored value reads as `null` rather than `NaN` or a throw. `browserDigestPort.test.ts` was read in full — eight `it` cases covering a same-job round-trip for each concern, job isolation, concern isolation, absence and a positive control for the finite-number guard. THE LEDGER: independently computed by script over `.agent/live_review.md` at HEAD — 317 distinct registered ids, 55 distinct resolved (R-0756 now among them), open 262 — matching the handback exactly. THE FOUR SUITES OF G7/G8 WERE INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT: `tests/ui_contracts/` 783 passed, 4 skipped; `tests/ui_server/` 515 passed; `tests/docs/` 295 passed; `tests/cli/test_golden_path.py` 42 passed — all match. THE RED PROOF WAS INDEPENDENTLY REPRODUCED, not merely read: the reviewer built its own disposable worktree (`.remedy-wt/wt-review-r12`, removed after), mutated the shared key builder to collapse every job id onto one fixed key, symlinked the worktree's `apps/ui/node_modules` at the primary's real one (the same plumbing the handback's Deviations item 2 declares), and ran `browserDigestVisibilityPort`'s own test file directly: REAL EXIT 1, 3 of 8 tests died — the two job-isolation cases and the positive-control case, exactly the collision the mutation should produce — then restored and re-confirmed REAL EXIT 0, 8/8. G1, G2 and the other three of G6's four mutations were read and cross-checked against the diff rather than independently re-executed byte-for-byte; nothing in that reading contradicts the handback. ONE NON-BLOCKING DEFECT IS NOTED, in the REVIEWER'S OWN AUTHORED BLOCK rather than in anything the worker built: `.remedy-wt/f040-r12-block.md`'s G2 gate text asserted PLAN12 would read "under 50" lines; the reviewer's own authored PLAN12 slice was 58 lines, and the worker correctly applied it byte-for-byte per constraint 1 and declared the false assertion in the handback rather than silently repairing either the plan or the gate. This damaged nothing on disk — the applied plan is byte-correct and complete — so per amend0827 rule 2 it spends no finding id and buys no correction round; the round 12 handback commit `9da5d097` is itself the durable record of the lesson, satisfying amend0827 rule 4's "into this handoff" clause. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated beyond the declared non-blocking gate-text error, the tree is clean and pushed. No new finding is raised by this review.
<<<END RECORD13

SPEC — `apps/ui/src/api/remedyApi.ts` (C3, edit — one new section)

Add, immediately after "the diff envelope door" section ends (after
`loadDiffEnvelope`'s closing brace), a comparable section for the digest
door: a comment banner in the same shape as the diff envelope door's own
(three-line `// ---` banner, one sentence naming the feature and task id,
one sentence on the testing shape), then:

  export type JobDigestFetcher = (path: string) => Promise<unknown>;

  export async function loadJobDigest(
    request: { jobId: string; token: string; baseUrl?: string },
    fetchPayload: JobDigestFetcher = fetchJson,
  ): Promise<JobDigest | null> {
    try {
      const payload = await fetchPayload(jobDigestPath(request));
      return decodeJobDigest(payload);
    } catch {
      return null;
    }
  }

Add the two new imports this needs — `jobDigestPath`, `decodeJobDigest` as
values and `JobDigest` as a type — from `./jobDigest`, placed with this
file's existing import block in whatever position that block's own
convention uses (read the top of the file before choosing). Write a doc
comment above `loadJobDigest` explaining, in your own words, why it never
throws and why its catch returns `null` directly rather than a total
"unavailable" object (constraint 5 states the reason; write it as this
file's own prose, not copied).

SPEC — `apps/ui/src/api/remedyApi.test.ts` (C4, edit — append one new
`describe` block)

Read "the diff envelope door" section in full at `9da5d097` before writing
this — match its shape, not its content. Import `loadJobDigest` alongside
this file's existing imports from `./remedyApi` (extend the existing import
statement; do not add a second one). Add one comment banner in the same
three-line shape naming the digest door and T5_F040 T002, then a
`describe("the job digest door", ...)` block covering exactly:
  - a request whose fetcher returns a real digest payload: `loadJobDigest`
    calls the fetcher with `jobDigestPath(request)`'s own address exactly
    once, and returns the decoded digest (assert on a couple of its actual
    fields, not just that the result is non-null — enough to prove
    `decodeJobDigest` really ran and was not bypassed);
  - a rejected fetch: `loadJobDigest` resolves to `null` rather than
    rejecting or throwing;
  - a junk body (a plain string, then an array — `decodeJobDigest`'s own
    two documented failure shapes): `loadJobDigest` resolves to `null` for
    both.
Do not re-test `jobDigestPath`'s own address-building (constraint 6) — that
belongs to `jobDigest.test.ts` and already lives there.
