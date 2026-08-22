── STEP T003 (record round, before round one of DECISION F009 D19) — F009 ──
Goal:        Put this session's second verdict and its measured design on disk
             before the session ends. The round records the R17 verdict and
             rules DECISION F009 D19, which cuts the dispatch round in two on a
             measurement the reviewer took rather than on an estimate. It writes
             NO production code, which G9 measures rather than asserts: a
             verdict that lives only in a session's chat is lost when that
             session ends.

Fortschritt: ~73 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und das vollständige Vokabular stehen, der
             Dispatch ist geschnitten, aber noch nicht gebaut) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R17 verdict
             · C3 DECISION F009 D19 · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r18.md` (NEW, C0a)
             `.agent/last_block.md` (C0b)
             `.agent/plan.md` (C1)
             `.agent/live_review.md` (C2)
             `.agent/decisions.md` (C3)
             `.agent/handoff.md` (C4)
             NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched.
             This round writes no production code and pays no finding in code.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 and C3 are APPENDS — LEDGER18 to `.agent/live_review.md`, DECISION19 to
    `.agent/decisions.md`. Both targets end in exactly one newline at the round
    base and both existing final entries are separated from their predecessor by
    one blank line, which the reviewer measured; each append is therefore one
    newline followed by the slice. There is NO FROM/TO pair in this round, so no
    replacement obligation arises and none is ordered.
 3. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 is the
    first substantive commit because this round writes the finding ledger and
    the plan must be current before it (checklist item 23).
 4. This round mints NO new finding id and resolves none. R-0636 is paid by the
    round that dispatches, which is not this one. The next free id is R-0638
    when this round ends, exactly as it was when it began.
 5. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all three of its lines.
 6. This is the LAST round of the session. The handback's `## Next` names Phase 1
    rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read — as
    the next session's FIRST action and the AGENTS.md Open PR Gate as its SECOND.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C4: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C4. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r18.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received. Report
     sha256, byte count and line count for both. C0b is written FROM the
     committed C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its
     `<<<SLICE ` and `<<<END ` marker lines with a script, and apply them
     programmatically. Report each slice's sha256, bytes and lines, plus the
     aggregate count your script printed. State no slice count you did not
     count.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R18 — report `cmp` exit and
     both sha256, with a negative control against another file that exits
     non-zero — and `wc -l` reads it against the 50-line cap of AGENTS.md.
     Line-anchored, `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPENDS, under TWO independent readers each, with a negative control on the
     FIRST appended paragraph (finding R-0631). For C2 over
     `.agent/live_review.md` with the round base as base, and again for C3 over
     `.agent/decisions.md` with the C2 tree as base: (a) the base blob is a
     byte-exact PREFIX and the remainder equals a newline plus the slice —
     report each remainder's sha256, bytes and lines; (b) N is counted BY YOUR
     SCRIPT, not asserted, and the last N blank-line units of the file equal the
     slice's N paragraphs IN ORDER. Then flip one printable byte in the FIRST
     appended paragraph, at equal length, and report that BOTH readers REJECT
     the flip while both ACCEPT the true file — for BOTH appends. Report each
     file's before/after byte and line counts.
 G6  Line-anchored over `.agent/live_review.md` at the round base and at C2
     (finding R-0630 — state that the anchor is line-start): `^- R-\d+ — ` with
     every captured id DISTINCT at each; `^Done: R-\d+ — `; `^Landed: `;
     `^Gate: R\d+ — ` over that many DISTINCT keys; `^Gate: R18 — `; and
     `^- R-0638 — `, which must read 0 at both because this round mints no id.
     Report each pair of readings, the max id, and the open count by DECISION
     F009 D10's rule — line-anchored entries minus line-anchored `Done:` lines —
     at C2. Report what you measure, not what this sentence expects.
 G7  Line-anchored over `.agent/decisions.md` at the round base and at C3:
     `^## DECISION F009 D\d+ — ` with every captured number DISTINCT at each,
     `^## DECISION ` as the total, and `^## DECISION F009 D19 — ` which must
     read 0 at the base and 1 at C3. Report both pairs.
 G8  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree. Report each command's REAL exit code and the
     count IT printed — predict no number:
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional and the four-path group is owed because this
     round's change set holds `.agent/` state files (finding R-0607). The
     reviewer ran both at the round base before ordering them: each exits 0, so
     each can fail honestly.
 G9  RANGE: the range from the round base to C3 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, which are `.agent/authored/f009-r18.md`,
     `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md` and
     `.agent/decisions.md`; the set difference EMPTY in both directions, and 0
     paths beginning `packages/`, `apps/`, `tests/` or `docs/`, which is this
     round's no-production-code constraint as a measurement. Each commit has ONE
     parent; `git show --numstat` and `git diff --numstat` AGREE on every cell;
     every cell equals the `+/-` column of the handback's `## Commits` table
     (checklist item 28) — compare them cell by cell and say so. Report each
     pre-handback commit's insertions against the 500 cap of AGENTS.md DECISION
     F104 D1; the handback commit's own numbers belong in the round report, not
     here (checklist item 14). `^<<<SLICE ` and `^<<<END ` read 0 lines in EVERY
     file any slice lands in, and the reviewer counted that set at three
     members: `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md`.
     `git ls-files .remedy-wt` reads 0. Classify THIS ROUND's reflog rows by the
     operation before the first `:` and report `amend`, `rebase` and `cherry`
     each reading 0; assert no total over the whole reflog (finding R-0601).
     Create NO worktree: no gate this round needs one, so `git worktree list`
     prints 1 line throughout.
 G10 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status table with exactly one row
     for each of C0a, C0b, C1, C2, C3 and C4, the round base SHA, one line per
     gate with the transcripts in the round report rather than in the file
     (finding R-0582), and the `Fortschritt:` line of this block VERBATIM.
     Report its `wc -l` against the 100 lines a bundle of more than five commits
     allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C4.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R18
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R18 records the R17 verdict and rules DECISION F009 D19, which cuts the
`job.stop` dispatch into two rounds on a measurement of the pin migration. It
writes no production code. The `rejected_effect` token and DECISION F009 D18's
four rulings landed at R17; the door still answers 501.

## Next Steps
1. Round one of DECISION F009 D19: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order —
   effect, then the `accepted` audit line, then the nonce publication — pays
   R-0636, and moves every seam pin that must move for the suite to stay green.
   Three of those migrations are uniform byte-string transformations the
   reviewer counted at `6101ca20`: `[0] == 501` 9 times, all `job.stop` through
   `_post_command`; `assert status == 501` 7 times, of which the
   `decision.resolve` one keeps the seam; and `"not_implemented"` 5 times.
2. Round two of D19: the effect assertions in a NEW file — the stop request the
   dispatch published, the nonce record it wrote, and a retry audited
   `replayed`.
3. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- Three vocabulary tokens exist with no caller. The door's own guard still
  asserts it writes no `accepted`, unedited, which keeps the gap visible.
- `test_an_audit_writer_that_raises_changes_neither_status_nor_body` submits the
  SAME default nonce in both of its loops, so once the door publishes, its second
  seam call becomes a REPLAY. D19's first round handles that site by itself.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R18

<<<SLICE LEDGER18
Gate: R18 — the R17 entry. R17 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r17.md` at `10681377` and `.agent/last_block.md` at `e92970bf` are both sha256 a99166a9d66fbd0c67dea646c6dab389707e001559c4978c0eee6d57a14a3196 over 26275 bytes and 322 lines, and the reviewer compared them not against a recorded digest but against the emitted bytes THEMSELVES, which were still on disk — `cmp`-against-original, not the digest fallback of docs/agents/planner_reviewer_prompt.md §4.9. The reviewer's own ordered extraction out of the committed C0a blob gives 7 slices aggregating 14216 bytes over 127 lines, the same aggregate the handback printed, every digest reproducing. `.agent/plan.md` at `bacc2459` is BYTE-EQUAL to PLANF009R17 at 45 lines against the 50-line cap, its negative control unequal, `^## Goal$` and `^## Next Steps$` reading 1 each. THE TWO APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS EACH: at `d3a3bd27` the round-base blob is a byte-exact prefix of `.agent/live_review.md` and the remainder is exactly a newline plus LEDGER17, sha256 `585973ea…` over 4804 bytes and 2 lines, the file going 476187 to 480991 bytes and 1092 to 1094 lines, N counted at 1 by the reviewer's own extractor; at `6f140128` the C2 blob is a byte-exact prefix of `.agent/decisions.md` and the remainder is exactly a newline plus DECISION18, sha256 `a7fad9c3…` over 4494 bytes and 18 lines, the file going 450056 to 454550 bytes and 6827 to 6845 lines, N counted at 9. For BOTH appends, flipping byte 0 of the FIRST appended paragraph at equal length makes BOTH readers REJECT while both ACCEPT the true file, which is finding R-0631's control applied to each append separately rather than to one of them. THE TWO REPLACEMENTS ARE PROVED AS REPLACEMENTS: the mechanical containment test printed `TO contains FROM: false` for both pairs, so both really are rewrites; at C3 each FROM read 1 whole-line and 1 indent-agnostic in its own file and 0 in the other, and at `e1850a5b` each FROM reads 0 and 0 while each TO reads 1 and 1, the two readings agreeing at all eight counts; and each file's C3 blob with its single pair applied is BYTE-EQUAL to what C4 landed — `command_audit.py` at `8268358d…` over 6081 bytes and the pin file at `03b86977…` over 8930 bytes — so no other byte of either file moved. THE CODE IS EXACTLY THE AUTHORED SLICES AND NOTHING MORE, which is the reading that matters for a round touching `packages/`: the reviewer read the real diff of `e1850a5b` and it is the two authored pairs and no third change. THE SETS HELD line-anchored at the round base and at C2: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each, `^Done: R-\d+ — ` 3 at both, `^Landed: ` 0 at both, `^Gate: R\d+ — ` 16 and 17 over that many DISTINCT keys, `^Gate: R17 — ` 0 and 1, `^- R-0638 — ` 0 at both, max id R-0637 at both, and 200 open by DECISION F009 D10's rule at both — a round that minted no id and resolved none, exactly as its constraint 7 required. `^## DECISION F009 D\d+ — ` reads 17 and 18 with every number DISTINCT, and the `^## DECISION ` total 102 and 103. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the two changed paths EXITS 0, the audit and nonce pair EXITS 0 at 45 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 507 passed — the same four results the handback reported and not one of them predicted by it. THE RED CONTROL IS THE REVIEWER'S OWN, run in a disposable worktree at `e1850a5b` on content byte-identical to what landed: the ordered target line reads 1 whole-line and 1 indent-agnostic, both readings agreeing, and deleting it EXITS 1 failing exactly `tests/orchestration/test_command_audit.py::test_the_outcome_vocabulary_is_the_closed_set_d14_ruled`, with the restored tree byte-identical and EXITING 0 — so the pin this round ships genuinely reaches the token it pins rather than passing beside it. THE DOOR IS UNTOUCHED, which this round existed to guarantee: the range holds 0 paths equal to `packages/orchestration/ui_server.py` and 0 beginning `tests/ui_server/`, and that suite passes UNMODIFIED inside the 507, so the guard asserting that no record the door wrote carries `accepted` is still true and still unedited. THE RANGE HELD: seven single-parent commits, the range to C4 listing exactly the seven declared paths with the set difference empty in both directions; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 322/0, 253/134, 17/18, 2/0, 18/0, 7/1 and 3/1; pre-handback insertions 322, 253, 17, 2, 18 and 10, every one under the 500 cap; zero `^<<<SLICE ` and `^<<<END ` LINES in all five slice targets; `git ls-files .remedy-wt` 0; one worktree and a clean tree at the verdict, and the branch pushed to the same SHA the reviewer read. The handback carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a through C5, the round base SHA, and the block's `Fortschritt:` line verbatim across all three of its lines, at 99 lines against the 100 a bundle of more than five commits allows. NO DEVIATION WAS DECLARED AND NONE IS FOUND. NOTHING IS OWED and no id is minted.
<<<END LEDGER18

<<<SLICE DECISION19
## DECISION F009 D19 — the `job.stop` dispatch round splits in two, and the effect assertions get their own file (2026-08-22)

Measured by the reviewer at `6101ca20`, before this round was delegated, by counting the strings the migration must move in `tests/ui_server/test_command_channel.py`: `[0] == 501` occurs 9 times and every one of them submits `job.stop` through `_post_command`, so all 9 become 200; `assert status == 501` occurs 7 times, of which the `decision.resolve` case keeps the seam and the loop over both exposed ids must split; `"not_implemented"` occurs 5 times, of which one is the raising-writer test whose second seam call becomes a REPLAY rather than an acceptance, because both of its loops submit the SAME default nonce. Three of those are uniform byte-string transformations the block can order once each and count; the remainder need their own FROM/TO pairs, and the door's own dispatch, the effect assertions and the plan and ledger slices sit beside them. Summed as slices plus the prose a done-when list needs, that block exceeds the 490 lines DECISION F085 D6 caps a step block at.

CHOSEN: DECISION F009 D18's round two becomes two, so D16's six rounds become seven and nothing else in its ordering changes. ROUND ONE lands the door — `packages/orchestration/ui_server.py` dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order of effect, audit line, publication — pays R-0636 by moving the replay audit token to `replayed`, and migrates every seam pin that must move for the suite to stay green, including the three counted uniform transformations. That round is self-testing rather than half-wired: the audit test asserting the outcome `accepted` for a `job.stop` passes only if the door really dispatched, so D16's rule that no round leaves a mechanism no test can reach is met by the migration itself. ROUND TWO adds the dedicated effect assertions in a NEW file, `tests/ui_server/test_command_dispatch.py` — that the stop request the dispatch published exists and carries the door's source, that the nonce record holds the body the client received, and that a retry of the same nonce is audited `replayed` — which is purely additive and touches no existing test.

WHY THE CUT IS HERE AND NOT ELSEWHERE. A cut between the door and the pins was already rejected by D17 and is rejected again for the same reason: a test pinning a status the door does not yet return asserts a falsehood, and the suite would be red between the two rounds. A cut between the pins that MUST move and the assertions that MAY be added later has neither problem — the suite is green at every commit of both rounds, and the second round adds a file rather than editing one.

ALTERNATIVES: (a) keep D18's round two whole and exceed the block cap — rejected on the cap, which is a measurement and not a preference, and on D16's own rule that a block which does not fit is not delivered. (b) raise the 490-line cap instead of splitting — rejected here because the cap is DECISION F085 D6's and a cap change must be measured against every other artifact it crosses rather than lifted for the one round it inconveniences; the reviewer records instead that this feature has now split three times on that single constraint, which is a fact a later reader should weigh before the next feature is planned the same way.

REVERSE by collapsing these two rounds back into one, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5, the write order from D18, and the round ordering from D16, D17 and D18, and none of them is altered here.
<<<END DECISION19
