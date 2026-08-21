── STEP T003/8 — F008 SSE event stream — ROUND 30 ────────────────────────────
Round base — the SHA every range gate in this block measures from: 860fc9c3
 (R29's handback, re-read from `git log` at emission, per R-0368.)
Goal:
 Record the R29 verdict and amend the OPEN finding R-0429 with the F008 R29
 instance: a numeral belonging to a DIFFERENT round written into a verdict
 slice, contradicting the clause beside it in the same sentence. This round
 changes NO code. It is the last round of this session, so its handback is
 also the session's return channel.

Bundle, in this commit order:
 C0a  save the block verbatim to `.agent/authored/f008-r30.md`
 C0b  mirror the COMMITTED C0a blob to `.agent/last_block.md`
 C1   `.agent/plan.md` <- PLANF008R30, applied whole
 C2a  `.agent/live_review.md` <- R0429FROM replaced by R0429TO, a REWRITE
 C2b  `.agent/live_review.md` <- LEDGER30, appended
 C3   `.agent/handoff.md`, the handback

Change set — exactly the paths named here and nothing else:
 `.agent/authored/f008-r30.md`, `.agent/last_block.md`, `.agent/plan.md`,
 `.agent/live_review.md`, `.agent/handoff.md`.

Transport:
 This block is on disk at `.remedy-wt/f008-r30.md`, gitignored. Read it there,
 verify its sha256 against the value in your task prompt BEFORE using it, and
 copy those bytes to `.agent/authored/f008-r30.md` for C0a. Never retype it. If
 the digest does not match, STOP and report both values.

Slice convention:
 The authored units below are delimited by a line beginning `<<<SLICE <name>`
 and one beginning `<<<END <name>`; marker lines are NOT part of a slice. Every
 slice is newline-terminated with no trailing whitespace on any line, and every
 count this block orders over a slice is taken over those newline-INCLUDED
 bytes.

Pair shape (§3 item 15). This line is the OUTPUT of the reviewer's containment
test over the final newline-INCLUDED bytes; the label is derived from that
output beside it and is never written on its own (R-0522):
 R0429FROM/R0429TO      TO contains FROM: false  -> REWRITE
 It reads as an append by eye — R0429TO opens with R0429FROM's words and adds
 to them — and it is not one, because R0429FROM is newline-TERMINATED while
 R0429TO continues that sentence on the same line. G5 therefore orders the
 FROM-0x / TO-1x count a rewrite owes.
 FROM uniqueness, counted by the reviewer's own script IN the named file at the
 round base and reported as its output (item 25): R0429FROM occurs 1x in
 `.agent/live_review.md`.

Constraints:
 1. APPLY EVERY SLICE BYTE FOR BYTE — never retype, rewrap, reflow, reindent
    or whitespace-adjust one. A slice that looks wrong is applied as written
    and the objection goes in the handback's deviations section.
 2. The commit order above is fixed: no extra, dropped or reordered commit.
    C1 is the first substantive commit (§3 item 23). C2a precedes C2b so each
    ledger proof reads against a single-purpose commit.
 3. Nothing outside the change set is touched. NO CODE FILE IS EDITED and NO
    DEPENDENCY IS ADDED; `apps/ui/package.json` and `apps/ui/package-lock.json`
    are not opened. `.agent/live_review.md` is the one previously existing file
    this round amends beyond the state files the bundle names.
 4. NO FINDING ID IS MINTED: R-0630 stays free. R-0429 is AMENDED, not
    resolved, and stays OPEN, as do R-0368, R-0553, R-0622, R-0628 and R-0629.
    Write no `Done:` and no `Landed:` line for any of them. The reviewer
    searched the ledger for the DEFECT before routing it here (item 30) and
    R-0429's subject — two clauses of one reviewer-authored text agreeing in
    TOPIC and disagreeing in a NUMERAL — is this defect exactly.
 5. The post-C3 porcelain, `git worktree list` and push output belong to the
    ROUND REPORT, not to `.agent/handoff.md` (R-0371).
 6. Two test processes never run at once, and G7's suites run in the PRIMARY
    checkout (R-0518). This round creates NO worktree and orders NO red
    control: it ships no behaviour to break.
 7. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. Push the
    branch and leave it open; `gh pr list --state open` returned `[]` at the
    reviewer's Phase 0 probe and nothing since has created one.
 8. The session command guard rejects `$(...)`, `; echo $?`, heredocs, shell
    loops and chained `;` commands BY FORM. Write every multi-step gate to a
    script under the gitignored `.remedy-wt/` and run it there, as R29 did;
    commit nothing from it.
 9. THE HANDBACK QUANTIFIES NOTHING IT DID NOT COUNT (R-0553, registered last
    round). Any handback sentence stating "every", "no", "all" or "none" over
    commits, files or rounds names the command that produced the number. State
    the particular you measured, or nothing.
 10. THE HANDBACK'S `## Next` SECTION states, in this order: that the next
    session's FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and
    its SECOND the Open PR Gate (Phase 1 rule 2); that R30 is PENDING REVIEW
    and its verdict is owed by the next round's ledger commit; that the next
    free finding id is R-0630; that R-0368, R-0429, R-0553, R-0622, R-0628 and
    R-0629 are OPEN; and that R31's work is the real `BrainStreamHostDeps`
    factory over the T001 and T002 endpoint plus wiring `useBrainStream` into
    `RemedyApp` and passing its status down to the badge R29 built — the round
    in which this feature's two halves finally meet.

The reviewer's OWN readings, each produced by RUNNING the tool at the round
base `860fc9c3` in the primary checkout, serially, not recalled (R-0625):
`npm run --silent typecheck` in `apps/ui` EXITS 0 with NO output; `npx vitest
run` EXITS 0 at 9 files and 137 tests; `python3 -m pytest tests/ui_contracts/
-q -rf` EXITS 0 at 409 passed plus 4 skipped = 413; G7's five-target state
reader EXITS 0 at 465 passed plus 0 skipped. `npm run lint` in `apps/ui` is RED
at base, which is R-0622 and NOT a gate (R-0364).

Done when — run every command, record its REAL exit code and output:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is EMPTY after
     each of C0a, C0b, C1, C2a and C2b. Per constraint 5 the post-C3 readings
     belong to the round report.
 G2  Transport. Report the sha256, bytes and lines of `.remedy-wt/f008-r30.md`
     as received, of `.agent/authored/f008-r30.md` at C0a and of
     `.agent/last_block.md` at C0b, whether all three are EQUAL, and whether
     they match the digest in your task prompt — which this text cannot carry,
     being unable to hold its own (R-0371).
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r30.md` with `git show`, by their marker lines, take
     the COUNT from that listing, and report it — this block states no numeral
     for it (item 11) — plus each slice's newline-INCLUDED sha256 prefix, bytes
     and lines, and that none carries trailing whitespace on any line.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R30. Its line count is UNDER 50, the
     substring `Steps` occurs, `## Goal` and `## Next Steps` each occur exactly
     once line-anchored, and a `\bF\d{3}\b` match exists — the four properties
     `tests/ui_server/test_dashboard_contract.py` and
     `tests/orchestration/test_test_runner.py` assert about this file.
 G5  The REWRITE at C2a. Read the base bytes with
     `git show 860fc9c3:.agent/live_review.md` into scratch or memory — never
     by writing over the tracked file, which protocol G5 forbids (item 29).
     Report the count of R0429FROM at the round base (expected 1) and at C2a
     (expected 0), and of R0429TO at the base (expected 0) and at C2a
     (expected 1) — the FROM-0x / TO-1x proof a rewrite owes, over the
     newline-INCLUDED bytes the slice convention defines. Report also that the
     base blob with that substitution applied is BYTE-EQUAL to the C2a blob,
     the paragraph COUNT unchanged, and EXACTLY ONE paragraph differing, the
     one beginning `- R-0429 — `.
 G6  The append at C2b, against C2a, two ways that must agree. (a) the C2a blob
     is a byte-exact PREFIX of the C2b blob and the remainder equals a newline
     plus LEDGER30 — report its sha256 prefix, bytes and lines; (b) an
     INDEPENDENT blank-line split of the WHOLE C2b file, terminating newline
     normalised first, has LEDGER30's paragraph as its LAST unit. NEGATIVE
     CONTROL: flip one PRINTABLE ASCII byte of the remainder to another
     printable one; BOTH readings must reject it and both accept the unflipped.
 G7  The sets, at C2a and C2b, line-anchored in `.agent/live_review.md`:
     `^- R-\d+ — ` reads 201 at BOTH — this round mints no id — `^- R-0630 — `
     0 at both, `^- R-0429 — `, `^- R-0553 — `, `^- R-0629 — `, `^- R-0628 — `
     and `^- R-0368 — ` 1 each at both, `^Done: R-\d+ — ` 6 at both,
     `^Landed: ` 0 at both, `^Gate: R\d+ — ` 29 then 30 over that many DISTINCT
     keys. HEADER SWEEP at C2b (item 26): report how many `Gate: ` lines match
     `^Gate: R(\d+) — the R(\d+) entry\.` with the second numeral one below the
     first, how many do not, the text of each non-match to its first period,
     and that the R30 pair occurs EXACTLY ONCE. Then, in the PRIMARY checkout,
     run SERIALLY at C2b — the commit at which both edited state files are
     final. Report each one's passed and skipped numbers SEPARATELY as well as
     their sum, that split moving run to run so a bare passed count is never a
     gate:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     EXITS 0 at 465, and
     `python3 -m pytest tests/ui_contracts/ -q -rf` EXITS 0 at 413.
     If either fails, report the real values and STOP.
 G8  The range, measured from the round base this block's header names and from
     no other SHA. Report `git diff --name-only 860fc9c3..C2b` and that it
     equals the Change set MINUS `.agent/handoff.md` exactly, none on either
     side alone; the full reading to C3 belongs to the ROUND REPORT
     (constraint 5). Report that every commit in the range has exactly ONE
     parent, and BOTH numstat cells per path from `git show --numstat`,
     cross-checked against `git diff --numstat`, every insertion under 500 and
     every cell equal to the `+/-` column of your `## Commits` table, cell by
     cell (item 28).
 G9  Marker leak and reflog. Count LINES BEGINNING with `<<<SLICE ` or `<<<END `
     in the plan at C1, the ledger at C2a and C2b, and the handback at C3 —
     each is 0. `.agent/last_block.md` is NOT in that list and is not expected
     to be 0, being the block's own mirror. Then count THIS round's own reflog
     entries by the OPERATION before the first `:` in `%gs`: every pre-C3 entry
     reads `commit`; report how many you classified and `amend`, `rebase` and
     `cherry` at 0. Assert no total over the whole reflog (R-0601).
 G10 The handback carries every mandated section of
     docs/agents/handback_template.md, the `## Next` content constraint 10
     names in that order, and an item-status table holding exactly one row for
     each of C0a, C0b, C1, C2a, C2b and C3 — "exactly one row" scoping to that
     TABLE. Measure its line count with `wc -l` BEFORE committing it; this
     round's commit count is above five, so the cap is 100, and an overage
     carries a DECISION D15 stated-cause line naming the real count and the
     mandated content that caused it. One line per gate here; raw transcripts
     go in the ROUND REPORT (R-0582).

Handback: completion report + rewrite `.agent/handoff.md`, whose state block repeats verbatim:
 ~98 % (T001 ✅ · T002 ✅ · T003 Client ✅ + Badge ✅, Endpoint-Wiring offen) — Schätzung
──────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF008R30
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
R30 records the R29 verdict and amends R-0429 with the F008 R29 instance: the
R29 verdict slice reported this branch's `Gate: R` count moving 28 to 29, which
is R29's OWN movement, where the round it was judging moved 27 to 28 — and the
clause beside it in the same sentence gave the correct reading. It changes no
code. T003's client is complete and the DELAYED badge now sits on the live
pill, gated by a source contract; only the endpoint wiring is left.

## Next Steps
1. R31 builds the real `BrainStreamHostDeps` factory over the endpoint T001 and
   T002 shipped — `openSource`, `readSnapshotSeq`, `readTail` and `schedule`,
   with its own vitest tests — then wires `useBrainStream` into `RemedyApp` and
   passes its status down to the badge: the round in which this feature's two
   halves meet.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The wiring round touches `RemedyApp.tsx`, the one file every cockpit surface
  renders through, so its blast radius is wider than any round since R4.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
<<<END PLANF008R30

<<<SLICE R0429FROM
An ordinal is a cross-reference, and an unresolved cross-reference is the one error a careful linear read cannot see.
<<<END R0429FROM

<<<SLICE R0429TO
An ordinal is a cross-reference, and an unresolved cross-reference is the one error a careful linear read cannot see. F008 R29 INSTANCE, IN A VERDICT SLICE AND INSIDE A SINGLE SENTENCE, WHERE THE TWO CLAUSES SIT SIX WORDS APART RATHER THAN TWO HUNDRED LINES. LEDGER29, applied at `210cc4a0`, reports of the round it was judging that ``Gate: R`` went "28 to 29 over that many DISTINCT keys, twenty-seven of twenty-eight headers matching the shape". Both halves describe the SAME set at the SAME two revisions and they disagree: measured by the reviewer at `1cf2280b` and `fcea57b5`, R28's ledger held 27 line-anchored `Gate: R` entries over 27 distinct keys at C2a and 28 over 28 at C2b, so the header clause is right and the transition clause is wrong. WHAT PRODUCED IT is worth more than the correction: 28-to-29 is R29's OWN movement, ordered as such in the R29 block's G7, and the reviewer drafted that gate list and this verdict paragraph in one sitting — the number did not come from nowhere, it came from the ADJACENT round. This finding as first written blames DISTANCE, "the two clauses are far apart", and that diagnosis is now falsified by its own second instance, in which adjacency did not help at all because the numerals were never resolved against a measurement in either case. NOTHING WENT WRONG DOWNSTREAM: every R28 gate is reproducible and the reviewer reproduced all of them out of the committed blobs, no gate consumed the sentence, and R28's verdict of PASS is unaffected — this is Low, where the R16 instance was also Low. THE CORRECTION IS THIS PARAGRAPH AND NOT A REWRITE, per checklist item 20: the landed sentence stays and is read with this one beside it. THE FIX IS WIDENED FROM AN ORDINAL TO ANY NUMERAL A VERDICT SLICE REPORTS. Before emission, every numeral in a slice that reports a MEASUREMENT is resolved against the reviewer's own recorded reading FOR THE ROUND THAT SLICE DESCRIBES, by re-reading the measurement rather than the draft, and a numeral that appears twice for one property is required to agree with itself. A verdict slice is the permanent record of a round nobody will re-measure, so a wrong number in it is believed for as long as the ledger lasts.
<<<END R0429TO

<<<SLICE LEDGER30
Gate: R30 — the R29 entry. R29 PASSED. It recorded the R28 verdict, amended R-0553 with the F008 R28 instance and shipped the DELAYED badge, and EVERY GATE WAS RE-RUN BY THE REVIEWER out of the committed blobs rather than read back out of the handback. TRANSPORT EQUAL THREE WAYS: `.remedy-wt/f008-r29.md`, `.agent/authored/f008-r29.md` at `e25e7f91` and `.agent/last_block.md` at `72eb21ea` are all sha256 21875ebb9d405ff6a7e5889cf2d3033bebc2bb1616c60d575e256339449b80b3 over 33559 bytes and 490 lines, equal to the digest the reviewer emitted and exactly at the 490-line budget DECISION F085 D6 rules. FOURTEEN SLICES by the reviewer's own ordered extraction out of the committed C0a blob — PLANF008R29 21396c53 at 40 lines, DECISION2 8ec63baa at 32, R0553TO 11a35388 at 23, PILL 1d49c044 at 21, PILLTEST 7dff6c4e at 58, PILLCSS 9aa75a6c and PANELIMPORTTO fce79824 at 2 each, and single-line slices for R0553FROM 47e4533c, LEDGER29 fb9ceebf, PANELIMPORTFROM b86ff519, PANELSIGFROM bb5d1233, PANELSIGTO 9780edb1, PANELCALLFROM 7be59d57 and PANELCALLTO 6b16deee — none carrying trailing whitespace on any line. THE PLAN LANDED FIRST at `b727d5e1`, byte-equal at 40 lines under the 50-line cap, and DECISION F008 D2 landed at `a9c0b2aa` as an ordered append whose remainder is a newline plus DECISION2, with the `## DECISION F008 D2` key going 0 to 1 and D1 unmoved at 1. THE REWRITE at `bade3be8` is proved twice over: R0553FROM 1 at the base and 0 after, R0553TO 0 then 1 — the FROM-0x/TO-1x count a rewrite owes — and, independently, the base blob with that one substitution applied is BYTE-EQUAL to the C2a blob, with 239 blank-line paragraphs before and after, exactly ONE differing, and that one the `- R-0553 — ` paragraph at index 145. THE APPEND at `210cc4a0` is a byte-exact prefix of the C2a blob plus a 3621-byte remainder equal to a newline plus LEDGER29, agreed by an INDEPENDENT split of the whole file into 240 units whose LAST is LEDGER29's paragraph, with a one-byte printable flip REJECTED by BOTH readings. THE SETS HELD — findings 201 at both revisions with NO id minted, `- R-0630` 0, and `- R-0553`, `- R-0629`, `- R-0628` and `- R-0368` 1 each and all OPEN, `Done:` 6, `Landed:` 0, `Gate: R` 28 at C2a and 29 at C2b over that many DISTINCT keys, 28 of 29 headers matching the shape with `Gate: R1 — the F255 R21 entry.` the single non-match, and the R29 pair occurring exactly once. THE BADGE IS PROVED BY CONSTRUCTION AND BY COLOUR. `LiveStatusPill.tsx` at `573f28c2` is BYTE-EQUAL to PILL and `tests/ui_contracts/test_live_status_pill.py` to PILLTEST; the CSS is a byte-exact prefix plus PILLCSS as an exact suffix; and the three `RightLivePanel.tsx` pairs, each reported separately, read FROM 1 at the base with PANELSIG and PANELCALL going FROM-0/TO-1 and PANELIMPORT — the one pair whose containment test printed true — carrying a TO-1 reading only, the one-pass replacement reproducing the C3 blob byte for byte at 51 lines to 52. THE RUNS ARE THE REVIEWER'S OWN, serial, in the primary checkout: typecheck EXITS 0 with no output, `npx vitest run` EXITS 0 at 9 files and 137 tests UNCHANGED because no file vitest covers was touched, `tests/ui_contracts/` EXITS 0 at 409 passed plus 4 skipped = 413 — the base's 406 plus exactly the seven tests PILLTEST adds, with the skipped set unmoved — and the state readers plus canary EXIT 0 at 465. BOTH RED CONTROLS DISCRIMINATE, measured by the reviewer in its own disposable worktree at `573f28c2` with `node_modules` and `dist` SYMLINKED and the primary checkout never touched, agreeing with the worker: each ordered byte string occurs 1x in the file the control names, deleting the delayed arm EXITS 1 failing exactly `test_a_delayed_stream_says_delayed` and `test_the_transport_status_is_read_before_the_dashboard_liveness`, and turning `/>RECONNECTING</div>` into `/>LIVE</div>` EXITS 1 failing exactly `test_a_reconnecting_stream_says_so_rather_than_live`, each restored to sha256 1d49c044 and the file then EXITING 0 at 7 passed. EIGHT single-parent commits, every insertion under 500 with 490 the maximum and every numstat cell equal to the `## Commits` column; zero marker lines in all nine targets; seven reflog operations all `commit`; an 86-line handback within the 100 eight commits allow; the tree clean and the primary checkout the only worktree. THE ROUND DECLARED FOUR DEVIATIONS AND EACH IS SOUND, the first two being the reviewer's own defects rather than the worker's: DECISION2 opens with a blank line while G4 ordered the remainder to equal a newline plus DECISION2, so the applied file carries TWO blank lines above the `## DECISION F008 D2` heading where D1 has ONE — the worker applied it as ordered, as constraint 1 requires, and objected, and the reviewer confirms the count; the round's seven commits carry a `Co-Authored-By` trailer this session's harness adds, reported as G12's measurement of 187 commits with 26 non-empty rather than as a universal, which is R-0553's counter-measure obeyed in the round that registered it; `npm run lint` was correctly not run; and the guard-refused commands were routed through scripts in gitignored scratch. ONE DEFECT IN THE REVIEWER'S OWN VERDICT SLICE IS REGISTERED ABOVE against R-0429 rather than a new id, the open set having been searched for the DEFECT first: LEDGER29 gave R28's `Gate: R` transition as 28-to-29, which is R29's own movement, six words from the clause that gives the correct 27-of-28 reading.
<<<END LEDGER30
