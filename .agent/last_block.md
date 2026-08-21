── STEP R10/1 — F008 SSE event stream ────────────────────────
Goal:        Wire T001's stream reader to a route. `GET /api/jobs/<jid>/events/stream`
             becomes a six-part path branch in `_RemedyHandler.do_GET`, a socket
             writer drains the R8 generator into `wfile` and ends the loop when the
             peer goes away, and an unknown job answers 404 before one byte of
             stream. R9 PASSED with no finding against its work, so this round
             records that verdict and mints no finding id.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 record the R9 verdict · C3 the import, the writer and the route ·
             C4 the tests · C5 the handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r10.md          (C0a, new)
             - .agent/last_block.md                 (C0b, rewrite)
             - .agent/plan.md                       (C1, rewrite)
             - .agent/live_review.md                (C2, append)
             - packages/orchestration/ui_server.py  (C3, four pairs)
             - tests/ui_server/test_sse_stream.py   (C4, append)
             - .agent/handoff.md                    (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r10.md, extracted by its marker lines — never retyped,
    rewrapped, reflowed or edited. A slice that looks wrong is APPLIED AS
    WRITTEN and the objection goes in the handback.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines strictly
    between its `<<<SLICE X` and `<<<END X` markers. PLANF008R10 is applied with
    its trailing newline INCLUDED and is the ENTIRE content of its file.
    LEDGER10 is applied as a newline plus its body, appended to
    `.agent/live_review.md` after exactly one blank line. TESTS10 is applied as
    its body appended to the END of `tests/ui_server/test_sse_stream.py`, whose
    committed blob already ends with exactly one newline. Every FROM/TO pair
    body carries its own trailing newline. Every file ends with exactly one
    newline.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5. `.agent/plan.md`
    is advanced at C1, the first substantive commit, ahead of the ledger append
    at C2 (§3 checklist item 23).
 4. PAIR SHAPES, from the reviewer's mechanical containment test, one reading
    printed per pair, none generalised from another:
      IMPORT — TO contains FROM: false  → REWRITE, FROM 1x before and 0x after.
      DRAIN  — TO contains FROM: true   → APPEND, §4.9 ordered equality.
      ROUTE  — TO contains FROM: true   → APPEND, §4.9 ordered equality.
      METHOD — TO contains FROM: true   → APPEND, §4.9 ordered equality.
    Each FROM occurs EXACTLY ONCE in `packages/orchestration/ui_server.py` at
    `a063be56`, a count the reviewer took there. No FROM-zero count is ordered
    for the three APPEND pairs: it is unattainable by construction (R-0522).
 5. C3 carries all four `packages/orchestration/ui_server.py` pairs and no other
    path. C4 carries `tests/ui_server/test_sse_stream.py` and no other path. The
    two are separate commits so the source can be reverted alone for G11's red
    proof.
 6. TESTS10 is CODE, so its obligation is §4.9 ORDERED EQUALITY and never a
    per-line count (R-0531): the pre-commit blob is a byte-exact PREFIX of the
    post-commit file and the lines C4's diff ADDS are exactly TESTS10's lines in
    order.
 7. LEDGER10 carries ONE paragraph, the `Gate: R10` entry holding the R9
    verdict. NO finding id is minted this round, so the next free id stays
    R-0617.
 8. `git status --porcelain` is empty after every commit and at the handback.
    Any worktree G11 creates is REMOVED and PRUNED before the handback, so
    `git worktree list` then names the primary checkout alone.
 9. Two pytest processes never run at once, and every suite runs in the PRIMARY
    checkout — a fresh worktree has no `apps/ui/node_modules` and its pass
    counts are untrustworthy in both directions (R-0518).
10. NO TEST DRIVES THIS ROUTE OVER A REAL SOCKET. Every new test injects its
    clock and its socket, matching the file's existing idiom, so cadence and
    disconnect are asserted rather than waited out. A hanging test is a defect
    of this round, not a slow one.
11. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature: T002 and T003 are unbuilt, so the branch is not closeable and
    no pull request is owed. It is pushed and left open.
12. The reviewer's own readings at `a063be56`, RE-DERIVED by the gates below
    rather than trusted: the combined state-reader suite exits 0 with
    `passed + skipped` equal to 414, and `tests/docs/` exits 0 at 295. Count by
    passed-plus-skipped, never by a bare passed count — data-dependent
    `pytest.skip(...)` calls in `test_brain_view_model.py` and
    `test_dashboard_contract.py` move the split at an unchanged tree.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r10.md` at C0a and of
     `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r10.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256/bytes/lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R10. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER10 — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST unit the paragraph of LEDGER10.
     NEGATIVE CONTROL: flip one byte of the remainder and report BOTH readings
     reject it, the unflipped accepted by both.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1 and
     C2: `^- R-\d+ — ` reads 188 at BOTH — constraint 7, no id is minted —
     `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at both, and
     `^Gate: R\d+ — ` reads 9 then 10 with the ten keys DISTINCT. `^- R-0617 — `
     is 0 at both. Report also that LEDGER10's header line matches the header
     shape of the entries already in that file, as a pattern match over
     `^Gate: R(\d+) — the R(\d+) entry\.` requiring the second number to be one
     less than the first and the pair to occur exactly once (§3 item 26).
 G7  Pairs. For EACH of the four `packages/orchestration/ui_server.py` pairs
     report the FROM count in the blob at `a063be56` — each is 1 — and the FROM
     count in the C3 blob. For IMPORT that count is 0 and the TO occurs 1x. For
     DRAIN, ROUTE and METHOD no FROM-zero count is ordered: report instead that
     the TO occurs exactly 1x in the C3 blob.
 G8  C3 ordered equality. Report that the `a063be56` blob of
     `packages/orchestration/ui_server.py` and its C3 blob differ, and that
     `import time` occurs exactly once line-anchored in the C3 blob while it
     occurs 0 times at `a063be56`. Report C3's insertion and deletion counts
     from `git show --numstat`.
 G9  C4 ordered equality (§4.9, code append). Report that the C3 blob of
     `tests/ui_server/test_sse_stream.py` is a byte-exact PREFIX of its C4 blob,
     that TESTS10 is an exact SUFFIX of the C4 blob, and that the lines C4's
     diff ADDS are exactly TESTS10's lines IN ORDER. Report the boolean of each.
 G10 The round gate, in the PRIMARY checkout, run SERIALLY, never two pytest
     processes at once. Report the exit code and `passed + skipped` of:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     Then, separately, `python3 -m pytest tests/docs/ -q -rf`, which exits 0 and
     sums to 295. Per constraint 12 report the SUM, never a bare passed count.
     Report the collected count of `tests/ui_server/test_sse_stream.py` alone at
     C4 and reconcile it against 414: the state-reader sum at C4 equals 414 plus
     the number of tests TESTS10 adds, and that arithmetic is REPORTED rather
     than predicted here.
 G11 RED PROOF, in a DISPOSABLE worktree at C4 and NEVER in the primary
     checkout. Restore `packages/orchestration/ui_server.py` alone to its
     `a063be56` blob — that file and no other — and run
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` there. Report
     the exit code and the failed count; order the COLOUR only: it must be
     NON-ZERO exit with at least one failure naming the new route or writer.
     Then restore that file to its C4 blob and report the same command EXITS 0.
     Remove and prune the worktree, then report `git worktree list`.
 G12 Lint. Report the rule-code MULTISET of
     `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_sse_stream.py`
     read at `a063be56` and at C4, and whether the two are EQUAL. Read the base
     bytes with `git show a063be56:<path>` piped through
     `ruff check --stdin-filename <path> -` so `per-file-ignores` still resolves
     and NOTHING is written to the primary checkout (§3 item 29). Compare
     multisets; do not demand exit 0 at either end.
 G13 Range. With BASE `a063be56`, `git diff --name-only BASE..C5` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C5 has exactly one parent. Report each commit's INSERTION count from
     `git show --numstat` for the commits BEFORE C5, all under 500, and compare
     them cell by cell against the `+/-` column of the handback's `## Commits`
     table, reporting agreement. C5's own numbers belong to the round report
     (R-0149).
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
     therefore continues on this branch at R11.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 40 % (F008 beansprucht · zehn Urteile im Ledger ·
            T001-Leser gebaut und geprüft · Route, Socket-Schreiber und
            404-vor-dem-ersten-Byte in dieser Runde · Verbindungsdeckel mit 429
            und der Rahmen-Golden folgen in R11 · T002-Resume und T003-Client
            danach) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R10
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
R10 wires T001's reader to the route. `GET /api/jobs/<jid>/events/stream` is a
six-part path branch in `_RemedyHandler.do_GET`, `drain_sse_frames` writes the
generator's frames to the socket and ends the loop when the peer goes away, and
an unknown job answers 404 before one byte of stream. The server was already
threaded, so an open stream no longer blocks the rest of the cockpit.

## Next Steps
1. R11 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
2. R12 onward builds T002 — Last-Event-ID resume, read from the header or the
   query, and the forced-disconnect hammer whose transcript must byte-equal the
   ledger.
3. Then T003's client hook, backoff, gap detection and polling fallback, then
   the integration gate before closure.

## Risks
- A streaming handler holds a socket open. The reader cannot observe a broken
  pipe from inside a `yield`, so the writer owns the flag its `should_continue`
  reads; if that flag is ever dropped, a departed peer leaks a thread that
  polls the ledger forever.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0614, R-0615 and R-0616 stay routed to a paydown branch,
  together with promoting the fix clauses of R-0387 and R-0573 into the §3
  checklist.
<<<END PLANF008R10

<<<SLICE LEDGER10
Gate: R10 — the R9 entry. R9 PASSED with NO finding against it. R9 was a state-only round that recorded the R8 verdict, registered R-0615 and R-0616 and closed its session at the round cap, and it did exactly what its block ordered: no code path was touched, no id beyond those two was minted, and no deviation was declared beyond the DECISION D15 handback overage its own G12 anticipated. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `a063be56` rather than reading the handback's numbers back. Transport EQUAL two ways on disk — `.agent/authored/f008-r9.md` at `eab78492` and `.agent/last_block.md` at `24518a53` — at sha256 8a7cc9db5cc3f61cb9d474599e43752fa32345e047b44174786236c1e9949850 over 17587 bytes and 187 lines, with the working copy of the authored file equal to its committed blob. TWO SLICES by the reviewer's own ordered extraction out of the committed C0a file, newline-included: PLANF008R9 2edcd10a over 2503 bytes and 45 lines, LEDGER9 5c6bdb26 over 6372 bytes and 5 lines. THE PLAN LANDED FIRST at `6fc736ea`, byte-equal to PLANF008R9 at 45 lines under the 50-line cap, which is §3 checklist item 23 met rather than claimed. THE LEDGER APPEND at `61281cb2` is a byte-exact prefix plus a 6373-byte remainder equal to a newline plus LEDGER9, agreed by an INDEPENDENT blank-line split into 201 units whose LAST THREE equal LEDGER9's three paragraphs in order, with a one-byte flip REJECTED by both readings and the unflipped value ACCEPTED by both. THE SETS moved 186 to 188 with zero `Done:` and zero `Landed:` lines at both commits, `Gate: R` going 9 over nine DISTINCT keys, R-0615 and R-0616 each appearing exactly once and R-0617 nowhere, so exactly the two ordered ids were minted. FIVE single-parent commits whose insertions read 187, 101, 13, 6 and 33, every one under the 500-line cap and agreeing cell by cell with the handback's `## Commits` column. ZERO marker lines in any of the three targets, a reflog whose operations over this round's own commits are `commit` five times with `amend`, `rebase` and `cherry` at 0 each, a 67-line handback carrying the DECISION D15 stated-cause line its own overage requires, the tree clean with the primary checkout the only worktree, the branch pushed to `a063be56` and `gh pr list` returning an empty list. THE RUNS ARE THE REVIEWER'S OWN: the state readers exit 0 at 414 passed plus 0 skipped, and `tests/docs/` exits 0 at 295 passed plus 0 skipped, both re-run serially in the primary checkout and both equal to the values the block stated at `95326a5f`.
<<<END LEDGER10

<<<SLICE IMPORTFROM
import sys
from datetime import datetime, timezone
<<<END IMPORTFROM

<<<SLICE IMPORTTO
import sys
import time
from datetime import datetime, timezone
<<<END IMPORTTO

<<<SLICE DRAINFROM
def _get_frontend_dist() -> Path | None:
<<<END DRAINFROM

<<<SLICE DRAINTO
def drain_sse_frames(frames: Any, write: Any, flush: Any, stop: Any) -> int:
    """Write one stream's frames to a socket until the peer goes away.

    A generator suspended in `yield` cannot observe a broken pipe, so the
    writer is the only actor that can end the loop: on the first failed write
    it calls `stop`, which is what `iter_sse_frames`' `should_continue` reads.
    Without that call a departed peer leaks a thread polling the ledger for
    ever. Returns the number of frames that actually reached the socket.
    """
    written = 0
    for frame in frames:
        try:
            write(frame)
            flush()
        except (OSError, ValueError):
            # OSError covers BrokenPipeError and ConnectionResetError; a wfile
            # already closed by the server raises ValueError instead.
            stop()
            break
        written += 1
    return written


def _get_frontend_dist() -> Path | None:
<<<END DRAINTO

<<<SLICE ROUTEFROM
        # /api/layers
<<<END ROUTEFROM

<<<SLICE ROUTETO
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

        # /api/layers
<<<END ROUTETO

<<<SLICE METHODFROM
    def do_POST(self) -> None:  # noqa: N802
<<<END METHODFROM

<<<SLICE METHODTO
    def _send_sse_stream(self, job: Any, cursor: str, *,
                         now: Any = time.monotonic,
                         sleep: Any = time.sleep) -> None:
        """Stream one job's events to this connection until the peer leaves.

        `now` and `sleep` are injected for the same reason `iter_sse_frames`
        injects them: cadence is then a fact a test asserts rather than a
        duration it waits out.
        """
        start = int(cursor) if cursor.isdigit() else 0
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        alive = [True]

        def stop() -> None:
            alive[0] = False

        frames = iter_sse_frames(
            lambda: _load_events(job),
            start,
            now=now,
            sleep=sleep,
            should_continue=lambda: alive[0],
        )
        drain_sse_frames(frames, self.wfile.write, self.wfile.flush, stop)

    def do_POST(self) -> None:  # noqa: N802
<<<END METHODTO

<<<SLICE TESTS10


# A job the route can carry: `_load_job` is stubbed, so only the id is read.
class _Job:
    id = "11111111-2222-3333-4444-555555555555"


class _Socket:
    """A peer that accepts `until` frames and then goes away."""

    def __init__(self, until: int) -> None:
        self.frames: list[bytes] = []
        self.until = until

    def write(self, frame: bytes) -> None:
        if len(self.frames) >= self.until:
            raise BrokenPipeError
        self.frames.append(frame)

    def flush(self) -> None:
        return None


def _dispatch(monkeypatch: Any, path: str, job: Any, err: Any) -> tuple[list, list]:
    """Drive `do_GET` on a socketless handler and record what it answered."""
    monkeypatch.setattr(mod, "_load_job", lambda jid: (job, err))
    handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = ""
    handler.path = path
    answered: list[Any] = []
    streamed: list[Any] = []
    handler._send_json = lambda code, data: answered.append((code, data))
    handler._send_sse_stream = lambda j, cursor: streamed.append((j, cursor))
    handler.do_GET()
    return answered, streamed


class TestFrameDraining:
    def test_every_frame_reaches_the_socket_in_order(self):
        socket = _Socket(3)
        sent = mod.drain_sse_frames(
            iter([b"a", b"b", b"c"]), socket.write, socket.flush, lambda: None)
        assert socket.frames == [b"a", b"b", b"c"]
        assert sent == 3

    def test_a_broken_pipe_stops_the_reader(self):
        stopped: list[bool] = []
        socket = _Socket(0)
        # The generator is suspended in `yield` and cannot see the pipe break,
        # so nothing but this call can end its loop.
        sent = mod.drain_sse_frames(
            iter([b"a", b"b"]), socket.write, socket.flush,
            lambda: stopped.append(True))
        assert sent == 0
        assert stopped == [True]

    def test_a_disconnect_keeps_the_frames_already_written(self):
        socket = _Socket(2)
        sent = mod.drain_sse_frames(
            iter([b"a", b"b", b"c"]), socket.write, socket.flush, lambda: None)
        assert socket.frames == [b"a", b"b"]
        assert sent == 2

    def test_a_closed_socket_ends_the_stream_rather_than_raising(self):
        # A wfile the server has already closed raises ValueError, not OSError.
        def flush() -> None:
            raise ValueError("I/O operation on closed file")

        assert mod.drain_sse_frames(
            iter([b"a"]), lambda frame: None, flush, lambda: None) == 0


class TestStreamRoute:
    def test_the_stream_path_reaches_the_writer_with_its_cursor(self, monkeypatch):
        job = _Job()
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", job, None)
        assert answered == []
        assert streamed == [(job, "7")]

    def test_a_stream_without_a_cursor_starts_at_the_beginning(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert streamed[0][1] == "0"

    def test_an_unknown_job_answers_404_before_one_stream_byte(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/nope/events/stream?token=tok", None,
            (404, {"error": "job not found"}))
        assert streamed == []
        assert answered == [(404, {"error": "job not found"})]

    def test_a_bad_token_never_reaches_the_stream(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=wrong", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 403

    def test_the_cursor_endpoint_still_answers_beside_the_stream(self, monkeypatch):
        # The stream is a SIXTH path part, so the five-part branch is untouched.
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(2))
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events-since?token=tok&cursor=0", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 200
        assert [e["seq"] for e in answered[0][1]["events"]] == [0, 1]


class TestStreamResponse:
    def _handler(self, socket: Any) -> Any:
        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.sent_code = []
        handler.headers_out = []
        handler.send_response = handler.sent_code.append
        handler.send_header = lambda key, value: handler.headers_out.append((key, value))
        handler.end_headers = lambda: None
        handler.wfile = socket
        return handler

    def test_the_response_declares_an_event_stream(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(1))
        handler = self._handler(_Socket(0))
        clock = _Clock()
        handler._send_sse_stream(_Job(), "0", now=clock.now, sleep=clock.sleep)
        assert handler.sent_code == [200]
        assert dict(handler.headers_out)["Content-Type"] == "text/event-stream"
        assert dict(handler.headers_out)["Cache-Control"] == "no-store"

    def test_the_cursor_span_reaches_the_socket_without_renumbering(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(3))
        socket = _Socket(2)
        handler = self._handler(socket)
        clock = _Clock()
        handler._send_sse_stream(_Job(), "1", now=clock.now, sleep=clock.sleep)
        # Resumed at 1, so the ids are the ledger's own and not 0-based.
        assert [_parse(f)["id"] for f in socket.frames] == ["1", "2"]

    def test_a_non_numeric_cursor_streams_from_the_beginning(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(2))
        socket = _Socket(2)
        handler = self._handler(socket)
        clock = _Clock()
        handler._send_sse_stream(_Job(), "junk", now=clock.now, sleep=clock.sleep)
        assert [_parse(f)["id"] for f in socket.frames] == ["0", "1"]

    def test_the_departed_peer_ends_the_loop(self, monkeypatch):
        # Without `stop` this call never returns: the reader would poll the
        # ledger for ever on a socket nobody is reading.
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(1))
        handler = self._handler(_Socket(0))
        clock = _Clock()
        handler._send_sse_stream(_Job(), "0", now=clock.now, sleep=clock.sleep)
        assert handler.wfile.frames == []
<<<END TESTS10
