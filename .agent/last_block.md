── STEP T003 (test what R23 shipped untested) — F009 ──
Goal:        Pay DECISION F009 D22's fifth clause, which scheduled this round by
             name. R23 landed the `decision.resolve` dispatch with only its 409
             refusal path under test: the 200 acceptance path and the 501 guard
             were reached by nothing. This round adds two tests that reach both,
             purely additively, and asserts all THREE writes DECISION F009 D18
             orders for an accepted command — the effect read back off disk, the
             `accepted` audit line and the nonce publication — which is the
             treatment `job.stop` already has. It touches NO production file.

Fortschritt: ~90 % (T001 gebaut · T002 gebaut · T003 fast fertig: beide
             Kommandos dispatchen und sind jetzt beidseitig wirkungsgeprüft;
             offen bleiben das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R23 verdict ·
             C3 the two tests · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r24.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `tests/ui_server/test_command_channel.py` (C3) ·
             `.agent/handoff.md` (C4). NOTHING under `packages/`, `apps/` or
             `docs/` is touched, and `.agent/decisions.md` is NOT touched: this
             round rules nothing and amends nothing.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 is an APPEND — LEDGER24 to `.agent/live_review.md`. That target ends in
    exactly ONE newline at the round base, which the reviewer measured on the
    bytes, so the append is one newline followed by the slice. LEDGER24 carries
    ONE paragraph.
 3. ONE FROM/TO PAIR, TESTS, over `tests/ui_server/test_command_channel.py`, and
    it is the whole of C3. THE REVIEWER CLASSIFIED IT BEFORE WRITING THE GATE
    THAT MEASURES IT: this pair IS APPEND-SHAPED — its TO re-quotes its FROM
    verbatim and puts the two new tests in front of it — so by finding R-0639's
    binding rule its after-clause is "the FROM STILL reads 1 and the TO reads
    1", never "the FROM reads 0". Do not report an unconverted site for it; that
    reading does not apply to a pair of this shape.
 4. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable. C1 precedes
    the ledger because the plan must be current before it (checklist item 23).
 5. This round mints NO id and resolves none: R23 was clean and LEDGER24 is a
    verdict paragraph with no finding under it. It writes no `Done:` line. The
    next free id is R-0642 when this round ends, exactly as when it started.
 6. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all FOUR of its lines.
    Four is the reviewer's own count of this block's bytes.
 7. SIZE, measured at emission by reading it back out of the assembled bytes and
    computing PROSE as TOTAL minus the slices' CONTENT lines, with marker lines
    counted as prose per DECISION F085 D5, which is finding R-0640's fix: this
    block is 283 lines TOTAL against DECISION F085 D6's 490 cap, 165 of them
    PROSE against D5's 400. Re-measure both from the committed C0a blob; a
    disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C4: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a, C0b, C1, C2 and C3. Report the round base SHA you
     read at step 0.
 G2  TRANSPORT: `.agent/authored/f009-r24.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 7's two numbers from that same blob — TOTAL, and PROSE as TOTAL
     minus the summed slice-CONTENT lines — and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R24 — report `cmp` exit and
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
     `Gate: R` key over that many DISTINCT keys; the `Gate: R24` key; and a
     leading `- R-0642` entry, which must read 0 at BOTH because this round
     mints no id at all. Report each pair of readings, the max id, and the open
     count by DECISION F009 D10's rule at C2. Report what you measure, not what
     this sentence expects.
 G7  `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C4 — the
     same sha256 — because this round rules nothing. Report both digests.
 G8  THE ONE PAIR, proved as a pair. Count TESTS_FROM and TESTS_TO in
     `tests/ui_server/test_command_channel.py`, BOTH whole-line and
     indent-agnostic, and require the two readings to AGREE at every count.
     Before C3 the FROM reads 1 and the TO reads 0; after C3 BOTH read 1,
     because constraint 3 classified this pair as APPEND-SHAPED. Report, as a
     value your SCRIPT prints, that the TO CONTAINS the FROM as a contiguous
     line block — which must be TRUE, and which is what proves the after-state
     is the append it was authored as rather than a failed application.
 G9  RUFF AND SUITES, run SERIALLY in the PRIMARY checkout, never two pytest
     processes at once and never in a worktree. Report each command's REAL exit
     code and the count IT printed — predict no number:
       `python3 -m ruff check tests/ui_server/test_command_channel.py`
       `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The reviewer ran all four at the round base before ordering them: each
     exits 0, so each can fail honestly (R-0364).
 G10 RED CONTROL, in a DISPOSABLE worktree only (guardrail G5), never in the
     primary checkout. At C3, revert `packages/orchestration/ui_server.py` ALONE
     to its PRE-R23 bytes, which are that path's blob at `9a47166c` — prove the
     mutation is REAL by reporting `git diff HEAD --numstat` for it and that the
     file is byte-equal to that blob — and run
     `python3 -m pytest tests/ui_server/test_command_channel.py -q -rf`.
     Report the REAL exit code and WHICH tests failed. BOTH tests this round
     adds must be among them: a test that passes against the pre-R23 door never
     reached what R23 shipped, which is the defect this round exists to prevent.
     Remove the worktree afterwards and report `git worktree list` back at 1
     line.
 G11 RANGE: the range from the round base to C3 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/` or `docs/`, which is
     this round's no-production-code constraint as a measurement. Each commit
     has ONE parent; `git show --numstat` and `git diff --numstat` AGREE on
     every cell — invoke `git show` WITHOUT a `--` before the SHA, which turns
     it into a pathspec and prints nothing; every cell equals the `+/-` column
     of the handback's `## Commits` table (checklist item 28), compared cell by
     cell. Report each pre-handback commit's insertions against the 500 cap of
     AGENTS.md DECISION F104 D1. Leading `<<<SLICE ` and `<<<END ` read 0 LINES
     in every file a slice lands in, a set the reviewer counted at two:
     `.agent/plan.md` and `tests/ui_server/test_command_channel.py`.
     `git ls-files .remedy-wt` reads 0. Classify THIS ROUND's reflog rows by the
     operation before the first `:` and report `amend`, `rebase` and `cherry`
     each 0; assert no total over the whole reflog (R-0601).
 G12 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM across all four of its lines. Report
     its `wc -l` against the 60-line cap, or against 100 with a stated cause.
     EVERY numeral this file states about the round's own measurements is
     COUNTED mechanically before it is written, or no numeral is stated and the
     enumeration speaks (R-0404, R-0641).

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C4.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R24
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
R24 pays DECISION F009 D22's fifth clause, which scheduled it by name. R23's
dispatch had only its 409 refusal path under test; this round reaches the 200
acceptance path and the 501 guard, and asserts all three writes D18 orders for
an accepted command. It touches no production file.

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
<<<END PLANF009R24

<<<SLICE LEDGER24
Gate: R24 — the R23 entry. R23 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r23.md` at `16904e69`, `.agent/last_block.md` at `3f0bf26f` and the bytes the reviewer EMITTED, still on disk, are all sha256 0166cb2cbf86413d8f604b124f52354c498b945269da2c82c830c2a4d00191f5 over 39789 bytes and 464 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own extraction out of the committed C0a blob gives 13 slices over 244 CONTENT lines, and constraint 8's numerals re-measure as 464 TOTAL and 220 PROSE, both under DECISION F085 D6's 490 and D5's 400. `.agent/plan.md` at `78664c08` is BYTE-EQUAL to PLANF009R23 at 41 lines against the 50-line cap. BOTH APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS EACH, with an equal-length printable-byte flip in the FIRST appended paragraph REJECTED by both while both ACCEPT the true file: `.agent/live_review.md` went 512626 to 520130 bytes and 1110 to 1114 lines with N counted at 2, `.agent/decisions.md` 467250 to 473798 bytes and 6887 to 6909 lines with N counted at 11. THE FIVE PAIRS ARE PROVED AS PAIRS, whole-line and indent-agnostic with the two readings agreeing at every count: before C4 every FROM reads 1 and every TO 0, after C4 every FROM reads 0 and every TO 1, and the containment reading printed FALSE five times, so constraint 3's not-append-shaped classification is a MEASUREMENT rather than a claim. THE SEAM IS GONE AS A PLACEHOLDER: line-anchored over `packages/orchestration/ui_server.py`, the quoted `command channel not yet accepting commands` reads 1 then 0, `_dispatch_decision_resolve` 0 then 2 — one definition and one call site — and the quoted `not_implemented` 1 at BOTH, because DECISION F009 D22 keeps that writer as the GUARD rather than deleting it. THE CODE IS EXACTLY THE AUTHORED SLICES AND NOTHING MORE, which is the reading that matters for a round touching `packages/`: the reviewer read the real diff of `15b8f85f` and the door is the three authored pairs and no fourth change, the pin file the two authored pairs and nothing else. THE SETS HELD line-anchored at line start, round base and C2: entries 206 and 207 with every id DISTINCT at each, leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 22 and 23 over that many DISTINCT keys, the `Gate: R23` key 0 and 1, a leading `- R-0641` entry 0 and 1, a leading `- R-0642` entry 0 at both, max id R-0640 and R-0641, and 203 then 204 open by DECISION F009 D10's rule; over `.agent/decisions.md` the `## DECISION ` total went 106 to 107 and the `## DECISION F009 D22 ` key 0 to 1. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the two changed paths EXITS 0, `test_command_channel.py` EXITS 0 at 84 passed, `test_command_dispatch.py` EXITS 0 at 4 passed, `test_command_audit.py` EXITS 0 at 17 passed, the canary EXITS 0 at 42 passed and the four-path state-reader group EXITS 0 at 511 passed — not one of the six predicted by the handback. THE RED CONTROL IS THE REVIEWER'S OWN, run in a disposable worktree with the door alone reverted to its pre-round bytes: `git diff HEAD --numstat` reads 9/93 over `packages/orchestration/ui_server.py`, and under it `test_command_channel.py` EXITS 1 with exactly the two migrated pins failing on `assert 501 == 409` — so both genuinely reach the dispatch rather than passing beside it. THE RANGE HELD: the range to C4 lists exactly the declared paths with the set difference EMPTY in both directions, 0 beginning `apps/` or `docs/` and 0 equal to `packages/orchestration/command_audit.py`; every commit has ONE parent; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 464/0, 368/186, 16/15, 4/0, 22/0 and 93/9 with 22/7; pre-handback insertions 464, 368, 16, 4, 22 and 115, every one under the 500 cap; zero leading `<<<SLICE ` and `<<<END ` LINES in all five slice targets; `git ls-files .remedy-wt` 0; the reflog rows classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `46189950`, the same SHA the reviewer read. R-0641'S OWN FIX HELD IN THE ROUND THAT REGISTERS IT, which is the reason this entry carries no new finding: the handback's G12 line states its path count as one "the script printed" and its commit count as one the script counted, and the reviewer's independent measurement returns 7 paths and 6 commits in that range — the numerals are pasted from measurement rather than typed beside it, which is exactly what R-0641 binds.
<<<END LEDGER24

<<<SLICE TESTS_FROM
    def test_unexposed_catalog_command_is_400_on_field_command(self):
        """`job.list` is a real catalog id that the write door does not expose."""
<<<END TESTS_FROM

<<<SLICE TESTS_TO
    def test_a_decision_resolve_naming_an_open_decision_is_answered_and_saved(self):
        """DECISION F009 D21's success path, read back off disk.

        The two writes D21 rules to be ONE effect are both checked: the record is
        `answered` in memory only if `answer_task_decision` ran, and it is that
        way in a job RELOADED from storage only if `save_job` ran too. The
        `answer_source` assertion is DECISION F009 D22 made testable — `human`,
        never this door's own name, because the escalation assumption log counts
        that field into exactly two buckets and "ui" is in neither.
        """
        from datetime import datetime, timezone

        from packages.orchestration.command_nonce import lookup_nonce_result
        from packages.orchestration.escalation import (
            enqueue_task_decision,
            find_task_decision,
        )
        from packages.orchestration.storage import load_job, save_job

        record = enqueue_task_decision(
            self.job, task_id=self.job.tasks[0].id,
            question="Which database should the task use?",
            now=datetime.now(timezone.utc))
        save_job(self.job)
        decision_id = record["decision_id"]

        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command="decision.resolve", client_nonce="nonce-resolve",
                args={"decision_id": decision_id, "answer": "postgres"}),
            headers=self._auth_headers(token))

        assert status == 200, body
        assert body["outcome"] == "accepted", body
        assert body["decision_id"] == decision_id, body
        answered = find_task_decision(load_job(self.job.id), decision_id)
        assert answered["status"] == "answered", answered
        assert answered["answer"] == "postgres", answered
        assert answered["answer_source"] == "human", answered
        assert self._audit_records()[-1]["outcome"] == "accepted"
        # D18's third write. With the effect and the audit line above, all three
        # writes D18 orders for an ACCEPTED command are now asserted for
        # `decision.resolve`, as they already were for `job.stop`.
        assert lookup_nonce_result(
            self.job_id, "nonce-resolve",
            control_root_path=self.tmp_path / "control") == {"status": 200,
                                                             "body": body}

    def test_an_exposed_id_with_no_dispatch_branch_is_the_501_guard(self, monkeypatch):
        """DECISION F009 D22's guard, and the only test that reaches it.

        Reachable only by exposing an id this door does not dispatch, which is
        exactly the mistake the guard exists to catch: without it such a request
        falls off the end of the handler with no response written at all.
        """
        from apps.cli import command_catalog

        monkeypatch.setattr(
            command_catalog, "UI_EXPOSED_COMMANDS",
            frozenset(["job.stop", "decision.resolve", UNEXPOSED_CATALOG_COMMAND]))
        port, token = self._start_server()
        status, body = self._request(
            port, "POST", self._commands_path(),
            body=self._valid_body(
                command=UNEXPOSED_CATALOG_COMMAND, client_nonce="nonce-guard"),
            headers=self._auth_headers(token))
        assert status == 501, body
        # The MESSAGE is what tells the guard apart from the placeholder it
        # replaced: the deleted seam answered 501 for this request too, so a test
        # that pinned only the status would pass against either door.
        assert body["error"] == "command is exposed but not dispatched", body
        assert "command" not in body, body
        assert self._audit_records()[-1]["outcome"] == "not_implemented"

    def test_unexposed_catalog_command_is_400_on_field_command(self):
        """`job.list` is a real catalog id that the write door does not expose."""
<<<END TESTS_TO
