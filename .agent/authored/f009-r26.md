── STEP T003 (the command.accepted SSE event) — F009 ──
Goal:        An ACCEPTED command announces itself on the job's own event stream,
             so the UI sees its own writes through the same truth channel it
             already reads. The feature file's Design names this event; F008
             built the transport. The round also records the R25 verdict, which
             was clean, and rules DECISION F009 D23.

Fortschritt: ~93 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen, sind beidseitig wirkungsgeprüft und melden
             sich jetzt auf dem SSE-Strom; offen bleiben der Import-Guard und
             die 405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R25 verdict ·
             C3 DECISION F009 D23 · C4 the emission · C5 its tests · C6 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r26.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `.agent/decisions.md` (C3) · `packages/orchestration/ui_server.py`
             (C4) · `tests/ui_server/test_command_channel.py` (C5) ·
             `.agent/handoff.md` (C6). NOTHING under `apps/` or `docs/` is
             touched.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. Commit order is C0a, C0b, C1, C2, C3, C4, C5, C6 and is not negotiable. C1
    precedes the ledger because the plan must be current before it (checklist
    item 23), and C3 precedes C4 because the code C4 lands cites D23 by name.
 3. PAIR SHAPES, each printed by the reviewer's own containment test on the
    exact bytes below, one reading per pair, never generalised:
      CONST  — `TO contains FROM: true`  → APPEND-shaped, §4.9 code obligation.
      PUB    — `TO contains FROM: false` → REWRITE.
      METH   — `TO contains FROM: true`  → APPEND-shaped, §4.9 code obligation.
      TESTS  — `TO contains FROM: true`  → APPEND-shaped, §4.9 code obligation.
    For every pair whose reading above is `true` the obligation is ORDERED
    EQUALITY per §4.9 as R-0531 narrowed it, NEVER a per-line count and NEVER a
    FROM-zero count: those slices are CODE and repeat lines structurally.
 4. THE PUB PAIR IS APPLIED TWICE. Its FROM occurs EXACTLY 2 times in
    `packages/orchestration/ui_server.py` at the round base — the reviewer
    counted 2 on the base bytes — and BOTH occurrences are replaced, because
    both are the accepted exit of a dispatch clause. Every other pair's FROM
    occurs exactly ONCE. Apply CONST, METH and TESTS first and PUB last, so the
    bulk replacement runs over a remainder no other pair still touches
    (findings R-0639 and R-0640's rule).
 5. C2 is an APPEND — LEDGER26 to `.agent/live_review.md`. That target ends in
    exactly ONE newline at the round base, which the reviewer measured on the
    bytes, so the append is one newline followed by the slice. LEDGER26 carries
    ONE paragraph.
 6. C3 is an APPEND — DECISION23 to `.agent/decisions.md`. That target also ends
    in exactly ONE newline at the round base, measured on the bytes, so that
    append is likewise one newline followed by the slice.
 7. This round mints NO id and resolves none. It writes no `Done:` line and no
    `Landed:` line. The next free id is R-0642 when this round ends, exactly as
    when it started. The 78-line R25 handback is NOT a new finding: R-0582 is
    OPEN and already holds that defect, and checklist item 30 forbids a second
    id for it.
 8. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 9. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5, which is finding R-0640's fix: this
    block is 451 lines TOTAL against DECISION F085 D6's 490 cap, 233 of them
    PROSE against D5's 400. Re-measure both from the committed C0a blob; a
    disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C6: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2, C3, C4 and C5. Report the round base
     SHA you read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r26.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 9's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R26 — report `cmp` exit and
     both sha256, with a negative control against another file exiting non-zero
     — and `wc -l` against the 50-line cap of AGENTS.md. Line-anchored,
     `^## Goal$` and `^## Next Steps$` each read 1.
 G5  APPEND, under TWO independent readers, with a negative control on the FIRST
     appended paragraph (finding R-0631). Run this for C2 over
     `.agent/live_review.md` AND for C3 over `.agent/decisions.md`, each based
     on the round base: (a) the base blob is a byte-exact PREFIX and the
     remainder equals a newline plus that slice — report its sha256, bytes and
     lines; (b) N is counted BY YOUR SCRIPT and the last N blank-line units
     equal the slice's N paragraphs IN ORDER. Then flip one printable byte in
     the FIRST appended paragraph, at equal length, and report that BOTH readers
     REJECT the flip while both ACCEPT the true file. Report before/after bytes
     and lines for each of the two files.
 G6  Line-anchored at line START over `.agent/live_review.md` at the round base
     and at C2 (finding R-0630): a leading `- R-` id with every captured id
     DISTINCT at each; a leading `Done: R-` id; a leading `Landed: `; a leading
     `Gate: R` key over that many DISTINCT keys; the `Gate: R26` key; and a
     leading `- R-0642` entry, which must read 0 at BOTH because this round
     mints no id at all. Report each pair of readings, the max REGISTERED id,
     and the open count by DECISION F009 D10's rule at C2. Read every one of
     these at line START and not as a bare substring: this file legitimately
     QUOTES ids and gate keys inside its own verdict prose, so an unanchored
     scan reports a maximum that was never registered (finding R-0630).
 G7  PAIRS. For EACH pair named in constraint 3 report, on whole lines and again
     indent-agnostically, with the two readings required to AGREE: the FROM
     count in its target at the round base and after its commit, and the TO
     count at both. Read the BASE side with `git show <base>:<path>` into a
     variable or into scratch under `.remedy-wt/` — never by writing the base
     blob over the tracked file, which guardrail G5 forbids (finding R-0594).
     The reviewer's base readings, which yours must reproduce:
     CONST_FROM 1, PUB_FROM 2, METH_FROM 1, TESTS_FROM 1, and each TO 0. After
     application every TO reads its FROM's base count and no FROM other than an
     APPEND-shaped one still occurs on its own. For the three APPEND-shaped
     pairs report the containment reading your OWN script printed — the words
     `TO contains FROM: true` — beside the §4.9 ordered-equality proof, and
     order NO FROM-zero count for them (finding R-0522).
 G8  ORDERED EQUALITY for C4 and C5, which is §4.9's obligation for a code
     append as R-0531 narrowed it. For each of the two commits report that the
     lines that commit's diff ADDS are exactly the applied slice's lines IN
     ORDER, compared as a list, and report `git show --numstat` for it. The
     reviewer measured 40 insertions and 0 deletions for C4 and 112 insertions
     and 0 deletions for C5 on its own dry run; report the numbers YOU measure
     and flag any difference rather than reconciling it.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree (finding R-0518). Report each command's REAL
     exit code and the count IT printed — predict no number:
       `python3 -m ruff check packages/orchestration/ui_server.py
        tests/ui_server/test_command_channel.py`
       `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The canary is unconditional; the four-path group is owed because this
     round's change set holds `.agent/` state files AND the UI server (finding
     R-0607). The reviewer ran all four at the round base before ordering them:
     each exits 0, so each can fail honestly (R-0364). Ruff was run at the base
     over the SAME two paths and exits 0 there, so the comparison is exit-0 to
     exit-0 rather than a multiset.
 G10 RED PROOF, in a DISPOSABLE worktree under `.remedy-wt/` and NEVER in the
     primary checkout (§4.10, guardrail G5). Mutations (a) and (b) below, each
     reverted before the next, each reported with the ids that failed:
     (a) delete BOTH occurrences of the single line
         `            self._emit_command_accepted_event(str(job.id), accepted_body)`
         in `packages/orchestration/ui_server.py` — that exact byte string, with
         its leading twelve spaces, occurs EXACTLY 2 times in THAT file at C5
         and nowhere else in it, which the reviewer counted on the C5 bytes
         whole-line and indent-agnostically, both agreeing; report the count you
         measure. EXPECT exactly the ids listed here to fail:
         `test_an_accepted_command_reaches_the_sse_frame_it_announces`,
         `test_a_replay_announces_nothing_a_second_time` and
         `test_an_event_writer_that_raises_changes_neither_status_nor_body`.
     (b) restore them, then insert that SAME line, with `payload` in place of
         `accepted_body`, directly BELOW the `rejected_state` audit call in the
         `decision.resolve` clause, so D21's 409 announces too. EXPECT exactly
         the id named here to fail: `test_a_refused_command_announces_nothing`.
     Neither mutation reaches the other's expected set, and that is why both are
     ordered rather than one: a negative test does not go red when its subject
     is DELETED, it goes red when the subject SPREADS (checklist item 5). The
     reviewer ran both mutations itself in a disposable worktree at the intended
     final tree and the two sets above are the ids that actually failed there.
     Report the ids that actually failed and flag any difference from the two
     sets above rather than reconciling it. Remove the worktree and report
     `git worktree list` at 1 line before C6.
 G11 RANGE: the range from the round base to C5 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `apps/` or `docs/`. Each commit has ONE
     parent; `git show --numstat` and `git diff --numstat` AGREE on every cell —
     invoke `git show` WITHOUT a `--` before the SHA, which turns it into a
     pathspec and prints nothing; every cell equals the `+/-` column of the
     handback's `## Commits` table (checklist item 28), compared cell by cell.
     Report each pre-handback commit's insertions against the 500 cap of
     AGENTS.md DECISION F104 D1; the handback commit's own numbers belong in the
     round report (item 14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in
     every file a slice lands in, which are `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/decisions.md`,
     `packages/orchestration/ui_server.py` and
     `tests/ui_server/test_command_channel.py`. `git ls-files
     .remedy-wt` reads 0. Classify THIS ROUND's reflog rows by the operation
     before the first `:` and report `amend`, `rebase` and `cherry` each 0;
     assert no total over the whole reflog (R-0601).
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3, C4, C5 and C6, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all four of its lines. Report
     its `wc -l` against the 100-line cap AGENTS.md allows for a per-commit
     table of more than five commits, which the commit sequence constraint 2
     fixes is. EVERY numeral this file states about the round's own measurements is
     COUNTED mechanically before it is written, or no numeral is stated and the
     enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C6.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R26
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
R26 lands the `command.accepted` event and records the R25 verdict. An accepted
command now appends the event to the job's run log, which is where the F008 SSE
stream reads, so the UI sees its own writes on the channel it already watches.
Refusals and replays announce nothing.

## Next Steps
1. The queue-only import guard, whose allowed set includes `save_job` because
   DECISION F009 D5's own effect mapping names it, and `append_run_event`
   because DECISION F009 D23's emission needs it.
2. Then the route-walking 405 test proving every other mutating method answers
   405; then the integration gate and closure.

## Risks
- `answer_source` is a two-valued field the escalation assumption log COUNTS.
  DECISION F009 D22 rules that this door must NOT pass its own source into it,
  the opposite of D20's rule for `request_stop`; a later round that generalises
  one to the other silently drops answers from both tallies.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R26

<<<SLICE LEDGER26
Gate: R26 — the R25 entry. R25 PASSED, and it PASSED CLEAN: no finding, no deviation, and every numeral it stated about its own bytes reproduced under the reviewer's own re-execution off disk rather than being read back out of the handback. ONE HONEST LIMIT IS STATED RATHER THAN PAPERED OVER: R25 was emitted by a session that has ended, so the reviewer's emitted original no longer exists and neither the primary `cmp`-against-scratchpad proof of §4.9 nor its digest fallback could be performed; what WAS proved is that the two committed copies are byte-equal to each other, and every slice applied is byte-equal to the copy committed at C0a, which is the property the applications actually depend on. TRANSPORT: `.agent/authored/f009-r25.md` at `cf658e26` and `.agent/last_block.md` at `5212f39a` are both sha256 0de7a9019fe3c6c80226c4f7484f331ac280924aa0fd8714a256adbaf82a75a7 over 16694 bytes and 176 lines, and `.agent/last_block.md` still holds those same bytes at `cd77e969`. The reviewer's own extraction out of the committed C0a blob prints an aggregate of 2 slices over 38 CONTENT lines — PLANF009R25 `bcda0e23…` at 2039 bytes and 37 lines, LEDGER25 `4f76e1ab…` at 5479 bytes and 1 line — and constraint 6's numerals re-measure as 176 TOTAL and 138 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `7bf5bb21` is BYTE-EQUAL to PLANF009R25 at the same `bcda0e23…` digest, 37 lines against the 50-line cap, with `^## Goal$` and `^## Next Steps$` each reading 1 and a negative control against another file differing. THE APPEND HOLDS UNDER THE REVIEWER'S OWN TWO READERS: at `84f81a31` the round-base blob is a byte-exact prefix of `.agent/live_review.md`, the remainder is exactly a newline plus LEDGER25 at sha256 `590b1061…` over 5480 bytes and 2 lines, the file going 524945 to 530425 bytes and 1116 to 1118 lines, N counted at 1 BY THE SCRIPT, the base ending in exactly ONE newline measured on the bytes; an equal-length printable-byte flip in the FIRST appended paragraph makes BOTH readers REJECT while both ACCEPT the true file. THE SETS HELD line-anchored at line start, round base and C2: entries 207 at BOTH with every id DISTINCT at each — this round minted none — leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 24 and 25 over that many DISTINCT keys, the `Gate: R25` key 0 and 1, a leading `- R-0642` entry 0 at both, max REGISTERED id R-0641 at both, and 204 open at both by DECISION F009 D10's rule. THE LEDGER ENTRY'S OWN HEADER WAS COMPARED AGAINST THE SERIES IT JOINS, which is checklist item 26 run rather than recalled: `Gate: R25 — the R24 entry.` matches the shape of every entry above it and the 25 keys are 25 DISTINCT keys, so the duplicate-header defect R-0587 records did not recur. `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C3 at sha256 `25f2d750…` over 473798 bytes, which is that round's rules-nothing constraint as a measurement. THE SUITES ARE THE REVIEWER'S OWN, re-run serially in the primary checkout: the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 513 passed, both exactly the counts the handback printed and neither predicted by it. THE RANGE HELD: the range base→`cd77e969` lists exactly the declared paths, set difference EMPTY in both directions, and 0 paths beginning `packages/`, `apps/`, `tests/` or `docs/`, which is that round's no-code constraint as a measurement; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 176/0, 82/189, 4/4 and 2/0; pre-handback insertions 176, 82, 4 and 2, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in both slice targets; `git ls-files .remedy-wt` 0; the reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict. THE VERDICT LEDGER25 ITSELF CARRIES WAS SPOT-CHECKED RATHER THAN TRUSTED, because it is the permanent record of R24 and no later round re-reads R24: `.agent/authored/f009-r24.md` at `7a349543` and `.agent/last_block.md` at `ac255fd0` both re-measure to sha256 fe07f2c38e0717c1d7ae5068a8e370bdc0aa46d6dcd555f2507ec1eda418ff51 over 21814 bytes and 283 lines, and R24's per-commit cells re-measure to 283/0, 192/373, 12/16, 2/0 and 76/0 in that order — every value LEDGER25 states. THE HANDBACK DECLARED ITS READINGS RATHER THAN HIDING THEM: its G6 line notes that an UNANCHORED `R-\d+` scan returns R-0642 because LEDGER25's prose quotes that id while reporting its own zero-reading, and the reviewer's own line-anchored measurement returns a max REGISTERED id of R-0641 with a leading `- R-0642` count of 0 at both readings, so the distinction the handback drew is the correct one. ONE READING IS RECORDED WITHOUT A NEW ID, DELIBERATELY: `.agent/handoff.md` at `cd77e969` is 78 lines, above the 60 AGENTS.md caps a handback at when its per-commit table covers five commits or fewer, and its G10 line names both the count and the cause on disk, which is what DECISION D15 requires of a declared overage and what finding R-0430's standing rule adds to it. No id is minted, because R-0582 is OPEN and holds exactly this defect and checklist item 30 forbids a second id for one defect. R25 is instead the round in which R-0582's own cheaper repair first landed: its G10 ordered the gate transcripts into the round report rather than into the handback, and the handback fell from the 223 lines R-0582 measured at R12 to 78 here — the first round on this branch whose overage shrank rather than grew.
<<<END LEDGER26

<<<SLICE DECISION23
## DECISION F009 D23 — the `command.accepted` event: where it is written, when, and what it carries (2026-08-22)

Measured by the reviewer at `cd77e969`, before this round was delegated, by reading the F008 stream end to end rather than only the door: `iter_sse_frames` is driven by `lambda: _load_events(job)`, `_load_events` calls `timeline.load_run_events(resolve_data_root(), job.id)`, and that function globs `<data root>/runs/<job id>/*.jsonl`. The stream therefore has no queue and no subscriber of its own — it is a TAIL of the job's run log, and the only way to put an event on it is to append one there.

FIRST, THE WRITER. CHOSEN: `timeline.append_run_event`, the wrapper this repository's other event writers already reach for — `autorun.py`, `do_run.py`, `builder_bridge.py`, `event_replay.py`, `job_fulfillment.py` and `repair_loop.py` among them, measured at `cd77e969`. ALTERNATIVES: (a) a new publish/subscribe seam inside `ui_server.py` — rejected, it would make the SSE stream and the cursor endpoint two contracts where `_safe_event_summary` deliberately keeps them one. (b) `commands_audit.jsonl` — rejected, and this is DECISION F009 D6's rejected alternative (b) read in the other direction: that record is per JOB and must outlive a run, while this is a live NOTIFICATION, so the two artefacts want opposite storage and both choices stand.

SECOND, WHEN. CHOSEN: LAST, after the publication DECISION F009 D18 orders third, making the emission D18's FOURTH write. A client that sees this frame will replay its nonce, and a client that replays before the publication lands gets a MISS — which sends it back through the door and runs the effect a second time. The ordering is the whole guard: `request_stop` is idempotent but `answer_task_decision` followed by `save_job` is not obliged to be.

THIRD, HOW IT FAILS. CHOSEN: SOFT, catching `OSError`, `RuntimeError`, `ValueError` and `TypeError` and returning, for D18 clause three's reason — the effect is already durable, so a full disk must not turn an accepted command into a 500 reporting it as refused. The caught set is spelled out rather than written as `except Exception`, which `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals` guarded this module against at `cd77e969`.

FOURTH, WHAT IT CARRIES. CHOSEN: `outcome="accepted"` as a NAMED parameter of `RunLogWriter.log` — not metadata, because `_safe_event_summary` reads `outcome` at the top level and a value one level down arrives on the wire as the empty string — plus the command id in metadata, which that summary drops. The frame is therefore `{seq, event, timestamp, outcome}` and carries no args, no nonce and no token: the stream is the job's own channel and D6 keeps this door's attribution in the audit file.

FIFTH, WHICH EXITS EMIT. CHOSEN: only the two ACCEPTED exits. A refusal announces nothing, and a replay announces nothing a second time — a replay REPEATS an acceptance rather than being one, which is the rule finding R-0636 already forced on the audit vocabulary, applied here so the UI cannot count a retry after a timeout as a second write.

REVERSE the first by moving the call behind a seam of its own; the second by re-ordering the two calls, which the replay-race argument above is the case against; the third by letting the exception escape, which converts a notification failure into a server fault; the fourth by widening `_safe_event_summary`, which would change both transports at once and is F008's contract rather than this door's; the fifth by emitting on refusals, which the tests this round ships forbid.
<<<END DECISION23

<<<SLICE CONST_FROM
#: The two ids this door dispatches. Named rather than inlined so that each
#: second call site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
<<<END CONST_FROM

<<<SLICE CONST_TO
#: The event one ACCEPTED command appends to the job's run log, and through it
#: to the F008 SSE stream (DECISION F009 D23). The spelling is the feature file's.
COMMAND_ACCEPTED_EVENT = "command.accepted"

#: The two ids this door dispatches. Named rather than inlined so that each
#: second call site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
<<<END CONST_TO

<<<SLICE METH_FROM
    def _audit_attempt(self, job_id: str, outcome: str, *, create: bool,
<<<END METH_FROM

<<<SLICE METH_TO
    def _emit_command_accepted_event(self, job_id: str,
                                     body: dict[str, Any]) -> None:
        """Announce one accepted command on the job's own event stream.

        DECISION F009 D23: this is D18's FOURTH write and it runs LAST, after
        the publication D18 orders third. A client that sees this frame and
        replays its nonce must find the published result, so emitting first
        would let a fast client race the door into running one effect twice.

        It fails SOFT for D18 clause three's reason: the effect is already
        durable, and a failed notification must not report a command that
        really ran as one that did not.

        `outcome` is a NAMED parameter of `RunLogWriter.log` rather than
        metadata, which is why it survives into `_safe_event_summary`'s
        envelope and reaches the SSE frame at all. The command id rides in
        metadata, where that summary drops it: the stream is the job's own
        channel and DECISION F009 D6 keeps this door's attribution in
        `commands_audit.jsonl`. This is not D6's rejected alternative (b)
        arriving by the back door — that record is per JOB and must outlive a
        run, while this is a live NOTIFICATION and the run log is exactly
        where the stream reads.
        """
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import append_run_event
        try:
            append_run_event(
                resolve_data_root(), job_id,
                event=COMMAND_ACCEPTED_EVENT,
                metadata={"outcome": "accepted",
                          "command": str(body.get("command", ""))})
        except (OSError, RuntimeError, ValueError, TypeError):   # D23, clause two
            return

    def _audit_attempt(self, job_id: str, outcome: str, *, create: bool,
<<<END METH_TO

<<<SLICE PUB_FROM
                                         accepted_body)
            self._send_json(200, accepted_body)
<<<END PUB_FROM

<<<SLICE PUB_TO
                                         accepted_body)
            self._emit_command_accepted_event(str(job.id), accepted_body)
            self._send_json(200, accepted_body)
<<<END PUB_TO

<<<SLICE TESTS_FROM
    # -- B: the GET door still behaves as it did ----------------------------
<<<END TESTS_FROM

<<<SLICE TESTS_TO
    # -- E: an accepted command announces itself (DECISION F009 D23) --------

    def _run_events(self):
        """Every run-log event for this job, read the way the stream reads them."""
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        return load_run_events(resolve_data_root(), self.job_id)

    def _accepted_events(self):
        from packages.orchestration.ui_server import COMMAND_ACCEPTED_EVENT
        return [e for e in self._run_events()
                if e.get("event") == COMMAND_ACCEPTED_EVENT]

    def test_an_accepted_command_reaches_the_sse_frame_it_announces(self):
        """The ledger event AND the frame the stream builds out of it.

        `_safe_event_summary` is the one writer both event transports share, so
        a field it drops never reaches a client however faithfully the ledger
        recorded it. `outcome` survives only because `RunLogWriter.log` takes it
        as a NAMED parameter: the same value passed as plain metadata would sit
        one level down and arrive on the wire as the empty string.
        """
        from packages.orchestration.ui_server import (
            COMMAND_ACCEPTED_EVENT,
            _safe_event_summary,
            sse_event_frame,
        )

        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce="nonce-sse-accept"),
            headers=self._auth_headers(token))
        assert status == 200, body

        events = self._run_events()
        matches = [(seq, e) for seq, e in enumerate(events)
                   if e.get("event") == COMMAND_ACCEPTED_EVENT]
        assert len(matches) == 1, events
        seq, event = matches[0]
        assert event["outcome"] == "accepted", event
        assert event["metadata"]["command"] == "job.stop", event

        frame = sse_event_frame(seq, _safe_event_summary(seq, event))
        payload = json.loads(frame.decode().split("data: ", 1)[1])
        assert payload["event"] == COMMAND_ACCEPTED_EVENT, payload
        assert payload["outcome"] == "accepted", payload
        assert payload["seq"] == seq, payload
        # The args never reach the stream: the safe summary is a fixed envelope,
        # and D6 keeps this door's own attribution in the audit file.
        assert "command" not in payload, payload

    def test_a_refused_command_announces_nothing(self):
        """The discriminator. A `decision.resolve` with no args is D21's 409.

        Its effect RAN and DECLINED, so the door leaves on a refusal path this
        round must keep silent — without this test the emission could sit on
        every exit of the handler and still look correct.
        """
        port, token = self._start_server()
        status, _ = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(command="decision.resolve",
                                  client_nonce="nonce-sse-refused"),
            headers=self._auth_headers(token))
        assert status == 409
        assert self._accepted_events() == []

    def test_a_replay_announces_nothing_a_second_time(self):
        """A replay REPEATS an acceptance rather than being one (R-0636's rule).

        The UI would otherwise see two frames for one effect and count a retry
        after a timeout as a second write.
        """
        port, token = self._start_server()
        for _ in range(2):
            status, _ = self._request(
                port, "POST", self._commands_path(),
                body=self._valid_body(client_nonce="nonce-sse-replay"),
                headers=self._auth_headers(token))
            assert status == 200
        assert len(self._accepted_events()) == 1

    def test_an_event_writer_that_raises_changes_neither_status_nor_body(
            self, monkeypatch):
        """DECISION F009 D23 clause two, proved rather than asserted.

        The effect is already durable when this write runs, so a full disk must
        not turn an accepted command into a 500 reporting it as refused.
        """
        from packages.orchestration import timeline

        calls = []

        def _raise_no_space(*_args, **_kwargs):
            calls.append(1)
            raise OSError("no space left on device")

        monkeypatch.setattr(timeline, "append_run_event", _raise_no_space)
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(client_nonce="nonce-sse-raises"),
            headers=self._auth_headers(token))
        assert status == 200, body
        assert body["outcome"] == "accepted", body
        # The counter is what makes this a test of the SOFT FAILURE rather than
        # of a door that never emits: a handler with no call site at all would
        # satisfy every line above it.
        assert calls == [1], calls
        assert self._accepted_events() == []

    # -- B: the GET door still behaves as it did ----------------------------
<<<END TESTS_TO
