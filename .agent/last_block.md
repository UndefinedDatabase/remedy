── STEP R11/1 — F008 SSE event stream ────────────────────────
Goal:        Cap the streams one job may hold at once and pin T001's wire
             format. A per-job slot registry under a lock answers 429 beyond
             the cap and before the slot is taken, the slot is returned in a
             `finally` so a raising handler cannot leak capacity, and a framing
             golden pins the exact bytes a client parses. R10 PASSED with no
             finding against its work; this round records that verdict and
             registers R-0617 against the reviewer's own R10 block text.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record the R10 verdict and register R-0617 · C3 the slot
             registry and the 429 branch · C4 the tests · C5 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r11.md          (C0a, new)
             - .agent/last_block.md                 (C0b, rewrite)
             - .agent/plan.md                       (C1, rewrite)
             - .agent/live_review.md                (C2, append)
             - packages/orchestration/ui_server.py  (C3, three pairs)
             - tests/ui_server/test_sse_stream.py   (C4, append)
             - .agent/handoff.md                    (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r11.md, extracted by its marker lines — never retyped,
    rewrapped, reflowed or edited. A slice that looks wrong is APPLIED AS
    WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R11 is applied with
    its trailing newline INCLUDED and is the ENTIRE content of its file.
    LEDGER11 is applied as a newline plus its body, appended to
    `.agent/live_review.md` after exactly one blank line. TESTS11 is applied as
    its body appended to the END of `tests/ui_server/test_sse_stream.py`, whose
    committed blob already ends with exactly one newline. Every FROM/TO pair
    body carries its own trailing newline. Every file ends with exactly one
    newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5. `.agent/plan.md`
    is advanced at C1, the first substantive commit, ahead of the ledger append
    at C2 (§3 checklist item 23).
 4. PAIR SHAPES, from the reviewer's mechanical containment test, one reading
    printed per pair, none generalised from another:
      THREAD — TO contains FROM: false → REWRITE, FROM 1x before and 0x after.
      SLOT   — TO contains FROM: true  → APPEND, §4.9 ordered equality.
      CAP    — TO contains FROM: false → REWRITE, FROM 1x before and 0x after.
    Each FROM occurs EXACTLY ONCE in `packages/orchestration/ui_server.py` at
    `c9367141`, a count the reviewer took there. No FROM-zero count is ordered
    for the SLOT pair: it is unattainable by construction (R-0522).
 5. C3 carries all three `packages/orchestration/ui_server.py` pairs and no
    other path. C4 carries `tests/ui_server/test_sse_stream.py` and no other
    path. The two are separate commits so the source can be reverted alone for
    G11's red proof.
 6. TESTS11 is CODE, so its obligation is §4.9 ORDERED EQUALITY and never a
    per-line count (R-0531): the pre-commit blob is a byte-exact PREFIX of the
    post-commit file and the lines C4's diff ADDS are exactly TESTS11's lines in
    order.
 7. LEDGER11 carries TWO paragraphs, blank-line separated, applied together in
    C2: the R-0617 registration and the `Gate: R11` entry holding the R10
    verdict. R-0617 is the only id minted, so the next free id becomes R-0618.
 8. `git status --porcelain` is empty after every commit and at the handback.
    Any worktree G11 creates is REMOVED and PRUNED before the handback, so
    `git worktree list` then names the primary checkout alone.
 9. Two pytest processes never run at once. The COUNTING suites of G10 run in
    the PRIMARY checkout, because a fresh worktree has no `apps/ui/node_modules`
    and its pass counts are untrustworthy in both directions (R-0518). That
    clause binds G10 alone: G11's red proof is destructive and therefore runs
    ONLY in a disposable worktree (self_drive_protocol G5), and G12 reads base
    bytes through stdin and writes nothing anywhere. This constraint and those
    two gates are written to agree — R-0617 records what happened when the R10
    block stated the same rule as an unqualified universal.
10. NO TEST DRIVES THIS ROUTE OVER A REAL SOCKET, and no test leaves a slot
    taken: every test that acquires one clears `_SSE_SLOTS_PER_JOB` first, so
    the file's tests pass in any order. A hanging or order-dependent test is a
    defect of this round.
11. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature: T002 and T003 are unbuilt, so the branch is not closeable and
    no pull request is owed. It is pushed and left open.
12. The reviewer's own readings at `c9367141`, RE-DERIVED by the gates below
    rather than trusted: the combined state-reader suite exits 0 with
    `passed + skipped` equal to 427, and `tests/docs/` exits 0 at 295. Count by
    passed-plus-skipped, never by a bare passed count — data-dependent
    `pytest.skip(...)` calls in `test_brain_view_model.py` and
    `test_dashboard_contract.py` move the split at an unchanged tree.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r11.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r11.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256/bytes/lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R11. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER11 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST TWO units, in order, the two
     paragraphs of LEDGER11. NEGATIVE CONTROL: flip one byte of the remainder
     and report BOTH readings reject it, the unflipped accepted by both.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1 and
     C2: `^- R-\d+ — ` reads 188 then 189 — constraint 7, one id is minted —
     `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at both, and
     `^Gate: R\d+ — ` reads 10 then 11 with the eleven keys DISTINCT.
     `^- R-0617 — ` reads 0 then 1 and `^- R-0618 — ` is 0 at both. Report also
     that LEDGER11's `Gate:` header matches the header shape of the entries
     already in that file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be one
     less than the first and the R11 pair to occur exactly once (§3 item 26).
 G7  Pairs. For EACH of the three `packages/orchestration/ui_server.py` pairs
     report the FROM count in the blob at `c9367141` — each is 1 — and the FROM
     count in the C3 blob. For THREAD and CAP that count is 0 and the TO occurs
     1x each. For SLOT no FROM-zero count is ordered: report instead that the
     TO occurs exactly 1x in the C3 blob.
 G8  C3 content. Report that the `c9367141` blob of
     `packages/orchestration/ui_server.py` and its C3 blob differ, that
     `^import threading$` occurs exactly once line-anchored in the C3 blob and
     0 times at `c9367141`, and that the C3 blob contains `429` exactly once
     while `c9367141` contains it 0 times. Report C3's insertion and deletion
     counts from `git show --numstat`.
 G9  C4 ordered equality (§4.9, code append). Report that the C3 blob of
     `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of its C4 blob,
     that TESTS11 is an exact SUFFIX of the C4 blob, and that the lines C4's
     diff ADDS are exactly TESTS11's lines IN ORDER. Report the boolean of each.
 G10 The round gate, in the PRIMARY checkout, run SERIALLY, never two pytest
     processes at once. Report the exit code and `passed + skipped` of:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     Then, separately, `python3 -m pytest tests/docs/ -q -rf`, which exits 0 and
     sums to 295. Per constraint 12 report the SUM, never a bare passed count.
     Report the collected count of `tests/ui_server/test_sse_stream.py` alone at
     C4 and reconcile it against 427: the state-reader sum at C4 equals 427 plus
     the number of tests TESTS11 adds, and that arithmetic is REPORTED rather
     than predicted here. Then run that file ALONE with `-q -rf` and report its
     exit code: green both alone and inside the directory run above is
     constraint 10's order-independence reading.
 G11 RED PROOF, in a DISPOSABLE worktree at C4 and NEVER in the primary
     checkout. Restore `packages/orchestration/ui_server.py` alone to its
     `c9367141` blob — that file and no other, confirmed by the worktree's own
     `git status --porcelain` — and run
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` there. Report
     the exit code and the failed-plus-error count; order the COLOUR only: the
     exit is NON-ZERO and at least one failure or ERROR names the slot registry
     `_SSE_SLOTS_PER_JOB` or the 429 branch. A SETUP-TIME ERROR COUNTS as red
     here — the reverted module has no registry for `setup_method` to clear,
     which is precisely the coupling this proof exists to show — and the
     framing-golden tests PASS at the reverted blob BY DESIGN, a golden pinning
     behaviour that already existed, so no count of the red is ordered. Then
     restore that file to its C4 blob and report the same command EXITS 0.
     Remove and prune the worktree, then report `git worktree list`.
 G12 Lint. Report the rule-code MULTISET of
     `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_sse_stream.py`
     read at `c9367141` and at C4, and whether the two are EQUAL. Read the base
     bytes with `git show c9367141:<path>` piped through
     `ruff check --stdin-filename <path> -` so `per-file-ignores` still resolves
     and NOTHING is written to the primary checkout (§3 item 29). Compare
     multisets; do not demand exit 0 at either end. Report also a RED CONTROL
     through the SAME extractor, shown non-empty at non-zero exit, so the
     reading is known not to be vacuous; report the property, not that control's
     own contents.
 G13 Range. With BASE `c9367141`, `git diff --name-only BASE..C5` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C5 has exactly one parent. Report each commit's INSERTION count from
     `git show --numstat` for the commits BEFORE C5, all under 500, and compare
     them cell by cell against the `+/-` column of the handback's `## Commits`
     table, reporting agreement. Both columns come from `git diff --numstat`,
     never from a file's line counts before and after (§3 item 28). C5's own
     numbers belong to the round report (R-0149).
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `packages/orchestration/ui_server.py` at C3,
     `tests/ui_server/test_sse_stream.py` at C4 and `.agent/handoff.md` at C5.
     Every count is 0.
 G15 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs` — is
     `amend`, `rebase` or `cherry`; it is 0. Count by operation, never by
     substring; no total is asserted.
 G16 The branch is pushed and NO pull request exists. Report the real output of
     `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G17 Handback. `.agent/handoff.md` at C5 carries the sections
     docs/agents/handback_template.md mandates and an item-status table naming
     C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Report its line count;
     the cap is 100, this round having seven commits, and an overage carries a
     DECISION D15 stated-cause line naming the mandated content that caused it.
     Its `## Next` section states, in this order, that the next session's FIRST
     action is the `.agent/STOP` re-read (Phase 1 rule 1) and its SECOND the
     Open PR Gate (Phase 1 rule 2), which finds no open pull request and
     therefore continues on this branch at R12.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 50 % (F008 beansprucht · elf Urteile im Ledger ·
            T001 fertig: Leser, Route, Socket-Schreiber, 404 vor dem ersten
            Byte, Verbindungsdeckel mit 429 und der Rahmen-Golden · T002
            Last-Event-ID-Resume und der Trennungs-Hammer folgen · dann T003
            Client-Hook und Fallback) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R11
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
R11 closes T001. A per-job slot registry under a lock caps the streams one job
may hold at once, the route answers 429 beyond the cap and before the slot is
taken, the slot returns in a `finally` so a raising handler cannot leak
capacity, and a framing golden pins the exact bytes a client parses: field
order, the blank-line separator and the comment shape.

## Next Steps
1. R12 begins T002: Last-Event-ID resume, read from the request header and
   falling back to the query cursor, replaying exactly the missed span from the
   ledger — which IS the buffer, so there is no in-memory ring to lose.
2. R13 adds T002's forced-disconnect hammer: kill the connection mid-stream N
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
  R-0611, R-0613, R-0614, R-0615, R-0616 and R-0617 stay routed to a paydown
  branch, together with promoting the fix clauses of R-0387 and R-0573 into the
  §3 checklist.
<<<END PLANF008R11

<<<SLICE LEDGER11
- R-0617 — Low — A BLOCK STATED A SCOPE RULE AS AN UNQUALIFIED UNIVERSAL AND ITS OWN NEXT GATE BROKE IT, SO NO WORKER COULD OBEY BOTH CLAUSES. Constraint 9 of the F008 R10 block, saved at `b96dec03`, reads "Two pytest processes never run at once, and every suite runs in the PRIMARY checkout", while G11 of the SAME block orders a pytest run inside a disposable worktree and "NEVER in the primary checkout". The two are unsatisfiable together, and the R10 worker was right to follow the specific gate, record the objection in its handback and change nothing. The rule constraint 9 was reaching for is real and narrow — R-0518, that a fresh worktree has no `apps/ui/node_modules` so its pass COUNTS are untrustworthy in both directions — and it binds the COUNTING suites alone; a destructive red proof has no count to distrust and self_drive_protocol G5 requires that it be isolated. THE COUNTER-MEASURE ALREADY EXISTS ON DISK and was not applied: §3 checklist item 21 carries exactly this carve-out, stating that such a clause "reaches SUITE commands, which need installed dependencies, and never a read-only baseline reading". Its home is item 21, whose subject is a BASELINE gate resolving its own paths, so a reviewer writing a primary-checkout constraint does not read it there and did not. THE FIX, routed to a paydown branch with the other reviewer-text findings: lift that carve-out out of item 21 into its own item, phrased from the writer's side — a clause binding commands to the primary checkout NAMES the gates it binds, and a block carrying a worktree gate says so in the same sentence. The R11 block's constraint 9 is that phrasing, so this finding's counter-measure is demonstrated in the block that registers it even though the checklist edit itself is deferred.

Gate: R11 — the R10 entry. R10 PASSED with NO finding against its work, and R-0617 above is against the reviewer's own block text rather than the round. R10 wired T001's reader to a route: `GET /api/jobs/<jid>/events/stream` as a six-part branch in `_RemedyHandler.do_GET`, the `drain_sse_frames` writer that ends the loop when the peer goes away, and 404 answered before one byte of stream. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `c9367141` rather than reading the handback's numbers back. Transport EQUAL three ways — the scratch block, `.agent/authored/f008-r10.md` at `b96dec03` and `.agent/last_block.md` at `0743410b` — at sha256 b8446596b9feebd462c6e3705a3e4436a9bf892284285ff7ed287150f7350590 over 27169 bytes and 489 lines. ELEVEN SLICES by the reviewer's own ordered extraction out of the committed C0a file, newline-included, every digest matching: PLANF008R10 f2003a51, LEDGER10 83a82ef5, IMPORTFROM 786abd4b, IMPORTTO 140061a7, DRAINFROM 3562a4b8, DRAINTO 5fb4b28e, ROUTEFROM 713a8a23, ROUTETO 4073a873, METHODFROM 7675709e, METHODTO 4a3883f2 and TESTS10 5c5ddc27. THE PLAN LANDED FIRST at `1613ae7e`, byte-equal to PLANF008R10 at 42 lines under the 50-line cap, which is §3 checklist item 23 met rather than claimed. THE LEDGER APPEND at `42df4347` is a byte-exact prefix plus a 2532-byte remainder equal to a newline plus LEDGER10, agreed by an INDEPENDENT blank-line split into 202 units whose LAST equals LEDGER10's paragraph, with a one-byte flip REJECTED by both readings and the unflipped value ACCEPTED by both; the registered set held at 188 with zero `Done:` and zero `Landed:` lines, `Gate: R` going 9 to 10 over ten DISTINCT keys, so no id was minted, exactly as ordered. THE SOURCE COMMIT IS PROVED CONSTRUCTIVELY, not merely counted: the reviewer applied the four FROM/TO slices to the `a063be56` blob itself and the result is BYTE-EQUAL to the C3 blob at `bd5ca5d2`, each FROM having occurred exactly once there. The test append at `5f763ba4` is a byte-exact prefix, TESTS10 an exact suffix, and the 154 lines that diff ADDS are exactly TESTS10's 154 lines IN ORDER. SEVEN single-parent commits whose insertions read 489, 428, 15, 2, 65 and 154 before the handback commit, every one under the 500-line cap and agreeing cell by cell with the handback's `## Commits` column, which is read from `git diff --numstat` on both sides. ZERO marker lines in any of the five targets, a reflog whose operations over this round's own commits are `commit` seven times with `amend`, `rebase` and `cherry` at 0 each, an 85-line handback under its 100-line cap naming C0a through C5 once each, the tree clean with the primary checkout the only worktree, the branch pushed to `c9367141` and `gh pr list` returning an empty list. THE RUNS ARE THE REVIEWER'S OWN: the state readers exit 0 at 427 passed plus 0 skipped, `tests/docs/` exits 0 at 295 plus 0, and the SSE file collects 27 — so the 13 tests TESTS10 adds reconcile 414 to 427 exactly. THE RED PROOF IS REAL AND THE REVIEWER RE-RAN IT in its own disposable worktree, never in the primary checkout: with `packages/orchestration/ui_server.py` alone reverted to its `a063be56` blob the file EXITS 1 at 11 failed and 16 passed, the failures naming `drain_sse_frames` and `_send_sse_stream`, and restored to its C4 blob the same command EXITS 0 at 27. Sixteen tests survive the revert because two of TESTS10's own assert that pre-existing behaviour is UNCHANGED — the token gate and the cursor endpoint beside the stream — which is why the block ordered the colour and never a count. RUFF IS EQUAL ACROSS THE CHANGE, empty multiset at base and at head, behind a control shown non-empty at non-zero exit through the same extractor.
<<<END LEDGER11

<<<SLICE THREADFROM
import sys
import time
<<<END THREADFROM

<<<SLICE THREADTO
import sys
import threading
import time
<<<END THREADTO

<<<SLICE SLOTFROM
def _get_frontend_dist() -> Path | None:
<<<END SLOTFROM

<<<SLICE SLOTTO
#: Live SSE streams one job may hold at once. A cockpit opens one per tab, so
#: the cap is what stops a reconnect storm from pinning a thread per attempt.
SSE_MAX_STREAMS_PER_JOB = 4

_SSE_SLOT_LOCK = threading.Lock()
_SSE_SLOTS_PER_JOB: dict[str, int] = {}


def acquire_sse_slot(job_id: str, limit: int = SSE_MAX_STREAMS_PER_JOB) -> bool:
    """Take one of a job's stream slots, or refuse once the cap is reached.

    The server is threaded, so the count is read and written under one lock:
    two tabs opening at the same moment must not both see the last free slot.
    """
    with _SSE_SLOT_LOCK:
        live = _SSE_SLOTS_PER_JOB.get(job_id, 0)
        if live >= limit:
            return False
        _SSE_SLOTS_PER_JOB[job_id] = live + 1
        return True


def release_sse_slot(job_id: str) -> None:
    """Give a job's stream slot back, forgetting the job once it reaches zero.

    A stream that ended is capacity again, so the caller releases in a
    `finally`: a handler that raised would otherwise cost that job a slot for
    the lifetime of the process.
    """
    with _SSE_SLOT_LOCK:
        live = _SSE_SLOTS_PER_JOB.get(job_id, 0) - 1
        if live > 0:
            _SSE_SLOTS_PER_JOB[job_id] = live
        else:
            _SSE_SLOTS_PER_JOB.pop(job_id, None)


def _get_frontend_dist() -> Path | None:
<<<END SLOTTO

<<<SLICE CAPFROM
        # /api/jobs/<job_id>/events/stream — the SSE transport of events-since
        if (len(parts) == 6 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "events" and parts[5] == "stream"):
            job, err = _load_job(parts[3])
            if err:
                # 404 before one byte of stream: once the event-stream headers
                # are out the status line is spent and cannot say "not found".
                self._send_json(*err)
                return
            self._send_sse_stream(job, (qs.get("cursor") or ["0"])[0])
            return
<<<END CAPFROM

<<<SLICE CAPTO
        # /api/jobs/<job_id>/events/stream — the SSE transport of events-since
        if (len(parts) == 6 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "events" and parts[5] == "stream"):
            job, err = _load_job(parts[3])
            if err:
                # 404 before one byte of stream: once the event-stream headers
                # are out the status line is spent and cannot say "not found".
                self._send_json(*err)
                return
            if not acquire_sse_slot(str(job.id)):
                # 429 for the same reason and in the same window: a refused
                # stream must not consume the capacity it was refused.
                self._send_json(*_safe_error(429, "too many streams for this job"))
                return
            try:
                self._send_sse_stream(job, (qs.get("cursor") or ["0"])[0])
            finally:
                release_sse_slot(str(job.id))
            return
<<<END CAPTO

<<<SLICE TESTS11


#: T001's framing golden: the exact bytes a client parses for a two-event
#: ledger that then goes idle past the heartbeat interval. Field order, the
#: blank-line separator and the comment shape are all pinned here, so any
#: change to the wire format has to be a deliberate edit of this constant.
GOLDEN_STREAM = (
    b'id: 0\ndata: {"seq": 0, "event": "e0", "timestamp": "2026-08-21T00:00:00Z", "outcome": "ok"}\n\n'
    b'id: 1\ndata: {"seq": 1, "event": "e1", "timestamp": "2026-08-21T00:00:01Z", "outcome": "ok"}\n\n'
    b": heartbeat\n\n"
)


class TestFramingGolden:
    def test_the_wire_bytes_match_the_golden(self):
        # 17 passes: one drains both events, fifteen sleep out the interval,
        # the last emits the single heartbeat that idling earns.
        joined = b"".join(_run(lambda: _events(2), 0, 17, _Clock()))
        assert joined == GOLDEN_STREAM

    def test_the_golden_is_what_the_frame_builders_produce(self):
        # Not a transcription of the constant above: rebuilt from the writers,
        # so a golden edited without a code change fails here.
        rebuilt = b"".join([
            mod.sse_event_frame(seq, mod._safe_event_summary(seq, _events(2)[seq]))
            for seq in (0, 1)
        ]) + mod.sse_heartbeat_frame()
        assert rebuilt == GOLDEN_STREAM


class TestStreamSlots:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_a_job_holds_slots_up_to_the_cap(self):
        taken = [mod.acquire_sse_slot("j", limit=2) for _ in range(3)]
        assert taken == [True, True, False]

    def test_a_released_slot_can_be_taken_again(self):
        assert mod.acquire_sse_slot("j", limit=1)
        assert not mod.acquire_sse_slot("j", limit=1)
        mod.release_sse_slot("j")
        assert mod.acquire_sse_slot("j", limit=1)

    def test_the_registry_forgets_a_job_at_zero(self):
        mod.acquire_sse_slot("j", limit=1)
        mod.release_sse_slot("j")
        # Not a lingering 0: an idle cockpit must not grow the registry.
        assert "j" not in mod._SSE_SLOTS_PER_JOB

    def test_an_extra_release_never_goes_negative(self):
        mod.release_sse_slot("j")
        mod.release_sse_slot("j")
        assert mod._SSE_SLOTS_PER_JOB.get("j", 0) == 0
        assert mod.acquire_sse_slot("j", limit=1)

    def test_two_jobs_do_not_share_one_cap(self):
        assert mod.acquire_sse_slot("a", limit=1)
        assert mod.acquire_sse_slot("b", limit=1)
        assert not mod.acquire_sse_slot("a", limit=1)

    def test_the_default_cap_is_four(self):
        assert mod.SSE_MAX_STREAMS_PER_JOB == 4


class TestStreamCapRoute:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_the_stream_is_refused_with_429_beyond_the_cap(self, monkeypatch):
        for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
            assert mod.acquire_sse_slot(_Job.id)
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 429

    def test_a_refused_stream_does_not_consume_a_slot(self, monkeypatch):
        for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
            mod.acquire_sse_slot(_Job.id)
        _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        # Still exactly at the cap: the refusal took nothing.
        assert mod._SSE_SLOTS_PER_JOB[_Job.id] == mod.SSE_MAX_STREAMS_PER_JOB

    def test_a_served_stream_releases_its_slot(self, monkeypatch):
        _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert _Job.id not in mod._SSE_SLOTS_PER_JOB

    def test_a_raising_stream_still_releases_its_slot(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_job", lambda jid: (_Job(), None))

        def boom(job, cursor):
            raise RuntimeError("socket died")

        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.server_token = "tok"
        handler.target_job_id = ""
        handler.path = "/api/jobs/J/events/stream?token=tok"
        handler._send_json = lambda code, data: None
        handler._send_sse_stream = boom
        raised = False
        try:
            handler.do_GET()
        except RuntimeError:
            raised = True
        assert raised
        # The `finally` is the whole point: a crash must not leak capacity.
        assert _Job.id not in mod._SSE_SLOTS_PER_JOB

    def test_an_unknown_job_never_takes_a_slot(self, monkeypatch):
        _dispatch(
            monkeypatch, "/api/jobs/nope/events/stream?token=tok", None,
            (404, {"error": "job not found"}))
        assert mod._SSE_SLOTS_PER_JOB == {}
<<<END TESTS11
