── STEP R8/1 — F008 SSE event stream · T001 reader, re-issued ─
Goal:        Register R-0614, record the R6 and R7 verdicts, and re-issue the
             bundle R7 halted on: T001's stream READER — the SSE frame
             builders, the safe per-event envelope both event transports
             share, and the frame generator carrying the ledger's own
             position as the SSE event id and sending a comment frame when
             idle. R7's worker was right to halt: one slice reached it with
             two byte-string literals' escapes doubled. Those characters are
             corrected, every other byte is the byte R7 measured, and R7's
             readings are re-derived here rather than carried over.

Bundle:      C0a save this block · C0b mirror it · C1 advance the plan ·
             C2 register R-0614 and record the R6 and R7 verdicts · C3 the
             reader in the UI server · C4 the domain tests · C5 handback.

Change:      Exactly these paths, and nothing else.
             - .agent/authored/f008-r8.md              (C0a, new)
             - .agent/last_block.md                    (C0b, rewrite)
             - .agent/plan.md                          (C1, rewrite)
             - .agent/live_review.md                   (C2, append)
             - packages/orchestration/ui_server.py     (C3, the pairs)
             - tests/ui_server/test_sse_stream.py      (C4, new)
             - .agent/handoff.md                       (C5, rewrite)

Constraints:
 1. Every slice is applied byte for byte out of the COMMITTED
    .agent/authored/f008-r8.md, extracted by its marker lines — never
    retyped, rewrapped, reflowed or edited. A slice that looks wrong is
    APPLIED AS WRITTEN and the objection goes in the handback — R7 halted on
    exactly such an objection and was right to.
 2. NEWLINE CONVENTION, stated not assumed. A slice body is the lines
    strictly between its `<<<SLICE X` and `<<<END X` markers. PLANF008R8 and
    TESTSSE are applied with their trailing newline INCLUDED and are the
    ENTIRE content of their files. LEDGER is applied as a newline plus its
    body, appended to `.agent/live_review.md` after exactly one blank line.
    Each FROM/TO body carries its newline; every file ends with one.
 3. The commit order is exactly C0a, C0b, C1, C2, C3, C4, C5.
    `.agent/plan.md` is advanced at C1, the first substantive commit, and the
    finding is registered at C2, before either fix commit.
 4. PAIR SHAPES, measured mechanically by the reviewer at emission and given
    here as the containment test's own output, one reading per pair: SUMMARY
    `TO contains FROM: false` so REWRITE · HELPERS `TO contains FROM: true`
    so APPEND. Each FROM occurs EXACTLY ONCE in
    `packages/orchestration/ui_server.py` at `83408011`, measured there by
    the same script. The REWRITE pair carries the "FROM 0x, TO 1x"
    obligation; the APPEND pair carries §4.9's ORDERED-EQUALITY obligation
    for code and NEVER a FROM-zero count. No import is added or moved: the
    generator's return annotation is `Any`, already imported by this file.
 5. SUMMARY IS APPLIED BEFORE HELPERS, both in C3 — one change: the reader
    and the call site it shares with the cursor endpoint.
 6. LEDGER carries THREE paragraphs, blank-line separated, applied together
    in C2: the R-0614 registration, the `Gate: R7` entry holding the R6
    verdict, and the `Gate: R8` entry holding the R7 verdict. R-0614 is the
    ONLY id minted, so the next free id becomes R-0615.
 7. NO OTHER PRODUCTION PATH. Nothing under apps/, docs/ or scripts/ is
    touched and inside packages/ only `ui_server.py` is. `.agent/context.md`
    is deliberately absent too: its clause "T001's endpoint itself is NOT
    built yet" stays true after C3, which lands the reader and no endpoint.
 8. `git status --porcelain` is empty after every commit and at the handback.
    The RED PROOF of G11 is the only destructive step this round and it runs
    ONLY inside a disposable git worktree under `.remedy-wt/`, removed and
    pruned before the handback.
 9. Two pytest processes never run at once, and every suite command runs in
    the PRIMARY checkout.
10. The reviewer's own readings at `83408011`, taken before this block was
    emitted and RE-DERIVED by the gates below rather than trusted: the
    combined state-reader suite exits 0 with `passed + skipped` equal to 400,
    and `tests/docs/` exits 0 at 295. Count by passed-plus-skipped, never by
    a bare passed count — data-dependent `pytest.skip(...)` calls in
    `test_brain_view_model.py` and `test_dashboard_contract.py` move the
    split at an unchanged tree, and the reviewer saw that 400 at two splits.
11. DO NOT MERGE, DO NOT OPEN A PULL REQUEST, DO NOT CREATE A BRANCH. F008 is
    mid-feature. The branch is pushed and left open for the next round.

Done when:
 G1  `.agent/STOP` is absent, read immediately before C0a; the branch is
     feature/f008-sse-event-stream; `git status --porcelain` is empty after
     every commit and at the handback, where `git worktree list` names the
     primary checkout alone. Report each reading.
 G2  Transport. Report the sha256, byte count and line count of the scratch
     block the worker was given, of `.agent/authored/f008-r8.md` at C0a and
     of `.agent/last_block.md` at C0b, and whether all three are EQUAL.
 G3  Slice inventory. Extract the slices from the COMMITTED
     `.agent/authored/f008-r8.md` by their marker lines, take the COUNT from
     that listing, and report each slice's newline-INCLUDED sha256/bytes/lines.
 G4  Plan. Report the sha256, bytes and lines of `.agent/plan.md` at C1 and
     whether it is byte-equal to PLANF008R8. Its line count is under 50,
     `## Goal` and `## Next Steps` each occur exactly once line-anchored, and
     `F008` occurs at least once.
 G5  The ledger append, measured two ways that must agree. C2 against C1:
     (a) the C1 blob is a byte-exact PREFIX of the C2 blob and the remainder
     equals a newline plus LEDGER — report its sha256, bytes and lines;
     (b) an INDEPENDENT blank-line split of the C2 file, its terminating
     newline normalised first, has as its LAST THREE units, in order, the
     three paragraphs of LEDGER. NEGATIVE CONTROL: flip one byte of the
     remainder and report BOTH readings reject it, the unflipped accepted.
 G6  The sets. Report line-anchored counts in `.agent/live_review.md` at C1
     and C2: `^- R-\d+ — ` reads 185 then 186 — constraint 6, R-0614 is the
     only id minted — `^Done: R-\d+ — ` is 0 at both, `^Landed: ` is 0 at
     both, and `^Gate: R\d+ — ` reads 6 then 8 with the eight keys DISTINCT.
     `^- R-0614 — ` reads 0 then 1, and `^- R-0615 — ` is 0 at both.
 G7  The pairs landed. For `packages/orchestration/ui_server.py`, report at
     `83408011` and at C3 the count of each FROM and each TO body: the
     SUMMARY FROM is 1 then 0, and for the APPEND pair report instead that
     the C3 blob CONTAINS the HELPERS TO body exactly once. Report
     `git show --numstat C3 -- packages/orchestration/ui_server.py`; it reads
     78 insertions and 11 deletions.
 G8  Ordered equality for the APPEND pair, §4.9's obligation for a code
     slice: the lines C3's diff ADDS to `packages/orchestration/ui_server.py`
     are, IN ORDER, exactly the HELPERS TO lines absent from its FROM body.
     Report both line counts and whether the comparison holds.
 G9  The test file. Report the sha256, byte count and line count of
     `tests/ui_server/test_sse_stream.py` at C4 and whether it is byte-equal
     to TESTSSE. Report `git show --numstat C4` for that path; being a new
     file, insertions equal its line count and deletions are 0.
 G10 The suites, in the PRIMARY checkout, run SERIALLY, never two pytest
     processes at once. Report the exit code and `passed + skipped` of:
     `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q -rf`
     It exits 0 and sums to 414. Then report the same two values for
     `python3 -m pytest tests/docs/ -q -rf`, which exits 0 and sums to 295.
     Per constraint 10 report the SUM, never a bare passed count, and do not
     read a skip as a failure. Report the arithmetic reconciling 414 against
     constraint 10's 400 and the new file's test count from
     `python3 -m pytest tests/ui_server/test_sse_stream.py --collect-only -q`.
 G11 RED PROOF, inside a disposable git worktree under `.remedy-wt/`, NEVER
     in the primary checkout. There, restore
     `packages/orchestration/ui_server.py` alone to its blob at `83408011`,
     leave `tests/ui_server/test_sse_stream.py` in place, run
     `python3 -m pytest tests/ui_server/test_sse_stream.py -q -rf` and report
     the exit code and outcome counts: it EXITS NON-ZERO and reports NO
     passing test. Then restore the file to its C3 blob, report the two are
     byte-identical, re-run and report exit 0. Remove and prune the worktree
     and report `git worktree list`. The reviewer ran this revert before
     emission and saw non-zero with no test passing.
 G12 Lint, scoped to the two paths this round writes and measured against the
     SAME paths at `83408011`, read WITHOUT writing the checkout — via
     `git show 83408011:<path>` into scratch under `.remedy-wt/`, or inside
     the disposable worktree. Report the exit code and rule-code multiset of
     `python3 -m ruff check --output-format json <path>` for
     `packages/orchestration/ui_server.py` at the base and at C3, and for
     `tests/ui_server/test_sse_stream.py` at C4: all three exit 0 with an
     EMPTY multiset. BEFORE believing any of the three, run the extractor
     once on input known to be RED — a scratch file under `.remedy-wt/` with
     unsorted imports and an undefined name — and report the NON-EMPTY
     multiset it returns (R-0573). Ruff is BLIND to R-0614's defect, so an
     empty multiset settles lint and nothing about the frames: G10/G11 do.
 G13 Range. With BASE `83408011`, `git diff --name-only BASE..C5` equals the
     Change list above with no path on either side alone. Every commit in
     BASE..C5 has exactly one parent. Report each commit's INSERTION count
     from `git show --numstat`, all under 500, and compare them cell by cell
     against the `+/-` column of the handback's `## Commits` table, reporting
     agreement. C5's own numbers belong to the round report (R-0149).
 G14 Marker leak. Count LINES BEGINNING with `<<<SLICE ` or `<<<END ` in
     `.agent/plan.md` at C1, `.agent/live_review.md` at C2,
     `packages/orchestration/ui_server.py` at C3,
     `tests/ui_server/test_sse_stream.py` at C4 and `.agent/handoff.md` at
     C5. Every count is 0.
 G15 History. Over this round's OWN reflog entries, report the count whose
     OPERATION — the text before the first `:` in `git reflog --format=%gs`
     — is `amend`, `rebase` or `cherry`; it is 0. Count by operation, never
     by substring; do not order that every entry read `commit:`; no total.
 G16 The branch is pushed and NO pull request exists. Report the real output
     of `git push` and of
     `gh pr list --state open --json number,headRefName,baseRefName,isDraft`,
     which returns an empty list. Nothing is merged this round.
 G17 Handback. `.agent/handoff.md` at C5 carries the sections
     docs/agents/handback_template.md mandates and an item-status table
     naming C0a, C0b, C1, C2, C3, C4 and C5 exactly once each. Report its
     line count; the cap is 100, this round having more than five commits.
     Its `## Next` section states, in this order, that the next session's
     FIRST action is the `.agent/STOP` re-read (Phase 1 rule 1) and its
     SECOND the Open PR Gate (Phase 1 rule 2), continuing here at R9.

Handback:   completion report + rewrite .agent/handoff.md.

            Fortschritt: 25 % (F008 beansprucht · acht Urteile im Ledger ·
            DECISION F008 D1 vollständig umgesetzt · T001-Leser gebaut —
            SSE-Rahmen, geteilte Hülle, Herzschlag-Kadenz · Route und
            Socket-Schreiber folgen in R9) — Schätzung
──────────────────────────────────────────────────────────────

<<<SLICE PLANF008R8
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
R8 registers R-0614, records the R6 and R7 verdicts, and re-issues the bundle
R7 halted on: T001's stream READER — the SSE frame builders, the safe
per-event envelope both event transports share, and the frame generator that
carries the ledger position as the event id and heartbeats while idle. R7
halted because one authored slice reached its worker with the escapes of two
byte-string literals doubled; those characters are corrected here and every
other byte of the bundle is unchanged.

## Next Steps
1. R9 wires the reader to the route: `GET /api/jobs/<jid>/events/stream` as a
   six-part path branch beside the existing `events-since` handler in
   `_RemedyHandler.do_GET`, the response writer that drains the generator into
   the socket, and 404 for an unknown job before one byte of stream.
2. R10 adds the per-job connection cap answering 429 beyond it and the framing
   golden the feature file names as T001's contract test.
3. R11 onward builds T002 — Last-Event-ID resume and the forced-disconnect
   hammer whose transcript must byte-equal the ledger — then T003's client
   hook and fallback, then the integration gate before closure.

## Risks
- A streaming handler holds a socket open. The reader takes `should_continue`
  from its caller, so R9's writer must bound the loop by the peer's
  disconnect, and no test may drive that route over a real socket without a
  hard timeout and a guaranteed close.
- No open finding is a code defect of F008. R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613 and R-0614 stay routed to a paydown branch, together with
  promoting the fix clauses of R-0387 and R-0573 into the §3 checklist.
<<<END PLANF008R8

<<<SLICE LEDGER
- R-0614 — Medium — A BLOCK SHIPPED A SLICE THE REVIEWER HAD NEVER RUN, BECAUSE THE DRY RUN CONSUMED AN EVALUATED FORM OF THE TEXT WHILE THE BLOCK CARRIED ITS RAW SOURCE. The F008 R7 block, delivered on disk and received intact at sha256 c57ddb619a288a17081ba32e9c8f7f5fa94de6ac6cfa6bdc3b5679392be859bf over 26837 bytes and 488 lines, carried a HELPERSTO slice whose two byte-string literals read `\\n` where the applied file needs `\n`. In Python source a doubled escape is a backslash followed by `n`, so `sse_event_frame` and `sse_heartbeat_frame` would emit literal backslash-n text instead of the line breaks that terminate an SSE frame, while the TESTSSE slice of the same block asserts real newlines. THE TWO HALVES OF THE BLOCK CONTRADICTED EACH OTHER AND CONSTRAINT 1 FORBADE REPAIRING EITHER, so the round could only halt. THE MECHANISM IS THE FINDING, not the two characters. The reviewer held the slice as a triple-quoted Python literal inside its own scratch applier; the dry run applied that literal's EVALUATED value and went green, and the block was then built by a second script that extracted the same literal's RAW SOURCE with a regex and never evaluated it. Both scripts "measured" the slice, each was correct about the bytes it saw, and nothing ever compared the two — so a green dry run certified a byte string the block did not contain. NEITHER STANDING GUARD REACHED IT: checklist item 12 binds the COMMAND a dry run runs, and this command was exact, while ruff is blind by construction because a doubled escape is valid Python — `ruff check` returned an empty multiset at exit 0 over the very file whose frames were broken. THE COST WAS ONE ROUND AND THE EVIDENCE IS MEASURED TWICE: the worker applied both slices verbatim in a disposable worktree and read 7 failed with 7 passed at the C3 state against 14 failed with 0 passed at the base, and the reviewer reproduced 7 failed with 7 passed independently at `83408011`. The seven survivors are the tests that never parse a frame, which is why the split is 7 and not 14. THE COUNTER-MEASURE IS A ROUND TRIP, and it is cheap: once the FINAL block bytes exist, extract every slice FROM THAT BLOCK by its marker lines, run the green and red proofs from THAT extraction, and report each extracted slice's sha256 beside the bytes the proof consumed. A slice that has not been round-tripped through the emitted block has not been verified, however green the run was. This finding is Medium rather than Low because the failure is silent, general and lands on the worker: every future code slice carried by a generator is exposed to it, the lint gate cannot see it, and the only actor positioned to catch it is the one forbidden to fix it.

Gate: R7 — the R6 entry. R6 PASSED with NO finding against its work and none against its block. R6 wrote no code by design: it recorded the R5 verdict, advanced the plan and the branch context, and closed a session at its stated round cap, which self-drive protocol G7 calls a SUCCESS rather than a failure. THE REVIEWER RE-DERIVED EVERY GATE ITSELF at `cc27ff16` instead of reading the handback's numbers back. Transport EQUAL three ways — the scratch block, `.agent/authored/f008-r6.md` at `42a923b8` and `.agent/last_block.md` at `a64f05f0` — at sha256 a3c2fd22641eb0f453ec32eab3f8d659aee5a71092a2c2011b90bdd51fe9c3df over 20619 bytes and 258 lines; three slices by the reviewer's own ordered extraction at `ceb79ebe`, `8c7b4f8d` and `ffeb3687`; `.agent/plan.md` at `5916cfa6` byte-equal to its slice at 44 lines under the 50-line cap, with `## Goal` and `## Next Steps` line-anchored once each; the verdict append at `12a3ac6d` a byte-exact prefix plus a 4926-byte remainder equal to a newline plus the slice, agreed by an INDEPENDENT blank-line split into 195 units whose last unit matches, with a one-byte flip at offset 100 REJECTED by both readings while the unflipped value was accepted by both; `.agent/context.md` at `39e872e9` byte-equal to its slice at 57 lines carrying every substring its live readers assert; the registered set unmoved at 185 with zero `Done:` and zero `Landed:` lines and `Gate: R` going 5 to 6 over six DISTINCT keys, so no id was minted; six single-parent commits whose insertions read 258, 188, 21, 2, 25 and 35, every one under the 500-line cap and agreeing cell by cell with the handback's own `## Commits` column for the five commits that column can honestly reach; zero marker lines in any target; a reflog whose operations are `commit` throughout, so zero amend, rebase or cherry; and the tree clean with the primary checkout the only worktree and the branch pushed, `gh pr list` returning an empty list. THE TWO SUITES ARE THE REVIEWER'S OWN RUNS AND NOT THE WORKER'S: the state readers exit 0 at 400 passed plus 0 skipped, and `tests/docs/` exits 0 at 295 passed plus 0 skipped. That 400 is the same TOTAL the worker reported at a different passed-to-skipped split, which is exactly what the block's constraint 8 predicted and precisely why passed-plus-skipped is the reading here and a bare passed count is not. NO DEVIATION WAS DECLARED AND NONE WAS OWED.

Gate: R8 — the R7 entry. R7 HALTED WITH ONE COMMIT, AND ITS WORKER WAS RIGHT TO HALT: the defect was in the reviewer's block, and the round's own conduct is the model this workflow exists to produce. Finding R-0614 records the defect and the mechanism behind it. THE WORKER DID EVERY THING THE PROTOCOL ASKS AND NOTHING IT FORBIDS: it verified receipt before touching anything and matched all three ordered readings; it executed every gate G1 through G17 rather than reasoning about them; it refused to edit the defective slice, which constraint 1 forbids; it refused to land the code, which would have put a red tip on the branch and made R8's own red proof dishonest; it refused to land the plan slice, whose Current Step asserts work that did not happen; it declared the six skipped commits as a deviation with its reason; and it left the tree clean, the worktree list bare and the branch pushed with no pull request. A ROUND THAT HALTS ON A CONTRADICTION IT DID NOT CREATE IS NOT A FAILED ROUND. THE REVIEWER RE-DERIVED THE HALT ITSELF at `83408011`: applying the block's SHIPPED SUMMARY and HELPERS slices verbatim in a disposable worktree and running the block's own G11 command reproduces 7 failed with 7 passed, against the worker's identical reading, and the block's base half of 14 failed with 0 passed stands unchanged. EVERYTHING ELSE IN THE BLOCK WAS CONFIRMED BY BOTH ACTORS AND SURVIVES INTO R8 UNTOUCHED: seven slices by ordered extraction, SUMMARY a REWRITE and HELPERS an APPEND by mechanical containment, 78 insertions against 11 deletions on the source path, ordered equality holding for the append, empty ruff multisets at base and at head behind a red control that returned four codes, and the suites at 400 and 295 with 14 collected tests reconciling to 414. THE ONE COMMIT IS HONEST STATE: `83408011` writes only `.agent/handoff.md`, at 78 lines under its cap, with the item table naming every planned commit and its status. R7's plan was deliberately left at its R6 text rather than advanced to a false sentence, which is the same judgement the halt was.
<<<END LEDGER

<<<SLICE SUMMARYFROM
    safe = []
    for offset, e in enumerate(new_events[:50]):
        safe.append({
            # The ledger's own position, never a per-response counter: F008's
            # stream uses it as the SSE event id, so a client resuming from
            # `seq` lands on the event the server meant (DECISION F008 D1).
            "seq": start + offset,
            "event": e.get("event", ""),
            "timestamp": e.get("timestamp", ""),
            "outcome": e.get("outcome", ""),
        })
<<<END SUMMARYFROM

<<<SLICE SUMMARYTO
    safe = [
        _safe_event_summary(start + offset, e)
        for offset, e in enumerate(new_events[:50])
    ]
<<<END SUMMARYTO

<<<SLICE HELPERSFROM
def _get_frontend_dist() -> Path | None:
<<<END HELPERSFROM

<<<SLICE HELPERSTO
#: Seconds of silence after which the stream sends a heartbeat comment frame.
#: Proxies drop idle connections, and an SSE comment is the no-op that holds
#: one open without ever entering the client's event stream.
SSE_HEARTBEAT_SECONDS = 15.0

#: Seconds the stream waits before re-reading the ledger for new events.
SSE_POLL_SECONDS = 1.0


def _safe_event_summary(seq: int, event: dict[str, Any]) -> dict[str, Any]:
    """The safe per-event envelope both event transports carry.

    The cursor endpoint and the SSE stream are one consumer contract over two
    transports, so this summary has ONE writer: a field added here reaches
    both or neither. `seq` is the ledger's own position and never a
    per-response counter, so a client resuming from it lands on the event the
    server meant (DECISION F008 D1).
    """
    return {
        "seq": seq,
        "event": event.get("event", ""),
        "timestamp": event.get("timestamp", ""),
        "outcome": event.get("outcome", ""),
    }


def sse_event_frame(seq: int, payload: dict[str, Any]) -> bytes:
    """One SSE event frame whose id is the ledger position it carries."""
    return f"id: {seq}\ndata: {json.dumps(payload, default=str)}\n\n".encode()


def sse_heartbeat_frame() -> bytes:
    """The SSE comment frame that holds an idle connection open.

    A comment carries no `id:`, `event:` or `data:` field, so a client never
    surfaces it as an event and a resuming client never asks to replay it.
    """
    return b": heartbeat\n\n"


def iter_sse_frames(
    load_events: Any,
    start: int,
    *,
    now: Any,
    sleep: Any,
    should_continue: Any,
    heartbeat_seconds: float = SSE_HEARTBEAT_SECONDS,
    poll_seconds: float = SSE_POLL_SECONDS,
) -> Any:
    """Yield one job's SSE frames from `start`, heartbeating while idle.

    Every collaborator that touches time is injected — `now`, `sleep` and
    `should_continue` — so cadence is a fact a test asserts rather than a
    duration it waits out. The response handler that writes these frames to a
    socket arrives with the route; this is the reader it will drive.
    """
    cursor = start
    last_frame_at = now()
    while should_continue():
        events = load_events()
        if cursor < len(events):
            for seq in range(cursor, len(events)):
                yield sse_event_frame(seq, _safe_event_summary(seq, events[seq]))
            cursor = len(events)
            last_frame_at = now()
            continue
        if now() - last_frame_at >= heartbeat_seconds:
            yield sse_heartbeat_frame()
            last_frame_at = now()
            continue
        sleep(poll_seconds)


def _get_frontend_dist() -> Path | None:
<<<END HELPERSTO

<<<SLICE TESTSSE
"""
Domain tests: ui_server/test_sse_stream.py

T001's stream reader: frames carry the ledger's own position as the SSE event
id, an idle stream heartbeats with a comment frame, and every collaborator
that touches time is injected so cadence is asserted rather than waited out.
"""

from __future__ import annotations

import json
from typing import Any

from packages.orchestration import ui_server as mod


def _events(count: int) -> list[dict[str, Any]]:
    return [
        {"event": f"e{i}", "timestamp": f"2026-08-21T00:00:{i:02d}Z", "outcome": "ok"}
        for i in range(count)
    ]


# A hand-wound clock: the test decides what time it is.
class _Clock:
    def __init__(self) -> None:
        self.t = 0.0
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds


def _budget(passes: int) -> Any:
    """A `should_continue` that permits exactly `passes` loop passes."""
    left = [passes]

    def should_continue() -> bool:
        if left[0] <= 0:
            return False
        left[0] -= 1
        return True

    return should_continue


def _run(load_events: Any, start: int, passes: int, clock: _Clock) -> list[bytes]:
    return list(mod.iter_sse_frames(
        load_events, start, now=clock.now, sleep=clock.sleep,
        should_continue=_budget(passes),
        heartbeat_seconds=15.0, poll_seconds=1.0,
    ))


def _parse(frame: bytes) -> dict[str, str]:
    """Split one event frame into its SSE fields."""
    assert frame.endswith(b"\n\n")
    fields: dict[str, str] = {}
    for line in frame.decode().rstrip("\n").split("\n"):
        key, _, value = line.partition(": ")
        fields[key] = value
    return fields


class TestFrameShape:
    def test_the_event_id_is_the_ledger_position(self):
        # Not the position within THIS response: a stream that renumbered
        # would say 0 for the first frame it happened to send.
        assert _parse(mod.sse_event_frame(7, {"seq": 7}))["id"] == "7"

    def test_the_data_line_is_the_json_envelope(self):
        payload = {"seq": 3, "event": "task_started", "timestamp": "t", "outcome": "ok"}
        assert json.loads(_parse(mod.sse_event_frame(3, payload))["data"]) == payload

    def test_the_heartbeat_is_a_comment_and_not_an_event(self):
        frame = mod.sse_heartbeat_frame()
        assert frame.startswith(b":")
        assert frame.endswith(b"\n\n")
        # No field a client can surface, so an idle stream stays silent to the
        # consumer and a resuming client never asks to replay a heartbeat.
        for field in (b"data:", b"id:", b"event:"):
            assert field not in frame

    def test_the_envelope_carries_the_safe_fields_only(self):
        summary = mod._safe_event_summary(2, {"event": "x", "timestamp": "t", "outcome": "ok"})
        assert set(summary) == {"seq", "event", "timestamp", "outcome"}

    def test_the_cursor_endpoint_and_the_stream_share_one_envelope(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(3))

        class _Job:
            id = "11111111-2222-3333-4444-555555555555"

        polled = mod._build_events_since_json(_Job(), "0")["events"]
        streamed = [json.loads(_parse(f)["data"])
                    for f in _run(lambda: _events(3), 0, 1, _Clock())]
        # Equal payloads: a field added to one can never be missing from the
        # other, because both come from the one envelope writer.
        assert streamed == polled


class TestStreamFrames:
    def test_every_event_from_the_cursor_is_streamed_in_ledger_order(self):
        frames = _run(lambda: _events(4), 0, 1, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["0", "1", "2", "3"]

    def test_a_cursor_resumes_without_renumbering(self):
        frames = _run(lambda: _events(5), 2, 1, _Clock())
        # First frame after a resume is 2, not 0: the ledger numbers, the
        # stream only carries the numbering.
        assert [_parse(f)["id"] for f in frames] == ["2", "3", "4"]

    def test_a_cursor_past_the_end_streams_no_event(self):
        frames = _run(lambda: _events(3), 9, 1, _Clock())
        assert [f for f in frames if not f.startswith(b":")] == []

    def test_events_appended_during_the_stream_continue_the_numbering(self):
        growing = [_events(2)]
        frames = _run(lambda: growing.pop(0) if growing else _events(4), 0, 2, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["0", "1", "2", "3"]


class TestHeartbeatCadence:
    def test_an_idle_stream_stays_silent_before_the_interval(self):
        clock = _Clock()
        assert _run(lambda: [], 0, 3, clock) == []
        assert clock.slept == [1.0, 1.0, 1.0]

    def test_one_heartbeat_is_sent_once_the_interval_has_passed(self):
        assert _run(lambda: [], 0, 16, _Clock()) == [mod.sse_heartbeat_frame()]

    def test_the_heartbeat_interval_restarts_after_each_frame(self):
        # Cadence, not a count of ticks: 30 slept seconds carry two beats.
        assert _run(lambda: [], 0, 32, _Clock()) == [mod.sse_heartbeat_frame()] * 2

    def test_an_event_defers_the_next_heartbeat(self):
        served = [_events(1)]
        frames = _run(lambda: served.pop(0) if served else _events(1), 0, 15, _Clock())
        # 14 idle seconds after the event is one short of the interval.
        assert [f for f in frames if f.startswith(b":")] == []

    def test_the_default_interval_is_fifteen_seconds(self):
        assert mod.SSE_HEARTBEAT_SECONDS == 15.0
<<<END TESTSSE
