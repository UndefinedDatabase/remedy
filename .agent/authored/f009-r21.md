── STEP T003 (record round — the R20 verdict, closing the session) — F009 ──
Goal:        Put this session's third verdict and the finding it produced on
             disk before the session ends. The round records the R20 verdict and
             registers R-0640, which is the reviewer's own block-numeral defect
             measured twice in one round. It writes NO production code and NO
             test, which G7 measures rather than asserts: a verdict that lives
             only in a session's chat is lost when that session ends.

Fortschritt: ~82 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft; offen bleiben
             `decision.resolve`, das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R20 verdict
             and finding R-0640 · C3 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r21.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/handoff.md` (C3). NOTHING under `packages/`, `apps/`,
             `tests/` or `docs/` is touched, and `.agent/decisions.md` is NOT
             touched: this round rules nothing and amends nothing.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 is an APPEND — LEDGER21 to `.agent/live_review.md`. That target ends in
    exactly ONE newline at the round base, which the reviewer measured on the
    bytes, so the append is one newline followed by the slice. LEDGER21 carries
    TWO paragraphs separated by one blank line.
 3. Commit order is C0a, C0b, C1, C2, C3 and is not negotiable. C1 precedes the
    ledger because the plan must be current before it (checklist item 23).
 4. This round mints ONE id, R-0640, in LEDGER21, and resolves none. It writes
    no `Done:` line: R-0636 was paid at R19 and its resolution is certified in a
    later round's record, not here. The next free id is R-0641 when this round
    ends.
 5. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of the block's bytes this time, which is
    the first half of finding R-0640 not recurring in the round that registers
    it.
 6. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5 — which is finding R-0640's fix
    applied to the block that registers it: this block is 181 lines TOTAL
    against DECISION F085 D6's 490 cap, 136 of them PROSE against D5's 400.
    Re-measure both from the committed C0a blob; a disagreement is a finding.
 7. THIS IS THE LAST ROUND OF THE SESSION. The handback's `## Next` names Phase
    1 rule 1 of docs/agents/self_drive_protocol.md — the `.agent/STOP` re-read —
    as the next session's FIRST action and the AGENTS.md Open PR Gate as its
    SECOND, and then names the `decision.resolve` dispatch as the work.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C3: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1 and C2. Report the round base SHA you read
     at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r21.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 6's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R21 — report `cmp` exit and
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
     `Gate: R` key over that many DISTINCT keys; the `Gate: R21` key; a leading
     `- R-0640` entry; and a leading `- R-0641` entry, which must read 0 at both
     because this round mints one id and it is not that one. Report each pair of
     readings, the max id, and the open count by DECISION F009 D10's rule at C2.
     Report what you measure, not what this sentence expects.
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
     `wc -l` against the 60-line cap, or against 100 with a stated cause.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C3.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R21
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
R21 records the R20 verdict and registers R-0640. It writes no code and rules
nothing. DECISION F009 D19 is now COMPLETE: `job.stop` dispatches through
`safe_points.request_stop` under D18's ruled order, its effects are pinned from
the outside by `tests/ui_server/test_command_dispatch.py`, and R-0636 is paid.
`decision.resolve` is the only id still answering the 501 seam.

## Next Steps
1. `decision.resolve` dispatches to `answer_task_decision` followed by
   `save_job` per DECISION F009 D5, and the 501 seam is gone entirely. That
   round must re-examine DECISION F009 D18's clause three against a
   non-idempotent effect, as D18 explicitly requires of it, and migrate the two
   pins that still expect 501 — the absent-args test and the exposed-subset
   loop's `else` branch.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, the per-command side-effect assertions and
   the route-walking 405 test; then the integration gate and closure.

## Risks
- D18's clause three ruled soft failure for both post-effect writes on the
  strength of `request_stop` being idempotent. `answer_task_decision` followed
  by `save_job` is not obviously so; D18 names that re-examination as the next
  round's obligation rather than an inheritance.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R21

<<<SLICE LEDGER21
Gate: R21 — the R20 entry. R20 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r20.md` at `dbca3df0`, `.agent/last_block.md` at `54120f8a` and the bytes the reviewer EMITTED, still on disk, are all sha256 f10ccb1c506164779c7cd8ac164b59587753fe7bc3f7828568cb34a07de53718 over 25976 bytes and 329 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob gives 3 slices aggregating 16398 bytes over 186 lines. `.agent/plan.md` at `58c1227e` is BYTE-EQUAL to PLANF009R20 at 40 lines against the 50-line cap, its negative control unequal. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: at `33d6edd1` the round-base blob is a byte-exact prefix of `.agent/live_review.md`, the remainder is exactly a newline plus LEDGER20, sha256 `560fd38c…` over 8166 bytes and 4 lines, the file going 492988 to 501154 bytes and 1100 to 1104 lines, N counted at 2, and flipping byte 0 of the FIRST appended paragraph at equal length makes BOTH readers REJECT while both ACCEPT the true file. THE NEW FILE IS THE SLICE AND NOTHING ELSE: `tests/ui_server/test_command_dispatch.py` did not exist at the round base — `git cat-file -e` exits non-zero — and at `5788b393` is BYTE-EQUAL to slice DISPATCHTESTS at sha256 `f58fafdb…` over 5932 bytes and 143 lines, with a negative control at exit 1. THE RED CONTROL IS THE REVIEWER'S OWN AND IT COVERS EXACTLY THE COMMITTED BYTES: the four new tests were run in a disposable worktree on content the reviewer then confirmed byte-identical to what C3 landed; with the R19 door in place they EXIT 0 at 4 passed, and with `packages/orchestration/ui_server.py` alone reverted to its pre-R19 bytes — a REAL mutation, `git diff HEAD --numstat` reading 13/76 and the file byte-equal to the base door — they EXIT 1 with all four failing. Every one of the four therefore reaches the dispatch rather than passing beside it, including the `rejected_effect` path that R19 shipped with no test reaching it. THE SETS HELD line-anchored at line start, round base and C2: entries 204 and 205 with every id DISTINCT at each, leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 19 and 20 over that many DISTINCT keys, the `Gate: R20` key 0 and 1, a leading `- R-0639` entry 0 and 1, a leading `- R-0640` entry 0 at both, max id R-0638 and R-0639, and 201 then 202 open by DECISION F009 D10's rule. `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C4 at sha256 `518e00e0…` over 461478 bytes, which is this round's rules-nothing constraint as a measurement. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the new file EXITS 0, the new file EXITS 0 at 4 passed, `tests/ui_server/` EXITS 0 at 422 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 511 passed — the 418 and 507 of R19 each grown by exactly the four tests this round adds, and not one of the five predicted by the handback. THE RANGE HELD: six single-parent commits, the range to C3 listing exactly the five declared paths with the set difference EMPTY in both directions and 0 paths beginning `packages/`, `apps/` or `docs/`; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 329/0, 251/410, 16/20, 4/0 and 143/0; pre-handback insertions 329, 251, 16, 4 and 143, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all three slice targets; `git ls-files .remedy-wt` 0; this round's six reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `a2af1014`, the same SHA the reviewer read. The handback carries every mandated section of docs/agents/handback_template.md in order, an item-status row for each of C0a through C4, the round base SHA and one line per gate, at 91 lines against the 100 a bundle of more than five commits allows. TWO DEVIATIONS WERE DECLARED AND BOTH ARE CORRECT, and both are defects in the REVIEWER'S BLOCK rather than in the work: the block's PROSE numeral and its count of its own `Fortschritt:` line. The worker measured both, reported both, repaired neither, and named the assumption it proceeded under. They are registered together below as R-0640.

- R-0640 — Low — A BLOCK STATED TWO NUMERALS ABOUT ITSELF AND BOTH DISAGREED WITH THE BLOCK'S OWN BYTES, IN THE SAME ROUND, AND THE WORKER SPENT BOTH ITS DEVIATIONS PROVING IT. FIRST, THE PROSE COUNT. The R20 block's constraint 7, committed at `dbca3df0`, states "329 lines TOTAL … 134 of them PROSE". The TOTAL is right. The PROSE is not: DECISION F085 D5 defines a block's prose as "every line outside a BEGIN-/END- marker pair, THE MARKER LINES INCLUDED, since those are the reviewer's own", so prose is TOTAL minus the slices' CONTENT lines. Measured by the reviewer off the committed C0a blob: 329 total, 186 slice-content lines, prose 143 — not 134. The reviewer's assembler had counted only the header region, silently dropping the 6 marker lines and the 3 blank separators between slices. SECOND, THE `Fortschritt:` COUNT. Constraint 6 and gate G11 both order the handback to repeat that line "VERBATIM across all three of its lines", while the block's own `Fortschritt:` occupies FOUR physical lines — the numeral was carried forward unexamined from R18 and R19, where three was correct. The worker reproduced all four verbatim and declared the assumption that the binding obligation is the text and not the count naming it, which is the right reading. WHY LOW: neither numeral controls anything. Under BOTH readings the block is far under D5's 400-line prose cap, so no cap decision turned on the wrong number, and the `Fortschritt:` text was relayed correctly because the worker read the text rather than the count. Nothing false reached a source file. THE CLASS IS COUNTING YOUR OWN ENUMERATION — R-0402, R-0404 and R-0436 are the same defect about a list, and F082 R20's "counted by listing them" is the same defect about the counting itself. What makes this instance worth an id is that the repository ALREADY carries the exact rule that would have caught the first half: prose equals total minus slices, markers counting as prose, iterated to a fixed point. The rule was recorded and then not applied, which is a different failure from not having the rule. FIX, BINDING ON EVERY LATER BLOCK OF THIS FEATURE: the assembler that emits a block computes PROSE as TOTAL minus the summed slice-CONTENT lines and never as the length of the header region, and every numeral a block states about its own text — the prose count, the total, the line count of any line it names — is READ BACK OUT OF THE ASSEMBLED BYTES before emission rather than typed beside them.
<<<END LEDGER21
