── STEP T002 PART 5E / F040 — ROUND 14 ────────────────────────
Goal:        MOUNT the completion digest's hero card into `RemedyShell.tsx`:
             load the digest once per job via `loadJobDigest` (R13), bind
             the storage edge for real via `browserDigestVisibilityPort`
             (R12) against `window.localStorage`, read the last-seen instant
             ONCE before writing a fresh one, read the dismissal once and
             re-read it after the card's own write, derive `latestActivityMs`
             from the brain stream's own `recent` ring buffer, and render the
             card as a SIBLING of the shell div — never a fifth child of
             `<main>`, which `tests/ui_contracts/test_main_layout_guard.py`
             pins to exactly four. `onOpenDecisions` and `onPrimaryAction`
             stay UNWIRED this round: `JobDigestPrimaryAction` carries only
             `label` and `rule_id`, no task or decision id to focus, so
             DECISION F040 D5's "in-page action" needs its own resolution
             design before either prop has anything real to call.
Bundle:      C0a save this block verbatim · C0b mirror it · C1 the plan ·
             C2 the record (the R13 verdict) · C3 the mount · C4 its guard ·
             C5 the handback.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r14.md`                         (C0a, new)
               `.agent/last_block.md`                                 (C0b)
               `.agent/plan.md`                                       (C1)
               `.agent/live_review.md`                                (C2)
               `apps/ui/src/components/shell/RemedyShell.tsx`         (C3)
               `tests/ui_contracts/test_digest_mount.py`     (C4, new)
               `.agent/handoff.md`                                     (C5)
             NOTHING ELSE IS EDITED. `jobDigest.ts`, `remedyApi.ts`,
             `digestVisibility.ts`, `browserDigestPort.ts`,
             `DigestHeroCard.tsx`, `DigestHeroCard.module.css`,
             `RemedyShell.module.css`, `actionClass.ts`,
             `test_main_layout_guard.py`, `test_remedy_shell_stream.py` and
             every file under `docs/roadmap/` are READ ONLY.

Constraints:
 1. APPLY EVERY AUTHORED SLICE BYTE FOR BYTE. If a slice looks wrong, apply
    it anyway and DECLARE the objection in the handback. Never repair a
    slice. `RemedyShell.tsx`'s new lines and the new guard file are a SPEC,
    not a slice — the code is yours to write — and this constraint does not
    bind them; constraints 5-11 below bind them instead.
 2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5 and it is fixed. Every
    claim any slice makes about this round's own landed change rests on
    this ordering constraint and on nothing else (§3 item 20, R-0524
    carve-out).
 3. C1 IS THE FIRST SUBSTANTIVE COMMIT (§3 item 23): the round moves the
    finding ledger, so `.agent/plan.md` is current before the ledger is
    touched.
 4. RECORD14 IS APPENDED, never inserted. Measured directly rather than
    assumed: `.agent/live_review.md` at the branch tip this round opens on
    (`24f5d155`) is 1727340 bytes and does NOT end with a trailing newline —
    its last byte is the period ending R13's own verdict paragraph. The
    append is one newline followed by the slice's bytes; G3 re-measures the
    base rather than trusting this paragraph. READING (b)'S WORDING IS
    CORRECTED THIS ROUND (R13's own G3 finding, carried in RECORD14 below):
    a single-newline join fuses the base's own last paragraph with the
    slice's first one, so ONLY THE LAST of the N blank-line units may be
    checked by raw equality; every earlier one of the N is checked by
    SUFFIX match. G3 states this precisely; do not use R11's or R12's
    equality-only wording.
 5. `RemedyShell.tsx`'s NEW LINES, IN SOURCE ORDER, MUST BE:
    (i) the digest load — a `useState<JobDigest | null>(null)` paired with a
        `useEffect` keyed on `[dashboard.jobId, serverToken]` that calls
        `loadJobDigest({ jobId: dashboard.jobId, token: serverToken })` and
        stores the result behind the SAME `cancelled` idiom the diff
        envelope effect two lines above already uses (constraint 7);
    (ii) the storage edge — ONE call to `browserDigestVisibilityPort(` with
         `window.localStorage` as its argument, bound to a local named
         `digestPort`, placed AFTER (i) and BEFORE (iii) and (iv), which
         both read it;
    (iii) the last-seen read-then-write pair — a `useState<number | null>`
          whose LAZY INITIALIZER calls `digestPort.readLastSeen(dashboard.jobId)`,
          followed by a `useEffect` keyed on `[dashboard.jobId]` alone whose
          ENTIRE body is one call to `digestPort.writeLastSeen(dashboard.jobId,
          Date.now())`. The read must appear BEFORE the write in SOURCE
          ORDER — G5 checks this by string position, not by React's own
          runtime order, because the guard cannot run React;
    (iv) the dismissal read — a `useState<DigestDismissal>` (import the type
         from `../../api/digestVisibility`) whose LAZY INITIALIZER calls
         `digestPort.readDismissal(dashboard.jobId)`;
    (v) `latestActivityMs`, a plain `const`, computed as
        `newestActionRow(stream.recent ?? [])?.receivedAtMs ?? null`,
        importing `newestActionRow` from `../../api/actionClass`;
    (vi) the visibility computation, a plain `const` calling
         `digestVisibility({ digest, lastSeenMs, dismissedAtMs,
         latestActivityMs, nowMs: Date.now() })`, the file's ONLY
         `Date.now()` call outside `writeLastSeen`'s own argument in (iii)
         — this is the mount's OWN clock read, the edge DECISION F040 D8
         and R11's constraint 7 both name, and it is not the SAME read as
         (iii)'s: two separate `Date.now()` calls, one per concern, never
         one value reused for both.
 6. THE CARD RENDERS AS THE FIRST CHILD OF `<div className={styles.viewport}>`,
    immediately after `<DegradedBanner .../>` and BEFORE the
    `<div className={`${styles.shell}` ...}>` that opens `<main>`. It is
    conditioned on `digest !== null` (never on `visibility.show` directly —
    the card itself already branches on that per its own constraint 6 from
    R11), and its `onDismissed` callback RE-READS the port
    (`() => setDismissedAtMs(digestPort.readDismissal(dashboard.jobId))`)
    rather than duplicating the card's own `Date.now()` read. `onOpenDecisions`
    and `onPrimaryAction` are NOT PASSED AT ALL — the props are optional
    (R11's own `DigestHeroCardProps`) and omitting them is how "unwired"
    reads, rather than passing an explicit no-op arrow function that would
    misstate a decision as made.
 7. THE DIGEST-LOAD EFFECT NEVER CLEARS `digest` TO `null` ON RE-RUN, UNLIKE
    THE DIFF-ENVELOPE EFFECT ABOVE IT. Declare this asymmetry in the new
    file's own header/inline comment rather than silently diverging from
    the sibling pattern: the diff effect clears because the SAME mount
    re-opens DIFFERENT task ids repeatedly across one session, and a stale
    diff under a new task's name would be a wrong answer; `dashboard.jobId`
    and `serverToken` are effectively stable for the whole life of one
    mounted shell (a job's page does not swap jobs under the operator), so
    there is no repeated re-selection this effect needs to guard against.
    The `cancelled` guard is kept regardless, because a slow first request
    racing a token refresh is still possible even if rare.
 8. NO NEW CAPABILITY IS ADDED TO THE SHELL BEYOND WHAT THIS SPEC NAMES.
    `RemedyShell.tsx` calls no `fetch` and no `XMLHttpRequest` directly
    today (it goes through `loadDiffEnvelope`/`useBrainStream`'s own doors)
    and this round keeps that true — `loadJobDigest` is the same kind of
    door. `window.localStorage` occurs EXACTLY ONCE in the new lines — the
    single `browserDigestVisibilityPort(window.localStorage)` call — never
    a second direct read or write of `localStorage` anywhere else in the
    file.
 9. `<main>` GAINS NO FIFTH CHILD. `tests/ui_contracts/test_main_layout_guard.py`
    parses `<main className={styles.main}>...</main>` and asserts exactly
    four children; the new card markup must not appear inside that span.
    G5 proves this by the SAME extraction regex that guard uses, not by a
    weaker substring check.
10. DESTRUCTIVE VERIFICATION ONLY INSIDE A DISPOSABLE `git worktree` WHERE
    ANY IS NEEDED, removed before the handback, with `git worktree list`
    showing one line. The primary checkout satisfies `git status
    --porcelain` empty at every commit. (This round's own guard, C4, is a
    pytest text guard with no vitest/tsc mutation route of its own — G6
    runs it directly in the primary checkout, the way R11's G6 ran
    `test_digest_hero_card.py`; a worktree is needed only for G3's negative
    control.)
11. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN BEFORE
    C5. If it appears, finish the commit in hand, write the handback and
    stop.
12. `npx vitest` and `npm run test:unit` are REFUSED to this session class
    as a DIRECT shell spelling. Reach vitest and tsc only through the
    pytest nodes named in G7.

Done when: every gate below is executed, each with its REAL exit code taken
from `subprocess.run(...).returncode`. All of them run at commits strictly
earlier than C5 (§3 item 31), and the commit each runs at is named below.

 G1 TRANSPORT, at C0b. ONE comparison, disk to disk, against the reviewer's
    own surviving original: report the sha256 and byte length of
    `.remedy-wt/f040-r14-block.md`, of `.agent/authored/f040-r14.md` and of
    `.agent/last_block.md`, and that all three are equal.
 G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to the PLAN14 slice; report
    its line count and that it is under 50; report that it holds `## Goal`,
    `## Next Steps` and a string matching `\bF\d{3}\b`.
 G3 THE RECORD APPEND, at C2, WITH THE CORRECTED READING (b). Re-measure the
    pre-commit length rather than taking it from this block. Reading (a):
    the base blob is a byte PREFIX of the committed file and base + one
    newline + slice reconstructs it whole. Reading (b), independent and
    structural: split the slice on blank lines into N paragraphs (N counted
    by the script, never asserted); the committed file's LAST blank-line
    unit equals paragraph N by RAW EQUALITY; each EARLIER paragraph 1..N-1,
    if any, is checked by asking whether SOME blank-line unit of the
    committed file ENDS WITH that paragraph, in order. Negative control:
    inside the disposable worktree, flip one byte in the LAST appended
    paragraph and report that both readings REJECT it and both ACCEPT the
    unflipped bytes — the last paragraph is chosen for the control because
    it is the one BOTH readings check by an equality-shaped comparison.
 G4 THE LEDGER, at C2. Compute by DIFFERENCE between the pre-commit base and
    the committed file, never by reading the slice: the distinct ids
    matching `^- R-\d+ — `, those matching `^Done: R-\d+`, those matching
    `DECISION F040 D\d+`, and the count of lines matching
    `^Gate: F040 R13 — `. Report ADDED and REMOVED for each set and the
    open count (registered minus resolved, both distinct) before and after;
    report that no id's status changes this round.
 G5 THE MOUNT'S SHAPE, at C3. Over `RemedyShell.tsx` with comments stripped:
    report, IN SOURCE-POSITION ORDER, the string offset of each of: the
    `useEffect` calling `loadJobDigest(`; the `browserDigestVisibilityPort(`
    call; the lazy-initializer call to `digestPort.readLastSeen(`; the
    `useEffect` whose body calls `digestPort.writeLastSeen(`; the
    lazy-initializer call to `digestPort.readDismissal(`; the
    `newestActionRow(` call; the `digestVisibility({` call — and that these
    seven offsets are STRICTLY INCREASING except where constraint 5 allows
    tied ordering, matching the (i)-(vi) sequence exactly. Report that
    `Date.now()` occurs exactly twice in the new lines, once inside
    `writeLastSeen(...)`'s own argument and once inside the
    `digestVisibility({...})` call's `nowMs` field, and that neither
    duplicates the other's own call expression by exact substring
    (constraint 5(vi)). Report that `window.localStorage` occurs exactly
    once. Extract `<main className={styles.main}>...</main>` with the SAME
    regex `tests/ui_contracts/test_main_layout_guard.py` uses and report
    that `DigestHeroCard` does not occur inside that span but DOES occur
    exactly once outside it, as a direct child of
    `<div className={styles.viewport}>` preceding the shell's own opening
    div (report the three tags' relative order by offset). Report that
    `onOpenDecisions` and `onPrimaryAction` do not occur anywhere in the
    file (constraint 6's omission, not a no-op).
 G6 THE GUARD'S OWN RUN AND ITS RED PROOF, at C4. First,
    `python3 -m pytest tests/ui_contracts/test_digest_mount.py -q` in the
    primary checkout, real exit code. Second, THE RED PROOF, over a SCRATCH
    COPY of `RemedyShell.tsx` inside a disposable worktree (no vitest is
    involved; this guard needs no `node_modules`), for EACH of these five
    mutations — reverting to the control and re-confirming green before the
    next:
      (a) move the digest card's JSX from before the shell div to AFTER it,
          nested one level deeper so it lands INSIDE `<main>`'s own span as
          a fifth child;
      (b) swap the order of the last-seen read and its write effect, so the
          write appears in source BEFORE the read;
      (c) delete `window.localStorage` from the `browserDigestVisibilityPort(`
          call, leaving it called with no argument;
      (d) change `onDismissed`'s callback to set a hard-coded instant
          instead of re-reading `digestPort.readDismissal(dashboard.jobId)`;
      (e) add a literal `onPrimaryAction={() => {}}` prop to the card.
    Assert each anchor is UNIQUE before replacing it, and report the count.
    For each, report the guard's real exit code (must be 1) and the node
    ids that FAILED. Restore and report byte equality to the committed
    file, and the guard green again, after each.
 G7 THE SUITES, THE TOOLCHAIN AND THE TREE, at C4:
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
      python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
      python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    Report each REAL exit code, and for the last two report PASSED or
    SKIPPED explicitly — the typescript node is this round's ONLY proof
    that the new `.tsx` lines actually type-check (`Storage`,
    `DigestVisibilityPort`, `JobDigest | null` all satisfied), since no
    vitest test renders this file. Then report `git status --porcelain`,
    the count from `git ls-files --others --exclude-standard`, `git
    worktree list`, and the `+` column of `git diff --numstat` for each
    commit from C0a through C4. C5's own insertion count is not orderable
    here and is not ordered (§3 item 14). Those insertion numbers are ALSO
    required by docs/agents/handback_template.md in the `+/-` column of the
    handback's `## Commits` table (§3 item 28): take every cell from THIS
    gate's output and say in the handback that you did.

Handback:    rewrite `.agent/handoff.md` per docs/agents/handback_template.md.
             Carry the SESSION NUMBER — this is SESSION 3 of F040 — the round
             (14), the range, the per-commit table with the `+/-` column from
             `git diff --numstat`, one line per gate with its REAL exit code,
             the item-status table, the deviations, and the open-findings
             count. Then `git push -u origin feature/f040-completion-digest`.
             Create no pull request, merge nothing, force-push nothing, touch
             no branch.
──────────────────────────────────────────────────────────────

<<<BEGIN PLAN14
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 3, round 14.

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
| T002 the fetch loader `loadJobDigest` | done | round 13, PASS |
| T002 the mount into `RemedyShell.tsx` | done | this round |
| T003 CLI parity and the end-to-end | open | next |

## Next Steps
1. This round mounts the card for real: the load, the storage edge bound to
   `window.localStorage`, last-seen and dismissal wiring, and placement as
   a sibling of the shell div — `<main>` stays at exactly four children.
   `onOpenDecisions`/`onPrimaryAction` stay unwired.
2. The next round is T003: `remedy job digest <id>` CLI parity, then the
   end-to-end (finish a fake job while the UI is "away", reopen, hero shows
   the right CTA, dismiss, no re-show), the integration gate and closure.
3. Wiring `onOpenDecisions`/`onPrimaryAction` for real needs its own
   resolution design (D5's "in-page action") and is not yet scheduled.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch;
  none is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- `browserDigestPort.ts`'s open risk (a real browser refusing a write) is
  still unaddressed and still deferred to whichever round first meets it.
<<<END PLAN14

<<<BEGIN RECORD14
Gate: F040 R13 — T002 PART 5D, THE FETCH LOADER `loadJobDigest`. VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, per docs/agents/self_drive_protocol.md Phase 2 step 3. THE LOADER: `remedyApi.ts` was read in full at HEAD — `loadJobDigest` sits directly after `loadDiffEnvelope`, imports `jobDigestPath`/`decodeJobDigest`/`JobDigest` from `./jobDigest`, defaults its fetcher to the file's own private `fetchJson`, and its catch returns `null` directly rather than a wrapped shape, exactly as ordered. `remedyApi.test.ts` was read in full — the new "the job digest door" block covers a real decoded payload (asserting on `state` and `primary_action`, not merely non-null), a rejected fetch, and two junk-body shapes, without re-testing `jobDigestPath`'s own address-building, which stays in `jobDigest.test.ts` alone. THE LEDGER: independently computed by script over `.agent/live_review.md` at HEAD — 317 distinct registered, 55 distinct resolved, open 262, one `^Gate: F040 R12 — ` line — matching the handback exactly. THE FOUR SUITES OF G7 WERE INDEPENDENTLY RE-RUN BY THE REVIEWER IN THE PRIMARY CHECKOUT: `tests/ui_contracts/` 783 passed, 4 skipped; `tests/ui_server/` 515 passed; `tests/docs/` 295 passed; `tests/cli/test_golden_path.py` 42 passed — all match. THE RED PROOF WAS INDEPENDENTLY REPRODUCED: the reviewer built its own disposable worktree (`.remedy-wt/wt-review-r13`, removed after), symlinked the primary's `node_modules` the same way the handback declares, ran the unmutated control (67/67 passed), mutated the catch block to return `undefined` instead of `null`, and got the SAME single failure the handback reports — `the job digest door > degrades a rejected fetch to null rather than throwing` — then restored and re-confirmed 67/67. G1, G2, G4 and mutation (b) were read and cross-checked against the diff rather than independently re-executed; nothing in that reading contradicts the handback. TWO DEVIATIONS THE WORKER DECLARED ARE BOTH GENUINE, CORRECT CATCHES, NEITHER A DEFECT ON DISK. FIRST, `git commit`'s own console summary for C1 (44 insertions, 58 deletions) disagreed with `git diff --numstat` for the identical commit pair (14, 28); the worker traced this to git's own rename/rewrite-detection heuristic substituting whole-file line counts once a file's changed fraction crosses its similarity threshold, verified the numstat figure independently with `difflib`, and reported 14/28 as G7 orders — correct, and consistent with the general rule (recorded elsewhere in this project) that a full-file rewrite is where a commit's own prose summary and `--numstat`'s real count diverge. SECOND, AND MORE SIGNIFICANT: the worker found that G3 reading (b)'s WORDING, carried forward verbatim from round to round including THIS reviewer's own R12 block, is imprecise wherever N includes more than the single final paragraph — because constraint 4 joins the base and the slice with ONE newline rather than a blank line, the base's own last pre-existing paragraph and the slice's FIRST paragraph fuse into a single blank-line unit, so raw equality holds for the LAST of the N paragraphs but only a SUFFIX match holds for any EARLIER one. The worker proved this by re-deriving the identical check against R12's own committed ledger append and finding the same fused-first-unit shape there, undeclared at the time. This damaged nothing on either round's actual bytes — reading (a)'s prefix-and-reconstruction check is airtight on its own and was never in question — so per amend0827 rule 2 it spends no finding id and buys no correction round. THE FIX IS APPLIED STARTING THIS ROUND: this block's own G3 above states reading (b) with the corrected suffix-for-earlier-paragraphs, equality-for-the-last semantics, and its negative control is chosen from the LAST paragraph specifically because that is the one both readings check by an equality-shaped comparison. THE ROUND PASSES: every path in the change set matches the block's order, no constraint is violated, the tree is clean and pushed. No new finding is raised by this review; both declared items are prose-precision corrections to the REVIEWER'S OWN gate template, already durably recorded in the R13 handback commit `24f5d155` per amend0827 rule 4's "into this handoff" clause.
<<<END RECORD14

SPEC — `apps/ui/src/components/shell/RemedyShell.tsx` (C3, edit)

Read the WHOLE file at `24f5d155` before writing anything — every anchor
below is a real line in it today. This is a SPEC: the exact wording of
comments and the exact variable layout are yours, but the ORDER, the calls,
and the placement are fixed by constraints 5, 6, 7, 8 and 9 above, which
G5 checks structurally rather than by any fixed byte pair.

IMPORTS: extend the existing `import { loadDiffEnvelope } from
"../../api/remedyApi";` line to also import `loadJobDigest` (one import
statement, not two). Add new imports for: `JobDigest` (type) from
`../../api/jobDigest`; `digestVisibility` (value) and `DigestVisibilityPort`,
`DigestDismissal` (types) from `../../api/digestVisibility` — you only need
`DigestDismissal`, but check whether the file already needs
`DigestVisibilityPort` named for the `digestPort` local's own type inference
before importing a type you do not use; `newestActionRow` (value) from
`../../api/actionClass`; `browserDigestVisibilityPort` (value) from
`../../api/browserDigestPort`; `DigestHeroCard` (value) from
`../digest/DigestHeroCard`.

BODY: place the six pieces constraint 5(i)-(vi) orders, in that order,
after the existing diff-envelope effect (which ends at the line
`}, [openDiffTaskId, dashboard.jobId, serverToken]);`) and before
`handleJump`. Write a short WHY comment above (ii) explaining the "bound
HERE because this is the edge" reasoning constraint 5 states, and one above
(i) or nearby stating constraint 7's clearing asymmetry with the diff
envelope effect, in your own words.

JSX: constraint 6 fixes the card's exact position, its condition, its
`onDismissed` wiring, and that `onOpenDecisions`/`onPrimaryAction` are
omitted entirely.

SPEC — `tests/ui_contracts/test_digest_mount.py` (C4, new file)

Follow the shape `tests/ui_contracts/test_remedy_shell_stream.py` and
`tests/ui_contracts/test_main_layout_guard.py` already establish over this
SAME file at `24f5d155` — read both before writing this, they are your two
closest siblings. Comment-stripped source, exact-substring pins for the
calls constraint 5 names (do not retype whole call expressions if a shorter
unique anchor proves the same fact — but every anchor must be checked
UNIQUE, the way `test_digest_hero_card.py`'s own helpers do), the
`<main>`-extraction check of G5 reusing the SAME regex
`test_main_layout_guard.py` uses (import it or reproduce it byte-for-byte —
your call, document which and why), and a
`TestTheStrippersReallyStrip`-shaped class if this file's own comment
stripper is not shared from an existing sibling module (read whether one is
importable before writing a fourth copy of the same twelve lines). Cover
every property constraint 5, 6, 8 and 9 states, each with its own
discriminator, matching the five mutations G6 above orders — a test file
that cannot fail against all five mutations is not this round's guard, it
is a guess that happens to read green.
