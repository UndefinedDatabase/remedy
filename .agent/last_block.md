── STEP T003/5 — F008 SSE event stream — ROUND 25 ────────────────────────────
Goal:
 Record the R24 verdict and register R-0629, a defect in the reviewer's own
 R24 block: a red control asserted its target line occurs once where it occurs
 twice. This round changes NO code. It is the last round of this session, so
 its handback is also the session's return channel.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r25.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R25, applied whole
 C2   `.agent/live_review.md` <- LEDGER25, appended
 C3   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r25.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r25.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r25.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R25 and LEDGER25, each delimited by a
 line beginning `<<<SLICE <name>` and one beginning `<<<END <name>`; marker
 lines are NOT part of the slice. Both are newline-terminated with no trailing
 whitespace on any line. There is NO FROM/TO pair: one slice replaces a file
 whole and the other is appended, so the obligations are byte equality and an
 ordered append, never a containment reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23).
 3. Nothing outside the change set is touched. NO CODE FILE IS EDITED and NO
    DEPENDENCY IS ADDED; `apps/ui/package.json` and `apps/ui/package-lock.json`
    are not edited.
 4. R-0629 is REGISTERED by LEDGER25 and stays OPEN, as does R-0628 — write no
    `Done:` and no `Landed:` line for either, and mint no further id: R-0630
    stays free. R-0622 stays OPEN.
 5. The post-C3 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G7's suites run in the PRIMARY
    checkout (R-0518). This round creates NO worktree and orders NO red
    control: it ships no behaviour to break.
 7. The reviewer's OWN readings at `6e39f19d`, each produced by RUNNING the
    tool rather than recalled (R-0625): from the root the state readers plus
    canary exit 0 at 465 and `tests/ui_contracts/` at 397, both
    passed-plus-skipped — that split moves run to run, so a bare passed count
    is never a gate. In `apps/ui`, untouched by this round, `npx vitest run`
    exits 0 at 8 files and 131 tests, typecheck exits 0 silently, and lint
    EXITS 1 at `57 problems (55 errors, 2 warnings)`, which is R-0622 and NOT
    a gate (R-0364).
 8. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R25 gate.
 9. THE HANDBACK ENDS THE SESSION. Its `## Next` section states, in this
    order: that the next session's FIRST action is the `.agent/STOP` re-read
    (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2); that
    R25 is PENDING REVIEW and its verdict is owed by the next round's ledger
    commit; that the next free finding id is R-0630; that R-0628 and R-0629
    are OPEN; and that R26's work is the thin `useBrainStream` hook over the
    runner store plus the visible delayed badge, gated by `npm run typecheck`
    and a NEW `tests/ui_contracts/` source contract, with the hook calling the
    host's `close` on unmount.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1 and C2. Per constraint 5 the post-C3 readings belong
     to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r25.md`
     as received, of `.agent/authored/f008-r25.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r25.md` with `git show`, by their marker lines,
     take the COUNT from that listing, and report each slice's
     newline-INCLUDED sha256, bytes and lines and that neither carries
     trailing whitespace. Expected: PLANF008R25 0cc72159 at 39 lines,
     LEDGER25 2dd41f07.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R25. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The ledger append, C2 against C1, two ways that must agree. (a) the C1
     blob is a byte-exact PREFIX of the C2 blob and the remainder equals a
     newline plus LEDGER25 — report its sha256, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, LEDGER25's
     two paragraphs. NEGATIVE CONTROL: flip one ASCII byte of the remainder to
     another and report that BOTH readings reject it and both accept the
     unflipped.
 G6  The sets, at C1 and C2, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 200 then 201 — R-0629 is the only id minted —
     `^- R-0629 — ` 0 then 1, `^- R-0630 — ` 0 at both, `^- R-0628 — ` 1 at
     both, `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at both,
     `^Gate: R\d+ — ` 24 then 25 over that many DISTINCT keys. HEADER SWEEP at
     C2: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below
     the first, how many do not, the text of every non-match, and that the R25
     pair occurs EXACTLY ONCE.
 G7  The state readers are green in the PRIMARY checkout, run SERIALLY, AT C2 —
     the commit at which both edited state files are final. Report the exit
     code and counts of each:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 397
     passed-plus-skipped. If either fails, report the real values and STOP.
 G8  The range. Report `git diff --name-only 6e39f19d..C2` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly — four paths, none on
     either side alone; the full `6e39f19d..C3` reading belongs to the ROUND
     REPORT (constraint 5). Report that every commit in the range has exactly
     ONE parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (§3 item 28).
 G9  Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `.agent/handoff.md` at C3 — each is 0. Then count THIS round's own reflog
     entries by the OPERATION before the first `:` in `%gs`: all four pre-C3
     entries are `commit`; report `amend`, `rebase` and `cherry` at 0, and
     assert no total.
 G10 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 9
     names, and an item-status table holding exactly one row for each of C0a,
     C0b, C1, C2 and C3 — "exactly one row" scoping to that TABLE, not the
     whole file. Measure its line count with `wc -l` BEFORE committing it;
     five commits make the cap 60 lines, and an overage carries a DECISION D15
     stated-cause line naming the real count and the mandated content that
     caused it. One line per gate here; the raw transcripts go in the ROUND
     REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~94 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host ✅, Hook offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R25
# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint that streams the event ledger from a cursor — the
ledger's own monotonic seq carried and never renumbered, a 15 s heartbeat and
Last-Event-ID resume replaying exactly the missed span — plus a client hook
with reconnect backoff, gap detection and an honest polling fallback that
labels itself delayed. DONE when a fake job streams into a test client with
zero gaps across forced disconnects, the transcript byte-equals the ledger's
envelope sequence, the heartbeat holds cadence, and the fallback engages on a
disabled EventSource and recovers to live.

## Current Step
R25 records the R24 verdict and registers R-0629, a defect in the reviewer's
own R24 block: a red control asserted that its target line occurs once when it
occurs twice. It changes no code. T003's client side is now rules, driver,
runner-as-store and the real host, each proved under the node-environment
vitest.

## Next Steps
1. R26 adds the thin `useBrainStream` hook over the runner store and the
   visible delayed badge, gated by `npm run typecheck` and a
   `tests/ui_contracts/` source contract — the style this repository uses for
   every React component (R-0628). The hook must call the host's `close` on
   unmount, or a remounting cockpit leaks one EventSource per mount.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- Nothing wires the host to a real job yet: R26 is the first round in which
  the endpoint T001 built and the client T003 built meet.
<<<END PLANF008R25

<<<SLICE LEDGER25
- R-0629 — Medium — A DESTRUCTIVE CONTROL THAT ASSERTED A UNIQUENESS IT NEVER MEASURED, IN THE REVIEWER'S OWN BLOCK. The R24 block's G9 control (b) ordered the deletion of the line `      drop();` — six leading spaces — and described it as "the FIRST statement of `connect`, occurring once at that indent". MEASURED at `46ac9da4` by the reviewer after the round, and by the worker during it: that exact line occurs TWICE in `apps/ui/src/api/brainStreamHost.ts`, at line 87 in `connect` and at line 123 in `close`, so the block's count was false and the "occurs EXACTLY ONCE" reading G9 orders was unmeetable for that control. WHAT PRODUCED IT is the specific trap §3 item 25 exists for: the reviewer's dry run measured a LONGER anchor — `    connect(lastEventId: string | null): void {` followed by the `      drop();` line — which really does occur once, and the block then named the SHORT line while carrying the LONG one's uniqueness reading. The measurement and the ordered bytes diverged, and only the ordered bytes reach the worker. NO FALSE GREEN LANDED: the worker counted 2, reported 2, deleted line 87 on the block's own disambiguating prose, and the run EXITED 1 naming exactly the predicted test with eleven passing — the round paid a declared deviation for the reviewer's error, which is the outcome R-0252 already named as the expensive one. WHY MEDIUM AND NOT LOW: deleting line 123 instead ALSO exits 1, because the close-idempotence test fails, so a reader who resolves an ambiguous name to the wrong line gets a red that is indistinguishable from success unless the predicted test NAME is checked — the R-0560 shape, where a control cannot tell its own success from a different failure. THE FIX, binding on the next block that orders a destructive control: the bytes a control deletes or replaces are counted by the reviewer's own script IN the named file at the SHA the control runs at, the number written into the block is that script's OUTPUT rather than a recollection, and where the count exceeds 1 the block orders the longest byte string that reads 1 — the string the dry run had already built here and the block then failed to carry.

Gate: R25 — the R24 entry. R24 PASSED. It pinned the stream host with twelve tests and three red controls, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS by the primary comparison: `.remedy-wt/f008-r24.md`, `.agent/authored/f008-r24.md` at `e9d1bea4` and `.agent/last_block.md` at `77906cb8` are all sha256 e1123bf53acb712bc891c69e77f2ce51392ba013ad2f633d49b0b187d2814b85 over 24620 bytes and 425 lines, equal to the digest the reviewer emitted. THREE SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R24 063f969b at 2033 bytes and 38 lines, LEDGER24 9243828b at 3396 bytes, HOSTTESTS 5281e235 at 6791 bytes and 194 lines — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `cd830005`, byte-equal at 38 lines under the 50-line cap, carrying `Steps`, one `## Goal`, one `## Next Steps` and the F-id `F008`. THE APPEND at `df466117` is a byte-exact prefix of the `cd830005` blob plus a 3397-byte remainder equal to a newline plus LEDGER24, agreed by an INDEPENDENT blank-line split of the whole file into 234 units whose LAST unit is LEDGER24's paragraph, with a one-ASCII-byte flip REJECTED by BOTH readings and the unflipped ACCEPTED by BOTH. THE SETS HELD — findings 200 at both revisions, `- R-0628` 1 at both and still OPEN, `- R-0629` 0 at both because this entry is the round that mints it, `Done:` 6 at both, `Landed:` 0 at both, `Gate: R` 23 to 24 over that many DISTINCT keys, twenty-three of twenty-four headers matching the `Gate: R<n> — the R<n-1> entry.` shape with the F255 entry the single non-match, and the R24 pair occurring exactly once. THE TEST FILE IS PROVED BY CONSTRUCTION: `git ls-tree b6a1c4d1` is EMPTY for it, its C3 blob is BYTE-EQUAL to HOSTTESTS, its numstat is 194 insertions and ZERO deletions, and the module's blob is IDENTICAL at `b6a1c4d1` and `46ac9da4` — the round added the tests that pin the adapter and changed nothing they measure. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npx vitest run` exits 0 at 8 files and 131 tests, that file alone at 12, `npm run --silent typecheck` exits 0 with no output, the state readers including the canary exit 0 at 465 passed-plus-skipped and `tests/ui_contracts/` at 393 passed plus 4 skipped. LINT IS RED AND DECLARED at 57 problems, 55 errors and 2 warnings, one above R23's because the round adds one file eslint cannot parse, which is R-0622 and not a gate. THE THREE RED CONTROLS WERE MEASURED TWICE, once by the reviewer in a disposable worktree at `b6a1c4d1` before the block was written and once by the worker at `46ac9da4`, agreeing on all three: each EXITS 1 with EXACTLY ONE failure and eleven passing, naming the malformed-frame test, the reconnect-closes-the-old-socket test and the polling-cursor test respectively, and after restoration the module's sha256 equals its `b6a1c4d1` blob with the suite EXITING 0 at 12. SIX single-parent commits, insertions 425, 296, 14, 2, 194 and 30, every one under 500 and every cell equal to the handback's `+/-` column; zero marker lines in all four targets; five reflog operations all `commit`; a 67-line handback within the 100 six commits allow; the tree clean and the primary checkout the only worktree. THE ROUND'S ONE DECLARED DEVIATION IS A DEFECT OF THIS REVIEWER'S BLOCK AND NOT OF ITS WORK, registered above as R-0629, and the worker's refusal either to edit the block or to silently pick another line is exactly what the deviation mechanism is for.
<<<END LEDGER25
