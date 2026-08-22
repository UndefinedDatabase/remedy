── STEP T003 (round one of DECISION F009 D18, which splits D17's round two) — F009 ──
Goal:        Land what the `job.stop` dispatch DEPENDS on, and rule the four
             questions that dispatch raises, without touching the door. The
             round records the R16 verdict, rules DECISION F009 D18, and adds
             `rejected_effect` to the audit vocabulary with its pin. The door
             keeps answering 501 and keeps auditing `not_implemented`, so
             `packages/orchestration/ui_server.py` and
             `tests/ui_server/test_command_channel.py` are provably untouched.

Fortschritt: ~72 % (T001 gebaut · T002 gebaut · T003 begonnen: Extraktion,
             Publikations-Bound und das vollständige Vokabular stehen, der
             Dispatch fehlt) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R16 verdict
             · C3 DECISION F009 D18 · C4 the `rejected_effect` token with its
             pin · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r17.md` (NEW, C0a)
             `.agent/last_block.md` (C0b)
             `.agent/plan.md` (C1)
             `.agent/live_review.md` (C2)
             `.agent/decisions.md` (C3)
             `packages/orchestration/command_audit.py` (C4)
             `tests/orchestration/test_command_audit.py` (C4)
             `.agent/handoff.md` (C5)
             NOTHING under `apps/`, `docs/` is touched, and within `packages/`
             and `tests/` only the two paths named above.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 and C3 are APPENDS — LEDGER17 to `.agent/live_review.md`, DECISION18 to
    `.agent/decisions.md`. Both targets end in exactly one newline at the round
    base and both existing final entries are separated from their predecessor by
    one blank line, which the reviewer measured; each append is therefore one
    newline followed by the slice.
 3. Both FROM/TO pairs were classified MECHANICALLY before emission by a script
    that printed, for each pair, whether the TO contains the FROM verbatim.
    AUDIT_FROM → AUDIT_TO printed `TO contains FROM: false`; PIN_FROM → PIN_TO
    printed `TO contains FROM: false`. Both are therefore REWRITES and carry the
    FROM-0x / TO-1x obligation, not an append obligation.
 4. Each FROM occurs EXACTLY ONCE in its own target file at the round base,
    counted by the reviewer whole-line AND indent-agnostic with both readings
    agreeing (checklist item 25). AUDIT_FROM's file is
    `packages/orchestration/command_audit.py`; PIN_FROM's file is
    `tests/orchestration/test_command_audit.py`. Neither string occurs in the
    other file.
 5. The token and its pin land in the SAME commit, C4. A vocabulary change whose
    pin lands separately leaves one commit on the branch at which the suite
    describes a set the source does not hold (the R-0151 class).
 6. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1 is
    the first substantive commit because this round writes the finding ledger and
    the plan must be current before it (checklist item 23).
 7. This round mints NO new finding id and resolves none: R-0636 is paid by the
    round that dispatches, which is not this one. The next free id is R-0638
    when this round ends, exactly as it was when it began.
 8. `rejected_effect` deliberately has NO writer when this round ends, which is
    the same shape DECISION F009 D17 ruled for `accepted` and `replayed` and for
    the same reason. The door's own guard in
    `tests/ui_server/test_command_channel.py` — that no record the door wrote
    carries `accepted` — stays TRUE and UNEDITED, which is what keeps the gap
    visible rather than papered over.
 9. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C5: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C5. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r17.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received. Report
     sha256, byte count and line count for both. C0b is written FROM the
     committed C0a blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its
     `<<<SLICE ` and `<<<END ` marker lines with a script, and apply them
     programmatically. Report each slice's sha256, bytes and lines, plus the
     aggregate count your script printed. State no slice count you did not
     count.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R17 — report `cmp` exit and
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
 G6  BOTH PAIRS ARE REPLACEMENTS, NOT APPENDS, so prove them as such. At C4:
     AUDIT_FROM reads 0 and AUDIT_TO reads 1 in
     `packages/orchestration/command_audit.py`, and PIN_FROM reads 0 and PIN_TO
     reads 1 in `tests/orchestration/test_command_audit.py`, with the whole-line
     and the indent-agnostic counts BOTH taken and AGREEING for all four
     readings. Then show that each file's C3 blob with its single pair applied
     is BYTE-EQUAL to what C4 landed, so no other byte of either file moved.
     Report `git show --numstat` for C4 over both paths.
 G7  Line-anchored over `.agent/live_review.md` at the round base and at C2
     (finding R-0630 — state that the anchor is line-start): `^- R-\d+ — ` with
     every captured id DISTINCT at each; `^Done: R-\d+ — `; `^Landed: `;
     `^Gate: R\d+ — ` over that many DISTINCT keys; `^Gate: R17 — `; and
     `^- R-0638 — `, which must read 0 at both because this round mints no id.
     Report each pair of readings, the max id, and the open count by DECISION
     F009 D10's rule — line-anchored entries minus line-anchored `Done:` lines —
     at C2. Report what you measure, not what this sentence expects.
 G8  Line-anchored over `.agent/decisions.md` at the round base and at C3:
     `^## DECISION F009 D\d+ — ` with every captured number DISTINCT at each,
     `^## DECISION ` as the total, and `^## DECISION F009 D18 — ` which must
     read 0 at the base and 1 at C3. Report both pairs.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree. Report each command's REAL exit code and the
     count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/command_audit.py
        tests/orchestration/test_command_audit.py`
       `python3 -m pytest tests/orchestration/test_command_audit.py
        tests/orchestration/test_command_nonce.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional; the four-path group is owed because this
     round's change set holds `.agent/` state files (finding R-0607); the
     ui_server half of it is the constraint-8 proof that the door's guard still
     passes UNEDITED. The reviewer ran all four at the round base before
     ordering them: each exits 0, so each can fail honestly.
 G10 RED CONTROL, inside a disposable `git worktree` under `.remedy-wt/` and
     NEVER in the primary checkout (guardrail G5). At content byte-identical to
     what C4 landed, delete the single line `    "rejected_effect",` from
     `packages/orchestration/command_audit.py` — the reviewer counted that exact
     byte string in that file at C4 as 1 whole-line and 1 indent-agnostic, both
     readings agreeing — and report which tests fail by NODE ID and that the
     exit code is non-zero. Restore the worktree and report the same command
     exiting 0 there. Order the colour, never the count: report the ids the run
     printed. Remove and prune the worktree; `git worktree list` prints 1 line
     at the end of the round.
 G11 RANGE: the range from the round base to C4 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, which are `.agent/authored/f009-r17.md`,
     `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/decisions.md`, `packages/orchestration/command_audit.py` and
     `tests/orchestration/test_command_audit.py`; the set difference EMPTY in
     both directions, and 0 paths equal to `packages/orchestration/ui_server.py`
     and 0 beginning `tests/ui_server/`, which is constraint 8 as a measurement.
     Each commit has ONE parent; `git show --numstat` and `git diff --numstat`
     AGREE on every cell; every cell equals the `+/-` column of the handback's
     `## Commits` table (checklist item 28) — compare them cell by cell and say
     so. Report each pre-handback commit's insertions against the 500 cap of
     AGENTS.md DECISION F104 D1; the handback commit's own numbers belong in the
     round report, not here (checklist item 14). `^<<<SLICE ` and `^<<<END ` read
     0 lines in EVERY file any slice lands in, and the reviewer counted that set
     at five members: `.agent/plan.md`, `.agent/live_review.md`,
     `.agent/decisions.md`, `packages/orchestration/command_audit.py` and
     `tests/orchestration/test_command_audit.py`. `git ls-files .remedy-wt`
     reads 0. Classify THIS ROUND's reflog rows by the operation before the
     first `:` and report `amend`, `rebase` and `cherry` each reading 0; assert
     no total over the whole reflog (finding R-0601).
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status table with exactly one row
     for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, one line
     per gate with the transcripts in the round report rather than in the file
     (finding R-0582), and the `Fortschritt:` line of this block VERBATIM.
     Report its `wc -l` against the 100 lines a bundle of more than five commits
     allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C5.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R17
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
R17 records the R16 verdict, rules DECISION F009 D18 — which splits D17's round
two and fixes the accepted response, the two write-failure rules and the
dispatch-failure token — and lands `rejected_effect` in the audit vocabulary
with its pin. The door is not touched and keeps answering 501.

## Next Steps
1. Round two of DECISION F009 D18: `packages/orchestration/ui_server.py`
   dispatches `job.stop` to `safe_points.request_stop` under D18's ruled order —
   effect, then the `accepted` audit line, then the nonce publication — and pays
   R-0636 by moving the replay token to `replayed`. The seam pins in
   `tests/ui_server/test_command_channel.py` migrate in that same round, and
   `test_every_exposed_command_reaches_the_seam` splits because after it one
   exposed id dispatches and the other still answers 501.
2. Then `decision.resolve` dispatches and the seam is gone; then the
   `command.accepted` SSE event; then the queue-only import guard, the
   per-command side-effect assertions and the route-walking 405 test; then the
   integration gate and closure.

## Risks
- Three vocabulary tokens now exist with no caller. The door's own guard still
  asserts it writes no `accepted`, which keeps the gap visible rather than
  papered over, and it is unedited by this round.
- The seam-pin migration is the largest single piece left: 21 lines of
  `tests/ui_server/test_command_channel.py` mention the literal 501, measured at
  `e7c621fc`, and most reach the door through a helper defaulting to `job.stop`.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R17

<<<SLICE LEDGER17
Gate: R17 — the R16 entry. R16 PASSED. R16 was a record round that wrote no production code, and the reviewer re-executed every gate off disk rather than reading any value back out of the handback; every value reproduced. TRANSPORT HELD: `.agent/authored/f009-r16.md` at `231435c1` and `.agent/last_block.md` at `baff3ed3` are both sha256 32f77b87327c8d4a1c5dbcb00fe49d397908f529ac24691f811cc784aa1137c6 over 21177 bytes and 203 lines, and byte-equal to each other. The reviewer's own ordered extraction out of the committed C0a blob gives 4 slices aggregating 11250 bytes over 49 lines, the same aggregate the handback printed, with each slice's digest reproducing: PLANF009R16 `1f13a5a5…`, LEDGER16 `238e9eb3…`, DONE0637_FROM `e349b294…` and DONE0637_TO `49de83ab…`. `.agent/plan.md` at `16b05554` is BYTE-EQUAL to PLANF009R16 at 46 lines against the 50-line cap, its negative control against `.agent/last_block.md` unequal, and `^## Goal$` and `^## Next Steps$` reading 1 each. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: at `6f83dad6` the round-base blob is a byte-exact prefix of `.agent/live_review.md` and the remainder is exactly a newline plus LEDGER16, sha256 `ba37138c…` over 6309 bytes and 2 lines, the file going 468268 to 474577 bytes and 1090 to 1092 lines; N is 1 counted by the reviewer's script and the last 1 blank-line unit equals the slice's 1 paragraph; and flipping byte 0 of the FIRST appended paragraph from `G` to `Z` at equal length makes BOTH readers REJECT while both ACCEPT the true file. THE REPLACEMENT IS PROVED AS ONE, which is what a non-append edit to an append-only record owes: at `80284ce1` DONE0637_FROM reads 0 whole-line and 0 indent-agnostic and DONE0637_TO reads 1 and 1, the two readings agreeing at every count, the mechanical containment test printing `TO contains FROM: false` so the pair really is a REWRITE, and the C2 blob with that single pair applied is BYTE-EQUAL to what C3 landed — both sha256 `7cc1729b…` over 476187 bytes — so no other byte of a 476-kilobyte record moved. `git show --numstat` for that commit reads `1 1`. THE SETS HELD line-anchored at the round base and at C3: `^- R-\d+ — ` 203 and 203 with every id DISTINCT at each, `^Done: R-\d+ — ` 2 and 3, `^Landed: ` 1 and 0, `^Gate: R\d+ — ` 15 and 16 over that many DISTINCT keys, `^Gate: R16 — ` 0 and 1, `^- R-0638 — ` 0 at both, max id R-0637 at both, and 201 then 200 open by DECISION F009 D10's rule. All three findings the round added evidence to — R-0585, R-0629 and R-0418 — read 1 at the round base line-anchored, so no id was minted for a defect the open set already held, which is checklist item 30 obeyed rather than asserted. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 507 passed, the same two results the handback reported and neither predicted by it. THE RANGE HELD: six single-parent commits, the range to C3 listing exactly the four declared paths with the set difference empty in both directions and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/` — the no-production-code constraint as a measurement rather than a promise; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own table, at 203/0, 137/363, 19/16, 2/0 and 1/1; pre-handback insertions 203, 137, 19, 2 and 1, every one under the 500 cap; zero `^<<<SLICE ` and `^<<<END ` LINES in both slice targets; `git ls-files .remedy-wt` 0; one worktree throughout and a clean tree at the verdict. The handback carries every mandated section of docs/agents/handback_template.md, an item-status row for each of C0a through C4, and the block's `Fortschritt:` line verbatim across all three of its lines, at 89 lines against the 100 a bundle of more than five commits allows. ONE READING NEEDED CARE AND SURVIVED IT: the handback reports 5 reflog rows for a six-commit round, which is correct rather than short — the gate ran while C4's own text was being written, so C4's row could not exist yet, and checklist item 14 is exactly the rule that a per-commit reading cannot reach the commit that states it. All 5 classify as `commit`, with `amend`, `rebase` and `cherry` at 0 and no total asserted over the whole reflog. THE ONE DECLARED NON-DEVIATION IS ACCURATE: LEDGER16's prose quotes the transport markers inline inside backticks, and the reviewer counted 1 occurrence of each token in that slice with 0 marker LINES, so the line-anchored zero-gate over both slice targets is satisfied by the property rather than by luck. NOTHING IS OWED and no id is minted: the round did what it existed to do, which was to put a session's judgements on disk before that session ended.
<<<END LEDGER17

<<<SLICE DECISION18
## DECISION F009 D18 — D17's round two splits again, and what an ACCEPTED command answers, audits and publishes (2026-08-22)

Measured by the reviewer at `e7c621fc`, before this round was delegated: DECISION F009 D17's round two does not fit. `tests/ui_server/test_command_channel.py` mentions the literal `501` on 21 lines and reaches the door through `_post_command`, whose body defaults to `job.stop`, so the dispatch moves most of those sites; `safe_points.request_stop` returns a `StopSignal` whose fields nothing has ever put on the wire; and D14 clause four ruled what a failed audit write does for a REJECTION while explicitly leaving the accepted case open. DECISION F085 D6 caps a step block at 490 lines TOTAL, and the FROM/TO pairs for those migrations plus a dispatch plus the tests for its effect do not fit inside one.

CHOSEN: D17's round two becomes two, so D16's five rounds become six and nothing else in its ordering changes. Round one — this one — touches no door: it rules the four questions below and lands the third vocabulary token they require. Round two edits `packages/orchestration/ui_server.py`, migrates the seam pins and pays R-0636. Rounds three onward are D16's second, third and fourth unchanged.

FIRST, WHAT AN ACCEPTED COMMAND ANSWERS. CHOSEN: status 200 with `{"command": <id>, "outcome": "accepted", ...}` plus the fields that command's own effect produces — for `job.stop`, `request_id` from the returned `StopSignal`. Each id in the exposed subset declares its own accepted body rather than sharing one envelope, because D5's three effects return three different things and a common shape would either drop what the caller needs or invent fields the effect never produced. The `outcome` field carries the same token the audit line carries, so a client and a later reader of `commands_audit.jsonl` describe the same event with the same word.

SECOND, THE ORDER OF THE THREE WRITES. CHOSEN: dispatch, then the `accepted` audit line, then the nonce publication. The effect runs first because the response body is not known until it returns; the audit line precedes the publication because the record of what the door did must not depend on a store the client controls the key of; and the publication is last because D8's contract is that a replay returns the ORIGINAL result, which does not exist until the other two have happened. ALTERNATIVE: audit `accepted` before dispatching — rejected, it writes a claim the effect may then falsify by raising.

THIRD, WHAT A FAILED WRITE DOES ON THE ACCEPTED PATH, which D14 clause four left open. CHOSEN: both later writes fail SOFT. A failed audit write changes nothing about the response, exactly as for a rejection, because the effect is already durable and refusing after the fact would report a stop that really was requested as not requested. A publication that returns None — which R-0637's bound now makes reachable — also changes nothing, and its stated cost is that a client retrying that nonce re-executes the command; that is tolerable only because every effect in D5's table is idempotent at its own layer, `request_stop` provably so, and the round that dispatches `decision.resolve` must re-examine this clause against that effect rather than inherit it.

FOURTH, A DISPATCH THAT RAISES. CHOSEN: a new closed-set token `rejected_effect`, audited with `create=True`, answered 500 through the existing safe-error path with no exception text on the wire. Without it a failed effect is either unaudited, which breaks D6's "every attempt is audited", or recorded as `accepted`, which is false; and T5_F035 and T9_F167 both read this file to count what the door did, so the distinction has to exist in the vocabulary rather than in a reader's inference. The token lands HERE, one round before its writer, for the reason D17 gave for `accepted` and `replayed`: it keeps the round that retires the seam to the door alone.

ALTERNATIVES for the split itself: (a) keep D17's round two whole and exceed the block cap — rejected on the cap, which is a measurement and not a preference. (b) migrate the seam pins in this round and dispatch in the next — rejected for the reason D17 already gave, that a test pinning a status the door does not yet return asserts a falsehood.

REVERSE by collapsing these two rounds back into one, which is possible only if DECISION F085 D6's cap changes; the effect mapping comes from D5, the round ordering from D16 and D17, and none of them is altered here.
<<<END DECISION18

<<<SLICE AUDIT_FROM
#: indistinguishable to the two features that care.
OUTCOMES = (
    "rejected_token",
    "rejected_csrf",
    "rejected_job",
    "rejected_shape",
    "rejected_command",
    "rejected_rate",
    "not_implemented",
    "accepted",
    "replayed",
)
<<<END AUDIT_FROM

<<<SLICE AUDIT_TO
#: indistinguishable to the two features that care. `rejected_effect` is DECISION F009
#: D18's third token with no writer, landed here for the same reason as the other two: it
#: names a dispatch that RAISED, so an effect which failed is never recorded as the
#: acceptance it is not, and D6's "every attempt is audited" survives an effect function
#: that refuses. Without it a failed effect would be unaudited or recorded as `accepted`,
#: and the two reading features cannot tell those apart from the outside.
OUTCOMES = (
    "rejected_token",
    "rejected_csrf",
    "rejected_job",
    "rejected_shape",
    "rejected_command",
    "rejected_rate",
    "not_implemented",
    "accepted",
    "replayed",
    "rejected_effect",
)
<<<END AUDIT_TO

<<<SLICE PIN_FROM
def test_the_outcome_vocabulary_is_the_closed_set_d14_ruled() -> None:
    """The closed set, in order. `accepted` and `replayed` are DECISION F009 D17's pair."""
    assert OUTCOMES == (
        "rejected_token",
        "rejected_csrf",
        "rejected_job",
        "rejected_shape",
        "rejected_command",
        "rejected_rate",
        "not_implemented",
        "accepted",
        "replayed",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert len(set(OUTCOMES)) == len(OUTCOMES)
<<<END PIN_FROM

<<<SLICE PIN_TO
def test_the_outcome_vocabulary_is_the_closed_set_d14_ruled() -> None:
    """The closed set, in order. The last three are the tokens no caller writes yet."""
    assert OUTCOMES == (
        "rejected_token",
        "rejected_csrf",
        "rejected_job",
        "rejected_shape",
        "rejected_command",
        "rejected_rate",
        "not_implemented",
        "accepted",
        "replayed",
        "rejected_effect",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert "rejected_effect" in OUTCOMES, "an effect that raised is not the acceptance it failed to be"
    assert len(set(OUTCOMES)) == len(OUTCOMES)
<<<END PIN_TO
