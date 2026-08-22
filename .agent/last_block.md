── STEP T003 (round two of DECISION F009 D19 — the dispatch effects) — F009 ──
Goal:        Pin what an accepted `job.stop` actually DID, not merely what the
             door answered. A NEW file asserts DECISION F009 D18's three writes
             from the outside: the stop request the dispatch published and the
             `request_id` that ties it to the body on the wire, the nonce record
             holding exactly what the client received, a retry audited
             `replayed`, and an effect that RAISES answered 500 and audited
             `rejected_effect` with no exception text on the wire. The round is
             purely ADDITIVE: it edits no existing test and no production file.
             It also records the R19 verdict and registers finding R-0639.

Fortschritt: ~82 % (T001 gebaut · T002 gebaut · T003 begonnen: der
             `job.stop`-Dispatch steht und ist wirkungsgeprüft; offen bleiben
             `decision.resolve`, das SSE-Event, der Import-Guard und die
             405-Routenprobe) — Schätzung

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 the R19 verdict
             and finding R-0639 · C3 the new effects file · C4 handback.

Change:      Exactly these paths, and nothing else:
             `.agent/authored/f009-r20.md` (NEW, C0a) · `.agent/last_block.md`
             (C0b) · `.agent/plan.md` (C1) · `.agent/live_review.md` (C2) ·
             `tests/ui_server/test_command_dispatch.py` (NEW, C3) ·
             `.agent/handoff.md` (C4). NOTHING under `packages/`, `apps/` or
             `docs/` is touched, and `.agent/decisions.md` is NOT touched: this
             round rules nothing and amends nothing.

Constraints:
 1. Apply every slice BYTE FOR BYTE. Never retype, rewrap, reflow, reindent or
    whitespace-adjust one. If a slice looks wrong, STOP and say so in the
    handback rather than fixing it.
 2. C2 is an APPEND — LEDGER20 to `.agent/live_review.md`. That target ends in
    exactly ONE newline at the round base, which the reviewer measured on the
    bytes, so the append is one newline followed by the slice. LEDGER20 carries
    TWO paragraphs separated by one blank line.
 3. C3 CREATES `tests/ui_server/test_command_dispatch.py` from slice
    DISPATCHTESTS and writes NOTHING else. The file must not exist before C3;
    verify that and report it. There is no FROM/TO pair in this round, so no
    replacement obligation arises and none is ordered — and therefore no
    append-shaped pair either, which is the case finding R-0639 rules on.
 4. Commit order is C0a, C0b, C1, C2, C3, C4 and is not negotiable.
 5. This round mints ONE id, R-0639, in LEDGER20, and resolves none. It does NOT
    write a `Done:` line for R-0636: R-0636 was PAID at R19 and its resolution
    is the reviewer's to certify, which happens in a later round's record.
 6. The `Fortschritt:` line above is relayed deliberately (finding R-0418); the
    handback's state block repeats it VERBATIM across all three of its lines.
 7. SIZE, measured at emission as DECISION F085 D6 requires both numbers to be:
    329 lines TOTAL against D6's 490 cap, 134 of them PROSE against D5's 400.
    Re-measure both from the committed C0a blob; a disagreement is a finding.

Done when — run every gate and record its REAL exit code and output:
 G1  Before C0a and again before C4: `.agent/STOP` is ABSENT,
     `git rev-parse --abbrev-ref HEAD` prints
     `feature/f009-single-write-channel`, and `git status --porcelain` prints 0
     lines after each of C0a through C3. Report the round base SHA you read at
     step 0.
 G2  TRANSPORT: `.agent/authored/f009-r20.md` at C0a and `.agent/last_block.md`
     at C0b are byte-equal to each other and to the block you received; report
     sha256, bytes and lines for both. C0b is written FROM the committed C0a
     blob, never from the scratch copy again.
 G3  SLICES: extract every slice from the COMMITTED C0a blob by its `<<<SLICE `
     and `<<<END ` marker lines with a script and apply them programmatically.
     Report each slice's sha256, bytes and lines plus the aggregate count your
     script printed. State no slice count you did not count. Re-measure
     constraint 7's two numbers from that same blob and report both.
 G4  `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R20 — report `cmp` exit and
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
     `Gate: R` key over that many DISTINCT keys; the `Gate: R20` key; a leading
     `- R-0639` entry; and a leading `- R-0640` entry, which must read 0 at both
     because this round mints one id and it is not that one. Report each pair of
     readings, the max id, and the open count by DECISION F009 D10's rule at C2.
     Report what you measure, not what this sentence expects.
 G7  `.agent/decisions.md` is BYTE-IDENTICAL at the round base and at C4 — the
     same sha256 — because this round rules nothing. Report both digests.
 G8  NEW FILE: `tests/ui_server/test_command_dispatch.py` does not exist at the
     round base (`git cat-file -e` fails; report that) and at C3 is BYTE-EQUAL
     to slice DISPATCHTESTS. Report `cmp` exit 0 and both sha256, with a
     negative control against another file that exits non-zero.
 G9  SUITES, run SERIALLY in the PRIMARY checkout, never two pytest processes at
     once and never in a worktree. Report each command's REAL exit code and the
     count IT printed — predict no number:
       `python3 -m ruff check tests/ui_server/test_command_dispatch.py`
       `python3 -m pytest tests/ui_server/test_command_dispatch.py -q -rf`
       `python3 -m pytest tests/ui_server/ -q -rf`
       `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
       `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py
        tests/regression/test_resource_safety.py
        tests/orchestration/test_integrity_gate.py -q -rf`
     The reviewer ran ruff and the four suites that exist at the round base
     before ordering them: each exits 0, so each can fail honestly (R-0364).
     The new file's own 4 tests the reviewer ran in a worktree, where they
     passed at 4 and, with the door alone reverted to its pre-R19 bytes, failed
     at 4 — so they reach the dispatch rather than passing beside it.
 G10 RANGE: the range from the round base to C3 lists EXACTLY the declared paths
     other than `.agent/handoff.md`, the set difference EMPTY in both
     directions, and 0 paths beginning `packages/`, `apps/` or `docs/`, which is
     this round's no-production-code constraint as a measurement. Each commit
     has ONE parent; `git show --numstat` and `git diff --numstat` AGREE on
     every cell — invoke `git show` WITHOUT a `--` before the SHA, which turns
     it into a pathspec and prints nothing; every cell equals the `+/-` column
     of the handback's `## Commits` table (checklist item 28), compared cell by
     cell. Report each pre-handback commit's insertions against the 500 cap of
     AGENTS.md DECISION F104 D1; the handback commit's own numbers belong in the
     round report (item 14). Leading `<<<SLICE ` and `<<<END ` read 0 LINES in
     every file a slice lands in, a set the reviewer counted at two:
     `.agent/plan.md` and `.agent/live_review.md` — plus the new file, which is
     a third target and must also read 0. `git ls-files .remedy-wt` reads 0.
     Classify THIS ROUND's reflog rows by the operation before the first `:` and
     report `amend`, `rebase` and `cherry` each 0; assert no total over the
     whole reflog (R-0601). Create NO worktree, so `git worktree list` prints 1.
 G11 The handback carries every mandated section of
     docs/agents/handback_template.md, an item-status row for each of C0a, C0b,
     C1, C2, C3 and C4, the round base SHA, one line per gate with the
     transcripts in the round report and not in the file (R-0582), and this
     block's `Fortschritt:` line VERBATIM. Report its `wc -l` against the 100
     lines a bundle of more than five commits allows.

Handback:    completion report + rewrite `.agent/handoff.md`. Push after C4.
             Create NO pull request: F009 opens one at its own closure.
─────────────────────────────────────────────────────────────────────────────

<<<SLICE PLANF009R20
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
R20 is round two of DECISION F009 D19 and is purely additive: a new
`tests/ui_server/test_command_dispatch.py` asserts DECISION F009 D18's three
writes from the outside — the published stop request, the nonce record, a retry
audited `replayed` — and the `rejected_effect` path that R19 shipped with no
test reaching it. It also records the R19 verdict and registers R-0639.

## Next Steps
1. `decision.resolve` dispatches to `answer_task_decision` followed by
   `save_job` per DECISION F009 D5, and the 501 seam is gone entirely. That
   round re-examines D18's clause three against a non-idempotent effect, as D18
   requires of it, and migrates the two pins that still expect 501.
2. Then the `command.accepted` SSE event on the F008 stream.
3. Then the queue-only import guard, the per-command side-effect assertions and
   the route-walking 405 test; then the integration gate and closure.

## Risks
- DECISION F009 D18's clause three ruled soft failure for BOTH later writes on
  the strength of `request_stop` being idempotent. `answer_task_decision`
  followed by `save_job` is not obviously so, and D18 already names that as the
  next round's obligation rather than an inheritance.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
<<<END PLANF009R20

<<<SLICE LEDGER20
Gate: R20 — the R19 entry. R19 PASSED. Every gate was RE-EXECUTED by the reviewer off disk rather than read back out of the handback, and every value reproduced. TRANSPORT HELD IN ITS STRONGEST FORM: `.agent/authored/f009-r19.md` at `ed036f14`, `.agent/last_block.md` at `de716e02` and the bytes the reviewer EMITTED, still on disk, are all sha256 36b24983aebc1f9e4f92569a7f59c6a1a9015dcf55e51564cfb9d3b627836595 over 36697 bytes and 488 lines, compared against the emitted original rather than against a recorded digest. The reviewer's own ordered extraction out of the committed C0a blob gives 31 slices aggregating 24295 bytes over 253 lines, the same aggregate the handback printed. `.agent/plan.md` at `909d37ee` is BYTE-EQUAL to PLANF009R20's predecessor PLANF009R19 at 44 lines against the 50-line cap, its negative control unequal, `^## Goal$` and `^## Next Steps$` reading 1 each. THE TWO APPENDS HOLD UNDER THE REVIEWER'S OWN TWO READERS EACH: at `768eba0f` the round-base blob is a byte-exact prefix of `.agent/live_review.md` and the remainder is exactly a newline plus LEDGER19, sha256 `6708ca1d…` over 6590 bytes and 4 lines, the file going 486398 to 492988 bytes and 1096 to 1100 lines, N counted at 2; at `d2388da2` the C2 blob is a byte-exact prefix of `.agent/decisions.md` and the remainder is exactly a newline plus DECISION20, sha256 `b94849e6…` over 3316 bytes and 10 lines, the file going 458162 to 461478 bytes and 6857 to 6867 lines, N counted at 5. Both bases ended in exactly ONE newline, measured on the bytes. For BOTH appends, flipping byte 0 of the FIRST appended paragraph at equal length makes BOTH readers REJECT while both ACCEPT the true file. THE FOURTEEN PAIRS ARE PROVED AS PAIRS, whole-line and indent-agnostic and the two readings agreeing at every count: before C4 every FROM read 1 and every TO 0; after C4 every TO reads 1 and thirteen FROMs read 0, with U1CONST alone reading 1 because its own TO re-quotes it — the containment reading `TO contains FROM` is TRUE for U1CONST and FALSE for the other thirteen, exactly as the block predicted. THE THREE ORDERED REPLACEMENTS ARE THE REVIEWER'S OWN COUNT: after C4 `[0] == 501`, `status == 501` and the quoted `not_implemented` each read 0 in `tests/ui_server/test_command_channel.py` while the quoted `replayed` reads 1, and `packages/orchestration/command_audit.py` still reads 1 for the quoted `not_implemented` and was not touched. THE CODE IS EXACTLY THE AUTHORED SLICES AND NOTHING MORE, which is the reading that matters for a round touching `packages/`: the reviewer read the real diff of `5d3d1e32` and the door is the three authored pairs and no fourth change, the pin file the eleven authored pairs and the three replacements and nothing else. THE SETS HELD line-anchored at line start, round base and C2: entries 203 and 204 with every id DISTINCT at each, leading `Done:` ids 3 at both, leading `Landed: ` 0 at both, `Gate: R` keys 18 and 19 over that many DISTINCT keys, the `Gate: R19` key 0 and 1, a leading `- R-0638` entry 0 and 1, a leading `- R-0639` entry 0 at both, max id R-0637 and R-0638, and 200 then 201 open by DECISION F009 D10's rule. Leading `## DECISION F009 D` numbers read 19 and 20 with every number DISTINCT, and the `## DECISION ` total 104 and 105. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout: ruff over the two changed paths EXITS 0, `tests/ui_server/` EXITS 0 at 418 passed, the canary EXITS 0 at 42 passed, the four-path state-reader group EXITS 0 at 507 passed and `tests/orchestration/test_command_audit.py` EXITS 0 at 17 passed — the same five results the handback reported and not one of them predicted by it. THE RED CONTROL IS THE REVIEWER'S OWN, run in a disposable worktree at `5d3d1e32` with the door alone reverted to its pre-round bytes: the mutation is REAL, `git diff HEAD --numstat` reading 13/76 over `packages/orchestration/ui_server.py` and the file byte-equal to the base door, and under it `tests/ui_server/test_command_channel.py` EXITS 1 with 18 shipped tests failing, among them the acceptance, the audit, the vocabulary walk and the replay. The pins this round migrated therefore genuinely REACH the dispatch rather than passing beside it. THE RANGE HELD: seven single-parent commits, the range to C4 listing exactly the seven declared paths with the set difference EMPTY in both directions and 0 paths beginning `apps/` or `docs/`; `git show --numstat` and `git diff --numstat` agree on every cell and every cell equals the `+/-` column of the handback's own tables, at 488/0, 426/138, 16/20, 4/0, 10/0 and 76/13 with 46/38; pre-handback insertions 488, 426, 16, 4, 10 and 122, every one under the 500 cap — the C0a reading of 488 being exactly the margin DECISION F085 D6 exists to preserve; zero leading `<<<SLICE ` and `<<<END ` LINES in all five slice targets; `git ls-files .remedy-wt` 0; this round's seven reflog rows all classify as `commit` with `amend`, `rebase` and `cherry` each 0 and no total asserted over the whole reflog; one worktree and a clean tree at the verdict, and `git ls-remote` shows the branch pushed to `7ac8d98c`, the same SHA the reviewer read. The handback carries every mandated section of docs/agents/handback_template.md in order, an item-status row for each of C0a through C5, the round base SHA, one line per gate, and the block's `Fortschritt:` line verbatim across all three of its lines, at 98 lines against the 100 a bundle of more than five commits allows. ONE DEVIATION WAS DECLARED AND IT IS CORRECT: G8's after-clause is unmeetable for U1CONST, the worker reported it and repaired nothing, and the defect is the REVIEWER'S GATE rather than the work — it is registered below as R-0639.

- R-0639 — Low — A REVIEWER GATE ORDERED TWO CLAUSES THAT CANNOT BOTH HOLD FOR ONE OF THE FOURTEEN PAIRS IT MEASURES, AND THE WORKER HAD TO SPEND ITS ONLY DEVIATION SAYING SO. The R19 block's G8, committed at `ed036f14`, orders that "each FROM reads 1 before and 0 after" and, in the same breath, that the containment reading `TO contains FROM` be reported — naming U1CONST as the one pair for which the reviewer measured it TRUE. The two sentences are individually correct and were never read against each other. A FROM that its own TO re-quotes verbatim, which is what an APPEND-shaped pair is, NECESSARILY still reads 1 after the pair is applied; U1CONST_TO restates the three lines of U1CONST_FROM and adds three constant blocks after them, so the gate simultaneously predicted the containment and forbade its consequence. MEASURED by the reviewer at `5d3d1e32`, whole-line and indent-agnostic with the two readings agreeing at every count: U1CONST reads FROM 1 and TO 1 after C4, the other thirteen read FROM 0 and TO 1. The worker reported the contradiction, changed no slice and no measurement, and named the assumption it worked under — that the after-clause's intent is that no pair leaves an unconverted site. That reading is correct and it holds for all fourteen. WHY LOW: nothing false reached disk, the round is otherwise clean, and the gate still discriminated — the containment reading is precisely what proves U1CONST's 1/1 is the append it was authored as rather than a failed application, so the evidence the gate produced was sufficient even though one of its clauses was not satisfiable. THE CLASS IS R-0636's EXACTLY — a block's own INTERNAL consistency, one clause of a spec against another clause of the same spec, which checklist item 13 covers for a block's ORDERING and item 16 for a count against a list it NAMES, while neither reaches two gate clauses about the same measurement. This is that class's second instance in three rounds, and that recurrence is what earns it an id rather than a shrug. FIX, RULED HERE AND BINDING ON EVERY LATER BLOCK OF THIS FEATURE: a pair whose TO contains its FROM is an APPEND-SHAPED pair, and its after-clause is "the FROM still reads 1 and the TO reads 1", never "the FROM reads 0". A block CLASSIFIES each of its pairs before the gate that measures them, and the containment reading decides the class — not the reviewer's memory of how the pair was written.
<<<END LEDGER20

<<<SLICE DISPATCHTESTS
"""
Domain tests: ui_server/test_command_dispatch.py

Effect tests for F009 T003 — what an ACCEPTED command actually DID. Its sibling
`test_command_channel.py` pins what the door ANSWERS; this file pins the three
writes DECISION F009 D18 orders behind that answer: the effect, the `accepted`
audit line and the nonce publication. Remedy deliberately keeps the two files
apart — a status can be right while the effect never ran, and only a test that
reads the job's control directory can tell those two cases apart.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.core.models import Job, Task

# Pinned as a literal for the reason its sibling gives: a test that imports the
# constant it checks cannot catch a rename of the header the browser must send.
CSRF_HEADER = "X-Remedy-CSRF"


def _make_job() -> Job:
    return Job(
        name="test-command-dispatch-job",
        user_prompt="Test prompt for the command dispatch effects",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


class TestJobStopDispatchEffects:
    """Integration tests that start a real server and then read what it wrote."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        self.job = _make_job()
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path
        self.control = tmp_path / "control"

    def _start_server(self):
        import secrets

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = secrets.token_urlsafe(16)

        def run():
            try:
                start_ui_server(self.job_id, host="127.0.0.1", port=0, token=token,
                                open_browser=False, info_file=info_file)
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()
        for _ in range(50):
            if Path(info_file).exists():
                return json.loads(Path(info_file).read_text())["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def _post(self, port, token, nonce, **overrides):
        """One fully credentialed `job.stop` submission, valid unless overridden."""
        payload = {"command": "job.stop", "client_nonce": nonce}
        payload.update(overrides)
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("POST", f"/api/jobs/{self.job_id}/commands",
                         body=json.dumps(payload),
                         headers={"Authorization": f"Bearer {token}",
                                  CSRF_HEADER: token,
                                  "Content-Type": "application/json"})
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def _audit_outcomes(self):
        from packages.orchestration.command_audit import AUDIT_FILENAME
        path = self.control / "jobs" / self.job_id / AUDIT_FILENAME
        return [json.loads(line)["outcome"] for line in path.read_bytes().splitlines()]

    def test_the_dispatch_publishes_the_stop_request_the_body_names(self):
        """D5's effect really ran: the request_id on the wire is the one on disk."""
        from packages.orchestration import safe_points

        port, token = self._start_server()
        status, body = self._post(port, token, "nonce-effect",
                                  args={"reason": "operator asked"})

        assert status == 200, body
        path = safe_points.stop_request_path(self.job_id, control_root_path=self.control)
        assert path.exists(), "the door answered accepted but requested no stop"
        signal = json.loads(path.read_bytes())
        assert signal["request_id"] == body["request_id"], (signal, body)
        assert signal["source"] == "ui", signal
        assert signal["reason"] == "operator asked", signal

    def test_the_nonce_record_holds_the_body_the_client_received(self):
        """D8's replay is byte-exact only if the store holds what was sent."""
        from packages.orchestration.command_nonce import lookup_nonce_result

        port, token = self._start_server()
        status, body = self._post(port, token, "nonce-published")

        assert status == 200, body
        assert lookup_nonce_result(
            self.job_id, "nonce-published",
            control_root_path=self.control) == {"status": 200, "body": body}

    def test_a_retry_of_the_same_nonce_is_audited_replayed(self):
        """Finding R-0636: a replay REPEATS an acceptance rather than being one."""
        port, token = self._start_server()
        first = self._post(port, token, "nonce-twice")
        second = self._post(port, token, "nonce-twice")

        assert first == second
        assert self._audit_outcomes() == ["accepted", "replayed"]

    def test_an_effect_that_raises_is_500_and_audited_rejected_effect(self, monkeypatch):
        """DECISION F009 D18 clause four, and the only test that reaches the token."""
        from packages.orchestration import safe_points

        def explode(*_args, **_kwargs):
            raise safe_points.StopControlError("containment could not be guaranteed")

        port, token = self._start_server()
        monkeypatch.setattr(safe_points, "request_stop", explode)
        status, body = self._post(port, token, "nonce-raises")

        assert status == 500, body
        assert "containment" not in json.dumps(body), "the exception text reached the wire"
        assert self._audit_outcomes() == ["rejected_effect"]
<<<END DISPATCHTESTS
