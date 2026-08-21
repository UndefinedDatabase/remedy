── STEP R9/1 — F008 SSE event stream · SESSION CLOSE ─────────
Goal:        Record the R8 verdict, register R-0615 and R-0616, and close
             this session cleanly at its round cap. This round writes no
             code. R8 PASSED and T001's stream reader is built and reviewed;
             both new findings are defects in the reviewer's own block text
             that the R8 worker declared and the reviewer re-measured, not
             defects in any round's work. A session that ends at its limit
             with a written handoff is a SUCCESS, not a failure (self-drive
             protocol G7).

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0615 and R-0616 and record the R8 verdict ·
             C3 write the session-closing handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r9.md      (C0a, new)
             - .agent/last_block.md            (C0b, rewrite)
             - .agent/plan.md                  (C1, rewrite)
             - .agent/live_review.md           (C2, append)
             - .agent/handoff.md               (C3, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r9.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R9 is
    applied with its trailing newline INCLUDED and is the ENTIRE content of
    its file. LEDGER9 is applied as a newline plus its body, appended to
    `.agent/live_review.md` after exactly one blank line. Every file ends
    with exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3. `.agent/plan.md` is
    advanced at C1, the first substantive commit, and the two findings are
    registered at C2.
 4. LEDGER9 carries THREE paragraphs, blank-line separated, applied together
    in C2: the R-0615 registration, the R-0616 registration, and the
    `Gate: R9` entry holding the R8 verdict. R-0615 and R-0616 are the only
    ids minted, so the next free id becomes R-0617.
 5. NO PRODUCTION CODE. No path under packages/, apps/, tests/ or docs/ is
    touched. This round writes only `.agent/` state.
 6. `git status --porcelain` is empty after every commit and at the handback,
    and `git worktree list` names the primary checkout alone. No worktree is
    created: nothing this round is destructive.
 7. Two pytest processes never run at once, and every suite runs in the
    PRIMARY checkout.
 8. The reviewer's own readings at `95326a5f`, taken before this block was
    emitted and RE-DERIVED by the gates below rather than trusted: the
    combined state-reader suite exits 0 with `passed + skipped` equal to 414,
    and `tests/docs/` exits 0 at 295. Count by passed-plus-skipped, never by
    a bare passed count — data-dependent `pytest.skip(...)` calls in
    `test_brain_view_model.py` and `test_dashboard_contract.py` move the
    split at an unchanged tree.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature: T001's route does not exist yet, so the branch is not in a
    closeable state and no pull request is owed. It is pushed and left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r9.md` at C0a and
     of `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r9.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256/bytes/lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R9. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER9 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST THREE units, in order, the
     three paragraphs of LEDGER9. NEGATIVE CONTROL: flip one byte of the
     remainder and report BOTH readings reject it, the unflipped accepted.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1
     and C2: `^- R-\d+ — ` reads 186 then 188 — constraint 4, two ids are
     minted — `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at both, and
     `^Gate: R\d+ — ` reads 8 then 9 with the nine keys DISTINCT. Each of
     `^- R-0615 — ` and `^- R-0616 — ` reads 0 then 1, and `^- R-0617 — ` is
     0 at both.
 G7  The state readers still pass, in the PRIMARY checkout, run SERIALLY,
     never two pytest processes at once. Report the exit code and
     `passed + skipped` of:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     It exits 0 and sums to 414. Then report the same two values for
     `python3 -m pytest tests/docs/ -q -rf`, which exits 0 and sums to 295.
     Per constraint 8 report the SUM, never a bare passed count, and do not
     read a skip as a failure. `.agent/` state is what several of these
     readers parse, which is why they are gated on a round that writes only
     state.
 G8  Range. With BASE `95326a5f`, `git diff --name-only BASE..C3` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C3 has exactly one parent. Report each commit's INSERTION count
     from `git show --numstat`, all under 500, and compare them cell by cell
     against the `+/-` column of the handback's `## Commits` table, reporting
     agreement. C3's own numbers belong to the round report (R-0149).
 G9  Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `.agent/handoff.md` at C3. Every count is 0.
 G10 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs`
     — is `amend`, `rebase` or `cherry`; it is 0. Count by operation, never
     by substring; do not order that every entry read `commit:`; no total.
 G11 The branch is pushed and NO pull request exists. Report the real output
     of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G12 Handback. `.agent/handoff.md` at C3 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2 and C3 exactly once each. Report its line count;
     the cap is 60, this round having five commits, and an overage carries a
     DECISION D15 stated-cause line naming the mandated content that caused
     it. Its `## Next` section states, in this order, that the next session's
     FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its
     SECOND the Open PR Gate (Phase 1 rule 2), which finds no open pull
     request and therefore continues on this branch at R10, whose work is
     the route named in `.agent/plan.md`.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 30 % (F008 beansprucht · neun Urteile im Ledger ·
            DECISION F008 D1 vollständig umgesetzt · T001-Leser gebaut und
            geprüft — SSE-Rahmen, geteilte Hülle, Herzschlag-Kadenz · Route
            und Socket-Schreiber folgen in R10 · Session endet an ihrem
            Rundenlimit mit geschriebenem Handoff) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R9
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
R9 records the R8 verdict, registers R-0615 and R-0616, and closes this
session at its round cap. This round writes no code. T001's stream READER is
built and reviewed as of R8: the SSE frame builders, the safe per-event
envelope both event transports share, and the frame generator that carries the
ledger position as the event id and heartbeats while idle. No route reaches it
yet, so no cockpit request can open a stream.

## Next Steps
1. R10 wires the reader to the route: `GET /api/jobs/<jid>/events/stream` as a
   six-part path branch beside the existing `events-since` handler in
   `_RemedyHandler.do_GET`, the response writer that drains the generator into
   the socket, and 404 for an unknown job before one byte of stream.
2. R11 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
3. R12 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer whose transcript must byte-equal the ledger — then T003's client
   hook and fallback, then the integration gate before closure.

## Risks
- A streaming handler holds a socket open. The reader takes `should_continue`
  from its caller, so R10's writer must bound the loop by the peer's
  disconnect, and no test may drive that route over a real socket without a
  hard timeout and a guaranteed close.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0614, R-0615 and R-0616 stay routed to a paydown branch,
  together with promoting the fix clauses of R-0387 and R-0573 into the §3
  checklist.
<<<END PLANF008R9

<<<SLICE LEDGER9
- R-0615 — Low — AN ORDERED-EQUALITY GATE WRITTEN FOR ONE PAIR WAS ORDERED OVER A COMMIT THAT CARRIES TWO, SO ITS LITERAL READING IS FALSE BY CONSTRUCTION. G8 of the F008 R8 block, saved at `dd4c36ff`, orders that "the lines C3's diff ADDS to `packages/orchestration/ui_server.py` are, IN ORDER, exactly the HELPERS TO lines absent from its FROM body". Constraint 5 of the SAME block puts BOTH pairs in C3, so that commit's added set is 78 lines of which the first 4 belong to the SUMMARY rewrite and only the remaining 74 belong to the APPEND pair the gate names. The literal comparison is therefore False for every possible round, and an honest worker can only declare it. Re-measured by the reviewer at `95326a5f`: the diff adds 78 lines, `added[0:4]` equals SUMMARY TO in order, `added[4:78]` equals the 74 HELPERS TO lines other than the anchor in order, and the naive whole-diff comparison returns False — the same three readings the worker reported. §4.9's obligation is PAIR-SCOPED and the gate dropped the scope while keeping the words: the ordered reading is correct, its RANGE is not. Item 22 of the §3 checklist governs a sentence quantifying across COMMITS and item 14 which commits a per-commit gate can reach; neither reaches a gate whose range is wrong WITHIN one commit, which is where this lands. THE COUNTER-MEASURE: a §4.9 ordered-equality gate names the SLICE BOUNDARIES it compares against — "added[0:n] is TO-1, added[n:] is TO-2 minus its anchor" — whenever the commit it is ordered over carries more than one pair, and a block that puts two pairs in one commit writes that arithmetic at emission, where the reviewer already knows both slice lengths. It cost a declared deviation and not a round, because the worker measured both readings and reported the pair-scoped one rather than choosing between them.

- R-0616 — Low — A VERDICT SLICE STATED A PROPERTY OF A SCRATCH ARTIFACT THAT NO BLOCK FIXES AND NO ACTOR SHARES. The `Gate: R8` entry landed at `dd762b80` describes R7's confirmed readings as "empty ruff multisets at base and at head behind a red control that returned four codes". The red control is a throwaway file each actor writes for itself under `.remedy-wt/` to prove its extractor can produce a reading at all (R-0573), and NOTHING in any block fixes its contents — so its code count is a property of whichever file that actor happened to write. Measured: the reviewer's control returns four distinct codes, the R7 worker's returns three and the R8 worker's returns two, all three non-empty and all three discharging the ordered property exactly. The sentence is therefore true of one actor's scratch file and reads as though it were true of the evidence, which is the R-0526 class — a claim about bytes nobody fixed — arriving through a VERDICT rather than through a constraint. The landed entry is NOT rewritten; this registration is the dated correction item 20 prescribes. THE COUNTER-MEASURE: a verdict names the PROPERTY a control established — non-empty at non-zero exit — and never that control's own contents, and the same rule binds any block clause describing scratch an actor supplies for itself. The R8 worker caught it unprompted and declared it as a disagreement with the block rather than adopting the number, which is the behaviour that turned a wrong sentence into a registration instead of a precedent.

Gate: R9 — the R8 entry. R8 PASSED with NO finding against its work, and the two findings above are against the reviewer's own block text rather than the round. R8 re-issued the bundle R7 halted on, with R-0614's two characters corrected and every other byte unchanged, and it landed T001's stream READER: the SSE frame builders, the shared per-event envelope, and the frame generator that carries the ledger position as the SSE event id and heartbeats a comment frame while idle. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `95326a5f` rather than reading the handback's numbers back. Transport EQUAL three ways at sha256 c8bd326868b2e828f9b8510a1c8ddbee9c8cdd19447217869985d9831c72083a over 31403 bytes and 489 lines; seven slices by the reviewer's own ordered extraction; `.agent/plan.md` at `ee08a6cf` byte-equal to its slice at 45 lines under the cap; the ledger append at `dd762b80` a byte-exact prefix plus a 7208-byte remainder equal to a newline plus LEDGER, agreed by an INDEPENDENT blank-line split into 198 units whose LAST THREE equal LEDGER's three paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped value accepted by both; the registered set moving 185 to 186 with zero `Done:` and zero `Landed:` lines, `Gate: R` going 6 to 8 over eight DISTINCT keys, R-0614 appearing exactly once and R-0615 nowhere, so exactly one id was minted; the SUMMARY FROM going 1 to 0 while the C3 blob contains the HELPERS TO body exactly once; `tests/ui_server/test_sse_stream.py` at `dc5e95db` byte-equal to TESTSSE at 147 lines; seven single-parent commits whose insertions read 489, 442, 22, 6, 78, 147 and 66, every one under the 500-line cap and agreeing cell by cell with the handback's `## Commits` column; zero marker lines in any of the five targets; a reflog whose operations are `commit` throughout; an 84-line handback under its cap naming C0a through C5 once each; and the tree clean with the primary checkout the only worktree, the branch pushed and `gh pr list` returning an empty list. THE RUNS ARE THE REVIEWER'S OWN: the state readers exit 0 at 414, `tests/docs/` exits 0 at 295, the new file collects 14, and 400 plus 14 reconciles exactly against the base the reviewer measured at `83408011`. THE RED PROOF IS REAL AND THE REVIEWER RE-RAN IT in a disposable worktree, never in the primary checkout: with `packages/orchestration/ui_server.py` alone reverted to its `83408011` blob the new file EXITS 1 at 14 failed with NO test passing, and restored to its `95326a5f` blob the same command EXITS 0 at 14 passed. A 14-of-14 red is honest here because every test in the file reads a frame the reverted code cannot build, which is exactly the coupling R5's 6-and-1 split did not have. RUFF IS BLIND TO THE DEFECT R-0614 RECORDS and says so: the multiset is empty at base and at head, equal across the change, behind a control shown non-empty first — and the frames are covered by the suite and the red proof, never by the linter.
<<<END LEDGER9
