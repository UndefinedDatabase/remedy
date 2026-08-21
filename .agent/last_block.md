── STEP T003/8 — F008 SSE event stream — ROUND 28 ────────────────────────────
Round base — the SHA every range gate in this block measures from: c768cf03
 (R27's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R27 verdict and append the F008 R27 instance to the OPEN finding
 R-0629, a defect in the reviewer's own R27 block: a destructive control's
 prose claimed a byte string also occurs in a second file, and it occurs there
 zero times. This round changes NO code. It is the last round of this session,
 so its handback is also the session's return channel.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r28.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R28, applied whole
 C2a  `.agent/live_review.md` <- R0629FROM replaced by R0629TO, a REWRITE
 C2b  `.agent/live_review.md` <- LEDGER28, appended
 C3   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r28.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r28.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r28.md` for C0a. Never retype it.
 If the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are PLANF008R28, R0629FROM, R0629TO and LEDGER28,
 each delimited by a line beginning `<<<SLICE <name>` and one beginning
 `<<<END <name>`; marker lines are NOT part of a slice. Every slice is
 newline-terminated with no trailing whitespace on any line.

Pair shape, measured and not asserted (§3 item 15):
 R0629FROM/R0629TO is the block's ONLY pair. The containment test the reviewer
 ran on the final bytes printed `TO contains FROM: false`, so the pair is a
 REWRITE and the §4.9 obligation is the FROM-0x / TO-1x count of G5, never an
 append reading. It reads as an append by eye — R0629TO opens with R0629FROM's
 words and adds to them — and it is not one, because R0629FROM is
 newline-TERMINATED and R0629TO continues that sentence on the same line; the
 label is the test's output and not the eye's (R-0508, R-0522). R0629FROM
 occurs EXACTLY ONCE in `.agent/live_review.md` at the round base by the
 reviewer's own count; report your own before applying.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23). C2a precedes C2b so each
    ledger proof reads against a single-purpose commit.
 3. Nothing outside the change set is touched. NO CODE FILE IS EDITED and NO
    DEPENDENCY IS ADDED; `apps/ui/package.json` and `apps/ui/package-lock.json`
    are not opened. `.agent/live_review.md` is the one file this round amends.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0629 is AMENDED, not
    resolved, and stays OPEN, as do R-0368, R-0628 and R-0622. Write no
    `Done:` and no `Landed:` line for any of them. R-0628 is NOT resolved
    here even though its hook has now landed and been reviewed: this round
    was authored to close the session, and only a reviewer-authored `Done:`
    text sets Resolved (§4.4) — R29 carries it.
 5. The post-C3 `git status --porcelain`, `git worktree list` and push output
    belong to the ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G7's suites run in the PRIMARY
    checkout (R-0518). This round creates NO worktree and orders NO red
    control: it ships no behaviour to break.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    R26 gate and nothing since has created one.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there, as R27 did;
    commit nothing from that directory.
 9. THE HANDBACK ENDS THE SESSION. Its `## Next` section states, in this
    order: that the next session's FIRST action is the `.agent/STOP` re-read
    (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2); that
    R28 is PENDING REVIEW and its verdict is owed by the next round's ledger
    commit; that the next free finding id is R-0630; that R-0628, R-0629,
    R-0368 and R-0622 are OPEN, and that R-0628's hook HAS landed and been
    reviewed so R29 may resolve it; and that R29's work is the delayed badge
    on a visible surface plus wiring the hook's deps to the endpoint T001 and
    T002 built — the first round in which this feature's two halves meet.

The reviewer's OWN readings, each produced by RUNNING the tool and not recalled
(R-0625). At the round base in the primary checkout, serially: typecheck exits 0
silently, `npx vitest run` exits 0 at 9 files and 137 tests, `tests/ui_contracts/`
exits 0 at 402 passed plus 4 skipped = 406 and the state readers plus canary at
465 — that split moves run to run, so a bare passed count is never a gate.
`npm run lint` in `apps/ui` is RED at base, which is R-0622 and NOT a gate
(R-0364).

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2a and C2b. Per constraint 5 the post-C3 readings
     belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r28.md`
     as received, of `.agent/authored/f008-r28.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r28.md` with `git show`, by their marker lines, take
     the COUNT from that listing, and report each slice's newline-INCLUDED
     sha256, bytes and lines and that none carries trailing whitespace.
     Expected: PLANF008R28 23eed56c at 39 lines, R0629FROM
     64428337 at 1, R0629TO f6653cda at 1, LEDGER28 c64702c1 at 1.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R28. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The REWRITE at C2a. Read the base bytes with
     `git show <round base>:.agent/live_review.md` into scratch or memory —
     never by writing over the tracked file, which protocol G5 forbids
     (§3 item 29). Report the count of R0629FROM at the round base (expected
     1) and at C2a (expected 0), and of R0629TO at the round base (expected 0)
     and at C2a (expected 1) — the FROM-0x / TO-1x proof a rewrite owes.
     Report also that the base blob with that one
     byte-string substitution applied is BYTE-EQUAL to the C2a blob, that the
     blank-line paragraph COUNT is unchanged, and that EXACTLY ONE paragraph
     differs and it is the one beginning `- R-0629 — `.
 G6  The append at C2b, against C2a, two ways that must agree. (a) the C2a blob
     is a byte-exact PREFIX of the C2b blob and the remainder equals a newline
     plus LEDGER28 — report its sha256, bytes and lines; (b) an INDEPENDENT
     blank-line split of the WHOLE C2b file, its terminating newline normalised
     first, has as its LAST unit LEDGER28's paragraph. NEGATIVE CONTROL: flip
     one PRINTABLE ASCII byte of the remainder to another printable one and
     report that BOTH readings reject it and both accept the unflipped.
 G7  The sets, at C2a and C2b, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 201 at BOTH — this round mints no id — `^- R-0630 — `
     0 at both, `^- R-0629 — ` 1 at both, `^- R-0628 — ` 1 at both,
     `^- R-0368 — ` 1 at both, `^Done: R-\d+ — ` 6 at both, `^Landed: ` 0 at
     both, `^Gate: R\d+ — ` 27 then 28 over that many DISTINCT keys. HEADER
     SWEEP at C2b: report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of every non-match to its first period,
     and that the R28 pair occurs EXACTLY ONCE. Then, in the PRIMARY checkout,
     run SERIALLY at C2b — the commit at which both edited state files are
     final:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     exits 0 at 465 passed-plus-skipped, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` exits 0 at 406
     passed-plus-skipped. If either fails, report the real values and STOP.
 G8  The range, measured from the round base named in this block's header and
     from no other SHA. Report `git diff --name-only <round base>..C2b` and
     that it equals the Change set MINUS `.agent/handoff.md` exactly — four
     paths, none on either side alone; the full reading to C3 belongs to the
     ROUND REPORT (constraint 5). Report that every commit in the range has
     exactly ONE parent, and BOTH numstat cells per path from
     `git show --numstat`, cross-checked against `git diff --numstat`, every
     insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (§3 item 28).
 G9  Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or `<<<END `
     in each file this round writes outside `.agent/authored/` — the plan at
     C1, the ledger at C2a and C2b, and the handback at C3 — each is 0. Then
     count THIS round's own reflog entries by the OPERATION before the first
     `:` in `%gs`: all five pre-C3 entries are `commit`; report `amend`,
     `rebase` and `cherry` at 0, and assert no total.
 G10 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 9
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2a, C2b and C3 — "exactly one row" scoping to that
     TABLE. Measure its line count with `wc -l` BEFORE committing it; six
     commits make the cap 100, and an overage carries a DECISION D15
     stated-cause line naming the real count and the mandated content that
     caused it. One line per gate here; raw transcripts go in the ROUND REPORT
     (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block
repeats this Fortschritt line verbatim:
 ~97 % (T001 ✅ · T002 ✅ · T003 Regeln+Treiber+Runner+Store+Host+Seam+Hook ✅, Badge offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R28
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
R28 records the R27 verdict and appends the F008 R27 instance to R-0629, a
defect in the reviewer's own R27 block: a destructive control's prose claimed
a byte string also occurs in a second file, where it occurs zero times. It
changes no code. T003's client is now complete as a unit — rules, driver,
runner-as-store, the real host, the composition seam and the React hook — and
every piece of it below React is proved under the node-environment vitest.

## Next Steps
1. R29 puts the delayed badge on a visible surface and wires the hook's deps
   to the endpoint T001 and T002 built: the first round in which this
   feature's server half and client half meet. It may also resolve R-0628,
   whose hook has now landed and been reviewed under its contract.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The badge is a visual surface docs/ui/design_reference/ binds, with any
  deviation owed an assumption_log entry carrying a technical reason.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
<<<END PLANF008R28

<<<SLICE R0629FROM
the string the dry run had already built here and the block then failed to carry.
<<<END R0629FROM

<<<SLICE R0629TO
the string the dry run had already built here and the block then failed to carry. F008 R27 INSTANCE, in the reviewer's own block again and one clause to the side of the fix just stated: the R27 block's G10 counted all three ordered byte strings in the file it names — 1 each, from the reviewer's own script, exactly as the fix above requires — and then added an aside nobody measured, that the same byte string `also occurs in CONTRACT, which ASSERTS it`. Measured at `345a8be8`, by the worker during the round and by the reviewer after it, all three occur ZERO times in `tests/ui_contracts/test_brain_stream_hook.py`: that file asserts the UNINDENTED `return () => { session.close(); };` and the bare `useSyncExternalStore(`, and says nothing whatever about `latestMakeDeps.current(jobId)`. NOTHING WENT WRONG because of it — the gate counts in the hook, all three counts were 1, and each control went red on exactly its named test — so this is Low where the R24 instance was Medium. IT IS REGISTERED ANYWAY, and against this id rather than a new one (§3 item 30), because the shape is the same and the lesson is narrower than the first telling suggests: the reviewer did run the script, did write its output, and then added one more sentence from memory, so the discipline held everywhere it was formalised and failed in the sentence beside it. A false clause sitting next to a measured one is the worst place for it, because a reader has no way to tell which is which. THE FIX IS WIDENED BY ITS SCOPE: every occurrence claim a control's prose makes is that script's output, in EVERY file the sentence names and never only in the file the control mutates. Measuring a second file costs one line of the script that is already running.
<<<END R0629TO

<<<SLICE LEDGER28
Gate: R28 — the R27 entry. R27 PASSED. It landed `useBrainStream.ts` and its source contract, recorded the R26 verdict and amended R-0368, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r27.md`, `.agent/authored/f008-r27.md` at `27984108` and `.agent/last_block.md` at `1408caf8` are all sha256 bc0f2ff03d5d9883809adf91764c63111c409d028a3a3e732d369ce7ae8bc2d1 over 27996 bytes and 394 lines, equal to the digest the reviewer emitted. SIX SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R27 4e8555ca at 40 lines, R0368FROM 432fdc8e and R0368TO 8e234582 and LEDGER27 5528f762 at 1 line each, HOOK 362a9d56 at 36 lines, CONTRACT 0565e0be at 87 lines — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `e22203b2`, byte-equal at 40 lines under the 50-line cap. THE REWRITE at `6264a959` is proved twice over: R0368FROM 1 at the base and 0 after, R0368TO 0 at the base and 1 after — the FROM-0x/TO-1x count a rewrite owes — and, independently, the base blob with that one byte-string substitution applied is BYTE-EQUAL to the C2a blob, with 237 blank-line paragraphs before and after, exactly ONE of them differing, and that one the `- R-0368 — ` paragraph. THE APPEND at `31223074` is a byte-exact prefix of the C2a blob plus a 3501-byte remainder equal to a newline plus LEDGER27, agreed by an INDEPENDENT split of the whole file into 238 units whose LAST is LEDGER27's paragraph, with a one-byte flip REJECTED by BOTH readings. THE SETS HELD — findings 201 at both revisions with NO id minted, `- R-0630` 0, `- R-0629`, `- R-0628` and `- R-0368` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 26 to 27 over that many DISTINCT keys, twenty-six of twenty-seven headers matching the shape with the F255 entry the single non-match, and the R27 pair occurring exactly once. THE TWO CODE FILES ARE PROVED BY CONSTRUCTION: `git ls-tree a86231c0` is EMPTY for both, each blob at `345a8be8` is BYTE-EQUAL to its slice, and their numstat cells are 36 and 87 insertions with ZERO deletions. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: typecheck exits 0 with no output, `npx vitest run` exits 0 at 9 files and 137 tests — UNCHANGED, because a hook this repository cannot render carries no vitest test, which is the whole reason the contract exists — `tests/ui_contracts/` exits 0 at 402 passed plus 4 skipped, nine more than the base's 397, and the state readers including the canary exit 0 at 465. ALL THREE RED CONTROLS DISCRIMINATE, measured by the reviewer in a disposable worktree before the block was written and by the worker at `345a8be8`, agreeing: the missing unmount cleanup fails ONLY `test_hook_closes_the_session_on_unmount`, the store read replaced by a bare call fails ONLY `test_hook_reads_the_runner_as_an_external_store`, and the argument dropped from the deps factory EXITS 2 — tsc's real code — naming `error TS2554`, each restored byte-identical. SEVEN single-parent commits, every insertion under 500 and every cell equal to the `## Commits` column; zero marker lines in all six targets; six reflog operations all `commit`; a 77-line handback within the 100 seven commits allow; the tree clean and the primary checkout the only worktree. THE ROUND DECLARED FOUR DEVIATIONS AND EVERY ONE IS SOUND: the worker discarded a degenerate negative control that flipped a space to a NUL and re-ran it printable-to-printable, which is a better control than the one ordered; it ran the contract file once before committing as the AGENTS.md self-review requires and said so; it retried a push that GitHub's SSH endpoint refused eight times; and it OBJECTED, correctly, to an unmeasured aside in G10 — recorded above against R-0629.
<<<END LEDGER28
