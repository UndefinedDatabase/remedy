── STEP T003/8 — F008 SSE event stream — ROUND 32 ────────────────────────────
Round base — the SHA every range gate in this block measures from: cbf6de37
 (R31's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R31 verdict — PASS, every gate re-run by the reviewer out of the
 committed blobs, including its red control in the reviewer's own worktree —
 and bind the injected environment to real globals: `browserBrainStreamEnv`,
 the last piece between `createBrainStreamHostDeps` and a browser. Wiring the
 cockpit to it is NOT in this round; it is R33, and DECISION F008 D3 below
 records where that wiring will land and why it moved.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r32.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R32, applied whole
 C2   `.agent/decisions.md` <- DECISION3, appended
 C3   `.agent/live_review.md` <- LEDGER32, appended
 C4   `apps/ui/src/api/brainStreamDeps.ts` <- ENV, appended
 C5   `apps/ui/src/api/brainStreamDeps.test.ts` <- TI1 and TI2 applied as
      one-line REWRITES, then ENVTEST appended — all three in this ONE commit
 C6   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r32.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/decisions.md`, `.agent/live_review.md`,
 `apps/ui/src/api/brainStreamDeps.ts`,
 `apps/ui/src/api/brainStreamDeps.test.ts`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r32.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r32.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, and every
 count this block orders over a slice is taken over those newline-INCLUDED
 bytes. NO slice begins with a blank line: each append's remainder is a newline
 PLUS the slice, which is what puts exactly one blank line between the file's
 last existing line and the new text (the F008 R29 DECISION2 lesson, where a
 slice that carried its own leading blank line landed two).

Pair shape (§3 item 15). Each line below is the OUTPUT of the reviewer's
containment test over the final newline-INCLUDED bytes; the label is derived
from that output beside it and is never written on its own (R-0522):
 TI1FROM/TI1TO          TO contains FROM: false  -> REWRITE
 TI2FROM/TI2TO          TO contains FROM: false  -> REWRITE
 Both read as an append by eye — each TO widens an import list the FROM already
 holds — and neither is one, because each FROM is newline-TERMINATED while its
 TO adds a name INSIDE the braces on that same line. G8 therefore orders the
 FROM-0x / TO-1x count a rewrite owes for each.
 FROM uniqueness, counted by the reviewer's own script IN the named file at the
 round base and reported as its output (item 25): TI1FROM occurs 1x and
 TI2FROM occurs 1x in `apps/ui/src/api/brainStreamDeps.test.ts`.
 ENV, ENVTEST, DECISION3 and LEDGER32 are appends and PLANF008R32 is a
 whole-file write, so none of them is a pair and none carries a containment
 reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23). C4 precedes C5 so the
    exported names land before the suite that imports them.
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED:
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened. ENV
    adds no import line: it uses `BrainStreamSource` and `BrainStreamEnv`,
    which `apps/ui/src/api/brainStreamDeps.ts` already imports and declares at
    the round base.
 4. NO FINDING ID IS MINTED: R-0630 stays free. The reviewer re-ran every gate
    R31 ordered and found no defect, so this round registers none. R-0368,
    R-0429, R-0553, R-0622, R-0628 and R-0629 stay OPEN and none is resolved
    here: write no `Done:` and no `Landed:` line for any of them.
 5. END EVERY COMMIT MESSAGE of this round with the trailer line
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, preceded by a
    blank line. R31 declared, and the reviewer confirmed by its own reading,
    that 0 of that round's 7 commits carried it; this constraint is that
    deviation's counter-measure, and G12 measures the result. Never repair a
    missing trailer by amending — protocol G2 forbids it and G11 gates it at 0.
 6. The post-C6 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 7. Two test processes never run at once, and G9's suites run in the PRIMARY
    checkout (R-0518). G10's red control is the ONLY destructive check and runs
    in a disposable worktree, never in the primary checkout (protocol G5).
 8. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    reviewer's Phase 0 probe and nothing since has created one.
 9. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there; commit nothing
    from it. Never `cd` into a worktree and leave the shell there — a later
    gate then silently measures the wrong tree (R-0463).
 10. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553). Any handback
    sentence stating "every", "no", "all" or "none" over commits, files or
    rounds names the command that produced the number. State the particular
    you measured, or nothing.
 11. THE HANDBACK'S `## Next` SECTION states, in this order: that the next
    session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
    its SECOND the Open PR Gate (Phase 1 rule 2); that R32 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0622, R-0628 and
    R-0629 are OPEN; and that R33's work is the cockpit wiring DECISION F008 D3
    fixes — `useBrainStream` called in `RemedyShell` over
    `createBrainStreamHostDeps` and `browserBrainStreamEnv`, its status passed
    to `RightLivePanel` as `streamStatus`, gated by a new source contract under
    `tests/ui_contracts/`.

The reviewer's OWN readings, each produced by RUNNING the tool at the round base
`cbf6de37`, serially, not recalled (R-0625): the five-target state reader plus
canary EXITS 0 at 465 passed and 0 skipped, in the PRIMARY checkout; `python3 -m
pytest tests/ui_contracts/ -q -rf` EXITS 0 at 409 passed plus 4 skipped = 413;
and in `apps/ui`, `npm run --silent typecheck` EXITS 0 with NO output while `npx
vitest run` EXITS 0 at 10 files and 149 tests. `npm run lint` is RED at base,
which is R-0622 and NOT a gate (R-0364). The reviewer also applied ENV, TI1, TI2
and ENVTEST in a disposable worktree at `cbf6de37` with `apps/ui/node_modules`
SYMLINKED and measured the values G9 orders there before ordering them.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2, C3, C4 and C5. Per constraint 6 the post-C6
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r32.md`
     as received, of `.agent/authored/f008-r32.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r32.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, that none carries trailing whitespace on any line, and that
     none begins with a blank line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R32. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The append at C2. Report that the round-base blob of
     `.agent/decisions.md`, read with `git show cbf6de37:.agent/decisions.md`
     into scratch or memory and never over the tracked file (item 29), is a
     byte-exact PREFIX of the C2 blob and that the remainder equals a newline
     plus DECISION3 — report its sha256 prefix, bytes and lines. Report also
     that `^## DECISION F008 D3` is line-anchored 0 at the base and 1 at C2,
     and that `^## DECISION F008 D2` and `^## DECISION F008 D1` each read 1 at
     BOTH, so this append moved neither.
 G6  The append at C3, against the round base, two ways that must agree.
     (a) the base blob of `.agent/live_review.md` is a byte-exact PREFIX of the
     C3 blob and the remainder equals a newline plus LEDGER32 — report its
     sha256 prefix, bytes and lines; (b) an INDEPENDENT blank-line split of the
     WHOLE C3 file, its terminating newline normalised first, has LEDGER32's
     paragraph as its LAST unit. NEGATIVE CONTROL: flip one PRINTABLE ASCII
     byte of the remainder to another printable one; BOTH readings must reject
     it and both accept the unflipped.
 G7  The sets in `.agent/live_review.md`, line-anchored, each reported at the
     round base AND at C3: `^- R-\d+ — ` reads 201 at both — this round mints
     no id — `^- R-0630 — ` 0 at both, `^- R-0429 — `, `^- R-0553 — `,
     `^- R-0629 — `, `^- R-0628 — ` and `^- R-0368 — ` 1 each at both,
     `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both, and `^Gate: R\d+ — `
     31 at the base and 32 at C3, over that many DISTINCT keys. HEADER SWEEP at
     C3 (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of each non-match to its first period,
     and that the R32 pair occurs EXACTLY ONCE.
 G8  The two source edits.
     (a) C4 is a pure APPEND: the round-base blob of
     `apps/ui/src/api/brainStreamDeps.ts` is a byte-exact PREFIX of the C4
     blob, the remainder equals a newline plus ENV, and the lines that commit's
     diff ADDS are exactly the remainder's lines IN ORDER — the ordered-equality
     a code append owes, never a per-line count (R-0531).
     (b) C5 is two REWRITES plus an append, in one commit. Report TI1FROM 1 at
     the base and 0 at C5 with TI1TO 0 then 1, and TI2FROM 1 then 0 with TI2TO
     0 then 1 — the FROM-0x / TO-1x count each rewrite owes. Then report that
     the base blob with BOTH substitutions applied, each ONCE, is a byte-exact
     PREFIX of the C5 blob and that the remainder equals a newline plus
     ENVTEST, with its sha256 prefix, bytes and lines.
 G9  The runs, in the PRIMARY checkout, SERIALLY, never two test processes
     alive at once, AT C5 — the commit at which both source files are final.
     In `apps/ui`: `npm run --silent typecheck` EXITS 0 with NO output, and
     `npx vitest run` EXITS 0 at 10 files and 152 tests, where the base reading
     stated above is 10 and 149. From the repository root:
     `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at a passed-plus-
     skipped SUM of 413, and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     EXITS 0 at 465. Report each pytest suite's passed and skipped numbers
     SEPARATELY as well as their sum. THE SUM IS THE GATE and a bare passed
     count is not: the reviewer measured `tests/ui_contracts/` at 409 passed
     plus 4 skipped at the base and at 408 plus 5 in its own worktree with this
     round's slices applied, the same 413 both times, because three
     data-dependent `pytest.skip(...)` calls move the split run to run. If any
     of the four fails, report the real values and STOP.
 G10 The red control, at C5, in a DISPOSABLE worktree with
     `apps/ui/node_modules` SYMLINKED into it — never copied, and never the
     primary checkout. In that worktree's `apps/ui/src/api/brainStreamDeps.ts`
     the newline-terminated byte string, six leading spaces included,
     `      if (!response.ok) throw new Error(\`Request failed ${response.status}: ${path}\`);`
     occurs EXACTLY ONCE; report that count FIRST. DELETE that one line and
     report that, run from that worktree's `apps/ui`,
     `npx vitest run src/api/brainStreamDeps.test.ts` EXITS 1 failing exactly
     one test and no other:
     `the browser environment > parses a successful body and refuses a failed status`.
     Then restore the file, report it byte-identical by sha256, and report the
     same command EXITING 0 at 15 passed. Remove the worktree and report
     `git worktree list` naming only the primary checkout.
 G11 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only cbf6de37..C5` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly, with none on either side
     alone; the full reading to C6 belongs to the ROUND REPORT (constraint 6).
     Walk `git rev-list --reverse cbf6de37..C5` and report ONE reading per
     commit: that it has exactly ONE parent, and BOTH numstat cells per path
     from `git show --numstat`, cross-checked against `git diff --numstat`,
     every insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (item 28). C6's own numbers cannot exist
     while C6 is being written, so they belong to the round report (item 14).
     Report also this round's own reflog entries, classified by the OPERATION
     before the first `:` in `%gs`: every pre-C6 entry reads `commit`; give how
     many you classified and `amend`, `rebase` and `cherry` at 0. Assert no
     total over the whole reflog (R-0601).
 G12 Marker leak and trailer. Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in the plan at C1, the decisions file at C2, the ledger at C3,
     each source file at C4 and C5, and the handback at C6 — each is 0.
     `.agent/last_block.md` is NOT in that list and is not expected to be 0,
     being the block's own mirror. Then measure constraint 5 with
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) cbf6de37..HEAD`
     before C6 and report how many commits it lists and how many return a
     NON-EMPTY value — state it as that measurement and never as a universal.
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 11
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2, C3, C4, C5 and C6 — "exactly one row" scoping to
     that TABLE. Measure its line count with `wc -l` BEFORE committing it; this
     round's commit count is above five, so the cap is 100, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; raw transcripts
     go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~99 % (T001 ✅ · T002 ✅ · T003 Client ✅ + Badge ✅ + Deps-Factory ✅ + Browser-Env ✅, Cockpit-Wiring offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R32
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R32 records the R31 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — and binds the injected environment to real globals with
`browserBrainStreamEnv`, the last piece between the factory R31 built and a
browser. A runtime with no EventSource yields a null source, which is the
`unsupported` the polling fallback engages on, so the cockpit degrades to
DELAYED instead of claiming a liveness it does not have.

## Next Steps
1. R33 wires the cockpit: `useBrainStream` called in `RemedyShell` over
   `createBrainStreamHostDeps` and `browserBrainStreamEnv`, its status passed
   to `RightLivePanel` as `streamStatus`, gated by a new source contract under
   `tests/ui_contracts/`. DECISION F008 D3 records why the call sits in the
   shell rather than in `RemedyApp`.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
- `RemedyShell` renders every cockpit surface, so R33's blast radius is the
  widest of any round since R4 even after DECISION F008 D3 narrowed it.
<<<END PLANF008R32

<<<SLICE DECISION3
## DECISION F008 D3 — the cockpit subscribes in RemedyShell, not RemedyApp

Chosen: `useBrainStream` is called in `RemedyShell` with `dashboard.jobId`.

Alternatives considered. (a) Call it in `RemedyApp`, as `.agent/plan.md` said
from R30 until this round. `RemedyApp` reads its job id from the URL and returns
an error screen when that id is empty, but a React hook cannot be called
conditionally, so the stream would open against `/api/jobs//events/stream`
whenever the URL carried no job — a request the server answers 404 and a
reconnect loop the badge would then report. (b) Pass the id down and subscribe
lower still, in `RightLivePanel`: rejected because the panel is a presentation
surface and the status already reaches it as a prop.

`RemedyShell` renders only after `RemedyApp` has loaded a dashboard, so
`dashboard.jobId` is a job the server has already answered for. The seam
`RightLivePanel` gained at R29 — an optional `streamStatus` — is unchanged by
this choice, and `RemedyApp.tsx` is not touched at all, which is the narrowest
blast radius of the three.

The feature file names no call site, so this decides an implementation question
rather than amending a spec. Reverse it by moving the call and passing the id
down; nothing else in the client depends on where the hook is called.
<<<END DECISION3

<<<SLICE LEDGER32
Gate: R32 — the R31 entry. R31 PASSED. It recorded the R30 verdict and built the real `BrainStreamHostDeps` factory over the T001 and T002 endpoints, and EVERY GATE WAS RE-RUN BY THE REVIEWER — the suites in the primary checkout and the red control in the reviewer's OWN disposable worktree — rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r31.md` as it survived on disk, `.agent/authored/f008-r31.md` at `4a724c10` and `.agent/last_block.md` at `beed4c72` are all sha256 593db9c3e879fc38954ec1d7663be727da612fb0ae4ae6216a72804c792a2e8d over 28969 bytes and 473 lines, EQUAL to the digest the reviewer emitted, and 473 is under the 490-line budget DECISION F085 D6 rules. FOUR SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R31 c6c09ffb at 39 lines, DEPS 0caa5b23 at 98, DEPSTEST 46a577b2 at 122 and the single-line LEDGER31 554fa860 — none carrying trailing whitespace on any line and each newline-terminated. THE PLAN LANDED FIRST at `db48dde8`, byte-equal to PLANF008R31 at 39 lines under the 50-line cap, with `## Goal` and `## Next Steps` once each line-anchored and `F008` matching. THE APPEND at `3d0f4f3d` is proved twice over: the round-base blob (5d29ff66, 503971 bytes, 1114 lines) is a byte-exact PREFIX of the C2 blob (218459ab, 507341 bytes, 1116 lines) with a 3370-byte remainder equal to a newline plus LEDGER31, and, independently, a blank-line split of the whole file gives 242 units whose LAST is LEDGER31's paragraph — with a one-byte printable flip at remainder offset 1 REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD — 201 findings at the round base and at C2 with NO id minted and R-0630 still 0, `- R-0429`, `- R-0553`, `- R-0629`, `- R-0628` and `- R-0368` 1 each at both and all OPEN, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 30 at the base and 31 at C2 over that many DISTINCT keys, 30 of 31 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R31 pair occurring exactly once. BOTH NEW MODULES ARE CREATIONS, NOT EDITS: `git ls-tree 82e30bb5` printed nothing for either path, and `apps/ui/src/api/brainStreamDeps.ts` at `e0174c84` is BYTE-EQUAL to DEPS while `apps/ui/src/api/brainStreamDeps.test.ts` at `38258352` is BYTE-EQUAL to DEPSTEST, each by sha256 over the committed blob against the slice extracted from the committed C0a blob. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npm run --silent typecheck` EXITS 0 with a zero-byte output stream, `npx vitest run` EXITS 0 at 10 files and 149 tests where the base is 9 and 137 — exactly the one file and twelve tests DEPSTEST adds — `tests/ui_contracts/` EXITS 0 at 409 passed plus 4 skipped = 413, and the five-target state readers plus canary EXIT 0 at 465 passed plus 0 skipped. THE RED CONTROL DISCRIMINATES, measured by the reviewer in its own disposable worktree at `cbf6de37` with `apps/ui/node_modules` SYMLINKED and the primary checkout never written to, agreeing with the worker: the ordered byte string occurs 1x in the file the control names, replacing `heldSeq + 1` with `heldSeq` EXITS 1 at 3 failed and 9 passed, failing exactly `the cursor arithmetic > asks for the position after the one it holds`, `the host deps over the real endpoints > opens the stream one position after the frame it holds` and `the host deps over the real endpoints > polls the tail strictly after the position it holds`, and the restored file returns to sha256 0caa5b23 and EXITS 0 at 12 passed. SEVEN single-parent commits over `82e30bb5`..`cbf6de37`, insertions 473, 378, 9, 2, 98, 122 and 46 in commit order — every one under 500, 473 the maximum — with `git show --numstat` and `git diff --numstat` AGREEING for all seven and every cell equal to the `## Commits` column for the six rows that table gives numbers for, the handback commit's own row naming itself instead, as R-0149 requires; zero marker lines in the plan at C1, the ledger at C2, both new modules at C3 and C4 and the handback at C5; seven reflog entries all `commit`; and a 76-line handback within the 100 seven commits allow. ONE DEVIATION WAS DECLARED AND IT IS SOUND: none of the round's commits carries the `Co-Authored-By` trailer this session's harness instructs, where R30's seven all did, and the reviewer's own reading of `82e30bb5`..`cbf6de37` returns 7 commits with 0 non-empty values. The worker did NOT repair it, because repairing means `git commit --amend`, which protocol G2 forbids and its own G11 gates at 0 — leaving the record honest was the correct call, and the counter-measure is an ordering constraint in the R32 block rather than a rewrite of history. NO FINDING IS REGISTERED AGAINST R31: every value reproduced, so R-0630 stays free.
<<<END LEDGER32

<<<SLICE ENV
/** The globals the browser environment is built from, taken as an argument
 *  rather than read off `globalThis`, so a test can present an environment
 *  WITHOUT EventSource without depending on which runtime is running it. */
export interface BrainStreamGlobals {
  EventSource?: new (url: string) => BrainStreamSource;
  fetch(path: string, init?: { method: "GET"; credentials: "same-origin" }): Promise<{
    ok: boolean;
    status: number;
    json(): Promise<unknown>;
  }>;
  setTimeout(resume: () => void, ms: number): unknown;
  clearTimeout(handle: unknown): void;
}

/** Bind the injected environment to real globals. A runtime with no
 *  EventSource yields `makeSource: null`, which is exactly the `unsupported`
 *  the polling fallback engages on — the client degrades to DELAYED instead of
 *  claiming a liveness it does not have. */
export function browserBrainStreamEnv(globals: BrainStreamGlobals): BrainStreamEnv {
  const Source = globals.EventSource;
  return {
    makeSource: Source === undefined ? null : (url: string): BrainStreamSource => new Source(url),
    fetchJson(path: string): Promise<unknown> {
      return globals
        .fetch(path, { method: "GET", credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw new Error(`Request failed ${response.status}: ${path}`);
          return response.json();
        });
    },
    setTimer(ms: number, resume: () => void): () => void {
      const handle = globals.setTimeout(resume, ms);
      return (): void => { globals.clearTimeout(handle); };
    },
  };
}
<<<END ENV

<<<SLICE TI1FROM
import { createBrainStreamHostDeps, cursorAfter, framesOf, snapshotSeqOf } from "./brainStreamDeps";
<<<END TI1FROM

<<<SLICE TI1TO
import { browserBrainStreamEnv, createBrainStreamHostDeps, cursorAfter, framesOf, snapshotSeqOf } from "./brainStreamDeps";
<<<END TI1TO

<<<SLICE TI2FROM
import type { BrainStreamEnv } from "./brainStreamDeps";
<<<END TI2FROM

<<<SLICE TI2TO
import type { BrainStreamEnv, BrainStreamGlobals } from "./brainStreamDeps";
<<<END TI2TO

<<<SLICE ENVTEST
describe("the browser environment", () => {
  interface Globals extends BrainStreamGlobals { cleared: unknown[]; }

  function globals(options: { source?: boolean; ok?: boolean } = {}): Globals {
    const cleared: unknown[] = [];
    const base = {
      cleared,
      fetch(_path: string): Promise<{ ok: boolean; status: number; json(): Promise<unknown> }> {
        return Promise.resolve({
          ok: options.ok !== false,
          status: options.ok === false ? 503 : 200,
          json: (): Promise<unknown> => Promise.resolve({ cursor: "2" }),
        });
      },
      setTimeout(resume: () => void, _ms: number): unknown { resume(); return "handle"; },
      clearTimeout(handle: unknown): void { cleared.push(handle); },
    };
    return options.source === true ? { ...base, EventSource: FakeSource } : base;
  }

  it("has no source where the runtime lacks EventSource, and one where it has it", () => {
    expect(browserBrainStreamEnv(globals()).makeSource).toBeNull();
    const make = browserBrainStreamEnv(globals({ source: true })).makeSource;
    expect(make).not.toBeNull();
    expect(make?.("/api/jobs/job-1/events/stream?cursor=0")).toBeInstanceOf(FakeSource);
  });

  it("parses a successful body and refuses a failed status", async () => {
    await expect(browserBrainStreamEnv(globals()).fetchJson("/p")).resolves.toEqual({ cursor: "2" });
    await expect(browserBrainStreamEnv(globals({ ok: false })).fetchJson("/p")).rejects.toThrow("503");
  });

  it("cancels a scheduled resume through the global it was given", () => {
    const g = globals();
    let resumed = 0;
    browserBrainStreamEnv(g).setTimer(10, () => { resumed += 1; })();
    expect(resumed).toBe(1);
    expect(g.cleared).toEqual(["handle"]);
  });
});
<<<END ENVTEST
