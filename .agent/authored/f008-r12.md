── STEP R12/1 — F008 SSE event stream · SESSION CLOSE ────────
Goal:        Record the R11 verdict, register R-0618, and close this session
             cleanly at its round cap. This round writes no code. R11 PASSED
             and T001 is complete: reader, route, socket writer, 404 before the
             stream, the per-job cap answering 429, and the framing golden.
             R-0618 is a defect in the reviewer's own R11 block text that the
             R11 worker declared and the reviewer re-measured, not a defect in
             any round's work. A session that ends at its limit with a written
             handoff is a SUCCESS, not a failure (self_drive_protocol G7).

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0618 and record the R11 verdict · C3 write the
             session-closing handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r12.md      (C0a, new)
             - .agent/last_block.md            (C0b, rewrite)
             - .agent/plan.md                  (C1, rewrite)
             - .agent/live_review.md           (C2, append)
             - .agent/handoff.md               (C3, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r12.md, extracted by its marker lines — never retyped,
    rewrapped, reflowed or edited. A slice that looks wrong is APPLIED AS
    WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R12 is applied with
    its trailing newline INCLUDED and is the ENTIRE content of its file.
    LEDGER12 is applied as a newline plus its body, appended to
    `.agent/live_review.md` after exactly one blank line. Every file ends with
    exactly one newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3. `.agent/plan.md` is
    advanced at C1, the first substantive commit, ahead of the ledger append at
    C2 (§3 checklist item 23).
 4. LEDGER12 carries TWO paragraphs, blank-line separated, applied together in
    C2: the R-0618 registration and the `Gate: R12` entry holding the R11
    verdict. R-0618 is the only id minted, so the next free id becomes R-0619.
 5. NO PRODUCTION CODE. No path under packages/, apps/, tests/ or docs/ is
    touched. This round writes only `.agent/` state.
 6. `git status --porcelain` is empty after every commit and at the handback,
    and `git worktree list` names the primary checkout alone. No worktree is
    created: nothing this round is destructive.
 7. Two pytest processes never run at once, and G7's counting suites run in the
    PRIMARY checkout — a fresh worktree has no `apps/ui/node_modules` and its
    pass counts are untrustworthy in both directions (R-0518). This round
    orders no destructive gate, so that clause has nothing to collide with.
 8. The reviewer's own readings at `aa22db60`, taken before this block was
    emitted and RE-DERIVED by the gates below rather than trusted: the combined
    state-reader suite exits 0 with `passed + skipped` equal to 440, and
    `tests/docs/` exits 0 at 295. Count by passed-plus-skipped, never by a bare
    passed count — data-dependent `pytest.skip(...)` calls in
    `test_brain_view_model.py` and `test_dashboard_contract.py` move the split
    at an unchanged tree.
 9. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature: T002 and T003 are unbuilt, so the branch is not in a closeable
    state and no pull request is owed. It is pushed and left open.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r12.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r12.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256/bytes/lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R12. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER12 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, the two
     paragraphs of LEDGER12. NEGATIVE CONTROL: flip one byte of the remainder
     and report BOTH readings reject it, the unflipped accepted by both.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1 and
     C2: `^- R-\d+ — ` reads 189 then 190 — constraint 4, one id is minted —
     `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at both, and
     `^Gate: R\d+ — ` reads 11 then 12 with the twelve keys DISTINCT.
     `^- R-0618 — ` reads 0 then 1 and `^- R-0619 — ` is 0 at both. Report also
     that LEDGER12's `Gate:` header matches the header shape of the entries
     already in that file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be one
     less than the first and the R12 pair to occur exactly once (§3 item 26).
     Report the number of `^Gate: ` lines that do NOT match that pattern; it is
     1, and that line is `Gate: R1 — the F255 R21 entry.`, which gated the
     PREVIOUS feature's last round and has no F008 predecessor by construction.
 G7  The state readers still pass, in the PRIMARY checkout, run SERIALLY, never
     two pytest processes at once. Report the exit code and `passed + skipped`
     of:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     It exits 0 and sums to 440. Then report the same two values for
     `python3 -m pytest tests/docs/ -q -rf`, which exits 0 and sums to 295. Per
     constraint 8 report the SUM, never a bare passed count, and do not read a
     skip as a failure. `.agent/` state is what several of these readers parse,
     which is why they are gated on a round that writes only state.
 G8  Range. With BASE `aa22db60`, `git diff --name-only BASE..C3` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C3 has exactly one parent. Report each commit's INSERTION count from
     `git show --numstat` for the commits BEFORE C3, all under 500, and compare
     them cell by cell against the `+/-` column of the handback's `## Commits`
     table, reporting agreement. Both columns come from `git diff --numstat`,
     never from a file's line counts before and after (§3 item 28). C3's own
     numbers belong to the round report (R-0149).
 G9  Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and
     `.agent/handoff.md` at C3. Every count is 0.
 G10 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs` —
     is `amend`, `rebase` or `cherry`; it is 0. Count by operation, never by
     substring; no total is asserted.
 G11 The branch is pushed and NO pull request exists. Report the real output of
     `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G12 Handback. `.agent/handoff.md` at C3 carries the sections
     docs/agents/handback_template.md mandates and an item-status table naming
     C0a, C0b, C1, C2 and C3 exactly once each. Report its line count; the cap
     is 60, this round having five commits, and an overage carries a DECISION
     D15 stated-cause line naming the mandated content that caused it. Its
     `## Next` section states, in this order, that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
     Open PR Gate (Phase 1 rule 2), which finds no open pull request and
     therefore continues on this branch at R13, whose work is T002 as named in
     `.agent/plan.md`.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 50 % (F008 beansprucht · zwölf Urteile im Ledger ·
            T001 KOMPLETT: Leser, Route, Socket-Schreiber, 404 vor dem ersten
            Byte, Verbindungsdeckel mit 429, Rahmen-Golden · T002
            Last-Event-ID-Resume und der Trennungs-Hammer folgen in R13 · dann
            T003 Client-Hook und Fallback · Session endet an ihrem Rundenlimit
            mit geschriebenem Handoff) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R12
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
R12 records the R11 verdict, registers R-0618, and closes this session at its
round cap. This round writes no code. T001 is COMPLETE and reviewed as of R11:
the frame builders and the shared envelope, the frame generator that carries
the ledger position as the SSE event id and heartbeats while idle, the
six-part route, the socket writer that ends the loop when the peer goes away,
404 before one byte of stream, the per-job slot cap answering 429, and the
framing golden that pins the wire bytes.

## Next Steps
1. R13 begins T002: Last-Event-ID resume, read from the request header and
   falling back to the query cursor, replaying exactly the missed span from the
   ledger — which IS the buffer, so there is no in-memory ring to lose.
2. R14 adds T002's forced-disconnect hammer: kill the connection mid-stream N
   times and require the client transcript to byte-equal the ledger's envelope
   sequence.
3. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- The slot registry is process-global mutable state. Every test that acquires a
  slot clears it first, and the release runs in a `finally`; if either
  discipline lapses, a leaked slot makes a later round's 429 test pass for the
  wrong reason.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0614, R-0615, R-0616, R-0617 and R-0618 stay routed to a
  paydown branch, together with promoting the fix clauses of R-0387 and R-0573
  into the §3 checklist.
<<<END PLANF008R12

<<<SLICE LEDGER12
- R-0618 — Low — A GATE ORDERED A STRING TO OCCUR EXACTLY ONCE IN A FILE WHILE THE SAME BLOCK'S OWN TO SLICE WROTE IT TWICE, SO THE COUNT WAS FALSE FOR EVERY POSSIBLE ROUND. G8 of the F008 R11 block, saved at `a63dd4ab`, orders that "the C3 blob contains `429` exactly once while `c9367141` contains it 0 times". The base half is correct and the reviewer measured it. The head half is not: the CAPTO slice of that same block contains `429` TWICE — once in the comment `# 429 for the same reason and in the same window` and once in the call `_safe_error(429, "too many streams for this job")` — so the applied file necessarily holds two. Re-measured by the reviewer at `aa22db60`: `429` occurs 2 times in the C3 blob at `16b544e7`, 0 times at `c9367141`, and 2 times in the CAPTO slice itself. The R11 worker applied CAPTO byte for byte as constraint 1 required, measured 2, reported both numbers and declared the disagreement rather than editing a comment to make the reviewer's arithmetic come true — which is exactly the behaviour that turns a reviewer slip into a registration instead of a corrupted slice. §3 checklist item 2 forbids a "must be 0" gate over a string a TO in the same block writes, and item 6 requires an "exactly 1x" gate to be checked against what the TARGET FILE already holds; the reviewer performed item 6's check, found 0 at the base, and never performed item 2's check against its own TO, because item 2 is worded for ZERO-gates alone. THE COUNTER-MEASURE, routed to a paydown branch with the other reviewer-text findings: widen item 2 from "must be 0" to ANY exact-count gate, so that a gate ordering N occurrences of a string is required to count that string in every TO slice of the same block that targets the same file and to state the sum, base plus slices, as the ordered value. A count gate has two inputs and this checklist has only ever bound one of them.

Gate: R12 — the R11 entry. R11 PASSED with NO finding against its work, and R-0618 above is against the reviewer's own block text rather than the round. R11 CLOSED T001: a per-job slot registry under a `threading.Lock`, the route answering 429 beyond the cap and before the slot is taken, the slot returned in a `finally` so a raising handler cannot leak capacity, and the framing golden that pins the exact bytes a client parses. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `aa22db60` rather than reading the handback's numbers back. Transport EQUAL three ways — the scratch block, `.agent/authored/f008-r11.md` at `a63dd4ab` and `.agent/last_block.md` at `6aff2607` — at sha256 cc321df189aec69d3c4156b922693546c7e8553afa9f8faa11673240a5a04904 over 30004 bytes and 464 lines. NINE SLICES by the reviewer's own ordered extraction out of the committed C0a file, newline-included, every digest matching: PLANF008R11 a70942c1, LEDGER11 ec8b2dac, THREADFROM 25ba394c, THREADTO 7cbe3f2c, SLOTFROM 3562a4b8, SLOTTO df42336d, CAPFROM 9656b180, CAPTO d164cb45 and TESTS11 07c2e468. THE PLAN LANDED FIRST at `a91ed9ba`, byte-equal to PLANF008R11 at 43 lines under the 50-line cap, which is §3 checklist item 23 met rather than claimed. THE LEDGER APPEND at `175b94fa` is a byte-exact prefix plus a 5506-byte remainder equal to a newline plus LEDGER11, agreed by an INDEPENDENT blank-line split into 204 units whose LAST TWO equal LEDGER11's two paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped value ACCEPTED by both; the registered set moved 188 to 189 with zero `Done:` and zero `Landed:` lines at both commits, `Gate: R` going 11 over eleven DISTINCT keys, R-0617 appearing exactly once and R-0618 nowhere, so exactly the one ordered id was minted. THE SOURCE COMMIT IS PROVED CONSTRUCTIVELY, not merely counted: the reviewer applied the three FROM/TO slices to the `c9367141` blob itself and the result is BYTE-EQUAL to the C3 blob at `16b544e7`, each FROM having occurred exactly once there. The test append at `62b2cf2b` is a byte-exact prefix, TESTS11 an exact suffix, and the 114 lines that diff ADDS are exactly TESTS11's 114 lines IN ORDER. SEVEN single-parent commits whose insertions read 464, 301, 18, 4, 47 and 114 before the handback commit, every one under the 500-line cap and agreeing cell by cell with the handback's `## Commits` column, read from `git diff --numstat` on both sides. ZERO marker lines in any of the five targets, a reflog whose operations over this round's own commits are `commit` seven times with `amend`, `rebase` and `cherry` at 0 each, an 85-line handback under its 100-line cap naming C0a through C5 once each, the tree clean with the primary checkout the only worktree, the branch pushed to `aa22db60` and `gh pr list` returning an empty list. THE RUNS ARE THE REVIEWER'S OWN: the state readers exit 0 at 440 passed plus 0 skipped, `tests/docs/` exits 0 at 295 plus 0, and the SSE file exits 0 at 40 both alone and inside the directory run — so the 13 tests TESTS11 adds reconcile 427 to 440 exactly. THE RED PROOF IS REAL AND THE REVIEWER RE-RAN IT in its own disposable worktree, never in the primary checkout: with `packages/orchestration/ui_server.py` alone reverted to its `c9367141` blob the file EXITS 1 at 29 passed and 11 ERRORS, every one an `AttributeError` naming `_SSE_SLOTS_PER_JOB` at `setup_method`, and restored to its C4 blob the same command EXITS 0 at 40. The 29 survivors include the framing-golden tests by design — a golden pins behaviour that already existed — which is why the block ordered the colour and never a count. RUFF IS EQUAL ACROSS THE CHANGE, empty multiset at base and at head, behind a control shown non-empty at non-zero exit through the same extractor. ONE OBSERVATION, NOT A FINDING: G12 named the ruff command without an output-format flag, and this ruff's default rendering puts the rule code first rather than after the locator, so the worker's first extractor read zero codes from a control that had exited 1 — the worker caught that from the control itself, corrected the extractor and re-ran, which is the red control doing precisely the job R-0463 gave it.
<<<END LEDGER12
