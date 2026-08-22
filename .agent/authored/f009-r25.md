── STEP T003 (record round — the R24 verdict, closing the session) — F009 ──
Goal:        Put this session's fourth verdict on disk before the session ends.
             The round records the R24 verdict and mints no id: R24 was clean.
             It writes NO production code and NO test, which G8 measures rather
             than asserts. A verdict that lives only in a session's chat is lost
             when that session ends, which is the whole reason this round shape
             exists — R21 was the same round for R20.

Fortschritt: ~90 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen und sind beidseitig wirkungsgeprüft; offen
             bleiben das SSE-Event, der Import-Guard und die 405-Routenprobe) —
             Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R24 verdict ·
             C3 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r25.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3). NOTHING under `packages/`, `apps/`,
             `tests/` or `docs/` is touched, and `.agent/decisions.md` is NOT
             touched: this round rules nothing and amends nothing.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 is an APPEND — LEDGER25 to `.agent/live_review.md`. That target ends in
    exactly ONE newline at the round base, which the reviewer measured on the
    bytes, so the append is one newline followed by the slice. LEDGER25 carries
    ONE paragraph.
 3. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger because the plan must be current before it (checklist item 23).
 4. This round mints NO id and resolves none. It writes no `Done:` line. The
    next free id is R-0642 when this round ends, exactly as when it started.
 5. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 6. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5, which is finding R-0640's fix: this
    block is 176 lines TOTAL against DECISION F085 D6's 490 cap, 138 of them
    PROSE against D5's 400. Re-measure both from the committed C0a blob; a
    disagreement is a finding.
 7. THIS IS THE LAST ROUND OF THE SESSION. The handback's `## Next` names Phase
    1 rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read —
    as the next session's FIRST action and the AGENTS.md Open PR Gate as its
    SECOND, and then names the `command.accepted` SSE event as the work.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C3: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1 and C2. Report the round base SHA you read
     at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r25.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 6's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R25 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPEND, under TWO independent readers, with a negative control on the FIRST
     appended paragraph (finding R-0631). For C2 over `.agent/live_review.md`
     based on the round base: (a) the base blob is a byte-exact PREFIX and the
     remainder equals a newline plus the slice — report its sha256, bytes and
     lines; (b) N is counted BY YOUR SCRIPT and the last N blank-line units
     equal the slice's N paragraphs IN ORDER. Then flip one printable byte in
     the FIRST appended paragraph, at equal length, and report that BOTH readers
     REJECT the flip while both ACCEPT the true file. Report before/after bytes
     and lines.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; the `Gate: R25` key; and a
     leading `- R-0642` entry, which must read 0 at BOTH because this round
     mints no id at all. Report each pair of readings, the max REGISTERED id,
     and the open count by DECISION F009 D10's rule at C2. Read every one of
     these at line START and not as a bare substring: this file legitimately
     QUOTES ids and gate keys inside its own verdict prose, so an unanchored
     scan reports a maximum that was never registered (finding R-0630, and the
     reading R24's own handback flagged).
 G7  `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C3 — the
     same sha256 — because this round rules nothing. Report both digests.
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
     each can fail honestly (R-0364).
 G9  RANGE: the range from the round base to C2 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/`, `tests/` or
     `docs/`, which is this round's no-code constraint as a measurement. Each
     commit has ONE parent; `git show --numstat` and `git diff --numstat` AGREE
     on every cell — invoke `git show` WITHOUT a `--` before the SHA, which
     turns it into a pathspec and prints nothing; every cell equals the `+/-`
     column of the handback's `## Commits` table (checklist item 28), compared
     cell by cell. Report each pre-handback commit's insertions against the 500
     cap of AGENTS.md DECISION F104 D1; the handback commit's own numbers belong
     in the round report (item 14). Leading `<<<SLICE ` and `<<<END ` read 0
     LINES in every file a slice lands in, a set the reviewer counted at two:
     `.agent/plan.md` and `.agent/live_review.md`. `git ls-files .remedy-wt`
     reads 0. Classify THIS ROUND's reflog rows by the operation before the
     first `:` and report `amend`, `rebase` and `cherry` each 0; assert no total
     over the whole reflog (R-0601). Create NO worktree, so `git worktree list`
     prints 1 line throughout.
 G10 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2 and C3, the round base SHA, one line per gate with the transcripts
     in the round report and not in the file (R-0582), and this block's
     `Fortschritt:` line VERBATIM across all four of its lines. Report its
     `wc -l` against the 60-line cap, or against 100 with a stated cause. EVERY
     numeral this file states about the round's own measurements is COUNTED
     mechanically before it is written, or no numeral is stated and the
     enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C3.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R25
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
R25 records the R24 verdict. It writes no code and rules nothing. The dispatch
half of T003 is COMPLETE: both UI-exposed ids reach a real effect, the 501 is a
guard rather than a placeholder, and every path — 200, 409, 500 and 501 — is
reached by a test that fails against the pre-dispatch door.

## Next Steps
1. The `command.accepted` SSE event on the F008 stream.
2. The queue-only import guard, whose allowed set includes `save_job` because
   DECISION F009 D5's own effect mapping names it.
3. Then the route-walking 405 test proving every other mutating method answers
   405; then the integration gate and closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  DECISION F009 D22 rules that this door must NOT pass its own source into it,
  the opposite of D20's rule for `request_stop`; a later round that generalises
  one to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R25

<<<SLICE LEDGER25
Gate: R25 — the R24 entry. R24 PASSED, and it PASSED CLEAN: no finding, no deviation, and every numeral it stated about its own bytes reproduced. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r24.md` at `7a349543`, `.agent/last_block.md` at `ac255fd0` and the bytes the reviewer EMITTED, still on disk, are all sha256 fe07f2c38e0717c1d7ae5068a8e370bdc0aa46d6dcd555f2507ec1eda418ff51 over 21814 bytes and 283 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 4 slices over 118 CONTENT lines, and constraint 7's numerals re-measure as 283 TOTAL and 165 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `cf407fc0` is BYTE-EQUAL to PLANF009R24 at 37 lines against the 50-line cap. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: at `2be1e945` the round-base blob is a byte-exact prefix of `.agent/live_review.md`, the remainder is exactly a newline plus LEDGER24, the file going 520130 to 524945 bytes and 1114 to 1116 lines, N counted at 1 BY THE SCRIPT, the base ending in exactly ONE newline measured on the bytes; an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE ONE PAIR IS PROVED AS THE APPEND-SHAPED PAIR IT WAS CLASSIFIED AS, which is finding R-0639's rule holding for the first pair of that shape since it was ruled: whole-line and indent-agnostic agreeing at every count, TESTS_FROM reads 1 before and 1 AFTER while TESTS_TO reads 0 then 1, and the containment reading TO-contains-FROM printed TRUE under both readers — so the after-state is the authored append rather than a failed application, and no unconverted site was reported because that reading does not apply to this shape. THE CODE IS EXACTLY THE AUTHORED SLICE AND NOTHING MORE: the reviewer read the real diff of `689e57b0` and it is 76 insertions and ZERO deletions over `tests/ui_server/test_command_channel.py`, adding exactly the two authored test definitions and no third change, and the committed file is BYTE-IDENTICAL to the reviewer's own dry-run copy made before the round was delegated. THE RED CONTROL IS THE REVIEWER'S OWN, run in a disposable worktree before delegation and again by the worker: with `packages/orchestration/ui_server.py` alone reverted to its PRE-R23 bytes — a REAL mutation, `git diff HEAD --numstat` reading 9/93 and the file byte-equal to the `9a47166c` blob — `test_command_channel.py` EXITS 1 with FOUR failures, the two pins R23 migrated and the two tests R24 adds, so both new tests genuinely reach what R23 shipped rather than passing beside it. That the guard test discriminates at all is the reviewer's own repair: measured before delegation, a status-only pin PASSED against both doors because the deleted seam also answered 501, so the authored test asserts the MESSAGE and the absence of the `command` key instead. THE SETS HELD line-anchored at line start, round base and C2: entries 207 at BOTH with every id DISTINCT at each — this round minted none — leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 23 and 24 over that many DISTINCT keys, the `Gate: R24` key 0 and 1, a leading `- R-0642` entry 0 at both, max REGISTERED id R-0641 at both, and 204 open at both by DECISION F009 D10's rule. `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C4 at sha256 `25f2d750…` over 473798 bytes, which is that round's rules-nothing constraint as a measurement. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the changed path EXITS 0, `test_command_channel.py` EXITS 0 at 86 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 513 passed — the 84 and 511 of R23 each grown by exactly the two tests this round adds, and not one of the four predicted by the handback. THE RANGE HELD: the range to C3 lists exactly the declared paths other than the handback with the set difference EMPTY in both directions and 0 paths beginning `packages/`, `apps/` or `docs/`, which is that round's no-production-code constraint as a measurement; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 283/0, 192/373, 12/16, 2/0 and 76/0; pre-handback insertions 283, 192, 12, 2 and 76, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in both slice targets; `git ls-files .remedy-wt` 0; the reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `c20cd5cb`, the same SHA the reviewer read. THE HANDBACK DECLARED A READING RATHER THAN HIDING IT, which is why this entry records no finding against it: its G6 line notes that an UNANCHORED `R-\d+` scan returns R-0642 because LEDGER24's prose quotes that id while reporting its own zero-reading, and states the max REGISTERED id as R-0641. The reviewer's own line-anchored measurement returns R-0641 and a leading `- R-0642` count of 0 at both readings, so the distinction the handback drew is the correct one and is finding R-0630's rule applied rather than rediscovered.
<<<END LEDGER25
