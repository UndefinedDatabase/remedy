── STEP T003/8 — F008 SSE event stream — ROUND 33 ────────────────────────────
Round base — the SHA every range gate in this block measures from: 9f14a79e
 (R32's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R32 verdict — PASS, every gate re-run by the reviewer out of the
 committed blobs — amend the OPEN finding R-0629 with the F008 R32 instance,
 which is a defect in the reviewer's own block text, and WIRE THE COCKPIT: the
 shell subscribes to its job's stream and the badge finally reads a real
 transport status. This is the round in which this feature's two halves meet.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r33.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R33, applied whole
 C2   `.agent/live_review.md` <- R0629FROM replaced by R0629TO, a REWRITE
 C3   `.agent/live_review.md` <- LEDGER33, appended
 C4   `apps/ui/src/components/shell/RemedyShell.tsx` <- SHIMP, SHSIG and
      SHCALL applied as three pairs, all three in this ONE commit
 C5   `tests/ui_contracts/test_remedy_shell_stream.py` <- CONTRACT, a NEW file
 C6   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r33.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `apps/ui/src/components/shell/RemedyShell.tsx`,
 `tests/ui_contracts/test_remedy_shell_stream.py`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r33.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r33.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, none
 begins with a blank line, and every count this block orders over a slice is
 taken over those newline-INCLUDED bytes.

Pair shape (§3 item 15). Each line below is the OUTPUT of the reviewer's
containment test over the final newline-INCLUDED bytes; the label is derived
from that output beside it and is never written on its own (R-0522):
 R0629FROM/R0629TO      TO contains FROM: false  -> REWRITE
 SHIMPFROM/SHIMPTO      TO contains FROM: true   -> APPEND
 SHSIGFROM/SHSIGTO      TO contains FROM: true   -> APPEND
 SHCALLFROM/SHCALLTO    TO contains FROM: false  -> REWRITE
 R0629FROM reads as an append by eye and is not one, because it is
 newline-TERMINATED while its TO continues that sentence on the same line;
 SHCALLFROM likewise ends in `/>` where its TO inserts a prop before it. G5
 therefore orders the FROM-0x / TO-1x count each REWRITE owes, and G8 orders
 for the two APPEND pairs the reading §4.9 gives code — that one pass of all
 three substitutions reproduces the committed blob byte for byte — and NOT a
 FROM-zero count, which is unattainable for a TO that contains its FROM.
 FROM uniqueness, each counted by the reviewer's own script IN the file the
 pair edits, at the round base, and reported as that script's output (item 25):
 R0629FROM occurs 1x in `.agent/live_review.md`; SHIMPFROM 1x, SHSIGFROM 1x and
 SHCALLFROM 1x in `apps/ui/src/components/shell/RemedyShell.tsx`.
 PLANF008R33 is a whole-file write, LEDGER33 an append and CONTRACT a file
 creation, so none of the three is a pair and none carries a containment
 reading.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23), C2 precedes C3 so each
    ledger proof reads against a single-purpose commit, and C4 precedes C5 so
    the wiring lands before the contract that reads it.
 3. Nothing outside the change set is touched. NO DEPENDENCY IS ADDED:
    `apps/ui/package.json` and `apps/ui/package-lock.json` are not opened.
    `apps/ui/src/RemedyApp.tsx` is NOT edited — DECISION F008 D3, recorded at
    `3517f345`, puts the subscription in the shell precisely so that file stays
    untouched.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0629 is AMENDED, not
    resolved, and stays OPEN, as do R-0368, R-0429, R-0553, R-0622 and R-0628.
    Write no `Done:` and no `Landed:` line for any of them. The reviewer
    searched the ledger for the DEFECT before routing it here (item 30), and
    R-0629's subject — a destructive control asserting a uniqueness it never
    measured — is this defect exactly, so it takes the amendment rather than a
    second id.
 5. END EVERY COMMIT MESSAGE of this round with the trailer line
    `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, preceded by a
    blank line. G13 measures the result. Never repair a missing trailer by
    amending — protocol G2 forbids it and G12 gates it at 0.
 6. The post-C6 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 7. Two test processes never run at once, and G10's suites run in the PRIMARY
    checkout (R-0518). G11's red control is the ONLY destructive check and runs
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
    its SECOND the Open PR Gate (Phase 1 rule 2); that R33 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0622, R-0628 and
    R-0629 are OPEN; and that R34's work is the INTEGRATION GATE per
    docs/agents/integration_gate.md, the full suite before closure, with T003
    complete once this round lands.

The reviewer's OWN readings, each produced by RUNNING the tool at the round base
`9f14a79e`, serially, in the PRIMARY checkout, not recalled (R-0625): the
five-target state reader plus canary EXITS 0 at 465 passed and 0 skipped;
`python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 409 passed plus 4
skipped = 413; and in `apps/ui`, `npm run --silent typecheck` EXITS 0 with NO
output while `npx vitest run` EXITS 0 at 10 files and 152 tests. `npm run lint`
is RED at base, which is R-0622 and NOT a gate (R-0364). The reviewer also
applied all four pairs and CONTRACT in a disposable worktree at `9f14a79e` and
measured every value G10 and G11 order there before ordering them.

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2, C3, C4 and C5. Per constraint 6 the post-C6
     readings belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r33.md`
     as received, of `.agent/authored/f008-r33.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r33.md` with `git show`, by their marker lines, take
     the COUNT from that listing and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, that none carries trailing whitespace on any line, and that
     none begins with a blank line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R33. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The REWRITE at C2. Read the base bytes with
     `git show 9f14a79e:.agent/live_review.md` into scratch or memory — never
     by writing over the tracked file, which protocol G5 forbids (item 29).
     Report the count of R0629FROM at the round base (expected 1) and at C2
     (expected 0), and of R0629TO at the base (expected 0) and at C2 (expected
     1) — the FROM-0x / TO-1x proof a rewrite owes. Report also that the base
     blob with that substitution applied ONCE is BYTE-EQUAL to the C2 blob, the
     blank-line paragraph COUNT unchanged, and EXACTLY ONE paragraph differing,
     the one beginning `- R-0629 — `.
 G6  The append at C3, against C2, two ways that must agree. (a) the C2 blob is
     a byte-exact PREFIX of the C3 blob and the remainder equals a newline plus
     LEDGER33 — report its sha256 prefix, bytes and lines; (b) an INDEPENDENT
     blank-line split of the WHOLE C3 file, its terminating newline normalised
     first, has LEDGER33's paragraph as its LAST unit. NEGATIVE CONTROL: flip
     one PRINTABLE ASCII byte of the remainder to another printable one; BOTH
     readings must reject it and both accept the unflipped.
 G7  The sets in `.agent/live_review.md`, line-anchored, each reported at the
     round base, at C2 AND at C3: `^- R-\d+ — ` reads 201 at all three — this
     round mints no id — `^- R-0630 — ` 0 at all three, `^- R-0629 — `,
     `^- R-0429 — `, `^- R-0553 — `, `^- R-0628 — ` and `^- R-0368 — ` 1 each
     at all three, `^Done: R-\d+ — ` 6 at all three, `^Landed: ` 0 at all
     three, and `^Gate: R\d+ — ` 32 at the base and at C2 and 33 at C3, over
     that many DISTINCT keys. HEADER SWEEP at C3 (item 26): report how many
     `Gate: ` lines match `^Gate: R(\d+) — the R(\d+) entry\.` with the second
     numeral one below the first, how many do not, the text of each non-match
     to its first period, and that the R33 pair occurs EXACTLY ONCE.
 G8  The wiring at C4, one commit carrying three pairs. Report, for each pair
     separately, the count of its FROM at the round base and at C4 and of its
     TO at C4: SHCALLFROM goes 1 to 0 with SHCALLTO 0 to 1, while SHIMPFROM and
     SHSIGFROM each read 1 at BOTH — their TOs contain them — with SHIMPTO and
     SHSIGTO each 0 at the base and 1 at C4. Then report the reading that
     covers all three at once: the round-base blob of
     `apps/ui/src/components/shell/RemedyShell.tsx` with SHIMP, SHSIG and
     SHCALL each substituted ONCE, in that order, is BYTE-EQUAL to the C4 blob.
     Report the file's line count at the base and at C4.
 G9  The contract file at C5. Report that
     `git ls-tree 9f14a79e -- tests/ui_contracts/test_remedy_shell_stream.py`
     prints NOTHING, so it is CREATED and not modified, and that the file at C5
     is BYTE-EQUAL to CONTRACT by sha256 over the committed blob against the
     slice extracted from the committed C0a blob.
 G10 The runs, in the PRIMARY checkout, SERIALLY, never two test processes
     alive at once, AT C5 — the commit at which the wiring and its contract are
     both final. In `apps/ui`: `npm run --silent typecheck` EXITS 0 with NO
     output, and `npx vitest run` EXITS 0 at 10 files and 152 tests, UNCHANGED
     from the base reading stated above because this round touches no file
     vitest covers. From the repository root:
     `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at a passed-plus-
     skipped SUM of 421, where the base sum stated above is 413 and CONTRACT is
     what adds the difference, and
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     EXITS 0 at 465. Report each pytest suite's passed and skipped numbers
     SEPARATELY as well as their sum. THE SUM IS THE GATE and a bare passed
     count is not: three data-dependent `pytest.skip(...)` calls move the split
     run to run at an unchanged tree. If any of the four fails, report the real
     values and STOP.
 G11 The red control, at C5, in a DISPOSABLE worktree, never the primary
     checkout. This control runs pytest ONLY, so the worktree needs NO
     `node_modules` and none is linked into it. In that worktree's
     `apps/ui/src/components/shell/RemedyShell.tsx`, the byte string
     consisting of a space followed by streamStatus={stream.status} — 29 bytes,
     no backtick in it, a MID-LINE substring rather than a whole line — occurs
     EXACTLY ONCE; report that count FIRST, and report alongside it the count
     of LINES in that file containing `streamStatus`, which is also 1, the two
     numbers agreeing being the reading item 25 now asks for. Delete that one
     occurrence and report that, run from that worktree's root,
     `python3 -m pytest tests/ui_contracts/test_remedy_shell_stream.py -q -rf`
     EXITS 1 failing exactly one test and no other:
     `TestShellSubscribesToTheStream::test_shell_passes_the_stream_status_to_the_live_panel`.
     Then restore the file, report it byte-identical by sha256, and report the
     same command EXITING 0 at 8 passed. Remove the worktree and report
     `git worktree list` naming only the primary checkout.
 G12 The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 9f14a79e..C5` and that it equals
     the Change set MINUS `.agent/handoff.md` exactly, with none on either side
     alone; the full reading to C6 belongs to the ROUND REPORT (constraint 6).
     Walk `git rev-list --reverse 9f14a79e..C5` and report ONE reading per
     commit: that it has exactly ONE parent, and BOTH numstat cells per path
     from `git show --numstat`, cross-checked against `git diff --numstat`,
     every insertion under 500 and every cell equal to the `+/-` column of your
     `## Commits` table, cell by cell (item 28). C6's own numbers cannot exist
     while C6 is being written, so they belong to the round report (item 14).
     Report also this round's own reflog entries, classified by the OPERATION
     before the first `:` in `%gs`: every pre-C6 entry reads `commit`; give how
     many you classified and `amend`, `rebase` and `cherry` at 0. Assert no
     total over the whole reflog (R-0601).
 G13 Marker leak and trailer. Count LINES BEGINNING with `<<<SLICE ` or
     `<<<END ` in the plan at C1, the ledger at C2 and at C3, the shell at C4,
     the contract file at C5, and the handback at C6 — each is 0.
     `.agent/last_block.md` is NOT in that list and is not expected to be 0,
     being the block's own mirror. Then measure constraint 5 with
     `git log --format=%H%x09%(trailers:key=Co-Authored-By,valueonly) 9f14a79e..HEAD`
     before C6 and report how many commits it lists and how many return a
     NON-EMPTY value — state it as that measurement and never as a universal.
 G14 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 11
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2, C3, C4, C5 and C6 — "exactly one row" scoping to
     that TABLE. Measure its line count with `wc -l` BEFORE committing it; this
     round's commit count is above five, so the cap is 100, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; raw transcripts
     go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~99 % (T001 ✅ · T002 ✅ · T003 ✅ — Client, Badge, Deps-Factory, Browser-Env und Cockpit-Wiring komplett; Integrations-Gate offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R33
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
R33 records the R32 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — amends R-0629 with the F008 R32 instance, a defect in the
reviewer's own block text, and WIRES THE COCKPIT: `RemedyShell` subscribes to
its dashboard's job with `useBrainStream` over `createBrainStreamHostDeps` and
`browserBrainStreamEnv`, and passes the transport status to `RightLivePanel`,
where the badge R29 built finally reads a real one. T003 is complete when this
round lands.

## Next Steps
1. R34 runs the INTEGRATION GATE per docs/agents/integration_gate.md — the full
   suite, once, before closure — and a regression there is a normal repair
   round.
2. Then the closure round per docs/roadmap/STATUS_closure_protocol.md: evidence
   job, a FRESH review zip, the STATUS line and the pull request.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
  The integration gate is the first run that exercises the wired shell at all.
<<<END PLANF008R33

<<<SLICE R0629FROM
Measuring a second file costs one line of the script that is already running.
<<<END R0629FROM

<<<SLICE R0629TO
Measuring a second file costs one line of the script that is already running. F008 R32 INSTANCE, THE THIRD, AND IT ARRIVES THROUGH THE PAGE RATHER THAN THROUGH THE SCRIPT. The R32 block's G10 ordered a red control on `apps/ui/src/api/brainStreamDeps.ts` and printed its target inside a markdown code span, so the two backticks the line really contains were emitted BACKSLASH-ESCAPED; it also called the indent "six leading spaces" where the line stands at TEN. Measured by the worker during the round and by the reviewer after it, at `78be8b8b`: the bytes the block PRINTS occur 0 times in that file, the same bytes with the escaping resolved occur 1 time, and the physical line as it stands occurs 1 time — so the "EXACTLY ONCE" G10 ordered was unmeetable as written, and only the worker's three-way reading kept the control honest. WHAT PRODUCED IT is a reviewer dry run that counted the target as a SUBSTRING: a six-space prefix is contained in a ten-space indent, so the script printed 1 and concealed BOTH errors at once, which is this finding's own lesson arriving one layer down — the count was measured, and the thing measured was not the thing ordered. NOTHING WENT WRONG DOWNSTREAM: the control still discriminated, failing exactly the one test the block named, and the reviewer reproduced that in its own worktree; this is Low, where the R24 instance was Medium, because the round lost a declared deviation rather than a proof. THE FIX IS WIDENED FROM THE COUNT TO THE BYTES. A destructive target is counted as a WHOLE LINE, anchored at both ends, never as a substring — an indentation-agnostic count and a full-line count are reported as two numbers, and they must agree. And any byte string a block orders CHANGED is emitted so that what the page shows is what the file holds: where the target contains a backtick, the block states the literal characters and their count instead of wrapping it in a code span, because the escaping a renderer needs is not in the file being mutated.
<<<END R0629TO

<<<SLICE LEDGER33
Gate: R33 — the R32 entry. R32 PASSED. It recorded the R31 verdict, ruled DECISION F008 D3 on where the cockpit subscribes, and bound the injected environment to real globals, and EVERY GATE WAS RE-RUN BY THE REVIEWER — the suites in the primary checkout and the red control in the reviewer's OWN disposable worktree — rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r32.md` as it survived on disk, `.agent/authored/f008-r32.md` at `a9574427` and `.agent/last_block.md` at `411f30d5` are all sha256 98d37fc6187c27b37cc0ef66411aa98b55cd8180170bc554355a380796cd742e over 29101 bytes and 413 lines, EQUAL to the digest the reviewer emitted and under the 490-line budget DECISION F085 D6 rules. NINE SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R32 494d765d at 40 lines, ENVTEST 3c666294 at 40, ENV 4207facb at 36, DECISION3 a618c170 at 22, and single-line slices for LEDGER32 604236a7, TI1FROM d48699d8, TI1TO da1e2cd9, TI2FROM e60c1fd1 and TI2TO ca1c32b5 — none carrying trailing whitespace on any line, none beginning with a blank line, and each newline-terminated. THE PLAN LANDED FIRST at `db40b59b`, byte-equal to PLANF008R32 at 40 lines under the 50-line cap. DECISION F008 D3 LANDED at `3517f345` as an ordered append whose remainder is a newline plus DECISION3, with the `## DECISION F008 D3` key going 0 to 1 while D2 and D1 each stayed at 1. THE LEDGER APPEND at `abc3f809` is proved twice over: the C2 blob is a byte-exact prefix of it with a 4820-byte remainder equal to a newline plus LEDGER32, and an INDEPENDENT split of the whole file gives 243 units whose LAST is LEDGER32's paragraph, with a one-byte printable flip REJECTED by BOTH readings and the unflipped value ACCEPTED by both. THE SETS HELD — 201 findings at the round base and at C3 with NO id minted and R-0630 still 0, `- R-0429`, `- R-0553`, `- R-0629`, `- R-0628` and `- R-0368` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 31 at the base and 32 at C3 over that many DISTINCT keys, 31 of 32 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R32 pair occurring exactly once. THE SOURCE EDITS ARE PROVED IN THE TWO SHAPES THEY OWE. `apps/ui/src/api/brainStreamDeps.ts` at `78be8b8b` is a PURE APPEND: the base blob is a byte-exact prefix, the remainder equals a newline plus ENV, and the 37 lines that commit's diff ADDS are exactly the remainder's 37 lines IN ORDER — the ordered equality §4.9 gives a code append, never a per-line count (R-0531). `apps/ui/src/api/brainStreamDeps.test.ts` at `17e304bc` carries two REWRITES and an append in ONE commit: TI1FROM and TI2FROM each go 1 at the base to 0, their TOs 0 to 1, and the base blob with BOTH substitutions applied is a byte-exact prefix of the C5 blob whose remainder equals a newline plus ENVTEST. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: `npm run --silent typecheck` EXITS 0 with a zero-byte output stream, `npx vitest run` EXITS 0 at 10 files and 152 tests where the base is 10 and 149 — exactly the three tests ENVTEST adds — `tests/ui_contracts/` EXITS 0 at 409 passed plus 4 skipped = 413, and the five-target state readers plus canary EXIT 0 at 465 passed plus 0 skipped. THE RED CONTROL DISCRIMINATES, measured by the reviewer in its own disposable worktree at `9f14a79e` with `apps/ui/node_modules` SYMLINKED and the primary checkout never written to: the physical line the control names occurs 1x in the file it names and is the only line in it containing `if (!response.ok)`, deleting it EXITS 1 at 1 failed and 14 passed, failing exactly `the browser environment > parses a successful body and refuses a failed status`, and the restored file returns to sha256 73ff9bd3 and EXITS 0 at 15 passed. EIGHT single-parent commits over `cbf6de37`..`9f14a79e`, insertions 413, 282, 13, 23, 2, 37, 43 and 47 in commit order — every one under 500, 413 the maximum — with `git show --numstat` and `git diff --numstat` AGREEING for all eight and every cell equal to the `## Commits` column for the seven rows that table gives numbers for; zero marker lines in all six targets; and an 83-line handback within the 100 eight commits allow. THE TRAILER CONSTRAINT WORKED: R31 left 0 of 7 commits carrying `Co-Authored-By` and the R32 block ordered it, so the reviewer's own reading of `cbf6de37`..`9f14a79e` returns 8 commits with 8 non-empty values — a deviation closed by an ordering constraint rather than by a rewrite of history. THE ROUND DECLARED FOUR DEVIATIONS AND EACH IS SOUND, and the FIRST is the reviewer's own defect, registered above against R-0629 rather than a new id after the open set was searched for the DEFECT: G10 printed its target inside a markdown code span, so its backticks travelled backslash-escaped and its stated six-space indent was ten, and the worker's three-way count — 0 for the bytes as printed, 1 with the escaping resolved, 1 for the physical line — is what kept the control honest. The others are a declared partial read of two large state files, a note that `git commit` reported 413 insertions for `411f30d5` where numstat reads 282 because rewrite detection differs from the column DECISION F104 D1 counts, and a `--no-verify` on C0a alone in a repository whose only hooks are `.git/hooks/*.sample`, which changed nothing. NO FINDING IS REGISTERED AGAINST THE WORKER: every value it reported reproduced.
<<<END LEDGER33

<<<SLICE SHIMPFROM
import styles from "./RemedyShell.module.css";
<<<END SHIMPFROM

<<<SLICE SHIMPTO
import styles from "./RemedyShell.module.css";
import { browserBrainStreamEnv, createBrainStreamHostDeps } from "../../api/brainStreamDeps";
import { useBrainStream } from "../../api/useBrainStream";
<<<END SHIMPTO

<<<SLICE SHSIGFROM
export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
<<<END SHSIGFROM

<<<SLICE SHSIGTO
export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  // The cockpit subscribes HERE rather than in RemedyApp: the shell renders
  // only once a dashboard has loaded, so `dashboard.jobId` is always a real
  // job, where RemedyApp would have to open a stream against an empty id on
  // every URL that carries none (DECISION F008 D3).
  const stream = useBrainStream(dashboard.jobId, (jobId) =>
    createBrainStreamHostDeps(jobId, browserBrainStreamEnv(window)));
<<<END SHSIGTO

<<<SLICE SHCALLFROM
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} />
<<<END SHCALLFROM

<<<SLICE SHCALLTO
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} />
<<<END SHCALLTO

<<<SLICE CONTRACT
"""Contract tests for the cockpit's subscription to the brain stream.

RemedyShell is where the two halves of F008 meet: the client the T003 rounds
built is handed the real endpoints T001 and T002 serve, and its status reaches
the badge. This repository has no DOM environment, so the wiring is gated the
way every other component here is gated — by reading its source. Every
assertion runs against COMMENT-STRIPPED source, because a guard that counted a
token inside a comment would be satisfied by the prose describing the code
rather than by the code (finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHELL = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"
DEPS = REPO_ROOT / "apps" / "ui" / "src" / "api" / "brainStreamDeps.ts"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files contain no string literal holding
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


class TestCommentStripping:
    def test_stripper_removes_a_comment_the_shell_really_carries(self):
        raw = SHELL.read_text()
        assert "// The cockpit subscribes HERE" in raw, "the wiring must keep its WHY comment"
        assert "The cockpit subscribes HERE" not in strip_ts_comments(raw), "stripper must remove it"


class TestShellSubscribesToTheStream:
    def test_shell_subscribes_with_the_dashboard_job_id(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "useBrainStream(dashboard.jobId," in code, (
            "the shell must subscribe with the loaded dashboard's own job id, which "
            "is the reason the call sits here and not in RemedyApp (DECISION F008 D3)"
        )

    def test_shell_builds_its_deps_from_the_real_factory_and_the_browser_env(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "createBrainStreamHostDeps(jobId, browserBrainStreamEnv(window))" in code, (
            "the stream must run against the real endpoints, not a stub"
        )

    def test_shell_passes_the_stream_status_to_the_live_panel(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "streamStatus={stream.status}" in code, (
            "the badge cannot say DELAYED unless the transport status reaches it"
        )

    def test_shell_does_not_compose_the_transport_itself(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "createBrainStreamHost(" not in code, (
            "composition belongs to brainStreamSession.ts, where vitest can test it"
        )


class TestBrowserEnvironmentContract:
    def test_env_is_exported_under_its_own_name(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "export function browserBrainStreamEnv(" in code

    def test_env_degrades_rather_than_claiming_liveness(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "Source === undefined ? null" in code, (
            "a runtime with no EventSource must yield a null source, which is the "
            "unsupported the polling fallback engages on"
        )

    def test_env_reads_its_globals_as_an_argument(self):
        code = strip_ts_comments(DEPS.read_text())
        assert "globalThis" not in code, (
            "reading a global directly would put this module beyond the reach of "
            "the node-environment vitest"
        )
<<<END CONTRACT
