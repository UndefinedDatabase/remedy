── STEP T003/5 — F008 SSE event stream — ROUND 22 ────────────────────────────
Goal:
 Record the R21 verdict, register R-0628 and re-plan T003. This round changes
 NO code: R-0628 says the blocker R21 wrote to disk does not follow from its
 own premise, and the ordering that fixes it is what R23 and R24 execute.

Why the block is a record round:
 R21 declared R22 blocked until a session installs a DOM environment. The
 reviewer re-measured that claim rather than inheriting it: the install is
 indeed denied here too, and the conclusion still does not follow, because
 this repository gates every React component by reading its SOURCE from
 `tests/ui_contracts/` and the piece the hook cannot exist without — the real
 host adapter — needs no DOM at all. The finding, the verdict and the re-plan
 are one indivisible record, and the adapter is a code round of its own.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r22.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R22, applied whole
 C2   `.agent/live_review.md` <- LEDGER22, appended
 C3   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r22.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r22.md`, which is gitignored. Read
 it there, verify its sha256 against the value in your task prompt BEFORE
 using it, and copy that file's bytes to `.agent/authored/f008-r22.md` for
 C0a. Never retype it. If the digest does not match, STOP and report both
 values.

Slice convention:
 The authored units below are PLANF008R22 and LEDGER22, each delimited by a
 line beginning `<<<SLICE <name>` and one beginning `<<<END <name>`; marker
 lines are NOT part of the slice. Both are newline-terminated with no trailing
 whitespace on any line. There is NO FROM/TO pair this round: one slice
 replaces a file whole and the other is appended, so the obligations are byte
 equality and an ordered append, never a containment reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, apply it as written and say
    so in the handback's deviations section — do not fix it.
 2. The commit order above is fixed: no extra commit, no dropped commit, no
    reordering. C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. NO CODE FILE IS EDITED and NO
    DEPENDENCY IS ADDED — not jsdom, not happy-dom, not a testing library.
    `apps/ui/package.json` and `apps/ui/package-lock.json`, the only two
    manifests this repository tracks, are not edited for any reason.
 4. R-0628 is REGISTERED by LEDGER22 and stays OPEN — write no `Done:` and no
    `Landed:` line for it, and mint no further id: R-0629 stays free.
 5. R-0622 stays OPEN — do not add a TypeScript parser to make lint green.
 6. The post-C3 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md`: C3 cannot state
    facts about itself (R-0371).
 7. Two test processes never run at once, and G7's suites run in the PRIMARY
    checkout (R-0518). This round needs no worktree: it mutates nothing and
    orders no red control, because it ships no behaviour to break.
 8. The reviewer's OWN readings at `37c93574`, each produced by RUNNING the
    tool rather than recalled (the R-0625 counter-measure): from the root the
    state readers plus canary exit 0 at 465 and `tests/ui_contracts/` at 397,
    both passed-plus-skipped — that split moves run to run at an unchanged
    tree, so a bare passed count is never a gate. In `apps/ui`, untouched by
    this round, `npx vitest run` exits 0 at 7 files and 119 tests,
    `npm run --silent typecheck` exits 0 with no output, and
    `npm run --silent lint` EXITS 1 at `55 problems (53 errors, 2 warnings)`,
    which is R-0622, is NOT a gate (R-0364) and is not repaired here.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. The
    branch is not closeable while T003 is unfinished: push it and leave it
    open. `gh pr list --state open` returned `[]` at the R22 gate.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1 and C2. Per constraint 6 the post-C3 readings belong
     to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r22.md`
     as you received it, of `.agent/authored/f008-r22.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL. The
     digest the reviewer measured for that file is in your task prompt and
     never inside this text, which cannot carry its own (R-0371); report
     whether the file you read matches it.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r22.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256, bytes and
     lines, and that neither carries trailing whitespace on any line.
     Expected: PLANF008R22 c7f6e97d at 43 lines, LEDGER22 b8f3fa92.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R22. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER22 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, LEDGER22's
     two paragraphs. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another ASCII byte and report that BOTH readings reject it and both
     accept the unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 199 then 200 — R-0628 is the only id minted —
     `^- R-0628 — ` 0 then 1, `^- R-0629 — ` 0 at both, `^Done: R-\d+ — ` 6 at
     BOTH, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 21 then 22 over that many
     DISTINCT keys. HEADER SWEEP at C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below
     the first, how many do not, the text of every non-match, and that the R22
     pair occurs EXACTLY ONCE.
 G7  The state readers are green in the PRIMARY checkout, run SERIALLY, AT C2 —
     the commit at which both edited state files are final. Report the exit
     code and counts of each:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. If either fails, report the real values and STOP.
 G8  The range. Report `git diff --name-only 37c93574..C2` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — four paths, none on
     either side alone. The full `37c93574..C3` reading belongs to the ROUND
     REPORT (constraint 6, R-0371). Report that every commit in the range has
     exactly ONE parent, and BOTH numstat cells per path from
     `git show --numstat`, cross-checked against `git diff --numstat`, every
     insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (§3 item 28).
 G9  Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `.agent/handoff.md` at C3. Each is 0.
 G10 Reflog. Count THIS round's own entries by the OPERATION before the first
     `:` in `%gs`. All four pre-C3 entries are `commit`; report `amend`,
     `rebase` and `cherry` at 0, and assert no total.
 G11 The handback carries every mandated section of
     docs/agents/handback_template.md and an item-status table holding exactly
     one row for each of C0a, C0b, C1, C2 and C3 — "exactly one row" scoping to
     that TABLE, not to the whole file. Measure its line count with `wc -l`
     BEFORE committing it; this round has five commits, so the cap is 60 lines,
     and an overage carries a DECISION D15 stated-cause line naming the real
     count and the mandated content that caused it. One line per gate here;
     the raw transcripts go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~90 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store ✅, Host+Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R22
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
R22 records the R21 verdict and registers R-0628, which retires the claim that
T003 is blocked until a DOM environment can be installed. It changes no code:
the ordering that finding fixes is what the next two rounds execute.

## Next Steps
1. R23 builds the REAL host behind `BrainStreamHost` — an injected
   EventSource, a snapshot read, a tail read and a scheduler — the piece the
   hook cannot exist without, proved under the node-environment vitest with
   no DOM at all.
2. R24 adds the thin `useBrainStream` hook over the runner store and the
   visible delayed badge, gated by `npm run typecheck` and a
   `tests/ui_contracts/` source contract — the style this repository already
   uses for every React component.
3. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): it
  exits 1 because that eslint config installs no TypeScript parser, which is
  R-0622 and routes to a paydown branch. `npm run typecheck` and
  `npx vitest run` both exit 0 and ARE the gates.
- The adapter R23 adds owns a socket, so a leak is the failure mode to fear:
  `close` belongs on the object its factory returns rather than on
  `BrainStreamHost`, and R24's hook must call it on unmount.
- The badge remains a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
<<<END PLANF008R22

<<<SLICE LEDGER22
- R-0628 — Medium — A BLOCKER DECLARED AGAINST THE REPOSITORY'S OWN DELIVERABLE STYLE, WHICH WOULD HAVE STALLED T003 ON AN OPERATOR ACTION IT NEVER NEEDED. `.agent/plan.md` at `de574779`, `.agent/handoff.md` at `37c93574` and the R21 block at `97f8b09c` each state that R22 IS BLOCKED until a session can install a DOM environment, because no jsdom, happy-dom or testing library is present and that session's command guard denied the npm commands which would add one. THE PREMISE IS TRUE AND WAS RE-MEASURED, the conclusion is not: this session's guard denies `npm view jsdom version` as well, and `apps/ui/package.json` at `37c93574` carries `react-dom` in its dependencies and neither jsdom, happy-dom nor a testing library in either dependency block. What does not follow is the word BLOCKED. `tests/ui_contracts/` at `37c93574` holds seven python modules that gate React components by reading their SOURCE — `test_degraded_banner.py` asserts `role="alert"` and `failedEndpoints` inside `DegradedBanner.tsx`, and `DegradedBanner` inside `RemedyShell.tsx` — so no component in this repository has ever carried a render test, and `docs/roadmap/features/T5_F008.md` names that style itself: "Contract tests are the deliverable style here (ui_contract marker)". THE OPEN SET WAS SEARCHED FOR THE DEFECT before this id was minted (§3 item 30): the only entry naming the hook is R-0622, whose subject is the lint parser, and nothing in the ledger describes a stalled T003. THE FIX IS AN ORDERING, NOT A RULE, and the plan this round writes carries it: T003's DOM-free piece — the real `BrainStreamHost` adapter over an injected EventSource, snapshot read, tail read and scheduler, which the hook cannot exist without — lands at R23, and R24 adds the hook and the badge under `npm run typecheck` plus a `tests/ui_contracts/` source contract, the same gate every other component here carries. The reviewer dry-ran that adapter and its twelve tests before writing this: `npx tsc --noEmit` exits 0 and the suite exits 0 at 8 files and 131 tests, with no dependency added. R-0628 stays OPEN until the hook has landed under that gate. A blocker is a claim about what CANNOT be proved, and it is owed the same measurement as any other gate value; this one was written from what the session could not INSTALL rather than from what the round could PROVE.

Gate: R22 — the R21 entry. R21 PASSED and no finding is registered against its work — the fourth consecutive round on this branch for which that is true. EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs, never read back out of the handback. TRANSPORT PROVED BY THE §4.9 DIGEST FALLBACK, the scratch original having died with the R21 session: `.agent/authored/f008-r21.md` at `97f8b09c`, `.agent/last_block.md` at `721fc60c` and that file's working copy are all EQUAL at sha256 b5ab6292a5d83b5296258a26874ae3929c21f139ca6fddae6e8843bfd283ab4a over 28075 bytes and 424 lines. FIFTEEN SLICES by the reviewer's own ordered extraction out of the committed C0a blob, every newline-included digest equal to the value the block names and none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `de574779`, byte-equal to PLANF008R21 at 46 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `e1622497` is a byte-exact prefix of the `de574779` blob plus a 5211-byte remainder equal to a newline plus LEDGER21, agreed by an INDEPENDENT blank-line split of the whole file into 230 units whose LAST TWO are LEDGER21's paragraphs in order, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS MOVED AS ORDERED — 199 findings at both revisions because no id was minted, `Done:` 5 to 6 over exactly R-0620, R-0621, R-0623, R-0624, R-0626 and R-0627, `Landed:` 0 at both, `Gate: R` 20 to 21 over that many DISTINCT keys, R-0628 0 at both; twenty of the twenty-one headers match the `Gate: R<n> — the R<n-1> entry.` shape and the single non-match is the F255 entry, correctly shaped for what it records. THE SIX PAIRS ARE PROVED CONSTRUCTIVELY: applying them to the `b97fb0b7` blob in bundle order reproduces the `e96ac8e7` blob byte for byte at sha256 f75aae30aed319bbbcc8c987a11dafa7deb21a086a921945fe304d5746ffaea2 over 5138 bytes and 136 lines, LETSFROM being the ONE pair whose TO contains its FROM and the other five printing false, with `subscribe` 1 to 4, `cachedView` 0 to 6, `publish` 0 to 3, `listeners` 0 to 4 and a 32/3 numstat. THE TEST APPEND at `64b5a19f` is a byte-exact prefix relationship whose remainder is 130408b3 over 1418 bytes and 40 lines, `^  it(` 12 to 16, `^describe(` 6 to 7, ZERO deletions. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 7 files and 119 tests with the runner file at 16, `npm run --silent typecheck` exits 0 with no output, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 393 passed plus 4 skipped. LINT IS RED AND DECLARED, never repaired: 55 problems, 53 errors, 2 warnings, which is R-0622. ALL THREE RED CONTROLS WERE RE-RUN in one disposable worktree with `node_modules` symlinked and removed before this text was written: the notification control EXITS 1 with EXACTLY the eight failures the block predicted, the identity control EXITS 1 naming only `the runner as a store > hands back the same view object until something visibly changes` with the other fifteen green, the silence control EXITS 1 naming only `the runner as a store > stays silent when an event changes nothing a reader can see`, and after restoration the file's sha256 equals the C4 blob's while the suite EXITS 0 at 16 passed. SEVEN single-parent commits, insertions 424, 278, 18, 4, 32, 40 and 34, every one under 500 and every cell equal to the handback's `+/-` column; zero lines beginning with a slice marker in all five targets; an 83-line handback within the 100 that seven commits allow, its item-status table naming C0a through C5 exactly once each; the tree clean and the primary checkout the only worktree. WHAT R21 GOT WRONG IS NOT ITS WORK BUT ITS FORECAST, registered above as R-0628: it declared R22 blocked pending a DOM install while this repository gates every React component by source contract and the next T003 piece needs no DOM at all.
<<<END LEDGER22
