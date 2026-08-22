── STEP T003 (dispatch `decision.resolve`, retire the 501 seam) — F009 ──
Goal:        Make `decision.resolve` a real dispatch and delete the placeholder.
             The door answers a well-formed submission by answering the named
             decision through `escalation.answer_task_decision` and PERSISTING
             it through `storage.save_job` — both inside the effect, per
             DECISION F009 D21 — audits `accepted`, publishes the nonce result
             and answers 200. An effect that RAN and DECLINED answers 409 and
             audits `rejected_state`, the token R22 landed. The 501 stops being
             a placeholder and becomes a GUARD for an id exposed with no
             dispatch branch, which DECISION F009 D22 rules here along with the
             `answer_source` trap that would otherwise corrupt a counted field.

Fortschritt: ~88 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             ausgesetzten Kommandos dispatchen jetzt wirklich, die 501-Naht ist
             weg; offen bleiben das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R22 verdict
             and finding R-0641 · C3 DECISION F009 D22 · C4 the door and the two
             migrated pins · C5 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r23.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `packages/orchestration/ui_server.py`
             and `tests/ui_server/test_command_channel.py` (C4) ·
             `.agent/handoff.md` (C5). NOTHING under `apps/` or `docs/` is
             touched, and `packages/orchestration/command_audit.py` is NOT
             touched: R22 landed its token and this round only writes it.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. TWO APPENDS. C2 appends LEDGER23 to `.agent/live_review.md`; C3 appends
    DECISION22 to `.agent/decisions.md`. The reviewer measured BOTH targets on
    the bytes at the round base: each ends in exactly ONE newline, so each
    append is one newline followed by the slice. LEDGER23 carries TWO
    paragraphs and DECISION22 carries ELEVEN, separated by single blank lines.
 3. FIVE FROM/TO PAIRS, and they are the whole of C4: CONST, SEAM and METHOD
    over `packages/orchestration/ui_server.py`, then PINABSENT and PINLOOP over
    `tests/ui_server/test_command_channel.py`. The reviewer CLASSIFIED every one
    of them before writing the gate that measures them, which is finding
    R-0639's binding fix: for all five the TO does NOT contain the FROM as a
    contiguous line block, so none is append-shaped and the after-clause for all
    five is "the FROM reads 0 and the TO reads 1" — measure it, do not assume
    it.
 4. C4 IS ONE COMMIT and may not be split. The door's new answers and the pins
    that assert them must land together or the suite is RED between commits,
    which is the cut DECISION F009 D19 already rejected once for this feature.
 5. Commit order is C0a, C0b, C1, C2, C3, C4, C5 and is not negotiable. C1
    precedes the ledger because the plan must be current before it (checklist
    item 23), and C3 precedes C4 because a ruling lands before the code it
    governs.
 6. This round mints ONE id, R-0641, in LEDGER23, and resolves none. It writes
    no `Done:` line. The next free id is R-0642 when this round ends.
 7. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 8. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5, which is finding R-0640's fix: this
    block is 464 lines TOTAL against DECISION F085 D6's 490 cap, 220 of them
    PROSE against D5's 400. Re-measure both from the committed C0a blob; a
    disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C5: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3 and C4. Report the round base SHA
     you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r23.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 8's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R23 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  THE TWO APPENDS, each under TWO independent readers, each with a negative
     control on its FIRST appended paragraph (finding R-0631). For C2 over
     `.agent/live_review.md` and for C3 over `.agent/decisions.md`, each based
     on that file's round-base blob: (a) the base blob is a byte-exact PREFIX
     and the remainder equals a newline plus the slice — report its sha256,
     bytes and lines; (b) N is counted BY YOUR SCRIPT and the last N blank-line
     units equal the slice's N paragraphs IN ORDER. Then, for EACH append, flip
     one printable byte in the FIRST appended paragraph, at equal length, and
     report that BOTH readers REJECT the flip while both ACCEPT the true file.
     Report before/after bytes and lines for both files.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; the `Gate: R23` key; a leading
     `- R-0641` entry; and a leading `- R-0642` entry, which must read 0 at BOTH
     because this round mints one id and it is not that one. Report each pair of
     readings, the max id, and the open count by DECISION F009 D10's rule at C2.
     Report what you measure, not what this sentence expects.
 G7  Line-anchored over `.agent/decisions.md` at the round base and at C3: the
     `## DECISION ` total; leading `## DECISION F009 D` numbers with every
     captured number DISTINCT at each and the max reported; and the
     `## DECISION F009 D22 ` key, which reads 0 at the base and 1 at C3. Report
     both readings of each.
 G8  THE FIVE PAIRS, proved as pairs. For each of CONST, SEAM, METHOD, PINABSENT
     and PINLOOP, count its FROM block and its TO block in the file it targets,
     BOTH whole-line and indent-agnostic, and require the two readings to AGREE
     at every count. Before C4 every FROM reads 1 and every TO reads 0; after C4
     every FROM reads 0 and every TO reads 1 — constraint 3 classified all five
     as NOT append-shaped, so also report, for each pair, whether the TO
     contains the FROM as a contiguous line block, a value your SCRIPT prints
     and which must be FALSE five times. Report the counts, not the conclusion.
 G9  THE SEAM IS GONE AS A PLACEHOLDER, measured line-anchored over
     `packages/orchestration/ui_server.py` at the round base and at C4: the
     quoted `"command channel not yet accepting commands"` reads 1 then 0, and
     `_dispatch_decision_resolve` reads 0 then 2 — one definition and one call
     site. The quoted `not_implemented` reads 1 at BOTH, because DECISION F009
     D22 keeps that writer as the GUARD rather than deleting it; report both
     readings rather than assuming either.
 G10 RUFF AND SUITES, run SERIALLY in the PRIMARY checkout, never two pytest
     processes at once and never in a worktree. Report each command's REAL exit
     code and the count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/ui_server.py
        tests/ui_server/test_command_channel.py`
       `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
       `python3 -m pytest tests/ui_server/test_command_dispatch.py -q -rf`
       `python3 -m pytest tests/orchestration/test_command_audit.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The reviewer ran all six at the round base before ordering them: each exits
     0, so each can fail honestly (R-0364). Ruff over these two paths is exit 0
     at base, so exit 0 is orderable rather than a multiset comparison.
 G11 RED CONTROL, in a DISPOSABLE worktree only (guardrail G5), never in the
     primary checkout. At C4, revert `packages/orchestration/ui_server.py` ALONE
     to its round-base bytes — prove the mutation is REAL by reporting
     `git diff HEAD --numstat` for that path and that the file is byte-equal to
     the base blob — and run
     `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`.
     Report the REAL exit code and which tests failed. The TWO pins this round
     migrates must be among them: a pin that passes with the old door never
     reached the dispatch. Remove the worktree
     afterwards and report `git worktree list` back at 1 line.
 G12 RANGE: the range from the round base to C4 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `apps/` or `docs/` and 0 equal to
     `packages/orchestration/command_audit.py`. Each commit has ONE parent;
     `git show --numstat` and `git diff --numstat` AGREE on every cell — invoke
     `git show` WITHOUT a `--` before the SHA, which turns it into a pathspec
     and prints nothing; every cell equals the `+/-` column of the handback's
     `## Commits` table (checklist item 28), compared cell by cell. Report each
     pre-handback commit's insertions against the 500 cap of AGENTS.md DECISION
     F104 D1; the handback commit's own numbers belong in the round report
     (item 14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in every file a
     slice lands in, a set the reviewer counted at five: `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`,
     `packages/orchestration/ui_server.py` and
     `tests/ui_server/test_command_channel.py`. `git ls-files .remedy-wt` reads
     0. Classify THIS ROUND's reflog rows by the operation before the first `:`
     and report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601).
 G13 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4 and C5, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all four of its lines. Report
     its `wc -l` against the 60-line cap, or against 100 with a stated cause.
     EVERY numeral this file states about the round's own measurements — a path
     count, a commit count, a row count — is COUNTED mechanically before it is
     written, or no numeral is stated and the enumeration speaks (R-0404, and
     R-0641 which this round registers).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C5.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R23
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
R23 dispatches `decision.resolve` and retires the 501 placeholder. Both exposed
ids now reach a real effect: the answer is written and PERSISTED per DECISION
F009 D21, a declined answer is 409 and `rejected_state`, and DECISION F009 D22
rules the `answer_source` trap and turns the 501 into a guard.

## Next Steps
1. R24 adds the tests DECISION F009 D22's fifth clause defers, purely
   additively: the 200 acceptance path, the 501 guard, and the disk-level
   `decision.resolve` effect assertions in `test_command_dispatch.py` — the
   reads that file already does for `job.stop`. Until it lands, `save_job`
   running and the accepted body's `decision_id` are asserted by nothing.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, whose allowed set includes `save_job`
   because DECISION F009 D5's own effect mapping names it; then the
   route-walking 405 test; then the integration gate and closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  D22 rules that this door must NOT pass its own source into it, which is the
  opposite of D20's rule for `request_stop`; a later round that generalises one
  to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R23

<<<SLICE LEDGER23
Gate: R23 — the R22 entry. R22 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r22.md` at `9d23eb4a`, `.agent/last_block.md` at `76c1a3fb` and the bytes the reviewer EMITTED, still on disk, are all sha256 11f2023104c32675429f9dc91afcd268bd9657f4539b6d1f860af16232f4b2c4 over 25633 bytes and 282 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob gives 11 slices aggregating 89 CONTENT lines, and constraint 7's numerals re-measure as 282 TOTAL and 193 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `bd5c3d9c` is BYTE-EQUAL to PLANF009R22 at `faa5b439…`, 40 lines against the 50-line cap, `^## Goal$` and `^## Next Steps$` reading 1 each, its negative control unequal. BOTH APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS EACH: at `a68d1693` the base blob is a byte-exact prefix of `.agent/live_review.md` and the remainder is exactly a newline plus LEDGER22, sha256 `69dda8a4…` over 4400 bytes and 2 lines, the file going 508226 to 512626 bytes and 1108 to 1110 lines, N counted at 1; at `9d154d00` the base blob is a byte-exact prefix of `.agent/decisions.md` and the remainder is exactly a newline plus DECISION21, sha256 `19ccc8d5…` over 5772 bytes and 20 lines, the file going 461478 to 467250 bytes and 6867 to 6887 lines, N counted at 10. Both bases ended in exactly ONE newline, measured on the bytes, and for BOTH appends an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start, round base and C2: entries 206 at BOTH with every id DISTINCT at each — this round minted none — leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 21 and 22 over that many DISTINCT keys, the `Gate: R22` key 0 and 1, a leading `- R-0641` entry 0 at both, max id R-0640 at both, and 203 open at both by DECISION F009 D10's rule. Over `.agent/decisions.md` the `## DECISION ` total went 105 to 106, the leading `## DECISION F009 D` numbers 20 to 21 with every number DISTINCT and the max 20 to 21, and the `## DECISION F009 D21 ` key 0 to 1. THE FOUR PAIRS ARE PROVED AS PAIRS, whole-line and indent-agnostic with the two readings agreeing at every count: before C4 every FROM reads 1 and every TO 0, after C4 every FROM reads 0 and every TO 1, and TO-contains-FROM printed FALSE four times, so constraint 3's not-append-shaped classification is a MEASUREMENT rather than a claim — which is R-0639's fix holding one round after it was ruled. THE CODE IS EXACTLY THE AUTHORED SLICES AND NOTHING MORE: the reviewer read the real diff of `3fc8e98d` and it is the four pairs and no fifth change — six comment lines and one tuple member in `packages/orchestration/command_audit.py`, one docstring word and two assertion lines in `tests/orchestration/test_command_audit.py`. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the two changed paths EXITS 0, `tests/orchestration/test_command_audit.py` EXITS 0 at 17 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 511 passed — not one of the four predicted by the handback. THE RED CONTROL IS THE REVIEWER'S OWN, run in a disposable worktree BEFORE the round was delegated: with the module's tuple changed and the pin left alone, `tests/orchestration/test_command_audit.py` EXITS 1 with the vocabulary test failing on "Left contains one more item: 'rejected_state'", so the pin genuinely reaches the token rather than passing beside it. THE RANGE HELD: seven single-parent commits, the range to C4 listing exactly the seven declared paths other than the handback with the set difference EMPTY in both directions, 0 paths beginning `apps/` or `docs/` and 0 equal to `packages/orchestration/ui_server.py`; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 282/0, 212/111, 13/15, 2/0, 20/0, 7/0 and 3/1; pre-handback insertions 282, 212, 13, 2, 20 and 10, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all five slice targets; `git ls-files .remedy-wt` 0; this round's reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `9a47166c`, the same SHA the reviewer read. ONE DEFECT SURVIVED INTO THE PERMANENT RECORD AND IT IS THE HANDBACK'S OWN ARITHMETIC, registered below as R-0641.

- R-0641 — Low — A HANDBACK RESTATED A CORRECT GATE AND INVENTED A COUNT THE GATE NEVER ORDERED, AND THE COUNT IS WRONG. The R22 handback's G10 line, committed at `9a47166c`, reads "the range base→C4 lists exactly the six declared paths other than `.agent/handoff.md`". MEASURED by the reviewer at that commit: `git diff --name-only 09d473d6..3fc8e98d` returns SEVEN paths — `.agent/authored/f009-r22.md`, `.agent/decisions.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/command_audit.py` and `tests/orchestration/test_command_audit.py` — and the block's Change section declares eight paths, seven of them other than the handback. No reading of that sentence yields six. The same line also says "this round's six reflog rows" where the round has SEVEN commits and the worker's own transcript printed `{'commit': 7}`; that clause is recoverable under a range-scoped reading, since base→C4 really is six commits, so it is recorded as the weaker half rather than as a second instance. WHAT MAKES THIS WORTH AN ID IS WHERE THE NUMERAL CAME FROM. The reviewer's G10 ordered "EXACTLY the declared paths … the set difference EMPTY in both directions" and named NO count; the worker performed exactly that measurement, got the right answer — set difference empty both ways, which the reviewer reproduced — and then introduced a cardinality of its own when restating the gate in prose. The defect is therefore not in the gate, not in the work, and not in the measurement, but in the RESTATEMENT, which is the one step no gate covers because the gate has already passed by the time it is written. WHY LOW: nothing false reached a source file, no decision turned on the numeral, and the underlying set equality is correct and independently reproduced. THE CLASS IS R-0404's EXACTLY — "any sentence in a handback or block that pairs a numeral with an enumeration either counts that enumeration mechanically first, or states no numeral at all", a counter-measure this repository has carried as an OPEN finding since F082 — and it is the second instance in two consecutive rounds, R-0640 having been the same class in a block rather than a handback. R-0640's fix was written to bind the assembler that emits a BLOCK; this instance shows that scoping was too narrow, because the handback is authored by the worker after every gate has run. FIX, BINDING ON EVERY LATER ROUND OF THIS FEATURE: a handback's gate line RESTATES the measurement the gate ordered and introduces no numeral the gate did not order; where a count genuinely helps a reader, it is produced by the same script that produced the gate's own output and is pasted from it, never typed beside it.
<<<END LEDGER23

<<<SLICE DECISION22
## DECISION F009 D22 — `answer_source` is not this door's to name, and the 501 becomes a guard (2026-08-22)

Measured by the reviewer at `9a47166c`, before this round was delegated, by reading `packages/orchestration/escalation.py` end to end rather than only the function DECISION F009 D5 names: `answer_task_decision(job, decision_id, *, answer, source=ANSWER_SOURCE_HUMAN, now)` writes its `source` argument into the record's `answer_source` field, and `escalation.py` lines 362-366 then COUNT that field into exactly two buckets — `ANSWER_SOURCE_HUMAN` is `"human"` and `ANSWER_SOURCE_DEFAULT` is `"default"` — emitting "Sources: N human, M default, K unresolved" into the escalation assumption log.

FIRST, AND THIS IS THE TRAP. CHOSEN: `_dispatch_decision_resolve` does NOT pass `source`. It takes the function's default, `human`. A person answering a question through the UI IS a human answering it, and the door is the TRANSPORT rather than the decider. Had this round inherited DECISION F009 D20's rule for `request_stop` and passed `COMMAND_EFFECT_SOURCE`, the record would carry `answer_source="ui"`, which is in NEITHER bucket: the assumption log's table would print "ui" in its Source column while the summary line beneath it counted the answer as neither human nor default, silently under-reporting every decision ever answered through this door.

WHY THIS IS NOT D20 GENERALISED, stated because the two fields share a name and a later round will be tempted. `request_stop`'s `source` names WHICH TRANSPORT asked — that is exactly the distinction D20 protected, a UI stop against a `remedy job stop` — and it is free-form inside the archived signal. `answer_source` names WHO DECIDED, over a closed two-value vocabulary that is counted. Attributing the transport into a field that means the decider is a category error, and the fact that both arguments are spelled `source` is the entire reason it is easy to make.

WHERE THE DOOR'S OWN ATTRIBUTION LIVES, since it is not lost: `commands_audit.jsonl`, per DECISION F009 D6, records `token_fp`, `command`, `args_hash`, `nonce` and `outcome` for every attempt at this door. A reader asking "was this decision answered through the UI?" answers it there, which is where D6 deliberately put it, rather than by widening a counted field in the job record.

SECOND, WHAT THE 501 BECOMES. DECISION F009 D21 said the seam goes; MEASURED while writing the dispatch, deleting it outright leaves the handler with no branch for an id that `_command_is_ui_exposed` admitted and no dispatch clause matches, so such a request would fall off the end of the method with NO response written at all. CHOSEN: the 501 stays as a GUARD rather than a placeholder, with a new constant `COMMAND_NOT_DISPATCHED_MESSAGE`, still audited `not_implemented`. It is unreachable while `UI_EXPOSED_COMMANDS` holds exactly the two ids this door dispatches, and a test reaches it by monkeypatching that frozenset to hold a third — which is precisely the mistake the guard exists to catch. This also supersedes D21's fifth clause by giving `not_implemented` a live writer rather than only a historical one; the clause's reasoning, that on-disk records must stay validatable, is unaffected and still holds.

THIRD, WHAT THE 409 PUTS ON THE WIRE. CHOSEN: `_safe_error(409, COMMAND_DECISION_STATE_MESSAGE)` with the message "decision is not open", carrying `error` and nothing else. Every other refusal this door issues — 400, 403, 429, 500 — goes out through `_safe_error` with exactly that shape; the deleted 501 seam was the only exception, and it is being deleted. A client knows which command it submitted, and its correlation key is the nonce it chose. CONSEQUENCE, stated because it is the whole of the pin migration: both surviving 501 pins asserted `body["command"]`, and neither can after this round.

FOURTH, WHAT THE EFFECT READS OUT OF `args`. CHOSEN: `decision_id` and `answer`, each taken from `args` when it is a `str` and degraded to `""` otherwise, exactly as DECISION F009 D20 ruled for `reason` and for the same reason — D14 types `args` as an object but never types what is inside it, and this door deliberately knows no command's argument schema. A `decision_id` of `""` matches no record, so `answer_task_decision` returns None and the request is refused 409 rather than raising, which is the same degradation path by construction.

FIFTH, WHAT THIS ROUND DELIBERATELY DOES NOT TEST, stated because DECISION F009 D16 forbids leaving a mechanism no test can reach and this round leaves two. MEASURED by the reviewer while assembling the block: the door, the two pin migrations and the three tests that would cover the new paths sum to 522 lines, over DECISION F085 D6's 490 cap, so the block does not fit and by D16's own rule a block that does not fit is not delivered. CHOSEN: this round lands the door and ONLY the two pin migrations that must move with it, both of which reach the 409 refusal path; the 200 acceptance path and the 501 guard are reached by NO test until the next round, which adds them purely additively together with the disk-level effect assertions in `tests/ui_server/test_command_dispatch.py`. That is exactly the cut DECISION F009 D19 made between R19 and R20 for `job.stop`, for the same measured reason, and it is the FOURTH time this feature has split on that single constraint — a fact recorded here rather than argued, because a later reader weighing how to plan a feature of this shape should have the count. The gap is explicit and scheduled rather than discovered: until that round lands, `save_job` running and the accepted body's `decision_id` field are asserted by nothing.

ALTERNATIVES: (a) pass `source="ui"` and widen the assumption log's vocabulary to three values — rejected, it changes a published artefact's meaning for every existing job to record something D6 already records elsewhere. (b) answer 404 rather than 409 for an absent decision — rejected by D21 already, and unchanged here. (c) delete the 501 and let an undispatched exposed id fall through — rejected, an unanswered request is the worst failure mode this door has and the guard costs four lines.

REVERSE the first clause by passing an explicit `source`, which requires first widening `ANSWER_SOURCE_*` and the two tallies that read them; the second by deleting the guard once a mechanism exists that makes an exposed-but-undispatched id impossible by construction; the third by giving refusals a richer body, which is a door-wide change rather than this command's.
<<<END DECISION22

<<<SLICE CONST_FROM
#: The one id this door dispatches for real; `decision.resolve` still answers the
#: seam. Named rather than inlined so its second call site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
<<<END CONST_FROM

<<<SLICE CONST_TO
#: What a `decision.resolve` naming no answerable decision returns (DECISION F009
#: D21). The effect RAN and DECLINED, so this is neither a shape error nor a
#: server fault, and it goes out through `_safe_error` like every other refusal
#: this door issues (DECISION F009 D22, third clause).
COMMAND_DECISION_STATE_MESSAGE = "decision is not open"

#: What an id that `_command_is_ui_exposed` admits but no dispatch clause matches
#: returns. DECISION F009 D22 keeps the 501 as a GUARD rather than a placeholder:
#: without it such a request falls off the end of the handler with no response
#: written at all.
COMMAND_NOT_DISPATCHED_MESSAGE = "command is exposed but not dispatched"

#: The two ids this door dispatches. Named rather than inlined so that each
#: second call site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
DECISION_RESOLVE_COMMAND_ID = "decision.resolve"
<<<END CONST_TO

<<<SLICE SEAM_FROM
        # `decision.resolve` keeps the seam until its own round: D5 maps it to
        # `answer_task_decision` followed by `save_job`, and that effect is not
        # wired here yet, so 501 is still the honest status for it.
        self._audit_attempt(str(job.id), "not_implemented", create=True, payload=payload)
        self._send_json(501, {
            "error": "command channel not yet accepting commands",
            "command": payload["command"],
        })
<<<END SEAM_FROM

<<<SLICE SEAM_TO
        # D5 maps `decision.resolve` to `answer_task_decision` followed by
        # `save_job`; DECISION F009 D21 rules that BOTH are the effect, because
        # the answer is durable only once `save_job` returns. D18's write order
        # above is unchanged: effect, then the audit line, then the publication.
        if payload["command"] == DECISION_RESOLVE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_decision_resolve(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body is None:
                # D21, clause three: the effect RAN and DECLINED — the decision
                # is absent or is no longer open. Nothing changed on disk, so
                # nothing is published and a retry cannot answer it differently.
                self._audit_attempt(str(job.id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_DECISION_STATE_MESSAGE))
                return
            # D18, clause three, re-examined by D21 and standing: both writes
            # below fail SOFT. The answer is already persisted, so refusing
            # after the fact would report an answer that really was written as
            # one that was not.
            self._audit_attempt(str(job.id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.id), payload["client_nonce"],
                                         accepted_body)
            self._send_json(200, accepted_body)
            return
        # An id `_command_is_ui_exposed` admitted that no clause above dispatches.
        # DECISION F009 D22: this is a GUARD, not a placeholder — unreachable
        # while the exposed subset holds exactly the two ids named above, and the
        # alternative is a request that gets no response at all.
        self._audit_attempt(str(job.id), "not_implemented", create=True, payload=payload)
        self._send_json(*_safe_error(501, COMMAND_NOT_DISPATCHED_MESSAGE))
<<<END SEAM_TO

<<<SLICE METHOD_FROM
        return {"command": payload["command"], "outcome": "accepted",
                "request_id": signal.request_id}

    def _publish_command_result(self, job_id: str, client_nonce: str,
<<<END METHOD_FROM

<<<SLICE METHOD_TO
        return {"command": payload["command"], "outcome": "accepted",
                "request_id": signal.request_id}

    def _dispatch_decision_resolve(self, job: Any,
                                   payload: Any) -> dict[str, Any] | None:
        """Answer one task decision and PERSIST it. None means the effect declined.

        DECISION F009 D21: `answer_task_decision` and `save_job` are BOTH the
        effect, because the answer is durable only once `save_job` returns, so a
        raise from either is D18 clause four's `rejected_effect`. A None return
        is NOT a failure — the decision is absent or is no longer open — and the
        caller answers it 409 and audits it `rejected_state`.

        DECISION F009 D22: `source` is deliberately NOT passed, so the answer
        takes `answer_task_decision`'s default of `human`. `answer_source` names
        WHO DECIDED over a closed two-value vocabulary that
        `escalation.escalation_assumptions_md` COUNTS, and a person answering
        through the UI is a human; passing this door's own name would land the
        record in neither tally. This is deliberately NOT DECISION F009 D20's
        rule for `request_stop`, whose `source` names the TRANSPORT instead.
        The door's own attribution lives in `commands_audit.jsonl` (D6).

        `decision_id` and `answer` degrade to "" when absent or non-string, for
        the reason D20 gave for `reason`: D14 types `args` as an object and never
        types what is inside it. An empty id matches no record, so the refusal
        path answers it rather than an exception.
        """
        from datetime import datetime, timezone

        from packages.orchestration.escalation import answer_task_decision
        from packages.orchestration.storage import save_job
        args = payload.get("args")
        args = args if isinstance(args, dict) else {}
        decision_id = args.get("decision_id")
        answer = args.get("answer")
        record = answer_task_decision(
            job, decision_id if isinstance(decision_id, str) else "",
            answer=answer if isinstance(answer, str) else "",
            now=datetime.now(timezone.utc))
        if record is None:
            return None
        save_job(job)
        return {"command": payload["command"], "outcome": "accepted",
                "decision_id": str(record.get("decision_id", ""))}

    def _publish_command_result(self, job_id: str, client_nonce: str,
<<<END METHOD_TO

<<<SLICE PINABSENT_FROM
    def test_absent_args_is_valid_and_reaches_the_seam(self):
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "decision.resolve", "client_nonce": "n-2"}),
            headers=self._auth_headers(token))
        assert (status, body["command"]) == (501, "decision.resolve")
<<<END PINABSENT_FROM

<<<SLICE PINABSENT_TO
    def test_absent_args_is_valid_and_reaches_the_effect(self):
        """Absent `args` is a SHAPE success: it reaches the effect, which declines.

        DECISION F009 D21: no `decision_id` names no answerable decision, so the
        effect RUNS and REFUSES, which is 409 and `rejected_state` — not the 400
        a shape error would give and not the 501 this pin asserted while the
        dispatch was a placeholder.
        """
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=json.dumps({"command": "decision.resolve", "client_nonce": "n-2"}),
            headers=self._auth_headers(token))
        assert status == 409, body
        assert body["error"] == "decision is not open", body
        assert self._audit_records()[-1]["outcome"] == "rejected_state"
<<<END PINABSENT_TO

<<<SLICE PINLOOP_FROM
    def test_every_exposed_command_reaches_the_answer_its_effect_gives(self):
        """The set itself is the contract, not the two literals above.

        `job.stop` dispatches and answers 200; `decision.resolve` keeps the seam
        until its own round, which is then ONE edit to the expectation below.
        """
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            expected = 200 if command_id == "job.stop" else 501
            assert status == expected, command_id
            assert body["command"] == command_id
<<<END PINLOOP_FROM

<<<SLICE PINLOOP_TO
    def test_every_exposed_command_reaches_the_answer_its_effect_gives(self):
        """The set itself is the contract, not the two literals above.

        BOTH exposed ids now dispatch. `job.stop` answers 200. A
        `decision.resolve` built by `_valid_body` carries no `args`, so it names
        no answerable decision and its effect RUNS and DECLINES: DECISION F009
        D21's 409, whose body carries `error` and not `command` because every
        refusal on this door goes out through the same safe-error shape.
        """
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        port, token = self._start_server()
        for index, command_id in enumerate(sorted(UI_EXPOSED_COMMANDS)):
            status, body = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(
                    command=command_id, client_nonce=f"nonce-exposed-{index}"),
                headers=self._auth_headers(token))
            if command_id == "job.stop":
                assert status == 200, command_id
                assert body["command"] == command_id
            else:
                assert status == 409, command_id
                assert body["error"] == "decision is not open", command_id
<<<END PINLOOP_TO
